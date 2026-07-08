"""
Management command to import professionally translated email templates.

After receiving translated JSON files from translation service, use this command
to import them into the database as base templates in admin languages.

Usage:
    python manage.py import_translated_templates /path/to/translated_files/
    python manage.py import_translated_templates /path/to/translated_files/ --dry-run
"""

from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site
from email_system.models import EmailTemplate
import json
import os
from pathlib import Path


class Command(BaseCommand):
    help = 'Import professionally translated email templates from JSON files'

    def add_arguments(self, parser):
        parser.add_argument(
            'directory',
            type=str,
            help='Directory containing translated JSON files',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be imported without actually importing',
        )
        parser.add_argument(
            '--overwrite',
            action='store_true',
            help='Overwrite existing templates (default: skip existing)',
        )

    def handle(self, *args, **options):
        directory = Path(options['directory'])

        if not directory.exists():
            raise CommandError(f"Directory not found: {directory}")

        if not directory.is_dir():
            raise CommandError(f"Not a directory: {directory}")

        # Get site
        site = Site.objects.first()
        if not site:
            raise CommandError('No site found')

        # Find all JSON files
        json_files = list(directory.glob('*.json'))

        # Filter to only translated files (not English, not EXAMPLE)
        translated_files = [
            f for f in json_files
            if not f.name.endswith('_en.json')
            and 'EXAMPLE' not in f.name
        ]

        if not translated_files:
            self.stdout.write(self.style.WARNING(
                f'No translated JSON files found in {directory}\n'
                f'Expected files like: order_confirmation_es.json, order_confirmation_fr.json, etc.'
            ))
            return

        self.stdout.write(self.style.SUCCESS(f'\n{"="*80}'))
        self.stdout.write(self.style.SUCCESS(f'Importing Translated Email Templates'))
        self.stdout.write(self.style.SUCCESS(f'{"="*80}\n'))
        self.stdout.write(f'Directory: {directory}')
        self.stdout.write(f'Files found: {len(translated_files)}')

        if options['dry_run']:
            self.stdout.write(self.style.WARNING('\nDRY RUN - No templates will be imported\n'))

        imported_count = 0
        skipped_count = 0
        error_count = 0

        for json_file in sorted(translated_files):
            try:
                # Load JSON
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Validate required fields
                required_fields = ['template_type', 'language_code', 'subject', 'html_content', 'text_content']
                missing_fields = [field for field in required_fields if field not in data]

                if missing_fields:
                    self.stdout.write(self.style.ERROR(
                        f'  ✗ {json_file.name} - missing fields: {", ".join(missing_fields)}'
                    ))
                    error_count += 1
                    continue

                template_type = data['template_type']
                language_code = data['language_code']

                # Check if English is being imported (shouldn't happen)
                if language_code == 'en':
                    self.stdout.write(self.style.WARNING(
                        f'  ⊘ {json_file.name} - skipping English template (already exists)'
                    ))
                    skipped_count += 1
                    continue

                # Check if already exists
                existing = EmailTemplate.objects.filter(
                    site=site,
                    template_type=template_type,
                    language_code=language_code,
                    is_system=True
                ).first()

                if existing and not options['overwrite']:
                    self.stdout.write(
                        f'  ⊘ {json_file.name} - already exists (use --overwrite to replace)'
                    )
                    skipped_count += 1
                    continue

                if options['dry_run']:
                    action = 'would overwrite' if existing else 'would create'
                    self.stdout.write(self.style.SUCCESS(
                        f'  ✓ {json_file.name} - {action} {template_type} ({language_code})'
                    ))
                    imported_count += 1
                    continue

                # Import the template
                if existing:
                    # Update existing
                    existing.subject = data['subject']
                    existing.html_content = data['html_content']
                    existing.text_content = data['text_content']
                    existing.version += 1
                    existing.save()
                    action = 'updated'
                else:
                    # Create new
                    EmailTemplate.objects.create(
                        site=site,
                        template_type=template_type,
                        language_code=language_code,
                        subject=data['subject'],
                        html_content=data['html_content'],
                        text_content=data['text_content'],
                        is_system=True,
                        is_active=True,
                        version=1
                    )
                    action = 'created'

                self.stdout.write(self.style.SUCCESS(
                    f'  ✓ {json_file.name} - {action} {template_type} ({language_code})'
                ))
                imported_count += 1

            except json.JSONDecodeError as e:
                self.stdout.write(self.style.ERROR(
                    f'  ✗ {json_file.name} - invalid JSON: {str(e)}'
                ))
                error_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f'  ✗ {json_file.name} - error: {str(e)}'
                ))
                error_count += 1

        # Summary
        self.stdout.write(f'\n{"="*80}')
        self.stdout.write(self.style.SUCCESS(f'Imported: {imported_count}'))
        if skipped_count:
            self.stdout.write(f'Skipped: {skipped_count}')
        if error_count:
            self.stdout.write(self.style.ERROR(f'Errors: {error_count}'))
        self.stdout.write(f'{"="*80}\n')

        if options['dry_run']:
            self.stdout.write(self.style.WARNING('DRY RUN complete - no changes made'))
        else:
            self.stdout.write(self.style.SUCCESS('✅ Template import complete!'))

            if imported_count > 0:
                self.stdout.write('\nMerchants using these admin languages will now see templates in their language.')
                self.stdout.write('They can further customize them or use AI Translation Service for customer languages.')
