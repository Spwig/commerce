"""
Custom Fields models for extending platform objects with merchant-defined fields.

The system uses a hybrid approach:
- CustomFieldGroup / CustomFieldDefinition store the schema (what fields exist)
- A JSONField on target models stores actual values ({field_slug: value})

This avoids EAV complexity while providing full schema governance.
"""
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from core.models import SoftDeleteModel


CACHE_KEY_PREFIX = 'custom_fields_defs'
CACHE_TTL = 3600  # 1 hour


# Models that support custom fields (app_label.model_name)
SUPPORTED_MODELS = [
    'catalog.product',
    'catalog.category',
    'orders.order',
    'accounts.customerprofile',
]


def get_supported_content_types():
    """Return ContentType IDs for supported models."""
    ct_ids = []
    for model_ref in SUPPORTED_MODELS:
        app_label, model_name = model_ref.split('.')
        try:
            ct = ContentType.objects.get(app_label=app_label, model=model_name)
            ct_ids.append(ct.pk)
        except ContentType.DoesNotExist:
            pass
    return ct_ids


class CustomFieldGroup(SoftDeleteModel):
    """
    Groups custom fields into logical sections.

    Example: "Shipping Info", "External IDs", "Custom Attributes"
    Groups are displayed as collapsible sections within the Custom Fields tab.

    Inherits SoftDeleteModel for recycle bin support (is_deleted, deleted_at, deleted_by).
    The is_active field is a separate concept: deactivation toggle vs. deletion.
    """
    name = models.CharField(
        _('group name'),
        max_length=100,
        help_text=_('Display name for this group of fields')
    )
    slug = models.SlugField(
        _('slug'),
        max_length=100,
        help_text=_('URL-safe identifier (auto-generated from name)')
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name='custom_field_groups',
        verbose_name=_('model'),
        help_text=_('Which model this group belongs to')
    )
    sort_order = models.PositiveIntegerField(
        _('sort order'),
        default=0,
        help_text=_('Display order (lower numbers appear first)')
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Inactive groups are hidden from forms but data is preserved')
    )
    show_on_storefront = models.BooleanField(
        _('show on storefront'),
        default=False,
        help_text=_('Whether this group should be visible on the customer-facing storefront')
    )
    translations = models.JSONField(
        default=dict,
        blank=True,
        help_text=_('Translated group names by language code')
    )
    created_at = models.DateTimeField(_('created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated'), auto_now=True)

    class Meta:
        ordering = ['content_type', 'sort_order', 'name']
        unique_together = ['slug', 'content_type']
        verbose_name = _('custom field group')
        verbose_name_plural = _('custom field groups')

    def __str__(self):
        return f"{self.name} ({self.content_type})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @classmethod
    def get_cached_for_content_type(cls, content_type):
        """Get all active groups for a content type, from cache."""
        cache_key = f'{CACHE_KEY_PREFIX}:groups:{content_type.pk}'
        groups = cache.get(cache_key)
        if groups is None:
            groups = list(
                cls.objects.filter(
                    content_type=content_type,
                    is_active=True
                ).order_by('sort_order', 'name')
            )
            cache.set(cache_key, groups, CACHE_TTL)
        return groups


