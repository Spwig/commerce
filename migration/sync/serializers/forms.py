"""
Forms Sync Serializer

Handles export/import of form models:
- Form (with FormStep, FormField, FormConditionalRule, FormAction children)
"""
import logging
from django.db import transaction

from .base import CollectionSyncSerializer

logger = logging.getLogger(__name__)

FORM_FIELDS = [
    'name', 'slug', 'title', 'description',
    'submit_button_text', 'success_message', 'error_message',
    'is_active', 'is_multi_step', 'require_login',
    'save_partial_responses', 'spam_protection',
    'recaptcha_site_key', 'translations',
]

FORM_STEP_FIELDS = [
    'title', 'description', 'order', 'is_skippable',
    'next_button_text', 'back_button_text', 'translations',
]

FORM_FIELD_FIELDS = [
    'field_name', 'field_type', 'label', 'placeholder', 'help_text',
    'is_required', 'min_length', 'max_length', 'min_value', 'max_value',
    'validation_regex', 'validation_message',
    'options', 'rating_config', 'file_config', 'product_config',
    'default_value', 'order', 'width', 'css_class', 'translations',
]

FORM_RULE_FIELDS = [
    'name', 'is_active', 'operator', 'value',
    'action', 'action_value', 'priority',
]

FORM_ACTION_FIELDS = [
    'action_type', 'name', 'is_active', 'config', 'order',
]


