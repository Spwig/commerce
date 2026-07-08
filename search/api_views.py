"""
DRF API views for search endpoints.
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .serializers import (
    SearchSettingsSerializer,
    SearchEngineSerializer,
    AutocompleteResponseSerializer,
    SearchResultsResponseSerializer,
    TrendingResponseSerializer,
    TrackClickRequestSerializer,
    SuggestCorrectionsResponseSerializer,
)
from .services import SearchService, FuzzyService, AnalyticsService
from .models import SearchSettings, SearchEngine
from core.api.authentication import HeadlessAPIMixin


def get_language_from_request(request) -> str:
    """
    Get language code from request.

    Priority:
    1. Explicit 'lang' query parameter
    2. Accept-Language header
    3. Default to 'en'
    """
    # Check query parameter first
    lang = request.GET.get('lang')
    if lang:
        return lang[:10]  # Truncate for safety

    # Check Accept-Language header
    accept_lang = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
    if accept_lang:
        # Parse first language from header (e.g., "en-US,en;q=0.9,es;q=0.8")
        parts = accept_lang.split(',')
        if parts:
            first_lang = parts[0].split(';')[0].strip()
            # Return just the language code (e.g., 'en' from 'en-US')
            return first_lang.split('-')[0][:10]

    return 'en'


class AutocompleteAPIView(HeadlessAPIMixin, APIView):
    """
    Fast autocomplete endpoint for predictive search.

    Returns grouped results by content type (products, categories, brands, blog posts).
    Target response time: < 200ms
    """
    permission_classes = [AllowAny]

    @extend_schema(
        parameters=[
            OpenApiParameter(name='q', description=_('Search query'), required=True, type=str),
            OpenApiParameter(name='lang', description=_('Language code (e.g., en, es, fr)'), type=str),
            OpenApiParameter(name='engine', description=_('Search engine slug'), type=str, default='shop'),
            OpenApiParameter(name='limit', description=_('Max results per type'), type=int),
        ],
        responses={200: AutocompleteResponseSerializer},
        tags=['Search'],
        summary=_('Autocomplete search'),
        description=_('Fast predictive search suggestions. Returns products, categories, brands, and blog posts.'),
    )
    def get(self, request):
        query = request.GET.get('q', '').strip()
        if not query:
            return Response({
                'query': '',
                'products': [],
                'categories': [],
                'brands': [],
                'blog_posts': [],
                'total_count': 0,
            })

        language = get_language_from_request(request)
        engine = request.GET.get('engine', 'shop')
        limit = request.GET.get('limit')
        if limit:
            try:
                limit = int(limit)
            except ValueError:
                limit = None

        search_service = SearchService()
        results = search_service.autocomplete(
            query=query,
            language=language,
            engine_slug=engine,
            limit=limit,
        )

        # Track the query if settings allow
        if results.get('total_count', 0) >= 0 and 'redirect' not in results:
            search_service.track_query(
                query=query,
                result_count=results.get('total_count', 0),
                language=language,
                engine_slug=engine,
                response_time_ms=results.get('response_time_ms', 0),
                user=request.user if request.user.is_authenticated else None,
                session_key=request.session.session_key or '',
            )

        return Response(results)


class SearchResultsAPIView(HeadlessAPIMixin, APIView):
    """
    Full search results with pagination and facets.

    Returns paginated results with filtering options.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        parameters=[
            OpenApiParameter(name='q', description=_('Search query'), required=True, type=str),
            OpenApiParameter(name='lang', description=_('Language code'), type=str),
            OpenApiParameter(name='engine', description=_('Search engine slug'), type=str, default='shop'),
            OpenApiParameter(name='type', description=_('Filter by type (product/category/brand/blog_post)'), type=str),
            OpenApiParameter(name='category', description=_('Filter by category ID'), type=int),
            OpenApiParameter(name='brand', description=_('Filter by brand ID'), type=int),
            OpenApiParameter(name='min_price', description=_('Minimum price'), type=float),
            OpenApiParameter(name='max_price', description=_('Maximum price'), type=float),
            OpenApiParameter(name='in_stock', description=_('Only in-stock items'), type=bool),
            OpenApiParameter(name='sort', description=_('Sort order (relevance/price_asc/price_desc/newest)'), type=str),
            OpenApiParameter(name='page', description=_('Page number'), type=int, default=1),
            OpenApiParameter(name='per_page', description=_('Results per page'), type=int),
        ],
        responses={200: SearchResultsResponseSerializer},
        tags=['Search'],
        summary=_('Full search results'),
        description=_('Paginated search results with facets and filtering.'),
    )
    def get(self, request):
        query = request.GET.get('q', '').strip()
        search_service = SearchService()

        # Reject too-short queries before any tracking or DB work. Without
        # this gate, a botnet pumping ?q=a,?q=b,... would flood both the
        # search_query table AND the django_session table (via the tracking
        # block further down).
        min_length = search_service.settings.min_query_length or 1
        if not query or len(query) < min_length:
            return Response({
                'query': query,
                'results': [],
                'total_count': 0,
                'page': 1,
                'per_page': 20,
                'total_pages': 0,
                'facets': {},
            })

        language = get_language_from_request(request)
        engine = request.GET.get('engine', 'shop')

        # Build filters
        filters = {}
        if request.GET.get('type'):
            filters['type'] = request.GET.get('type')
        if request.GET.get('category'):
            try:
                filters['category'] = int(request.GET.get('category'))
            except ValueError:
                pass
        if request.GET.get('brand'):
            try:
                filters['brand'] = int(request.GET.get('brand'))
            except ValueError:
                pass
        if request.GET.get('min_price'):
            try:
                filters['min_price'] = float(request.GET.get('min_price'))
            except ValueError:
                pass
        if request.GET.get('max_price'):
            try:
                filters['max_price'] = float(request.GET.get('max_price'))
            except ValueError:
                pass
        if request.GET.get('in_stock'):
            filters['in_stock'] = request.GET.get('in_stock').lower() == 'true'

        # Pagination
        page = 1
        per_page = None
        if request.GET.get('page'):
            try:
                page = max(1, int(request.GET.get('page')))
            except ValueError:
                pass
        if request.GET.get('per_page'):
            try:
                per_page = min(100, max(1, int(request.GET.get('per_page'))))
            except ValueError:
                pass

        sort = request.GET.get('sort', 'relevance')

        results = search_service.search(
            query=query,
            language=language,
            engine_slug=engine,
            filters=filters,
            page=page,
            per_page=per_page,
            sort=sort,
        )

        # Track the query and expose the created SearchQuery ID in the response
        # so headless frontends can later call POST /api/search/click/ with
        # the correct search_query_id to attribute clicks to this search.
        #
        # Note: the search service always includes `redirect` in the result
        # dict (set to None when no redirect matched), so the correct check
        # is `.get('redirect') is None`, not `'redirect' not in results`.
        #
        # Session creation is gated on `track_search_queries` — without
        # the gate, an attacker could flood the session table by pumping
        # queries even when tracking is disabled in SearchSettings.
        tracking_enabled = search_service.settings.track_search_queries
        if (
            tracking_enabled
            and results.get('total_count', 0) >= 0
            and results.get('redirect') is None
        ):
            # Ensure a session exists so anonymous visitors get a stable
            # session_key for click attribution.
            if not request.session.session_key:
                request.session.save()

            search_query = search_service.track_query(
                query=query,
                result_count=results.get('total_count', 0),
                language=language,
                engine_slug=engine,
                response_time_ms=results.get('response_time_ms', 0),
                user=request.user if request.user.is_authenticated else None,
                session_key=request.session.session_key or '',
            )
            if search_query is not None:
                results['search_query_id'] = search_query.id

        return Response(results)


