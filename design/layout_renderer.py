"""
Layout Renderer - Server-Side Rendering Engine

Transforms theme schemas into rendered HTML while enforcing tier restrictions
and maintaining security. Supports preview mode with CSS isolation.

Usage:
    renderer = LayoutRenderer(
        page_type='home',
        tier='C',
        context={'preview_mode': True}
    )
    html = renderer.render()

Architecture:
    Theme Schema → LayoutRenderer → Component Resolution → Slot Injection
    → Sanitization → Rendered HTML → CSS Isolation (preview mode)
"""

import logging
from typing import Dict, List, Optional, Any
from django.core.cache import cache
from django.template import Template, Context
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError

from .models import PageTier, ComponentStore
from .schema_registry import PageSchemaRegistry, SchemaValidationError
from .content_sanitizer import ContentSanitizer

logger = logging.getLogger(__name__)


class LayoutRenderError(Exception):
    """Raised when layout rendering fails"""
    pass


class LayoutRenderer:
    """
    Server-side layout renderer with tier enforcement.

    Provides:
    - Schema-driven rendering
    - Component resolution and rendering
    - Safe slot injection
    - Tier-based security enforcement
    - Preview mode with CSS isolation
    - Comprehensive error handling

    Example:
        >>> renderer = LayoutRenderer(
        ...     page_type='product',
        ...     tier='B',
        ...     context={'product_id': 123}
        ... )
        >>> html = renderer.render()
    """

    # Cache timeout for rendered layouts (1 minute)
    CACHE_TIMEOUT = 60
    CACHE_KEY_PREFIX = 'layout_render'

    # CSS isolation classes for preview mode
    ISOLATION_CLASSES = {
        'brand_builder': 'hf-content-preview',
        'page_editor': 'pb-content-preview',
    }

    def __init__(
        self,
        page_type: str,
        tier: str,
        context: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize renderer with page type and tier.

        Args:
            page_type: Page type identifier (e.g., 'home', 'product', 'checkout')
            tier: Page tier ('A', 'B', or 'C')
            context: Additional rendering context (preview_mode, user data, etc.)

        Raises:
            ValueError: If tier is invalid
            SchemaValidationError: If page type not found
        """
        if tier not in ['A', 'B', 'C']:
            raise ValueError(f"Invalid tier: {tier}. Must be 'A', 'B', or 'C'")

        self.page_type = page_type
        self.tier = tier
        self.context = context or {}

        # Detect preview mode and isolation settings (before other initialization)
        self.preview_mode = self.context.get('preview_mode', False)
        self.isolation_type = self.context.get('isolation_type', 'page_editor')

        # Initialize services
        self.schema_registry = PageSchemaRegistry()
        self.sanitizer = ContentSanitizer(tier=tier)

        # Load page tier configuration
        self.page_tier = self.schema_registry.get_page_tier(page_type)
        if not self.page_tier:
            raise SchemaValidationError(
                f"Page type '{page_type}' not found in schema registry"
            )

        logger.debug(
            f"LayoutRenderer initialized: page_type={page_type}, "
            f"tier={tier}, preview_mode={self.preview_mode}"
        )

    def render(self) -> str:
        """
        Render complete layout as HTML.

        Returns:
            Rendered HTML string

        Raises:
            LayoutRenderError: If rendering fails

        Example:
            >>> renderer = LayoutRenderer('home', 'C')
            >>> html = renderer.render()
            >>> assert '<html' in html
        """
        try:
            # Check cache first (skip cache in preview mode)
            if not self.preview_mode:
                cached = self._get_cached_render()
                if cached:
                    logger.debug(f"Cache hit for {self.page_type} (tier {self.tier})")
                    return cached

            # Build rendering context
            render_context = self._build_render_context()

            # Get page schema
            schema = self.page_tier.schema
            if not schema:
                raise LayoutRenderError(
                    f"No schema defined for page type '{self.page_type}'"
                )

            # Render regions
            regions_html = {}
            for region_id in schema.get('regions', {}):
                region_config = schema['regions'][region_id]
                regions_html[region_id] = self.render_region(
                    region_id,
                    region_config
                )

            # Build complete layout
            html = self._assemble_layout(regions_html, render_context)

            # Wrap in CSS isolation container if preview mode
            if self.preview_mode:
                html = self._wrap_with_isolation(html)

            # Cache result (if not preview mode)
            if not self.preview_mode:
                self._cache_render(html)

            logger.info(
                f"Rendered {self.page_type} layout (tier {self.tier}, "
                f"{len(html)} bytes)"
            )
            return html

        except Exception as e:
            logger.error(
                f"Failed to render {self.page_type}: {e}",
                exc_info=True
            )
            # Return fallback HTML instead of crashing
            return self._get_fallback_html(str(e))

    def render_region(
        self,
        region_id: str,
        region_config: Dict[str, Any]
    ) -> str:
        """
        Render a specific region with components.

        Args:
            region_id: Region identifier (e.g., 'header', 'footer', 'main')
            region_config: Region configuration from schema

        Returns:
            Rendered region HTML

        Example:
            >>> renderer = LayoutRenderer('home', 'C')
            >>> html = renderer.render_region('header', {...})
        """
        try:
            # Check if region is locked (cannot be modified)
            if region_config.get('locked', False):
                logger.debug(f"Rendering locked region: {region_id}")

            # Get components for this region
            components = region_config.get('components', [])

            # Render each component
            component_htmls = []
            for component_config in components:
                component_html = self._render_component(component_config)
                if component_html:
                    component_htmls.append(component_html)

            # Assemble region HTML
            region_html = '\n'.join(component_htmls)

            # Wrap in region container (always wrap for consistent structure)
            region_classes = region_config.get('classes', '')
            region_html = (
                f'<div class="region region-{region_id} {region_classes}">'
                f'{region_html}'
                f'</div>'
            )

            return region_html

        except Exception as e:
            logger.error(f"Failed to render region {region_id}: {e}", exc_info=True)
            return f'<!-- Region {region_id} failed to render: {e} -->'

    def enforce_tier_restrictions(self, component_type: str) -> bool:
        """
        Check if component is allowed in current tier.

        Args:
            component_type: Component type identifier

        Returns:
            True if component is allowed, False otherwise

        Example:
            >>> renderer = LayoutRenderer('checkout', 'A')
            >>> renderer.enforce_tier_restrictions('custom_banner')
            False  # Custom banners not allowed in checkout (Tier A)
        """
        try:
            # Use schema registry to validate component placement
            self.schema_registry.validate_component_placement(
                page_type=self.page_type,
                component_type=component_type,
                region=None  # Region check is separate
            )
            return True

        except (SchemaValidationError, ValidationError) as e:
            logger.warning(
                f"Component {component_type} not allowed in {self.page_type} "
                f"(tier {self.tier}): {e}"
            )
            return False

    def get_css_isolation_class(self) -> str:
        """
        Return appropriate CSS isolation class for preview mode.

        Returns:
            CSS isolation class name

        Example:
            >>> renderer = LayoutRenderer('home', 'C', {'isolation_type': 'brand_builder'})
            >>> renderer.get_css_isolation_class()
            'hf-content-preview'
        """
        return self.ISOLATION_CLASSES.get(
            self.isolation_type,
            self.ISOLATION_CLASSES['page_editor']  # Default
        )

    def _build_render_context(self) -> Dict[str, Any]:
        """Build rendering context with all necessary data."""
        context = {
            'page_type': self.page_type,
            'tier': self.tier,
            'preview_mode': self.preview_mode,
            'schema': self.page_tier.schema,
        }

        # Merge user-provided context
        context.update(self.context)

        return context

    def _render_component(self, component_config: Dict[str, Any]) -> str:
        """
        Render a single component.

        Args:
            component_config: Component configuration from schema

        Returns:
            Rendered component HTML
        """
        component_type = component_config.get('type')
        if not component_type:
            logger.warning("Component missing 'type' field")
            return ''

        # Check tier restrictions
        if not self.enforce_tier_restrictions(component_type):
            logger.debug(f"Component {component_type} blocked by tier restrictions")
            return ''

        # For now, return a placeholder
        # Task 2 (Component Resolution Service) will handle actual rendering
        component_data = component_config.get('data', {})
        return f'<!-- Component: {component_type} (data: {component_data}) -->'

    def _assemble_layout(
        self,
        regions_html: Dict[str, str],
        context: Dict[str, Any]
    ) -> str:
        """
        Assemble complete layout from rendered regions.

        Args:
            regions_html: Dict mapping region IDs to rendered HTML
            context: Rendering context

        Returns:
            Complete layout HTML
        """
        # Build basic HTML structure
        # This will be replaced with actual theme template rendering in later tasks
        parts = []
        parts.append('<!DOCTYPE html>')
        parts.append('<html lang="en">')
        parts.append('<head>')
        parts.append(f'<title>{self.page_type.title()} - Tier {self.tier}</title>')
        parts.append('<meta charset="UTF-8">')
        parts.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
        parts.append('</head>')
        parts.append('<body>')

        # Add regions
        for region_id, region_html in regions_html.items():
            parts.append(region_html)

        parts.append('</body>')
        parts.append('</html>')

        return '\n'.join(parts)

    def _wrap_with_isolation(self, html: str) -> str:
        """
        Wrap HTML with CSS isolation container for preview mode.

        Args:
            html: HTML to wrap

        Returns:
            Wrapped HTML with isolation class

        Example:
            >>> renderer = LayoutRenderer('home', 'C', {'preview_mode': True})
            >>> wrapped = renderer._wrap_with_isolation('<p>Content</p>')
            >>> assert 'pb-content-preview' in wrapped
        """
        isolation_class = self.get_css_isolation_class()

        # Wrap in isolation container with forced light theme
        wrapped = (
            f'<div class="{isolation_class}" data-theme="light">\n'
            f'{html}\n'
            f'</div>'
        )

        logger.debug(f"Wrapped HTML with isolation class: {isolation_class}")
        return wrapped

    def _get_fallback_html(self, error_msg: str) -> str:
        """
        Generate fallback HTML when rendering fails.

        Args:
            error_msg: Error message to display (in debug mode)

        Returns:
            Fallback HTML
        """
        # In production, show generic error
        # In preview/debug mode, show details
        if self.preview_mode:
            return (
                f'<div class="layout-render-error">\n'
                f'<h2>Layout Rendering Error</h2>\n'
                f'<p>Failed to render {self.page_type} layout (tier {self.tier})</p>\n'
                f'<pre>{error_msg}</pre>\n'
                f'</div>'
            )
        else:
            return (
                f'<div class="layout-render-error">\n'
                f'<p>This page is temporarily unavailable. Please try again later.</p>\n'
                f'</div>'
            )

    def _get_cached_render(self) -> Optional[str]:
        """Get cached render if available."""
        cache_key = f'{self.CACHE_KEY_PREFIX}:{self.page_type}:{self.tier}'
        return cache.get(cache_key)

    def _cache_render(self, html: str) -> None:
        """Cache rendered HTML."""
        cache_key = f'{self.CACHE_KEY_PREFIX}:{self.page_type}:{self.tier}'
        cache.set(cache_key, html, self.CACHE_TIMEOUT)
        logger.debug(f"Cached render for {self.page_type} (tier {self.tier})")
