from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from core.widgets import IconPickerWidget

from .models import CustomElement
from .registry import BINDABLE_MODELS


@admin.register(CustomElement)
class CustomElementAdmin(admin.ModelAdmin):
    """
    Admin for custom elements with card-based list template.
    Uses a custom change_list_template with AJAX filtering.
    """

    change_list_template = "admin/element_builder/customelement/change_list.html"
    list_display = ["name", "target_model_display", "icon_display", "is_active", "updated_at"]
    list_filter = ["is_active", "target_model", "category"]
    search_fields = ["name", "slug", "description"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        (
            None,
            {
                "fields": ("name", "slug", "description"),
            },
        ),
        (
            _("Data Binding"),
            {
                "fields": ("target_model",),
                "description": _("Select which model this element will display data from."),
            },
        ),
        (
            _("Appearance"),
            {
                "fields": ("icon", "category"),
            },
        ),
        (
            _("Status"),
            {
                "fields": ("is_active",),
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == "icon":
            from django import forms

            return forms.CharField(
                widget=IconPickerWidget(
                    priority_icons=[
                        "fa-puzzle-piece",
                        "fa-cube",
                        "fa-code",
                        "fa-palette",
                        "fa-wand-magic-wand",
                        "fa-layer-group",
                        "fa-image",
                        "fa-table",
                        "fa-list",
                    ],
                    style_prefix=True,
                ),
                required=False,
                initial="fas fa-puzzle-piece",
            )
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def target_model_display(self, obj):
        """Display human-readable model name with icon."""
        if not obj.target_model:
            return format_html('<i class="fas fa-cube"></i> {}', _("None (Static)"))
        model_config = BINDABLE_MODELS.get(obj.target_model, {})
        label = model_config.get("label", obj.target_model)
        icon = model_config.get("icon", "fas fa-database")
        return format_html('<i class="{}"></i> {}', icon, label)

    target_model_display.short_description = _("Target Model")
    target_model_display.admin_order_field = "target_model"

    def icon_display(self, obj):
        """Display the element icon."""
        return format_html('<i class="{}"></i>', obj.icon)

    icon_display.short_description = _("Icon")

    def changelist_view(self, request, extra_context=None):
        """Add context for the change list template."""
        extra_context = extra_context or {}
        extra_context["bindable_models"] = BINDABLE_MODELS
        extra_context["title"] = _("Custom Elements")
        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        """Add custom admin URLs for the visual builder."""
        from django.urls import path

        from . import admin_views

        urls = super().get_urls()
        custom_urls = [
            path(
                "add/",
                self.admin_site.admin_view(admin_views.quick_add_view),
                name="element_builder_customelement_add",
            ),
            path(
                "<int:pk>/builder/",
                self.admin_site.admin_view(admin_views.visual_builder_view),
                name="element_builder_customelement_builder",
            ),
            path(
                "search-items/",
                self.admin_site.admin_view(admin_views.search_model_items),
                name="element_builder_search_items",
            ),
        ]
        return custom_urls + urls
