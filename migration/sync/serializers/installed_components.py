"""
Installed Components Sync Serializer

Handles export/import of installed component packages:
- ComponentRegistry (DB records)
- ComponentVersion (version history)
- ComponentDependency (inter-component dependencies)
- Filesystem packages (themes as ZIPs, integrations/utilities as directory archives)

This is a full_migration only category that must be imported BEFORE
any provider categories so that provider accounts can reference their components.
"""
import base64
import io
import logging
import os
import zipfile
from pathlib import Path

from django.conf import settings
from django.db import transaction

from .base import CollectionSyncSerializer

logger = logging.getLogger(__name__)

REGISTRY_FIELDS = [
    'component_type', 'slug', 'name', 'current_version',
    'update_available', 'latest_version', 'latest_version_checksum',
    'auto_update', 'locked', 'lock_reason',
    'author', 'author_details', 'description',
    'homepage_url', 'support_url', 'thumbnail_url',
    'preview_images', 'preview_videos',
    'requires_platform_version', 'engine_min_version', 'engine_max_version',
]

VERSION_FIELDS = [
    'version', 'is_active', 'install_method',
    'rollback_available', 'health_status', 'health_details',
    'package_checksum', 'package_size_bytes', 'package_url',
    'release_notes', 'breaking_changes', 'security_update',
]

DEPENDENCY_FIELDS = [
    'version_constraint', 'is_required',
]

# Max inline package size (50MB for themes, most are ~2-5MB)
MAX_PACKAGE_SIZE = 50 * 1024 * 1024


def _get_components_data_root():
    return Path(settings.BASE_DIR) / 'components_data'


