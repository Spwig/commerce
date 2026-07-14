"""
Translation utilities for page builder
"""

import json
import logging

from django.conf import settings
from django.core.cache import cache
from django.utils import timezone

logger = logging.getLogger(__name__)


def get_available_languages():
    """
    Get available languages from the translation service.
    Returns list of tuples: [(code, name), ...]
    Caches the result for performance.
    """
    # Try cache first
    cached_langs = cache.get("translation_service_languages")
    if cached_langs:
        return cached_langs

    try:
        from translations.models import SiteLanguage

        languages = []
        # Only return languages marked as active in the translations app
        for lang in SiteLanguage.objects.filter(is_active=True).order_by("order", "name"):
            languages.append((lang.code, lang.name))

        # Cache for 1 hour
        cache.set("translation_service_languages", languages, 3600)
        return languages  # No fallback - if no active languages, return empty

    except ImportError:
        # Translations app not installed - no fallback
        return []
    except Exception:
        # Database not ready or translation service not working - no fallback
        return []


def get_language_choices():
    """
    Get language choices formatted for form fields.
    Returns list of tuples suitable for Django choice fields.
    """
    return get_available_languages()


def get_language_dict():
    """
    Get languages as a dictionary.
    Returns: {code: name, ...}
    """
    return dict(get_available_languages())


def get_primary_language():
    """
    Get the site's primary language.
    This should be the default source language for translations.
    """
    try:
        from translations.models import SiteLanguage

        primary = SiteLanguage.objects.filter(is_active=True, is_default=True).first()

        if primary:
            return primary.code

    except (ImportError, Exception):
        pass

    # Fallback to settings or default
    lang_code = getattr(settings, "LANGUAGE_CODE", "en")

    # Normalize language code for translator (en-us -> en)
    # The translator expects simple language codes like 'en', 'es', 'fr'
    if "-" in lang_code:
        lang_code = lang_code.split("-")[0]

    return lang_code


def get_language_name(code):
    """
    Get the display name for a language code.
    """
    language_dict = get_language_dict()
    return language_dict.get(code, code.upper())


def is_language_supported(code):
    """
    Check if a language code is supported by the translation service.
    """
    language_dict = get_language_dict()

    # Check exact match
    if code in language_dict:
        return True

    # Check base language (e.g., 'en' for 'en-US')
    if "-" in code:
        base_code = code.split("-")[0]
        return base_code in language_dict

    return False


def get_language_fallback_chain(language_code):
    """
    Get fallback chain for a language.
    For example: es-MX -> es -> en
    """
    chain = []

    # Add the requested language
    chain.append(language_code)

    # Add base language if it's a variant
    if "-" in language_code:
        base_code = language_code.split("-")[0]
        if base_code != language_code:
            chain.append(base_code)

    # Add primary language as final fallback
    primary = get_primary_language()
    if primary not in chain:
        chain.append(primary)

    # Filter to only supported languages
    language_dict = get_language_dict()
    return [lang for lang in chain if lang in language_dict]


def serialize_translations_for_js():
    """
    Serialize available languages for use in JavaScript.
    Returns JSON string.
    """
    languages = []
    for code, name in get_available_languages():
        languages.append({"code": code, "name": name})

    return json.dumps(languages)


def get_translation_coverage(element):
    """
    Calculate translation coverage for an element.
    Returns dict with coverage statistics.
    Now checks the separate translations field, not content field.
    """
    if not hasattr(element, "translations"):
        return {"coverage": 0, "translated": 0, "total": 0}

    # Get translations from the separate field
    translations = element.translations or {}
    available_languages = get_available_languages()

    # Exclude primary language from count
    primary_lang = get_primary_language()
    target_languages = [lang[0] for lang in available_languages if lang[0] != primary_lang]

    translated_count = len([lang for lang in target_languages if lang in translations])
    total_count = len(target_languages)

    coverage = (translated_count / total_count * 100) if total_count > 0 else 0

    return {
        "coverage": round(coverage, 1),
        "translated": translated_count,
        "total": total_count,
        "missing": [lang for lang in target_languages if lang not in translations],
    }


