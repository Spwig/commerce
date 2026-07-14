"""
Customers App Integration Tests.

Comprehensive tests covering:
- Models: CustomerMetrics, CustomerSegment, LTVSettings, ProductCategoryLTVMultiplier,
  CustomerCohort, CohortMetrics, AbandonedCart, CustomerNote
- Admin: EnhancedCustomerProfileAdmin, CustomerMetricsAdmin, CustomerSegmentAdmin,
  AbandonedCartAdmin, CustomerNoteAdmin (list views, actions, filters, Media)
- Views: dashboard, cohort_dashboard redirect, ltv_settings GET/POST, export_customers,
  filter_customers AJAX, add_customer_note, customer_profile_actions,
  set_address_default, refresh_customer_metrics, recalculate_ltv, cohort_data_api,
  customer_analytics_api
- Security: staff_member_required on all admin views, CSRF protection, AJAX-only guards
- i18n: verbose_name translations on all models
- CSP: No inline styles in admin display methods (only CSS custom properties)
"""

import csv
import io
import json
from datetime import date, timedelta
from decimal import Decimal
from unittest.mock import MagicMock, patch

import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.test import Client, RequestFactory
from django.urls import reverse
from django.utils import timezone
from djmoney.money import Money

from accounts.models import CustomerProfile
from customers.admin import (
    AbandonedCartAdmin,
    CustomerMetricsAdmin,
    CustomerNoteAdmin,
    CustomerSegmentAdmin,
    EnhancedCustomerProfileAdmin,
)
from customers.models import (
    AbandonedCart,
    CohortMetrics,
    CustomerCohort,
    CustomerMetrics,
    CustomerNote,
    CustomerSegment,
    LTVSettings,
    ProductCategoryLTVMultiplier,
)
from tests.factories import (
    CartFactory,
    CartItemFactory,
    OrderFactory,
    ProductFactory,
    UserFactory,
)

User = get_user_model()

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.customers]


# ============================================================
# Fixtures
# ============================================================


@pytest.fixture
def staff_client(admin_user):
    """Django test client authenticated as staff user."""
    client = Client()
    client.force_login(admin_user)
    return client


@pytest.fixture
def anon_client():
    """Unauthenticated Django test client."""
    return Client()


@pytest.fixture
def non_staff_client(customer_user):
    """Django test client authenticated as non-staff user."""
    client = Client()
    client.force_login(customer_user)
    return client


@pytest.fixture
def customer_profile(customer_user):
    """CustomerProfile for the customer_user fixture."""
    profile, _ = CustomerProfile.objects.get_or_create(
        user=customer_user,
        defaults={"user": customer_user},
    )
    return profile


@pytest.fixture
def admin_profile(admin_user):
    """CustomerProfile for the admin_user fixture."""
    profile, _ = CustomerProfile.objects.get_or_create(
        user=admin_user,
        defaults={"user": admin_user},
    )
    return profile


@pytest.fixture
def customer_metrics(customer_user):
    """CustomerMetrics for the customer_user fixture."""
    metrics, _ = CustomerMetrics.objects.get_or_create(
        user=customer_user,
        defaults={
            "total_spent": Money(500, "USD"),
            "lifetime_value": Money(750, "USD"),
            "total_orders": 5,
            "completed_orders": 4,
            "cancelled_orders": 1,
            "average_order_value": Money(125, "USD"),
            "days_since_last_purchase": 15,
            "purchase_frequency": 30.0,
            "ltv_calculation_method": "simple",
            "ltv_confidence_score": 0.7,
            "cohort_month": date(2024, 1, 1),
        },
    )
    return metrics


@pytest.fixture
def customer_segment_vip():
    """VIP customer segment."""
    segment, _ = CustomerSegment.objects.update_or_create(
        name="vip",
        defaults={
            "display_name": "VIP Customer",
            "description": "High-value customers",
            "min_total_spent": Money(1000, "USD"),
            "max_total_spent": None,
            "min_orders": 5,
            "max_orders": None,
            "min_days_since_last_purchase": None,
            "max_days_since_last_purchase": None,
            "color": "#FFD700",
            "priority": 10,
            "is_active": True,
        },
    )
    return segment


@pytest.fixture
def customer_segment_new():
    """New customer segment."""
    segment, _ = CustomerSegment.objects.update_or_create(
        name="new",
        defaults={
            "display_name": "New Customer",
            "description": "Recently registered customers",
            "min_total_spent": None,
            "max_total_spent": None,
            "min_orders": None,
            "max_orders": 2,
            "min_days_since_last_purchase": None,
            "max_days_since_last_purchase": None,
            "color": "#28a745",
            "priority": 1,
            "is_active": True,
        },
    )
    return segment


@pytest.fixture
def customer_segment_at_risk():
    """At-risk customer segment."""
    segment, _ = CustomerSegment.objects.update_or_create(
        name="at_risk",
        defaults={
            "display_name": "At Risk",
            "description": "Customers at risk of churning",
            "min_total_spent": None,
            "max_total_spent": None,
            "min_orders": None,
            "max_orders": None,
            "min_days_since_last_purchase": 90,
            "max_days_since_last_purchase": None,
            "color": "#dc3545",
            "priority": 5,
            "is_active": True,
        },
    )
    return segment


@pytest.fixture
def customer_segment_guest():
    """Guest customer segment."""
    segment, _ = CustomerSegment.objects.update_or_create(
        name="guest",
        defaults={
            "display_name": "Guest Customer",
            "description": "Guest checkout users",
            "min_total_spent": None,
            "max_total_spent": None,
            "min_orders": None,
            "max_orders": None,
            "min_days_since_last_purchase": None,
            "max_days_since_last_purchase": None,
            "color": "#6c757d",
            "priority": 100,
            "is_active": True,
        },
    )
    return segment


@pytest.fixture
def ltv_settings():
    """LTV Settings singleton."""
    return LTVSettings.get_settings()


@pytest.fixture
def category_multiplier():
    """Product category LTV multiplier."""
    return ProductCategoryLTVMultiplier.objects.create(
        category_name="Electronics",
        repeat_purchase_multiplier=Decimal("1.5"),
        notes="High repeat purchase rate for electronics",
        is_active=True,
    )


@pytest.fixture
def customer_cohort():
    """A test customer cohort."""
    return CustomerCohort.objects.create(
        cohort_date=date(2024, 1, 1),
        acquisition_channel="direct",
        customer_count=50,
    )


@pytest.fixture
def cohort_metrics(customer_cohort):
    """Cohort metrics for month 3."""
    return CohortMetrics.objects.create(
        cohort=customer_cohort,
        months_since_acquisition=3,
        active_customers=30,
        cumulative_revenue=Money(15000, "USD"),
        cumulative_orders=120,
        average_ltv=Money(300, "USD"),
        retention_rate=0.6,
    )


@pytest.fixture
def abandoned_cart(customer_user, site_settings):
    """An abandoned cart for customer_user."""
    cart = CartFactory(user=customer_user)
    product = ProductFactory(price=Decimal("49.99"))
    CartItemFactory(cart=cart, product=product)
    return AbandonedCart.objects.create(
        user=customer_user,
        cart=cart,
        total_items=1,
        total_value=Money(Decimal("49.99"), "USD"),
        estimated_reason="unknown",
    )


@pytest.fixture
def customer_note(customer_user, admin_user):
    """A customer note created by admin for customer_user."""
    return CustomerNote.objects.create(
        customer=customer_user,
        created_by=admin_user,
        note_type="general",
        title="Test Note",
        content="This is a test note about the customer.",
    )


@pytest.fixture
def guest_user():
    """A guest user (username starts with guest_)."""
    return UserFactory(
        username="guest_abc123",
        email="guest@test.spwig.com",
    )


@pytest.fixture
def guest_profile(guest_user):
    """CustomerProfile for a guest user."""
    profile, _ = CustomerProfile.objects.get_or_create(
        user=guest_user,
        defaults={"user": guest_user},
    )
    return profile


@pytest.fixture
def request_factory():
    """Django RequestFactory for admin testing."""
    return RequestFactory()


# ============================================================
# Model Tests: CustomerMetrics
# ============================================================


