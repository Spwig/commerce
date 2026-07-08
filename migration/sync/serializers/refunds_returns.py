"""
Refunds, Returns & Order Notes Sync Serializer

Handles export/import of post-order records:
- Refund (with MoneyFields)
- ReturnRequest (with MoneyField)
- OrderNote
"""
import logging
from decimal import Decimal
from django.db import transaction

from .base import CollectionSyncSerializer

logger = logging.getLogger(__name__)

REFUND_FIELDS = [
    'refund_type', 'reason', 'status',
    'refund_method', 'refund_method_display',
    'total_amount_base', 'shipping_refund_amount_base', 'tax_refund_amount_base',
    'items_json', 'customer_notes', 'staff_notes',
]

REFUND_MONEY_FIELDS = ['total_amount', 'shipping_refund_amount', 'tax_refund_amount']

RETURN_FIELDS = [
    'reason', 'status', 'items_json',
    'return_label_generated', 'return_tracking_number', 'return_label_url',
    'customer_notes', 'merchant_notes', 'rejection_reason',
    'inspection_notes', 'items_condition',
]

RETURN_MONEY_FIELDS = ['restocking_fee']

ORDER_NOTE_FIELDS = [
    'note', 'is_customer_note', 'is_read',
]


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


class RefundsReturnsSerializer(CollectionSyncSerializer):
    category_key = 'refunds_returns'
    natural_key_fields = ['_order_number']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from orders.models import Refund
        self.model_class = Refund

    def get_count(self):
        from orders.models import Refund, ReturnRequest, OrderNote
        return Refund.objects.count() + ReturnRequest.objects.count() + OrderNote.objects.count()

    def export(self, credential_mode='redact'):
        from orders.models import Refund, ReturnRequest, OrderNote

        items = []

        for refund in Refund.objects.select_related('order', 'processed_by').all():
            data = {f: getattr(refund, f) for f in REFUND_FIELDS}
            data['_source_pk'] = refund.pk
            data['_model'] = 'Refund'
            data['_order_number'] = refund.order.order_number
            data['_processed_by_email'] = refund.processed_by.email if refund.processed_by else None

            for mf in REFUND_MONEY_FIELDS:
                _serialize_money(data, refund, mf)
            for df in ['total_amount_base', 'shipping_refund_amount_base', 'tax_refund_amount_base']:
                if data.get(df) is not None:
                    data[df] = str(data[df])

            if refund.created_at:
                data['_created_at'] = refund.created_at.isoformat()

            items.append(data)

        for ret in ReturnRequest.objects.select_related('order', 'user', 'refund').all():
            data = {f: getattr(ret, f) for f in RETURN_FIELDS}
            data['_source_pk'] = ret.pk
            data['_model'] = 'ReturnRequest'
            data['_order_number'] = ret.order.order_number
            data['_user_email'] = ret.user.email

            for mf in RETURN_MONEY_FIELDS:
                _serialize_money(data, ret, mf)

            if ret.requested_at:
                data['_requested_at'] = ret.requested_at.isoformat()

            items.append(data)

        for note in OrderNote.objects.select_related('order', 'author').all():
            data = {f: getattr(note, f) for f in ORDER_NOTE_FIELDS}
            data['_source_pk'] = note.pk
            data['_model'] = 'OrderNote'
            data['_order_number'] = note.order.order_number
            data['_author_email'] = note.author.email if note.author else None
            if note.created_at:
                data['_created_at'] = note.created_at.isoformat()
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
                    if model_type == 'Refund':
                        self._import_refund(item)
                    elif model_type == 'ReturnRequest':
                        self._import_return(item)
                    elif model_type == 'OrderNote':
                        self._import_note(item)
                    else:
                        skipped += 1
                        continue
                    synced += 1
            except Exception as e:
                failed += 1
                errors.append(f"{model_type} for order {item.get('_order_number', '?')}: {e}")

        return {'synced': synced, 'skipped': skipped, 'failed': failed, 'errors': errors}

    def _import_refund(self, item):
        from orders.models import Order, Refund
        from django.contrib.auth import get_user_model
        from django.utils.dateparse import parse_datetime
        User = get_user_model()

        order = Order.objects.filter(order_number=item['_order_number']).first()
        if not order:
            raise ValueError(f"Order not found: {item['_order_number']}")

        refund = Refund(order=order)
        for f in REFUND_FIELDS:
            if f in item:
                val = item[f]
                if f.endswith('_base') and val is not None:
                    val = Decimal(str(val))
                setattr(refund, f, val)

        for mf in REFUND_MONEY_FIELDS:
            _deserialize_money(refund, item, mf)

        email = item.get('_processed_by_email')
        if email:
            refund.processed_by = User.objects.filter(email=email).first()

        refund.save()

    def _import_return(self, item):
        from orders.models import Order, ReturnRequest
        from django.contrib.auth import get_user_model
        User = get_user_model()

        order = Order.objects.filter(order_number=item['_order_number']).first()
        if not order:
            raise ValueError(f"Order not found: {item['_order_number']}")

        user = User.objects.filter(email=item['_user_email']).first()
        if not user:
            raise ValueError(f"User not found: {item['_user_email']}")

        ret = ReturnRequest(order=order, user=user)
        for f in RETURN_FIELDS:
            if f in item:
                setattr(ret, f, item[f])

        for mf in RETURN_MONEY_FIELDS:
            _deserialize_money(ret, item, mf)

        ret.save()

    def _import_note(self, item):
        from orders.models import Order, OrderNote
        from django.contrib.auth import get_user_model
        from django.utils.dateparse import parse_datetime
        User = get_user_model()

        order = Order.objects.filter(order_number=item['_order_number']).first()
        if not order:
            raise ValueError(f"Order not found: {item['_order_number']}")

        note = OrderNote(order=order)
        for f in ORDER_NOTE_FIELDS:
            if f in item:
                setattr(note, f, item[f])

        email = item.get('_author_email')
        if email:
            note.author = User.objects.filter(email=email).first()

        note.save()

    def generate_diff(self, remote_data):
        items = remote_data.get('items', [])
        adds = len(items)

        return {
            'changes': [{'type': 'add', 'model': item.get('_model', '?'),
                         'name': item.get('_order_number', '?'), 'fields': {}}
                        for item in items],
            'warnings': [],
            'summary': f'{adds} record(s)' if adds else 'No changes',
        }

    def snapshot_current(self):
        return self.export(credential_mode='skip')

    def restore_snapshot(self, snapshot):
        try:
            result = self.import_data(snapshot, dry_run=False)
            return {'restored': result.get('synced', 0), 'errors': result.get('errors', [])}
        except Exception as e:
            return {'restored': 0, 'errors': [str(e)]}
