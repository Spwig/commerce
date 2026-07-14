"""
Provider Service
Handles provider discovery, installation, and management
"""

import logging
from pathlib import Path

from component_updates.integration_paths import INTEGRATIONS_DIR
from component_updates.models import ComponentRegistry
from component_updates.services import UpdateManager
from shipping.providers.loader import load_provider_manifest

logger = logging.getLogger(__name__)


class ProviderService:
    """
    Service for managing shipping provider components.

    Handles:
    - Fetching available providers from update server
    - Installing provider packages
    - Checking installation status
    - Loading provider metadata
    """

    def __init__(self):
        self.update_manager = UpdateManager()

    @staticmethod
    def get_component_path(component_slug: str) -> Path:
        """
        Get the component directory path for a provider.

        Args:
            component_slug: Provider component slug

        Returns:
            Path to component directory (current version)
        """
        return INTEGRATIONS_DIR / "shipping_provider" / component_slug / "current"

    def fetch_available_providers(self) -> list[dict]:
        """
        Fetch all available shipping providers from update server.

        Returns:
            List of provider dictionaries with metadata
        """
        try:
            # Get all shipping provider components from update server
            available = self.update_manager.list_available_components(
                component_type="shipping_provider"
            )

            # Enhance with local installation status
            providers = []
            for component_data in available:
                slug = component_data.get("slug")

                # Check if already installed locally
                is_installed = ComponentRegistry.objects.filter(
                    slug=slug, component_type="shipping_provider"
                ).exists()

                component_data["is_installed"] = is_installed
                providers.append(component_data)

            return providers

        except Exception as e:
            logger.error(f"Error fetching providers from update server: {e}")
            return []

    def get_installed_providers(self) -> list[dict]:
        """
        Get all locally installed shipping providers.

        Returns:
            List of installed provider dictionaries with manifests
        """
        providers = []

        components = ComponentRegistry.objects.filter(component_type="shipping_provider").order_by(
            "name"
        )

        for component in components:
            try:
                component_path = self.get_component_path(component.slug)

                if component_path.exists():
                    manifest = load_provider_manifest(component_path)
                else:
                    logger.warning(
                        f"Component directory not found for {component.name}: {component_path}"
                    )
                    manifest = None

                providers.append(
                    {
                        "component": component,
                        "manifest": manifest or {},
                        "capabilities": manifest.get("capabilities", {}) if manifest else {},
                        "setup": manifest.get("setup", {}) if manifest else {},
                    }
                )
            except Exception as e:
                logger.warning(f"Could not load manifest for {component.name}: {e}")
                providers.append(
                    {
                        "component": component,
                        "manifest": {},
                        "capabilities": {},
                        "setup": {},
                    }
                )

        return providers

    def is_provider_installed(self, slug: str) -> bool:
        """
        Check if a provider is installed locally.

        Args:
            slug: Component slug

        Returns:
            True if installed, False otherwise
        """
        return ComponentRegistry.objects.filter(
            slug=slug, component_type="shipping_provider"
        ).exists()

    def get_provider_metadata(self, component_id: str) -> dict | None:
        """
        Get provider metadata including manifest.

        Args:
            component_id: Component ID or slug

        Returns:
            Dict with component and manifest data, or None if not found
        """
        try:
            # Try by ID first
            try:
                component = ComponentRegistry.objects.get(
                    id=component_id, component_type="shipping_provider"
                )
            except (ComponentRegistry.DoesNotExist, ValueError):
                # Try by slug
                component = ComponentRegistry.objects.get(
                    slug=component_id, component_type="shipping_provider"
                )

            # Load manifest from component path
            component_path = self.get_component_path(component.slug)
            manifest = load_provider_manifest(component_path) if component_path.exists() else None

            return {
                "component": component,
                "manifest": manifest or {},
                "capabilities": manifest.get("capabilities", {}) if manifest else {},
                "setup": manifest.get("setup", {}) if manifest else {},
                "credential_schema": manifest.get("credential_schema", {}) if manifest else {},
            }

        except ComponentRegistry.DoesNotExist:
            return None
        except Exception as e:
            logger.error(f"Error loading provider metadata for {component_id}: {e}")
            return None
