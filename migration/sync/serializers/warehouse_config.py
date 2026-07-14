"""
Warehouse Configuration Sync Serializer

Handles export/import of warehouse-related models:
- SalesRegion: Geographic market regions
- Warehouse: Physical fulfillment locations (with FK to SalesRegion, OneToOne to Location)

Must be imported BEFORE catalog (products) since StockItem depends on Warehouse.
"""

import logging
from decimal import Decimal

from django.db import transaction

from .base import CollectionSyncSerializer

logger = logging.getLogger(__name__)

SALES_REGION_FIELDS = [
    "name",
    "code",
    "countries",
    "default_currency",
    "is_active",
    "priority",
]

WAREHOUSE_FIELDS = [
    "name",
    "code",
    # Address
    "address_line1",
    "address_line2",
    "city",
    "state_province",
    "postal_code",
    "country",
    "latitude",
    "longitude",
    # Settings
    "is_active",
    "fulfillment_priority",
    "stock_buffer_percentage",
    # Display
    "display_name",
    "show_on_frontend",
    # Contact
    "contact_name",
    "contact_email",
    "contact_phone",
    # POS / Retail
    "is_retail_location",
    "pos_display_name",
]


class WarehouseConfigSerializer(CollectionSyncSerializer):
    """Serializer for warehouse configuration.

    Models handled:
        - SalesRegion: Geographic regions with country lists
        - Warehouse: Physical locations with address and settings

    Import order: SalesRegion first (Warehouse.region FK), then Warehouse.
    """

    category_key = "warehouse_config"
    natural_key_fields = ["code"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from catalog.models import SalesRegion

        self.model_class = SalesRegion

    def get_count(self):
        from catalog.models import SalesRegion, Warehouse

        return SalesRegion.objects.count() + Warehouse.objects.count()

    def export(self, credential_mode="redact"):
        from catalog.models import SalesRegion, Warehouse

        items = []

        # SalesRegions
        for region in SalesRegion.objects.all():
            data = {f: getattr(region, f) for f in SALES_REGION_FIELDS}
            data["_model"] = "SalesRegion"
            data["_source_pk"] = region.pk
            items.append(data)

        # Warehouses
        for wh in Warehouse.objects.select_related(
            "region", "shipping_location", "store_group"
        ).all():
            data = {f: getattr(wh, f) for f in WAREHOUSE_FIELDS}
            data["_model"] = "Warehouse"
            data["_source_pk"] = wh.pk

            # Decimal fields
            for df in ["latitude", "longitude"]:
                val = data.get(df)
                if val is not None:
                    data[df] = str(val)

            # FK references (portable)
            data["_region_code"] = wh.region.code if wh.region else None
            data["_shipping_location_code"] = (
                wh.shipping_location.code if wh.shipping_location else None
            )
            data["_store_group_slug"] = wh.store_group.slug if wh.store_group else None

            items.append(data)

        return {
            "category": self.category_key,
            "sync_type": "collection",
            "items": items,
            "total": len(items),
        }

    def import_data(self, data, dry_run=False, sync_mode="additive"):
        if dry_run:
            return self.generate_diff(data)

        items = data.get("items", [])
        synced = 0
        skipped = 0
        failed = 0
        errors = []

        # Pass 1: SalesRegions
        for item in items:
            if item.get("_model") != "SalesRegion":
                continue
            try:
                with transaction.atomic():
                    self._import_sales_region(item)
                    synced += 1
            except Exception as e:
                failed += 1
                errors.append(f"SalesRegion {item.get('code', '?')}: {e}")

        # Pass 2: Warehouses
        for item in items:
            if item.get("_model") != "Warehouse":
                continue
            try:
                with transaction.atomic():
                    self._import_warehouse(item)
                    synced += 1
            except Exception as e:
                failed += 1
                errors.append(f"Warehouse {item.get('code', '?')}: {e}")

        result = {"synced": synced, "skipped": skipped, "failed": failed, "errors": errors}

        if sync_mode == "mirror":
            deleted = self._delete_absent(items)
            result["deleted"] = deleted

        return result

    def _import_sales_region(self, item):
        from catalog.models import SalesRegion

        existing = SalesRegion.objects.filter(code=item["code"]).first()
        region = existing or SalesRegion()

        for f in SALES_REGION_FIELDS:
            if f in item:
                setattr(region, f, item[f])

        region.save()

    def _import_warehouse(self, item):
        from catalog.models import SalesRegion, Warehouse

        existing = Warehouse.objects.filter(code=item["code"]).first()
        wh = existing or Warehouse()

        for f in WAREHOUSE_FIELDS:
            if f in item:
                val = item[f]
                if f in ("latitude", "longitude") and val is not None:
                    val = Decimal(str(val))
                setattr(wh, f, val)

        # Resolve region FK (PROTECT — required)
        region_code = item.get("_region_code")
        if region_code:
            region = SalesRegion.objects.filter(code=region_code).first()
            if region:
                wh.region = region
            else:
                raise ValueError(f"SalesRegion '{region_code}' not found")
        elif not existing:
            raise ValueError("SalesRegion reference required for new Warehouse")

        # Resolve shipping_location (SET_NULL — optional)
        loc_code = item.get("_shipping_location_code")
        if loc_code:
            from shipping.models import Location

            wh.shipping_location = Location.objects.filter(code=loc_code).first()
        else:
            wh.shipping_location = None

        # Resolve store_group (SET_NULL — optional)
        sg_slug = item.get("_store_group_slug")
        if sg_slug:
            from pos_app.models import StoreGroup

            wh.store_group = StoreGroup.objects.filter(slug=sg_slug).first()
        else:
            wh.store_group = None

        wh.save()

    def _delete_absent(self, remote_items):
        from catalog.models import SalesRegion, Warehouse

        deleted = 0

        # Delete warehouses first (FK to SalesRegion is PROTECT)
        remote_wh_codes = {
            item["code"] for item in remote_items if item.get("_model") == "Warehouse"
        }
        for wh in Warehouse.objects.all():
            if wh.code not in remote_wh_codes:
                try:
                    wh.delete()
                    deleted += 1
                except Exception as e:
                    logger.warning(f"Cannot delete warehouse {wh.code}: {e}")

        # Then delete regions
        remote_region_codes = {
            item["code"] for item in remote_items if item.get("_model") == "SalesRegion"
        }
        for region in SalesRegion.objects.all():
            if region.code not in remote_region_codes:
                try:
                    region.delete()
                    deleted += 1
                except Exception as e:
                    logger.warning(f"Cannot delete region {region.code}: {e}")

        return deleted

    def generate_diff(self, remote_data):
        from catalog.models import SalesRegion, Warehouse

        items = remote_data.get("items", [])
        changes = []

        for item in items:
            model_type = item.get("_model")
            if model_type == "SalesRegion":
                existing = SalesRegion.objects.filter(code=item.get("code")).first()
                compare_fields = SALES_REGION_FIELDS
                name = item.get("code", "?")
            elif model_type == "Warehouse":
                existing = Warehouse.objects.filter(code=item.get("code")).first()
                compare_fields = WAREHOUSE_FIELDS
                name = item.get("code", "?")
            else:
                continue

            if existing:
                field_changes = self._compute_field_diff(existing, item, compare_fields)
                if field_changes:
                    changes.append(
                        {
                            "type": "modify",
                            "model": model_type,
                            "name": name,
                            "changes": field_changes,
                        }
                    )
            else:
                changes.append(
                    {
                        "type": "add",
                        "model": model_type,
                        "name": name,
                        "fields": {k: v for k, v in item.items() if not k.startswith("_")},
                    }
                )

        adds = sum(1 for c in changes if c["type"] == "add")
        mods = sum(1 for c in changes if c["type"] == "modify")
        parts = []
        if adds:
            parts.append(f"{adds} addition(s)")
        if mods:
            parts.append(f"{mods} modification(s)")

        return {
            "changes": changes,
            "warnings": [],
            "summary": ", ".join(parts) if parts else "No changes",
        }

    def snapshot_current(self):
        return self.export(credential_mode="skip")

    def restore_snapshot(self, snapshot):
        try:
            result = self.import_data(snapshot, dry_run=False)
            return {"restored": result.get("synced", 0), "errors": result.get("errors", [])}
        except Exception as e:
            return {"restored": 0, "errors": [str(e)]}
