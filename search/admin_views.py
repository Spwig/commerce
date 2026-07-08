"""
Admin AJAX views for search management.
"""
from datetime import datetime, timedelta

from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.db.models import Count, Avg, Q
from django.utils import timezone

from .models import SearchQuery, Synonym, SearchRedirect, SearchEngine
from .services import AnalyticsService


@staff_member_required
@require_GET
def filter_search_queries(request):
    """
    AJAX filter endpoint for search queries analytics.

    Returns rendered HTML for the query cards.
    """
    # Verify AJAX request
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    queryset = SearchQuery.objects.all()

    # Date range filter
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if date_from:
        try:
            from_dt = datetime.strptime(date_from, '%Y-%m-%d')
            queryset = queryset.filter(created_at__date__gte=from_dt.date())
        except ValueError:
            pass

    if date_to:
        try:
            to_dt = datetime.strptime(date_to, '%Y-%m-%d')
            queryset = queryset.filter(created_at__date__lte=to_dt.date())
        except ValueError:
            pass

    # Search engine filter
    engine = request.GET.get('engine')
    if engine:
        queryset = queryset.filter(engine__slug=engine)

    # Zero results filter
    zero_results = request.GET.get('zero_results')
    if zero_results == 'true':
        queryset = queryset.filter(is_zero_result=True)

    # Language filter
    language = request.GET.get('language')
    if language:
        queryset = queryset.filter(language=language)

    # Search text filter
    search = request.GET.get('search', '').strip()
    if search:
        queryset = queryset.filter(query_normalized__icontains=search.lower())

    # Aggregate by normalized query
    aggregated = queryset.values(
        'query_normalized'
    ).annotate(
        search_count=Count('id'),
        avg_results=Avg('result_count'),
        zero_count=Count('id', filter=Q(is_zero_result=True)),
        avg_response=Avg('response_time_ms'),
    ).order_by('-search_count')[:50]

    # Calculate CTR for each query
    queries_data = []
    for item in aggregated:
        query_ids = queryset.filter(
            query_normalized=item['query_normalized']
        ).values_list('id', flat=True)

        total = item['search_count']
        with_clicks = SearchQuery.objects.filter(
            id__in=query_ids,
            clicks__isnull=False
        ).distinct().count()

        ctr = (with_clicks / total * 100) if total > 0 else 0

        queries_data.append({
            'query': item['query_normalized'],
            'search_count': item['search_count'],
            'avg_results': round(item['avg_results'] or 0, 1),
            'zero_count': item['zero_count'],
            'zero_rate': round(item['zero_count'] / item['search_count'] * 100, 1) if item['search_count'] > 0 else 0,
            'avg_response': round(item['avg_response'] or 0, 0),
            'ctr': round(ctr, 1),
        })

    html = render_to_string(
        'admin/search/partials/query_cards.html',
        {'queries': queries_data},
        request=request
    )

    return JsonResponse({
        'html': html,
        'count': len(queries_data),
    })


@staff_member_required
@require_GET
def dashboard_data(request):
    """
    AJAX endpoint for analytics dashboard data.

    Returns dashboard statistics as JSON.
    """
    # Verify AJAX request
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    # Parse date range
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if date_from:
        try:
            from_date = datetime.strptime(date_from, '%Y-%m-%d').date()
        except ValueError:
            from_date = (timezone.now() - timedelta(days=30)).date()
    else:
        from_date = (timezone.now() - timedelta(days=30)).date()

    if date_to:
        try:
            to_date = datetime.strptime(date_to, '%Y-%m-%d').date()
        except ValueError:
            to_date = timezone.now().date()
    else:
        to_date = timezone.now().date()

    engine = request.GET.get('engine')

    analytics = AnalyticsService()
    stats = analytics.get_dashboard_stats(
        date_from=from_date,
        date_to=to_date,
        engine_slug=engine
    )

    return JsonResponse(stats)


