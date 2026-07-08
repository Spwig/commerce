"""
License Checkout Models

Models for the spwig.com purchase flows:

Self-Hosted Licenses:
1. LicenseProduct — purchasable license offerings (trial, core, bundle, dev)
2. LicenseCheckoutRequest — tracks each checkout attempt and its provisioning status

Hosted Subscriptions:
3. HostedPlan — subscription plan tiers displayed on the pricing page
4. HostedSubscription — tracks ongoing hosted subscription billing lifecycle
5. HostedBillingLog — audit trail for each billing cycle attempt
6. HostedCheckoutRequest — tracks hosted plan checkout → payment → provisioning
"""

import uuid
from decimal import Decimal

from django.conf import settings
from django.db import models
from django_countries.fields import CountryField
from djmoney.models.fields import MoneyField


class LicenseProduct(models.Model):
    """
    A purchasable license offering displayed on the spwig.com purchase page.
    Managed via Django admin — pricing changes here flow to the frontend API.
    """

    class ProductType(models.TextChoices):
        TRIAL = 'trial', 'Free Trial'
        LICENSE = 'license', 'Production License'
        BUNDLE = 'bundle', 'Bundle'
        ADDON = 'addon', 'Add-on'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    product_type = models.CharField(max_length=20, choices=ProductType.choices)

    price = MoneyField(
        max_digits=10, decimal_places=2,
        default_currency='EUR', default=0,
        help_text='Current selling price',
    )
    regular_price = MoneyField(
        max_digits=10, decimal_places=2,
        default_currency='EUR', default=0,
        help_text='Original price (shown as strikethrough)',
    )
    savings_amount = MoneyField(
        max_digits=10, decimal_places=2,
        default_currency='EUR', default=0, null=True, blank=True,
        help_text='Amount saved vs buying separately (for bundles)',
    )

    features = models.JSONField(
        default=list, blank=True,
        help_text='List of feature key strings for display on the card',
    )
    includes_pos = models.BooleanField(default=False)
    trial_days = models.PositiveIntegerField(
        default=0,
        help_text='Number of trial days (0 for non-trial products)',
    )

    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(
        default=False,
        help_text='Highlighted as recommended / best value',
    )
    note = models.CharField(
        max_length=300, blank=True, default='',
        help_text='Optional note displayed on the card (e.g. "First license free via Developer Portal")',
    )
    note_link = models.CharField(
        max_length=200, blank=True, default='',
        help_text='Optional URL for the note text',
    )
    sort_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'created_at']

    def __str__(self):
        return f"{self.name} ({self.price})"


class LicenseCheckoutRequest(models.Model):
    """
    Tracks each license checkout attempt — from initial request through
    payment and provisioning. Serves as the audit trail for license sales.
    """

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PROVISIONING = 'provisioning', 'Provisioning'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    license_product = models.ForeignKey(
        LicenseProduct, on_delete=models.PROTECT,
        related_name='checkout_requests',
    )
    email = models.EmailField(db_index=True)
    name = models.CharField(max_length=200, blank=True, default='')
    company = models.CharField(max_length=200, blank=True, default='')
    billing_country = CountryField(blank=True, default='')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='license_checkout_requests',
    )

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING,
    )

    # Payment (null for free trials)
    order = models.ForeignKey(
        'orders.Order', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='license_checkouts',
    )
    payment_intent = models.ForeignKey(
        'payment_providers.PaymentIntent', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='license_checkouts',
    )

    # License provisioning results (from upgrade server)
    license_key = models.CharField(max_length=255, blank=True, default='')
    setup_token = models.TextField(blank=True, default='')
    setup_token_id = models.UUIDField(null=True, blank=True)
    setup_token_expires_at = models.DateTimeField(null=True, blank=True)

    error_message = models.TextField(blank=True, default='')
    metadata = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.email} — {self.license_product.name} ({self.status})"


# ---------------------------------------------------------------------------
# Hosted Subscription Models
# ---------------------------------------------------------------------------

