"""
SMS System Admin.

Provides admin interface for SMS provider accounts, templates, and message tracking.
"""
import json
import logging

from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .models import SMSProviderAccount, SMSTemplate, SMSOutbox
from .services.provider_service import SMSProviderService
from .providers.registry import SMSProviderRegistry

logger = logging.getLogger(__name__)


def get_dynamic_sms_form(provider_key=None):
    """
    Dynamically build a form class based on the provider's credential schema.

    Args:
        provider_key: The provider identifier to build the form for

    Returns:
        A form class with dynamic credential fields
    """

    class DynamicSMSProviderAccountForm(forms.ModelForm):
        """Dynamic form that builds credential fields from provider schema."""

        class Meta:
            model = SMSProviderAccount
            fields = ['display_name', 'provider_key', 'is_active', 'is_default_sms', 'is_default_whatsapp']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            # Determine provider key
            current_provider = provider_key
            if self.instance and self.instance.pk and self.instance.provider_key:
                current_provider = self.instance.provider_key
            elif 'data' in kwargs and kwargs['data']:
                current_provider = kwargs['data'].get('provider_key')

            # Set up provider choices from registry
            providers = SMSProviderRegistry.list_providers()
            provider_choices = [('', _('-- Select Provider --'))]
            for p in providers:
                provider_choices.append((p['key'], p['name']))
            self.fields['provider_key'].widget = forms.Select(choices=provider_choices)

            # Add dynamic credential fields if we have a provider
            if current_provider:
                self._add_credential_fields(current_provider)

        def _add_credential_fields(self, provider_key):
            """Add credential fields dynamically based on provider schema."""
            field_defs = SMSProviderService.build_credential_form_fields(provider_key)

            if not field_defs:
                return

            # Get existing credentials for pre-filling
            existing_creds = {}
            if self.instance and self.instance.pk:
                existing_creds = self.instance.get_credentials()

            for field_name, field_def in field_defs.items():
                field_class = field_def['field_class']
                field_kwargs = {
                    'required': field_def['required'],
                    'label': field_def['label'],
                    'help_text': field_def['help_text'],
                    'widget': field_def['widget'],
                }

                # Set initial value from existing credentials (not secrets)
                schema = SMSProviderService.get_credential_schema(provider_key)
                is_secret = schema.get('properties', {}).get(field_name, {}).get('secret', False)

                if not is_secret and field_name in existing_creds:
                    field_kwargs['initial'] = existing_creds.get(field_name)
                elif field_def.get('initial'):
                    field_kwargs['initial'] = field_def['initial']

                self.fields[f'cred_{field_name}'] = field_class(**field_kwargs)

        def save(self, commit=True):
            instance = super().save(commit=False)
            provider = self.cleaned_data.get('provider_key')

            # Build credentials from dynamic fields
            credentials = {}
            schema = SMSProviderService.get_credential_schema(provider) if provider else {}
            properties = schema.get('properties', {}) if schema else {}

            for field_name in properties.keys():
                form_field_name = f'cred_{field_name}'
                if form_field_name in self.cleaned_data:
                    value = self.cleaned_data.get(form_field_name, '').strip() if self.cleaned_data.get(form_field_name) else ''

                    # For secret fields, only update if a value was provided
                    is_secret = properties.get(field_name, {}).get('secret', False)

                    if value:
                        credentials[field_name] = value
                    elif is_secret and instance.pk:
                        # Keep existing secret value
                        existing_creds = instance.get_credentials()
                        if field_name in existing_creds:
                            credentials[field_name] = existing_creds[field_name]
                    elif not is_secret:
                        credentials[field_name] = value

            instance.set_credentials(credentials)

            if commit:
                instance.save()
            return instance

    return DynamicSMSProviderAccountForm


