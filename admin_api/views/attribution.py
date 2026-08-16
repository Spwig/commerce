"""Admin API — Revenue Attribution analytics.

Exposes the same attribution dashboard payload the admin page uses
(``attribution.services.dashboard_data``) over the admin API, so the merchant
mobile app can render the identical live model-flip view. Read-only.
"""

from datetime import datetime

from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response

from admin_api.permissions import category_permission
from admin_api.serializers.attribution import AttributionAnalyticsResponseSerializer
from admin_api.throttling import AdminAPIThrottle
from attribution.services.dashboard_data import VALID_PERIODS, build_payload, resolve_period
from attribution.services.preview import MODEL_IDS
from core.api.api_descriptions import AUTH_REQUIRED, PERMISSION_DENIED, RATE_LIMIT_EXCEEDED


def _parse_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def _bad_request(message):
    return Response(
        {"success": False, "error": {"code": 400, "message": message}},
        status=status.HTTP_400_BAD_REQUEST,
    )


@extend_schema(
    tags=["Admin"],
    summary=_("Get revenue attribution"),
    description=_("""
    Multi-touch revenue attribution for the store — the same data as the admin
    Insights dashboard, so the mobile app can render the live model-flip.

    Scope required: **analytics.attribution** (read). Reachable by an admin
    session, the merchant mobile app, or a token holding that scope.

    **Rate Limit:** 300 requests per minute

    Accepts a `period` (`last_7_days`, `last_14_days`, `last_30_days`,
    `last_90_days`, `month_to_date`, or `custom`). For `custom`, provide
    `start_date` and `end_date` (YYYY-MM-DD). Pass `model` to return only one
    model's block (lighter payload); by default every model is returned so the
    app can flip models instantly with no round-trip.

    Returns, for the resolved range: totals + reconciliation flag, per-model
    channel breakdown and time-series (`by_model`), the assisted `influenced`
    lens, top journey `journeys`, and `campaigns`.
    """),
    parameters=[
        OpenApiParameter(
            name="period",
            type=str,
            location=OpenApiParameter.QUERY,
            required=False,
            description=_(
                "last_7_days | last_14_days | last_30_days | last_90_days | month_to_date | custom"
            ),
        ),
        OpenApiParameter(
            name="start_date",
            type=str,
            location=OpenApiParameter.QUERY,
            required=False,
            description=_("Custom range start (YYYY-MM-DD); required when period=custom"),
        ),
        OpenApiParameter(
            name="end_date",
            type=str,
            location=OpenApiParameter.QUERY,
            required=False,
            description=_("Custom range end (YYYY-MM-DD); required when period=custom"),
        ),
        OpenApiParameter(
            name="model",
            type=str,
            location=OpenApiParameter.QUERY,
            required=False,
            description=_("Return only this model's block (default: all models)"),
        ),
    ],
    responses={
        200: AttributionAnalyticsResponseSerializer,
        400: OpenApiResponse(description=_("Invalid period or date range.")),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    },
)
@api_view(["GET"])
@permission_classes([category_permission("analytics", "view")])
@throttle_classes([AdminAPIThrottle])
def attribution_analytics(request):
    """Revenue attribution payload wrapping attribution.services.dashboard_data."""
    period = request.query_params.get("period", "last_14_days")
    if period not in VALID_PERIODS:
        return _bad_request(_("Invalid period."))

    start_date = _parse_date(request.query_params.get("start_date"))
    end_date = _parse_date(request.query_params.get("end_date"))
    if period == "custom":
        if not start_date or not end_date:
            return _bad_request(_("Custom period requires start_date and end_date (YYYY-MM-DD)."))
        if start_date > end_date:
            return _bad_request(_("start_date must not be after end_date."))

    model = request.query_params.get("model")
    if model and model not in MODEL_IDS:
        return _bad_request(_("Invalid model."))

    try:
        start, end, resolved = resolve_period(period, start_date, end_date)
        data = build_payload(start, end, resolved)
        if model and model in data["by_model"]:
            data["by_model"] = {model: data["by_model"][model]}
        return Response({"success": True, "data": data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 500,
                    "message": _("Failed to retrieve revenue attribution."),
                    "details": str(e)
                    if hasattr(request, "user") and request.user.is_superuser
                    else None,
                },
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
