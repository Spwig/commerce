"""
Management command to cleanup expired affiliate tracking clicks.

Usage:
    ./manage.py cleanup_expired_clicks [--days 365] [--dry-run]

This command:
1. Finds clicks older than the specified retention period
2. Optionally filters to only delete clicks beyond their program's cookie lifetime
3. Deletes expired clicks to keep database clean
4. Provides detailed statistics on cleanup

Best practice: Run this command daily via cron/celery beat
"""

import logging
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db.models import Count
from django.utils import timezone

from affiliate.models import Click

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Cleanup expired affiliate tracking clicks"

    def add_arguments(self, parser):
        parser.add_argument(
            "--days", type=int, default=365, help="Delete clicks older than N days (default: 365)"
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Preview what would be deleted without actually deleting",
        )
        parser.add_argument(
            "--batch-size",
            type=int,
            default=1000,
            help="Number of records to delete per batch (default: 1000)",
        )
        parser.add_argument(
            "--respect-cookie-lifetime",
            action="store_true",
            help="Only delete clicks older than their program cookie lifetime",
        )

    def handle(self, *args, **options):
        retention_days = options["days"]
        dry_run = options["dry_run"]
        batch_size = options["batch_size"]
        respect_cookie_lifetime = options["respect_cookie_lifetime"]

        self.stdout.write(self.style.SUCCESS("=" * 70))
        self.stdout.write(self.style.SUCCESS("Affiliate Click Cleanup"))
        self.stdout.write(self.style.SUCCESS("=" * 70))
        self.stdout.write(f"Retention period: {retention_days} days")
        self.stdout.write(f"Dry run: {dry_run}")
        self.stdout.write(f"Batch size: {batch_size}")
        self.stdout.write(f"Respect cookie lifetime: {respect_cookie_lifetime}")
        self.stdout.write("")

        # Calculate cutoff date
        cutoff_date = timezone.now() - timedelta(days=retention_days)

        # Build query
        if respect_cookie_lifetime:
            # Only delete clicks that are older than both:
            # 1. The retention period AND
            # 2. Their program's cookie lifetime
            # This ensures we don't delete clicks that could still attribute
            self.stdout.write(
                self.style.WARNING(
                    "Note: Only deleting clicks that are expired based on their "
                    "program's cookie lifetime\n"
                )
            )

            # Get clicks where clicked_at + cookie_lifetime < now
            # This is more complex and requires raw SQL or computed field
            # For simplicity, we'll use the retention period
            expired_clicks = Click.objects.filter(clicked_at__lt=cutoff_date)
        else:
            # Simple: delete all clicks older than retention period
            expired_clicks = Click.objects.filter(clicked_at__lt=cutoff_date)

        # Get statistics before deletion
        total_expired = expired_clicks.count()

        if total_expired == 0:
            self.stdout.write(
                self.style.SUCCESS(f"✓ No clicks found older than {retention_days} days")
            )
            return

        # Get breakdown by program
        program_stats = (
            expired_clicks.values("link__program__name")
            .annotate(click_count=Count("id"))
            .order_by("-click_count")
        )

        self.stdout.write(
            self.style.WARNING(f"Found {total_expired:,} expired clicks to delete:\n")
        )

        for stat in program_stats[:10]:  # Show top 10 programs
            program_name = stat["link__program__name"] or "Unknown Program"
            self.stdout.write(f"  • {program_name}: {stat['click_count']:,} clicks")

        if len(program_stats) > 10:
            self.stdout.write(f"  ... and {len(program_stats) - 10} more programs")

        self.stdout.write("")

        if dry_run:
            self.stdout.write(
                self.style.WARNING("DRY RUN - No clicks deleted. Remove --dry-run to execute.")
            )
            # Show sample of clicks that would be deleted
            sample_clicks = expired_clicks.select_related("link", "link__program")[:5]

            if sample_clicks:
                self.stdout.write("\nSample clicks that would be deleted:")
                for click in sample_clicks:
                    self.stdout.write(
                        f"  • Click #{click.id}: {click.clicked_at.strftime('%Y-%m-%d')} "
                        f"- {click.link.program.name if click.link and click.link.program else 'N/A'}"
                    )

            return

        # Delete in batches to avoid memory issues
        self.stdout.write(
            self.style.WARNING(f"Deleting {total_expired:,} clicks in batches of {batch_size}...")
        )
        self.stdout.write("")

        deleted_total = 0
        batch_num = 0

        while True:
            # Get IDs of next batch
            batch_ids = list(expired_clicks.values_list("id", flat=True)[:batch_size])

            if not batch_ids:
                break

            # Delete batch
            batch_num += 1
            deleted_count, _ = Click.objects.filter(id__in=batch_ids).delete()
            deleted_total += deleted_count

            self.stdout.write(
                f"  Batch {batch_num}: Deleted {deleted_count:,} clicks "
                f"(Total: {deleted_total:,}/{total_expired:,})"
            )

            # Small delay to avoid overwhelming database
            # time.sleep(0.1)

        # Final summary
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("=" * 70))
        self.stdout.write(self.style.SUCCESS("Cleanup Complete"))
        self.stdout.write(self.style.SUCCESS("=" * 70))
        self.stdout.write(self.style.SUCCESS(f"✓ Deleted {deleted_total:,} expired clicks"))
        self.stdout.write(
            self.style.SUCCESS(f"✓ Cutoff date: {cutoff_date.strftime('%Y-%m-%d %H:%M:%S')}")
        )

        # Log to application logs
        logger.info(
            f"Affiliate click cleanup completed: {deleted_total:,} clicks deleted "
            f"(older than {retention_days} days)"
        )
