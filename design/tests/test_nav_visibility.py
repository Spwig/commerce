"""Region-aware navigation, Phases 1–2.

Phase 1 (``*AttachTests``): the shared visibility engine (``visibility.RuleGroup``)
is *attachable* to nav models — ``MenuItem`` and ``WidgetPlacement`` — with the
same rule model that gates page elements.

Phase 2 (``NavShellVisibilityTests``): those rules are *evaluated* during nav
render. Shell rules (geo_region/market, language, currency) and temporal rules
resolve server-side, deterministic per market URL; per-visitor (deferred) rules
fail closed until Phase 3 adds nav placeholders.
"""

from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from django.test import RequestFactory, TestCase

from catalog.models import SalesRegion
from design.header_footer_models import (
    HeaderTemplate,
    Menu,
    MenuItem,
    Widget,
    WidgetPlacement,
)
from design.templatetags.theme_tags import _filter_visible_menu_items, _nav_shell_visible
from visibility.models import RuleGroup, RuleGroupMember, VisibilityRule
from visibility.service import resolve_visibility


def _rule(rule_type="geo_region", value="NZ", operator="equals"):
    return VisibilityRule.objects.create(
        name=f"{rule_type}={value}",
        rule_type=rule_type,
        operator=operator,
        value={"value": value},
    )


def _group_with(rule):
    group = RuleGroup.objects.create(name="grp")
    RuleGroupMember.objects.create(rule_group=group, rule=rule, order=0)
    return group


class MenuItemRuleGroupAttachTests(TestCase):
    def test_menu_item_can_attach_rule_group(self):
        menu = Menu.objects.create(name="Main", slug="main")
        item = MenuItem.objects.create(menu=menu, item_type="link", title="Shop", url="/shop/")
        group = _group_with(_rule("geo_region", "NZ"))

        item.rule_groups.add(group)

        self.assertEqual(list(item.rule_groups.all()), [group])
        # reverse accessor on the shared RuleGroup resolves back to the item
        self.assertEqual(list(group.menu_items.all()), [item])

    def test_menu_item_rule_groups_default_empty(self):
        menu = Menu.objects.create(name="Main", slug="main2")
        item = MenuItem.objects.create(menu=menu, item_type="link", title="Shop", url="/shop/")
        self.assertEqual(item.rule_groups.count(), 0)

    def test_legacy_visibility_rules_json_is_untouched(self):
        # Phase 1 does not disturb the legacy shallow JSON — it stays live until
        # Phase 2 supersedes it.
        menu = Menu.objects.create(name="Main", slug="main3")
        item = MenuItem.objects.create(
            menu=menu,
            item_type="link",
            title="Members",
            url="/account/",
            visibility_rules=[{"type": "user_status", "value": "logged_in"}],
        )
        item.refresh_from_db()
        self.assertEqual(item.visibility_rules, [{"type": "user_status", "value": "logged_in"}])


class WidgetPlacementRuleGroupAttachTests(TestCase):
    def test_widget_placement_can_attach_rule_group(self):
        header = HeaderTemplate.objects.create(name="H", slug="h")
        widget = Widget.objects.create(name="Cart", widget_type="cart")
        placement = WidgetPlacement.objects.create(
            widget=widget, header=header, zone="right", order=0
        )
        group = _group_with(_rule("selected_currency", "NZD"))

        placement.rule_groups.add(group)

        self.assertEqual(list(placement.rule_groups.all()), [group])
        self.assertEqual(list(group.widget_placements.all()), [placement])


class NavShellVisibilityTests(TestCase):
    """Phase 2: nav objects are filtered by the shared engine's SHELL decision —
    market/geo, language, currency, time — server-side, deterministic per market
    URL. Per-visitor (deferred) nav rules fail closed until Phase 3."""

    def setUp(self):
        cache.clear()
        self.factory = RequestFactory()
        # Mirror the page-engine determinism tests: default market is the
        # highest-priority region and is served unprefixed.
        self.default = SalesRegion.objects.create(
            name="Global", code="GLB", default_currency="USD", priority=100
        )
        self.nz = SalesRegion.objects.create(
            name="New Zealand",
            code="NZ",
            slug="nz",
            default_currency="NZD",
            countries=["NZ"],
            priority=50,
        )
        self.menu = Menu.objects.create(name="Main", slug="main-p2")

    def _req(self, market_slug=None):
        req = self.factory.get("/")
        req.user = AnonymousUser()
        req.session = {}
        req.market_slug = market_slug
        return req

    def _menu_item(self, **kw):
        kw.setdefault("item_type", "link")
        kw.setdefault("url", "/x/")
        return MenuItem.objects.create(menu=self.menu, **kw)

    def test_menu_item_geo_rule_shown_in_matching_market(self):
        item = self._menu_item(title="NZ deals")
        item.rule_groups.add(_group_with(_rule("geo_region", "NZ")))
        self.assertEqual(resolve_visibility(item, self._req("nz")), "show")
        self.assertTrue(_nav_shell_visible(item, self._req("nz")))

    def test_menu_item_geo_rule_hidden_in_default_market(self):
        item = self._menu_item(title="NZ deals")
        item.rule_groups.add(_group_with(_rule("geo_region", "NZ")))
        self.assertEqual(resolve_visibility(item, self._req(None)), "hide")
        self.assertFalse(_nav_shell_visible(item, self._req(None)))

    def test_widget_placement_geo_rule_filtered_by_market(self):
        header = HeaderTemplate.objects.create(name="H2", slug="h2")
        widget = Widget.objects.create(name="Banner", widget_type="text")
        placement = WidgetPlacement.objects.create(
            widget=widget, header=header, zone="top", order=0
        )
        placement.rule_groups.add(_group_with(_rule("geo_region", "NZ")))
        self.assertTrue(_nav_shell_visible(placement, self._req("nz")))
        self.assertFalse(_nav_shell_visible(placement, self._req(None)))

    def test_deferred_nav_rule_fails_closed_in_shell(self):
        # A per-visitor (auth) rule resolves to "defer"; Phase 2 nav has no
        # placeholder mechanism yet, so it must fail closed (hidden) — never leak.
        item = self._menu_item(title="Members")
        item.rule_groups.add(_group_with(_rule("user_logged_in", True, operator="is_true")))
        self.assertEqual(resolve_visibility(item, self._req(None)), "defer")
        self.assertFalse(_nav_shell_visible(item, self._req(None)))

    def test_ungated_nav_item_always_shown(self):
        item = self._menu_item(title="Home", url="/")
        self.assertTrue(_nav_shell_visible(item, self._req(None)))

    def test_only_inactive_group_restores_visibility(self):
        # Disabling every rule group on an item un-gates it (an inactive group is
        # not a "hide" switch) — regression for the codex P2 finding.
        item = self._menu_item(title="NZ deals")
        group = _group_with(_rule("geo_region", "NZ"))
        group.is_active = False
        group.save()
        item.rule_groups.add(group)
        self.assertEqual(resolve_visibility(item, self._req(None)), "show")
        self.assertTrue(_nav_shell_visible(item, self._req(None)))

    def test_inactive_item_hidden(self):
        item = self._menu_item(title="Off", is_active=False)
        self.assertFalse(_nav_shell_visible(item, self._req(None)))

    def test_filter_visible_menu_items_drops_wrong_market(self):
        keep = self._menu_item(title="Global")
        drop = self._menu_item(title="NZ only")
        drop.rule_groups.add(_group_with(_rule("geo_region", "NZ")))
        visible = _filter_visible_menu_items([keep, drop], self._req(None))
        self.assertEqual(visible, [keep])