class TrendingSearchesAPIView(HeadlessAPIMixin, APIView):
    """
    Get trending/popular search queries.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        parameters=[
            OpenApiParameter(name='lang', description=_('Language code'), type=str),
            OpenApiParameter(name='engine', description=_('Search engine slug'), type=str),
            OpenApiParameter(name='days', description=_('Number of days to analyze'), type=int, default=7),
            OpenApiParameter(name='limit', description=_('Max results'), type=int, default=10),
        ],
        responses={200: TrendingResponseSerializer},
        tags=['Search'],
        summary=_('Trending searches'),
        description=_('Popular search queries over the specified period.'),
    )
    def get(self, request):
        language = get_language_from_request(request)
        engine = request.GET.get('engine')
        days = 7
        limit = 10

        if request.GET.get('days'):
            try:
                days = min(90, max(1, int(request.GET.get('days'))))
            except ValueError:
                pass
        if request.GET.get('limit'):
            try:
                limit = min(50, max(1, int(request.GET.get('limit'))))
            except ValueError:
                pass

        analytics = AnalyticsService()
        trending = analytics.get_trending_queries(
            days=days,
            limit=limit,
            language=language,
            engine_slug=engine,
        )

        return Response({
            'queries': trending,
            'period_days': days,
        })


class SearchSettingsAPIView(HeadlessAPIMixin, APIView):
    """
    Get public search settings for frontend configuration.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        responses={200: SearchSettingsSerializer},
        tags=['Search'],
        summary=_('Search settings'),
        description=_('Public search configuration for frontend JS.'),
    )
    def get(self, request):
        settings = SearchSettings.get_settings()
        serializer = SearchSettingsSerializer(settings)
        return Response(serializer.data)


