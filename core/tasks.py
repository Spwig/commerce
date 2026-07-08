"""
Celery tasks for core app
"""
from celery import shared_task
from django.core.cache import cache
from django.utils import timezone
from core.celery_utils import BackgroundDBTask
import logging

logger = logging.getLogger(__name__)


@shared_task(name='core.refresh_platform_secrets', ignore_result=True)
def refresh_platform_secrets():
    """
    Refresh platform secrets from license server if needed.
    Run periodically to ensure secrets don't expire during operation.

    This task runs every 30 minutes via Celery beat to ensure
    the JWT tokens and service secrets remain valid.
    """
    from core.models import PlatformSecrets
    from component_updates.services import UpdateManager

    try:
        secrets = PlatformSecrets.get_secrets()

        # Check if secrets need refresh (within 5 minutes of expiry or not initialized)
        if secrets.needs_token_refresh:
            logger.info("Platform secrets need refresh, authenticating with license server...")

            manager = UpdateManager()
            manager._ensure_authenticated()

            # Verify secrets were updated
            secrets.refresh_from_db()
            if secrets.is_initialized:
                logger.info("✅ Platform secrets refreshed successfully")
            else:
                logger.warning("⚠️ Authenticated but secrets not fully initialized")
        else:
            logger.debug("Platform secrets still valid, no refresh needed")

        return {'status': 'success', 'is_initialized': secrets.is_initialized}

    except Exception as e:
        logger.error(f"❌ Failed to refresh platform secrets: {e}")
        return {'status': 'error', 'error': str(e)}


@shared_task(bind=True, name='core.regenerate_thumbnails')
def regenerate_thumbnails_task(self):
    """
    Background task to regenerate all product image thumbnails.
    Uses Celery for proper background processing to handle thousands of images.
    """
    from media_library.models import MediaAsset, MediaThumbnail, ImageSizePreset
    from media_library.services import ImageProcessor

    processor = ImageProcessor()
    # Get image size presets from database (configurable in Media Library → Image Size Presets)
    image_presets = list(ImageSizePreset.objects.filter(is_active=True))

    # Get all product images
    product_image_assets = MediaAsset.objects.filter(
        product_uses__isnull=False
    ).distinct()

    total = product_image_assets.count()
    processed = 0

    # Initialize status in cache
    cache.set('thumbnail_regeneration_status', {
        'task_id': self.request.id,
        'complete': False,
        'progress': 0,
        'processed': 0,
        'total': total,
        'message': f'Starting regeneration of {total} images...'
    }, timeout=7200)  # 2 hours timeout

    try:
        for asset in product_image_assets:
            try:
                # Skip non-images
                if not asset.is_image():
                    processed += 1
                    continue

                # Delete existing thumbnails
                MediaThumbnail.objects.filter(media_asset=asset).delete()

                # Generate WebP if not exists
                if not asset.webp_file and asset.mime_type != 'image/svg+xml':
                    try:
                        webp_content = processor.convert_to_webp(asset.original_file)
                        if webp_content:
                            webp_filename = f"{asset.id}.webp"
                            asset.webp_file.save(webp_filename, webp_content, save=True)
                    except Exception as e:
                        logger.warning(f"Failed to generate WebP for asset {asset.id}: {e}")

                # Generate all thumbnail sizes
                for preset in image_presets:
                    try:
                        original_content, webp_content = processor.generate_thumbnail(
                            asset.original_file,
                            preset.width,
                            preset.height,
                            crop_mode=preset.crop_mode
                        )

                        if original_content:
                            thumbnail = MediaThumbnail.objects.create(
                                media_asset=asset,
                                size_preset=preset.slug,
                                width=preset.width,
                                height=preset.height
                            )
                            thumbnail.file.save(f"{asset.id}_{preset.slug}.jpg", original_content, save=False)
                            if webp_content:
                                thumbnail.webp_file.save(f"{asset.id}_{preset.slug}.webp", webp_content, save=False)
                            thumbnail.save()
                    except Exception as e:
                        logger.warning(f"Failed to generate {preset.slug} thumbnail for asset {asset.id}: {e}")

                processed += 1
                progress = int((processed / total) * 100) if total > 0 else 100

                # Update progress in cache
                cache.set('thumbnail_regeneration_status', {
                    'task_id': self.request.id,
                    'complete': False,
                    'progress': progress,
                    'processed': processed,
                    'total': total,
                    'message': f'Processing image {processed} of {total}...'
                }, timeout=7200)

                # Update Celery task state for monitoring
                self.update_state(
                    state='PROGRESS',
                    meta={
                        'processed': processed,
                        'total': total,
                        'progress': progress
                    }
                )

            except Exception as e:
                logger.error(f"Error regenerating thumbnails for asset {asset.id}: {e}")
                processed += 1

        # Mark as complete
        completion_time = timezone.now()
        cache.set('thumbnail_regeneration_status', {
            'task_id': self.request.id,
            'complete': True,
            'progress': 100,
            'processed': processed,
            'total': total,
            'message': f'Completed! Regenerated {processed} images.'
        }, timeout=7200)

        # Store last regeneration timestamp (persists longer)
        cache.set('thumbnail_last_regeneration', {
            'timestamp': completion_time.isoformat(),
            'processed': processed,
            'total': total
        }, timeout=2592000)  # 30 days

        return {
            'status': 'complete',
            'processed': processed,
            'total': total
        }

    except Exception as e:
        logger.error(f"Fatal error in thumbnail regeneration task: {e}")
        # Mark as failed
        cache.set('thumbnail_regeneration_status', {
            'task_id': self.request.id,
            'complete': True,
            'progress': 0,
            'processed': processed,
            'total': total,
            'message': f'Failed: {str(e)}',
            'error': str(e)
        }, timeout=7200)
        raise


