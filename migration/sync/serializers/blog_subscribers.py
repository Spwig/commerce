"""
Blog Subscribers Sync Serializer

Handles export/import of blog email subscribers.
"""
import logging
from django.db import transaction

from .base import CollectionSyncSerializer

logger = logging.getLogger(__name__)

SUBSCRIBER_FIELDS = [
    'email', 'name', 'notification_frequency', 'language_code',
    'verification_status', 'is_active',
]


class BlogSubscribersSerializer(CollectionSyncSerializer):
    category_key = 'blog_subscribers'
    natural_key_fields = ['email']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from blog.models import BlogSubscriber
        self.model_class = BlogSubscriber

    def get_count(self):
        from blog.models import BlogSubscriber
        return BlogSubscriber.objects.count()

    def export(self, credential_mode='redact'):
        from blog.models import BlogSubscriber

        items = []
        for sub in BlogSubscriber.objects.prefetch_related('subscribed_categories').all():
            data = {f: getattr(sub, f) for f in SUBSCRIBER_FIELDS}
            data['_source_pk'] = str(sub.pk)
            data['_model'] = 'BlogSubscriber'
            data['_user_email'] = sub.user.email if sub.user else None
            data['_category_slugs'] = list(
                sub.subscribed_categories.values_list('slug', flat=True)
            )
            if sub.verified_at:
                data['_verified_at'] = sub.verified_at.isoformat()
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
                    self._import_subscriber(item)
                    synced += 1
            except Exception as e:
                failed += 1
                errors.append(f"Subscriber '{item.get('email', '?')}': {e}")

        return {'synced': synced, 'skipped': skipped, 'failed': failed, 'errors': errors}

    def _import_subscriber(self, item):
        from blog.models import BlogSubscriber, BlogCategory
        from django.contrib.auth import get_user_model
        from django.utils.dateparse import parse_datetime
        User = get_user_model()

        existing = BlogSubscriber.objects.filter(email=item['email']).first()
        obj = existing or BlogSubscriber()

        for f in SUBSCRIBER_FIELDS:
            if f in item:
                setattr(obj, f, item[f])

        user_email = item.get('_user_email')
        if user_email:
            obj.user = User.objects.filter(email=user_email).first()

        verified = item.get('_verified_at')
        if verified:
            parsed = parse_datetime(verified)
            if parsed:
                obj.verified_at = parsed

        obj.save()

        # M2M categories
        cat_slugs = item.get('_category_slugs', [])
        if cat_slugs:
            cats = BlogCategory.objects.filter(slug__in=cat_slugs)
            obj.subscribed_categories.set(cats)

    def generate_diff(self, remote_data):
        from blog.models import BlogSubscriber

        items = remote_data.get('items', [])
        changes = []

        for item in items:
            existing = BlogSubscriber.objects.filter(email=item.get('email')).first()
            if existing:
                field_changes = self._compute_field_diff(existing, item, SUBSCRIBER_FIELDS)
                if field_changes:
                    changes.append({
                        'type': 'modify', 'model': 'BlogSubscriber',
                        'name': item.get('email', '?'), 'changes': field_changes,
                    })
            else:
                changes.append({
                    'type': 'add', 'model': 'BlogSubscriber',
                    'name': item.get('email', '?'),
                    'fields': {k: v for k, v in item.items() if not k.startswith('_')},
                })

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
