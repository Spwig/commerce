"""Hosted-gateway bounce/complaint poll → list hygiene (Stage 3).

The Spwig mail gateway performs the actual SMTP delivery, so an asynchronous
("delayed") bounce or a Feedback-Loop complaint is recorded on the gateway and
never reaches this install synchronously. For a Spwig-hosted deployment we PULL
that log on a schedule and feed each record into the same Stage-1 suppression
seam used by the SMTP-reject and provider-webhook paths:

- match the record to a message we actually sent → record an ``EmailEvent`` (the
  ``email_marketing`` receiver then suppresses hard bounces / complaints — and
  reflects onto the subscriber — and counts soft bounces toward the threshold);
- no matching outbox → suppress the ADDRESS only for a hard bounce / complaint
  (``reflect=False``: no send trail means no destructive subscriber relabel /
  forced unsubscribe off an unverified external address). Soft bounces with no
  outbox are dropped — a threshold needs a message trail.

Pull-only and idempotent (per gateway record id, at account scope so a later send
to the same address can't cause a re-count). A **no-op** unless (a) an active
hosted account exists and (b) the gateway management API is explicitly configured
(``SPWIG_MAIL_GATEWAY_API_URL`` + ``SPWIG_MAIL_GATEWAY_API_KEY``) — so a Community
install on its own gateway, or an un-provisioned dev install, does nothing. The
base URL is NEVER derived from stored credentials: this call carries the fleet
management key, so it must only ever be sent to the operator-pinned URL.
"""

import hashlib
import logging

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

logger = logging.getLogger("email_marketing")

_HOSTED_PROVIDER_KEY = "spwig_hosted_mail"

# A single poll can't legitimately carry an unbounded bounce log; cap the work per
# tick so a large or hostile response can't turn one beat into a write/suppress storm.
_MAX_GATEWAY_RECORDS = 1000


def _active_hosted_account():
    """Return the active hosted (gateway) EmailAccount, preferring the default, or None."""
    from email_system.models import EmailAccount

    return (
        EmailAccount.objects.filter(provider_key=_HOSTED_PROVIDER_KEY, is_active=True)
        .order_by("-is_default")
        .first()
    )


def _records(payload):
    """Normalise the gateway bounce response into a flat list of record dicts."""
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("bounces", "records", "results", "events"):
            val = payload.get(key)
            if isinstance(val, list):
                return val
    return []


def _classify(rec):
    """Map a gateway record to (event_type, bounce_type) or (None, None) to skip.

    The explicit ``bounce_type`` (hard/soft) wins over the coarser ``type``/``event``
    label, so a generic "bounce" that carries ``bounce_type=soft`` is treated as a
    soft bounce, not mis-escalated to an immediate hard suppression.
    """
    label = str(rec.get("type") or rec.get("event") or "").lower()
    if "complaint" in label or "complained" in label or "abuse" in label or label == "fbl":
        return "complained", ""

    btype = str(rec.get("bounce_type") or "").lower()
    if btype.startswith("hard"):
        return "bounced", "hard"
    if btype.startswith("soft") or btype in ("transient", "deferred", "delayed"):
        return "bounced", "soft"

    # No explicit bounce_type → fall back to the coarse label (soft before hard so a
    # "soft bounce" label isn't caught by the generic "bounce" test).
    if "soft" in label or "transient" in label or "defer" in label or "delay" in label:
        return "bounced", "soft"
    if "hard" in label or label in ("bounce", "bounced", "block", "blocked"):
        return "bounced", "hard"
    return None, None


def _dedup_key(rec, email, etype, btype):
    """Stable id for a gateway record, or "" when it can't be identified safely.

    Prefers the gateway's own id; else derives one from address + type + the record
    timestamp. A record with neither an id nor a timestamp has no stable identity —
    returning "" tells the caller to skip it rather than re-count it every poll.
    """
    rid = str(rec.get("id") or rec.get("event_id") or "").strip()
    if rid:
        return rid
    ts = str(
        rec.get("timestamp")
        or rec.get("occurred_at")
        or rec.get("created_at")
        or rec.get("date")
        or ""
    ).strip()
    if not ts:
        return ""
    return hashlib.sha256(f"{email}|{etype}|{btype}|{ts}".encode()).hexdigest()


def _recent_outbox(site, account, email):
    """Most recent truly-sent message to this address on the hosted account, or None."""
    from email_system.models import EmailOutbox

    return (
        EmailOutbox.objects.filter(
            site=site,
            account=account,
            to_email__iexact=email,
            status__in=("sent", "bounced"),
        )
        .order_by("-created_at")
        .first()
    )


def _already_ingested(account, rid):
    """True if this gateway record id was already recorded for the account.

    Scoped to the ACCOUNT (not a single outbox) so a later send to the same address
    — which would move ``_recent_outbox`` to a newer row — can't cause the same
    record to be re-recorded and falsely advance the soft-bounce threshold.
    """
    from email_system.models import EmailEvent

    return EmailEvent.objects.filter(email__account=account, event_data__event_id=rid).exists()


