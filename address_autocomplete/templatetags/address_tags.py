"""
Template tags for address autocomplete
"""
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from django.templatetags.static import static
import json

register = template.Library()

@register.inclusion_tag('address_autocomplete/widget.html')
def address_autocomplete_widget(
    field_id='id_address',
    options=None,
    css_class='',
    placeholder='Start typing an address...'
):
    """
    Render address autocomplete widget

    Usage:
        {% load address_tags %}
        {% address_autocomplete_widget field_id="id_shipping_address" %}
    """
    # Check if service is available (maintenance status)
    enabled = getattr(settings, 'ADDRESS_AUTOCOMPLETE_ENABLED', True)
    if enabled:
        try:
            from core.license import get_license_manager
            if not get_license_manager().are_spwig_services_available():
                enabled = False
        except Exception:
            pass  # Fail open

    if not enabled:
        return {'enabled': False}

    default_options = {
        'minChars': 3,
        'delay': 300,
        'maxSuggestions': 5,
        'autoDetectCountry': True
    }

    if options:
        default_options.update(options)

    return {
        'enabled': True,
        'field_id': field_id,
        'options': json.dumps(default_options),
        'css_class': css_class,
        'placeholder': placeholder
    }


@register.simple_tag
def address_autocomplete_scripts():
    """
    Include necessary JavaScript for autocomplete

    Usage:
        {% load address_tags %}
        {% address_autocomplete_scripts %}
    """
    js_url = static('address_autocomplete/js/autocomplete.js')
    css_url = static('address_autocomplete/css/autocomplete.css')

    return mark_safe(f'''
        <link rel="stylesheet" href="{css_url}">
        <script src="{js_url}"></script>
    ''')


@register.simple_tag
def init_address_autocomplete(
    selector,
    api_url='/api/address/autocomplete',
    **kwargs
):
    """
    Initialize address autocomplete on specific element

    Usage:
        {% load address_tags %}
        {% init_address_autocomplete "#shipping-address" postalCodeFirst=True %}
    """
    options = {
        'apiUrl': api_url,
        'normalizeUrl': '/api/address/normalize',
        'validateUrl': '/api/address/validate'
    }
    options.update(kwargs)

    script = f'''
        <script>
        document.addEventListener('DOMContentLoaded', function() {{
            new AddressAutocomplete('{selector}', {json.dumps(options)});
        }});
        </script>
    '''

    return mark_safe(script)


@register.inclusion_tag('address_autocomplete/checkout_integration.html')
def checkout_address_autocomplete(
    shipping_prefix='shipping_',
    billing_prefix='billing_',
    separate_billing=True
):
    """
    Complete checkout form integration

    Usage:
        {% load address_tags %}
        {% checkout_address_autocomplete %}
    """
    return {
        'shipping_prefix': shipping_prefix,
        'billing_prefix': billing_prefix,
        'separate_billing': separate_billing
    }


@register.filter
def format_address_components(components):
    """
    Format address components for display

    Usage:
        {{ suggestion.components|format_address_components }}
    """
    if not components:
        return ''

    parts = []

    # Build address lines
    if components.get('house_number') and components.get('road'):
        parts.append(f"{components['house_number']} {components['road']}")
    elif components.get('road'):
        parts.append(components['road'])

    if components.get('city'):
        parts.append(components['city'])

    if components.get('state'):
        parts.append(components['state'])

    if components.get('postcode'):
        parts.append(components['postcode'])

    if components.get('country'):
        parts.append(components['country'])

    return ', '.join(parts)


@register.simple_tag(takes_context=True)
def get_address_config(context):
    """
    Get address autocomplete configuration from settings

    Usage:
        {% get_address_config as config %}
    """
    request = context.get('request')

    enabled = getattr(settings, 'ADDRESS_AUTOCOMPLETE_ENABLED', True)
    if enabled:
        try:
            from core.license import get_license_manager
            if not get_license_manager().are_spwig_services_available():
                enabled = False
        except Exception:
            pass  # Fail open

    config = {
        'enabled': enabled,
        'api_url': getattr(settings, 'ADDRESS_AUTOCOMPLETE_URL', '/api/address/autocomplete'),
        'min_chars': getattr(settings, 'ADDRESS_AUTOCOMPLETE_MIN_CHARS', 3),
        'max_suggestions': getattr(settings, 'ADDRESS_AUTOCOMPLETE_MAX_SUGGESTIONS', 5),
        'auto_detect_country': True
    }

    # Add user tier if authenticated
    if request and request.user.is_authenticated:
        if request.user.is_superuser:
            config['user_tier'] = 'admin'
        elif hasattr(request.user, 'is_merchant') and request.user.is_merchant:
            config['user_tier'] = 'merchant'
        else:
            config['user_tier'] = 'authenticated'
    else:
        config['user_tier'] = 'anonymous'

    # Add geo bias from request if available
    if request and hasattr(request, 'geo_location'):
        geo = request.geo_location
        if geo.get('country'):
            config['country_bias'] = geo['country']
        if geo.get('coordinates'):
            config['geo_bias'] = geo['coordinates']

    return config