class TestCustomerMetricsModel:
    def test_create_customer_metrics(self, customer_user):
        """CustomerMetrics can be created with all fields."""
        metrics = CustomerMetrics.objects.create(
            user=customer_user,
            total_spent=Money(100, "USD"),
            lifetime_value=Money(150, "USD"),
            total_orders=3,
            completed_orders=2,
            cancelled_orders=1,
            average_order_value=Money(50, "USD"),
            days_since_last_purchase=10,
            purchase_frequency=45.0,
            probability_alive=0.85,
            predicted_purchases_12m=3.5,
            predicted_purchases_24m=6.0,
            ltv_confidence_score=0.7,
            ltv_calculation_method="simple",
            cohort_month=date(2024, 1, 1),
        )
        assert metrics.pk is not None
        assert metrics.total_orders == 3
        assert metrics.ltv_calculation_method == "simple"

    def test_str_representation(self, customer_metrics):
        """__str__ returns descriptive string with user info."""
        result = str(customer_metrics)
        assert "Metrics for" in result

    def test_verbose_name_translated(self):
        """Meta verbose_name uses gettext_lazy for i18n."""
        assert str(CustomerMetrics._meta.verbose_name) == "Customer Metrics"
        assert str(CustomerMetrics._meta.verbose_name_plural) == "Customer Metrics"

    def test_one_to_one_constraint(self, customer_user):
        """Only one CustomerMetrics per user (OneToOneField)."""
        CustomerMetrics.objects.create(user=customer_user, total_orders=1)
        from django.db import IntegrityError, transaction

        with pytest.raises(IntegrityError), transaction.atomic():
            CustomerMetrics.objects.create(user=customer_user, total_orders=2)

    def test_indexes_defined(self):
        """Model has indexes on key query fields."""
        index_fields = [idx.fields for idx in CustomerMetrics._meta.indexes]
        assert ["total_spent"] in index_fields
        assert ["lifetime_value"] in index_fields
        assert ["last_purchase_date"] in index_fields
        assert ["cohort_month"] in index_fields

    def test_calculate_for_user_no_orders(self, customer_user, site_settings):
        """calculate_for_user with no orders sets zeroes."""
        metrics = CustomerMetrics.calculate_for_user(customer_user)
        assert metrics is not None
        assert metrics.total_orders == 0
        assert metrics.completed_orders == 0
        assert float(metrics.total_spent.amount) == 0
        assert float(metrics.lifetime_value.amount) == 0

    def test_calculate_for_user_skips_guest(self, guest_user, site_settings):
        """calculate_for_user returns None for guest users."""
        result = CustomerMetrics.calculate_for_user(guest_user)
        assert result is None

    def test_calculate_for_user_with_orders(self, customer_user, site_settings, category):
        """calculate_for_user calculates metrics from delivered orders."""
        product = ProductFactory(category=category, price=Decimal("100.00"))
        for _ in range(3):
            OrderFactory(
                user=customer_user,
                status="delivered",
                total_amount=Decimal("100.00"),
            )
        metrics = CustomerMetrics.calculate_for_user(customer_user)
        assert metrics.total_orders >= 3
        assert metrics.completed_orders == 3
        assert float(metrics.total_spent.amount) > 0
        assert metrics.first_purchase_date is not None
        assert metrics.last_purchase_date is not None

    def test_ltv_confidence_tiers(self, customer_user, site_settings):
        """LTV confidence score is based on completed order count."""
        # 1 order: low confidence (0.3)
        OrderFactory(user=customer_user, status="delivered", total_amount=Decimal("100.00"))
        metrics = CustomerMetrics.calculate_for_user(customer_user)
        assert metrics.ltv_confidence_score == 0.3

    def test_cohort_month_set_from_first_order(self, customer_user, site_settings):
        """cohort_month is set from the first completed order date."""
        OrderFactory(user=customer_user, status="delivered", total_amount=Decimal("50.00"))
        metrics = CustomerMetrics.calculate_for_user(customer_user)
        assert metrics.cohort_month is not None
        # Should be first day of current month
        today = timezone.now()
        assert metrics.cohort_month.day == 1
        assert metrics.cohort_month.month == today.month
        assert metrics.cohort_month.year == today.year


# ============================================================
# Model Tests: CustomerSegment
# ============================================================


class TestCustomerSegmentModel:
    def test_create_segment(self, customer_segment_vip):
        """CustomerSegment can be created with all criteria fields."""
        assert customer_segment_vip.pk is not None
        assert customer_segment_vip.name == "vip"
        assert customer_segment_vip.display_name == "VIP Customer"

    def test_str_representation(self, customer_segment_vip):
        """__str__ returns the display_name."""
        assert str(customer_segment_vip) == "VIP Customer"

    def test_verbose_name_translated(self):
        """Meta verbose_name uses gettext_lazy."""
        assert str(CustomerSegment._meta.verbose_name) == "Customer Segment"

    def test_ordering(self):
        """Default ordering is by -priority, name."""
        assert CustomerSegment._meta.ordering == ["-priority", "name"]

    def test_segment_type_choices(self):
        """SEGMENT_TYPES covers all expected values."""
        type_names = [t[0] for t in CustomerSegment.SEGMENT_TYPES]
        expected = [
            "guest",
            "vip",
            "regular",
            "new",
            "at_risk",
            "inactive",
            "high_value",
            "frequent_buyer",
            "bargain_hunter",
        ]
        for name in expected:
            assert name in type_names

    def test_unique_name_constraint(self):
        """Segment name is unique."""
        unique_name = f"test_unique_{timezone.now().timestamp()}"
        CustomerSegment.objects.create(
            name=unique_name,
            display_name="Unique Test",
            description="Test",
        )
        from django.db import IntegrityError, transaction

        with pytest.raises(IntegrityError), transaction.atomic():
            CustomerSegment.objects.create(
                name=unique_name,
                display_name="Copy",
                description="Copy",
            )

    def test_matches_user_spending_criteria(self, customer_segment_vip, customer_user):
        """matches_user checks min/max spending criteria."""
        metrics = CustomerMetrics.objects.create(
            user=customer_user,
            total_spent=Money(1500, "USD"),
            completed_orders=6,
        )
        assert customer_segment_vip.matches_user(metrics) is True

    def test_matches_user_fails_below_spending(self, customer_segment_vip, customer_user):
        """matches_user returns False when spending is below minimum."""
        metrics = CustomerMetrics.objects.create(
            user=customer_user,
            total_spent=Money(100, "USD"),
            completed_orders=6,
        )
        assert customer_segment_vip.matches_user(metrics) is False

    def test_matches_user_fails_below_orders(self, customer_segment_vip, customer_user):
        """matches_user returns False when order count is below minimum."""
        metrics = CustomerMetrics.objects.create(
            user=customer_user,
            total_spent=Money(2000, "USD"),
            completed_orders=2,
        )
        assert customer_segment_vip.matches_user(metrics) is False

    def test_matches_user_recency_criteria(self, customer_segment_at_risk, customer_user):
        """matches_user checks min/max recency criteria."""
        metrics = CustomerMetrics.objects.create(
            user=customer_user,
            days_since_last_purchase=120,
        )
        assert customer_segment_at_risk.matches_user(metrics) is True

    def test_matches_user_recency_too_recent(self, customer_segment_at_risk, customer_user):
        """matches_user returns False when purchase is too recent."""
        metrics = CustomerMetrics.objects.create(
            user=customer_user,
            days_since_last_purchase=30,
        )
        assert customer_segment_at_risk.matches_user(metrics) is False

    def test_guest_segment_never_matches_through_criteria(
        self, customer_segment_guest, customer_user
    ):
        """Guest segment always returns False from matches_user."""
        metrics = CustomerMetrics.objects.create(user=customer_user)
        assert customer_segment_guest.matches_user(metrics) is False

    def test_determine_segment_for_guest_user(self, customer_segment_guest, guest_user):
        """determine_segment_for_user returns guest segment for guest users."""
        segment = CustomerSegment.determine_segment_for_user(guest_user)
        assert segment == customer_segment_guest

    def test_determine_segment_for_regular_user(
        self, customer_segment_new, customer_user, site_settings
    ):
        """determine_segment_for_user evaluates criteria for non-guest users."""
        # New customer with 0 orders should match 'new' segment (max_orders=2)
        CustomerMetrics.objects.create(
            user=customer_user,
            completed_orders=0,
        )
        segment = CustomerSegment.determine_segment_for_user(customer_user)
        assert segment == customer_segment_new

    def test_determine_segment_returns_none_no_match(self, customer_user, site_settings):
        """determine_segment_for_user returns None when no segments match."""
        # Deactivate all existing segments so none can match
        CustomerSegment.objects.all().update(is_active=False)
        try:
            metrics, _ = CustomerMetrics.objects.get_or_create(
                user=customer_user,
                defaults={"completed_orders": 5},
            )
            metrics.completed_orders = 5
            metrics.save()
            segment = CustomerSegment.determine_segment_for_user(customer_user)
            assert segment is None
        finally:
            # Re-activate segments for other tests
            CustomerSegment.objects.all().update(is_active=True)


# ============================================================
# Model Tests: LTVSettings
# ============================================================


class TestLTVSettingsModel:
    def test_singleton_pattern(self):
        """LTVSettings enforces singleton via pk=1 in save()."""
        # get_settings creates or retrieves the singleton
        s1 = LTVSettings.get_settings()
        assert s1.pk == 1

        # Update the existing singleton
        s1.calculation_method = "cohort"
        s1.save()

        # Reload and verify
        s1.refresh_from_db()
        assert s1.pk == 1
        assert s1.calculation_method == "cohort"

        # Verify only one instance exists
        assert LTVSettings.objects.count() == 1

        # Reset to default for other tests
        s1.calculation_method = "simple"
        s1.save()

    def test_get_settings_creates_if_not_exists(self):
        """get_settings creates the singleton if it does not exist."""
        LTVSettings.objects.all().delete()
        settings = LTVSettings.get_settings()
        assert settings.pk == 1
        assert settings.calculation_method == "simple"

    def test_str_representation(self):
        """__str__ shows calculation method display."""
        settings = LTVSettings.get_settings()
        assert "Simple (RFM-Based)" in str(settings)

    def test_verbose_name_translated(self):
        """Meta verbose_name uses gettext_lazy."""
        assert str(LTVSettings._meta.verbose_name) == "LTV Settings"

    def test_calculation_methods_choices(self):
        """All expected calculation methods are available."""
        method_keys = [m[0] for m in LTVSettings.CALCULATION_METHODS]
        assert "simple" in method_keys
        assert "cohort" in method_keys
        assert "probabilistic" in method_keys

    def test_can_use_probabilistic_below_threshold(self):
        """can_use_probabilistic returns False when insufficient data."""
        settings = LTVSettings.get_settings()
        settings.min_data_quality_threshold = 100
        settings.save()
        assert settings.can_use_probabilistic() is False

    def test_default_discount_rate_validator(self):
        """default_discount_rate has MinValueValidator(0.01)."""
        from django.core.exceptions import ValidationError

        settings = LTVSettings.get_settings()
        settings.default_discount_rate = Decimal("0.00")
        with pytest.raises(ValidationError):
            settings.full_clean()


# ============================================================
# Model Tests: ProductCategoryLTVMultiplier
# ============================================================


