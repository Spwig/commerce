"""Visitor identity: the spine that binds an anonymous touch stream to a buyer.

A first-party ``attr_vid`` cookie holds an opaque, random visitor key that is
independent of Django's session key (which rotates at login and would otherwise
orphan the touch stream — the exact gap that leaves traffic-source records
disconnected from the buyer today). The key is also stashed in session data so
it survives that rotation, mirroring the cart's proven ``guest_cart_id``
adoption in ``cart/signals.py``.

Binding to a customer happens at login (see ``attribution.signals``) and at
order creation (the P2 orchestrator), at which point every anonymous touch for
that key is backfilled with the customer. Cross-device unification is out of
scope by design and disclosed to merchants.
"""

import logging
import secrets

logger = logging.getLogger(__name__)

VISITOR_COOKIE = "attr_vid"
SESSION_STASH_KEY = "attr_vid"


def mint_visitor_key():
    return secrets.token_urlsafe(32)[:64]


def get_visitor_key(request):
    """Best-effort read of the current visitor key without minting one."""
    key = getattr(request, "attribution_visitor_key", None)
    if key:
        return key
    key = request.COOKIES.get(VISITOR_COOKIE)
    if key:
        return key
    try:
        return request.session.get(SESSION_STASH_KEY)
    except Exception:
        return None


def ensure_visitor_key(request):
    """Return the visitor key for this request, minting one if needed.

    Records the key on the request (and flags a new key so the middleware sets
    the cookie on the response) and stashes it in session so it survives
    login's session-key rotation. Callers must have already checked consent —
    this writes a first-party identifier.
    """
    key = request.COOKIES.get(VISITOR_COOKIE)
    is_new = False
    if not key:
        key = mint_visitor_key()
        is_new = True
        request._attribution_new_visitor_key = True

    request.attribution_visitor_key = key

    # Stash in session so login's key rotation does not orphan the stream.
    try:
        if request.session.get(SESSION_STASH_KEY) != key:
            request.session[SESSION_STASH_KEY] = key
    except Exception:
        pass

    return key, is_new


def set_visitor_cookie(request, response, key):
    """Set the first-party visitor cookie, scoped to the attribution window."""
    try:
        from attribution.models import AttributionSettings

        max_age = AttributionSettings.get_settings().lookback_days * 86400
    except Exception:
        max_age = 90 * 86400
    response.set_cookie(
        key=VISITOR_COOKIE,
        value=key,
        max_age=max_age,
        httponly=True,
        samesite="Lax",
        secure=request.is_secure(),
    )


def bind_customer(visitor_key, user):
    """Bind a visitor thread to a customer and backfill their touch stream.

    Idempotent. Returns the number of touch points backfilled.
    """
    if not visitor_key or user is None or not getattr(user, "is_authenticated", False):
        return 0

    from attribution.models import TouchPoint, VisitorThread

    thread, _created = VisitorThread.objects.get_or_create(visitor_key=visitor_key)
    if thread.customer_id != user.id:
        thread.customer = user
        thread.save(update_fields=["customer"])

    backfilled = TouchPoint.objects.filter(visitor_key=visitor_key, customer__isnull=True).update(
        customer=user
    )
    if backfilled:
        logger.info(
            "attribution: bound %s touch(es) on visitor %s… to customer %s",
            backfilled,
            visitor_key[:8],
            user.pk,
        )
    return backfilled


def stitch_from_request(request, user):
    """Resolve the request's visitor key and bind it to ``user``."""
    return bind_customer(get_visitor_key(request), user)
