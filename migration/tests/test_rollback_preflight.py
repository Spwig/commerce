"""
Unit tests for the rollback closure itself (migration/utils/rollback_preflight.py).

test_rollback.py exercises the whole rollback against realistic store data.
This file pins the three mechanics that whole-rollback tests only cover
indirectly:

* cascade_closure expands CASCADE children (and does so transitively);
* build_retention_plan iterates to a fixpoint rather than stopping after one
  pass, so retention propagates up the graph;
* carry_retained preserves an earlier pass's retention entries. That last one
  was a real bug: rollback_migration re-plans after folding in dependent seeds,
  and without carrying the earlier decisions the report told the merchant
  nothing had been retained when things had.
"""

import uuid
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from djmoney.money import Money

from catalog.models import Category, Product, ProductImage
from core.models import SiteSettings
from media_library.models import MediaAsset
from migration.utils.rollback_preflight import (
    RetentionPlan,
    build_retention_plan,
    cascade_closure,
    find_blocked,
    protect_edges_into,
)
from orders.models import Order, OrderItem

User = get_user_model()


class PreflightTestBase(TestCase):
    def setUp(self):
        SiteSettings.objects.update_or_create(
            pk=1,
            defaults={
                "site_name": "Rollback Test Store",
                "admin_email": "merchant@example.com",
            },
        )

    def make_category(self, name="Cat", **kwargs):
        return Category.objects.create(name=name, slug=f"cat-{uuid.uuid4().hex[:8]}", **kwargs)

    def make_product(self, category, name="Widget", **kwargs):
        suffix = uuid.uuid4().hex[:8]
        kwargs.setdefault("price", Money(Decimal("10.00"), "USD"))
        return Product.objects.create(
            name=name, slug=f"p-{suffix}", sku=f"SKU-{suffix}", category=category, **kwargs
        )

    def make_media(self, title="Asset"):
        return MediaAsset.objects.create(
            title=title,
            original_file=f"media/{uuid.uuid4().hex[:8]}.jpg",
            file_size=100,
            mime_type="image/jpeg",
        )

    def make_order(self, user=None):
        return Order.objects.create(
            order_number=f"ORD-{uuid.uuid4().hex[:10].upper()}",
            user=user,
            email="buyer@example.com",
            shipping_name="Buyer",
            shipping_address1="1 Street",
            shipping_city="Town",
            shipping_state="TS",
            shipping_postal_code="12345",
            shipping_country="US",
            subtotal=Money(Decimal("10.00"), "USD"),
            total_amount=Money(Decimal("10.00"), "USD"),
        )

    def make_order_item(self, order, product):
        return OrderItem.objects.create(
            order=order,
            product=product,
            product_name=product.name,
            sku=product.sku,
            quantity=1,
            unit_price=Money(Decimal("10.00"), "USD"),
            total_price=Money(Decimal("10.00"), "USD"),
        )


class CascadeClosureTest(PreflightTestBase):
    def test_expands_cascade_children(self):
        category = self.make_category()
        product = self.make_product(category)
        asset = self.make_media()
        image = ProductImage.objects.create(product=product, media_asset=asset)

        closure = cascade_closure({Product: {product.pk}})

        self.assertEqual(closure[Product], {product.pk})
        self.assertIn(ProductImage, closure)
        self.assertIn(
            image.pk,
            closure[ProductImage],
            "ProductImage cascades from Product and must appear in the closure",
        )

    def test_does_not_expand_across_protect_edges(self):
        """OrderItem PROTECTs Product, so a Product seed must not drag it in."""
        category = self.make_category()
        product = self.make_product(category)
        order = self.make_order()
        item = self.make_order_item(order, product)

        closure = cascade_closure({Product: {product.pk}})

        self.assertNotIn(
            item.pk,
            closure.get(OrderItem, set()),
            "OrderItem.product is PROTECT, not CASCADE — it is not a cascade child",
        )

    def test_expands_transitively(self):
        """Order -> OrderItem is one hop; the walk must not stop at depth one."""
        category = self.make_category()
        product = self.make_product(category)
        order = self.make_order()
        item = self.make_order_item(order, product)

        closure = cascade_closure({Order: {order.pk}})

        self.assertIn(item.pk, closure[OrderItem])

    def test_ignores_empty_seed_sets(self):
        closure = cascade_closure({Product: set(), Category: set()})
        self.assertEqual(closure, {})

    def test_leaves_unrelated_rows_alone(self):
        category = self.make_category()
        kept = self.make_product(category, name="Kept")
        seeded = self.make_product(category, name="Seeded")

        closure = cascade_closure({Product: {seeded.pk}})

        self.assertEqual(closure[Product], {seeded.pk})
        self.assertNotIn(kept.pk, closure[Product])


