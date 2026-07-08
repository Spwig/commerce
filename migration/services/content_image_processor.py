"""
Content Image Processor for WordPress Blog Migration.

Handles extraction and processing of images embedded in blog post content.
Only downloads same-origin images (matching the WordPress source domain)
and replaces their URLs with new Spwig media library URLs.
"""
import logging
import re
import hashlib
import requests
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from django.core.files.base import ContentFile
from django.utils import timezone

from media_library.models import MediaAsset

logger = logging.getLogger(__name__)


class ContentImageProcessor:
    """
    Process images embedded in blog post content.

    This processor:
    - Parses HTML for <img> tags using BeautifulSoup
    - Filters: only downloads same-origin images (matching source domain)
    - Skips external images (CDN, Unsplash, etc.)
    - Downloads images using the media downloader
    - Replaces URLs in content with new media library URLs
    - Handles srcset attributes

    Usage:
        processor = ContentImageProcessor(
            source_domain='example.com',
            migration_job=job
        )
        processed_html, stats = processor.process_content(html_content)
    """

    def __init__(
        self,
        source_domain: str,
        migration_job=None,
        timeout: int = 30,
        max_file_size: int = 10 * 1024 * 1024  # 10MB
    ):
        """
        Initialize the content image processor.

        Args:
            source_domain: The WordPress site domain (for same-origin filtering)
            migration_job: Optional MigrationJob instance for tracking
            timeout: Request timeout in seconds
            max_file_size: Maximum file size to download in bytes
        """
        self.source_domain = source_domain.lower()
        self.migration_job = migration_job
        self.timeout = timeout
        self.max_file_size = max_file_size

        # Cache for processed URLs: old_url -> new_url
        self.processed_urls: Dict[str, str] = {}

        # Statistics
        self.stats = {
            'images_found': 0,
            'images_downloaded': 0,
            'images_skipped_external': 0,
            'images_failed': 0,
            'images_cached': 0,
        }

    def is_same_origin(self, image_url: str) -> bool:
        """
        Check if an image URL is from the WordPress site (same-origin).

        Args:
            image_url: Full URL to the image

        Returns:
            bool: True if the image is from the source domain
        """
        try:
            parsed = urlparse(image_url)
            domain = parsed.netloc.lower()

            # Remove www. prefix for comparison
            if domain.startswith('www.'):
                domain = domain[4:]

            source = self.source_domain
            if source.startswith('www.'):
                source = source[4:]

            # Check if domains match (including subdomains)
            return domain == source or domain.endswith('.' + source)

        except Exception as e:
            logger.warning(f"Error parsing URL {image_url}: {e}")
            return False

    def process_content(self, html_content: str) -> Tuple[str, Dict]:
        """
        Process HTML content and replace same-origin image URLs.

        Args:
            html_content: The HTML content of the blog post

        Returns:
            Tuple of (processed_html, statistics)
        """
        if not html_content:
            return html_content, self.stats.copy()

        # Reset stats for this content
        self.stats = {
            'images_found': 0,
            'images_downloaded': 0,
            'images_skipped_external': 0,
            'images_failed': 0,
            'images_cached': 0,
        }

        # Parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all img tags
        img_tags = soup.find_all('img')
        self.stats['images_found'] = len(img_tags)

        for img in img_tags:
            self._process_img_tag(img)

        # Also check for background images in style attributes
        elements_with_style = soup.find_all(style=True)
        for element in elements_with_style:
            self._process_style_attribute(element)

        return str(soup), self.stats.copy()

    # Regex to detect WordPress auto-generated size variants in filenames
    # Matches patterns like: image-300x169.jpg, photo-1024x575.png, etc.
    WP_SIZE_VARIANT_RE = re.compile(r'-\d+x\d+\.(jpg|jpeg|png|gif|webp)$', re.IGNORECASE)

    def _get_original_url(self, url: str) -> str:
        """
        If a URL is a WordPress size variant, return the original image URL.
        e.g. 'https://site.com/image-300x169.jpg' -> 'https://site.com/image.jpg'
        """
        parsed = urlparse(url)
        filename = parsed.path.split('/')[-1]
        match = self.WP_SIZE_VARIANT_RE.search(filename)
        if match:
            ext = match.group(1)
            original_filename = self.WP_SIZE_VARIANT_RE.sub(f'.{ext}', filename)
            original_path = parsed.path[:parsed.path.rfind('/') + 1] + original_filename
            original_url = parsed._replace(path=original_path).geturl()
            logger.debug(f"Detected WP size variant: {filename} -> {original_filename}")
            return original_url
        return url

    def _process_img_tag(self, img_tag) -> None:
        """
        Process a single img tag.

        Args:
            img_tag: BeautifulSoup img tag element
        """
        # Process src attribute
        src = img_tag.get('src', '')
        if src:
            new_src = self._process_image_url(src)
            if new_src and new_src != src:
                img_tag['src'] = new_src

        # Strip srcset — our media library generates its own responsive thumbnails,
        # so WordPress srcset variants are unnecessary and would create duplicate assets
        if img_tag.get('srcset'):
            del img_tag['srcset']
        if img_tag.get('data-srcset'):
            del img_tag['data-srcset']

        # Process data-src (lazy loading)
        data_src = img_tag.get('data-src', '')
        if data_src:
            new_data_src = self._process_image_url(data_src)
            if new_data_src and new_data_src != data_src:
                img_tag['data-src'] = new_data_src

    def _process_style_attribute(self, element) -> None:
        """
        Process background-image URLs in style attributes.

        Args:
            element: BeautifulSoup element with style attribute
        """
        style = element.get('style', '')
        if 'url(' not in style:
            return

        # Find all url(...) patterns
        url_pattern = re.compile(r'url\([\'"]?([^\'")]+)[\'"]?\)')

        def replace_url(match):
            url = match.group(1)
            new_url = self._process_image_url(url)
            if new_url and new_url != url:
                return f'url("{new_url}")'
            return match.group(0)

        new_style = url_pattern.sub(replace_url, style)
        if new_style != style:
            element['style'] = new_style

    def _process_image_url(self, url: str) -> Optional[str]:
        """
        Process a single image URL.

        Downloads same-origin images and returns new media library URL.
        Returns original URL for external images.

        Args:
            url: Image URL to process

        Returns:
            New URL if downloaded, original URL otherwise
        """
        if not url or url.startswith('data:'):
            return url

        # Redirect WordPress size variant URLs to their original
        # e.g. image-300x169.jpg -> image.jpg (avoids importing duplicates)
        url = self._get_original_url(url)

        # Check cache first
        if url in self.processed_urls:
            self.stats['images_cached'] += 1
            return self.processed_urls[url]

        # Check if same-origin
        if not self.is_same_origin(url):
            self.stats['images_skipped_external'] += 1
            self.processed_urls[url] = url
            return url

        # Download and import the image
        try:
            media_asset = self._download_and_create_asset(url)
            if media_asset:
                new_url = media_asset.get_display_url()
                self.processed_urls[url] = new_url
                self.stats['images_downloaded'] += 1
                return new_url
            else:
                self.stats['images_failed'] += 1
                self.processed_urls[url] = url
                return url

        except Exception as e:
            logger.error(f"Failed to process image {url}: {e}")
            self.stats['images_failed'] += 1
            self.processed_urls[url] = url
            return url

    def _download_and_create_asset(self, url: str) -> Optional[MediaAsset]:
        """
        Download an image and create a MediaAsset.

        Args:
            url: Image URL to download

        Returns:
            MediaAsset instance or None if failed
        """
        try:
            # Check for existing asset by URL hash
            url_hash = hashlib.md5(url.encode()).hexdigest()
            existing = MediaAsset.objects.filter(
                external_id=f"wp_content_image_{url_hash}"
            ).first()

            if existing:
                logger.debug(f"Found existing asset for {url}")
                return existing

            # Download the image
            response = requests.get(url, timeout=self.timeout, stream=True)
            response.raise_for_status()

            # Check content length
            content_length = int(response.headers.get('Content-Length', 0))
            if content_length > self.max_file_size:
                logger.warning(f"Image too large ({content_length} bytes): {url}")
                return None

            # Read content
            content = response.content

            # Get filename from URL
            parsed = urlparse(url)
            filename = parsed.path.split('/')[-1]
            if not filename or '.' not in filename:
                filename = f"image_{url_hash[:8]}.jpg"

            # Detect mime type
            content_type = response.headers.get('Content-Type', 'image/jpeg')
            if ';' in content_type:
                content_type = content_type.split(';')[0].strip()

            # Create MediaAsset
            media_asset = MediaAsset.objects.create(
                external_id=f"wp_content_image_{url_hash}",
                migration_job=self.migration_job,
                title=filename.rsplit('.', 1)[0].replace('-', ' ').replace('_', ' ').title(),
                alt_text='',
                mime_type=content_type,
                file_size=len(content),
                created_at=timezone.now(),
            )

            # Save the file
            media_asset.original_file.save(
                filename,
                ContentFile(content),
                save=True
            )

            # Try to generate WebP and thumbnails
            self._generate_variants(media_asset)

            logger.debug(f"Created MediaAsset for content image: {filename}")
            return media_asset

        except requests.exceptions.RequestException as e:
            logger.warning(f"Failed to download image {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error creating MediaAsset for {url}: {e}")
            return None

    def _generate_variants(self, media_asset: MediaAsset) -> None:
        """
        Generate WebP version and thumbnails for a media asset.

        Args:
            media_asset: MediaAsset instance
        """
        try:
            from media_library.services import ImageProcessor
            from media_library.models import MediaThumbnail
            from media_library.models import ImageSizePreset

            # Skip non-images
            if not media_asset.mime_type.startswith('image/'):
                return

            # Skip SVGs
            if 'svg' in media_asset.mime_type:
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
                        crop_mode=preset.crop_mode
                    )
                    if original_content:
                        thumbnail = MediaThumbnail.objects.create(
                            media_asset=media_asset,
                            size_preset=preset.slug,
                            width=preset.width,
                            height=preset.height
                        )
                        thumbnail.file.save(
                            f"{media_asset.id}_{preset.slug}.jpg",
                            original_content,
                            save=False
                        )
                        if webp_content:
                            thumbnail.webp_file.save(
                                f"{media_asset.id}_{preset.slug}.webp",
                                webp_content,
                                save=False
                            )
                        thumbnail.save()
            except Exception as e:
                logger.debug(f"Failed to generate thumbnails: {e}")

        except ImportError:
            logger.debug("ImageProcessor not available, skipping variant generation")
        except Exception as e:
            logger.warning(f"Error generating variants: {e}")

    def get_stats(self) -> Dict:
        """Get processing statistics."""
        return self.stats.copy()

    def clear_cache(self) -> None:
        """Clear the URL cache."""
        self.processed_urls.clear()
