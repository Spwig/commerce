"""
Provider Registry for SEO Providers.
Pattern follows exchange_rates/providers/registry.py.

Uses ProviderLoader to dynamically discover providers from builtin and components.
"""

import logging
from typing import Dict, List, Optional, Type

from seo_generator.providers.base import BaseSEOProvider, ProviderNotAvailable
from seo_generator.providers.loader import ProviderLoader

logger = logging.getLogger(__name__)


class ProviderRegistry:
    """
    Central registry for SEO providers.

    Uses ProviderLoader to discover providers from builtin providers
    and component packages.
    """

    @classmethod
    def get_provider(cls, provider_key: str) -> Optional[Type[BaseSEOProvider]]:
        """
        Get provider class by key.

        Args:
            provider_key: Provider identifier (e.g., 'deterministic', 'openai')

        Returns:
            Provider class or None if not found
        """
        return ProviderLoader.get_provider(provider_key)

    @classmethod
    def list_providers(cls) -> List[Dict]:
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
    def get_provider_choices(cls) -> List[tuple]:
        """
        Get provider choices for Django form fields.

        Returns:
            List of (provider_key, provider_name) tuples
        """
        providers = cls.list_providers()
        return [(p['key'], p['name']) for p in sorted(providers, key=lambda x: x['name'])]

    @classmethod
    def get_default_provider(cls) -> Optional[Type[BaseSEOProvider]]:
        """
        Get the default provider (builtin deterministic provider).

        Returns:
            DeterministicSEOProvider class or None if not found
        """
        return cls.get_provider('deterministic')

    @classmethod
    def get_primary_provider_instance(cls) -> BaseSEOProvider:
        """
        Get the merchant's primary provider, fully initialized with credentials.

        Falls back to deterministic provider if no primary is configured.

        Returns:
            Initialized BaseSEOProvider instance

        Raises:
            ProviderNotAvailable: If no provider can be resolved
        """
        from seo_generator.models import SEOProviderAccount

        try:
            account = SEOProviderAccount.objects.get(is_primary=True, is_active=True)
            return account.get_provider_instance()
        except SEOProviderAccount.DoesNotExist:
            provider_class = cls.get_provider('deterministic')
            if provider_class:
                return provider_class()
            raise ProviderNotAvailable("No SEO provider available")

    @classmethod
    def get_provider_instance(cls, provider_key: Optional[str] = None) -> BaseSEOProvider:
        """
        Get an initialized provider instance by key, with credentials if needed.

        If provider_key is None or empty, returns the primary provider.
        If provider_key is 'deterministic', returns builtin (no credentials needed).
        Otherwise, looks up the SEOProviderAccount for that provider key.

        Args:
            provider_key: Optional provider key. None = primary provider.

        Returns:
            Initialized BaseSEOProvider instance

        Raises:
            ProviderNotAvailable: If the requested provider cannot be resolved
        """
        if not provider_key:
            return cls.get_primary_provider_instance()

        if provider_key == 'deterministic':
            provider_class = cls.get_provider('deterministic')
            if provider_class:
                return provider_class()
            raise ProviderNotAvailable("Deterministic provider not found")

        # External provider - look up account for credentials
        from seo_generator.models import SEOProviderAccount
        from django.db.models import Q

        try:
            account = SEOProviderAccount.objects.get(
                Q(provider_key=provider_key) | Q(component__slug=provider_key),
                is_active=True
            )
            return account.get_provider_instance()
        except SEOProviderAccount.DoesNotExist:
            raise ProviderNotAvailable(
                f"Provider '{provider_key}' not configured. "
                f"Set up a provider account first."
            )
