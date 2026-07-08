"""
Celery tasks for component updates
"""
import logging
import traceback
from celery import shared_task
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task(bind=True, name='component_updates.perform_platform_update',
             soft_time_limit=1800, time_limit=2000)
def perform_platform_update(self, update_id: str):
    """
    Perform a platform update via the Upgrader Orchestrator service.

    Delegates to the same upgrader service used by management.tasks.run_upgrade.
    The orchestrator handles backup, Docker image pulling, container management,
    migrations, health checks, and rollback.

    Args:
        update_id: UUID of the PlatformUpdate record

    Returns:
        Dict with update result
    """
    import requests
    import time
    from django.conf import settings
    from .models import PlatformUpdate
    from .services import PlatformUpdateService, PlatformUpdateError

    UPGRADER_URL = getattr(settings, 'UPGRADER_URL', 'http://upgrader:8080')
    FLEET_INSTANCE = getattr(settings, 'FLEET_INSTANCE_NAME', '')

    try:
        update = PlatformUpdate.objects.get(id=update_id)
    except PlatformUpdate.DoesNotExist:
        logger.error(f"Platform update {update_id} not found")
        return {'status': 'error', 'message': 'Update not found'}

    service = PlatformUpdateService()

    try:
        update.celery_task_id = self.request.id
        update.started_at = timezone.now()
        update.save(update_fields=['celery_task_id', 'started_at'])

        # Report start to update server
        service.report_update_status(
            from_version=update.from_version,
            to_version=update.to_version,
            status='started'
        )

        # Step 1: Preflight checks via orchestrator
        update.status = 'pre_checks'
        update.current_step = 'Running preflight checks...'
        update.progress_percent = 5
        update.add_log_line("Running preflight checks...")
        update.save()

        try:
            _params = {'instance': FLEET_INSTANCE} if FLEET_INSTANCE else {}
            preflight_response = requests.get(
                f'{UPGRADER_URL}/preflight',
                params=_params,
                timeout=60
            )
            preflight_data = preflight_response.json()

            if not preflight_data.get('all_passed'):
                failed_checks = [
                    k for k, v in preflight_data.get('checks', {}).items()
                    if not v.get('passed')
                ]
                raise PlatformUpdateError(
                    f"Preflight checks failed: {', '.join(failed_checks)}"
                )

            update.add_log_line("Preflight checks passed")
        except requests.RequestException as e:
            raise PlatformUpdateError(f"Could not connect to upgrader service: {e}")

        # Step 2: Start upgrade via orchestrator
        update.status = 'deploying'
        update.current_step = 'Starting upgrade...'
        update.progress_percent = 10
        update.add_log_line(f"Starting upgrade to v{update.to_version}...")
        update.save()

        try:
            upgrade_payload = {
                'target_version': update.to_version,
                'upgrade_id': str(update.id),
                'create_backup': True,
            }
            if FLEET_INSTANCE:
                upgrade_payload['instance'] = FLEET_INSTANCE

            start_response = requests.post(
                f'{UPGRADER_URL}/upgrade/start',
                json=upgrade_payload,
                timeout=30
            )
            start_data = start_response.json()

            if not start_data.get('success'):
                raise PlatformUpdateError(
                    start_data.get('error', 'Failed to start upgrade')
                )
        except requests.RequestException as e:
            raise PlatformUpdateError(f"Could not start upgrade: {e}")

        # Step 3: Poll for progress
        poll_interval = 5
        max_polls = 360  # 30 minutes max
        polls = 0
        was_in_progress = False

        while polls < max_polls:
            time.sleep(poll_interval)
            polls += 1

            try:
                status_response = requests.get(
                    f'{UPGRADER_URL}/status',
                    params=_params,
                    timeout=10
                )
                status_data = status_response.json()
                operation = status_data.get('operation', {})

                step = operation.get('step', 'Upgrading...')
                progress = operation.get('progress', 0)
                op_status = operation.get('status', 'in_progress')

                # Detect upgrader crash (was in_progress but now idle unexpectedly)
                if was_in_progress and op_status == 'idle' \
                        and not operation.get('completed') \
                        and not operation.get('failed'):
                    raise PlatformUpdateError(
                        'Upgrade service restarted unexpectedly during upgrade. '
                        'This may indicate insufficient memory. '
                        'Please check system resources and try again.'
                    )

                if op_status == 'in_progress':
                    was_in_progress = True

                update.current_step = step
                update.progress_percent = progress
                update.add_log_line(step)
                update.save(update_fields=['current_step', 'progress_percent'])

                # Check for completion
                if operation.get('completed'):
                    update.mark_completed()
                    update.rollback_available = True
                    update.add_log_line(
                        f"Platform updated successfully to v{update.to_version}"
                    )
                    update.save()

                    service.report_update_status(
                        from_version=update.from_version,
                        to_version=update.to_version,
                        status='completed',
                        duration_seconds=update.duration_seconds,
                        downtime_seconds=update.downtime_seconds or 0
                    )

                    logger.info(
                        f"Platform update completed: "
                        f"v{update.from_version} -> v{update.to_version}"
                    )
                    return {
                        'status': 'success',
                        'from_version': update.from_version,
                        'to_version': update.to_version,
                        'duration_seconds': update.duration_seconds
                    }

                # Check for failure
                if operation.get('failed'):
                    error_msg = operation.get('error', 'Upgrade failed')
                    raise PlatformUpdateError(error_msg)

                if op_status not in ('in_progress', 'idle'):
                    break

            except requests.RequestException as e:
                logger.warning(f"Could not get upgrade status: {e}")
                # Continue polling - the upgrade might still be running

        # Timeout
        raise PlatformUpdateError('Upgrade timed out waiting for completion')

    except PlatformUpdateError as e:
        logger.error(f"Platform update failed: {e}")
        update.mark_failed(
            error_message=str(e),
            error_stage=update.current_step,
            traceback=traceback.format_exc()
        )

        service.report_update_status(
            from_version=update.from_version,
            to_version=update.to_version,
            status='failed',
            duration_seconds=update.duration_seconds,
            error_message=str(e),
            error_stage=update.current_step
        )

        return {'status': 'error', 'message': str(e)}

    except Exception as e:
        logger.exception(f"Unexpected error during platform update: {e}")
        update.mark_failed(
            error_message=str(e),
            error_stage=update.current_step,
            traceback=traceback.format_exc()
        )

        service.report_update_status(
            from_version=update.from_version,
            to_version=update.to_version,
            status='failed',
            duration_seconds=update.duration_seconds,
            error_message=str(e),
            error_stage=update.current_step
        )

        return {'status': 'error', 'message': str(e)}


