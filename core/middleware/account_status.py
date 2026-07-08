"""
Account Status Enforcement Middleware (Spwig-Hosted Only)

For Spwig-hosted installations, enforces restrictions based on account_status:
- suspended / read_only: blocks write operations (POST, PUT, PATCH, DELETE)
  on admin panel and admin API URLs
- cancelled: redirects ALL admin requests to login with an error message

Self-hosted installations pass through unconditionally.

Modelled on AdminReadOnlyMiddleware — uses the same path patterns, write method
set, and whitelisted paths for login/logout/password change/allauth/jsi18n.
"""
import logging
import re

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.translation import gettext as _

logger = logging.getLogger(__name__)

# Match admin panel paths with optional language prefix
ADMIN_PATH_RE = re.compile(r'^(/[a-z]{2}(-[a-z]+)?)?/admin/')

# Match admin API paths
ADMIN_API_PATH_RE = re.compile(r'^/api/admin/')

WRITE_METHODS = frozenset({'POST', 'PUT', 'PATCH', 'DELETE'})

# Statuses that block write operations but allow read access
READ_ONLY_STATUSES = frozenset({'suspended', 'read_only'})

# Statuses that block all admin access
LOCKOUT_STATUSES = frozenset({'cancelled'})

# Path suffixes (after stripping language prefix) that always allow through.
WHITELISTED_SUFFIXES = (
    '/admin/login/',
    '/admin/logout/',
    '/admin/jsi18n/',
)

WHITELISTED_PATTERNS = (
    '/i18n/setlang/',
)

WHITELISTED_REGEXES = [
    re.compile(r'^(/[a-z]{2}(-[a-z]+)?)?/admin/password_change/'),
    re.compile(r'^(/[a-z]{2}(-[a-z]+)?)?/accounts/'),
]


class AccountStatusMiddleware:
    """
    Enforce account status restrictions for Spwig-hosted installations.

    Must be placed after AdminReadOnlyMiddleware in the MIDDLEWARE list.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        is_admin_panel = bool(ADMIN_PATH_RE.match(path))
        is_admin_api = bool(ADMIN_API_PATH_RE.match(path))

        # Only applies to admin paths
        if not is_admin_panel and not is_admin_api:
            return self.get_response(request)

        # Only applies to authenticated staff
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated or not user.is_staff:
            return self.get_response(request)

        # Only applies to Spwig-hosted installations
        from core.license import get_license_manager
        lm = get_license_manager()
        if not lm.is_spwig_hosted():
            return self.get_response(request)

        account_status = lm.get_account_status()

        # Active, past_due, grace_period — no enforcement
        if account_status not in READ_ONLY_STATUSES and account_status not in LOCKOUT_STATUSES:
            return self.get_response(request)

        # Always allow whitelisted paths (login, logout, password change, etc.)
        if self._is_whitelisted(path):
            return self.get_response(request)

        # --- Cancelled: block ALL admin access ---
        if account_status in LOCKOUT_STATUSES:
            logger.info(
                "Account lockout: blocked %s %s for user %s (status=%s)",
                request.method, path, user.username, account_status,
            )

            if is_admin_api:
                return JsonResponse(
                    {
                        'success': False,
                        'error': 'account_cancelled',
                        'message': str(_(
                            'Your subscription has been cancelled. '
                            'Please visit your account page to restore access.'
                        )),
                    },
                    status=403,
                )

            messages.error(
                request,
                _(
                    'Your subscription has been cancelled. '
                    'Please visit your account page to restore access.'
                ),
            )
            # Redirect to login — stripped path to get the language-aware login URL
            stripped = re.sub(r'^(/[a-z]{2}(-[a-z]+)?)', '', path)
            lang_prefix = path[:len(path) - len(stripped)] if stripped != path else ''
            return redirect(f'{lang_prefix}/admin/login/')

        # --- Suspended / Read-Only: block write operations only ---
        if account_status in READ_ONLY_STATUSES and request.method in WRITE_METHODS:
            logger.info(
                "Account read-only: blocked %s %s for user %s (status=%s)",
                request.method, path, user.username, account_status,
            )

            if is_admin_api:
                return JsonResponse(
                    {
                        'success': False,
                        'error': 'account_suspended',
                        'message': str(_(
                            'Your account is currently suspended. '
                            'Write operations are not permitted.'
                        )),
                    },
                    status=403,
                )

            messages.warning(
                request,
                _(
                    'Your account is currently suspended. '
                    'This action is not available until your account is restored.'
                ),
            )
            referer = request.META.get('HTTP_REFERER', '')
            if referer and request.get_host() in referer:
                return redirect(referer)
            return redirect(request.path)

        return self.get_response(request)

    def _is_whitelisted(self, path):
        """Check if a path is whitelisted for all operations."""
        stripped = re.sub(r'^/[a-z]{2}(-[a-z]+)?(?=/)', '', path)

        for suffix in WHITELISTED_SUFFIXES:
            if stripped.startswith(suffix):
                return True

        for pattern in WHITELISTED_PATTERNS:
            if path == pattern or stripped == pattern:
                return True

        for regex in WHITELISTED_REGEXES:
            if regex.match(path):
                return True

        return False
