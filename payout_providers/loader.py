"""
Payout Provider Loader

Dynamically loads payout provider classes from installed components
or built-in providers. Pattern follows exchange_rates/providers/loader.py architecture.
"""

import importlib
import json
import logging
import sys
import time

logger = logging.getLogger(__name__)


class PayoutProviderLoader:
    """
    Loads payout providers from component packages.

    Discovers providers from components_data/integrations/payout_providers/
    and loads them dynamically based on their manifest.json.
    """

    COMPONENT_TYPE = "payout_provider"

    _providers: dict[str, type] = {}
    _loaded = False
    _last_loaded_at: float = 0

    @classmethod
    def discover_providers(cls) -> dict[str, type]:
        """
        Discover and load all payout providers from components.

        Returns:
            Dictionary of {provider_key: ProviderClass}
        """
        from .providers.base import BasePayoutProvider

        if cls._loaded:
            return cls._providers

        # First load built-in providers
        cls._load_builtin_providers()

        # Then discover component providers (can override built-in)
        from component_updates.integration_paths import INTEGRATIONS_DIR, import_component_module

        components_path = INTEGRATIONS_DIR / "payout_provider"

        if not components_path.exists():
            logger.debug(f"Components path not found: {components_path}")
            cls._loaded = True
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
                with open(manifest_path) as f:
                    manifest = json.load(f)

                provider_key = manifest["provider_key"]
                entry_point = manifest.get("entry_point", "provider")
                class_name = manifest["class_name"]

                # Remove .py extension if present
                if entry_point.endswith(".py"):
                    entry_point = entry_point[:-3]

                # Import provider module using file-path-based loading
                module_name = f"payout_provider_{provider_dir.name}"
                module = import_component_module(current_path, entry_point, module_name)

                # Get provider class
                provider_class = getattr(module, class_name)

                # Validate it's a subclass of BasePayoutProvider
                if not issubclass(provider_class, BasePayoutProvider):
                    logger.error(f"{class_name} does not inherit from BasePayoutProvider")
                    continue

                cls._providers[provider_key] = provider_class
                logger.info(f"Loaded payout provider: {provider_key} ({class_name})")

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
    def _load_builtin_providers(cls):
        """Load built-in payout providers (PayPal, Airwallex)."""
        from .providers.base import BasePayoutProvider

        builtin_providers = {
            "paypal": ("payout_providers.providers.paypal", "PayPalPayoutProvider"),
            "airwallex": ("payout_providers.providers.airwallex", "AirwallexPayoutProvider"),
        }

        for provider_key, (module_path, class_name) in builtin_providers.items():
            try:
                module = importlib.import_module(module_path)
                provider_class = getattr(module, class_name)

                if issubclass(provider_class, BasePayoutProvider):
                    cls._providers[provider_key] = provider_class
                    logger.debug(f"Loaded built-in payout provider: {provider_key}")
                else:
                    logger.warning(f"{class_name} is not a BasePayoutProvider subclass")

            except ImportError:
                logger.debug(f"Built-in provider module not found: {module_path}")
            except AttributeError:
                logger.debug(f"Provider class {class_name} not found in {module_path}")
            except Exception as e:
                logger.error(f"Failed to load built-in provider {provider_key}: {e}")

    @classmethod
    def get_provider(cls, provider_key: str) -> type | None:
        """
        Get a specific provider by key.

        Args:
            provider_key: Provider identifier (e.g., 'paypal', 'airwallex')

        Returns:
            Provider class or None if not found
        """
        if not cls._loaded:
            cls.discover_providers()
        elif cls._cache_is_stale():
            logger.info("Cache marker detected — reloading payout providers from disk")
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
                # Create temporary instance with empty config to get metadata
                temp_instance = provider_class({})
                providers.append(
                    {
                        "key": key,
                        "name": temp_instance.display_name,
                        "provider_name": temp_instance.provider_name,
                        "supported_methods": [m.value for m in temp_instance.supported_methods],
                        "supported_currencies": temp_instance.supported_currencies,
                    }
                )
            except Exception as e:
                logger.warning(f"Could not instantiate {key} for metadata: {e}")
                providers.append(
                    {
                        "key": key,
                        "name": key.title(),
                        "provider_name": key,
                        "supported_methods": [],
                        "supported_currencies": [],
                    }
                )

        return providers

    @classmethod
    def reload_providers(cls):
        """
        Force reload of all providers.

        Clears the provider cache and removes provider modules from
        Python's module cache to ensure updated code is loaded.
        """
        # Clear our provider cache
        cls._providers = {}
        cls._loaded = False

        # Clear Python's module cache for component provider modules
        modules_to_remove = [
            module_name
            for module_name in list(sys.modules.keys())
            if module_name.startswith("payout_provider_")
        ]

        for module_name in modules_to_remove:
            del sys.modules[module_name]
            logger.debug(f"Removed cached module: {module_name}")

        # Rediscover and load providers
        cls.discover_providers()

        logger.info(f"Reloaded {len(cls._providers)} payout providers")


# Convenience alias
ProviderRegistry = PayoutProviderLoader


def get_provider_class(provider_type: str, component=None) -> type | None:
    """
    Get the provider class for a given provider type.

    Args:
        provider_type: The type of provider ('paypal', 'airwallex', etc.)
        component: Optional ComponentRegistry instance (for future component-specific loading)

    Returns:
        Provider class or None if not found
    """
    return PayoutProviderLoader.get_provider(provider_type)


def get_default_provider_for_method(method: str):
    """
    Get the default payout provider account for a given payout method.

    Args:
        method: The payout method ('paypal', 'bank_transfer', etc.)

    Returns:
        PayoutProviderAccount instance or None
    """
    from .models import PayoutProviderAccount

    # Map methods to provider types
    method_to_provider = {
        "paypal": "paypal",
        "bank_transfer": "airwallex",
        "bank_transfer_local": "airwallex",
        "bank_transfer_swift": "airwallex",
    }

    provider_type = method_to_provider.get(method)
    if not provider_type:
        return None

    return PayoutProviderAccount.objects.filter(
        provider_type=provider_type, is_active=True, is_default=True
    ).first()


def clear_provider_cache():
    """Clear the provider class cache (useful for testing)"""
    PayoutProviderLoader.reload_providers()
