"""
Dynamic provider loading from component registry.

Pattern follows exchange_rates/providers/loader.py architecture.
"""

import logging
import time

from email_system.providers.base import EmailProviderBase

logger = logging.getLogger(__name__)


class ProviderLoader:
    """
    Loads email providers from component packages.

    Discovers providers from components_data/integrations/email_providers/
    and loads them dynamically based on their manifest.json.
    """

    COMPONENT_TYPE = "email_provider"

    _providers: dict[str, type[EmailProviderBase]] = {}
    _loaded = False
    _last_loaded_at: float = 0

    @classmethod
    def _load_builtin_provider(cls):
        """
        Load the built-in SMTP provider.

        The built-in provider is not a component package, it's part of the
        email_system app and always available.
        """
        try:
            from email_system.providers.builtin.provider import BuiltinSMTPProvider

            cls._providers["builtin_smtp"] = BuiltinSMTPProvider
            logger.info("Loaded built-in SMTP provider: builtin_smtp")

        except Exception as e:
            logger.error(f"Failed to load built-in SMTP provider: {e}")

    @classmethod
    def _load_spwig_hosted_provider(cls):
        """
        Load the Spwig Hosted Mail provider.

        Built-in provider for Spwig-hosted deployments. Sends through the
        centralized Spwig Mail Gateway. Always loaded (availability gated
        by is_spwig_hosted() in the wizard and admin UI).
        """
        try:
            from email_system.providers.spwig_hosted.provider import SpwigHostedMailProvider

            cls._providers["spwig_hosted_mail"] = SpwigHostedMailProvider
            logger.info("Loaded Spwig Hosted Mail provider: spwig_hosted_mail")

        except Exception as e:
            logger.error(f"Failed to load Spwig Hosted Mail provider: {e}")

    @classmethod
    def discover_providers(cls) -> dict[str, type[EmailProviderBase]]:
        """
        Discover and load all email providers from components.

        Returns:
            Dictionary of {provider_key: ProviderClass}
        """
        if cls._loaded:
            return cls._providers

        # Load built-in SMTP provider first (always available)
        cls._load_builtin_provider()

        # Load Spwig Hosted Mail provider (for hosted deployments)
        cls._load_spwig_hosted_provider()

        from component_updates.integration_paths import INTEGRATIONS_DIR, import_component_module

        components_path = INTEGRATIONS_DIR / "email_provider"

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
                module_name = f"email_provider_{provider_dir.name}"
                module = import_component_module(current_path, entry_point, module_name)

                # Get provider class
                provider_class = getattr(module, class_name)

                # Validate it's a subclass of EmailProviderBase
                if not issubclass(provider_class, EmailProviderBase):
                    logger.error(f"{class_name} does not inherit from EmailProviderBase")
                    continue

                cls._providers[provider_key] = provider_class
                logger.info(f"Loaded email provider: {provider_key} ({class_name})")

            except Exception as e:
                logger.error(f"Failed to load provider {provider_dir.name}: {e}")

        cls._loaded = True
        cls._last_loaded_at = time.time()
        return cls._providers

    @classmethod
    def _cache_is_stale(cls) -> bool:
        """Check if provider files on disk are newer than our in-memory cache.

        Uses a file-based marker written by the component update system.
        Cost: one os.stat() call, typically < 0.1ms (served from VFS cache).
        """
        try:
            from component_updates.integration_paths import provider_cache_is_stale

            return provider_cache_is_stale(cls.COMPONENT_TYPE, cls._last_loaded_at)
        except Exception:
            return False

    @classmethod
    def get_provider(cls, provider_key: str) -> type[EmailProviderBase] | None:
        """
        Get a specific provider by key.

        Args:
            provider_key: Provider identifier (e.g., 'gmail_api')

        Returns:
            Provider class or None if not found
        """
        if not cls._loaded:
            cls.discover_providers()
        elif cls._cache_is_stale():
            logger.info("Provider cache marker detected — reloading email providers from disk")
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
            # Get metadata from class attributes
            try:
                providers.append(
                    {
                        "key": provider_class.provider_key,
                        "name": provider_class.provider_name,
                    }
                )
            except Exception as e:
                logger.warning(f"Could not get metadata for {key}: {e}")
                providers.append(
                    {
                        "key": key,
                        "name": key,
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
            if module_name.startswith("email_provider_")
        ]

        for module_name in modules_to_remove:
            del sys.modules[module_name]
            logger.debug(f"Removed cached module: {module_name}")

        # Rediscover and load providers (also updates _last_loaded_at)
        cls.discover_providers()

        logger.info(f"Reloaded {len(cls._providers)} email providers")
