"""
Tests for Subscription Models
"""

from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from djmoney.money import Money

from catalog.models import Category, Product
from component_updates.models import ComponentRegistry
from payment_providers.models import PaymentProviderAccount
from subscriptions.models import (
    BillingCycleLog,
    CustomerSubscription,
    PaymentToken,
    PlanPricingTier,
    SubscriptionPlan,
)

User = get_user_model()


def _ensure_site_settings():
    """Ensure Site 1 and default SiteSettings exist."""
    from django.contrib.sites.models import Site

    from core.models import SiteSettings

    if not Site.objects.filter(pk=1).exists():
        Site.objects.create(pk=1, domain="testserver", name="Test Site")

    SiteSettings.objects.get_or_create(
        pk=1,
        defaults={
            "admin_email": "admin@example.com",
            "default_currency": "USD",
            "enable_multi_warehouse": False,
        },
    )


def _make_provider_account(user, slug="stripe-test"):
    """Create a PaymentProviderAccount tied to a payment_provider ComponentRegistry."""
    component, _ = ComponentRegistry.objects.get_or_create(
        slug=slug,
        component_type="payment_provider",
        defaults={
            "name": f"Test Payment Provider ({slug})",
            "current_version": "1.0.0",
            "author": "Spwig",
            "description": "Test payment provider component",
        },
    )
    return PaymentProviderAccount.objects.create(
        component=component,
        user=user,
        display_name="Test Provider Account",
        is_active=True,
        checkout_mode="hosted",
        connection_status="connected",
    )


class SubscriptionPlanModelTest(TestCase):
    """Test SubscriptionPlan model."""

    def setUp(self):
        _ensure_site_settings()

    def test_create_subscription_plan(self):
        """A basic plan can be created and exposes the fields we assert on."""
        plan = SubscriptionPlan.objects.create(
            name="Monthly Premium",
            slug="monthly-premium",
            description="Premium subscription",
            pricing_model="tiered",
            is_active=True,
            is_public=True,
        )

        self.assertEqual(plan.name, "Monthly Premium")
        self.assertEqual(plan.slug, "monthly-premium")
        self.assertEqual(plan.pricing_model, "tiered")
        self.assertTrue(plan.is_active)
        self.assertTrue(plan.is_public)
        self.assertIsNotNone(plan.plan_id)

    def test_subscription_plan_with_trial(self):
        """Plans can have a trial period configuration."""
        plan = SubscriptionPlan.objects.create(
            name="Annual with Trial",
            slug="annual-trial",
            trial_period_days=30,
            trial_price=Money(Decimal("0.00"), "USD"),
            is_active=True,
        )

        self.assertEqual(plan.trial_period_days, 30)
        self.assertEqual(plan.trial_price.amount, Decimal("0.00"))

    def test_subscription_plan_with_setup_fee(self):
        """Plans can carry a one-time setup fee."""
        plan = SubscriptionPlan.objects.create(
            name="Enterprise",
            slug="enterprise",
            setup_fee=Money(Decimal("50.00"), "USD"),
            is_active=True,
        )

        self.assertEqual(plan.setup_fee.amount, Decimal("50.00"))

    def test_get_default_tier_returns_default_when_present(self):
        """`get_default_tier` prefers a tier marked as default."""
        plan = SubscriptionPlan.objects.create(
            name="Plan With Tiers",
            slug="plan-with-tiers",
        )
        PlanPricingTier.objects.create(
            plan=plan,
            tier_name="Monthly",
            billing_cycle="monthly",
            billing_interval=1,
            is_default=False,
        )
        default_tier = PlanPricingTier.objects.create(
            plan=plan,
            tier_name="Annual",
            billing_cycle="annual",
            billing_interval=1,
            is_default=True,
        )

        self.assertEqual(plan.get_default_tier(), default_tier)


