"""Template filters for search app."""
from django import template

register = template.Library()


@register.filter
def getattr_filter(obj, attr):
    """Get an attribute from an object dynamically.

    Usage: {{ form|getattr:"field_name" }}
    """
    if hasattr(obj, attr):
        return getattr(obj, attr)
    # For form objects, try to get the field via __getitem__
    if hasattr(obj, '__getitem__'):
        try:
            return obj[attr]
        except (KeyError, TypeError):
            pass
    return None


# Register as both 'getattr_filter' and 'getattr' for convenience
register.filter('getattr', getattr_filter)


@register.filter
def attr(obj, attr_name):
    """Get an attribute from an object.

    Usage: {{ field|attr:"label" }}
    """
    if obj is None:
        return None
    if hasattr(obj, attr_name):
        result = getattr(obj, attr_name)
        # If it's callable (like a method or bound method), call it
        if callable(result):
            try:
                return result()
            except TypeError:
                # If calling fails, return the result as-is
                return result
        return result
    return None


@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary by key.

    Usage: {{ my_dict|get_item:"key_name" }}
    """
    if dictionary is None:
        return None
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None
