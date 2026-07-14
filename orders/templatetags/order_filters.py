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
    if not value:
        return value

    # Convert Money object to string
    money_str = str(value)

    # Split on first digit to separate currency from amount
    for i, char in enumerate(money_str):
        if char.isdigit() or char == "-":
            return f"{money_str[:i]} {money_str[i:]}"

    return money_str


@register.filter
def country_name(country_code):
    """
    Convert country code to full country name using CountryMapping

    Example: SG -> Singapore, US -> United States
    """
    if not country_code:
        return country_code

    try:
        mapping = CountryMapping.objects.get(country_code=country_code)
        return mapping.country_name
    except CountryMapping.DoesNotExist:
        # Fallback to country code if not found in mapping
        return country_code
