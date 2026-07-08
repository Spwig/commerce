"""
Blog Settings Sync Serializer

Handles export/import of the BlogSettings singleton.
"""
import logging
from django.db import transaction
from .base import SingletonSyncSerializer

logger = logging.getLogger(__name__)

BLOG_SETTINGS_FIELDS = [
    'posts_per_page', 'show_reading_time', 'show_view_count',
    'show_related_posts', 'related_posts_count',
    'rss_enabled', 'rss_posts_count', 'rss_include_full_content',
    'enable_subscriptions', 'require_double_opt_in', 'default_frequency',
    'weekly_digest_day', 'weekly_digest_hour',
    'monthly_digest_day', 'monthly_digest_hour',
]


class BlogSettingsSerializer(SingletonSyncSerializer):
    """Serializer for the BlogSettings singleton model."""

    category_key = 'blog_settings'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from blog.models import BlogSettings
        self.model_class = BlogSettings

    @property
    def export_fields(self):
        return BLOG_SETTINGS_FIELDS

    def import_data(self, data, dry_run=False, sync_mode='additive'):
        if dry_run:
            return self.generate_diff(data)

        items = data.get('items', {})
        if not items:
            return {'synced': 0, 'skipped': 0, 'failed': 0, 'errors': []}

        errors = []
        try:
            with transaction.atomic():
                instance = self._get_instance()
                if not instance:
                    from blog.models import BlogSettings
                    instance = BlogSettings(pk=1)

                for field_name, value in items.items():
                    if field_name in BLOG_SETTINGS_FIELDS:
                        try:
                            setattr(instance, field_name, value)
                        except Exception as e:
                            errors.append(f"Field {field_name}: {e}")

                instance.save()

        except Exception as e:
            logger.error(f"BlogSettings import failed: {e}")
            return {'synced': 0, 'skipped': 0, 'failed': 1, 'errors': [str(e)]}

        return {'synced': 1, 'skipped': 0, 'failed': len(errors), 'errors': errors}

    def restore_snapshot(self, snapshot):
        try:
            result = self.import_data(snapshot, dry_run=False)
            return {'restored': result.get('synced', 0), 'errors': result.get('errors', [])}
        except Exception as e:
            return {'restored': 0, 'errors': [str(e)]}
