"""Behaviour 2 — resolve_segment compiles rules into a Subscriber queryset.

Segment resolution must produce a single ORM query (a ``QuerySet``), never a
per-user Python loop, and must return exactly the right members.
"""

from django.db.models import QuerySet
from djmoney.money import Money

from customers.models import CustomerMetrics
from email_marketing.models import Segment, Subscriber
from email_marketing.services.segmentation import build_segment, resolve_segment
from tests.factories import UserFactory

from .base import MarketingTestCase


class SegmentResolutionTests(MarketingTestCase):
    def _make_segment(self, kind=Segment.KIND_DYNAMIC, rules=None, slug="seg"):
        return Segment.objects.create(
            site=self.site,
            name=slug,
            slug=slug,
            kind=kind,
            rules=rules or {},
        )

    def _registered_subscriber(self, email, total_spent=None, completed_orders=0):
        user = UserFactory()
        CustomerMetrics.objects.update_or_create(
            user=user,
            defaults={
                "total_spent": Money(total_spent or 0, "USD"),
                "completed_orders": completed_orders,
            },
        )
        return self.make_subscriber(email, user=user)

    def test_resolve_returns_queryset_not_list(self):
        seg = self._make_segment(rules={})
        result = resolve_segment(seg)
        self.assertIsInstance(result, QuerySet)

    def test_empty_rules_returns_all_active_site_subscribers(self):
        a = self.make_anon_emailable("a@example.com")
        b = self.make_anon_emailable("b@example.com")
        self.make_subscriber("gone@example.com", status=Subscriber.STATUS_UNSUBSCRIBED)
        seg = self._make_segment(rules={})
        ids = set(resolve_segment(seg).values_list("id", flat=True))
        self.assertEqual(ids, {a.id, b.id})

    def test_total_spent_gte_filters_via_customer_metrics(self):
        big = self._registered_subscriber("big@example.com", total_spent=150, completed_orders=3)
        self._registered_subscriber("small@example.com", total_spent=10, completed_orders=1)
        self.make_anon_emailable("anon@example.com")  # no metrics → excluded

        seg = self._make_segment(
            rules={
                "match": "all",
                "conditions": [{"field": "total_spent", "op": "gte", "value": 100}],
            }
        )
        ids = set(resolve_segment(seg).values_list("id", flat=True))
        self.assertEqual(ids, {big.id})

    def test_has_orders_excludes_anonymous_subscribers(self):
        buyer = self._registered_subscriber("buyer@example.com", completed_orders=2)
        self._registered_subscriber("browser@example.com", completed_orders=0)
        self.make_anon_emailable("anon@example.com")  # no user → excluded by inner join

        seg = self._make_segment(
            rules={"match": "all", "conditions": [{"field": "has_orders", "op": "is_true"}]}
        )
        ids = set(resolve_segment(seg).values_list("id", flat=True))
        self.assertEqual(ids, {buyer.id})

    def test_static_segment_returns_its_members(self):
        member = self.make_anon_emailable("member@example.com")
        self.make_anon_emailable("outsider@example.com")
        seg = self._make_segment(kind=Segment.KIND_STATIC, slug="static")
        seg.members.add(member)

        ids = set(resolve_segment(seg).values_list("id", flat=True))
        self.assertEqual(ids, {member.id})

    def test_match_any_unions_conditions(self):
        spender = self._registered_subscriber("spend@example.com", total_spent=500)
        english = self.make_subscriber(
            "en@example.com", language_code="en", marketing_opt_in=True, marketing_verified=True
        )
        self.make_subscriber(
            "fr@example.com", language_code="fr", marketing_opt_in=True, marketing_verified=True
        )

        seg = self._make_segment(
            rules={
                "match": "any",
                "conditions": [
                    {"field": "total_spent", "op": "gte", "value": 100},
                    {"field": "language", "op": "eq", "value": "en"},
                ],
            }
        )
        ids = set(resolve_segment(seg).values_list("id", flat=True))
        self.assertEqual(ids, {spender.id, english.id})

    def test_match_all_intersects_conditions(self):
        # Spender AND english → only the one that is both.
        both = self._registered_subscriber("both@example.com", total_spent=500)
        both.language_code = "en"
        both.save(update_fields=["language_code"])
        spender_fr = self._registered_subscriber("fr@example.com", total_spent=500)
        spender_fr.language_code = "fr"
        spender_fr.save(update_fields=["language_code"])

        seg = self._make_segment(
            rules={
                "match": "all",
                "conditions": [
                    {"field": "total_spent", "op": "gte", "value": 100},
                    {"field": "language", "op": "eq", "value": "en"},
                ],
            }
        )
        ids = set(resolve_segment(seg).values_list("id", flat=True))
        self.assertEqual(ids, {both.id})

    def test_build_segment_caches_count(self):
        self.make_anon_emailable("a@example.com")
        self.make_anon_emailable("b@example.com")
        seg = self._make_segment(rules={})

        count = build_segment(seg)
        seg.refresh_from_db()
        self.assertEqual(count, 2)
        self.assertEqual(seg.cached_count, 2)
        self.assertIsNotNone(seg.last_built_at)

    def test_unknown_rule_field_fails_closed_to_no_members(self):
        self.make_anon_emailable("a@example.com")
        seg = self._make_segment(
            rules={"match": "all", "conditions": [{"field": "made_up", "op": "eq", "value": 1}]}
        )
        # Conditions were specified but none are valid → fail closed (nobody),
        # never blast the whole active base. (An *empty* rule set still means
        # "all", covered by test_empty_rules_returns_all_active_site_subscribers.)
        ids = set(resolve_segment(seg).values_list("id", flat=True))
        self.assertEqual(ids, set())

    def test_total_spent_invalid_value_is_ignored(self):
        # A non-numeric value must not blow up resolution.
        self._registered_subscriber("x@example.com", total_spent=50)
        seg = self._make_segment(
            rules={
                "match": "all",
                "conditions": [{"field": "total_spent", "op": "gte", "value": "not-a-number"}],
            }
        )
        result = resolve_segment(seg)
        self.assertIsInstance(result, QuerySet)
        # The only condition dropped → fail closed (no members), not the whole base.
        self.assertEqual(result.count(), 0)
