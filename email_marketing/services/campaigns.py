"""Campaign send path — turn an authored campaign into per-recipient outbox rows.

``send_campaign`` resolves the target audience, renders the MJML once, then
queues one consent-checked email per subscriber via the ``email_system`` send
service and records a ``CampaignSend`` linking each outbox row. Actual delivery
is performed later by the throttled batch drainer (``tasks.drain_campaign_outbox``).

Consent is enforced twice by design: ``Subscriber.is_emailable`` gates before
queueing (the only gate anonymous leads get, since ``email_system``'s own gate
keys off a User row), and ``queue_email`` re-checks registered users.
"""

import logging

from django.contrib.sites.models import Site
from django.db import IntegrityError, transaction
from django.template import Context, Template

from email_marketing.merge_fields import resolve_merge_fields

logger = logging.getLogger("email_marketing")


def _render_mjml(mjml_source: str) -> str:
    """Compile MJML to email-safe HTML once (merge tags pass through untouched)."""
    from mjml.mjml2html import mjml_to_html

    result = mjml_to_html(mjml_source)
    if result.get("errors"):
        messages = [f"{e.get('line')}:{e.get('message')}" for e in result["errors"]]
        raise ValueError(f"MJML validation errors: {'; '.join(messages)}")
    return result["html"]


def html_to_text(html: str) -> str:
    """A readable plain-text alternative from a rendered HTML email (dependency-free).

    MJML output carries its CSS in ``<style>`` and metadata in ``<head>``, so those
    blocks are dropped first (else ``strip_tags`` would leak raw CSS into the text).
    Remaining tags are stripped, entities unescaped, and runs of blank lines collapsed.
    Good enough for a ``text/plain`` part; not a pixel-perfect rendering.
    """
    import re
    from html import unescape

    from django.utils.html import strip_tags

    if not html:
        return ""
    # Drop non-content blocks whose text must never appear in the plain part.
    cleaned = re.sub(r"(?is)<(script|style|head)\b.*?</\1>", " ", html)
    # Preserve a line break for common block boundaries before stripping tags.
    # Handles <br>, <br/>, <br /> and the closing block tags.
    cleaned = re.sub(r"(?i)<(?:br\s*/?|/(?:p|div|tr|h[1-6]|li))\s*>", "\n", cleaned)
    text = unescape(strip_tags(cleaned))
    # Collapse trailing spaces and runs of >2 blank lines.
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _strip_newlines(value):
    """Neutralise CR/LF so merge values can't inject email headers.

    Django's auto-escaping does not strip newlines, and recipient-controlled
    fields (e.g. a customer's first name) can reach the Subject header, which
    the stdlib email module does not defend. Collapse newlines to spaces.
    """
    if isinstance(value, str):
        return value.replace("\r", " ").replace("\n", " ")
    return value


def _merge_context(subscriber, campaign, unsubscribe_url: str) -> dict:
    """Per-recipient template context for merge tags (header-injection safe)."""
    first_name = ""
    if subscriber.user_id and subscriber.user.first_name:
        first_name = subscriber.user.first_name
    ctx = {
        "first_name": first_name,
        "email": subscriber.email,
        "unsubscribe_url": unsubscribe_url,
        "preview_text": campaign.preview_text,
    }
    return {key: _strip_newlines(val) for key, val in ctx.items()}


def _anonymous_unsubscribe_footer(html_body: str, unsubscribe_url: str) -> str:
    """Append a CAN-SPAM/GDPR-compliant unsubscribe footer for anonymous leads.

    email_system only footers recipients that have a CommunicationPreference, so
    anonymous subscribers would otherwise receive marketing with no opt-out.
    """
    if "/marketing/unsubscribe/" in html_body or "/accounts/unsubscribe/" in html_body:
        return html_body
    footer = f"""
    <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #e0e0e0; font-family: system-ui, -apple-system, sans-serif; font-size: 12px; color: #666; text-align: center;">
        <p style="margin: 0 0 10px 0;">You received this email because you subscribed to our updates.</p>
        <p style="margin: 0;">
            <a href="{unsubscribe_url}" style="color: #0066cc; text-decoration: underline;">Unsubscribe</a>
        </p>
    </div>
    """
    if "</body>" in html_body:
        return html_body.replace("</body>", f"{footer}</body>")
    return html_body + footer


