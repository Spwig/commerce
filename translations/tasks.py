"""
Background tasks for translation processing
"""
import logging
from datetime import timedelta

from celery import shared_task
from django.utils import timezone
from core.celery_utils import BackgroundDBTask
from .models import TranslationJob, TranslationProvider
from .client import get_translator_client

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    name='translations.process_job',
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
)
def process_translation_job(self, job_id):
    """
    Process a single translation job via Celery

    This task is automatically retried up to 3 times with exponential backoff
    if it fails. Progress is tracked in the TranslationJob model.
    """
    try:
        job = TranslationJob.objects.get(id=job_id)

        # Use the advanced processor class which has all the logic
        processor = TranslationJobProcessor()
        processor.process_job(job_id)

        logger.info(f"Successfully processed translation job {job_id}")
        return {'status': 'completed', 'job_id': job_id}

    except TranslationJob.DoesNotExist:
        logger.error(f"Translation job {job_id} not found")
        return {'status': 'error', 'message': 'Job not found'}

    except Exception as e:
        logger.error(f"Failed to process translation job {job_id}: {e}")

        # Mark job as failed if we've exhausted retries
        if self.request.retries >= self.max_retries:
            try:
                job = TranslationJob.objects.get(id=job_id)
                job.status = 'failed'
                job.error_message = f"Failed after {self.max_retries} retries: {str(e)}"
                job.save()
            except:
                pass

        # Re-raise to trigger Celery's retry mechanism
        raise


