"""
Management command to sync existing components to the registry
Creates registry entries for all installed themes, utilities, etc.
"""

import json

from django.core.management.base import BaseCommand

from component_updates.models import ComponentRegistry, ComponentVersion, UpdateChannel
from component_updates.utility_registry import get_utility_registry
from component_updates.utility_version_manager import UtilityVersionManager
from design.theme_models import Theme


class Command(BaseCommand):
    help = "Sync existing components to the update registry"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be synced without actually doing it",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]

        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN MODE - No changes will be made"))

        # Get or create stable channel
        stable_channel, created = UpdateChannel.objects.get_or_create(
            name=UpdateChannel.STABLE,
            defaults={
                "description": "Stable production releases",
                "priority": 0,
                "is_active": True,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS("✓ Created stable update channel"))

        # Note: Widgets are now baked into the platform and don't need syncing

        # Sync Themes
        self.stdout.write("\n🎨 Syncing Themes...")
        theme_count = 0
        for theme in Theme.objects.all():
            if dry_run:
                self.stdout.write(f"  Would sync: {theme.name} v{theme.version}")
            else:
                registry, created = ComponentRegistry.objects.update_or_create(
                    component_type="theme",
                    slug=theme.slug,
                    defaults={
                        "name": theme.name,
                        "current_version": theme.version,
                        "author": theme.author,
                        "description": theme.description,
                        "update_channel": stable_channel,
                        "theme": theme,
                        "engine_min_version": theme.engine_min_version or "",
                        "engine_max_version": theme.engine_max_version or "",
                    },
                )

                # Create version entry
                version, v_created = ComponentVersion.objects.get_or_create(
                    component=registry,
                    version=theme.version,
                    defaults={
                        "install_method": "manual",
                        "is_active": True,
                        "rollback_available": True,
                    },
                )

                action = "Created" if created else "Updated"
                self.stdout.write(f"  ✓ {action}: {theme.name} v{theme.version}")
                theme_count += 1

        # Sync Utilities
        self.stdout.write("\n🛠️ Syncing Utilities...")
        utility_count = 0

        # Get all utilities from registry
        utility_registry = get_utility_registry()
        utility_registry.initialize()  # Ensure built-in utilities are registered

        for utility_slug, utility_config in utility_registry.get_all_utilities().items():
            # Get current version from version manager
            current_version = UtilityVersionManager.get_current_version(utility_slug) or "v1.0.0"
            version = current_version.lstrip("v")  # Remove 'v' prefix for database storage

            if dry_run:
                self.stdout.write(f"  Would sync: {utility_config.display_name} v{version}")
            else:
                registry, created = ComponentRegistry.objects.update_or_create(
                    component_type="utility",
                    slug=utility_slug,
                    defaults={
                        "name": utility_config.display_name,
                        "current_version": version,
                        "author": "Spwig",
                        "description": utility_config.description,
                        "update_channel": stable_channel,
                    },
                )

                # Create version entry
                version_obj, v_created = ComponentVersion.objects.get_or_create(
                    component=registry,
                    version=version,
                    defaults={
                        "install_method": "manual",
                        "is_active": True,
                        "rollback_available": True,
                    },
                )

                action = "Created" if created else "Updated"
                self.stdout.write(f"  ✓ {action}: {utility_config.display_name} v{version}")
                utility_count += 1

        # Sync Terminal Providers
        self.stdout.write("\n💳 Syncing Terminal Providers...")
        terminal_provider_count = 0
        from component_updates.integration_paths import INTEGRATIONS_DIR

        terminal_providers_path = INTEGRATIONS_DIR / "terminal_provider"
        if terminal_providers_path.exists():
            for provider_dir in terminal_providers_path.iterdir():
                if not provider_dir.is_dir():
                    continue

                # Find current version symlink or highest version
                current_path = provider_dir / "current"
                if current_path.is_symlink():
                    version_dir = current_path.resolve()
                else:
                    versions = [
                        d for d in provider_dir.iterdir() if d.is_dir() and d.name.startswith("v")
                    ]
                    if not versions:
                        continue
                    version_dir = max(versions, key=lambda x: x.name)

                manifest_path = version_dir / "manifest.json"
                if not manifest_path.exists():
                    continue

                try:
                    with open(manifest_path) as f:
                        manifest = json.load(f)
                except (OSError, json.JSONDecodeError) as e:
                    self.stdout.write(self.style.WARNING(f"  ⚠ Skipping {provider_dir.name}: {e}"))
                    continue

                slug = manifest.get("slug", provider_dir.name)
                name = manifest.get("name", slug)
                version = manifest.get("version", "1.0.0")
                author = manifest.get("author", "Spwig")
                description = manifest.get("description", "")

                if dry_run:
                    self.stdout.write(f"  Would sync: {name} v{version}")
                else:
                    registry, created = ComponentRegistry.objects.update_or_create(
                        component_type="terminal_provider",
                        slug=slug,
                        defaults={
                            "name": name,
                            "current_version": version,
                            "author": author,
                            "description": description,
                            "update_channel": stable_channel,
                        },
                    )

                    # Create version entry
                    version_obj, v_created = ComponentVersion.objects.get_or_create(
                        component=registry,
                        version=version,
                        defaults={
                            "install_method": "manual",
                            "is_active": True,
                            "rollback_available": True,
                        },
                    )

                    action = "Created" if created else "Updated"
                    self.stdout.write(f"  ✓ {action}: {name} v{version}")
                    terminal_provider_count += 1
        else:
            self.stdout.write("  (no terminal providers directory found)")

        # Summary
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("✓ Sync Complete"))
        self.stdout.write(f"  Themes: {theme_count}")
        self.stdout.write(f"  Utilities: {utility_count}")
        self.stdout.write(f"  Terminal Providers: {terminal_provider_count}")
        self.stdout.write(f"  Total: {theme_count + utility_count + terminal_provider_count}")

        if not dry_run:
            self.stdout.write("\n📊 Component Registry Status:")
            total_components = ComponentRegistry.objects.count()
            total_versions = ComponentVersion.objects.count()
            self.stdout.write(f"  Total Components: {total_components}")
            self.stdout.write(f"  Total Versions: {total_versions}")
