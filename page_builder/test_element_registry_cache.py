"""Regression tests for the element-registry cache across platform versions.

The registry caches pickled ``ElementConfig`` instances in Redis. When a release
adds a field to ``ElementConfig`` (as 1.7.3 did with ``conditional_css_files``),
an object pickled under the *previous* release rehydrates without re-running
``__init__``, so the new attribute is simply absent. Reading it from the
storefront home path raised ``AttributeError`` and returned HTTP 500.

Two independent guards are covered here:

1. The cache key is versioned by the platform release, so a new build can never
   read a prior release's differently-shaped objects.
2. The home CSS-collection path reads the field defensively, so even a stale
   object degrades to "no variant CSS" instead of 500ing.
"""

from pathlib import Path
from unittest.mock import patch

from django.test import TestCase

from core.version import __version__ as PLATFORM_VERSION
from page_builder.element_registry import REGISTRY_CACHE_KEY, ElementConfig
from page_builder.models import Element, Page
from page_builder.views import PageView


class RegistryCacheKeyVersioningTests(TestCase):
    def test_cache_key_is_pinned_to_platform_version(self):
        # If this ever drops the version suffix, cross-version cache poisoning
        # (the 1.7.3 conditional_css_files 500) becomes possible again.
        self.assertEqual(
            REGISTRY_CACHE_KEY,
            f"page_builder_elements_registry:v{PLATFORM_VERSION}",
        )


class StaleCachedElementConfigTests(TestCase):
    """A cached ElementConfig from an older release must not 500 the home page."""

    def setUp(self):
        self.page = Page.objects.create(
            title="Home", slug="home", page_type="home", status="published"
        )
        self.element = Element.objects.create(
            page=self.page,
            element_type="product_grid",
            is_active=True,
            content={"layout": "grid"},
        )

    @staticmethod
    def _stale_config():
        """An ElementConfig shaped like one pickled before conditional_css_files existed."""
        cfg = ElementConfig(
            "product_grid",
            {
                "css_files": ["page_builder/elements/product_grid/style.css"],
                "conditional_css_files": [
                    {
                        "property": "layout",
                        "default": "grid",
                        "map": {"grid": "grid.css", "list": "list.css"},
                    }
                ],
            },
            Path("."),
        )
        # Simulate an unpickled older-release object: __init__ never ran under
        # the new code, so the attribute the new field introduced is missing.
        del cfg.conditional_css_files
        return cfg

    def test_collect_css_does_not_raise_on_stale_config(self):
        stale = self._stale_config()
        self.assertFalse(hasattr(stale, "conditional_css_files"))

        with patch("page_builder.element_registry.registry.get_element", return_value=stale):
            css_files = PageView()._collect_element_css(self.page.elements.all())

        # Base css_files still collected; variant CSS silently skipped rather than 500.
        self.assertIn("page_builder/elements/product_grid/style.css", css_files)

    def test_fresh_config_still_collects_variant_css(self):
        fresh = self._stale_config()
        # Restore the field the way a correctly-built object would have it.
        fresh.conditional_css_files = [
            {"property": "layout", "default": "grid", "map": {"grid": "grid.css"}}
        ]

        with patch("page_builder.element_registry.registry.get_element", return_value=fresh):
            css_files = PageView()._collect_element_css(self.page.elements.all())

        # layout=grid on the element resolves to the grid variant stylesheet.
        self.assertIn("grid.css", css_files)
