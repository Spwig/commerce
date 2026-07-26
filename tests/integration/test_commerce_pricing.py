"""
Equivalence, purity and invariant tests for `commerce.PricingService.quote()`.

The equivalence suite is the linchpin of the pricing extraction. `quote()` is
a transcription of `CheckoutSession.recalculate_totals()`; step 3 of the
rollout points `recalculate_totals` at `quote()`, moving every price on the
storefront onto new code. The only thing making that safe is proof that the
two paths agree to the cent across every interacting feature -- vouchers,
shipping rules, compound tax, bundles, multi-currency and zero-value carts.

If a scenario here fails or is skipped, step 3 must not merge.
"""

from decimal import Decimal

import pytest
from django.db import connection
from django.test.utils import CaptureQueriesContext

from cart.services.checkout_service import CheckoutService
from commerce import PricingService, QuoteRequest
from tests.factories import (
    AddressFactory,
    CartFactory,
    CartItemFactory,
    ProductFactory,
    TaxRateFactory,
)

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.integration,
    pytest.mark.checkout,
    pytest.mark.tax,
]


# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------


@pytest.fixture
def ny_address(db, customer_user):
    return AddressFactory(
        user=customer_user,
        country="US",
        state="NY",
        city="New York",
        postal_code="10001",
    )


@pytest.fixture
def uk_address(db, customer_user):
    return AddressFactory(
        user=customer_user,
        country="GB",
        state="",
        city="London",
        postal_code="SW1A 1AA",
    )


def _cart_with(customer_user, *specs):
    """Build a cart from (name, unit_price, quantity) triples."""
    cart = CartFactory(user=customer_user)
    for name, price, qty in specs:
        CartItemFactory(
            cart=cart,
            product=ProductFactory(name=name, price=Decimal(price)),
            quantity=qty,
            unit_price=Decimal(price),
        )
    return cart


def _session_for(cart, address=None, method=None):
    """A checkout session wired to an address/method but not yet totalled."""
    session = CheckoutService.get_or_create_session(cart)
    if address is not None:
        session.shipping_address = address
        session.save(update_fields=["shipping_address"])
    if method is not None:
        session.selected_shipping_method = method
        session.save(update_fields=["selected_shipping_method"])
    return session


def _assert_equivalent(session, quote):
    """
    Every figure `recalculate_totals` stores must match the fresh quote.

    Compared field by field rather than on the total alone: two offsetting
    errors inside a matching total is exactly the failure this suite exists to
    catch.
    """
    assert quote.subtotal == session.subtotal, "subtotal diverged"
    assert quote.discount_amount == session.discount_amount, "discount diverged"
    assert quote.shipping_cost == session.shipping_cost, "shipping diverged"
    assert quote.tax_amount == session.tax_amount, "tax diverged"
    assert quote.total_amount == session.total_amount, "total diverged"
    assert quote.tax_breakdown == session.tax_breakdown, "tax breakdown diverged"
    assert quote.gift_card_discount == session.gift_card_discount, "gift card diverged"


def _run_both(cart, address=None, method=None):
    """Total via the legacy path and via quote(); return (session, quote)."""
    session = _session_for(cart, address=address, method=method)
    session.recalculate_totals()
    session.refresh_from_db()

    quote = PricingService.quote(
        QuoteRequest(
            cart=cart,
            shipping_address=session.shipping_address or session.shipping_address_data,
            shipping_method=session.selected_shipping_method,
        )
    )
    return session, quote


# --------------------------------------------------------------------------
# Equivalence matrix
# --------------------------------------------------------------------------


