"""
Sales Bell API - Internal endpoint for the Spwig Sales Bell (Pi dashboard).
Only active when SPWIG_IS_HQ=True.
Authenticated via a shared bearer token (SALES_BELL_TOKEN env var).
"""

import logging
from decimal import Decimal

from django.conf import settings
from django.db.models import Q, Sum
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from core.models import SalesBellEvent

logger = logging.getLogger(__name__)


def bell_token_required(view_func):
    """Simple bearer token auth for the sales bell endpoint."""

    def wrapper(request, *args, **kwargs):
        token = getattr(settings, "SALES_BELL_TOKEN", "")
        if not token:
            return JsonResponse({"error": "Sales bell not configured"}, status=503)

        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        if not auth_header.startswith("Bearer ") or auth_header[7:] != token:
            return JsonResponse({"error": "Unauthorized"}, status=401)

        return view_func(request, *args, **kwargs)

    return wrapper


@require_GET
@bell_token_required
def bell_events(request):
    """
    GET /api/internal/bell/events/?since=<id>

    Returns new events since the given ID, plus running totals.
    """
    since_id = request.GET.get("since")

    # Fetch new events
    qs = SalesBellEvent.objects.all()
    if since_id:
        try:
            qs = qs.filter(id__gt=int(since_id))
        except (ValueError, TypeError):
            pass

    events = list(
        qs.order_by("-id")[:50].values(
            "id", "event_type", "subtype", "name", "product", "amount", "currency", "created_at"
        )
    )

    # Serialize events for JSON
    for event in events:
        event["amount"] = float(event["amount"])
        event["created_at"] = event["created_at"].isoformat()
        # Map field names to match the Pi app's expected format
        event["type"] = event.pop("event_type")
        event["timestamp"] = event.pop("created_at")

    # Running totals (computed from all events, not just since)
    totals = SalesBellEvent.objects.aggregate(
        total_revenue=Sum("amount", filter=Q(event_type="sale")),
        total_refunded=Sum("amount", filter=Q(event_type="refund")),
        total_sales=Sum(1, filter=Q(event_type="sale")),
        total_refunds=Sum(1, filter=Q(event_type="refund")),
        developer_signups=Sum(1, filter=Q(event_type="developer_signup")),
    )

    sale_revenue = totals["total_revenue"] or Decimal("0")
    refund_total = totals["total_refunded"] or Decimal("0")

    return JsonResponse(
        {
            "events": events,
            "total_revenue": float(sale_revenue - refund_total),
            "total_sales": totals["total_sales"] or 0,
            "total_refunds": totals["total_refunds"] or 0,
            "developer_signups": totals["developer_signups"] or 0,
        }
    )
