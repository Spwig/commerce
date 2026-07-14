"""
Dynamic provider loading from component registry and builtin providers.

Pattern follows exchange_rates/providers/loader.py architecture.
"""

import logging
import time

from seo_generator.providers.base import BaseSEOProvider

logger = logging.getLogger(__name__)


class ProviderLoader:
    """
    Loads SEO providers from:
    1. Builtin providers (included with the app)
    2. Component packages (from components_data/integrations/seo_generator/)
    """

    COMPONENT_TYPE = "seo_generator_provider"

    _providers: dict[str, type[BaseSEOProvider]] = {}
    _loaded = False
    _last_loaded_at: float = 0

    @classmethod
    def discover_builtin_providers(cls):
        """
        Discover and load builtin SEO providers.

        Currently loads:
        - DeterministicSEOProvider: CPU-based keyword extraction and template generation
        """
        try:
            from seo_generator.providers.builtin import DeterministicSEOProvider

            cls._providers["deterministic"] = DeterministicSEOProvider
            logger.info("Loaded builtin SEO provider: deterministic (DeterministicSEOProvider)")
        except ImportError as e:
            logger.warning(f"Could not load builtin provider: {e}")

    @classmethod
    def discover_component_providers(cls):
        """
        Discover and load SEO providers from component packages.

        Looks for providers in: components_data/integrations/seo_generator_provider/
        """
        from component_updates.integration_paths import INTEGRATIONS_DIR, import_component_module

        components_path = INTEGRATIONS_DIR / "seo_generator_provider"

        if not components_path.exists():
            logger.debug(f"SEO component path not found: {components_path}")
            return

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
                module_name = f"seo_provider_{provider_dir.name}"
                module = import_component_module(current_path, entry_point, module_name)

                # Get provider class
                provider_class = getattr(module, class_name)

                # Validate it's a subclass of BaseSEOProvider
                if not issubclass(provider_class, BaseSEOProvider):
                    logger.error(f"{class_name} does not inherit from BaseSEOProvider")
                    continue

                cls._providers[provider_key] = provider_class
                logger.info(f"Loaded SEO provider: {provider_key} ({class_name})")

            except Exception as e:
                logger.error(f"Failed to load provider {provider_dir.name}: {e}")

    @classmethod
    def discover_providers(cls) -> dict[str, type[BaseSEOProvider]]:
        """
        Discover and load all SEO providers from builtin and components.

        Returns:
            Dictionary of {provider_key: ProviderClass}
        """
        if cls._loaded:
            return cls._providers

        # Load builtin providers first
        cls.discover_builtin_providers()

        # Then load component providers (can override builtin)
        cls.discover_component_providers()

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
    def get_provider(cls, provider_key: str) -> type[BaseSEOProvider] | None:
        """
        Get a specific provider by key.

        Args:
            provider_key: Provider identifier (e.g., 'deterministic', 'openai')

        Returns:
            Provider class or None if not found
        """
        if not cls._loaded:
            cls.discover_providers()
        elif cls._cache_is_stale():
            logger.info("Cache marker detected — reloading SEO providers from disk")
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
            try:
                # Create temporary instance to get metadata
                # Builtin providers don't need credentials
                temp_instance = provider_class()
                providers.append(temp_instance.get_provider_info())
            except Exception as e:
                # If we can't instantiate, get what we can from class attributes
                logger.warning(f"Could not instantiate {key} for metadata: {e}")
                providers.append(
                    {
                        "key": key,
                        "name": provider_class.provider_name or key,
                        "capabilities": {},
                        "requires_credentials": getattr(
                            provider_class, "requires_credentials", False
                        ),
                    }
                )

        return providers

    @classmethod
    def reload_providers(cls):
        """
        Force reload of all providers.

        Clears the provider cache and removes provider modules from Python's
        module cache to ensure updated code is loaded.
        """
        import sys

        # Clear our provider cache
        cls._providers = {}
        cls._loaded = False

        # Clear Python's module cache for SEO provider modules
        modules_to_remove = [
            module_name
            for module_name in list(sys.modules.keys())
            if module_name.startswith("seo_provider_")
        ]

        for module_name in modules_to_remove:
            del sys.modules[module_name]
            logger.debug(f"Removed cached module: {module_name}")

        # Rediscover and load providers
        cls.discover_providers()

        logger.info(f"Reloaded {len(cls._providers)} SEO providers")
