"""
Shared component installation functions.

Extracted from UpdateManager._install_package() so both marketplace installs
and bundled component installs use the same code path.
"""

import json
import logging
import shutil
import tempfile
import zipfile
from pathlib import Path

from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)


class InstallError(Exception):
    """Raised when a component installation fails."""
    pass


def install_theme_from_package(extract_dir: Path, manifest: dict, *, create_db_record: bool = True) -> dict:
    """
    Install a theme package from an extracted directory.

    Uses ThemeVersionManager to install files + optionally creates the Theme
    database record with compiled_css populated.

    Args:
        extract_dir: Path to extracted package (contains theme/ subdirectory)
        manifest: Parsed manifest.json dict
        create_db_record: If True, create/update Theme model and run extract_theme()

    Returns:
        Dict with 'success', 'theme_slug', 'version' keys
    """
    from design.theme_version_manager import ThemeVersionManager

    theme_slug = manifest['slug']
    version = manifest['version']

    logger.info(f"Installing theme: {theme_slug} v{version}")

    try:
        # Step 1: Install theme files via ThemeVersionManager
        result = ThemeVersionManager.install_theme_version(
            theme_slug=theme_slug,
            version=version,
            package_path=extract_dir
        )

        if not result['success']:
            raise InstallError(f"ThemeVersionManager failed: {result.get('error')}")

        # Step 2: Activate this version (set current symlink only, don't change
        # active_theme during bulk install — _ensure_theme_db_record handles it)
        activate_result = ThemeVersionManager.activate_theme_version(
            theme_slug=theme_slug,
            version=version,
            update_active_theme=False,
        )

        if not activate_result['success']:
            logger.warning(f"Theme installed but activation failed: {activate_result.get('error')}")

        # Step 3: Create/update Theme database record
        if create_db_record:
            _ensure_theme_db_record(extract_dir, manifest)

        logger.info(f"Theme {theme_slug} v{version} installed successfully")
        return {'success': True, 'theme_slug': theme_slug, 'version': version}

    except Exception as e:
        logger.error(f"Failed to install theme {theme_slug}: {e}")
        return {'success': False, 'theme_slug': theme_slug, 'version': version, 'error': str(e)}


def _ensure_theme_db_record(extract_dir: Path, manifest: dict):
    """Create or update Theme DB record and populate compiled_css via extract_theme()."""
    from design.theme_models import Theme
    from django.core.files import File

    slug = manifest['slug']
    version = manifest['version']

    # Build a ZIP package from the extracted directory (Theme model stores a package_file)
    with tempfile.TemporaryDirectory() as tmp:
        zip_path = Path(tmp) / f"{slug}.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            # Walk the extract_dir and add all files
            for file_path in extract_dir.rglob('*'):
                if file_path.is_file():
                    arcname = str(file_path.relative_to(extract_dir))
                    zf.write(file_path, arcname)

        import hashlib
        with open(zip_path, 'rb') as f:
            checksum = hashlib.sha256(f.read()).hexdigest()

        # Check if theme already exists
        existing = Theme.objects.filter(slug=slug).first()
        if existing:
            # Update version if needed but don't recreate
            if existing.version != version:
                existing.version = version
                existing.save(update_fields=['version'])
            # Re-extract to update compiled_css
            existing.extract_theme()

            # If this is the default theme and no active theme is set yet,
            # assign it now.  Handles themes pre-created by another path
            # (e.g. create_default_themes) before install_bundled_components.
            is_default = manifest.get('is_default', slug == 'starter')
            if is_default:
                try:
                    from design.models import GlobalDesignSettings
                    settings_obj = GlobalDesignSettings.get_settings()
                    if not settings_obj.active_theme_id:
                        settings_obj.active_theme = existing
                        settings_obj.save(update_fields=['active_theme'])
                        logger.info(f"Set existing default theme '{slug}' as active theme (was unset)")
                except Exception as e:
                    logger.warning(f"Failed to set default active theme: {e}")
            return

        # Create new Theme record
        is_default = manifest.get('is_default', slug == 'starter')

        # Load tokens from manifest or extract_dir
        tokens = manifest.get('tokens', {})
        if not tokens:
            tokens_path = extract_dir / 'theme' / 'tokens.json'
            if tokens_path.exists():
                with open(tokens_path) as f:
                    tokens = json.load(f)

        with open(zip_path, 'rb') as f:
            theme = Theme.objects.create(
                name=manifest.get('name', slug.replace('-', ' ').title()),
                slug=slug,
                description=manifest.get('description', ''),
                version=version,
                engine_min_version=manifest.get('engine', {}).get('min', '1.0.0'),
                author=manifest.get('author', 'Spwig'),
                author_email=manifest.get('author_email', 'themes@spwig.com'),
                manifest=manifest,
                package_file=File(f, name=f"{slug}.zip"),
                package_checksum=checksum,
                is_active=True,
                is_default=is_default,
                installed_at=timezone.now()
            )

        # extract_theme() populates compiled_css from the package
        theme.extract_theme()

        # Set default theme as the active theme in GlobalDesignSettings
        if is_default:
            try:
                from design.models import GlobalDesignSettings
                settings_obj = GlobalDesignSettings.get_settings()
                settings_obj.active_theme = theme
                settings_obj.save(update_fields=['active_theme'])
                logger.info(f"Set default theme '{slug}' as active theme")
            except Exception as e:
                logger.warning(f"Failed to set default active theme: {e}")


