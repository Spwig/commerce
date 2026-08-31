"""Deeper analytics: per-campaign time-series, link-level clicks, per-recipient drill-down.

Builds on the CampaignSend / EmailOutbox / EmailEvent scaffolding used by test_reporting.
"""

import uuid
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils import timezone

from email_marketing.models import Campaign, CampaignSend
from email_marketing.services import reporting
from email_system.models import EmailEvent, EmailOutbox

from .base import MarketingTestCase

User = get_user_model()


class _Base(MarketingTestCase):
    def _campaign(self, **kw):
        kw.setdefault("site", self.site)
        kw.setdefault("name", "C")
        kw.setdefault("subject", "s")
        return Campaign.objects.create(**kw)

    def _send(
        self,
        campaign,
        *,
        created_days_ago=0,
        opened_days_ago=None,
        clicked_days_ago=None,
        email=None,
    ):
        email = email or f"u{uuid.uuid4().hex[:8]}@example.com"
        sub = self.make_anon_emailable(email)
        cs = CampaignSend.objects.create(
            campaign=campaign,
            subscriber=sub,
            status=CampaignSend.STATUS_SENT,
            opened=opened_days_ago is not None,
            clicked=clicked_days_ago is not None,
        )
        now = timezone.now()
        fields = {"created_at": now - timedelta(days=created_days_ago)}
        if opened_days_ago is not None:
            fields["opened_at"] = now - timedelta(days=opened_days_ago)
        if clicked_days_ago is not None:
            fields["clicked_at"] = now - timedelta(days=clicked_days_ago)
        CampaignSend.objects.filter(pk=cs.pk).update(**fields)
        return cs

    def _sent_with_outbox(self, campaign, email=None, sub=None):
        email = email or f"u{uuid.uuid4().hex[:8]}@example.com"
        sub = sub or self.make_anon_emailable(email)
        outbox = EmailOutbox.objects.create(
            site=self.site,
            account=self.account,
            from_email="store@example.com",
            to_email=email,
            subject="s",
            html_body="<p>h</p>",
            template_type="newsletter",
            status="sent",
        )
        cs = CampaignSend.objects.create(
            campaign=campaign, subscriber=sub, outbox=outbox, status=CampaignSend.STATUS_SENT
        )
        return cs, outbox

    def _click(self, outbox, url):
        EmailEvent.objects.create(email=outbox, event_type="clicked", event_data={"url": url})

    def _marketing_staff(self):
        from staff_roles.models import StaffRole
        from staff_roles.services import invalidate_user_cache

        user = User.objects.create_user(
            username=f"mkt-{uuid.uuid4().hex[:8]}",
            email="mkt@test.spwig.com",
            password="pw",
            is_staff=True,
        )
        group = Group.objects.create(name=f"marketing-{uuid.uuid4().hex[:8]}")
        user.groups.add(group)
        StaffRole.objects.create(
            group=group,
            display_name=group.name,
            can_access_admin=True,
            permission_categories={"marketing": "full"},
        )
        invalidate_user_cache(user)
        return user


