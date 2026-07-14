"""
Brand Serializers for Admin API

Serializers for brand management (CRUD + bulk operations).
"""

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from catalog.models import Brand


class AdminBrandListSerializer(serializers.ModelSerializer):
    """Compact serializer for brand list view."""

    product_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Brand
        fields = [
            "id",
            "name",
            "slug",
            "is_active",
            "is_featured",
            "website",
            "product_count",
            "created_at",
        ]


class AdminBrandDetailSerializer(serializers.ModelSerializer):
    """Full brand detail serializer."""

    product_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Brand
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "website",
            "show_brand_page",
            "brand_story",
            "is_active",
            "is_featured",
            "meta_title",
            "meta_description",
            "product_count",
            "created_at",
        ]


class BrandCreateSerializer(serializers.Serializer):
    """Serializer for creating a brand."""

    name = serializers.CharField(max_length=200)
    slug = serializers.SlugField(max_length=200, required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True, default="")
    website = serializers.URLField(required=False, allow_blank=True, default="")
    show_brand_page = serializers.BooleanField(default=True)
    brand_story = serializers.CharField(required=False, allow_blank=True, default="")
    is_active = serializers.BooleanField(default=True)
    is_featured = serializers.BooleanField(default=False)
    meta_title = serializers.CharField(max_length=255, required=False, allow_blank=True, default="")
    meta_description = serializers.CharField(
        max_length=255, required=False, allow_blank=True, default=""
    )

    def validate_name(self, value):
        if Brand.objects.filter(name=value).exists():
            raise serializers.ValidationError(_("A brand with this name already exists."))
        return value

    def validate_slug(self, value):
        if value and Brand.objects.filter(slug=value).exists():
            raise serializers.ValidationError(_("A brand with this slug already exists."))
        return value


class BrandUpdateSerializer(serializers.Serializer):
    """Serializer for partial update of a brand."""

    name = serializers.CharField(max_length=200, required=False)
    slug = serializers.SlugField(max_length=200, required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    website = serializers.URLField(required=False, allow_blank=True)
    show_brand_page = serializers.BooleanField(required=False)
    brand_story = serializers.CharField(required=False, allow_blank=True)
    is_active = serializers.BooleanField(required=False)
    is_featured = serializers.BooleanField(required=False)
    meta_title = serializers.CharField(max_length=255, required=False, allow_blank=True)
    meta_description = serializers.CharField(max_length=255, required=False, allow_blank=True)

    def validate_name(self, value):
        brand = self.context.get("brand")
        qs = Brand.objects.filter(name=value)
        if brand:
            qs = qs.exclude(id=brand.id)
        if qs.exists():
            raise serializers.ValidationError(_("A brand with this name already exists."))
        return value

    def validate_slug(self, value):
        if value:
            brand = self.context.get("brand")
            qs = Brand.objects.filter(slug=value)
            if brand:
                qs = qs.exclude(id=brand.id)
            if qs.exists():
                raise serializers.ValidationError(_("A brand with this slug already exists."))
        return value


class BrandFilterSerializer(serializers.Serializer):
    """Serializer for brand list filters."""

    search = serializers.CharField(required=False, allow_blank=True)
    is_active = serializers.ChoiceField(
        choices=[("all", "All"), ("true", "Active"), ("false", "Inactive")],
        required=False,
        default="all",
    )
    sort = serializers.ChoiceField(
        choices=[
            ("name", "Name A-Z"),
            ("-name", "Name Z-A"),
            ("-created_at", "Newest First"),
            ("created_at", "Oldest First"),
        ],
        required=False,
        default="name",
    )
    page = serializers.IntegerField(required=False, default=1, min_value=1)
    page_size = serializers.IntegerField(required=False, default=50, min_value=1, max_value=100)


class BulkBrandCreateSerializer(serializers.Serializer):
    """Wrapper serializer for bulk brand creation."""

    brands = BrandCreateSerializer(many=True)

    def validate_brands(self, value):
        if len(value) > 100:
            raise serializers.ValidationError(_("Maximum 100 brands per bulk request."))
        if len(value) == 0:
            raise serializers.ValidationError(_("At least one brand is required."))
        return value
