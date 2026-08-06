"""
Golden-flow browser E2E — the small set of complete customer journeys that
should pass on every PR (Tier 3). Unlike the rest of tests/e2e/ (which drive
checkout only up to the payment step), these complete a real card payment
through the deterministic test_gateway and assert the full financial footprint
of the resulting order via the Footprint oracle.

Golden flow #1: card checkout → paid order.

Runs against live_server by default; the same journey runs against a deployed
target when SPWIG_E2E_BASE_URL is set (see conftest ``target_url``).
"""

from decimal import Decimal

import pytest

from commerce_footprint import assert_charged_equals, assert_exactly_one_order
from commerce_footprint.footprint import Amount
from commerce_footprint.orm_backend import footprint_for_order
from tests.fixtures.checkout_scenarios import domestic_us_merchant
from tests.fixtures.product_scenarios import simple_product_scenario
from tests.helpers import E2E_TIMEOUT_MS, parse_money

pytestmark = [pytest.mark.django_db(transaction=True), pytest.mark.e2e, pytest.mark.purchase_flow]


@pytest.fixture(autouse=True)
def _force_sandbox_mode():
    """Force sandbox mode on for every golden flow.

    The golden flows pay through the *simulated* ``test_gateway``, which
    ``payment_method_filter`` hides from checkout unless the install is in
    sandbox mode (``core.license.is_sandbox_mode``). Locally there's no
    production licence, so sandbox is already on; CI, however, bootstraps a
    signed **Community** licence in ``CoreConfig.ready()`` (a *production*
    licence), so the gateway was hidden, the payment list rendered empty, and
    every flow hung on a permanently-disabled ``continue-payment`` button.

    Forcing sandbox on here makes the simulated gateway appear regardless of
    licence state (a no-op where it's already on). ``payment_method_filter``
    imports the name at call time, so patching the module attribute reaches the
    live_server thread (same process) too.
    """
    from unittest import mock

    with mock.patch("core.license.is_sandbox_mode", return_value=True):
        yield


@pytest.fixture
def test_gateway_provider(db, test_gateway_on_disk):
    """An active PaymentProviderAccount bound to the real on-disk test_gateway
    provider so its embedded card form can be driven to completion.

    Two conditions must BOTH hold for it to appear in checkout: the provider
    code must be on disk (``test_gateway_on_disk`` unpacks it — components_data/
    is gitignored, so a fresh clone / CI has none) AND the install must be in
    sandbox mode (``_force_sandbox_mode`` above — CI's bootstrapped Community
    licence is otherwise non-sandbox and the filter hides simulated gateways).
    Miss either and the payment list is empty and every flow times out at
    checkout on a disabled continue-payment button."""
    from tests.factories import ComponentRegistryFactory, PaymentProviderAccountFactory

    component = ComponentRegistryFactory(slug="test_gateway", name="Test Gateway")
    return PaymentProviderAccountFactory(component=component)


def _fill_test_gateway_card(page, card_number):
    """Fill (but do not submit) the test_gateway embedded card form."""
    page.wait_for_selector("#tg-card-number", timeout=E2E_TIMEOUT_MS)
    page.fill("#tg-card-name", "Test Customer")
    page.fill("#tg-card-number", card_number)
    page.fill("#tg-card-expiry", "12/34")
    page.fill("#tg-card-cvc", "123")


def _complete_test_gateway_card(page, card_number="4242 4242 4242 4242"):
    """Fill and submit the card form, then wait for the confirmation redirect."""
    _fill_test_gateway_card(page, card_number)
    page.click("#tg-submit-btn")
    page.wait_for_url("**/checkout/confirmation/**", timeout=E2E_TIMEOUT_MS)
    # Let the confirmation page settle so no requests are in flight at teardown
    # (a page closed mid-request can deadlock the live_server DB flush under
    # transaction=True, cascading into later tests).
    page.wait_for_load_state("networkidle")


def _order_number_from_url(url: str) -> str:
    # Parse the path (drop any query/fragment) then take the final segment of
    # /en/checkout/confirmation/<order_number>/.
    from urllib.parse import urlparse

    return urlparse(url).path.rstrip("/").split("/")[-1]


