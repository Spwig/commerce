"""
Regression suite for migration rollback (migration/utils/rollback.py).

This is a merge gate. The code under test deletes customer and order data, and
the previous implementation deleted rows it had no business touching:

* every order belonging to a migrated customer, including genuine orders placed
  after go-live;
* OrderItems referencing a migrated product even on orders belonging to
  customers the migration never touched, leaving those orders with missing line
  items and a total that no longer matched its lines;
* loyalty transactions unscoped, destroying points earned on real orders;
* nothing at all for affiliates / commissions / payouts / blog tags, which were
  simply left behind.

The rewritten implementation is preserve-and-report: a row may be deleted only
if every PROTECT reference to it comes from a row that is also being deleted.
Retention is transitive, derived from the FK graph rather than a hand-written
list, and reported back to the merchant.

Every test below pins one of those behaviours. Weakening an assertion here to
make the suite green re-opens a data-loss bug.
"""

import uuid
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from djmoney.money import Money

from accounts.models import CustomerProfile
from affiliate.models import Affiliate, Commission, Payout, Program
from blog.models import BlogCategory, BlogPost, BlogTag
from catalog.models import (
    BundleItem,
    Category,
    Product,
    ProductImage,
    ProductReview,
    SalesRegion,
    Warehouse,
)
from core.models import SiteSettings
from loyalty.models import LoyaltyMember, LoyaltyTransaction
from media_library.models import MediaAsset
from migration.models import MigrationJob
from migration.utils.rollback import RollbackRefused, plan_rollback, rollback_migration
from orders.models import Address, Order, OrderItem
from pos_app.models import CashMovement, POSShift, POSTerminal
from shipping.models import Shipment
from vouchers.models import VoucherCode
from wallet.models import CustomerWallet, WalletTransaction

User = get_user_model()


class RollbackTestBase(TestCase):
    """Fixtures shared by every rollback test.

    `self.job` is the migration being rolled back. `self.other_job` exists so
    that "belongs to a migration" is never confused with "belongs to *this*
    migration" — a rollback must not touch a different import's rows either.
    """

    def setUp(self):
        # CurrencyMiddleware and several signals call SiteSettings.get_settings(),
        # which full_clean()s the row. Without a non-blank admin_email every
        # request and some saves blow up on a validation error.
        SiteSettings.objects.update_or_create(
            pk=1,
            defaults={
                "site_name": "Rollback Test Store",
                "admin_email": "merchant@example.com",
            },
        )

        self.staff = User.objects.create_user(
            "merchant", "merchant@example.com", "pw", is_staff=True
        )
        self.job = MigrationJob.objects.create(
            created_by=self.staff, platform="woocommerce", method="api"
        )
        self.other_job = MigrationJob.objects.create(
            created_by=self.staff, platform="shopify", method="api"
        )

    # ---------------------------------------------------------------- helpers

    def make_category(self, name, job=None, **kwargs):
        return Category.objects.create(
            name=name,
            slug=f"{name.lower().replace(' ', '-')}-{uuid.uuid4().hex[:6]}",
            migration_job=job,
            **kwargs,
        )

    def make_product(self, name, category, job=None, **kwargs):
        suffix = uuid.uuid4().hex[:8]
        kwargs.setdefault("price", Money(Decimal("10.00"), "USD"))
        return Product.objects.create(
            name=name,
            slug=f"{name.lower().replace(' ', '-')}-{suffix}",
            sku=f"SKU-{suffix}",
            category=category,
            migration_job=job,
            **kwargs,
        )

    def make_media(self, title, job=None):
        return MediaAsset.objects.create(
            title=title,
            original_file=f"media/{uuid.uuid4().hex[:8]}.jpg",
            file_size=1234,
            mime_type="image/jpeg",
            migration_job=job,
        )

    def make_customer(self, username, job=None):
        """A shop customer. `job` set => imported by that migration."""
        user = User.objects.create_user(username, f"{username}@example.com", "pw")
        CustomerProfile.objects.create(user=user, migration_job=job)
        return user

    def make_order(self, user=None, job=None, **kwargs):
        kwargs.setdefault("subtotal", Money(Decimal("50.00"), "USD"))
        kwargs.setdefault("total_amount", Money(Decimal("50.00"), "USD"))
        return Order.objects.create(
            order_number=f"ORD-{uuid.uuid4().hex[:10].upper()}",
            user=user,
            email=(user.email if user else "guest@example.com"),
            shipping_name="Test Person",
            shipping_address1="1 Test Street",
            shipping_city="Testville",
            shipping_state="TS",
            shipping_postal_code="12345",
            shipping_country="US",
            migration_job=job,
            **kwargs,
        )

    def make_order_item(self, order, product, quantity=1, unit_price=Decimal("25.00")):
        return OrderItem.objects.create(
            order=order,
            product=product,
            product_name=product.name,
            sku=product.sku,
            quantity=quantity,
            unit_price=Money(unit_price, "USD"),
            total_price=Money(unit_price * quantity, "USD"),
        )

    def make_shipment(self, order, user):
        return Shipment.objects.create(
            order=order, user=user, origin_country="US", dest_country="US"
        )

    def loyalty_member(self, user):
        """The loyalty member auto-created by the signup signal."""
        return LoyaltyMember.objects.get(customer=user)

    def make_loyalty_txn(self, user, points=100, description="Points earned"):
        return LoyaltyTransaction.objects.create(
            member=self.loyalty_member(user),
            transaction_type=LoyaltyTransaction.TYPE_EARN,
            points=points,
            description=description,
        )

    def make_pos_terminal(self):
        region = SalesRegion.objects.create(
            name=f"Region {uuid.uuid4().hex[:4]}",
            code=uuid.uuid4().hex[:6].upper(),
            default_currency="USD",
        )
        warehouse = Warehouse.objects.create(
            name="Shop Floor",
            code=f"WH-{uuid.uuid4().hex[:6].upper()}",
            region=region,
            address_line1="1 Retail Way",
            city="Testville",
            postal_code="12345",
            country="US",
            is_retail_location=True,
        )
        return POSTerminal.objects.create(name="Front Register", warehouse=warehouse)

    # ------------------------------------------------------------- assertions

    def assertRetains(self, report, model_label):
        self.assertIn(
            model_label,
            report["retained"],
            f"{model_label} should appear in the retained report; got {report['retained']!r}",
        )

    def assertRetainedBecauseOf(self, report, model_label, protecting_label):
        self.assertRetains(report, model_label)
        count, reasons = report["retained"][model_label]
        self.assertGreaterEqual(count, 1)
        self.assertIn(
            protecting_label,
            reasons,
            f"{model_label} should be reported as retained because of "
            f"{protecting_label}; reasons were {reasons!r}",
        )


