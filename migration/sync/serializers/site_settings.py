"""
Site Settings Sync Serializer

Handles export/import of the SiteSettings singleton.
Includes file handling for logo and favicon (via MediaAsset ForeignKeys).
"""
import logging
from django.db import transaction

from .base import SingletonSyncSerializer
from ..file_handler import export_file_field, import_file_field

logger = logging.getLogger(__name__)

# Fields to export/import (excludes FKs to other models that need special handling)
SITE_SETTINGS_FIELDS = [
    # Basic info
    'site_name', 'site_tagline', 'site_url', 'site_description',
    # Contact
    'admin_email', 'support_email', 'phone_number',
    # Address
    'address_line_1', 'address_line_2', 'city', 'state_province',
    'postal_code', 'country',
    # Currency & Locale
    'default_currency', 'default_language', 'default_timezone',
    'enable_multi_currency', 'supported_currencies',
    'currency_selection_mode', 'show_currency_switcher',
    'currency_switcher_position', 'show_exchange_rate_info',
    'enable_locale_formatting',
    # Exchange rate
    'exchange_rate_markup_enabled', 'exchange_rate_markup_percentage',
    'exchange_rate_selection_strategy', 'exchange_rate_sync_interval',
    'multi_currency_checkout_mode',
    # E-commerce
    'allow_guest_checkout', 'require_phone_for_checkout',
    'enable_inventory_tracking', 'enable_multi_warehouse',
    'auto_approve_reviews',
    'account_creation_timing', 'account_creation_message',
    'show_social_auth_on_account_creation',
    # Email notifications
    'enable_order_confirmation_emails', 'enable_shipping_notification_emails',
    'enable_low_stock_alerts', 'low_stock_threshold',
    # SEO
    'meta_title', 'meta_description', 'meta_keywords',
    # Social
    'facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url',
    # Maintenance
    'maintenance_mode', 'maintenance_message',
    # Units
    'default_weight_unit', 'default_length_unit', 'default_volume_unit',
    'default_area_unit', 'default_temperature_unit', 'enable_unit_conversion',
    # Cookie consent
    'cookie_consent_enabled', 'cookie_banner_position', 'cookie_consent_mode',
    'cookie_banner_title', 'cookie_banner_text',
    # Shipping
    'shipping_origin_country',
    # Security
    'staff_2fa_enforcement', 'staff_2fa_grace_period_days',
    'allow_trusted_devices', 'trusted_device_duration_days',
    # Error reporting
    'error_reporting_enabled', 'error_reporting_include_js',
    # Translations
    'translations',
]

# Fields that are ForeignKeys needing special handling (excluded from direct copy)
FK_FIELDS_SKIP = [
    'site_logo', 'favicon', 'maintenance_page',
    'home_page', 'privacy_page', 'terms_page', 'cookie_page',
    'shipping_page', 'returns_page',
    'default_shipping_provider', 'default_manual_carrier',
]


class SiteSettingsSerializer(SingletonSyncSerializer):
    """Serializer for the SiteSettings singleton model."""

    category_key = 'site_settings'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from core.models import SiteSettings
        self.model_class = SiteSettings

    @property
    def export_fields(self):
        return SITE_SETTINGS_FIELDS

    def export(self, credential_mode='redact'):
        instance = self._get_instance()
        if not instance:
            return {
                'category': self.category_key,
                'sync_type': 'singleton',
                'items': {},
                'total': 0,
                'files': {},
            }

        data = {}
        for field_name in SITE_SETTINGS_FIELDS:
            try:
                field = instance._meta.get_field(field_name)
                data[field_name] = field.value_from_object(instance)
            except Exception:
                data[field_name] = getattr(instance, field_name, None)

        # Handle logo/favicon MediaAsset references
        # We export the actual image files, not just the FK IDs
        files = {}
        if instance.site_logo and instance.site_logo.original_file:
            files['site_logo'] = export_file_field(instance.site_logo, 'original_file')
        if instance.favicon and instance.favicon.original_file:
            files['favicon'] = export_file_field(instance.favicon, 'original_file')

        return {
            'category': self.category_key,
            'sync_type': 'singleton',
            'items': data,
            'total': 1,
            'files': files,
        }

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
                    from core.models import SiteSettings
                    instance = SiteSettings()

                for field_name, value in items.items():
                    if field_name in SITE_SETTINGS_FIELDS:
                        try:
                            setattr(instance, field_name, value)
                        except Exception as e:
                            errors.append(f"Field {field_name}: {e}")

                instance.save()

                # Handle file imports (logo, favicon)
                files = data.get('files', {})
                if files:
                    self._import_files(instance, files)

        except Exception as e:
            logger.error(f"SiteSettings import failed: {e}")
            return {'synced': 0, 'skipped': 0, 'failed': 1, 'errors': [str(e)]}

        return {
            'synced': 1,
            'skipped': 0,
            'failed': len(errors),
            'errors': errors,
        }

    def _import_files(self, instance, files):
        """Import logo and favicon files, creating MediaAsset records."""
        from media_library.models import MediaAsset
        import base64
        from django.core.files.base import ContentFile

        for file_key in ('site_logo', 'favicon'):
            file_data = files.get(file_key)
            if not file_data or not file_data.get('data'):
                continue

            try:
                content = base64.b64decode(file_data['data'])
                filename = file_data.get('filename', f'{file_key}.png')
                import os
                filename = os.path.basename(filename)

                # Create or reuse MediaAsset
                content_file = ContentFile(content, name=filename)
                asset = MediaAsset(
                    title=f"Synced {file_key}",
                    alt_text=file_key.replace('_', ' ').title(),
                )
                asset.original_file.save(filename, content_file, save=True)

                setattr(instance, file_key, asset)
                instance.save(update_fields=[file_key])
            except Exception as e:
                logger.error(f"Failed to import {file_key}: {e}")

    def snapshot_current(self):
        return self.export(credential_mode='skip')

    def restore_snapshot(self, snapshot):
        try:
            result = self.import_data(snapshot, dry_run=False)
            return {'restored': result.get('synced', 0), 'errors': result.get('errors', [])}
        except Exception as e:
            return {'restored': 0, 'errors': [str(e)]}