def test_logged_in_card_checkout_creates_a_paid_order(
    product_page, checkout, site_settings, warehouse, test_gateway_provider
):
    """Golden flow (logged-in): browse → cart → checkout → card → confirmation,
    and the order lands paid with the amount charged equal to its total."""
    domestic_us_merchant()
    product = simple_product_scenario()["product"]

    product_page.go_to_product(product.slug)
    checkout.add_to_cart(product.id)
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

    summary = checkout.get_summary()
    # Guard: a priced total proves the cart was populated (add_to_cart worked)
    # and reached payment — so the charged==total assertion below isn't vacuous.
    total = parse_money(summary["total"])
    assert total > Decimal("0.00")

    checkout.select_payment_provider()
    _complete_test_gateway_card(checkout.page)

    order_number = _order_number_from_url(checkout.page.url)
    fp = footprint_for_order(order_number)
    order = assert_exactly_one_order(fp)
    assert order.payment_status == "paid"

    assert_charged_equals(fp, Amount(parse_money(summary["total"]), "USD"))


def test_guest_card_checkout_creates_a_paid_order(
    page, site_settings, warehouse, test_gateway_provider
):
    """Golden flow #1 (guest): an anonymous shopper completes a card checkout
    and the order lands paid, attributed to the email they entered — no account
    required."""
    from tests.e2e.conftest import CheckoutHelper

    # allow_guest_checkout defaults to True; no settings mutation needed
    # (and SiteSettings.save() would run unrelated multi-warehouse validation).
    domestic_us_merchant()
    product = simple_product_scenario()["product"]
    helper = CheckoutHelper(page)

    # Visit the product page first to establish a guest session + CSRF cookie,
    # then add to cart and drive checkout as a guest.
    page.goto(f"{helper.base_url}/en/product/{product.slug}/")
    page.wait_for_load_state("networkidle")
    helper.add_to_cart(product.id)

    helper.go_to_checkout()
    helper.submit_contact(email="guest@example.test")
    helper.fill_address(
        name="Guest Buyer",
        address1="456 Broadway",
        city="New York",
        state="NY",
        postal_code="10013",
        country="US",
    )
    helper.submit_address()
    helper.select_shipping_method("Standard Shipping")
    helper.wait_for_payment_step()

    summary = helper.get_summary()
    total = parse_money(summary["total"])
    assert total > Decimal("0.00")  # cart populated + priced (add_to_cart worked)

    helper.select_payment_provider()
    _complete_test_gateway_card(page)

    order_number = _order_number_from_url(page.url)
    fp = footprint_for_order(order_number)
    order = assert_exactly_one_order(fp)
    assert order.payment_status == "paid"
    assert order.email == "guest@example.test"  # attributed to the guest
    assert_charged_equals(fp, Amount(parse_money(summary["total"]), "USD"))


def test_payment_failure_then_retry_yields_one_paid_order(
    product_page, checkout, site_settings, warehouse, test_gateway_provider
):
    """Golden flow (recovery): a declined card is surfaced to the customer, who
    retries with a good card and succeeds — and the failed attempt leaves NO
    extra order. Exactly one order, paid. This is the browser-level proof of
    the retry-idempotency invariant."""
    domestic_us_merchant()
    product = simple_product_scenario()["product"]

    product_page.go_to_product(product.slug)
    checkout.add_to_cart(product.id)
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
    checkout.select_payment_provider()

    page = checkout.page

    # First attempt: a declined card. The gateway surfaces a retryable error and
    # the form stays put — no redirect, no paid order.
    _fill_test_gateway_card(page, "4000 0000 0000 0002")
    page.click("#tg-submit-btn")
    page.wait_for_selector("#tg-error-message", state="visible", timeout=E2E_TIMEOUT_MS)
    assert "confirmation" not in page.url

    # Retry with a good card → success.
    _complete_test_gateway_card(page, "4242 4242 4242 4242")

    fp = footprint_for_order(_order_number_from_url(page.url))
    order = assert_exactly_one_order(fp)
    assert order.payment_status == "paid"

    # The load-bearing recovery invariant: the failed attempt created NO second
    # order. The e2e DB is isolated per test (transaction=True), so a global
    # count of exactly one Order proves it (assert_exactly_one_order above only
    # inspects this order's own footprint).
    from orders.models import Order

    assert Order.objects.count() == 1


