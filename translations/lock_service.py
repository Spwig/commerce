"""
Translation lock service.

Centralized helpers for checking and toggling translation locks.
Used by all translation code paths to enforce lock protection.

Model-field locks use TranslationMeta records.
UI string locks use the meta_info JSONField on UITranslationOverride.

"""
from django.utils import timezone


def get_locked_fields(content_type, object_ids, language):
    """
    Return set of (object_id, field_name) tuples that are locked.

    Used by bulk translation paths to skip locked fields efficiently.
    """
    from .models import TranslationMeta

    if not object_ids:
        return set()

    locked = TranslationMeta.objects.filter(
        content_type=content_type,
        object_id__in=object_ids,
        language=language,
        is_locked=True,
    ).values_list('object_id', 'field_name')
    return set(locked)


def is_field_locked(content_type, object_id, field_name, language):
    """Check if a specific field translation is locked."""
    from .models import TranslationMeta

    return TranslationMeta.objects.filter(
        content_type=content_type,
        object_id=object_id,
        field_name=field_name,
        language=language,
        is_locked=True,
    ).exists()


def toggle_field_lock(content_type, object_id, field_name, language, user):
    """
    Toggle lock state for a model-field translation.

    Creates TranslationMeta record if it doesn't exist.
    Returns new is_locked value.
    """
    from .models import TranslationMeta

    meta, created = TranslationMeta.objects.get_or_create(
        content_type=content_type,
        object_id=int(object_id),
        field_name=field_name,
        language=language,
    )
    meta.is_locked = not meta.is_locked
    meta.locked_by = user if meta.is_locked else None
    meta.locked_at = timezone.now() if meta.is_locked else None
    meta.save(update_fields=['is_locked', 'locked_by', 'locked_at'])
    return meta.is_locked


def get_locked_fields_for_status(content_type, object_id):
    """
    Return dict {language: [field_names]} of locked fields for an object.

    Used by the status API to communicate lock state to the frontend.
    """
    from .models import TranslationMeta

    locked = TranslationMeta.objects.filter(
        content_type=content_type,
        object_id=int(object_id),
        is_locked=True,
    ).values_list('language', 'field_name')

    result = {}
    for lang, field in locked:
        result.setdefault(lang, []).append(field)
    return result


def get_ui_locked_keys(language_code):
    """Return set of locked UI string keys for a language."""
    from .models import UITranslationOverride

    try:
        override = UITranslationOverride.objects.select_related('language').get(
            language__code=language_code
        )
    except UITranslationOverride.DoesNotExist:
        return set()

    meta = override.meta_info or {}
    return {k for k, v in meta.items() if isinstance(v, dict) and v.get('locked')}
