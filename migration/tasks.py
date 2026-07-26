"""
Background tasks for migration processing
"""

import logging

from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded
from django.utils import timezone

logger = logging.getLogger(__name__)

# 4 hours — raises SoftTimeLimitExceeded, giving the task a chance to record why.
MIGRATION_SOFT_TIME_LIMIT = 14400
# 4h 5min — hard kill (SIGKILL). Past this the worker cannot write to the job at all.
MIGRATION_HARD_TIME_LIMIT = 14700

# A rollback is bounded by the size of what one import created, so it is far
# shorter than an import. Bounding it matters: an unbounded rollback that hangs
# leaves the job in "rolling_back", which nothing else can act on.
ROLLBACK_SOFT_TIME_LIMIT = 3600
ROLLBACK_HARD_TIME_LIMIT = 3900

# How long a job may sit without a write before the reaper treats it as dead.
#
# Deliberately longer than the hard time limit of the task itself. The executors
# write the MigrationJob row only at *step* boundaries — within a step they touch
# MigrationStep rows instead — so a single large products step legitimately goes
# for hours without updating the job. Anything shorter than the maximum lifetime
# of a run would reap healthy imports, and once the completion write becomes
# conditional that false reap becomes a permanent wrong terminal state rather
# than something the final save silently undoes.
#
# Past this point the worker has been SIGKILLed by Celery and provably cannot
# write again, so failing the job is safe. Phase 2 adds a heartbeat at batch
# boundaries, after which this can come down substantially.
STALLED_JOB_TIMEOUT_SECONDS = MIGRATION_HARD_TIME_LIMIT + 900


def _record_failure(job_id, reason):
    """Mark an import failed and, if the merchant opted in, undo it.

    Auto-rollback is dispatched as a separate task rather than run here. The
    failing task may have seconds left before Celery kills it — nowhere near
    enough to unwind a large import — and a rollback aborted half way is worse
    than one that never started.
    """
    from migration.models import MigrationJob

    try:
        job = MigrationJob.objects.get(id=job_id)
    except MigrationJob.DoesNotExist:
        return

    auto = job.auto_rollback_on_failure

    if auto:
        reason = (
            f"{reason} Because you asked for it, Spwig is now removing what "
            "this import added — check back shortly to see the result."
        )

    job.status = "failed"
    job.error_summary = reason
    job.completed_at = timezone.now()
    job.save(update_fields=["status", "error_summary", "completed_at"])

    if not auto:
        return

    # Claim the job before queueing, so a concurrent manual rollback cannot
    # start a second one.
    claimed = MigrationJob.objects.filter(pk=job.pk, status="failed").update(
        status="rolling_back", updated_at=timezone.now()
    )
    if not claimed:
        return

    try:
        rollback_migration_task.delay(str(job.pk))
        logger.info("Queued automatic rollback for failed migration job %s", job.pk)
    except Exception:
        logger.exception("Could not queue automatic rollback for job %s", job.pk)
        MigrationJob.objects.filter(pk=job.pk, status="rolling_back").update(
            status="failed",
            error_summary=(
                "This import stopped because of an unexpected error, and Spwig "
                "could not start the automatic removal. The items imported so "
                "far are still in your store — you can roll the import back "
                "yourself from the Migrations list."
            ),
        )


