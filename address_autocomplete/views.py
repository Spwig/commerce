"""
Views for address autocomplete functionality
"""
import json
import logging
import re
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django_countries import countries

from .services import AutocompleteClient, AddressEnhancer

logger = logging.getLogger(__name__)

# Module-level singleton client with pre-warmed token for better performance
_autocomplete_client = None

def get_autocomplete_client():
    """Get or create singleton autocomplete client with pre-warmed JWT token"""
    global _autocomplete_client
    if _autocomplete_client is None:
        _autocomplete_client = AutocompleteClient(prewarm_token=True)
    return _autocomplete_client

class AutocompleteView(View):
    """Handle autocomplete requests"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = get_autocomplete_client()

    def get_user_tier(self, request):
        """Determine user tier from request"""
        if request.user.is_superuser:
            return "admin"
        elif request.user.is_authenticated:
            # Check if merchant (you might have a merchant flag/group)
            if hasattr(request.user, 'is_merchant') and request.user.is_merchant:
                return "merchant"
            return "authenticated"
        return "anonymous"

    def get_geo_bias(self, request):
        """Extract geo-bias from request"""
        # Try to get from GeoIP middleware
        geo_location = getattr(request, 'geo_location', {})
        lat = lon = None

        if geo_location:
            coords = geo_location.get('coordinates', {})
            lat = coords.get('lat')
            lon = coords.get('lon')

        # Override with explicit parameters
        if 'lat' in request.GET and 'lon' in request.GET:
            try:
                lat = float(request.GET['lat'])
                lon = float(request.GET['lon'])
            except ValueError:
                pass

        return lat, lon

    def get_country_bias(self, request):
        """Extract country bias from request"""
        country_bias = request.GET.get('country')

        # Get geo location from middleware if available
        if not country_bias and hasattr(request, 'geo_location'):
            country_bias = request.geo_location.get('country_code')

        return country_bias

    def _is_postcode_query(self, query, country_code):
        """Detect if query looks like a postcode"""
        if not query or not country_code:
            return False

        query_clean = query.strip().replace(' ', '')

        # Country-specific postcode patterns
        patterns = {
            'SG': r'^\d{6}$',  # Singapore: 6 digits
            'AU': r'^\d{4}$',  # Australia: 4 digits
            'GB': r'^[A-Z]{1,2}\d{1,2}[A-Z]?\s?\d[A-Z]{2}$',  # UK
            'US': r'^\d{5}(-\d{4})?$',  # US: 5 or 9 digits
            'CA': r'^[A-Z]\d[A-Z]\s?\d[A-Z]\d$',  # Canada
        }

        pattern = patterns.get(country_code.upper())
        if pattern:
            return bool(re.match(pattern, query_clean, re.IGNORECASE))

        # Generic: mostly digits (>70%)
        if len(query_clean) > 0:
            digit_ratio = len(re.findall(r'\d', query_clean)) / len(query_clean)
            return digit_ratio > 0.7

        return False

    def _sort_by_country_match(self, suggestions, preferred_country):
        """Sort suggestions with preferred country first, then by confidence"""
        if not suggestions or not preferred_country:
            return suggestions

        def sort_key(suggestion):
            # Get country from suggestion components
            components = suggestion.get('components', {})
            suggestion_country = components.get('country_code', '').upper()
            confidence = suggestion.get('confidence', 0.5)

            # Country match gets priority boost
            if suggestion_country == preferred_country.upper():
                priority = 0  # Highest priority
            else:
                priority = 1  # Lower priority

            # Within each priority group, sort by confidence (descending)
            return (priority, -confidence)

        return sorted(suggestions, key=sort_key)

    def get(self, request):
        """Handle GET request for autocomplete"""
        query = request.GET.get('q', '').strip()

        if len(query) < 3:
            return JsonResponse({
                'suggestions': [],
                'error': 'Query must be at least 3 characters'
            })

        # Get parameters
        country_bias = self.get_country_bias(request)
        lat, lon = self.get_geo_bias(request)
        limit = min(int(request.GET.get('limit', 10)), 10)
        user_tier = self.get_user_tier(request)

        # Detect if query is likely a postcode
        is_postcode = self._is_postcode_query(query, country_bias)

        # Request extra results for filtering if we're applying country bias
        request_limit = 15 if country_bias else limit

        # Call autocomplete service
        result = self.client.autocomplete(
            query=query,
            country_bias=country_bias,
            lat=lat,
            lon=lon,
            limit=request_limit,
            user_tier=user_tier,
            is_postcode=is_postcode
        )

        # Apply country-based sorting if we have suggestions and country bias
        if 'suggestions' in result and country_bias and result['suggestions']:
            result['suggestions'] = self._sort_by_country_match(
                result['suggestions'],
                country_bias
            )

            # Limit to requested amount after sorting
            result['suggestions'] = result['suggestions'][:limit]

        # Enrich suggestions with full country names from django-countries
        if 'suggestions' in result:
            for suggestion in result['suggestions']:
                components = suggestion.get('components', {})
                country_code = components.get('country_code')

                # Add full country name if we have a country code
                if country_code:
                    country_code_upper = country_code.upper()
                    # django-countries provides a dict-like object
                    country_name = countries.name(country_code_upper)
                    if country_name:
                        components['country'] = country_name

        return JsonResponse(result)


@method_decorator(csrf_exempt, name='dispatch')
class NormalizeView(View):
    """Handle address normalization requests"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = get_autocomplete_client()

    def post(self, request):
        """Handle POST request for normalization"""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        address = data.get('address', '').strip()

        if not address:
            return JsonResponse({'error': 'No address provided'}, status=400)

        # Get user tier
        user_tier = "authenticated" if request.user.is_authenticated else "anonymous"

        # Normalize address
        result = self.client.normalize_address(address, user_tier)

        return JsonResponse(result)