def _recipient_queryset(campaign):
    """Resolve the campaign's audience: its segment, or all active subscribers.

    ``select_related("user")`` so per-recipient merge fields (name, loyalty
    points) don't add a query per subscriber.
    """
    from email_marketing.models import Subscriber

    if campaign.segment_id:
        qs = campaign.segment.resolve_queryset()
    else:
        qs = Subscriber.objects.filter(site=campaign.site, status=Subscriber.STATUS_ACTIVE)
    return qs.select_related("user")


def _queue_for_subscriber(campaign, sub, site, account, body_template, base_subject):
    """Personalise and queue one email for one subscriber; return the outbox.

    The caller must have consent-checked (``is_emailable``) already. Shared by
    the broadcast loop and the single-subscriber triggered-journey send so both
    get identical merge-field personalisation and the anonymous-lead footer.
    """
    from email_system.services.email_sender import EmailSendingService

    unsubscribe_url = f"https://{site.domain}/marketing/unsubscribe/{sub.unsubscribe_token}/"
    ctx = _merge_context(sub, campaign, unsubscribe_url)
    html_body = body_template.render(Context(ctx))
    # Personalisation merge fields ([[first_name]], …) — resolved by plain
    # allowlisted substitution (no template engine), HTML-escaped in the body.
    html_body = resolve_merge_fields(html_body, sub, html=True)
    # Personalise the subject via [[ ]] merge fields (header-safe: values are
    # newline-stripped). No Django templating of the subject → no SSTI.
    subject = resolve_merge_fields(base_subject, sub, html=False)

    if not sub.user_id:
        html_body = _anonymous_unsubscribe_footer(html_body, unsubscribe_url)

    # Plain-text alternative from the final HTML (before tracking, which only rewrites
    # the HTML part): a multipart/alternative message is standard for bulk mail and a
    # mild deliverability + accessibility win over HTML-only.
    text_body = html_to_text(html_body)

    from email_system.models import EmailOutbox

    from .attribution_link import ensure_attribution_campaign

    # Per-campaign revenue attribution: ensure the attribution.Campaign exists and
    # stamp its slug on the outbox so tracked links carry utm_campaign=<slug> and a
    # converting click credits revenue back to THIS campaign. Best-effort (None on
    # failure) so attribution can never block a send.
    attribution_slug = ensure_attribution_campaign(campaign) or ""

    outbox = EmailSendingService.queue_email(
        to_email=sub.email,
        subject=subject,
        html_body=html_body,
        text_body=text_body,
        template_type=campaign.message_type,
        account=account,
        site=site,
        tags=["campaign", str(campaign.id)],
        attribution_campaign=attribution_slug,
        # RFC 8058 one-click unsubscribe. Gmail/Yahoo require these headers for bulk
        # senders; the URL carries the subscriber's token and the endpoint unsubscribes
        # on a bare POST (csrf-exempt, token-authenticated). https-only — there is no
        # inbound unsubscribe mailbox. Value is domain + a safe token: no CRLF surface.
        headers={
            "List-Unsubscribe": f"<{unsubscribe_url}>",
            "List-Unsubscribe-Post": "List-Unsubscribe=One-Click",
        },
        # Marketing (campaigns + journeys both flow through here): throttleable, and
        # yields SMTP headroom to transactional mail under the per-account budget.
        priority=EmailOutbox.PRIORITY_MARKETING,
    )
    _add_open_click_tracking(outbox)
    return outbox


