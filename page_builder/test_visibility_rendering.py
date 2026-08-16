"""Tests for the Stage-1 server-side visibility render hook and the rule-type
render-stage taxonomy (step 2 of the multi-market work).
"""

import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from django.template import Context
from django.test import RequestFactory, TestCase
from django.urls import reverse

from catalog.models import SalesRegion
from page_builder.models import Element, Page
from page_builder.templatetags.element_tags import render_element
from visibility.models import RuleGroup, RuleGroupMember, VisibilityRule


def _rule(rule_type, value, operator="equals"):
    return VisibilityRule.objects.create(
        name=f"{rule_type}={value}", rule_type=rule_type, operator=operator, value=value
    )


def _group_with(rule, logic="OR"):
    group = RuleGroup.objects.create(name="grp", logic_operator=logic)
    RuleGroupMember.objects.create(rule_group=group, rule=rule, order=0)
    return group


class RenderStageTaxonomyTests(TestCase):
    def test_shell_rules(self):
        for rt in ("geo_region", "selected_language", "selected_currency"):
            self.assertEqual(_rule(rt, "x").render_stage, VisibilityRule.RENDER_STAGE_SHELL)

    def test_temporal_rules(self):
        for rt in ("date_range", "time_range", "day_of_week", "business_hours"):
            self.assertEqual(_rule(rt, "x").render_stage, VisibilityRule.RENDER_STAGE_TEMPORAL)

    def test_deferred_rules(self):
        for rt in ("cart_value", "user_logged_in", "device_type", "geo_country", "first_visit"):
            rule = _rule(rt, "x")
            self.assertEqual(rule.render_stage, VisibilityRule.RENDER_STAGE_DEFERRED)
            self.assertTrue(rule.is_deferred)

    def test_shell_rule_is_not_deferred(self):
        self.assertFalse(_rule("geo_region", "NZ").is_deferred)


class GroupClassificationTests(TestCase):
    def test_group_with_only_shell_rules_is_not_deferred(self):
        group = _group_with(_rule("geo_region", "NZ"))
        self.assertFalse(group.contains_deferred_rule())

    def test_group_with_a_deferred_rule_is_deferred(self):
        group = _group_with(_rule("cart_value", 100, operator="greater_than"))
        self.assertTrue(group.contains_deferred_rule())

    def test_nested_child_group_deferred_bubbles_up(self):
        parent = _group_with(_rule("geo_region", "NZ"))
        child = _group_with(_rule("user_logged_in", True, operator="is_true"))
        child.parent_group = parent
        child.save()
        self.assertTrue(parent.contains_deferred_rule())


