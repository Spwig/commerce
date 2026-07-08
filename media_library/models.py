import os
import uuid
import hashlib
from datetime import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from core.models import SoftDeleteModel


def media_upload_path(instance, filename):
    """Generate upload path for media files"""
    ext = os.path.splitext(filename)[1]
    # Use UUID for filename to avoid conflicts
    new_filename = f"{instance.id}{ext}"
    # Organize by year/month
    date_path = datetime.now().strftime('%Y/%m')
    return f"media_library/{date_path}/{new_filename}"


def thumbnail_upload_path(instance, filename):
    """Generate upload path for thumbnail files"""
    ext = os.path.splitext(filename)[1]
    # Include size preset in filename
    new_filename = f"{instance.media_asset.id}_{instance.size_preset}{ext}"
    date_path = datetime.now().strftime('%Y/%m')
    return f"media_library/thumbnails/{date_path}/{new_filename}"


class MediaFolder(models.Model):
    """Organize media assets into folders"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    path = models.CharField(max_length=500, unique=True, editable=False)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['path']

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
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class MediaAsset(SoftDeleteModel):
    """Core media asset model for images and videos"""
    MIME_TYPE_CHOICES = [
        ('image/jpeg', 'JPEG'),
        ('image/png', 'PNG'),
        ('image/gif', 'GIF'),
        ('image/webp', 'WebP'),
        ('image/svg+xml', 'SVG'),
        ('video/mp4', 'MP4'),
        ('video/webm', 'WebM'),
        ('video/quicktime', 'MOV'),
        ('video/x-matroska', 'MKV'),
        ('video/x-msvideo', 'AVI'),
        ('model/gltf-binary', 'GLB'),
        ('model/gltf+json', 'glTF'),
        ('image/hdr', 'HDR'),
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
        help_text="Original media ID from source platform"
    )
    migration_job = models.ForeignKey(
        'migration.MigrationJob',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='imported_media',
        help_text="Migration job that imported this media asset"
    )

    # Files
    original_file = models.FileField(
        upload_to=media_upload_path,
        help_text=_('Original uploaded file')
    )
    webp_file = models.FileField(
        upload_to=media_upload_path,
        blank=True,
        null=True,
        help_text=_('WebP version of the image')
    )

    # Video-specific fields
    converted_video = models.FileField(
        upload_to=media_upload_path,
        blank=True,
        null=True,
        help_text=_('Optimized/converted video file')
    )
    poster_image = models.ImageField(
        upload_to=media_upload_path,
        blank=True,
        null=True,
        help_text=_('Video poster/thumbnail image')
    )
    duration = models.FloatField(
        null=True,
        blank=True,
        help_text=_('Video duration in seconds')
    )
    frame_rate = models.FloatField(
        null=True,
        blank=True,
        help_text=_('Video frame rate (fps)')
    )
    bitrate = models.IntegerField(
        null=True,
        blank=True,
        help_text=_('Video bitrate in bits/sec')
    )
    video_codec = models.CharField(
        max_length=50,
        blank=True,
        help_text=_('Video codec (e.g., h264, av1, vp9)')
    )
    audio_codec = models.CharField(
        max_length=50,
        blank=True,
        help_text=_('Audio codec (e.g., aac, opus, vorbis)')
    )

    # Technical metadata
    file_size = models.PositiveIntegerField()
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    mime_type = models.CharField(
        max_length=50,
        choices=MIME_TYPE_CHOICES
    )

    # Organization
    folder = models.ForeignKey(
        MediaFolder,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assets'
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='assets')

    # Extended metadata
    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text=_('EXIF data and other metadata')
    )

    # Translations for multilingual fields
    translations = models.JSONField(
        default=dict,
        blank=True,
        help_text=_('Translations for title, alt_text, and description')
    )
    focal_point_x = models.FloatField(
        default=0.5,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text=_('X coordinate of focal point (0-1)')
    )
    focal_point_y = models.FloatField(
        default=0.5,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text=_('Y coordinate of focal point (0-1)')
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
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['mime_type']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.title

    def is_video(self):
        """Check if this asset is a video file"""
        return self.mime_type.startswith('video/')

    def is_image(self):
        """Check if this asset is an image file"""
        return self.mime_type.startswith('image/')

    def is_3d_model(self):
        """Check if this asset is a 3D model file (GLB/glTF)"""
        return self.mime_type.startswith('model/')

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

        # For images, look for thumbnails
        try:
            thumbnail = self.thumbnails.get(size_preset=size_preset)
            if thumbnail.webp_file:
                return thumbnail.webp_file.url
            return thumbnail.file.url
        except MediaThumbnail.DoesNotExist:
            return self.get_display_url()

    @property
    def thumbnail_small(self):
        """Get small thumbnail (300x300) for gallery/list views"""
        return self.get_thumbnail('small')

    @property
    def thumbnail_medium(self):
        """Get medium thumbnail (600x600) for larger displays"""
        return self.get_thumbnail('medium')

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
        if language_code and '-' in language_code:
            base_code = language_code.split('-')[0]
        else:
            base_code = language_code

        # Check for translations
        if self.translations and language_code:
            # Try exact match first
            if language_code in self.translations:
                lang_translations = self.translations[language_code]
                if field_name in lang_translations and not field_name.startswith('_'):
                    return lang_translations[field_name]

            # Try base language code
            if base_code != language_code and base_code in self.translations:
                lang_translations = self.translations[base_code]
                if field_name in lang_translations and not field_name.startswith('_'):
                    return lang_translations[field_name]

        # Fallback to original field value
        return getattr(self, field_name, '')


class ImageSizePreset(models.Model):
    """Predefined image size configurations"""
    CROP_MODES = [
        ('contain', _('Contain - Fit within dimensions')),
        ('cover', _('Cover - Fill dimensions')),
        ('crop', _('Crop - Exact dimensions')),
        ('pad', _('Pad - Fit and add padding (preserves all content)')),
        ('smart', _('Smart Crop - Focus on important areas')),
    ]

    PADDING_COLOR_CHOICES = [
        ('transparent', _('Transparent')),
        ('white', _('White')),
        ('black', _('Black')),
    ]

    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(
        max_length=100,
        blank=True,
        help_text=_("Human-readable name (e.g., 'Small', 'Product Listing')")
    )
    slug = models.SlugField(max_length=50, unique=True)
    width = models.IntegerField(validators=[MinValueValidator(1)])
    height = models.IntegerField(validators=[MinValueValidator(1)])
    crop_mode = models.CharField(max_length=20, choices=CROP_MODES, default='cover')
    padding_color = models.CharField(
        max_length=20,
        choices=PADDING_COLOR_CHOICES,
        default='transparent',
        help_text=_('Padding color when using "pad" crop mode. Use "transparent" for logos.')
    )
    quality = models.IntegerField(
        default=85,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text=_('WebP quality (1-100)')
    )
    is_active = models.BooleanField(default=True)
    is_system_preset = models.BooleanField(
        default=False,
        editable=False,
        help_text=_('System presets cannot be deleted or have their names/slugs changed')
    )
    description = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(
        default=0,
        help_text=_("Display order (lower numbers appear first)")
    )

    class Meta:
        ordering = ['sort_order', 'name']

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
    media_asset = models.ForeignKey(
        MediaAsset,
        on_delete=models.CASCADE,
        related_name='thumbnails'
    )
    size_preset = models.CharField(max_length=50)
    width = models.IntegerField()
    height = models.IntegerField()

    # Files
    file = models.ImageField(upload_to=thumbnail_upload_path)
    webp_file = models.ImageField(
        upload_to=thumbnail_upload_path,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['size_preset']
        unique_together = [['media_asset', 'size_preset']]

    def __str__(self):
        return f"{self.media_asset.title} - {self.size_preset}"


class MediaUsage(models.Model):
    """Track where media assets are used"""
    media_asset = models.ForeignKey(
        MediaAsset,
        on_delete=models.CASCADE,
        related_name='usages'
    )
    content_type = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100)
    field_name = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = [['media_asset', 'content_type', 'object_id', 'field_name']]

    def __str__(self):
        return f"{self.media_asset.title} used in {self.content_type}"


class MediaProcessingJob(models.Model):
    """Track media upload and processing jobs"""

    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('uploading', _('Uploading')),
        ('processing', _('Processing')),
        ('converting', _('Converting Video')),
        ('generating_thumbnails', _('Generating Thumbnails')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
        ('cancelled', _('Cancelled')),
    ]

    JOB_TYPE_CHOICES = [
        ('upload', _('File Upload')),
        ('convert_video', _('Video Conversion')),
        ('generate_thumbnails', _('Thumbnail Generation')),
        ('optimize_image', _('Image Optimization')),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job_type = models.CharField(max_length=30, choices=JOB_TYPE_CHOICES)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')

    # Progress tracking
    progress = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text=_('Progress percentage (0-100)')
    )
    status_message = models.CharField(max_length=255, blank=True)

    # File information
    filename = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField(null=True, blank=True)
    mime_type = models.CharField(max_length=50, blank=True)

    # Related asset (once created)
    media_asset = models.ForeignKey(
        MediaAsset,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='processing_jobs'
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
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['user', 'status']),
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
        return self.status == 'completed'

    @property
    def is_failed(self):
        return self.status == 'failed'

    @property
    def is_active(self):
        return self.status in ['uploading', 'processing', 'converting', 'generating_thumbnails']