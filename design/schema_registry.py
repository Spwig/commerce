"""
Page Schema Registry

This module provides runtime schema validation and enforcement of tier-based
security rules for page layouts and component placement.

The PageSchemaRegistry:
- Loads and caches page tier configurations
- Validates component placement against tier rules
- Enforces locked regions (cannot be modified by themes)
- Checks component whitelist permissions
- Validates CSP policy compliance
"""

from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db.models import Prefetch

from .models import ComponentStore, PageTier, TierComponentPermission


class SchemaValidationError(ValidationError):
    """Raised when schema validation fails"""

    pass


class ComponentPlacementError(SchemaValidationError):
    """Raised when component cannot be placed in requested location"""

    pass


class LockedRegionError(SchemaValidationError):
    """Raised when attempting to modify a locked region"""

    pass


class PageSchemaRegistry:
    """
    Central registry for page schemas and tier-based security enforcement.

    This class provides:
    - Schema loading and caching
    - Component placement validation
    - Tier security enforcement
    - Locked region protection

    Example:
        >>> registry = PageSchemaRegistry()
        >>> registry.validate_component_placement(
        ...     page_type='checkout',
        ...     component_type='custom_banner',
        ...     region='header'
        ... )
        ComponentPlacementError: Component 'custom_banner' not allowed in Tier A page
    """

    # Cache timeout for schema data (5 minutes)
    CACHE_TIMEOUT = 300
    CACHE_KEY_PREFIX = "page_schema_registry"

    def __init__(self):
        """Initialize the schema registry."""
        self._schema_cache: dict[str, PageTier] = {}

    def get_page_tier(self, page_type: str) -> PageTier | None:
        """
        Get PageTier configuration for a specific page type.

        Args:
            page_type: The page type identifier (e.g., 'checkout', 'product')

        Returns:
            PageTier instance or None if not found

        Example:
            >>> tier = registry.get_page_tier('checkout')
            >>> tier.tier
            'A'
        """
        cache_key = f"{self.CACHE_KEY_PREFIX}:tier:{page_type}"

        # Try cache first
        cached = cache.get(cache_key)
        if cached:
            return cached

        # Load from database
        try:
            tier = PageTier.objects.prefetch_related(
                Prefetch(
                    "component_permissions",
                    queryset=TierComponentPermission.objects.select_related("component"),
                )
            ).get(page_type=page_type)

            # Cache for future requests
            cache.set(cache_key, tier, self.CACHE_TIMEOUT)
            return tier

        except PageTier.DoesNotExist:
            return None

    def get_allowed_components(self, page_type: str) -> list[ComponentStore]:
        """
        Get list of components allowed on a specific page type.

        Args:
            page_type: The page type identifier

        Returns:
            List of ComponentStore instances allowed on this page

        Example:
            >>> components = registry.get_allowed_components('product')
            >>> [c.component_type for c in components]
            ['hero_banner', 'product_gallery', 'reviews_widget']
        """
        tier = self.get_page_tier(page_type)
        if not tier:
            return []

        cache_key = f"{self.CACHE_KEY_PREFIX}:components:{page_type}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        # Get components from tier permissions
        permissions = (
            TierComponentPermission.objects.filter(tier=tier)
            .select_related("component")
            .filter(component__review_status="approved")
        )

        components = [perm.component for perm in permissions]
        cache.set(cache_key, components, self.CACHE_TIMEOUT)
        return components

    def get_allowed_regions(self, page_type: str, component_type: str) -> list[str]:
        """
        Get list of regions where a component can be placed.

        Args:
            page_type: The page type identifier
            component_type: The component type identifier

        Returns:
            List of region IDs where component is allowed

        Example:
            >>> regions = registry.get_allowed_regions('product', 'hero_banner')
            >>> regions
            ['hero', 'main']
        """
        tier = self.get_page_tier(page_type)
        if not tier:
            return []

        try:
            permission = TierComponentPermission.objects.select_related("component").get(
                tier=tier, component__component_type=component_type
            )
            return permission.allowed_regions
        except TierComponentPermission.DoesNotExist:
            return []

    def is_region_locked(self, page_type: str, region: str) -> bool:
        """
        Check if a region is locked (cannot be modified by themes).

        Args:
            page_type: The page type identifier
            region: The region identifier

        Returns:
            True if region is locked, False otherwise

        Example:
            >>> registry.is_region_locked('checkout', 'payment_form')
            True
        """
        tier = self.get_page_tier(page_type)
        if not tier:
            return False

        return region in tier.locked_regions

    def validate_component_placement(
        self, page_type: str, component_type: str, region: str, instance_count: int = 1
    ) -> tuple[bool, str | None]:
        """
        Validate if a component can be placed in a specific region.

        Checks:
        1. Page tier exists
        2. Region is not locked
        3. Component is allowed on this tier
        4. Component is allowed in this region
        5. Instance count doesn't exceed max_instances

        Args:
            page_type: The page type identifier
            component_type: The component type identifier
            region: The region identifier
            instance_count: Number of instances to place (default: 1)

        Returns:
            Tuple of (is_valid, error_message)

        Example:
            >>> valid, error = registry.validate_component_placement(
            ...     'checkout', 'custom_banner', 'header'
            ... )
            >>> valid
            False
            >>> error
            'Component not allowed in Tier A pages'
        """
        # Check if page tier exists
        tier = self.get_page_tier(page_type)
        if not tier:
            return False, f"Page type '{page_type}' not found in registry"

        # Check if region is locked
        if self.is_region_locked(page_type, region):
            return False, f"Region '{region}' is locked and cannot be modified"

        # Get component permission
        try:
            permission = TierComponentPermission.objects.select_related("component", "tier").get(
                tier=tier,
                component__component_type=component_type,
                component__review_status="approved",
            )
        except TierComponentPermission.DoesNotExist:
            return False, f"Component '{component_type}' not allowed in Tier {tier.tier} pages"

        # Check if component is allowed in this region
        # Empty allowed_regions means all regions are allowed
        if permission.allowed_regions and region not in permission.allowed_regions:
            allowed = ", ".join(permission.allowed_regions)
            return False, (
                f"Component '{component_type}' not allowed in region '{region}'. "
                f"Allowed regions: {allowed}"
            )

        # Check instance count limit
        if permission.max_instances >= 0 and instance_count > permission.max_instances:
            return False, (
                f"Component '{component_type}' exceeds max instances "
                f"({instance_count} > {permission.max_instances})"
            )

        return True, None

    def validate_page_schema(self, page_type: str, layout_data: dict) -> tuple[bool, list[str]]:
        """
        Validate an entire page layout against tier rules.

        Args:
            page_type: The page type identifier
            layout_data: Dictionary containing page layout structure
                Format: {
                    'regions': {
                        'header': [
                            {'component': 'logo', 'config': {...}},
                            {'component': 'nav', 'config': {...}}
                        ],
                        'main': [...]
                    }
                }

        Returns:
            Tuple of (is_valid, list_of_errors)

        Example:
            >>> layout = {
            ...     'regions': {
            ...         'header': [{'component': 'custom_banner'}],
            ...         'main': [{'component': 'product_grid'}]
            ...     }
            ... }
            >>> valid, errors = registry.validate_page_schema('checkout', layout)
            >>> valid
            False
            >>> errors
            ['Component custom_banner not allowed in Tier A pages']
        """
        errors = []

        # Get page tier
        tier = self.get_page_tier(page_type)
        if not tier:
            return False, [f"Page type '{page_type}' not found"]

        # Validate structure
        if "regions" not in layout_data:
            return False, ["Layout data must contain 'regions' key"]

        regions = layout_data["regions"]
        if not isinstance(regions, dict):
            return False, ["'regions' must be a dictionary"]

        # Track component instances for max_instances validation
        component_counts: dict[str, int] = {}

        # Validate each region
        for region_id, components in regions.items():
            # Check if region is locked
            if self.is_region_locked(page_type, region_id):
                errors.append(f"Region '{region_id}' is locked and cannot be modified")
                continue

            if not isinstance(components, list):
                errors.append(f"Region '{region_id}' must contain a list of components")
                continue

            # Validate each component in region
            for component_data in components:
                if not isinstance(component_data, dict):
                    errors.append(f"Component in region '{region_id}' must be a dictionary")
                    continue

                component_type = component_data.get("component")
                if not component_type:
                    errors.append(f"Component in region '{region_id}' missing 'component' field")
                    continue

                # Track instance count
                component_counts[component_type] = component_counts.get(component_type, 0) + 1

                # Validate placement
                valid, error = self.validate_component_placement(
                    page_type=page_type,
                    component_type=component_type,
                    region=region_id,
                    instance_count=component_counts[component_type],
                )

                if not valid:
                    errors.append(error)

        return len(errors) == 0, errors

    def get_schema_for_page(self, page_type: str) -> dict:
        """
        Get the full schema definition for a page type.

        Args:
            page_type: The page type identifier

        Returns:
            Dictionary containing schema, tier info, and allowed components

        Example:
            >>> schema = registry.get_schema_for_page('product')
            >>> schema['tier']
            'B'
            >>> schema['locked_regions']
            ['checkout_button']
        """
        tier = self.get_page_tier(page_type)
        if not tier:
            return {}

        allowed_components = self.get_allowed_components(page_type)

        return {
            "page_type": page_type,
            "tier": tier.tier,
            "tier_name": tier.get_tier_display(),
            "display_name": tier.display_name,
            "description": tier.description,
            "schema": tier.schema,
            "locked_regions": tier.locked_regions,
            "csp_policy": tier.csp_policy,
            "max_external_scripts": tier.max_external_scripts,
            "allows_custom_html": tier.allows_custom_html,
            "allowed_components": [
                {
                    "component_type": c.component_type,
                    "display_name": c.display_name,
                    "render_mode": c.render_mode,
                    "capabilities": c.capabilities,
                }
                for c in allowed_components
            ],
        }

    def clear_cache(self, page_type: str | None = None):
        """
        Clear cached schema data.

        Args:
            page_type: Specific page type to clear, or None to clear all

        Example:
            >>> registry.clear_cache('checkout')  # Clear specific page
            >>> registry.clear_cache()  # Clear all cached schemas
        """
        if page_type:
            cache.delete(f"{self.CACHE_KEY_PREFIX}:tier:{page_type}")
            cache.delete(f"{self.CACHE_KEY_PREFIX}:components:{page_type}")
        else:
            # Clear all schema-related cache keys
            cache.delete_pattern(f"{self.CACHE_KEY_PREFIX}:*")


# Singleton instance for global access
_registry_instance: PageSchemaRegistry | None = None


def get_schema_registry() -> PageSchemaRegistry:
    """
    Get the global PageSchemaRegistry instance.

    Returns:
        The singleton PageSchemaRegistry instance

    Example:
        >>> from design.schema_registry import get_schema_registry
        >>> registry = get_schema_registry()
        >>> registry.get_page_tier('checkout')
    """
    global _registry_instance
    if _registry_instance is None:
        _registry_instance = PageSchemaRegistry()
    return _registry_instance
