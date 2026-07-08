"""
Orders Sync Serializer

Handles export/import of order models (full_migration only):
- Order (with 8 MoneyFields, customer/product references)
- OrderItem (with 3 MoneyFields, parent_bundle self-FK)

Orders are imported as historical records. Payment and fulfillment
state is preserved but provider-specific references may not be
valid on the destination instance.
"""
import logging
from decimal import Decimal
from django.db import transaction

from .base import CollectionSyncSerializer

logger = logging.getLogger(__name__)

ORDER_FIELDS = [
    'order_number', 'status', 'source', 'tracking_number',
    'email', 'phone',
    # Shipping address (inline, not FK)
    'shipping_name', 'shipping_address1', 'shipping_address2',
    'shipping_city', 'shipping_state', 'shipping_postal_code',
    'shipping_country', 'shipping_phone',
    # Billing address (inline)
    'billing_same_as_shipping',
    'billing_name', 'billing_address1', 'billing_address2',
    'billing_city', 'billing_state', 'billing_postal_code',
    'billing_country', 'billing_phone',
    # Payment
    'payment_status', 'payment_method_type', 'payment_method_last4',
    # Currency
    'customer_currency', 'exchange_rate_used', 'exchange_rate_provider',
    'base_currency', 'fx_policy',
    # Base currency amounts
    'subtotal_base', 'tax_amount_base', 'shipping_cost_base',
    'discount_amount_base', 'gift_card_discount_base',
    'total_amount_base', 'amount_paid_base', 'amount_refunded_base',
    # Display
    'order_page_layout', 'show_order_progress',
    'show_shipping_updates', 'show_item_images',
    # Other
    'notes', 'special_instructions', 'metadata',
    'is_test_order', 'channel', 'language',
    'external_id',
    # Design mixin
    'template_variant', 'css_classes', 'layout_config',
    'style_overrides', 'responsive_config', 'inherit_parent_theme',
]

ORDER_ITEM_FIELDS = [
    'product_name', 'variant_name', 'sku', 'quantity',
    # Base currency
    'unit_price_base', 'total_price_base',
    # Discount
    'discount_type', 'discount_value', 'discount_reason',
    'exclude_from_vouchers',
    'customizations',
    'stock_allocated', 'stock_fulfilled',
]

# MoneyFields on Order
ORDER_MONEY_FIELDS = [
    'subtotal', 'tax_amount', 'shipping_cost',
    'discount_amount', 'gift_card_discount',
    'total_amount', 'amount_paid', 'amount_refunded',
]

