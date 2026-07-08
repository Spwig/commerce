"""
Admin API Analytics Views

Dashboard analytics endpoints for the merchant mobile app
and advanced analytics for the admin web interface.
"""
from datetime import datetime, date

from django.http import StreamingHttpResponse, HttpResponse
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

from admin_api.permissions import IsStaffWithWritePermission
from admin_api.throttling import AdminAPIThrottle
from admin_api.services.analytics_service import AnalyticsService
from admin_api.services.analytics_export_service import AnalyticsExportService
from admin_api.serializers.analytics import (
    DashboardAnalyticsSerializer,
    QuickStatsSerializer,
    SalesKPISerializer,
    TopProductSerializer,
    SalesComparisonSerializer,
    DailyStatsSerializer,
    HourlySalesSerializer,
)
from admin_api.serializers.auth import AdminDataResponseSerializer, ErrorResponseSerializer
from core.api.api_descriptions import AUTH_REQUIRED, PERMISSION_DENIED, RATE_LIMIT_EXCEEDED


# ------------------------------------------------------------------ #
#  Helper: parse ISO 8601 date from query param
# ------------------------------------------------------------------ #
def _parse_date(date_str):
    """
    Parse a date string in YYYY-MM-DD format and return a date object.
    Returns None if parsing fails.
    """
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return None


# ================================================================== #
#  Existing endpoints
# ================================================================== #

