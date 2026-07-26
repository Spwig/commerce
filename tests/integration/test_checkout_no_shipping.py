"""
No-shipping checkout integration tests.

Carts containing only digital and/or booking products never collect a
shipping address or shipping method. These tests cover:

- Product/cart `requires_shipping` semantics for digital and booking types
- validate_checkout not demanding address/method for no-shipping carts
- The minimal billing record (name + country, postal optional) accepted at
  /api/checkout/billing-address/ for no-shipping carts only
- Payment provider filtering without a shipping address: billing country
  first, then the GeoIP fallback, with the merchant ships-to gate skipped
- Mixed carts (digital + physical) still treated as shipping-required
"""

from decimal import Decimal
from unittest.mock import patch

import pytest

from cart.services.checkout_service import CheckoutService
from tests.factories import (
    CartFactory,
    CartItemFactory,
    PaymentProviderAccountFactory,
    ProductFactory,
)
from tests.fixtures.checkout_scenarios import domestic_us_merchant

pytestmark = [pytest.mark.django_db, pytest.mark.checkout, pytest.mark.integration]


SUPPORTS_CURRENCY = (
    "payment_providers.services.payment_method_filter.PaymentMethodFilter._supports_currency"
)


@pytest.fixture
def booking_product(db, category):
    """Booking product — save() forces requires_shipping False."""
    return ProductFactory(
        name="Test Consultation",
        slug="test-consultation",
        category=category,
        price=Decimal("40.00"),
        product_type="booking",
    )


@pytest.fixture
def digital_cart(db, customer_user, digital_product, site_settings):
    cart = CartFactory(user=customer_user)
    CartItemFactory(cart=cart, product=digital_product)
    return cart


@pytest.fixture
def booking_cart(db, customer_user, booking_product, site_settings):
    cart = CartFactory(user=customer_user)
    CartItemFactory(cart=cart, product=booking_product)
    return cart


@pytest.fixture
def mixed_cart(db, customer_user, digital_product, simple_product, site_settings):
    cart = CartFactory(user=customer_user)
    CartItemFactory(cart=cart, product=digital_product)
    CartItemFactory(cart=cart, product=simple_product)
    return cart


@pytest.fixture
def provider_account(db):
    """Active provider with card enabled for US, GB, DE and JP."""
    methods = {"US": ["card"], "GB": ["card"], "DE": ["card"], "JP": ["card"]}
    return PaymentProviderAccountFactory(
        available_payment_methods=methods,
        enabled_payment_methods=methods,
    )


# ============================================================
# A. requires_shipping semantics
# ============================================================


class TestRequiresShipping:
    def test_digital_product_requires_no_shipping(self, digital_product):
        assert digital_product.requires_shipping is False

    def test_booking_product_requires_no_shipping(self, booking_product):
        assert booking_product.requires_shipping is False

    def test_booking_save_forces_requires_shipping_off(self, category):
        """Even if data says True, save() corrects booking products."""
        product = ProductFactory(
            name="Forced Booking",
            slug="forced-booking",
            category=category,
            product_type="booking",
        )
        product.requires_shipping = True
        product.save()
        product.refresh_from_db()
        assert product.requires_shipping is False

    def test_digital_cart_requires_no_shipping(self, digital_cart):
        assert digital_cart.requires_shipping is False

    def test_booking_cart_requires_no_shipping(self, booking_cart):
        assert booking_cart.requires_shipping is False

    def test_digital_plus_booking_cart_requires_no_shipping(self, digital_cart, booking_product):
        CartItemFactory(cart=digital_cart, product=booking_product)
        assert digital_cart.requires_shipping is False

    def test_mixed_cart_requires_shipping(self, mixed_cart):
        assert mixed_cart.requires_shipping is True


# ============================================================
# B. Checkout validation
# ============================================================


