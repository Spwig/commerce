"""
R1 coverage: ``Product.requires_shipping`` promoted from property to column.

``requires_shipping`` used to be a ``@property`` returning
``product_type not in ("digital", "booking")``. ``cart/models.py`` filters on
``product__requires_shipping=True`` in three places, and the ORM cannot resolve
a property — so the shippable-cart path raised ``FieldError`` at query time.

Migration ``catalog/0005`` adds the column and backfills it by replaying the
old property exactly, so no existing product changes behaviour. Two things need
pinning: that the ORM queries now work, and that the semantics are unchanged.

Plan: docs/.claude_code/plans/wondrous-moseying-wolf.md (R1 / P1.2)
"""

import pytest

from tests.factories import CartFactory, CartItemFactory, ProductFactory

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.integration,
    pytest.mark.r1,
]


# The types the old property treated as non-shippable.
NON_SHIPPABLE_TYPES = ("digital", "booking")


def _old_property_semantics(product_type):
    """What the pre-migration ``@property`` would have returned."""
    return product_type not in NON_SHIPPABLE_TYPES


# ============================================================
# It is a real, queryable field
# ============================================================


class TestRequiresShippingIsQueryable:
    """These queries raised ``FieldError`` before the migration."""

    def test_product_can_be_filtered_on_requires_shipping(self):
        from catalog.models import Product

        shippable = ProductFactory(product_type="simple")
        ProductFactory(product_type="digital")

        result = Product.objects.filter(requires_shipping=True)

        assert shippable in result
        assert result.filter(product_type="digital").count() == 0

    def test_product_can_be_filtered_on_requires_shipping_false(self):
        from catalog.models import Product

        digital = ProductFactory(product_type="digital")
        ProductFactory(product_type="simple")

        result = Product.objects.filter(requires_shipping=False)

        assert digital in result
        assert result.filter(product_type="simple").count() == 0

    def test_cart_item_can_traverse_the_relation(self, site_settings):
        """
        ``cart/models.py:326`` does exactly this. It is the query that was
        raising ``FieldError`` on the live shippable-cart path.
        """
        from cart.models import CartItem

        cart = CartFactory()
        shippable = ProductFactory(product_type="simple")
        digital = ProductFactory(product_type="digital")
        CartItemFactory(cart=cart, product=shippable)
        CartItemFactory(cart=cart, product=digital)

        result = CartItem.objects.filter(product__requires_shipping=True)

        assert result.count() == 1
        assert result.first().product_id == shippable.id

    def test_cart_requires_shipping_property_works(self, site_settings):
        """The model property that aggregates over items."""
        cart = CartFactory()
        CartItemFactory(cart=cart, product=ProductFactory(product_type="digital"))

        assert cart.requires_shipping is False

        CartItemFactory(cart=cart, product=ProductFactory(product_type="simple"))
        assert cart.requires_shipping is True

    def test_cart_item_requires_shipping_delegates_to_the_product(self, site_settings):
        cart = CartFactory()
        item = CartItemFactory(cart=cart, product=ProductFactory(product_type="digital"))

        assert item.requires_shipping is False

    def test_exclude_and_ordering_also_work(self):
        """Anything the ORM can do with a column, not just equality."""
        from catalog.models import Product

        ProductFactory(product_type="simple")
        ProductFactory(product_type="booking")

        assert Product.objects.exclude(requires_shipping=True).count() >= 1
        assert list(Product.objects.order_by("requires_shipping"))  # no FieldError


# ============================================================
# save() semantics
# ============================================================


class TestSaveForcesNonShippableTypes:
    @pytest.mark.parametrize("product_type", NON_SHIPPABLE_TYPES)
    def test_non_shippable_types_save_as_false(self, product_type):
        product = ProductFactory(product_type=product_type)

        product.refresh_from_db()
        assert product.requires_shipping is False

    @pytest.mark.parametrize("product_type", NON_SHIPPABLE_TYPES)
    def test_non_shippable_types_are_forced_even_if_set_true(self, product_type):
        """A digital product can never ship, whatever the merchant ticks."""
        product = ProductFactory(product_type=product_type)
        product.requires_shipping = True
        product.save()

        product.refresh_from_db()
        assert product.requires_shipping is False

    @pytest.mark.parametrize(
        "product_type",
        ["simple", "variable", "bundle", "customizable", "configurable"],
    )
    def test_other_types_default_to_true(self, product_type):
        product = ProductFactory(product_type=product_type)

        product.refresh_from_db()
        assert product.requires_shipping is True

    def test_gift_cards_are_not_shipped(self):
        """
        Changed in P2.3, when gift card sales went live.

        A DIGITAL gift card is delivered by email. Leaving requires_shipping
        True made checkout demand a postal address and quote postage for an
        emailed code, which blocked the sale outright the moment the sales gate
        came off. R3 revisits this for PHYSICAL cards, which are shipped and
        stocked like any other good.
        """
        product = ProductFactory(product_type="gift_card")

        product.refresh_from_db()
        assert product.requires_shipping is False
        assert product.is_digital is True


