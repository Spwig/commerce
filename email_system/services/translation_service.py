"""
Translation Service
Integrates email templates with the translations app for AI-powered translation
"""

import logging

from django.db import transaction

logger = logging.getLogger(__name__)


class EmailTemplateTranslationService:
    """
    Manages email template translations using the translations app
    """

    def translate_template(
        self,
        template,
        target_languages: list[str],
        user=None,
        force_retranslate=False,
        create_base_template=False,
    ) -> dict[str, any]:
        """
        Create AI translation jobs for template in multiple languages

        Args:
            template: EmailTemplate to translate
            target_languages: List of language codes (e.g., ['es', 'fr', 'de'])
            user: User requesting translation (optional)
            force_retranslate: If True, retranslate even if translation exists (default: False)
            create_base_template: If True, creates base EmailTemplate records instead of translations (default: False)

        Returns:
            Dict with job IDs and status
        """
        from email_system.models import EmailTemplateTranslation

        try:
            from translations.models import (
                TranslationJob,
                TranslationProvider,
                TranslationProviderAccount,
            )
        except ImportError:
            logger.warning("Translations app not available")
            return {"success": False, "message": "Translations app not configured", "jobs": []}

        # Get active translation provider (local or external component-based)
        provider = TranslationProvider.objects.filter(is_active=True).first()
        has_external = TranslationProviderAccount.objects.filter(is_active=True).exists()
        if not provider and not has_external:
            return {
                "success": False,
                "message": "No active translation provider configured",
                "jobs": [],
            }

        # Filter out languages based on force_retranslate flag
        if force_retranslate:
            # Delete existing translations for requested languages
            EmailTemplateTranslation.objects.filter(
                template=template, language_code__in=target_languages
            ).delete()
            logger.info(f"Force retranslate: deleted existing translations for {target_languages}")

            languages_to_translate = [
                lang for lang in target_languages if lang != template.language_code
            ]
        else:
            # Filter out languages that already have translations
            existing_languages = set(
                EmailTemplateTranslation.objects.filter(template=template).values_list(
                    "language_code", flat=True
                )
            )

            languages_to_translate = [
                lang
                for lang in target_languages
                if lang not in existing_languages and lang != template.language_code
            ]

        if not languages_to_translate:
            return {
                "success": True,
                "message": "All requested languages already translated",
                "jobs": [],
            }

        # Extract translatable strings from template
        from email_system.services.template_translation_extractor import (
            TemplateTranslationExtractor,
        )

        extractor = TemplateTranslationExtractor()
        templates_with_placeholders, translatable_strings = extractor.extract_from_template(
            template_type=template.template_type,
            subject=template.subject,
            html_content=template.html_content,
            text_content=template.text_content,
        )

        # Prepare strings for translation API (just the text, not the structure)
        strings_for_translation = extractor.prepare_for_translation(translatable_strings)

        logger.info(
            f"Extracted {len(strings_for_translation)} translatable strings from "
            f"template '{template.template_type}'"
        )

        # Create translation jobs
        jobs_created = []

        with transaction.atomic():
            for language_code in languages_to_translate:
                # Store both the strings to translate AND the template structure
                # The translation worker will translate the strings, then we reconstruct
                content_to_translate = {
                    "translatable_strings": strings_for_translation,
                    "templates_with_placeholders": templates_with_placeholders,
                    "extraction_metadata": {
                        "string_count": len(strings_for_translation),
                        "extractor_version": "1.0",
                    },
                }

                # Create translation job
                # Note: object_id is PositiveIntegerField, but EmailTemplate uses UUID
                # Store template_id in translated_data instead
                job = TranslationJob.objects.create(
                    provider=provider,
                    job_type="email",
                    source_language=template.language_code,
                    target_languages=[language_code],
                    content_type="email_template",
                    object_id=None,  # Can't store UUID in integer field
                    fields_to_translate=["subject", "html_content", "text_content"],
                    translated_data={
                        "template_id": str(template.id),  # Store UUID as string
                        "source_content": content_to_translate,
                        "language": language_code,
                        "create_base_template": create_base_template,  # Flag to create base template vs translation
                    },
                    created_by=user,
                    status="pending",
                )

                jobs_created.append(
                    {"language": language_code, "job_id": job.id, "status": job.status}
                )

                logger.info(
                    f"Created translation job {job.id} for template "
                    f"'{template.template_type}' to {language_code} "
                    f"({len(strings_for_translation)} strings)"
                )

        # Queue jobs for processing via Celery
        try:
            from translations.tasks import process_translation_job

            for job_data in jobs_created:
                # Dispatch to Celery worker asynchronously
                process_translation_job.delay(job_data["job_id"])
                logger.info(f"Dispatched job {job_data['job_id']} to Celery worker")
        except ImportError:
            logger.warning("Celery tasks not available, jobs will be processed manually")

        return {
            "success": True,
            "message": f"Created {len(jobs_created)} translation jobs",
            "jobs": jobs_created,
        }

    def handle_translation_complete(self, job_id: int) -> None:
        """
        Callback when translation job completes

        Called by translations app when AI translation is ready.
        Creates EmailTemplateTranslation record with translated content.

        Args:
            job_id: TranslationJob ID
        """
        from email_system.models import EmailTemplate, EmailTemplateTranslation

        try:
            from translations.models import TranslationJob
        except ImportError:
            logger.error("Translations app not available")
            return

        try:
            job = TranslationJob.objects.get(id=job_id)

            if job.status != "completed":
                logger.warning(f"Translation job {job_id} not completed, skipping")
                return

            if job.content_type != "email_template":
                logger.warning(f"Translation job {job_id} not for email template, skipping")
                return

            # Extract translated content from translated_data
            translated_data = job.translated_data
            if not translated_data:
                logger.error(f"Translation job {job_id} has no translated data")
                return

            # Get the template (ID stored in translated_data since it's UUID)
            template_id = translated_data.get("template_id")
            if not template_id:
                logger.error(f"Translation job {job_id} has no template_id in translated_data")
                return

            template = EmailTemplate.objects.get(id=template_id)

            # Check if this uses the new extraction system
            source_content = translated_data.get("source_content", {})
            translated = translated_data.get("translated_content", {})

            if "translatable_strings" in source_content:
                # New system: reconstruct template from translated strings
                from email_system.services.template_translation_extractor import (
                    TemplateTranslationExtractor,
                )

                extractor = TemplateTranslationExtractor()

                # Translated strings should be in the translated_content
                # The AI service should return dict mapping keys to translated text
                translated_strings = translated.get("translatable_strings", {})
                templates_with_placeholders = source_content["templates_with_placeholders"]

                # Reconstruct the full templates
                reconstructed = extractor.reconstruct_template(
                    templates_with_placeholders, translated_strings
                )

                subject = reconstructed["subject"]
                html_content = reconstructed["html_content"]
                text_content = reconstructed["text_content"]

                logger.info(
                    f"Reconstructed template from {len(translated_strings)} translated strings"
                )
            else:
                # Old system: direct translation (will timeout, but keep for compatibility)
                subject = translated.get("subject", "")
                html_content = translated.get("html_content", "")
                text_content = translated.get("text_content", "")

            # Get target language from translated_data or target_languages
            target_lang = translated_data.get("language")
            if not target_lang and job.target_languages:
                target_lang = job.target_languages[0]

            # Check if this should create a base template (for site language) or a translation
            create_base_template = translated_data.get("create_base_template", False)

            if create_base_template:
                # Create base EmailTemplate for site language
                from django.contrib.sites.models import Site

                site = Site.objects.get(pk=1)

                base_template, created = EmailTemplate.objects.update_or_create(
                    site=site,
                    template_type=template.template_type,
                    language_code=target_lang,
                    is_system=True,
                    defaults={
                        "subject": subject,
                        "html_content": html_content,
                        "text_content": text_content,
                        "is_active": True,
                        "created_by": job.created_by,
                    },
                )

                action = "Created" if created else "Updated"
                logger.info(
                    f"{action} base template for '{template.template_type}' "
                    f"in {target_lang} (job_id={job_id})"
                )
            else:
                # Create or update translation (for non-site languages)
                translation, created = EmailTemplateTranslation.objects.update_or_create(
                    template=template,
                    language_code=target_lang,
                    defaults={
                        "subject": subject,
                        "html_content": html_content,
                        "text_content": text_content,
                        "translation_job": job,
                        "quality_score": None,  # Will be calculated later
                        "is_verified": False,  # Requires manual verification
                    },
                )

                action = "Created" if created else "Updated"
                logger.info(
                    f"{action} translation for template '{template.template_type}' "
                    f"in {target_lang} (job_id={job_id})"
                )

        except EmailTemplate.DoesNotExist:
            logger.error(f"Template not found for translation job {job_id}")
        except Exception as e:
            logger.error(f"Error handling translation completion: {e}")

    def bulk_translate_all_templates(
        self, target_languages: list[str] | None = None, user=None
    ) -> dict:
        """
        Translate all system templates to target languages

        Used during initial setup to create starter translations

        Args:
            target_languages: Languages to translate to (default: all supported)
            user: User requesting translation

        Returns:
            Summary of jobs created
        """
        from email_system.models import EmailTemplate

        if not target_languages:
            target_languages = ["es", "fr", "de", "ja", "pt", "zh-hans"]

        system_templates = EmailTemplate.objects.filter(is_system=True, language_code="en")

        total_jobs = 0
        results = []

        for template in system_templates:
            result = self.translate_template(
                template=template, target_languages=target_languages, user=user
            )
            total_jobs += len(result.get("jobs", []))
            results.append({"template": template.template_type, "jobs": result.get("jobs", [])})

        return {
            "success": True,
            "total_templates": system_templates.count(),
            "total_jobs": total_jobs,
            "languages": target_languages,
            "results": results,
        }

    def verify_translation(self, translation_id: int, user, verified: bool = True):
        """
        Manually verify or reject a translation

        Args:
            translation_id: EmailTemplateTranslation ID
            user: User performing verification
            verified: Mark as verified or not

        Returns:
            Updated EmailTemplateTranslation
        """
        from email_system.models import EmailTemplateTranslation

        translation = EmailTemplateTranslation.objects.get(id=translation_id)
        translation.is_verified = verified
        translation.translated_by = user
        translation.save()

        logger.info(
            f"Translation {translation_id} {'verified' if verified else 'rejected'} "
            f"by {user.username}"
        )

        return translation

    def get_translation_status(self, template) -> dict:
        """
        Get translation status for a template

        Returns:
            Dict with language coverage and job status
        """
        from email_system.models import EmailTemplateTranslation

        translations = EmailTemplateTranslation.objects.filter(template=template).select_related(
            "translation_job"
        )

        status = {
            "template_type": template.template_type,
            "languages": {},
            "coverage_percentage": 0,
        }

        # All supported languages
        supported_languages = ["en", "es", "fr", "de", "ja", "pt", "zh-hans"]

        for lang in supported_languages:
            if lang == template.language_code:
                # Source language
                status["languages"][lang] = {
                    "status": "source",
                    "is_verified": True,
                    "quality_score": 1.0,
                }
            else:
                translation = translations.filter(language_code=lang).first()
                if translation:
                    status["languages"][lang] = {
                        "status": "translated",
                        "is_verified": translation.is_verified,
                        "quality_score": translation.quality_score,
                        "job_id": translation.translation_job_id
                        if translation.translation_job
                        else None,
                    }
                else:
                    status["languages"][lang] = {
                        "status": "missing",
                        "is_verified": False,
                        "quality_score": None,
                    }

        # Calculate coverage
        translated_count = sum(
            1
            for lang_data in status["languages"].values()
            if lang_data["status"] in ["source", "translated"]
        )
        status["coverage_percentage"] = (translated_count / len(supported_languages)) * 100

        return status
