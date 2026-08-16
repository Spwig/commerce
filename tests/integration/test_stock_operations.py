"""
Stock operations service tests.

Covers the execution paths behind the previously declared-only StockMovement
types: transfer, damage, recount — happy paths plus edge/negative cases and
idempotency.
"""

import pytest

from catalog.models import StockItem, StockMovement
from catalog.services.stock_operations import (
    InsufficientStockError,
    StockOperationError,
    record_damage,
    recount_stock,
    transfer_stock,
)
from tests.factories import ProductFactory, StockItemFactory, WarehouseFactory

pytestmark = [pytest.mark.django_db, pytest.mark.integration]


@pytest.fixture
def site_settings(db):
    """SiteSettings required for single-tenant money defaults."""
    from core.models import SiteSettings

    settings, _ = SiteSettings.objects.get_or_create(
        pk=1,
        defaults={
            "site_name": "Test Store",
            "admin_email": "admin@test.spwig.com",
            "default_currency": "USD",
            "default_language": "en",
        },
    )
    return settings


@pytest.fixture
def two_warehouses(db):
    return (
        WarehouseFactory(code="WH-SRC", name="Source WH"),
        WarehouseFactory(code="WH-DST", name="Dest WH"),
    )


# ============================================================
# transfer_stock
# ============================================================


class TestTransferStock:
    def test_transfer_moves_on_hand_between_warehouses(self, site_settings, two_warehouses):
        src_wh, dst_wh = two_warehouses
        product = ProductFactory(track_inventory=True)
        src = StockItemFactory(product=product, warehouse=src_wh, on_hand=50, allocated=0)
        dst = StockItemFactory(product=product, warehouse=dst_wh, on_hand=10, allocated=0)

        transfer_stock(product, src_wh, dst_wh, 20)

        src.refresh_from_db()
        dst.refresh_from_db()
        assert src.on_hand == 30
        assert dst.on_hand == 30

    def test_transfer_creates_paired_movements(self, site_settings, two_warehouses):
        src_wh, dst_wh = two_warehouses
        product = ProductFactory(track_inventory=True)
        StockItemFactory(product=product, warehouse=src_wh, on_hand=50)
        StockItemFactory(product=product, warehouse=dst_wh, on_hand=0)

        result = transfer_stock(product, src_wh, dst_wh, 15)

        movements = result["movements"]
        assert len(movements) == 2
        deltas = sorted(m.quantity for m in movements)
        assert deltas == [-15, 15]
        assert all(m.movement_type == "transfer" for m in movements)

    def test_transfer_creates_destination_stock_item_when_absent(
        self, site_settings, two_warehouses
    ):
        src_wh, dst_wh = two_warehouses
        product = ProductFactory(track_inventory=True)
        StockItemFactory(product=product, warehouse=src_wh, on_hand=40)
        assert not StockItem.objects.filter(product=product, warehouse=dst_wh).exists()

        transfer_stock(product, src_wh, dst_wh, 10)

        dst = StockItem.objects.get(product=product, warehouse=dst_wh)
        assert dst.on_hand == 10

    def test_transfer_rejects_more_than_available(self, site_settings, two_warehouses):
        """Allocated units cannot be transferred — only available stock can."""
        src_wh, dst_wh = two_warehouses
        product = ProductFactory(track_inventory=True)
        StockItemFactory(product=product, warehouse=src_wh, on_hand=30, allocated=25)
        StockItemFactory(product=product, warehouse=dst_wh, on_hand=0)

        with pytest.raises(InsufficientStockError):
            transfer_stock(product, src_wh, dst_wh, 10)  # only 5 available

    def test_transfer_rejects_same_warehouse(self, site_settings, two_warehouses):
        src_wh, _ = two_warehouses
        product = ProductFactory(track_inventory=True)
        StockItemFactory(product=product, warehouse=src_wh, on_hand=30)

        with pytest.raises(StockOperationError):
            transfer_stock(product, src_wh, src_wh, 5)

    def test_transfer_rejects_nonpositive_quantity(self, site_settings, two_warehouses):
        src_wh, dst_wh = two_warehouses
        product = ProductFactory(track_inventory=True)
        StockItemFactory(product=product, warehouse=src_wh, on_hand=30)

        with pytest.raises(StockOperationError):
            transfer_stock(product, src_wh, dst_wh, 0)

    def test_transfer_missing_source_raises(self, site_settings, two_warehouses):
        src_wh, dst_wh = two_warehouses
        product = ProductFactory(track_inventory=True)  # no stock item at source

        with pytest.raises(InsufficientStockError):
            transfer_stock(product, src_wh, dst_wh, 5)

    def test_transfer_is_idempotent_on_reference_key(self, site_settings, two_warehouses):
        src_wh, dst_wh = two_warehouses
        product = ProductFactory(track_inventory=True)
        src = StockItemFactory(product=product, warehouse=src_wh, on_hand=50)
        StockItemFactory(product=product, warehouse=dst_wh, on_hand=0)

        transfer_stock(product, src_wh, dst_wh, 10, reference_key="txn-abc")
        transfer_stock(product, src_wh, dst_wh, 10, reference_key="txn-abc")  # retry

        src.refresh_from_db()
        assert src.on_hand == 40  # applied once, not twice


# ============================================================
# record_damage
# ============================================================


