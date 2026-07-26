"""
Regression tests for the multi-currency checkout-breaking bug.

Background
----------
With multi-currency enabled, cart items could end up holding a ``unit_price``
in a currency different from their cart's ``effective_currency`` — e.g. a
product priced in EUR added to a USD cart, or the shopper switched session
currency and existing line items were never repriced. Any Money sum/comparison
across mixed currencies raises ``TypeError``, so ``cart.final_amount``,
``CheckoutSession.recalculate_totals()`` and the ``/api/cart/`` and
``/api/checkout/`` endpoints all returned 500 (infinite spinners in the
storefront).

The fix has two parts, both exercised here:

1. ``CartService.sync_cart_currency(cart)`` — called at the end of
   ``get_or_create_cart`` — reprices any item whose currency differs from the
   cart's, and is safe against conversion failures (logs and leaves the item
   unchanged rather than raising).
2. ``CartItem.savings`` — converts the product's regular price before comparing
   when its currency differs from ``unit_price``, and returns ``Money(0, ...)``
   on conversion failure instead of raising.

These are service/model-level tests (no HTTP). The end-to-end API coverage
lives in ``tests/integration/test_cart_currency_sync_api.py``.
"""

from decimal import Decimal
from unittest.mock import patch

import pytest
from djmoney.money import Money

from cart.services.cart_service import CartService
from tests.factories import CartFactory, CartItemFactory, ProductFactory

pytestmark = [pytest.mark.django_db]

# The class is imported lazily inside both cart_service.sync_cart_currency and
# CartItem.savings, so patch it on the source module (see agent-memory: lazy
# imports must be patched where they are defined). Both the simple-item FX
# fallback and every derived/customization conversion go through .convert.
FX_CONVERT = "exchange_rates.services.exchange_service.ExchangeRateService.convert"


@pytest.fixture(autouse=True)
def usd_site(db):
    """Site + SiteSettings with USD default currency, and a clean FX cache.

    Required because sync_cart_currency instantiates ExchangeRateService(),
    whose __init__ calls Site.objects.get_current() (SITE_ID=1) and
    SiteSettings.get_settings(). Multi-currency stays disabled — the repricing
    path does not depend on it, and leaving it off avoids the clean() provider
    validation dance.

    We also clear the process/Redis cache: sync_cart_currency negative-caches
    failed currency pairs under ``cart_fx_sync_fail:{source}:{target}`` for
    300s, and with pytest.ini's --reuse-db that key survives across runs and
    across tests, silently skipping repricing and poisoning unrelated tests.
    """
    from django.contrib.sites.models import Site
    from django.core.cache import cache

    from core.models import SiteSettings

    cache.clear()
    Site.objects.get_or_create(id=1, defaults={"domain": "localhost", "name": "Test"})
    settings, _ = SiteSettings.objects.get_or_create(
        pk=1,
        defaults={
            "site_name": "Test Store",
            "admin_email": "admin@test.spwig.com",
            "default_currency": "USD",
            "default_language": "en",
        },
    )
    if settings.default_currency != "USD":
        SiteSettings.objects.filter(pk=settings.pk).update(default_currency="USD")
        settings.refresh_from_db()
    return settings


@pytest.fixture
def usd_product(db):
    """Simple product priced in USD (matches the store default)."""
    return ProductFactory(
        name="USD Widget Sync",
        slug="usd-widget-sync",
        price=Decimal("25.00"),
        price_currency="USD",
    )


@pytest.fixture
def eur_product(db):
    """Simple product priced in EUR (differs from the USD store default)."""
    return ProductFactory(
        name="EUR Widget Sync",
        slug="eur-widget-sync",
        price=Decimal("49.99"),
        price_currency="EUR",
    )


# ============================================================
# A. sync_cart_currency — plain (simple) items
# ============================================================