class ProtectEdgeDiscoveryTest(PreflightTestBase):
    def test_finds_protect_referrers_from_the_fk_graph(self):
        edges = protect_edges_into([Product])
        pairs = {(referrer._meta.label, field) for _t, referrer, field in edges}

        # These are never hand-listed anywhere in the rollback code.
        self.assertIn(("orders.OrderItem", "product"), pairs)
        self.assertIn(("catalog.BundleItem", "component_product"), pairs)

    def test_find_blocked_names_the_protecting_model(self):
        category = self.make_category()
        product = self.make_product(category)
        order = self.make_order()
        self.make_order_item(order, product)

        # Plan to delete only the product — the order stays.
        blocked = find_blocked(cascade_closure({Product: {product.pk}}))

        self.assertIn(Product, blocked)
        self.assertEqual(blocked[Product][product.pk], "orders.OrderItem")

    def test_a_referrer_inside_the_delete_set_does_not_block(self):
        category = self.make_category()
        product = self.make_product(category)
        order = self.make_order()
        self.make_order_item(order, product)

        # Delete the order too, so its item goes with it.
        blocked = find_blocked(cascade_closure({Product: {product.pk}, Order: {order.pk}}))

        self.assertNotIn(
            product.pk,
            blocked.get(Product, {}),
            "an OrderItem that is itself being deleted must not protect the product",
        )


class BuildRetentionPlanTest(PreflightTestBase):
    def test_deletes_everything_when_nothing_depends_on_it(self):
        category = self.make_category()
        product = self.make_product(category)

        plan = build_retention_plan({Product: {product.pk}, Category: {category.pk}})

        self.assertEqual(plan.pks(Product), {product.pk})
        self.assertEqual(plan.pks(Category), {category.pk})
        self.assertFalse(plan.has_retentions)
        self.assertEqual(plan.retained_counts(), {})

    def test_withdraws_a_blocked_row_and_reports_the_reason(self):
        category = self.make_category()
        product = self.make_product(category)
        order = self.make_order()
        self.make_order_item(order, product)

        plan = build_retention_plan({Product: {product.pk}, Category: {category.pk}})

        self.assertEqual(plan.pks(Product), set())
        self.assertEqual(plan.retained_counts()["catalog.Product"], (1, ["orders.OrderItem"]))

    def test_reaches_a_fixpoint_so_retention_propagates(self):
        """Product retained -> its Category retained -> its media retained.

        A single-pass implementation withdraws the Product and stops, then the
        Category delete hits PROTECT at runtime. Only iteration to a fixpoint
        gets this right, and the chain here is three levels deep.
        """
        category = self.make_category()
        product = self.make_product(category)
        asset = self.make_media()
        ProductImage.objects.create(product=product, media_asset=asset)

        order = self.make_order()
        self.make_order_item(order, product)

        plan = build_retention_plan(
            {
                Product: {product.pk},
                Category: {category.pk},
                MediaAsset: {asset.pk},
            }
        )

        self.assertEqual(plan.pks(Product), set())
        self.assertEqual(
            plan.pks(Category), set(), "the retained product's category must be withdrawn too"
        )
        self.assertEqual(
            plan.pks(MediaAsset),
            set(),
            "media the retained product's images point at must be withdrawn too",
        )

        counts = plan.retained_counts()
        self.assertEqual(counts["catalog.Product"], (1, ["orders.OrderItem"]))
        self.assertEqual(counts["catalog.Category"], (1, ["catalog.Product"]))
        self.assertEqual(counts["media_library.MediaAsset"], (1, ["catalog.ProductImage"]))

    def test_only_the_blocked_row_is_withdrawn(self):
        category = self.make_category()
        blocked_product = self.make_product(category, name="Blocked")
        free_product = self.make_product(category, name="Free")
        order = self.make_order()
        self.make_order_item(order, blocked_product)

        plan = build_retention_plan({Product: {blocked_product.pk, free_product.pk}})

        self.assertEqual(plan.pks(Product), {free_product.pk})
        self.assertEqual(plan.retained_counts()["catalog.Product"][0], 1)

    def test_raises_rather_than_deleting_against_an_unstable_plan(self):
        category = self.make_category()
        product = self.make_product(category)
        order = self.make_order()
        self.make_order_item(order, product)

        with self.assertRaises(RuntimeError) as ctx:
            build_retention_plan({Product: {product.pk}, Category: {category.pk}}, max_passes=1)

        self.assertIn("did not converge", str(ctx.exception))


