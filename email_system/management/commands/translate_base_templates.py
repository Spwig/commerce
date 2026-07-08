"""
Management command to translate all base email templates to admin languages.

This creates the 72 base templates (12 template types × 6 admin languages):
- en (English) - already exists
- es (Spanish)
- fr (French)
- de (German)
- ja (Japanese)
- pt (Portuguese)
- zh-hans (Simplified Chinese)

Usage:
    python manage.py translate_base_templates
    python manage.py translate_base_templates --languages es fr  # Specific languages only
    python manage.py translate_base_templates --template-types order_confirmation  # Specific templates only
    python manage.py translate_base_templates --process-jobs  # Also process the jobs immediately
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from email_system.models import EmailTemplate, EmailTemplateTranslation
from email_system.services.translation_service import EmailTemplateTranslationService
from translations.models import TranslationJob, TranslationProvider, TranslationProviderAccount
from translations.tasks import TranslationJobProcessor
import time


class Command(BaseCommand):
    help = 'Translate all base email templates to admin languages'

    # Admin languages (excluding English which is the source)
    ADMIN_LANGUAGES = ['es', 'fr', 'de', 'ja', 'pt', 'zh-hans', 'ar', 'ru']

    # All template types
    TEMPLATE_TYPES = [
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

    def add_arguments(self, parser):
        parser.add_argument(
            '--languages',
            nargs='+',
            help='Specific languages to translate to (space-separated)',
        )
        parser.add_argument(
            '--template-types',
            nargs='+',
            help='Specific template types to translate (space-separated)',
        )
        parser.add_argument(
            '--process-jobs',
            action='store_true',
            help='Process translation jobs immediately after creating them',
        )
        parser.add_argument(
            '--skip-existing',
            action='store_true',
            default=True,
            help='Skip templates that already have translations (default: True)',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force re-translation even if translation exists',
        )

    def handle(self, *args, **options):
        # Get options
        languages = options.get('languages') or self.ADMIN_LANGUAGES
        template_types = options.get('template_types') or self.TEMPLATE_TYPES
        process_jobs = options.get('process_jobs', False)
        skip_existing = options.get('skip_existing', True) and not options.get('force', False)

        self.stdout.write(self.style.SUCCESS('🌍 Email Template Base Translation'))
        self.stdout.write(self.style.SUCCESS('=' * 60))

        # Verify translation provider is active (local or external component)
        provider = TranslationProvider.objects.filter(is_active=True).first()
        external_account = TranslationProviderAccount.objects.filter(is_active=True).first()
        if not provider and not external_account:
            raise CommandError(
                '❌ No active translation provider found. '
                'Please configure a translation provider first.'
            )

        provider_name = provider.name if provider else external_account.display_name
        self.stdout.write(f"✓ Translation provider: {provider_name}")
        self.stdout.write(f"✓ Languages: {', '.join(languages)}")
        self.stdout.write(f"✓ Template types: {len(template_types)}")
        self.stdout.write('')

        # Get all English base templates
        base_templates = EmailTemplate.objects.filter(
            language_code='en',
            is_system=True,
            template_type__in=template_types
        )

        if not base_templates.exists():
            raise CommandError('❌ No English base templates found')

        self.stdout.write(f"Found {base_templates.count()} English base templates\n")

        # Statistics
        stats = {
            'jobs_created': 0,
            'jobs_skipped': 0,
            'jobs_processed': 0,
            'jobs_failed': 0,
            'total_strings': 0,
        }

        translation_service = EmailTemplateTranslationService()
        job_processor = TranslationJobProcessor() if process_jobs else None

        # Translate each template
        for template in base_templates:
            self.stdout.write(f"\n📧 {template.template_type} (v{template.version})")
            self.stdout.write(f"   ID: {template.id}")

            # Check which languages already have translations
            if skip_existing:
                existing_translations = set(
                    EmailTemplateTranslation.objects.filter(
                        template=template
                    ).values_list('language_code', flat=True)
                )
                languages_to_translate = [
                    lang for lang in languages
                    if lang not in existing_translations
                ]

                if len(languages_to_translate) < len(languages):
                    skipped = set(languages) - set(languages_to_translate)
                    self.stdout.write(
                        self.style.WARNING(
                            f"   ⏭️  Skipping existing: {', '.join(sorted(skipped))}"
                        )
                    )
                    stats['jobs_skipped'] += len(skipped)
            else:
                languages_to_translate = languages

            if not languages_to_translate:
                self.stdout.write(self.style.WARNING("   ⏭️  All translations exist, skipping"))
                continue

            # Create translation jobs
            try:
                result = translation_service.translate_template(
                    template=template,
                    target_languages=languages_to_translate,
                    user=None
                )

                if result.get('success'):
                    jobs = result.get('jobs', [])
                    stats['jobs_created'] += len(jobs)

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"   ✓ Created {len(jobs)} translation jobs: {', '.join(languages_to_translate)}"
                        )
                    )

                    # Get string count from first job
                    if jobs:
                        first_job = TranslationJob.objects.get(id=jobs[0]['job_id'])
                        source_content = first_job.translated_data.get('source_content', {})
                        string_count = len(source_content.get('translatable_strings', {}))
                        stats['total_strings'] += string_count * len(jobs)
                        self.stdout.write(f"   📝 {string_count} strings per language")

                    # Process jobs immediately if requested
                    if process_jobs and job_processor:
                        self.stdout.write(f"   🔄 Processing {len(jobs)} jobs...")

                        for job_info in jobs:
                            job_id = job_info['job_id']
                            lang = job_info['language']

                            try:
                                # Process the job
                                job_processor.process_job(job_id)

                                # Check result
                                job = TranslationJob.objects.get(id=job_id)
                                if job.status == 'completed':
                                    self.stdout.write(
                                        self.style.SUCCESS(f"      ✓ {lang}: completed")
                                    )
                                    stats['jobs_processed'] += 1
                                elif job.status == 'failed':
                                    self.stdout.write(
                                        self.style.ERROR(
                                            f"      ✗ {lang}: failed - {job.error_message}"
                                        )
                                    )
                                    stats['jobs_failed'] += 1

                            except Exception as e:
                                self.stdout.write(
                                    self.style.ERROR(f"      ✗ {lang}: {e}")
                                )
                                stats['jobs_failed'] += 1

                        # Small delay between templates to avoid overwhelming the AI service
                        if template != base_templates.last():
                            time.sleep(1)

                else:
                    self.stdout.write(
                        self.style.ERROR(f"   ✗ Failed: {result.get('message')}")
                    )

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"   ✗ Error: {e}"))
                continue

        # Print summary
        self.stdout.write('\n')
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('📊 Translation Summary'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(f"✓ Translation jobs created: {stats['jobs_created']}")
        self.stdout.write(f"⏭️  Jobs skipped (existing): {stats['jobs_skipped']}")
        self.stdout.write(f"📝 Total strings queued: {stats['total_strings']}")

        if process_jobs:
            self.stdout.write(f"✓ Jobs processed successfully: {stats['jobs_processed']}")
            if stats['jobs_failed'] > 0:
                self.stdout.write(
                    self.style.ERROR(f"✗ Jobs failed: {stats['jobs_failed']}")
                )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"\n⚠️  Jobs created but not processed. "
                    f"Run with --process-jobs to translate immediately."
                )
            )

        self.stdout.write('')

        # Show next steps
        if not process_jobs and stats['jobs_created'] > 0:
            self.stdout.write(self.style.WARNING('Next steps:'))
            self.stdout.write('  1. Process jobs manually or via queue system')
            self.stdout.write('  2. Verify translations in admin interface')
            self.stdout.write('  3. Test email rendering with translated templates')
