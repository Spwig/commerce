"""
Checkout scenario builders.

Each function creates a complete merchant shipping/tax configuration
for testing. Returns a dict with all created objects for assertions.

Usage in tests:
    from tests.fixtures.checkout_scenarios import domestic_us_merchant

    @pytest.fixture
    def domestic_merchant(db):
        return domestic_us_merchant()
"""
from decimal import Decimal
from tests.factories import (
    ShippingZoneFactory, ShippingMethodFactory, TaxRateFactory,
    SalesRegionFactory, WarehouseFactory, ProductFactory,
    ProductVariantFactory, StockItemFactory,
    ShippingCountryFactory, CountryWarehouseFallbackFactory,
    CategoryFactory,
)


def domestic_us_merchant():
    """
    US-only merchant with three shipping tiers.

    - Standard Shipping: $5.99 (5-7 days)
    - Express Shipping: $14.99 (1-3 days)
    - Free Shipping: $0 but requires min_order_value=$100
    """
    zone = ShippingZoneFactory(name='US Domestic', countries=['US'])

    standard = ShippingMethodFactory(
        name='Standard Shipping',
        flat_rate_cost=Decimal('5.99'),
        min_delivery_days=5,
        max_delivery_days=7,
        zones=[zone],
    )
    express = ShippingMethodFactory(
        name='Express Shipping',
        flat_rate_cost=Decimal('14.99'),
        min_delivery_days=1,
        max_delivery_days=3,
        zones=[zone],
    )
    free = ShippingMethodFactory(
        name='Free Shipping',
        method_type='free_shipping',
        flat_rate_cost=Decimal('0.00'),
        min_order_value=Decimal('100.00'),
        min_order_value_currency='USD',
        min_delivery_days=7,
        max_delivery_days=10,
        zones=[zone],
    )

    # ShippingCountry record (needed by payment method filter)
    us_country = ShippingCountryFactory(country_code='US')

    tax_ny = TaxRateFactory(ny=True)
    tax_ca = TaxRateFactory(ca=True)

    return {
        'zone': zone,
        'methods': {'standard': standard, 'express': express, 'free': free},
        'taxes': {'ny': tax_ny, 'ca': tax_ca},
        'shipping_country': us_country,
    }


def international_merchant():
    """
    International merchant with zone-based shipping.

    Zones:
    - North America (US, CA, MX): Domestic Standard $5.99
    - Europe (GB, DE, FR, ES, IT, NL): Intl Standard $19.99, Express $39.99
    - Asia Pacific (JP, AU, SG, KR): Intl Standard $19.99, Express $39.99

    Tax: UK VAT 20%, DE VAT 19%
    """
    na_zone = ShippingZoneFactory(
        name='North America',
        countries=['US', 'CA', 'MX'],
    )
    eu_zone = ShippingZoneFactory(
        name='Europe',
        countries=['GB', 'DE', 'FR', 'ES', 'IT', 'NL'],
    )
    apac_zone = ShippingZoneFactory(
        name='Asia Pacific',
        countries=['JP', 'AU', 'SG', 'KR'],
    )

    domestic = ShippingMethodFactory(
        name='Domestic Standard',
        flat_rate_cost=Decimal('5.99'),
        min_delivery_days=3,
        max_delivery_days=7,
        zones=[na_zone],
    )
    intl_standard = ShippingMethodFactory(
        name='International Standard',
        flat_rate_cost=Decimal('19.99'),
        min_delivery_days=7,
        max_delivery_days=14,
        zones=[eu_zone, apac_zone],
    )
    intl_express = ShippingMethodFactory(
        name='International Express',
        flat_rate_cost=Decimal('39.99'),
        min_delivery_days=3,
        max_delivery_days=5,
        zones=[eu_zone, apac_zone],
    )

    uk_vat = TaxRateFactory(uk_vat=True)
    de_vat = TaxRateFactory(de_vat=True)

    return {
        'zones': {'na': na_zone, 'eu': eu_zone, 'apac': apac_zone},
        'methods': {
            'domestic': domestic,
            'intl_standard': intl_standard,
            'intl_express': intl_express,
        },
        'taxes': {'uk_vat': uk_vat, 'de_vat': de_vat},
    }


def free_shipping_threshold_merchant():
    """
    Merchant offering free shipping for orders over $75.

    Uses a free_shipping method type with min_order_value.
    Standard paid option always available.
    """
    zone = ShippingZoneFactory(name='Worldwide', countries=[])

    standard = ShippingMethodFactory(
        name='Standard Shipping',
        flat_rate_cost=Decimal('7.99'),
        min_delivery_days=5,
        max_delivery_days=10,
        zones=[zone],
    )
    free = ShippingMethodFactory(
        name='Free Shipping (Orders $75+)',
        method_type='free_shipping',
        flat_rate_cost=Decimal('0.00'),
        min_order_value=Decimal('75.00'),
        min_order_value_currency='USD',
        min_delivery_days=7,
        max_delivery_days=14,
        zones=[zone],
    )

    return {
        'zone': zone,
        'methods': {'standard': standard, 'free': free},
    }


