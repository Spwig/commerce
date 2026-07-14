"""
Tests for LayoutRenderer - Server-Side Rendering Engine

Tests cover:
- Initialization and configuration
- Schema resolution and validation
- Region rendering
- Component tier enforcement
- Preview mode and CSS isolation
- Caching behavior
- Error handling and fallbacks
"""

from unittest.mock import Mock, patch

import pytest
from django.core.cache import cache

from design.layout_renderer import LayoutRenderer
from design.models import PageTier
from design.schema_registry import SchemaValidationError


@pytest.mark.django_db
class TestLayoutRendererInitialization:
    """Test LayoutRenderer initialization and configuration."""

    def test_initialize_with_valid_tier_a(self):
        """Test initialization with Tier A (checkout)."""
        with patch("design.layout_renderer.PageSchemaRegistry") as mock_registry:
            mock_registry_instance = mock_registry.return_value
            mock_tier = Mock(spec=PageTier)
            mock_tier.tier = "A"
            mock_tier.schema = {"regions": {}}
            mock_registry_instance.get_page_tier.return_value = mock_tier

            renderer = LayoutRenderer(page_type="checkout", tier="A")

            assert renderer.page_type == "checkout"
            assert renderer.tier == "A"
            assert renderer.preview_mode is False

    def test_initialize_with_valid_tier_b(self):
        """Test initialization with Tier B (product)."""
        with patch("design.layout_renderer.PageSchemaRegistry") as mock_registry:
            mock_registry_instance = mock_registry.return_value
            mock_tier = Mock(spec=PageTier)
            mock_tier.tier = "B"
            mock_tier.schema = {"regions": {}}
            mock_registry_instance.get_page_tier.return_value = mock_tier

            renderer = LayoutRenderer(page_type="product", tier="B")

            assert renderer.tier == "B"

    def test_initialize_with_valid_tier_c(self):
        """Test initialization with Tier C (marketing)."""
        with patch("design.layout_renderer.PageSchemaRegistry") as mock_registry:
            mock_registry_instance = mock_registry.return_value
            mock_tier = Mock(spec=PageTier)
            mock_tier.tier = "C"
            mock_tier.schema = {"regions": {}}
            mock_registry_instance.get_page_tier.return_value = mock_tier

            renderer = LayoutRenderer(page_type="home", tier="C")

            assert renderer.tier == "C"

    def test_initialize_with_invalid_tier(self):
        """Test initialization with invalid tier raises ValueError."""
        with pytest.raises(ValueError, match="Invalid tier"):
            LayoutRenderer(page_type="home", tier="X")

    def test_initialize_with_preview_mode(self):
        """Test initialization with preview mode enabled."""
        with patch("design.layout_renderer.PageSchemaRegistry") as mock_registry:
            mock_registry_instance = mock_registry.return_value
            mock_tier = Mock(spec=PageTier)
            mock_tier.schema = {"regions": {}}
            mock_registry_instance.get_page_tier.return_value = mock_tier

            renderer = LayoutRenderer(page_type="home", tier="C", context={"preview_mode": True})

            assert renderer.preview_mode is True

    def test_initialize_with_custom_context(self):
        """Test initialization with custom rendering context."""
        with patch("design.layout_renderer.PageSchemaRegistry") as mock_registry:
            mock_registry_instance = mock_registry.return_value
            mock_tier = Mock(spec=PageTier)
            mock_tier.schema = {"regions": {}}
            mock_registry_instance.get_page_tier.return_value = mock_tier

            custom_context = {
                "user_id": 123,
                "preview_mode": True,
                "isolation_type": "brand_builder",
            }
            renderer = LayoutRenderer(page_type="home", tier="C", context=custom_context)

            assert renderer.context["user_id"] == 123
            assert renderer.isolation_type == "brand_builder"

    def test_initialize_with_nonexistent_page_type(self):
        """Test initialization with nonexistent page type raises error."""
        with patch("design.layout_renderer.PageSchemaRegistry") as mock_registry:
            mock_registry_instance = mock_registry.return_value
            mock_registry_instance.get_page_tier.return_value = None

            with pytest.raises(SchemaValidationError, match="not found"):
                LayoutRenderer(page_type="invalid_page", tier="C")


