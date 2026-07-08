"""
Checkout E2E browser tests.

These tests drive the full checkout flow via Playwright, validating
the UI renders correctly, totals calculate properly, and the customer
experience is smooth across different merchant configurations.

Run with: pytest tests/e2e/test_checkout.py -v
"""
import pytest
from decimal import Decimal

from tests.helpers import parse_money, assert_totals, measure_time
from tests.factories import (
    ProductFactory, ShippingZoneFactory, ShippingMethodFactory,
    TaxRateFactory, CartFactory, CartItemFactory,
)
from tests.fixtures.checkout_scenarios import (
    domestic_us_merchant, international_merchant,
    free_shipping_threshold_merchant,
)

pytestmark = [pytest.mark.django_db, pytest.mark.checkout, pytest.mark.e2e]


# ============================================================
# A. Happy Path Tests
# ============================================================

class TestDomesticCheckout:
    """Tests for domestic-only (US) merchant scenarios."""

    def test_standard_shipping(self, checkout, simple_product):
        """Complete checkout with standard US shipping."""
        domestic_us_merchant()
        checkout.add_to_cart(simple_product.id)
        checkout.go_to_checkout()

        # Step 1: Contact (email pre-filled)
        checkout.submit_contact()

        # Step 2: Shipping address (US)
        checkout.fill_address(
            name='Test Customer', address1='456 Broadway',
            city='New York', state='NY', postal_code='10013', country='US',
        )
        checkout.submit_address()

        # Step 3: Verify shipping methods available
        methods = checkout.get_available_shipping_methods()
        assert 'Standard Shipping' in methods
        assert 'Express Shipping' in methods

        # Select standard
        checkout.select_shipping_method('Standard Shipping')

        # Verify summary totals
        summary = checkout.get_summary()
        assert parse_money(summary['subtotal']) == Decimal('25.00')
        assert parse_money(summary['shipping']) == Decimal('5.99')

    def test_express_shipping(self, checkout, simple_product):
        """Express shipping shows higher cost in summary."""
        domestic_us_merchant()
        checkout.add_to_cart(simple_product.id)
        checkout.go_to_checkout()
        checkout.submit_contact()
        checkout.fill_address(country='US', state='NY', city='New York')
        checkout.submit_address()

        checkout.select_shipping_method('Express Shipping')

        summary = checkout.get_summary()
        assert parse_money(summary['shipping']) == Decimal('14.99')

    def test_free_shipping_over_threshold(self, checkout, expensive_product):
        """$150 cart qualifies for free shipping ($100 min)."""
        domestic_us_merchant()
        checkout.add_to_cart(expensive_product.id)
        checkout.go_to_checkout()
        checkout.submit_contact()
        checkout.fill_address(country='US', state='NY', city='New York')
        checkout.submit_address()

        methods = checkout.get_available_shipping_methods()
        assert 'Free Shipping' in methods

        checkout.select_shipping_method('Free Shipping')
        summary = checkout.get_summary()
        assert parse_money(summary['shipping']) == Decimal('0.00')

    def test_below_free_threshold(self, checkout, simple_product):
        """$25 cart does not qualify for $100 min free shipping."""
        domestic_us_merchant()
        checkout.add_to_cart(simple_product.id)
        checkout.go_to_checkout()
        checkout.submit_contact()
        checkout.fill_address(country='US', state='NY', city='New York')
        checkout.submit_address()

        methods = checkout.get_available_shipping_methods()
        assert 'Free Shipping' not in methods

    def test_shipping_method_cost_display(self, checkout, simple_product):
        """Shipping method cards show correct prices (final_cost)."""
        domestic_us_merchant()
        checkout.add_to_cart(simple_product.id)
        checkout.go_to_checkout()
        checkout.submit_contact()
        checkout.fill_address(country='US', state='NY', city='New York')
        checkout.submit_address()

        standard_cost = checkout.get_shipping_method_cost('Standard Shipping')
        express_cost = checkout.get_shipping_method_cost('Express Shipping')

        assert parse_money(standard_cost) == Decimal('5.99')
        assert parse_money(express_cost) == Decimal('14.99')


