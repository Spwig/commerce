"""
Plain digital products must not be stock-gated.

A ``product_type="digital"`` product is delivered as a download/licence and
has no physical stock. The admin hides the Inventory fieldset
(admin_product_form.js) and the StockItemInline (ProductAdmin.get_inlines)
for it, so a merchant can never create a StockItem. But the model default is
``track_inventory=True`` and, before this fix, ``Product.save()`` cleared it
only for ``gift_card`` and ``booking`` — not for a plain ``digital`` product.
The result: a digital product silently kept ``track_inventory=True``, had zero
StockItems, so ``available_stock == 0`` and every add-to-cart failed with
"Insufficient stock".

``Product.save()`` now forces ``track_inventory=False`` for digital, mirroring
the gift_card/booking handling.

Note: ``ProductFactory`` defaults ``track_inventory`` to False, so it is set
explicitly to True below — otherwise these assertions pass vacuously and would
never catch a regression.
"""

import pytest

from tests.factories import CartFactory, ProductFactory, UserFactory

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.integration,
]


def test_save_forces_track_inventory_off_for_digital():
    product = ProductFactory(product_type="digital", track_inventory=True)
    product.refresh_from_db()

    assert product.is_digital is True
    assert product.requires_shipping is False
    assert product.track_inventory is False
    assert product.is_in_stock is True


def test_digital_product_can_be_added_to_cart_without_stock(site_settings):
    """
    The real regression: a digital product created with the field default
    (``track_inventory=True``) and no StockItem must still add to cart. Before
    the fix this failed with "Insufficient stock".
    """
    from cart.services.cart_service import CartService

    cart = CartFactory(user=UserFactory())
    product = ProductFactory(product_type="digital", track_inventory=True)

    success, message, item = CartService.add_item(cart, product.id, quantity=1)

    assert success is True, f"digital product was refused: {message}"
    assert item is not None
    assert cart.items.count() == 1


@pytest.mark.parametrize("product_type", ["simple", "variable"])
def test_non_digital_products_keep_their_track_inventory(product_type):
    """
    The fix must be scoped to digital/booking/gift_card. A physical product
    that opts into inventory tracking must keep it.
    """
    product = ProductFactory(product_type=product_type, track_inventory=True)
    product.refresh_from_db()

    assert product.track_inventory is True
