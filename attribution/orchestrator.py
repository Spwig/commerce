"""Unified order-completion orchestrator.

One ``pre_save`` + one ``post_save`` on Order replace the three independent
handlers that previously fired (affiliate commission, referral attribution/
reward, and the attribution reporting resolve). Payout logic is NOT
reimplemented here — the existing, tested domain functions are called verbatim
and each self-guards on order status, so commissions and rewards stay
byte-for-byte identical (invariant #5, pinned by tests/attribution/
test_payout_invariants.py + referrals/tests/test_signals.py). The only change
is that everything now runs from one deterministic entry point, in a fixed
order, and the unified reporting attribution is produced alongside.

Ordering: referral payout → affiliate payout → reporting attribution. Each
stage is isolated so a failure in one never blocks the others or the order save.
"""

import logging

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from attribution.services.resolution import resolve_order

logger = logging.getLogger(__name__)

_COMPLETED_STATUSES = {"completed", "complete", "delivered", "fulfilled"}
_REFUND_STATUSES = {"refunded", "cancelled", "canceled", "returned"}
_REFUND_PAYMENT_STATUSES = {"refunded", "partially_refunded"}

# Rich attribution channels → Order.SOURCE_CHOICES. Kept within the existing
# choices so no orders migration is needed; the full-fidelity channel always
# lives on the Attribution rows. Order.source is only a convenience denormal.
_SOURCE_MAP = {
    "affiliate": "referral",
    "referral": "referral",
    "referral_external": "referral",
    "email": "email",
    "paid_social": "social",
    "organic_social": "social",
    "paid_search": "organic",
    "organic_search": "organic",
    "campaign": "utm_tracked",
    "loyalty": "loyalty",
    "direct": "direct",
}


@receiver(pre_save, sender="orders.Order")
def capture_previous_order_status(sender, instance, **kwargs):
    """Record the pre-save status so the referral handlers can detect a
    transition. Reuses referrals' own capture function unchanged."""
    try:
        from referrals.signals import track_order_status_change

        track_order_status_change(sender, instance)
    except Exception:  # pragma: no cover - never block a save
        logger.exception("attribution: pre_save status capture failed")


@receiver(post_save, sender="orders.Order")
def orchestrate_order(sender, instance, created, **kwargs):
    """Run all order-completion payout + reporting from one entry point."""
    # 1. Referral payout (attribution/reward on completion; reject/revoke on
    #    cancellation). Each self-guards on the status transition.
    try:
        from referrals.signals import handle_order_cancellation, handle_order_completion

        handle_order_completion(sender, instance, created)
        handle_order_cancellation(sender, instance)
    except Exception:  # pragma: no cover
        logger.exception("attribution: referral payout stage failed for order %s", instance.pk)

    # 2. Affiliate payout (commission on completion; reversal on refund).
    try:
        from affiliate.signals import (
            mark_commission_paid_on_order_refund,
            process_order_for_affiliate_commission,
        )

        process_order_for_affiliate_commission(sender, instance, created)
        mark_commission_paid_on_order_refund(sender, instance, created)
    except Exception:  # pragma: no cover
        logger.exception("attribution: affiliate payout stage failed for order %s", instance.pk)

    # 3. Unified reporting attribution + Order.source denormalisation.
    try:
        _resolve_reporting(instance)
    except Exception:  # pragma: no cover
        logger.exception("attribution: reporting stage failed for order %s", instance.pk)


def _bind_order_visitor(order):
    """Bind the checkout visitor's anonymous touch stream to the order's
    customer before resolving.

    Touches captured while logged out (an affiliate link redirect, a ``?ref=``
    click) are stored with ``customer=None``. The login stitch covers shoppers
    who authenticate, but a guest — or a returning customer who clicked while
    logged out — would otherwise resolve to Direct even though the touch exists.
    We reuse referrals' thread-local request to recover the visitor key at
    checkout and bind the stream to this order's customer. No-ops outside a
    request (management commands, etc.) and is idempotent with the login stitch.
    """
    if not order.user_id:
        return
    try:
        from attribution.services.identity import stitch_from_request
        from referrals.middleware import get_current_request

        request = get_current_request()
        if request is not None:
            stitch_from_request(request, order.user)
    except Exception:  # pragma: no cover - best-effort binding
        logger.exception("attribution: order-time visitor bind failed for order %s", order.pk)


def _credit_campaign_vouchers(order):
    """Record a campaign touch for each campaign-linked voucher actually redeemed
    on this order.

    Crediting at order time (from VoucherUsage), not at cart-apply, means a code
    that was applied and then removed before checkout never counts — only codes
    on the finished order do. The touch is a first-party record derived from the
    order's own redemption data (like a commission), bound directly to the
    order's customer and timestamped at the order date so it falls inside the
    lookback window. Idempotent via a synthetic per-order/per-campaign key.
    """
    if not order.user_id:
        return
    try:
        from attribution.constants import CHANNEL_CAMPAIGN, CONSENT_GRANTED
        from attribution.models import TouchPoint
        from vouchers.models import VoucherUsage

        uses = VoucherUsage.objects.filter(
            order=order, voucher__attribution_campaign__isnull=False
        ).select_related("voucher__attribution_campaign")
        for usage in uses:
            campaign = usage.voucher.attribution_campaign
            visitor_key = f"voucher:{order.pk}:{campaign.pk}"
            touch, created = TouchPoint.objects.get_or_create(
                visitor_key=visitor_key,
                channel=CHANNEL_CAMPAIGN,
                campaign_ref=campaign,
                defaults={"customer_id": order.user_id, "consent_state": CONSENT_GRANTED},
            )
            if created:
                # occurred_at is auto_now_add; pin it to the order date so the
                # resolver's lookback window includes it.
                TouchPoint.objects.filter(pk=touch.pk).update(
                    occurred_at=order.created_at, customer_id=order.user_id
                )
    except Exception:  # pragma: no cover - best-effort
        logger.exception("attribution: voucher campaign crediting failed for order %s", order.pk)


def _resolve_reporting(order):
    status = getattr(order, "status", "")
    payment_status = getattr(order, "payment_status", "")
    if not (
        status in _COMPLETED_STATUSES
        or status in _REFUND_STATUSES
        or payment_status in _REFUND_PAYMENT_STATUSES
    ):
        return

    _bind_order_visitor(order)
    _credit_campaign_vouchers(order)
    version = resolve_order(order)
    if not version:
        return

    # Denormalise the highest-weighted primary channel onto Order.source using
    # .update() to bypass save()/signals (no orchestrator recursion).
    from attribution.models import Attribution
    from orders.models import Order

    row = (
        Attribution.objects.filter(order=order, model_version=version, role="primary")
        .order_by("-weight")
        .first()
    )
    if row:
        Order.objects.filter(pk=order.pk).update(source=_SOURCE_MAP.get(row.channel, "unknown"))