@shared_task(name='core.cleanup_expired_trusted_devices', base=BackgroundDBTask, ignore_result=True)
def cleanup_expired_trusted_devices():
    """
    Clean up expired and revoked trusted devices.

    This task should run daily via Celery beat to remove:
    - Devices that have passed their expiration date
    - Devices that were revoked more than 30 days ago

    This helps maintain database hygiene and ensures that old device
    records don't accumulate indefinitely.
    """
    from core.models import TrustedDevice

    try:
        # Delete expired devices
        expired_count = TrustedDevice.cleanup_expired()

        # Also delete revoked devices older than 30 days
        revoked_cutoff = timezone.now() - timezone.timedelta(days=30)
        old_revoked = TrustedDevice.objects.filter(
            is_revoked=True,
            created_at__lt=revoked_cutoff
        )
        revoked_count = old_revoked.count()
        old_revoked.delete()

        total_deleted = expired_count + revoked_count

        if total_deleted > 0:
            logger.info(
                f"Trusted device cleanup: deleted {expired_count} expired, "
                f"{revoked_count} old revoked devices"
            )

        return {
            'status': 'success',
            'expired_deleted': expired_count,
            'revoked_deleted': revoked_count,
            'total_deleted': total_deleted
        }

    except Exception as e:
        logger.error(f"Failed to cleanup trusted devices: {e}")
        return {'status': 'error', 'error': str(e)}


