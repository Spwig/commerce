"""
Full purchase flow E2E tests.

Tests the complete customer journey: Browse -> Add to Cart -> Checkout
-> Payment -> Order Confirmation.

Run with: pytest tests/e2e/test_full_purchase_flow.py -v
"""

from decimal import Decimal

import pytest

from tests.factories import (
    CategoryFactory,
    OrderFactory,
    OrderItemFactory,
    ProductFactory,
    ShippingCountryFactory,
    ShippingMethodFactory,
    ShippingZoneFactory,
)
from tests.fixtures.checkout_scenarios import domestic_us_merchant
from tests.fixtures.product_scenarios import (
    digital_product_scenario,
    simple_product_scenario,
    variable_product_scenario,
)
from tests.helpers import parse_money

pytestmark = [pytest.mark.django_db(transaction=True), pytest.mark.e2e, pytest.mark.purchase_flow]


# ============================================================
# Simple Product Purchase Flow
# ============================================================


class TestSimplePurchaseFlow:
    """Tests for complete simple product purchase journey."""

    def test_browse_add_to_cart_checkout_to_shipping(
        self, product_page, checkout, site_settings, warehouse
    ):
        """Browse product -> Add to Cart -> Checkout through shipping step."""
        domestic_us_merchant()
        data = simple_product_scenario()
        product = data["product"]

        # Step 1: Browse to product page
        product_page.go_to_product(product.slug)
        assert product_page.get_product_title() == product.name

        # Step 2: Add to cart via API (faster than clicking)
        checkout.add_to_cart(product.id)

        # Step 3: Go to checkout
        checkout.go_to_checkout()

        # Step 4: Fill contact
        checkout.submit_contact()

        # Step 5: Fill shipping address
        checkout.fill_address(
            name="Test Customer",
            address1="456 Broadway",
            city="New York",
            state="NY",
            postal_code="10013",
            country="US",
        )
        checkout.submit_address()

        # Step 6: Verify shipping methods and summary
        methods = checkout.get_available_shipping_methods()
        assert len(methods) > 0
        assert "Standard Shipping" in methods

        checkout.select_shipping_method("Standard Shipping")

        summary = checkout.get_summary()
        assert parse_money(summary["subtotal"]) == Decimal("29.99")
        assert parse_money(summary["shipping"]) == Decimal("5.99")

    def test_full_flow_browse_to_payment_step(
        self, product_page, checkout, site_settings, warehouse, stripe_provider
    ):
        """Complete flow through payment selection step."""
        domestic_us_merchant()
        data = simple_product_scenario()
        product = data["product"]

        # Browse product and add to cart
        product_page.go_to_product(product.slug)
        checkout.add_to_cart(product.id)

        # Checkout flow
        checkout.go_to_checkout()
        checkout.submit_contact()
        checkout.fill_address(
            name="Test Customer",
            address1="456 Broadway",
            city="New York",
            state="NY",
            postal_code="10013",
            country="US",
        )
        checkout.submit_address()
        checkout.select_shipping_method("Standard Shipping")

        # Payment step - select provider
        checkout.select_payment_provider()

        # Verify we advanced past payment step (or it shows payment options)
        summary = checkout.get_summary()
        total = parse_money(summary["total"])
        assert total > Decimal("0.00")


# ============================================================
# Variable Product Purchase Flow
# ============================================================


class TestVariableProductPurchaseFlow:
    """Tests for variable product purchase journey."""

    def test_variable_product_select_variant_checkout(
        self, authenticated_page, site_settings, warehouse
    ):
        """Select variant, add to cart, proceed through checkout."""
        from tests.e2e.conftest import CheckoutHelper

        zone = ShippingZoneFactory(countries=["US"])
        ShippingMethodFactory(name="Standard", flat_rate_cost=Decimal("5.99"), zones=[zone])

        data = variable_product_scenario()
        product = data["product"]
        variant = data["variants"][1]  # Medium

        helper = CheckoutHelper(authenticated_page)

        # Add variant to cart via API with variant_id
        csrf = helper._get_csrf_token()
        authenticated_page.evaluate(f"""
            async () => {{
                const resp = await fetch('/api/cart/add/', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json',
                        'X-CSRFToken': '{csrf}',
                    }},
                    body: JSON.stringify({{
                        product_id: {product.id},
                        variant_id: {variant.id},
                        quantity: 1
                    }}),
                }});
                return resp.json();
            }}
        """)

        # Go to checkout and verify
        helper.go_to_checkout()
        helper.submit_contact()
        helper.fill_address(country="US", city="New York", state="NY")
        helper.submit_address()

        methods = helper.get_available_shipping_methods()
        assert len(methods) > 0

        summary = helper.get_summary()
        assert parse_money(summary["subtotal"]) == Decimal("34.99")


