"""
Tests for Subscription API Endpoints
"""
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
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


class SubscriptionPlanAPITest(APITestCase):
    """Test Subscription Plan API endpoints"""

    def setUp(self):
        """Set up test data"""
        self.client = APIClient()

        # Create site settings
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

        # Create plans
        self.plan1 = SubscriptionPlan.objects.create(
            name='Monthly Basic',
            slug='monthly-basic',
            description='Basic monthly subscription',
            billing_cycle='month',
            billing_interval=1,
            price=Money(9.99, 'USD'),
            is_active=True,
            is_public=True
        )

        self.plan2 = SubscriptionPlan.objects.create(
            name='Annual Pro',
            slug='annual-pro',
            description='Professional annual subscription',
            billing_cycle='year',
            billing_interval=1,
            price=Money(99.99, 'USD'),
            trial_period_days=14,
            is_active=True,
            is_public=True
        )

        self.inactive_plan = SubscriptionPlan.objects.create(
            name='Discontinued Plan',
            slug='discontinued',
            billing_cycle='month',
            billing_interval=1,
            price=Money(19.99, 'USD'),
            is_active=False,
            is_public=False
        )

    def test_list_subscription_plans(self):
        """Test listing all active, public subscription plans"""
        url = reverse('subscriptions_api:plan-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Only active, public plans

    def test_retrieve_subscription_plan(self):
        """Test retrieving a specific subscription plan"""
        url = reverse('subscriptions_api:plan-detail', kwargs={'plan_id': self.plan1.plan_id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Monthly Basic')
        self.assertEqual(response.data['billing_cycle'], 'month')

    def test_retrieve_inactive_plan_fails(self):
        """Test that inactive plans cannot be retrieved"""
        url = reverse('subscriptions_api:plan-detail', kwargs={'plan_id': self.inactive_plan.plan_id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PaymentTokenAPITest(APITestCase):
    """Test Payment Token API endpoints"""

    def setUp(self):
        """Set up test data"""
        self.client = APIClient()

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

        # Create users
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )

        # Create gateway
        self.gateway = PaymentGateway.objects.create(
            name='stripe',
            display_name='Test Gateway',
            is_active=True,
            supports_recurring=True
        )

        # Create tokens
        self.token = PaymentToken.objects.create(
            user=self.user,
            gateway=self.gateway,
            gateway_customer_id='cus_test123',
            gateway_token_id='pm_test123',
            payment_method_type='card',
            card_brand='visa',
            card_last4='4242',
            is_active=True
        )

        self.other_token = PaymentToken.objects.create(
            user=self.other_user,
            gateway=self.gateway,
            gateway_customer_id='cus_test456',
            gateway_token_id='pm_test456',
            payment_method_type='card',
            card_brand='mastercard',
            card_last4='5555',
            is_active=True
        )

    def test_list_payment_tokens_authenticated(self):
        """Test listing payment tokens for authenticated user"""
        self.client.force_authenticate(user=self.user)
        url = reverse('subscriptions_api:token-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Only user's tokens
        self.assertEqual(response.data['results'][0]['card_last4'], '4242')

    def test_list_payment_tokens_unauthenticated(self):
        """Test that unauthenticated users cannot list tokens"""
        url = reverse('subscriptions_api:token-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_own_payment_token(self):
        """Test retrieving own payment token"""
        self.client.force_authenticate(user=self.user)
        url = reverse('subscriptions_api:token-detail', kwargs={'token_id': self.token.token_id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['card_last4'], '4242')

    def test_retrieve_other_user_token_fails(self):
        """Test that users cannot access other users' tokens"""
        self.client.force_authenticate(user=self.user)
        url = reverse('subscriptions_api:token-detail', kwargs={'token_id': self.other_token.token_id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CustomerSubscriptionAPITest(APITestCase):
    """Test Customer Subscription API endpoints"""

    def setUp(self):
        """Set up test data"""
        self.client = APIClient()

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

        # Create user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        # Create gateway
        self.gateway = PaymentGateway.objects.create(
            name='stripe',
            display_name='Test Gateway',
            is_active=True,
            supports_recurring=True
        )

        # Create plan
        self.plan = SubscriptionPlan.objects.create(
            name='Monthly Plan',
            slug='monthly-plan',
            billing_cycle='month',
            billing_interval=1,
            price=Money(29.99, 'USD'),
            is_active=True
        )

        # Create token
        self.token = PaymentToken.objects.create(
            user=self.user,
            gateway=self.gateway,
            gateway_customer_id='cus_test123',
            gateway_token_id='pm_test123',
            payment_method_type='card',
            is_active=True
        )

        # Create product
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

        # Create subscription
        self.subscription = CustomerSubscription.objects.create(
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

    def test_list_subscriptions_authenticated(self):
        """Test listing subscriptions for authenticated user"""
        self.client.force_authenticate(user=self.user)
        url = reverse('subscriptions_api:subscription-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_list_subscriptions_unauthenticated(self):
        """Test that unauthenticated users cannot list subscriptions"""
        url = reverse('subscriptions_api:subscription-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_subscription(self):
        """Test retrieving a specific subscription"""
        self.client.force_authenticate(user=self.user)
        url = reverse('subscriptions_api:subscription-detail', 
                     kwargs={'subscription_id': self.subscription.subscription_id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'active')
        self.assertEqual(response.data['plan']['name'], 'Monthly Plan')

    def test_filter_subscriptions_by_status(self):
        """Test filtering subscriptions by status"""
        # Create another subscription with different status
        now = timezone.now()
        canceled_subscription = CustomerSubscription.objects.create(
            user=self.user,
            plan=self.plan,
            product=self.product,
            payment_gateway=self.gateway,
            payment_token=self.token,
            provider_mode='native',
            status='canceled',
            current_period_start=now - timedelta(days=30),
            current_period_end=now,
            next_billing_date=now,
            canceled_at=now
        )

        self.client.force_authenticate(user=self.user)
        url = reverse('subscriptions_api:subscription-list') + '?status=active'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['status'], 'active')

    def test_get_billing_history(self):
        """Test getting billing history for a subscription"""
        # Create billing logs
        BillingCycleLog.objects.create(
            subscription=self.subscription,
            cycle_number=1,
            billing_date=timezone.now() - timedelta(days=30),
            amount=Money(29.99, 'USD'),
            status='successful'
        )

        BillingCycleLog.objects.create(
            subscription=self.subscription,
            cycle_number=2,
            billing_date=timezone.now(),
            amount=Money(29.99, 'USD'),
            status='successful'
        )

        self.client.force_authenticate(user=self.user)
        url = reverse('subscriptions_api:subscription-billing-history',
                     kwargs={'subscription_id': self.subscription.subscription_id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['status'], 'successful')
