"""
Media downloader for WooCommerce product images

Downloads images from WooCommerce products and processes them through the media library.
Handles duplicate detection, retry logic, and progress tracking.
"""
import os
import requests
import hashlib
import mimetypes
from typing import Dict, List, Optional, Tuple, Callable
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction
from django.contrib.auth.models import User
from media_library.models import MediaAsset, MediaFolder
from media_library.services import ImageProcessor
import logging

logger = logging.getLogger(__name__)


class MediaDownloader:
    """Download and process images from external sources"""

    def __init__(self, migration_job, user: Optional[User] = None):
        """
        Initialize media downloader

        Args:
            migration_job: MigrationJob instance for tracking
            user: User who initiated the migration (for media ownership)
        """
        self.job = migration_job
        self.user = user
        self.image_processor = ImageProcessor()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; ShopMigration/1.0)'
        })

        # Stats tracking
        self.stats = {
            'total': 0,
            'downloaded': 0,
            'skipped': 0,
            'failed': 0,
            'duplicates': 0,
        }

    def download_product_images(
        self,
        product_data: Dict,
        folder_name: str = 'migration',
        progress_callback: Optional[Callable] = None
    ) -> List[MediaAsset]:
        """
        Download all images for a WooCommerce product

        Args:
            product_data: WooCommerce product dictionary
            folder_name: Media folder to organize images
            progress_callback: Optional callback for progress updates

        Returns:
            List of MediaAsset instances
        """
        media_assets = []

        # Get or create migration folder
        folder = self._get_or_create_folder(folder_name)

        # Process featured image
        if product_data.get('images'):
            images = product_data['images']
            self.stats['total'] += len(images)

            for idx, image_data in enumerate(images):
                try:
                    # Download and process image
                    asset = self._download_and_process_image(
                        image_url=image_data.get('src'),
                        image_name=image_data.get('name') or f"product_{product_data['id']}_image_{idx}",
                        alt_text=image_data.get('alt', ''),
                        folder=folder
                    )

                    if asset:
                        media_assets.append(asset)
                        self.stats['downloaded'] += 1
                        logger.info(f"Downloaded image {idx + 1}/{len(images)} for product {product_data['id']}")
                    else:
                        self.stats['failed'] += 1
                        logger.warning(f"Failed to download image {idx + 1} for product {product_data['id']}")

                    # Progress callback
                    if progress_callback:
                        progress_callback(
                            current=self.stats['downloaded'],
                            total=self.stats['total'],
                            status=f"Downloaded {self.stats['downloaded']}/{self.stats['total']} images"
                        )

                except Exception as e:
                    self.stats['failed'] += 1
                    logger.error(f"Error downloading image {idx} for product {product_data['id']}: {e}")
                    continue

        return media_assets

    def _download_and_process_image(
        self,
        image_url: str,
        image_name: str,
        alt_text: str = '',
        folder: Optional[MediaFolder] = None
    ) -> Optional[MediaAsset]:
        """
        Download a single image and create MediaAsset

        Args:
            image_url: URL of the image to download
            image_name: Name for the media asset
            alt_text: Alternative text for the image
            folder: MediaFolder to organize the asset

        Returns:
            MediaAsset instance or None if failed
        """
        try:
            # Download image with retry logic
            image_data, content_type = self._download_file(image_url)
            if not image_data:
                return None

            # Check for duplicates using content hash
            file_hash = hashlib.md5(image_data).hexdigest()
            existing = MediaAsset.objects.filter(metadata__contains={'hash': file_hash}).first()

            if existing:
                logger.info(f"Image already exists (duplicate): {image_name}")
                self.stats['duplicates'] += 1
                return existing

            # Determine file extension and mime type
            ext = self._get_extension_from_url(image_url) or '.jpg'
            mime_type = content_type or mimetypes.guess_type(image_url)[0] or 'image/jpeg'

            # Create file object
            image_file = ContentFile(image_data, name=f"{image_name}{ext}")

            # Extract metadata
            metadata = self.image_processor.extract_metadata(BytesIO(image_data))
            metadata['source_url'] = image_url
            metadata['migration_job_id'] = str(self.job.id)

            # Get dimensions
            dimensions = self.image_processor.get_image_dimensions(BytesIO(image_data))
            width, height = dimensions if dimensions else (None, None)

            # Calculate focal point
            focal_x, focal_y = self.image_processor.calculate_focal_point(BytesIO(image_data))

            # Create MediaAsset with transaction
            with transaction.atomic():
                media_asset = MediaAsset.objects.create(
                    title=image_name,
                    alt_text=alt_text,
                    original_file=image_file,
                    file_size=len(image_data),
                    width=width,
                    height=height,
                    mime_type=mime_type,
                    folder=folder,
                    metadata=metadata,
                    focal_point_x=focal_x,
                    focal_point_y=focal_y,
                    uploaded_by=self.user,
                    is_public=True
                )

                # Convert to WebP
                try:
                    webp_content = self.image_processor.convert_to_webp(BytesIO(image_data))
                    if webp_content:
                        media_asset.webp_file.save(
                            f"{image_name}.webp",
                            webp_content,
                            save=False
                        )
                        logger.info(f"Generated WebP version for {image_name}")
                except Exception as e:
                    logger.warning(f"Failed to generate WebP for {image_name}: {e}")

                media_asset.save()

                # Generate thumbnails (async if possible, sync for now)
                self._generate_thumbnails(media_asset)

                logger.info(f"Created MediaAsset: {media_asset.id} - {image_name}")
                return media_asset

        except Exception as e:
            logger.error(f"Error processing image {image_name}: {e}")
            return None

    def _download_file(
        self,
        url: str,
        max_retries: int = 3,
        timeout: int = 30
    ) -> Tuple[Optional[bytes], Optional[str]]:
        """
        Download file from URL with retry logic

        Args:
            url: URL to download
            max_retries: Maximum number of retry attempts
            timeout: Request timeout in seconds

        Returns:
            Tuple of (file_data, content_type)
        """
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, timeout=timeout, stream=True)

                if response.status_code == 200:
                    # Download in chunks to handle large files
                    chunks = []
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            chunks.append(chunk)

                    file_data = b''.join(chunks)
                    content_type = response.headers.get('Content-Type')

                    return file_data, content_type

                elif response.status_code == 404:
                    logger.warning(f"Image not found (404): {url}")
                    return None, None

                else:
                    logger.warning(f"Failed to download {url}: HTTP {response.status_code}")
                    if attempt < max_retries - 1:
                        # Retry on non-404 errors
                        continue
                    return None, None

            except requests.exceptions.Timeout:
                logger.warning(f"Timeout downloading {url}, attempt {attempt + 1}/{max_retries}")
                if attempt < max_retries - 1:
                    continue
                return None, None

            except requests.exceptions.RequestException as e:
                logger.error(f"Request error downloading {url}: {e}")
                if attempt < max_retries - 1:
                    continue
                return None, None

        return None, None

    def _get_or_create_folder(self, folder_name: str) -> MediaFolder:
        """
        Get or create a media folder for migration

        Args:
            folder_name: Name of the folder

        Returns:
            MediaFolder instance
        """
        folder, created = MediaFolder.objects.get_or_create(
            name=folder_name,
            defaults={
                'description': f'Images imported from WooCommerce migration job {self.job.id}',
                'created_by': self.user
            }
        )

        if created:
            logger.info(f"Created media folder: {folder_name}")

        return folder

    def _generate_thumbnails(self, media_asset: MediaAsset):
        """
        Generate thumbnails for a media asset

        Args:
            media_asset: MediaAsset to generate thumbnails for
        """
        from media_library.models import ImageSizePreset, MediaThumbnail

        try:
            # Get active size presets
            presets = ImageSizePreset.objects.filter(is_active=True)

            for preset in presets:
                try:
                    # Open original file
                    media_asset.original_file.open('rb')

                    # Generate thumbnail
                    thumb_content, webp_content = self.image_processor.generate_thumbnail(
                        media_asset.original_file,
                        preset.width,
                        preset.height,
                        preset.crop_mode
                    )

                    if thumb_content:
                        # Create or update thumbnail
                        thumbnail, created = MediaThumbnail.objects.get_or_create(
                            media_asset=media_asset,
                            size_preset=preset.slug,
                            defaults={
                                'width': preset.width,
                                'height': preset.height
                            }
                        )

                        # Save files
                        thumbnail.file.save(
                            f"{media_asset.id}_{preset.slug}.jpg",
                            thumb_content,
                            save=False
                        )

                        if webp_content:
                            thumbnail.webp_file.save(
                                f"{media_asset.id}_{preset.slug}.webp",
                                webp_content,
                                save=False
                            )

                        thumbnail.save()
                        logger.debug(f"Generated thumbnail {preset.slug} for {media_asset.id}")

                    media_asset.original_file.close()

                except Exception as e:
                    logger.warning(f"Failed to generate thumbnail {preset.slug} for {media_asset.id}: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error generating thumbnails for {media_asset.id}: {e}")

    def _get_extension_from_url(self, url: str) -> Optional[str]:
        """
        Extract file extension from URL

        Args:
            url: Image URL

        Returns:
            File extension with dot (e.g., '.jpg') or None
        """
        try:
            # Remove query parameters
            path = url.split('?')[0]
            ext = os.path.splitext(path)[1].lower()

            # Validate extension
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']
            if ext in valid_extensions:
                return ext

            return None
        except:
            return None

    def get_stats(self) -> Dict:
        """
        Get download statistics

        Returns:
            Dictionary with stats
        """
        return {
            **self.stats,
            'success_rate': (
                (self.stats['downloaded'] / self.stats['total'] * 100)
                if self.stats['total'] > 0 else 0
            )
        }

    def cleanup(self):
        """Cleanup resources"""
        self.session.close()


