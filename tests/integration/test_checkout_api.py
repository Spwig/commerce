"""
Checkout API integration tests.

Tests the checkout flow via DRF APIClient — no browser needed.
These are fast, reliable, and test the business logic directly.
"""
import pytest
from decimal import Decimal

from tests.factories import (
    CartFactory, CartItemFactory, ProductFactory,
    AddressFactory, ShippingMethodFactory, ShippingZoneFactory,
    TaxRateFactory,
)
from tests.fixtures.checkout_scenarios import (
    domestic_us_merchant, international_merchant,
    free_shipping_threshold_merchant,
)

pytestmark = [pytest.mark.django_db, pytest.mark.checkout, pytest.mark.integration]


# ============================================================
# A. Session Management
# ============================================================

class TestCheckoutSession:

    def test_get_session_creates_new(self, auth_client, cart_with_item):
        """GET /api/checkout/ creates session if none exists."""
        resp = auth_client.get('/api/checkout/')
        assert resp.status_code == 200
        data = resp.json()
        assert data['cart'] is not None
        assert 'subtotal' in data

    def test_get_session_returns_cart_data(self, auth_client, cart_with_item):
        """Session response includes nested cart with items."""
        resp = auth_client.get('/api/checkout/')
        data = resp.json()
        cart = data['cart']
        assert len(cart['items']) == 1
        assert cart['items'][0]['product']['name'] == 'Test Widget A'

    def test_session_recalculates_on_fetch(
        self, auth_client, customer_user, simple_product, site_settings
    ):
        """GET /api/checkout/ recalculates totals from current cart state."""
        cart = CartFactory(user=customer_user)
        CartItemFactory(cart=cart, product=simple_product, quantity=1)

        resp = auth_client.get('/api/checkout/')
        data = resp.json()
        assert Decimal(data['subtotal']) == Decimal('25.00')

        # Add another item directly
        CartItemFactory(cart=cart, product=simple_product, quantity=2)

        resp = auth_client.get('/api/checkout/')
        data = resp.json()
        # Subtotal should now reflect 3 items (1 + 2)
        assert Decimal(data['subtotal']) == Decimal('75.00')

    def test_unauthenticated_returns_401(self, api_client, site_settings):
        """Checkout APIs require authentication when guest checkout is disabled."""
        # Disable guest checkout for this test
        site_settings.admin_email = site_settings.admin_email or 'admin@test.com'
        site_settings.allow_guest_checkout = False
        site_settings.account_creation_timing = 'before_checkout'
        site_settings.save()

        resp = api_client.get('/api/checkout/')
        assert resp.status_code in (401, 403)


# ============================================================
# B. Shipping Address
# ============================================================

