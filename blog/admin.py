"""
Blog admin configuration for Spwig eCommerce platform.

Provides comprehensive admin interfaces for:
- Blog categories and tags
- Blog posts with rich content editing
- Subscriber management
- Social connector accounts
- Auto-share tracking
- Global blog settings

"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.urls import reverse, path
from django.http import HttpResponseRedirect
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from core.admin_mixins import TranslatableAdminMixin
from core.widgets import TranslatableFieldWidget
from media_library.widgets import MediaLibrarySelectWidget
from seo_generator.admin_mixin import SEOGeneratorAdminMixin

from .models import (
    BlogCategory, BlogTag, BlogPost, BlogSubscriber,
    SocialConnectorAccount, BlogPostAutoShare, BlogSettings
)


# =============================================================================
# Forms
# =============================================================================

class BlogCategoryForm(forms.ModelForm):
    """Form for BlogCategory with translatable field widgets."""
    class Meta:
        model = BlogCategory
        fields = '__all__'
        widgets = {
            'name': TranslatableFieldWidget(
                base_widget=forms.TextInput(attrs={'class': 'vTextField', 'style': 'width: 100%;'})
            ),
            'description': TranslatableFieldWidget(
                base_widget=forms.Textarea(attrs={'rows': 3, 'class': 'vLargeTextField', 'style': 'width: 100%;'})
            ),
            'meta_title': TranslatableFieldWidget(
                base_widget=forms.TextInput(attrs={'class': 'vTextField', 'style': 'width: 100%;'})
            ),
            'meta_description': TranslatableFieldWidget(
                base_widget=forms.Textarea(attrs={'rows': 3, 'class': 'vLargeTextField', 'style': 'width: 100%;'})
            ),
        }


class BlogPostForm(forms.ModelForm):
    """Form for BlogPost with translatable fields and CKEditor support."""
    class Meta:
        model = BlogPost
        fields = '__all__'
        exclude = [
            'css_classes', 'layout_config', 'style_overrides',
            'responsive_config', 'inherit_parent_theme',
            'template_variant',
        ]
        widgets = {
            'title': TranslatableFieldWidget(
                base_widget=forms.TextInput(attrs={'class': 'vTextField', 'style': 'width: 100%;'})
            ),
            'excerpt': TranslatableFieldWidget(
                base_widget=forms.Textarea(attrs={'rows': 3, 'class': 'vLargeTextField', 'style': 'width: 100%;'})
            ),
            'simple_content': TranslatableFieldWidget(
                base_widget=CKEditor5Widget(config_name='content_rich')
            ),
            'meta_title': TranslatableFieldWidget(
                base_widget=forms.TextInput(attrs={'class': 'vTextField', 'style': 'width: 100%;'})
            ),
            'meta_description': TranslatableFieldWidget(
                base_widget=forms.Textarea(attrs={'rows': 3, 'class': 'vLargeTextField', 'style': 'width: 100%;'})
            ),
            'featured_image': MediaLibrarySelectWidget(selection_mode='single'),
            'og_image': MediaLibrarySelectWidget(selection_mode='single'),
        }


# =============================================================================
# Inlines
# =============================================================================

class BlogPostAutoShareInline(admin.TabularInline):
    """Inline for viewing auto-share status of a blog post."""
    model = BlogPostAutoShare
    extra = 0
    readonly_fields = [
        'social_account', 'status', 'scheduled_at',
        'posted_at', 'platform_post_url_link', 'retry_count', 'error_message'
    ]
    fields = [
        'social_account', 'status', 'scheduled_at',
        'posted_at', 'platform_post_url_link', 'retry_count'
    ]
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

    def platform_post_url_link(self, obj):
        """Display platform post URL as a clickable link."""
        if obj.platform_post_url:
            return format_html(
                '<a href="{}" target="_blank" rel="noopener">View Post</a>',
                obj.platform_post_url
            )
        return '-'
    platform_post_url_link.short_description = _('Platform Link')


# =============================================================================
# Category Admin
# =============================================================================

@admin.register(BlogCategory)
class BlogCategoryAdmin(SEOGeneratorAdminMixin, TranslatableAdminMixin, admin.ModelAdmin):
    """Admin for blog categories with hierarchical display."""
    form = BlogCategoryForm
    change_list_template = 'admin/blog/blogcategory/change_list.html'
    list_display = ['name', 'parent', 'post_count', 'is_active', 'sort_order']
    list_filter = ['is_active', 'parent']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ['parent', 'image_asset']

    translatable_fields = ['name', 'description', 'meta_title', 'meta_description']

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'slug', 'parent', 'description')
        }),
        (_('Media'), {
            'fields': ('image_asset',)
        }),
        (_('Design & Theme'), {
            'fields': ('template_variant',),
            'classes': ('collapse',),
        }),
        (_('SEO'), {
            'fields': ('meta_title', 'meta_description', 'seo_auto_generated')
        }),
        (_('Status'), {
            'fields': ('is_active', 'sort_order')
        }),
    )

    class Media:
        js = TranslatableAdminMixin.Media.js + SEOGeneratorAdminMixin.Media.js
        css = {
            'all': TranslatableAdminMixin.Media.css.get('all', ()) +
                   SEOGeneratorAdminMixin.Media.css.get('all', ())
        }

    def post_count(self, obj):
        """Display number of posts in category."""
        count = obj.posts.count()
        if count > 0:
            url = reverse('admin:blog_blogpost_changelist') + f'?category__id__exact={obj.pk}'
            return format_html('<a href="{}">{} posts</a>', url, count)
        return '0 posts'
    post_count.short_description = _('Posts')

    def changelist_view(self, request, extra_context=None):
        """Add extra context for the custom change list template."""
        extra_context = extra_context or {}
        extra_context['parent_categories'] = BlogCategory.objects.filter(
            parent__isnull=True
        ).order_by('sort_order', 'name')
        return super().changelist_view(request, extra_context=extra_context)


# =============================================================================
# Tag Admin
# =============================================================================

@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    """Admin for blog tags."""
    change_list_template = 'admin/blog/blogtag/change_list.html'
    list_display = ['name', 'post_count', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['post_count', 'created_at']

    fieldsets = (
        (None, {
            'fields': ('name', 'slug')
        }),
        (_('Translations'), {
            'fields': ('translations',),
            'classes': ('collapse',),
        }),
        (_('Info'), {
            'fields': ('post_count', 'created_at'),
            'classes': ('collapse',),
        }),
    )

    def post_count(self, obj):
        """Display usage count with link to posts."""
        count = obj.posts.count()
        if count > 0:
            url = reverse('admin:blog_blogpost_changelist') + f'?tags__id__exact={obj.pk}'
            return format_html('<a href="{}">{}</a>', url, count)
        return '0'
    post_count.short_description = _('Posts')


# =============================================================================
# Blog Post Admin
# =============================================================================

@admin.register(BlogPost)
class BlogPostAdmin(SEOGeneratorAdminMixin, TranslatableAdminMixin, admin.ModelAdmin):
    """Admin for blog posts with full content editing."""
    form = BlogPostForm
    change_form_template = 'admin/blog/blogpost/change_form.html'
    change_list_template = 'admin/blog/blogpost/change_list.html'
    list_per_page = 20

    list_display = [
        'title', 'category', 'status', 'is_featured', 'is_pinned',
        'published_at_display', 'view_count', 'reading_time_display'
    ]
    list_filter = [
        'status', 'is_featured', 'is_pinned', 'category',
        'created_at', 'published_at'
    ]
    search_fields = ['title', 'excerpt', 'simple_content']
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ['category', 'content_page']
    filter_horizontal = ['tags']
    readonly_fields = [
        'view_count', 'reading_time_minutes', 'notification_sent',
        'created_at', 'updated_at', 'created_by'
    ]
    date_hierarchy = 'published_at'

    translatable_fields = ['title', 'excerpt', 'simple_content', 'meta_title', 'meta_description']

    inlines = [BlogPostAutoShareInline]

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('title', 'slug', 'status', 'category', 'tags')
        }),
        (_('Content'), {
            'fields': (
                'excerpt', 'simple_content',
                'use_page_builder', 'content_page'
            ),
            'description': _(
                'Use simple content for basic posts, or enable Page Builder for '
                'advanced layouts. When Page Builder is enabled, edit the linked page.'
            )
        }),
        (_('Media'), {
            'fields': ('featured_image', 'og_image'),
        }),
        (_('Design & Theme'), {
            'fields': ('page_template',),
            'classes': ('collapse',),
        }),
        (_('SEO'), {
            'fields': ('meta_title', 'meta_description', 'seo_auto_generated')
        }),
        (_('Publishing'), {
            'fields': (
                'published_at', 'scheduled_at',
                'is_featured', 'is_pinned'
            )
        }),
        (_('Subscriber Notification'), {
            'fields': ('notify_subscribers', 'notification_sent'),
        }),
        (_('Auto Social Sharing'), {
            'fields': (
                'auto_share_facebook', 'auto_share_instagram', 'auto_share_linkedin',
                'social_share_message'
            ),
            'classes': ('collapse',),
        }),
        (_('Stats'), {
            'fields': ('view_count', 'reading_time_minutes'),
            'classes': ('collapse',),
        }),
        (_('Meta'), {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    class Media:
        js = TranslatableAdminMixin.Media.js + SEOGeneratorAdminMixin.Media.js + (
            'blog/admin/js/blog_post.js',
        )
        css = {
            'all': TranslatableAdminMixin.Media.css.get('all', ()) +
                   SEOGeneratorAdminMixin.Media.css.get('all', ()) + (
                'blog/admin/css/blog_post.css',
            )
        }

    def published_at_display(self, obj):
        """Display published date or scheduled date with icon."""
        if obj.status == 'published' and obj.published_at:
            return format_html(
                '<span style="color: green;">&#10003;</span> {}',
                obj.published_at.strftime('%Y-%m-%d %H:%M')
            )
        elif obj.status == 'scheduled' and obj.scheduled_at:
            return format_html(
                '<span style="color: orange;">&#9203;</span> {}',
                obj.scheduled_at.strftime('%Y-%m-%d %H:%M')
            )
        return '-'
    published_at_display.short_description = _('Published/Scheduled')
    published_at_display.admin_order_field = 'published_at'

    def reading_time_display(self, obj):
        """Display reading time in minutes."""
        return f'{obj.reading_time_minutes} min'
    reading_time_display.short_description = _('Read Time')

    def save_model(self, request, obj, form, change):
        """Set created_by on new posts."""
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def add_view(self, request, form_url='', extra_context=None):
        """Create a draft post and redirect to the change form for full editing experience."""
        from django.utils.text import slugify
        import uuid

        # Create a new draft post with a unique slug
        unique_id = str(uuid.uuid4())[:8]
        new_post = BlogPost.objects.create(
            title=_('Untitled Post'),
            slug=f'untitled-post-{unique_id}',
            status='draft',
            created_by=request.user
        )

        self.message_user(
            request,
            _('New draft post created. Start editing below.'),
            level='INFO'
        )

        return HttpResponseRedirect(
            reverse('admin:blog_blogpost_change', args=[new_post.pk])
        )

    def get_urls(self):
        """Add custom URLs for page builder link."""
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:pk>/create-page/',
                self.admin_site.admin_view(self.create_page_view),
                name='blog_blogpost_create_page'
            ),
        ]
        return custom_urls + urls

    def create_page_view(self, request, pk):
        """Create a page builder page for this blog post."""
        obj = self.get_object(request, pk)
        if obj:
            obj.get_content_page(create=True)
            self.message_user(
                request,
                _('Page Builder page created. You can now edit the page layout.')
            )
        return HttpResponseRedirect(
            reverse('admin:blog_blogpost_change', args=[pk])
        )

    def changelist_view(self, request, extra_context=None):
        """Add extra context for the custom change list template."""
        extra_context = extra_context or {}

        # Get counts for filter tabs
        extra_context['all_count'] = BlogPost.objects.count()
        extra_context['published_count'] = BlogPost.objects.filter(status='published').count()
        extra_context['draft_count'] = BlogPost.objects.filter(status='draft').count()
        extra_context['scheduled_count'] = BlogPost.objects.filter(status='scheduled').count()
        extra_context['featured_count'] = BlogPost.objects.filter(is_featured=True).count()

        # Get categories for filter dropdown
        extra_context['categories'] = BlogCategory.objects.filter(is_active=True)

        return super().changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Add extra context for the blog post change form (stats, auto-shares)."""
        extra_context = extra_context or {}

        if object_id:
            post = self.get_object(request, object_id)
            if post:
                # Social shares count (from social_sharing app if available)
                share_count = 0
                try:
                    from django.contrib.contenttypes.models import ContentType
                    from social_sharing.models import SocialShare
                    content_type = ContentType.objects.get_for_model(BlogPost)
                    share_count = SocialShare.objects.filter(
                        content_type=content_type,
                        object_id=post.pk
                    ).count()
                except (ImportError, Exception):
                    pass
                extra_context['share_count'] = share_count

                # Notification count (subscribers notified)
                # For now, use a simple count based on notification_sent status
                notification_count = 0
                if post.notification_sent:
                    # If notification was sent, estimate based on verified subscribers
                    notification_count = BlogSubscriber.objects.filter(
                        is_active=True,
                        verification_status='verified'
                    ).count()
                extra_context['notification_count'] = notification_count

                # Auto-share statuses
                extra_context['auto_shares'] = post.auto_shares.select_related(
                    'social_account'
                ).order_by('-created_at')

                # Configured social accounts for sidebar display
                extra_context['configured_social_accounts'] = SocialConnectorAccount.objects.filter(
                    status='connected',
                    auto_share_enabled=True
                ).select_related('component')

        return super().change_view(request, object_id, form_url, extra_context)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Inject auto-save attributes for media library widgets."""
        if db_field.name in ('featured_image', 'og_image'):
            object_id = request.resolver_match.kwargs.get('object_id', '')
            return forms.ModelChoiceField(
                queryset=db_field.remote_field.model.objects.all(),
                widget=MediaLibrarySelectWidget(attrs={
                    'auto_save_url': '/api/media/auto-save/',
                    'auto_save_app': 'blog',
                    'auto_save_model': 'blogpost',
                    'auto_save_pk': object_id,
                    'auto_save_field': db_field.name,
                }),
                required=False
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        """Optimize queryset with prefetch."""
        qs = super().get_queryset(request)
        return qs.select_related(
            'category', 'featured_image', 'created_by'
        ).prefetch_related('tags')

    actions = ['make_published', 'make_draft', 'make_featured', 'remove_featured']

    def make_published(self, request, queryset):
        """Publish selected posts."""
        from django.utils import timezone
        count = queryset.update(status='published', published_at=timezone.now())
        self.message_user(request, _('%d posts published.') % count)
    make_published.short_description = _('Publish selected posts')

    def make_draft(self, request, queryset):
        """Move selected posts to draft."""
        count = queryset.update(status='draft')
        self.message_user(request, _('%d posts moved to draft.') % count)
    make_draft.short_description = _('Move to draft')

    def make_featured(self, request, queryset):
        """Mark selected posts as featured."""
        count = queryset.update(is_featured=True)
        self.message_user(request, _('%d posts marked as featured.') % count)
    make_featured.short_description = _('Mark as featured')

    def remove_featured(self, request, queryset):
        """Remove featured status from selected posts."""
        count = queryset.update(is_featured=False)
        self.message_user(request, _('%d posts removed from featured.') % count)
    remove_featured.short_description = _('Remove from featured')


# =============================================================================
# Subscriber Admin
# =============================================================================

@admin.register(BlogSubscriber)
class BlogSubscriberAdmin(admin.ModelAdmin):
    """Admin for blog subscribers."""
    change_list_template = 'admin/blog/blogsubscriber/change_list.html'
    list_display = [
        'email', 'name', 'notification_frequency', 'verification_status',
        'is_active', 'verified_at', 'created_at'
    ]
    list_filter = [
        'verification_status', 'notification_frequency', 'is_active',
        'created_at', 'verified_at'
    ]
    search_fields = ['email', 'name']
    readonly_fields = [
        'id', 'verification_token', 'verification_sent_at', 'verified_at',
        'unsubscribe_token', 'unsubscribed_at', 'last_digest_sent_at',
        'ip_address', 'user_agent', 'created_at', 'updated_at'
    ]
    filter_horizontal = ['subscribed_categories']

    fieldsets = (
        (_('Subscriber Information'), {
            'fields': ('id', 'email', 'name', 'user', 'language_code')
        }),
        (_('Preferences'), {
            'fields': ('notification_frequency', 'subscribed_categories')
        }),
        (_('Verification'), {
            'fields': (
                'verification_status', 'verification_token',
                'verification_sent_at', 'verified_at'
            )
        }),
        (_('Subscription Status'), {
            'fields': (
                'is_active', 'unsubscribe_token',
                'unsubscribed_at', 'unsubscribe_reason'
            )
        }),
        (_('Tracking'), {
            'fields': (
                'last_digest_sent_at', 'ip_address', 'user_agent',
                'created_at', 'updated_at'
            ),
            'classes': ('collapse',),
        }),
    )

    actions = ['verify_subscribers', 'send_verification_email', 'unsubscribe_selected']

    def changelist_view(self, request, extra_context=None):
        """Add extra context for the custom change list template."""
        extra_context = extra_context or {}
        extra_context['total_count'] = BlogSubscriber.objects.count()
        extra_context['verified_count'] = BlogSubscriber.objects.filter(
            verification_status='verified'
        ).count()
        extra_context['pending_count'] = BlogSubscriber.objects.filter(
            verification_status='pending'
        ).count()
        extra_context['active_count'] = BlogSubscriber.objects.filter(
            is_active=True
        ).count()
        return super().changelist_view(request, extra_context=extra_context)

    def verify_subscribers(self, request, queryset):
        """Manually verify selected subscribers."""
        count = 0
        for subscriber in queryset.filter(verification_status='pending'):
            subscriber.verify()
            count += 1
        self.message_user(request, _('%d subscribers verified.') % count)
    verify_subscribers.short_description = _('Verify selected subscribers')

    def send_verification_email(self, request, queryset):
        """Send verification email to pending subscribers."""
        from blog.tasks import send_blog_verification_email
        pending = queryset.filter(verification_status='pending')
        count = 0
        for subscriber in pending:
            send_blog_verification_email.delay(subscriber.pk)
            count += 1
        self.message_user(request, _('Verification emails queued for %d subscribers.') % count)
    send_verification_email.short_description = _('Send verification email')

    def unsubscribe_selected(self, request, queryset):
        """Unsubscribe selected subscribers."""
        count = 0
        for subscriber in queryset.filter(is_active=True):
            subscriber.unsubscribe(reason='Admin unsubscribed')
            count += 1
        self.message_user(request, _('%d subscribers unsubscribed.') % count)
    unsubscribe_selected.short_description = _('Unsubscribe selected')


# =============================================================================
# Social Connector Account Admin
# =============================================================================

@admin.register(SocialConnectorAccount)
class SocialConnectorAccountAdmin(admin.ModelAdmin):
    """Admin for social connector accounts."""
    list_display = [
        'name', 'provider_key', 'platform_account_name',
        'status', 'auto_share_enabled', 'last_successful_post_at'
    ]
    list_filter = ['status', 'provider_key', 'auto_share_enabled']
    search_fields = ['name', 'platform_account_name', 'platform_account_id']
    readonly_fields = [
        'id', 'platform_account_id', 'platform_account_name',
        'platform_account_url', 'platform_avatar_url',
        'access_token_expires_at', 'refresh_token_expires_at',
        'last_error', 'last_error_at', 'last_successful_post_at',
        'created_at', 'updated_at', 'connected_by'
    ]

    fieldsets = (
        (_('Account Information'), {
            'fields': (
                'id', 'name', 'provider_key', 'component', 'site'
            )
        }),
        (_('Platform Details'), {
            'fields': (
                'platform_account_id', 'platform_account_name',
                'platform_account_url', 'platform_avatar_url'
            )
        }),
        (_('Status'), {
            'fields': (
                'status', 'auto_share_enabled', 'is_default_for_provider',
                'last_successful_post_at'
            )
        }),
        (_('Token Status'), {
            'fields': ('access_token_expires_at', 'refresh_token_expires_at'),
            'classes': ('collapse',),
        }),
        (_('Post Template'), {
            'fields': ('post_template', 'default_hashtags'),
            'classes': ('collapse',),
        }),
        (_('Error Information'), {
            'fields': ('last_error', 'last_error_at'),
            'classes': ('collapse',),
        }),
        (_('Meta'), {
            'fields': ('connected_by', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    actions = ['refresh_tokens', 'disconnect_accounts']
    change_list_template = 'admin/blog/socialconnectoraccount/change_list.html'

    def add_view(self, request, form_url='', extra_context=None):
        """Redirect add view to the wizard."""
        return HttpResponseRedirect(reverse('blog_admin:wizard_step1'))

    def changelist_view(self, request, extra_context=None):
        """Custom changelist view with counts and provider list."""
        extra_context = extra_context or {}

        # Get counts for filter tabs
        all_accounts = SocialConnectorAccount.objects.all()
        extra_context['all_count'] = all_accounts.count()
        extra_context['connected_count'] = all_accounts.filter(
            status__in=['connected', 'active']
        ).count()
        extra_context['expired_count'] = all_accounts.filter(
            status='token_expired'
        ).count()
        extra_context['error_count'] = all_accounts.filter(
            status='error'
        ).count()

        # Get unique providers for filter dropdown
        extra_context['providers'] = all_accounts.values_list(
            'provider_key', flat=True
        ).distinct().order_by('provider_key')

        return super().changelist_view(request, extra_context)

    def refresh_tokens(self, request, queryset):
        """Attempt to refresh OAuth tokens for selected accounts."""
        from blog.tasks import _load_social_connector
        refreshed = 0
        failed = 0
        for account in queryset:
            try:
                connector = _load_social_connector(account)
                if connector and hasattr(connector, 'refresh_token'):
                    connector.refresh_token(account)
                    refreshed += 1
                else:
                    failed += 1
            except Exception:
                failed += 1
        if refreshed:
            self.message_user(request, _('Refreshed tokens for %d accounts.') % refreshed)
        if failed:
            self.message_user(request, _('Failed to refresh %d accounts (connector not available).') % failed, level='warning')
    refresh_tokens.short_description = _('Refresh OAuth tokens')

    def disconnect_accounts(self, request, queryset):
        """Disconnect selected social accounts."""
        count = queryset.update(status='disconnected')
        self.message_user(request, _('%d accounts disconnected.') % count)
    disconnect_accounts.short_description = _('Disconnect selected accounts')


# =============================================================================
# Blog Post Auto Share Admin
# =============================================================================

@admin.register(BlogPostAutoShare)
class BlogPostAutoShareAdmin(admin.ModelAdmin):
    """Admin for auto-share tracking."""
    list_display = [
        'post', 'social_account', 'status', 'scheduled_at',
        'posted_at', 'retry_count'
    ]
    list_filter = ['status', 'social_account__provider_key']
    search_fields = ['post__title', 'social_account__name']
    readonly_fields = [
        'id', 'platform_post_id', 'platform_post_url',
        'posted_at', 'posted_content', 'error_message',
        'retry_count', 'next_retry_at', 'created_at', 'updated_at'
    ]

    fieldsets = (
        (_('Post & Account'), {
            'fields': ('id', 'post', 'social_account')
        }),
        (_('Status'), {
            'fields': ('status', 'scheduled_at')
        }),
        (_('Result'), {
            'fields': (
                'platform_post_id', 'platform_post_url',
                'posted_at', 'posted_content'
            )
        }),
        (_('Retry'), {
            'fields': ('retry_count', 'max_retries', 'next_retry_at', 'error_message'),
            'classes': ('collapse',),
        }),
        (_('Meta'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    actions = ['retry_failed_shares', 'skip_selected']

    def retry_failed_shares(self, request, queryset):
        """Queue failed shares for retry."""
        count = 0
        for share in queryset.filter(status='failed'):
            if share.can_retry():
                share.status = 'pending'
                share.next_retry_at = share.calculate_next_retry()
                share.save()
                count += 1
        self.message_user(request, _('%d shares queued for retry.') % count)
    retry_failed_shares.short_description = _('Retry failed shares')

    def skip_selected(self, request, queryset):
        """Skip selected shares (won't be posted)."""
        count = queryset.exclude(status__in=['posted', 'skipped']).update(status='skipped')
        self.message_user(request, _('%d shares marked as skipped.') % count)
    skip_selected.short_description = _('Skip selected (won\'t post)')


# =============================================================================
# Blog Settings Admin (Singleton)
# =============================================================================

@admin.register(BlogSettings)
class BlogSettingsAdmin(admin.ModelAdmin):
    """Admin for blog settings (singleton)."""
    list_display = ['__str__', 'posts_per_page', 'rss_enabled', 'enable_subscriptions']

    fieldsets = (
        (_('Display Settings'), {
            'fields': (
                'posts_per_page', 'show_reading_time',
                'show_view_count', 'show_related_posts', 'related_posts_count'
            )
        }),
        (_('RSS Feed'), {
            'fields': (
                'rss_enabled', 'rss_posts_count', 'rss_include_full_content'
            )
        }),
        (_('Subscriptions'), {
            'fields': (
                'enable_subscriptions', 'require_double_opt_in', 'default_frequency'
            )
        }),
        (_('Digest Schedule (UTC)'), {
            'fields': (
                'weekly_digest_day', 'weekly_digest_hour',
                'monthly_digest_day', 'monthly_digest_hour'
            )
        }),
    )

    def has_add_permission(self, request):
        """Prevent adding new settings (singleton)."""
        return not BlogSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of settings."""
        return False

    def changelist_view(self, request, extra_context=None):
        """Redirect changelist to the singleton instance."""
        obj, created = BlogSettings.objects.get_or_create(pk=1)
        return HttpResponseRedirect(
            reverse('admin:blog_blogsettings_change', args=[obj.pk])
        )
