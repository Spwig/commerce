"""
Variable products display a variant price range.

A variable product's listing/PDP price is the range of its active variants'
effective prices — cheapest to most expensive — collapsing to a single price
when all variants match. Non-variable products (and variable products with no
priced variants) fall back to the single product price.
"""

from decimal import Decimal

import pytest
from djmoney.money import Money

from core.templatetags.currency_tags import product_price_range
from tests.factories import ProductFactory, ProductVariantFactory

pytestmark = [pytest.mark.django_db]


def _variable_with_variant_prices(amounts):
    product = ProductFactory(product_type="variable", price=Money("0.00", "USD"))
    for amount in amounts:
        ProductVariantFactory(
            product=product,
            pricing_strategy="custom",
            price=Money(str(amount), "USD"),
            is_active=True,
        )
    return product


# ---------------------------------------------------------------------------
# Product.get_variant_price_range
# ---------------------------------------------------------------------------


def test_range_returns_min_and_max_across_variants():
    product = _variable_with_variant_prices(["59.99", "89.99", "74.99"])
    low, high = product.get_variant_price_range("USD")
    assert low.amount == Decimal("59.99")
    assert high.amount == Decimal("89.99")


def test_range_collapses_when_all_variants_equal():
    product = _variable_with_variant_prices(["59.99", "59.99"])
    low, high = product.get_variant_price_range("USD")
    assert low.amount == high.amount == Decimal("59.99")


def test_range_is_none_for_non_variable_product():
    product = ProductFactory(product_type="simple", price=Money("24.99", "USD"))
    assert product.get_variant_price_range("USD") is None


def test_range_is_none_when_no_active_variants():
    product = ProductFactory(product_type="variable", price=Money("0.00", "USD"))
    assert product.get_variant_price_range("USD") is None


def test_range_ignores_inactive_variants():
    product = _variable_with_variant_prices(["59.99"])
    ProductVariantFactory(
        product=product, pricing_strategy="custom", price=Money("999.00", "USD"), is_active=False
    )
    low, high = product.get_variant_price_range("USD")
    assert low.amount == high.amount == Decimal("59.99")


# ---------------------------------------------------------------------------
# product_price_range filter
# ---------------------------------------------------------------------------


def test_filter_shows_single_price_when_variants_equal():
    product = _variable_with_variant_prices(["59.99", "59.99"])
    out = product_price_range(product, "USD")
    assert "59.99" in out
    assert "–" not in out  # no range separator


def test_filter_shows_range_when_variants_differ():
    product = _variable_with_variant_prices(["59.99", "89.99"])
    out = product_price_range(product, "USD")
    assert "59.99" in out
    assert "89.99" in out
    assert "–" in out


def test_filter_falls_back_to_single_price_for_simple_product():
    product = ProductFactory(product_type="simple", price=Money("24.99", "USD"))
    out = product_price_range(product, "USD")
    assert "24.99" in out
    assert "–" not in out
