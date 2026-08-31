"""Recurring-campaign engine: schedule math, freshness gate, occurrence spawning."""

from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

from django.utils import timezone

from email_marketing.models import Campaign, CampaignBlock, CampaignSchedule
from email_marketing.services.recurrence import (
    compute_next_run,
    has_fresh_content,
    run_due_schedule,
)

from .base import MarketingTestCase


def _post(title, days_ago):
    from blog.models import BlogPost

    return BlogPost.objects.create(
        title=title,
        status="published",
        excerpt="x",
        published_at=timezone.now() - timedelta(days=days_ago),
    )


class ComputeNextRunTests(MarketingTestCase):
    def _sched(self, **kw):
        campaign = Campaign.objects.create(
            site=self.site, name="T", subject="S", campaign_type=Campaign.TYPE_RECURRING
        )
        defaults = {
            "campaign": campaign,
            "send_time": time(9, 0),
            "timezone": "UTC",
        }
        defaults.update(kw)
        return CampaignSchedule.objects.create(**defaults)

    def test_weekly_picks_the_next_target_weekday_at_send_time(self):
        sched = self._sched(cadence="weekly", weekday=0, send_time=time(9, 0))  # Monday 09:00
        after = datetime(2026, 1, 7, 12, 0, tzinfo=ZoneInfo("UTC"))  # Wed 2026-01-07
        nxt = compute_next_run(sched, after)
        self.assertEqual(nxt.weekday(), 0)
        self.assertEqual((nxt.hour, nxt.minute), (9, 0))
        self.assertEqual((nxt.year, nxt.month, nxt.day), (2026, 1, 12))  # next Monday

    def test_daily_advances_to_next_day_when_todays_time_passed(self):
        sched = self._sched(cadence="daily", send_time=time(8, 0))
        after = datetime(2026, 1, 7, 12, 0, tzinfo=ZoneInfo("UTC"))
        nxt = compute_next_run(sched, after)
        self.assertEqual((nxt.month, nxt.day, nxt.hour), (1, 8, 8))

    def test_monthly_clamps_day_to_the_month_length(self):
        sched = self._sched(cadence="monthly", day_of_month=31, send_time=time(9, 0))
        after = datetime(2026, 1, 31, 12, 0, tzinfo=ZoneInfo("UTC"))
        nxt = compute_next_run(sched, after)
        self.assertEqual((nxt.month, nxt.day), (2, 28))  # Feb clamps 31 -> 28


class FreshnessGateTests(MarketingTestCase):
    def _template(self, source="since_last_send"):
        campaign = Campaign.objects.create(
            site=self.site,
            name="N",
            subject="S",
            campaign_type=Campaign.TYPE_RECURRING,
            last_content_sent_at=timezone.now() - timedelta(days=5),
        )
        CampaignBlock.objects.create(
            campaign=campaign,
            block_type="blog_posts",
            content={"source": source, "count": "3", "layout": "list"},
            order=0,
        )
        return campaign

    def test_fresh_when_a_post_is_newer_than_the_watermark(self):
        campaign = self._template()
        _post("New", days_ago=1)
        self.assertTrue(has_fresh_content(campaign, campaign.last_content_sent_at))

    def test_not_fresh_when_all_posts_predate_the_watermark(self):
        campaign = self._template()
        _post("Old", days_ago=10)
        self.assertFalse(has_fresh_content(campaign, campaign.last_content_sent_at))

    def test_latest_mode_block_is_not_delta_sensitive_so_always_fresh(self):
        campaign = self._template(source="latest")
        _post("Old", days_ago=10)
        self.assertTrue(has_fresh_content(campaign, campaign.last_content_sent_at))

    def test_campaign_without_delta_blocks_is_always_fresh(self):
        campaign = Campaign.objects.create(site=self.site, name="Static", subject="S")
        CampaignBlock.objects.create(
            campaign=campaign, block_type="heading", content={"text": "Hi"}, order=0
        )
        self.assertTrue(has_fresh_content(campaign, None))

    def test_product_grid_new_since_send_is_delta_aware(self):
        from tests.factories import ProductFactory

        campaign = Campaign.objects.create(
            site=self.site,
            name="P",
            subject="S",
            campaign_type=Campaign.TYPE_RECURRING,
            last_content_sent_at=timezone.now() - timedelta(days=5),
        )
        CampaignBlock.objects.create(
            campaign=campaign,
            block_type="product_grid",
            content={"mode": "new_since_send", "count": "3"},
            order=0,
        )
        # No products added since the watermark → not fresh.
        self.assertFalse(has_fresh_content(campaign, campaign.last_content_sent_at))
        # A newly-added published product → fresh.
        ProductFactory(name="Just added", status="published")
        self.assertTrue(has_fresh_content(campaign, campaign.last_content_sent_at))


