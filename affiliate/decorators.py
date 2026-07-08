"""
Affiliate App Decorators
Provides rate limiting and security decorators for affiliate views.
"""

import hashlib
from functools import wraps
from django.core.cache import cache
from django.http import HttpResponse
from django.utils.translation import gettext as _
import logging

logger = logging.getLogger(__name__)


def rate_limit(max_requests=100, window_seconds=60, key_prefix='rate_limit'):
    """
    Rate limiting decorator for tracking endpoints.

    Limits requests based on IP address to prevent abuse.

    Args:
        max_requests: Maximum number of requests allowed in the time window
        window_seconds: Time window in seconds
        key_prefix: Prefix for cache keys

    Usage:
        @rate_limit(max_requests=100, window_seconds=60)
        def my_view(request):
            ...
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            # Get client IP
            ip_address = get_client_ip(request)

            # Create cache key
            cache_key = f"{key_prefix}:{hashlib.md5(ip_address.encode()).hexdigest()}"

            # Get current request count
            request_count = cache.get(cache_key, 0)

            if request_count >= max_requests:
                logger.warning(
                    f"Rate limit exceeded for IP {ip_address}: "
                    f"{request_count} requests in {window_seconds}s"
                )
                return HttpResponse(
                    _('Rate limit exceeded. Please try again later.'),
                    status=429,
                    content_type='text/plain'
                )

            # Increment counter
            if request_count == 0:
                # First request in window - set with expiry
                cache.set(cache_key, 1, window_seconds)
            else:
                # Increment existing counter
                cache.incr(cache_key)

            return view_func(request, *args, **kwargs)

        return wrapped_view

    return decorator


def get_client_ip(request):
    """
    Extract client IP address from request.

    Handles X-Forwarded-For header for proxied requests.

    Args:
        request: Django HttpRequest object

    Returns:
        str: Client IP address
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        # X-Forwarded-For can contain multiple IPs, get the first one
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', '0.0.0.0')

    return ip


def track_affiliate_click(view_func):
    """
    Decorator to track affiliate click attempts and detect suspicious patterns.

    Logs click attempts for fraud detection analysis.

    Args:
        view_func: View function to wrap

    Returns:
        Wrapped view function
    """

    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        link_code = kwargs.get('link_code', '')

        # Log click attempt
        logger.info(
            f"Affiliate click tracking: link={link_code}, ip={ip_address}, "
            f"user_agent={user_agent[:50]}"
        )

        # Check for suspicious patterns
        # 1. Missing or suspicious user agent
        if not user_agent or len(user_agent) < 10:
            logger.warning(
                f"Suspicious click from {ip_address}: "
                f"Invalid user agent '{user_agent}'"
            )

        # 2. Check for bot user agents (basic check)
        bot_keywords = ['bot', 'crawler', 'spider', 'scraper', 'curl', 'wget']
        if any(keyword in user_agent.lower() for keyword in bot_keywords):
            logger.warning(
                f"Bot detected in click from {ip_address}: {user_agent}"
            )

        return view_func(request, *args, **kwargs)

    return wrapped_view
