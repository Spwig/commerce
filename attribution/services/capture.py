"""Record a single attribution touch from an HTTP request.

Append-only and cheap. A row is written only when the arrival carries a real
source signal — untagged direct navigation does not spam the stream; "direct"
is inferred at resolution time by the *absence* of a non-direct touch in the
lookback window. Capture is refused entirely unless analytics consent is
granted (see ``services.consent``).
"""

import logging
from urllib.parse import urlparse

from attribution.constants import CHANNEL_DIRECT
from attribution.services import channels, consent, identity

logger = logging.getLogger(__name__)

# Paths we never attribute against.
_SKIP_PREFIXES = (
    "/admin",
    "/api",
    "/internal",
    "/static",
    "/media",
    "/webhooks",
    "/i18n",
    "/track",
)

_UTM_KEYS = ("utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content")


def _extract(request):
    """Pull the raw signal fields out of a request."""
    get = request.GET
    referrer = request.META.get("HTTP_X_PAGE_REFERRER") or request.META.get("HTTP_REFERER", "")
    referrer_host = urlparse(referrer).hostname or "" if referrer else ""
    try:
        request_host = request.get_host().split(":")[0]
    except Exception:
        request_host = ""
    return {
        "utm_source": get.get("utm_source", "")[:255],
        "utm_medium": get.get("utm_medium", "")[:255],
        "utm_campaign": get.get("utm_campaign", "")[:255],
        "utm_term": get.get("utm_term", "")[:255],
        "utm_content": get.get("utm_content", "")[:255],
        "gclid": get.get("gclid", "")[:255],
        "fbclid": get.get("fbclid", "")[:255],
        "msclkid": get.get("msclkid", "")[:255],
        "referrer_host": referrer_host[:255],
        "referrer_is_internal": bool(referrer_host) and referrer_host == request_host,
        "landing_path": (request.path or "")[:512],
    }


def has_signal(sig):
    """True when the arrival carries something worth recording."""
    if any(sig.get(k) for k in _UTM_KEYS):
        return True
    if sig.get("gclid") or sig.get("fbclid") or sig.get("msclkid"):
        return True
    # An external referrer is itself a signal (organic/referral); an internal
    # or absent referrer is not.
    return bool(sig.get("referrer_host") and not sig.get("referrer_is_internal"))


def should_capture(request):
    """Cheap pre-checks before doing any work."""
    if request.method != "GET":
        return False
    path = request.path or "/"
    if any(path.startswith(p) for p in _SKIP_PREFIXES):
        return False
    # Localised prefixes (/en/admin, /fr/api) — strip one locale segment.
    parts = path.split("/", 2)
    if len(parts) > 2 and len(parts[1]) in (2, 5):
        if any(("/" + parts[2]).startswith(p) for p in _SKIP_PREFIXES):
            return False
    return True


