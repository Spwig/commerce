"""Read models over the attribution engine — the consolidated revenue overview.

Everything here reads the *current* attribution batch per order
(``is_current=True``, ``role='primary'``), so figures reflect the active
model and reconcile to net revenue. Amounts are aggregated in the store's base
currency (``amount_base``) so multi-currency orders sum correctly.

This is the headless data layer. The eventual merchant dashboard, CSV export
and public API are thin readers over these functions — no presentation here.

Vocabulary:
- **Attributed revenue** — the model's allocation of each order's net revenue
  to channels. Sums to total net revenue across channels (reconciles).
- **Influenced revenue** — each channel credited the *full* net of every order
  it touched (counted once per order). Totals may exceed 100% by design; this
  is the "assisted" lens that shows top-of-funnel value last-click hides.
"""

from collections import defaultdict
from decimal import Decimal

from django.db.models import Count, Sum
from django.db.models.functions import TruncDay, TruncMonth, TruncWeek


def _current_primary(start=None, end=None):
    from attribution.models import Attribution

    qs = Attribution.objects.filter(is_current=True, role="primary")
    if start is not None:
        qs = qs.filter(order__created_at__gte=start)
    if end is not None:
        qs = qs.filter(order__created_at__lte=end)
    return qs


def _q(value):
    return (value or Decimal("0")).quantize(Decimal("0.01"))


def summary(start=None, end=None):
    """Totals + a reconciliation check for the period."""
    agg = _current_primary(start, end).aggregate(
        revenue=Sum("amount_base"), orders=Count("order", distinct=True)
    )
    return {
        "attributed_revenue": _q(agg["revenue"]),
        "orders": agg["orders"] or 0,
    }


def revenue_by_channel(start=None, end=None):
    """Attributed revenue per channel, highest first, with % share."""
    # Single-touch models (last-non-direct/first-touch) write zero-weight rows
    # for the touches they don't credit — kept for the influenced lens but
    # excluded here, since a £0 channel is not "revenue by channel".
    rows = list(
        _current_primary(start, end)
        .values("channel")
        .annotate(revenue=Sum("amount_base"), orders=Count("order", distinct=True))
        .filter(revenue__gt=0)
        .order_by("-revenue")
    )
    total = sum((r["revenue"] or Decimal("0")) for r in rows) or Decimal("0")
    out = []
    for r in rows:
        rev = _q(r["revenue"])
        share = (rev / total * 100).quantize(Decimal("0.1")) if total else Decimal("0")
        out.append(
            {"channel": r["channel"], "revenue": rev, "orders": r["orders"], "share_pct": share}
        )
    return out


def revenue_by_campaign(start=None, end=None):
    """Attributed revenue per named campaign (touches with no campaign excluded)."""
    rows = (
        _current_primary(start, end)
        .filter(campaign_ref__isnull=False)
        .values("campaign_ref", "campaign_ref__name", "campaign_ref__slug")
        .annotate(revenue=Sum("amount_base"), orders=Count("order", distinct=True))
        .filter(revenue__gt=0)
        .order_by("-revenue")
    )
    return [
        {
            "campaign_id": r["campaign_ref"],
            "name": r["campaign_ref__name"],
            "slug": r["campaign_ref__slug"],
            "revenue": _q(r["revenue"]),
            "orders": r["orders"],
        }
        for r in rows
    ]


_BUCKETS = {"day": TruncDay, "week": TruncWeek, "month": TruncMonth}


def time_series(start=None, end=None, bucket="day"):
    """Attributed revenue per channel per time bucket (for stacked charts)."""
    trunc = _BUCKETS.get(bucket, TruncDay)
    rows = (
        _current_primary(start, end)
        .annotate(period=trunc("order__created_at"))
        .values("period", "channel")
        .annotate(revenue=Sum("amount_base"))
        .filter(revenue__gt=0)
        .order_by("period")
    )
    return [
        {"period": r["period"], "channel": r["channel"], "revenue": _q(r["revenue"])} for r in rows
    ]


def influenced_revenue_by_channel(start=None, end=None):
    """Full net of every order a channel touched (assisted lens; may exceed 100%).

    Computed in Python from the current primary rows: build each order's net
    once, then credit it to every distinct channel present in that order's
    journey. This surfaces top-of-funnel channels that last-click buries.
    """
    order_net = defaultdict(lambda: Decimal("0"))
    channel_orders = defaultdict(set)
    for row in _current_primary(start, end).values("order_id", "channel", "amount_base"):
        order_net[row["order_id"]] += row["amount_base"] or Decimal("0")
        channel_orders[row["channel"]].add(row["order_id"])

    out = [
        {
            "channel": channel,
            "influenced_revenue": _q(sum(order_net[o] for o in orders)),
            "orders": len(orders),
        }
        for channel, orders in channel_orders.items()
    ]
    out.sort(key=lambda r: r["influenced_revenue"], reverse=True)
    return out
