"""In-process product-type purchase flows (Tier-3, live_server).

Beyond the golden flows (which cover simple + digital), these drive EACH
product type to a paid order and assert the **type-specific detail** on the
resulting order line via the extended Footprint oracle — the right variant /
configuration / booking / design / gift-card was actually bought, not just that
a line exists.

Add-to-cart goes through the same ``/api/cart/add/`` path with the type's
payload (``variant_id``, ``configuration``, ``booking_data``, …) via the shared
``CheckoutHelper.add_to_cart(**payload)``; the browser then drives the real
checkout to a card payment through the deterministic ``test_gateway``.
"""

from decimal import Decimal

import pytest

from commerce_footprint import assert_charged_equals, assert_exactly_one_order
from commerce_footprint.footprint import (
    assert_bundle_components,
    assert_line_booking,
    assert_line_configuration,
    assert_line_customization,
    assert_line_gift_card_recipient,
    line_by_sku,
)
from commerce_footprint.orm_backend import footprint_for_order

# Reuse the golden-flow gateway helpers + fixture (importing the fixture makes it
# available in this module's namespace to pytest).
from tests.e2e.test_golden_flows import (  # noqa: F401
    _complete_test_gateway_card,
    _order_number_from_url,
    test_gateway_provider,
)
from tests.fixtures.checkout_scenarios import domestic_us_merchant
from tests.fixtures.product_scenarios import (
    booking_product_scenario,
    bundle_product_scenario,
    configurable_product_scenario,
    customizable_product_scenario,
    gift_card_product_scenario,
    simple_product_scenario,
    variable_product_scenario,
)

pytestmark = [
    pytest.mark.django_db(transaction=True),
    pytest.mark.e2e,
    pytest.mark.product_types,
]

_ADDR = {
    "name": "Test Customer",
    "address1": "456 Broadway",
    "city": "New York",
    "state": "NY",
    "postal_code": "10013",
    "country": "US",
}


def _checkout_to_paid_order(checkout):
    """Drive the shared checkout steps to a completed card payment; return the
    order's footprint. Assumes the cart is already populated."""
    checkout.go_to_checkout()
    checkout.submit_contact()
    checkout.fill_address(**_ADDR)
    checkout.submit_address()
    checkout.select_shipping_method("Standard Shipping")
    checkout.wait_for_payment_step()
    checkout.select_payment_provider()
    _complete_test_gateway_card(checkout.page)
    return footprint_for_order(_order_number_from_url(checkout.page.url))


def test_variable_product_buys_the_chosen_variant(
    product_page, checkout, site_settings, warehouse, test_gateway_provider
):
    """A variable product bought with a specific variant lands a paid order whose
    line records that exact variant (not just the parent product)."""
    domestic_us_merchant()
    product = variable_product_scenario()["product"]
    variant_m = product.variants.get(sku="TSHIRT-M")

    product_page.go_to_product(product.slug)
    status = checkout.add_to_cart(product.id, variant_id=variant_m.id)
    assert status in (200, 201), f"add-to-cart failed with {status}"

    fp = _checkout_to_paid_order(checkout)
    order = assert_exactly_one_order(fp)
    assert order.payment_status == "paid"
    assert len(order.lines) == 1
    assert order.lines[0].variant_sku == "TSHIRT-M"  # the RIGHT variant was bought
    assert_charged_equals(fp, order.total)


def _stock(product, warehouse, on_hand=50):
    """Give a stock-tracked product on-hand at the warehouse so it's buyable."""
    from catalog.models import StockItem

    StockItem.objects.get_or_create(
        product=product, warehouse=warehouse, variant=None, defaults={"on_hand": on_hand}
    )


def test_gift_card_product_purchase_records_recipient_and_amount(
    product_page, checkout, site_settings, warehouse, test_gateway_provider
):
    """Buying a gift-card PRODUCT (chosen denomination + recipient) lands a paid
    order whose gift-card line records that recipient and amount. Bought
    alongside a simple item so the cart ships (gift cards are no-shipping); the
    assertion targets the gift-card line specifically."""
    domestic_us_merchant()
    simple = simple_product_scenario()["product"]
    gc = gift_card_product_scenario()["product"]

    product_page.go_to_product(simple.slug)
    checkout.add_to_cart(simple.id)
    status = checkout.add_to_cart(
        gc.id, gift_card_data={"recipient_email": "giftee@example.test", "amount": 50}
    )
    assert status in (200, 201), f"gift-card add-to-cart failed with {status}"

    fp = _checkout_to_paid_order(checkout)
    order = assert_exactly_one_order(fp)
    assert order.payment_status == "paid"
    assert_line_gift_card_recipient(fp, gc.sku, "giftee@example.test")
    assert line_by_sku(fp, gc.sku).unit_price.value == Decimal("50.00")  # the chosen denomination


