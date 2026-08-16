"""Region-aware navigation, Phase 3: deferred (per-visitor) nav.

A header/footer widget gated by a per-visitor rule (auth / cart / device) is
emitted as a content-less placeholder in the cacheable shell, then resolved for
the actual visitor by the personalize-nav endpoint — with an ownership/IDOR guard
that only renders placements belonging to the site's active navigation.
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.template import Context
from django.test import RequestFactory, TestCase

from design.header_footer_models import HeaderTemplate, Menu, MenuItem, Widget, WidgetPlacement
from design.services.nav_visibility import _active_nav_placement, resolve_personalized_nav
from design.templatetags.theme_tags import _placement_nav_state, render_widget
from visibility.models import RuleGroup, RuleGroupMember, VisibilityRule
from visibility.service import is_fully_visible

User = get_user_model()


def _group(rule_type="user_logged_in", operator="is_true", value=True, name="grp"):
    group = RuleGroup.objects.create(name=name)
    rule = VisibilityRule.objects.create(
        name=name, rule_type=rule_type, operator=operator, value={"value": value}
    )
    RuleGroupMember.objects.create(rule_group=group, rule=rule, order=0)
    return group


class Base(TestCase):
    def setUp(self):
        from core.models import SiteSettings

        SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                "admin_email": "admin@example.com",
                "default_currency": "USD",
                "enable_multi_warehouse": False,
            },
        )
        self.factory = RequestFactory()
        self.header = HeaderTemplate.objects.create(name="H", slug="h", is_active=True)
        self.widget = Widget.objects.create(
            name="Members note", widget_type="text", content="MEMBER-ONLY", is_active=True
        )
        self.placement = WidgetPlacement.objects.create(
            widget=self.widget, header=self.header, zone="right", order=0, is_active=True
        )

    def _req(self, authed=False):
        req = self.factory.get("/")
        req.user = User.objects.create_user("u", "u@e.com", "pw") if authed else AnonymousUser()
        req.session = {}
        req.market_slug = None
        return req


class DeferredPlaceholderTests(Base):
    def test_deferred_widget_emits_placeholder_in_shell(self):
        self.placement.rule_groups.add(_group("user_logged_in", "is_true"))
        html = render_widget(Context({"request": self._req()}), self.placement)
        self.assertIn("data-pb-defer-nav-widget", str(html))
        self.assertIn(str(self.placement.id), str(html))
        # the real content must NOT be in the shell
        self.assertNotIn("MEMBER-ONLY", str(html))

    def test_ungated_widget_renders_normally(self):
        html = str(render_widget(Context({"request": self._req()}), self.placement))
        self.assertIn("MEMBER-ONLY", html)
        self.assertNotIn("data-pb-defer-nav-widget", html)

    def test_placement_state_is_defer_for_per_visitor_rule(self):
        self.placement.rule_groups.add(_group("user_logged_in", "is_true"))
        self.assertEqual(_placement_nav_state(self.placement, self._req()), "defer")

    def test_menu_widget_with_deferred_item_defers_whole_widget(self):
        menu = Menu.objects.create(name="M", slug="m")
        item = MenuItem.objects.create(menu=menu, item_type="link", title="Members", url="/a/")
        item.rule_groups.add(_group("user_logged_in", "is_true"))
        mwidget = Widget.objects.create(
            name="Menu", widget_type="menu", config={"menu_id": menu.id}, is_active=True
        )
        mplace = WidgetPlacement.objects.create(
            widget=mwidget, header=self.header, zone="main", order=1, is_active=True
        )
        self.assertEqual(_placement_nav_state(mplace, self._req()), "defer")


class OwnershipGuardTests(Base):
    def test_active_nav_placement_returned(self):
        self.assertEqual(_active_nav_placement(self.placement.id).id, self.placement.id)

    def test_placement_in_inactive_header_rejected(self):
        self.header.is_active = False
        self.header.save()
        self.assertIsNone(_active_nav_placement(self.placement.id))

    def test_placement_with_inactive_widget_rejected(self):
        self.widget.is_active = False
        self.widget.save()
        self.assertIsNone(_active_nav_placement(self.placement.id))

    def test_inactive_placement_rejected(self):
        self.placement.is_active = False
        self.placement.save()
        self.assertIsNone(_active_nav_placement(self.placement.id))

    def test_bad_ids_rejected(self):
        self.assertIsNone(_active_nav_placement(999999))
        self.assertIsNone(_active_nav_placement("not-an-int"))
        self.assertIsNone(_active_nav_placement(None))


class PersonalizeNavTests(Base):
    def test_full_visibility_helper(self):
        self.placement.rule_groups.add(_group("user_logged_in", "is_true"))
        self.assertTrue(is_fully_visible(self.placement, self._req(authed=True)))
        self.assertFalse(is_fully_visible(self.placement, self._req(authed=False)))

    def test_entitled_visitor_gets_widget_html(self):
        self.placement.rule_groups.add(_group("user_logged_in", "is_true"))
        result = resolve_personalized_nav(self._req(authed=True), [self.placement.id])
        self.assertIn(str(self.placement.id), result)
        self.assertIn("MEMBER-ONLY", result[str(self.placement.id)] or "")

    def test_non_entitled_visitor_gets_none(self):
        self.placement.rule_groups.add(_group("user_logged_in", "is_true"))
        result = resolve_personalized_nav(self._req(authed=False), [self.placement.id])
        self.assertIsNone(result.get(str(self.placement.id)))

    def test_non_nav_placement_present_as_null_no_oracle(self):
        # a placement not part of an active header/footer must never be rendered —
        # and must be reported as null (present), not absent, so a caller can't
        # distinguish "not live nav" from "not entitled" (enumeration oracle).
        self.header.is_active = False
        self.header.save()
        result = resolve_personalized_nav(self._req(authed=True), [self.placement.id])
        self.assertIn(str(self.placement.id), result)
        self.assertIsNone(result[str(self.placement.id)])


class MarketPinningTests(Base):
    """MEDIUM fix: the deferred pass must evaluate shell region rules against the
    visitor's real market (carried on the placeholder), not the default market."""

    def setUp(self):
        super().setUp()
        from catalog.models import SalesRegion

        self.default = SalesRegion.objects.create(
            name="Global", code="GLB", default_currency="USD", priority=100
        )
        self.nz = SalesRegion.objects.create(
            name="NZ", code="NZ", slug="nz", default_currency="NZD", countries=["NZ"], priority=50
        )
        # placement gated: (geo_region == NZ)  OR  (logged in)  -> defers (has a
        # per-visitor group), and a guest is entitled only via the NZ market.
        self.placement.rule_groups.add(_group("geo_region", "equals", "NZ", name="nz"))
        self.placement.rule_groups.add(_group("user_logged_in", "is_true", True, name="auth"))

    def _req_market(self, market_slug):
        req = self._req(authed=False)
        req.market_slug = market_slug
        return req

    def test_placeholder_carries_market(self):
        # a placement that always defers (auth-only) so a placeholder is emitted,
        # and it must carry the current market for the personalization round-trip.
        widget = Widget.objects.create(name="w2", widget_type="text", content="X", is_active=True)
        place = WidgetPlacement.objects.create(
            widget=widget, header=self.header, zone="left", order=2, is_active=True
        )
        place.rule_groups.add(_group("user_logged_in", "is_true", True, name="auth2"))
        html = str(render_widget(Context({"request": self._req_market("nz")}), place))
        self.assertIn('data-pb-market="nz"', html)

    def test_region_rule_matches_when_market_pinned(self):
        # guest on the nz market: the NZ region group matches -> widget renders
        result = resolve_personalized_nav(self._req_market("nz"), [self.placement.id])
        self.assertIn("MEMBER-ONLY", result[str(self.placement.id)] or "")

    def test_region_rule_does_not_match_default_market(self):
        # guest with no market: region defaults to GLB, auth fails -> not rendered
        result = resolve_personalized_nav(self._req_market(None), [self.placement.id])
        self.assertIsNone(result[str(self.placement.id)])