class HostedPlan(models.Model):
    """
    A hosted subscription plan displayed on the spwig.com pricing page.
    Maps 1:1 to a SubscriptionPlan on the update server by slug.
    Pricing is stored here for the frontend; quotas/enforcement live on the
    update server's SubscriptionPlan model.
    """

    class InfraTier(models.TextChoices):
        SHARED = 'shared', 'Shared Fleet'
        DEDICATED = 'dedicated', 'Dedicated Linode'
        PREMIUM = 'premium', 'Premium Dedicated'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=50, unique=True,
                            help_text='Must match SubscriptionPlan.slug on the update server')
    name = models.CharField(max_length=200)
    tagline = models.CharField(max_length=300, blank=True, default='',
                               help_text='Short description for pricing card')

    # Pricing (EUR). monthly_price = price when billed monthly.
    # annual_price = per-month price when billed annually (e.g. €59/mo billed as €708/yr).
    monthly_price = MoneyField(
        max_digits=10, decimal_places=2, default_currency='EUR', default=0,
        help_text='Monthly billing price (e.g. €69 for Starter)',
    )
    annual_price = MoneyField(
        max_digits=10, decimal_places=2, default_currency='EUR', default=0,
        help_text='Per-month price when billed annually (e.g. €59 for Starter)',
    )

    # Infrastructure tier
    infra_tier = models.CharField(max_length=20, choices=InfraTier.choices)

    # Plan limits (for display on pricing page — enforcement is on the update server)
    max_products = models.IntegerField(default=0, help_text='0 = unlimited')
    max_staff = models.IntegerField(default=0, help_text='0 = unlimited')
    storage_gb = models.IntegerField(default=25)
    emails_monthly = models.IntegerField(default=10000)
    includes_pos = models.BooleanField(default=False,
                                       help_text='POS included in plan (Pro Plus)')
    includes_api = models.BooleanField(default=False,
                                       help_text='API access included')
    includes_sla = models.BooleanField(default=False,
                                       help_text='SLA guarantee included')
    includes_custom_domain = models.BooleanField(default=True)

    # Feature keys for frontend display
    features = models.JSONField(
        default=list, blank=True,
        help_text='List of feature key strings for pricing card bullets',
    )

    # Introductory offer — monthly billing (admin-configurable)
    intro_monthly_discount_percent = models.IntegerField(
        default=50,
        help_text='Percentage discount for monthly intro period (e.g. 50 = half price)',
    )
    intro_monthly_discount_cycles = models.IntegerField(
        default=3,
        help_text='Number of monthly billing cycles the discount applies (0 = no intro offer)',
    )
    # Introductory offer — annual billing (admin-configurable)
    intro_annual_discount_percent = models.IntegerField(
        default=30,
        help_text='Percentage discount for annual intro period (e.g. 30 = 30%% off)',
    )
    intro_annual_discount_cycles = models.IntegerField(
        default=1,
        help_text='Number of annual billing cycles the discount applies (0 = no intro offer)',
    )

    # Display
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(
        default=False, help_text='Highlighted as recommended / best value',
    )
    sort_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'created_at']

    def __str__(self):
        return f"{self.name} (€{self.annual_price.amount}/mo annual, €{self.monthly_price.amount}/mo monthly)"

    @property
    def annual_total(self):
        """Total annual cost when billed annually."""
        return self.annual_price.amount * 12

    @property
    def has_intro_offer(self):
        """True if either monthly or annual intro offer is configured."""
        return (
            (self.intro_monthly_discount_cycles > 0 and self.intro_monthly_discount_percent > 0)
            or (self.intro_annual_discount_cycles > 0 and self.intro_annual_discount_percent > 0)
        )

    @property
    def has_monthly_intro(self):
        return self.intro_monthly_discount_cycles > 0 and self.intro_monthly_discount_percent > 0

    @property
    def has_annual_intro(self):
        return self.intro_annual_discount_cycles > 0 and self.intro_annual_discount_percent > 0

    @property
    def intro_monthly_price(self):
        """Monthly price during introductory period."""
        if not self.has_monthly_intro:
            return self.monthly_price.amount
        multiplier = Decimal(100 - self.intro_monthly_discount_percent) / Decimal(100)
        return (self.monthly_price.amount * multiplier).quantize(Decimal('0.01'))

    @property
    def intro_annual_price(self):
        """Per-month price during introductory period (annual billing)."""
        if not self.has_annual_intro:
            return self.annual_price.amount
        multiplier = Decimal(100 - self.intro_annual_discount_percent) / Decimal(100)
        return (self.annual_price.amount * multiplier).quantize(Decimal('0.01'))