class TestNoShippingValidation:
    def test_validate_skips_address_and_method_for_digital_cart(self, auth_client, digital_cart):
        resp = auth_client.post("/api/checkout/validate/")
        assert resp.status_code == 200
        errors = resp.json()["errors"]
        assert "Shipping address is required" not in errors
        assert "Shipping method is required" not in errors

    def test_validate_skips_address_and_method_for_booking_cart(self, auth_client, booking_cart):
        resp = auth_client.post("/api/checkout/validate/")
        errors = resp.json()["errors"]
        assert "Shipping address is required" not in errors
        assert "Shipping method is required" not in errors

    def test_validate_still_demands_address_for_mixed_cart(self, auth_client, mixed_cart):
        resp = auth_client.post("/api/checkout/validate/")
        errors = resp.json()["errors"]
        assert "Shipping address is required" in errors
        assert "Shipping method is required" in errors

    def test_shipping_cost_zero_for_no_shipping_cart(self, auth_client, digital_cart):
        resp = auth_client.get("/api/checkout/")
        session = resp.json()["session"]
        assert Decimal(session["shipping_cost"] or "0") == Decimal("0")


# ============================================================
# C. Minimal billing record
# ============================================================


class TestMinimalBilling:
    def test_minimal_billing_accepted_for_digital_cart(self, auth_client, digital_cart):
        resp = auth_client.post(
            "/api/checkout/billing-address/",
            {
                "same_as_shipping": False,
                "name": "Dana Digital",
                "country": "US",
                "postal_code": "90210",
            },
            format="json",
        )
        assert resp.status_code == 200, resp.content
        session = resp.json()["session"]
        assert session["billing_address_data"]["country"] == "US"

    def test_minimal_billing_postal_optional(self, auth_client, booking_cart):
        resp = auth_client.post(
            "/api/checkout/billing-address/",
            {"same_as_shipping": False, "name": "Bea Booker", "country": "GB"},
            format="json",
        )
        assert resp.status_code == 200, resp.content

    def test_minimal_billing_requires_country(self, auth_client, digital_cart):
        resp = auth_client.post(
            "/api/checkout/billing-address/",
            {"same_as_shipping": False, "name": "No Country"},
            format="json",
        )
        assert resp.status_code == 400

    def test_minimal_billing_rejected_for_shipping_cart(self, auth_client, cart_with_item):
        """Physical carts still require the full billing address."""
        resp = auth_client.post(
            "/api/checkout/billing-address/",
            {
                "same_as_shipping": False,
                "name": "Phil Physical",
                "country": "US",
                "postal_code": "90210",
            },
            format="json",
        )
        assert resp.status_code == 400


# ============================================================
# D. Payment provider filtering without a shipping address
# ============================================================


