"""
Management command to validate that all {{% mtrans %}} strings in templates
are registered in UI_STRING_REGISTRY (and thus extractable to .po files).

Usage:
    python manage.py validate_mtrans_coverage
    python manage.py validate_mtrans_coverage --strict  # exit code 1 if gaps found
"""
import os
import re
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Validate that all {{% mtrans %}} template strings are in UI_STRING_REGISTRY'

    def add_arguments(self, parser):
        parser.add_argument(
            '--strict',
            action='store_true',
            help='Exit with code 1 if any template strings are missing from registry',
        )

    def handle(self, *args, **options):
        from translations.ui_string_registry import UI_STRING_REGISTRY

        registry_values = set(UI_STRING_REGISTRY.values())
        base_dir = Path(settings.BASE_DIR)

        # Scan all HTML templates for {{% mtrans %}} usage
        template_strings = {}  # string -> list of file paths
        skip_dirs = {
            'shop_venv', 'staticfiles', 'media', '.git',
            'node_modules', 'catalog_gen', 'catalog_output',
        }

        for root, dirs, files in os.walk(base_dir):
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            for f in files:
                if not f.endswith('.html'):
                    continue
                filepath = os.path.join(root, f)
                try:
                    with open(filepath, 'r') as fh:
                        content = fh.read()
                except (OSError, UnicodeDecodeError):
                    continue

                for m in re.finditer(
                    r"""\{%\s*mtrans\s+(['"])(.*?)\1\s*(?:as\s+\w+\s*)?%\}""",
                    content,
                ):
                    quote_char = m.group(1)
                    string = m.group(2)
                    # Unescape escaped quotes (matches do_mtrans runtime behaviour)
                    string = string.replace('\\' + quote_char, quote_char)
                    if string not in template_strings:
                        template_strings[string] = []
                    rel_path = os.path.relpath(filepath, base_dir)
                    if rel_path not in template_strings[string]:
                        template_strings[string].append(rel_path)

                # Also check for {% mtrans that span attributes etc.

        # Compare
        template_set = set(template_strings.keys())
        missing_from_registry = template_set - registry_values
        registry_only = registry_values - template_set

        self.stdout.write(f'\nUnique {{% mtrans %}} strings in templates: {len(template_set)}')
        self.stdout.write(f'Strings in UI_STRING_REGISTRY: {len(registry_values)}')

        if missing_from_registry:
            self.stdout.write(self.style.ERROR(
                f'\nMISSING from registry ({len(missing_from_registry)} strings):'
            ))
            for s in sorted(missing_from_registry):
                files = template_strings[s]
                self.stdout.write(f'  "{s}"')
                for f in files[:3]:
                    self.stdout.write(f'    <- {f}')
        else:
            self.stdout.write(self.style.SUCCESS(
                '\nAll template {{% mtrans %}} strings are in the registry.'
            ))

        if registry_only:
            self.stdout.write(f'\nRegistry-only strings (not in templates, may be JS/Python): {len(registry_only)}')

        coverage = len(template_set - missing_from_registry)
        total = len(template_set)
        pct = (coverage / total * 100) if total else 100
        self.stdout.write(f'\nCoverage: {coverage}/{total} ({pct:.0f}%)')

        if options['strict'] and missing_from_registry:
            raise SystemExit(1)