class GenuineOrderAfterImportTest(RollbackTestBase):
    """The headline regression.

    A migrated customer places a real order after go-live. The old rollback
    deleted every order belonging to a migrated customer, so that order — real
    revenue, already fulfilled — vanished along with its shipment, and the
    customer's loyalty points with it.
    """

    def setUp(self):
        super().setUp()
        self.category = self.make_category("Imported Cat", job=self.job)
        self.imported_product = self.make_product("Imported Widget", self.category, job=self.job)

        self.customer = self.make_customer("imported_customer", job=self.job)
        self.address = Address.objects.create(
            user=self.customer,
            name="Test Person",
            address1="1 Test Street",
            city="Testville",
            state="TS",
            postal_code="12345",
            country="US",
        )

        # What the migration brought over.
        self.historic_order = self.make_order(user=self.customer, job=self.job)
        self.make_order_item(self.historic_order, self.imported_product)

        # What happened afterwards, in the merchant's live store.
        self.genuine_order = self.make_order(user=self.customer, job=None)
        self.genuine_item = self.make_order_item(self.genuine_order, self.imported_product)
        self.genuine_shipment = self.make_shipment(self.genuine_order, self.customer)
        self.genuine_points = self.make_loyalty_txn(
            self.customer, points=250, description="Points from post-go-live order"
        )

    def test_genuine_order_and_everything_it_depends_on_survives(self):
        report = rollback_migration(self.job)

        # The order itself, its line item, its shipment.
        self.assertTrue(
            Order.objects.filter(pk=self.genuine_order.pk).exists(),
            "a genuine post-go-live order must never be deleted by a rollback",
        )
        self.assertTrue(OrderItem.objects.filter(pk=self.genuine_item.pk).exists())
        self.assertTrue(Shipment.objects.filter(pk=self.genuine_shipment.pk).exists())

        # The customer account and everything hanging off it.
        self.assertTrue(User.objects.filter(pk=self.customer.pk).exists())
        self.assertTrue(CustomerProfile.objects.filter(user=self.customer).exists())
        self.assertTrue(Address.objects.filter(pk=self.address.pk).exists())

        # Points earned on the real order.
        self.assertTrue(
            LoyaltyTransaction.objects.filter(pk=self.genuine_points.pk).exists(),
            "loyalty points earned on a real order must survive a rollback",
        )
        self.assertTrue(LoyaltyMember.objects.filter(customer=self.customer).exists())

        # The imported order is gone, and so is its line item.
        self.assertFalse(Order.objects.filter(pk=self.historic_order.pk).exists())
        self.assertFalse(OrderItem.objects.filter(order_id=self.historic_order.pk).exists())

        # And the merchant is told the user was kept.
        self.assertRetainedBecauseOf(report, "auth.User", "orders.Order")

    def test_retained_product_keeps_the_genuine_orders_total_intact(self):
        """The genuine order's total must still match the sum of its lines."""
        rollback_migration(self.job)

        self.genuine_order.refresh_from_db()
        line_total = sum(
            (item.total_price for item in self.genuine_order.items.all()),
            Money(Decimal("0.00"), "USD"),
        )
        self.assertEqual(self.genuine_order.items.count(), 1)
        self.assertEqual(line_total, Money(Decimal("25.00"), "USD"))

    def test_product_referenced_by_the_genuine_order_is_retained(self):
        report = rollback_migration(self.job)

        self.assertTrue(
            Product.all_objects.filter(pk=self.imported_product.pk).exists(),
            "a product a live order references must be retained",
        )
        self.assertRetainedBecauseOf(report, "catalog.Product", "orders.OrderItem")


