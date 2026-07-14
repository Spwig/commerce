"""
Affiliate App Models
Defines database models for affiliate program management, tracking, and payouts
"""

import secrets

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Program(models.Model):
    """
    Affiliate Program
    Defines commission structure and rules for an affiliate program
    """

    COMMISSION_TYPE_CHOICES = [
        ("percentage", _("Percentage")),
        ("fixed", _("Fixed Amount")),
    ]

    STATUS_CHOICES = [
        ("active", _("Active")),
        ("paused", _("Paused")),
        ("archived", _("Archived")),
    ]

    # Basic Information
    name = models.CharField(
        max_length=200,
        verbose_name=_("program name"),
        help_text=_("Descriptive name for this affiliate program"),
    )
    slug = models.SlugField(
        max_length=200, unique=True, verbose_name=_("slug"), help_text=_("URL-friendly identifier")
    )
    merchant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="affiliate_programs",
        verbose_name=_("merchant"),
        help_text=_("Program owner/merchant"),
    )
    description = models.TextField(
        blank=True, verbose_name=_("description"), help_text=_("Program description for affiliates")
    )

    # Commission Configuration
    commission_type = models.CharField(
        max_length=20,
        choices=COMMISSION_TYPE_CHOICES,
        default="percentage",
        verbose_name=_("commission type"),
    )
    commission_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_("commission value"),
        help_text=_("Percentage (0-100) or fixed amount"),
    )
    cookie_lifetime_days = models.IntegerField(
        default=30,
        validators=[MinValueValidator(1), MaxValueValidator(365)],
        verbose_name=_("cookie lifetime days"),
        help_text=_("How long to track clicks (1-365 days)"),
    )

    # Status and Settings
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="active", verbose_name=_("status")
    )
    auto_approve_affiliates = models.BooleanField(
        default=False,
        verbose_name=_("auto-approve affiliates"),
        help_text=_("Automatically approve new affiliate applications"),
    )
    minimum_payout = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=50.00,
        validators=[MinValueValidator(0)],
        verbose_name=_("minimum payout"),
        help_text=_("Minimum balance required for payout"),
    )

    # Timestamps
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        verbose_name = _("affiliate program")
        verbose_name_plural = _("affiliate programs")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["merchant", "status"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.name

    @property
    def commission_rate(self):
        """Template-friendly alias for commission_value."""
        return self.commission_value

    @property
    def cookie_duration(self):
        """Template-friendly alias for cookie_lifetime_days."""
        return self.cookie_lifetime_days


class Affiliate(models.Model):
    """
    Affiliate User
    Represents an affiliate participating in one or more programs
    """

    STATUS_CHOICES = [
        ("pending", _("Pending Approval")),
        ("active", _("Active")),
        ("suspended", _("Suspended")),
        ("rejected", _("Rejected")),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="affiliate_profile", verbose_name=_("user")
    )
    programs = models.ManyToManyField(
        Program,
        through="AffiliateProgramMembership",
        related_name="affiliates",
        verbose_name=_("programs"),
    )
    affiliate_code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name=_("affiliate code"),
        help_text=_("Unique identifier for this affiliate"),
    )

    # Contact Information
    company_name = models.CharField(max_length=200, blank=True, verbose_name=_("company name"))
    website = models.URLField(blank=True, verbose_name=_("website"))

    # Payment Information
    payment_email = models.EmailField(
        verbose_name=_("payment email"), help_text=_("Email for PayPal or other payment methods")
    )
    payment_method = models.CharField(
        max_length=50,
        default="paypal",
        verbose_name=_("payment method"),
        choices=[
            ("paypal", _("PayPal")),
            ("bank_transfer", _("Bank Transfer")),
        ],
    )

    # Bank Transfer Details (for Airwallex payouts)
    bank_account_holder = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("account holder name"),
        help_text=_("Name as it appears on the bank account"),
    )
    bank_account_number = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("account number"),
        help_text=_("Bank account number (encrypted in database)"),
    )
    bank_routing_code = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("routing code"),
        help_text=_("Bank routing/sort code (ABA, BSB, etc.)"),
    )
    bank_swift_code = models.CharField(
        max_length=11,
        blank=True,
        verbose_name=_("SWIFT/BIC code"),
        help_text=_("Bank SWIFT/BIC code for international transfers"),
    )
    bank_country = models.CharField(
        max_length=2,
        blank=True,
        verbose_name=_("bank country"),
        help_text=_("ISO 3166-1 alpha-2 country code (e.g., US, GB, AU)"),
    )
    bank_currency = models.CharField(
        max_length=3,
        blank=True,
        verbose_name=_("account currency"),
        help_text=_("ISO 4217 currency code (e.g., USD, GBP, EUR)"),
    )

    # Preferred payout provider (optional - system will auto-select based on payment_method if not set)
    preferred_payout_provider = models.ForeignKey(
        "payout_providers.PayoutProviderAccount",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="affiliates",
        verbose_name=_("preferred payout provider"),
        help_text=_("Override automatic provider selection"),
    )

    # Status
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name=_("status")
    )

    # Timestamps
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        verbose_name = _("affiliate")
        verbose_name_plural = _("affiliates")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["affiliate_code"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.affiliate_code})"

    def save(self, *args, **kwargs):
        if not self.affiliate_code:
            self.affiliate_code = self.generate_unique_code()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_unique_code():
        """Generate a unique affiliate code"""
        while True:
            code = secrets.token_urlsafe(8)[:8].upper()
            if not Affiliate.objects.filter(affiliate_code=code).exists():
                return code

    def get_balance_summary(self):
        """Get complete balance summary for affiliate"""
        from django.db.models import Sum

        # Total earned (approved + paid commissions)
        total_earned = (
            self.commissions.filter(status__in=["approved", "paid"]).aggregate(Sum("amount"))[
                "amount__sum"
            ]
            or 0
        )

        # Pending approval
        pending_approval = (
            self.commissions.filter(status="pending").aggregate(Sum("amount"))["amount__sum"] or 0
        )

        # Approved but not paid (outstanding balance)
        outstanding = (
            self.commissions.filter(status="approved").aggregate(Sum("amount"))["amount__sum"] or 0
        )

        # Already paid
        paid = self.commissions.filter(status="paid").aggregate(Sum("amount"))["amount__sum"] or 0

        # Total from all completed payouts
        total_payouts = (
            self.payouts.filter(status="completed").aggregate(Sum("amount"))["amount__sum"] or 0
        )

        return {
            "total_earned": total_earned,
            "pending_approval": pending_approval,
            "outstanding_balance": outstanding,
            "total_paid": paid,
            "total_payouts": total_payouts,
            "pending_payouts": self.payouts.filter(status__in=["pending", "processing"]).aggregate(
                Sum("amount")
            )["amount__sum"]
            or 0,
        }

    @property
    def outstanding_balance(self):
        """Calculate outstanding balance (approved but not paid)"""
        from django.db.models import Sum

        return (
            self.commissions.filter(status="approved").aggregate(Sum("amount"))["amount__sum"] or 0
        )

    @property
    def total_earned(self):
        """Calculate total earnings (approved + paid)"""
        from django.db.models import Sum

        return (
            self.commissions.filter(status__in=["approved", "paid"]).aggregate(Sum("amount"))[
                "amount__sum"
            ]
            or 0
        )

    @property
    def total_paid(self):
        """Calculate total paid amount"""
        from django.db.models import Sum

        return self.commissions.filter(status="paid").aggregate(Sum("amount"))["amount__sum"] or 0


