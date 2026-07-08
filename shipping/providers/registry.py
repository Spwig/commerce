"""
Provider registry for discovering and managing shipping providers.

The registry scans the ComponentRegistry for shipping_provider components
and dynamically loads provider classes.
"""
import importlib
import logging
import time
from typing import Dict, Optional, List, Type
from pathlib import Path

from shipping.providers.base import ProviderBase

logger = logging.getLogger(__name__)


class ProviderRegistry:
    """
    Singleton registry for shipping provider discovery and access.

    The registry:
    1. Discovers shipping_provider components from ComponentRegistry
    2. Dynamically imports provider classes
    3. Caches loaded providers for performance
    4. Provides access to provider classes by key

    Usage:
        # Get a provider class
        provider_class = ProviderRegistry.get_provider('easyship')

        # Create provider instance
        provider = provider_class(credentials={'api_key': '...'})

        # List all available providers
        providers = ProviderRegistry.list_providers()
    """

    COMPONENT_TYPE = 'shipping_provider'

    # Class-level cache of loaded providers
    _providers: Dict[str, Type[ProviderBase]] = {}
    _discovered: bool = False
    _last_loaded_at: float = 0

    @classmethod
    def discover_providers(cls) -> None:
        """
        Discover and load all shipping provider components.

        Scans ComponentRegistry for components of type 'shipping_provider',
        imports their main Python module, and registers provider classes.

        This method is called automatically on first access and caches results.
        """
        if cls._discovered:
            return

        logger.info("Discovering shipping providers...")

        try:
            from component_updates.models import ComponentRegistry

            # Query for all shipping provider components that have an installed version
            provider_components = ComponentRegistry.objects.filter(
                component_type='shipping_provider'
            ).exclude(current_version__isnull=True)

            for component in provider_components:
                try:
                    cls._load_provider_from_component(component)
                except Exception as e:
                    logger.error(
                        f"Failed to load provider '{component.slug}': {e}",
                        exc_info=True
                    )
                    continue

            cls._discovered = True
            cls._last_loaded_at = time.time()
            logger.info(f"Discovered {len(cls._providers)} shipping providers")

        except Exception as e:
            logger.error(f"Error discovering providers: {e}", exc_info=True)
            cls._discovered = True  # Mark as discovered to prevent retry loops

    @classmethod
    def _load_provider_from_component(cls, component) -> None:
        """
        Load a provider class from a component.

        Args:
            component: ComponentRegistry instance

        Raises:
            ImportError: If provider module cannot be imported
            ValueError: If provider class is invalid
        """
        from shipping.providers.loader import load_provider_manifest, validate_provider_package
        from component_updates.integration_paths import INTEGRATIONS_DIR

        # Resolve component directory path
        # Expected: components_data/integrations/shipping_provider/{slug}/current/
        component_dir = INTEGRATIONS_DIR / 'shipping_provider' / component.slug / 'current'

        if not component_dir.exists():
            logger.warning(f"Component directory not found: {component_dir}")
            return

        # Load and validate manifest
        try:
            manifest = load_provider_manifest(component_dir)
            validate_provider_package(manifest, component_dir)
        except Exception as e:
            logger.error(f"Failed to load/validate manifest for {component.slug}: {e}")
            return

        # Import provider module
        module_path = manifest.get('entry_point', 'provider')
        provider_class_name = manifest.get('class_name', 'Provider')

        try:
            # Dynamic import from component directory
            # Expected structure: components_data/integrations/shipping/{slug}/current/provider.py
            module = cls._import_provider_module(component_dir, module_path)

            # Get provider class
            provider_class = getattr(module, provider_class_name, None)

            if not provider_class:
                raise ValueError(f"Provider class '{provider_class_name}' not found in module")

            if not issubclass(provider_class, ProviderBase):
                raise ValueError(f"Provider class must inherit from ProviderBase")

            # Register provider
            provider_key = manifest.get('provider_key', component.slug)
            cls._providers[provider_key] = provider_class

            logger.info(f"Loaded provider: {provider_key} ({provider_class_name}) from {component_dir}")

        except ImportError as e:
            logger.error(f"Failed to import provider module '{module_path}': {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading provider class: {e}")
            raise

    @classmethod
    def _import_provider_module(cls, component_dir: Path, module_path: str):
        """
        Dynamically import a provider module from component directory.

        Args:
            component_dir: Path to component directory
            module_path: Relative module path (e.g., 'provider' or 'provider.py')

        Returns:
            Imported module

        Raises:
            ImportError: If module cannot be imported
        """
        # Delegate to the shared helper. It handles the file-path-based
        # spec loading AND purges stale submodule entries from
        # sys.modules first so hot-reload after a component upgrade
        # doesn't silently return the pre-upgrade class via a cached
        # submodule reference in the package's __init__.py.
        from component_updates.integration_paths import import_component_module

        component_name = component_dir.parent.name  # e.g., 'australiapost'
        package_name = f"shipping_provider_{component_name}"
        return import_component_module(component_dir, module_path, package_name)

    @classmethod
    def _cache_is_stale(cls) -> bool:
        """Check if provider files on disk are newer than our in-memory cache."""
        try:
            from component_updates.integration_paths import provider_cache_is_stale
            return provider_cache_is_stale(cls.COMPONENT_TYPE, cls._last_loaded_at)
        except Exception:
            return False

    @classmethod
    def get_provider(cls, provider_key: str) -> Optional[Type[ProviderBase]]:
        """
        Get a provider class by its key.

        Args:
            provider_key: Unique provider identifier (e.g., 'easyship')

        Returns:
            Provider class, or None if not found

        Example:
            provider_class = ProviderRegistry.get_provider('easyship')
            if provider_class:
                provider = provider_class(credentials={'api_key': '...'})
        """
        if not cls._discovered:
            cls.discover_providers()
        elif cls._cache_is_stale():
            logger.info("Cache marker detected — reloading shipping providers from disk")
            cls.reload_providers()

        return cls._providers.get(provider_key)

    @classmethod
    def list_providers(cls) -> Dict[str, Type[ProviderBase]]:
        """
        Get dictionary of all registered providers.

        Returns:
            Dictionary mapping provider_key to provider class

        Example:
            providers = ProviderRegistry.list_providers()
            for key, provider_class in providers.items():
                print(f"{key}: {provider_class.provider_name}")
        """
        if not cls._discovered:
            cls.discover_providers()
        elif cls._cache_is_stale():
            cls.reload_providers()

        return cls._providers.copy()

    @classmethod
    def is_registered(cls, provider_key: str) -> bool:
        """
        Check if a provider is registered.

        Args:
            provider_key: Provider identifier

        Returns:
            True if provider is registered
        """
        if not cls._discovered:
            cls.discover_providers()
        elif cls._cache_is_stale():
            cls.reload_providers()

        return provider_key in cls._providers

    @classmethod
    def get_provider_info(cls, provider_key: str) -> Optional[Dict]:
        """
        Get information about a provider without instantiating it.

        Args:
            provider_key: Provider identifier

        Returns:
            Dictionary with provider info:
            {
                'provider_key': 'easyship',
                'provider_name': 'Easyship',
                'class_name': 'EasyshipProvider',
                'capabilities': {...},
                'credential_schema': {...}
            }
        """
        provider_class = cls.get_provider(provider_key)
        if not provider_class:
            return None

        # Access class attributes without instantiation
        return {
            'provider_key': provider_class.provider_key,
            'provider_name': provider_class.provider_name,
            'class_name': provider_class.__name__,
            'module': provider_class.__module__,
        }

    @classmethod
    def reload_providers(cls) -> None:
        """
        Clear cache and force re-discovery of providers.

        Useful during development or after installing new provider components.
        """
        cls._providers.clear()
        cls._discovered = False
        cls.discover_providers()

    @classmethod
    def register_provider(cls, provider_class: Type[ProviderBase]) -> None:
        """
        Manually register a provider class (useful for testing).

        Args:
            provider_class: Provider class to register

        Raises:
            ValueError: If provider_class is invalid
        """
        if not issubclass(provider_class, ProviderBase):
            raise ValueError("Provider class must inherit from ProviderBase")

        if not provider_class.provider_key:
            raise ValueError("Provider class must set provider_key")

        cls._providers[provider_class.provider_key] = provider_class
        logger.info(f"Manually registered provider: {provider_class.provider_key}")

    @classmethod
    def unregister_provider(cls, provider_key: str) -> bool:
        """
        Unregister a provider (useful for testing).

        Args:
            provider_key: Provider identifier

        Returns:
            True if provider was unregistered, False if not found
        """
        if provider_key in cls._providers:
            del cls._providers[provider_key]
            logger.info(f"Unregistered provider: {provider_key}")
            return True
        return False