def test_voucher_checkout_applies_discount(
    product_page, checkout, site_settings, warehouse, test_gateway_provider
):
    """Golden flow (voucher): a $5 code entered at checkout reduces the total,
    the order records the discount, and the voucher redemption is tracked."""
    from tests.factories import VoucherFactory

    domestic_us_merchant()
    product = simple_product_scenario()["product"]
    VoucherFactory(fixed=True, code="SAVE5")  # $5.00 off

    product_page.go_to_product(product.slug)
    checkout.add_to_cart(product.id)
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

    page = checkout.page
    page.fill("#checkout-voucher-code", "SAVE5")
    page.click("#checkout-apply-voucher")
    # Wait for the summary to reflect the applied discount.
    page.wait_for_function(
        "() => { const d = document.getElementById('summary-discount');"
        " return d && /[1-9]/.test(d.textContent || ''); }",
        timeout=E2E_TIMEOUT_MS,
    )

    summary = checkout.get_summary()
    assert parse_money(summary["discount"]) == Decimal("5.00")  # UI reflects the discount

    checkout.select_payment_provider()
    _complete_test_gateway_card(page)

    fp = footprint_for_order(_order_number_from_url(page.url))
    order = assert_exactly_one_order(fp)
    assert order.payment_status == "paid"
    assert order.discount == Amount(Decimal("5.00"), "USD")  # discount recorded on the order
    assert len(fp.voucher_usages) == 1  # redemption tracked
    # The gateway charged exactly the (discounted) order total — not the
    # pre-discount amount. Assert against order.total, not the UI total, which
    # can be read mid-update.
    assert_charged_equals(fp, order.total)


def test_mixed_physical_and_digital_cart_checkout(
    product_page, checkout, site_settings, warehouse, test_gateway_provider
):
    """Golden flow (mixed cart): a physical + a digital item check out together;
    the order carries both lines and lands paid."""
    from tests.factories import CategoryFactory, ProductFactory

    domestic_us_merchant()
    physical = simple_product_scenario()["product"]
    digital = ProductFactory(
        name="Digital Extra",
        slug="digital-extra",
        status="published",
        digital=True,
        price=Decimal("9.99"),
        category=CategoryFactory(name="Downloads", slug="downloads"),
    )

    product_page.go_to_product(physical.slug)
    checkout.add_to_cart(physical.id)
    checkout.add_to_cart(digital.id)
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

    summary = checkout.get_summary()
    total = parse_money(summary["total"])
    assert total > Decimal("0.00")

    checkout.select_payment_provider()
    _complete_test_gateway_card(checkout.page)

    fp = footprint_for_order(_order_number_from_url(checkout.page.url))
    order = assert_exactly_one_order(fp)
    assert order.payment_status == "paid"
    assert len(order.lines) == 2  # physical + digital both present
    assert_charged_equals(fp, Amount(total, "USD"))


def test_gift_card_plus_card_split_payment(
    product_page, checkout, site_settings, warehouse, test_gateway_provider
):
    """Golden flow (gift-card tender): a $10 gift card covers part of the order
    and the gateway card covers the remainder — the order lands paid, the gift
    card redemption is recorded, and the gateway is charged only the remainder
    (not the full total)."""
    from djmoney.money import Money

    from catalog.models import GiftCard
    from commerce_footprint import total_captured
    from tests.factories import ProductFactory

    domestic_us_merchant()
    product = simple_product_scenario()["product"]
    gc_product = ProductFactory(product_type="gift_card", status="published")
    GiftCard.objects.create(
        code="GIFT10TEST",
        product=gc_product,
        initial_value=Money(Decimal("10.00"), "USD"),
        current_balance=Money(Decimal("10.00"), "USD"),
        is_active=True,
        recipient_email="giftee@example.test",
    )

    product_page.go_to_product(product.slug)
    checkout.add_to_cart(product.id)
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

    page = checkout.page
    page.fill("#tender-gift-card-code", "GIFT10TEST")
    page.click('[data-action="apply-gift-card"]')
    # Wait for the applied-tender row to render (gift card accepted).
    page.wait_for_function(
        "() => { const a = document.getElementById('tenders-applied');"
        " return a && a.children.length > 0; }",
        timeout=E2E_TIMEOUT_MS,
    )

    checkout.select_payment_provider()
    _complete_test_gateway_card(page)

    fp = footprint_for_order(_order_number_from_url(page.url))
    order = assert_exactly_one_order(fp)
    assert order.payment_status == "paid"
    # The $10 gift card was actually transacted against THIS card.
    assert any(
        e.gift_card_code == "GIFT10TEST" and abs(e.amount.value) == Decimal("10.00")
        for e in fp.gift_card_events
    )
    # The gateway was charged the REMAINDER (order total minus the $10 gift
    # card), proving the split — not the full amount.
    captured = total_captured(fp)
    assert captured is not None
    assert captured.value == order.total.value - Decimal("10.00")


