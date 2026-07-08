"""
Custom Fields Sync Serializer

Handles export/import of custom field models:
- CustomFieldGroup
- CustomFieldDefinition

Content types are serialized as 'app_label.model' strings for portability
between instances that may have different ContentType PKs.

Groups are exported/imported first so definitions can resolve their group FK.
Both models inherit SoftDeleteModel — the default manager excludes soft-deleted
records, but imports use all_objects to avoid unique constraint violations when
a matching soft-deleted record exists.
"""
import logging
from django.db import transaction
from django.contrib.contenttypes.models import ContentType

from .base import CollectionSyncSerializer

logger = logging.getLogger(__name__)

GROUP_FIELDS = [
    'name', 'slug', 'sort_order', 'is_active',
    'show_on_storefront', 'translations',
]

DEFINITION_FIELDS = [
    'name', 'slug', 'field_type', 'help_text_value',
    'default_value', 'validation_config',
    'is_required', 'is_active', 'show_on_storefront',
    'is_translatable', 'sort_order', 'translations',
]


class CustomFieldsSerializer(CollectionSyncSerializer):
    """Serializer for custom field groups and definitions.

    Models handled:
        - CustomFieldGroup: Grouping containers for custom fields
        - CustomFieldDefinition: Individual field definitions (type, validation, etc.)

    Natural keys:
        - Group: (slug, content_type)
        - Definition: (slug, content_type)
    """

    category_key = 'custom_fields'
    natural_key_fields = ['slug']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from custom_fields.models import CustomFieldGroup
        self.model_class = CustomFieldGroup

    def get_count(self):
        from custom_fields.models import CustomFieldGroup, CustomFieldDefinition
        return CustomFieldGroup.objects.count() + CustomFieldDefinition.objects.count()

    # -- Content type helpers --

    def _content_type_to_key(self, content_type):
        """Convert a ContentType instance to a portable 'app_label.model' string."""
        return f'{content_type.app_label}.{content_type.model}'

    def _key_to_content_type(self, key):
        """Resolve an 'app_label.model' string to a ContentType instance."""
        app_label, model = key.split('.')
        return ContentType.objects.get(app_label=app_label, model=model)

    # -- Export --

    def export(self, credential_mode='redact'):
        from custom_fields.models import CustomFieldGroup, CustomFieldDefinition

        items = []

        # Export groups first
        for group in CustomFieldGroup.objects.select_related('content_type').all():
            data = {field: getattr(group, field) for field in GROUP_FIELDS}
            data['_source_pk'] = group.pk
            data['_model'] = 'CustomFieldGroup'
            data['_content_type'] = self._content_type_to_key(group.content_type)
            items.append(data)

        # Export definitions
        for defn in CustomFieldDefinition.objects.select_related(
            'group', 'content_type'
        ).all():
            data = {field: getattr(defn, field) for field in DEFINITION_FIELDS}
            data['_source_pk'] = defn.pk
            data['_model'] = 'CustomFieldDefinition'
            data['_content_type'] = self._content_type_to_key(defn.content_type)
            data['_group_slug'] = defn.group.slug
            items.append(data)

        return {
            'category': self.category_key,
            'sync_type': 'collection',
            'items': items,
            'total': len(items),
        }

    # -- Import --

    def import_data(self, data, dry_run=False, sync_mode='additive'):
        if dry_run:
            return self.generate_diff(data)

        from custom_fields.models import CustomFieldDefinition

        items = data.get('items', [])
        synced = 0
        skipped = 0
        failed = 0
        deleted = 0
        errors = []

        try:
            with transaction.atomic():
                # Separate groups and definitions
                groups = [i for i in items if i.get('_model') == 'CustomFieldGroup']
                definitions = [i for i in items if i.get('_model') == 'CustomFieldDefinition']

                # Pass 1: Import groups (must exist before definitions)
                for item in groups:
                    try:
                        self._import_group(item)
                        synced += 1
                    except Exception as e:
                        failed += 1
                        errors.append(f"Group '{item.get('name', 'Unknown')}': {e}")
                        logger.error(
                            "Failed to import custom field group '%s': %s",
                            item.get('slug'), e
                        )

                # Pass 2: Import definitions (resolve group FK)
                for item in definitions:
                    try:
                        self._import_definition(item)
                        synced += 1
                    except Exception as e:
                        failed += 1
                        errors.append(f"Field '{item.get('name', 'Unknown')}': {e}")
                        logger.error(
                            "Failed to import custom field definition '%s': %s",
                            item.get('slug'), e
                        )

                # Mirror mode: delete local items not present in remote data
                if sync_mode == 'mirror':
                    deleted = self._delete_absent(items)

                # Invalidate custom fields cache for all affected content types
                ct_keys = {i.get('_content_type') for i in items if i.get('_content_type')}
                for ct_key in ct_keys:
                    try:
                        ct = self._key_to_content_type(ct_key)
                        CustomFieldDefinition.invalidate_cache(ct)
                    except ContentType.DoesNotExist:
                        pass

        except Exception as e:
            logger.error("Custom fields import failed: %s", e)
            return {'synced': 0, 'skipped': 0, 'failed': 1, 'errors': [str(e)]}

        result = {'synced': synced, 'skipped': skipped, 'failed': failed, 'errors': errors}
        if sync_mode == 'mirror':
            result['deleted'] = deleted
        return result

    def _import_group(self, item):
        """Import or update a custom field group."""
        from custom_fields.models import CustomFieldGroup

        ct = self._key_to_content_type(item['_content_type'])

        # Use all_objects to include soft-deleted groups (avoids unique constraint
        # violations if a matching soft-deleted group exists)
        existing = CustomFieldGroup.all_objects.filter(
            slug=item['slug'], content_type=ct
        ).first()

        if existing:
            for field in GROUP_FIELDS:
                if field in item:
                    setattr(existing, field, item[field])
            # Un-delete if it was soft-deleted
            if existing.is_deleted:
                existing.is_deleted = False
                existing.deleted_at = None
                existing.deleted_by = None
            existing.save()
        else:
            group = CustomFieldGroup(content_type=ct)
            for field in GROUP_FIELDS:
                if field in item:
                    setattr(group, field, item[field])
            group.save()

    def _import_definition(self, item):
        """Import or update a custom field definition."""
        from custom_fields.models import CustomFieldGroup, CustomFieldDefinition

        ct = self._key_to_content_type(item['_content_type'])

        # Resolve group FK via slug + content_type
        group = CustomFieldGroup.objects.filter(
            slug=item['_group_slug'], content_type=ct
        ).first()
        if not group:
            raise ValueError(
                f"Group '{item['_group_slug']}' not found for {item['_content_type']}"
            )

        # Use all_objects to include soft-deleted definitions
        existing = CustomFieldDefinition.all_objects.filter(
            slug=item['slug'], content_type=ct
        ).first()

        if existing:
            existing.group = group
            for field in DEFINITION_FIELDS:
                if field in item:
                    setattr(existing, field, item[field])
            if existing.is_deleted:
                existing.is_deleted = False
                existing.deleted_at = None
                existing.deleted_by = None
            existing.save()
        else:
            defn = CustomFieldDefinition(content_type=ct, group=group)
            for field in DEFINITION_FIELDS:
                if field in item:
                    setattr(defn, field, item[field])
            defn.save()

    def _delete_absent(self, items):
        """In mirror mode, delete local items not present in remote data."""
        from custom_fields.models import CustomFieldGroup, CustomFieldDefinition

        deleted_count = 0

        # Build sets of remote (slug, content_type_key) pairs
        remote_groups = set()
        remote_defs = set()
        for item in items:
            key = (item.get('slug'), item.get('_content_type'))
            if item.get('_model') == 'CustomFieldGroup':
                remote_groups.add(key)
            elif item.get('_model') == 'CustomFieldDefinition':
                remote_defs.add(key)

        # Delete definitions first (they FK to groups)
        for defn in CustomFieldDefinition.objects.select_related('content_type').all():
            key = (defn.slug, self._content_type_to_key(defn.content_type))
            if key not in remote_defs:
                defn.delete()
                deleted_count += 1

        # Delete groups
        for group in CustomFieldGroup.objects.select_related('content_type').all():
            key = (group.slug, self._content_type_to_key(group.content_type))
            if key not in remote_groups:
                group.delete()
                deleted_count += 1

        return deleted_count

    # -- Diff --

    def generate_diff(self, remote_data):
        from custom_fields.models import CustomFieldGroup, CustomFieldDefinition

        items = remote_data.get('items', [])
        if not items:
            return {'changes': [], 'warnings': [], 'summary': 'No data to sync'}

        changes = []
        warnings = []

        for item in items:
            model_type = item.get('_model')
            ct_key = item.get('_content_type')

            # Resolve content type
            try:
                ct = self._key_to_content_type(ct_key)
            except (ContentType.DoesNotExist, ValueError, AttributeError):
                warnings.append(f"Unknown content type '{ct_key}', will be skipped")
                continue

            display_name = f"{item.get('name', item.get('slug', 'Unknown'))} ({ct_key})"

            if model_type == 'CustomFieldGroup':
                existing = CustomFieldGroup.objects.filter(
                    slug=item.get('slug'), content_type=ct
                ).first()
                compare_fields = GROUP_FIELDS
            elif model_type == 'CustomFieldDefinition':
                existing = CustomFieldDefinition.objects.filter(
                    slug=item.get('slug'), content_type=ct
                ).first()
                compare_fields = DEFINITION_FIELDS
            else:
                continue

            if existing:
                field_changes = self._compute_field_diff(existing, item, compare_fields)
                if field_changes:
                    changes.append({
                        'type': 'modify',
                        'model': model_type,
                        'name': display_name,
                        'changes': field_changes,
                    })
            else:
                changes.append({
                    'type': 'add',
                    'model': model_type,
                    'name': display_name,
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
            'warnings': warnings,
            'summary': ', '.join(parts) if parts else 'No changes',
        }

    # -- Snapshot & Restore --

    def snapshot_current(self):
        return self.export(credential_mode='skip')

    def restore_snapshot(self, snapshot):
        try:
            result = self.import_data(snapshot, dry_run=False)
            return {'restored': result.get('synced', 0), 'errors': result.get('errors', [])}
        except Exception as e:
            return {'restored': 0, 'errors': [str(e)]}
