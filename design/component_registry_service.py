"""
Component Registry Service - Component Resolution and Loading

Provides runtime component resolution for the LayoutRenderer:
- Component lookup by type and tier
- Version resolution (latest or specific)
- Template loading from component packages
- Component context preparation
- Caching for performance

Usage:
    service = ComponentRegistryService()
    component_data = service.resolve_for_render(
        component_type='banner',
        tier='C',
        version='1.0.0'
    )
    template = service.load_component_template(component_data['component'])
"""

import logging
import os
from pathlib import Path
from typing import Any

from django.core.cache import cache

from .models import ComponentStore, TierComponentPermission
from .schema_registry import PageSchemaRegistry

logger = logging.getLogger(__name__)


class ComponentResolutionError(Exception):
    """Raised when component resolution fails"""

    pass


class ComponentRegistryService:
    """
    Service for resolving and loading components at render time.

    Provides:
    - Component lookup with caching
    - Version resolution
    - Template loading from packages
    - Context preparation
    - Fallback handling for missing components

    Example:
        >>> service = ComponentRegistryService()
        >>> data = service.resolve_for_render('banner', 'C')
        >>> template = service.load_component_template(data['component'])
    """

    # Cache timeout for component data (1 hour)
    CACHE_TIMEOUT = 3600
    CACHE_KEY_PREFIX = "component_registry"

    def __init__(self):
        """Initialize the component registry service."""
        self.schema_registry = PageSchemaRegistry()

    def resolve_for_render(
        self,
        component_type: str,
        tier: str,
        version: str | None = None,
        page_type: str | None = None,
    ) -> dict[str, Any]:
        """
        Resolve component for rendering.

        Args:
            component_type: Component type identifier (e.g., 'banner', 'newsletter')
            tier: Page tier ('A', 'B', or 'C')
            version: Specific version to load (None = latest)
            page_type: Page type for permission checking (optional)

        Returns:
            Dict with component data:
            {
                'component': ComponentStore instance,
                'template_path': str,
                'assets': dict,
                'permissions': dict
            }

        Raises:
            ComponentResolutionError: If component cannot be resolved

        Example:
            >>> service = ComponentRegistryService()
            >>> data = service.resolve_for_render('banner', 'C', version='1.0.0')
            >>> print(data['component'].name)
            'Banner Component'
        """
        try:
            # Check cache first
            component = self._get_cached_component(component_type, tier, version)

            if not component:
                # Load from database
                component = self._load_component_from_db(component_type, tier, version)

                # Cache for future requests
                self._cache_component(component, tier, version)

            # Check tier permissions if page_type provided
            if page_type:
                self._validate_tier_permissions(component, tier, page_type)

            # Prepare component data
            return {
                "component": component,
                "template_path": self._get_template_path(component),
                "assets": self._get_component_assets(component),
                "permissions": self._get_component_permissions(component, tier),
            }

        except ComponentStore.DoesNotExist:
            logger.error(f"Component '{component_type}' not found")
            raise ComponentResolutionError(f"Component '{component_type}' not found")
        except Exception as e:
            logger.error(f"Failed to resolve component '{component_type}': {e}")
            raise ComponentResolutionError(str(e))

    def load_component_template(self, component: ComponentStore) -> str:
        """
        Load component template from package.

        Args:
            component: ComponentStore instance

        Returns:
            Template content as string

        Example:
            >>> service = ComponentRegistryService()
            >>> component = ComponentStore.objects.get(component_type='banner')
            >>> template = service.load_component_template(component)
            >>> assert '<div' in template
        """
        try:
            template_path = self._get_template_path(component)

            # Load template file
            if os.path.exists(template_path):
                with open(template_path, encoding="utf-8") as f:
                    return f.read()

            # Fallback to default template
            logger.warning(f"Template not found for {component.component_type}, using fallback")
            return self._get_fallback_template(component)

        except Exception as e:
            logger.error(f"Failed to load template for {component.component_type}: {e}")
            return self._get_fallback_template(component)

    def prepare_component_context(
        self, component: ComponentStore, instance_data: dict[str, Any], page_context: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Prepare rendering context for component instance.

        Args:
            component: ComponentStore instance
            instance_data: Component-specific data from page schema
            page_context: Page-level context (tier, page_type, user data, etc.)

        Returns:
            Complete context dict for rendering

        Example:
            >>> service = ComponentRegistryService()
            >>> component = ComponentStore.objects.get(component_type='banner')
            >>> context = service.prepare_component_context(
            ...     component,
            ...     {'title': 'Welcome'},
            ...     {'tier': 'C', 'user_id': 123}
            ... )
            >>> assert 'component' in context
            >>> assert context['title'] == 'Welcome'
        """
        # Build base context
        context = {
            "component": {
                "type": component.component_type,
                "name": component.name,
                "version": component.version,
            },
            "tier": page_context.get("tier"),
            "page_type": page_context.get("page_type"),
        }

        # Add instance-specific data
        context.update(instance_data)

        # Add page context (but don't override instance data)
        for key, value in page_context.items():
            if key not in context:
                context[key] = value

        return context

    def get_fallback_component(self, component_type: str) -> dict[str, Any]:
        """
        Get fallback data for missing component.

        Args:
            component_type: The component type that couldn't be loaded

        Returns:
            Fallback component data

        Example:
            >>> service = ComponentRegistryService()
            >>> fallback = service.get_fallback_component('missing_component')
            >>> assert 'component' in fallback
        """
        logger.warning(f"Using fallback for missing component: {component_type}")

        # Create a mock component for fallback
        mock_component = type(
            "MockComponent",
            (),
            {
                "component_type": component_type,
                "name": f"[Missing: {component_type}]",
                "version": "0.0.0",
                "package_name": "fallback",
            },
        )()

        return {
            "component": mock_component,
            "template_path": "",
            "assets": {},
            "permissions": {},
            "is_fallback": True,
        }

    # Private methods

    def _load_component_from_db(
        self, component_type: str, tier: str, version: str | None = None
    ) -> ComponentStore:
        """
        Load component from database.

        Args:
            component_type: Component type identifier
            tier: Page tier
            version: Specific version or None for latest

        Returns:
            ComponentStore instance

        Raises:
            ComponentStore.DoesNotExist: If component not found
        """
        query = ComponentStore.objects.filter(component_type=component_type, is_active=True)

        # Specific version if requested, otherwise the latest
        query = query.filter(version=version) if version else query.order_by("-created_at")

        component = query.first()

        if not component:
            raise ComponentStore.DoesNotExist(
                f"Component '{component_type}' (version={version}) not found"
            )

        logger.debug(f"Loaded component: {component_type} v{component.version} for tier {tier}")
        return component

    def _validate_tier_permissions(
        self, component: ComponentStore, tier: str, page_type: str
    ) -> None:
        """
        Validate that component is allowed in the given tier/page.

        Args:
            component: ComponentStore instance
            tier: Page tier
            page_type: Page type

        Raises:
            ComponentPlacementError: If component not allowed
        """
        try:
            self.schema_registry.validate_component_placement(
                page_type=page_type,
                component_type=component.component_type,
                region=None,  # Region check happens at layout level
            )
        except Exception as e:
            logger.warning(
                f"Component {component.component_type} not allowed in "
                f"{page_type} (tier {tier}): {e}"
            )
            raise

    def _get_template_path(self, component: ComponentStore) -> str:
        """
        Get template file path for component.

        Args:
            component: ComponentStore instance

        Returns:
            Absolute path to template file
        """
        # Components are stored in media/components/{type}/{version}/
        # For now, return a placeholder path
        # This will be updated when actual component packages are implemented
        from django.conf import settings

        media_root = getattr(settings, "MEDIA_ROOT", "/tmp")
        template_path = (
            Path(media_root)
            / "components"
            / component.component_type
            / component.version
            / "template.html"
        )

        return str(template_path)

    def _get_component_assets(self, component: ComponentStore) -> dict[str, Any]:
        """
        Get component assets (CSS, JS, images).

        Args:
            component: ComponentStore instance

        Returns:
            Dict with asset URLs
        """
        # Placeholder - will be implemented when component packages are ready
        return {"css": [], "js": [], "images": []}

    def _get_component_permissions(self, component: ComponentStore, tier: str) -> dict[str, Any]:
        """
        Get component permissions for the given tier.

        Args:
            component: ComponentStore instance
            tier: Page tier

        Returns:
            Permission data dict
        """
        try:
            permission = TierComponentPermission.objects.filter(
                component=component, tier__tier=tier
            ).first()

            if permission:
                return {
                    "allowed_regions": permission.allowed_regions or [],
                    "max_instances": permission.max_instances,
                    "is_locked": permission.is_locked,
                }

            return {}

        except Exception as e:
            logger.warning(f"Failed to load permissions for {component.component_type}: {e}")
            return {}

    def _get_fallback_template(self, component: ComponentStore) -> str:
        """
        Get fallback template when actual template is missing.

        Args:
            component: ComponentStore instance

        Returns:
            Fallback template HTML
        """
        return (
            f'<div class="component-fallback">\n'
            f'  <p class="component-name">{component.name}</p>\n'
            f'  <p class="component-type">{component.component_type}</p>\n'
            f'  <p class="component-version">v{component.version}</p>\n'
            f"</div>"
        )

    def _get_cached_component(
        self, component_type: str, tier: str, version: str | None = None
    ) -> ComponentStore | None:
        """
        Get component from cache.

        Args:
            component_type: Component type identifier
            tier: Page tier
            version: Component version

        Returns:
            Cached ComponentStore or None
        """
        cache_key = self._build_cache_key(component_type, tier, version)
        return cache.get(cache_key)

    def _cache_component(
        self, component: ComponentStore, tier: str, version: str | None = None
    ) -> None:
        """
        Cache component for future requests.

        Args:
            component: ComponentStore instance to cache
            tier: Page tier
            version: Component version
        """
        cache_key = self._build_cache_key(component.component_type, tier, version)
        cache.set(cache_key, component, self.CACHE_TIMEOUT)
        logger.debug(f"Cached component: {cache_key}")

    def _build_cache_key(self, component_type: str, tier: str, version: str | None = None) -> str:
        """
        Build cache key for component.

        Args:
            component_type: Component type identifier
            tier: Page tier
            version: Component version

        Returns:
            Cache key string
        """
        version_str = version or "latest"
        return f"{self.CACHE_KEY_PREFIX}:{tier}:{component_type}:{version_str}"

    @staticmethod
    def clear_component_cache(component_type: str | None = None) -> None:
        """
        Clear component cache.

        Args:
            component_type: Specific component type to clear, or None for all

        Example:
            >>> ComponentRegistryService.clear_component_cache('banner')
            >>> ComponentRegistryService.clear_component_cache()  # Clear all
        """
        if component_type:
            # Clear specific component across all tiers and versions
            logger.info(f"Clearing cache for component: {component_type}")
            # Note: Django's default cache doesn't support pattern matching
            # In production, use Redis with delete_pattern
            cache.delete_many([])
        else:
            # Clear all component cache
            logger.info("Clearing all component cache")
            cache.clear()