class NonMigratedCustomerOrderTest(RollbackTestBase):
    """An order the migration never touched, containing an imported product.

    The old rollback deleted OrderItems by product provenance, so this order
    silently lost line items and its total stopped matching its lines.
    """

    def setUp(self):
        super().setUp()
        self.imported_category = self.make_category("Imported Cat", job=self.job)
        self.asset = self.make_media("Imported Product Shot", job=self.job)
        self.imported_product = self.make_product(
            "Imported Widget", self.imported_category, job=self.job
        )
        ProductImage.objects.create(product=self.imported_product, media_asset=self.asset)

        self.own_category = self.make_category("Merchant Cat")
        self.own_product = self.make_product("Merchant Widget", self.own_category)

        self.customer = self.make_customer("real_customer")  # never migrated
        self.order = self.make_order(
            user=self.customer,
            subtotal=Money(Decimal("75.00"), "USD"),
            total_amount=Money(Decimal("75.00"), "USD"),
        )
        self.item_imported = self.make_order_item(
            self.order, self.imported_product, unit_price=Decimal("25.00")
        )
        self.item_own = self.make_order_item(
            self.order, self.own_product, quantity=2, unit_price=Decimal("25.00")
        )

    def test_order_keeps_every_line_item_and_its_total(self):
        rollback_migration(self.job)

        self.order.refresh_from_db()
        self.assertEqual(
            self.order.items.count(),
            2,
            "an order the migration never created must keep all of its line items",
        )
        self.assertTrue(OrderItem.objects.filter(pk=self.item_imported.pk).exists())
        self.assertTrue(OrderItem.objects.filter(pk=self.item_own.pk).exists())

        line_total = sum(
            (item.total_price for item in self.order.items.all()),
            Money(Decimal("0.00"), "USD"),
        )
        self.assertEqual(self.order.total_amount, Money(Decimal("75.00"), "USD"))
        self.assertEqual(line_total, self.order.total_amount)

    def test_transitive_closure_keeps_category_and_media_of_a_retained_product(self):
        report = rollback_migration(self.job)

        self.assertTrue(Product.all_objects.filter(pk=self.imported_product.pk).exists())
        self.assertTrue(
            Category.objects.filter(pk=self.imported_category.pk).exists(),
            "a retained product's category is retained too (Product.category is PROTECT)",
        )
        self.assertTrue(
            MediaAsset.objects.filter(pk=self.asset.pk).exists(),
            "media the retained product's images point at is retained too",
        )
        self.assertTrue(
            ProductImage.objects.filter(product=self.imported_product).exists(),
            "the retained product's images are not orphaned",
        )

        self.assertRetainedBecauseOf(report, "catalog.Product", "orders.OrderItem")
        self.assertRetainedBecauseOf(report, "catalog.Category", "catalog.Product")
        self.assertRetainedBecauseOf(report, "media_library.MediaAsset", "catalog.ProductImage")


