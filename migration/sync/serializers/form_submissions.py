"""
Form Submissions Sync Serializer

Handles export/import of form response data.
"""
import logging
from django.db import transaction

from .base import CollectionSyncSerializer

logger = logging.getLogger(__name__)

FORM_RESPONSE_FIELDS = [
    'session_key', 'data', 'ip_address', 'user_agent', 'referrer',
    'language', 'current_step', 'completed_steps',
    'status', 'action_results', 'time_to_complete',
]


class FormSubmissionsSerializer(CollectionSyncSerializer):
    category_key = 'form_submissions'
    natural_key_fields = ['_form_slug', 'session_key']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from form_builder.models import FormResponse
        self.model_class = FormResponse

    def get_count(self):
        from form_builder.models import FormResponse
        return FormResponse.objects.count()

    def export(self, credential_mode='redact'):
        from form_builder.models import FormResponse

        items = []
        for resp in FormResponse.objects.select_related('form', 'user').all():
            data = {f: getattr(resp, f) for f in FORM_RESPONSE_FIELDS}
            data['_source_pk'] = resp.pk
            data['_model'] = 'FormResponse'
            data['_form_slug'] = resp.form.slug
            data['_user_email'] = resp.user.email if resp.user else None
            if resp.submitted_at:
                data['_submitted_at'] = resp.submitted_at.isoformat()
            if resp.completed_at:
                data['_completed_at'] = resp.completed_at.isoformat()
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
                    self._import_response(item)
                    synced += 1
            except Exception as e:
                failed += 1
                errors.append(f"FormResponse: {e}")

        return {'synced': synced, 'skipped': skipped, 'failed': failed, 'errors': errors}

    def _import_response(self, item):
        from form_builder.models import Form, FormResponse
        from django.contrib.auth import get_user_model
        from django.utils.dateparse import parse_datetime
        User = get_user_model()

        form = Form.objects.filter(slug=item['_form_slug']).first()
        if not form:
            raise ValueError(f"Form not found: {item['_form_slug']}")

        existing = FormResponse.objects.filter(
            form=form, session_key=item.get('session_key', ''),
        ).first()
        obj = existing or FormResponse(form=form)

        for f in FORM_RESPONSE_FIELDS:
            if f in item:
                setattr(obj, f, item[f])

        user_email = item.get('_user_email')
        if user_email:
            obj.user = User.objects.filter(email=user_email).first()

        for dt_field in ['submitted_at', 'completed_at']:
            val = item.get(f'_{dt_field}')
            if val:
                parsed = parse_datetime(val)
                if parsed:
                    setattr(obj, dt_field, parsed)

        obj.save()

    def generate_diff(self, remote_data):
        items = remote_data.get('items', [])
        adds = len(items)  # Simplified: treat all as potential adds

        return {
            'changes': [{'type': 'add', 'model': 'FormResponse', 'name': f"Response #{i+1}", 'fields': {}}
                        for i in range(len(items))],
            'warnings': [],
            'summary': f'{adds} submission(s)' if adds else 'No changes',
        }

    def snapshot_current(self):
        return self.export(credential_mode='skip')

    def restore_snapshot(self, snapshot):
        try:
            result = self.import_data(snapshot, dry_run=False)
            return {'restored': result.get('synced', 0), 'errors': result.get('errors', [])}
        except Exception as e:
            return {'restored': 0, 'errors': [str(e)]}
