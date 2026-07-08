"""
Generic Translation API endpoints for any model with translations field.

This module provides reusable translation endpoints that work with any Spwig model,
not just specific apps like page_builder. Models must have a JSONField named 'translations'.

"""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.apps import apps
import json
import logging
from typing import Dict, Optional
from datetime import datetime
from design.content_sanitizer import ContentSanitizer
from django_ckeditor_5.fields import CKEditor5Field

logger = logging.getLogger(__name__)

# Initialize sanitizer for admin content (Tier C - most permissive but still secure)
content_sanitizer = ContentSanitizer(tier='C')


def _is_richtext_field(model_class, field_name: str) -> bool:
    """
    Check if a field is a CKEditor rich text field.

    Args:
        model_class: Model class
        field_name: Name of the field to check

    Returns:
        True if field is CKEditor5Field, False otherwise
    """
    try:
        field = model_class._meta.get_field(field_name)
        return isinstance(field, CKEditor5Field)
    except:
        return False


def _sanitize_if_html(content: str, is_html_field: bool) -> str:
    """
    Sanitize content if it's an HTML field.

    Args:
        content: Content to sanitize
        is_html_field: Whether the field contains HTML

    Returns:
        Sanitized content (or original if not HTML field)
    """
    if not content or not is_html_field:
        return content

    try:
        sanitized = content_sanitizer.sanitize_html(content)
        if sanitized != content:
            logger.info(f"HTML content was sanitized (removed potentially dangerous content)")
        return sanitized
    except Exception as e:
        logger.error(f"Error sanitizing HTML: {e}")
        return content  # Return original on error


def _get_model_instance(model_type: str, object_id: int):
    """
    Get a model instance by model type and ID.

    Args:
        model_type: Model identifier in format 'app_label.model_name' (e.g., 'core.sitesettings')
        object_id: Primary key of the object

    Returns:
        Tuple of (instance, error_response)
        If successful: (instance, None)
        If error: (None, JsonResponse)
    """
    try:
        app_label, model_name = model_type.lower().split('.')
        model_class = apps.get_model(app_label, model_name)

        # Verify model has translations field
        if not hasattr(model_class, 'translations'):
            return None, JsonResponse({
                'error': f'Model {model_type} does not have a translations field'
            }, status=400)

        # Get the instance
        try:
            instance = model_class.objects.get(pk=object_id)
            return instance, None
        except model_class.DoesNotExist:
            return None, JsonResponse({
                'error': f'{model_class.__name__} with id {object_id} not found'
            }, status=404)

    except ValueError:
        return None, JsonResponse({
            'error': 'Invalid model_type format. Use "app_label.model_name" (e.g., "core.sitesettings")'
        }, status=400)
    except LookupError:
        return None, JsonResponse({
            'error': f'Model {model_type} not found'
        }, status=404)


def _get_translation_utils():
    """Get translation utility functions from page_builder (reusable)"""
    try:
        from page_builder.translation_utils import (
            get_available_languages,
            get_primary_language,
            get_translation_health_status,
            should_schedule_translation,
            estimate_translation_time
        )
        return {
            'get_available_languages': get_available_languages,
            'get_primary_language': get_primary_language,
            'get_translation_health_status': get_translation_health_status,
            'should_schedule_translation': should_schedule_translation,
            'estimate_translation_time': estimate_translation_time
        }
    except ImportError as e:
        logger.error(f"Failed to import translation utilities: {e}")
        return None


