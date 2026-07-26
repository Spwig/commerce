"""
Regression coverage for today's ``apply_voucher`` float(Money) fix.

``cart/views.py::CartViewSet.apply_voucher`` built its success response with
``float(discount_amount)``. On the success path ``CartService.apply_voucher``
returns a ``Money`` (from ``VoucherCode.calculate_discount``), and
``float(Money(...))`` raises ``TypeError`` — so a *successful* voucher apply
500'd. (Failure paths return a bare ``Decimal``, so only the happy path broke.)

The fix coalesces to the underlying amount before ``float``::

    amount = getattr(discount_amount, "amount", discount_amount)
    ... "discount_amount": float(amount) ...

Driven through the real HTTP endpoint via DRF's APIClient.
"""

from decimal import Decimal

import pytest

from tests.factories import CartFactory, CartItemFactory, ProductFactory, VoucherFactory

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.checkout]

APPLY_URL = "/api/cart/apply-voucher/"


@pytest.fixture
def priced_product(db, category):
    return ProductFactory(
        name="Voucher Widget",
        slug="voucher-widget",
        category=category,
        price=Decimal("40.00"),
        price_currency="USD",
    )


@pytest.fixture
def user_cart_with_item(db, customer_user, priced_product, site_settings):
    """The signed-in customer's account cart (session_key IS NULL) with one
    USD line — ``get_or_create_cart(user=...)`` resolves to exactly this cart."""
    cart = CartFactory(user=customer_user, currency="USD")
    CartItemFactory(
        cart=cart,
        product=priced_product,
        quantity=1,
        unit_price=Decimal("40.00"),
        unit_price_currency="USD",
    )
    return cart


class TestApplyVoucherMoneyFix:
    def test_successful_apply_returns_200_with_float_discount(
        self, auth_client, user_cart_with_item
    ):
        """POST /api/cart/apply-voucher/ with a valid percentage voucher returns
        200 (pre-fix: 500), success=True, a float discount_amount, and the cart
        payload — the exact response shape the storefront consumes."""
        voucher = VoucherFactory(
            code="SAVE10",
            discount_type="percentage",
            discount_value=Decimal("10.00"),
            application_scope="cart",
            currency="USD",
        )

        resp = auth_client.post(APPLY_URL, {"code": voucher.code}, format="json")

        assert resp.status_code == 200, resp.content
        body = resp.json()
        assert body["success"] is True
        # The regression itself: discount_amount is a JSON number (float), not
        # a 500. 10% of a single $40 line.
        assert isinstance(body["discount_amount"], float)
        assert body["discount_amount"] == pytest.approx(4.0)
        assert "cart" in body

        # And the voucher genuinely landed on the account cart.
        assert user_cart_with_item.applied_vouchers.filter(voucher=voucher).exists()

    def test_invalid_code_still_returns_structured_400(self, auth_client, user_cart_with_item):
        """Guard against a false positive: the failure path (which returns a
        bare Decimal, never a Money) must keep working — a bogus code yields a
        clean 400, not a 500 and not a spurious success."""
        resp = auth_client.post(APPLY_URL, {"code": "NOPE-DOES-NOT-EXIST"}, format="json")

        assert resp.status_code == 400, resp.content
        body = resp.json()
        assert body["success"] is False
