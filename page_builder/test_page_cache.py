"""Tests for the market/language/currency-aware page cache key and the temporal
visibility TTL guard (step 3 of the multi-market work).

The currency-in-key test doubles as the cache-leak guard: if a future change drops
currency (or market/language) from the key, one visitor's cached variant could be
served to another, and these fail.
"""

from django.core.cache import cache
from django.test import RequestFactory, TestCase

from page_builder.models import Element, Page
from page_builder.views import PageView
from visibility.models import RuleGroup, RuleGroupMember, VisibilityRule


def _rule(rule_type, value, operator="equals"):
    return VisibilityRule.objects.create(
        name=rule_type, rule_type=rule_type, operator=operator, value=value
    )


def _group_with(rule):
    group = RuleGroup.objects.create(name="g", logic_operator="OR")
    RuleGroupMember.objects.create(rule_group=group, rule=rule, order=0)
    return group


class PageCacheKeyTests(TestCase):
    def setUp(self):
        cache.clear()
        self.factory = RequestFactory()
        self.page = Page.objects.create(
            title="H", slug="cache-home", page_type="home", status="published"
        )

    def _req(self, market=None, lang="en", currency="USD"):
        req = self.factory.get("/")
        req.market_slug = market
        req.LANGUAGE_CODE = lang
        req.currency = currency
        return req

    def test_key_varies_by_currency(self):
        a = PageView._page_cache_key_prefix(self._req(currency="USD"), self.page)
        b = PageView._page_cache_key_prefix(self._req(currency="NZD"), self.page)
        self.assertNotEqual(a, b)

    def test_key_varies_by_market(self):
        a = PageView._page_cache_key_prefix(self._req(market=None), self.page)
        b = PageView._page_cache_key_prefix(self._req(market="nz"), self.page)
        self.assertNotEqual(a, b)

    def test_key_varies_by_language(self):
        a = PageView._page_cache_key_prefix(self._req(lang="en"), self.page)
        b = PageView._page_cache_key_prefix(self._req(lang="fr"), self.page)
        self.assertNotEqual(a, b)

    def test_same_context_same_key(self):
        a = PageView._page_cache_key_prefix(self._req(), self.page)
        b = PageView._page_cache_key_prefix(self._req(), self.page)
        self.assertEqual(a, b)


class TemporalCacheGuardTests(TestCase):
    def setUp(self):
        cache.clear()
        self.page = Page.objects.create(
            title="H", slug="temporal-home", page_type="home", status="published"
        )

    def _element_with(self, rule):
        el = Element.objects.create(page=self.page, name="e", element_type="text")
        el.visibility_rules.add(_group_with(rule))
        return el

    def test_shell_only_page_has_no_temporal_rules(self):
        self._element_with(_rule("geo_region", "NZ"))
        cache.clear()
        self.assertFalse(self.page.has_temporal_visibility_rules())

    def test_business_hours_rule_is_detected(self):
        self._element_with(_rule("business_hours", True, operator="is_true"))
        cache.clear()
        self.assertTrue(self.page.has_temporal_visibility_rules())
        # And the cache would be capped for such a page.
        self.assertEqual(
            min(self.page.cache_timeout, PageView.TEMPORAL_CACHE_MAX_SECONDS),
            PageView.TEMPORAL_CACHE_MAX_SECONDS,
        )

    def test_nested_child_temporal_rule_is_detected(self):
        # A page=NULL child inside a container with a temporal rule must still be
        # detected (the page's element tree is walked, not just top-level).
        container = Element.objects.create(page=self.page, name="box", element_type="container")
        child = Element.objects.create(name="c", element_type="text", parent_element=container)
        child.visibility_rules.add(_group_with(_rule("business_hours", True, operator="is_true")))
        cache.clear()
        self.assertTrue(self.page.has_temporal_visibility_rules())

    def test_element_change_bumps_visibility_version(self):
        # Moving/activating an element must invalidate the derived temporal flag.
        # The bump is deferred to transaction commit, so run the on_commit
        # callbacks that TestCase's wrapping transaction would otherwise swallow.
        from visibility.models import visibility_config_version

        before = visibility_config_version()
        with self.captureOnCommitCallbacks(execute=True):
            Element.objects.create(page=self.page, name="moved", element_type="text")
        self.assertGreater(visibility_config_version(), before)

    def test_temporal_flag_invalidated_when_rule_added(self):
        # Flag caches False for a page with no temporal rules...
        self.assertFalse(self.page.has_temporal_visibility_rules())
        # ...then adding a temporal rule via the M2M (no Page.save) bumps the
        # visibility-config version on commit, so the next read recomputes True.
        with self.captureOnCommitCallbacks(execute=True):
            el = Element.objects.create(page=self.page, name="e", element_type="text")
            el.visibility_rules.add(_group_with(_rule("business_hours", True, operator="is_true")))
        self.assertTrue(self.page.has_temporal_visibility_rules())

    def test_rolled_back_element_change_does_not_bump(self):
        # Regression: the version must only bump once the enclosing transaction
        # commits. A rolled-back change must leave the cached version untouched.
        from django.db import transaction

        from visibility.models import visibility_config_version

        before = visibility_config_version()
        with self.captureOnCommitCallbacks(execute=True):
            try:
                with transaction.atomic():
                    Element.objects.create(page=self.page, name="rb", element_type="text")
                    raise RuntimeError("force rollback")
            except RuntimeError:
                pass
        self.assertEqual(visibility_config_version(), before)

    def test_nested_temporal_rule_is_detected(self):
        # A temporal rule buried in a nested child group must still be found.
        parent = RuleGroup.objects.create(name="p", logic_operator="OR")
        child = RuleGroup.objects.create(name="c", logic_operator="OR", parent_group=parent)
        RuleGroupMember.objects.create(
            rule_group=child,
            rule=_rule("time_range", {"start": "09:00", "end": "17:00"}),
            order=0,
        )
        el = Element.objects.create(page=self.page, name="e", element_type="text")
        el.visibility_rules.add(parent)
        cache.clear()
        self.assertTrue(self.page.has_temporal_visibility_rules())
