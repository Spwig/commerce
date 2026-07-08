"""
GeoIP Integration for Shipping
Provides helper functions to integrate with the geoip app's CountryMapping model
for shipping zones, currencies, and country information.
"""
from typing import Optional, Dict, Any
from django.core.cache import cache


def get_country_mapping(country_code: str) -> Optional['CountryMapping']:
    """
    Get CountryMapping for a given country code.
    Uses caching to reduce database queries.

    Args:
        country_code: Two-letter ISO 3166-1 alpha-2 country code (e.g., 'US', 'CA', 'GB')

    Returns:
        CountryMapping instance or None if not found

    Example:
        >>> mapping = get_country_mapping('US')
        >>> if mapping:
        ...     print(mapping.country_name)  # "United States"
        ...     print(mapping.default_currency)  # "USD"
    """
    if not country_code:
        return None

    # Normalize to uppercase
    country_code = country_code.upper()

    # Check cache first
    cache_key = f'country_mapping:{country_code}'
    mapping = cache.get(cache_key)

    if mapping is None:
        # Import here to avoid circular imports
        from geoip.models import CountryMapping

        try:
            mapping = CountryMapping.objects.get(country_code=country_code, is_active=True)
            # Cache for 1 hour
            cache.set(cache_key, mapping, 3600)
        except CountryMapping.DoesNotExist:
            # Cache the "not found" result for 5 minutes to avoid repeated queries
            cache.set(cache_key, False, 300)
            return None

    # Return None if cached result was False (not found)
    return mapping if mapping else None


def is_domestic_shipment(origin_country: str, dest_country: str) -> bool:
    """
    Check if a shipment is domestic (within the same country).

    Args:
        origin_country: Origin country code (e.g., 'US')
        dest_country: Destination country code (e.g., 'CA')

    Returns:
        True if both countries are the same, False otherwise

    Example:
        >>> is_domestic_shipment('US', 'US')
        True
        >>> is_domestic_shipment('US', 'CA')
        False
    """
    if not origin_country or not dest_country:
        return False

    return origin_country.upper() == dest_country.upper()


def get_shipping_zone(country_code: str, origin_country: str = 'US') -> str:
    """
    Get the shipping zone for a destination country.

    Args:
        country_code: Destination country code
        origin_country: Origin country code (default: 'US')

    Returns:
        Shipping zone identifier ('domestic', 'international', or custom zone from CountryMapping)

    Example:
        >>> get_shipping_zone('US', 'US')
        'domestic'
        >>> get_shipping_zone('CA', 'US')
        'international'
        >>> get_shipping_zone('GB', 'US')  # If GB has custom zone in mapping
        'europe'
    """
    if not country_code:
        return 'international'

    # Check if domestic
    if is_domestic_shipment(origin_country, country_code):
        return 'domestic'

    # Look up custom shipping zone
    mapping = get_country_mapping(country_code)
    if mapping and mapping.shipping_zone:
        return mapping.shipping_zone

    # Default to international
    return 'international'


def get_country_currency(country_code: str) -> str:
    """
    Get the default currency for a country.

    Args:
        country_code: Two-letter country code

    Returns:
        Currency code (e.g., 'USD', 'EUR', 'GBP') or 'USD' as fallback

    Example:
        >>> get_country_currency('US')
        'USD'
        >>> get_country_currency('GB')
        'GBP'
        >>> get_country_currency('XX')  # Unknown country
        'USD'
    """
    mapping = get_country_mapping(country_code)

    if mapping and mapping.default_currency:
        return mapping.default_currency

    # Fallback to store default currency for unknown countries
    from core.utils import get_default_currency
    return get_default_currency()


def get_country_name(country_code: str) -> str:
    """
    Get the full country name from country code.

    Args:
        country_code: Two-letter country code

    Returns:
        Full country name or the country code itself if not found

    Example:
        >>> get_country_name('US')
        'United States'
        >>> get_country_name('SG')
        'Singapore'
        >>> get_country_name('XX')  # Unknown country
        'XX'
    """
    if not country_code:
        return ''

    mapping = get_country_mapping(country_code)

    if mapping and mapping.country_name:
        return mapping.country_name

    # Fallback to country code if not found
    return country_code.upper()


