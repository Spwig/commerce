"""
Sandbox API views.

Handles tamper report beacon from the storefront/POS sandbox banners.
When a banner tamper is detected client-side, it sends a beacon here,
which we log and forward to the update server via Celery.
"""

import json
import logging

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from core.license import is_sandbox_mode

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def tamper_report(request):
    """
    Receive sandbox banner tamper reports from the client.

    The storefront and POS banners send a beacon here if someone
    removes or hides the sandbox banner via DevTools.

    Rate-limited inherently by navigator.sendBeacon (fires once on tamper).
    """
    if not is_sandbox_mode():
        return HttpResponse(status=204)

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return HttpResponseBadRequest("Invalid JSON")

    event = data.get("event", "unknown")
    url = data.get("url", "")
    timestamp = data.get("ts", 0)

    logger.warning(
        f"[SANDBOX TAMPER] event={event}, url={url}, ts={timestamp}, "
        f"ip={request.META.get('REMOTE_ADDR', 'unknown')}"
    )

    # Forward to update server asynchronously
    try:
        from core.sandbox.tasks import report_tamper_to_server

        report_tamper_to_server.delay(
            event=event,
            url=url,
            ip=request.META.get("REMOTE_ADDR", ""),
        )
    except Exception:
        # Don't fail if Celery isn't available
        pass

    return HttpResponse(status=204)
