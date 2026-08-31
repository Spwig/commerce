"""Inbound email-provider delivery-event webhooks (bounce / complaint / delivered).

A public, CSRF-exempt endpoint that an installed API provider (SES / SendGrid /
Mailgun / Postmark …) posts delivery events to. The provider signature is the only
proof of authenticity, so it is verified BEFORE any state changes. Verified events
are matched to a message we actually sent (an ``EmailOutbox``) and recorded as
``EmailEvent`` rows; ``email_marketing``'s list-hygiene reacts to bounces/complaints.
Mirrors the payment-provider webhook pattern (verify → idempotency → audit → 200-ack).

Security notes:
- Signature verified against an active provider account before any mutation.
- Idempotent on ``(provider_slug, event_id)`` — a redelivered event is a no-op.
- **Ownership check**: an event only acts if its address matches an outbound
  message through this provider — a webhook can never suppress an address we never
  sent to (the ``EmailEvent.email`` FK is non-nullable, which enforces this).
- Acks 200 once events are processed; 400 for a malformed / unverified request; 5xx if
  processing throws AFTER verification, so the provider redelivers and the
  (provider, event_id) idempotency makes the retry a safe no-op (a real
  bounce/complaint is never silently dropped).
- Rate-limited by client IP (unauthenticated JSON parse + a DB lookup precede the
  signature gate).
"""

import hashlib
import json
import logging
import re

from django.db.models import Q
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django_ratelimit.decorators import ratelimit

logger = logging.getLogger("email_system")

# Provider slug is a URL path param on a PUBLIC endpoint — constrain the charset so a
# `%0A`-style injection can't forge a log line, and reject anything exotic fast.
_SLUG_RE = re.compile(r"[a-z0-9_-]+")

# A single webhook delivery can't legitimately carry this many events (the request
# body is already bounded by DATA_UPLOAD_MAX_MEMORY_SIZE); an oversized batch is
# rejected loudly (5xx), never truncated — see _process_events.
_MAX_EVENTS_PER_WEBHOOK = 1000

# Header names an email provider might carry its signature in (last-resort fallback;
# a provider verifier can also read whatever header it likes from ``headers``).
_SIGNATURE_HEADERS = (
    "x-signature",
    "signature",
    "x-webhook-signature",
    "x-mailgun-signature",
    "x-twilio-email-event-webhook-signature",
    "x-amz-sns-message-id",
)

_ACTIONABLE = ("bounced", "complained", "delivered")


def _active_accounts(provider_slug):
    from email_system.models import EmailAccount

    return list(
        EmailAccount.objects.filter(is_active=True).filter(
            Q(component__slug=provider_slug) | Q(provider_key=provider_slug)
        )
    )


def _signature(headers):
    norm = {k.lower(): v for k, v in headers.items()}
    for name in _SIGNATURE_HEADERS:
        if name in norm:
            return norm[name]
    return ""