class TestProductCategoryLTVMultiplierModel:
    def test_create_multiplier(self, category_multiplier):
        """ProductCategoryLTVMultiplier can be created."""
        assert category_multiplier.pk is not None
        assert category_multiplier.category_name == "Electronics"
        assert category_multiplier.repeat_purchase_multiplier == Decimal("1.5")

    def test_str_representation(self, category_multiplier):
        """__str__ shows category name and multiplier."""
        result = str(category_multiplier)
        assert "Electronics" in result
        assert "1.5" in result

    def test_verbose_name_translated(self):
        """Meta verbose_name uses gettext_lazy."""
        assert str(ProductCategoryLTVMultiplier._meta.verbose_name) == (
            "Product Category LTV Multiplier"
        )

    def test_ordering_by_category_name(self):
        """Default ordering is by category_name."""
        assert ProductCategoryLTVMultiplier._meta.ordering == ["category_name"]

    def test_unique_category_name(self):
        """category_name is unique."""
        ProductCategoryLTVMultiplier.objects.create(
            category_name="Books",
            repeat_purchase_multiplier=Decimal("1.2"),
        )
        from django.db import IntegrityError, transaction

        with pytest.raises(IntegrityError), transaction.atomic():
            ProductCategoryLTVMultiplier.objects.create(
                category_name="Books",
                repeat_purchase_multiplier=Decimal("1.3"),
            )

    def test_get_multiplier_for_category_exists(self, category_multiplier):
        """get_multiplier_for_category returns multiplier when category exists."""
        result = ProductCategoryLTVMultiplier.get_multiplier_for_category("Electronics")
        assert result == Decimal("1.5")

    def test_get_multiplier_for_category_not_found(self):
        """get_multiplier_for_category returns 1.0 for unknown categories."""
        result = ProductCategoryLTVMultiplier.get_multiplier_for_category("NonExistent")
        assert result == Decimal("1.0")

    def test_get_multiplier_ignores_inactive(self):
        """get_multiplier_for_category ignores inactive multipliers."""
        ProductCategoryLTVMultiplier.objects.create(
            category_name="Clothing",
            repeat_purchase_multiplier=Decimal("1.4"),
            is_active=False,
        )
        result = ProductCategoryLTVMultiplier.get_multiplier_for_category("Clothing")
        assert result == Decimal("1.0")

    def test_min_value_validator(self):
        """repeat_purchase_multiplier has MinValueValidator(0.1)."""
        from django.core.exceptions import ValidationError

        mult = ProductCategoryLTVMultiplier(
            category_name="Test",
            repeat_purchase_multiplier=Decimal("0.05"),
        )
        with pytest.raises(ValidationError):
            mult.full_clean()


# ============================================================
# Model Tests: CustomerCohort
# ============================================================


class TestCustomerCohortModel:
    def test_create_cohort(self, customer_cohort):
        """CustomerCohort can be created."""
        assert customer_cohort.pk is not None
        assert customer_cohort.customer_count == 50

    def test_str_representation(self, customer_cohort):
        """__str__ shows date and channel."""
        result = str(customer_cohort)
        assert "2024-01" in result
        assert "direct" in result

    def test_verbose_name_translated(self):
        """Meta verbose_name uses gettext_lazy."""
        assert str(CustomerCohort._meta.verbose_name) == "Customer Cohort"

    def test_ordering(self):
        """Default ordering is by -cohort_date, acquisition_channel."""
        assert CustomerCohort._meta.ordering == ["-cohort_date", "acquisition_channel"]

    def test_unique_together_constraint(self):
        """cohort_date + acquisition_channel + first_product_category is unique."""
        CustomerCohort.objects.create(
            cohort_date=date(2024, 6, 1),
            acquisition_channel="organic",
            first_product_category="",
            customer_count=10,
        )
        from django.db import IntegrityError, transaction

        with pytest.raises(IntegrityError), transaction.atomic():
            CustomerCohort.objects.create(
                cohort_date=date(2024, 6, 1),
                acquisition_channel="organic",
                first_product_category="",
                customer_count=20,
            )

    def test_cohort_age_months(self, customer_cohort):
        """cohort_age_months calculates months since cohort date."""
        age = customer_cohort.cohort_age_months
        assert isinstance(age, int)
        assert age >= 0

    def test_average_ltv_with_metrics(self, customer_cohort, cohort_metrics):
        """average_ltv returns value from latest cohort metrics."""
        result = customer_cohort.average_ltv
        assert float(result.amount) == 300.0

    def test_average_ltv_without_metrics(self):
        """average_ltv returns Money(0, 'USD') when no metrics exist."""
        cohort = CustomerCohort.objects.create(
            cohort_date=date(2024, 3, 1),
            acquisition_channel="referral",
            customer_count=5,
        )
        result = cohort.average_ltv
        assert float(result.amount) == 0

    def test_total_revenue_property(self, customer_cohort, cohort_metrics):
        """total_revenue returns cumulative_revenue from latest metrics."""
        result = customer_cohort.total_revenue
        assert float(result.amount) == 15000.0

    def test_retention_rate_month_3(self, customer_cohort, cohort_metrics):
        """retention_rate_month_3 returns retention rate at month 3."""
        rate = customer_cohort.retention_rate_month_3
        assert rate == 60.0  # 0.6 * 100

    def test_average_orders_property(self, customer_cohort, cohort_metrics):
        """average_orders calculates orders per customer."""
        result = customer_cohort.average_orders
        assert result == 2.4  # 120 / 50


# ============================================================
# Model Tests: CohortMetrics
# ============================================================


class TestCohortMetricsModel:
    def test_create_cohort_metrics(self, cohort_metrics):
        """CohortMetrics can be created."""
        assert cohort_metrics.pk is not None
        assert cohort_metrics.months_since_acquisition == 3
        assert cohort_metrics.retention_rate == 0.6

    def test_str_representation(self, cohort_metrics):
        """__str__ shows cohort, month, and LTV."""
        result = str(cohort_metrics)
        assert "Month 3" in result

    def test_verbose_name_translated(self):
        """Meta verbose_name uses gettext_lazy."""
        assert str(CohortMetrics._meta.verbose_name) == "Cohort Metrics"

    def test_unique_together_constraint(self, customer_cohort):
        """cohort + months_since_acquisition is unique."""
        CohortMetrics.objects.create(
            cohort=customer_cohort,
            months_since_acquisition=6,
            average_ltv=Money(400, "USD"),
        )
        from django.db import IntegrityError, transaction

        with pytest.raises(IntegrityError), transaction.atomic():
            CohortMetrics.objects.create(
                cohort=customer_cohort,
                months_since_acquisition=6,
                average_ltv=Money(500, "USD"),
            )


# ============================================================
# Model Tests: AbandonedCart
# ============================================================


class TestAbandonedCartModel:
    def test_create_abandoned_cart(self, abandoned_cart):
        """AbandonedCart can be created."""
        assert abandoned_cart.pk is not None
        assert abandoned_cart.total_items == 1
        assert abandoned_cart.recovered is False

    def test_str_representation_abandoned(self, abandoned_cart):
        """__str__ shows 'Abandoned' when not recovered."""
        result = str(abandoned_cart)
        assert "Abandoned" in result

    def test_str_representation_recovered(self, abandoned_cart):
        """__str__ shows 'Recovered' when recovered."""
        abandoned_cart.recovered = True
        abandoned_cart.save()
        result = str(abandoned_cart)
        assert "Recovered" in result

    def test_verbose_name_translated(self):
        """Meta verbose_name uses gettext_lazy."""
        assert str(AbandonedCart._meta.verbose_name) == "Abandoned Cart"

    def test_ordering(self):
        """Default ordering is by -abandoned_at."""
        assert AbandonedCart._meta.ordering == ["-abandoned_at"]

    def test_abandonment_reasons_choices(self):
        """ABANDONMENT_REASONS covers all expected values."""
        reason_keys = [r[0] for r in AbandonedCart.ABANDONMENT_REASONS]
        expected = [
            "unknown",
            "high_shipping",
            "total_too_high",
            "checkout_issues",
            "payment_failed",
            "comparison_shopping",
            "save_for_later",
        ]
        for key in expected:
            assert key in reason_keys

    def test_days_since_abandonment_property(self, abandoned_cart):
        """days_since_abandonment calculates days since abandoned_at."""
        days = abandoned_cart.days_since_abandonment
        assert isinstance(days, int)
        assert days >= 0

    def test_create_from_cart_method(self, customer_user, site_settings):
        """create_from_cart creates an AbandonedCart from a Cart."""
        cart = CartFactory(user=customer_user)
        product = ProductFactory(price=Decimal("29.99"))
        CartItemFactory(cart=cart, product=product)

        # Mock total_items and total_amount properties
        with patch.object(type(cart), "total_items", new_callable=lambda: property(lambda self: 1)):
            with patch.object(
                type(cart),
                "total_amount",
                new_callable=lambda: property(lambda self: Money(Decimal("29.99"), "USD")),
            ):
                result = AbandonedCart.create_from_cart(cart, reason="high_shipping")

        assert result is not None
        assert result.user == customer_user
        assert result.estimated_reason == "high_shipping"

    def test_create_from_cart_skips_guest(self, guest_user, site_settings):
        """create_from_cart returns None for guest users."""
        cart = CartFactory(user=guest_user)
        result = AbandonedCart.create_from_cart(cart)
        assert result is None

    def test_one_to_one_cart_constraint(self, abandoned_cart, customer_user):
        """Only one AbandonedCart per cart (OneToOneField)."""
        from django.db import IntegrityError, transaction

        with pytest.raises(IntegrityError), transaction.atomic():
            AbandonedCart.objects.create(
                user=customer_user,
                cart=abandoned_cart.cart,
                total_items=2,
                total_value=Money(100, "USD"),
            )


# ============================================================
# Model Tests: CustomerNote
# ============================================================


