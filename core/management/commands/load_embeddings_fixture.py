"""
Management command to load pre-computed help topic embeddings from a fixture file.

Supports both JSONL (v2, streaming) and legacy JSON (v1) fixture formats.
JSONL format streams line-by-line to prevent OOM on low-memory containers.

Usage:
    python manage.py load_embeddings_fixture                  # Auto-detect format, sync
    python manage.py load_embeddings_fixture --force          # Force reload
    python manage.py load_embeddings_fixture --async          # Dispatch to Celery worker
    python manage.py load_embeddings_fixture --batch-size 100 # Smaller batches
"""

import gzip
import json
import logging
import time
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from tqdm import tqdm

from core.models import HelpSearchIndex, HelpTopic

logger = logging.getLogger(__name__)

EXPECTED_DIMENSIONS = 384
DEFAULT_BATCH_SIZE = 200
DEFAULT_THROTTLE = 0.1


class Command(BaseCommand):
    help = "Load pre-computed help topic embeddings from fixture file"

    def add_arguments(self, parser):
        parser.add_argument(
            "--fixture",
            type=str,
            default=None,
            help="Path to fixture file (auto-detects .jsonl.gz then .json.gz)",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force reload even if embeddings already exist and are current",
        )
        parser.add_argument(
            "--async",
            dest="run_async",
            action="store_true",
            help="Dispatch to Celery worker instead of loading synchronously",
        )
        parser.add_argument(
            "--batch-size",
            type=int,
            default=DEFAULT_BATCH_SIZE,
            help=f"Entries per bulk_create batch (default: {DEFAULT_BATCH_SIZE})",
        )
        parser.add_argument(
            "--throttle",
            type=float,
            default=DEFAULT_THROTTLE,
            help=f"Seconds to sleep between batches (default: {DEFAULT_THROTTLE})",
        )

    def handle(self, *args, **options):
        fixture_path = self._resolve_fixture_path(options["fixture"])
        if fixture_path is None:
            self.stdout.write(
                self.style.WARNING(
                    "Embeddings fixture not found.\n"
                    "Help semantic search will be unavailable until embeddings are generated.\n"
                    "Run 'python manage.py index_help_topics' to generate embeddings manually."
                )
            )
            return

        force = options["force"]
        batch_size = options["batch_size"]
        throttle = options["throttle"]
        is_jsonl = str(fixture_path).endswith(".jsonl.gz")

        # Try async dispatch if requested (JSONL only — legacy JSON can't be streamed)
        if options["run_async"] and is_jsonl:
            dispatched = self._dispatch_celery_task(fixture_path, force, batch_size, throttle)
            if dispatched:
                self.stdout.write(
                    self.style.SUCCESS("Embeddings loading dispatched to background worker")
                )
                return
            self.stdout.write(
                self.style.WARNING("Celery not available, falling back to synchronous loading")
            )

        # Synchronous loading
        if is_jsonl:
            self._load_jsonl_sync(fixture_path, force, batch_size, throttle)
        else:
            self._load_json_sync(fixture_path, force)

    def _resolve_fixture_path(self, explicit_path):
        """Resolve fixture path, preferring JSONL over legacy JSON."""
        if explicit_path:
            path = Path(explicit_path)
            if not path.is_absolute():
                path = Path(settings.BASE_DIR) / path
            return path if path.exists() else None

        base = Path(settings.BASE_DIR)
        jsonl_path = base / "core/fixtures/help_embeddings.jsonl.gz"
        json_path = base / "core/fixtures/help_embeddings.json.gz"

        if jsonl_path.exists():
            return jsonl_path
        if json_path.exists():
            return json_path
        return None

    def _dispatch_celery_task(self, fixture_path, force, batch_size, throttle):
        """Try to dispatch loading to a Celery worker. Returns True on success."""
        try:
            from django.core.cache import cache

            # Skip if already loading
            status = cache.get("help_embeddings_loading_status")
            if status and status.get("status") == "loading":
                self.stdout.write("Embeddings already loading in background, skipping")
                return True

            # Check if any workers are available
            from celery import current_app

            inspect = current_app.control.inspect(timeout=2.0)
            ping = inspect.ping()
            if not ping:
                return False

            from core.tasks import load_help_embeddings_async

            load_help_embeddings_async.delay(
                str(fixture_path),
                force=force,
                batch_size=batch_size,
                throttle_seconds=throttle,
            )
            return True
        except Exception as e:
            logger.debug(f"Celery dispatch failed: {e}")
            return False

    def _load_jsonl_sync(self, fixture_path, force, batch_size, throttle):
        """Stream-load JSONL fixture line-by-line (low memory)."""
        self.stdout.write(f"Reading JSONL fixture: {fixture_path}")

        try:
            with gzip.open(fixture_path, "rt", encoding="utf-8") as f:
                header = json.loads(f.readline())
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to read fixture header: {e}"))
            return

        # Validate
        model_dimensions = header.get("model_dimensions", 0)
        generated_at = header.get("generated_at", "")
        stats = header.get("stats", {})
        total_chunks = stats.get("total_chunks", 0)

        if model_dimensions != EXPECTED_DIMENSIONS:
            self.stdout.write(
                self.style.ERROR(
                    f"Dimension mismatch: expected {EXPECTED_DIMENSIONS}, got {model_dimensions}"
                )
            )
            return

        if total_chunks == 0:
            self.stdout.write(self.style.WARNING("Fixture contains no chunks"))
            return

        self.stdout.write(
            f"Fixture: {stats.get('topics', '?')} topics, "
            f"{stats.get('languages', '?')} languages, "
            f"{total_chunks} chunks"
        )

        # Freshness check
        if not force:
            existing_count = HelpSearchIndex.objects.count()
            if existing_count > 0:
                latest = (
                    HelpSearchIndex.objects.order_by("-indexed_at")
                    .values_list("indexed_at", flat=True)
                    .first()
                )
                if latest and generated_at:
                    from django.utils.dateparse import parse_datetime

                    fixture_dt = parse_datetime(generated_at)
                    if fixture_dt and latest >= fixture_dt:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Embeddings already loaded and up to date "
                                f"({existing_count} chunks, indexed {latest.strftime('%Y-%m-%d %H:%M')}). "
                                f"Use --force to reload."
                            )
                        )
                        return

        # Build topic lookup
        topic_map = dict(HelpTopic.objects.filter(is_published=True).values_list("slug", "id"))
        if not topic_map:
            self.stdout.write(
                self.style.WARNING(
                    "No published help topics found. Run 'python manage.py sync_help --no-index' first."
                )
            )
            return

        self.stdout.write(f"Found {len(topic_map)} published topics in database")

        # Clear existing
        deleted_count, _ = HelpSearchIndex.objects.all().delete()
        if deleted_count:
            self.stdout.write(f"Cleared {deleted_count} existing index entries")

        # Stream and insert
        entries = []
        loaded = 0
        skipped = 0

        with gzip.open(fixture_path, "rt", encoding="utf-8") as f:
            f.readline()  # skip header
            for line in tqdm(f, desc="Loading embeddings", total=total_chunks, unit="chunk"):
                line = line.strip()
                if not line:
                    continue

                chunk_data = json.loads(line)
                topic_id = topic_map.get(chunk_data.get("topic_slug"))

                if topic_id is None:
                    skipped += 1
                    continue

                entries.append(
                    HelpSearchIndex(
                        topic_id=topic_id,
                        language=chunk_data["language"],
                        chunk_text=chunk_data["chunk_text"],
                        chunk_position=chunk_data["chunk_position"],
                        embedding=chunk_data["embedding"],
                        is_title_chunk=chunk_data.get("is_title_chunk", False),
                        contains_keywords=chunk_data.get("contains_keywords", False),
                    )
                )

                if len(entries) >= batch_size:
                    HelpSearchIndex.objects.bulk_create(entries)
                    loaded += len(entries)
                    entries = []
                    if throttle > 0:
                        time.sleep(throttle)

        if entries:
            HelpSearchIndex.objects.bulk_create(entries)
            loaded += len(entries)

        self.stdout.write(self.style.SUCCESS("\nEmbeddings loaded successfully:"))
        self.stdout.write(f"  Loaded: {loaded} chunks")
        if skipped:
            self.stdout.write(
                self.style.WARNING(f"  Skipped: {skipped} chunks (topic not found in database)")
            )

    def _load_json_sync(self, fixture_path, force):
        """Legacy loader for v1 JSON format (loads entire file into memory)."""
        self.stdout.write(f"Reading legacy JSON fixture: {fixture_path}")

        try:
            with gzip.open(fixture_path, "rt", encoding="utf-8") as f:
                fixture = json.load(f)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to read fixture: {e}"))
            return

        model_dimensions = fixture.get("model_dimensions", 0)
        generated_at = fixture.get("generated_at", "")
        stats = fixture.get("stats", {})
        chunks = fixture.get("chunks", [])

        if model_dimensions != EXPECTED_DIMENSIONS:
            self.stdout.write(
                self.style.ERROR(
                    f"Dimension mismatch: expected {EXPECTED_DIMENSIONS}, got {model_dimensions}"
                )
            )
            return

        if not chunks:
            self.stdout.write(self.style.WARNING("Fixture contains no chunks"))
            return

        self.stdout.write(
            f"Fixture: {stats.get('topics', '?')} topics, "
            f"{stats.get('languages', '?')} languages, "
            f"{stats.get('total_chunks', '?')} chunks"
        )

        if not force:
            existing_count = HelpSearchIndex.objects.count()
            if existing_count > 0:
                latest = (
                    HelpSearchIndex.objects.order_by("-indexed_at")
                    .values_list("indexed_at", flat=True)
                    .first()
                )
                if latest and generated_at:
                    from django.utils.dateparse import parse_datetime

                    fixture_dt = parse_datetime(generated_at)
                    if fixture_dt and latest >= fixture_dt:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Embeddings already loaded and up to date "
                                f"({existing_count} chunks, indexed {latest.strftime('%Y-%m-%d %H:%M')}). "
                                f"Use --force to reload."
                            )
                        )
                        return

        topic_map = dict(HelpTopic.objects.filter(is_published=True).values_list("slug", "id"))
        if not topic_map:
            self.stdout.write(
                self.style.WARNING(
                    "No published help topics found. Run 'python manage.py sync_help --no-index' first."
                )
            )
            return

        self.stdout.write(f"Found {len(topic_map)} published topics in database")

        deleted_count, _ = HelpSearchIndex.objects.all().delete()
        if deleted_count:
            self.stdout.write(f"Cleared {deleted_count} existing index entries")

        entries = []
        skipped = 0
        loaded = 0
        batch_size = 500

        for chunk_data in tqdm(chunks, desc="Loading embeddings", unit="chunk"):
            topic_id = topic_map.get(chunk_data.get("topic_slug"))
            if topic_id is None:
                skipped += 1
                continue

            entries.append(
                HelpSearchIndex(
                    topic_id=topic_id,
                    language=chunk_data["language"],
                    chunk_text=chunk_data["chunk_text"],
                    chunk_position=chunk_data["chunk_position"],
                    embedding=chunk_data["embedding"],
                    is_title_chunk=chunk_data.get("is_title_chunk", False),
                    contains_keywords=chunk_data.get("contains_keywords", False),
                )
            )

            if len(entries) >= batch_size:
                HelpSearchIndex.objects.bulk_create(entries)
                loaded += len(entries)
                entries = []

        if entries:
            HelpSearchIndex.objects.bulk_create(entries)
            loaded += len(entries)

        self.stdout.write(self.style.SUCCESS("\nEmbeddings loaded successfully:"))
        self.stdout.write(f"  Loaded: {loaded} chunks")
        if skipped:
            self.stdout.write(
                self.style.WARNING(f"  Skipped: {skipped} chunks (topic not found in database)")
            )