@shared_task(
    bind=True,
    name='core.load_help_embeddings',
    base=BackgroundDBTask,
    ignore_result=True,
)
def load_help_embeddings_async(self, fixture_path, force=False, batch_size=200, throttle_seconds=0.1):
    """
    Background task to stream-load help embeddings from a JSONL fixture.

    Uses line-by-line streaming to keep memory usage minimal (~4MB)
    regardless of fixture size. Reports progress via cache for dashboard.
    """
    import gzip
    import json
    import time
    from pathlib import Path

    from django.conf import settings
    from core.models import HelpTopic, HelpSearchIndex

    CACHE_KEY = 'help_embeddings_loading_status'
    EXPECTED_DIMENSIONS = 384
    fixture_path = Path(fixture_path)

    if not fixture_path.is_absolute():
        fixture_path = Path(settings.BASE_DIR) / fixture_path

    def update_progress(status, loaded=0, total=0, message=''):
        progress = int((loaded / total) * 100) if total > 0 else 0
        cache.set(CACHE_KEY, {
            'task_id': self.request.id,
            'status': status,
            'loaded': loaded,
            'total': total,
            'progress': progress,
            'message': message,
        }, timeout=3600)

    try:
        if not fixture_path.exists():
            logger.warning(f"Embeddings fixture not found: {fixture_path}")
            update_progress('error', message=f'Fixture not found: {fixture_path}')
            return

        # Deduplication: skip if already loading
        current = cache.get(CACHE_KEY)
        if current and current.get('status') == 'loading' and current.get('task_id') != self.request.id:
            logger.info("Help embeddings already loading in another task, skipping")
            return

        # Read header (first line of JSONL)
        with gzip.open(fixture_path, 'rt', encoding='utf-8') as f:
            header = json.loads(f.readline())

        total_chunks = header.get('stats', {}).get('total_chunks', 0)

        if header.get('model_dimensions') != EXPECTED_DIMENSIONS:
            msg = f"Dimension mismatch: expected {EXPECTED_DIMENSIONS}, got {header.get('model_dimensions')}"
            logger.error(msg)
            update_progress('error', message=msg)
            return

        # Freshness check
        if not force:
            existing_count = HelpSearchIndex.objects.count()
            if existing_count > 0:
                latest = HelpSearchIndex.objects.order_by('-indexed_at').values_list(
                    'indexed_at', flat=True
                ).first()
                generated_at = header.get('generated_at', '')
                if latest and generated_at:
                    from django.utils.dateparse import parse_datetime
                    fixture_dt = parse_datetime(generated_at)
                    if fixture_dt and latest >= fixture_dt:
                        logger.info(
                            f"Help embeddings already loaded and up to date "
                            f"({existing_count} chunks). Skipping."
                        )
                        update_progress('complete', loaded=existing_count, total=existing_count,
                                        message='Already up to date')
                        return

        # Build topic slug -> id lookup
        topic_map = dict(
            HelpTopic.objects.filter(is_published=True).values_list('slug', 'id')
        )

        if not topic_map:
            logger.warning("No published help topics found. Run sync_help first.")
            update_progress('error', message='No published help topics')
            return

        # Clear existing search index
        deleted_count, _ = HelpSearchIndex.objects.all().delete()
        if deleted_count:
            logger.info(f"Cleared {deleted_count} existing index entries")

        update_progress('loading', loaded=0, total=total_chunks, message='Starting...')

        # Stream JSONL line by line
        entries = []
        loaded = 0
        skipped = 0

        with gzip.open(fixture_path, 'rt', encoding='utf-8') as f:
            f.readline()  # skip header
            for line in f:
                line = line.strip()
                if not line:
                    continue

                chunk_data = json.loads(line)
                topic_id = topic_map.get(chunk_data.get('topic_slug'))

                if topic_id is None:
                    skipped += 1
                    continue

                entries.append(HelpSearchIndex(
                    topic_id=topic_id,
                    language=chunk_data['language'],
                    chunk_text=chunk_data['chunk_text'],
                    chunk_position=chunk_data['chunk_position'],
                    embedding=chunk_data['embedding'],
                    is_title_chunk=chunk_data.get('is_title_chunk', False),
                    contains_keywords=chunk_data.get('contains_keywords', False),
                ))

                if len(entries) >= batch_size:
                    HelpSearchIndex.objects.bulk_create(entries)
                    loaded += len(entries)
                    entries = []
                    update_progress('loading', loaded=loaded, total=total_chunks,
                                    message=f'Loading embeddings: {loaded}/{total_chunks}')
                    if throttle_seconds > 0:
                        time.sleep(throttle_seconds)

        # Insert remaining
        if entries:
            HelpSearchIndex.objects.bulk_create(entries)
            loaded += len(entries)

        update_progress('complete', loaded=loaded, total=total_chunks,
                        message=f'Loaded {loaded} embeddings successfully')
        logger.info(f"Help embeddings loaded: {loaded} chunks ({skipped} skipped)")

    except Exception as e:
        logger.error(f"Help embeddings loading failed: {e}")
        update_progress('error', message=str(e))
        raise


@shared_task(bind=True, max_retries=3, name='core.index_help_topic_async')
def index_help_topic_async(self, topic_id, languages=None):
    """
    Asynchronously index a help topic for semantic search.

    Args:
        topic_id: ID of the HelpTopic to index
        languages: List of language codes to index (None = all languages)

    Raises:
        Retry on failure with exponential backoff
    """
    from core.services.semantic_search import IndexingService

    try:
        logger.info(f"Indexing help topic ID {topic_id}")
        stats = IndexingService.index_topic(topic_id, languages=languages)
        logger.info(
            f"Successfully indexed topic {topic_id}: "
            f"{stats['total_chunks']} chunks in {len(stats['languages'])} language(s)"
        )
        return stats
    except Exception as exc:
        logger.error(f"Failed to index topic {topic_id}: {exc}")
        # Retry with exponential backoff: 60s, 120s, 240s
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))
