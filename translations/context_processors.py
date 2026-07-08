"""
Context processors for merchant UI translations.

Provides JavaScript-accessible UI translations for the current language.
"""
import json
import logging
from django.utils.translation import get_language, gettext

logger = logging.getLogger(__name__)


def js_ui_translations(request):
    """
    Provide JS-accessible UI translations for the current language.

    Only includes 'js.*' keys from the registry to keep payload small.
    Available in templates as {{ js_ui_translations }}.

    Fallback chain mirrors the {% mtrans %} template tag:
    1. Merchant override (from UITranslationOverride)
    2. .po translation (for built-in languages)
    3. English source string
    """
    from translations.templatetags.merchant_trans import (
        _get_ui_overrides, BUILTIN_LANGUAGES,
    )
    from translations.ui_string_registry import UI_STRING_REGISTRY

    language_code = get_language() or 'en'
    is_builtin = language_code in BUILTIN_LANGUAGES

    # Only include js.* strings to keep payload small
    js_strings = {k: v for k, v in UI_STRING_REGISTRY.items() if k.startswith('js.')}
    overrides = _get_ui_overrides(language_code)

    translated = {}
    for key, english in js_strings.items():
        override = overrides.get(english)
        if override:
            translated[key] = override
        elif is_builtin and language_code != 'en':
            po_val = gettext(english)
            translated[key] = po_val if po_val else english
        else:
            translated[key] = english

    return {'js_ui_translations': json.dumps(translated, ensure_ascii=False)}
