"""
Admin Access Control Middleware

Prevents POS-only staff (and any staff without admin-access roles) from
accessing the Django admin panel.

Rules:
- Superusers always pass
- Staff with at least one role that has can_access_admin=True pass
- Staff with NO roles assigned pass (backwards compatibility)
- Staff whose only roles have can_access_admin=False get redirected
- Non-staff users are handled by Django's built-in admin auth
"""
import logging
import re

from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext as _

logger = logging.getLogger(__name__)

# Match admin paths with or without language prefix
# e.g. /admin/, /en/admin/, /de/admin/login/
ADMIN_PATH_RE = re.compile(r'^(/[a-z]{2})?/admin/')


class AdminAccessMiddleware:
    """
    Gate admin panel access based on StaffRole.can_access_admin.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only check admin paths
        if not ADMIN_PATH_RE.match(request.path):
            return self.get_response(request)

        # Only check authenticated staff users
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated or not user.is_staff:
            return self.get_response(request)

        # Superusers always have access
        if user.is_superuser:
            return self.get_response(request)

        # Allow the admin login/logout pages themselves
        if '/admin/login/' in request.path or '/admin/logout/' in request.path:
            return self.get_response(request)

        # Check role-based admin access
        from staff_roles.services import can_access_admin
        if not can_access_admin(user):
            messages.error(
                request,
                _('Your account does not have admin panel access. '
                  'Contact your store owner if you believe this is an error.')
            )
            # Redirect to the storefront home page
            return redirect('/')

        return self.get_response(request)