@pytest.mark.django_db
class TestLayoutRendererCSSIsolation:
    """Test CSS isolation for preview mode."""

    def test_get_css_isolation_class_page_editor(self):
        """Test CSS isolation class for page editor."""
        with patch("design.layout_renderer.PageSchemaRegistry") as mock_registry:
            mock_registry_instance = mock_registry.return_value
            mock_tier = Mock(spec=PageTier)
            mock_tier.schema = {"regions": {}}
            mock_registry_instance.get_page_tier.return_value = mock_tier

            renderer = LayoutRenderer(
                page_type="home", tier="C", context={"isolation_type": "page_editor"}
            )

            assert renderer.get_css_isolation_class() == "pb-content-preview"

    def test_get_css_isolation_class_brand_builder(self):
        """Test CSS isolation class for brand builder."""
        with patch("design.layout_renderer.PageSchemaRegistry") as mock_registry:
            mock_registry_instance = mock_registry.return_value
            mock_tier = Mock(spec=PageTier)
            mock_tier.schema = {"regions": {}}
            mock_registry_instance.get_page_tier.return_value = mock_tier

            renderer = LayoutRenderer(
                page_type="home", tier="C", context={"isolation_type": "brand_builder"}
            )

            assert renderer.get_css_isolation_class() == "hf-content-preview"

    def test_wrap_with_isolation_page_editor(self):
        """Test HTML wrapping with page editor isolation."""
        with patch("design.layout_renderer.PageSchemaRegistry") as mock_registry:
            mock_registry_instance = mock_registry.return_value
            mock_tier = Mock(spec=PageTier)
            mock_tier.schema = {"regions": {}}
            mock_registry_instance.get_page_tier.return_value = mock_tier

            renderer = LayoutRenderer(
                page_type="home",
                tier="C",
                context={"preview_mode": True, "isolation_type": "page_editor"},
            )

            html = "<p>Test content</p>"
            wrapped = renderer._wrap_with_isolation(html)

            assert "pb-content-preview" in wrapped
            assert 'data-theme="light"' in wrapped
            assert "<p>Test content</p>" in wrapped

    def test_wrap_with_isolation_brand_builder(self):
        """Test HTML wrapping with brand builder isolation."""
        with patch("design.layout_renderer.PageSchemaRegistry") as mock_registry:
            mock_registry_instance = mock_registry.return_value
            mock_tier = Mock(spec=PageTier)
            mock_tier.schema = {"regions": {}}
            mock_registry_instance.get_page_tier.return_value = mock_tier

            renderer = LayoutRenderer(
                page_type="home",
                tier="C",
                context={"preview_mode": True, "isolation_type": "brand_builder"},
            )

            html = "<p>Test content</p>"
            wrapped = renderer._wrap_with_isolation(html)

            assert "hf-content-preview" in wrapped
            assert 'data-theme="light"' in wrapped


@pytest.mark.django_db
class TestLayoutRendererTierEnforcement:
    """Test tier-based component restrictions."""

    def test_enforce_tier_restrictions_allowed(self):
        """Test component allowed in tier."""
        with patch("design.layout_renderer.PageSchemaRegistry") as mock_registry:
            mock_registry_instance = mock_registry.return_value
            mock_tier = Mock(spec=PageTier)
            mock_tier.schema = {"regions": {}}
            mock_registry_instance.get_page_tier.return_value = mock_tier

            # Mock validate_component_placement to succeed
            mock_registry_instance.validate_component_placement.return_value = None

            renderer = LayoutRenderer(page_type="home", tier="C")
            result = renderer.enforce_tier_restrictions("banner")

            assert result is True

    def test_enforce_tier_restrictions_blocked(self):
        """Test component blocked in tier."""
        with patch("design.layout_renderer.PageSchemaRegistry") as mock_registry:
            mock_registry_instance = mock_registry.return_value
            mock_tier = Mock(spec=PageTier)
            mock_tier.schema = {"regions": {}}
            mock_registry_instance.get_page_tier.return_value = mock_tier

            # Mock validate_component_placement to raise error
            mock_registry_instance.validate_component_placement.side_effect = SchemaValidationError(
                "Component not allowed"
            )

            renderer = LayoutRenderer(page_type="checkout", tier="A")
            result = renderer.enforce_tier_restrictions("custom_banner")

            assert result is False


