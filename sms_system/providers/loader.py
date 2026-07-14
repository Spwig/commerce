"""
Dynamic SMS provider loading from component registry.

Discovers SMS providers from components_data/integrations/sms/
and loads them dynamically based on their manifest.json.
"""

import json
import logging
import time
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class SMSProviderLoader:
    """
    Loads SMS providers from component packages.

    Discovers providers from components_data/integrations/sms/
    and loads them dynamically based on their manifest.json.
    """

    COMPONENT_TYPE = "sms_provider"

    _providers: dict[str, type] = {}
    _manifests: dict[str, dict[str, Any]] = {}
    _loaded = False
    _last_loaded_at: float = 0

    @classmethod
    def discover_providers(cls) -> dict[str, type]:
        """
        Discover and load all SMS providers from components.

        Returns:
            Dictionary of {provider_key: ProviderClass}
        """
        if cls._loaded:
            return cls._providers

        from component_updates.integration_paths import INTEGRATIONS_DIR, import_component_module

        components_path = INTEGRATIONS_DIR / "sms_provider"

        if not components_path.exists():
            logger.warning(f"SMS components path not found: {components_path}")
            cls._loaded = True
            return cls._providers

        # Iterate through provider directories
        for provider_dir in components_path.iterdir():
            if not provider_dir.is_dir():
                continue

            # Look for 'current' symlink pointing to version
            current_path = provider_dir / "current"
            if not current_path.exists():
                logger.debug(f"Skipping {provider_dir.name} - no 'current' symlink/directory")
                continue

            # Load manifest
            manifest_path = current_path / "manifest.json"
            if not manifest_path.exists():
                logger.warning(f"No manifest found for SMS provider {provider_dir.name}")
                continue

            try:
                with open(manifest_path) as f:
                    manifest = json.load(f)

                provider_key = manifest.get("provider_key")
                if not provider_key:
                    logger.warning(f"No provider_key in manifest for {provider_dir.name}")
                    continue

                entry_point = manifest.get("entry_point", "provider")
                class_name = manifest.get("class_name")

                if not class_name:
                    logger.warning(f"No class_name in manifest for {provider_dir.name}")
                    continue

                # Remove .py extension if present
                if entry_point.endswith(".py"):
                    entry_point = entry_point[:-3]

                # Import provider module using file-path-based loading
                module_name = f"sms_provider_{provider_dir.name}"
                module = import_component_module(current_path, entry_point, module_name)

                # Get provider class
                provider_class = getattr(module, class_name)

                cls._providers[provider_key] = provider_class
                cls._manifests[provider_key] = manifest
                logger.info(f"Loaded SMS provider: {provider_key} ({class_name})")

            except Exception as e:
                logger.error(f"Failed to load SMS provider {provider_dir.name}: {e}")

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
    def get_provider(cls, provider_key: str) -> type | None:
        """
        Get a specific provider class by key.

        Args:
            provider_key: Provider identifier (e.g., 'twilio')

        Returns:
            Provider class or None if not found
        """
        if not cls._loaded:
            cls.discover_providers()
        elif cls._cache_is_stale():
            logger.info("Cache marker detected — reloading SMS providers from disk")
            cls.reload_providers()

        return cls._providers.get(provider_key)

    @classmethod
    def get_manifest(cls, provider_key: str) -> dict[str, Any] | None:
        """
        Get the manifest for a specific provider.

        Args:
            provider_key: Provider identifier

        Returns:
            Manifest dictionary or None if not found
        """
        if not cls._loaded:
            cls.discover_providers()
        elif cls._cache_is_stale():
            cls.reload_providers()

        return cls._manifests.get(provider_key)

    @classmethod
    def list_providers(cls) -> list[dict[str, Any]]:
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
        for key, _provider_class in cls._providers.items():
            manifest = cls._manifests.get(key, {})

            providers.append(
                {
                    "key": key,
                    "name": manifest.get("name", key),
                    "description": manifest.get("description", ""),
                    "capabilities": manifest.get("capabilities", {}),
                    "version": manifest.get("version", "1.0.0"),
                    "logo": manifest.get("logo"),
                    "documentation_url": manifest.get("documentation_url", "")
                    or manifest.get("api_docs_url", ""),
                    "homepage_url": manifest.get("homepage_url", ""),
                    "setup": manifest.get("setup_wizard", manifest.get("setup", {})),
                    "translations": manifest.get("translations", {}),
                    "default_language": manifest.get("default_language", "en"),
                }
            )

        return providers

    @classmethod
    def get_credential_schema(cls, provider_key: str) -> dict[str, Any] | None:
        """
        Get the credential schema for a provider.

        Args:
            provider_key: Provider identifier

        Returns:
            Credential schema dictionary or None
        """
        manifest = cls.get_manifest(provider_key)
        if manifest:
            return manifest.get("credential_schema")
        return None

    @classmethod
    def reload_providers(cls):
        """
        Force reload of all providers.

        Clears the provider cache and removes provider modules from
        Python's module cache to ensure updated code is loaded.
        """
        import sys

        # Clear our caches
        cls._providers = {}
        cls._manifests = {}
        cls._loaded = False

        # Clear Python's module cache for SMS provider modules
        modules_to_remove = [
            module_name
            for module_name in list(sys.modules.keys())
            if module_name.startswith("sms_provider_")
        ]

        for module_name in modules_to_remove:
            del sys.modules[module_name]
            logger.debug(f"Removed cached module: {module_name}")

        # Rediscover and load providers
        cls.discover_providers()

        logger.info(f"Reloaded {len(cls._providers)} SMS providers")

    @classmethod
    def get_provider_path(cls, provider_key: str) -> Path | None:
        """
        Get the filesystem path to a provider's current version.

        Args:
            provider_key: Provider identifier

        Returns:
            Path to provider directory or None
        """
        from component_updates.integration_paths import INTEGRATIONS_DIR

        components_path = INTEGRATIONS_DIR / "sms_provider"

        if not components_path.exists():
            return None

        # Find the provider directory by checking manifests
        for provider_dir in components_path.iterdir():
            if not provider_dir.is_dir():
                continue

            current_path = provider_dir / "current"
            manifest_path = current_path / "manifest.json"

            if manifest_path.exists():
                try:
                    with open(manifest_path) as f:
                        manifest = json.load(f)
                        if manifest.get("provider_key") == provider_key:
                            return current_path
                except Exception:
                    pass

        return None

    @classmethod
    def get_setup_instructions(cls, provider_key: str) -> str | None:
        """
        Get the setup instructions HTML for a provider.

        Args:
            provider_key: Provider identifier

        Returns:
            HTML content string or None
        """
        provider_path = cls.get_provider_path(provider_key)
        if not provider_path:
            return None

        instructions_path = provider_path / "setup_instructions.html"
        if instructions_path.exists():
            try:
                with open(instructions_path, encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                logger.error(f"Failed to read setup instructions for {provider_key}: {e}")

        return None
