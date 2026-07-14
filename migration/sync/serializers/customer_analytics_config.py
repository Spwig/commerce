"""
Customer Analytics Configuration Sync Serializer

Handles export/import of analytics configuration models:
- CustomerSegment (with MoneyFields)
- LTVSettings (singleton)
- ProductCategoryLTVMultiplier
"""

import logging
from decimal import Decimal

from django.db import transaction

from .base import CollectionSyncSerializer

logger = logging.getLogger(__name__)

CUSTOMER_SEGMENT_FIELDS = [
    "name",
    "display_name",
    "description",
    "min_orders",
    "max_orders",
    "min_days_since_last_purchase",
    "max_days_since_last_purchase",
    "color",
    "priority",
    "is_active",
]

# MoneyFields on CustomerSegment
SEGMENT_MONEY_FIELDS = ["min_total_spent", "max_total_spent"]

LTV_SETTINGS_FIELDS = [
    "calculation_method",
    "default_discount_rate",
    "min_data_quality_threshold",
]

LTV_MULTIPLIER_FIELDS = [
    "category_name",
    "repeat_purchase_multiplier",
    "notes",
    "is_active",
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
    else:
        setattr(instance, field_name, None)
    if currency:
        setattr(instance, f"{field_name}_currency", currency)


class CustomerAnalyticsConfigSerializer(CollectionSyncSerializer):
    """Serializer for customer analytics configuration.

    Models handled:
        - CustomerSegment: Customer segmentation definitions
        - LTVSettings: Lifetime value calculation settings (singleton)
        - ProductCategoryLTVMultiplier: Category-based LTV adjustments
    """

    category_key = "customer_analytics_config"
    natural_key_fields = ["name"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from customers.models import CustomerSegment

        self.model_class = CustomerSegment

    def get_count(self):
        from customers.models import CustomerSegment, LTVSettings, ProductCategoryLTVMultiplier

        return (
            CustomerSegment.objects.count()
            + LTVSettings.objects.count()
            + ProductCategoryLTVMultiplier.objects.count()
        )

    def export(self, credential_mode="redact"):
        from customers.models import CustomerSegment, LTVSettings, ProductCategoryLTVMultiplier

        items = []

        # LTVSettings (singleton)
        ltv = LTVSettings.objects.first()
        if ltv:
            data = {f: getattr(ltv, f) for f in LTV_SETTINGS_FIELDS}
            data["_source_pk"] = ltv.pk
            data["_model"] = "LTVSettings"
            if data.get("default_discount_rate") is not None:
                data["default_discount_rate"] = str(data["default_discount_rate"])
            items.append(data)

        # CustomerSegments
        for seg in CustomerSegment.objects.all().order_by("priority"):
            data = {f: getattr(seg, f) for f in CUSTOMER_SEGMENT_FIELDS}
            data["_source_pk"] = seg.pk
            data["_model"] = "CustomerSegment"
            for mf in SEGMENT_MONEY_FIELDS:
                _serialize_money(data, seg, mf)
            items.append(data)

        # ProductCategoryLTVMultiplier
        for mult in ProductCategoryLTVMultiplier.objects.all():
            data = {f: getattr(mult, f) for f in LTV_MULTIPLIER_FIELDS}
            data["_source_pk"] = mult.pk
            data["_model"] = "ProductCategoryLTVMultiplier"
            if data.get("repeat_purchase_multiplier") is not None:
                data["repeat_purchase_multiplier"] = str(data["repeat_purchase_multiplier"])
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
            model_type = item.get("_model")
            try:
                with transaction.atomic():
                    if model_type == "LTVSettings":
                        self._import_ltv_settings(item)
                    elif model_type == "CustomerSegment":
                        self._import_segment(item)
                    elif model_type == "ProductCategoryLTVMultiplier":
                        self._import_multiplier(item)
                    else:
                        skipped += 1
                        continue
                    synced += 1
            except Exception as e:
                failed += 1
                errors.append(
                    f"{model_type} '{item.get('name', item.get('category_name', '?'))}': {e}"
                )

        result = {"synced": synced, "skipped": skipped, "failed": failed, "errors": errors}

        if sync_mode == "mirror":
            deleted = self._delete_absent(items)
            result["deleted"] = deleted

        return result

    def _import_ltv_settings(self, item):
        from customers.models import LTVSettings

        obj = LTVSettings.objects.first() or LTVSettings()
        for f in LTV_SETTINGS_FIELDS:
            if f in item:
                val = item[f]
                if f == "default_discount_rate" and val is not None:
                    val = Decimal(str(val))
                setattr(obj, f, val)
        obj.save()

    def _import_segment(self, item):
        from customers.models import CustomerSegment

        existing = CustomerSegment.objects.filter(name=item["name"]).first()
        obj = existing or CustomerSegment()
        for f in CUSTOMER_SEGMENT_FIELDS:
            if f in item:
                setattr(obj, f, item[f])
        for mf in SEGMENT_MONEY_FIELDS:
            _deserialize_money(obj, item, mf)
        obj.save()

    def _import_multiplier(self, item):
        from customers.models import ProductCategoryLTVMultiplier

        existing = ProductCategoryLTVMultiplier.objects.filter(
            category_name=item["category_name"],
        ).first()
        obj = existing or ProductCategoryLTVMultiplier()
        for f in LTV_MULTIPLIER_FIELDS:
            if f in item:
                val = item[f]
                if f == "repeat_purchase_multiplier" and val is not None:
                    val = Decimal(str(val))
                setattr(obj, f, val)
        obj.save()

    def _delete_absent(self, remote_items):
        from customers.models import CustomerSegment, ProductCategoryLTVMultiplier

        remote_seg_names = {
            item["name"] for item in remote_items if item.get("_model") == "CustomerSegment"
        }
        remote_mult_names = {
            item["category_name"]
            for item in remote_items
            if item.get("_model") == "ProductCategoryLTVMultiplier"
        }
        deleted = 0
        for seg in CustomerSegment.objects.all():
            if seg.name not in remote_seg_names:
                try:
                    seg.delete()
                    deleted += 1
                except Exception as e:
                    logger.warning(f"Cannot delete CustomerSegment '{seg.name}': {e}")
        for mult in ProductCategoryLTVMultiplier.objects.all():
            if mult.category_name not in remote_mult_names:
                try:
                    mult.delete()
                    deleted += 1
                except Exception as e:
                    logger.warning(f"Cannot delete LTVMultiplier '{mult.category_name}': {e}")
        return deleted

    def generate_diff(self, remote_data):
        from customers.models import CustomerSegment, LTVSettings, ProductCategoryLTVMultiplier

        items = remote_data.get("items", [])
        changes = []

        for item in items:
            model_type = item.get("_model")
            if model_type == "LTVSettings":
                existing = LTVSettings.objects.first()
                fields = LTV_SETTINGS_FIELDS
                name = "LTV Settings"
            elif model_type == "CustomerSegment":
                existing = CustomerSegment.objects.filter(name=item.get("name")).first()
                fields = CUSTOMER_SEGMENT_FIELDS
                name = item.get("name", "?")
            elif model_type == "ProductCategoryLTVMultiplier":
                existing = ProductCategoryLTVMultiplier.objects.filter(
                    category_name=item.get("category_name"),
                ).first()
                fields = LTV_MULTIPLIER_FIELDS
                name = item.get("category_name", "?")
            else:
                continue

            if existing:
                field_changes = self._compute_field_diff(existing, item, fields)
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
