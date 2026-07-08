"""
Shared pytest fixtures for the Spwig test pipeline.

These fixtures provide the foundational test data (site settings, users,
products, warehouse, etc.) that any test suite can depend on.
"""
import pytest
import tempfile
import shutil
from pathlib import Path
from decimal import Decimal
from .factories import (
    UserFactory, CategoryFactory, ProductFactory,
    SalesRegionFactory, WarehouseFactory, CartFactory, CartItemFactory,
    VoucherFactory, OrderFactory, MediaAssetFactory,
)


# ============================================================
# Test Configuration (File Storage)
# ============================================================

@pytest.fixture(scope='session', autouse=True)
def temp_media_root():
    """
    Create a temporary directory for media files during test session.
    This prevents permission errors in Docker where the container runs as root
    but the host media directory is owned by a different user.
    """
    temp_dir = tempfile.mkdtemp(prefix='test_media_')
    yield Path(temp_dir)
    # Cleanup after all tests complete
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture(autouse=True)
def configure_test_media_root(settings, temp_media_root):
    """
    Override Django's MEDIA_ROOT to use temporary directory for all tests.
    This is applied automatically to every test.
    """
    settings.MEDIA_ROOT = temp_media_root
    # Keep MEDIA_URL as /media/ for test consistency
    settings.MEDIA_URL = '/media/'


# ============================================================
# Core Infrastructure (required by single-tenant architecture)
# ============================================================

@pytest.fixture
def site_settings(db):
    """Create SiteSettings required for single-tenant operation."""
    from core.models import SiteSettings
    settings, _ = SiteSettings.objects.get_or_create(
        pk=1,
        defaults={
            'site_name': 'Test Store',
            'admin_email': 'admin@test.spwig.com',
            'default_currency': 'USD',
            'default_language': 'en',
        }
    )
    return settings


@pytest.fixture
def django_site(db):
    """Ensure Django Sites framework has a site with ID=1."""
    from django.contrib.sites.models import Site
    site, _ = Site.objects.get_or_create(
        id=1,
        defaults={'domain': 'localhost', 'name': 'Test Site'}
    )
    return site


# ============================================================
# Users
# ============================================================

@pytest.fixture
def admin_user(db):
    """Staff superuser for admin operations."""
    return UserFactory(
        username='test_admin',
        email='admin@test.spwig.com',
        staff=True,
    )


@pytest.fixture
def customer_user(db):
    """Regular customer user."""
    return UserFactory(
        username='test_customer',
        email='customer@test.spwig.com',
    )


@pytest.fixture
def customer_user_uk(db):
    """UK-based customer user."""
    return UserFactory(
        username='test_customer_uk',
        email='customer_uk@test.spwig.com',
    )


@pytest.fixture
def customer_user_de(db):
    """DE-based customer user."""
    return UserFactory(
        username='test_customer_de',
        email='customer_de@test.spwig.com',
    )


# ============================================================
# Catalog
# ============================================================

@pytest.fixture
def category(db):
    """Default test category."""
    return CategoryFactory(name='Test Products', slug='test-products')


@pytest.fixture
def sales_region(db):
    """Default sales region covering major countries."""
    return SalesRegionFactory()


@pytest.fixture
def warehouse(db, sales_region):
    """Default warehouse."""
    return WarehouseFactory(region=sales_region)


@pytest.fixture
def simple_product(db, category):
    """$25 physical product, no inventory tracking."""
    return ProductFactory(
        name='Test Widget A',
        slug='test-widget-a',
        category=category,
        price=Decimal('25.00'),
        weight=Decimal('0.5'),
    )


@pytest.fixture
def expensive_product(db, category):
    """$150 product (over typical free-shipping thresholds)."""
    return ProductFactory(
        name='Test Bundle',
        slug='test-bundle',
        category=category,
        expensive=True,
    )


@pytest.fixture
def digital_product(db, category):
    """$9.99 digital product, no shipping required."""
    return ProductFactory(
        name='Digital Download',
        slug='digital-download',
        category=category,
        price=Decimal('9.99'),
        digital=True,
    )


@pytest.fixture
def heavy_product(db, category):
    """$89 heavy product for weight-based shipping tests."""
    return ProductFactory(
        name='Heavy Widget',
        slug='heavy-widget',
        category=category,
        price=Decimal('89.00'),
        heavy=True,
    )


# ============================================================
# Cart helpers
# ============================================================

@pytest.fixture
def cart_with_item(db, customer_user, simple_product, site_settings):
    """Cart with one $25 item."""
    cart = CartFactory(user=customer_user)
    CartItemFactory(cart=cart, product=simple_product)
    return cart


@pytest.fixture
def cart_with_expensive_item(db, customer_user, expensive_product, site_settings):
    """Cart with one $150 item (over free shipping threshold)."""
    cart = CartFactory(user=customer_user)
    CartItemFactory(cart=cart, product=expensive_product)
    return cart


# ============================================================
# Vouchers
# ============================================================

@pytest.fixture
def voucher_10pct(db):
    """10% discount voucher code 'SAVE10'."""
    return VoucherFactory(
        code='SAVE10',
        name='Save 10%',
        discount_value=Decimal('10.00'),
    )


# ============================================================
# Factory fixtures (callable factories for parametric tests)
# ============================================================

@pytest.fixture
def user_factory(db):
    """Return UserFactory for creating users in tests."""
    return UserFactory


@pytest.fixture
def product_factory(db):
    """Return ProductFactory for creating products in tests."""
    return ProductFactory


@pytest.fixture
def category_factory(db):
    """Return CategoryFactory for creating categories in tests."""
    return CategoryFactory


@pytest.fixture
def cart_factory(db):
    """Return CartFactory for creating carts in tests."""
    return CartFactory


@pytest.fixture
def warehouse_factory(db):
    """Return WarehouseFactory for creating warehouses in tests."""
    return WarehouseFactory


@pytest.fixture
def order_factory(db):
    """Return OrderFactory for creating orders in tests."""
    return OrderFactory


@pytest.fixture
def media_asset_factory(db):
    """Return MediaAssetFactory for creating media assets in tests."""
    return MediaAssetFactory
