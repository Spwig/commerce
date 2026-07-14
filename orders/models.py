from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField

from custom_fields.mixins import CustomFieldsMixin
from design.models import DesignMixin

User = get_user_model()


class Order(CustomFieldsMixin, DesignMixin):
    """Order model with design customization"""

    STATUS_CHOICES = [
        ("pending", _("Pending")),
        ("processing", _("Processing")),
        ("shipped", _("Shipped")),
        ("delivered", _("Delivered")),
        ("cancelled", _("Cancelled")),
        ("refunded", _("Refunded")),
    ]

    # Order identification
    order_number = models.CharField(max_length=32, unique=True, db_index=True)
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="orders", null=True, blank=True
    )

    # Import tracking
    external_id = models.CharField(
        max_length=100,
        blank=True,
        db_index=True,
        help_text="Original order ID from source platform",
    )
    migration_job = models.ForeignKey(
        "migration.MigrationJob",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="imported_orders",
        help_text="Migration job that imported this order",
    )

    # Sales channel attribution
    SOURCE_CHOICES = [
        ("direct", _("Direct")),  # Typed URL or bookmark
        ("referral", _("Referral")),  # Affiliate program
        ("email", _("Email")),  # Email campaigns
        ("social", _("Social Media")),  # Social media platforms
        ("loyalty", _("Loyalty Program")),  # Loyalty program
        ("organic", _("Organic Search")),  # Search engines
        ("utm_tracked", _("UTM Campaign")),  # Custom UTM campaigns
        ("unknown", _("Unknown")),  # Default/undetermined
    ]

    # Order status and tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        default="unknown",
        db_index=True,
        help_text="How the customer came to make this purchase",
    )

    # Email attribution tracking (for campaign ROI)
    attributed_email = models.ForeignKey(
        "email_system.EmailOutbox",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="attributed_orders",
        db_index=True,
        help_text="Email campaign that led to this order (7-day attribution window)",
    )

    tracking_number = models.CharField(max_length=100, blank=True)

    # Customer information
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)

    # Shipping address (snapshot data at time of order)
    shipping_address_ref = models.ForeignKey(
        "Address",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders_as_shipping",
        help_text="Reference to saved address used for shipping (for audit trail)",
    )
    shipping_name = models.CharField(max_length=200)
    shipping_address1 = models.CharField(max_length=200)
    shipping_address2 = models.CharField(max_length=200, blank=True)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_postal_code = models.CharField(max_length=20)
    shipping_country = models.CharField(max_length=100)
    shipping_phone = models.CharField(max_length=20, blank=True)

    # Pickup information (for local pickup orders)
    pickup_location = models.ForeignKey(
        "shipping.Location",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pickup_orders",
        verbose_name="Pickup Location",
        help_text="Location where customer will pick up this order",
    )
    pickup_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Pickup Date",
        help_text="Date and time when customer will pick up the order",
    )

    # Billing address (snapshot data at time of order)
    billing_same_as_shipping = models.BooleanField(default=True)
    billing_address_ref = models.ForeignKey(
        "Address",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders_as_billing",
        help_text="Reference to saved address used for billing (for audit trail)",
    )
    billing_name = models.CharField(max_length=200, blank=True)
    billing_address1 = models.CharField(max_length=200, blank=True)
    billing_address2 = models.CharField(max_length=200, blank=True)
    billing_city = models.CharField(max_length=100, blank=True)
    billing_state = models.CharField(max_length=100, blank=True)
    billing_postal_code = models.CharField(max_length=20, blank=True)
    billing_country = models.CharField(max_length=100, blank=True)
    billing_phone = models.CharField(max_length=20, blank=True)

    # Order totals
    subtotal = MoneyField(max_digits=10, decimal_places=2, default_currency="USD")
    tax_amount = MoneyField(max_digits=10, decimal_places=2, default_currency="USD", default=0)
    shipping_cost = MoneyField(max_digits=10, decimal_places=2, default_currency="USD", default=0)
    discount_amount = MoneyField(max_digits=10, decimal_places=2, default_currency="USD", default=0)
    gift_card_discount = MoneyField(
        max_digits=10, decimal_places=2, default_currency="USD", default=0
    )
    total_amount = MoneyField(max_digits=10, decimal_places=2, default_currency="USD")

    # Payment tracking
    PAYMENT_STATUS_CHOICES = [
        ("unpaid", _("Unpaid")),
        ("partially_paid", _("Partially Paid")),
        ("paid", _("Paid")),
        ("refunded", _("Refunded")),
        ("partially_refunded", _("Partially Refunded")),
        ("failed", _("Failed")),
        ("pending", _("Pending")),
    ]

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="unpaid",
        db_index=True,
        verbose_name="payment status",
        help_text="Current payment status of this order",
    )

    payment_provider = models.ForeignKey(
        "payment_providers.PaymentProviderAccount",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
        verbose_name="payment provider",
        help_text="Payment provider account used for this order",
    )

    payment_method_type = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="payment method type",
        help_text="Type of payment method used (credit_card, bank_transfer, etc.)",
    )

    payment_method_last4 = models.CharField(
        max_length=4,
        blank=True,
        verbose_name="payment method last 4 digits",
        help_text="Last 4 digits of card/account for display",
    )

    paid_at = models.DateTimeField(
        null=True, blank=True, verbose_name="paid at", help_text="When payment was completed"
    )

    amount_paid = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency="USD",
        default=0,
        verbose_name="amount paid",
        help_text="Total amount paid (for partial payment tracking)",
    )

    amount_refunded = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency="USD",
        default=0,
        verbose_name="amount refunded",
        help_text="Total amount refunded",
    )

    # Email Enhancement Fields
    estimated_delivery_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="estimated delivery date",
        help_text="Estimated date when order will be delivered (calculated from shipping method + carrier)",
    )

    delivered_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="delivered at",
        help_text="Actual delivery timestamp (set when order status changes to 'delivered')",
    )

    carrier = models.ForeignKey(
        "shipping.CarrierPreset",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
        verbose_name="shipping carrier",
        help_text="Carrier used for shipment (links to shipping app for logo, tracking URL template)",
    )

    delay_reason = models.TextField(
        blank=True,
        verbose_name="delay reason",
        help_text="Explanation for order delay (displayed in delay notification emails)",
    )

    # Exchange Rate Audit Trail (for multi-currency orders)
    customer_currency = models.CharField(
        max_length=3,
        blank=True,
        null=True,
        help_text="Currency code selected by customer at checkout",
    )
    exchange_rate_used = models.DecimalField(
        max_digits=18,
        decimal_places=6,
        blank=True,
        null=True,
        help_text="Exchange rate applied at time of order (if multi-currency)",
    )
    exchange_rate_provider = models.CharField(
        max_length=255, blank=True, help_text="Name of exchange rate provider used for conversion"
    )
    base_currency = models.CharField(
        max_length=3, blank=True, default="USD", help_text="Store's base currency at time of order"
    )

    # FX policy tracking
    FX_POLICY_CHOICES = [
        ("none", _("No Conversion")),
        ("spot", _("Spot Rate at Capture")),
        ("daily", _("Daily Rate")),
        ("psp", _("Payment Service Provider")),
    ]
    fx_policy = models.CharField(
        max_length=10,
        choices=FX_POLICY_CHOICES,
        default="none",
        verbose_name="FX policy",
        help_text="FX rate policy used for this order's currency conversion",
    )

    # Base-currency equivalents for reporting
    # These store the merchant's base currency amounts, computed using exchange_rate_used
    # For single-currency orders, these equal the customer-facing amounts
    subtotal_base = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="subtotal (base currency)",
        help_text="Subtotal in store's base currency",
    )
    tax_amount_base = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="tax amount (base currency)",
        help_text="Tax amount in store's base currency",
    )
    shipping_cost_base = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="shipping cost (base currency)",
        help_text="Shipping cost in store's base currency",
    )
    discount_amount_base = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="discount amount (base currency)",
        help_text="Discount amount in store's base currency",
    )
    gift_card_discount_base = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="gift card discount (base currency)",
        help_text="Gift card discount in store's base currency",
    )
    total_amount_base = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        db_index=True,
        verbose_name="total amount (base currency)",
        help_text="Total amount in store's base currency",
    )
    amount_paid_base = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="amount paid (base currency)",
        help_text="Amount paid in store's base currency",
    )
    amount_refunded_base = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="amount refunded (base currency)",
        help_text="Amount refunded in store's base currency",
    )

    # Order page customization
    ORDER_PAGE_LAYOUTS = [
        ("standard", _("Standard Layout")),
        ("detailed", _("Detailed View")),
        ("minimal", _("Minimal View")),
        ("timeline", _("Timeline View")),
    ]

    order_page_layout = models.CharField(
        max_length=20,
        choices=ORDER_PAGE_LAYOUTS,
        default="standard",
        help_text="How order details are displayed",
    )

    # Display preferences
    show_order_progress = models.BooleanField(default=True)
    show_shipping_updates = models.BooleanField(default=True)
    show_item_images = models.BooleanField(default=True)

    # Notes and special instructions
    notes = models.TextField(blank=True)
    special_instructions = models.TextField(blank=True)

    # Metadata (e.g., marketplace purchase context)
    metadata = models.JSONField(
        default=dict, blank=True, help_text="Extra metadata (e.g., marketplace purchase context)"
    )

    # Sandbox / Test order flag
    is_test_order = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="test order",
        help_text="Whether this order was placed in sandbox/development mode",
    )

    # POS / Sales Channel
    CHANNEL_CHOICES = [
        ("web", _("Online Store")),
        ("pos", _("Point of Sale")),
    ]
    channel = models.CharField(
        max_length=20,
        choices=CHANNEL_CHOICES,
        default="web",
        db_index=True,
        help_text="Channel where this order was placed",
    )
    pos_terminal = models.ForeignKey(
        "pos_app.POSTerminal",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="orders",
        help_text="Terminal where this order was processed (POS orders only)",
    )
    cashier = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="pos_orders",
        help_text="Staff member who processed this order (POS orders only)",
    )

    # Digital receipt tracking
    receipt_email_sent_at = models.DateTimeField(
        null=True, blank=True, help_text="When digital receipt was sent via email"
    )
    receipt_sms_sent_at = models.DateTimeField(
        null=True, blank=True, help_text="When digital receipt was sent via SMS/WhatsApp"
    )
    receipt_token = models.CharField(
        max_length=64,
        blank=True,
        db_index=True,
        help_text="Unique token for viewing receipt without auth",
    )

    # Language the customer was browsing in at checkout time
    language = models.CharField(
        max_length=10,
        default="en",
        blank=True,
        verbose_name=_("Language"),
        help_text=_("Language the customer was browsing in when placing the order"),
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        indexes = [
            models.Index(fields=["order_number"]),
            models.Index(fields=["user", "-created_at"]),
            models.Index(fields=["status"]),
            models.Index(fields=["source"]),
            models.Index(fields=["source", "-created_at"]),
        ]

    def compute_base_amounts(self):
        """
        Compute base-currency equivalents from customer-currency amounts.
        Called at order creation time. Uses the captured exchange_rate_used.
        For single-currency orders, copies amounts directly.

        Rate direction: exchange_rate_used is base->customer
        (e.g., 1 EUR = 1.78 NZD), so base = customer_amount / rate.
        """
        if not self.customer_currency or self.customer_currency == self.base_currency:
            # Single-currency order - base equals customer amounts
            self.subtotal_base = (
                self.subtotal.amount
                if hasattr(self.subtotal, "amount")
                else Decimal(str(self.subtotal or 0))
            )
            self.tax_amount_base = (
                self.tax_amount.amount
                if hasattr(self.tax_amount, "amount")
                else Decimal(str(self.tax_amount or 0))
            )
            self.shipping_cost_base = (
                self.shipping_cost.amount
                if hasattr(self.shipping_cost, "amount")
                else Decimal(str(self.shipping_cost or 0))
            )
            self.discount_amount_base = (
                self.discount_amount.amount
                if hasattr(self.discount_amount, "amount")
                else Decimal(str(self.discount_amount or 0))
            )
            self.gift_card_discount_base = (
                self.gift_card_discount.amount
                if hasattr(self.gift_card_discount, "amount")
                else Decimal(str(self.gift_card_discount or 0))
            )
            self.total_amount_base = (
                self.total_amount.amount
                if hasattr(self.total_amount, "amount")
                else Decimal(str(self.total_amount or 0))
            )
            self.amount_paid_base = (
                self.amount_paid.amount
                if hasattr(self.amount_paid, "amount")
                else Decimal(str(self.amount_paid or 0))
            )
            self.amount_refunded_base = (
                self.amount_refunded.amount
                if hasattr(self.amount_refunded, "amount")
                else Decimal(str(self.amount_refunded or 0))
            )
        else:
            if not self.exchange_rate_used:
                # Cross-currency order with no captured rate -- leave base amounts
                # as NULL so analytics Coalesce fallback handles them and the order
                # is clearly flagged for manual rate entry.
                return
            rate = self.exchange_rate_used
            if rate == 0:
                return

            def _to_base(money_val):
                amt = (
                    money_val.amount
                    if hasattr(money_val, "amount")
                    else Decimal(str(money_val or 0))
                )
                return (amt / rate).quantize(Decimal("0.01"))

            self.subtotal_base = _to_base(self.subtotal)
            self.tax_amount_base = _to_base(self.tax_amount)
            self.shipping_cost_base = _to_base(self.shipping_cost)
            self.discount_amount_base = _to_base(self.discount_amount)
            self.gift_card_discount_base = _to_base(self.gift_card_discount)
            self.total_amount_base = _to_base(self.total_amount)
            self.amount_paid_base = _to_base(self.amount_paid)
            self.amount_refunded_base = _to_base(self.amount_refunded)

    def __str__(self):
        return f"Order #{self.order_number}"

    @property
    def top_level_items(self):
        """Return only top-level items (exclude bundle/configurable components)."""
        return self.items.filter(parent_bundle__isnull=True)

    @property
    def total_item_quantity(self):
        """Calculate total quantity of top-level items in the order."""
        from django.db.models import Sum

        return (
            self.items.filter(parent_bundle__isnull=True).aggregate(total=Sum("quantity"))["total"]
            or 0
        )

    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate order number
            import uuid

            self.order_number = str(uuid.uuid4()).replace("-", "").upper()[:12]
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """Individual items in an order"""

    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey("catalog.Product", on_delete=models.PROTECT)
    variant = models.ForeignKey(
        "catalog.ProductVariant", on_delete=models.PROTECT, null=True, blank=True
    )

    # Item details at time of order
    product_name = models.CharField(max_length=255)
    variant_name = models.CharField(max_length=100, blank=True)
    sku = models.CharField(max_length=100)

    quantity = models.PositiveIntegerField()
    unit_price = MoneyField(max_digits=10, decimal_places=2, default_currency="USD")
    total_price = MoneyField(max_digits=10, decimal_places=2, default_currency="USD")

    # Base-currency equivalents for reporting
    unit_price_base = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="unit price (base currency)",
        help_text="Unit price in store's base currency",
    )
    total_price_base = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="total price (base currency)",
        help_text="Total price in store's base currency",
    )

    # Item-level discounts
    base_price = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency="USD",
        null=True,
        blank=True,
        help_text="Original product price before any discount",
    )
    discount_type = models.CharField(
        max_length=20,
        choices=[
            ("none", _("No Discount")),
            ("percentage", _("Percentage")),
            ("fixed", _("Fixed Amount")),
        ],
        default="none",
        help_text="Type of discount applied to this item",
    )
    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Discount value: percentage (0-100) or fixed amount",
    )
    discount_reason = models.CharField(
        max_length=200, blank=True, help_text="Optional reason for the discount"
    )
    exclude_from_vouchers = models.BooleanField(
        default=False, help_text="Exclude this item from order-level voucher discounts"
    )

    # Product customizations at time of order
    customizations = models.JSONField(default=dict, blank=True)

    # Bundle tracking
    parent_bundle = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="component_items",
        help_text="If this is a bundle component, reference to bundle OrderItem",
    )

    # Multi-location inventory tracking
    warehouse = models.ForeignKey(
        "catalog.Warehouse",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="order_items",
        help_text="Warehouse from which this item will be/was fulfilled",
    )
    stock_allocated = models.BooleanField(
        default=False, help_text="Whether stock has been allocated for this item"
    )
    stock_fulfilled = models.BooleanField(
        default=False, help_text="Whether stock has been fulfilled (shipped) for this item"
    )

    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")
        indexes = [
            models.Index(fields=["order"]),
            models.Index(fields=["product"]),
        ]

    def __str__(self):
        variant_info = f" - {self.variant_name}" if self.variant_name else ""
        return f"{self.quantity}x {self.product_name}{variant_info}"

    def has_discount(self):
        """Check if this item has any discount applied (explicit or implicit)"""
        # Check for explicit discount
        if self.discount_type != "none" and self.discount_value > 0:
            return True

        # Check for implicit discount (manually reduced price)
        return bool(self.base_price and self.unit_price.amount < self.base_price.amount)

    def get_discount_amount(self):
        """Calculate the discount amount in money per unit"""
        from djmoney.money import Money

        if not self.has_discount() or not self.base_price:
            return Money(0, self.unit_price.currency)

        if self.discount_type == "percentage":
            discount_amount = self.base_price * (self.discount_value / 100)
            return Money(discount_amount.amount, self.base_price.currency)
        elif self.discount_type == "fixed":
            return Money(self.discount_value, self.base_price.currency)
        else:
            # Implicit discount: calculate difference between base_price and unit_price
            discount_amount = self.base_price.amount - self.unit_price.amount
            return Money(discount_amount, self.unit_price.currency)

        return Money(0, self.unit_price.currency)

    def get_discount_percentage(self):
        """Calculate discount as a percentage"""
        if not self.has_discount() or not self.base_price or self.base_price.amount == 0:
            return 0

        if self.discount_type == "percentage":
            return float(self.discount_value)
        elif self.discount_type == "fixed":
            from decimal import Decimal

            discount_pct = (
                Decimal(str(self.discount_value)) / Decimal(str(self.base_price.amount))
            ) * 100
            return round(float(discount_pct), 2)
        else:
            # Implicit discount: calculate percentage from base_price and unit_price
            from decimal import Decimal

            discount_amount = self.base_price.amount - self.unit_price.amount
            if discount_amount > 0:
                discount_pct = (
                    Decimal(str(discount_amount)) / Decimal(str(self.base_price.amount))
                ) * 100
                return round(float(discount_pct), 2)

        return 0

    def get_final_unit_price(self):
        """Calculate final unit price after discount"""
        if not self.has_discount() or not self.base_price:
            return self.unit_price

        discount_amount = self.get_discount_amount()
        return self.base_price - discount_amount


