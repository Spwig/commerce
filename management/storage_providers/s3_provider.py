"""
S3 and S3-compatible storage provider.

Covers: AWS S3, Backblaze B2, Wasabi, DigitalOcean Spaces,
Cloudflare R2, MinIO (self-hosted), Vultr Object Storage.
"""

import logging
import os
from collections.abc import Callable

from .base import (
    BaseStorageProvider,
    ConnectionTestResult,
    RemoteFile,
    UploadResult,
)

logger = logging.getLogger(__name__)


class S3StorageProvider(BaseStorageProvider):
    provider_type = "s3"
    provider_name = "Amazon S3 / S3-Compatible"

    credential_fields = [
        {
            "key": "access_key_id",
            "label": "Access Key ID",
            "secret": True,
            "required": True,
            "type": "text",
        },
        {
            "key": "secret_access_key",
            "label": "Secret Access Key",
            "secret": True,
            "required": True,
            "type": "password",
        },
    ]

    settings_fields = [
        {
            "key": "preset",
            "label": "Provider",
            "type": "select",
            "required": False,
            "default": "",
            "options": [
                {"value": "", "label": "Custom / AWS S3"},
                {"value": "backblaze_b2", "label": "Backblaze B2"},
                {"value": "wasabi", "label": "Wasabi"},
                {"value": "digitalocean_spaces", "label": "DigitalOcean Spaces"},
                {"value": "cloudflare_r2", "label": "Cloudflare R2"},
                {"value": "minio", "label": "MinIO (Self-hosted)"},
                {"value": "vultr", "label": "Vultr Object Storage"},
            ],
            "help_text": "Select a preset to auto-fill the endpoint URL, or choose Custom.",
        },
        {
            "key": "bucket",
            "label": "Bucket Name",
            "type": "text",
            "required": True,
        },
        {
            "key": "prefix",
            "label": "Path Prefix",
            "type": "text",
            "required": False,
            "default": "spwig-backups/",
            "help_text": "Folder path inside the bucket (e.g. spwig-backups/).",
        },
        {
            "key": "region",
            "label": "Region",
            "type": "text",
            "required": False,
            "default": "us-east-1",
            "help_text": "AWS region or provider region code.",
        },
        {
            "key": "endpoint_url",
            "label": "Custom Endpoint URL",
            "type": "text",
            "required": False,
            "help_text": "Required for non-AWS providers (auto-filled by preset).",
        },
    ]

    # Presets map to endpoint URL templates.
    PRESETS: dict[str, dict[str, str]] = {
        "backblaze_b2": {
            "endpoint_template": "https://s3.{region}.backblazeb2.com",
            "default_region": "us-west-004",
        },
        "wasabi": {
            "endpoint_template": "https://s3.{region}.wasabisys.com",
            "default_region": "us-east-1",
        },
        "digitalocean_spaces": {
            "endpoint_template": "https://{region}.digitaloceanspaces.com",
            "default_region": "nyc3",
        },
        "cloudflare_r2": {
            "endpoint_template": "https://{account_id}.r2.cloudflarestorage.com",
            "default_region": "auto",
        },
        "vultr": {
            "endpoint_template": "https://{region}.vultrobjects.com",
            "default_region": "ewr1",
        },
        "minio": {
            "endpoint_template": "",
            "default_region": "us-east-1",
        },
    }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_client(self):
        import boto3
        from botocore.config import Config

        kwargs = {
            "aws_access_key_id": self.credentials.get("access_key_id"),
            "aws_secret_access_key": self.credentials.get("secret_access_key"),
            "region_name": self.settings.get("region") or "us-east-1",
            "config": Config(
                signature_version="s3v4",
                retries={"max_attempts": 3, "mode": "standard"},
            ),
        }
        endpoint_url = self.settings.get("endpoint_url")
        if endpoint_url:
            kwargs["endpoint_url"] = endpoint_url
        return boto3.client("s3", **kwargs)

    def _bucket(self) -> str:
        return self.settings.get("bucket", "")

    def _prefix(self) -> str:
        prefix = self.settings.get("prefix", "spwig-backups/")
        if prefix and not prefix.endswith("/"):
            prefix += "/"
        return prefix

    # ------------------------------------------------------------------
    # ABC implementation
    # ------------------------------------------------------------------

    def test_connection(self) -> ConnectionTestResult:
        try:
            client = self._get_client()
            bucket = self._bucket()
            if not bucket:
                return ConnectionTestResult(success=False, message="Bucket name is required.")

            # 1. Check bucket exists and we have access
            client.head_bucket(Bucket=bucket)

            # 2. Upload a small test object
            test_key = f"{self._prefix()}.spwig_connection_test"
            client.put_object(
                Bucket=bucket,
                Key=test_key,
                Body=b"spwig-connection-test",
            )

            # 3. Verify we can list
            client.list_objects_v2(Bucket=bucket, Prefix=self._prefix(), MaxKeys=1)

            # 4. Delete test object
            client.delete_object(Bucket=bucket, Key=test_key)

            # 5. Try to get bucket location for details
            details = {"bucket": bucket}
            try:
                loc = client.get_bucket_location(Bucket=bucket)
                details["region"] = loc.get("LocationConstraint") or "us-east-1"
            except Exception:
                details["region"] = self.settings.get("region", "unknown")

            return ConnectionTestResult(
                success=True,
                message=f'Successfully connected to bucket "{bucket}".',
                details=details,
            )

        except Exception as e:
            error_msg = str(e)
            # Provide friendly messages for common errors
            if "AccessDenied" in error_msg or "403" in error_msg:
                msg = "Access denied. Check your access key and secret key, and verify bucket permissions."
            elif "NoSuchBucket" in error_msg or "404" in error_msg:
                msg = f'Bucket "{self._bucket()}" not found. Verify the bucket name and region.'
            elif "InvalidAccessKeyId" in error_msg:
                msg = "Invalid Access Key ID. Check your credentials."
            elif "SignatureDoesNotMatch" in error_msg:
                msg = "Invalid Secret Access Key. Check your credentials."
            elif "EndpointConnectionError" in error_msg or "Could not connect" in error_msg:
                msg = "Could not connect to the endpoint. Check the endpoint URL and region."
            else:
                msg = f"Connection failed: {error_msg}"
            return ConnectionTestResult(success=False, message=msg)

    def upload_file(
        self,
        local_path: str,
        remote_path: str,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> UploadResult:
        try:
            client = self._get_client()
            bucket = self._bucket()
            file_size = os.path.getsize(local_path)

            callback = None
            if progress_callback:
                uploaded = {"bytes": 0}

                def callback(bytes_amount):
                    uploaded["bytes"] += bytes_amount
                    progress_callback(uploaded["bytes"], file_size)

            client.upload_file(
                Filename=local_path,
                Bucket=bucket,
                Key=remote_path,
                Callback=callback,
            )

            return UploadResult(
                success=True,
                remote_path=f"s3://{bucket}/{remote_path}",
                file_size=file_size,
                message="Upload completed.",
            )

        except Exception as e:
            logger.error("S3 upload failed: %s", e)
            return UploadResult(success=False, message=str(e))

    def download_file(
        self,
        remote_path: str,
        local_path: str,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> bool:
        try:
            client = self._get_client()
            bucket = self._bucket()

            # Get file size first for progress
            total_size = 0
            if progress_callback:
                head = client.head_object(Bucket=bucket, Key=remote_path)
                total_size = head.get("ContentLength", 0)

            callback = None
            if progress_callback and total_size:
                downloaded = {"bytes": 0}

                def callback(bytes_amount):
                    downloaded["bytes"] += bytes_amount
                    progress_callback(downloaded["bytes"], total_size)

            client.download_file(
                Bucket=bucket,
                Key=remote_path,
                Filename=local_path,
                Callback=callback,
            )
            return True

        except Exception as e:
            logger.error("S3 download failed: %s", e)
            return False

    def list_files(self, prefix: str = "") -> list[RemoteFile]:
        try:
            client = self._get_client()
            bucket = self._bucket()
            full_prefix = prefix or self._prefix()

            files: list[RemoteFile] = []
            paginator = client.get_paginator("list_objects_v2")
            for page in paginator.paginate(Bucket=bucket, Prefix=full_prefix):
                for obj in page.get("Contents", []):
                    files.append(
                        RemoteFile(
                            path=obj["Key"],
                            size=obj["Size"],
                            last_modified=obj["LastModified"].isoformat(),
                        )
                    )
            return files

        except Exception as e:
            logger.error("S3 list_files failed: %s", e)
            return []

    def delete_file(self, remote_path: str) -> bool:
        try:
            client = self._get_client()
            client.delete_object(Bucket=self._bucket(), Key=remote_path)
            return True
        except Exception as e:
            logger.error("S3 delete failed: %s", e)
            return False
