"""
Merchant Translation template tags.

Provides {% mtrans %} which checks merchant UI translation overrides
before falling back to Django's standard {% trans %} behaviour.

Usage:
    {% load merchant_trans %}
    {% mtrans 'Shopping Cart' %}
    {% mtrans 'Shopping Cart' as cart_title %}
"""
import logging
from django import template
from django.conf import settings
from django.utils.translation import get_language, gettext
from django.core.cache import cache

logger = logging.getLogger(__name__)
register = template.Library()

# Built-in languages that have .po file translations.
# Derived from settings.LANGUAGES so it stays in sync automatically.
BUILTIN_LANGUAGES = frozenset(code for code, _name in settings.LANGUAGES)


def _get_ui_overrides(language_code):
    """
    Get all UI translation overrides for a language.
    Returns a dict of {english_string: translated_string}.
    Cached for 5 minutes.
    """
    cache_key = f'ui_trans_overrides:{language_code}'
    overrides = cache.get(cache_key)

    if overrides is not None:
        return overrides  # Could be empty dict (valid cache)

    try:
        from translations.models import SiteLanguage, UITranslationOverride
        from translations.ui_string_registry import UI_STRING_REGISTRY

        site_lang = SiteLanguage.objects.filter(
            code=language_code, is_active=True
        ).first()

        if not site_lang:
            cache.set(cache_key, {}, 300)
            return {}

        try:
            override_obj = UITranslationOverride.objects.get(language=site_lang)
            # Build lookup: English source -> translated text
            overrides_by_english = {}
            for string_key, translated_text in override_obj.overrides.items():
                if string_key in UI_STRING_REGISTRY and translated_text:
                    english_source = UI_STRING_REGISTRY[string_key]
                    overrides_by_english[english_source] = translated_text

            cache.set(cache_key, overrides_by_english, 300)
            return overrides_by_english
        except UITranslationOverride.DoesNotExist:
            cache.set(cache_key, {}, 300)
            return {}
    except Exception as e:
        logger.error(f"Error loading UI overrides for {language_code}: {e}")
        return {}


class MerchantTransNode(template.Node):
    """Template node for {% mtrans %} tag."""

    def __init__(self, message_string, asvar=None):
        self.message_string = message_string
        self.asvar = asvar

    def render(self, context):
        source_string = self.message_string
        language_code = get_language() or 'en'

        # Check merchant overrides (works for all languages including built-in)
        overrides = _get_ui_overrides(language_code)
        if source_string in overrides:
            result = overrides[source_string]
        elif language_code in BUILTIN_LANGUAGES:
            # Built-in language without override: use Django's .po translation
            result = gettext(source_string)
        else:
            # Non-built-in language without override: return English source
            result = source_string

        if self.asvar:
            context[self.asvar] = result
            return ''
        return result


@register.tag('mtrans')
def do_mtrans(parser, token):
    """
    Merchant-aware translation tag.

    For built-in languages (those in settings.LANGUAGES with .po files):
    checks overrides first, then falls back to Django's standard gettext
    (.po file translation).

    For merchant-added languages not in settings.LANGUAGES: checks overrides,
    falls back to English source string.

    Usage:
        {% mtrans 'Shopping Cart' %}
        {% mtrans 'Shopping Cart' as cart_title %}
    """
    bits = token.split_contents()
    if len(bits) < 2:
        raise template.TemplateSyntaxError(
            "'%s' tag requires at least one argument" % bits[0]
        )

    # Extract the string (remove quotes and unescape)
    message_string = bits[1]
    if len(message_string) >= 2 and message_string[0] in ('"', "'") and message_string[-1] == message_string[0]:
        quote_char = message_string[0]
        message_string = message_string[1:-1]
        # Unescape escaped quotes (e.g. we\'ll -> we'll)
        message_string = message_string.replace('\\' + quote_char, quote_char)

    asvar = None
    if len(bits) >= 4 and bits[2] == 'as':
        asvar = bits[3]

    return MerchantTransNode(message_string, asvar=asvar)