def get_country_info(country_code: str) -> Dict[str, Any]:
    """
    Get comprehensive country information for shipping.

    Args:
        country_code: Two-letter country code

    Returns:
        Dictionary containing country information with keys:
        - country_code: Two-letter code
        - country_name: Full country name
        - currency: Default currency code
        - shipping_zone: Shipping zone identifier
        - tax_rate: Default tax rate
        - is_eu_member: Whether country is in EU
        - requires_vat: Whether VAT is required
        - uses_metric: Whether country uses metric system
        - timezone: Default timezone

    Example:
        >>> info = get_country_info('GB')
        >>> info['country_name']
        'United Kingdom'
        >>> info['currency']
        'GBP'
        >>> info['is_eu_member']
        False
    """
    mapping = get_country_mapping(country_code)

    if mapping:
        return {
            'country_code': mapping.country_code,
            'country_name': mapping.country_name,
            'currency': mapping.default_currency,
            'shipping_zone': mapping.shipping_zone or 'international',
            'tax_rate': float(mapping.tax_rate),
            'is_eu_member': mapping.is_eu_member,
            'requires_vat': mapping.requires_vat,
            'uses_metric': mapping.uses_metric,
            'timezone': mapping.timezone,
            'supports_cod': mapping.supports_cod,
        }

    # Fallback for unknown countries
    from core.utils import get_default_currency
    return {
        'country_code': country_code.upper() if country_code else '',
        'country_name': country_code.upper() if country_code else '',
        'currency': get_default_currency(),
        'shipping_zone': 'international',
        'tax_rate': 0.0,
        'is_eu_member': False,
        'requires_vat': False,
        'uses_metric': True,
        'timezone': '',
        'supports_cod': False,
    }


def get_accepted_currencies(country_code: str) -> list:
    """
    Get list of accepted currencies for a country.

    Args:
        country_code: Two-letter country code

    Returns:
        List of currency codes (always includes default currency)

    Example:
        >>> get_accepted_currencies('US')
        ['USD']
        >>> get_accepted_currencies('EU')
        ['EUR', 'USD']
    """
    mapping = get_country_mapping(country_code)

    if mapping:
        currencies = list(mapping.accepted_currencies) if mapping.accepted_currencies else []
        # Always include default currency
        if mapping.default_currency not in currencies:
            currencies.insert(0, mapping.default_currency)
        return currencies

    # Fallback to store default currency
    from core.utils import get_default_currency
    return [get_default_currency()]


def is_eu_country(country_code: str) -> bool:
    """
    Check if a country is an EU member.

    Args:
        country_code: Two-letter country code

    Returns:
        True if country is EU member, False otherwise

    Example:
        >>> is_eu_country('DE')
        True
        >>> is_eu_country('US')
        False
    """
    mapping = get_country_mapping(country_code)
    return mapping.is_eu_member if mapping else False


def requires_vat_number(country_code: str) -> bool:
    """
    Check if a country requires VAT number for business shipments.

    Args:
        country_code: Two-letter country code

    Returns:
        True if VAT required, False otherwise

    Example:
        >>> requires_vat_number('FR')
        True
        >>> requires_vat_number('US')
        False
    """
    mapping = get_country_mapping(country_code)
    return mapping.requires_vat if mapping else False


def get_tax_rate(country_code: str) -> float:
    """
    Get default tax rate for a country.

    Args:
        country_code: Two-letter country code

    Returns:
        Tax rate as decimal (e.g., 0.20 for 20%)

    Example:
        >>> get_tax_rate('US')
        0.0  # US tax varies by state
        >>> get_tax_rate('GB')
        20.0
    """
    mapping = get_country_mapping(country_code)
    return float(mapping.tax_rate) if mapping else 0.0


def clear_country_cache(country_code: str = None):
    """
    Clear cached country mapping data.

    Args:
        country_code: Specific country code to clear, or None to clear all

    Example:
        >>> clear_country_cache('US')  # Clear US cache
        >>> clear_country_cache()  # Clear all country caches
    """
    if country_code:
        cache_key = f'country_mapping:{country_code.upper()}'
        cache.delete(cache_key)
    else:
        # Clear all country mapping caches
        # Note: This is a simple implementation; for production you might want
        # to use cache versioning or a more sophisticated approach
        from geoip.models import CountryMapping
        for mapping in CountryMapping.objects.all():
            cache_key = f'country_mapping:{mapping.country_code}'
            cache.delete(cache_key)
