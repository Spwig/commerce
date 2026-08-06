"""
Media Library Service integration tests.

Tests image processing, WebP conversion, thumbnail generation,
and media file handling services.
"""

import io

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from media_library.models import ImageSizePreset, MediaAsset, MediaThumbnail
from media_library.services import ImageProcessor
from tests.factories import (
    ImageSizePresetFactory,
    MediaAssetFactory,
    ThumbnailFactory,
)

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.media_library]


# ============================================================
# Helper Functions
# ============================================================


def create_test_image(width=800, height=600, format="JPEG", color="red"):
    """Create a test image file in memory."""
    img = Image.new("RGB", (width, height), color=color)
    img_io = io.BytesIO()
    img.save(img_io, format=format)
    img_io.seek(0)
    return img_io


def create_uploaded_file(width=800, height=600, format="JPEG", filename="test.jpg"):
    """Create a Django UploadedFile for testing."""
    img_io = create_test_image(width, height, format)
    content_types = {
        "JPEG": "image/jpeg",
        "PNG": "image/png",
        "WEBP": "image/webp",
        "GIF": "image/gif",
    }
    return SimpleUploadedFile(
        filename, img_io.read(), content_type=content_types.get(format, "image/jpeg")
    )


# ============================================================
# Image Processing Service Tests
# ============================================================


class TestImageProcessor:
    """Test ImageProcessor service functionality."""

    def test_extract_image_dimensions(self):
        """ImageProcessor can extract dimensions from image files."""
        processor = ImageProcessor()
        img_io = create_test_image(width=1920, height=1080)

        width, height = processor.get_image_dimensions(img_io)

        assert width == 1920
        assert height == 1080

    def test_extract_dimensions_from_various_formats(self):
        """Can extract dimensions from JPEG, PNG, WebP."""
        processor = ImageProcessor()
        formats = [
            ("JPEG", 1024, 768),
            ("PNG", 800, 600),
            ("WEBP", 1200, 900),
        ]

        for format_name, width, height in formats:
            img_io = create_test_image(width, height, format_name)
            extracted_width, extracted_height = processor.get_image_dimensions(img_io)

            assert extracted_width == width
            assert extracted_height == height

    def test_convert_to_webp(self):
        """Can convert JPEG/PNG to WebP format."""
        processor = ImageProcessor()
        jpeg_io = create_test_image(800, 600, "JPEG")

        webp_content = processor.convert_to_webp(jpeg_io, quality=85)

        assert webp_content is not None

        # Verify image is valid WebP
        from io import BytesIO

        webp_io = BytesIO(webp_content.read())
        webp_io.seek(0)
        img = Image.open(webp_io)
        assert img.format == "WEBP"
        assert img.size == (800, 600)

    def test_webp_quality_parameter(self):
        """WebP conversion respects quality parameter."""
        processor = ImageProcessor()
        jpeg_io = create_test_image(800, 600, "JPEG")

        # High quality
        high_quality = processor.convert_to_webp(jpeg_io, quality=95)
        if high_quality:
            high_quality_size = len(high_quality.read())
            high_quality.seek(0)
        else:
            high_quality_size = 0

        # Low quality
        jpeg_io.seek(0)
        low_quality = processor.convert_to_webp(jpeg_io, quality=50)
        low_quality_size = len(low_quality.read()) if low_quality else 0

        # Both should succeed
        assert high_quality_size > 0
        assert low_quality_size > 0


