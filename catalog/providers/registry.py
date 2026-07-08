"""
License Provider Registry

Discovers and caches available license provider adapters.
Follows the same pattern as payment and shipping provider registries.
"""

import os
import importlib
import json
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional, Type
from django.conf import settings
from catalog.providers.base import BaseLicenseProviderAdapter

logger = logging.getLogger(__name__)


class LicenseProviderRegistry:
    """
    Central registry for discovering and caching license provider implementations.

    This registry discovers providers from:
    1. Built-in providers (catalog/providers/builtin/)
    2. Component-based providers (components_data/integrations/license_server_providers/)

    Usage:
        # Get a provider class
        provider_class = LicenseProviderRegistry.get_provider('keygen')

        # List all available providers
        providers = LicenseProviderRegistry.list_providers()

        # Force reload (after updates)
        LicenseProviderRegistry.reload_providers()
    """

    COMPONENT_TYPE = 'license_server_provider'

    _providers: Dict[str, Type[BaseLicenseProviderAdapter]] = {}
    _discovered: bool = False
    _last_loaded_at: float = 0

    @classmethod
    def discover_providers(cls):
        """
        Discover all available license providers.

        Scans both:
        1. builtin/ directory for provider modules (fallback)
        2. components_data/integrations/license_server_providers/ for component-based providers
        """
        if cls._discovered:
            return

        logger.info("Discovering license providers...")

        # Discover component-based providers first (preferred)
        cls._discover_component_providers()

        # Discover built-in providers as fallback (for providers not yet componentized)
        cls._discover_builtin_providers()

        cls._discovered = True
        cls._last_loaded_at = time.time()
        logger.info(f"Discovered {len(cls._providers)} license providers: {', '.join(cls._providers.keys())}")

    @classmethod
    def _discover_builtin_providers(cls):
        """Discover providers in catalog/providers/builtin/ directory"""
        builtin_dir = os.path.join(os.path.dirname(__file__), 'builtin')

        if not os.path.exists(builtin_dir):
            logger.warning(f"Built-in providers directory not found: {builtin_dir}")
            return

        # Scan for Python files in builtin directory
        for filename in os.listdir(builtin_dir):
            if filename.startswith('_') or not filename.endswith('.py'):
                continue

            module_name = filename[:-3]  # Remove .py extension

            try:
                # Import the provider module
                module_path = f'catalog.providers.builtin.{module_name}'
                module = importlib.import_module(module_path)

                # Find adapter classes in the module
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)

                    # Check if it's a provider adapter class
                    if (
                        isinstance(attr, type) and
                        issubclass(attr, BaseLicenseProviderAdapter) and
                        attr is not BaseLicenseProviderAdapter and
                        hasattr(attr, 'provider_key') and
                        attr.provider_key is not None
                    ):
                        # Register the provider only if not already registered (component providers take precedence)
                        if attr.provider_key not in cls._providers:
                            cls._providers[attr.provider_key] = attr
                            logger.debug(f"Registered builtin provider: {attr.provider_key} ({attr.provider_name})")
                        else:
                            logger.debug(f"Skipping builtin provider {attr.provider_key} - component version already loaded")

            except Exception as e:
                logger.error(f"Failed to load provider module {module_name}: {e}")
                continue

    @classmethod
    def _discover_component_providers(cls):
        """
        Discover component-based providers from components_data/integrations/license_server_providers/.

        Loads providers from component packages, reading manifest.json for metadata
        and dynamically importing provider classes.
        """
        from component_updates.integration_paths import INTEGRATIONS_DIR, import_component_module

        components_path = INTEGRATIONS_DIR / 'license_server_provider'

        if not components_path.exists():
            logger.debug(f"Component providers path not found: {components_path}")
            return

        # Iterate through provider directories
        for provider_dir in components_path.iterdir():
            if not provider_dir.is_dir():
                continue

            # Look for 'current' symlink pointing to active version
            current_path = provider_dir / 'current'
            if not current_path.exists() or not current_path.is_symlink():
                logger.debug(f"Skipping {provider_dir.name} - no 'current' symlink")
                continue

            # Load manifest.json
            manifest_path = current_path / 'manifest.json'
            if not manifest_path.exists():
                logger.warning(f"No manifest.json found for {provider_dir.name}")
                continue

            try:
                with open(manifest_path) as f:
                    manifest = json.load(f)

                provider_key = manifest['provider_key']
                entry_point = manifest.get('entry_point', 'provider')
                class_name = manifest['class_name']

                # Remove .py extension if present
                if entry_point.endswith('.py'):
                    entry_point = entry_point[:-3]

                # Import provider module using file-path-based loading
                module_name = f"license_provider_{provider_dir.name}"
                module = import_component_module(current_path, entry_point, module_name)

                # Get provider class
                provider_class = getattr(module, class_name)

                # Validate it's a subclass of BaseLicenseProviderAdapter
                if not issubclass(provider_class, BaseLicenseProviderAdapter):
                    logger.error(f"{class_name} does not inherit from BaseLicenseProviderAdapter")
                    continue

                # Store manifest data on the class for later use
                provider_class._manifest = manifest
                provider_class._component_path = current_path

                cls._providers[provider_key] = provider_class
                logger.info(f"Loaded license provider component: {provider_key} ({class_name}) v{manifest.get('version', 'unknown')}")

            except Exception as e:
                logger.error(f"Failed to load provider component {provider_dir.name}: {e}")
                import traceback
                logger.debug(traceback.format_exc())

    @classmethod
    def _cache_is_stale(cls) -> bool:
        """Check if provider files on disk are newer than our in-memory cache."""
        try:
            from component_updates.integration_paths import provider_cache_is_stale
            return provider_cache_is_stale(cls.COMPONENT_TYPE, cls._last_loaded_at)
        except Exception:
            return False

    @classmethod
    def get_provider(cls, provider_type: str) -> Optional[Type[BaseLicenseProviderAdapter]]:
        """
        Get provider class by provider type/key.

        Args:
            provider_type: Provider key (e.g., 'keygen', 'licensespring', 'spwig_server')

        Returns:
            Provider adapter class or None if not found
        """
        if not cls._discovered:
            cls.discover_providers()
        elif cls._cache_is_stale():
            logger.info("Cache marker detected — reloading license providers from disk")
            cls.reload_providers()

        provider_class = cls._providers.get(provider_type)

        if not provider_class:
            logger.warning(f"Provider not found: {provider_type}")
            logger.debug(f"Available providers: {', '.join(cls._providers.keys())}")

        return provider_class

    @classmethod
    def list_providers(cls) -> List[Dict]:
        """
        List all available providers with metadata.

        Returns:
            List of dicts with provider information:
            [
                {
                    'key': 'keygen',
                    'name': 'Keygen.sh',
                    'description': '...',
                    'logo': '...',
                    'class': KeygenAdapter,
                },
                ...
            ]
        """
        if not cls._discovered:
            cls.discover_providers()
        elif cls._cache_is_stale():
            cls.reload_providers()

        # Fallback metadata for built-in providers (if not componentized)
        fallback_metadata = {
            'spwig_server': {
                'description': 'Built-in license management server. Fully managed by Spwig, no external setup required.',
                'logo': None,
            },
            'keygen': {
                'description': 'Popular license management platform with policy-based licensing.',
                'logo': None,
            },
            'licensespring': {
                'description': 'Comprehensive license management with floating licenses and usage tracking.',
                'logo': None,
            },
            'cryptlex': {
                'description': 'Secure license management with node-locked and floating licenses.',
                'logo': None,
            },
            'custom': {
                'description': 'Connect your own license server via REST API.',
                'logo': None,
            },
        }

        providers = []

        for key, provider_class in cls._providers.items():
            try:
                # Check if this is a component-based provider with manifest
                if hasattr(provider_class, '_manifest') and hasattr(provider_class, '_component_path'):
                    manifest = provider_class._manifest
                    component_path = provider_class._component_path

                    # Get description from manifest
                    description = manifest.get('description', '')

                    # Get logo path from manifest (handle dict and string formats)
                    logo_raw = manifest.get('logo')
                    if isinstance(logo_raw, dict):
                        logo_file = logo_raw.get('file', '')
                    else:
                        logo_file = logo_raw or ''
                    if logo_file:
                        # Build relative path to logo file
                        logo_path = component_path / logo_file
                        if logo_path.exists():
                            # Convert to path relative to components_data/integrations (STATICFILES_DIR)
                            # Path should be: license_server_providers/{provider}/current/logo.ext
                            from component_updates.integration_paths import INTEGRATIONS_DIR
                            logo = str(logo_path.relative_to(INTEGRATIONS_DIR))
                        else:
                            logo = None
                    else:
                        logo = None

                else:
                    # Fall back to hardcoded metadata for built-in providers
                    metadata = fallback_metadata.get(key, {})
                    description = metadata.get('description', '')
                    logo = metadata.get('logo')

                providers.append({
                    'key': key,
                    'name': provider_class.provider_name,
                    'description': description,
                    'logo': logo,
                    'class': provider_class,
                })
            except Exception as e:
                logger.error(f"Error listing provider {key}: {e}")
                continue

        # Sort: spwig_server first, then alphabetically
        providers.sort(key=lambda p: (0 if p['key'] == 'spwig_server' else 1, p['name']))

        return providers

    @classmethod
    def reload_providers(cls):
        """
        Force reload all providers.

        Useful when providers are updated or new ones are added.
        """
        logger.info("Reloading license providers...")

        cls._providers.clear()
        cls._discovered = False
        cls.discover_providers()

    @classmethod
    def is_provider_available(cls, provider_type: str) -> bool:
        """
        Check if a provider is available.

        Args:
            provider_type: Provider key to check

        Returns:
            bool: True if provider is registered
        """
        if not cls._discovered:
            cls.discover_providers()

        return provider_type in cls._providers

    @classmethod
    def get_provider_count(cls) -> int:
        """
        Get total number of registered providers.

        Returns:
            int: Count of registered providers
        """
        if not cls._discovered:
            cls.discover_providers()

        return len(cls._providers)
