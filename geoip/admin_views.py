"""
Admin AJAX views for GeoIP management.
"""
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.db.models import Q, F
from django.utils import timezone
from datetime import datetime
import json

from .models import GeoLocation, VisitorLocation
from .services import analytics_service


@staff_member_required
@require_GET
def filter_geolocations(request):
    """
    AJAX filter endpoint for GeoLocation entries.
    Returns rendered HTML for location cards.
    """
    # Verify AJAX request
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    queryset = GeoLocation.objects.all()

    # IP Address search filter
    ip_search = request.GET.get('ip', '').strip()
    if ip_search:
        queryset = queryset.filter(ip_address__icontains=ip_search)

    # Country code filter
    country = request.GET.get('country', '').strip()
    if country:
        queryset = queryset.filter(country_code__iexact=country)

    # Source filter
    source = request.GET.get('source', '').strip()
    if source:
        queryset = queryset.filter(source=source)

    # Security flags filters
    is_proxy = request.GET.get('is_proxy', '').strip()
    if is_proxy == 'true':
        queryset = queryset.filter(is_proxy=True)
    elif is_proxy == 'false':
        queryset = queryset.filter(is_proxy=False)

    is_vpn = request.GET.get('is_vpn', '').strip()
    if is_vpn == 'true':
        queryset = queryset.filter(is_vpn=True)
    elif is_vpn == 'false':
        queryset = queryset.filter(is_vpn=False)

    is_tor = request.GET.get('is_tor', '').strip()
    if is_tor == 'true':
        queryset = queryset.filter(is_tor=True)
    elif is_tor == 'false':
        queryset = queryset.filter(is_tor=False)

    is_mobile = request.GET.get('is_mobile', '').strip()
    if is_mobile == 'true':
        queryset = queryset.filter(is_mobile=True)
    elif is_mobile == 'false':
        queryset = queryset.filter(is_mobile=False)

    # Expired filter
    expired = request.GET.get('expired', '').strip()
    if expired == 'true':
        queryset = queryset.filter(expires_at__lt=timezone.now())
    elif expired == 'false':
        queryset = queryset.filter(
            Q(expires_at__isnull=True) | Q(expires_at__gte=timezone.now())
        )

    # Get total count before limiting
    total_count = queryset.count()

    # Order by most recent first, limit to 100 for performance
    locations = queryset.order_by('-resolved_at')[:100]

    html = render_to_string(
        'admin/geoip/partials/geolocation_cards.html',
        {'locations': locations},
        request=request
    )

    return JsonResponse({
        'html': html,
        'count': total_count,
    })


@staff_member_required
@require_GET
def filter_visitor_locations(request):
    """
    AJAX filter endpoint for VisitorLocation entries.
    Returns rendered HTML for visitor location cards.
    """
    # Verify AJAX request
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    queryset = VisitorLocation.objects.all()

    # Search (session_key or IP)
    search = request.GET.get('search', '').strip()
    if search:
        queryset = queryset.filter(
            Q(session_key__icontains=search) | Q(ip_address__icontains=search)
        )

    # Country filter
    country = request.GET.get('country', '').strip()
    if country:
        queryset = queryset.filter(
            Q(resolved_country__iexact=country) | Q(actual_country__iexact=country)
        )

    # Device type
    device_type = request.GET.get('device_type', '').strip()
    if device_type:
        queryset = queryset.filter(device_type=device_type)

    # Corrected filter
    corrected = request.GET.get('corrected', '').strip()
    if corrected == 'true':
        queryset = queryset.filter(
            actual_country__isnull=False
        ).exclude(
            actual_country=''
        ).exclude(
            actual_country=F('resolved_country')
        )
    elif corrected == 'false':
        queryset = queryset.filter(
            Q(actual_country__isnull=True) |
            Q(actual_country='') |
            Q(actual_country=F('resolved_country'))
        )

    # Get total count before limiting
    total_count = queryset.count()

    # Order by most recent first, limit to 100 for performance
    visitors = queryset.order_by('-last_seen')[:100]

    html = render_to_string(
        'admin/geoip/partials/visitorlocation_cards.html',
        {'visitors': visitors},
        request=request
    )

    return JsonResponse({
        'html': html,
        'count': total_count,
    })


@staff_member_required
@require_GET
def visitor_analytics_dashboard(request):
    """
    Main visitor analytics dashboard page.
    Renders the template with initial data for the default period (30 days).
    """
    period = request.GET.get('period', '30_days')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date and period == 'custom':
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            start_date = end_date = None
            period = '30_days'

    start, end = analytics_service.get_date_range_for_period(period, start_date, end_date)

    context = {
        'title': 'Visitor Analytics',
        'period': period,
        'start_date': start,
        'end_date': end,
        'overview': analytics_service.get_overview(start, end),
        'top_pages': analytics_service.get_top_pages(start, end),
        'campaigns': analytics_service.get_campaign_stats(start, end),
        'geographic': analytics_service.get_geographic_distribution(start, end),
        'devices': analytics_service.get_device_distribution(start, end),
        'devices_json': json.dumps(analytics_service.get_device_distribution(start, end)),
        'landing_pages': analytics_service.get_landing_pages(start, end, limit=10),
        'referrers': analytics_service.get_referrer_stats(start, end),
        'bot_summary': analytics_service.get_bot_summary(start, end),
        'new_vs_returning': analytics_service.get_new_vs_returning(start, end),
        'new_vs_returning_json': json.dumps(analytics_service.get_new_vs_returning(start, end)),
        'has_permission': True,
    }

    return TemplateResponse(
        request,
        'admin/geoip/visitor_analytics_dashboard.html',
        context,
    )


@staff_member_required
@require_GET
def visitor_analytics_data(request):
    """
    AJAX endpoint returning JSON data for Chart.js charts.
    Called when the period selector changes.
    """
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    period = request.GET.get('period', '30_days')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date and period == 'custom':
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            start_date = end_date = None
            period = '30_days'

    start, end = analytics_service.get_date_range_for_period(period, start_date, end_date)

    return JsonResponse({
        'overview': analytics_service.get_overview(start, end),
        'traffic_trends': analytics_service.get_traffic_trends(start, end),
        'top_pages': analytics_service.get_top_pages(start, end),
        'campaigns': analytics_service.get_campaign_stats(start, end),
        'geographic': analytics_service.get_geographic_distribution(start, end),
        'devices': analytics_service.get_device_distribution(start, end),
        'landing_pages': analytics_service.get_landing_pages(start, end, limit=10),
        'referrers': analytics_service.get_referrer_stats(start, end),
        'bot_summary': analytics_service.get_bot_summary(start, end),
        'new_vs_returning': analytics_service.get_new_vs_returning(start, end),
        'hourly': analytics_service.get_hourly_distribution(start, end),
    })
