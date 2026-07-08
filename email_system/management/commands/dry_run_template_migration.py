"""
Dry run for email template migration - validates all markdown files without database changes.
Usage: python manage.py dry_run_template_migration
"""

import os
import re
import glob
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = 'Dry run: Validate all email template markdown files before migration'

    # Supported language codes (16 non-English languages)
    LANGUAGE_CODES = ['ar', 'de', 'es', 'fr', 'hi', 'id', 'it', 'ja',
                      'ko', 'pt', 'ru', 'th', 'tr', 'vi', 'zh-hans', 'zh-hant']

    # System files to exclude
    EXCLUDE_FILES = ['INDEX.md', 'PROGRESS.md', 'README.md']

    def __init__(self):
        super().__init__()
        self.template_dir = os.path.join(
            str(settings.BASE_DIR), 'email_templates_for_translation'
        )
        self.errors = []
        self.warnings = []
        self.stats = {
            'base_files_found': 0,
            'base_files_parsed': 0,
            'translations_found': 0,
            'translations_parsed': 0,
            'missing_translations': 0,
            'parse_errors': 0,
            'validation_errors': 0,
        }

    def add_arguments(self, parser):
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed parsing information for each file',
        )
        parser.add_argument(
            '--check-colors',
            action='store_true',
            help='Check for hardcoded colors (slower)',
        )

    def handle(self, *args, **options):
        verbose = options.get('verbose', False)
        check_colors = options.get('check_colors', False)

        self.stdout.write("\n" + "="*70)
        self.stdout.write("🧪 DRY RUN: Email Template Migration Validation")
        self.stdout.write("="*70 + "\n")

        # Step 1: Discover English base files
        self.stdout.write("📂 Step 1: Discovering English base template files...")
        base_files = self.get_english_base_files()
        self.stats['base_files_found'] = len(base_files)
        self.stdout.write(f"   ✓ Found {len(base_files)} English base files\n")

        # Step 2: Parse and validate each base file
        self.stdout.write("📝 Step 2: Parsing and validating base templates...")
        base_templates = {}

        for i, filepath in enumerate(base_files, 1):
            filename = os.path.basename(filepath)
            template_name = filename.replace('.md', '')

            if verbose:
                self.stdout.write(f"   [{i}/{len(base_files)}] Parsing {filename}...")

            # Parse English base
            data = self.parse_markdown_template(filepath)

            if 'error' in data:
                self.errors.append(f"❌ {filename}: {data['error']}")
                self.stats['parse_errors'] += 1
                continue

            # Validate required fields
            validation_result = self.validate_template_data(data, filename)
            if validation_result:
                self.errors.append(validation_result)
                self.stats['validation_errors'] += 1
                continue

            # Check for hardcoded colors if requested
            if check_colors:
                color_issues = self.check_hardcoded_colors(data['html_content'], filename)
                if color_issues:
                    self.warnings.extend(color_issues)

            base_templates[template_name] = data
            self.stats['base_files_parsed'] += 1

            if verbose:
                self.stdout.write(f"      ✓ {data['template_type']}")

        self.stdout.write(f"   ✓ Successfully parsed {self.stats['base_files_parsed']}/{self.stats['base_files_found']} base templates\n")

        # Step 3: Check translations for each base template
        self.stdout.write("🌍 Step 3: Checking translations for each template...")

        for template_name, base_data in base_templates.items():
            base_filepath = os.path.join(self.template_dir, f"{template_name}.md")

            for lang_code in self.LANGUAGE_CODES:
                translation_file = base_filepath.replace('.md', f'.{lang_code}.md')

                if not os.path.exists(translation_file):
                    self.warnings.append(f"⚠️  Missing: {template_name}.{lang_code}.md")
                    self.stats['missing_translations'] += 1
                    continue

                self.stats['translations_found'] += 1

                # Parse translation
                trans_data = self.parse_markdown_template(translation_file)

                if 'error' in trans_data:
                    self.errors.append(f"❌ {template_name}.{lang_code}.md: {trans_data['error']}")
                    self.stats['parse_errors'] += 1
                    continue

                # Validate translation has same structure as base
                validation_result = self.validate_translation(trans_data, base_data, template_name, lang_code)
                if validation_result:
                    self.errors.append(validation_result)
                    self.stats['validation_errors'] += 1
                    continue

                self.stats['translations_parsed'] += 1

        self.stdout.write(f"   ✓ Found {self.stats['translations_found']} translation files")
        self.stdout.write(f"   ✓ Successfully parsed {self.stats['translations_parsed']} translations\n")

        # Step 4: Print summary report
        self.print_summary_report(check_colors)

        # Return exit code based on errors
        if self.errors:
            return 1  # Exit with error code
        return 0

    def get_english_base_files(self):
        """Get all English base template files (excluding translations and system files)"""
        all_md_files = glob.glob(os.path.join(self.template_dir, '*.md'))

        base_files = []
        for filepath in all_md_files:
            filename = os.path.basename(filepath)

            # Exclude system files
            if filename in self.EXCLUDE_FILES:
                continue

            # Exclude translation files (have language suffix before .md)
            has_lang_suffix = any(filename.endswith(f'.{lang}.md') for lang in self.LANGUAGE_CODES)
            if has_lang_suffix:
                continue

            base_files.append(filepath)

        return sorted(base_files)

    def parse_markdown_template(self, filepath):
        """Parse markdown template file and extract all components"""
        result = {}

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {'error': f'Failed to read file: {str(e)}'}

        # Extract YAML frontmatter
        yaml_match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if yaml_match:
            frontmatter = yaml_match.group(1)

            # Extract template_type
            type_match = re.search(r'template_type:\s*(.+)', frontmatter)
            if type_match:
                result['template_type'] = type_match.group(1).strip()

            # Extract category
            cat_match = re.search(r'category:\s*(.+)', frontmatter)
            if cat_match:
                result['category'] = cat_match.group(1).strip()
        else:
            return {'error': 'Missing YAML frontmatter'}

        # Extract subject (between ## Subject and next ## or blank lines)
        subject_match = re.search(r'## Subject\s*\n(.+?)(?=\n\n|\n##)', content, re.DOTALL)
        if subject_match:
            result['subject'] = subject_match.group(1).strip()
        else:
            return {'error': 'Missing ## Subject section'}

        # Extract HTML content (between ## HTML Content and next section)
        html_match = re.search(r'## HTML Content\s*\n(.+?)(?=\n## (?:Text Content|Variables|Notes)|$)', content, re.DOTALL)
        if html_match:
            result['html_content'] = html_match.group(1).strip()
        else:
            return {'error': 'Missing ## HTML Content section'}

        # Extract text content (optional - between ## Text Content and next section)
        text_match = re.search(r'## Text Content\s*\n(.+?)(?=\n## (?:Variables|Notes)|$)', content, re.DOTALL)
        if text_match:
            result['text_content'] = text_match.group(1).strip()
        else:
            result['text_content'] = ''  # Text content is optional

        return result

    def validate_template_data(self, data, filename):
        """Validate that template data has all required fields"""

        if 'template_type' not in data or not data['template_type']:
            return f"❌ {filename}: Missing or empty template_type"

        if 'subject' not in data or not data['subject']:
            return f"❌ {filename}: Missing or empty subject"

        if 'html_content' not in data or not data['html_content']:
            return f"❌ {filename}: Missing or empty HTML content"

        # Check that HTML content looks like MJML
        if '<mjml>' not in data['html_content'].lower():
            return f"❌ {filename}: HTML content doesn't appear to be MJML (missing <mjml> tag)"

        return None  # No errors

    def validate_translation(self, trans_data, base_data, template_name, lang_code):
        """Validate that translation has same structure as base template"""

        # Check template_type matches
        if trans_data.get('template_type') != base_data.get('template_type'):
            return f"❌ {template_name}.{lang_code}.md: template_type mismatch (base: {base_data.get('template_type')}, translation: {trans_data.get('template_type')})"

        # Count Django variables in base and translation
        base_vars = set(re.findall(r'\{\{[\s\w\.\|:\'"]+\}\}', base_data['subject'] + base_data['html_content']))
        trans_vars = set(re.findall(r'\{\{[\s\w\.\|:\'"]+\}\}', trans_data['subject'] + trans_data['html_content']))

        # Check if translation has significantly fewer variables (might indicate translation error)
        if len(trans_vars) < len(base_vars) * 0.8:  # Allow 20% tolerance
            return f"⚠️  {template_name}.{lang_code}.md: Variable count mismatch (base: {len(base_vars)}, translation: {len(trans_vars)})"

        return None  # No errors

    def check_hardcoded_colors(self, html_content, filename):
        """Check for hardcoded hex colors that aren't in theme tokens"""
        issues = []

        # Find all hex colors
        color_pattern = re.compile(r'#[0-9a-fA-F]{3,6}')
        theme_pattern = re.compile(r'\{\{\s*theme\.')

        matches = color_pattern.finditer(html_content)

        for match in matches:
            color = match.group()
            start = max(0, match.start() - 100)
            end = min(len(html_content), match.end() + 100)
            context = html_content[start:end]

            # Check if this color is inside a theme token
            if not theme_pattern.search(context):
                issues.append(f"⚠️  {filename}: Hardcoded color {color} at position {match.start()}")

        return issues

    def print_summary_report(self, check_colors):
        """Print final summary report"""
        self.stdout.write("\n" + "="*70)
        self.stdout.write("📊 DRY RUN SUMMARY REPORT")
        self.stdout.write("="*70 + "\n")

        # Statistics
        self.stdout.write("📈 Statistics:")
        self.stdout.write(f"   • English base files found:    {self.stats['base_files_found']}")
        self.stdout.write(f"   • English base files parsed:   {self.stats['base_files_parsed']}")
        self.stdout.write(f"   • Translation files found:     {self.stats['translations_found']}")
        self.stdout.write(f"   • Translation files parsed:    {self.stats['translations_parsed']}")
        self.stdout.write(f"   • Missing translations:        {self.stats['missing_translations']}")

        expected_translations = self.stats['base_files_parsed'] * 16
        self.stdout.write(f"\n   Expected translations:         {expected_translations}")
        self.stdout.write(f"   Actual translations found:     {self.stats['translations_found']}")
        self.stdout.write(f"   Coverage:                      {(self.stats['translations_found']/expected_translations*100):.1f}%")

        # Total records that would be created
        total_records = self.stats['base_files_parsed'] + self.stats['translations_parsed']
        self.stdout.write(f"\n   📦 Total database records to create: {total_records}")
        self.stdout.write(f"      ({self.stats['base_files_parsed']} base + {self.stats['translations_parsed']} translations)")

        # Errors
        self.stdout.write(f"\n❌ Errors: {len(self.errors)}")
        if self.errors:
            self.stdout.write("\n   Critical errors that would cause migration to fail:")
            for error in self.errors[:20]:  # Show first 20
                self.stdout.write(f"   {error}")
            if len(self.errors) > 20:
                self.stdout.write(f"   ... and {len(self.errors) - 20} more errors")

        # Warnings
        self.stdout.write(f"\n⚠️  Warnings: {len(self.warnings)}")
        if self.warnings:
            self.stdout.write("\n   Non-critical warnings:")
            for warning in self.warnings[:20]:  # Show first 20
                self.stdout.write(f"   {warning}")
            if len(self.warnings) > 20:
                self.stdout.write(f"   ... and {len(self.warnings) - 20} more warnings")

        # Final verdict
        self.stdout.write("\n" + "="*70)
        if self.errors:
            self.stdout.write(self.style.ERROR("\n❌ DRY RUN FAILED"))
            self.stdout.write(self.style.ERROR(f"   Found {len(self.errors)} critical errors that must be fixed"))
            self.stdout.write(self.style.ERROR("   before running the actual migration.\n"))
        else:
            self.stdout.write(self.style.SUCCESS("\n✅ DRY RUN PASSED"))
            self.stdout.write(self.style.SUCCESS(f"   All {self.stats['base_files_parsed']} base templates validated"))
            self.stdout.write(self.style.SUCCESS(f"   All {self.stats['translations_parsed']} translations validated"))
            if self.warnings:
                self.stdout.write(self.style.WARNING(f"   Found {len(self.warnings)} warnings (non-critical)"))
            self.stdout.write(self.style.SUCCESS("\n   ✓ Ready to proceed with migration!\n"))

        self.stdout.write("="*70 + "\n")
