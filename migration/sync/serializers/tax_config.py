"""
Tax Configuration Sync Serializer

Handles export/import of tax-related models:
- TaxPresetGroup: Regional tax preset collections (e.g., EU VAT, US Sales Tax)
- TaxPresetRate: Individual preset rates within groups
- TaxRate: Active merchant-configured tax rates with geographic scope

TaxRate has M2M exempt_categories → Category, resolved silently if not found.
"""

import logging
from decimal import Decimal

from django.db import transaction

from .base import CollectionSyncSerializer

logger = logging.getLogger(__name__)

TAX_PRESET_GROUP_FIELDS = [
    "key",
    "name",
    "description",
    "icon",
    "tax_type",
    "region",
    "is_active",
    "version",
]

TAX_PRESET_RATE_FIELDS = [
    "country",
    "country_name",
    "state",
    "state_name",
    "rate",
    "tax_type",
    "notes",
    "is_active",
]

TAX_RATE_FIELDS = [
    "name",
    "country",
    "state",
    "city",
    "postal_codes",
    "rate",
    "tax_type",
    "applies_to_shipping",
    "compound",
    "exempt_product_types",
    "priority",
    "is_active",
]


class TaxConfigSerializer(CollectionSyncSerializer):
    """Serializer for tax configuration.

    Models handled:
        - TaxPresetGroup: Preset tax rate collections
        - TaxPresetRate: Individual preset rates (nested under groups)
        - TaxRate: Active tax rates with M2M exempt_categories

    Import order: TaxPresetGroup → TaxPresetRate → TaxRate
    """

    category_key = "tax_config"
    natural_key_fields = ["key"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from cart.models import TaxRate

        self.model_class = TaxRate

    def get_count(self):
        from cart.models import TaxPresetGroup, TaxPresetRate, TaxRate

        return (
            TaxPresetGroup.objects.count() + TaxPresetRate.objects.count() + TaxRate.objects.count()
        )

    def export(self, credential_mode="redact"):
        from cart.models import TaxPresetGroup, TaxRate

        items = []

        # TaxPresetGroups with nested rates
        for group in TaxPresetGroup.objects.prefetch_related("rates").all():
            data = {f: getattr(group, f) for f in TAX_PRESET_GROUP_FIELDS}
            data["_model"] = "TaxPresetGroup"
            data["_source_pk"] = group.pk

            # Nested preset rates
            data["_rates"] = []
            for rate in group.rates.all():
                rate_data = {f: getattr(rate, f) for f in TAX_PRESET_RATE_FIELDS}
                if rate_data.get("rate") is not None:
                    rate_data["rate"] = str(rate_data["rate"])
                data["_rates"].append(rate_data)

            items.append(data)

        # Active TaxRates
        for tax in TaxRate.objects.prefetch_related("exempt_categories").all():
            data = {f: getattr(tax, f) for f in TAX_RATE_FIELDS}
            data["_model"] = "TaxRate"
            data["_source_pk"] = tax.pk

            # Decimal
            if data.get("rate") is not None:
                data["rate"] = str(data["rate"])

            # M2M exempt categories as slug list
            data["_exempt_category_slugs"] = list(
                tax.exempt_categories.values_list("slug", flat=True)
            )

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

        # Pass 1: TaxPresetGroups (with nested rates)
        for item in items:
            if item.get("_model") != "TaxPresetGroup":
                continue
            try:
                with transaction.atomic():
                    self._import_preset_group(item)
                    synced += 1
            except Exception as e:
                failed += 1
                errors.append(f"TaxPresetGroup {item.get('key', '?')}: {e}")

        # Pass 2: TaxRates
        for item in items:
            if item.get("_model") != "TaxRate":
                continue
            try:
                with transaction.atomic():
                    self._import_tax_rate(item)
                    synced += 1
            except Exception as e:
                failed += 1
                errors.append(f"TaxRate {item.get('name', '?')}: {e}")

        result = {"synced": synced, "skipped": skipped, "failed": failed, "errors": errors}

        if sync_mode == "mirror":
            deleted = self._delete_absent(items)
            result["deleted"] = deleted

        return result

    def _import_preset_group(self, item):
        from cart.models import TaxPresetGroup, TaxPresetRate

        existing = TaxPresetGroup.objects.filter(key=item["key"]).first()
        group = existing or TaxPresetGroup()

        for f in TAX_PRESET_GROUP_FIELDS:
            if f in item:
                setattr(group, f, item[f])

        group.save()

        # Replace nested rates
        if existing:
            TaxPresetRate.objects.filter(group=group).delete()

        for rate_data in item.get("_rates", []):
            rate = TaxPresetRate(group=group)
            for f in TAX_PRESET_RATE_FIELDS:
                if f in rate_data:
                    val = rate_data[f]
                    if f == "rate" and val is not None:
                        val = Decimal(str(val))
                    setattr(rate, f, val)
            rate.save()

    def _import_tax_rate(self, item):
        from cart.models import TaxRate

        # Match by composite natural key
        existing = TaxRate.objects.filter(
            country=item.get("country", ""),
            state=item.get("state", ""),
            city=item.get("city", ""),
            name=item.get("name", ""),
        ).first()

        tax = existing or TaxRate()

        for f in TAX_RATE_FIELDS:
            if f in item:
                val = item[f]
                if f == "rate" and val is not None:
                    val = Decimal(str(val))
                setattr(tax, f, val)

        tax.save()

        # M2M exempt categories
        cat_slugs = item.get("_exempt_category_slugs", [])
        if cat_slugs:
            from catalog.models import Category

            categories = Category.objects.filter(slug__in=cat_slugs)
            tax.exempt_categories.set(categories)
        else:
            tax.exempt_categories.clear()

    def _delete_absent(self, remote_items):
        from cart.models import TaxPresetGroup, TaxRate

        deleted = 0

        # Delete TaxRates not in remote
        remote_tax_keys = set()
        for item in remote_items:
            if item.get("_model") == "TaxRate":
                remote_tax_keys.add(
                    (
                        item.get("country", ""),
                        item.get("state", ""),
                        item.get("city", ""),
                        item.get("name", ""),
                    )
                )

        for tax in TaxRate.objects.all():
            key = (tax.country, tax.state, tax.city, tax.name)
            if key not in remote_tax_keys:
                try:
                    tax.delete()
                    deleted += 1
                except Exception as e:
                    logger.warning(f"Cannot delete TaxRate {tax.name}: {e}")

        # Delete TaxPresetGroups not in remote (CASCADE deletes rates)
        remote_group_keys = {
            item["key"] for item in remote_items if item.get("_model") == "TaxPresetGroup"
        }
        for group in TaxPresetGroup.objects.all():
            if group.key not in remote_group_keys:
                try:
                    group.delete()
                    deleted += 1
                except Exception as e:
                    logger.warning(f"Cannot delete TaxPresetGroup {group.key}: {e}")

        return deleted

    def generate_diff(self, remote_data):
        from cart.models import TaxPresetGroup, TaxRate

        items = remote_data.get("items", [])
        changes = []

        for item in items:
            model_type = item.get("_model")

            if model_type == "TaxPresetGroup":
                existing = TaxPresetGroup.objects.filter(key=item.get("key")).first()
                compare_fields = TAX_PRESET_GROUP_FIELDS
                name = item.get("key", "?")
            elif model_type == "TaxRate":
                existing = TaxRate.objects.filter(
                    country=item.get("country", ""),
                    state=item.get("state", ""),
                    city=item.get("city", ""),
                    name=item.get("name", ""),
                ).first()
                compare_fields = TAX_RATE_FIELDS
                name = item.get("name", "?")
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
