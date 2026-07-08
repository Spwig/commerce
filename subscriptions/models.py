"""
Subscription models for recurring billing support - Modern Design

This module provides a comprehensive subscription management system with:
1. Tiered pricing (monthly/quarterly/annual with discounts)
2. Quantity-based subscriptions (per-seat pricing)
3. Modular add-ons
4. Promotional discounts and coupons
5. Flexible cancellation policies
6. Plan changes with proration
7. Support for both native (Stripe, PayPal) and fallback providers
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from djmoney.models.fields import MoneyField
from decimal import Decimal
import uuid
from datetime import timedelta

User = get_user_model()


class SubscriptionPlan(models.Model):
    """
    Defines a subscription plan with multiple pricing tiers and optional add-ons.

    Example: "Premium Plan" can have:
    - Monthly tier: $50/mo
    - Annual tier: $40/mo (20% discount, billed $480/year)
    - Quarterly tier: $45/mo (10% discount, billed $135/quarter)
    """

    # Pricing Model Choices
    PRICING_MODEL_CHOICES = [
        ('tiered', _('Tiered Pricing')),  # Multiple commitment options with discounts
        ('quantity_based', _('Quantity-Based')),  # Per-seat/per-user pricing
        ('flat', _('Flat Rate')),  # Single price, no variations
    ]

    # Cancellation Policy Choices
    CANCELLATION_POLICY_CHOICES = [
        ('anytime', _('Cancel Anytime')),  # Immediate cancellation
        ('end_of_period', _('Cancel at Period End')),  # Finish paid period
        ('minimum_commitment', _('Minimum Commitment Required')),  # Enforce commitment period
    ]

    # Identity
    plan_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        verbose_name=_("Plan ID"),
        help_text=_("Unique identifier for this plan")
    )

    # Basic Information
    name = models.CharField(
        max_length=200,
        verbose_name=_("Plan Name"),
        help_text=_("Name displayed to customers (e.g., 'Premium Plan', 'Enterprise Plan')")
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name=_("Slug"),
        help_text=_("URL-friendly version of the name")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description"),
        help_text=_("Detailed description of what this plan includes")
    )

    # Translations (for merchant multi-language support)
    translations = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Translations"),
        help_text=_("Multilingual content for customer-facing fields (name, description)")
    )

    # Pricing Model
    pricing_model = models.CharField(
        max_length=20,
        choices=PRICING_MODEL_CHOICES,
        default='tiered',
        verbose_name=_("Pricing Model"),
        help_text=_("How pricing is structured for this plan")
    )

    # Quantity-Based Pricing Settings
    allow_quantity = models.BooleanField(
        default=False,
        verbose_name=_("Allow Quantity"),
        help_text=_("Enable per-seat/per-user pricing (price × quantity)")
    )
    minimum_quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name=_("Minimum Quantity"),
        help_text=_("Minimum number of units required (for quantity-based pricing)")
    )
    maximum_quantity = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Maximum Quantity"),
        help_text=_("Maximum number of units allowed (leave empty for unlimited)")
    )

    # Setup Fee (one-time charge at subscription start)
    setup_fee = MoneyField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        default_currency='USD',
        verbose_name=_("Setup Fee"),
        help_text=_("One-time fee charged at subscription start (0.00 for no fee)")
    )

    # Trial Period
    trial_period_days = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(365)],
        verbose_name=_("Trial Period (Days)"),
        help_text=_("Number of free trial days before first charge (0 for no trial)")
    )
    trial_price = MoneyField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        default_currency='USD',
        verbose_name=_("Trial Price"),
        help_text=_("Optional reduced price during trial period (leave empty for free trial)")
    )

    # Limits
    max_billing_cycles = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Maximum Billing Cycles"),
        help_text=_("Total number of billing cycles before subscription ends (leave empty for unlimited)")
    )

    # Cancellation Policy
    cancellation_policy = models.CharField(
        max_length=25,
        choices=CANCELLATION_POLICY_CHOICES,
        default='end_of_period',
        verbose_name=_("Cancellation Policy"),
        help_text=_("Policy for handling subscription cancellations")
    )
    minimum_commitment_cycles = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Minimum Commitment (Cycles)"),
        help_text=_("Minimum billing cycles required before cancellation allowed (0 for no minimum)")
    )

    # Grace Periods
    grace_period_days = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(90)],
        verbose_name=_("Grace Period (Days)"),
        help_text=_("Days to keep access active after payment failure (0 for immediate suspension)")
    )
    reactivation_period_days = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(90)],
        verbose_name=_("Reactivation Period (Days)"),
        help_text=_("Days after cancellation during which customer can reactivate (0 to disable)")
    )

    # Plan Change Behavior
    PLAN_CHANGE_BEHAVIOR_CHOICES = [
        ('immediate', _('Immediate')),
        ('at_renewal', _('At Renewal')),
    ]
    upgrade_behavior = models.CharField(
        max_length=20,
        choices=PLAN_CHANGE_BEHAVIOR_CHOICES,
        default='immediate',
        verbose_name=_("Upgrade Behavior"),
        help_text=_("Upgrades to this plan: 'Immediate' with proration, 'At Renewal' deferred")
    )
    downgrade_behavior = models.CharField(
        max_length=20,
        choices=PLAN_CHANGE_BEHAVIOR_CHOICES,
        default='at_renewal',
        verbose_name=_("Downgrade Behavior"),
        help_text=_("Downgrades from this plan: 'Immediate' with credit, 'At Renewal' deferred")
    )

    # Status
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
        help_text=_("Whether this plan can be purchased by customers")
    )
    is_public = models.BooleanField(
        default=True,
        verbose_name=_("Public"),
        help_text=_("Show this plan on product pages and subscription lists")
    )

    # Provider Integration
    provider_plan_mappings = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Provider Plan IDs"),
        help_text=_("Mapping of payment provider names to their plan IDs (e.g., {'stripe': 'price_xxx', 'paypal': 'P-xxx'})")
    )

    # Metadata
    metadata = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Metadata"),
        help_text=_("Additional data for custom integrations")
    )

    # Ordering
    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Sort Order"),
        help_text=_("Display order (lower numbers appear first)")
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Subscription Plan")
        verbose_name_plural = _("Subscription Plans")
        ordering = ['sort_order', 'name']
        indexes = [
            models.Index(fields=['is_active', 'is_public']),
            models.Index(fields=['pricing_model']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.name

    def get_default_tier(self):
        """Get the default pricing tier for this plan"""
        return self.pricing_tiers.filter(is_default=True).first() or self.pricing_tiers.first()

    def get_provider_plan_id(self, provider_key):
        """Get plan ID for specific payment provider"""
        return self.provider_plan_mappings.get(provider_key)

    def get_active_subscriptions_count(self):
        """Return count of active and trial subscriptions"""
        return self.subscriptions.filter(status__in=['active', 'trial']).count()


class PlanPricingTier(models.Model):
    """
    Defines a pricing tier for a subscription plan template.

    Pricing tiers define billing frequency and discount percentages. The actual price
    is derived from the product price when a customer subscribes.

    Example tiers for "Essential Oil Subscription" template:
    - Monthly: 0% discount (full product price)
    - Quarterly: 10% discount off product price
    - Annual: 20% discount off product price

    When applied to products:
    - Lavender Oil ($15): Monthly $15, Quarterly $13.50, Annual $12
    - Rose Oil ($50): Monthly $50, Quarterly $45, Annual $40
    """

    # Billing Cycle Choices
    BILLING_CYCLE_CHOICES = [
        ('daily', _('Daily')),
        ('weekly', _('Weekly')),
        ('monthly', _('Monthly')),
        ('quarterly', _('Quarterly')),  # Every 3 months
        ('semiannual', _('Semi-Annual')),  # Every 6 months
        ('annual', _('Annual')),
    ]

    # Identity
    tier_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_("Tier ID")
    )

    # Relationship
    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.CASCADE,
        related_name='pricing_tiers',
        verbose_name=_("Plan")
    )

    # Tier Information
    tier_name = models.CharField(
        max_length=100,
        verbose_name=_("Tier Name"),
        help_text=_("Display name (e.g., 'Monthly', 'Annual - Save 20%')")
    )

    # Translations
    translations = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Translations"),
        help_text=_("Multilingual content for tier name")
    )

    # Billing Configuration
    billing_cycle = models.CharField(
        max_length=20,
        choices=BILLING_CYCLE_CHOICES,
        default='monthly',
        verbose_name=_("Billing Cycle"),
        help_text=_("How often the customer is billed")
    )
    billing_interval = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(24)],
        verbose_name=_("Billing Interval"),
        help_text=_("Number of billing cycles between charges (e.g., '2' for 'every 2 months')")
    )

    # Discount Configuration
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_("Discount Percentage"),
        help_text=_("Discount applied to product price (e.g., 10.00 for 10% off product price, 0.00 for full price)")
    )

    # Status
    is_default = models.BooleanField(
        default=False,
        verbose_name=_("Default Tier"),
        help_text=_("Show this tier as the default option to customers")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
        help_text=_("Whether this tier can be selected by customers")
    )

    # Ordering
    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Sort Order"),
        help_text=_("Display order within the plan")
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Pricing Tier")
        verbose_name_plural = _("Pricing Tiers")
        ordering = ['plan', 'sort_order', 'tier_name']
        unique_together = [['plan', 'tier_name']]
        indexes = [
            models.Index(fields=['plan', 'is_active']),
            models.Index(fields=['plan', 'is_default']),
        ]

    def __str__(self):
        return f"{self.plan.name} - {self.tier_name}"

    def get_billing_display(self):
        """Get human-readable billing frequency"""
        if self.billing_interval == 1:
            return self.get_billing_cycle_display()
        return f"Every {self.billing_interval} {self.get_billing_cycle_display()}s"

    def calculate_price(self, product, variant=None):
        """
        Calculate subscription price from product price and discount.

        Args:
            product: Product instance to get base price from
            variant: Optional ProductVariant to use variant-specific pricing

        Returns:
            Money object with calculated price
        """
        from djmoney.money import Money

        # Use variant price if provided, otherwise product price
        base_price = variant.price if variant else product.price

        # Apply discount percentage
        discount_multiplier = Decimal('1.00') - (self.discount_percentage / Decimal('100'))
        discounted_amount = base_price.amount * discount_multiplier

        return Money(discounted_amount, base_price.currency)

    def get_annual_price(self, product, variant=None):
        """
        Calculate approximate annual cost for this tier.

        Args:
            product: Product instance to get base price from
            variant: Optional ProductVariant to use variant-specific pricing

        Returns:
            Money object with approximate annual cost
        """
        cycle_multipliers = {
            'daily': 365,
            'weekly': 52,
            'monthly': 12,
            'quarterly': 4,
            'semiannual': 2,
            'annual': 1,
        }

        # Get discounted price per cycle
        price_per_cycle = self.calculate_price(product, variant)

        # Calculate annual cost
        multiplier = cycle_multipliers.get(self.billing_cycle, 12) / self.billing_interval
        annual_amount = price_per_cycle.amount * Decimal(str(multiplier))

        return Money(annual_amount, price_per_cycle.currency)


class PlanAddon(models.Model):
    """
    Defines an optional add-on for a subscription plan.

    Example: "Priority Support" add-on for $10/month
    """

    # Billing Frequency Choices
    BILLING_FREQUENCY_CHOICES = [
        ('per_cycle', _('Per Billing Cycle')),  # Charged every billing cycle
        ('one_time', _('One-Time')),  # Charged once at subscription start
    ]

    # Identity
    addon_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_("Add-on ID")
    )

    # Relationship
    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.CASCADE,
        related_name='addons',
        verbose_name=_("Plan")
    )

    # Add-on Information
    name = models.CharField(
        max_length=200,
        verbose_name=_("Add-on Name"),
        help_text=_("Name displayed to customers (e.g., 'Priority Support', 'Extra Storage')")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description"),
        help_text=_("Detailed description of what this add-on provides")
    )

    # Translations
    translations = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Translations"),
        help_text=_("Multilingual content for add-on name and description")
    )

    # Pricing
    price = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='USD',
        verbose_name=_("Price"),
        help_text=_("Add-on price per billing frequency")
    )
    billing_frequency = models.CharField(
        max_length=15,
        choices=BILLING_FREQUENCY_CHOICES,
        default='per_cycle',
        verbose_name=_("Billing Frequency"),
        help_text=_("How often the add-on is charged")
    )

    # Quantity Support
    allow_quantity = models.BooleanField(
        default=False,
        verbose_name=_("Allow Quantity"),
        help_text=_("Allow customers to select multiple units of this add-on")
    )

    # Status
    is_required = models.BooleanField(
        default=False,
        verbose_name=_("Required"),
        help_text=_("Automatically include this add-on in all new subscriptions")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
        help_text=_("Whether this add-on can be purchased")
    )

    # Ordering
    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Sort Order"),
        help_text=_("Display order")
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Plan Add-on")
        verbose_name_plural = _("Plan Add-ons")
        ordering = ['plan', 'sort_order', 'name']
        indexes = [
            models.Index(fields=['plan', 'is_active']),
        ]

    def __str__(self):
        return f"{self.plan.name} - {self.name}"


class PaymentToken(models.Model):
    """
    Stores tokenized payment method for recurring billing.

    Payment tokens allow us to charge customers without storing sensitive card data.
    """

    # Payment Method Type Choices
    PAYMENT_METHOD_TYPE_CHOICES = [
        ('card', _('Credit/Debit Card')),
        ('bank_account', _('Bank Account (ACH)')),
        ('paypal', _('PayPal')),
        ('apple_pay', _('Apple Pay')),
        ('google_pay', _('Google Pay')),
    ]

    # Token Identity
    token_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        verbose_name=_("Token ID")
    )

    # Ownership
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payment_tokens',
        verbose_name=_("User")
    )
    provider_account = models.ForeignKey(
        'payment_providers.PaymentProviderAccount',
        on_delete=models.CASCADE,
        related_name='payment_tokens',
        verbose_name=_("Payment Provider Account")
    )

    # Token Data
    gateway_customer_id = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("Gateway Customer ID"),
        help_text=_("Customer ID in payment provider's system")
    )
    gateway_token_id = models.CharField(
        max_length=200,
        verbose_name=_("Gateway Token ID"),
        help_text=_("Payment method ID in payment provider's system")
    )

    # Payment Method Details
    payment_method_type = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_TYPE_CHOICES,
        default='card',
        verbose_name=_("Payment Method Type")
    )

    # Card-specific fields
    card_brand = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("Card Brand"),
        help_text=_("e.g., Visa, Mastercard, Amex")
    )
    card_last4 = models.CharField(
        max_length=4,
        blank=True,
        verbose_name=_("Card Last 4 Digits")
    )
    card_exp_month = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name=_("Card Expiration Month")
    )
    card_exp_year = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Card Expiration Year")
    )

    # Billing Address
    billing_address_line1 = models.CharField(max_length=255, blank=True, verbose_name=_("Address Line 1"))
    billing_address_line2 = models.CharField(max_length=255, blank=True, verbose_name=_("Address Line 2"))
    billing_city = models.CharField(max_length=100, blank=True, verbose_name=_("City"))
    billing_state = models.CharField(max_length=100, blank=True, verbose_name=_("State/Province"))
    billing_postal_code = models.CharField(max_length=20, blank=True, verbose_name=_("Postal Code"))
    billing_country = models.CharField(max_length=2, blank=True, verbose_name=_("Country Code"))

    # Status
    is_default = models.BooleanField(
        default=False,
        verbose_name=_("Default Payment Method"),
        help_text=_("Use this payment method for new subscriptions by default")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
        help_text=_("Whether this payment method can be used for billing")
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name=_("Verified"),
        help_text=_("Whether the payment method has been verified (e.g., bank account verified)")
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Payment Token")
        verbose_name_plural = _("Payment Tokens")
        ordering = ['-is_default', '-created_at']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['provider_account', 'gateway_token_id']),
        ]

    def __str__(self):
        if self.payment_method_type == 'card':
            return f"{self.card_brand} •••• {self.card_last4}"
        return f"{self.get_payment_method_type_display()}"

    def is_expired(self):
        """Check if payment method is expired"""
        if self.payment_method_type != 'card' or not (self.card_exp_month and self.card_exp_year):
            return False

        now = timezone.now()
        # Card expires at end of expiration month
        return (self.card_exp_year < now.year) or \
               (self.card_exp_year == now.year and self.card_exp_month < now.month)


class CustomerSubscription(models.Model):
    """
    Represents a customer's active subscription to a plan.

    Tracks the full subscription lifecycle: trial, active, paused, canceled, expired.
    """

    # Subscription Status Choices
    STATUS_CHOICES = [
        ('trial', _('Trial')),  # In free/reduced trial period
        ('active', _('Active')),  # Actively billing and providing service
        ('past_due', _('Past Due')),  # Payment failed, retrying
        ('paused', _('Paused')),  # Temporarily suspended by customer
        ('canceled', _('Canceled')),  # Canceled, may still have access until period end
        ('expired', _('Expired')),  # Subscription ended (trial expired, max cycles reached, etc.)
    ]

    # Provider Mode Choices
    PROVIDER_MODE_CHOICES = [
        ('native', _('Native Provider')),  # Stripe/PayPal manages billing
        ('fallback', _('Fallback Provider')),  # Internal billing engine
    ]

    # Cancellation Type Choices
    CANCELLATION_TYPE_CHOICES = [
        ('none', _('Not Canceled')),
        ('immediate', _('Immediate Cancellation')),
        ('end_of_period', _('Cancel at Period End')),
        ('scheduled', _('Scheduled Cancellation')),
    ]

    # Identity
    subscription_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        verbose_name=_("Subscription ID")
    )

    # Relationships
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name=_("User")
    )
    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.PROTECT,
        related_name='subscriptions',
        verbose_name=_("Plan")
    )
    pricing_tier = models.ForeignKey(
        PlanPricingTier,
        on_delete=models.PROTECT,
        related_name='subscriptions',
        verbose_name=_("Pricing Tier"),
        help_text=_("Which pricing tier the customer selected")
    )

    # Product Linkage (subscriptions can be tied to catalog products)
    product = models.ForeignKey(
        'catalog.Product',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subscriptions',
        verbose_name=_("Product")
    )
    variant = models.ForeignKey(
        'catalog.ProductVariant',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subscriptions',
        verbose_name=_("Product Variant")
    )

    # Order Linkage
    originating_order = models.ForeignKey(
        'orders.Order',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subscriptions_created',
        verbose_name=_("Originating Order"),
        help_text=_("The order from which this subscription was created")
    )

    # Quantity (for per-seat pricing)
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name=_("Quantity"),
        help_text=_("Number of seats/units subscribed (for quantity-based pricing)")
    )

    # Payment Configuration
    payment_provider_account = models.ForeignKey(
        'payment_providers.PaymentProviderAccount',
        on_delete=models.PROTECT,
        related_name='subscriptions',
        verbose_name=_("Payment Provider Account")
    )
    payment_token = models.ForeignKey(
        PaymentToken,
        on_delete=models.PROTECT,
        related_name='subscriptions',
        verbose_name=_("Payment Token"),
        help_text=_("Payment method used for recurring billing")
    )
    provider_mode = models.CharField(
        max_length=20,
        choices=PROVIDER_MODE_CHOICES,
        default='native',
        verbose_name=_("Provider Mode")
    )
    provider_subscription_id = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("Provider Subscription ID"),
        help_text=_("Subscription ID in payment provider's system (for native mode)")
    )

    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='trial',
        verbose_name=_("Status")
    )

    # Billing Schedule
    current_period_start = models.DateTimeField(
        verbose_name=_("Current Period Start"),
        help_text=_("Start date of current billing period")
    )
    current_period_end = models.DateTimeField(
        verbose_name=_("Current Period End"),
        help_text=_("End date of current billing period")
    )
    next_billing_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Next Billing Date"),
        help_text=_("Date of next scheduled billing attempt")
    )
    trial_end_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Trial End Date"),
        help_text=_("End date of trial period")
    )

    # Billing History
    billing_cycle_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Billing Cycle Count"),
        help_text=_("Number of successful billing cycles completed")
    )
    last_billing_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Last Billing Date")
    )
    last_billing_status = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_("Last Billing Status")
    )

    # Cancellation
    cancellation_type = models.CharField(
        max_length=20,
        choices=CANCELLATION_TYPE_CHOICES,
        default='none',
        verbose_name=_("Cancellation Type")
    )
    canceled_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Canceled At")
    )
    cancellation_reason = models.TextField(
        blank=True,
        verbose_name=_("Cancellation Reason")
    )

    # Commitment & Grace Periods
    minimum_commitment_end_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Minimum Commitment End Date"),
        help_text=_("Date when minimum commitment period ends")
    )
    reactivation_deadline = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Reactivation Deadline"),
        help_text=_("Deadline for reactivating canceled subscription")
    )
    grace_period_end_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Grace Period End Date"),
        help_text=_("When grace period expires after payment failure (null = not in grace period)")
    )

    # Pause/Resume
    paused_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Paused At")
    )
    pause_reason = models.TextField(
        blank=True,
        verbose_name=_("Pause Reason")
    )
    auto_resume_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Auto Resume Date"),
        help_text=_("Date to automatically resume paused subscription")
    )

    # Plan Changes & Proration
    scheduled_plan_change = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Scheduled Plan Change"),
        help_text=_("Scheduled tier/plan change for future date")
    )
    proration_credit = MoneyField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        default_currency='USD',
        verbose_name=_("Proration Credit"),
        help_text=_("Credit from downgrades to be applied to next bill")
    )

    # Metadata
    metadata = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Metadata")
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Customer Subscription")
        verbose_name_plural = _("Customer Subscriptions")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['status', 'next_billing_date']),
            models.Index(fields=['provider_subscription_id']),
            models.Index(fields=['trial_end_date']),
            models.Index(fields=['auto_resume_date']),
            models.Index(fields=['status', 'grace_period_end_date']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.plan.name} ({self.get_status_display()})"

    def days_until_next_billing(self):
        """Calculate days until next billing"""
        if not self.next_billing_date:
            return None
        delta = self.next_billing_date - timezone.now()
        return max(0, delta.days)

    def is_in_trial(self):
        """Check if subscription is currently in trial period"""
        return self.status == 'trial' and self.trial_end_date and self.trial_end_date > timezone.now()

    def is_in_grace_period(self):
        """Check if subscription is currently in a dunning grace period."""
        return (
            self.status == 'past_due'
            and self.grace_period_end_date is not None
            and self.grace_period_end_date > timezone.now()
        )

    def has_scheduled_plan_change(self):
        """Check if there is a pending scheduled plan change."""
        return bool(self.scheduled_plan_change)

    def cancel_scheduled_plan_change(self):
        """Cancel any pending scheduled plan change."""
        self.scheduled_plan_change = {}
        self.save(update_fields=['scheduled_plan_change'])

    def can_reactivate(self):
        """Check if subscription can be reactivated"""
        if self.status != 'canceled':
            return False
        if not self.reactivation_deadline:
            return False
        return timezone.now() <= self.reactivation_deadline

    def total_amount_paid(self):
        """Calculate total amount paid across all successful billing cycles"""
        from django.db.models import Sum
        total = self.billing_logs.filter(status='successful').aggregate(
            total=Sum('total_amount')
        )['total']
        return total if total else Decimal('0.00')


class CustomerSubscriptionAddon(models.Model):
    """
    Tracks which add-ons a customer has activated on their subscription.
    """

    # Identity
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # Relationships
    subscription = models.ForeignKey(
        CustomerSubscription,
        on_delete=models.CASCADE,
        related_name='active_addons',
        verbose_name=_("Subscription")
    )
    addon = models.ForeignKey(
        PlanAddon,
        on_delete=models.PROTECT,
        verbose_name=_("Add-on")
    )

    # Quantity
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name=_("Quantity")
    )

    # Status
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active")
    )

    # Timestamps
    activated_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Activated At")
    )
    deactivated_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Deactivated At")
    )

    class Meta:
        verbose_name = _("Subscription Add-on")
        verbose_name_plural = _("Subscription Add-ons")
        ordering = ['subscription', 'addon']
        unique_together = [['subscription', 'addon']]
        indexes = [
            models.Index(fields=['subscription', 'is_active']),
        ]

    def __str__(self):
        return f"{self.subscription.user.email} - {self.addon.name}"

    def calculate_cost(self):
        """Calculate cost of this add-on"""
        return self.addon.price.amount * self.quantity


class SubscriptionDiscount(models.Model):
    """
    Represents a discount applied to a customer's subscription.

    Supports promotional pricing, coupon codes, and special offers.
    """

    # Discount Type Choices
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', _('Percentage Off')),  # e.g., 20% off
        ('fixed_amount', _('Fixed Amount Off')),  # e.g., $10 off
        ('fixed_price_override', _('Fixed Price Override')),  # e.g., $5/month instead of $10/month
    ]

    # Duration Type Choices
    DURATION_TYPE_CHOICES = [
        ('once', _('Apply Once')),  # Apply to next billing cycle only
        ('forever', _('Forever')),  # Apply to all future billing cycles
        ('repeating', _('Repeating')),  # Apply for X months
    ]

    # Identity
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # Relationship
    subscription = models.ForeignKey(
        CustomerSubscription,
        on_delete=models.CASCADE,
        related_name='discounts',
        verbose_name=_("Subscription")
    )

    # Coupon Information
    coupon_code = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("Coupon Code"),
        help_text=_("Coupon code used to apply this discount (if applicable)")
    )

    # Discount Configuration
    discount_type = models.CharField(
        max_length=25,
        choices=DISCOUNT_TYPE_CHOICES,
        default='percentage',
        verbose_name=_("Discount Type")
    )
    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_("Discount Value"),
        help_text=_("Percentage (e.g., 20.00 for 20%), amount, or fixed price depending on type")
    )

    # Duration
    duration_type = models.CharField(
        max_length=15,
        choices=DURATION_TYPE_CHOICES,
        default='once',
        verbose_name=_("Duration Type")
    )
    duration_months = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Duration (Months)"),
        help_text=_("Number of months to apply discount (for repeating type)")
    )
    remaining_cycles = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Remaining Cycles"),
        help_text=_("Billing cycles remaining for this discount")
    )

    # Status
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active")
    )

    # Timestamps
    applied_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Applied At")
    )
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Expires At")
    )

    class Meta:
        verbose_name = _("Subscription Discount")
        verbose_name_plural = _("Subscription Discounts")
        ordering = ['subscription', '-applied_at']
        indexes = [
            models.Index(fields=['subscription', 'is_active']),
            models.Index(fields=['coupon_code']),
        ]

    def __str__(self):
        return f"{self.subscription.user.email} - {self.get_discount_display()}"

    def get_discount_display(self):
        """Get human-readable discount description"""
        if self.discount_type == 'percentage':
            return f"{self.value}% off"
        elif self.discount_type == 'fixed_amount':
            return f"${self.value} off"
        else:
            return f"${self.value} fixed price"

    def calculate_discount_amount(self, base_amount):
        """Calculate discount amount for given base amount"""
        if self.discount_type == 'percentage':
            return base_amount * (self.value / Decimal('100'))
        elif self.discount_type == 'fixed_amount':
            return min(self.value, base_amount)  # Can't discount more than base
        else:  # fixed_price_override
            return max(Decimal('0'), base_amount - self.value)


class BillingCycleLog(models.Model):
    """
    Audit log of billing cycles and payment attempts.

    Provides complete billing history with detailed breakdowns.
    """

    # Billing Status Choices
    STATUS_CHOICES = [
        ('pending', _('Pending')),  # Scheduled but not yet attempted
        ('processing', _('Processing')),  # Payment currently processing
        ('successful', _('Successful')),  # Payment succeeded
        ('failed', _('Failed')),  # Payment failed
        ('retrying', _('Retrying')),  # Failed, will retry
    ]

    # Identity
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # Relationship
    subscription = models.ForeignKey(
        CustomerSubscription,
        on_delete=models.CASCADE,
        related_name='billing_logs',
        verbose_name=_("Subscription")
    )

    # Billing Information
    cycle_number = models.PositiveIntegerField(
        verbose_name=_("Cycle Number"),
        help_text=_("Which billing cycle this is (1 = first billing)")
    )
    billing_date = models.DateTimeField(
        verbose_name=_("Billing Date"),
        help_text=_("Date billing was attempted")
    )

    # Amount Breakdown
    base_amount = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='USD',
        verbose_name=_("Base Amount"),
        help_text=_("Plan price before quantity/addons/discounts")
    )
    quantity_amount = MoneyField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        default_currency='USD',
        verbose_name=_("Quantity Amount"),
        help_text=_("Additional charge for quantity (quantity × price)")
    )
    addons_amount = MoneyField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        default_currency='USD',
        verbose_name=_("Add-ons Amount"),
        help_text=_("Total cost of active add-ons")
    )
    discount_amount = MoneyField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        default_currency='USD',
        verbose_name=_("Discount Amount"),
        help_text=_("Total discounts applied")
    )
    tax_amount = MoneyField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        default_currency='USD',
        verbose_name=_("Tax Amount"),
        help_text=_("Calculated tax")
    )
    proration_amount = MoneyField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        default_currency='USD',
        verbose_name=_("Proration Amount"),
        help_text=_("Proration credit/charge from plan changes")
    )
    total_amount = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='USD',
        verbose_name=_("Total Amount"),
        help_text=_("Final amount charged (base + quantity + addons - discounts + tax + proration)")
    )

    # Itemized Breakdown
    billing_breakdown = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Billing Breakdown"),
        help_text=_("Detailed itemized breakdown of charges")
    )

    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_("Status")
    )

    # Transaction References
    transaction = models.ForeignKey(
        'payment_providers.PaymentTransaction',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='billing_logs',
        verbose_name=_("Payment Transaction")
    )
    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subscription_billing_logs',
        verbose_name=_("Order")
    )

    # Retry Management
    retry_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Retry Count"),
        help_text=_("Number of times billing has been retried")
    )
    max_retries = models.PositiveIntegerField(
        default=3,
        verbose_name=_("Maximum Retries")
    )
    next_retry_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Next Retry Date")
    )

    # Error Details
    error_message = models.TextField(
        blank=True,
        verbose_name=_("Error Message")
    )
    error_code = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Error Code")
    )
    provider_response = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Provider Response"),
        help_text=_("Raw response from payment provider")
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Billing Cycle Log")
        verbose_name_plural = _("Billing Cycle Logs")
        ordering = ['-created_at']
        unique_together = [['subscription', 'cycle_number']]
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['subscription', 'status']),
            models.Index(fields=['status', 'next_retry_date']),
        ]

    def __str__(self):
        return f"Cycle {self.cycle_number} - {self.subscription.user.email} - {self.get_status_display()}"

    def can_retry(self):
        """Check if this billing can be retried"""
        return (
            self.status == 'failed' and
            self.retry_count < self.max_retries and
            self.subscription.status != 'canceled'
        )

    def calculate_next_retry_date(self):
        """Calculate next retry date using exponential backoff"""
        if not self.can_retry():
            return None

        # Exponential backoff: 2, 4, 8 hours
        hours = 2 ** (self.retry_count + 1)
        return timezone.now() + timedelta(hours=hours)


class SubscriptionWebhookEvent(models.Model):
    """
    Audit log for subscription lifecycle events.
    Provides idempotency (prevents duplicate processing) and an audit trail
    for both webhook events (native providers) and synthetic events (fallback engine).
    """

    SOURCE_CHOICES = [
        ('webhook', _('Webhook')),
        ('fallback', _('Fallback Engine')),
    ]

    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('processed', _('Processed')),
        ('failed', _('Failed')),
        ('skipped', _('Skipped')),
    ]

    # Event identification
    event_id = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name=_("Event ID"),
        help_text=_("Provider event ID or generated fallback ID")
    )
    event_type = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name=_("Event Type"),
        help_text=_("Standardized event type (e.g. subscription.payment_succeeded)")
    )
    provider_event_type = models.CharField(
        max_length=100,
        blank=True,
        default='',
        verbose_name=_("Provider Event Type"),
        help_text=_("Original provider-specific event type")
    )
    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        verbose_name=_("Source"),
        help_text=_("Whether this event came from a webhook or fallback engine")
    )

    # Subscription linkage
    subscription = models.ForeignKey(
        'subscriptions.CustomerSubscription',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='webhook_events',
        verbose_name=_("Subscription"),
        help_text=_("Linked subscription (null if not yet matched)")
    )
    provider_subscription_id = models.CharField(
        max_length=200,
        db_index=True,
        blank=True,
        default='',
        verbose_name=_("Provider Subscription ID"),
        help_text=_("Provider's subscription ID for lookup")
    )

    # Event data
    event_data = models.JSONField(
        default=dict,
        verbose_name=_("Event Data"),
        help_text=_("Full serialized SubscriptionEvent")
    )

    # Processing status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        db_index=True,
        verbose_name=_("Status")
    )
    processing_error = models.TextField(
        blank=True,
        default='',
        verbose_name=_("Processing Error"),
        help_text=_("Error message if processing failed")
    )
    retry_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Retry Count")
    )

    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At")
    )
    processed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Processed At")
    )

    class Meta:
        verbose_name = _("Subscription Webhook Event")
        verbose_name_plural = _("Subscription Webhook Events")
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['event_id', 'source'],
                name='unique_subscription_event'
            ),
        ]
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status', 'retry_count']),
            models.Index(fields=['provider_subscription_id', '-created_at']),
        ]

    def __str__(self):
        return f"{self.event_type} ({self.source}) - {self.get_status_display()}"