class RunDueScheduleTests(MarketingTestCase):
    def _template_and_schedule(self, policy=CampaignSchedule.POLICY_SKIP):
        template = Campaign.objects.create(
            site=self.site,
            name="Weekly digest",
            subject="News",
            campaign_type=Campaign.TYPE_RECURRING,
            last_content_sent_at=timezone.now() - timedelta(days=7),
        )
        CampaignBlock.objects.create(
            campaign=template,
            block_type="blog_posts",
            content={"source": "since_last_send", "count": "3", "layout": "list"},
            order=0,
        )
        schedule = CampaignSchedule.objects.create(
            campaign=template,
            cadence="weekly",
            weekday=0,
            send_time=time(9, 0),
            timezone="UTC",
            freshness_policy=policy,
            next_run_at=timezone.now() - timedelta(minutes=1),
        )
        return template, schedule

    def test_skip_policy_sends_nothing_when_no_new_content(self):
        template, schedule = self._template_and_schedule(CampaignSchedule.POLICY_SKIP)
        _post("Stale", days_ago=30)  # older than the watermark

        result = run_due_schedule(schedule, timezone.now())

        self.assertEqual(result["outcome"], "skipped")
        self.assertEqual(Campaign.objects.filter(parent=template).count(), 0)
        schedule.refresh_from_db()
        self.assertGreater(schedule.next_run_at, timezone.now())  # advanced

    def test_sends_an_occurrence_when_content_is_fresh(self):
        template, schedule = self._template_and_schedule(CampaignSchedule.POLICY_SKIP)
        _post("Fresh news", days_ago=1)
        before = template.last_content_sent_at

        result = run_due_schedule(schedule, timezone.now())

        self.assertEqual(result["outcome"], "sent")
        occurrence = Campaign.objects.get(parent=template)
        self.assertEqual(occurrence.campaign_type, Campaign.TYPE_BROADCAST)
        template.refresh_from_db()
        self.assertGreater(template.last_content_sent_at, before)  # watermark advanced
        schedule.refresh_from_db()
        self.assertEqual(schedule.occurrences_sent, 1)

    def test_send_partial_policy_sends_even_when_stale(self):
        template, schedule = self._template_and_schedule(CampaignSchedule.POLICY_SEND_PARTIAL)
        _post("Stale", days_ago=30)

        result = run_due_schedule(schedule, timezone.now())

        self.assertEqual(result["outcome"], "sent")
        self.assertEqual(Campaign.objects.filter(parent=template).count(), 1)

    def test_hold_policy_postpones_then_expires_after_the_window(self):
        template, schedule = self._template_and_schedule(CampaignSchedule.POLICY_HOLD)
        schedule.hold_days = 3
        schedule.save(update_fields=["hold_days"])
        _post("Stale", days_ago=30)

        held = run_due_schedule(schedule, timezone.now())
        self.assertEqual(held["outcome"], "held")
        self.assertEqual(Campaign.objects.filter(parent=template).count(), 0)
        schedule.refresh_from_db()
        self.assertIsNotNone(schedule.hold_until)

        # Simulate the hold window having elapsed.
        schedule.hold_until = timezone.now() - timedelta(minutes=1)
        schedule.save(update_fields=["hold_until"])
        expired = run_due_schedule(schedule, timezone.now())
        self.assertEqual(expired["outcome"], "hold_expired")
        self.assertEqual(Campaign.objects.filter(parent=template).count(), 0)


