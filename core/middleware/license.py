"""
License Enforcement Middleware

Progressive enforcement based on license status and grace period:

- Licensed:       No restrictions
- Grace Period:    Sandbox mode (test payments only via SandboxPaymentGuard)
- Warning Phase:   Same as grace but non-dismissible admin banner
- Full Lockout:    Storefront down, admin restricted to license page only
- Trial Expired:   Auto-converts to dev license (sandbox mode, never locks out)
"""

import logging

from django.contrib import messages
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import gettext as _

from core.license import get_license_manager
from core.license_grace import get_grace_period_status

logger = logging.getLogger(__name__)


class LicenseEnforcementMiddleware(MiddlewareMixin):
    """
    Enforce license restrictions with progressive lockout.

    Modes:
    1. Licensed - pass through, no restrictions
    2. Grace period (days 0-14) - sandbox mode, sandbox banners shown
    3. Warning phase (days 15-21) - same as grace, more urgent banners
    4. Full lockout (day 22+) - storefront blocked, admin restricted
    5. Trial expired - auto-converts to dev, sandbox mode (never locks out)
    """

    # Always allowed regardless of license state
    ALWAYS_ALLOWED = (
        "/static/",
        "/media/",
        "/health/",
        "/license/",
        "/activate/",
        "/__debug__/",
        "/api/sandbox/tamper-report/",
        "/i18n/",
    )

    # Admin paths allowed during full lockout
    ADMIN_ALLOWED_LOCKOUT = (
        "/admin/login/",
        "/admin/logout/",
        "/admin/core/licensestatus/",
        "/admin/jsi18n/",
        "/admin/password_change/",
    )

    # Webhook paths allowed even during lockout (prevent breaking integrations)
    WEBHOOK_PATHS = ("/webhooks/",)

    # Cache key for trial auto-convert attempt (prevent repeated calls)
    TRIAL_CONVERT_CACHE_KEY = "trial_auto_convert_attempted"
    TRIAL_CONVERT_CACHE_TTL = 3600  # Try once per hour

    def process_request(self, request):
        """Check license and enforce restrictions."""
        path = request.path
        stripped = self._strip_language_prefix(path)

        # Always allow certain paths
        if self._is_always_allowed(path, stripped):
            return None

        # Check license
        license_manager = get_license_manager()
        if license_manager.is_valid():
            return None  # Licensed - pass through

        # License is invalid - check if it's an expired trial
        if self._is_expired_trial(license_manager):
            # Expired trials never lock out - they run in sandbox mode
            # Attempt auto-convert to dev license in the background
            self._attempt_trial_to_dev_conversion(license_manager)
            return None  # Allow through in sandbox mode

        # Not licensed and not a trial - check grace period status
        grace = get_grace_period_status()

        if grace.is_locked_out:
            return self._enforce_lockout(request, path, stripped)

        # Grace period or warning phase - sandbox mode
        # Payment endpoints are accessible (SandboxPaymentGuard enforces test-only credentials)
        # No path restrictions in grace/warning mode
        return None

    def _is_expired_trial(self, license_manager):
        """Check if the current license is an expired trial."""
        license_data = license_manager.get_license_data()
        if not license_data:
            return False
        license_info = license_data.get("license", {})
        return license_info.get("license_type") == "trial"

    def _attempt_trial_to_dev_conversion(self, license_manager):
        """
        Attempt to convert an expired trial to a dev license via phone-home.

        Only tries once per hour to avoid hammering the update server.
        On success, reloads the license manager with the new dev license data.
        """
        if cache.get(self.TRIAL_CONVERT_CACHE_KEY):
            return  # Already attempted recently

        cache.set(self.TRIAL_CONVERT_CACHE_KEY, True, self.TRIAL_CONVERT_CACHE_TTL)

        try:
            from core.license_convert import attempt_trial_to_dev_conversion

            attempt_trial_to_dev_conversion()
        except Exception as e:
            logger.warning(f"Trial-to-dev conversion attempt failed: {e}")

    def process_template_response(self, request, response):
        """Add license info to template context for admin pages."""
        if hasattr(response, "context_data") and response.context_data is not None:
            license_manager = get_license_manager()
            response.context_data["license_info"] = license_manager.get_license_info()
            response.context_data["is_licensed"] = license_manager.is_valid()
            response.context_data["trial_mode"] = not license_manager.is_valid()
            response.context_data["maintenance_status"] = license_manager.get_maintenance_status()

        return response

    def _strip_language_prefix(self, path):
        """Strip /en/, /de/ etc. from path."""
        if len(path) > 3 and path[3] == "/" and path[1:3].isalpha():
            return path[3:]
        # Also handle longer codes like /zh-hans/
        if len(path) > 4 and path[0] == "/":
            parts = path.split("/", 2)
            if len(parts) >= 3 and 2 <= len(parts[1]) <= 7:
                candidate = "/" + parts[2] if parts[2] else "/"
                return candidate
        return path

    def _is_always_allowed(self, path, stripped):
        """Check if path is always allowed regardless of license state."""
        for allowed in self.ALWAYS_ALLOWED:
            if path.startswith(allowed) or stripped.startswith(allowed):
                return True
        return False

    def _is_admin_allowed_lockout(self, stripped):
        """Check if admin path is allowed during lockout."""
        return any(stripped.startswith(allowed) for allowed in self.ADMIN_ALLOWED_LOCKOUT)

    def _enforce_lockout(self, request, path, stripped):
        """Full lockout: block almost everything."""

        # Allow webhook paths to avoid breaking integrations
        for webhook in self.WEBHOOK_PATHS:
            if path.startswith(webhook) or stripped.startswith(webhook):
                return None

        is_admin = "/admin/" in stripped

        if is_admin:
            return self._lockout_admin(request, stripped)
        elif stripped.startswith("/api/"):
            return self._lockout_api(request)
        else:
            return self._lockout_storefront(request)

    def _lockout_admin(self, request, stripped):
        """Handle admin lockout: redirect to license page."""
        if self._is_admin_allowed_lockout(stripped):
            return None  # Allowed admin path

        # Redirect to license status page with message
        if request.user.is_authenticated:
            try:
                messages.error(
                    request,
                    _(
                        "Your license has expired. Please activate or renew your license to continue using the platform."
                    ),
                )
            except Exception:
                pass  # MessageMiddleware may not have processed yet

        from django.urls import reverse

        license_url = reverse("admin:core_licensestatus_changelist")
        return redirect(license_url)

    def _lockout_api(self, request):
        """Handle API lockout: return 503 JSON."""
        return JsonResponse(
            {
                "error": "license_required",
                "message": "Platform license has expired. Contact the store administrator.",
                "code": "LICENSE_EXPIRED",
            },
            status=503,
        )

    def _lockout_storefront(self, request):
        """Handle storefront lockout: show 503 page."""
        response = render(
            request,
            "core/license_expired.html",
            status=503,
        )
        response["Retry-After"] = "3600"
        return response
