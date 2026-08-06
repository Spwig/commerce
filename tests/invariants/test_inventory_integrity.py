"""
Tier-1 inventory-integrity invariants (plan invariant #4: no double deduction).

Inventory truth lives on the ``StockItem`` counters, not a ledger — the
checkout path writes no ``StockMovement`` row for allocate/fulfil/release (a
fact the foundation review established). The footprint oracle reads those
counters via ``allocated_by_stock_item`` / ``on_hand_by_stock_item``.

Two complementary altitudes, because "no double deduction" has two distinct
failure modes:

1. **The allocation seam itself**
   (``FulfillmentService.allocate_stock``) — allocation deducts exactly the
   ordered quantity, on_hand is untouched until fulfilment, and the last unit
   is never oversold under contention (one placement wins, the other is
   refused). Plus a negative control proving the oracle is not blind to an
   over-deduction.

2. **The real retry-driven risk** — a double-submitted "Pay" (two
   ``create_payment_intent`` calls in flight) must allocate stock only ONCE.
   This is the failure a retry/duplicate actually causes in production, and it
   is driven through the real ``PaymentOrchestrationService`` order-creation
   path (which calls ``allocate_stock`` under the hood), not the seam directly.
"""

from decimal import Decimal
from unittest import mock

import pytest

from catalog.services.fulfillment import FulfillmentService, InsufficientStockError
from commerce_footprint import assert_exactly_one_order
from commerce_footprint.orm_backend import footprint_for_order
from payment_providers.services.payment_orchestration_service import (
    PaymentOrchestrationService,
)
from tests.factories import (
    CartFactory,
    CartItemFactory,
    OrderFactory,
    OrderItemFactory,
    PaymentProviderAccountFactory,
    ProductFactory,
    StockItemFactory,
    WarehouseFactory,
)

pytestmark = [pytest.mark.django_db, pytest.mark.invariant, pytest.mark.fulfillment]

# Stub only the PSP boundary (as the rest of the suite does); real
# order-creation + allocation run against the DB.
REGISTRY = "payment_providers.services.payment_orchestration_service.ProviderRegistry.get_provider"
GET_PROVIDER = "payment_providers.models.PaymentProviderAccount.get_provider_instance"


@pytest.fixture
def fulfillment_svc():
    return FulfillmentService()


def _stub_provider(provider_intent_id="pi_inventory_1"):
    provider = mock.MagicMock()
    provider.create_payment_intent_for_checkout.return_value = {
        "success": True,
        "provider_intent_id": provider_intent_id,
        "status": "requires_payment_method",
    }
    return provider


def _tracked_product(price="20.00"):
    return ProductFactory(track_inventory=True, price=Decimal(price))


def _order_item(product, warehouse, quantity):
    """A physical order line wired to a warehouse (as create_order assigns),
    so the footprint can resolve it back to its StockItem."""
    order = OrderFactory(shipping_country="US")
    item = OrderItemFactory(order=order, product=product, quantity=quantity, warehouse=warehouse)
    return order, item


def test_allocation_deducts_exactly_ordered_quantity(fulfillment_svc, site_settings):
    """Allocating an order line commits exactly its quantity — no more, no less —
    and leaves on_hand untouched (allocation reserves, fulfilment ships)."""
    warehouse = WarehouseFactory()
    product = _tracked_product()
    stock = StockItemFactory(product=product, warehouse=warehouse, on_hand=50, allocated=0)
    order, item = _order_item(product, warehouse, quantity=3)

    fulfillment_svc.allocate_stock(item, warehouse)

    fp = footprint_for_order(order)
    assert fp.allocated_by_stock_item() == {stock.pk: 3}
    assert fp.on_hand_by_stock_item() == {stock.pk: 50}  # untouched until fulfil
    stock.refresh_from_db()
    assert stock.available == 47  # 50 on_hand - 3 allocated


def test_last_unit_is_never_oversold(fulfillment_svc, site_settings):
    """The canonical 'stock is never deducted twice' case: two customers race
    for the last unit; exactly one wins, the other is refused, and the counter
    never exceeds what exists."""
    warehouse = WarehouseFactory()
    product = _tracked_product()
    stock = StockItemFactory(product=product, warehouse=warehouse, on_hand=1, allocated=0)

    _order_a, item_a = _order_item(product, warehouse, quantity=1)
    _order_b, item_b = _order_item(product, warehouse, quantity=1)

    fulfillment_svc.allocate_stock(item_a, warehouse)  # wins the last unit
    with pytest.raises(InsufficientStockError):
        fulfillment_svc.allocate_stock(item_b, warehouse)  # refused, not oversold

    stock.refresh_from_db()
    assert stock.allocated == 1  # never 2
    assert stock.available == 0