def get_translation_health_status():
    """
    Get translation service health status using the translator API.
    Returns dict with health information.
    """
    cache_key = "translation_service_health"
    cache_timeout = 60  # 1 minute cache

    # Check cache first
    cached_status = cache.get(cache_key)
    if cached_status:
        return cached_status

    try:
        from translations.client import TranslatorClient

        client = TranslatorClient()

        # Get health info from translator service
        health_data = client.get_system_info()

        if health_data:
            status = {
                "available": True,
                "status": health_data.get("status", "unknown"),
                "message": "Translation service is operational",
                "model_loaded": health_data.get("model_loaded", False),
                "cpu_percent": health_data.get("cpu_percent", 0),
                "memory_percent": health_data.get("memory_percent", 0),
                "available_languages": health_data.get("available_languages", []),
                "checked_at": timezone.now().isoformat(),
            }

            # Update message based on status
            if not status["model_loaded"]:
                status["status"] = "degraded"
                status["message"] = "Translation models not loaded"
            elif status["cpu_percent"] > 80 or status["memory_percent"] > 90:
                status["status"] = "degraded"
                status["message"] = (
                    f"High resource usage (CPU: {status['cpu_percent']}%, Memory: {status['memory_percent']}%)"
                )

        else:
            # Service not responding
            status = {
                "available": False,
                "status": "offline",
                "message": "Translation service is not responding",
                "checked_at": timezone.now().isoformat(),
            }

    except Exception as e:
        logger.error(f"Error checking translation service health: {e}")
        status = {
            "available": False,
            "status": "offline",
            "message": "Error connecting to translation service",
            "checked_at": timezone.now().isoformat(),
        }

    # Cache the result
    cache.set(cache_key, status, cache_timeout)
    return status


def should_schedule_translation(char_count: int, language_count: int) -> tuple[bool, str]:
    """
    Determine if translation should be scheduled instead of immediate.
    Based on sentence count rather than just character count.

    Args:
        char_count: Number of characters to translate
        language_count: Number of target languages

    Returns:
        Tuple of (should_schedule: bool, reason: str)
    """
    # Get current health status
    status = get_translation_health_status()

    # Check if service is under heavy load
    if status.get("status") == "degraded":
        cpu = status.get("cpu_percent", 0)
        mem = status.get("memory_percent", 0)

        # Only recommend scheduling if actually under heavy load
        if cpu > 80 or mem > 90:
            return True, f"High server load (CPU: {cpu}%, Memory: {mem}%)"

    # Estimate sentence count (rough approximation)
    # Average sentence is ~15-20 words, ~75-100 characters
    estimated_sentences = max(1, char_count / 75)

    # Calculate work units: sentences × languages
    work_units = estimated_sentences * language_count

    # Threshold: More than 100 work units suggests scheduling
    # This means:
    # - 10 sentences × 10 languages = 100 units (schedule)
    # - 2 sentences × 50 languages = 100 units (schedule)
    # - 1 sentence × 100 languages = 100 units (schedule)
    # - 5 sentences × 20 languages = 100 units (schedule)
    # But:
    # - 1-2 sentences × 10 languages = 10-20 units (immediate)
    # - 10 sentences × 5 languages = 50 units (immediate)

    if work_units > 100:
        return (
            True,
            f"Large translation job (~{int(estimated_sentences)} sentences × {language_count} languages = {int(work_units)} work units)",
        )

    # Otherwise, proceed with immediate translation
    return False, ""


def estimate_translation_time(char_count: int, language_count: int) -> int:
    """
    Estimate translation time in seconds.

    Args:
        char_count: Number of characters
        language_count: Number of languages

    Returns:
        Estimated time in seconds
    """
    # Base estimation: ~1 second per 100 characters per language
    base_time = (char_count / 100) * language_count

    # Check current load and adjust estimate
    status = get_translation_health_status()
    if status.get("status") == "degraded":
        base_time *= 2  # Double time if degraded
    elif status.get("cpu_percent", 0) > 70:
        base_time *= 1.5  # 50% more if high CPU

    return max(5, int(base_time))  # Minimum 5 seconds


