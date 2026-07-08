"""
DRF Serializers for Blog API.

Provides serializers for:
- Blog posts (list/detail/write)
- Blog categories (list/detail/write)
- Blog tags (list/write)
- Subscriber management (subscribe/preferences)
- Blog settings (public subset)

"""
from rest_framework import serializers
from django.utils.text import slugify
from drf_spectacular.utils import extend_schema_field
from media_library.models import MediaAsset

from .models import BlogPost, BlogCategory, BlogTag, BlogSubscriber, BlogSettings


# =============================================================================
# Category Serializers
# =============================================================================

class BlogCategorySlimSerializer(serializers.ModelSerializer):
    """Minimal category serializer for nesting inside other serializers."""

    class Meta:
        model = BlogCategory
        fields = ['id', 'name', 'slug']


class BlogCategorySerializer(serializers.ModelSerializer):
    """
    Category list serializer with translation support.
    Returns translated name/description when Accept-Language header is present.
    """
    image_url = serializers.SerializerMethodField()
    parent_id = serializers.PrimaryKeyRelatedField(source='parent', read_only=True)
    post_count = serializers.SerializerMethodField()

    class Meta:
        model = BlogCategory
        fields = [
            'id',
            'name',
            'slug',
            'parent_id',
            'description',
            'image_url',
            'post_count',
            'is_active',
            'sort_order',
        ]

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_image_url(self, obj) -> str | None:
        """Get image URL from MediaAsset."""
        if obj.image_asset:
            return obj.image_asset.get_display_url()
        return None

    @extend_schema_field(serializers.IntegerField())
    def get_post_count(self, obj) -> int:
        """Count published posts in this category."""
        return obj.posts.filter(status='published').count()

    def to_representation(self, instance):
        """Apply translations based on Accept-Language header."""
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request:
            lang = getattr(request, 'LANGUAGE_CODE', None)
            if lang:
                translated = instance.get_translated_content(lang)
                data['name'] = translated.get('name', data['name'])
                data['description'] = translated.get('description', data['description'])
        return data


class BlogCategoryDetailSerializer(BlogCategorySerializer):
    """
    Category detail serializer.
    Adds SEO fields and child categories.
    """
    children = BlogCategorySlimSerializer(many=True, read_only=True)

    class Meta(BlogCategorySerializer.Meta):
        fields = BlogCategorySerializer.Meta.fields + [
            'meta_title',
            'meta_description',
            'children',
            'created_at',
            'updated_at',
        ]

    def to_representation(self, instance):
        """Apply translations for SEO fields in addition to parent's name/description."""
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request:
            lang = getattr(request, 'LANGUAGE_CODE', None)
            if lang and lang in (instance.translations or {}):
                trans = instance.translations[lang]
                data['meta_title'] = trans.get('meta_title', data['meta_title'])
                data['meta_description'] = trans.get('meta_description', data['meta_description'])
        return data


class BlogCategoryWriteSerializer(serializers.ModelSerializer):
    """
    Category write serializer for staff create/update operations.
    Slug is auto-generated from name if not provided.
    """
    slug = serializers.SlugField(required=False, allow_blank=True, default='')
    image_asset = serializers.PrimaryKeyRelatedField(
        queryset=MediaAsset.objects.all(),
        required=False,
        allow_null=True,
    )
    parent = serializers.PrimaryKeyRelatedField(
        queryset=BlogCategory.objects.all(),
        required=False,
        allow_null=True,
    )
    translations = serializers.JSONField(required=False, default=dict)

    class Meta:
        model = BlogCategory
        fields = [
            'name',
            'slug',
            'parent',
            'description',
            'image_asset',
            'is_active',
            'sort_order',
            'meta_title',
            'meta_description',
            'translations',
        ]

    def validate(self, data):
        if not data.get('slug') and data.get('name'):
            data['slug'] = slugify(data['name'])
        return data


# =============================================================================
# Tag Serializers
# =============================================================================

