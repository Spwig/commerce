"""
Install bundled translation provider components from spwig-components.

Sets up the components_data/integrations/translation_provider/ directory
structure with versioned directories and 'current' symlinks, and creates
ComponentRegistry entries.

Usage:
    python manage.py install_translation_providers
    python manage.py install_translation_providers --force
"""
import json
import logging
import shutil
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)

# Source directory containing provider packages
SPWIG_COMPONENTS = Path(settings.BASE_DIR).parent / 'spwig-components'
SOURCE_DIR = SPWIG_COMPONENTS / 'integrations' / 'translation_provider'


class Command(BaseCommand):
    help = 'Install bundled translation provider components'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Reinstall even if already at the same version',
        )

    def handle(self, *args, **options):
        from component_updates.models import ComponentRegistry
        from component_updates.integration_paths import INTEGRATIONS_DIR, touch_provider_cache_marker

        force = options['force']

        if not SOURCE_DIR.exists():
            self.stdout.write(self.style.ERROR(
                f"Source directory not found: {SOURCE_DIR}"
            ))
            return

        # Create target base directory
        target_base = INTEGRATIONS_DIR / 'translation_provider'
        target_base.mkdir(parents=True, exist_ok=True)

        installed = 0
        skipped = 0

        # Scan for provider packages
        for provider_dir in sorted(SOURCE_DIR.iterdir()):
            if not provider_dir.is_dir():
                continue

            manifest_path = provider_dir / 'manifest.json'
            if not manifest_path.exists():
                self.stdout.write(self.style.WARNING(
                    f"  ! No manifest.json in {provider_dir.name}, skipping"
                ))
                continue

            with open(manifest_path) as f:
                manifest = json.load(f)

            slug = manifest['slug']
            version = manifest['version']
            name = manifest['name']

            # Check if already installed at this version
            if not force:
                existing = ComponentRegistry.objects.filter(
                    component_type='translation_provider',
                    slug=slug,
                    current_version=version,
                ).first()
                if existing:
                    self.stdout.write(f"  = {name} v{version} (already installed)")
                    skipped += 1
                    continue

            # Install: copy to versioned directory
            provider_target = target_base / slug
            provider_target.mkdir(parents=True, exist_ok=True)
            version_dir = provider_target / f'v{version}'

            if version_dir.exists():
                shutil.rmtree(version_dir)

            shutil.copytree(provider_dir, version_dir)

            # Create/update 'current' symlink
            current_link = provider_target / 'current'
            if current_link.exists() or current_link.is_symlink():
                current_link.unlink()
            current_link.symlink_to(f'v{version}')

            # Create/update ComponentRegistry entry
            registry, created = ComponentRegistry.objects.update_or_create(
                component_type='translation_provider',
                slug=slug,
                defaults={
                    'name': name,
                    'current_version': version,
                    'author': manifest.get('author', 'Spwig'),
                    'author_details': manifest.get('author_details', {}),
                    'description': manifest.get('description', ''),
                    'homepage_url': manifest.get('homepage_url', ''),
                    'support_url': manifest.get('support_url', ''),
                    'requires_platform_version': manifest.get('min_platform_version', ''),
                },
            )

            action = 'installed' if created else 'updated'
            self.stdout.write(self.style.SUCCESS(
                f"  + {name} v{version} ({action})"
            ))
            installed += 1

        # Invalidate provider cache so ProviderRegistry reloads
        if installed > 0:
            touch_provider_cache_marker('translation_provider')

        self.stdout.write(self.style.SUCCESS(
            f"\nTranslation providers: {installed} installed, {skipped} skipped"
        ))
