"""
Category Serializers for Admin API

Serializers for category management (CRUD + bulk operations).
"""
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from catalog.models import Category


class AdminCategoryListSerializer(serializers.ModelSerializer):
    """Compact serializer for category list view."""
    parent_name = serializers.SerializerMethodField()
    product_count = serializers.IntegerField(read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
            'parent_id',
            'parent_name',
            'is_active',
            'is_featured',
            'sort_order',
            'product_count',
            'image_url',
        ]

    def get_parent_name(self, obj):
        return obj.parent.name if obj.parent else None

    def get_image_url(self, obj):
        if obj.image_asset:
            return obj.image_asset.get_thumbnail('medium') or obj.image_asset.get_display_url()
        return None


class AdminCategoryDetailSerializer(serializers.ModelSerializer):
    """Full category detail serializer."""
    parent_name = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()
    product_count = serializers.IntegerField(read_only=True)
    image_url = serializers.SerializerMethodField()
    banner_url = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
            'parent_id',
            'parent_name',
            'description',
            'icon',
            'is_active',
            'is_featured',
            'sort_order',
            'products_per_page',
            'page_template',
            'meta_title',
            'meta_description',
            'image_url',
            'banner_url',
            'children',
            'product_count',
            'created_at',
            'updated_at',
        ]

    def get_parent_name(self, obj):
        return obj.parent.name if obj.parent else None

    def get_children(self, obj):
        children = obj.children.filter(is_active=True).order_by('sort_order', 'name')
        return [{'id': c.id, 'name': c.name, 'slug': c.slug} for c in children]

    def get_image_url(self, obj):
        if obj.image_asset:
            return obj.image_asset.get_thumbnail('medium') or obj.image_asset.get_display_url()
        return None

    def get_banner_url(self, obj):
        if obj.banner_asset:
            return obj.banner_asset.get_display_url()
        return None


class CategoryCreateSerializer(serializers.Serializer):
    """Serializer for creating a category."""
    name = serializers.CharField(max_length=200)
    slug = serializers.SlugField(max_length=200, required=False, allow_blank=True)
    parent_id = serializers.IntegerField(required=False, allow_null=True)
    description = serializers.CharField(required=False, allow_blank=True, default='')
    icon = serializers.CharField(max_length=100, required=False, allow_blank=True, default='')
    is_active = serializers.BooleanField(default=True)
    is_featured = serializers.BooleanField(default=False)
    sort_order = serializers.IntegerField(default=0, min_value=0)
    products_per_page = serializers.IntegerField(default=24, min_value=1)
    page_template = serializers.ChoiceField(
        choices=[c[0] for c in Category.CATEGORY_PAGE_TEMPLATE_CHOICES],
        required=False,
        default=''
    )
    meta_title = serializers.CharField(max_length=255, required=False, allow_blank=True, default='')
    meta_description = serializers.CharField(max_length=255, required=False, allow_blank=True, default='')
    external_id = serializers.CharField(max_length=100, required=False, allow_blank=True, default='')

    def validate_slug(self, value):
        if value and Category.objects.filter(slug=value).exists():
            raise serializers.ValidationError(_("A category with this slug already exists."))
        return value

    def validate_parent_id(self, value):
        if value is not None:
            try:
                Category.objects.get(id=value)
            except Category.DoesNotExist:
                raise serializers.ValidationError(_("Parent category not found."))
        return value


class CategoryUpdateSerializer(serializers.Serializer):
    """Serializer for partial update of a category."""
    name = serializers.CharField(max_length=200, required=False)
    slug = serializers.SlugField(max_length=200, required=False, allow_blank=True)
    parent_id = serializers.IntegerField(required=False, allow_null=True)
    description = serializers.CharField(required=False, allow_blank=True)
    icon = serializers.CharField(max_length=100, required=False, allow_blank=True)
    is_active = serializers.BooleanField(required=False)
    is_featured = serializers.BooleanField(required=False)
    sort_order = serializers.IntegerField(min_value=0, required=False)
    products_per_page = serializers.IntegerField(min_value=1, required=False)
    page_template = serializers.ChoiceField(
        choices=[c[0] for c in Category.CATEGORY_PAGE_TEMPLATE_CHOICES],
        required=False,
    )
    meta_title = serializers.CharField(max_length=255, required=False, allow_blank=True)
    meta_description = serializers.CharField(max_length=255, required=False, allow_blank=True)

    def validate_parent_id(self, value):
        if value is not None:
            category = self.context.get('category')
            try:
                parent = Category.objects.get(id=value)
            except Category.DoesNotExist:
                raise serializers.ValidationError(_("Parent category not found."))
            # Prevent circular reference
            if category:
                if parent.id == category.id:
                    raise serializers.ValidationError(_("A category cannot be its own parent."))
                # Check if the proposed parent is a descendant
                current = parent
                while current.parent_id:
                    if current.parent_id == category.id:
                        raise serializers.ValidationError(_("Cannot set parent to a descendant category."))
                    current = current.parent
        return value

    def validate_slug(self, value):
        if value:
            category = self.context.get('category')
            qs = Category.objects.filter(slug=value)
            if category:
                qs = qs.exclude(id=category.id)
            if qs.exists():
                raise serializers.ValidationError(_("A category with this slug already exists."))
        return value


class CategoryFilterSerializer(serializers.Serializer):
    """Serializer for category list filters."""
    search = serializers.CharField(required=False, allow_blank=True)
    parent_id = serializers.IntegerField(required=False, allow_null=True)
    is_active = serializers.ChoiceField(
        choices=[('all', 'All'), ('true', 'Active'), ('false', 'Inactive')],
        required=False,
        default='all'
    )
    sort = serializers.ChoiceField(
        choices=[
            ('sort_order', 'Sort Order'),
            ('name', 'Name A-Z'),
            ('-name', 'Name Z-A'),
            ('-created_at', 'Newest First'),
            ('created_at', 'Oldest First'),
        ],
        required=False,
        default='sort_order'
    )
    page = serializers.IntegerField(required=False, default=1, min_value=1)
    page_size = serializers.IntegerField(required=False, default=50, min_value=1, max_value=100)


class BulkCategoryCreateSerializer(serializers.Serializer):
    """Wrapper serializer for bulk category creation."""
    categories = CategoryCreateSerializer(many=True)

    def validate_categories(self, value):
        if len(value) > 100:
            raise serializers.ValidationError(_("Maximum 100 categories per bulk request."))
        if len(value) == 0:
            raise serializers.ValidationError(_("At least one category is required."))
        return value


class CategoryImageUploadSerializer(serializers.Serializer):
    """Serializer for uploading a category image or banner."""
    image = serializers.ImageField(
        help_text=_('Image file to upload (JPEG, PNG, GIF, WebP supported)')
    )
    alt_text = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
        help_text=_('Alt text for accessibility')
    )