class TranslationJobProcessor:
    """
    Advanced job processor with priority and concurrency support
    """

    def __init__(self):
        self.client = get_translator_client()

    def process_job(self, job_id):
        """Process a single job with error handling"""
        try:
            job = TranslationJob.objects.get(id=job_id)

            # Update status
            job.status = 'processing'
            job.started_at = timezone.now()
            job.save()

            # Get content to translate based on job type
            content = self._get_content_for_translation(job)

            # Perform translation
            if content:
                translated = self._translate_content(job, content)
                self._save_translations(job, translated)

            # Mark as completed
            job.status = 'completed'
            job.completed_at = timezone.now()
            job.progress = 100
            job.save()

            logger.info(f"Job {job_id} marked as completed, calling _notify_completion...")

            # Notify if webhook configured
            try:
                self._notify_completion(job)
                logger.info(f"Successfully called _notify_completion for job {job_id}")
            except Exception as callback_error:
                logger.error(f"❌ Callback failed for job {job_id}: {callback_error}", exc_info=True)
                # Don't let callback failure fail the entire job
                pass

        except Exception as e:
            logger.error(f"Job {job_id} failed during processing: {e}", exc_info=True)
            self._handle_failure(job_id, e)

    def batch_translate(self, items, source_lang, target_langs):
        """Translate multiple items in batch"""
        results = []

        for target_lang in target_langs:
            batch_items = [
                {
                    'id': item['id'],
                    'text': item['text'],
                    'target_lang': target_lang
                }
                for item in items
            ]

            translated = self.client.translate_batch(batch_items)
            results.extend(translated)

        return results

    def update_progress(self, job, percent):
        """Update job progress"""
        job.progress = percent
        job.save(update_fields=['progress'])

    def _get_content_for_translation(self, job):
        """Extract content based on job type"""
        translated_data = job.translated_data or {}
        source_content = translated_data.get('source_content', {})

        # Email template with extracted strings
        if job.content_type == 'email_template' and 'translatable_strings' in source_content:
            return source_content['translatable_strings']

        # Legacy email template (full content - will likely timeout)
        elif job.content_type == 'email_template':
            return {
                'subject': source_content.get('subject', ''),
                'html_content': source_content.get('html_content', ''),
                'text_content': source_content.get('text_content', ''),
            }

        # Model-based content types (products, categories, pages, etc.)
        elif translated_data.get('registry_key'):
            return self._get_model_content(job, translated_data)

        # Generic field translation (scheduled from translation_api.py)
        elif job.content_type == 'generic_field':
            field_key = translated_data.get('field_key', '')
            text = translated_data.get('source_text', '')
            if field_key and text:
                return {field_key: text}

        return {}

    def _translate_content(self, job, content):
        """Perform the actual translation"""
        results = {}

        # Get target language from translated_data or target_languages list
        translated_data = job.translated_data or {}
        target_lang = translated_data.get('language')
        if not target_lang and job.target_languages:
            target_lang = job.target_languages[0]

        total_items = len(content)
        for idx, (key, text) in enumerate(content.items(), 1):
            try:
                # Translate this string
                translated = self.client.translate(
                    text=text,
                    source_lang=job.source_language,
                    target_lang=target_lang
                )

                if translated:
                    results[key] = translated

                # Update progress
                progress = int((idx / total_items) * 90)  # Reserve 10% for saving
                if progress != job.progress:
                    self.update_progress(job, progress)

                logger.debug(f"Translated string {idx}/{total_items} for job {job.id}")

            except Exception as e:
                logger.error(f"Failed to translate key '{key}' in job {job.id}: {e}")
                # Store original text as fallback
                results[key] = text

        return results

    def _save_translations(self, job, translations):
        """Save translated content"""
        # For email templates with extracted strings, save in the format expected by
        # EmailTemplateTranslationService.handle_translation_complete()
        translated_data = job.translated_data or {}
        source_content = translated_data.get('source_content', {})

        if job.content_type == 'email_template' and 'translatable_strings' in source_content:
            # Update translated_data with translated strings
            translated_data['translated_content'] = {
                'translatable_strings': translations,  # Dict of key -> translated text
            }
            job.translated_data = translated_data
            job.save(update_fields=['translated_data'])
            logger.info(f"Saved {len(translations)} translated strings for job {job.id}")

        # Legacy email template format
        elif job.content_type == 'email_template':
            translated_data['translated_content'] = translations  # Dict with subject, html_content, text_content
            job.translated_data = translated_data
            job.save(update_fields=['translated_data'])
            logger.info(f"Saved translated content for job {job.id}")

        # Model-based content types
        elif job.translated_data and job.translated_data.get('registry_key'):
            self._save_model_translations(job, translations)

        # Generic field: save to model instance's translations JSONField
        elif job.content_type == 'generic_field':
            self._save_generic_field_translations(job, translations)

        else:
            logger.warning(f"Unknown content type '{job.content_type}' for job {job.id}")

    def _get_model_content(self, job, translated_data):
        """
        Extract translatable field values from model instances.

        Returns dict keyed by "{pk}:{field_name}" -> source text.
        """
        from translations.content_registry import get_content_type, get_model_class

        registry_key = translated_data.get('registry_key')
        ct_entry = get_content_type(registry_key)
        if not ct_entry:
            logger.warning(f"Unknown registry key '{registry_key}' for job {job.id}")
            return {}

        model_class = get_model_class(registry_key)
        if not model_class:
            return {}

        object_ids = translated_data.get('object_ids', [])
        fields = ct_entry['fields']
        target_lang = translated_data.get('language') or (job.target_languages[0] if job.target_languages else None)
        is_simple = ct_entry.get('format') == 'simple'
        is_widget_config = ct_entry.get('format') == 'widget_config'

        content = {}
        try:
            instances = model_class.objects.filter(pk__in=object_ids)
        except Exception as e:
            logger.error(f"Failed to query {registry_key} for job {job.id}: {e}")
            return {}

        # Check locked fields
        locked = set()
        if target_lang:
            from translations.lock_service import get_locked_fields
            locked = get_locked_fields(registry_key, object_ids, target_lang)

        # Widget config format: extract from config JSONField dynamically
        if is_widget_config:
            return self._get_widget_content(instances, target_lang, locked, job)

        for instance in instances:
            translations = instance.translations or {}

            for field_name in fields:
                # Skip locked fields
                if (instance.pk, field_name) in locked:
                    continue

                source_value = getattr(instance, field_name, '')
                if not source_value:
                    continue

                # Check if already translated
                if target_lang:
                    if is_simple:
                        if translations.get(target_lang):
                            continue
                    else:
                        lang_data = translations.get(target_lang)
                        if isinstance(lang_data, dict) and lang_data.get(field_name):
                            continue

                content_key = f"{instance.pk}:{field_name}"
                content[content_key] = str(source_value)

        logger.info(f"Extracted {len(content)} strings from {registry_key} for job {job.id}")
        return content

    def _get_widget_content(self, instances, target_lang, locked, job):
        """
        Extract translatable content from Widget instances.

        Widget translatable fields are determined dynamically per widget_type
        from Widget.TRANSLATABLE_CONFIG_FIELDS and TRANSLATABLE_ARRAY_FIELDS.
        Also extracts 'content' TextField for text widgets.

        Returns dict keyed by "{pk}:{config_key}" -> source text.
        """
        from design.header_footer_models import Widget

        content = {}
        for instance in instances:
            config = instance.config or {}
            translations = instance.translations or {}
            lang_data = translations.get(target_lang, {}) if target_lang else {}
            wtype = instance.widget_type

            # Simple config fields
            simple_fields = Widget.TRANSLATABLE_CONFIG_FIELDS.get(wtype, [])
            for field in simple_fields:
                if (instance.pk, field) in locked:
                    continue
                value = config.get(field, '')
                if not value:
                    continue
                # Skip if already translated
                if lang_data.get(field):
                    continue
                content[f"{instance.pk}:{field}"] = str(value)

            # Array fields (e.g. links[].text, badges[].title)
            array_spec = Widget.TRANSLATABLE_ARRAY_FIELDS.get(wtype)
            if array_spec:
                array_key = array_spec['array_key']
                array_fields = array_spec['fields']
                items = config.get(array_key, [])
                for idx, item in enumerate(items):
                    if not isinstance(item, dict):
                        continue
                    for af in array_fields:
                        dotted_key = f"{array_key}.{idx}.{af}"
                        if (instance.pk, dotted_key) in locked:
                            continue
                        value = item.get(af, '')
                        if not value:
                            continue
                        if lang_data.get(dotted_key):
                            continue
                        content[f"{instance.pk}:{dotted_key}"] = str(value)

            # Text widget content field
            if wtype == 'text' and instance.content:
                if (instance.pk, 'content') not in locked and not lang_data.get('content'):
                    content[f"{instance.pk}:content"] = str(instance.content)

        logger.info(f"Extracted {len(content)} widget strings for job {job.id}")
        return content

    def _save_model_translations(self, job, translations):
        """
        Save translated content back to model instances.

        translations dict has keys like "123:name" -> "Nombre".
        """
        from translations.content_registry import get_content_type, get_model_class

        translated_data = job.translated_data or {}
        registry_key = translated_data.get('registry_key')
        ct_entry = get_content_type(registry_key)
        if not ct_entry:
            return

        model_class = get_model_class(registry_key)
        if not model_class:
            return

        target_lang = translated_data.get('language') or (job.target_languages[0] if job.target_languages else None)
        is_simple = ct_entry.get('format') == 'simple'
        is_widget_config = ct_entry.get('format') == 'widget_config'

        # Group translations by instance PK
        by_instance = {}
        for key, translated_text in translations.items():
            if ':' not in key:
                continue
            pk_str, field_name = key.split(':', 1)
            try:
                pk = int(pk_str)
            except ValueError:
                continue
            by_instance.setdefault(pk, {})[field_name] = translated_text

        if not by_instance:
            return

        # Check locked fields
        locked = set()
        if target_lang:
            from translations.lock_service import get_locked_fields
            locked = get_locked_fields(registry_key, list(by_instance.keys()), target_lang)

        instances = model_class.objects.filter(pk__in=by_instance.keys())
        saved_count = 0

        for instance in instances:
            instance_translations = by_instance.get(instance.pk, {})
            if not instance_translations:
                continue

            current = instance.translations or {}

            if is_simple:
                # Simple format: translations[lang] = value directly
                for field_name, value in instance_translations.items():
                    if (instance.pk, field_name) in locked:
                        continue
                    current[target_lang] = value
            else:
                # Nested / widget_config format: translations[lang][field] = value
                # For widget_config, keys may be dotted (e.g. "links.0.text")
                if target_lang not in current:
                    current[target_lang] = {}
                for field_name, value in instance_translations.items():
                    if (instance.pk, field_name) in locked:
                        continue
                    current[target_lang][field_name] = value

                # Add metadata
                current[target_lang]['_meta'] = {
                    'auto': True,
                    'verified': False,
                    'translated_at': timezone.now().isoformat(),
                }

            instance.translations = current
            instance.save(update_fields=['translations'])
            saved_count += 1

        # Invalidate coverage cache
        try:
            from translations.coverage_service import invalidate_coverage_cache
            invalidate_coverage_cache()
        except Exception:
            pass

        logger.info(f"Saved translations for {saved_count} {registry_key} instances in job {job.id}")

    def _save_generic_field_translations(self, job, translations):
        """
        Save translations for generic field jobs back to the model instance.

        These jobs are created by core/api/translation_api.py when scheduling
        is requested. The translated_data contains model_type, object_id,
        and field_key identifying exactly which field to update.
        """
        from django.apps import apps
        from django.core.cache import cache
        from translations.lock_service import is_field_locked

        translated_data = job.translated_data or {}
        model_type = translated_data.get('model_type', '')
        object_id = translated_data.get('object_id')
        field_key = translated_data.get('field_key', '')
        target_lang = translated_data.get('language') or (
            job.target_languages[0] if job.target_languages else None
        )

        if not all([model_type, object_id, field_key, target_lang]):
            logger.error(
                f"Missing data for generic_field job {job.id}: "
                f"model_type={model_type}, object_id={object_id}, "
                f"field_key={field_key}, target_lang={target_lang}"
            )
            return

        try:
            app_label, model_name = model_type.lower().split('.')
            model_class = apps.get_model(app_label, model_name)
            instance = model_class.objects.get(pk=object_id)
        except Exception as e:
            logger.error(f"Failed to load {model_type}:{object_id} for job {job.id}: {e}")
            return

        if is_field_locked(model_type, int(object_id), field_key, target_lang):
            logger.info(f"Skipping locked field {field_key}:{target_lang} for job {job.id}")
            return

        translated_text = translations.get(field_key, '')
        if not translated_text:
            logger.warning(f"No translated text for {field_key} in job {job.id}")
            return

        current = instance.translations or {}
        if target_lang not in current:
            current[target_lang] = {}

        current[target_lang][field_key] = translated_text

        if '_meta' not in current[target_lang]:
            current[target_lang]['_meta'] = {}
        current[target_lang]['_meta'].update({
            'auto': True,
            'verified': False,
            'translated_at': timezone.now().isoformat(),
            'last_field': field_key,
        })

        instance.translations = current
        instance.save(update_fields=['translations'])

        cache.delete(f'translations_{model_type}_{object_id}')

        try:
            from translations.coverage_service import invalidate_coverage_cache
            invalidate_coverage_cache()
        except Exception:
            pass

        logger.info(
            f"Saved generic_field translation for {model_type}:{object_id}."
            f"{field_key} -> {target_lang} (job {job.id})"
        )

    def _handle_failure(self, job_id, error):
        """Handle job failure"""
        try:
            job = TranslationJob.objects.get(id=job_id)
            job.status = 'failed'
            job.error_message = str(error)
            job.save()

            logger.error(f"Translation job {job_id} failed: {error}")

            # Fire webhook for external integrations
            try:
                from webhooks.services import trigger_webhook
                trigger_webhook('translation.job_failed', instance=job)
            except Exception as webhook_err:
                logger.warning(f"Failed to fire webhook for failed job {job_id}: {webhook_err}")
        except:
            pass

    def _notify_completion(self, job):
        """Send webhook notification and trigger callbacks"""
        # For email templates, trigger the email system callback
        if job.content_type == 'email_template':
            try:
                from email_system.services.translation_service import EmailTemplateTranslationService
                service = EmailTemplateTranslationService()
                service.handle_translation_complete(job.id)
                logger.info(f"Triggered email template callback for job {job.id}")
            except Exception as e:
                logger.error(f"Failed to trigger email template callback for job {job.id}: {e}")

        # Fire webhook for external integrations
        try:
            from webhooks.services import trigger_webhook
            trigger_webhook('translation.job_completed', instance=job)
        except Exception as e:
            logger.warning(f"Failed to fire webhook for completed job {job.id}: {e}")


