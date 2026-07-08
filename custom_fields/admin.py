"""
Admin registration for Custom Fields management.

The main management is done through a custom view (management page),
not through the standard Django admin changelist.
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import CustomFieldGroup, CustomFieldDefinition


@admin.register(CustomFieldGroup)
class CustomFieldGroupAdmin(admin.ModelAdmin):
    """Admin for custom field groups (primarily for debugging - merchants use the management page)."""
    list_display = ['name', 'content_type', 'sort_order', 'is_active', 'show_on_storefront']
    list_filter = ['content_type', 'is_active']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

    def has_module_permission(self, request):
        # Hide from admin index - merchants use the custom management page
        return False


@admin.register(CustomFieldDefinition)
class CustomFieldDefinitionAdmin(admin.ModelAdmin):
    """Admin for custom field definitions (primarily for debugging)."""
    list_display = ['name', 'slug', 'field_type', 'group', 'content_type', 'is_required', 'is_active']
    list_filter = ['content_type', 'field_type', 'is_active', 'is_required']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

    def has_module_permission(self, request):
        # Hide from admin index - merchants use the custom management page
        return False
