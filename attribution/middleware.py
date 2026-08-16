"""Attribution capture middleware.

Records a touch (when warranted and consented) before the view runs, and sets
the first-party visitor cookie on the way out. Deliberately thin and
fail-open: attribution is best-effort and must never break a page load. Must
run after SessionMiddleware, AuthenticationMiddleware and GeoIPMiddleware so
that session, user and bot detection are available.
"""

import logging

from attribution.services import capture
from attribution.services.identity import set_visitor_cookie

logger = logging.getLogger(__name__)


class AttributionCaptureMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            capture.record_touch(request)
        except Exception:  # pragma: no cover - never break the request
            logger.exception("attribution: capture middleware error")

        response = self.get_response(request)

        # Persist a freshly minted visitor key.
        try:
            if getattr(request, "_attribution_new_visitor_key", False):
                key = getattr(request, "attribution_visitor_key", None)
                if key:
                    set_visitor_cookie(request, response, key)
        except Exception:  # pragma: no cover
            logger.exception("attribution: failed to set visitor cookie")

        return response
