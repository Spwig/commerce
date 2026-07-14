"""
Digital Products & Licenses Sync Serializer

Handles export/import of digital product assets:
- DigitalAsset (with file transfer)
- LicenseKeyTemplate
- LicensePool
- LicenseProvider (with credentials)
"""

import logging

from django.db import transaction

from ..credential_handler import redact_credentials
from ..file_handler import export_file_field, import_file_field
from .base import CollectionSyncSerializer

logger = logging.getLogger(__name__)

DIGITAL_ASSET_FIELDS = [
    "filename",
    "file_size",
    "file_type",
    "file_hash",
    "version",
    "changelog",
    "is_active",
    "download_limit",
    "expiration_days",
    "requires_license",
]

LICENSE_TEMPLATE_FIELDS = [
    "name",
    "description",
    "is_active",
    "pattern",
    "prefix",
    "suffix",
    "separator",
    "character_set",
    "min_length",
    "max_length",
]

LICENSE_POOL_FIELDS = [
    "name",
    "description",
    "total_keys",
    "keys_generated",
    "keys_distributed",
    "status",
    "key_type",
    "max_activations",
    "expires_after_days",
]

LICENSE_PROVIDER_FIELDS = [
    "name",
    "provider_type",
    "is_active",
    "api_endpoint",
    "sync_on_order",
    "sync_on_activation",
    "sync_on_deactivation",
    "sync_bidirectional",
    "webhook_events",
    "provider_config",
    "product_mapping",
    "connection_status",
]


