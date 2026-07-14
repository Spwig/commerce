"""
License Keys Sync Serializer

Handles export/import of software license keys:
- LicenseKey (with nested LicenseActivation)
"""

import logging

from django.db import transaction

from .base import CollectionSyncSerializer

logger = logging.getLogger(__name__)

LICENSE_KEY_FIELDS = [
    "key",
    "key_type",
    "max_activations",
    "current_activations",
    "status",
    "is_lifetime",
    "notes",
]

ACTIVATION_FIELDS = [
    "device_identifier",
    "device_name",
    "device_info",
    "is_active",
    "ip_address",
    "location",
]


class LicenseKeysSerializer(CollectionSyncSerializer):
    category_key = "license_keys"
    natural_key_fields = ["key"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from catalog.models import LicenseKey

        self.model_class = LicenseKey

    def get_count(self):
        from catalog.models import LicenseActivation, LicenseKey

        return LicenseKey.objects.count() + LicenseActivation.objects.count()

    def export(self, credential_mode="redact"):
        from catalog.models import LicenseKey

        items = []
        for lk in (
            LicenseKey.objects.select_related(
                "license_pool",
                "license_pool__license_template",
                "digital_asset",
                "digital_asset__product",
                "order_item",
                "order_item__order",
                "user",
            )
            .prefetch_related("activations")
            .all()
        ):
            data = {f: getattr(lk, f) for f in LICENSE_KEY_FIELDS}
            data["_source_pk"] = lk.pk
            data["_model"] = "LicenseKey"

            # Portable FK references
            data["_user_email"] = lk.user.email if lk.user else None
            data["_order_number"] = (
                lk.order_item.order.order_number if lk.order_item and lk.order_item.order else None
            )
            data["_order_item_sku"] = lk.order_item.sku if lk.order_item else None
            data["_digital_asset_product_sku"] = (
                lk.digital_asset.product.sku
                if lk.digital_asset and lk.digital_asset.product
                else None
            )
            data["_digital_asset_filename"] = (
                lk.digital_asset.filename if lk.digital_asset else None
            )
            data["_license_pool_template_name"] = (
                lk.license_pool.license_template.name
                if lk.license_pool and lk.license_pool.license_template
                else None
            )

            # Datetime fields
            for dt in ["expires_at", "issued_at", "first_activated_at", "last_activated_at"]:
                val = getattr(lk, dt, None)
                if val and hasattr(val, "isoformat"):
                    data[f"_{dt}"] = val.isoformat()

            # Nested activations
            data["_activations"] = []
            for act in lk.activations.all().order_by("activated_at"):
                a_data = {f: getattr(act, f) for f in ACTIVATION_FIELDS}
                if act.activated_at:
                    a_data["_activated_at"] = act.activated_at.isoformat()
                if act.deactivated_at:
                    a_data["_deactivated_at"] = act.deactivated_at.isoformat()
                data["_activations"].append(a_data)

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
                    self._import_license_key(item)
                    synced += 1
            except Exception as e:
                failed += 1
                errors.append(f"LicenseKey '{item.get('key', '?')}': {e}")

        return {"synced": synced, "skipped": skipped, "failed": failed, "errors": errors}

    def _import_license_key(self, item):
        from django.contrib.auth import get_user_model
        from django.utils.dateparse import parse_datetime

        from catalog.models import (
            DigitalAsset,
            LicenseActivation,
            LicenseKey,
            LicenseKeyTemplate,
            LicensePool,
            Product,
        )
        from orders.models import Order, OrderItem

        User = get_user_model()

        existing = LicenseKey.objects.filter(key=item["key"]).first()
        lk = existing or LicenseKey()

        for f in LICENSE_KEY_FIELDS:
            if f in item:
                setattr(lk, f, item[f])

        # Resolve user
        user_email = item.get("_user_email")
        if user_email:
            lk.user = User.objects.filter(email=user_email).first()

        # Resolve order item
        order_number = item.get("_order_number")
        order_item_sku = item.get("_order_item_sku")
        if order_number and order_item_sku:
            order = Order.objects.filter(order_number=order_number).first()
            if order:
                lk.order_item = OrderItem.objects.filter(
                    order=order,
                    sku=order_item_sku,
                ).first()

        # Resolve digital asset
        da_product_sku = item.get("_digital_asset_product_sku")
        da_filename = item.get("_digital_asset_filename")
        if da_product_sku and da_filename:
            product = Product.objects.filter(sku=da_product_sku).first()
            if product:
                lk.digital_asset = DigitalAsset.objects.filter(
                    product=product,
                    filename=da_filename,
                ).first()

        # Resolve license pool
        pool_template_name = item.get("_license_pool_template_name")
        if pool_template_name and lk.digital_asset:
            template = LicenseKeyTemplate.objects.filter(name=pool_template_name).first()
            if template:
                lk.license_pool = LicensePool.objects.filter(
                    product=lk.digital_asset.product,
                    template=template,
                ).first()

        # Datetime fields
        for dt in ["expires_at", "first_activated_at", "last_activated_at"]:
            val = item.get(f"_{dt}")
            if val:
                parsed = parse_datetime(val)
                if parsed:
                    setattr(lk, dt, parsed)

        lk.save()

        # Activations
        for a_data in item.get("_activations", []):
            device_id = a_data.get("device_identifier")
            if not device_id:
                continue

            act, created = LicenseActivation.objects.get_or_create(
                license_key=lk,
                device_identifier=device_id,
            )
            for f in ACTIVATION_FIELDS:
                if f in a_data and f != "device_identifier":
                    setattr(act, f, a_data[f])

            deactivated = a_data.get("_deactivated_at")
            if deactivated:
                act.deactivated_at = parse_datetime(deactivated)

            act.save()

    def generate_diff(self, remote_data):
        from catalog.models import LicenseKey

        items = remote_data.get("items", [])
        changes = []

        for item in items:
            existing = LicenseKey.objects.filter(key=item.get("key")).first()
            if existing:
                field_changes = self._compute_field_diff(existing, item, LICENSE_KEY_FIELDS)
                if field_changes:
                    changes.append(
                        {
                            "type": "modify",
                            "model": "LicenseKey",
                            "name": item.get("key", "?"),
                            "changes": field_changes,
                        }
                    )
            else:
                changes.append(
                    {
                        "type": "add",
                        "model": "LicenseKey",
                        "name": item.get("key", "?"),
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
