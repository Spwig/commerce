"""
Template tags for rendering admin readonly fields in custom templates
"""

from decimal import Decimal

from django import template

register = template.Library()


@register.filter
def money_amount(value):
    """
    Safely extract the amount from a MoneyField value.

    Works with:
    - Money objects (value.amount)
    - Lists/tuples [amount, currency] from bound form data
    - Decimal/float values directly
    - None or empty values

    Usage in template:
        {{ adminform.form.price.value|money_amount }}
    """
    if value is None:
        return ""

    # Handle Money objects
    if hasattr(value, "amount"):
        return value.amount

    # Handle list/tuple from MultiWidget (bound form data)
    if isinstance(value, (list, tuple)) and len(value) >= 1:
        return value[0] if value[0] not in (None, "") else ""

    # Handle Decimal/float/int directly
    if isinstance(value, (Decimal, float, int)):
        return value

    # Handle string representation
    if isinstance(value, str):
        return value

    return ""


@register.filter
def money_currency(value):
    """
    Safely extract the currency from a MoneyField value.

    Works with:
    - Money objects (value.currency or value.currency.code)
    - Lists/tuples [amount, currency] from bound form data
    - String currency codes directly
    - None or empty values

    Usage in template:
        {{ adminform.form.price.value|money_currency }}
    """
    if value is None:
        return ""

    # Handle Money objects
    if hasattr(value, "currency"):
        currency = value.currency
        # Currency might be a Currency object or string
        if hasattr(currency, "code"):
            return currency.code
        return str(currency)

    # Handle list/tuple from MultiWidget (bound form data)
    if isinstance(value, (list, tuple)) and len(value) >= 2:
        return value[1] if value[1] not in (None, "") else ""

    # Handle string currency code directly
    if isinstance(value, str) and len(value) == 3:
        return value

    return ""


@register.simple_tag
def call_admin_method(admin_instance, method_name, obj):
    """
    Call an admin method (readonly field) and return its result

    Usage in template:
        {% call_admin_method inline_admin_form method_name inline_admin_form.original %}

    Args:
        admin_instance: The admin or inline admin instance
        method_name: Name of the method to call (e.g., 'stock_summary')
        obj: The object instance to pass to the method

    Returns:
        The result of calling the admin method
    """
    if not obj:
        return ""

    # Get the model admin from inline admin form
    if hasattr(admin_instance, "model_admin"):
        model_admin = admin_instance.model_admin
    else:
        model_admin = admin_instance

    # Get the method from the admin class
    if hasattr(model_admin, method_name):
        method = getattr(model_admin, method_name)
        if callable(method):
            return method(obj)

    return ""


@register.simple_tag
def get_readonly_field_label(admin_instance, method_name):
    """
    Get the label (short_description) for a readonly field

    Usage in template:
        {% get_readonly_field_label inline_admin_form 'stock_summary' %}

    Args:
        admin_instance: The admin or inline admin instance
        method_name: Name of the method

    Returns:
        The short_description or method name as fallback
    """
    # Get the model admin from inline admin form
    if hasattr(admin_instance, "model_admin"):
        model_admin = admin_instance.model_admin
    else:
        model_admin = admin_instance

    # Get the method from the admin class
    if hasattr(model_admin, method_name):
        method = getattr(model_admin, method_name)
        if hasattr(method, "short_description"):
            return method.short_description

    # Fallback: convert method_name to human-readable
    return method_name.replace("_", " ").title()