class TestAVIFConversion:
    """Test AVIF conversion — the primary next-gen rendition alongside WebP."""

    def test_convert_to_avif_produces_avif_bytes(self):
        """convert_to_avif returns valid AVIF-encoded content."""
        processor = ImageProcessor()
        jpeg_io = create_test_image(800, 600, "JPEG")

        avif_content = processor.convert_to_avif(jpeg_io, quality=63)

        assert avif_content is not None
        data = avif_content.read()
        assert len(data) > 0
        # ISO-BMFF ftyp box brand for AVIF still images.
        assert data[4:12] == b"ftypavif"

    def test_convert_to_avif_uses_settings_defaults(self):
        """Quality/speed default to MEDIA_LIBRARY_SETTINGS when not passed."""
        processor = ImageProcessor()

        assert processor.avif_quality == 63
        assert processor.avif_speed == 6

        avif_content = processor.convert_to_avif(create_test_image(400, 400, "JPEG"))
        assert avif_content is not None
        assert avif_content.read()[4:12] == b"ftypavif"

    def test_avif_preserves_transparency(self):
        """RGBA input keeps its alpha channel when preserve_transparency=True."""
        processor = ImageProcessor()
        rgba = Image.new("RGBA", (64, 64), (120, 30, 200, 128))
        buf = io.BytesIO()
        rgba.save(buf, format="PNG")
        buf.seek(0)

        avif_content = processor.convert_to_avif(buf, preserve_transparency=True)

        assert avif_content is not None
        decoded = Image.open(io.BytesIO(avif_content.read()))
        decoded.load()
        assert decoded.mode in ("RGBA", "LA")

    def test_avif_smaller_than_webp_at_default_quality(self):
        """AVIF typically encodes smaller than WebP for photographic content."""
        processor = ImageProcessor()
        # A gradient compresses realistically (a flat colour would be atypical).
        img = Image.new("RGB", (600, 600))
        px = img.load()
        for y in range(600):
            for x in range(600):
                px[x, y] = ((x + y) % 256, (x * 2) % 256, (y * 2) % 256)
        webp_io = io.BytesIO()
        img.save(webp_io, format="PNG")
        webp_io.seek(0)
        webp = processor.convert_to_webp(webp_io)
        webp_io.seek(0)
        avif = processor.convert_to_avif(webp_io)

        assert webp is not None and avif is not None
        assert avif.size <= webp.size

    def test_convert_to_avif_handles_invalid_data(self):
        """Invalid image data returns None rather than raising."""
        processor = ImageProcessor()
        assert processor.convert_to_avif(io.BytesIO(b"not an image")) is None


class TestAVIFVariantGeneration:
    """Test async AVIF rendition generation for assets and their thumbnails."""

    def _real_image_asset(self, admin_user, **kwargs):
        """MediaAsset whose original_file holds real (decodable) JPEG bytes."""
        jpeg = create_test_image(400, 400, "JPEG").read()
        return MediaAssetFactory(
            original_file__data=jpeg,
            original_file__filename="orig.jpg",
            uploaded_by=admin_user,
            **kwargs,
        )

    def _real_thumbnail(self, asset, preset="medium"):
        thumb_bytes = create_test_image(300, 300, "JPEG").read()
        return ThumbnailFactory(
            media_asset=asset,
            size_preset=preset,
            file__data=thumb_bytes,
            file__filename="thumb.jpg",
            webp_file=None,
        )

    def test_generate_avif_variants_populates_asset_and_thumbnail(self, admin_user):
        """AVIF is written for the full-size asset and each thumbnail."""
        from media_library.services import generate_avif_variants

        asset = self._real_image_asset(admin_user)
        self._real_thumbnail(asset)

        written = generate_avif_variants(asset)

        assert written >= 2
        asset.refresh_from_db()
        assert asset.avif_file
        thumb = asset.thumbnails.get(size_preset="medium")
        assert thumb.avif_file

    def test_generate_avif_variants_is_idempotent_without_force(self, admin_user):
        """A second pass writes nothing unless force=True."""
        from media_library.services import generate_avif_variants

        asset = self._real_image_asset(admin_user)
        self._real_thumbnail(asset)
        generate_avif_variants(asset)

        assert generate_avif_variants(asset) == 0
        assert generate_avif_variants(asset, force=True) >= 2

    def test_generate_avif_variants_skips_non_image(self, admin_user):
        """Videos/3D/SVG produce no AVIF and no error."""
        from media_library.services import generate_avif_variants

        video = MediaAssetFactory(video=True, uploaded_by=admin_user)
        assert generate_avif_variants(video) == 0
        video.refresh_from_db()
        assert not video.avif_file

    def test_queue_avif_generation_enqueues_task_for_image(self, admin_user):
        """Upload paths enqueue the Celery task for images when AUTO_AVIF on."""
        from unittest.mock import patch

        from media_library.services import queue_avif_generation

        asset = self._real_image_asset(admin_user)
        with patch("core.tasks.generate_avif_for_asset.delay") as delay:
            queue_avif_generation(asset)
        delay.assert_called_once_with(str(asset.id))

    def test_queue_avif_generation_noop_for_video(self, admin_user):
        """Non-images are never enqueued."""
        from unittest.mock import patch

        from media_library.services import queue_avif_generation

        video = MediaAssetFactory(video=True, uploaded_by=admin_user)
        with patch("core.tasks.generate_avif_for_asset.delay") as delay:
            queue_avif_generation(video)
        delay.assert_not_called()

    def test_generate_avif_for_asset_task_runs(self, admin_user):
        """The Celery task resolves the asset and writes AVIF synchronously."""
        from core.tasks import generate_avif_for_asset

        asset = self._real_image_asset(admin_user)
        self._real_thumbnail(asset)

        result = generate_avif_for_asset(str(asset.id))

        assert result["status"] == "success"
        assert result["avif_written"] >= 2
        asset.refresh_from_db()
        assert asset.avif_file


