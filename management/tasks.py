"""
Celery tasks for system monitoring and management operations
"""

import logging
from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from core.celery_utils import BackgroundDBTask

from .models import SystemMetrics
from .utils import SystemMonitor

logger = logging.getLogger(__name__)


@shared_task(name="management.collect_system_metrics", base=BackgroundDBTask, ignore_result=True)
def collect_system_metrics():
    """
    Periodic task to collect system metrics
    Should be run every 5-15 minutes via Celery Beat
    """
    try:
        metrics = SystemMonitor.get_system_metrics()
        SystemMetrics.objects.create(**metrics)
        logger.info("System metrics collected successfully")
        return {"success": True, "timestamp": timezone.now().isoformat()}
    except Exception as e:
        logger.error(f"Failed to collect system metrics: {e}")
        return {"success": False, "error": str(e)}


@shared_task(name="management.cleanup_old_metrics", base=BackgroundDBTask, ignore_result=True)
def cleanup_old_metrics(days=30):
    """
    Clean up old system metrics to prevent database bloat
    Keeps the last 30 days of metrics by default
    """
    try:
        cutoff_date = timezone.now() - timedelta(days=days)
        deleted_count = SystemMetrics.objects.filter(timestamp__lt=cutoff_date).delete()[0]
        logger.info(f"Cleaned up {deleted_count} old metric records")
        return {"success": True, "deleted_count": deleted_count}
    except Exception as e:
        logger.error(f"Failed to cleanup old metrics: {e}")
        return {"success": False, "error": str(e)}


@shared_task(name="management.generate_metrics_report", base=BackgroundDBTask)
def generate_metrics_report():
    """
    Generate a summary report of system metrics
    Can be used for daily/weekly reports
    """
    try:
        from django.db.models import Avg, Max, Min

        # Get metrics from last 24 hours
        since = timezone.now() - timedelta(hours=24)
        metrics = SystemMetrics.objects.filter(timestamp__gte=since)

        if not metrics.exists():
            return {"success": False, "message": "No metrics data available"}

        report = {
            "period": "Last 24 hours",
            "timestamp": timezone.now().isoformat(),
            "cpu": {
                "avg": metrics.aggregate(Avg("cpu_percent"))["cpu_percent__avg"],
                "max": metrics.aggregate(Max("cpu_percent"))["cpu_percent__max"],
                "min": metrics.aggregate(Min("cpu_percent"))["cpu_percent__min"],
            },
            "memory": {
                "avg": metrics.aggregate(Avg("memory_percent"))["memory_percent__avg"],
                "max": metrics.aggregate(Max("memory_percent"))["memory_percent__max"],
                "min": metrics.aggregate(Min("memory_percent"))["memory_percent__min"],
            },
            "disk": {
                "avg": metrics.aggregate(Avg("disk_percent"))["disk_percent__avg"],
                "max": metrics.aggregate(Max("disk_percent"))["disk_percent__max"],
                "min": metrics.aggregate(Min("disk_percent"))["disk_percent__min"],
            },
            "sessions": {
                "avg": metrics.aggregate(Avg("active_sessions"))["active_sessions__avg"],
                "max": metrics.aggregate(Max("active_sessions"))["active_sessions__max"],
            },
        }

        logger.info("Generated metrics report")
        return {"success": True, "report": report}
    except Exception as e:
        logger.error(f"Failed to generate metrics report: {e}")
        return {"success": False, "error": str(e)}


# =============================================================================
# Deployment Dashboard Tasks
# =============================================================================


@shared_task(name="management.collect_system_status", base=BackgroundDBTask, ignore_result=True)
def collect_system_status():
    """
    Periodic task to collect system status (DB, Redis, Celery, SSL, disk).
    Updates the SystemStatus model for dashboard display.
    Should be run every 5 minutes via Celery Beat.
    """
    try:
        from .services import SystemStatusService

        # Collect all status
        status_data = SystemStatusService.collect_all_status()

        # Update the model
        SystemStatusService.update_system_status_model(status_data)

        logger.info("System status collected and cached")
        return {"success": True, "timestamp": timezone.now().isoformat()}
    except Exception as e:
        logger.error(f"Failed to collect system status: {e}")
        return {"success": False, "error": str(e)}


