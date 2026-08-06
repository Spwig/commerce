"""
Template filters for order displays
"""

from django import template

from geoip.models import CountryMapping

register = template.Library()


@register.filter
def money_format(value):
    """
    Format Money object with space between currency and amount

    Example: SGD70.20 -> SGD 70.20
    """
    if value in (None, ""):
        return value

    # Convert Money object to string
    money_str = str(value)

    # Separate an optional leading minus sign so it stays with the amount
    sign = ""
    if money_str.startswith("-"):
        sign = "-"
        money_str = money_str[1:]

    # Split on first digit to separate currency from amount
    for i, char in enumerate(money_str):
        if char.isdigit():
            return f"{money_str[:i]} {sign}{money_str[i:]}"

    return f"{sign}{money_str}"


@register.filter
def country_name(country_code):
    """
    Convert country code to full country name using CountryMapping

    Example: SG -> Singapore, US -> United States
    """
    if not country_code:
        return country_code

    try:
        mapping = CountryMapping.objects.get(country_code__iexact=country_code)
        return mapping.country_name
    except CountryMapping.DoesNotExist:
        # Fallback to country code if not found in mapping
        return country_code
