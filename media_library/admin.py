from django.contrib import admin
from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .forms import MediaAssetForm
from .models import (
    ImageSizePreset,
    MediaAsset,
    MediaFolder,
    MediaProcessingJob,
    MediaThumbnail,
    MediaUsage,
    Tag,
)
from .services import ImageProcessor


class MediaThumbnailInline(admin.TabularInline):
    """Inline admin for thumbnails"""

    model = MediaThumbnail
    extra = 0
    readonly_fields = ("size_preset", "width", "height", "file", "webp_file", "created_at")
    can_delete = False


class MediaUsageInline(admin.TabularInline):
    """Inline admin for usage tracking"""

    model = MediaUsage
    extra = 0
    readonly_fields = ("content_type", "object_id", "field_name", "created_at")
    can_delete = False


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    """Admin interface for media assets"""

    form = MediaAssetForm
    change_form_template = "admin/media_library/mediaasset/change_form.html"
    change_list_template = "admin/media_library/mediaasset/change_list.html"

    list_display = [
        "thumbnail_preview",
        "title",
        "folder",
        "mime_type",
        "file_size_display",
        "dimensions",
        "usage_count",
        "uploaded_by",
        "created_at",
    ]
    list_filter = ["mime_type", "folder", "is_public", "created_at"]
    search_fields = ["title", "alt_text", "description", "tags__name"]
    filter_horizontal = ["tags"]
    date_hierarchy = "created_at"

    # We'll define fieldsets dynamically based on whether it's video or image
    def get_fieldsets(self, request, obj=None):
        """Return different fieldsets for images vs videos"""
        if obj and obj.is_video():
            return (
                (_("Basic Information"), {"fields": ("title", "alt_text", "description")}),
                (
                    _("Video Files"),
                    {"fields": ("original_file", "converted_video", "poster_image")},
                ),
                (
                    _("Video Details"),
                    {"fields": ("duration", "frame_rate", "bitrate", "video_codec", "audio_codec")},
                ),
                (_("Organization"), {"fields": ("folder", "tags")}),
                (
                    _("Technical Details"),
                    {
                        "fields": ("id", "file_size", "width", "height", "mime_type", "metadata"),
                    },
                ),
                (_("Permissions"), {"fields": ("uploaded_by", "is_public")}),
                (
                    _("Usage"),
                    {
                        "fields": ("usage_count", "last_used_at"),
                    },
                ),
                (
                    _("Timestamps"),
                    {
                        "fields": ("created_at", "updated_at"),
                    },
                ),
            )
        else:
            return (
                (_("Basic Information"), {"fields": ("title", "alt_text", "description")}),
                (_("Image Files"), {"fields": ("original_file", "webp_file")}),
                (_("Organization"), {"fields": ("folder", "tags")}),
                (
                    _("Technical Details"),
                    {
                        "fields": ("id", "file_size", "width", "height", "mime_type", "metadata"),
                    },
                ),
                (
                    _("Focal Point"),
                    {
                        "fields": ("focal_point_x", "focal_point_y"),
                    },
                ),
                (_("Permissions"), {"fields": ("uploaded_by", "is_public")}),
                (
                    _("Usage"),
                    {
                        "fields": ("usage_count", "last_used_at"),
                    },
                ),
                (
                    _("Timestamps"),
                    {
                        "fields": ("created_at", "updated_at"),
                    },
                ),
            )

    def get_readonly_fields(self, request, obj=None):
        """Define readonly fields"""
        readonly = [
            "id",
            "file_size",
            "width",
            "height",
            "mime_type",
            "metadata",
            "usage_count",
            "last_used_at",
            "created_at",
            "updated_at",
            "original_file",
            "webp_file",
            "uploaded_by",
        ]

        if obj and obj.is_video():
            readonly.extend(
                [
                    "converted_video",
                    "poster_image",
                    "duration",
                    "frame_rate",
                    "bitrate",
                    "video_codec",
                    "audio_codec",
                ]
            )

        return readonly

    inlines = [MediaThumbnailInline, MediaUsageInline]

    def has_add_permission(self, request):
        """Disable adding media through admin - use gallery upload instead"""
        return False

    def get_urls(self):
        """Add custom URLs for media library"""
        urls = super().get_urls()
        custom_urls = [
            path(
                "gallery/",
                self.admin_site.admin_view(self.gallery_view),
                name="media_library_gallery",
            ),
            path(
                "upload/", self.admin_site.admin_view(self.upload_view), name="media_library_upload"
            ),
            path(
                "api/search/",
                self.admin_site.admin_view(self.api_search),
                name="media_library_api_search",
            ),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        """Add note about thumbnail regeneration to changelist"""
        from django.urls import reverse

        extra_context = extra_context or {}

        # Add helpful note about thumbnail regeneration
        settings_url = reverse("admin:core_sitesettings_change", args=[1])
        extra_context["thumbnail_regen_note"] = format_html(
            '<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); '
            'padding: 15px; border-radius: 6px; margin-bottom: 20px; color: white;">'
            '<div style="font-weight: bold; margin-bottom: 8px; font-size: 14px;">'
            '<i class="fas fa-images"></i> {}</div>'
            '<div style="font-size: 13px; opacity: 0.9; margin-bottom: 10px;">{}</div>'
            '<a href="{}#images" style="background: white; color: #667eea; padding: 8px 16px; '
            "border-radius: 4px; text-decoration: none; font-weight: 600; display: inline-flex; "
            'align-items: center; gap: 6px;">'
            '<i class="fas fa-cog"></i> {}</a>'
            "</div>",
            _("Image Optimization & Thumbnails"),
            _(
                "Configure thumbnail sizes and regenerate thumbnails for all product images in Site Settings."
            ),
            settings_url,
            _("Go to Image Settings"),
        )

        # Add filter dropdown context
        from .models import MediaFolder

        extra_context["mime_types"] = MediaAsset.MIME_TYPE_CHOICES
        extra_context["folders"] = MediaFolder.objects.all().order_by("name")

        return super().changelist_view(request, extra_context=extra_context)

    def gallery_view(self, request):
        """Gallery view for selecting images"""
        context = dict(
            self.admin_site.each_context(request),
            title=_("Media Gallery"),
            media_assets=MediaAsset.objects.all(),
            folders=MediaFolder.objects.all(),
            tags=Tag.objects.all(),
        )
        return TemplateResponse(request, "admin/media_library/gallery.html", context)

    def upload_view(self, request):
        """
        Handle file uploads from the Django admin.

        This endpoint validates file uploads using MediaAssetCreateSerializer
        to ensure security (blocking HTML/SVG files, checking magic bytes, etc.)
        """
        if request.method != "POST":
            return JsonResponse({"error": "Method not allowed"}, status=405)

        from rest_framework.parsers import FormParser, MultiPartParser
        from rest_framework.request import Request

        from .serializers import MediaAssetCreateSerializer

        # Convert Django request to DRF request to use the serializer
        drf_request = Request(request, parsers=[MultiPartParser(), FormParser()])

        # Map 'file' field to 'original_file' (admin frontend uses 'file')
        data = drf_request.data.copy()
        if "file" in request.FILES:
            data["original_file"] = request.FILES["file"]

        # Add uploaded_by to track who uploaded
        if request.user.is_authenticated:
            # The serializer will handle this via perform_create
            pass

        # Validate and create using serializer (includes HTML/SVG blocking)
        serializer = MediaAssetCreateSerializer(data=data, context={"request": drf_request})

        if serializer.is_valid():
            # Save the media asset
            try:
                media_asset = serializer.save(uploaded_by=request.user)

                return JsonResponse(
                    {
                        "status": "success",
                        "id": str(media_asset.id),
                        "title": media_asset.title,
                        "url": media_asset.get_display_url(),
                        "mime_type": media_asset.mime_type,
                    },
                    status=201,
                )
            except Exception as e:
                return JsonResponse({"status": "error", "error": str(e)}, status=500)
        else:
            # Validation failed - return errors
            return JsonResponse({"status": "error", "errors": serializer.errors}, status=400)

    def api_search(self, request):
        """API endpoint for searching media"""
        from django.db import models

        query = request.GET.get("q", "")
        folder_id = request.GET.get("folder")
        tag_ids = request.GET.getlist("tags")

        assets = MediaAsset.objects.all()

        if query:
            assets = assets.filter(
                models.Q(title__icontains=query)
                | models.Q(alt_text__icontains=query)
                | models.Q(description__icontains=query)
            )

        if folder_id:
            assets = assets.filter(folder_id=folder_id)

        if tag_ids:
            assets = assets.filter(tags__id__in=tag_ids)

        data = [
            {
                "id": str(asset.id),
                "title": asset.title,
                "url": asset.get_display_url(),
                "thumbnail": asset.get_thumbnail("small") if asset.is_image() else None,
                "poster_url": asset.poster_image.url
                if asset.is_video() and asset.poster_image
                else None,
                "alt_text": asset.alt_text,
                "width": asset.width,
                "height": asset.height,
                "mime_type": asset.mime_type,
                "file_size": asset.file_size,
                "duration": asset.duration if asset.is_video() else None,
            }
            for asset in assets[:50]
        ]

        return JsonResponse({"results": data})

    def thumbnail_preview(self, obj):
        """Display thumbnail in list view"""
        if obj.webp_file:
            url = obj.webp_file.url
        elif obj.original_file:
            url = obj.original_file.url
        else:
            return "-"
        return format_html(
            '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />',
            url,
        )

    thumbnail_preview.short_description = _("Preview")

    def image_preview(self, obj):
        """Display larger preview in detail view"""
        if obj.original_file:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; border: 1px solid #ddd; border-radius: 4px;" />',
                obj.original_file.url,
            )
        return "-"

    image_preview.short_description = _("Original Preview")

    def webp_preview(self, obj):
        """Display WebP preview in detail view"""
        if obj.webp_file:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; border: 1px solid #ddd; border-radius: 4px;" />',
                obj.webp_file.url,
            )
        return "-"

    webp_preview.short_description = _("WebP Preview")

    def file_size_display(self, obj):
        """Human-readable file size"""
        size = obj.file_size
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

    file_size_display.short_description = _("Size")

    def dimensions(self, obj):
        """Display image dimensions"""
        if obj.width and obj.height:
            return f"{obj.width} × {obj.height}"
        return "-"

    dimensions.short_description = _("Dimensions")

    class Media:
        css = {
            "all": (
                "media_library/css/media-library.css",
                "media_library/css/upload-queue.css",
                "utilities/base/current/utility_base.css",
                "components/utilities/translation_editor/translation_editor.css",
            )
        }
        js = (
            "media_library/js/upload-queue.js",
            "media_library/js/media-library.js",
            "components/utilities/translation_editor/translation_editor.js",
            "media_library/js/media-translation-adapter.js",
            "media_library/js/media-asset-admin.js",
        )


