from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import InstalledModel, TranslationMeta, TranslationProvider, TranslationProviderAccount


def _is_shared_fleet():
    """Check if this is a shared fleet hosted installation."""
    from core.license import get_license_manager

    return get_license_manager().is_shared_fleet()


def _is_hosted():
    """Check if this is any Spwig-hosted installation."""
    from core.license import get_license_manager

    return get_license_manager().is_spwig_hosted()


@admin.register(TranslationProvider)
class TranslationProviderAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "provider_type",
        "is_active",
        "is_default",
        "priority",
        "total_translations",
        "last_used_at",
    ]
    list_filter = ["provider_type", "is_active", "is_default"]
    search_fields = ["name", "api_endpoint"]
    readonly_fields = [
        "total_translations",
        "total_characters",
        "total_errors",
        "last_used_at",
        "created_at",
        "updated_at",
    ]

    fieldsets = (
        (
            _("Basic Information"),
            {"fields": ("name", "provider_type", "is_active", "is_default", "priority")},
        ),
        (
            _("API Configuration"),
            {
                "fields": ("api_endpoint", "api_key", "api_secret"),
                "classes": ("collapse",),
                "description": _("Configuration for external translation providers"),
            },
        ),
        (
            _("Language Mapping"),
            {
                "fields": ("language_code_mapping",),
                "classes": ("collapse",),
                "description": _("Map internal language codes to provider-specific codes"),
            },
        ),
        (
            _("Limits & Performance"),
            {"fields": ("max_chars_per_request", "rate_limit", "timeout_seconds")},
        ),
        (
            _("Statistics"),
            {
                "fields": (
                    "total_translations",
                    "total_characters",
                    "total_errors",
                    "last_used_at",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    actions = ["mark_as_default", "activate_providers", "deactivate_providers"]

    def has_module_permission(self, request):
        """Hide from admin index for shared fleet (translator managed by Spwig)."""
        if _is_shared_fleet():
            return False
        return super().has_module_permission(request)

    def has_change_permission(self, request, obj=None):
        """Make read-only for all hosted installations (local provider is pre-configured)."""
        if _is_hosted():
            return False
        return super().has_change_permission(request, obj)

    def has_add_permission(self, request):
        """Prevent adding providers on hosted installations."""
        if _is_hosted():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        """Prevent deleting providers on hosted installations."""
        if _is_hosted():
            return False
        return super().has_delete_permission(request, obj)

    def mark_as_default(self, request, queryset):
        if queryset.count() > 1:
            self.message_user(
                request, _("Please select only one provider to set as default"), level="error"
            )
            return

        provider = queryset.first()
        provider.is_default = True
        provider.save()
        self.message_user(
            request,
            _("%(provider)s has been set as the default provider") % {"provider": provider.name},
        )

    mark_as_default.short_description = _("Set as default provider")

    def activate_providers(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, _("%(count)d provider(s) activated") % {"count": updated})

    activate_providers.short_description = _("Activate selected providers")

    def deactivate_providers(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, _("%(count)d provider(s) deactivated") % {"count": updated})

    deactivate_providers.short_description = _("Deactivate selected providers")


@admin.register(TranslationProviderAccount)
class TranslationProviderAccountAdmin(admin.ModelAdmin):
    list_display = [
        "display_name",
        "component",
        "is_active",
        "is_default",
        "connection_status",
        "total_translations",
        "last_used_at",
    ]
    list_filter = ["is_active", "is_default", "connection_status"]
    search_fields = ["display_name", "component__name"]
    readonly_fields = [
        "id",
        "connection_status",
        "connection_error",
        "last_tested_at",
        "total_translations",
        "total_characters",
        "total_errors",
        "last_used_at",
        "created_at",
        "updated_at",
    ]

    fieldsets = (
        (_("Account"), {"fields": ("id", "component", "user", "display_name")}),
        (_("Status"), {"fields": ("is_active", "is_default", "priority")}),
        (
            _("Connection"),
            {
                "fields": ("connection_status", "connection_error", "last_tested_at"),
                "classes": ("collapse",),
            },
        ),
        (
            _("Metrics"),
            {
                "fields": (
                    "total_translations",
                    "total_characters",
                    "total_errors",
                    "last_used_at",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )


# TranslationJob admin is now managed through a custom interface
# Access it at: /admin/translations/jobs/
# The old Django admin is disabled to avoid confusion and provide a better user experience
#
# @admin.register(TranslationJob)
# class TranslationJobAdmin(admin.ModelAdmin):
#     """
#     This admin interface has been replaced with a modern custom interface.
#     Access the new Translation Jobs management at: /admin/translations/jobs/
#
#     The new interface provides:
#     - Real-time job status updates with auto-refresh
#     - Modern tabbed interface (Queue, Processing, Completed, Failed)
#     - Bulk operations support
#     - Better filtering and sorting
#     - Progress tracking with live updates
#     - API endpoints for programmatic access
#     - Priority-based job scheduling
#     - Detailed job analytics
#     """
#     pass


@admin.register(TranslationMeta)
class TranslationMetaAdmin(admin.ModelAdmin):
    list_display = [
        "content_type",
        "object_id",
        "field_name",
        "language",
        "is_locked",
        "is_reviewed",
        "translated_at",
    ]
    list_filter = ["language", "is_locked", "is_reviewed", "content_type"]
    search_fields = ["content_type", "object_id", "field_name"]
    readonly_fields = ["source_checksum", "translated_at", "created_at", "updated_at"]

    fieldsets = (
        (
            _("Content Reference"),
            {"fields": ("content_type", "object_id", "field_name", "language")},
        ),
        (_("Lock Status"), {"fields": ("is_locked", "locked_by", "locked_at")}),
        (
            _("Translation Information"),
            {
                "fields": (
                    "source_checksum",
                    "translation_provider",
                    "translated_at",
                    "translated_by",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Quality Control"),
            {
                "fields": ("confidence_score", "is_reviewed", "reviewed_by", "reviewed_at"),
                "classes": ("collapse",),
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    actions = ["lock_translations", "unlock_translations", "mark_as_reviewed"]

    def lock_translations(self, request, queryset):
        count = queryset.update(is_locked=True, locked_by=request.user, locked_at=timezone.now())
        self.message_user(request, _("%(count)d translation(s) locked") % {"count": count})

    lock_translations.short_description = _("Lock selected translations")

    def unlock_translations(self, request, queryset):
        count = queryset.update(is_locked=False, locked_by=None, locked_at=None)
        self.message_user(request, _("%(count)d translation(s) unlocked") % {"count": count})

    unlock_translations.short_description = _("Unlock selected translations")

    def mark_as_reviewed(self, request, queryset):
        count = queryset.update(
            is_reviewed=True, reviewed_by=request.user, reviewed_at=timezone.now()
        )
        self.message_user(
            request, _("%(count)d translation(s) marked as reviewed") % {"count": count}
        )

    mark_as_reviewed.short_description = _("Mark as reviewed")


@admin.register(InstalledModel)
class InstalledModelAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "version",
        "model_type",
        "size_mb",
        "is_active",
        "is_downloaded",
        "download_progress_bar",
    ]
    list_filter = ["model_type", "is_active", "is_downloaded", "device"]
    search_fields = ["name", "version"]
    readonly_fields = ["total_translations", "avg_latency_ms", "installed_at", "last_used_at"]

    def has_module_permission(self, request):
        """Hide from admin index for shared fleet (models managed by Spwig)."""
        if _is_shared_fleet():
            return False
        return super().has_module_permission(request)

    def has_change_permission(self, request, obj=None):
        """Make read-only for all hosted installations."""
        if _is_hosted():
            return False
        return super().has_change_permission(request, obj)

    def has_add_permission(self, request):
        if _is_hosted():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        if _is_hosted():
            return False
        return super().has_delete_permission(request, obj)

    fieldsets = (
        (_("Model Information"), {"fields": ("name", "version", "model_type")}),
        (_("Language Support"), {"fields": ("source_languages", "target_languages")}),
        (_("Storage"), {"fields": ("file_path", "size_mb")}),
        (_("Performance Settings"), {"fields": ("compute_type", "device")}),
        (_("Status"), {"fields": ("is_active", "is_downloaded", "download_progress")}),
        (
            _("Metrics"),
            {
                "fields": ("total_translations", "avg_latency_ms"),
                "classes": ("collapse",),
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": ("installed_at", "last_used_at"),
                "classes": ("collapse",),
            },
        ),
    )

    actions = ["activate_models", "deactivate_models", "download_models"]

    class Media:
        css = {"all": ("translations/admin/css/translations.css",)}
        js = ("translations/admin/js/admin-list-init.js",)

    def download_progress_bar(self, obj):
        if obj.is_downloaded:
            state_class = "dl-progress--complete"
            text = _("Downloaded")
        elif obj.download_progress > 0:
            state_class = "dl-progress--active"
            text = f"{obj.download_progress}%"
        else:
            state_class = "dl-progress--empty"
            text = _("Not downloaded")

        width = obj.download_progress if obj.download_progress > 0 else 100

        return format_html(
            '<div class="dl-progress-bar">'
            '<div class="dl-progress-fill {}" data-width="{}">'
            "{}</div></div>",
            state_class,
            width,
            text,
        )

    download_progress_bar.short_description = _("Download Status")

    def activate_models(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, _("%(count)d model(s) activated") % {"count": count})

    activate_models.short_description = _("Activate selected models")

    def deactivate_models(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, _("%(count)d model(s) deactivated") % {"count": count})

    deactivate_models.short_description = _("Deactivate selected models")

    def download_models(self, request, queryset):
        # This would trigger actual download logic
        self.message_user(
            request, _("Download initiated for %(count)d model(s)") % {"count": queryset.count()}
        )

    download_models.short_description = _("Download selected models")
