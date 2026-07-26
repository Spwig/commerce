"""
The gift card product page (P2.5e-2) — the form web sales were missing.

P2.3 made gift cards purchasable at the API level, but GiftCardDataSerializer
requires recipient_email and NOTHING in the storefront collected it: the
product rendered on a generic template whose add-to-cart always refused. The
docs, meanwhile, said selling was live. This template closes that gap, and its
form mirrors the serializer's rules exactly — whatever the form lets through,
the server accepts.
"""

from decimal import Decimal

import pytest
from djmoney.money import Money

from tests.factories import ProductFactory

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.r2]


def _gift_card_product(**kwargs):
    defaults = {
        "product_type": "gift_card",
        "status": "published",
        "price": Money(Decimal("25.00"), "USD"),
    }
    defaults.update(kwargs)
    return ProductFactory(**defaults)


class TestTemplateSelection:
    def test_gift_card_products_get_the_gift_card_template(self, client, site_settings):
        product = _gift_card_product(
            gift_card_denomination_type="fixed",
            gift_card_denominations=[25, 50, 100],
        )

        resp = client.get(f"/en/product/{product.slug}/")

        assert resp.status_code == 200
        content = resp.content.decode()
        assert "gift-card-form" in content, (
            "Without this form the product is visible but unbuyable — the API "
            "refuses every add-to-cart for want of a recipient."
        )
        assert 'id="gc-recipient-email"' in content
        assert "gift-card-config" in content

    def test_fixed_denominations_render_as_buttons(self, client, site_settings):
        product = _gift_card_product(
            gift_card_denomination_type="fixed",
            gift_card_denominations=[25, 50, 100],
        )

        content = client.get(f"/en/product/{product.slug}/").content.decode()

        assert content.count("gift-card-denom") >= 3
        # Fixed-only: no free-amount input.
        assert 'id="gc-custom-amount"' not in content

    def test_custom_type_renders_the_amount_input_with_bounds(self, client, site_settings):
        product = _gift_card_product(
            gift_card_denomination_type="custom",
            gift_card_min_amount=Decimal("5.00"),
            gift_card_max_amount=Decimal("500.00"),
        )

        content = client.get(f"/en/product/{product.slug}/").content.decode()

        assert 'id="gc-custom-amount"' in content
        assert 'min="5.00"' in content
        assert 'max="500.00"' in content

    def test_both_type_renders_buttons_and_input(self, client, site_settings):
        product = _gift_card_product(
            gift_card_denomination_type="both",
            gift_card_denominations=[25, 50],
            gift_card_min_amount=Decimal("5.00"),
            gift_card_max_amount=Decimal("500.00"),
        )

        content = client.get(f"/en/product/{product.slug}/").content.decode()

        assert "gift-card-denom" in content
        assert 'id="gc-custom-amount"' in content

    def test_ordinary_products_are_untouched(self, client, site_settings):
        product = ProductFactory(product_type="simple", status="published")

        content = client.get(f"/en/product/{product.slug}/").content.decode()

        assert "gift-card-form" not in content