class AffiliateProgramMembership(models.Model):
    """
    Through model for Affiliate-Program relationship
    Tracks affiliate participation in specific programs
    """

    STATUS_CHOICES = [
        ("pending", _("Pending")),
        ("approved", _("Approved")),
        ("rejected", _("Rejected")),
    ]

    affiliate = models.ForeignKey(Affiliate, on_delete=models.CASCADE, verbose_name=_("affiliate"))
    program = models.ForeignKey(Program, on_delete=models.CASCADE, verbose_name=_("program"))
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name=_("status")
    )
    notes = models.TextField(
        blank=True, verbose_name=_("notes"), help_text=_("Internal notes about this membership")
    )

    # Timestamps
    applied_at = models.DateTimeField(default=timezone.now, verbose_name=_("applied at"))
    approved_at = models.DateTimeField(null=True, blank=True, verbose_name=_("approved at"))

    class Meta:
        verbose_name = _("program membership")
        verbose_name_plural = _("program memberships")
        unique_together = [["affiliate", "program"]]
        ordering = ["-applied_at"]

    def __str__(self):
        return f"{self.affiliate.affiliate_code} - {self.program.name}"


class Link(models.Model):
    """
    Affiliate Tracking Link
    Unique link used by affiliates to track referrals
    """

    affiliate = models.ForeignKey(
        Affiliate, on_delete=models.CASCADE, related_name="links", verbose_name=_("affiliate")
    )
    program = models.ForeignKey(
        Program, on_delete=models.CASCADE, related_name="links", verbose_name=_("program")
    )
    link_code = models.CharField(
        max_length=32, unique=True, verbose_name=_("link code"), help_text=_("Unique tracking code")
    )
    destination_url = models.URLField(
        verbose_name=_("destination URL"), help_text=_("Where this link redirects to")
    )
    label = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("label"),
        help_text=_("Optional label for organizing links"),
    )
    is_active = models.BooleanField(default=True, verbose_name=_("is active"))

    # Timestamps
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        verbose_name = _("tracking link")
        verbose_name_plural = _("tracking links")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["link_code"]),
            models.Index(fields=["affiliate", "program"]),
        ]

    def __str__(self):
        return f"{self.affiliate.affiliate_code} - {self.link_code}"

    def save(self, *args, **kwargs):
        if not self.link_code:
            self.link_code = self.generate_unique_link_code()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_unique_link_code():
        """Generate a unique link code"""
        while True:
            code = secrets.token_urlsafe(12)[:12]
            if not Link.objects.filter(link_code=code).exists():
                return code

    def get_tracking_url(self):
        """Get the full tracking URL"""
        from django.urls import reverse

        return reverse("affiliate:track", kwargs={"link_code": self.link_code})

    def get_full_url(self):
        """Template-friendly alias for get_tracking_url."""
        return self.get_tracking_url()