@shared_task(bind=True, name="management.run_full_backup", soft_time_limit=1800, time_limit=2000)
def run_full_backup(self, backup_id, backup_type="full", encrypt=False, destination_ids=None):
    """
    Execute a full system backup via backup.sh script.

    After backup completes, dispatches upload tasks for any specified
    remote storage destinations.

    Args:
        backup_id: ID of the DeploymentBackup record
        backup_type: 'full', 'db', 'media', or 'config'
        encrypt: Whether to encrypt the backup
        destination_ids: Optional list of RemoteStorageDestination UUIDs to upload to
    """
    import os
    import subprocess

    from django.conf import settings

    from .models import BackupRemoteUpload, DeploymentBackup

    try:
        backup = DeploymentBackup.objects.get(pk=backup_id)
        backup.status = "running"
        backup.task_id = self.request.id
        backup.started_at = timezone.now()
        backup.save(update_fields=["status", "task_id", "started_at"])

        # Build command
        script_path = os.path.join(settings.BASE_DIR, "deploy", "scripts", "backup.sh")

        if not os.path.exists(script_path):
            raise FileNotFoundError(f"Backup script not found: {script_path}")

        cmd = [script_path, "--type", backup_type, "--quiet"]

        if encrypt:
            cmd.append("--encrypt")

        # Update progress
        backup.current_step = "Starting backup..."
        backup.progress_percent = 10
        backup.save(update_fields=["current_step", "progress_percent"])

        # Execute script
        env = os.environ.copy()
        env["SPWIG_INSTALL_DIR"] = str(settings.BASE_DIR)

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=1700,  # Just under soft_time_limit
            env=env,
        )

        if result.returncode != 0:
            raise Exception(f"Backup script failed: {result.stderr}")

        # Parse output for BACKUP_PATH and BACKUP_SIZE
        backup_path = None
        backup_size = None

        for line in result.stdout.strip().split("\n"):
            if line.startswith("BACKUP_PATH="):
                backup_path = line.split("=", 1)[1]
            elif line.startswith("BACKUP_SIZE="):
                try:
                    backup_size = int(line.split("=", 1)[1])
                except ValueError:
                    pass

        # Update backup record
        backup.status = "completed"
        backup.completed_at = timezone.now()
        backup.progress_percent = 100
        backup.current_step = "Completed"
        if backup_path:
            backup.local_path = backup_path
        if backup_size:
            backup.file_size = backup_size
        backup.save()

        # Dispatch remote uploads for any specified destinations
        if destination_ids and backup_path:
            from .models import RemoteStorageDestination

            for dest_id in destination_ids:
                try:
                    dest = RemoteStorageDestination.objects.get(pk=dest_id, is_active=True)
                    upload, created = BackupRemoteUpload.objects.get_or_create(
                        backup=backup,
                        destination=dest,
                        defaults={"status": "pending"},
                    )
                    if created:
                        upload_backup_to_remote.delay(str(upload.pk))
                except RemoteStorageDestination.DoesNotExist:
                    logger.warning(f"Destination {dest_id} not found, skipping upload")

        logger.info(f"Backup {backup_id} completed successfully")
        return {"success": True, "backup_id": backup_id, "path": backup_path}

    except DeploymentBackup.DoesNotExist:
        logger.error(f"Backup record {backup_id} not found")
        return {"success": False, "error": "Backup record not found"}

    except subprocess.TimeoutExpired:
        backup.status = "failed"
        backup.error_message = "Backup timed out"
        backup.save(update_fields=["status", "error_message"])
        logger.error(f"Backup {backup_id} timed out")
        return {"success": False, "error": "Backup timed out"}

    except Exception as e:
        if "backup" in locals():
            backup.status = "failed"
            backup.error_message = str(e)
            backup.save(update_fields=["status", "error_message"])
        logger.error(f"Backup {backup_id} failed: {e}")
        return {"success": False, "error": str(e)}