def _add_open_click_tracking(outbox) -> None:
    """Inject the open pixel + click-tracking into a queued campaign email.

    The campaign path renders its own HTML and calls ``queue_email`` directly,
    which (unlike ``send_template_email``) does not add tracking — so without this
    campaign opens/clicks are never measured. Keyed to the outbox id, the same id
    ``track_open`` / ``track_click`` resolve. Best-effort: a tracking failure must
    never break the send.
    """
    if not outbox or getattr(outbox, "status", None) != "queued":
        return
    try:
        from email_system.services.tracking_service import TrackingService

        tracked = TrackingService().add_tracking(outbox.html_body, str(outbox.id))
        if tracked and tracked != outbox.html_body:
            outbox.html_body = tracked
            outbox.save(update_fields=["html_body"])
    except Exception:  # noqa: BLE001 — tracking is best-effort, never fatal to a send
        logger.warning(
            "Could not add tracking to campaign outbox %s",
            getattr(outbox, "id", "?"),
            exc_info=True,
        )


def send_campaign_to_subscriber(campaign, subscriber, subject_override=None, event_context=None):
    """Render ``campaign`` for one subscriber and queue it (triggered journeys).

    Renders the campaign's saved MJML fresh, applies the same consent gate and
    merge-field personalisation as a broadcast, and queues one email. Unlike
    ``send_campaign`` it creates **no** CampaignSend row — a journey tracks
    delivery per enrollment, and the same step email may legitimately be sent to
    one subscriber across separate enrollments (e.g. an order-triggered series
    firing once per order). ``subject_override`` swaps the subject line (used by a
    journey subject-line A/B, where each arm shares the content).

    ``event_context`` is a triggered journey's event payload (e.g. ``{"cart_id": 123}``).
    When present, the campaign's blocks are RE-serialized for this subscriber so a
    per-recipient dynamic block (an abandoned-cart block) resolves the subscriber's
    live cart/product — rather than the shared ``html_content`` baked at save time.
    Returns a small result dict including the ``outbox_id`` of the queued email.
    """
    from email_marketing.services import suppression
    from email_system.services.email_sender import EmailSendingService

    if suppression.is_suppressed(campaign.site, subscriber.email):
        return {"queued": False, "reason": "suppressed"}

    if not subscriber.is_emailable(campaign.message_type):
        return {"queued": False, "reason": "not_emailable"}

    account = campaign.from_account or EmailSendingService.get_default_account(site=campaign.site)
    if not account:
        return {"queued": False, "reason": "no_account"}

    site = campaign.site or Site.objects.get_current()
    if event_context and campaign.blocks.exists():
        from email_marketing.services.block_serializer import serialize_campaign

        mjml_doc = serialize_campaign(
            campaign, extra_ctx={"event": event_context, "subscriber": subscriber}
        )
    else:
        mjml_doc = campaign.html_content or ""
    body_template = Template(_render_mjml(mjml_doc))
    raw_subject = subject_override if subject_override else (campaign.subject or "")
    base_subject = " ".join(raw_subject.splitlines()).strip()

    outbox = _queue_for_subscriber(campaign, subscriber, site, account, body_template, base_subject)
    return {
        "queued": outbox.status == "queued",
        "reason": outbox.status,
        "outbox_id": str(outbox.id),
    }


