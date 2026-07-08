"""
Utility Version Management

Handles installation, activation, and rollback of utility versions using symlinks.
Provides zero-downtime updates by flipping symlinks atomically.
"""

import json
import logging
import shutil
from pathlib import Path
from typing import Dict, Any, Optional, List
from django.conf import settings

logger = logging.getLogger(__name__)

# Paths — utilities live in the components_data volume
COMPONENTS_DATA = Path(settings.BASE_DIR) / 'components_data'
UTILITIES_STATIC = COMPONENTS_DATA / 'static' / 'utilities'
UTILITIES_TEMPLATES = COMPONENTS_DATA / 'templates' / 'utilities'
REGISTRY_FILE = COMPONENTS_DATA / 'registries' / 'utilities.json'


class UtilityVersionManager:
    """Manages utility versions using symlink-based activation"""

    @staticmethod
    def get_registry() -> Dict[str, Any]:
        """Load registry.json"""
        if not REGISTRY_FILE.exists():
            return {"version": "1.0", "utilities": {}}

        with open(REGISTRY_FILE, 'r') as f:
            return json.load(f)

    @staticmethod
    def save_registry(registry: Dict[str, Any]):
        """Save registry.json"""
        REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(REGISTRY_FILE, 'w') as f:
            json.dump(registry, f, indent=2)

    @staticmethod
    def install_utility_version(
        utility_slug: str,
        version: str,
        package_path: Path
    ) -> Dict[str, Any]:
        """
        Install a new utility version from package.

        Args:
            utility_slug: Utility name (e.g., 'background_editor')
            version: Version string (e.g., 'v1.0.0', 'v2.0.0')
            package_path: Path to extracted package directory

        Returns:
            Dict with success status and details
        """
        # Normalize slug: packages use hyphens, filesystem uses underscores
        utility_slug = utility_slug.replace('-', '_')

        try:
            static_dest = UTILITIES_STATIC / utility_slug / version
            templates_dest = UTILITIES_TEMPLATES / utility_slug / version

            # Create version directories
            static_dest.mkdir(parents=True, exist_ok=True)
            templates_dest.mkdir(parents=True, exist_ok=True)

            # Copy static files (CSS/JS/logo)
            static_src = package_path / 'static'
            if static_src.exists():
                for file in static_src.iterdir():
                    if file.is_file():
                        shutil.copy2(file, static_dest)
                logger.info(f"Copied static files for {utility_slug} {version}")

            # Copy manifest.json from package root to version dir (defensive -
            # ensures manifest is available for logo resolution even if not in static/)
            manifest_src = package_path / 'manifest.json'
            if manifest_src.exists() and not (static_dest / 'manifest.json').exists():
                shutil.copy2(manifest_src, static_dest / 'manifest.json')
                logger.info(f"Copied manifest.json for {utility_slug} {version}")

            # Copy template files
            templates_src = package_path / 'templates'
            if templates_src.exists():
                for file in templates_src.iterdir():
                    if file.is_file():
                        shutil.copy2(file, templates_dest)
                logger.info(f"Copied template files for {utility_slug} {version}")

            # Update registry
            registry = UtilityVersionManager.get_registry()

            if utility_slug not in registry['utilities']:
                registry['utilities'][utility_slug] = {
                    'current_version': version,
                    'available_versions': [version],
                    'description': f'{utility_slug.replace("_", " ").title()} utility',
                    'author': 'Spwig',
                    'category': 'utility'
                }
            else:
                if version not in registry['utilities'][utility_slug]['available_versions']:
                    registry['utilities'][utility_slug]['available_versions'].append(version)

            UtilityVersionManager.save_registry(registry)

            return {
                'success': True,
                'message': f'Utility {utility_slug} {version} installed successfully',
                'utility': utility_slug,
                'version': version,
            }

        except Exception as e:
            logger.error(f"Failed to install {utility_slug} {version}: {e}")
            return {
                'success': False,
                'error': str(e),
                'utility': utility_slug,
                'version': version,
            }

    @staticmethod
    def activate_utility_version(utility_slug: str, version: str) -> Dict[str, Any]:
        """
        Activate a utility version by flipping the 'current' symlink.
        This is an ATOMIC operation - instant zero-downtime activation!

        Args:
            utility_slug: Utility name
            version: Version to activate (e.g., 'v1.0.0')

        Returns:
            Dict with success status
        """
        # Normalize slug: packages use hyphens, filesystem uses underscores
        utility_slug = utility_slug.replace('-', '_')

        try:
            static_dir = UTILITIES_STATIC / utility_slug
            templates_dir = UTILITIES_TEMPLATES / utility_slug

            version_dir = static_dir / version
            if not version_dir.exists():
                return {
                    'success': False,
                    'error': f'Version {version} does not exist for {utility_slug}'
                }

            # Flip symlink atomically
            current_link = static_dir / 'current'
            temp_link = static_dir / 'current.tmp'

            # Create temporary symlink
            if temp_link.exists():
                temp_link.unlink()
            temp_link.symlink_to(version)

            # Atomic rename (replaces old symlink)
            temp_link.replace(current_link)

            # Do the same for templates if they exist
            templates_version_dir = templates_dir / version
            if templates_version_dir.exists():
                templates_current = templates_dir / 'current'
                templates_temp = templates_dir / 'current.tmp'

                if templates_temp.exists():
                    templates_temp.unlink()
                templates_temp.symlink_to(version)
                templates_temp.replace(templates_current)

            # Update registry
            registry = UtilityVersionManager.get_registry()
            if utility_slug in registry['utilities']:
                registry['utilities'][utility_slug]['current_version'] = version
                UtilityVersionManager.save_registry(registry)

            # Invalidate cache
            from .utility_discovery import invalidate_utility_cache
            invalidate_utility_cache()

            logger.info(f"Activated {utility_slug} {version}")

            return {
                'success': True,
                'message': f'{utility_slug} {version} activated! Changes live immediately.',
                'utility': utility_slug,
                'version': version,
                'requires_restart': False,  # No restart needed!
            }

        except Exception as e:
            logger.error(f"Failed to activate {utility_slug} {version}: {e}")
            return {
                'success': False,
                'error': str(e),
                'utility': utility_slug,
                'version': version,
            }

    @staticmethod
    def get_utility_versions(utility_slug: str) -> List[str]:
        """Get all available versions for a utility"""
        utility_slug = utility_slug.replace('-', '_')
        static_dir = UTILITIES_STATIC / utility_slug

        if not static_dir.exists():
            return []

        versions = []
        for item in static_dir.iterdir():
            if item.is_dir() and item.name.startswith('v'):
                versions.append(item.name)

        return sorted(versions, reverse=True)  # Newest first

    @staticmethod
    def get_current_version(utility_slug: str) -> Optional[str]:
        """Get currently active version"""
        utility_slug = utility_slug.replace('-', '_')
        current_link = UTILITIES_STATIC / utility_slug / 'current'

        if not current_link.exists() or not current_link.is_symlink():
            return None

        return current_link.resolve().name

    @staticmethod
    def rollback_utility(utility_slug: str, to_version: Optional[str] = None) -> Dict[str, Any]:
        """
        Rollback utility to previous version or specified version.

        Args:
            utility_slug: Utility name
            to_version: Version to rollback to (if None, uses previous version)

        Returns:
            Dict with success status
        """
        try:
            current = UtilityVersionManager.get_current_version(utility_slug)
            if not current:
                return {
                    'success': False,
                    'error': f'No current version for {utility_slug}'
                }

            if to_version is None:
                # Find previous version
                versions = UtilityVersionManager.get_utility_versions(utility_slug)
                if len(versions) < 2:
                    return {
                        'success': False,
                        'error': 'No previous version available for rollback'
                    }

                # Get version before current
                try:
                    current_index = versions.index(current)
                    to_version = versions[current_index + 1]
                except (ValueError, IndexError):
                    to_version = versions[1]  # Fallback to second newest

            # Activate the target version
            return UtilityVersionManager.activate_utility_version(utility_slug, to_version)

        except Exception as e:
            logger.error(f"Failed to rollback {utility_slug}: {e}")
            return {
                'success': False,
                'error': str(e),
                'utility': utility_slug,
            }

    @staticmethod
    def uninstall_utility(utility_slug: str, version: Optional[str] = None) -> Dict[str, Any]:
        """
        Uninstall a utility version or entire utility.

        Args:
            utility_slug: Utility name
            version: Specific version to remove (if None, removes entire utility)

        Returns:
            Dict with success status
        """
        # Normalize slug: packages use hyphens, filesystem uses underscores
        utility_slug = utility_slug.replace('-', '_')

        try:
            if version:
                # Remove specific version
                static_dir = UTILITIES_STATIC / utility_slug / version
                templates_dir = UTILITIES_TEMPLATES / utility_slug / version

                if static_dir.exists():
                    shutil.rmtree(static_dir)
                if templates_dir.exists():
                    shutil.rmtree(templates_dir)

                # Update registry
                registry = UtilityVersionManager.get_registry()
                if utility_slug in registry['utilities']:
                    versions = registry['utilities'][utility_slug]['available_versions']
                    if version in versions:
                        versions.remove(version)
                    UtilityVersionManager.save_registry(registry)

                message = f'Version {version} removed from {utility_slug}'

            else:
                # Remove entire utility
                static_dir = UTILITIES_STATIC / utility_slug
                templates_dir = UTILITIES_TEMPLATES / utility_slug

                if static_dir.exists():
                    shutil.rmtree(static_dir)
                if templates_dir.exists():
                    shutil.rmtree(templates_dir)

                # Update registry
                registry = UtilityVersionManager.get_registry()
                if utility_slug in registry['utilities']:
                    del registry['utilities'][utility_slug]
                    UtilityVersionManager.save_registry(registry)

                message = f'Utility {utility_slug} completely removed'

            # Invalidate cache
            from .utility_discovery import invalidate_utility_cache
            invalidate_utility_cache()

            logger.info(message)

            return {
                'success': True,
                'message': f'{message}',
                'utility': utility_slug,
            }

        except Exception as e:
            logger.error(f"Failed to uninstall {utility_slug}: {e}")
            return {
                'success': False,
                'error': str(e),
                'utility': utility_slug,
            }