class DeferredChildFilteringTests(Base):
    """Phase 5: a menu widget with a per-visitor CHILD item renders in the
    personalization pass with the child gated per visitor — the whole widget no
    longer fails closed, and the gated nested link never leaks to a guest."""

    def _menu_placement_with_gated_child(self):
        menu = Menu.objects.create(name="M", slug="m")
        parent = MenuItem.objects.create(
            menu=menu, item_type="link", title="Shop", url="/s/", is_active=True
        )
        child = MenuItem.objects.create(
            menu=menu, parent=parent, item_type="link", title="Members", url="/a/", is_active=True
        )
        child.rule_groups.add(_group("user_logged_in", "is_true"))
        mwidget = Widget.objects.create(
            name="Menu", widget_type="menu", config={"menu_id": menu.id}, is_active=True
        )
        return WidgetPlacement.objects.create(
            widget=mwidget, header=self.header, zone="main", order=1, is_active=True
        )

    def test_entitled_visitor_sees_gated_child(self):
        mplace = self._menu_placement_with_gated_child()
        result = resolve_personalized_nav(self._req(authed=True), [mplace.id])
        html = result[str(mplace.id)] or ""
        self.assertIn("Shop", html)  # ungated parent
        self.assertIn("Members", html)  # gated child — visible to a logged-in visitor

    def test_guest_sees_menu_without_gated_child(self):
        mplace = self._menu_placement_with_gated_child()
        result = resolve_personalized_nav(self._req(authed=False), [mplace.id])
        html = result[str(mplace.id)] or ""
        # the widget still renders (parent shown) but the gated nested link is gone —
        # no leak, no fail-closed blanking of the whole menu.
        self.assertIn("Shop", html)
        self.assertNotIn("Members", html)

    def test_nested_grandchild_is_gated(self):
        # depth-2 gating: parent -> child -> gated grandchild. Only the MEGA menu
        # template renders three levels (item -> child -> subchild), so exercise
        # depth-2 there — the standard dropdown only renders one level.
        menu = Menu.objects.create(name="Deep", slug="deep")
        parent = MenuItem.objects.create(
            menu=menu, item_type="link", title="Shop", url="/s/", is_active=True
        )
        child = MenuItem.objects.create(
            menu=menu, parent=parent, item_type="link", title="Sale", url="/sale/", is_active=True
        )
        grand = MenuItem.objects.create(
            menu=menu, parent=child, item_type="link", title="VIPGrand", url="/vip/", is_active=True
        )
        grand.rule_groups.add(_group("user_logged_in", "is_true"))
        mwidget = Widget.objects.create(
            name="Menu",
            widget_type="menu",
            config={"menu_id": menu.id, "mega_dropdown": True},
            is_active=True,
        )
        mplace = WidgetPlacement.objects.create(
            widget=mwidget, header=self.header, zone="main", order=1, is_active=True
        )
        guest = resolve_personalized_nav(self._req(authed=False), [mplace.id])[str(mplace.id)] or ""
        member = resolve_personalized_nav(self._req(authed=True), [mplace.id])[str(mplace.id)] or ""
        self.assertNotIn("VIPGrand", guest)
        self.assertIn("VIPGrand", member)


