import mimetypes
import os
import tempfile

from PIL import Image
from rest_framework import serializers

from .models import MediaAsset, MediaFolder, MediaProcessingJob, MediaThumbnail, Tag
from .services import ImageProcessor
from .video_services import VideoProcessor


class MediaFolderSerializer(serializers.ModelSerializer):
    """Serializer for media folders"""

    asset_count = serializers.SerializerMethodField()

    class Meta:
        model = MediaFolder
        fields = [
            "id",
            "name",
            "slug",
            "path",
            "description",
            "parent",
            "asset_count",
            "created_at",
        ]
        read_only_fields = ["id", "slug", "path", "created_at"]  # slug is auto-generated from name

    def get_asset_count(self, obj) -> int:
        return obj.assets.count()


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags"""

    asset_count = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ["id", "name", "slug", "asset_count"]
        read_only_fields = ["id", "slug"]  # slug is auto-generated from name

    def get_asset_count(self, obj) -> int:
        return obj.assets.count()


class MediaThumbnailSerializer(serializers.ModelSerializer):
    """Serializer for media thumbnails"""

    url = serializers.SerializerMethodField()
    webp_url = serializers.SerializerMethodField()

    class Meta:
        model = MediaThumbnail
        fields = ["size_preset", "width", "height", "url", "webp_url", "created_at"]
        read_only_fields = ["created_at"]

    def get_url(self, obj) -> str | None:
        if obj.file:
            return obj.file.url
        return None

    def get_webp_url(self, obj) -> str | None:
        if obj.webp_file:
            return obj.webp_file.url
        return None


class MediaAssetListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for media asset lists"""

    folder_name = serializers.CharField(source="folder.name", read_only=True)
    tag_names = serializers.StringRelatedField(source="tags", many=True, read_only=True)
    thumbnail_url = serializers.SerializerMethodField()
    display_url = serializers.SerializerMethodField()
    poster_url = serializers.SerializerMethodField()
    file_size_display = serializers.SerializerMethodField()

    class Meta:
        model = MediaAsset
        fields = [
            "id",
            "title",
            "alt_text",
            "description",
            "mime_type",
            "width",
            "height",
            "file_size",
            "file_size_display",
            "folder_name",
            "tag_names",
            "thumbnail_url",
            "display_url",
            "poster_url",
            "is_public",
            "created_at",
            "usage_count",
        ]
        read_only_fields = ["id", "created_at", "usage_count"]

    def get_thumbnail_url(self, obj) -> str | None:
        return obj.get_thumbnail("small")

    def get_display_url(self, obj) -> str | None:
        return obj.get_display_url()

    def get_poster_url(self, obj) -> str | None:
        if (obj.is_video() or obj.is_3d_model()) and obj.poster_image:
            return obj.poster_image.url
        return None

    def get_file_size_display(self, obj) -> str:
        size = obj.file_size
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"


class MediaAssetDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for media assets"""

    folder = MediaFolderSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    thumbnails = MediaThumbnailSerializer(many=True, read_only=True)
    uploaded_by_name = serializers.CharField(source="uploaded_by.get_full_name", read_only=True)
    original_url = serializers.SerializerMethodField()
    webp_url = serializers.SerializerMethodField()
    display_url = serializers.SerializerMethodField()
    file_size_display = serializers.SerializerMethodField()
    dimensions = serializers.SerializerMethodField()

    class Meta:
        model = MediaAsset
        fields = [
            "id",
            "title",
            "alt_text",
            "description",
            "mime_type",
            "width",
            "height",
            "file_size",
            "file_size_display",
            "dimensions",
            "folder",
            "tags",
            "thumbnails",
            "metadata",
            "focal_point_x",
            "focal_point_y",
            "is_public",
            "uploaded_by_name",
            "original_url",
            "webp_url",
            "display_url",
            "usage_count",
            "last_used_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "file_size",
            "width",
            "height",
            "mime_type",
            "metadata",
            "uploaded_by_name",
            "usage_count",
            "last_used_at",
            "created_at",
            "updated_at",
        ]

    def get_original_url(self, obj) -> str | None:
        if obj.original_file:
            return obj.original_file.url
        return None

    def get_webp_url(self, obj) -> str | None:
        if obj.webp_file:
            return obj.webp_file.url
        return None

    def get_display_url(self, obj) -> str | None:
        return obj.get_display_url()

    def get_file_size_display(self, obj) -> str:
        size = obj.file_size
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

    def get_dimensions(self, obj) -> str:
        return f"{obj.width} × {obj.height}"


class MediaAssetCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating media assets"""

    folder_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    tag_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False, allow_empty=True
    )
    job_id = serializers.CharField(read_only=True)
    job_status = serializers.CharField(read_only=True)
    thumbnail_url = serializers.SerializerMethodField()
    display_url = serializers.SerializerMethodField()
    poster_image = serializers.SerializerMethodField()

    class Meta:
        model = MediaAsset
        fields = [
            "id",
            "title",
            "alt_text",
            "description",
            "original_file",
            "mime_type",
            "folder_id",
            "tag_ids",
            "focal_point_x",
            "focal_point_y",
            "is_public",
            "job_id",
            "job_status",
            "thumbnail_url",
            "display_url",
            "poster_image",
        ]
        read_only_fields = ["id", "mime_type"]

    def get_thumbnail_url(self, obj) -> str | None:
        """Get thumbnail URL for the asset"""
        return obj.get_thumbnail("small")

    def get_display_url(self, obj) -> str | None:
        """Get display URL for the asset"""
        return obj.get_display_url()

    def get_poster_image(self, obj) -> str | None:
        """Get poster image URL for videos and 3D models"""
        if (obj.is_video() or obj.is_3d_model()) and obj.poster_image:
            return obj.poster_image.url
        return None

    def validate_original_file(self, value):
        """
        Validate uploaded file for security.

        Blocks:
        - HTML files (XSS risk)
        - SVG files (XSS risk - can contain JavaScript)
        - Files with double extensions (e.g., .html.jpg)
        - Files where magic bytes don't match extension
        """
        import os

        import magic
        from django.conf import settings

        if not value:
            return value

        # Get file extension
        filename = value.name.lower()
        _, ext = os.path.splitext(filename)
        ext = ext.lstrip(".")  # Remove leading dot

        # Get settings
        blocked_extensions = settings.MEDIA_LIBRARY_SETTINGS.get("BLOCKED_EXTENSIONS", [])
        blocked_mime_types = settings.MEDIA_LIBRARY_SETTINGS.get("BLOCKED_MIME_TYPES", [])

        # Check for double extensions (e.g., .html.jpg)
        parts = filename.split(".")
        if len(parts) > 2:
            # Check if any part (except last) is a blocked extension
            for part in parts[1:-1]:  # Skip filename and last extension
                if part in blocked_extensions:
                    raise serializers.ValidationError(
                        f"File has suspicious double extension. "
                        f"Files with '.{part}.' in the name are not allowed."
                    )

        # Check extension (SVG handled separately with sanitization)
        if ext in blocked_extensions and ext not in ["svg", "svgz"]:
            raise serializers.ValidationError(
                f"File type '.{ext}' is not allowed for security reasons. "
                f"Blocked file types: {', '.join([e for e in blocked_extensions if e not in ['svg', 'svgz']])}"
            )

        # Use magic bytes to detect actual file type
        try:
            value.seek(0)
            mime_type = magic.from_buffer(value.read(2048), mime=True)
            value.seek(0)

            # Check if detected MIME type is blocked (SVG handled separately with sanitization)
            if mime_type in blocked_mime_types and mime_type not in ["image/svg+xml"]:
                raise serializers.ValidationError(
                    f"File content detected as '{mime_type}' which is not allowed for security reasons."
                )

            # Check for HTML content specifically
            if mime_type in ["text/html", "application/xhtml+xml"]:
                raise serializers.ValidationError(
                    "HTML content detected in file. HTML files are not allowed for security reasons."
                )

            # Validate SVG files (reject if contains dangerous content)
            if mime_type in ["image/svg+xml", "text/xml"] or ext in ["svg", "svgz"]:
                from media_library.svg_sanitizer import is_svg_safe

                # Read the SVG content
                value.seek(0)
                svg_content = value.read()
                value.seek(0)

                # Check for dangerous content
                is_safe, reason = is_svg_safe(svg_content)
                if not is_safe:
                    raise serializers.ValidationError(
                        f"SVG file rejected: {reason}. "
                        f"Please remove scripts, event handlers, and external references from your SVG file before uploading."
                    )

                # SVG is clean - allow upload
                import logging

                logger = logging.getLogger(__name__)
                logger.info(f"Clean SVG file '{filename}' validated successfully")

        except serializers.ValidationError:
            # Re-raise validation errors (from SVG sanitization, etc.)
            raise
        except Exception as e:
            # If magic detection fails, fall back to stricter validation
            import logging

            logger = logging.getLogger(__name__)
            logger.warning(f"Magic byte detection failed for {filename}: {e}")

            # Read first bytes manually to check for HTML markers
            try:
                value.seek(0)
                first_bytes = value.read(1024).lower()
                value.seek(0)

                # Check for HTML markers
                html_markers = [
                    b"<!doctype html",
                    b"<html",
                    b"<head",
                    b"<body",
                    b"<script",
                    b"<?php",
                    b"<%",  # ASP/JSP
                ]
                if any(marker in first_bytes for marker in html_markers):
                    raise serializers.ValidationError(
                        "HTML or script content detected in file. Such files are not allowed for security reasons."
                    )
            except Exception:
                # If we can't validate, reject the file
                raise serializers.ValidationError("Unable to verify file safety. Upload rejected.")

        return value

    def create(self, validated_data):
        import logging

        from django.utils import timezone

        from .models import MediaProcessingJob

        logger = logging.getLogger(__name__)

        # Create processing job to track the upload
        job = None
        request = self.context.get("request")
        if request and request.user:
            original_file = validated_data.get("original_file")
            if original_file:
                job = MediaProcessingJob.objects.create(
                    job_type="upload",
                    status="uploading",
                    progress=10,
                    status_message="Processing uploaded file",
                    filename=original_file.name,
                    file_size=original_file.size,
                    user=request.user,
                    started_at=timezone.now(),
                )
                logger.info(f"Created processing job {job.id} for file {original_file.name}")

        try:
            folder_id = validated_data.pop("folder_id", None)
            tag_ids = validated_data.pop("tag_ids", [])

            # Set folder
            if folder_id:
                try:
                    folder = MediaFolder.objects.get(id=folder_id)
                    validated_data["folder"] = folder
                except MediaFolder.DoesNotExist:
                    raise serializers.ValidationError({"folder_id": "Invalid folder ID"})

            # Extract metadata from the uploaded file
            original_file = validated_data.get("original_file")
            if original_file:
                # Get file size
                validated_data["file_size"] = original_file.size

                # Get MIME type
                mime_type, _ = mimetypes.guess_type(original_file.name)
                if not mime_type:
                    # Try to detect from content for images
                    try:
                        original_file.seek(0)
                        img = Image.open(original_file)
                        img.load()  # Force PIL to fully load image data into memory
                        format_to_mime = {
                            "JPEG": "image/jpeg",
                            "PNG": "image/png",
                            "GIF": "image/gif",
                            "WEBP": "image/webp",
                            "BMP": "image/bmp",
                        }
                        mime_type = format_to_mime.get(img.format, "application/octet-stream")
                        original_file.seek(0)
                    except Exception:
                        mime_type = "application/octet-stream"

                validated_data["mime_type"] = mime_type

                # Handle based on file type
                if mime_type.startswith("video/"):
                    # Handle video files
                    try:
                        # Save file temporarily to probe it
                        with tempfile.NamedTemporaryFile(
                            delete=False, suffix=os.path.splitext(original_file.name)[1]
                        ) as tmp_file:
                            for chunk in original_file.chunks():
                                tmp_file.write(chunk)
                            tmp_path = tmp_file.name

                        # Update job status
                        if job:
                            job.status = "processing"
                            job.progress = 20
                            job.status_message = "Extracting video metadata"
                            job.save()

                        # Extract video metadata
                        video_processor = VideoProcessor()
                        metadata = video_processor.probe_video(tmp_path)

                        if metadata:
                            validated_data["width"] = metadata.get("width", 0)
                            validated_data["height"] = metadata.get("height", 0)
                            validated_data["duration"] = metadata.get("duration")
                            validated_data["frame_rate"] = metadata.get("frame_rate")
                            validated_data["bitrate"] = metadata.get("bitrate")
                            # Ensure codecs are never None (videos without audio track)
                            validated_data["video_codec"] = metadata.get("video_codec") or ""
                            validated_data["audio_codec"] = metadata.get("audio_codec") or ""
                            validated_data["metadata"] = metadata

                        # Clean up temp file
                        os.unlink(tmp_path)

                        # Reset file pointer
                        original_file.seek(0)

                    except Exception as e:
                        logger.error(f"Error extracting video metadata: {e}")
                        validated_data["metadata"] = {}

                elif mime_type.startswith("model/"):
                    # Handle 3D model files (GLB/glTF) — skip image/video processing
                    validated_data["metadata"] = {"type": "3d_model"}

                elif mime_type.startswith("image/"):
                    # Handle image files
                    try:
                        original_file.seek(0)
                        img = Image.open(original_file)
                        img.load()  # Force PIL to fully load image data into memory
                        validated_data["width"] = img.width
                        validated_data["height"] = img.height

                        # Extract image metadata
                        processor = ImageProcessor()
                        original_file.seek(0)
                        metadata = processor.extract_metadata(original_file)
                        validated_data["metadata"] = metadata

                        # Reset file pointer
                        original_file.seek(0)
                    except Exception as e:
                        logger.error(f"Error extracting image metadata: {e}")
                        validated_data["width"] = 0
                        validated_data["height"] = 0
                        validated_data["metadata"] = {}

            # Create the asset
            asset = super().create(validated_data)

            # Post-processing based on file type
            if asset.is_video():
                # Handle video post-processing
                try:
                    # Save file temporarily for video processing
                    with tempfile.NamedTemporaryFile(
                        delete=False, suffix=os.path.splitext(asset.original_file.name)[1]
                    ) as tmp_file:
                        asset.original_file.seek(0)
                        for chunk in asset.original_file.chunks():
                            tmp_file.write(chunk)
                        tmp_path = tmp_file.name

                    video_processor = VideoProcessor()

                    # Generate poster/thumbnail image
                    try:
                        if job:
                            job.status = "generating_thumbnails"
                            job.progress = 30
                            job.status_message = "Generating video thumbnail"
                            job.save()

                        poster_content = video_processor.extract_thumbnail(tmp_path)
                        if poster_content:
                            asset.poster_image.save(
                                f"{asset.id}_poster.jpg", poster_content, save=True
                            )
                    except Exception as e:
                        logger.error(f"Error generating video thumbnail: {e}")

                    # Convert video if auto-conversion is enabled
                    from django.conf import settings

                    ml_settings = getattr(settings, "MEDIA_LIBRARY_SETTINGS", {})
                    auto_convert = ml_settings.get("AUTO_CONVERT_VIDEOS", False)

                    if auto_convert:
                        try:
                            format = ml_settings.get("VIDEO_CONVERSION_FORMAT", "webm_av1")
                            crf = ml_settings.get("VIDEO_CRF", 30)
                            preset = ml_settings.get("VIDEO_PRESET", 6)

                            if job:
                                job.status = "converting"
                                job.progress = 50
                                job.status_message = f"Converting video to {format.upper()}"
                                job.save()

                            # Create a progress callback for conversion
                            def update_progress(progress):
                                if job:
                                    # Map 0-100 conversion progress to 50-90 job progress
                                    job_progress = 50 + int(progress * 0.4)
                                    job.progress = min(job_progress, 90)
                                    job.status_message = f"Converting video... {progress}%"
                                    job.save()

                            converted_path = None
                            if format == "webm_av1":
                                converted_path = video_processor.convert_to_webm_av1(
                                    tmp_path,
                                    crf=crf,
                                    preset=preset,
                                    progress_callback=update_progress if job else None,
                                )
                                output_ext = ".webm"
                            elif format == "webm_vp9":
                                converted_path = video_processor.convert_to_webm_vp9(
                                    tmp_path,
                                    crf=crf,
                                    progress_callback=update_progress if job else None,
                                )
                                output_ext = ".webm"
                            elif format == "mp4_h265":
                                converted_path = video_processor.convert_to_mp4_h265(
                                    tmp_path,
                                    crf=crf,
                                    progress_callback=update_progress if job else None,
                                )
                                output_ext = ".mp4"

                            if converted_path and os.path.exists(converted_path):
                                if job:
                                    job.progress = 95
                                    job.status_message = "Saving converted video"
                                    job.save()

                                with open(converted_path, "rb") as f:
                                    from django.core.files.base import ContentFile

                                    content = ContentFile(f.read())
                                    asset.converted_video.save(
                                        f"{asset.id}{output_ext}", content, save=True
                                    )
                                os.unlink(converted_path)
                                logger.info(f"Video converted to {format} successfully")

                                if job:
                                    job.status = "completed"
                                    job.progress = 100
                                    job.status_message = "Video processing completed"
                                    job.completed_at = timezone.now()
                                    job.save()
                        except Exception as e:
                            logger.error(f"Error converting video: {e}")
                            if job:
                                job.status = "failed"
                                job.status_message = f"Conversion failed: {str(e)}"
                                job.completed_at = timezone.now()
                                job.save()

                    # Clean up temp file
                    os.unlink(tmp_path)

                except Exception as e:
                    logger.error(f"Error in video post-processing: {e}")

            elif asset.is_image():
                # Handle image post-processing
                try:
                    # Generate WebP version if it's not already WebP
                    if asset.mime_type != "image/webp":
                        processor = ImageProcessor()
                        asset.original_file.seek(0)
                        webp_content = processor.convert_to_webp(asset.original_file)
                        if webp_content:
                            asset.webp_file.save(f"{asset.id}.webp", webp_content, save=True)
                except Exception as e:
                    logger.error(f"Error generating WebP: {e}")

                try:
                    # Generate thumbnails using ImageSizePreset model for crop_mode and padding_color
                    from media_library.models import ImageSizePreset

                    processor = ImageProcessor()
                    presets = ImageSizePreset.objects.filter(is_active=True)

                    for preset in presets:
                        try:
                            asset.original_file.seek(0)
                            original_content, webp_content = processor.generate_thumbnail(
                                asset.original_file,
                                preset.width,
                                preset.height,
                                crop_mode=preset.crop_mode,
                                padding_color=getattr(preset, "padding_color", None),
                            )

                            if original_content:
                                # Determine file extension based on crop mode (PNG for pad with transparency)
                                ext = (
                                    "png"
                                    if preset.crop_mode == "pad"
                                    and getattr(preset, "padding_color", "transparent")
                                    == "transparent"
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
                        except Exception as e:
                            logger.error(f"Error generating thumbnail {preset.slug}: {e}")
                            continue
                except Exception as e:
                    logger.error(f"Error in thumbnail generation: {e}")

            # Set tags
            if tag_ids:
                tags = Tag.objects.filter(id__in=tag_ids)
                asset.tags.set(tags)

            # Mark job as completed if not a video (videos complete after conversion)
            if job and not asset.is_video():
                job.status = "completed"
                job.progress = 100
                job.status_message = "Upload completed"
                job.completed_at = timezone.now()
                job.save()

            # Attach job ID and status to response
            if job:
                self._job_id = job.id
                self._job_status = job.status

            return asset
        except Exception as e:
            logger.error(f"Error in MediaAssetCreateSerializer.create: {e}")
            if job:
                job.status = "failed"
                job.status_message = "Upload failed"
                job.error_message = str(e)[:5000]  # Limit to 5000 chars for safety
                job.completed_at = timezone.now()
                job.save()
            raise

    def to_representation(self, instance):
        """Add job_id and job_status to the response"""
        ret = super().to_representation(instance)
        if hasattr(self, "_job_id"):
            ret["job_id"] = self._job_id

            # Include job status if the job exists
            if hasattr(self, "_job_status"):
                ret["job_status"] = self._job_status

        return ret


class MediaAssetUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating media assets"""

    folder_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    tag_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False, allow_empty=True
    )

    class Meta:
        model = MediaAsset
        fields = [
            "title",
            "alt_text",
            "description",
            "folder_id",
            "tag_ids",
            "focal_point_x",
            "focal_point_y",
            "is_public",
        ]

    def update(self, instance, validated_data):
        folder_id = validated_data.pop("folder_id", None)
        tag_ids = validated_data.pop("tag_ids", None)

        # Update folder
        if folder_id is not None:
            if folder_id:
                try:
                    folder = MediaFolder.objects.get(id=folder_id)
                    instance.folder = folder
                except MediaFolder.DoesNotExist:
                    raise serializers.ValidationError({"folder_id": "Invalid folder ID"})
            else:
                instance.folder = None

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # Update tags
        if tag_ids is not None:
            tags = Tag.objects.filter(id__in=tag_ids)
            instance.tags.set(tags)

        return instance


class BulkOperationSerializer(serializers.Serializer):
    """Serializer for bulk operations"""

    asset_ids = serializers.ListField(child=serializers.UUIDField(), min_length=1)
    action = serializers.ChoiceField(
        choices=[
            ("delete", "Delete"),
            ("move_to_folder", "Move to Folder"),
            ("add_tags", "Add Tags"),
            ("remove_tags", "Remove Tags"),
            ("toggle_public", "Toggle Public Status"),
        ]
    )
    folder_id = serializers.UUIDField(required=False, allow_null=True)
    tag_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False, allow_empty=True
    )

    def validate(self, data):
        action = data.get("action")

        if action == "move_to_folder" and "folder_id" not in data:
            raise serializers.ValidationError(
                {"folder_id": "Folder ID is required for move_to_folder action"}
            )

        if action in ["add_tags", "remove_tags"] and not data.get("tag_ids"):
            raise serializers.ValidationError(
                {"tag_ids": f"Tag IDs are required for {action} action"}
            )

        return data


class MediaProcessingJobSerializer(serializers.ModelSerializer):
    """Serializer for media processing jobs"""

    class Meta:
        model = MediaProcessingJob
        fields = [
            "id",
            "job_type",
            "status",
            "progress",
            "status_message",
            "error_message",
            "filename",
            "file_size",
            "user",
            "started_at",
            "completed_at",
            "created_at",
        ]
        read_only_fields = fields  # All fields are read-only