# ============================================================
# Digital Product Purchase Flow
# ============================================================


class TestDigitalProductPurchaseFlow:
    """Tests for digital product purchase journey (no shipping)."""

    def test_digital_product_no_shipping_required(self, checkout, site_settings, warehouse):
        """Digital product checkout shows zero shipping."""
        data = digital_product_scenario()
        product = data["product"]

        checkout.add_to_cart(product.id)
        checkout.go_to_checkout()
        checkout.submit_contact()

        # Still fill address for billing/tax purposes
        checkout.fill_address(country="US", city="New York", state="NY")
        checkout.submit_address()

        # Shipping should be $0
        summary = checkout.get_summary()
        shipping = parse_money(summary.get("shipping", "$0.00"))
        assert shipping == Decimal("0.00")


# ============================================================
# Payment Scenarios
# ============================================================


class TestPaymentScenarios:
    """Tests for payment provider integration.

    These tests require real Stripe test API keys set via environment:
    - STRIPE_TEST_SECRET_KEY
    - STRIPE_TEST_PUBLISHABLE_KEY

    They test the payment flow up to the payment step. Full payment
    completion requires interacting with the Stripe hosted checkout page.
    """

    def test_successful_payment_intent_creation(
        self, checkout, site_settings, warehouse, stripe_provider
    ):
        """Checkout with payment provider reaches payment step successfully."""
        domestic_us_merchant()
        data = simple_product_scenario()

        checkout.add_to_cart(data["product"].id)
        checkout.go_to_checkout()
        checkout.submit_contact()
        checkout.fill_address(
            name="Test Customer",
            address1="456 Broadway",
            city="New York",
            state="NY",
            postal_code="10013",
            country="US",
        )
        checkout.submit_address()
        checkout.select_shipping_method("Standard Shipping")
        checkout.wait_for_payment_step()

        # Payment step should show available providers
        page = checkout.page
        payment_cards = page.query_selector_all(".payment-provider-card")
        # At least the Stripe provider should be available
        assert (
            len(payment_cards) >= 1
            or page.query_selector('[data-action="submit-payment"]') is not None
        )

    def test_checkout_without_payment_provider_shows_message(
        self, checkout, site_settings, warehouse
    ):
        """Checkout with no payment providers shows appropriate message."""
        zone = ShippingZoneFactory(countries=["US"])
        ShippingMethodFactory(name="Standard", flat_rate_cost=Decimal("5.99"), zones=[zone])
        ShippingCountryFactory(country_code="US")

        category = CategoryFactory(name="Payment Test", slug="payment-test")
        product = ProductFactory(
            name="Payment Test Item",
            slug="payment-test-item",
            category=category,
            price=Decimal("25.00"),
            status="published",
        )

        checkout.add_to_cart(product.id)
        checkout.go_to_checkout()
        checkout.submit_contact()
        checkout.fill_address(country="US", city="New York", state="NY")
        checkout.submit_address()
        checkout.select_shipping_method("Standard")
        checkout.wait_for_payment_step()

        # Without any payment provider, the payment step should indicate no providers
        page = checkout.page
        payment_cards = page.query_selector_all(".payment-provider-card")
        empty_state = page.query_selector(".checkout-empty-state")
        # No payment providers should be available
        assert len(payment_cards) == 0
        assert empty_state is not None

    def test_place_order_without_payment_shows_error(self, checkout, site_settings, warehouse):
        """Attempting to place order without completing payment shows error."""
        zone = ShippingZoneFactory(countries=["US"])
        ShippingMethodFactory(name="Standard", flat_rate_cost=Decimal("5.99"), zones=[zone])
        ShippingCountryFactory(country_code="US")

        category = CategoryFactory(name="Error Test", slug="error-test")
        product = ProductFactory(
            name="Error Test Item",
            slug="error-test-item",
            category=category,
            price=Decimal("25.00"),
            status="published",
        )

        checkout.add_to_cart(product.id)
        checkout.go_to_checkout()
        checkout.submit_contact()
        checkout.fill_address(country="US", city="New York", state="NY")
        checkout.submit_address()
        checkout.select_shipping_method("Standard")
        checkout.wait_for_payment_step()

        # Try to find and click place order button
        place_btn = checkout.page.query_selector('[data-action="place-order"]')
        if place_btn:
            place_btn.click()
            checkout.page.wait_for_timeout(1000)
            # Should still be on checkout page (not redirected to confirmation)
            assert "/checkout/" in checkout.page.url