# MoneyFields on OrderItem
ITEM_MONEY_FIELDS = [
    'unit_price', 'total_price', 'base_price',
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
    else:
        setattr(instance, field_name, None)
    if currency:
        setattr(instance, f'{field_name}_currency', currency)


def _serialize_datetime(data, field_name):
    val = data.get(field_name)
    if val and hasattr(val, 'isoformat'):
        data[field_name] = val.isoformat()


def _serialize_decimal(data, field_name):
    val = data.get(field_name)
    if val is not None:
        data[field_name] = str(val)


class OrdersSerializer(CollectionSyncSerializer):
    """Serializer for orders and order items (full_migration only).

    Models handled:
        - Order: Order records with status, totals, and customer reference
        - OrderItem: Individual line items within an order

    Orders are imported as historical records. PROTECT FKs (user, product,
    variant) are resolved by email/SKU but set to None if not found.
    """

    category_key = 'orders'
    natural_key_fields = ['order_number']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from orders.models import Order
        self.model_class = Order

    def get_count(self):
        from orders.models import Order, OrderItem
        return Order.objects.count() + OrderItem.objects.count()

    def export(self, credential_mode='redact'):
        from orders.models import Order, OrderItem

        items = []

        for order in Order.objects.select_related(
            'user', 'carrier', 'pickup_location',
        ).prefetch_related('items', 'items__product', 'items__variant').all():
            data = {f: getattr(order, f) for f in ORDER_FIELDS}
            data['_source_pk'] = order.pk
            data['_model'] = 'Order'

            # MoneyFields
            for mf in ORDER_MONEY_FIELDS:
                _serialize_money(data, order, mf)

            # Decimal fields
            for df in ['exchange_rate_used', 'subtotal_base', 'tax_amount_base',
                        'shipping_cost_base', 'discount_amount_base',
                        'gift_card_discount_base', 'total_amount_base',
                        'amount_paid_base', 'amount_refunded_base']:
                _serialize_decimal(data, df)

            # Datetime fields
            for dt in ['created_at', 'paid_at', 'delivered_at',
                        'pickup_date', 'estimated_delivery_date']:
                val = getattr(order, dt, None)
                if val and hasattr(val, 'isoformat'):
                    data[f'_{dt}'] = val.isoformat()

            # Portable references
            data['_user_email'] = order.user.email if order.user else None
            data['_carrier_slug'] = order.carrier.slug if order.carrier else None
            data['_pickup_location_code'] = order.pickup_location.code if order.pickup_location else None

            # Order items as nested list
            data['_items'] = []
            for oi in order.items.all().order_by('pk'):
                oi_data = {f: getattr(oi, f) for f in ORDER_ITEM_FIELDS}

                for mf in ITEM_MONEY_FIELDS:
                    _serialize_money(oi_data, oi, mf)

                for df in ['discount_value', 'unit_price_base', 'total_price_base']:
                    _serialize_decimal(oi_data, df)

                # Product/variant refs
                oi_data['_product_sku'] = oi.product.sku if oi.product else None
                oi_data['_variant_sku'] = oi.variant.sku if oi.variant else None

                # Parent bundle ref (self-FK for bundle items)
                if oi.parent_bundle:
                    oi_data['_parent_bundle_sku'] = oi.parent_bundle.sku
                else:
                    oi_data['_parent_bundle_sku'] = None

                if oi.created_at and hasattr(oi.created_at, 'isoformat'):
                    oi_data['_created_at'] = oi.created_at.isoformat()

                data['_items'].append(oi_data)

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
            if item.get('_model') != 'Order':
                skipped += 1
                continue
            try:
                with transaction.atomic():
                    self._import_order(item)
                    synced += 1
            except Exception as e:
                failed += 1
                errors.append(f"Order {item.get('order_number', '?')}: {e}")

        result = {'synced': synced, 'skipped': skipped, 'failed': failed, 'errors': errors}

        if sync_mode == 'mirror':
            deleted = self._delete_absent(items)
            result['deleted'] = deleted

        return result

    def _import_order(self, item):
        from orders.models import Order, OrderItem
        from django.contrib.auth import get_user_model
        from django.utils.dateparse import parse_datetime, parse_date
        User = get_user_model()

        existing = Order.objects.filter(order_number=item['order_number']).first()
        order = existing or Order()

        for f in ORDER_FIELDS:
            if f in item:
                val = item[f]
                if f == 'exchange_rate_used' and val is not None:
                    val = Decimal(str(val))
                # Base currency decimal fields
                if f.endswith('_base') and val is not None:
                    val = Decimal(str(val))
                setattr(order, f, val)

        # MoneyFields
        for mf in ORDER_MONEY_FIELDS:
            _deserialize_money(order, item, mf)

        # Resolve user by email (PROTECT FK - set None if not found)
        user_email = item.get('_user_email')
        if user_email:
            order.user = User.objects.filter(email=user_email).first()
        else:
            order.user = None

        # Resolve carrier by slug
        carrier_slug = item.get('_carrier_slug')
        if carrier_slug:
            from shipping.models import CarrierPreset
            order.carrier = CarrierPreset.objects.filter(slug=carrier_slug).first()
        else:
            order.carrier = None

        # Resolve pickup location
        loc_code = item.get('_pickup_location_code')
        if loc_code:
            from shipping.models import Location
            order.pickup_location = Location.objects.filter(code=loc_code).first()
        else:
            order.pickup_location = None

        # Datetime fields
        for dt_field in ['created_at', 'paid_at', 'delivered_at', 'pickup_date']:
            val = item.get(f'_{dt_field}')
            if val:
                parsed = parse_datetime(val)
                if parsed:
                    setattr(order, dt_field, parsed)

        est_delivery = item.get('_estimated_delivery_date')
        if est_delivery:
            parsed = parse_date(est_delivery) if len(est_delivery) == 10 else None
            if not parsed:
                parsed_dt = parse_datetime(est_delivery)
                if parsed_dt:
                    parsed = parsed_dt.date()
            if parsed:
                order.estimated_delivery_date = parsed

        order.save()

        # Import order items
        if existing:
            OrderItem.objects.filter(order=order).delete()

        item_map = {}  # sku -> OrderItem for parent_bundle resolution
        items_data = item.get('_items', [])

        # Two-pass: first create items without parent_bundle, then set parent
        for oi_data in items_data:
            oi = OrderItem(order=order)

            for f in ORDER_ITEM_FIELDS:
                if f in oi_data:
                    val = oi_data[f]
                    if f in ('discount_value', 'unit_price_base', 'total_price_base') and val is not None:
                        val = Decimal(str(val))
                    setattr(oi, f, val)

            for mf in ITEM_MONEY_FIELDS:
                _deserialize_money(oi, oi_data, mf)

            # Resolve product/variant (PROTECT FK)
            product_sku = oi_data.get('_product_sku')
            if product_sku:
                from catalog.models import Product
                oi.product = Product.objects.filter(sku=product_sku).first()
                if not oi.product:
                    logger.warning(f"Product not found for order item: {product_sku}")

            variant_sku = oi_data.get('_variant_sku')
            if variant_sku:
                from catalog.models import ProductVariant
                oi.variant = ProductVariant.objects.filter(sku=variant_sku).first()

            # Datetime
            created = oi_data.get('_created_at')
            if created:
                from django.utils.dateparse import parse_datetime as pd
                parsed = pd(created)
                if parsed:
                    oi.created_at = parsed

            oi.save()
            if oi.sku:
                item_map[oi.sku] = oi

        # Second pass: set parent_bundle
        for i, oi_data in enumerate(items_data):
            parent_sku = oi_data.get('_parent_bundle_sku')
            if parent_sku and parent_sku in item_map:
                # Get the corresponding OrderItem
                oi_sku = oi_data.get('sku')
                if oi_sku and oi_sku in item_map:
                    oi = item_map[oi_sku]
                    oi.parent_bundle = item_map[parent_sku]
                    oi.save(update_fields=['parent_bundle'])

    def _delete_absent(self, remote_items):
        from orders.models import Order

        remote_numbers = {item.get('order_number') for item in remote_items if item.get('_model') == 'Order'}

        deleted = 0
        for order in Order.objects.all():
            if order.order_number not in remote_numbers:
                try:
                    order.delete()
                    deleted += 1
                except Exception as e:
                    logger.warning(f"Cannot delete order {order.order_number}: {e}")
        return deleted

    def generate_diff(self, remote_data):
        from orders.models import Order

        items = remote_data.get('items', [])
        changes = []

        for item in items:
            if item.get('_model') != 'Order':
                continue

            order_number = item.get('order_number')
            existing = Order.objects.filter(order_number=order_number).first()

            if existing:
                field_changes = self._compute_field_diff(existing, item, ORDER_FIELDS)
                if field_changes:
                    changes.append({
                        'type': 'modify', 'model': 'Order',
                        'name': order_number, 'changes': field_changes,
                    })
            else:
                changes.append({
                    'type': 'add', 'model': 'Order',
                    'name': order_number,
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