@admin.register(MediaFolder)
class MediaFolderAdmin(admin.ModelAdmin):
    """Admin interface for media folders"""

    list_display = ["name", "path", "parent", "asset_count", "created_by", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["name", "path"]
    readonly_fields = ["id", "path", "created_at", "updated_at"]

    def asset_count(self, obj):
        """Count assets in folder"""
        return obj.assets.count()

    asset_count.short_description = _("Assets")

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin interface for tags"""

    list_display = ["name", "slug", "asset_count"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}

    def asset_count(self, obj):
        """Count assets with this tag"""
        return obj.assets.count()

    asset_count.short_description = _("Assets")


@admin.register(ImageSizePreset)
class ImageSizePresetAdmin(admin.ModelAdmin):
    """Admin interface for image size presets"""

    change_list_template = "admin/media_library/imagesizepreset/change_list.html"
    list_display = ["name", "dimensions", "crop_mode", "quality", "is_active", "preset_type"]
    list_filter = ["crop_mode", "is_active", "is_system_preset"]
    search_fields = ["name", "description"]

    fieldsets = (
        (_("Basic Information"), {"fields": ("name", "slug", "description")}),
        (_("Size & Quality"), {"fields": ("width", "height", "crop_mode", "quality")}),
        (_("Status"), {"fields": ("is_active", "is_system_preset")}),
    )

    def get_prepopulated_fields(self, request, obj=None):
        """Only prepopulate slug for non-system presets"""
        if obj and obj.is_system_preset:
            return {}
        return {"slug": ("name",)}

    def get_readonly_fields(self, request, obj=None):
        """Make name and slug readonly for system presets"""
        if obj and obj.is_system_preset:
            return ["name", "slug", "is_system_preset"]
        return ["is_system_preset"]

    def preset_type(self, obj):
        """Display if this is a system preset"""
        if obj.is_system_preset:
            return format_html(
                '<span style="background: var(--primary); color: white; padding: 3px 8px; '
                'border-radius: 3px; font-size: 11px; font-weight: 600;">'
                '<i class="fas fa-lock"></i> System</span>'
            )
        return format_html(
            '<span style="background: var(--body-quiet-color); color: white; padding: 3px 8px; '
            'border-radius: 3px; font-size: 11px; font-weight: 600;">Custom</span>'
        )

    preset_type.short_description = _("Type")

    def dimensions(self, obj):
        """Display dimensions"""
        return f"{obj.width} × {obj.height}"

    dimensions.short_description = _("Dimensions")

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of system presets"""
        if obj and obj.is_system_preset:
            return False
        return super().has_delete_permission(request, obj)

    def get_actions(self, request):
        """Remove delete action for system presets"""
        actions = super().get_actions(request)
        # Keep the regenerate action
        return actions

    def delete_queryset(self, request, queryset):
        """Prevent bulk deletion of system presets"""
        system_presets = queryset.filter(is_system_preset=True)
        if system_presets.exists():
            self.message_user(
                request,
                _("System presets cannot be deleted. Only custom presets were deleted."),
                level="warning",
            )
            queryset = queryset.exclude(is_system_preset=True)
        super().delete_queryset(request, queryset)

    def changelist_view(self, request, extra_context=None):
        """Add crop mode dropdown data + helpful info about system presets"""
        extra_context = extra_context or {}
        extra_context["crop_modes"] = ImageSizePreset.CROP_MODES

        extra_context["system_presets_note"] = format_html(
            '<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); '
            'padding: 15px; border-radius: 6px; margin-bottom: 20px; color: white;">'
            '<div style="font-weight: bold; margin-bottom: 8px; font-size: 14px;">'
            '<i class="fas fa-lock"></i> {}</div>'
            '<div style="font-size: 13px; opacity: 0.9;">{}</div>'
            "</div>",
            _("System Presets Protected"),
            _(
                "9 default image size presets (Thumbnail, Small, Medium, Large, Gallery, Hero, Banner, Card, Avatar) "
                "are protected system presets. You cannot delete them or change their names, but you can modify "
                "their dimensions and quality settings. You can create additional custom presets as needed."
            ),
        )

        return super().changelist_view(request, extra_context=extra_context)

    actions = ["regenerate_thumbnails"]

    def regenerate_thumbnails(self, request, queryset):
        """Regenerate thumbnails for selected presets"""
        processor = ImageProcessor()
        count = 0

        for preset in queryset:
            # Delete existing thumbnails
            MediaThumbnail.objects.filter(size_preset=preset.slug).delete()

            # Regenerate for all assets
            for asset in MediaAsset.objects.all():
                if asset.original_file:
                    asset.original_file.seek(0)
                    original_content, webp_content = processor.generate_thumbnail(
                        asset.original_file,
                        preset.width,
                        preset.height,
                        crop_mode=preset.crop_mode,
                        padding_color=getattr(preset, "padding_color", None),
                    )

                    if original_content:
                        # Determine file extension based on crop mode
                        ext = (
                            "png"
                            if preset.crop_mode == "pad"
                            and getattr(preset, "padding_color", "transparent") == "transparent"
                            else "jpg"
                        )
                        thumbnail = MediaThumbnail.objects.create(
                            media_asset=asset,
                            size_preset=preset.slug,
                            width=preset.width,
                            height=preset.height,
                        )
                        thumbnail.file.save(
                            f"{asset.id}_{preset.slug}.{ext}", original_content, save=False
                        )
                        if webp_content:
                            thumbnail.webp_file.save(
                                f"{asset.id}_{preset.slug}.webp", webp_content, save=False
                            )
                        thumbnail.save()
                        count += 1

        self.message_user(request, _("Regenerated {} thumbnails").format(count))

    regenerate_thumbnails.short_description = _("Regenerate thumbnails for selected presets")


@admin.register(MediaProcessingJob)
class MediaProcessingJobAdmin(admin.ModelAdmin):
    """Admin interface for media processing jobs"""

    list_display = [
        "filename",
        "job_type",
        "status",
        "progress_bar",
        "user",
        "created_at",
        "duration_display",
    ]
    list_filter = ["status", "job_type", "created_at"]
    search_fields = ["filename", "user__username", "error_message"]
    readonly_fields = [
        "id",
        "job_type",
        "status",
        "progress",
        "status_message",
        "filename",
        "file_size",
        "mime_type",
        "media_asset",
        "user",
        "created_at",
        "started_at",
        "completed_at",
        "duration",
        "error_message",
        "metadata",
    ]
    date_hierarchy = "created_at"

    fieldsets = (
        (
            _("Job Information"),
            {"fields": ("id", "job_type", "status", "progress", "status_message")},
        ),
        (_("File Details"), {"fields": ("filename", "file_size", "mime_type", "media_asset")}),
        (_("Timing"), {"fields": ("created_at", "started_at", "completed_at", "duration")}),
        (_("Error Details"), {"fields": ("error_message",), "classes": ("collapse",)}),
        (_("Metadata"), {"fields": ("metadata",), "classes": ("collapse",)}),
    )

    def progress_bar(self, obj):
        """Display progress as a bar"""
        # Use CSS classes instead of inline colors for theming
        status_class = (
            "completed"
            if obj.is_complete
            else "active"
            if obj.is_active
            else "failed"
            if obj.is_failed
            else "pending"
        )
        return format_html(
            '<div class="progress-bar-container" style="width: 100px; height: 20px; background: var(--hairline-color); border-radius: 3px; overflow: hidden;">'
            '<div class="progress-bar-fill progress-{}" style="width: {}%; height: 100%; transition: width 0.3s;"></div>'
            "</div>"
            "<style>"
            ".progress-completed {{ background: var(--success-fg); }}"
            ".progress-active {{ background: var(--primary); }}"
            ".progress-failed {{ background: var(--error-fg); }}"
            ".progress-pending {{ background: var(--body-quiet-color); }}"
            "</style>",
            status_class,
            obj.progress,
        )

    progress_bar.short_description = _("Progress")

    def duration_display(self, obj):
        """Display duration in human-readable format"""
        if obj.duration:
            minutes = int(obj.duration // 60)
            seconds = int(obj.duration % 60)
            if minutes > 0:
                return f"{minutes}m {seconds}s"
            return f"{seconds}s"
        return "-"

    duration_display.short_description = _("Duration")

    def has_add_permission(self, request):
        """Disable manual job creation"""
        return False

    actions = ["cancel_jobs"]

    def cancel_jobs(self, request, queryset):
        """Cancel selected jobs"""
        active_jobs = queryset.filter(
            status__in=["pending", "uploading", "processing", "converting", "generating_thumbnails"]
        )
        count = active_jobs.count()

        from django.utils import timezone

        active_jobs.update(
            status="cancelled", status_message="Cancelled by admin", completed_at=timezone.now()
        )

        self.message_user(request, _("Cancelled {} active job(s)").format(count))

    cancel_jobs.short_description = _("Cancel selected jobs")
