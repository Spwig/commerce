"""
Admin Read-Only Enforcement Middleware

Blocks write operations (POST, PUT, PATCH, DELETE) on admin panel and
admin API URLs for staff users who are effectively read-only -- i.e.
all of their StaffRole permission categories are set to 'view' or 'none',
with no 'full' access on any category.

Returns a friendly JSON 403 for API requests and redirects with a Django
message for HTML admin requests.

Whitelisted paths (always allowed even for read-only users):
- Login / logout (authentication must work)
- Password change (security action)
- Language switching (user preference)
- Allauth / MFA flows
- Django admin jsi18n
"""

import logging
import re

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.translation import gettext as _

logger = logging.getLogger(__name__)

# Match admin panel paths with optional language prefix
# e.g. /admin/, /en/admin/, /de/admin/orders/order/1/change/
ADMIN_PATH_RE = re.compile(r"^(/[a-z]{2}(-[a-z]+)?)?/admin/")

# Match admin API paths
ADMIN_API_PATH_RE = re.compile(r"^/api/admin/")

WRITE_METHODS = frozenset({"POST", "PUT", "PATCH", "DELETE"})

# Path suffixes (after stripping language prefix) that always allow POST.
# These are essential operations that don't modify business data.
WHITELISTED_SUFFIXES = (
    "/admin/login/",
    "/admin/logout/",
    "/admin/jsi18n/",
)

# Full path patterns that always allow POST (no language prefix).
WHITELISTED_PATTERNS = ("/i18n/setlang/",)

# Regex patterns for more complex whitelisted paths.
WHITELISTED_REGEXES = [
    re.compile(r"^(/[a-z]{2}(-[a-z]+)?)?/admin/password_change/"),
    re.compile(r"^(/[a-z]{2}(-[a-z]+)?)?/accounts/"),
]


class AdminReadOnlyMiddleware:
    """
    Block write operations for effectively read-only admin users.

    Must be placed after AdminAccessMiddleware in the MIDDLEWARE list
    so that users who can't access admin at all are already redirected.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method not in WRITE_METHODS:
            return self.get_response(request)

        path = request.path
        is_admin_panel = bool(ADMIN_PATH_RE.match(path))
        is_admin_api = bool(ADMIN_API_PATH_RE.match(path))

        if not is_admin_panel and not is_admin_api:
            return self.get_response(request)

        user = getattr(request, "user", None)
        if not user or not user.is_authenticated or not user.is_staff:
            return self.get_response(request)

        if user.is_superuser:
            return self.get_response(request)

        # Check whitelist before the permission check
        if self._is_whitelisted(path):
            return self.get_response(request)

        from staff_roles.services import is_effectively_read_only

        if not is_effectively_read_only(user):
            return self.get_response(request)

        # Block the write operation
        logger.info(
            "Read-only enforcement: blocked %s %s for user %s (pk=%s)",
            request.method,
            path,
            user.username,
            user.pk,
        )

        if is_admin_api:
            return JsonResponse(
                {
                    "success": False,
                    "error": "read_only",
                    "message": str(
                        _("Your account has read-only access. Write operations are not permitted.")
                    ),
                },
                status=403,
            )

        # HTML admin -- redirect back with a message
        messages.warning(
            request,
            _("Your account has read-only access. This action is not available in read-only mode."),
        )
        referer = request.META.get("HTTP_REFERER", "")
        if referer and request.get_host() in referer:
            return redirect(referer)
        return redirect(request.path)

    def _is_whitelisted(self, path):
        """Check if a path is whitelisted for write operations."""
        # Strip language prefix for suffix matching
        stripped = re.sub(r"^/[a-z]{2}(-[a-z]+)?(?=/)", "", path)

        for suffix in WHITELISTED_SUFFIXES:
            if stripped.startswith(suffix):
                return True

        for pattern in WHITELISTED_PATTERNS:
            if path == pattern or stripped == pattern:
                return True

        return any(regex.match(path) for regex in WHITELISTED_REGEXES)
