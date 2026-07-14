"""
Dynamic provider loading from component registry.

Pattern follows shipping/providers/loader.py architecture.
"""

import logging
import time

from exchange_rates.providers.base import ExchangeRateProviderBase

logger = logging.getLogger(__name__)


class ProviderLoader:
    """
    Loads exchange rate providers from component packages.

    Discovers providers from components_data/integrations/exchange_rates/
    and loads them dynamically based on their manifest.json.
    """

    COMPONENT_TYPE = "exchange_rate_provider"

    _providers: dict[str, type[ExchangeRateProviderBase]] = {}
    _loaded = False
    _last_loaded_at: float = 0

    @classmethod
    def discover_providers(cls) -> dict[str, type[ExchangeRateProviderBase]]:
        """
        Discover and load all exchange rate providers from components.

        Returns:
            Dictionary of {provider_key: ProviderClass}
        """
        if cls._loaded:
            return cls._providers

        from component_updates.integration_paths import INTEGRATIONS_DIR, import_component_module

        components_path = INTEGRATIONS_DIR / "exchange_rate_provider"

        if not components_path.exists():
            logger.warning(f"Components path not found: {components_path}")
            return cls._providers

        # Iterate through provider directories
        for provider_dir in components_path.iterdir():
            if not provider_dir.is_dir():
                continue

            # Look for 'current' symlink pointing to version
            current_path = provider_dir / "current"
            if not current_path.exists() or not current_path.is_symlink():
                logger.debug(f"Skipping {provider_dir.name} - no 'current' symlink")
                continue

            # Load manifest
            manifest_path = current_path / "manifest.json"
            if not manifest_path.exists():
                logger.warning(f"No manifest found for {provider_dir.name}")
                continue

            try:
                import json

                with open(manifest_path) as f:
                    manifest = json.load(f)

                provider_key = manifest["provider_key"]
                entry_point = manifest.get("entry_point", "provider")
                class_name = manifest["class_name"]

                # Remove .py extension if present
                if entry_point.endswith(".py"):
                    entry_point = entry_point[:-3]

                # Import provider module using file-path-based loading
                module_name = f"exchange_rate_provider_{provider_dir.name}"
                module = import_component_module(current_path, entry_point, module_name)

                # Get provider class
                provider_class = getattr(module, class_name)

                # Validate it's a subclass of ExchangeRateProviderBase
                if not issubclass(provider_class, ExchangeRateProviderBase):
                    logger.error(f"{class_name} does not inherit from ExchangeRateProviderBase")
                    continue

                cls._providers[provider_key] = provider_class
                logger.info(f"Loaded exchange rate provider: {provider_key} ({class_name})")

            except Exception as e:
                logger.error(f"Failed to load provider {provider_dir.name}: {e}")

        cls._loaded = True
        cls._last_loaded_at = time.time()
        return cls._providers

    @classmethod
    def _cache_is_stale(cls) -> bool:
        """Check if provider files on disk are newer than our in-memory cache."""
        try:
            from component_updates.integration_paths import provider_cache_is_stale

            return provider_cache_is_stale(cls.COMPONENT_TYPE, cls._last_loaded_at)
        except Exception:
            return False

    @classmethod
    def get_provider(cls, provider_key: str) -> type[ExchangeRateProviderBase] | None:
        """
        Get a specific provider by key.

        Args:
            provider_key: Provider identifier (e.g., 'openexchangerates')

        Returns:
            Provider class or None if not found
        """
        if not cls._loaded:
            cls.discover_providers()
        elif cls._cache_is_stale():
            logger.info("Cache marker detected — reloading exchange rate providers from disk")
            cls.reload_providers()

        return cls._providers.get(provider_key)

    @classmethod
    def list_providers(cls) -> list[dict]:
        """
        List all available providers with metadata.

        Returns:
            List of provider info dictionaries
        """
        if not cls._loaded:
            cls.discover_providers()
        elif cls._cache_is_stale():
            cls.reload_providers()

        providers = []
        for key, provider_class in cls._providers.items():
            # Get metadata from class
            try:
                # Create temporary instance with empty credentials to get metadata
                # This is safe because we're only calling get_provider_info()
                temp_instance = provider_class(credentials={})
                providers.append(temp_instance.get_provider_info())
            except Exception as e:
                # If we can't instantiate, get what we can from class attributes
                logger.warning(f"Could not instantiate {key} for metadata: {e}")
                providers.append(
                    {
                        "key": key,
                        "name": provider_class.provider_name or key,
                        "capabilities": {},
                    }
                )

        return providers

    @classmethod
    def reload_providers(cls):
        """
        Force reload of all providers.

        This clears the provider cache and also removes provider modules from
        Python's module cache to ensure updated code is loaded without requiring
        a server restart. This is essential for production environments where
        providers may be updated via the component update system.
        """
        import sys

        # Clear our provider cache
        cls._providers = {}
        cls._loaded = False

        # Clear Python's module cache for all provider modules
        # This ensures that updated provider code is loaded from disk
        modules_to_remove = [
            module_name
            for module_name in list(sys.modules.keys())
            if module_name.startswith("exchange_rate_provider_")
        ]

        for module_name in modules_to_remove:
            del sys.modules[module_name]
            logger.debug(f"Removed cached module: {module_name}")

        # Rediscover and load providers
        cls.discover_providers()

        logger.info(f"Reloaded {len(cls._providers)} exchange rate providers")