@shared_task(
    bind=True,
    name="migration.run_migration_job",
    soft_time_limit=MIGRATION_SOFT_TIME_LIMIT,
    time_limit=MIGRATION_HARD_TIME_LIMIT,
)
def run_migration_job(self, job_id):
    """
    Execute migration job asynchronously

    Args:
        job_id: UUID of MigrationJob

    This task:
    1. Initializes the appropriate importer (WooCommerce, Shopify, Magento, CSV)
    2. Runs the import, committing each item as it is imported
    3. Updates progress via the MigrationJob model
    4. Records failures on the job

    There is no enclosing transaction. If the import fails part way through,
    everything imported up to that point stays in the store. It is removed
    afterwards by a rollback — automatically when the job opted in via
    auto_rollback_on_failure, otherwise when the merchant asks for one.
    """
    from migration.importers.cancellation import MigrationCancelled
    from migration.importers.executor import ImportExecutor
    from migration.models import MigrationJob

    try:
        job = MigrationJob.objects.get(id=job_id)

        logger.info(f"Starting migration job {job_id} ({job.get_platform_display()})")

        # Use platform-specific executor
        if job.platform == "shopify":
            from migration.importers.shopify_executor import ShopifyImportExecutor

            executor = ShopifyImportExecutor(job)
        elif job.platform == "magento":
            from migration.importers.magento_executor import MagentoImportExecutor

            executor = MagentoImportExecutor(job)
        else:
            executor = ImportExecutor(job)
        executor.execute()

        logger.info(f"Migration job {job_id} completed successfully")

        return {
            "status": "completed",
            "job_id": str(job_id),
            "imported": job.total_imported,
            "skipped": job.total_skipped,
            "failed": job.total_failed,
        }

    except MigrationCancelled:
        # A deliberate stop, not a failure. The executor has already recorded
        # the outcome on the job and its steps; the task just reports it.
        logger.info(f"Migration job {job_id} was cancelled")
        return {"status": "cancelled", "job_id": str(job_id)}

    except MigrationJob.DoesNotExist:
        logger.error(f"Migration job {job_id} not found")
        return {"status": "error", "message": "Job not found"}

    except SoftTimeLimitExceeded:
        logger.warning(f"Migration job {job_id} exceeded soft time limit (4 hours)")

        try:
            _record_failure(
                job_id,
                "This import ran for longer than four hours and was stopped. "
                "The items imported so far are still in your store. Running the "
                "import again starts from the beginning and skips items that have "
                "already been imported.",
            )
        except Exception:
            logger.exception("Could not record the timeout for job %s", job_id)

        return {"status": "timeout", "error": "Soft time limit exceeded"}

    except Exception as e:
        logger.error(f"Migration job {job_id} failed: {e}", exc_info=True)

        # Mark job as failed. Exception text can carry table and column names;
        # the full detail is already in the log above.
        try:
            _record_failure(
                job_id,
                "This import stopped because of an unexpected error. The items "
                "imported so far are still in your store. Running the import "
                "again starts from the beginning and skips items that have "
                "already been imported.",
            )
        except Exception:
            logger.exception("Could not record the failure for job %s", job_id)

        return {"status": "failed", "error": str(e)}


@shared_task(
    name="migration.rollback_migration",
    # acks_late so the message is only acknowledged once the rollback finishes.
    # A worker killed mid-rollback (OOM, deploy) would otherwise lose the task
    # with the job already committed to "rolling_back", leaving it stranded in a
    # state nothing can act on.
    acks_late=True,
    soft_time_limit=ROLLBACK_SOFT_TIME_LIMIT,
    time_limit=ROLLBACK_HARD_TIME_LIMIT,
)
def rollback_migration_task(job_id):
    """
    Rollback migration asynchronously

    Args:
        job_id: UUID of MigrationJob

    Deletes all imported data in reverse dependency order
    within a transaction.
    """
    from migration.models import MigrationJob
    from migration.utils.rollback import RollbackRefused, rollback_migration

    try:
        job = MigrationJob.objects.get(id=job_id)

        logger.info(f"Starting rollback for migration job {job_id}")

        report = rollback_migration(job)

        # Keep the report on the job so the merchant can see what was removed
        # and — just as important — what was kept and why.
        config = job.connection_config or {}
        config["rollback_report"] = report
        job.connection_config = config
        job.save(update_fields=["connection_config"])

        logger.info(f"Migration job {job_id} rolled back: {report}")

        return {"status": "rolled_back", "job_id": str(job_id), "report": report}

    except MigrationJob.DoesNotExist:
        logger.error(f"Migration job {job_id} not found")
        return {"status": "error", "message": "Job not found"}

    except Exception as e:
        logger.error(f"Rollback failed for job {job_id}: {e}", exc_info=True)

        # Mark rollback as failed
        try:
            job = MigrationJob.objects.get(id=job_id)
            job.status = "rollback_failed"
            # RollbackRefused messages are written for merchants and are safe to
            # show; anything else is an internal error and is only logged.
            job.error_summary = (
                str(e)
                if isinstance(e, RollbackRefused)
                else (
                    "The rollback stopped because of an unexpected error. Some "
                    "of the imported data may still be in your store. You can "
                    "start the rollback again."
                )
            )
            job.save(update_fields=["status", "error_summary"])
        except Exception:
            pass

        return {"status": "failed", "error": str(e)}


