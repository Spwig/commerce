"""
Regression tests: bundle component items must not be taxed.

A bundle is stored as a parent `CartItem` carrying the bundle's price, plus
one child `CartItem` per component carrying that component's own price. Every
money aggregation on `Cart` excludes children (`parent_bundle_id is None`) —
`total_amount`, `total_items`, `total_savings`, and voucher-eligible amount —
because the customer is billed the bundle price, not the sum of its parts.

`CheckoutSession._calculate_tax` did not apply that filter, so a bundle whose
components price higher than the bundle itself was taxed on the sum of
*parent + children*. `CheckoutService.create_order` copies `session.tax_amount`
verbatim onto the Order, so the over-tax was collected.
"""

from decimal import Decimal

import pytest

from tests.factories import (
    AddressFactory,
    CartFactory,
    CartItemFactory,
    CheckoutSessionFactory,
    ProductFactory,
    TaxRateFactory,
)

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.integration,
    pytest.mark.tax,
    pytest.mark.checkout,
]


@pytest.fixture
def us_ny_tax(db):
    """8.88% NY sales tax, not applied to shipping."""
    return TaxRateFactory(ny=True)


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
def bundle_cart(db, customer_user, site_settings):
    """
    A cart holding one bundle priced at $100 whose two components would
    price at $120 standalone.

    Billed subtotal is $100. Anything taxing $220 is taxing goods the
    customer was never charged for.
    """
    cart = CartFactory(user=customer_user)

    bundle_product = ProductFactory(
        name="Starter Bundle",
        price=Decimal("100.00"),
        product_type="bundle",
    )
    component_a = ProductFactory(name="Component A", price=Decimal("70.00"))
    component_b = ProductFactory(name="Component B", price=Decimal("50.00"))

    parent = CartItemFactory(
        cart=cart,
        product=bundle_product,
        quantity=1,
        unit_price=Decimal("100.00"),
        parent_bundle=None,
    )
    CartItemFactory(
        cart=cart,
        product=component_a,
        quantity=1,
        unit_price=Decimal("70.00"),
        parent_bundle=parent,
    )
    CartItemFactory(
        cart=cart,
        product=component_b,
        quantity=1,
        unit_price=Decimal("50.00"),
        parent_bundle=parent,
    )
    return cart


class TestBundleComponentsAreNotTaxed:
    def test_cart_subtotal_excludes_components(self, bundle_cart):
        """Baseline: the billed subtotal is the bundle price, not the sum of parts."""
        assert bundle_cart.total_amount.amount == Decimal("100.00")

    def test_tax_is_charged_on_the_billed_subtotal(self, bundle_cart, ny_address, us_ny_tax):
        """
        Tax base must be the subtotal the customer is billed.

        Before the fix this computed tax on $220 (100 + 70 + 50) and returned
        $19.54 instead of $8.88.
        """
        session = CheckoutSessionFactory(cart=bundle_cart, shipping_address=ny_address)

        tax, _breakdown = session._calculate_tax()

        expected = (Decimal("100.00") * Decimal("0.0888")).quantize(Decimal("0.01"))
        assert tax == expected, (
            f"Tax was {tax}, expected {expected}. A value near "
            f"{(Decimal('220.00') * Decimal('0.0888')).quantize(Decimal('0.01'))} "
            f"means bundle components are being taxed."
        )

    def test_recalculate_totals_taxes_only_the_bundle_price(
        self, bundle_cart, ny_address, us_ny_tax
    ):
        """End-to-end through the path that writes onto the Order."""
        session = CheckoutSessionFactory(cart=bundle_cart, shipping_address=ny_address)

        session.recalculate_totals()
        session.refresh_from_db()

        assert session.subtotal.amount == Decimal("100.00")
        assert session.tax_amount.amount == Decimal("8.88")
        assert session.total_amount.amount == Decimal("108.88")

    def test_tax_base_matches_subtotal_for_a_plain_cart(
        self, db, customer_user, site_settings, ny_address, us_ny_tax
    ):
        """A cart with no bundles must be unaffected by the fix."""
        cart = CartFactory(user=customer_user)
        CartItemFactory(
            cart=cart,
            product=ProductFactory(price=Decimal("40.00")),
            quantity=2,
            unit_price=Decimal("40.00"),
            parent_bundle=None,
        )
        session = CheckoutSessionFactory(cart=cart, shipping_address=ny_address)

        tax, _ = session._calculate_tax()

        assert cart.total_amount.amount == Decimal("80.00")
        assert tax == (Decimal("80.00") * Decimal("0.0888")).quantize(Decimal("0.01"))

    def test_bundle_quantity_scales_the_tax_base(self, bundle_cart, ny_address, us_ny_tax):
        """Two of the same bundle taxes $200, not $440."""
        parent = bundle_cart.items.get(parent_bundle__isnull=True)
        parent.quantity = 2
        parent.save(update_fields=["quantity"])

        session = CheckoutSessionFactory(cart=bundle_cart, shipping_address=ny_address)
        tax, _ = session._calculate_tax()

        assert bundle_cart.total_amount.amount == Decimal("200.00")
        assert tax == (Decimal("200.00") * Decimal("0.0888")).quantize(Decimal("0.01"))
