"""
Management command to index help topics for semantic search.

Generates embeddings and creates search index entries for all or specific help topics.
"""

from django.core.management.base import BaseCommand, CommandError
from tqdm import tqdm

from core.models import HelpTopic
from core.services.semantic_search import IndexingService


class Command(BaseCommand):
    help = "Index help topics for semantic search"

    def add_arguments(self, parser):
        parser.add_argument(
            "--language",
            type=str,
            help="Index specific language (default: all languages from settings.LANGUAGES)",
        )
        parser.add_argument(
            "--topic",
            type=str,
            help="Index specific topic by slug (default: all published topics)",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force re-indexing even if already indexed",
        )

    def handle(self, *args, **options):
        language = options.get("language")
        topic_slug = options.get("topic")
        options.get("force")

        # Determine which languages to index
        if language:
            languages = [language]
            # Validate language
            supported_languages = IndexingService.get_supported_languages()
            if language not in supported_languages:
                raise CommandError(
                    f"Language '{language}' not supported. "
                    f"Supported languages: {', '.join(supported_languages)}"
                )
        else:
            languages = None  # Will use all languages from settings

        # Index specific topic or all topics
        if topic_slug:
            # Index single topic
            try:
                topic = HelpTopic.objects.get(slug=topic_slug, is_published=True)
            except HelpTopic.DoesNotExist:
                raise CommandError(f"Topic '{topic_slug}' not found or not published")

            self.stdout.write(f"Indexing topic: {topic.slug}")

            if languages is None:
                lang_list = IndexingService.get_supported_languages()
                self.stdout.write(f"Languages: {', '.join(lang_list)} ({len(lang_list)} total)")
            else:
                self.stdout.write(f"Language: {language}")

            stats = IndexingService.index_topic(topic.id, languages=languages)

            self.stdout.write(
                self.style.SUCCESS(
                    f"✓ Indexed {stats['topics_indexed']} topic, "
                    f"{stats['total_chunks']} chunks in "
                    f"{len(stats['languages'])} language(s)"
                )
            )

        else:
            # Index all topics
            topics = HelpTopic.objects.filter(is_published=True).order_by("slug")
            topic_count = topics.count()

            if topic_count == 0:
                self.stdout.write(self.style.WARNING("No published topics found to index"))
                return

            if languages is None:
                lang_list = IndexingService.get_supported_languages()
                self.stdout.write(
                    f"Indexing {topic_count} topics in {len(lang_list)} language(s)..."
                )
            else:
                self.stdout.write(f"Indexing {topic_count} topics in language: {language}...")

            total_chunks = 0
            total_topics_indexed = 0

            # Use tqdm for progress bar
            for topic in tqdm(topics, desc="Indexing topics", unit="topic"):
                stats = IndexingService.index_topic(topic.id, languages=languages)
                total_topics_indexed += stats["topics_indexed"]
                total_chunks += stats["total_chunks"]

            # Final summary
            self.stdout.write(self.style.SUCCESS("\nIndexing complete:"))
            self.stdout.write(f"- Topics indexed: {total_topics_indexed}")
            self.stdout.write(f"- Total chunks: {total_chunks}")

            if languages:
                self.stdout.write(f"- Languages: {', '.join(languages)}")
            else:
                lang_list = IndexingService.get_supported_languages()
                self.stdout.write(f"- Languages: {', '.join(lang_list)} ({len(lang_list)} total)")
