"""Cooperative cancellation for the migration executors.

An import runs for up to four hours inside a single Celery task. There is no way
to interrupt it from outside without killing the worker mid-write, so stopping
one has to be cooperative: the operator records the request, and the executor
notices it at a safe point and unwinds.
"""

import logging
from datetime import timedelta

from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)


class MigrationCancelled(BaseException):
    """Raised inside an executor when the operator has asked it to stop.

    Deliberately derived from BaseException, not Exception.

    The import loops are full of per-item `except Exception` handlers that
    quarantine the failing row, increment items_failed and carry on — which is
    right for a bad product, and catastrophic for a cancellation. Caught by one
    of those, a stop request would be recorded as a single bogus failed item and
    the import would run for another three hours. BaseException cannot be
    swallowed by them, so the unwind always reaches execute().
    """


def request_cancel(job_id):
    """Ask a running import to stop.

    Written with a queryset update rather than through a model instance: the
    executor holds its own MigrationJob in memory for hours, and an instance
    save from this side would be overwritten by its next progress write.
    """
    from migration.models import MigrationJob

    return MigrationJob.objects.filter(pk=job_id, status="running").update(
        cancel_requested=True, updated_at=timezone.now()
    )


class CancellationMixin:
    """Gives an executor a cancellation checkpoint. Expects `self.job`."""

    def _check_cancelled(self):
        """Stop the import if cancellation was requested; otherwise heartbeat.

        Call this at page or batch boundaries — never inside a per-item
        try/except, and never per item (it costs a query).

        The same call doubles as the worker's heartbeat. The job row is only
        written at step boundaries otherwise, so without this a long-running
        products step looks dead to the stalled-job reaper.
        """
        from migration.models import MigrationJob

        # One query in the common case: bumps the heartbeat and tells us the
        # flag is clear, because a cancelled row will not match the filter.
        alive = MigrationJob.objects.filter(pk=self.job.pk, cancel_requested=False).update(
            updated_at=timezone.now()
        )
        if alive:
            return

        # Either cancelled, or the row is gone. Distinguish, so a deleted job
        # does not masquerade as an operator cancellation.
        if not MigrationJob.objects.filter(pk=self.job.pk).exists():
            raise MigrationCancelled(f"Migration job {self.job.pk} no longer exists")

        logger.info("Migration job %s: cancellation requested, stopping", self.job.pk)
        raise MigrationCancelled(f"Migration job {self.job.pk} was cancelled by an operator")

    def _mark_completed(self):
        """Mark the import finished — but only if it is still ours to finish.

        A conditional update, not an instance save. The executor's job object is
        hours old by this point; writing "completed" from it unconditionally is
        what let a cancelled or deleted job come back to life as a successful
        one.

        cancel_requested is part of the condition, not just status: cancellation
        deliberately leaves the status alone until the worker acknowledges it,
        so filtering on status alone would still let a job the operator stopped
        be written as completed if the run happened to finish first.
        """
        from migration.models import MigrationJob, MigrationStep

        now = timezone.now()
        duration = None
        if self.job.started_at:
            duration = int((now - self.job.started_at).total_seconds())

        # Optional expiry on the rollback window. Unset means it never expires,
        # which is the default — see MIGRATION_ROLLBACK_WINDOW_HOURS.
        window_hours = getattr(settings, "MIGRATION_ROLLBACK_WINDOW_HOURS", None)
        deadline = now + timedelta(hours=window_hours) if window_hours else None

        finished = MigrationJob.objects.filter(
            pk=self.job.pk, status="running", cancel_requested=False
        ).update(
            rollback_deadline=deadline,
            status="completed",
            completed_at=now,
            duration_seconds=duration,
            progress_percent=100,
            updated_at=now,
        )

        if not finished:
            # Someone else decided this job's fate — cancelled, reaped, or
            # deleted. Do not resurrect it, but do not leave its steps spinning
            # either.
            logger.warning(
                "Migration job %s finished but was no longer running; "
                "leaving its final state alone",
                self.job.pk,
            )
            MigrationStep.objects.filter(job=self.job, status="running").update(
                status="cancelled", completed_at=now
            )
            return False

        logger.info("Import completed successfully for job %s", self.job.pk)
        self._update_overall_progress()
        return True

    def _mark_cancelled(self):
        """Record the stop, on the job and on whatever step was in flight.

        Uses a conditional update so a job that was already terminated by
        something else is not overwritten.
        """
        from migration.models import MigrationJob, MigrationStep

        if getattr(self, "current_step", None) is not None:
            MigrationStep.objects.filter(pk=self.current_step.pk, status="running").update(
                status="cancelled", completed_at=timezone.now()
            )

        # Any other step left running belongs to this job too.
        MigrationStep.objects.filter(job=self.job, status="running").update(
            status="cancelled", completed_at=timezone.now()
        )

        MigrationJob.objects.filter(pk=self.job.pk, status="running").update(
            status="cancelled",
            completed_at=timezone.now(),
            updated_at=timezone.now(),
            error_summary=(
                "This import was cancelled. The items imported before it "
                "stopped are still in your store — nothing was removed. You can "
                "roll the import back to remove them, or run it again and it "
                "will skip whatever already came across."
            ),
        )