@shared_task(bind=True, name="management.run_restore", soft_time_limit=3600, time_limit=3800)
def run_restore(self, restore_id):
    """
    Execute a system restore via restore.sh script.
    Creates a safety backup before restoring.

    Args:
        restore_id: ID of the SystemRestore record
    """
    import os
    import subprocess

    from django.conf import settings

    from .models import DeploymentBackup, SystemRestore

    try:
        restore = SystemRestore.objects.get(pk=restore_id)
        restore.status = "backup"
        restore.task_id = self.request.id
        restore.started_at = timezone.now()
        restore.current_step = "Creating safety backup..."
        restore.progress_percent = 5
        restore.save()

        # Create safety backup first
        safety_backup = DeploymentBackup.objects.create(
            name=f"Pre-restore safety backup {timezone.now().strftime('%Y%m%d_%H%M%S')}",
            backup_type="full",
            status="pending",
            created_by=restore.created_by,
        )

        # Run safety backup
        backup_result = run_full_backup.apply(args=[safety_backup.id, "full", False])

        if not backup_result.get("success"):
            raise Exception(f"Safety backup failed: {backup_result.get('error')}")

        safety_backup.refresh_from_db()
        restore.pre_restore_backup = safety_backup
        restore.status = "restoring"
        restore.current_step = "Restoring from backup..."
        restore.progress_percent = 30
        restore.save()

        # Build restore command
        script_path = os.path.join(settings.BASE_DIR, "deploy", "scripts", "restore.sh")

        if not os.path.exists(script_path):
            raise FileNotFoundError(f"Restore script not found: {script_path}")

        source_backup = restore.source_backup
        backup_path = source_backup.local_path

        # If local file doesn't exist, try downloading from remote storage
        if not backup_path or not os.path.exists(backup_path):
            from .models import BackupRemoteUpload
            from .storage_providers.registry import StorageProviderRegistry

            remote_upload = (
                BackupRemoteUpload.objects.filter(
                    backup=source_backup,
                    status="completed",
                )
                .select_related("destination")
                .first()
            )

            if not remote_upload:
                raise Exception("No backup file available — not on local disk or remote storage")

            restore.status = "downloading"
            restore.current_step = f"Downloading from {remote_upload.destination.name}..."
            restore.progress_percent = 15
            restore.save()

            provider = StorageProviderRegistry.create_from_destination(remote_upload.destination)

            # Download to backups directory
            backup_dir = os.path.join(settings.BASE_DIR, "backups")
            os.makedirs(backup_dir, exist_ok=True)

            # Determine filename: use original local_path if available,
            # otherwise remote_path (Google Drive uses file IDs as remote_path
            # which have no extension, so fall back to a safe name)
            if backup_path:
                local_filename = os.path.basename(backup_path)
            else:
                local_filename = os.path.basename(remote_upload.remote_path)
                if "." not in local_filename:
                    local_filename = f"backup_{source_backup.pk}.tar.gz"

            download_path = os.path.join(backup_dir, local_filename)

            def progress_cb(downloaded, total):
                if total > 0:
                    pct = int((downloaded / total) * 15) + 15  # 15-30% range
                    restore.progress_percent = pct
                    restore.save(update_fields=["progress_percent"])

            success = provider.download_file(
                remote_path=remote_upload.remote_path,
                local_path=download_path,
                progress_callback=progress_cb,
            )

            if not success:
                raise Exception(f"Failed to download backup from {remote_upload.destination.name}")

            backup_path = download_path
            source_backup.local_path = download_path
            source_backup.save(update_fields=["local_path"])

            restore.status = "restoring"
            restore.current_step = "Restoring from backup..."
            restore.progress_percent = 30
            restore.save()

        cmd = [script_path, backup_path, "-y"]

        if restore.skip_database:
            cmd.append("--skip-db")
        if restore.skip_media:
            cmd.append("--skip-media")
        if restore.skip_config:
            cmd.append("--skip-config")

        # Execute restore
        env = os.environ.copy()
        env["SPWIG_INSTALL_DIR"] = str(settings.BASE_DIR)

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=3500, env=env)

        if result.returncode != 0:
            raise Exception(f"Restore script failed: {result.stderr}")

        # Update restore record
        restore.status = "completed"
        restore.completed_at = timezone.now()
        restore.progress_percent = 100
        restore.current_step = "Restore completed"
        restore.save()

        logger.info(f"Restore {restore_id} completed successfully")
        return {"success": True, "restore_id": restore_id}

    except SystemRestore.DoesNotExist:
        logger.error(f"Restore record {restore_id} not found")
        return {"success": False, "error": "Restore record not found"}

    except Exception as e:
        if "restore" in locals():
            restore.status = "failed"
            restore.error_message = str(e)
            restore.save(update_fields=["status", "error_message"])
        logger.error(f"Restore {restore_id} failed: {e}")
        return {"success": False, "error": str(e)}


