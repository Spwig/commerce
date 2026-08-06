"""Seed a coherent demo catalog for a DEPLOYED cert/demo target.

Deliberately NOT part of ``manage.py seed`` — merchants don't want demo products
in their store. Run it *after* seed on a cert host or demo box::

    python manage.py seed
    python manage.py demo_store --profile full

It produces a purchasable US storefront so the ``spwig-e2e`` golden flows can
drive a real checkout to a paid order against the host: products of every type
with stock (in-stock / low / out / backorder / preorder), a redeemable gift
card, fixed + percentage vouchers, and a working flat-rate shipping method +
US shipping-country + sales tax.

Idempotent: every object is keyed on a stable ``demo-`` slug / ``DEMO-`` sku /
code and created via get-or-create, so re-runs (``--force``) don't duplicate.
Two profiles:

- ``smoke`` (default) — the minimal golden set the core flows need.
- ``full`` — the whole catalog-state matrix (variable, bundle, every stock
  state, cross-border shipping).

The catalog it builds is the deployed-target twin of the in-process
``tests/fixtures`` scenarios the shop-dev golden flows use.
"""

from datetime import timedelta
from decimal import Decimal

from django.core.management.base import CommandError
from django.utils import timezone
from djmoney.money import Money

from core.management.commands._seed_base import SeedCommand

_USD = "USD"


