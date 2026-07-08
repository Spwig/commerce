"""
Media Sync Serializer

Handles export/import of media library models (full_migration only):
- MediaAsset

Large data category - files are base64-encoded inline.
"""
import logging
from django.db import transaction

from .base import CollectionSyncSerializer
from ..file_handler import export_file_field, import_file_field

logger = logging.getLogger(__name__)

MEDIA_ASSET_FIELDS = [
    'title', 'alt_text', 'description', 'external_id',
    'file_size', 'width', 'height', 'mime_type',
    'metadata', 'translations',
    'focal_point_x', 'focal_point_y', 'is_public',
]


class MediaSerializer(CollectionSyncSerializer):
    """Serializer for the media library (full_migration only).

    Models handled:
        - MediaAsset: All uploaded media files (images, documents, videos)

    Note: Large data category. Files are base64-encoded for transfer.
    Only original_file is transferred (webp/video conversions regenerated on target).
    """

    category_key = 'media'
    natural_key_fields = ['external_id']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from media_library.models import MediaAsset
        self.model_class = MediaAsset

    def get_count(self):
        from media_library.models import MediaAsset
        return MediaAsset.objects.count()

    def export(self, credential_mode='redact'):
        from media_library.models import MediaAsset

        items = []
        files = {}

        for asset in MediaAsset.objects.all():
            data = {f: getattr(asset, f) for f in MEDIA_ASSET_FIELDS}
            data['_source_pk'] = str(asset.pk)
            data['_model'] = 'MediaAsset'
            data['_uuid'] = str(asset.pk)

            # Folder path for reconstruction
            if asset.folder:
                data['_folder_path'] = asset.folder.path
            else:
                data['_folder_path'] = None

            # Tags
            data['_tags'] = list(asset.tags.values_list('name', flat=True))

            # Export file
            file_key = f'MediaAsset:{asset.pk}:original_file'
            file_data = export_file_field(asset, 'original_file')
            if file_data:
                files[file_key] = file_data
                data['_file_key'] = file_key

            # Datetime
            if asset.created_at:
                data['_created_at'] = asset.created_at.isoformat()

            items.append(data)

        return {
            'category': self.category_key,
            'sync_type': 'collection',
            'items': items,
            'total': len(items),
            'files': files,
        }

    def import_data(self, data, dry_run=False, sync_mode='additive'):
        if dry_run:
            return self.generate_diff(data)

        items = data.get('items', [])
        files = data.get('files', {})
        synced = 0
        skipped = 0
        failed = 0
        errors = []

        for item in items:
            try:
                with transaction.atomic():
                    self._import_asset(item, files)
                    synced += 1
            except Exception as e:
                failed += 1
                errors.append(f"{item.get('title', 'Unknown')}: {e}")

        result = {'synced': synced, 'skipped': skipped, 'failed': failed, 'errors': errors}

        if sync_mode == 'mirror':
            deleted = self._delete_absent(items)
            result['deleted'] = deleted

        return result

    def _import_asset(self, item, files):
        from media_library.models import MediaAsset, Tag

        external_id = item.get('external_id')

        # Try to match by external_id if available
        existing = None
        if external_id:
            existing = MediaAsset.objects.filter(external_id=external_id).first()

        if existing:
            for f in MEDIA_ASSET_FIELDS:
                if f in item:
                    setattr(existing, f, item[f])
            # Import file if provided
            file_key = item.get('_file_key')
            if file_key and file_key in files:
                import_file_field(existing, 'original_file', files[file_key])
            existing.save()
            asset = existing
        else:
            asset = MediaAsset()
            for f in MEDIA_ASSET_FIELDS:
                if f in item:
                    setattr(asset, f, item[f])
            # Import file
            file_key = item.get('_file_key')
            if file_key and file_key in files:
                import_file_field(asset, 'original_file', files[file_key])
            asset.save()

        # Handle tags
        tag_names = item.get('_tags', [])
        if tag_names:
            tags = []
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(
                    name=name,
                    defaults={'slug': name.lower().replace(' ', '-')},
                )
                tags.append(tag)
            asset.tags.set(tags)

        # Handle folder
        folder_path = item.get('_folder_path')
        if folder_path and not asset.folder:
            from media_library.models import MediaFolder
            folder = MediaFolder.objects.filter(path=folder_path).first()
            if folder:
                asset.folder = folder
                asset.save(update_fields=['folder'])

    def _delete_absent(self, remote_items):
        from media_library.models import MediaAsset

        remote_ids = set()
        for item in remote_items:
            eid = item.get('external_id')
            if eid:
                remote_ids.add(eid)

        deleted = 0
        for asset in MediaAsset.objects.exclude(external_id=''):
            if asset.external_id not in remote_ids:
                try:
                    asset.hard_delete()
                    deleted += 1
                except Exception as e:
                    logger.warning(f"Cannot delete media asset {asset.pk}: {e}")
        return deleted

    def generate_diff(self, remote_data):
        from media_library.models import MediaAsset

        items = remote_data.get('items', [])
        changes = []

        for item in items:
            external_id = item.get('external_id')
            title = item.get('title', 'Unknown')

            existing = None
            if external_id:
                existing = MediaAsset.objects.filter(external_id=external_id).first()

            if existing:
                field_changes = self._compute_field_diff(existing, item, MEDIA_ASSET_FIELDS)
                if field_changes:
                    changes.append({
                        'type': 'modify', 'model': 'MediaAsset',
                        'name': title, 'changes': field_changes,
                    })
            else:
                changes.append({
                    'type': 'add', 'model': 'MediaAsset',
                    'name': title,
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
        # Snapshot metadata only (file data too large for snapshot)
        from media_library.models import MediaAsset

        items = []
        for asset in MediaAsset.objects.all():
            data = {f: getattr(asset, f) for f in MEDIA_ASSET_FIELDS}
            data['_source_pk'] = str(asset.pk)
            data['_model'] = 'MediaAsset'
            data['_uuid'] = str(asset.pk)
            items.append(data)

        return {
            'category': self.category_key,
            'sync_type': 'collection',
            'items': items,
            'total': len(items),
        }

    def restore_snapshot(self, snapshot):
        try:
            result = self.import_data(snapshot, dry_run=False)
            return {'restored': result.get('synced', 0), 'errors': result.get('errors', [])}
        except Exception as e:
            return {'restored': 0, 'errors': [str(e)]}