class BundleItemTest(RollbackTestBase):
    """catalog.BundleItem.component_product is PROTECT.

    This edge is not in any hand-written list; it has to fall out of the FK
    graph. If someone replaces the graph walk with an enumeration, this test is
    what catches it.
    """

    def setUp(self):
        super().setUp()
        self.imported_category = self.make_category("Imported Cat", job=self.job)
        self.component = self.make_product(
            "Imported Component", self.imported_category, job=self.job
        )

        self.own_category = self.make_category("Merchant Cat")
        self.bundle = self.make_product("Merchant Bundle", self.own_category, product_type="bundle")
        BundleItem.objects.create(bundle=self.bundle, component_product=self.component)

    def test_component_of_a_merchant_bundle_is_retained(self):
        report = rollback_migration(self.job)

        self.assertTrue(
            Product.all_objects.filter(pk=self.component.pk).exists(),
            "a product used in a merchant's bundle must be retained",
        )
        self.assertTrue(BundleItem.objects.filter(bundle=self.bundle).exists())
        self.assertRetainedBecauseOf(report, "catalog.Product", "catalog.BundleItem")
        self.assertRetainedBecauseOf(report, "catalog.Category", "catalog.Product")


class MerchantProductInImportedCategoryTest(RollbackTestBase):
    """catalog.Product.category is PROTECT."""

    def setUp(self):
        super().setUp()
        self.imported_category = self.make_category("Imported Cat", job=self.job)
        self.imported_product = self.make_product(
            "Imported Widget", self.imported_category, job=self.job
        )
        self.own_product = self.make_product("Merchant Widget", self.imported_category)

    def test_category_holding_a_merchant_product_is_retained(self):
        report = rollback_migration(self.job)

        self.assertTrue(
            Category.objects.filter(pk=self.imported_category.pk).exists(),
            "a category the merchant filed their own product under must be retained",
        )
        self.assertTrue(Product.all_objects.filter(pk=self.own_product.pk).exists())
        # The imported product itself has nothing depending on it, so it goes.
        self.assertFalse(Product.all_objects.filter(pk=self.imported_product.pk).exists())
        self.assertRetainedBecauseOf(report, "catalog.Category", "catalog.Product")


class MerchantUsesImportedMediaTest(RollbackTestBase):
    """MediaAsset has six PROTECT referrers. The old code crashed here.

    Deleting an imported MediaAsset that the merchant had attached to their own
    product or category raised ProtectedError, which aborted the whole rollback
    part-way through with rows already gone.
    """

    def setUp(self):
        super().setUp()
        self.imported_category = self.make_category("Imported Cat", job=self.job)
        self.product_asset = self.make_media("Imported Shot A", job=self.job)
        self.category_asset = self.make_media("Imported Shot B", job=self.job)
        self.unused_asset = self.make_media("Imported Shot C", job=self.job)

        self.own_category = self.make_category("Merchant Cat", image_asset=self.category_asset)
        self.own_product = self.make_product("Merchant Widget", self.own_category)
        ProductImage.objects.create(product=self.own_product, media_asset=self.product_asset)

    def test_rollback_succeeds_and_retains_assets_the_merchant_uses(self):
        report = rollback_migration(self.job)  # must not raise

        self.assertTrue(
            MediaAsset.objects.filter(pk=self.product_asset.pk).exists(),
            "an asset attached to the merchant's own product must be retained",
        )
        self.assertTrue(
            MediaAsset.objects.filter(pk=self.category_asset.pk).exists(),
            "an asset attached to the merchant's own category must be retained",
        )
        self.assertFalse(
            MediaAsset.objects.filter(pk=self.unused_asset.pk).exists(),
            "an imported asset nothing depends on is still deleted",
        )

        self.assertRetains(report, "media_library.MediaAsset")
        count, reasons = report["retained"]["media_library.MediaAsset"]
        self.assertEqual(count, 2)
        self.assertEqual(sorted(reasons), ["catalog.Category", "catalog.ProductImage"])

    def test_merchants_own_product_and_category_are_untouched(self):
        rollback_migration(self.job)

        self.assertTrue(Product.all_objects.filter(pk=self.own_product.pk).exists())
        self.assertTrue(Category.objects.filter(pk=self.own_category.pk).exists())
        self.assertTrue(ProductImage.objects.filter(product=self.own_product).exists())


