"""Behaviour matrix for the visibility-rule capability.

One place that exercises every rule type end-to-end through the RuleEvaluator, so
the capability (market-aware + personalized page content) is discoverable and the
render-stage taxonomy is pinned. Also honestly records the rule types that are
declared but NOT yet evaluated, so they aren't mistaken for shipped behaviour.
"""

from django.test import SimpleTestCase, TestCase
from django.utils import timezone

from page_builder.models import Element, Page
from page_builder.services.visibility_service import (
    resolve_element_visibility,
    resolve_personalized_elements,
)
from visibility.evaluator import RuleEvaluator
from visibility.models import RuleGroup, RuleGroupMember, VisibilityRule


def _base_context():
    now = timezone.localtime(timezone.now())
    return {
        "user": {
            "is_authenticated": False,
            "groups": [],
            "segment": None,
            "lifetime_value": 0,
            "order_count": 0,
            "username": None,
        },
        "geo": {"country_code": None, "region": None, "city": None, "timezone": None},
        "device": {
            "device_type": "desktop",
            "browser": "firefox",
            "operating_system": "linux",
            "screen_width": 0,
        },
        "time": {
            "date": now.date(),
            "time": now.time(),
            "day_name": now.strftime("%A"),
            "is_business_hours": False,
        },
        "behavior": {
            "is_first_visit": False,
            "visit_count": 1,
            "page_views": 0,
            "referrer": "",
        },
        "ecommerce": {
            "cart_value": 0,
            "cart_items": 0,
            "has_purchased": False,
            "has_abandoned_cart": False,
            "wishlist_items": 0,
        },
        "language": {
            "browser_language": "fr",
            "selected_language": "fr",
            "selected_currency": "EUR",
        },
        "utm": {"utm_campaign": ""},
    }


def _merge(patch):
    ctx = _base_context()
    for section, values in patch.items():
        ctx[section].update(values)
    return ctx


# (rule_type, operator, value, matching context patch). Each rule must match under
# its patch and NOT match under the base context.
_TODAY = timezone.localtime(timezone.now())
MATRIX = [
    ("geo_country", "equals", "NZ", {"geo": {"country_code": "NZ"}}),
    ("geo_region", "equals", "APAC", {"geo": {"region": "APAC"}}),
    ("geo_city", "equals", "Auckland", {"geo": {"city": "Auckland"}}),
    ("geo_timezone", "equals", "Pacific/Auckland", {"geo": {"timezone": "Pacific/Auckland"}}),
    ("user_logged_in", "is_true", True, {"user": {"is_authenticated": True}}),
    ("user_group", "in_list", ["vip"], {"user": {"groups": ["vip"]}}),
    ("user_segment", "equals", "gold", {"user": {"segment": "gold"}}),
    ("user_lifetime_value", "greater_than", 100, {"user": {"lifetime_value": 250}}),
    ("user_order_count", "greater_than", 5, {"user": {"order_count": 12}}),
    ("device_type", "equals", "mobile", {"device": {"device_type": "mobile"}}),
    ("browser", "equals", "chrome", {"device": {"browser": "chrome"}}),
    ("operating_system", "equals", "windows", {"device": {"operating_system": "windows"}}),
    ("screen_size", "greater_than", 768, {"device": {"screen_width": 1024}}),
    (
        "date_range",
        "equals",
        {
            "start": (_TODAY.date().replace(day=1)).isoformat(),
            "end": _TODAY.date().isoformat(),
        },
        {},  # today is within [first-of-month, today]
    ),
    ("time_range", "equals", {"start": "00:00", "end": "23:59"}, {}),
    ("day_of_week", "in_list", [_TODAY.strftime("%A")], {}),
    ("business_hours", "is_true", True, {"time": {"is_business_hours": True}}),
    ("first_visit", "is_true", True, {"behavior": {"is_first_visit": True}}),
    ("visit_count", "greater_than", 2, {"behavior": {"visit_count": 5}}),
    ("page_views", "greater_than", 1, {"behavior": {"page_views": 4}}),
    ("referrer", "contains", "google", {"behavior": {"referrer": "https://google.com/"}}),
    ("utm_campaign", "equals", "summer", {"utm": {"utm_campaign": "summer"}}),
    ("cart_value", "greater_than", 50, {"ecommerce": {"cart_value": 120}}),
    ("cart_items", "greater_than", 0, {"ecommerce": {"cart_items": 3}}),
    ("has_purchased", "is_true", True, {"ecommerce": {"has_purchased": True}}),
    ("abandoned_cart", "is_true", True, {"ecommerce": {"has_abandoned_cart": True}}),
    ("wishlist_items", "greater_than", 0, {"ecommerce": {"wishlist_items": 2}}),
    ("browser_language", "equals", "en", {"language": {"browser_language": "en"}}),
    ("selected_language", "equals", "en", {"language": {"selected_language": "en"}}),
    ("selected_currency", "equals", "USD", {"language": {"selected_currency": "USD"}}),
]

# Declared in RULE_TYPES but with no branch in RuleEvaluator._evaluate_rule_type —
# they never match. Pinned here so they read as planned-not-shipped, not as
# working behaviour.
UNIMPLEMENTED_RULE_TYPES = ["connection_speed", "time_on_site"]