class CustomFieldDefinition(SoftDeleteModel):
    """
    Defines a single custom field and its configuration.

    Each definition specifies:
    - Which model it belongs to (via content_type)
    - Field type (text, number, boolean, etc.)
    - Validation rules (min/max, regex, choices)
    - Display options (required, storefront visibility, translatable)

    Inherits SoftDeleteModel for recycle bin support (is_deleted, deleted_at, deleted_by).
    The is_active field is a separate concept: deactivation toggle vs. deletion.
    """
    FIELD_TYPES = [
        ('text', _('Text')),
        ('textarea', _('Textarea')),
        ('number', _('Number (integer)')),
        ('decimal', _('Decimal')),
        ('boolean', _('Yes/No')),
        ('date', _('Date')),
        ('datetime', _('Date & Time')),
        ('url', _('URL')),
        ('email', _('Email')),
        ('select', _('Dropdown (single)')),
        ('multiselect', _('Dropdown (multiple)')),
        ('color', _('Color picker')),
    ]

    group = models.ForeignKey(
        CustomFieldGroup,
        on_delete=models.CASCADE,
        related_name='fields',
        verbose_name=_('group'),
        help_text=_('Which group this field belongs to')
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name='custom_field_definitions',
        verbose_name=_('model'),
        help_text=_('Which model this field belongs to')
    )
    name = models.CharField(
        _('field name'),
        max_length=100,
        help_text=_('Display label shown in forms')
    )
    slug = models.SlugField(
        _('slug'),
        max_length=100,
        help_text=_('JSON key used to store the value (auto-generated from name)')
    )
    field_type = models.CharField(
        _('field type'),
        max_length=20,
        choices=FIELD_TYPES,
        help_text=_('Determines the input widget and validation rules')
    )
    help_text_value = models.CharField(
        _('help text'),
        max_length=255,
        blank=True,
        help_text=_('Hint shown below the field in forms')
    )
    default_value = models.JSONField(
        _('default value'),
        default=None,
        null=True,
        blank=True,
        help_text=_('Default value for new records (JSON format)')
    )
    validation_config = models.JSONField(
        _('validation rules'),
        default=dict,
        blank=True,
        help_text=_(
            'Type-specific validation. '
            'Text: {"min_length": 0, "max_length": 500, "regex": "..."}. '
            'Number: {"min": 0, "max": 9999}. '
            'Select: {"choices": [{"value": "sm", "label": "Small"}, ...]}'
        )
    )
    is_required = models.BooleanField(
        _('required'),
        default=False,
        help_text=_('Whether this field must be filled in')
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Inactive fields are hidden from forms but data is preserved')
    )
    show_on_storefront = models.BooleanField(
        _('show on storefront'),
        default=False,
        help_text=_('Whether this field is visible on the customer-facing storefront')
    )
    is_translatable = models.BooleanField(
        _('translatable'),
        default=False,
        help_text=_('Allow translation of this field value (text/textarea only)')
    )
    sort_order = models.PositiveIntegerField(
        _('sort order'),
        default=0,
        help_text=_('Display order within the group')
    )
    translations = models.JSONField(
        default=dict,
        blank=True,
        help_text=_('Translated field names and help text by language code')
    )
    created_at = models.DateTimeField(_('created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated'), auto_now=True)

    class Meta:
        ordering = ['group__sort_order', 'sort_order', 'name']
        unique_together = ['content_type', 'slug']
        verbose_name = _('custom field definition')
        verbose_name_plural = _('custom field definitions')

    def __str__(self):
        return f"{self.name} ({self.get_field_type_display()}) - {self.content_type}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name).replace('-', '_')
        # Ensure content_type matches group's content_type
        if self.group_id and not self.content_type_id:
            self.content_type = self.group.content_type
        super().save(*args, **kwargs)

    @classmethod
    def get_cached_for_content_type(cls, content_type):
        """Get all active field definitions for a content type, from cache."""
        cache_key = f'{CACHE_KEY_PREFIX}:fields:{content_type.pk}'
        definitions = cache.get(cache_key)
        if definitions is None:
            definitions = list(
                cls.objects.filter(
                    content_type=content_type,
                    is_active=True
                ).select_related('group').order_by(
                    'group__sort_order', 'sort_order', 'name'
                )
            )
            cache.set(cache_key, definitions, CACHE_TTL)
        return definitions

    @classmethod
    def get_cached_for_model(cls, model_class):
        """Get all active field definitions for a model class, from cache."""
        ct = ContentType.objects.get_for_model(model_class)
        return cls.get_cached_for_content_type(ct)

    @classmethod
    def invalidate_cache(cls, content_type):
        """Clear cached definitions for a content type."""
        cache.delete(f'{CACHE_KEY_PREFIX}:fields:{content_type.pk}')
        cache.delete(f'{CACHE_KEY_PREFIX}:groups:{content_type.pk}')

    def get_choices(self):
        """Get choices for select/multiselect fields."""
        if self.field_type in ('select', 'multiselect'):
            return self.validation_config.get('choices', [])
        return []
