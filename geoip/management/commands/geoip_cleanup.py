"""
Clean up expired GeoIP cache entries
"""

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import models
from django.utils import timezone

from geoip.models import GeoLocation


class Command(BaseCommand):
    help = "Clean up expired GeoIP cache entries"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be deleted without actually deleting",
        )
        parser.add_argument(
            "--days",
            type=int,
            default=0,
            help="Also remove entries older than X days (even if not expired)",
        )
        parser.add_argument(
            "--keep-recent",
            type=int,
            default=0,
            help="Keep at least X most recent entries per IP prefix",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        days = options["days"]
        options["keep_recent"]

        now = timezone.now()

        # Count expired entries
        expired_qs = GeoLocation.objects.filter(expires_at__lt=now)
        expired_count = expired_qs.count()

        # Count old entries if days specified
        old_count = 0
        if days > 0:
            cutoff_date = now - timedelta(days=days)
            old_qs = GeoLocation.objects.filter(resolved_at__lt=cutoff_date)
            old_count = old_qs.count()

        self.stdout.write(f"Found {expired_count} expired entries")
        if days > 0:
            self.stdout.write(f"Found {old_count} entries older than {days} days")

        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN - No entries will be deleted"))

            # Show sample of what would be deleted
            if expired_count > 0:
                self.stdout.write("\nSample of expired entries to be deleted:")
                for entry in expired_qs[:5]:
                    self.stdout.write(
                        f"  - {entry.ip_address} ({entry.country_code}) expired {entry.expires_at}"
                    )

            if old_count > 0 and days > 0:
                self.stdout.write(f"\nSample of old entries to be deleted (>{days} days):")
                for entry in old_qs[:5]:
                    self.stdout.write(
                        f"  - {entry.ip_address} ({entry.country_code}) from {entry.resolved_at}"
                    )
        else:
            # Delete expired entries
            if expired_count > 0:
                expired_qs.delete()
                self.stdout.write(self.style.SUCCESS(f"✓ Deleted {expired_count} expired entries"))

            # Delete old entries if specified
            if days > 0 and old_count > 0:
                old_qs.delete()
                self.stdout.write(self.style.SUCCESS(f"✓ Deleted {old_count} old entries"))

        # Vacuum/optimize if significant deletions
        total_deleted = expired_count + (old_count if days > 0 else 0)
        if total_deleted > 1000 and not dry_run:
            self.stdout.write("Optimizing database...")
            from django.db import connection

            with connection.cursor() as cursor:
                cursor.execute("VACUUM ANALYZE geoip_geolocation;")
            self.stdout.write(self.style.SUCCESS("✓ Database optimized"))

        # Final summary
        remaining = GeoLocation.objects.count()
        self.stdout.write(f"\nRemaining cached entries: {remaining}")

        # Calculate cache size
        if remaining > 0:
            avg_confidence = GeoLocation.objects.aggregate(avg=models.Avg("confidence"))["avg"]
            self.stdout.write(f"Average confidence: {avg_confidence:.1%}")
