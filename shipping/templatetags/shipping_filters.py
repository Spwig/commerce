"""
Template filters for shipping app
Provides filters for displaying shipping-related data
"""

from django import template

from shipping.integrations import get_country_currency, get_country_name, get_shipping_zone

register = template.Library()


@register.filter
def country_name(country_code):
    """
    Convert country code to full country name.

    Usage:
        {{ shipment.dest_country|country_name }}
        {{ 'US'|country_name }}  -> "United States"
    """
    if not country_code:
        return ""
    return get_country_name(country_code)


@register.filter
def shipping_zone(country_code, origin="US"):
    """
    Get shipping zone for a country code.

    Usage:
        {{ shipment.dest_country|shipping_zone }}
        {{ shipment.dest_country|shipping_zone:shipment.origin_country }}
    """
    if not country_code:
        return "international"
    return get_shipping_zone(country_code, origin)


@register.filter
def country_currency(country_code):
    """
    Get currency code for a country.

    Usage:
        {{ shipment.dest_country|country_currency }}
        {{ 'GB'|country_currency }}  -> "GBP"
    """
    if not country_code:
        from core.utils import get_default_currency

        return get_default_currency()
    return get_country_currency(country_code)


@register.filter
def country_with_code(country_code):
    """
    Display country name with code in parentheses.

    Usage:
        {{ shipment.dest_country|country_with_code }}
        "GB" -> "United Kingdom (GB)"
    """
    if not country_code:
        return ""
    name = get_country_name(country_code)
    if name == country_code.upper():
        # Country not found in mapping, just return code
        return country_code.upper()
    return f"{name} ({country_code.upper()})"