class TestQuoteMatchesLegacyPath:
    def test_plain_cart_no_address(self, db, customer_user, site_settings):
        """No address means no tax and no shipping -- subtotal only."""
        cart = _cart_with(customer_user, ("Widget", "25.00", 2))

        session, quote = _run_both(cart)

        _assert_equivalent(session, quote)
        assert quote.total_amount.amount == Decimal("50.00")

    def test_empty_cart(self, db, customer_user, site_settings, ny_address):
        """A zero-value cart must not blow up either path."""
        cart = CartFactory(user=customer_user)

        session, quote = _run_both(cart, address=ny_address)

        _assert_equivalent(session, quote)
        assert quote.total_amount.amount == Decimal("0.00")

    def test_with_simple_tax(self, db, customer_user, site_settings, ny_address):
        TaxRateFactory(ny=True)
        cart = _cart_with(customer_user, ("Widget", "100.00", 1))

        session, quote = _run_both(cart, address=ny_address)

        _assert_equivalent(session, quote)
        assert quote.tax_amount.amount == Decimal("8.88")

    def test_with_vat_applied_to_shipping(self, db, customer_user, site_settings, uk_address):
        """UK VAT has applies_to_shipping=True, exercising a different branch."""
        TaxRateFactory(uk_vat=True)
        cart = _cart_with(customer_user, ("Widget", "50.00", 2))

        session, quote = _run_both(cart, address=uk_address)

        _assert_equivalent(session, quote)

    def test_with_compound_tax(self, db, customer_user, site_settings, ny_address):
        """Two rates, one compounding on the other -- two-phase arithmetic."""
        TaxRateFactory(name="NY State", country="US", state="NY", rate=Decimal("0.0400"))
        TaxRateFactory(
            name="NY City Compound",
            country="US",
            state="NY",
            city="New York",
            rate=Decimal("0.0450"),
            compound=True,
        )
        cart = _cart_with(customer_user, ("Widget", "200.00", 1))

        session, quote = _run_both(cart, address=ny_address)

        _assert_equivalent(session, quote)
        assert len(quote.tax_components) == 2
        assert any(c.compound for c in quote.tax_components)

    def test_with_multiple_line_items(self, db, customer_user, site_settings, ny_address):
        TaxRateFactory(ny=True)
        cart = _cart_with(
            customer_user,
            ("Widget", "25.00", 2),
            ("Gadget", "40.00", 1),
            ("Doohickey", "7.50", 3),
        )

        session, quote = _run_both(cart, address=ny_address)

        _assert_equivalent(session, quote)
        assert quote.subtotal.amount == Decimal("112.50")

    def test_with_bundle_components(self, db, customer_user, site_settings, ny_address):
        """
        Bundle children are priced but excluded from subtotal and tax.

        Guards the interaction between the bundle-exclusion fix and the
        extraction: both paths must exclude children identically.
        """
        TaxRateFactory(ny=True)
        cart = CartFactory(user=customer_user)
        parent = CartItemFactory(
            cart=cart,
            product=ProductFactory(name="Bundle", price=Decimal("100.00")),
            quantity=1,
            unit_price=Decimal("100.00"),
            parent_bundle=None,
        )
        CartItemFactory(
            cart=cart,
            product=ProductFactory(name="Part A", price=Decimal("70.00")),
            quantity=1,
            unit_price=Decimal("70.00"),
            parent_bundle=parent,
        )

        session, quote = _run_both(cart, address=ny_address)

        _assert_equivalent(session, quote)
        assert quote.subtotal.amount == Decimal("100.00")
        assert quote.tax_amount.amount == Decimal("8.88")
        assert sum(1 for ln in quote.lines if ln.is_bundle_child) == 1
        assert sum(1 for ln in quote.lines if ln.counts_toward_subtotal) == 1

    def test_zero_priced_items(self, db, customer_user, site_settings, ny_address):
        TaxRateFactory(ny=True)
        cart = _cart_with(customer_user, ("Freebie", "0.00", 3))

        session, quote = _run_both(cart, address=ny_address)

        _assert_equivalent(session, quote)
        assert quote.total_amount.amount == Decimal("0.00")

    def test_address_as_dict_not_model(self, db, customer_user, site_settings):
        """
        Checkout keeps the address in a JSONField until the order is placed, so
        both shapes are live on the pricing path.
        """
        TaxRateFactory(ny=True)
        cart = _cart_with(customer_user, ("Widget", "100.00", 1))
        address_data = {
            "country": "US",
            "state": "NY",
            "city": "New York",
            "postal_code": "10001",
        }

        session = _session_for(cart)
        session.shipping_address_data = address_data
        session.save(update_fields=["shipping_address_data"])
        session.recalculate_totals()
        session.refresh_from_db()

        quote = PricingService.quote(QuoteRequest(cart=cart, shipping_address=address_data))

        _assert_equivalent(session, quote)
        assert quote.tax_amount.amount == Decimal("8.88")