class MigratedCustomerIsCashierTest(RollbackTestBase):
    """pos_app.POSShift.cashier and CashMovement.performed_by are PROTECT -> User."""

    def setUp(self):
        super().setUp()
        self.cashier = self.make_customer("imported_cashier", job=self.job)
        terminal = self.make_pos_terminal()
        self.shift = POSShift.objects.create(terminal=terminal, cashier=self.cashier)
        self.movement = CashMovement.objects.create(
            shift=self.shift,
            movement_type="in",
            amount=Decimal("50.00"),
            reason="Change float top-up",
            performed_by=self.cashier,
        )

    def test_cashier_account_is_retained_and_rollback_still_succeeds(self):
        report = rollback_migration(self.job)  # must not raise

        self.assertTrue(
            User.objects.filter(pk=self.cashier.pk).exists(),
            "a migrated user who works the till must be retained",
        )
        self.assertTrue(POSShift.objects.filter(pk=self.shift.pk).exists())
        self.assertTrue(CashMovement.objects.filter(pk=self.movement.pk).exists())
        self.assertTrue(CustomerProfile.objects.filter(user=self.cashier).exists())

        self.assertRetains(report, "auth.User")
        _count, reasons = report["retained"]["auth.User"]
        self.assertIn("pos_app.POSShift", reasons)

        self.job.refresh_from_db()
        self.assertEqual(self.job.status, "rolled_back")