def test_bundle_purchase_creates_parent_and_component_lines(
    product_page, checkout, site_settings, warehouse, test_gateway_provider
):
    """Buying a bundle lands a paid order with the parent line PLUS its component
    lines (flagged is_bundle_component)."""
    domestic_us_merchant()
    scenario = bundle_product_scenario()
    bundle = scenario["bundle"]
    components = scenario["components"]

    # A bundle's availability derives from its components — the parent isn't
    # stock-tracked; the components are, so they need on-hand to allocate.
    bundle.track_inventory = False
    bundle.save(update_fields=["track_inventory"])
    for component in components:
        _stock(component, warehouse)

    product_page.go_to_product(bundle.slug)
    status = checkout.add_to_cart(bundle.id)
    assert status in (200, 201), f"bundle add-to-cart failed with {status}"

    fp = _checkout_to_paid_order(checkout)
    order = assert_exactly_one_order(fp)
    assert order.payment_status == "paid"
    assert_bundle_components(fp, bundle.sku, {c.sku for c in components})
    assert_charged_equals(fp, order.total)


def test_configurable_product_records_its_configuration(
    product_page, checkout, site_settings, warehouse, test_gateway_provider
):
    """Building a configurable product (a required option chosen per slot) lands a
    paid order whose parent line records the exact configuration (slot -> options)."""
    from catalog.models import ConfigurationSlotOption

    domestic_us_merchant()
    scenario = configurable_product_scenario()
    product = scenario["product"]

    # Parent availability derives from the chosen option components (like a
    # bundle) — don't stock-gate the parent; stock the option products.
    product.track_inventory = False
    product.save(update_fields=["track_inventory"])
    for option_product in scenario["options"]:
        _stock(option_product, warehouse)

    # Choose the (single required) option in each slot.
    configuration = {}
    expected = {}
    for slot in scenario["slots"]:
        opt = ConfigurationSlotOption.objects.filter(slot=slot).first()
        configuration[str(slot.id)] = [opt.id]
        expected[str(slot.id)] = [str(opt.id)]

    product_page.go_to_product(product.slug)
    status = checkout.add_to_cart(product.id, configuration=configuration)
    assert status in (200, 201), f"configurable add-to-cart failed with {status}"

    fp = _checkout_to_paid_order(checkout)
    order = assert_exactly_one_order(fp)
    assert order.payment_status == "paid"
    assert_line_configuration(fp, product.sku, expected)  # the exact build was recorded
    assert_charged_equals(fp, order.total)


def test_booking_product_records_the_reservation(
    product_page, checkout, site_settings, warehouse, test_gateway_provider
):
    """Booking a slot (future date, resource, persons) lands a paid order whose
    booking line records the reservation (start/end/resource). Bought alongside a
    simple item so the cart ships (booking products are no-shipping)."""
    from datetime import timedelta

    from django.utils import timezone

    domestic_us_merchant()
    simple = simple_product_scenario()["product"]
    scenario = booking_product_scenario()
    booking = scenario["product"]
    resource = scenario["resource"]
    person_type = scenario["person_type"]

    start = (timezone.now() + timedelta(days=3)).replace(hour=10, minute=0, second=0, microsecond=0)
    end = start + timedelta(minutes=60)
    booking_data = {
        "start_datetime": start.isoformat(),
        "end_datetime": end.isoformat(),
        "resource_id": resource.id,
        "persons": {str(person_type.id): 1},
        "timezone": "UTC",
    }

    product_page.go_to_product(simple.slug)
    checkout.add_to_cart(simple.id)
    status = checkout.add_to_cart(booking.id, booking_data=booking_data)
    assert status in (200, 201), f"booking add-to-cart failed with {status}"

    fp = _checkout_to_paid_order(checkout)
    order = assert_exactly_one_order(fp)
    assert order.payment_status == "paid"
    reservation = assert_line_booking(fp, booking.sku, resource_id=resource.id)
    assert reservation.start and reservation.end  # a real slot was reserved


def test_customizable_product_records_its_customization(
    product_page, checkout, site_settings, warehouse, test_gateway_provider
):
    """Buying a customizable product with a text-engraving value lands a paid
    order whose line records that customization value (CustomizationOption path)."""
    domestic_us_merchant()
    scenario = customizable_product_scenario()
    product = scenario["product"]
    option = scenario["options"][0]
    _stock(product, warehouse)

    product_page.go_to_product(product.slug)
    status = checkout.add_to_cart(product.id, customizations={str(option.id): "Happy Birthday"})
    assert status in (200, 201), f"customizable add-to-cart failed with {status}"

    fp = _checkout_to_paid_order(checkout)
    order = assert_exactly_one_order(fp)
    assert order.payment_status == "paid"
    assert_line_customization(fp, product.sku, "Happy Birthday", option=str(option.id))
    assert_charged_equals(fp, order.total)