class ElementVisibilityTests(TestCase):
    def setUp(self):
        cache.clear()  # rule-eval micro-cache is locmem and persists across tests
        self.factory = RequestFactory()
        self.page = Page.objects.create(
            title="Home", slug="home-test", page_type="home", status="published"
        )
        self.nz = SalesRegion.objects.create(
            name="New Zealand", code="NZ", slug="nz", default_currency="NZD", countries=["NZ"]
        )
        self.sg = SalesRegion.objects.create(
            name="Singapore", code="SG", slug="sg", default_currency="SGD", countries=["SG"]
        )

    def _element(self, **kw):
        defaults = {"page": self.page, "name": "el", "element_type": "text"}
        defaults.update(kw)
        return Element.objects.create(**defaults)

    def _request(self, path="/", market=None):
        req = self.factory.get(path)
        req.user = AnonymousUser()
        req.session = {}
        if market is not None:
            req.sales_region = market
            req.market_slug = market.slug  # URL-authoritative market, as MarketMiddleware sets
        return req

    def test_no_rules_is_always_renderable(self):
        el = self._element()
        self.assertTrue(el.is_renderable(self._request(market=self.nz)))

    def test_inactive_element_is_not_renderable(self):
        el = self._element(is_active=False)
        self.assertFalse(el.is_renderable(self._request(market=self.nz)))

    def test_geo_region_rule_matches_pinned_market(self):
        el = self._element()
        el.visibility_rules.add(_group_with(_rule("geo_region", "NZ")))
        self.assertTrue(el.is_renderable(self._request(market=self.nz)))
        self.assertFalse(el.is_renderable(self._request(market=self.sg)))

    def test_shell_defers_deferred_only_element(self):
        # A per-visitor (deferred) rule must NOT be evaluated into the cacheable
        # shell — the element is DEFERRED (content-less placeholder) and resolved
        # by the personalization pass, so it never leaks via the page cache.
        el = self._element()
        el.visibility_rules.add(_group_with(_rule("cart_value", 50, operator="greater_than")))
        self.assertEqual(el.shell_visibility(self._request(market=self.sg)), "defer")

    def test_shell_shows_or_hides_shell_rule_by_market(self):
        el = self._element()
        el.visibility_rules.add(_group_with(_rule("geo_region", "NZ")))
        self.assertEqual(el.shell_visibility(self._request(market=self.nz)), "show")
        self.assertEqual(el.shell_visibility(self._request(market=self.sg)), "hide")

    def test_shell_shows_element_with_no_rules(self):
        el = self._element()
        self.assertEqual(el.shell_visibility(self._request(market=self.nz)), "show")

    def test_inactive_deferred_rule_does_not_force_defer(self):
        # A group with an active shell rule + an INACTIVE deferred rule stays
        # shell-safe (the disabled rule must not push it to the deferred path).
        el = self._element()
        group = RuleGroup.objects.create(name="mixed", logic_operator="OR")
        RuleGroupMember.objects.create(rule_group=group, rule=_rule("geo_region", "NZ"), order=0)
        inactive = _rule("cart_value", 50, operator="greater_than")
        inactive.is_active = False
        inactive.save()
        RuleGroupMember.objects.create(rule_group=group, rule=inactive, order=1)
        el.visibility_rules.add(group)
        self.assertEqual(el.shell_visibility(self._request(market=self.nz)), "show")
        self.assertEqual(el.shell_visibility(self._request(market=self.sg)), "hide")

    def test_requires_personalization_reflects_rule_stage(self):
        shell_el = self._element()
        shell_el.visibility_rules.add(_group_with(_rule("geo_region", "NZ")))
        self.assertFalse(shell_el.requires_personalization())

        deferred_el = self._element()
        deferred_el.visibility_rules.add(
            _group_with(_rule("cart_value", 50, operator="greater_than"))
        )
        self.assertTrue(deferred_el.requires_personalization())

    def test_device_toggle_does_not_server_omit(self):
        # show_on_mobile is a CSS/responsive concern, not a server-omit — a
        # mobile request must still render the element (hidden via CSS class).
        el = self._element(show_on_mobile=False)
        req = self._request(market=self.nz)
        req.META["HTTP_USER_AGENT"] = "Mozilla/5.0 (iPhone; CPU iPhone OS) Mobile"
        self.assertTrue(el.is_renderable(req))


class RenderElementHookTests(TestCase):
    def setUp(self):
        cache.clear()  # rule-eval micro-cache is locmem and persists across tests
        self.factory = RequestFactory()
        self.page = Page.objects.create(
            title="Home", slug="home-hook", page_type="home", status="published"
        )
        self.sg = SalesRegion.objects.create(
            name="Singapore", code="SG", slug="sg", default_currency="SGD", countries=["SG"]
        )

    def _hidden_element(self):
        el = Element.objects.create(page=self.page, name="nz-only", element_type="text")
        el.visibility_rules.add(_group_with(_rule("geo_region", "NZ")))
        return el

    def _request(self, path):
        req = self.factory.get(path)
        req.user = AnonymousUser()
        req.session = {}
        req.sales_region = self.sg  # SG visitor; NZ-only element should hide
        req.market_slug = self.sg.slug
        return req

    def test_storefront_omits_hidden_element(self):
        el = self._hidden_element()
        result = render_element(Context({"request": self._request("/")}), el)
        self.assertEqual(result, {"hidden": True})

    def test_builder_never_hides_element(self):
        el = self._hidden_element()
        # Builder path bypasses visibility so the merchant can edit hidden blocks
        result = render_element(Context({"request": self._request("/visual-builder/1/")}), el)
        self.assertNotEqual(result.get("hidden"), True)

    def test_storefront_defers_per_visitor_element(self):
        # A cart-value (deferred) element becomes a placeholder, not content —
        # its per-visitor decision never enters the (cacheable) shell HTML.
        el = Element.objects.create(page=self.page, name="cart-only", element_type="text")
        el.visibility_rules.add(_group_with(_rule("cart_value", 50, operator="greater_than")))
        result = render_element(Context({"request": self._request("/")}), el)
        self.assertEqual(result, {"deferred": True, "element": el})


