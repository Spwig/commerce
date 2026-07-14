"""
Component permission templates.

Preset permission configurations for common scenarios:
- System components (allowed in all tiers)
- Marketing components (Tier C only)
- Product components (Tier B, C)
- Checkout components (Tier A only)
- Content components (all tiers)

These templates can be applied to components to quickly configure
tier-based access without manually creating permissions for each tier.

Usage:
    from design.component_permissions import apply_permission_template

    # Apply system component permissions (all tiers)
    apply_permission_template(component, 'system')

    # Apply marketing component permissions (Tier C only)
    apply_permission_template(component, 'marketing')
"""

from django.utils.translation import gettext_lazy as _

from .models import ComponentStore, PageTier, TierComponentPermission

# Permission template definitions
PERMISSION_TEMPLATES = {
    "system": {
        "description": _("System components - allowed in all tiers"),
        "allowed_tiers": ["A", "B", "C"],
        "allowed_regions": [],  # All regions
        "max_instances": -1,  # Unlimited
    },
    "marketing": {
        "description": _("Marketing components - Tier C only (public pages)"),
        "allowed_tiers": ["C"],
        "allowed_regions": [],
        "max_instances": -1,
    },
    "product": {
        "description": _("Product components - Tier B and C"),
        "allowed_tiers": ["B", "C"],
        "allowed_regions": [],
        "max_instances": -1,
    },
    "checkout": {
        "description": _("Checkout components - Tier A only (secure pages)"),
        "allowed_tiers": ["A"],
        "allowed_regions": [],
        "max_instances": 1,  # Usually only one per page
    },
    "content": {
        "description": _("Content components - all tiers"),
        "allowed_tiers": ["A", "B", "C"],
        "allowed_regions": [],
        "max_instances": -1,
    },
    "restricted": {
        "description": _("Restricted components - Tier A and B only"),
        "allowed_tiers": ["A", "B"],
        "allowed_regions": [],
        "max_instances": -1,
    },
}


def apply_permission_template(
    component: ComponentStore, template_name: str, override_settings: dict = None
) -> list[TierComponentPermission]:
    """
    Apply a permission template to a component.

    Creates TierComponentPermission records for the component based on
    the specified template.

    Args:
        component: ComponentStore instance
        template_name: Name of template to apply
        override_settings: Optional dict to override template settings

    Returns:
        List of created TierComponentPermission instances

    Example:
        >>> component = ComponentStore.objects.get(component_type='hero_banner')
        >>> permissions = apply_permission_template(component, 'marketing')
        >>> len(permissions)
        1  # Created permission for Tier C

    Raises:
        ValueError: If template_name is invalid
    """
    if template_name not in PERMISSION_TEMPLATES:
        raise ValueError(
            f"Invalid template: {template_name}. "
            f"Available: {', '.join(PERMISSION_TEMPLATES.keys())}"
        )

    template = PERMISSION_TEMPLATES[template_name].copy()
    template.pop("description", None)  # Remove description from template

    # Apply overrides
    if override_settings:
        template.update(override_settings)

    # Delete existing permissions
    TierComponentPermission.objects.filter(component=component).delete()

    # Create permissions for each tier
    created_permissions = []
    for tier_id in template["allowed_tiers"]:
        try:
            tier = PageTier.objects.get(tier=tier_id)

            permission = TierComponentPermission.objects.create(
                tier=tier,
                component=component,
                allowed_regions=template["allowed_regions"],
                max_instances=template["max_instances"],
            )
            created_permissions.append(permission)

        except PageTier.DoesNotExist:
            # Skip tier if it doesn't exist
            continue

    return created_permissions


def copy_permissions(
    source_component: ComponentStore, target_component: ComponentStore
) -> list[TierComponentPermission]:
    """
    Copy permissions from one component to another.

    Args:
        source_component: Component to copy permissions from
        target_component: Component to copy permissions to

    Returns:
        List of created TierComponentPermission instances

    Example:
        >>> source = ComponentStore.objects.get(component_type='hero_banner')
        >>> target = ComponentStore.objects.get(component_type='hero_banner_v2')
        >>> permissions = copy_permissions(source, target)
    """
    # Delete existing permissions on target
    TierComponentPermission.objects.filter(component=target_component).delete()

    # Copy permissions from source
    created_permissions = []
    for source_perm in source_component.tier_permissions.all():
        new_perm = TierComponentPermission.objects.create(
            tier=source_perm.tier,
            component=target_component,
            allowed_regions=source_perm.allowed_regions,
            max_instances=source_perm.max_instances,
        )
        created_permissions.append(new_perm)

    return created_permissions


def get_available_templates() -> dict[str, str]:
    """
    Get list of available permission templates.

    Returns:
        Dict mapping template names to descriptions
    """
    return {name: str(config["description"]) for name, config in PERMISSION_TEMPLATES.items()}


def remove_all_permissions(component: ComponentStore) -> int:
    """
    Remove all tier permissions from a component.

    Args:
        component: ComponentStore instance

    Returns:
        Number of permissions deleted
    """
    deleted_count, _ = TierComponentPermission.objects.filter(component=component).delete()

    return deleted_count


def get_permission_summary(component: ComponentStore) -> dict:
    """
    Get summary of component's tier permissions.

    Args:
        component: ComponentStore instance

    Returns:
        Dict with permission summary

    Example:
        >>> component = ComponentStore.objects.get(component_type='hero_banner')
        >>> summary = get_permission_summary(component)
        >>> summary['tier_count']
        3
        >>> summary['allowed_tiers']
        ['A', 'B', 'C']
    """
    permissions = component.tier_permissions.all()

    return {
        "tier_count": permissions.count(),
        "allowed_tiers": sorted([p.tier.tier for p in permissions]),
        "has_restrictions": any(p.allowed_regions or p.max_instances != -1 for p in permissions),
    }
