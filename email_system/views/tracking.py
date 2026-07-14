"""
Email Tracking Views
Handles open and click tracking endpoints
"""

import logging
from urllib.parse import unquote

from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

from email_system.models import EmailEvent, EmailOutbox
from email_system.services.tracking_service import TrackingService

logger = logging.getLogger(__name__)

# 1x1 transparent GIF pixel
TRACKING_PIXEL = (
    b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff"
    b"\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00"
    b"\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b"
)


@require_GET
@csrf_exempt
def track_open(request, tracking_id):
    """
    Track email open event via tracking pixel

    Returns 1x1 transparent GIF image
    """
    try:
        # Parse tracking ID to get email_outbox_id
        tracking_service = TrackingService()
        email_outbox_id = tracking_service.parse_tracking_id(tracking_id)

        if not email_outbox_id:
            logger.warning(f"Invalid tracking ID format: {tracking_id}")
            return _return_pixel()

        # Get email outbox entry
        try:
            email_outbox = EmailOutbox.objects.get(id=email_outbox_id)
        except EmailOutbox.DoesNotExist:
            logger.warning(f"Email outbox not found: {email_outbox_id}")
            return _return_pixel()

        # Check if already tracked (avoid duplicate opens)
        existing_open = EmailEvent.objects.filter(email=email_outbox, event_type="opened").first()

        if not existing_open:
            # Record open event
            EmailEvent.objects.create(
                email=email_outbox,
                event_type="opened",
                occurred_at=timezone.now(),
                user_agent=request.META.get("HTTP_USER_AGENT", ""),
                ip_address=_get_client_ip(request),
            )

            logger.info(f"Email opened: outbox_id={email_outbox_id}, to={email_outbox.to_email}")

    except Exception as e:
        logger.error(f"Error tracking email open: {e}", exc_info=True)

    # Always return pixel (even on error)
    return _return_pixel()


@require_GET
@csrf_exempt
def track_click(request, tracking_id):
    """
    Track email link click event and redirect to original URL

    Query params:
        url: Original URL to redirect to
    """
    # Get original URL from query params
    original_url = request.GET.get("url")

    if not original_url:
        logger.warning("Click tracking missing URL parameter")
        raise Http404("Invalid tracking URL")

    # Decode URL
    original_url = unquote(original_url)

    # Validate URL to prevent open redirect attacks
    # Allow the site's own domain and HTTPS URLs only
    allowed_hosts = set()
    try:
        from django.contrib.sites.models import Site

        current_site = Site.objects.get_current()
        allowed_hosts.add(current_site.domain)
    except Exception:
        pass

    if not url_has_allowed_host_and_scheme(
        original_url,
        allowed_hosts=allowed_hosts,
        require_https=not settings.DEBUG,
    ):
        # For external URLs in emails (e.g., partner links), allow http(s) schemes
        # but block javascript:, data:, and other dangerous schemes
        from urllib.parse import urlparse

        parsed = urlparse(original_url)
        if parsed.scheme not in ("http", "https", ""):
            logger.warning(f"Click tracking blocked dangerous URL scheme: {parsed.scheme}")
            raise Http404("Invalid tracking URL")

    try:
        # Parse tracking ID to get email_outbox_id
        tracking_service = TrackingService()
        email_outbox_id = tracking_service.parse_tracking_id(tracking_id)

        if email_outbox_id:
            # Get email outbox entry
            try:
                email_outbox = EmailOutbox.objects.get(id=email_outbox_id)

                # Record click event
                EmailEvent.objects.create(
                    email=email_outbox,
                    event_type="clicked",
                    occurred_at=timezone.now(),
                    user_agent=request.META.get("HTTP_USER_AGENT", ""),
                    ip_address=_get_client_ip(request),
                    event_data={"url": original_url},
                )

                logger.info(
                    f"Email link clicked: outbox_id={email_outbox_id}, "
                    f"to={email_outbox.to_email}, url={original_url}"
                )

            except EmailOutbox.DoesNotExist:
                logger.warning(f"Email outbox not found: {email_outbox_id}")

    except Exception as e:
        logger.error(f"Error tracking email click: {e}", exc_info=True)

    # Always redirect to original URL (even on tracking error)
    return HttpResponseRedirect(original_url)


def _return_pixel():
    """
    Return 1x1 transparent GIF pixel

    Returns:
        HttpResponse with GIF image
    """
    response = HttpResponse(TRACKING_PIXEL, content_type="image/gif")
    # Prevent caching
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"
    return response


def _get_client_ip(request):
    """
    Get client IP address from request

    Checks X-Forwarded-For header first (for proxies)
    Falls back to REMOTE_ADDR

    Args:
        request: Django request object

    Returns:
        IP address string or empty string
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        # Take first IP if multiple (proxy chain)
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR", "")

    return ip
