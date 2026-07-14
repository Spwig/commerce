"""
Product scenario builders for E2E testing.

Each function creates a fully-configured product of a specific type
with all related objects needed for frontend display and cart operations.

Usage in tests:
    from tests.fixtures.product_scenarios import simple_product_scenario

    def test_simple_product(db, site_settings):
        data = simple_product_scenario()
        product = data['product']
"""

from decimal import Decimal

from tests.factories import (
    CategoryFactory,
    ProductFactory,
    ProductVariantFactory,
)


def simple_product_scenario():
    """
    Simple product with features, ready for frontend display.

    Returns dict with: product, category
    """
    category = CategoryFactory(name="Widgets", slug="widgets")
    product = ProductFactory(
        name="Simple Widget",
        slug="simple-widget",
        category=category,
        price=Decimal("29.99"),
        product_type="simple",
        status="published",
        weight=Decimal("0.5"),
        short_description="A simple test widget for E2E testing",
        features={"Material": "Steel", "Color": "Silver", "Weight": "0.5 kg"},
    )
    return {"product": product, "category": category}


def variable_product_scenario():
    """
    Variable product with 3 size variants (direct selection mode).

    Returns dict with: product, variants, category
    """
    category = CategoryFactory(name="Clothing", slug="clothing")
    product = ProductFactory(
        name="T-Shirt",
        slug="test-tshirt",
        category=category,
        price=Decimal("34.99"),
        product_type="variable",
        status="published",
        weight=Decimal("0.3"),
    )
    variant_s = ProductVariantFactory(product=product, name="Small", sku="TSHIRT-S")
    variant_m = ProductVariantFactory(product=product, name="Medium", sku="TSHIRT-M")
    variant_l = ProductVariantFactory(product=product, name="Large", sku="TSHIRT-L")
    return {
        "product": product,
        "variants": [variant_s, variant_m, variant_l],
        "category": category,
    }


def digital_product_scenario():
    """
    Digital product (no shipping, instant delivery).

    Returns dict with: product, category
    """
    category = CategoryFactory(name="Software", slug="software")
    product = ProductFactory(
        name="E-Book Download",
        slug="ebook-download",
        category=category,
        price=Decimal("14.99"),
        product_type="digital",
        digital=True,
        status="published",
        page_template="digital",
        short_description="A comprehensive guide in PDF format",
        features={"Format": "PDF", "Pages": "250", "Language": "English"},
    )
    return {"product": product, "category": category}


def bundle_product_scenario():
    """
    Bundle product with 2 component products.

    Returns dict with: bundle, components, category
    """
    from catalog.models import BundleItem

    category = CategoryFactory(name="Bundles", slug="bundles")
    comp_a = ProductFactory(
        name="Bundle Component A",
        slug="bundle-comp-a",
        category=category,
        price=Decimal("15.00"),
        status="published",
    )
    comp_b = ProductFactory(
        name="Bundle Component B",
        slug="bundle-comp-b",
        category=category,
        price=Decimal("20.00"),
        status="published",
    )
    bundle = ProductFactory(
        name="Starter Bundle",
        slug="starter-bundle",
        category=category,
        price=Decimal("30.00"),
        product_type="bundle",
        status="published",
        bundle_pricing_strategy="fixed",
    )
    BundleItem.objects.create(
        bundle=bundle,
        component_product=comp_a,
        quantity=1,
        sort_order=0,
    )
    BundleItem.objects.create(
        bundle=bundle,
        component_product=comp_b,
        quantity=2,
        sort_order=1,
    )
    return {
        "bundle": bundle,
        "components": [comp_a, comp_b],
        "category": category,
    }


def gift_card_product_scenario():
    """
    Gift card product with fixed denominations.

    Returns dict with: product, category
    """
    category = CategoryFactory(name="Gift Cards", slug="gift-cards")
    product = ProductFactory(
        name="Store Gift Card",
        slug="store-gift-card",
        category=category,
        price=Decimal("50.00"),
        product_type="gift_card",
        status="published",
    )
    product.gift_card_denomination_type = "fixed"
    product.gift_card_denominations = [25, 50, 100, 200]
    product.save(update_fields=["gift_card_denomination_type", "gift_card_denominations"])
    return {"product": product, "category": category}


def customizable_product_scenario():
    """
    Customizable product with a text engraving option.

    Returns dict with: product, options, category
    """
    from catalog.models import CustomizationOption

    category = CategoryFactory(name="Gifts", slug="gifts")
    product = ProductFactory(
        name="Personalized Mug",
        slug="personalized-mug",
        category=category,
        price=Decimal("19.99"),
        product_type="customizable",
        status="published",
        allow_customization=True,
    )
    option = CustomizationOption.objects.create(
        product=product,
        name="Engraving Text",
        slug="engraving-text",
        option_type="text",
        is_required=True,
        sort_order=0,
    )
    return {"product": product, "options": [option], "category": category}


def configurable_product_scenario():
    """
    Configurable product (build-to-order) with configuration slots.

    Returns dict with: product, slots, options, category
    """
    from catalog.models import ConfigurationSlot, ConfigurationSlotOption

    category = CategoryFactory(name="Computers", slug="computers")
    product = ProductFactory(
        name="Custom PC",
        slug="custom-pc",
        category=category,
        price=Decimal("999.99"),
        product_type="configurable",
        status="published",
        configurator_pricing_strategy="components_sum",
    )
    cpu_slot = ConfigurationSlot.objects.create(
        product=product,
        name="Processor",
        slug="processor",
        is_required=True,
        min_selections=1,
        max_selections=1,
        sort_order=0,
    )
    ram_slot = ConfigurationSlot.objects.create(
        product=product,
        name="Memory",
        slug="memory",
        is_required=True,
        min_selections=1,
        max_selections=1,
        sort_order=1,
    )
    # Option products
    cpu_option = ProductFactory(
        name="Intel i7",
        slug="intel-i7",
        category=category,
        price=Decimal("350.00"),
        status="published",
    )
    ram_option = ProductFactory(
        name="16GB RAM",
        slug="16gb-ram",
        category=category,
        price=Decimal("120.00"),
        status="published",
    )
    ConfigurationSlotOption.objects.create(
        slot=cpu_slot,
        option_product=cpu_option,
        sort_order=0,
    )
    ConfigurationSlotOption.objects.create(
        slot=ram_slot,
        option_product=ram_option,
        sort_order=0,
    )
    return {
        "product": product,
        "slots": [cpu_slot, ram_slot],
        "options": [cpu_option, ram_option],
        "category": category,
    }
