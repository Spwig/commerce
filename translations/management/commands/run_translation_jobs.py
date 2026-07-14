import logging
import time

from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _

from translations.client import get_translator_client
from translations.models import TranslationJob, TranslationProvider

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = _("Run queued translation jobs")

    def add_arguments(self, parser):
        parser.add_argument(
            "--batch-size", type=int, default=10, help=_("Number of jobs to process in each batch")
        )
        parser.add_argument(
            "--continuous",
            action="store_true",
            help=_("Keep running and processing jobs continuously"),
        )
        parser.add_argument(
            "--interval",
            type=int,
            default=5,
            help=_("Seconds to wait between batches in continuous mode"),
        )

    def handle(self, *args, **options):
        batch_size = options["batch_size"]
        continuous = options["continuous"]
        interval = options["interval"]

        self.stdout.write(self.style.SUCCESS(_("Starting translation job processor...")))

        if continuous:
            self.stdout.write(_("Running in continuous mode. Press Ctrl+C to stop."))

        client = get_translator_client()
        if not client.is_available():
            self.stdout.write(
                self.style.ERROR(
                    _(
                        "Translation service is not available. Please check if the service is running."
                    )
                )
            )
            return

        processed_count = 0

        try:
            while True:
                # Get pending jobs
                jobs = TranslationJob.objects.filter(status="pending").order_by(
                    "-priority", "created_at"
                )[:batch_size]

                if not jobs:
                    if continuous:
                        time.sleep(interval)
                        continue
                    else:
                        break

                for job in jobs:
                    try:
                        self.process_job(job, client)
                        processed_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(_("Processed job #%(id)d") % {"id": job.id})
                        )
                    except Exception as e:
                        logger.error(f"Failed to process job #{job.id}: {e}")
                        job.mark_failed(str(e))
                        self.stdout.write(
                            self.style.ERROR(
                                _("Failed job #%(id)d: %(error)s") % {"id": job.id, "error": str(e)}
                            )
                        )

                if not continuous:
                    break

                time.sleep(interval)

        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING(_("\nStopping job processor...")))

        self.stdout.write(
            self.style.SUCCESS(
                _("Processed %(count)d translation jobs") % {"count": processed_count}
            )
        )

    def process_job(self, job, client):
        """Process a single translation job"""
        job.mark_processing()

        # Get provider
        provider = (
            job.provider
            or TranslationProvider.objects.filter(is_default=True, is_active=True).first()
        )

        if not provider:
            raise ValueError(_("No translation provider available"))

        # Perform translation based on job type
        if job.job_type == "product":
            self.translate_product(job, client)
        elif job.job_type == "category":
            self.translate_category(job, client)
        elif job.job_type == "email":
            self.translate_email_template(job, client)
        elif job.job_type == "custom":
            self.translate_custom(job, client)
        else:
            raise ValueError(_("Unsupported job type: %(type)s") % {"type": job.job_type})

        job.mark_completed()

    def translate_product(self, job, client):
        """Translate a product"""
        # This would be implemented to actually translate product fields
        # For now, just simulate
        time.sleep(1)
        job.progress = 100
        job.save()

    def translate_category(self, job, client):
        """Translate a category"""
        # This would be implemented to actually translate category fields
        time.sleep(1)
        job.progress = 100
        job.save()

    def translate_custom(self, job, client):
        """Process custom translation job"""
        # This would handle generic translation requests
        time.sleep(1)
        job.progress = 100
        job.save()

    def translate_email_template(self, job, client):
        """
        Translate an email template
        Processes the translation job data to create EmailTemplateTranslation records
        """
        from email_system.models import EmailTemplate, EmailTemplateTranslation

        # Extract job data
        translated_data = job.translated_data
        template_id = translated_data.get("template_id")
        source_content = translated_data.get("source_content", {})
        translatable_strings = source_content.get("translatable_strings", {})
        templates_with_placeholders = source_content.get("templates_with_placeholders", {})

        # Get the base template
        template = EmailTemplate.objects.get(id=template_id)

        # Process each target language
        for target_lang in job.target_languages:
            # Translate all strings
            translated_strings = {}
            total_strings = len(translatable_strings)

            for i, (key, text) in enumerate(translatable_strings.items(), 1):
                translated_text = client.translate(
                    text=text, source_lang=job.source_language, target_lang=target_lang
                )
                translated_strings[key] = translated_text

                # Update progress
                job.progress = int((i / total_strings) * 100)
                job.save(update_fields=["progress"])

            # Reconstruct template from translated strings
            subject = templates_with_placeholders.get("subject", "")
            html_content = templates_with_placeholders.get("html_content", "")
            text_content = templates_with_placeholders.get("text_content", "")

            for key, translated_text in translated_strings.items():
                placeholder = f"__TRANSLATE_{key}__"
                subject = subject.replace(placeholder, translated_text)
                html_content = html_content.replace(placeholder, translated_text)
                text_content = text_content.replace(placeholder, translated_text)

            # Create or update EmailTemplateTranslation
            EmailTemplateTranslation.objects.update_or_create(
                template=template,
                language_code=target_lang,
                defaults={
                    "subject": subject,
                    "html_content": html_content,
                    "text_content": text_content,
                    "base_template_version": template.version,
                },
            )

            logger.info(
                f"Created translation for template '{template.template_type}' in {target_lang}"
            )
