"""
Management command to evaluate loyalty tiers for all members.

This command should be run periodically (e.g., daily via cron) to ensure
all members have the correct tier based on their current metrics.
"""

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from loyalty.services.tiering_service import TieringService


class Command(BaseCommand):
    help = 'Evaluate and update loyalty tiers for all active members'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            default=None,
            help='Limit number of members to process (for testing)'
        )

        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Run without making any changes (preview only)'
        )

    def handle(self, *args, **options):
        limit = options.get('limit')
        dry_run = options.get('dry_run')

        self.stdout.write(
            self.style.SUCCESS(f'Starting loyalty tier evaluation at {timezone.now()}')
        )

        if dry_run:
            self.stdout.write(
                self.style.WARNING('DRY RUN MODE - No changes will be saved')
            )

        if limit:
            self.stdout.write(f'Processing limit: {limit} members')

        # Initialize tiering service
        tiering_service = TieringService()

        try:
            # Run batch evaluation
            if dry_run:
                self.stdout.write('Dry run not fully implemented - would evaluate tiers')
                stats = {
                    'total_processed': 0,
                    'promotions': 0,
                    'demotions': 0,
                    'no_change': 0,
                    'errors': 0,
                }
            else:
                stats = tiering_service.batch_evaluate_all_members(limit=limit)

            # Display results
            self.stdout.write('\n' + '=' * 60)
            self.stdout.write(self.style.SUCCESS('Tier Evaluation Complete'))
            self.stdout.write('=' * 60)
            self.stdout.write(f"Total Processed: {stats['total_processed']}")
            self.stdout.write(
                self.style.SUCCESS(f"Promotions: {stats['promotions']}")
            )
            self.stdout.write(
                self.style.WARNING(f"Demotions: {stats['demotions']}")
            )
            self.stdout.write(f"No Change: {stats['no_change']}")

            if stats['errors'] > 0:
                self.stdout.write(
                    self.style.ERROR(f"Errors: {stats['errors']}")
                )

            self.stdout.write('=' * 60)

            # Exit code based on errors
            if stats['errors'] > 0:
                raise CommandError(
                    f"Completed with {stats['errors']} error(s)"
                )

        except Exception as e:
            raise CommandError(f'Tier evaluation failed: {str(e)}')
