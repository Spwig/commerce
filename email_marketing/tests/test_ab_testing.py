"""A/B testing engine: deterministic bucketing, variant sends, winner decision."""

from datetime import timedelta

from django.utils import timezone

from email_marketing.models import ABTest, ABVariant, Campaign, CampaignSend, Segment
from email_marketing.services import ab_testing

from .base import MarketingTestCase

_MJML = "<mjml><mj-body><mj-section><mj-column><mj-text>Hi</mj-text></mj-column></mj-section></mj-body></mjml>"


class _ABBase(MarketingTestCase):
    def _segment_with(self, n, prefix="s"):
        seg = Segment.objects.create(
            site=self.site, name=f"aud-{prefix}", slug=f"aud-{prefix}", kind=Segment.KIND_STATIC
        )
        for i in range(n):
            seg.members.add(self.make_anon_emailable(f"{prefix}{i}@example.com"))
        return seg

    def _test(
        self, segment=None, sample_percent=50, metric=ABTest.METRIC_OPENS, window=4, auto=True
    ):
        container = Campaign.objects.create(
            site=self.site, name="Container", subject="base", segment=segment
        )
        return ABTest.objects.create(
            campaign=container,
            test_type=ABTest.TYPE_SUBJECT,
            winner_metric=metric,
            sample_percent=sample_percent,
            test_window_hours=window,
            auto_send_winner=auto,
        )

    def _variant(self, test, label, subject):
        vc = Campaign.objects.create(
            site=self.site,
            name=f"variant-{label}",
            subject=subject,
            message_type="newsletter",
            html_content=_MJML,
        )
        return ABVariant.objects.create(ab_test=test, label=label, campaign=vc)


class BucketingTests(_ABBase):
    def test_bucketing_is_deterministic(self):
        test = self._test()
        sub = self.make_anon_emailable("d@example.com")
        first = ab_testing.assign_bucket(test, sub, 2)
        again = ab_testing.assign_bucket(test, sub, 2)
        self.assertEqual(first, again)

    def test_test_group_and_holdout_are_exact_complements(self):
        seg = self._segment_with(40)
        test = self._test(segment=seg, sample_percent=50)
        in_test = holdout = 0
        for sub in seg.members.all():
            idx = ab_testing.assign_bucket(test, sub, 2)
            if idx is None:
                holdout += 1
            else:
                self.assertIn(idx, (0, 1))
                in_test += 1
        self.assertEqual(in_test + holdout, 40)
        # ~50% sampled — allow slack for hashing, but both sides must be populated.
        self.assertGreater(in_test, 0)
        self.assertGreater(holdout, 0)

    def test_sample_100_puts_everyone_in_the_test(self):
        seg = self._segment_with(20)
        test = self._test(segment=seg, sample_percent=100)
        holdout = [s for s in seg.members.all() if ab_testing.assign_bucket(test, s, 2) is None]
        self.assertEqual(holdout, [])


