"""
DRF permission classes for role-based access control.
"""
from rest_framework import permissions

from staff_roles.services import get_pos_permission


class HasPOSPermission(permissions.BasePermission):
    """
    Check POS-specific permission flags from StaffRole.

    Usage:
        @permission_classes([IsStaffUser, HasPOSPermission('pos_refund')])

    Or as a factory:
        permission_classes = [IsStaffUser, pos_permission('pos_refund')]
    """

    def __init__(self, required_permission=None):
        self.required_permission = required_permission

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return bool(get_pos_permission(request.user, self.required_permission))


def pos_permission(permission_key):
    """
    Factory function to create a permission class for a specific POS permission.

    Usage in views:
        @permission_classes([IsStaffUser, pos_permission('pos_refund')])
    """
    class POSPermission(HasPOSPermission):
        def __init__(self):
            super().__init__(required_permission=permission_key)
    POSPermission.__name__ = f'POSPermission_{permission_key}'
    POSPermission.__qualname__ = f'POSPermission_{permission_key}'
    return POSPermission