def multi_warehouse_merchant():
    """
    Multi-warehouse merchant for fulfillment/allocation tests.

    Regions:
    - US region (priority 80): US, CA countries
    - EU region (priority 60): GB, DE, FR countries

    Warehouses:
    - US-EAST (NJ, priority 80, coords: 40.73, -74.17)
    - EU-WEST (DE, priority 60, coords: 50.11, 8.68)

    Products:
    - product_a: simple product, 100 units at US-EAST, 20 units at EU-WEST
    - product_b: simple product, 5 units at US-EAST, 80 units at EU-WEST
    - variable_product: variable product with 2 variants
        - variant_red: 50 units at US-EAST, 0 at EU-WEST
        - variant_blue: 0 at US-EAST, 40 at EU-WEST

    ShippingCountry + Fallbacks:
    - AU shipping country with source_warehouse=None
    - AU fallback 1: EU-WEST (priority 0)
    - AU fallback 2: US-EAST (priority 1)
    """
    from catalog.models import SalesRegion, Warehouse

    # Deactivate any pre-existing regions/warehouses from migrations
    # so they don't interfere with our test data
    SalesRegion.objects.exclude(code__in=['NAM', 'EUR']).update(is_active=False)
    Warehouse.objects.exclude(code__in=['US-EAST', 'EU-WEST']).update(is_active=False)

    category = CategoryFactory(name='Fulfillment Test', slug='fulfillment-test')

    # Regions
    us_region = SalesRegionFactory(
        name='North America', code='NAM', countries=['US', 'CA'],
        default_currency='USD', priority=80,
    )
    eu_region = SalesRegionFactory(
        name='Europe', code='EUR', countries=['GB', 'DE', 'FR'],
        default_currency='EUR', priority=60,
    )

    # Warehouses
    wh_us = WarehouseFactory(
        name='US East Warehouse', code='US-EAST',
        region=us_region,
        address_line1='100 Warehouse Dr', city='Newark',
        state_province='NJ', postal_code='07102', country='US',
        fulfillment_priority=80,
        latitude=Decimal('40.735657'), longitude=Decimal('-74.172363'),
    )
    wh_eu = WarehouseFactory(
        name='EU West Warehouse', code='EU-WEST',
        region=eu_region,
        address_line1='10 Lager Str', city='Frankfurt',
        state_province='Hessen', postal_code='60311', country='DE',
        fulfillment_priority=60,
        latitude=Decimal('50.110924'), longitude=Decimal('8.682127'),
    )

    # Simple products
    product_a = ProductFactory(
        name='Widget A', slug='widget-a', category=category,
        track_inventory=True, price=Decimal('25.00'),
    )
    product_b = ProductFactory(
        name='Widget B', slug='widget-b', category=category,
        track_inventory=True, price=Decimal('35.00'),
    )

    # Stock for simple products
    stock_a_us = StockItemFactory(product=product_a, warehouse=wh_us, on_hand=100)
    stock_a_eu = StockItemFactory(product=product_a, warehouse=wh_eu, on_hand=20)
    stock_b_us = StockItemFactory(product=product_b, warehouse=wh_us, on_hand=5)
    stock_b_eu = StockItemFactory(product=product_b, warehouse=wh_eu, on_hand=80)

    # Variable product with variants
    variable_product = ProductFactory(
        name='T-Shirt', slug='t-shirt', category=category,
        product_type='variable', track_inventory=True, price=Decimal('29.99'),
    )
    variant_red = ProductVariantFactory(
        product=variable_product, name='Red', sku='TSHIRT-RED',
    )
    variant_blue = ProductVariantFactory(
        product=variable_product, name='Blue', sku='TSHIRT-BLUE',
    )

    # Stock for variants
    stock_red_us = StockItemFactory(
        product=variable_product, warehouse=wh_us,
        variant=variant_red, on_hand=50,
    )
    stock_red_eu = StockItemFactory(
        product=variable_product, warehouse=wh_eu,
        variant=variant_red, on_hand=0,
    )
    stock_blue_us = StockItemFactory(
        product=variable_product, warehouse=wh_us,
        variant=variant_blue, on_hand=0,
    )
    stock_blue_eu = StockItemFactory(
        product=variable_product, warehouse=wh_eu,
        variant=variant_blue, on_hand=40,
    )

    # ShippingCountry + Fallbacks for AU (no region)
    from django.contrib.sites.models import Site
    site = Site.objects.get_or_create(id=1, defaults={'domain': 'localhost', 'name': 'Test'})[0]

    au_country = ShippingCountryFactory(
        site=site, country_code='AU', source_warehouse=None,
    )
    fallback_au_1 = CountryWarehouseFallbackFactory(
        country=au_country, warehouse=wh_eu, priority=0,
    )
    fallback_au_2 = CountryWarehouseFallbackFactory(
        country=au_country, warehouse=wh_us, priority=1,
    )

    return {
        'regions': {'us': us_region, 'eu': eu_region},
        'warehouses': {'us': wh_us, 'eu': wh_eu},
        'products': {
            'a': product_a,
            'b': product_b,
            'variable': variable_product,
        },
        'variants': {'red': variant_red, 'blue': variant_blue},
        'stock': {
            'a_us': stock_a_us, 'a_eu': stock_a_eu,
            'b_us': stock_b_us, 'b_eu': stock_b_eu,
            'red_us': stock_red_us, 'red_eu': stock_red_eu,
            'blue_us': stock_blue_us, 'blue_eu': stock_blue_eu,
        },
        'shipping_countries': {'au': au_country},
        'fallbacks': {'au_1': fallback_au_1, 'au_2': fallback_au_2},
    }
