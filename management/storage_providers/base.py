"""
Base storage provider abstraction for remote backup destinations.

All storage provider implementations inherit from BaseStorageProvider
and implement the required abstract methods.
"""

import logging
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class UploadResult:
    """Result from an upload operation."""

    success: bool
    remote_path: str = ""
    file_size: int = 0
    message: str = ""


@dataclass
class ConnectionTestResult:
    """Result from a connection test."""

    success: bool
    message: str = ""
    details: dict[str, Any] | None = None
    storage_used: int | None = None
    storage_available: int | None = None


@dataclass
class RemoteFile:
    """Represents a file in remote storage."""

    path: str
    size: int
    last_modified: str | None = None
    metadata: dict[str, Any] | None = field(default_factory=dict)


class BaseStorageProvider(ABC):
    """
    Abstract base class for remote storage providers.

    Each subclass must set provider_type, provider_name, credential_fields,
    and settings_fields as class-level attributes. These are used by the
    admin wizard to dynamically generate forms.
    """

    provider_type: str = ""
    provider_name: str = ""

    # Fields the wizard renders for this provider.
    # Each entry: {'key': str, 'label': str, 'secret': bool, 'required': bool,
    #              'type': 'text'|'password'|'textarea'|'select'|'number',
    #              'default': str, 'help_text': str, 'options': list}
    credential_fields: list[dict[str, Any]] = []
    settings_fields: list[dict[str, Any]] = []

    # OAuth support — override in subclasses that use OAuth
    requires_oauth: bool = False
    oauth_scopes: list[str] = []

    def __init__(self, credentials: dict[str, Any], settings: dict[str, Any] | None = None):
        self.credentials = credentials
        self.settings = settings or {}

    @classmethod
    def create_oauth_handler(cls, client_id: str, client_secret: str, redirect_uri: str):
        """Override for OAuth providers. Returns an OAuth handler instance."""
        raise NotImplementedError(f"{cls.provider_name} does not support OAuth")

    def refresh_credentials_if_needed(self) -> dict[str, Any]:
        """Override for OAuth providers to handle token refresh.
        Returns updated credentials dict (or original if no refresh needed)."""
        return self.credentials

    @abstractmethod
    def test_connection(self) -> ConnectionTestResult:
        """Verify credentials and basic read/write access."""

    @abstractmethod
    def upload_file(
        self,
        local_path: str,
        remote_path: str,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> UploadResult:
        """Upload a local file to remote storage."""

    @abstractmethod
    def download_file(
        self,
        remote_path: str,
        local_path: str,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> bool:
        """Download a file from remote storage. Returns True on success."""

    @abstractmethod
    def list_files(self, prefix: str = "") -> list[RemoteFile]:
        """List files in remote storage, optionally filtered by prefix."""

    @abstractmethod
    def delete_file(self, remote_path: str) -> bool:
        """Delete a single file. Returns True on success."""

    def cleanup_old_files(self, prefix: str, retention_days: int) -> int:
        """Delete files older than *retention_days*. Returns count deleted."""
        from datetime import datetime, timedelta

        cutoff = datetime.now(UTC) - timedelta(days=retention_days)
        deleted = 0
        for f in self.list_files(prefix=prefix):
            if f.last_modified:
                try:
                    ts = datetime.fromisoformat(f.last_modified)
                    if ts.tzinfo is None:
                        ts = ts.replace(tzinfo=UTC)
                    if ts < cutoff and self.delete_file(f.path):
                        deleted += 1
                except (ValueError, TypeError):
                    continue
        return deleted