@pytest.mark.parametrize("layout", ["multi_step", "single_page"])
def test_card_checkout_completes_through_layout(
    layout, product_page, checkout, site_settings, warehouse, test_gateway_provider
):
    """Golden flows #1 (single_page / one-page) and #2 (multi_step / multistep):
    a full card checkout is driven to a paid order through each non-default
    checkout layout — not just proven to render (Tier-2 template matrix), but
    actually completed end-to-end.

    The accordion (default) and express layouts are covered by the other golden
    flows; these close the pairwise "every checkout template driven to a paid
    order somewhere" requirement. The three step-based layouts share the same
    step partials, field IDs and ``continue-*`` actions on top of the base
    ``checkout.js`` controller, so the shared CheckoutHelper drives them — the
    only difference is the ``?template=`` selection."""
    domestic_us_merchant()
    product = simple_product_scenario()["product"]

    layout_marker = {
        "multi_step": ".checkout-container--multistep",
        "single_page": ".checkout-container--single-page",
    }[layout]

    product_page.go_to_product(product.slug)
    checkout.add_to_cart(product.id)
    checkout.go_to_checkout(template=layout)
    # Prove we're actually on the requested layout, not a silent fallback to the
    # default (only express falls back — but assert it so this stays honest if
    # that ever changes; otherwise a degraded flow would pass as this layout).
    assert checkout.page.query_selector(layout_marker) is not None, (
        f"{layout} layout marker {layout_marker} not present — wrong template rendered"
    )
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

    summary = checkout.get_summary()
    total = parse_money(summary["total"])
    assert total > Decimal("0.00")  # cart populated + priced through this layout

    checkout.select_payment_provider()
    _complete_test_gateway_card(checkout.page)

    order_number = _order_number_from_url(checkout.page.url)
    fp = footprint_for_order(order_number)
    order = assert_exactly_one_order(fp)
    assert order.payment_status == "paid"
    # A real charge equal to the order total moved through this layout — proof
    # the layout completes a checkout, not merely renders one.
    assert_charged_equals(fp, order.total)


def test_express_checkout_returning_customer(
    checkout, customer_user, site_settings, warehouse, test_gateway_provider
):
    """Golden flow (express): a returning customer with a saved default address
    checks out through the express template — a condensed flow that rides the
    saved address straight to shipping + payment — and the order lands paid."""
    from tests.factories import AddressFactory

    domestic_us_merchant()
    product = simple_product_scenario()["product"]
    AddressFactory(user=customer_user, is_default=True)  # so express doesn't fall back

    checkout.add_to_cart(product.id)
    page = checkout.page
    page.goto(f"{checkout.base_url}/en/checkout/?template=express")
    page.wait_for_load_state("networkidle")

    # Open the shipping-method picker (the change link toggles the panel and
    # fetches the methods), pick one, and confirm.
    page.click("#express-change-shipping-method")
    page.wait_for_selector(
        "#shipping-methods-list input[type='radio']", state="visible", timeout=E2E_TIMEOUT_MS
    )
    page.locator("#shipping-methods-list input[type='radio']").first.check()
    page.click("#express-confirm-shipping-method")

    # Confirming shipping walks forward to payment; selecting a provider applies
    # immediately and mounts the gateway card form.
    page.wait_for_selector(
        "#payment-providers-list .payment-provider-card input[type='radio']",
        state="visible",
        timeout=E2E_TIMEOUT_MS,
    )
    page.locator("#payment-providers-list .payment-provider-card input[type='radio']").first.check()

    _complete_test_gateway_card(page)

    fp = footprint_for_order(_order_number_from_url(page.url))
    order = assert_exactly_one_order(fp)
    assert order.payment_status == "paid"
    # A completed gateway capture equal to the total — proving a real charge,
    # not just a paid flag set without money moving.
    assert_charged_equals(fp, order.total)