@shared_task(bind=True, name="management.run_upgrade", soft_time_limit=1800, time_limit=2000)
def run_upgrade(self, upgrade_id, target_version):
    """
    Execute a system upgrade via the Upgrader Orchestrator API.
    The orchestrator handles backup, container management, and rollback.

    Args:
        upgrade_id: ID of the SystemUpgrade record
        target_version: Version to upgrade to
    """
    import time

    import requests
    from django.conf import settings

    from .models import SystemUpgrade

    # Upgrader service URL (internal Docker network)
    UPGRADER_URL = getattr(settings, "UPGRADER_URL", "http://upgrader:8080")
    FLEET_INSTANCE = getattr(settings, "FLEET_INSTANCE_NAME", "")
    _params = {"instance": FLEET_INSTANCE} if FLEET_INSTANCE else {}

    try:
        upgrade = SystemUpgrade.objects.get(pk=upgrade_id)
        upgrade.status = "preflight"
        upgrade.task_id = self.request.id
        upgrade.started_at = timezone.now()
        upgrade.current_step = "Running preflight checks..."
        upgrade.progress_percent = 5
        upgrade.save()

        # Step 1: Run preflight checks via orchestrator
        try:
            preflight_response = requests.get(
                f"{UPGRADER_URL}/preflight", params=_params, timeout=60
            )
            preflight_data = preflight_response.json()

            upgrade.preflight_results = preflight_data.get("checks", {})
            upgrade.save(update_fields=["preflight_results"])

            if not preflight_data.get("all_passed"):
                failed_checks = [
                    k for k, v in preflight_data.get("checks", {}).items() if not v.get("passed")
                ]
                raise Exception(f"Preflight checks failed: {', '.join(failed_checks)}")

        except requests.RequestException as e:
            raise Exception(f"Could not connect to upgrader service: {e}")

        # Step 2: Start the upgrade via orchestrator
        upgrade.status = "upgrading"
        upgrade.current_step = "Starting upgrade..."
        upgrade.progress_percent = 10
        upgrade.save(update_fields=["status", "current_step", "progress_percent"])

        try:
            upgrade_payload = {
                "target_version": target_version,
                "upgrade_id": upgrade_id,
                "create_backup": True,
            }
            if FLEET_INSTANCE:
                upgrade_payload["instance"] = FLEET_INSTANCE

            start_response = requests.post(
                f"{UPGRADER_URL}/upgrade/start", json=upgrade_payload, timeout=30
            )
            start_data = start_response.json()

            if not start_data.get("success"):
                raise Exception(start_data.get("error", "Failed to start upgrade"))

        except requests.RequestException as e:
            raise Exception(f"Could not start upgrade: {e}")

        # Step 3: Poll for progress
        poll_interval = 5  # seconds
        max_polls = 360  # 30 minutes max
        polls = 0
        was_in_progress = False

        while polls < max_polls:
            time.sleep(poll_interval)
            polls += 1

            try:
                status_response = requests.get(f"{UPGRADER_URL}/status", params=_params, timeout=10)
                status_data = status_response.json()
                operation = status_data.get("operation", {})

                # Update progress
                step = operation.get("step", "Upgrading...")
                progress = operation.get("progress", 0)
                status = operation.get("status", "in_progress")

                # Detect upgrader crash: was in_progress but now idle without
                # completion/failure (indicates OOM kill or unexpected restart)
                if (
                    was_in_progress
                    and status == "idle"
                    and not operation.get("completed")
                    and not operation.get("failed")
                ):
                    error_msg = (
                        "Upgrade service restarted unexpectedly during upgrade. "
                        "This may indicate insufficient memory for the database backup. "
                        "Please check system resources and try again."
                    )
                    upgrade.status = "failed"
                    upgrade.error_message = error_msg
                    upgrade.save(update_fields=["status", "error_message"])
                    logger.error(
                        f"Upgrade {upgrade_id} failed: upgrader crash detected (in_progress -> idle)"
                    )
                    return {"success": False, "error": error_msg}

                if status == "in_progress":
                    was_in_progress = True

                upgrade.current_step = step
                upgrade.progress_percent = progress
                upgrade.save(update_fields=["current_step", "progress_percent"])

                # Check for completion
                if operation.get("completed"):
                    upgrade.status = "completed"
                    upgrade.completed_at = timezone.now()
                    upgrade.progress_percent = 100
                    upgrade.current_step = "Upgrade completed"
                    upgrade.save()
                    logger.info(f"Upgrade {upgrade_id} to {target_version} completed successfully")
                    return {"success": True, "upgrade_id": upgrade_id, "version": target_version}

                # Check for failure
                if operation.get("failed"):
                    error_msg = operation.get("error", "Upgrade failed")
                    upgrade.status = "failed"
                    upgrade.error_message = error_msg
                    upgrade.save(update_fields=["status", "error_message"])
                    logger.error(f"Upgrade {upgrade_id} failed: {error_msg}")
                    return {"success": False, "error": error_msg}

                # Check if still in progress
                if status not in ("in_progress", "idle"):
                    break

            except requests.RequestException as e:
                logger.warning(f"Could not get upgrade status: {e}")
                # Continue polling - the upgrade might still be running

        # Timeout
        upgrade.status = "failed"
        upgrade.error_message = "Upgrade timed out waiting for completion"
        upgrade.save(update_fields=["status", "error_message"])
        logger.error(f"Upgrade {upgrade_id} timed out")
        return {"success": False, "error": "Upgrade timed out"}

    except SystemUpgrade.DoesNotExist:
        logger.error(f"Upgrade record {upgrade_id} not found")
        return {"success": False, "error": "Upgrade record not found"}

    except Exception as e:
        if "upgrade" in locals():
            upgrade.status = "failed"
            upgrade.error_message = str(e)
            upgrade.save(update_fields=["status", "error_message"])
        logger.error(f"Upgrade {upgrade_id} failed: {e}")
        return {"success": False, "error": str(e)}


