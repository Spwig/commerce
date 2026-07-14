"""
Background tasks for migration processing
"""

import logging

from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    name="migration.run_migration_job",
    soft_time_limit=14400,  # 4 hours — raises SoftTimeLimitExceeded
    time_limit=14700,  # 4h 5min — hard kill (SIGKILL)
)
def run_migration_job(self, job_id):
    """
    Execute migration job asynchronously

    Args:
        job_id: UUID of MigrationJob

    This task:
    1. Initializes the appropriate importer (WooCommerce, CSV, etc.)
    2. Runs the import with full transaction support
    3. Updates progress via MigrationJob model
    4. Handles errors and automatic rollback
    """
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

    except MigrationJob.DoesNotExist:
        logger.error(f"Migration job {job_id} not found")
        return {"status": "error", "message": "Job not found"}

    except SoftTimeLimitExceeded:
        logger.warning(f"Migration job {job_id} exceeded soft time limit (4 hours)")

        try:
            job = MigrationJob.objects.get(id=job_id)
            job.status = "failed"
            job.error_summary = (
                "Migration exceeded the 4-hour time limit. "
                "Partial data was imported — you can retry to continue from where it left off."
            )
            job.completed_at = timezone.now()
            job.save()
        except Exception:
            pass

        return {"status": "timeout", "error": "Soft time limit exceeded"}

    except Exception as e:
        logger.error(f"Migration job {job_id} failed: {e}", exc_info=True)

        # Mark job as failed
        try:
            job = MigrationJob.objects.get(id=job_id)
            job.status = "failed"
            job.error_summary = str(e)
            job.completed_at = timezone.now()
            job.save()
        except Exception:
            pass

        return {"status": "failed", "error": str(e)}


@shared_task(name="migration.rollback_migration")
def rollback_migration_task(job_id):
    """
    Rollback migration asynchronously

    Args:
        job_id: UUID of MigrationJob

    Deletes all imported data in reverse dependency order
    within a transaction.
    """
    from migration.models import MigrationJob
    from migration.utils.rollback import rollback_migration

    try:
        job = MigrationJob.objects.get(id=job_id)

        logger.info(f"Starting rollback for migration job {job_id}")

        # Perform rollback
        rollback_migration(job)

        logger.info(f"Migration job {job_id} rolled back successfully")

        return {"status": "rolled_back", "job_id": str(job_id)}

    except MigrationJob.DoesNotExist:
        logger.error(f"Migration job {job_id} not found")
        return {"status": "error", "message": "Job not found"}

    except Exception as e:
        logger.error(f"Rollback failed for job {job_id}: {e}", exc_info=True)

        # Mark rollback as failed
        try:
            job = MigrationJob.objects.get(id=job_id)
            job.status = "rollback_failed"
            job.error_summary = f"Rollback failed: {str(e)}"
            job.save()
        except Exception:
            pass

        return {"status": "failed", "error": str(e)}


@shared_task(name="migration.cleanup_old_jobs")
def cleanup_old_jobs():
    """
    Cleanup old migration jobs past their rollback deadline

    Runs daily to:
    1. Mark jobs past rollback deadline as can_rollback=False
    2. Delete very old jobs (>90 days) and their logs
    """
    from datetime import timedelta

    from django.utils import timezone

    from migration.models import MigrationJob, MigrationLog

    now = timezone.now()

    # Disable rollback for old jobs
    expired_jobs = MigrationJob.objects.filter(
        can_rollback=True, rollback_deadline__lt=now, status="completed"
    )

    expired_count = expired_jobs.count()
    expired_jobs.update(can_rollback=False)

    logger.info(f"Disabled rollback for {expired_count} expired migration jobs")

    # Delete very old jobs (>90 days)
    cutoff_date = now - timedelta(days=90)
    old_jobs = MigrationJob.objects.filter(created_at__lt=cutoff_date)

    old_count = old_jobs.count()

    # Delete associated logs first
    for job in old_jobs:
        MigrationLog.objects.filter(job=job).delete()

    old_jobs.delete()

    logger.info(f"Deleted {old_count} migration jobs older than 90 days")

    return {"expired_rollback_disabled": expired_count, "old_jobs_deleted": old_count}
