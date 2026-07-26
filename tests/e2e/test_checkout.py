"""
Checkout E2E browser tests.

These tests drive the full checkout flow via Playwright, validating
the UI renders correctly, totals calculate properly, and the customer
experience is smooth across different merchant configurations.

Run with: pytest tests/e2e/test_checkout.py -v
"""

from decimal import Decimal

import pytest

from tests.e2e.conftest import CheckoutHelper
from tests.factories import (
    ShippingMethodFactory,
    ShippingZoneFactory,
)
from tests.fixtures.checkout_scenarios import (
    domestic_us_merchant,
    international_merchant,
)
from tests.helpers import measure_time, parse_money

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
            name="Test Customer",
            address1="456 Broadway",
            city="New York",
            state="NY",
            postal_code="10013",
            country="US",
        )
        checkout.submit_address()

        # Step 3: Verify shipping methods available
        methods = checkout.get_available_shipping_methods()
        assert "Standard Shipping" in methods
        assert "Express Shipping" in methods

        # Select standard
        checkout.select_shipping_method("Standard Shipping")

        # Verify summary totals
        summary = checkout.get_summary()
        assert parse_money(summary["subtotal"]) == Decimal("25.00")
        assert parse_money(summary["shipping"]) == Decimal("5.99")

    def test_express_shipping(self, checkout, simple_product):
        """Express shipping shows higher cost in summary."""
        domestic_us_merchant()
        checkout.add_to_cart(simple_product.id)
        checkout.go_to_checkout()
        checkout.submit_contact()
        checkout.fill_address(country="US", state="NY", city="New York")
        checkout.submit_address()

        checkout.select_shipping_method("Express Shipping")

        summary = checkout.get_summary()
        assert parse_money(summary["shipping"]) == Decimal("14.99")

    def test_free_shipping_over_threshold(self, checkout, expensive_product):
        """$150 cart qualifies for free shipping ($100 min)."""
        domestic_us_merchant()
        checkout.add_to_cart(expensive_product.id)
        checkout.go_to_checkout()
        checkout.submit_contact()
        checkout.fill_address(country="US", state="NY", city="New York")
        checkout.submit_address()

        methods = checkout.get_available_shipping_methods()
        assert "Free Shipping" in methods

        checkout.select_shipping_method("Free Shipping")
        summary = checkout.get_summary()
        assert parse_money(summary["shipping"]) == Decimal("0.00")

    @pytest.mark.skip(
        reason="Stale: ShippingMethod no longer has min_order_value/free_shipping "
        "(see checkout_scenarios.py) — 'Free Shipping' is now an unconditional $0 "
        "method, so a below-threshold cart DOES see it. Threshold free shipping "
        "moved to promotion_type='free_shipping' rules; re-test needs a "
        "shipping-promotion-rule fixture, not the flat-rate scenario."
    )
    def test_below_free_threshold(self, checkout, simple_product):
        """$25 cart does not qualify for $100 min free shipping."""
        domestic_us_merchant()
        checkout.add_to_cart(simple_product.id)
        checkout.go_to_checkout()
        checkout.submit_contact()
        checkout.fill_address(country="US", state="NY", city="New York")
        checkout.submit_address()

        methods = checkout.get_available_shipping_methods()
        assert "Free Shipping" not in methods

    def test_shipping_method_cost_display(self, checkout, simple_product):
        """Shipping method cards show correct prices (final_cost)."""
        domestic_us_merchant()
        checkout.add_to_cart(simple_product.id)
        checkout.go_to_checkout()
        checkout.submit_contact()
        checkout.fill_address(country="US", state="NY", city="New York")
        checkout.submit_address()

        standard_cost = checkout.get_shipping_method_cost("Standard Shipping")
        express_cost = checkout.get_shipping_method_cost("Express Shipping")

        assert parse_money(standard_cost) == Decimal("5.99")
        assert parse_money(express_cost) == Decimal("14.99")