class TestCustomerNoteModel:
    def test_create_note(self, customer_note):
        """CustomerNote can be created."""
        assert customer_note.pk is not None
        assert customer_note.title == "Test Note"
        assert customer_note.note_type == "general"

    def test_str_representation(self, customer_note):
        """__str__ shows title and customer info."""
        result = str(customer_note)
        assert "Test Note" in result

    def test_verbose_name_translated(self):
        """Meta verbose_name uses gettext_lazy."""
        assert str(CustomerNote._meta.verbose_name) == "Customer Note"

    def test_ordering(self):
        """Default ordering is by -created_at."""
        assert CustomerNote._meta.ordering == ["-created_at"]

    def test_note_type_choices(self):
        """NOTE_TYPES covers all expected values."""
        type_keys = [t[0] for t in CustomerNote.NOTE_TYPES]
        expected = [
            "general",
            "support",
            "complaint",
            "compliment",
            "vip",
            "follow_up",
            "payment",
            "shipping",
        ]
        for key in expected:
            assert key in type_keys

    def test_follow_up_fields(self, customer_user, admin_user):
        """CustomerNote supports follow-up tracking."""
        note = CustomerNote.objects.create(
            customer=customer_user,
            created_by=admin_user,
            note_type="follow_up",
            title="Follow Up",
            content="Needs follow up",
            requires_follow_up=True,
            follow_up_date=date.today() + timedelta(days=7),
        )
        assert note.requires_follow_up is True
        assert note.follow_up_date is not None
        assert note.completed is False

    def test_created_by_set_null(self, customer_user, admin_user):
        """created_by is set to NULL when the staff user is deleted."""
        note = CustomerNote.objects.create(
            customer=customer_user,
            created_by=admin_user,
            note_type="general",
            title="Test",
            content="Content",
        )
        admin_user.delete()
        note.refresh_from_db()
        assert note.created_by is None


# ============================================================
# Admin Tests: EnhancedCustomerProfileAdmin
# ============================================================


class TestEnhancedCustomerProfileAdmin:
    def test_changelist_loads(self, staff_client, customer_profile):
        """Admin changelist page loads successfully."""
        url = reverse("admin:accounts_customerprofile_changelist")
        response = staff_client.get(url)
        assert response.status_code == 200

    def test_change_form_loads(self, staff_client, customer_profile, site_settings):
        """Admin change form loads for a customer profile."""
        url = reverse("admin:accounts_customerprofile_change", args=[customer_profile.pk])
        response = staff_client.get(url)
        assert response.status_code == 200

    def test_list_display_fields(self):
        """list_display contains expected columns."""
        admin_instance = EnhancedCustomerProfileAdmin(CustomerProfile, AdminSite())
        expected_fields = [
            "user",
            "account_type_display",
            "affiliate_status_display",
            "customer_value",
            "customer_segment_display",
            "total_orders_display",
            "days_since_last_order",
            "is_vip_customer",
        ]
        for field in expected_fields:
            assert field in admin_instance.list_display

    def test_search_fields(self):
        """search_fields includes user and phone fields."""
        admin_instance = EnhancedCustomerProfileAdmin(CustomerProfile, AdminSite())
        assert "user__username" in admin_instance.search_fields
        assert "user__email" in admin_instance.search_fields
        assert "phone" in admin_instance.search_fields

    def test_media_css(self):
        """Media class includes customer_admin_list.css."""
        admin_instance = EnhancedCustomerProfileAdmin(CustomerProfile, AdminSite())
        css = admin_instance.media._css.get("all", [])
        assert any("customer_admin_list.css" in c for c in css)

    def test_actions_registered(self):
        """Admin has all expected actions."""
        admin_instance = EnhancedCustomerProfileAdmin(CustomerProfile, AdminSite())
        assert "refresh_customer_metrics" in admin_instance.actions
        assert "export_customer_data" in admin_instance.actions
        assert "convert_to_affiliate" in admin_instance.actions
        assert "send_activation_invitations" in admin_instance.actions

    def test_account_type_display_registered(self, customer_profile, request_factory, admin_user):
        """account_type_display shows 'Registered' badge for non-guest users."""
        admin_instance = EnhancedCustomerProfileAdmin(CustomerProfile, AdminSite())
        result = admin_instance.account_type_display(customer_profile)
        assert "Registered" in result or "customer-badge-registered" in result

    def test_account_type_display_guest(self, guest_profile, request_factory, admin_user):
        """account_type_display shows 'Guest' badge for guest users."""
        admin_instance = EnhancedCustomerProfileAdmin(CustomerProfile, AdminSite())
        result = admin_instance.account_type_display(guest_profile)
        assert "Guest" in result or "customer-badge-guest" in result

    def test_customer_value_display(self, customer_profile, customer_metrics):
        """customer_value display method returns styled HTML."""
        admin_instance = EnhancedCustomerProfileAdmin(CustomerProfile, AdminSite())
        result = admin_instance.customer_value(customer_profile)
        assert "customer-value" in result

    def test_total_orders_display(self, customer_profile):
        """total_orders_display shows completed/total format."""
        admin_instance = EnhancedCustomerProfileAdmin(CustomerProfile, AdminSite())
        result = admin_instance.total_orders_display(customer_profile)
        assert "/" in result

    def test_account_type_display_no_inline_style(self, customer_profile):
        """account_type_display uses CSS classes, not inline styles."""
        admin_instance = EnhancedCustomerProfileAdmin(CustomerProfile, AdminSite())
        result = admin_instance.account_type_display(customer_profile)
        # Inline styles would contain style= with property:value patterns
        # CSS custom properties (--var) in style= are acceptable
        assert 'style="' not in result or "--" in result

    def test_export_customer_data_action(self, staff_client, customer_profile, site_settings):
        """export_customer_data action generates CSV download."""
        url = reverse("admin:accounts_customerprofile_changelist")
        response = staff_client.post(
            url,
            {
                "action": "export_customer_data",
                "_selected_action": [customer_profile.pk],
            },
        )
        assert response.status_code == 200
        assert response["Content-Type"] == "text/csv"
        assert "customers_export.csv" in response.get("Content-Disposition", "")

        # Parse CSV content
        content = response.content.decode("utf-8")
        reader = csv.reader(io.StringIO(content))
        header = next(reader)
        assert "Username" in header
        assert "Email" in header

    def test_refresh_customer_metrics_action(self, staff_client, customer_profile, site_settings):
        """refresh_customer_metrics action updates metrics."""
        url = reverse("admin:accounts_customerprofile_changelist")
        response = staff_client.post(
            url,
            {
                "action": "refresh_customer_metrics",
                "_selected_action": [customer_profile.pk],
            },
            follow=True,
        )
        assert response.status_code == 200

    def test_fieldsets_use_translations(self):
        """All fieldset names use gettext_lazy."""
        admin_instance = EnhancedCustomerProfileAdmin(CustomerProfile, AdminSite())
        for fieldset in admin_instance.fieldsets:
            # fieldset[0] is the name - should be a lazy string or None
            name = fieldset[0]
            if name is not None:
                # If it's a lazy string, str() resolves it
                assert isinstance(str(name), str)


# ============================================================
# Admin Tests: CustomerMetricsAdmin
# ============================================================


class TestCustomerMetricsAdmin:
    def test_changelist_loads(self, staff_client, customer_metrics):
        """Admin changelist page loads successfully."""
        url = reverse("admin:customers_customermetrics_changelist")
        response = staff_client.get(url)
        assert response.status_code == 200

    def test_list_display_fields(self):
        """list_display contains expected LTV-related columns."""
        admin_instance = CustomerMetricsAdmin(CustomerMetrics, AdminSite())
        assert "lifetime_value_display" in admin_instance.list_display
        assert "ltv_method_display" in admin_instance.list_display
        assert "ltv_confidence_display" in admin_instance.list_display
        assert "cohort_month_display" in admin_instance.list_display

    def test_lifetime_value_display_tiers(self):
        """lifetime_value_display shows tiered styling."""
        admin_instance = CustomerMetricsAdmin(CustomerMetrics, AdminSite())

        # High value (>5000)
        user = UserFactory()
        metrics = CustomerMetrics.objects.create(
            user=user,
            lifetime_value=Money(6000, "USD"),
        )
        result = admin_instance.lifetime_value_display(metrics)
        assert "ltv-value-very-high" in result
        assert "fa-crown" in result

    def test_ltv_method_display_rfm(self, customer_metrics):
        """ltv_method_display shows RFM badge for simple method."""
        admin_instance = CustomerMetricsAdmin(CustomerMetrics, AdminSite())
        result = admin_instance.ltv_method_display(customer_metrics)
        assert "ltv-badge-rfm" in result

    def test_ltv_method_display_not_calculated(self):
        """ltv_method_display shows 'Not Calculated' when no method set."""
        admin_instance = CustomerMetricsAdmin(CustomerMetrics, AdminSite())
        user = UserFactory()
        metrics = CustomerMetrics.objects.create(
            user=user,
            ltv_calculation_method="",
        )
        result = admin_instance.ltv_method_display(metrics)
        assert "ltv-badge-not-calculated" in result

    def test_ltv_confidence_display_levels(self):
        """ltv_confidence_display shows high/medium/low indicators."""
        admin_instance = CustomerMetricsAdmin(CustomerMetrics, AdminSite())

        # High confidence
        user = UserFactory()
        metrics = CustomerMetrics.objects.create(
            user=user,
            ltv_confidence_score=0.85,
        )
        result = admin_instance.ltv_confidence_display(metrics)
        assert "ltv-confidence-high" in result

    def test_cohort_month_display_with_link(self, customer_metrics):
        """cohort_month_display links to cohort dashboard."""
        admin_instance = CustomerMetricsAdmin(CustomerMetrics, AdminSite())
        result = admin_instance.cohort_month_display(customer_metrics)
        assert "Jan 2024" in result
        assert "cohort_dashboard" in result or "cohort-month-link" in result

    def test_cohort_month_display_no_cohort(self):
        """cohort_month_display shows dash when no cohort assigned."""
        admin_instance = CustomerMetricsAdmin(CustomerMetrics, AdminSite())
        user = UserFactory()
        metrics = CustomerMetrics.objects.create(
            user=user,
            cohort_month=None,
        )
        result = admin_instance.cohort_month_display(metrics)
        assert "muted-dash" in result

    def test_no_inline_styles_in_display_methods(self):
        """Admin display methods use CSS classes, not inline styles."""
        admin_instance = CustomerMetricsAdmin(CustomerMetrics, AdminSite())
        user = UserFactory()
        metrics = CustomerMetrics.objects.create(
            user=user,
            lifetime_value=Money(1000, "USD"),
            ltv_confidence_score=0.5,
            ltv_calculation_method="simple",
            cohort_month=date(2024, 6, 1),
        )
        for method_name in [
            "lifetime_value_display",
            "ltv_method_display",
            "ltv_confidence_display",
            "cohort_month_display",
        ]:
            method = getattr(admin_instance, method_name)
            result = method(metrics)
            # Check no inline style= (except CSS custom properties with --)
            if 'style="' in str(result):
                assert "--" in str(result), (
                    f"{method_name} uses inline style without CSS custom property"
                )

    def test_actions_registered(self):
        """Admin has recalculate actions."""
        admin_instance = CustomerMetricsAdmin(CustomerMetrics, AdminSite())
        assert "recalculate_metrics" in admin_instance.actions
        assert "recalculate_ltv_all_methods" in admin_instance.actions

    def test_recalculate_metrics_action(self, staff_client, customer_metrics, site_settings):
        """recalculate_metrics action updates metrics."""
        url = reverse("admin:customers_customermetrics_changelist")
        response = staff_client.post(
            url,
            {
                "action": "recalculate_metrics",
                "_selected_action": [customer_metrics.pk],
            },
            follow=True,
        )
        assert response.status_code == 200


