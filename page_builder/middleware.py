"""
Page Builder Middleware for language detection and translation handling
"""

import re

from django.conf import settings
from django.core.cache import cache
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin


class LanguageDetectionMiddleware(MiddlewareMixin):
    """
    Detects visitor's preferred language and makes it available throughout the request.
    Detection priority:
    1. URL parameter (?lang=xx)
    2. Session preference
    3. Cookie preference
    4. Accept-Language header
    5. Site default language
    """

    def __init__(self, get_response):
        super().__init__(get_response)
        self.available_languages = None
        self.language_codes = None
        self._refresh_languages()

    def _get_available_languages(self):
        """Get available languages from translation service"""
        # Try to get from cache first
        cached_langs = cache.get("translation_service_languages")
        if cached_langs:
            return cached_langs

        try:
            from translations.models import SiteLanguage

            # Get all active languages from translation service
            languages = []
            for lang in SiteLanguage.objects.filter(is_active=True).order_by(
                "display_order", "name"
            ):
                languages.append((lang.code, lang.name))

            # Cache for 1 hour
            cache.set("translation_service_languages", languages, 3600)
            return languages if languages else [("en", "English")]

        except ImportError:
            # Fallback if translations app not installed
            return getattr(settings, "LANGUAGES", [("en", "English")])
        except Exception as e:
            # Fallback on any other error (DB not ready, etc.)
            print(f"Warning: Could not load languages from translation service: {e}")
            return getattr(settings, "LANGUAGES", [("en", "English")])

    def _refresh_languages(self):
        """Refresh the available languages list"""
        self.available_languages = self._get_available_languages()
        self.language_codes = {lang[0] for lang in self.available_languages}

    def _parse_accept_language(self, accept_language_header):
        """
        Parse the Accept-Language header and return languages sorted by preference
        Example: "en-US,en;q=0.9,es;q=0.8" -> ['en-US', 'en', 'es']
        """
        if not accept_language_header:
            return []

        languages = []
        for item in accept_language_header.split(","):
            parts = item.strip().split(";")
            lang = parts[0].strip()

            # Parse quality value if present
            quality = 1.0
            if len(parts) > 1:
                quality_match = re.match(r"q=([0-9.]+)", parts[1].strip())
                if quality_match:
                    quality = float(quality_match.group(1))

            languages.append((lang, quality))

        # Sort by quality (descending)
        languages.sort(key=lambda x: x[1], reverse=True)
        return [lang[0] for lang in languages]

    def _normalize_language_code(self, lang_code):
        """
        Normalize language codes to match our available languages
        Examples: 'en-US' -> 'en', 'zh-CN' -> 'zh'
        """
        if not lang_code:
            return None

        # Direct match
        if lang_code in self.language_codes:
            return lang_code

        # Try the base language (before hyphen)
        if "-" in lang_code:
            base_lang = lang_code.split("-")[0]
            if base_lang in self.language_codes:
                return base_lang

        return None

    def get_visitor_language(self, request):
        """
        Detect visitor's preferred language with fallback chain
        """
        # 1. Check URL parameter (highest priority for explicit selection)
        url_lang = request.GET.get("lang")
        if url_lang:
            normalized = self._normalize_language_code(url_lang)
            if normalized:
                # Save preference for future visits
                request.session["preferred_language"] = normalized
                return normalized

        # 2. Check session preference
        session_lang = request.session.get("preferred_language")
        if session_lang and session_lang in self.language_codes:
            return session_lang

        # 3. Check cookie preference
        cookie_lang = request.COOKIES.get("django_language")
        if cookie_lang:
            normalized = self._normalize_language_code(cookie_lang)
            if normalized:
                return normalized

        # 4. Parse Accept-Language header
        accept_language = request.META.get("HTTP_ACCEPT_LANGUAGE", "")
        if accept_language:
            parsed_languages = self._parse_accept_language(accept_language)
            for lang in parsed_languages:
                normalized = self._normalize_language_code(lang)
                if normalized:
                    return normalized

        # 5. Fall back to site default
        return settings.LANGUAGE_CODE

    def process_request(self, request):
        """
        Process the request to detect and set the visitor's language
        """
        # Detect language
        visitor_language = self.get_visitor_language(request)

        # Store in request for easy access
        request.visitor_language = visitor_language
        request.available_languages = self.available_languages
        request.language_codes = self.language_codes

        # Add translation service status (non-blocking)
        self._add_translation_service_status(request)

        # Activate the language for Django's translation system
        translation.activate(visitor_language)
        request.LANGUAGE_CODE = visitor_language

        return None

    def _add_translation_service_status(self, request):
        """
        Add translation service health status to request.
        This is done in a non-blocking way using cached data.
        """
        try:
            from page_builder.translation_utils import TranslationServiceHealth

            health = TranslationServiceHealth()
            # This uses cached data, so it's fast
            status = health.get_health_status()

            request.translation_service_available = status["available"]
            request.translation_service_status = status["status"]
            request.translation_service_message = status.get("message", "")

        except Exception as e:
            # Don't let health check failures break the request
            request.translation_service_available = False
            request.translation_service_status = "unknown"
            request.translation_service_message = str(e)

    def process_response(self, request, response):
        """
        Ensure the language cookie is set for future visits
        """
        if hasattr(request, "visitor_language"):
            response.set_cookie(
                "django_language",
                request.visitor_language,
                max_age=365 * 24 * 60 * 60,  # 1 year
                httponly=True,
                samesite="Lax",
            )

        return response


class TranslationCacheMiddleware(MiddlewareMixin):
    """
    Middleware to handle translation caching headers
    """

    def process_response(self, request, response):
        """
        Add cache headers based on language
        """
        if hasattr(request, "visitor_language"):
            # Add Vary header for proper caching
            response["Vary"] = "Accept-Language, Cookie"

            # Add language to cache key
            if hasattr(response, "cache_control"):
                response.cache_control.private = True

        return response
