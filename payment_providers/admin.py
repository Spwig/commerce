"""
Django admin configuration for payment provider models
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse, path
from django.http import JsonResponse
from django.db.models import Count, Q
import json

from .models import PaymentProviderAccount, PaymentTransaction, PaymentWebhook, PaymentIntent
from .forms import PaymentProviderConfigForm


@admin.register(PaymentProviderAccount)
class PaymentProviderAccountAdmin(admin.ModelAdmin):
    """Admin for payment provider connections"""

    # Use custom form for credential decryption/encryption
    form = PaymentProviderConfigForm

    # Use custom change_list template for modern card view
    change_list_template = 'admin/payment_providers/paymentprovideraccount/change_list.html'
    change_form_template = 'admin/payment_providers/paymentprovideraccount/change_form.html'

    list_display = [
        'display_name_or_component',
        'user',
        'connection_status_badge',
        'is_active_badge',
        'is_default_badge',
        'checkout_mode_badge',
        'environment_badge',
        'last_tested_at',
        'created_at'
    ]
    list_filter = ['is_active', 'is_default', 'connection_status', 'checkout_mode', 'created_at']
    search_fields = ['display_name', 'component__name', 'user__username', 'user__email']
    readonly_fields = [
        'component', 'user', 'last_tested_at', 'connection_status',
        'connection_error', 'last_method_sync_at', 'method_sync_status',
        'method_sync_error', 'created_at', 'updated_at'
    ]
    list_per_page = 1000  # High limit for client-side filtering

    class Media:
        css = {
            'all': ('payment_providers/css/admin_provider_account.css',)
        }
        js = ('payment_providers/js/admin_provider_account.js',)

    def get_fieldsets(self, request, obj=None):
        """
        Dynamic fieldsets based on whether we're editing or creating.
        Note: Credential fields are NOT included in fieldsets - they're rendered
        in the custom change_form template to avoid Django admin field validation issues.
        """
        if obj:
            # Editing existing provider
            return (
                (_('Provider Information'), {
                    'fields': ('component', 'user', 'display_name'),
                    'description': _('Component and User cannot be changed after creation for security and audit purposes.')
                }),
                (_('Configuration'), {
                    'fields': ('checkout_mode', 'sort_order')
                }),
                (_('Status'), {
                    'fields': ('is_active', 'is_default')
                }),
                (_('Payment Method Synchronization'), {
                    'fields': ('method_sync_status', 'last_method_sync_at', 'method_sync_error'),
                    'classes': ('collapse',),
                    'description': mark_safe(
                        '<div class="help">' +
                        str(_('Payment methods can be synced from your provider account. ')) +
                        '<a href="#" class="pp-sync-methods-link" data-account-id="{}">'.format(obj.id if obj else '') +
                        str(_('Sync Payment Methods Now')) +
                        '</a></div>'
                    ) if obj else _('Save the account first to enable payment method synchronization.')
                }),
                (_('Connection Health'), {
                    'fields': ('connection_status', 'connection_error', 'last_tested_at'),
                    'classes': ('collapse',),
                    'description': _('Connection health is automatically updated when you test the connection from the wizard.')
                }),
                (_('Metadata'), {
                    'fields': ('created_at', 'updated_at'),
                    'classes': ('collapse',)
                }),
            )
        else:
            # Creating new provider - use wizard instead
            wizard_url = reverse('payment_providers:wizard_step1')
            return (
                (_('Create Provider'), {
                    'fields': ('component', 'user', 'display_name'),
                    'description': mark_safe(
                        '<div class="messagelist">'
                        '<div class="warning">'
                        '<strong>' + str(_('Please use the Payment Provider Connection Wizard')) + '</strong><br/>'
                        + str(_('For the best experience, please use the <a href="%(url)s">Provider Connection Wizard</a> to set up new providers.') % {'url': wizard_url}) +
                        '</div>'
                        '</div>'
                    )
                }),
            )

    def display_name_or_component(self, obj):
        """Display name or fallback to component name"""
        if obj.display_name:
            return obj.display_name
        return format_html('<em>{}</em>', obj.component.name)
    display_name_or_component.short_description = _('Name')

    def connection_status_badge(self, obj):
        """Display connection status with color-coded badge"""
        css_map = {
            'connected': 'pp-list-badge-connected',
            'error': 'pp-list-badge-error',
            'unknown': 'pp-list-badge-unknown'
        }
        css_class = css_map.get(obj.connection_status, 'pp-list-badge-unknown')
        return format_html(
            '<span class="pp-list-badge {}">{}</span>',
            css_class,
            obj.get_connection_status_display().upper()
        )
    connection_status_badge.short_description = _('Connection')

    def is_active_badge(self, obj):
        """Display active status badge"""
        if obj.is_active:
            return format_html(
                '<span class="pp-list-badge pp-list-badge-active">ACTIVE</span>'
            )
        return format_html(
            '<span class="pp-list-badge pp-list-badge-inactive">INACTIVE</span>'
        )
    is_active_badge.short_description = _('Status')

    def is_default_badge(self, obj):
        """Display default provider badge"""
        if obj.is_default:
            return format_html(
                '<span class="pp-list-badge pp-list-badge-default">DEFAULT</span>'
            )
        return '-'
    is_default_badge.short_description = _('Default')

    def checkout_mode_badge(self, obj):
        """Display checkout mode badge"""
        css_map = {
            'hosted': 'pp-list-badge-hosted',
            'integrated': 'pp-list-badge-integrated'
        }
        css_class = css_map.get(obj.checkout_mode, 'pp-list-badge-unknown')
        return format_html(
            '<span class="pp-list-badge {}">{}</span>',
            css_class,
            obj.get_checkout_mode_display().upper()
        )
    checkout_mode_badge.short_description = _('Checkout Mode')

    @admin.display(description=_('Environment'))
    def environment_badge(self, obj):
        """Display environment mode with badge styling."""
        creds = obj.credentials_encrypted or {}
        env = creds.get('environment', 'unknown')

        if obj.test_mode:
            css_class = 'pp-list-badge-test'
        else:
            css_class = 'pp-list-badge-live'

        return format_html(
            '<span class="pp-list-badge {}">{}</span>',
            css_class,
            str(env).title()
        )

    def changelist_view(self, request, extra_context=None):
        """Add custom context data for the provider account list view"""
        extra_context = extra_context or {}

        # Get all provider accounts
        all_providers = PaymentProviderAccount.objects.select_related('component', 'user').all()

        # Status counts
        extra_context['active_count'] = all_providers.filter(is_active=True).count()
        extra_context['inactive_count'] = all_providers.filter(is_active=False).count()

        # Connection status counts
        extra_context['connected_count'] = all_providers.filter(connection_status='connected').count()
        extra_context['error_count'] = all_providers.filter(connection_status='error').count()
        extra_context['unknown_count'] = all_providers.filter(connection_status='unknown').count()

        # Checkout mode counts
        extra_context['hosted_count'] = all_providers.filter(checkout_mode='hosted').count()
        extra_context['integrated_count'] = all_providers.filter(checkout_mode='integrated').count()

        # Provider type counts (group by component)
        provider_types = all_providers.values(
            'component__name', 'component__slug'
        ).annotate(
            count=Count('id')
        ).order_by('-count')
        extra_context['provider_types'] = provider_types

        # Default provider
        default_provider = all_providers.filter(is_default=True).first()
        extra_context['default_provider'] = default_provider

        return super().changelist_view(request, extra_context=extra_context)

    def get_queryset(self, request):
        """Filter queryset based on request parameters"""
        qs = super().get_queryset(request)

        # Active filter
        is_active = request.GET.get('is_active')
        if is_active:
            qs = qs.filter(is_active=(is_active == '1'))

        # Connection status filter
        connection_status = request.GET.get('connection_status')
        if connection_status:
            qs = qs.filter(connection_status=connection_status)

        # Checkout mode filter
        checkout_mode = request.GET.get('checkout_mode')
        if checkout_mode:
            qs = qs.filter(checkout_mode=checkout_mode)

        # Component filter
        component_slug = request.GET.get('component')
        if component_slug:
            qs = qs.filter(component__slug=component_slug)

        # Search query
        search = request.GET.get('q')
        if search:
            qs = qs.filter(
                Q(display_name__icontains=search) |
                Q(component__name__icontains=search) |
                Q(user__username__icontains=search)
            )

        return qs

    def get_urls(self):
        """Add custom admin URLs"""
        urls = super().get_urls()
        custom_urls = [
            path(
                '<uuid:account_id>/test/',
                self.admin_site.admin_view(self.test_connection_view),
                name='payment_providers_paymentprovideraccount_test'
            ),
            path(
                '<uuid:account_id>/set-default/',
                self.admin_site.admin_view(self.set_default_view),
                name='payment_providers_paymentprovideraccount_setdefault'
            ),
            path(
                '<uuid:account_id>/toggle-active/',
                self.admin_site.admin_view(self.toggle_active_view),
                name='payment_providers_paymentprovideraccount_toggle_active'
            ),
            path(
                '<uuid:account_id>/sync-payment-methods/',
                self.admin_site.admin_view(self.sync_payment_methods_view),
                name='payment_providers_paymentprovideraccount_sync_methods'
            ),
            path(
                '<uuid:account_id>/configure-payment-methods/',
                self.admin_site.admin_view(self.configure_payment_methods_view),
                name='payment_providers_paymentprovideraccount_configure_methods'
            ),
            path(
                '<uuid:account_id>/update-payment-method/',
                self.admin_site.admin_view(self.update_payment_method_view),
                name='payment_providers_paymentprovideraccount_update_method'
            ),
            path(
                '<uuid:account_id>/remove-country-override/',
                self.admin_site.admin_view(self.remove_country_override_view),
                name='payment_providers_paymentprovideraccount_remove_country_override'
            ),
            path(
                '<uuid:account_id>/delete/',
                self.admin_site.admin_view(self.delete_provider_view),
                name='payment_providers_paymentprovideraccount_delete_ajax'
            ),
        ]
        return custom_urls + urls

    def test_connection_view(self, request, account_id):
        """AJAX endpoint to test provider connection"""
        try:
            account = PaymentProviderAccount.objects.get(id=account_id)
            result = account.test_connection()
            return JsonResponse({
                'success': result.get('success', False),
                'message': result.get('message', str(_('Connection test completed'))),
                'details': result.get('details', {})
            })
        except PaymentProviderAccount.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': str(_('Provider account not found'))
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(_('Connection test failed: %(error)s') % {'error': str(e)})
            }, status=500)

    def set_default_view(self, request, account_id):
        """AJAX endpoint to set provider as default"""
        try:
            account = PaymentProviderAccount.objects.get(id=account_id)
            # Clear other defaults
            PaymentProviderAccount.objects.filter(is_default=True).update(is_default=False)
            # Set this as default
            account.is_default = True
            account.save()
            return JsonResponse({
                'success': True,
                'message': _('Set as default provider')
            })
        except PaymentProviderAccount.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': _('Provider account not found')
            }, status=404)

    def toggle_active_view(self, request, account_id):
        """AJAX endpoint to toggle provider active status"""
        if request.method != 'POST':
            return JsonResponse({
                'success': False,
                'message': str(_('Method not allowed'))
            }, status=405)
        try:
            account = PaymentProviderAccount.objects.get(id=account_id)
            account.is_active = not account.is_active
            account.save(update_fields=['is_active'])
            return JsonResponse({
                'success': True,
                'is_active': account.is_active,
                'message': str(_('Provider enabled')) if account.is_active else str(_('Provider disabled'))
            })
        except PaymentProviderAccount.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': str(_('Provider account not found'))
            }, status=404)

    def sync_payment_methods_view(self, request, account_id):
        """AJAX endpoint to sync payment methods from provider API"""
        if request.method != 'POST':
            return JsonResponse({
                'success': False,
                'error': _('Method not allowed')
            }, status=405)

        try:
            account = PaymentProviderAccount.objects.get(id=account_id)

            # Check if provider supports payment method sync
            try:
                provider_instance = account.get_provider_instance()
                if not hasattr(provider_instance, 'get_payment_method_types'):
                    return JsonResponse({
                        'success': False,
                        'error': _('This provider does not support payment method synchronization')
                    })
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'error': _('Failed to load provider: %(error)s') % {'error': str(e)}
                })

            # Perform sync
            result = account.sync_payment_methods()

            if result['success']:
                methods_data = result.get('methods', {})
                total_countries = len(methods_data)
                total_methods = sum(len(methods) for methods in methods_data.values())

                return JsonResponse({
                    'success': True,
                    'message': _('Successfully synced %(methods)d payment methods across %(countries)d countries') % {
                        'methods': total_methods,
                        'countries': total_countries
                    },
                    'data': {
                        'methods': methods_data,
                        'total_countries': total_countries,
                        'total_methods': total_methods,
                        'last_sync': account.last_method_sync_at.isoformat() if account.last_method_sync_at else None
                    }
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': result.get('message', _('Synchronization failed'))
                })

        except PaymentProviderAccount.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': _('Provider account not found')
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': _('Unexpected error: %(error)s') % {'error': str(e)}
            }, status=500)

    def configure_payment_methods_view(self, request, account_id):
        """Admin page to configure payment methods — global + optional per-country"""
        from django.shortcuts import render
        from shipping.models import ShippingCountry

        try:
            account = PaymentProviderAccount.objects.get(id=account_id)

            GLOBAL_KEY = PaymentProviderAccount.GLOBAL_KEY

            # --- Global section ---
            # Build global available methods as the union of all provider methods
            all_available = account.available_payment_methods
            global_available_slugs = list(all_available.get(GLOBAL_KEY, []))
            if not global_available_slugs:
                # No explicit _global entry — union all country methods
                seen = set()
                for methods in all_available.values():
                    for m in methods:
                        if m not in seen:
                            global_available_slugs.append(m)
                            seen.add(m)

            global_enabled = account.enabled_payment_methods.get(GLOBAL_KEY, [])
            global_data = {
                'country_code': GLOBAL_KEY,
                'country_name': _('Global (All Countries)'),
                'available_methods': [
                    {'slug': s, 'name': s.replace('_', ' ').title()}
                    for s in global_available_slugs
                ],
                'enabled_methods': global_enabled,
                'is_global': True,
            }

            # --- Per-country overrides ---
            country_data = []
            # Include countries already configured in enabled_payment_methods
            configured_countries = [
                k for k in account.enabled_payment_methods.keys()
                if k != GLOBAL_KEY
            ]
            # Also include shipping countries as suggestions
            shipping_countries = ShippingCountry.objects.filter(
                site_id=1, is_active=True
            ).order_by('country_code')
            shipping_country_map = {
                sc.country_code: str(sc) for sc in shipping_countries
            }

            # Merge: configured countries + shipping countries (no duplicates)
            all_country_codes = list(dict.fromkeys(
                configured_countries + list(shipping_country_map.keys())
            ))

            for country_code in all_country_codes:
                available_slugs = account.get_available_methods_for_country(country_code)
                # Only show country-specific enabled (not global fallback)
                enabled_methods = account.enabled_payment_methods.get(country_code, [])
                country_name = shipping_country_map.get(
                    country_code, country_code
                )

                country_data.append({
                    'country_code': country_code,
                    'country_name': country_name,
                    'available_methods': [
                        {'slug': s, 'name': s.replace('_', ' ').title()}
                        for s in available_slugs
                    ],
                    'enabled_methods': enabled_methods,
                    'is_global': False,
                })

            context = {
                'account': account,
                'global_data': global_data,
                'country_data': country_data,
                'has_methods': bool(global_available_slugs),
                'title': _('Configure Payment Methods - %(provider)s') % {
                    'provider': account.component.name
                },
            }

            return render(
                request,
                'admin/payment_providers/configure_payment_methods.html',
                context
            )

        except PaymentProviderAccount.DoesNotExist:
            from django.http import Http404
            raise Http404(_('Provider account not found'))

    def update_payment_method_view(self, request, account_id):
        """AJAX endpoint to enable/disable payment method for a country"""
        if request.method != 'POST':
            return JsonResponse({
                'success': False,
                'error': _('Method not allowed')
            }, status=405)

        try:
            import json as json_module
            import re
            data = json_module.loads(request.body)
            country_code = data.get('country_code', '')
            method_slug = data.get('method_slug', '')
            enabled = data.get('enabled')

            # Validate required parameters
            if not country_code or not method_slug or enabled is None:
                return JsonResponse({
                    'success': False,
                    'error': _('Missing required parameters')
                }, status=400)

            # Validate country_code format (ISO 3166-1 alpha-2 or _global)
            if str(country_code) != '_global' and not re.match(r'^[A-Za-z]{2}$', str(country_code)):
                return JsonResponse({
                    'success': False,
                    'error': _('Invalid country code')
                }, status=400)

            # Validate method_slug format (alphanumeric + underscores, max 50 chars)
            if not re.match(r'^[a-z0-9_]{1,50}$', str(method_slug)):
                return JsonResponse({
                    'success': False,
                    'error': _('Invalid payment method identifier')
                }, status=400)

            # Validate enabled is boolean
            if not isinstance(enabled, bool):
                return JsonResponse({
                    'success': False,
                    'error': _('Invalid enabled value')
                }, status=400)

            account = PaymentProviderAccount.objects.get(id=account_id)

            if enabled:
                account.enable_payment_method(country_code, method_slug)
                message = _('Enabled %(method)s for %(country)s') % {
                    'method': method_slug,
                    'country': country_code
                }
            else:
                account.disable_payment_method(country_code, method_slug)
                message = _('Disabled %(method)s for %(country)s') % {
                    'method': method_slug,
                    'country': country_code
                }

            return JsonResponse({
                'success': True,
                'message': message
            })

        except PaymentProviderAccount.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': _('Provider account not found')
            }, status=404)
        except ValueError as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
        except json_module.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': _('Invalid request body')
            }, status=400)
        except Exception:
            import logging
            logging.getLogger(__name__).exception('Error updating payment method')
            return JsonResponse({
                'success': False,
                'error': _('An unexpected error occurred')
            }, status=500)

    def remove_country_override_view(self, request, account_id):
        """AJAX endpoint to remove a country-specific override (falls back to global)"""
        if request.method != 'POST':
            return JsonResponse({
                'success': False,
                'error': _('Method not allowed')
            }, status=405)

        try:
            import json as json_module
            import re
            data = json_module.loads(request.body)
            country_code = data.get('country_code', '')

            if not country_code or not re.match(r'^[A-Za-z]{2}$', str(country_code)):
                return JsonResponse({
                    'success': False,
                    'error': _('Invalid country code')
                }, status=400)

            country_code = country_code.upper()
            account = PaymentProviderAccount.objects.get(id=account_id)

            if country_code in account.enabled_payment_methods:
                del account.enabled_payment_methods[country_code]
                account.save(update_fields=['enabled_payment_methods', 'updated_at'])

            return JsonResponse({
                'success': True,
                'message': _('Country override removed. Global settings will apply for %(country)s.') % {
                    'country': country_code
                }
            })

        except PaymentProviderAccount.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': _('Provider account not found')
            }, status=404)
        except json_module.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': _('Invalid request body')
            }, status=400)
        except Exception:
            import logging
            logging.getLogger(__name__).exception('Error removing country override')
            return JsonResponse({
                'success': False,
                'error': _('An unexpected error occurred')
            }, status=500)

    def delete_provider_view(self, request, account_id):
        """AJAX endpoint to delete a provider account"""
        if request.method != 'POST':
            return JsonResponse({
                'success': False,
                'message': str(_('Method not allowed'))
            }, status=405)

        try:
            account = PaymentProviderAccount.objects.get(id=account_id)
            # Prevent deletion if transactions exist
            if account.transactions.exists():
                return JsonResponse({
                    'success': False,
                    'message': str(_('Cannot delete provider with existing transactions. Deactivate it instead.'))
                }, status=400)
            account.delete()
            return JsonResponse({
                'success': True,
                'message': str(_('Provider deleted successfully'))
            })
        except PaymentProviderAccount.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': str(_('Provider account not found'))
            }, status=404)

    def save_model(self, request, obj, form, change):
        """Save model with user tracking"""
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    """Admin interface for Payment Transactions"""

    change_list_template = 'admin/payment_providers/paymenttransaction/change_list.html'

    class Media:
        css = {
            'all': ('payment_providers/css/admin_provider_account.css',)
        }

    list_display = [
        'transaction_id', 'provider_account', 'amount',
        'status', 'transaction_type', 'created_at'
    ]

    list_filter = [
        'status', 'transaction_type', 'provider_account', 'created_at'
    ]

    search_fields = [
        'transaction_id', 'provider_transaction_id',
        'authorization_id', 'payment_method_type', 'payment_method_last4'
    ]

    readonly_fields = [
        'transaction_id', 'provider_transaction_id', 'provider_response_display',
        'created_at', 'updated_at', 'expires_at', 'error_code', 'error_message'
    ]

    fieldsets = (
        (_('Transaction Information'), {
            'fields': (
                'transaction_id', 'provider_transaction_id', 'provider_account',
                'order', 'transaction_type', 'authorization_id'
            )
        }),

        (_('Payment Details'), {
            'fields': ('amount', 'status', 'payment_method_type', 'payment_method_last4')
        }),

        (_('Provider Response'), {
            'fields': ('provider_response_display',),
            'classes': ('collapse',)
        }),

        (_('Error Information'), {
            'fields': ('error_code', 'error_message'),
            'classes': ('collapse',)
        }),

        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at', 'expires_at'),
            'classes': ('collapse',)
        }),
    )

    def provider_response_display(self, obj):
        """Display formatted provider response"""
        if obj.provider_response:
            formatted_json = json.dumps(obj.provider_response, indent=2)
            return format_html(
                '<pre class="pp-json-display">{}</pre>',
                formatted_json
            )
        return _('No response data')
    provider_response_display.short_description = _('Provider Response')

    def changelist_view(self, request, extra_context=None):
        """Add custom context data for the transaction list view"""
        extra_context = extra_context or {}

        all_transactions = PaymentTransaction.objects.all()

        # Counts
        extra_context['total_transactions'] = all_transactions.count()
        extra_context['successful_count'] = all_transactions.filter(
            status__in=['completed', 'authorized']
        ).count()
        extra_context['failed_count'] = all_transactions.filter(status='failed').count()
        extra_context['refunded_count'] = all_transactions.filter(
            status__in=['refunded', 'partially_refunded']
        ).count()

        # Choices for filter dropdowns
        extra_context['status_choices'] = PaymentTransaction.STATUS_CHOICES
        extra_context['type_choices'] = PaymentTransaction.TYPE_CHOICES

        # Provider accounts for filter dropdown
        extra_context['provider_accounts'] = PaymentProviderAccount.objects.select_related(
            'component'
        ).filter(is_active=True).order_by('display_name')

        return super().changelist_view(request, extra_context=extra_context)

    def has_add_permission(self, request):
        """Prevent manual creation of transactions"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of transactions for audit purposes"""
        return False


