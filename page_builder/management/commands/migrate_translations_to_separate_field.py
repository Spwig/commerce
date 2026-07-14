"""
Django management command to migrate translations from content field to separate translations field.
This ensures clean separation of content and translations.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from page_builder.models import Element


class Command(BaseCommand):
    help = "Migrate translations from content field to separate translations field"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Preview changes without making them",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]

        self.stdout.write("Starting translation migration...")
        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN - No changes will be made"))

        elements = Element.objects.all()
        migrated_count = 0
        cleaned_count = 0

        with transaction.atomic():
            for element in elements:
                changes_made = False

                if element.content and isinstance(element.content, dict):
                    # Check if translations exist in content field
                    if "_translations" in element.content:
                        translations = element.content.get("_translations", {})

                        if translations:
                            # Move translations to separate field
                            if not element.translations:
                                element.translations = {}

                            # Merge with existing translations in separate field
                            for lang, trans_data in translations.items():
                                if lang not in element.translations:
                                    element.translations[lang] = trans_data
                                    self.stdout.write(
                                        f"  Element {element.id}: Migrating {lang} translation"
                                    )

                            migrated_count += 1
                            changes_made = True

                        # Remove from content field
                        del element.content["_translations"]
                        cleaned_count += 1

                    # Also remove translation metadata from content
                    if "_translation_meta" in element.content:
                        del element.content["_translation_meta"]
                        changes_made = True

                    # Save if changes were made
                    if changes_made and not dry_run:
                        element.save()
                        self.stdout.write(self.style.SUCCESS(f"✓ Element {element.id} updated"))

        # Summary
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("Migration Summary:"))
        self.stdout.write(f"- Elements with translations migrated: {migrated_count}")
        self.stdout.write(f"- Content fields cleaned: {cleaned_count}")
        self.stdout.write(f"- Total elements processed: {elements.count()}")

        if dry_run:
            self.stdout.write(
                self.style.WARNING("\nDRY RUN COMPLETE - Run without --dry-run to apply changes")
            )
        else:
            self.stdout.write(self.style.SUCCESS("\nMigration complete!"))
