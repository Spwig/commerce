"""Tests for the multi-market URL layer: MarketMiddleware, region pinning,
market-slug helpers, and the {% market_url %} template tag.
"""

from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.template import Context, Template
from django.test import RequestFactory, TestCase
from django.urls import get_script_prefix, set_script_prefix

from catalog.middleware import (
    MarketMiddleware,
    RegionDetectionMiddleware,
    get_default_region,
    get_market_slugs,
    get_region_for_market_slug,
)
from catalog.models import SalesRegion


class MarketMiddlewareTests(TestCase):
    def setUp(self):
        cache.clear()  # signal on_commit doesn't fire inside TestCase; read fresh
        self.factory = RequestFactory()
        self.default = SalesRegion.objects.create(
            name="Global", code="GLB", default_currency="USD", priority=100
        )
        self.nz = SalesRegion.objects.create(
            name="New Zealand", code="NZ", slug="nz", default_currency="NZD", priority=50
        )

    def tearDown(self):
        set_script_prefix("/")  # reset thread-local so tests don't bleed

    def _run(self, path):
        request = self.factory.get(path)
        captured = {}

        def get_response(req):
            captured["script_prefix"] = get_script_prefix()
            return "ok"

        MarketMiddleware(get_response)(request)
        return request, captured

    def test_market_prefix_is_stripped_and_recorded(self):
        request, captured = self._run("/nz/en/products/")
        self.assertEqual(request.market_slug, "nz")
        self.assertEqual(request.market_prefix, "/nz")
        self.assertEqual(request.path_info, "/en/products/")
        self.assertEqual(request.META["PATH_INFO"], "/en/products/")

    def test_market_folded_into_script_prefix_for_reverse(self):
        _, captured = self._run("/nz/en/products/")
        # reverse()/{% url %} inside the request keep the market prefix
        self.assertEqual(captured["script_prefix"], "/nz/")

    def test_default_market_has_no_prefix(self):
        request, captured = self._run("/en/products/")
        self.assertIsNone(request.market_slug)
        self.assertEqual(request.market_prefix, "")
        self.assertEqual(request.path_info, "/en/products/")
        self.assertEqual(captured["script_prefix"], "/")

    def test_language_segment_is_never_treated_as_market(self):
        # "en" is a language code, not a market slug — must not be stripped
        request, _ = self._run("/en/")
        self.assertIsNone(request.market_slug)
        self.assertEqual(request.path_info, "/en/")

    def test_unknown_first_segment_untouched(self):
        request, _ = self._run("/some-page-slug/")
        self.assertIsNone(request.market_slug)
        self.assertEqual(request.path_info, "/some-page-slug/")

    def test_request_market_resolves_region(self):
        request, _ = self._run("/nz/en/")
        self.assertEqual(request.market.pk, self.nz.pk)

    def test_request_market_defaults_to_highest_priority(self):
        request, _ = self._run("/en/")
        self.assertEqual(request.market.pk, self.default.pk)

    def test_bare_market_path_normalises_to_root(self):
        request, _ = self._run("/nz")
        self.assertEqual(request.market_slug, "nz")
        self.assertEqual(request.path_info, "/")


class MarketRegionPinningTests(TestCase):
    def setUp(self):
        cache.clear()
        self.factory = RequestFactory()
        SalesRegion.objects.create(name="Global", code="GLB", default_currency="USD", priority=100)
        self.nz = SalesRegion.objects.create(
            name="New Zealand", code="NZ", slug="nz", default_currency="NZD", priority=50
        )
        self.sg = SalesRegion.objects.create(
            name="Singapore", code="SG", slug="sg", default_currency="SGD", priority=40
        )

    def test_url_market_overrides_cookie_region(self):
        request = self.factory.get("/nz/en/")
        request.market_slug = "nz"  # as MarketMiddleware would set it
        request.COOKIES["preferred_region"] = "SG"  # conflicting user override

        RegionDetectionMiddleware(lambda r: HttpResponse("ok"))(request)
        self.assertEqual(request.sales_region.pk, self.nz.pk)

    def test_no_market_falls_back_to_detection(self):
        request = self.factory.get("/en/")
        request.market_slug = None
        request.COOKIES["preferred_region"] = "SG"

        RegionDetectionMiddleware(lambda r: HttpResponse("ok"))(request)
        self.assertEqual(request.sales_region.pk, self.sg.pk)


