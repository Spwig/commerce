"""
Marketplace Checkout API integration tests.

Tests the marketplace purchase flow: token validation, checkout initiation,
and payment status polling. All external service calls (upgrade server,
payment providers) are mocked.

Note: marketplace_checkout is only loaded when SPWIG_IS_HQ=True.
"""
import pytest
from datetime import timedelta
from unittest.mock import patch, MagicMock
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.utils import timezone

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.marketplace]

User = get_user_model()


@pytest.fixture(autouse=True)
def disable_throttling():
    """Disable DRF throttling for marketplace tests to avoid rate limit interference."""
    from django.core.cache import cache
    cache.clear()
    with patch(
        'marketplace_checkout.views.MarketplaceCheckoutThrottle.allow_request',
        return_value=True,
    ), patch(
        'marketplace_checkout.views.MarketplaceStatusThrottle.allow_request',
        return_value=True,
    ):
        yield


# ============================================================
# Test Data
# ============================================================

VALID_TOKEN_UUID = str(uuid4())

VALID_TOKEN_DATA = {
    'component': {
        'id': 42,
        'slug': 'test-component',
        'name': 'Test Component',
        'price': '29.99',
        'currency': 'EUR',
    },
    'merchant_email': 'merchant@example.com',
    'merchant_name': 'Test Merchant',
    'license_key': 'LIC-XXXX-YYYY',
    'return_url': 'https://shop.example.com/admin/marketplace/',
}


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def mock_validate_token():
    """Mock the upgrade server token validation to return valid data."""
    with patch(
        'marketplace_checkout.views.validate_purchase_token',
        return_value=VALID_TOKEN_DATA,
    ) as mock:
        yield mock


@pytest.fixture
def mock_validate_token_invalid():
    """Mock the upgrade server token validation to raise ValueError."""
    with patch(
        'marketplace_checkout.views.validate_purchase_token',
        side_effect=ValueError('Purchase token has expired'),
    ) as mock:
        yield mock


@pytest.fixture
def mock_validate_token_server_error():
    """Mock the upgrade server being unreachable."""
    import requests
    with patch(
        'marketplace_checkout.views.validate_purchase_token',
        side_effect=requests.ConnectionError('Connection refused'),
    ) as mock:
        yield mock


@pytest.fixture
def hosted_payment_provider(db, admin_user):
    """Create an active hosted-checkout payment provider."""
    from payment_providers.models import PaymentProviderAccount
    from component_updates.models import ComponentRegistry

    component, _ = ComponentRegistry.objects.get_or_create(
        slug='airwallex',
        component_type='payment_provider',
        defaults={
            'name': 'Airwallex',
            'current_version': '1.0.0',
            'author': 'Spwig',
        },
    )
    provider = PaymentProviderAccount.objects.create(
        component=component,
        user=admin_user,
        is_active=True,
        connection_status='connected',
        checkout_mode='hosted',
    )
    return provider


@pytest.fixture
def mock_payment_orchestration():
    """Mock PaymentOrchestrationService.create_payment_intent."""
    mock_intent = MagicMock()
    mock_intent.checkout_url = 'https://checkout.airwallex.com/pay/intent_123'
    mock_intent.id = uuid4()
    mock_intent.order = MagicMock()
    mock_intent.order.order_number = 'ORD-001'

    with patch(
        'payment_providers.services.payment_orchestration_service.'
        'PaymentOrchestrationService.create_payment_intent',
        return_value=(True, mock_intent, None),
    ) as mock:
        mock.intent = mock_intent
        yield mock


# ============================================================
# A. Validate Purchase Token
# ============================================================