def ingest_hosted_gateway_bounces(client=None):
    """Pull the hosted gateway's bounce/complaint log and feed it into list hygiene.

    Returns a small summary dict (also used by tests). Never raises for an expected
    condition (unconfigured, no account, gateway error) — the caller is a Celery beat.
    """
    from email_marketing.models import SuppressionEntry
    from email_marketing.services import suppression
    from email_system.models import EmailEvent

    account = _active_hosted_account()
    if account is None:
        return {"skipped": "no_hosted_account"}

    creds = {}
    try:
        creds = account.get_credentials() or {}
    except Exception:  # noqa: BLE001 — a corrupt credential blob must not crash the beat
        logger.warning("Hosted bounce poll: could not read account credentials", exc_info=True)

    slug = (creds.get("auth_user") or "").strip()
    api_key = getattr(settings, "SPWIG_MAIL_GATEWAY_API_KEY", None)
    # The base URL is operator-pinned and NEVER derived from stored credentials: this
    # request carries the fleet management key, so it must only reach the trusted URL.
    base_url = getattr(settings, "SPWIG_MAIL_GATEWAY_API_URL", None)
    if client is None and (not slug or not api_key or not base_url):
        # Not a live hosted install (or infra not provisioned yet) → do nothing.
        return {"skipped": "not_configured"}

    if client is None:
        from email_system.providers.spwig_hosted.gateway_client import SpwigMailGatewayClient

        client = SpwigMailGatewayClient(base_url=base_url, api_key=api_key)

    try:
        payload = client.get_merchant_bounces(slug)
    except Exception as e:  # noqa: BLE001 — network / gateway error: log and retry next tick
        logger.warning("Hosted bounce poll: gateway call failed: %s", e, exc_info=True)
        return {"error": "gateway_unreachable"}

    site = account.site
    summary = {"recorded": 0, "suppressed": 0, "skipped": 0}

    records = _records(payload)
    if len(records) > _MAX_GATEWAY_RECORDS:
        logger.warning(
            "Hosted bounce poll: %d records exceeds cap %d; processing the first %d",
            len(records),
            _MAX_GATEWAY_RECORDS,
            _MAX_GATEWAY_RECORDS,
        )
        records = records[:_MAX_GATEWAY_RECORDS]

    for rec in records:
        email = (rec.get("email") or rec.get("recipient") or "").strip().lower()
        etype, btype = _classify(rec)
        if not email or etype is None:
            summary["skipped"] += 1
            continue
        try:
            validate_email(email)
        except ValidationError:
            # Junk address from the gateway → never let it pollute the do-not-mail list.
            summary["skipped"] += 1
            continue

        rid = _dedup_key(rec, email, etype, btype)
        if not rid or _already_ingested(account, rid):
            summary["skipped"] += 1
            continue

        reason_text = (rec.get("reason") or rec.get("detail") or rec.get("diagnostic") or "")[:2000]
        outbox = _recent_outbox(site, account, email)
        if outbox is not None:
            # Has a send trail → record the event; the receiver suppresses (hard /
            # complaint, with subscriber reflection) or counts it (soft).
            EmailEvent.objects.create(
                email=outbox,
                event_type=etype,
                bounce_type=btype,
                bounce_reason=reason_text,
                event_data={"source": SuppressionEntry.SOURCE_GATEWAY_POLL, "event_id": rid},
            )
            summary["recorded"] += 1
            continue

        # No message trail: only a hard bounce / complaint is decisive enough to
        # block the address, and reflect=False keeps a registered subscriber's
        # status/consent untouched off this unverified gateway address.
        if etype == "complained":
            sup_reason = SuppressionEntry.REASON_COMPLAINT
        elif btype == "hard":
            sup_reason = SuppressionEntry.REASON_HARD_BOUNCE
        else:
            summary["skipped"] += 1
            continue
        # The direct path can't hang a per-record id on an EmailEvent (there's no
        # outbox), so dedup on the do-not-mail list. If the address is already
        # suppressed, re-writing is worth it ONLY for a genuine hard → complaint
        # upgrade — never overwrite a manual block, a soft-bounce entry, or downgrade
        # an existing complaint, and never re-count an unchanged repeat each tick.
        existing = SuppressionEntry.objects.filter(site=site, email=email).first()
        if existing is not None:
            is_upgrade = (
                sup_reason == SuppressionEntry.REASON_COMPLAINT
                and existing.reason == SuppressionEntry.REASON_HARD_BOUNCE
            )
            if not is_upgrade:
                summary["skipped"] += 1
                continue
        suppression.suppress(
            site,
            email,
            reason=sup_reason,
            source=SuppressionEntry.SOURCE_GATEWAY_POLL,
            detail=reason_text[:1000],
            reflect=False,
        )
        summary["suppressed"] += 1

    return summary