@extend_schema(
    tags=['Admin'],
    summary=_("Get dashboard analytics"),
    description=_("""
    Get complete analytics data for the mobile app dashboard.

    **Rate Limit:** 300 requests per minute

    Optionally accepts start_date and end_date query params (YYYY-MM-DD)
    for a custom date range KPI section alongside the standard periods.

    Returns:
    - Sales KPIs for today, 7 days, and 30 days
    - Top selling products
    - Order status breakdown
    - Pending orders count
    - Low stock item count
    """),
    parameters=[
        OpenApiParameter(
            name='start_date',
            type=str,
            location=OpenApiParameter.QUERY,
            description=_("Custom range start date (YYYY-MM-DD)"),
            required=False,
        ),
        OpenApiParameter(
            name='end_date',
            type=str,
            location=OpenApiParameter.QUERY,
            description=_("Custom range end date (YYYY-MM-DD)"),
            required=False,
        ),
    ],
    responses={
        200: DashboardAnalyticsSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    }
)
@api_view(['GET'])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def dashboard_analytics(request):
    """
    Get complete dashboard analytics.

    Returns all analytics data needed for the mobile app dashboard.
    When start_date and end_date are provided, includes a custom_range KPI section.
    """
    try:
        start_date = _parse_date(request.query_params.get('start_date'))
        end_date = _parse_date(request.query_params.get('end_date'))

        data = AnalyticsService.get_dashboard_analytics(
            start_date=start_date, end_date=end_date
        )
        return Response({
            'success': True,
            'data': data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'error': {
                'code': 500,
                'message': _('Failed to retrieve analytics data.'),
                'details': str(e) if hasattr(request, 'user') and request.user.is_superuser else None
            }
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    tags=['Admin'],
    summary=_("Get quick stats"),
    description=_("""
    Get quick stats for dashboard header.

    **Rate Limit:** 300 requests per minute

    Returns:
    - Today's sales total
    - Today's order count
    - Pending orders count
    - Low stock items count
    """),
    responses={
        200: QuickStatsSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    }
)
@api_view(['GET'])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def quick_stats(request):
    """
    Get quick stats for dashboard header.

    Lightweight endpoint for header KPI display.
    """
    try:
        data = AnalyticsService.get_quick_stats()
        return Response({
            'success': True,
            'data': data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'error': {
                'code': 500,
                'message': _('Failed to retrieve quick stats.'),
            }
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    tags=['Admin'],
    summary=_("Get sales KPIs"),
    description=_("""
    Get sales KPIs for a specific period.

    **Rate Limit:** 300 requests per minute

    **Parameters:**
    - period: 'today', '7_days', or '30_days' (default: 'today')
    """),
    parameters=[
        OpenApiParameter(
            name='period',
            type=str,
            location=OpenApiParameter.QUERY,
            description=_("Time period: 'today', '7_days', or '30_days'"),
            required=False,
            default='today'
        )
    ],
    responses={
        200: SalesKPISerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    }
)
@api_view(['GET'])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def sales_kpi(request):
    """
    Get sales KPIs for a specified period.
    """
    period = request.query_params.get('period', 'today')
    if period not in ['today', '7_days', '30_days']:
        period = 'today'

    try:
        data = AnalyticsService.get_sales_kpi(period)
        return Response({
            'success': True,
            'data': data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'error': {
                'code': 500,
                'message': _('Failed to retrieve sales KPIs.'),
            }
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    tags=['Admin'],
    summary=_("Get top selling products"),
    description=_("""
    Get top selling products for a specific period.

    **Rate Limit:** 300 requests per minute

    **Parameters:**
    - period: 'today' or '7_days' (default: 'today')
    - limit: Maximum number of products (default: 5, max: 20)
    """),
    parameters=[
        OpenApiParameter(
            name='period',
            type=str,
            location=OpenApiParameter.QUERY,
            description=_("Time period: 'today' or '7_days'"),
            required=False,
            default='today'
        ),
        OpenApiParameter(
            name='limit',
            type=int,
            location=OpenApiParameter.QUERY,
            description=_("Maximum number of products to return (max 20)"),
            required=False,
            default=5
        )
    ],
    responses={
        200: TopProductSerializer(many=True),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    }
)
@api_view(['GET'])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def top_products(request):
    """
    Get top selling products for a specified period.
    """
    period = request.query_params.get('period', 'today')
    if period not in ['today', '7_days']:
        period = 'today'

    try:
        limit = int(request.query_params.get('limit', 5))
        limit = min(max(1, limit), 20)  # Clamp between 1 and 20
    except (ValueError, TypeError):
        limit = 5

    try:
        data = AnalyticsService.get_top_products(period, limit)
        return Response({
            'success': True,
            'data': data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'error': {
                'code': 500,
                'message': _('Failed to retrieve top products.'),
            }
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    tags=['Admin'],
    summary=_("Get sales comparison"),
    description=_("""
    Get sales comparison with previous period.

    **Rate Limit:** 300 requests per minute

    **Parameters:**
    - period: 'today' (vs yesterday) or '7_days' (vs previous 7 days)

    Returns current and previous period sales with trend indicator.
    """),
    parameters=[
        OpenApiParameter(
            name='period',
            type=str,
            location=OpenApiParameter.QUERY,
            description=_("Time period: 'today' or '7_days'"),
            required=False,
            default='today'
        )
    ],
    responses={
        200: SalesComparisonSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    }
)
@api_view(['GET'])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def sales_comparison(request):
    """
    Get sales comparison with previous period.
    """
    period = request.query_params.get('period', 'today')
    if period not in ['today', '7_days']:
        period = 'today'

    try:
        data = AnalyticsService.get_sales_comparison(period)
        return Response({
            'success': True,
            'data': data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'error': {
                'code': 500,
                'message': _('Failed to retrieve sales comparison.'),
            }
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    tags=['Admin'],
    summary=_("Get daily stats breakdown"),
    description=_("""
    Get per-day revenue and order counts for dashboard charts.

    **Rate Limit:** 300 requests per minute

    **Parameters:**
    - period: '7_days' (default), '30_days', or '90_days'

    Returns an array of daily data points including days with zero orders.
    """),
    parameters=[
        OpenApiParameter(
            name='period',
            type=str,
            location=OpenApiParameter.QUERY,
            description=_("Time period: '7_days', '30_days', or '90_days'"),
            required=False,
            default='7_days'
        )
    ],
    responses={
        200: DailyStatsSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    }
)
@api_view(['GET'])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def daily_stats(request):
    """
    Get per-day breakdown for dashboard charts.
    """
    period = request.query_params.get('period', '7_days')
    if period not in ['7_days', '30_days', '90_days']:
        period = '7_days'

    try:
        data = AnalyticsService.get_daily_stats(period)
        return Response({
            'success': True,
            'data': data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'error': {
                'code': 500,
                'message': _('Failed to retrieve daily stats.'),
            }
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    tags=['Admin'],
    summary=_("Get hourly sales breakdown"),
    description=_("""
    Get per-hour revenue and order counts for a single date.

    **Rate Limit:** 300 requests per minute

    Revenue is reported in the store's default currency. Multi-currency
    orders are converted via the pre-computed base-currency totals.

    **Parameters:**
    - date: Date in YYYY-MM-DD format (defaults to today)

    Returns 24 data points (hours 0-23) including hours with zero orders.
    """),
    parameters=[
        OpenApiParameter(
            name='date',
            type=str,
            location=OpenApiParameter.QUERY,
            description=_("Date to query (YYYY-MM-DD, defaults to today)"),
            required=False,
        )
    ],
    responses={
        200: HourlySalesSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    }
)
@api_view(['GET'])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def hourly_sales(request):
    """
    Get per-hour breakdown for a single date.
    """
    date_str = request.query_params.get('date')
    target_date = _parse_date(date_str) if date_str else date.today()

    if target_date is None:
        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('Invalid date format. Use YYYY-MM-DD.'),
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        data = AnalyticsService.get_hourly_sales(target_date)
        return Response({
            'success': True,
            'data': data
        }, status=status.HTTP_200_OK)
    except Exception:
        return Response({
            'success': False,
            'error': {
                'code': 500,
                'message': _('Failed to retrieve hourly sales.'),
            }
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ================================================================== #
#  NEW: Advanced Analytics Endpoints
# ================================================================== #

@extend_schema(
    tags=['Admin Analytics'],
    summary=_("Product analytics"),
    description=_("""
    Get product-level performance analytics for a date range.

    **Rate Limit:** 300 requests per minute

    Returns product-level metrics including units sold, revenue,
    orders count, return rate, and average selling price.
    Filterable by category, brand, and search term.
    """),
    parameters=[
        OpenApiParameter(
            name='start_date', type=str, location=OpenApiParameter.QUERY,
            description=_("Start date (YYYY-MM-DD)"), required=True,
        ),
        OpenApiParameter(
            name='end_date', type=str, location=OpenApiParameter.QUERY,
            description=_("End date (YYYY-MM-DD)"), required=True,
        ),
        OpenApiParameter(
            name='category_id', type=int, location=OpenApiParameter.QUERY,
            description=_("Filter by category ID"), required=False,
        ),
        OpenApiParameter(
            name='brand_id', type=int, location=OpenApiParameter.QUERY,
            description=_("Filter by brand ID"), required=False,
        ),
        OpenApiParameter(
            name='search', type=str, location=OpenApiParameter.QUERY,
            description=_("Search by product name or SKU"), required=False,
        ),
        OpenApiParameter(
            name='ordering', type=str, location=OpenApiParameter.QUERY,
            description=_("Sort field: revenue, -revenue, units_sold, -units_sold, orders_count, -orders_count"),
            required=False, default='-revenue',
        ),
        OpenApiParameter(
            name='page', type=int, location=OpenApiParameter.QUERY,
            description=_("Page number"), required=False, default=1,
        ),
        OpenApiParameter(
            name='page_size', type=int, location=OpenApiParameter.QUERY,
            description=_("Items per page (max 100)"), required=False, default=20,
        ),
    ],
    responses={
        200: AdminDataResponseSerializer,
        400: ErrorResponseSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    }
)
@api_view(['GET'])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def product_analytics(request):
    """
    Get product-level performance analytics for a date range.
    """
    start_date = _parse_date(request.query_params.get('start_date'))
    end_date = _parse_date(request.query_params.get('end_date'))

    if not start_date or not end_date:
        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('start_date and end_date are required (YYYY-MM-DD).'),
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    if start_date > end_date:
        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('start_date must be before or equal to end_date.'),
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    # Optional filters
    category_id = request.query_params.get('category_id')
    brand_id = request.query_params.get('brand_id')
    search = request.query_params.get('search', '').strip() or None
    ordering = request.query_params.get('ordering', '-revenue')

    try:
        category_id = int(category_id) if category_id else None
    except (ValueError, TypeError):
        category_id = None

    try:
        brand_id = int(brand_id) if brand_id else None
    except (ValueError, TypeError):
        brand_id = None

    try:
        page = max(1, int(request.query_params.get('page', 1)))
    except (ValueError, TypeError):
        page = 1

    try:
        page_size = min(100, max(1, int(request.query_params.get('page_size', 20))))
    except (ValueError, TypeError):
        page_size = 20

    try:
        data = AnalyticsService.get_product_analytics(
            start_date=start_date,
            end_date=end_date,
            category_id=category_id,
            brand_id=brand_id,
            search=search,
            ordering=ordering,
            page=page,
            page_size=page_size,
        )
        return Response({
            'success': True,
            'data': data,
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'error': {
                'code': 500,
                'message': _('Failed to retrieve product analytics.'),
                'details': str(e) if hasattr(request, 'user') and request.user.is_superuser else None,
            }
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    tags=['Admin Analytics'],
    summary=_("Customer analytics"),
    description=_("""
    Get customer analytics for a date range.

    **Rate Limit:** 300 requests per minute

    Returns customer summary (total, new, returning, average LTV),
    geographic breakdown, LTV distribution, and top customers list.
    """),
    parameters=[
        OpenApiParameter(
            name='start_date', type=str, location=OpenApiParameter.QUERY,
            description=_("Start date (YYYY-MM-DD)"), required=True,
        ),
        OpenApiParameter(
            name='end_date', type=str, location=OpenApiParameter.QUERY,
            description=_("End date (YYYY-MM-DD)"), required=True,
        ),
        OpenApiParameter(
            name='segment', type=str, location=OpenApiParameter.QUERY,
            description=_("Filter by segment: 'new', 'returning', or omit for all"),
            required=False,
        ),
        OpenApiParameter(
            name='ordering', type=str, location=OpenApiParameter.QUERY,
            description=_("Sort field for top customers: total_spent, -total_spent, range_spent, etc."),
            required=False, default='-total_spent',
        ),
        OpenApiParameter(
            name='page', type=int, location=OpenApiParameter.QUERY,
            description=_("Page number"), required=False, default=1,
        ),
        OpenApiParameter(
            name='page_size', type=int, location=OpenApiParameter.QUERY,
            description=_("Items per page (max 100)"), required=False, default=20,
        ),
    ],
    responses={
        200: AdminDataResponseSerializer,
        400: ErrorResponseSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    }
)
@api_view(['GET'])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def customer_analytics(request):
    """
    Get customer analytics for a date range.
    """
    start_date = _parse_date(request.query_params.get('start_date'))
    end_date = _parse_date(request.query_params.get('end_date'))

    if not start_date or not end_date:
        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('start_date and end_date are required (YYYY-MM-DD).'),
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    if start_date > end_date:
        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('start_date must be before or equal to end_date.'),
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    segment = request.query_params.get('segment')
    if segment and segment not in ('new', 'returning'):
        segment = None

    ordering = request.query_params.get('ordering', '-total_spent')

    try:
        page = max(1, int(request.query_params.get('page', 1)))
    except (ValueError, TypeError):
        page = 1

    try:
        page_size = min(100, max(1, int(request.query_params.get('page_size', 20))))
    except (ValueError, TypeError):
        page_size = 20

    try:
        data = AnalyticsService.get_customer_analytics(
            start_date=start_date,
            end_date=end_date,
            segment=segment,
            ordering=ordering,
            page=page,
            page_size=page_size,
        )
        return Response({
            'success': True,
            'data': data,
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'error': {
                'code': 500,
                'message': _('Failed to retrieve customer analytics.'),
                'details': str(e) if hasattr(request, 'user') and request.user.is_superuser else None,
            }
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    tags=['Admin Analytics'],
    summary=_("Category analytics"),
    description=_("""
    Get revenue and sales breakdown per category for a date range.

    **Rate Limit:** 300 requests per minute
    """),
    parameters=[
        OpenApiParameter(
            name='start_date', type=str, location=OpenApiParameter.QUERY,
            description=_("Start date (YYYY-MM-DD)"), required=True,
        ),
        OpenApiParameter(
            name='end_date', type=str, location=OpenApiParameter.QUERY,
            description=_("End date (YYYY-MM-DD)"), required=True,
        ),
        OpenApiParameter(
            name='ordering', type=str, location=OpenApiParameter.QUERY,
            description=_("Sort field: revenue, -revenue, units_sold, -units_sold, name, -name"),
            required=False, default='-revenue',
        ),
    ],
    responses={
        200: AdminDataResponseSerializer,
        400: ErrorResponseSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    }
)
@api_view(['GET'])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def category_analytics(request):
    """
    Get revenue per category for a date range.
    """
    start_date = _parse_date(request.query_params.get('start_date'))
    end_date = _parse_date(request.query_params.get('end_date'))

    if not start_date or not end_date:
        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('start_date and end_date are required (YYYY-MM-DD).'),
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    if start_date > end_date:
        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('start_date must be before or equal to end_date.'),
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    ordering = request.query_params.get('ordering', '-revenue')

    try:
        data = AnalyticsService.get_category_analytics(
            start_date=start_date,
            end_date=end_date,
            ordering=ordering,
        )
        return Response({
            'success': True,
            'data': data,
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'error': {
                'code': 500,
                'message': _('Failed to retrieve category analytics.'),
                'details': str(e) if hasattr(request, 'user') and request.user.is_superuser else None,
            }
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    tags=['Admin Analytics'],
    summary=_("Brand analytics"),
    description=_("""
    Get revenue and sales breakdown per brand for a date range.

    **Rate Limit:** 300 requests per minute
    """),
    parameters=[
        OpenApiParameter(
            name='start_date', type=str, location=OpenApiParameter.QUERY,
            description=_("Start date (YYYY-MM-DD)"), required=True,
        ),
        OpenApiParameter(
            name='end_date', type=str, location=OpenApiParameter.QUERY,
            description=_("End date (YYYY-MM-DD)"), required=True,
        ),
        OpenApiParameter(
            name='ordering', type=str, location=OpenApiParameter.QUERY,
            description=_("Sort field: revenue, -revenue, units_sold, -units_sold, name, -name"),
            required=False, default='-revenue',
        ),
    ],
    responses={
        200: AdminDataResponseSerializer,
        400: ErrorResponseSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    }
)
@api_view(['GET'])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def brand_analytics(request):
    """
    Get revenue per brand for a date range.
    """
    start_date = _parse_date(request.query_params.get('start_date'))
    end_date = _parse_date(request.query_params.get('end_date'))

    if not start_date or not end_date:
        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('start_date and end_date are required (YYYY-MM-DD).'),
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    if start_date > end_date:
        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('start_date must be before or equal to end_date.'),
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    ordering = request.query_params.get('ordering', '-revenue')

    try:
        data = AnalyticsService.get_brand_analytics(
            start_date=start_date,
            end_date=end_date,
            ordering=ordering,
        )
        return Response({
            'success': True,
            'data': data,
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'error': {
                'code': 500,
                'message': _('Failed to retrieve brand analytics.'),
                'details': str(e) if hasattr(request, 'user') and request.user.is_superuser else None,
            }
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    tags=['Admin Analytics'],
    summary=_("Enhanced sales comparison"),
    description=_("""
    Get sales comparison between two date ranges with daily breakdown for charts.

    **Rate Limit:** 300 requests per minute

    When explicit dates are provided, compares those ranges.
    Otherwise falls back to period-based comparison (today vs yesterday, etc.).
    Includes a daily_breakdown array for chart rendering.
    """),
    parameters=[
        OpenApiParameter(
            name='period', type=str, location=OpenApiParameter.QUERY,
            description=_("Fallback period if dates not provided: 'today' or '7_days'"),
            required=False, default='today',
        ),
        OpenApiParameter(
            name='start_date', type=str, location=OpenApiParameter.QUERY,
            description=_("Current period start date (YYYY-MM-DD)"), required=False,
        ),
        OpenApiParameter(
            name='end_date', type=str, location=OpenApiParameter.QUERY,
            description=_("Current period end date (YYYY-MM-DD)"), required=False,
        ),
        OpenApiParameter(
            name='compare_start_date', type=str, location=OpenApiParameter.QUERY,
            description=_("Comparison period start date (YYYY-MM-DD)"), required=False,
        ),
        OpenApiParameter(
            name='compare_end_date', type=str, location=OpenApiParameter.QUERY,
            description=_("Comparison period end date (YYYY-MM-DD)"), required=False,
        ),
    ],
    responses={
        200: AdminDataResponseSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    }
)
@api_view(['GET'])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def analytics_comparison(request):
    """
    Enhanced sales comparison with optional explicit date ranges and daily breakdown.
    """
    period = request.query_params.get('period', 'today')
    if period not in ['today', '7_days']:
        period = 'today'

    start_date = _parse_date(request.query_params.get('start_date'))
    end_date = _parse_date(request.query_params.get('end_date'))
    compare_start_date = _parse_date(request.query_params.get('compare_start_date'))
    compare_end_date = _parse_date(request.query_params.get('compare_end_date'))

    try:
        data = AnalyticsService.get_sales_comparison(
            period=period,
            start_date=start_date,
            end_date=end_date,
            compare_start_date=compare_start_date,
            compare_end_date=compare_end_date,
        )
        return Response({
            'success': True,
            'data': data,
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'error': {
                'code': 500,
                'message': _('Failed to retrieve sales comparison.'),
                'details': str(e) if hasattr(request, 'user') and request.user.is_superuser else None,
            }
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ================================================================== #
#  NEW: Analytics Export
# ================================================================== #

@extend_schema(
    tags=['Admin Analytics'],
    summary=_("Export analytics report"),
    description=_("""
    Export analytics data as CSV or PDF.

    **Rate Limit:** 300 requests per minute

    Returns the file directly with appropriate Content-Type and
    Content-Disposition headers (not wrapped in JSON envelope).

    **Report types:** products, customers, categories, brands, orders, summary
    **Formats:** csv, pdf
    """),
    parameters=[
        OpenApiParameter(
            name='report_type', type=str, location=OpenApiParameter.QUERY,
            description=_("Report type: products, customers, categories, brands, orders, summary"),
            required=True,
        ),
        OpenApiParameter(
            name='format', type=str, location=OpenApiParameter.QUERY,
            description=_("Export format: csv or pdf"),
            required=True,
        ),
        OpenApiParameter(
            name='start_date', type=str, location=OpenApiParameter.QUERY,
            description=_("Start date (YYYY-MM-DD)"), required=True,
        ),
        OpenApiParameter(
            name='end_date', type=str, location=OpenApiParameter.QUERY,
            description=_("End date (YYYY-MM-DD)"), required=True,
        ),
    ],
    responses={
        200: OpenApiResponse(description=_("File download (CSV or PDF)")),
        400: ErrorResponseSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    }
)
@api_view(['GET'])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def analytics_export(request):
    """
    Export analytics data as CSV or PDF file.

    Returns the raw file with Content-Type and Content-Disposition headers.
    """
    report_type = request.query_params.get('report_type', '')
    export_format = request.query_params.get('format', '')
    start_date = _parse_date(request.query_params.get('start_date'))
    end_date = _parse_date(request.query_params.get('end_date'))

    # Validate params
    valid_types = ('products', 'customers', 'categories', 'brands', 'orders', 'summary')
    valid_formats = ('csv', 'pdf')

    if report_type not in valid_types:
        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('Invalid report_type. Must be one of: %(types)s') % {
                    'types': ', '.join(valid_types)
                },
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    if export_format not in valid_formats:
        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('Invalid format. Must be csv or pdf.'),
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    if not start_date or not end_date:
        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('start_date and end_date are required (YYYY-MM-DD).'),
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    if start_date > end_date:
        return Response({
            'success': False,
            'error': {
                'code': 400,
                'message': _('start_date must be before or equal to end_date.'),
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    filename_base = f'spwig_{report_type}_{start_date}_{end_date}'

    try:
        if export_format == 'csv':
            csv_content = AnalyticsExportService.export_csv(
                report_type, start_date, end_date
            )
            response = HttpResponse(
                csv_content,
                content_type='text/csv; charset=utf-8',
            )
            response['Content-Disposition'] = f'attachment; filename="{filename_base}.csv"'
            return response

        else:  # pdf
            pdf_buffer = AnalyticsExportService.export_pdf(
                report_type, start_date, end_date
            )
            response = HttpResponse(
                pdf_buffer.getvalue(),
                content_type='application/pdf',
            )
            response['Content-Disposition'] = f'attachment; filename="{filename_base}.pdf"'
            pdf_buffer.close()
            return response

    except Exception as e:
        return Response({
            'success': False,
            'error': {
                'code': 500,
                'message': _('Failed to generate export.'),
                'details': str(e) if hasattr(request, 'user') and request.user.is_superuser else None,
            }
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
