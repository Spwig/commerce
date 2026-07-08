import os
import io
import hashlib
from PIL import Image, ImageOps, ExifTags
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class ImageProcessor:
    """Service for processing images - conversion, optimization, and thumbnail generation"""
    
    def __init__(self):
        self.webp_quality = getattr(settings, 'MEDIA_LIBRARY_SETTINGS', {}).get('WEBP_QUALITY', 85)
        self.thumbnail_sizes = getattr(settings, 'MEDIA_LIBRARY_SETTINGS', {}).get('THUMBNAIL_SIZES', {})
    
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

            has_transparency = img.mode in ('RGBA', 'LA', 'P')

            if has_transparency and preserve_transparency:
                # Preserve transparency - convert to RGBA if needed
                if img.mode == 'P':
                    img = img.convert('RGBA')
                elif img.mode == 'LA':
                    img = img.convert('RGBA')
                # WebP supports RGBA transparency natively
            elif has_transparency:
                # Flatten to RGB with white background (original behavior)
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode not in ('RGB', 'L'):
                img = img.convert('RGB')

            # Save as WebP
            output = io.BytesIO()
            img.save(output, format='WEBP', quality=quality or self.webp_quality, method=6)
            output.seek(0)

            return ContentFile(output.read())

        except Exception as e:
            logger.error(f"Error converting image to WebP: {e}")
            return None
    
    def _parse_padding_color(self, padding_color):
        """
        Parse padding color string to a color tuple.

        Args:
            padding_color: 'transparent', 'white', 'black', or '#RRGGBB' hex color

        Returns:
            Tuple (color, is_transparent) where color is RGB/RGBA tuple
        """
        if padding_color == 'transparent' or padding_color is None:
            return (0, 0, 0, 0), True  # Transparent (RGBA with alpha=0)
        elif padding_color == 'white':
            return (255, 255, 255), False
        elif padding_color == 'black':
            return (0, 0, 0), False
        elif padding_color.startswith('#') and len(padding_color) == 7:
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

    def generate_thumbnail(self, image_file, width, height, crop_mode='cover', padding_color=None):
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
            if crop_mode == 'contain':
                # Fit image within bounds maintaining aspect ratio
                img.thumbnail((width, height), Image.Resampling.LANCZOS)
            elif crop_mode == 'cover':
                # Fill the dimensions, cropping if necessary
                img = ImageOps.fit(img, (width, height), Image.Resampling.LANCZOS)
            elif crop_mode == 'crop':
                # Simple center crop to exact dimensions
                img = ImageOps.fit(img, (width, height), Image.Resampling.LANCZOS)
            elif crop_mode == 'pad':
                # Fit image within bounds and pad to exact dimensions
                color, is_transparent = self._parse_padding_color(padding_color)
                preserve_transparency = is_transparent

                if is_transparent:
                    # For transparent padding, ensure image is in RGBA mode
                    if img.mode != 'RGBA':
                        img = img.convert('RGBA')
                    # Use ImageOps.pad with transparent color
                    img = ImageOps.pad(img, (width, height), Image.Resampling.LANCZOS, color=(0, 0, 0, 0))
                else:
                    # For solid color padding
                    img = ImageOps.pad(img, (width, height), Image.Resampling.LANCZOS, color=color)
            elif crop_mode == 'smart':
                # Smart crop focusing on important areas (simplified version)
                img = self.smart_crop(img, width, height)

            # Determine output format - use PNG for transparent images, JPEG otherwise
            original_format = img.format
            if preserve_transparency or (img.mode == 'RGBA' and crop_mode == 'pad'):
                format = 'PNG'  # Use PNG to preserve transparency in original
            else:
                format = original_format or 'JPEG'

            # Save original format thumbnail
            output = io.BytesIO()

            # Convert RGBA to RGB for JPEG format
            save_img = img
            if format == 'JPEG' and img.mode in ('RGBA', 'LA', 'P'):
                # Create white background for transparent images
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                if img.mode == 'RGBA':
                    background.paste(img, mask=img.split()[-1])
                else:
                    background.paste(img)
                save_img = background
            elif format == 'JPEG' and img.mode not in ('RGB', 'L'):
                save_img = img.convert('RGB')

            if format == 'JPEG':
                save_img.save(output, format=format, quality=90, optimize=True)
            elif format == 'PNG':
                save_img.save(output, format='PNG', optimize=True)
            else:
                save_img.save(output, format=format)
            output.seek(0)
            original_content = ContentFile(output.read())

            # Save WebP version (WebP supports transparency natively)
            webp_output = io.BytesIO()
            webp_img = img

            if preserve_transparency and webp_img.mode == 'RGBA':
                # Preserve transparency in WebP
                pass  # Keep as RGBA
            elif webp_img.mode in ('RGBA', 'LA', 'P'):
                # Flatten transparency with white background
                background = Image.new('RGB', webp_img.size, (255, 255, 255))
                if webp_img.mode == 'P':
                    webp_img = webp_img.convert('RGBA')
                background.paste(webp_img, mask=webp_img.split()[-1] if webp_img.mode == 'RGBA' else None)
                webp_img = background
            elif webp_img.mode not in ('RGB', 'L'):
                webp_img = webp_img.convert('RGB')

            webp_img.save(webp_output, format='WEBP', quality=self.webp_quality, method=6)
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
            return value.replace('\x00', '').replace('\u0000', '')
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
            'exif': {},
            'size': None,
            'format': None,
            'mode': None,
        }

        try:
            img = Image.open(image_file)
            img.load()  # Force PIL to fully load image data into memory

            # Basic metadata
            metadata['size'] = img.size
            metadata['format'] = img.format
            metadata['mode'] = img.mode

            # EXIF data
            exifdata = img.getexif()
            if exifdata:
                for tag_id, value in exifdata.items():
                    tag = ExifTags.TAGS.get(tag_id, tag_id)

                    # Convert to JSON-serializable types
                    if isinstance(value, bytes):
                        try:
                            # Try UTF-16 first (common for Windows XP tags like XPTitle)
                            value = value.decode('utf-16-le').rstrip('\x00')
                        except:
                            try:
                                value = value.decode('utf-8')
                            except:
                                value = str(value)
                    elif hasattr(value, '__class__') and value.__class__.__name__ == 'IFDRational':
                        # Convert IFDRational to float
                        value = float(value)
                    elif isinstance(value, (list, tuple)):
                        # Handle lists/tuples that might contain IFDRational
                        converted = []
                        for v in value:
                            if hasattr(v, '__class__') and v.__class__.__name__ == 'IFDRational':
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

                    metadata['exif'][tag] = value
            
            # Calculate file hash for duplicate detection
            image_file.seek(0)
            metadata['hash'] = hashlib.md5(image_file.read()).hexdigest()
            image_file.seek(0)
            
        except Exception as e:
            logger.error(f"Error extracting metadata: {e}")
        
        return metadata
    
    def fix_orientation(self, img):
        """
        Fix image orientation based on EXIF data
        """
        try:
            # Get EXIF data
            exif = img.getexif()
            if exif:
                orientation_key = None
                for key in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[key] == 'Orientation':
                        orientation_key = key
                        break
                
                if orientation_key and orientation_key in exif:
                    orientation = exif[orientation_key]
                    
                    # Rotate based on orientation
                    if orientation == 3:
                        img = img.rotate(180, expand=True)
                    elif orientation == 6:
                        img = img.rotate(270, expand=True)
                    elif orientation == 8:
                        img = img.rotate(90, expand=True)
        except:
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
            format = img.format or 'JPEG'
            
            if format == 'JPEG':
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                img.save(output, format='JPEG', quality=85, optimize=True, progressive=True)
            elif format == 'PNG':
                img.save(output, format='PNG', optimize=True)
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
        except:
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
                focal_x = (face['x'] + face['width'] / 2) / img.width
                focal_y = (face['y'] + face['height'] / 2) / img.height
            
            return focal_x, focal_y
            
        except Exception as e:
            logger.error(f"Error calculating focal point: {e}")
            return 0.5, 0.5