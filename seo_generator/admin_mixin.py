"""
Admin mixin for SEO generation functionality.

Adds "Regenerate SEO" button to admin change forms for models with SEO fields.
"""

from django.contrib import admin
from django.utils.html import format_html


# Field names that identify an SEO fieldset (core meta fields only, not og_image
# which may appear in a separate Media fieldset)
SEO_FIELD_NAMES = {'meta_title', 'meta_description', 'meta_keywords'}


class SEOGeneratorAdminMixin:
    """
    Mixin for Django admin classes to add SEO generation functionality.

    Usage:
        class MyModelAdmin(SEOGeneratorAdminMixin, admin.ModelAdmin):
            ...

    This adds:
    - "Regenerate SEO" button in admin change form
    - JavaScript and CSS for SEO generation UI
    - Auto-generation support via seo_auto_generated field
    """

    # Add seo_auto_generated to fieldsets if present
    def get_fieldsets(self, request, obj=None):
        """Add seo_auto_generated field to SEO fieldset if it exists."""
        fieldsets = super().get_fieldsets(request, obj)

        # Look for SEO fieldset by checking if it contains SEO-related fields
        new_fieldsets = []
        for name, data in fieldsets:
            fields = list(data.get('fields', []))
            # Flatten nested tuples for field name checking
            flat_fields = set()
            for f in fields:
                if isinstance(f, (list, tuple)):
                    flat_fields.update(f)
                else:
                    flat_fields.add(f)

            if flat_fields & SEO_FIELD_NAMES:
                if 'seo_auto_generated' not in flat_fields and hasattr(self.model, 'seo_auto_generated'):
                    fields.append('seo_auto_generated')
                    data = dict(data)
                    data['fields'] = tuple(fields)
            new_fieldsets.append((name, data))

        return new_fieldsets

    class Media:
        """Include SEO generation assets."""
        js = (
            'seo_generator/admin/seo_generator.js',
        )
        css = {
            'all': (
                'seo_generator/admin/seo_generator.css',
            )
        }
