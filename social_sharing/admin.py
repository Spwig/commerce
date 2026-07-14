"""
Social Sharing Admin

Admin interface for viewing and analyzing social media shares.
"""

from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from social_sharing.models import ShareCount, SocialShare
from social_sharing.settings_models import SocialSharingSettings


@admin.register(SocialShare)
class SocialShareAdmin(admin.ModelAdmin):
    """Admin interface for individual social shares"""

    list_display = [
        "id",
        "platform_badge",
        "content_info",
        "user_info",
        "device_type",
        "shared_at",
    ]

    list_filter = [
        "platform",
        "device_type",
        "shared_at",
        "content_type",
    ]

    search_fields = [
        "shared_url",
        "user__email",
        "user__username",
        "session_id",
        "ip_address",
    ]

    readonly_fields = [
        "content_type",
        "object_id",
        "content_object",
        "shared_at",
        "created_at",
    ]

    date_hierarchy = "shared_at"

    list_per_page = 50

    class Media:
        css = {"all": ("social_sharing/css/admin-shares.css",)}

    def platform_badge(self, obj):
        """Display platform with colored badge"""
        return format_html(
            '<span class="social-admin-platform-badge platform-{}">{}</span>',
            obj.platform,
            obj.get_platform_display(),
        )

    platform_badge.short_description = _("Platform")

    def content_info(self, obj):
        """Display content type and link"""
        if obj.content_object:
            return format_html("{}: {}", obj.content_type.model, str(obj.content_object)[:50])
        return format_html("{} #{}", obj.content_type.model, obj.object_id)

    content_info.short_description = _("Shared Content")

    def user_info(self, obj):
        """Display user or anonymous"""
        if obj.user:
            return format_html(
                '<a href="{}">{}</a>',
                reverse("admin:auth_user_change", args=[obj.user.pk]),
                obj.user.email or obj.user.username,
            )
        return format_html('<span class="social-admin-anonymous">{}</span>', _("Anonymous"))

    user_info.short_description = _("User")

    def has_add_permission(self, request):
        """Disable manual share creation - shares come from API"""
        return False

    def has_change_permission(self, request, obj=None):
        """Disable editing shares - they're audit records"""
        return False

    def changelist_view(self, request, extra_context=None):
        """Override to add custom context for AJAX filtering"""
        extra_context = extra_context or {}

        # Get all content types that have shares
        content_types = ContentType.objects.filter(
            id__in=SocialShare.objects.values_list("content_type_id", flat=True).distinct()
        ).order_by("model")

        # Get shares for initial display
        shares = SocialShare.objects.select_related("user", "content_type").order_by("-shared_at")[
            :50
        ]  # Limit initial display to 50 most recent

        extra_context["content_types"] = content_types
        extra_context["shares"] = shares

        return super().changelist_view(request, extra_context)


@admin.register(ShareCount)
class ShareCountAdmin(admin.ModelAdmin):
    """Admin interface for aggregated share counts"""

    change_list_template = "admin/social_sharing/sharecount/change_list.html"

    list_display = [
        "id",
        "content_info",
        "platform_badge",
        "count_display",
        "last_updated",
    ]

    list_filter = [
        "platform",
        "content_type",
    ]

    search_fields = [
        "object_id",
    ]

    readonly_fields = [
        "content_type",
        "object_id",
        "content_object",
        "platform",
        "count",
        "last_updated",
        "created_at",
    ]

    list_per_page = 50

    class Media:
        css = {"all": ("social_sharing/css/admin-shares.css",)}

    def platform_badge(self, obj):
        """Display platform with colored badge"""
        return format_html(
            '<span class="social-admin-platform-badge platform-{}">{}</span>',
            obj.platform,
            obj.get_platform_display(),
        )

    platform_badge.short_description = _("Platform")

    def content_info(self, obj):
        """Display content type and link"""
        if obj.content_object:
            return format_html("{}: {}", obj.content_type.model, str(obj.content_object)[:50])
        return format_html("{} #{}", obj.content_type.model, obj.object_id)

    content_info.short_description = _("Content")

    def count_display(self, obj):
        """Display count with formatting"""
        css = (
            "social-admin-count-high"
            if obj.count > 1000
            else ("social-admin-count-medium" if obj.count > 100 else "social-admin-count-normal")
        )
        return format_html('<span class="{}">{}</span>', css, f"{obj.count:,}")

    count_display.short_description = _("Share Count")

    def has_add_permission(self, request):
        """Disable manual count creation - counts are auto-generated"""
        return False

    def has_change_permission(self, request, obj=None):
        """Disable editing counts - they're auto-calculated"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Disable deleting counts - they're managed by signals"""
        return False

    def changelist_view(self, request, extra_context=None):
        """Override to add custom context for AJAX filtering"""
        extra_context = extra_context or {}

        # Get all content types that have share counts
        content_types = ContentType.objects.filter(
            id__in=ShareCount.objects.values_list("content_type_id", flat=True).distinct()
        ).order_by("model")

        # Get share counts for initial display
        sharecounts = ShareCount.objects.select_related("content_type").order_by(
            "-count", "-last_updated"
        )[:50]  # Top 50 by count

        extra_context["content_types"] = content_types
        extra_context["sharecounts"] = sharecounts

        return super().changelist_view(request, extra_context)


@admin.register(SocialSharingSettings)
class SocialSharingSettingsAdmin(admin.ModelAdmin):
    """Admin interface for social sharing settings (singleton)"""

    from social_sharing.forms import SocialSharingSettingsForm

    form = SocialSharingSettingsForm

    def has_add_permission(self, request):
        """Only allow one settings instance"""
        return not SocialSharingSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of settings"""
        return False

    def changelist_view(self, request, extra_context=None):
        """Redirect changelist to the singleton instance."""
        from django.shortcuts import redirect
        from django.urls import reverse

        obj, created = SocialSharingSettings.objects.get_or_create(pk=1)
        return redirect(reverse("admin:social_sharing_socialsharingsettings_change", args=[obj.pk]))

    fieldsets = (
        (
            _("Placement"),
            {
                "fields": (
                    "enable_on_products",
                    "enable_on_categories",
                    "enable_on_blog_posts",
                    "enable_on_pages",
                    "placement_position",
                ),
                "description": _("Configure where social share buttons appear automatically"),
            },
        ),
        (
            _("Appearance"),
            {
                "fields": (
                    "enabled_platforms",
                    "button_style",
                    "button_size",
                    "layout_direction",
                    "show_title",
                    "mobile_visibility",
                ),
            },
        ),
        (
            _("Tracking"),
            {
                "fields": (
                    "show_counts",
                    "track_shares",
                ),
            },
        ),
        (
            _("Metadata"),
            {
                "fields": (
                    "updated_at",
                    "updated_by",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    readonly_fields = ("updated_at", "updated_by")

    def save_model(self, request, obj, form, change):
        """Set updated_by field"""
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