class PlanPricingTierModelTest(TestCase):
    """Test PlanPricingTier model behavior."""

    def setUp(self):
        _ensure_site_settings()
        self.plan = SubscriptionPlan.objects.create(name="Tiered Plan", slug="tiered-plan")
        self.category = Category.objects.create(name="Test Category", slug="test-category-tier")
        self.product = Product.objects.create(
            name="Test Product",
            slug="test-product-tier",
            sku="TIER-SKU-001",
            price=Money(Decimal("100.00"), "USD"),
            category=self.category,
        )

    def test_calculate_price_applies_discount(self):
        """`calculate_price` applies the tier's discount to the product price."""
        tier = PlanPricingTier.objects.create(
            plan=self.plan,
            tier_name="Annual - Save 20%",
            billing_cycle="annual",
            billing_interval=1,
            discount_percentage=Decimal("20.00"),
        )

        price = tier.calculate_price(self.product)
        self.assertEqual(price.amount, Decimal("80.00"))
        self.assertEqual(str(price.currency), "USD")


class PaymentTokenModelTest(TestCase):
    """Test PaymentToken model."""

    def setUp(self):
        _ensure_site_settings()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.provider_account = _make_provider_account(self.user, slug="stripe-tokens")

    def test_create_payment_token(self):
        """A payment token can be created and links back to its provider account."""
        token = PaymentToken.objects.create(
            user=self.user,
            provider_account=self.provider_account,
            gateway_customer_id="cus_test123",
            gateway_token_id="pm_test123",
            payment_method_type="card",
            card_brand="visa",
            card_last4="4242",
            card_exp_month=12,
            card_exp_year=2099,
            is_active=True,
            is_verified=True,
        )

        self.assertEqual(token.user, self.user)
        self.assertEqual(token.provider_account, self.provider_account)
        self.assertEqual(token.card_last4, "4242")
        self.assertIsNotNone(token.token_id)

    def test_payment_token_is_expired(self):
        """`is_expired()` returns True for past cards and False for future ones."""
        expired_token = PaymentToken.objects.create(
            user=self.user,
            provider_account=self.provider_account,
            gateway_customer_id="cus_test123",
            gateway_token_id="pm_test123",
            payment_method_type="card",
            card_brand="visa",
            card_last4="4242",
            card_exp_month=1,
            card_exp_year=2020,
            is_active=True,
        )

        self.assertTrue(expired_token.is_expired())

        valid_token = PaymentToken.objects.create(
            user=self.user,
            provider_account=self.provider_account,
            gateway_customer_id="cus_test456",
            gateway_token_id="pm_test456",
            payment_method_type="card",
            card_brand="mastercard",
            card_last4="5555",
            card_exp_month=12,
            card_exp_year=timezone.now().year + 5,
            is_active=True,
        )

        self.assertFalse(valid_token.is_expired())

    def test_non_card_token_is_never_expired(self):
        """Non-card payment method types are never reported as expired."""
        token = PaymentToken.objects.create(
            user=self.user,
            provider_account=self.provider_account,
            gateway_customer_id="cus_test789",
            gateway_token_id="pm_test789",
            payment_method_type="paypal",
            is_active=True,
        )
        self.assertFalse(token.is_expired())

    def test_set_default_payment_token(self):
        """Manually flipping default flags is persisted on refresh."""
        token1 = PaymentToken.objects.create(
            user=self.user,
            provider_account=self.provider_account,
            gateway_customer_id="cus_test123",
            gateway_token_id="pm_test123",
            payment_method_type="card",
            is_active=True,
            is_default=True,
        )

        token2 = PaymentToken.objects.create(
            user=self.user,
            provider_account=self.provider_account,
            gateway_customer_id="cus_test456",
            gateway_token_id="pm_test456",
            payment_method_type="card",
            is_active=True,
            is_default=False,
        )

        PaymentToken.objects.filter(user=self.user).update(is_default=False)
        token2.is_default = True
        token2.save()

        token1.refresh_from_db()
        token2.refresh_from_db()

        self.assertFalse(token1.is_default)
        self.assertTrue(token2.is_default)


