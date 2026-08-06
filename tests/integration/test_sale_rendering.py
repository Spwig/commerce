"""
Sale/promotion rendering regression tests.

Guards the canonical sale mechanism after the sale-rendering audit: the shared
{% product_price_display %} tag, the ProductQuerySet.on_sale() filter, and the
cart line sale fields. Everything derives from sale_type/sale_value ->
effective_price/is_on_sale — there is no compare_at_price or sale_price field.
"""

from decimal import Decimal

import pytest
from djmoney.money import Money

from catalog.models import Product
from core.templatetags.currency_tags import product_price_display
from tests.factories import ProductFactory, ProductVariantFactory

pytestmark = [pytest.mark.django_db]


def _on_sale(**kwargs):
    """A published product on sale: $100 regular, $40 off -> $60 effective."""
    kwargs.setdefault("price", Money("100.00", "USD"))
    kwargs.setdefault("sale_type", "amount_off")
    kwargs.setdefault("sale_value", Decimal("40.00"))
    return ProductFactory(**kwargs)


# ---------------------------------------------------------------------------
# {% product_price_display %} tag
# ---------------------------------------------------------------------------


def test_simple_on_sale_shows_effective_and_strikethrough():
    ctx = product_price_display(_on_sale(product_type="simple"), "USD")
    assert ctx["on_sale"] is True
    assert "60" in ctx["current"]  # effective price
    assert ctx["original"] is not None and "100" in ctx["original"]  # struck-through regular


def test_simple_not_on_sale_has_no_strikethrough():
    p = ProductFactory(product_type="simple", price=Money("30.00", "USD"))
    ctx = product_price_display(p, "USD")
    assert ctx["on_sale"] is False
    assert ctx["original"] is None


def test_variable_on_sale_with_inheriting_variants_shows_sale():
    # Variants with no own price inherit the parent's sale, so the displayed
    # (collapsed) range IS discounted — show the strikethrough.
    p = _on_sale(product_type="variable")
    ProductVariantFactory(product=p)  # price=None -> inherits
    ProductVariantFactory(product=p)
    ctx = product_price_display(p, "USD")
    assert ctx["on_sale"] is True
    assert ctx["original"] is not None


def test_variable_on_sale_with_custom_variants_no_false_sale():
    # The parent is on sale, but variants carry their own (non-sale-adjusted)
    # prices, so the displayed range is NOT discounted — no misleading badge.
    p = _on_sale(product_type="variable")
    ProductVariantFactory(product=p, pricing_strategy="custom", price=Money("50.00", "USD"))
    ProductVariantFactory(product=p, pricing_strategy="custom", price=Money("70.00", "USD"))
    ctx = product_price_display(p, "USD")
    assert ctx["on_sale"] is False
    assert ctx["original"] is None


# ---------------------------------------------------------------------------
# ProductQuerySet.on_sale()
# ---------------------------------------------------------------------------


def test_on_sale_includes_amount_off():
    p = _on_sale(product_type="simple")
    assert Product.objects.filter(pk=p.pk).on_sale().exists()


def test_on_sale_excludes_fixed_price_not_below_regular():
    # A fixed_price sale at or above the regular price is not a discount.
    p = ProductFactory(
        product_type="simple",
        price=Money("50.00", "USD"),
        sale_type="fixed_price",
        sale_value=Decimal("60.00"),
    )
    assert not Product.objects.filter(pk=p.pk).on_sale().exists()


def test_on_sale_excludes_non_sale():
    p = ProductFactory(product_type="simple", price=Money("30.00", "USD"))
    assert not Product.objects.filter(pk=p.pk).on_sale().exists()


# ---------------------------------------------------------------------------
# Cart line sale fields
# ---------------------------------------------------------------------------