@shared_task(name="migration.reap_stalled_migrations")
def reap_stalled_migrations():
    """Fail jobs whose worker died, so the merchant has an action again.

    A worker killed by the hard time limit, an OOM or a deploy leaves the job
    marked "running" (or "rolling_back") for ever. Every admin action is gated
    on status — cancel wants running, retry wants failed, rollback wants
    completed — so such a job offers the merchant nothing at all.

    Staleness is judged by the updated_at heartbeat, which every progress write
    refreshes, rather than by elapsed time since the job started. started_at is
    stamped when the task is *enqueued*, so a long queue backlog would make a
    perfectly healthy import look expired.
    """
    from datetime import timedelta

    from django.utils import timezone

    from migration.models import MigrationJob

    cutoff = timezone.now() - timedelta(seconds=STALLED_JOB_TIMEOUT_SECONDS)
    reaped = {}

    # A job the operator asked to stop, whose worker then died before it reached
    # a checkpoint, ends as "cancelled" rather than "failed". Otherwise the
    # reaper erases the very distinction cooperative cancellation exists to
    # create, and the merchant is told their import broke when in fact they
    # stopped it.
    cancelled_stalled = MigrationJob.objects.filter(
        status="running", cancel_requested=True, updated_at__lt=cutoff
    )
    cancelled_count = cancelled_stalled.count()
    if cancelled_count:
        cancelled_stalled.update(
            status="cancelled",
            completed_at=timezone.now(),
            updated_at=timezone.now(),
            error_summary=(
                "This import was cancelled. Anything imported before it stopped "
                "is still in your store."
            ),
        )
        logger.info("Reaped %d cancelled migration job(s)", cancelled_count)
    reaped["cancelled"] = cancelled_count

    for status, next_status, message in (
        (
            "running",
            "failed",
            "This import stopped unexpectedly — its background worker is no "
            "longer running. Anything imported before it stopped is still in "
            "your store. Run the import again to continue; items already "
            "imported will be skipped.",
        ),
        (
            "rolling_back",
            "rollback_failed",
            "This rollback stopped unexpectedly — its background worker is no "
            "longer running. Some data may still remain. You can start the "
            "rollback again.",
        ),
    ):
        stalled = MigrationJob.objects.filter(status=status, updated_at__lt=cutoff)
        count = stalled.count()
        if count:
            # Conditional update: re-check the status so a worker that came back
            # to life between the query and the write is not stomped.
            # Note: a queryset .update() bypasses Model.save(), so the auto_now
            # heartbeat does not fire — set it explicitly.
            stalled.filter(status=status).update(
                status=next_status,
                error_summary=message,
                completed_at=timezone.now(),
                updated_at=timezone.now(),
            )
            logger.warning("Reaped %d migration job(s) stalled in '%s'", count, status)
        reaped[status] = count

    return reaped


@shared_task(name="migration.cleanup_migration_history")
def cleanup_migration_history():
    """Trim migration history without destroying provenance.

    Two things this deliberately does NOT do, both of which the previous
    version did and which is why it was never scheduled:

    * It never deletes MigrationJob rows. Every imported product, order,
      customer and media asset points at its job with on_delete=SET_NULL, so
      removing job rows silently strips that provenance store-wide and makes
      rollback and audit impossible. The rows are tiny; keeping them is cheap.
    * It never touches a job that is still running or rolling back.

    What it does trim is the bulky per-item history — logs, step records and
    quarantined items — for jobs that finished long ago.
    """
    from datetime import timedelta

    from django.conf import settings
    from django.utils import timezone

    from migration.models import MigrationJob, MigrationLog, MigrationStagedItem, MigrationStep

    now = timezone.now()

    # Close the rollback window on jobs that have one and have passed it. Jobs
    # with no deadline never expire, which is the default.
    expired = MigrationJob.objects.filter(
        can_rollback=True,
        rollback_deadline__isnull=False,
        rollback_deadline__lt=now,
    )
    expired_count = expired.count()
    if expired_count:
        expired.update(can_rollback=False, updated_at=now)
        logger.info("Closed the rollback window on %d migration job(s)", expired_count)

    retention_days = getattr(settings, "MIGRATION_LOG_RETENTION_DAYS", 90)
    cutoff = now - timedelta(days=retention_days)

    # Only finished jobs. A long-running import must keep its live log.
    stale_jobs = MigrationJob.objects.filter(
        created_at__lt=cutoff,
        status__in=["completed", "failed", "cancelled", "rolled_back", "rollback_failed"],
    )

    # Single filtered deletes rather than a per-job Python loop.
    logs_deleted, _ = MigrationLog.objects.filter(job__in=stale_jobs).delete()
    steps_deleted, _ = MigrationStep.objects.filter(job__in=stale_jobs).delete()
    staged_deleted, _ = MigrationStagedItem.objects.filter(job__in=stale_jobs).delete()

    logger.info(
        "Trimmed migration history older than %d days: %d log(s), %d step(s), %d staged item(s). "
        "Job records kept.",
        retention_days,
        logs_deleted,
        steps_deleted,
        staged_deleted,
    )

    return {
        "rollback_windows_closed": expired_count,
        "logs_deleted": logs_deleted,
        "steps_deleted": steps_deleted,
        "staged_items_deleted": staged_deleted,
        "jobs_deleted": 0,
    }
