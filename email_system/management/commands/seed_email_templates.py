import os
import re
import glob
import logging

from core.management.commands._seed_base import SeedCommand

logger = logging.getLogger(__name__)

# Supported language codes (16 non-English languages)
LANGUAGE_CODES = [
    'ar', 'de', 'es', 'fr', 'hi', 'id', 'it', 'ja',
    'ko', 'pt', 'ru', 'th', 'tr', 'vi', 'zh-hans', 'zh-hant',
]

# System files to exclude
EXCLUDE_FILES = ['INDEX.md', 'PROGRESS.md', 'README.md']


def parse_markdown_template(filepath):
    """
    Parse markdown template file and extract all components.
    Returns dict with: template_type, category, subject, html_content, text_content
    """
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
    subject_match = re.search(
        r'## Subject\s*\n(.+?)(?=\n\n|\n##)', content, re.DOTALL
    )
    if subject_match:
        result['subject'] = subject_match.group(1).strip()
    else:
        return {'error': 'Missing ## Subject section'}

    # Extract HTML content (between ## HTML Content and next section)
    html_match = re.search(
        r'## HTML Content\s*\n(.+?)(?=\n## (?:Text Content|Variables|Notes)|$)',
        content,
        re.DOTALL,
    )
    if html_match:
        result['html_content'] = html_match.group(1).strip()
    else:
        return {'error': 'Missing ## HTML Content section'}

    # Extract text content (optional - between ## Text Content and next section)
    text_match = re.search(
        r'## Text Content\s*\n(.+?)(?=\n## (?:Variables|Notes)|$)',
        content,
        re.DOTALL,
    )
    if text_match:
        result['text_content'] = text_match.group(1).strip()
    else:
        result['text_content'] = ''  # Text content is optional

    return result


def get_english_base_files(template_dir):
    """Get all English base template files (excluding translations and system files)"""
    all_md_files = glob.glob(os.path.join(template_dir, '*.md'))

    base_files = []
    for filepath in all_md_files:
        filename = os.path.basename(filepath)

        # Exclude system files
        if filename in EXCLUDE_FILES:
            continue

        # Exclude translation files (have language suffix before .md)
        has_lang_suffix = any(
            filename.endswith(f'.{lang}.md') for lang in LANGUAGE_CODES
        )
        if has_lang_suffix:
            continue

        base_files.append(filepath)

    return sorted(base_files)


class Command(SeedCommand):
    seed_name = 'email_templates'
    seed_version = 7
    help = 'Seed all email templates (English base + 16 language translations) from markdown files'

    def seed(self) -> int:
        from django.conf import settings
        from django.contrib.sites.models import Site
        from email_system.models import EmailTemplate, EmailTemplateTranslation

        site = Site.objects.get(pk=1)
        is_hq = getattr(settings, 'SPWIG_IS_HQ', False)

        # On non-HQ installations, clean up any previously-seeded HQ-only
        # system templates (from before gating was added).
        if not is_hq:
            from django.db.models import Q
            hq_filter = Q()
            for prefix in EmailTemplate.HQ_ONLY_PREFIXES:
                hq_filter |= Q(template_type__startswith=prefix)
            hq_qs = EmailTemplate.objects.filter(hq_filter, is_system=True)
            deleted_count = hq_qs.count()
            if deleted_count:
                # Use hard_delete() since EmailTemplate uses SoftDeleteModel
                hq_qs.hard_delete()
            if deleted_count:
                self.stdout.write(
                    f"    Cleaned up {deleted_count} HQ-only system "
                    f"template(s) from non-HQ installation"
                )

        # Resolve template directory relative to project root.
        # settings.BASE_DIR works in both dev and production Docker (/app/).
        template_dir = os.path.join(
            settings.BASE_DIR, 'email_templates_for_translation'
        )

        if not os.path.isdir(template_dir):
            self.stderr.write(
                self.style.ERROR(
                    f"Template directory not found: {template_dir}"
                )
            )
            return 0

        # Discover English base template files
        base_files = get_english_base_files(template_dir)
        if not base_files:
            self.stderr.write(
                self.style.ERROR("No English base template files found")
            )
            return 0

        self.stdout.write(
            f"    Found {len(base_files)} English base template files"
        )

        total_count = 0
        skipped_hq = 0
        errors = []

        for english_file in base_files:
            filename = os.path.basename(english_file)
            template_name = filename.replace('.md', '')

            # Parse English base template
            english_data = parse_markdown_template(english_file)

            if 'error' in english_data:
                errors.append(f"{filename}: {english_data['error']}")
                continue

            # Skip HQ-only templates on non-HQ installations
            if not is_hq and EmailTemplate.is_hq_only_type(
                english_data.get('template_type', '')
            ):
                skipped_hq += 1
                continue

            # Upsert English base EmailTemplate
            try:
                _obj, _created = EmailTemplate.objects.update_or_create(
                    site=site,
                    template_type=english_data['template_type'],
                    language_code='en',
                    is_system=True,
                    defaults={
                        'subject': english_data['subject'],
                        'html_content': english_data['html_content'],
                        'text_content': english_data.get('text_content', ''),
                        'is_active': True,
                        'version': 1,
                    },
                )
                total_count += 1
            except Exception as e:
                errors.append(
                    f"{filename}: Failed to upsert base template: {e}"
                )
                continue

            # Process translations for all 16 languages
            for lang_code in LANGUAGE_CODES:
                translation_file = english_file.replace(
                    '.md', f'.{lang_code}.md'
                )

                if not os.path.exists(translation_file):
                    continue

                translation_data = parse_markdown_template(translation_file)

                if 'error' in translation_data:
                    errors.append(
                        f"{template_name}.{lang_code}.md: "
                        f"{translation_data['error']}"
                    )
                    continue

                try:
                    EmailTemplateTranslation.objects.update_or_create(
                        template=_obj,
                        language_code=lang_code,
                        defaults={
                            'subject': translation_data['subject'],
                            'html_content': translation_data['html_content'],
                            'text_content': translation_data.get(
                                'text_content', ''
                            ),
                            'base_template_version': 1,
                            'is_verified': True,
                            'quality_score': 1.0,
                        },
                    )
                    total_count += 1
                except Exception as e:
                    errors.append(
                        f"{template_name}.{lang_code}.md: "
                        f"Failed to upsert translation: {e}"
                    )

        if skipped_hq:
            self.stdout.write(
                f"    Skipped {skipped_hq} HQ-only template(s) "
                f"on non-HQ installation"
            )

        if errors:
            self.stderr.write(
                self.style.WARNING(
                    f"    {len(errors)} issues encountered:"
                )
            )
            for error in errors[:10]:
                self.stderr.write(f"      {error}")
            if len(errors) > 10:
                self.stderr.write(f"      ... and {len(errors) - 10} more")

        return total_count