def _zip_directory(dir_path):
    """Zip a directory tree into an in-memory bytes buffer."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        base = Path(dir_path)
        for file_path in base.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(base)
                zf.write(file_path, arcname)
    buffer.seek(0)
    return buffer.read()


def _extract_zip_to(zip_data, target_dir):
    """Extract zip bytes into target directory."""
    target = Path(target_dir)
    target.mkdir(parents=True, exist_ok=True)
    buffer = io.BytesIO(zip_data)
    with zipfile.ZipFile(buffer, 'r') as zf:
        zf.extractall(target)


class InstalledComponentsSerializer(CollectionSyncSerializer):
    """Serializer for installed component packages.

    Handles three model types plus filesystem data:
        - ComponentRegistry: Component registration records
        - ComponentVersion: Version history for each component
        - ComponentDependency: Inter-component dependency declarations

    Filesystem handling:
        - Themes: Export Theme.package_file (already a .zip)
        - Integrations: Zip the current/ directory for each provider component
        - Utilities: Zip static + template directories for each utility
    """

    category_key = 'installed_components'
    natural_key_fields = ['component_type', 'slug']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from component_updates.models import ComponentRegistry
        self.model_class = ComponentRegistry

    def get_count(self):
        from component_updates.models import (
            ComponentRegistry, ComponentVersion, ComponentDependency,
        )
        return (
            ComponentRegistry.objects.count()
            + ComponentVersion.objects.count()
            + ComponentDependency.objects.count()
        )

    def export(self, credential_mode='redact'):
        from component_updates.models import (
            ComponentRegistry, ComponentVersion, ComponentDependency,
        )

        items = []
        components_root = _get_components_data_root()

        for comp in ComponentRegistry.objects.prefetch_related(
            'versions', 'dependencies', 'dependencies__depends_on',
        ).all():
            data = {f: getattr(comp, f) for f in REGISTRY_FIELDS}
            data['_source_pk'] = comp.pk
            data['_model'] = 'ComponentRegistry'

            # OneToOne references (portable by slug)
            if comp.theme:
                data['_theme_slug'] = comp.theme.slug
            if comp.header_template:
                data['_header_template_slug'] = comp.header_template.slug
            if comp.footer_template:
                data['_footer_template_slug'] = comp.footer_template.slug

            # Versions
            data['_versions'] = []
            for ver in comp.versions.all().order_by('-installed_at'):
                v_data = {f: getattr(ver, f) for f in VERSION_FIELDS}
                if ver.installed_at:
                    v_data['_installed_at'] = ver.installed_at.isoformat()
                if ver.uninstalled_at:
                    v_data['_uninstalled_at'] = ver.uninstalled_at.isoformat()
                data['_versions'].append(v_data)

            # Dependencies
            data['_dependencies'] = []
            for dep in comp.dependencies.all():
                d_data = {f: getattr(dep, f) for f in DEPENDENCY_FIELDS}
                d_data['_depends_on_type'] = dep.depends_on.component_type
                d_data['_depends_on_slug'] = dep.depends_on.slug
                data['_dependencies'].append(d_data)

            # Filesystem package export
            data['_package'] = self._export_package(comp, components_root)

            items.append(data)

        return {
            'category': self.category_key,
            'sync_type': 'collection',
            'items': items,
            'total': len(items),
        }

    def _export_package(self, comp, components_root):
        """Export filesystem package for a component as base64.

        Strategy:
        - Themes: Use Theme.package_file if available (it's already a .zip)
        - Integrations: Zip the resolved current/ directory
        - Utilities: Zip static/ and templates/ current directories
        """
        ctype = comp.component_type
        slug = comp.slug

        # Theme: prefer the stored package_file
        if ctype == 'theme' and comp.theme:
            try:
                pf = comp.theme.package_file
                if pf and pf.storage.exists(pf.name):
                    raw = pf.read()
                    if len(raw) <= MAX_PACKAGE_SIZE:
                        return {
                            'source': 'package_file',
                            'data': base64.b64encode(raw).decode('ascii'),
                            'size': len(raw),
                        }
                    else:
                        logger.warning(
                            f"Theme package too large for inline transfer: "
                            f"{comp.slug} ({len(raw)} bytes)"
                        )
                        return {'source': 'too_large', 'size': len(raw)}
            except Exception as e:
                logger.warning(f"Could not read theme package for {slug}: {e}")

        # Theme fallback: zip extracted directory
        if ctype == 'theme':
            theme_dir = components_root / 'static' / 'design' / 'themes' / slug / 'current'
            if theme_dir.exists():
                resolved = theme_dir.resolve()
                if resolved.is_dir():
                    try:
                        raw = _zip_directory(resolved)
                        if len(raw) <= MAX_PACKAGE_SIZE:
                            return {
                                'source': 'directory',
                                'path_type': 'theme',
                                'data': base64.b64encode(raw).decode('ascii'),
                                'size': len(raw),
                            }
                    except Exception as e:
                        logger.warning(f"Could not zip theme directory for {slug}: {e}")
            return None

        # Integration providers
        integration_types = [
            'shipping_provider', 'email_provider', 'sms_provider',
            'exchange_rate_provider', 'payment_provider',
            'product_feed_provider', 'terminal_provider',
            'seo_generator_provider', 'translation_provider',
        ]
        if ctype in integration_types:
            int_dir = components_root / 'integrations' / ctype / slug / 'current'
            if int_dir.exists():
                resolved = int_dir.resolve()
                if resolved.is_dir():
                    try:
                        raw = _zip_directory(resolved)
                        if len(raw) <= MAX_PACKAGE_SIZE:
                            return {
                                'source': 'directory',
                                'path_type': 'integration',
                                'component_type': ctype,
                                'data': base64.b64encode(raw).decode('ascii'),
                                'size': len(raw),
                            }
                    except Exception as e:
                        logger.warning(f"Could not zip integration for {ctype}/{slug}: {e}")
            return None

        # Utilities (widget, utility, element)
        if ctype in ('widget', 'utility', 'element'):
            package_parts = {}

            # Static files
            static_dir = components_root / 'static' / 'utilities' / slug / 'current'
            if static_dir.exists():
                resolved = static_dir.resolve()
                if resolved.is_dir():
                    try:
                        raw = _zip_directory(resolved)
                        package_parts['static'] = base64.b64encode(raw).decode('ascii')
                    except Exception as e:
                        logger.warning(f"Could not zip utility static for {slug}: {e}")

            # Template files
            tmpl_dir = components_root / 'templates' / 'utilities' / slug / 'current'
            if tmpl_dir.exists():
                resolved = tmpl_dir.resolve()
                if resolved.is_dir():
                    try:
                        raw = _zip_directory(resolved)
                        package_parts['templates'] = base64.b64encode(raw).decode('ascii')
                    except Exception as e:
                        logger.warning(f"Could not zip utility templates for {slug}: {e}")

            if package_parts:
                return {
                    'source': 'directory',
                    'path_type': 'utility',
                    **package_parts,
                }
            return None

        # Header/footer templates
        if ctype in ('header_template', 'footer_template'):
            # These are typically theme-bundled, no separate filesystem
            return None

        return None

    def import_data(self, data, dry_run=False, sync_mode='additive'):
        if dry_run:
            return self.generate_diff(data)

        items = data.get('items', [])
        synced = 0
        skipped = 0
        failed = 0
        errors = []

        for item in items:
            try:
                with transaction.atomic():
                    self._import_component(item)
                    synced += 1
            except Exception as e:
                slug = item.get('slug', '?')
                ctype = item.get('component_type', '?')
                failed += 1
                errors.append(f"Component {ctype}/{slug}: {e}")

        # Second pass: dependencies (all components must exist first)
        for item in items:
            try:
                self._import_dependencies(item)
            except Exception as e:
                errors.append(f"Dependencies for {item.get('slug', '?')}: {e}")

        result = {'synced': synced, 'skipped': skipped, 'failed': failed, 'errors': errors}

        if sync_mode == 'mirror':
            deleted = self._delete_absent(items)
            result['deleted'] = deleted

        return result

    def _import_component(self, item):
        from component_updates.models import ComponentRegistry, ComponentVersion

        ctype = item['component_type']
        slug = item['slug']

        existing = ComponentRegistry.objects.filter(
            component_type=ctype, slug=slug,
        ).first()
        comp = existing or ComponentRegistry()

        for f in REGISTRY_FIELDS:
            if f in item:
                setattr(comp, f, item[f])

        # Don't link OneToOne FKs yet — they'll be resolved after
        # theme/header/footer imports by the design_theme serializer
        comp.save()

        # Import filesystem package
        package = item.get('_package')
        if package:
            self._import_package(comp, package)

        # Import versions (clear existing and recreate)
        if existing:
            comp.versions.all().delete()

        for v_data in item.get('_versions', []):
            ver = ComponentVersion(component=comp)
            for f in VERSION_FIELDS:
                if f in v_data:
                    setattr(ver, f, v_data[f])
            # Datetime fields
            from django.utils.dateparse import parse_datetime
            installed_at = v_data.get('_installed_at')
            if installed_at:
                parsed = parse_datetime(installed_at)
                if parsed:
                    ver.installed_at = parsed
            uninstalled_at = v_data.get('_uninstalled_at')
            if uninstalled_at:
                parsed = parse_datetime(uninstalled_at)
                if parsed:
                    ver.uninstalled_at = parsed
            ver.save()

    def _import_package(self, comp, package):
        """Import filesystem package for a component."""
        components_root = _get_components_data_root()
        ctype = comp.component_type
        slug = comp.slug
        version = comp.current_version

        source = package.get('source')
        if source == 'too_large':
            logger.warning(f"Skipping large package for {ctype}/{slug}")
            return

        if source == 'package_file' and ctype == 'theme':
            # Theme with stored package: save as package_file then extract
            raw = base64.b64decode(package['data'])
            self._install_theme_package(comp, raw, components_root, version)
            return

        if source == 'directory':
            path_type = package.get('path_type')

            if path_type == 'theme':
                raw = base64.b64decode(package['data'])
                target = components_root / 'static' / 'design' / 'themes' / slug / version
                _extract_zip_to(raw, str(target))
                self._create_symlink(target.parent / 'current', target)

            elif path_type == 'integration':
                raw = base64.b64decode(package['data'])
                int_ctype = package.get('component_type', ctype)
                target = (
                    components_root / 'integrations' / int_ctype / slug
                    / f'v{version}'
                )
                _extract_zip_to(raw, str(target))
                self._create_symlink(target.parent / 'current', target)

            elif path_type == 'utility':
                # Static files
                static_data = package.get('static')
                if static_data:
                    raw = base64.b64decode(static_data)
                    target = (
                        components_root / 'static' / 'utilities' / slug
                        / f'v{version}'
                    )
                    _extract_zip_to(raw, str(target))
                    self._create_symlink(target.parent / 'current', target)

                # Template files
                tmpl_data = package.get('templates')
                if tmpl_data:
                    raw = base64.b64decode(tmpl_data)
                    target = (
                        components_root / 'templates' / 'utilities' / slug
                        / f'v{version}'
                    )
                    _extract_zip_to(raw, str(target))
                    self._create_symlink(target.parent / 'current', target)

    def _install_theme_package(self, comp, raw_zip, components_root, version):
        """Install a theme from its package file ZIP."""
        from django.core.files.base import ContentFile

        # Save as package_file on the Theme model if it exists
        if comp.theme:
            theme = comp.theme
            theme.package_file.save(
                f'{comp.slug}-{version}.zip',
                ContentFile(raw_zip),
                save=False,
            )

            # Extract to theme directory
            target = (
                components_root / 'static' / 'design' / 'themes'
                / comp.slug / version
            )
            _extract_zip_to(raw_zip, str(target))
            self._create_symlink(target.parent / 'current', target)

            # Update extracted_path
            theme.extracted_path = str(target.parent / 'current')
            theme.save()

    @staticmethod
    def _create_symlink(link_path, target_path):
        """Create or replace a symlink atomically."""
        link = Path(link_path)
        target = Path(target_path)

        link.parent.mkdir(parents=True, exist_ok=True)

        # Atomic rename pattern
        temp_link = link.parent / f'.tmp_symlink_{os.getpid()}'
        try:
            if temp_link.is_symlink() or temp_link.exists():
                temp_link.unlink()
            temp_link.symlink_to(target)
            temp_link.replace(link)
        except Exception:
            if temp_link.is_symlink() or temp_link.exists():
                temp_link.unlink()
            raise

    def _import_dependencies(self, item):
        from component_updates.models import ComponentRegistry, ComponentDependency

        ctype = item['component_type']
        slug = item['slug']
        comp = ComponentRegistry.objects.filter(
            component_type=ctype, slug=slug,
        ).first()
        if not comp:
            return

        # Clear existing dependencies
        comp.dependencies.all().delete()

        for d_data in item.get('_dependencies', []):
            dep_type = d_data.get('_depends_on_type')
            dep_slug = d_data.get('_depends_on_slug')
            if dep_type and dep_slug:
                depends_on = ComponentRegistry.objects.filter(
                    component_type=dep_type, slug=dep_slug,
                ).first()
                if depends_on:
                    dep = ComponentDependency(
                        component=comp,
                        depends_on=depends_on,
                    )
                    for f in DEPENDENCY_FIELDS:
                        if f in d_data:
                            setattr(dep, f, d_data[f])
                    dep.save()

    def _delete_absent(self, remote_items):
        from component_updates.models import ComponentRegistry

        remote_keys = {
            (item['component_type'], item['slug'])
            for item in remote_items
        }
        deleted = 0
        for comp in ComponentRegistry.objects.all():
            if (comp.component_type, comp.slug) not in remote_keys:
                try:
                    # Remove filesystem data
                    self._remove_component_files(comp)
                    comp.delete()
                    deleted += 1
                except Exception as e:
                    logger.warning(
                        f"Cannot delete component {comp.component_type}/{comp.slug}: {e}"
                    )
        return deleted

    def _remove_component_files(self, comp):
        """Remove filesystem files for a component."""
        import shutil
        components_root = _get_components_data_root()
        ctype = comp.component_type
        slug = comp.slug

        dirs_to_remove = []
        if ctype == 'theme':
            dirs_to_remove.append(
                components_root / 'static' / 'design' / 'themes' / slug
            )
        elif ctype in ('widget', 'utility', 'element'):
            dirs_to_remove.extend([
                components_root / 'static' / 'utilities' / slug,
                components_root / 'templates' / 'utilities' / slug,
            ])
        else:
            dirs_to_remove.append(
                components_root / 'integrations' / ctype / slug
            )

        for d in dirs_to_remove:
            if d.exists():
                try:
                    shutil.rmtree(d)
                except Exception as e:
                    logger.warning(f"Could not remove {d}: {e}")

    def generate_diff(self, remote_data):
        from component_updates.models import ComponentRegistry

        items = remote_data.get('items', [])
        changes = []

        for item in items:
            existing = ComponentRegistry.objects.filter(
                component_type=item.get('component_type'),
                slug=item.get('slug'),
            ).first()

            name = f"{item.get('component_type')}/{item.get('slug')}"

            if existing:
                field_changes = self._compute_field_diff(existing, item, REGISTRY_FIELDS)
                if field_changes:
                    changes.append({
                        'type': 'modify', 'model': 'ComponentRegistry',
                        'name': name, 'changes': field_changes,
                    })
            else:
                changes.append({
                    'type': 'add', 'model': 'ComponentRegistry',
                    'name': name,
                    'fields': {k: v for k, v in item.items() if not k.startswith('_')},
                })

        adds = sum(1 for c in changes if c['type'] == 'add')
        mods = sum(1 for c in changes if c['type'] == 'modify')
        parts = []
        if adds:
            parts.append(f'{adds} addition(s)')
        if mods:
            parts.append(f'{mods} modification(s)')

        return {
            'changes': changes,
            'warnings': [],
            'summary': ', '.join(parts) if parts else 'No changes',
        }

    def snapshot_current(self):
        return self.export(credential_mode='skip')

    def restore_snapshot(self, snapshot):
        try:
            result = self.import_data(snapshot, dry_run=False)
            return {'restored': result.get('synced', 0), 'errors': result.get('errors', [])}
        except Exception as e:
            return {'restored': 0, 'errors': [str(e)]}
