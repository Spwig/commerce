"""Admin dashboard for revenue attribution.

Thin presentation over the shared ``dashboard_data`` contract (also used by the
mobile API). The page server-renders the full payload for instant first paint;
the AJAX ``data`` endpoint returns the same shape for date-range changes.
"""

import csv
from datetime import datetime
from functools import wraps

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.template.response import TemplateResponse
from django.views.decorators.http import require_GET

from attribution.constants import CHANNEL_CHOICES
from attribution.services import preview
from attribution.services.dashboard_data import PERIODS, build_payload, resolve_period
from staff_roles.services import has_category_access

_CHANNEL_LABELS = {cid: str(label) for cid, label in CHANNEL_CHOICES}


def _analytics_required(view):
    """Staff AND the ``analytics`` permission category (superusers bypass).

    The sidebar only *shows* Insights to analytics-permitted staff; this ensures
    the endpoints themselves are not reachable by other staff.
    """

    @staff_member_required
    @wraps(view)
    def wrapped(request, *args, **kwargs):
        if not (request.user.is_superuser or has_category_access(request.user, "analytics")):
            return HttpResponseForbidden("You don't have access to Insights.")
        return view(request, *args, **kwargs)

    return wrapped


def _parse_date(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


def _range_from_request(request):
    return resolve_period(
        request.GET.get("period"),
        _parse_date(request.GET.get("start")),
        _parse_date(request.GET.get("end")),
    )


@_analytics_required
@require_GET
def attribution_dashboard(request):
    """The Revenue Attribution dashboard page."""
    start, end, period = _range_from_request(request)
    payload = build_payload(start, end, period)
    context = {
        "title": "Revenue Attribution",
        "period": period,
        "periods": PERIODS,
        "payload": payload,
        "has_data": payload["totals"]["orders"] > 0,
        "has_permission": True,
    }
    return TemplateResponse(request, "admin/attribution/dashboard.html", context)


@_analytics_required
@require_GET
def attribution_data(request):
    """AJAX endpoint — same payload, for date-range changes."""
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)
    start, end, period = _range_from_request(request)
    return JsonResponse(build_payload(start, end, period))


@_analytics_required
@require_GET
def attribution_export(request):
    """CSV of the channel breakdown for the chosen model + period."""
    start, end, _period = _range_from_request(request)
    prev = preview.preview_by_model(start, end)
    model = request.GET.get("model")
    if model not in prev["by_model"]:
        model = prev["active_model"]

    response = HttpResponse(content_type="text/csv")
    fname = f"attribution_{model}_{start.date()}_{end.date()}.csv"
    response["Content-Disposition"] = f'attachment; filename="{fname}"'
    writer = csv.writer(response)
    writer.writerow(["Channel", "Revenue", "Orders", "Share %"])
    for row in prev["by_model"][model]["channels"]:
        writer.writerow(
            [
                _CHANNEL_LABELS.get(row["channel"], row["channel"]),
                row["revenue"],
                row["orders"],
                row["share"],
            ]
        )
    return response
