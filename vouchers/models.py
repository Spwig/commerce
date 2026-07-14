import json
import secrets
import string
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
from djmoney.money import Money

User = get_user_model()


class VoucherCode(models.Model):
    """
    Main voucher/coupon model supporting discounts and gift cards
    """

    DISCOUNT_TYPES = [
        ("percentage", _("Percentage Discount")),
        ("fixed", _("Fixed Amount Discount")),
        ("gift_card", _("Gift Card Value")),
    ]

    APPLICATION_SCOPES = [
        ("cart", _("Entire Cart")),
        ("products", _("Specific Products")),
        ("categories", _("Specific Categories")),
    ]

    # Basic voucher information
    code = models.CharField(max_length=50, unique=True, db_index=True)
    name = models.CharField(max_length=200, help_text=_("Internal name for this voucher"))
    description = models.TextField(blank=True, help_text=_("Description shown to customers"))

    # Import tracking
    external_id = models.CharField(
        max_length=100,
        blank=True,
        db_index=True,
        help_text=_("Original coupon ID from source platform"),
    )
    migration_job = models.ForeignKey(
        "migration.MigrationJob",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="imported_coupons",
        help_text=_("Migration job that imported this coupon"),
    )

    # Discount configuration
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES, default="percentage")
    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        help_text=_("Percentage (0-100) or fixed amount"),
    )

    # For percentage discounts
    max_discount_amount = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency="USD",
        null=True,
        blank=True,
        help_text=_("Maximum discount amount for percentage vouchers"),
    )

    # Application scope
    application_scope = models.CharField(
        max_length=20,
        choices=APPLICATION_SCOPES,
        default="cart",
        help_text=_("What this voucher applies to"),
    )

    # Expiry settings
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True, help_text=_("Leave blank for no expiry"))
    days_valid = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text=_("Number of days valid from creation date (overrides end_date)"),
    )

    # Usage limits
    max_uses_total = models.PositiveIntegerField(
        null=True, blank=True, help_text=_("Total number of times this voucher can be used")
    )
    max_uses_per_customer = models.PositiveIntegerField(
        null=True, blank=True, help_text=_("Max uses per customer (0 = unlimited)")
    )
    current_uses = models.PositiveIntegerField(default=0)

    # Restrictions and rules
    min_order_value = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency="USD",
        null=True,
        blank=True,
        help_text=_("Minimum cart value to apply voucher"),
    )

    exclude_sale_items = models.BooleanField(
        default=False, help_text=_("Cannot be used on items already on sale")
    )

    cannot_combine_with_other_vouchers = models.BooleanField(
        default=False, help_text=_("Cannot be used with other vouchers")
    )

    cannot_combine_with_sale_items = models.BooleanField(
        default=False, help_text=_("Cannot be used if cart contains sale items")
    )

    # Customer restrictions
    first_time_customers_only = models.BooleanField(
        default=False, help_text=_("Only for customers with no previous orders")
    )

    # Gift card specific fields
    gift_card_balance = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency="USD",
        null=True,
        blank=True,
        help_text=_("Current balance for gift cards"),
    )

    original_gift_card_value = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency="USD",
        null=True,
        blank=True,
        help_text=_("Original gift card value"),
    )

    # Admin and status
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="created_vouchers"
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # Eligible products and categories (for targeted discounts)
    eligible_products = models.ManyToManyField(
        "catalog.Product",
        blank=True,
        help_text=_("Products this voucher applies to (if scope is products)"),
    )
    eligible_categories = models.ManyToManyField(
        "catalog.Category",
        blank=True,
        help_text=_("Categories this voucher applies to (if scope is categories)"),
    )

    class Meta:
        verbose_name = _("Voucher Code")
        verbose_name_plural = _("Voucher Codes")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["is_active", "start_date", "end_date"]),
            models.Index(fields=["discount_type"]),
            models.Index(fields=["application_scope"]),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_unique_code()

        # For gift cards, set discount_value to gift card value
        if self.discount_type == "gift_card" and self.original_gift_card_value:
            self.discount_value = self.original_gift_card_value.amount
            if not self.gift_card_balance:
                self.gift_card_balance = self.original_gift_card_value

        super().save(*args, **kwargs)

    def generate_unique_code(self, length=8):
        """Generate a unique voucher code"""
        characters = string.ascii_uppercase + string.digits
        while True:
            code = "".join(secrets.choice(characters) for _ in range(length))
            if not VoucherCode.objects.filter(code=code).exists():
                return code

    @property
    def is_valid(self):
        """Check if voucher is currently valid"""
        if not self.is_active:
            return False

        now = timezone.now()

        # Check start date
        if self.start_date and now < self.start_date:
            return False

        # Check end date
        if self.end_date and now > self.end_date:
            return False

        # Check days_valid (days from creation)
        if self.days_valid and self.created_at:
            expiry = self.created_at + timedelta(days=self.days_valid)
            if now > expiry:
                return False

        # Check usage limits
        return not (self.max_uses_total and self.current_uses >= self.max_uses_total)

    @property
    def is_gift_card(self):
        """Check if this is a gift card"""
        return self.discount_type == "gift_card"

    @property
    def uses_remaining(self):
        """Get number of uses remaining"""
        if not self.max_uses_total:
            return None
        return max(0, self.max_uses_total - self.current_uses)

    def can_be_used_by_customer(self, user, order_total=None, context=None):
        """
        Check if customer can use this voucher.

        Args:
            user: The user attempting to use the voucher
            order_total: Optional Money object for min_order_value check
            context: Optional dict for restriction evaluation (shipping_country, payment_method, etc.)

        Returns:
            tuple: (bool, str) - (can_use, message)
        """
        if not self.is_valid:
            return False, _("Voucher is not valid")

        # Check first-time customer restriction
        if self.first_time_customers_only and (
            user.is_authenticated
            and hasattr(user, "orders")
            and user.orders.filter(status="delivered").exists()
        ):
            return False, _("This voucher is only for first-time customers")

        # Check per-customer usage limit
        if self.max_uses_per_customer:
            customer_uses = VoucherUsage.objects.filter(voucher=self, user=user).count()
            if customer_uses >= self.max_uses_per_customer:
                return False, _("You have reached the usage limit for this voucher")

        # Check minimum order value
        if order_total is not None and self.min_order_value:
            if order_total < self.min_order_value:
                return False, _("Order total does not meet the minimum required for this voucher")

        # Evaluate advanced restrictions
        if context is not None:
            ctx = dict(context)
            ctx.setdefault("user", user)
            for restriction in self.restrictions.all():
                if not restriction.evaluate(ctx):
                    return False, _("This voucher cannot be used due to restrictions")

        return True, _("Valid")

    def calculate_discount(self, cart_total, eligible_amount=None):
        """Calculate discount amount for given cart total"""
        if not self.is_valid:
            return Decimal("0.00")

        # Use eligible amount if provided (for product/category specific discounts)
        base_amount = eligible_amount if eligible_amount is not None else cart_total

        if self.discount_type == "percentage":
            discount = base_amount * (self.discount_value / 100)
            # Apply max discount limit if set
            if self.max_discount_amount:
                discount = min(discount, self.max_discount_amount)
            return discount

        elif self.discount_type == "fixed":
            # Fixed discount cannot exceed the base amount
            fixed_discount = Money(self.discount_value, base_amount.currency)
            return min(fixed_discount, base_amount)

        elif self.discount_type == "gift_card":
            # Gift card discount cannot exceed balance or cart total
            if self.gift_card_balance:
                return min(self.gift_card_balance, cart_total)
            return Money(0, cart_total.currency)

        from core.utils import get_default_currency

        return Money(0, cart_total.currency if cart_total else get_default_currency())


