"""
Translation API endpoints for page builder elements
"""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.core.cache import cache
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime

from page_builder.models import Element
from page_builder.translation_utils import (
    get_translation_health_status,
    should_schedule_translation,
    estimate_translation_time,
    TranslationFallbackHandler,
    get_available_languages,
    get_primary_language,
    get_translation_coverage
)

logger = logging.getLogger(__name__)


@staff_member_required
@require_http_methods(["GET"])
def translation_health(request):
    """
    Get translation service health status.
    Includes service availability, performance metrics, and recommendations.
    """
    status = get_translation_health_status()

    # Add additional context for UI
    status['ui_recommendations'] = {
        'can_translate': status.get('available', False),
        'warnings': health.get_degradation_warnings(),
        'available_languages': get_available_languages()
    }

    return JsonResponse(status)


@staff_member_required
@require_http_methods(["POST"])
@csrf_exempt
def translate_element(request):
    """
    Translate a page builder element to specified languages.
    Integrates health checks and scheduling recommendations.
    """
    try:
        data = json.loads(request.body)
        element_id = data.get('element_id')
        target_languages = data.get('languages', [])
        fields = data.get('fields', ['text'])  # Fields to translate
        content_to_translate = data.get('content')  # Content sent from frontend
        schedule = data.get('schedule', False)  # Whether to schedule for later
        force_immediate = data.get('force_immediate', False)  # Bypass recommendation check

        logger.info(f"Translation request: element_id={element_id}, languages={target_languages}, fields={fields}, force_immediate={force_immediate}")

        # Validate input
        if not element_id:
            return JsonResponse({'error': 'Element ID required'}, status=400)

        # Get element
        try:
            element = Element.objects.get(id=element_id)
        except Element.DoesNotExist:
            return JsonResponse({'error': 'Element not found'}, status=404)

        # Check service health first
        health_status = get_translation_health_status()
        if not health_status.get('available', False):
            # Use fallback handler
            fallback = TranslationFallbackHandler()
            response = fallback.handle_service_unavailable(
                element.content,
                target_languages,
                element_id
            )
            return JsonResponse(response, status=503)

        # Check if we should recommend scheduling
        text_content = ' '.join([
            str(element.content.get(field, ''))
            for field in fields
        ])
        char_count = len(text_content)

        should_schedule, reason = should_schedule_translation(
            char_count,
            len(target_languages)
        )

        # Only recommend scheduling if not forcing immediate and not already scheduling
        if should_schedule and not schedule and not force_immediate:
            # Return recommendation to schedule
            return JsonResponse({
                'success': False,
                'recommend_schedule': True,
                'reason': reason,
                'estimated_time': estimate_translation_time(
                    char_count,
                    len(target_languages)
                ),
                'char_count': char_count,
                'language_count': len(target_languages)
            }, status=202)

        # Handle degraded service
        warnings = []
        if health_status.get('status') == 'degraded':
            warnings.append(health_status.get('message', 'Service degraded'))
            if health_status.get('cpu_percent', 0) > 70:
                warnings.append('High CPU usage may result in slower translations')
            if health_status.get('memory_percent', 0) > 80:
                warnings.append('High memory usage may limit batch translation size')
        if warnings:
            fallback = TranslationFallbackHandler()
            degradation_response = fallback.handle_service_degraded(
                text_content,
                target_languages
            )

            # Add to response but continue
            response_data = {
                'warnings': warnings,
                'degradation_info': degradation_response
            }
        else:
            response_data = {}

        # Perform translation (or schedule it)
        if schedule:
            # Create translation job
            job = _create_translation_job(
                element,
                target_languages,
                fields,
                char_count
            )

            response_data.update({
                'success': True,
                'scheduled': True,
                'job_id': job.id if job else None,
                'message': f'Translation scheduled for {len(target_languages)} languages'
            })

            return JsonResponse(response_data)

        # Immediate translation
        logger.info(f"Starting immediate translation for element {element_id} to {len(target_languages)} languages: {target_languages}")
        try:
            from translations.client import TranslatorClient
            client = TranslatorClient()

            translations = {}
            failed_languages = []

            # Debug: Check what we're about to translate
            logger.info(f"About to translate to languages: {target_languages}")
            logger.info(f"Fields to translate: {fields}")
            logger.info(f"Element content: {element.content}")

            # Translate to each target language
            for lang in target_languages:
                logger.info(f"Processing language: {lang}")
                try:
                    lang_translations = {}

                    for field in fields:
                        # Use content from request if provided, otherwise from element
                        if content_to_translate:
                            field_content = content_to_translate
                        else:
                            field_content = element.content.get(field, '')

                        if field_content:
                            logger.info(f"Translating field '{field}' to {lang}: '{field_content[:50]}...'")
                            print(f"[DEBUG] Calling translate: text='{field_content}', source={get_primary_language()}, target={lang}")
                            try:
                                translated = client.translate(
                                    field_content,
                                    source_lang=get_primary_language(),
                                    target_lang=lang
                                )
                                print(f"[DEBUG] Translation result for {lang}: {translated}")
                                if translated:
                                    lang_translations[field] = translated
                                    logger.info(f"Translation result for {lang}: '{translated[:50]}...'")
                                else:
                                    logger.warning(f"No translation returned for field '{field}' to {lang}")
                                    print(f"[DEBUG] No translation returned for {lang}")
                            except Exception as trans_error:
                                print(f"[DEBUG] Translation error for {lang}: {trans_error}")
                                logger.error(f"Translation error for {lang}: {trans_error}")
                                raise

                    if lang_translations:
                        translations[lang] = lang_translations

                except Exception as e:
                    logger.error(f"Failed to translate to {lang}: {e}")
                    failed_languages.append(lang)

            # Update element with translations
            if translations:
                # Store translations in the dedicated translations field, not in content
                if not element.translations:
                    element.translations = {}

                # Update translations for each language
                for lang, lang_translations in translations.items():
                    if lang not in element.translations:
                        element.translations[lang] = {}

                    # Store the translations with metadata
                    element.translations[lang] = {
                        **lang_translations,  # Contains the translated fields
                        '_meta': {
                            'auto': True,
                            'verified': False,
                            'translated_at': datetime.now().isoformat()
                        }
                    }

                # Save the element with updated translations
                element.save()

                # Clear any cached translations
                cache_key = f'element_translations_{element_id}'
                cache.delete(cache_key)

            # Handle partial failures
            if failed_languages:
                fallback = TranslationFallbackHandler()
                partial_response = fallback.handle_partial_failure(
                    translations,
                    failed_languages,
                    'Translation service error'
                )
                response_data.update(partial_response)
            else:
                # Build detailed response
                message_parts = []
                if translations:
                    message_parts.append(f"Translated to {len(translations)} languages")
                if failed_languages:
                    message_parts.append(f"{len(failed_languages)} failed")

                response_data.update({
                    'success': len(translations) > 0,
                    'translations': translations,
                    'message': ' - '.join(message_parts) if message_parts else 'No translations completed',
                    'successful_languages': list(translations.keys()),
                    'failed_languages': failed_languages,
                    'total_requested': len(target_languages)
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
        logger.error(f"Unexpected error in translate_element: {e}")
        return JsonResponse({'error': 'Internal server error'}, status=500)


@staff_member_required
@require_http_methods(["POST"])
@csrf_exempt
def save_element_translations(request, element_id):
    """
    Save translations for an element.
    This endpoint updates only the translations field, not the content.
    """
    try:
        data = json.loads(request.body)
        translations = data.get('translations', {})

        # Get the element
        try:
            element = Element.objects.get(id=element_id)
        except Element.DoesNotExist:
            return JsonResponse({'error': 'Element not found'}, status=404)

        # Update translations field
        if not element.translations:
            element.translations = {}

        # Merge new translations with existing ones
        element.translations.update(translations)

        # Save the element
        element.save(update_fields=['translations'])

        return JsonResponse({
            'success': True,
            'message': 'Translations saved successfully',
            'translations': element.translations
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.error(f"Error saving translations: {e}")
        return JsonResponse({'error': str(e)}, status=500)


@staff_member_required
@require_http_methods(["GET"])
def element_translation_status(request, element_id):
    """
    Get translation status and coverage for an element.
    Now reads from the separate translations field, not from content.
    """
    try:
        element = Element.objects.get(id=element_id)
    except Element.DoesNotExist:
        return JsonResponse({'error': 'Element not found'}, status=404)

    # Get coverage info
    coverage = get_translation_coverage(element)

    # Get translations from the separate translations field
    # NOT from the content field
    translations = element.translations or {}

    # Build detailed status
    status = {
        'element_id': element_id,
        'coverage': coverage,
        'primary_language': get_primary_language(),
        'available_translations': list(translations.keys()),
        'translations': translations,  # Include actual translations for frontend
        'translation_details': {}
    }

    # Add details for each translation
    for lang, content in translations.items():
        # Skip metadata fields
        if isinstance(content, dict):
            # Filter out metadata fields
            actual_fields = {k: v for k, v in content.items() if not k.startswith('_')}
            status['translation_details'][lang] = {
                'fields': list(actual_fields.keys()),
                'char_count': sum(len(str(v)) for v in actual_fields.values()),
                'meta': content.get('_meta', {})
            }

    return JsonResponse(status)


@staff_member_required
@require_http_methods(["POST"])
@csrf_exempt
def clear_element_translations(request, element_id):
    """
    Clear all translations for an element.
    Now clears the separate translations field, not content field.
    """
    try:
        element = Element.objects.get(id=element_id)
    except Element.DoesNotExist:
        return JsonResponse({'error': 'Element not found'}, status=404)

    # Clear the separate translations field
    element.translations = {}
    element.save(update_fields=['translations'])

    # Clear cache
    cache_key = f'element_translations_{element_id}'
    cache.delete(cache_key)

    return JsonResponse({
        'success': True,
        'message': 'Translations cleared successfully'
    })


@staff_member_required
@require_http_methods(["POST"])
@csrf_exempt
def schedule_page_translation(request):
    """
    Schedule translation for an entire page.
    """
    try:
        data = json.loads(request.body)
        page_id = data.get('page_id')
        target_languages = data.get('languages', [])

        if not page_id:
            return JsonResponse({'error': 'Page ID required'}, status=400)

        # Get all text elements on the page
        elements = Element.objects.filter(
            page_id=page_id,
            element_type='text'
        )

        if not elements:
            return JsonResponse({
                'message': 'No text elements found on page'
            }, status=404)

        # Calculate total work
        total_chars = 0
        for element in elements:
            text_content = element.content.get('text', '')
            total_chars += len(text_content)

        # Check if scheduling is recommended
        health = TranslationServiceHealth()
        should_schedule, reason = health.should_schedule_translation(
            total_chars,
            len(target_languages)
        )

        estimated_time = health.estimate_translation_time(
            total_chars,
            len(target_languages)
        )

        # Create translation jobs for each element
        jobs_created = []
        for element in elements:
            job = _create_translation_job(
                element,
                target_languages,
                ['text'],
                len(element.content.get('text', ''))
            )
            if job:
                jobs_created.append(job.id)

        return JsonResponse({
            'success': True,
            'scheduled': True,
            'element_count': len(elements),
            'total_characters': total_chars,
            'language_count': len(target_languages),
            'estimated_time': estimated_time,
            'jobs_created': len(jobs_created),
            'recommendation': reason if should_schedule else None
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.error(f"Error scheduling page translation: {e}")
        return JsonResponse({'error': 'Internal server error'}, status=500)


def _create_translation_job(element, languages, fields, char_count):
    """
    Create a translation job for background processing.
    """
    try:
        from translations.models import TranslationJob

        job = TranslationJob.objects.create(
            job_type='page_element',
            status='pending',
            source_language=get_primary_language(),
            target_languages=languages,
            content_snapshot={
                'element_id': str(element.id),
                'fields': fields,
                'char_count': char_count,
                'content': {
                    field: element.content.get(field, '')
                    for field in fields
                }
            }
        )

        return job

    except ImportError:
        logger.warning("Translation job model not available")
        return None
    except Exception as e:
        logger.error(f"Failed to create translation job: {e}")
        return None


@staff_member_required
@require_http_methods(["GET"])
def get_available_languages_api(request):
    """
    Get list of available languages from translation service.
    """
    languages = get_available_languages()
    primary = get_primary_language()

    return JsonResponse({
        'languages': [
            {
                'code': code,
                'name': str(name),  # Convert to string to handle lazy translations
                'is_primary': code == primary
            }
            for code, name in languages
        ],
        'primary_language': primary
    })


@staff_member_required
@require_http_methods(["GET"])
def get_translation_job_status(request, job_id):
    """
    Get the status of a translation job.
    """
    try:
        from translations.models import TranslationJob

        job = TranslationJob.objects.get(id=job_id)

        return JsonResponse({
            'job_id': job.id,
            'status': job.status,
            'progress': job.progress,
            'total_characters': job.total_characters,
            'translated_characters': job.translated_characters,
            'translated_data': job.translated_data,
            'error_message': job.error_message if job.status == 'failed' else None,
            'created_at': job.created_at.isoformat(),
            'completed_at': job.completed_at.isoformat() if job.completed_at else None
        })
    except TranslationJob.DoesNotExist:
        return JsonResponse({'error': 'Job not found'}, status=404)