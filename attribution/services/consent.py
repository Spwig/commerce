"""Server-side analytics-consent gate.

The platform ships a first-party consent banner whose choice is stored in the
``spwig_cookie_consent`` cookie (``{"necessary":true,"analytics":bool,...}``),
but until now *nothing on the server honoured it* — geoip and referral tracking
recorded UTM/IP regardless. Capturing an attribution touch is analytics
tracking and writes a first-party identifier cookie, so it must respect the
``analytics`` bit. This module is the gate; recording is refused unless consent
is granted (or the merchant runs no banner at all, which is their legal
choice).
"""

import json
import logging
from urllib.parse import unquote

from attribution.constants import CONSENT_DENIED, CONSENT_GRANTED, CONSENT_UNKNOWN

logger = logging.getLogger(__name__)

CONSENT_COOKIE = "spwig_cookie_consent"


def analytics_consent_state(request):
    """Return the analytics-consent state for this request.

    - If the merchant has no consent banner enabled, there is no gate to honour
      and analytics is implicitly permitted (``granted``).
    - If the banner is enabled but the visitor has not answered, state is
      ``unknown`` and we do not track.
    - Otherwise it reflects the stored ``analytics`` choice.
    """
    try:
        from core.models import SiteSettings

        site_settings = SiteSettings.get_settings()
        if not getattr(site_settings, "cookie_consent_enabled", False):
            return CONSENT_GRANTED
    except Exception:  # pragma: no cover - defensive; never block a request on this
        logger.debug("attribution: could not read consent settings; treating as unknown")
        return CONSENT_UNKNOWN

    raw = request.COOKIES.get(CONSENT_COOKIE)
    if not raw:
        return CONSENT_UNKNOWN
    try:
        data = json.loads(unquote(raw))
    except (ValueError, TypeError):
        return CONSENT_UNKNOWN
    return CONSENT_GRANTED if data.get("analytics") else CONSENT_DENIED


def analytics_allowed(request):
    """True only when analytics tracking is affirmatively permitted."""
    return analytics_consent_state(request) == CONSENT_GRANTED