class TestInternationalCheckout:
    """Tests for international merchant scenarios."""

    def test_uk_address_shows_international_methods(self, checkout, simple_product):
        """UK address shows international methods, hides domestic."""
        international_merchant()
        checkout.add_to_cart(simple_product.id)
        checkout.go_to_checkout()
        checkout.submit_contact()
        checkout.fill_address(
            name='UK Customer', address1='10 Downing St',
            city='London', state='London', postal_code='SW1A 2AA', country='GB',
        )
        checkout.submit_address()

        methods = checkout.get_available_shipping_methods()
        assert 'International Standard' in methods
        assert 'International Express' in methods
        assert 'Domestic Standard' not in methods

    def test_us_address_shows_domestic_methods(self, checkout, simple_product):
        """US address shows domestic methods, hides international."""
        international_merchant()
        checkout.add_to_cart(simple_product.id)
        checkout.go_to_checkout()
        checkout.submit_contact()
        checkout.fill_address(country='US', city='New York', state='NY')
        checkout.submit_address()

        methods = checkout.get_available_shipping_methods()
        assert 'Domestic Standard' in methods
        # International should not be available for US zone
        assert 'International Standard' not in methods

    def test_unsupported_country_no_methods(self, checkout, simple_product):
        """Country not in any zone shows no methods."""
        # Create only a US zone
        zone = ShippingZoneFactory(countries=['US'])
        ShippingMethodFactory(name='US Only', zones=[zone])

        checkout.add_to_cart(simple_product.id)
        checkout.go_to_checkout()
        checkout.submit_contact()
        checkout.fill_address(
            name='Brazil Customer', address1='Rua Test',
            city='Sao Paulo', state='SP', postal_code='01310-100', country='BR',
        )
        checkout.submit_address()

        methods = checkout.get_available_shipping_methods()
        assert len(methods) == 0


# ============================================================
# B. Customer Behavior Tests
# ============================================================

