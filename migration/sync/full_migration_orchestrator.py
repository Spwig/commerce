"""
Full Migration Orchestrator

Extends the base SyncOrchestrator with additional handling for full system migration:
- Version compatibility checking
- Large data chunked transfer
- Media file streaming
- ID mapping for relational integrity
- Resume support after interruption
"""
import logging

from .orchestrator import SyncOrchestrator
from .client import SpwigSyncClient, SyncClientError
from .category_registry import SYNC_CATEGORIES, resolve_dependencies
from .compatibility import check_version_compatibility, check_component_compatibility, get_local_version
from .id_mapper import IDMapper
from .serializers import get_serializer_for_category
from migration.models import SyncJob, SyncStep

logger = logging.getLogger(__name__)


class FullMigrationOrchestrator(SyncOrchestrator):
    """
    Orchestrator for full system migration (Spwig -> Spwig).

    Extends the base orchestrator with:
    - Version compatibility checking before migration
    - Chunked media file transfer with progress
    - ID mapping between source and target for FK resolution
    - Resume support: track completed steps, skip on retry
    """

    def __init__(self, sync_job: SyncJob):
        super().__init__(sync_job)
        self.id_mapper = IDMapper()

    def check_compatibility(self):
        """
        Check version and component compatibility with the remote instance.

        Returns:
            dict: {
                'version': CompatibilityResult,
                'components': component compatibility dict,
                'preflight': preflight info from remote,
            }
        """
        # Get remote info
        remote_info = self.client.get_info()
        remote_version = remote_info.get('version', 'unknown')

        # Version check
        local_version = get_local_version() or 'unknown'
        version_compat = check_version_compatibility(local_version, remote_version)

        # Component check via preflight
        preflight = {}
        component_compat = {}
        try:
            preflight = self.client.get_preflight_info()
            remote_components = preflight.get('components', [])

            # Get local components
            local_components = []
            try:
                from component_updates.models import ComponentRegistry
                for comp in ComponentRegistry.objects.all():
                    local_components.append({
                        'slug': comp.slug,
                        'name': comp.name,
                        'version': comp.version,
                        'component_type': comp.component_type,
                    })
            except Exception:
                pass

            component_compat = check_component_compatibility(
                local_components, remote_components
            )
        except SyncClientError as e:
            logger.warning(f"Could not get preflight info: {e}")

        return {
            'version': {
                'compatible': bool(version_compat),
                'message': version_compat.message,
                'warnings': version_compat.warnings,
                'local_version': local_version,
                'remote_version': remote_version,
            },
            'components': component_compat,
            'preflight': preflight,
        }

    def execute_migration(self):
        """
        Execute the full system migration.
        Uses the base sync execution with additional media transfer handling.

        Returns:
            dict: Migration results
        """
        self.job.start()

        ordered_categories = resolve_dependencies(self.job.selected_categories)

        # Create SyncStep records for all categories
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
            # Take rollback snapshots for settings categories (non-large-data)
            settings_categories = [
                c for c in ordered_categories
                if not SYNC_CATEGORIES.get(c, {}).get('large_data')
            ]
            if settings_categories:
                self.job.add_log_entry("Taking rollback snapshots...")
                self._take_snapshots(settings_categories)

            for i, category_key in enumerate(ordered_categories):
                step = SyncStep.objects.get(job=self.job, category=category_key)
                config = SYNC_CATEGORIES.get(category_key, {})
                label = str(config.get('label', category_key))

                # Resume support: skip completed steps
                if step.status == 'completed':
                    logger.info(f"Skipping already completed step: {category_key}")
                    self.job.add_log_entry(f"Resuming: skipping completed {label}")
                    # Aggregate previously completed step totals
                    total_items += step.items_total
                    total_synced += step.items_synced
                    total_skipped += step.items_skipped
                    total_failed += step.items_failed
                    # Restore ID mappings from completed step
                    if step.diff_data and step.diff_data.get('id_map'):
                        stored_mapper = IDMapper.from_dict(step.diff_data['id_map'])
                        for model_key in stored_mapper._maps:
                            for src_id, tgt_id in stored_mapper._maps[model_key].items():
                                self.id_mapper.add(model_key, src_id, tgt_id)
                    continue

                step.start()

                # Update progress
                progress = int((i / len(ordered_categories)) * 100)
                self.job.update_progress(label, progress)
                self.job.add_log_entry(f"Migrating: {label}")

                try:
                    if config.get('large_data'):
                        result = self._migrate_large_data(category_key, step)
                    else:
                        result = self._migrate_category(category_key, step)

                    step.items_synced = result.get('synced', 0)
                    step.items_skipped = result.get('skipped', 0)
                    step.items_failed = result.get('failed', 0)
                    step.items_total = step.items_synced + step.items_skipped + step.items_failed

                    # Store ID mappings in step for resume/rollback
                    if result.get('id_map'):
                        step.diff_data = {'id_map': result['id_map']}

                    step.complete()

                    total_items += step.items_total
                    total_synced += step.items_synced
                    total_skipped += step.items_skipped
                    total_failed += step.items_failed

                    self.job.add_log_entry(
                        f"Completed: {label} "
                        f"({step.items_synced} migrated, {step.items_failed} failed)"
                    )

                    if result.get('errors'):
                        all_errors.extend(result['errors'])

                except Exception as e:
                    step.fail(str(e))
                    total_failed += 1
                    all_errors.append(f"{category_key}: {e}")
                    self.job.add_log_entry(f"Failed: {label} - {e}")
                    logger.error(f"Migration failed for {category_key}: {e}")

            # Update job
            self.job.items_total = total_items
            self.job.items_synced = total_synced
            self.job.items_skipped = total_skipped
            self.job.items_failed = total_failed

            if total_failed > 0 and total_synced == 0:
                self.job.mark_failed('\n'.join(all_errors[:10]))
            else:
                self.job.mark_completed()

        except Exception as e:
            logger.error(f"Full migration failed: {e}")
            self.job.mark_failed(str(e))
            raise

        return {
            'total': total_items,
            'synced': total_synced,
            'skipped': total_skipped,
            'failed': total_failed,
            'errors': all_errors,
        }

    def _migrate_category(self, category_key, step):
        """
        Migrate a single category from remote to local.
        Handles pagination and ID mapping.
        """
        serializer = get_serializer_for_category(
            category_key, sync_job=self.job, sync_step=step
        )
        if not serializer:
            return {'synced': 0, 'skipped': 0, 'failed': 0, 'errors': ['No serializer']}

        # Fetch all pages from remote
        all_items = list(self.client.export_category_all(category_key))
        remote_data = {
            'category': category_key,
            'sync_type': SYNC_CATEGORIES.get(category_key, {}).get('sync_type', 'collection'),
            'items': all_items,
            'total': len(all_items),
        }

        result = serializer.import_data(remote_data, dry_run=False, sync_mode='additive')

        # Store ID mappings if the serializer produced them
        if hasattr(serializer, 'id_mapper') and serializer.id_mapper:
            result['id_map'] = serializer.id_mapper.to_dict()
            # Merge into the orchestrator's global mapper
            for model_key in serializer.id_mapper._maps:
                for src_id, tgt_id in serializer.id_mapper._maps[model_key].items():
                    self.id_mapper.add(model_key, src_id, tgt_id)

        return result

    def _migrate_large_data(self, category_key, step):
        """
        Migrate a large data category (e.g., media) with chunked transfer.
        """
        # For now, use the same approach as regular categories
        # Media file transfer will be handled by separate Celery tasks
        return self._migrate_category(category_key, step)

    def rollback(self):
        """
        Rollback full migration by deleting created objects in reverse dependency order.
        """
        if not self.job.is_rollbackable:
            raise ValueError("This migration cannot be rolled back.")

        self.job.status = 'rolling_back'
        self.job.save(update_fields=['status'])

        errors = []
        deleted = 0

        # Get steps in reverse order
        steps = self.job.steps.filter(
            status='completed'
        ).order_by('-id')

        for step in steps:
            try:
                id_map_data = (step.diff_data or {}).get('id_map', {})
                if id_map_data:
                    mapper = IDMapper.from_dict(id_map_data)
                    for model_key in mapper._maps:
                        target_ids = mapper.get_all_target_ids(model_key)
                        if target_ids:
                            count = self._delete_by_ids(model_key, target_ids)
                            deleted += count

                step.status = 'rolled_back'
                step.save(update_fields=['status'])

            except Exception as e:
                errors.append(f"Rollback {step.category}: {e}")
                logger.error(f"Rollback failed for {step.category}: {e}")

        # For settings categories, restore from snapshots
        snapshots = self.job.rollback_snapshot or {}
        for category_key, snapshot_data in snapshots.items():
            try:
                serializer = get_serializer_for_category(category_key)
                if serializer:
                    result = serializer.restore_snapshot(snapshot_data)
                    deleted += result.get('restored', 0)
            except Exception as e:
                errors.append(f"Restore {category_key}: {e}")

        # Only mark as rolled_back if at least some steps succeeded
        total_steps = steps.count() + len(snapshots)
        if errors and len(errors) >= total_steps and total_steps > 0:
            self.job.status = 'failed'
            self.job.error_summary = 'Rollback failed: ' + '; '.join(errors[:5])
        else:
            self.job.status = 'rolled_back'
        self.job.can_rollback = False
        self.job.save(update_fields=['status', 'can_rollback', 'error_summary'])

        return {'deleted': deleted, 'errors': errors}

    def _delete_by_ids(self, model_key, target_ids):
        """Delete objects by their IDs. model_key format: 'app.Model'."""
        try:
            from django.apps import apps
            app_label, model_name = model_key.split('.')
            model = apps.get_model(app_label, model_name)
            count, _ = model.objects.filter(pk__in=target_ids).delete()
            return count
        except Exception as e:
            logger.error(f"Could not delete {model_key} IDs: {e}")
            return 0