class TrackClickAPIView(HeadlessAPIMixin, APIView):
    """
    Track a click on a search result.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        request=TrackClickRequestSerializer,
        responses={200: dict},
        tags=['Search'],
        summary=_('Track click'),
        description=_('Record a click on a search result for analytics.'),
    )
    def post(self, request):
        serializer = TrackClickRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        search_service = SearchService()
        success = search_service.track_click(
            search_query_id=serializer.validated_data['search_query_id'],
            content_type_str=serializer.validated_data['content_type'],
            object_id=serializer.validated_data['object_id'],
            position=serializer.validated_data.get('position', 0),
            user=request.user if request.user.is_authenticated else None,
            session_key=request.session.session_key or '',
        )

        return Response({'success': success})


class SuggestCorrectionsAPIView(HeadlessAPIMixin, APIView):
    """
    Get spelling correction suggestions for a query.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        parameters=[
            OpenApiParameter(name='q', description=_('Search query'), required=True, type=str),
            OpenApiParameter(name='lang', description=_('Language code'), type=str),
        ],
        responses={200: SuggestCorrectionsResponseSerializer},
        tags=['Search'],
        summary=_('Spelling suggestions'),
        description=_('Suggest spelling corrections for misspelled queries.'),
    )
    def get(self, request):
        query = request.GET.get('q', '').strip()
        if not query:
            return Response({
                'query': '',
                'suggestion': None,
                'confidence': None,
            })

        language = get_language_from_request(request)

        fuzzy_service = FuzzyService()
        suggestion = fuzzy_service.suggest_correction(query, language)

        confidence = None
        if suggestion:
            confidence = fuzzy_service.similarity_ratio(query, suggestion)

        return Response({
            'query': query,
            'suggestion': suggestion,
            'confidence': round(confidence, 2) if confidence else None,
        })


class SearchEnginesAPIView(HeadlessAPIMixin, APIView):
    """
    List available search engines.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        responses={200: SearchEngineSerializer(many=True)},
        tags=['Search'],
        summary=_('List search engines'),
        description=_('Get list of available search engines.'),
    )
    def get(self, request):
        engines = SearchEngine.objects.filter(is_active=True)
        serializer = SearchEngineSerializer(engines, many=True)
        return Response(serializer.data)