class TestCustomerBehavior:
    """Tests for various customer actions during checkout."""

    def test_address_change_invalidates_downstream(self, checkout, simple_product):
        """Changing address resets shipping method, payment, review steps."""
        scenario = international_merchant()
        checkout.add_to_cart(simple_product.id)
        checkout.go_to_checkout()
        checkout.submit_contact()

        # First: US address
        checkout.fill_address(country='US', city='New York', state='NY')
        checkout.submit_address()
        checkout.select_shipping_method('Domestic Standard')

        assert checkout.get_step_state('shipping-method') == 'completed'

        # Go back and change to UK address
        checkout.page.click('[data-step="shipping"] .checkout-step__header')
        checkout.page.wait_for_timeout(300)

        checkout.fill_address(
            name='UK Test', address1='10 Downing St',
            city='London', state='London', postal_code='SW1A 2AA', country='GB',
        )
        checkout.submit_address()

        # Downstream steps should be reset
        assert checkout.get_step_state('shipping-method') == 'active'
        assert checkout.get_step_state('payment') == 'disabled'

        # Should now show international methods
        methods = checkout.get_available_shipping_methods()
        assert 'International Standard' in methods
        assert 'Domestic Standard' not in methods

    def test_shipping_method_change_updates_totals(self, checkout, simple_product):
        """Switching shipping method updates summary totals."""
        domestic_us_merchant()
        checkout.add_to_cart(simple_product.id)
        checkout.go_to_checkout()
        checkout.submit_contact()
        checkout.fill_address(country='US', city='New York', state='NY')
        checkout.submit_address()

        # Select standard ($5.99)
        checkout.select_shipping_method('Standard Shipping')
        summary1 = checkout.get_summary()
        shipping1 = parse_money(summary1['shipping'])
        assert shipping1 == Decimal('5.99')

        # Go back and select express ($14.99)
        checkout.page.click('[data-step="shipping-method"] .checkout-step__header')
        checkout.page.wait_for_timeout(300)
        checkout.select_shipping_method('Express Shipping')

        summary2 = checkout.get_summary()
        shipping2 = parse_money(summary2['shipping'])
        assert shipping2 == Decimal('14.99')
        # Total should increase by $9.00
        assert parse_money(summary2['total']) > parse_money(summary1['total'])

    def test_session_restore_on_reload(self, checkout, simple_product):
        """Reloading the page restores checkout state from server session."""
        zone = ShippingZoneFactory(countries=['US'])
        ShippingMethodFactory(name='Test Standard', flat_rate_cost=Decimal('5.99'), zones=[zone])

        checkout.add_to_cart(simple_product.id)
        checkout.go_to_checkout()
        checkout.submit_contact()
        checkout.fill_address(country='US', city='New York', state='NY')
        checkout.submit_address()
        checkout.select_shipping_method('Test Standard')

        # Reload
        checkout.page.reload()
        checkout.page.wait_for_load_state('networkidle')
        checkout.page.wait_for_selector('.checkout-step', timeout=5000)

        # Verify state restored
        assert checkout.get_step_state('contact') == 'completed'
        assert checkout.get_step_state('shipping') == 'completed'
        assert checkout.get_step_state('shipping-method') == 'completed'

    def test_back_navigation_between_steps(self, checkout, simple_product):
        """Clicking completed step headers allows re-editing."""
        zone = ShippingZoneFactory(countries=['US'])
        ShippingMethodFactory(name='Standard', zones=[zone])

        checkout.add_to_cart(simple_product.id)
        checkout.go_to_checkout()
        checkout.submit_contact()
        checkout.fill_address(country='US', city='New York', state='NY')
        checkout.submit_address()

        # Click back to contact step
        checkout.page.click('[data-step="contact"] .checkout-step__header')
        checkout.page.wait_for_timeout(300)
        assert checkout.get_current_step() == 'contact'

        # Click to shipping step
        checkout.page.click('[data-step="shipping"] .checkout-step__header')
        checkout.page.wait_for_timeout(300)
        assert checkout.get_current_step() == 'shipping'

    def test_empty_cart_redirects(self, authenticated_page, site_settings, warehouse):
        """Checkout with empty cart redirects to cart page."""
        from tests.e2e.conftest import CheckoutHelper
        helper = CheckoutHelper(authenticated_page)
        helper.page.goto(f'{helper.base_url}/en/checkout/')
        helper.page.wait_for_load_state('networkidle')

        # Should be redirected to cart page
        assert '/cart/' in helper.page.url

    def test_required_field_validation(self, checkout, simple_product):
        """Empty shipping address fields show validation errors."""
        checkout.add_to_cart(simple_product.id)
        checkout.go_to_checkout()
        checkout.submit_contact()

        # Try to submit without filling any fields
        # Click toggle to show new address form first
        toggle = checkout.page.query_selector('[data-action="toggle-new-address"]')
        if toggle:
            toggle.click()
            checkout.page.wait_for_timeout(200)

        checkout.page.click('[data-action="submit-shipping"]')
        checkout.page.wait_for_timeout(500)

        # Should show field errors and NOT advance to next step
        assert checkout.get_current_step() == 'shipping'

    def test_place_order_graceful_error(self, checkout, simple_product):
        """Place Order with no payment API keys shows graceful error."""
        zone = ShippingZoneFactory(countries=['US'])
        ShippingMethodFactory(name='Standard', zones=[zone])

        checkout.add_to_cart(simple_product.id)
        checkout.go_to_checkout()
        checkout.submit_contact()
        checkout.fill_address(country='US', city='New York', state='NY')
        checkout.submit_address()
        checkout.select_shipping_method('Standard')

        # Try to select payment (may not have providers in test)
        # and attempt place order — should show error, not crash
        checkout.page.wait_for_timeout(500)
        place_btn = checkout.page.query_selector('[data-action="place-order"]')
        if place_btn:
            place_btn.click()
            checkout.page.wait_for_timeout(1000)
            # Page should still be on checkout, showing an error
            assert '/checkout/' in checkout.page.url


