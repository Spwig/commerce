"""
Management command to process completed translation jobs that haven't created templates yet.

This command checks for completed email template translation jobs and ensures
their callbacks are triggered to create EmailTemplate/EmailTemplateTranslation records.

Usage:
    python manage.py process_pending_translations

Can be run as a cron job or periodic Celery beat task.
"""

import logging
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Process completed translation jobs that haven't created templates"

    def handle(self, *args, **options):
        from email_system.models import EmailTemplate
        from email_system.services.translation_service import EmailTemplateTranslationService
        from translations.models import TranslationJob

        self.stdout.write(
            self.style.SUCCESS("\n=== Processing Pending Translation Callbacks ===\n")
        )

        # Find completed email template jobs from the last 24 hours
        cutoff_time = timezone.now() - timedelta(hours=24)
        completed_jobs = TranslationJob.objects.filter(
            content_type="email_template",
            status="completed",
            completed_at__isnull=False,
            completed_at__gte=cutoff_time,
        ).order_by("completed_at")

        if not completed_jobs.exists():
            self.stdout.write("No completed translation jobs found in the last 24 hours")
            return

        self.stdout.write(f"Found {completed_jobs.count()} completed translation jobs\n")

        service = EmailTemplateTranslationService()
        processed = 0
        skipped = 0
        errors = 0

        for job in completed_jobs:
            # Check if this job already created its template/translation
            if not job.translated_data:
                skipped += 1
                continue

            template_id = job.translated_data.get("template_id")
            if not template_id:
                skipped += 1
                continue

            target_lang = job.translated_data.get("language") or (
                job.target_languages[0] if job.target_languages else None
            )
            if not target_lang:
                skipped += 1
                continue

            create_base_template = job.translated_data.get("create_base_template", False)

            # Check if template/translation already exists
            try:
                if create_base_template:
                    # Check for base template
                    template = EmailTemplate.all_objects.get(id=template_id)
                    exists = EmailTemplate.objects.filter(
                        template_type=template.template_type,
                        language_code=target_lang,
                        is_system=True,
                    ).exists()

                    if exists:
                        skipped += 1
                        continue
                else:
                    # Check for translation
                    from email_system.models import EmailTemplateTranslation

                    template = EmailTemplate.all_objects.get(id=template_id)
                    exists = EmailTemplateTranslation.objects.filter(
                        template=template, language_code=target_lang
                    ).exists()

                    if exists:
                        skipped += 1
                        continue

            except Exception:
                # Template not found or other error, skip
                skipped += 1
                continue

            # Template/translation doesn't exist, trigger callback
            try:
                self.stdout.write(
                    f"  Processing job {job.id} ({template.template_type} → {target_lang})...",
                    ending="",
                )
                service.handle_translation_complete(job.id)
                processed += 1
                self.stdout.write(self.style.SUCCESS(" ✓"))
            except Exception as e:
                errors += 1
                self.stdout.write(self.style.ERROR(f" ✗ {str(e)}"))
                logger.error(f"Failed to process translation job {job.id}: {e}", exc_info=True)

        # Summary
        self.stdout.write("\n=== Summary ===")
        self.stdout.write(f"Processed: {processed}")
        self.stdout.write(f"Skipped: {skipped}")
        self.stdout.write(f"Errors: {errors}")

        if processed > 0:
            self.stdout.write(
                self.style.SUCCESS(f"\n✓ Successfully processed {processed} translation jobs")
            )
        elif errors > 0:
            self.stdout.write(self.style.ERROR(f"\n✗ {errors} jobs failed"))
        else:
            self.stdout.write("\nNo jobs needed processing")
