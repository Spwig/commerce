"""
Base class for all seed data management commands.

Subclasses must define:
    seed_name: str           -- Unique identifier (e.g., 'customer_segments')
    seed_version: int        -- Bump when seed data changes
    dependencies: list[str]  -- List of seed_names that must run first (informational)

Subclasses must implement:
    seed(self) -> int        -- Perform the seeding, return record count
"""
import logging

from django.core.management.base import BaseCommand
from django.db import transaction

logger = logging.getLogger(__name__)


class SeedCommand(BaseCommand):
    seed_name = None
    seed_version = 1
    dependencies = []

    def add_arguments(self, parser):
        parser.add_argument(
            '--force', action='store_true',
            help='Run even if version is current',
        )
        parser.add_argument(
            '--dry-run', action='store_true',
            help='Show what would be done without making changes',
        )

    def handle(self, *args, **options):
        from core.models import SeedVersion

        force = options.get('force', False)
        dry_run = options.get('dry_run', False)

        if not self.seed_name:
            raise ValueError("SeedCommand subclass must define seed_name")

        # Check version
        current = SeedVersion.objects.filter(seed_name=self.seed_name).first()
        if current and current.version >= self.seed_version and not force:
            self.stdout.write(
                f"  {self.seed_name} v{self.seed_version} already applied, skipping"
            )
            return

        if dry_run:
            action = "update" if current else "create"
            self.stdout.write(
                f"  [DRY RUN] Would {action} {self.seed_name} "
                f"to v{self.seed_version}"
            )
            return

        self.stdout.write(f"  Seeding {self.seed_name} v{self.seed_version}...")

        with transaction.atomic():
            record_count = self.seed()

        # Update version tracker
        SeedVersion.objects.update_or_create(
            seed_name=self.seed_name,
            defaults={
                'version': self.seed_version,
                'record_count': record_count or 0,
            },
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"  {self.seed_name} v{self.seed_version}: "
                f"{record_count} records"
            )
        )

    def seed(self) -> int:
        """Override in subclass. Return number of records affected."""
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement seed()"
        )
