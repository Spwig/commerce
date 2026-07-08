"""
Base Sync Serializer

Abstract base class for all sync category serializers.
Each serializer handles: export, import, diff, snapshot, and restore.
"""
import logging
from django.db import transaction

logger = logging.getLogger(__name__)


class BaseSyncSerializer:
    """
    Base class for all sync category serializers.

    Subclasses must implement:
    - export(): Serialize local data to a transferable dict
    - import_data(): Apply incoming data to the local database
    - generate_diff(): Compare incoming data with local state
    - snapshot_current(): Take a snapshot of current state for rollback
    - restore_snapshot(): Restore from a snapshot

    The `credential_mode` parameter controls how encrypted credentials are handled:
    - 'decrypt': Decrypt and include plaintext credentials (for actual transfer)
    - 'redact': Include masked/redacted credentials (for preview)
    - 'skip': Omit credential fields entirely
    """

    category_key = None  # Must be set by subclass
    sync_type = 'collection'  # 'singleton' or 'collection'

    def __init__(self, sync_job=None, sync_step=None):
        self.sync_job = sync_job
        self.sync_step = sync_step

    def export(self, credential_mode='redact'):
        """
        Export local data as a serializable dict.

        Args:
            credential_mode: How to handle credentials ('decrypt', 'redact', 'skip')

        Returns:
            dict: {
                'category': str,
                'sync_type': str,
                'items': list[dict] (for collections) or dict (for singletons),
                'total': int,
                'files': list[dict] (optional, base64-encoded file data)
            }
        """
        raise NotImplementedError

    def import_data(self, data, dry_run=False, sync_mode='additive'):
        """
        Import data into the local database.

        Args:
            data: dict from export() of the remote instance
            dry_run: If True, return diff without applying changes
            sync_mode: 'additive' (add/update only) or 'mirror' (includes deletions)

        Returns:
            dict: {
                'synced': int,
                'skipped': int,
                'failed': int,
                'deleted': int (only in mirror mode),
                'errors': list[str],
                'changes': list[dict] (if dry_run)
            }
        """
        raise NotImplementedError

    def generate_diff(self, remote_data):
        """
        Compare remote data with local state and produce a structured diff.

        Args:
            remote_data: dict from export() of the remote instance

        Returns:
            dict: {
                'changes': [
                    {
                        'type': 'add' | 'modify' | 'remove',
                        'model': str,
                        'name': str,
                        'fields': dict (for add),
                        'changes': [{'field': str, 'old': any, 'new': any}] (for modify),
                    }
                ],
                'warnings': list[str],
                'summary': str
            }
        """
        raise NotImplementedError

    def snapshot_current(self):
        """
        Take a snapshot of the current state for rollback.

        Returns:
            dict: Serialized current state that can be passed to restore_snapshot()
        """
        raise NotImplementedError

    def restore_snapshot(self, snapshot):
        """
        Restore state from a snapshot (rollback).

        Args:
            snapshot: dict from snapshot_current()

        Returns:
            dict: {restored: int, errors: list[str]}
        """
        raise NotImplementedError

    def get_count(self):
        """
        Get the count of items in this category.

        Returns:
            int: Number of items
        """
        raise NotImplementedError

    # ---- Helper methods for subclasses ----

    def _serialize_model_instance(self, instance, fields, exclude=None):
        """
        Serialize a model instance to a dict.

        Args:
            instance: Django model instance
            fields: list of field names to include
            exclude: list of field names to exclude

        Returns:
            dict: Serialized fields
        """
        exclude = exclude or []
        data = {}
        for field_name in fields:
            if field_name in exclude:
                continue
            field = instance._meta.get_field(field_name)
            value = getattr(instance, field_name)

            # Handle special field types
            if hasattr(value, 'pk'):
                # ForeignKey - store the related object's natural key or ID
                data[field_name] = value.pk if value else None
            elif hasattr(field, 'value_from_object'):
                data[field_name] = field.value_from_object(instance)
            else:
                data[field_name] = value

        return data

    def _get_model_fields(self, model_class, exclude=None):
        """
        Get serializable field names for a model, excluding auto fields and specified fields.
        """
        exclude = set(exclude or [])
        exclude.update({'id', 'pk'})
        fields = []
        for field in model_class._meta.get_fields():
            if hasattr(field, 'column') and field.name not in exclude:
                fields.append(field.name)
        return fields

    def _match_by_natural_key(self, model_class, data, key_fields):
        """
        Find an existing model instance by natural key fields.

        Args:
            model_class: Django model class
            data: dict with field values
            key_fields: list of field names that form the natural key

        Returns:
            model instance or None
        """
        lookup = {}
        for field in key_fields:
            value = data.get(field)
            if value is None:
                return None
            lookup[field] = value

        try:
            return model_class.objects.get(**lookup)
        except model_class.DoesNotExist:
            return None
        except model_class.MultipleObjectsReturned:
            return model_class.objects.filter(**lookup).first()

    def _compute_field_diff(self, existing, incoming, fields):
        """
        Compare field values between an existing instance and incoming data.

        Returns:
            list of {field, old, new} dicts for changed fields
        """
        changes = []
        for field_name in fields:
            old_value = getattr(existing, field_name, None)
            new_value = incoming.get(field_name)

            # Normalize for comparison
            if hasattr(old_value, 'pk'):
                old_value = old_value.pk if old_value else None

            if old_value != new_value:
                changes.append({
                    'field': field_name,
                    'old': str(old_value)[:200] if old_value is not None else None,
                    'new': str(new_value)[:200] if new_value is not None else None,
                })

        return changes