class TestNoShippingPaymentProviders:
    def test_no_country_known_returns_empty(self, digital_cart, provider_account):
        session = CheckoutService.get_or_create_session(digital_cart)
        with patch(SUPPORTS_CURRENCY, return_value=True):
            assert CheckoutService.get_available_payment_providers(session) == []

    def test_geoip_fallback_country_used(self, digital_cart, provider_account):
        session = CheckoutService.get_or_create_session(digital_cart)
        with patch(SUPPORTS_CURRENCY, return_value=True):
            providers = CheckoutService.get_available_payment_providers(
                session, fallback_country="US"
            )
        assert provider_account in providers

    def test_billing_country_wins_over_fallback(self, digital_cart, provider_account):
        session = CheckoutService.get_or_create_session(digital_cart)
        CheckoutService.set_billing_address(
            session,
            same_as_shipping=False,
            address_data={"address_type": "billing", "name": "Dana", "country": "FR"},
        )
        with patch(SUPPORTS_CURRENCY, return_value=True):
            # FR has no enabled methods on the account — billing country FR
            # must be used (empty), not the fallback US (non-empty)
            providers = CheckoutService.get_available_payment_providers(
                session, fallback_country="US"
            )
        assert providers == []

    def test_ships_to_gate_skipped_for_no_shipping_cart(self, digital_cart, provider_account):
        """Merchant ships only to US; JP customer can still buy a download."""
        domestic_us_merchant()  # creates the US ShippingCountry record
        session = CheckoutService.get_or_create_session(digital_cart)
        CheckoutService.set_billing_address(
            session,
            same_as_shipping=False,
            address_data={"address_type": "billing", "name": "Jiro", "country": "JP"},
        )
        with patch(SUPPORTS_CURRENCY, return_value=True):
            providers = CheckoutService.get_available_payment_providers(session)
        assert provider_account in providers

    def test_ships_to_gate_still_enforced_for_shipping_cart(self, mixed_cart, provider_account):
        """Same JP customer with a physical item in the cart: gate applies."""
        domestic_us_merchant()
        session = CheckoutService.get_or_create_session(mixed_cart)
        CheckoutService.set_shipping_address(
            session,
            address_data={
                "address_type": "shipping",
                "name": "Jiro",
                "address1": "1 Chome",
                "city": "Tokyo",
                "postal_code": "100-0001",
                "country": "JP",
                "phone": "+81 3 1234 5678",
            },
        )
        with patch(SUPPORTS_CURRENCY, return_value=True):
            providers = CheckoutService.get_available_payment_providers(session)
        assert providers == []

    def test_api_providers_list_with_billing_country(
        self, auth_client, digital_cart, provider_account
    ):
        """End-to-end API: billing country set → providers list populates."""
        resp = auth_client.post(
            "/api/checkout/billing-address/",
            {
                "same_as_shipping": False,
                "name": "Dana Digital",
                "country": "US",
                "postal_code": "90210",
            },
            format="json",
        )
        assert resp.status_code == 200

        with patch(SUPPORTS_CURRENCY, return_value=True):
            resp = auth_client.get("/api/checkout/payment-providers/")
        assert resp.status_code == 200
        providers = resp.json()["payment_providers"]
        assert str(provider_account.id) in [str(p["id"]) for p in providers]


# ============================================================
# E. Order creation for a no-shipping cart
# ============================================================


class TestNoShippingOrderCreation:
    def test_create_order_without_address_or_method(
        self, digital_cart, provider_account, warehouse
    ):
        # NOTE: warehouse fixture is required because
        # fulfillment.select_warehouse_for_order raises when no warehouse
        # exists at all, even for a fully digital order — every real
        # install has at least one warehouse.
        session = CheckoutService.get_or_create_session(digital_cart)
        session.recalculate_totals()
        # No-shipping orders need no shipping address/method, but DO require a
        # complete billing address (the merchant collects a full billing form
        # for digital carts).
        CheckoutService.set_billing_address(
            session,
            same_as_shipping=False,
            address_data={
                "address_type": "billing",
                "name": "Dana Digital",
                "address1": "500 Market St",
                "city": "Beverly Hills",
                "state": "CA",
                "country": "US",
                "postal_code": "90210",
            },
        )
        session.payment_provider = provider_account
        session.save(update_fields=["payment_provider"])

        success, message, order = CheckoutService.create_order(session, clear_session=False)
        assert success, message
        assert order is not None
        assert order.shipping_country == ""
        assert order.billing_country == "US"
        assert order.billing_address1 == "500 Market St"
        assert order.shipping_cost.amount == Decimal("0")
        assert order.items.count() == 1

    def test_no_shipping_rejects_incomplete_billing(
        self, digital_cart, provider_account, warehouse
    ):
        """Server backstop: a no-shipping order with only name+country billing
        is rejected. Regression — this used to pass, creating paid orders with
        blank street/city billing."""
        session = CheckoutService.get_or_create_session(digital_cart)
        session.recalculate_totals()
        CheckoutService.set_billing_address(
            session,
            same_as_shipping=False,
            address_data={
                "address_type": "billing",
                "name": "Dana Digital",
                "country": "US",
                "postal_code": "90210",
            },
        )
        session.payment_provider = provider_account
        session.save(update_fields=["payment_provider"])

        is_valid, errors = CheckoutService.validate_checkout(session)
        assert not is_valid
        assert any("billing" in str(e).lower() for e in errors), errors
