"""
Translation API endpoints for media library assets
"""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
import json
import logging
from datetime import datetime

from media_library.models import MediaAsset
from page_builder.translation_utils import (
    get_translation_health_status,
    should_schedule_translation,
    get_available_languages,
    get_primary_language
)

logger = logging.getLogger(__name__)


@staff_member_required
@require_http_methods(["POST"])
def translate_media_asset(request):
    """
    Translate media asset fields (title, alt_text, description) to specified languages.
    """
    try:
        data = json.loads(request.body)
        # Support both media_id and element_id for compatibility with TranslationEditor
        media_id = data.get('media_id') or data.get('element_id')
        target_languages = data.get('languages', [])
        fields = data.get('fields', ['title', 'alt_text', 'description'])
        force_immediate = data.get('force_immediate', False)

        logger.info(f"Translation request for media: media_id={media_id}, languages={target_languages}, fields={fields}")

        # Validate input
        if not media_id:
            return JsonResponse({'error': 'Media ID required'}, status=400)

        # Get media asset
        try:
            media_asset = MediaAsset.objects.get(id=media_id)
        except MediaAsset.DoesNotExist:
            return JsonResponse({'error': 'Media asset not found'}, status=404)

        # Check service health
        health_status = get_translation_health_status()
        if not health_status.get('available', False):
            return JsonResponse({
                'error': 'Translation service unavailable',
                'details': health_status
            }, status=503)

        # Calculate content size for scheduling check
        text_content = ' '.join([
            str(getattr(media_asset, field, ''))
            for field in fields
        ])
        char_count = len(text_content)

        should_schedule, reason = should_schedule_translation(
            char_count,
            len(target_languages)
        )

        if should_schedule and not force_immediate:
            return JsonResponse({
                'recommend_schedule': True,
                'reason': reason,
                'estimated_time': f"{(char_count * len(target_languages)) / 1000:.1f} seconds"
            })

        # Perform translations
        from translations.client import TranslatorClient
        client = TranslatorClient()

        translations_made = {}
        errors = []

        # Get source language
        source_lang = get_primary_language()

        for lang in target_languages:
            if lang == source_lang:
                continue

            lang_translations = {}

            for field in fields:
                field_content = getattr(media_asset, field, '')
                if not field_content:
                    continue

                try:
                    translated = client.translate(
                        field_content,
                        source_lang=source_lang,
                        target_lang=lang
                    )

                    lang_translations[field] = translated
                    logger.info(f"Translated {field} to {lang} for media {media_id}")

                except Exception as e:
                    logger.error(f"Translation failed for {field} to {lang}: {str(e)}")
                    errors.append(f"Failed to translate {field} to {lang}: {str(e)}")

            if lang_translations:
                # Store translations in the model
                if not media_asset.translations:
                    media_asset.translations = {}

                media_asset.translations[lang] = {
                    **lang_translations,
                    '_meta': {
                        'auto': True,
                        'verified': False,
                        'translated_at': datetime.now().isoformat()
                    }
                }
                translations_made[lang] = lang_translations

        # Save the media asset with translations
        if translations_made:
            media_asset.save()

        return JsonResponse({
            'success': True,
            'translations': translations_made,
            'errors': errors if errors else None
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)


@staff_member_required
@require_http_methods(["GET"])
def media_translation_status(request, media_id):
    """
    Get translation status for a media asset.
    """
    try:
        media_asset = MediaAsset.objects.get(id=media_id)
    except MediaAsset.DoesNotExist:
        return JsonResponse({'error': 'Media asset not found'}, status=404)

    translations = media_asset.translations or {}

    # Get available languages
    available_languages = get_available_languages()
    primary_language = get_primary_language()

    # Check which languages have translations
    translated_languages = list(translations.keys())
    missing_languages = [
        lang for lang in available_languages
        if lang != primary_language and lang not in translated_languages
    ]

    return JsonResponse({
        'media_id': str(media_id),
        'translations': translations,
        'translated_languages': translated_languages,
        'missing_languages': missing_languages,
        'primary_language': primary_language
    })


@staff_member_required
@require_http_methods(["POST"])
@csrf_exempt
def save_media_translations(request, media_id):
    """
    Save manual translations for a media asset.
    """
    try:
        data = json.loads(request.body)
        translations = data.get('translations', {})

        try:
            media_asset = MediaAsset.objects.get(id=media_id)
        except MediaAsset.DoesNotExist:
            return JsonResponse({'error': 'Media asset not found'}, status=404)

        # Update translations
        if not media_asset.translations:
            media_asset.translations = {}

        for lang, fields in translations.items():
            if lang not in media_asset.translations:
                media_asset.translations[lang] = {}

            # Update fields
            media_asset.translations[lang].update(fields)

            # Update metadata
            if '_meta' not in media_asset.translations[lang]:
                media_asset.translations[lang]['_meta'] = {}

            media_asset.translations[lang]['_meta'].update({
                'verified': True,
                'updated_at': datetime.now().isoformat()
            })

        media_asset.save()

        return JsonResponse({
            'success': True,
            'message': 'Translations saved successfully'
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)
    except Exception as e:
        logger.error(f"Save translations error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)


@staff_member_required
@require_http_methods(["POST"])
@csrf_exempt
def clear_media_translations(request, media_id):
    """
    Clear translations for a media asset.
    """
    try:
        data = json.loads(request.body)
        languages = data.get('languages', [])

        try:
            media_asset = MediaAsset.objects.get(id=media_id)
        except MediaAsset.DoesNotExist:
            return JsonResponse({'error': 'Media asset not found'}, status=404)

        if not media_asset.translations:
            return JsonResponse({
                'success': True,
                'message': 'No translations to clear'
            })

        if languages:
            # Clear specific languages
            for lang in languages:
                if lang in media_asset.translations:
                    del media_asset.translations[lang]
        else:
            # Clear all translations
            media_asset.translations = {}

        media_asset.save()

        return JsonResponse({
            'success': True,
            'message': 'Translations cleared successfully'
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)
    except Exception as e:
        logger.error(f"Clear translations error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)