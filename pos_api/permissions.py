from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status as http_status
from django.utils.translation import gettext_lazy as _


class IsStaffUser(permissions.BasePermission):
    """
    Only allow staff users to access POS endpoints.
    """
    message = _('POS access requires a staff account.')

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
        )


class IsPOSTerminalUser(permissions.BasePermission):
    """
    Verify that the authenticated user is assigned to the terminal
    making the request (if terminal_uuid is provided).
    """
    message = _('You are not assigned to this terminal.')

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        terminal_uuid = request.headers.get('X-Terminal-UUID')
        if not terminal_uuid:
            # No terminal specified, allow (terminal assignment is optional)
            return True

        from pos_app.models import POSTerminal
        try:
            terminal = POSTerminal.objects.get(uuid=terminal_uuid, is_active=True)
        except POSTerminal.DoesNotExist:
            return False

        # If terminal has assigned users, check membership
        if terminal.assigned_users.exists():
            return terminal.assigned_users.filter(pk=request.user.pk).exists()

        # No user restrictions on this terminal
        return True


def check_pos_permission(request, permission_key):
    """
    Check if the current user has a specific POS permission flag.

    Returns None if allowed, or a Response with 403 error if denied.
    Use in views like:
        err = check_pos_permission(request, 'pos_refund')
        if err:
            return err
    """
    from staff_roles.services import get_pos_permission

    if not get_pos_permission(request.user, permission_key):
        from staff_roles.pos_permissions import POS_PERMISSION_FLAGS
        flag = POS_PERMISSION_FLAGS.get(permission_key, {})
        label = str(flag.get('label', permission_key))
        return Response(
            {
                'success': False,
                'error': {
                    'code': 'PERMISSION_DENIED',
                    'message': str(_('You do not have permission: %(label)s.') % {'label': label}),
                },
            },
            status=http_status.HTTP_403_FORBIDDEN,
        )
    return None
