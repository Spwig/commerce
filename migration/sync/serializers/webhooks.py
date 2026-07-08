"""
Webhooks & Integrations Sync Serializer

Handles export/import of webhook and OAuth models:
- WebhookEndpoint
- OAuthProviderSettings
"""
import logging
from django.db import transaction

from .base import CollectionSyncSerializer
from ..credential_handler import redact_credentials

logger = logging.getLogger(__name__)

WEBHOOK_FIELDS = [
    'name', 'url', 'is_active', 'events',
    'max_retries', 'timeout_seconds', 'description',
]

OAUTH_SETTINGS_FIELDS = [
    'provider', 'enabled', 'display_name', 'button_order',
    'custom_scopes', 'configuration_notes',
]


class WebhooksSerializer(CollectionSyncSerializer):
    """Serializer for webhook endpoints and OAuth provider settings.

    Models handled:
        - WebhookEndpoint: Webhook URL configurations and event subscriptions
        - OAuthProviderSettings: OAuth provider display settings
    """

    category_key = 'webhooks_integrations'
    natural_key_fields = ['url']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from webhooks.models import WebhookEndpoint
        self.model_class = WebhookEndpoint

    def get_count(self):
        from webhooks.models import WebhookEndpoint
        from accounts.models import OAuthProviderSettings
        return WebhookEndpoint.objects.count() + OAuthProviderSettings.objects.count()

    def export(self, credential_mode='redact'):
        from webhooks.models import WebhookEndpoint
        from accounts.models import OAuthProviderSettings

        items = []

        for endpoint in WebhookEndpoint.objects.all():
            data = {field: getattr(endpoint, field) for field in WEBHOOK_FIELDS}
            data['_source_pk'] = str(endpoint.pk)
            data['_model'] = 'WebhookEndpoint'

            if credential_mode == 'decrypt':
                data['_secret'] = endpoint.secret
            elif credential_mode == 'redact':
                data['_secret_redacted'] = redact_credentials({'secret': endpoint.secret})

            items.append(data)

        for oauth in OAuthProviderSettings.objects.all():
            data = {field: getattr(oauth, field) for field in OAUTH_SETTINGS_FIELDS}
            data['_source_pk'] = oauth.pk
            data['_model'] = 'OAuthProviderSettings'
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
            model_type = item.get('_model')
            try:
                with transaction.atomic():
                    if model_type == 'WebhookEndpoint':
                        self._import_webhook(item)
                        synced += 1
                    elif model_type == 'OAuthProviderSettings':
                        self._import_oauth(item)
                        synced += 1
                    else:
                        skipped += 1
            except Exception as e:
                failed += 1
                errors.append(
                    f"{item.get('name') or item.get('provider', 'Unknown')}: {e}"
                )

        result = {'synced': synced, 'skipped': skipped, 'failed': failed, 'errors': errors}

        if sync_mode == 'mirror':
            deleted = self._delete_absent(items)
            result['deleted'] = deleted

        return result

    def _import_webhook(self, item):
        from webhooks.models import WebhookEndpoint

        existing = WebhookEndpoint.objects.filter(url=item['url']).first()

        if existing:
            for field in WEBHOOK_FIELDS:
                if field in item:
                    setattr(existing, field, item[field])
            if '_secret' in item:
                existing.secret = item['_secret']
            existing.save()
        else:
            endpoint = WebhookEndpoint()
            for field in WEBHOOK_FIELDS:
                if field in item:
                    setattr(endpoint, field, item[field])
            if '_secret' in item:
                endpoint.secret = item['_secret']
            endpoint.save()

    def _import_oauth(self, item):
        from accounts.models import OAuthProviderSettings

        existing = OAuthProviderSettings.objects.filter(provider=item['provider']).first()

        if existing:
            for field in OAUTH_SETTINGS_FIELDS:
                if field in item:
                    setattr(existing, field, item[field])
            existing.save()
        else:
            oauth = OAuthProviderSettings()
            for field in OAUTH_SETTINGS_FIELDS:
                if field in item:
                    setattr(oauth, field, item[field])
            oauth.save()

    def _delete_absent(self, remote_items):
        from webhooks.models import WebhookEndpoint
        from accounts.models import OAuthProviderSettings

        remote_urls = set()
        remote_providers = set()
        for item in remote_items:
            if item.get('_model') == 'WebhookEndpoint':
                remote_urls.add(item.get('url'))
            elif item.get('_model') == 'OAuthProviderSettings':
                remote_providers.add(item.get('provider'))

        deleted = 0
        for endpoint in WebhookEndpoint.objects.all():
            if endpoint.url not in remote_urls:
                endpoint.delete()
                deleted += 1
        for oauth in OAuthProviderSettings.objects.all():
            if oauth.provider not in remote_providers:
                oauth.delete()
                deleted += 1
        return deleted

    def generate_diff(self, remote_data):
        from webhooks.models import WebhookEndpoint
        from accounts.models import OAuthProviderSettings

        items = remote_data.get('items', [])
        changes = []

        for item in items:
            model_type = item.get('_model')
            if model_type == 'WebhookEndpoint':
                existing = WebhookEndpoint.objects.filter(url=item.get('url')).first()
                name = item.get('name', 'Unknown')
                if existing:
                    field_changes = self._compute_field_diff(existing, item, WEBHOOK_FIELDS)
                    if field_changes:
                        changes.append({
                            'type': 'modify', 'model': 'WebhookEndpoint',
                            'name': name, 'changes': field_changes,
                        })
                else:
                    changes.append({
                        'type': 'add', 'model': 'WebhookEndpoint',
                        'name': name,
                        'fields': {k: v for k, v in item.items() if not k.startswith('_')},
                    })
            elif model_type == 'OAuthProviderSettings':
                existing = OAuthProviderSettings.objects.filter(
                    provider=item.get('provider')
                ).first()
                name = item.get('display_name', item.get('provider', 'Unknown'))
                if existing:
                    field_changes = self._compute_field_diff(
                        existing, item, OAUTH_SETTINGS_FIELDS
                    )
                    if field_changes:
                        changes.append({
                            'type': 'modify', 'model': 'OAuthProviderSettings',
                            'name': name, 'changes': field_changes,
                        })
                else:
                    changes.append({
                        'type': 'add', 'model': 'OAuthProviderSettings',
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