class RecurringABTests(MarketingTestCase):
    def _ab_template_and_schedule(
        self, subjects=("Subject A", "Subject B"), sample=100, audience=12
    ):
        template = Campaign.objects.create(
            site=self.site,
            name="Weekly A/B digest",
            subject="Base",
            campaign_type=Campaign.TYPE_RECURRING,
        )
        # A static (non-delta) block keeps the freshness gate open every run.
        CampaignBlock.objects.create(
            campaign=template, block_type="heading", content={"text": "Hi"}, order=0
        )
        for i in range(audience):
            self.make_anon_emailable(f"aud{i}@ex.com")
        schedule = CampaignSchedule.objects.create(
            campaign=template,
            cadence="weekly",
            weekday=0,
            send_time=time(9, 0),
            timezone="UTC",
            next_run_at=timezone.now() - timedelta(minutes=1),
            ab_test_subjects=list(subjects),
            ab_sample_percent=sample,
            ab_test_window_hours=4,
            ab_winner_metric="opens",
            ab_auto_send_winner=True,
        )
        return template, schedule

    def test_occurrence_runs_a_subject_ab_test_when_configured(self):
        from email_marketing.models import ABTest

        template, schedule = self._ab_template_and_schedule()

        result = run_due_schedule(schedule, timezone.now())

        self.assertEqual(result["outcome"], "sent")
        occurrence = Campaign.objects.get(parent=template)
        test = ABTest.objects.get(campaign=occurrence)
        self.assertEqual(test.status, ABTest.STATUS_TESTING)
        self.assertEqual(test.test_type, ABTest.TYPE_SUBJECT)
        self.assertEqual(
            sorted(v.campaign.subject for v in test.variants.all()),
            ["Subject A", "Subject B"],
        )
        # The template watermark still advances — the occurrence's content went out.
        schedule.refresh_from_db()
        self.assertEqual(schedule.occurrences_sent, 1)

    def test_occurrence_without_ab_config_is_a_plain_broadcast(self):
        from email_marketing.models import ABTest

        template, schedule = self._ab_template_and_schedule(subjects=())

        result = run_due_schedule(schedule, timezone.now())

        self.assertEqual(result["outcome"], "sent")
        occurrence = Campaign.objects.get(parent=template)
        self.assertFalse(ABTest.objects.filter(campaign=occurrence).exists())

    def test_falls_back_to_a_plain_send_when_the_audience_is_too_small(self):
        from email_marketing.models import ABTest

        # One subscriber can't fill two arms → drop the test, send it anyway.
        template, schedule = self._ab_template_and_schedule(audience=1)

        result = run_due_schedule(schedule, timezone.now())

        self.assertEqual(result["outcome"], "sent")  # the newsletter still goes out
        occurrence = Campaign.objects.get(parent=template)
        self.assertFalse(ABTest.objects.filter(campaign=occurrence).exists())  # no dangling test


class ScheduleSelfArmTests(MarketingTestCase):
    def test_active_schedule_computes_next_run_on_save(self):
        campaign = Campaign.objects.create(
            site=self.site, name="T", subject="S", campaign_type=Campaign.TYPE_RECURRING
        )
        schedule = CampaignSchedule.objects.create(
            campaign=campaign, cadence="daily", send_time=time(9, 0), timezone="UTC"
        )
        self.assertIsNotNone(schedule.next_run_at)
        self.assertGreater(schedule.next_run_at, timezone.now())


class ProcessRecurringBeatTests(MarketingTestCase):
    def test_beat_spawns_occurrences_for_due_schedules(self):
        from email_marketing.tasks import process_recurring_campaigns

        template = Campaign.objects.create(
            site=self.site,
            name="Digest",
            subject="News",
            campaign_type=Campaign.TYPE_RECURRING,
            last_content_sent_at=timezone.now() - timedelta(days=7),
        )
        CampaignBlock.objects.create(
            campaign=template,
            block_type="blog_posts",
            content={"source": "since_last_send", "count": "3", "layout": "list"},
            order=0,
        )
        CampaignSchedule.objects.create(
            campaign=template,
            cadence="weekly",
            weekday=0,
            send_time=time(9, 0),
            timezone="UTC",
            next_run_at=timezone.now() - timedelta(minutes=1),
        )
        _post("Fresh", days_ago=1)

        result = process_recurring_campaigns()

        self.assertEqual(result["processed"], 1)
        self.assertEqual(Campaign.objects.filter(parent=template).count(), 1)

    def test_beat_ignores_schedules_not_yet_due(self):
        from email_marketing.tasks import process_recurring_campaigns

        template = Campaign.objects.create(
            site=self.site, name="Future", subject="S", campaign_type=Campaign.TYPE_RECURRING
        )
        CampaignSchedule.objects.create(
            campaign=template,
            cadence="daily",
            send_time=time(9, 0),
            timezone="UTC",
            next_run_at=timezone.now() + timedelta(days=1),
        )
        result = process_recurring_campaigns()
        self.assertEqual(result["processed"], 0)
