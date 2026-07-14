"""
MFA Enforcement Middleware

Enforces two-factor authentication requirements for staff users
based on SiteSettings configuration.

This middleware handles two separate concerns:
1. Enforcement: Requiring users to SET UP 2FA based on policy
2. Verification: Requiring users who HAVE 2FA to verify on login
"""

import logging
import re

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import gettext as _

logger = logging.getLogger(__name__)

# Cookie name for trusted devices
TRUSTED_DEVICE_COOKIE = "spwig_trusted_device"

# Session key to track MFA verification status
MFA_VERIFIED_SESSION_KEY = "mfa_verified_at"

# Match admin paths with or without language prefix
# e.g. /admin/, /en/admin/, /de/admin/login/
ADMIN_PATH_RE = re.compile(r"^(/[a-z]{2})?/admin/")


class MFAEnforcementMiddleware(MiddlewareMixin):
    """
    Enforce MFA requirements for staff users accessing the admin.

    This middleware:
    1. Checks if 2FA enforcement is enabled in SiteSettings
    2. Determines if the current user requires 2FA
    3. Checks if user has 2FA set up or is within grace period
    4. Checks for trusted device cookie
    5. Redirects to 2FA setup if required

    Enforcement Levels:
    - disabled: 2FA is optional for all staff
    - recommended: Show prompts but allow access
    - required: Must have 2FA to access admin (after grace period)
    """

    # Paths that are always exempt from MFA enforcement (no language prefix)
    EXEMPT_PATHS_NO_PREFIX = [
        "/static/",
        "/media/",
        "/api/",
        "/i18n/",
        "/oidc/",
    ]

    # Paths that may have a language prefix (e.g. /en/accounts/mfa/)
    EXEMPT_PATH_PATTERNS = [
        re.compile(r"^(/[a-z]{2})?/accounts/mfa/"),
        re.compile(r"^(/[a-z]{2})?/accounts/2fa/"),
        re.compile(r"^(/[a-z]{2})?/account/2fa/"),
        re.compile(r"^(/[a-z]{2})?/accounts/login/"),
        re.compile(r"^(/[a-z]{2})?/accounts/logout/"),
        re.compile(r"^(/[a-z]{2})?/admin/login/"),
        re.compile(r"^(/[a-z]{2})?/admin/logout/"),
        re.compile(r"^(/[a-z]{2})?/admin/jsi18n/"),
    ]

    # Additional path patterns to check (for paths that vary by app)
    EXEMPT_PATH_CONTAINS = [
        "/mfa/verify/",  # Admin MFA verification page (under any app)
    ]

    def process_request(self, request):
        """Check MFA requirements before processing admin requests."""

        path = request.path

        # Skip for paths that never have language prefix
        if any(path.startswith(p) for p in self.EXEMPT_PATHS_NO_PREFIX):
            return None

        # Skip for paths containing exempt patterns
        if any(pattern in path for pattern in self.EXEMPT_PATH_CONTAINS):
            return None

        # Skip for exempt paths (with optional language prefix)
        if any(pattern.match(path) for pattern in self.EXEMPT_PATH_PATTERNS):
            return None

        # Only check for admin paths (with optional language prefix)
        if not ADMIN_PATH_RE.match(path):
            return None

        # Skip for unauthenticated users
        if not request.user.is_authenticated:
            return None

        # Skip for non-staff users
        if not request.user.is_staff:
            return None

        # Check if user has 2FA enabled
        user_has_2fa = self._user_has_2fa(request.user)

        # FIRST: If user has 2FA, verify they've completed MFA verification this session
        if user_has_2fa and not self._is_mfa_verified(request):
            # Check for trusted device first
            from core.models import SiteSettings

            try:
                settings = SiteSettings.get_settings()
                if settings.allow_trusted_devices:
                    if self._is_trusted_device(request, request.user, settings):
                        # Trusted device - mark as verified and continue
                        self._mark_mfa_verified(request)
                        return None
            except Exception:
                pass

            # Redirect to MFA verification
            return self._redirect_to_mfa_verification(request)

        # Get site settings for enforcement checks
        from core.models import SiteSettings

        try:
            settings = SiteSettings.get_settings()
        except Exception as e:
            logger.error(f"Failed to get site settings for MFA enforcement: {e}")
            return None

        # Check if enforcement is enabled
        enforcement_level = settings.staff_2fa_enforcement
        if enforcement_level == "disabled":
            return None

        if enforcement_level == "recommended":
            # Just show a recommendation, don't block
            if not user_has_2fa and not self._has_dismissed_recommendation(request):
                self._show_recommendation(request)
            return None

        # enforcement_level == 'required'
        # User doesn't have 2FA set up - check grace period
        if self._is_within_grace_period(request.user, settings):
            # Within grace period - show reminder but allow access
            self._show_setup_reminder(request, settings)
            return None

        # Grace period expired or enforcement is immediate
        # Redirect to MFA setup
        return self._redirect_to_mfa_setup(request)

    def _user_has_2fa(self, user):
        """Check if user has MFA enabled."""
        try:
            from allauth.mfa.utils import is_mfa_enabled

            return is_mfa_enabled(user)
        except ImportError:
            try:
                from allauth.mfa.adapter import get_adapter

                adapter = get_adapter()
                return adapter.is_mfa_enabled(user)
            except Exception as e:
                logger.error(f"Failed to check MFA status: {e}")
                return False
        except Exception as e:
            logger.error(f"Failed to check MFA status: {e}")
            return False

    def _is_trusted_device(self, request, user, settings):
        """Check if the current device is trusted."""
        from core.models import TrustedDevice

        token = request.COOKIES.get(TRUSTED_DEVICE_COOKIE)
        if not token:
            return False

        device = TrustedDevice.validate_token(user, token)
        return device is not None

    def _is_within_grace_period(self, user, settings):
        """
        Check if user is within the 2FA setup grace period.

        Grace period logic:
        - If grace_period_days is 0, no grace period (immediate enforcement)
        - If enforcement_date is not set, user is in grace period (shouldn't happen)
        - For existing users: grace ends at (enforcement_date + grace_period_days)
        - For new users (created after enforcement_date): grace ends at (date_joined + grace_period_days)
        """
        if settings.staff_2fa_grace_period_days == 0:
            return False

        if not settings.staff_2fa_enforcement_date:
            # Enforcement date not set - allow access (this is a config issue)
            logger.warning("2FA enforcement is 'required' but enforcement_date is not set")
            return True

        # Determine grace period end date
        # For users created after enforcement, use their join date
        if user.date_joined > settings.staff_2fa_enforcement_date:
            # New user - grace period from account creation
            grace_end = user.date_joined + timezone.timedelta(
                days=settings.staff_2fa_grace_period_days
            )
        else:
            # Existing user - grace period from enforcement date
            grace_end = settings.staff_2fa_enforcement_date + timezone.timedelta(
                days=settings.staff_2fa_grace_period_days
            )

        return timezone.now() < grace_end

    def _get_grace_days_remaining(self, user, settings):
        """Calculate remaining days in grace period."""
        if not settings.staff_2fa_enforcement_date:
            return settings.staff_2fa_grace_period_days

        # Determine grace period end date
        if user.date_joined > settings.staff_2fa_enforcement_date:
            grace_end = user.date_joined + timezone.timedelta(
                days=settings.staff_2fa_grace_period_days
            )
        else:
            grace_end = settings.staff_2fa_enforcement_date + timezone.timedelta(
                days=settings.staff_2fa_grace_period_days
            )

        delta = grace_end - timezone.now()
        return max(0, delta.days)

    def _has_dismissed_recommendation(self, request):
        """Check if user has dismissed the 2FA recommendation."""
        return request.session.get("2fa_recommendation_dismissed", False)

    def _show_recommendation(self, request):
        """Show a recommendation to set up 2FA."""
        if not hasattr(request, "_mfa_recommendation_shown"):
            messages.info(
                request,
                _(
                    "For better security, we recommend enabling two-factor authentication. "
                    "You can set this up in your account settings."
                ),
            )
            request._mfa_recommendation_shown = True

    def _show_setup_reminder(self, request, settings):
        """Show a reminder to set up 2FA during grace period."""
        if not hasattr(request, "_mfa_reminder_shown"):
            days_remaining = self._get_grace_days_remaining(request.user, settings)
            level = messages.WARNING if days_remaining <= 3 else messages.INFO

            messages.add_message(
                request,
                level,
                _(
                    "Two-factor authentication will be required in %(days)s day(s). "
                    "Please set up 2FA in your account settings to continue accessing the admin."
                )
                % {"days": days_remaining},
            )
            request._mfa_reminder_shown = True

    def _redirect_to_mfa_setup(self, request):
        """Redirect user to MFA setup page."""
        messages.error(
            request,
            _(
                "Two-factor authentication is required for admin access. "
                "Please set up 2FA to continue."
            ),
        )
        # Redirect to allauth MFA setup
        try:
            setup_url = reverse("mfa_activate_totp")
        except Exception:
            # Fallback URL
            setup_url = "/accounts/2fa/totp/activate/"

        # Include next parameter to return after setup
        next_url = request.get_full_path()
        return HttpResponseRedirect(f"{setup_url}?next={next_url}")

    def _is_mfa_verified(self, request):
        """
        Check if the user has verified MFA for this session.

        Returns True if:
        - MFA was verified in this session via our admin verification, OR
        - MFA was verified via allauth's login flow (recorded in session)
        """
        # Check our session key (set by admin MFA verification view)
        mfa_verified_at = request.session.get(MFA_VERIFIED_SESSION_KEY)
        if mfa_verified_at:
            return True

        # Check allauth's authentication records for MFA verification
        # Allauth stores authentication methods in session when MFA is completed
        auth_methods = request.session.get("account_authentication_methods", [])
        return any(method.get("method") == "mfa" for method in auth_methods)

    def _mark_mfa_verified(self, request):
        """Mark MFA as verified for this session."""
        request.session[MFA_VERIFIED_SESSION_KEY] = timezone.now().isoformat()
        request.session.modified = True

    def _redirect_to_mfa_verification(self, request):
        """Redirect user to MFA verification page."""
        # Store the next URL in session for redirect after verification
        request.session["mfa_next_url"] = request.get_full_path()

        try:
            verify_url = reverse("admin:mfa_verify")
        except Exception:
            verify_url = "/admin/mfa/verify/"

        return HttpResponseRedirect(verify_url)
