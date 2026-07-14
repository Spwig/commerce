from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Avg, Sum
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
from djmoney.money import Money

User = get_user_model()


class CustomerMetrics(models.Model):
    """
    Cache customer analytics for performance optimization
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer_metrics")

    # Lifetime Value Metrics
    total_spent = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency="USD",
        default=0,
        help_text="Total amount customer has spent",
    )

    lifetime_value = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency="USD",
        default=0,
        help_text="Calculated customer lifetime value",
    )

    # Order Statistics
    total_orders = models.PositiveIntegerField(default=0)
    completed_orders = models.PositiveIntegerField(default=0)
    cancelled_orders = models.PositiveIntegerField(default=0)

    average_order_value = MoneyField(
        max_digits=10, decimal_places=2, default_currency="USD", default=0
    )

    # Purchase Behavior
    first_purchase_date = models.DateTimeField(null=True, blank=True)
    last_purchase_date = models.DateTimeField(null=True, blank=True)
    days_since_last_purchase = models.IntegerField(default=0)
    purchase_frequency = models.FloatField(default=0.0, help_text="Average days between purchases")

    # Cart Behavior
    abandoned_carts_count = models.PositiveIntegerField(default=0)
    cart_abandonment_rate = models.FloatField(default=0.0)

    # Product Insights
    favorite_category = models.CharField(max_length=100, blank=True)
    most_purchased_product = models.CharField(max_length=255, blank=True)

    # Engagement Metrics
    total_sessions = models.PositiveIntegerField(default=0)
    wishlist_items_count = models.PositiveIntegerField(default=0)
    reviews_count = models.PositiveIntegerField(default=0)

    # Risk Indicators
    refund_rate = models.FloatField(default=0.0)
    support_tickets_count = models.PositiveIntegerField(default=0)

    # Probabilistic LTV Fields
    probability_alive = models.FloatField(
        default=0.0,
        help_text="Probability customer is still active (0.0 to 1.0) - from BG/NBD model",
    )
    predicted_purchases_12m = models.FloatField(
        default=0.0, help_text="Expected number of purchases in next 12 months"
    )
    predicted_purchases_24m = models.FloatField(
        default=0.0, help_text="Expected number of purchases in next 24 months"
    )
    ltv_confidence_score = models.FloatField(
        default=0.0, help_text="Confidence in LTV calculation (0.0 to 1.0)"
    )
    ltv_calculation_method = models.CharField(
        max_length=20, default="simple", help_text="Method used to calculate this customer's LTV"
    )
    ltv_last_calculated = models.DateTimeField(
        null=True, blank=True, help_text="When LTV was last calculated for this customer"
    )

    # Cohort Information
    cohort_month = models.DateField(
        null=True, blank=True, help_text="Customer's acquisition cohort (YYYY-MM-01)"
    )

    # Cache timestamps
    last_calculated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Customer Metrics")
        verbose_name_plural = _("Customer Metrics")
        indexes = [
            models.Index(fields=["total_spent"]),
            models.Index(fields=["lifetime_value"]),
            models.Index(fields=["last_purchase_date"]),
            models.Index(fields=["last_calculated"]),
            models.Index(fields=["cohort_month"]),
            models.Index(fields=["ltv_calculation_method"]),
            models.Index(fields=["probability_alive"]),
        ]

    def __str__(self):
        return f"Metrics for {self.user.get_full_name() or self.user.username}"

    @classmethod
    def calculate_for_user(cls, user):
        """Calculate and update metrics for a specific user"""
        from cart.models import Cart, Wishlist

        # Skip guest users
        if not user.is_authenticated or user.username.startswith("guest_"):
            return None

        metrics, created = cls.objects.get_or_create(user=user)

        # Get default currency from site settings
        from core.utils import get_default_currency

        default_currency = get_default_currency()

        # Get completed orders
        completed_orders = user.orders.filter(status="delivered")

        # Calculate order statistics
        metrics.total_orders = user.orders.count()
        metrics.completed_orders = completed_orders.count()
        metrics.cancelled_orders = user.orders.filter(status="cancelled").count()

        if completed_orders.exists():
            # Financial metrics
            total_spent = completed_orders.aggregate(total=Sum("total_amount"))["total"]
            if total_spent is None:
                total_spent = Money(0, default_currency)
            metrics.total_spent = total_spent

            avg_order_value = completed_orders.aggregate(avg=Avg("total_amount"))["avg"]
            if avg_order_value is None:
                avg_order_value = Money(0, default_currency)
            metrics.average_order_value = avg_order_value

            # Purchase dates
            first_order = completed_orders.earliest("created_at")
            last_order = completed_orders.latest("created_at")

            metrics.first_purchase_date = first_order.created_at
            metrics.last_purchase_date = last_order.created_at

            # Days since last purchase
            metrics.days_since_last_purchase = (timezone.now() - last_order.created_at).days

            # Purchase frequency (average days between orders)
            if metrics.completed_orders > 1:
                total_days = (last_order.created_at - first_order.created_at).days
                metrics.purchase_frequency = total_days / (metrics.completed_orders - 1)

            # Set cohort month (first day of acquisition month)
            if first_order:
                cohort_year = first_order.created_at.year
                cohort_month = first_order.created_at.month
                metrics.cohort_month = timezone.datetime(cohort_year, cohort_month, 1).date()

            # Calculate favorite category (most frequently purchased)
            category_counts = {}
            for order in completed_orders:
                for item in order.items.all():
                    if item.product and item.product.category:
                        category_name = item.product.category.name
                        category_counts[category_name] = (
                            category_counts.get(category_name, 0) + item.quantity
                        )

            if category_counts:
                metrics.favorite_category = max(category_counts, key=category_counts.get)

            # Enhanced RFM-based LTV Calculation
            # =====================================

            # 1. Recency Score (0-40 points)
            if metrics.days_since_last_purchase < 30:
                recency_score = 40
            elif metrics.days_since_last_purchase < 90:
                recency_score = 30
            elif metrics.days_since_last_purchase < 180:
                recency_score = 20
            elif metrics.days_since_last_purchase < 365:
                recency_score = 10
            else:
                recency_score = 5

            # 2. Frequency Score (0-35 points)
            if metrics.completed_orders >= 10:
                frequency_score = 35
            elif metrics.completed_orders >= 5:
                frequency_score = 25
            elif metrics.completed_orders >= 3:
                frequency_score = 18
            elif metrics.completed_orders >= 2:
                frequency_score = 12
            else:
                frequency_score = 5

            # 3. Monetary Score (0-25 points) - based on total_spent amount
            total_spent_amount = float(metrics.total_spent.amount)
            if total_spent_amount >= 5000:
                monetary_score = 25
            elif total_spent_amount >= 2000:
                monetary_score = 22
            elif total_spent_amount >= 1000:
                monetary_score = 18
            elif total_spent_amount >= 500:
                monetary_score = 15
            elif total_spent_amount >= 250:
                monetary_score = 12
            else:
                monetary_score = 8

            # 4. Calculate RFM Score (0-100)
            rfm_score = recency_score + frequency_score + monetary_score

            # 5. Convert RFM score to multiplier (range: 1.0 to 2.5)
            base_multiplier = Decimal("1.0") + (Decimal(str(rfm_score)) / Decimal("100")) * Decimal(
                "1.5"
            )

            # 6. Apply category adjustment
            category_multiplier = Decimal("1.0")
            if metrics.favorite_category:
                category_multiplier = ProductCategoryLTVMultiplier.get_multiplier_for_category(
                    metrics.favorite_category
                )

            # 7. Apply purchase frequency boost (for highly frequent buyers)
            frequency_boost = Decimal("1.0")
            if (
                metrics.purchase_frequency and metrics.purchase_frequency < 45
            ):  # Buying every 45 days or less
                frequency_boost = Decimal("1.3")
            elif metrics.purchase_frequency and metrics.purchase_frequency < 90:
                frequency_boost = Decimal("1.15")

            # 8. Calculate final LTV
            final_multiplier = base_multiplier * category_multiplier * frequency_boost
            metrics.lifetime_value = total_spent * final_multiplier

            # 9. Calculate confidence score (0.0 to 1.0)
            # High confidence with 10+ orders, medium at 5-9, low below 5
            if metrics.completed_orders >= 10:
                metrics.ltv_confidence_score = 1.0
            elif metrics.completed_orders >= 5:
                metrics.ltv_confidence_score = 0.7
            elif metrics.completed_orders >= 3:
                metrics.ltv_confidence_score = 0.5
            else:
                metrics.ltv_confidence_score = 0.3

            # 10. Set calculation metadata
            metrics.ltv_calculation_method = "simple"
            metrics.ltv_last_calculated = timezone.now()

        else:
            # No completed orders - reset to zero
            metrics.total_spent = Money(0, default_currency)
            metrics.average_order_value = Money(0, default_currency)
            metrics.lifetime_value = Money(0, default_currency)
            metrics.ltv_confidence_score = 0.0
            metrics.ltv_calculation_method = "simple"
            metrics.ltv_last_calculated = timezone.now()

        # Cart abandonment
        abandoned_carts = (
            Cart.objects.filter(
                user=user, items__isnull=False, updated_at__lt=timezone.now() - timedelta(hours=24)
            )
            .distinct()
            .count()
        )

        metrics.abandoned_carts_count = abandoned_carts
        if metrics.total_orders > 0:
            metrics.cart_abandonment_rate = abandoned_carts / (
                metrics.total_orders + abandoned_carts
            )

        # Wishlist items
        try:
            wishlist = Wishlist.objects.get(user=user, name="My Wishlist")
            metrics.wishlist_items_count = wishlist.items.count()
        except Wishlist.DoesNotExist:
            metrics.wishlist_items_count = 0

        # Refund rate
        refunded_orders = user.orders.filter(status="refunded").count()
        if metrics.completed_orders > 0:
            metrics.refund_rate = refunded_orders / metrics.completed_orders

        metrics.save()
        return metrics


class CustomerSegment(models.Model):
    """
    Define customer segments for targeted marketing
    """

    SEGMENT_TYPES = [
        ("guest", _("Guest Customer")),
        ("vip", _("VIP Customer")),
        ("regular", _("Regular Customer")),
        ("new", _("New Customer")),
        ("at_risk", _("At Risk")),
        ("inactive", _("Inactive")),
        ("high_value", _("High Value")),
        ("frequent_buyer", _("Frequent Buyer")),
        ("bargain_hunter", _("Bargain Hunter")),
    ]

    name = models.CharField(max_length=50, choices=SEGMENT_TYPES, unique=True)
    display_name = models.CharField(max_length=100)
    description = models.TextField()

    # Segment criteria
    min_total_spent = MoneyField(
        max_digits=10, decimal_places=2, default_currency="USD", null=True, blank=True
    )
    max_total_spent = MoneyField(
        max_digits=10, decimal_places=2, default_currency="USD", null=True, blank=True
    )

    min_orders = models.PositiveIntegerField(null=True, blank=True)
    max_orders = models.PositiveIntegerField(null=True, blank=True)

    min_days_since_last_purchase = models.IntegerField(null=True, blank=True)
    max_days_since_last_purchase = models.IntegerField(null=True, blank=True)

    # Display properties
    color = models.CharField(
        max_length=7, default="#007bff", help_text="Hex color code for segment display"
    )
    priority = models.IntegerField(
        default=0, help_text="Higher priority segments are checked first"
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Customer Segment")
        verbose_name_plural = _("Customer Segments")
        ordering = ["-priority", "name"]

    def __str__(self):
        return self.display_name

    @classmethod
    def determine_segment_for_user(cls, user):
        """Determine the appropriate segment for a user"""
        # First check if user is a guest (highest priority)
        if user.username.startswith("guest_"):
            try:
                return cls.objects.get(name="guest", is_active=True)
            except cls.DoesNotExist:
                pass  # Guest segment not configured, fall through to other segments

        try:
            metrics = user.customer_metrics
        except CustomerMetrics.DoesNotExist:
            metrics = CustomerMetrics.calculate_for_user(user)
            if not metrics:
                return None

        # Check segments in priority order (excluding guest segment)
        segments = (
            cls.objects.filter(is_active=True).exclude(name="guest").order_by("-priority", "name")
        )

        for segment in segments:
            if segment.matches_user(metrics):
                return segment

        return None

    def matches_user(self, metrics):
        """Check if user metrics match this segment criteria"""
        # Guest segment is handled separately in determine_segment_for_user
        if self.name == "guest":
            return False  # Never match through criteria

        # Currency-safe spending comparison
        if self.min_total_spent or self.max_total_spent:
            metrics_currency = str(metrics.total_spent_currency)

            if self.min_total_spent:
                min_amount = self._get_comparable_amount(self.min_total_spent, metrics_currency)
                if metrics.total_spent.amount < min_amount:
                    return False

            if self.max_total_spent:
                max_amount = self._get_comparable_amount(self.max_total_spent, metrics_currency)
                if metrics.total_spent.amount > max_amount:
                    return False

        # Check order count criteria
        if self.min_orders and metrics.completed_orders < self.min_orders:
            return False
        if self.max_orders and metrics.completed_orders > self.max_orders:
            return False

        # Check recency criteria
        if (
            self.min_days_since_last_purchase
            and metrics.days_since_last_purchase < self.min_days_since_last_purchase
        ):
            return False
        return not (
            self.max_days_since_last_purchase
            and metrics.days_since_last_purchase > self.max_days_since_last_purchase
        )

    @staticmethod
    def _get_comparable_amount(money_value, target_currency):
        """
        Convert a Money value to a Decimal amount in the target currency.
        Uses ExchangeRateService for cross-currency conversion.
        Falls back to raw amount comparison if conversion is unavailable.
        """
        source_currency = str(money_value.currency)
        if source_currency == target_currency:
            return money_value.amount

        try:
            from exchange_rates.services.exchange_service import ExchangeRateService

            service = ExchangeRateService()
            return service.convert(money_value.amount, source_currency, target_currency)
        except Exception:
            import logging

            logging.getLogger(__name__).warning(
                "Currency conversion failed (%s → %s), comparing raw amounts",
                source_currency,
                target_currency,
            )
            return money_value.amount


class LTVSettings(models.Model):
    """
    Singleton model for LTV calculation settings
    """

    CALCULATION_METHODS = [
        ("simple", "Simple (RFM-Based)"),
        ("cohort", "Cohort-Based Historical"),
        ("probabilistic", "Probabilistic (BG/NBD)"),
    ]

    calculation_method = models.CharField(
        max_length=20,
        choices=CALCULATION_METHODS,
        default="simple",
        help_text="Method used to calculate customer lifetime value",
    )

    default_discount_rate = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        default=Decimal("0.10"),
        validators=[MinValueValidator(Decimal("0.01"))],
        help_text="Annual discount rate for present value calculations (e.g., 0.10 for 10%)",
    )

    min_data_quality_threshold = models.IntegerField(
        default=100,
        help_text="Minimum number of customers with 2+ orders required for probabilistic method",
    )

    last_calculation_run = models.DateTimeField(
        null=True, blank=True, help_text="When LTV was last calculated for all customers"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("LTV Settings")
        verbose_name_plural = _("LTV Settings")

    def __str__(self):
        return f"LTV Settings ({self.get_calculation_method_display()})"

    def save(self, *args, **kwargs):
        # Ensure only one instance exists (singleton pattern)
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        """Get or create the singleton settings instance"""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings

    def can_use_probabilistic(self):
        """Check if there's enough data quality for probabilistic method"""
        repeat_customers = CustomerMetrics.objects.filter(completed_orders__gte=2).count()
        return repeat_customers >= self.min_data_quality_threshold


