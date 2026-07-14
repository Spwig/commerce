"""
Provider Registry for Email Providers.
Pattern follows exchange_rates/providers/registry.py.

Uses ProviderLoader to dynamically discover providers from components.
"""

from email_system.providers.base import EmailProviderBase
from email_system.providers.loader import ProviderLoader


class ProviderRegistry:
    """
    Central registry for email providers.

    Uses ProviderLoader to discover providers from component packages.
    """

    @classmethod
    def get_provider(cls, provider_key: str) -> type[EmailProviderBase] | None:
        """
        Get provider class by key.

        Args:
            provider_key: Provider identifier (e.g., 'gmail_api')

        Returns:
            Provider class or None if not found
        """
        return ProviderLoader.get_provider(provider_key)

    @classmethod
    def list_providers(cls) -> list[dict]:
        """
        List all available providers with metadata.

        Returns:
            List of provider info dictionaries
        """
        return ProviderLoader.list_providers()

    @classmethod
    def is_provider_installed(cls, provider_key: str) -> bool:
        """
        Check if provider is installed.

        Args:
            provider_key: Provider identifier

        Returns:
            True if provider is installed, False otherwise
        """
        return ProviderLoader.get_provider(provider_key) is not None

    @classmethod
    def reload_providers(cls):
        """Reload all providers from disk."""
        ProviderLoader.reload_providers()

    @classmethod
    def get_provider_choices(cls) -> list[tuple]:
        """
        Get provider choices for Django form fields.

        Returns:
            List of (provider_key, provider_name) tuples
        """
        providers = cls.list_providers()
        return [(p["key"], p["name"]) for p in sorted(providers, key=lambda x: x["name"])]
