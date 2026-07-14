"""
Storage provider registry.

Discovers providers and creates instances from RemoteStorageDestination models.
"""

import logging

from .base import BaseStorageProvider

logger = logging.getLogger(__name__)


class StorageProviderRegistry:
    _providers: dict[str, type[BaseStorageProvider]] = {}

    @classmethod
    def register(cls, provider_class: type[BaseStorageProvider]):
        cls._providers[provider_class.provider_type] = provider_class

    @classmethod
    def get_provider_class(cls, provider_type: str) -> type[BaseStorageProvider] | None:
        return cls._providers.get(provider_type)

    @classmethod
    def get_available_providers(cls) -> list[dict]:
        """Return provider metadata for the wizard UI."""
        return [
            {
                "type": p.provider_type,
                "name": p.provider_name,
                "credential_fields": p.credential_fields,
                "settings_fields": p.settings_fields,
            }
            for p in cls._providers.values()
        ]

    @classmethod
    def create_from_destination(cls, destination) -> BaseStorageProvider:
        """
        Instantiate a provider from a RemoteStorageDestination model instance.
        Handles credential decryption.
        """
        from payment_providers.utils.encryption import decrypt_credentials

        provider_class = cls.get_provider_class(destination.provider_type)
        if not provider_class:
            raise ValueError(f"Unknown provider type: {destination.provider_type}")

        decrypted_creds = decrypt_credentials(destination.credentials_encrypted)
        return provider_class(credentials=decrypted_creds, settings=destination.settings)

    @classmethod
    def create_from_raw(
        cls,
        provider_type: str,
        credentials: dict,
        settings: dict,
    ) -> BaseStorageProvider:
        """
        Instantiate a provider from raw (unencrypted) credentials.
        Used by the test-connection endpoint before saving to DB.
        """
        provider_class = cls.get_provider_class(provider_type)
        if not provider_class:
            raise ValueError(f"Unknown provider type: {provider_type}")
        return provider_class(credentials=credentials, settings=settings)


# Auto-register built-in providers
from .dropbox_provider import DropboxStorageProvider  # noqa: E402
from .google_drive import GoogleDriveStorageProvider  # noqa: E402
from .s3_provider import S3StorageProvider  # noqa: E402
from .sftp_provider import SFTPStorageProvider  # noqa: E402

StorageProviderRegistry.register(S3StorageProvider)
StorageProviderRegistry.register(SFTPStorageProvider)
StorageProviderRegistry.register(GoogleDriveStorageProvider)
StorageProviderRegistry.register(DropboxStorageProvider)
