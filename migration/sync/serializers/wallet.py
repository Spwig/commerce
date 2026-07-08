"""
Wallet Sync Serializer

Handles export/import of store credit wallets:
- CustomerWallet (4 MoneyFields)
- WalletTransaction (2 MoneyFields, immutable ledger)
"""
import logging
from decimal import Decimal
from django.db import transaction

from .base import CollectionSyncSerializer

logger = logging.getLogger(__name__)

WALLET_FIELDS = ['is_active']
WALLET_MONEY_FIELDS = ['available_balance', 'pending_balance', 'lifetime_credited', 'lifetime_used']

TRANSACTION_FIELDS = [
    'transaction_type', 'status', 'source',
    'description', 'reference_id',
]
TRANSACTION_MONEY_FIELDS = ['amount', 'balance_after']


def _serialize_money(data, instance, field_name):
    val = getattr(instance, field_name, None)
    if val is not None:
        data[f'_{field_name}_amount'] = str(val.amount) if hasattr(val, 'amount') else str(val)
        data[f'_{field_name}_currency'] = str(val.currency) if hasattr(val, 'currency') else getattr(instance, f'{field_name}_currency', None)
    else:
        data[f'_{field_name}_amount'] = None
        data[f'_{field_name}_currency'] = None


def _deserialize_money(instance, item, field_name):
    amount = item.get(f'_{field_name}_amount')
    currency = item.get(f'_{field_name}_currency')
    if amount is not None:
        setattr(instance, field_name, Decimal(str(amount)))
    else:
        setattr(instance, field_name, None)
    if currency:
        setattr(instance, f'{field_name}_currency', currency)


class WalletSerializer(CollectionSyncSerializer):
    category_key = 'wallet'
    natural_key_fields = ['_user_email']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from wallet.models import CustomerWallet
        self.model_class = CustomerWallet

    def get_count(self):
        from wallet.models import CustomerWallet, WalletTransaction
        return CustomerWallet.objects.count() + WalletTransaction.objects.count()

    def export(self, credential_mode='redact'):
        from wallet.models import CustomerWallet

        items = []
        for wallet in CustomerWallet.objects.select_related('customer').prefetch_related(
            'transactions',
        ).all():
            data = {f: getattr(wallet, f) for f in WALLET_FIELDS}
            data['_source_pk'] = wallet.pk
            data['_model'] = 'CustomerWallet'
            data['_user_email'] = wallet.customer.email

            for mf in WALLET_MONEY_FIELDS:
                _serialize_money(data, wallet, mf)

            # Nested transactions (immutable ledger — full export)
            data['_transactions'] = []
            for tx in wallet.transactions.all().order_by('created_at'):
                tx_data = {f: getattr(tx, f) for f in TRANSACTION_FIELDS}
                for mf in TRANSACTION_MONEY_FIELDS:
                    _serialize_money(tx_data, tx, mf)
                if tx.created_at:
                    tx_data['_created_at'] = tx.created_at.isoformat()
                data['_transactions'].append(tx_data)

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
                    self._import_wallet(item)
                    synced += 1
            except Exception as e:
                failed += 1
                errors.append(f"Wallet '{item.get('_user_email', '?')}': {e}")

        return {'synced': synced, 'skipped': skipped, 'failed': failed, 'errors': errors}

    def _import_wallet(self, item):
        from wallet.models import CustomerWallet, WalletTransaction
        from django.contrib.auth import get_user_model
        from django.utils.dateparse import parse_datetime
        User = get_user_model()

        user = User.objects.filter(email=item['_user_email']).first()
        if not user:
            raise ValueError(f"User not found: {item['_user_email']}")

        existing = CustomerWallet.objects.filter(customer=user).first()
        wallet = existing or CustomerWallet(customer=user)

        for f in WALLET_FIELDS:
            if f in item:
                setattr(wallet, f, item[f])
        for mf in WALLET_MONEY_FIELDS:
            _deserialize_money(wallet, item, mf)
        wallet.save()

        # Import transactions (append-only: skip if already exist by timestamp)
        for tx_data in item.get('_transactions', []):
            created_at_str = tx_data.get('_created_at')
            created_at = parse_datetime(created_at_str) if created_at_str else None

            # Check for duplicate by timestamp + type
            if created_at:
                exists = WalletTransaction.objects.filter(
                    wallet=wallet,
                    transaction_type=tx_data.get('transaction_type'),
                    created_at=created_at,
                ).exists()
                if exists:
                    continue

            tx = WalletTransaction(wallet=wallet)
            for f in TRANSACTION_FIELDS:
                if f in tx_data:
                    setattr(tx, f, tx_data[f])
            for mf in TRANSACTION_MONEY_FIELDS:
                _deserialize_money(tx, tx_data, mf)
            tx.save()

    def generate_diff(self, remote_data):
        from wallet.models import CustomerWallet
        from django.contrib.auth import get_user_model
        User = get_user_model()

        items = remote_data.get('items', [])
        changes = []

        for item in items:
            user = User.objects.filter(email=item.get('_user_email')).first()
            if user:
                existing = CustomerWallet.objects.filter(customer=user).first()
                if existing:
                    changes.append({'type': 'modify', 'model': 'CustomerWallet',
                                    'name': item.get('_user_email'), 'changes': []})
                else:
                    changes.append({'type': 'add', 'model': 'CustomerWallet',
                                    'name': item.get('_user_email'), 'fields': {}})
            else:
                changes.append({'type': 'add', 'model': 'CustomerWallet',
                                'name': item.get('_user_email'), 'fields': {}})

        adds = sum(1 for c in changes if c['type'] == 'add')
        mods = sum(1 for c in changes if c['type'] == 'modify')
        parts = []
        if adds:
            parts.append(f'{adds} addition(s)')
        if mods:
            parts.append(f'{mods} modification(s)')

        return {'changes': changes, 'warnings': [], 'summary': ', '.join(parts) if parts else 'No changes'}

    def snapshot_current(self):
        return self.export(credential_mode='skip')

    def restore_snapshot(self, snapshot):
        try:
            result = self.import_data(snapshot, dry_run=False)
            return {'restored': result.get('synced', 0), 'errors': result.get('errors', [])}
        except Exception as e:
            return {'restored': 0, 'errors': [str(e)]}
