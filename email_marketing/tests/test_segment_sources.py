"""Segment rules sourced from loyalty, affiliate and shop RFM intelligence.

These cover the audience fields that reach *through* ``Subscriber.user`` into the
neighbouring apps — customer metrics (recency / lifetime value), the loyalty
programme (tier / points / membership), the affiliate roster, and the shop's own
named value buckets (``customers.CustomerSegment``). Each resolves as one ORM
query alongside the subscriber's own fields; anonymous leads (no ``user``) never
match a customer/loyalty/affiliate rule.
"""

from djmoney.money import Money

from affiliate.models import Affiliate
from customers.models import CustomerMetrics, CustomerSegment
from email_marketing.models import Segment
from email_marketing.services.segmentation import available_rule_fields, resolve_segment
from loyalty.models import LoyaltyBalance, LoyaltyMember, LoyaltyTier
from tests.factories import UserFactory

from .base import MarketingTestCase


class SegmentSourceTests(MarketingTestCase):
    # --- builders ------------------------------------------------------------

    def _make_segment(self, rules, slug="seg"):
        return Segment.objects.create(
            site=self.site, name=slug, slug=slug, kind=Segment.KIND_DYNAMIC, rules=rules
        )

    def _resolve_ids(self, rules):
        return set(resolve_segment(self._make_segment(rules)).values_list("id", flat=True))

    def _metrics_subscriber(self, email, **metric_fields):
        """Registered subscriber with a CustomerMetrics cache row."""
        user = UserFactory()
        defaults = {}
        for key in ("total_spent", "lifetime_value", "average_order_value"):
            if key in metric_fields:
                defaults[key] = Money(metric_fields.pop(key), "USD")
        defaults.update(metric_fields)  # completed_orders, days_since_last_purchase, …
        CustomerMetrics.objects.update_or_create(user=user, defaults=defaults)
        return self.make_subscriber(email, user=user)

    def _tier(self, slug, rank, name=None):
        return LoyaltyTier.objects.create(slug=slug, rank=rank, name=name or slug.title())

    def _loyalty_subscriber(self, email, tier=None, points=None, is_active=True):
        user = UserFactory()
        # Creating a User auto-enrols a LoyaltyMember (loyalty signup signal), so
        # adjust the existing member rather than creating a duplicate.
        member, _ = LoyaltyMember.objects.get_or_create(customer=user)
        member.current_tier = tier
        member.is_active = is_active
        member.save(update_fields=["current_tier", "is_active"])
        if points is not None:
            LoyaltyBalance.objects.update_or_create(
                member=member, defaults={"available_points": points}
            )
        return self.make_subscriber(email, user=user)

    def _affiliate_subscriber(self, email, status="active"):
        user = UserFactory()
        Affiliate.objects.create(
            user=user, affiliate_code=f"AFF-{email.split('@')[0]}", status=status
        )
        return self.make_subscriber(email, user=user)

    # --- shop / RFM primitives ----------------------------------------------

    def test_days_since_last_purchase_targets_lapsed_customers(self):
        lapsed = self._metrics_subscriber("lapsed@e.com", days_since_last_purchase=120)
        self._metrics_subscriber("recent@e.com", days_since_last_purchase=10)
        self.make_anon_emailable("anon@e.com")  # no metrics → excluded

        ids = self._resolve_ids(
            {"conditions": [{"field": "days_since_last_purchase", "op": "gte", "value": 90}]}
        )
        self.assertEqual(ids, {lapsed.id})

    def test_lifetime_value_rule_filters_high_value_customers(self):
        vip = self._metrics_subscriber("vip@e.com", lifetime_value=2500)
        self._metrics_subscriber("modest@e.com", lifetime_value=100)

        ids = self._resolve_ids(
            {"conditions": [{"field": "lifetime_value", "op": "gte", "value": 1000}]}
        )
        self.assertEqual(ids, {vip.id})

    def test_average_order_value_rule(self):
        big = self._metrics_subscriber("big@e.com", average_order_value=300)
        self._metrics_subscriber("small@e.com", average_order_value=20)

        ids = self._resolve_ids(
            {"conditions": [{"field": "average_order_value", "op": "gte", "value": 200}]}
        )
        self.assertEqual(ids, {big.id})

    # --- loyalty -------------------------------------------------------------

    def test_loyalty_tier_in_targets_named_tiers(self):
        gold = self._tier("gold", rank=1)
        silver = self._tier("silver", rank=2)
        bronze = self._tier("bronze", rank=3)
        g = self._loyalty_subscriber("g@e.com", tier=gold)
        s = self._loyalty_subscriber("s@e.com", tier=silver)
        self._loyalty_subscriber("b@e.com", tier=bronze)
        self.make_anon_emailable("anon@e.com")  # not a member → excluded

        ids = self._resolve_ids(
            {"conditions": [{"field": "loyalty_tier", "op": "in", "value": ["gold", "silver"]}]}
        )
        self.assertEqual(ids, {g.id, s.id})

    def test_loyalty_points_threshold(self):
        rich = self._loyalty_subscriber("rich@e.com", points=1500)
        self._loyalty_subscriber("poor@e.com", points=50)

        ids = self._resolve_ids(
            {"conditions": [{"field": "loyalty_points", "op": "gte", "value": 1000}]}
        )
        self.assertEqual(ids, {rich.id})

    def test_is_loyalty_member_excludes_non_and_inactive_members(self):
        active = self._loyalty_subscriber("active@e.com", is_active=True)
        self._loyalty_subscriber("lapsed@e.com", is_active=False)
        self.make_anon_emailable("anon@e.com")

        ids = self._resolve_ids({"conditions": [{"field": "is_loyalty_member", "op": "is_true"}]})
        self.assertEqual(ids, {active.id})

    # --- affiliate -----------------------------------------------------------

    def test_is_affiliate_targets_active_affiliates_only(self):
        active = self._affiliate_subscriber("aff@e.com", status="active")
        self._affiliate_subscriber("susp@e.com", status="suspended")
        self.make_anon_emailable("anon@e.com")

        ids = self._resolve_ids({"conditions": [{"field": "is_affiliate", "op": "is_true"}]})
        self.assertEqual(ids, {active.id})

    # --- named CustomerSegment buckets --------------------------------------

    def _vip_bucket(self):
        return CustomerSegment.objects.create(
            name="vip",
            display_name="VIP Customer",
            description="Top spenders",
            min_total_spent=Money(5000, "USD"),
            min_orders=10,
            max_days_since_last_purchase=90,
        )

    def test_customer_segment_bucket_compiles_to_membership(self):
        self._vip_bucket()
        qualifies = self._metrics_subscriber(
            "vip@e.com", total_spent=6000, completed_orders=12, days_since_last_purchase=10
        )
        # Fails on spend and orders.
        self._metrics_subscriber(
            "regular@e.com", total_spent=200, completed_orders=2, days_since_last_purchase=10
        )
        # Right spend/orders but lapsed past the bucket's recency ceiling.
        self._metrics_subscriber(
            "stale@e.com", total_spent=9000, completed_orders=20, days_since_last_purchase=200
        )

        ids = self._resolve_ids(
            {"conditions": [{"field": "customer_segment", "op": "in", "value": ["vip"]}]}
        )
        self.assertEqual(ids, {qualifies.id})

    def test_unknown_bucket_name_matches_nobody_not_everybody(self):
        # A stale/unknown bucket must fail CLOSED — never fall back to the whole
        # active base and blast every subscriber.
        self._metrics_subscriber("a@e.com", total_spent=100)
        ids = self._resolve_ids(
            {"conditions": [{"field": "customer_segment", "op": "in", "value": ["does_not_exist"]}]}
        )
        self.assertEqual(ids, set())

    def test_deactivated_bucket_matches_nobody(self):
        # Deleting/deactivating a bucket a live segment points at must not turn
        # that segment into "everyone".
        bucket = self._vip_bucket()
        bucket.is_active = False
        bucket.save(update_fields=["is_active"])
        self._metrics_subscriber(
            "vip@e.com", total_spent=9000, completed_orders=20, days_since_last_purchase=5
        )
        ids = self._resolve_ids(
            {"conditions": [{"field": "customer_segment", "op": "in", "value": ["vip"]}]}
        )
        self.assertEqual(ids, set())

    def test_criteria_less_bucket_does_not_widen_an_any_match(self):
        # A bucket with no thresholds must be *dropped*, never compiled to an
        # empty (match-everything) Q that would pull the whole base into an OR.
        CustomerSegment.objects.create(
            name="new", display_name="New", description=""
        )  # no criteria
        gold = self._tier("gold", rank=1)
        member = self._loyalty_subscriber("gold@e.com", tier=gold)
        self.make_anon_emailable("everyone@e.com")  # must NOT be swept in

        ids = self._resolve_ids(
            {
                "match": "any",
                "conditions": [
                    {"field": "customer_segment", "op": "in", "value": ["new"]},
                    {"field": "loyalty_tier", "op": "in", "value": ["gold"]},
                ],
            }
        )
        self.assertEqual(ids, {member.id})

    def test_new_numeric_field_ignores_non_numeric_value(self):
        self._loyalty_subscriber("m@e.com", points=100)
        ids = self._resolve_ids(
            {"conditions": [{"field": "loyalty_points", "op": "gte", "value": "not-a-number"}]}
        )
        # Bad value → the only condition drops → fail closed (nobody), not the base.
        self.assertEqual(ids, set())

    # --- schema: data-aware field exposure -----------------------------------

    def test_schema_hides_sources_without_data(self):
        keys = {f["key"] for f in available_rule_fields()}
        # RFM primitives are always available (shop-native, like total_spent).
        self.assertIn("lifetime_value", keys)
        self.assertIn("days_since_last_purchase", keys)
        # Source-backed fields are absent until their data exists.
        self.assertNotIn("loyalty_tier", keys)
        self.assertNotIn("is_loyalty_member", keys)
        self.assertNotIn("is_affiliate", keys)
        self.assertNotIn("customer_segment", keys)

    def test_schema_shows_sources_once_data_exists(self):
        self._tier("gold", rank=1)
        self._loyalty_subscriber("m@e.com")
        self._affiliate_subscriber("aff@e.com")
        self._vip_bucket()

        fields = {f["key"]: f for f in available_rule_fields()}
        self.assertIn("loyalty_tier", fields)
        self.assertIn("is_loyalty_member", fields)
        self.assertIn("loyalty_points", fields)
        self.assertIn("is_affiliate", fields)
        self.assertIn("customer_segment", fields)
        # Options are the live values, not a hardcoded list.
        self.assertIn("gold", [o["value"] for o in fields["loyalty_tier"]["options"]])
        self.assertIn("vip", [o["value"] for o in fields["customer_segment"]["options"]])

    def test_pending_affiliate_does_not_show_affiliate_field(self):
        # A pending affiliate isn't an active partner, so is_affiliate (which
        # matches status="active") stays hidden.
        Affiliate.objects.create(user=UserFactory(), affiliate_code="AFF-pending", status="pending")
        keys = {f["key"] for f in available_rule_fields()}
        self.assertNotIn("is_affiliate", keys)
