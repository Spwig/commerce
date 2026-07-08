"""
Activation Middleware

Gates ALL requests until the platform has been activated with a valid license.
Checks for the existence of a license file at the configured LICENSE_PATH.

This middleware must run AFTER LicenseAcceptanceMiddleware so that merchants
accept the Software License Agreement before being prompted to activate.

Exempt paths:
- /static/, /media/ — assets must load for the activation page
- /health/* — monitoring probes
- /activate/ — the activation page itself
- /license/* — license acceptance pages (must be accessible before activation)
- /api/* — DRF endpoints have own permissions; must not redirect to HTML
- /__debug__/ — Django debug toolbar
"""

import logging

from django.conf import settings
from django.core.cache import cache
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from pathlib import Path

logger = logging.getLogger(__name__)

ACTIVATION_CACHE_KEY = 'spwig_activated'
ACTIVATION_CACHE_TTL = 60 * 60 * 24  # 24 hours (only cached when True)


class ActivationMiddleware(MiddlewareMixin):
    """
    Redirect all traffic to /activate/ until a license file exists.

    Runs after LicenseAcceptanceMiddleware — merchants must accept the EULA
    before they can activate. Once a license file is written (via /activate/
    POST or the activate_with_token management command), the cache is set
    and this middleware becomes a no-op.
    """

    EXEMPT_PREFIXES = (
        '/static/',
        '/media/',
        '/health/',
        '/activate/',
        '/license/',
        '/api/',
        '/__debug__/',
    )

    REDIRECT_URL = '/activate/'

    def process_request(self, request):
        path = request.path

        # Always allow exempt paths
        if any(path.startswith(prefix) for prefix in self.EXEMPT_PREFIXES):
            return None

        # Check if already activated
        if self._is_activated():
            return None

        # Not activated — redirect to activation page
        return redirect(self.REDIRECT_URL)

    def _is_activated(self):
        """Check if a license file exists (cached once True)."""
        cached = cache.get(ACTIVATION_CACHE_KEY)
        if cached is not None:
            return cached

        license_path = getattr(
            settings,
            'LICENSE_PATH',
            '/opt/shop-platform/license/license.json'
        )
        activated = Path(license_path).exists()

        if activated:
            # Only cache when True — once activated, stays activated
            cache.set(ACTIVATION_CACHE_KEY, True, ACTIVATION_CACHE_TTL)

        return activated