class PersonalizeEndpointTests(TestCase):
    def setUp(self):
        cache.clear()
        # The endpoint runs through the full middleware stack, which resolves
        # SiteSettings — seed the singleton so those lookups don't 500.
        from core.models import SiteSettings

        SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                "admin_email": "admin@example.com",
                "default_currency": "USD",
                "enable_multi_warehouse": False,
            },
        )
        self.page = Page.objects.create(
            title="H", slug="perso-home", page_type="home", status="published"
        )
        self.other_page = Page.objects.create(
            title="O", slug="perso-other", page_type="page", status="published"
        )

    def _deferred_element(self, page):
        el = Element.objects.create(page=page, name="d", element_type="text")
        el.visibility_rules.add(_group_with(_rule("user_logged_in", True, operator="is_true")))
        return el

    def _post(self, payload):
        return self.client.post(
            reverse("page_builder_api:personalize"),
            data=json.dumps(payload),
            content_type="application/json",
        )

    def test_get_not_allowed(self):
        self.assertEqual(self.client.get(reverse("page_builder_api:personalize")).status_code, 405)

    def test_invalid_json_returns_400(self):
        resp = self.client.post(
            reverse("page_builder_api:personalize"),
            data="not json",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 400)

    def test_unknown_page_returns_404(self):
        self.assertEqual(self._post({"page_id": 999999, "element_ids": [1]}).status_code, 404)

    def test_logged_in_element_shown_to_authenticated(self):
        el = self._deferred_element(self.page)
        user = get_user_model().objects.create_user(username="u", password="x")
        self.client.force_login(user)
        resp = self._post({"page_id": self.page.id, "element_ids": [el.id]})
        self.assertEqual(resp.status_code, 200)
        html = resp.json()["elements"][str(el.id)]
        self.assertIsNotNone(html)
        self.assertNotIn("element-error", html)  # real content, not a render error

    def test_logged_in_element_hidden_for_anonymous(self):
        el = self._deferred_element(self.page)
        resp = self._post({"page_id": self.page.id, "element_ids": [el.id]})
        self.assertEqual(resp.status_code, 200)
        self.assertIsNone(resp.json()["elements"][str(el.id)])

    def test_element_from_other_page_is_ignored(self):
        el = self._deferred_element(self.other_page)  # belongs to a different page
        resp = self._post({"page_id": self.page.id, "element_ids": [el.id]})
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn(str(el.id), resp.json()["elements"])

    def _gated_container_with_child(self):
        container = Element.objects.create(page=self.page, name="vip", element_type="container")
        container.visibility_rules.add(
            _group_with(_rule("user_logged_in", True, operator="is_true"))
        )
        # Plain child with NO rules of its own — gated only by its container.
        # page=None, linked to the page only via parent_element (real data model).
        child = Element.objects.create(name="secret", element_type="text", parent_element=container)
        return child

    def test_child_of_gated_container_hidden_for_anonymous(self):
        # IDOR guard: a child of a members-only container must not render for an
        # anonymous caller who POSTs the child id directly.
        child = self._gated_container_with_child()
        resp = self._post({"page_id": self.page.id, "element_ids": [child.id]})
        self.assertEqual(resp.status_code, 200)
        self.assertIsNone(resp.json()["elements"][str(child.id)])

    def test_child_of_gated_container_shown_for_authenticated(self):
        child = self._gated_container_with_child()
        user = get_user_model().objects.create_user(username="v", password="x")
        self.client.force_login(user)
        resp = self._post({"page_id": self.page.id, "element_ids": [child.id]})
        self.assertIsNotNone(resp.json()["elements"][str(child.id)])

    def test_nested_child_page_null_is_resolved(self):
        # A page=NULL child inside a VISIBLE container must still resolve (it is
        # owned by the page via its ancestor chain), not be dropped.
        container = Element.objects.create(page=self.page, name="box", element_type="container")
        child = Element.objects.create(name="c", element_type="text", parent_element=container)
        child.visibility_rules.add(_group_with(_rule("user_logged_in", True, operator="is_true")))
        user = get_user_model().objects.create_user(username="v2", password="x")
        self.client.force_login(user)
        resp = self._post({"page_id": self.page.id, "element_ids": [child.id]})
        self.assertIsNotNone(resp.json()["elements"][str(child.id)])

    def test_nested_child_of_other_page_is_rejected(self):
        # IDOR: a page=NULL child owned by ANOTHER page must not be rendered here.
        container = Element.objects.create(
            page=self.other_page, name="box", element_type="container"
        )
        child = Element.objects.create(name="c", element_type="text", parent_element=container)
        resp = self._post({"page_id": self.page.id, "element_ids": [child.id]})
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn(str(child.id), resp.json()["elements"])

    def test_requires_auth_page_blocks_anonymous(self):
        self.page.requires_auth = True
        self.page.save()
        resp = self._post({"page_id": self.page.id, "element_ids": [1]})
        self.assertEqual(resp.status_code, 404)