class ShellChildMarketGapTests(Base):
    """Phase 5: the auditor's shell market-on-child gap. A CHILD gated by a shell
    (region) rule must be filtered per market in the shell pass itself — it must
    never render for the wrong market — the same way a top-level item is. This is a
    shell-pass (full=False) rendering, no personalization round-trip."""

    def setUp(self):
        super().setUp()
        from catalog.models import SalesRegion

        SalesRegion.objects.create(name="Global", code="GLB", default_currency="USD", priority=100)
        SalesRegion.objects.create(
            name="NZ", code="NZ", slug="nz", default_currency="NZD", countries=["NZ"], priority=50
        )
        self.menu = Menu.objects.create(name="M", slug="m")
        parent = MenuItem.objects.create(
            menu=self.menu, item_type="link", title="Shop", url="/s/", is_active=True
        )
        # child visible only in the NZ market (a shell rule, not per-visitor)
        self.child = MenuItem.objects.create(
            menu=self.menu,
            parent=parent,
            item_type="link",
            title="NZDeal",
            url="/nz/",
            is_active=True,
        )
        self.child.rule_groups.add(_group("geo_region", "equals", "NZ", name="nz"))
        self.mwidget = Widget.objects.create(
            name="Menu", widget_type="menu", config={"menu_id": self.menu.id}, is_active=True
        )
        self.mplace = WidgetPlacement.objects.create(
            widget=self.mwidget, header=self.header, zone="main", order=1, is_active=True
        )

    def _shell_html(self, market_slug):
        req = self._req(authed=False)
        req.market_slug = market_slug
        return str(render_widget(Context({"request": req}), self.mplace))

    def test_region_child_hidden_on_wrong_market(self):
        # default market: the NZ-only child must NOT be in the cached shell
        self.assertNotIn("NZDeal", self._shell_html(None))

    def test_region_child_shown_on_matching_market(self):
        self.assertIn("NZDeal", self._shell_html("nz"))

    def test_region_child_never_defers(self):
        # a purely region-gated child is a shell decision — it must not force the
        # whole menu widget to defer (no per-visitor rule present).
        self.assertEqual(_placement_nav_state(self.mplace, self._req(authed=False)), "show")


class MenuDepthCapTests(Base):
    """Phase 5 DoS guard: the recursive child filter walks the WHOLE menu tree
    eagerly (the templates render at most 3 levels, but the annotation descends the
    full subtree). A merchant can nest a very deep chain (each item's parent = the
    previous); the depth cap must stop the walk well before Python's recursion
    limit, fail-closed (no visible children past the cap)."""

    def _deep_chain(self, length):
        menu = Menu.objects.create(name="Deep", slug="deep")
        root = MenuItem.objects.create(
            menu=menu, item_type="link", title="n0", url="/0/", is_active=True
        )
        node = root
        for i in range(1, length):
            node = MenuItem.objects.create(
                menu=menu,
                parent=node,
                item_type="link",
                title=f"n{i}",
                url=f"/{i}/",
                is_active=True,
            )
        return menu, root

    def test_deep_chain_walk_is_capped(self):
        from design.templatetags.theme_tags import _MAX_MENU_DEPTH, _annotate_visible_children

        menu, root = self._deep_chain(_MAX_MENU_DEPTH + 5)
        # walk from the root; must terminate (no RecursionError) and cap the depth
        _annotate_visible_children([root], self._req())
        # descend the annotated chain and confirm it is bounded at the cap
        depth, node = 0, root
        while getattr(node, "_visible_children", None):
            node = node._visible_children[0]
            depth += 1
        self.assertLessEqual(depth, _MAX_MENU_DEPTH)
