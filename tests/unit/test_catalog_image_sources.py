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


SOURCE_KEYS = {"avif", "webp", "fallback", "width", "height"}


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
