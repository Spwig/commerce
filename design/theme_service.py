"""
Theme Service - Handles theme operations including installation, migration, and CSS generation
"""

import json
import zipfile
import shutil
from pathlib import Path
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class ThemeService:
    """Service class for theme operations"""

    def __init__(self):
        self.themes_root = Path(settings.STATIC_ROOT) / 'themes'
        self.themes_root.mkdir(exist_ok=True, parents=True)

    def extract_bundled_components(self, theme, package_file, user=None):
        """
        Extract and install bundled components from theme package.

        Args:
            theme: Theme instance
            package_file: Path to theme ZIP file
            user: User installing the theme

        Returns:
            Tuple of (component_count, success_list, error_list)
        """
        from .models import ComponentStore
        from .component_schema_validator import ComponentSchemaValidator
        from component_updates.models import ComponentRegistry
        import tempfile
        import hashlib

        manifest = theme.manifest
        bundled_components = manifest.get('bundled_components', [])

        if not bundled_components:
            logger.info(f"No bundled components in theme {theme.name}")
            return 0, [], []

        success_list = []
        error_list = []
        validator = ComponentSchemaValidator()

        logger.info(f"Extracting {len(bundled_components)} bundled components from {theme.name}")

        try:
            with zipfile.ZipFile(package_file, 'r') as zip_file:
                for component_ref in bundled_components:
                    component_path = component_ref.get('path', '')
                    component_name = component_ref.get('name', '')
                    component_type = component_ref.get('type', 'section')

                    if not component_path:
                        error_list.append(f"Missing path for component: {component_name}")
                        continue

                    try:
                        # Create temporary directory for component extraction
                        with tempfile.TemporaryDirectory() as temp_dir:
                            temp_component_dir = Path(temp_dir) / 'component'
                            temp_component_dir.mkdir()

                            # Extract component files from ZIP
                            # Components in new format are at root: components/{type}/{name}/
                            component_prefix = f"{component_path}/"
                            component_files_found = False

                            for file_name in zip_file.namelist():
                                if file_name.startswith(component_prefix) and not file_name.endswith('/'):
                                    # Extract relative path
                                    rel_path = file_name[len(component_prefix):]
                                    target_path = temp_component_dir / rel_path
                                    target_path.parent.mkdir(parents=True, exist_ok=True)

                                    with zip_file.open(file_name) as source:
                                        with open(target_path, 'wb') as target:
                                            shutil.copyfileobj(source, target)

                                    component_files_found = True

                            if not component_files_found:
                                error_list.append(f"No files found for component: {component_name} at {component_path}")
                                continue

                            # Validate component structure
                            is_valid, validation_errors = validator.validate_component(temp_component_dir)

                            if not is_valid:
                                error_msg = f"Component validation failed for {component_name}: {'; '.join(validation_errors)}"
                                logger.error(error_msg)
                                error_list.append(error_msg)
                                continue

                            # Load component manifest
                            manifest_path = temp_component_dir / 'manifest.json'
                            with open(manifest_path, 'r') as f:
                                component_manifest = json.load(f)

                            # Create component package ZIP
                            component_zip_name = f"{component_manifest['name']}-{component_manifest['version']}.zip"
                            component_zip_path = Path(temp_dir) / component_zip_name

                            with zipfile.ZipFile(component_zip_path, 'w', zipfile.ZIP_DEFLATED) as comp_zip:
                                for file_path in temp_component_dir.rglob('*'):
                                    if file_path.is_file():
                                        arc_path = file_path.relative_to(temp_component_dir)
                                        comp_zip.write(file_path, arc_path)

                            # Calculate checksum
                            sha256_hash = hashlib.sha256()
                            with open(component_zip_path, 'rb') as f:
                                for chunk in iter(lambda: f.read(4096), b''):
                                    sha256_hash.update(chunk)
                            checksum = sha256_hash.hexdigest()

                            # Create/update ComponentStore entry
                            component_type_id = component_manifest.get('name', component_name.lower().replace(' ', '_'))

                            component, created = ComponentStore.objects.update_or_create(
                                component_type=component_type_id,
                                defaults={
                                    'display_name': component_manifest.get('display_name', component_name),
                                    'description': component_manifest.get('description', ''),
                                    'version': component_manifest['version'],
                                    'author': component_manifest.get('author', theme.author),
                                    'capabilities': component_manifest.get('props_schema', {}).get('properties', {}).keys() if 'props_schema' in component_manifest else [],
                                    'allowed_tiers': component_manifest.get('tier_compatibility', ['B', 'C']),
                                    'render_mode': 'ssr',  # Default to server-side rendering
                                    'checksum_sha256': checksum,
                                    'review_status': 'approved',  # Auto-approve theme-bundled components
                                    'source_theme': theme,  # Link to source theme
                                    'reviewed_by': user,
                                    'reviewed_at': timezone.now(),
                                }
                            )

                            # Save component package file
                            with open(component_zip_path, 'rb') as f:
                                from django.core.files import File
                                component.package_file.save(component_zip_name, File(f), save=True)

                            # Create/update ComponentRegistry entry
                            ComponentRegistry.objects.update_or_create(
                                slug=component_type_id,
                                defaults={
                                    'component_type': 'component',  # Generic component type
                                    'name': component_manifest.get('display_name', component_name),
                                    'current_version': component_manifest['version'],
                                    'latest_version': component_manifest['version'],
                                    'installed_at': timezone.now(),
                                    'update_available': False,
                                }
                            )

                            action = "Created" if created else "Updated"
                            success_msg = f"{action} component: {component_name} v{component_manifest['version']}"
                            logger.info(success_msg)
                            success_list.append(success_msg)

                    except Exception as comp_error:
                        error_msg = f"Failed to extract component {component_name}: {str(comp_error)}"
                        logger.error(error_msg)
                        error_list.append(error_msg)

        except Exception as e:
            logger.error(f"Failed to extract bundled components: {str(e)}")
            error_list.append(f"Extraction failed: {str(e)}")

        logger.info(f"Bundled component extraction complete: {len(success_list)} succeeded, {len(error_list)} failed")
        return len(success_list), success_list, error_list

    def get_current_theme(self):
        """Get currently active theme.

        Delegates to get_active_theme() — the canonical source of truth —
        so all callers resolve the active theme consistently via
        GlobalDesignSettings.active_theme.
        """
        from .theme_utils import get_active_theme

        current = cache.get('current_theme')
        if not current:
            current = get_active_theme()
            if current:
                cache.set('current_theme', current, 3600)
        return current

    def generate_layered_css(self, request=None):
        """
        Generate complete CSS with proper layering:
        1. Base CSS (platform utilities)
        2. Theme CSS (from theme package)
        3. Brand CSS (from database)
        4. Overrides (per-page/widget)
        """
        from .theme_models import ThemeBranding

        css_parts = []

        # 1. Base CSS (loaded separately via static files)
        # This would be in base.css

        # 2. Theme CSS
        theme = self.get_current_theme()
        if theme:
            css_parts.append(f'/* Theme: {theme.name} v{theme.version} */')
            theme_css_url = theme.get_css_url()
            if theme_css_url:
                css_parts.append(f'@import url("{theme_css_url}");')

        # 3. Brand CSS
        try:
            branding = ThemeBranding.objects.first()
            if branding:
                if not branding.generated_css:
                    branding.generate_css()
                css_parts.append('\n/* Brand Customizations */')
                css_parts.append(branding.generated_css)
        except:
            pass

        # 4. Page/Widget overrides would be added dynamically

        return '\n'.join(css_parts)

    def preview_theme(self, theme_id, branding_tokens=None):
        """
        Generate preview of theme with optional branding tokens
        Returns preview CSS for iframe rendering
        """
        from .theme_models import Theme, ThemeBranding

        try:
            theme = Theme.objects.get(id=theme_id)
            css_parts = []

            # Add theme CSS
            if theme.get_css_url():
                css_parts.append(f'@import url("{theme.get_css_url()}");')

            # Apply branding tokens if provided
            if branding_tokens:
                css_parts.append(':root {')
                for token, value in branding_tokens.items():
                    css_parts.append(f'  --{token}: {value};')
                css_parts.append('}')

            return '\n'.join(css_parts)

        except Theme.DoesNotExist:
            return ''

# Singleton instance
theme_service = ThemeService()