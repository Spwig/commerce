"""
Tests for Subscription Models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta
from djmoney.money import Money

from subscriptions.models import (
    SubscriptionPlan, PaymentToken, CustomerSubscription, BillingCycleLog
)
from catalog.models import Product, Category
from payment_providers.models import PaymentGateway

User = get_user_model()


class SubscriptionPlanModelTest(TestCase):
    """Test SubscriptionPlan model"""

    def setUp(self):
        """Set up test data"""
        from django.contrib.sites.models import Site
        from core.models import SiteSettings

        # Ensure Site exists
        if not Site.objects.filter(pk=1).exists():
            Site.objects.create(pk=1, domain='testserver', name='Test Site')

        SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                'admin_email': 'admin@example.com',
                'default_currency': 'USD',
                'enable_multi_warehouse': False
            }
        )

    def test_create_subscription_plan(self):
        """Test creating a subscription plan"""
        plan = SubscriptionPlan.objects.create(
            name='Monthly Premium',
            slug='monthly-premium',
            description='Premium subscription billed monthly',
            billing_cycle='month',
            billing_interval=1,
            price=Money(19.99, 'USD'),
            is_active=True,
            is_public=True
        )

        self.assertEqual(plan.name, 'Monthly Premium')
        self.assertEqual(plan.billing_cycle, 'month')
        self.assertEqual(plan.price.amount, Decimal('19.99'))
        self.assertTrue(plan.is_active)
        self.assertIsNotNone(plan.plan_id)

    def test_subscription_plan_with_trial(self):
        """Test subscription plan with trial period"""
        plan = SubscriptionPlan.objects.create(
            name='Annual with Trial',
            slug='annual-trial',
            billing_cycle='year',
            billing_interval=1,
            price=Money(199.99, 'USD'),
            trial_period_days=30,
            trial_price=Money(0, 'USD'),
            is_active=True
        )

        self.assertEqual(plan.trial_period_days, 30)
        self.assertEqual(plan.trial_price.amount, Decimal('0'))

    def test_subscription_plan_with_setup_fee(self):
        """Test subscription plan with setup fee"""
        plan = SubscriptionPlan.objects.create(
            name='Enterprise',
            slug='enterprise',
            billing_cycle='month',
            billing_interval=1,
            price=Money(99.99, 'USD'),
            setup_fee=Money(50.00, 'USD'),
            is_active=True
        )

        self.assertEqual(plan.setup_fee.amount, Decimal('50.00'))


class PaymentTokenModelTest(TestCase):
    """Test PaymentToken model"""

    def setUp(self):
        """Set up test data"""
        from django.contrib.sites.models import Site
        from core.models import SiteSettings

        if not Site.objects.filter(pk=1).exists():
            Site.objects.create(pk=1, domain='testserver', name='Test Site')

        SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                'admin_email': 'admin@example.com',
                'default_currency': 'USD'
            }
        )

        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        self.gateway = PaymentGateway.objects.create(
            name='stripe',
            display_name='Test Gateway',
            is_active=True,
            supports_recurring=True
        )

    def test_create_payment_token(self):
        """Test creating a payment token"""
        token = PaymentToken.objects.create(
            user=self.user,
            gateway=self.gateway,
            gateway_customer_id='cus_test123',
            gateway_token_id='pm_test123',
            payment_method_type='card',
            card_brand='visa',
            card_last4='4242',
            card_exp_month=12,
            card_exp_year=2025,
            is_active=True,
            is_verified=True
        )

        self.assertEqual(token.user, self.user)
        self.assertEqual(token.gateway, self.gateway)
        self.assertEqual(token.card_last4, '4242')
        self.assertIsNotNone(token.token_id)

    def test_payment_token_is_expired(self):
        """Test payment token expiration check"""
        # Create expired card
        expired_token = PaymentToken.objects.create(
            user=self.user,
            gateway=self.gateway,
            gateway_customer_id='cus_test123',
            gateway_token_id='pm_test123',
            payment_method_type='card',
            card_brand='visa',
            card_last4='4242',
            card_exp_month=1,
            card_exp_year=2020,
            is_active=True
        )

        self.assertTrue(expired_token.is_expired())

        # Create valid card
        valid_token = PaymentToken.objects.create(
            user=self.user,
            gateway=self.gateway,
            gateway_customer_id='cus_test456',
            gateway_token_id='pm_test456',
            payment_method_type='card',
            card_brand='mastercard',
            card_last4='5555',
            card_exp_month=12,
            card_exp_year=2030,
            is_active=True
        )

        self.assertFalse(valid_token.is_expired())

    def test_set_default_payment_token(self):
        """Test setting a payment token as default"""
        token1 = PaymentToken.objects.create(
            user=self.user,
            gateway=self.gateway,
            gateway_customer_id='cus_test123',
            gateway_token_id='pm_test123',
            payment_method_type='card',
            is_active=True,
            is_default=True
        )

        token2 = PaymentToken.objects.create(
            user=self.user,
            gateway=self.gateway,
            gateway_customer_id='cus_test456',
            gateway_token_id='pm_test456',
            payment_method_type='card',
            is_active=True,
            is_default=False
        )

        # Set token2 as default
        PaymentToken.objects.filter(user=self.user).update(is_default=False)
        token2.is_default = True
        token2.save()

        # Refresh from DB
        token1.refresh_from_db()
        token2.refresh_from_db()

        self.assertFalse(token1.is_default)
        self.assertTrue(token2.is_default)


class CustomerSubscriptionModelTest(TestCase):
    """Test CustomerSubscription model"""

    def setUp(self):
        """Set up test data"""
        from django.contrib.sites.models import Site
        from core.models import SiteSettings

        if not Site.objects.filter(pk=1).exists():
            Site.objects.create(pk=1, domain='testserver', name='Test Site')

        SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                'admin_email': 'admin@example.com',
                'default_currency': 'USD'
            }
        )

        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        self.gateway = PaymentGateway.objects.create(
            name='stripe',
            display_name='Test Gateway',
            is_active=True,
            supports_recurring=True
        )

        self.plan = SubscriptionPlan.objects.create(
            name='Monthly Plan',
            slug='monthly-plan',
            billing_cycle='month',
            billing_interval=1,
            price=Money(29.99, 'USD'),
            is_active=True
        )

        self.token = PaymentToken.objects.create(
            user=self.user,
            gateway=self.gateway,
            gateway_customer_id='cus_test123',
            gateway_token_id='pm_test123',
            payment_method_type='card',
            is_active=True
        )

        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )

        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            sku='TEST-001',
            price=Money(29.99, 'USD'),
            category=self.category,
            is_subscription_enabled=True
        )

    def test_create_subscription(self):
        """Test creating a customer subscription"""
        subscription = CustomerSubscription.objects.create(
            user=self.user,
            plan=self.plan,
            product=self.product,
            payment_gateway=self.gateway,
            payment_token=self.token,
            provider_mode='native',
            status='active',
            current_period_start=timezone.now(),
            current_period_end=timezone.now() + timedelta(days=30),
            next_billing_date=timezone.now() + timedelta(days=30)
        )

        self.assertEqual(subscription.user, self.user)
        self.assertEqual(subscription.plan, self.plan)
        self.assertEqual(subscription.product, self.product)
        self.assertEqual(subscription.status, 'active')
        self.assertIsNotNone(subscription.subscription_id)

    def test_subscription_days_until_next_billing(self):
        """Test days until next billing calculation"""
        now = timezone.now()
        next_billing = now + timedelta(days=15)
        subscription = CustomerSubscription.objects.create(
            user=self.user,
            plan=self.plan,
            product=self.product,
            payment_gateway=self.gateway,
            payment_token=self.token,
            provider_mode='native',
            status='active',
            current_period_start=now,
            current_period_end=next_billing,
            next_billing_date=next_billing
        )

        days = subscription.days_until_next_billing()
        self.assertIsNotNone(days)
        self.assertGreaterEqual(days, 14)
        self.assertLessEqual(days, 16)

    def test_subscription_total_amount_paid(self):
        """Test total amount paid calculation"""
        now = timezone.now()
        subscription = CustomerSubscription.objects.create(
            user=self.user,
            plan=self.plan,
            product=self.product,
            payment_gateway=self.gateway,
            payment_token=self.token,
            provider_mode='native',
            status='active',
            current_period_start=now,
            current_period_end=now + timedelta(days=30),
            next_billing_date=now + timedelta(days=30)
        )

        # Create billing logs
        BillingCycleLog.objects.create(
            subscription=subscription,
            cycle_number=1,
            billing_date=timezone.now() - timedelta(days=30),
            amount=Money(29.99, 'USD'),
            status='successful'
        )

        BillingCycleLog.objects.create(
            subscription=subscription,
            cycle_number=2,
            billing_date=timezone.now(),
            amount=Money(29.99, 'USD'),
            status='successful'
        )

        total = subscription.total_amount_paid()
        self.assertEqual(total, Decimal('59.98'))


class BillingCycleLogModelTest(TestCase):
    """Test BillingCycleLog model"""

    def setUp(self):
        """Set up test data"""
        from django.contrib.sites.models import Site
        from core.models import SiteSettings

        if not Site.objects.filter(pk=1).exists():
            Site.objects.create(pk=1, domain='testserver', name='Test Site')

        SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                'admin_email': 'admin@example.com',
                'default_currency': 'USD'
            }
        )

        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        self.gateway = PaymentGateway.objects.create(
            name='stripe',
            display_name='Test Gateway',
            is_active=True,
            supports_recurring=True
        )

        self.plan = SubscriptionPlan.objects.create(
            name='Monthly Plan',
            slug='monthly-plan',
            billing_cycle='month',
            billing_interval=1,
            price=Money(29.99, 'USD'),
            is_active=True
        )

        self.token = PaymentToken.objects.create(
            user=self.user,
            gateway=self.gateway,
            gateway_customer_id='cus_test123',
            gateway_token_id='pm_test123',
            payment_method_type='card',
            is_active=True
        )

        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )

        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            sku='TEST-001',
            price=Money(29.99, 'USD'),
            category=self.category
        )

        now = timezone.now()
        self.subscription = CustomerSubscription.objects.create(
            user=self.user,
            plan=self.plan,
            product=self.product,
            payment_gateway=self.gateway,
            payment_token=self.token,
            provider_mode='native',
            status='active',
            current_period_start=now,
            current_period_end=now + timedelta(days=30),
            next_billing_date=now + timedelta(days=30)
        )

    def test_create_billing_log_success(self):
        """Test creating a successful billing log"""
        log = BillingCycleLog.objects.create(
            subscription=self.subscription,
            cycle_number=1,
            billing_date=timezone.now(),
            amount=Money(29.99, 'USD'),
            status='successful'
        )

        self.assertEqual(log.subscription, self.subscription)
        self.assertEqual(log.cycle_number, 1)
        self.assertEqual(log.status, 'successful')
        self.assertEqual(log.amount.amount, Decimal('29.99'))

    def test_create_billing_log_failed(self):
        """Test creating a failed billing log"""
        log = BillingCycleLog.objects.create(
            subscription=self.subscription,
            cycle_number=1,
            billing_date=timezone.now(),
            amount=Money(29.99, 'USD'),
            status='failed',
            error_code='card_declined',
            error_message='Your card was declined.'
        )

        self.assertEqual(log.status, 'failed')
        self.assertEqual(log.error_code, 'card_declined')
        self.assertIsNotNone(log.error_message)
