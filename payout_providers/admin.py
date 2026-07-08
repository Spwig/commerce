"""
Payout Provider Admin Interface
"""

import json
import logging
from django.contrib import admin
from django.http import JsonResponse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.urls import reverse, path
from django.contrib import messages
from django.views.decorators.http import require_POST

from .models import PayoutProviderAccount, PayoutWebhookLog

logger = logging.getLogger(__name__)


@admin.register(PayoutProviderAccount)
class PayoutProviderAccountAdmin(admin.ModelAdmin):
    """Admin interface for payout provider accounts"""

    list_display = (
        'name', 'provider_type_display', 'connection_status_badge',
        'is_active_badge', 'is_default_badge', 'last_tested_at', 'updated_at'
    )
    list_filter = ('provider_type', 'is_active', 'is_default', 'connection_status')
    search_fields = ('name',)
    readonly_fields = ('connection_status', 'last_tested_at', 'last_error_message', 'created_at', 'updated_at')

    fieldsets = (
        (_('Provider Information'), {
            'fields': ('provider_type', 'name', 'component')
        }),
        (_('Status'), {
            'fields': ('is_active', 'is_default')
        }),
        (_('Connection Status'), {
            'fields': ('connection_status', 'last_tested_at', 'last_error_message'),
            'classes': ('collapse',)
        }),
        (_('Configuration'), {
            'fields': ('supported_methods', 'settings'),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['test_connection_action']

    def changelist_view(self, request, extra_context=None):
        """Add context data for the changelist view"""
        from django.db.models import Count

        extra_context = extra_context or {}
        extra_context['browse_url'] = reverse('payout_providers:provider_browse')
        extra_context['wizard_url'] = reverse('payout_providers:wizard_step1')

        # Get counts for filters
        qs = self.get_queryset(request)

        # Active/Inactive counts
        extra_context['active_count'] = qs.filter(is_active=True).count()
        extra_context['inactive_count'] = qs.filter(is_active=False).count()

        # Connection status counts
        extra_context['connected_count'] = qs.filter(connection_status='connected').count()
        extra_context['failed_count'] = qs.filter(connection_status='failed').count()
        extra_context['untested_count'] = qs.filter(connection_status='untested').count()

        # Provider type counts
        provider_type_counts = []
        type_counts = qs.values('provider_type').annotate(count=Count('id'))
        for item in type_counts:
            provider_type_counts.append({
                'type': item['provider_type'],
                'name': dict(PayoutProviderAccount.PROVIDER_CHOICES).get(
                    item['provider_type'], item['provider_type']
                ),
                'count': item['count']
            })
        extra_context['provider_type_counts'] = provider_type_counts

        return super().changelist_view(request, extra_context=extra_context)

    def provider_type_display(self, obj):
        """Display provider type with icon"""
        icons = {
            'paypal': ('fab', 'fa-paypal'),
            'airwallex': ('fas', 'fa-university'),
            'wise': ('fas', 'fa-exchange-alt'),
        }
        icon_prefix, icon_name = icons.get(obj.provider_type, ('fas', 'fa-money-bill-transfer'))
        return format_html(
            '<span><i class="{} {}"></i> {}</span>',
            icon_prefix, icon_name, obj.get_provider_type_display()
        )
    provider_type_display.short_description = _('Provider')
    provider_type_display.admin_order_field = 'provider_type'

    def connection_status_badge(self, obj):
        """Display connection status with colored badge"""
        colors = {
            'untested': 'secondary',
            'connected': 'success',
            'failed': 'danger',
            'invalid_credentials': 'warning'
        }
        icons = {
            'untested': 'fa-question-circle',
            'connected': 'fa-check-circle',
            'failed': 'fa-times-circle',
            'invalid_credentials': 'fa-exclamation-triangle'
        }
        color = colors.get(obj.connection_status, 'secondary')
        icon = icons.get(obj.connection_status, 'fa-circle')
        return format_html(
            '<span class="badge badge-{}"><i class="fas {}"></i> {}</span>',
            color, icon, obj.get_connection_status_display()
        )
    connection_status_badge.short_description = _('Connection')

    def is_active_badge(self, obj):
        """Display active status as badge"""
        if obj.is_active:
            return format_html('<span class="badge badge-success">{}</span>', _('Active'))
        return format_html('<span class="badge badge-secondary">{}</span>', _('Inactive'))
    is_active_badge.short_description = _('Active')
    is_active_badge.admin_order_field = 'is_active'

    def is_default_badge(self, obj):
        """Display default status as badge"""
        if obj.is_default:
            return format_html('<span class="badge badge-primary">{}</span>', _('Default'))
        return format_html('<span class="badge badge-secondary">-</span>')
    is_default_badge.short_description = _('Default')
    is_default_badge.admin_order_field = 'is_default'

    @admin.action(description=_('Test connection for selected providers'))
    def test_connection_action(self, request, queryset):
        """Test connection for selected provider accounts"""
        success_count = 0
        fail_count = 0

        for account in queryset:
            result = account.test_connection()
            if result.get('success'):
                success_count += 1
            else:
                fail_count += 1

        if success_count:
            self.message_user(
                request,
                _('Successfully connected to %(count)d provider(s).') % {'count': success_count},
                messages.SUCCESS
            )
        if fail_count:
            self.message_user(
                request,
                _('Failed to connect to %(count)d provider(s). Check error messages.') % {'count': fail_count},
                messages.ERROR
            )

    def get_urls(self):
        """Add custom AJAX action URLs"""
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:provider_id>/toggle-active/',
                self.admin_site.admin_view(self.toggle_active_view),
                name='payout_providers_payoutprovideraccount_toggle_active'
            ),
            path(
                '<int:provider_id>/set-default/',
                self.admin_site.admin_view(self.set_default_view),
                name='payout_providers_payoutprovideraccount_set_default'
            ),
            path(
                '<int:provider_id>/test-connection/',
                self.admin_site.admin_view(self.test_connection_view),
                name='payout_providers_payoutprovideraccount_test_connection'
            ),
            path(
                'bulk-action/',
                self.admin_site.admin_view(self.bulk_action_view),
                name='payout_providers_payoutprovideraccount_bulk_action'
            ),
        ]
        return custom_urls + urls

    def toggle_active_view(self, request, provider_id):
        """Toggle provider active status via AJAX"""
        if request.method != 'POST':
            return JsonResponse({'success': False, 'message': 'POST required'}, status=405)

        try:
            provider = PayoutProviderAccount.objects.get(pk=provider_id)
            provider.is_active = not provider.is_active
            provider.save(update_fields=['is_active'])

            return JsonResponse({
                'success': True,
                'is_active': provider.is_active,
                'message': _('Provider {} successfully.').format(
                    _('enabled') if provider.is_active else _('disabled')
                )
            })
        except PayoutProviderAccount.DoesNotExist:
            return JsonResponse({'success': False, 'message': _('Provider not found')}, status=404)
        except Exception:
            logger.exception('Error toggling provider %s active status', provider_id)
            return JsonResponse({'success': False, 'message': _('An unexpected error occurred.')}, status=500)

    def set_default_view(self, request, provider_id):
        """Set provider as default via AJAX"""
        if request.method != 'POST':
            return JsonResponse({'success': False, 'message': 'POST required'}, status=405)

        try:
            provider = PayoutProviderAccount.objects.get(pk=provider_id)

            # Clear other defaults for the same provider type
            PayoutProviderAccount.objects.filter(
                provider_type=provider.provider_type,
                is_default=True
            ).update(is_default=False)

            # Set this one as default
            provider.is_default = True
            provider.save(update_fields=['is_default'])

            return JsonResponse({
                'success': True,
                'message': _('%(name)s set as default provider.') % {'name': provider.name}
            })
        except PayoutProviderAccount.DoesNotExist:
            return JsonResponse({'success': False, 'message': _('Provider not found')}, status=404)
        except Exception:
            logger.exception('Error setting provider %s as default', provider_id)
            return JsonResponse({'success': False, 'message': _('An unexpected error occurred.')}, status=500)

    def test_connection_view(self, request, provider_id):
        """Test provider connection via AJAX"""
        if request.method != 'POST':
            return JsonResponse({'success': False, 'message': 'POST required'}, status=405)

        try:
            provider = PayoutProviderAccount.objects.get(pk=provider_id)
            result = provider.test_connection()

            if result.get('success'):
                return JsonResponse({
                    'success': True,
                    'message': result.get('message', _('Connection test successful!'))
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': result.get('error', _('Connection test failed'))
                })
        except PayoutProviderAccount.DoesNotExist:
            return JsonResponse({'success': False, 'message': _('Provider not found')}, status=404)
        except Exception:
            logger.exception('Error testing connection for provider %s', provider_id)
            return JsonResponse({'success': False, 'message': _('An unexpected error occurred.')}, status=500)

    def bulk_action_view(self, request):
        """Handle bulk actions via AJAX"""
        if request.method != 'POST':
            return JsonResponse({'success': False, 'message': 'POST required'}, status=405)

        try:
            data = json.loads(request.body)
            action = data.get('action')
            provider_ids = data.get('provider_ids', [])

            if not action or not provider_ids:
                return JsonResponse({
                    'success': False,
                    'message': _('Action and provider IDs required')
                }, status=400)

            providers = PayoutProviderAccount.objects.filter(pk__in=provider_ids)
            count = providers.count()

            if action == 'enable':
                providers.update(is_active=True)
                message = _('%(count)d provider(s) enabled.') % {'count': count}

            elif action == 'disable':
                providers.update(is_active=False)
                message = _('%(count)d provider(s) disabled.') % {'count': count}

            elif action == 'set_default':
                if count != 1:
                    return JsonResponse({
                        'success': False,
                        'message': _('Select exactly one provider to set as default')
                    }, status=400)
                target_provider = providers.first()
                PayoutProviderAccount.objects.filter(
                    provider_type=target_provider.provider_type,
                    is_default=True
                ).update(is_default=False)
                providers.update(is_default=True)
                message = _('Default provider updated.')

            elif action == 'test_connection':
                success_count = 0
                fail_count = 0
                for provider in providers:
                    result = provider.test_connection()
                    if result.get('success'):
                        success_count += 1
                    else:
                        fail_count += 1
                message = _('Tested %(count)d provider(s): %(success)d succeeded, %(fail)d failed.') % {
                    'count': count,
                    'success': success_count,
                    'fail': fail_count
                }

            elif action == 'delete':
                if not request.user.has_perm('payout_providers.delete_payoutprovideraccount'):
                    return JsonResponse({
                        'success': False,
                        'message': _('You do not have permission to delete providers.')
                    }, status=403)
                providers.delete()
                message = _('%(count)d provider(s) deleted.') % {'count': count}

            else:
                return JsonResponse({
                    'success': False,
                    'message': _('Unknown action: %(action)s') % {'action': action}
                }, status=400)

            return JsonResponse({'success': True, 'message': message})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': _('Invalid request data.')}, status=400)
        except Exception:
            logger.exception('Error processing bulk action')
            return JsonResponse({'success': False, 'message': _('An unexpected error occurred.')}, status=500)


@admin.register(PayoutWebhookLog)
class PayoutWebhookLogAdmin(admin.ModelAdmin):
    """Admin interface for webhook logs"""

    list_display = (
        'received_at', 'provider_type', 'event_type', 'payout_reference',
        'signature_valid_badge', 'processed_badge'
    )
    list_filter = ('provider_type', 'event_type', 'signature_valid', 'processed', 'received_at')
    search_fields = ('event_id', 'payout_reference', 'event_type')
    readonly_fields = (
        'provider_account', 'provider_type', 'event_type', 'event_id',
        'payload', 'headers', 'signature_valid', 'processed',
        'processing_error', 'payout_reference', 'received_at', 'processed_at'
    )
    date_hierarchy = 'received_at'

    fieldsets = (
        (_('Event Information'), {
            'fields': ('provider_account', 'provider_type', 'event_type', 'event_id', 'payout_reference')
        }),
        (_('Status'), {
            'fields': ('signature_valid', 'processed', 'processing_error')
        }),
        (_('Payload'), {
            'fields': ('payload', 'headers'),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('received_at', 'processed_at')
        }),
    )

    def signature_valid_badge(self, obj):
        """Display signature validation status"""
        if obj.signature_valid is None:
            return format_html('<span class="badge badge-secondary">{}</span>', _('Not Checked'))
        elif obj.signature_valid:
            return format_html('<span class="badge badge-success">{}</span>', _('Valid'))
        return format_html('<span class="badge badge-danger">{}</span>', _('Invalid'))
    signature_valid_badge.short_description = _('Signature')

    def processed_badge(self, obj):
        """Display processing status"""
        if obj.processed:
            return format_html('<span class="badge badge-success">{}</span>', _('Processed'))
        elif obj.processing_error:
            return format_html('<span class="badge badge-danger">{}</span>', _('Error'))
        return format_html('<span class="badge badge-warning">{}</span>', _('Pending'))
    processed_badge.short_description = _('Status')

    def has_add_permission(self, request):
        """Webhook logs are created automatically, not manually"""
        return False

    def has_change_permission(self, request, obj=None):
        """Webhook logs are read-only"""
        return False