class CleanRollbackTest(RollbackTestBase):
    """An import nothing depends on: everything the job created goes."""

    def setUp(self):
        super().setUp()
        self.category = self.make_category("Imported Cat", job=self.job)
        self.asset = self.make_media("Imported Shot", job=self.job)
        self.product = self.make_product("Imported Widget", self.category, job=self.job)
        ProductImage.objects.create(product=self.product, media_asset=self.asset)

        self.customer = self.make_customer("imported_customer", job=self.job)
        self.address = Address.objects.create(
            user=self.customer,
            name="Test Person",
            address1="1 Test Street",
            city="Testville",
            state="TS",
            postal_code="12345",
            country="US",
        )
        self.order = self.make_order(user=self.customer, job=self.job)
        self.item = self.make_order_item(self.order, self.product)
        self.shipment = self.make_shipment(self.order, self.customer)
        self.points = self.make_loyalty_txn(self.customer, points=10)

        self.review = ProductReview.objects.create(
            product=self.product,
            user=self.customer,
            rating=5,
            title="Great",
            comment="Imported review",
            migration_job=self.job,
        )
        self.voucher = VoucherCode.objects.create(
            code=f"IMP{uuid.uuid4().hex[:8].upper()}",
            name="Imported coupon",
            discount_value=Decimal("10.00"),
            migration_job=self.job,
        )

        self.blog_category = BlogCategory.objects.create(
            name="Imported Blog Cat", slug=f"bc-{uuid.uuid4().hex[:6]}", migration_job=self.job
        )
        self.blog_tag = BlogTag.objects.create(
            name="Imported Tag", slug=f"bt-{uuid.uuid4().hex[:6]}", migration_job=self.job
        )
        self.blog_post = BlogPost.objects.create(
            title="Imported Post", slug=f"bp-{uuid.uuid4().hex[:6]}", migration_job=self.job
        )
        self.blog_post.tags.add(self.blog_tag)

        # Affiliate side, recorded in the importer's rollback manifest.
        self.affiliate_user = User.objects.create_user(
            "imported_affiliate", "aff@example.com", "pw"
        )
        self.program = Program.objects.create(
            name="Imported Program",
            slug=f"prog-{uuid.uuid4().hex[:6]}",
            merchant=self.staff,
            commission_value=Decimal("10.00"),
        )
        self.affiliate = Affiliate.objects.create(
            user=self.affiliate_user,
            affiliate_code=f"AFF{uuid.uuid4().hex[:6].upper()}",
            payment_email="aff@example.com",
        )
        self.commission = Commission.objects.create(
            affiliate=self.affiliate,
            program=self.program,
            order=self.order,
            amount=Decimal("5.00"),
        )
        self.payout = Payout.objects.create(
            affiliate=self.affiliate, amount=Decimal("5.00"), method="paypal"
        )
        self.payout.commissions.add(self.commission)

        self.job.connection_config = {
            "affiliate_rollback_ids": {
                "affiliate_ids": [self.affiliate.pk],
                "program_ids": [self.program.pk],
                "user_ids": [self.affiliate_user.pk],
            }
        }
        self.job.save(update_fields=["connection_config"])

    def test_everything_is_deleted_and_nothing_is_retained(self):
        report = rollback_migration(self.job)

        self.assertEqual(
            report["retained"],
            {},
            "a clean import must report nothing retained",
        )

        self.assertFalse(Category.objects.filter(pk=self.category.pk).exists())
        self.assertFalse(Product.all_objects.filter(pk=self.product.pk).exists())
        self.assertFalse(MediaAsset.objects.filter(pk=self.asset.pk).exists())
        self.assertFalse(ProductReview.objects.filter(pk=self.review.pk).exists())
        self.assertFalse(VoucherCode.objects.filter(pk=self.voucher.pk).exists())
        self.assertFalse(Order.objects.filter(pk=self.order.pk).exists())
        self.assertFalse(OrderItem.objects.filter(pk=self.item.pk).exists())
        self.assertFalse(Shipment.objects.filter(pk=self.shipment.pk).exists())
        self.assertFalse(LoyaltyTransaction.objects.filter(pk=self.points.pk).exists())
        self.assertFalse(User.objects.filter(pk=self.customer.pk).exists())
        self.assertFalse(CustomerProfile.objects.filter(user_id=self.customer.pk).exists())
        self.assertFalse(Address.objects.filter(pk=self.address.pk).exists())
        self.assertFalse(LoyaltyMember.objects.filter(customer_id=self.customer.pk).exists())

        self.assertFalse(BlogPost.objects.filter(pk=self.blog_post.pk).exists())
        self.assertFalse(
            BlogTag.objects.filter(pk=self.blog_tag.pk).exists(),
            "blog tags were ignored entirely by the old rollback",
        )
        self.assertFalse(BlogCategory.objects.filter(pk=self.blog_category.pk).exists())

        self.assertFalse(Affiliate.objects.filter(pk=self.affiliate.pk).exists())
        self.assertFalse(Program.objects.filter(pk=self.program.pk).exists())
        self.assertFalse(Commission.objects.filter(pk=self.commission.pk).exists())
        self.assertFalse(Payout.objects.filter(pk=self.payout.pk).exists())

        self.job.refresh_from_db()
        self.assertEqual(self.job.status, "rolled_back")
        self.assertFalse(self.job.can_rollback)

    def test_report_counts_what_it_deleted(self):
        report = rollback_migration(self.job)
        deleted = report["deleted"]

        self.assertEqual(deleted["Products"], 1)
        self.assertEqual(deleted["Categories"], 1)
        self.assertEqual(deleted["Orders"], 1)
        self.assertEqual(deleted["Media assets"], 1)
        self.assertEqual(deleted["Blog Tags"], 1)
        self.assertEqual(deleted["Shipments"], 1)
        self.assertEqual(deleted["Loyalty Transactions"], 1)
        self.assertEqual(deleted["Affiliates"], 1)
        self.assertEqual(deleted["Voucher Codes"], 1)
        # The imported customer plus the affiliate account from the manifest.
        self.assertEqual(deleted["Users"], 2)

    def test_report_does_not_understate_the_cascade(self):
        """The consent screen must name what confirming actually destroys.

        Reporting only the models deleted explicitly hides the rows that go with
        them: a customer takes their profile, addresses and loyalty membership,
        an order takes its line items. Those have to be counted too.
        """
        deleted = rollback_migration(self.job)["deleted"]

        self.assertEqual(deleted["Order Items"], 1)
        self.assertEqual(deleted["Addresses"], 1)
        self.assertEqual(deleted["Customer profiles"], 1)
        self.assertEqual(deleted["Product images"], 1)
        self.assertEqual(deleted["Commissions"], 1)
        self.assertEqual(deleted["Payouts"], 1)

        counts = list(deleted.values())
        self.assertEqual(
            counts, sorted(counts, reverse=True), "the report is ordered largest first"
        )

    def test_products_are_hard_deleted_not_soft_deleted(self):
        """Product's default manager hides soft-deleted rows.

        A soft delete would leave the row in place, so Product.objects would
        look empty while the Category delete still hit PROTECT. Check the
        unfiltered manager.
        """
        rollback_migration(self.job)

        self.assertFalse(
            Product.all_objects.filter(pk=self.product.pk).exists(),
            "rollback must hard-delete products, not set is_deleted",
        )
        self.assertEqual(Product.all_objects.filter(migration_job=self.job).count(), 0)

    def test_affiliate_user_without_a_profile_is_removed(self):
        """Affiliate accounts carry no CustomerProfile.

        Their only provenance is the manifest in job.connection_config; if the
        rollback reads provenance from CustomerProfile alone they are stranded.
        """
        rollback_migration(self.job)

        self.assertFalse(
            User.objects.filter(pk=self.affiliate_user.pk).exists(),
            "an affiliate user tracked only via connection_config must still be removed",
        )

    def test_affiliate_attached_to_a_pre_existing_account_spares_that_account(self):
        """The importer reuses an existing account when the email matches.

        That account is the merchant's customer, not something the migration
        created, so it must not appear in the manifest's user_ids and must not
        be deleted — even though its Affiliate row is removed.
        """
        existing = self.make_customer("already_a_customer")
        existing_affiliate = Affiliate.objects.create(
            user=existing,
            affiliate_code=f"AFF{uuid.uuid4().hex[:6].upper()}",
            payment_email=existing.email,
        )
        config = dict(self.job.connection_config)
        config["affiliate_rollback_ids"] = dict(config["affiliate_rollback_ids"])
        config["affiliate_rollback_ids"]["affiliate_ids"] = [
            self.affiliate.pk,
            existing_affiliate.pk,
        ]
        self.job.connection_config = config
        self.job.save(update_fields=["connection_config"])

        rollback_migration(self.job)

        self.assertFalse(Affiliate.objects.filter(pk=existing_affiliate.pk).exists())
        self.assertTrue(
            User.objects.filter(pk=existing.pk).exists(),
            "a pre-existing account the importer merely linked must survive",
        )
        self.assertTrue(CustomerProfile.objects.filter(user=existing).exists())

    def test_a_different_jobs_rows_are_untouched(self):
        other_category = self.make_category("Other Import Cat", job=self.other_job)
        other_product = self.make_product("Other Import Widget", other_category, job=self.other_job)

        rollback_migration(self.job)

        self.assertTrue(Category.objects.filter(pk=other_category.pk).exists())
        self.assertTrue(Product.all_objects.filter(pk=other_product.pk).exists())

    def test_dry_run_changes_nothing(self):
        before = {
            "products": Product.all_objects.count(),
            "categories": Category.objects.count(),
            "orders": Order.objects.count(),
            "order_items": OrderItem.objects.count(),
            "users": User.objects.count(),
            "media": MediaAsset.objects.count(),
            "loyalty": LoyaltyTransaction.objects.count(),
            "affiliates": Affiliate.objects.count(),
            "blog_tags": BlogTag.objects.count(),
        }

        report = rollback_migration(self.job, dry_run=True)

        self.assertEqual(
            before,
            {
                "products": Product.all_objects.count(),
                "categories": Category.objects.count(),
                "orders": Order.objects.count(),
                "order_items": OrderItem.objects.count(),
                "users": User.objects.count(),
                "media": MediaAsset.objects.count(),
                "loyalty": LoyaltyTransaction.objects.count(),
                "affiliates": Affiliate.objects.count(),
                "blog_tags": BlogTag.objects.count(),
            },
            "dry_run must not touch the database",
        )

        # Same shape as a real run.
        self.assertEqual(set(report), {"deleted", "retained"})
        self.assertEqual(report["deleted"], rollback_migration(self.job, dry_run=True)["deleted"])
        self.assertEqual(report["retained"], {})
        self.assertEqual(report["deleted"]["Products"], 1)

        self.job.refresh_from_db()
        self.assertNotEqual(self.job.status, "rolled_back")
        self.assertTrue(self.job.can_rollback)

    def test_rollback_is_idempotent(self):
        first = rollback_migration(self.job)
        self.assertTrue(first["deleted"])

        second = rollback_migration(self.job)  # must not raise

        self.assertEqual(
            second["deleted"], {}, "a second rollback of the same job must delete nothing"
        )
        self.assertEqual(second["retained"], {})


