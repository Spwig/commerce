"""Template helpers used by the voucher admin (import wizard, list view)."""

from django import template

register = template.Library()


@register.filter
def get_item(value, key):
    """Look up a key on a dict-like (or a positional index on a sequence).

    Returns an empty string when the key is missing, so dict-of-row
    rendering in the import-preview template stays robust against
    ragged source rows.
    """
    if value is None:
        return ""
    try:
        return value.get(key, "") if hasattr(value, "get") else value[key]
    except (KeyError, IndexError, TypeError):
        return ""