@admin.register(SMSProviderAccount)
class SMSProviderAccountAdmin(admin.ModelAdmin):
    """Admin for SMS provider accounts with dynamic credential forms."""

    change_list_template = 'admin/sms_system/smsprovideraccount/change_list.html'
    change_form_template = 'admin/sms_system/smsprovideraccount/change_form.html'
    list_display = [
        'display_name',
        'provider_key',
        'is_active_badge',
        'is_default_sms_badge',
        'is_default_whatsapp_badge',
        'connection_status_badge',
        'last_checked',
    ]
    list_filter = ['provider_key', 'is_active', 'is_default_sms', 'is_default_whatsapp', 'connection_status']
    search_fields = ['display_name']
    readonly_fields = ['connection_status', 'last_checked', 'created_at', 'updated_at']

    def get_form(self, request, obj=None, **kwargs):
        """Get dynamic form based on provider."""
        provider_key = None
        if obj:
            provider_key = obj.provider_key
        elif request.GET.get('provider'):
            provider_key = request.GET.get('provider')

        return get_dynamic_sms_form(provider_key)

    def get_fieldsets(self, request, obj=None):
        """Build fieldsets dynamically based on provider."""
        provider_key = None
        if obj:
            provider_key = obj.provider_key

        # Base fieldsets
        fieldsets = [
            (None, {
                'fields': ['display_name', 'provider_key', 'is_active'],
                'classes': ['tab-basic'],
            }),
        ]

        # Add credential fields if we have a provider
        if provider_key:
            credential_schema = SMSProviderService.get_credential_schema(provider_key)
            if credential_schema:
                properties = credential_schema.get('properties', {})
                cred_fields = [f'cred_{name}' for name in properties.keys()]
                if cred_fields:
                    fieldsets.append(
                        (_('Provider Credentials'), {
                            'fields': cred_fields,
                            'description': _('Enter your provider API credentials.'),
                            'classes': ['tab-credentials'],
                        })
                    )
        else:
            # Show instructions if no provider selected
            fieldsets.append(
                (_('Provider Credentials'), {
                    'fields': [],
                    'description': _('Select a provider above to see credential fields, or use the Setup Wizard for a guided experience.'),
                    'classes': ['tab-credentials'],
                })
            )

        # Default settings
        fieldsets.append(
            (_('Default Settings'), {
                'fields': ['is_default_sms', 'is_default_whatsapp'],
                'classes': ['tab-defaults'],
            })
        )

        # Connection status
        fieldsets.append(
            (_('Connection Status'), {
                'fields': ['connection_status', 'last_checked'],
                'classes': ['tab-status'],
            })
        )

        # Timestamps
        fieldsets.append(
            (_('Timestamps'), {
                'fields': ['created_at', 'updated_at'],
                'classes': ['tab-timestamps'],
            })
        )

        return fieldsets

    def changelist_view(self, request, extra_context=None):
        """Add links to wizard and browse in changelist."""
        extra_context = extra_context or {}
        extra_context['wizard_url'] = reverse('sms_system:wizard_step1')
        extra_context['browse_url'] = reverse('sms_system:provider_browse')
        return super().changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Add test connection button to change view."""
        extra_context = extra_context or {}
        extra_context['show_test_connection'] = True
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span class="sms-badge-active">{}</span>', _('Active'))
        return format_html('<span class="sms-badge-inactive">{}</span>', _('Inactive'))
    is_active_badge.short_description = _('Status')
    is_active_badge.admin_order_field = 'is_active'

    def is_default_sms_badge(self, obj):
        if obj.is_default_sms:
            return format_html('<span class="sms-badge-default-sms">{}</span>', _('Default SMS'))
        return '-'
    is_default_sms_badge.short_description = _('SMS')
    is_default_sms_badge.admin_order_field = 'is_default_sms'

    def is_default_whatsapp_badge(self, obj):
        if obj.is_default_whatsapp:
            return format_html('<span class="sms-badge-default-whatsapp">{}</span>', _('Default WhatsApp'))
        return '-'
    is_default_whatsapp_badge.short_description = _('WhatsApp')
    is_default_whatsapp_badge.admin_order_field = 'is_default_whatsapp'

    def connection_status_badge(self, obj):
        css_classes = {
            'success': 'sms-badge-connected',
            'failed': 'sms-badge-failed',
            'untested': 'sms-badge-untested',
        }
        css_class = css_classes.get(obj.connection_status, 'sms-badge-untested')
        return format_html(
            '<span class="{}">{}</span>',
            css_class,
            obj.get_connection_status_display()
        )
    connection_status_badge.short_description = _('Connection')
    connection_status_badge.admin_order_field = 'connection_status'

    class Media:
        css = {
            'all': (
                'core/admin/css/wizard-base.css',
                'sms_system/css/sms_admin_list.css',
            ),
        }


@admin.register(SMSTemplate)
class SMSTemplateAdmin(admin.ModelAdmin):
    """Admin for SMS templates."""

    change_list_template = 'admin/sms_system/smstemplate/change_list.html'
    list_display = ['name', 'template_type', 'is_active', 'updated_at']
    list_filter = ['template_type', 'is_active']
    search_fields = ['name', 'message']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = [
        (None, {
            'fields': ['name', 'template_type', 'is_active'],
        }),
        (_('Message Content'), {
            'fields': ['message'],
            'description': _('Use {variable} syntax for placeholders. Example: "Hello {name}, your order #{order_number} is ready."'),
        }),
        (_('Timestamps'), {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse'],
        }),
    ]


@admin.register(SMSOutbox)
class SMSOutboxAdmin(admin.ModelAdmin):
    """Admin for SMS outbox/delivery tracking."""

    change_list_template = 'admin/sms_system/smsoutbox/change_list.html'
    list_display = ['phone', 'message_type', 'status_badge', 'created_at', 'sent_at']
    list_filter = ['message_type', 'status', 'created_at']
    search_fields = ['phone', 'message', 'provider_message_id']
    readonly_fields = [
        'account', 'template', 'phone', 'message', 'message_type',
        'status', 'provider_message_id', 'error_message', 'retry_count',
        'created_at', 'queued_at', 'sent_at', 'delivered_at',
    ]
    date_hierarchy = 'created_at'
    list_per_page = 50

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        """Add message stats to changelist context."""
        extra_context = extra_context or {}
        qs = SMSOutbox.objects.all()
        extra_context['total_messages'] = qs.count()
        extra_context['sent_count'] = qs.filter(status='sent').count()
        extra_context['delivered_count'] = qs.filter(status='delivered').count()
        extra_context['failed_count'] = qs.filter(status='failed').count()
        return super().changelist_view(request, extra_context=extra_context)

    def status_badge(self, obj):
        css_classes = {
            'pending': 'sms-status-pending',
            'queued': 'sms-status-queued',
            'sent': 'sms-status-sent',
            'delivered': 'sms-status-delivered',
            'failed': 'sms-status-failed',
            'skipped': 'sms-status-skipped',
        }
        css_class = css_classes.get(obj.status, 'sms-status-pending')
        return format_html(
            '<span class="{}">{}</span>',
            css_class,
            obj.get_status_display()
        )
    status_badge.short_description = _('Status')
    status_badge.admin_order_field = 'status'

    class Media:
        css = {
            'all': ('sms_system/css/sms_admin_list.css',),
        }