@shared_task(bind=True, name="management.run_rollback", soft_time_limit=1800, time_limit=2000)
def run_rollback(self, upgrade_id, target_version=None, backup_file=None):
    """
    Execute a system rollback via the Upgrader Orchestrator API.

    Args:
        upgrade_id: ID of the SystemUpgrade record to rollback
        target_version: Optional version to rollback to (defaults to previous)
        backup_file: Optional specific backup file to restore
    """
    import time

    import requests
    from django.conf import settings

    from .models import SystemUpgrade

    UPGRADER_URL = getattr(settings, "UPGRADER_URL", "http://upgrader:8080")
    FLEET_INSTANCE = getattr(settings, "FLEET_INSTANCE_NAME", "")
    _params = {"instance": FLEET_INSTANCE} if FLEET_INSTANCE else {}

    try:
        upgrade = SystemUpgrade.objects.get(pk=upgrade_id)
        upgrade.status = "rolling_back"
        upgrade.task_id = self.request.id
        upgrade.current_step = "Initiating rollback..."
        upgrade.progress_percent = 5
        upgrade.save()

        # Start rollback via orchestrator
        try:
            rollback_payload = {
                "target_version": target_version,
                "backup_file": backup_file,
            }
            if FLEET_INSTANCE:
                rollback_payload["instance"] = FLEET_INSTANCE

            start_response = requests.post(
                f"{UPGRADER_URL}/rollback/start", json=rollback_payload, timeout=30
            )
            start_data = start_response.json()

            if not start_data.get("success"):
                raise Exception(start_data.get("error", "Failed to start rollback"))

        except requests.RequestException as e:
            raise Exception(f"Could not start rollback: {e}")

        # Poll for progress
        poll_interval = 5
        max_polls = 360
        polls = 0
        was_in_progress = False

        while polls < max_polls:
            time.sleep(poll_interval)
            polls += 1

            try:
                status_response = requests.get(f"{UPGRADER_URL}/status", params=_params, timeout=10)
                status_data = status_response.json()
                operation = status_data.get("operation", {})

                step = operation.get("step", "Rolling back...")
                progress = operation.get("progress", 0)
                status = operation.get("status", "in_progress")

                # Detect upgrader crash during rollback
                if (
                    was_in_progress
                    and status == "idle"
                    and not operation.get("completed")
                    and not operation.get("failed")
                ):
                    error_msg = "Upgrade service restarted unexpectedly during rollback. Please check system resources and try again."
                    upgrade.status = "failed"
                    upgrade.error_message = error_msg
                    upgrade.save(update_fields=["status", "error_message"])
                    logger.error(
                        f"Rollback {upgrade_id} failed: upgrader crash detected (in_progress -> idle)"
                    )
                    return {"success": False, "error": error_msg}

                if status == "in_progress":
                    was_in_progress = True

                upgrade.current_step = step
                upgrade.progress_percent = progress
                upgrade.save(update_fields=["current_step", "progress_percent"])

                if operation.get("completed"):
                    upgrade.status = "rolled_back"
                    upgrade.completed_at = timezone.now()
                    upgrade.progress_percent = 100
                    upgrade.current_step = "Rollback completed"
                    upgrade.save()
                    logger.info(f"Rollback for upgrade {upgrade_id} completed successfully")
                    return {"success": True, "upgrade_id": upgrade_id, "rolled_back": True}

                if operation.get("failed"):
                    error_msg = operation.get("error", "Rollback failed")
                    upgrade.status = "failed"
                    upgrade.error_message = f"Rollback failed: {error_msg}"
                    upgrade.save(update_fields=["status", "error_message"])
                    logger.error(f"Rollback for upgrade {upgrade_id} failed: {error_msg}")
                    return {"success": False, "error": error_msg}

                if status not in ("in_progress", "idle"):
                    break

            except requests.RequestException as e:
                logger.warning(f"Could not get rollback status: {e}")

        upgrade.status = "failed"
        upgrade.error_message = "Rollback timed out"
        upgrade.save(update_fields=["status", "error_message"])
        logger.error(f"Rollback for upgrade {upgrade_id} timed out")
        return {"success": False, "error": "Rollback timed out"}

    except SystemUpgrade.DoesNotExist:
        logger.error(f"Upgrade record {upgrade_id} not found for rollback")
        return {"success": False, "error": "Upgrade record not found"}

    except Exception as e:
        if "upgrade" in locals():
            upgrade.status = "failed"
            upgrade.error_message = str(e)
            upgrade.save(update_fields=["status", "error_message"])
        logger.error(f"Rollback for upgrade {upgrade_id} failed: {e}")
        return {"success": False, "error": str(e)}