@pytest.mark.django_db
class TestLayoutRendererRegionRendering:
    """Test region rendering functionality."""

    def test_render_region_with_no_components(self):
        """Test rendering empty region."""
        with patch("design.layout_renderer.PageSchemaRegistry") as mock_registry:
            mock_registry_instance = mock_registry.return_value
            mock_tier = Mock(spec=PageTier)
            mock_tier.schema = {"regions": {}}
            mock_registry_instance.get_page_tier.return_value = mock_tier

            renderer = LayoutRenderer(page_type="home", tier="C")
            region_config = {"components": [], "classes": "custom-class"}

            html = renderer.render_region("header", region_config)

            assert "region-header" in html
            assert "custom-class" in html

    def test_render_region_with_components(self):
        """Test rendering region with components."""
        with patch("design.layout_renderer.PageSchemaRegistry") as mock_registry:
            mock_registry_instance = mock_registry.return_value
            mock_tier = Mock(spec=PageTier)
            mock_tier.schema = {"regions": {}}
            mock_registry_instance.get_page_tier.return_value = mock_tier
            mock_registry_instance.validate_component_placement.return_value = None

            renderer = LayoutRenderer(page_type="home", tier="C")
            region_config = {
                "components": [{"type": "banner", "data": {}}, {"type": "newsletter", "data": {}}]
            }

            html = renderer.render_region("header", region_config)

            assert "Component: banner" in html
            assert "Component: newsletter" in html

    def test_render_region_locked(self):
        """Test rendering locked region."""
        with patch("design.layout_renderer.PageSchemaRegistry") as mock_registry:
            mock_registry_instance = mock_registry.return_value
            mock_tier = Mock(spec=PageTier)
            mock_tier.schema = {"regions": {}}
            mock_registry_instance.get_page_tier.return_value = mock_tier

            renderer = LayoutRenderer(page_type="home", tier="C")
            region_config = {"locked": True, "components": []}

            # Should not raise error
            html = renderer.render_region("header", region_config)
            assert html is not None

    def test_render_region_error_handling(self):
        """Test region rendering error handling."""
        with patch("design.layout_renderer.PageSchemaRegistry") as mock_registry:
            mock_registry_instance = mock_registry.return_value
            mock_tier = Mock(spec=PageTier)
            mock_tier.schema = {"regions": {}}
            mock_registry_instance.get_page_tier.return_value = mock_tier

            renderer = LayoutRenderer(page_type="home", tier="C")

            # Pass invalid region config to trigger error
            html = renderer.render_region("header", None)

            # Should return error comment, not crash
            assert "<!-- Region header failed to render" in html


@pytest.mark.django_db
class TestLayoutRendererFullRender:
    """Test complete layout rendering."""

    @pytest.fixture(autouse=True)
    def clear_cache(self):
        """Clear cache before and after each test."""
        cache.clear()
        yield
        cache.clear()

    def test_render_complete_layout(self):
        """Test rendering complete layout with multiple regions."""
        with patch("design.layout_renderer.PageSchemaRegistry") as mock_registry:
            mock_registry_instance = mock_registry.return_value
            mock_tier = Mock(spec=PageTier)
            mock_tier.schema = {
                "regions": {
                    "header": {"components": []},
                    "main": {"components": []},
                    "footer": {"components": []},
                }
            }
            mock_registry_instance.get_page_tier.return_value = mock_tier

            renderer = LayoutRenderer(page_type="home", tier="C")
            html = renderer.render()

            assert "<!DOCTYPE html>" in html
            assert "<html" in html
            assert "</html>" in html
            assert "region-header" in html
            assert "region-main" in html
            assert "region-footer" in html

    def test_render_with_preview_mode_wraps_in_isolation(self):
        """Test rendering in preview mode includes CSS isolation."""
        with patch("design.layout_renderer.PageSchemaRegistry") as mock_registry:
            mock_registry_instance = mock_registry.return_value
            mock_tier = Mock(spec=PageTier)
            mock_tier.schema = {"regions": {"main": {"components": []}}}
            mock_registry_instance.get_page_tier.return_value = mock_tier

            renderer = LayoutRenderer(
                page_type="home",
                tier="C",
                context={"preview_mode": True, "isolation_type": "page_editor"},
            )
            html = renderer.render()

            assert "pb-content-preview" in html
            assert 'data-theme="light"' in html

    def test_render_without_preview_mode_no_isolation(self):
        """Test rendering in production mode has no CSS isolation wrapper."""
        with patch("design.layout_renderer.PageSchemaRegistry") as mock_registry:
            mock_registry_instance = mock_registry.return_value
            mock_tier = Mock(spec=PageTier)
            mock_tier.schema = {"regions": {"main": {"components": []}}}
            mock_registry_instance.get_page_tier.return_value = mock_tier

            renderer = LayoutRenderer(page_type="home", tier="C", context={"preview_mode": False})
            html = renderer.render()

            # Should not have isolation wrapper
            assert "pb-content-preview" not in html
            assert "hf-content-preview" not in html

    def test_render_with_missing_schema(self):
        """Test rendering with missing schema returns fallback."""
        with patch("design.layout_renderer.PageSchemaRegistry") as mock_registry:
            mock_registry_instance = mock_registry.return_value
            mock_tier = Mock(spec=PageTier)
            mock_tier.schema = None  # No schema
            mock_registry_instance.get_page_tier.return_value = mock_tier

            renderer = LayoutRenderer(page_type="home", tier="C")
            html = renderer.render()

            # Should return fallback HTML with error message
            assert "temporarily unavailable" in html.lower() or "error" in html.lower()

    def test_render_fallback_html_production_mode(self):
        """Test fallback HTML in production mode is generic."""
        with patch("design.layout_renderer.PageSchemaRegistry") as mock_registry:
            mock_registry_instance = mock_registry.return_value
            mock_tier = Mock(spec=PageTier)
            mock_tier.schema = {"regions": {}}
            mock_registry_instance.get_page_tier.return_value = mock_tier

            renderer = LayoutRenderer(page_type="home", tier="C", context={"preview_mode": False})
            fallback = renderer._get_fallback_html("Test error")

            assert "temporarily unavailable" in fallback.lower()
            # Should not show error details in production
            assert "Test error" not in fallback

    def test_render_fallback_html_preview_mode(self):
        """Test fallback HTML in preview mode shows details."""
        with patch("design.layout_renderer.PageSchemaRegistry") as mock_registry:
            mock_registry_instance = mock_registry.return_value
            mock_tier = Mock(spec=PageTier)
            mock_tier.schema = {"regions": {}}
            mock_registry_instance.get_page_tier.return_value = mock_tier

            renderer = LayoutRenderer(page_type="home", tier="C", context={"preview_mode": True})
            fallback = renderer._get_fallback_html("Test error")

            # Should show error details in preview mode
            assert "Test error" in fallback
            assert "Layout Rendering Error" in fallback


