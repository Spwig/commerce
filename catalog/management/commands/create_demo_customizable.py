"""Create demo CUSTOMIZABLE products (the CustomizationOption path — text
engraving, dropdowns) for a deployed cert/demo host.

The only product type with no seeder, so the black-box cert suite couldn't buy
one. Mirrors create_demo_bookings / create_demo_configurator: one product per
--product key, USD, idempotent, stock created in the default warehouse.

    python manage.py create_demo_customizable --product personalized_mug
    python manage.py create_demo_customizable --product custom_tshirt --delete
"""

from decimal import Decimal

from django.core.management.base import BaseCommand

# Each product: a physical item with one or more CustomizationOptions.
PRODUCTS = {
    "personalized_mug": {
        "name": "Personalized Mug",
        "slug": "personalized-mug",
        "sku": "DEMO-CUSTOM-MUG",
        "price": Decimal("19.99"),
        "category": "Demo Personalized",
        "options": [
            {"name": "Engraving Text", "slug": "engraving-text", "option_type": "text"},
        ],
    },
    "custom_tshirt": {
        "name": "Custom Print T-Shirt",
        "slug": "custom-print-tshirt",
        "sku": "DEMO-CUSTOM-TEE",
        "price": Decimal("24.99"),
        "category": "Demo Personalized",
        "options": [
            {"name": "Front Text", "slug": "front-text", "option_type": "text"},
            {"name": "Ink Colour", "slug": "ink-colour", "option_type": "color"},
        ],
    },
}


class Command(BaseCommand):
    help = "Create a demo customizable product (CustomizationOption path)"

    def add_arguments(self, parser):
        parser.add_argument("--product", required=True, choices=PRODUCTS.keys())
        parser.add_argument("--delete", action="store_true", help="Delete the product instead")

    def handle(self, *args, **options):
        spec = PRODUCTS[options["product"]]
        if options["delete"]:
            self._delete(spec)
        else:
            self._create(spec)

    def _delete(self, spec):
        from catalog.models import Product

        n, _ = Product.all_objects.filter(sku=spec["sku"]).delete()
        self.stdout.write(f"Deleted {spec['sku']} ({n} objects)")

    def _create(self, spec):
        from catalog.models import (
            Category,
            CustomizationOption,
            Product,
            StockItem,
            Warehouse,
        )

        existing = Product.all_objects.filter(sku=spec["sku"]).first()
        if existing:
            # Idempotent: still make sure the storefront design config exists —
            # older runs created only CustomizationOptions, which the storefront
            # does NOT render, leaving the product unbuyable (backend returns
            # "requires customization" with no UI to satisfy it).
            self._ensure_design_config(existing)
            self.stdout.write(f"{spec['sku']} exists — ensured design config")
            return

        category, _ = Category.objects.get_or_create(
            name=spec["category"],
            defaults={"slug": spec["category"].lower().replace(" ", "-")},
        )
        product = Product.objects.create(
            name=spec["name"],
            slug=spec["slug"],
            sku=spec["sku"],
            product_type="customizable",
            category=category,
            price=spec["price"],
            price_currency="USD",
            status="published",
            allow_customization=True,
        )
        for i, opt in enumerate(spec["options"]):
            CustomizationOption.objects.create(
                product=product,
                name=opt["name"],
                slug=opt["slug"],
                option_type=opt["option_type"],
                is_required=opt.get("is_required", i == 0),
                sort_order=i,
            )

        # The storefront customization UI is the Fabric.js design editor, which
        # renders ONLY when the product has a ProductDesignConfig with an enabled
        # surface (page_builder/views.py routes to designer.html on that). Without
        # it the product can't be customized or bought from the storefront.
        self._ensure_design_config(product)

        # Stock it so it's buyable (customizable is a physical product).
        warehouse = Warehouse.objects.filter(code="MAIN-WH").first()
        if warehouse:
            StockItem.objects.get_or_create(
                product=product, warehouse=warehouse, variant=None, defaults={"on_hand": 50}
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Created customizable '{product.name}' ({len(spec['options'])} option(s) "
                "+ design editor)"
            )
        )

    def _ensure_design_config(self, product):
        """Give the product a canvas design editor with one enabled 'Front'
        surface, so the storefront renders the Fabric.js editor and add-to-cart
        (which requires a design element) is reachable. Idempotent."""
        from customizable_product.models import ProductDesignConfig, ProductSurface

        config, _ = ProductDesignConfig.objects.get_or_create(
            product=product,
            defaults={"is_enabled": True, "editor_mode": "canvas", "allow_text": True},
        )
        ProductSurface.objects.get_or_create(
            design_config=config,
            slug="front",
            defaults={"name": "Front", "sort_order": 0, "is_enabled": True},
        )