class TestInternationalCheckout:
    """Tests for international merchant scenarios."""

    def test_uk_address_shows_international_methods(self, checkout, simple_product):
        """UK address shows international methods, hides domestic."""
        international_merchant()
        checkout.add_to_cart(simple_product.id)
        checkout.go_to_checkout()
        checkout.submit_contact()
        checkout.fill_address(
            name="UK Customer",
            address1="10 Downing St",
            city="London",
            state="London",
            postal_code="SW1A 2AA",
            country="GB",
        )
        checkout.submit_address()

        methods = checkout.get_available_shipping_methods()
        assert "International Standard" in methods
        assert "International Express" in methods
        assert "Domestic Standard" not in methods

    def test_us_address_shows_domestic_methods(self, checkout, simple_product):
        """US address shows domestic methods, hides international."""
        international_merchant()
        checkout.add_to_cart(simple_product.id)
        checkout.go_to_checkout()
        checkout.submit_contact()
        checkout.fill_address(country="US", city="New York", state="NY")
        checkout.submit_address()

        methods = checkout.get_available_shipping_methods()
        assert "Domestic Standard" in methods
        # International should not be available for US zone
        assert "International Standard" not in methods

    def test_unsupported_country_no_methods(self, checkout, simple_product):
        """Country not in any zone shows no methods."""
        # Create only a US zone
        zone = ShippingZoneFactory(countries=["US"])
        ShippingMethodFactory(name="US Only", zones=[zone])

        checkout.add_to_cart(simple_product.id)
        checkout.go_to_checkout()
        checkout.submit_contact()
        checkout.fill_address(
            name="Brazil Customer",
            address1="Rua Test",
            city="Sao Paulo",
            state="SP",
            postal_code="01310-100",
            country="BR",
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
        checkout.fill_address(country="US", city="New York", state="NY")
        checkout.submit_address()
        checkout.select_shipping_method("Domestic Standard")

        assert checkout.get_step_state("shipping-method") == "completed"

        # Go back and change to UK address
        checkout.page.click('[data-step="shipping"] .checkout-step__header')
        checkout.page.wait_for_timeout(300)

        checkout.fill_address(
            name="UK Test",
            address1="10 Downing St",
            city="London",
            state="London",
            postal_code="SW1A 2AA",
            country="GB",
        )
        checkout.submit_address()

        # Downstream steps should be reset
        assert checkout.get_step_state("shipping-method") == "active"
        assert checkout.get_step_state("payment") == "disabled"

        # Should now show international methods
        methods = checkout.get_available_shipping_methods()
        assert "International Standard" in methods
        assert "Domestic Standard" not in methods

    def test_shipping_method_change_updates_totals(self, checkout, simple_product):
        """Switching shipping method updates summary totals."""
        domestic_us_merchant()
        checkout.add_to_cart(simple_product.id)
        checkout.go_to_checkout()
        checkout.submit_contact()
        checkout.fill_address(country="US", city="New York", state="NY")
        checkout.submit_address()

        # Select standard ($5.99)
        checkout.select_shipping_method("Standard Shipping")
        summary1 = checkout.get_summary()
        shipping1 = parse_money(summary1["shipping"])
        assert shipping1 == Decimal("5.99")

        # Go back and select express ($14.99)
        checkout.page.click('[data-step="shipping-method"] .checkout-step__header')
        checkout.page.wait_for_timeout(300)
        checkout.select_shipping_method("Express Shipping")

        summary2 = checkout.get_summary()
        shipping2 = parse_money(summary2["shipping"])
        assert shipping2 == Decimal("14.99")
        # Total should increase by $9.00
        assert parse_money(summary2["total"]) > parse_money(summary1["total"])

    def test_session_restore_on_reload(self, checkout, simple_product):
        """Reloading the page restores checkout state from server session."""
        zone = ShippingZoneFactory(countries=["US"])
        ShippingMethodFactory(name="Test Standard", flat_rate_cost=Decimal("5.99"), zones=[zone])

        checkout.add_to_cart(simple_product.id)
        checkout.go_to_checkout()
        checkout.submit_contact()
        checkout.fill_address(country="US", city="New York", state="NY")
        checkout.submit_address()
        checkout.select_shipping_method("Test Standard")

        # Reload
        checkout.page.reload()
        checkout.page.wait_for_load_state("networkidle")
        checkout.page.wait_for_selector(".checkout-step", timeout=5000)

        # Verify state restored
        assert checkout.get_step_state("contact") == "completed"
        assert checkout.get_step_state("shipping") == "completed"
        assert checkout.get_step_state("shipping-method") == "completed"

    def test_back_navigation_between_steps(self, checkout, simple_product):
        """Clicking completed step headers allows re-editing."""
        zone = ShippingZoneFactory(countries=["US"])
        ShippingMethodFactory(name="Standard", zones=[zone])

        checkout.add_to_cart(simple_product.id)
        checkout.go_to_checkout()
        checkout.submit_contact()
        checkout.fill_address(country="US", city="New York", state="NY")
        checkout.submit_address()

        # Click back to contact step
        checkout.page.click('[data-step="contact"] .checkout-step__header')
        checkout.page.wait_for_timeout(300)
        assert checkout.get_current_step() == "contact"

        # Click to shipping step
        checkout.page.click('[data-step="shipping"] .checkout-step__header')
        checkout.page.wait_for_timeout(300)
        assert checkout.get_current_step() == "shipping"

    def test_empty_cart_redirects(self, authenticated_page, site_settings, warehouse):
        """Checkout with empty cart redirects to cart page."""
        from tests.e2e.conftest import CheckoutHelper

        helper = CheckoutHelper(authenticated_page)
        helper.page.goto(f"{helper.base_url}/en/checkout/")
        helper.page.wait_for_load_state("networkidle")

        # Should be redirected to cart page
        assert "/cart/" in helper.page.url

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
        assert checkout.get_current_step() == "shipping"

    def test_place_order_graceful_error(self, checkout, simple_product):
        """Place Order with no payment API keys shows graceful error."""
        zone = ShippingZoneFactory(countries=["US"])
        ShippingMethodFactory(name="Standard", zones=[zone])

        checkout.add_to_cart(simple_product.id)
        checkout.go_to_checkout()
        checkout.submit_contact()
        checkout.fill_address(country="US", city="New York", state="NY")
        checkout.submit_address()
        checkout.select_shipping_method("Standard")

        # Try to select payment (may not have providers in test)
        # and attempt place order — should show error, not crash
        checkout.page.wait_for_timeout(500)
        place_btn = checkout.page.query_selector('[data-action="place-order"]')
        if place_btn:
            place_btn.click()
            checkout.page.wait_for_timeout(1000)
            # Page should still be on checkout, showing an error
            assert "/checkout/" in checkout.page.url


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
        checkout.fill_address(country="US", city="New York", state="NY")
        checkout.submit_address()

        methods = checkout.get_available_shipping_methods()
        assert "Free Shipping" in methods

        summary = checkout.get_summary()
        assert parse_money(summary["subtotal"]) == Decimal("125.00")

    def test_digital_only_cart(self, checkout, digital_product):
        """Digital-only cart should not require shipping method."""
        checkout.add_to_cart(digital_product.id)
        checkout.go_to_checkout()
        checkout.submit_contact()

        # Still need address for billing/tax
        checkout.fill_address(country="US", city="New York", state="NY")
        checkout.submit_address()

        # Shipping should show $0 or be skipped
        summary = checkout.get_summary()
        shipping = parse_money(summary.get("shipping", "0"))
        assert shipping == Decimal("0.00")

    def test_mixed_physical_and_digital(self, checkout, simple_product, digital_product):
        """Mixed cart requires shipping for the physical item."""
        zone = ShippingZoneFactory(countries=["US"])
        ShippingMethodFactory(name="Standard", flat_rate_cost=Decimal("5.99"), zones=[zone])

        checkout.add_to_cart(simple_product.id)
        checkout.add_to_cart(digital_product.id)
        checkout.go_to_checkout()
        checkout.submit_contact()
        checkout.fill_address(country="US", city="New York", state="NY")
        checkout.submit_address()

        # Shipping methods should be available (physical item in cart)
        methods = checkout.get_available_shipping_methods()
        assert len(methods) > 0

        # Subtotal should include both items
        summary = checkout.get_summary()
        subtotal = parse_money(summary["subtotal"])
        assert subtotal == Decimal("34.99")  # 25.00 + 9.99


# ============================================================
# D. Security Tests
# ============================================================


class TestPhoneValidationRegression:
    """Regression tests for the checkout shipping-phone dead-end fix.

    Two defects were fixed:

    A. checkout.js initLiveFieldValidation() — a shipping-phone (or email/
       password/required) validation error used to persist until the next
       submit even after the customer typed a valid value. It now clears the
       moment the field becomes valid.

    B. checkout-express.js autoMountPayment() — a returning customer whose
       saved shipping address had NO phone hit a dead end: the payment card
       showed a previously-selected provider (painted by renderSavedPayment)
       with no form and no place-order button, because autoMountPayment
       returned early on the phone-missing branch without touching it. It now
       overwrites the stale provider card with actionable "add a phone" guidance
       and reveals/focuses the supplemental phone field.
    """

    # --- A. Live-clear of the shipping-phone validation error ---

    def _phone_error_state(self, page):
        """Return (has_error_class, error_message_or_None) for #shipping-phone."""
        return page.evaluate(
            """() => {
                const f = document.getElementById('shipping-phone');
                if (!f) return [null, null];
                const hasErr = f.classList.contains('checkout-input--error');
                const n = f.nextElementSibling;
                const msg = n && n.classList.contains('checkout-form-error')
                    ? n.textContent : null;
                return [hasErr, msg];
            }"""
        )

    def _open_shipping_step(self, checkout, simple_product):
        """Load the accordion checkout and expose the shipping address form.

        The shipping-phone validation error and its live-clear are the target;
        both are driven client-side by submitShippingAddress() and the
        document-level 'input' listener, which bindEvents() /
        initLiveFieldValidation() wire up BEFORE loadCheckout() runs. We reveal
        the CSS-collapsed step bodies with a style override so the fields are
        actionable with real user events, instead of depending on step-by-step
        accordion navigation.

        NOTE: the normal accordion flow (submit_contact -> submit_address) is
        currently broken in this environment — the contact step's Continue
        button never becomes visible, reproduced by the untouched
        TestDomesticCheckout.test_standard_shipping. That is a separate,
        pre-existing defect (loadCheckout appears to collapse the active
        contact step), upstream of and unrelated to the phone-validation fix
        under test here.
        """
        # Need a selectable US option in the country <select>, populated from
        # active ShippingCountry rows.
        domestic_us_merchant()

        checkout.add_to_cart(simple_product.id)
        checkout.go_to_checkout()
        page = checkout.page
        # Wait until the checkout JS has initialised (listeners bound).
        page.wait_for_function(
            "() => window.Checkout && typeof window.Checkout.submitShippingAddress === 'function'",
            timeout=10000,
        )
        # Reveal the collapsed step bodies so the address inputs are fillable
        # with genuine events (real input events are essential: the fix is an
        # 'input' listener).
        page.add_style_tag(
            content=(
                ".checkout-container--accordion .checkout-step__body{ display: block !important; }"
            )
        )
        page.wait_for_selector("#shipping-phone", state="visible", timeout=5000)
        return page

    def _fill_address_invalid_phone(self, page, phone):
        """Fill all shipping fields valid EXCEPT the phone.

        The phone must be present-but-invalid so submitShippingAddress()
        reaches the isValidPhone() check (empty required fields short-circuit
        earlier and would flag every field).
        """
        page.fill("#shipping-name", "Test Customer")
        page.fill("#shipping-address1", "456 Broadway")
        page.fill("#shipping-city", "New York")
        page.fill("#shipping-state", "NY")
        page.fill("#shipping-postal-code", "10013")
        page.select_option("#shipping-country", "US")
        page.fill("#shipping-phone", phone)
        # Real, still-bound handler runs submitShippingAddress(); dispatch_event
        # bypasses actionability since the accordion step is nominally disabled.
        page.dispatch_event('[data-action="continue-shipping"]', "click")
        page.wait_for_timeout(400)

    def test_shipping_phone_error_clears_on_valid_input(self, checkout, simple_product):
        """Typing a valid phone clears the error WITHOUT re-submitting."""
        page = self._open_shipping_step(checkout, simple_product)
        self._fill_address_invalid_phone(page, "abcxyz")  # no digits: invalid

        has_err, msg = self._phone_error_state(page)
        assert has_err is True, "phone field should carry .checkout-input--error"
        assert msg, "an inline .checkout-form-error message should be shown"

        # Type a valid phone. The delegated 'input' listener must clear both the
        # error class and the message immediately — no second submit.
        page.fill("#shipping-phone", "+1 212 555 0100")
        page.wait_for_timeout(250)

        has_err_after, msg_after = self._phone_error_state(page)
        assert has_err_after is False, (
            ".checkout-input--error should be gone once the phone is valid "
            "(live validation regression)"
        )
        assert msg_after is None, (
            ".checkout-form-error message should be removed once the phone is "
            "valid (live validation regression)"
        )

    def test_invalid_input_keeps_error_until_valid(self, checkout, simple_product):
        """The error must NOT clear while the value is still invalid.

        Guards against a false positive where the listener clears on any
        keystroke rather than on genuine validity.
        """
        page = self._open_shipping_step(checkout, simple_product)
        self._fill_address_invalid_phone(page, "abc")

        has_err, _ = self._phone_error_state(page)
        assert has_err is True

        # Still invalid (letters, < 5 digits) — error must remain.
        page.fill("#shipping-phone", "12ab")
        page.wait_for_timeout(200)
        has_err_still, msg_still = self._phone_error_state(page)
        assert has_err_still is True, "error must persist while the phone is still invalid"
        assert msg_still, "error message must persist while still invalid"

    # --- B. Express: phoneless saved address must not dead-end payment ---

    def test_express_phoneless_address_shows_pending_not_dead_end(
        self, authenticated_page, customer_user, site_settings, warehouse, simple_product
    ):
        """A returning customer whose saved default address has no phone must
        see actionable guidance in the payment card, not a stale selected
        provider with no control, and the supplemental phone field must be
        revealed and focused.
        """
        from orders.models import Address

        # Ensures the express template renders (needs a saved-address-card so it
        # doesn't fall back) AND that the default address is genuinely phoneless.
        Address.objects.create(
            user=customer_user,
            address_type="both",
            name="Jane Doe",
            address1="1 Main St",
            city="New York",
            state="NY",
            postal_code="10001",
            country="US",
            phone="",  # the crux: recorded without a phone
            is_default=True,
            is_active=True,
        )
        domestic_us_merchant()

        helper = CheckoutHelper(authenticated_page)
        page = authenticated_page
        base = helper.base_url

        helper.add_to_cart(simple_product.id)
        page.goto(f"{base}/en/checkout/?template=express")
        page.wait_for_load_state("networkidle")
        page.wait_for_selector(".checkout-container--express", timeout=10000)

        # Wait for the base + express loadCheckout() render pass to finish: the
        # payment card's initial spinner is gone once clearStalePlaceholders()
        # has run.
        page.wait_for_function(
            """() => {
                const e = document.getElementById('express-selected-payment');
                return !!window.Checkout && !!e && !e.querySelector('.fa-spinner');
            }""",
            timeout=10000,
        )

        # Seed the exact returning-customer session state the dead-end requires.
        # The current client guards prevent a phoneless address entering the
        # session through the UI, so this state only arises for sessions created
        # before phone became a required field — precisely what the fix targets.
        # renderSavedPayment() and autoMountPayment() are private to the express
        # IIFE, so we (1) reproduce renderSavedPayment()'s stale "selected
        # provider" output verbatim, then (2) drive the REAL, still-bound
        # #express-confirm-shipping-method handler, whose openFirstIncompleteSection()
        # call routes into the real autoMountPayment() fixed branch.
        page.evaluate(
            """() => {
                const C = window.Checkout;
                C.requiresShipping = true;
                C.sessionData = Object.assign({}, C.sessionData, {
                    shipping_address_data: {
                        name: 'Jane Doe', address1: '1 Main St', city: 'New York',
                        state: 'NY', postal_code: '10001', country: 'US', phone: ''
                    },
                    selected_shipping_method: { id: 1, name: 'Standard Shipping' },
                    shipping_cost: '5.99',
                    payment_provider: 999,
                    payment_provider_name: 'Test Pay Provider'
                });
                // Reproduce the stale card renderSavedPayment() paints: a chosen
                // provider name with NO actionable control — the dead end.
                document.getElementById('express-selected-payment').innerHTML =
                    '<div class="express__saved-card-content">' +
                    '<p class="express__saved-card-name">Test Pay Provider</p></div>';
                // Keep the seeded session intact when the confirm handler calls
                // the server for the (already-chosen) shipping method.
                C.submitShippingMethod = async () => {};
                // The confirm handler needs a checked radio to proceed.
                const list = document.getElementById('shipping-methods-list');
                list.innerHTML =
                    '<label><input type="radio" name="shipping_method" ' +
                    'value="1" checked></label>';
            }"""
        )

        # Fire the real handler (bypass visibility: the picker panel is hidden).
        page.dispatch_event("#express-confirm-shipping-method", "click")
        page.wait_for_timeout(600)

        # 1. The payment card no longer shows the stale provider; it shows the
        #    actionable "add a phone" guidance instead.
        payment_text = page.inner_text("#express-selected-payment")
        assert "Add a phone number" in payment_text, (
            f"payment card must show the add-phone guidance, got: {payment_text!r}"
        )
        assert "Test Pay Provider" not in payment_text, (
            "stale selected-provider card must be replaced, not left as a "
            "selected-but-unactionable dead end"
        )

        # 2. The supplemental phone field is revealed and focused so the
        #    customer can fix it immediately.
        group_hidden = page.get_attribute("#saved-address-phone-group", "hidden")
        assert group_hidden is None, "#saved-address-phone-group must be revealed (not hidden)"
        focused_id = page.evaluate("() => document.activeElement && document.activeElement.id")
        assert focused_id == "saved-address-phone", (
            f"supplemental phone field must be focused, activeElement was {focused_id!r}"
        )


class TestCheckoutSecurity:
    def test_unauthenticated_redirect(self, page, site_settings):
        """Unauthenticated user redirected to login from checkout."""
        base = page._live_server_url
        page.goto(f"{base}/en/checkout/")
        page.wait_for_load_state("networkidle")
        # Should be on login page
        assert "login" in page.url.lower() or "account" in page.url.lower()


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
            f"Checkout page took {timer.elapsed_ms:.0f}ms to load (limit: 2000ms)"
        )

    @pytest.mark.slow
    def test_shipping_methods_load_under_1s(self, checkout, simple_product):
        """Shipping methods should load in under 1 second after address submit."""
        zone = ShippingZoneFactory(countries=["US"])
        ShippingMethodFactory(name="Standard", zones=[zone])

        checkout.add_to_cart(simple_product.id)
        checkout.go_to_checkout()
        checkout.submit_contact()
        checkout.fill_address(country="US", city="New York", state="NY")

        with measure_time() as timer:
            checkout.submit_address()

        assert timer.elapsed_ms < 1000, (
            f"Shipping methods took {timer.elapsed_ms:.0f}ms to load (limit: 1000ms)"
        )
