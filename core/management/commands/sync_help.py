"""
Management command to sync help content from markdown files to database.
This command reads help topics from the help_content directory and syncs them to the database.
Supports per-language translation files using the convention: {slug}.{lang}.md
"""

import json
import logging
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models.signals import post_save
from django.utils.text import slugify

from core.models import HelpCategory, HelpTopic

logger = logging.getLogger(__name__)

# Built-in translation languages (matching platform languages minus English)
_BUILTIN_HELP_LANGUAGES = [
    "ar",
    "de",
    "es",
    "fr",
    "hi",
    "id",
    "it",
    "ja",
    "ko",
    "pt",
    "ru",
    "th",
    "tr",
    "vi",
    "zh-hans",
    "zh-hant",
]


def _get_supported_languages():
    """Return help languages: built-in + any installed language packs."""
    from django.conf import settings

    # All non-English languages from settings.LANGUAGES (includes packs)
    all_codes = {code for code, _ in settings.LANGUAGES if code != "en"}
    # Merge with built-in list (preserves order, adds pack languages at end)
    result = list(_BUILTIN_HELP_LANGUAGES)
    for code in sorted(all_codes - set(result)):
        result.append(code)
    return result


SUPPORTED_LANGUAGES = _get_supported_languages()


def parse_frontmatter(content):
    """Parse YAML frontmatter from markdown content.

    Returns (frontmatter_dict, body_content) tuple.
    """
    import yaml

    frontmatter = {}
    body = content

    if content.startswith("---\n"):
        parts = content.split("---\n", 2)
        if len(parts) >= 3:
            frontmatter = yaml.safe_load(parts[1]) or {}
            body = parts[2].strip()

    return frontmatter, body


