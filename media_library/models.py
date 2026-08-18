import os
import uuid
from datetime import datetime

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from core.models import SoftDeleteModel


def media_upload_path(instance, filename):
    """Generate upload path for media files"""
    ext = os.path.splitext(filename)[1]
    # Use UUID for filename to avoid conflicts
    new_filename = f"{instance.id}{ext}"
    # Organize by year/month
    date_path = datetime.now().strftime("%Y/%m")
    return f"media_library/{date_path}/{new_filename}"


def thumbnail_upload_path(instance, filename):
    """Generate upload path for thumbnail files"""
    ext = os.path.splitext(filename)[1]
    # Include size preset in filename
    new_filename = f"{instance.media_asset.id}_{instance.size_preset}{ext}"
    date_path = datetime.now().strftime("%Y/%m")
    return f"media_library/thumbnails/{date_path}/{new_filename}"


class MediaFolder(models.Model):
    """Organize media assets into folders"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    path = models.CharField(max_length=500, unique=True, editable=False)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["path"]

    def __str__(self):
        return self.path or self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        # Build path from parent
        if self.parent:
            self.path = f"{self.parent.path}/{self.slug}"
        else:
            self.path = self.slug

        super().save(*args, **kwargs)


class Tag(models.Model):
    """Tags for categorizing media assets"""

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class MediaAsset(SoftDeleteModel):
    """Core media asset model for images and videos"""

    MIME_TYPE_CHOICES = [
        ("image/jpeg", "JPEG"),
        ("image/png", "PNG"),
        ("image/gif", "GIF"),
        ("image/webp", "WebP"),
        ("image/avif", "AVIF"),
        ("image/svg+xml", "SVG"),
        ("video/mp4", "MP4"),
        ("video/webm", "WebM"),
        ("video/quicktime", "MOV"),
        ("video/x-matroska", "MKV"),
        ("video/x-msvideo", "AVI"),
        ("model/gltf-binary", "GLB"),
        ("model/gltf+json", "glTF"),
        ("image/hdr", "HDR"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    alt_text = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    # Import tracking
    external_id = models.CharField(
        max_length=100,
        blank=True,
        db_index=True,
        help_text="Original media ID from source platform",
    )
    migration_job = models.ForeignKey(
        "migration.MigrationJob",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="imported_media",
        help_text="Migration job that imported this media asset",
    )

    # Files
    original_file = models.FileField(
        upload_to=media_upload_path, help_text=_("Original uploaded file")
    )
    webp_file = models.FileField(
        upload_to=media_upload_path, blank=True, null=True, help_text=_("WebP version of the image")
    )
    avif_file = models.FileField(
        upload_to=media_upload_path,
        blank=True,
        null=True,
        help_text=_("AVIF version of the image"),
    )

    # Video-specific fields
    converted_video = models.FileField(
        upload_to=media_upload_path,
        blank=True,
        null=True,
        help_text=_("Optimized/converted video file"),
    )
    poster_image = models.ImageField(
        upload_to=media_upload_path,
        blank=True,
        null=True,
        help_text=_("Video poster/thumbnail image"),
    )
    duration = models.FloatField(null=True, blank=True, help_text=_("Video duration in seconds"))
    frame_rate = models.FloatField(null=True, blank=True, help_text=_("Video frame rate (fps)"))
    bitrate = models.IntegerField(null=True, blank=True, help_text=_("Video bitrate in bits/sec"))
    video_codec = models.CharField(
        max_length=50, blank=True, help_text=_("Video codec (e.g., h264, av1, vp9)")
    )
    audio_codec = models.CharField(
        max_length=50, blank=True, help_text=_("Audio codec (e.g., aac, opus, vorbis)")
    )

    # Technical metadata
    file_size = models.PositiveIntegerField()
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    mime_type = models.CharField(max_length=50, choices=MIME_TYPE_CHOICES)

    # Organization
    folder = models.ForeignKey(
        MediaFolder, on_delete=models.SET_NULL, null=True, blank=True, related_name="assets"
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="assets")

    # Extended metadata
    metadata = models.JSONField(
        default=dict, blank=True, help_text=_("EXIF data and other metadata")
    )

    # Translations for multilingual fields
    translations = models.JSONField(
        default=dict, blank=True, help_text=_("Translations for title, alt_text, and description")
    )
    focal_point_x = models.FloatField(
        default=0.5,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text=_("X coordinate of focal point (0-1)"),
    )
    focal_point_y = models.FloatField(
        default=0.5,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text=_("Y coordinate of focal point (0-1)"),
    )

    # Permissions
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_public = models.BooleanField(default=True)

    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # Usage tracking
    usage_count = models.PositiveIntegerField(default=0, editable=False)
    last_used_at = models.DateTimeField(null=True, blank=True, editable=False)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["mime_type"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return self.title

    def is_video(self):
        """Check if this asset is a video file"""
        return self.mime_type.startswith("video/")

    def is_image(self):
        """Check if this asset is an image file"""
        return self.mime_type.startswith("image/")

    def is_3d_model(self):
        """Check if this asset is a 3D model file (GLB/glTF)"""
        return self.mime_type.startswith("model/")

    def get_display_url(self):
        """Get the best URL for display (WebP for images, converted for videos)"""
        if self.is_video():
            if self.converted_video:
                return self.converted_video.url
            return self.original_file.url
        else:
            if self.webp_file:
                return self.webp_file.url
            return self.original_file.url

    def get_thumbnail(self, size_preset):
        """Get thumbnail for specific size preset"""
        # For videos and 3D models, return poster image if available
        if self.is_video() or self.is_3d_model():
            if self.poster_image:
                return self.poster_image.url
            return None

        # For images, look for thumbnails. When the ``thumbnails`` relation was
        # prefetched (list views), read from the prefetch cache instead of
        # issuing a per-asset ``.get()`` query — a ``.get(size_preset=…)`` never
        # uses the cache, which reintroduces an N+1 in card/list rendering.
        cache = getattr(self, "_prefetched_objects_cache", None)
        if cache is not None and "thumbnails" in cache:
            thumbnail = next((t for t in cache["thumbnails"] if t.size_preset == size_preset), None)
            if thumbnail is None:
                return self.get_display_url()
            return thumbnail.webp_file.url if thumbnail.webp_file else thumbnail.file.url

        try:
            thumbnail = self.thumbnails.get(size_preset=size_preset)
            if thumbnail.webp_file:
                return thumbnail.webp_file.url
            return thumbnail.file.url
        except MediaThumbnail.DoesNotExist:
            return self.get_display_url()

    def get_picture_sources(self, size_preset=None):
        """Return a responsive source set for a <picture>.

        Shape: ``{avif, webp, fallback, width, height, avif_srcset,
        webp_srcset, fallback_srcset}``.

        ``avif``/``webp`` are the single-URL, next-gen candidates (None when
        that rendition isn't generated yet — callers omit the matching
        <source>); ``fallback`` is always a usable original-format URL for the
        <img>. ``width``/``height`` are the intrinsic size of that base
        rendition.

        The ``*_srcset`` values are additive, backwards-compatible ``"url Nw,
        url Nw"`` width-ladder strings — one per format — assembled from the
        asset's already-generated preset thumbnails plus the full-size file, so
        a headless client can pair them with a ``sizes`` hint and let the
        browser fetch the right width instead of always downloading the largest
        file. Each is None when fewer than two same-aspect widths exist for that
        format (a single-entry srcset carries no benefit). Only renditions
        sharing the base rendition's aspect ratio are laddered together, so the
        ``w`` descriptors stay valid (a square-cropped thumbnail is never mixed
        into a wide image's ladder).

        A <source>/srcset entry is only ever emitted for a file known to
        exist — never guess a URL by swapping extensions, because a 404
        candidate renders a broken image with no fallback.
        """
        # Video / 3D: only a poster still image, no avif/webp candidates.
        if self.is_video() or self.is_3d_model():
            poster = self.poster_image.url if self.poster_image else None
            return self._picture_dict(None, None, poster, self.width, self.height)
        # SVG is vector — serve as-is, no raster renditions.
        if self.mime_type == "image/svg+xml":
            fallback = self.original_file.url if self.original_file else None
            return self._picture_dict(None, None, fallback, self.width, self.height)

        thumbs = self._thumbnails_for_srcset()

        base = None
        if size_preset:
            base = next((t for t in thumbs if t.size_preset == size_preset), None)

        if base is not None:
            sources = {
                "avif": base.avif_file.url if base.avif_file else None,
                "webp": base.webp_file.url if base.webp_file else None,
                "fallback": (base.file.url if base.file else None) or self.get_display_url(),
                "width": base.width,
                "height": base.height,
            }
        else:
            sources = {
                "avif": self.avif_file.url if self.avif_file else None,
                "webp": self.webp_file.url if self.webp_file else None,
                "fallback": self.original_file.url if self.original_file else None,
                "width": self.width,
                "height": self.height,
            }

        sources.update(self._build_srcsets(sources["width"], sources["height"], thumbs))
        return sources

    @staticmethod
    def _picture_dict(avif, webp, fallback, width, height):
        """Assemble a source dict with the full (srcset-less) key shape."""
        return {
            "avif": avif,
            "webp": webp,
            "fallback": fallback,
            "width": width,
            "height": height,
            "avif_srcset": None,
            "webp_srcset": None,
            "fallback_srcset": None,
        }

    def _thumbnails_for_srcset(self):
        """All thumbnail rows for this asset, prefetch-aware and memoised.

        Reads the ``thumbnails`` prefetch cache when present (list/detail views
        that ``prefetch_related('...media_asset__thumbnails')`` pay zero extra
        queries). Otherwise it issues a single ``.all()`` and caches it on the
        instance, so repeated ``get_picture_sources`` calls for one asset in a
        single request don't re-query.
        """
        cache = getattr(self, "_prefetched_objects_cache", None)
        if cache is not None and "thumbnails" in cache:
            return list(cache["thumbnails"])
        if "_srcset_thumbs" not in self.__dict__:
            self.__dict__["_srcset_thumbs"] = list(self.thumbnails.all())
        return self.__dict__["_srcset_thumbs"]

    def _build_srcsets(self, base_width, base_height, thumbs):
        """Build the per-format ``*_srcset`` width ladders.

        Candidates are the thumbnails plus the full-size file, restricted to
        those sharing the base rendition's aspect ratio (within 2%) so the
        emitted ``w`` descriptors describe the same image at different sizes.
        """
        empty = {"avif_srcset": None, "webp_srcset": None, "fallback_srcset": None}
        if not base_width or not base_height:
            return empty
        ref_ar = base_width / base_height
        tolerance = 0.02 * ref_ar

        # (width, avif_url, webp_url, fallback_url) per same-aspect rendition.
        candidates = []
        for t in thumbs:
            if not t.width or not t.height:
                continue
            if abs((t.width / t.height) - ref_ar) > tolerance:
                continue
            candidates.append(
                (
                    t.width,
                    t.avif_file.url if t.avif_file else None,
                    t.webp_file.url if t.webp_file else None,
                    t.file.url if t.file else None,
                )
            )
        # Full-size file caps the ladder when it shares the base aspect ratio.
        if self.width and self.height and abs((self.width / self.height) - ref_ar) <= tolerance:
            candidates.append(
                (
                    self.width,
                    self.avif_file.url if self.avif_file else None,
                    self.webp_file.url if self.webp_file else None,
                    self.original_file.url if self.original_file else None,
                )
            )

        return {
            "avif_srcset": self._srcset_string(candidates, 1),
            "webp_srcset": self._srcset_string(candidates, 2),
            "fallback_srcset": self._srcset_string(candidates, 3),
        }

    @staticmethod
    def _srcset_string(candidates, url_index):
        """Join ``candidates`` into a ``"url Nw, ..."`` string for one format.

        Dedupes by width (first candidate at a given width wins), sorts
        ascending, and returns None when fewer than two widths carry that
        format — a one-entry srcset gives the browser nothing to choose.
        """
        by_width = {}
        for candidate in candidates:
            width = candidate[0]
            url = candidate[url_index]
            if url and width and width not in by_width:
                by_width[width] = url
        if len(by_width) < 2:
            return None
        return ", ".join(f"{by_width[width]} {width}w" for width in sorted(by_width))

    @classmethod
    def resolve_from_url(cls, url):
        """Best-effort resolution of a stored media URL back to its MediaAsset.

        Page-builder elements store a plain image URL (no asset id); this maps
        that URL to the owning asset so its AVIF/WebP siblings can be served in
        a <picture>. Returns None for external or unrecognised URLs. Callers
        should cache the derived source set — this does one DB query per miss.
        """
        import os
        from urllib.parse import urlparse

        if not url or not isinstance(url, str):
            return None
        filename = os.path.basename(urlparse(url).path)
        if not filename:
            return None
        return cls.objects.filter(
            models.Q(original_file__icontains=filename)
            | models.Q(webp_file__icontains=filename)
            | models.Q(avif_file__icontains=filename)
        ).first()

    @property
    def thumbnail_small(self):
        """Get small thumbnail (300x300) for gallery/list views"""
        return self.get_thumbnail("small")

    @property
    def thumbnail_medium(self):
        """Get medium thumbnail (600x600) for larger displays"""
        return self.get_thumbnail("medium")

    @property
    def aspect_ratio(self):
        """Calculate aspect ratio"""
        if self.height > 0:
            return self.width / self.height
        return 1

    def get_translated_field(self, field_name, language_code=None):
        """Get translated value for a specific field with fallback logic."""
        from django.utils import translation

        if not language_code:
            language_code = translation.get_language()

        # Normalize language code
        if language_code and "-" in language_code:
            base_code = language_code.split("-")[0]
        else:
            base_code = language_code

        # Check for translations
        if self.translations and language_code:
            # Try exact match first
            if language_code in self.translations:
                lang_translations = self.translations[language_code]
                if field_name in lang_translations and not field_name.startswith("_"):
                    return lang_translations[field_name]

            # Try base language code
            if base_code != language_code and base_code in self.translations:
                lang_translations = self.translations[base_code]
                if field_name in lang_translations and not field_name.startswith("_"):
                    return lang_translations[field_name]

        # Fallback to original field value
        return getattr(self, field_name, "")


class ImageSizePreset(models.Model):
    """Predefined image size configurations"""

    CROP_MODES = [
        ("contain", _("Contain - Fit within dimensions")),
        ("cover", _("Cover - Fill dimensions")),
        ("crop", _("Crop - Exact dimensions")),
        ("pad", _("Pad - Fit and add padding (preserves all content)")),
        ("smart", _("Smart Crop - Focus on important areas")),
    ]

    PADDING_COLOR_CHOICES = [
        ("transparent", _("Transparent")),
        ("white", _("White")),
        ("black", _("Black")),
    ]

    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(
        max_length=100,
        blank=True,
        help_text=_("Human-readable name (e.g., 'Small', 'Product Listing')"),
    )
    slug = models.SlugField(max_length=50, unique=True)
    width = models.IntegerField(validators=[MinValueValidator(1)])
    height = models.IntegerField(validators=[MinValueValidator(1)])
    crop_mode = models.CharField(max_length=20, choices=CROP_MODES, default="cover")
    padding_color = models.CharField(
        max_length=20,
        choices=PADDING_COLOR_CHOICES,
        default="transparent",
        help_text=_('Padding color when using "pad" crop mode. Use "transparent" for logos.'),
    )
    quality = models.IntegerField(
        default=85,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text=_("WebP quality (1-100)"),
    )
    is_active = models.BooleanField(default=True)
    is_system_preset = models.BooleanField(
        default=False,
        editable=False,
        help_text=_("System presets cannot be deleted or have their names/slugs changed"),
    )
    description = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(
        default=0, help_text=_("Display order (lower numbers appear first)")
    )

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self):
        return f"{self.display_name or self.name} ({self.width}x{self.height})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.display_name:
            self.display_name = self.name
        super().save(*args, **kwargs)

    @classmethod
    def get_sizes_dict(cls):
        """
        Get active image size presets as a dictionary.
        Returns dict like: {'small': (300, 300), 'medium': (600, 600), ...}
        """
        sizes = {}
        for preset in cls.objects.filter(is_active=True):
            sizes[preset.slug] = (preset.width, preset.height)
        return sizes


class MediaThumbnail(models.Model):
    """Generated thumbnails for media assets"""

    media_asset = models.ForeignKey(MediaAsset, on_delete=models.CASCADE, related_name="thumbnails")
    size_preset = models.CharField(max_length=50)
    width = models.IntegerField()
    height = models.IntegerField()

    # Files
    file = models.ImageField(upload_to=thumbnail_upload_path)
    webp_file = models.ImageField(upload_to=thumbnail_upload_path, blank=True, null=True)
    avif_file = models.ImageField(upload_to=thumbnail_upload_path, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["size_preset"]
        unique_together = [["media_asset", "size_preset"]]

    def __str__(self):
        return f"{self.media_asset.title} - {self.size_preset}"


class MediaUsage(models.Model):
    """Track where media assets are used"""

    media_asset = models.ForeignKey(MediaAsset, on_delete=models.CASCADE, related_name="usages")
    content_type = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100)
    field_name = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = [["media_asset", "content_type", "object_id", "field_name"]]

    def __str__(self):
        return f"{self.media_asset.title} used in {self.content_type}"


class MediaProcessingJob(models.Model):
    """Track media upload and processing jobs"""

    STATUS_CHOICES = [
        ("pending", _("Pending")),
        ("uploading", _("Uploading")),
        ("processing", _("Processing")),
        ("converting", _("Converting Video")),
        ("generating_thumbnails", _("Generating Thumbnails")),
        ("completed", _("Completed")),
        ("failed", _("Failed")),
        ("cancelled", _("Cancelled")),
    ]

    JOB_TYPE_CHOICES = [
        ("upload", _("File Upload")),
        ("convert_video", _("Video Conversion")),
        ("generate_thumbnails", _("Thumbnail Generation")),
        ("optimize_image", _("Image Optimization")),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job_type = models.CharField(max_length=30, choices=JOB_TYPE_CHOICES)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="pending")

    # Progress tracking
    progress = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text=_("Progress percentage (0-100)"),
    )
    status_message = models.CharField(max_length=255, blank=True)

    # File information
    filename = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField(null=True, blank=True)
    mime_type = models.CharField(max_length=50, blank=True)

    # Related asset (once created)
    media_asset = models.ForeignKey(
        MediaAsset, on_delete=models.CASCADE, null=True, blank=True, related_name="processing_jobs"
    )

    # User and timing
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    # Error tracking
    error_message = models.TextField(blank=True)

    # Additional data (JSON field for flexibility)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "created_at"]),
            models.Index(fields=["user", "status"]),
        ]

    def __str__(self):
        return f"{self.get_job_type_display()} - {self.filename} ({self.get_status_display()})"

    @property
    def duration(self):
        """Calculate job duration"""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None

    @property
    def is_complete(self):
        return self.status == "completed"

    @property
    def is_failed(self):
        return self.status == "failed"

    @property
    def is_active(self):
        return self.status in ["uploading", "processing", "converting", "generating_thumbnails"]
