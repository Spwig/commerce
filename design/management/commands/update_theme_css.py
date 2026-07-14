"""
Management command to update a theme's compiled_css in the database from source files.

This is useful during development when making changes to theme tokens or CSS files.
It reads the CSS files from the components directory and updates the database directly,
without needing to repackage or reinstall the theme.

Usage:
    python manage.py update_theme_css --theme starter
    python manage.py update_theme_css --all
"""

import hashlib
import json
import re
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from design.models import GlobalDesignSettings
from design.theme_models import Theme


class Command(BaseCommand):
    help = "Updates theme compiled_css in database from source CSS files"

    def add_arguments(self, parser):
        parser.add_argument(
            "--theme",
            type=str,
            help="Theme slug to update (e.g., starter, modern-shop)",
        )
        parser.add_argument(
            "--theme-version",
            type=str,
            default=None,
            help="Legacy: theme version subfolder (ignored for flat layout)",
        )
        parser.add_argument(
            "--all",
            action="store_true",
            help="Update all themes in the database",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be updated without making changes",
        )

    def handle(self, *args, **options):
        theme_slug = options.get("theme")
        version = options.get("theme_version")
        update_all = options.get("all")
        dry_run = options.get("dry_run")

        if not theme_slug and not update_all:
            raise CommandError("Please specify --theme SLUG or --all")

        # Try installed location first (Docker/production), fall back to dev source
        installed_dir = Path(settings.BASE_DIR) / "components_data" / "static" / "design" / "themes"
        components_root = Path(
            getattr(settings, "SPWIG_COMPONENTS_DIR", str(Path(settings.BASE_DIR) / "components"))
        )
        components_dir = components_root / "themes"

        if update_all:
            themes = Theme.objects.all()
            if not themes.exists():
                self.stdout.write(self.style.WARNING("No themes found in database"))
                return
        else:
            themes = Theme.objects.filter(slug=theme_slug)
            if not themes.exists():
                raise CommandError(f'Theme "{theme_slug}" not found in database')

        updated_count = 0
        for theme in themes:
            # Try installed location first (has theme/ subdirectory structure)
            # Require tokens.css to be present — if only theme.css exists (partial migration),
            # fall back to the dev source which has the complete set of CSS files.
            installed_base = installed_dir / theme.slug / "current" / "theme"
            installed_css_dir = installed_base / "css"
            if (
                installed_base.exists()
                and installed_css_dir.exists()
                and (installed_css_dir / "tokens.css").exists()
            ):
                theme_base_dir = installed_base
            else:
                # Dev source: flat layout (files directly in theme dir)
                # Legacy fallback: version subfolder
                flat_dir = components_dir / theme.slug
                if (flat_dir / "tokens.json").exists() or (flat_dir / "css").exists():
                    theme_base_dir = flat_dir
                elif version and (flat_dir / version).exists():
                    theme_base_dir = flat_dir / version
                else:
                    theme_base_dir = flat_dir

            theme_dir = theme_base_dir / "css"

            if not theme_dir.exists():
                self.stdout.write(
                    self.style.WARNING(
                        f"CSS directory not found for {theme.slug} v{version}: {theme_dir}"
                    )
                )
                continue

            # Load and update tokens.json into manifest
            tokens_path = theme_base_dir / "tokens.json"
            if tokens_path.exists():
                tokens_data = json.loads(tokens_path.read_text())
                # Update manifest with new tokens
                manifest = theme.manifest or {}
                manifest["tokens"] = tokens_data
                theme.manifest = manifest
                self.stdout.write(f"  ✓ Loaded tokens.json ({len(tokens_data)} sections)")
            else:
                self.stdout.write("  - Skipped tokens.json (not found)")

            # Collect CSS files in the correct order
            css_files = ["tokens.css", "reset.css", "components.css", "theme.css"]
            combined_css = []

            for css_file in css_files:
                css_path = theme_dir / css_file
                if css_path.exists():
                    css_content = css_path.read_text()
                    combined_css.append(f"/* {css_file} */\n{css_content}")
                    self.stdout.write(f"  ✓ Loaded {css_file} ({len(css_content)} bytes)")
                else:
                    self.stdout.write(f"  - Skipped {css_file} (not found)")

            if not combined_css:
                self.stdout.write(
                    self.style.WARNING(f"No CSS files found for {theme.slug} v{version}")
                )
                continue

            compiled_css = "\n\n".join(combined_css)

            # Strip relative @import statements (keep external font imports like Google Fonts)
            compiled_css = re.sub(
                r'@import\s+url\([\'"]?(?!https?://)[^\'")\s]+[\'"]?\)\s*;?\s*\n?', "", compiled_css
            )

            css_hash = hashlib.md5(compiled_css.encode()).hexdigest()[:8]

            if dry_run:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"[DRY RUN] Would update {theme.slug}: "
                        f"{len(compiled_css)} bytes, hash={css_hash}"
                    )
                )
            else:
                # Update theme with new CSS and manifest (with tokens)
                theme.compiled_css = compiled_css
                theme.css_hash = css_hash
                theme.save(update_fields=["compiled_css", "css_hash", "manifest"])
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ Updated {theme.slug}: {len(compiled_css)} bytes, hash={css_hash}"
                    )
                )
                updated_count += 1

        self.stdout.write("")
        self.stdout.write("=" * 50)
        if dry_run:
            self.stdout.write(f"[DRY RUN] Would update: {len(themes)} theme(s)")
        else:
            self.stdout.write(self.style.SUCCESS(f"✓ Updated: {updated_count} theme(s)"))

            # Ensure starter theme is set as default and active
            self._ensure_starter_theme_active()

    def _ensure_starter_theme_active(self):
        """Ensure the starter theme is set as the default active theme."""
        starter_theme = Theme.objects.filter(slug="starter").first()

        if not starter_theme:
            self.stdout.write(self.style.WARNING("Starter theme not found in database"))
            return

        # Ensure starter theme is marked as default
        if not starter_theme.is_default:
            Theme.objects.filter(is_default=True).update(is_default=False)
            starter_theme.is_default = True
            starter_theme.save(update_fields=["is_default"])
            self.stdout.write("  ✓ Set starter theme as default")

        # Ensure starter theme is active in GlobalDesignSettings
        settings_obj = GlobalDesignSettings.get_settings()
        if settings_obj.active_theme != starter_theme:
            settings_obj.active_theme = starter_theme
            settings_obj.save(update_fields=["active_theme"])
            self.stdout.write("  ✓ Set starter theme as active in GlobalDesignSettings")
        else:
            self.stdout.write("  ✓ Starter theme already active")
