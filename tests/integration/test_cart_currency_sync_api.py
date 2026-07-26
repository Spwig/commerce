"""
End-to-end regression coverage for the multi-currency checkout-breaking bug.

A cart holding a line in a currency different from the cart's own currency made
every Money aggregation raise TypeError, so ``/api/cart/`` and ``/api/checkout/``
returned 500 (the storefront showed infinite spinners). The fix reprices such
lines inside ``CartService.get_or_create_cart`` — which both endpoints route
through — so they now return 200.

These tests drive the real HTTP endpoints via DRF's APIClient.
"""

from decimal import Decimal

import pytest

from tests.factories import CartFactory, CartItemFactory, ProductFactory

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.checkout]


@pytest.fixture(autouse=True)
def _clear_fx_cache():
    """sync_cart_currency negative-caches failed currency pairs under
    ``cart_fx_sync_fail:{source}:{target}`` (300s). With pytest.ini's
    --reuse-db that key survives across runs and would skip repricing here,
    turning a 200 back into a 500. Start each test from a clean cache."""
    from django.core.cache import cache

    cache.clear()
    yield


@pytest.fixture
def usd_product(db, category):
    """Simple product priced in USD (matches the store default)."""
    return ProductFactory(
        name="USD Widget API",
        slug="usd-widget-api",
        category=category,
        price=Decimal("25.00"),
        price_currency="USD",
    )


@pytest.fixture
def mismatched_cart(db, customer_user, usd_product, site_settings):
    """The customer's regular cart (session_key IS NULL) carrying a EUR line in
    a USD cart — the mixed-currency state that used to 500 the APIs.

    get_or_create_cart(user=...) resolves to exactly this cart, so fetching
    either endpoint triggers sync_cart_currency on it.
    """
    cart = CartFactory(user=customer_user, currency="USD")
    CartItemFactory(
        cart=cart,
        product=usd_product,
        quantity=2,
        unit_price=Decimal("49.99"),
        unit_price_currency="EUR",
    )
    return cart


class TestCartCurrencySyncEndToEnd:
    def test_mixed_currency_is_the_pre_fix_500(self, mismatched_cart):
        """Sanity-check the regression is genuinely reproduced: before any sync
        runs, the money arithmetic the cart/checkout serializers rely on raises.
        """
        with pytest.raises(TypeError):
            _ = mismatched_cart.final_amount

    def test_get_cart_returns_200_and_reprices(self, auth_client, mismatched_cart):
        """GET /api/cart/ returns 200 (not 500) and the stranded EUR line is
        repriced into the cart's USD currency."""
        resp = auth_client.get("/api/cart/")
        assert resp.status_code == 200, resp.content

        item = mismatched_cart.items.first()
        item.refresh_from_db()
        assert str(item.unit_price.currency) == "USD"
        assert item.unit_price.amount == Decimal("25.00")

    def test_checkout_session_returns_200(self, auth_client, mismatched_cart):
        """GET /api/checkout/ returns 200 — recalculate_totals no longer trips
        over the mixed-currency line."""
        resp = auth_client.get("/api/checkout/")
        assert resp.status_code == 200, resp.content
        data = resp.json()
        assert data["success"] is True
        session = data["session"]
        # 2 x 25.00 after repricing.
        assert Decimal(session["subtotal"]) == Decimal("50.00")

    def test_cart_then_checkout_both_succeed(self, auth_client, mismatched_cart):
        """The full storefront path: fetch the cart, then the checkout session —
        both 200 after a single repricing pass."""
        assert auth_client.get("/api/cart/").status_code == 200
        assert auth_client.get("/api/checkout/").status_code == 200
