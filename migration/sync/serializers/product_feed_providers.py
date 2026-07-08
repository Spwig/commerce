"""
Product Feed Providers Sync Serializer

Handles export/import of product feed provider accounts.
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

FEED_PROVIDER_FIELDS = [
    'name', 'is_active', 'is_primary', 'priority',
    'config', 'feed_url',
]


class ProductFeedProvidersSerializer(CollectionSyncSerializer):
    """Serializer for product feed provider accounts.

    Models handled:
        - FeedProviderAccount: Product feed provider configurations (Google Shopping, Meta, etc.)
    """

    category_key = 'product_feed_providers'
    natural_key_fields = ['name']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from product_feeds.models import FeedProviderAccount
        self.model_class = FeedProviderAccount

    def get_count(self):
        from product_feeds.models import FeedProviderAccount
        return FeedProviderAccount.objects.count()

    def export(self, credential_mode='redact'):
        from product_feeds.models import FeedProviderAccount

        items = []
        for account in FeedProviderAccount.objects.all():
            data = {f: getattr(account, f) for f in FEED_PROVIDER_FIELDS}
            data['_source_pk'] = account.pk
            data['_model'] = 'FeedProviderAccount'

            if account.component:
                data['_component_slug'] = account.component.slug
                data['_component_type'] = account.component.component_type

            if credential_mode == 'decrypt':
                creds = decrypt_credentials_for_export(
                    'product_feed_providers', 'FeedProviderAccount', account,
                )
                if creds:
                    data['_credentials'] = creds
            elif credential_mode == 'redact':
                creds = decrypt_credentials_for_export(
                    'product_feed_providers', 'FeedProviderAccount', account,
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
                errors.append(f"FeedProviderAccount '{item.get('name', '?')}': {e}")

        result = {'synced': synced, 'skipped': skipped, 'failed': failed, 'errors': errors}

        if sync_mode == 'mirror':
            deleted = self._delete_absent(items)
            result['deleted'] = deleted

        return result

    def _import_account(self, item, site):
        from product_feeds.models import FeedProviderAccount

        # Match by component_slug + name for uniqueness
        component_slug = item.get('_component_slug')
        existing = None
        if component_slug:
            from component_updates.models import ComponentRegistry
            component = ComponentRegistry.objects.filter(slug=component_slug).first()
            if component:
                existing = FeedProviderAccount.objects.filter(
                    component=component, name=item['name'],
                ).first()

        if not existing:
            existing = FeedProviderAccount.objects.filter(name=item['name']).first()

        obj = existing or FeedProviderAccount(site=site)

        for f in FEED_PROVIDER_FIELDS:
            if f in item:
                setattr(obj, f, item[f])

        if '_credentials' in item and item['_credentials']:
            encrypted = encrypt_credentials_for_import(
                'product_feed_providers', 'FeedProviderAccount', item['_credentials'],
            )
            if encrypted:
                obj.credentials = encrypted

        if component_slug and not existing:
            try:
                from component_updates.models import ComponentRegistry
                obj.component = ComponentRegistry.objects.get(slug=component_slug)
            except Exception:
                pass

        obj.save()

    def _delete_absent(self, remote_items):
        from product_feeds.models import FeedProviderAccount

        remote_names = {item['name'] for item in remote_items}
        deleted = 0
        for obj in FeedProviderAccount.objects.all():
            if obj.name not in remote_names:
                try:
                    obj.delete()
                    deleted += 1
                except Exception as e:
                    logger.warning(f"Cannot delete FeedProviderAccount '{obj.name}': {e}")
        return deleted

    def generate_diff(self, remote_data):
        from product_feeds.models import FeedProviderAccount

        items = remote_data.get('items', [])
        changes = []

        for item in items:
            existing = FeedProviderAccount.objects.filter(name=item.get('name')).first()
            if existing:
                field_changes = self._compute_field_diff(existing, item, FEED_PROVIDER_FIELDS)
                if field_changes:
                    changes.append({
                        'type': 'modify', 'model': 'FeedProviderAccount',
                        'name': item.get('name', '?'), 'changes': field_changes,
                    })
            else:
                changes.append({
                    'type': 'add', 'model': 'FeedProviderAccount',
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
