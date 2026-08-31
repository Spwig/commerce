"""Lifecycle signals that start triggered journeys.

Two real events feed the journey engine:

* **customer signup** — a new active, non-staff User → ``customer_signup``.
* **order placed** — a new Order → ``order_placed`` (plus ``first_order`` when
  it's the customer's first).

Each resolves (or creates) the Subscriber for the person, then asks the journey
orchestrator to enroll them. Everything is wrapped so a journey hiccup can never
break signup or checkout. Consent is enforced later, per send, so enrolling a
not-yet-opted-in subscriber simply results in skipped sends.
"""

import logging

from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

logger = logging.getLogger("email_marketing")


def _site():
    from django.contrib.sites.models import Site

    return Site.objects.get(pk=1)


def _get_or_create_subscriber(email, *, user=None, source="manual"):
    """Find or create the Subscriber for an email (single-tenant, site=1)."""
    from email_marketing.models import Subscriber

    email = (email or "").strip().lower()
    if not email:
        return None
    sub, created = Subscriber.objects.get_or_create(
        site=_site(),
        email=email,
        defaults={"user": user, "source": source, "status": Subscriber.STATUS_ACTIVE},
    )
    if user and not sub.user_id:
        sub.user = user
        sub.save(update_fields=["user", "updated_at"])
    return sub


def _has_active_journey(triggers) -> bool:
    """Whether any active journey listens for one of these trigger events."""
    from email_marketing.models import Journey

    return Journey.objects.filter(
        site=_site(), status=Journey.STATUS_ACTIVE, trigger_event__in=triggers
    ).exists()


@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="em_journey_signup")
def enroll_on_signup(sender, instance, created, **kwargs):
    if not created or not instance.is_active or instance.is_staff or not instance.email:
        return
    try:
        from email_marketing.models import Journey

        # Only touch subscribers when a journey is actually listening for this
        # event — with no journey configured this receiver is a complete no-op,
        # so ordinary signups never create marketing rows as a side effect.
        if not _has_active_journey([Journey.TRIGGER_SIGNUP]):
            return
        from email_marketing.services.journeys import trigger_event

        sub = _get_or_create_subscriber(instance.email, user=instance, source="signup")
        if sub:
            trigger_event(Journey.TRIGGER_SIGNUP, sub)
    except Exception as exc:  # noqa: BLE001 — never break account creation
        logger.error("Journey signup trigger failed: %s", exc)


def _order_receiver(sender, instance, created, **kwargs):
    if not created:
        return
    order = instance
    email = order.email or (order.user.email if getattr(order, "user_id", None) else None)
    if not email:
        return
    try:
        from email_marketing.models import Journey

        # No order journey configured → no-op (don't create subscribers per order).
        if not _has_active_journey([Journey.TRIGGER_ORDER_PLACED, Journey.TRIGGER_FIRST_ORDER]):
            return
        from email_marketing.services.journeys import trigger_event

        sub = _get_or_create_subscriber(email, user=getattr(order, "user", None), source="order")
        if not sub:
            return
        trigger_event(Journey.TRIGGER_ORDER_PLACED, sub)

        # First order? Count this customer's orders (by user, else by email).
        from orders.models import Order

        if getattr(order, "user_id", None):
            order_count = Order.objects.filter(user_id=order.user_id).count()
        else:
            order_count = Order.objects.filter(email__iexact=email).count()
        if order_count == 1:
            trigger_event(Journey.TRIGGER_FIRST_ORDER, sub)
    except Exception as exc:  # noqa: BLE001 — never break checkout
        logger.error("Journey order trigger failed: %s", exc)


def _order_pre_save(sender, instance, **kwargs):
    """Stash the order's previous status so the post_save receiver can detect a
    genuine transition INTO 'delivered' (fires the review trigger exactly once)."""
    if not instance.pk:
        instance._em_prev_status = None
        return
    try:
        instance._em_prev_status = (
            sender.objects.filter(pk=instance.pk).values_list("status", flat=True).first()
        )
    except Exception:  # noqa: BLE001 — never break the order save
        instance._em_prev_status = None