class Command(SeedCommand):
    help = (
        "Seed a demo catalog (products, stock, gift card, vouchers, shipping) for a cert/demo host"
    )
    seed_name = "demo_store"
    seed_version = 1
    dependencies = ["site_defaults", "default_warehouse", "tax_presets"]

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--profile",
            choices=["smoke", "full"],
            default="smoke",
            help="smoke = minimal golden set; full = the whole catalog-state matrix",
        )

    def handle(self, *args, **options):
        # Stash the profile so seed() (called by the base handle) can read it.
        self.profile = options.get("profile", "smoke")
        super().handle(*args, **options)

    # ------------------------------------------------------------------ seed

    def seed(self) -> int:
        self.stdout.write(f"    profile: {self.profile}")
        count = 0

        warehouse = self._warehouse()
        count += self._shipping_and_tax()
        count += self._activate_test_gateway()

        apparel = self._category("Demo Apparel", "demo-apparel")
        goods = self._category("Demo Goods", "demo-goods")

        # --- smoke set: enough for the core golden flows ---
        count += self._simple(
            sku="DEMO-TEE",
            name="Demo Cotton Tee",
            slug="demo-cotton-tee",
            price="24.99",
            category=apparel,
            warehouse=warehouse,
            on_hand=50,
        )
        count += self._simple(
            sku="DEMO-MUG",
            name="Demo Ceramic Mug",
            slug="demo-ceramic-mug",
            price="12.50",
            category=goods,
            warehouse=warehouse,
            on_hand=50,
        )
        count += self._digital(
            sku="DEMO-EBOOK",
            name="Demo E-Book",
            slug="demo-ebook",
            price="9.99",
            category=goods,
        )
        count += self._gift_card(warehouse=warehouse)
        count += self._vouchers()

        if self.profile == "full":
            count += self._full_matrix(apparel, goods, warehouse)

        return count

    # -------------------------------------------------------------- helpers

    def _warehouse(self):
        """The default warehouse (MAIN-WH, from ``setup_default_warehouse``).

        Ensure it exists so demo_store is self-sufficient even if a host ran it
        before the full seed — ``setup_default_warehouse`` is idempotent."""
        from django.core.management import call_command

        from catalog.models import Warehouse

        wh = Warehouse.objects.filter(code="MAIN-WH").first()
        if wh is None:
            self.stdout.write("    MAIN-WH missing — creating default warehouse")
            call_command("setup_default_warehouse", skip_stock_migration=True)
            wh = Warehouse.objects.filter(code="MAIN-WH").first()
        if wh is None:
            # Fail loud rather than pass None into a non-null StockItem.warehouse
            # FK and surface an opaque IntegrityError deep in the seed.
            raise CommandError(
                "No MAIN-WH warehouse and setup_default_warehouse did not create one; "
                "run `python manage.py seed` first."
            )
        return wh

    def _category(self, name, slug):
        from catalog.models import Category

        cat, _ = Category.objects.get_or_create(
            slug=slug, defaults={"name": name, "is_active": True}
        )
        return cat

    def _product(self, *, sku, name, slug, product_type, category, price, **extra):
        """Get-or-create a product by SKU (slug/sku are non-unique, so we can't
        rely on get_or_create's uniqueness). Returns (product, created)."""
        from catalog.models import Product

        existing = Product.objects.filter(sku=sku).first()
        if existing:
            return existing, False
        product = Product.objects.create(
            sku=sku,
            name=name,
            slug=slug,
            product_type=product_type,
            category=category,
            price=Money(Decimal(price), _USD),
            status="published",
            **extra,
        )
        return product, True

    def _stock(self, product, warehouse, on_hand, variant=None):
        """Set a product/variant's on-hand at the warehouse (deterministic on
        re-run: overwrite on_hand so stock states stay as declared)."""
        from catalog.models import StockItem

        item, _ = StockItem.objects.get_or_create(
            product=product,
            warehouse=warehouse,
            variant=variant,
            defaults={"on_hand": on_hand},
        )
        if item.on_hand != on_hand:
            item.on_hand = on_hand
            item.save(update_fields=["on_hand"])
        return item

    def _simple(
        self,
        *,
        sku,
        name,
        slug,
        price,
        category,
        warehouse,
        on_hand,
        allow_backorders=False,
        is_preorder=False,
    ):
        extra = {"allow_backorders": allow_backorders}
        if is_preorder:
            extra["is_preorder"] = True
            extra["preorder_release_date"] = timezone.now().date() + timedelta(days=30)
        product, created = self._product(
            sku=sku,
            name=name,
            slug=slug,
            product_type="simple",
            category=category,
            price=price,
            **extra,
        )
        self._stock(product, warehouse, on_hand)
        return 1 if created else 0

    def _digital(self, *, sku, name, slug, price, category):
        # save() forces is_digital=True and requires_shipping=False, and no
        # DigitalAsset is needed to be purchasable (only to deliver a file).
        #
        # track_inventory MUST be set False explicitly: unlike gift_card and
        # booking, Product.save() does NOT clear track_inventory for a plain
        # `digital` product, so it keeps the field default (True). With no
        # StockItem that makes is_in_stock() False → the PDP renders
        # out-of-stock and add-to-cart is refused. (Filed as a finding: the
        # model arguably should force this like it does for gift_card/booking.)
        _, created = self._product(
            sku=sku,
            name=name,
            slug=slug,
            product_type="digital",
            category=category,
            price=price,
            track_inventory=False,
        )
        return 1 if created else 0

    def _gift_card(self, *, warehouse):
        """A gift-card product plus one redeemable card with a known code, so a
        flow can apply DEMOGIFT25 for $25 of stored value."""
        from catalog.models import GiftCard

        category = self._category("Demo Gift Cards", "demo-gift-cards")
        product, created = self._product(
            sku="DEMO-GIFTCARD",
            name="Demo Gift Card",
            slug="demo-gift-card",
            product_type="gift_card",
            category=category,
            price="25.00",
            gift_card_currency=_USD,
            # Preset denominations MUST be seeded: with the default empty list
            # the PDP renders no ".gift-card-denom" buttons and (for the
            # "fixed" type) no custom-amount input either, so there is nothing
            # to select and the card can't be bought. "both" also allows a
            # custom amount, exercising both denomination paths in one product.
            gift_card_denomination_type="both",
            gift_card_denominations=[25, 50, 100],
            gift_card_min_amount=Decimal("10.00"),
            gift_card_max_amount=Decimal("500.00"),
        )
        count = 1 if created else 0
        # initial_value has default_currency=None → an explicit currency is
        # mandatory; current_balance defaults to initial_value on create.
        card, card_created = GiftCard.objects.get_or_create(
            code="DEMOGIFT25",
            defaults={
                "product": product,
                "initial_value": Money(Decimal("25.00"), _USD),
                "recipient_email": "demo-giftee@example.test",
                "is_active": True,
            },
        )
        if not card_created:
            # Restore known state: a prior cert run may have depleted the balance
            # or deactivated it. demo_store is the "reset to a purchasable store"
            # tool, so re-running must top the card back up.
            card.current_balance = Money(Decimal("25.00"), _USD)
            card.is_active = True
            card.save(update_fields=["current_balance", "current_balance_currency", "is_active"])
        return count + (1 if card_created else 0)

    def _vouchers(self):
        """A reusable fixed voucher (for repeatable flows), a single-use fixed
        one (the matrix's single-use case), and a reusable percentage voucher."""
        from vouchers.models import VoucherCode

        specs = [
            # (code, name, type, value, extra)
            ("DEMO5", "Demo $5 off (reusable)", "fixed", "5.00", {}),
            ("DEMOONCE", "Demo $10 off (single-use)", "fixed", "10.00", {"max_uses_total": 1}),
            (
                "DEMO20PCT",
                "Demo 20% off (reusable)",
                "percentage",
                "20.00",
                {"max_discount_amount": Money(Decimal("50.00"), _USD)},
            ),
        ]
        created = 0
        for code, name, dtype, value, extra in specs:
            voucher, was_created = VoucherCode.objects.get_or_create(
                code=code,
                defaults={
                    "name": name,
                    "discount_type": dtype,
                    "discount_value": Decimal(value),
                    "currency": _USD,
                    "is_active": True,
                    "created_by": None,
                    **extra,
                },
            )
            if not was_created:
                # Restore known state: a single-use voucher consumed by a prior
                # cert run must be reset so it can be applied again.
                voucher.current_uses = 0
                voucher.is_active = True
                voucher.save(update_fields=["current_uses", "is_active"])
            created += 1 if was_created else 0
        return created

    def _activate_test_gateway(self) -> int:
        """Make the simulated test_gateway usable at checkout.

        `seed` installs the test_gateway component and an account but leaves the
        account inactive, so it never surfaces at checkout. A demo/cert store
        pays with it (deterministic magic cards), so activate it. Simulated
        gateways only ever show in sandbox mode (a dev/staging licence) — they're
        hidden in production regardless — so activating it is safe on any install.
        """
        from payment_providers.models import PaymentProviderAccount

        updated = PaymentProviderAccount.objects.filter(component__slug="test_gateway").update(
            is_active=True, connection_status="connected"
        )
        if updated:
            self.stdout.write(f"    activated test_gateway ({updated} account)")
        else:
            self.stdout.write(
                self.style.WARNING(
                    "    no test_gateway account to activate — run `seed` "
                    "(install_bundled_components) first"
                )
            )
        return 1 if updated else 0

    def _shipping_and_tax(self) -> int:
        """A working flat-rate shipping method, a US shipping-country (payment
        methods filter on it), and a US sales-tax rate — the minimum for a US
        checkout to reach payment and carry tax."""
        from django.contrib.sites.models import Site

        from cart.models import ShippingMethod, TaxRate
        from shipping.models import ShippingCountry

        count = 0
        _, created = ShippingMethod.objects.get_or_create(
            name="Standard Shipping",
            defaults={
                "method_type": "flat_rate",
                "flat_rate_cost": Money(Decimal("5.00"), _USD),
                "is_active": True,
            },
        )
        count += 1 if created else 0

        site = Site.objects.get(pk=1)
        _, created = ShippingCountry.objects.get_or_create(
            site=site, country_code="US", defaults={"is_active": True}
        )
        count += 1 if created else 0

        _, created = TaxRate.objects.get_or_create(
            name="Demo US Sales Tax",
            country="US",
            defaults={"state": "NY", "rate": Decimal("0.08875"), "tax_type": "sales_tax"},
        )
        count += 1 if created else 0
        return count

    # ------------------------------------------------------- full matrix

    def _full_matrix(self, apparel, goods, warehouse) -> int:
        """The rest of the catalog-state matrix beyond the smoke set."""
        count = 0

        # Stock states on simple products.
        count += self._simple(
            sku="DEMO-LOW",
            name="Demo Low-Stock Item",
            slug="demo-low-stock",
            price="19.99",
            category=goods,
            warehouse=warehouse,
            on_hand=2,  # < threshold 5
        )
        count += self._simple(
            sku="DEMO-OOS",
            name="Demo Out-of-Stock Item",
            slug="demo-out-of-stock",
            price="19.99",
            category=goods,
            warehouse=warehouse,
            on_hand=0,
        )
        count += self._simple(
            sku="DEMO-BACKORDER",
            name="Demo Backorder Item",
            slug="demo-backorder",
            price="29.99",
            category=goods,
            warehouse=warehouse,
            on_hand=0,
            allow_backorders=True,
        )
        count += self._simple(
            sku="DEMO-PREORDER",
            name="Demo Pre-Order Item",
            slug="demo-preorder",
            price="39.99",
            category=goods,
            warehouse=warehouse,
            on_hand=0,
            is_preorder=True,
        )

        count += self._variable(apparel, warehouse)
        count += self._bundle(goods, warehouse)
        count += self._cross_border_shipping()
        return count

    def _variable(self, category, warehouse) -> int:
        from catalog.models import ProductVariant

        product, created = self._product(
            sku="DEMO-HOODIE",
            name="Demo Hoodie",
            slug="demo-hoodie",
            product_type="variable",
            category=category,
            price="49.99",
        )
        count = 1 if created else 0
        for size in ("S", "M", "L"):
            variant, v_created = ProductVariant.objects.get_or_create(
                sku=f"DEMO-HOODIE-{size}",
                defaults={"product": product, "name": f"Size {size}"},
            )
            # Variant SKU is globally unique — if this SKU already belonged to a
            # different product, we'd stock a foreign variant. Fail loud instead.
            if variant.product_id != product.id:
                raise CommandError(
                    f"variant SKU DEMO-HOODIE-{size} already exists on product "
                    f"{variant.product_id}, not the demo hoodie ({product.id})"
                )
            self._stock(product, warehouse, on_hand=20, variant=variant)
            count += 1 if v_created else 0
        return count

    def _bundle(self, category, warehouse) -> int:
        from catalog.models import BundleItem, Product

        # Two simple components for the bundle.
        tee = Product.objects.filter(sku="DEMO-TEE").first()
        mug = Product.objects.filter(sku="DEMO-MUG").first()

        # track_inventory=False on the bundle PARENT: a bundle's availability
        # derives from its components' stock, and cart add-to-cart checks the
        # top-level product's inventory BEFORE the bundle branch — a tracked
        # bundle with no StockItem of its own fails "insufficient stock" before
        # component stock is consulted. (Product.save() only auto-disables
        # inventory for gift_card/booking, not bundle, so set it explicitly.)
        bundle, created = self._product(
            sku="DEMO-BUNDLE",
            name="Demo Starter Bundle",
            slug="demo-starter-bundle",
            product_type="bundle",
            category=category,
            price="32.00",
            bundle_pricing_strategy="fixed",
            track_inventory=False,
        )
        count = 1 if created else 0
        for component in (tee, mug):
            if component is None:
                continue
            BundleItem.objects.get_or_create(
                bundle=bundle,
                component_product=component,
                component_variant=None,
                defaults={"quantity": 1},
            )
        # Re-save so the bundle's is_digital reflects its (now attached) components.
        bundle.save()
        return count

    def _cross_border_shipping(self) -> int:
        """A US vs International zone split + an express method, so cross-border
        journeys have somewhere to go."""
        from cart.models import ShippingMethod
        from shipping.models import ShippingZone

        count = 0
        us_zone, created = ShippingZone.objects.get_or_create(
            name="Demo United States", defaults={"countries": ["US"]}
        )
        count += 1 if created else 0
        intl_zone, created = ShippingZone.objects.get_or_create(
            name="Demo International",
            defaults={"countries": []},  # empty = everywhere else
        )
        count += 1 if created else 0

        express, created = ShippingMethod.objects.get_or_create(
            name="Demo Express Shipping",
            defaults={
                "method_type": "flat_rate",
                "flat_rate_cost": Money(Decimal("15.00"), _USD),
                "is_active": True,
            },
        )
        if created:
            express.zones.add(us_zone, intl_zone)
        count += 1 if created else 0
        return count