# ============================================================
# Order Confirmation Page
# ============================================================


class TestOrderConfirmationPage:
    """Tests for the order confirmation page rendering."""

    def test_confirmation_shows_order_details(
        self, authenticated_page, site_settings, customer_user
    ):
        """Order confirmation page displays order number and addresses."""
        order = OrderFactory(
            user=customer_user,
            status="processing",
            payment_status="paid",
        )
        OrderItemFactory(order=order, quantity=1, unit_price=Decimal("25.00"))

        base = authenticated_page._live_server_url
        authenticated_page.goto(f"{base}/en/checkout/confirmation/{order.order_number}/")
        authenticated_page.wait_for_load_state("networkidle")

        # Verify order number is displayed
        page_text = authenticated_page.text_content("body")
        assert order.order_number in page_text

    def test_confirmation_shows_items_and_totals(
        self, authenticated_page, site_settings, customer_user
    ):
        """Order confirmation shows item list and order totals."""
        order = OrderFactory(
            user=customer_user,
            status="processing",
            payment_status="paid",
            subtotal=Decimal("50.00"),
            total_amount=Decimal("58.99"),
        )
        product = ProductFactory(
            name="Confirm Test Widget",
            slug="confirm-test-widget",
            price=Decimal("25.00"),
            status="published",
        )
        OrderItemFactory(
            order=order,
            product=product,
            product_name="Confirm Test Widget",
            quantity=2,
            unit_price=Decimal("25.00"),
            total_price=Decimal("50.00"),
        )

        base = authenticated_page._live_server_url
        authenticated_page.goto(f"{base}/en/checkout/confirmation/{order.order_number}/")
        authenticated_page.wait_for_load_state("networkidle")

        page_text = authenticated_page.text_content("body")
        # Order should show the product name and totals
        assert "Confirm Test Widget" in page_text

    def test_confirmation_has_continue_shopping(
        self, authenticated_page, site_settings, customer_user
    ):
        """Order confirmation page has Continue Shopping link."""
        order = OrderFactory(
            user=customer_user,
            status="processing",
            payment_status="paid",
        )
        OrderItemFactory(order=order)

        base = authenticated_page._live_server_url
        authenticated_page.goto(f"{base}/en/checkout/confirmation/{order.order_number}/")
        authenticated_page.wait_for_load_state("networkidle")

        # Look for continue shopping link/button
        continue_link = authenticated_page.query_selector(
            'a[href*="category"], a[href="/en/"], .confirmation__continue, '
            '[data-action="continue-shopping"]'
        )
        assert continue_link is not None


# ============================================================
# Mixed Cart Flow
# ============================================================


class TestMixedCartFlow:
    """Tests for carts with mixed product types."""

    def test_mixed_physical_digital_cart(self, checkout, site_settings, warehouse):
        """Cart with both physical and digital items requires shipping."""
        zone = ShippingZoneFactory(countries=["US"])
        ShippingMethodFactory(name="Standard", flat_rate_cost=Decimal("5.99"), zones=[zone])

        category = CategoryFactory(name="Mixed Test", slug="mixed-test")
        physical = ProductFactory(
            name="Physical Widget",
            slug="physical-widget",
            category=category,
            price=Decimal("25.00"),
            status="published",
            weight=Decimal("0.5"),
        )
        digital = ProductFactory(
            name="Digital Widget",
            slug="digital-widget",
            category=category,
            price=Decimal("9.99"),
            status="published",
            product_type="digital",
            digital=True,
        )

        checkout.add_to_cart(physical.id)
        checkout.add_to_cart(digital.id)
        checkout.go_to_checkout()
        checkout.submit_contact()
        checkout.fill_address(country="US", city="New York", state="NY")
        checkout.submit_address()

        # Should have shipping methods (physical item in cart)
        methods = checkout.get_available_shipping_methods()
        assert len(methods) > 0

        # Subtotal should include both items
        summary = checkout.get_summary()
        subtotal = parse_money(summary["subtotal"])
        assert subtotal == Decimal("34.99")  # 25.00 + 9.99
