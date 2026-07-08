"""
Sync Celery Tasks

Background tasks for settings sync and full migration operations.
"""
import os
import logging
from io import BytesIO
from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded

logger = logging.getLogger(__name__)


@shared_task(bind=True, name='migration.sync.execute_settings_sync', soft_time_limit=3600)
def execute_settings_sync(self, sync_job_id):
    """
    Execute a settings sync job asynchronously.
    Soft time limit: 1 hour.
    """
    from migration.models import SyncJob
    from .orchestrator import SyncOrchestrator

    try:
        job = SyncJob.objects.get(pk=sync_job_id)
    except SyncJob.DoesNotExist:
        logger.error(f"SyncJob {sync_job_id} not found")
        return

    if job.status not in ('pending', 'awaiting_confirmation'):
        logger.warning(f"SyncJob {sync_job_id} is in status '{job.status}', skipping")
        return

    logger.info(f"Starting settings sync job {sync_job_id}")

    try:
        orchestrator = SyncOrchestrator(job)
        result = orchestrator.execute_sync()
        logger.info(
            f"Settings sync {sync_job_id} completed: "
            f"{result['synced']} synced, {result['failed']} failed"
        )
        return result
    except SoftTimeLimitExceeded:
        logger.error(f"Settings sync {sync_job_id} timed out")
        job.refresh_from_db()
        if job.status == 'running':
            job.mark_failed('Sync timed out after 1 hour.')
    except Exception as e:
        logger.error(f"Settings sync {sync_job_id} failed: {e}")
        job.refresh_from_db()
        if job.status == 'running':
            job.mark_failed(str(e))
        raise


@shared_task(bind=True, name='migration.sync.execute_full_migration', soft_time_limit=28800)
def execute_full_migration(self, sync_job_id):
    """
    Execute a full system migration asynchronously.
    Soft time limit: 8 hours.
    """
    from migration.models import SyncJob
    from .full_migration_orchestrator import FullMigrationOrchestrator

    try:
        job = SyncJob.objects.get(pk=sync_job_id)
    except SyncJob.DoesNotExist:
        logger.error(f"SyncJob {sync_job_id} not found")
        return

    if job.status not in ('pending', 'awaiting_confirmation'):
        logger.warning(f"SyncJob {sync_job_id} is in status '{job.status}', skipping")
        return

    logger.info(f"Starting full migration job {sync_job_id}")

    try:
        orchestrator = FullMigrationOrchestrator(job)
        result = orchestrator.execute_migration()
        logger.info(
            f"Full migration {sync_job_id} completed: "
            f"{result['synced']} synced, {result['failed']} failed"
        )
        return result
    except SoftTimeLimitExceeded:
        logger.error(f"Full migration {sync_job_id} timed out")
        job.refresh_from_db()
        if job.status == 'running':
            job.mark_failed('Migration timed out after 8 hours.')
    except Exception as e:
        logger.error(f"Full migration {sync_job_id} failed: {e}")
        job.refresh_from_db()
        if job.status == 'running':
            job.mark_failed(str(e))
        raise


@shared_task(name='migration.sync.transfer_media_batch')
def transfer_media_batch(sync_job_id, asset_ids):
    """
    Transfer a batch of media files from remote to local.
    Used for chunked media transfer during full migration.
    """
    from migration.models import SyncJob
    from .client import SpwigSyncClient
    from .media_transfer import import_media_file

    try:
        job = SyncJob.objects.get(pk=sync_job_id)
    except SyncJob.DoesNotExist:
        logger.error(f"SyncJob {sync_job_id} not found")
        return

    client = SpwigSyncClient(job.connection)
    results = {'transferred': 0, 'failed': 0, 'errors': []}

    for asset_id in asset_ids:
        try:
            # Stream the file from remote
            response = client.stream_media(asset_id)
            if response.status_code != 200:
                results['failed'] += 1
                results['errors'].append(f"Asset {asset_id}: HTTP {response.status_code}")
                continue

            # Get the target path from Content-Disposition header
            content_disp = response.headers.get('Content-Disposition', '')
            if 'filename=' in content_disp:
                raw_filename = content_disp.split('filename=')[1].strip('"')
                # Sanitize to prevent path traversal
                target_path = os.path.join('synced_media', os.path.basename(raw_filename))
            else:
                target_path = f'synced_media/{asset_id}'

            # Stream chunks into a BytesIO buffer to avoid accumulating a list
            buf = BytesIO()
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    buf.write(chunk)
            buf.seek(0)
            file_data = buf.read()
            buf.close()

            # Save locally
            result = import_media_file(
                file_data,
                target_path,
            )

            if result['success']:
                results['transferred'] += 1
            else:
                results['failed'] += 1
                results['errors'].append(f"Asset {asset_id}: {result['error']}")

        except Exception as e:
            results['failed'] += 1
            results['errors'].append(f"Asset {asset_id}: {e}")

    logger.info(
        f"Media batch for job {sync_job_id}: "
        f"{results['transferred']} transferred, {results['failed']} failed"
    )
    return results


@shared_task(name='migration.sync.rollback_sync')
def rollback_sync(sync_job_id):
    """
    Rollback a sync operation using stored snapshot.
    """
    from migration.models import SyncJob
    from .orchestrator import SyncOrchestrator
    from .full_migration_orchestrator import FullMigrationOrchestrator

    try:
        job = SyncJob.objects.get(pk=sync_job_id)
    except SyncJob.DoesNotExist:
        logger.error(f"SyncJob {sync_job_id} not found")
        return

    # Guard: check rollbackable before starting
    if not job.is_rollbackable:
        logger.warning(f"SyncJob {sync_job_id} is not rollbackable (status={job.status})")
        return

    logger.info(f"Rolling back sync job {sync_job_id}")

    try:
        if job.job_type == 'full_migration':
            orchestrator = FullMigrationOrchestrator(job)
        else:
            orchestrator = SyncOrchestrator(job)

        result = orchestrator.rollback()
        logger.info(f"Rollback {sync_job_id} completed: {result}")
        return result
    except ValueError as e:
        # Non-rollbackable state -- don't corrupt the job status
        logger.warning(f"Rollback {sync_job_id} not possible: {e}")
    except Exception as e:
        logger.error(f"Rollback {sync_job_id} failed: {e}")
        job.refresh_from_db()
        if job.status == 'rolling_back':
            job.status = 'failed'
            job.error_summary = f'Rollback failed: {e}'
            job.save(update_fields=['status', 'error_summary'])
        raise
