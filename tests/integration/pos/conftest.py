"""
POS integration test fixtures.

Provides authenticated POS API clients, terminals, shifts, products
with stock, and staff discount configurations.
"""

from decimal import Decimal

import pytest
from django.contrib.auth.models import Group
from rest_framework.test import APIClient

from tests.factories import (
    CategoryFactory,
    MobileAuthTokenFactory,
    POSShiftFactory,
    POSStaffDiscountFactory,
    POSTerminalFactory,
    ProductFactory,
    SalesRegionFactory,
    StockItemFactory,
    UserFactory,
    WarehouseFactory,
)

# ============================================================
# License mock (autouse for all POS tests)
# ============================================================


@pytest.fixture(autouse=True)
def _clear_throttle_cache():
    """Clear DRF throttle cache before every POS test.

    Under --reuse-db the throttle counters persist across runs, which causes
    login endpoints (5/min) to throw 429 on the first live test. Clearing the
    cache guarantees an isolated starting state.
    """
    from django.core.cache import cache

    cache.clear()


@pytest.fixture(autouse=True)
def mock_pos_license(monkeypatch):
    """Bypass POS license check for all POS tests."""
    monkeypatch.setattr("pos_app.license.pos_license_is_valid", lambda: True)


# ============================================================
# Core infrastructure — all POS tests need SiteSettings
# because middleware calls SiteSettings.get_settings()
# ============================================================


@pytest.fixture(autouse=True)
def _ensure_site_settings(site_settings):
    """All POS tests need SiteSettings for currency middleware to function."""


@pytest.fixture
def sales_region(db):
    return SalesRegionFactory(code="POS-REG", name="POS Test Region")


@pytest.fixture
def warehouse(db, sales_region):
    return WarehouseFactory(
        code="POS-WH",
        name="POS Test Warehouse",
        region=sales_region,
        is_retail_location=True,
    )


@pytest.fixture
def category(db):
    return CategoryFactory(name="POS Category", slug="pos-category")


# ============================================================
# Staff users with POS roles
# ============================================================


def _create_pos_role(group_name, display_name, pos_permissions, can_access_pos=True):
    """Helper to create a Django Group + StaffRole with POS access."""
    from staff_roles.models import StaffRole

    group, _ = Group.objects.get_or_create(name=group_name)
    StaffRole.objects.update_or_create(
        group=group,
        defaults={
            "display_name": display_name,
            "can_access_pos": can_access_pos,
            "pos_permissions": pos_permissions,
        },
    )
    return group


@pytest.fixture
def pos_cashier_group(db):
    """Django Group with basic POS cashier permissions."""
    return _create_pos_role(
        "POS Cashiers",
        "POS Cashier",
        {"pos_access": True},
    )


@pytest.fixture
def pos_manager_group(db):
    """Django Group with full POS manager permissions."""
    return _create_pos_role(
        "POS Managers",
        "POS Manager",
        {
            "pos_access": True,
            "pos_refund": True,
            "pos_void": True,
            "pos_stock_adjustment": True,
            "pos_close_shift": True,
            "pos_view_reports": True,
            "pos_cash_management": True,
        },
    )


@pytest.fixture
def pos_staff_user(db, pos_cashier_group):
    """Staff user with basic POS cashier access."""
    user = UserFactory(
        username="pos_cashier",
        email="cashier@pos.test",
        is_staff=True,
        first_name="Test",
        last_name="Cashier",
    )
    user.groups.add(pos_cashier_group)
    return user


@pytest.fixture
def pos_manager_user(db, pos_manager_group):
    """Staff user with full POS manager permissions."""
    user = UserFactory(
        username="pos_manager",
        email="manager@pos.test",
        is_staff=True,
        first_name="Test",
        last_name="Manager",
    )
    user.groups.add(pos_manager_group)
    return user


# ============================================================
# Terminal
# ============================================================


@pytest.fixture
def pos_terminal(db, warehouse):
    """Active POS terminal linked to the test warehouse."""
    return POSTerminalFactory(
        name="Test Register",
        warehouse=warehouse,
    )


# ============================================================
# Auth tokens
# ============================================================


@pytest.fixture
def pos_access_token(db, pos_staff_user, pos_terminal):
    """Access token for the POS cashier user."""
    return MobileAuthTokenFactory(
        user=pos_staff_user,
        token_type="access",
        device_id=f"terminal-{pos_terminal.uuid}",
    )