class CustomerSubscriptionModelTest(TestCase):
    """Test CustomerSubscription model."""

    def setUp(self):
        _ensure_site_settings()

        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        self.provider_account = _make_provider_account(self.user, slug="stripe-subs")

        self.plan = SubscriptionPlan.objects.create(
            name="Monthly Plan",
            slug="monthly-plan",
            is_active=True,
        )

        self.tier = PlanPricingTier.objects.create(
            plan=self.plan,
            tier_name="Monthly",
            billing_cycle="monthly",
            billing_interval=1,
            is_default=True,
        )

        self.token = PaymentToken.objects.create(
            user=self.user,
            provider_account=self.provider_account,
            gateway_customer_id="cus_test123",
            gateway_token_id="pm_test123",
            payment_method_type="card",
            is_active=True,
        )

        self.category = Category.objects.create(name="Sub Category", slug="sub-category")
        self.product = Product.objects.create(
            name="Test Sub Product",
            slug="test-sub-product",
            sku="SUB-TEST-001",
            price=Money(Decimal("29.99"), "USD"),
            category=self.category,
            is_subscription_enabled=True,
        )

    def _make_subscription(self, **overrides):
        now = timezone.now()
        defaults = {
            "user": self.user,
            "plan": self.plan,
            "pricing_tier": self.tier,
            "product": self.product,
            "payment_provider_account": self.provider_account,
            "payment_token": self.token,
            "provider_mode": "native",
            "status": "active",
            "current_period_start": now,
            "current_period_end": now + timedelta(days=30),
            "next_billing_date": now + timedelta(days=30),
        }
        defaults.update(overrides)
        return CustomerSubscription.objects.create(**defaults)

    def test_create_subscription(self):
        """A subscription can be created against the current FK layout."""
        subscription = self._make_subscription()

        self.assertEqual(subscription.user, self.user)
        self.assertEqual(subscription.plan, self.plan)
        self.assertEqual(subscription.pricing_tier, self.tier)
        self.assertEqual(subscription.product, self.product)
        self.assertEqual(subscription.payment_provider_account, self.provider_account)
        self.assertEqual(subscription.status, "active")
        self.assertIsNotNone(subscription.subscription_id)

    def test_subscription_days_until_next_billing(self):
        """`days_until_next_billing` returns the whole-day delta to `next_billing_date`."""
        now = timezone.now()
        next_billing = now + timedelta(days=15)
        subscription = self._make_subscription(
            current_period_start=now,
            current_period_end=next_billing,
            next_billing_date=next_billing,
        )

        days = subscription.days_until_next_billing()
        self.assertIsNotNone(days)
        self.assertGreaterEqual(days, 14)
        self.assertLessEqual(days, 15)

    def test_subscription_days_until_next_billing_none(self):
        """Without a next_billing_date the method returns None."""
        subscription = self._make_subscription(next_billing_date=None)
        self.assertIsNone(subscription.days_until_next_billing())

    def test_subscription_total_amount_paid(self):
        """`total_amount_paid` sums successful billing logs' `total_amount`."""
        subscription = self._make_subscription()

        BillingCycleLog.objects.create(
            subscription=subscription,
            cycle_number=1,
            billing_date=timezone.now() - timedelta(days=30),
            base_amount=Money(Decimal("29.99"), "USD"),
            total_amount=Money(Decimal("29.99"), "USD"),
            status="successful",
        )

        BillingCycleLog.objects.create(
            subscription=subscription,
            cycle_number=2,
            billing_date=timezone.now(),
            base_amount=Money(Decimal("29.99"), "USD"),
            total_amount=Money(Decimal("29.99"), "USD"),
            status="successful",
        )

        total = subscription.total_amount_paid()
        self.assertEqual(Decimal(str(total)), Decimal("59.98"))

    def test_subscription_can_reactivate(self):
        """`can_reactivate()` is only True for canceled subs before the deadline."""
        now = timezone.now()
        subscription = self._make_subscription(
            status="canceled",
            canceled_at=now,
            reactivation_deadline=now + timedelta(days=7),
        )
        self.assertTrue(subscription.can_reactivate())

        # Expired reactivation window
        subscription.reactivation_deadline = now - timedelta(days=1)
        subscription.save(update_fields=["reactivation_deadline"])
        self.assertFalse(subscription.can_reactivate())

    def test_active_subscription_cannot_be_reactivated(self):
        """Active subscriptions never report `can_reactivate() == True`."""
        subscription = self._make_subscription(status="active")
        self.assertFalse(subscription.can_reactivate())


