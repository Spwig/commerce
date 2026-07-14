"""
Celery tasks for accounts app.

Background tasks for:
- Cleaning up expired preference change logs (GDPR retention)
"""

import logging

from celery import shared_task

from core.celery_utils import BackgroundDBTask

logger = logging.getLogger(__name__)


@shared_task(name="accounts.cleanup_old_preference_logs", base=BackgroundDBTask, ignore_result=True)
def cleanup_old_preference_logs(days=90):
    """
    Clean up preference change logs older than specified days.

    GDPR best practice: Retain consent logs for 90 days minimum,
    then clean up to minimize data storage.

    Args:
        days: Number of days to retain logs (default: 90)

    Returns:
        int: Number of logs deleted
    """
    from accounts.models import PreferenceChangeLog

    try:
        deleted_count = PreferenceChangeLog.cleanup_old_logs(days=days)

        logger.info(f"Cleaned up {deleted_count} preference change logs older than {days} days")

        return deleted_count

    except Exception as e:
        logger.error(f"Error cleaning up preference logs: {e}", exc_info=True)
        return 0


@shared_task(name="accounts.cleanup_expired_sms_codes", base=BackgroundDBTask, ignore_result=True)
def cleanup_expired_sms_codes():
    """
    Clean up expired SMS verification codes.

    Clears codes sent more than 15 minutes ago to prevent reuse
    and reduce attack surface. Runs every 60 minutes.

    Returns:
        int: Number of codes cleared
    """
    from datetime import timedelta

    from django.utils import timezone

    from accounts.models import CommunicationPreference

    try:
        # TTL is 15 minutes
        cutoff_time = timezone.now() - timedelta(minutes=15)

        # Find preferences with expired codes
        expired_prefs = CommunicationPreference.objects.filter(
            sms_verification_sent_at__lt=cutoff_time, sms_verification_code__isnull=False
        ).exclude(sms_verification_code="")

        count = expired_prefs.count()

        # Clear codes
        expired_prefs.update(sms_verification_code="", updated_at=timezone.now())

        logger.info(f"Cleaned up {count} expired SMS verification codes")

        return count

    except Exception as e:
        logger.error(f"Error cleaning up SMS codes: {e}", exc_info=True)
        return 0
