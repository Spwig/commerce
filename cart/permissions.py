"""
Custom permissions for cart and checkout operations.
"""
from rest_framework import permissions
from core.utils import allows_guest_checkout


class IsAuthenticatedOrGuestCheckoutAllowed(permissions.BasePermission):
    """
    Permission class that allows:
    - All authenticated users
    - Unauthenticated users only if guest checkout is enabled in site settings

    Used by CheckoutViewSet to conditionally allow guest checkout based on merchant configuration.
    """

    def has_permission(self, request, view):
        # Always allow authenticated users
        if request.user and request.user.is_authenticated:
            return True

        # For unauthenticated users, check if guest checkout is allowed
        if allows_guest_checkout():
            return True

        # Deny access if guest checkout is disabled
        return False

    message = "Please log in or create an account to checkout."
