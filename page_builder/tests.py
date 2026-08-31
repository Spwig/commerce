"""Regression tests for page_builder F821 bugs.

- page_builder/api/translation_endpoints.py:40 called
  `health.get_degradation_warnings()` without defining `health`.
- page_builder/api/translation_endpoints.py:431 and
  page_builder/translation_utils.py:369 instantiated
  TranslationServiceHealth which never existed.
- page_builder/api_views.py referenced the deleted PageSection model
  inside a `RemovedSectionAPIView` class that was never removed.
"""

import inspect
from unittest.mock import patch

import pytest
from django.test import Client, SimpleTestCase


class TranslationServiceHealthTest(SimpleTestCase):
    """The wrapper class must exist and expose the four methods callers
    were assuming: get_health_status, should_schedule_translation,
    estimate_translation_time, get_degradation_warnings. The first was
    added after an initial code review noted that
    page_builder/middleware.py:174 called it but the wrapper did not
    define it — the surrounding try/except swallowed the AttributeError,
    silently disabling middleware-level health monitoring."""

    def test_wrapper_class_exists(self):
        from page_builder.translation_utils import TranslationServiceHealth

        h = TranslationServiceHealth()
        self.assertTrue(callable(h.get_health_status))
        self.assertTrue(callable(h.should_schedule_translation))
        self.assertTrue(callable(h.estimate_translation_time))
        self.assertTrue(callable(h.get_degradation_warnings))

    def test_middleware_health_call_resolves(self):
        """Simulate the middleware call and assert it returns real
        health data, not the swallowed-AttributeError fallback."""
        from unittest.mock import patch

        from page_builder.translation_utils import TranslationServiceHealth

        with patch("page_builder.translation_utils.get_translation_health_status") as m:
            m.return_value = {
                "available": True,
                "status": "ok",
                "message": "Translation service is operational",
            }
            status = TranslationServiceHealth().get_health_status()

        self.assertTrue(status["available"])
        self.assertEqual(status["status"], "ok")

    def test_degradation_warnings_returns_list_when_available(self):
        from page_builder.translation_utils import TranslationServiceHealth

        with patch("page_builder.translation_utils.get_translation_health_status") as m:
            m.return_value = {"available": True, "status": "ok", "message": ""}
            self.assertEqual(TranslationServiceHealth().get_degradation_warnings(), [])

    def test_degradation_warnings_returns_message_when_unavailable(self):
        from page_builder.translation_utils import TranslationServiceHealth

        with patch("page_builder.translation_utils.get_translation_health_status") as m:
            m.return_value = {
                "available": False,
                "status": "offline",
                "message": "Translation service is not responding",
            }
            warnings = TranslationServiceHealth().get_degradation_warnings()
            self.assertEqual(warnings, ["Translation service is not responding"])


class RemovedSectionAPIViewGoneTest(SimpleTestCase):
    """The dead RemovedSectionAPIView class referenced a deleted model.
    It has been removed entirely."""

    def test_class_is_gone(self):
        from page_builder import api_views

        self.assertFalse(hasattr(api_views, "RemovedSectionAPIView"))
        self.assertFalse(hasattr(api_views, "PageSection"))


class TranslationHealthEndpointHealthLocalTest(SimpleTestCase):
    """translation_health() previously referenced `health` without a
    local assignment. Assert the fix wires it up before use."""

    def test_translation_health_endpoint_source_defines_health(self):

        from page_builder.api.translation_endpoints import translation_health

        source = inspect.getsource(translation_health)
        self.assertIn("health = TranslationServiceHealth()", source)


# ---------------------------------------------------------------------------
# Conditional element-CSS loading
# ---------------------------------------------------------------------------
#
# product_grid used to list all six layout stylesheets in css_files, so
# PageView._collect_element_css unioned every variant into the page <head>
# even when a single grid instance rendered one layout. The new mechanism
# keeps only the base sheet in css_files and resolves the variant sheet from
# a `conditional_css_files` rule keyed on the element's `layout` content
# property. These tests pin that per-instance resolution so a regression that
# re-introduces the union (or drops the variant entirely) is caught.