@staff_member_required
@require_http_methods(["GET"])
def generic_translation_status(request, model_type, object_id, field_key):
    """
    Get translation status for a specific field of any model.

    URL pattern: /api/translation/<model_type>/<object_id>/<field_key>/status/
    Example: /api/translation/core.sitesettings/1/site_name/status/

    Returns:
        JSON with translation status:
        - translations: Dict of {lang_code: translated_text}
        - available_languages: List of available target languages
        - primary_language: Primary language code
        - coverage: Translation coverage statistics
    """
    # Get the model instance
    instance, error = _get_model_instance(model_type, object_id)
    if error:
        return error

    # Get translation utilities
    utils = _get_translation_utils()
    if not utils:
        return JsonResponse({
            'error': 'Translation utilities not available'
        }, status=503)

    # Get translations for this specific field
    translations = instance.translations or {}
    field_translations = {}

    # Extract translations for the specific field across all languages
    for lang_code, lang_data in translations.items():
        if isinstance(lang_data, dict) and field_key in lang_data:
            # Skip metadata
            if not field_key.startswith('_'):
                field_translations[lang_code] = lang_data[field_key]

    # Calculate coverage
    available_languages = utils['get_available_languages']()
    primary_language = utils['get_primary_language']()

    # Exclude primary language from target languages
    target_languages = [lang[0] for lang in available_languages if lang[0] != primary_language]
    translated_count = len([lang for lang in target_languages if lang in field_translations])
    total_count = len(target_languages)
    coverage = (translated_count / total_count * 100) if total_count > 0 else 0

    # Get lock status for this object
    from translations.lock_service import get_locked_fields_for_status
    locked_map = get_locked_fields_for_status(model_type, int(object_id))

    return JsonResponse({
        'model_type': model_type,
        'object_id': object_id,
        'field_key': field_key,
        'translations': field_translations,
        'primary_language': primary_language,
        'available_languages': [
            {'code': code, 'name': str(name)}
            for code, name in available_languages
            if code != primary_language  # Don't include primary in targets
        ],
        'coverage': {
            'percentage': round(coverage, 1),
            'translated': translated_count,
            'total': total_count,
            'missing': [lang for lang in target_languages if lang not in field_translations]
        },
        'locked_fields': locked_map,
    })