@admin.register(PaymentWebhook)
class PaymentWebhookAdmin(admin.ModelAdmin):
    """Admin interface for Payment Webhooks"""

    change_list_template = 'admin/payment_providers/paymentwebhook/change_list.html'

    class Media:
        css = {
            'all': ('payment_providers/css/admin_provider_account.css',)
        }

    list_display = [
        'event_id', 'provider_slug', 'event_type', 'processed',
        'signature_verified', 'created_at', 'processed_at'
    ]

    list_filter = ['provider_slug', 'event_type', 'processed', 'signature_verified', 'created_at']

    search_fields = ['event_id', 'event_type', 'idempotency_key']

    readonly_fields = [
        'event_id', 'event_type', 'payload_display', 'headers_display',
        'created_at', 'processed_at'
    ]

    fieldsets = (
        (_('Webhook Information'), {
            'fields': ('provider_slug', 'provider_account', 'event_id', 'event_type',
                      'processed', 'signature_verified', 'idempotency_key')
        }),

        (_('Payload'), {
            'fields': ('payload_display',),
            'classes': ('collapse',)
        }),

        (_('Headers'), {
            'fields': ('headers_display',),
            'classes': ('collapse',)
        }),

        (_('Processing'), {
            'fields': ('processing_result', 'processing_error', 'processed_at'),
            'classes': ('collapse',)
        }),

        (_('System Information'), {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def payload_display(self, obj):
        """Display formatted webhook payload"""
        if obj.payload:
            formatted_json = json.dumps(obj.payload, indent=2)
            return format_html(
                '<pre class="pp-json-display">{}</pre>',
                formatted_json
            )
        return _('No payload data')
    payload_display.short_description = _('Webhook Payload')

    def headers_display(self, obj):
        """Display formatted webhook headers"""
        if obj.headers:
            formatted_json = json.dumps(obj.headers, indent=2)
            return format_html(
                '<pre class="pp-json-display">{}</pre>',
                formatted_json
            )
        return _('No headers data')
    headers_display.short_description = _('HTTP Headers')

    def changelist_view(self, request, extra_context=None):
        """Add custom context data for the webhook list view"""
        extra_context = extra_context or {}

        all_webhooks = PaymentWebhook.objects.all()

        # Counts
        extra_context['total_webhooks'] = all_webhooks.count()
        extra_context['processed_count'] = all_webhooks.filter(processed=True).count()
        extra_context['unprocessed_count'] = all_webhooks.filter(processed=False).count()
        extra_context['verified_count'] = all_webhooks.filter(signature_verified=True).count()

        # Distinct provider slugs for filter dropdown
        extra_context['provider_slugs'] = list(
            all_webhooks.exclude(provider_slug='').values_list(
                'provider_slug', flat=True
            ).distinct().order_by('provider_slug')
        )

        return super().changelist_view(request, extra_context=extra_context)

    def has_add_permission(self, request):
        """Prevent manual creation of webhooks"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of webhooks for audit trail integrity"""
        return False


@admin.register(PaymentIntent)
class PaymentIntentAdmin(admin.ModelAdmin):
    """Read-only admin for payment intents (created by checkout flow)"""

    list_display = [
        'id', 'provider_account', 'order', 'status', 'amount', 'created_at'
    ]

    list_filter = ['status', 'provider_account', 'created_at']

    search_fields = ['id', 'provider_intent_id', 'order__order_number']

    readonly_fields = [
        'id', 'checkout_session', 'provider_account', 'order',
        'provider_intent_id', 'client_secret', 'checkout_url',
        'status', 'amount', 'amount_currency',
        'requires_action', 'action_type', 'action_url', 'action_data',
        'metadata', 'provider_response', 'created_at', 'updated_at'
    ]

    fieldsets = (
        (_('Intent Information'), {
            'fields': (
                'id', 'provider_account', 'order', 'checkout_session',
                'provider_intent_id', 'status', 'amount',
            )
        }),
        (_('Checkout Details'), {
            'fields': ('checkout_url', 'client_secret'),
            'classes': ('collapse',)
        }),
        (_('3DS / Authentication'), {
            'fields': ('requires_action', 'action_type', 'action_url', 'action_data'),
            'classes': ('collapse',)
        }),
        (_('Provider Response'), {
            'fields': ('provider_response', 'metadata'),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
