"""
Announcements admin configuration for Spwig eCommerce platform.

Provides admin interface for managing store announcements with
card-based list view, CKEditor rich text, media library integration,
and visibility rules.

"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import strip_tags, format_html
from django.utils import timezone
from core.admin_mixins import TranslatableAdminMixin

from .models import Announcement
from .forms import AnnouncementForm


@admin.register(Announcement)
class AnnouncementAdmin(TranslatableAdminMixin, admin.ModelAdmin):
    """Admin interface for Announcement model."""

    form = AnnouncementForm
    change_list_template = 'admin/announcements/announcement/change_list.html'
    change_form_template = 'admin/announcements/announcement/change_form.html'

    list_display = [
        'title_display', 'is_enabled', 'expiry_status',
        'link_type', 'show_modal', 'priority', 'updated_at'
    ]
    list_filter = ['is_enabled', 'link_type', 'show_modal']
    search_fields = ['title']
    # visibility_rules uses CheckboxSelectMultiple widget (see forms.py)
    list_editable = ['is_enabled', 'priority']

    translatable_fields = ['title', 'body', 'link_text']

    fieldsets = (
        (_('Content'), {
            'fields': ('title', 'body'),
        }),
        (_('Image'), {
            'fields': ('image', 'image_display_mode', 'image_overlay_opacity'),
            'classes': ('collapse',),
            'description': _('Optional image for modal display. Choose between banner (above content) or background (behind text with overlay).'),
        }),
        (_('Link'), {
            'fields': (
                'link_type',
                'product_reference', 'category_reference',
                'blog_post_reference', 'page_reference',
                'custom_url', 'link_text', 'show_modal',
            ),
        }),
        (_('Display'), {
            'fields': ('is_enabled', 'priority', 'expires_at'),
        }),
        (_('Visibility Rules'), {
            'fields': ('visibility_rules',),
            'classes': ('collapse',),
            'description': _('Optional: restrict when this announcement is shown based on advanced conditions.'),
        }),
    )

    class Media:
        css = {
            'all': [
                'core/admin/css/link_selector.css',
                'announcements/admin/css/announcements.css',
            ]
        }
        js = [
            'core/admin/js/link_selector.js',
            'announcements/admin/js/announcements_admin.js',
        ]

    def title_display(self, obj):
        """Display title with HTML stripped for list view."""
        return strip_tags(obj.title)[:80]
    title_display.short_description = _('Title')
    title_display.admin_order_field = 'title'

    def expiry_status(self, obj):
        """Show expiry status as a badge."""
        if obj.expires_at is None:
            return format_html(
                '<span class="badge">{}</span>',
                _('No expiry')
            )
        elif obj.is_expired():
            return format_html(
                '<span class="badge error">{}</span>',
                _('Expired')
            )
        else:
            return format_html(
                '<span class="badge success">{}</span>',
                _('Active')
            )
    expiry_status.short_description = _('Status')

    def get_queryset(self, request):
        qs = super().get_queryset(request).select_related(
            'image', 'product_reference', 'category_reference',
            'blog_post_reference', 'page_reference',
        )
        # Apply custom filters from tab navigation
        is_enabled = request.GET.get('is_enabled')
        expired = request.GET.get('expired')

        if is_enabled == '1':
            qs = qs.filter(is_enabled=True)
        elif is_enabled == '0':
            qs = qs.filter(is_enabled=False)

        if expired == '1':
            qs = qs.filter(expires_at__isnull=False, expires_at__lt=timezone.now())

        return qs

    def changelist_view(self, request, extra_context=None):
        """Pass filter counts for the tab navigation."""
        extra_context = extra_context or {}
        now = timezone.now()
        base_qs = Announcement.objects.all()

        extra_context['all_count'] = base_qs.count()
        extra_context['enabled_count'] = base_qs.filter(is_enabled=True).count()
        extra_context['disabled_count'] = base_qs.filter(is_enabled=False).count()
        extra_context['expired_count'] = base_qs.filter(
            expires_at__isnull=False, expires_at__lt=now
        ).count()

        return super().changelist_view(request, extra_context)
