"""
Registry for POS terminal payment providers.

The registry scans the ComponentRegistry for terminal_provider components
and dynamically loads provider classes. Also includes built-in providers
(manual) that don't require a component package.
"""
import importlib.util
import logging
import sys
import time
from pathlib import Path
from typing import Dict, Optional, Type

from .base import TerminalProviderBase

logger = logging.getLogger(__name__)


class TerminalProviderRegistry:
    """
    Singleton registry for terminal provider discovery and access.

    The registry:
    1. Registers built-in providers (manual)
    2. Discovers terminal_provider components from ComponentRegistry
    3. Dynamically imports provider classes from component packages
    4. Caches loaded providers for performance
    5. Provides access to provider classes by key

    Usage:
        # Get a provider class
        provider_class = TerminalProviderRegistry.get_provider('stripe_terminal')

        # Create provider instance
        provider = provider_class(credentials={'secret_key': '...'})

        # List all available providers
        providers = TerminalProviderRegistry.list_providers()
    """

    COMPONENT_TYPE = 'terminal_provider'

    # Class-level cache of loaded providers
    _providers: Dict[str, Type[TerminalProviderBase]] = {}
    _discovered: bool = False
    _last_loaded_at: float = 0

    # Built-in providers that don't require component packages
    BUILTIN_PROVIDERS = ['manual']

    @classmethod
    def discover_providers(cls) -> None:
        """
        Discover and load all terminal providers.

        1. Registers built-in manual provider
        2. Scans ComponentRegistry for terminal_provider components
        3. Imports and registers provider classes from component packages

        This method is called automatically on first access and caches results.
        """
        if cls._discovered:
            return

        logger.info("Discovering terminal providers...")

        # 1. Register built-in manual provider
        try:
            from .manual import ManualTerminalProvider
            cls._providers['manual'] = ManualTerminalProvider
            logger.debug("Registered built-in provider: manual")
        except ImportError as e:
            logger.warning(f"Failed to load built-in manual provider: {e}")

        # 2. Scan ComponentRegistry for terminal_provider components
        try:
            from component_updates.models import ComponentRegistry

            provider_components = ComponentRegistry.objects.filter(
                component_type='terminal_provider'
            ).exclude(current_version__isnull=True)

            for component in provider_components:
                try:
                    cls._load_provider_from_component(component)
                except Exception as e:
                    logger.error(
                        f"Failed to load terminal provider '{component.slug}': {e}",
                        exc_info=True
                    )
                    continue

            cls._discovered = True
            cls._last_loaded_at = time.time()
            logger.info(f"Discovered {len(cls._providers)} terminal providers")

        except Exception as e:
            logger.error(f"Error discovering terminal providers: {e}", exc_info=True)
            cls._discovered = True  # Mark as discovered to prevent retry loops

    @classmethod
    def _load_provider_from_component(cls, component) -> None:
        """
        Load a provider class from a component package.

        Args:
            component: ComponentRegistry instance

        Raises:
            ImportError: If provider module cannot be imported
            ValueError: If provider class is invalid
        """
        from django.conf import settings
        import json

        # Resolve component directory path
        # Expected: components_data/integrations/terminal_provider/{slug}/current/
        from component_updates.integration_paths import INTEGRATIONS_DIR
        component_dir = INTEGRATIONS_DIR / 'terminal_provider' / component.slug / 'current'

        if not component_dir.exists():
            logger.warning(f"Component directory not found: {component_dir}")
            return

        # Load manifest
        manifest_path = component_dir / 'manifest.json'
        if not manifest_path.exists():
            logger.warning(f"Manifest not found: {manifest_path}")
            return

        try:
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load manifest for {component.slug}: {e}")
            return

        # Import provider module
        module_path = manifest.get('entry_point', 'provider')
        provider_class_name = manifest.get('class_name', 'Provider')

        try:
            # Dynamic import from component directory
            module = cls._import_provider_module(component_dir, module_path)

            # Get provider class
            provider_class = getattr(module, provider_class_name, None)

            if not provider_class:
                raise ValueError(f"Provider class '{provider_class_name}' not found in module")

            if not issubclass(provider_class, TerminalProviderBase):
                raise ValueError(f"Provider class must inherit from TerminalProviderBase")

            # Register provider
            provider_key = manifest.get('provider_key', component.slug)
            cls._providers[provider_key] = provider_class

            logger.info(
                f"Loaded terminal provider: {provider_key} ({provider_class_name}) from {component_dir}"
            )

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

        component_name = component_dir.parent.name  # e.g., 'stripe_terminal'
        package_name = f"terminal_provider_{component_name}"
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
    def get_provider(cls, provider_key: str) -> Optional[Type[TerminalProviderBase]]:
        """
        Get a provider class by its key.

        Args:
            provider_key: Unique provider identifier (e.g., 'stripe_terminal', 'manual')

        Returns:
            Provider class, or None if not found
        """
        if not cls._discovered:
            cls.discover_providers()
        elif cls._cache_is_stale():
            logger.info("Cache marker detected — reloading terminal providers from disk")
            cls.reload_providers()

        return cls._providers.get(provider_key)

    @classmethod
    def list_providers(cls) -> Dict[str, Type[TerminalProviderBase]]:
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
    def get_provider_choices(cls):
        """
        Return list of (key, name) tuples for Django model choices.

        Useful for populating choice fields in admin forms.
        """
        if not cls._discovered:
            cls.discover_providers()
        elif cls._cache_is_stale():
            cls.reload_providers()

        return [
            (key, klass.provider_name)
            for key, klass in sorted(cls._providers.items())
        ]

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
            Dictionary with provider info or None if not found
        """
        provider_class = cls.get_provider(provider_key)
        if not provider_class:
            return None

        return {
            'provider_key': provider_class.provider_key,
            'provider_name': provider_class.provider_name,
            'class_name': provider_class.__name__,
            'module': provider_class.__module__,
            'is_builtin': provider_key in cls.BUILTIN_PROVIDERS,
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
    def register(cls, provider_class: Type[TerminalProviderBase]) -> None:
        """
        Manually register a provider class (for testing or built-in providers).

        Args:
            provider_class: Provider class to register

        Raises:
            ValueError: If provider_class is invalid
        """
        if not issubclass(provider_class, TerminalProviderBase):
            raise ValueError("Provider class must inherit from TerminalProviderBase")

        if not provider_class.provider_key:
            raise ValueError("Provider class must set provider_key")

        cls._providers[provider_class.provider_key] = provider_class
        logger.debug(f"Registered terminal provider: {provider_class.provider_key}")

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
            logger.info(f"Unregistered terminal provider: {provider_key}")
            return True
        return False