@shared_task(name='component_updates.refresh_license')
def refresh_license():
    """
    Periodic task to refresh license.json from the update server.

    Runs daily to pick up maintenance changes, entitlement updates,
    and detect license revocations. Updates the local license.json
    file and invalidates the license cache across all workers.

    Returns:
        Dict with refresh result
    """
    from core.license import is_sandbox_mode

    # Skip in sandbox mode
    if is_sandbox_mode():
        logger.debug("License refresh skipped: sandbox mode")
        return {'status': 'skipped', 'reason': 'sandbox_mode'}

    try:
        from .services import UpdateManager
        manager = UpdateManager()
        result = manager.refresh_license()

        if result.get('refreshed'):
            logger.info(
                f"License refreshed successfully — "
                f"changes: {result.get('changes', [])}"
            )
        elif result.get('error'):
            logger.warning(f"License refresh issue: {result.get('error')}")
        else:
            logger.debug("License refresh: no changes")

        return result

    except Exception as e:
        logger.error(f"License refresh task failed: {e}", exc_info=True)
        return {'status': 'error', 'error': str(e)}


@shared_task(name='component_updates.check_platform_updates')
def check_platform_updates():
    """
    Periodic task to check for platform updates.

    This task runs periodically (e.g., daily) to check if a new
    platform version is available.

    Returns:
        Dict with check result
    """
    from .services import PlatformUpdateService, PlatformUpdateError
    from django.core.cache import cache

    try:
        service = PlatformUpdateService()
        result = service.check_for_update()

        # Cache the result for the admin UI
        cache.set('platform_update_available', result, timeout=86400)  # 24 hours

        if result.get('update_available'):
            logger.info(
                f"Platform update available: v{result.get('current_version')} → "
                f"v{result.get('latest_version')}"
            )
        else:
            logger.info(f"Platform is up to date: v{result.get('current_version')}")

        return result

    except PlatformUpdateError as e:
        logger.error(f"Failed to check for platform updates: {e}")
        return {'error': str(e)}
    except Exception as e:
        logger.exception(f"Unexpected error checking platform updates: {e}")
        return {'error': str(e)}


@shared_task(name='component_updates.check_hotfixes')
def check_hotfixes():
    """
    Periodic task to check for available hotfixes.

    Runs every 6 hours to check if a new hotfix is published for
    the current platform version on the update server.

    Returns:
        Dict with check result
    """
    from .services import PlatformUpdateService, PlatformUpdateError

    try:
        service = PlatformUpdateService()
        result = service.check_for_hotfix()

        if result.get('hotfix_available'):
            hotfix = result.get('latest_hotfix', {})
            logger.info(
                f"Hotfix available: v{result.get('current_version')}"
                f"-hf{hotfix.get('hotfix_number')}"
                f"{' (security)' if hotfix.get('security_update') else ''}"
            )
        else:
            logger.info(
                f"No hotfixes available for v{result.get('current_version')}"
            )

        return result

    except PlatformUpdateError as e:
        logger.error(f"Failed to check for hotfixes: {e}")
        return {'error': str(e)}
    except Exception as e:
        logger.exception(f"Unexpected error checking hotfixes: {e}")
        return {'error': str(e)}
