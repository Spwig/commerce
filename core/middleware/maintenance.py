"""
Maintenance Mode Middleware - Database-Driven

When maintenance_mode=True in SiteSettings, this middleware:
1. Shows the assigned maintenance page (PageBuilder) to all storefront visitors
2. Falls back to static 'maintenance.html' if no custom page is assigned
3. Allows admin access (/admin/*)
4. Allows health check access (/health/*)
5. Allows static/media file access
6. Allows API and webhook access for integrations
7. Provides a secret bypass for testing
8. Caches maintenance status for 10 seconds to reduce DB load

Bypass:
    Add ?secret=<MAINTENANCE_SECRET> to any URL to bypass maintenance mode
    The secret is stored in a cookie for subsequent requests
"""

import logging

from django.conf import settings
from django.core.cache import cache
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

MAINTENANCE_CACHE_KEY = "maintenance_mode_status"
MAINTENANCE_CACHE_TTL = 10  # seconds


class MaintenanceModeMiddleware(MiddlewareMixin):
    """
    Middleware to show maintenance page when maintenance_mode is enabled in SiteSettings.
    """

    # Paths that should always be accessible during maintenance
    ALLOWED_PATHS = (
        "/admin/",
        "/health/",
        "/static/",
        "/media/",
        "/theme/",  # Theme CSS served via custom view
        "/i18n/",  # Language switching
        "/__debug__/",  # Django debug toolbar
        "/api/",  # API access for headless setups
        "/webhooks/",  # Webhooks for payment/shipping providers
    )

    # Paths that match setup wizard (with language prefix support)
    SETUP_PATHS = (
        "/setup/",
        "/en/setup/",
        "/admin/setup/",
        "/en/admin/setup/",
    )

    def process_request(self, request):
        """
        Check maintenance mode and return maintenance page or None.

        Returning an HttpResponse from process_request short-circuits the
        middleware chain (MiddlewareMixin handles this for both sync and ASGI).
        Returning None lets the request continue to the view.
        """
        # Not in maintenance mode — continue
        if not self._is_maintenance_enabled():
            return None

        # Request is allowed to bypass maintenance — continue
        if self._should_bypass(request):
            return None

        # Show maintenance page (short-circuit)
        return self._render_maintenance_page(request)

    def process_response(self, request, response):
        """
        Set the bypass cookie on the response when ?secret= was used.

        This runs after the view (or after process_request short-circuits),
        allowing the cookie to be set on whichever response is returned.
        """
        if getattr(request, "_maintenance_bypass_granted", False):
            secret = getattr(settings, "MAINTENANCE_SECRET", "")
            response.set_cookie(
                "maintenance_bypass",
                secret,
                max_age=86400,  # 24 hours
                httponly=True,
                secure=not settings.DEBUG,
                samesite="Lax",
            )
        return response

    def _get_cached_settings(self):
        """Get maintenance settings from cache or database."""
        cached = cache.get(MAINTENANCE_CACHE_KEY)
        if cached is not None:
            return cached

        try:
            from core.models import SiteSettings

            site_settings = SiteSettings.objects.first()

            if site_settings:
                # Get logo URL if available
                logo_url = None
                if hasattr(site_settings, "site_logo") and site_settings.site_logo:
                    try:
                        logo_url = (
                            site_settings.site_logo.file.url
                            if site_settings.site_logo.file
                            else None
                        )
                    except Exception:
                        pass

                data = {
                    "enabled": site_settings.maintenance_mode,
                    "message": site_settings.maintenance_message,
                    "page_id": getattr(site_settings, "maintenance_page_id", None),
                    "store_name": site_settings.site_name or "Our Store",
                    "logo_url": logo_url,
                }
            else:
                data = {"enabled": False}

            cache.set(MAINTENANCE_CACHE_KEY, data, MAINTENANCE_CACHE_TTL)
            return data
        except Exception as e:
            logger.warning(f"Error fetching maintenance settings: {e}")
            return {"enabled": False}

    def _is_maintenance_enabled(self):
        """Check if maintenance mode is enabled in SiteSettings."""
        # Check environment variable as emergency override (can force ON or OFF)
        env_override = getattr(settings, "MAINTENANCE_MODE_OVERRIDE", None)
        if env_override is not None:
            if isinstance(env_override, str):
                return env_override.lower() in ("true", "1", "yes")
            return bool(env_override)

        # Read from database (cached)
        settings_data = self._get_cached_settings()
        return settings_data.get("enabled", False)

    def _should_bypass(self, request):
        """
        Check if the request should bypass maintenance mode.

        Returns True if:
        - Request is for an allowed path (admin, health, static, api, etc.)
        - Request has valid maintenance secret
        - Request is for setup wizard
        - User is authenticated staff member
        """
        path = request.path

        # Check allowed paths (also handles language-prefixed paths like /en/theme/)
        # Strip language prefix if present (e.g., /en/theme/ -> /theme/)
        stripped_path = path
        if len(path) > 3 and path[3] == "/" and path[1:3].isalpha():
            stripped_path = path[3:]  # Remove /xx/ prefix

        for allowed in self.ALLOWED_PATHS:
            if path.startswith(allowed) or stripped_path.startswith(allowed):
                return True

        # Check setup paths (with language prefix support)
        for setup_path in self.SETUP_PATHS:
            if path.startswith(setup_path):
                return True

        # Check for any language prefix + admin/setup
        # Handles /de/admin/setup/, /fr/setup/, etc.
        path_parts = path.strip("/").split("/")
        if len(path_parts) >= 2:
            if "setup" in path_parts[:3] or "admin" in path_parts[:2]:
                return True

        # Check secret bypass
        if self._check_secret(request):
            return True

        # Allow authenticated staff users (they might need frontend access for testing)
        return bool(
            hasattr(request, "user") and request.user.is_authenticated and request.user.is_staff
        )

    def _check_secret(self, request):
        """
        Check if request has valid maintenance secret.

        The secret can be provided via:
        - Query parameter: ?secret=<MAINTENANCE_SECRET>
        - Cookie: maintenance_bypass=<MAINTENANCE_SECRET>
        """
        secret = getattr(settings, "MAINTENANCE_SECRET", None)

        if not secret:
            return False

        # Check query parameter
        if request.GET.get("secret") == secret:
            # Will set cookie in response
            request._maintenance_bypass_granted = True
            return True

        # Check cookie
        return request.COOKIES.get("maintenance_bypass") == secret

    def _render_maintenance_page(self, request):
        """Render the maintenance page (PageBuilder or fallback)."""
        settings_data = self._get_cached_settings()
        page_id = settings_data.get("page_id")

        # Try to render PageBuilder page
        if page_id:
            try:
                from page_builder.models import Page

                page = (
                    Page.objects.prefetch_related("elements")
                    .select_related("theme", "header_template", "footer_template")
                    .get(pk=page_id, status="published")
                )

                elements = page.elements.filter(
                    parent_element__isnull=True, is_active=True
                ).order_by("order")

                # Get brand CSS
                brand_css_url = None
                try:
                    from design.theme_models import ThemeBranding

                    branding = ThemeBranding.objects.first()
                    if branding:
                        brand_css_url = branding.get_css_url()
                except Exception:
                    pass

                context = {
                    "page": page,
                    "elements": elements,
                    "page_title": page.meta_title or page.title,
                    "brand_css_url": brand_css_url,
                    "is_maintenance": True,
                    "hide_header": getattr(page, "hide_header", True),
                    "hide_footer": getattr(page, "hide_footer", True),
                }

                response = render(request, "page_builder/page.html", context, status=503)
                self._set_response_headers(response)
                return response

            except Page.DoesNotExist:
                logger.warning(f"Maintenance page {page_id} not found, using fallback")
            except Exception as e:
                logger.error(f"Error rendering maintenance page: {e}")

        # Fallback to static template
        return self._render_fallback_page(request, settings_data)

    def _render_fallback_page(self, request, settings_data):
        """Render the static fallback maintenance page."""
        context = {
            "store_name": settings_data.get("store_name", "Our Store"),
            "maintenance_message": settings_data.get("message", ""),
            "store_logo": settings_data.get("logo_url"),
            "spwig_url": "https://spwig.com",
        }

        response = render(request, "maintenance/maintenance.html", context, status=503)
        self._set_response_headers(response)
        return response

    def _set_response_headers(self, response):
        """Set cache and other headers for maintenance response."""
        # Prevent caching of maintenance page
        response["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response["Pragma"] = "no-cache"
        response["Expires"] = "0"
        response["Retry-After"] = "3600"  # Hint to retry in 1 hour
        return response


def invalidate_maintenance_cache():
    """
    Utility function to invalidate maintenance cache when settings change.
    Call this from signal handlers when SiteSettings is saved.
    """
    cache.delete(MAINTENANCE_CACHE_KEY)


def is_maintenance_mode():
    """
    Utility function to check if maintenance mode is enabled.
    Can be used in templates and views.
    """
    cached = cache.get(MAINTENANCE_CACHE_KEY)
    if cached is not None:
        return cached.get("enabled", False)

    try:
        from core.models import SiteSettings

        site_settings = SiteSettings.objects.first()
        return site_settings.maintenance_mode if site_settings else False
    except Exception:
        return False