class TestMerchantControlIsPreserved:
    """
    The point of making this a column rather than keeping the property: the
    merchant can express a non-shipping simple product (a service, a workshop
    seat), which is also what makes a physical gift card expressible in R3.
    """

    def test_a_merchant_can_turn_shipping_off_for_a_simple_product(self):
        product = ProductFactory(product_type="simple")
        product.requires_shipping = False
        product.save()

        product.refresh_from_db()
        assert product.requires_shipping is False, (
            "save() overwrote a merchant's choice on a shippable type."
        )

    def test_the_choice_survives_a_later_unrelated_save(self):
        product = ProductFactory(product_type="simple")
        product.requires_shipping = False
        product.save()

        product.name = "Renamed"
        product.save()

        product.refresh_from_db()
        assert product.requires_shipping is False
        assert product.name == "Renamed"

    def test_a_non_shipping_simple_product_is_excluded_from_shippable_queries(self):
        from catalog.models import Product

        product = ProductFactory(product_type="simple")
        product.requires_shipping = False
        product.save()

        assert product not in Product.objects.filter(requires_shipping=True)

    def test_changing_type_to_digital_forces_it_off(self):
        product = ProductFactory(product_type="simple")
        assert product.requires_shipping is True

        product.product_type = "digital"
        product.save()

        product.refresh_from_db()
        assert product.requires_shipping is False


# ============================================================
# Migration backfill
# ============================================================


class TestMigrationBackfill:
    """
    The backfill must replay the old property exactly. Anything else silently
    changes fulfilment for products that already exist.
    """

    def test_backfill_function_matches_old_property(self):
        """
        Import the migration's ``backfill_requires_shipping`` and run it over
        deliberately-wrong data, then compare against the old property.

        ``.update()`` is used to seed the wrong values because ``save()`` would
        re-apply the forcing rule and hide the bug this asserts against.
        """
        import importlib

        from django.apps import apps as global_apps

        from catalog.models import Product

        migration = importlib.import_module("catalog.migrations.0005_add_product_requires_shipping")

        types = [
            "simple",
            "variable",
            "digital",
            "bundle",
            "gift_card",
            "customizable",
            "configurable",
            "booking",
        ]
        created = {t: ProductFactory(product_type=t) for t in types}

        # Scramble: set every row to the opposite of what it should be.
        for product_type, product in created.items():
            Product.objects.filter(pk=product.pk).update(
                requires_shipping=not _old_property_semantics(product_type)
            )

        migration.backfill_requires_shipping(global_apps, None)

        for product_type, product in created.items():
            product.refresh_from_db()
            assert product.requires_shipping == _old_property_semantics(product_type), (
                f"Backfill produced {product.requires_shipping} for "
                f"product_type={product_type!r}; the old property returned "
                f"{_old_property_semantics(product_type)}."
            )

    def test_backfill_constant_lists_exactly_digital_and_booking(self):
        import importlib

        migration = importlib.import_module("catalog.migrations.0005_add_product_requires_shipping")

        assert set(migration.NON_SHIPPABLE_TYPES) == {"digital", "booking"}

    def test_every_product_type_agrees_with_the_old_property_after_save(self):
        """
        End-to-end: normal creation lands on the old semantics.

        ``gift_card`` is the one deliberate exception, added in P2.3 when gift
        card sales went live: a digital card is emailed, so demanding a postal
        address and postage for it blocked the sale outright. The MIGRATION
        backfill is unchanged and still replays the old property exactly —
        that parity is asserted separately above; this divergence happens at
        ``save()`` time on new writes only.
        """
        diverged_in_p23 = {"gift_card": False}

        for product_type in [
            "simple",
            "variable",
            "digital",
            "bundle",
            "gift_card",
            "customizable",
            "configurable",
            "booking",
        ]:
            product = ProductFactory(product_type=product_type)
            product.refresh_from_db()
            expected = diverged_in_p23.get(product_type, _old_property_semantics(product_type))
            assert product.requires_shipping == expected, (
                f"product_type={product_type!r} changed fulfilment behaviour."
            )