# Absolute file strings copied from the real product_grid config.json so the
# assertions fail loudly if either the config or the collector drifts.
_PG_BASE = "page_builder/css/elements/product-grid.css"
_PG_VARIANTS = {
    "grid": "page_builder/css/category-grid.css",
    "list": "page_builder/css/category-list.css",
    "carousel": "page_builder/css/category-carousel.css",
    "masonry": "page_builder/css/category-masonry.css",
    "featured": "page_builder/css/category-featured.css",
}
_HEADING_BASE = "page_builder/css/elements/heading.css"


def _snapshot_registry(reg):
    """Capture the process-global ElementRegistry's mutable state so a test
    that calls reload() can restore it afterwards. discover_elements() clears
    the `_elements`/`_categories` dicts in place, so shallow copies suffice.

    The cache entry is captured too: reload() deletes and rewrites
    REGISTRY_CACHE_KEY with a DB-less registry (the custom-element query is
    forbidden under SimpleTestCase). Restoring only the in-memory fields would
    leave that poisoned cache behind — a later lookup with `_loaded=False`
    reads it back and silently loses every DB-backed custom element."""
    from django.core.cache import cache

    from page_builder.element_registry import REGISTRY_CACHE_KEY

    return {
        "elements": dict(reg._elements),
        "categories": {k: list(v) for k, v in reg._categories.items()},
        "loaded": reg._loaded,
        "base_properties": reg._base_properties,
        "cache": cache.get(REGISTRY_CACHE_KEY),
    }


def _restore_registry(reg, snapshot):
    """Restore a snapshot taken by _snapshot_registry so the global registry
    (including its DB-backed custom elements) is left exactly as it was."""
    from django.core.cache import cache

    from page_builder.element_registry import REGISTRY_CACHE_KEY

    reg._elements = dict(snapshot["elements"])
    reg._categories = {k: list(v) for k, v in snapshot["categories"].items()}
    reg._loaded = snapshot["loaded"]
    reg._base_properties = snapshot["base_properties"]

    # Undo reload()'s rewrite of the versioned cache key. If there was no entry
    # before, drop the poisoned one so the next lookup re-discovers from a
    # DB-capable context; otherwise put the original entry back verbatim.
    cached = snapshot["cache"]
    if cached is None:
        cache.delete(REGISTRY_CACHE_KEY)
    else:
        cache.set(REGISTRY_CACHE_KEY, cached, timeout=3600)


class _FakeChildManager:
    """Stand-in for Element.child_elements so the collector's
    `.filter(is_active=True).exists()` recursion guard short-circuits."""

    def filter(self, *args, **kwargs):
        return self

    def exists(self):
        return False


class _FakeElement:
    """Lightweight element the collector can walk without touching the DB.

    Exposes exactly the surface PageView._collect_element_css reads:
    is_active, element_type, content, and child_elements."""

    def __init__(self, element_type, content=None, is_active=True):
        self.element_type = element_type
        self.content = {} if content is None else content
        self.is_active = is_active
        self.child_elements = _FakeChildManager()


