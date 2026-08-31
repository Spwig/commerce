"""Starter audiences — one-click seeding of segments from the store's app data.

``seed_starter_segments`` creates ready-made dynamic segments from the customer,
loyalty and affiliate intelligence the platform already computes — but only the
ones the store has data for, idempotently, and never resurrecting a starter the
merchant removed.
"""

from django.contrib.auth import get_user_model
from django.urls import reverse
from djmoney.money import Money

from affiliate.models import Affiliate
from customers.models import CustomerMetrics, CustomerSegment
from email_marketing.models import Segment
from email_marketing.services.segmentation import resolve_segment
from email_marketing.services.starter_segments import available_starters, seed_starter_segments
from loyalty.models import LoyaltyMember, LoyaltyTier
from tests.factories import UserFactory

from .base import MarketingTestCase


class StarterSegmentTests(MarketingTestCase):
    def _vip_bucket(self):
        return CustomerSegment.objects.create(
            name="vip",
            display_name="VIP Customer",
            description="Top spenders",
            min_total_spent=Money(5000, "USD"),
            min_orders=10,
            max_days_since_last_purchase=90,
        )

    def _metrics_subscriber(self, email, **fields):
        user = UserFactory()
        defaults = {}
        for key in ("total_spent", "lifetime_value", "average_order_value"):
            if key in fields:
                defaults[key] = Money(fields.pop(key), "USD")
        defaults.update(fields)
        CustomerMetrics.objects.update_or_create(user=user, defaults=defaults)
        return self.make_subscriber(email, user=user)

    def _slugs(self):
        return {s["slug"] for s in available_starters()}

    def test_seed_creates_starters_for_available_sources(self):
        self._vip_bucket()
        LoyaltyTier.objects.create(name="Gold", slug="gold", rank=1)
        self._metrics_subscriber(
            "c@e.com", total_spent=6000, completed_orders=12, days_since_last_purchase=5
        )
        Affiliate.objects.create(user=UserFactory(), affiliate_code="AFF1", status="active")

        result = seed_starter_segments(self.site)

        slugs = set(Segment.objects.filter(site=self.site).values_list("slug", flat=True))
        for expected in ("vip-customers", "lapsing-customers", "loyalty-members", "affiliates"):
            self.assertIn(expected, slugs)
        self.assertIn("top-tier-loyalty", slugs)  # a tier exists
        # Everything seeded as a live dynamic segment the merchant now owns.
        for seg in Segment.objects.filter(site=self.site):
            self.assertEqual(seg.kind, Segment.KIND_DYNAMIC)
            self.assertTrue(seg.is_active)
        self.assertTrue(result["created"])

    def test_seed_is_idempotent(self):
        self._vip_bucket()
        first = seed_starter_segments(self.site)
        self.assertTrue(first["created"])
        before = Segment.objects.filter(site=self.site).count()

        second = seed_starter_segments(self.site)
        self.assertEqual(second["created"], [])
        self.assertEqual(Segment.objects.filter(site=self.site).count(), before)

    def test_starters_skip_absent_sources(self):
        # Customer metrics present, but no buckets / loyalty members / affiliates.
        self._metrics_subscriber("c@e.com", days_since_last_purchase=200)
        LoyaltyMember.objects.all().delete()  # drop the auto-enrolled member
        self.assertEqual(self._slugs(), {"lapsing-customers"})

    def test_bucket_starter_references_only_present_buckets(self):
        self._vip_bucket()  # only "vip" exists, not "high_value"
        starters = {s["slug"]: s for s in available_starters()}
        self.assertIn("high-value-customers", starters)
        value = starters["high-value-customers"]["rules"]["conditions"][0]["value"]
        self.assertEqual(value, ["vip"])

    def test_seeded_vip_starter_resolves_to_qualifying_customers(self):
        self._vip_bucket()
        good = self._metrics_subscriber(
            "vip@e.com", total_spent=6000, completed_orders=12, days_since_last_purchase=5
        )
        self._metrics_subscriber(
            "reg@e.com", total_spent=100, completed_orders=1, days_since_last_purchase=5
        )
        seed_starter_segments(self.site)

        seg = Segment.objects.get(site=self.site, slug="vip-customers")
        ids = set(resolve_segment(seg).values_list("id", flat=True))
        self.assertEqual(ids, {good.id})

    def test_seed_does_not_resurrect_a_removed_starter(self):
        self._vip_bucket()
        seed_starter_segments(self.site)
        Segment.objects.get(site=self.site, slug="vip-customers").delete()  # soft delete

        result = seed_starter_segments(self.site)
        self.assertNotIn("VIP customers", result["created"])
        self.assertFalse(Segment.objects.filter(site=self.site, slug="vip-customers").exists())

    def test_concurrent_double_submit_is_absorbed_not_500(self):
        # A lost double-submit race (unique-constraint IntegrityError on create)
        # is reported as skipped and the loop continues — never a 500.
        from unittest.mock import patch

        from django.db import IntegrityError

        self._vip_bucket()  # yields vip-customers + high-value-customers
        real_create = Segment.objects.create
        state = {"first": True}

        def flaky_create(*args, **kwargs):
            if state["first"]:
                state["first"] = False
                raise IntegrityError("duplicate key value violates unique constraint")
            return real_create(*args, **kwargs)

        with patch.object(Segment.objects, "create", side_effect=flaky_create):
            result = seed_starter_segments(self.site)

        # The raced starter is skipped; the other is still created.
        self.assertEqual(len(result["skipped"]), 1)
        self.assertEqual(len(result["created"]), 1)

    def test_pending_only_affiliates_are_not_offered(self):
        # Affiliates default to "pending"; the Affiliates starter targets active
        # partners, so a pending-only store shouldn't be offered it.
        Affiliate.objects.create(user=UserFactory(), affiliate_code="AFF-pending", status="pending")
        self.assertNotIn("affiliates", self._slugs())


class StarterSeedViewTests(MarketingTestCase):
    """The changelist 'Add starter audiences' button posts to this endpoint."""

    def _admin(self, username):
        return get_user_model().objects.create_superuser(username, f"{username}@e.com", "pw")

    def test_post_seeds_and_redirects(self):
        CustomerSegment.objects.create(
            name="vip",
            display_name="VIP",
            description="",
            min_total_spent=Money(5000, "USD"),
            min_orders=10,
        )
        self.client.force_login(self._admin("seed_admin"))
        resp = self.client.post(reverse("email_marketing_admin:seed_starter_segments"))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Segment.objects.filter(site=self.site, slug="vip-customers").exists())

    def test_get_is_rejected(self):
        # Seeding mutates state, so only POST is allowed.
        self.client.force_login(self._admin("seed_admin2"))
        resp = self.client.get(reverse("email_marketing_admin:seed_starter_segments"))
        self.assertEqual(resp.status_code, 405)

    def test_anonymous_is_redirected_to_login(self):
        resp = self.client.post(reverse("email_marketing_admin:seed_starter_segments"))
        self.assertEqual(resp.status_code, 302)
        self.assertNotIn("/admin/email_marketing/segments/", resp["Location"])