class MarketSlugHelperTests(TestCase):
    def setUp(self):
        cache.clear()
        self.nz = SalesRegion.objects.create(
            name="New Zealand", code="NZ", slug="nz", default_currency="NZD", priority=50
        )
        self.inactive = SalesRegion.objects.create(
            name="Old", code="OLD", slug="old", default_currency="USD", is_active=False
        )
        SalesRegion.objects.create(name="Global", code="GLB", default_currency="USD", priority=100)

    def test_get_market_slugs_only_active_with_slug(self):
        self.assertEqual(get_market_slugs(), {"nz"})

    def test_get_region_for_market_slug(self):
        self.assertEqual(get_region_for_market_slug("nz").pk, self.nz.pk)
        self.assertEqual(get_region_for_market_slug("NZ").pk, self.nz.pk)  # case-insensitive
        self.assertIsNone(get_region_for_market_slug("old"))  # inactive
        self.assertIsNone(get_region_for_market_slug(""))

    def test_get_default_region_is_highest_priority(self):
        self.assertEqual(get_default_region().code, "GLB")

    def test_default_region_slug_excluded_from_markets(self):
        # The default (highest-priority) region is served unprefixed only; a slug
        # on it must NOT create a second, prefixed URL for the same market.
        default = SalesRegion.objects.get(code="GLB")
        default.slug = "global"
        default.save()
        cache.clear()
        slugs = get_market_slugs()
        self.assertNotIn("global", slugs)
        self.assertIn("nz", slugs)


class SalesRegionSlugValidationTests(TestCase):
    def _region(self, **kw):
        defaults = {"name": "R", "code": "R", "default_currency": "USD", "countries": ["NZ"]}
        defaults.update(kw)
        return SalesRegion(**defaults)

    def test_language_code_slug_rejected(self):
        with self.assertRaises(ValidationError) as cm:
            self._region(name="Bad", code="BAD", slug="en").full_clean()
        self.assertIn("slug", cm.exception.message_dict)

    def test_reserved_route_slug_rejected(self):
        with self.assertRaises(ValidationError) as cm:
            self._region(name="Bad2", code="BAD2", slug="api").full_clean()
        self.assertIn("slug", cm.exception.message_dict)

    def test_top_level_route_slug_rejected(self):
        # A real top-level route like /pos/ must not be usable as a market slug.
        with self.assertRaises(ValidationError) as cm:
            self._region(name="Pos", code="POS", slug="pos").full_clean()
        self.assertIn("slug", cm.exception.message_dict)

    def test_valid_slug_is_lowercased(self):
        region = self._region(name="NZ", code="NZ", slug="NZ", default_currency="NZD")
        region.full_clean()
        self.assertEqual(region.slug, "nz")


class MarketUrlTagTests(TestCase):
    def setUp(self):
        cache.clear()
        self.factory = RequestFactory()

    def tearDown(self):
        set_script_prefix("/")

    def _render(self, template_str, request):
        ctx = Context({"request": request})
        return Template("{% load market_tags %}" + template_str).render(ctx)

    def test_market_url_builds_cross_market_link(self):
        # Simulate being on the /nz/ market
        request = self.factory.get("/nz/en/admin/")
        request.market_prefix = "/nz"
        request.market_slug = "nz"
        set_script_prefix("/nz/")

        out = self._render("{% market_url 'sg' 'admin:index' %}", request)
        self.assertEqual(out, "/sg/en/admin/")

    def test_market_url_default_market_has_no_prefix(self):
        request = self.factory.get("/nz/en/admin/")
        request.market_prefix = "/nz"
        request.market_slug = "nz"
        set_script_prefix("/nz/")

        out = self._render("{% market_url 'default' 'admin:index' %}", request)
        self.assertEqual(out, "/en/admin/")

    def test_market_url_composes_with_subpath(self):
        # Site mounted under /shop, visitor on the /nz market
        request = self.factory.get("/shop/nz/en/admin/")
        request.script_name = "/shop"
        request.market_prefix = "/nz"
        request.market_slug = "nz"
        set_script_prefix("/shop/nz/")

        out = self._render("{% market_url 'sg' 'admin:index' %}", request)
        self.assertEqual(out, "/shop/sg/en/admin/")

    def test_market_url_default_market_under_subpath(self):
        request = self.factory.get("/shop/nz/en/admin/")
        request.script_name = "/shop"
        request.market_prefix = "/nz"
        request.market_slug = "nz"
        set_script_prefix("/shop/nz/")

        out = self._render("{% market_url 'default' 'admin:index' %}", request)
        self.assertEqual(out, "/shop/en/admin/")

    def test_current_market_tag(self):
        request = self.factory.get("/nz/en/")
        request.market_slug = "nz"
        out = self._render("{% current_market %}", request)
        self.assertEqual(out, "nz")
