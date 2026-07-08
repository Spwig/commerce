"""
Splash Screen Service for POS Terminal Readers.

Generates branded PNG splash screens for Stripe Terminal readers
with merchant logo and Spwig branding.
"""
import io
import logging
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)


class SplashScreenService:
    """Generate and upload splash screens for Stripe Terminal readers."""

    # Reader type to dimensions mapping (width, height)
    READER_SIZES = {
        'stripe_s700': (1080, 1920),
        'bbpos_wisepos_e': (720, 1280),
        'verifone_p400': (320, 480),
        'bbpos_wisepad_3': (320, 240),
    }

    # Readers that require grayscale/B&W images
    BW_READERS = {'verifone_p400', 'bbpos_wisepad_3'}

    # Gradient colors (subtle brand colors)
    GRADIENT_START = (45, 35, 65)      # Deep purple
    GRADIENT_END = (25, 45, 75)        # Deep blue

    # Spwig branding
    POWERED_BY_TEXT = "Powered by Spwig"

    def __init__(self):
        self._spwig_logo = None
        self._spwig_favicon_path = None

    @property
    def spwig_favicon_path(self):
        """Lazy-load Spwig favicon path."""
        if self._spwig_favicon_path is None:
            self._spwig_favicon_path = Path(settings.BASE_DIR) / 'core' / 'static' / 'core' / 'images' / 'favicon-256x256.png'
        return self._spwig_favicon_path

    @property
    def spwig_logo(self):
        """Lazy-load Spwig favicon."""
        if self._spwig_logo is None:
            try:
                self._spwig_logo = Image.open(self.spwig_favicon_path).convert('RGBA')
            except Exception as e:
                logger.warning(f"Could not load Spwig favicon: {e}")
                self._spwig_logo = False
        return self._spwig_logo if self._spwig_logo else None

    def get_reader_size(self, reader_type: str) -> tuple:
        """Get dimensions for a reader type."""
        # Normalize reader type (lowercase, strip whitespace)
        normalized = reader_type.lower().strip() if reader_type else ''
        return self.READER_SIZES.get(normalized, (720, 1280))  # Default to WisePOS E

    def is_bw_reader(self, reader_type: str) -> bool:
        """Check if reader requires B&W image."""
        normalized = reader_type.lower().strip() if reader_type else ''
        return normalized in self.BW_READERS

    def generate_gradient(self, width: int, height: int) -> Image.Image:
        """Generate a vertical gradient background."""
        gradient = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(gradient)

        for y in range(height):
            ratio = y / height
            r = int(self.GRADIENT_START[0] + (self.GRADIENT_END[0] - self.GRADIENT_START[0]) * ratio)
            g = int(self.GRADIENT_START[1] + (self.GRADIENT_END[1] - self.GRADIENT_START[1]) * ratio)
            b = int(self.GRADIENT_START[2] + (self.GRADIENT_END[2] - self.GRADIENT_START[2]) * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        return gradient

    def load_merchant_logo(self, logo_asset) -> Image.Image | None:
        """Load merchant logo from MediaAsset."""
        if not logo_asset:
            return None

        try:
            # Get the file path or URL
            if hasattr(logo_asset, 'original_file') and logo_asset.original_file:
                logo_path = logo_asset.original_file.path
                return Image.open(logo_path).convert('RGBA')
        except Exception as e:
            logger.warning(f"Could not load merchant logo: {e}")

        return None

    def resize_logo_to_fit(self, logo: Image.Image, max_width: int, max_height: int) -> Image.Image:
        """Resize logo to fit within bounds while preserving aspect ratio."""
        if logo.width <= max_width and logo.height <= max_height:
            return logo

        # Calculate scale factor
        scale = min(max_width / logo.width, max_height / logo.height)
        new_width = int(logo.width * scale)
        new_height = int(logo.height * scale)

        return logo.resize((new_width, new_height), Image.Resampling.LANCZOS)

    def get_font(self, size: int):
        """Get a font for text rendering."""
        # Try system fonts
        font_paths = [
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
            '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
            '/usr/share/fonts/TTF/DejaVuSans.ttf',
        ]
        for path in font_paths:
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
        # Fallback to default
        return ImageFont.load_default()

    def generate_splash_png(
        self,
        reader_type: str,
        logo_asset=None,
        custom_image=None
    ) -> bytes:
        """
        Generate a PNG splash screen for a reader.

        Args:
            reader_type: Type of reader (e.g., 'bbpos_wisepos_e')
            logo_asset: MediaAsset for merchant logo (optional)
            custom_image: Custom override image as bytes or PIL Image (optional)

        Returns:
            PNG image as bytes
        """
        width, height = self.get_reader_size(reader_type)
        is_bw = self.is_bw_reader(reader_type)

        # If custom image provided, resize and return
        if custom_image:
            return self._process_custom_image(custom_image, width, height, is_bw)

        # Generate background
        image = self.generate_gradient(width, height)

        # Load and overlay merchant logo
        merchant_logo = self.load_merchant_logo(logo_asset)
        if merchant_logo:
            # Logo should be max 1/3 of screen width
            max_logo_width = width // 3
            max_logo_height = height // 3
            logo_resized = self.resize_logo_to_fit(merchant_logo, max_logo_width, max_logo_height)

            # Center the logo
            logo_x = (width - logo_resized.width) // 2
            logo_y = (height - logo_resized.height) // 2 - int(height * 0.05)  # Slightly above center

            # Composite with alpha
            image = image.convert('RGBA')
            image.paste(logo_resized, (logo_x, logo_y), logo_resized)
            image = image.convert('RGB')

        # Add Spwig branding in bottom-right
        self._add_spwig_branding(image, width, height)

        # Convert to B&W if needed
        if is_bw:
            image = image.convert('L')

        # Save as PNG
        buffer = io.BytesIO()
        image.save(buffer, format='PNG', optimize=True)
        buffer.seek(0)
        return buffer.read()

    def _process_custom_image(
        self,
        custom_image,
        width: int,
        height: int,
        is_bw: bool
    ) -> bytes:
        """Process a custom override image."""
        if isinstance(custom_image, bytes):
            img = Image.open(io.BytesIO(custom_image))
        else:
            img = custom_image

        # Resize to fit reader dimensions (crop to fill)
        img = img.convert('RGB')
        img_ratio = img.width / img.height
        target_ratio = width / height

        if img_ratio > target_ratio:
            # Image is wider - crop sides
            new_width = int(img.height * target_ratio)
            left = (img.width - new_width) // 2
            img = img.crop((left, 0, left + new_width, img.height))
        else:
            # Image is taller - crop top/bottom
            new_height = int(img.width / target_ratio)
            top = (img.height - new_height) // 2
            img = img.crop((0, top, img.width, top + new_height))

        img = img.resize((width, height), Image.Resampling.LANCZOS)

        if is_bw:
            img = img.convert('L')

        buffer = io.BytesIO()
        img.save(buffer, format='PNG', optimize=True)
        buffer.seek(0)
        return buffer.read()

    def _add_spwig_branding(self, image: Image.Image, width: int, height: int):
        """Add Spwig favicon and 'Powered by Spwig' text to bottom-right."""
        draw = ImageDraw.Draw(image)

        # Calculate sizes based on image dimensions
        padding = int(width * 0.03)  # 3% padding
        icon_size = int(min(width, height) * 0.05)  # 5% of smaller dimension
        font_size = int(icon_size * 0.6)

        font = self.get_font(font_size)

        # Get text dimensions
        text_bbox = draw.textbbox((0, 0), self.POWERED_BY_TEXT, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # Position text (bottom-right corner)
        text_x = width - text_width - padding
        text_y = height - text_height - padding

        # Draw text with slight shadow for readability
        shadow_offset = max(1, font_size // 20)
        draw.text((text_x + shadow_offset, text_y + shadow_offset), self.POWERED_BY_TEXT, fill=(0, 0, 0), font=font)
        draw.text((text_x, text_y), self.POWERED_BY_TEXT, fill=(200, 200, 200), font=font)

        # Add Spwig logo to left of text
        if self.spwig_logo:
            logo = self.spwig_logo.copy()
            logo = logo.resize((icon_size, icon_size), Image.Resampling.LANCZOS)

            logo_x = text_x - icon_size - int(padding * 0.5)
            logo_y = text_y + (text_height - icon_size) // 2

            # Ensure position is valid
            if logo_x > 0 and logo_y > 0:
                image_rgba = image.convert('RGBA')
                image_rgba.paste(logo, (logo_x, logo_y), logo)
                image.paste(image_rgba.convert('RGB'))

    def update_reader_splash(self, reader, force: bool = False) -> dict:
        """
        Generate and upload splash screen for a reader.

        Args:
            reader: POSTerminalReader instance
            force: Force regeneration even if already generated

        Returns:
            dict with success status and details
        """
        from core.models import SiteSettings

        # Check if already generated and not forcing
        if not force and reader.splash_generated_at and not reader.splash_override_image:
            return {'success': True, 'skipped': True, 'reason': 'Already generated'}

        # Get logo source
        if reader.splash_override_image:
            logo_asset = reader.splash_override_image
            custom_image = None
            try:
                # Load the custom image directly
                custom_image = Image.open(reader.splash_override_image.original_file.path)
            except Exception as e:
                logger.error(f"Failed to load custom splash image: {e}")
                return {'success': False, 'error': str(e)}
        else:
            # Use site logo
            site_settings = SiteSettings.get_settings()
            logo_asset = site_settings.site_logo
            custom_image = None

        # Generate PNG
        try:
            png_bytes = self.generate_splash_png(
                reader_type=reader.reader_type,
                logo_asset=logo_asset if not custom_image else None,
                custom_image=custom_image
            )
        except Exception as e:
            logger.error(f"Failed to generate splash screen: {e}")
            return {'success': False, 'error': str(e)}

        # Upload to Stripe
        try:
            result = self._upload_to_stripe(reader, png_bytes)
        except Exception as e:
            logger.error(f"Failed to upload splash screen to Stripe: {e}")
            return {'success': False, 'error': str(e)}

        # Update reader record
        reader.stripe_splash_file_id = result.get('file_id', '')
        reader.stripe_splash_config_id = result.get('config_id', '')
        reader.splash_generated_at = timezone.now()
        reader.save(update_fields=[
            'stripe_splash_file_id',
            'stripe_splash_config_id',
            'splash_generated_at'
        ])

        logger.info(f"Splash screen updated for reader {reader.pk}: file={result.get('file_id')}")
        return {'success': True, **result}

    def _upload_to_stripe(self, reader, png_bytes: bytes) -> dict:
        """Upload PNG to Stripe and configure the reader."""
        provider_instance = reader.provider.get_provider_instance()

        if not provider_instance:
            raise ValueError("No provider instance available")

        if not hasattr(provider_instance, 'upload_splash_screen'):
            raise ValueError(f"Provider {reader.provider.provider_key} does not support splash screens")

        # Upload file
        file_id = provider_instance.upload_splash_screen(png_bytes)

        # Create configuration
        config_id = provider_instance.create_splash_configuration(file_id, reader.reader_type)

        # Assign to reader
        provider_instance.assign_configuration_to_reader(reader.provider_reader_id, config_id)

        return {
            'file_id': file_id,
            'config_id': config_id
        }


# Singleton instance
splash_screen_service = SplashScreenService()
