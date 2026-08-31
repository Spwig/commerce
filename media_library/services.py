import hashlib
import io
import logging

from django.conf import settings
from django.core.files.base import ContentFile
from PIL import ExifTags, Image, ImageOps

logger = logging.getLogger(__name__)


class ImageProcessor:
    """Service for processing images - conversion, optimization, and thumbnail generation"""

    def __init__(self):
        media_settings = getattr(settings, "MEDIA_LIBRARY_SETTINGS", {})
        self.webp_quality = media_settings.get("WEBP_QUALITY", 85)
        self.avif_quality = media_settings.get("AVIF_QUALITY", 63)
        self.avif_speed = media_settings.get("AVIF_SPEED", 6)
        self.thumbnail_sizes = media_settings.get("THUMBNAIL_SIZES", {})

    def convert_to_webp(self, image_file, quality=None, preserve_transparency=False):
        """
        Convert an image to WebP format

        Args:
            image_file: Django UploadedFile or File object
            quality: WebP quality (1-100), uses default if not specified
            preserve_transparency: If True, preserve alpha channel for transparent images

        Returns:
            ContentFile with WebP image
        """
        try:
            # Open image and force load to avoid lazy loading issues
            img = Image.open(image_file)
            img.load()  # Force PIL to fully load image data into memory
            img = self.fix_orientation(img)  # Apply EXIF orientation before encoding

            has_transparency = img.mode in ("RGBA", "LA", "P")

            if has_transparency and preserve_transparency:
                # Preserve transparency - convert to RGBA if needed
                if img.mode == "P" or img.mode == "LA":
                    img = img.convert("RGBA")
                # WebP supports RGBA transparency natively
            elif has_transparency:
                # Flatten to RGB with white background (original behavior)
                background = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "P":
                    img = img.convert("RGBA")
                background.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
                img = background
            elif img.mode not in ("RGB", "L"):
                img = img.convert("RGB")

            # Save as WebP
            output = io.BytesIO()
            img.save(output, format="WEBP", quality=quality or self.webp_quality, method=6)
            output.seek(0)

            return ContentFile(output.read())

        except Exception as e:
            logger.error(f"Error converting image to WebP: {e}")
            return None

    def convert_to_avif(self, image_file, quality=None, speed=None, preserve_transparency=False):
        """
        Convert an image to AVIF format.

        AVIF is the primary next-gen rendition, typically 30-50% smaller than
        WebP at equivalent quality. Alpha is supported natively. Encoding is
        CPU-heavier than WebP, so callers should run this off the request path
        (Celery), not inline during upload.

        Args:
            image_file: Django UploadedFile or File object
            quality: AVIF quality (0-100); uses AVIF_QUALITY setting if not given
            speed: AVIF encoder speed (0-10, higher = faster/larger); uses
                AVIF_SPEED setting if not given
            preserve_transparency: If True, keep the alpha channel

        Returns:
            ContentFile with AVIF image, or None on failure
        """
        try:
            img = Image.open(image_file)
            img.load()  # Force PIL to fully load image data into memory
            img = self.fix_orientation(img)  # Apply EXIF orientation before encoding

            has_transparency = img.mode in ("RGBA", "LA", "P")

            if has_transparency and preserve_transparency:
                # AVIF supports RGBA transparency natively
                if img.mode == "P" or img.mode == "LA":
                    img = img.convert("RGBA")
            elif has_transparency:
                # Flatten to RGB with white background (matches WebP behaviour)
                background = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode in ("P", "LA"):
                    img = img.convert("RGBA")
                background.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
                img = background
            elif img.mode not in ("RGB", "L"):
                img = img.convert("RGB")

            output = io.BytesIO()
            img.save(
                output,
                format="AVIF",
                quality=quality if quality is not None else self.avif_quality,
                speed=speed if speed is not None else self.avif_speed,
            )
            output.seek(0)

            return ContentFile(output.read())

        except Exception as e:
            logger.error(f"Error converting image to AVIF: {e}")
            return None

    def _parse_padding_color(self, padding_color):
        """
        Parse padding color string to a color tuple.

        Args:
            padding_color: 'transparent', 'white', 'black', or '#RRGGBB' hex color

        Returns:
            Tuple (color, is_transparent) where color is RGB/RGBA tuple
        """
        if padding_color == "transparent" or padding_color is None:
            return (0, 0, 0, 0), True  # Transparent (RGBA with alpha=0)
        elif padding_color == "white":
            return (255, 255, 255), False
        elif padding_color == "black":
            return (0, 0, 0), False
        elif padding_color.startswith("#") and len(padding_color) == 7:
            # Parse hex color #RRGGBB
            try:
                r = int(padding_color[1:3], 16)
                g = int(padding_color[3:5], 16)
                b = int(padding_color[5:7], 16)
                return (r, g, b), False
            except ValueError:
                return (255, 255, 255), False  # Default to white on parse error
        else:
            return (255, 255, 255), False  # Default to white

    def generate_thumbnail(self, image_file, width, height, crop_mode="cover", padding_color=None):
        """
        Generate a thumbnail of specified size

        Args:
            image_file: Django UploadedFile or File object
            width: Target width
            height: Target height
            crop_mode: 'contain', 'cover', 'crop', 'pad', or 'smart'
            padding_color: For 'pad' mode - 'transparent', 'white', 'black', or '#RRGGBB'

        Returns:
            Tuple of (image_content, webp_content)
        """
        try:
            img = Image.open(image_file)
            img.load()  # Force PIL to fully load image data into memory

            # Fix orientation based on EXIF data
            img = self.fix_orientation(img)

            # Track if we need to preserve transparency
            preserve_transparency = False

            # Calculate dimensions based on crop mode
            if crop_mode == "contain":
                # Fit image within bounds maintaining aspect ratio
                img.thumbnail((width, height), Image.Resampling.LANCZOS)
            elif crop_mode == "cover":
                # Fill the dimensions, cropping if necessary
                img = ImageOps.fit(img, (width, height), Image.Resampling.LANCZOS)
            elif crop_mode == "crop":
                # Simple center crop to exact dimensions
                img = ImageOps.fit(img, (width, height), Image.Resampling.LANCZOS)
            elif crop_mode == "pad":
                # Fit image within bounds and pad to exact dimensions
                color, is_transparent = self._parse_padding_color(padding_color)
                preserve_transparency = is_transparent

                if is_transparent:
                    # For transparent padding, ensure image is in RGBA mode
                    if img.mode != "RGBA":
                        img = img.convert("RGBA")
                    # Use ImageOps.pad with transparent color
                    img = ImageOps.pad(
                        img, (width, height), Image.Resampling.LANCZOS, color=(0, 0, 0, 0)
                    )
                else:
                    # For solid color padding
                    img = ImageOps.pad(img, (width, height), Image.Resampling.LANCZOS, color=color)
            elif crop_mode == "smart":
                # Smart crop focusing on important areas (simplified version)
                img = self.smart_crop(img, width, height)

            # Determine output format - use PNG for transparent images, JPEG otherwise
            original_format = img.format
            if preserve_transparency or (img.mode == "RGBA" and crop_mode == "pad"):
                format = "PNG"  # Use PNG to preserve transparency in original
            else:
                format = original_format or "JPEG"

            # Save original format thumbnail
            output = io.BytesIO()

            # Convert RGBA to RGB for JPEG format
            save_img = img
            if format == "JPEG" and img.mode in ("RGBA", "LA", "P"):
                # Create white background for transparent images
                background = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "P":
                    img = img.convert("RGBA")
                if img.mode == "RGBA":
                    background.paste(img, mask=img.split()[-1])
                else:
                    background.paste(img)
                save_img = background
            elif format == "JPEG" and img.mode not in ("RGB", "L"):
                save_img = img.convert("RGB")

            if format == "JPEG":
                save_img.save(output, format=format, quality=90, optimize=True)
            elif format == "PNG":
                save_img.save(output, format="PNG", optimize=True)
            else:
                save_img.save(output, format=format)
            output.seek(0)
            original_content = ContentFile(output.read())

            # Save WebP version (WebP supports transparency natively)
            webp_output = io.BytesIO()
            webp_img = img

            if preserve_transparency and webp_img.mode == "RGBA":
                # Preserve transparency in WebP
                pass  # Keep as RGBA
            elif webp_img.mode in ("RGBA", "LA", "P"):
                # Flatten transparency with white background
                background = Image.new("RGB", webp_img.size, (255, 255, 255))
                if webp_img.mode == "P":
                    webp_img = webp_img.convert("RGBA")
                background.paste(
                    webp_img, mask=webp_img.split()[-1] if webp_img.mode == "RGBA" else None
                )
                webp_img = background
            elif webp_img.mode not in ("RGB", "L"):
                webp_img = webp_img.convert("RGB")

            webp_img.save(webp_output, format="WEBP", quality=self.webp_quality, method=6)
            webp_output.seek(0)
            webp_content = ContentFile(webp_output.read())

            return original_content, webp_content

        except Exception as e:
            logger.error(f"Error generating thumbnail: {e}")
            return None, None

    def smart_crop(self, img, width, height):
        """
        Smart crop that tries to focus on the most important part of the image
        Simplified version - can be enhanced with face detection or AI
        """
        # For now, use entropy-based cropping
        # This finds the "busiest" part of the image
        return ImageOps.fit(img, (width, height), Image.Resampling.LANCZOS, centering=(0.5, 0.5))

    def _sanitize_string(self, value):
        """
        Sanitize a string value for PostgreSQL JSON storage.
        Removes null bytes and other problematic characters.
        """
        if isinstance(value, str):
            # Remove null bytes which PostgreSQL JSON cannot store
            return value.replace("\x00", "").replace("\u0000", "")
        return value

    def _sanitize_value(self, value):
        """
        Recursively sanitize a value for JSON storage.
        Handles strings, lists, tuples, and dicts.
        """
        if isinstance(value, str):
            return self._sanitize_string(value)
        elif isinstance(value, (list, tuple)):
            return [self._sanitize_value(v) for v in value]
        elif isinstance(value, dict):
            return {k: self._sanitize_value(v) for k, v in value.items()}
        return value

    def extract_metadata(self, image_file):
        """
        Extract EXIF and other metadata from image

        Returns:
            Dictionary with metadata
        """
        metadata = {
            "exif": {},
            "size": None,
            "format": None,
            "mode": None,
        }

        try:
            img = Image.open(image_file)
            img.load()  # Force PIL to fully load image data into memory

            # Basic metadata
            metadata["size"] = img.size
            metadata["format"] = img.format
            metadata["mode"] = img.mode

            # EXIF data
            exifdata = img.getexif()
            if exifdata:
                for tag_id, value in exifdata.items():
                    tag = ExifTags.TAGS.get(tag_id, tag_id)

                    # Convert to JSON-serializable types
                    if isinstance(value, bytes):
                        try:
                            # Try UTF-16 first (common for Windows XP tags like XPTitle)
                            value = value.decode("utf-16-le").rstrip("\x00")
                        except Exception:
                            try:
                                value = value.decode("utf-8")
                            except Exception:
                                value = str(value)
                    elif hasattr(value, "__class__") and value.__class__.__name__ == "IFDRational":
                        # Convert IFDRational to float
                        value = float(value)
                    elif isinstance(value, (list, tuple)):
                        # Handle lists/tuples that might contain IFDRational
                        converted = []
                        for v in value:
                            if hasattr(v, "__class__") and v.__class__.__name__ == "IFDRational":
                                converted.append(float(v))
                            else:
                                converted.append(v)
                        value = converted

                    # Sanitize to remove null bytes (PostgreSQL JSON cannot store them)
                    value = self._sanitize_value(value)

                    # Final check: ensure value is JSON serializable
                    try:
                        import json

                        json.dumps(value)
                    except (TypeError, ValueError):
                        value = str(value)

                    metadata["exif"][tag] = value

            # Calculate file hash for duplicate detection
            image_file.seek(0)
            metadata["hash"] = hashlib.md5(image_file.read()).hexdigest()
            image_file.seek(0)

        except Exception as e:
            logger.error(f"Error extracting metadata: {e}")

        return metadata

    def fix_orientation(self, img):
        """
        Fix image orientation based on EXIF data.

        Uses ImageOps.exif_transpose, which honours all eight EXIF
        orientation values, including the mirrored ones (2, 4, 5, 7).
        """
        try:
            img = ImageOps.exif_transpose(img)
        except Exception:
            pass

        return img

    def optimize_image(self, image_file, max_width=None, max_height=None):
        """
        Optimize image for web delivery

        Args:
            image_file: Django UploadedFile or File object
            max_width: Maximum width (optional)
            max_height: Maximum height (optional)

        Returns:
            Optimized image as ContentFile
        """
        try:
            img = Image.open(image_file)
            img.load()  # Force PIL to fully load image data into memory
            img = self.fix_orientation(img)

            # Resize if necessary
            if max_width or max_height:
                current_width, current_height = img.size

                # Calculate new dimensions maintaining aspect ratio
                if max_width and current_width > max_width:
                    ratio = max_width / current_width
                    new_height = int(current_height * ratio)
                    img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

                if max_height and img.height > max_height:
                    ratio = max_height / img.height
                    new_width = int(img.width * ratio)
                    img = img.resize((new_width, max_height), Image.Resampling.LANCZOS)

            # Save optimized image
            output = io.BytesIO()
            format = img.format or "JPEG"

            if format == "JPEG":
                # Convert to RGB if necessary
                if img.mode != "RGB":
                    img = img.convert("RGB")
                img.save(output, format="JPEG", quality=85, optimize=True, progressive=True)
            elif format == "PNG":
                img.save(output, format="PNG", optimize=True)
            else:
                img.save(output, format=format)

            output.seek(0)
            return ContentFile(output.read())

        except Exception as e:
            logger.error(f"Error optimizing image: {e}")
            return None

    def get_image_dimensions(self, image_file):
        """
        Get image dimensions without loading the entire image

        Returns:
            Tuple of (width, height)
        """
        try:
            img = Image.open(image_file)
            img.load()  # Force PIL to fully load image data into memory
            return img.size
        except Exception:
            return None, None

    def detect_faces(self, image_file):
        """
        Detect faces in image for smart cropping
        This is a placeholder - would need face detection library like opencv

        Returns:
            List of face coordinates
        """
        # Placeholder for face detection
        # In production, use opencv-python or similar
        return []

    def calculate_focal_point(self, image_file):
        """
        Calculate the focal point of an image for smart cropping

        Returns:
            Tuple of (x, y) coordinates (0-1 range)
        """
        try:
            img = Image.open(image_file)
            img.load()  # Force PIL to fully load image data into memory

            # For now, use center point
            # Can be enhanced with face detection or saliency detection
            focal_x = 0.5
            focal_y = 0.5

            # Try to detect faces
            faces = self.detect_faces(image_file)
            if faces:
                # Use center of first face as focal point
                face = faces[0]
                focal_x = (face["x"] + face["width"] / 2) / img.width
                focal_y = (face["y"] + face["height"] / 2) / img.height

            return focal_x, focal_y

        except Exception as e:
            logger.error(f"Error calculating focal point: {e}")
            return 0.5, 0.5