class TestRecordDamage:
    def test_damage_decrements_on_hand_and_logs_movement(self, site_settings):
        item = StockItemFactory(on_hand=20, allocated=0)

        mv = record_damage(item, 5, reason="Water damage")

        item.refresh_from_db()
        assert item.on_hand == 15
        assert mv.movement_type == "damage"
        assert mv.quantity == -5

    def test_damage_cannot_write_off_allocated_units(self, site_settings):
        item = StockItemFactory(on_hand=10, allocated=8)  # only 2 unreserved

        with pytest.raises(InsufficientStockError):
            record_damage(item, 5)

    def test_damage_rejects_nonpositive(self, site_settings):
        item = StockItemFactory(on_hand=10)

        with pytest.raises(StockOperationError):
            record_damage(item, 0)

    def test_damage_is_idempotent_on_reference_key(self, site_settings):
        item = StockItemFactory(on_hand=20)

        record_damage(item, 5, reference_key="dmg-1")
        record_damage(item, 5, reference_key="dmg-1")

        item.refresh_from_db()
        assert item.on_hand == 15
        assert StockMovement.objects.filter(reference_key="dmg-1").count() == 1


# ============================================================
# recount_stock
# ============================================================


class TestRecountStock:
    def test_recount_increase_sets_on_hand_and_positive_delta(self, site_settings):
        item = StockItemFactory(on_hand=10)

        mv = recount_stock(item, 18)

        item.refresh_from_db()
        assert item.on_hand == 18
        assert mv.movement_type == "recount"
        assert mv.quantity == 8

    def test_recount_decrease_records_negative_delta(self, site_settings):
        item = StockItemFactory(on_hand=10)

        mv = recount_stock(item, 4)

        item.refresh_from_db()
        assert item.on_hand == 4
        assert mv.quantity == -6

    def test_recount_below_allocated_is_allowed(self, site_settings):
        """A physical shortage below allocated must still be recordable."""
        item = StockItemFactory(on_hand=10, allocated=8)

        recount_stock(item, 3)

        item.refresh_from_db()
        assert item.on_hand == 3

    def test_recount_rejects_negative(self, site_settings):
        item = StockItemFactory(on_hand=10)

        with pytest.raises(StockOperationError):
            recount_stock(item, -1)

    def test_recount_is_idempotent_on_reference_key(self, site_settings):
        item = StockItemFactory(on_hand=10)

        recount_stock(item, 25, reference_key="rc-1")
        recount_stock(item, 25, reference_key="rc-1")

        assert StockMovement.objects.filter(reference_key="rc-1").count() == 1


# ============================================================
# Admin actions (surface the operations to merchants)
# ============================================================


class TestStockAdminActions:
    """Verify the StockItem admin actions render and re-dispatch correctly."""

    @pytest.fixture
    def staff_client(self, db):
        from django.test import Client

        from tests.factories import UserFactory

        user = UserFactory(staff=True, username="stock_admin")
        client = Client()
        client.force_login(user)
        return client

    def _changelist_url(self):
        from django.urls import reverse

        return reverse("admin:catalog_stockitem_changelist")

    def test_transfer_action_renders_intermediate_page(
        self, staff_client, site_settings, two_warehouses
    ):
        """Selecting the transfer action returns the confirmation page (no
        TemplateSyntaxError)."""
        src_wh, dst_wh = two_warehouses
        product = ProductFactory(track_inventory=True)
        item = StockItemFactory(product=product, warehouse=src_wh, on_hand=40)

        response = staff_client.post(
            self._changelist_url(),
            {"action": "transfer_stock_action", "_selected_action": [item.pk]},
        )
        assert response.status_code == 200
        assert b"Transfer Stock" in response.content

    def test_transfer_action_applies_and_moves_stock(
        self, staff_client, site_settings, two_warehouses
    ):
        """Submitting the confirmation form re-dispatches the action and moves
        stock (regression for the missing hidden 'action' field)."""
        src_wh, dst_wh = two_warehouses
        product = ProductFactory(track_inventory=True)
        src = StockItemFactory(product=product, warehouse=src_wh, on_hand=40)

        response = staff_client.post(
            self._changelist_url(),
            {
                "action": "transfer_stock_action",
                "_selected_action": [src.pk],
                "apply": "1",
                "destination": dst_wh.pk,
                "quantity": 12,
                "reason": "Rebalance",
            },
            follow=True,
        )
        assert response.status_code == 200
        src.refresh_from_db()
        assert src.on_hand == 28
        dst = StockItem.objects.get(product=product, warehouse=dst_wh)
        assert dst.on_hand == 12
        assert StockMovement.objects.filter(movement_type="transfer").count() == 2

    def test_damage_action_applies(self, staff_client, site_settings):
        item = StockItemFactory(on_hand=30, allocated=0)
        response = staff_client.post(
            self._changelist_url(),
            {
                "action": "record_damage_action",
                "_selected_action": [item.pk],
                "apply": "1",
                "quantity": 7,
                "reason": "Breakage",
            },
            follow=True,
        )
        assert response.status_code == 200
        item.refresh_from_db()
        assert item.on_hand == 23
        assert StockMovement.objects.filter(movement_type="damage").count() == 1

    def test_recount_action_applies(self, staff_client, site_settings):
        item = StockItemFactory(on_hand=30)
        response = staff_client.post(
            self._changelist_url(),
            {
                "action": "recount_stock_action",
                "_selected_action": [item.pk],
                "apply": "1",
                "counted_quantity": 27,
                "reason": "Cycle count",
            },
            follow=True,
        )
        assert response.status_code == 200
        item.refresh_from_db()
        assert item.on_hand == 27
        assert StockMovement.objects.filter(movement_type="recount").count() == 1