class TestValidatePurchaseToken:

    def test_valid_token_returns_component_info(
        self, api_client, mock_validate_token, site_settings, settings
    ):
        """GET with valid token returns component details."""
        settings.SPWIG_IS_HQ = True
        resp = api_client.get(f'/api/marketplace/purchase-token/{VALID_TOKEN_UUID}/')
        assert resp.status_code == 200
        data = resp.json()
        assert data['success'] is True
        assert data['component']['name'] == 'Test Component'
        assert data['merchant_email'] == 'merchant@example.com'
        assert data['return_url'] == 'https://shop.example.com/admin/marketplace/'

    def test_invalid_token_returns_400(
        self, api_client, mock_validate_token_invalid, site_settings, settings
    ):
        """GET with expired/invalid token returns 400."""
        settings.SPWIG_IS_HQ = True
        resp = api_client.get(f'/api/marketplace/purchase-token/{uuid4()}/')
        assert resp.status_code == 400
        data = resp.json()
        assert data['success'] is False
        assert 'expired' in data['error'].lower()

    def test_upgrade_server_down_returns_502(
        self, api_client, mock_validate_token_server_error, site_settings, settings
    ):
        """GET when upgrade server is unreachable returns 502."""
        settings.SPWIG_IS_HQ = True
        resp = api_client.get(f'/api/marketplace/purchase-token/{uuid4()}/')
        assert resp.status_code == 502
        data = resp.json()
        assert data['success'] is False


# ============================================================
# B. Initiate Checkout
# ============================================================