class ConditionalElementCssTest(SimpleTestCase):
    """PageView._collect_element_css must add the base css_files plus only the
    single variant sheet that matches each element instance's layout."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Force a fresh read from disk so a stale in-process/cache registry
        # (possible under --reuse-db or a long-lived worker) cannot mask the
        # new conditional_css_files config. reload() touches the custom-element
        # table via _discover_custom_elements; that query is forbidden under
        # SimpleTestCase but is swallowed by the collector's broad except, so
        # filesystem elements (product_grid, heading) still register.
        #
        # reload() mutates the process-global singleton and marks it loaded with
        # only filesystem elements, which would silently strip DB-backed custom
        # elements from every later test. Snapshot the singleton's state so
        # tearDownClass can restore it and leave the global registry untouched.
        from page_builder.element_registry import get_registry

        cls._registry_snapshot = _snapshot_registry(get_registry())
        get_registry().reload()

    @classmethod
    def tearDownClass(cls):
        from page_builder.element_registry import get_registry

        _restore_registry(get_registry(), cls._registry_snapshot)
        super().tearDownClass()

    def _collect(self, *elements):
        from page_builder.views import PageView

        # _collect_element_css only uses `self` to reach the module-level
        # registry, so a bare instance is sufficient — no request needed.
        return set(PageView()._collect_element_css(list(elements)))

    def test_registry_exposes_the_conditional_rule(self):
        """Guard the fixtures: the real product_grid config must carry the
        base sheet in css_files and the full five-layout conditional map."""
        from page_builder.element_registry import get_registry

        cfg = get_registry().get_element("product_grid")
        self.assertIsNotNone(cfg, "product_grid element should be registered")
        self.assertEqual(cfg.css_files, [_PG_BASE])
        self.assertEqual(len(cfg.conditional_css_files), 1)
        rule = cfg.conditional_css_files[0]
        self.assertEqual(rule["property"], "layout")
        self.assertEqual(rule["default"], "grid")
        self.assertEqual(rule["map"], _PG_VARIANTS)

    def test_list_layout_loads_base_plus_only_list_variant(self):
        """Case 1: a list-layout grid yields base + category-list.css and
        none of grid/carousel/masonry/featured."""
        result = self._collect(_FakeElement("product_grid", {"layout": "list"}))

        self.assertEqual(result, {_PG_BASE, _PG_VARIANTS["list"]})
        for other in ("grid", "carousel", "masonry", "featured"):
            self.assertNotIn(_PG_VARIANTS[other], result)

    def test_each_layout_maps_to_its_own_single_variant(self):
        """Case 2: every layout resolves to exactly base + its own sheet, and
        no sheet belonging to a different layout leaks in."""
        for layout, variant in _PG_VARIANTS.items():
            with self.subTest(layout=layout):
                result = self._collect(_FakeElement("product_grid", {"layout": layout}))
                self.assertEqual(result, {_PG_BASE, variant})
                for other_layout, other_variant in _PG_VARIANTS.items():
                    if other_layout != layout:
                        self.assertNotIn(other_variant, result)

    def test_unset_layout_falls_back_to_default_grid(self):
        """Case 3: content without a layout key resolves to the declared
        default ("grid") → category-grid.css."""
        result = self._collect(_FakeElement("product_grid", {}))

        self.assertEqual(result, {_PG_BASE, _PG_VARIANTS["grid"]})

    def test_unknown_layout_loads_base_only_no_broken_variant(self):
        """Case 4: a bogus layout value has no map entry, so only the base
        sheet loads — never a nonexistent variant link."""
        result = self._collect(_FakeElement("product_grid", {"layout": "definitely-not-a-layout"}))

        self.assertEqual(result, {_PG_BASE})
        for variant in _PG_VARIANTS.values():
            self.assertNotIn(variant, result)

    def test_element_without_conditional_key_defaults_to_empty_list(self):
        """Case 5 (backward-compat): an element whose config declares no
        conditional_css_files gets an empty list, and its css_files behavior
        is unchanged — no variant sheets are ever added."""
        from page_builder.element_registry import get_registry

        heading_cfg = get_registry().get_element("heading")
        self.assertIsNotNone(heading_cfg, "heading element should be registered")
        self.assertEqual(heading_cfg.conditional_css_files, [])
        self.assertEqual(heading_cfg.css_files, [_HEADING_BASE])

        # Collecting for a heading instance yields exactly its base sheet —
        # a `layout` value in content must not conjure any variant.
        result = self._collect(_FakeElement("heading", {"layout": "list"}))
        self.assertEqual(result, {_HEADING_BASE})

    def test_default_construction_yields_empty_conditional_list(self):
        """The ElementConfig contract itself: a config dict with no
        conditional_css_files key defaults the attribute to []."""
        from page_builder.element_registry import ElementConfig

        cfg = ElementConfig("dummy", {"css_files": ["x.css"]}, base_path=None)
        self.assertEqual(cfg.conditional_css_files, [])
        self.assertEqual(cfg.css_files, ["x.css"])


# ---------------------------------------------------------------------------
# Manifest resolution of element script URLs
# ---------------------------------------------------------------------------
#
# Element configs declare `scripts` as raw `/static/...` paths, which bypass
# the staticfiles manifest (ManifestStaticFilesStorage). PageView now routes
# every collected element script through `_manifest_static_url`, which strips
# STATIC_URL and re-resolves the relative path via django.templatetags.static
# .static() — the same machinery `{% static %}` uses. The payoff: a script
# loaded both as a global `{% static %}` (e.g. search-autocomplete.js in
# base.html) and as a raw element script resolves to the IDENTICAL hashed URL,
# so the browser dedupes them instead of fetching two byte-identical files.

# The search autocomplete script is the canonical dual-loaded file: global in
# base.html AND declared as a raw element script. Its relative (post-STATIC_URL)
# path is what {% static %} is called with.
_SEARCH_JS_REL = "search/js/search-autocomplete.js"
# Real raw script path declared by the product_grid element config.json.
_PG_SCRIPT_RAW = "/static/page_builder/js/elements/product-grid.js"


class ManifestStaticUrlTest(SimpleTestCase):
    """PageView._manifest_static_url must resolve `/static/`-prefixed element
    script URLs through the same manifest machinery as `{% static %}`, while
    leaving external / non-static URLs untouched."""

    def _static_url(self):
        from django.conf import settings

        return settings.STATIC_URL or "/static/"

    def test_static_path_resolves_identically_to_static_templatetag(self):
        """A raw `/static/<rel>` element script and the `{% static %}` form of
        the same file must produce the byte-identical URL — that identity is
        what lets the browser dedupe the globally-loaded search script against
        the element-loaded copy."""
        from django.templatetags.static import static

        from page_builder.views import PageView

        raw = self._static_url() + _SEARCH_JS_REL
        resolved = PageView._manifest_static_url(raw)

        # The important, non-tautological assertion: element-script resolution
        # and the {% static %} tag land on the same URL for the same file.
        self.assertEqual(resolved, static(_SEARCH_JS_REL))

    def test_external_and_protocol_relative_urls_pass_through_unchanged(self):
        """Absolute (https://) and protocol-relative (//) URLs are not static
        assets and must be returned verbatim — never fed to static()."""
        from page_builder.views import PageView

        external = "https://cdn.example.com/x.js"
        protocol_relative = "//cdn.example.com/x.js"

        self.assertEqual(PageView._manifest_static_url(external), external)
        self.assertEqual(PageView._manifest_static_url(protocol_relative), protocol_relative)

    def test_static_path_without_manifest_entry_does_not_raise(self):
        """A `/static/`-prefixed path with no matching file must resolve
        without raising under non-strict (dev / default) storage, which returns
        the unhashed path. Kept robust to both hashed and unhashed backends by
        asserting a non-empty string that either starts with STATIC_URL or
        carries the relative name — never an exact hash."""
        from page_builder.views import PageView

        static_url = self._static_url()
        rel = "page_builder/js/elements/does-not-exist-xyz.js"
        raw = static_url + rel

        resolved = PageView._manifest_static_url(raw)

        self.assertIsInstance(resolved, str)
        self.assertTrue(resolved, "resolver must not return an empty string")
        self.assertTrue(
            resolved.startswith(static_url) or "does-not-exist-xyz" in resolved,
            f"unexpected resolution: {resolved!r}",
        )


class CollectElementScriptsManifestTest(SimpleTestCase):
    """PageView._collect_element_scripts must return element script URLs routed
    through _manifest_static_url, not the raw `/static/...` config paths."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Force a fresh disk read so a stale registry (possible under
        # --reuse-db / a long-lived worker) cannot mask the real product_grid
        # `scripts` config. Mirrors ConditionalElementCssTest.setUpClass,
        # including the snapshot/restore that keeps the process-global registry
        # (and its DB-backed custom elements) intact for later tests.
        from page_builder.element_registry import get_registry

        cls._registry_snapshot = _snapshot_registry(get_registry())
        get_registry().reload()

    @classmethod
    def tearDownClass(cls):
        from page_builder.element_registry import get_registry

        _restore_registry(get_registry(), cls._registry_snapshot)
        super().tearDownClass()

    def _collect(self, *elements):
        from page_builder.views import PageView

        return PageView()._collect_element_scripts(list(elements))

    def test_registry_exposes_the_product_grid_script(self):
        """Guard the fixture: the real product_grid config must declare the raw
        element script path the collector is expected to resolve."""
        from page_builder.element_registry import get_registry

        cfg = get_registry().get_element("product_grid")
        self.assertIsNotNone(cfg, "product_grid element should be registered")
        self.assertIn(_PG_SCRIPT_RAW, cfg.scripts)

    def test_collected_script_is_manifest_resolved_not_raw(self):
        """A product_grid element's script comes back resolved through
        _manifest_static_url — equal to the resolver's output for the raw path,
        which under manifest storage is the hashed form (never the raw literal
        when hashing is active)."""
        from page_builder.views import PageView

        result = self._collect(_FakeElement("product_grid", {"layout": "grid"}))

        expected = PageView._manifest_static_url(_PG_SCRIPT_RAW)
        self.assertEqual(result, [expected])
        # Cross-check the resolution actually went through the manifest
        # machinery: it matches the {% static %} form of the same relative path.
        from django.templatetags.static import static

        self.assertEqual(result[0], static("page_builder/js/elements/product-grid.js"))


# ---------------------------------------------------------------------------
# Conditional product-card asset suppression (cart / checkout denylist)
# ---------------------------------------------------------------------------
#
# base.html loads the product-card interaction script, the quick-view script,
# and the quick-view modal by DEFAULT. This is a safe denylist: only surfaces
# that never render product cards opt out by passing
# `suppress_product_card_assets=True`. cart_view and checkout_view do so; every
# product-card surface (home, listing, product) must keep loading them so a
# regression that either (a) drops the assets from a card surface or (b) stops
# suppressing them on cart/checkout is caught.
#
# These use pytest-style tests (not SimpleTestCase) on purpose: the root
# conftest's autouse `_seed_site_settings` (CurrencyMiddleware needs the
# SiteSettings singleton or every request 500s) and
# `_bypass_license_acceptance_middleware` fixtures only run for pytest-collected
# tests, NOT unittest.TestCase methods. A TestCase here would 500 / redirect.

# The three tokens base.html emits only when the assets are NOT suppressed.
_PRODUCT_CARD_JS = "js/product-card"
_QUICK_VIEW_JS = "js/quick-view"
_QUICK_VIEW_MODAL_ID = "product-quick-view"


@pytest.mark.django_db
class TestSuppressProductCardAssets:
    """base.html gates the product-card JS + quick-view modal on
    `suppress_product_card_assets`. Cart/checkout suppress; card surfaces load."""

    def _client(self):
        # HTTP_HOST=localhost matches ALLOWED_HOSTS in the test settings and the
        # Site framework's SITE_ID=1 domain expectations.
        return Client(HTTP_HOST="localhost")

    def test_cart_page_omits_product_card_and_quick_view_assets(self):
        """(1) GET /en/cart/ renders 200 and its HTML carries NONE of the
        product-card script, quick-view script, or quick-view modal id."""
        response = self._client().get("/en/cart/")

        assert response.status_code == 200, response.status_code
        html = response.content.decode()
        assert _PRODUCT_CARD_JS not in html
        assert _QUICK_VIEW_JS not in html
        assert _QUICK_VIEW_MODAL_ID not in html

    def test_cart_context_sets_suppress_flag_true(self):
        """(3) Context-level pin: the cart response context explicitly carries
        suppress_product_card_assets == True, independent of DB/template state —
        so the test fails loudly if cart_view stops passing the flag even if the
        HTML happened to omit the tokens for an unrelated reason."""
        response = self._client().get("/en/cart/")

        assert response.status_code == 200, response.status_code
        assert response.context["suppress_product_card_assets"] is True

    def test_home_surface_loads_product_card_and_quick_view_assets(self):
        """(2) GET /en/ (a product-card surface — page-builder home or the
        simple_home fallback, both extend base.html without the flag) renders
        200 and its HTML DOES carry all three tokens. base.html emits them on
        any non-suppressing page, so this holds whether or not the seeded DB has
        featured products to render."""
        response = self._client().get("/en/")

        assert response.status_code == 200, response.status_code
        html = response.content.decode()
        assert _PRODUCT_CARD_JS in html
        assert _QUICK_VIEW_JS in html
        assert _QUICK_VIEW_MODAL_ID in html

    def test_products_listing_surface_loads_the_assets(self):
        """(2, cross-check) The all-products listing is unambiguously a
        product-card surface. It must also load the assets. If home in this DB
        resolves to something without cards, the listing still proves a genuine
        card surface keeps them."""
        response = self._client().get("/en/products/")

        assert response.status_code == 200, response.status_code
        html = response.content.decode()
        assert _PRODUCT_CARD_JS in html
        assert _QUICK_VIEW_JS in html
        assert _QUICK_VIEW_MODAL_ID in html

    def test_checkout_view_source_sets_suppress_flag(self):
        """(checkout, source-level) checkout_view redirects to the cart when the
        cart is empty, so an HTTP-level assertion would need a seeded cart with
        items. Instead pin the flag directly in the view source (same technique
        the F821 health-endpoint regression test uses above): checkout_view must
        initialise its context with suppress_product_card_assets=True."""
        from page_builder.views import checkout_view

        source = inspect.getsource(checkout_view)
        assert '"suppress_product_card_assets": True' in source