class CampaignTimeseriesTests(_Base):
    def test_buckets_sends_opens_clicks_by_day(self):
        c = self._campaign()
        # A: sent 2d ago, opened 2d ago, clicked 1d ago. B: sent today.
        self._send(c, created_days_ago=2, opened_days_ago=2, clicked_days_ago=1)
        self._send(c, created_days_ago=0)
        ts = reporting.campaign_timeseries(c, days=30)
        self.assertEqual(len(ts["labels"]), 3)  # 2 days ago … today, inclusive
        self.assertEqual(ts["sends"], [1, 0, 1])
        self.assertEqual(ts["opens"], [1, 0, 0])
        self.assertEqual(ts["clicks"], [0, 1, 0])

    def test_empty_campaign_returns_empty_series(self):
        ts = reporting.campaign_timeseries(self._campaign())
        self.assertEqual(ts, {"labels": [], "sends": [], "opens": [], "clicks": []})

    def test_only_opened_rows_count_toward_opens(self):
        c = self._campaign()
        self._send(c, created_days_ago=0)  # sent, never opened
        ts = reporting.campaign_timeseries(c)
        self.assertEqual(sum(ts["sends"]), 1)
        self.assertEqual(sum(ts["opens"]), 0)
        self.assertEqual(sum(ts["clicks"]), 0)

    def test_ab_parent_rolls_up_variant_children(self):
        parent = self._campaign(name="P")
        variant = self._campaign(name="A", parent=parent)
        self._send(variant, created_days_ago=0, opened_days_ago=0)
        ts = reporting.campaign_timeseries(parent, days=30)
        self.assertEqual(sum(ts["sends"]), 1)
        self.assertEqual(sum(ts["opens"]), 1)

    def test_non_sent_rows_are_excluded_from_the_sent_series(self):
        # CampaignSend rows exist before delivery; only STATUS_SENT counts as "sent"
        # (matches campaign_report's `sent`).
        c = self._campaign()
        self._send(c, created_days_ago=0)  # STATUS_SENT
        skipped_sub = self.make_anon_emailable("skip@example.com")
        CampaignSend.objects.create(
            campaign=c,
            subscriber=skipped_sub,
            status=CampaignSend.STATUS_SKIPPED,
            skip_reason="suppressed",
        )
        ts = reporting.campaign_timeseries(c)
        self.assertEqual(sum(ts["sends"]), 1)  # skipped row not counted as sent

    def test_opened_but_bounced_row_is_excluded_from_opens(self):
        # Consistent with campaign_report: an open on a send that later bounced is not
        # delivered, so it must not inflate the opens series.
        c = self._campaign()
        sub = self.make_anon_emailable("ob@example.com")
        cs = CampaignSend.objects.create(
            campaign=c,
            subscriber=sub,
            status=CampaignSend.STATUS_SENT,
            opened=True,
            bounced=True,
            bounce_type="soft",
        )
        CampaignSend.objects.filter(pk=cs.pk).update(opened_at=timezone.now())
        ts = reporting.campaign_timeseries(c)
        self.assertEqual(sum(ts["opens"]), 0)

    def test_window_is_capped_to_days(self):
        c = self._campaign()
        # A send 100 days ago must not stretch the window past the `days` cap.
        self._send(c, created_days_ago=100)
        self._send(c, created_days_ago=0)
        ts = reporting.campaign_timeseries(c, days=30)
        self.assertEqual(len(ts["labels"]), 30)
        self.assertEqual(sum(ts["sends"]), 1)  # only the in-window (today) send shows