class BlogTagSerializer(serializers.ModelSerializer):
    """Tag serializer with translation support."""

    class Meta:
        model = BlogTag
        fields = ['id', 'name', 'slug', 'post_count']

    def to_representation(self, instance):
        """Apply tag name translation."""
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request:
            lang = getattr(request, 'LANGUAGE_CODE', None)
            if lang:
                data['name'] = instance.get_translated_name(lang)
        return data


class BlogTagWriteSerializer(serializers.ModelSerializer):
    """Tag write serializer for staff create/update operations."""
    slug = serializers.SlugField(required=False, allow_blank=True, default='')
    translations = serializers.JSONField(required=False, default=dict)

    class Meta:
        model = BlogTag
        fields = ['name', 'slug', 'translations']

    def validate(self, data):
        if not data.get('slug') and data.get('name'):
            data['slug'] = slugify(data['name'])
        return data


# =============================================================================
# Post Serializers
# =============================================================================

class BlogPostListSerializer(serializers.ModelSerializer):
    """
    Lightweight post serializer for list views.
    Includes translation support and computed image URLs.
    """
    category = BlogCategorySlimSerializer(read_only=True)
    tags = BlogTagSerializer(many=True, read_only=True)
    featured_image_url = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = [
            'id',
            'title',
            'slug',
            'status',
            'excerpt',
            'category',
            'tags',
            'featured_image_url',
            'published_at',
            'reading_time_minutes',
            'view_count',
            'is_featured',
            'is_pinned',
            'created_at',
        ]

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_featured_image_url(self, obj) -> str | None:
        if obj.featured_image:
            return obj.featured_image.get_display_url()
        return None

    def to_representation(self, instance):
        """Apply post translations based on Accept-Language header."""
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request:
            lang = getattr(request, 'LANGUAGE_CODE', None)
            if lang:
                translated = instance.get_translated_content(lang)
                data['title'] = translated.get('title', data['title'])
                data['excerpt'] = translated.get('excerpt', data['excerpt'])
        return data


class BlogPostDetailSerializer(BlogPostListSerializer):
    """
    Full post serializer for detail views.
    Includes content, related posts, SEO, and OG image.

    Note: When content_type is 'page_builder', the post uses the Page Builder
    for its layout and simple_content is not available via API. Fetch the
    rendered HTML from the storefront URL instead.
    """
    related_posts = serializers.SerializerMethodField()
    og_image_url = serializers.SerializerMethodField()
    content_type = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()

    class Meta(BlogPostListSerializer.Meta):
        fields = BlogPostListSerializer.Meta.fields + [
            'simple_content',
            'content_type',
            'meta_title',
            'meta_description',
            'og_image_url',
            'scheduled_at',
            'related_posts',
            'author_name',
            'updated_at',
        ]

    @extend_schema_field(serializers.ListSerializer(child=BlogPostListSerializer()))
    def get_related_posts(self, obj) -> list:
        settings = BlogSettings.get_settings()
        if not settings.show_related_posts:
            return []
        related = obj.get_related_posts(limit=settings.related_posts_count)
        return BlogPostListSerializer(
            related,
            many=True,
            context=self.context,
        ).data

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_og_image_url(self, obj) -> str | None:
        return obj.get_og_image_url()

    @extend_schema_field(serializers.ChoiceField(choices=['simple', 'page_builder']))
    def get_content_type(self, obj) -> str:
        return 'page_builder' if obj.use_page_builder else 'simple'

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_author_name(self, obj) -> str | None:
        if obj.created_by:
            return obj.created_by.get_full_name() or obj.created_by.username
        return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request:
            lang = getattr(request, 'LANGUAGE_CODE', None)
            if lang:
                translated = instance.get_translated_content(lang)
                data['meta_title'] = translated.get('meta_title', data['meta_title'])
                data['meta_description'] = translated.get('meta_description', data['meta_description'])
                # Only overlay simple_content when it's the content type in use
                if data.get('content_type') == 'simple':
                    data['simple_content'] = translated.get('simple_content', data['simple_content'])
        # Page builder posts: clear simple_content — it lives in the page builder, not the API
        if data.get('content_type') == 'page_builder':
            data['simple_content'] = None
        return data


