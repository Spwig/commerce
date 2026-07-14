"""
Management command to create base email templates in all admin interface languages.

These base templates are platform-provided translations that merchants will see
based on their selected admin interface language. This is different from the
AI Translation Service which merchants use to translate templates for their customers.

Usage:
    python manage.py create_admin_language_templates --all
    python manage.py create_admin_language_templates --languages es fr de
    python manage.py create_admin_language_templates --template-types order_confirmation shipping_confirmation
"""

import time

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand, CommandError

from email_system.models import EmailTemplate
from translations.client import TranslatorClient


class Command(BaseCommand):
    help = "Create base email templates in all admin interface languages using AI translation"

    def add_arguments(self, parser):
        parser.add_argument(
            "--all",
            action="store_true",
            help="Create templates for all template types and all admin languages",
        )
        parser.add_argument(
            "--languages",
            nargs="+",
            help="Specific languages to create (e.g., es fr de)",
        )
        parser.add_argument(
            "--template-types",
            nargs="+",
            help="Specific template types to create",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be created without actually creating",
        )

    def handle(self, *args, **options):
        # Get site
        site = Site.objects.first()
        if not site:
            raise CommandError("No site found")

        # Determine target languages
        admin_languages = [
            lang[0] for lang in settings.LANGUAGES if lang[0] != "en"
        ]  # Exclude English (already exists)

        if options["languages"]:
            target_languages = options["languages"]
            # Validate languages
            invalid = [lang for lang in target_languages if lang not in admin_languages]
            if invalid:
                raise CommandError(f"Invalid languages: {invalid}. Valid: {admin_languages}")
        elif options["all"]:
            target_languages = admin_languages
        else:
            raise CommandError("Please specify --all or --languages")

        # Determine template types
        if options["template_types"]:
            template_types = options["template_types"]
        else:
            # Get all system template types in English
            template_types = list(
                EmailTemplate.objects.filter(site=site, is_system=True, language_code="en")
                .values_list("template_type", flat=True)
                .distinct()
            )

        self.stdout.write(self.style.SUCCESS(f"\n{'=' * 80}"))
        self.stdout.write(self.style.SUCCESS("Creating Admin Language Base Templates"))
        self.stdout.write(self.style.SUCCESS(f"{'=' * 80}\n"))
        self.stdout.write(f"Target Languages: {', '.join(target_languages)}")
        self.stdout.write(f"Template Types: {', '.join(template_types)}")
        self.stdout.write(
            f"Total to create: {len(template_types)} × {len(target_languages)} = {len(template_types) * len(target_languages)}\n"
        )

        if options["dry_run"]:
            self.stdout.write(self.style.WARNING("DRY RUN - No templates will be created\n"))
            return

        # Get translation client
        try:
            client = TranslatorClient()
        except Exception as e:
            raise CommandError(f"Could not initialize translation client: {e}")

        created_count = 0
        skipped_count = 0
        error_count = 0

        for template_type in template_types:
            # Get English base template
            try:
                base_template = EmailTemplate.objects.get(
                    site=site, template_type=template_type, language_code="en", is_system=True
                )
            except EmailTemplate.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f"✗ No English template for {template_type}, skipping")
                )
                continue

            for target_lang in target_languages:
                # Check if already exists
                if EmailTemplate.objects.filter(
                    site=site,
                    template_type=template_type,
                    language_code=target_lang,
                    is_system=True,
                ).exists():
                    self.stdout.write(f"  ⊘ {template_type} ({target_lang}) - already exists")
                    skipped_count += 1
                    continue

                # Translate using AI service
                try:
                    self.stdout.write(
                        f"  ⟳ {template_type} ({target_lang}) - translating...", ending=""
                    )
                    self.stdout.flush()

                    # Translate subject
                    translated_subject = client.translate(
                        text=base_template.subject, source_lang="en", target_lang=target_lang
                    )

                    # Translate HTML content
                    translated_html = client.translate(
                        text=base_template.html_content, source_lang="en", target_lang=target_lang
                    )

                    # Translate text content
                    translated_text = client.translate(
                        text=base_template.text_content, source_lang="en", target_lang=target_lang
                    )

                    # Create new template
                    EmailTemplate.objects.create(
                        site=site,
                        template_type=template_type,
                        language_code=target_lang,
                        subject=translated_subject,
                        html_content=translated_html,
                        text_content=translated_text,
                        is_system=True,
                        is_active=True,
                        version=1,
                    )

                    self.stdout.write("\r" + " " * 80 + "\r", ending="")  # Clear line
                    self.stdout.write(
                        self.style.SUCCESS(f"  ✓ {template_type} ({target_lang}) - created")
                    )
                    created_count += 1

                    # Small delay to avoid overwhelming translation service
                    time.sleep(0.5)

                except Exception as e:
                    self.stdout.write("\r" + " " * 80 + "\r", ending="")  # Clear line
                    self.stdout.write(
                        self.style.ERROR(
                            f"  ✗ {template_type} ({target_lang}) - error: {str(e)[:50]}"
                        )
                    )
                    error_count += 1

        # Summary
        self.stdout.write(f"\n{'=' * 80}")
        self.stdout.write(self.style.SUCCESS(f"Created: {created_count}"))
        if skipped_count:
            self.stdout.write(f"Skipped: {skipped_count}")
        if error_count:
            self.stdout.write(self.style.ERROR(f"Errors: {error_count}"))
        self.stdout.write(f"{'=' * 80}\n")

        self.stdout.write(self.style.SUCCESS("✅ Base template creation complete!"))
        self.stdout.write(
            "\nThese templates are now available as base templates for merchants using"
        )
        self.stdout.write(
            "those admin interface languages. Merchants can still use the AI Translation"
        )
        self.stdout.write("Service to create customer-facing translations in additional languages.")
