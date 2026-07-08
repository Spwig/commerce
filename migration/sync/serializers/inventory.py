"""
Inventory Sync Serializer

Handles export/import of stock levels:
- StockItem (per-warehouse stock quantities)
"""
import logging
from django.db import transaction

from .base import CollectionSyncSerializer

logger = logging.getLogger(__name__)

STOCK_ITEM_FIELDS = [
    'on_hand', 'allocated', 'low_stock_threshold',
]


class InventorySerializer(CollectionSyncSerializer):
    """Serializer for per-warehouse stock levels.

    Models handled:
        - StockItem: Stock quantities per product/variant/warehouse
    """

    category_key = 'inventory'
    natural_key_fields = ['_product_sku', '_warehouse_code']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from catalog.models import StockItem
        self.model_class = StockItem

    def get_count(self):
        from catalog.models import StockItem
        return StockItem.objects.count()

    def export(self, credential_mode='redact'):
        from catalog.models import StockItem

        items = []
        for si in StockItem.objects.select_related(
            'product', 'warehouse', 'variant',
        ).all():
            data = {f: getattr(si, f) for f in STOCK_ITEM_FIELDS}
            data['_source_pk'] = si.pk
            data['_model'] = 'StockItem'
            data['_product_sku'] = si.product.sku
            data['_warehouse_code'] = si.warehouse.code
            data['_variant_sku'] = si.variant.sku if si.variant else None
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
                    self._import_stock_item(item)
                    synced += 1
            except Exception as e:
                failed += 1
                errors.append(
                    f"StockItem {item.get('_product_sku')}/{item.get('_warehouse_code')}: {e}"
                )

        result = {'synced': synced, 'skipped': skipped, 'failed': failed, 'errors': errors}

        if sync_mode == 'mirror':
            deleted = self._delete_absent(items)
            result['deleted'] = deleted

        return result

    def _import_stock_item(self, item):
        from catalog.models import StockItem, Product, Warehouse, ProductVariant

        product = Product.objects.filter(sku=item['_product_sku']).first()
        if not product:
            raise ValueError(f"Product not found: {item['_product_sku']}")

        warehouse = Warehouse.objects.filter(code=item['_warehouse_code']).first()
        if not warehouse:
            raise ValueError(f"Warehouse not found: {item['_warehouse_code']}")

        variant = None
        variant_sku = item.get('_variant_sku')
        if variant_sku:
            variant = ProductVariant.objects.filter(sku=variant_sku).first()

        existing = StockItem.objects.filter(
            product=product, warehouse=warehouse, variant=variant,
        ).first()
        obj = existing or StockItem(product=product, warehouse=warehouse, variant=variant)

        for f in STOCK_ITEM_FIELDS:
            if f in item:
                setattr(obj, f, item[f])
        obj.save()

    def _delete_absent(self, remote_items):
        from catalog.models import StockItem, Product, Warehouse

        remote_keys = set()
        for item in remote_items:
            p = Product.objects.filter(sku=item.get('_product_sku')).first()
            w = Warehouse.objects.filter(code=item.get('_warehouse_code')).first()
            if p and w:
                remote_keys.add((p.pk, w.pk, item.get('_variant_sku')))

        deleted = 0
        for si in StockItem.objects.select_related('product', 'warehouse', 'variant').all():
            key = (si.product_id, si.warehouse_id, si.variant.sku if si.variant else None)
            if key not in remote_keys:
                try:
                    si.delete()
                    deleted += 1
                except Exception as e:
                    logger.warning(f"Cannot delete StockItem: {e}")
        return deleted

    def generate_diff(self, remote_data):
        from catalog.models import StockItem, Product, Warehouse

        items = remote_data.get('items', [])
        changes = []

        for item in items:
            product = Product.objects.filter(sku=item.get('_product_sku')).first()
            warehouse = Warehouse.objects.filter(code=item.get('_warehouse_code')).first()
            name = f"{item.get('_product_sku')} @ {item.get('_warehouse_code')}"

            if product and warehouse:
                existing = StockItem.objects.filter(
                    product=product, warehouse=warehouse,
                ).first()
                if existing:
                    field_changes = self._compute_field_diff(existing, item, STOCK_ITEM_FIELDS)
                    if field_changes:
                        changes.append({
                            'type': 'modify', 'model': 'StockItem',
                            'name': name, 'changes': field_changes,
                        })
                else:
                    changes.append({
                        'type': 'add', 'model': 'StockItem',
                        'name': name,
                        'fields': {k: v for k, v in item.items() if not k.startswith('_')},
                    })
            else:
                changes.append({
                    'type': 'add', 'model': 'StockItem',
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
