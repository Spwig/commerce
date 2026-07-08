"""
HQ-only serializers for the Spwig merchant account portal API.

These serializers are used exclusively on spwig.com (SPWIG_IS_HQ=True)
to expose hosted subscription, billing, and license data to the
Next.js account frontend.
"""
from rest_framework import serializers

from license_checkout.models import (
    HostedBillingLog,
    HostedPlan,
    HostedSubscription,
)


class HostedPlanSerializer(serializers.ModelSerializer):
    monthly_price = serializers.DecimalField(
        source='monthly_price.amount', max_digits=10, decimal_places=2,
    )
    annual_price = serializers.DecimalField(
        source='annual_price.amount', max_digits=10, decimal_places=2,
    )
    annual_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    has_intro_offer = serializers.BooleanField(read_only=True)
    intro_monthly_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True,
    )
    intro_annual_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True,
    )

    class Meta:
        model = HostedPlan
        fields = [
            'slug', 'name', 'tagline',
            'monthly_price', 'annual_price', 'annual_total',
            'infra_tier',
            'max_products', 'max_staff', 'storage_gb', 'emails_monthly',
            'includes_pos', 'includes_api', 'includes_sla', 'includes_custom_domain',
            'features',
            'has_intro_offer', 'intro_monthly_price', 'intro_annual_price',
            'intro_monthly_discount_percent', 'intro_monthly_discount_cycles',
            'intro_annual_discount_percent', 'intro_annual_discount_cycles',
        ]


class HostedSubscriptionSerializer(serializers.ModelSerializer):
    plan = HostedPlanSerializer(source='hosted_plan', read_only=True)
    billing_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True,
    )
    is_in_intro_period = serializers.BooleanField(read_only=True)
    store_url = serializers.SerializerMethodField()
    admin_url = serializers.SerializerMethodField()
    actions = serializers.SerializerMethodField()

    class Meta:
        model = HostedSubscription
        fields = [
            'id', 'status', 'billing_interval',
            'plan', 'billing_amount', 'is_in_intro_period',
            'store_name', 'store_slug', 'region',
            'store_url', 'admin_url',
            'pos_addon',
            'current_period_start', 'current_period_end',
            'next_billing_date', 'billing_cycle_count',
            'cancellation_type', 'cancelled_at', 'cancellation_reason',
            'termination_scheduled_at',
            'created_at',
            'actions',
        ]

    def get_store_url(self, obj):
        if obj.store_slug:
            return f'https://{obj.store_slug}.myspwig.com'
        return ''

    def get_admin_url(self, obj):
        if obj.store_slug:
            return f'https://{obj.store_slug}.myspwig.com/en/admin/'
        return ''

    def get_actions(self, obj):
        from django.utils import timezone
        now = timezone.now()

        can_cancel = obj.status in (
            HostedSubscription.Status.ACTIVE,
            HostedSubscription.Status.PAST_DUE,
            HostedSubscription.Status.SUSPENDED,
            HostedSubscription.Status.PENDING,
        )
        can_undo_cancel = (
            obj.status == HostedSubscription.Status.CANCELLED
            and obj.current_period_end
            and obj.current_period_end > now
        )
        can_reactivate = (
            obj.status in (
                HostedSubscription.Status.SUSPENDED,
                HostedSubscription.Status.CANCELLED,
            )
            and not can_undo_cancel
        )
        can_change_interval = obj.status == HostedSubscription.Status.ACTIVE
        can_update_payment = obj.status in (
            HostedSubscription.Status.ACTIVE,
            HostedSubscription.Status.PAST_DUE,
            HostedSubscription.Status.SUSPENDED,
            HostedSubscription.Status.PENDING,
        )

        return {
            'can_cancel': can_cancel,
            'can_undo_cancel': can_undo_cancel,
            'can_reactivate': can_reactivate,
            'can_change_interval': can_change_interval,
            'can_update_payment': can_update_payment,
        }


class HostedSubscriptionListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for subscription lists."""
    plan_name = serializers.CharField(source='hosted_plan.name')
    plan_slug = serializers.CharField(source='hosted_plan.slug')
    billing_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True,
    )
    store_url = serializers.SerializerMethodField()

    class Meta:
        model = HostedSubscription
        fields = [
            'id', 'status', 'billing_interval',
            'plan_name', 'plan_slug', 'billing_amount',
            'store_name', 'store_slug', 'store_url',
            'next_billing_date', 'created_at',
        ]

    def get_store_url(self, obj):
        if obj.store_slug:
            return f'https://{obj.store_slug}.myspwig.com'
        return ''


class HostedBillingLogSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(
        source='amount.amount', max_digits=10, decimal_places=2,
    )

    class Meta:
        model = HostedBillingLog
        fields = [
            'id', 'cycle_number', 'billing_date', 'amount',
            'status', 'error_message', 'retry_count', 'created_at',
        ]


class PaymentConfigSerializer(serializers.Serializer):
    client_secret = serializers.CharField()
    intent_id = serializers.CharField()
    provider_slug = serializers.CharField()
    env = serializers.CharField()


class IntervalChangeDetailSerializer(serializers.Serializer):
    current_interval = serializers.CharField()
    new_interval = serializers.CharField()
    current_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    new_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    charge_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    credit = serializers.DecimalField(max_digits=10, decimal_places=2)
    savings = serializers.DecimalField(max_digits=10, decimal_places=2)
    next_billing_date = serializers.DateTimeField(allow_null=True)


class LicenseDetailSerializer(serializers.Serializer):
    license_key = serializers.CharField()
    license_type = serializers.CharField()
    product_type = serializers.CharField(default='')
    owner_name = serializers.CharField(default='')
    company = serializers.CharField(default='')
    is_active = serializers.BooleanField()
    expires_at = serializers.CharField(allow_null=True, default=None)
    installations_count = serializers.IntegerField(default=0)
    max_installations = serializers.IntegerField(default=1)


class LicenseListItemSerializer(serializers.Serializer):
    """License item with source info (self-hosted or hosted)."""
    license_key = serializers.CharField()
    license_type = serializers.CharField()
    product_type = serializers.CharField(default='')
    owner_name = serializers.CharField(default='')
    company = serializers.CharField(default='')
    is_active = serializers.BooleanField()
    expires_at = serializers.CharField(allow_null=True, default=None)
    installations_count = serializers.IntegerField(default=0)
    max_installations = serializers.IntegerField(default=1)
    source = serializers.CharField()  # 'self_hosted' or 'hosted'
    subscription_id = serializers.CharField(allow_null=True, default=None)
    store_name = serializers.CharField(default='', allow_blank=True)


class MaintenanceStatusSerializer(serializers.Serializer):
    active = serializers.BooleanField()
    expires_at = serializers.CharField(allow_null=True, default=None)
    days_remaining = serializers.IntegerField(default=0)
    grace_period = serializers.BooleanField(default=False)
    reinstatement_tier = serializers.CharField(default='', allow_blank=True)


class DashboardSerializer(serializers.Serializer):
    account_type = serializers.CharField()
    user = serializers.SerializerMethodField()
    # Backward compat — singular (first item)
    hosted_subscription = HostedSubscriptionSerializer(allow_null=True)
    license_summary = LicenseDetailSerializer(allow_null=True)
    # Plural fields
    hosted_subscriptions = HostedSubscriptionListSerializer(many=True, default=[])
    licenses = LicenseListItemSerializer(many=True, default=[])
    subscription_count = serializers.IntegerField(default=0)
    license_count = serializers.IntegerField(default=0)

    def get_user(self, obj):
        user = obj.get('_user')
        if not user:
            return None
        return {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }


class CancelSubscriptionSerializer(serializers.Serializer):
    reason = serializers.CharField(required=False, default='', max_length=500)


class ChangeIntervalSerializer(serializers.Serializer):
    """Validates the POST body for interval change (empty body is fine)."""
    pass


class UpdatePaymentSerializer(serializers.Serializer):
    payment_intent_id = serializers.CharField(required=True)


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError({'new_password_confirm': 'Passwords do not match.'})
        return data


class GhostActivationSerializer(serializers.Serializer):
    uidb64 = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    password = serializers.CharField(required=True, min_length=8)
    password_confirm = serializers.CharField(required=True)

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'password_confirm': 'Passwords do not match.'})
        return data
