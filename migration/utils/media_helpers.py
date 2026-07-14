"""
Media Helper Utilities for Migration.

Provides helper functions for downloading and creating media assets
during WordPress/WooCommerce migration.
"""

import hashlib
import logging
from urllib.parse import urlparse

import requests
from django.core.files.base import ContentFile
from django.utils import timezone

from media_library.models import MediaAsset

logger = logging.getLogger(__name__)


def download_and_create_media_asset(
    url: str,
    alt_text: str = "",
    title: str = "",
    timeout: int = 30,
    max_file_size: int = 10 * 1024 * 1024,  # 10MB
    migration_job=None,
) -> MediaAsset | None:
    """
    Download an image from a URL and create a MediaAsset.

    Args:
        url: URL to download the image from
        alt_text: Alt text for the image
        title: Title for the media asset
        timeout: Request timeout in seconds
        max_file_size: Maximum file size to download in bytes
        migration_job: Optional MigrationJob for tracking

    Returns:
        MediaAsset instance or None if failed
    """
    try:
        # Generate a unique identifier based on URL
        url_hash = hashlib.md5(url.encode()).hexdigest()

        # Check for existing asset by URL hash
        existing = MediaAsset.objects.filter(external_id=f"wp_media_{url_hash}").first()

        if existing:
            logger.debug(f"Found existing asset for {url}")
            return existing

        # Download the image
        response = requests.get(url, timeout=timeout, stream=True)
        response.raise_for_status()

        # Check content length
        content_length = int(response.headers.get("Content-Length", 0))
        if content_length > max_file_size:
            logger.warning(f"Image too large ({content_length} bytes): {url}")
            return None

        # Read content
        content = response.content

        # Get filename from URL
        parsed = urlparse(url)
        filename = parsed.path.split("/")[-1]
        if not filename or "." not in filename:
            filename = f"image_{url_hash[:8]}.jpg"

        # Clean up title
        if not title:
            title = filename.rsplit(".", 1)[0].replace("-", " ").replace("_", " ").title()

        # Detect mime type
        content_type = response.headers.get("Content-Type", "image/jpeg")
        if ";" in content_type:
            content_type = content_type.split(";")[0].strip()

        # Create MediaAsset
        media_asset = MediaAsset.objects.create(
            external_id=f"wp_media_{url_hash}",
            migration_job=migration_job,
            title=title,
            alt_text=alt_text,
            mime_type=content_type,
            file_size=len(content),
            created_at=timezone.now(),
        )

        # Save the file
        media_asset.original_file.save(filename, ContentFile(content), save=True)

        # Try to generate WebP and thumbnails
        _generate_variants(media_asset)

        logger.debug(f"Created MediaAsset: {media_asset.id} - {filename}")
        return media_asset

    except requests.exceptions.RequestException as e:
        logger.warning(f"Failed to download image {url}: {e}")
        return None
    except Exception as e:
        logger.error(f"Error creating MediaAsset for {url}: {e}")
        return None


def _generate_variants(media_asset: MediaAsset) -> None:
    """
    Generate WebP version and thumbnails for a media asset.

    Args:
        media_asset: MediaAsset instance
    """
    try:
        from media_library.models import ImageSizePreset, MediaThumbnail
        from media_library.services import ImageProcessor

        # Skip non-images
        if not media_asset.mime_type.startswith("image/"):
            return

        # Skip SVGs
        if "svg" in media_asset.mime_type:
            return

        processor = ImageProcessor()

        # Generate WebP
        try:
            webp_content = processor.convert_to_webp(media_asset.original_file)
            if webp_content:
                webp_filename = f"{media_asset.id}.webp"
                media_asset.webp_file.save(webp_filename, webp_content, save=True)
        except Exception as e:
            logger.debug(f"Failed to generate WebP: {e}")

        # Generate thumbnails
        try:
            for preset in ImageSizePreset.objects.filter(is_active=True):
                original_content, webp_content = processor.generate_thumbnail(
                    media_asset.original_file,
                    preset.width,
                    preset.height,
                    crop_mode=preset.crop_mode,
                )
                if original_content:
                    thumbnail = MediaThumbnail.objects.create(
                        media_asset=media_asset,
                        size_preset=preset.slug,
                        width=preset.width,
                        height=preset.height,
                    )
                    thumbnail.file.save(
                        f"{media_asset.id}_{preset.slug}.jpg", original_content, save=False
                    )
                    if webp_content:
                        thumbnail.webp_file.save(
                            f"{media_asset.id}_{preset.slug}.webp", webp_content, save=False
                        )
                    thumbnail.save()
        except Exception as e:
            logger.debug(f"Failed to generate thumbnails: {e}")

    except ImportError:
        logger.debug("ImageProcessor not available, skipping variant generation")
    except Exception as e:
        logger.warning(f"Error generating variants: {e}")
