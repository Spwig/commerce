"""
Wishlists Sync Serializer

Handles export/import of customer wishlists:
- Wishlist (with nested WishlistItem)
"""
import logging
from django.db import transaction

from .base import CollectionSyncSerializer

logger = logging.getLogger(__name__)

WISHLIST_FIELDS = [
    'name', 'wishlist_layout', 'is_public', 'share_slug',
    'show_prices', 'show_availability', 'show_add_to_cart',
]

WISHLIST_ITEM_FIELDS = [
    'notes', 'priority', 'notify_when_available', 'notify_when_on_sale',
]


class WishlistsSerializer(CollectionSyncSerializer):
    category_key = 'wishlists'
    natural_key_fields = ['_user_email', 'name']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from cart.models import Wishlist
        self.model_class = Wishlist

    def get_count(self):
        from cart.models import Wishlist, WishlistItem
        return Wishlist.objects.count() + WishlistItem.objects.count()

    def export(self, credential_mode='redact'):
        from cart.models import Wishlist

        items = []
        for wl in Wishlist.objects.select_related('user').prefetch_related(
            'items', 'items__product', 'items__variant',
        ).all():
            data = {f: getattr(wl, f) for f in WISHLIST_FIELDS}
            data['_source_pk'] = wl.pk
            data['_model'] = 'Wishlist'
            data['_user_email'] = wl.user.email

            data['_items'] = []
            for wi in wl.items.all():
                wi_data = {f: getattr(wi, f) for f in WISHLIST_ITEM_FIELDS}
                wi_data['_product_sku'] = wi.product.sku if wi.product else None
                wi_data['_variant_sku'] = wi.variant.sku if wi.variant else None
                data['_items'].append(wi_data)

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
                    self._import_wishlist(item)
                    synced += 1
            except Exception as e:
                failed += 1
                errors.append(f"Wishlist '{item.get('name', '?')}': {e}")

        return {'synced': synced, 'skipped': skipped, 'failed': failed, 'errors': errors}

    def _import_wishlist(self, item):
        from cart.models import Wishlist, WishlistItem
        from django.contrib.auth import get_user_model
        User = get_user_model()

        user = User.objects.filter(email=item['_user_email']).first()
        if not user:
            raise ValueError(f"User not found: {item['_user_email']}")

        existing = Wishlist.objects.filter(user=user, name=item['name']).first()
        wl = existing or Wishlist(user=user)

        for f in WISHLIST_FIELDS:
            if f in item:
                setattr(wl, f, item[f])
        wl.save()

        # Replace items
        if existing:
            wl.items.all().delete()

        for wi_data in item.get('_items', []):
            from catalog.models import Product, ProductVariant
            wi = WishlistItem(wishlist=wl)
            for f in WISHLIST_ITEM_FIELDS:
                if f in wi_data:
                    setattr(wi, f, wi_data[f])

            product_sku = wi_data.get('_product_sku')
            if product_sku:
                wi.product = Product.objects.filter(sku=product_sku).first()
            variant_sku = wi_data.get('_variant_sku')
            if variant_sku:
                wi.variant = ProductVariant.objects.filter(sku=variant_sku).first()

            if wi.product:
                wi.save()

    def generate_diff(self, remote_data):
        from cart.models import Wishlist
        from django.contrib.auth import get_user_model
        User = get_user_model()

        items = remote_data.get('items', [])
        changes = []

        for item in items:
            user = User.objects.filter(email=item.get('_user_email')).first()
            name = f"{item.get('_user_email')}/{item.get('name', '?')}"
            if user:
                existing = Wishlist.objects.filter(user=user, name=item.get('name')).first()
                if existing:
                    changes.append({'type': 'modify', 'model': 'Wishlist', 'name': name, 'changes': []})
                else:
                    changes.append({'type': 'add', 'model': 'Wishlist', 'name': name, 'fields': {}})
            else:
                changes.append({'type': 'add', 'model': 'Wishlist', 'name': name, 'fields': {}})

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