class BatchMediaDownloader:
    """Download media for multiple products in batch with concurrency control"""

    def __init__(
        self,
        migration_job,
        user: Optional[User] = None,
        max_concurrent: int = 5
    ):
        """
        Initialize batch downloader

        Args:
            migration_job: MigrationJob instance
            user: User who initiated migration
            max_concurrent: Maximum concurrent downloads
        """
        self.migration_job = migration_job
        self.user = user
        self.max_concurrent = max_concurrent
        self.downloader = MediaDownloader(migration_job, user)

    def download_products_media(
        self,
        products: List[Dict],
        progress_callback: Optional[Callable] = None
    ) -> Dict[str, List[MediaAsset]]:
        """
        Download images for multiple products

        Args:
            products: List of WooCommerce product dictionaries
            progress_callback: Optional progress callback

        Returns:
            Dictionary mapping product IDs to lists of MediaAsset instances
        """
        results = {}
        total = len(products)

        for idx, product in enumerate(products):
            try:
                product_id = str(product.get('id'))

                # Download images for this product
                assets = self.downloader.download_product_images(
                    product_data=product,
                    folder_name=f"migration_{self.migration_job.id}",
                    progress_callback=None  # Use outer progress callback instead
                )

                results[product_id] = assets

                # Overall progress callback
                if progress_callback:
                    progress_callback(
                        current=idx + 1,
                        total=total,
                        product_id=product_id,
                        assets_count=len(assets)
                    )

            except Exception as e:
                logger.error(f"Error downloading media for product {product.get('id')}: {e}")
                results[str(product.get('id'))] = []
                continue

        return results

    def get_stats(self) -> Dict:
        """Get aggregated download statistics"""
        return self.downloader.get_stats()

    def cleanup(self):
        """Cleanup resources"""
        self.downloader.cleanup()