class BillingCycleLogModelTest(TestCase):
    """Test BillingCycleLog model."""

    def setUp(self):
        _ensure_site_settings()

        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.provider_account = _make_provider_account(self.user, slug="stripe-billing")

        self.plan = SubscriptionPlan.objects.create(
            name="Monthly Plan",
            slug="monthly-plan",
            is_active=True,
        )
        self.tier = PlanPricingTier.objects.create(
            plan=self.plan,
            tier_name="Monthly",
            billing_cycle="monthly",
            billing_interval=1,
            is_default=True,
        )

        self.token = PaymentToken.objects.create(
            user=self.user,
            provider_account=self.provider_account,
            gateway_customer_id="cus_test123",
            gateway_token_id="pm_test123",
            payment_method_type="card",
            is_active=True,
        )

        self.category = Category.objects.create(name="Billing Category", slug="billing-category")
        self.product = Product.objects.create(
            name="Billing Product",
            slug="billing-product",
            sku="BILL-TEST-001",
            price=Money(Decimal("29.99"), "USD"),
            category=self.category,
        )

        now = timezone.now()
        self.subscription = CustomerSubscription.objects.create(
            user=self.user,
            plan=self.plan,
            pricing_tier=self.tier,
            product=self.product,
            payment_provider_account=self.provider_account,
            payment_token=self.token,
            provider_mode="native",
            status="active",
            current_period_start=now,
            current_period_end=now + timedelta(days=30),
            next_billing_date=now + timedelta(days=30),
        )

    def test_create_billing_log_success(self):
        """A successful billing log stores the correct total and status."""
        log = BillingCycleLog.objects.create(
            subscription=self.subscription,
            cycle_number=1,
            billing_date=timezone.now(),
            base_amount=Money(Decimal("29.99"), "USD"),
            total_amount=Money(Decimal("29.99"), "USD"),
            status="successful",
        )

        self.assertEqual(log.subscription, self.subscription)
        self.assertEqual(log.cycle_number, 1)
        self.assertEqual(log.status, "successful")
        self.assertEqual(log.total_amount.amount, Decimal("29.99"))

    def test_create_billing_log_failed(self):
        """A failed billing log stores error metadata."""
        log = BillingCycleLog.objects.create(
            subscription=self.subscription,
            cycle_number=1,
            billing_date=timezone.now(),
            base_amount=Money(Decimal("29.99"), "USD"),
            total_amount=Money(Decimal("29.99"), "USD"),
            status="failed",
            error_code="card_declined",
            error_message="Your card was declined.",
        )

        self.assertEqual(log.status, "failed")
        self.assertEqual(log.error_code, "card_declined")
        self.assertIn("declined", log.error_message)

    def test_can_retry_failed_within_max_retries(self):
        """`can_retry()` is True for a failed log below the max retry ceiling."""
        log = BillingCycleLog.objects.create(
            subscription=self.subscription,
            cycle_number=1,
            billing_date=timezone.now(),
            base_amount=Money(Decimal("29.99"), "USD"),
            total_amount=Money(Decimal("29.99"), "USD"),
            status="failed",
            retry_count=1,
            max_retries=3,
        )
        self.assertTrue(log.can_retry())

    def test_can_retry_false_when_retries_exhausted(self):
        """`can_retry()` returns False once retries are exhausted."""
        log = BillingCycleLog.objects.create(
            subscription=self.subscription,
            cycle_number=2,
            billing_date=timezone.now(),
            base_amount=Money(Decimal("29.99"), "USD"),
            total_amount=Money(Decimal("29.99"), "USD"),
            status="failed",
            retry_count=3,
            max_retries=3,
        )
        self.assertFalse(log.can_retry())