class StartTests(_ABBase):
    def test_start_sends_each_variant_to_its_bucket(self):
        seg = self._segment_with(30)
        test = self._test(segment=seg, sample_percent=100)  # no holdout, whole audience split
        self._variant(test, "A", "Subject A")
        self._variant(test, "B", "Subject B")

        result = ab_testing.start_ab_test(test)
        self.assertNotIn("error", result)
        test.refresh_from_db()
        self.assertEqual(test.status, ABTest.STATUS_TESTING)
        self.assertIsNotNone(test.decide_at)

        total_sends = 0
        for variant in test.variants.all():
            sends = CampaignSend.objects.filter(campaign=variant.campaign)
            self.assertTrue(sends.exists())
            self.assertTrue(all(cs.variant == variant.label for cs in sends))
            total_sends += sends.count()
        self.assertEqual(total_sends, 30)  # everyone got exactly one variant

    def test_refuses_when_the_audience_is_too_small(self):
        seg = self._segment_with(2)
        test = self._test(segment=seg, sample_percent=20)  # 20% of 2 ≈ 0 in test
        self._variant(test, "A", "A")
        self._variant(test, "B", "B")
        self.assertEqual(ab_testing.start_ab_test(test).get("error"), "audience_too_small")

    def test_refuses_with_fewer_than_two_variants(self):
        seg = self._segment_with(20)
        test = self._test(segment=seg)
        self._variant(test, "A", "A")
        self.assertEqual(ab_testing.start_ab_test(test).get("error"), "need_two_variants")

    def test_start_rolls_back_if_a_variant_send_fails(self):
        seg = self._segment_with(30)
        test = self._test(segment=seg, sample_percent=100)
        va = self._variant(test, "A", "A")
        vb = self._variant(test, "B", "B")
        # Variant B is unsendable (already SENT) → send_campaign refuses.
        Campaign.objects.filter(pk=vb.campaign_id).update(status=Campaign.STATUS_SENT)

        result = ab_testing.start_ab_test(test)
        self.assertIn("error", result)
        test.refresh_from_db()
        self.assertEqual(test.status, ABTest.STATUS_DRAFT)  # never entered testing
        # Variant A's sends were rolled back with the whole start (atomic).
        self.assertFalse(CampaignSend.objects.filter(campaign=va.campaign).exists())