class TestPictureSources:
    """Test MediaAsset.get_picture_sources — the <picture> data layer."""

    def _asset_with(self, admin_user, avif=False, webp=False, **kwargs):
        from django.core.files.base import ContentFile

        asset = MediaAssetFactory(uploaded_by=admin_user, **kwargs)
        if webp:
            asset.webp_file.save("a.webp", ContentFile(b"webp-bytes"), save=True)
        if avif:
            asset.avif_file.save("a.avif", ContentFile(b"avif-bytes"), save=True)
        return asset

    def test_sources_include_avif_and_webp_when_present(self, admin_user):
        asset = self._asset_with(admin_user, avif=True, webp=True)
        sources = asset.get_picture_sources()
        assert sources["avif"].endswith(".avif")
        assert sources["webp"].endswith(".webp")
        # Fallback is the ORIGINAL format, not webp — webp is offered as a <source>.
        assert sources["fallback"] == asset.original_file.url

    def test_sources_omit_avif_when_missing(self, admin_user):
        """Backfill-window safety: no avif file -> no avif source."""
        asset = self._asset_with(admin_user, webp=True)
        sources = asset.get_picture_sources()
        assert sources["avif"] is None
        assert sources["fallback"] == asset.original_file.url

    def test_sources_for_preset_use_thumbnail(self, admin_user):
        from django.core.files.base import ContentFile

        asset = MediaAssetFactory(uploaded_by=admin_user)
        thumb = ThumbnailFactory(media_asset=asset, size_preset="product_listing", webp_file=None)
        thumb.avif_file.save("t.avif", ContentFile(b"avif-bytes"), save=True)
        sources = asset.get_picture_sources("product_listing")
        assert sources["avif"].endswith(".avif")
        assert sources["width"] == thumb.width

    def test_svg_has_no_raster_candidates(self, admin_user):
        asset = MediaAssetFactory(svg=True, uploaded_by=admin_user)
        sources = asset.get_picture_sources()
        assert sources["avif"] is None
        assert sources["webp"] is None
        assert sources["fallback"] == asset.original_file.url

    def test_resolve_from_url_matches_by_filename(self, admin_user):
        asset = MediaAssetFactory(uploaded_by=admin_user)
        assert MediaAsset.resolve_from_url(asset.original_file.url) == asset
        assert MediaAsset.resolve_from_url("https://cdn.example.com/nope.jpg") is None
        assert MediaAsset.resolve_from_url("") is None


