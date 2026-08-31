"""Storefront newsletter signup — the anonymous marketing opt-in seam.

Two behaviours power the storefront newsletter forms (the page-builder element
and the footer/header widget both post here):

* ``subscribe_email`` — opt an email address into marketing from the storefront,
  honouring the merchant's double opt-in policy and recording consent evidence.
* ``confirm_subscription`` — complete a double opt-in from the emailed link.

Consent is deliberately conservative. When double opt-in is on (the default), a
new lead is created ``pending`` and only becomes emailable once it confirms.
When the email belongs to a registered customer, consent is mirrored into their
``CommunicationPreference`` — the authority that ``Subscriber.is_emailable``
defers to for linked users — so the two systems never disagree.
"""

import logging

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core.validators import validate_email, validate_ipv46_address
from django.db import IntegrityError, transaction
from django.utils import timezone

from ..models import Subscriber, generate_token

logger = logging.getLogger("email_marketing")

# Opaque outcomes. Callers MUST NOT reveal these to anonymous visitors — doing so
# would let an attacker probe whether an address is already subscribed.
OUTCOME_CONFIRM_SENT = "confirm_sent"
OUTCOME_SUBSCRIBED = "subscribed"
OUTCOME_ALREADY = "already"


def _client_ip(request):
    """Best-effort client IP for consent evidence.

    The X-Forwarded-For head is client-spoofable, so we only ever store a
    *well-formed* address and fall back to REMOTE_ADDR — never a raw header
    value, which would otherwise raise a DataError against the ``inet`` column.
    Returns None when nothing valid is available.
    """
    if request is None:
        return None
    candidates = []
    xff = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if xff:
        candidates.append(xff.split(",")[0].strip())
    candidates.append(request.META.get("REMOTE_ADDR"))
    for ip in candidates:
        if not ip:
            continue
        try:
            validate_ipv46_address(ip)
            return ip
        except ValidationError:
            continue
    return None


def subscribe_email(email, *, request=None, source="signup", language=""):
    """Opt an email address into storefront marketing.

    Creates or refreshes a Subscriber for ``email``, recording consent metadata.
    When the merchant requires double opt-in the subscriber is left pending and a
    confirmation email is queued; otherwise it becomes active immediately.
    Returns an opaque outcome string (see the ``OUTCOME_*`` constants); callers
    must collapse it to a single response so subscription state cannot be probed.
    Raises ``django.core.exceptions.ValidationError`` on a malformed address.
    """
    email = (email or "").strip().lower()
    validate_email(email)

    site = Site.objects.get(pk=1)
    double_opt_in = Subscriber._double_opt_in_required()

    User = get_user_model()
    user = User.objects.filter(email__iexact=email, is_active=True).order_by("date_joined").first()

    # A registered customer's marketing consent must never be flipped by an
    # anonymous, unauthenticated POST without proof of inbox control. When the
    # address matches an account we therefore always require email confirmation,
    # even if the merchant has double opt-in switched off — the emailed token is
    # what authorises mirroring consent into their CommunicationPreference.
    require_confirm = double_opt_in or user is not None

    ip = _client_ip(request)
    ua = request.META.get("HTTP_USER_AGENT", "")[:1000] if request is not None else ""

    with transaction.atomic():
        sub = Subscriber.objects.select_for_update().filter(site=site, email=email).first()

        already_emailable = (
            sub is not None
            and sub.status == Subscriber.STATUS_ACTIVE
            and sub.marketing_opt_in
            and (sub.marketing_verified or not double_opt_in)
        )
        if already_emailable:
            return OUTCOME_ALREADY

        # Anti-bomb: a pending confirmation already stands. Don't rotate its token
        # (which would break the link in the first email) and don't re-send —
        # repeated submits of the same address must not spray confirmation mail.
        if (
            sub is not None
            and require_confirm
            and sub.status == Subscriber.STATUS_PENDING
            and sub.verification_token
        ):
            return OUTCOME_CONFIRM_SENT

        if sub is None:
            sub = Subscriber(site=site, email=email, source=source)

        sub.user = user or sub.user
        sub.marketing_opt_in = True
        sub.consent_source = "storefront_signup"
        sub.consent_ip = ip
        sub.consent_user_agent = ua
        sub.consent_timestamp = timezone.now()
        if language:
            sub.language_code = language

        if require_confirm:
            sub.status = Subscriber.STATUS_PENDING
            sub.marketing_verified = False
            sub.verification_token = generate_token()
            outcome = OUTCOME_CONFIRM_SENT
        else:
            sub.status = Subscriber.STATUS_ACTIVE
            sub.marketing_verified = True
            sub.verification_token = ""
            outcome = OUTCOME_SUBSCRIBED

        try:
            sub.save()
        except IntegrityError:
            # A concurrent signup (or a soft-deleted duplicate) collided on the
            # (site, email) uniqueness. Treat as already handled — non-enumerating.
            logger.info(
                "Subscribe collision for a storefront signup; treating as already-subscribed"
            )
            return OUTCOME_ALREADY

    if outcome == OUTCOME_CONFIRM_SENT:
        _queue_confirmation(sub.pk)
    # Consent is only ever mirrored to a registered account from confirm_subscription
    # (i.e. after the emailed token is presented) — never from this anonymous path.

    return outcome


