"""
Gift Cards & Voucher Usage Sync Serializer

Handles export/import of financial gift card data:
- GiftCard (with MoneyFields, nested GiftCardTransaction)
- VoucherUsage
- AppliedVoucher
"""
import logging
from decimal import Decimal
from django.db import transaction

from .base import CollectionSyncSerializer

logger = logging.getLogger(__name__)

GIFT_CARD_FIELDS = [
    'code', 'recipient_email', 'recipient_name', 'sender_name',
    'message', 'translations', 'is_active',
]
GIFT_CARD_MONEY_FIELDS = ['initial_value', 'current_balance']

GC_TRANSACTION_FIELDS = ['transaction_type', 'notes']
GC_TRANSACTION_MONEY_FIELDS = ['amount', 'balance_after']

VOUCHER_USAGE_FIELDS = []  # Most fields are FK refs
VOUCHER_USAGE_MONEY_FIELDS = ['discount_amount', 'cart_total']

APPLIED_VOUCHER_MONEY_FIELDS = ['discount_amount']


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
    if currency:
        setattr(instance, f'{field_name}_currency', currency)


class GiftCardsSerializer(CollectionSyncSerializer):
    category_key = 'gift_cards'
    natural_key_fields = ['code']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from catalog.models import GiftCard
        self.model_class = GiftCard

    def get_count(self):
        from catalog.models import GiftCard, GiftCardTransaction
        from vouchers.models import VoucherUsage, AppliedVoucher
        return (
            GiftCard.objects.count() + GiftCardTransaction.objects.count()
            + VoucherUsage.objects.count() + AppliedVoucher.objects.count()
        )

    def export(self, credential_mode='redact'):
        from catalog.models import GiftCard, GiftCardTransaction
        from vouchers.models import VoucherUsage, AppliedVoucher

        items = []

        # Gift Cards with nested transactions
        for gc in GiftCard.objects.select_related('product', 'order_item').prefetch_related(
            'transactions',
        ).all():
            data = {f: getattr(gc, f) for f in GIFT_CARD_FIELDS}
            data['_source_pk'] = gc.pk
            data['_model'] = 'GiftCard'
            data['_product_sku'] = gc.product.sku if gc.product else None

            for mf in GIFT_CARD_MONEY_FIELDS:
                _serialize_money(data, gc, mf)

            if gc.expires_at:
                data['_expires_at'] = gc.expires_at.isoformat()
            if gc.created_at:
                data['_created_at'] = gc.created_at.isoformat()

            # Nested transactions (immutable ledger)
            data['_transactions'] = []
            for tx in gc.transactions.all().order_by('created_at'):
                tx_data = {f: getattr(tx, f) for f in GC_TRANSACTION_FIELDS}
                for mf in GC_TRANSACTION_MONEY_FIELDS:
                    _serialize_money(tx_data, tx, mf)
                if tx.order:
                    tx_data['_order_number'] = tx.order.order_number
                if tx.created_at:
                    tx_data['_created_at'] = tx.created_at.isoformat()
                data['_transactions'].append(tx_data)

            items.append(data)

        # VoucherUsage records
        for vu in VoucherUsage.objects.select_related('voucher', 'user', 'order').all():
            data = {'_model': 'VoucherUsage', '_source_pk': vu.pk}
            data['_voucher_code'] = vu.voucher.code if vu.voucher else None
            data['_user_email'] = vu.user.email if vu.user else None
            data['_order_number'] = vu.order.order_number if vu.order else None
            for mf in VOUCHER_USAGE_MONEY_FIELDS:
                _serialize_money(data, vu, mf)
            if vu.used_at:
                data['_used_at'] = vu.used_at.isoformat()
            items.append(data)

        # AppliedVoucher records
        for av in AppliedVoucher.objects.select_related('voucher', 'order').all():
            data = {'_model': 'AppliedVoucher', '_source_pk': av.pk}
            data['_voucher_code'] = av.voucher.code if av.voucher else None
            data['_order_number'] = av.order.order_number if av.order else None
            for mf in APPLIED_VOUCHER_MONEY_FIELDS:
                _serialize_money(data, av, mf)
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

        # Import in order: GiftCards first, then usage records
        order_map = {'GiftCard': 0, 'VoucherUsage': 1, 'AppliedVoucher': 2}
        sorted_items = sorted(items, key=lambda x: order_map.get(x.get('_model'), 99))

        for item in sorted_items:
            model_type = item.get('_model')
            try:
                with transaction.atomic():
                    if model_type == 'GiftCard':
                        self._import_gift_card(item)
                    elif model_type == 'VoucherUsage':
                        self._import_voucher_usage(item)
                    elif model_type == 'AppliedVoucher':
                        self._import_applied_voucher(item)
                    else:
                        skipped += 1
                        continue
                    synced += 1
            except Exception as e:
                failed += 1
                errors.append(f"{model_type}: {e}")

        return {'synced': synced, 'skipped': skipped, 'failed': failed, 'errors': errors}

    def _import_gift_card(self, item):
        from catalog.models import GiftCard, GiftCardTransaction, Product
        from orders.models import Order
        from django.utils.dateparse import parse_datetime

        existing = GiftCard.objects.filter(code=item['code']).first()
        gc = existing or GiftCard()

        for f in GIFT_CARD_FIELDS:
            if f in item:
                setattr(gc, f, item[f])

        for mf in GIFT_CARD_MONEY_FIELDS:
            _deserialize_money(gc, item, mf)

        product_sku = item.get('_product_sku')
        if product_sku:
            gc.product = Product.objects.filter(sku=product_sku).first()

        expires = item.get('_expires_at')
        if expires:
            parsed = parse_datetime(expires)
            if parsed:
                gc.expires_at = parsed

        gc.save()

        # Import transactions (append-only ledger)
        for tx_data in item.get('_transactions', []):
            created_str = tx_data.get('_created_at')
            created_at = parse_datetime(created_str) if created_str else None

            if created_at:
                exists = GiftCardTransaction.objects.filter(
                    gift_card=gc,
                    transaction_type=tx_data.get('transaction_type'),
                    created_at=created_at,
                ).exists()
                if exists:
                    continue

            tx = GiftCardTransaction(gift_card=gc)
            for f in GC_TRANSACTION_FIELDS:
                if f in tx_data:
                    setattr(tx, f, tx_data[f])
            for mf in GC_TRANSACTION_MONEY_FIELDS:
                _deserialize_money(tx, tx_data, mf)

            order_num = tx_data.get('_order_number')
            if order_num:
                tx.order = Order.objects.filter(order_number=order_num).first()

            tx.save()

    def _import_voucher_usage(self, item):
        from vouchers.models import VoucherCode, VoucherUsage
        from orders.models import Order
        from django.contrib.auth import get_user_model
        from django.utils.dateparse import parse_datetime
        User = get_user_model()

        voucher = VoucherCode.objects.filter(code=item.get('_voucher_code')).first()
        if not voucher:
            return

        vu = VoucherUsage(voucher=voucher)
        user_email = item.get('_user_email')
        if user_email:
            vu.user = User.objects.filter(email=user_email).first()
        order_num = item.get('_order_number')
        if order_num:
            vu.order = Order.objects.filter(order_number=order_num).first()

        for mf in VOUCHER_USAGE_MONEY_FIELDS:
            _deserialize_money(vu, item, mf)

        used_at = item.get('_used_at')
        if used_at:
            parsed = parse_datetime(used_at)
            if parsed:
                vu.used_at = parsed

        vu.save()

    def _import_applied_voucher(self, item):
        from vouchers.models import VoucherCode, AppliedVoucher
        from orders.models import Order

        voucher = VoucherCode.objects.filter(code=item.get('_voucher_code')).first()
        if not voucher:
            return

        av = AppliedVoucher(voucher=voucher)
        order_num = item.get('_order_number')
        if order_num:
            av.order = Order.objects.filter(order_number=order_num).first()

        for mf in APPLIED_VOUCHER_MONEY_FIELDS:
            _deserialize_money(av, item, mf)

        av.save()

    def generate_diff(self, remote_data):
        items = remote_data.get('items', [])
        gc_count = sum(1 for i in items if i.get('_model') == 'GiftCard')
        vu_count = sum(1 for i in items if i.get('_model') == 'VoucherUsage')
        av_count = sum(1 for i in items if i.get('_model') == 'AppliedVoucher')

        parts = []
        if gc_count:
            parts.append(f'{gc_count} gift card(s)')
        if vu_count:
            parts.append(f'{vu_count} voucher usage(s)')
        if av_count:
            parts.append(f'{av_count} applied voucher(s)')

        return {
            'changes': [],
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
