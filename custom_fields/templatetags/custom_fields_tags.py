"""
Template tags for rendering custom fields on the storefront.

Usage:
    {% load custom_fields_tags %}

    {# Render all storefront-visible custom fields for an object #}
    {% render_custom_fields product %}

    {# Get a specific custom field value #}
    {% get_custom_field product "warehouse_location" as location %}
    {{ location }}
"""
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.inclusion_tag('custom_fields/storefront/field_list.html', takes_context=True)
def render_custom_fields(context, obj):
    """
    Render all storefront-visible custom fields for an object.

    Only shows fields where both the group and the field have
    show_on_storefront=True, and where the value is non-empty.
    """
    if not hasattr(obj, 'get_custom_fields_display'):
        return {'groups': []}

    groups = obj.get_custom_fields_display(storefront_only=True)
    return {'groups': groups, 'object': obj}


@register.simple_tag
def get_custom_field(obj, slug, default=''):
    """
    Get a single custom field value from an object.

    Usage: {% get_custom_field product "color_code" as color %}
    """
    if hasattr(obj, 'get_custom_field_value'):
        value = obj.get_custom_field_value(slug, default=default)
        return value if value is not None else default
    return default