def test_cart_item_serializer_exposes_sale_fields():
    from cart.models import Cart, CartItem
    from cart.serializers import CartItemSerializer

    p = _on_sale(product_type="simple")  # $100 -> $60
    cart = Cart.objects.create(session_key="test-sale-rendering-cart")
    item = CartItem.objects.create(
        cart=cart,
        product=p,
        quantity=2,
        unit_price=p.effective_price,
        base_unit_price=p.price,
    )
    data = CartItemSerializer(item).data
    assert data["is_on_sale"] is True
    assert Decimal(data["total_price"]) == Decimal("120.00")  # 2 x 60 effective
    assert Decimal(data["regular_total"]) == Decimal("200.00")  # 2 x 100 regular


# ---------------------------------------------------------------------------
# Search — effective price for display AND for the min/max price filter
# ---------------------------------------------------------------------------


@pytest.fixture
def search_setup():
    """Site + enabled SearchSettings + a 'shop' engine, so SearchService runs."""
    from django.contrib.sites.models import Site

    from search.models import SearchEngine, SearchSettings

    Site.objects.get_or_create(pk=1, defaults={"domain": "testserver", "name": "Test"})
    settings = SearchSettings.get_settings()
    settings.is_enabled = True
    settings.save()
    SearchEngine.objects.get_or_create(
        slug="shop",
        defaults={"name": "Shop Search", "is_active": True, "content_types": ["product"]},
    )


def _search_products(term, **filters):
    from search.services.search_service import SearchService

    res = SearchService().search(term, language="en", filters=filters or None)
    return [d for d in res.get("results", []) if isinstance(d, dict) and d.get("type") == "product"]


def _find(results, slug):
    return next((d for d in results if d.get("slug") == slug), None)


def test_search_shows_effective_price_and_regular(search_setup):
    # $100 regular, $40 off -> $60 effective. Distinctive token so it's findable.
    p = _on_sale(product_type="simple", name="Zzql Sale Widget")
    hit = _find(_search_products("Zzql"), p.slug)
    assert hit is not None
    assert hit["price"] == "60.00"  # effective — what the customer pays
    assert hit["regular_price"] == "100.00"  # struck-through regular
    assert hit["is_on_sale"] is True


def test_search_non_sale_has_no_regular_price(search_setup):
    p = ProductFactory(product_type="simple", name="Zzql Plain Widget", price=Money("30.00", "USD"))
    hit = _find(_search_products("Zzql"), p.slug)
    assert hit is not None
    assert hit["price"] == "30.00"
    assert hit["regular_price"] is None
    assert hit["is_on_sale"] is False


def test_search_price_filter_uses_effective_not_regular(search_setup):
    # $100 -> $60. A max_price between effective and regular MUST include it;
    # filtering on the base price would wrongly drop it.
    p = _on_sale(product_type="simple", name="Zzql Filtered Widget")  # eff 60, base 100
    assert _find(_search_products("Zzql", max_price=80), p.slug) is not None  # 60 <= 80
    assert _find(_search_products("Zzql", max_price=50), p.slug) is None  # 60 > 50
    assert _find(_search_products("Zzql", min_price=55), p.slug) is not None  # 60 >= 55


def test_search_variable_custom_variants_no_false_sale(search_setup):
    # Parent is on sale, but the variants carry their own (non-sale-adjusted)
    # prices, so search must NOT show a discount — fall back to the regular price.
    p = _on_sale(product_type="variable", name="Zzql Variant Widget")
    ProductVariantFactory(product=p, pricing_strategy="custom", price=Money("50.00", "USD"))
    ProductVariantFactory(product=p, pricing_strategy="custom", price=Money("70.00", "USD"))
    hit = _find(_search_products("Zzql"), p.slug)
    assert hit is not None
    assert hit["is_on_sale"] is False
    assert hit["regular_price"] is None
    assert hit["price"] == "100.00"  # regular parent price, not the parent's effective

    # ...and the price filter must use that same regular price, not the parent's
    # sale price — otherwise it would include a product shown at $100 under an
    # $80 ceiling.
    assert _find(_search_products("Zzql", max_price=80), p.slug) is None  # 100 > 80
    assert _find(_search_products("Zzql", max_price=120), p.slug) is not None  # 100 <= 120
