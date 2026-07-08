"""
Management command to generate tokens.css from tokens.json

Delegates all CSS generation logic to design.services.token_css_generator.
See that module for the full documentation on naming conventions and prefixes.
"""
import json
from pathlib import Path

from django.core.management.base import BaseCommand
from django.conf import settings

from design.services.token_css_generator import generate_tokens_css


class Command(BaseCommand):
    help = 'Generates tokens.css from tokens.json for themes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--theme',
            type=str,
            help='Generate for specific theme by slug (e.g., modern-shop)',
        )
        parser.add_argument(
            '--theme-version',
            type=str,
            default=None,
            help='Legacy: theme version subfolder (ignored for flat layout)',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Generate for all themes',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be generated without writing files',
        )

    def handle(self, *args, **options):
        components_root = Path(getattr(
            settings, 'SPWIG_COMPONENTS_DIR',
            str(Path(settings.BASE_DIR) / 'components')
        ))
        themes_dir = components_root / 'themes'
        theme_slug = options.get('theme')
        version = options.get('theme_version')
        process_all = options.get('all')
        dry_run = options.get('dry_run')

        if not theme_slug and not process_all:
            self.stdout.write(self.style.ERROR(
                'Please specify --theme <slug> or --all'
            ))
            return

        # Get themes to process
        if process_all:
            theme_dirs = [d for d in themes_dir.iterdir() if d.is_dir()]
        else:
            theme_dirs = [themes_dir / theme_slug]

        generated_count = 0
        failed_count = 0

        for theme_dir in theme_dirs:
            if not theme_dir.exists():
                self.stdout.write(self.style.ERROR(
                    f"Theme directory not found: {theme_dir}"
                ))
                failed_count += 1
                continue

            theme_name = theme_dir.name

            # Flat layout: tokens.json directly in theme dir
            # Legacy fallback: tokens.json in a version subfolder
            component_dir = theme_dir
            if (theme_dir / 'tokens.json').exists():
                component_dir = theme_dir
            elif version and (theme_dir / version).exists():
                component_dir = theme_dir / version
            else:
                self.stdout.write(self.style.WARNING(
                    f"No tokens.json found for {theme_name}, skipping"
                ))
                continue

            tokens_json_path = component_dir / 'tokens.json'
            if not tokens_json_path.exists():
                self.stdout.write(self.style.WARNING(
                    f"No tokens.json found for {theme_name}, skipping"
                ))
                continue

            # Read manifest to determine dark_mode_enabled
            dark_mode_enabled = False
            manifest_path = component_dir / 'manifest.json'
            if manifest_path.exists():
                try:
                    manifest_data = json.loads(manifest_path.read_text())
                    features = manifest_data.get('features', {})
                    if isinstance(features, dict):
                        dark_mode_enabled = features.get('dark_mode', False)
                except (json.JSONDecodeError, KeyError):
                    pass

            # Generate tokens.css using the standalone service function
            try:
                css_content = generate_tokens_css(
                    tokens_json_path, theme_name,
                    dark_mode_enabled=dark_mode_enabled,
                )

                css_dir = component_dir / 'css'
                css_dir.mkdir(parents=True, exist_ok=True)
                tokens_css_path = css_dir / 'tokens.css'

                if dry_run:
                    self.stdout.write(self.style.SUCCESS(
                        f"\n{'='*60}\n"
                        f"Would generate: {tokens_css_path}\n"
                        f"{'='*60}\n"
                        f"{css_content[:500]}...\n"
                    ))
                else:
                    tokens_css_path.write_text(css_content)
                    self.stdout.write(self.style.SUCCESS(
                        f"✓ Generated: {tokens_css_path}"
                    ))

                generated_count += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"✗ Failed to generate for {theme_name}: {e}"
                ))
                failed_count += 1

        # Summary
        self.stdout.write("\n" + "="*50)
        self.stdout.write(self.style.SUCCESS(f"✓ Generated: {generated_count}"))
        if failed_count > 0:
            self.stdout.write(self.style.ERROR(f"✗ Failed: {failed_count}"))
        self.stdout.write("="*50 + "\n")
