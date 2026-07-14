from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import (
    ClipartAsset,
    ClipartCategory,
    CustomFont,
    DesignSnapshot,
    DesignTemplate,
    ProductDesignConfig,
    ProductSurface,
    SavedDesign,
)

# ─── Inlines ────────────────────────────────────────────────────────────────


class ProductSurfaceInline(admin.TabularInline):
    model = ProductSurface
    extra = 0
    fields = ("name", "slug", "sort_order", "dimension_unit", "width", "height", "is_enabled")
    prepopulated_fields = {"slug": ("name",)}


class DesignTemplateInline(admin.TabularInline):
    model = DesignTemplate
    extra = 0
    fields = ("name", "slug", "category", "sort_order", "is_active")
    prepopulated_fields = {"slug": ("name",)}


# ─── Product Design Config ──────────────────────────────────────────────────


@admin.register(ProductDesignConfig)
class ProductDesignConfigAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "editor_mode",
        "is_enabled",
        "surface_count",
        "template_count",
        "updated_at",
    )
    list_filter = ("is_enabled", "editor_mode")
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("product",)
    inlines = [ProductSurfaceInline, DesignTemplateInline]

    fieldsets = (
        (
            None,
            {
                "fields": ("product", "is_enabled", "editor_mode"),
            },
        ),
        (
            _("Feature Toggles"),
            {
                "fields": ("allow_text", "allow_image_upload", "allow_clipart"),
            },
        ),
        (
            _("Upload Restrictions"),
            {
                "fields": ("max_uploads_per_surface", "max_upload_size_mb", "allowed_upload_types"),
            },
        ),
        (
            _("Pricing"),
            {
                "fields": ("base_design_fee", "per_surface_fee", "per_upload_fee", "per_text_fee"),
            },
        ),
        (
            _("Timestamps"),
            {
                "classes": ("collapse",),
                "fields": ("created_at", "updated_at"),
            },
        ),
    )

    def surface_count(self, obj):
        return obj.surfaces.count()

    surface_count.short_description = _("Surfaces")

    def template_count(self, obj):
        return obj.templates.count()

    template_count.short_description = _("Templates")


# ─── Clipart ─────────────────────────────────────────────────────────────────


class ClipartAssetInline(admin.TabularInline):
    model = ClipartAsset
    extra = 0
    fields = ("name", "media_asset", "scope", "product", "sort_order", "is_active")
    autocomplete_fields = ("media_asset", "product")


@admin.register(ClipartCategory)
class ClipartCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "asset_count", "sort_order", "is_active")
    list_filter = ("is_active",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    inlines = [ClipartAssetInline]

    def asset_count(self, obj):
        return obj.assets.count()

    asset_count.short_description = _("Assets")


@admin.register(ClipartAsset)
class ClipartAssetAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "scope", "thumbnail_preview", "sort_order", "is_active")
    list_filter = ("is_active", "scope", "category")
    search_fields = ("name", "tags")
    autocomplete_fields = ("category", "media_asset", "product")

    def thumbnail_preview(self, obj):
        if obj.media_asset and obj.media_asset.original_file:
            return format_html(
                '<img src="{}" style="max-width: 48px; max-height: 48px; object-fit: contain;" />',
                obj.media_asset.original_file.url,
            )
        return "-"

    thumbnail_preview.short_description = _("Preview")


# ─── Custom Fonts ────────────────────────────────────────────────────────────


@admin.register(CustomFont)
class CustomFontAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "family",
        "is_system_font",
        "has_regular",
        "has_bold",
        "sort_order",
        "is_active",
    )
    list_filter = ("is_active", "is_system_font")
    search_fields = ("name", "family")
    autocomplete_fields = ("regular", "bold", "italic", "bold_italic")

    fieldsets = (
        (
            None,
            {
                "fields": ("name", "family", "is_system_font", "is_active", "sort_order"),
            },
        ),
        (
            _("Font Files"),
            {
                "description": _(
                    "Upload WOFF2 or TTF font files. At minimum, a Regular weight is needed for custom fonts."
                ),
                "fields": ("regular", "bold", "italic", "bold_italic"),
            },
        ),
    )

    def has_regular(self, obj):
        return bool(obj.regular_id) or obj.is_system_font

    has_regular.boolean = True
    has_regular.short_description = _("Regular")

    def has_bold(self, obj):
        return bool(obj.bold_id)

    has_bold.boolean = True
    has_bold.short_description = _("Bold")


# ─── Saved Designs (read-only for admin) ─────────────────────────────────────


@admin.register(SavedDesign)
class SavedDesignAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "product", "created_at", "updated_at")
    list_filter = ("created_at",)
    search_fields = ("name", "user__username", "product__name")
    readonly_fields = (
        "user",
        "product",
        "name",
        "design_data",
        "thumbnails",
        "created_at",
        "updated_at",
    )

    def has_add_permission(self, request):
        return False


# ─── Design Snapshots (read-only for admin) ──────────────────────────────────


@admin.register(DesignSnapshot)
class DesignSnapshotAdmin(admin.ModelAdmin):
    list_display = ("order_item", "is_rendered", "render_completed_at", "created_at")
    list_filter = ("is_rendered",)
    readonly_fields = (
        "order_item",
        "design_data",
        "rendered_images",
        "fulfillment_files",
        "is_rendered",
        "render_completed_at",
        "created_at",
    )

    def has_add_permission(self, request):
        return False
