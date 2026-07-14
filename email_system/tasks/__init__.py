"""
Email System Celery Tasks

Async tasks for scheduled email processing and other email system operations.
"""

import logging

from celery import shared_task
from django.db import transaction
from django.utils import timezone

logger = logging.getLogger("email_system")


@shared_task
def process_scheduled_emails():
    """Process pending scheduled emails that are due for sending.

    Runs every 5 minutes via Celery Beat (HQ only). Picks up ScheduledEmail
    records where status='pending' and scheduled_for <= now, then sends each
    via EmailSendingService.send_template_email().
    """
    from email_system.models import ScheduledEmail
    from email_system.services.email_sender import EmailSendingService

    now = timezone.now()

    # Collect IDs under a lock so concurrent workers don't pick the same rows,
    # then process outside the transaction to avoid long-held locks.
    with transaction.atomic():
        pending_ids = list(
            ScheduledEmail.objects.filter(
                status="pending",
                scheduled_for__lte=now,
            )
            .select_for_update(skip_locked=True)
            .values_list("id", flat=True)
        )
        if pending_ids:
            ScheduledEmail.objects.filter(id__in=pending_ids).update(
                status="sent",  # Claim them; failures get corrected below
            )

    sent = 0
    failed = 0

    for scheduled in ScheduledEmail.objects.filter(id__in=pending_ids):
        try:
            outbox = EmailSendingService.send_template_email(
                to_email=scheduled.recipient_email,
                template_type=scheduled.template_type,
                context=scheduled.context_json,
            )
            if outbox and outbox.status == "queued":
                EmailSendingService.send_email(str(outbox.id))

            scheduled.sent_at = timezone.now()
            scheduled.save(update_fields=["status", "sent_at"])
            sent += 1

        except Exception as e:
            logger.error(
                "Failed to send scheduled email %d (%s → %s): %s",
                scheduled.id,
                scheduled.template_type,
                scheduled.recipient_email,
                e,
            )
            scheduled.status = "failed"
            scheduled.error_message = str(e)[:1000]
            scheduled.save(update_fields=["status", "error_message"])
            failed += 1

    if sent or failed:
        logger.info(
            "Processed scheduled emails: %d sent, %d failed",
            sent,
            failed,
        )