class Click(models.Model):
    """
    Click Tracking
    Records when someone clicks an affiliate link
    """

    link = models.ForeignKey(
        Link, on_delete=models.CASCADE, related_name="clicks", verbose_name=_("link")
    )
    ip_address = models.GenericIPAddressField(verbose_name=_("IP address"))
    user_agent = models.TextField(blank=True, verbose_name=_("user agent"))
    referrer = models.URLField(blank=True, verbose_name=_("referrer"))
    session_id = models.CharField(max_length=255, db_index=True, verbose_name=_("session ID"))
    cookie_value = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("cookie value"),
        help_text=_("Unique cookie for attribution"),
    )

    # Timestamps
    clicked_at = models.DateTimeField(
        default=timezone.now, db_index=True, verbose_name=_("clicked at")
    )

    class Meta:
        verbose_name = _("click")
        verbose_name_plural = _("clicks")
        ordering = ["-clicked_at"]
        indexes = [
            models.Index(fields=["link", "clicked_at"]),
            models.Index(fields=["ip_address", "clicked_at"]),
            models.Index(fields=["session_id"]),
        ]

    def __str__(self):
        return f"Click on {self.link.link_code} at {self.clicked_at}"


class Commission(models.Model):
    """
    Commission Record
    Represents earnings from a conversion
    """

    STATUS_CHOICES = [
        ("pending", _("Pending")),
        ("approved", _("Approved")),
        ("rejected", _("Rejected")),
        ("paid", _("Paid")),
    ]

    affiliate = models.ForeignKey(
        Affiliate, on_delete=models.CASCADE, related_name="commissions", verbose_name=_("affiliate")
    )
    program = models.ForeignKey(
        Program, on_delete=models.CASCADE, related_name="commissions", verbose_name=_("program")
    )
    order = models.ForeignKey(
        "orders.Order",  # Reference to orders app
        on_delete=models.CASCADE,
        related_name="affiliate_commissions",
        verbose_name=_("order"),
    )
    click = models.ForeignKey(
        Click,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="commissions",
        verbose_name=_("click"),
    )

    # Commission Details
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name=_("amount")
    )
    currency = models.CharField(
        max_length=3,
        blank=True,
        verbose_name=_("currency"),
        help_text=_("Currency of the commission amount (from order)"),
    )
    amount_base = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("base currency amount"),
        help_text=_("Commission amount in store's base currency"),
    )
    base_currency = models.CharField(
        max_length=3,
        blank=True,
        verbose_name=_("base currency"),
        help_text=_("Store's base currency at time of commission"),
    )
    exchange_rate_used = models.DecimalField(
        max_digits=18,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name=_("exchange rate used"),
        help_text=_("Exchange rate used to compute amount_base"),
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name=_("status")
    )
    notes = models.TextField(blank=True, verbose_name=_("notes"))

    # Timestamps
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_("created at"))
    approved_at = models.DateTimeField(null=True, blank=True, verbose_name=_("approved at"))
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name=_("paid at"))

    class Meta:
        verbose_name = _("commission")
        verbose_name_plural = _("commissions")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["affiliate", "status"]),
            models.Index(fields=["program", "status"]),
            models.Index(fields=["status", "created_at"]),
        ]

    def __str__(self):
        return f"Commission {self.id} - {self.affiliate.affiliate_code} - ${self.amount}"


