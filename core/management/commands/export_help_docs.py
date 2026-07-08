"""
Management command to export help documentation for external publishing.

Exports help content from database to static files suitable for docs.spwig.com,
with URL sanitization, image path rewriting, and translation bundling.

Usage:
    python manage.py export_help_docs \\
        --output /path/to/output \\
        --version 1.2.1 \\
        --sanitize-urls \\
        --copy-images
"""

import json
import os
import re
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

try:
    import markdown
except ImportError:
    markdown = None

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from core.models import HelpCategory, HelpTopic


# URL sanitization rules: (pattern, replacement)
URL_SANITIZE_RULES = [
    # Catalog/Products
    (r'/admin/catalog/product/add/', 'Navigate to **Products > Add Product**'),
    (r'/admin/catalog/product/(\d+)/change/', 'Navigate to **Products > Edit Product**'),
    (r'/admin/catalog/product/', 'Navigate to **Products > All Products**'),
    (r'/admin/catalog/category/add/', 'Navigate to **Products > Categories > Add Category**'),
    (r'/admin/catalog/category/(\d+)/change/', 'Navigate to **Products > Categories > Edit Category**'),
    (r'/admin/catalog/category/', 'Navigate to **Products > Categories**'),
    (r'/admin/catalog/brand/', 'Navigate to **Products > Brands**'),
    (r'/admin/catalog/attribute/', 'Navigate to **Products > Attributes**'),

    # Orders
    (r'/admin/orders/order/(\d+)/change/', 'Navigate to **Orders > View Order**'),
    (r'/admin/orders/order/', 'Navigate to **Orders > All Orders**'),
    (r'/admin/orders/shipment/', 'Navigate to **Orders > Shipments**'),

    # Customers
    (r'/admin/customers/customer/(\d+)/change/', 'Navigate to **Customers > View Customer**'),
    (r'/admin/customers/customer/', 'Navigate to **Customers > All Customers**'),
    (r'/admin/customers/customergroup/', 'Navigate to **Customers > Customer Groups**'),

    # Marketing
    (r'/admin/affiliate/affiliateprogram/', 'Navigate to **Marketing > Affiliate Programs**'),
    (r'/admin/affiliate/commission/', 'Navigate to **Marketing > Commissions**'),
    (r'/admin/loyalty/loyaltycampaign/', 'Navigate to **Marketing > Loyalty Campaigns**'),
    (r'/admin/vouchers/voucher/', 'Navigate to **Marketing > Vouchers**'),

    # Shipping
    (r'/admin/shipping/shippingprovider/', 'Navigate to **Settings > Shipping Providers**'),
    (r'/admin/shipping/shippingzone/', 'Navigate to **Settings > Shipping Zones**'),

    # Payment
    (r'/admin/payment_providers/paymentprovideraccount/', 'Navigate to **Settings > Payment Providers**'),

    # Design
    (r'/admin/design/theme/', 'Navigate to **Design > Themes**'),
    (r'/admin/design/headerfooter/', 'Navigate to **Design > Headers & Footers**'),

    # Media
    (r'/admin/media_library/mediaasset/', 'Navigate to **Media > Media Library**'),

    # Email
    (r'/admin/email_system/emailaccount/', 'Navigate to **Settings > Email Accounts**'),
    (r'/admin/email_system/emailtemplate/', 'Navigate to **Settings > Email Templates**'),

    # Blog
    (r'/admin/blog/blogpost/', 'Navigate to **Content > Blog Posts**'),
    (r'/admin/blog/blogcategory/', 'Navigate to **Content > Blog Categories**'),

    # Pages
    (r'/admin/page_builder/page/', 'Navigate to **Content > Pages**'),

    # Translations
    (r'/admin/translations/language/', 'Navigate to **Settings > Languages**'),
    (r'/admin/translations/translationjob/', 'Navigate to **Settings > Translation Jobs**'),

    # Generic fallback (lowercase and titlecase component/model names)
    (r'/admin/(\w+)/(\w+)/', lambda m: f'Navigate to **{m.group(1).title()} > {m.group(2).replace("_", " ").title()}**'),
]