@shared_task(name="management.check_upgrader_health")
def check_upgrader_health():
    """
    Check if the upgrader service is healthy.
    Returns health status for dashboard display.
    """
    import requests
    from django.conf import settings

    UPGRADER_URL = getattr(settings, "UPGRADER_URL", "http://upgrader:8080")

    try:
        response = requests.get(f"{UPGRADER_URL}/health", timeout=10)
        data = response.json()
        return {
            "success": True,
            "healthy": data.get("status") == "healthy",
            "version": data.get("version"),
            "timestamp": data.get("timestamp"),
        }
    except Exception as e:
        logger.warning(f"Upgrader health check failed: {e}")
        return {
            "success": False,
            "healthy": False,
            "error": str(e),
        }


@shared_task(name="management.run_scheduled_backup", ignore_result=True)
def run_scheduled_backup():
    """
    Check if a scheduled backup is due and run it.
    Called every hour by Celery Beat.
    """
    from .models import BackupSchedule, DeploymentBackup

    try:
        # Get the schedule (singleton-like, just get first one)
        schedule = BackupSchedule.objects.first()

        if not schedule or not schedule.is_enabled:
            return {"success": True, "message": "Scheduled backups not enabled"}

        # Check if backup is due
        now = timezone.now()

        if schedule.next_run and now < schedule.next_run:
            return {
                "success": True,
                "message": "Backup not yet due",
                "next_run": schedule.next_run.isoformat(),
            }

        # Create backup record
        backup = DeploymentBackup.objects.create(
            name=f"Scheduled backup {now.strftime('%Y%m%d_%H%M%S')}",
            backup_type=schedule.backup_type,
            status="pending",
            is_encrypted=schedule.encrypt,
        )

        # Collect remote destination IDs from the schedule
        destination_ids = list(
            schedule.remote_destinations.filter(is_active=True).values_list("pk", flat=True)
        )
        # Convert UUIDs to strings for JSON serialization
        destination_ids = [str(d) for d in destination_ids]

        # Run backup
        result = run_full_backup.apply(
            args=[
                backup.id,
                schedule.backup_type,
                schedule.encrypt,
                destination_ids or None,
            ]
        )

        # Update schedule tracking
        schedule.last_run = now
        schedule.last_backup = backup
        schedule.calculate_next_run()
        schedule.save()

        if result.get("success"):
            logger.info(f"Scheduled backup completed: {backup.id}")
            return {"success": True, "backup_id": backup.id}
        else:
            logger.error(f"Scheduled backup failed: {result.get('error')}")
            return {"success": False, "error": result.get("error")}

    except Exception as e:
        logger.error(f"Scheduled backup task failed: {e}")
        return {"success": False, "error": str(e)}


@shared_task(name="management.cleanup_old_backups", base=BackgroundDBTask, ignore_result=True)
def cleanup_old_backups():
    """
    Clean up old backups based on retention policy.
    Runs daily at 4 AM via Celery Beat.
    """
    import os

    from .models import BackupSchedule, DeploymentBackup

    try:
        schedule = BackupSchedule.objects.first()
        retention_days = schedule.retention_days if schedule else 30

        cutoff_date = timezone.now() - timedelta(days=retention_days)

        # Find old backups
        old_backups = DeploymentBackup.objects.filter(
            created_at__lt=cutoff_date,
            status="completed",
        )

        deleted_count = 0
        errors = []

        for backup in old_backups:
            try:
                # Delete local file if exists
                if backup.local_path and os.path.exists(backup.local_path):
                    os.remove(backup.local_path)

                backup.delete()
                deleted_count += 1

            except Exception as e:
                errors.append(f"Failed to delete backup {backup.id}: {e}")
                logger.error(f"Failed to delete backup {backup.id}: {e}")

        logger.info(f"Cleaned up {deleted_count} old backups")
        return {
            "success": len(errors) == 0,
            "deleted_count": deleted_count,
            "errors": errors if errors else None,
        }

    except Exception as e:
        logger.error(f"Backup cleanup failed: {e}")
        return {"success": False, "error": str(e)}