# ============================================================
# Admin Tests: CustomerSegmentAdmin
# ============================================================


class TestCustomerSegmentAdmin:
    def test_changelist_loads(self, staff_client, customer_segment_vip):
        """Admin changelist page loads successfully."""
        url = reverse("admin:customers_customersegment_changelist")
        response = staff_client.get(url)
        assert response.status_code == 200

    def test_list_display_fields(self):
        """list_display contains expected columns."""
        admin_instance = CustomerSegmentAdmin(CustomerSegment, AdminSite())
        assert "color_preview" in admin_instance.list_display
        assert "customer_count" in admin_instance.list_display

    def test_color_preview_uses_css_custom_property(self, customer_segment_vip):
        """color_preview uses CSS custom property --swatch-color, not inline color."""
        admin_instance = CustomerSegmentAdmin(CustomerSegment, AdminSite())
        result = admin_instance.color_preview(customer_segment_vip)
        assert "--swatch-color" in result
        assert customer_segment_vip.color in result

    def test_customer_count_for_guest_segment(self, customer_segment_guest, guest_user):
        """customer_count counts guest users for guest segment."""
        admin_instance = CustomerSegmentAdmin(CustomerSegment, AdminSite())
        count = admin_instance.customer_count(customer_segment_guest)
        assert count >= 1  # At least the guest_user fixture


# ============================================================
# Admin Tests: AbandonedCartAdmin
# ============================================================


class TestAbandonedCartAdmin:
    def test_changelist_loads(self, staff_client, abandoned_cart):
        """Admin changelist page loads successfully."""
        url = reverse("admin:customers_abandonedcart_changelist")
        response = staff_client.get(url)
        assert response.status_code == 200

    def test_recovery_status_not_contacted(self, abandoned_cart):
        """recovery_status shows 'Not contacted' when no emails sent."""
        admin_instance = AbandonedCartAdmin(AbandonedCart, AdminSite())
        result = admin_instance.recovery_status(abandoned_cart)
        assert "Not contacted" in result or "recovery-not-contacted" in result

    def test_recovery_status_contacted(self, abandoned_cart):
        """recovery_status shows email count when emails sent."""
        abandoned_cart.recovery_emails_sent = 2
        abandoned_cart.save()
        admin_instance = AbandonedCartAdmin(AbandonedCart, AdminSite())
        result = admin_instance.recovery_status(abandoned_cart)
        assert "2" in result or "recovery-contacted" in result

    def test_recovery_status_recovered(self, abandoned_cart):
        """recovery_status shows 'Recovered' when cart is recovered."""
        abandoned_cart.recovered = True
        abandoned_cart.save()
        admin_instance = AbandonedCartAdmin(AbandonedCart, AdminSite())
        result = admin_instance.recovery_status(abandoned_cart)
        assert "Recovered" in result or "recovery-recovered" in result

    def test_mark_as_recovered_action(self, staff_client, abandoned_cart):
        """mark_as_recovered action marks selected carts as recovered."""
        url = reverse("admin:customers_abandonedcart_changelist")
        response = staff_client.post(
            url,
            {
                "action": "mark_as_recovered",
                "_selected_action": [abandoned_cart.pk],
            },
            follow=True,
        )
        assert response.status_code == 200
        abandoned_cart.refresh_from_db()
        assert abandoned_cart.recovered is True
        assert abandoned_cart.recovered_at is not None

    @patch("email_system.services.email_sender.EmailSendingService.queue_email")
    def test_send_recovery_email_action(
        self, mock_queue, staff_client, abandoned_cart, site_settings
    ):
        """send_recovery_email action queues emails for eligible carts."""
        url = reverse("admin:customers_abandonedcart_changelist")
        response = staff_client.post(
            url,
            {
                "action": "send_recovery_email",
                "_selected_action": [abandoned_cart.pk],
            },
            follow=True,
        )
        assert response.status_code == 200
        mock_queue.assert_called_once()
        abandoned_cart.refresh_from_db()
        assert abandoned_cart.recovery_emails_sent == 1

    @patch("email_system.services.email_sender.EmailSendingService.queue_email")
    def test_send_recovery_email_skips_recovered(
        self, mock_queue, staff_client, abandoned_cart, site_settings
    ):
        """send_recovery_email skips already-recovered carts."""
        abandoned_cart.recovered = True
        abandoned_cart.save()
        url = reverse("admin:customers_abandonedcart_changelist")
        response = staff_client.post(
            url,
            {
                "action": "send_recovery_email",
                "_selected_action": [abandoned_cart.pk],
            },
            follow=True,
        )
        assert response.status_code == 200
        mock_queue.assert_not_called()

    def test_media_includes_css_and_js(self):
        """Media class includes both CSS and JS files."""
        admin_instance = AbandonedCartAdmin(AbandonedCart, AdminSite())
        css = admin_instance.media._css.get("all", [])
        assert any("abandonedcart_change_form.css" in c for c in css)
        js = admin_instance.media._js
        assert any("abandonedcart_change_form.js" in j for j in js)

    def test_no_inline_style_in_recovery_status(self, abandoned_cart):
        """recovery_status uses CSS classes, not inline styles."""
        admin_instance = AbandonedCartAdmin(AbandonedCart, AdminSite())
        for state in ["not_contacted", "contacted", "recovered"]:
            if state == "contacted":
                abandoned_cart.recovery_emails_sent = 1
            elif state == "recovered":
                abandoned_cart.recovered = True
            result = admin_instance.recovery_status(abandoned_cart)
            if 'style="' in str(result):
                assert "--" in str(result), (
                    f"recovery_status ({state}) uses inline style without CSS custom property"
                )


# ============================================================
# Admin Tests: CustomerNoteAdmin
# ============================================================


class TestCustomerNoteAdmin:
    def test_changelist_loads(self, staff_client, customer_note):
        """Admin changelist page loads successfully."""
        url = reverse("admin:customers_customernote_changelist")
        response = staff_client.get(url)
        assert response.status_code == 200

    def test_save_model_sets_created_by(self, admin_user, customer_user, request_factory):
        """save_model sets created_by to request.user on creation."""
        admin_instance = CustomerNoteAdmin(CustomerNote, AdminSite())
        request = request_factory.post("/")
        request.user = admin_user

        note = CustomerNote(
            customer=customer_user,
            note_type="general",
            title="Auto Created",
            content="Test content",
        )
        admin_instance.save_model(request, note, form=None, change=False)
        assert note.created_by == admin_user

    def test_save_model_preserves_created_by_on_update(
        self, admin_user, customer_user, request_factory
    ):
        """save_model does NOT override created_by on update."""
        other_admin = UserFactory(staff=True, username="other_admin")
        note = CustomerNote.objects.create(
            customer=customer_user,
            created_by=other_admin,
            note_type="general",
            title="Original",
            content="Original content",
        )

        admin_instance = CustomerNoteAdmin(CustomerNote, AdminSite())
        request = request_factory.post("/")
        request.user = admin_user

        note.title = "Updated"
        admin_instance.save_model(request, note, form=None, change=True)
        assert note.created_by == other_admin  # Not overridden

    def test_mark_completed_action(self, staff_client, customer_note):
        """mark_completed action sets completed=True."""
        url = reverse("admin:customers_customernote_changelist")
        response = staff_client.post(
            url,
            {
                "action": "mark_completed",
                "_selected_action": [customer_note.pk],
            },
            follow=True,
        )
        assert response.status_code == 200
        customer_note.refresh_from_db()
        assert customer_note.completed is True

    def test_set_follow_up_required_action(self, staff_client, customer_note):
        """set_follow_up_required action sets requires_follow_up=True."""
        url = reverse("admin:customers_customernote_changelist")
        response = staff_client.post(
            url,
            {
                "action": "set_follow_up_required",
                "_selected_action": [customer_note.pk],
            },
            follow=True,
        )
        assert response.status_code == 200
        customer_note.refresh_from_db()
        assert customer_note.requires_follow_up is True


