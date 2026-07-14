"""
Tests for Subscription API Endpoints
"""
from datetime import timedelta
from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from djmoney.money import Money
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

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
        Site.objects.create(pk=1, domain='testserver', name='Test Site')

    SiteSettings.objects.get_or_create(
        pk=1,
        defaults={
            'admin_email': 'admin@example.com',
            'default_currency': 'USD',
        },
    )


def _make_provider_account(user, slug='stripe-api'):
    """Create a PaymentProviderAccount tied to a payment_provider ComponentRegistry."""
    component, _ = ComponentRegistry.objects.get_or_create(
        slug=slug,
        component_type='payment_provider',
        defaults={
            'name': f'Test Payment Provider ({slug})',
            'current_version': '1.0.0',
            'author': 'Spwig',
            'description': 'Test payment provider component',
        },
    )
    return PaymentProviderAccount.objects.create(
        component=component,
        user=user,
        display_name='Test Provider Account',
        is_active=True,
        checkout_mode='hosted',
        connection_status='connected',
    )


class SubscriptionPlanAPITest(APITestCase):
    """Test Subscription Plan API endpoints (read-only ViewSet)."""

    def setUp(self):
        self.client = APIClient()
        _ensure_site_settings()

        self.plan1 = SubscriptionPlan.objects.create(
            name='Monthly Basic',
            slug='monthly-basic',
            description='Basic monthly subscription',
            is_active=True,
            is_public=True,
        )
        PlanPricingTier.objects.create(
            plan=self.plan1,
            tier_name='Monthly',
            billing_cycle='monthly',
            billing_interval=1,
            is_default=True,
        )

        self.plan2 = SubscriptionPlan.objects.create(
            name='Annual Pro',
            slug='annual-pro',
            description='Professional annual subscription',
            trial_period_days=14,
            is_active=True,
            is_public=True,
        )
        PlanPricingTier.objects.create(
            plan=self.plan2,
            tier_name='Annual',
            billing_cycle='annual',
            billing_interval=1,
            is_default=True,
        )

        self.inactive_plan = SubscriptionPlan.objects.create(
            name='Discontinued Plan',
            slug='discontinued',
            is_active=False,
            is_public=False,
        )

    def test_list_subscription_plans(self):
        """The list endpoint returns only active + public plans for anonymous users."""
        url = reverse('subscriptions_api:plan-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 2)
        slugs = {plan['slug'] for plan in results}
        self.assertSetEqual(slugs, {'monthly-basic', 'annual-pro'})

    def test_retrieve_subscription_plan(self):
        """The detail endpoint returns the plan payload keyed by `plan_id`."""
        url = reverse(
            'subscriptions_api:plan-detail', kwargs={'plan_id': self.plan1.plan_id}
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Monthly Basic')
        self.assertEqual(response.data['slug'], 'monthly-basic')
        # pricing_tiers is nested in the response.
        self.assertEqual(len(response.data['pricing_tiers']), 1)
        self.assertEqual(response.data['pricing_tiers'][0]['tier_name'], 'Monthly')

    def test_retrieve_inactive_plan_fails(self):
        """Inactive/private plans are not visible to anonymous users."""
        url = reverse(
            'subscriptions_api:plan-detail',
            kwargs={'plan_id': self.inactive_plan.plan_id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_staff_can_see_inactive_plans(self):
        """Staff users can retrieve inactive or private plans."""
        staff = User.objects.create_user(
            username='staff', email='staff@example.com', password='pw', is_staff=True
        )
        self.client.force_authenticate(user=staff)

        url = reverse(
            'subscriptions_api:plan-detail',
            kwargs={'plan_id': self.inactive_plan.plan_id},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PaymentTokenAPITest(APITestCase):
    """Test Payment Token API endpoints."""

    def setUp(self):
        self.client = APIClient()
        _ensure_site_settings()

        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser', email='other@example.com', password='testpass123'
        )

        self.provider_account = _make_provider_account(self.user, slug='stripe-user')
        self.other_provider_account = _make_provider_account(
            self.other_user, slug='stripe-other'
        )

        self.token = PaymentToken.objects.create(
            user=self.user,
            provider_account=self.provider_account,
            gateway_customer_id='cus_test123',
            gateway_token_id='pm_test123',
            payment_method_type='card',
            card_brand='visa',
            card_last4='4242',
            is_active=True,
        )

        self.other_token = PaymentToken.objects.create(
            user=self.other_user,
            provider_account=self.other_provider_account,
            gateway_customer_id='cus_test456',
            gateway_token_id='pm_test456',
            payment_method_type='card',
            card_brand='mastercard',
            card_last4='5555',
            is_active=True,
        )

    def test_list_payment_tokens_authenticated(self):
        """A user sees only their own tokens in the list endpoint."""
        self.client.force_authenticate(user=self.user)
        url = reverse('subscriptions_api:token-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['card_last4'], '4242')

    def test_list_payment_tokens_unauthenticated(self):
        """Unauthenticated requests to the token list are rejected."""
        url = reverse('subscriptions_api:token-list')
        response = self.client.get(url)

        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )

    def test_retrieve_own_payment_token(self):
        """A user can retrieve their own token by id."""
        self.client.force_authenticate(user=self.user)
        url = reverse(
            'subscriptions_api:token-detail', kwargs={'token_id': self.token.token_id}
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['card_last4'], '4242')

    def test_retrieve_other_user_token_fails(self):
        """A user cannot retrieve another user's token."""
        self.client.force_authenticate(user=self.user)
        url = reverse(
            'subscriptions_api:token-detail',
            kwargs={'token_id': self.other_token.token_id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CustomerSubscriptionAPITest(APITestCase):
    """Test Customer Subscription API endpoints."""

    def setUp(self):
        self.client = APIClient()
        _ensure_site_settings()

        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpass123'
        )

        self.provider_account = _make_provider_account(self.user, slug='stripe-cs')

        self.plan = SubscriptionPlan.objects.create(
            name='Monthly Plan', slug='monthly-plan', is_active=True
        )
        self.tier = PlanPricingTier.objects.create(
            plan=self.plan,
            tier_name='Monthly',
            billing_cycle='monthly',
            billing_interval=1,
            is_default=True,
        )

        self.token = PaymentToken.objects.create(
            user=self.user,
            provider_account=self.provider_account,
            gateway_customer_id='cus_test123',
            gateway_token_id='pm_test123',
            payment_method_type='card',
            is_active=True,
        )

        self.category = Category.objects.create(
            name='API Category', slug='api-category'
        )
        self.product = Product.objects.create(
            name='API Sub Product',
            slug='api-sub-product',
            sku='API-SUB-001',
            price=Money(Decimal('29.99'), 'USD'),
            category=self.category,
            is_subscription_enabled=True,
        )

        now = timezone.now()
        self.subscription = CustomerSubscription.objects.create(
            user=self.user,
            plan=self.plan,
            pricing_tier=self.tier,
            product=self.product,
            payment_provider_account=self.provider_account,
            payment_token=self.token,
            provider_mode='native',
            status='active',
            current_period_start=now,
            current_period_end=now + timedelta(days=30),
            next_billing_date=now + timedelta(days=30),
        )

    def test_list_subscriptions_unauthenticated(self):
        """The subscription list requires authentication."""
        url = reverse('subscriptions_api:subscription-list')
        response = self.client.get(url)

        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )

    def test_get_billing_history(self):
        """The billing_history action returns logs for the caller's subscription."""
        BillingCycleLog.objects.create(
            subscription=self.subscription,
            cycle_number=1,
            billing_date=timezone.now() - timedelta(days=30),
            base_amount=Money(Decimal('29.99'), 'USD'),
            total_amount=Money(Decimal('29.99'), 'USD'),
            status='successful',
        )
        BillingCycleLog.objects.create(
            subscription=self.subscription,
            cycle_number=2,
            billing_date=timezone.now(),
            base_amount=Money(Decimal('29.99'), 'USD'),
            total_amount=Money(Decimal('29.99'), 'USD'),
            status='successful',
        )

        self.client.force_authenticate(user=self.user)
        url = reverse(
            'subscriptions_api:subscription-billing-history',
            kwargs={'subscription_id': self.subscription.subscription_id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertTrue(all(log['status'] == 'successful' for log in response.data))

    def test_billing_history_scoped_to_own_subscription(self):
        """Another user calling billing_history on this sub gets 404."""
        other = User.objects.create_user(
            username='other-hist', email='other-hist@example.com', password='pw'
        )
        self.client.force_authenticate(user=other)
        url = reverse(
            'subscriptions_api:subscription-billing-history',
            kwargs={'subscription_id': self.subscription.subscription_id},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_subscriptions_authenticated(self):
        """The list endpoint returns the caller's subscriptions."""
        self.client.force_authenticate(user=self.user)
        url = reverse('subscriptions_api:subscription-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results'] if isinstance(response.data, dict) else response.data
        self.assertEqual(len(results), 1)
        self.assertEqual(
            str(results[0]['subscription_id']), str(self.subscription.subscription_id)
        )
        self.assertEqual(results[0]['total_amount_paid'], '0.00')
        self.assertEqual(results[0]['proration_credit'], '0.00')
        self.assertEqual(results[0]['proration_credit_currency'], 'USD')

    def test_retrieve_subscription(self):
        """The detail endpoint returns the subscription with nested plan data."""
        BillingCycleLog.objects.create(
            subscription=self.subscription,
            cycle_number=1,
            billing_date=timezone.now(),
            base_amount=Money(Decimal('29.99'), 'USD'),
            total_amount=Money(Decimal('29.99'), 'USD'),
            status='successful',
        )

        self.client.force_authenticate(user=self.user)
        url = reverse(
            'subscriptions_api:subscription-detail',
            kwargs={'subscription_id': self.subscription.subscription_id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['plan']['name'], 'Monthly Plan')
        self.assertEqual(response.data['total_amount_paid'], '29.99')
        self.assertEqual(response.data['proration_credit'], '0.00')
        self.assertEqual(response.data['status'], 'active')

    def test_filter_subscriptions_by_status(self):
        """`?status=` restricts the list to matching subscriptions only."""
        # Create a canceled second subscription to filter against.
        now = timezone.now()
        CustomerSubscription.objects.create(
            user=self.user,
            plan=self.plan,
            pricing_tier=self.tier,
            product=self.product,
            payment_provider_account=self.provider_account,
            payment_token=self.token,
            provider_mode='native',
            status='canceled',
            current_period_start=now,
            current_period_end=now + timedelta(days=30),
            next_billing_date=now + timedelta(days=30),
        )

        self.client.force_authenticate(user=self.user)
        url = reverse('subscriptions_api:subscription-list')
        response = self.client.get(url, {'status': 'active'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results'] if isinstance(response.data, dict) else response.data
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['status'], 'active')

    def test_cannot_retrieve_other_users_subscription(self):
        """A user can't retrieve another user's subscription by id."""
        other = User.objects.create_user(
            username='other-sub', email='other-sub@example.com', password='pw'
        )
        self.client.force_authenticate(user=other)
        url = reverse(
            'subscriptions_api:subscription-detail',
            kwargs={'subscription_id': self.subscription.subscription_id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_handles_non_numeric_total_amount_paid(self):
        """If total_amount_paid() ever returns None or a non-numeric, the
        serializer falls back to "0.00" instead of 500-ing on the client."""
        self.client.force_authenticate(user=self.user)
        url = reverse(
            'subscriptions_api:subscription-detail',
            kwargs={'subscription_id': self.subscription.subscription_id},
        )

        with patch.object(CustomerSubscription, 'total_amount_paid', return_value=None):
            response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_amount_paid'], '0.00')
