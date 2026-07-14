"""
Signal handlers for translations app.

Handles:
- Cache invalidation when UITranslationOverride is saved
- Dynamic LANGUAGES extension when SiteLanguage is activated
- Auto-translation trigger when a new language is enabled
"""

import hashlib
import logging

from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.urls import clear_url_caches

logger = logging.getLogger(__name__)


def calculate_checksum(text: str) -> str:
    """Calculate MD5 checksum of text"""
    return hashlib.md5(text.encode("utf-8")).hexdigest()


@receiver(post_save, sender="translations.UITranslationOverride")
def invalidate_ui_translation_cache(sender, instance, **kwargs):
    """Clear cached UI overrides when translations are saved."""
    cache_key = f"ui_trans_overrides:{instance.language.code}"
    cache.delete(cache_key)
    logger.debug(f"Invalidated UI translation cache for {instance.language.code}")


@receiver(post_delete, sender="translations.UITranslationOverride")
def invalidate_ui_translation_cache_on_delete(sender, instance, **kwargs):
    """Clear cached UI overrides when translations are deleted."""
    cache_key = f"ui_trans_overrides:{instance.language.code}"
    cache.delete(cache_key)


@receiver(post_save, sender="translations.SiteLanguage")
def handle_site_language_change(sender, instance, created, **kwargs):
    """
    When a SiteLanguage is saved:
    1. Extend settings.LANGUAGES if this is a new active language
    2. Clear URL resolver caches so i18n_patterns picks up new prefixes
    3. Trigger auto-translation of UI strings if newly activated
    """
    if instance.is_active:
        # Extend LANGUAGES if not already present
        existing_codes = {code for code, _ in settings.LANGUAGES}
        if instance.code not in existing_codes:
            settings.LANGUAGES.append((instance.code, instance.name))
            # Clear URL resolver caches so i18n_patterns picks up new prefix
            try:
                clear_url_caches()
            except Exception as e:
                logger.warning(f"Failed to clear URL caches: {e}")
            logger.info(f"Added language {instance.code} to settings.LANGUAGES")

        # Trigger auto-translation for newly activated languages
        try:
            from translations.tasks import auto_translate_ui_strings

            auto_translate_ui_strings.delay(instance.id)
        except Exception as e:
            logger.warning(f"Failed to queue auto-translate for {instance.code}: {e}")

        # Sync registry to ensure all override rows have correct totals
        try:
            from translations.tasks import sync_ui_string_registry_task

            sync_ui_string_registry_task.delay()
        except Exception as e:
            logger.warning(f"Failed to queue UI string registry sync: {e}")

    # Invalidate any cached UI overrides for this language
    cache_key = f"ui_trans_overrides:{instance.code}"
    cache.delete(cache_key)