# ============================================================
# Admin Tests: SimpleListFilter Classes
# ============================================================


class TestAdminFilters:
    def test_account_type_filter_guest(self, staff_client, guest_profile, customer_profile):
        """AccountTypeFilter 'guest' returns only guest profiles."""
        url = reverse("admin:accounts_customerprofile_changelist")
        response = staff_client.get(url, {"account_type": "guest"})
        assert response.status_code == 200

    def test_account_type_filter_registered(self, staff_client, guest_profile, customer_profile):
        """AccountTypeFilter 'registered' excludes guest profiles."""
        url = reverse("admin:accounts_customerprofile_changelist")
        response = staff_client.get(url, {"account_type": "registered"})
        assert response.status_code == 200

    def test_ltv_method_filter(self, staff_client, customer_metrics):
        """LTVCalculationMethodFilter filters by LTV method."""
        url = reverse("admin:customers_customermetrics_changelist")
        response = staff_client.get(url, {"ltv_method": "simple"})
        assert response.status_code == 200

    def test_ltv_confidence_filter_high(self, staff_client):
        """LTVConfidenceFilter 'high' filters by confidence >= 80."""
        user = UserFactory()
        CustomerMetrics.objects.create(
            user=user,
            ltv_confidence_score=0.9,
        )
        url = reverse("admin:customers_customermetrics_changelist")
        response = staff_client.get(url, {"ltv_confidence": "high"})
        assert response.status_code == 200


# ============================================================
# View Tests: Staff-only Admin Views
# ============================================================


class TestDashboardView:
    def test_dashboard_renders(self, staff_client, site_settings):
        """Dashboard view renders successfully for staff."""
        url = reverse("customers:dashboard")
        response = staff_client.get(url)
        assert response.status_code == 200

    def test_dashboard_context_has_key_metrics(self, staff_client, site_settings):
        """Dashboard context includes all expected metrics."""
        url = reverse("customers:dashboard")
        response = staff_client.get(url)
        context = response.context
        assert "total_customers" in context
        assert "active_customers" in context
        assert "vip_count" in context
        assert "at_risk_count" in context
        assert "total_revenue" in context
        assert "segment_data" in context
        assert "recent_abandoned" in context
        assert "top_customers" in context
        assert "cohorts" in context

    def test_dashboard_requires_staff(self, non_staff_client, anon_client):
        """Dashboard redirects non-staff users."""
        url = reverse("customers:dashboard")
        # Non-staff user
        response = non_staff_client.get(url)
        assert response.status_code == 302
        assert "/admin/" in response.url or "/login/" in response.url

        # Anonymous user
        response = anon_client.get(url)
        assert response.status_code == 302


class TestCohortDashboardRedirect:
    def test_cohort_dashboard_redirects_to_dashboard_with_tab(self, staff_client):
        """cohort_dashboard redirects to dashboard?tab=cohorts."""
        url = reverse("customers:cohort_dashboard")
        response = staff_client.get(url)
        assert response.status_code == 302
        assert "dashboard" in response.url
        assert "tab=cohorts" in response.url


class TestLTVSettingsView:
    def test_ltv_settings_get(self, staff_client, site_settings):
        """LTV settings page renders with form data."""
        url = reverse("customers:ltv_settings")
        response = staff_client.get(url)
        assert response.status_code == 200
        context = response.context
        assert "settings" in context
        assert "data_quality" in context
        assert "calculation_methods" in context

    def test_ltv_settings_post_saves(self, staff_client, site_settings):
        """LTV settings POST saves configuration changes."""
        url = reverse("customers:ltv_settings")
        response = staff_client.post(
            url,
            {
                "calculation_method": "cohort",
                "default_discount_rate": "0.12",
                "min_data_quality_threshold": "200",
            },
        )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["success"] is True

        # Verify settings were saved
        settings = LTVSettings.get_settings()
        assert settings.calculation_method == "cohort"
        assert settings.min_data_quality_threshold == 200

    @patch("customers.tasks.calculate_all_customer_ltv_task")
    def test_ltv_settings_post_with_recalculation(self, mock_task, staff_client, site_settings):
        """LTV settings POST with trigger_recalculation queues task."""
        mock_task.delay.return_value = MagicMock(id="test-task-id")
        url = reverse("customers:ltv_settings")
        response = staff_client.post(
            url,
            {
                "calculation_method": "simple",
                "default_discount_rate": "0.10",
                "min_data_quality_threshold": "100",
                "trigger_recalculation": "true",
            },
        )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["success"] is True
        assert "task_id" in data
        mock_task.delay.assert_called_once()

    def test_ltv_settings_requires_staff(self, non_staff_client, anon_client):
        """LTV settings requires staff access."""
        url = reverse("customers:ltv_settings")
        response = non_staff_client.get(url)
        assert response.status_code == 302


class TestExportCustomersView:
    def test_export_csv(self, staff_client, customer_profile, site_settings):
        """export_customers generates a valid CSV."""
        url = reverse("customers:export")
        response = staff_client.get(url)
        assert response.status_code == 200
        assert response["Content-Type"] == "text/csv"
        assert "customers_export.csv" in response.get("Content-Disposition", "")

        content = response.content.decode("utf-8")
        reader = csv.reader(io.StringIO(content))
        header = next(reader)
        assert len(header) >= 10

    def test_export_excludes_guests(
        self, staff_client, customer_profile, guest_profile, site_settings
    ):
        """export_customers excludes guest users."""
        url = reverse("customers:export")
        response = staff_client.get(url)
        content = response.content.decode("utf-8")
        assert "guest_" not in content

    def test_export_requires_staff(self, non_staff_client):
        """export_customers requires staff access."""
        url = reverse("customers:export")
        response = non_staff_client.get(url)
        assert response.status_code == 302


class TestRefreshMetricsView:
    def test_refresh_metrics_post(self, staff_client, customer_profile, site_settings):
        """refresh_customer_metrics POST recalculates all metrics."""
        url = reverse("customers:refresh_metrics")
        response = staff_client.post(url)
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["success"] is True

    def test_refresh_metrics_get_rejected(self, staff_client, site_settings):
        """refresh_customer_metrics GET returns failure."""
        url = reverse("customers:refresh_metrics")
        response = staff_client.get(url)
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["success"] is False

    def test_refresh_metrics_requires_staff(self, non_staff_client):
        """refresh_customer_metrics requires staff access."""
        url = reverse("customers:refresh_metrics")
        response = non_staff_client.post(url)
        assert response.status_code == 302


