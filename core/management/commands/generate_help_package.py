"""
Management command to generate a help content package for the update server.
This creates a .zip package with help topics, translations, and manifest.
"""

import json
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from core.models import HelpCategory, HelpTopic


class Command(BaseCommand):
    help = "Generate help content package for update server distribution"

    def add_arguments(self, parser):
        parser.add_argument(
            "--version",
            type=str,
            required=True,
            help="Version number for this help package (e.g., 1.0.0)",
        )
        parser.add_argument(
            "--output",
            type=str,
            default=".",
            help="Output directory for package (default: current directory)",
        )
        parser.add_argument(
            "--component",
            type=str,
            default="core",
            help="Component to generate help for (default: core)",
        )
        parser.add_argument(
            "--all-components",
            action="store_true",
            help="Generate help for all components",
        )

    def handle(self, *args, **options):
        version = options["version"]
        output_dir = Path(options["output"])
        component = options["component"]
        all_components = options["all_components"]

        if not output_dir.exists():
            output_dir.mkdir(parents=True)

        # Get topics to package
        if all_components:
            topics = HelpTopic.objects.filter(is_published=True)
            package_name = f"help_content-{version}"
        else:
            topics = HelpTopic.objects.filter(component=component, is_published=True)
            package_name = f"help_{component}-{version}"

        if not topics.exists():
            raise CommandError(f"No published topics found for component: {component}")

        self.stdout.write(f"Packaging {topics.count()} help topics...")

        # Create temporary directory for package contents
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            package_path = temp_path / package_name

            # Create package structure
            (package_path / "topics").mkdir(parents=True)
            (package_path / "locale").mkdir(parents=True)

            # Export categories
            categories = HelpCategory.objects.all()
            categories_data = []
            for category in categories:
                categories_data.append(
                    {
                        "slug": category.slug,
                        "name": category.name,
                        "icon": category.icon,
                        "order": category.order,
                        "description": category.description,
                    }
                )

            with open(package_path / "categories.json", "w", encoding="utf-8") as f:
                json.dump(categories_data, f, indent=2, ensure_ascii=False)

            # Export topics
            for topic in topics:
                # Create frontmatter
                frontmatter = {
                    "slug": topic.slug,
                    "title_i18n_key": topic.title_i18n_key,
                    "category": topic.category.slug,
                    "component": topic.component,
                    "published": topic.is_published,
                }

                if topic.min_version:
                    frontmatter["min_version"] = topic.min_version
                if topic.max_version:
                    frontmatter["max_version"] = topic.max_version
                if topic.keywords:
                    frontmatter["keywords"] = topic.keywords
                if topic.url_patterns:
                    frontmatter["url_patterns"] = topic.url_patterns

                # Get related topics
                related = topic.related_topics.all()
                if related:
                    frontmatter["related"] = [t.slug for t in related]

                # Write markdown file with frontmatter
                topic_file = package_path / "topics" / f"{topic.slug}.md"
                with open(topic_file, "w", encoding="utf-8") as f:
                    f.write("---\n")
                    import yaml

                    yaml.dump(frontmatter, f, default_flow_style=False, allow_unicode=True)
                    f.write("---\n\n")
                    f.write(topic.content_markdown)

                self.stdout.write(f"  Exported: {topic.slug}")

            # Generate translation files for each language
            # Note: This exports the .po files from Django's locale directories
            locale_base = Path(settings.BASE_DIR) / "locale"
            if locale_base.exists():
                for lang_code in ["es", "fr", "de", "ja", "pt", "zh_Hans", "zh_Hant", "ru", "ar"]:
                    lang_dir = locale_base / lang_code / "LC_MESSAGES"
                    po_file = lang_dir / "django.po"
                    mo_file = lang_dir / "django.mo"

                    if po_file.exists():
                        # Copy translation files
                        dest_dir = package_path / "locale" / lang_code / "LC_MESSAGES"
                        dest_dir.mkdir(parents=True, exist_ok=True)

                        import shutil

                        shutil.copy2(po_file, dest_dir / "django.po")
                        if mo_file.exists():
                            shutil.copy2(mo_file, dest_dir / "django.mo")

                        self.stdout.write(f"  Included translations: {lang_code}")

            # Create manifest
            manifest = {
                "name": f"Help Content - {component.title()}"
                if not all_components
                else "Help Content - All",
                "slug": package_name,
                "type": "help_content",
                "version": version,
                "description": f"Help documentation for {component} component",
                "author": "Spwig",
                "component": component if not all_components else "all",
                "min_platform_version": "1.0.0",
                "created_at": datetime.utcnow().isoformat() + "Z",
                "topics_count": topics.count(),
                "categories_count": categories.count(),
                "languages": ["en", "es", "fr", "de", "ja", "pt", "zh-hans", "zh-hant", "ru", "ar"],
                "changelog": [
                    {
                        "version": version,
                        "date": datetime.utcnow().strftime("%Y-%m-%d"),
                        "changes": ["Initial help content package"],
                    }
                ],
            }

            with open(package_path / "manifest.json", "w", encoding="utf-8") as f:
                json.dump(manifest, f, indent=2, ensure_ascii=False)

            # Create README
            readme = f"""# Help Content Package - {component.title()}

Version: {version}
Topics: {topics.count()}
Categories: {categories.count()}

## Installation

This package can be installed through the Spwig admin interface:
1. Go to Components > Help Content
2. Click "Install Package"
3. Upload this package or fetch from update server

## Contents

- categories.json: Help topic categories
- topics/: Individual help topic markdown files
- locale/: Translation files for 10 languages
- manifest.json: Package metadata

## Languages Supported

- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Japanese (ja)
- Portuguese (pt)
- Chinese Simplified (zh-hans)
- Chinese Traditional (zh-hant)
- Russian (ru)
- Arabic (ar)

## Generated

{datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")} UTC
"""

            with open(package_path / "README.md", "w", encoding="utf-8") as f:
                f.write(readme)

            # Create ZIP package
            zip_path = output_dir / f"{package_name}.zip"
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for file_path in package_path.rglob("*"):
                    if file_path.is_file():
                        arcname = file_path.relative_to(temp_path)
                        zipf.write(file_path, arcname)

            self.stdout.write("\n" + "=" * 50)
            self.stdout.write(self.style.SUCCESS(f"Package created: {zip_path}"))
            self.stdout.write(f"Size: {zip_path.stat().st_size / 1024:.1f} KB")
            self.stdout.write(f"Topics: {topics.count()}")
            self.stdout.write(f"Categories: {categories.count()}")