class ImportedOrderDoesNotBlockItsOwnProductsTest(RollbackTestBase):
    """Cascade-awareness.

    OrderItem is CASCADE from Order and PROTECT to Product. An imported order's
    own items therefore reference imported products, and a naive "is anything
    pointing at this product?" check would retain the entire catalogue. The
    closure has to notice those items are themselves being deleted.
    """

    def setUp(self):
        super().setUp()
        self.category = self.make_category("Imported Cat", job=self.job)
        self.product_a = self.make_product("Imported A", self.category, job=self.job)
        self.product_b = self.make_product("Imported B", self.category, job=self.job)

        self.customer = self.make_customer("imported_customer", job=self.job)
        self.order = self.make_order(user=self.customer, job=self.job)
        self.make_order_item(self.order, self.product_a)
        self.make_order_item(self.order, self.product_b)

    def test_products_are_deletable_despite_imported_order_items(self):
        plan = plan_rollback(self.job)

        self.assertEqual(
            plan.pks(Product),
            {self.product_a.pk, self.product_b.pk},
            "an imported order's own items must not protect the imported products",
        )
        self.assertFalse(plan.has_retentions)

        report = rollback_migration(self.job)

        self.assertEqual(report["retained"], {})
        self.assertEqual(Product.all_objects.filter(migration_job=self.job).count(), 0)
        self.assertFalse(Category.objects.filter(pk=self.category.pk).exists())