@pytest.fixture
def pos_refresh_token(db, pos_staff_user, pos_terminal):
    """Refresh token for the POS cashier user."""
    return MobileAuthTokenFactory(
        user=pos_staff_user,
        refresh=True,
        device_id=f"terminal-{pos_terminal.uuid}",
    )


@pytest.fixture
def pos_manager_access_token(db, pos_manager_user, pos_terminal):
    """Access token for the POS manager user."""
    return MobileAuthTokenFactory(
        user=pos_manager_user,
        token_type="access",
        device_id=f"terminal-{pos_terminal.uuid}",
    )


# ============================================================
# API Clients
# ============================================================


@pytest.fixture
def pos_client(pos_access_token, pos_terminal):
    """
    Authenticated POS API client (cashier level).
    Has Bearer token and X-Terminal-UUID headers set.
    """
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {pos_access_token.token}",
        HTTP_X_TERMINAL_UUID=str(pos_terminal.uuid),
    )
    return client


@pytest.fixture
def pos_manager_client(pos_manager_access_token, pos_terminal):
    """
    Authenticated POS API client (manager level).
    Has Bearer token and X-Terminal-UUID headers set.
    """
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {pos_manager_access_token.token}",
        HTTP_X_TERMINAL_UUID=str(pos_terminal.uuid),
    )
    return client


@pytest.fixture
def pos_client_no_terminal(pos_access_token):
    """
    Authenticated POS API client WITHOUT terminal UUID header.
    Useful for testing terminal-required endpoints.
    """
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {pos_access_token.token}",
    )
    return client


@pytest.fixture
def anon_client():
    """Unauthenticated API client for testing auth-required endpoints."""
    return APIClient()


# ============================================================
# Shifts
# ============================================================


@pytest.fixture
def open_shift(db, pos_terminal, pos_staff_user, site_settings):
    """An open POS shift for the cashier on the test terminal."""
    return POSShiftFactory(
        terminal=pos_terminal,
        cashier=pos_staff_user,
        opening_cash=Decimal("100.00"),
    )


@pytest.fixture
def manager_open_shift(db, pos_terminal, pos_manager_user, site_settings):
    """An open POS shift for the manager on the test terminal."""
    return POSShiftFactory(
        terminal=pos_terminal,
        cashier=pos_manager_user,
        opening_cash=Decimal("100.00"),
    )


# ============================================================
# Products with stock
# ============================================================


@pytest.fixture
def product_with_stock(db, category, warehouse, site_settings):
    """A published product with 50 units in the POS warehouse."""
    product = ProductFactory(
        name="Stocked Widget",
        slug="stocked-widget",
        category=category,
        price=Decimal("25.00"),
        track_inventory=True,
    )
    StockItemFactory(product=product, warehouse=warehouse, on_hand=50)
    return product


@pytest.fixture
def product_no_stock(db, category, warehouse, site_settings):
    """A published product with 0 stock in the POS warehouse."""
    product = ProductFactory(
        name="Empty Widget",
        slug="empty-widget",
        category=category,
        price=Decimal("15.00"),
        track_inventory=True,
    )
    StockItemFactory(product=product, warehouse=warehouse, on_hand=0)
    return product


@pytest.fixture
def product_with_barcode(db, category, warehouse, site_settings):
    """A product with a barcode set."""
    product = ProductFactory(
        name="Barcode Widget",
        slug="barcode-widget",
        category=category,
        price=Decimal("19.99"),
        barcode="1234567890123",
        track_inventory=True,
    )
    StockItemFactory(product=product, warehouse=warehouse, on_hand=30)
    return product


@pytest.fixture
def product_no_inventory(db, category, site_settings):
    """A product that doesn't track inventory (always available)."""
    return ProductFactory(
        name="No Track Widget",
        slug="no-track-widget",
        category=category,
        price=Decimal("12.50"),
        track_inventory=False,
    )


# ============================================================
# Discount configurations
# ============================================================


@pytest.fixture
def staff_discount_config(db, pos_staff_user):
    """POSStaffDiscount for the cashier (max 10% discount)."""
    return POSStaffDiscountFactory(
        user=pos_staff_user,
        max_discount_percentage=Decimal("10.00"),
        cashier_pin="1234",
    )


@pytest.fixture
def manager_discount_config(db, pos_manager_user):
    """POSStaffDiscount for the manager (max 50%, is_manager=True)."""
    return POSStaffDiscountFactory(
        user=pos_manager_user,
        manager=True,
        cashier_pin="5678",
    )
