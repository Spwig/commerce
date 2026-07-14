"""
Management command to translate email templates
Usage: ./shop_venv/bin/python manage.py translate_email_templates --languages es fr de
"""

from django.core.management.base import BaseCommand

from email_system.models import EmailTemplate
from email_system.services.translation_service import EmailTemplateTranslationService


class Command(BaseCommand):
    help = "Translate email templates to specified languages"

    def add_arguments(self, parser):
        parser.add_argument(
            "--languages",
            nargs="+",
            type=str,
            help="Language codes to translate to (e.g., es fr de)",
        )
        parser.add_argument(
            "--template-types",
            nargs="+",
            type=str,
            help="Specific template types to translate (optional)",
        )
        parser.add_argument(
            "--all",
            action="store_true",
            help="Translate all templates to all supported languages",
        )

    def handle(self, *args, **options):
        service = EmailTemplateTranslationService()

        if options["all"]:
            self.stdout.write("Translating all templates to all supported languages...")
            result = service.bulk_translate_all_templates()

            if result["success"]:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created {result['total_jobs']} translation jobs for "
                        f"{result['total_templates']} templates"
                    )
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f"Error: {result.get('message', 'Unknown error')}")
                )
            return

        languages = options.get("languages")
        if not languages:
            self.stdout.write(self.style.ERROR("Please specify --languages or use --all"))
            return

        template_types = options.get("template_types")
        if template_types:
            templates = EmailTemplate.objects.filter(
                is_system=True, language_code="en", template_type__in=template_types
            )
        else:
            templates = EmailTemplate.objects.filter(is_system=True, language_code="en")

        if not templates.exists():
            self.stdout.write(self.style.WARNING("No templates found to translate"))
            return

        total_jobs = 0
        for template in templates:
            self.stdout.write(f"Translating {template.template_type}...")
            result = service.translate_template(template=template, target_languages=languages)

            if result["success"]:
                jobs_count = len(result.get("jobs", []))
                total_jobs += jobs_count
                if jobs_count > 0:
                    self.stdout.write(f"  Created {jobs_count} translation jobs")
                else:
                    self.stdout.write(f"  {result['message']}")
            else:
                self.stdout.write(
                    self.style.WARNING(f"  Error: {result.get('message', 'Unknown error')}")
                )

        self.stdout.write(self.style.SUCCESS(f"Successfully created {total_jobs} translation jobs"))
