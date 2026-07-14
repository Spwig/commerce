"""
Tests for CSS Isolation Integration

Verifies that LayoutRenderer correctly applies CSS isolation for different builders.
"""

import pytest
from django.core.cache import cache

from design.layout_renderer import LayoutRenderer
from design.models import PageTier

TIER_MAP = {
    "checkout": "A",
    "cart": "A",
    "product": "B",
    "collection": "B",
    "home": "C",
    "landing": "C",
}


@pytest.fixture
def page_tiers(db):
    """Create PageTier records for every page type the tests reference."""
    # Clear registry cache so LayoutRenderer sees freshly-created tiers.
    cache.clear()
    tiers = {}
    for page_type, tier in TIER_MAP.items():
        tiers[page_type] = PageTier.objects.create(
            page_type=page_type,
            tier=tier,
            display_name=page_type.title(),
            description=f"{page_type} page",
            schema={
                "regions": {
                    "header": {"label": "Header", "locked": False},
                    "main": {"label": "Main", "locked": False},
                    "footer": {"label": "Footer", "locked": False},
                }
            },
            csp_policy={"script-src": ["'self'"]},
            max_external_scripts=0 if tier == "A" else 3,
            allows_custom_html=tier == "C",
            locked_regions=[],
        )
    yield tiers
    cache.clear()


@pytest.mark.django_db
@pytest.mark.usefixtures("page_tiers")
class TestCSSIsolationIntegration:
    """Test CSS isolation mechanisms for Brand Builder and Page Editor."""

    def test_brand_builder_isolation_class(self):
        """Test that Brand Builder isolation class is applied correctly."""
        renderer = LayoutRenderer(
            page_type="home",
            tier="C",
            context={
                "preview_mode": True,
                "isolation_type": "brand_builder",
            },
        )

        html = renderer.render()

        # Should wrap in hf-content-preview
        assert 'class="hf-content-preview"' in html
        assert 'data-theme="light"' in html

        # Should NOT contain page editor class
        assert "pb-content-preview" not in html

    def test_page_editor_isolation_class(self):
        """Test that Page Editor isolation class is applied correctly."""
        renderer = LayoutRenderer(
            page_type="home",
            tier="C",
            context={
                "preview_mode": True,
                "isolation_type": "page_editor",
            },
        )

        html = renderer.render()

        # Should wrap in pb-content-preview
        assert 'class="pb-content-preview"' in html
        assert 'data-theme="light"' in html

        # Should NOT contain brand builder class
        assert "hf-content-preview" not in html

    def test_default_isolation_type(self):
        """Test that default isolation type is page_editor."""
        renderer = LayoutRenderer(
            page_type="home",
            tier="C",
            context={
                "preview_mode": True,
                # No isolation_type specified - should default to page_editor
            },
        )

        html = renderer.render()

        # Should default to page editor isolation
        assert "pb-content-preview" in html

    def test_production_mode_no_isolation(self):
        """Test that production mode doesn't add isolation wrapper."""
        renderer = LayoutRenderer(
            page_type="home",
            tier="C",
            context={
                "preview_mode": False,  # Production mode
            },
        )

        html = renderer.render()

        # Should NOT wrap in any isolation classes
        assert "hf-content-preview" not in html
        assert "pb-content-preview" not in html

    def test_get_css_isolation_class_method(self):
        """Test the get_css_isolation_class() method."""
        # Brand Builder
        renderer_bb = LayoutRenderer(
            page_type="home",
            tier="C",
            context={
                "preview_mode": True,
                "isolation_type": "brand_builder",
            },
        )
        assert renderer_bb.get_css_isolation_class() == "hf-content-preview"

        # Page Editor
        renderer_pe = LayoutRenderer(
            page_type="home",
            tier="C",
            context={
                "preview_mode": True,
                "isolation_type": "page_editor",
            },
        )
        assert renderer_pe.get_css_isolation_class() == "pb-content-preview"

    def test_isolation_wrapper_structure(self):
        """Test that isolation wrapper has correct structure."""
        renderer = LayoutRenderer(
            page_type="home",
            tier="C",
            context={
                "preview_mode": True,
                "isolation_type": "brand_builder",
            },
        )

        html = renderer.render()

        # Should have opening div with isolation class
        assert '<div class="hf-content-preview" data-theme="light">' in html

        # Should have closing div
        assert html.strip().endswith("</div>")

    def test_isolation_preserves_inner_content(self):
        """Test that isolation wrapper preserves rendered content."""
        renderer = LayoutRenderer(
            page_type="home",
            tier="C",
            context={
                "preview_mode": True,
                "isolation_type": "page_editor",
            },
        )

        html = renderer.render()

        # Should contain the basic HTML structure
        assert "<html" in html
        assert "</html>" in html
        assert "<body>" in html
        assert "</body>" in html

        # Should contain region divs
        assert 'class="region' in html

    def test_different_page_types_with_isolation(self):
        """Test isolation works for different page types."""
        page_types = ["home", "landing", "product", "collection", "cart", "checkout"]

        for page_type in page_types:
            renderer = LayoutRenderer(
                page_type=page_type,
                tier=get_tier_for_page_type(page_type),
                context={
                    "preview_mode": True,
                    "isolation_type": "page_editor",
                },
            )

            html = renderer.render()

            # All should have isolation wrapper
            assert "pb-content-preview" in html, f"Failed for {page_type}"

    def test_caching_disabled_in_preview_mode(self):
        """Test that caching is disabled when preview_mode=True."""
        renderer = LayoutRenderer(
            page_type="home",
            tier="C",
            context={
                "preview_mode": True,
                "isolation_type": "brand_builder",
            },
        )

        # Render twice
        html1 = renderer.render()
        html2 = renderer.render()

        # Should get fresh renders (not cached)
        # Both should have isolation wrapper
        assert "hf-content-preview" in html1
        assert "hf-content-preview" in html2

    def test_invalid_isolation_type_fallback(self):
        """Test that invalid isolation type falls back to default."""
        renderer = LayoutRenderer(
            page_type="home",
            tier="C",
            context={
                "preview_mode": True,
                "isolation_type": "invalid_type",
            },
        )

        # Should fall back to page_editor (default)
        isolation_class = renderer.get_css_isolation_class()
        assert isolation_class == "pb-content-preview"


def get_tier_for_page_type(page_type):
    """Helper to get correct tier for page type."""
    tier_map = {
        "checkout": "A",
        "cart": "A",
        "product": "B",
        "collection": "B",
        "home": "C",
        "landing": "C",
    }
    return tier_map.get(page_type, "C")
