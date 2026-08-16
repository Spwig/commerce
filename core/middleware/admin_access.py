"""
Admin Access Control Middleware

Prevents POS-only staff (and any staff without admin-access roles) from
accessing the Django admin panel.

Rules (deny-by-default):
- Superusers always pass
- Staff with at least one role that has can_access_admin=True pass
- Staff with NO roles assigned are denied — they must be given a role
- Staff whose only roles have can_access_admin=False get redirected
- Non-staff users are handled by Django's built-in admin auth
"""

import logging
import re

from django.contrib import messages
from django.contrib.messages.storage import default_storage
from django.shortcuts import redirect
from django.utils.translation import gettext as _

logger = logging.getLogger(__name__)

# Match admin paths with or without language prefix
# e.g. /admin/, /en/admin/, /de/admin/login/
ADMIN_PATH_RE = re.compile(r"^(/[a-z]{2})?/admin/")


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
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated or not user.is_staff:
            return self.get_response(request)

        # Superusers always have access
        if user.is_superuser:
            return self.get_response(request)

        # Allow the admin login/logout pages themselves
        if "/admin/login/" in request.path or "/admin/logout/" in request.path:
            return self.get_response(request)

        # Check role-based admin access
        from staff_roles.services import can_access_admin

        if not can_access_admin(user):
            # This middleware runs before MessageMiddleware, so request._messages
            # isn't set up yet — and returning the redirect here short-circuits
            # MessageMiddleware entirely, so it never gets to persist a message
            # either. Build a fresh storage and write the message onto the
            # redirect ourselves: the denied user still gets the explanation on
            # the storefront, with no MessageFailure 500.
            response = redirect("/")
            storage = default_storage(request)
            storage.add(
                messages.ERROR,
                _(
                    "Your account doesn't have admin access yet. "
                    "Ask your store owner to assign you a staff role."
                ),
            )
            storage.update(response)
            return response

        return self.get_response(request)