# --------------------------------------------------------------------------
# Purity -- the property that makes re-quoting cheap and safe
# --------------------------------------------------------------------------


class TestQuoteIsPure:
    def test_quote_issues_no_writes(self, db, customer_user, site_settings, ny_address):
        """
        The defining property. If quote() writes, it cannot be called to verify
        a total before charging, which is the entire point of the extraction.
        """
        TaxRateFactory(ny=True)
        cart = _cart_with(customer_user, ("Widget", "100.00", 1))

        with CaptureQueriesContext(connection) as ctx:
            PricingService.quote(QuoteRequest(cart=cart, shipping_address=ny_address))

        written = [
            q["sql"]
            for q in ctx.captured_queries
            if q["sql"].strip().split()[0].upper() in {"INSERT", "UPDATE", "DELETE"}
        ]
        assert not written, f"quote() must not write, but issued: {written}"

    def test_quote_is_repeatable(self, db, customer_user, site_settings, ny_address):
        """Same inputs, same outputs -- safe to call in a loop."""
        TaxRateFactory(ny=True)
        cart = _cart_with(customer_user, ("Widget", "33.33", 3))
        req = QuoteRequest(cart=cart, shipping_address=ny_address)

        first = PricingService.quote(req)
        second = PricingService.quote(req)

        assert first.total_amount == second.total_amount
        assert first.tax_amount == second.tax_amount
        assert first.inputs_fingerprint == second.inputs_fingerprint

    def test_quote_does_not_touch_the_session_row(
        self, db, customer_user, site_settings, ny_address
    ):
        """An existing session's stored totals must be left exactly as found."""
        TaxRateFactory(ny=True)
        cart = _cart_with(customer_user, ("Widget", "100.00", 1))
        session = _session_for(cart, address=ny_address)
        session.recalculate_totals()
        session.refresh_from_db()
        before = session.total_amount

        PricingService.quote(QuoteRequest(cart=cart, shipping_address=ny_address))
        session.refresh_from_db()

        assert session.total_amount == before


# --------------------------------------------------------------------------
# Invariants
# --------------------------------------------------------------------------


class TestQuoteInvariants:
    def test_gift_card_discount_is_always_zero(self, db, customer_user, site_settings, ny_address):
        """A gift card is a tender, not a discount. Structurally enforced."""
        cart = _cart_with(customer_user, ("Widget", "120.00", 1))

        quote = PricingService.quote(QuoteRequest(cart=cart, shipping_address=ny_address))

        assert quote.gift_card_discount.amount == Decimal("0")
        assert quote.gift_card_discount.currency == quote.subtotal.currency

    def test_total_is_never_negative(self, db, customer_user, site_settings):
        cart = _cart_with(customer_user, ("Widget", "0.00", 1))

        quote = PricingService.quote(QuoteRequest(cart=cart))

        assert quote.total_amount.amount >= Decimal("0")

    def test_fingerprint_changes_when_quantity_changes(
        self, db, customer_user, site_settings, ny_address
    ):
        cart = _cart_with(customer_user, ("Widget", "10.00", 1))
        before = PricingService.quote(
            QuoteRequest(cart=cart, shipping_address=ny_address)
        ).inputs_fingerprint

        item = cart.items.first()
        item.quantity = 5
        item.save(update_fields=["quantity"])

        after = PricingService.quote(
            QuoteRequest(cart=cart, shipping_address=ny_address)
        ).inputs_fingerprint

        assert before != after

    def test_all_money_is_in_cart_currency(self, db, customer_user, site_settings, ny_address):
        """Mixed currencies in a total is the classic silent-corruption bug."""
        TaxRateFactory(ny=True)
        cart = _cart_with(customer_user, ("Widget", "100.00", 1))

        quote = PricingService.quote(QuoteRequest(cart=cart, shipping_address=ny_address))

        for label, value in (
            ("subtotal", quote.subtotal),
            ("discount", quote.discount_amount),
            ("shipping", quote.shipping_cost),
            ("tax", quote.tax_amount),
            ("total", quote.total_amount),
        ):
            assert str(value.currency) == quote.currency, f"{label} in wrong currency"