class TestSyncCartCurrencySimpleItem:
    """A plain product line stored in the wrong currency is repriced through
    the normal pricing path (product.get_price_in_currency)."""

    def test_eur_item_in_usd_cart_is_repriced_to_usd(self, usd_product):
        """An item stranded in EUR inside a USD cart is repriced to USD.

        product is priced in USD, so get_price_in_currency('USD') returns the
        base price directly — no exchange rate needed, fully deterministic.
        """
        cart = CartFactory(user=None, session_key="sync_simple_1", currency="USD")
        item = CartItemFactory(
            cart=cart,
            product=usd_product,
            quantity=1,
            unit_price=Decimal("49.99"),
            unit_price_currency="EUR",
        )
        # Precondition: the line really is mismatched.
        assert str(item.unit_price.currency) == "EUR"

        repriced = CartService.sync_cart_currency(cart)

        assert repriced is True
        item.refresh_from_db()
        assert str(item.unit_price.currency) == "USD"
        # Repriced through the pricing path to the product's USD base price.
        assert item.unit_price.amount == Decimal("25.00")

    def test_already_consistent_cart_is_not_repriced(self, usd_product):
        """When every item already matches the cart currency, nothing changes."""
        cart = CartFactory(user=None, session_key="sync_simple_2", currency="USD")
        item = CartItemFactory(
            cart=cart,
            product=usd_product,
            quantity=1,
            unit_price=Decimal("25.00"),
            unit_price_currency="USD",
        )

        repriced = CartService.sync_cart_currency(cart)

        assert repriced is False
        item.refresh_from_db()
        assert str(item.unit_price.currency) == "USD"
        assert item.unit_price.amount == Decimal("25.00")

    def test_get_or_create_cart_reprices_and_final_amount_no_longer_raises(self, usd_product):
        """The real entry point (get_or_create_cart) reprices the cart, and the
        previously-500ing cart.final_amount arithmetic then succeeds."""
        cart = CartFactory(user=None, session_key="sync_simple_3", currency="USD")
        CartItemFactory(
            cart=cart,
            product=usd_product,
            quantity=2,
            unit_price=Decimal("49.99"),
            unit_price_currency="EUR",
        )

        # Regression precondition: mixed currency breaks the money arithmetic
        # that the cart/checkout APIs rely on. total_amount yields Money(EUR)
        # while the zero-valued voucher discount defaults to the cart currency
        # (USD), so the subtraction raises — this is the exact former 500.
        with pytest.raises(TypeError):
            _ = cart.final_amount

        synced_cart = CartService.get_or_create_cart(session_key="sync_simple_3")

        assert synced_cart.id == cart.id
        # After sync the arithmetic is safe.
        assert str(synced_cart.final_amount.currency) == "USD"
        assert synced_cart.final_amount.amount == Decimal("50.00")  # 2 x 25.00


# ============================================================
# B. sync_cart_currency — derived-price items
# ============================================================


class TestSyncCartCurrencyDerivedItem:
    """Items carrying a derived price (customizations, bundles, subscriptions)
    are rate-converted, and their per-customization calculated_price values are
    scaled by the same rate."""

    def test_customization_item_is_converted_and_calculated_prices_scaled(self, usd_product):
        """A line with customizations is converted from its base_unit_price
        anchor, and each calculated_price in the customizations dict is
        converted by the same base->target rate."""
        cart = CartFactory(user=None, session_key="sync_derived_1", currency="USD")
        item = CartItemFactory(
            cart=cart,
            product=usd_product,
            quantity=1,
            unit_price=Decimal("100.00"),
            unit_price_currency="EUR",
            customizations={
                "5": {"value": "engrave", "calculated_price": "10.00"},
                "7": {"value": "giftwrap", "calculated_price": "4.00"},
            },
        )
        # base_unit_price is anchored to the as-priced value on first save.
        assert str(item.base_unit_price.currency) == "EUR"

        # Both the unit price and every customization are converted through
        # ExchangeRateService.convert(base_amount, base_currency, target).
        def fake_convert(amount, from_currency, to_currency):
            assert from_currency == "EUR" and to_currency == "USD"
            return Decimal(str(amount)) * Decimal("1.10")

        with patch(FX_CONVERT, side_effect=fake_convert):
            repriced = CartService.sync_cart_currency(cart)

        assert repriced is True
        item.refresh_from_db()
        # unit_price converted EUR -> USD at 1.10
        assert str(item.unit_price.currency) == "USD"
        assert item.unit_price.amount == Decimal("110.00")
        # Each stored calculated_price converted by the same base->target rate.
        assert item.customizations["5"]["calculated_price"] == "11.00"
        assert item.customizations["7"]["calculated_price"] == "4.40"
        # Non-price fields untouched.
        assert item.customizations["5"]["value"] == "engrave"


