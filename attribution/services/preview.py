"""What-if attribution — compute every model over the touch stream, read-only.

The dashboard's hero interaction re-attributes revenue the instant a merchant
switches model. We must NOT re-resolve and overwrite their chosen
``AttributionSettings.active_model`` to preview another. So this module computes
channel + time-series totals for *all* models in memory, from the same touches
and net revenue the resolver uses (``compute_weights`` + ``attributable_net``) —
writing nothing.

Because it reuses those exact functions over the same order universe that
``reporting.py`` reads, ``preview_by_model()[active_model]`` reconciles to
``reporting.summary()`` for the period (asserted in tests). The stored
``Attribution`` rows remain the canonical record for exports / Order.source;
this is a projection on top.

``journeys()`` (top first→last channel flows for the Sankey) shares the same
loader and is model-independent.
"""

import logging
from collections import defaultdict
from datetime import timedelta
from decimal import Decimal

from django.conf import settings as dj_settings
from django.core.cache import cache
from django.db.models import Count, Max

from attribution.constants import ATTRIBUTION_MODEL_CHOICES, CHANNEL_DIRECT, ROLE_PRIMARY
from attribution.services.attribution_models import compute_weights
from attribution.services.reporting import _q
from attribution.services.revenue import CENTS, attributable_net

logger = logging.getLogger(__name__)

MODEL_IDS = [c[0] for c in ATTRIBUTION_MODEL_CHOICES]


def _max_orders():
    """Above this many orders in range we skip the (heavy) all-model recompute
    and serve only the stored/canonical model. Read live so it's configurable
    per deployment; never silently sampled."""
    return getattr(dj_settings, "ATTRIBUTION_PREVIEW_MAX_ORDERS", 50000)


def _cache_ttl():
    return getattr(dj_settings, "ATTRIBUTION_PREVIEW_CACHE_TTL", 300)


def _base_currency():
    try:
        from core.models import SiteSettings

        return SiteSettings.get_settings().default_currency
    except Exception:  # pragma: no cover - defensive
        return ""


def _order_ids(start, end):
    """Ids of orders that have a current attribution in range (the same universe
    ``reporting.py`` reports over)."""
    from attribution.models import Attribution

    q = Attribution.objects.filter(is_current=True, role=ROLE_PRIMARY)
    if start is not None:
        q = q.filter(order__created_at__gte=start)
    if end is not None:
        q = q.filter(order__created_at__lte=end)
    return list(q.order_by().values_list("order_id", flat=True).distinct())


def _load(order_ids, lookback_days):
    """Load the orders and, in one query, every eligible touch for their
    customers within the widest lookback window. Returns
    ``(orders, touches_by_customer)``."""
    from attribution.models import TouchPoint
    from orders.models import Order

    orders = list(Order.objects.filter(id__in=order_ids))
    touches_by_customer = defaultdict(list)
    customer_ids = {o.user_id for o in orders if o.user_id}
    if orders and customer_ids:
        min_created = min(o.created_at for o in orders)
        max_created = max(o.created_at for o in orders)
        since = min_created - timedelta(days=lookback_days)
        touches = (
            TouchPoint.objects.filter(
                customer_id__in=customer_ids,
                is_bot=False,
                occurred_at__gte=since,
                occurred_at__lte=max_created,
            )
            .order_by("occurred_at")
            .only("customer_id", "channel", "occurred_at")
        )
        for t in touches:
            touches_by_customer[t.customer_id].append(t)
    return orders, touches_by_customer


def _window(order, touches_by_customer, lookback_days):
    """The touches eligible to credit this order (customer + lookback window),
    oldest→newest — mirrors ``resolution.touches_for_order``."""
    if not order.user_id:
        return []
    since = order.created_at - timedelta(days=lookback_days)
    return [
        t
        for t in touches_by_customer.get(order.user_id, ())
        if since <= t.occurred_at <= order.created_at
    ]


def _cache_key(start, end, conf):
    from attribution.models import Attribution

    sig = Attribution.objects.filter(is_current=True, role=ROLE_PRIMARY).aggregate(
        n=Count("id"), mx=Max("id")
    )
    # Settings affect the output (active_model label, and lookback/half-life feed
    # the per-model math), so a settings change must bust the cache even when no
    # rows changed.
    return (
        f"attr:preview:{start}:{end}:{sig['n']}:{sig['mx']}"
        f":{conf.active_model}:{conf.lookback_days}:{conf.time_decay_half_life_days}"
    )


def _canonical_only(start, end, active_model, order_count):
    """Truncation fallback: serve only the stored model from reporting.py."""
    from attribution.services import reporting

    channels = reporting.revenue_by_channel(start, end)
    ts = [
        {"date": r["period"].date().isoformat(), "channel": r["channel"], "revenue": r["revenue"]}
        for r in reporting.time_series(start, end)
    ]
    s = reporting.summary(start, end)
    return {
        "active_model": active_model,
        "models": MODEL_IDS,
        "totals": {
            "attributed": s["attributed_revenue"],
            "orders": s["orders"],
            "avg_touches": None,
        },
        "by_model": {
            active_model: {
                "channels": [
                    {
                        "channel": c["channel"],
                        "revenue": c["revenue"],
                        "orders": c["orders"],
                        "share": c["share_pct"],
                    }
                    for c in channels
                ],
                "timeseries": ts,
            }
        },
        "truncated": True,
        "truncated_count": order_count,
    }


