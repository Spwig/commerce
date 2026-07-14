"""
Template tags for handling element translations in page builder
"""

import json

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import get_language

from page_builder.translation_utils import (
    get_available_languages,
    get_primary_language,
)
from page_builder.translation_utils import (
    get_language_name as get_lang_name,
)

register = template.Library()


@register.simple_tag(takes_context=True)
def get_translated_field(context, element, field_name, language=None):
    """
    Get translated field value with intelligent fallback.

    Usage:
        {% get_translated_field element 'text' as translated_text %}
        {% get_translated_field element 'text' 'es' as spanish_text %}
    """
    # Use request language if not specified
    if not language:
        request = context.get("request")
        if request and hasattr(request, "visitor_language"):
            language = request.visitor_language
        else:
            language = get_language()

    # Get element content
    content = element.content if hasattr(element, "content") else element

    # Check for translation
    translations = content.get("_translations", {})
    translation_meta = content.get("_translation_meta", {})
    primary_lang = translation_meta.get("primary_lang", get_primary_language())

    # Return primary language content if requested
    if language == primary_lang:
        return content.get(field_name, "")

    # Check for exact language match
    if language in translations and field_name in translations[language]:
        return translations[language][field_name]

    # Try language family fallback (es-MX -> es)
    if "-" in language:
        lang_family = language.split("-")[0]
        if lang_family in translations and field_name in translations[lang_family]:
            return translations[lang_family][field_name]

    # Return primary content as fallback
    return content.get(field_name, "")


@register.filter
def is_translated(element, language=None):
    """
    Check if element has translation for the specified language.

    Usage:
        {% if element|is_translated:'es' %}
        {% if element|is_translated %}
    """
    if not language:
        language = get_language()

    content = element.content if hasattr(element, "content") else element

    translations = content.get("_translations", {})
    return language in translations


@register.simple_tag(takes_context=True)
def get_translation_status(context, element):
    """
    Get translation status for an element.
    Returns dict with translation availability and fallback info.
    """
    request = context.get("request")
    visitor_lang = getattr(request, "visitor_language", get_language())

    content = element.content if hasattr(element, "content") else element

    translations = content.get("_translations", {})
    translation_meta = content.get("_translation_meta", {})
    primary_lang = translation_meta.get("primary_lang", settings.LANGUAGE_CODE)
    available_langs = translation_meta.get("available", [])

    status = {
        "requested_language": visitor_lang,
        "rendered_language": None,
        "is_primary": False,
        "is_translated": False,
        "is_fallback": False,
        "available_languages": available_langs,
    }

    # Check if using primary language
    if visitor_lang == primary_lang:
        status["rendered_language"] = primary_lang
        status["is_primary"] = True
        return status

    # Check for exact translation
    if visitor_lang in translations:
        status["rendered_language"] = visitor_lang
        status["is_translated"] = True
        return status

    # Check for language family fallback
    if "-" in visitor_lang:
        lang_family = visitor_lang.split("-")[0]
        if lang_family in translations:
            status["rendered_language"] = lang_family
            status["is_translated"] = True
            status["is_fallback"] = True
            return status

    # Using primary as fallback
    status["rendered_language"] = primary_lang
    status["is_fallback"] = True

    return status


@register.inclusion_tag("page_builder/partials/translation_indicator.html")
def translation_indicator(element, show_always=False):
    """
    Show a translation status indicator.

    Usage:
        {% translation_indicator element %}
        {% translation_indicator element show_always=True %}
    """
    content = element.content if hasattr(element, "content") else element

    translation_meta = content.get("_translation_meta", {})

    # Get actual count from translation service
    available_langs = get_available_languages()
    primary_lang = get_primary_language()
    # Exclude primary language from total count
    total_target_languages = len([lang for lang in available_langs if lang[0] != primary_lang])

    return {
        "available_count": len(translation_meta.get("available", [])),
        "total_languages": total_target_languages,
        "show_always": show_always,
    }


@register.filter
def json_script(value):
    """
    Safely output JSON for use in script tags.
    """
    try:
        return json.dumps(value)
    except (TypeError, ValueError):
        return "{}"


@register.simple_tag
def get_language_name(language_code):
    """
    Get the display name for a language code from translation service.
    """
    return get_lang_name(language_code)


@register.simple_tag
def page_builder_languages_json():
    """
    Get available languages as JSON for JavaScript.
    Used to populate PAGE_BUILDER_LANGUAGES global variable.
    """
    languages = []
    for code, name in get_available_languages():
        # Convert translation proxy to string for JSON serialization
        languages.append({"code": code, "name": str(name)})

    return mark_safe(json.dumps(languages))


@register.simple_tag(takes_context=True)
def should_lazy_load_translation(context, element):
    """
    Determine if translation should be lazy loaded.
    Used for performance optimization.
    """
    request = context.get("request")
    visitor_lang = getattr(request, "visitor_language", get_language())

    content = element.content if hasattr(element, "content") else element

    # Don't lazy load if already has the right translation
    translations = content.get("_translations", {})
    if visitor_lang in translations:
        return False

    # Large content (>500 chars) is worth lazy loading
    text_content = content.get("text", "")
    return len(text_content) > 500