def generate_avif_variants(asset, processor=None, force=False):
    """Generate AVIF renditions for a MediaAsset and all of its thumbnails.

    AVIF is the primary next-gen rendition, served ahead of WebP in a
    <picture> element. This mirrors the existing WebP files: a full-size
    ``avif_file`` on the asset plus one ``avif_file`` per MediaThumbnail.
    Thumbnails are re-encoded from their already-cropped ``file`` so the crop
    geometry never has to be reproduced here.

    Idempotent: existing AVIF files are skipped unless ``force`` is True.
    Non-images (video, 3D, SVG) are skipped. Safe to run inside a Celery task
    or a management command. Returns the number of AVIF files written.
    """
    if processor is None:
        processor = ImageProcessor()

    written = 0

    if not asset.is_image() or asset.mime_type == "image/svg+xml":
        return written

    # Full-size AVIF from the original (flattened to match the WebP sibling).
    if asset.original_file and (force or not asset.avif_file):
        try:
            asset.original_file.seek(0)
            content = processor.convert_to_avif(asset.original_file)
            if content:
                asset.avif_file.save(f"{asset.id}.avif", content, save=True)
                written += 1
        except Exception as e:
            logger.warning(f"Failed to generate AVIF for asset {asset.id}: {e}")

    # Per-preset AVIF from each already-cropped thumbnail file. preserve
    # transparency so padded/transparent thumbnails (PNG) keep their alpha,
    # matching how the WebP thumbnail was produced.
    for thumb in asset.thumbnails.all():
        if (thumb.avif_file and not force) or not thumb.file:
            continue
        try:
            thumb.file.seek(0)
            content = processor.convert_to_avif(thumb.file, preserve_transparency=True)
            if content:
                thumb.avif_file.save(f"{asset.id}_{thumb.size_preset}.avif", content, save=True)
                written += 1
        except Exception as e:
            logger.warning(
                f"Failed to generate AVIF thumbnail {thumb.size_preset} for asset {asset.id}: {e}"
            )

    return written


