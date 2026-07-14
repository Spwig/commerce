"""
Referral Cookie Tracking Middleware.

Automatically tracks referral link clicks and sets tracking cookies.
Also attaches request context to user/order objects for signal handlers.
"""

import logging

from django.utils.deprecation import MiddlewareMixin

from .models import ReferralProgram
from .services.tracking import set_ref_cookie, track_click

logger = logging.getLogger(__name__)


class ReferralTrackingMiddleware(MiddlewareMixin):
    """
    Middleware to handle referral link tracking.

    Features:
    - Detects 'ref' query parameter in URL
    - Tracks click event and sets referral cookie
    - Attaches request to user/order instances for signal handlers
    - Non-intrusive: Does not interfere with normal request flow
    """

    def process_request(self, request):
        """
        Process incoming request to check for referral tracking.

        Args:
            request: HttpRequest object

        Returns:
            None (allows request to continue)
        """
        # Check for referral token in query parameter
        ref_token = request.GET.get("ref")

        if ref_token:
            try:
                # Check if program is active
                program = ReferralProgram.get_program()
                if program and program.is_active():
                    # Track the click
                    success, identity, message = track_click(ref_token, request)

                    if success:
                        # Mark that we need to set cookie in response
                        request._ref_token_to_set = ref_token
                        logger.info(f"Tracked referral click from token: {ref_token[:8]}...")
                    else:
                        logger.warning(f"Failed to track referral: {message}")
            except Exception as e:
                logger.error(f"Error in referral tracking middleware: {e}", exc_info=True)

        # Always return None to continue request processing
        return None

    def process_response(self, request, response):
        """
        Process outgoing response to set referral cookie if needed.

        Args:
            request: HttpRequest object
            response: HttpResponse object

        Returns:
            HttpResponse with referral cookie set (if applicable)
        """
        # Check if we need to set referral cookie
        if hasattr(request, "_ref_token_to_set"):
            try:
                # Get cookie TTL from program settings
                program = ReferralProgram.get_program()
                ttl_days = program.get_cookie_ttl_days() if program else 30

                # Set cookie on response
                set_ref_cookie(response, request._ref_token_to_set, ttl_days)
                logger.debug(f"Set referral cookie with TTL: {ttl_days} days")
            except Exception as e:
                logger.error(f"Error setting referral cookie: {e}", exc_info=True)

        return response


class RequestContextMiddleware(MiddlewareMixin):
    """
    Middleware to attach request context to model instances.

    Allows signal handlers to access request data (cookies, IP, etc.)
    by attaching request to user/order instances during save operations.

    IMPORTANT: This should be placed AFTER authentication middleware
    in settings.MIDDLEWARE.
    """

    def process_request(self, request):
        """
        Store request in thread-local storage for access in signals.

        Args:
            request: HttpRequest object

        Returns:
            None (allows request to continue)
        """
        # Store request in thread-local storage
        from threading import current_thread

        thread = current_thread()
        thread.request = request

        return None

    def process_response(self, request, response):
        """
        Clean up thread-local storage after request.

        Args:
            request: HttpRequest object
            response: HttpResponse object

        Returns:
            HttpResponse unchanged
        """
        # Clean up thread-local storage
        from threading import current_thread

        thread = current_thread()
        if hasattr(thread, "request"):
            delattr(thread, "request")

        return response

    def process_exception(self, request, exception):
        """
        Clean up thread-local storage on exception.

        Args:
            request: HttpRequest object
            exception: Exception instance

        Returns:
            None (allows exception to propagate)
        """
        # Clean up thread-local storage
        from threading import current_thread

        thread = current_thread()
        if hasattr(thread, "request"):
            delattr(thread, "request")

        return None


def get_current_request():
    """
    Get current request from thread-local storage.

    Returns:
        HttpRequest or None: Current request if available

    Usage:
        from referrals.middleware import get_current_request

        # In model save() method or signal handler
        request = get_current_request()
        if request:
            # Access request data
            token = request.COOKIES.get('ref_token')
    """
    from threading import current_thread

    thread = current_thread()
    return getattr(thread, "request", None)