@csrf_exempt
@require_POST
@ratelimit(key="ip", rate="120/m", method="POST", block=True)
def email_webhook_handler(request, provider_slug):
    """Ingest a delivery-event webhook from an installed email provider."""
    from email_system.models import EmailProviderWebhook

    # Reject a malformed slug fast (before any DB work); also stops a %0A in the
    # path param from becoming a forged log line.
    if not _SLUG_RE.fullmatch(provider_slug or ""):
        return HttpResponse(status=400)

    raw = request.body
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError, RecursionError):
        # ValueError covers JSONDecodeError; RecursionError guards deeply-nested JSON.
        return HttpResponse(status=400)
    if not isinstance(payload, dict):
        return HttpResponse(status=400)

    headers = dict(request.headers.items())
    signature = _signature(headers)

    accounts = _active_accounts(provider_slug)
    if not accounts:
        logger.warning("Email webhook for unknown/inactive provider: %s", provider_slug)
        return HttpResponse(status=400)

    # The signature is the only authenticity proof on this public endpoint — verify
    # against ANY active account for the provider before touching state.
    verified_provider = None
    verified_account = None
    for account in accounts:
        try:
            provider = account.get_provider_instance()
        except Exception:  # noqa: BLE001 — a misconfigured account must not 500 the endpoint
            logger.warning(
                "Webhook: provider init failed for account %s", account.pk, exc_info=True
            )
            continue
        try:
            if signature and provider.verify_webhook_signature(raw, signature, headers):
                verified_provider = provider
                verified_account = account
                break
        except Exception:  # noqa: BLE001
            logger.warning("Webhook verify errored for account %s", account.pk, exc_info=True)
    if verified_provider is None:
        logger.warning("Email webhook signature verification failed: %s", provider_slug)
        return HttpResponse(status=400)

    event_id = str(payload.get("id") or payload.get("event_id") or payload.get("messageId") or "")
    if not event_id:
        # No stable id → dedup on the body hash so an identical redelivery is a no-op.
        event_id = hashlib.sha256(raw).hexdigest()

    # Persist the audit row first (idempotency + traceability), then process.
    record, _created = EmailProviderWebhook.objects.get_or_create(
        provider_slug=provider_slug,
        event_id=event_id,
        defaults={"payload": payload, "headers": headers, "signature_verified": True},
    )
    if record.processed:
        return HttpResponse(status=200)  # duplicate — ack, don't reprocess

    try:
        # Scope matching to the account that verified the signature — a webhook
        # signed by one account must never act on another account's sends.
        _process_events(verified_provider, provider_slug, [verified_account], payload, record)
    except Exception as e:  # noqa: BLE001
        # Persist the error for traceability and return 5xx so the provider
        # redelivers — the (provider, event_id) idempotency makes the retry safe,
        # and a real bounce/complaint isn't silently dropped (never suppressed).
        record.processing_error = str(e)[:2000]
        record.save(update_fields=["processing_error", "event_type"])
        logger.error("Email webhook processing failed for %s: %s", provider_slug, e, exc_info=True)
        return HttpResponse(status=500)
    record.processed = True
    record.processed_at = timezone.now()
    record.save(update_fields=["processed", "processed_at", "event_type"])
    return HttpResponse(status=200)


def _process_events(provider, provider_slug, accounts, payload, record):
    """Match each parsed delivery event to a sent EmailOutbox and record an EmailEvent."""
    from email_system.models import EmailEvent

    events = provider.parse_delivery_events(payload) or []
    if len(events) > _MAX_EVENTS_PER_WEBHOOK:
        # Never silently truncate — a real provider doesn't batch this many, and a
        # slice would drop the tail while the audit row is marked processed, losing
        # those bounces forever (idempotency blocks redelivery). Raise → the caller
        # 5xxes, so it's loud, retryable, and nothing is dropped.
        raise ValueError(f"webhook batch too large: {len(events)} events")

    account_ids = [a.id for a in accounts]
    seen_types = []
    for ev in events:
        etype = ev.get("event_type")
        if etype not in _ACTIONABLE:
            continue
        outbox = _match_outbox(ev, account_ids)
        if outbox is None:
            # Only act on addresses we actually sent to — never suppress an address
            # supplied in a webhook payload with no matching outbound message.
            logger.info(
                "Webhook %s %s event for %r has no matching outbox; skipped",
                provider_slug,
                etype,
                ev.get("email"),
            )
            continue
        seen_types.append(etype)
        # Don't double-record the same event type for the same message.
        if EmailEvent.objects.filter(email=outbox, event_type=etype).exists():
            continue
        EmailEvent.objects.create(
            email=outbox,
            event_type=etype,
            bounce_type=(ev.get("bounce_type") or "") if etype == "bounced" else "",
            bounce_reason=(ev.get("reason") or "")[:2000],
            event_data={
                "source": "webhook",
                "provider": provider_slug,
                "event_id": ev.get("event_id"),
            },
        )
    if seen_types:
        record.event_type = ",".join(sorted(set(seen_types)))[:64]


def _match_outbox(ev, account_ids):
    """Find the outbound message a webhook event refers to (the ownership check).

    By ``provider_message_id`` first (exact), else the most recent send to the
    address through one of this provider's accounts. Returns None when we never
    sent to it — so an unknown address is skipped, not suppressed.
    """
    from email_system.models import EmailOutbox

    # Only a message we actually handed to the provider can bounce/complain — a
    # queued / failed / skipped row must never be matched (and suppressed) by address.
    sent = ("sent", "bounced")
    pmid = ev.get("provider_message_id")
    if pmid:
        ob = EmailOutbox.objects.filter(
            provider_message_id=pmid, account_id__in=account_ids, status__in=sent
        ).first()
        if ob is not None:
            return ob
    email = (ev.get("email") or "").strip()
    if not email:
        return None
    return (
        EmailOutbox.objects.filter(
            to_email__iexact=email, account_id__in=account_ids, status__in=sent
        )
        .order_by("-created_at")
        .first()
    )