@shared_task(name="management.run_diagnostics", base=BackgroundDBTask)
def run_diagnostics():
    """
    Run system diagnostics via doctor.sh script.
    Returns parsed JSON results.
    """
    import json
    import os
    import subprocess

    from django.conf import settings

    try:
        script_path = os.path.join(settings.BASE_DIR, "deploy", "scripts", "doctor.sh")

        if not os.path.exists(script_path):
            # If script doesn't exist, run basic checks
            from .services import SystemStatusService

            status = SystemStatusService.collect_all_status()
            return {"success": True, "diagnostics": status, "source": "python"}

        cmd = [script_path, "--json"]

        env = os.environ.copy()
        env["SPWIG_INSTALL_DIR"] = str(settings.BASE_DIR)

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60, env=env)

        if result.returncode != 0 and not result.stdout:
            raise Exception(f"Diagnostics failed: {result.stderr}")

        # Parse JSON output
        try:
            diagnostics = json.loads(result.stdout)
        except json.JSONDecodeError:
            diagnostics = {"raw_output": result.stdout}

        return {"success": True, "diagnostics": diagnostics, "source": "script"}

    except Exception as e:
        logger.error(f"Diagnostics failed: {e}")
        return {"success": False, "error": str(e)}


# =============================================================================
# Log Viewer Tasks
# =============================================================================


@shared_task(name="management.collect_docker_logs", ignore_result=True)
def collect_docker_logs():
    """
    Collect recent logs from all Docker containers and store in Redis.
    Runs every 10 seconds via Celery Beat.
    """
    from .models import LogViewerSettings

    try:
        settings_obj = LogViewerSettings.get_instance()

        if not settings_obj.stream_enabled:
            return {"success": True, "skipped": True, "reason": "streaming disabled"}

        from .services.docker_log_service import DockerLogService

        service = DockerLogService()

        total_collected = 0

        for container in DockerLogService.CONTAINER_SERVICES:
            try:
                collected = service.collect_container_logs(container, tail=20)
                total_collected += collected
            except Exception as e:
                logger.debug(f"Could not collect logs from {container}: {e}")

        return {"success": True, "collected": total_collected}

    except Exception as e:
        logger.warning(f"Log collection failed: {e}")
        return {"success": False, "error": str(e)}


@shared_task(name="management.archive_logs_to_db", base=BackgroundDBTask, ignore_result=True)
def archive_logs_to_db():
    """
    Archive logs from Redis to PostgreSQL for long-term storage.
    Runs every 5 minutes via Celery Beat.
    """
    from .models import LogViewerSettings

    try:
        settings_obj = LogViewerSettings.get_instance()
        batch_size = settings_obj.archive_batch_size

        from .services.docker_log_service import DockerLogService

        service = DockerLogService()

        archived_count = service.archive_logs_to_db(batch_size=batch_size)

        logger.info(f"Archived {archived_count} log entries to database")
        return {"success": True, "archived": archived_count}

    except Exception as e:
        logger.error(f"Log archiving failed: {e}")
        return {"success": False, "error": str(e)}


@shared_task(name="management.cleanup_old_logs", base=BackgroundDBTask, ignore_result=True)
def cleanup_old_logs():
    """
    Clean up logs older than the retention period.
    Runs daily at 3 AM via Celery Beat.
    """
    from datetime import timedelta

    from .models import LogEntry, LogViewerSettings

    try:
        settings_obj = LogViewerSettings.get_instance()
        retention_days = settings_obj.db_retention_days

        cutoff = timezone.now() - timedelta(days=retention_days)

        deleted_count, _ = LogEntry.objects.filter(archived_at__lt=cutoff).delete()

        logger.info(
            f"Cleaned up {deleted_count} old log entries (retention: {retention_days} days)"
        )
        return {"success": True, "deleted": deleted_count, "retention_days": retention_days}

    except Exception as e:
        logger.error(f"Log cleanup failed: {e}")
        return {"success": False, "error": str(e)}


