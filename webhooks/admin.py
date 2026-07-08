"""
Admin configuration for webhook management.

Provides a user-friendly interface for merchants to manage webhook
endpoints and view delivery logs.
"""
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponseRedirect
from datetime import timedelta

from .models import WebhookEndpoint, WebhookDelivery


@admin.register(WebhookEndpoint)
class WebhookEndpointAdmin(admin.ModelAdmin):
    """Admin interface for webhook endpoints."""

    change_list_template = 'admin/webhooks/webhookendpoint/change_list.html'
    change_form_template = 'admin/webhooks/webhookendpoint/change_form.html'

    def add_view(self, request, form_url='', extra_context=None):
        """Redirect to wizard instead of default add form."""
        return HttpResponseRedirect(reverse('webhooks:endpoint_wizard'))

    list_display = [
        'name',
        'url_display',
        'is_active_display',
        'events_display',
        'health_status',
        'last_triggered_display',
        'created_at',
    ]
    list_filter = ['is_active', 'is_disabled_by_failures', 'created_at']
    search_fields = ['name', 'url', 'description']
    readonly_fields = [
        'id',
        'secret_display',
        'created_at',
        'updated_at',
        'last_triggered_at',
        'consecutive_failures',
        'is_disabled_by_failures',
        'delivery_stats',
    ]
    fieldsets = (
        (_('Basic'), {
            'fields': ('name', 'url', 'description', 'is_active'),
            'classes': ('tab-basic',),
        }),
        (_('Event Subscriptions'), {
            'fields': ('events',),
            'classes': ('tab-events',),
            'description': _('Select the events this endpoint should receive. '
                           'Use ["*"] to receive all events.')
        }),
        (_('Configuration'), {
            'fields': ('max_retries', 'timeout_seconds'),
            'classes': ('tab-config',),
        }),
        (_('Security'), {
            'fields': ('id', 'secret_display'),
            'classes': ('tab-security',),
            'description': _('The secret is used to sign webhook payloads. '
                           'Use the API to rotate the secret if needed.')
        }),
        (_('Health & Status'), {
            'fields': (
                'delivery_stats',
                'consecutive_failures',
                'is_disabled_by_failures',
                'last_triggered_at',
            ),
            'classes': ('tab-health',),
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('tab-timestamps',),
        }),
    )

    class Media:
        css = {
            'all': ('webhooks/admin/css/webhookendpoint_form.css',)
        }
        js = ('webhooks/admin/js/webhookendpoint_form.js',)

    def url_display(self, obj):
        """Display truncated URL."""
        url = obj.url
        if len(url) > 50:
            return format_html(
                '<span title="{}">{}&hellip;</span>',
                url, url[:50]
            )
        return url
    url_display.short_description = _('URL')
    url_display.admin_order_field = 'url'

    def is_active_display(self, obj):
        """Display active status with icon."""
        if obj.is_disabled_by_failures:
            return format_html(
                '<span style="color: #dc3545;" title="{}">&#x26A0; {}</span>',
                _('Disabled due to consecutive failures'),
                _('Disabled')
            )
        if obj.is_active:
            return format_html(
                '<span style="color: #28a745;">&#x2714; {}</span>',
                _('Active')
            )
        return format_html(
            '<span style="color: #6c757d;">&#x2716; {}</span>',
            _('Inactive')
        )
    is_active_display.short_description = _('Status')
    is_active_display.admin_order_field = 'is_active'

    def events_display(self, obj):
        """Display subscribed events count."""
        count = len(obj.events) if obj.events else 0
        if count == 0:
            return format_html('<span style="color: #dc3545;">{}</span>', _('None'))
        if '*' in obj.events:
            return format_html('<span style="color: #17a2b8;">{}</span>', _('All events'))
        return format_html('{} {}', count, _('events'))
    events_display.short_description = _('Subscribed Events')

    def health_status(self, obj):
        """Display endpoint health status."""
        if obj.is_disabled_by_failures:
            return format_html(
                '<span style="color: #dc3545;">&#x2716; {} ({})</span>',
                _('Unhealthy'),
                obj.consecutive_failures
            )
        if obj.consecutive_failures > 0:
            return format_html(
                '<span style="color: #ffc107;">&#x26A0; {} ({})</span>',
                _('Degraded'),
                obj.consecutive_failures
            )
        return format_html(
            '<span style="color: #28a745;">&#x2714; {}</span>',
            _('Healthy')
        )
    health_status.short_description = _('Health')

    def last_triggered_display(self, obj):
        """Display when the endpoint was last triggered."""
        if not obj.last_triggered_at:
            return format_html('<span style="color: #6c757d;">{}</span>', _('Never'))
        delta = timezone.now() - obj.last_triggered_at
        if delta < timedelta(hours=1):
            return format_html('<span style="color: #28a745;">{}</span>',
                             _('Recently'))
        if delta < timedelta(days=1):
            return format_html('{} {} {}', delta.seconds // 3600, _('hours'), _('ago'))
        return format_html('{} {} {}', delta.days, _('days'), _('ago'))
    last_triggered_display.short_description = _('Last Triggered')
    last_triggered_display.admin_order_field = 'last_triggered_at'

    def secret_display(self, obj):
        """Display masked secret."""
        if obj.secret:
            return format_html(
                '<code>{}...{}</code> '
                '<span style="color: #6c757d; font-size: 0.9em;">({})</span>',
                obj.secret[:8],
                obj.secret[-4:],
                _('Use API to view or rotate')
            )
        return '-'
    secret_display.short_description = _('Secret')

    def delivery_stats(self, obj):
        """Display delivery statistics for last 24 hours."""
        from .services import get_endpoint_stats
        stats = get_endpoint_stats(str(obj.id))
        if not stats:
            return '-'

        return format_html(
            '<div style="line-height: 1.8;">'
            '<strong>{}:</strong> {} | '
            '<span style="color: #28a745;">{}: {}</span> | '
            '<span style="color: #dc3545;">{}: {}</span> | '
            '<span style="color: #ffc107;">{}: {}</span><br>'
            '<strong>{}</strong>: {}% | '
            '<strong>{}</strong>: {}ms'
            '</div>',
            _('Total'), stats.get('total_deliveries', 0),
            _('Success'), stats.get('successful', 0),
            _('Failed'), stats.get('failed', 0),
            _('Retrying'), stats.get('retrying', 0),
            _('Success Rate'), stats.get('success_rate', 0),
            _('Avg Response'), int(stats.get('avg_response_time_ms', 0)),
        )
    delivery_stats.short_description = _('Delivery Stats (24h)')

    actions = ['enable_endpoints', 'disable_endpoints', 'reset_failures_action']

    @admin.action(description=_('Enable selected endpoints'))
    def enable_endpoints(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, _('%d endpoint(s) enabled.') % updated)

    @admin.action(description=_('Disable selected endpoints'))
    def disable_endpoints(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, _('%d endpoint(s) disabled.') % updated)

    @admin.action(description=_('Reset failure count'))
    def reset_failures_action(self, request, queryset):
        for endpoint in queryset:
            endpoint.reset_failures()
        self.message_user(request, _('%d endpoint(s) reset.') % queryset.count())

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Add extra context for the change form template."""
        extra_context = extra_context or {}
        return super().change_view(request, object_id, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):
        """Add dashboard stats to the context."""
        extra_context = extra_context or {}

        # Get counts for dashboard
        total = WebhookEndpoint.objects.count()
        active = WebhookEndpoint.objects.filter(
            is_active=True,
            is_disabled_by_failures=False
        ).count()
        unhealthy = WebhookEndpoint.objects.filter(
            is_disabled_by_failures=True
        ).count()

        # Get delivery count for last 24 hours
        from django.utils import timezone
        from datetime import timedelta
        last_24h = timezone.now() - timedelta(hours=24)
        deliveries_24h = WebhookDelivery.objects.filter(
            created_at__gte=last_24h
        ).count()

        extra_context['total_endpoints'] = total
        extra_context['active_endpoints'] = active
        extra_context['unhealthy_endpoints'] = unhealthy
        extra_context['deliveries_24h'] = deliveries_24h

        return super().changelist_view(request, extra_context=extra_context)


@admin.register(WebhookDelivery)
class WebhookDeliveryAdmin(admin.ModelAdmin):
    """Admin interface for webhook delivery logs."""

    list_display = [
        'id_short',
        'endpoint_link',
        'event_type',
        'status_display',
        'response_code_display',
        'response_time_display',
        'attempt_count',
        'created_at',
    ]
    list_filter = ['status', 'event_type', 'endpoint', 'created_at']
    search_fields = ['id', 'event_type', 'endpoint__name', 'payload']
    readonly_fields = [
        'id',
        'endpoint',
        'event_type',
        'payload_display',
        'status',
        'response_status_code',
        'response_body_display',
        'response_headers',
        'response_time_ms',
        'error_message',
        'attempt_count',
        'next_retry_at',
        'created_at',
        'delivered_at',
    ]
    fieldsets = (
        (None, {
            'fields': ('id', 'endpoint', 'event_type', 'status')
        }),
        (_('Payload'), {
            'fields': ('payload_display',),
        }),
        (_('Response'), {
            'fields': (
                'response_status_code',
                'response_time_ms',
                'response_body_display',
                'response_headers',
            ),
            'classes': ('collapse',),
        }),
        (_('Error Details'), {
            'fields': ('error_message',),
            'classes': ('collapse',),
        }),
        (_('Retry Information'), {
            'fields': ('attempt_count', 'next_retry_at'),
            'classes': ('collapse',),
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'delivered_at'),
            'classes': ('collapse',),
        }),
    )

    def has_add_permission(self, request):
        """Deliveries are created automatically, not manually."""
        return False

    def has_change_permission(self, request, obj=None):
        """Deliveries should not be edited."""
        return False

    def id_short(self, obj):
        """Display shortened UUID."""
        return str(obj.id)[:8] + '...'
    id_short.short_description = _('ID')
    id_short.admin_order_field = 'id'

    def endpoint_link(self, obj):
        """Link to the endpoint."""
        url = reverse('admin:webhooks_webhookendpoint_change', args=[obj.endpoint.id])
        return format_html('<a href="{}">{}</a>', url, obj.endpoint.name)
    endpoint_link.short_description = _('Endpoint')
    endpoint_link.admin_order_field = 'endpoint__name'

    def status_display(self, obj):
        """Display status with color coding."""
        colors = {
            'pending': '#6c757d',
            'success': '#28a745',
            'failed': '#dc3545',
            'retrying': '#ffc107',
        }
        icons = {
            'pending': '&#x23F3;',  # Hourglass
            'success': '&#x2714;',  # Check
            'failed': '&#x2716;',   # X
            'retrying': '&#x21BB;', # Retry arrow
        }
        color = colors.get(obj.status, '#6c757d')
        icon = icons.get(obj.status, '')
        return format_html(
            '<span style="color: {};">{} {}</span>',
            color, icon, obj.get_status_display()
        )
    status_display.short_description = _('Status')
    status_display.admin_order_field = 'status'

    def response_code_display(self, obj):
        """Display response code with color coding."""
        if not obj.response_status_code:
            return '-'
        code = obj.response_status_code
        if 200 <= code < 300:
            color = '#28a745'
        elif 400 <= code < 500:
            color = '#ffc107'
        else:
            color = '#dc3545'
        return format_html('<span style="color: {};">{}</span>', color, code)
    response_code_display.short_description = _('Response')
    response_code_display.admin_order_field = 'response_status_code'

    def response_time_display(self, obj):
        """Display response time with color coding."""
        if not obj.response_time_ms:
            return '-'
        ms = obj.response_time_ms
        if ms < 500:
            color = '#28a745'
        elif ms < 2000:
            color = '#ffc107'
        else:
            color = '#dc3545'
        return format_html('<span style="color: {};">{}ms</span>', color, ms)
    response_time_display.short_description = _('Time')
    response_time_display.admin_order_field = 'response_time_ms'

    def payload_display(self, obj):
        """Display formatted payload JSON."""
        import json
        try:
            formatted = json.dumps(obj.payload, indent=2, default=str)
            return format_html('<pre style="max-height: 400px; overflow: auto;">{}</pre>', formatted)
        except Exception:
            return str(obj.payload)
    payload_display.short_description = _('Payload')

    def response_body_display(self, obj):
        """Display response body (truncated)."""
        if not obj.response_body:
            return '-'
        body = obj.response_body
        if len(body) > 1000:
            body = body[:1000] + '...'
        return format_html('<pre style="max-height: 200px; overflow: auto;">{}</pre>', body)
    response_body_display.short_description = _('Response Body')

    actions = ['retry_deliveries']

    @admin.action(description=_('Retry selected deliveries'))
    def retry_deliveries(self, request, queryset):
        from .tasks import deliver_webhook
        count = 0
        for delivery in queryset.exclude(status=WebhookDelivery.Status.SUCCESS):
            deliver_webhook.delay(str(delivery.id))
            count += 1
        self.message_user(request, _('%d delivery(ies) queued for retry.') % count)
