"""
Site Language Translation Service
Automatically translates email templates when site language changes to non-admin language
"""

import logging
from typing import Dict, List, Optional
from django.conf import settings
from django.db import transaction

logger = logging.getLogger(__name__)


class SiteLanguageTranslationService:
    """
    Service for automatically translating email templates when site language changes
    """

    def __init__(self):
        # Get admin languages from Django settings
        self.ADMIN_LANGUAGES = [lang[0] for lang in settings.LANGUAGES]

        # All email template types that need translation
        self.TEMPLATE_TYPES = [
            'account_welcome',
            'admin_new_order',
            'admin_payment_failed',
            'delivery_confirmation',
            'email_verification',
            'order_confirmation',
            'order_delay',
            'password_reset',
            'payment_confirmation',
            'refund_notification',
            'review_request',
            'shipping_confirmation',
        ]

    def auto_translate_for_site_language(
        self,
        target_language: str,
        triggered_by: str = 'unknown'
    ) -> Dict:
        """
        Automatically create base email templates for a site language

        This is called when:
        - Admin changes site default language to a non-admin language
        - A custom language is selected that needs base templates

        Creates actual EmailTemplate records (is_system=True, language_code=target_language)
        by translating from English base templates.

        Args:
            target_language: ISO language code (e.g., 'it', 'ko', 'hi')
            triggered_by: Source of the trigger ('site_settings_change', 'manual', etc.)

        Returns:
            Dict with:
                success: bool
                message: str
                jobs_created: int
                target_language: str
                already_exists: bool (if base templates already exist)
        """
        from email_system.models import EmailTemplate, EmailTemplateTranslation
        from django.contrib.sites.models import Site

        # Validate that this is not an admin language
        if target_language in self.ADMIN_LANGUAGES:
            return {
                'success': False,
                'message': f'{target_language} is an admin language, use base templates instead',
                'jobs_created': 0,
                'target_language': target_language,
                'is_admin_language': True
            }

        # Check if base templates already exist for this language
        existing_count = EmailTemplate.objects.filter(
            language_code=target_language,
            is_system=True
        ).count()

        if existing_count >= len(self.TEMPLATE_TYPES):
            logger.info(
                f"Base templates already exist for {target_language} "
                f"({existing_count} templates). Skipping auto-translation."
            )
            return {
                'success': True,
                'message': f'All email base templates already exist for {target_language}',
                'jobs_created': 0,
                'target_language': target_language,
                'already_exists': True,
                'existing_count': existing_count
            }

        # Get all English base templates
        base_templates = EmailTemplate.objects.filter(
            language_code='en',
            is_system=True,
            template_type__in=self.TEMPLATE_TYPES
        )

        if not base_templates.exists():
            return {
                'success': False,
                'message': 'No English base templates found',
                'jobs_created': 0,
                'target_language': target_language
            }

        logger.info(
            f"Creating {base_templates.count()} base email templates for {target_language} "
            f"(triggered by: {triggered_by})"
        )

        # Use existing EmailTemplateTranslationService
        from email_system.services.translation_service import EmailTemplateTranslationService

        translation_service = EmailTemplateTranslationService()
        jobs_created = 0
        site = Site.objects.get(pk=1)

        # Create translation jobs for each template
        for template in base_templates:
            # Check if base template already exists for this template type
            existing = EmailTemplate.objects.filter(
                template_type=template.template_type,
                language_code=target_language,
                is_system=True
            ).exists()

            if existing:
                logger.debug(f"Base template already exists for {template.template_type} in {target_language}, skipping")
                continue

            # Create translation job that will create a base template
            result = translation_service.translate_template(
                template=template,
                target_languages=[target_language],
                user=None,  # System-triggered
                force_retranslate=False,
                create_base_template=True  # Create base EmailTemplate, not translation
            )

            if result['success'] and result['jobs']:
                jobs_created += len(result['jobs'])
                logger.debug(
                    f"Created translation job for {template.template_type} → {target_language}"
                )

        return {
            'success': True,
            'message': f'Created {jobs_created} translation jobs for {target_language}',
            'jobs_created': jobs_created,
            'target_language': target_language,
            'triggered_by': triggered_by,
            'templates_count': base_templates.count()
        }

    def get_translation_status_for_language(self, language_code: str) -> Dict:
        """
        Get translation status for a specific language

        Returns info about:
        - Is this an admin language?
        - How many templates are translated?
        - Which templates are missing?
        - Are there any pending translation jobs?
        """
        from email_system.models import EmailTemplate, EmailTemplateTranslation
        from translations.models import TranslationJob

        is_admin_language = language_code in self.ADMIN_LANGUAGES

        # Count existing translations
        existing_translations = EmailTemplateTranslation.objects.filter(
            language_code=language_code
        ).values_list('template__template_type', flat=True)

        existing_count = len(existing_translations)
        total_templates = len(self.TEMPLATE_TYPES)

        # Find missing templates
        missing_templates = set(self.TEMPLATE_TYPES) - set(existing_translations)

        # Check for pending/processing jobs
        pending_jobs = TranslationJob.objects.filter(
            content_type='email_template',
            target_languages__contains=[language_code],
            status__in=['pending', 'processing']
        ).count()

        return {
            'language_code': language_code,
            'is_admin_language': is_admin_language,
            'translations_count': existing_count,
            'total_templates': total_templates,
            'coverage_percentage': round((existing_count / total_templates) * 100, 1),
            'missing_templates': list(missing_templates),
            'pending_jobs': pending_jobs,
            'is_complete': existing_count >= total_templates,
        }

    def bulk_translate_multiple_languages(
        self,
        target_languages: List[str],
        user=None
    ) -> Dict:
        """
        Translate email templates to multiple non-admin languages at once

        Useful for:
        - Setup wizard (pre-translate common languages)
        - Merchant selecting multiple customer languages

        Args:
            target_languages: List of ISO language codes
            user: User requesting the translation (optional)

        Returns:
            Summary of jobs created per language
        """
        results = []
        total_jobs = 0

        for language_code in target_languages:
            result = self.auto_translate_for_site_language(
                target_language=language_code,
                triggered_by='bulk_translation'
            )
            results.append(result)
            if result['success']:
                total_jobs += result['jobs_created']

        return {
            'success': True,
            'total_jobs_created': total_jobs,
            'languages_processed': len(target_languages),
            'results': results
        }
