"""
Django Admin interface for GeoIP
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse, path
from django.utils.safestring import mark_safe
from django.db.models import Count, Q, Avg, Sum, F, Case, When, BooleanField
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.template.response import TemplateResponse

from .models import (
    GeoLocation,
    CountryMapping,
    GeoIPProvider,
    VisitorLocation,
    BusinessRule,
    PageView,
    DailyPageStats,
    DailyTrafficStats,
)
from .templatetags.geoip_tags import country_flag as _country_code_to_flag


@admin.register(GeoLocation)
class GeoLocationAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'country_flag', 'country_code', 'city_name',
                    'source', 'confidence_display', 'is_expired_display', 'resolved_at']
    list_filter = ['source', 'is_proxy', 'is_vpn', 'is_tor', 'is_mobile', 'country_code']
    search_fields = ['ip_address', 'country_code', 'city_name']
    readonly_fields = ['resolved_at', 'updated_at']
    change_list_template = 'admin/geoip/geolocation/change_list.html'

    fieldsets = (
        (_('IP Information'), {
            'fields': ('ip_address', 'ip_prefix')
        }),
        (_('Location'), {
            'fields': ('country_code', 'country_name', 'region_code', 'region_name',
                      'city_name', 'postal_code', 'latitude', 'longitude')
        }),
        (_('Network'), {
            'fields': ('asn', 'isp')
        }),
        (_('Metadata'), {
            'fields': ('source', 'confidence', 'is_proxy', 'is_vpn', 'is_tor', 'is_mobile')
        }),
        (_('Timestamps'), {
            'fields': ('resolved_at', 'updated_at', 'expires_at')
        })
    )

    def country_flag(self, obj):
        if obj.country_code:
            flag = _country_code_to_flag(obj.country_code)
            return format_html('{} {}', flag, obj.country_code)
        return '-'
    country_flag.short_description = 'Country'

    def confidence_display(self, obj):
        confidence = obj.confidence * 100
        if confidence >= 80:
            css_class = 'geoip-confidence-high'
        elif confidence >= 50:
            css_class = 'geoip-confidence-medium'
        else:
            css_class = 'geoip-confidence-low'
        return format_html(
            '<span class="{}">{}%</span>',
            css_class, int(confidence)
        )
    confidence_display.short_description = 'Confidence'

    def is_expired_display(self, obj):
        if obj.is_expired:
            return format_html('<span class="geoip-status-expired">❌ Expired</span>')
        return format_html('<span class="geoip-status-valid">✓ Valid</span>')
    is_expired_display.short_description = 'Status'

    def changelist_view(self, request, extra_context=None):
        """Override changelist view to add dashboard statistics"""
        extra_context = extra_context or {}

        # Time ranges
        now = timezone.now()
        last_24h = now - timedelta(hours=24)
        last_7d = now - timedelta(days=7)
        last_30d = now - timedelta(days=30)

        # Overall statistics
        total_locations = GeoLocation.objects.count()
        expired_locations = GeoLocation.objects.filter(expires_at__lt=now).count()

        # Recent activity
        recent_24h = GeoLocation.objects.filter(resolved_at__gte=last_24h).count()
        recent_7d = GeoLocation.objects.filter(resolved_at__gte=last_7d).count()

        # Top countries
        top_countries = (GeoLocation.objects
            .values('country_code', 'country_name')
            .annotate(count=Count('id'))
            .order_by('-count')[:10])

        # Source distribution
        source_stats = (GeoLocation.objects
            .values('source')
            .annotate(count=Count('id'), avg_confidence=Avg('confidence'))
            .order_by('-count'))

        # Threat detection
        vpn_count = GeoLocation.objects.filter(is_vpn=True).count()
        proxy_count = GeoLocation.objects.filter(is_proxy=True).count()
        tor_count = GeoLocation.objects.filter(is_tor=True).count()

        # Provider statistics
        providers = GeoIPProvider.objects.all().order_by('priority')
        configured_providers = list(
            providers.filter(is_active=True).values_list('provider_type', flat=True)
        )

        # Country mappings
        total_countries = CountryMapping.objects.count()
        active_countries = CountryMapping.objects.filter(is_active=True).count()

        # Visitor statistics
        total_visitors = VisitorLocation.objects.count()
        recent_visitors = VisitorLocation.objects.filter(last_seen__gte=last_24h).count()

        # Accuracy metrics
        corrections = VisitorLocation.objects.exclude(actual_country__isnull=True).exclude(
            actual_country=F('resolved_country')).count()

        accuracy_rate = 100
        if total_visitors > 0:
            accuracy_rate = ((total_visitors - corrections) / total_visitors) * 100

        extra_context.update({
            'total_locations': total_locations,
            'expired_locations': expired_locations,
            'recent_24h': recent_24h,
            'recent_7d': recent_7d,
            'top_countries': top_countries,
            'source_stats': source_stats,
            'vpn_count': vpn_count,
            'proxy_count': proxy_count,
            'tor_count': tor_count,
            'providers': providers,
            'configured_providers': configured_providers,
            'total_countries': total_countries,
            'active_countries': active_countries,
            'total_visitors': total_visitors,
            'recent_visitors': recent_visitors,
            'accuracy_rate': accuracy_rate,
            'corrections': corrections,
        })

        return super().changelist_view(request, extra_context=extra_context)


@admin.register(CountryMapping)
class CountryMappingAdmin(admin.ModelAdmin):
    list_display = ['country_flag_display', 'country_code', 'country_name',
                    'default_currency', 'default_language', 'is_eu_member',
                    'requires_vat', 'is_active']
    list_filter = ['is_active', 'is_eu_member', 'requires_vat', 'supports_cod', 'default_currency']
    search_fields = ['country_code', 'country_name']
    list_editable = ['is_active', 'default_currency', 'default_language']
    change_list_template = 'admin/geoip/countrymapping/change_list.html'

    fieldsets = (
        (_('Country Information'), {
            'fields': ('country_code', 'country_name', 'is_active')
        }),
        (_('Currency & Language'), {
            'fields': ('default_currency', 'accepted_currencies',
                      'default_language', 'supported_languages')
        }),
        (_('Regional Settings'), {
            'fields': ('timezone', 'date_format', 'uses_metric')
        }),
        (_('Tax & Shipping'), {
            'fields': ('tax_rate', 'is_eu_member', 'requires_vat', 'shipping_zone')
        }),
        (_('Payment Options'), {
            'fields': ('supports_cod', 'blocked_payment_methods')
        }),
        (_('Custom Rules'), {
            'fields': ('custom_rules',),
            'classes': ('collapse',)
        })
    )

    def country_flag_display(self, obj):
        flag = _country_code_to_flag(obj.country_code)
        return format_html('{} {}', flag, obj.country_name)
    country_flag_display.short_description = 'Country'


@admin.register(GeoIPProvider)
class GeoIPProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'provider_type', 'is_active', 'priority',
                    'accuracy_display', 'last_update', 'database_version']
    list_filter = ['is_active', 'provider_type']
    list_editable = ['is_active', 'priority']
    readonly_fields = ['total_lookups', 'successful_lookups', 'failed_lookups',
                      'average_response_ms', 'accuracy_rate', 'created_at', 'updated_at']
    change_list_template = 'admin/geoip/geoipprovider/change_list.html'

    def changelist_view(self, request, extra_context=None):
        """Override changelist view to add provider statistics"""
        extra_context = extra_context or {}

        providers = GeoIPProvider.objects.all().order_by('priority', 'name')
        total_providers = providers.count()
        active_providers = providers.filter(is_active=True).count()
        total_lookups = providers.aggregate(total=Sum('total_lookups'))['total'] or 0

        extra_context.update({
            'providers': providers,
            'total_providers': total_providers,
            'active_providers': active_providers,
            'total_lookups': total_lookups,
            'has_add_permission': self.has_add_permission(request),
        })

        return super().changelist_view(request, extra_context=extra_context)

    fieldsets = (
        (_('Provider Information'), {
            'fields': ('name', 'provider_type', 'is_active', 'priority')
        }),
        (_('Configuration'), {
            'fields': ('config', 'database_path', 'database_url', 'license_key')
        }),
        (_('Database Updates'), {
            'fields': ('last_update', 'next_update', 'database_version')
        }),
        (_('Statistics'), {
            'fields': ('total_lookups', 'successful_lookups', 'failed_lookups',
                      'average_response_ms', 'accuracy_rate')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at')
        })
    )

    def accuracy_display(self, obj):
        rate = obj.accuracy_rate
        if rate >= 95:
            css_class = 'geoip-confidence-high'
        elif rate >= 80:
            css_class = 'geoip-confidence-medium'
        else:
            css_class = 'geoip-confidence-low'
        return format_html(
            '<span class="{}">{}%</span>',
            css_class, f"{rate:.1f}"
        )
    accuracy_display.short_description = 'Accuracy'

    actions = ['update_database', 'test_provider']

    def update_database(self, request, queryset):
        """Admin action to update provider databases"""
        import requests as http_requests

        updated = 0
        errors = []
        for provider in queryset:
            if not provider.database_url:
                errors.append(_('%(name)s has no database URL configured') % {'name': provider.name})
                continue

            try:
                response = http_requests.head(provider.database_url, timeout=10, allow_redirects=True)
                if response.status_code == 200:
                    provider.last_update = timezone.now()
                    provider.save(update_fields=['last_update', 'updated_at'])
                    updated += 1
                else:
                    errors.append(_('%(name)s: HTTP %(status)s from database URL') % {
                        'name': provider.name,
                        'status': response.status_code,
                    })
            except Exception as e:
                errors.append(_('%(name)s: %(error)s') % {'name': provider.name, 'error': str(e)})

        if updated:
            self.message_user(request, _('Database update checked for %(count)d provider(s)') % {'count': updated})
        for error in errors:
            self.message_user(request, error, level='error')
    update_database.short_description = _("Update selected provider databases")

    def test_provider(self, request, queryset):
        """Admin action to test selected providers with a known IP"""
        import time

        test_ip = '8.8.8.8'
        results = []
        for provider in queryset:
            if not provider.is_active:
                results.append(_('%(name)s is inactive — skipped') % {'name': provider.name})
                continue

            start_time = time.time()
            try:
                from .services import resolve_ip
                location = resolve_ip(test_ip, provider_type=provider.provider_type)
                elapsed = (time.time() - start_time) * 1000

                if location:
                    results.append(
                        _('%(name)s: OK (%(ms).0f ms) — %(ip)s → %(country)s') % {
                            'name': provider.name,
                            'ms': elapsed,
                            'ip': test_ip,
                            'country': location.get('country', '?'),
                        }
                    )
                else:
                    results.append(_('%(name)s: No data returned for %(ip)s') % {
                        'name': provider.name, 'ip': test_ip,
                    })
            except ImportError:
                results.append(
                    _('%(name)s: Provider configured (service module not available for direct test)') % {
                        'name': provider.name,
                    }
                )
            except Exception as e:
                results.append(_('%(name)s: Error — %(error)s') % {'name': provider.name, 'error': str(e)})

        for result in results:
            self.message_user(request, result)
    test_provider.short_description = _("Test selected providers")


@admin.register(VisitorLocation)
class VisitorLocationAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'ip_address', 'country_display',
                    'city_display', 'device_type', 'was_corrected_display',
                    'page_views', 'utm_source', 'is_bot', 'last_seen']
    list_filter = ['is_bot', 'is_admin_traffic', 'device_type', 'resolved_country',
                   'utm_source', 'selected_currency', 'selected_language']
    search_fields = ['session_key', 'ip_address', 'resolved_country', 'resolved_city']
    readonly_fields = ['first_seen', 'last_seen']
    date_hierarchy = 'last_seen'
    change_list_template = 'admin/geoip/visitorlocation/change_list.html'

    fieldsets = (
        (_('Session Information'), {
            'fields': ('session_key', 'ip_address', 'page_views', 'device_type',
                       'is_bot', 'is_admin_traffic')
        }),
        (_('Resolved Location'), {
            'fields': ('resolved_country', 'resolved_region', 'resolved_city')
        }),
        (_('User Corrections'), {
            'fields': ('actual_country', 'actual_region', 'actual_city')
        }),
        (_('User Preferences'), {
            'fields': ('selected_currency', 'selected_language')
        }),
        (_('Campaign Attribution'), {
            'fields': ('referrer_url', 'utm_source', 'utm_medium', 'utm_campaign',
                       'utm_term', 'utm_content'),
        }),
        (_('Browser Information'), {
            'fields': ('user_agent', 'accept_language', 'timezone_offset'),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('first_seen', 'last_seen')
        })
    )

    def country_display(self, obj):
        if obj.actual_country:
            return format_html(
                '{} → <strong>{}</strong>',
                obj.resolved_country or '?',
                obj.actual_country
            )
        return obj.resolved_country or '-'
    country_display.short_description = 'Country'

    def city_display(self, obj):
        if obj.actual_city:
            return format_html(
                '{} → <strong>{}</strong>',
                obj.resolved_city or '?',
                obj.actual_city
            )
        return obj.resolved_city or '-'
    city_display.short_description = 'City'

    def was_corrected_display(self, obj):
        # Use annotation if available, otherwise fall back to property
        corrected = getattr(obj, '_was_corrected_annotated', None)
        if corrected is None:
            corrected = obj.was_corrected
        if corrected:
            return format_html('<span class="geoip-corrected-yes">⚠️ Corrected</span>')
        return format_html('<span class="geoip-corrected-no">✓</span>')
    was_corrected_display.short_description = 'Accuracy'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Add annotation for was_corrected (use different name to avoid property conflict)
        return qs.annotate(
            _was_corrected_annotated=Case(
                When(actual_country__isnull=False, then=~Q(actual_country=F('resolved_country'))),
                default=False,
                output_field=BooleanField()
            )
        )

    def changelist_view(self, request, extra_context=None):
        """Override changelist view to add visitor statistics"""
        extra_context = extra_context or {}

        total_visitors = VisitorLocation.objects.count()

        # Corrected count: actual_country is set and differs from resolved_country
        corrected_count = VisitorLocation.objects.filter(
            actual_country__isnull=False
        ).exclude(
            actual_country=''
        ).exclude(
            actual_country=F('resolved_country')
        ).count()

        # Device counts
        desktop_count = VisitorLocation.objects.filter(device_type='desktop').count()
        mobile_count = VisitorLocation.objects.filter(device_type='mobile').count()
        tablet_count = VisitorLocation.objects.filter(device_type='tablet').count()

        extra_context.update({
            'total_visitors': total_visitors,
            'corrected_count': corrected_count,
            'desktop_count': desktop_count,
            'mobile_count': mobile_count,
            'tablet_count': tablet_count,
        })

        return super().changelist_view(request, extra_context=extra_context)


@admin.register(BusinessRule)
class BusinessRuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'priority', 'times_triggered_display', 'last_triggered']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['times_triggered', 'last_triggered', 'created_at', 'updated_at']
    change_list_template = 'admin/geoip/businessrule/change_list.html'

    fieldsets = (
        (_('Rule Information'), {
            'fields': ('name', 'description', 'is_active', 'priority')
        }),
        (_('Conditions'), {
            'fields': ('conditions',),
            'description': _('JSON object defining when this rule should trigger')
        }),
        (_('Actions'), {
            'fields': ('actions',),
            'description': _('JSON object defining what should happen when rule triggers')
        }),
        (_('Statistics'), {
            'fields': ('times_triggered', 'last_triggered'),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def times_triggered_display(self, obj):
        if obj.times_triggered > 1000:
            return format_html(
                '<strong>{}</strong>',
                f"{obj.times_triggered:,}"
            )
        return f"{obj.times_triggered:,}"
    times_triggered_display.short_description = 'Triggered'

    actions = ['test_rule', 'reset_statistics']

    def test_rule(self, request, queryset):
        """Test selected rules against a sample location"""
        from core.utils import get_default_country
        sample_location = {
            'country': get_default_country(),
            'region': '',
            'city': '',
            'is_mobile': False,
        }
        for rule in queryset:
            matched = rule.evaluate(sample_location)
            if matched:
                actions_summary = ', '.join(
                    f'{k}={v}' for k, v in rule.actions.items()
                ) or _('no actions')
                self.message_user(
                    request,
                    _('%(name)s: MATCHED sample (US/California) → %(actions)s') % {
                        'name': rule.name,
                        'actions': actions_summary,
                    }
                )
            else:
                self.message_user(
                    request,
                    _('%(name)s: Did not match sample location (US/California)') % {
                        'name': rule.name,
                    }
                )
    test_rule.short_description = _("Test selected rules")

    def reset_statistics(self, request, queryset):
        """Reset rule statistics"""
        queryset.update(times_triggered=0, last_triggered=None)
        self.message_user(request, f"Reset statistics for {queryset.count()} rules")
    reset_statistics.short_description = _("Reset statistics")

    def changelist_view(self, request, extra_context=None):
        """Override changelist view to add business rule statistics"""
        extra_context = extra_context or {}

        rules = BusinessRule.objects.all().order_by('priority', 'name')
        total_rules = rules.count()
        active_rules = rules.filter(is_active=True).count()

        extra_context.update({
            'rules': rules,
            'total_rules': total_rules,
            'active_rules': active_rules,
            'has_add_permission': self.has_add_permission(request),
        })

        return super().changelist_view(request, extra_context=extra_context)


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ['url_path', 'session_key_short', 'source', 'is_bot',
                    'is_entry_page', 'timestamp']
    list_filter = ['is_bot', 'source', 'is_entry_page']
    search_fields = ['url_path', 'url', 'session_key']
    date_hierarchy = 'timestamp'
    readonly_fields = ['visitor', 'session_key', 'url', 'url_path', 'referrer',
                       'timestamp', 'is_entry_page', 'is_exit_page', 'is_bot', 'source']

    def session_key_short(self, obj):
        return obj.session_key[:12] + '...' if len(obj.session_key) > 12 else obj.session_key
    session_key_short.short_description = 'Session'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(DailyPageStats)
class DailyPageStatsAdmin(admin.ModelAdmin):
    list_display = ['date', 'url_path', 'views', 'unique_visitors', 'bot_views', 'entries']
    list_filter = ['date']
    search_fields = ['url_path']
    date_hierarchy = 'date'
    ordering = ['-date', '-views']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(DailyTrafficStats)
class DailyTrafficStatsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_views', 'unique_visitors', 'bot_views',
                    'new_visitors', 'returning_visitors',
                    'desktop_views', 'mobile_views', 'tablet_views']
    date_hierarchy = 'date'
    ordering = ['-date']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False