class SingletonSyncSerializer(BaseSyncSerializer):
    """
    Base class for singleton model serializers (e.g., SiteSettings, BlogSettings).
    """
    sync_type = 'singleton'
    model_class = None  # Must be set by subclass
    export_fields = None  # Must be set by subclass
    exclude_fields = None  # Fields to exclude from export/import

    def get_count(self):
        return 1 if self.model_class.objects.exists() else 0

    def _get_instance(self):
        """Get the singleton instance."""
        return self.model_class.objects.first()

    def export(self, credential_mode='redact'):
        instance = self._get_instance()
        if not instance:
            return {
                'category': self.category_key,
                'sync_type': 'singleton',
                'items': {},
                'total': 0,
            }

        fields = self.export_fields or self._get_model_fields(
            self.model_class, exclude=self.exclude_fields
        )
        data = self._serialize_model_instance(instance, fields)

        return {
            'category': self.category_key,
            'sync_type': 'singleton',
            'items': data,
            'total': 1,
        }

    def snapshot_current(self):
        return self.export(credential_mode='skip')

    def generate_diff(self, remote_data):
        items = remote_data.get('items', {})
        if not items:
            return {'changes': [], 'warnings': [], 'summary': 'No data to sync'}

        instance = self._get_instance()
        if not instance:
            return {
                'changes': [{'type': 'add', 'model': self.model_class.__name__,
                             'name': 'Settings', 'fields': items}],
                'warnings': [],
                'summary': '1 addition',
            }

        fields = list(items.keys())
        changes = self._compute_field_diff(instance, items, fields)
        if not changes:
            return {'changes': [], 'warnings': [], 'summary': 'No changes'}

        return {
            'changes': [{
                'type': 'modify',
                'model': self.model_class.__name__,
                'name': 'Settings',
                'changes': changes,
            }],
            'warnings': [],
            'summary': f'{len(changes)} field(s) modified',
        }


class CollectionSyncSerializer(BaseSyncSerializer):
    """
    Base class for collection model serializers (multiple instances).
    """
    sync_type = 'collection'
    model_class = None  # Primary model class
    natural_key_fields = None  # Fields that form the natural key for matching
    export_fields = None
    exclude_fields = None

    def get_count(self):
        return self.model_class.objects.count()

    def _get_queryset(self):
        """Get the queryset for export. Override for custom filtering."""
        return self.model_class.objects.all()

    def export(self, credential_mode='redact'):
        queryset = self._get_queryset()
        fields = self.export_fields or self._get_model_fields(
            self.model_class, exclude=self.exclude_fields
        )

        items = []
        for instance in queryset:
            data = self._serialize_model_instance(instance, fields)
            data['_source_pk'] = instance.pk
            items.append(data)

        return {
            'category': self.category_key,
            'sync_type': 'collection',
            'items': items,
            'total': len(items),
        }

    def snapshot_current(self):
        return self.export(credential_mode='skip')

    def generate_diff(self, remote_data):
        items = remote_data.get('items', [])
        if not items:
            return {'changes': [], 'warnings': [], 'summary': 'No data to sync'}

        changes = []
        for item_data in items:
            existing = self._match_by_natural_key(
                self.model_class, item_data, self.natural_key_fields or []
            )
            if existing:
                fields = [k for k in item_data.keys() if k != '_source_pk']
                field_changes = self._compute_field_diff(existing, item_data, fields)
                if field_changes:
                    changes.append({
                        'type': 'modify',
                        'model': self.model_class.__name__,
                        'name': self._get_display_name(item_data),
                        'changes': field_changes,
                    })
            else:
                changes.append({
                    'type': 'add',
                    'model': self.model_class.__name__,
                    'name': self._get_display_name(item_data),
                    'fields': {k: v for k, v in item_data.items() if k != '_source_pk'},
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

    def _get_display_name(self, item_data):
        """Get a human-readable name for an item. Override for custom display."""
        for field in ['name', 'title', 'slug', 'code']:
            if field in item_data and item_data[field]:
                return str(item_data[field])
        return str(item_data.get('_source_pk', 'Unknown'))