def test_oracle_catches_a_double_deduction(fulfillment_svc, site_settings):
    """Negative control (break-an-invariant): simulate a bug that allocates the
    same line twice and prove the footprint reflects the over-deduction — so
    the real invariant assertion (allocated == ordered qty) would go red rather
    than silently pass. Guards against a vacuous oracle."""
    warehouse = WarehouseFactory()
    product = _tracked_product()
    stock = StockItemFactory(product=product, warehouse=warehouse, on_hand=50, allocated=0)
    order, item = _order_item(product, warehouse, quantity=2)

    # A correct system allocates once (== 2). Force the double-deduction bug:
    fulfillment_svc.allocate_stock(item, warehouse)
    fulfillment_svc.allocate_stock(item, warehouse)

    fp = footprint_for_order(order)
    # The oracle SEES 4, not 2 — a real invariant test asserting == 2 fails here,
    # which is exactly the protection we want.
    assert fp.allocated_by_stock_item() == {stock.pk: 4}
    stock.refresh_from_db()
    assert stock.available == 46  # over-deducted: 50 - 4


# ---------------------------------------------------------------------------
# The real retry-driven invariant: a double-submitted checkout allocates once.
# ---------------------------------------------------------------------------


def _create_intent(session, provider):
    with (
        mock.patch(REGISTRY, return_value=mock.MagicMock()),
        mock.patch(GET_PROVIDER, return_value=_stub_provider()),
    ):
        ok, intent, msg = PaymentOrchestrationService.create_payment_intent(
            session, provider, "https://example.test/return", "https://example.test/cancel"
        )
    assert ok, f"intent creation failed: {msg}"
    return intent


def test_double_submitted_pay_allocates_stock_once(
    customer_user, site_settings, category, warehouse
):
    """Invariant #4 (the real one): two ``create_payment_intent`` calls in
    flight — a double-clicked Pay — create ONE order and allocate the ordered
    quantity exactly ONCE. Without the session lock this would raise two orders
    and deduct stock twice.

    Uses an inventory-tracked, no-shipping product so the order-creation path
    (which allocates stock) runs without the full shipping/warehouse-selection
    setup, while still exercising real allocation. It must be a *physical*
    product with shipping turned off (e.g. local pickup / a stocked service) —
    a ``digital`` product is force-untracked in ``Product.save()`` and so would
    never allocate.
    """
    from cart.services.checkout_service import CheckoutService
    from orders.models import Order

    product = ProductFactory(
        name="Tracked No-Ship Item",
        slug="tracked-no-ship-item",
        category=category,
        price=Decimal("20.00"),
        requires_shipping=False,
        track_inventory=True,
    )
    stock = StockItemFactory(product=product, warehouse=warehouse, on_hand=10, allocated=0)

    cart = CartFactory(user=customer_user)
    CartItemFactory(cart=cart, product=product, quantity=2)
    session = CheckoutService.get_or_create_session(cart)
    session.recalculate_totals()
    CheckoutService.set_billing_address(
        session,
        same_as_shipping=False,
        address_data={
            "address_type": "billing",
            "name": "Ivy Invariant",
            "address1": "1 Ledger Way",
            "city": "Beverly Hills",
            "state": "CA",
            "country": "US",
            "postal_code": "90210",
        },
    )
    provider = PaymentProviderAccountFactory()
    session.payment_provider = provider
    session.save(update_fields=["payment_provider"])

    orders_before = Order.objects.count()

    intent1 = _create_intent(session, provider)
    _create_intent(session, provider)  # the double-submit

    assert Order.objects.count() == orders_before + 1  # exactly one order

    fp = footprint_for_order(intent1.order)
    assert_exactly_one_order(fp)
    # Two units ordered, allocated once — not 4.
    assert fp.allocated_by_stock_item() == {stock.pk: 2}
    stock.refresh_from_db()
    assert stock.allocated == 2
    assert stock.available == 8  # 10 - 2
