"""
Subscription API Serializers
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import (
    SubscriptionPlan,
    PlanPricingTier,
    PaymentToken,
    CustomerSubscription,
    BillingCycleLog
)
from payment_providers.models import PaymentProviderAccount
from .provider_base import is_subscription_supported

User = get_user_model()


class PlanPricingTierSerializer(serializers.ModelSerializer):
    """Serializer for pricing tiers (shows discount applied to product prices)"""

    billing_cycle_display = serializers.CharField(
        source='get_billing_cycle_display',
        read_only=True
    )

    class Meta:
        model = PlanPricingTier
        fields = [
            'tier_id',
            'tier_name',
            'billing_cycle',
            'billing_cycle_display',
            'billing_interval',
            'discount_percentage',  # Discount applied to product price
            'is_default',
            'is_active',
        ]
        read_only_fields = [
            'tier_id',
            'billing_cycle_display',
        ]


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    """Serializer for subscription plan templates"""

    trial_available = serializers.SerializerMethodField()
    pricing_tiers = PlanPricingTierSerializer(many=True, read_only=True)

    class Meta:
        model = SubscriptionPlan
        fields = [
            'plan_id',
            'name',
            'slug',
            'description',
            'pricing_model',
            'pricing_tiers',  # Available pricing tiers with discounts
            'allow_quantity',
            'minimum_quantity',
            'maximum_quantity',
            'trial_period_days',
            'trial_price',
            'trial_price_currency',
            'trial_available',
            'cancellation_policy',
            'minimum_commitment_cycles',
            'max_billing_cycles',
            'is_active',
            'is_public',
            'created_at',
        ]
        read_only_fields = [
            'plan_id',
            'trial_available',
            'pricing_tiers',
            'created_at',
        ]

    def get_trial_available(self, obj):
        """Check if trial is available for this plan"""
        return obj.trial_period_days > 0


class PaymentTokenSerializer(serializers.ModelSerializer):
    """Serializer for payment tokens"""

    payment_method_display = serializers.SerializerMethodField()
    is_expired = serializers.BooleanField(read_only=True)
    provider_account_name = serializers.CharField(source='provider_account.display_name', read_only=True)

    class Meta:
        model = PaymentToken
        fields = [
            'token_id',
            'provider_account',
            'provider_account_name',
            'payment_method_type',
            'payment_method_display',
            'card_brand',
            'card_last4',
            'card_exp_month',
            'card_exp_year',
            'is_default',
            'is_active',
            'is_verified',
            'is_expired',
            'created_at',
        ]
        read_only_fields = [
            'token_id',
            'payment_method_display',
            'is_expired',
            'provider_account_name',
            'created_at',
        ]

    def get_payment_method_display(self, obj):
        """Get display string for payment method"""
        if obj.payment_method_type == 'card':
            brand = obj.card_brand.upper() if obj.card_brand else 'Card'
            return f"{brand} •••• {obj.card_last4}"
        return obj.get_payment_method_type_display()


class BillingCycleLogSerializer(serializers.ModelSerializer):
    """Serializer for billing cycle logs"""

    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )

    can_retry = serializers.BooleanField(read_only=True)

    class Meta:
        model = BillingCycleLog
        fields = [
            'id',
            'cycle_number',
            'billing_date',
            'total_amount',
            'total_amount_currency',
            'status',
            'status_display',
            'retry_count',
            'max_retries',
            'can_retry',
            'next_retry_date',
            'error_message',
            'error_code',
        ]
        read_only_fields = (
            'id',
            'cycle_number',
            'billing_date',
            'total_amount',
            'total_amount_currency',
            'status',
            'retry_count',
            'max_retries',
            'next_retry_date',
            'error_message',
            'error_code',
        )


class CustomerSubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for customer subscriptions"""

    plan = SubscriptionPlanSerializer(read_only=True)
    payment_token = PaymentTokenSerializer(read_only=True)

    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    provider_mode_display = serializers.CharField(
        source='get_provider_mode_display',
        read_only=True
    )
    provider_account_name = serializers.CharField(
        source='payment_provider_account.display_name',
        read_only=True
    )
    days_until_next_billing = serializers.IntegerField(read_only=True)
    total_amount_paid = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    is_active_or_trial = serializers.SerializerMethodField()
    cancel_at_period_end = serializers.SerializerMethodField(
        help_text=_("Whether subscription will cancel at end of current period")
    )
    has_scheduled_plan_change = serializers.BooleanField(read_only=True)
    scheduled_plan_change = serializers.JSONField(read_only=True)
    proration_credit = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    proration_credit_currency = serializers.CharField(read_only=True)
    can_reactivate = serializers.SerializerMethodField()

    # Product information (optional)
    product_name = serializers.CharField(
        source='product.name',
        read_only=True,
        allow_null=True
    )
    variant_name = serializers.CharField(
        source='variant.name',
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = CustomerSubscription
        fields = [
            'subscription_id',
            'plan',
            'product_name',
            'variant_name',
            'payment_provider_account',
            'provider_account_name',
            'payment_token',
            'provider_mode',
            'provider_mode_display',
            'provider_subscription_id',
            'status',
            'status_display',
            'current_period_start',
            'current_period_end',
            'next_billing_date',
            'days_until_next_billing',
            'trial_end_date',
            'billing_cycle_count',
            'last_billing_date',
            'last_billing_status',
            'total_amount_paid',
            'cancel_at_period_end',
            'canceled_at',
            'cancellation_reason',
            'paused_at',
            'pause_reason',
            'auto_resume_date',
            'has_scheduled_plan_change',
            'scheduled_plan_change',
            'proration_credit',
            'proration_credit_currency',
            'reactivation_deadline',
            'can_reactivate',
            'is_active_or_trial',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'subscription_id',
            'provider_subscription_id',
            'status',
            'status_display',
            'provider_mode',
            'provider_mode_display',
            'current_period_start',
            'current_period_end',
            'next_billing_date',
            'days_until_next_billing',
            'trial_end_date',
            'billing_cycle_count',
            'last_billing_date',
            'last_billing_status',
            'total_amount_paid',
            'canceled_at',
            'paused_at',
            'has_scheduled_plan_change',
            'scheduled_plan_change',
            'proration_credit',
            'proration_credit_currency',
            'reactivation_deadline',
            'can_reactivate',
            'is_active_or_trial',
            'provider_account_name',
            'product_name',
            'variant_name',
            'created_at',
            'updated_at',
        ]

    def get_is_active_or_trial(self, obj):
        """Check if subscription is in active or trial status"""
        return obj.status in ('active', 'trial')

    def get_cancel_at_period_end(self, obj):
        """Check if subscription will cancel at end of current period"""
        return obj.cancellation_type == 'end_of_period'

    def get_can_reactivate(self, obj):
        """Check if canceled subscription can be reactivated"""
        return obj.can_reactivate()


class CreateSubscriptionSerializer(serializers.Serializer):
    """Serializer for creating a subscription"""

    plan_id = serializers.UUIDField(required=True)
    pricing_tier_id = serializers.UUIDField(required=True)  # Required - which tier to use
    payment_token_id = serializers.UUIDField(required=True)
    product_id = serializers.IntegerField(required=True)  # Required - pricing comes from product
    variant_id = serializers.IntegerField(required=False, allow_null=True)
    quantity = serializers.IntegerField(required=False, default=1, min_value=1)
    trial_override_days = serializers.IntegerField(required=False, allow_null=True, min_value=0)

    def validate_plan_id(self, value):
        """Validate plan exists and is active"""
        try:
            plan = SubscriptionPlan.objects.get(plan_id=value)
        except SubscriptionPlan.DoesNotExist:
            raise serializers.ValidationError("Subscription plan not found")

        if not plan.is_active:
            raise serializers.ValidationError("This subscription plan is not active")

        if not plan.is_public:
            raise serializers.ValidationError("This subscription plan is not available")

        return value

    def validate_pricing_tier_id(self, value):
        """Validate pricing tier exists and is active"""
        try:
            tier = PlanPricingTier.objects.get(tier_id=value)
        except PlanPricingTier.DoesNotExist:
            raise serializers.ValidationError("Pricing tier not found")

        if not tier.is_active:
            raise serializers.ValidationError("This pricing tier is not active")

        return value

    def validate_payment_token_id(self, value):
        """Validate payment token exists and is active"""
        user = self.context['request'].user

        try:
            token = PaymentToken.objects.get(token_id=value, user=user)
        except PaymentToken.DoesNotExist:
            raise serializers.ValidationError("Payment token not found")

        if not token.is_active:
            raise serializers.ValidationError("Payment token is not active")

        if token.is_expired():
            raise serializers.ValidationError("Payment token has expired")

        return value

    def validate(self, data):
        """Cross-field validation"""
        # Validate pricing tier belongs to plan
        try:
            plan = SubscriptionPlan.objects.get(plan_id=data['plan_id'])
            tier = PlanPricingTier.objects.get(tier_id=data['pricing_tier_id'])

            if tier.plan != plan:
                raise serializers.ValidationError({
                    'pricing_tier_id': "Pricing tier does not belong to the specified plan"
                })
        except (SubscriptionPlan.DoesNotExist, PlanPricingTier.DoesNotExist):
            pass  # Already validated in field validators

        # Validate product exists and is active
        from catalog.models import Product
        try:
            product = Product.objects.get(id=data['product_id'])

            if not product.is_active:
                raise serializers.ValidationError({
                    'product_id': "Product is not active"
                })

            # If variant specified, ensure it belongs to the product
            if data.get('variant_id'):
                from catalog.models import ProductVariant
                try:
                    variant = ProductVariant.objects.get(
                        id=data['variant_id'],
                        product=product
                    )
                    if not variant.is_active:
                        raise serializers.ValidationError({
                            'variant_id': "Product variant is not active"
                        })
                except ProductVariant.DoesNotExist:
                    raise serializers.ValidationError({
                        'variant_id': "Variant does not belong to the specified product"
                    })

        except Product.DoesNotExist:
            raise serializers.ValidationError({
                'product_id': "Product not found"
            })

        return data


class CancelSubscriptionSerializer(serializers.Serializer):
    """Serializer for canceling a subscription"""

    immediately = serializers.BooleanField(default=False)
    reason = serializers.CharField(required=False, allow_blank=True, max_length=500)


class PauseSubscriptionSerializer(serializers.Serializer):
    """Serializer for pausing a subscription"""

    reason = serializers.CharField(required=False, allow_blank=True, max_length=500)
    auto_resume_date = serializers.DateTimeField(required=False, allow_null=True)


class UpdatePaymentMethodSerializer(serializers.Serializer):
    """Serializer for updating subscription payment method"""

    payment_token_id = serializers.UUIDField(required=True)

    def validate_payment_token_id(self, value):
        """Validate payment token exists and is active"""
        user = self.context['request'].user

        try:
            token = PaymentToken.objects.get(token_id=value, user=user)
        except PaymentToken.DoesNotExist:
            raise serializers.ValidationError("Payment token not found")

        if not token.is_active:
            raise serializers.ValidationError("Payment token is not active")

        if token.is_expired():
            raise serializers.ValidationError("Payment token has expired")

        return value


class ChangePlanSerializer(serializers.Serializer):
    """Serializer for changing a subscription plan"""

    new_plan_id = serializers.UUIDField(required=True)
    new_tier_id = serializers.UUIDField(required=True)
    mode = serializers.ChoiceField(
        choices=['auto', 'immediate', 'at_renewal'],
        default='auto',
        required=False,
        help_text=_("'auto' uses plan-configured behavior, 'immediate' forces immediate change, 'at_renewal' defers to next billing cycle")
    )

    def validate_new_plan_id(self, value):
        """Validate new plan exists and is active"""
        try:
            plan = SubscriptionPlan.objects.get(plan_id=value)
        except SubscriptionPlan.DoesNotExist:
            raise serializers.ValidationError("Subscription plan not found")

        if not plan.is_active:
            raise serializers.ValidationError("This subscription plan is not active")

        return value

    def validate_new_tier_id(self, value):
        """Validate new pricing tier exists and is active"""
        try:
            tier = PlanPricingTier.objects.get(tier_id=value)
        except PlanPricingTier.DoesNotExist:
            raise serializers.ValidationError("Pricing tier not found")

        if not tier.is_active:
            raise serializers.ValidationError("This pricing tier is not active")

        return value

    def validate(self, data):
        """Cross-field validation: tier must belong to plan"""
        try:
            plan = SubscriptionPlan.objects.get(plan_id=data['new_plan_id'])
            tier = PlanPricingTier.objects.get(tier_id=data['new_tier_id'])

            if tier.plan != plan:
                raise serializers.ValidationError({
                    'new_tier_id': "Pricing tier does not belong to the specified plan"
                })
        except (SubscriptionPlan.DoesNotExist, PlanPricingTier.DoesNotExist):
            pass  # Already validated in field validators

        return data


class CancelScheduledChangeSerializer(serializers.Serializer):
    """Serializer for canceling a scheduled plan change (empty body, POST only)"""
    pass


class ReactivateSubscriptionSerializer(serializers.Serializer):
    """Serializer for reactivating a canceled subscription"""

    payment_token_id = serializers.UUIDField(
        required=False,
        allow_null=True,
        help_text=_("Optional new payment token. Uses existing token if not provided.")
    )

    def validate_payment_token_id(self, value):
        """Validate payment token exists and is active"""
        if value is None:
            return value

        user = self.context['request'].user

        try:
            token = PaymentToken.objects.get(token_id=value, user=user)
        except PaymentToken.DoesNotExist:
            raise serializers.ValidationError("Payment token not found")

        if not token.is_active:
            raise serializers.ValidationError("Payment token is not active")

        if token.is_expired():
            raise serializers.ValidationError("Payment token has expired")

        return value


class CreatePaymentTokenSerializer(serializers.Serializer):
    """Serializer for creating a payment token"""

    provider_account_id = serializers.UUIDField(required=True)
    payment_method_data = serializers.JSONField(required=True)
    set_as_default = serializers.BooleanField(default=True)

    def validate_provider_account_id(self, value):
        """Validate provider account exists and supports subscriptions"""
        try:
            provider_account = PaymentProviderAccount.objects.get(id=value, is_active=True)
        except PaymentProviderAccount.DoesNotExist:
            raise serializers.ValidationError("Payment provider account not found or not active")

        if not is_subscription_supported(provider_account):
            raise serializers.ValidationError(
                "This payment provider does not support subscriptions"
            )

        return value