class PreviewAsMarketTests(TestCase):
    def setUp(self):
        cache.clear()
        from core.models import SiteSettings

        SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                "admin_email": "admin@example.com",
                "default_currency": "USD",
                "enable_multi_warehouse": False,
            },
        )
        SalesRegion.objects.create(name="Global", code="GLB", default_currency="USD", priority=100)
        SalesRegion.objects.create(
            name="New Zealand",
            code="NZ",
            slug="nz",
            default_currency="NZD",
            countries=["NZ"],
            priority=50,
        )
        self.page = Page.objects.create(
            title="P", slug="preview-me", page_type="page", status="published"
        )
        el = Element.objects.create(
            page=self.page,
            name="nz-block",
            element_type="text",
            content={"text": "NZONLYMARKER"},
        )
        el.visibility_rules.add(_group_with(_rule("geo_region", "NZ")))
        # Superuser: page_preview is an admin URL gated by role-based admin access
        # (deny-by-default), which superusers bypass.
        self.staff = get_user_model().objects.create_superuser(
            username="s", password="x", email="s@example.com"
        )
        self.client.force_login(self.staff)

    def _preview_url(self, market=None):
        url = reverse("page_builder_admin:page_preview", kwargs={"slug": self.page.slug})
        return f"{url}?preview_market={market}" if market else url

    def test_nz_element_shown_when_previewing_nz_market(self):
        resp = self.client.get(self._preview_url("nz"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "NZONLYMARKER")

    def test_nz_element_hidden_in_default_market_preview(self):
        resp = self.client.get(self._preview_url())
        self.assertEqual(resp.status_code, 200)
        self.assertNotContains(resp, "NZONLYMARKER")


class DefaultMarketDeterminismTests(TestCase):
    """The shell's region is URL-authoritative (market prefix, else default) — it
    must NOT vary by the visitor's cookie/GeoIP region, or the default-URL cache
    would serve one region's content to another (codex P1)."""

    def setUp(self):
        cache.clear()
        self.factory = RequestFactory()
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
        self.page = Page.objects.create(
            title="P", slug="determinism", page_type="page", status="published"
        )
        self.el = Element.objects.create(page=self.page, name="nz-only", element_type="text")
        self.el.visibility_rules.add(_group_with(_rule("geo_region", "NZ")))

    def _req(self, market_slug, cookie_region):
        req = self.factory.get("/")
        req.user = AnonymousUser()
        req.session = {}
        req.market_slug = market_slug
        req.sales_region = self.nz if cookie_region == "NZ" else self.default
        return req

    def test_default_url_ignores_cookie_region_for_shell(self):
        # NZ-cookie visitor on the DEFAULT (unprefixed) URL: the shell renders the
        # default region, so the NZ-only block is hidden — deterministic + cacheable.
        self.assertEqual(self.el.shell_visibility(self._req(None, "NZ")), "hide")

    def test_market_url_shows_market_content(self):
        self.assertEqual(self.el.shell_visibility(self._req("nz", "NZ")), "show")


class VisibilitySummaryTests(TestCase):
    """Canvas chip indicator: compact, de-duplicated labels for gated elements."""

    def test_short_labels_are_compact(self):
        self.assertEqual(_rule("geo_region", "nz").short_label(), "NZ")
        self.assertEqual(
            str(_rule("user_logged_in", True, operator="is_true").short_label()), "Members"
        )
        self.assertEqual(
            _rule("cart_value", 50, operator="greater_than").short_label(), "Cart ≥ 50"
        )
        self.assertEqual(_rule("selected_currency", "nzd").short_label(), "NZD")

    def test_element_summary_dedupes_and_lists_rules(self):
        page = Page.objects.create(title="P", slug="vsum", page_type="page", status="published")
        el = Element.objects.create(page=page, name="e", element_type="text")
        el.visibility_rules.add(_group_with(_rule("geo_region", "nz")))
        g2 = RuleGroup.objects.create(name="g2", logic_operator="OR")
        RuleGroupMember.objects.create(
            rule_group=g2, rule=_rule("user_logged_in", True, operator="is_true"), order=0
        )
        RuleGroupMember.objects.create(
            rule_group=g2,
            rule=_rule("geo_region", "nz"),
            order=1,  # duplicate label
        )
        el.visibility_rules.add(g2)
        summary = [str(x) for x in el.visibility_summary()]
        self.assertEqual(summary.count("NZ"), 1)  # deduped across groups
        self.assertIn("Members", summary)

    def test_element_without_rules_has_empty_summary(self):
        page = Page.objects.create(title="P", slug="vsum2", page_type="page", status="published")
        el = Element.objects.create(page=page, name="e", element_type="text")
        self.assertEqual(el.visibility_summary(), [])

    def test_canvas_partial_emits_chip_html(self):
        from django.template.loader import render_to_string

        page = Page.objects.create(title="P", slug="chip", page_type="page", status="published")
        el = Element.objects.create(
            page=page, name="e", element_type="text", content={"text": "hi"}
        )
        el.visibility_rules.add(_group_with(_rule("geo_region", "nz")))
        html = render_to_string(
            "page_builder/partials/visual_builder_element.html",
            {"element": el, "is_visual_builder": True},
        )
        self.assertIn("element-visibility-chips", html)
        self.assertIn("NZ", html)

    def test_short_labels_handle_builder_dict_values(self):
        # The rule builder persists values as {"value": n} / {"values": [...]} /
        # {"min":a,"max":b} — chips must show the real gate, not "…".
        self.assertEqual(
            _rule("cart_value", {"value": 50}, operator="greater_than").short_label(), "Cart ≥ 50"
        )
        self.assertEqual(
            _rule("user_group", {"values": ["vip", "gold"]}, operator="in_list").short_label(),
            "vip, gold",
        )
        self.assertEqual(
            _rule("cart_value", {"min": 10, "max": 20}, operator="between").short_label(),
            "Cart ∈ 10–20",
        )


class PreviewVisitorStateTests(TestCase):
    """Preview renders deferred-gated content for a simulated visitor state."""

    def setUp(self):
        cache.clear()
        from core.models import SiteSettings

        SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                "admin_email": "admin@example.com",
                "default_currency": "USD",
                "enable_multi_warehouse": False,
            },
        )
        self.page = Page.objects.create(
            title="P", slug="pv-state", page_type="page", status="published"
        )
        self.member_el = Element.objects.create(
            page=self.page, name="m", element_type="text", content={"text": "MEMBERONLY"}
        )
        self.member_el.visibility_rules.add(
            _group_with(_rule("user_logged_in", True, operator="is_true"))
        )
        self.cart_el = Element.objects.create(
            page=self.page, name="c", element_type="text", content={"text": "BIGCART"}
        )
        self.cart_el.visibility_rules.add(
            _group_with(_rule("cart_value", 50, operator="greater_than"))
        )
        self.staff = get_user_model().objects.create_superuser("pv", "pv@example.com", "x")
        self.client.force_login(self.staff)

    def _url(self, **params):
        from urllib.parse import urlencode

        base = reverse("page_builder_admin:page_preview", kwargs={"slug": self.page.slug})
        return f"{base}?{urlencode(params)}" if params else base

    def test_member_content_shown_for_member(self):
        resp = self.client.get(self._url(preview_auth="member"))
        self.assertContains(resp, "MEMBERONLY")

    def test_member_content_hidden_for_guest(self):
        resp = self.client.get(self._url(preview_auth="guest"))
        self.assertNotContains(resp, "MEMBERONLY")

    def test_cart_gated_shown_with_high_cart(self):
        resp = self.client.get(self._url(preview_auth="guest", preview_cart="100"))
        self.assertContains(resp, "BIGCART")

    def test_cart_gated_hidden_with_low_cart(self):
        resp = self.client.get(self._url(preview_auth="guest", preview_cart="10"))
        self.assertNotContains(resp, "BIGCART")

    def test_guest_clears_group_context(self):
        # Even though the previewing staff user is in the "vip" group, a
        # group-gated element must be HIDDEN when previewing as guest (the whole
        # user context is reset, not just is_authenticated).
        from django.contrib.auth.models import Group

        self.staff.groups.add(Group.objects.create(name="vip"))
        el = Element.objects.create(
            page=self.page, name="vip", element_type="text", content={"text": "VIPBLOCK"}
        )
        el.visibility_rules.add(
            _group_with(_rule("user_group", {"values": ["vip"]}, operator="in_list"))
        )
        self.assertContains(self.client.get(self._url(preview_auth="member")), "VIPBLOCK")
        self.assertNotContains(self.client.get(self._url(preview_auth="guest")), "VIPBLOCK")