class Payout(models.Model):
    """
    Payout Record
    Represents payment to an affiliate for their commissions
    """

    STATUS_CHOICES = [
        ("pending", _("Pending")),
        ("processing", _("Processing")),
        ("completed", _("Completed")),
        ("failed", _("Failed")),
        ("cancelled", _("Cancelled")),
    ]

    affiliate = models.ForeignKey(
        Affiliate, on_delete=models.CASCADE, related_name="payouts", verbose_name=_("affiliate")
    )
    commissions = models.ManyToManyField(
        "Commission",
        related_name="payouts",
        verbose_name=_("commissions"),
        help_text=_("Commissions included in this payout"),
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name=_("amount")
    )
    method = models.CharField(max_length=50, verbose_name=_("payment method"))
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name=_("status")
    )
    reference = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("reference"),
        help_text=_("Payment reference/transaction ID"),
    )
    notes = models.TextField(blank=True, verbose_name=_("notes"))

    # Provider integration fields
    provider_account = models.ForeignKey(
        "payout_providers.PayoutProviderAccount",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payouts",
        verbose_name=_("provider account"),
        help_text=_("Payout provider account used to process this payment"),
    )
    provider_reference = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("provider reference"),
        help_text=_("External reference ID from the payout provider"),
    )
    provider_response = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("provider response"),
        help_text=_("Full API response from the payout provider"),
    )
    currency = models.CharField(
        max_length=3,
        default="USD",
        verbose_name=_("currency"),
        help_text=_("Currency code for this payout"),
    )
    amount_base = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("base currency amount"),
        help_text=_("Payout amount in store's base currency"),
    )
    base_currency = models.CharField(
        max_length=3,
        blank=True,
        verbose_name=_("base currency"),
        help_text=_("Store's base currency at time of payout"),
    )

    # Timestamps
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_("created at"))
    processed_at = models.DateTimeField(null=True, blank=True, verbose_name=_("processed at"))
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name=_("completed at"))

    class Meta:
        verbose_name = _("payout")
        verbose_name_plural = _("payouts")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["affiliate", "status"]),
            models.Index(fields=["status", "created_at"]),
        ]

    def __str__(self):
        return f"Payout {self.id} - {self.affiliate.affiliate_code} - ${self.amount}"

    def mark_as_processing(
        self, reference="", provider_account=None, provider_reference="", provider_response=None
    ):
        """
        Mark payout as processing.

        Args:
            reference: Internal reference/transaction ID
            provider_account: PayoutProviderAccount used for processing
            provider_reference: External reference from the provider
            provider_response: Full API response from the provider
        """
        self.status = "processing"
        self.processed_at = timezone.now()
        if reference:
            self.reference = reference
        if provider_account:
            self.provider_account = provider_account
        if provider_reference:
            self.provider_reference = provider_reference
        if provider_response:
            self.provider_response = provider_response
        self.save()

    def mark_as_completed(self, reference="", provider_reference="", provider_response=None):
        """
        Mark payout as completed and update commission statuses.

        Args:
            reference: Internal reference/transaction ID
            provider_reference: External reference from the provider
            provider_response: Full API response from the provider
        """
        self.status = "completed"
        self.completed_at = timezone.now()
        if reference:
            self.reference = reference
        if provider_reference:
            self.provider_reference = provider_reference
        if provider_response:
            self.provider_response = provider_response
        self.save()

        # Update all associated commissions to 'paid'
        self.commissions.filter(status="approved").update(status="paid", paid_at=timezone.now())

    def mark_as_failed(self, notes="", provider_response=None):
        """
        Mark payout as failed.

        Args:
            notes: Failure notes/reason
            provider_response: Full API response from the provider
        """
        self.status = "failed"
        if notes:
            self.notes = notes
        if provider_response:
            self.provider_response = provider_response
        self.save()

    def cancel(self, notes=""):
        """Cancel payout and revert commissions to approved"""
        self.status = "cancelled"
        if notes:
            self.notes = notes
        self.save()

        # Revert commissions back to 'approved' status
        self.commissions.filter(status="paid").update(status="approved", paid_at=None)

    @property
    def commission_count(self):
        """Count of commissions in this payout"""
        return self.commissions.count()

    @property
    def is_editable(self):
        """Check if payout can be edited"""
        return self.status in ["pending", "failed"]