def _order_delivered_receiver(sender, instance, created, **kwargs):
    """Fire the order-delivered (post-purchase / review) trigger on the transition.

    This fires on exactly the same signal path as the platform's existing
    delivery-confirmation email (``email_system.signals.send_order_status_emails``,
    also a post_save receiver): both react to a per-order ``.save()``. A raw bulk
    ``Order.objects.filter(...).update(status="delivered")`` (the admin bulk action at
    ``orders/admin.py``) bypasses signals and so sends neither the confirmation email
    nor this trigger — consistent, expected behaviour. The mobile bulk status action
    saves per order, so both fire there.
    """
    if created:
        return
    order = instance
    if order.status != "delivered" or getattr(order, "_em_prev_status", None) == "delivered":
        return  # only on the transition INTO delivered — not every later save
    try:
        # Resolve inside the try: a dangling user FK (email empty, user row deleted)
        # would otherwise raise RelatedObjectDoesNotExist out of the post_save receiver.
        email = order.email or getattr(getattr(order, "user", None), "email", None)
        if not email:
            return
        from email_marketing.models import Journey

        if not _has_active_journey([Journey.TRIGGER_ORDER_DELIVERED]):
            return
        from email_marketing.services.journeys import trigger_event

        sub = _get_or_create_subscriber(email, user=getattr(order, "user", None), source="order")
        if not sub:
            return
        trigger_event(
            Journey.TRIGGER_ORDER_DELIVERED,
            sub,
            context={"order_id": order.id},
            trigger_ref=f"order:{order.id}",
        )
    except Exception as exc:  # noqa: BLE001 — never break the order save
        logger.error("Journey order-delivered trigger failed: %s", exc)


def _connect_order_signal():
    """Connect the order receivers once the Order model is importable."""
    try:
        from orders.models import Order
    except Exception:  # noqa: BLE001 — orders app not ready yet
        return
    post_save.connect(_order_receiver, sender=Order, dispatch_uid="em_journey_order")
    pre_save.connect(_order_pre_save, sender=Order, dispatch_uid="em_order_prev_status")
    post_save.connect(
        _order_delivered_receiver, sender=Order, dispatch_uid="em_journey_order_delivered"
    )


def _engagement_receiver(sender, instance, created, **kwargs):
    """Roll an EmailEvent up onto the campaign's CampaignSend for reporting.

    email_system records opens/clicks/bounces/complaints as ``EmailEvent`` rows
    against an ``EmailOutbox``; this reflects them onto the ``CampaignSend`` linked
    to that outbox so per-campaign open/click **and bounce/complaint** rates (and
    A/B winner metrics) are real. A click implies an open. Keeps email_system
    unaware of email_marketing, and is SEPARATE from address-level suppression
    (``_delivery_event_receiver``) — this is per-send campaign reporting.
    """
    if not created or instance.event_type not in ("opened", "clicked", "bounced", "complained"):
        return

    from email_marketing.models import CampaignSend, JourneyStepSend

    # This fires from the PUBLIC tracking-pixel / click endpoints and ingestion
    # paths — a rollup failure must never bubble up and 500 that request or break
    # event recording.
    try:
        cs = CampaignSend.objects.filter(outbox_id=instance.email_id).first()
        if cs is not None:
            _stamp_engagement(cs, instance, cs.subscriber_id)
            return
        # No CampaignSend → this may be a journey A/B variant send, which records a
        # JourneyStepSend keyed by the same outbox instead. Only opens/clicks roll up
        # there (JourneyStepSend has no bounce columns; journeys aren't campaigns).
        if instance.event_type in ("opened", "clicked"):
            jss = (
                JourneyStepSend.objects.select_related("enrollment")
                .filter(outbox_id=instance.email_id)
                .first()
            )
            if jss is not None:
                _stamp_engagement(jss, instance, jss.enrollment.subscriber_id)
    except Exception:  # noqa: BLE001 — engagement rollup is best-effort
        logger.warning("Campaign engagement rollup failed for event %s", instance.pk, exc_info=True)


def _stamp_engagement(record, event, subscriber_id):
    """Reflect an EmailEvent onto a per-send record (CampaignSend or
    JourneyStepSend). A click implies an open; the first event of each kind wins.
    Bounce/complaint columns are stamped only on records that have them (CampaignSend)."""
    from django.utils import timezone

    from email_marketing.models import Subscriber

    now = event.occurred_at or timezone.now()
    fields = []
    if event.event_type in ("opened", "clicked") and not record.opened:
        record.opened = True
        record.opened_at = now
        fields += ["opened", "opened_at"]
    if event.event_type == "clicked" and not record.clicked:
        record.clicked = True
        record.clicked_at = now
        fields += ["clicked", "clicked_at"]
    # Delivery failures — only CampaignSend carries these columns.
    if event.event_type == "bounced" and hasattr(record, "bounced") and not record.bounced:
        record.bounced = True
        record.bounced_at = now
        record.bounce_type = event.bounce_type or ""
        fields += ["bounced", "bounced_at", "bounce_type"]
    if event.event_type == "complained" and hasattr(record, "complained") and not record.complained:
        record.complained = True
        record.complained_at = now
        fields += ["complained", "complained_at"]
    if fields:
        record.save(update_fields=[*fields, "updated_at"])
        if subscriber_id and "opened" in fields:
            Subscriber.objects.filter(pk=subscriber_id).update(last_opened_at=now)


