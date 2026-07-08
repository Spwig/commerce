from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


class CustomElement(models.Model):
    """
    A merchant-created custom UI element built from page builder primitives.
    Elements can be bound to model fields for dynamic data display.
    """
    name = models.CharField(
        _('Name'),
        max_length=100,
        help_text=_('Display name for the custom element')
    )
    slug = models.SlugField(
        _('Slug'),
        max_length=100,
        unique=True,
        help_text=_('URL-friendly identifier')
    )
    description = models.TextField(
        _('Description'),
        blank=True,
        help_text=_('Optional description of what this element displays')
    )

    # Target model for data binding (empty = static element with no model binding)
    target_model = models.CharField(
        _('Target Model'),
        max_length=100,
        blank=True,
        help_text=_('Model to bind data from (e.g., "catalog.Product"). Leave empty for static elements.')
    )

    # Root element - links to page_builder Element tree
    root_element = models.OneToOneField(
        'page_builder.Element',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='custom_element_definition',
        help_text=_('Root element of the custom element tree')
    )

    # Metadata for display in element library
    icon = models.CharField(
        _('Icon'),
        max_length=50,
        default='fas fa-puzzle-piece',
        help_text=_('Font Awesome icon class')
    )
    category = models.CharField(
        _('Category'),
        max_length=50,
        default='custom',
        help_text=_('Category for grouping in element library')
    )

    is_active = models.BooleanField(
        _('Active'),
        default=True,
        help_text=_('Whether this element is available for use')
    )

    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated'), auto_now=True)

    class Meta:
        verbose_name = _('Custom Element')
        verbose_name_plural = _('Custom Elements')
        ordering = ['name']
        indexes = [
            models.Index(fields=['target_model']),
            models.Index(fields=['is_active']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_target_model_label(self):
        """Get human-readable label for the target model."""
        if not self.target_model:
            return _('None (Static Element)')
        from .registry import BINDABLE_MODELS
        model_config = BINDABLE_MODELS.get(self.target_model, {})
        return model_config.get('label', self.target_model)


class ElementBinding(models.Model):
    """
    Configures data binding for elements within a CustomElement.
    Maps page_builder Element content fields to model instance fields.
    """
    custom_element = models.ForeignKey(
        CustomElement,
        on_delete=models.CASCADE,
        related_name='bindings',
        verbose_name=_('Custom Element')
    )
    element = models.ForeignKey(
        'page_builder.Element',
        on_delete=models.CASCADE,
        related_name='data_bindings',
        verbose_name=_('Element')
    )
    # The content field in the element to bind (e.g., 'text', 'src', 'url')
    content_field = models.CharField(
        _('Content Field'),
        max_length=50,
        help_text=_('Element content field to bind data to (e.g., "text", "src")')
    )
    # The model field to get data from (e.g., 'name', 'price', 'thumbnail')
    model_field = models.CharField(
        _('Model Field'),
        max_length=100,
        help_text=_('Model field to bind data from (e.g., "name", "get_price")')
    )
    # Optional thumbnail preset for image fields
    thumbnail_preset = models.CharField(
        _('Thumbnail Preset'),
        max_length=50,
        blank=True,
        help_text=_('Thumbnail preset for image fields (e.g., "thumbnail", "medium")')
    )

    class Meta:
        verbose_name = _('Element Binding')
        verbose_name_plural = _('Element Bindings')
        unique_together = ['custom_element', 'element', 'content_field']
        indexes = [
            models.Index(fields=['custom_element']),
        ]

    def __str__(self):
        return f'{self.element.element_type}.{self.content_field} → {self.model_field}'