@shared_task(
    name="management.upload_backup_to_remote",
    base=BackgroundDBTask,
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    ignore_result=True,
)
def upload_backup_to_remote(self, upload_id):
    """
    Upload a completed backup file to a remote storage destination.
    Each upload runs as an independent task so multiple destinations
    can be uploaded to in parallel.
    """
    import os

    from .models import BackupRemoteUpload

    try:
        upload = BackupRemoteUpload.objects.select_related("backup", "destination").get(
            pk=upload_id
        )
    except BackupRemoteUpload.DoesNotExist:
        logger.error(f"BackupRemoteUpload {upload_id} not found")
        return {"success": False, "error": "Upload record not found"}

    backup = upload.backup
    destination = upload.destination
    local_path = backup.local_path

    # Validate the local backup file exists
    if not local_path or not os.path.isfile(local_path):
        upload.status = "failed"
        upload.error_message = f"Local backup file not found: {local_path}"
        upload.save(update_fields=["status", "error_message", "updated_at"])
        logger.error(f"Upload {upload_id}: local file missing ({local_path})")
        return {"success": False, "error": upload.error_message}

    # Mark as uploading
    upload.status = "uploading"
    upload.started_at = timezone.now()
    upload.task_id = self.request.id or ""
    upload.file_size = os.path.getsize(local_path)
    upload.save(
        update_fields=[
            "status",
            "started_at",
            "task_id",
            "file_size",
            "updated_at",
        ]
    )

    # Build remote path based on provider type
    filename = os.path.basename(local_path)
    if destination.provider_type == "sftp":
        remote_dir = destination.settings.get("remote_directory", "/backups/spwig/").rstrip("/")
        remote_path = f"{remote_dir}/{filename}"
    else:
        prefix = destination.settings.get("prefix", "").strip("/")
        remote_path = f"{prefix}/{filename}" if prefix else filename

    try:
        from payment_providers.utils.encryption import encrypt_credentials

        from .storage_providers.registry import StorageProviderRegistry

        provider = StorageProviderRegistry.create_from_destination(destination)

        # Refresh OAuth tokens if needed (Google Drive, Dropbox)
        # Snapshot before refresh — refresh modifies self.credentials in-place
        creds_before = dict(provider.credentials)
        provider.refresh_credentials_if_needed()
        if provider.credentials != creds_before:
            # Persist refreshed tokens
            destination.credentials_encrypted = encrypt_credentials(provider.credentials)
            destination.save(update_fields=["credentials_encrypted", "updated_at"])

        # Progress callback updates the DB periodically
        last_pct = [0]

        def on_progress(bytes_transferred, total_bytes):
            if total_bytes > 0:
                pct = int(bytes_transferred * 100 / total_bytes)
                # Only write to DB every 5% to avoid excessive queries
                if pct - last_pct[0] >= 5 or pct >= 100:
                    last_pct[0] = pct
                    BackupRemoteUpload.objects.filter(pk=upload_id).update(progress_percent=pct)

        result = provider.upload_file(local_path, remote_path, progress_callback=on_progress)

        if result.success:
            upload.status = "completed"
            upload.remote_path = result.remote_path
            upload.progress_percent = 100
            upload.completed_at = timezone.now()
            upload.save(
                update_fields=[
                    "status",
                    "remote_path",
                    "progress_percent",
                    "completed_at",
                    "updated_at",
                ]
            )

            # Update destination stats
            file_size = upload.file_size or 0
            destination.last_upload_at = timezone.now()
            destination.last_upload_size = file_size
            destination.total_uploads = (destination.total_uploads or 0) + 1
            destination.total_bytes_uploaded = (destination.total_bytes_uploaded or 0) + file_size
            destination.save(
                update_fields=[
                    "last_upload_at",
                    "last_upload_size",
                    "total_uploads",
                    "total_bytes_uploaded",
                    "updated_at",
                ]
            )

            logger.info(
                f"Upload {upload_id}: {filename} → {destination.name} completed ({file_size} bytes)"
            )
            return {"success": True, "upload_id": upload_id, "remote_path": result.remote_path}
        else:
            raise Exception(result.message or "Upload failed")

    except Exception as exc:
        upload.status = "failed"
        upload.error_message = str(exc)[:1000]
        upload.save(update_fields=["status", "error_message", "updated_at"])

        logger.error(f"Upload {upload_id}: failed — {exc}")

        # Retry on transient errors (network issues, timeouts)
        if self.request.retries < self.max_retries:
            raise self.retry(exc=exc)

        return {"success": False, "error": str(exc)}


@shared_task(
    name="management.cleanup_remote_backups",
    base=BackgroundDBTask,
    ignore_result=True,
)
def cleanup_remote_backups():
    """
    Delete old backups from remote destinations based on each destination's
    retention_days setting.  Runs daily via Celery Beat.
    """
    from .models import RemoteStorageDestination

    destinations = RemoteStorageDestination.objects.filter(
        is_active=True,
        retention_days__gt=0,
    )

    results = []
    for dest in destinations:
        try:
            from .storage_providers.registry import StorageProviderRegistry

            provider = StorageProviderRegistry.create_from_destination(dest)

            # Determine prefix from destination settings
            prefix = dest.settings.get("prefix", "") or dest.settings.get("remote_directory", "")
            deleted_count = provider.cleanup_old_files(prefix, dest.retention_days)
            logger.info(f"Remote cleanup: {dest.name} — deleted {deleted_count} old file(s)")
            results.append(
                {
                    "destination": dest.name,
                    "deleted": deleted_count,
                    "success": True,
                }
            )
        except Exception as e:
            logger.error(f"Remote cleanup failed for {dest.name}: {e}")
            results.append(
                {
                    "destination": dest.name,
                    "success": False,
                    "error": str(e),
                }
            )

    return {"success": True, "results": results}