class AffiliateSettings(models.Model):
    """
    Affiliate Portal Settings
    Singleton model for merchant customization of affiliate landing page content.
    """

    # Default feature content
    DEFAULT_FEATURES = [
        {
            "icon": "fas fa-dollar-sign",
            "title": "High Commissions",
            "description": "Earn generous commissions on every sale you refer. Both percentage and fixed rate options available.",
        },
        {
            "icon": "fas fa-clock",
            "title": "Cookie Duration",
            "description": "Extended cookie lifetime ensures you get credit for sales even if customers return later.",
        },
        {
            "icon": "fas fa-chart-bar",
            "title": "Real-time Tracking",
            "description": "Track clicks, conversions, and earnings in real-time with our comprehensive dashboard.",
        },
        {
            "icon": "fas fa-money-bill-wave",
            "title": "Fast Payouts",
            "description": "Request payouts anytime once you reach the minimum threshold. Multiple payment methods supported.",
        },
        {
            "icon": "fas fa-headset",
            "title": "Dedicated Support",
            "description": "Get help from our dedicated affiliate support team whenever you need assistance.",
        },
        {
            "icon": "fas fa-tools",
            "title": "Marketing Tools",
            "description": "Access banners, links, and promotional materials to help you succeed.",
        },
    ]

    # Default how-it-works steps
    DEFAULT_STEPS = [
        {
            "title": "Sign Up",
            "description": "Create your free affiliate account in just a few minutes.",
        },
        {
            "title": "Get Your Links",
            "description": "Choose programs and generate unique tracking links.",
        },
        {
            "title": "Promote",
            "description": "Share your links on your website, social media, or email.",
        },
        {"title": "Earn Money", "description": "Get paid commissions for every sale you generate!"},
    ]

    # Hero Section
    hero_title = models.CharField(
        max_length=200,
        default="Join Our Affiliate Program",
        verbose_name=_("hero title"),
        help_text=_("Main heading on the affiliate landing page"),
    )
    hero_subtitle = models.TextField(
        default="Earn commissions by promoting our products. Join thousands of successful affiliates!",
        verbose_name=_("hero subtitle"),
        help_text=_("Subheading text below the main title"),
    )

    # Features Section
    features_title = models.CharField(
        max_length=200,
        default="Why Join Our Affiliate Program?",
        verbose_name=_("features section title"),
        help_text=_("Title for the features section"),
    )
    features = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("features"),
        help_text=_("List of features. Each feature has: icon, title, description"),
    )

    # How It Works Section
    how_it_works_title = models.CharField(
        max_length=200,
        default="How It Works",
        verbose_name=_("how it works title"),
        help_text=_("Title for the how it works section"),
    )
    steps = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("steps"),
        help_text=_("List of steps. Each step has: title, description"),
    )

    # CTA Section
    cta_title = models.CharField(
        max_length=200,
        default="Ready to Start Earning?",
        verbose_name=_("CTA title"),
        help_text=_("Call-to-action section title"),
    )
    cta_description = models.TextField(
        default="Join our affiliate program today and start earning commissions!",
        verbose_name=_("CTA description"),
        help_text=_("Call-to-action section description"),
    )

    # Registration Settings
    registration_form = models.ForeignKey(
        "form_builder.Form",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="affiliate_settings",
        verbose_name=_("registration form"),
        help_text=_("Custom registration form. If blank, uses default fields."),
    )
    allow_guest_registration = models.BooleanField(
        default=True,
        verbose_name=_("allow guest registration"),
        help_text=_("Allow new users to register an account during affiliate signup"),
    )
    terms_url = models.URLField(
        blank=True,
        verbose_name=_("terms & conditions URL"),
        help_text=_("Link to affiliate terms & conditions page"),
    )
    require_approval = models.BooleanField(
        default=True,
        verbose_name=_("require approval"),
        help_text=_(
            "If enabled, new affiliates must be approved before they can access the dashboard"
        ),
    )
    welcome_message = models.TextField(
        blank=True,
        verbose_name=_("welcome message"),
        help_text=_("Message shown to newly registered affiliates"),
    )

    # Translations JSONField for all text content
    translations = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("translations"),
        help_text=_("Translations for content in different languages"),
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        verbose_name = _("affiliate settings")
        verbose_name_plural = _("affiliate settings")

    def __str__(self):
        return "Affiliate Portal Settings"

    def save(self, *args, **kwargs):
        # Ensure singleton behavior
        if not self.pk and AffiliateSettings.objects.exists():
            # Update the existing instance instead
            existing = AffiliateSettings.objects.first()
            self.pk = existing.pk

        # Populate default features if empty
        if not self.features:
            self.features = self.DEFAULT_FEATURES

        # Populate default steps if empty
        if not self.steps:
            self.steps = self.DEFAULT_STEPS

        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        """Get or create the singleton settings instance"""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings

    def get_translated_field(self, field_name, language_code=None):
        """
        Get a field value with translation fallback.

        Args:
            field_name: Name of the field to get
            language_code: Language code (e.g., 'es', 'fr'). If None, uses current language.

        Returns:
            Translated value if available, otherwise the default field value.
        """
        from django.utils.translation import get_language

        if language_code is None:
            language_code = get_language()

        # Check if translation exists
        if self.translations and language_code in self.translations:
            if field_name in self.translations[language_code]:
                return self.translations[language_code][field_name]

        # Fall back to default field value
        return getattr(self, field_name, "")


