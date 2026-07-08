"""
Reviews Sync Serializer

Handles export/import of product review models (full_migration only):
- ProductReview
"""
import logging
from django.db import transaction
from django.utils import timezone

from .base import CollectionSyncSerializer

logger = logging.getLogger(__name__)

REVIEW_FIELDS = [
    'rating', 'title', 'comment', 'external_id',
    'is_verified_purchase', 'is_approved', 'helpful_count',
    'images', 'created_at',
]


class ReviewsSerializer(CollectionSyncSerializer):
    """Serializer for product reviews (full_migration only).

    Models handled:
        - ProductReview: Customer product reviews with ratings and text

    Note: Reviews reference products (by SKU) and customers (by email)
    which must be resolved during import.
    """

    category_key = 'reviews'
    natural_key_fields = ['_product_sku', '_user_email']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from catalog.models import ProductReview
        self.model_class = ProductReview

    def get_count(self):
        from catalog.models import ProductReview
        return ProductReview.objects.count()

    def export(self, credential_mode='redact'):
        from catalog.models import ProductReview

        items = []
        for review in ProductReview.objects.select_related('product', 'user').all():
            data = {}
            for field in REVIEW_FIELDS:
                value = getattr(review, field)
                if hasattr(value, 'isoformat'):
                    value = value.isoformat()
                data[field] = value

            data['_source_pk'] = review.pk
            data['_model'] = 'ProductReview'
            data['_product_sku'] = review.product.sku if review.product else ''
            data['_user_email'] = review.user.email if review.user else ''

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
                    self._import_review(item)
                    synced += 1
            except Exception as e:
                failed += 1
                errors.append(f"Review by {item.get('_user_email', '?')} on "
                              f"{item.get('_product_sku', '?')}: {e}")

        result = {'synced': synced, 'skipped': skipped, 'failed': failed, 'errors': errors}

        if sync_mode == 'mirror':
            deleted = self._delete_absent(items)
            result['deleted'] = deleted

        return result

    def _import_review(self, item):
        from catalog.models import Product, ProductReview
        from django.contrib.auth import get_user_model
        User = get_user_model()

        product_sku = item.get('_product_sku')
        user_email = item.get('_user_email')

        if not product_sku:
            raise ValueError("Missing _product_sku")
        if not user_email:
            raise ValueError("Missing _user_email")

        product = Product.objects.filter(sku=product_sku).first()
        if not product:
            raise ValueError(f"Product not found: {product_sku}")

        user = User.objects.filter(email=user_email).first()
        if not user:
            raise ValueError(f"User not found: {user_email}")

        existing = ProductReview.objects.filter(product=product, user=user).first()

        if existing:
            for field in REVIEW_FIELDS:
                if field in item and field != 'created_at':
                    setattr(existing, field, item[field])
            existing.save()
        else:
            review = ProductReview(product=product, user=user)
            for field in REVIEW_FIELDS:
                if field in item:
                    setattr(review, field, item[field])
            review.save()

    def _delete_absent(self, remote_items):
        from catalog.models import Product, ProductReview
        from django.contrib.auth import get_user_model
        User = get_user_model()

        remote_keys = set()
        for item in remote_items:
            sku = item.get('_product_sku')
            email = item.get('_user_email')
            if sku and email:
                remote_keys.add((sku, email))

        deleted = 0
        for review in ProductReview.objects.select_related('product', 'user').all():
            key = (review.product.sku, review.user.email)
            if key not in remote_keys:
                try:
                    review.delete()
                    deleted += 1
                except Exception as e:
                    logger.warning(f"Cannot delete review {review.pk}: {e}")
        return deleted

    def generate_diff(self, remote_data):
        from catalog.models import Product, ProductReview
        from django.contrib.auth import get_user_model
        User = get_user_model()

        items = remote_data.get('items', [])
        changes = []

        for item in items:
            product = Product.objects.filter(sku=item.get('_product_sku')).first()
            user = User.objects.filter(email=item.get('_user_email')).first()

            display = f"Review by {item.get('_user_email', '?')} on {item.get('_product_sku', '?')}"

            if product and user:
                existing = ProductReview.objects.filter(
                    product=product, user=user
                ).first()
                if existing:
                    compare_fields = [f for f in REVIEW_FIELDS if f != 'created_at']
                    field_changes = self._compute_field_diff(existing, item, compare_fields)
                    if field_changes:
                        changes.append({
                            'type': 'modify', 'model': 'ProductReview',
                            'name': display, 'changes': field_changes,
                        })
                else:
                    changes.append({
                        'type': 'add', 'model': 'ProductReview',
                        'name': display,
                        'fields': {k: v for k, v in item.items() if not k.startswith('_')},
                    })
            else:
                changes.append({
                    'type': 'add', 'model': 'ProductReview',
                    'name': display,
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
