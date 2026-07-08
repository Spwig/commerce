"""
Marketplace Views
Browse, detail, install, and review components from the marketplace.
"""

import json
import logging
from urllib.parse import urlparse
from django.conf import settings as django_settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _, get_language
from django.views import View
from django.views.decorators.http import require_POST, require_GET
from django.template.response import TemplateResponse

from django_countries import countries as django_countries
from providers_common.utils import get_translated_provider_fields
from .services import MarketplaceService

logger = logging.getLogger(__name__)


def _upgrade_server_origin():
    """Extract origin (scheme + host) from UPGRADE_SERVER_URL for preconnect hints."""
    url = getattr(django_settings, 'UPGRADE_SERVER_URL', 'https://updates.spwig.com')
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"




@method_decorator(staff_member_required, name='dispatch')
class BrowseView(View):
    """Main marketplace browse page."""

    template_name = 'admin/marketplace/browse.html'

    def get(self, request):
        service = MarketplaceService()
        component_types = service.get_component_types()

        country_list = sorted(django_countries, key=lambda x: x[1])

        context = {
            'title': _('Marketplace'),
            'component_types': component_types,
            'countries': country_list,
            'upgrade_server_origin': _upgrade_server_origin(),
            'has_permission': True,
            'is_nav_sidebar_enabled': True,
        }
        return TemplateResponse(request, self.template_name, context)


@method_decorator(staff_member_required, name='dispatch')
class DetailView(View):
    """Full detail page for a single marketplace component."""

    template_name = 'admin/marketplace/detail.html'

    def get(self, request, slug):
        service = MarketplaceService()
        component = service.get_detail(slug)

        if not component:
            from django.http import Http404
            raise Http404(_('Component not found'))

        # Translate provider name/description from manifest translations
        lang = get_language() or 'en'
        translated = get_translated_provider_fields(component, lang)
        component['name'] = translated['name']
        component['description'] = translated['description']

        # Inject detail URL for templates
        from django.urls import reverse
        component['detail_url'] = reverse('marketplace:detail', args=[slug])

        # Pre-serialize reviews_summary as JSON for safe embedding in template
        component['reviews_summary_json'] = json.dumps(
            component.get('reviews_summary') or {}
        )

        # If modal=true query param, return partial
        if request.GET.get('modal') == 'true':
            return TemplateResponse(
                request,
                'admin/marketplace/partials/detail_modal.html',
                {'component': component, 'has_permission': True},
            )

        context = {
            'title': component.get('name', slug),
            'component': component,
            'upgrade_server_origin': _upgrade_server_origin(),
            'has_permission': True,
            'is_nav_sidebar_enabled': True,
        }
        return TemplateResponse(request, self.template_name, context)


@staff_member_required
def browse_api(request):
    """AJAX endpoint for marketplace browse with filters."""
    service = MarketplaceService()

    filters = {}
    for param in ('type', 'pricing', 'author', 'q', 'sort', 'country', 'page', 'page_size'):
        val = request.GET.get(param, '').strip()
        if val:
            filters[param] = val

    data = service.browse(filters)
    return JsonResponse(data)


@staff_member_required
@require_POST
def install_ajax(request):
    """AJAX endpoint to install a free component."""
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

    slug = body.get('slug', '').strip()
    version = body.get('version', '').strip() or None

    if not slug:
        return JsonResponse({'success': False, 'error': 'slug is required'}, status=400)

    service = MarketplaceService()
    result = service.install_free_component(slug, version)

    if result and result.get('success'):
        return JsonResponse({
            'success': True,
            'message': _('Component installed successfully.'),
        })
    else:
        error = result.get('error', _('Installation failed')) if result else _('Installation failed')
        return JsonResponse({'success': False, 'error': error}, status=400)


@staff_member_required
@require_POST
def review_ajax(request):
    """AJAX endpoint to submit a review."""
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

    slug = body.get('slug', '').strip()
    rating = body.get('rating')
    title = body.get('title', '').strip()
    comment = body.get('comment', '').strip()

    if not slug:
        return JsonResponse({'success': False, 'error': 'slug is required'}, status=400)

    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            raise ValueError
    except (TypeError, ValueError):
        return JsonResponse({'success': False, 'error': 'rating must be 1-5'}, status=400)

    service = MarketplaceService()
    result = service.submit_review(slug, rating, title, comment)

    if result and result.get('success'):
        return JsonResponse({'success': True, 'message': _('Review submitted.')})
    else:
        error = result.get('error', _('Failed to submit review')) if result else _('Failed to submit review')
        return JsonResponse({'success': False, 'error': error}, status=400)


@staff_member_required
@require_GET
def purchase_redirect(request, slug):
    """Redirect to spwig.com for purchasing a paid component."""
    service = MarketplaceService()
    return_url = request.build_absolute_uri(reverse('marketplace:detail', args=[slug]))
    data = service.get_purchase_url(slug, return_url=return_url)

    if data and data.get('purchase_url'):
        return JsonResponse({'purchase_url': data['purchase_url']})
    else:
        return JsonResponse({'error': _('Could not generate purchase URL')}, status=400)
