"""
Template filters for unit conversion and formatting.
Automatically converts units based on customer location.
"""
from django import template
from django.utils.safestring import mark_safe
from core.models import SiteSettings
from core.utils.units import UnitConverter

register = template.Library()


@register.filter
def convert_weight(value, customer_country=None):
    """
    Convert weight to customer's preferred unit based on their location.

    Usage in templates:
        {{ product.weight|convert_weight:request.country_code }}
        {{ product.weight|convert_weight }}  (no conversion, just format)

    Args:
        value: Weight value (Decimal)
        customer_country: ISO 2-letter country code (optional)

    Returns:
        Formatted string with converted weight and original in parentheses

    Example:
        Admin stores: 100 g
        US customer sees: "3.53 oz (100 g)"
        EU customer sees: "100 g"
    """
    if not value:
        return ""

    try:
        settings = SiteSettings.get_settings()
        admin_unit = settings.default_weight_unit

        # If conversion is disabled or no country provided, just format with admin unit
        if not settings.enable_unit_conversion or not customer_country:
            return UnitConverter.format_weight(value, admin_unit)

        # Get customer's preferred unit
        customer_unit = UnitConverter.get_country_preferred_weight_unit(customer_country)

        # If units are the same, no conversion needed
        if customer_unit == admin_unit:
            return UnitConverter.format_weight(value, admin_unit)

        # Convert and show both units
        converted_value = UnitConverter.convert_weight(value, admin_unit, customer_unit)

        if converted_value:
            converted_str = UnitConverter.format_weight(converted_value, customer_unit)
            original_str = UnitConverter.format_weight(value, admin_unit)
            return mark_safe(f"{converted_str} <span class='unit-original'>({original_str})</span>")

        return UnitConverter.format_weight(value, admin_unit)

    except Exception as e:
        # Fallback to simple display if something goes wrong
        return f"{value} {getattr(settings, 'default_weight_unit', 'kg')}"


@register.filter
def convert_dimension(value, customer_country=None):
    """
    Convert dimension (length/width/height) to customer's preferred unit.

    Usage in templates:
        {{ product.length|convert_dimension:request.country_code }}
        {{ product.width|convert_dimension }}

    Args:
        value: Length value (Decimal)
        customer_country: ISO 2-letter country code (optional)

    Returns:
        Formatted string with converted dimension and original in parentheses

    Example:
        Admin stores: 10 cm
        US customer sees: "3.9 in (10 cm)"
        EU customer sees: "10 cm"
    """
    if not value:
        return ""

    try:
        settings = SiteSettings.get_settings()
        admin_unit = settings.default_length_unit

        # If conversion is disabled or no country provided, just format with admin unit
        if not settings.enable_unit_conversion or not customer_country:
            return UnitConverter.format_length(value, admin_unit)

        # Get customer's preferred unit
        customer_unit = UnitConverter.get_country_preferred_length_unit(customer_country)

        # If units are the same, no conversion needed
        if customer_unit == admin_unit:
            return UnitConverter.format_length(value, admin_unit)

        # Convert and show both units
        converted_value = UnitConverter.convert_length(value, admin_unit, customer_unit)

        if converted_value:
            converted_str = UnitConverter.format_length(converted_value, customer_unit)
            original_str = UnitConverter.format_length(value, admin_unit)
            return mark_safe(f"{converted_str} <span class='unit-original'>({original_str})</span>")

        return UnitConverter.format_length(value, admin_unit)

    except Exception as e:
        # Fallback to simple display if something goes wrong
        return f"{value} {getattr(settings, 'default_length_unit', 'cm')}"


