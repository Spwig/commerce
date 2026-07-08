"""
Django admin configuration for shipping models
"""

from decimal import Decimal
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe
from django.urls import reverse, path
from django.http import JsonResponse
from django.utils import timezone

from .models import (
    CarrierPreset,
    ShippingPackage,
    ProviderAccount,
    Shipment,
    TrackingEvent,
    WebhookLog,
    ShippingZone,
    ShippingPromotion,
    ShippingRateTable,
    ShippingRateTier,
    Location,
    ShippingCountry,
)
from .forms import ProviderAccountAdminForm, ShippingZoneAdminForm


# ============================================================================
# Inline Admins
# ============================================================================

class TrackingEventInline(admin.TabularInline):
    """Inline display of tracking events for a shipment"""
    model = TrackingEvent
    extra = 0
    readonly_fields = ['status', 'description', 'location', 'occurred_at', 'created_at']
    can_delete = False
    ordering = ['-occurred_at']

    def has_add_permission(self, request, obj=None):
        """Prevent manual addition of tracking events in admin"""
        return False


# ============================================================================
# Model Admins
# ============================================================================

@admin.register(ShippingCountry)
class ShippingCountryAdmin(admin.ModelAdmin):
    """Admin for shipping countries - defines which countries the merchant ships to"""

    list_display = [
        'country_flag_and_name',
        'country_code',
        'source_warehouse_display',
        'priority_badge',
        'is_active_badge',
        'created_at',
    ]

    list_filter = ['is_active', 'site', 'source_warehouse', 'created_at']
    search_fields = ['country_code']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        (_('Country Information'), {
            'fields': ('site', 'country_code', 'is_active')
        }),
        (_('Routing Configuration'), {
            'fields': ('source_warehouse', 'priority'),
            'description': _(
                'Optional warehouse routing for multi-warehouse setups. '
                'Lower priority numbers = higher priority for routing.'
            )
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['enable_shipping', 'disable_shipping']

    class Media:
        css = {
            'all': ('shipping/css/admin_badges.css',)
        }

    def country_flag_and_name(self, obj):
        """Display country flag and full name"""
        from django_countries.fields import Country
        country = Country(obj.country_code)
        return format_html(
            '<div class="shipping-country-flag-name">'
            '<img src="{}" />'
            '<span>{}</span>'
            '</div>',
            country.flag,
            country.name
        )
    country_flag_and_name.short_description = _('Country')

    def source_warehouse_display(self, obj):
        """Display source warehouse or 'Any'"""
        if obj.source_warehouse:
            return format_html(
                '<i class="fas fa-warehouse shipping-icon-warehouse"></i> {}',
                obj.source_warehouse.name
            )
        return format_html('<span class="shipping-text-muted"><em>{}</em></span>', _('Any warehouse'))
    source_warehouse_display.short_description = _('Source Warehouse')

    def priority_badge(self, obj):
        """Display priority as badge"""
        if obj.priority == 0:
            return format_html('<span class="priority-badge highest">P0 - HIGHEST</span>')
        elif obj.priority <= 5:
            return format_html('<span class="priority-badge high">P{}</span>', obj.priority)
        elif obj.priority <= 10:
            return format_html('<span class="priority-badge medium">P{}</span>', obj.priority)
        else:
            return format_html('<span class="priority-badge low">P{}</span>', obj.priority)
    priority_badge.short_description = _('Priority')
    priority_badge.admin_order_field = 'priority'

    def is_active_badge(self, obj):
        """Display active status as badge"""
        if obj.is_active:
            return format_html('<span class="shipping-badge-active">ACTIVE</span>')
        return format_html('<span class="shipping-badge-inactive">INACTIVE</span>')
    is_active_badge.short_description = _('Status')

    def enable_shipping(self, request, queryset):
        """Bulk action to enable shipping to selected countries"""
        count = queryset.update(is_active=True)
        self.message_user(
            request,
            _('Successfully enabled shipping to %(count)d countries.') % {'count': count},
            level='success'
        )
    enable_shipping.short_description = _('Enable shipping to selected countries')

    def disable_shipping(self, request, queryset):
        """Bulk action to disable shipping to selected countries"""
        count = queryset.update(is_active=False)
        self.message_user(
            request,
            _('Successfully disabled shipping to %(count)d countries.') % {'count': count},
            level='success'
        )
    disable_shipping.short_description = _('Disable shipping to selected countries')


@admin.register(CarrierPreset)
class CarrierPresetAdmin(admin.ModelAdmin):
    """Admin for manual shipping carriers"""

    # Use custom change_list template for modern card view
    change_list_template = 'admin/shipping/carrierpreset/change_list.html'

    # Show all carriers on one page for client-side filtering
    list_per_page = 1000  # High limit to show all carriers at once

    list_display = [
        'logo_preview_with_fallback',
        'name',
        'country_badge',
        'slug',
        'is_default_badge',
        'is_active_badge',
        'is_system_badge',
        'created_at',
    ]
    list_filter = ['country_of_operation', 'is_active', 'is_default', 'is_system', 'created_at']
    search_fields = ['name', 'slug', 'country_of_operation', 'description']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'logo_preview_full', 'tracking_url_display', 'url_status_display']
    prepopulated_fields = {'slug': ('name',)}

    class Media:
        css = {
            'all': ('shipping/css/admin_carrier_preset.css',)
        }

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'slug', 'country_of_operation', 'description')
        }),
        (_('Branding'), {
            'fields': ('logo', 'logo_preview_full'),
            'description': mark_safe(
                '<div class="warning-box">'
                '<strong>' + str(_('Logo Attribution:')) + '</strong> '
                + str(_('Carrier logos are trademarks of their respective owners and are used solely for identification and reference purposes. No affiliation or endorsement is implied.')) +
                '</div>'
            )
        }),
        (_('Tracking Configuration'), {
            'fields': ('tracking_url_display', 'tracking_url_template_override', 'url_status_display'),
            'description': mark_safe(
                '<div class="info-box">'
                '<strong>' + str(_('URL Override System:')) + '</strong><br/>'
                + str(_('System carriers come with default tracking URLs. You can override these URLs if needed.')) + '<br/>'
                + str(_('Use {tracking_number} as the placeholder for the tracking number in your URL.')) + '<br/>'
                '<strong>' + str(_('Example:')) + '</strong> <code>https://example.com/track?id={tracking_number}</code><br/>'
                + str(_('Your override will be reported to our update server to help improve default URLs for all users.')) +
                '</div>'
            )
        }),
        (_('Status'), {
            'fields': ('is_active', 'is_default', 'is_system')
        }),
        (_('Metadata'), {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def logo_preview_with_fallback(self, obj):
        """Show logo or Font Awesome fallback with attribution tooltip"""
        logo_info = obj.logo_with_fallback()

        attribution = (
            'Carrier logos are trademarks of their respective owners '
            'and are used solely for identification and reference purposes. '
            'No affiliation or endorsement is implied.'
        )

        if logo_info['type'] == 'image':
            return format_html(
                '<div class="logo-preview"><img src="{}" title="{}" /></div>',
                logo_info['url'],
                attribution
            )
        else:
            return format_html(
                '<div class="logo-preview"><i class="{}" title="No logo available"></i></div>',
                logo_info['class']
            )
    logo_preview_with_fallback.short_description = _('Logo')

    def logo_preview_full(self, obj):
        """Show full logo preview in detail view with attribution"""
        logo_info = obj.logo_with_fallback()

        if logo_info['type'] == 'image':
            return format_html(
                '<div class="logo-preview-full"><img src="{}" /></div>',
                logo_info['url']
            )
        else:
            return format_html(
                '<div class="logo-preview-full">'
                '<i class="{}"></i>'
                '<p>{}</p>'
                '</div>',
                logo_info['class'],
                _('No logo uploaded')
            )
    logo_preview_full.short_description = _('Logo Preview')

    def country_badge(self, obj):
        """Show country flag and code"""
        if obj.country_of_operation:
            return format_html(
                '<div class="country-badge" title="{}">'
                '<img src="{}" />'
                '<span>{}</span>'
                '</div>',
                obj.country_of_operation.name,
                obj.country_of_operation.flag,
                obj.country_of_operation.code
            )
        return format_html('<span class="quiet" title="International">INT</span>')
    country_badge.short_description = _('Country')

    def is_default_badge(self, obj):
        if obj.is_default:
            return format_html('<span class="status-badge default">DEFAULT</span>')
        return '-'
    is_default_badge.short_description = _('Default')

    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span class="status-badge active">ACTIVE</span>')
        return format_html('<span class="status-badge inactive">INACTIVE</span>')
    is_active_badge.short_description = _('Status')

    def is_system_badge(self, obj):
        if obj.is_system:
            return format_html('<span class="status-badge system">SYSTEM</span>')
        return '-'
    is_system_badge.short_description = _('Type')

    def tracking_url_display(self, obj):
        """Show system tracking URL (read-only)"""
        if obj.tracking_url_template:
            return format_html(
                '<div class="url-display-box">'
                '<strong>{}</strong><br/>'
                '<code>{}</code>'
                '</div>',
                _('System Default URL'),
                obj.tracking_url_template
            )
        return format_html('<span class="quiet">{}</span>', _('No tracking URL'))
    tracking_url_display.short_description = _('System Tracking URL')

    def url_status_display(self, obj):
        """Show current URL status with badge and effective URL"""
        status = obj.get_url_status()
        effective_url = obj.get_tracking_url_template()

        if status['type'] == 'override':
            badge_class = 'override'
            icon = '✓'
        else:
            badge_class = 'system'
            icon = '•'

        return format_html(
            '<div class="url-status-container">'
            '<span class="url-status-badge {}">{} {}</span>'
            '<div class="url-effective-box">'
            '<strong>{}</strong><br/>'
            '<code>{}</code>'
            '</div>'
            '</div>',
            badge_class,
            icon,
            status['display'],
            _('Effective URL'),
            effective_url if effective_url else _('No URL configured')
        )
    url_status_display.short_description = _('Current URL Status')

    def changelist_view(self, request, extra_context=None):
        """Add custom context data for the carrier list view"""
        from django.db.models import Count, Q

        extra_context = extra_context or {}

        # Get all carriers for counts
        all_carriers = CarrierPreset.objects.all()

        # Status counts
        extra_context['active_count'] = all_carriers.filter(is_active=True).count()
        extra_context['inactive_count'] = all_carriers.filter(is_active=False).count()

        # Type counts
        extra_context['system_count'] = all_carriers.filter(is_system=True).count()
        extra_context['custom_count'] = all_carriers.filter(is_system=False).count()

        # Country counts
        country_counts = all_carriers.exclude(
            country_of_operation=''
        ).exclude(
            country_of_operation=None
        ).values('country_of_operation').annotate(
            count=Count('id')
        ).order_by('-count')

        # Build countries list with counts
        countries_with_counts = []
        for item in country_counts:
            country_code = item['country_of_operation']
            if country_code:
                try:
                    from django_countries.fields import Country
                    country = Country(country_code)
                    countries_with_counts.append({
                        'code': country_code,
                        'name': country.name,
                        'flag': country.flag,
                        'count': item['count']
                    })
                except Exception:
                    # Skip invalid country codes
                    pass

        extra_context['countries_with_counts'] = countries_with_counts

        # International (no country) count
        extra_context['international_count'] = all_carriers.filter(
            Q(country_of_operation='') | Q(country_of_operation=None)
        ).count()

        return super().changelist_view(request, extra_context=extra_context)

    def get_queryset(self, request):
        """Filter queryset based on request parameters"""
        qs = super().get_queryset(request)

        # Country filter
        country = request.GET.get('country')
        if country:
            if country == 'NONE':
                qs = qs.filter(Q(country_of_operation='') | Q(country_of_operation=None))
            else:
                qs = qs.filter(country_of_operation=country)

        # Status filter
        is_active = request.GET.get('is_active')
        if is_active:
            qs = qs.filter(is_active=(is_active == '1'))

        # Type filter
        is_system = request.GET.get('is_system')
        if is_system:
            qs = qs.filter(is_system=(is_system == '1'))

        # Search query
        search = request.GET.get('q')
        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(slug__icontains=search) |
                Q(description__icontains=search)
            )

        return qs

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ShippingPackage)
class ShippingPackageAdmin(admin.ModelAdmin):
    """Admin for predefined shipping packages"""

    change_list_template = 'admin/shipping/shippingpackage/change_list.html'

    list_display = [
        'name',
        'dimensions_display',
        'volume_display',
        'max_weight',
        'tare_weight',
        'cost',
        'priority',
        'is_active',
        'usage_count',
    ]
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at', 'volume_display_detailed', 'external_dimensions_display']

    class Media:
        css = {
            'all': ('shipping/css/admin_badges.css',)
        }

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'description', 'is_active')
        }),
        (_('Dimensions'), {
            'fields': ('length', 'width', 'height', 'wall_thickness', 'volume_display_detailed', 'external_dimensions_display'),
            'description': mark_safe(
                '<div class="info-box">'
                '<i class="fas fa-info-circle"></i>'
                '<div>'
                '<strong>' + str(_('Internal vs External Dimensions:')) + '</strong>'
                '<p>' + str(_('• <strong>Internal dimensions</strong> are used for packing algorithm calculations (determining what fits inside)')) + '<br/>'
                + str(_('• <strong>Wall thickness</strong> defines the package material thickness (default 0.5cm for standard cardboard)')) + '<br/>'
                + str(_('• <strong>External dimensions</strong> are automatically calculated and sent to shipping carriers for rate calculations')) + '</p>'
                '</div>'
                '</div>'
            )
        }),
        (_('Weight Constraints'), {
            'fields': ('max_weight', 'tare_weight'),
            'description': _('Weight values in kilograms')
        }),
        (_('Configuration'), {
            'fields': ('cost', 'priority'),
            'description': _('Package cost and selection priority (higher = preferred for auto-packing)')
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def dimensions_display(self, obj):
        """Display package dimensions"""
        return f"{obj.length} × {obj.width} × {obj.height} cm"
    dimensions_display.short_description = _('Dimensions (L×W×H)')

    def volume_display(self, obj):
        """Display package volume"""
        volume_liters = obj.get_volume_liters()
        if volume_liters is None:
            return '-'
        return f"{volume_liters:.2f} L"
    volume_display.short_description = _('Volume')

    def volume_display_detailed(self, obj):
        """Detailed volume display for form"""
        volume_cm3 = obj.get_volume()
        volume_liters = obj.get_volume_liters()

        if volume_cm3 is None or volume_liters is None:
            return format_html(
                '<em class="shipping-em-quiet">{}</em>',
                _('Enter dimensions to calculate volume')
            )

        return format_html(
            '<strong>{:.2f} cm³</strong> ({:.2f} liters)',
            volume_cm3,
            volume_liters
        )
    volume_display_detailed.short_description = _('Calculated Volume (Internal)')

    def external_dimensions_display(self, obj):
        """Display external dimensions calculated from internal + wall thickness"""
        external_dims = obj.get_external_dimensions()
        external_volume = obj.get_external_volume()

        if external_dims is None or external_volume is None:
            return format_html(
                '<div class="shipping-dims-empty">'
                '<em>{}</em>'
                '</div>',
                _('Enter dimensions and wall thickness to calculate external dimensions')
            )

        external_volume_liters = external_volume / Decimal('1000')

        return format_html(
            '<div class="shipping-dims-box">'
            '<div class="shipping-dims-header">'
            '<strong>External Dimensions:</strong> '
            '<span class="shipping-dims-value">'
            '{:.2f} × {:.2f} × {:.2f} cm'
            '</span>'
            '</div>'
            '<div class="shipping-dims-detail">'
            'External Volume: <strong>{:.2f} cm³</strong> ({:.2f} liters)<br/>'
            '<em>These dimensions will be sent to shipping carriers for rate calculations</em>'
            '</div>'
            '</div>',
            external_dims['length'],
            external_dims['width'],
            external_dims['height'],
            external_volume,
            external_volume_liters
        )
    external_dimensions_display.short_description = _('External Dimensions (for carriers)')

    def usage_count(self, obj):
        """Count how many products/variants use this package"""
        product_count = obj.products.count()
        variant_count = obj.variants.count()
        total = product_count + variant_count

        if total == 0:
            return format_html('<span class="shipping-text-quiet">0</span>')

        return format_html(
            '<span class="shipping-usage-count">{}</span> <span class="shipping-usage-breakdown">({}P + {}V)</span>',
            total,
            product_count,
            variant_count
        )
    usage_count.short_description = _('Usage')
    usage_count.admin_order_field = 'products__count'

    def changelist_view(self, request, extra_context=None):
        """Add context for the custom change list template"""
        extra_context = extra_context or {}
        extra_context['active_count'] = ShippingPackage.objects.filter(is_active=True).count()
        extra_context['inactive_count'] = ShippingPackage.objects.filter(is_active=False).count()
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(ProviderAccount)
class ProviderAccountAdmin(admin.ModelAdmin):
    """Admin for API provider connections"""

    form = ProviderAccountAdminForm

    # Use custom change_list template for modern card view
    change_list_template = 'admin/shipping/provideraccount/change_list.html'
    change_form_template = 'admin/shipping/provideraccount/change_form.html'

    list_display = ['display_name_or_component', 'user', 'connection_status_badge', 'is_active_badge', 'is_default_badge', 'last_tested_at', 'created_at']
    list_filter = ['is_active', 'is_default', 'connection_status', 'created_at']
    search_fields = ['display_name', 'component__name', 'user__username', 'user__email']
    readonly_fields = ['component', 'user', 'last_tested_at', 'connection_status', 'connection_error', 'created_at', 'updated_at']

    class Media:
        css = {
            'all': ('shipping/css/admin_provider_account.css', 'shipping/css/admin_badges.css')
        }
        js = ('shipping/js/admin_provider_account.js',)

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
                (_('Status'), {'fields': ('is_active', 'is_default')}),
                (_('Connection Health'), {
                    'fields': ('connection_status', 'connection_error', 'last_tested_at'),
                    'classes': ('collapse',),
                    'description': _('Connection health is automatically updated when you test the connection from the wizard.')
                }),
                (_('Metadata'), {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
            )
        else:
            # Creating new provider - use wizard instead
            return (
                (_('Create Provider'), {
                    'fields': ('component', 'user', 'display_name'),
                    'description': mark_safe(
                        '<div class="messagelist">'
                        '<div class="warning">'
                        '<strong>' + str(_('Please use the Provider Connection Wizard')) + '</strong><br/>'
                        + str(_('For the best experience, please use the <a href="/admin/shipping/wizard/step1/">Provider Connection Wizard</a> to set up new providers.')) +
                        '</div>'
                        '</div>'
                    )
                }),
            )

    def display_name_or_component(self, obj):
        if obj.display_name:
            return obj.display_name
        return format_html('<em>{}</em>', obj.component.name)
    display_name_or_component.short_description = _('Name')

    def connection_status_badge(self, obj):
        css_map = {'connected': 'shipping-badge-status-connected', 'error': 'shipping-badge-status-error', 'unknown': 'shipping-badge-status-unknown'}
        css_class = css_map.get(obj.connection_status, 'shipping-badge-status-unknown')
        return format_html('<span class="shipping-badge-status {}">{}</span>', css_class, obj.get_connection_status_display().upper())
    connection_status_badge.short_description = _('Connection')

    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span class="shipping-badge-active">ACTIVE</span>')
        return format_html('<span class="shipping-badge-inactive">INACTIVE</span>')
    is_active_badge.short_description = _('Status')

    def is_default_badge(self, obj):
        if obj.is_default:
            return format_html('<span class="shipping-badge-default">DEFAULT</span>')
        return '-'
    is_default_badge.short_description = _('Default')

    def changelist_view(self, request, extra_context=None):
        """Add custom context data for the provider account list view"""
        from django.db.models import Count, Q

        extra_context = extra_context or {}

        # Get all provider accounts
        all_providers = ProviderAccount.objects.select_related('component').all()

        # Status counts
        extra_context['active_count'] = all_providers.filter(is_active=True).count()
        extra_context['inactive_count'] = all_providers.filter(is_active=False).count()

        # Connection status counts
        extra_context['connected_count'] = all_providers.filter(connection_status='connected').count()
        extra_context['error_count'] = all_providers.filter(connection_status='error').count()
        extra_context['unknown_count'] = all_providers.filter(connection_status='unknown').count()

        # Component counts (group by provider type)
        component_counts = all_providers.values(
            'component__slug',
            'component__name'
        ).annotate(
            count=Count('id')
        ).order_by('-count')

        # Build component list with counts
        components_with_counts = []
        for item in component_counts:
            if item['component__slug']:
                components_with_counts.append({
                    'slug': item['component__slug'],
                    'name': item['component__name'],
                    'count': item['count']
                })

        extra_context['component_counts'] = components_with_counts

        return super().changelist_view(request, extra_context=extra_context)

    def get_queryset(self, request):
        """Filter queryset based on request parameters"""
        from django.db.models import Q

        qs = super().get_queryset(request).select_related('component', 'user')

        # Connection status filter
        connection_status = request.GET.get('connection_status')
        if connection_status:
            qs = qs.filter(connection_status=connection_status)

        # Active status filter
        is_active = request.GET.get('is_active')
        if is_active:
            qs = qs.filter(is_active=(is_active == '1'))

        # Component filter
        component = request.GET.get('component')
        if component:
            qs = qs.filter(component__slug=component)

        # Search query
        search = request.GET.get('q')
        if search:
            qs = qs.filter(
                Q(display_name__icontains=search) |
                Q(component__name__icontains=search) |
                Q(user__username__icontains=search) |
                Q(user__email__icontains=search)
            )

        return qs

    def get_urls(self):
        """Add custom URLs for provider actions"""
        urls = super().get_urls()
        custom_urls = [
            path(
                '<path:object_id>/test-connection/',
                self.admin_site.admin_view(self.test_connection_view),
                name='shipping_provideraccount_test_connection',
            ),
        ]
        return custom_urls + urls

    def test_connection_view(self, request, object_id):
        """Test provider connection and update status"""
        if request.method != 'POST':
            return JsonResponse({'success': False, 'error': 'POST required'}, status=405)

        try:
            # Get provider account
            provider_account = ProviderAccount.objects.select_related('component').get(pk=object_id)

            # Decrypt credentials
            from .utils.encryption import decrypt_credentials
            credentials = decrypt_credentials(provider_account.credentials_encrypted)

            # Get provider class
            from .providers.registry import ProviderRegistry
            provider_class = ProviderRegistry.get_provider(provider_account.component.slug)

            if not provider_class:
                return JsonResponse({
                    'success': False,
                    'error': _('Provider implementation not found for %(provider)s') % {
                        'provider': provider_account.component.name
                    }
                }, status=404)

            # Create provider instance
            provider = provider_class(credentials=credentials)

            # Test connection
            test_result = provider.test_connection()

            # Update connection status
            if test_result.get('success'):
                provider_account.connection_status = 'connected'
                provider_account.connection_error = ''
                provider_account.last_tested_at = timezone.now()
            else:
                provider_account.connection_status = 'error'
                provider_account.connection_error = test_result.get('message', 'Connection failed')

            provider_account.save()

            return JsonResponse(test_result)

        except ProviderAccount.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': _('Provider account not found')
            }, status=404)

        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Test connection failed: {e}", exc_info=True)

            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    """Admin for shipments"""

    change_list_template = 'admin/shipping/shipment/change_list.html'
    list_display = ['id_short', 'order_link', 'provider_display', 'tracking_id_link', 'status_badge', 'dest_country', 'created_at']
    list_filter = ['status', 'carrier_preset', 'created_at', 'dest_country']
    search_fields = ['tracking_id', 'order__order_number', 'order__user__username', 'order__user__email', 'provider_reference']
    readonly_fields = [
        'created_at', 'updated_at', 'tracking_url_display', 'label_preview',
        'packing_slip_preview', 'commercial_invoice_preview', 'customs_form_preview'
    ]
    date_hierarchy = 'created_at'
    inlines = [TrackingEventInline]
    actions = ['purchase_labels', 'generate_packing_slips', 'generate_commercial_invoices', 'generate_customs_forms']

    class Media:
        css = {
            'all': ('shipping/css/admin_badges.css',)
        }

    fieldsets = (
        (_('Shipment Details'), {'fields': ('order', 'user', 'status')}),
        (_('Provider'), {'fields': ('carrier_preset', 'provider_account')}),
        (_('Tracking'), {'fields': ('tracking_id', 'tracking_url_display', 'label_url', 'label_preview', 'provider_reference')}),
        (_('Documents (Phase 6)'), {
            'fields': (
                'packing_slip_url', 'packing_slip_preview',
                'commercial_invoice_url', 'commercial_invoice_preview',
                'customs_form_url', 'customs_form_preview'
            ),
            'classes': ('collapse',)
        }),
        (_('Shipping Details'), {'fields': ('origin_country', 'dest_country', 'service_level', 'packages')}),
        (_('Costs'), {'fields': ('shipping_cost', 'carrier_cost', 'pricing_mode_used'), 'classes': ('collapse',)}),
        (_('Provider Data'), {'fields': ('provider_meta', 'audit_log'), 'classes': ('collapse',)}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    def changelist_view(self, request, extra_context=None):
        """Override changelist to add shipping statistics"""
        extra_context = extra_context or {}

        # Calculate statistics
        extra_context['total_shipments'] = Shipment.objects.count()
        extra_context['created_count'] = Shipment.objects.filter(status='created').count()
        extra_context['in_transit_count'] = Shipment.objects.filter(status='in_transit').count()
        extra_context['delivered_count'] = Shipment.objects.filter(status='delivered').count()
        extra_context['exceptions_count'] = Shipment.objects.filter(status='exception').count()
        extra_context['cancelled_count'] = Shipment.objects.filter(status='canceled').count()

        return super().changelist_view(request, extra_context=extra_context)

    def id_short(self, obj):
        return str(obj.id)[:8]
    id_short.short_description = _('ID')

    def order_link(self, obj):
        if obj.order:
            url = reverse('admin:orders_order_change', args=[obj.order.pk])
            return format_html('<a href="{}">{}</a>', url, obj.order.order_number)
        return '-'
    order_link.short_description = _('Order')

    def provider_display(self, obj):
        if obj.carrier_preset:
            return format_html('<i class="fas fa-warehouse shipping-icon-warehouse"></i> {}', obj.carrier_preset.name)
        elif obj.provider_account:
            return format_html('<i class="fas fa-plug shipping-icon-provider"></i> {}', obj.provider_account.display_name or obj.provider_account.component.name)
        return '-'
    provider_display.short_description = _('Provider')

    def tracking_id_link(self, obj):
        if not obj.tracking_id:
            return '-'
        tracking_url = obj.get_tracking_url()
        if tracking_url:
            return format_html('<a href="{}" target="_blank" rel="noopener">{} <i class="fas fa-external-link-alt shipping-icon-external"></i></a>', tracking_url, obj.tracking_id)
        return obj.tracking_id
    tracking_id_link.short_description = _('Tracking')

    def tracking_url_display(self, obj):
        tracking_url = obj.get_tracking_url()
        if tracking_url:
            return format_html('<a href="{}" target="_blank" rel="noopener">{}</a>', tracking_url, tracking_url)
        return '-'
    tracking_url_display.short_description = _('Tracking URL')

    def status_badge(self, obj):
        css_map = {
            'created': 'shipping-badge-status-created',
            'labeled': 'shipping-badge-status-labeled',
            'in_transit': 'shipping-badge-status-in-transit',
            'out_for_delivery': 'shipping-badge-status-out-for-delivery',
            'delivered': 'shipping-badge-status-delivered',
            'exception': 'shipping-badge-status-exception',
            'returned': 'shipping-badge-status-returned',
            'canceled': 'shipping-badge-status-canceled',
        }
        css_class = css_map.get(obj.status, 'shipping-badge-status-created')
        return format_html('<span class="shipping-badge-status {}">{}</span>', css_class, obj.get_status_display().split(' - ')[0])
    status_badge.short_description = _('Status')

    def label_preview(self, obj):
        """Display label preview with download link"""
        if not obj.label_url:
            return format_html('<em class="shipping-em-muted">{}</em>', _('No label available'))

        # Check if it's a data URI (base64 encoded)
        if obj.label_url.startswith('data:'):
            # Extract mime type and format
            mime_type = obj.label_url.split(';')[0].split(':')[1]

            if 'pdf' in mime_type:
                # PDF preview with download button
                return format_html(
                    '<div class="shipping-doc-preview">'
                    '<iframe src="{}"></iframe>'
                    '<div class="shipping-doc-actions">'
                    '<a href="{}" download="label_{}.pdf" class="button shipping-btn-label">'
                    '<i class="fas fa-download"></i> {} PDF'
                    '</a>'
                    '</div>'
                    '</div>',
                    obj.label_url,
                    obj.label_url,
                    obj.tracking_id or str(obj.id)[:8],
                    _('Download')
                )
            elif 'png' in mime_type or 'image' in mime_type:
                # PNG/Image preview with download button
                return format_html(
                    '<div class="shipping-doc-preview">'
                    '<img src="{}" alt="Shipping Label" />'
                    '<div class="shipping-doc-actions">'
                    '<a href="{}" download="label_{}.png" class="button shipping-btn-label">'
                    '<i class="fas fa-download"></i> {} PNG'
                    '</a>'
                    '</div>'
                    '</div>',
                    obj.label_url,
                    obj.label_url,
                    obj.tracking_id or str(obj.id)[:8],
                    _('Download')
                )
            else:
                # Other formats (ZPL, EPL) - show download button only
                return format_html(
                    '<div class="shipping-doc-preview">'
                    '<p class="shipping-doc-thermal-note"><em>{}</em></p>'
                    '<a href="{}" download="label_{}.txt" class="button shipping-btn-label">'
                    '<i class="fas fa-download"></i> {} Label'
                    '</a>'
                    '</div>',
                    _('Thermal printer format (ZPL/EPL)'),
                    obj.label_url,
                    obj.tracking_id or str(obj.id)[:8],
                    _('Download')
                )
        else:
            # External URL - show link
            return format_html(
                '<a href="{}" target="_blank" rel="noopener" class="button shipping-btn-label">'
                '<i class="fas fa-external-link-alt"></i> {} Label'
                '</a>',
                obj.label_url,
                _('View')
            )

    label_preview.short_description = _('Label')

    # Phase 6: Document Generation Preview Methods
    def packing_slip_preview(self, obj):
        """Display packing slip preview with download link"""
        if not obj.packing_slip_url:
            return format_html('<em class="shipping-em-muted">{}</em>', _('No packing slip available'))

        # Packing slips are always PDF data URIs
        if obj.packing_slip_url.startswith('data:'):
            return format_html(
                '<div class="shipping-doc-preview">'
                '<iframe src="{}"></iframe>'
                '<div class="shipping-doc-actions">'
                '<a href="{}" download="packing_slip_{}.pdf" class="button shipping-btn-packing-slip">'
                '<i class="fas fa-download"></i> {} Packing Slip'
                '</a>'
                '</div>'
                '</div>',
                obj.packing_slip_url,
                obj.packing_slip_url,
                obj.tracking_id or str(obj.id)[:8],
                _('Download')
            )
        else:
            # External URL
            return format_html(
                '<a href="{}" target="_blank" rel="noopener" class="button shipping-btn-packing-slip">'
                '<i class="fas fa-external-link-alt"></i> {} Packing Slip'
                '</a>',
                obj.packing_slip_url,
                _('View')
            )

    packing_slip_preview.short_description = _('Packing Slip')

    def commercial_invoice_preview(self, obj):
        """Display commercial invoice preview with download link"""
        if not obj.commercial_invoice_url:
            return format_html('<em class="shipping-em-muted">{}</em>', _('No commercial invoice available'))

        # Commercial invoices are always PDF data URIs
        if obj.commercial_invoice_url.startswith('data:'):
            return format_html(
                '<div class="shipping-doc-preview">'
                '<iframe src="{}"></iframe>'
                '<div class="shipping-doc-actions">'
                '<a href="{}" download="commercial_invoice_{}.pdf" class="button shipping-btn-invoice">'
                '<i class="fas fa-download"></i> {} Commercial Invoice'
                '</a>'
                '</div>'
                '</div>',
                obj.commercial_invoice_url,
                obj.commercial_invoice_url,
                obj.tracking_id or str(obj.id)[:8],
                _('Download')
            )
        else:
            # External URL
            return format_html(
                '<a href="{}" target="_blank" rel="noopener" class="button shipping-btn-invoice">'
                '<i class="fas fa-external-link-alt"></i> {} Commercial Invoice'
                '</a>',
                obj.commercial_invoice_url,
                _('View')
            )

    commercial_invoice_preview.short_description = _('Commercial Invoice')

    def customs_form_preview(self, obj):
        """Display customs form preview with download link"""
        if not obj.customs_form_url:
            return format_html('<em class="shipping-em-muted">{}</em>', _('No customs form available'))

        # Customs forms are always PDF data URIs
        if obj.customs_form_url.startswith('data:'):
            return format_html(
                '<div class="shipping-doc-preview">'
                '<iframe src="{}"></iframe>'
                '<div class="shipping-doc-actions">'
                '<a href="{}" download="customs_form_{}.pdf" class="button shipping-btn-customs">'
                '<i class="fas fa-download"></i> {} Customs Form'
                '</a>'
                '</div>'
                '</div>',
                obj.customs_form_url,
                obj.customs_form_url,
                obj.tracking_id or str(obj.id)[:8],
                _('Download')
            )
        else:
            # External URL
            return format_html(
                '<a href="{}" target="_blank" rel="noopener" class="button shipping-btn-customs">'
                '<i class="fas fa-external-link-alt"></i> {} Customs Form'
                '</a>',
                obj.customs_form_url,
                _('View')
            )

    customs_form_preview.short_description = _('Customs Form')

    def purchase_labels(self, request, queryset):
        """Admin action to purchase labels for selected shipments"""
        from shipping.jobs.tasks import buy_label

        # Filter for shipments that can have labels purchased
        valid_shipments = queryset.filter(
            status='created',
            provider_account__isnull=False,
            provider_account__is_active=True
        )

        if not valid_shipments.exists():
            self.message_user(
                request,
                _('No valid shipments selected. Shipments must be in "created" status and have an active provider account.'),
                level='warning'
            )
            return

        # Queue Celery tasks for each shipment
        queued_count = 0
        for shipment in valid_shipments:
            try:
                buy_label.delay(str(shipment.id))
                queued_count += 1
            except Exception as e:
                self.message_user(
                    request,
                    _('Failed to queue label purchase for shipment %(id)s: %(error)s') % {
                        'id': str(shipment.id)[:8],
                        'error': str(e)
                    },
                    level='error'
                )

        if queued_count > 0:
            self.message_user(
                request,
                _('Successfully queued %(count)d label purchase task(s). Labels will be generated in the background.') % {
                    'count': queued_count
                },
                level='success'
            )

    purchase_labels.short_description = _('Purchase shipping labels for selected shipments')

    # Phase 6: Document Generation Admin Actions
    def generate_packing_slips(self, request, queryset):
        """Admin action to generate packing slips for selected shipments"""
        from shipping.services.document_service import DocumentService

        generated_count = 0
        error_count = 0

        for shipment in queryset:
            try:
                # Generate packing slip
                data_uri = DocumentService.generate_packing_slip(shipment)
                shipment.packing_slip_url = data_uri
                shipment.save(update_fields=['packing_slip_url'])
                generated_count += 1
            except Exception as e:
                error_count += 1
                self.message_user(
                    request,
                    _('Failed to generate packing slip for shipment %(id)s: %(error)s') % {
                        'id': str(shipment.id)[:8],
                        'error': str(e)
                    },
                    level='error'
                )

        if generated_count > 0:
            self.message_user(
                request,
                _('Successfully generated %(count)d packing slip(s).') % {
                    'count': generated_count
                },
                level='success'
            )

        if error_count > 0:
            self.message_user(
                request,
                _('Failed to generate %(count)d packing slip(s). See errors above.') % {
                    'count': error_count
                },
                level='warning'
            )

    generate_packing_slips.short_description = _('Generate packing slips for selected shipments')

    def generate_commercial_invoices(self, request, queryset):
        """Admin action to generate commercial invoices for selected shipments"""
        from shipping.services.document_service import DocumentService

        generated_count = 0
        error_count = 0

        for shipment in queryset:
            try:
                # Generate commercial invoice
                data_uri = DocumentService.generate_commercial_invoice(shipment)
                shipment.commercial_invoice_url = data_uri
                shipment.save(update_fields=['commercial_invoice_url'])
                generated_count += 1
            except Exception as e:
                error_count += 1
                self.message_user(
                    request,
                    _('Failed to generate commercial invoice for shipment %(id)s: %(error)s') % {
                        'id': str(shipment.id)[:8],
                        'error': str(e)
                    },
                    level='error'
                )

        if generated_count > 0:
            self.message_user(
                request,
                _('Successfully generated %(count)d commercial invoice(s).') % {
                    'count': generated_count
                },
                level='success'
            )

        if error_count > 0:
            self.message_user(
                request,
                _('Failed to generate %(count)d commercial invoice(s). See errors above.') % {
                    'count': error_count
                },
                level='warning'
            )

    generate_commercial_invoices.short_description = _('Generate commercial invoices for selected shipments')

    def generate_customs_forms(self, request, queryset):
        """Admin action to generate customs forms for selected shipments"""
        from shipping.services.document_service import DocumentService

        generated_count = 0
        error_count = 0

        for shipment in queryset:
            try:
                # Determine form type based on shipment characteristics
                # CN22: up to 2kg and value <= 425 EUR
                # CN23: over 2kg or value > 425 EUR
                # For simplicity, we'll use CN23 as default (more comprehensive)
                form_type = 'CN23'

                # Generate customs form
                data_uri = DocumentService.generate_customs_form(shipment, form_type=form_type)
                shipment.customs_form_url = data_uri
                shipment.save(update_fields=['customs_form_url'])
                generated_count += 1
            except Exception as e:
                error_count += 1
                self.message_user(
                    request,
                    _('Failed to generate customs form for shipment %(id)s: %(error)s') % {
                        'id': str(shipment.id)[:8],
                        'error': str(e)
                    },
                    level='error'
                )

        if generated_count > 0:
            self.message_user(
                request,
                _('Successfully generated %(count)d customs form(s).') % {
                    'count': generated_count
                },
                level='success'
            )

        if error_count > 0:
            self.message_user(
                request,
                _('Failed to generate %(count)d customs form(s). See errors above.') % {
                    'count': error_count
                },
                level='warning'
            )

    generate_customs_forms.short_description = _('Generate customs forms (CN23) for selected shipments')


@admin.register(TrackingEvent)
class TrackingEventAdmin(admin.ModelAdmin):
    """Admin for tracking events (read-only)"""

    change_list_template = 'admin/shipping/trackingevent/change_list.html'

    list_display = ['id_short', 'shipment_link', 'status_badge', 'description', 'location', 'occurred_at']
    list_filter = ['status', 'occurred_at', 'created_at']
    search_fields = ['shipment__tracking_id', 'shipment__order__order_number', 'description', 'location']
    readonly_fields = ['shipment', 'status', 'description', 'location', 'occurred_at', 'raw', 'created_at']
    date_hierarchy = 'occurred_at'

    class Media:
        css = {
            'all': ('shipping/css/admin_badges.css',)
        }

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def id_short(self, obj):
        return str(obj.id)[:8]
    id_short.short_description = _('ID')

    def shipment_link(self, obj):
        if obj.shipment:
            url = reverse('admin:shipping_shipment_change', args=[obj.shipment.pk])
            return format_html('<a href="{}">{}</a>', url, obj.shipment.tracking_id or str(obj.shipment.id)[:8])
        return '-'
    shipment_link.short_description = _('Shipment')

    def status_badge(self, obj):
        css_map = {
            'info_received': 'shipping-badge-status-info-received',
            'in_transit': 'shipping-badge-status-in-transit',
            'out_for_delivery': 'shipping-badge-status-out-for-delivery',
            'delivered': 'shipping-badge-status-delivered',
            'exception': 'shipping-badge-status-exception',
            'returned': 'shipping-badge-status-returned',
        }
        css_class = css_map.get(obj.status, 'shipping-badge-status-info-received')
        return format_html('<span class="shipping-badge-status {}">{}</span>', css_class, obj.get_status_display().upper())
    status_badge.short_description = _('Status')

    def changelist_view(self, request, extra_context=None):
        """Add context for the custom change list template"""
        extra_context = extra_context or {}
        extra_context['info_received_count'] = TrackingEvent.objects.filter(status='info_received').count()
        extra_context['in_transit_count'] = TrackingEvent.objects.filter(status='in_transit').count()
        extra_context['out_for_delivery_count'] = TrackingEvent.objects.filter(status='out_for_delivery').count()
        extra_context['delivered_count'] = TrackingEvent.objects.filter(status='delivered').count()
        extra_context['exception_count'] = TrackingEvent.objects.filter(status='exception').count()
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(WebhookLog)
class WebhookLogAdmin(admin.ModelAdmin):
    """Admin for webhook logs (read-only)"""

    change_list_template = 'admin/shipping/webhooklog/change_list.html'

    list_display = ['id_short', 'provider_key', 'endpoint', 'status_code_display', 'processing_status_badge', 'received_at']
    list_filter = ['provider_key', 'processing_status', 'status_code', 'received_at']
    search_fields = ['provider_key', 'endpoint', 'error_message']
    readonly_fields = ['provider_key', 'endpoint', 'payload', 'headers', 'status_code', 'processing_status', 'error_message', 'received_at', 'processed_at']
    date_hierarchy = 'received_at'

    class Media:
        css = {
            'all': ('shipping/css/admin_badges.css',)
        }

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def id_short(self, obj):
        return str(obj.id)[:8]
    id_short.short_description = _('ID')

    def status_code_display(self, obj):
        if not obj.status_code:
            return '-'
        if 200 <= obj.status_code < 300:
            css_class = 'shipping-text-http-success'
        elif 400 <= obj.status_code < 500:
            css_class = 'shipping-text-http-client-error'
        else:
            css_class = 'shipping-text-http-server-error'
        return format_html('<span class="{}">{}</span>', css_class, obj.status_code)
    status_code_display.short_description = _('Status Code')

    def processing_status_badge(self, obj):
        css_map = {'pending': 'shipping-badge-status-pending', 'processed': 'shipping-badge-status-processed', 'failed': 'shipping-badge-status-failed'}
        css_class = css_map.get(obj.processing_status, 'shipping-badge-status-pending')
        return format_html('<span class="shipping-badge-status {}">{}</span>', css_class, obj.get_processing_status_display().upper())
    processing_status_badge.short_description = _('Processing')

    def changelist_view(self, request, extra_context=None):
        """Add context for the custom change list template"""
        extra_context = extra_context or {}
        extra_context['pending_count'] = WebhookLog.objects.filter(processing_status='pending').count()
        extra_context['processed_count'] = WebhookLog.objects.filter(processing_status='processed').count()
        extra_context['failed_count'] = WebhookLog.objects.filter(processing_status='failed').count()
        extra_context['providers'] = WebhookLog.objects.values_list('provider_key', flat=True).distinct()
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(ShippingZone)
class ShippingZoneAdmin(admin.ModelAdmin):
    """Admin for shipping zones with modern card-based interface"""

    # Use custom change_list and change_form templates
    change_list_template = 'admin/shipping/shippingzone/change_list.html'
    change_form_template = 'admin/shipping/shippingzone/change_form.html'
    form = ShippingZoneAdminForm

    def add_view(self, request, form_url='', extra_context=None):
        """Redirect to zone wizard instead of default add form."""
        from django.http import HttpResponseRedirect

        # Clear any stale wizard session data
        if 'zone_wizard_data' in request.session:
            del request.session['zone_wizard_data']

        return HttpResponseRedirect(reverse('shipping:zone_wizard_step1'))

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Add context data for the edit form."""
        from django_countries import countries as django_countries_list

        extra_context = extra_context or {}

        all_countries = [
            {'code': code, 'name': str(name)}
            for code, name in django_countries_list
        ]

        # Get the zone being edited
        zone = self.get_object(request, object_id)
        if zone:
            extra_context['zone'] = zone
            extra_context['zone_edit_config'] = {
                'allCountries': all_countries,
                'zone': {
                    'countries': zone.countries,
                    'states': zone.states,
                    'postalCodePatterns': zone.postal_code_patterns,
                }
            }
        else:
            extra_context['zone_edit_config'] = {}

        return super().change_view(request, object_id, form_url, extra_context)

    # Show all zones on one page for client-side filtering
    list_per_page = 1000

    list_display = [
        'name',
        'priority_badge',
        'coverage_summary_display',
        'shipping_methods_count',
        'is_active_badge',
        'created_at',
    ]
    list_filter = ['is_active', 'priority', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'coverage_details_display']
    ordering = ['priority', 'name']

    class Media:
        css = {
            'all': ('shipping/css/admin_shipping_zone.css',)
        }
        js = ('shipping/js/admin_shipping_zone.js',)

    fieldsets = (
        (_('Zone Information'), {
            'fields': ('name', 'description', 'priority', 'is_active')
        }),
        (_('Geographic Coverage'), {
            'fields': ('countries', 'states', 'postal_code_patterns'),
            'description': mark_safe(
                '<div class="info-box">'
                '<strong>' + str(_('Zone Configuration:')) + '</strong><br/>'
                + str(_('Define the geographic areas covered by this shipping zone.')) + '<br/>'
                + str(_('- <strong>Countries:</strong> List of ISO 3166-1 alpha-2 country codes (e.g., ["US", "CA", "MX"]). Leave empty for all countries.')) + '<br/>'
                + str(_('- <strong>States:</strong> Dict mapping country codes to state codes (e.g., {"US": ["CA", "NY"], "CA": ["ON", "BC"]}).')) + '<br/>'
                + str(_('- <strong>Postal Patterns:</strong> List of regex patterns for postal codes (e.g., ["^90[0-9]{3}$"] for Los Angeles area).')) +
                '</div>'
            )
        }),
        (_('Coverage Summary'), {
            'fields': ('coverage_details_display',),
            'classes': ('collapse',)
        }),
        (_('Metadata'), {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def priority_badge(self, obj):
        """Display priority as a badge"""
        if obj.priority == 0:
            return format_html('<span class="priority-badge highest">P0 - HIGHEST</span>')
        elif obj.priority <= 5:
            return format_html('<span class="priority-badge high">P{}</span>', obj.priority)
        elif obj.priority <= 10:
            return format_html('<span class="priority-badge medium">P{}</span>', obj.priority)
        else:
            return format_html('<span class="priority-badge low">P{}</span>', obj.priority)
    priority_badge.short_description = _('Priority')
    priority_badge.admin_order_field = 'priority'

    def coverage_summary_display(self, obj):
        """Display coverage summary"""
        return format_html('<span class="coverage-summary">{}</span>', obj.get_coverage_summary())
    coverage_summary_display.short_description = _('Coverage')

    def coverage_details_display(self, obj):
        """Display detailed coverage information"""
        html = '<div class="coverage-details">'

        # Countries
        if obj.countries:
            html += '<div class="coverage-section"><strong>' + str(_('Countries:')) + '</strong><br/>'
            html += '<div class="country-list">'
            for country_code in obj.countries:
                html += f'<span class="country-badge">{country_code}</span>'
            html += '</div></div>'
        else:
            html += '<div class="coverage-section"><em>' + str(_('All countries')) + '</em></div>'

        # States
        if obj.states:
            html += '<div class="coverage-section"><strong>' + str(_('States/Provinces:')) + '</strong><br/>'
            for country, states in obj.states.items():
                html += f'<div class="state-group"><strong>{country}:</strong> '
                html += ', '.join(states)
                html += '</div>'
            html += '</div>'

        # Postal code patterns
        if obj.postal_code_patterns:
            html += '<div class="coverage-section"><strong>' + str(_('Postal Code Patterns:')) + '</strong><br/>'
            html += '<ul class="postal-patterns">'
            for pattern in obj.postal_code_patterns:
                html += f'<li><code>{pattern}</code></li>'
            html += '</ul></div>'

        html += '</div>'
        return format_html(html)
    coverage_details_display.short_description = _('Coverage Details')

    def shipping_methods_count(self, obj):
        """Display count of shipping methods assigned to this zone"""
        count = obj.shipping_methods.count()
        if count > 0:
            return format_html('<span class="methods-count active">{} {}</span>', count, _('methods'))
        return format_html('<span class="methods-count empty">{}</span>', _('No methods'))
    shipping_methods_count.short_description = _('Shipping Methods')

    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span class="status-badge active">ACTIVE</span>')
        return format_html('<span class="status-badge inactive">INACTIVE</span>')
    is_active_badge.short_description = _('Status')
    is_active_badge.admin_order_field = 'is_active'

    def changelist_view(self, request, extra_context=None):
        """Add custom context data for the zone list view"""
        from django.db.models import Count, Q

        extra_context = extra_context or {}

        # Get all zones
        all_zones = ShippingZone.objects.all()

        # Status counts
        extra_context['active_count'] = all_zones.filter(is_active=True).count()
        extra_context['inactive_count'] = all_zones.filter(is_active=False).count()

        # Priority distribution
        extra_context['high_priority_count'] = all_zones.filter(priority__lte=5).count()
        extra_context['medium_priority_count'] = all_zones.filter(priority__gt=5, priority__lte=10).count()
        extra_context['low_priority_count'] = all_zones.filter(priority__gt=10).count()

        # Zones with/without methods
        extra_context['zones_with_methods'] = all_zones.annotate(
            methods_count=Count('shipping_methods')
        ).filter(methods_count__gt=0).count()
        extra_context['zones_without_methods'] = all_zones.annotate(
            methods_count=Count('shipping_methods')
        ).filter(methods_count=0).count()

        return super().changelist_view(request, extra_context=extra_context)

    def get_queryset(self, request):
        """Filter queryset based on request parameters"""
        from django.db.models import Q, Count

        qs = super().get_queryset(request).annotate(
            methods_count=Count('shipping_methods')
        )

        # Status filter
        is_active = request.GET.get('is_active')
        if is_active:
            qs = qs.filter(is_active=(is_active == '1'))

        # Priority filter
        priority = request.GET.get('priority')
        if priority == 'high':
            qs = qs.filter(priority__lte=5)
        elif priority == 'medium':
            qs = qs.filter(priority__gt=5, priority__lte=10)
        elif priority == 'low':
            qs = qs.filter(priority__gt=10)

        # Methods filter
        has_methods = request.GET.get('has_methods')
        if has_methods == '1':
            qs = qs.filter(methods_count__gt=0)
        elif has_methods == '0':
            qs = qs.filter(methods_count=0)

        # Search query
        search = request.GET.get('q')
        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )

        return qs

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


# ============================================================================
# Shipping Promotions Admin
# ============================================================================

class ShippingRateTierInline(admin.TabularInline):
    """Inline display of rate tiers for rate tables"""
    model = ShippingRateTier
    extra = 1
    fields = ['min_value', 'max_value', 'rate', 'is_active']

    def get_formset(self, request, obj=None, **kwargs):
        """Limit currency choices to enabled currencies from site settings"""
        formset = super().get_formset(request, obj, **kwargs)
        from core.admin_mixins import _apply_money_field_currency_defaults
        _apply_money_field_currency_defaults(formset.form, obj)
        return formset


@admin.register(ShippingRateTable)
class ShippingRateTableAdmin(admin.ModelAdmin):
    """Admin for shipping rate tables (tiered pricing)"""

    list_display = [
        'name',
        'basis_type',
        'shipping_method',
        'tier_count',
        'is_active_badge',
        'created_at',
    ]

    list_filter = [
        'is_active',
        'basis_type',
        'created_at',
    ]

    search_fields = ['name', 'description']

    readonly_fields = ['created_at', 'updated_at', 'created_by']

    inlines = [ShippingRateTierInline]

    class Media:
        css = {
            'all': ('shipping/css/admin_badges.css',)
        }

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'description', 'is_active')
        }),
        (_('Table Configuration'), {
            'fields': ('basis_type', 'shipping_method'),
            'description': _('Basis type determines what value is used for tier lookup: weight, price, or quantity')
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at', 'created_by'),
            'classes': ('collapse',)
        }),
    )

    def is_active_badge(self, obj):
        """Display active status as badge"""
        if obj.is_active:
            return format_html(
                '<span class="shipping-text-success-bold">&#10003; {}</span>',
                _('Active')
            )
        return format_html(
            '<span class="shipping-text-muted">&#9675; {}</span>',
            _('Inactive')
        )
    is_active_badge.short_description = _('Status')

    def tier_count(self, obj):
        """Count of tiers in this table"""
        count = obj.tiers.count()
        if count == 0:
            return format_html('<span class="shipping-text-danger">&#9888; 0 tiers</span>')
        return format_html('<span class="shipping-text-success">{} tiers</span>', count)
    tier_count.short_description = _('Tiers')


    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ShippingPromotion)
class ShippingPromotionAdmin(admin.ModelAdmin):
    """Admin for shipping promotions (conditional logic)"""

    change_list_template = 'admin/shipping/shippingpromotion/change_list.html'
    change_form_template = 'admin/shipping/shippingpromotion/change_form.html'

    class Media:
        css = {
            'all': ('shipping/css/admin_badges.css',)
        }

    list_display = [
        'name',
        'promotion_type_badge',
        'promotion_value',
        'priority',
        'zones_display',
        'time_valid_badge',
        'is_active_badge',
        'stop_further_promotions',
        'created_at',
    ]

    list_filter = [
        'is_active',
        'promotion_type',
        'stop_further_promotions',
        'first_time_customers_only',
        'created_at',
    ]

    search_fields = ['name', 'description']

    readonly_fields = [
        'created_at',
        'updated_at',
        'created_by',
        'time_validity_display',
        'conditions_summary',
    ]

    autocomplete_fields = [
        'zones',
        'shipping_methods',
        'requires_products',
        'requires_categories',
        'excludes_products',
        'excludes_categories',
    ]

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'description', 'is_active'),
            'classes': ('tab-basic',)
        }),
        (_('Promotion Action'), {
            'fields': ('promotion_type', 'promotion_value'),
            'classes': ('tab-action',)
        }),
        (_('Cart Conditions'), {
            'fields': (
                'min_cart_value', 'max_cart_value',
                'min_cart_weight', 'max_cart_weight',
                'min_item_count', 'max_item_count',
            ),
            'classes': ('tab-cart',)
        }),
        (_('Geographic Restrictions'), {
            'fields': ('zones',),
            'classes': ('tab-zones',)
        }),
        (_('Shipping Method Restrictions'), {
            'fields': ('shipping_methods',),
            'classes': ('tab-methods',)
        }),
        (_('Product/Category Restrictions'), {
            'fields': (
                'requires_products', 'requires_categories',
                'excludes_products', 'excludes_categories',
            ),
            'classes': ('tab-products',)
        }),
        (_('Customer Restrictions'), {
            'fields': ('customer_groups', 'first_time_customers_only'),
            'classes': ('tab-customers',)
        }),
        (_('Time Restrictions'), {
            'fields': ('start_date', 'end_date', 'time_validity_display'),
            'classes': ('tab-time',)
        }),
        (_('Promotion Behavior'), {
            'fields': ('priority', 'stop_further_promotions', 'controls_visibility'),
            'classes': ('tab-behavior',)
        }),
        (_('Conditions Summary'), {
            'fields': ('conditions_summary',),
            'classes': ('tab-summary',)
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at', 'created_by'),
            'classes': ('tab-metadata',)
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        """Override to filter MoneyField currency choices"""
        form = super().get_form(request, obj, **kwargs)
        from core.admin_mixins import _apply_money_field_currency_defaults
        _apply_money_field_currency_defaults(form, obj)
        return form

    def promotion_type_badge(self, obj):
        """Display promotion type with color coding"""
        css_map = {
            'free_shipping': 'shipping-text-rule-free',
            'discount_percentage': 'shipping-text-rule-discount',
            'discount_fixed': 'shipping-text-rule-discount',
            'override_cost': 'shipping-text-rule-set-cost',
            'surcharge_fixed': 'shipping-text-rule-surcharge',
            'surcharge_percentage': 'shipping-text-rule-surcharge',
        }
        css_class = css_map.get(obj.promotion_type, 'shipping-text-rule-default')
        return format_html(
            '<span class="{}">{}</span>',
            css_class,
            obj.get_promotion_type_display()
        )
    promotion_type_badge.short_description = _('Promotion Type')

    def is_active_badge(self, obj):
        """Display active status as badge"""
        if obj.is_active:
            return format_html(
                '<span class="shipping-text-success-bold">&#10003; {}</span>',
                _('Active')
            )
        return format_html(
            '<span class="shipping-text-muted">&#9675; {}</span>',
            _('Inactive')
        )
    is_active_badge.short_description = _('Status')

    def time_valid_badge(self, obj):
        """Display if rule is currently time-valid"""
        if obj.is_time_valid():
            return format_html(
                '<span class="shipping-text-success">&#10003; {}</span>',
                _('Valid now')
            )
        return format_html(
            '<span class="shipping-text-danger">&#10007; {}</span>',
            _('Not valid')
        )
    time_valid_badge.short_description = _('Time Status')

    def time_validity_display(self, obj):
        """Show time validity in readonly field"""
        now = timezone.now()
        parts = []

        if obj.start_date:
            if now < obj.start_date:
                parts.append(format_html(
                    '<span class="shipping-text-danger">&#9888; Not yet active (starts {})</span>',
                    obj.start_date
                ))
            else:
                parts.append(format_html(
                    '<span class="shipping-text-success">&#10003; Active since {}</span>',
                    obj.start_date
                ))

        if obj.end_date:
            if now > obj.end_date:
                parts.append(format_html(
                    '<span class="shipping-text-danger">&#10007; Expired on {}</span>',
                    obj.end_date
                ))
            else:
                parts.append(format_html(
                    '<span class="shipping-text-success">Valid until {}</span>',
                    obj.end_date
                ))

        if not parts:
            return _('No time restrictions')

        return format_html('<br>'.join(parts))
    time_validity_display.short_description = _('Time Validity')

    def zones_display(self, obj):
        """Display number of zones"""
        count = obj.zones.count()
        if count == 0:
            return _('All zones')
        return _('{count} zones').format(count=count)
    zones_display.short_description = _('Zones')

    def conditions_summary(self, obj):
        """Generate summary of all conditions"""
        conditions = []

        # Cart value conditions
        if obj.min_cart_value:
            conditions.append(f"Min cart value: {obj.min_cart_value}")
        if obj.max_cart_value:
            conditions.append(f"Max cart value: {obj.max_cart_value}")

        # Weight conditions
        if obj.min_cart_weight:
            conditions.append(f"Min weight: {obj.min_cart_weight}kg")
        if obj.max_cart_weight:
            conditions.append(f"Max weight: {obj.max_cart_weight}kg")

        # Item count
        if obj.min_item_count:
            conditions.append(f"Min items: {obj.min_item_count}")
        if obj.max_item_count:
            conditions.append(f"Max items: {obj.max_item_count}")

        # Geographic
        zone_count = obj.zones.count()
        if zone_count > 0:
            conditions.append(f"Applies to {zone_count} specific zones")

        # Methods
        method_count = obj.shipping_methods.count()
        if method_count > 0:
            conditions.append(f"Applies to {method_count} specific shipping methods")

        # Products/Categories
        if obj.requires_products.exists():
            conditions.append(f"Requires {obj.requires_products.count()} specific products")
        if obj.requires_categories.exists():
            conditions.append(f"Requires {obj.requires_categories.count()} categories")
        if obj.excludes_products.exists():
            conditions.append(f"Excludes {obj.excludes_products.count()} products")
        if obj.excludes_categories.exists():
            conditions.append(f"Excludes {obj.excludes_categories.count()} categories")

        # Customer restrictions
        if obj.customer_groups.exists():
            conditions.append(f"Limited to {obj.customer_groups.count()} customer groups")
        if obj.first_time_customers_only:
            conditions.append("First-time customers only")

        # Time restrictions
        if obj.start_date:
            conditions.append(f"Active from: {obj.start_date}")
        if obj.end_date:
            conditions.append(f"Active until: {obj.end_date}")

        if not conditions:
            return format_html('<span class="shipping-text-muted">No conditions (rule applies to all)</span>')

        items = format_html_join('', '<li>{}</li>', ((cond,) for cond in conditions))
        return format_html('<ul>{}</ul>', items)
    conditions_summary.short_description = _('All Conditions')

    def changelist_view(self, request, extra_context=None):
        """Add custom context for card-based list view"""
        extra_context = extra_context or {}

        # Get queryset
        queryset = self.get_queryset(request)

        # Active/Inactive counts
        extra_context['active_count'] = queryset.filter(is_active=True).count()
        extra_context['inactive_count'] = queryset.filter(is_active=False).count()

        # Promotion type counts
        extra_context['free_shipping_count'] = queryset.filter(promotion_type='free_shipping').count()
        extra_context['discount_percentage_count'] = queryset.filter(promotion_type='discount_percentage').count()
        extra_context['discount_fixed_count'] = queryset.filter(promotion_type='discount_fixed').count()
        extra_context['override_cost_count'] = queryset.filter(promotion_type='override_cost').count()
        extra_context['surcharge_fixed_count'] = queryset.filter(promotion_type='surcharge_fixed').count()
        extra_context['surcharge_percentage_count'] = queryset.filter(promotion_type='surcharge_percentage').count()

        # Priority counts (high >= 50, medium 0-49, low < 0)
        extra_context['high_priority_count'] = queryset.filter(priority__gte=50).count()
        extra_context['medium_priority_count'] = queryset.filter(priority__gte=0, priority__lt=50).count()
        extra_context['low_priority_count'] = queryset.filter(priority__lt=0).count()

        return super().changelist_view(request, extra_context)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


# ============================================================================
# Location Admin
# ============================================================================

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Admin interface for Location model."""

    list_display = [
        'name',
        'code',
        'location_type_badge',
        'city',
        'state',
        'country',
        'accepts_pickup_badge',
        'accepts_delivery_badge',
        'coordinates_badge',
        'is_active_badge',
    ]

    list_filter = [
        'is_active',
        'location_type',
        'accepts_pickup',
        'accepts_delivery_dispatch',
        'country',
        'state',
        'created_at',
    ]

    search_fields = [
        'name',
        'code',
        'city',
        'state',
        'postal_code',
        'address1',
        'phone',
        'email',
    ]

    class Media:
        css = {
            'all': ('shipping/css/admin_badges.css',)
        }

    fieldsets = [
        (_('Basic Information'), {
            'fields': [
                'name',
                'code',
                'location_type',
                'is_active',
            ]
        }),
        (_('Address'), {
            'fields': [
                'address1',
                'address2',
                'city',
                'state',
                'postal_code',
                'country',
            ]
        }),
        (_('Geocoding'), {
            'fields': [
                'latitude',
                'longitude',
            ],
            'description': _('Coordinates for distance calculations and mapping'),
        }),
        (_('Contact Information'), {
            'fields': [
                'phone',
                'email',
            ]
        }),
        (_('Operating Hours'), {
            'fields': [
                'operating_hours',
            ],
            'description': _(
                'JSON format: {"monday": {"open": "09:00", "close": "17:00", "closed": false}, ...}'
            ),
        }),
        (_('Pickup Configuration'), {
            'fields': [
                'accepts_pickup',
                'max_daily_pickups',
                'pickup_preparation_time',
                'pickup_instructions',
            ]
        }),
        (_('Delivery Configuration'), {
            'fields': [
                'accepts_delivery_dispatch',
                'delivery_radius',
                'delivery_notes',
            ]
        }),
        (_('Shipping Zones'), {
            'fields': [
                'zones',
            ]
        }),
        (_('Metadata'), {
            'fields': [
                'created_by',
                'created_at',
                'updated_at',
            ],
            'classes': ['collapse'],
        }),
    ]

    readonly_fields = ['created_at', 'updated_at', 'created_by']
    filter_horizontal = ['zones']

    def location_type_badge(self, obj):
        """Display location type with color coding."""
        css_map = {
            'store': 'shipping-text-loc-store',
            'warehouse': 'shipping-text-loc-warehouse',
            'fulfillment_center': 'shipping-text-loc-fulfillment',
            'dispatch_center': 'shipping-text-loc-dispatch',
        }
        css_class = css_map.get(obj.location_type, 'shipping-text-loc-default')
        return format_html(
            '<span class="{}">{}</span>',
            css_class,
            obj.get_location_type_display()
        )
    location_type_badge.short_description = _('Type')

    def accepts_pickup_badge(self, obj):
        """Display pickup acceptance status."""
        if not obj.is_active:
            return format_html('<span class="shipping-text-muted">Inactive</span>')
        if obj.accepts_pickup:
            return format_html('<span class="shipping-text-success">&#10003; Pickup</span>')
        return format_html('<span class="shipping-text-danger">&#10007; No Pickup</span>')
    accepts_pickup_badge.short_description = _('Pickup')

    def accepts_delivery_badge(self, obj):
        """Display delivery dispatch acceptance status."""
        if not obj.is_active:
            return format_html('<span class="shipping-text-muted">Inactive</span>')
        if obj.accepts_delivery_dispatch:
            radius = f" ({obj.delivery_radius}km)" if obj.delivery_radius else ""
            return format_html(
                '<span class="shipping-text-success">&#10003; Delivery{}</span>',
                radius
            )
        return format_html('<span class="shipping-text-danger">&#10007; No Delivery</span>')
    accepts_delivery_badge.short_description = _('Delivery')

    def coordinates_badge(self, obj):
        """Display coordinate availability."""
        if obj.coordinates:
            lat, lon = obj.coordinates
            return format_html(
                '<span class="shipping-text-success" title="Lat: {}, Lon: {}">&#10003; Mapped</span>',
                lat, lon
            )
        return format_html('<span class="shipping-text-warning">&#9888; No Coords</span>')
    coordinates_badge.short_description = _('Coords')

    def is_active_badge(self, obj):
        """Display active status as badge."""
        if obj.is_active:
            return format_html('<span class="shipping-badge-active">ACTIVE</span>')
        return format_html('<span class="shipping-badge-error">INACTIVE</span>')
    is_active_badge.short_description = _('Status')

    def save_model(self, request, obj, form, change):
        """Set created_by on new locations."""
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
