"""
Install pre-built component packages bundled with the platform image.

This is the single entry point for bootstrapping all preinstalled components
(themes + utilities) on first boot and during platform upgrades. It uses the
same installation code paths as marketplace installs.

Usage:
    python manage.py install_bundled_components
    python manage.py install_bundled_components --force
    python manage.py install_bundled_components --type theme
"""

import json
import logging
import tempfile
import zipfile
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from component_updates.installers import (
    ensure_component_registry,
    install_theme_from_package,
    install_utility_from_package,
)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Install bundled component packages (themes + utilities) from preinstalled/"

    def add_arguments(self, parser):
        parser.add_argument(
            "--type",
            choices=["theme", "utility", "all"],
            default="all",
            help="Component type to install (default: all)",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Reinstall even if already at the same version",
        )
        parser.add_argument(
            "--bundle-dir",
            default=str(Path(settings.BASE_DIR) / "preinstalled"),
            help="Path to preinstalled bundles directory",
        )

    def handle(self, *args, **options):
        bundle_dir = Path(options["bundle_dir"])
        manifest_path = bundle_dir / "manifest.json"
        component_type = options["type"]
        force = options["force"]

        if not manifest_path.exists():
            self.stdout.write(
                self.style.WARNING(
                    f"No preinstalled manifest found at {manifest_path}. "
                    "Run 'build_preinstalled_packages' first."
                )
            )
            return

        with open(manifest_path) as f:
            manifest = json.load(f)

        components = manifest.get("components", [])
        if component_type != "all":
            components = [c for c in components if c["type"] == component_type]

        installed = 0
        skipped = 0
        failed = 0

        for entry in components:
            comp_type = entry["type"]
            slug = entry["slug"]
            version = entry["version"]
            package_rel = entry["package"]
            package_path = bundle_dir / package_rel

            if not package_path.exists():
                self.stdout.write(self.style.ERROR(f"  ! Package not found: {package_path}"))
                failed += 1
                continue

            # Check if already installed at this version
            if not force and self._is_installed(comp_type, slug, version):
                self.stdout.write(f"  = {comp_type}: {slug} v{version} (already installed)")
                skipped += 1
                continue

            try:
                if comp_type == "theme":
                    result = self._install_theme(package_path, entry)
                elif comp_type == "utility":
                    result = self._install_utility(package_path, entry)
                else:
                    self.stdout.write(self.style.WARNING(f"  ! Unknown type: {comp_type}"))
                    skipped += 1
                    continue

                if result.get("success"):
                    installed += 1
                    self.stdout.write(self.style.SUCCESS(f"  + {comp_type}: {slug} v{version}"))
                else:
                    failed += 1
                    self.stdout.write(
                        self.style.ERROR(
                            f"  x {comp_type}: {slug} v{version} - {result.get('error', 'unknown')}"
                        )
                    )

            except Exception as e:
                failed += 1
                self.stdout.write(self.style.ERROR(f"  x {comp_type}: {slug} v{version} - {e}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"\nBundled components: {installed} installed, {skipped} skipped, {failed} failed"
            )
        )

    def _install_theme(self, package_path: Path, entry: dict) -> dict:
        """Install a theme from a bundled ZIP package."""
        with tempfile.TemporaryDirectory() as extract_dir:
            extract_path = Path(extract_dir)
            with zipfile.ZipFile(package_path, "r") as zf:
                zf.extractall(extract_path)

            # Read manifest from the extracted package
            manifest = self._read_manifest(extract_path, entry)
            manifest["is_default"] = entry.get("is_default", False)

            result = install_theme_from_package(
                extract_dir=extract_path,
                manifest=manifest,
                create_db_record=True,
            )

            if result.get("success"):
                ensure_component_registry(
                    "theme", entry["slug"], manifest, install_method="bundled"
                )

            return result

    def _install_utility(self, package_path: Path, entry: dict) -> dict:
        """Install a utility from a bundled ZIP package."""
        with tempfile.TemporaryDirectory() as extract_dir:
            extract_path = Path(extract_dir)
            with zipfile.ZipFile(package_path, "r") as zf:
                zf.extractall(extract_path)

            # Read manifest from the extracted package
            manifest = self._read_manifest(extract_path, entry)

            result = install_utility_from_package(
                extract_dir=extract_path,
                manifest=manifest,
            )

            if result.get("success"):
                ensure_component_registry(
                    "utility", entry["slug"], manifest, install_method="bundled"
                )

            return result

    def _read_manifest(self, extract_path: Path, entry: dict) -> dict:
        """Read manifest.json from extracted package, falling back to entry data."""
        manifest_path = extract_path / "manifest.json"
        # Some theme packages have manifest under theme/ subdir
        theme_manifest = extract_path / "theme" / "manifest.json"

        if manifest_path.exists():
            with open(manifest_path) as f:
                return json.load(f)
        elif theme_manifest.exists():
            with open(theme_manifest) as f:
                return json.load(f)

        # Fallback: construct from entry data
        return {
            "slug": entry["slug"],
            "name": entry["slug"].replace("-", " ").replace("_", " ").title(),
            "version": entry["version"],
            "author": "Spwig",
        }

    def _is_installed(self, component_type: str, slug: str, version: str) -> bool:
        """Check if a component is already installed at the given version."""
        from component_updates.models import ComponentRegistry

        try:
            return ComponentRegistry.objects.filter(
                component_type=component_type,
                slug=slug,
                current_version=version,
            ).exists()
        except Exception:
            return False