def record_touch(request):
    """Capture a TouchPoint for this request if warranted. Returns it or None.

    Never raises into the request cycle — attribution is best-effort and must
    not break page loads.
    """
    try:
        if not should_capture(request):
            return None

        # Bots never attribute.
        from geoip.tracking import detect_bot, detect_device_type

        ua = request.META.get("HTTP_USER_AGENT", "")
        if detect_bot(ua):
            return None

        sig = _extract(request)
        if not has_signal(sig):
            return None

        # Consent gate — also the point that closes the platform's existing
        # "track regardless of consent" gap for this new capture path.
        if not consent.analytics_allowed(request):
            logger.debug("attribution: analytics consent not granted; skipping capture")
            return None

        channel = channels.resolve_channel(
            **{
                k: sig[k]
                for k in (
                    "utm_source",
                    "utm_medium",
                    "utm_campaign",
                    "gclid",
                    "fbclid",
                    "msclkid",
                    "referrer_host",
                    "referrer_is_internal",
                )
            }
        )
        if channel == CHANNEL_DIRECT:
            # No distinguishing signal after all — do not record.
            return None

        visitor_key, _is_new = identity.ensure_visitor_key(request)

        # Resolve a known campaign by its slug (raw string kept regardless).
        campaign_ref = None
        slug = sig["utm_campaign"]
        if slug:
            from attribution.models import Campaign

            campaign_ref = Campaign.objects.filter(slug=slug).first()

        from attribution.constants import CONSENT_GRANTED
        from attribution.models import TouchPoint

        session_key = ""
        try:
            session_key = request.session.session_key or ""
        except Exception:
            pass

        touch = TouchPoint.objects.create(
            visitor_key=visitor_key,
            session_key=session_key,
            customer=request.user
            if getattr(request, "user", None) and request.user.is_authenticated
            else None,
            channel=channel,
            source=sig["utm_source"],
            medium=sig["utm_medium"],
            campaign=sig["utm_campaign"],
            term=sig["utm_term"],
            content=sig["utm_content"],
            gclid=sig["gclid"],
            fbclid=sig["fbclid"],
            msclkid=sig["msclkid"],
            referrer_host=sig["referrer_host"],
            landing_path=sig["landing_path"],
            campaign_ref=campaign_ref,
            consent_state=CONSENT_GRANTED,
            is_bot=False,
            device_type=detect_device_type(ua),
        )

        # Ensure the visitor thread exists (and is bound if already logged in).
        from attribution.models import VisitorThread

        thread, _created = VisitorThread.objects.get_or_create(visitor_key=visitor_key)
        if touch.customer_id and thread.customer_id != touch.customer_id:
            thread.customer_id = touch.customer_id
            thread.save(update_fields=["customer"])

        return touch
    except Exception:  # pragma: no cover - defensive
        logger.exception("attribution: record_touch failed")
        return None


def record_channel_touch(request, channel, *, affiliate_click=None, referral_event=None):
    """Record a touch whose channel is known by a first-party marker, not UTM.

    Affiliate and referral arrivals are identified by their own tracking
    (an affiliate link redirect, a ``?ref=`` cookie), not by UTM params, so
    their capture points call this to place an explicit ``affiliate`` /
    ``referral`` touch into the shared stream — linked back to the originating
    Click / ReferralEvent. This is how affiliate and referral revenue becomes
    visible as its own channel in the unified attribution reporting.

    Consent-gated and best-effort, exactly like ``record_touch``. Returns the
    TouchPoint or None.
    """
    try:
        if not consent.analytics_allowed(request):
            return None

        from geoip.tracking import detect_bot, detect_device_type

        ua = request.META.get("HTTP_USER_AGENT", "")
        if detect_bot(ua):
            return None

        sig = _extract(request)
        visitor_key, _is_new = identity.ensure_visitor_key(request)

        # Resolve a campaign if the marker link also carried a UTM campaign.
        campaign_ref = None
        if sig["utm_campaign"]:
            from attribution.models import Campaign

            campaign_ref = Campaign.objects.filter(slug=sig["utm_campaign"]).first()

        from attribution.constants import CONSENT_GRANTED
        from attribution.models import TouchPoint, VisitorThread

        session_key = ""
        try:
            session_key = request.session.session_key or ""
        except Exception:
            pass

        customer = (
            request.user
            if getattr(request, "user", None) and request.user.is_authenticated
            else None
        )
        touch = TouchPoint.objects.create(
            visitor_key=visitor_key,
            session_key=session_key,
            customer=customer,
            channel=channel,
            source=sig["utm_source"],
            medium=sig["utm_medium"],
            campaign=sig["utm_campaign"],
            term=sig["utm_term"],
            content=sig["utm_content"],
            referrer_host=sig["referrer_host"],
            landing_path=sig["landing_path"],
            campaign_ref=campaign_ref,
            affiliate_click=affiliate_click,
            referral_event=referral_event,
            consent_state=CONSENT_GRANTED,
            is_bot=False,
            device_type=detect_device_type(ua),
        )
        thread, _created = VisitorThread.objects.get_or_create(visitor_key=visitor_key)
        if touch.customer_id and thread.customer_id != touch.customer_id:
            thread.customer_id = touch.customer_id
            thread.save(update_fields=["customer"])
        return touch
    except Exception:  # pragma: no cover - defensive
        logger.exception("attribution: record_channel_touch failed for channel %s", channel)
        return None