class CampaignLinkClicksTests(_Base):
    def test_aggregates_clicks_and_unique_clickers(self):
        c = self._campaign()
        _, ob1 = self._sent_with_outbox(c)
        _, ob2 = self._sent_with_outbox(c)
        # subscriber 1 clicks A twice; subscriber 2 clicks A once + B once
        self._click(ob1, "https://shop.test/a")
        self._click(ob1, "https://shop.test/a")
        self._click(ob2, "https://shop.test/a")
        self._click(ob2, "https://shop.test/b")
        rows = reporting.campaign_link_clicks(c)
        by_url = {r["url"]: r for r in rows}
        self.assertEqual(by_url["https://shop.test/a"]["clicks"], 3)
        self.assertEqual(by_url["https://shop.test/a"]["unique_clickers"], 2)
        self.assertEqual(by_url["https://shop.test/b"]["clicks"], 1)
        self.assertEqual(rows[0]["url"], "https://shop.test/a")  # ordered by clicks desc

    def test_ctr_is_over_delivered(self):
        c = self._campaign()
        _, ob1 = self._sent_with_outbox(c)  # delivered
        self._sent_with_outbox(c)  # delivered, no click
        self._click(ob1, "https://shop.test/a")
        rows = reporting.campaign_link_clicks(c)
        self.assertEqual(rows[0]["ctr"], 50.0)  # 1 unique clicker / 2 delivered

    def test_skips_empty_or_missing_url(self):
        c = self._campaign()
        _, ob = self._sent_with_outbox(c)
        self._click(ob, "")  # empty url
        EmailEvent.objects.create(email=ob, event_type="clicked", event_data={})  # no url key
        self.assertEqual(reporting.campaign_link_clicks(c), [])

    def test_respects_limit(self):
        c = self._campaign()
        _, ob = self._sent_with_outbox(c)
        for i in range(5):
            self._click(ob, f"https://shop.test/{i}")
        self.assertEqual(len(reporting.campaign_link_clicks(c, limit=3)), 3)

    def test_only_this_campaigns_clicks(self):
        c = self._campaign()
        other = self._campaign(name="other")
        _, ob_c = self._sent_with_outbox(c)
        _, ob_o = self._sent_with_outbox(other)
        self._click(ob_c, "https://shop.test/mine")
        self._click(ob_o, "https://shop.test/theirs")
        rows = reporting.campaign_link_clicks(c)
        self.assertEqual({r["url"] for r in rows}, {"https://shop.test/mine"})

    def test_ab_parent_rolls_up_children_link_clicks(self):
        parent = self._campaign(name="P")
        variant = self._campaign(name="A", parent=parent)
        _, ob = self._sent_with_outbox(variant)
        self._click(ob, "https://shop.test/x")
        rows = reporting.campaign_link_clicks(parent)
        self.assertEqual(rows[0]["url"], "https://shop.test/x")

    def test_click_on_a_bounced_send_is_excluded(self):
        # A click on a send that later bounced must not appear (matches the report's
        # delivered-only click population; keeps CTR ≤ 100%).
        c = self._campaign()
        _, ob = self._sent_with_outbox(c)
        CampaignSend.objects.filter(outbox=ob).update(bounced=True, bounce_type="soft")
        self._click(ob, "https://shop.test/bounced")
        self.assertEqual(reporting.campaign_link_clicks(c), [])

    def test_unique_clickers_counts_distinct_sends_across_occurrences(self):
        # A recurring rollup where the SAME subscriber clicks the same URL across two
        # occurrences counts as two (per-send basis, matching the delivered denominator)
        # — not collapsed to one subscriber.
        parent = self._campaign(name="P")
        occ1 = self._campaign(name="occ1", parent=parent)
        occ2 = self._campaign(name="occ2", parent=parent)
        sub = self.make_anon_emailable("repeat@example.com")
        _, ob1 = self._sent_with_outbox(occ1, sub=sub)
        _, ob2 = self._sent_with_outbox(occ2, sub=sub)
        self._click(ob1, "https://shop.test/x")
        self._click(ob2, "https://shop.test/x")
        rows = reporting.campaign_link_clicks(parent)
        self.assertEqual(rows[0]["clicks"], 2)
        self.assertEqual(rows[0]["unique_clickers"], 2)  # two distinct sends, not one sub

    def test_report_page_shows_top_links(self):
        c = self._campaign()
        _, ob = self._sent_with_outbox(c)
        self._click(ob, "https://shop.test/deal")
        self.client.force_login(self._marketing_staff())
        resp = self.client.get(reverse("email_marketing_admin:campaign_report", args=[c.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Top links")
        self.assertContains(resp, "https://shop.test/deal")


class RecipientDrilldownTests(_Base):
    AJAX = {"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"}

    def _filter_url(self):
        return reverse("email_marketing_admin:filter_campaign_sends")

    def test_filter_lists_and_filters_by_engagement(self):
        c = self._campaign()
        opened, _ = self._sent_with_outbox(c, email="opened@example.com")
        CampaignSend.objects.filter(pk=opened.pk).update(opened=True)
        self._sent_with_outbox(c, email="plain@example.com")  # delivered, not opened
        self.client.force_login(self._marketing_staff())
        resp = self.client.get(self._filter_url(), {"campaign": str(c.id)}, **self.AJAX)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["count"], 2)
        resp = self.client.get(
            self._filter_url(), {"campaign": str(c.id), "engagement": "opened"}, **self.AJAX
        )
        data = resp.json()
        self.assertEqual(data["count"], 1)
        self.assertIn("opened@example.com", data["html"])
        self.assertNotIn("plain@example.com", data["html"])

    def test_filter_search_by_email(self):
        c = self._campaign()
        self._sent_with_outbox(c, email="alice@example.com")
        self._sent_with_outbox(c, email="bob@example.com")
        self.client.force_login(self._marketing_staff())
        resp = self.client.get(
            self._filter_url(), {"campaign": str(c.id), "search": "alice"}, **self.AJAX
        )
        self.assertEqual(resp.json()["count"], 1)

    def test_filter_requires_ajax(self):
        c = self._campaign()
        self.client.force_login(self._marketing_staff())
        resp = self.client.get(self._filter_url(), {"campaign": str(c.id)})  # no AJAX header
        self.assertEqual(resp.status_code, 400)

    def test_filter_is_scoped_to_campaign(self):
        c = self._campaign()
        other = self._campaign(name="other")
        self._sent_with_outbox(c, email="mine@example.com")
        self._sent_with_outbox(other, email="theirs@example.com")
        self.client.force_login(self._marketing_staff())
        resp = self.client.get(self._filter_url(), {"campaign": str(c.id)}, **self.AJAX)
        data = resp.json()
        self.assertEqual(data["count"], 1)
        self.assertIn("mine@example.com", data["html"])
        self.assertNotIn("theirs@example.com", data["html"])

    def test_filter_bad_campaign_id_is_404(self):
        self.client.force_login(self._marketing_staff())
        resp = self.client.get(self._filter_url(), {"campaign": "not-a-uuid"}, **self.AJAX)
        self.assertEqual(resp.status_code, 404)

    def test_recipients_page_renders_and_is_gated(self):
        c = self._campaign()
        url = reverse("email_marketing_admin:campaign_recipients", args=[c.id])
        self.client.force_login(self._marketing_staff())
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Recipients")
        self.assertContains(resp, "filter/campaign-sends")  # filter config wired in
        plain = User.objects.create_user(
            username=f"p-{uuid.uuid4().hex[:6]}",
            email="p@test.spwig.com",
            password="pw",
            is_staff=True,
        )
        self.client.force_login(plain)
        self.assertIn(self.client.get(url).status_code, (302, 403))

    def test_recipient_activity_returns_ordered_events(self):
        c = self._campaign()
        cs, ob = self._sent_with_outbox(c)
        EmailEvent.objects.create(
            email=ob,
            event_type="clicked",
            event_data={"url": "https://shop.test/a"},
            occurred_at=timezone.now(),
        )
        EmailEvent.objects.create(
            email=ob, event_type="opened", occurred_at=timezone.now() - timedelta(hours=1)
        )
        self.client.force_login(self._marketing_staff())
        url = reverse("email_marketing_admin:campaign_recipient_activity", args=[c.id, cs.id])
        resp = self.client.get(url, **self.AJAX)
        self.assertEqual(resp.status_code, 200)
        html = resp.json()["html"]
        self.assertIn("https://shop.test/a", html)
        self.assertLess(html.index("Opened"), html.index("Clicked"))  # earliest first

    def test_recipient_activity_refuses_a_send_from_another_campaign(self):
        c = self._campaign()
        other = self._campaign(name="other")
        cs_other, _ = self._sent_with_outbox(other)
        self.client.force_login(self._marketing_staff())
        url = reverse("email_marketing_admin:campaign_recipient_activity", args=[c.id, cs_other.id])
        self.assertEqual(self.client.get(url, **self.AJAX).status_code, 404)
