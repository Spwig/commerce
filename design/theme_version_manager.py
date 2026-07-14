"""
Theme Version Management

Handles installation, activation, and rollback of theme versions using symlinks.
Provides zero-downtime updates by flipping symlinks atomically.
"""

import json
import logging
import shutil
from pathlib import Path
from typing import Any

from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

# Paths — themes live in the components_data volume
COMPONENTS_DATA = Path(settings.BASE_DIR) / "components_data"
THEMES_STATIC = COMPONENTS_DATA / "static" / "design" / "themes"
REGISTRY_FILE = COMPONENTS_DATA / "registries" / "themes.json"


class ThemeVersionManager:
    """Manages theme versions using symlink-based activation"""

    @staticmethod
    def get_registry() -> dict[str, Any]:
        """Load theme_registry.json"""
        if not REGISTRY_FILE.exists():
            return {"version": "1.0", "themes": {}}

        with open(REGISTRY_FILE) as f:
            return json.load(f)

    @staticmethod
    def save_registry(registry: dict[str, Any]):
        """Save theme_registry.json"""
        REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(REGISTRY_FILE, "w") as f:
            json.dump(registry, f, indent=2)

    @staticmethod
    def install_theme_version(theme_slug: str, version: str, package_path: Path) -> dict[str, Any]:
        """
        Install a new theme version from package.

        Args:
            theme_slug: Theme slug (e.g., 'default', 'modern-dark')
            version: Version string (e.g., '1.0.0', '2.0.0')
            package_path: Path to extracted package directory

        Returns:
            Dict with success status and details
        """
        try:
            # Create version directory
            version_dest = THEMES_STATIC / theme_slug / version

            version_dest.mkdir(parents=True, exist_ok=True)

            # Copy all theme files (theme/ directory contains css/, manifest.json, etc.)
            theme_src = package_path / "theme"
            if not theme_src.exists():
                # Some packages might have files at root
                theme_src = package_path

            # Copy entire theme structure
            for item in theme_src.rglob("*"):
                if item.is_file():
                    rel_path = item.relative_to(theme_src)
                    dest_file = version_dest / "theme" / rel_path
                    dest_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, dest_file)

            logger.info(f"Copied theme files for {theme_slug} {version}")

            # Update registry
            registry = ThemeVersionManager.get_registry()

            if theme_slug not in registry["themes"]:
                registry["themes"][theme_slug] = {
                    "current_version": version,
                    "available_versions": [version],
                    "description": f"{theme_slug.replace('-', ' ').replace('_', ' ').title()} theme",
                    "author": "Spwig",
                    "category": "theme",
                }
            else:
                if version not in registry["themes"][theme_slug]["available_versions"]:
                    registry["themes"][theme_slug]["available_versions"].append(version)

            ThemeVersionManager.save_registry(registry)

            return {
                "success": True,
                "message": f"Theme {theme_slug} {version} installed successfully",
                "theme": theme_slug,
                "version": version,
            }

        except Exception as e:
            logger.error(f"Failed to install {theme_slug} {version}: {e}")
            return {
                "success": False,
                "error": str(e),
                "theme": theme_slug,
                "version": version,
            }

    @staticmethod
    def activate_theme_version(
        theme_slug: str, version: str, *, update_active_theme: bool = True
    ) -> dict[str, Any]:
        """
        Activate a theme version by flipping the 'current' symlink.
        This is an ATOMIC operation - instant zero-downtime activation!

        Args:
            theme_slug: Theme slug
            version: Version to activate (e.g., '1.0.0')
            update_active_theme: If True, also set GlobalDesignSettings.active_theme.
                Set to False during bulk installation or theme extraction to avoid
                the last installed theme overwriting the default theme selection.

        Returns:
            Dict with success status
        """
        try:
            theme_dir = THEMES_STATIC / theme_slug
            version_dir = theme_dir / version

            if not version_dir.exists():
                return {
                    "success": False,
                    "error": f"Version {version} does not exist for {theme_slug}",
                }

            logger.info(
                f"Activating {theme_slug} {version} (update_active_theme={update_active_theme})"
            )

            # ── Flip symlink atomically ──
            current_link = theme_dir / "current"
            temp_link = theme_dir / "current.tmp"

            if temp_link.exists() or temp_link.is_symlink():
                temp_link.unlink()
            temp_link.symlink_to(version)
            temp_link.replace(current_link)
            logger.debug(f"Symlink flipped: {current_link} -> {version}")

            # ── Update registry ──
            registry = ThemeVersionManager.get_registry()
            if theme_slug in registry["themes"]:
                registry["themes"][theme_slug]["current_version"] = version
                ThemeVersionManager.save_registry(registry)

            # ── Update database when this is a user-initiated activation ──
            # Skipped during bulk installation so the default theme isn't overwritten.
            if update_active_theme:
                try:
                    from .models import GlobalDesignSettings
                    from .theme_models import Theme

                    theme_obj = Theme.objects.filter(slug=theme_slug).first()
                    if theme_obj:
                        # CRITICAL: sync theme_obj.version to the activation target BEFORE
                        # calling extract_theme(). extract_theme() internally calls
                        # install_theme_version() + activate_theme_version() using
                        # self.version, so a stale DB version would re-flip the symlink
                        # back to the old target.
                        if theme_obj.version != version:
                            logger.info(
                                f"Syncing Theme DB row version {theme_obj.version} -> {version} "
                                f"before compiled_css regeneration"
                            )
                            theme_obj.version = version
                            theme_obj.save(update_fields=["version"])

                        settings = GlobalDesignSettings.get_settings()
                        settings.active_theme = theme_obj
                        settings.save(update_fields=["active_theme"])
                        logger.info(f"Set GlobalDesignSettings.active_theme = {theme_slug}")

                        # Regenerate compiled_css so the canvas picks up current platform CSS.
                        # extract_theme uses theme_obj.version (now synced above).
                        if theme_obj.package_file:
                            theme_obj.extract_theme()
                            logger.info(f"Regenerated compiled_css for {theme_slug} {version}")
                    else:
                        logger.warning(
                            f"Theme '{theme_slug}' not found in database, skipping DB update"
                        )
                except Exception as db_err:
                    logger.error(f"Failed to update active_theme in database: {db_err}")

            # ── Post-flip verification ──
            # extract_theme() above may call activate_theme_version() recursively,
            # so re-verify the symlink points where we expect before returning success.
            try:
                final_target = current_link.resolve().name
            except OSError as e:
                return {
                    "success": False,
                    "error": f"Symlink verification failed: {e}",
                    "theme": theme_slug,
                    "version": version,
                }

            if final_target != version:
                logger.warning(
                    f"Symlink drift detected: {theme_slug}/current points to {final_target}, "
                    f"expected {version}. Re-flipping."
                )
                temp_link = theme_dir / "current.tmp"
                if temp_link.exists() or temp_link.is_symlink():
                    temp_link.unlink()
                temp_link.symlink_to(version)
                temp_link.replace(current_link)
                final_target = current_link.resolve().name
                if final_target != version:
                    return {
                        "success": False,
                        "error": f"Could not establish symlink to {version} (resolves to {final_target})",
                        "theme": theme_slug,
                        "version": version,
                    }

            # ── Invalidate theme cache ──
            cache.delete("active_theme")
            cache.delete_pattern("theme_*")

            logger.info(f"Activated {theme_slug} {version}")

            return {
                "success": True,
                "message": f"✅ {theme_slug} {version} activated! Changes live immediately.",
                "theme": theme_slug,
                "version": version,
                "requires_restart": False,  # No restart needed!
            }

        except Exception as e:
            logger.error(f"Failed to activate {theme_slug} {version}: {e}")
            return {
                "success": False,
                "error": str(e),
                "theme": theme_slug,
                "version": version,
            }

    @staticmethod
    def get_theme_versions(theme_slug: str) -> list[str]:
        """Get all available versions for a theme"""
        theme_dir = THEMES_STATIC / theme_slug

        if not theme_dir.exists():
            return []

        versions = []
        for item in theme_dir.iterdir():
            if item.is_dir() and item.name not in ["current", "current.tmp"]:
                # Check if it looks like a version (digits and dots)
                if any(c.isdigit() for c in item.name):
                    versions.append(item.name)

        return sorted(versions, reverse=True)  # Newest first

    @staticmethod
    def get_current_version(theme_slug: str) -> str | None:
        """Get currently active version"""
        current_link = THEMES_STATIC / theme_slug / "current"

        if current_link.exists() and current_link.is_symlink():
            return current_link.resolve().name

        return None

    @staticmethod
    def rollback_theme(theme_slug: str, to_version: str | None = None) -> dict[str, Any]:
        """
        Rollback theme to previous version or specified version.

        Args:
            theme_slug: Theme slug
            to_version: Version to rollback to (if None, uses previous version)

        Returns:
            Dict with success status
        """
        try:
            current = ThemeVersionManager.get_current_version(theme_slug)
            if not current:
                return {"success": False, "error": f"No current version for {theme_slug}"}

            if to_version is None:
                # Find previous version
                versions = ThemeVersionManager.get_theme_versions(theme_slug)
                if len(versions) < 2:
                    return {"success": False, "error": "No previous version available for rollback"}

                # Get version before current
                try:
                    current_index = versions.index(current)
                    to_version = versions[current_index + 1]
                except (ValueError, IndexError):
                    to_version = versions[1]  # Fallback to second newest

            # Activate the target version
            return ThemeVersionManager.activate_theme_version(theme_slug, to_version)

        except Exception as e:
            logger.error(f"Failed to rollback {theme_slug}: {e}")
            return {
                "success": False,
                "error": str(e),
                "theme": theme_slug,
            }

    @staticmethod
    def uninstall_theme(theme_slug: str, version: str | None = None) -> dict[str, Any]:
        """
        Uninstall a theme version or entire theme.
        Removes filesystem files, registry entries, header/footer presets,
        and database records (Theme model + cascaded DesignTokens, ThemeAssets,
        ThemeInstallations).

        Cannot uninstall the currently active theme.

        Args:
            theme_slug: Theme slug
            version: Specific version to remove (if None, removes entire theme)

        Returns:
            Dict with success status and cleanup counts
        """
        try:
            # Guard: cannot uninstall the active theme
            active = ThemeVersionManager.get_active_theme()
            if active and active["slug"] == theme_slug:
                return {
                    "success": False,
                    "error": "Cannot uninstall the active theme. Switch to a different theme first.",
                    "theme": theme_slug,
                }

            # Remove presets installed by this theme
            try:
                from design.services.theme_preset_installer import ThemePresetInstaller

                preset_result = ThemePresetInstaller.uninstall_presets(theme_slug)
                if preset_result["headers_deleted"] or preset_result["footers_deleted"]:
                    logger.info(
                        f"Removed presets for {theme_slug}: "
                        f"{preset_result['headers_deleted']} headers, "
                        f"{preset_result['footers_deleted']} footers"
                    )
            except Exception as e:
                logger.warning(f"Failed to remove presets for {theme_slug}: {e}")

            if version:
                # Remove specific version
                version_dir = THEMES_STATIC / theme_slug / version

                if version_dir.exists():
                    shutil.rmtree(version_dir)

                # Update registry
                registry = ThemeVersionManager.get_registry()
                if theme_slug in registry["themes"]:
                    versions = registry["themes"][theme_slug]["available_versions"]
                    if version in versions:
                        versions.remove(version)
                    ThemeVersionManager.save_registry(registry)

                message = f"Version {version} removed from {theme_slug}"

            else:
                # Remove entire theme
                theme_dir = THEMES_STATIC / theme_slug

                if theme_dir.exists():
                    shutil.rmtree(theme_dir)

                # Update registry
                registry = ThemeVersionManager.get_registry()
                if theme_slug in registry["themes"]:
                    del registry["themes"][theme_slug]
                    ThemeVersionManager.save_registry(registry)

                message = f"Theme {theme_slug} completely removed"

            # Clean up database records
            # Deleting Theme triggers CASCADE on: DesignToken, ThemeAsset,
            # ThemeInstallation. ThemeBranding.theme is SET_NULL (preserved).
            db_cleanup = {"tokens_deleted": 0, "themes_deleted": 0}
            try:
                from .models import DesignToken
                from .theme_models import Theme

                themes_qs = Theme.objects.filter(slug=theme_slug)
                if version:
                    themes_qs = themes_qs.filter(version=version)

                # Log counts before deletion
                token_count = DesignToken.objects.filter(
                    source="theme", theme__in=themes_qs
                ).count()
                theme_count = themes_qs.count()

                if theme_count > 0:
                    themes_qs.delete()  # CASCADE handles tokens, assets, installations
                    db_cleanup["tokens_deleted"] = token_count
                    db_cleanup["themes_deleted"] = theme_count
                    logger.info(
                        f"DB cleanup for {theme_slug}: "
                        f"{theme_count} theme(s), {token_count} token(s) deleted"
                    )
            except Exception as e:
                logger.warning(f"DB cleanup for {theme_slug} had issues: {e}")

            # Invalidate cache
            cache.delete("active_theme")
            cache.delete_pattern("theme_*")

            logger.info(message)

            return {
                "success": True,
                "message": f"✅ {message}",
                "theme": theme_slug,
                "db_cleanup": db_cleanup,
            }

        except Exception as e:
            logger.error(f"Failed to uninstall {theme_slug}: {e}")
            return {
                "success": False,
                "error": str(e),
                "theme": theme_slug,
            }

    @staticmethod
    def get_active_theme() -> dict[str, Any] | None:
        """
        Get the currently active theme from GlobalDesignSettings.

        Returns:
            Dict with theme info {'slug': 'theme-slug', 'name': 'Theme Name', 'version': '1.0.0'}
            or None if no theme is active
        """
        try:
            # Import here to avoid circular dependency
            from .models import GlobalDesignSettings

            settings = GlobalDesignSettings.get_settings()
            if settings.active_theme:
                theme = settings.active_theme
                current_version = ThemeVersionManager.get_current_version(theme.slug)

                return {
                    "slug": theme.slug,
                    "name": theme.name,
                    "version": current_version or theme.version,
                    "id": theme.id,
                }

            return None

        except Exception as e:
            logger.error(f"Failed to get active theme: {e}")
            return None

    @staticmethod
    def health_check(theme_slug: str, version: str) -> dict[str, Any]:
        """
        Perform health check on a theme version.

        Args:
            theme_slug: Theme slug
            version: Version to check

        Returns:
            Dict with health status
        """
        try:
            version_dir = THEMES_STATIC / theme_slug / version

            if not version_dir.exists():
                return {
                    "status": "unhealthy",
                    "message": f"Version directory does not exist: {version_dir}",
                }

            # Check if current symlink is valid
            current_link = THEMES_STATIC / theme_slug / "current"
            if current_link.exists() and current_link.is_symlink():
                current_version = current_link.resolve().name
                if current_version != version:
                    return {
                        "status": "degraded",
                        "message": f"Symlink points to {current_version}, expected {version}",
                    }
            else:
                return {"status": "degraded", "message": "Current symlink is missing or invalid"}

            # Check for essential theme files
            manifest_path = version_dir / "theme" / "manifest.json"
            if not manifest_path.exists():
                return {"status": "unhealthy", "message": "Theme manifest.json is missing"}

            # Check for CSS directory
            css_dir = version_dir / "theme" / "css"
            if not css_dir.exists():
                return {"status": "unhealthy", "message": "Theme CSS directory is missing"}

            return {"status": "healthy", "message": f"Theme {theme_slug} {version} is healthy"}

        except Exception as e:
            logger.error(f"Health check failed for {theme_slug} {version}: {e}")
            return {"status": "unhealthy", "message": str(e)}
