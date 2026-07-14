"""
Admin mixins for reusable functionality across Django admin.

This module provides mixins that can be used with any Django ModelAdmin
to add common functionality like translation support, audit logging, etc.

"""

import json


class MoneyFieldCurrencyMixin:
    """
    Mixin for ModelAdmin that sets MoneyField form defaults to the merchant's
    configured default currency instead of hardcoded 'USD'.

    Automatically:
    - Filters currency widget choices to enabled currencies
    - Sets initial currency to site default for new objects

    Usage:
        class MyModelAdmin(MoneyFieldCurrencyMixin, admin.ModelAdmin):
            pass

    For inline admins, use MoneyFieldCurrencyInlineMixin instead.
    """

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        _apply_money_field_currency_defaults(form, obj)
        return form


class MoneyFieldCurrencyInlineMixin:
    """
    Inline version of MoneyFieldCurrencyMixin for TabularInline/StackedInline.
    """

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        _apply_money_field_currency_defaults(formset.form, obj)
        return formset


def _apply_money_field_currency_defaults(form, obj=None):
    """Apply merchant's default currency to all MoneyField widgets in a form.

    For existing objects, ensures the stored currency is always included in the
    dropdown choices — even if it's not in the merchant's enabled currency list.
    This prevents silent currency overwrites when saving.
    """
    from core.utils import get_default_currency
    from core.utils.currency_helpers import get_enabled_currencies

    default_currency = get_default_currency()
    currency_choices = get_enabled_currencies()
    enabled_codes = {code for code, _ in currency_choices}

    for field_name, field in form.base_fields.items():
        if hasattr(field, "widget") and hasattr(field.widget, "widgets"):
            if len(field.widget.widgets) == 2:
                currency_widget = field.widget.widgets[1]
                if hasattr(currency_widget, "choices"):
                    field_choices = list(currency_choices)
                    if obj is not None:
                        # MoneyField stores currency in <field>_currency column
                        stored = getattr(obj, f"{field_name}_currency", None)
                        if stored and stored not in enabled_codes:
                            try:
                                from moneyed import CURRENCIES

                                label = f"{stored} - {CURRENCIES[stored].name}"
                            except (KeyError, ImportError):
                                label = stored
                            field_choices.insert(0, (stored, label))
                    currency_widget.choices = field_choices
                    if obj is None:
                        field.initial = [None, default_currency]


class TranslatableAdminMixin:
    """
    Mixin for Django ModelAdmin classes to add translation support.

    Usage:
        class MyModelAdmin(TranslatableAdminMixin, admin.ModelAdmin):
            translatable_fields = ['field1', 'field2']  # Fields that can be translated

            class Media:
                js = TranslatableAdminMixin.Media.js
                css = TranslatableAdminMixin.Media.css

    The mixin provides:
    - Translation editor assets (JS/CSS) in admin forms
    - Available languages data for the translation editor
    - Helper methods for translation management
    """

    # Fields that can be translated (override in subclass)
    translatable_fields: list[str] = []

    class Media:
        """
        Media assets required for translation functionality.
        Include these in your ModelAdmin's Media class.
        """

        js = (
            # Translation Editor utility (using symlink to current version)
            "utilities/translation_editor/current/translation_editor.js",
        )
        css = {"all": ("utilities/translation_editor/current/translation_editor.css",)}

    def get_translatable_fields(self, request, obj=None):
        """
        Get list of fields that can be translated.
        Override this method for dynamic field determination.

        Args:
            request: HTTP request object
            obj: Model instance (None for add view)

        Returns:
            List of field names that can be translated
        """
        return self.translatable_fields

    def get_available_languages_json(self, request, obj=None):
        """
        Get available languages as JSON for use in templates.

        This method fetches languages from the translation service
        and formats them for JavaScript consumption.

        Args:
            request: HTTP request object
            obj: Model instance (None for add view)

        Returns:
            JSON string of available languages
        """
        try:
            from page_builder.translation_utils import get_available_languages, get_primary_language

            languages = get_available_languages()
            primary = get_primary_language()

            # Format for JavaScript
            lang_list = [
                {"code": code, "name": str(name), "is_primary": code == primary}
                for code, name in languages
                if code != primary  # Exclude primary from translation targets
            ]

            return json.dumps(lang_list)

        except Exception:
            # Return empty array if translation service unavailable
            return json.dumps([])

    def get_translation_model_type(self, request, obj=None):
        """
        Get the model type identifier for translation API endpoints.

        Returns format: 'app_label.model_name' (e.g., 'core.sitesettings')

        Args:
            request: HTTP request object
            obj: Model instance (None for add view)

        Returns:
            String identifying the model type
        """
        model = self.model
        return f"{model._meta.app_label}.{model._meta.model_name}"

    def get_translation_object_id(self, request, obj=None):
        """
        Get the object ID for translation API endpoints.

        Args:
            request: HTTP request object
            obj: Model instance (None for add view)

        Returns:
            Primary key of the object, or None if not yet saved
        """
        if obj and obj.pk:
            return obj.pk
        return None

    def change_view(self, request, object_id, form_url="", extra_context=None):
        """
        Override change view to inject translation context.

        This adds translation-related data to the template context
        that can be used by the translation editor JavaScript.
        """
        extra_context = extra_context or {}

        # Get the object
        obj = self.get_object(request, object_id)

        # Add translation context
        extra_context["translatable_fields"] = json.dumps(
            self.get_translatable_fields(request, obj)
        )
        extra_context["available_languages_json"] = self.get_available_languages_json(request, obj)
        extra_context["translation_model_type"] = self.get_translation_model_type(request, obj)
        extra_context["translation_object_id"] = self.get_translation_object_id(request, obj)
        extra_context["has_translation_support"] = True

        return super().change_view(request, object_id, form_url, extra_context)

    def add_view(self, request, form_url="", extra_context=None):
        """
        Override add view to inject translation context.

        Note: Translation is typically only available for existing objects,
        but this ensures the context is available if needed.
        """
        extra_context = extra_context or {}

        # Add translation context (object_id will be None for add view)
        extra_context["translatable_fields"] = json.dumps(
            self.get_translatable_fields(request, None)
        )
        extra_context["available_languages_json"] = self.get_available_languages_json(request, None)
        extra_context["translation_model_type"] = self.get_translation_model_type(request, None)
        extra_context["translation_object_id"] = None
        extra_context["has_translation_support"] = False  # Disable for new objects

        return super().add_view(request, form_url, extra_context)