# ============================================================
# C. sync_cart_currency — conversion failure is non-fatal
# ============================================================


class TestSyncCartCurrencyConversionFailure:
    """A conversion failure must log and leave the item unchanged — it must
    never raise, or the whole cart/checkout request 500s again."""

    def test_conversion_failure_leaves_item_unchanged(self, eur_product):
        """When the FX service raises, the mismatched item is left as-is."""
        cart = CartFactory(user=None, session_key="sync_fail_1", currency="USD")
        item = CartItemFactory(
            cart=cart,
            product=eur_product,
            quantity=1,
            unit_price=Decimal("49.99"),
            unit_price_currency="EUR",
        )

        # Simple item -> get_price_in_currency returns EUR base (multi-currency
        # off), then the explicit rate-convert fallback calls .convert(), which
        # we force to raise.
        with patch(FX_CONVERT, side_effect=Exception("provider down")):
            repriced = CartService.sync_cart_currency(cart)

        assert repriced is False
        item.refresh_from_db()
        assert str(item.unit_price.currency) == "EUR"
        assert item.unit_price.amount == Decimal("49.99")

    def test_get_or_create_cart_does_not_raise_when_conversion_fails(self, eur_product):
        """get_or_create_cart still returns the cart even if repricing can't
        complete — a dead FX provider must not take down the cart."""
        cart = CartFactory(user=None, session_key="sync_fail_2", currency="USD")
        CartItemFactory(
            cart=cart,
            product=eur_product,
            quantity=1,
            unit_price=Decimal("49.99"),
            unit_price_currency="EUR",
        )

        with patch(FX_CONVERT, side_effect=Exception("provider down")):
            returned = CartService.get_or_create_cart(session_key="sync_fail_2")

        assert returned.id == cart.id


# ============================================================
# D. CartItem.savings — cross-currency handling
# ============================================================


class TestCartItemSavingsCrossCurrency:
    """CartItem.savings must convert the product's regular price before
    comparing, and must return zero (never raise) when conversion fails.
    A savings display nicety was the exact source of the former 500."""

    def test_savings_converts_regular_price_before_comparing(self, eur_product):
        """product.price is EUR, unit_price is USD: the regular price is
        converted to USD and savings computed in USD."""
        cart = CartFactory(user=None, session_key="savings_1", currency="USD")
        # eur_product.price = EUR 49.99; store the line in USD below its regular
        # price so there is a positive saving after conversion.
        item = CartItemFactory(
            cart=cart,
            product=eur_product,
            quantity=2,
            unit_price=Decimal("40.00"),
            unit_price_currency="USD",
        )

        # Regular EUR 49.99 -> USD 55.00 (mocked). 55.00 > 40.00 -> saving 15.00/unit.
        with patch(FX_CONVERT, return_value=Decimal("55.00")):
            savings = item.savings

        assert str(savings.currency) == "USD"
        assert savings.amount == Decimal("30.00")  # (55.00 - 40.00) x 2

    def test_savings_returns_zero_money_on_conversion_failure(self, eur_product):
        """This is the exact former-500 regression: a cross-currency savings
        comparison must degrade to Money(0, unit_price.currency), not raise."""
        cart = CartFactory(user=None, session_key="savings_2", currency="USD")
        item = CartItemFactory(
            cart=cart,
            product=eur_product,
            quantity=1,
            unit_price=Decimal("40.00"),
            unit_price_currency="USD",
        )

        with patch(FX_CONVERT, side_effect=Exception("provider down")):
            savings = item.savings  # must not raise

        assert savings == Money(0, "USD")

    def test_savings_same_currency_unaffected(self, usd_product):
        """Same-currency lines skip conversion entirely (no regression)."""
        cart = CartFactory(user=None, session_key="savings_3", currency="USD")
        # usd_product.price = USD 25.00; line stored at USD 20.00 -> saving 5.00.
        item = CartItemFactory(
            cart=cart,
            product=usd_product,
            quantity=1,
            unit_price=Decimal("20.00"),
            unit_price_currency="USD",
        )

        savings = item.savings
        assert savings == Money(Decimal("5.00"), "USD")