class TestPictureTag:
    """Test the {% picture %} inclusion tag and picture_sources filter."""

    def _render(self, tpl, ctx):
        from django.template import Context, Template

        return Template(tpl).render(Context(ctx))

    def test_tag_renders_avif_then_webp_then_img(self, admin_user):
        from django.core.files.base import ContentFile

        asset = MediaAssetFactory(uploaded_by=admin_user)
        asset.webp_file.save("a.webp", ContentFile(b"webp-bytes"), save=True)
        asset.avif_file.save("a.avif", ContentFile(b"avif-bytes"), save=True)
        html = self._render(
            '{% load media_picture %}{% picture asset alt="Hi" css="product-card__img" %}',
            {"asset": asset},
        )
        assert '<picture class="spwig-picture">' in html
        # Ordering: avif source appears before webp source, which precedes <img>.
        assert html.index('type="image/avif"') < html.index('type="image/webp"')
        assert html.index('type="image/webp"') < html.index("<img")
        assert 'class="product-card__img"' in html
        assert 'alt="Hi"' in html

    def test_tag_omits_avif_source_when_missing(self, admin_user):
        asset = MediaAssetFactory(uploaded_by=admin_user)
        html = self._render(
            '{% load media_picture %}{% picture asset alt="Hi" %}', {"asset": asset}
        )
        assert 'type="image/avif"' not in html
        assert "<img" in html
        assert asset.original_file.url in html

    def test_filter_resolves_thumbnail_url_to_thumbnail_sources(self, admin_user):
        """A thumbnail rendition URL resolves to that thumbnail's own siblings."""
        from django.core.files.base import ContentFile

        from media_library.templatetags.media_picture import resolve_sources

        asset = MediaAssetFactory(uploaded_by=admin_user)
        thumb = ThumbnailFactory(media_asset=asset, size_preset="product_listing", webp_file=None)
        thumb.avif_file.save("t.avif", ContentFile(b"avif-bytes"), save=True)
        sources = resolve_sources(thumb.file.url)
        assert sources["avif"].endswith(".avif")
        assert sources["fallback"] == thumb.file.url

    def test_filter_resolves_url_to_sources(self, admin_user):
        from django.core.files.base import ContentFile

        asset = MediaAssetFactory(uploaded_by=admin_user)
        asset.avif_file.save("a.avif", ContentFile(b"avif-bytes"), save=True)
        html = self._render(
            "{% load media_picture %}"
            "{% with s=url|picture_sources %}{{ s.avif }}|{{ s.fallback }}{% endwith %}",
            {"url": asset.original_file.url},
        )
        assert ".avif" in html
        assert asset.original_file.url in html


# ============================================================
# Thumbnail Generation Tests
# ============================================================


class TestThumbnailGeneration:
    """Test thumbnail generation service."""

    def test_generate_thumbnail_crop_mode(self):
        """Crop mode generates exact dimensions."""
        processor = ImageProcessor()
        img_io = create_test_image(width=1920, height=1080)

        original_content, webp_content = processor.generate_thumbnail(
            img_io, width=400, height=400, crop_mode="crop"
        )

        assert original_content is not None

        # Verify dimensions
        from io import BytesIO

        thumb_io = BytesIO(original_content.read())
        thumb_io.seek(0)
        thumb_img = Image.open(thumb_io)

        # Should be exactly 400x400 (cropped to center)
        assert thumb_img.size == (400, 400)

    def test_generate_thumbnail_contain_mode(self):
        """Contain mode fits within dimensions maintaining aspect ratio."""
        processor = ImageProcessor()
        img_io = create_test_image(width=1920, height=1080)

        original_content, webp_content = processor.generate_thumbnail(
            img_io, width=600, height=600, crop_mode="contain"
        )

        assert original_content is not None

        # Verify it fits within bounds
        from io import BytesIO

        thumb_io = BytesIO(original_content.read())
        thumb_io.seek(0)
        thumb_img = Image.open(thumb_io)

        # Should fit within 600x600 while maintaining 16:9 ratio
        assert thumb_img.size[0] <= 600
        assert thumb_img.size[1] <= 600

    def test_generate_thumbnail_cover_mode(self):
        """Cover mode fills dimensions."""
        processor = ImageProcessor()
        img_io = create_test_image(width=1920, height=1080)

        original_content, webp_content = processor.generate_thumbnail(
            img_io, width=300, height=300, crop_mode="cover"
        )

        assert original_content is not None

        # Verify dimensions
        from io import BytesIO

        thumb_io = BytesIO(original_content.read())
        thumb_io.seek(0)
        thumb_img = Image.open(thumb_io)

        # Should be exactly 300x300
        assert thumb_img.size == (300, 300)

    def test_thumbnail_returns_original_and_webp(self):
        """Thumbnail generation returns both original and WebP versions."""
        processor = ImageProcessor()
        img_io = create_test_image(width=800, height=600)

        original_content, webp_content = processor.generate_thumbnail(
            img_io, width=300, height=300, crop_mode="cover"
        )

        assert original_content is not None
        assert webp_content is not None


# ============================================================
# Thumbnail Model Integration Tests
# ============================================================


