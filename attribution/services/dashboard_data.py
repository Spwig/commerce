"""The shared attribution dashboard data contract.

One payload builder for the admin dashboard page AND the mobile admin API, so
the two surfaces can never drift. Everything here is presentation-agnostic and
JSON-safe (Decimals -> float).
"""

from datetime import datetime, time, timedelta
from decimal import Decimal

from django.utils import timezone

from attribution.services import preview, reporting

# period key -> days back
PERIODS = {
    "last_7_days": 7,
    "last_14_days": 14,
    "last_30_days": 30,
    "last_90_days": 90,
}
DEFAULT_PERIOD = "last_14_days"
VALID_PERIODS = tuple(PERIODS) + ("month_to_date", "custom")


def resolve_period(period=None, start_date=None, end_date=None):
    """Resolve (start, end, period_key) from a period key and optional custom
    ``date`` bounds. Falls back to the default on anything unrecognised."""
    now = timezone.now()
    if period == "custom" and start_date and end_date:
        start = timezone.make_aware(datetime.combine(start_date, time.min))
        end = timezone.make_aware(datetime.combine(end_date, time.max))
        return start, end, "custom"
    if period == "month_to_date":
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return start, now, "month_to_date"
    period = period if period in PERIODS else DEFAULT_PERIOD
    start = (now - timedelta(days=PERIODS[period])).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    return start, now, period


def _native(value):
    """Make reporting output JSON-safe (Decimal -> float)."""
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, list):
        return [_native(v) for v in value]
    if isinstance(value, dict):
        return {k: _native(v) for k, v in value.items()}
    return value


def _base_currency():
    try:
        from core.models import SiteSettings

        return SiteSettings.get_settings().default_currency
    except Exception:
        return ""


def build_payload(start, end, period_key):
    """The single data contract, shared by the page and the API."""
    prev = preview.preview_by_model(start, end)
    summary = reporting.summary(start, end)
    payload = {
        "period": {
            "start": start.date().isoformat(),
            "end": end.date().isoformat(),
            "preset": period_key,
        },
        "currency": _base_currency(),
        "active_model": prev["active_model"],
        "models": prev["models"],
        "totals": prev["totals"],
        "reconciles": (
            True
            if prev.get("truncated")
            else prev["totals"]["attributed"] == float(summary["attributed_revenue"])
        ),
        "by_model": prev["by_model"],
        "influenced": reporting.influenced_revenue_by_channel(start, end),
        "journeys": preview.journeys(start, end),
        "campaigns": reporting.revenue_by_campaign(start, end),
        "meta": {"truncated": prev.get("truncated", False)},
    }
    return _native(payload)
