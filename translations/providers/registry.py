"""
Provider registry for discovering and managing translation providers.

The registry scans the ComponentRegistry for translation_provider components
and dynamically loads provider classes.
"""
import logging
import time
from typing import Dict, Optional, Type
from pathlib import Path

from translations.providers.base import TranslationProviderBase

logger = logging.getLogger(__name__)


class ProviderRegistry:
    """
    Singleton registry for translation provider discovery and access.

    The registry:
    1. Discovers translation_provider components from ComponentRegistry
    2. Dynamically imports provider classes
    3. Caches loaded providers for performance
    4. Provides access to provider classes by key

    Usage:
        # Get a provider class
        provider_class = ProviderRegistry.get_provider('deepl')

        # Create provider instance
        provider = provider_class(credentials={'api_key': '...'})

        # List all available providers
        providers = ProviderRegistry.list_providers()
    """

    COMPONENT_TYPE = 'translation_provider'

    # Class-level cache of loaded providers
    _providers: Dict[str, Type[TranslationProviderBase]] = {}
    _manifests: Dict[str, dict] = {}
    _discovered: bool = False
    _last_loaded_at: float = 0

    @classmethod
    def discover_providers(cls) -> None:
        """
        Discover and load all translation provider components.

        Scans ComponentRegistry for components of type 'translation_provider',
        imports their main Python module, and registers provider classes.
        """
        if cls._discovered:
            return

        logger.info("Discovering translation providers...")

        try:
            from component_updates.models import ComponentRegistry

            provider_components = ComponentRegistry.objects.filter(
                component_type='translation_provider'
            ).exclude(current_version__isnull=True)

            for component in provider_components:
                try:
                    cls._load_provider_from_component(component)
                except Exception as e:
                    logger.error(
                        f"Failed to load translation provider '{component.slug}': {e}",
                        exc_info=True
                    )
                    continue

            cls._discovered = True
            cls._last_loaded_at = time.time()
            logger.info(f"Discovered {len(cls._providers)} translation providers")

        except Exception as e:
            logger.error(f"Error discovering translation providers: {e}", exc_info=True)
            cls._discovered = True

    @classmethod
    def _load_provider_from_component(cls, component) -> None:
        """
        Load a provider class from a component.
        """
        from component_updates.integration_paths import INTEGRATIONS_DIR, import_component_module

        component_dir = INTEGRATIONS_DIR / 'translation_provider' / component.slug / 'current'

        if not component_dir.exists():
            logger.warning(f"Component directory not found: {component_dir}")
            return

        # Load manifest
        manifest = cls._load_manifest(component_dir)
        if not manifest:
            return

        # Import provider module
        module_path = manifest.get('entry_point', 'provider')
        provider_class_name = manifest.get('class_name', 'Provider')
        module_name = f"translation_provider_{component.slug}"

        try:
            module = import_component_module(component_dir, module_path, module_name)

            provider_class = getattr(module, provider_class_name, None)

            if not provider_class:
                raise ValueError(f"Provider class '{provider_class_name}' not found in module")

            if not issubclass(provider_class, TranslationProviderBase):
                raise ValueError(f"Provider class must inherit from TranslationProviderBase")

            provider_key = manifest.get('provider_key', component.slug)
            cls._providers[provider_key] = provider_class
            cls._manifests[provider_key] = manifest

            logger.info(f"Loaded translation provider: {provider_key} ({provider_class_name})")

        except ImportError as e:
            logger.error(f"Failed to import provider module '{module_path}': {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading provider class: {e}")
            raise

    @classmethod
    def _load_manifest(cls, component_dir: Path) -> Optional[dict]:
        """Load and return manifest.json from component directory."""
        import json
        manifest_path = component_dir / 'manifest.json'
        if not manifest_path.exists():
            logger.error(f"No manifest.json found in {component_dir}")
            return None
        try:
            with open(manifest_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load manifest from {component_dir}: {e}")
            return None

    @classmethod
    def _cache_is_stale(cls) -> bool:
        """Check if provider files on disk are newer than our in-memory cache."""
        try:
            from component_updates.integration_paths import provider_cache_is_stale
            return provider_cache_is_stale(cls.COMPONENT_TYPE, cls._last_loaded_at)
        except Exception:
            return False

    @classmethod
    def get_provider(cls, provider_key: str) -> Optional[Type[TranslationProviderBase]]:
        """
        Get a provider class by its key.

        Args:
            provider_key: Unique provider identifier (e.g., 'deepl')

        Returns:
            Provider class, or None if not found
        """
        if not cls._discovered:
            cls.discover_providers()
        elif cls._cache_is_stale():
            logger.info("Cache marker detected — reloading translation providers from disk")
            cls.reload_providers()

        return cls._providers.get(provider_key)

    @classmethod
    def get_manifest(cls, provider_key: str) -> Optional[dict]:
        """
        Get the manifest data for a provider.

        Args:
            provider_key: Provider identifier

        Returns:
            Manifest dictionary, or None if not found
        """
        if not cls._discovered:
            cls.discover_providers()
        elif cls._cache_is_stale():
            cls.reload_providers()

        return cls._manifests.get(provider_key)

    @classmethod
    def list_providers(cls) -> Dict[str, Type[TranslationProviderBase]]:
        """
        Get dictionary of all registered providers.

        Returns:
            Dictionary mapping provider_key to provider class
        """
        if not cls._discovered:
            cls.discover_providers()
        elif cls._cache_is_stale():
            cls.reload_providers()

        return cls._providers.copy()

    @classmethod
    def list_manifests(cls) -> Dict[str, dict]:
        """
        Get dictionary of all provider manifests.

        Returns:
            Dictionary mapping provider_key to manifest dict
        """
        if not cls._discovered:
            cls.discover_providers()
        elif cls._cache_is_stale():
            cls.reload_providers()

        return cls._manifests.copy()

    @classmethod
    def is_registered(cls, provider_key: str) -> bool:
        """Check if a provider is registered."""
        if not cls._discovered:
            cls.discover_providers()
        elif cls._cache_is_stale():
            cls.reload_providers()

        return provider_key in cls._providers

    @classmethod
    def get_provider_info(cls, provider_key: str) -> Optional[Dict]:
        """
        Get information about a provider without instantiating it.
        """
        provider_class = cls.get_provider(provider_key)
        if not provider_class:
            return None

        manifest = cls._manifests.get(provider_key, {})
        return {
            'provider_key': provider_class.provider_key,
            'provider_name': provider_class.provider_name,
            'class_name': provider_class.__name__,
            'capabilities': manifest.get('capabilities', {}),
            'credential_schema': manifest.get('credential_schema', {}),
            'signup_url': manifest.get('signup_url', ''),
            'logo': manifest.get('logo', {}),
        }

    @classmethod
    def reload_providers(cls) -> None:
        """Clear cache and force re-discovery of providers."""
        cls._providers.clear()
        cls._manifests.clear()
        cls._discovered = False
        cls.discover_providers()

    @classmethod
    def register_provider(cls, provider_class: Type[TranslationProviderBase],
                          manifest: Optional[dict] = None) -> None:
        """Manually register a provider class (useful for testing)."""
        if not issubclass(provider_class, TranslationProviderBase):
            raise ValueError("Provider class must inherit from TranslationProviderBase")

        if not provider_class.provider_key:
            raise ValueError("Provider class must set provider_key")

        cls._providers[provider_class.provider_key] = provider_class
        if manifest:
            cls._manifests[provider_class.provider_key] = manifest
        logger.info(f"Manually registered translation provider: {provider_class.provider_key}")

    @classmethod
    def unregister_provider(cls, provider_key: str) -> bool:
        """Unregister a provider (useful for testing)."""
        removed = provider_key in cls._providers
        cls._providers.pop(provider_key, None)
        cls._manifests.pop(provider_key, None)
        if removed:
            logger.info(f"Unregistered translation provider: {provider_key}")
        return removed