@staff_member_required
@require_GET
def filter_synonyms(request):
    """
    AJAX filter endpoint for synonyms.

    Returns rendered HTML for synonym cards.
    """
    # Verify AJAX request
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    queryset = Synonym.objects.all()

    # Search filter
    search = request.GET.get('search', '').strip()
    if search:
        queryset = queryset.filter(
            Q(term__icontains=search) |
            Q(synonyms__icontains=search)
        )

    # Engine filter
    engine = request.GET.get('engine')
    if engine:
        queryset = queryset.filter(engine__slug=engine)
    elif request.GET.get('no_engine') == 'true':
        queryset = queryset.filter(engine__isnull=True)

    # Active filter
    active = request.GET.get('active')
    if active == 'true':
        queryset = queryset.filter(is_active=True)
    elif active == 'false':
        queryset = queryset.filter(is_active=False)

    # Language filter
    language = request.GET.get('language')
    if language:
        queryset = queryset.filter(language=language)
    elif request.GET.get('no_language') == 'true':
        queryset = queryset.filter(Q(language__isnull=True) | Q(language=''))

    synonyms = queryset.select_related('engine').order_by('term')[:50]

    html = render_to_string(
        'admin/search/partials/synonym_cards.html',
        {'synonyms': synonyms},
        request=request
    )

    return JsonResponse({
        'html': html,
        'count': queryset.count(),
    })


@staff_member_required
@require_GET
def filter_redirects(request):
    """
    AJAX filter endpoint for search redirects.

    Returns rendered HTML for redirect cards.
    """
    # Verify AJAX request
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    queryset = SearchRedirect.objects.all()

    # Search filter
    search = request.GET.get('search', '').strip()
    if search:
        queryset = queryset.filter(
            Q(term__icontains=search) |
            Q(redirect_url__icontains=search)
        )

    # Match type filter
    match_type = request.GET.get('match_type')
    if match_type:
        queryset = queryset.filter(match_type=match_type)

    # Engine filter
    engine = request.GET.get('engine')
    if engine:
        queryset = queryset.filter(engine__slug=engine)
    elif request.GET.get('no_engine') == 'true':
        queryset = queryset.filter(engine__isnull=True)

    # Active filter
    active = request.GET.get('active')
    if active == 'true':
        queryset = queryset.filter(is_active=True)
    elif active == 'false':
        queryset = queryset.filter(is_active=False)

    redirects = queryset.select_related('engine').order_by('-hit_count', 'term')[:50]

    html = render_to_string(
        'admin/search/partials/redirect_cards.html',
        {'redirects': redirects},
        request=request
    )

    return JsonResponse({
        'html': html,
        'count': queryset.count(),
    })


@staff_member_required
@require_GET
def filter_engines(request):
    """
    AJAX filter endpoint for search engines.

    Returns rendered HTML for engine cards.
    """
    # Verify AJAX request
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    queryset = SearchEngine.objects.all()

    # Search filter
    search = request.GET.get('search', '').strip()
    if search:
        queryset = queryset.filter(
            Q(name__icontains=search) |
            Q(slug__icontains=search)
        )

    # Active filter
    active = request.GET.get('active')
    if active == 'true':
        queryset = queryset.filter(is_active=True)
    elif active == 'false':
        queryset = queryset.filter(is_active=False)

    # Annotate with counts for display
    engines = queryset.order_by('name')[:50]

    # Add annotation for excluded counts
    engines_with_counts = []
    for engine in engines:
        engine.excluded_categories_count = engine.excluded_categories.count()
        engine.excluded_brands_count = engine.excluded_brands.count()
        engines_with_counts.append(engine)

    html = render_to_string(
        'admin/search/partials/engine_cards.html',
        {'engines': engines_with_counts},
        request=request
    )

    return JsonResponse({
        'html': html,
        'count': queryset.count(),
    })


@staff_member_required
@require_GET
def export_analytics(request):
    """
    Export analytics data as CSV.
    """
    # Parse date range
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if date_from:
        try:
            from_date = datetime.strptime(date_from, '%Y-%m-%d').date()
        except ValueError:
            from_date = (timezone.now() - timedelta(days=30)).date()
    else:
        from_date = (timezone.now() - timedelta(days=30)).date()

    if date_to:
        try:
            to_date = datetime.strptime(date_to, '%Y-%m-%d').date()
        except ValueError:
            to_date = timezone.now().date()
    else:
        to_date = timezone.now().date()

    analytics = AnalyticsService()
    csv_data = analytics.export_analytics(from_date, to_date)

    response = HttpResponse(csv_data, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="search_analytics_{from_date}_{to_date}.csv"'
    return response
