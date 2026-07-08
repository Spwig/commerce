"""
Frontend views for search results page.
"""
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.utils.translation import get_language

from search.services import SearchService
from search.models import SearchSettings

# Export wizard views
from .engine_wizard import (
    EngineWizardStep1View,
    EngineWizardStep2View,
    EngineWizardStep3View,
    EngineWizardStep4View,
)


class SearchResultsView(TemplateView):
    """
    Search results page view.

    Renders the full search results page with filters and pagination.
    """
    template_name = 'search/search_results.html'

    def get(self, request, *args, **kwargs):
        """Handle GET request, check for redirects first."""
        query = request.GET.get('q', '').strip()

        if query:
            search_service = SearchService()

            # Check for redirect
            redirect_info = search_service.check_redirect(
                query=query,
                engine_slug=request.GET.get('engine', 'shop')
            )

            if redirect_info:
                # Perform the redirect
                redirect_type = redirect_info.get('type', 'temporary')
                url = redirect_info.get('url', '/')

                if redirect_type == 'permanent':
                    return redirect(url, permanent=True)
                else:
                    return redirect(url)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query = self.request.GET.get('q', '').strip()
        language = get_language() or 'en'
        engine_slug = self.request.GET.get('engine', 'shop')

        # Get settings
        settings = SearchSettings.get_settings()
        context['search_settings'] = settings

        if not query:
            context['query'] = ''
            context['results'] = []
            context['total_count'] = 0
            context['show_empty_state'] = True
            return context

        # Build filters from query params
        filters = {}
        if self.request.GET.get('type'):
            filters['type'] = self.request.GET.get('type')
        if self.request.GET.get('category'):
            try:
                filters['category'] = int(self.request.GET.get('category'))
            except ValueError:
                pass
        if self.request.GET.get('brand'):
            try:
                filters['brand'] = int(self.request.GET.get('brand'))
            except ValueError:
                pass
        if self.request.GET.get('min_price'):
            try:
                filters['min_price'] = float(self.request.GET.get('min_price'))
            except ValueError:
                pass
        if self.request.GET.get('max_price'):
            try:
                filters['max_price'] = float(self.request.GET.get('max_price'))
            except ValueError:
                pass
        if self.request.GET.get('in_stock'):
            filters['in_stock'] = self.request.GET.get('in_stock').lower() == 'true'

        # Pagination
        page = 1
        if self.request.GET.get('page'):
            try:
                page = max(1, int(self.request.GET.get('page')))
            except ValueError:
                pass

        sort = self.request.GET.get('sort', 'relevance')

        # Perform search
        search_service = SearchService()
        results = search_service.search(
            query=query,
            language=language,
            engine_slug=engine_slug,
            filters=filters,
            page=page,
            sort=sort,
        )

        # Track the query
        if results.get('total_count', 0) >= 0:
            search_service.track_query(
                query=query,
                result_count=results.get('total_count', 0),
                language=language,
                engine_slug=engine_slug,
                response_time_ms=results.get('response_time_ms', 0),
                user=self.request.user if self.request.user.is_authenticated else None,
                session_key=self.request.session.session_key or '',
            )

        # Add to context
        context['query'] = query
        context['language'] = language
        context['results'] = results.get('results', [])
        context['total_count'] = results.get('total_count', 0)
        context['page'] = results.get('page', 1)
        context['per_page'] = results.get('per_page', 20)
        context['total_pages'] = results.get('total_pages', 0)
        context['facets'] = results.get('facets', {})
        context['applied_synonyms'] = results.get('applied_synonyms', [])
        context['did_you_mean'] = results.get('did_you_mean')
        context['response_time_ms'] = results.get('response_time_ms', 0)

        # Current filter values for form
        context['current_filters'] = {
            'type': self.request.GET.get('type', ''),
            'category': self.request.GET.get('category', ''),
            'brand': self.request.GET.get('brand', ''),
            'min_price': self.request.GET.get('min_price', ''),
            'max_price': self.request.GET.get('max_price', ''),
            'in_stock': self.request.GET.get('in_stock', ''),
            'sort': sort,
        }

        # Pagination range
        context['page_range'] = self._get_page_range(
            results.get('page', 1),
            results.get('total_pages', 0)
        )

        context['show_empty_state'] = results.get('total_count', 0) == 0

        return context

    def _get_page_range(self, current_page, total_pages, window=2):
        """Generate page range for pagination."""
        if total_pages <= 1:
            return []

        start = max(1, current_page - window)
        end = min(total_pages, current_page + window)

        # Extend to show at least 5 pages if possible
        while end - start < 4 and (start > 1 or end < total_pages):
            if start > 1:
                start -= 1
            elif end < total_pages:
                end += 1

        return list(range(start, end + 1))


__all__ = [
    'SearchResultsView',
    'EngineWizardStep1View',
    'EngineWizardStep2View',
    'EngineWizardStep3View',
    'EngineWizardStep4View',
]
