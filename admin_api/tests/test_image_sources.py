"""Behaviour tests for the mobile Admin API sized image sources.

Covers the width-keyed ``image_sources`` contract the merchant app uses to pick
the right-sized image per context, and the shared thumbnail generator that keeps
every upload path on the same system presets.
"""

import io

from django.core.files.base import ContentFile
from django.test import TestCase
from PIL import Image

from admin_api.serializers.image_sources import build_image_sources
from media_library.models import ImageSizePreset, MediaAsset, MediaThumbnail
from media_library.services import generate_thumbnails_for_asset


def _make_thumbnail(asset, preset, width, height=None):
    thumb = MediaThumbnail.objects.create(
        media_asset=asset, size_preset=preset, width=width, height=height or width
    )
    thumb.webp_file.save(f"{preset}.webp", ContentFile(b"webp-bytes"), save=True)
    return thumb


class BuildImageSourcesTests(TestCase):
    def setUp(self):
        self.asset = MediaAsset.objects.create(title="Test", mime_type="image/jpeg", file_size=8)
        self.asset.original_file.save("orig.jpg", ContentFile(b"original"), save=True)

    def test_sources_are_keyed_by_intrinsic_width_not_preset_name(self):
        # App-upload historically named 150/300/600 as small/medium/large.
        # Keying on width must still resolve them to thumbnail/small/medium.
        t150 = _make_thumbnail(self.asset, "small", 150)
        t300 = _make_thumbnail(self.asset, "medium", 300)
        t600 = _make_thumbnail(self.asset, "large", 600)

        sources = build_image_sources(self.asset)

        self.assertEqual(set(sources), {"thumbnail", "small", "medium"})
        self.assertEqual(sources["thumbnail"], t150.webp_file.url)
        self.assertEqual(sources["small"], t300.webp_file.url)
        self.assertEqual(sources["medium"], t600.webp_file.url)

    def test_list_context_omits_large_and_full(self):
        for preset, width in [("thumbnail", 150), ("small", 300), ("medium", 600), ("large", 1200)]:
            _make_thumbnail(self.asset, preset, width)

        sources = build_image_sources(self.asset, detail=False)

        self.assertNotIn("large", sources)
        self.assertNotIn("full", sources)

    def test_detail_context_includes_large_and_full(self):
        _make_thumbnail(self.asset, "thumbnail", 150)
        _make_thumbnail(self.asset, "large", 1200)

        sources = build_image_sources(self.asset, detail=True)

        self.assertIn("large", sources)
        self.assertIn("full", sources)  # falls back to the display URL

    def test_only_generated_sizes_are_returned(self):
        # No full-size image masquerading as a thumbnail: a missing size is
        # simply absent rather than resolving to the display URL.
        _make_thumbnail(self.asset, "thumbnail", 150)

        sources = build_image_sources(self.asset)

        self.assertEqual(set(sources), {"thumbnail"})

    def test_width_collision_prefers_standard_square_preset(self):
        # A wide banner and a square large both report width 1200 — the square
        # `large` must win so 'large' is never a letterboxed banner.
        _make_thumbnail(self.asset, "banner", 1200, height=400)
        large = _make_thumbnail(self.asset, "large", 1200, height=1200)

        sources = build_image_sources(self.asset, detail=True)

        self.assertEqual(sources["large"], large.webp_file.url)

    def test_none_asset_returns_none(self):
        self.assertIsNone(build_image_sources(None))

    def test_asset_without_renditions_returns_none(self):
        self.assertIsNone(build_image_sources(self.asset))


class GenerateThumbnailsForAssetTests(TestCase):
    """The shared generator drives sizes off ImageSizePreset for every caller."""

    def setUp(self):
        buf = io.BytesIO()
        Image.new("RGB", (900, 900), "red").save(buf, "JPEG")
        buf.seek(0)
        data = buf.read()
        self.asset = MediaAsset.objects.create(
            title="Real", mime_type="image/jpeg", file_size=len(data)
        )
        self.asset.original_file.save("real.jpg", ContentFile(data), save=True)

        ImageSizePreset.objects.get_or_create(
            slug="thumbnail",
            defaults={"name": "Thumbnail", "width": 150, "height": 150, "is_active": True},
        )
        ImageSizePreset.objects.get_or_create(
            slug="small",
            defaults={"name": "Small", "width": 300, "height": 300, "is_active": True},
        )

    def test_generates_a_rendition_per_active_preset(self):
        written = generate_thumbnails_for_asset(self.asset)

        self.assertEqual(written, 2)
        slugs = set(self.asset.thumbnails.values_list("size_preset", flat=True))
        self.assertEqual(slugs, {"thumbnail", "small"})
        self.assertEqual(self.asset.thumbnails.get(size_preset="thumbnail").width, 150)

    def test_existing_presets_are_skipped_without_force(self):
        generate_thumbnails_for_asset(self.asset)
        written_second = generate_thumbnails_for_asset(self.asset)

        self.assertEqual(written_second, 0)
        self.assertEqual(self.asset.thumbnails.count(), 2)


class SerializersExposeImageFieldsTests(TestCase):
    """Every image-bearing admin serializer surfaces the new fields."""

    def test_product_serializers_expose_image_sources(self):
        from admin_api.serializers.products import (
            AdminProductDetailSerializer,
            AdminProductImageSerializer,
            AdminProductListSerializer,
        )

        for serializer_cls in (
            AdminProductListSerializer,
            AdminProductDetailSerializer,
            AdminProductImageSerializer,
        ):
            self.assertIn("image_sources", serializer_cls().fields)

    def test_catalog_serializers_expose_image_sources(self):
        from admin_api.serializers.categories import (
            AdminCategoryDetailSerializer,
            AdminCategoryListSerializer,
        )
        from admin_api.serializers.orders import AdminOrderItemSerializer
        from admin_api.serializers.variants import AdminVariantListSerializer

        for serializer_cls in (
            AdminCategoryListSerializer,
            AdminCategoryDetailSerializer,
            AdminVariantListSerializer,
            AdminOrderItemSerializer,
        ):
            self.assertIn("image_sources", serializer_cls().fields)

    def test_brand_serializers_expose_logo(self):
        from admin_api.serializers.brands import (
            AdminBrandDetailSerializer,
            AdminBrandListSerializer,
        )

        self.assertIn("logo_url", AdminBrandListSerializer().fields)
        self.assertIn("logo_url", AdminBrandDetailSerializer().fields)
        self.assertIn("banner_url", AdminBrandDetailSerializer().fields)
