"""
Enhanced branding admin interface for comprehensive brand management
"""

from django.contrib import admin
from django.utils.html import mark_safe, format_html
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django import forms
from django.conf import settings
import json

from .theme_models import ThemeBranding


class BrandingAdminForm(forms.ModelForm):
    """Enhanced form for branding with better UI"""

    # Color tokens as individual fields
    primary_color = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'type': 'color', 'style': 'width: 100px; height: 40px;'}),
        help_text='Primary brand color'
    )
    secondary_color = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'type': 'color', 'style': 'width: 100px; height: 40px;'}),
        help_text='Secondary brand color'
    )
    accent_color = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'type': 'color', 'style': 'width: 100px; height: 40px;'}),
        help_text='Accent color for CTAs'
    )
    success_color = forms.CharField(
        required=False,
        initial='#10b981',
        widget=forms.TextInput(attrs={'type': 'color', 'style': 'width: 100px; height: 40px;'}),
        help_text='Success messages and indicators'
    )
    warning_color = forms.CharField(
        required=False,
        initial='#f59e0b',
        widget=forms.TextInput(attrs={'type': 'color', 'style': 'width: 100px; height: 40px;'}),
        help_text='Warning messages'
    )
    error_color = forms.CharField(
        required=False,
        initial='#ef4444',
        widget=forms.TextInput(attrs={'type': 'color', 'style': 'width: 100px; height: 40px;'}),
        help_text='Error messages'
    )

    # Typography
    font_family_heading = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g., Inter, system-ui, sans-serif'}),
        help_text='Font family for headings'
    )
    font_family_body = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g., Inter, system-ui, sans-serif'}),
        help_text='Font family for body text'
    )
    font_size_base = forms.CharField(
        required=False,
        initial='16px',
        widget=forms.TextInput(attrs={'placeholder': 'e.g., 16px'}),
        help_text='Base font size'
    )
    line_height_base = forms.CharField(
        required=False,
        initial='1.5',
        widget=forms.TextInput(attrs={'placeholder': 'e.g., 1.5'}),
        help_text='Base line height'
    )

    # Spacing
    spacing_unit = forms.CharField(
        required=False,
        initial='0.25rem',
        widget=forms.TextInput(attrs={'placeholder': 'e.g., 0.25rem'}),
        help_text='Base spacing unit (multiplied for larger spaces)'
    )

    # Border radius
    border_radius_sm = forms.CharField(
        required=False,
        initial='0.125rem',
        widget=forms.TextInput(attrs={'placeholder': 'e.g., 0.125rem'}),
        help_text='Small border radius'
    )
    border_radius_base = forms.CharField(
        required=False,
        initial='0.25rem',
        widget=forms.TextInput(attrs={'placeholder': 'e.g., 0.25rem'}),
        help_text='Default border radius'
    )
    border_radius_lg = forms.CharField(
        required=False,
        initial='0.5rem',
        widget=forms.TextInput(attrs={'placeholder': 'e.g., 0.5rem'}),
        help_text='Large border radius'
    )

    class Meta:
        model = ThemeBranding
        fields = '__all__'
        widgets = {
            'color_tokens': forms.HiddenInput(),
            'typography_tokens': forms.HiddenInput(),
            'spacing_tokens': forms.HiddenInput(),
            'border_tokens': forms.HiddenInput(),
            'shadow_tokens': forms.Textarea(attrs={'rows': 5, 'style': 'font-family: monospace;'}),
            'animation_tokens': forms.Textarea(attrs={'rows': 5, 'style': 'font-family: monospace;'}),
            'component_overrides': forms.Textarea(attrs={'rows': 10, 'style': 'font-family: monospace;'}),
            'custom_css': forms.Textarea(attrs={'rows': 15, 'class': 'vLargeTextField', 'style': 'font-family: monospace;'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load existing values into individual fields
        if self.instance and self.instance.pk:
            # Colors
            color_tokens = self.instance.color_tokens or {}
            self.fields['primary_color'].initial = color_tokens.get('primary', '#3B82F6')
            self.fields['secondary_color'].initial = color_tokens.get('secondary', '#8B5CF6')
            self.fields['accent_color'].initial = color_tokens.get('accent', '#EC4899')
            self.fields['success_color'].initial = color_tokens.get('success', '#10b981')
            self.fields['warning_color'].initial = color_tokens.get('warning', '#f59e0b')
            self.fields['error_color'].initial = color_tokens.get('error', '#ef4444')

            # Typography
            typography_tokens = self.instance.typography_tokens or {}
            self.fields['font_family_heading'].initial = typography_tokens.get('font-family-heading', '')
            self.fields['font_family_body'].initial = typography_tokens.get('font-family-body', '')
            self.fields['font_size_base'].initial = typography_tokens.get('font-size-base', '16px')
            self.fields['line_height_base'].initial = typography_tokens.get('line-height-base', '1.5')

            # Spacing
            spacing_tokens = self.instance.spacing_tokens or {}
            self.fields['spacing_unit'].initial = spacing_tokens.get('unit', '0.25rem')

            # Borders
            border_tokens = self.instance.border_tokens or {}
            self.fields['border_radius_sm'].initial = border_tokens.get('radius-sm', '0.125rem')
            self.fields['border_radius_base'].initial = border_tokens.get('radius-base', '0.25rem')
            self.fields['border_radius_lg'].initial = border_tokens.get('radius-lg', '0.5rem')

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Save individual fields back to JSON fields
        instance.color_tokens = {
            'primary': self.cleaned_data.get('primary_color', '#3B82F6'),
            'secondary': self.cleaned_data.get('secondary_color', '#8B5CF6'),
            'accent': self.cleaned_data.get('accent_color', '#EC4899'),
            'success': self.cleaned_data.get('success_color', '#10b981'),
            'warning': self.cleaned_data.get('warning_color', '#f59e0b'),
            'error': self.cleaned_data.get('error_color', '#ef4444'),
            'text': '#1F2937',
            'text-light': '#6B7280',
            'background': '#FFFFFF',
            'background-secondary': '#F9FAFB',
            'border': '#E5E7EB',
        }

        instance.typography_tokens = {
            'font-family-heading': self.cleaned_data.get('font_family_heading') or 'Inter, system-ui, sans-serif',
            'font-family-body': self.cleaned_data.get('font_family_body') or 'Inter, system-ui, sans-serif',
            'font-size-base': self.cleaned_data.get('font_size_base', '16px'),
            'font-size-xs': '0.75rem',
            'font-size-sm': '0.875rem',
            'font-size-lg': '1.125rem',
            'font-size-xl': '1.25rem',
            'font-size-2xl': '1.5rem',
            'font-size-3xl': '1.875rem',
            'font-size-4xl': '2.25rem',
            'line-height-base': self.cleaned_data.get('line_height_base', '1.5'),
            'line-height-tight': '1.25',
            'line-height-relaxed': '1.75',
            'font-weight-normal': '400',
            'font-weight-medium': '500',
            'font-weight-semibold': '600',
            'font-weight-bold': '700',
        }

        spacing_unit = self.cleaned_data.get('spacing_unit', '0.25rem')
        instance.spacing_tokens = {
            'unit': spacing_unit,
            '0': '0',
            '1': f'calc({spacing_unit} * 1)',
            '2': f'calc({spacing_unit} * 2)',
            '3': f'calc({spacing_unit} * 3)',
            '4': f'calc({spacing_unit} * 4)',
            '5': f'calc({spacing_unit} * 5)',
            '6': f'calc({spacing_unit} * 6)',
            '8': f'calc({spacing_unit} * 8)',
            '10': f'calc({spacing_unit} * 10)',
            '12': f'calc({spacing_unit} * 12)',
            '16': f'calc({spacing_unit} * 16)',
            '20': f'calc({spacing_unit} * 20)',
            '24': f'calc({spacing_unit} * 24)',
            '32': f'calc({spacing_unit} * 32)',
        }

        instance.border_tokens = {
            'width': '1px',
            'width-2': '2px',
            'width-4': '4px',
            'radius-sm': self.cleaned_data.get('border_radius_sm', '0.125rem'),
            'radius-base': self.cleaned_data.get('border_radius_base', '0.25rem'),
            'radius-lg': self.cleaned_data.get('border_radius_lg', '0.5rem'),
            'radius-xl': '0.75rem',
            'radius-2xl': '1rem',
            'radius-full': '9999px',
        }

        if commit:
            instance.save()
        return instance


@admin.register(ThemeBranding)
class EnhancedBrandingAdmin(admin.ModelAdmin):
    """Enhanced admin interface for branding"""
    form = BrandingAdminForm

    change_form_template = 'admin/design/branding_change_form.html'

    fieldsets = (
        (_('Theme Selection'), {
            'fields': ('theme',),
            'description': 'Select the theme to customize. Leave empty to use default theme.'
        }),
        (_('🎨 Brand Colors'), {
            'fields': (
                ('primary_color', 'secondary_color', 'accent_color'),
                ('success_color', 'warning_color', 'error_color'),
            ),
            'classes': ('wide',),
            'description': 'Define your brand color palette. These colors will be used throughout the theme.'
        }),
        (_('✏️ Typography'), {
            'fields': (
                ('font_family_heading', 'font_family_body'),
                ('font_size_base', 'line_height_base'),
            ),
            'classes': ('wide', 'collapse'),
            'description': 'Customize fonts and text styling.'
        }),
        (_('📐 Layout & Spacing'), {
            'fields': (
                'spacing_unit',
                ('border_radius_sm', 'border_radius_base', 'border_radius_lg'),
            ),
            'classes': ('wide', 'collapse'),
            'description': 'Control spacing and border radius throughout your site.'
        }),
        (_('🎭 Shadows & Effects'), {
            'fields': ('shadow_tokens', 'animation_tokens'),
            'classes': ('collapse',),
            'description': 'Advanced visual effects and animations.'
        }),
        (_('🧩 Component Overrides'), {
            'fields': ('component_overrides',),
            'classes': ('collapse',),
            'description': 'Override specific component styles (JSON format).'
        }),
        (_('🔧 Custom CSS'), {
            'fields': ('custom_css',),
            'classes': ('collapse',),
            'description': 'Add custom CSS for fine-grained control. Use with caution.'
        }),
        (_('Generated Output'), {
            'fields': ('generated_css', 'css_hash'),
            'classes': ('collapse',),
            'description': 'Auto-generated CSS output (read-only).'
        }),
    )

    readonly_fields = ['generated_css', 'css_hash', 'created_at', 'updated_at', 'preview_frame']

    def preview_frame(self, obj):
        """Live preview iframe"""
        if obj.pk:
            preview_url = reverse('design:branding_preview')
            return format_html(
                '<iframe src="{}" style="width: 100%; height: 600px; border: 1px solid #ddd; border-radius: 4px;"></iframe>',
                preview_url
            )
        return "Save to see preview"
    preview_frame.short_description = "Live Preview"

    def save_model(self, request, obj, form, change):
        """Auto-generate CSS on save"""
        super().save_model(request, obj, form, change)
        obj.generate_css()

        # Clear theme cache
        from django.core.cache import cache
        cache.delete_pattern('theme_*')
        cache.delete_pattern('active_theme*')

    def changelist_view(self, request, extra_context=None):
        """Redirect to branding builder"""
        branding = ThemeBranding.objects.first()
        if not branding:
            branding = ThemeBranding.objects.create()

        # Redirect to the visual branding builder
        from django.shortcuts import redirect
        return redirect(f'/theme/branding/{branding.pk}/builder/')

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Redirect to branding builder instead of default form"""
        from django.shortcuts import redirect
        return redirect(f'/theme/branding/{object_id}/builder/')

    def redirect_to_change_form(self, request, pk):
        """Helper to redirect to change form"""
        from django.shortcuts import redirect
        return redirect(f'/admin/design/themebranding/{pk}/change/')

    # Media files are embedded in the template for now
    # class Media:
    #     css = {
    #         'all': ('admin/css/branding.css',)
    #     }
    #     js = ('admin/js/branding.js',)