"""
Mixins for models and admin classes to support custom fields.

CustomFieldsMixin - add to models that should have custom fields
CustomFieldsAdminMixin - add to ModelAdmin classes to render custom fields in forms
"""
import json
import logging

from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.indexes import GinIndex
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from .models import CustomFieldDefinition, CustomFieldGroup
from .validators import validate_custom_field_value

logger = logging.getLogger(__name__)


class CustomFieldsMixin(models.Model):
    """
    Abstract model mixin that adds a custom_fields JSONField.

    Add to any model that should support merchant-defined custom fields:

        class Product(CustomFieldsMixin, models.Model):
            ...

    The JSONField stores values as {field_slug: value}.
    """
    custom_fields = models.JSONField(
        _('custom fields'),
        default=dict,
        blank=True,
        help_text=_('Custom field values defined by the merchant')
    )

    class Meta:
        abstract = True

    def get_custom_field_value(self, slug, default=None):
        """
        Get a custom field value with lazy default from the field definition.

        If the field has no stored value, returns the definition's default_value.
        This avoids needing to backfill existing records when new fields are added.
        """
        value = self.custom_fields.get(slug)
        if value is not None:
            return value

        # Fall back to definition default
        definitions = CustomFieldDefinition.get_cached_for_model(type(self))
        for field_def in definitions:
            if field_def.slug == slug:
                if field_def.default_value is not None:
                    return field_def.default_value
                break
        return default

    def set_custom_field_value(self, slug, value):
        """Set a single custom field value."""
        if not self.custom_fields:
            self.custom_fields = {}
        self.custom_fields[slug] = value

    def get_custom_fields_display(self, storefront_only=False):
        """
        Get custom field values with their definitions for display.

        Returns a list of dicts:
        [{"group": group, "fields": [{"definition": def, "value": val}, ...]}]
        """
        ct = ContentType.objects.get_for_model(type(self))
        groups = CustomFieldGroup.get_cached_for_content_type(ct)
        definitions = CustomFieldDefinition.get_cached_for_content_type(ct)

        result = []
        for group in groups:
            if storefront_only and not group.show_on_storefront:
                continue

            group_fields = []
            for field_def in definitions:
                if field_def.group_id != group.pk:
                    continue
                if storefront_only and not field_def.show_on_storefront:
                    continue

                value = self.get_custom_field_value(field_def.slug)
                if value is not None and value != '' and value != []:
                    # Format display value for select/multiselect
                    display_value = value
                    if field_def.field_type == 'select':
                        choices = field_def.get_choices()
                        for c in choices:
                            if c.get('value') == value:
                                display_value = c.get('label', value)
                                break
                    elif field_def.field_type == 'multiselect' and isinstance(value, list):
                        choices = {c['value']: c['label'] for c in field_def.get_choices()}
                        display_value = [choices.get(v, v) for v in value]
                    elif field_def.field_type == 'boolean':
                        display_value = _('Yes') if value else _('No')

                    group_fields.append({
                        'definition': field_def,
                        'value': value,
                        'display_value': display_value,
                    })

            if group_fields:
                result.append({
                    'group': group,
                    'fields': group_fields,
                })

        return result

    def validate_custom_fields(self):
        """Validate all custom field values against their definitions."""
        definitions = CustomFieldDefinition.get_cached_for_model(type(self))
        errors = {}
        for field_def in definitions:
            value = self.custom_fields.get(field_def.slug)
            try:
                validate_custom_field_value(field_def, value)
            except ValidationError as e:
                errors[field_def.slug] = e.message
        if errors:
            raise ValidationError(errors)


class CustomFieldsAdminMixin:
    """
    Admin mixin that injects custom fields into model change forms.

    Usage:
        @admin.register(Product)
        class ProductAdmin(CustomFieldsAdminMixin, admin.ModelAdmin):
            ...

    The mixin:
    - Injects field definitions into the template context
    - Extracts custom field values from POST data on save
    - Validates values against definitions
    """

    class CustomFieldsMedia:
        js = (
            'custom_fields/js/custom_fields_admin.js',
        )
        css = {
            'all': (
                'custom_fields/css/custom_fields_admin.css',
            )
        }

    def _get_custom_fields_context(self, obj=None):
        """Build template context for custom fields."""
        ct = ContentType.objects.get_for_model(self.model)
        definitions = CustomFieldDefinition.get_cached_for_content_type(ct)
        groups = CustomFieldGroup.get_cached_for_content_type(ct)

        # Build grouped field data with current values
        grouped_fields = []
        for group in groups:
            group_defs = [d for d in definitions if d.group_id == group.pk]
            if not group_defs:
                continue

            fields_with_values = []
            for field_def in group_defs:
                value = None
                if obj and obj.pk and hasattr(obj, 'custom_fields'):
                    value = obj.custom_fields.get(field_def.slug)
                if value is None and field_def.default_value is not None:
                    value = field_def.default_value

                fields_with_values.append({
                    'definition': field_def,
                    'value': value,
                    'choices': field_def.get_choices(),
                })

            grouped_fields.append({
                'group': group,
                'fields': fields_with_values,
            })

        return {
            'custom_field_groups': grouped_fields,
            'has_custom_fields': bool(definitions),
            'custom_field_definitions_json': json.dumps([
                {
                    'slug': d.slug,
                    'name': d.name,
                    'field_type': d.field_type,
                    'is_required': d.is_required,
                    'help_text': d.help_text_value,
                    'validation_config': d.validation_config,
                    'choices': d.get_choices(),
                }
                for d in definitions
            ]),
        }

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        obj = self.get_object(request, object_id)
        extra_context.update(self._get_custom_fields_context(obj))
        return super().change_view(request, object_id, form_url, extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context.update(self._get_custom_fields_context(None))
        return super().add_view(request, form_url, extra_context)

    def save_model(self, request, obj, form, change):
        """Extract custom field values from POST data and save."""
        ct = ContentType.objects.get_for_model(self.model)
        definitions = CustomFieldDefinition.get_cached_for_content_type(ct)

        custom_data = obj.custom_fields.copy() if obj.custom_fields else {}

        for field_def in definitions:
            post_key = f'cf_{field_def.slug}'

            if field_def.field_type == 'boolean':
                # Checkbox: present in POST = True, absent = False
                custom_data[field_def.slug] = post_key in request.POST
            elif field_def.field_type == 'multiselect':
                values = request.POST.getlist(post_key)
                custom_data[field_def.slug] = values if values else []
            else:
                value = request.POST.get(post_key, '').strip()
                if value == '':
                    # Don't store empty strings, use None
                    custom_data[field_def.slug] = None
                else:
                    # Validate and coerce
                    try:
                        custom_data[field_def.slug] = validate_custom_field_value(
                            field_def, value
                        )
                    except ValidationError:
                        # Store raw value, validation errors shown via form
                        custom_data[field_def.slug] = value

        obj.custom_fields = custom_data
        super().save_model(request, obj, form, change)