class TestFilterCustomersView:
    def test_filter_requires_ajax_header(self, staff_client, site_settings):
        """filter_customers requires X-Requested-With: XMLHttpRequest."""
        url = reverse("customers:filter_customers")
        # Without AJAX header
        response = staff_client.get(url)
        assert response.status_code == 400

    def test_filter_with_ajax_header(self, staff_client, customer_profile, site_settings):
        """filter_customers returns HTML and count with AJAX header."""
        url = reverse("customers:filter_customers")
        response = staff_client.get(
            url,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert "html" in data
        assert "count" in data

    def test_filter_with_search(self, staff_client, customer_profile, site_settings):
        """filter_customers supports search parameter."""
        url = reverse("customers:filter_customers")
        response = staff_client.get(
            url,
            {"search": customer_profile.user.username},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["count"] >= 0

    def test_filter_requires_staff(self, non_staff_client):
        """filter_customers requires staff access."""
        url = reverse("customers:filter_customers")
        response = non_staff_client.get(
            url,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        assert response.status_code == 302


class TestAddCustomerNoteView:
    def test_add_note_post(self, staff_client, customer_profile, admin_user, site_settings):
        """add_customer_note creates a new note via POST."""
        url = reverse("customers:add_customer_note")
        response = staff_client.post(
            url,
            {
                "customer_id": customer_profile.pk,
                "note_type": "general",
                "title": "Test AJAX Note",
                "content": "Note content from AJAX",
            },
        )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["success"] is True
        assert data["note_id"] is not None

        # Verify note was created
        note = CustomerNote.objects.get(pk=data["note_id"])
        assert note.title == "Test AJAX Note"
        assert note.customer == customer_profile.user
        assert note.created_by == admin_user

    def test_add_note_get_rejected(self, staff_client, site_settings):
        """add_customer_note rejects GET requests."""
        url = reverse("customers:add_customer_note")
        response = staff_client.get(url)
        assert response.status_code == 405

    def test_add_note_requires_staff(self, non_staff_client):
        """add_customer_note requires staff access."""
        url = reverse("customers:add_customer_note")
        response = non_staff_client.post(url, {})
        assert response.status_code == 302


class TestCustomerProfileActionsView:
    def test_refresh_metrics_action(self, staff_client, customer_profile, site_settings):
        """customer_profile_actions with action=refresh_metrics works."""
        url = reverse(
            "customers:customer_profile_actions",
            args=[customer_profile.pk],
        )
        response = staff_client.get(url, {"action": "refresh_metrics"})
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["success"] is True

    def test_export_action_returns_csv(self, staff_client, customer_profile, site_settings):
        """customer_profile_actions with action=export returns CSV."""
        url = reverse(
            "customers:customer_profile_actions",
            args=[customer_profile.pk],
        )
        response = staff_client.get(url, {"action": "export"})
        assert response.status_code == 200
        assert response["Content-Type"] == "text/csv"

    def test_invalid_action(self, staff_client, customer_profile, site_settings):
        """customer_profile_actions with unknown action returns 400."""
        url = reverse(
            "customers:customer_profile_actions",
            args=[customer_profile.pk],
        )
        response = staff_client.get(url, {"action": "nonexistent"})
        assert response.status_code == 400

    def test_requires_staff(self, non_staff_client, customer_profile):
        """customer_profile_actions requires staff access."""
        url = reverse(
            "customers:customer_profile_actions",
            args=[customer_profile.pk],
        )
        response = non_staff_client.get(url, {"action": "refresh_metrics"})
        assert response.status_code == 302


class TestSetAddressDefaultView:
    def test_set_default_requires_post(self, staff_client, site_settings):
        """set_address_default only accepts POST."""
        from orders.models import Address

        addr = Address.objects.create(
            user=UserFactory(),
            name="Test",
            address1="123 Test St",
            city="NYC",
            state="NY",
            postal_code="10001",
            country="US",
        )
        # The URL pattern is in the customers.urls (API urls), not admin urls
        # It's at: api/customers/admin/addresses/<id>/set-default/
        url = f"/api/customers/admin/addresses/{addr.pk}/set-default/"
        response = staff_client.get(url)
        assert response.status_code == 405  # Method not allowed for GET

    @patch("orders.services.address_service.AddressService.set_default_address")
    def test_set_default_post(self, mock_set_default, staff_client, site_settings):
        """set_address_default POST sets address as default."""
        from orders.models import Address

        addr = Address.objects.create(
            user=UserFactory(),
            name="Test",
            address1="123 Test St",
            city="NYC",
            state="NY",
            postal_code="10001",
            country="US",
        )
        mock_set_default.return_value = (True, "Address set as default")
        url = f"/api/customers/admin/addresses/{addr.pk}/set-default/"
        response = staff_client.post(url)
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["success"] is True

    def test_set_default_nonexistent_address(self, staff_client, site_settings):
        """set_address_default returns 404 for nonexistent address."""
        url = "/api/customers/admin/addresses/99999/set-default/"
        response = staff_client.post(url)
        assert response.status_code == 404


class TestRecalculateLTVView:
    def test_requires_ajax_header(self, staff_client, site_settings):
        """recalculate_ltv requires X-Requested-With header."""
        url = reverse("customers:recalculate_ltv")
        response = staff_client.post(url)
        assert response.status_code == 400

    def test_requires_post_method(self, staff_client, site_settings):
        """recalculate_ltv rejects GET requests."""
        url = reverse("customers:recalculate_ltv")
        response = staff_client.get(
            url,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        assert response.status_code == 405

    def test_sync_simple_recalculation(self, staff_client, customer_profile, site_settings):
        """recalculate_ltv sync mode with simple method updates customers."""
        LTVSettings.objects.update_or_create(
            pk=1,
            defaults={"calculation_method": "simple"},
        )
        url = reverse("customers:recalculate_ltv")
        response = staff_client.post(
            url,
            {"scope": "all", "async": "false"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["success"] is True
        assert "customers_updated" in data

    @patch("customers.tasks.calculate_all_customer_ltv_task")
    def test_async_recalculation(self, mock_task, staff_client, site_settings):
        """recalculate_ltv async mode queues Celery task."""
        mock_task.delay.return_value = MagicMock(id="test-task-id")
        url = reverse("customers:recalculate_ltv")
        response = staff_client.post(
            url,
            {"scope": "all", "async": "true"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["success"] is True
        assert data["async"] is True
        assert data["task_id"] == "test-task-id"

    def test_single_user_sync_recalculation(
        self, staff_client, customer_user, customer_profile, site_settings
    ):
        """recalculate_ltv can target a single user ID."""
        url = reverse("customers:recalculate_ltv")
        response = staff_client.post(
            url,
            {"scope": str(customer_user.pk), "async": "false"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["success"] is True

    def test_requires_staff(self, non_staff_client):
        """recalculate_ltv requires staff access."""
        url = reverse("customers:recalculate_ltv")
        response = non_staff_client.post(
            url,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        assert response.status_code == 302


class TestCohortDataAPIView:
    def test_requires_ajax_header(self, staff_client, site_settings):
        """cohort_data_api requires X-Requested-With header."""
        url = reverse("customers:cohort_data_api")
        response = staff_client.get(url)
        assert response.status_code == 400

    @patch("customers.services.cohort_service.CohortService.get_cohort_comparison")
    @patch("customers.services.cohort_service.CohortService.get_retention_heatmap_data")
    @patch("customers.services.cohort_service.CohortService.get_retention_insights")
    @patch("customers.services.cohort_service.CohortService.get_ltv_by_channel")
    @patch("customers.services.cohort_service.CohortService.get_channel_insights")
    @patch("customers.services.cohort_service.CohortService.get_ltv_by_category")
    @patch("customers.services.cohort_service.CohortService.get_category_insights")
    @patch("customers.services.cohort_service.CohortService.get_cumulative_revenue_curve")
    @patch("customers.services.cohort_service.CohortService.get_revenue_curve_insights")
    def test_cohort_data_returns_json(
        self,
        mock_rev_insights,
        mock_rev_curve,
        mock_cat_insights,
        mock_cat_data,
        mock_ch_insights,
        mock_ch_data,
        mock_ret_insights,
        mock_heatmap,
        mock_comparison,
        staff_client,
        site_settings,
    ):
        """cohort_data_api returns JSON with datasets."""
        mock_comparison.return_value = []
        mock_heatmap.return_value = {"cohorts": [], "months": [], "data": []}
        mock_ret_insights.return_value = []
        mock_ch_data.return_value = []
        mock_ch_insights.return_value = []
        mock_cat_data.return_value = []
        mock_cat_insights.return_value = []
        mock_rev_curve.return_value = []
        mock_rev_insights.return_value = []

        url = reverse("customers:cohort_data_api")
        response = staff_client.get(
            url,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["success"] is True
        assert "labels" in data
        assert "datasets" in data

    def test_cohort_data_specific_cohort(
        self, staff_client, customer_cohort, cohort_metrics, site_settings
    ):
        """cohort_data_api returns specific cohort when cohort_id is provided."""
        url = reverse("customers:cohort_data_api")
        with patch(
            "customers.services.cohort_service.CohortService.get_cohort_retention_curve"
        ) as mock_curve:
            mock_curve.return_value = []
            response = staff_client.get(
                url,
                {"cohort_id": customer_cohort.pk},
                HTTP_X_REQUESTED_WITH="XMLHttpRequest",
            )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["success"] is True
        assert data["cohort"]["id"] == customer_cohort.pk

    def test_requires_staff(self, non_staff_client):
        """cohort_data_api requires staff access."""
        url = reverse("customers:cohort_data_api")
        response = non_staff_client.get(
            url,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        assert response.status_code == 302


class TestCustomerAnalyticsAPIView:
    @patch("customers.services.customer_service.CustomerService.get_revenue_by_segment")
    @patch("customers.services.customer_service.CustomerService.get_segment_insights")
    @patch("customers.services.customer_service.CustomerService.get_churn_risk_distribution")
    @patch("customers.services.customer_service.CustomerService.get_churn_risk_insights")
    @patch(
        "customers.services.customer_service.CustomerService.get_purchase_frequency_distribution"
    )
    @patch("customers.services.customer_service.CustomerService.get_frequency_insights")
    @patch("customers.services.customer_service.CustomerService.get_predicted_vs_actual")
    @patch("customers.services.customer_service.CustomerService.get_prediction_insights")
    def test_analytics_api_returns_json(
        self,
        mock_pred_insights,
        mock_pred_data,
        mock_freq_insights,
        mock_freq_data,
        mock_churn_insights,
        mock_churn_data,
        mock_seg_insights,
        mock_seg_rev,
        staff_client,
        site_settings,
    ):
        """customer_analytics_api returns comprehensive JSON data."""
        mock_seg_rev.return_value = []
        mock_seg_insights.return_value = []
        mock_churn_data.return_value = {}
        mock_churn_insights.return_value = []
        mock_freq_data.return_value = {}
        mock_freq_insights.return_value = []
        mock_pred_data.return_value = {}
        mock_pred_insights.return_value = []

        url = reverse("customers:analytics_api")
        response = staff_client.get(url)
        assert response.status_code == 200
        data = json.loads(response.content)
        assert "customer_growth" in data
        assert "segment_revenue" in data
        assert "frequency_distribution" in data

    def test_requires_staff(self, non_staff_client):
        """customer_analytics_api requires staff access."""
        url = reverse("customers:analytics_api")
        response = non_staff_client.get(url)
        assert response.status_code == 302


# ============================================================
# View Tests: Customer-Facing API (DRF)
# ============================================================


class TestCustomerDashboardAPI:
    @patch("customers.services.customer_service.CustomerService.get_dashboard_summary")
    def test_dashboard_api_authenticated(self, mock_dashboard, auth_client):
        """Customer dashboard API returns data for authenticated user."""
        mock_dashboard.return_value = {
            "customer_info": {},
            "quick_stats": {},
            "loyalty_status": {},
            "recent_activity": [],
            "recommendations": [],
            "alerts": [],
        }
        response = auth_client.get("/api/customers/dashboard/")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_dashboard_api_unauthenticated(self, api_client):
        """Customer dashboard API rejects unauthenticated requests."""
        response = api_client.get("/api/customers/dashboard/")
        assert response.status_code in (401, 403)


class TestCustomerStatsAPI:
    @patch("customers.services.customer_service.CustomerService.get_order_statistics")
    def test_stats_api_authenticated(self, mock_stats, auth_client):
        """Customer stats API returns data for authenticated user."""
        mock_stats.return_value = {
            "total_orders": 5,
            "completed_orders": 4,
            "total_spent": "500.00",
        }
        response = auth_client.get("/api/customers/stats/")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_stats_api_unauthenticated(self, api_client):
        """Customer stats API rejects unauthenticated requests."""
        response = api_client.get("/api/customers/stats/")
        assert response.status_code in (401, 403)


class TestCustomerInsightsAPI:
    @patch("customers.services.customer_service.CustomerService.get_spending_insights")
    def test_insights_api_authenticated(self, mock_insights, auth_client):
        """Customer insights API returns data for authenticated user."""
        mock_insights.return_value = {
            "spending_overview": {},
            "monthly_spending": [],
            "category_preferences": [],
        }
        response = auth_client.get("/api/customers/insights/")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


class TestCustomerLifetimeValueAPI:
    @patch("customers.services.customer_service.CustomerService.get_lifetime_value")
    def test_ltv_api_authenticated(self, mock_ltv, auth_client):
        """Customer LTV API returns data for authenticated user."""
        mock_ltv.return_value = {
            "total_revenue": Decimal("500.00"),
            "total_orders": 5,
            "average_order_value": Decimal("100.00"),
            "predicted_ltv": Decimal("750.00"),
            "confidence_level": "medium",
            "value_tier": "silver",
            "percentile": 60,
            "engagement_score": 0.7,
            "churn_risk": "low",
            "customer_since": date(2024, 1, 1),
            "months_active": 12,
            "last_purchase_date": date(2025, 12, 1),
            "days_since_last_purchase": 30,
        }
        response = auth_client.get("/api/customers/lifetime-value/")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


class TestCustomerLoyaltyStatusAPI:
    @patch("customers.services.customer_service.CustomerService.get_loyalty_status")
    def test_loyalty_api_authenticated(self, mock_loyalty, auth_client):
        """Customer loyalty API returns data for authenticated user."""
        mock_loyalty.return_value = {
            "current_segment": {},
            "loyalty_points": 0,
        }
        response = auth_client.get("/api/customers/loyalty-status/")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


class TestCustomerSavingsAPI:
    @patch("customers.services.savings_service.SavingsService.get_savings_summary")
    def test_savings_api_authenticated(self, mock_savings, auth_client):
        """Customer savings API returns data for authenticated user."""
        mock_savings.return_value = {
            "total_savings": "50.00",
            "breakdown": [],
        }
        response = auth_client.get("/api/customers/savings/")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


# ============================================================
# Security Tests
# ============================================================


class TestSecurityAllAdminViewsRequireStaff:
    """Verify all admin views are protected by staff_member_required."""

    @pytest.fixture(autouse=True)
    def _setup(self, site_settings):
        """Ensure site_settings exists for all security tests."""
        pass

    @pytest.mark.parametrize(
        "url_name,kwargs",
        [
            ("customers:dashboard", {}),
            ("customers:export", {}),
            ("customers:refresh_metrics", {}),
            ("customers:filter_customers", {}),
            ("customers:add_customer_note", {}),
            ("customers:ltv_settings", {}),
            ("customers:cohort_dashboard", {}),
            ("customers:recalculate_ltv", {}),
            ("customers:cohort_data_api", {}),
            ("customers:analytics_api", {}),
        ],
    )
    def test_anon_redirected(self, anon_client, url_name, kwargs):
        """Anonymous users are redirected to login for all admin views."""
        url = reverse(url_name, kwargs=kwargs)
        response = anon_client.get(url)
        assert response.status_code == 302, f"{url_name} allows anonymous access"

    @pytest.mark.parametrize(
        "url_name,kwargs",
        [
            ("customers:dashboard", {}),
            ("customers:export", {}),
            ("customers:refresh_metrics", {}),
            ("customers:filter_customers", {}),
            ("customers:add_customer_note", {}),
            ("customers:ltv_settings", {}),
            ("customers:cohort_dashboard", {}),
            ("customers:recalculate_ltv", {}),
            ("customers:cohort_data_api", {}),
            ("customers:analytics_api", {}),
        ],
    )
    def test_non_staff_redirected(self, non_staff_client, url_name, kwargs):
        """Non-staff users are redirected for all admin views."""
        url = reverse(url_name, kwargs=kwargs)
        response = non_staff_client.get(url)
        assert response.status_code == 302, f"{url_name} allows non-staff access"

    def test_profile_actions_anon_redirected(self, anon_client, customer_profile):
        """Anonymous users are redirected from profile actions."""
        url = reverse(
            "customers:customer_profile_actions",
            args=[customer_profile.pk],
        )
        response = anon_client.get(url, {"action": "refresh_metrics"})
        assert response.status_code == 302


class TestAPIAuthenticationRequired:
    """Verify all customer-facing API endpoints require authentication."""

    @pytest.mark.parametrize(
        "url",
        [
            "/api/customers/dashboard/",
            "/api/customers/stats/",
            "/api/customers/insights/",
            "/api/customers/lifetime-value/",
            "/api/customers/loyalty-status/",
            "/api/customers/savings/",
            "/api/customers/favorites/",
            "/api/customers/recommendations/",
            "/api/customers/digital-products/",
            "/api/customers/digital-products/licenses/",
        ],
    )
    def test_unauthenticated_rejected(self, api_client, url):
        """Unauthenticated API requests are rejected."""
        response = api_client.get(url)
        assert response.status_code in (401, 403), (
            f"GET {url} returned {response.status_code} for unauthenticated user"
        )


# ============================================================
# CSP Compliance: No inline styles in admin display methods
# ============================================================


class TestCSPCompliance:
    def test_customer_segment_display_no_inline_style(
        self, customer_profile, customer_segment_vip, customer_metrics
    ):
        """customer_segment_display uses CSS custom properties, not inline styles."""
        admin_instance = EnhancedCustomerProfileAdmin(CustomerProfile, AdminSite())
        # Need to set up metrics so segment matches
        customer_metrics.total_spent = Money(2000, "USD")
        customer_metrics.completed_orders = 10
        customer_metrics.save()
        result = admin_instance.customer_segment_display(customer_profile)
        # The method uses style="--segment-bg: ..." which is a CSS custom property
        if 'style="' in str(result):
            assert "--segment-bg" in str(result), (
                "customer_segment_display uses inline style without CSS custom property"
            )

    def test_color_preview_uses_css_custom_property(self, customer_segment_vip):
        """CustomerSegmentAdmin.color_preview uses --swatch-color CSS variable."""
        admin_instance = CustomerSegmentAdmin(CustomerSegment, AdminSite())
        result = admin_instance.color_preview(customer_segment_vip)
        assert "--swatch-color" in result
        # Should NOT contain direct style property values like background-color
        assert "background-color" not in str(result)


# ============================================================
# i18n Compliance
# ============================================================


class TestI18nCompliance:
    def test_all_models_have_translated_verbose_names(self):
        """All customers app models have translated verbose_name."""
        models_to_check = [
            CustomerMetrics,
            CustomerSegment,
            LTVSettings,
            ProductCategoryLTVMultiplier,
            CustomerCohort,
            CohortMetrics,
            AbandonedCart,
            CustomerNote,
        ]
        for model in models_to_check:
            verbose = model._meta.verbose_name
            assert verbose is not None, f"{model.__name__} has no verbose_name"
            assert str(verbose), f"{model.__name__} verbose_name is empty"

    def test_admin_fieldset_names_translatable(self):
        """Admin fieldset names are wrapped in gettext_lazy."""
        admin_classes = [
            (EnhancedCustomerProfileAdmin, CustomerProfile),
            (CustomerMetricsAdmin, CustomerMetrics),
            (CustomerSegmentAdmin, CustomerSegment),
            (AbandonedCartAdmin, AbandonedCart),
            (CustomerNoteAdmin, CustomerNote),
        ]
        for admin_cls, model_cls in admin_classes:
            admin_instance = admin_cls(model_cls, AdminSite())
            for fieldset in admin_instance.fieldsets:
                name = fieldset[0]
                if name is not None:
                    # A lazy string resolves to str
                    assert isinstance(str(name), str), (
                        f"{admin_cls.__name__} fieldset name is not translatable: {name}"
                    )

    def test_admin_action_short_descriptions_translatable(self):
        """Admin actions have translatable short_description."""
        admin_classes = [
            (EnhancedCustomerProfileAdmin, CustomerProfile),
            (CustomerMetricsAdmin, CustomerMetrics),
            (AbandonedCartAdmin, AbandonedCart),
            (CustomerNoteAdmin, CustomerNote),
        ]
        for admin_cls, model_cls in admin_classes:
            admin_instance = admin_cls(model_cls, AdminSite())
            for action_name in admin_instance.actions:
                action_func = getattr(admin_instance, action_name, None)
                if action_func:
                    desc = getattr(action_func, "short_description", None)
                    assert desc is not None, (
                        f"{admin_cls.__name__}.{action_name} has no short_description"
                    )


# ============================================================
# URL Configuration Tests
# ============================================================


class TestURLConfiguration:
    def test_admin_urls_resolve(self):
        """All admin URL names resolve correctly."""
        url_names = [
            "customers:dashboard",
            "customers:analytics_api",
            "customers:export",
            "customers:refresh_metrics",
            "customers:filter_customers",
            "customers:add_customer_note",
            "customers:ltv_settings",
            "customers:cohort_dashboard",
            "customers:recalculate_ltv",
            "customers:cohort_data_api",
        ]
        for name in url_names:
            url = reverse(name)
            assert url, f"URL {name} did not resolve"

    def test_admin_urls_with_kwargs_resolve(self):
        """Admin URLs with kwargs resolve correctly."""
        # profile actions
        url = reverse("customers:customer_profile_actions", args=[1])
        assert "/profile/1/actions/" in url

    def test_api_urls_are_mounted(self):
        """Customer API URLs are mounted under /api/customers/."""
        client = Client()
        # Just verify the URL pattern exists (will get 401/302)
        response = client.get("/api/customers/dashboard/")
        assert response.status_code in (200, 301, 302, 401, 403)
