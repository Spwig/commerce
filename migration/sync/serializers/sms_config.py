"""
SMS Configuration Sync Serializer

Handles export/import of SMS-related models:
- SMSProviderAccount
- SMSTemplate

Includes encrypted credential handling.
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

SMS_ACCOUNT_FIELDS = [
    'provider_key', 'display_name', 'is_active',
    'is_default_sms', 'is_default_whatsapp',
    'connection_status',
]

SMS_TEMPLATE_FIELDS = [
    'template_type', 'name', 'message', 'is_active',
]


class SMSConfigSerializer(CollectionSyncSerializer):
    """Serializer for SMS provider accounts and templates.

    Models handled:
        - SMSProviderAccount: SMS provider connection settings and credentials
        - SMSTemplate: SMS message templates
    """

    category_key = 'sms_config'
    natural_key_fields = ['provider_key', 'display_name']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from sms_system.models import SMSProviderAccount
        self.model_class = SMSProviderAccount

    def get_count(self):
        from sms_system.models import SMSProviderAccount, SMSTemplate
        return SMSProviderAccount.objects.count() + SMSTemplate.objects.count()

    def export(self, credential_mode='redact'):
        from sms_system.models import SMSProviderAccount, SMSTemplate

        items = []

        for account in SMSProviderAccount.objects.all():
            data = {field: getattr(account, field) for field in SMS_ACCOUNT_FIELDS}
            data['_source_pk'] = account.pk
            data['_model'] = 'SMSProviderAccount'

            if credential_mode == 'decrypt':
                creds = decrypt_credentials_for_export('sms_config', 'SMSProviderAccount', account)
                if creds:
                    data['_credentials'] = creds
            elif credential_mode == 'redact':
                creds = decrypt_credentials_for_export('sms_config', 'SMSProviderAccount', account)
                if creds:
                    data['_credentials_redacted'] = redact_credentials(creds)

            if account.component:
                data['_component_slug'] = account.component.slug

            items.append(data)

        for template in SMSTemplate.objects.all():
            data = {field: getattr(template, field) for field in SMS_TEMPLATE_FIELDS}
            data['_source_pk'] = template.pk
            data['_model'] = 'SMSTemplate'
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

        try:
            with transaction.atomic():
                site = Site.objects.get(pk=1)

                for item in items:
                    model_type = item.get('_model')
                    try:
                        if model_type == 'SMSProviderAccount':
                            self._import_account(item, site)
                            synced += 1
                        elif model_type == 'SMSTemplate':
                            self._import_template(item)
                            synced += 1
                        else:
                            skipped += 1
                    except Exception as e:
                        failed += 1
                        errors.append(
                            f"{item.get('display_name') or item.get('name', 'Unknown')}: {e}"
                        )

        except Exception as e:
            logger.error(f"SMS config import failed: {e}")
            return {'synced': 0, 'skipped': 0, 'failed': 1, 'errors': [str(e)]}

        result = {'synced': synced, 'skipped': skipped, 'failed': failed, 'errors': errors}

        if sync_mode == 'mirror':
            deleted = self._delete_absent(items)
            result['deleted'] = deleted

        return result

    def _import_account(self, item, site):
        from sms_system.models import SMSProviderAccount

        existing = SMSProviderAccount.objects.filter(
            provider_key=item['provider_key'],
            display_name=item['display_name'],
        ).first()

        if existing:
            for field in SMS_ACCOUNT_FIELDS:
                if field in item:
                    setattr(existing, field, item[field])
            if '_credentials' in item and item['_credentials']:
                encrypted = encrypt_credentials_for_import(
                    'sms_config', 'SMSProviderAccount', item['_credentials']
                )
                if encrypted:
                    existing.credentials = encrypted
            existing.save()
        else:
            account = SMSProviderAccount(site=site)
            for field in SMS_ACCOUNT_FIELDS:
                if field in item:
                    setattr(account, field, item[field])
            if '_credentials' in item and item['_credentials']:
                encrypted = encrypt_credentials_for_import(
                    'sms_config', 'SMSProviderAccount', item['_credentials']
                )
                if encrypted:
                    account.credentials = encrypted
            if '_component_slug' in item:
                try:
                    from component_updates.models import ComponentRegistry
                    account.component = ComponentRegistry.objects.get(
                        slug=item['_component_slug']
                    )
                except Exception:
                    pass
            account.save()

    def _import_template(self, item):
        from sms_system.models import SMSTemplate

        existing = SMSTemplate.objects.filter(template_type=item['template_type']).first()

        if existing:
            for field in SMS_TEMPLATE_FIELDS:
                if field in item:
                    setattr(existing, field, item[field])
            existing.save()
        else:
            template = SMSTemplate()
            for field in SMS_TEMPLATE_FIELDS:
                if field in item:
                    setattr(template, field, item[field])
            template.save()

    def _delete_absent(self, remote_items):
        from sms_system.models import SMSProviderAccount, SMSTemplate

        remote_account_keys = set()
        remote_template_types = set()
        for item in remote_items:
            if item.get('_model') == 'SMSProviderAccount':
                remote_account_keys.add((item.get('provider_key'), item.get('display_name')))
            elif item.get('_model') == 'SMSTemplate':
                remote_template_types.add(item.get('template_type'))

        deleted = 0
        for account in SMSProviderAccount.objects.all():
            if (account.provider_key, account.display_name) not in remote_account_keys:
                account.delete()
                deleted += 1
        for template in SMSTemplate.objects.all():
            if template.template_type not in remote_template_types:
                template.delete()
                deleted += 1
        return deleted

    def generate_diff(self, remote_data):
        from sms_system.models import SMSProviderAccount, SMSTemplate

        items = remote_data.get('items', [])
        changes = []

        for item in items:
            model_type = item.get('_model')
            if model_type == 'SMSProviderAccount':
                existing = SMSProviderAccount.objects.filter(
                    provider_key=item.get('provider_key'),
                    display_name=item.get('display_name'),
                ).first()
                name = item.get('display_name', 'Unknown')
                if existing:
                    field_changes = self._compute_field_diff(existing, item, SMS_ACCOUNT_FIELDS)
                    if field_changes:
                        changes.append({
                            'type': 'modify', 'model': 'SMSProviderAccount',
                            'name': name, 'changes': field_changes,
                        })
                else:
                    changes.append({
                        'type': 'add', 'model': 'SMSProviderAccount',
                        'name': name,
                        'fields': {k: v for k, v in item.items() if not k.startswith('_')},
                    })
            elif model_type == 'SMSTemplate':
                existing = SMSTemplate.objects.filter(
                    template_type=item.get('template_type'),
                ).first()
                name = item.get('name', item.get('template_type', 'Unknown'))
                if existing:
                    field_changes = self._compute_field_diff(existing, item, SMS_TEMPLATE_FIELDS)
                    if field_changes:
                        changes.append({
                            'type': 'modify', 'model': 'SMSTemplate',
                            'name': name, 'changes': field_changes,
                        })
                else:
                    changes.append({
                        'type': 'add', 'model': 'SMSTemplate',
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
