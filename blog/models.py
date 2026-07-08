"""
Blog models for Spwig eCommerce platform.

Provides blog functionality with:
- Hierarchical categories and flat tags (with translations)
- Rich content via CKEditor or Page Builder (hybrid approach)
- SEO integration
- Subscriber system with digest options
- Social connector accounts for auto-sharing

"""

import uuid
import secrets
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache
from django_ckeditor_5.fields import CKEditor5Field
from design.models import DesignMixin

User = get_user_model()


class BlogCategory(DesignMixin):
    """
    Blog categories with hierarchical structure and design customization.
    Follows catalog.Category pattern for consistency.
    """
    # Basic information
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    parent = models.ForeignKey(
        'self',
        related_name='children',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    description = models.TextField(blank=True)

    # Media Library integration
    image_asset = models.ForeignKey(
        'media_library.MediaAsset',
        on_delete=models.SET_NULL,
        related_name='blog_category_images',
        null=True,
        blank=True,
        help_text=_("Category image from media library")
    )

    # Translations JSONField (merchant content)
    # Structure: {"es": {"name": "...", "description": "..."}, "fr": {...}}
    translations = models.JSONField(
        default=dict,
        blank=True,
        help_text=_("Multilingual content for category name and description")
    )

    # SEO fields
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(max_length=320, blank=True)
    seo_auto_generated = models.BooleanField(
        default=False,
        help_text=_("Automatically regenerate SEO content when saved")
    )

    # Status and display
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    # Migration tracking
    external_id = models.CharField(
        max_length=100, blank=True, db_index=True,
        help_text=_("Original ID from source platform (e.g. WordPress category ID)")
    )
    migration_job = models.ForeignKey(
        'migration.MigrationJob',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='imported_blog_categories',
        help_text=_("Migration job that imported this category")
    )
    imported_meta = models.JSONField(
        default=dict, blank=True,
        help_text=_("Metadata from import (permalink, identifiers, etc.)")
    )

    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name = _('Blog Category')
        verbose_name_plural = _('Blog Categories')
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active']),
            models.Index(fields=['sort_order']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def full_path(self):
        """Get full category path including parents."""
        if self.parent:
            return f"{self.parent.full_path} > {self.name}"
        return self.name

    def get_translated_content(self, language_code):
        """Get translated fields with fallback to default."""
        if not language_code or language_code not in self.translations:
            return {'name': self.name, 'description': self.description}

        trans = self.translations.get(language_code, {})
        return {
            'name': trans.get('name', self.name),
            'description': trans.get('description', self.description),
        }


class BlogTag(models.Model):
    """
    Flat tag structure for blog posts.
    Tags are non-hierarchical and used for cross-cutting topics.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    # Translations JSONField
    # Structure: {"es": {"name": "..."}, "fr": {...}}
    translations = models.JSONField(
        default=dict,
        blank=True,
        help_text=_("Multilingual tag names")
    )

    # Usage tracking (updated via signals)
    post_count = models.PositiveIntegerField(default=0, editable=False)

    # Migration tracking
    external_id = models.CharField(
        max_length=100, blank=True, db_index=True,
        help_text=_("Original ID from source platform (e.g. WordPress tag ID)")
    )
    migration_job = models.ForeignKey(
        'migration.MigrationJob',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='imported_blog_tags',
        help_text=_("Migration job that imported this tag")
    )

    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['name']
        verbose_name = _('Blog Tag')
        verbose_name_plural = _('Blog Tags')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_translated_name(self, language_code):
        """Get translated name with fallback."""
        if language_code and language_code in self.translations:
            return self.translations[language_code].get('name', self.name)
        return self.name


class BlogPost(DesignMixin):
    """
    Main blog post model with rich content, translations, and page_builder integration.

    Supports two content modes:
    1. Simple mode: CKEditor rich text (default)
    2. Advanced mode: Full page_builder layout (use_page_builder=True)
    """
    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('scheduled', _('Scheduled')),
        ('published', _('Published')),
        ('archived', _('Archived')),
    ]

    # Basic Information
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        db_index=True
    )

    # Template selection (overrides site-wide default from PageTemplateConfig)
    BLOG_POST_TEMPLATE_CHOICES = [
        ('', _('Use site default')),
        ('classic', _('Classic')),
        ('minimal', _('Minimal')),
        ('magazine', _('Magazine')),
        ('full_width', _('Full Width')),
    ]
    page_template = models.CharField(
        max_length=30,
        choices=BLOG_POST_TEMPLATE_CHOICES,
        default='',
        blank=True,
        verbose_name=_('Post Template'),
        help_text=_('Override the site-wide blog post template for this post.')
    )

    # Content - Hybrid approach
    excerpt = models.TextField(
        max_length=500,
        blank=True,
        help_text=_("Brief summary for listings and social sharing (primary language)")
    )
    simple_content = CKEditor5Field(
        blank=True,
        config_name='default',
        help_text=_("Full post content with rich text formatting (primary language)")
    )

    # Page Builder Integration
    use_page_builder = models.BooleanField(
        default=False,
        help_text=_("Use Page Builder for custom layout instead of simple content")
    )
    content_page = models.OneToOneField(
        'page_builder.Page',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='blog_post',
        help_text=_("Page containing the post content layout")
    )

    # Categorization
    category = models.ForeignKey(
        BlogCategory,
        related_name='posts',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    tags = models.ManyToManyField(
        BlogTag,
        related_name='posts',
        blank=True
    )

    # Media - Featured image (Media Library integration)
    featured_image = models.ForeignKey(
        'media_library.MediaAsset',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='blog_featured_images',
        help_text=_("Featured image from media library")
    )
    og_image = models.ForeignKey(
        'media_library.MediaAsset',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='blog_og_images',
        help_text=_("Open Graph image for social sharing (defaults to featured image)")
    )

    # Translations JSONField (merchant content)
    # Structure: {"es": {"title": "...", "excerpt": "...", "simple_content": "...",
    #             "meta_title": "...", "meta_description": "..."}, "fr": {...}}
    translations = models.JSONField(
        default=dict,
        blank=True,
        help_text=_("Multilingual content (title, excerpt, content, SEO)")
    )

    # SEO fields
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(max_length=320, blank=True)
    seo_auto_generated = models.BooleanField(
        default=False,
        help_text=_("Automatically regenerate SEO content when saved")
    )

    # Publishing
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)
    scheduled_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("Schedule post to be published at this time")
    )

    # Features
    is_featured = models.BooleanField(default=False, db_index=True)
    is_pinned = models.BooleanField(
        default=False,
        help_text=_("Pinned posts appear at the top of listings")
    )
    reading_time_minutes = models.PositiveIntegerField(
        default=0,
        help_text=_("Estimated reading time (auto-calculated)")
    )
    view_count = models.PositiveIntegerField(default=0, editable=False)

    # Subscriber Notification
    notify_subscribers = models.BooleanField(
        default=True,
        help_text=_("Send notification to subscribers when published")
    )
    notification_sent = models.BooleanField(default=False, editable=False)

    # Auto Social Sharing (per-post toggles)
    auto_share_facebook = models.BooleanField(default=True)
    auto_share_instagram = models.BooleanField(default=False)
    auto_share_linkedin = models.BooleanField(default=True)
    social_share_message = models.TextField(
        blank=True,
        max_length=280,
        help_text=_("Custom message for social shares (optional)")
    )

    # Author and timestamps
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='blog_posts'
    )
    # Migration tracking
    external_id = models.CharField(
        max_length=100, blank=True, db_index=True,
        help_text=_("Original ID from source platform (e.g. WordPress post ID)")
    )
    migration_job = models.ForeignKey(
        'migration.MigrationJob',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='imported_blog_posts',
        help_text=_("Migration job that imported this post")
    )
    imported_meta = models.JSONField(
        default=dict, blank=True,
        help_text=_("Metadata from import (permalink, identifiers, etc.)")
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_pinned', '-published_at']
        verbose_name = _('Blog Post')
        verbose_name_plural = _('Blog Posts')
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status', '-published_at']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['-is_pinned', '-published_at']),
            models.Index(fields=['category', 'status']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Auto-generate slug
        if not self.slug:
            self.slug = slugify(self.title)

        # Set published_at when publishing
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()

        # Calculate reading time
        self.reading_time_minutes = self.calculate_reading_time()

        super().save(*args, **kwargs)

    def calculate_reading_time(self):
        """Calculate estimated reading time (200 words per minute)."""
        word_count = 0
        if self.simple_content:
            # Strip HTML tags for word count
            import re
            text = re.sub(r'<[^>]+>', '', self.simple_content)
            word_count = len(text.split())

        if self.excerpt:
            word_count += len(self.excerpt.split())

        return max(1, word_count // 200)

    def get_absolute_url(self):
        """Return the URL for this blog post."""
        return f'/blog/{self.slug}/'

    def get_translated_content(self, language_code):
        """Get translated fields with fallback to default."""
        result = {
            'title': self.title,
            'excerpt': self.excerpt,
            'simple_content': self.simple_content,
            'meta_title': self.meta_title,
            'meta_description': self.meta_description,
        }

        if language_code and language_code in self.translations:
            trans = self.translations[language_code]
            for key in result.keys():
                if key in trans and trans[key]:
                    result[key] = trans[key]

        return result

    def get_og_image_url(self):
        """Get Open Graph image URL (og_image or featured_image)."""
        if self.og_image:
            return self.og_image.get_display_url()
        if self.featured_image:
            return self.featured_image.get_display_url()
        return None

    def get_content_page(self, create=False):
        """
        Get or create the content page for page_builder mode.

        Args:
            create: If True, create the page if it doesn't exist

        Returns:
            Page instance or None
        """
        if self.content_page:
            return self.content_page

        if create and self.pk:
            from page_builder.models import Page
            page = Page.objects.create(
                title=f"Blog: {self.title}",
                slug=f"blog-post-{self.pk}",
                page_type='blog',
                status='draft',
            )
            self.content_page = page
            self.use_page_builder = True
            self.save(update_fields=['content_page', 'use_page_builder'])
            return page

        return None

    @classmethod
    def published(cls):
        """Return queryset of published posts."""
        return cls.objects.filter(
            status='published',
            published_at__lte=timezone.now()
        )

    def get_related_posts(self, limit=3):
        """Get related posts based on category and tags."""
        related = BlogPost.published().exclude(pk=self.pk)

        # First try same category
        if self.category:
            related = related.filter(category=self.category)

        # If not enough, add posts with same tags
        if related.count() < limit and self.tags.exists():
            tag_ids = self.tags.values_list('id', flat=True)
            related = related | BlogPost.published().filter(
                tags__id__in=tag_ids
            ).exclude(pk=self.pk)

        return related.distinct()[:limit]


class BlogSubscriber(models.Model):
    """
    Blog email subscriber with frequency preferences and double opt-in.

    Subscribers can choose notification frequency:
    - immediate: Email for each new post
    - weekly: Weekly digest
    - monthly: Monthly digest
    """
    FREQUENCY_CHOICES = [
        ('immediate', _('Immediately')),
        ('weekly', _('Weekly Digest')),
        ('monthly', _('Monthly Digest')),
    ]

    VERIFICATION_STATUS = [
        ('pending', _('Pending Verification')),
        ('verified', _('Verified')),
        ('bounced', _('Email Bounced')),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True)

    # Optional link to registered user
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='blog_subscription'
    )

    # Preferences
    notification_frequency = models.CharField(
        max_length=20,
        choices=FREQUENCY_CHOICES,
        default='immediate'
    )
    subscribed_categories = models.ManyToManyField(
        BlogCategory,
        blank=True,
        related_name='subscribers',
        help_text=_("Categories to receive notifications for (empty = all)")
    )
    language_code = models.CharField(max_length=10, default='en')

    # Verification (double opt-in)
    verification_status = models.CharField(
        max_length=20,
        choices=VERIFICATION_STATUS,
        default='pending',
        db_index=True
    )
    verification_token = models.CharField(max_length=64, blank=True)
    verification_sent_at = models.DateTimeField(null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)

    # Unsubscribe
    is_active = models.BooleanField(default=True)
    unsubscribe_token = models.CharField(max_length=64, unique=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)
    unsubscribe_reason = models.TextField(blank=True)

    # Tracking
    last_digest_sent_at = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Blog Subscriber')
        verbose_name_plural = _('Blog Subscribers')
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['verification_status', 'is_active']),
            models.Index(fields=['notification_frequency', 'is_active']),
            models.Index(fields=['unsubscribe_token']),
        ]

    def __str__(self):
        return f"{self.email} ({self.get_notification_frequency_display()})"

    def save(self, *args, **kwargs):
        if not self.unsubscribe_token:
            self.unsubscribe_token = secrets.token_urlsafe(32)
        if not self.verification_token and self.verification_status == 'pending':
            self.verification_token = secrets.token_urlsafe(32)
        super().save(*args, **kwargs)

    def verify(self):
        """Mark subscriber as verified."""
        self.verification_status = 'verified'
        self.verified_at = timezone.now()
        self.verification_token = ''
        self.save(update_fields=['verification_status', 'verified_at', 'verification_token'])

    def unsubscribe(self, reason=''):
        """Unsubscribe from blog notifications."""
        self.is_active = False
        self.unsubscribed_at = timezone.now()
        self.unsubscribe_reason = reason
        self.save(update_fields=['is_active', 'unsubscribed_at', 'unsubscribe_reason'])

    def resubscribe(self):
        """Re-activate subscription."""
        self.is_active = True
        self.unsubscribed_at = None
        self.unsubscribe_reason = ''
        self.save(update_fields=['is_active', 'unsubscribed_at', 'unsubscribe_reason'])

    def get_verification_url(self, site=None):
        """Get URL for email verification."""
        if not site:
            site = Site.objects.get(pk=1)
        return f"https://{site.domain}/blog/verify/{self.verification_token}/"

    def get_unsubscribe_url(self, site=None):
        """Get URL for one-click unsubscribe."""
        if not site:
            site = Site.objects.get(pk=1)
        return f"https://{site.domain}/blog/unsubscribe/{self.unsubscribe_token}/"

    def get_preferences_url(self, site=None):
        """Get URL for managing subscription preferences."""
        if not site:
            site = Site.objects.get(pk=1)
        return f"https://{site.domain}/blog/preferences/{self.unsubscribe_token}/"

    def should_receive_post(self, post):
        """Check if subscriber should receive notification for a specific post."""
        if not self.is_active or self.verification_status != 'verified':
            return False

        # If no category preferences, receive all posts
        if not self.subscribed_categories.exists():
            return True

        # Check if post's category is in subscribed categories
        if post.category:
            return self.subscribed_categories.filter(pk=post.category.pk).exists()

        return True


class SocialConnectorAccount(models.Model):
    """
    Merchant's connected social media account for auto-posting.

    Social connectors are packaged as installable components (like exchange rate providers),
    allowing updates via the upgrade server when platforms change their APIs.
    """
    STATUS_CHOICES = [
        ('active', _('Active')),
        ('token_expired', _('Token Expired')),
        ('disconnected', _('Disconnected')),
        ('error', _('Error')),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    site = models.ForeignKey(
        'sites.Site',
        on_delete=models.CASCADE,
        verbose_name=_("site")
    )

    # Link to installed component (social connector package)
    # References the component registry entry for the social connector
    component = models.ForeignKey(
        'component_updates.ComponentRegistry',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_("Installed social connector component from registry")
    )
    provider_key = models.CharField(
        max_length=50,
        db_index=True,
        help_text=_("Provider identifier (e.g., 'facebook_page', 'linkedin_company')")
    )

    # Account display name (merchant-defined)
    name = models.CharField(max_length=255)

    # Platform details (from OAuth response)
    platform_account_id = models.CharField(max_length=255)
    platform_account_name = models.CharField(max_length=255, blank=True)
    platform_account_url = models.URLField(blank=True)
    platform_avatar_url = models.URLField(blank=True)

    # Encrypted OAuth credentials (following EmailAccount pattern)
    credentials = models.BinaryField(
        verbose_name=_("encrypted credentials"),
        help_text=_("Encrypted OAuth tokens")
    )
    access_token_expires_at = models.DateTimeField(null=True, blank=True)
    refresh_token_expires_at = models.DateTimeField(null=True, blank=True)

    # Status and error tracking
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        db_index=True
    )
    last_error = models.TextField(blank=True)
    last_error_at = models.DateTimeField(null=True, blank=True)
    last_successful_post_at = models.DateTimeField(null=True, blank=True)

    # Settings
    auto_share_enabled = models.BooleanField(default=True)
    is_default_for_provider = models.BooleanField(default=False)
    post_template = models.TextField(
        blank=True,
        help_text=_("Template for posts. Variables: {title}, {excerpt}, {url}, {hashtags}")
    )
    default_hashtags = models.CharField(max_length=500, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    connected_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='connected_social_accounts'
    )

    class Meta:
        verbose_name = _('Social Connector Account')
        verbose_name_plural = _('Social Connector Accounts')
        ordering = ['provider_key', 'name']
        indexes = [
            models.Index(fields=['site', 'provider_key', 'status']),
            models.Index(fields=['access_token_expires_at']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['site', 'provider_key', 'platform_account_id'],
                name='unique_social_connector_account'
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.provider_key})"

    def get_credentials(self):
        """Decrypt and return credentials."""
        from email_system.utils.encryption import decrypt_credentials
        if not self.credentials:
            return {}
        return decrypt_credentials(self.credentials)

    def set_credentials(self, credentials_dict):
        """Encrypt and store credentials."""
        from email_system.utils.encryption import encrypt_credentials
        self.credentials = encrypt_credentials(credentials_dict)

    def is_token_expired(self):
        """Check if access token is expired or expiring soon."""
        if not self.access_token_expires_at:
            return False
        from datetime import timedelta
        return self.access_token_expires_at <= timezone.now() + timedelta(hours=1)

    @property
    def token_expires_soon(self):
        """Check if token expires within the next 7 days."""
        if not self.access_token_expires_at:
            return False
        from datetime import timedelta
        return self.access_token_expires_at <= timezone.now() + timedelta(days=7)

    @property
    def post_count(self):
        """Count successful posts made through this account."""
        return self.auto_shares.filter(status='posted').count()


class BlogPostAutoShare(models.Model):
    """
    Tracks auto-share status for each blog post per social platform.

    Created when a post is published with auto-share enabled.
    Supports scheduling and retry logic for failed shares.
    """
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('scheduled', _('Scheduled')),
        ('posting', _('Posting')),
        ('posted', _('Posted')),
        ('failed', _('Failed')),
        ('skipped', _('Skipped')),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name='auto_shares'
    )
    social_account = models.ForeignKey(
        SocialConnectorAccount,
        on_delete=models.CASCADE,
        related_name='auto_shares'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        db_index=True
    )

    # Scheduling
    scheduled_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("When to post (null = immediately on publish)")
    )

    # Result
    platform_post_id = models.CharField(max_length=255, blank=True)
    platform_post_url = models.URLField(blank=True)
    posted_at = models.DateTimeField(null=True, blank=True)
    posted_content = models.TextField(blank=True)

    # Retry logic
    error_message = models.TextField(blank=True)
    retry_count = models.PositiveIntegerField(default=0)
    max_retries = models.PositiveIntegerField(default=3)
    next_retry_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Blog Post Auto Share')
        verbose_name_plural = _('Blog Post Auto Shares')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'scheduled_at']),
            models.Index(fields=['status', 'next_retry_at']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['post', 'social_account'],
                name='unique_post_social_account'
            ),
        ]

    def __str__(self):
        return f"{self.post.title} -> {self.social_account.name} ({self.status})"

    def can_retry(self):
        """Check if this share can be retried."""
        return (
            self.status == 'failed' and
            self.retry_count < self.max_retries and
            self.social_account.status == 'active'
        )

    def calculate_next_retry(self):
        """Calculate next retry time with exponential backoff."""
        from datetime import timedelta
        if not self.can_retry():
            return None
        # Exponential backoff: 5 min, 30 min, 2 hours
        delays = [5, 30, 120]
        delay_minutes = delays[min(self.retry_count, len(delays) - 1)]
        return timezone.now() + timedelta(minutes=delay_minutes)


class BlogSettings(models.Model):
    """
    Global blog settings - singleton model.

    Configures display options, RSS feed, subscriptions, and digest schedules.
    """
    # Display
    posts_per_page = models.PositiveIntegerField(default=10)
    show_reading_time = models.BooleanField(default=True)
    show_view_count = models.BooleanField(default=False)
    show_related_posts = models.BooleanField(default=True)
    related_posts_count = models.PositiveIntegerField(default=3)

    # RSS Feed
    rss_enabled = models.BooleanField(default=True)
    rss_posts_count = models.PositiveIntegerField(default=20)
    rss_include_full_content = models.BooleanField(
        default=False,
        help_text=_("Include full content in RSS (False = excerpt only)")
    )

    # Subscriptions
    enable_subscriptions = models.BooleanField(default=True)
    require_double_opt_in = models.BooleanField(default=True)
    default_frequency = models.CharField(
        max_length=20,
        choices=BlogSubscriber.FREQUENCY_CHOICES,
        default='weekly'
    )

    # Digest schedule (UTC)
    weekly_digest_day = models.PositiveIntegerField(
        default=1,
        help_text=_("Day of week for weekly digest (0=Sunday, 1=Monday, ...)")
    )
    weekly_digest_hour = models.PositiveIntegerField(
        default=9,
        help_text=_("Hour (UTC) to send weekly digest")
    )
    monthly_digest_day = models.PositiveIntegerField(
        default=1,
        help_text=_("Day of month for monthly digest")
    )
    monthly_digest_hour = models.PositiveIntegerField(
        default=9,
        help_text=_("Hour (UTC) to send monthly digest")
    )

    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('Blog Settings')
        verbose_name_plural = _('Blog Settings')

    def __str__(self):
        return "Blog Settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
        cache.delete('blog_settings')

    def delete(self, *args, **kwargs):
        pass  # Prevent deletion of singleton

    @classmethod
    def get_settings(cls):
        """Get the blog settings instance (cached)."""
        settings = cache.get('blog_settings')
        if settings is None:
            settings, _ = cls.objects.get_or_create(pk=1)
            cache.set('blog_settings', settings, 3600)
        return settings
