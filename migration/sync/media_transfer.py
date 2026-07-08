"""
Media Transfer Service

Handles chunked media file transfer for full system migration.
Uses streaming endpoints rather than base64 inline encoding.
Works with both local filesystem and S3/MinIO storage backends.
"""
import hashlib
import logging

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import Sum

logger = logging.getLogger(__name__)

# Transfer chunk size (5MB)
CHUNK_SIZE = 5 * 1024 * 1024

# Maximum media assets per batch
BATCH_SIZE = 50


def export_media_metadata(queryset):
    """
    Export metadata for media assets (without file content).

    Args:
        queryset: QuerySet of MediaAsset instances

    Returns:
        list of dicts with asset metadata
    """
    metadata = []
    for asset in queryset.iterator():
        entry = {
            'id': asset.pk,
            'original_file': asset.original_file.name if asset.original_file else None,
            'webp_file': asset.webp_file.name if asset.webp_file else None,
        }

        # Add optional fields if they exist
        if hasattr(asset, 'converted_video') and asset.converted_video:
            entry['converted_video'] = asset.converted_video.name
        if hasattr(asset, 'poster_image') and asset.poster_image:
            entry['poster_image'] = asset.poster_image.name

        # Add non-file metadata
        for field_name in ['title', 'alt_text', 'caption', 'content_type',
                           'file_size', 'width', 'height', 'duration']:
            if hasattr(asset, field_name):
                entry[field_name] = getattr(asset, field_name)

        # Compute checksum for verification
        if asset.original_file:
            try:
                entry['checksum'] = _compute_file_checksum(asset.original_file)
            except Exception:
                entry['checksum'] = None

        metadata.append(entry)

    return metadata


def stream_media_file(file_field):
    """
    Generator that yields chunks of a file for streaming transfer.

    Args:
        file_field: Django FileField value

    Yields:
        bytes: File chunks
    """
    if not file_field or not file_field.name:
        return

    try:
        file_field.open('rb')
        try:
            while True:
                chunk = file_field.read(CHUNK_SIZE)
                if not chunk:
                    break
                yield chunk
        finally:
            file_field.close()
    except Exception as e:
        logger.error(f"Error streaming file {file_field.name}: {e}")
        raise


def import_media_file(file_content, target_path, expected_checksum=None):
    """
    Save a downloaded media file to the target storage.

    Args:
        file_content: bytes or file-like object
        target_path: Relative path within MEDIA_ROOT
        expected_checksum: Optional MD5 checksum for verification

    Returns:
        dict: {success, saved_path, error}
    """
    try:
        if isinstance(file_content, bytes):
            content_file = ContentFile(file_content)
        else:
            content_file = file_content

        # Verify checksum if provided
        if expected_checksum:
            if isinstance(file_content, bytes):
                actual_checksum = hashlib.md5(file_content).hexdigest()
            else:
                hasher = hashlib.md5()
                for chunk in file_content.chunks():
                    hasher.update(chunk)
                actual_checksum = hasher.hexdigest()

            if actual_checksum != expected_checksum:
                return {
                    'success': False,
                    'saved_path': None,
                    'error': f"Checksum mismatch: expected {expected_checksum}, got {actual_checksum}",
                }

        # Save using Django's storage API (works for local and S3)
        saved_path = default_storage.save(target_path, content_file)

        return {
            'success': True,
            'saved_path': saved_path,
            'error': None,
        }

    except Exception as e:
        logger.error(f"Failed to save media file to {target_path}: {e}")
        return {
            'success': False,
            'saved_path': None,
            'error': str(e),
        }


def get_media_transfer_batches(asset_ids):
    """
    Split asset IDs into transfer batches.

    Args:
        asset_ids: list of media asset IDs

    Returns:
        list of lists (batches)
    """
    return [
        asset_ids[i:i + BATCH_SIZE]
        for i in range(0, len(asset_ids), BATCH_SIZE)
    ]


def get_media_total_size():
    """
    Estimate total size of all media files in the library.

    Returns:
        int: Total size in bytes
    """
    try:
        from media_library.models import MediaAsset
        result = MediaAsset.objects.aggregate(
            total_size=Sum('file_size')
        )
        return result.get('total_size') or 0
    except Exception:
        return 0


def _compute_file_checksum(file_field):
    """Compute MD5 checksum of a file."""
    hasher = hashlib.md5()
    file_field.open('rb')
    try:
        for chunk in iter(lambda: file_field.read(CHUNK_SIZE), b''):
            hasher.update(chunk)
    finally:
        file_field.close()
    return hasher.hexdigest()
