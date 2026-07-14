"""
Permission resolution, merge logic, and caching services.
"""

import logging

from django.contrib.auth.models import Permission
from django.core.cache import cache

from staff_roles.categories import PERMISSION_CATEGORIES
from staff_roles.pos_permissions import POS_PERMISSION_FLAGS

logger = logging.getLogger(__name__)

# Cache timeout for merged POS permissions (5 minutes)
POS_PERM_CACHE_TIMEOUT = 300


def resolve_category_permissions(category_settings):
    """
    Resolve a permission_categories dict to a set of Django Permission objects.

    Args:
        category_settings: Dict like {"catalog": "full", "orders": "view", ...}

    Returns:
        Set of Permission objects
    """
    all_perms = set()

    for category_key, access_level in category_settings.items():
        category = PERMISSION_CATEGORIES.get(category_key)
        if not category:
            continue

        perm_strings = []
        if access_level in ("view", "full"):
            perm_strings.extend(category["permissions"]["view"])
        if access_level == "full":
            perm_strings.extend(category["permissions"]["full"])

        for perm_string in perm_strings:
            try:
                app_label, codename = perm_string.split(".")
                perm = Permission.objects.get(
                    content_type__app_label=app_label,
                    codename=codename,
                )
                all_perms.add(perm)
            except Permission.DoesNotExist:
                logger.debug(f"Permission not found: {perm_string}")
            except ValueError:
                logger.warning(f"Invalid permission format: {perm_string}")

    return all_perms


def get_user_roles(user):
    """
    Get all StaffRole objects for a user.

    Args:
        user: Django User instance

    Returns:
        QuerySet of StaffRole objects
    """
    from staff_roles.models import StaffRole

    cache_key = f"user_roles_{user.pk}"
    role_ids = cache.get(cache_key)

    if role_ids is None:
        roles = StaffRole.objects.filter(group__in=user.groups.all()).select_related("group")
        role_ids = list(roles.values_list("id", flat=True))
        cache.set(cache_key, role_ids, timeout=POS_PERM_CACHE_TIMEOUT)
        return roles

    return StaffRole.objects.filter(id__in=role_ids).select_related("group")


def invalidate_user_cache(user):
    """Clear cached permissions for a user."""
    cache.delete(f"user_roles_{user.pk}")
    cache.delete(f"pos_perms_{user.pk}")
    cache.delete(f"admin_access_{user.pk}")
    cache.delete(f"read_only_{user.pk}")


def get_pos_permission(user, permission_key):
    """
    Check if a user has a specific POS permission via any of their roles.

    Uses OR logic: if any role grants the permission, it's granted.
    For integer values (like max discount %), takes the maximum.

    Args:
        user: Django User instance
        permission_key: String key from POS_PERMISSION_FLAGS

    Returns:
        bool or int depending on permission type
    """
    if user.is_superuser:
        flag_def = POS_PERMISSION_FLAGS.get(permission_key, {})
        if flag_def.get("type") == "integer":
            return flag_def.get("max", 100)
        return True

    perms = _get_merged_pos_permissions(user)
    flag_def = POS_PERMISSION_FLAGS.get(permission_key, {})
    default = flag_def.get("default", False)
    return perms.get(permission_key, default)


def _get_merged_pos_permissions(user):
    """
    Get merged POS permissions across all of a user's roles.

    Cached for POS_PERM_CACHE_TIMEOUT seconds.
    """
    cache_key = f"pos_perms_{user.pk}"
    perms = cache.get(cache_key)

    if perms is not None:
        return perms

    perms = {}
    for role in get_user_roles(user):
        for key, value in role.pos_permissions.items():
            flag_def = POS_PERMISSION_FLAGS.get(key, {})
            if flag_def.get("type") == "integer":
                # Take the maximum value across roles
                current = perms.get(key, 0)
                perms[key] = max(current, value) if isinstance(value, (int, float)) else current
            else:
                # OR logic: any role granting = granted
                perms[key] = perms.get(key, False) or bool(value)

    cache.set(cache_key, perms, timeout=POS_PERM_CACHE_TIMEOUT)
    return perms


def get_user_pos_permissions_summary(user):
    """
    Get a complete POS permissions summary for a user.

    Used in POS login response to send permissions to the frontend.

    Returns:
        Dict of permission flags and their values
    """
    if user.is_superuser:
        summary = {}
        for key, flag_def in POS_PERMISSION_FLAGS.items():
            if flag_def.get("type") == "integer":
                summary[key] = flag_def.get("max", 100)
            else:
                summary[key] = True
        return summary

    return _get_merged_pos_permissions(user)


def can_access_admin(user):
    """
    Check if a user can access the admin panel.

    Superusers always can. For other staff, checks if any of their
    roles have can_access_admin=True.
    """
    if user.is_superuser:
        return True

    cache_key = f"admin_access_{user.pk}"
    result = cache.get(cache_key)

    if result is not None:
        return result

    roles = get_user_roles(user)
    result = any(role.can_access_admin for role in roles)

    # If user has no roles at all and is_staff, allow access
    # (backwards compatibility for users not yet assigned roles)
    if not roles.exists() and user.is_staff:
        result = True

    cache.set(cache_key, result, timeout=POS_PERM_CACHE_TIMEOUT)
    return result


def can_access_pos(user):
    """
    Check if a user can access the POS system.

    Superusers always can. For other staff, checks if any of their
    roles have can_access_pos=True.
    """
    if user.is_superuser:
        return True

    roles = get_user_roles(user)
    return any(role.can_access_pos for role in roles)


def is_effectively_read_only(user):
    """
    Determine if a user is effectively read-only across the admin.

    A user is read-only if they are not a superuser, have at least one
    StaffRole assigned, and none of their roles grant 'full' access on
    any permission category.

    Users with no roles are NOT treated as read-only (backwards
    compatibility for merchants who haven't set up roles yet).
    """
    if user.is_superuser:
        return False

    cache_key = f"read_only_{user.pk}"
    result = cache.get(cache_key)
    if result is not None:
        return result

    roles = get_user_roles(user)

    # No roles assigned = not read-only (backwards compat)
    if not roles.exists():
        cache.set(cache_key, False, timeout=POS_PERM_CACHE_TIMEOUT)
        return False

    # Check if ANY role grants "full" on ANY category
    for role in roles:
        for level in role.permission_categories.values():
            if level == "full":
                cache.set(cache_key, False, timeout=POS_PERM_CACHE_TIMEOUT)
                return False

    cache.set(cache_key, True, timeout=POS_PERM_CACHE_TIMEOUT)
    return True


def has_category_access(user, category_key, level="view"):
    """
    Check if a user has at least the specified access level for a permission category.

    Used by template tags to control sidebar visibility.

    Args:
        user: Django User instance
        category_key: Key from PERMISSION_CATEGORIES
        level: 'view' or 'full'

    Returns:
        bool
    """
    if user.is_superuser:
        return True

    for role in get_user_roles(user):
        role_level = role.permission_categories.get(category_key, "none")
        if level == "view" and role_level in ("view", "full"):
            return True
        if level == "full" and role_level == "full":
            return True

    return False
