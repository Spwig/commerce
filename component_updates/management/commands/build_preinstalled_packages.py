"""
Build pre-packaged component ZIPs for deployment.

Packages themes and utilities from the spwig-components project into
preinstalled/ directory. These ZIPs are included in the Docker image
and installed at first boot by the install_bundled_components command.

Usage:
    python manage.py build_preinstalled_packages
    python manage.py build_preinstalled_packages --type theme
    python manage.py build_preinstalled_packages --components-dir /path/to/spwig-components
"""

import hashlib
import json
import zipfile
from datetime import UTC, datetime
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Build preinstalled component packages (themes + utilities) for deployment"

    THEME_SLUGS_TO_BUNDLE = [
        "starter",
        "elegant-shop",
        "modern-shop",
        "modern-dark",
        "tech-theme",
        "apparel-theme",
        "space-theme",
        "botanica",
        "artisan",
        "nature",
        "bold",
        "vivid",
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            "--type",
            choices=["theme", "utility", "all"],
            default="all",
            help="Component type to build (default: all)",
        )
        parser.add_argument(
            "--output-dir",
            default=str(Path(settings.BASE_DIR) / "preinstalled"),
            help="Output directory for packages (default: preinstalled/)",
        )
        parser.add_argument(
            "--components-dir",
            default=getattr(
                settings, "SPWIG_COMPONENTS_DIR", str(Path(settings.BASE_DIR) / "components")
            ),
            help="Component source directory (default: from SPWIG_COMPONENTS_DIR setting)",
        )

    def handle(self, *args, **options):
        component_type = options["type"]
        output_dir = Path(options["output_dir"])
        self.components_dir = Path(options["components_dir"])

        if not self.components_dir.exists():
            self.stderr.write(
                self.style.ERROR(
                    f"Components directory not found: {self.components_dir}\n"
                    f"Set SPWIG_COMPONENTS_DIR or pass --components-dir"
                )
            )
            return

        # Create output directories
        (output_dir / "themes").mkdir(parents=True, exist_ok=True)
        (output_dir / "utilities").mkdir(parents=True, exist_ok=True)

        manifest_components = []

        if component_type in ("theme", "all"):
            manifest_components.extend(self._build_theme_packages(output_dir))

        if component_type in ("utility", "all"):
            manifest_components.extend(self._build_utility_packages(output_dir))

        # Write master manifest
        manifest = {
            "platform_version": getattr(settings, "SPWIG_VERSION", "1.0.0"),
            "built_at": datetime.now(UTC).isoformat(),
            "components": manifest_components,
        }
        manifest_path = output_dir / "manifest.json"
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)

        self.stdout.write(
            self.style.SUCCESS(
                f"\nBuild complete: {len(manifest_components)} packages in {output_dir}"
            )
        )

    def _build_theme_packages(self, output_dir: Path) -> list:
        """Build ZIP packages for all bundled themes."""
        themes_dir = self.components_dir / "themes"
        components = []

        for slug in self.THEME_SLUGS_TO_BUNDLE:
            # Find the current version directory
            theme_dir = themes_dir / slug
            if not theme_dir.exists():
                self.stdout.write(self.style.WARNING(f"  ! Theme {slug} not found, skipping"))
                continue

            version_dir, version = self._resolve_component(theme_dir)
            if not version_dir:
                self.stdout.write(self.style.WARNING(f"  ! No version dir for {slug}, skipping"))
                continue

            # Read manifest
            manifest_path = version_dir / "manifest.json"
            if manifest_path.exists():
                with open(manifest_path) as f:
                    manifest = json.load(f)
            else:
                manifest = {
                    "name": slug.replace("-", " ").title(),
                    "slug": slug,
                    "version": version,
                    "description": f"{slug.replace('-', ' ').title()} theme",
                    "author": "Spwig",
                    "author_email": "themes@spwig.com",
                    "license": "MIT",
                    "engine": {"min": "1.0.0"},
                    "assets": {"css": ["css/theme.css"]},
                }

            # Read tokens
            tokens_path = version_dir / "tokens.json"
            if tokens_path.exists():
                with open(tokens_path) as f:
                    tokens = json.load(f)
                manifest["tokens"] = tokens

            # Build ZIP in the format Theme.extract_theme() expects:
            # theme/manifest.json, theme/tokens.json, theme/css/tokens.css, theme/css/theme.css
            zip_filename = f"{slug}-{version}.zip"
            zip_path = output_dir / "themes" / zip_filename

            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                # Manifest
                zf.writestr("theme/manifest.json", json.dumps(manifest, indent=2))

                # Tokens
                if tokens_path.exists():
                    zf.write(tokens_path, "theme/tokens.json")

                # CSS files
                css_dir = version_dir / "css"
                if css_dir.exists():
                    for css_file in css_dir.iterdir():
                        if css_file.is_file():
                            zf.write(css_file, f"theme/css/{css_file.name}")

                # JS files (if any)
                js_dir = version_dir / "js"
                if js_dir.exists():
                    for js_file in js_dir.iterdir():
                        if js_file.is_file():
                            zf.write(js_file, f"theme/js/{js_file.name}")

            # Calculate checksum
            checksum = self._sha256(zip_path)

            is_default = slug == "starter"
            entry = {
                "type": "theme",
                "slug": slug,
                "version": version,
                "package": f"themes/{zip_filename}",
                "checksum": checksum,
            }
            if is_default:
                entry["is_default"] = True

            components.append(entry)
            self.stdout.write(
                self.style.SUCCESS(
                    f"  + theme: {slug} v{version} ({zip_path.stat().st_size // 1024}KB)"
                )
            )

        return components

    def _build_utility_packages(self, output_dir: Path) -> list:
        """Build ZIP packages for all utilities from spwig-components/utilities/.

        Reads from a flat layout: each utility has its own directory containing
        manifest.json, CSS, JS, and logo.svg at the root level.
        """
        utilities_src = self.components_dir / "utilities"
        if not utilities_src.exists():
            self.stdout.write(self.style.WARNING("  ! utilities source dir not found"))
            return []

        components = []
        for util_dir in sorted(utilities_src.iterdir()):
            if not util_dir.is_dir() or util_dir.name.startswith("."):
                continue

            manifest_path = util_dir / "manifest.json"
            if not manifest_path.exists():
                self.stdout.write(
                    self.style.WARNING(f"  ! {util_dir.name}: no manifest.json, skipping")
                )
                continue

            with open(manifest_path) as f:
                manifest = json.load(f)

            slug = manifest.get("slug", util_dir.name.replace("_", "-"))
            version = manifest.get("version", "1.0.0")

            # Build ZIP: manifest.json at root, all other files under static/
            zip_filename = f"{slug}-{version}.zip"
            zip_path = output_dir / "utilities" / zip_filename

            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                zf.writestr("manifest.json", json.dumps(manifest, indent=2))

                # All files (CSS, JS, logo) go under static/ in the ZIP
                for f in util_dir.iterdir():
                    if f.is_file() and f.name != "manifest.json" and not f.name.startswith("."):
                        zf.write(f, f"static/{f.name}")

            checksum = self._sha256(zip_path)

            components.append(
                {
                    "type": "utility",
                    "slug": slug,
                    "version": version,
                    "package": f"utilities/{zip_filename}",
                    "checksum": checksum,
                }
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"  + utility: {slug} v{version} ({zip_path.stat().st_size // 1024}KB)"
                )
            )

        return components

    def _resolve_component(self, component_dir: Path) -> tuple[Path | None, str]:
        """Resolve a component directory and its version.

        Supports flat layout (manifest.json at root) and legacy version-folder layout.
        Returns (directory, version_string) or (None, '') if not found.
        """
        # Flat layout: manifest.json directly in component dir
        manifest_path = component_dir / "manifest.json"
        if manifest_path.exists():
            with open(manifest_path) as f:
                manifest = json.load(f)
            return component_dir, manifest.get("version", "1.0.0")

        # Legacy: 'current' symlink pointing to a version directory
        current = component_dir / "current"
        if current.is_symlink():
            target = current.resolve()
            if target.exists():
                return target, target.name.lstrip("v")

        # Legacy fallback: first version-like directory
        for item in sorted(component_dir.iterdir()):
            if item.is_dir() and any(c.isdigit() for c in item.name) and item.name != "current":
                return item, item.name.lstrip("v")
        return None, ""

    @staticmethod
    def _sha256(path: Path) -> str:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
