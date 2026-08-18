"""
P4: storefront catalog serializers expose an additive `image_sources`
<picture> source set alongside the existing single-URL image fields.

These assert both that the new field is present with the right shape AND
that the legacy string fields remain (back-compat for deployed clients).
"""

import pytest

from catalog.models import ProductImage
from catalog.serializers import (
    CategoryDetailSerializer,
    CategoryListSerializer,
    ProductImageSerializer,
    ProductListSerializer,
)
from media_library.models import MediaThumbnail
from tests.factories import CategoryFactory, MediaAssetFactory, ProductFactory

pytestmark = [pytest.mark.django_db, pytest.mark.unit]


def _product_with_image(admin_user):
    product = ProductFactory()
    asset = MediaAssetFactory(uploaded_by=admin_user, mime_type="image/jpeg")
    ProductImage.objects.create(
        product=product,
        media_asset=asset,
        is_primary=True,
        show_in_listing=True,
        show_in_gallery=True,
    )
    return product, asset


SOURCE_KEYS = {
    "avif",
    "webp",
    "fallback",
    "width",
    "height",
    "avif_srcset",
    "webp_srcset",
    "fallback_srcset",
}


class TestProductImageSources:
    def test_product_image_serializer_adds_sources_and_keeps_string(self, admin_user):
        product, asset = _product_with_image(admin_user)
        data = ProductImageSerializer(product.images.first()).data
        # Legacy string field retained
        assert "image" in data
        # New additive field with the full source-set shape
        assert set(data["image_sources"]) == SOURCE_KEYS
        assert data["image_sources"]["fallback"]

    def test_product_list_primary_and_images_carry_sources(self, admin_user):
        product, asset = _product_with_image(admin_user)
        data = ProductListSerializer(product).data
        assert set(data["primary_image"]) >= {"url", "image_sources", "alt_text"}
        img = data["images"][0]
        assert "image_url" in img and "thumbnail_url" in img  # back-compat
        assert set(img["image_sources"]) == SOURCE_KEYS
        assert set(img["thumbnail_sources"]) == SOURCE_KEYS

    def test_sources_omit_avif_when_not_generated(self, admin_user):
        """No AVIF file -> avif is null, so the client skips that <source>."""
        product, asset = _product_with_image(admin_user)
        data = ProductImageSerializer(product.images.first()).data
        assert data["image_sources"]["avif"] is None


class TestCategoryImageSources:
    def test_category_list_serializer_adds_sources(self, admin_user):
        asset = MediaAssetFactory(uploaded_by=admin_user)
        category = CategoryFactory(image_asset=asset)
        data = CategoryListSerializer(category).data
        assert "image" in data
        assert set(data["image_sources"]) == SOURCE_KEYS

    def test_category_detail_serializer_adds_image_and_banner_sources(self, admin_user):
        img = MediaAssetFactory(uploaded_by=admin_user)
        banner = MediaAssetFactory(uploaded_by=admin_user)
        category = CategoryFactory(image_asset=img, banner_asset=banner)
        data = CategoryDetailSerializer(category).data
        assert set(data["image_sources"]) == SOURCE_KEYS
        assert set(data["banner_image_sources"]) == SOURCE_KEYS

    def test_category_sources_null_when_no_asset(self, admin_user):
        category = CategoryFactory(image_asset=None)
        data = CategoryListSerializer(category).data
        assert data["image_sources"] is None


def _thumb(asset, preset, width, height, *, avif=True, webp=True):
    """Create a MediaThumbnail row with URL-resolvable file fields."""
    return MediaThumbnail.objects.create(
        media_asset=asset,
        size_preset=preset,
        width=width,
        height=height,
        file=f"thumb/{preset}.jpg",
        webp_file=f"thumb/{preset}.webp" if webp else None,
        avif_file=f"thumb/{preset}.avif" if avif else None,
    )


class TestSrcsetLadder:
    """The additive ``*_srcset`` width ladders built by get_picture_sources()."""

    def test_srcset_lists_same_aspect_widths_ascending(self, admin_user):
        # Full-size asset is 16:9 (factory default 1920x1080).
        asset = MediaAssetFactory(uploaded_by=admin_user, mime_type="image/jpeg")
        _thumb(asset, "small", 640, 360)
        _thumb(asset, "medium", 960, 540)
        _thumb(asset, "large", 1280, 720)

        sources = asset.get_picture_sources()

        # Every generated width appears with a correct ``Nw`` descriptor, in
        # ascending order, each pointing at that format's file.
        avif = sources["avif_srcset"]
        assert avif.count(",") == 2
        assert "small.avif 640w" in avif
        assert "medium.avif 960w" in avif
        assert "large.avif 1280w" in avif
        assert avif.index("640w") < avif.index("960w") < avif.index("1280w")

        webp = sources["webp_srcset"]
        assert "small.webp 640w" in webp and "large.webp 1280w" in webp

        # The full-size original (1920w) caps the fallback ladder.
        assert sources["fallback_srcset"].endswith("1920w")
        assert "640w" in sources["fallback_srcset"]

    def test_srcset_excludes_mismatched_aspect_renditions(self, admin_user):
        asset = MediaAssetFactory(uploaded_by=admin_user, mime_type="image/jpeg")
        _thumb(asset, "small", 640, 360)  # 16:9 — kept
        _thumb(asset, "medium", 960, 540)  # 16:9 — kept
        _thumb(asset, "avatar", 300, 300)  # 1:1 — square crop, must be excluded

        avif_srcset = asset.get_picture_sources()["avif_srcset"]

        assert "300w" not in avif_srcset
        assert "640w" in avif_srcset and "960w" in avif_srcset

    def test_srcset_null_when_single_width(self, admin_user):
        # Original 1920x1080 has no avif/webp file; the one 16:9 thumbnail is the
        # only avif width -> a one-entry ladder is suppressed.
        asset = MediaAssetFactory(uploaded_by=admin_user, mime_type="image/jpeg")
        _thumb(asset, "small", 640, 360)

        sources = asset.get_picture_sources()

        assert sources["avif_srcset"] is None
        assert sources["webp_srcset"] is None

    def test_srcset_null_when_no_thumbnails(self, admin_user):
        asset = MediaAssetFactory(uploaded_by=admin_user, mime_type="image/jpeg")
        sources = asset.get_picture_sources()
        assert sources["avif_srcset"] is None
        assert sources["fallback_srcset"] is None
        # Legacy single-URL keys are unaffected.
        assert sources["fallback"]