# ============================================================
# C. Edge Cases
# ============================================================

class TestEdgeCases:
    """Tests for edge cases and unusual scenarios."""

    def test_high_quantity_triggers_free_shipping(self, checkout, simple_product):
        """qty=5 of $25 item = $125 qualifies for $100 free shipping."""
        domestic_us_merchant()
        checkout.add_to_cart(simple_product.id, quantity=5)
        checkout.go_to_checkout()
        checkout.submit_contact()
        checkout.fill_address(country='US', city='New York', state='NY')
        checkout.submit_address()

        methods = checkout.get_available_shipping_methods()
        assert 'Free Shipping' in methods

        summary = checkout.get_summary()
        assert parse_money(summary['subtotal']) == Decimal('125.00')

    def test_digital_only_cart(self, checkout, digital_product):
        """Digital-only cart should not require shipping method."""
        checkout.add_to_cart(digital_product.id)
        checkout.go_to_checkout()
        checkout.submit_contact()

        # Still need address for billing/tax
        checkout.fill_address(country='US', city='New York', state='NY')
        checkout.submit_address()

        # Shipping should show $0 or be skipped
        summary = checkout.get_summary()
        shipping = parse_money(summary.get('shipping', '0'))
        assert shipping == Decimal('0.00')

    def test_mixed_physical_and_digital(self, checkout, simple_product, digital_product):
        """Mixed cart requires shipping for the physical item."""
        zone = ShippingZoneFactory(countries=['US'])
        ShippingMethodFactory(name='Standard', flat_rate_cost=Decimal('5.99'), zones=[zone])

        checkout.add_to_cart(simple_product.id)
        checkout.add_to_cart(digital_product.id)
        checkout.go_to_checkout()
        checkout.submit_contact()
        checkout.fill_address(country='US', city='New York', state='NY')
        checkout.submit_address()

        # Shipping methods should be available (physical item in cart)
        methods = checkout.get_available_shipping_methods()
        assert len(methods) > 0

        # Subtotal should include both items
        summary = checkout.get_summary()
        subtotal = parse_money(summary['subtotal'])
        assert subtotal == Decimal('34.99')  # 25.00 + 9.99


# ============================================================
# D. Security Tests
# ============================================================

class TestCheckoutSecurity:

    def test_unauthenticated_redirect(self, page, site_settings):
        """Unauthenticated user redirected to login from checkout."""
        base = page._live_server_url
        page.goto(f'{base}/en/checkout/')
        page.wait_for_load_state('networkidle')
        # Should be on login page
        assert 'login' in page.url.lower() or 'account' in page.url.lower()


# ============================================================
# E. Performance Tests
# ============================================================

class TestCheckoutPerformance:

    @pytest.mark.slow
    def test_checkout_page_loads_under_2s(self, checkout, simple_product):
        """Checkout page should load in under 2 seconds."""
        checkout.add_to_cart(simple_product.id)

        with measure_time() as timer:
            checkout.go_to_checkout()

        assert timer.elapsed_ms < 2000, (
            f'Checkout page took {timer.elapsed_ms:.0f}ms to load (limit: 2000ms)'
        )

    @pytest.mark.slow
    def test_shipping_methods_load_under_1s(self, checkout, simple_product):
        """Shipping methods should load in under 1 second after address submit."""
        zone = ShippingZoneFactory(countries=['US'])
        ShippingMethodFactory(name='Standard', zones=[zone])

        checkout.add_to_cart(simple_product.id)
        checkout.go_to_checkout()
        checkout.submit_contact()
        checkout.fill_address(country='US', city='New York', state='NY')

        with measure_time() as timer:
            checkout.submit_address()

        assert timer.elapsed_ms < 1000, (
            f'Shipping methods took {timer.elapsed_ms:.0f}ms to load (limit: 1000ms)'
        )