class RollbackRefusedTest(RollbackTestBase):
    """The fail-closed path.

    RollbackRefused exists so that an unmodelled PROTECT edge surfaces as a
    merchant-readable refusal rather than a half-finished delete. The plan is
    supposed to make it unreachable; this checks the guard is wired to the
    right exception rather than asserting it fires in normal use.
    """

    def test_refusal_is_a_distinct_exception(self):
        self.assertTrue(issubclass(RollbackRefused, Exception))
        self.assertFalse(issubclass(RollbackRefused, SystemExit))


class DependentRowsAreFoldedInTest(RollbackTestBase):
    """Rows the import created that are only reachable through a PROTECT edge.

    Some rows an import creates are not seeds and are not cascade descendants of
    a seed — they sit on the *protecting* side of the edge. Loyalty transactions
    protect the loyalty member that cascades from an imported customer; wallet
    transactions protect that customer's wallet; a shipment protects the order
    it belongs to. All three belong to the import and all three must go with it.

    rollback._dependent_seeds is what folds them in, but it is derived from an
    already-settled plan (`plan.pks(User)`, `plan.pks(Order)`). Once the
    retention pass withdraws the ancestor *because* of those very rows, the
    query it feeds is empty, nothing is folded in, and the withdrawal is never
    reconsidered. Each test below is a minimal instance of that circularity.
    """

    def test_imported_customer_with_loyalty_points_is_deleted(self):
        customer = self.make_customer("imported_customer", job=self.job)
        txn = self.make_loyalty_txn(customer, points=100, description="Imported balance")

        report = rollback_migration(self.job)

        self.assertFalse(
            User.objects.filter(pk=customer.pk).exists(),
            "points the import itself created must not keep the imported customer alive",
        )
        self.assertFalse(LoyaltyTransaction.objects.filter(pk=txn.pk).exists())
        self.assertEqual(report["retained"], {})

    def test_customer_with_store_credit_is_kept_and_their_money_survives(self):
        """Store credit is always real money, so it always keeps the customer.

        This test previously asserted the opposite, on the assumption that an
        import can create store credit. It cannot: nothing in migration/importers
        or migration/services creates a CustomerWallet or a WalletTransaction, so
        every balance on a migrated customer was granted by the merchant after
        go-live — goodwill, a refund, a referral or a promotion. Deleting it
        would destroy real money, and wallet transactions are declared immutable
        and append-only by their own model.
        """
        customer = self.make_customer("imported_customer", job=self.job)
        wallet = CustomerWallet.objects.create(customer=customer)
        txn = WalletTransaction.objects.create(
            wallet=wallet,
            transaction_type="credit",
            amount=Money(Decimal("25.00"), "USD"),
            balance_after=Money(Decimal("25.00"), "USD"),
            source="manual",
            description="Goodwill credit granted after go-live",
        )

        report = rollback_migration(self.job)

        self.assertTrue(
            User.objects.filter(pk=customer.pk).exists(),
            "a customer holding store credit must survive the rollback",
        )
        self.assertTrue(WalletTransaction.objects.filter(pk=txn.pk).exists())
        self.assertTrue(CustomerWallet.objects.filter(pk=wallet.pk).exists())
        self.assertIn(
            "auth.User",
            report["retained"],
            "keeping the customer must be reported, not silent",
        )

    def test_imported_order_with_a_shipment_is_deleted(self):
        """The shipment's own user must not decide the order's fate.

        Shipment.user is CASCADE from User, so when the buyer is also being
        deleted the shipment lands in the cascade closure and the order is
        deletable by accident. A guest order — or one shipped by a staff
        account — has no such luck, and that is the case that breaks.
        """
        order = self.make_order(user=None, job=self.job)
        shipment = self.make_shipment(order, self.staff)

        report = rollback_migration(self.job)

        self.assertFalse(
            Order.objects.filter(pk=order.pk).exists(),
            "a shipment the import created must not protect the order it belongs to",
        )
        self.assertFalse(Shipment.objects.filter(pk=shipment.pk).exists())
        self.assertEqual(report["retained"], {})

    def test_a_genuine_shipment_on_a_retained_order_is_untouched(self):
        """The mirror image: this retention is correct and must stay."""
        customer = self.make_customer("imported_customer", job=self.job)
        genuine_order = self.make_order(user=customer, job=None)
        genuine_shipment = self.make_shipment(genuine_order, customer)

        rollback_migration(self.job)

        self.assertTrue(Order.objects.filter(pk=genuine_order.pk).exists())
        self.assertTrue(Shipment.objects.filter(pk=genuine_shipment.pk).exists())
        self.assertTrue(User.objects.filter(pk=customer.pk).exists())
