"""
Tax & Currency Sync Serializer

Handles export/import of currency and exchange rate models:
- SupportedCurrency
- ExchangeRateProviderAccount
- ManualExchangeRate

Includes encrypted credential handling for exchange rate providers.
"""
import logging
from decimal import Decimal
from django.db import transaction
from django.contrib.sites.models import Site

from .base import CollectionSyncSerializer
from ..credential_handler import (
    decrypt_credentials_for_export, encrypt_credentials_for_import,
    redact_credentials,
)

logger = logging.getLogger(__name__)

CURRENCY_FIELDS = [
    'code', 'is_active', 'order', 'show_flag',
    'show_symbol', 'custom_symbol',
]

EXCHANGE_PROVIDER_FIELDS = [
    'name', 'is_active', 'is_primary', 'priority', 'settings',
]

MANUAL_RATE_FIELDS = [
    'base_currency', 'target_currency', 'rate',
    'is_active', 'exclude_from_auto_sync', 'notes',
]


class TaxCurrencySerializer(CollectionSyncSerializer):
    """Serializer for currency configuration and exchange rate providers.

    Models handled:
        - SupportedCurrency: Enabled currencies and display settings
        - ExchangeRateProviderAccount: Exchange rate provider credentials
        - ManualExchangeRate: Manually set exchange rates
    """

    category_key = 'tax_currency'
    natural_key_fields = ['code']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from core.supported_currency_model import SupportedCurrency
        self.model_class = SupportedCurrency

    def get_count(self):
        from core.supported_currency_model import SupportedCurrency
        from exchange_rates.models import ExchangeRateProviderAccount, ManualExchangeRate
        return (SupportedCurrency.objects.count() +
                ExchangeRateProviderAccount.objects.count() +
                ManualExchangeRate.objects.count())

    def export(self, credential_mode='redact'):
        from core.supported_currency_model import SupportedCurrency
        from exchange_rates.models import ExchangeRateProviderAccount, ManualExchangeRate

        items = []

        for currency in SupportedCurrency.objects.all():
            data = {field: getattr(currency, field) for field in CURRENCY_FIELDS}
            data['_source_pk'] = currency.pk
            data['_model'] = 'SupportedCurrency'
            items.append(data)

        for provider in ExchangeRateProviderAccount.objects.all():
            data = {field: getattr(provider, field) for field in EXCHANGE_PROVIDER_FIELDS}
            data['_source_pk'] = provider.pk
            data['_model'] = 'ExchangeRateProviderAccount'

            if credential_mode == 'decrypt':
                creds = decrypt_credentials_for_export(
                    'tax_currency', 'ExchangeRateProviderAccount', provider
                )
                if creds:
                    data['_credentials'] = creds
            elif credential_mode == 'redact':
                creds = decrypt_credentials_for_export(
                    'tax_currency', 'ExchangeRateProviderAccount', provider
                )
                if creds:
                    data['_credentials_redacted'] = redact_credentials(creds)

            if provider.component:
                data['_component_slug'] = provider.component.slug

            items.append(data)

        for rate in ManualExchangeRate.objects.all():
            data = {field: getattr(rate, field) for field in MANUAL_RATE_FIELDS}
            data['rate'] = str(data['rate'])
            data['_source_pk'] = rate.pk
            data['_model'] = 'ManualExchangeRate'
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
            model_type = item.get('_model')
            try:
                with transaction.atomic():
                    if model_type == 'SupportedCurrency':
                        self._import_currency(item)
                        synced += 1
                    elif model_type == 'ExchangeRateProviderAccount':
                        self._import_provider(item, site)
                        synced += 1
                    elif model_type == 'ManualExchangeRate':
                        self._import_manual_rate(item, site)
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

    def _import_currency(self, item):
        from core.supported_currency_model import SupportedCurrency

        existing = SupportedCurrency.objects.filter(code=item['code']).first()

        if existing:
            for field in CURRENCY_FIELDS:
                if field in item:
                    setattr(existing, field, item[field])
            existing.save()
        else:
            currency = SupportedCurrency()
            for field in CURRENCY_FIELDS:
                if field in item:
                    setattr(currency, field, item[field])
            currency.save()

    def _import_provider(self, item, site):
        from exchange_rates.models import ExchangeRateProviderAccount

        existing = ExchangeRateProviderAccount.objects.filter(
            name=item['name'], site=site,
        ).first()

        if existing:
            for field in EXCHANGE_PROVIDER_FIELDS:
                if field in item:
                    setattr(existing, field, item[field])
            if '_credentials' in item and item['_credentials']:
                encrypted = encrypt_credentials_for_import(
                    'tax_currency', 'ExchangeRateProviderAccount', item['_credentials']
                )
                if encrypted:
                    existing.credentials = encrypted
            existing.save()
        else:
            provider = ExchangeRateProviderAccount(site=site)
            for field in EXCHANGE_PROVIDER_FIELDS:
                if field in item:
                    setattr(provider, field, item[field])
            if '_credentials' in item and item['_credentials']:
                encrypted = encrypt_credentials_for_import(
                    'tax_currency', 'ExchangeRateProviderAccount', item['_credentials']
                )
                if encrypted:
                    provider.credentials = encrypted
            if '_component_slug' in item:
                try:
                    from component_updates.models import ComponentRegistry
                    provider.component = ComponentRegistry.objects.get(
                        slug=item['_component_slug']
                    )
                except Exception:
                    pass
            provider.save()

    def _import_manual_rate(self, item, site):
        from exchange_rates.models import ManualExchangeRate

        existing = ManualExchangeRate.objects.filter(
            site=site,
            base_currency=item['base_currency'],
            target_currency=item['target_currency'],
        ).first()

        if existing:
            for field in MANUAL_RATE_FIELDS:
                if field in item:
                    value = item[field]
                    if field == 'rate':
                        value = Decimal(str(value))
                    setattr(existing, field, value)
            existing.save()
        else:
            rate = ManualExchangeRate(site=site)
            for field in MANUAL_RATE_FIELDS:
                if field in item:
                    value = item[field]
                    if field == 'rate':
                        value = Decimal(str(value))
                    setattr(rate, field, value)
            rate.save()

    def _delete_absent(self, remote_items):
        from core.supported_currency_model import SupportedCurrency
        from exchange_rates.models import ExchangeRateProviderAccount, ManualExchangeRate

        remote_codes = set()
        remote_providers = set()
        remote_rates = set()
        for item in remote_items:
            if item.get('_model') == 'SupportedCurrency':
                remote_codes.add(item.get('code'))
            elif item.get('_model') == 'ExchangeRateProviderAccount':
                remote_providers.add(item.get('name'))
            elif item.get('_model') == 'ManualExchangeRate':
                remote_rates.add((item.get('base_currency'), item.get('target_currency')))

        deleted = 0
        for currency in SupportedCurrency.objects.all():
            if currency.code not in remote_codes:
                currency.delete()
                deleted += 1
        for provider in ExchangeRateProviderAccount.objects.all():
            if provider.name not in remote_providers:
                provider.delete()
                deleted += 1
        for rate in ManualExchangeRate.objects.all():
            if (rate.base_currency, rate.target_currency) not in remote_rates:
                rate.delete()
                deleted += 1
        return deleted

    def generate_diff(self, remote_data):
        from core.supported_currency_model import SupportedCurrency
        from exchange_rates.models import ExchangeRateProviderAccount, ManualExchangeRate

        items = remote_data.get('items', [])
        changes = []

        for item in items:
            model_type = item.get('_model')
            if model_type == 'SupportedCurrency':
                existing = SupportedCurrency.objects.filter(code=item.get('code')).first()
                name = item.get('code', 'Unknown')
                if existing:
                    field_changes = self._compute_field_diff(existing, item, CURRENCY_FIELDS)
                    if field_changes:
                        changes.append({
                            'type': 'modify', 'model': 'SupportedCurrency',
                            'name': name, 'changes': field_changes,
                        })
                else:
                    changes.append({
                        'type': 'add', 'model': 'SupportedCurrency',
                        'name': name,
                        'fields': {k: v for k, v in item.items() if not k.startswith('_')},
                    })
            elif model_type == 'ExchangeRateProviderAccount':
                existing = ExchangeRateProviderAccount.objects.filter(
                    name=item.get('name')
                ).first()
                name = item.get('name', 'Unknown')
                if existing:
                    field_changes = self._compute_field_diff(
                        existing, item, EXCHANGE_PROVIDER_FIELDS
                    )
                    if field_changes:
                        changes.append({
                            'type': 'modify', 'model': 'ExchangeRateProviderAccount',
                            'name': name, 'changes': field_changes,
                        })
                else:
                    changes.append({
                        'type': 'add', 'model': 'ExchangeRateProviderAccount',
                        'name': name,
                        'fields': {k: v for k, v in item.items() if not k.startswith('_')},
                    })
            elif model_type == 'ManualExchangeRate':
                existing = ManualExchangeRate.objects.filter(
                    base_currency=item.get('base_currency'),
                    target_currency=item.get('target_currency'),
                ).first()
                name = f"{item.get('base_currency')}/{item.get('target_currency')}"
                if existing:
                    field_changes = self._compute_field_diff(existing, item, MANUAL_RATE_FIELDS)
                    if field_changes:
                        changes.append({
                            'type': 'modify', 'model': 'ManualExchangeRate',
                            'name': name, 'changes': field_changes,
                        })
                else:
                    changes.append({
                        'type': 'add', 'model': 'ManualExchangeRate',
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
