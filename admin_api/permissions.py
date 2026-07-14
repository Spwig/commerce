"""
Admin API Permissions

Custom permission classes for staff-only mobile app API endpoints.
"""

import secrets

from django.conf import settings as django_settings
from rest_framework import permissions


class IsStaffUser(permissions.BasePermission):
    """
    Permission to only allow staff users to access endpoints.
    All methods require is_staff=True.

    Usage:
        class MyView(APIView):
            permission_classes = [IsStaffUser]
    """

    message = "Staff access required for this endpoint."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_active
            and request.user.is_staff
        )


class IsSuperUser(permissions.BasePermission):
    """
    Permission for superuser-only operations.
    Used for sensitive settings and administrative actions.
    """

    message = "Superuser access required for this endpoint."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_active
            and request.user.is_superuser
        )


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Permission to allow read-only access to authenticated users,
    but require staff status for write operations.
    """

    message = "Staff access required for write operations."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return request.user.is_active

        return request.user.is_active and request.user.is_staff


class IsStaffWithWritePermission(permissions.BasePermission):
    """
    Staff permission that enforces read-only for view-only roles.

    Safe methods (GET, HEAD, OPTIONS) require is_staff.
    Write methods (POST, PUT, PATCH, DELETE) additionally require
    the user to not be effectively read-only (must have at least
    one 'full' permission category in their staff roles).

    Defense-in-depth alongside AdminReadOnlyMiddleware.
    """

    message = "Your account has read-only access. Write operations are not permitted."

    def has_permission(self, request, view):
        if not (
            request.user
            and request.user.is_authenticated
            and request.user.is_active
            and request.user.is_staff
        ):
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_superuser:
            return True

        from staff_roles.services import is_effectively_read_only

        return not is_effectively_read_only(request.user)


def category_permission(category_key, level="view"):
    """
    Factory to create a DRF permission class for category-based access control.

    Uses the staff_roles permission system to check if a user has the required
    access level for a given permission category.

    Args:
        category_key: Key from PERMISSION_CATEGORIES (e.g. 'catalog', 'orders', 'users')
        level: 'view' or 'full'

    Returns:
        A DRF BasePermission subclass

    Usage:
        @permission_classes([category_permission('orders', 'full')])
        def my_write_view(request): ...

        @permission_classes([category_permission('catalog', 'view')])
        def my_read_view(request): ...
    """

    class CategoryPermission(permissions.BasePermission):
        message = f"You do not have {level} access to {category_key}."

        def has_permission(self, request, view):
            if not (
                request.user
                and request.user.is_authenticated
                and request.user.is_active
                and request.user.is_staff
            ):
                return False

            if request.user.is_superuser:
                return True

            from staff_roles.services import has_category_access

            return has_category_access(request.user, category_key, level)

    CategoryPermission.__name__ = f"Has_{category_key}_{level}"
    CategoryPermission.__qualname__ = f"Has_{category_key}_{level}"
    return CategoryPermission


class HasMobileAppKey(permissions.BasePermission):
    """
    Verify X-Spwig-App-Key header for pre-auth mobile endpoints.

    When MOBILE_APP_API_KEY is configured in MOBILE_API_SETTINGS,
    requests must include a matching X-Spwig-App-Key header.
    If the key is not configured (empty/missing), all requests are allowed.
    """

    message = "Invalid or missing app key."

    def has_permission(self, request, view):
        mobile_settings = getattr(django_settings, "MOBILE_API_SETTINGS", {})
        app_key = mobile_settings.get("MOBILE_APP_API_KEY", "")
        if not app_key:
            return True
        request_key = request.META.get("HTTP_X_SPWIG_APP_KEY", "")
        if not request_key:
            return False
        return secrets.compare_digest(request_key, app_key)
