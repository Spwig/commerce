"""
SEO Generator Signals

Auto-generates SEO content (meta_title, meta_description) on model save
when the model has seo_auto_generated=True.

Uses QuerySet.update() to save generated fields, avoiding infinite recursion
from post_save triggering another save.
"""

import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


def _auto_generate_seo(sender, instance, **kwargs):
    """
    Auto-generate SEO for a model instance after save.

    Only runs if:
    - instance has seo_auto_generated field set to True
    - update_fields is not limited to SEO-only fields (recursion guard)
    - The model has meta_title and meta_description fields
    """
    # Skip if update_fields contains only SEO fields (our own update)
    update_fields = kwargs.get('update_fields')
    seo_only_fields = {'meta_title', 'meta_description'}
    if update_fields and set(update_fields) <= seo_only_fields:
        return

    # Check if auto-generation is enabled
    if not getattr(instance, 'seo_auto_generated', False):
        return

    # Check if model has SEO fields
    if not hasattr(instance, 'meta_title') or not hasattr(instance, 'meta_description'):
        return

    # Skip if SEO fields already have content (only generate for empty fields)
    if instance.meta_title and instance.meta_description:
        return

    try:
        from seo_generator.providers.registry import ProviderRegistry
        from seo_generator.api.endpoints import extract_content_from_object, MODEL_MAP

        # Determine model_type from sender
        model_type = None
        for key, (app_label, model_name) in MODEL_MAP.items():
            if sender._meta.app_label == app_label and sender._meta.model_name.lower() == model_name.lower():
                model_type = key
                break

        if not model_type:
            return

        # Get primary provider (falls back to deterministic if none configured)
        try:
            provider = ProviderRegistry.get_primary_provider_instance()
        except Exception:
            return

        # Extract content and generate SEO
        content = extract_content_from_object(instance, model_type)
        result = provider.generate_seo(content)

        # Use QuerySet.update() to avoid triggering post_save again
        type(instance).objects.filter(pk=instance.pk).update(
            meta_title=result['meta_title'],
            meta_description=result['meta_description']
        )

        # Invalidate coverage cache
        from seo_generator.services.coverage_service import invalidate_seo_coverage_cache
        invalidate_seo_coverage_cache()

        logger.info(
            "Auto-generated SEO for %s %s: %s",
            model_type, instance.pk, result['meta_title']
        )

    except Exception as e:
        logger.warning(
            "Auto SEO generation failed for %s %s: %s",
            sender._meta.label, instance.pk, e
        )


def connect_signals():
    """Connect post_save signals for all models that support SEO auto-generation."""
    from seo_generator.api.endpoints import MODEL_MAP
    from django.apps import apps

    for model_type, (app_label, model_name) in MODEL_MAP.items():
        try:
            model_class = apps.get_model(app_label, model_name)
            if hasattr(model_class, 'seo_auto_generated'):
                post_save.connect(
                    _auto_generate_seo,
                    sender=model_class,
                    dispatch_uid=f'seo_auto_generate_{app_label}_{model_name}'
                )
                logger.debug("Connected SEO auto-generation signal for %s.%s", app_label, model_name)
        except LookupError:
            logger.debug("Model %s.%s not found, skipping SEO signal", app_label, model_name)


# Connect signals when module is imported (from apps.py ready())
connect_signals()
