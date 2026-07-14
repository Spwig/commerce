"""
Shipments & Tracking Sync Serializer

Handles export/import of shipment records:
- Shipment (with MoneyFields, nested TrackingEvent)
"""

import logging
from decimal import Decimal

from django.db import transaction

from .base import CollectionSyncSerializer

logger = logging.getLogger(__name__)

SHIPMENT_FIELDS = [
    "origin_country",
    "dest_country",
    "packages",
    "service_level",
    "pricing_mode_used",
    "tracking_id",
    "label_url",
    "packing_slip_url",
    "commercial_invoice_url",
    "customs_form_url",
    "status",
    "provider_reference",
    "provider_meta",
    "audit_log",
]

SHIPMENT_MONEY_FIELDS = ["shipping_cost", "carrier_cost"]

TRACKING_EVENT_FIELDS = [
    "status",
    "description",
    "location",
    "raw",
]


def _serialize_money(data, instance, field_name):
    val = getattr(instance, field_name, None)
    if val is not None:
        data[f"_{field_name}_amount"] = str(val.amount) if hasattr(val, "amount") else str(val)
        data[f"_{field_name}_currency"] = (
            str(val.currency)
            if hasattr(val, "currency")
            else getattr(instance, f"{field_name}_currency", None)
        )
    else:
        data[f"_{field_name}_amount"] = None
        data[f"_{field_name}_currency"] = None


def _deserialize_money(instance, item, field_name):
    amount = item.get(f"_{field_name}_amount")
    currency = item.get(f"_{field_name}_currency")
    if amount is not None:
        setattr(instance, field_name, Decimal(str(amount)))
    if currency:
        setattr(instance, f"{field_name}_currency", currency)


class ShipmentsSerializer(CollectionSyncSerializer):
    category_key = "shipments"
    natural_key_fields = ["tracking_id"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from shipping.models import Shipment

        self.model_class = Shipment

    def get_count(self):
        from shipping.models import Shipment, TrackingEvent

        return Shipment.objects.count() + TrackingEvent.objects.count()

    def export(self, credential_mode="redact"):
        from shipping.models import Shipment

        items = []
        for ship in (
            Shipment.objects.select_related(
                "order",
                "carrier_preset",
                "provider_account",
            )
            .prefetch_related("tracking_events")
            .all()
        ):
            data = {f: getattr(ship, f) for f in SHIPMENT_FIELDS}
            data["_source_pk"] = str(ship.pk)
            data["_model"] = "Shipment"

            for mf in SHIPMENT_MONEY_FIELDS:
                _serialize_money(data, ship, mf)

            data["_order_number"] = ship.order.order_number if ship.order else None
            data["_carrier_slug"] = ship.carrier_preset.slug if ship.carrier_preset else None

            if ship.created_at:
                data["_created_at"] = ship.created_at.isoformat()

            # Nested tracking events
            data["_events"] = []
            for evt in ship.tracking_events.all().order_by("occurred_at"):
                e_data = {f: getattr(evt, f) for f in TRACKING_EVENT_FIELDS}
                if evt.occurred_at:
                    e_data["_occurred_at"] = evt.occurred_at.isoformat()
                data["_events"].append(e_data)

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

        for item in items:
            try:
                with transaction.atomic():
                    self._import_shipment(item)
                    synced += 1
            except Exception as e:
                failed += 1
                errors.append(f"Shipment '{item.get('tracking_id', '?')}': {e}")

        return {"synced": synced, "skipped": skipped, "failed": failed, "errors": errors}

    def _import_shipment(self, item):
        from django.utils.dateparse import parse_datetime

        from orders.models import Order
        from shipping.models import CarrierPreset, Shipment, TrackingEvent

        existing = Shipment.objects.filter(tracking_id=item.get("tracking_id", "")).first()
        ship = existing or Shipment()

        for f in SHIPMENT_FIELDS:
            if f in item:
                setattr(ship, f, item[f])

        for mf in SHIPMENT_MONEY_FIELDS:
            _deserialize_money(ship, item, mf)

        order_num = item.get("_order_number")
        if order_num:
            ship.order = Order.objects.filter(order_number=order_num).first()
            if ship.order:
                ship.user = ship.order.user

        carrier_slug = item.get("_carrier_slug")
        if carrier_slug:
            ship.carrier_preset = CarrierPreset.objects.filter(slug=carrier_slug).first()

        ship.save()

        # Replace tracking events
        if existing:
            ship.tracking_events.all().delete()

        for e_data in item.get("_events", []):
            evt = TrackingEvent(shipment=ship)
            for f in TRACKING_EVENT_FIELDS:
                if f in e_data:
                    setattr(evt, f, e_data[f])
            occurred = e_data.get("_occurred_at")
            if occurred:
                parsed = parse_datetime(occurred)
                if parsed:
                    evt.occurred_at = parsed
            evt.save()

    def generate_diff(self, remote_data):
        from shipping.models import Shipment

        items = remote_data.get("items", [])
        changes = []

        for item in items:
            existing = Shipment.objects.filter(tracking_id=item.get("tracking_id", "")).first()
            name = item.get("tracking_id", "?")
            if existing:
                field_changes = self._compute_field_diff(existing, item, SHIPMENT_FIELDS)
                if field_changes:
                    changes.append(
                        {
                            "type": "modify",
                            "model": "Shipment",
                            "name": name,
                            "changes": field_changes,
                        }
                    )
            else:
                changes.append({"type": "add", "model": "Shipment", "name": name, "fields": {}})

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