def _soft_bounce_over_threshold(site, email):
    """True once an address has accumulated enough recent soft bounces to be suppressed.

    Counts soft-bounce ``EmailEvent`` rows for the address (this site) inside a
    rolling window. Threshold and window are tunable via
    ``EMAIL_SOFT_BOUNCE_THRESHOLD`` (default 5) / ``EMAIL_SOFT_BOUNCE_WINDOW_DAYS``
    (default 30). The just-saved event is included in the count.
    """
    from datetime import timedelta

    from django.utils import timezone

    from email_system.models import EmailEvent

    try:
        threshold = max(1, int(getattr(settings, "EMAIL_SOFT_BOUNCE_THRESHOLD", 5)))
    except (TypeError, ValueError):
        threshold = 5
    try:
        window_days = max(1, int(getattr(settings, "EMAIL_SOFT_BOUNCE_WINDOW_DAYS", 30)))
    except (TypeError, ValueError):
        window_days = 30

    cutoff = timezone.now() - timedelta(days=window_days)
    count = EmailEvent.objects.filter(
        email__site=site,
        email__to_email__iexact=email,
        event_type="bounced",
        bounce_type="soft",
        occurred_at__gte=cutoff,
    ).count()
    return count >= threshold


def _delivery_event_receiver(sender, instance, created, **kwargs):
    """Suppress an address when a hard bounce, complaint, or repeated soft bounces land.

    email_system records delivery failures as ``EmailEvent`` rows (bounced /
    complained) against an ``EmailOutbox``; this reflects a HARD bounce or a
    complaint onto the marketing do-not-mail list (email-keyed) and the
    Subscriber immediately. A single SOFT bounce is transient and ignored, but
    once an address accumulates enough recent soft bounces it is effectively
    undeliverable and is suppressed too. Keeps email_system unaware of
    email_marketing (mirrors the engagement rollup).
    """
    if not created or instance.event_type not in ("bounced", "complained"):
        return

    from email_marketing.models import SuppressionEntry
    from email_marketing.services import suppression

    # Fires from an ingestion path (synchronous today via the SMTP-reject event;
    # async gateway poll / provider webhook later) — a failure here must never
    # bubble up or break event recording.
    try:
        outbox = instance.email
        email = getattr(outbox, "to_email", "") if outbox else ""
        site = getattr(outbox, "site", None)
        if not email or site is None:
            return
        if instance.event_type == "complained":
            reason = SuppressionEntry.REASON_COMPLAINT
        elif instance.bounce_type == "hard":
            reason = SuppressionEntry.REASON_HARD_BOUNCE
        elif _soft_bounce_over_threshold(site, email):
            # Repeated soft bounces for one address = effectively undeliverable.
            reason = SuppressionEntry.REASON_SOFT_BOUNCE
        else:
            return  # a single soft / transient bounce is not yet decisive
        valid = {c[0] for c in SuppressionEntry.SOURCE_CHOICES}
        source = (instance.event_data or {}).get("source")
        if source not in valid:
            source = SuppressionEntry.SOURCE_WEBHOOK
        suppression.suppress(
            site,
            email,
            reason=reason,
            source=source,
            detail=(instance.bounce_reason or "")[:1000],
        )
    except Exception:  # noqa: BLE001 — suppression rollup is best-effort
        logger.warning(
            "Suppression from delivery event %s failed",
            getattr(instance, "pk", "?"),
            exc_info=True,
        )


def _connect_engagement_signal():
    """Connect the EmailEvent → CampaignSend rollup once EmailEvent is importable."""
    try:
        from email_system.models import EmailEvent
    except Exception:  # noqa: BLE001 — email_system app not ready yet
        return
    post_save.connect(
        _engagement_receiver, sender=EmailEvent, dispatch_uid="em_campaign_engagement"
    )
    post_save.connect(
        _delivery_event_receiver, sender=EmailEvent, dispatch_uid="em_delivery_suppression"
    )