class VoucherUsage(models.Model):
    """
    Track individual voucher uses
    """

    voucher = models.ForeignKey(VoucherCode, on_delete=models.CASCADE, related_name="uses")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey("orders.Order", on_delete=models.CASCADE, null=True, blank=True)

    # Usage details
    discount_amount = MoneyField(max_digits=10, decimal_places=2, default_currency="USD")
    cart_total = MoneyField(max_digits=10, decimal_places=2, default_currency="USD")

    # Session tracking for guest users
    session_key = models.CharField(max_length=255, null=True, blank=True)

    used_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Voucher Usage")
        verbose_name_plural = _("Voucher Usages")
        ordering = ["-used_at"]
        indexes = [
            models.Index(fields=["voucher", "-used_at"]),
            models.Index(fields=["user", "-used_at"]),
            models.Index(fields=["order"]),
        ]

    def __str__(self):
        user_info = self.user.username if self.user else f"Guest ({self.session_key[:8]})"
        return f"{self.voucher.code} used by {user_info}"


class VoucherRestriction(models.Model):
    """
    Advanced voucher restrictions and rules
    """

    RESTRICTION_TYPES = [
        ("user_group", _("Specific User Groups")),
        ("user_email_domain", _("Email Domain")),
        ("shipping_country", _("Shipping Country")),
        ("payment_method", _("Payment Method")),
        ("day_of_week", _("Day of Week")),
        ("time_of_day", _("Time of Day")),
    ]

    voucher = models.ForeignKey(VoucherCode, on_delete=models.CASCADE, related_name="restrictions")
    restriction_type = models.CharField(max_length=30, choices=RESTRICTION_TYPES)
    restriction_value = models.TextField(help_text=_("JSON or comma-separated values"))
    is_inclusive = models.BooleanField(
        default=True, help_text=_("True = must match, False = must not match")
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Voucher Restriction")
        verbose_name_plural = _("Voucher Restrictions")
        indexes = [
            models.Index(fields=["voucher", "restriction_type"]),
        ]

    def __str__(self):
        return f"{self.voucher.code} - {self.restriction_type}"

    def evaluate(self, context):
        """
        Evaluate this restriction against the given context.

        Args:
            context: dict with keys like 'user', 'shipping_country', 'payment_method',
                     'current_time', 'current_day'

        Returns:
            bool: True if the restriction passes (voucher can be used)
        """
        try:
            values = (
                json.loads(self.restriction_value)
                if self.restriction_value.startswith("[")
                else [v.strip() for v in self.restriction_value.split(",")]
            )
        except (json.JSONDecodeError, AttributeError):
            values = [v.strip() for v in self.restriction_value.split(",")]

        match = False

        if self.restriction_type == "user_group":
            user = context.get("user")
            if user and hasattr(user, "groups"):
                user_groups = set(user.groups.values_list("name", flat=True))
                match = bool(user_groups & set(values))

        elif self.restriction_type == "user_email_domain":
            user = context.get("user")
            if user and hasattr(user, "email") and user.email:
                domain = user.email.split("@")[-1].lower()
                match = domain in [v.lower() for v in values]

        elif self.restriction_type == "shipping_country":
            country = context.get("shipping_country", "")
            match = country.upper() in [v.upper() for v in values]

        elif self.restriction_type == "payment_method":
            method = context.get("payment_method", "")
            match = method.lower() in [v.lower() for v in values]

        elif self.restriction_type == "day_of_week":
            current_day = context.get("current_day") or timezone.now().strftime("%A")
            match = current_day.lower() in [v.lower() for v in values]

        elif self.restriction_type == "time_of_day":
            current_time = context.get("current_time") or timezone.now().time()
            for value in values:
                parts = value.split("-")
                if len(parts) == 2:
                    try:
                        from datetime import time as dt_time

                        start_h, start_m = map(int, parts[0].strip().split(":"))
                        end_h, end_m = map(int, parts[1].strip().split(":"))
                        start = dt_time(start_h, start_m)
                        end = dt_time(end_h, end_m)
                        if start <= current_time <= end:
                            match = True
                            break
                    except (ValueError, IndexError):
                        continue

        # is_inclusive=True means must match; is_inclusive=False means must NOT match
        return match if self.is_inclusive else not match


class GiftCard(models.Model):
    """
    Voucher-based gift card model (extends VoucherCode system).

    NOTE: The primary gift card system used in checkout, admin, POS, and
    email delivery is catalog.GiftCard. This model wraps VoucherCode for
    voucher-based gift card codes created via the admin voucher interface.
    See catalog/models.py GiftCard for the active implementation used
    in the main checkout and purchase flows.
    """

    GIFT_CARD_STATUS = [
        ("active", _("Active")),
        ("redeemed", _("Fully Redeemed")),
        ("expired", _("Expired")),
        ("cancelled", _("Cancelled")),
    ]

    # Links to voucher code
    voucher = models.OneToOneField(VoucherCode, on_delete=models.CASCADE, related_name="gift_card")

    # Gift card specific information
    recipient_email = models.EmailField(blank=True)
    recipient_name = models.CharField(max_length=200, blank=True)
    sender_name = models.CharField(max_length=200, blank=True)
    message = models.TextField(blank=True, help_text=_("Personal message from sender"))

    # Delivery options
    send_immediately = models.BooleanField(default=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    is_delivered = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(null=True, blank=True)

    # Purchase information
    purchased_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="purchased_gift_cards"
    )
    purchase_order = models.ForeignKey(
        "orders.Order", on_delete=models.SET_NULL, null=True, blank=True
    )

    status = models.CharField(max_length=20, choices=GIFT_CARD_STATUS, default="active")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Gift Card")
        verbose_name_plural = _("Gift Cards")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["recipient_email"]),
            models.Index(fields=["status"]),
            models.Index(fields=["delivery_date"]),
        ]

    def __str__(self):
        return f"Gift Card {self.voucher.code} - ${self.voucher.original_gift_card_value}"

    @property
    def balance(self):
        """Get current gift card balance"""
        return self.voucher.gift_card_balance

    @property
    def original_value(self):
        """Get original gift card value"""
        return self.voucher.original_gift_card_value

    def redeem_amount(self, amount):
        """Redeem a specific amount from gift card"""
        if self.balance and amount <= self.balance.amount:
            new_balance = self.balance.amount - amount
            self.voucher.gift_card_balance = Money(new_balance, self.balance.currency)
            self.voucher.save()

            if new_balance == 0:
                self.status = "redeemed"
                self.save()

            return True
        return False


class AppliedVoucher(models.Model):
    """
    Track vouchers applied to carts or orders.
    Used for cart-level voucher tracking during checkout,
    and for admin-side voucher application to existing orders.
    """

    cart = models.ForeignKey(
        "cart.Cart",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="applied_vouchers",
    )
    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="applied_vouchers",
    )
    voucher = models.ForeignKey(VoucherCode, on_delete=models.CASCADE)

    # Calculated discount at time of application
    discount_amount = MoneyField(max_digits=10, decimal_places=2, default_currency="USD")

    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Applied Voucher")
        verbose_name_plural = _("Applied Vouchers")
        ordering = ["-applied_at"]
        indexes = [
            models.Index(fields=["cart"]),
            models.Index(fields=["order"]),
            models.Index(fields=["voucher"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "voucher"],
                condition=models.Q(cart__isnull=False),
                name="unique_voucher_per_cart",
            ),
            models.UniqueConstraint(
                fields=["order", "voucher"],
                condition=models.Q(order__isnull=False),
                name="unique_voucher_per_order",
            ),
        ]

    def __str__(self):
        target = "cart" if self.cart_id else "order" if self.order_id else "unknown"
        return f"{self.voucher.code} applied to {target}"