class ProductCategoryLTVMultiplier(models.Model):
    """
    Configure LTV multipliers for different product categories
    """

    category_name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Product category name (must match catalog categories)",
    )

    repeat_purchase_multiplier = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=Decimal("1.0"),
        validators=[MinValueValidator(Decimal("0.1"))],
        help_text="Multiplier for LTV based on repeat purchase likelihood (e.g., 1.3 for high-repeat categories)",
    )

    notes = models.TextField(
        blank=True, help_text="Internal notes about this category's purchase behavior"
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Product Category LTV Multiplier")
        verbose_name_plural = _("Product Category LTV Multipliers")
        ordering = ["category_name"]

    def __str__(self):
        return f"{self.category_name} ({self.repeat_purchase_multiplier}x)"

    @classmethod
    def get_multiplier_for_category(cls, category_name):
        """Get the multiplier for a specific category, or default to 1.0"""
        try:
            multiplier_obj = cls.objects.get(category_name=category_name, is_active=True)
            return multiplier_obj.repeat_purchase_multiplier
        except cls.DoesNotExist:
            return Decimal("1.0")


class CustomerCohort(models.Model):
    """
    Customer cohorts grouped by acquisition month and channel
    """

    cohort_date = models.DateField(help_text="First day of the acquisition month (YYYY-MM-01)")

    acquisition_channel = models.CharField(
        max_length=50, help_text="Acquisition channel from Order.source"
    )

    first_product_category = models.CharField(
        max_length=100, blank=True, help_text="Category of customer's first purchase"
    )

    customer_count = models.PositiveIntegerField(
        default=0, help_text="Total customers in this cohort"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Customer Cohort")
        verbose_name_plural = _("Customer Cohorts")
        ordering = ["-cohort_date", "acquisition_channel"]
        unique_together = [["cohort_date", "acquisition_channel", "first_product_category"]]
        indexes = [
            models.Index(fields=["cohort_date"]),
            models.Index(fields=["acquisition_channel"]),
        ]

    def __str__(self):
        channel_part = self.acquisition_channel or "All Channels"
        category_part = f" - {self.first_product_category}" if self.first_product_category else ""
        return f"{self.cohort_date.strftime('%Y-%m')} - {channel_part}{category_part}"

    @property
    def cohort_age_months(self):
        """Calculate how many months old this cohort is"""
        today = timezone.now().date()
        return (today.year - self.cohort_date.year) * 12 + (today.month - self.cohort_date.month)

    @property
    def average_ltv(self):
        """Get average LTV from latest cohort metrics"""
        latest_metric = self.metrics.order_by("-months_since_acquisition").first()
        if latest_metric:
            return latest_metric.average_ltv
        try:
            from core.utils import get_default_currency

            currency = get_default_currency()
        except Exception:
            currency = "USD"
        return Money(0, currency)

    @property
    def total_revenue(self):
        """Get total cumulative revenue from latest cohort metrics"""
        latest_metric = self.metrics.order_by("-months_since_acquisition").first()
        if latest_metric:
            return latest_metric.cumulative_revenue
        try:
            from core.utils import get_default_currency

            currency = get_default_currency()
        except Exception:
            currency = "USD"
        return Money(0, currency)

    @property
    def retention_rate_month_3(self):
        """Get retention rate at month 3"""
        metric = self.metrics.filter(months_since_acquisition=3).first()
        if metric:
            return round(metric.retention_rate * 100, 1)  # Convert to percentage
        return None

    @property
    def average_orders(self):
        """Calculate average orders per customer"""
        latest_metric = self.metrics.order_by("-months_since_acquisition").first()
        if latest_metric and self.customer_count > 0:
            return round(latest_metric.cumulative_orders / self.customer_count, 1)
        return 0


class CohortMetrics(models.Model):
    """
    Time-series metrics for each cohort showing retention and LTV over time
    """

    cohort = models.ForeignKey(CustomerCohort, on_delete=models.CASCADE, related_name="metrics")

    months_since_acquisition = models.PositiveIntegerField(
        help_text="Number of months since cohort's first purchase"
    )

    active_customers = models.PositiveIntegerField(
        default=0, help_text="Number of customers who made a purchase in this period"
    )

    cumulative_revenue = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="USD",
        default=0,
        help_text="Total revenue generated by cohort up to this point",
    )

    cumulative_orders = models.PositiveIntegerField(
        default=0, help_text="Total orders placed by cohort up to this point"
    )

    average_ltv = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency="USD",
        default=0,
        help_text="Average lifetime value per customer (cumulative_revenue / customer_count)",
    )

    retention_rate = models.FloatField(
        default=0.0, help_text="Percentage of customers still active (0.0 to 1.0)"
    )

    calculated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Cohort Metrics")
        verbose_name_plural = _("Cohort Metrics")
        ordering = ["cohort", "months_since_acquisition"]
        unique_together = [["cohort", "months_since_acquisition"]]
        indexes = [
            models.Index(fields=["cohort", "months_since_acquisition"]),
            models.Index(fields=["calculated_at"]),
        ]

    def __str__(self):
        return f"{self.cohort} - Month {self.months_since_acquisition} ({self.average_ltv})"


