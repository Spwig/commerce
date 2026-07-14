"""
Server-side design rendering service using Pillow.

Generates composite images by overlaying design elements onto product mockup images.
Used for order fulfillment to produce print-ready files.
"""

import logging

from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)


class DesignRenderService:
    """Renders a design state into a composite image using Pillow."""

    @staticmethod
    def render_surface(surface, surface_data, output_dpi=300):
        """
        Render a single surface's design as a composite image.

        Args:
            surface: ProductSurface instance
            surface_data: Dict with 'canvas_json' and optionally 'canvas_width'/'canvas_height'
            output_dpi: Target DPI for the rendered output

        Returns:
            PIL.Image instance of the rendered composite
        """
        canvas_json = surface_data.get("canvas_json", surface_data)
        objects = canvas_json.get("objects", [])
        if not objects:
            return None

        # Calculate output dimensions based on physical size and DPI
        if surface.dimension_unit == "mm":
            width_inches = float(surface.width) / 25.4
            height_inches = float(surface.height) / 25.4
        elif surface.dimension_unit == "in":
            width_inches = float(surface.width)
            height_inches = float(surface.height)
        else:  # px
            width_inches = float(surface.width) / 96  # assume 96 PPI screen
            height_inches = float(surface.height) / 96

        output_width = int(width_inches * output_dpi)
        output_height = int(height_inches * output_dpi)

        # Determine source canvas dimensions for coordinate scaling.
        # These are the pixel dimensions of the Fabric.js canvas the user designed on.
        source_width = surface_data.get("canvas_width") or canvas_json.get("width")
        source_height = surface_data.get("canvas_height") or canvas_json.get("height")

        # Fallback: compute from surface physical dimensions at 96 PPI
        if not source_width:
            source_width = (
                float(surface.width) / 25.4 * 96
                if surface.dimension_unit == "mm"
                else float(surface.width) * 96
                if surface.dimension_unit == "in"
                else float(surface.width)
            )
        if not source_height:
            source_height = (
                float(surface.height) / 25.4 * 96
                if surface.dimension_unit == "mm"
                else float(surface.height) * 96
                if surface.dimension_unit == "in"
                else float(surface.height)
            )

        source_width = float(source_width)
        source_height = float(source_height)

        scale_x = output_width / source_width if source_width > 0 else 1
        scale_y = output_height / source_height if source_height > 0 else 1

        # Create canvas
        canvas = Image.new("RGBA", (output_width, output_height), surface.background_color)

        for obj in objects:
            try:
                obj_type = obj.get("type", "")
                if obj_type in ("i-text", "textbox", "text"):
                    DesignRenderService._render_text(canvas, obj, scale_x, scale_y)
                elif obj_type == "image":
                    DesignRenderService._render_image(canvas, obj, scale_x, scale_y)
            except Exception as e:
                logger.warning(f"Failed to render object {obj.get('type')}: {e}")

        return canvas

    @staticmethod
    def _render_text(canvas, obj, scale_x, scale_y):
        """Render a text element onto the canvas."""
        draw = ImageDraw.Draw(canvas)

        text = obj.get("text", "")
        if not text:
            return

        font_size = int(obj.get("fontSize", 24) * scale_x)

        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
        except OSError:
            font = ImageFont.load_default()

        fill = obj.get("fill", "#000000")
        x = int(obj.get("left", 0) * scale_x)
        y = int(obj.get("top", 0) * scale_y)

        draw.text((x, y), text, fill=fill, font=font)

    @staticmethod
    def _render_image(canvas, obj, scale_x, scale_y):
        """Render an image element onto the canvas."""
        src = obj.get("src", "")
        if not src:
            return

        import os

        from django.conf import settings

        # Convert URL to file path
        if src.startswith("/media/"):
            file_path = os.path.join(settings.MEDIA_ROOT, src[7:])
        else:
            logger.warning(f"Cannot render image with src: {src}")
            return

        if not os.path.exists(file_path):
            logger.warning(f"Image file not found: {file_path}")
            return

        try:
            img = Image.open(file_path).convert("RGBA")

            # Apply Fabric.js object scaling
            obj_scale_x = float(obj.get("scaleX", 1.0))
            obj_scale_y = float(obj.get("scaleY", 1.0))
            new_width = int(img.width * obj_scale_x * scale_x)
            new_height = int(img.height * obj_scale_y * scale_y)

            if new_width > 0 and new_height > 0:
                img = img.resize((new_width, new_height), Image.LANCZOS)

            # Apply opacity
            opacity = float(obj.get("opacity", 1.0))
            if opacity < 1.0:
                alpha = img.split()[3]
                alpha = alpha.point(lambda p: int(p * opacity))
                img.putalpha(alpha)

            x = int(obj.get("left", 0) * scale_x)
            y = int(obj.get("top", 0) * scale_y)

            canvas.paste(img, (x, y), img)
        except Exception as e:
            logger.warning(f"Failed to render image: {e}")
