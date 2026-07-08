"""
License Acceptance Middleware

Gates requests until the Software License Agreement has been accepted.
This middleware must be placed early in the stack (after WhiteNoise/Session/Locale
but BEFORE ActivationMiddleware) so that license acceptance is the very first
gate a merchant encounters on a fresh installation.

Behavior:
- Fresh install (never accepted): gates ALL paths → redirect to /license/accept/
- Re-acceptance needed (major version bump): gates only /admin/ paths, storefront
  remains accessible to customers
- Accepted & current: no-op

Exempt paths (always pass through):
- /static/, /media/ — CSS/JS must load for the acceptance page
- /health/* — monitoring probes
- /license/* — the acceptance page itself
- /api/* — DRF endpoints have own permissions; must not redirect to HTML
- /__debug__/ — Django debug toolbar
"""

import logging
import re

from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class LicenseAcceptanceMiddleware(MiddlewareMixin):
    """
    Enforce Software License Agreement acceptance before any platform use.

    Uses the LicenseAcceptanceService with class-level caching to avoid
    filesystem reads on every request.
    """

    EXEMPT_PREFIXES = (
        '/static/',
        '/media/',
        '/health/',
        '/license/',
        '/api/',
        '/__debug__/',
    )

    REDIRECT_URL = '/license/accept/'

    # Matches /admin/ with optional locale prefix: /en/admin/, /zh-hans/admin/
    ADMIN_PATH_RE = re.compile(r'^(/[a-z]{2}(-[a-z]+)?)?/admin/')

    def process_request(self, request):
        """Check license acceptance before processing any request."""

        path = request.path

        # Exempt paths always pass through
        if any(path.startswith(prefix) for prefix in self.EXEMPT_PREFIXES):
            return None

        try:
            from core.license_acceptance import get_license_acceptance_service

            service = get_license_acceptance_service()

            if service.is_accepted():
                # License was accepted before — check if re-acceptance needed
                needs_reaccept, _ = service.needs_reacceptance()
                if not needs_reaccept:
                    return None  # Fully accepted and current

                # Re-acceptance needed (major version bump) — only gate admin
                # paths. Storefront must remain accessible to customers.
                if not self.ADMIN_PATH_RE.match(path):
                    return None

            # Either never accepted (fresh install) or admin path needing
            # re-acceptance → redirect to acceptance page
            logger.info(
                f"License not accepted, redirecting {path} to "
                f"{self.REDIRECT_URL}"
            )
            return redirect(self.REDIRECT_URL)

        except Exception as e:
            # If we can't determine acceptance status, don't block
            # (e.g., LICENSE.txt doesn't exist yet during initial setup)
            logger.warning(f"License acceptance check failed: {e}")
            return None