def queue_avif_generation(asset):
    """Queue async AVIF generation for an image asset if enabled.

    No-op for non-images or when AUTO_AVIF is disabled. Enqueue failures are
    swallowed so they never break the upload response — the storefront falls
    back to WebP until AVIF exists.
    """
    try:
        if not asset.is_image():
            return
        if not getattr(settings, "MEDIA_LIBRARY_SETTINGS", {}).get("AUTO_AVIF", True):
            return
        from core.tasks import generate_avif_for_asset

        generate_avif_for_asset.delay(str(asset.id))
    except Exception as e:
        logger.warning(f"Could not queue AVIF generation for {getattr(asset, 'id', '?')}: {e}")


def generate_thumbnails_for_asset(asset, *, processor=None, force=False):
    """Generate thumbnails for every active ImageSizePreset on an asset.

    Single source of truth for rendition sizes — driven by the ImageSizePreset
    table (system presets: thumbnail 150, small 300, medium 600, large 1200, …)
    — so every upload path produces the same, consistently-named renditions.
    Without this, callers that hardcode their own size map drift out of sync with
    the storefront and each other.

    Existing presets are skipped unless ``force`` (then all are regenerated).
    Returns the number of thumbnails written.
    """
    from media_library.models import ImageSizePreset, MediaThumbnail

    if not asset.original_file:
        return 0

    processor = processor or ImageProcessor()

    if force:
        asset.thumbnails.all().delete()

    written = 0
    for preset in ImageSizePreset.objects.filter(is_active=True):
        if not force and asset.thumbnails.filter(size_preset=preset.slug).exists():
            continue
        try:
            asset.original_file.seek(0)
            original_content, webp_content = processor.generate_thumbnail(
                asset.original_file,
                preset.width,
                preset.height,
                crop_mode=preset.crop_mode,
                padding_color=getattr(preset, "padding_color", None),
            )
            if not original_content:
                continue

            # Replace any stale rendition for this preset.
            MediaThumbnail.objects.filter(media_asset=asset, size_preset=preset.slug).delete()

            ext = (
                "png"
                if preset.crop_mode == "pad"
                and getattr(preset, "padding_color", "transparent") == "transparent"
                else "jpg"
            )
            thumbnail = MediaThumbnail.objects.create(
                media_asset=asset,
                size_preset=preset.slug,
                width=preset.width,
                height=preset.height,
            )
            thumbnail.file.save(f"{asset.id}_{preset.slug}.{ext}", original_content, save=False)
            if webp_content:
                thumbnail.webp_file.save(f"{asset.id}_{preset.slug}.webp", webp_content, save=False)
            thumbnail.save()
            written += 1
        except Exception as e:
            # Resilient: one failed preset shouldn't cost the others or the
            # upload. Callers needing strictness can compare `written` to the
            # active-preset count.
            logger.error(f"Error generating {preset.slug} thumbnail for asset {asset.id}: {e}")
            continue
    return written