class FormsSerializer(CollectionSyncSerializer):
    """Serializer for merchant-created forms.

    Models handled:
        - Form: Form definitions with nested steps, fields, rules, actions
    """

    category_key = 'forms'
    natural_key_fields = ['slug']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from form_builder.models import Form
        self.model_class = Form

    def get_count(self):
        from form_builder.models import Form
        return Form.objects.count()

    def export(self, credential_mode='redact'):
        from form_builder.models import Form

        items = []
        for form in Form.objects.prefetch_related(
            'steps', 'fields', 'fields__step', 'rules',
            'rules__source_field', 'rules__target_field', 'rules__target_step',
            'actions',
        ).all():
            data = {field: getattr(form, field) for field in FORM_FIELDS}
            data['_source_pk'] = form.pk
            data['_model'] = 'Form'

            # Handle recaptcha_secret_key as credential
            if credential_mode == 'redact' and form.recaptcha_secret_key:
                data['_recaptcha_secret_redacted'] = (
                    form.recaptcha_secret_key[:2] + '***'
                    if len(form.recaptcha_secret_key) > 2 else '***'
                )
            elif credential_mode == 'decrypt':
                data['recaptcha_secret_key'] = form.recaptcha_secret_key

            # Nested steps
            data['_steps'] = []
            for step in form.steps.all().order_by('order'):
                step_data = {f: getattr(step, f) for f in FORM_STEP_FIELDS}
                step_data['_source_pk'] = step.pk
                data['_steps'].append(step_data)

            # Nested fields
            data['_fields'] = []
            for field in form.fields.all().order_by('order'):
                field_data = {f: getattr(field, f) for f in FORM_FIELD_FIELDS}
                field_data['_source_pk'] = field.pk
                field_data['_step_order'] = field.step.order if field.step else None
                data['_fields'].append(field_data)

            # Nested rules
            data['_rules'] = []
            for rule in form.rules.all().order_by('priority'):
                rule_data = {f: getattr(rule, f) for f in FORM_RULE_FIELDS}
                rule_data['_source_pk'] = rule.pk
                rule_data['_source_field_name'] = (
                    rule.source_field.field_name if rule.source_field else None
                )
                rule_data['_target_field_name'] = (
                    rule.target_field.field_name if rule.target_field else None
                )
                rule_data['_target_step_order'] = (
                    rule.target_step.order if rule.target_step else None
                )
                data['_rules'].append(rule_data)

            # Nested actions
            data['_actions'] = []
            for action in form.actions.all().order_by('order'):
                action_data = {f: getattr(action, f) for f in FORM_ACTION_FIELDS}
                action_data['_source_pk'] = action.pk
                data['_actions'].append(action_data)

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
                    self._import_form(item)
                    synced += 1
            except Exception as e:
                failed += 1
                errors.append(f"{item.get('name', 'Unknown')}: {e}")

        result = {'synced': synced, 'skipped': skipped, 'failed': failed, 'errors': errors}

        if sync_mode == 'mirror':
            deleted = self._delete_absent(items)
            result['deleted'] = deleted

        return result

    def _import_form(self, item):
        from form_builder.models import (
            Form, FormStep, FormField, FormConditionalRule, FormAction,
        )

        slug = item['slug']
        existing = Form.objects.filter(slug=slug).first()

        if existing:
            form = existing
            for field in FORM_FIELDS:
                if field in item:
                    setattr(form, field, item[field])
            if 'recaptcha_secret_key' in item:
                form.recaptcha_secret_key = item['recaptcha_secret_key']
            form.save()
            # Clear existing children for re-import
            form.steps.all().delete()
            form.fields.all().delete()
            form.rules.all().delete()
            form.actions.all().delete()
        else:
            form = Form()
            for field in FORM_FIELDS:
                if field in item:
                    setattr(form, field, item[field])
            if 'recaptcha_secret_key' in item:
                form.recaptcha_secret_key = item['recaptcha_secret_key']
            form.save()

        # Import steps
        step_map = {}  # order -> step instance
        for step_data in item.get('_steps', []):
            step = FormStep(form=form)
            for f in FORM_STEP_FIELDS:
                if f in step_data:
                    setattr(step, f, step_data[f])
            step.save()
            step_map[step.order] = step

        # Import fields
        field_map = {}  # field_name -> field instance
        for field_data in item.get('_fields', []):
            form_field = FormField(form=form)
            for f in FORM_FIELD_FIELDS:
                if f in field_data:
                    setattr(form_field, f, field_data[f])
            # Resolve step reference
            step_order = field_data.get('_step_order')
            if step_order is not None and step_order in step_map:
                form_field.step = step_map[step_order]
            form_field.save()
            field_map[form_field.field_name] = form_field

        # Import rules
        for rule_data in item.get('_rules', []):
            rule = FormConditionalRule(form=form)
            for f in FORM_RULE_FIELDS:
                if f in rule_data:
                    setattr(rule, f, rule_data[f])
            # Resolve field references
            src_name = rule_data.get('_source_field_name')
            if src_name and src_name in field_map:
                rule.source_field = field_map[src_name]
            tgt_name = rule_data.get('_target_field_name')
            if tgt_name and tgt_name in field_map:
                rule.target_field = field_map[tgt_name]
            tgt_step = rule_data.get('_target_step_order')
            if tgt_step is not None and tgt_step in step_map:
                rule.target_step = step_map[tgt_step]
            rule.save()

        # Import actions
        for action_data in item.get('_actions', []):
            action = FormAction(form=form)
            for f in FORM_ACTION_FIELDS:
                if f in action_data:
                    setattr(action, f, action_data[f])
            action.save()

    def _delete_absent(self, remote_items):
        from form_builder.models import Form

        remote_slugs = {item['slug'] for item in remote_items}
        deleted = 0
        for form in Form.objects.all():
            if form.slug not in remote_slugs:
                try:
                    with transaction.atomic():
                        form.hard_delete()
                        deleted += 1
                except Exception as e:
                    logger.warning(f"Cannot delete form {form.slug}: {e}")
        return deleted

    def generate_diff(self, remote_data):
        from form_builder.models import Form

        items = remote_data.get('items', [])
        changes = []

        for item in items:
            existing = Form.objects.filter(slug=item.get('slug')).first()
            if existing:
                field_changes = self._compute_field_diff(existing, item, FORM_FIELDS)
                if field_changes:
                    changes.append({
                        'type': 'modify', 'model': 'Form',
                        'name': item.get('name', 'Unknown'),
                        'changes': field_changes,
                    })
            else:
                changes.append({
                    'type': 'add', 'model': 'Form',
                    'name': item.get('name', 'Unknown'),
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
