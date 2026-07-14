"""
POS scenario builders.

Each function creates a complete POS environment for testing.
Returns a dict with all created objects for assertions.

Usage in tests:
    from tests.fixtures.pos_scenarios import basic_pos_store

    @pytest.fixture
    def store(db, site_settings):
        return basic_pos_store()
"""

from decimal import Decimal

from tests.factories import (
    CategoryFactory,
    POSStaffDiscountFactory,
    POSTerminalFactory,
    ProductFactory,
    SalesRegionFactory,
    StockItemFactory,
    StoreGroupFactory,
    UserFactory,
    WarehouseFactory,
)


def basic_pos_store():
    """
    A single-terminal store with 3 products stocked.

    Returns dict with: region, warehouse, terminal, products (list),
    stock_items (list), category.
    """
    region = SalesRegionFactory(code="POS-DEFAULT", name="POS Test Region")
    warehouse = WarehouseFactory(
        code="POS-WH-01",
        name="POS Test Store",
        region=region,
        is_retail_location=True,
    )
    terminal = POSTerminalFactory(
        name="Register 1",
        warehouse=warehouse,
    )

    category = CategoryFactory(name="POS Products", slug="pos-products")
    products = []
    stock_items = []
    for _i, (name, price) in enumerate(
        [
            ("Widget A", Decimal("10.00")),
            ("Widget B", Decimal("25.00")),
            ("Widget C", Decimal("99.99")),
        ]
    ):
        p = ProductFactory(
            name=name,
            slug=f"pos-{name.lower().replace(' ', '-')}",
            category=category,
            price=price,
            track_inventory=True,
        )
        si = StockItemFactory(product=p, warehouse=warehouse, on_hand=50)
        products.append(p)
        stock_items.append(si)

    return {
        "region": region,
        "warehouse": warehouse,
        "terminal": terminal,
        "category": category,
        "products": products,
        "stock_items": stock_items,
    }


def multi_terminal_store():
    """
    Two terminals in separate warehouses.

    Returns dict with: region, warehouses (list), terminals (list),
    store_group.
    """
    group = StoreGroupFactory(name="Test Group", code="TST-GRP")
    region = SalesRegionFactory(code="POS-MULTI", name="Multi Terminal Region")

    wh1 = WarehouseFactory(
        code="POS-WH-A",
        name="Store A",
        region=region,
        is_retail_location=True,
        store_group=group,
    )
    wh2 = WarehouseFactory(
        code="POS-WH-B",
        name="Store B",
        region=region,
        is_retail_location=True,
        store_group=group,
    )

    t1 = POSTerminalFactory(name="Store A Register", warehouse=wh1)
    t2 = POSTerminalFactory(name="Store B Register", warehouse=wh2)

    return {
        "region": region,
        "store_group": group,
        "warehouses": [wh1, wh2],
        "terminals": [t1, t2],
    }


def manager_cashier_team():
    """
    A manager and cashier with POS staff roles set up.

    Returns dict with: manager (User), cashier (User),
    manager_discount (POSStaffDiscount), cashier_discount (POSStaffDiscount),
    manager_group (Group), cashier_group (Group).
    """
    from django.contrib.auth.models import Group

    from staff_roles.models import StaffRole

    manager = UserFactory(
        username="pos_manager",
        email="manager@pos.test",
        is_staff=True,
        first_name="Manager",
        last_name="Test",
    )
    cashier = UserFactory(
        username="pos_cashier",
        email="cashier@pos.test",
        is_staff=True,
        first_name="Cashier",
        last_name="Test",
    )

    # Create groups + staff roles for POS access
    mgr_group, _ = Group.objects.get_or_create(name="POS Managers")
    csh_group, _ = Group.objects.get_or_create(name="POS Cashiers")

    StaffRole.objects.get_or_create(
        group=mgr_group,
        defaults={
            "display_name": "POS Manager",
            "can_access_pos": True,
            "pos_permissions": {
                "pos_access": True,
                "pos_refund": True,
                "pos_void": True,
                "pos_stock_adjustment": True,
                "pos_close_shift": True,
                "pos_view_reports": True,
                "pos_manage_cash": True,
            },
        },
    )
    StaffRole.objects.get_or_create(
        group=csh_group,
        defaults={
            "display_name": "POS Cashier",
            "can_access_pos": True,
            "pos_permissions": {
                "pos_access": True,
            },
        },
    )

    manager.groups.add(mgr_group)
    cashier.groups.add(csh_group)

    manager_discount = POSStaffDiscountFactory(
        user=manager,
        manager=True,
        cashier_pin="5678",
    )
    cashier_discount = POSStaffDiscountFactory(
        user=cashier,
        cashier_pin="1234",
    )

    return {
        "manager": manager,
        "cashier": cashier,
        "manager_discount": manager_discount,
        "cashier_discount": cashier_discount,
        "manager_group": mgr_group,
        "cashier_group": csh_group,
    }