@shared_task(base=BackgroundDBTask, ignore_result=True)
def process_pending_translation_callbacks():
    """
    Process completed translation jobs that haven't created templates yet.

    This task runs periodically to ensure translation callbacks are executed
    even if the Celery callback mechanism fails. Should be scheduled to run
    every 5-10 minutes via Celery Beat.

    Returns:
        int: Number of callbacks processed
    """
    from email_system.services.translation_service import EmailTemplateTranslationService
    from email_system.models import EmailTemplate, EmailTemplateTranslation

    # Find completed email template jobs from the last 2 hours
    cutoff_time = timezone.now() - timedelta(hours=2)
    completed_jobs = TranslationJob.objects.filter(
        content_type='email_template',
        status='completed',
        completed_at__isnull=False,
        completed_at__gte=cutoff_time
    ).order_by('completed_at')

    if not completed_jobs.exists():
        logger.debug("No recent completed translation jobs found")
        return 0

    service = EmailTemplateTranslationService()
    processed = 0

    for job in completed_jobs:
        # Check if this job already created its template/translation
        if not job.translated_data:
            continue

        template_id = job.translated_data.get('template_id')
        if not template_id:
            continue

        target_lang = job.translated_data.get('language') or (job.target_languages[0] if job.target_languages else None)
        if not target_lang:
            continue

        create_base_template = job.translated_data.get('create_base_template', False)

        # Check if template/translation already exists
        try:
            if create_base_template:
                # Check for base template
                template = EmailTemplate.all_objects.get(id=template_id)
                exists = EmailTemplate.objects.filter(
                    template_type=template.template_type,
                    language_code=target_lang,
                    is_system=True
                ).exists()

                if exists:
                    continue
            else:
                # Check for translation
                template = EmailTemplate.all_objects.get(id=template_id)
                exists = EmailTemplateTranslation.objects.filter(
                    template=template,
                    language_code=target_lang
                ).exists()

                if exists:
                    continue

        except Exception:
            # Template not found or other error, skip
            continue

        # Template/translation doesn't exist, trigger callback
        try:
            service.handle_translation_complete(job.id)
            processed += 1
            logger.info(f"Processed pending translation callback for job {job.id}")
        except Exception as e:
            logger.error(f"Failed to process translation job {job.id}: {e}", exc_info=True)

    if processed > 0:
        logger.info(f"✅ Processed {processed} pending translation callbacks")

    return processed