class CarryRetainedTest(PreflightTestBase):
    """The report-loses-retentions bug.

    rollback_migration plans once, folds in the rows that follow from that
    decision (loyalty, shipments), then re-plans. The second call starts from
    the first call's *reduced* delete set, so rows already withdrawn are simply
    absent — nothing blocks them any more, and they drop out of the report. The
    merchant is then told nothing was retained while rows were sitting there
    retained.
    """

    def setUp(self):
        super().setUp()
        self.category = self.make_category()
        self.product = self.make_product(self.category)
        self.order = self.make_order()
        self.make_order_item(self.order, self.product)

        self.first_pass = build_retention_plan(
            {Product: {self.product.pk}, Category: {self.category.pk}}
        )

    def test_a_second_plan_without_carry_retained_forgets_the_first(self):
        second = build_retention_plan(dict(self.first_pass.deletable))

        self.assertEqual(
            second.retained_counts(),
            {},
            "this is the failure mode carry_retained exists to prevent",
        )

    def test_carry_retained_preserves_the_earlier_decision(self):
        second = build_retention_plan(
            dict(self.first_pass.deletable), carry_retained=self.first_pass.retained
        )

        counts = second.retained_counts()
        self.assertEqual(counts["catalog.Product"], (1, ["orders.OrderItem"]))
        self.assertEqual(counts["catalog.Category"], (1, ["catalog.Product"]))

    def test_carry_retained_merges_rather_than_replaces(self):
        """New retentions found in the second pass must be added, not lost."""
        other_product = self.make_product(self.category, name="Second")
        other_order = self.make_order()
        self.make_order_item(other_order, other_product)

        second = build_retention_plan(
            {Product: {other_product.pk}}, carry_retained=self.first_pass.retained
        )

        count, reasons = second.retained_counts()["catalog.Product"]
        self.assertEqual(count, 2, "both the carried and the newly found row must be reported")
        self.assertEqual(reasons, ["orders.OrderItem"])

    def test_carry_retained_does_not_mutate_the_source_mapping(self):
        before = {model: dict(entries) for model, entries in self.first_pass.retained.items()}

        other_product = self.make_product(self.category, name="Second")
        other_order = self.make_order()
        self.make_order_item(other_order, other_product)
        build_retention_plan({Product: {other_product.pk}}, carry_retained=self.first_pass.retained)

        after = {model: dict(entries) for model, entries in self.first_pass.retained.items()}
        self.assertEqual(before, after, "carry_retained must not write back into its argument")


class RetentionPlanApiTest(TestCase):
    def test_pks_returns_an_empty_set_for_an_unknown_model(self):
        plan = RetentionPlan({}, {})
        self.assertEqual(plan.pks(Product), set())

    def test_empty_retention_entries_are_not_reported(self):
        plan = RetentionPlan({}, {Product: {}})
        self.assertEqual(plan.retained_counts(), {})
        self.assertFalse(plan.has_retentions)

    def test_reasons_are_deduplicated_and_sorted(self):
        plan = RetentionPlan(
            {}, {Product: {1: "orders.OrderItem", 2: "catalog.BundleItem", 3: "orders.OrderItem"}}
        )
        self.assertEqual(
            plan.retained_counts()["catalog.Product"],
            (3, ["catalog.BundleItem", "orders.OrderItem"]),
        )
        self.assertTrue(plan.has_retentions)