class Command(BaseCommand):
    help = "Sync help content from markdown files to database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--content-dir",
            type=str,
            default="help_content",
            help="Directory containing help content (default: help_content)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be synced without making changes",
        )
        parser.add_argument(
            "--delete-orphans",
            action="store_true",
            help="Delete topics not found in content directory",
        )
        parser.add_argument(
            "--no-index",
            action="store_true",
            help="Skip queuing search index tasks (sync content only)",
        )

    def handle(self, *args, **options):
        content_dir = Path(options["content_dir"])
        dry_run = options["dry_run"]
        delete_orphans = options["delete_orphans"]
        no_index = options["no_index"]

        if not content_dir.exists():
            raise CommandError(f"Content directory does not exist: {content_dir}")

        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN MODE - No changes will be made"))

        # Track synced topic slugs
        synced_slugs = set()

        # Stats
        stats = {
            "categories_created": 0,
            "categories_updated": 0,
            "categories_auto_created": 0,
            "topics_created": 0,
            "topics_updated": 0,
            "topics_deleted": 0,
            "translations_loaded": 0,
        }

        # Disconnect the reindex signal during bulk sync to prevent
        # flooding the task queue with one task per save() call.
        # We'll queue a single controlled batch at the end instead.
        from core.signals import reindex_help_topic_on_save

        post_save.disconnect(
            reindex_help_topic_on_save,
            sender=HelpTopic,
            dispatch_uid="core_reindex_help_topic_on_save",
        )
        logger.info("Disconnected reindex signal for bulk sync")

        synced_topic_ids = []

        try:
            with transaction.atomic():
                # Process categories
                categories_file = content_dir / "categories.json"
                if categories_file.exists():
                    self.stdout.write("Processing categories...")
                    with open(categories_file, encoding="utf-8") as f:
                        categories_data = json.load(f)

                    for cat_data in categories_data:
                        slug = cat_data.get("slug") or slugify(cat_data["name"])

                        if dry_run:
                            self.stdout.write(f"  Would sync category: {cat_data['name']} ({slug})")
                            continue

                        # Extract translations from categories.json if present
                        cat_translations = cat_data.get("translations", {})

                        category, created = HelpCategory.objects.update_or_create(
                            slug=slug,
                            defaults={
                                "name": cat_data["name"],
                                "icon": cat_data.get("icon", "fa-question-circle"),
                                "order": cat_data.get("order", 0),
                                "description": cat_data.get("description", ""),
                                "translations": cat_translations,
                            },
                        )

                        if created:
                            stats["categories_created"] += 1
                            self.stdout.write(
                                self.style.SUCCESS(f"  Created category: {category.name}")
                            )
                        else:
                            stats["categories_updated"] += 1
                            self.stdout.write(f"  Updated category: {category.name}")

                # Process topics
                topics_dir = content_dir / "topics"
                if topics_dir.exists():
                    self.stdout.write("\nProcessing topics...")

                    # Only process English source files (no lang suffix)
                    for topic_file in sorted(topics_dir.glob("**/*.md")):
                        # Skip translation files (e.g., add-product.es.md)
                        stem = topic_file.stem
                        if "." in stem:
                            # This is a translation file like add-product.es
                            continue

                        with open(topic_file, encoding="utf-8") as f:
                            content = f.read()

                        # Parse frontmatter
                        frontmatter, body = parse_frontmatter(content)

                        # Extract metadata
                        slug = frontmatter.get("slug") or slugify(stem)
                        synced_slugs.add(slug)

                        title_key = frontmatter.get("title_i18n_key", f"help.topic.{slug}.title")
                        category_slug = frontmatter.get("category")

                        if not category_slug:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"  Skipping {topic_file.name}: No category specified"
                                )
                            )
                            continue

                        try:
                            category = HelpCategory.objects.get(slug=category_slug)
                        except HelpCategory.DoesNotExist:
                            if dry_run:
                                self.stdout.write(
                                    self.style.WARNING(
                                        f"  Would auto-create missing category: {category_slug}"
                                    )
                                )
                                continue
                            # Auto-create the category so topics are never silently skipped.
                            # The category gets sensible defaults; update categories.json to
                            # give it proper icon, order, and translations.
                            category = HelpCategory.objects.create(
                                slug=category_slug,
                                name=category_slug.replace("-", " ").title(),
                                icon="fas fa-question-circle",
                                order=99,
                                description="",
                            )
                            stats["categories_auto_created"] += 1
                            self.stdout.write(
                                self.style.WARNING(
                                    f"  Auto-created missing category: {category_slug} "
                                    f"— add it to categories.json for proper icon/translations"
                                )
                            )

                        # Scan for translation files in the same directory
                        translations = {}
                        topic_dir = topic_file.parent
                        for lang in SUPPORTED_LANGUAGES:
                            trans_file = topic_dir / f"{stem}.{lang}.md"
                            if trans_file.exists():
                                with open(trans_file, encoding="utf-8") as f:
                                    trans_content = f.read()

                                trans_frontmatter, trans_body = parse_frontmatter(trans_content)

                                translations[lang] = {
                                    "title": trans_frontmatter.get("title", ""),
                                    "content": trans_body,
                                }
                                stats["translations_loaded"] += 1

                        if dry_run:
                            trans_langs = list(translations.keys())
                            trans_info = f" [{', '.join(trans_langs)}]" if trans_langs else ""
                            self.stdout.write(f"  Would sync topic: {slug}{trans_info}")
                            continue

                        # Create or update topic
                        topic, created = HelpTopic.objects.update_or_create(
                            slug=slug,
                            defaults={
                                "category": category,
                                "title_i18n_key": title_key,
                                "content_markdown": body,
                                "component": frontmatter.get("component", "core"),
                                "min_version": frontmatter.get("min_version", ""),
                                "max_version": frontmatter.get("max_version", ""),
                                "keywords": frontmatter.get("keywords", []),
                                "url_patterns": frontmatter.get("url_patterns", []),
                                "is_published": frontmatter.get("published", True),
                                "translations": translations,
                            },
                        )

                        # Track published topics for batch indexing
                        if topic.is_published:
                            synced_topic_ids.append(topic.id)

                        # Handle related topics
                        related_slugs = frontmatter.get("related", [])
                        if related_slugs:
                            related_topics = HelpTopic.objects.filter(slug__in=related_slugs)
                            topic.related_topics.set(related_topics)

                        if created:
                            stats["topics_created"] += 1
                            self.stdout.write(self.style.SUCCESS(f"  Created topic: {slug}"))
                        else:
                            stats["topics_updated"] += 1
                            self.stdout.write(f"  Updated topic: {slug}")

                        # Log translations
                        if translations:
                            langs = ", ".join(sorted(translations.keys()))
                            self.stdout.write(f"    Translations: {langs}")

                # Delete orphaned topics
                if delete_orphans and not dry_run:
                    orphaned = HelpTopic.objects.exclude(slug__in=synced_slugs)
                    count = orphaned.count()
                    if count > 0:
                        self.stdout.write(
                            self.style.WARNING(f"\nDeleting {count} orphaned topics...")
                        )
                        for topic in orphaned:
                            self.stdout.write(f"  Deleting: {topic.slug}")
                        orphaned.delete()
                        stats["topics_deleted"] = count

                if dry_run:
                    # Rollback transaction in dry run
                    raise CommandError("DRY RUN - Rolling back")

        except CommandError:
            if not dry_run:
                raise
        finally:
            # Always reconnect the signal so individual topic saves
            # in the admin still trigger reindexing
            post_save.connect(
                reindex_help_topic_on_save,
                sender=HelpTopic,
                dispatch_uid="core_reindex_help_topic_on_save",
            )
            logger.info("Reconnected reindex signal after bulk sync")

        # Print summary
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(self.style.SUCCESS("Sync completed!"))
        self.stdout.write(f"Categories created: {stats['categories_created']}")
        self.stdout.write(f"Categories updated: {stats['categories_updated']}")
        if stats["categories_auto_created"]:
            self.stdout.write(
                self.style.WARNING(
                    f"Categories auto-created (missing from categories.json): "
                    f"{stats['categories_auto_created']}"
                )
            )
        self.stdout.write(f"Topics created: {stats['topics_created']}")
        self.stdout.write(f"Topics updated: {stats['topics_updated']}")
        self.stdout.write(f"Translations loaded: {stats['translations_loaded']}")
        if delete_orphans:
            self.stdout.write(f"Topics deleted: {stats['topics_deleted']}")

        # Queue a single batch of indexing tasks (one per topic, no duplicates)
        if not dry_run and not no_index and synced_topic_ids:
            self.stdout.write(f"\nQueuing search index for {len(synced_topic_ids)} topics...")
            try:
                from core.tasks import index_help_topic_async

                for topic_id in synced_topic_ids:
                    index_help_topic_async.delay(topic_id)
                self.stdout.write(
                    self.style.SUCCESS(f"Queued {len(synced_topic_ids)} indexing tasks")
                )
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(
                        f"Could not queue indexing tasks: {e}\n"
                        f"Run 'manage.py index_help_topics' manually to index."
                    )
                )
        elif no_index:
            self.stdout.write("\nSkipping search index (--no-index)")