def confirm_subscription(token):
    """Complete a double opt-in from an emailed confirmation link.

    Idempotent: a second click on an already-confirmed link is a no-op success.
    Returns the Subscriber when the token matched, else ``None`` (an invalid or
    expired link). The token is left in place so re-clicks stay idempotent — the
    ``marketing_verified`` flag, not the token, is what gates sending.
    """
    if not token:
        return None

    sub = Subscriber.objects.filter(verification_token=token).exclude(verification_token="").first()
    if sub is None:
        return None

    if sub.status != Subscriber.STATUS_ACTIVE or not sub.marketing_verified:
        sub.status = Subscriber.STATUS_ACTIVE
        sub.marketing_opt_in = True
        sub.marketing_verified = True
        sub.consent_timestamp = sub.consent_timestamp or timezone.now()
        sub.save(
            update_fields=[
                "status",
                "marketing_opt_in",
                "marketing_verified",
                "consent_timestamp",
                "updated_at",
            ]
        )
        if sub.user_id:
            _mirror_optin_to_preferences(sub.user, verified=True)

    return sub


def _queue_confirmation(subscriber_id):
    """Queue the double opt-in confirmation email (inline fallback if no broker)."""
    from ..tasks import send_subscription_confirmation

    try:
        send_subscription_confirmation.delay(str(subscriber_id))
    except Exception as exc:  # noqa: BLE001 — broker down (e.g. local dev): send inline
        logger.warning("Confirmation email broker unavailable, sending inline: %s", exc)
        try:
            send_subscription_confirmation(str(subscriber_id))
        except Exception:  # noqa: BLE001 — best effort; a failed email must not 500 the signup
            logger.exception("Inline confirmation email failed for subscriber %s", subscriber_id)


def _mirror_optin_to_preferences(user, *, verified):
    """Mirror marketing consent into the linked customer's CommunicationPreference.

    ``Subscriber.is_emailable`` defers to CommunicationPreference for registered
    users, so a storefront opt-in that didn't update it would never actually be
    emailable. Best-effort: a failure here must not break the signup.
    """
    try:
        from accounts.models import CommunicationPreference
        from accounts.services.preference_service import PreferenceService

        prefs, _ = CommunicationPreference.get_or_create_for_user(user)
        changed = []
        if not prefs.email_enabled:
            prefs.email_enabled = True
            changed.append("email_enabled")
        if not prefs.email_marketing:
            prefs.email_marketing = True
            changed.append("email_marketing")
        if verified and not prefs.email_verified:
            prefs.email_verified = True
            prefs.email_verified_at = timezone.now()
            changed += ["email_verified", "email_verified_at"]
        if changed:
            prefs.save(update_fields=changed)
            try:
                PreferenceService.invalidate_cache(user.id)
            except Exception:  # noqa: BLE001 — cache layer is optional
                pass
    except Exception as exc:  # noqa: BLE001 — best-effort mirror
        logger.warning("Could not mirror storefront opt-in to preferences: %s", exc)
