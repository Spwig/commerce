"""
Celery tasks for geoip app.

Background tasks for:
- Aggregating daily page/traffic stats from raw PageView records
- Cleaning up old PageView records (raw data; aggregates are preserved)
- Cleaning up old bot VisitorLocation records
"""

import logging

from celery import shared_task

from core.celery_utils import BackgroundDBTask

logger = logging.getLogger(__name__)


@shared_task(name="geoip.aggregate_daily_page_stats", base=BackgroundDBTask, ignore_result=True)
def aggregate_daily_page_stats():
    """
    Aggregate yesterday's PageView records into DailyPageStats and DailyTrafficStats.

    Runs daily at 3:00 AM. Idempotent (uses update_or_create).
    """
    from datetime import timedelta

    from django.db.models import Count, Q
    from django.utils import timezone

    from geoip.models import DailyPageStats, DailyTrafficStats, PageView, VisitorLocation

    try:
        yesterday = (timezone.now() - timedelta(days=1)).date()
        pv_qs = PageView.objects.filter(timestamp__date=yesterday)

        if not pv_qs.exists():
            logger.info(f"No page views for {yesterday}, skipping aggregation")
            return

        # Aggregate per-page stats
        page_stats = pv_qs.values("url_path").annotate(
            views=Count("id"),
            unique_visitors=Count("session_key", distinct=True),
            bot_views=Count("id", filter=Q(is_bot=True)),
            entries=Count("id", filter=Q(is_entry_page=True)),
        )

        page_count = 0
        for row in page_stats:
            DailyPageStats.objects.update_or_create(
                date=yesterday,
                url_path=row["url_path"],
                defaults={
                    "views": row["views"],
                    "unique_visitors": row["unique_visitors"],
                    "bot_views": row["bot_views"],
                    "entries": row["entries"],
                },
            )
            page_count += 1

        # Aggregate global traffic stats
        total_views = pv_qs.count()
        human_qs = pv_qs.filter(is_bot=False)
        bot_views = pv_qs.filter(is_bot=True).count()
        unique_visitors = human_qs.values("session_key").distinct().count()

        # New vs returning: new = first_seen is yesterday
        visitor_sessions = human_qs.values_list("session_key", flat=True).distinct()
        new_visitors = VisitorLocation.objects.filter(
            session_key__in=list(visitor_sessions),
            first_seen__date=yesterday,
        ).count()
        returning_visitors = unique_visitors - new_visitors

        # Device breakdown from visitor records that were active yesterday
        device_counts = (
            VisitorLocation.objects.filter(
                session_key__in=list(visitor_sessions),
            )
            .values("device_type")
            .annotate(count=Count("id"))
        )
        devices = {row["device_type"]: row["count"] for row in device_counts}

        DailyTrafficStats.objects.update_or_create(
            date=yesterday,
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

        logger.info(
            f"Aggregated daily stats for {yesterday}: "
            f"{total_views} views across {page_count} pages, "
            f"{unique_visitors} unique visitors"
        )

    except Exception as e:
        logger.error(f"Error aggregating daily page stats: {e}", exc_info=True)


@shared_task(name="geoip.cleanup_old_pageviews", base=BackgroundDBTask, ignore_result=True)
def cleanup_old_pageviews(days=90):
    """
    Delete raw PageView records older than specified days.
    DailyPageStats/DailyTrafficStats aggregates are preserved indefinitely.

    Args:
        days: Number of days to retain raw PageView data (default: 90)
    """
    from datetime import timedelta

    from django.utils import timezone

    from geoip.models import PageView

    try:
        cutoff = timezone.now() - timedelta(days=days)
        deleted_count, _ = PageView.objects.filter(timestamp__lt=cutoff).delete()

        logger.info(f"Cleaned up {deleted_count} page view records older than {days} days")
        return deleted_count

    except Exception as e:
        logger.error(f"Error cleaning up old page views: {e}", exc_info=True)
        return 0


@shared_task(name="geoip.cleanup_old_visitors", base=BackgroundDBTask, ignore_result=True)
def cleanup_old_visitors(bot_days=30, human_days=180):
    """
    Clean up old VisitorLocation records.

    - Bot records older than bot_days (default 30)
    - Human records with no activity older than human_days (default 180)

    Args:
        bot_days: Retention period for bot visitor records
        human_days: Retention period for inactive human visitor records
    """
    from datetime import timedelta

    from django.utils import timezone

    from geoip.models import VisitorLocation

    try:
        now = timezone.now()

        # Clean up old bot records
        bot_cutoff = now - timedelta(days=bot_days)
        bot_deleted, _ = VisitorLocation.objects.filter(
            is_bot=True,
            last_seen__lt=bot_cutoff,
        ).delete()

        # Clean up old inactive human records
        human_cutoff = now - timedelta(days=human_days)
        human_deleted, _ = VisitorLocation.objects.filter(
            is_bot=False,
            last_seen__lt=human_cutoff,
        ).delete()

        logger.info(
            f"Cleaned up visitors: {bot_deleted} bots (>{bot_days}d), "
            f"{human_deleted} inactive humans (>{human_days}d)"
        )
        return bot_deleted + human_deleted

    except Exception as e:
        logger.error(f"Error cleaning up old visitors: {e}", exc_info=True)
        return 0