class DecideTests(_ABBase):
    def _started(self, sample_percent=50, metric=ABTest.METRIC_OPENS):
        seg = self._segment_with(40)
        test = self._test(segment=seg, sample_percent=sample_percent, metric=metric)
        va = self._variant(test, "A", "Subject A")
        vb = self._variant(test, "B", "Subject B")
        ab_testing.start_ab_test(test)
        return test, va, vb

    def test_higher_open_rate_variant_wins_and_holdout_gets_it(self):
        test, va, vb = self._started(sample_percent=50)
        # Everyone who got variant B opens; nobody on A does.
        CampaignSend.objects.filter(campaign=vb.campaign).update(opened=True)

        before = Campaign.objects.count()
        result = ab_testing.decide_ab_test(test)

        self.assertEqual(result["winner"], "B")
        self.assertTrue(result["winner_send"])
        test.refresh_from_db()
        self.assertEqual(test.status, ABTest.STATUS_COMPLETE)
        self.assertEqual(test.winner_id, vb.id)
        vb.refresh_from_db()
        self.assertGreater(vb.opened, 0)
        # A fresh winner-send campaign was spawned to the holdout.
        self.assertEqual(Campaign.objects.count(), before + 1)
        winner_send = Campaign.objects.filter(parent=test.campaign).order_by("-created_at").first()
        self.assertTrue(CampaignSend.objects.filter(campaign=winner_send).exists())

    def test_winner_send_failure_completes_but_reports_false(self):
        from email_system.models import EmailAccount

        test, va, vb = self._started(sample_percent=50)
        CampaignSend.objects.filter(campaign=vb.campaign).update(opened=True)
        # No sending account available at decision time → the winner can't enqueue.
        EmailAccount.objects.filter(site=self.site).update(is_active=False, is_default=False)

        result = ab_testing.decide_ab_test(test)
        self.assertEqual(result["winner"], "B")
        self.assertFalse(result["winner_send"])  # holdout not queued
        test.refresh_from_db()
        self.assertEqual(test.status, ABTest.STATUS_COMPLETE)  # still completes

    def test_sample_100_completes_without_a_winner_send(self):
        test, va, vb = self._started(sample_percent=100)
        CampaignSend.objects.filter(campaign=vb.campaign).update(opened=True)
        before = Campaign.objects.count()
        result = ab_testing.decide_ab_test(test)
        self.assertFalse(result["winner_send"])
        self.assertEqual(Campaign.objects.count(), before)  # no holdout → no new campaign

    def test_tie_breaks_to_the_earlier_label(self):
        test, va, vb = self._started(sample_percent=100)
        # The winner key is (rate, recipients, -label). Deterministic bucketing
        # splits the audience unevenly, so equalise reach first — otherwise a 0-0
        # rate tie would be decided by recipient count (bucketing luck), not label.
        a_sends = list(
            CampaignSend.objects.filter(campaign=va.campaign).values_list("pk", flat=True)
        )
        b_sends = list(
            CampaignSend.objects.filter(campaign=vb.campaign).values_list("pk", flat=True)
        )
        n = min(len(a_sends), len(b_sends))
        CampaignSend.objects.filter(pk__in=a_sends[n:] + b_sends[n:]).delete()
        # No engagement anywhere → a genuine 0-0 tie with equal reach → A wins by label.
        result = ab_testing.decide_ab_test(test)
        self.assertEqual(result["winner"], "A")

    def _sent(self, variant_campaign, count, opened):
        for i in range(count):
            CampaignSend.objects.create(
                campaign=variant_campaign,
                subscriber=self.make_anon_emailable(f"{variant_campaign.id}-{i}@ex.com"),
                status=CampaignSend.STATUS_SENT,
                opened=opened,
            )

    def test_decide_stores_confidence_for_a_reliable_clear_winner(self):
        test = self._test(sample_percent=100)
        va = self._variant(test, "A", "A subj")
        vb = self._variant(test, "B", "B subj")
        test.status = ABTest.STATUS_TESTING
        test.save(update_fields=["status"])
        # Reliable and unambiguous: 30 each, everyone on B opens, nobody on A.
        self._sent(va.campaign, 30, opened=False)
        self._sent(vb.campaign, 30, opened=True)

        result = ab_testing.decide_ab_test(test)

        self.assertEqual(result["winner"], "B")
        self.assertTrue(result["reliable"])
        test.refresh_from_db()
        self.assertIsNotNone(test.winner_confidence)
        self.assertGreaterEqual(test.winner_confidence, ABTest.SIGNIFICANCE_THRESHOLD)

    def test_decide_leaves_confidence_null_when_the_sample_is_too_small(self):
        test = self._test(sample_percent=100)
        va = self._variant(test, "A", "A subj")
        vb = self._variant(test, "B", "B subj")
        test.status = ABTest.STATUS_TESTING
        test.save(update_fields=["status"])
        # B has the best rate (1/1) but a single opener is noise, not a signal.
        self._sent(vb.campaign, 1, opened=True)
        self._sent(va.campaign, 5, opened=False)

        result = ab_testing.decide_ab_test(test)

        self.assertEqual(result["winner"], "B")  # best rate still wins the pick...
        self.assertFalse(result["reliable"])
        test.refresh_from_db()
        self.assertIsNone(test.winner_confidence)  # ...but no confidence is stored for it

    def test_assess_flags_a_reliable_near_tie_as_inconclusive(self):
        # 55/100 vs 45/100 is plenty of data, but the gap is too small to call.
        from email_marketing.services.ab_stats import assess

        test = self._test(sample_percent=100)
        va = self._variant(test, "A", "A subj")
        vb = self._variant(test, "B", "B subj")
        va.recipients, va.opened = 100, 45
        vb.recipients, vb.opened = 100, 55

        result = assess(vb, [va, vb], ABTest.METRIC_OPENS)
        self.assertTrue(result["reliable"])  # enough data...
        self.assertGreater(result["confidence"], 0.0)
        self.assertLess(
            result["confidence"], ABTest.SIGNIFICANCE_THRESHOLD
        )  # ...but not a clear win


class BeatTests(_ABBase):
    def test_beat_decides_a_due_test(self):
        from email_marketing.tasks import process_due_ab_tests

        seg = self._segment_with(30)
        test = self._test(segment=seg, sample_percent=100)
        vb = self._variant(test, "B", "B")
        self._variant(test, "A", "A")
        ab_testing.start_ab_test(test)
        # Force the window to have elapsed.
        ABTest.objects.filter(pk=test.pk).update(decide_at=timezone.now() - timedelta(hours=1))

        out = process_due_ab_tests()
        self.assertEqual(out["decided"], 1)
        test.refresh_from_db()
        self.assertEqual(test.status, ABTest.STATUS_COMPLETE)
