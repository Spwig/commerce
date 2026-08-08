"""
Admin API Throttling

Custom throttle classes for rate limiting admin API endpoints.
"""

from rest_framework.throttling import SimpleRateThrottle, UserRateThrottle


class AdminAuthThrottle(SimpleRateThrottle):
    """
    Strict rate limiting for admin authentication endpoints.
    Prevents brute-force login attempts.

    Keys on the client IP regardless of authentication state, so callers
    supplying a valid token/session cannot bypass the limit on these
    AllowAny endpoints.

    Rate: 5 requests per minute (configured in settings)
    """

    scope = "admin_auth"

    def get_cache_key(self, request, view):
        return self.cache_format % {
            "scope": self.scope,
            "ident": self.get_ident(request),
        }


class AdminAPIThrottle(UserRateThrottle):
    """
    Rate limiting for authenticated admin API calls.
    More permissive than auth endpoints but still protective.

    Rate: 300 requests per minute (configured in settings)
    """

    scope = "admin_api"


class AdminSensitiveOperationThrottle(UserRateThrottle):
    """
    Throttle for sensitive operations (status changes, stock adjustments).
    More restrictive to prevent rapid automated changes.

    Rate: 30 requests per minute (configured in settings)
    """

    scope = "admin_sensitive"
