"""
Back-order and pre-order products must be purchasable end-to-end.

`is_preorder` and `allow_backorders` mean "sellable with no on-hand stock", and
the storefront stock badge already advertises "Pre-Order"/"Backorder". But every
gate that governed an *actual* purchase used to treat a tracked product with zero
stock as unavailable, so such a product could not be added to the cart, was
filtered out of region listings, and — even if forced through — was rejected at
order placement. The feature was surfaced in the UI but never wired through the
purchase path.

The single source of truth is now `Product.can_sell_without_stock()` (pre-order
OR effective backorders), honoured by:
  * the add-to-cart gate (`CartService._check_stock_availability`),
  * checkout validation and reorder,
  * warehouse selection and stock allocation at order placement — a backordered
    item is recorded with `stock_allocated=False` instead of failing the order.

Region/listing querysets (`available_in_region`, `in_stock_in_region`) surface
backorder/preorder products using the product-level fields.

Setup gotcha: `ProductFactory` defaults `track_inventory=False`, which would make
`can_sell_without_stock()` return True for the wrong reason and pass these tests
vacuously. Every product below is created with `track_inventory=True` and a
zero-stock `StockItem`, so the assertions genuinely exercise the backorder/preorder
paths.
"""

from decimal import Decimal

import pytest

from cart.services.cart_service import CartService
from cart.services.checkout_service import CheckoutService
from catalog.models import Product
from tests.factories import (
    AddressFactory,
    CartFactory,
    PaymentProviderAccountFactory,
    ProductFactory,
    SalesRegionFactory,
    ShippingMethodFactory,
    ShippingZoneFactory,
    StockItemFactory,
    UserFactory,
    WarehouseFactory,
)

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.integration,
    pytest.mark.checkout,
    pytest.mark.fulfillment,
]


# ---------------------------------------------------------------------------
# Model: can_sell_without_stock() + is_in_stock
# ---------------------------------------------------------------------------


def test_can_sell_without_stock_true_for_product_level_backorder():
    product = ProductFactory(track_inventory=True, allow_backorders=True)
    assert product.can_sell_without_stock() is True


def test_can_sell_without_stock_true_for_preorder():
    product = ProductFactory(track_inventory=True, is_preorder=True)
    assert product.can_sell_without_stock() is True


def test_can_sell_without_stock_true_for_category_backorder_override():
    """Effective (cascade-aware): backorders enabled at the category level."""
    product = ProductFactory(track_inventory=True, allow_backorders=False)
    product.category.allow_backorders_override = True
    product.category.save(update_fields=["allow_backorders_override"])
    assert product.can_sell_without_stock() is True


def test_can_sell_without_stock_false_for_plain_tracked_product():
    product = ProductFactory(track_inventory=True, allow_backorders=False, is_preorder=False)
    assert product.can_sell_without_stock() is False


def test_is_in_stock_true_for_preorder_zero_stock():
    """Regression: the property honoured backorders but not pre-orders."""
    product = ProductFactory(track_inventory=True, is_preorder=True)
    StockItemFactory(product=product, on_hand=0, allocated=0)
    assert product.is_in_stock is True


# ---------------------------------------------------------------------------
# Region / listing querysets
# ---------------------------------------------------------------------------


def test_available_in_region_includes_zero_stock_backorder_and_preorder():
    region = SalesRegionFactory()
    warehouse = WarehouseFactory(region=region)

    stocked = ProductFactory(track_inventory=True)
    StockItemFactory(product=stocked, warehouse=warehouse, on_hand=5, allocated=0)

    backorder = ProductFactory(track_inventory=True, allow_backorders=True)
    StockItemFactory(product=backorder, warehouse=warehouse, on_hand=0, allocated=0)

    preorder = ProductFactory(track_inventory=True, is_preorder=True)
    StockItemFactory(product=preorder, warehouse=warehouse, on_hand=0, allocated=0)

    oos = ProductFactory(track_inventory=True, allow_backorders=False, is_preorder=False)
    StockItemFactory(product=oos, warehouse=warehouse, on_hand=0, allocated=0)

    available = set(Product.objects.all().available_in_region(region).values_list("pk", flat=True))

    assert stocked.pk in available
    assert backorder.pk in available
    assert preorder.pk in available
    assert oos.pk not in available  # genuinely out of stock, not backorderable


def test_in_stock_in_region_includes_zero_stock_backorder_and_preorder():
    region = SalesRegionFactory()
    warehouse = WarehouseFactory(region=region)

    backorder = ProductFactory(track_inventory=True, allow_backorders=True)
    StockItemFactory(product=backorder, warehouse=warehouse, on_hand=0, allocated=0)

    preorder = ProductFactory(track_inventory=True, is_preorder=True)
    StockItemFactory(product=preorder, warehouse=warehouse, on_hand=0, allocated=0)

    oos = ProductFactory(track_inventory=True, allow_backorders=False, is_preorder=False)
    StockItemFactory(product=oos, warehouse=warehouse, on_hand=0, allocated=0)

    in_stock = set(Product.objects.all().in_stock_in_region(region).values_list("pk", flat=True))

    assert backorder.pk in in_stock
    assert preorder.pk in in_stock
    assert oos.pk not in in_stock


# ---------------------------------------------------------------------------
# Region visibility (allowlist) must NOT be weakened by the stock decoupling
# ---------------------------------------------------------------------------


