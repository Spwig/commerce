"""
Custom storage backends for Spwig platform.
Provides S3-compatible storage using MinIO for digital assets and media files,
and a non-strict manifest storage for production static file hashing.
"""

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from whitenoise.storage import CompressedManifestStaticFilesStorage


class NonStrictManifestStorage(CompressedManifestStaticFilesStorage):
    """
    WhiteNoise manifest storage that tolerates missing files referenced in CSS.
    Some vendor CSS (e.g. intl-tel-input) references image files that may not
    be present in the Docker build. Without this override, collectstatic
    crashes (set -e in entrypoint) and puts the container in a restart loop.
    """

    manifest_strict = False

    def stored_name(self, name):
        """Fallback to unhashed name if file isn't in manifest or STATIC_ROOT."""
        try:
            return super().stored_name(name)
        except ValueError:
            return name

    def post_process(self, *args, **kwargs):
        for name, hashed_name, processed in super().post_process(*args, **kwargs):
            if isinstance(processed, Exception):
                import sys

                print(
                    f"Warning: Post-processing '{name}' skipped: {processed}",
                    file=sys.stderr,
                )
                yield name, hashed_name, True
            else:
                yield name, hashed_name, processed


class MinIODigitalAssetsStorage(S3Boto3Storage):
    """
    MinIO storage backend for digital product assets (software, eBooks, etc.).
    Files are stored in the 'digital-assets' bucket with private access by default.
    Download URLs are generated using signed URLs with expiration.
    """

    bucket_name = settings.MINIO_DIGITAL_ASSETS_BUCKET
    default_acl = "private"  # Digital assets require signed URLs
    file_overwrite = False  # Never overwrite digital assets
    custom_domain = False  # Use MinIO endpoint directly

    def __init__(self, **settings_override):
        super().__init__(**settings_override)
        # Override settings with MinIO-specific configuration
        self.access_key = settings.MINIO_ACCESS_KEY
        self.secret_key = settings.MINIO_SECRET_KEY
        self.endpoint_url = (
            f"{'https' if settings.MINIO_USE_SSL else 'http'}://{settings.MINIO_ENDPOINT}"
        )
        self.region_name = getattr(settings, "MINIO_REGION", "us-east-1")
        self.use_ssl = settings.MINIO_USE_SSL
        self.addressing_style = "path"  # Required for MinIO


class MinIOMediaStorage(S3Boto3Storage):
    """
    MinIO storage backend for general media files (product images, etc.).
    Files are stored in the 'media' bucket with public read access.
    """

    bucket_name = settings.MINIO_MEDIA_BUCKET
    default_acl = "public-read"  # Media files are publicly accessible
    file_overwrite = False
    custom_domain = False

    def __init__(self, **settings_override):
        super().__init__(**settings_override)
        # Override settings with MinIO-specific configuration
        self.access_key = settings.MINIO_ACCESS_KEY
        self.secret_key = settings.MINIO_SECRET_KEY
        self.endpoint_url = (
            f"{'https' if settings.MINIO_USE_SSL else 'http'}://{settings.MINIO_ENDPOINT}"
        )
        self.region_name = getattr(settings, "MINIO_REGION", "us-east-1")
        self.use_ssl = settings.MINIO_USE_SSL
        self.addressing_style = "path"