def _share(value, total):
    return (value / total * 100).quantize(Decimal("0.1")) if total else Decimal("0")


def _allocate(net_amount, pairs):
    """Split ``net_amount`` across ``pairs`` [(channel, weight)] the way the
    resolver does: quantize each share to cents, then push the rounding drift
    onto the last share so the order reconciles EXACTLY to net. Keeps
    ``preview_by_model()[active_model]`` byte-equal to the stored rows."""
    allocs = [(ch, (net_amount * w).quantize(CENTS)) for ch, w in pairs]
    if allocs:
        drift = net_amount - sum(a for _, a in allocs)
        if drift:
            ch, a = allocs[-1]
            allocs[-1] = (ch, a + drift)
    return allocs


def preview_by_model(start=None, end=None, *, use_cache=True):
    """All-model channel + time-series + totals for the period. Read-only."""
    from attribution.models import AttributionSettings

    conf = AttributionSettings.get_settings()

    key = _cache_key(start, end, conf) if use_cache else None
    if key:
        hit = cache.get(key)
        if hit is not None:
            return hit

    order_ids = _order_ids(start, end)
    if len(order_ids) > _max_orders():
        logger.info(
            "attribution: preview truncated for %s..%s (%d orders > cap %d)",
            start,
            end,
            len(order_ids),
            _max_orders(),
        )
        result = _canonical_only(start, end, conf.active_model, len(order_ids))
        if key:
            cache.set(key, result, _cache_ttl())
        return result

    orders, tbc = _load(order_ids, conf.lookback_days)
    base_currency = _base_currency()
    hl = conf.time_decay_half_life_days

    channels = {m: defaultdict(lambda: Decimal("0")) for m in MODEL_IDS}
    ch_orders = {m: defaultdict(set) for m in MODEL_IDS}
    ts = {m: defaultdict(lambda: defaultdict(lambda: Decimal("0"))) for m in MODEL_IDS}
    total = Decimal("0")
    touch_sum = 0

    for o in orders:
        net = attributable_net(o, base_currency=base_currency)
        amt = net["amount_base"] if net["amount_base"] is not None else net["amount"]
        total += amt
        day = o.created_at.date().isoformat()
        window = _window(o, tbc, conf.lookback_days)
        touch_sum += len(window) if window else 1
        for m in MODEL_IDS:
            if window:
                pairs = [(t.channel, w) for t, w in compute_weights(window, m, o.created_at, hl)]
                allocs = _allocate(amt, pairs)
            else:
                allocs = [(CHANNEL_DIRECT, amt)]
            for ch, a in allocs:
                # Add every allocation incl. zero-weight touches (single-touch
                # models write £0 rows for the touches they don't credit) so
                # per-channel order counts match the stored reporting layer.
                channels[m][ch] += a
                ch_orders[m][ch].add(o.id)
                ts[m][day][ch] += a

    by_model = {}
    for m in MODEL_IDS:
        chlist = [
            {
                "channel": ch,
                "revenue": _q(v),
                "orders": len(ch_orders[m][ch]),
                "share": _share(v, total),
            }
            for ch, v in channels[m].items()
            if v > 0
        ]
        chlist.sort(key=lambda r: r["revenue"], reverse=True)
        tslist = []
        for day in sorted(ts[m]):
            for ch, v in ts[m][day].items():
                if v > 0:
                    tslist.append({"date": day, "channel": ch, "revenue": _q(v)})
        by_model[m] = {"channels": chlist, "timeseries": tslist}

    order_count = len(orders)
    result = {
        "active_model": conf.active_model,
        "models": MODEL_IDS,
        "totals": {
            "attributed": _q(total),
            "orders": order_count,
            "avg_touches": round(touch_sum / order_count, 1) if order_count else 0,
        },
        "by_model": by_model,
        "truncated": False,
    }
    if key:
        cache.set(key, result, _cache_ttl())
    return result


def journeys(start=None, end=None, limit=8):
    """Top first-touch → last-touch channel flows for the Sankey.

    Model-independent (reads the touch sequence). Untouched orders flow
    direct→direct. Returns the ``limit`` highest-revenue flows.
    """
    from attribution.models import AttributionSettings

    conf = AttributionSettings.get_settings()
    order_ids = _order_ids(start, end)
    if len(order_ids) > _max_orders():
        return []  # too large to trace per-order; the dashboard notes this

    orders, tbc = _load(order_ids, conf.lookback_days)
    base_currency = _base_currency()
    flows = defaultdict(lambda: {"revenue": Decimal("0"), "orders": 0})
    for o in orders:
        net = attributable_net(o, base_currency=base_currency)
        amt = net["amount_base"] if net["amount_base"] is not None else net["amount"]
        window = _window(o, tbc, conf.lookback_days)
        a = window[0].channel if window else CHANNEL_DIRECT
        b = window[-1].channel if window else CHANNEL_DIRECT
        flows[(a, b)]["revenue"] += amt
        flows[(a, b)]["orders"] += 1

    out = [
        {"from": a, "to": b, "revenue": _q(v["revenue"]), "orders": v["orders"]}
        for (a, b), v in flows.items()
    ]
    out.sort(key=lambda r: r["revenue"], reverse=True)
    return out[:limit]