@pytest.mark.django_db
class TestLayoutRendererCaching:
    """Test caching behavior."""

    @pytest.fixture(autouse=True)
    def clear_cache(self):
        """Clear cache before and after each test."""
        cache.clear()
        yield
        cache.clear()

    def test_render_caches_result_in_production(self):
        """Test that rendering caches result in production mode."""
        with patch("design.layout_renderer.PageSchemaRegistry") as mock_registry:
            mock_registry_instance = mock_registry.return_value
            mock_tier = Mock(spec=PageTier)
            mock_tier.schema = {"regions": {"main": {"components": []}}}
            mock_registry_instance.get_page_tier.return_value = mock_tier

            renderer = LayoutRenderer(page_type="home", tier="C", context={"preview_mode": False})

            # First render should cache
            html1 = renderer.render()

            # Second render should use cache
            html2 = renderer.render()

            assert html1 == html2

    def test_render_skips_cache_in_preview_mode(self):
        """Test that preview mode skips cache."""
        with patch("design.layout_renderer.PageSchemaRegistry") as mock_registry:
            mock_registry_instance = mock_registry.return_value
            mock_tier = Mock(spec=PageTier)
            mock_tier.schema = {"regions": {"main": {"components": []}}}
            mock_registry_instance.get_page_tier.return_value = mock_tier

            renderer = LayoutRenderer(page_type="home", tier="C", context={"preview_mode": True})

            # Should not use cache
            html = renderer.render()

            # Check that cache is not set
            cache_key = "layout_render:home:C"
            cached = cache.get(cache_key)
            assert cached is None


@pytest.mark.django_db
class TestLayoutRendererComponents:
    """Test component rendering."""

    def test_render_component_with_valid_type(self):
        """Test rendering component with valid type."""
        with patch("design.layout_renderer.PageSchemaRegistry") as mock_registry:
            mock_registry_instance = mock_registry.return_value
            mock_tier = Mock(spec=PageTier)
            mock_tier.schema = {"regions": {}}
            mock_registry_instance.get_page_tier.return_value = mock_tier
            mock_registry_instance.validate_component_placement.return_value = None

            renderer = LayoutRenderer(page_type="home", tier="C")

            component_config = {"type": "banner", "data": {"title": "Test"}}
            html = renderer._render_component(component_config)

            assert "Component: banner" in html

    def test_render_component_missing_type(self):
        """Test rendering component without type returns empty."""
        with patch("design.layout_renderer.PageSchemaRegistry") as mock_registry:
            mock_registry_instance = mock_registry.return_value
            mock_tier = Mock(spec=PageTier)
            mock_tier.schema = {"regions": {}}
            mock_registry_instance.get_page_tier.return_value = mock_tier

            renderer = LayoutRenderer(page_type="home", tier="C")

            component_config = {"data": {}}
            html = renderer._render_component(component_config)

            assert html == ""

    def test_render_component_blocked_by_tier(self):
        """Test component blocked by tier restrictions returns empty."""
        with patch("design.layout_renderer.PageSchemaRegistry") as mock_registry:
            mock_registry_instance = mock_registry.return_value
            mock_tier = Mock(spec=PageTier)
            mock_tier.schema = {"regions": {}}
            mock_registry_instance.get_page_tier.return_value = mock_tier
            mock_registry_instance.validate_component_placement.side_effect = SchemaValidationError(
                "Not allowed"
            )

            renderer = LayoutRenderer(page_type="checkout", tier="A")

            component_config = {"type": "custom_banner", "data": {}}
            html = renderer._render_component(component_config)

            assert html == ""
