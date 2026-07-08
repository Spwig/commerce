from django.contrib import admin
from django.utils.html import format_html

from .models import (
    LicenseProduct, LicenseCheckoutRequest,
    HostedPlan, HostedSubscription, HostedBillingLog, HostedCheckoutRequest,
)


@admin.register(LicenseProduct)
class LicenseProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'product_type', 'price', 'regular_price', 'includes_pos', 'is_active', 'is_featured', 'sort_order']
    list_editable = ['is_active', 'is_featured', 'sort_order']
    list_filter = ['product_type', 'is_active', 'includes_pos']
    search_fields = ['name', 'slug']
    readonly_fields = ['id', 'created_at', 'updated_at']
    fieldsets = (
        (None, {
            'fields': ('id', 'slug', 'name', 'product_type'),
        }),
        ('Pricing', {
            'fields': ('price', 'regular_price', 'savings_amount'),
        }),
        ('Details', {
            'fields': ('features', 'includes_pos', 'trial_days'),
        }),
        ('Display', {
            'fields': ('is_active', 'is_featured', 'note', 'note_link', 'sort_order'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


@admin.register(LicenseCheckoutRequest)
class LicenseCheckoutRequestAdmin(admin.ModelAdmin):
    list_display = ['email', 'license_product', 'status', 'license_key_short', 'created_at']
    list_filter = ['status', 'license_product__product_type']
    search_fields = ['email', 'name', 'license_key']
    readonly_fields = [
        'id', 'license_product', 'email', 'name', 'billing_country',
        'status', 'order', 'payment_intent', 'license_key', 'setup_token',
        'setup_token_id', 'setup_token_expires_at', 'error_message',
        'metadata', 'created_at', 'updated_at',
    ]
    date_hierarchy = 'created_at'

    def license_key_short(self, obj):
        if obj.license_key:
            return f"{obj.license_key[:12]}..."
        return '-'
    license_key_short.short_description = 'License Key'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# ---------------------------------------------------------------------------
# Hosted Subscription Admin
# ---------------------------------------------------------------------------

@admin.register(HostedPlan)
class HostedPlanAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'slug', 'annual_price', 'monthly_price', 'infra_tier',
        'is_active', 'is_featured', 'sort_order',
    ]
    list_editable = ['is_active', 'is_featured', 'sort_order']
    list_filter = ['infra_tier', 'is_active']
    search_fields = ['name', 'slug']
    readonly_fields = ['id', 'created_at', 'updated_at']
    fieldsets = (
        (None, {
            'fields': ('id', 'slug', 'name', 'tagline'),
        }),
        ('Pricing (EUR)', {
            'fields': ('monthly_price', 'annual_price'),
        }),
        ('Infrastructure', {
            'fields': ('infra_tier',),
        }),
        ('Plan Limits', {
            'fields': (
                'max_products', 'max_staff', 'storage_gb', 'emails_monthly',
                'includes_pos', 'includes_api', 'includes_sla',
                'includes_custom_domain',
            ),
        }),
        ('Display', {
            'fields': ('features', 'is_active', 'is_featured', 'sort_order'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


class HostedBillingLogInline(admin.TabularInline):
    model = HostedBillingLog
    extra = 0
    readonly_fields = [
        'cycle_number', 'billing_date', 'amount', 'status',
        'error_message', 'error_code', 'retry_count', 'next_retry_date', 'created_at',
    ]
    fields = readonly_fields
    ordering = ['-created_at']

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HostedSubscription)
class HostedSubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        'store_name', 'email', 'plan_name', 'billing_interval',
        'status_badge', 'region', 'pos_addon', 'next_billing_date', 'created_at',
    ]
    list_filter = ['status', 'billing_interval', 'hosted_plan', 'region']
    search_fields = ['store_name', 'store_slug', 'email', 'license_key']
    readonly_fields = [
        'id', 'created_at', 'updated_at', 'billing_cycle_count',
        'last_billing_date', 'last_billing_status',
    ]
    date_hierarchy = 'created_at'
    inlines = [HostedBillingLogInline]

    fieldsets = (
        (None, {
            'fields': ('id', 'hosted_plan', 'billing_interval', 'status'),
        }),
        ('Customer', {
            'fields': ('email', 'name', 'user'),
        }),
        ('Store', {
            'fields': ('store_name', 'store_slug', 'region', 'license_key'),
        }),
        ('Payment', {
            'fields': (
                'payment_provider_account', 'airwallex_customer_id',
                'airwallex_consent_id',
            ),
        }),
        ('Billing State', {
            'fields': (
                'current_period_start', 'current_period_end',
                'next_billing_date', 'billing_cycle_count',
                'last_billing_date', 'last_billing_status',
            ),
        }),
        ('Grace / Dunning', {
            'fields': ('grace_period_end_date', 'retry_count'),
        }),
        ('Cancellation', {
            'fields': (
                'cancellation_type', 'cancelled_at', 'cancellation_reason',
                'termination_scheduled_at',
            ),
        }),
        ('Add-ons', {
            'fields': ('pos_addon',),
        }),
        ('Metadata', {
            'fields': ('metadata', 'error_message'),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def plan_name(self, obj):
        return obj.hosted_plan.name
    plan_name.short_description = 'Plan'

    def status_badge(self, obj):
        colours = {
            'active': '#28a745',
            'pending': '#6c757d',
            'past_due': '#ffc107',
            'suspended': '#dc3545',
            'cancelled': '#fd7e14',
            'terminated': '#343a40',
        }
        colour = colours.get(obj.status, '#6c757d')
        return format_html(
            '<span style="color:{}; font-weight:600;">{}</span>',
            colour, obj.get_status_display(),
        )
    status_badge.short_description = 'Status'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HostedCheckoutRequest)
class HostedCheckoutRequestAdmin(admin.ModelAdmin):
    list_display = [
        'email', 'hosted_plan', 'store_slug', 'billing_interval',
        'status', 'region', 'created_at',
    ]
    list_filter = ['status', 'hosted_plan', 'billing_interval', 'region']
    search_fields = ['email', 'name', 'store_name', 'store_slug']
    readonly_fields = [
        'id', 'hosted_plan', 'billing_interval', 'email', 'name',
        'billing_country', 'store_name', 'store_slug', 'region', 'pos_addon',
        'payment_intent', 'order', 'subscription', 'status', 'error_message',
        'metadata', 'created_at', 'updated_at',
    ]
    date_hierarchy = 'created_at'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
