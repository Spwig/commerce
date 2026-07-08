"""
Template tags for GeoIP functionality
"""
from django import template
from django.utils.safestring import mark_safe
from django.conf import settings
import json

register = template.Library()


@register.simple_tag(takes_context=True)
def get_visitor_country(context):
    """
    Get the visitor's country code
    Usage: {% get_visitor_country %}
    """
    request = context.get('request')
    if request and hasattr(request, 'geo_location'):
        location = request.geo_location
        if location:
            return location.get('country', '')
    return ''


@register.simple_tag(takes_context=True)
def get_visitor_location(context):
    """
    Get the visitor's full location data
    Usage: {% get_visitor_location as location %}
    """
    request = context.get('request')
    if request and hasattr(request, 'geo_location'):
        return request.geo_location
    return {}


@register.simple_tag(takes_context=True)
def visitor_currency(context):
    """
    Get the recommended currency for the visitor
    Usage: {% visitor_currency %}
    """
    request = context.get('request')
    if request and hasattr(request, 'geo_location'):
        location = request.geo_location
        if location:
            # Check if user has a preferred currency in session
            preferred = request.session.get('preferred_currency')
            if preferred:
                return preferred
            # Otherwise use geo-based currency
            return location.get('currency', 'USD')
    return 'USD'


@register.simple_tag(takes_context=True)
def visitor_language(context):
    """
    Get the recommended language for the visitor
    Usage: {% visitor_language %}
    """
    request = context.get('request')
    if request and hasattr(request, 'geo_location'):
        location = request.geo_location
        if location:
            # Check if user has a preferred language in session
            preferred = request.session.get('preferred_language')
            if preferred:
                return preferred
            # Otherwise use geo-based language
            return location.get('language', 'en')
    return 'en'


@register.filter
def country_flag(country_code):
    """
    Convert country code to flag emoji
    Usage: {{ "US"|country_flag }}
    """
    if not country_code or len(country_code) != 2:
        return ''
    # Convert country code to flag emoji using regional indicator symbols
    return ''.join(chr(0x1F1E6 + ord(c) - ord('A')) for c in country_code.upper())


@register.simple_tag
def country_name(country_code):
    """
    Get country name from country code
    Usage: {% country_name "US" %}
    """
    from ..models import CountryMapping
    try:
        mapping = CountryMapping.objects.get(country_code=country_code.upper())
        return mapping.country_name
    except CountryMapping.DoesNotExist:
        # Fallback to basic mapping
        countries = {
            'US': 'United States',
            'GB': 'United Kingdom',
            'CA': 'Canada',
            'AU': 'Australia',
            'DE': 'Germany',
            'FR': 'France',
            'ES': 'Spain',
            'IT': 'Italy',
            'JP': 'Japan',
            'CN': 'China',
            'IN': 'India',
            'BR': 'Brazil',
            'MX': 'Mexico',
        }
        return countries.get(country_code.upper(), country_code)


@register.inclusion_tag('geoip/location_widget.html', takes_context=True)
def location_widget(context):
    """
    Render a location selection widget
    Usage: {% location_widget %}
    """
    request = context.get('request')
    location = {}
    if request and hasattr(request, 'geo_location'):
        location = request.geo_location or {}

    return {
        'location': location,
        'country': location.get('country', ''),
        'city': location.get('city', ''),
        'currency': location.get('currency', 'USD'),
        'language': location.get('language', 'en'),
    }


@register.simple_tag
def geoip_script():
    """
    Include the GeoIP JavaScript API via external file (CSP-compliant).
    Usage: {% geoip_script %}

    Prefer using {% static 'geoip/js/geoip-api.js' %} directly in templates.
    """
    from django.templatetags.static import static
    url = static('geoip/js/geoip-api.js')
    return mark_safe(f'<script src="{url}"></script>')


@register.inclusion_tag('geoip/partials/location_debug.html', takes_context=True)
def location_debug(context):
    """
    Display debug information about current location (CSP-compliant).
    Only renders content when DEBUG=True.
    Usage: {% location_debug %}
    """
    if not settings.DEBUG:
        return {'show_debug': False, 'location': {}}

    request = context.get('request')
    if not request or not hasattr(request, 'geo_location'):
        return {'show_debug': True, 'location': {}, 'country_flag': '', 'confidence_pct': '0'}

    location = request.geo_location or {}
    confidence = location.get('confidence', 0) * 100

    return {
        'show_debug': True,
        'location': location,
        'country_flag': country_flag(location.get('country', '')),
        'confidence_pct': f'{confidence:.0f}',
    }