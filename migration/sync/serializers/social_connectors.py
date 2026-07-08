"""
Blog Social Connectors Sync Serializer

Handles export/import of blog social connector accounts.
OAuth tokens will need re-authorization on the destination.
"""
import logging
from django.db import transaction
from django.contrib.sites.models import Site

from .base import CollectionSyncSerializer
from ..credential_handler import (
    decrypt_credentials_for_export, encrypt_credentials_for_import,
    redact_credentials,
)

logger = logging.getLogger(__name__)

SOCIAL_CONNECTOR_FIELDS = [
    'provider_key', 'name', 'platform_account_id',
    'platform_account_name', 'platform_account_url', 'platform_avatar_url',
    'status', 'auto_share_enabled', 'is_default_for_provider',
    'post_template', 'default_hashtags',
]


class SocialConnectorsSerializer(CollectionSyncSerializer):
    """Serializer for blog social connector accounts.

    Models handled:
        - SocialConnectorAccount: Social media platform connections for blog auto-sharing
    """

    category_key = 'social_connectors'
    natural_key_fields = ['provider_key', 'platform_account_id']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from blog.models import SocialConnectorAccount
        self.model_class = SocialConnectorAccount

    def get_count(self):
        from blog.models import SocialConnectorAccount
        return SocialConnectorAccount.objects.count()

    def export(self, credential_mode='redact'):
        from blog.models import SocialConnectorAccount

        items = []
        for account in SocialConnectorAccount.objects.all():
            data = {f: getattr(account, f) for f in SOCIAL_CONNECTOR_FIELDS}
            data['_source_pk'] = str(account.pk)
            data['_model'] = 'SocialConnectorAccount'

            if account.component:
                data['_component_slug'] = account.component.slug

            if credential_mode == 'decrypt':
                creds = decrypt_credentials_for_export(
                    'social_connectors', 'SocialConnectorAccount', account,
                )
                if creds:
                    data['_credentials'] = creds
            elif credential_mode == 'redact':
                creds = decrypt_credentials_for_export(
                    'social_connectors', 'SocialConnectorAccount', account,
                )
                if creds:
                    data['_credentials_redacted'] = redact_credentials(creds)

            items.append(data)

        return {
            'category': self.category_key,
            'sync_type': 'collection',
            'items': items,
            'total': len(items),
        }

    def import_data(self, data, dry_run=False, sync_mode='additive'):
        if dry_run:
            return self.generate_diff(data)

        items = data.get('items', [])
        synced = 0
        skipped = 0
        failed = 0
        errors = []

        site = Site.objects.get(pk=1)

        for item in items:
            try:
                with transaction.atomic():
                    self._import_account(item, site)
                    synced += 1
            except Exception as e:
                failed += 1
                errors.append(f"SocialConnector '{item.get('name', '?')}': {e}")

        result = {'synced': synced, 'skipped': skipped, 'failed': failed, 'errors': errors}

        if sync_mode == 'mirror':
            deleted = self._delete_absent(items)
            result['deleted'] = deleted

        return result

    def _import_account(self, item, site):
        from blog.models import SocialConnectorAccount

        existing = SocialConnectorAccount.objects.filter(
            provider_key=item['provider_key'],
            platform_account_id=item['platform_account_id'],
        ).first()
        obj = existing or SocialConnectorAccount(site=site)

        for f in SOCIAL_CONNECTOR_FIELDS:
            if f in item:
                setattr(obj, f, item[f])

        if '_credentials' in item and item['_credentials']:
            encrypted = encrypt_credentials_for_import(
                'social_connectors', 'SocialConnectorAccount', item['_credentials'],
            )
            if encrypted:
                obj.credentials = encrypted

        if '_component_slug' in item and item['_component_slug']:
            try:
                from component_updates.models import ComponentRegistry
                obj.component = ComponentRegistry.objects.get(slug=item['_component_slug'])
            except Exception:
                pass

        obj.save()

    def _delete_absent(self, remote_items):
        from blog.models import SocialConnectorAccount

        remote_keys = {
            (item['provider_key'], item['platform_account_id'])
            for item in remote_items
        }
        deleted = 0
        for obj in SocialConnectorAccount.objects.all():
            if (obj.provider_key, obj.platform_account_id) not in remote_keys:
                try:
                    obj.delete()
                    deleted += 1
                except Exception as e:
                    logger.warning(f"Cannot delete SocialConnector '{obj.name}': {e}")
        return deleted

    def generate_diff(self, remote_data):
        from blog.models import SocialConnectorAccount

        items = remote_data.get('items', [])
        changes = []

        for item in items:
            existing = SocialConnectorAccount.objects.filter(
                provider_key=item.get('provider_key'),
                platform_account_id=item.get('platform_account_id'),
            ).first()
            if existing:
                field_changes = self._compute_field_diff(existing, item, SOCIAL_CONNECTOR_FIELDS)
                if field_changes:
                    changes.append({
                        'type': 'modify', 'model': 'SocialConnectorAccount',
                        'name': item.get('name', '?'), 'changes': field_changes,
                    })
            else:
                changes.append({
                    'type': 'add', 'model': 'SocialConnectorAccount',
                    'name': item.get('name', '?'),
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