class RuleEvaluationMatrixTests(SimpleTestCase):
    def setUp(self):
        self.evaluator = RuleEvaluator()

    def _rule(self, rule_type, operator, value):
        # cache_duration=0 → evaluate_single_rule never touches the cache/DB.
        return VisibilityRule(
            name=rule_type,
            rule_type=rule_type,
            operator=operator,
            value=value,
            is_active=True,
            cache_duration=0,
        )

    def test_every_rule_type_is_in_the_matrix(self):
        covered = {row[0] for row in MATRIX} | set(UNIMPLEMENTED_RULE_TYPES)
        declared = {rt for rt, _label in VisibilityRule.RULE_TYPES}
        self.assertEqual(covered, declared, "A rule type is missing from the behaviour matrix")

    def test_each_rule_matches_and_rejects(self):
        for rule_type, operator, value, patch in MATRIX:
            with self.subTest(rule_type=rule_type):
                rule = self._rule(rule_type, operator, value)
                self.assertTrue(
                    self.evaluator.evaluate_single_rule(rule, _merge(patch)),
                    f"{rule_type} should match its context",
                )
                if patch:  # time rules match the base context by design
                    self.assertFalse(
                        self.evaluator.evaluate_single_rule(rule, _base_context()),
                        f"{rule_type} should not match the base context",
                    )

    def test_builder_dict_values_are_unwrapped(self):
        # The rule builder saves {"value": n} / {"values": [...]}; the evaluator
        # must compare against the real gate, not the wrapper dict.
        numeric = self._rule("cart_value", "greater_than", {"value": 50})
        self.assertTrue(
            self.evaluator.evaluate_single_rule(numeric, _merge({"ecommerce": {"cart_value": 120}}))
        )
        self.assertFalse(
            self.evaluator.evaluate_single_rule(numeric, _merge({"ecommerce": {"cart_value": 10}}))
        )

        listed = self._rule("user_group", "in_list", {"values": ["vip", "gold"]})
        self.assertTrue(
            self.evaluator.evaluate_single_rule(listed, _merge({"user": {"groups": ["vip"]}}))
        )
        self.assertFalse(
            self.evaluator.evaluate_single_rule(listed, _merge({"user": {"groups": ["silver"]}}))
        )

    def test_unimplemented_rule_types_never_match(self):
        for rule_type in UNIMPLEMENTED_RULE_TYPES:
            with self.subTest(rule_type=rule_type):
                rule = self._rule(rule_type, "is_true", True)
                self.assertFalse(
                    self.evaluator.evaluate_single_rule(rule, _merge({"behavior": {}})),
                    f"{rule_type} is not implemented and must not silently match",
                )

    def test_render_stage_classification(self):
        shell = {"geo_region", "selected_language", "selected_currency"}
        temporal = {"date_range", "time_range", "day_of_week", "business_hours"}
        for rule_type, _label in VisibilityRule.RULE_TYPES:
            with self.subTest(rule_type=rule_type):
                stage = self._rule(rule_type, "equals", "x").render_stage
                if rule_type in shell:
                    self.assertEqual(stage, VisibilityRule.RENDER_STAGE_SHELL)
                elif rule_type in temporal:
                    self.assertEqual(stage, VisibilityRule.RENDER_STAGE_TEMPORAL)
                else:
                    self.assertEqual(stage, VisibilityRule.RENDER_STAGE_DEFERRED)


class VisibilityServiceSeamTests(TestCase):
    """Direct behaviour tests for the capability seam functions."""

    def setUp(self):
        from django.contrib.auth import get_user_model
        from django.core.cache import cache
        from django.test import RequestFactory

        from catalog.models import SalesRegion

        cache.clear()
        self.factory = RequestFactory()
        self.nz = SalesRegion.objects.create(
            name="NZ", code="NZ", slug="nz", default_currency="NZD", countries=["NZ"]
        )
        self.sg = SalesRegion.objects.create(
            name="SG", code="SG", slug="sg", default_currency="SGD", countries=["SG"]
        )
        self.page = Page.objects.create(
            title="P", slug="seam", page_type="page", status="published"
        )
        self.User = get_user_model()

    def _rule(self, rule_type, value, operator="equals"):
        return VisibilityRule.objects.create(
            name=rule_type, rule_type=rule_type, operator=operator, value=value
        )

    def _group(self, rule):
        g = RuleGroup.objects.create(name="g", logic_operator="OR")
        RuleGroupMember.objects.create(rule_group=g, rule=rule, order=0)
        return g

    def _request(self, market):
        from django.contrib.auth.models import AnonymousUser

        req = self.factory.get("/")
        req.user = AnonymousUser()
        req.session = {}
        req.sales_region = market
        req.market_slug = market.slug
        return req

    def test_resolve_element_visibility_show_hide_defer(self):
        shell_el = Element.objects.create(page=self.page, name="a", element_type="text")
        shell_el.visibility_rules.add(self._group(self._rule("geo_region", "NZ")))
        self.assertEqual(resolve_element_visibility(shell_el, self._request(self.nz)), "show")
        self.assertEqual(resolve_element_visibility(shell_el, self._request(self.sg)), "hide")

        deferred_el = Element.objects.create(page=self.page, name="b", element_type="text")
        deferred_el.visibility_rules.add(
            self._group(self._rule("cart_value", 50, operator="greater_than"))
        )
        self.assertEqual(resolve_element_visibility(deferred_el, self._request(self.nz)), "defer")

    def test_resolve_personalized_elements_only_entitled(self):
        el = Element.objects.create(page=self.page, name="c", element_type="text")
        el.visibility_rules.add(self._group(self._rule("user_logged_in", True, operator="is_true")))
        req = self._request(self.nz)  # anonymous
        result = resolve_personalized_elements(self.page, [el.id], req)
        self.assertIsNone(result[str(el.id)])
