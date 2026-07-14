"""
Celery tasks for error report batch transmission.

Runs periodically to flush buffered error reports to the update server.
"""

import logging
from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from core.celery_utils import BackgroundDBTask

logger = logging.getLogger(__name__)


@shared_task(
    base=BackgroundDBTask,
    name="core.error_reporting.flush_error_reports",
    max_retries=2,
    default_retry_delay=120,
    soft_time_limit=120,
    ignore_result=True,
)
def flush_error_reports():
    """
    Batch-send pending error reports to the update server.
    Runs every 5 minutes via CELERY_BEAT_SCHEDULE.
    """
    from core.models import ErrorReport, SiteSettings

    settings_obj = SiteSettings.get_settings()
    if not settings_obj or not settings_obj.error_reporting_enabled:
        return {"status": "disabled", "sent": 0}

    reports = list(ErrorReport.objects.filter(status="pending").order_by("first_seen")[:100])

    if not reports:
        return {"status": "empty", "sent": 0}

    try:
        from core.error_reporting.client import ErrorReportingClient

        client = ErrorReportingClient()
        payload = client.build_payload(reports)
        success = client.send_batch(payload)

        if success:
            report_ids = [r.id for r in reports]
            ErrorReport.objects.filter(id__in=report_ids).update(
                status="sent",
                sent_at=timezone.now(),
            )
            _cleanup_old_reports()
            return {"status": "sent", "sent": len(reports)}
        else:
            return {"status": "failed", "sent": 0}

    except Exception as e:
        logger.warning("Error report transmission failed: %s", e)
        return {"status": "error", "sent": 0}


def _cleanup_old_reports():
    """Delete sent reports older than 7 days, pending/held reports older than 30 days."""
    from core.models import ErrorReport

    now = timezone.now()
    ErrorReport.objects.filter(status="sent", sent_at__lt=now - timedelta(days=7)).delete()
    ErrorReport.objects.filter(
        status__in=["pending", "held"], first_seen__lt=now - timedelta(days=30)
    ).delete()


@shared_task(
    base=BackgroundDBTask,
    name="core.error_reporting.send_bug_report",
    max_retries=3,
    default_retry_delay=60,
    soft_time_limit=30,
)
def send_bug_report(bug_report_id):
    """Send a single bug report to the update server immediately."""
    from core.models import BugReport

    try:
        report = BugReport.objects.get(id=bug_report_id, status="pending")
    except BugReport.DoesNotExist:
        return {"status": "not_found"}

    try:
        from core.error_reporting.client import BugReportClient

        client = BugReportClient()
        payload = client.build_payload(report)
        success = client.send(payload)

        if success:
            report.status = "sent"
            report.sent_at = timezone.now()
            report.save(update_fields=["status", "sent_at"])
            return {"status": "sent", "id": bug_report_id}
        else:
            report.status = "failed"
            report.save(update_fields=["status"])
            return {"status": "failed", "id": bug_report_id}

    except Exception as e:
        logger.warning("Bug report transmission failed: %s", e)
        report.status = "failed"
        report.save(update_fields=["status"])
        return {"status": "error", "id": bug_report_id}