@register.simple_tag
def format_dimensions(length, width, height, customer_country=None):
    """
    Format product dimensions (L × W × H) with unit conversion.

    Usage in templates:
        {% format_dimensions product.length product.width product.height request.country_code %}

    Args:
        length: Length value
        width: Width value
        height: Height value
        customer_country: ISO 2-letter country code (optional)

    Returns:
        Formatted dimensions string like "10.5 cm × 5.2 cm × 2.1 cm"
        or with conversion: "4.1 in × 2.0 in × 0.8 in (10.5 × 5.2 × 2.1 cm)"
    """
    if not (length and width and height):
        return ""

    try:
        settings = SiteSettings.get_settings()
        admin_unit = settings.default_length_unit

        # If conversion is disabled or no country provided
        if not settings.enable_unit_conversion or not customer_country:
            l_str = UnitConverter.format_length(length, admin_unit)
            w_str = UnitConverter.format_length(width, admin_unit)
            h_str = UnitConverter.format_length(height, admin_unit)
            return mark_safe(f"{l_str} × {w_str} × {h_str}")

        # Get customer's preferred unit
        customer_unit = UnitConverter.get_country_preferred_length_unit(customer_country)

        # If units are the same
        if customer_unit == admin_unit:
            l_str = UnitConverter.format_length(length, admin_unit)
            w_str = UnitConverter.format_length(width, admin_unit)
            h_str = UnitConverter.format_length(height, admin_unit)
            return mark_safe(f"{l_str} × {w_str} × {h_str}")

        # Convert all dimensions
        l_conv = UnitConverter.convert_length(length, admin_unit, customer_unit)
        w_conv = UnitConverter.convert_length(width, admin_unit, customer_unit)
        h_conv = UnitConverter.convert_length(height, admin_unit, customer_unit)

        if l_conv and w_conv and h_conv:
            # Format converted dimensions
            l_conv_str = UnitConverter.format_length(l_conv, customer_unit)
            w_conv_str = UnitConverter.format_length(w_conv, customer_unit)
            h_conv_str = UnitConverter.format_length(h_conv, customer_unit)

            # Format original dimensions
            l_orig_str = f"{float(length):.1f}"
            w_orig_str = f"{float(width):.1f}"
            h_orig_str = f"{float(height):.1f}"

            return mark_safe(
                f"{l_conv_str} × {w_conv_str} × {h_conv_str} "
                f"<span class='unit-original'>({l_orig_str} × {w_orig_str} × {h_orig_str} {admin_unit})</span>"
            )

        # Fallback
        l_str = UnitConverter.format_length(length, admin_unit)
        w_str = UnitConverter.format_length(width, admin_unit)
        h_str = UnitConverter.format_length(height, admin_unit)
        return mark_safe(f"{l_str} × {w_str} × {h_str}")

    except Exception as e:
        # Fallback to simple display
        return f"{length} × {width} × {height} {getattr(settings, 'default_length_unit', 'cm')}"


@register.filter
def convert_volume(value, customer_country=None):
    """
    Convert volume to customer's preferred unit based on their location.

    Usage in templates:
        {{ product.volume|convert_volume:request.country_code }}
        {{ product.volume|convert_volume }}

    Args:
        value: Volume value (Decimal)
        customer_country: ISO 2-letter country code (optional)

    Returns:
        Formatted string with converted volume and original in parentheses

    Example:
        Admin stores: 100 ml
        US customer sees: "3.38 fl oz (100 ml)"
        EU customer sees: "100 ml"
    """
    if not value:
        return ""

    try:
        settings = SiteSettings.get_settings()
        admin_unit = settings.default_volume_unit

        # If conversion is disabled or no country provided, just format with admin unit
        if not settings.enable_unit_conversion or not customer_country:
            return UnitConverter.format_volume(value, admin_unit)

        # Get customer's preferred unit
        customer_unit = UnitConverter.get_country_preferred_volume_unit(customer_country)

        # If units are the same, no conversion needed
        if customer_unit == admin_unit:
            return UnitConverter.format_volume(value, admin_unit)

        # Convert and show both units
        converted_value = UnitConverter.convert_volume(value, admin_unit, customer_unit)

        if converted_value:
            converted_str = UnitConverter.format_volume(converted_value, customer_unit)
            original_str = UnitConverter.format_volume(value, admin_unit)
            return mark_safe(f"{converted_str} <span class='unit-original'>({original_str})</span>")

        return UnitConverter.format_volume(value, admin_unit)

    except Exception as e:
        # Fallback to simple display if something goes wrong
        return f"{value} {getattr(settings, 'default_volume_unit', 'ml')}"