def test_visible_in_region_enforces_allowlist_semantics():
    """
    An 'only_in' product is shown only in its selected regions. The PDP's
    region_unavailable flag relies on this, so a geo-restricted product must not
    become visible in other regions just because it can be sold without stock.
    """
    from catalog.models import ProductRegionVisibility

    region_us = SalesRegionFactory(name="US Region", code="US-ONLY", countries=["US"])
    region_eu = SalesRegionFactory(name="EU Region", code="EU-ONLY", countries=["DE", "FR"])

    # US-only product (only_in mode, selected = US). Made a backorder product to
    # prove stock-eligibility does not override geo rules.
    us_only = ProductFactory(
        track_inventory=True, allow_backorders=True, region_restriction_mode="only_in"
    )
    ProductRegionVisibility.objects.create(product=us_only, region=region_us)

    unrestricted = ProductFactory(track_inventory=True)  # mode 'all' → visible everywhere

    visible_us = set(
        Product.objects.all().visible_in_region(region_us).values_list("pk", flat=True)
    )
    visible_eu = set(
        Product.objects.all().visible_in_region(region_eu).values_list("pk", flat=True)
    )

    assert us_only.pk in visible_us
    assert us_only.pk not in visible_eu  # geo restriction preserved
    assert unrestricted.pk in visible_us
    assert unrestricted.pk in visible_eu


# ---------------------------------------------------------------------------
# Add-to-cart gate
# ---------------------------------------------------------------------------


def test_backorder_zero_stock_can_be_added_to_cart(site_settings):
    cart = CartFactory(user=UserFactory())
    product = ProductFactory(track_inventory=True, allow_backorders=True)
    StockItemFactory(product=product, on_hand=0, allocated=0)

    success, message, item = CartService.add_item(cart, product.id, quantity=1)

    assert success is True, f"backorder product was refused: {message}"
    assert item is not None
    assert cart.items.count() == 1


def test_preorder_zero_stock_can_be_added_to_cart(site_settings):
    cart = CartFactory(user=UserFactory())
    product = ProductFactory(track_inventory=True, is_preorder=True)
    StockItemFactory(product=product, on_hand=0, allocated=0)

    success, message, item = CartService.add_item(cart, product.id, quantity=1)

    assert success is True, f"pre-order product was refused: {message}"
    assert item is not None
    assert cart.items.count() == 1


def test_plain_tracked_zero_stock_still_cannot_be_added(site_settings):
    """Guard against the fix leaking: a genuinely OOS product must still fail."""
    cart = CartFactory(user=UserFactory())
    product = ProductFactory(track_inventory=True, allow_backorders=False, is_preorder=False)
    StockItemFactory(product=product, on_hand=0, allocated=0)

    success, message, item = CartService.add_item(cart, product.id, quantity=1)

    assert success is False
    assert "Insufficient stock" in str(message)
    assert item is None
    assert cart.items.count() == 0


# ---------------------------------------------------------------------------
# End-to-end checkout / order placement
# ---------------------------------------------------------------------------


def _checkout(product, customer_user, admin_user, quantity=1):
    """Run a full card checkout for a single product; return (success, msg, order)."""
    cart = CartService.get_or_create_cart(user=customer_user)
    CartService.add_item(cart=cart, product_id=product.id, quantity=quantity)

    address = AddressFactory(user=customer_user)
    session = CheckoutService.get_or_create_session(cart)
    CheckoutService.set_shipping_address(session, address_id=address.id)
    CheckoutService.set_billing_address(session, same_as_shipping=True)

    zone = ShippingZoneFactory(countries=["US"])
    method = ShippingMethodFactory(flat_rate_cost=Decimal("10.00"), zones=[zone])
    CheckoutService.set_shipping_method(session, shipping_method_id=method.id)

    session.payment_provider = PaymentProviderAccountFactory(user=admin_user)
    session.save()

    return CheckoutService.create_order(session)


def test_checkout_of_zero_stock_backorder_places_order_unallocated(
    site_settings, warehouse, customer_user, admin_user
):
    product = ProductFactory(track_inventory=True, allow_backorders=True, price=Decimal("25.00"))
    StockItemFactory(product=product, warehouse=warehouse, on_hand=0, allocated=0)

    success, message, order = _checkout(product, customer_user, admin_user)

    assert success is True, f"backorder checkout failed: {message}"
    assert order is not None
    item = order.items.get(product=product)
    assert item.stock_allocated is False  # recorded as backordered, not allocated


def test_checkout_of_zero_stock_preorder_places_order_unallocated(
    site_settings, warehouse, customer_user, admin_user
):
    product = ProductFactory(track_inventory=True, is_preorder=True, price=Decimal("25.00"))
    StockItemFactory(product=product, warehouse=warehouse, on_hand=0, allocated=0)

    success, message, order = _checkout(product, customer_user, admin_user)

    assert success is True, f"pre-order checkout failed: {message}"
    assert order is not None
    item = order.items.get(product=product)
    assert item.stock_allocated is False


# A genuinely out-of-stock, non-backorderable product is blocked at the
# add-to-cart gate (test_plain_tracked_zero_stock_still_cannot_be_added), so it
# never reaches order placement through the normal flow. The allocation-loop
# "delete the order" branch is a safety net for inconsistent state only, and is
# not reachable via an integration checkout — reserved stock legitimately
# converts — so it is asserted at the unit level, not re-tested here.