class AffiliateReportSettings(models.Model):
    """
    Singleton settings for affiliate monthly reports.

    Controls when and how monthly performance reports are sent to affiliates.
    Pattern: Similar to BlogSettings - singleton with pk=1
    """

    monthly_report_enabled = models.BooleanField(
        default=True,
        verbose_name=_("enable monthly reports"),
        help_text=_("Send monthly performance reports to affiliates"),
    )

    monthly_report_day = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(28)],
        verbose_name=_("report send day"),
        help_text=_("Day of month to send reports (1-28)"),
    )

    monthly_report_hour = models.PositiveIntegerField(
        default=9,
        validators=[MinValueValidator(0), MaxValueValidator(23)],
        verbose_name=_("report send hour"),
        help_text=_("Hour (UTC) to send reports (0-23)"),
    )

    include_top_orders_count = models.PositiveIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(20)],
        verbose_name=_("top orders count"),
        help_text=_("Number of top orders to include in report (1-20)"),
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        verbose_name = _("Affiliate Report Settings")
        verbose_name_plural = _("Affiliate Report Settings")

    def __str__(self):
        return f"Affiliate Report Settings (Monthly Reports: {'Enabled' if self.monthly_report_enabled else 'Disabled'})"

    @classmethod
    def get_settings(cls):
        """Get or create the singleton settings instance"""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings
