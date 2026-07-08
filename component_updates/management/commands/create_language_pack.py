"""
Create a language pack template or package for distribution.

This command has two modes:

1. Template mode (--output): Generate a directory with blank .po files,
   ui_strings template, and help content templates for translators to fill in.

2. Package mode (--source --package): Compile a completed translation
   directory into a distributable ZIP for the update server.

Usage:
    # Generate a blank template for Swahili:
    python manage.py create_language_pack sw --output /tmp/language-pack-sw/

    # Package a completed translation:
    python manage.py create_language_pack sw --source /tmp/language-pack-sw/ --package

    # Generate template with auto-populated language metadata:
    python manage.py create_language_pack sw --output /tmp/language-pack-sw/ --version 1.0.0
"""
import json
import os
import shutil
import subprocess
import zipfile
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from component_updates.language_pack_installer import LOCALE_APP_NAMES


class Command(BaseCommand):
    help = 'Create a language pack template or package for a target language'

    def add_arguments(self, parser):
        parser.add_argument(
            'language_code',
            type=str,
            help='Target language code (e.g. sw, pl, uk)',
        )
        parser.add_argument(
            '--output',
            type=str,
            help='Output directory for generating a blank template',
        )
        parser.add_argument(
            '--source',
            type=str,
            help='Source directory of completed translations (for packaging)',
        )
        parser.add_argument(
            '--package',
            action='store_true',
            help='Package the source directory into a distributable ZIP',
        )
        parser.add_argument(
            '--pack-version',
            type=str,
            default='1.0.0',
            help='Pack version (default: 1.0.0)',
        )
        parser.add_argument(
            '--skip-makemessages',
            action='store_true',
            help='Skip running makemessages (use existing .po files)',
        )

    def handle(self, *args, **options):
        lang_code = options['language_code']
        version = options['pack_version']

        if options['output']:
            self._generate_template(lang_code, options['output'], version, options)
        elif options['source'] and options['package']:
            self._package(lang_code, options['source'], version)
        else:
            raise CommandError(
                'Specify --output to generate a template, '
                'or --source with --package to create a ZIP'
            )

    def _generate_template(self, lang_code: str, output_dir: str, version: str, options: dict):
        """Generate a blank language pack template for translators."""
        output = Path(output_dir)
        if output.exists():
            raise CommandError(f'Output directory already exists: {output}')

        output.mkdir(parents=True)
        base_dir = Path(settings.BASE_DIR)
        self.stdout.write(f'Generating language pack template for "{lang_code}" in {output}')

        # --- 1. Generate .po files via makemessages ---
        locale_output = output / 'locale'
        locale_output.mkdir()
        po_count = 0

        if not options.get('skip_makemessages'):
            self.stdout.write('\nGenerating .po files...')
            po_count = self._generate_po_files(lang_code, locale_output, base_dir)
        else:
            self.stdout.write('\nCollecting existing .po files...')
            po_count = self._collect_existing_po_files(lang_code, locale_output, base_dir)

        self.stdout.write(f'  {po_count} .po files generated')

        # --- 2. Export UI string registry template ---
        self.stdout.write('\nExporting UI string registry...')
        self._export_ui_strings_template(lang_code, output)

        # --- 3. Copy English help files as templates ---
        self.stdout.write('\nCopying help content templates...')
        help_count = self._copy_help_templates(lang_code, output, base_dir)
        self.stdout.write(f'  {help_count} help files copied')

        # --- 4. Copy English email templates as templates ---
        self.stdout.write('\nCopying email template files...')
        email_count = self._copy_email_templates(lang_code, output, base_dir)
        self.stdout.write(f'  {email_count} email templates copied')

        # --- 5. Generate language_meta.json ---
        self.stdout.write('\nGenerating language_meta.json...')
        self._generate_language_meta(lang_code, output)

        # --- 6. Generate manifest.json ---
        self._generate_manifest(lang_code, version, output, po_count, help_count, email_count)

        self.stdout.write(self.style.SUCCESS(
            f'\nTemplate generated at: {output}\n'
            f'Next steps for translators:\n'
            f'  1. Translate .po files in locale/ using Poedit or similar\n'
            f'  2. Fill in translations in ui_strings.json\n'
            f'  3. Translate help .md files in help_content/\n'
            f'  4. Translate email templates in email_templates/\n'
            f'  5. Review language_meta.json (name, native_name, flag, rtl)\n'
            f'  6. Package: python manage.py create_language_pack {lang_code} '
            f'--source {output} --package'
        ))

    def _generate_po_files(self, lang_code: str, locale_output: Path, base_dir: Path) -> int:
        """Run makemessages for each app and collect the generated .po files."""
        count = 0
        python = str(base_dir / 'shop_venv' / 'bin' / 'python')

        for app_name in LOCALE_APP_NAMES:
            app_dir = base_dir / app_name
            if not app_dir.is_dir():
                continue

            # Ensure locale dir exists
            app_locale = app_dir / 'locale'
            app_locale.mkdir(exist_ok=True)

            try:
                subprocess.run(
                    [python, str(base_dir / 'manage.py'), 'makemessages',
                     '-l', lang_code, '--no-location'],
                    cwd=str(app_dir),
                    capture_output=True,
                    timeout=60,
                )
            except (subprocess.TimeoutExpired, Exception) as e:
                self.stdout.write(self.style.WARNING(f'  makemessages failed for {app_name}: {e}'))
                continue

            # Copy the generated .po file to the output
            src_po = app_locale / lang_code / 'LC_MESSAGES' / 'django.po'
            if src_po.exists():
                dest_dir = locale_output / app_name / lang_code / 'LC_MESSAGES'
                dest_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_po, dest_dir / 'django.po')
                count += 1

                # Clean up the generated file from the app directory
                # (we only want it in the pack output, not committed)
                shutil.rmtree(app_locale / lang_code)

        # Also handle page builder elements
        elements_dir = base_dir / 'page_builder' / 'templates' / 'page_builder' / 'elements'
        if elements_dir.is_dir():
            for element_path in elements_dir.iterdir():
                if not element_path.is_dir():
                    continue
                element_locale = element_path / 'locale'
                if not element_locale.is_dir():
                    continue

                # Check if there are any existing locale dirs (meaning this element has strings)
                if not any(d.is_dir() for d in element_locale.iterdir()):
                    continue

                try:
                    subprocess.run(
                        [python, str(base_dir / 'manage.py'), 'makemessages',
                         '-l', lang_code, '--no-location'],
                        cwd=str(element_path),
                        capture_output=True,
                        timeout=60,
                    )
                except Exception:
                    continue

                src_po = element_locale / lang_code / 'LC_MESSAGES' / 'django.po'
                if src_po.exists():
                    dest_dir = (locale_output / 'page_builder_elements' /
                                lang_code / element_path.name / 'LC_MESSAGES')
                    dest_dir.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src_po, dest_dir / 'django.po')
                    count += 1

                    # Clean up
                    shutil.rmtree(element_locale / lang_code)

        return count

    def _collect_existing_po_files(self, lang_code: str, locale_output: Path, base_dir: Path) -> int:
        """Collect already-existing .po files for the language (skip makemessages)."""
        count = 0
        for app_name in LOCALE_APP_NAMES:
            src_po = base_dir / app_name / 'locale' / lang_code / 'LC_MESSAGES' / 'django.po'
            if src_po.exists():
                dest_dir = locale_output / app_name / lang_code / 'LC_MESSAGES'
                dest_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_po, dest_dir / 'django.po')
                count += 1
        return count

    def _export_ui_strings_template(self, lang_code: str, output: Path):
        """Export UI_STRING_REGISTRY as a JSON template for translators."""
        from translations.ui_string_registry import UI_STRING_REGISTRY, UI_STRING_SECTIONS

        strings = {}
        for key, english_source in sorted(UI_STRING_REGISTRY.items()):
            strings[key] = ''  # Empty — translator fills this in

        data = {
            'format_version': '1.0',
            'language_code': lang_code,
            'total_strings': len(strings),
            'sections': {k: str(v) for k, v in UI_STRING_SECTIONS.items()},
            'strings': strings,
            '_reference': {
                key: english_source
                for key, english_source in sorted(UI_STRING_REGISTRY.items())
            },
        }

        with open(output / 'ui_strings.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        self.stdout.write(f'  {len(strings)} UI strings exported')

    def _copy_help_templates(self, lang_code: str, output: Path, base_dir: Path) -> int:
        """Copy English help .md files as templates for the target language."""
        help_src = base_dir / 'help_content'
        help_dest = output / 'help_content'
        count = 0

        if not help_src.is_dir():
            return 0

        # Find all English source .md files (no language suffix)
        for md_file in help_src.rglob('*.md'):
            stem = md_file.stem
            if '.' in stem:
                # Skip existing translation files
                continue

            relative = md_file.relative_to(help_src)
            # Create the target language version
            dest_file = help_dest / relative.parent / f'{stem}.{lang_code}.md'
            dest_file.parent.mkdir(parents=True, exist_ok=True)

            # Copy English content as a reference for the translator
            content = md_file.read_text(encoding='utf-8')
            header = (
                f'---\n'
                f'# TRANSLATOR: Replace this content with the {lang_code} translation.\n'
                f'# The English source is provided below as reference.\n'
                f'# Keep the YAML frontmatter fields (title, etc.) and translate their values.\n'
                f'---\n\n'
            )
            dest_file.write_text(header + content, encoding='utf-8')
            count += 1

        return count

    def _generate_language_meta(self, lang_code: str, output: Path):
        """Generate language_meta.json from populate_languages data."""
        from translations.management.commands.populate_languages import Command as PopCmd

        pop = PopCmd()
        lang_data = pop.M2M100_LANGUAGES.get(lang_code)
        nllb_data = pop.NLLB_ONLY.get(lang_code)

        if lang_data:
            name, native_name, flag, rtl = lang_data
            m2m100_support = 'limited' if lang_code in pop.LIMITED_M2M100 else 'full'
            nllb_support = 'full'  # All M2M100 languages have full NLLB support
        elif nllb_data:
            name, native_name, flag, rtl = nllb_data
            m2m100_support = 'none'
            nllb_support = 'full'
        else:
            name = lang_code
            native_name = lang_code
            flag = ''
            rtl = False
            m2m100_support = 'none'
            nllb_support = 'none'

        meta = {
            'code': lang_code,
            'name': name,
            'native_name': native_name,
            'rtl': rtl,
            'flag': flag,
            'date_format': 'd/m/Y',
            'time_format': 'H:i',
            'm2m100_support': m2m100_support,
            'nllb_support': nllb_support,
        }

        with open(output / 'language_meta.json', 'w', encoding='utf-8') as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)

        self.stdout.write(f'  {name} ({native_name}) — RTL: {rtl}, flag: {flag}')

    def _copy_email_templates(self, lang_code: str, output: Path, base_dir: Path) -> int:
        """Copy English email template files as templates for the target language."""
        email_src = base_dir / 'email_templates_for_translation'
        email_dest = output / 'email_templates'
        count = 0

        if not email_src.is_dir():
            return 0

        email_dest.mkdir(exist_ok=True)
        exclude_files = {'INDEX.md', 'PROGRESS.md', 'README.md'}

        for md_file in sorted(email_src.glob('*.md')):
            filename = md_file.name

            # Skip system files
            if filename in exclude_files:
                continue

            # Skip existing translation files (only copy English sources)
            if '.' in filename.rsplit('.md', 1)[0]:
                continue

            template_name = filename.replace('.md', '')
            dest_file = email_dest / f'{template_name}.{lang_code}.md'

            # Copy English content as reference
            content = md_file.read_text(encoding='utf-8')
            header = (
                f'---\n'
                f'# TRANSLATOR: Translate the Subject, HTML text content,\n'
                f'# and Text Content sections below into {lang_code}.\n'
                f'# Keep all YAML frontmatter, Django template tags ({{% %}}, '
                f'{{{{ }}}}) and MJML tags (<mj-*>) EXACTLY as-is.\n'
                f'# Only translate human-readable text.\n'
                f'# The English source is provided below as reference.\n'
                f'---\n\n'
            )
            # Replace the original frontmatter with the translator header +
            # original frontmatter content so template_type is preserved
            dest_file.write_text(content, encoding='utf-8')
            count += 1

        return count

    def _generate_manifest(self, lang_code: str, version: str, output: Path,
                           po_count: int, help_count: int, email_count: int = 0):
        """Generate manifest.json for the language pack."""
        from translations.ui_string_registry import get_total_string_count

        # Load name from language_meta if available
        meta_file = output / 'language_meta.json'
        lang_name = lang_code
        if meta_file.exists():
            with open(meta_file) as f:
                lang_name = json.load(f).get('name', lang_code)

        manifest = {
            'slug': f'language-pack-{lang_code}',
            'name': f'{lang_name} Language Pack',
            'version': version,
            'component_type': 'language_pack',
            'description': f'Complete {lang_name} translation for Spwig admin, frontend, and help content',
            'author': 'Spwig',
            'author_email': 'translations@spwig.com',
            'language_code': lang_code,
            'requires_platform_version': '>=1.0.0',
            'coverage': {
                'po_apps': po_count,
                'ui_strings': get_total_string_count(),
                'help_topics': help_count,
                'email_templates': email_count,
            },
        }

        with open(output / 'manifest.json', 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

    def _package(self, lang_code: str, source_dir: str, version: str):
        """Package a completed translation directory into a ZIP."""
        source = Path(source_dir)
        if not source.is_dir():
            raise CommandError(f'Source directory does not exist: {source}')

        # Validate required files
        manifest_path = source / 'manifest.json'
        if not manifest_path.exists():
            raise CommandError('Source directory missing manifest.json')

        with open(manifest_path) as f:
            manifest = json.load(f)

        # Update version in manifest
        manifest['version'] = version
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

        # Compile .po files to .mo
        self.stdout.write('Compiling .po files...')
        locale_dir = source / 'locale'
        compiled = 0
        if locale_dir.is_dir():
            compiled = self._compile_po_files(locale_dir)
        self.stdout.write(f'  Compiled {compiled} .mo files')

        # Calculate coverage
        self.stdout.write('Calculating coverage...')
        coverage = self._calculate_coverage(source, lang_code)
        self.stdout.write(f'  UI strings: {coverage["ui_translated"]}/{coverage["ui_total"]}')
        self.stdout.write(f'  Help topics: {coverage["help_count"]}')
        self.stdout.write(f'  .po apps: {coverage["po_apps"]}')
        self.stdout.write(f'  Email templates: {coverage["email_count"]}')

        # Update manifest coverage
        manifest['coverage'] = {
            'po_apps': coverage['po_apps'],
            'ui_strings': coverage['ui_translated'],
            'help_topics': coverage['help_count'],
            'email_templates': coverage['email_count'],
        }
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

        # Strip _reference section from ui_strings.json (translator aid, not needed at install)
        ui_file = source / 'ui_strings.json'
        if ui_file.exists():
            with open(ui_file) as f:
                ui_data = json.load(f)
            if '_reference' in ui_data:
                del ui_data['_reference']
                with open(ui_file, 'w', encoding='utf-8') as f:
                    json.dump(ui_data, f, indent=2, ensure_ascii=False)

        # Create ZIP
        slug = manifest.get('slug', f'language-pack-{lang_code}')
        zip_name = f'{slug}-v{version}.zip'
        zip_path = source.parent / zip_name

        self.stdout.write(f'\nCreating {zip_name}...')
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path in source.rglob('*'):
                if file_path.is_file():
                    arcname = str(file_path.relative_to(source))
                    zf.write(file_path, arcname)

        size_mb = zip_path.stat().st_size / (1024 * 1024)
        self.stdout.write(self.style.SUCCESS(
            f'\nPackage created: {zip_path} ({size_mb:.1f} MB)\n'
            f'Upload to update server:\n'
            f'  python manage.py upload_update {zip_path}'
        ))

    def _compile_po_files(self, locale_dir: Path) -> int:
        """Compile all .po files to .mo using msgfmt."""
        count = 0
        for po_file in locale_dir.rglob('*.po'):
            mo_file = po_file.with_suffix('.mo')
            try:
                subprocess.run(
                    ['msgfmt', '-o', str(mo_file), str(po_file)],
                    capture_output=True,
                    check=True,
                    timeout=30,
                )
                count += 1
            except FileNotFoundError:
                # msgfmt not installed — try Django's compilemessages
                self.stdout.write(self.style.WARNING(
                    '  msgfmt not found, .mo files must be compiled manually'
                ))
                return count
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  Failed to compile {po_file}: {e}'))
        return count

    def _calculate_coverage(self, source: Path, lang_code: str) -> dict:
        """Calculate translation coverage stats."""
        # UI strings
        ui_file = source / 'ui_strings.json'
        ui_total = 0
        ui_translated = 0
        if ui_file.exists():
            with open(ui_file) as f:
                data = json.load(f)
            strings = data.get('strings', {})
            ui_total = len(strings)
            ui_translated = sum(1 for v in strings.values() if v)

        # Help content
        help_dir = source / 'help_content'
        help_count = 0
        if help_dir.is_dir():
            help_count = sum(1 for _ in help_dir.rglob(f'*.{lang_code}.md'))

        # .po files
        locale_dir = source / 'locale'
        po_apps = 0
        if locale_dir.is_dir():
            po_apps = sum(
                1 for d in locale_dir.iterdir()
                if d.is_dir() and any(d.rglob('*.po'))
            )

        # Email templates
        email_dir = source / 'email_templates'
        email_count = 0
        if email_dir.is_dir():
            email_count = sum(
                1 for _ in email_dir.glob(f'*.{lang_code}.md')
            )

        return {
            'ui_total': ui_total,
            'ui_translated': ui_translated,
            'help_count': help_count,
            'po_apps': po_apps,
            'email_count': email_count,
        }
