"""
Languages Sync Serializer

Handles export/import of language and translation models:
- SiteLanguage (with UITranslationOverride inline)
- TranslationProvider
"""
import logging
from django.db import transaction

from .base import CollectionSyncSerializer

logger = logging.getLogger(__name__)

SITE_LANGUAGE_FIELDS = [
    'code', 'name', 'native_name', 'is_active', 'is_default',
    'm2m100_support', 'nllb_support', 'requires_nllb',
    'order', 'rtl', 'flag', 'date_format', 'time_format',
]

UI_OVERRIDE_FIELDS = [
    'overrides', 'meta_info',
]

TRANSLATION_PROVIDER_FIELDS = [
    'name', 'provider_type', 'api_endpoint',
    'language_code_mapping', 'max_chars_per_request',
    'rate_limit', 'timeout_seconds', 'is_active', 'is_default', 'priority',
]


class LanguagesSerializer(CollectionSyncSerializer):
    """Serializer for language configuration and translation overrides.

    Models handled:
        - SiteLanguage: Enabled languages and their display order
        - UITranslationOverride: Merchant customizations of admin UI strings (inline)
        - TranslationProvider: AI translation service provider settings
    """

    category_key = 'languages'
    natural_key_fields = ['code']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from translations.models import SiteLanguage
        self.model_class = SiteLanguage

    def get_count(self):
        from translations.models import SiteLanguage, UITranslationOverride, TranslationProvider
        return (SiteLanguage.objects.count() +
                UITranslationOverride.objects.count() +
                TranslationProvider.objects.count())

    def export(self, credential_mode='redact'):
        from translations.models import SiteLanguage, UITranslationOverride, TranslationProvider

        items = []

        for lang in SiteLanguage.objects.all():
            data = {field: getattr(lang, field) for field in SITE_LANGUAGE_FIELDS}
            data['_source_pk'] = lang.pk
            data['_model'] = 'SiteLanguage'

            # Include UI overrides inline
            try:
                override = lang.ui_overrides
                data['_ui_overrides'] = {
                    f: getattr(override, f) for f in UI_OVERRIDE_FIELDS
                }
            except UITranslationOverride.DoesNotExist:
                data['_ui_overrides'] = None

            items.append(data)

        for provider in TranslationProvider.objects.all():
            data = {field: getattr(provider, field) for field in TRANSLATION_PROVIDER_FIELDS}
            data['_source_pk'] = provider.pk
            data['_model'] = 'TranslationProvider'

            # Handle API credentials
            if credential_mode == 'decrypt':
                data['_api_key'] = provider.api_key or ''
                data['_api_secret'] = provider.api_secret or ''
            elif credential_mode == 'redact':
                if provider.api_key:
                    k = provider.api_key
                    data['_api_key_redacted'] = k[:2] + '***' + k[-2:] if len(k) > 4 else '***'
                if provider.api_secret:
                    s = provider.api_secret
                    data['_api_secret_redacted'] = s[:2] + '***' + s[-2:] if len(s) > 4 else '***'

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
                    if model_type == 'SiteLanguage':
                        self._import_language(item)
                        synced += 1
                    elif model_type == 'TranslationProvider':
                        self._import_provider(item)
                        synced += 1
                    else:
                        skipped += 1
            except Exception as e:
                failed += 1
                errors.append(f"{item.get('name') or item.get('code', 'Unknown')}: {e}")

        result = {'synced': synced, 'skipped': skipped, 'failed': failed, 'errors': errors}

        if sync_mode == 'mirror':
            deleted = self._delete_absent(items)
            result['deleted'] = deleted

        return result

    def _import_language(self, item):
        from translations.models import SiteLanguage, UITranslationOverride

        code = item['code']
        existing = SiteLanguage.objects.filter(code=code).first()

        if existing:
            for field in SITE_LANGUAGE_FIELDS:
                if field in item:
                    setattr(existing, field, item[field])
            existing.save()
            lang = existing
        else:
            lang = SiteLanguage()
            for field in SITE_LANGUAGE_FIELDS:
                if field in item:
                    setattr(lang, field, item[field])
            lang.save()

        # Handle UI overrides
        ui_data = item.get('_ui_overrides')
        if ui_data:
            override, _ = UITranslationOverride.objects.get_or_create(language=lang)
            for field in UI_OVERRIDE_FIELDS:
                if field in ui_data:
                    setattr(override, field, ui_data[field])
            override.save()

    def _import_provider(self, item):
        from translations.models import TranslationProvider

        existing = TranslationProvider.objects.filter(name=item['name']).first()

        if existing:
            for field in TRANSLATION_PROVIDER_FIELDS:
                if field in item:
                    setattr(existing, field, item[field])
            if '_api_key' in item:
                existing.api_key = item['_api_key']
            if '_api_secret' in item:
                existing.api_secret = item['_api_secret']
            existing.save()
        else:
            provider = TranslationProvider()
            for field in TRANSLATION_PROVIDER_FIELDS:
                if field in item:
                    setattr(provider, field, item[field])
            if '_api_key' in item:
                provider.api_key = item['_api_key']
            if '_api_secret' in item:
                provider.api_secret = item['_api_secret']
            provider.save()

    def _delete_absent(self, remote_items):
        from translations.models import SiteLanguage, TranslationProvider

        remote_codes = set()
        remote_providers = set()
        for item in remote_items:
            if item.get('_model') == 'SiteLanguage':
                remote_codes.add(item.get('code'))
            elif item.get('_model') == 'TranslationProvider':
                remote_providers.add(item.get('name'))

        deleted = 0
        for lang in SiteLanguage.objects.all():
            if lang.code not in remote_codes:
                lang.delete()
                deleted += 1
        for provider in TranslationProvider.objects.all():
            if provider.name not in remote_providers:
                provider.delete()
                deleted += 1
        return deleted

    def generate_diff(self, remote_data):
        from translations.models import SiteLanguage, TranslationProvider

        items = remote_data.get('items', [])
        changes = []

        for item in items:
            model_type = item.get('_model')
            if model_type == 'SiteLanguage':
                existing = SiteLanguage.objects.filter(code=item.get('code')).first()
                name = f"{item.get('name', '')} ({item.get('code', '')})"
                if existing:
                    field_changes = self._compute_field_diff(existing, item, SITE_LANGUAGE_FIELDS)
                    if field_changes:
                        changes.append({
                            'type': 'modify', 'model': 'SiteLanguage',
                            'name': name, 'changes': field_changes,
                        })
                else:
                    changes.append({
                        'type': 'add', 'model': 'SiteLanguage',
                        'name': name,
                        'fields': {k: v for k, v in item.items() if not k.startswith('_')},
                    })
            elif model_type == 'TranslationProvider':
                existing = TranslationProvider.objects.filter(name=item.get('name')).first()
                name = item.get('name', 'Unknown')
                if existing:
                    field_changes = self._compute_field_diff(
                        existing, item, TRANSLATION_PROVIDER_FIELDS
                    )
                    if field_changes:
                        changes.append({
                            'type': 'modify', 'model': 'TranslationProvider',
                            'name': name, 'changes': field_changes,
                        })
                else:
                    changes.append({
                        'type': 'add', 'model': 'TranslationProvider',
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
