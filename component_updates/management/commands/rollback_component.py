"""
Management command to rollback a component to a previous version.

Usage:
    python manage.py rollback_component logo          # Rollback to previous version
    python manage.py rollback_component logo 1.0.0    # Rollback to specific version
"""

from django.core.management.base import BaseCommand, CommandError

from component_updates.models import ComponentRegistry
from component_updates.services import UpdateInstallError, UpdateManager


class Command(BaseCommand):
    help = "Rollback a component to a previous version"

    def add_arguments(self, parser):
        parser.add_argument(
            "component",
            type=str,
            help='Component slug to rollback (e.g., "logo")',
        )
        parser.add_argument(
            "version",
            type=str,
            nargs="?",
            help="Specific version to rollback to (optional)",
        )

    def handle(self, *args, **options):
        component_slug = options["component"]
        target_version = options.get("version")

        # Find component
        try:
            component = ComponentRegistry.objects.get(slug=component_slug)
        except ComponentRegistry.DoesNotExist:
            raise CommandError(f"Component not found: {component_slug}")

        # Check if locked
        if component.locked:
            raise CommandError(f'Component "{component.name}" is locked and cannot be rolled back')

        # Get available rollback versions
        available_versions = component.get_rollback_versions()

        if not available_versions:
            raise CommandError(f"No rollback versions available for {component.name}")

        # Display current version
        self.stdout.write(
            f"\n📦 {component.name} ({component.component_type})\n"
            f"   Current version: {component.current_version}\n"
        )

        # Display available versions
        self.stdout.write("\n⏮️  Available rollback versions:\n")
        for version in available_versions:
            health_indicator = {
                "healthy": "✅",
                "degraded": "⚠️",
                "unhealthy": "❌",
                "unknown": "❓",
            }.get(version.health_status, "❓")

            self.stdout.write(
                f"   {health_indicator} v{version.version} "
                f"(installed {version.installed_at.strftime('%Y-%m-%d %H:%M')})\n"
            )

        # If no target version specified, use most recent
        if not target_version:
            target_version = available_versions[0].version
            self.stdout.write(f"\n⏮️  Rolling back to most recent version: v{target_version}\n")

        # Confirm rollback
        self.stdout.write(
            self.style.WARNING(
                f"\n⚠️  This will rollback {component.name} from v{component.current_version} "
                f"to v{target_version}\n"
            )
        )

        manager = UpdateManager()

        try:
            self.stdout.write("\n🔄 Performing rollback...")
            success = manager.rollback(component, target_version)

            if success:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"\n✅ Successfully rolled back {component.name} to v{target_version}\n"
                    )
                )
            else:
                raise CommandError("Rollback failed")

        except UpdateInstallError as e:
            raise CommandError(f"Rollback failed: {e}")
        except Exception as e:
            raise CommandError(f"Unexpected error during rollback: {e}")