class ValidateView(View):
    """Handle address validation requests"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.enhancer = AddressEnhancer(client=get_autocomplete_client())

    def get(self, request):
        """Validate address from query parameters"""
        address_data = {
            'address1': request.GET.get('address1', ''),
            'address2': request.GET.get('address2', ''),
            'city': request.GET.get('city', ''),
            'state': request.GET.get('state', ''),
            'postal_code': request.GET.get('postal_code', ''),
            'country': request.GET.get('country', '')
        }

        # Remove empty fields
        address_data = {k: v for k, v in address_data.items() if v}

        if not address_data:
            return JsonResponse({'error': 'No address data provided'}, status=400)

        # Get user tier
        user_tier = "authenticated" if request.user.is_authenticated else "anonymous"

        # Validate and enhance
        is_valid, enhanced_data, errors = self.enhancer.validate_and_enhance(
            address_data,
            user_tier
        )

        return JsonResponse({
            'valid': is_valid,
            'errors': errors,
            'enhanced': enhanced_data if is_valid else None
        })


@method_decorator(login_required, name='dispatch')
class EnhanceAddressView(View):
    """Enhance existing address with geocoding and normalization"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.enhancer = AddressEnhancer(client=get_autocomplete_client())

    def post(self, request):
        """Enhance address data"""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        address_data = data.get('address', {})

        if not address_data:
            return JsonResponse({'error': 'No address data provided'}, status=400)

        # Get user tier
        user_tier = "merchant" if hasattr(request.user, 'is_merchant') else "authenticated"

        # Enhance address
        enhanced = self.enhancer.enhance_address_data(address_data, user_tier)

        return JsonResponse({'enhanced': enhanced})


class ReverseGeocodeView(View):
    """Handle reverse geocoding requests"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = get_autocomplete_client()

    def get(self, request):
        """Reverse geocode coordinates"""
        try:
            lat = float(request.GET.get('lat'))
            lon = float(request.GET.get('lon'))
        except (TypeError, ValueError):
            return JsonResponse({'error': 'Invalid coordinates'}, status=400)

        # Get user tier
        user_tier = "authenticated" if request.user.is_authenticated else "anonymous"

        # Reverse geocode
        result = self.client.reverse_geocode(lat, lon, user_tier)

        return JsonResponse(result)


class ServiceHealthView(View):
    """Check health of autocomplete service"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = get_autocomplete_client()

    def get(self, request):
        """Get service health status"""
        health = self.client.get_service_health()

        # Add Django app health
        health['django_integration'] = {
            'status': 'healthy',
            'cache_backend': 'redis' if hasattr(request, 'session') else 'none'
        }

        return JsonResponse(health)