class Command(BaseCommand):
    help = 'Export help documentation for external publishing to docs.spwig.com'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            required=True,
            help='Output directory for exported files'
        )
        parser.add_argument(
            '--doc-version',
            type=str,
            default=None,
            help='Documentation version string (e.g., "2.1.0"). If not provided, uses shop version from core.__version__'
        )
        parser.add_argument(
            '--sanitize-urls',
            action='store_true',
            help='Replace admin URLs with navigation hints'
        )
        parser.add_argument(
            '--copy-images',
            action='store_true',
            help='Copy help images to output directory'
        )
        parser.add_argument(
            '--languages',
            type=str,
            default='es,fr,de,pt,ja,zh-hans,zh-hant,ru,ar,hi,id,it,ko,tr,vi,th',
            help='Comma-separated list of language codes to export (default: all 16)'
        )

    def handle(self, *args, **options):
        from core import __version__

        output_dir = Path(options['output'])
        version = options['doc_version'] or __version__
        sanitize_urls = options['sanitize_urls']
        copy_images = options['copy_images']
        languages = [lang.strip() for lang in options['languages'].split(',') if lang.strip()]

        # Store version as instance attribute for use in helper methods
        self.version = version

        self.stdout.write(self.style.SUCCESS(f'Exporting help documentation to {output_dir}'))
        self.stdout.write(f'Version: {version}')
        self.stdout.write(f'Languages: {", ".join(languages)}')
        self.stdout.write(f'URL sanitization: {"enabled" if sanitize_urls else "disabled"}')
        self.stdout.write(f'Image copying: {"enabled" if copy_images else "disabled"}')

        # Create output directory structure
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / 'topics' / 'en').mkdir(parents=True, exist_ok=True)
        for lang in languages:
            (output_dir / 'topics' / lang).mkdir(parents=True, exist_ok=True)

        # Export categories
        self.stdout.write('\nExporting categories...')
        categories_data = self._export_categories(languages)
        with open(output_dir / 'categories.json', 'w', encoding='utf-8') as f:
            json.dump(categories_data, f, ensure_ascii=False, indent=2)
        self.stdout.write(self.style.SUCCESS(f'  ✓ Exported {len(categories_data)} categories'))

        # Export topics
        self.stdout.write('\nExporting topics...')
        topics = HelpTopic.objects.filter(is_published=True).select_related('category').prefetch_related('related_topics')

        topics_exported = 0
        translations_exported = 0
        translation_bundle = {}

        for topic in topics:
            # Export English version
            content = topic.content_markdown

            if sanitize_urls:
                content = self._sanitize_urls(content)

            content = self._rewrite_image_paths(content)

            # Write English markdown file
            filename = f"{topic.category.slug}__{topic.slug}.md"
            self._write_topic_file(output_dir / 'topics' / 'en', filename, topic, content, 'en')
            topics_exported += 1

            # Prepare translation bundle entry
            available_langs = ['en']
            translation_bundle[topic.slug] = {
                'available_langs': available_langs,
                'translations': {}
            }

            # Export translations
            for lang in languages:
                if lang in topic.translations and topic.translations[lang]:
                    trans = topic.translations[lang]
                    trans_title = trans.get('title', topic.title_i18n_key)
                    trans_content = trans.get('content', content)

                    if sanitize_urls:
                        trans_content = self._sanitize_urls(trans_content)

                    trans_content = self._rewrite_image_paths(trans_content)

                    # Write translation markdown file
                    self._write_topic_file(output_dir / 'topics' / lang, filename, topic, trans_content, lang, trans_title)
                    translations_exported += 1

                    # Add to translation bundle
                    available_langs.append(lang)
                    translation_bundle[topic.slug]['translations'][lang] = {
                        'title': trans_title,
                        'content': self._markdown_to_html_placeholder(trans_content)
                    }

            translation_bundle[topic.slug]['available_langs'] = available_langs

        self.stdout.write(self.style.SUCCESS(f'  ✓ Exported {topics_exported} English topics'))
        self.stdout.write(self.style.SUCCESS(f'  ✓ Exported {translations_exported} translations'))

        # Write translation bundle
        self.stdout.write('\nGenerating translation bundle...')

        # Convert categories list to dict keyed by slug for easier client-side lookup
        categories_dict = {cat['slug']: cat for cat in categories_data}

        with open(output_dir / 'translations.json', 'w', encoding='utf-8') as f:
            json.dump({
                'languages': self._get_language_metadata(),
                'categories': categories_dict,
                'topics': translation_bundle
            }, f, ensure_ascii=False, indent=2)
        self.stdout.write(self.style.SUCCESS('  ✓ Translation bundle created'))

        # Copy images
        if copy_images:
            self.stdout.write('\nCopying help images...')
            images_copied = self._copy_help_images(output_dir)
            self.stdout.write(self.style.SUCCESS(f'  ✓ Copied {images_copied} images'))

        # Generate metadata
        self.stdout.write('\nGenerating metadata...')
        metadata = {
            'version': version,
            'exported_at': self._get_timestamp(),
            'topics_count': topics_exported,
            'translations_count': translations_exported,
            'categories_count': len(categories_data),
            'languages': ['en'] + languages,
            'url_sanitization': sanitize_urls,
            'images_copied': copy_images
        }
        with open(output_dir / 'metadata.json', 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        self.stdout.write(self.style.SUCCESS('  ✓ Metadata generated'))

        self.stdout.write(self.style.SUCCESS(f'\n✅ Export complete! Output: {output_dir}'))
        self.stdout.write(f'   Total files: {topics_exported + translations_exported + len(categories_data) + 2}')

    def _export_categories(self, languages: List[str]) -> List[Dict]:
        """Export help categories with translations"""
        categories = HelpCategory.objects.all().order_by('order', 'name')
        categories_data = []

        for category in categories:
            cat_data = {
                'name': category.name,
                'slug': category.slug,
                'icon': category.icon,
                'order': category.order,
                'description': category.description,
                'translations': {}
            }

            # Add translations
            for lang in languages:
                if lang in category.translations and category.translations[lang]:
                    cat_data['translations'][lang] = category.translations[lang]

            categories_data.append(cat_data)

        return categories_data

    def _sanitize_urls(self, content: str) -> str:
        """Replace admin URLs with navigation hints (excluding image src attributes)"""
        # First, protect image tags by temporarily replacing them with placeholders
        img_tags = []

        def save_img_tag(match):
            img_tags.append(match.group(0))
            return f'__IMG_PLACEHOLDER_{len(img_tags)-1}__'

        # Save all image tags (markdown and HTML)
        content = re.sub(r'!\[.*?\]\(.*?\)', save_img_tag, content)
        content = re.sub(r'<img[^>]*>', save_img_tag, content)

        # Now apply URL sanitization
        for pattern, replacement in URL_SANITIZE_RULES:
            if callable(replacement):
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
            else:
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

        # Restore image tags
        for i, img_tag in enumerate(img_tags):
            content = content.replace(f'__IMG_PLACEHOLDER_{i}__', img_tag)

        return content

    def _rewrite_image_paths(self, content: str) -> str:
        """Rewrite image paths from /static/core/admin/img/help/ to /{version}/help-images/"""
        # Match markdown image syntax: ![alt text](/static/core/admin/img/help/path/to/image.webp)
        pattern = r'!\[(.*?)\]\(/static/core/admin/img/help/(.*?)\)'
        replacement = rf'![\1](/{self.version}/help-images/\2)'
        content = re.sub(pattern, replacement, content)

        # Also handle HTML img tags
        pattern = r'<img\s+([^>]*?)src="/static/core/admin/img/help/(.*?)"'
        replacement = rf'<img \1src="/{self.version}/help-images/\2"'
        content = re.sub(pattern, replacement, content)

        # Ensure /help-images/ paths have version prefix (for content that was already partially rewritten)
        # This catches: /help-images/... and adds version to make: /1.2.1/help-images/...
        # But avoids double-adding version if it's already there
        pattern = r'!\[(.*?)\]\(/help-images/(.*?)\)'
        replacement = rf'![\1](/{self.version}/help-images/\2)'
        content = re.sub(pattern, replacement, content)

        pattern = r'<img\s+([^>]*?)src="/help-images/(.*?)"'
        replacement = rf'<img \1src="/{self.version}/help-images/\2"'
        content = re.sub(pattern, replacement, content)

        return content

    def _write_topic_file(self, output_dir: Path, filename: str, topic: HelpTopic, content: str, lang: str, title: str = None):
        """Write topic markdown file with YAML frontmatter"""
        if title is None:
            title = topic.title_i18n_key

        # Build related topics list
        related_slugs = [rt.slug for rt in topic.related_topics.all()]

        # YAML frontmatter
        frontmatter = f"""---
slug: {topic.slug}
title: {title}
category: {topic.category.slug}
component: {topic.component}
keywords: {json.dumps(topic.keywords)}
url_patterns: {json.dumps(topic.url_patterns)}
related: {json.dumps(related_slugs)}
published: true
"""
        if topic.min_version:
            frontmatter += f"min_version: \"{topic.min_version}\"\n"
        if topic.max_version:
            frontmatter += f"max_version: \"{topic.max_version}\"\n"

        frontmatter += "---\n\n"

        # Write file
        filepath = output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(frontmatter)
            f.write(content)

    def _copy_help_images(self, output_dir: Path) -> int:
        """Copy help images from static directory"""
        help_images_source = Path(settings.BASE_DIR) / 'core' / 'static' / 'core' / 'admin' / 'img' / 'help'
        help_images_dest = output_dir / 'images'

        if not help_images_source.exists():
            self.stdout.write(self.style.WARNING(f'  ⚠ Help images source not found: {help_images_source}'))
            return 0

        # Copy entire directory
        if help_images_dest.exists():
            shutil.rmtree(help_images_dest)

        shutil.copytree(help_images_source, help_images_dest)

        # Count images
        image_count = sum(1 for _ in help_images_dest.rglob('*.webp'))
        image_count += sum(1 for _ in help_images_dest.rglob('*.png'))
        image_count += sum(1 for _ in help_images_dest.rglob('*.jpg'))
        image_count += sum(1 for _ in help_images_dest.rglob('*.jpeg'))

        return image_count

    def _markdown_to_html_placeholder(self, markdown_content: str) -> str:
        """
        Convert markdown to HTML for translation bundle.
        Uses same extensions as build-help-pages.py for consistency.
        """
        if not markdown:
            self.stdout.write(self.style.WARNING('  ⚠ markdown library not available, translations will lack formatting'))
            return markdown_content

        md = markdown.Markdown(extensions=[
            'fenced_code',
            'codehilite',
            'tables',
            'toc',
            'nl2br',
            'sane_lists'
        ])

        return md.convert(markdown_content)

    def _get_language_metadata(self) -> List[Dict]:
        """Get language metadata for translation bundle"""
        return [
            {"code": "en", "name": "English", "native": "English"},
            {"code": "es", "name": "Spanish", "native": "Español"},
            {"code": "fr", "name": "French", "native": "Français"},
            {"code": "de", "name": "German", "native": "Deutsch"},
            {"code": "pt", "name": "Portuguese", "native": "Português"},
            {"code": "ja", "name": "Japanese", "native": "日本語"},
            {"code": "zh-hans", "name": "Chinese (Simplified)", "native": "简体中文"},
            {"code": "zh-hant", "name": "Chinese (Traditional)", "native": "繁體中文"},
            {"code": "ru", "name": "Russian", "native": "Русский"},
            {"code": "ar", "name": "Arabic", "native": "العربية", "rtl": True},
            {"code": "hi", "name": "Hindi", "native": "हिन्दी"},
            {"code": "id", "name": "Indonesian", "native": "Bahasa Indonesia"},
            {"code": "it", "name": "Italian", "native": "Italiano"},
            {"code": "ko", "name": "Korean", "native": "한국어"},
            {"code": "tr", "name": "Turkish", "native": "Türkçe"},
            {"code": "vi", "name": "Vietnamese", "native": "Tiếng Việt"},
            {"code": "th", "name": "Thai", "native": "ไทย"},
        ]

    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        from datetime import datetime
        return datetime.now().isoformat()
