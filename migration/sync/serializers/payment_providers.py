"""
Payment Providers Sync Serializer

Handles export/import of payment provider models:
- PaymentProviderAccount

Includes encrypted credential handling and production warnings.
"""
import logging
from django.db import transaction

from .base import CollectionSyncSerializer
from ..credential_handler import (
    decrypt_credentials_for_export, encrypt_credentials_for_import,
    redact_credentials,
)

logger = logging.getLogger(__name__)

PAYMENT_PROVIDER_FIELDS = [
    'display_name', 'is_active', 'is_default',
    'checkout_mode', 'sort_order', 'settings',
    'connection_status',
    'available_payment_methods', 'enabled_payment_methods',
]


class PaymentProviderSerializer(CollectionSyncSerializer):
    """Serializer for payment provider accounts.

    Models handled:
        - PaymentProviderAccount: Payment gateway configurations and credentials
    """

    category_key = 'payment_providers'
    natural_key_fields = ['_component_slug', 'display_name']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from payment_providers.models import PaymentProviderAccount
        self.model_class = PaymentProviderAccount

    def get_count(self):
        from payment_providers.models import PaymentProviderAccount
        return PaymentProviderAccount.objects.count()

    def export(self, credential_mode='redact'):
        from payment_providers.models import PaymentProviderAccount

        items = []
        for account in PaymentProviderAccount.objects.select_related('component').all():
            data = {field: getattr(account, field) for field in PAYMENT_PROVIDER_FIELDS}
            data['_source_pk'] = str(account.pk)
            data['_model'] = 'PaymentProviderAccount'

            if account.component:
                data['_component_slug'] = account.component.slug

            if credential_mode == 'decrypt':
                creds = decrypt_credentials_for_export(
                    'payment_providers', 'PaymentProviderAccount', account
                )
                if creds:
                    data['_credentials'] = creds
            elif credential_mode == 'redact':
                creds = decrypt_credentials_for_export(
                    'payment_providers', 'PaymentProviderAccount', account
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

        for item in items:
            try:
                with transaction.atomic():
                    self._import_account(item)
                    synced += 1
            except Exception as e:
                failed += 1
                errors.append(f"{item.get('display_name', 'Unknown')}: {e}")

        result = {'synced': synced, 'skipped': skipped, 'failed': failed, 'errors': errors}

        if sync_mode == 'mirror':
            deleted = self._delete_absent(items)
            result['deleted'] = deleted

        return result

    def _import_account(self, item):
        from payment_providers.models import PaymentProviderAccount
        from django.contrib.auth import get_user_model
        User = get_user_model()

        component_slug = item.get('_component_slug')
        component = None
        if component_slug:
            try:
                from component_updates.models import ComponentRegistry
                component = ComponentRegistry.objects.get(slug=component_slug)
            except Exception:
                logger.warning(f"Component not found: {component_slug}")

        # Match by component + display_name
        lookup = {'display_name': item['display_name']}
        if component:
            lookup['component'] = component

        existing = PaymentProviderAccount.objects.filter(**lookup).first()

        if existing:
            for field in PAYMENT_PROVIDER_FIELDS:
                if field in item:
                    setattr(existing, field, item[field])
            if '_credentials' in item and item['_credentials']:
                encrypted = encrypt_credentials_for_import(
                    'payment_providers', 'PaymentProviderAccount', item['_credentials']
                )
                if encrypted:
                    existing.credentials_encrypted = encrypted
            existing.save()
        else:
            admin_user = User.objects.filter(is_superuser=True).first()
            if not admin_user:
                raise ValueError("No admin user available for payment provider account")

            account = PaymentProviderAccount(user=admin_user)
            if component:
                account.component = component
            for field in PAYMENT_PROVIDER_FIELDS:
                if field in item:
                    setattr(account, field, item[field])
            if '_credentials' in item and item['_credentials']:
                encrypted = encrypt_credentials_for_import(
                    'payment_providers', 'PaymentProviderAccount', item['_credentials']
                )
                if encrypted:
                    account.credentials_encrypted = encrypted
            account.save()

    def _delete_absent(self, remote_items):
        from payment_providers.models import PaymentProviderAccount

        remote_names = {item.get('display_name') for item in remote_items}
        deleted = 0
        for account in PaymentProviderAccount.objects.all():
            if account.display_name not in remote_names:
                account.delete()
                deleted += 1
        return deleted

    def generate_diff(self, remote_data):
        from payment_providers.models import PaymentProviderAccount

        items = remote_data.get('items', [])
        changes = []

        for item in items:
            component_slug = item.get('_component_slug')
            lookup = {'display_name': item.get('display_name')}
            if component_slug:
                try:
                    from component_updates.models import ComponentRegistry
                    component = ComponentRegistry.objects.get(slug=component_slug)
                    lookup['component'] = component
                except Exception:
                    pass

            existing = PaymentProviderAccount.objects.filter(**lookup).first()
            name = item.get('display_name', 'Unknown')

            if existing:
                field_changes = self._compute_field_diff(
                    existing, item, PAYMENT_PROVIDER_FIELDS
                )
                if field_changes:
                    changes.append({
                        'type': 'modify', 'model': 'PaymentProviderAccount',
                        'name': name, 'changes': field_changes,
                    })
            else:
                changes.append({
                    'type': 'add', 'model': 'PaymentProviderAccount',
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