class HostedSubscription(models.Model):
    """
    Tracks a Spwig hosted subscription lifecycle and billing state.

    Manages recurring billing via Airwallex payment consents (saved cards)
    charged by internal Celery tasks. Deliberately separate from
    subscriptions.CustomerSubscription (merchant-to-customer billing).
    """

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending Payment'
        ACTIVE = 'active', 'Active'
        PAST_DUE = 'past_due', 'Past Due'
        SUSPENDED = 'suspended', 'Suspended'
        CANCELLED = 'cancelled', 'Cancelled'
        TERMINATED = 'terminated', 'Terminated'

    class BillingInterval(models.TextChoices):
        MONTHLY = 'monthly', 'Monthly'
        ANNUAL = 'annual', 'Annual'

    class CancellationType(models.TextChoices):
        NONE = 'none', 'Not Cancelled'
        END_OF_PERIOD = 'end_of_period', 'End of Billing Period'
        IMMEDIATE = 'immediate', 'Immediate'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Plan
    hosted_plan = models.ForeignKey(
        HostedPlan, on_delete=models.PROTECT, related_name='subscriptions',
    )
    billing_interval = models.CharField(
        max_length=10, choices=BillingInterval.choices,
    )

    # Customer
    email = models.EmailField(db_index=True)
    name = models.CharField(max_length=200, blank=True, default='')
    company = models.CharField(max_length=200, blank=True, default='')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='hosted_subscriptions',
    )

    # Store identity
    store_name = models.CharField(max_length=200)
    store_slug = models.SlugField(max_length=63, unique=True)
    region = models.CharField(max_length=30)

    # License (created on the update server during checkout)
    license_key = models.CharField(max_length=255, blank=True, default='')

    # Payment
    payment_provider_account = models.ForeignKey(
        'payment_providers.PaymentProviderAccount', on_delete=models.PROTECT,
        null=True, blank=True,
    )
    airwallex_customer_id = models.CharField(max_length=200, blank=True, default='')
    airwallex_consent_id = models.CharField(
        max_length=200, blank=True, default='',
        help_text='Payment consent ID for recurring off-session charges',
    )

    # Billing state
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True,
    )
    current_period_start = models.DateTimeField(null=True, blank=True)
    current_period_end = models.DateTimeField(null=True, blank=True)
    next_billing_date = models.DateTimeField(null=True, blank=True, db_index=True)
    billing_cycle_count = models.IntegerField(default=0)
    last_billing_date = models.DateTimeField(null=True, blank=True)
    last_billing_status = models.CharField(max_length=20, blank=True, default='')

    # Grace / dunning
    grace_period_end_date = models.DateTimeField(null=True, blank=True)
    retry_count = models.IntegerField(default=0)

    # Suspension
    suspended_at = models.DateTimeField(null=True, blank=True)

    # Cancellation
    cancellation_type = models.CharField(
        max_length=20, choices=CancellationType.choices, default=CancellationType.NONE,
    )
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.CharField(max_length=500, blank=True, default='')
    termination_scheduled_at = models.DateTimeField(null=True, blank=True)

    # Add-ons
    pos_addon = models.BooleanField(
        default=False, help_text='POS add-on active (€29/mo, changes at next period)',
    )

    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    error_message = models.TextField(blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'next_billing_date']),
            models.Index(fields=['status', 'grace_period_end_date']),
            models.Index(fields=['status', 'termination_scheduled_at']),
            models.Index(fields=['suspended_at']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['license_key'],
                condition=~models.Q(license_key=''),
                name='unique_nonempty_license_key',
            ),
        ]

    def __str__(self):
        return f"{self.store_name} — {self.hosted_plan.name} ({self.status})"

    @property
    def is_in_intro_period(self):
        """True if the subscription is still within the introductory discount period.

        billing_cycle_count starts at 1 (set at creation = initial checkout payment).
        process_due_billing reads billing_amount BEFORE incrementing the count.
        So for 3 monthly intro cycles: count=1,2 at read time → 2 renewals at intro,
        plus the initial checkout = 3 total intro payments.
        """
        plan = self.hosted_plan
        if self.billing_interval == self.BillingInterval.ANNUAL:
            if not plan.has_annual_intro:
                return False
            return self.billing_cycle_count < plan.intro_annual_discount_cycles
        else:
            if not plan.has_monthly_intro:
                return False
            return self.billing_cycle_count < plan.intro_monthly_discount_cycles

    @property
    def _intro_discount_percent(self):
        """Current intro discount percent based on billing interval."""
        plan = self.hosted_plan
        if self.billing_interval == self.BillingInterval.ANNUAL:
            return plan.intro_annual_discount_percent
        return plan.intro_monthly_discount_percent

    @property
    def billing_amount(self):
        """Current billing amount per cycle including add-ons and intro discount."""
        plan = self.hosted_plan

        # Apply introductory discount if within intro period
        if self.is_in_intro_period:
            if self.billing_interval == self.BillingInterval.ANNUAL:
                base = plan.intro_annual_price * 12
            else:
                base = plan.intro_monthly_price
        else:
            if self.billing_interval == self.BillingInterval.ANNUAL:
                base = plan.annual_price.amount * 12
            else:
                base = plan.monthly_price.amount

        # POS add-on (not charged if plan includes POS)
        if self.pos_addon and not plan.includes_pos:
            addon = Decimal('29.00')
            if self.is_in_intro_period:
                multiplier = Decimal(100 - self._intro_discount_percent) / Decimal(100)
                addon = (addon * multiplier).quantize(Decimal('0.01'))
            if self.billing_interval == self.BillingInterval.ANNUAL:
                addon *= 12
            base += addon

        return base