def install_utility_from_package(extract_dir: Path, manifest: dict) -> dict:
    """
    Install a utility package from an extracted directory.

    Uses UtilityVersionManager to install files and activate the version.

    Args:
        extract_dir: Path to extracted package (contains static/ and optionally templates/)
        manifest: Parsed manifest.json dict

    Returns:
        Dict with 'success', 'utility_slug', 'version' keys
    """
    from .utility_version_manager import UtilityVersionManager

    utility_slug = manifest['slug'].replace('-', '_')
    version = manifest['version']
    # Ensure version has 'v' prefix for filesystem
    fs_version = version if version.startswith('v') else f'v{version}'

    logger.info(f"Installing utility: {utility_slug} v{version}")

    try:
        result = UtilityVersionManager.install_utility_version(
            utility_slug=utility_slug,
            version=fs_version,
            package_path=extract_dir
        )

        if not result['success']:
            raise InstallError(f"UtilityVersionManager failed: {result.get('error')}")

        # Activate the version
        activate_result = UtilityVersionManager.activate_utility_version(
            utility_slug=utility_slug,
            version=fs_version
        )

        if not activate_result['success']:
            logger.warning(f"Utility installed but activation failed: {activate_result.get('error')}")

        logger.info(f"Utility {utility_slug} v{version} installed successfully")
        return {'success': True, 'utility_slug': utility_slug, 'version': version}

    except Exception as e:
        logger.error(f"Failed to install utility {utility_slug}: {e}")
        return {'success': False, 'utility_slug': utility_slug, 'version': version, 'error': str(e)}


def ensure_component_registry(component_type: str, slug: str, manifest: dict, install_method: str = 'bundled') -> None:
    """
    Create or update ComponentRegistry and ComponentVersion entries.

    Args:
        component_type: One of 'theme', 'utility', etc.
        slug: Component slug
        manifest: Parsed manifest dict
        install_method: How the component was installed ('bundled', 'update_server', etc.)
    """
    from component_updates.models import ComponentRegistry, ComponentVersion

    version = manifest.get('version', '1.0.0')

    registry_entry, created = ComponentRegistry.objects.get_or_create(
        component_type=component_type,
        slug=slug,
        defaults={
            'name': manifest.get('name', slug.replace('-', ' ').replace('_', ' ').title()),
            'current_version': version,
            'latest_version': version,
            'update_available': False,
            'author': manifest.get('author', 'Spwig'),
            'author_details': {
                'name': manifest.get('author', 'Spwig'),
                'email': manifest.get('author_email', 'themes@spwig.com'),
                'verified': True,
            },
            'description': manifest.get('description', ''),
            'locked': False,
        }
    )

    if not created and registry_entry.current_version != version:
        registry_entry.current_version = version
        registry_entry.latest_version = version
        registry_entry.save(update_fields=['current_version', 'latest_version'])

    # Create ComponentVersion entry
    ComponentVersion.objects.get_or_create(
        component=registry_entry,
        version=version,
        defaults={
            'is_active': True,
            'install_method': install_method,
            'rollback_available': True,
            'health_status': 'healthy',
        }
    )
