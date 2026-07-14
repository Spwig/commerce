"""
Management command to compile utility translations
"""

import subprocess
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Compile Page Builder Utilities translation files (.po to .mo)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--locale",
            "-l",
            dest="locale",
            help="Locale to compile (e.g., de, es, fr). If not specified, compiles all locales.",
        )

    def handle(self, *args, **options):
        # Path to utilities locale directory
        utilities_path = Path(settings.BASE_DIR) / "page_builder" / "utilities" / "locale"

        if not utilities_path.exists():
            raise CommandError(f"Utilities locale directory does not exist: {utilities_path}")

        locale = options.get("locale")

        # Specific locale if requested, otherwise all available
        locales_to_compile = [locale] if locale else ["de", "en", "es", "fr", "ja", "pt", "zh-hans"]

        compiled_count = 0
        errors = []

        for locale_code in locales_to_compile:
            locale_dir = utilities_path / locale_code / "LC_MESSAGES"
            po_file = locale_dir / "utilities.po"
            mo_file = locale_dir / "utilities.mo"

            if not po_file.exists():
                self.stdout.write(
                    self.style.WARNING(f"Skipping {locale_code}: {po_file} does not exist")
                )
                continue

            try:
                # Compile .po to .mo using msgfmt
                subprocess.run(
                    ["msgfmt", "-o", str(mo_file), str(po_file)],
                    capture_output=True,
                    text=True,
                    check=True,
                )

                compiled_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"✓ Compiled {locale_code}: {po_file.name} → {mo_file.name}")
                )

            except subprocess.CalledProcessError as e:
                errors.append(f"{locale_code}: {e.stderr}")
                self.stdout.write(
                    self.style.ERROR(f"✗ Failed to compile {locale_code}: {e.stderr}")
                )
            except FileNotFoundError:
                self.stdout.write(
                    self.style.ERROR(
                        "msgfmt command not found. Please install gettext tools:\n"
                        "  Ubuntu/Debian: sudo apt-get install gettext\n"
                        "  macOS: brew install gettext\n"
                        "  Windows: Use WSL or install gettext from GnuWin32"
                    )
                )
                return

        # Summary
        self.stdout.write("")
        if compiled_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f"Successfully compiled {compiled_count} translation file(s)")
            )

        if errors:
            self.stdout.write(self.style.ERROR(f"Failed to compile {len(errors)} file(s)"))
            for error in errors:
                self.stdout.write(self.style.ERROR(f"  - {error}"))

        # Add locale path to Django settings reminder
        self.stdout.write("")
        self.stdout.write(
            self.style.WARNING("Remember to add the utilities locale path to your Django settings:")
        )
        self.stdout.write(
            "LOCALE_PATHS = [\n    ...,\n    BASE_DIR / 'page_builder' / 'utilities' / 'locale',\n]"
        )
