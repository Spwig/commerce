"""
Regression tests: cart mutations must refresh the checkout session's totals.

`CartService._sync_checkout_session` is called after every cart mutation to
recalculate the session totals. It filtered on `CheckoutSession.status`, a
field that does not exist -- the model's state field is `step_completed`.
Django resolves field names when the queryset is compiled, so the filter
raised `FieldError` before issuing any SQL, and a bare `except Exception:
pass` swallowed it. `recalculate_totals()` was unreachable from all six call
sites.

A browser never noticed: `CheckoutViewSet.list` calls `recalculate_totals()`
on every GET, so the totals self-corrected before anyone saw them. A client
that mutates a cart and goes straight to payment got stale totals, and
`CheckoutService.create_order` copies session totals verbatim onto the Order.

Every test here therefore reads the session back **from the database** and
never calls `recalculate_totals()` or hits a view -- that is the whole point.
"""

from decimal import Decimal

import pytest
from django.db import connection
from django.test.utils import CaptureQueriesContext

from cart.models import CheckoutSession
from cart.services.cart_service import CartService
from cart.services.checkout_service import CheckoutService
from tests.factories import (
    AddressFactory,
    CartFactory,
    CartItemFactory,
    ProductFactory,
)

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.integration,
    pytest.mark.checkout,
]


@pytest.fixture
def address(db, customer_user):
    return AddressFactory(
        user=customer_user,
        country="US",
        state="NY",
        city="New York",
        postal_code="10001",
    )


@pytest.fixture
def priced_cart(db, customer_user, site_settings):
    """Cart holding two distinct products at $25 and $40 -> $65 subtotal."""
    cart = CartFactory(user=customer_user)
    CartItemFactory(
        cart=cart,
        product=ProductFactory(name="Widget", price=Decimal("25.00")),
        quantity=1,
        unit_price=Decimal("25.00"),
    )
    CartItemFactory(
        cart=cart,
        product=ProductFactory(name="Gadget", price=Decimal("40.00")),
        quantity=1,
        unit_price=Decimal("40.00"),
    )
    return cart


@pytest.fixture
def session_for(priced_cart, address):
    """An established checkout session with its totals already stored."""
    session = CheckoutService.get_or_create_session(priced_cart)
    session.shipping_address = address
    session.save(update_fields=["shipping_address"])
    session.recalculate_totals()
    session.refresh_from_db()
    assert session.total_amount.amount == Decimal("65.00")
    return session


def _stored_total(session):
    """Re-read the session from the database, bypassing any in-memory state."""
    return CheckoutSession.objects.get(pk=session.pk).total_amount.amount


class TestCartMutationsSyncSessionTotals:
    def test_removing_item_updates_session_total(self, priced_cart, session_for):
        """The headless 'removed an item, still charged for it' path."""
        gadget_item = priced_cart.items.get(product__name="Gadget")

        CartService.remove_item(gadget_item)

        assert _stored_total(session_for) == Decimal("25.00")

    def test_adding_item_updates_session_total(self, priced_cart, session_for):
        CartService.add_item(
            cart=priced_cart,
            product_id=ProductFactory(name="Doohickey", price=Decimal("10.00")).id,
            quantity=1,
        )

        assert _stored_total(session_for) == Decimal("75.00")

    def test_updating_quantity_updates_session_total(self, priced_cart, session_for):
        widget_item = priced_cart.items.get(product__name="Widget")

        CartService.update_item(widget_item, quantity=3)

        assert _stored_total(session_for) == Decimal("115.00")

    def test_clearing_cart_zeroes_session_total(self, priced_cart, session_for):
        CartService.clear_cart(priced_cart)

        assert _stored_total(session_for) == Decimal("0.00")


class TestSyncMechanism:
    def test_sync_filters_on_a_field_that_exists(self, priced_cart, session_for):
        """
        Guard against regressing the *class* of bug, not just this instance.

        A filter naming a non-existent field raises when the queryset is
        compiled -- before any SQL is emitted. So "a query against
        checkoutsession was actually issued" is the precise assertion, and it
        fails on the mechanism rather than on a total.
        """
        with CaptureQueriesContext(connection) as ctx:
            CartService._sync_checkout_session(priced_cart)

        assert any("checkoutsession" in q["sql"].lower() for q in ctx.captured_queries), (
            "No query touched checkoutsession. The session lookup raised before "
            "emitting SQL -- most likely a filter naming a field that does not "
            "exist on the model."
        )

    def test_sync_is_a_noop_when_no_session_exists(self, priced_cart):
        """A cart with no checkout session must not raise."""
        assert not CheckoutSession.objects.filter(cart=priced_cart).exists()

        CartService._sync_checkout_session(priced_cart)

    def test_sync_bumps_cart_updated_at(self, priced_cart):
        """The other job this method has -- keep get_or_create_cart ordering sane."""
        before = priced_cart.updated_at

        CartService._sync_checkout_session(priced_cart)
        priced_cart.refresh_from_db()

        assert priced_cart.updated_at > before
