"""
Settings Sync Orchestrator

Orchestrates a complete settings sync operation between two Spwig instances.
Handles dependency ordering, progress tracking, snapshot/rollback, and error handling.
"""

import logging

from migration.models import SyncJob, SyncStep

from .category_registry import SYNC_CATEGORIES, resolve_dependencies
from .client import SpwigSyncClient, SyncClientError
from .diff_engine import SyncDiffEngine
from .serializers import get_serializer_for_category

logger = logging.getLogger(__name__)


class SyncOrchestrator:
    """
    Orchestrates a settings sync operation.

    Flow:
    1. Connect to remote instance
    2. Resolve dependencies and order categories
    3. Generate preview diff (optional, for UI)
    4. Take rollback snapshots
    5. Execute sync per category (pull or push)
    6. Update progress and statistics
    """

    def __init__(self, sync_job: SyncJob):
        self.job = sync_job
        self.client = SpwigSyncClient(sync_job.connection)
        self.diff_engine = SyncDiffEngine()

    def generate_preview(self):
        """
        Fetch remote data and generate diff for all selected categories.
        Updates the job's diff_preview field.

        Returns:
            dict: Complete diff preview
        """
        self.job.status = "previewing"
        self.job.save(update_fields=["status"])

        try:
            ordered_categories = resolve_dependencies(self.job.selected_categories)
            remote_data = {}

            for category_key in ordered_categories:
                try:
                    data = self.client.export_category(category_key)
                    remote_data[category_key] = data
                except SyncClientError as e:
                    logger.warning(f"Could not export {category_key} from remote: {e}")
                    remote_data[category_key] = {}

            if self.job.sync_mode == "mirror":
                diff = self.diff_engine.generate_mirror_diff(self.job, remote_data)
            else:
                diff = self.diff_engine.generate_job_diff(self.job, remote_data)

            self.job.diff_preview = diff
            self.job.status = "awaiting_confirmation"
            self.job.save(update_fields=["diff_preview", "status"])

            return diff

        except Exception as e:
            logger.error(f"Preview generation failed: {e}")
            self.job.mark_failed(str(e))
            raise

    def execute_sync(self):
        """
        Execute the sync operation.

        For 'pull' direction: fetch from remote, apply locally
        For 'push' direction: export locally, send to remote

        Returns:
            dict: Execution results
        """
        self.job.start()

        ordered_categories = resolve_dependencies(self.job.selected_categories)

        # Create SyncStep records
        for category_key in ordered_categories:
            SyncStep.objects.get_or_create(
                job=self.job,
                category=category_key,
            )

        total_items = 0
        total_synced = 0
        total_skipped = 0
        total_failed = 0
        all_errors = []

        try:
            # Take rollback snapshots before any changes
            if self.job.direction == "pull":
                self.job.add_log_entry("Taking rollback snapshots...")
                self._take_snapshots(ordered_categories)

            for i, category_key in enumerate(ordered_categories):
                step = SyncStep.objects.get(job=self.job, category=category_key)
                step.start()

                # Update overall progress
                progress = int((i / len(ordered_categories)) * 100)
                config = SYNC_CATEGORIES.get(category_key, {})
                label = str(config.get("label", category_key))
                self.job.update_progress(label, progress)

                direction_verb = "Pulling" if self.job.direction == "pull" else "Pushing"
                self.job.add_log_entry(f"{direction_verb}: {label}")

                try:
                    if self.job.direction == "pull":
                        result = self._pull_category(category_key, step)
                    else:
                        result = self._push_category(category_key, step)

                    step.items_synced = result.get("synced", 0)
                    step.items_skipped = result.get("skipped", 0)
                    step.items_failed = result.get("failed", 0)
                    step.items_total = step.items_synced + step.items_skipped + step.items_failed
                    step.complete()

                    total_items += step.items_total
                    total_synced += step.items_synced
                    total_skipped += step.items_skipped
                    total_failed += step.items_failed

                    self.job.add_log_entry(
                        f"Completed: {label} "
                        f"({step.items_synced} synced, {step.items_failed} failed)"
                    )

                    if result.get("errors"):
                        all_errors.extend(result["errors"])

                except Exception as e:
                    step.fail(str(e))
                    total_failed += 1
                    all_errors.append(f"{category_key}: {e}")
                    self.job.add_log_entry(f"Failed: {label} - {e}")
                    logger.error(f"Sync failed for {category_key}: {e}")

            # Update job totals
            self.job.items_total = total_items
            self.job.items_synced = total_synced
            self.job.items_skipped = total_skipped
            self.job.items_failed = total_failed

            if total_failed > 0 and total_synced == 0:
                self.job.mark_failed("\n".join(all_errors[:10]))
            else:
                self.job.mark_completed()

        except Exception as e:
            logger.error(f"Sync execution failed: {e}")
            self.job.mark_failed(str(e))
            raise

        return {
            "total": total_items,
            "synced": total_synced,
            "skipped": total_skipped,
            "failed": total_failed,
            "errors": all_errors,
        }

    def rollback(self):
        """
        Restore pre-sync state from snapshots.
        """
        if not self.job.is_rollbackable:
            raise ValueError("This sync job cannot be rolled back.")

        self.job.status = "rolling_back"
        self.job.save(update_fields=["status"])

        errors = []
        restored = 0

        snapshots = self.job.rollback_snapshot
        for category_key, snapshot_data in snapshots.items():
            try:
                serializer = get_serializer_for_category(category_key)
                if serializer:
                    result = serializer.restore_snapshot(snapshot_data)
                    restored += result.get("restored", 0)
                    if result.get("errors"):
                        errors.extend(result["errors"])

                    # Update step status
                    step = SyncStep.objects.filter(job=self.job, category=category_key).first()
                    if step:
                        step.status = "rolled_back"
                        step.save(update_fields=["status"])

            except Exception as e:
                errors.append(f"Rollback {category_key}: {e}")
                logger.error(f"Rollback failed for {category_key}: {e}")

        # Only mark as rolled_back if at least some categories succeeded
        # If ALL categories failed to rollback, mark as failed instead
        total_categories = len(snapshots) if snapshots else 0
        if errors and len(errors) >= total_categories and total_categories > 0:
            self.job.status = "failed"
            self.job.error_summary = "Rollback failed: " + "; ".join(errors[:5])
        else:
            self.job.status = "rolled_back"
        self.job.can_rollback = False
        self.job.save(update_fields=["status", "can_rollback", "error_summary"])

        return {"restored": restored, "errors": errors}

    # ---- Private Methods ----

    def _pull_category(self, category_key, step):
        """Pull data from remote and import locally."""
        # Fetch from remote
        remote_data = self.client.export_category(category_key)

        # Import locally
        serializer = get_serializer_for_category(category_key, sync_job=self.job, sync_step=step)
        if not serializer:
            return {"synced": 0, "skipped": 0, "failed": 0, "errors": ["No serializer"]}

        return serializer.import_data(
            remote_data,
            dry_run=False,
            sync_mode=self.job.sync_mode,
        )

    def _push_category(self, category_key, step):
        """Export data locally and push to remote."""
        # Export locally
        serializer = get_serializer_for_category(category_key, sync_job=self.job, sync_step=step)
        if not serializer:
            return {"synced": 0, "skipped": 0, "failed": 0, "errors": ["No serializer"]}

        local_data = serializer.export(credential_mode="decrypt")

        # Send to remote
        result = self.client.import_category(
            category_key,
            {
                **local_data,
                "sync_mode": self.job.sync_mode,
            },
        )

        return result

    def _take_snapshots(self, ordered_categories):
        """Take rollback snapshots for all categories before sync."""
        snapshots = {}
        for category_key in ordered_categories:
            try:
                serializer = get_serializer_for_category(category_key)
                if serializer:
                    snapshots[category_key] = serializer.snapshot_current()
            except Exception as e:
                logger.warning(f"Could not snapshot {category_key}: {e}")

        self.job.rollback_snapshot = snapshots
        self.job.save(update_fields=["rollback_snapshot"])
