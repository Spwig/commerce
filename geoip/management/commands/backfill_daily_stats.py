"""
One-time management command to aggregate existing PageView records
into DailyPageStats and DailyTrafficStats.

Run after deploying the new models to seed the aggregation tables.
Idempotent — safe to re-run (uses update_or_create).

Usage:
    python manage.py backfill_daily_stats
    python manage.py backfill_daily_stats --days 90
"""

from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count, Q
from django.utils import timezone

from geoip.models import DailyPageStats, DailyTrafficStats, PageView, VisitorLocation


class Command(BaseCommand):
    help = "Backfill DailyPageStats and DailyTrafficStats from existing PageView records"

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=90,
            help="Number of days to backfill (default: 90)",
        )

    def handle(self, *args, **options):
        days = options["days"]
        if days < 1:
            raise CommandError("--days must be a positive integer.")
        now = timezone.now()
        end_date = now.date()
        start_date = end_date - timedelta(days=days - 1)

        total_pageviews = PageView.objects.filter(
            timestamp__date__gte=start_date,
            timestamp__date__lte=end_date,
        ).count()

        if total_pageviews == 0:
            self.stdout.write(self.style.WARNING("No PageView records found to backfill."))
            return

        self.stdout.write(
            f"Backfilling {total_pageviews} PageView records from {start_date} to {end_date}..."
        )

        current = start_date
        days_processed = 0

        while current <= end_date:
            pv_qs = PageView.objects.filter(timestamp__date=current)

            if pv_qs.exists():
                # Per-page stats
                page_stats = pv_qs.values("url_path").annotate(
                    views=Count("id"),
                    unique_visitors=Count("session_key", distinct=True),
                    bot_views=Count("id", filter=Q(is_bot=True)),
                    entries=Count("id", filter=Q(is_entry_page=True)),
                )

                for row in page_stats:
                    DailyPageStats.objects.update_or_create(
                        date=current,
                        url_path=row["url_path"],
                        defaults={
                            "views": row["views"],
                            "unique_visitors": row["unique_visitors"],
                            "bot_views": row["bot_views"],
                            "entries": row["entries"],
                        },
                    )

                # Global traffic stats
                total_views = pv_qs.count()
                human_qs = pv_qs.filter(is_bot=False)
                bot_views = pv_qs.filter(is_bot=True).count()
                unique_visitors = human_qs.values("session_key").distinct().count()

                visitor_sessions = list(human_qs.values_list("session_key", flat=True).distinct())
                new_visitors = VisitorLocation.objects.filter(
                    session_key__in=visitor_sessions,
                    first_seen__date=current,
                ).count()
                returning_visitors = unique_visitors - new_visitors

                session_devices = dict(
                    VisitorLocation.objects.filter(session_key__in=visitor_sessions).values_list(
                        "session_key", "device_type"
                    )
                )
                devices = {}
                for row in human_qs.values("session_key").annotate(views=Count("id")):
                    device_type = session_devices.get(row["session_key"], "unknown")
                    devices[device_type] = devices.get(device_type, 0) + row["views"]

                DailyTrafficStats.objects.update_or_create(
                    date=current,
                    defaults={
                        "total_views": total_views,
                        "unique_visitors": unique_visitors,
                        "bot_views": bot_views,
                        "new_visitors": new_visitors,
                        "returning_visitors": returning_visitors,
                        "desktop_views": devices.get("desktop", 0),
                        "mobile_views": devices.get("mobile", 0),
                        "tablet_views": devices.get("tablet", 0),
                    },
                )

                days_processed += 1

            current += timedelta(days=1)

        self.stdout.write(
            self.style.SUCCESS(f"Backfill complete: {days_processed} days processed.")
        )
