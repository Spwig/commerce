"""
Core utility functions for the e-commerce platform
"""

from ..models import SiteSettings


def get_site_settings():
    """
    Convenience function to get the current site settings.
    This can be used throughout the application to access site configuration.

    Returns:
        SiteSettings: The current site settings instance
    """
    return SiteSettings.get_settings()


def get_site_name():
    """
    Get the current site name

    Returns:
        str: The site name
    """
    return get_site_settings().site_name


def get_admin_email():
    """
    Get the admin email address

    Returns:
        str: The admin email address
    """
    return get_site_settings().admin_email


def get_support_email():
    """
    Get the support email address (falls back to admin email if not set)

    Returns:
        str: The support email address
    """
    return get_site_settings().get_support_email()


def is_maintenance_mode():
    """
    Check if the site is in maintenance mode

    Returns:
        bool: True if maintenance mode is enabled
    """
    return get_site_settings().maintenance_mode


def get_default_currency():
    """
    Get the default currency for the site

    Returns:
        str: The default currency code (e.g., 'USD')
    """
    return get_site_settings().default_currency


def get_default_country():
    """
    Get the merchant's default country as a 2-letter ISO code.

    Derives from SiteSettings.country (business address), converting full
    country names to codes. Falls back to shipping_origin_country.

    Returns:
        str: Two-letter ISO 3166-1 alpha-2 country code (e.g., 'US', 'DE')
    """
    settings = get_site_settings()
    country = settings.country
    if country:
        if len(country) == 2:
            return country.upper()
        # Convert full name to code
        try:
            from geoip.models import CountryMapping
            mapping = CountryMapping.objects.filter(
                country_name__iexact=country
            ).first()
            if mapping:
                return mapping.country_code
        except Exception:
            pass
    return settings.shipping_origin_country or 'US'


def get_shipping_origin_country():
    """
    Get the merchant's shipping origin country (2-letter ISO code).

    Returns:
        str: Two-letter ISO 3166-1 alpha-2 country code (e.g., 'US')
    """
    return get_site_settings().shipping_origin_country or 'US'


def allows_guest_checkout():
    """
    Check if guest checkout is allowed

    Returns:
        bool: True if guest checkout is enabled
    """
    return get_site_settings().allow_guest_checkout


def get_low_stock_threshold():
    """
    Get the low stock alert threshold

    Returns:
        int: The stock level at which to send alerts
    """
    return get_site_settings().low_stock_threshold


def safe_money_sum(items, currency=None):
    """
    Safely sum Money values, returning Money(0, currency) for empty iterables.

    This function solves the problem where Python's sum() returns 0 (integer)
    for empty iterables, which breaks when working with django-money Money fields.

    Args:
        items: Iterable of Money objects to sum
        currency: Currency code to use for zero value (optional, defaults to site currency)

    Returns:
        Money: Sum of all items, or Money(0, currency) if items is empty

    Example:
        # Instead of: total = sum(item.price for item in items)
        # Use: total = safe_money_sum(item.price for item in items)
    """
    from djmoney.money import Money

    items_list = list(items)
    if not items_list:
        if currency is None:
            currency = get_default_currency()
        return Money(0, currency)

    return sum(items_list)