class PersonalizeRouteContextTests(TestCase):
    """The personalize endpoint rebuilds home/category/product page context so
    deferred elements on those pages render with the data they need."""

    def setUp(self):
        cache.clear()
        self.factory = RequestFactory()

    def _req(self):
        req = self.factory.get("/")
        req.user = AnonymousUser()
        req.session = {}
        return req

    def test_category_route_context_rebuilt(self):
        from catalog.models import Category
        from page_builder.services.visibility_service import _build_route_context

        cat = Category.objects.create(name="Shoes", slug="shoes", is_active=True)
        page = Page.objects.create(
            title="Cat", slug="cat-tpl", page_type="category", status="published"
        )
        ctx = _build_route_context(page, self._req(), category_slug="shoes")
        self.assertEqual(ctx.get("category"), cat)
        self.assertIn("products", ctx)

    def test_missing_category_returns_empty_context(self):
        from page_builder.services.visibility_service import _build_route_context

        page = Page.objects.create(
            title="Cat", slug="cat-tpl2", page_type="category", status="published"
        )
        self.assertEqual(_build_route_context(page, self._req(), category_slug="nope"), {})

    def test_home_route_context_rebuilt(self):
        from page_builder.services.visibility_service import _build_route_context

        page = Page.objects.create(title="H", slug="home-rc", page_type="home", status="published")
        ctx = _build_route_context(page, self._req())
        self.assertIn("featured_products", ctx)
        self.assertIn("categories", ctx)
