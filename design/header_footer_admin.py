"""
Admin interfaces for header, footer, and menu management
"""

from django.contrib import admin, messages
from django.utils.html import mark_safe, format_html
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django import forms
from django.db import models

from .header_footer_models import (
    HeaderTemplate, FooterTemplate, Widget,
    WidgetPlacement, Menu, MenuItem
)
from core.widgets import IconPickerWidget


class WidgetPlacementInline(admin.TabularInline):
    """Inline for widget placements"""
    model = WidgetPlacement
    extra = 1
    fields = ['widget', 'zone', 'order', 'is_active']
    autocomplete_fields = ['widget']


@admin.register(HeaderTemplate)
class HeaderTemplateAdmin(admin.ModelAdmin):
    """Admin for header templates"""
    list_display = [
        'name', 'slug', 'layout_type', 'is_sticky',
        'is_active', 'is_default', 'preview_link'
    ]
    list_filter = ['layout_type', 'is_sticky', 'is_active', 'is_default']
    search_fields = ['name', 'slug', 'description']
    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'slug', 'description')
        }),
        (_('Layout'), {
            'fields': (
                'layout_type', 'is_sticky', 'sticky_offset',
                'has_top_bar', 'top_bar_content'
            )
        }),
        (_('Mobile Settings'), {
            'fields': ('mobile_layout',),
            'classes': ('collapse',)
        }),
        (_('Styling'), {
            'fields': ('css_classes', 'custom_css'),
            'classes': ('collapse',)
        }),
        (_('Status'), {
            'fields': ('is_active', 'is_default')
        })
    )

    inlines = [WidgetPlacementInline]

    def get_urls(self):
        """Add custom admin URLs for unified header management"""
        from django.urls import path
        from .unified_header_footer_views import unified_header_management_view

        urls = super().get_urls()
        custom_urls = [
            path('unified/', unified_header_management_view, name='unified_header_management'),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        """Redirect to unified header management view"""
        from django.shortcuts import redirect
        return redirect('admin:unified_header_management')

    def preview_link(self, obj):
        """Preview link for header"""
        url = reverse('design:preview_header', args=[obj.pk])
        return format_html(
            '<a href="{}" target="_blank" class="button">Preview</a>',
            url
        )
    preview_link.short_description = 'Preview'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(FooterTemplate)
class FooterTemplateAdmin(admin.ModelAdmin):
    """Admin for footer templates"""
    list_display = [
        'name', 'slug', 'layout_type', 'column_count',
        'is_active', 'is_default', 'preview_link'
    ]
    list_filter = ['layout_type', 'is_active', 'is_default']
    search_fields = ['name', 'slug', 'description']
    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'slug', 'description')
        }),
        (_('Layout'), {
            'fields': (
                'layout_type', 'column_count',
                'has_bottom_bar', 'bottom_bar_content'
            )
        }),
        (_('Styling'), {
            'fields': (
                'background_color', 'text_color',
                'css_classes', 'custom_css'
            ),
            'classes': ('collapse',)
        }),
        (_('Status'), {
            'fields': ('is_active', 'is_default')
        })
    )

    inlines = [WidgetPlacementInline]

    def get_urls(self):
        """Add custom admin URLs for unified footer management"""
        from django.urls import path
        from .unified_header_footer_views import unified_footer_management_view

        urls = super().get_urls()
        custom_urls = [
            path('unified/', unified_footer_management_view, name='unified_footer_management'),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        """Redirect to unified footer management view"""
        from django.shortcuts import redirect
        return redirect('admin:unified_footer_management')

    def preview_link(self, obj):
        """Preview link for footer"""
        url = reverse('design:preview_footer', args=[obj.pk])
        return format_html(
            '<a href="{}" target="_blank" class="button">Preview</a>',
            url
        )
    preview_link.short_description = 'Preview'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class WidgetAdminForm(forms.ModelForm):
    """Custom form for widget admin with JSON field widgets"""

    class Meta:
        model = Widget
        fields = '__all__'
        widgets = {
            'config': forms.Textarea(attrs={'rows': 10, 'style': 'font-family: monospace;'}),
            'visibility_rules': forms.Textarea(attrs={'rows': 5, 'style': 'font-family: monospace;'}),
            'content': forms.Textarea(attrs={'rows': 10, 'class': 'vLargeTextField'}),
        }


@admin.register(Widget)
class WidgetAdmin(admin.ModelAdmin):
    """Admin for widgets"""
    form = WidgetAdminForm
    list_display = [
        'name', 'widget_type', 'visibility_summary',
        'is_active', 'usage_count'
    ]
    list_filter = [
        'widget_type', 'is_active',
        'show_on_mobile', 'show_on_tablet', 'show_on_desktop'
    ]
    search_fields = ['name', 'content']

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'widget_type')
        }),
        (_('Configuration'), {
            'fields': ('config', 'content'),
            'description': 'Configuration varies by widget type. See documentation for each type.'
        }),
        (_('Visibility'), {
            'fields': (
                ('show_on_mobile', 'show_on_tablet', 'show_on_desktop'),
                'visibility_rules'
            ),
            'classes': ('collapse',)
        }),
        (_('Styling'), {
            'fields': ('css_classes', 'custom_css'),
            'classes': ('collapse',)
        }),
        (_('Performance'), {
            'fields': ('cache_duration',),
            'classes': ('collapse',)
        }),
        (_('Status'), {
            'fields': ('is_active',)
        })
    )

    def visibility_summary(self, obj):
        """Show device visibility summary with Font Awesome icons"""
        devices = []
        if obj.show_on_mobile:
            devices.append('<i class="fas fa-mobile-alt" title="%s"></i>' % _('Mobile'))
        if obj.show_on_tablet:
            devices.append('<i class="fas fa-tablet-alt" title="%s"></i>' % _('Tablet'))
        if obj.show_on_desktop:
            devices.append('<i class="fas fa-desktop" title="%s"></i>' % _('Desktop'))

        if devices:
            return format_html(' '.join(devices))
        return format_html('<i class="fas fa-times-circle" style="color: var(--error-color);" title="%s"></i>' % _('None'))
    visibility_summary.short_description = _('Devices')

    def usage_count(self, obj):
        """Count how many times this widget is used"""
        count = obj.placements.count()
        if count > 0:
            return format_html('<strong>{}</strong>', count)
        return format_html('<span style="color: var(--body-quiet-color);">{}</span>', count)
    usage_count.short_description = _('Used In')

    def changelist_view(self, request, extra_context=None):
        """Add widget types to context for filter dropdown"""
        extra_context = extra_context or {}
        from .header_footer_models import Widget
        extra_context['widget_types'] = Widget.WIDGET_TYPES
        return super().changelist_view(request, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class MenuItemInline(admin.TabularInline):
    """Inline for menu items"""
    model = MenuItem
    extra = 1
    fields = ['title', 'url', 'parent', 'order', 'is_active']
    ordering = ['order', 'title']


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    """Admin for menus"""
    list_display = ['name', 'slug', 'location', 'display_type', 'item_count', 'is_active', 'edit_items_link']
    list_filter = ['location', 'display_type', 'is_active']
    search_fields = ['name', 'slug', 'description']
    prepopulated_fields = {'slug': ('name',)}

    # Custom change list template
    change_list_template = 'admin/design/menu/change_list.html'

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'slug', 'description')
        }),
        (_('Configuration'), {
            'fields': ('location', 'display_type')
        }),
        (_('Styling'), {
            'fields': ('css_classes', 'custom_css'),
            'classes': ('collapse',)
        }),
        (_('Status'), {
            'fields': ('is_active',)
        })
    )

    inlines = [MenuItemInline]

    def changelist_view(self, request, extra_context=None):
        """Add statistics to the change list context"""
        extra_context = extra_context or {}

        # Calculate statistics
        total_menus = Menu.objects.count()
        active_menus = Menu.objects.filter(is_active=True).count()
        total_items = MenuItem.objects.count()

        # Count unique locations used
        locations_used = Menu.objects.filter(is_active=True).values('location').distinct().count()

        extra_context['stats'] = {
            'total_menus': total_menus,
            'active_menus': active_menus,
            'total_items': total_items,
            'locations_used': locations_used,
        }

        return super().changelist_view(request, extra_context=extra_context)

    def item_count(self, obj):
        """Count menu items"""
        return obj.items.count()
    item_count.short_description = 'Items'

    def edit_items_link(self, obj):
        """Link to edit menu structure"""
        url = reverse('design:menu_builder', args=[obj.pk])
        return format_html(
            '<a href="{}" class="button">Build Menu</a>',
            url
        )
    edit_items_link.short_description = 'Actions'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    """Admin for individual menu items"""
    list_display = ['title', 'menu', 'parent', 'url', 'order', 'is_active', 'has_children']
    list_filter = ['menu', 'is_active']
    search_fields = ['title', 'url']
    list_editable = ['order', 'is_active']

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'icon':
            return forms.CharField(
                widget=IconPickerWidget(
                    priority_icons=[
                        'fa-house', 'fa-store', 'fa-tag', 'fa-bars',
                        'fa-link', 'fa-arrow-right', 'fa-star',
                        'fa-circle-info', 'fa-phone', 'fa-envelope',
                    ],
                    style_prefix=True,
                ),
                required=False,
            )
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('menu', 'parent', 'title', 'url', 'target')
        }),
        (_('Appearance'), {
            'fields': ('icon', 'badge_text', 'badge_color', 'css_classes'),
            'classes': ('collapse',)
        }),
        (_('Mega Menu'), {
            'fields': ('mega_menu_content',),
            'classes': ('collapse',),
            'description': 'Configuration for mega menu layout (if applicable)'
        }),
        (_('Order & Status'), {
            'fields': ('order', 'is_active')
        })
    )

    def has_children(self, obj):
        """Check if item has children"""
        return obj.has_children()
    has_children.boolean = True
    has_children.short_description = 'Has Sub-items'