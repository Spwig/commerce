"""
Language metadata for the language switcher component.

This module provides centralized metadata for all supported languages including:
- Flag emoji representation
- Native language name (in the language's own script)
- Text direction (ltr or rtl)

Used by template filters in core.templatetags.language_tags to display
language information in the language switcher dropdown.
"""

from django.core.cache import cache

SITE_LANGUAGE_METADATA_CACHE_KEY = "site_language_metadata"
SITE_LANGUAGE_METADATA_CACHE_TTL = 300

LANGUAGE_METADATA = {
    "en": {"flag": "🇺🇸", "native_name": "English", "dir": "ltr"},
    "es": {"flag": "🇪🇸", "native_name": "Español", "dir": "ltr"},
    "fr": {"flag": "🇫🇷", "native_name": "Français", "dir": "ltr"},
    "de": {"flag": "🇩🇪", "native_name": "Deutsch", "dir": "ltr"},
    "pt": {"flag": "🇵🇹", "native_name": "Português", "dir": "ltr"},
    "zh-hans": {"flag": "🇨🇳", "native_name": "简体中文", "dir": "ltr"},
    "zh-hant": {"flag": "🇹🇼", "native_name": "繁體中文", "dir": "ltr"},
    "ja": {"flag": "🇯🇵", "native_name": "日本語", "dir": "ltr"},
    "ar": {"flag": "🇸🇦", "native_name": "العربية", "dir": "rtl"},
    "ru": {"flag": "🇷🇺", "native_name": "Русский", "dir": "ltr"},
    "hi": {"flag": "🇮🇳", "native_name": "हिन्दी", "dir": "ltr"},
    "id": {"flag": "🇮🇩", "native_name": "Bahasa Indonesia", "dir": "ltr"},
    "ko": {"flag": "🇰🇷", "native_name": "한국어", "dir": "ltr"},
    "tr": {"flag": "🇹🇷", "native_name": "Türkçe", "dir": "ltr"},
    "vi": {"flag": "🇻🇳", "native_name": "Tiếng Việt", "dir": "ltr"},
    "it": {"flag": "🇮🇹", "native_name": "Italiano", "dir": "ltr"},
    "th": {"flag": "🇹🇭", "native_name": "ไทย", "dir": "ltr"},
}


def _get_site_language_metadata():
    """
    Build a {code: {flag, native_name, dir}} mapping from active SiteLanguage
    records, cached and invalidated by the translations SiteLanguage signals.
    """
    metadata = cache.get(SITE_LANGUAGE_METADATA_CACHE_KEY)
    if metadata is None:
        metadata = {}
        try:
            from translations.models import SiteLanguage

            for lang in SiteLanguage.objects.filter(is_active=True):
                metadata[lang.code] = {
                    "flag": lang.flag or "🌐",
                    "native_name": lang.native_name or lang.code.upper(),
                    "dir": "rtl" if lang.rtl else "ltr",
                }
        except Exception:
            metadata = {}
        cache.set(SITE_LANGUAGE_METADATA_CACHE_KEY, metadata, SITE_LANGUAGE_METADATA_CACHE_TTL)
    return metadata


def get_language_info(code):
    """
    Get metadata for a language code with fallback.

    Args:
        code (str): Language code (e.g., 'en', 'es', 'zh-hans')

    Returns:
        dict: Dictionary containing 'flag', 'native_name', and 'dir' keys.
              Known codes come from LANGUAGE_METADATA; otherwise the merchant's
              active SiteLanguage configuration is consulted before falling back
              to generic values.

    Example:
        >>> get_language_info('en')
        {'flag': '🇺🇸', 'native_name': 'English', 'dir': 'ltr'}

        >>> get_language_info('unknown')
        {'flag': '🌐', 'native_name': 'UNKNOWN', 'dir': 'ltr'}
    """
    if code in LANGUAGE_METADATA:
        return LANGUAGE_METADATA[code]

    site_metadata = _get_site_language_metadata().get(code)
    if site_metadata is not None:
        return site_metadata

    return {"flag": "🌐", "native_name": code.upper() if code else "UNKNOWN", "dir": "ltr"}
