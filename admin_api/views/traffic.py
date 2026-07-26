"""
Admin API Web Traffic Analytics View

Exposes the visitor/traffic analytics that previously lived only behind the
plain-Django ``@staff_member_required`` geoip dashboard, so a scoped Bearer API
token (or the mobile app / an admin session) can read them over the admin API.

Wraps ``geoip.services.analytics_service`` — the same service the admin
dashboard uses — and returns a single combined JSON payload.
"""

from datetime import datetime

from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response

from admin_api.permissions import IsStaffWithWritePermission
from admin_api.serializers.traffic import TrafficAnalyticsResponseSerializer
from admin_api.throttling import AdminAPIThrottle
from core.api.api_descriptions import AUTH_REQUIRED, PERMISSION_DENIED, RATE_LIMIT_EXCEEDED
from geoip.services import analytics_service

VALID_PERIODS = ("7_days", "30_days", "90_days", "custom")


def _parse_date(date_str):
    """Parse YYYY-MM-DD to a date, or None."""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


@extend_schema(
    tags=["Admin"],
    summary=_("Get web traffic analytics"),
    description=_("""
    Get combined visitor/traffic analytics for the store.

    Scope required: **analytics.traffic** (read). Reachable by an admin
    session, the merchant mobile app, or a merchant API token holding the
    ``analytics.traffic`` scope.

    **Rate Limit:** 300 requests per minute

    Accepts a `period` (`7_days`, `30_days`, `90_days`, or `custom`). For
    `custom`, provide `start_date` and `end_date` (YYYY-MM-DD).

    Returns, for the resolved date range:
    - `overview` — totals, unique visitors, bots, bounce rate, pages/session
    - `traffic_trends` — daily labels/views/visitors/bot_views series
    - `top_pages` — most-viewed pages
    - `geographic_distribution` — visitors by country
    - `referrer_stats` — top referrer domains
    """),
    parameters=[
        OpenApiParameter(
            name="period",
            type=str,
            location=OpenApiParameter.QUERY,
            description=_("7_days | 30_days | 90_days | custom (default 30_days)"),
            required=False,
        ),
        OpenApiParameter(
            name="start_date",
            type=str,
            location=OpenApiParameter.QUERY,
            description=_("Custom range start date (YYYY-MM-DD); required when period=custom"),
            required=False,
        ),
        OpenApiParameter(
            name="end_date",
            type=str,
            location=OpenApiParameter.QUERY,
            description=_("Custom range end date (YYYY-MM-DD); required when period=custom"),
            required=False,
        ),
    ],
    responses={
        200: TrafficAnalyticsResponseSerializer,
        400: OpenApiResponse(description=_("Invalid period or date range.")),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    },
)
@api_view(["GET"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def traffic_analytics(request):
    """Combined web/visitor analytics wrapping geoip.analytics_service."""
    period = request.query_params.get("period", "30_days")
    if period not in VALID_PERIODS:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Invalid period. Use 7_days, 30_days, 90_days or custom."),
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    start_date = _parse_date(request.query_params.get("start_date"))
    end_date = _parse_date(request.query_params.get("end_date"))

    if period == "custom":
        if not start_date or not end_date:
            return Response(
                {
                    "success": False,
                    "error": {
                        "code": 400,
                        "message": _(
                            "Custom period requires start_date and end_date (YYYY-MM-DD)."
                        ),
                    },
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if start_date > end_date:
            return Response(
                {
                    "success": False,
                    "error": {
                        "code": 400,
                        "message": _("start_date must not be after end_date."),
                    },
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    try:
        start, end = analytics_service.get_date_range_for_period(
            period, start_date=start_date, end_date=end_date
        )
        data = {
            "period": period,
            "start": start,
            "end": end,
            "overview": analytics_service.get_overview(start, end),
            "traffic_trends": analytics_service.get_traffic_trends(start, end),
            "top_pages": analytics_service.get_top_pages(start, end),
            "geographic_distribution": analytics_service.get_geographic_distribution(start, end),
            "referrer_stats": analytics_service.get_referrer_stats(start, end),
        }
        return Response({"success": True, "data": data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 500,
                    "message": _("Failed to retrieve traffic analytics."),
                    "details": str(e)
                    if hasattr(request, "user") and request.user.is_superuser
                    else None,
                },
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
