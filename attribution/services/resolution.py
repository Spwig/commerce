"""Resolve an order's touch stream into versioned attribution rows.

Reads the customer's touches within the lookback window, applies the active
model, and writes ``Attribution`` rows dividing the order's net revenue. Rows
are immutable and forward-only: a re-resolution (model change, or a refund that
changes net) writes a *new* ``model_version`` batch and leaves prior batches
intact — the newest batch is the current attribution. This mirrors the
affiliate ``Commission`` immutability invariant.

Primary rows only, by design: their weights sum to 1.0 so total attributed
revenue reconciles to net revenue (invariant #1). The retained touch stream
lets the reporting layer derive assisted-revenue as a read-time lens without
materialising it here.
"""

import logging
from datetime import timedelta
from decimal import Decimal

from django.db import transaction

from attribution.constants import CHANNEL_DIRECT, ROLE_PRIMARY
from attribution.services.attribution_models import compute_weights
from attribution.services.revenue import CENTS, attributable_net

logger = logging.getLogger(__name__)


def touches_for_order(order, lookback_days):
    """Ordered (oldest→newest) touches eligible to receive credit for ``order``.

    Bound to the order's customer and within the lookback window ending at the
    order's creation time. Guest orders with no bound customer yield nothing
    until their stream is stitched (the orchestrator attempts a stitch first).
    """
    from attribution.models import TouchPoint

    if not order.user_id:
        return []
    order_time = order.created_at
    since = order_time - timedelta(days=lookback_days)
    return list(
        TouchPoint.objects.filter(
            customer_id=order.user_id,
            occurred_at__lte=order_time,
            occurred_at__gte=since,
            is_bot=False,
        ).order_by("occurred_at")
    )


def _latest_batch(order):
    """Return (model_version, model, net_amount, touch_ids) of the newest batch.

    ``touch_ids`` is the frozenset of touchpoint ids the batch credited (``{None}``
    for a Direct-fallback batch). It lets the idempotency check detect a changed
    touch *composition* even when net revenue is unchanged — e.g. a Direct order
    that later has a touch stitched in at the same value must re-resolve, not
    no-op. Returns None if the order has no attribution yet.
    """
    from django.db.models import Sum

    from attribution.models import Attribution

    latest = (
        Attribution.objects.filter(order=order, role=ROLE_PRIMARY)
        .order_by("-created_at", "-id")
        .first()
    )
    if not latest:
        return None
    batch = Attribution.objects.filter(
        order=order, role=ROLE_PRIMARY, model_version=latest.model_version
    )
    net_amount = batch.aggregate(s=Sum("amount"))["s"] or Decimal("0")
    touch_ids = frozenset(batch.values_list("touchpoint_id", flat=True))
    model = latest.model_version.split("#", 1)[0]
    return latest.model_version, model, net_amount.quantize(CENTS), touch_ids


def _next_version(order, model):
    from attribution.models import Attribution

    # .order_by() clears Attribution.Meta.ordering; without it Django adds
    # created_at to the SELECT and DISTINCT counts rows, not versions.
    seq = (
        Attribution.objects.filter(order=order)
        .order_by()
        .values("model_version")
        .distinct()
        .count()
    )
    return f"{model}#{seq + 1}"


@transaction.atomic
def resolve_order(order, *, force=False):
    """(Re)resolve attribution for ``order``. Returns the model_version written,
    or the existing version if skipped as a no-op, or None if nothing to attribute.
    """
    from attribution.models import Attribution, AttributionSettings

    settings = AttributionSettings.get_settings()
    net = attributable_net(order)
    touches = touches_for_order(order, settings.lookback_days)
    current_touch_ids = frozenset(t.id for t in touches) if touches else frozenset({None})

    # Idempotency: skip only if the newest batch already reflects this model, this
    # net revenue AND this exact touch composition. Comparing the touch set (not
    # just net) is what lets a Direct order re-resolve when a touch stitches in.
    latest = _latest_batch(order)
    if latest and not force:
        _version, _model, _net, _ids = latest
        if _model == settings.active_model and _net == net["amount"] and _ids == current_touch_ids:
            return _version

    version = _next_version(order, settings.active_model)

    if touches:
        weights = compute_weights(
            touches, settings.active_model, order.created_at, settings.time_decay_half_life_days
        )
        rows = [
            _build_row(
                order, touch, touch.channel, touch.campaign_ref, weight, weight, net, version
            )
            for touch, weight in weights
        ]
        # Absorb per-row rounding so the batch reconciles EXACTLY to net (inv #1).
        _reconcile(rows, "amount", net["amount"])
        if net["amount_base"] is not None:
            _reconcile(rows, "amount_base", net["amount_base"])
        touch_count = len(rows)
    else:
        # No eligible touches (untracked/typed/bookmark arrival, or a guest whose
        # stream is not yet stitched): attribute the whole order to Direct. Every
        # revenue-bearing order MUST produce a batch so store-wide attributed
        # revenue reconciles to net revenue (invariant #1) — dropping these would
        # silently undercount. Direct is the honest label for unknown-source
        # revenue; a later guest-stitch may reclassify it on re-resolution.
        rows = [
            _build_row(order, None, CHANNEL_DIRECT, None, Decimal("1"), Decimal("1"), net, version)
        ]
        touch_count = 0

    # Forward-only supersede: prior batches are retained but no longer current,
    # so reporting reads exactly one batch per order.
    Attribution.objects.filter(order=order, is_current=True).update(is_current=False)
    Attribution.objects.bulk_create(rows)
    logger.info(
        "attribution: resolved order %s -> %s (%d touch(es)%s, %s %s)",
        order.pk,
        version,
        touch_count,
        "" if touch_count else " -> direct",
        net["currency"],
        net["amount"],
    )
    return version


def _build_row(order, touch, channel, campaign_ref, weight, base_weight, net, version):
    from attribution.models import Attribution

    amount = (net["amount"] * weight).quantize(CENTS)
    amount_base = (
        (net["amount_base"] * base_weight).quantize(CENTS)
        if net["amount_base"] is not None
        else None
    )
    return Attribution(
        order=order,
        touchpoint=touch,
        channel=channel,
        campaign_ref=campaign_ref,
        model_version=version,
        role=ROLE_PRIMARY,
        weight=weight,
        amount=amount,
        currency=net["currency"],
        amount_base=amount_base,
        base_currency=net["base_currency"],
        exchange_rate_used=net["exchange_rate"],
    )


def _reconcile(rows, field, target):
    """Nudge the last row's ``field`` so the column sums exactly to ``target``."""
    total = sum(getattr(r, field) for r in rows)
    drift = (target - total).quantize(CENTS)
    if drift and rows:
        setattr(rows[-1], field, (getattr(rows[-1], field) + drift).quantize(CENTS))