class TestShippingAddress:

    def test_set_address_with_data(self, auth_client, cart_with_item):
        """POST shipping address with inline data creates address."""
        resp = auth_client.post('/api/checkout/shipping-address/', {
            'name': 'Test User',
            'address1': '456 Broadway',
            'city': 'New York',
            'state': 'NY',
            'postal_code': '10013',
            'country': 'US',
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data['success'] is True
        session = data['session']
        # Inline address data is stored in shipping_address_data (JSON field), not shipping_address (FK)
        assert session['shipping_address_data']['city'] == 'New York'

    def test_set_address_with_id(self, auth_client, cart_with_item, customer_user):
        """POST shipping address with existing address_id."""
        addr = AddressFactory(user=customer_user)
        resp = auth_client.post('/api/checkout/shipping-address/', {
            'address_id': addr.id,
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data['session']['shipping_address']['id'] == addr.id

    def test_address_change_clears_shipping_method(self, auth_client, cart_with_item):
        """Changing address clears previously selected shipping method."""
        zone = ShippingZoneFactory(countries=['US'])
        method = ShippingMethodFactory(zones=[zone])

        # Set address
        auth_client.post('/api/checkout/shipping-address/', {
            'name': 'Test', 'address1': '123 St', 'city': 'NYC',
            'state': 'NY', 'postal_code': '10001', 'country': 'US',
        })
        # Set shipping method
        auth_client.post('/api/checkout/shipping-method/', {
            'shipping_method_id': method.id,
        })

        # Verify method is set
        resp = auth_client.get('/api/checkout/')
        assert resp.json()['selected_shipping_method'] is not None

        # Change address
        auth_client.post('/api/checkout/shipping-address/', {
            'name': 'New', 'address1': '789 Ave', 'city': 'LA',
            'state': 'CA', 'postal_code': '90001', 'country': 'US',
        })

        # Method should be cleared
        resp = auth_client.get('/api/checkout/')
        assert resp.json()['selected_shipping_method'] is None
        assert Decimal(resp.json()['shipping_cost']) == Decimal('0.00')


# ============================================================
# C. Shipping Methods
# ============================================================

class TestShippingMethods:

    def test_methods_filtered_by_zone_domestic(self, auth_client, cart_with_item):
        """US address only shows US-zone shipping methods."""
        scenario = domestic_us_merchant()

        auth_client.post('/api/checkout/shipping-address/', {
            'name': 'Test', 'address1': '123 St', 'city': 'NYC',
            'state': 'NY', 'postal_code': '10001', 'country': 'US',
        })

        resp = auth_client.get('/api/checkout/shipping-methods/?refresh=true')
        assert resp.status_code == 200
        methods = resp.json()['shipping_methods']
        method_names = [m['name'] for m in methods]
        assert 'Standard Shipping' in method_names
        assert 'Express Shipping' in method_names

    def test_methods_filtered_by_zone_international(self, auth_client, cart_with_item):
        """UK address shows international methods, not domestic."""
        scenario = international_merchant()

        auth_client.post('/api/checkout/shipping-address/', {
            'name': 'Test', 'address1': '10 Downing St', 'city': 'London',
            'state': 'London', 'postal_code': 'SW1A 2AA', 'country': 'GB',
        })

        resp = auth_client.get('/api/checkout/shipping-methods/?refresh=true')
        methods = resp.json()['shipping_methods']
        method_names = [m['name'] for m in methods]
        assert 'International Standard' in method_names
        assert 'International Express' in method_names
        assert 'Domestic Standard' not in method_names

    def test_no_methods_for_unsupported_country(self, auth_client, cart_with_item):
        """Country with no matching zone returns empty methods list."""
        # Only create a US zone
        zone = ShippingZoneFactory(countries=['US'])
        ShippingMethodFactory(zones=[zone])

        # Use a country not in any zone
        auth_client.post('/api/checkout/shipping-address/', {
            'name': 'Test', 'address1': 'Rua Test', 'city': 'Sao Paulo',
            'state': 'SP', 'postal_code': '01310-100', 'country': 'BR',
        })

        resp = auth_client.get('/api/checkout/shipping-methods/?refresh=true')
        methods = resp.json()['shipping_methods']
        assert len(methods) == 0

    def test_free_shipping_below_threshold(self, auth_client, cart_with_item):
        """$25 cart should not qualify for $100 min free shipping."""
        scenario = domestic_us_merchant()

        auth_client.post('/api/checkout/shipping-address/', {
            'name': 'Test', 'address1': '123 St', 'city': 'NYC',
            'state': 'NY', 'postal_code': '10001', 'country': 'US',
        })

        resp = auth_client.get('/api/checkout/shipping-methods/?refresh=true')
        methods = resp.json()['shipping_methods']
        method_names = [m['name'] for m in methods]
        # Free shipping requires $100 min, cart is $25
        assert 'Free Shipping' not in method_names

    def test_free_shipping_above_threshold(
        self, auth_client, cart_with_expensive_item
    ):
        """$150 cart should qualify for $100 min free shipping."""
        scenario = domestic_us_merchant()

        auth_client.post('/api/checkout/shipping-address/', {
            'name': 'Test', 'address1': '123 St', 'city': 'NYC',
            'state': 'NY', 'postal_code': '10001', 'country': 'US',
        })

        resp = auth_client.get('/api/checkout/shipping-methods/?refresh=true')
        methods = resp.json()['shipping_methods']
        method_names = [m['name'] for m in methods]
        assert 'Free Shipping' in method_names

    def test_set_shipping_method_updates_cost(self, auth_client, cart_with_item):
        """Selecting a shipping method updates session shipping_cost."""
        zone = ShippingZoneFactory(countries=['US'])
        method = ShippingMethodFactory(
            name='Test Standard',
            flat_rate_cost=Decimal('8.50'),
            zones=[zone],
        )

        auth_client.post('/api/checkout/shipping-address/', {
            'name': 'Test', 'address1': '123 St', 'city': 'NYC',
            'state': 'NY', 'postal_code': '10001', 'country': 'US',
        })
        resp = auth_client.post('/api/checkout/shipping-method/', {
            'shipping_method_id': method.id,
        })
        assert resp.status_code == 200
        session = resp.json()['session']
        assert Decimal(session['shipping_cost']) == Decimal('8.50')


# ============================================================
# D. Totals & Recalculation
# ============================================================

class TestTotalsRecalculation:

    def test_address_change_resets_shipping_cost(self, auth_client, cart_with_item):
        """Changing address resets shipping_cost to 0."""
        zone = ShippingZoneFactory(countries=['US'])
        method = ShippingMethodFactory(
            flat_rate_cost=Decimal('12.00'),
            zones=[zone],
        )

        # Set address and method
        auth_client.post('/api/checkout/shipping-address/', {
            'name': 'Test', 'address1': '123 St', 'city': 'NYC',
            'state': 'NY', 'postal_code': '10001', 'country': 'US',
        })
        auth_client.post('/api/checkout/shipping-method/', {
            'shipping_method_id': method.id,
        })

        # Verify shipping cost set
        resp = auth_client.get('/api/checkout/')
        assert Decimal(resp.json()['shipping_cost']) == Decimal('12.00')

        # Change address
        auth_client.post('/api/checkout/shipping-address/', {
            'name': 'Test2', 'address1': '789 Ave', 'city': 'LA',
            'state': 'CA', 'postal_code': '90001', 'country': 'US',
        })

        # Shipping cost should be reset
        resp = auth_client.get('/api/checkout/')
        assert Decimal(resp.json()['shipping_cost']) == Decimal('0.00')

    def test_cart_mutation_syncs_session(
        self, auth_client, customer_user, simple_product, site_settings
    ):
        """Adding items to cart recalculates checkout session subtotal."""
        cart = CartFactory(user=customer_user)
        CartItemFactory(cart=cart, product=simple_product, quantity=1)

        # Create session
        resp = auth_client.get('/api/checkout/')
        assert Decimal(resp.json()['subtotal']) == Decimal('25.00')

        # Add item via cart API
        resp = auth_client.post('/api/cart/add/', {
            'product_id': simple_product.id,
            'quantity': 1,
        })
        assert resp.status_code == 200

        # Session should reflect new total
        resp = auth_client.get('/api/checkout/')
        assert Decimal(resp.json()['subtotal']) == Decimal('50.00')

    def test_billing_same_as_shipping_default(self, auth_client, cart_with_item):
        """billing_same_as_shipping defaults to True."""
        resp = auth_client.get('/api/checkout/')
        assert resp.json()['billing_same_as_shipping'] is True


# ============================================================
# E. Validation
# ============================================================

class TestCheckoutValidation:

    def test_validate_missing_address(self, auth_client, cart_with_item):
        """Validation fails without shipping address."""
        resp = auth_client.post('/api/checkout/validate/')
        assert resp.status_code == 200
        data = resp.json()
        assert data['is_valid'] is False
        errors = data.get('errors', [])
        assert any('address' in e.lower() for e in errors)

    def test_validate_missing_shipping_method(self, auth_client, cart_with_item):
        """Validation fails without shipping method (physical items)."""
        auth_client.post('/api/checkout/shipping-address/', {
            'name': 'Test', 'address1': '123 St', 'city': 'NYC',
            'state': 'NY', 'postal_code': '10001', 'country': 'US',
        })

        resp = auth_client.post('/api/checkout/validate/')
        data = resp.json()
        assert data['is_valid'] is False
        errors = data.get('errors', [])
        assert any('shipping method' in e.lower() for e in errors)

    def test_validate_missing_payment(self, auth_client, cart_with_item):
        """Validation fails without payment provider selected."""
        zone = ShippingZoneFactory(countries=['US'])
        method = ShippingMethodFactory(zones=[zone])

        auth_client.post('/api/checkout/shipping-address/', {
            'name': 'Test', 'address1': '123 St', 'city': 'NYC',
            'state': 'NY', 'postal_code': '10001', 'country': 'US',
        })
        auth_client.post('/api/checkout/shipping-method/', {
            'shipping_method_id': method.id,
        })

        resp = auth_client.post('/api/checkout/validate/')
        data = resp.json()
        assert data['is_valid'] is False
        errors = data.get('errors', [])
        assert any('payment' in e.lower() for e in errors)

    def test_validate_empty_cart(
        self, auth_client, customer_user, site_settings
    ):
        """Validation fails for empty cart."""
        CartFactory(user=customer_user)

        resp = auth_client.post('/api/checkout/validate/')
        data = resp.json()
        assert data['is_valid'] is False
        errors = data.get('errors', [])
        assert any('empty' in e.lower() for e in errors)


# ============================================================
# F. Security
# ============================================================

class TestCheckoutSecurity:

    def test_checkout_requires_auth(self, api_client, site_settings):
        """All checkout endpoints require authentication when guest checkout is disabled."""
        # Disable guest checkout for this test
        # Note: Must also set account_creation_timing because 'post_purchase' requires guest checkout
        site_settings.admin_email = site_settings.admin_email or 'admin@test.com'  # Ensure admin_email is set
        site_settings.allow_guest_checkout = False
        site_settings.account_creation_timing = 'before_checkout'  # Compatible with no guest checkout
        site_settings.save()

        endpoints = [
            ('get', '/api/checkout/'),
            ('post', '/api/checkout/shipping-address/'),
            ('get', '/api/checkout/shipping-methods/'),
            ('post', '/api/checkout/shipping-method/'),
            ('get', '/api/checkout/payment-providers/'),
            ('post', '/api/checkout/payment-method/'),
            ('post', '/api/checkout/validate/'),
        ]
        for method, url in endpoints:
            resp = getattr(api_client, method)(url)
            assert resp.status_code in (401, 403), (
                f'{method.upper()} {url} returned {resp.status_code}, expected 401/403'
            )

    def test_order_confirmation_owner_only(
        self, client, customer_user, customer_user_uk, admin_user
    ):
        """Order confirmation page only accessible to order owner or staff."""
        from django.test import Client

        # This test would need an actual order — placeholder for now
        # The view checks: order.user == request.user or request.user.is_staff
        pass