class HostedBillingLog(models.Model):
    """
    Audit trail for each billing attempt on a hosted subscription.
    One record per charge attempt (including retries).
    """

    class Status(models.TextChoices):
        PROCESSING = 'processing', 'Processing'
        SUCCESSFUL = 'successful', 'Successful'
        FAILED = 'failed', 'Failed'
        RETRYING = 'retrying', 'Retrying'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subscription = models.ForeignKey(
        HostedSubscription, on_delete=models.CASCADE, related_name='billing_logs',
    )
    cycle_number = models.IntegerField()
    billing_date = models.DateTimeField()
    amount = MoneyField(
        max_digits=10, decimal_places=2, default_currency='EUR', default=0,
    )
    status = models.CharField(max_length=20, choices=Status.choices)
    error_message = models.TextField(blank=True, default='')
    error_code = models.CharField(max_length=50, blank=True, default='')
    retry_count = models.IntegerField(default=0)
    max_retries = models.IntegerField(default=3)
    next_retry_date = models.DateTimeField(null=True, blank=True)
    provider_response = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['subscription', 'cycle_number']),
        ]

    def __str__(self):
        return f"Cycle {self.cycle_number} — {self.subscription.store_name} ({self.status})"


class HostedCheckoutRequest(models.Model):
    """
    Tracks a hosted plan checkout attempt — from initial form submission
    through payment and provisioning. Analogous to LicenseCheckoutRequest
    but for hosted subscriptions.
    """

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PAYMENT_PROCESSING = 'payment_processing', 'Payment Processing'
        PROVISIONING = 'provisioning', 'Provisioning'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hosted_plan = models.ForeignKey(
        HostedPlan, on_delete=models.PROTECT, related_name='checkout_requests',
    )
    billing_interval = models.CharField(
        max_length=10, choices=HostedSubscription.BillingInterval.choices,
    )

    # Customer
    email = models.EmailField(db_index=True)
    name = models.CharField(max_length=200, blank=True, default='')
    company = models.CharField(max_length=200, blank=True, default='')
    billing_country = CountryField(blank=True, default='')

    # Store setup
    store_name = models.CharField(max_length=200)
    store_slug = models.SlugField(max_length=63)
    region = models.CharField(max_length=30)
    pos_addon = models.BooleanField(default=False)

    # Payment
    payment_intent = models.ForeignKey(
        'payment_providers.PaymentIntent', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='hosted_checkouts',
    )
    order = models.ForeignKey(
        'orders.Order', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='hosted_checkouts',
    )

    # Result
    subscription = models.ForeignKey(
        HostedSubscription, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='checkout_requests',
    )

    status = models.CharField(
        max_length=25, choices=Status.choices, default=Status.PENDING,
    )
    error_message = models.TextField(blank=True, default='')
    metadata = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.email} — {self.hosted_plan.name} {self.billing_interval} ({self.status})"