class BlogPostWriteSerializer(serializers.ModelSerializer):
    """
    Post write serializer for staff create/update.
    Slug is auto-generated from title when not provided.
    Tags can be supplied as a list of slugs.
    Featured image is supplied as a MediaAsset primary key.
    """
    slug = serializers.SlugField(required=False, allow_blank=True, default='')
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=BlogCategory.objects.all(),
        required=False,
        allow_null=True,
    )
    tags = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=BlogTag.objects.all(),
        many=True,
        required=False,
    )
    featured_image = serializers.PrimaryKeyRelatedField(
        queryset=MediaAsset.objects.all(),
        required=False,
        allow_null=True,
    )
    translations = serializers.JSONField(required=False, default=dict)

    class Meta:
        model = BlogPost
        fields = [
            'title',
            'slug',
            'status',
            'excerpt',
            'simple_content',
            'category',
            'tags',
            'featured_image',
            'is_featured',
            'is_pinned',
            'scheduled_at',
            'meta_title',
            'meta_description',
            'notify_subscribers',
            'auto_share_facebook',
            'auto_share_instagram',
            'auto_share_linkedin',
            'social_share_message',
            'translations',
        ]

    def validate(self, data):
        # Auto-generate slug from title if not provided
        if not data.get('slug') and data.get('title'):
            base_slug = slugify(data['title'])
            slug = base_slug
            counter = 1
            instance = getattr(self, 'instance', None)
            qs = BlogPost.objects.filter(slug=slug)
            if instance:
                qs = qs.exclude(pk=instance.pk)
            while qs.exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
                qs = BlogPost.objects.filter(slug=slug)
                if instance:
                    qs = qs.exclude(pk=instance.pk)
            data['slug'] = slug

        # Scheduled posts must have a scheduled_at time
        if data.get('status') == 'scheduled' and not data.get('scheduled_at'):
            if not (self.instance and self.instance.scheduled_at):
                raise serializers.ValidationError(
                    {'scheduled_at': 'A scheduled_at datetime is required for scheduled posts.'}
                )
        return data

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['created_by'] = request.user
        post = super().create(validated_data)
        if tags:
            post.tags.set(tags)
        return post

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        post = super().update(instance, validated_data)
        if tags is not None:
            post.tags.set(tags)
        return post


# =============================================================================
# Subscriber Serializers
# =============================================================================

class BlogSubscribeSerializer(serializers.Serializer):
    """
    Subscription request serializer.
    Validates and normalises incoming subscribe POST data.
    """
    email = serializers.EmailField()
    name = serializers.CharField(max_length=255, required=False, allow_blank=True, default='')
    notification_frequency = serializers.ChoiceField(
        choices=BlogSubscriber.FREQUENCY_CHOICES,
        required=False,
    )
    category_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        default=list,
    )
    language_code = serializers.CharField(max_length=10, required=False, default='en')

    def validate_email(self, value):
        return value.strip().lower()


class BlogPreferencesSerializer(serializers.Serializer):
    """
    Subscription preferences serializer — used for both GET and PUT.
    """
    notification_frequency = serializers.ChoiceField(choices=BlogSubscriber.FREQUENCY_CHOICES)
    subscribed_categories = BlogCategorySlimSerializer(many=True, read_only=True)
    subscribed_category_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        default=list,
    )
    language_code = serializers.CharField(max_length=10)
    is_active = serializers.BooleanField(read_only=True)
    verification_status = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)


# =============================================================================
# Settings Serializer
# =============================================================================

class BlogSettingsPublicSerializer(serializers.ModelSerializer):
    """
    Public-facing subset of blog settings.
    Exposes display preferences and feature flags relevant to frontend consumers.
    """

    class Meta:
        model = BlogSettings
        fields = [
            'posts_per_page',
            'show_reading_time',
            'show_view_count',
            'show_related_posts',
            'related_posts_count',
            'rss_enabled',
            'enable_subscriptions',
            'require_double_opt_in',
            'default_frequency',
        ]
