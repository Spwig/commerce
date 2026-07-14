"""
Admin API Throttling

Custom throttle classes for rate limiting admin API endpoints.
"""

from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class AdminAuthThrottle(AnonRateThrottle):
    """
    Strict rate limiting for admin authentication endpoints.
    Prevents brute-force login attempts.

    Rate: 5 requests per minute (configured in settings)
    """

    scope = "admin_auth"


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
