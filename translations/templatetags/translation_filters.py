from django import template
from django.core.cache import cache

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary"""
    if dictionary:
        return dictionary.get(key)
    return None


@register.simple_tag
def get_site_languages():
    """
    Get active site languages configured by the merchant for the frontend.
    Returns a list of SiteLanguage objects where is_active=True.
    Usage: {% get_site_languages as site_languages %}
    """
    cache_key = 'active_site_languages'
    languages = cache.get(cache_key)

    if languages is None:
        try:
            from translations.models import SiteLanguage
            languages = list(
                SiteLanguage.objects.filter(is_active=True).order_by('order', 'name')
            )
            cache.set(cache_key, languages, 300)
        except Exception:
            languages = []

    return languages


@register.simple_tag
def has_site_languages():
    """
    Check if merchant has configured multiple active site languages.
    Usage: {% has_site_languages as show_language_selector %}
    """
    languages = get_site_languages()
    return len(languages) > 1