class TranslationServiceHealth:
    """Thin wrapper over the module-level health helpers.

    Introduced because several call sites (page_builder middleware,
    translation endpoints, and this module's own TranslationFallbackHandler)
    were instantiating a TranslationServiceHealth() that never existed,
    raising NameError as soon as the code path was hit.
    """

    def get_health_status(self) -> dict:
        """Return the current cached health-status dict."""
        return get_translation_health_status()

    def should_schedule_translation(self, char_count: int, language_count: int) -> tuple[bool, str]:
        return should_schedule_translation(char_count, language_count)

    def estimate_translation_time(self, char_count: int, language_count: int) -> int:
        return estimate_translation_time(char_count, language_count)

    def get_degradation_warnings(self) -> list[str]:
        """Return any active degradation warnings from the current health status."""
        status = get_translation_health_status()
        warnings = []
        if not status.get("available"):
            warnings.append(status.get("message", "Translation service is unavailable"))
        elif status.get("status") == "degraded":
            warnings.append(status.get("message", "Translation service is degraded"))
        return warnings


class TranslationFallbackHandler:
    """
    Handle translation service failures gracefully.
    Provides fallback strategies and error recovery.
    """

    def __init__(self):
        self.context_manager = TranslationContextManager()

    def handle_service_unavailable(
        self, content: str, languages: list[str], element_id: str | None = None
    ) -> dict:
        """
        Handle when service is completely down.

        Returns:
            Dict with fallback response
        """
        # Try to create a translation job for later
        job = None
        if self.context_manager.service_available:
            job = self.context_manager.create_translation_job(
                job_type="page_element",
                status="pending",
                source_language=get_primary_language(),
                target_languages=languages,
                content_snapshot={"text": content, "element_id": element_id},
            )

        return {
            "success": False,
            "error": "service_unavailable",
            "message": "Translation service is currently offline",
            "queued": job is not None,
            "job_id": job.id if job else None,
            "retry_after": 300,  # Suggest retry after 5 minutes
        }

    def handle_service_degraded(self, content: str, languages: list[str]) -> dict:
        """
        Handle when service is slow/limited.

        Returns:
            Dict with degradation handling strategy
        """
        # Suggest scheduling or limiting batch size
        health = TranslationServiceHealth()
        should_schedule, reason = health.should_schedule_translation(len(content), len(languages))

        return {
            "success": True,
            "warning": "service_degraded",
            "message": reason,
            "suggest_schedule": should_schedule,
            "max_batch_size": 3,  # Limit concurrent translations
            "estimated_time": health.estimate_translation_time(len(content), len(languages)),
        }

    def handle_partial_failure(
        self, succeeded: dict[str, str], failed: list[str], reason: str
    ) -> dict:
        """
        Handle when some languages fail to translate.

        Args:
            succeeded: Dict of successful translations {lang: text}
            failed: List of failed language codes
            reason: Failure reason

        Returns:
            Dict with partial success information
        """
        return {
            "success": "partial",
            "message": f"Translated {len(succeeded)} of {len(succeeded) + len(failed)} languages",
            "translations": succeeded,
            "failed_languages": failed,
            "failure_reason": reason,
            "retry_failed": True,
        }


class TranslationContextManager:
    """
    Context manager for handling translation service availability.
    Provides safe access to translation models with fallback.
    """

    def __init__(self):
        self.service_available = False
        self.SiteLanguage = None
        self.TranslationJob = None
        self._load_models()

    def _load_models(self):
        """Try to load translation models"""
        try:
            from translations.models import SiteLanguage, TranslationJob

            self.SiteLanguage = SiteLanguage
            self.TranslationJob = TranslationJob
            self.service_available = True
        except ImportError:
            self.service_available = False

    def get_languages(self):
        """Get languages with fallback"""
        if self.service_available and self.SiteLanguage:
            try:
                return [
                    (lang.code, lang.name)
                    for lang in self.SiteLanguage.objects.filter(is_active=True)
                ]
            except Exception:
                pass

        return getattr(settings, "LANGUAGES", [("en", "English")])

    def create_translation_job(self, **kwargs):
        """Create a translation job if service is available"""
        if self.service_available and self.TranslationJob:
            try:
                return self.TranslationJob.objects.create(**kwargs)
            except Exception as e:
                logger.error(f"Failed to create translation job: {e}")

        return None
