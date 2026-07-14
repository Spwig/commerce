"""
Base Importer
Abstract base class for all data importers with transaction support
"""

import logging
from abc import ABC, abstractmethod
from typing import Any

from django.db import transaction

logger = logging.getLogger(__name__)


class BaseImporter(ABC):
    """
    Abstract base class for importing data with transaction support

    All importers should inherit from this class and implement import methods
    """

    def __init__(self, migration_job, dry_run: bool = False):
        """
        Initialize importer

        Args:
            migration_job: MigrationJob instance
            dry_run: If True, don't commit changes to database
        """
        self.migration_job = migration_job
        self.dry_run = dry_run

        # Statistics
        self.stats = {
            "created": 0,
            "updated": 0,
            "skipped": 0,
            "failed": 0,
            "total": 0,
        }

        # Tracking for rollback
        self.created_objects = []
        self.updated_objects = []
        self.errors = []

    @abstractmethod
    def import_data(self, mapped_data: dict) -> Any:
        """
        Import mapped data into database

        Args:
            mapped_data: Data in internal format

        Returns:
            Created/updated model instance
        """
        pass

    def import_batch(self, mapped_data_list: list[dict], progress_callback=None) -> dict:
        """
        Import a batch of items with transaction support

        Args:
            mapped_data_list: List of mapped data dictionaries
            progress_callback: Optional callback for progress updates

        Returns:
            Dictionary with statistics
        """
        self.stats["total"] = len(mapped_data_list)

        with transaction.atomic():
            # Create savepoint for potential rollback
            savepoint_id = transaction.savepoint()

            try:
                for idx, mapped_data in enumerate(mapped_data_list):
                    try:
                        # Import single item
                        result = self.import_data(mapped_data)

                        if result:
                            if hasattr(result, "_state") and result._state.adding:
                                self.stats["created"] += 1
                                self.created_objects.append(result)
                            else:
                                self.stats["updated"] += 1
                                self.updated_objects.append(result)
                        else:
                            self.stats["skipped"] += 1

                        # Progress callback
                        if progress_callback:
                            progress_callback(
                                current=idx + 1,
                                total=self.stats["total"],
                                created=self.stats["created"],
                                updated=self.stats["updated"],
                                failed=self.stats["failed"],
                            )

                    except Exception as e:
                        self.stats["failed"] += 1
                        self.errors.append({"index": idx, "data": mapped_data, "error": str(e)})
                        logger.error(f"Failed to import item {idx}: {e}")

                        # Continue with next item (don't fail entire batch)
                        continue

                # Check if we should commit or rollback
                if self.dry_run:
                    logger.info("Dry run mode - rolling back changes")
                    transaction.savepoint_rollback(savepoint_id)
                else:
                    logger.info(
                        f"Committing {self.stats['created']} creates, {self.stats['updated']} updates"
                    )
                    transaction.savepoint_commit(savepoint_id)

            except Exception as e:
                logger.error(f"Batch import failed: {e}")
                transaction.savepoint_rollback(savepoint_id)
                raise

        return self.get_stats()

    def get_or_create(
        self, model_class: type, lookup_fields: dict, defaults: dict, update_existing: bool = True
    ) -> tuple:
        """
        Get or create model instance

        Args:
            model_class: Django model class
            lookup_fields: Fields to look up existing instance
            defaults: Default values for creation
            update_existing: Whether to update existing instances

        Returns:
            Tuple of (instance, created)
        """
        try:
            # Try to get existing instance
            instance = model_class.objects.get(**lookup_fields)
            created = False

            # Update if requested
            if update_existing:
                for key, value in defaults.items():
                    setattr(instance, key, value)
                instance.save()

        except model_class.DoesNotExist:
            # Create new instance
            instance = model_class.objects.create(**{**lookup_fields, **defaults})
            created = True

        except model_class.MultipleObjectsReturned:
            # Multiple objects found - use first one
            instance = model_class.objects.filter(**lookup_fields).first()
            created = False

            if update_existing:
                for key, value in defaults.items():
                    setattr(instance, key, value)
                instance.save()

        return instance, created

    def record_mapping(
        self, source_id: str, source_platform: str, target_model: str, target_id: Any
    ):
        """
        Record mapping between source and target for future reference

        Args:
            source_id: ID in source platform
            source_platform: Source platform name
            target_model: Target model name
            target_id: ID in target system
        """
        from migration.models import MigrationMapping

        MigrationMapping.objects.create(
            job=self.migration_job,
            source_platform=source_platform,
            source_model=target_model,
            source_id=source_id,
            target_model=target_model,
            target_id=str(target_id),
        )

    def get_mapped_id(self, source_id: str, source_platform: str, target_model: str) -> Any | None:
        """
        Get mapped target ID for a source ID

        Args:
            source_id: ID in source platform
            source_platform: Source platform name
            target_model: Target model name

        Returns:
            Target ID or None
        """
        from migration.models import MigrationMapping

        try:
            mapping = MigrationMapping.objects.get(
                job=self.migration_job,
                source_platform=source_platform,
                source_model=target_model,
                source_id=source_id,
            )
            return mapping.target_id
        except MigrationMapping.DoesNotExist:
            return None

    def get_stats(self) -> dict:
        """Get import statistics"""
        return {
            **self.stats,
            "success_rate": (
                ((self.stats["created"] + self.stats["updated"]) / self.stats["total"] * 100)
                if self.stats["total"] > 0
                else 0
            ),
            "errors": self.errors,
        }

    def get_errors(self) -> list[dict]:
        """Get import errors"""
        return self.errors

    def clear_stats(self):
        """Clear statistics"""
        self.stats = {
            "created": 0,
            "updated": 0,
            "skipped": 0,
            "failed": 0,
            "total": 0,
        }
        self.created_objects = []
        self.updated_objects = []
        self.errors = []