def send_campaign(campaign, recipients=None, variant_label=""):
    """Queue a campaign to its audience (or an explicit ``recipients`` subset).

    Renders the email once, then creates a consent-checked outbox row and a
    CampaignSend per recipient. Returns a summary dict. Delivery happens
    asynchronously via the batch drainer; this only enqueues.

    ``recipients`` — an explicit iterable of Subscribers to send to instead of the
    campaign's whole segment (used by A/B testing to send a variant to its bucket
    and the winner to the holdout). ``variant_label`` stamps ``CampaignSend.variant``.
    """
    from email_marketing.models import Campaign, CampaignSend
    from email_system.services.email_sender import EmailSendingService

    # Claim the campaign atomically so a scheduled dispatch and an admin
    # "Send now" (or two workers) can't both proceed and double-send.
    claimed = Campaign.objects.filter(
        id=campaign.id, status__in=[campaign.STATUS_DRAFT, campaign.STATUS_SCHEDULED]
    ).update(status=campaign.STATUS_SENDING)
    if not claimed:
        campaign.refresh_from_db(fields=["status"])
        logger.warning("Campaign %s is %s; refusing to send", campaign.id, campaign.status)
        return {"error": "invalid_status", "status": campaign.status}
    campaign.status = campaign.STATUS_SENDING

    account = campaign.from_account or EmailSendingService.get_default_account(site=campaign.site)
    if not account:
        campaign.status = campaign.STATUS_FAILED
        campaign.save(update_fields=["status", "updated_at"])
        logger.error("Campaign %s has no email account available", campaign.id)
        return {"error": "no_account"}

    site = campaign.site or Site.objects.get_current()
    compiled_html = _render_mjml(campaign.html_content or "")
    body_template = Template(compiled_html)
    # The subject is plain text: personalise it with allowlisted [[ ]] merge
    # fields only — never the Django template engine — so a marketing-category
    # staffer can't put a `{{ ... }}` SSTI payload in the subject line.
    base_subject = " ".join((campaign.subject or "").splitlines()).strip()

    audience = recipients if recipients is not None else _recipient_queryset(campaign).iterator()

    # List hygiene: preload the site's do-not-mail set once (bounced / complained /
    # manually-blocked addresses), then skip in-loop — O(1), no per-recipient query.
    from email_marketing.services import suppression

    suppressed = suppression.suppressed_emails(site)

    queued = skipped = 0
    for sub in audience:
        # Claim the (campaign, subscriber) row FIRST. The unique constraint makes
        # this the serialisation point: a concurrent run loses the create here
        # and skips, so no duplicate outbox/email is ever produced.
        try:
            # Savepoint so a duplicate only rolls back this create, never an
            # enclosing transaction a future caller might wrap us in.
            with transaction.atomic():
                cs = CampaignSend.objects.create(
                    campaign=campaign,
                    subscriber=sub,
                    status=CampaignSend.STATUS_PENDING,
                    variant=variant_label,
                )
        except IntegrityError:
            continue

        if (sub.email or "").strip().lower() in suppressed:
            cs.status = CampaignSend.STATUS_SKIPPED
            cs.skip_reason = "suppressed"
            cs.save(update_fields=["status", "skip_reason", "updated_at"])
            skipped += 1
            continue

        if not sub.is_emailable(campaign.message_type):
            cs.status = CampaignSend.STATUS_SKIPPED
            cs.skip_reason = "not_emailable"
            cs.save(update_fields=["status", "skip_reason", "updated_at"])
            skipped += 1
            continue

        outbox = _queue_for_subscriber(campaign, sub, site, account, body_template, base_subject)

        cs.outbox = outbox
        if outbox.status == "queued":
            cs.status = CampaignSend.STATUS_QUEUED
            queued += 1
        elif outbox.status == "skipped":
            cs.status = CampaignSend.STATUS_SKIPPED
            cs.skip_reason = outbox.skip_reason or "email_system_skipped"
            skipped += 1
        else:
            # held / logged / sandbox_logged — not delivered in this mode.
            cs.status = CampaignSend.STATUS_SKIPPED
            cs.skip_reason = outbox.status
            skipped += 1
        cs.save(update_fields=["outbox", "status", "skip_reason", "updated_at"])

    campaign.total_recipients = queued + skipped
    campaign.skipped_count = skipped
    campaign.save(update_fields=["total_recipients", "skipped_count", "updated_at"])

    logger.info("Campaign %s enqueued: %d queued, %d skipped", campaign.id, queued, skipped)
    return {"queued": queued, "skipped": skipped, "total": queued + skipped}