@staff_member_required
@require_http_methods(["POST"])
@csrf_exempt
def translate_generic_field(request, model_type, object_id, field_key):
    """
    Translate a specific field to target languages using AI translation.
    Integrates with translation queue for heavy workloads.

    URL pattern: /api/translation/<model_type>/<object_id>/<field_key>/translate/
    Example: /api/translation/core.sitesettings/1/site_name/translate/

    POST body:
        {
            "text": "Text to translate",
            "languages": ["es", "fr", "de"],
            "force_immediate": false,
            "schedule": false
        }

    Returns:
        JSON with translation results:
        - success: Boolean
        - translations: Dict of {lang_code: translated_text}
        - successful_languages: List of successful language codes
        - failed_languages: List of failed language codes

        OR scheduling recommendation (202 status):
        - recommend_schedule: true
        - reason: "Explanation"
        - estimated_time: "5-10 minutes"
        - char_count: 1500
        - language_count: 5
    """
    try:
        data = json.loads(request.body)
        text = data.get('text', '').strip()
        target_languages = data.get('languages', [])
        force_immediate = data.get('force_immediate', False)
        schedule = data.get('schedule', False)

        # Validate input
        if not text:
            return JsonResponse({'error': 'Text is required'}, status=400)

        if not target_languages:
            return JsonResponse({'error': 'Target languages are required'}, status=400)

        # Get the model instance
        instance, error = _get_model_instance(model_type, object_id)
        if error:
            return error

        # Get translation utilities
        utils = _get_translation_utils()
        if not utils:
            return JsonResponse({
                'error': 'Translation utilities not available'
            }, status=503)

        # Check translation service health
        health_status = utils['get_translation_health_status']()
        if not health_status.get('available', False):
            return JsonResponse({
                'error': 'Translation service is not available',
                'health': health_status
            }, status=503)

        # Check if we should recommend scheduling (workload detection)
        char_count = len(text)
        should_schedule_flag, reason = utils['should_schedule_translation'](
            char_count,
            len(target_languages)
        )

        # Recommend scheduling if workload is heavy and not forcing immediate
        if should_schedule_flag and not schedule and not force_immediate:
            return JsonResponse({
                'success': False,
                'recommend_schedule': True,
                'reason': reason,
                'estimated_time': utils['estimate_translation_time'](
                    char_count,
                    len(target_languages)
                ),
                'char_count': char_count,
                'language_count': len(target_languages)
            }, status=202)

        # Handle degraded service warnings
        warnings = []
        if health_status.get('status') == 'degraded':
            warnings.append(health_status.get('message', 'Service degraded'))
            if health_status.get('cpu_percent', 0) > 70:
                warnings.append('High CPU usage may result in slower translations')
            if health_status.get('memory_percent', 0) > 80:
                warnings.append('High memory usage may limit batch translation size')

        response_data = {'warnings': warnings} if warnings else {}

        # Handle scheduled translation: create background jobs via Celery
        if schedule:
            try:
                from translations.models import TranslationJob
                from translations.tasks import process_translation_job
                from translations.lock_service import is_field_locked

                primary_language = utils['get_primary_language']()
                job_ids = []
                skipped_locked = []

                for lang in target_languages:
                    if is_field_locked(model_type, int(object_id), field_key, lang):
                        skipped_locked.append(lang)
                        continue

                    job = TranslationJob.objects.create(
                        job_type='custom',
                        status='pending',
                        source_language=primary_language,
                        target_languages=[lang],
                        content_type='generic_field',
                        object_id=int(object_id),
                        fields_to_translate=[field_key],
                        total_characters=len(text),
                        created_by=request.user,
                        translated_data={
                            'model_type': model_type,
                            'object_id': int(object_id),
                            'field_key': field_key,
                            'source_text': text,
                            'language': lang,
                        },
                    )
                    process_translation_job.delay(job.id)
                    job_ids.append(job.id)

                return JsonResponse({
                    'success': True,
                    'scheduled': True,
                    'job_count': len(job_ids),
                    'job_ids': job_ids,
                    'skipped_locked': skipped_locked,
                    'message': f'Scheduled {len(job_ids)} translation job(s) for background processing',
                }, status=202)

            except Exception as e:
                logger.error(f"Failed to schedule translation jobs: {e}")
                return JsonResponse({
                    'error': f'Failed to schedule translations: {str(e)}'
                }, status=500)

        # Perform immediate translation
        try:
            from translations.client import TranslatorClient
            client = TranslatorClient()

            primary_language = utils['get_primary_language']()
            translations = {}
            failed_languages = []

            logger.info(f"Translating {field_key} for {model_type}:{object_id} to {len(target_languages)} languages")

            # Translate to each target language
            from translations.lock_service import is_field_locked
            skipped_languages = []

            for lang in target_languages:
                # Skip locked languages
                if is_field_locked(model_type, int(object_id), field_key, lang):
                    skipped_languages.append(lang)
                    continue

                try:
                    logger.info(f"Translating to {lang}: '{text[:50]}...'")
                    translated = client.translate(
                        text,
                        source_lang=primary_language,
                        target_lang=lang
                    )

                    if translated:
                        translations[lang] = translated
                        logger.info(f"Translation successful for {lang}")
                    else:
                        logger.warning(f"No translation returned for {lang}")
                        failed_languages.append(lang)

                except Exception as e:
                    logger.error(f"Failed to translate to {lang}: {e}")
                    failed_languages.append(lang)

            # Update instance with translations
            if translations:
                if not instance.translations:
                    instance.translations = {}

                # Update translations for each language
                for lang, translated_text in translations.items():
                    if lang not in instance.translations:
                        instance.translations[lang] = {}

                    # Store the translation for this specific field
                    instance.translations[lang][field_key] = translated_text

                    # Add metadata if not present
                    if '_meta' not in instance.translations[lang]:
                        instance.translations[lang]['_meta'] = {}

                    instance.translations[lang]['_meta'].update({
                        'auto': True,
                        'verified': False,
                        'translated_at': datetime.now().isoformat(),
                        'last_field': field_key
                    })

                # Save the instance
                instance.save(update_fields=['translations'])
                logger.info(f"Saved {len(translations)} translations for {model_type}:{object_id}.{field_key}")

                # Clear cache for this instance
                cache_key = f'translations_{model_type}_{object_id}'
                cache.delete(cache_key)

            # Build response
            response_data.update({
                'success': len(translations) > 0,
                'translations': translations,
                'successful_languages': list(translations.keys()),
                'failed_languages': failed_languages,
                'skipped_locked': skipped_languages,
                'total_requested': len(target_languages),
                'message': f"Translated to {len(translations)} of {len(target_languages)} languages"
            })

            return JsonResponse(response_data)

        except ImportError:
            return JsonResponse({
                'error': 'Translation service not configured'
            }, status=503)
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return JsonResponse({
                'error': f'Translation failed: {str(e)}'
            }, status=500)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.error(f"Unexpected error in translate_generic_field: {e}")
        return JsonResponse({'error': 'Internal server error'}, status=500)