class DigitalProductsSerializer(CollectionSyncSerializer):
    category_key = "digital_products"
    natural_key_fields = ["name"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from catalog.models import DigitalAsset

        self.model_class = DigitalAsset

    def get_count(self):
        from catalog.models import DigitalAsset, LicenseKeyTemplate, LicensePool, LicenseProvider

        return (
            DigitalAsset.objects.count()
            + LicenseKeyTemplate.objects.count()
            + LicensePool.objects.count()
            + LicenseProvider.objects.count()
        )

    def export(self, credential_mode="redact"):
        from catalog.models import DigitalAsset, LicenseKeyTemplate, LicensePool, LicenseProvider

        items = []

        # License Templates (no dependencies)
        for tmpl in LicenseKeyTemplate.objects.all():
            data = {f: getattr(tmpl, f) for f in LICENSE_TEMPLATE_FIELDS}
            data["_source_pk"] = tmpl.pk
            data["_model"] = "LicenseKeyTemplate"
            items.append(data)

        # License Providers
        for prov in LicenseProvider.objects.all():
            data = {f: getattr(prov, f) for f in LICENSE_PROVIDER_FIELDS}
            data["_source_pk"] = prov.pk
            data["_model"] = "LicenseProvider"
            # Credentials (api_key, api_secret, webhook_secret are plaintext CharFields)
            if credential_mode == "decrypt":
                data["_credentials"] = {
                    "api_key": prov.api_key,
                    "api_secret": prov.api_secret,
                    "webhook_secret": prov.webhook_secret,
                }
            elif credential_mode == "redact":
                data["_credentials_redacted"] = redact_credentials(
                    {
                        "api_key": prov.api_key,
                        "api_secret": prov.api_secret,
                        "webhook_secret": prov.webhook_secret,
                    }
                )
            items.append(data)

        # Digital Assets
        for asset in DigitalAsset.objects.select_related("product").all():
            data = {f: getattr(asset, f) for f in DIGITAL_ASSET_FIELDS}
            data["_source_pk"] = asset.pk
            data["_model"] = "DigitalAsset"
            data["_product_sku"] = asset.product.sku
            # File data (may be large — use file_handler)
            try:
                data["_file"] = export_file_field(asset, "file")
            except Exception:
                data["_file"] = None
                logger.warning(f"Could not export file for DigitalAsset {asset.filename}")
            items.append(data)

        # License Pools
        for pool in LicensePool.objects.select_related(
            "product",
            "license_template",
            "sync_to_provider",
        ).all():
            data = {f: getattr(pool, f) for f in LICENSE_POOL_FIELDS}
            data["_source_pk"] = pool.pk
            data["_model"] = "LicensePool"
            data["_product_sku"] = pool.product.sku
            data["_template_name"] = pool.license_template.name if pool.license_template else None
            data["_provider_name"] = pool.sync_to_provider.name if pool.sync_to_provider else None

            if pool.pool_expires_at:
                data["_pool_expires_at"] = pool.pool_expires_at.isoformat()

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

        # Import in dependency order
        order_map = {
            "LicenseKeyTemplate": 0,
            "LicenseProvider": 1,
            "DigitalAsset": 2,
            "LicensePool": 3,
        }
        sorted_items = sorted(items, key=lambda x: order_map.get(x.get("_model"), 99))

        for item in sorted_items:
            model_type = item.get("_model")
            try:
                with transaction.atomic():
                    if model_type == "LicenseKeyTemplate":
                        self._import_template(item)
                    elif model_type == "LicenseProvider":
                        self._import_provider(item)
                    elif model_type == "DigitalAsset":
                        self._import_asset(item)
                    elif model_type == "LicensePool":
                        self._import_pool(item)
                    else:
                        skipped += 1
                        continue
                    synced += 1
            except Exception as e:
                failed += 1
                errors.append(f"{model_type} '{item.get('name', item.get('filename', '?'))}': {e}")

        return {"synced": synced, "skipped": skipped, "failed": failed, "errors": errors}

    def _import_template(self, item):
        from catalog.models import LicenseKeyTemplate

        existing = LicenseKeyTemplate.objects.filter(name=item["name"]).first()
        obj = existing or LicenseKeyTemplate()
        for f in LICENSE_TEMPLATE_FIELDS:
            if f in item:
                setattr(obj, f, item[f])
        obj.save()

    def _import_provider(self, item):
        from catalog.models import LicenseProvider

        existing = LicenseProvider.objects.filter(name=item["name"]).first()
        obj = existing or LicenseProvider()
        for f in LICENSE_PROVIDER_FIELDS:
            if f in item:
                setattr(obj, f, item[f])
        creds = item.get("_credentials", {})
        if creds:
            obj.api_key = creds.get("api_key", obj.api_key)
            obj.api_secret = creds.get("api_secret", obj.api_secret)
            obj.webhook_secret = creds.get("webhook_secret", obj.webhook_secret)
        obj.save()

    def _import_asset(self, item):
        from catalog.models import DigitalAsset, Product

        product = Product.objects.filter(sku=item["_product_sku"]).first()
        if not product:
            raise ValueError(f"Product not found: {item['_product_sku']}")

        existing = DigitalAsset.objects.filter(
            product=product,
            filename=item["filename"],
        ).first()
        obj = existing or DigitalAsset(product=product)

        for f in DIGITAL_ASSET_FIELDS:
            if f in item:
                setattr(obj, f, item[f])

        file_data = item.get("_file")
        if file_data:
            import_file_field(obj, "file", file_data)

        obj.save()

    def _import_pool(self, item):
        from django.utils.dateparse import parse_datetime

        from catalog.models import LicenseKeyTemplate, LicensePool, LicenseProvider, Product

        product = Product.objects.filter(sku=item["_product_sku"]).first()
        if not product:
            raise ValueError(f"Product not found: {item['_product_sku']}")

        existing = LicensePool.objects.filter(
            product=product,
            name=item["name"],
        ).first()
        obj = existing or LicensePool(product=product)

        for f in LICENSE_POOL_FIELDS:
            if f in item:
                setattr(obj, f, item[f])

        tmpl_name = item.get("_template_name")
        if tmpl_name:
            obj.license_template = LicenseKeyTemplate.objects.filter(name=tmpl_name).first()

        prov_name = item.get("_provider_name")
        if prov_name:
            obj.sync_to_provider = LicenseProvider.objects.filter(name=prov_name).first()

        expires = item.get("_pool_expires_at")
        if expires:
            parsed = parse_datetime(expires)
            if parsed:
                obj.pool_expires_at = parsed

        obj.save()

    def generate_diff(self, remote_data):
        from catalog.models import (
            DigitalAsset,
            LicenseKeyTemplate,
            LicensePool,
            LicenseProvider,
            Product,
        )

        items = remote_data.get("items", [])
        changes = []

        for item in items:
            model_type = item.get("_model")
            existing = None
            fields = []
            name = item.get("name", item.get("filename", "?"))

            if model_type == "LicenseKeyTemplate":
                existing = LicenseKeyTemplate.objects.filter(name=item.get("name", "")).first()
                fields = LICENSE_TEMPLATE_FIELDS

            elif model_type == "LicenseProvider":
                existing = LicenseProvider.objects.filter(name=item.get("name", "")).first()
                fields = LICENSE_PROVIDER_FIELDS

            elif model_type == "DigitalAsset":
                product = Product.objects.filter(sku=item.get("_product_sku", "")).first()
                if product:
                    existing = DigitalAsset.objects.filter(
                        product=product,
                        filename=item.get("filename", ""),
                    ).first()
                name = item.get("filename", "?")
                fields = DIGITAL_ASSET_FIELDS

            elif model_type == "LicensePool":
                product = Product.objects.filter(sku=item.get("_product_sku", "")).first()
                if product:
                    existing = LicensePool.objects.filter(
                        product=product,
                        name=item.get("name", ""),
                    ).first()
                fields = LICENSE_POOL_FIELDS

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
