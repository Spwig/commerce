"""
Affiliate Program Configuration Sync Serializer

Handles export/import of affiliate program configuration:
- AffiliateSettings (singleton)
- AffiliateReportSettings (singleton)
- Program (collection)
"""
import logging
from decimal import Decimal
from django.db import transaction

from .base import CollectionSyncSerializer

logger = logging.getLogger(__name__)

AFFILIATE_SETTINGS_FIELDS = [
    'hero_title', 'hero_subtitle',
    'features_title', 'features',
    'how_it_works_title', 'steps',
    'cta_title', 'cta_description',
    'allow_guest_registration', 'terms_url',
    'require_approval', 'welcome_message',
    'translations',
]

REPORT_SETTINGS_FIELDS = [
    'monthly_report_enabled', 'monthly_report_day', 'monthly_report_hour',
    'include_top_orders_count',
]

PROGRAM_FIELDS = [
    'name', 'slug', 'description',
    'commission_type', 'commission_value',
    'cookie_lifetime_days', 'status',
    'auto_approve_affiliates', 'minimum_payout',
]


class AffiliateConfigSerializer(CollectionSyncSerializer):
    """Serializer for affiliate program configuration.

    Models handled:
        - AffiliateSettings: Landing page content and registration settings (singleton)
        - AffiliateReportSettings: Report scheduling settings (singleton)
        - Program: Affiliate program definitions
    """

    category_key = 'affiliate_config'
    natural_key_fields = ['slug']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from affiliate.models import Program
        self.model_class = Program

    def get_count(self):
        from affiliate.models import AffiliateSettings, AffiliateReportSettings, Program
        return (
            AffiliateSettings.objects.count()
            + AffiliateReportSettings.objects.count()
            + Program.objects.count()
        )

    def export(self, credential_mode='redact'):
        from affiliate.models import AffiliateSettings, AffiliateReportSettings, Program

        items = []

        # AffiliateSettings singleton
        settings = AffiliateSettings.objects.first()
        if settings:
            data = {f: getattr(settings, f) for f in AFFILIATE_SETTINGS_FIELDS}
            data['_source_pk'] = settings.pk
            data['_model'] = 'AffiliateSettings'
            # Store registration form slug for portable ref
            if settings.registration_form:
                data['_registration_form_slug'] = settings.registration_form.slug
            items.append(data)

        # AffiliateReportSettings singleton
        report_settings = AffiliateReportSettings.objects.first()
        if report_settings:
            data = {f: getattr(report_settings, f) for f in REPORT_SETTINGS_FIELDS}
            data['_source_pk'] = report_settings.pk
            data['_model'] = 'AffiliateReportSettings'
            items.append(data)

        # Programs
        for program in Program.objects.all():
            data = {f: getattr(program, f) for f in PROGRAM_FIELDS}
            data['_source_pk'] = program.pk
            data['_model'] = 'Program'
            # Decimal fields
            for df in ['commission_value', 'minimum_payout']:
                if data.get(df) is not None:
                    data[df] = str(data[df])
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
                    if model_type == 'AffiliateSettings':
                        self._import_settings(item)
                    elif model_type == 'AffiliateReportSettings':
                        self._import_report_settings(item)
                    elif model_type == 'Program':
                        self._import_program(item)
                    else:
                        skipped += 1
                        continue
                    synced += 1
            except Exception as e:
                failed += 1
                errors.append(f"{model_type} '{item.get('name', item.get('slug', '?'))}': {e}")

        result = {'synced': synced, 'skipped': skipped, 'failed': failed, 'errors': errors}

        if sync_mode == 'mirror':
            deleted = self._delete_absent(items)
            result['deleted'] = deleted

        return result

    def _import_settings(self, item):
        from affiliate.models import AffiliateSettings
        obj = AffiliateSettings.objects.first() or AffiliateSettings()
        for f in AFFILIATE_SETTINGS_FIELDS:
            if f in item:
                setattr(obj, f, item[f])
        # Resolve registration form FK
        form_slug = item.get('_registration_form_slug')
        if form_slug:
            from form_builder.models import Form
            obj.registration_form = Form.objects.filter(slug=form_slug).first()
        obj.save()

    def _import_report_settings(self, item):
        from affiliate.models import AffiliateReportSettings
        obj = AffiliateReportSettings.objects.first() or AffiliateReportSettings()
        for f in REPORT_SETTINGS_FIELDS:
            if f in item:
                setattr(obj, f, item[f])
        obj.save()

    def _import_program(self, item):
        from affiliate.models import Program
        from django.contrib.auth import get_user_model
        User = get_user_model()

        existing = Program.objects.filter(slug=item['slug']).first()
        obj = existing or Program()

        for f in PROGRAM_FIELDS:
            if f in item:
                val = item[f]
                if f in ('commission_value', 'minimum_payout') and val is not None:
                    val = Decimal(str(val))
                setattr(obj, f, val)

        # Assign merchant to first staff user if creating new
        if not existing and not obj.merchant_id:
            staff_user = User.objects.filter(is_staff=True).first()
            if staff_user:
                obj.merchant = staff_user

        obj.save()

    def _delete_absent(self, remote_items):
        from affiliate.models import Program

        remote_slugs = {
            item['slug'] for item in remote_items if item.get('_model') == 'Program'
        }
        deleted = 0
        for prog in Program.objects.all():
            if prog.slug not in remote_slugs:
                try:
                    prog.delete()
                    deleted += 1
                except Exception as e:
                    logger.warning(f"Cannot delete Program '{prog.slug}': {e}")
        return deleted

    def generate_diff(self, remote_data):
        from affiliate.models import AffiliateSettings, AffiliateReportSettings, Program

        items = remote_data.get('items', [])
        changes = []

        for item in items:
            model_type = item.get('_model')
            if model_type == 'AffiliateSettings':
                existing = AffiliateSettings.objects.first()
                fields = AFFILIATE_SETTINGS_FIELDS
                name = 'Affiliate Settings'
            elif model_type == 'AffiliateReportSettings':
                existing = AffiliateReportSettings.objects.first()
                fields = REPORT_SETTINGS_FIELDS
                name = 'Report Settings'
            elif model_type == 'Program':
                existing = Program.objects.filter(slug=item.get('slug')).first()
                fields = PROGRAM_FIELDS
                name = item.get('name', item.get('slug', '?'))
            else:
                continue

            if existing:
                field_changes = self._compute_field_diff(existing, item, fields)
                if field_changes:
                    changes.append({
                        'type': 'modify', 'model': model_type,
                        'name': name, 'changes': field_changes,
                    })
            else:
                changes.append({
                    'type': 'add', 'model': model_type,
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