class Address(models.Model):
    """Reusable customer addresses with versioning for audit trail"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")

    ADDRESS_TYPES = [
        ("shipping", _("Shipping")),
        ("billing", _("Billing")),
        ("both", _("Both")),
    ]

    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPES, default="both")
    name = models.CharField(max_length=200)
    company = models.CharField(max_length=200, blank=True)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)

    is_default = models.BooleanField(default=False)

    # Address versioning for audit trail
    original_address = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="versions",
        help_text="Original address if this is an edited version",
    )
    is_active = models.BooleanField(
        default=True, db_index=True, help_text="Whether this address version is currently active"
    )
    edited_at = models.DateTimeField(
        null=True, blank=True, help_text="When this address was superseded by a new version"
    )
    version = models.PositiveIntegerField(default=1, help_text="Version number of this address")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")
        indexes = [
            models.Index(fields=["user", "is_default"]),
            models.Index(fields=["user", "is_active"]),
            models.Index(fields=["original_address", "version"]),
        ]

    def __str__(self):
        version_str = f" (v{self.version})" if self.version > 1 or not self.is_active else ""
        active_str = "" if self.is_active else " [Inactive]"
        return f"{self.name} - {self.city}, {self.state}{version_str}{active_str}"

    def save(self, *args, **kwargs):
        # Ensure only one default address per type per user (among active addresses)
        if self.is_default and self.is_active:
            Address.objects.filter(
                user=self.user, address_type=self.address_type, is_default=True, is_active=True
            ).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)

    def get_version_history(self):
        """Get all versions of this address including this one"""
        if self.original_address:
            # This is a version, get root and all versions
            root = self.original_address
            return Address.objects.filter(Q(pk=root.pk) | Q(original_address=root)).order_by(
                "version"
            )
        else:
            # This is the root, get all versions
            return Address.objects.filter(Q(pk=self.pk) | Q(original_address=self)).order_by(
                "version"
            )

    def get_latest_version(self):
        """Get the latest active version of this address"""
        return self.get_version_history().filter(is_active=True).last()

    def get_order_count(self):
        """Get count of orders that used this address"""
        from django.db.models import Q

        return Order.objects.filter(
            Q(shipping_address_ref=self) | Q(billing_address_ref=self)
        ).count()

    def is_used_in_orders(self):
        """Check if this address has been used in any orders"""
        return self.get_order_count() > 0


class OrderNote(models.Model):
    """Notes/comments on orders"""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_notes")
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="order_notes"
    )

    note = models.TextField(help_text="Note content")
    is_customer_note = models.BooleanField(
        default=False, help_text="Whether this note is visible to the customer"
    )
    is_read = models.BooleanField(
        default=False, help_text="Whether merchant has read this note (for customer messages)"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Order Note")
        verbose_name_plural = _("Order Notes")
        indexes = [
            models.Index(fields=["order", "-created_at"]),
        ]

    def __str__(self):
        note_type = "Customer" if self.is_customer_note else "Private"
        author_name = self.author.get_full_name() if self.author else "System"
        return f"{note_type} note by {author_name} on Order #{self.order.order_number}"


class Refund(models.Model):
    """
    Order refund tracking - supports full and partial refunds.
    Tracks item-level refunds, shipping refunds, and tax adjustments.
    """

    REFUND_TYPE_CHOICES = [
        ("full", _("Full Refund")),
        ("partial", _("Partial Refund")),
    ]

    REFUND_REASON_CHOICES = [
        ("customer_request", _("Customer Request")),
        ("damaged", _("Damaged Product")),
        ("wrong_item", _("Wrong Item Sent")),
        ("defective", _("Defective Product")),
        ("not_as_described", _("Not as Described")),
        ("duplicate_order", _("Duplicate Order")),
        ("other", _("Other")),
    ]

    STATUS_CHOICES = [
        ("requested", _("Requested")),
        ("approved", _("Approved")),
        ("processing", _("Processing")),
        ("completed", _("Completed")),
        ("failed", _("Failed")),
    ]

    # Relationships
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="refunds", help_text="Order being refunded"
    )
    processed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="processed_refunds",
        help_text="Staff member who processed the refund",
    )
    pos_terminal = models.ForeignKey(
        "pos_app.POSTerminal",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="refunds",
        help_text="POS terminal where this refund was processed",
    )

    # Refund details
    refund_type = models.CharField(
        max_length=10,
        choices=REFUND_TYPE_CHOICES,
        default="full",
        help_text="Whether this is a full or partial refund",
    )
    reason = models.CharField(
        max_length=30, choices=REFUND_REASON_CHOICES, help_text="Reason for the refund"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="requested",
        help_text="Current status of the refund",
    )

    # Refund method (dynamic — no hardcoded choices, stores method key)
    refund_method = models.CharField(
        max_length=50,
        blank=True,
        help_text="Payment method used for the refund (e.g. cash, card, terminal_card, gift_card, or provider slug)",
    )
    refund_method_display = models.CharField(
        max_length=100, blank=True, help_text="Human-readable name of the refund method"
    )

    # Refund amounts
    total_amount = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency="USD",
        help_text="Total amount to be refunded",
    )
    shipping_refund_amount = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency="USD",
        default=0,
        null=True,
        blank=True,
        help_text="Shipping cost being refunded",
    )
    tax_refund_amount = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency="USD",
        default=0,
        null=True,
        blank=True,
        help_text="Tax amount being refunded",
    )

    # Base-currency equivalents for reporting
    total_amount_base = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="total amount (base currency)",
        help_text="Refund total in store's base currency",
    )
    shipping_refund_amount_base = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="shipping refund (base currency)",
        help_text="Shipping refund in store's base currency",
    )
    tax_refund_amount_base = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="tax refund (base currency)",
        help_text="Tax refund in store's base currency",
    )

    # Item-level refund details stored as JSON
    # Format: [{"order_item_id": 123, "quantity": 2, "amount": "29.99"}, ...]
    items_json = models.JSONField(
        default=list,
        blank=True,
        help_text="Item-level refund details (order_item_id, quantity, amount)",
    )

    # Notes
    customer_notes = models.TextField(
        blank=True, help_text="Customer-facing notes about the refund"
    )
    staff_notes = models.TextField(blank=True, help_text="Internal staff notes")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the refund was requested")
    approved_at = models.DateTimeField(
        null=True, blank=True, help_text="When the refund was approved"
    )
    processed_at = models.DateTimeField(
        null=True, blank=True, help_text="When the refund processing started"
    )
    completed_at = models.DateTimeField(
        null=True, blank=True, help_text="When the refund was completed"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Refund")
        verbose_name_plural = _("Refunds")
        indexes = [
            models.Index(fields=["order", "-created_at"]),
            models.Index(fields=["status"]),
            models.Index(fields=["reason"]),
            models.Index(fields=["-created_at"]),
            models.Index(fields=["pos_terminal", "-processed_at"]),
        ]

    def compute_base_amounts(self):
        """
        Compute base-currency equivalents using the parent order's locked exchange rate.
        Must be called after the refund is created when the order is multi-currency.
        """
        order = self.order
        if not order.customer_currency or order.customer_currency == order.base_currency:
            # Single-currency - copy amounts directly
            self.total_amount_base = (
                self.total_amount.amount
                if hasattr(self.total_amount, "amount")
                else Decimal(str(self.total_amount or 0))
            )
            shipping = self.shipping_refund_amount
            self.shipping_refund_amount_base = (
                shipping.amount if hasattr(shipping, "amount") else Decimal(str(shipping or 0))
            )
            tax = self.tax_refund_amount
            self.tax_refund_amount_base = (
                tax.amount if hasattr(tax, "amount") else Decimal(str(tax or 0))
            )
        else:
            if not order.exchange_rate_used or order.exchange_rate_used == 0:
                # Parent order has no captured rate -- leave base amounts NULL
                return
            rate = order.exchange_rate_used

            def _to_base(money_val):
                amt = (
                    money_val.amount
                    if hasattr(money_val, "amount")
                    else Decimal(str(money_val or 0))
                )
                return (amt / rate).quantize(Decimal("0.01"))

            self.total_amount_base = _to_base(self.total_amount)
            self.shipping_refund_amount_base = _to_base(self.shipping_refund_amount)
            self.tax_refund_amount_base = _to_base(self.tax_refund_amount)

    def __str__(self):
        return f"Refund for Order #{self.order.order_number} - {self.get_status_display()}"

    def approve(self, user=None):
        """Approve the refund"""
        self.status = "approved"
        self.approved_at = timezone.now()
        if user:
            self.processed_by = user
        self.save()

    def start_processing(self):
        """Mark refund as processing"""
        self.status = "processing"
        self.processed_at = timezone.now()
        self.save()

    def complete(self):
        """Mark refund as completed"""
        self.status = "completed"
        self.completed_at = timezone.now()
        self.save()

    def fail(self, notes=""):
        """Mark refund as failed"""
        self.status = "failed"
        if notes:
            self.staff_notes += f"\nFailed: {notes}"
        self.save()

    def calculate_items_total(self):
        """Calculate total amount from refunded items"""
        if not self.items_json:
            return Decimal("0.00")
        return sum(Decimal(str(item.get("amount", 0))) for item in self.items_json)


class ReturnRequest(models.Model):
    """
    Customer return request tracking - Phase 7: Returns & RMA Workflow.
    Handles the physical return of products separately from financial refund processing.

    Workflow:
    1. Customer requests return (pending)
    2. Merchant approves/rejects (approved/rejected)
    3. Return label sent to customer (label_sent)
    4. Customer ships items (in_transit)
    5. Merchant receives return (received)
    6. Merchant inspects items (inspected)
    7. Refund processed and return completed (completed)
    """

    RETURN_REASON_CHOICES = [
        ("defective", _("Defective Product")),
        ("wrong_item", _("Wrong Item Received")),
        ("not_as_described", _("Not as Described")),
        ("changed_mind", _("Changed Mind")),
        ("sizing", _("Wrong Size/Fit")),
        ("damaged_shipping", _("Damaged in Shipping")),
        ("other", _("Other")),
    ]

    STATUS_CHOICES = [
        ("pending", _("Pending Approval")),
        ("approved", _("Approved")),
        ("rejected", _("Rejected")),
        ("label_sent", _("Return Label Sent")),
        ("in_transit", _("In Transit to Warehouse")),
        ("received", _("Received at Warehouse")),
        ("inspected", _("Inspected")),
        ("completed", _("Completed")),
        ("cancelled", _("Cancelled")),
    ]

    # Relationships
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="return_requests",
        help_text="Order being returned",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="return_requests",
        help_text="Customer requesting the return",
    )
    return_shipment = models.ForeignKey(
        "shipping.Shipment",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="return_for_shipment",
        help_text="Return shipment tracking (customer to warehouse)",
    )
    refund = models.OneToOneField(
        Refund,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="return_request",
        help_text="Associated refund (created after inspection)",
    )

    # Return details
    reason = models.CharField(
        max_length=30, choices=RETURN_REASON_CHOICES, help_text="Primary reason for return"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        help_text="Current status in return workflow",
    )

    # Items being returned - JSON format:
    # [{"order_item_id": 123, "quantity": 2, "reason": "defective", "notes": "Button broken"}, ...]
    items_json = models.JSONField(
        default=list, help_text="Items being returned with quantities and item-specific reasons"
    )

    # Return label tracking
    return_label_generated = models.BooleanField(
        default=False, help_text="Whether return shipping label has been generated"
    )
    return_tracking_number = models.CharField(
        max_length=100, blank=True, help_text="Tracking number for return shipment"
    )
    return_label_url = models.URLField(
        blank=True, help_text="URL to download return shipping label PDF"
    )

    # Notes and communication
    customer_notes = models.TextField(blank=True, help_text="Customer explanation for the return")
    merchant_notes = models.TextField(
        blank=True, help_text="Internal merchant notes about the return"
    )
    rejection_reason = models.TextField(
        blank=True, help_text="Reason for rejecting the return request"
    )
    inspection_notes = models.TextField(
        blank=True, help_text="Notes from inspection after receiving items"
    )

    # Inspection results
    CONDITION_CHOICES = [
        ("excellent", _("Excellent - Like New")),
        ("good", _("Good - Minor Wear")),
        ("acceptable", _("Acceptable - Noticeable Wear")),
        ("damaged", _("Damaged - Not Resellable")),
        ("defective", _("Defective - As Described")),
    ]

    items_condition = models.CharField(
        max_length=20,
        choices=CONDITION_CHOICES,
        blank=True,
        help_text="Overall condition of returned items after inspection",
    )

    restocking_fee = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency="USD",
        default=0,
        null=True,
        blank=True,
        help_text="Restocking fee to deduct from refund (if applicable)",
    )

    # Processed by tracking
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_returns",
        help_text="Staff member who approved the return",
    )
    inspected_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="inspected_returns",
        help_text="Staff member who inspected the return",
    )

    # Timestamps for workflow tracking
    requested_at = models.DateTimeField(
        auto_now_add=True, help_text="When customer requested the return"
    )
    approved_at = models.DateTimeField(
        null=True, blank=True, help_text="When return was approved by merchant"
    )
    rejected_at = models.DateTimeField(
        null=True, blank=True, help_text="When return was rejected by merchant"
    )
    label_sent_at = models.DateTimeField(
        null=True, blank=True, help_text="When return label was sent to customer"
    )
    received_at = models.DateTimeField(
        null=True, blank=True, help_text="When items were received at warehouse"
    )
    inspected_at = models.DateTimeField(
        null=True, blank=True, help_text="When items were inspected"
    )
    completed_at = models.DateTimeField(
        null=True, blank=True, help_text="When return process was completed"
    )
    updated_at = models.DateTimeField(auto_now=True, help_text="Last update to this return request")

    class Meta:
        ordering = ["-requested_at"]
        indexes = [
            models.Index(fields=["order", "-requested_at"]),
            models.Index(fields=["user", "-requested_at"]),
            models.Index(fields=["status"]),
            models.Index(fields=["reason"]),
            models.Index(fields=["-requested_at"]),
        ]
        verbose_name = _("Return Request")
        verbose_name_plural = _("Return Requests")

    def __str__(self):
        return f"Return Request for Order #{self.order.order_number} - {self.get_status_display()}"

    def approve(self, user=None):
        """
        Approve the return request and prepare for return label generation.

        Args:
            user: Staff member approving the return
        """
        self.status = "approved"
        self.approved_at = timezone.now()
        if user:
            self.approved_by = user
        self.save()

        from django.db import transaction

        from orders.emails import send_return_approved_notification

        transaction.on_commit(lambda: send_return_approved_notification(self))

    def reject(self, reason, user=None):
        """
        Reject the return request with explanation.

        Args:
            reason: Explanation for rejection
            user: Staff member rejecting the return
        """
        self.status = "rejected"
        self.rejected_at = timezone.now()
        self.rejection_reason = reason
        if user:
            self.approved_by = user  # Track who made the decision
        self.save()

        from django.db import transaction

        from orders.emails import send_return_rejected_notification

        transaction.on_commit(lambda: send_return_rejected_notification(self))

    def mark_label_sent(self):
        """Mark that return label has been sent to customer"""
        self.status = "label_sent"
        self.label_sent_at = timezone.now()
        self.save()

    def mark_in_transit(self, tracking_number=None):
        """
        Mark return as in transit (customer has shipped items back).

        Args:
            tracking_number: Optional tracking number for return shipment
        """
        self.status = "in_transit"
        if tracking_number:
            self.return_tracking_number = tracking_number
        self.save()

    def mark_received(self, user=None):
        """
        Mark items as received at warehouse.

        Args:
            user: Staff member receiving the items
        """
        self.status = "received"
        self.received_at = timezone.now()
        self.save()

        from django.db import transaction

        from orders.emails import (
            send_inspection_reminder_to_staff,
            send_return_received_notification,
        )

        transaction.on_commit(lambda: send_return_received_notification(self))
        transaction.on_commit(lambda: send_inspection_reminder_to_staff(self))

    def mark_inspected(self, condition, inspection_notes="", restocking_fee=None, user=None):
        """
        Mark items as inspected with condition assessment.

        Args:
            condition: Condition of items (excellent, good, acceptable, damaged, defective)
            inspection_notes: Notes from inspection
            restocking_fee: Optional restocking fee to deduct
            user: Staff member who inspected the items
        """
        self.status = "inspected"
        self.inspected_at = timezone.now()
        self.items_condition = condition
        self.inspection_notes = inspection_notes
        if restocking_fee is not None:
            self.restocking_fee = restocking_fee
        if user:
            self.inspected_by = user
        self.save()

        # Refund notification fires from process_refund() after the Refund object is created

    def process_refund(self, refund_data):
        """
        Process refund after inspection and link to this return request.

        Args:
            refund_data: Dictionary with refund details:
                - total_amount: Total refund amount
                - shipping_refund_amount: Shipping refund
                - tax_refund_amount: Tax refund
                - items_json: Item-level refund details
                - customer_notes: Customer-facing notes
                - staff_notes: Internal notes

        Returns:
            Refund: Created refund instance
        """
        # Create refund
        refund = Refund.objects.create(
            order=self.order,
            refund_type="partial" if len(self.items_json) < self.order.items.count() else "full",
            reason=self.reason
            if self.reason in dict(Refund.REFUND_REASON_CHOICES)
            else "customer_request",
            status="approved",  # Auto-approve since return was already inspected
            total_amount=refund_data["total_amount"],
            shipping_refund_amount=refund_data.get("shipping_refund_amount", 0),
            tax_refund_amount=refund_data.get("tax_refund_amount", 0),
            items_json=refund_data.get("items_json", self.items_json),
            customer_notes=refund_data.get("customer_notes", "Refund processed for return request"),
            staff_notes=refund_data.get(
                "staff_notes", f"Return request inspection: {self.items_condition}"
            ),
            approved_at=timezone.now(),
        )
        refund.compute_base_amounts()
        refund.save(
            update_fields=[
                "total_amount_base",
                "shipping_refund_amount_base",
                "tax_refund_amount_base",
            ]
        )

        # Link refund to this return request
        self.refund = refund
        self.save()

        from django.db import transaction

        from orders.emails import send_refund_processed_notification

        transaction.on_commit(lambda: send_refund_processed_notification(self))

        return refund

    def complete(self):
        """Mark return request as completed"""
        self.status = "completed"
        self.completed_at = timezone.now()
        self.save()

    def cancel(self):
        """Cancel the return request"""
        self.status = "cancelled"
        self.save()

    def get_items_summary(self):
        """Get human-readable summary of items being returned"""
        if not self.items_json:
            return "No items specified"

        item_count = len(self.items_json)
        total_quantity = sum(item.get("quantity", 0) for item in self.items_json)

        return f"{item_count} item(s), {total_quantity} unit(s)"

    def calculate_refund_amount(self):
        """
        Calculate suggested refund amount based on returned items.
        Does not include restocking fees or shipping costs.

        Returns:
            Decimal: Sum of returned item values
        """
        if not self.items_json:
            return Decimal("0.00")

        total = Decimal("0.00")
        for item_data in self.items_json:
            try:
                order_item = self.order.items.get(id=item_data["order_item_id"])
                quantity = item_data.get("quantity", 0)
                # Calculate proportional refund based on quantity
                item_total = order_item.unit_price.amount * quantity
                total += item_total
            except (OrderItem.DoesNotExist, KeyError):
                continue

        return total
