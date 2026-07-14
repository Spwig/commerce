"""
Template Tags and Filters for Language Display

Provides template filters for displaying language information in the language switcher.

Usage in templates:
    {% load language_tags %}

    {{ 'en'|language_flag }}
    {{ 'en'|language_native_name }}
    {{ 'ar'|language_dir }}
    {% with lang_info='en'|language_info %}
        {{ lang_info.flag }} {{ lang_info.native_name }}
    {% endwith %}
"""

from django import template

from core.language_metadata import get_language_info

register = template.Library()


@register.filter
def language_flag(code):
    """
    Return flag emoji for a language code.

    Args:
        code (str): Language code (e.g., 'en', 'es', 'zh-hans')

    Returns:
        str: Flag emoji for the language

    Example:
        {{ 'en'|language_flag }}  -> 🇺🇸
        {{ 'ja'|language_flag }}  -> 🇯🇵
    """
    return get_language_info(code)["flag"]


@register.filter
def language_native_name(code):
    """
    Return native name for a language code.

    Args:
        code (str): Language code (e.g., 'en', 'es', 'zh-hans')

    Returns:
        str: Native name of the language in its own script

    Example:
        {{ 'en'|language_native_name }}  -> English
        {{ 'ar'|language_native_name }}  -> العربية
    """
    return get_language_info(code)["native_name"]


@register.filter
def language_dir(code):
    """
    Return text direction (ltr/rtl) for a language code.

    Args:
        code (str): Language code (e.g., 'en', 'es', 'ar')

    Returns:
        str: Text direction - 'ltr' (left-to-right) or 'rtl' (right-to-left)

    Example:
        {{ 'en'|language_dir }}  -> ltr
        {{ 'ar'|language_dir }}  -> rtl
    """
    return get_language_info(code)["dir"]


@register.filter
def language_info(code):
    """
    Return complete metadata dict for a language code.

    Args:
        code (str): Language code (e.g., 'en', 'es', 'zh-hans')

    Returns:
        dict: Dictionary containing 'flag', 'native_name', and 'dir' keys

    Example:
        {% with info='en'|language_info %}
            {{ info.flag }} {{ info.native_name }} ({{ info.dir }})
        {% endwith %}
    """
    return get_language_info(code)
