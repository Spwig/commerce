"""
Social Sharing Settings Sync Serializer
"""
import logging
from django.db import transaction
from .base import SingletonSyncSerializer

logger = logging.getLogger(__name__)

SOCIAL_SHARING_FIELDS = [
    'enable_on_products', 'enable_on_categories',
    'enable_on_blog_posts', 'enable_on_pages',
    'placement_position', 'button_style', 'button_size',
    'layout_direction', 'show_title',
    'mobile_visibility', 'widget_slug', 'default_config',
    'enabled_platforms', 'show_counts', 'track_shares',
]


class SocialSharingSerializer(SingletonSyncSerializer):
    """Serializer for the SocialSharingSettings singleton model."""

    category_key = 'social_sharing'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from social_sharing.settings_models import SocialSharingSettings
        self.model_class = SocialSharingSettings

    @property
    def export_fields(self):
        return SOCIAL_SHARING_FIELDS

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
                    from social_sharing.settings_models import SocialSharingSettings
                    instance = SocialSharingSettings(pk=1)

                for field_name, value in items.items():
                    if field_name in SOCIAL_SHARING_FIELDS:
                        try:
                            setattr(instance, field_name, value)
                        except Exception as e:
                            errors.append(f"Field {field_name}: {e}")

                instance.save()

        except Exception as e:
            logger.error(f"SocialSharingSettings import failed: {e}")
            return {'synced': 0, 'skipped': 0, 'failed': 1, 'errors': [str(e)]}

        return {'synced': 1, 'skipped': 0, 'failed': len(errors), 'errors': errors}

    def restore_snapshot(self, snapshot):
        try:
            result = self.import_data(snapshot, dry_run=False)
            return {'restored': result.get('synced', 0), 'errors': result.get('errors', [])}
        except Exception as e:
            return {'restored': 0, 'errors': [str(e)]}