class AbandonedCart(models.Model):
    """
    Track abandoned carts for recovery campaigns
    """

    ABANDONMENT_REASONS = [
        ("unknown", _("Unknown")),
        ("high_shipping", _("High Shipping Cost")),
        ("total_too_high", _("Total Too High")),
        ("checkout_issues", _("Checkout Issues")),
        ("payment_failed", _("Payment Failed")),
        ("comparison_shopping", _("Comparison Shopping")),
        ("save_for_later", _("Saved for Later")),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="abandoned_carts")
    cart = models.OneToOneField("cart.Cart", on_delete=models.CASCADE)

    # Abandonment details
    abandoned_at = models.DateTimeField(auto_now_add=True)
    estimated_reason = models.CharField(
        max_length=20, choices=ABANDONMENT_REASONS, default="unknown"
    )

    # Cart snapshot at abandonment
    total_items = models.PositiveIntegerField()
    total_value = MoneyField(max_digits=10, decimal_places=2, default_currency="USD")

    # Recovery tracking
    recovery_emails_sent = models.PositiveIntegerField(default=0)
    recovered = models.BooleanField(default=False)
    recovered_at = models.DateTimeField(null=True, blank=True)
    recovery_order = models.ForeignKey(
        "orders.Order", on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        verbose_name = _("Abandoned Cart")
        verbose_name_plural = _("Abandoned Carts")
        ordering = ["-abandoned_at"]
        indexes = [
            models.Index(fields=["abandoned_at"]),
            models.Index(fields=["recovered"]),
            models.Index(fields=["user", "-abandoned_at"]),
        ]

    def __str__(self):
        status = "Recovered" if self.recovered else "Abandoned"
        return f"{status} cart - {self.user.get_full_name() or self.user.username}"

    @property
    def days_since_abandonment(self):
        return (timezone.now() - self.abandoned_at).days

    @classmethod
    def create_from_cart(cls, cart, reason="unknown"):
        """Create abandoned cart record from existing cart"""
        if cart.user and not cart.user.username.startswith("guest_"):
            abandoned, created = cls.objects.get_or_create(
                cart=cart,
                defaults={
                    "user": cart.user,
                    "estimated_reason": reason,
                    "total_items": cart.total_items,
                    "total_value": cart.total_amount,
                },
            )
            return abandoned
        return None


class CustomerNote(models.Model):
    """
    Staff notes about customers
    """

    NOTE_TYPES = [
        ("general", _("General Note")),
        ("support", _("Support Issue")),
        ("complaint", _("Complaint")),
        ("compliment", _("Compliment")),
        ("vip", _("VIP Service")),
        ("follow_up", _("Follow Up Required")),
        ("payment", _("Payment Issue")),
        ("shipping", _("Shipping Issue")),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer_notes")
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="created_customer_notes"
    )

    note_type = models.CharField(max_length=20, choices=NOTE_TYPES, default="general")
    title = models.CharField(max_length=200)
    content = models.TextField()

    # Follow-up tracking
    requires_follow_up = models.BooleanField(default=False)
    follow_up_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)

    # Visibility
    is_internal = models.BooleanField(
        default=True, help_text="Internal notes are only visible to staff"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Customer Note")
        verbose_name_plural = _("Customer Notes")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["customer", "-created_at"]),
            models.Index(fields=["requires_follow_up", "follow_up_date"]),
            models.Index(fields=["note_type"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.customer.get_full_name() or self.customer.username}"