class TestInitiateCheckout:

    def test_successful_checkout_returns_checkout_url(
        self, api_client, mock_validate_token, hosted_payment_provider,
        mock_payment_orchestration, site_settings, settings
    ):
        """POST with valid data creates checkout and returns URL."""
        settings.SPWIG_IS_HQ = True
        resp = api_client.post(
            '/api/marketplace/checkout/',
            data={
                'purchase_token': VALID_TOKEN_UUID,
                'email': 'buyer@example.com',
                'name': 'Jane Doe',
            },
            format='json',
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data['success'] is True
        assert 'checkout_url' in data
        assert 'payment_intent_id' in data

    def test_missing_purchase_token_returns_400(
        self, api_client, site_settings, settings
    ):
        """POST without purchase_token returns 400."""
        settings.SPWIG_IS_HQ = True
        resp = api_client.post(
            '/api/marketplace/checkout/',
            data={'email': 'buyer@example.com'},
            format='json',
        )
        assert resp.status_code == 400
        assert 'purchase_token' in resp.json()['error']

    def test_missing_email_returns_400(
        self, api_client, site_settings, settings
    ):
        """POST without email returns 400."""
        settings.SPWIG_IS_HQ = True
        resp = api_client.post(
            '/api/marketplace/checkout/',
            data={'purchase_token': VALID_TOKEN_UUID},
            format='json',
        )
        assert resp.status_code == 400
        assert 'email' in resp.json()['error']

    def test_invalid_email_returns_400(
        self, api_client, mock_validate_token, site_settings, settings
    ):
        """POST with malformed email returns 400."""
        settings.SPWIG_IS_HQ = True
        resp = api_client.post(
            '/api/marketplace/checkout/',
            data={
                'purchase_token': VALID_TOKEN_UUID,
                'email': 'not-an-email',
            },
            format='json',
        )
        assert resp.status_code == 400
        assert 'Invalid email' in resp.json()['error']

    def test_invalid_token_returns_400(
        self, api_client, mock_validate_token_invalid, site_settings, settings
    ):
        """POST with invalid purchase token returns 400."""
        settings.SPWIG_IS_HQ = True
        resp = api_client.post(
            '/api/marketplace/checkout/',
            data={
                'purchase_token': str(uuid4()),
                'email': 'buyer@example.com',
            },
            format='json',
        )
        assert resp.status_code == 400

    def test_no_payment_provider_returns_500(
        self, api_client, mock_validate_token, site_settings, settings
    ):
        """POST when no hosted payment provider is configured returns 500."""
        settings.SPWIG_IS_HQ = True
        resp = api_client.post(
            '/api/marketplace/checkout/',
            data={
                'purchase_token': VALID_TOKEN_UUID,
                'email': 'buyer@example.com',
            },
            format='json',
        )
        assert resp.status_code == 500
        assert 'No payment provider' in resp.json()['error']

    def test_creates_user_if_not_exists(
        self, api_client, mock_validate_token, hosted_payment_provider,
        mock_payment_orchestration, site_settings, settings
    ):
        """POST auto-creates user by email if none exists."""
        settings.SPWIG_IS_HQ = True
        email = 'newbuyer@example.com'
        assert not User.objects.filter(email=email).exists()

        resp = api_client.post(
            '/api/marketplace/checkout/',
            data={
                'purchase_token': VALID_TOKEN_UUID,
                'email': email,
                'name': 'New Buyer',
            },
            format='json',
        )
        assert resp.status_code == 201
        user = User.objects.get(email=email)
        assert user.first_name == 'New'
        assert user.last_name == 'Buyer'
        assert not user.has_usable_password()

    def test_email_normalized_to_lowercase(
        self, api_client, mock_validate_token, hosted_payment_provider,
        mock_payment_orchestration, site_settings, settings
    ):
        """POST normalizes email to lowercase."""
        settings.SPWIG_IS_HQ = True
        resp = api_client.post(
            '/api/marketplace/checkout/',
            data={
                'purchase_token': VALID_TOKEN_UUID,
                'email': 'Buyer@Example.COM',
            },
            format='json',
        )
        assert resp.status_code == 201
        assert User.objects.filter(email='buyer@example.com').exists()

    def test_idempotent_returns_existing_checkout(
        self, api_client, mock_validate_token, hosted_payment_provider,
        mock_payment_orchestration, site_settings, settings
    ):
        """Duplicate POST with same purchase_token returns existing checkout."""
        settings.SPWIG_IS_HQ = True
        payload = {
            'purchase_token': VALID_TOKEN_UUID,
            'email': 'buyer@example.com',
        }

        resp1 = api_client.post('/api/marketplace/checkout/', data=payload, format='json')
        assert resp1.status_code == 201
        data1 = resp1.json()

        # The mock bypassed real DB creation of the PaymentIntent.
        # Create a real one so the idempotency check finds it.
        from cart.models import CheckoutSession
        from payment_providers.models import PaymentIntent
        from orders.models import Order
        from djmoney.money import Money

        session = CheckoutSession.objects.get(
            metadata__purchase_token=VALID_TOKEN_UUID,
        )

        # Bypass Order post_save signals (email, webhooks) that would
        # fail in a test environment without configured providers.
        from django.db.models.signals import post_save
        receivers = post_save.receivers
        post_save.receivers = []
        try:
            order = Order.objects.create(
                user=session.cart.user,
                order_number='ORD-IDEM-001',
                payment_status='unpaid',
                subtotal=Money('29.99', 'EUR'),
                total_amount=Money('29.99', 'EUR'),
            )
        finally:
            post_save.receivers = receivers

        PaymentIntent.objects.create(
            checkout_session=session,
            provider_account=hosted_payment_provider,
            order=order,
            provider_intent_id='int_test_idempotent',
            checkout_url='https://checkout.airwallex.com/pay/intent_idem',
            status='created',
            amount=Money('29.99', 'EUR'),
            expires_at=timezone.now() + timedelta(hours=1),
        )

        # Second call should return the existing session (200, not 201)
        resp2 = api_client.post('/api/marketplace/checkout/', data=payload, format='json')
        assert resp2.status_code == 200
        assert resp2.json()['success'] is True
        assert 'checkout_url' in resp2.json()


# ============================================================
# C. Payment Status
# ============================================================

class TestPaymentStatus:

    def test_valid_intent_returns_status(
        self, api_client, site_settings, settings
    ):
        """GET with valid payment intent ID returns status."""
        settings.SPWIG_IS_HQ = True

        mock_intent = MagicMock()
        mock_intent.status = 'succeeded'
        mock_intent.order = MagicMock()
        mock_intent.order.order_number = 'ORD-001'
        mock_intent.order.payment_status = 'paid'
        mock_intent.order.metadata = {
            'marketplace': True,
            'component_slug': 'test-component',
        }

        with patch(
            'payment_providers.models.PaymentIntent.objects'
        ) as mock_manager:
            mock_manager.select_related.return_value.get.return_value = mock_intent

            intent_id = uuid4()
            resp = api_client.get(f'/api/marketplace/payment-status/{intent_id}/')
            assert resp.status_code == 200
            data = resp.json()
            assert data['success'] is True
            assert data['payment_status'] == 'succeeded'
            assert data['order_number'] == 'ORD-001'
            assert data['component_name'] == 'test-component'
            # return_url should NOT be in the response (pruned for security)
            assert 'return_url' not in data

    def test_nonexistent_intent_returns_404(
        self, api_client, site_settings, settings
    ):
        """GET with nonexistent payment intent ID returns 404."""
        settings.SPWIG_IS_HQ = True
        resp = api_client.get(f'/api/marketplace/payment-status/{uuid4()}/')
        assert resp.status_code == 404


# ============================================================
# D. Services (unit-level, no HTTP)
# ============================================================

class TestServices:

    def test_validate_token_non_json_response(self, settings):
        """validate_purchase_token handles non-JSON upgrade server response."""
        settings.SPWIG_IS_HQ = True
        from marketplace_checkout.services import validate_purchase_token

        mock_response = MagicMock()
        mock_response.json.side_effect = ValueError('No JSON')
        mock_response.status_code = 502
        mock_response.text = '<html>Bad Gateway</html>'

        with patch('marketplace_checkout.services.requests.get', return_value=mock_response):
            with pytest.raises(ValueError, match='Unable to validate purchase token'):
                validate_purchase_token(str(uuid4()))

    def test_grant_entitlement_missing_metadata(self, settings):
        """grant_component_entitlement raises when metadata is missing."""
        settings.SPWIG_IS_HQ = True
        from marketplace_checkout.services import grant_component_entitlement

        mock_order = MagicMock()
        mock_order.metadata = {}
        mock_order.order_number = 'ORD-MISSING'

        with pytest.raises(ValueError, match='Missing marketplace metadata'):
            grant_component_entitlement(mock_order)

    def test_grant_entitlement_non_json_response(self, settings):
        """grant_component_entitlement handles non-JSON upgrade server response."""
        settings.SPWIG_IS_HQ = True
        from marketplace_checkout.services import grant_component_entitlement

        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.side_effect = ValueError('No JSON')
        mock_response.status_code = 200
        mock_response.text = 'OK'

        mock_order = MagicMock()
        mock_order.metadata = {
            'component_slug': 'test-component',
            'license_key': 'LIC-XXXX',
        }
        mock_order.order_number = 'ORD-001'

        with patch('marketplace_checkout.services.requests.post', return_value=mock_response):
            with pytest.raises(ValueError, match='invalid response'):
                grant_component_entitlement(mock_order)

    def test_error_sanitization_hides_internal_errors(self, settings):
        """validate_purchase_token sanitizes unexpected error messages."""
        settings.SPWIG_IS_HQ = True
        from marketplace_checkout.services import validate_purchase_token

        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {
            'error': 'Internal database error: connection to postgres lost'
        }

        with patch('marketplace_checkout.services.requests.get', return_value=mock_response):
            with pytest.raises(ValueError, match='Invalid purchase token'):
                validate_purchase_token(str(uuid4()))

    def test_safe_error_messages_pass_through(self, settings):
        """validate_purchase_token passes through known safe error messages."""
        settings.SPWIG_IS_HQ = True
        from marketplace_checkout.services import validate_purchase_token

        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            'error': 'Purchase token has expired'
        }

        with patch('marketplace_checkout.services.requests.get', return_value=mock_response):
            with pytest.raises(ValueError, match='Purchase token has expired'):
                validate_purchase_token(str(uuid4()))