@shared_task(
    bind=True,
    name='translations.auto_translate_ui_strings',
    max_retries=3,
    default_retry_delay=120,
)
def auto_translate_ui_strings(self, site_language_id):
    """
    Auto-translate all UI strings for a language using the AI translation service.

    Triggered when a SiteLanguage is activated. Creates/updates the
    UITranslationOverride row with machine-translated strings.
    Only translates strings that don't already have a translation.
    """
    from translations.models import SiteLanguage, UITranslationOverride
    from translations.ui_string_registry import UI_STRING_REGISTRY, get_total_string_count

    try:
        site_lang = SiteLanguage.objects.get(id=site_language_id)
    except SiteLanguage.DoesNotExist:
        logger.warning(f"SiteLanguage {site_language_id} not found for auto-translate")
        return

    # Skip English — it's the source language
    if site_lang.code == 'en':
        return

    # Get or create the override row
    override_obj, created = UITranslationOverride.objects.get_or_create(
        language=site_lang,
        defaults={'total_strings': get_total_string_count()}
    )

    # Update total strings count (in case registry has grown)
    override_obj.total_strings = get_total_string_count()

    # Find strings that need translation (not already translated, not locked)
    existing = override_obj.overrides or {}
    locked_keys = {
        k for k, v in (override_obj.meta_info or {}).items()
        if isinstance(v, dict) and v.get('locked')
    }
    strings_to_translate = {
        k: v for k, v in UI_STRING_REGISTRY.items()
        if (k not in existing or not existing[k]) and k not in locked_keys
    }

    if not strings_to_translate:
        override_obj.save(update_fields=['total_strings'])
        logger.info(f"All UI strings already translated for {site_lang.code}")
        return

    client = get_translator_client()
    if not client.is_available():
        logger.warning(f"Translation service not available for UI strings auto-translate ({site_lang.code})")
        return

    logger.info(f"Auto-translating {len(strings_to_translate)} UI strings for {site_lang.code}")

    # Process in chunks of 50
    CHUNK_SIZE = 50
    meta_info = override_obj.meta_info or {}
    now = timezone.now().isoformat()
    items_list = list(strings_to_translate.items())

    for i in range(0, len(items_list), CHUNK_SIZE):
        chunk = items_list[i:i + CHUNK_SIZE]
        batch_items = [
            {
                "id": key,
                "text": english_text,
                "source_lang": "en",
                "target_lang": site_lang.code,
            }
            for key, english_text in chunk
        ]

        try:
            results = client.translate_batch(batch_items)

            for result in results:
                if result.get('success') and result.get('translated_text'):
                    key = result['id']
                    existing[key] = result['translated_text']
                    meta_info[key] = {
                        'auto': True,
                        'verified': False,
                        'translated_at': now,
                    }
        except Exception as e:
            logger.error(f"Batch translation failed for {site_lang.code} chunk {i}: {e}")

    # Save
    override_obj.overrides = existing
    override_obj.meta_info = meta_info
    override_obj.translated_count = sum(1 for v in existing.values() if v)
    override_obj.last_auto_translated_at = timezone.now()
    override_obj.save()

    # Invalidate cache
    from django.core.cache import cache
    cache_key = f'ui_trans_overrides:{site_lang.code}'
    cache.delete(cache_key)

    logger.info(
        f"Auto-translated {override_obj.translated_count}/{override_obj.total_strings} "
        f"UI strings for {site_lang.code}"
    )


@shared_task(name='translations.sync_ui_string_registry')
def sync_ui_string_registry_task():
    """
    Sync UI string registry with all UITranslationOverride rows.

    Updates total_strings, translated_count, and verified_count.
    Queued after language activation to ensure counts are correct.
    """
    from django.core.management import call_command
    call_command('sync_ui_string_registry')