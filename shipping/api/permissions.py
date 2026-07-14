"""
Shipping API Permissions
Custom permission classes for API endpoints
"""

from rest_framework import permissions


class IsShipmentOwner(permissions.BasePermission):
    """
    Permission to only allow owners of a shipment to view/edit it.
    Checks if shipment.order.user == request.user or user is staff.
    """

    def has_object_permission(self, request, view, obj):
        """Check if user owns the shipment"""
        # Staff can access all shipments
        if request.user and request.user.is_staff:
            return True

        # Check if shipment belongs to user's order
        if hasattr(obj, "order") and obj.order:
            return obj.order.user == request.user

        # Check if shipment.user matches (fallback)
        if hasattr(obj, "user"):
            return obj.user == request.user

        return False


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Permission to only allow staff to modify objects.
    Read permissions are allowed to authenticated users.
    """

    def has_permission(self, request, view):
        """Check permission at view level"""
        # Read permissions (GET, HEAD, OPTIONS) for authenticated users
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        # Write permissions only for staff
        return request.user and request.user.is_staff


class IsProviderOwner(permissions.BasePermission):
    """
    Permission to only allow owners of a provider account to access it.
    Staff can access all provider accounts.
    """

    def has_object_permission(self, request, view, obj):
        """Check if user owns the provider account"""
        # Staff can access all provider accounts
        if request.user and request.user.is_staff:
            return True

        # Check if provider account belongs to user
        if hasattr(obj, "user"):
            return obj.user == request.user

        return False


class IsAuthenticatedOrStaffReadOnly(permissions.BasePermission):
    """
    Authenticated users can read, only staff can write.
    """

    def has_permission(self, request, view):
        """Check permission at view level"""
        if not request.user or not request.user.is_authenticated:
            return False

        # Safe methods allowed for authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True

        # Unsafe methods only for staff
        return request.user.is_staff