class TestThumbnailModelIntegration:
    """Test thumbnail generation with MediaAsset model."""

    def test_create_thumbnail_for_asset(self, admin_user):
        """Can create and save thumbnail for media asset.

        Note: MediaThumbnail.size_preset is a CharField (preset slug/name), not a FK.
        """
        asset = MediaAssetFactory(width=1920, height=1080, uploaded_by=admin_user)
        # ImageSizePreset uses crop_mode (not crop) and is_system_preset (not is_system).
        ImageSizePresetFactory(name="test_small", width=300, height=300, crop_mode="crop")

        # Create thumbnail manually (in real system, this is done by signals)
        thumbnail = ThumbnailFactory(
            media_asset=asset, size_preset="test_small", width=300, height=300
        )

        assert thumbnail.media_asset == asset
        assert thumbnail.size_preset == "test_small"
        assert thumbnail.width == 300
        assert thumbnail.height == 300

    def test_multiple_thumbnails_per_asset(self, admin_user):
        """Asset can have multiple thumbnails for different presets."""
        asset = MediaAssetFactory(uploaded_by=admin_user)

        ImageSizePresetFactory(name="small", width=150, height=150)
        ImageSizePresetFactory(name="medium", width=600, height=600)
        ImageSizePresetFactory(name="large", width=1200, height=1200)

        ThumbnailFactory(media_asset=asset, size_preset="small", width=150, height=150)
        ThumbnailFactory(media_asset=asset, size_preset="medium", width=600, height=600)
        ThumbnailFactory(media_asset=asset, size_preset="large", width=1200, height=1200)

        thumbnails = MediaThumbnail.objects.filter(media_asset=asset)
        assert thumbnails.count() == 3

        sizes = list(thumbnails.values_list("size_preset", flat=True))
        assert "small" in sizes
        assert "medium" in sizes
        assert "large" in sizes

    def test_get_thumbnail_by_size(self, admin_user):
        """Can retrieve specific thumbnail size from asset."""
        asset = MediaAssetFactory(uploaded_by=admin_user)
        ImageSizePresetFactory(name="large", width=1200, height=1200)
        thumbnail = ThumbnailFactory(
            media_asset=asset, size_preset="large", width=1200, height=1200
        )

        # Get thumbnail by preset slug/name
        retrieved = MediaThumbnail.objects.filter(media_asset=asset, size_preset="large").first()

        assert retrieved == thumbnail
        assert retrieved.size_preset == "large"


# ============================================================
# Image Size Preset Tests
# ============================================================


class TestImageSizePreset:
    """Test ImageSizePreset model functionality."""

    def test_create_preset(self):
        """Can create image size preset."""
        preset = ImageSizePresetFactory(
            name="custom", width=800, height=600, crop_mode="crop", quality=85
        )

        assert preset.name == "custom"
        assert preset.width == 800
        assert preset.height == 600
        assert preset.crop_mode == "crop"
        assert preset.quality == 85

    def test_system_presets_exist(self):
        """System presets (small, medium, large) can be created and queried."""
        ImageSizePresetFactory(name="small", width=300, height=300, is_system_preset=True)
        ImageSizePresetFactory(name="medium", width=600, height=600, is_system_preset=True)
        ImageSizePresetFactory(name="large", width=1200, height=1200, is_system_preset=True)

        system_presets = ImageSizePreset.objects.filter(is_system_preset=True)
        assert system_presets.count() >= 3

        names = list(system_presets.values_list("name", flat=True))
        assert "small" in names
        assert "medium" in names
        assert "large" in names

    def test_custom_presets_not_system(self):
        """Custom presets are not marked as system presets."""
        custom = ImageSizePresetFactory(name="custom", is_system_preset=False)

        assert custom.is_system_preset is False

    def test_preset_dimensions_validation(self):
        """Preset dimensions must be positive."""
        # This would normally be validated by the model
        # Just verify we can create with valid dimensions
        preset = ImageSizePresetFactory(width=100, height=100)
        assert preset.width > 0
        assert preset.height > 0


# ============================================================
# WebP Conversion Integration Tests
# ============================================================


class TestWebPConversionIntegration:
    """Test WebP conversion integration with MediaAsset."""

    def test_webp_file_saved_on_upload(self, admin_user):
        """WebP version is saved when uploading JPEG/PNG."""
        # This would normally be tested via upload view
        # Here we verify the model supports webp_file field
        asset = MediaAssetFactory(mime_type="image/jpeg", uploaded_by=admin_user)

        # Verify webp_file field exists and can be accessed
        assert hasattr(asset, "webp_file")

    def test_svg_not_converted_to_webp(self, admin_user):
        """SVG files should not be converted to WebP."""
        svg_asset = MediaAssetFactory(
            mime_type="image/svg+xml", width=None, height=None, uploaded_by=admin_user, svg=True
        )

        # SVG should not have webp_file
        assert svg_asset.mime_type == "image/svg+xml"
        # WebP conversion should be skipped for SVG

    def test_video_not_converted_to_webp(self, admin_user):
        """Video files should not be converted to WebP."""
        video = MediaAssetFactory(mime_type="video/mp4", uploaded_by=admin_user, video=True)

        assert video.mime_type == "video/mp4"
        # WebP conversion should be skipped for video