@register.filter
def convert_area(value, customer_country=None):
    """
    Convert area to customer's preferred unit based on their location.

    Usage in templates:
        {{ product.area|convert_area:request.country_code }}
        {{ product.area|convert_area }}

    Args:
        value: Area value (Decimal)
        customer_country: ISO 2-letter country code (optional)

    Returns:
        Formatted string with converted area and original in parentheses

    Example:
        Admin stores: 1 sq_m
        US customer sees: "10.76 sq ft (1 sq m)"
        EU customer sees: "1 sq m"
    """
    if not value:
        return ""

    try:
        settings = SiteSettings.get_settings()
        admin_unit = settings.default_area_unit

        # If conversion is disabled or no country provided, just format with admin unit
        if not settings.enable_unit_conversion or not customer_country:
            return UnitConverter.format_area(value, admin_unit)

        # Get customer's preferred unit
        customer_unit = UnitConverter.get_country_preferred_area_unit(customer_country)

        # If units are the same, no conversion needed
        if customer_unit == admin_unit:
            return UnitConverter.format_area(value, admin_unit)

        # Convert and show both units
        converted_value = UnitConverter.convert_area(value, admin_unit, customer_unit)

        if converted_value:
            converted_str = UnitConverter.format_area(converted_value, customer_unit)
            original_str = UnitConverter.format_area(value, admin_unit)
            return mark_safe(f"{converted_str} <span class='unit-original'>({original_str})</span>")

        return UnitConverter.format_area(value, admin_unit)

    except Exception as e:
        # Fallback to simple display if something goes wrong
        return f"{value} {getattr(settings, 'default_area_unit', 'sq_m')}"


@register.filter
def convert_temperature(value, customer_country=None):
    """
    Convert temperature to customer's preferred unit based on their location.

    Usage in templates:
        {{ product.operating_temp|convert_temperature:request.country_code }}
        {{ product.storage_temp|convert_temperature }}

    Args:
        value: Temperature value (Decimal)
        customer_country: ISO 2-letter country code (optional)

    Returns:
        Formatted string with converted temperature and original in parentheses

    Example:
        Admin stores: 20 c
        US customer sees: "68.0°F (20.0°C)"
        EU customer sees: "20.0°C"
    """
    if value is None:
        return ""

    try:
        settings = SiteSettings.get_settings()
        admin_unit = settings.default_temperature_unit

        # If conversion is disabled or no country provided, just format with admin unit
        if not settings.enable_unit_conversion or not customer_country:
            return UnitConverter.format_temperature(value, admin_unit)

        # Get customer's preferred unit
        customer_unit = UnitConverter.get_country_preferred_temperature_unit(customer_country)

        # If units are the same, no conversion needed
        if customer_unit == admin_unit:
            return UnitConverter.format_temperature(value, admin_unit)

        # Convert and show both units
        converted_value = UnitConverter.convert_temperature(value, admin_unit, customer_unit)

        if converted_value is not None:
            converted_str = UnitConverter.format_temperature(converted_value, customer_unit)
            original_str = UnitConverter.format_temperature(value, admin_unit)
            return mark_safe(f"{converted_str} <span class='unit-original'>({original_str})</span>")

        return UnitConverter.format_temperature(value, admin_unit)

    except Exception as e:
        # Fallback to simple display if something goes wrong
        return f"{value} {getattr(settings, 'default_temperature_unit', 'c')}"


# Dictionary access filter
@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary by key. Usage: {{ mydict|get_item:key }}"""
    if dictionary is None:
        return None
    return dictionary.get(str(key))


# Math filters
@register.filter
def mul(value, arg):
    """Multiply value by arg."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def div(value, arg):
    """Divide value by arg."""
    try:
        arg = float(arg)
        if arg == 0:
            return 0
        return float(value) / arg
    except (ValueError, TypeError):
        return 0


@register.filter
def sub(value, arg):
    """Subtract arg from value."""
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return 0