@staff_member_required
@require_http_methods(["POST"])
@csrf_exempt
def save_generic_translations(request, model_type, object_id, field_key):
    """
    Save manually edited translations for a specific field.

    URL pattern: /api/translation/<model_type>/<object_id>/<field_key>/save/
    Example: /api/translation/core.sitesettings/1/site_name/save/

    POST body:
        {
            "translations": {
                "es": "Mi Tienda",
                "fr": "Ma Boutique",
                "de": "Mein Geschäft"
            }
        }

    Returns:
        JSON with save status
    """
    try:
        data = json.loads(request.body)
        translations = data.get('translations', {})

        if not translations:
            return JsonResponse({'error': 'Translations are required'}, status=400)

        # Get the model instance
        instance, error = _get_model_instance(model_type, object_id)
        if error:
            return error

        # Check if field is rich text (HTML) field
        is_html_field = _is_richtext_field(instance.__class__, field_key)

        # Update translations field
        if not instance.translations:
            instance.translations = {}

        # Update translations for this specific field
        from translations.lock_service import is_field_locked
        skipped_locked = []

        for lang, translated_text in translations.items():
            # Skip locked languages
            if is_field_locked(model_type, int(object_id), field_key, lang):
                skipped_locked.append(lang)
                continue

            if lang not in instance.translations:
                instance.translations[lang] = {}

            # Sanitize HTML content if this is a rich text field
            sanitized_text = _sanitize_if_html(translated_text, is_html_field)
            instance.translations[lang][field_key] = sanitized_text

            # Update metadata
            if '_meta' not in instance.translations[lang]:
                instance.translations[lang]['_meta'] = {}

            instance.translations[lang]['_meta'].update({
                'auto': False,  # Manually edited
                'verified': True,  # User verified
                'edited_at': datetime.now().isoformat(),
                'last_field': field_key
            })

        # Save the instance
        instance.save(update_fields=['translations'])

        # Clear cache
        cache_key = f'translations_{model_type}_{object_id}'
        cache.delete(cache_key)

        saved_languages = [l for l in translations.keys() if l not in skipped_locked]
        logger.info(f"Saved manual translations for {model_type}:{object_id}.{field_key}")

        return JsonResponse({
            'success': True,
            'message': f'Translations saved successfully for {field_key}',
            'saved_languages': saved_languages,
            'skipped_locked': skipped_locked,
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.error(f"Error saving translations: {e}")
        return JsonResponse({'error': str(e)}, status=500)


@staff_member_required
@require_http_methods(["GET"])
def get_available_languages_api(request):
    """
    Get list of available languages from translation service.

    URL pattern: /api/translation/languages/

    Returns:
        JSON with available languages and primary language
    """
    utils = _get_translation_utils()
    if not utils:
        return JsonResponse({
            'error': 'Translation utilities not available'
        }, status=503)

    languages = utils['get_available_languages']()
    primary = utils['get_primary_language']()

    return JsonResponse({
        'languages': [
            {
                'code': code,
                'name': str(name),
                'is_primary': code == primary
            }
            for code, name in languages
        ],
        'primary_language': primary
    })


@staff_member_required
@require_http_methods(["POST"])
@csrf_exempt
def save_field_value(request, model_type, object_id, field_key):
    """
    Save the source field value before translation (prevents data loss).

    URL pattern: /api/translation/<model_type>/<object_id>/<field_key>/save_field/
    Example: /api/translation/core.sitesettings/1/site_name/save_field/

    POST body:
        {
            "value": "My Store Name"
        }

    Returns:
        JSON with save status
    """
    try:
        data = json.loads(request.body)
        value = data.get('value', '').strip()

        if not value:
            return JsonResponse({'error': 'Value is required'}, status=400)

        # Get the model instance
        instance, error = _get_model_instance(model_type, object_id)
        if error:
            return error

        # Check if the model has this field
        if not hasattr(instance, field_key):
            return JsonResponse({
                'error': f'Field {field_key} does not exist on {model_type}'
            }, status=400)

        # Check if field is rich text (HTML) field and sanitize if needed
        is_html_field = _is_richtext_field(instance.__class__, field_key)
        sanitized_value = _sanitize_if_html(value, is_html_field)

        # Save the field value
        setattr(instance, field_key, sanitized_value)
        instance.save(update_fields=[field_key])

        logger.info(f"Saved field value for {model_type}:{object_id}.{field_key}")

        return JsonResponse({
            'success': True,
            'message': f'Field {field_key} saved successfully',
            'value': value
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.error(f"Error saving field value: {e}")
        return JsonResponse({'error': str(e)}, status=500)


@staff_member_required
@require_http_methods(["GET"])
def translation_health(request):
    """
    Get translation service health status.

    URL pattern: /api/translation/health/

    Returns:
        JSON with service health information
    """
    utils = _get_translation_utils()
    if not utils:
        return JsonResponse({
            'error': 'Translation utilities not available'
        }, status=503)

    status = utils['get_translation_health_status']()
    return JsonResponse(status)