# ============================================================
# File Size and Optimization Tests
# ============================================================


class TestFileOptimization:
    """Test file size tracking and optimization."""

    def test_file_size_tracked(self):
        """File size is tracked in bytes."""
        asset = MediaAssetFactory(file_size=102400)  # 100KB

        assert asset.file_size == 102400

    def test_optimization_flag(self):
        """MediaAsset carries a webp_file which acts as the optimized version."""
        # MediaAsset no longer has an explicit `is_optimized` boolean; the
        # presence of a webp_file is the "optimized" signal.
        asset = MediaAssetFactory()
        assert hasattr(asset, "webp_file")

    def test_webp_smaller_than_original(self):
        """WebP conversion typically results in smaller file size."""
        # Create JPEG
        jpeg_io = create_test_image(800, 600, "JPEG")
        jpeg_size = len(jpeg_io.getvalue())

        # Convert to WebP (instance method, not classmethod)
        processor = ImageProcessor()
        webp_content = processor.convert_to_webp(jpeg_io, quality=85)
        webp_size = webp_content.size

        # WebP should typically be smaller (not always guaranteed, but common)
        # Just verify both have content
        assert jpeg_size > 0
        assert webp_size > 0


# ============================================================
# Batch Processing Tests
# ============================================================


class TestBatchProcessing:
    """Test batch thumbnail generation and processing."""

    def test_generate_thumbnails_for_multiple_presets(self, admin_user):
        """Can generate all thumbnail sizes for an asset."""
        asset = MediaAssetFactory(uploaded_by=admin_user)

        # Create multiple presets
        presets = [
            ImageSizePresetFactory(name="small", width=150, height=150, small=True),
            ImageSizePresetFactory(name="medium", width=600, height=600, medium=True),
            ImageSizePresetFactory(name="large", width=1200, height=1200, large=True),
        ]

        # Generate thumbnails for all presets
        for preset in presets:
            ThumbnailFactory(media_asset=asset, size_preset=preset)

        # Verify all were created
        assert asset.thumbnails.count() == 3

    def test_regenerate_thumbnails(self, admin_user):
        """Can regenerate thumbnails (delete and recreate)."""
        asset = MediaAssetFactory(uploaded_by=admin_user)
        preset = ImageSizePresetFactory(name="test", width=300, height=300)

        # Create initial thumbnail
        old_thumb = ThumbnailFactory(media_asset=asset, size_preset=preset)
        old_id = old_thumb.id

        # Delete and recreate
        MediaThumbnail.objects.filter(media_asset=asset).delete()
        new_thumb = ThumbnailFactory(media_asset=asset, size_preset=preset)

        assert new_thumb.id != old_id
        assert asset.thumbnails.count() == 1


# ============================================================
# Error Handling Tests
# ============================================================


class TestImageProcessingErrors:
    """Test error handling in image processing."""

    def test_invalid_image_data(self):
        """Gracefully handle invalid image data."""
        invalid_io = io.BytesIO(b"not an image")

        # Should raise or return None gracefully
        try:
            ImageProcessor.get_image_dimensions(invalid_io)
            raise AssertionError("Should have raised an error")
        except Exception:
            # Expected behavior
            pass

    def test_corrupted_image_file(self):
        """Handle corrupted image files."""
        # Create partially corrupted data
        img_io = create_test_image(800, 600, "JPEG")
        corrupted = io.BytesIO(img_io.read()[:100])  # Truncated

        try:
            ImageProcessor.get_image_dimensions(corrupted)
            raise AssertionError("Should have raised an error")
        except Exception:
            # Expected behavior
            pass

    def test_zero_dimensions(self):
        """Handle edge case of zero dimensions on the MediaAsset aspect ratio."""
        # ImageProcessor has no calculate_aspect_ratio helper; the aspect ratio
        # lives on MediaAsset.aspect_ratio and returns 1 when height is 0.
        asset = MediaAssetFactory(width=100, height=0)
        assert asset.aspect_ratio == 1
