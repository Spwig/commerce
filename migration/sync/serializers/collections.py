"""
Collections Sync Serializer

Handles export/import of product collections:
- Collection: Manual/automatic product groupings with images and design settings

M2M products are resolved by SKU during full migration.
In settings sync, collection definitions are synced but product assignments
are skipped (products may not exist on the target).
"""

import logging

from django.db import transaction

from ..file_handler import export_file_field, import_file_field
from .base import CollectionSyncSerializer as BaseCollectionSerializer

logger = logging.getLogger(__name__)

COLLECTION_FIELDS = [
    "name",
    "slug",
    "description",
    "collection_type",
    "auto_criteria",
    # SEO
    "meta_title",
    "meta_description",
    # Display
    "is_active",
    "is_featured",
    "sort_order",
    # DesignMixin
    "template_variant",
    "css_classes",
    "layout_config",
    "style_overrides",
    "responsive_config",
    "inherit_parent_theme",
]


class CollectionsSerializer(BaseCollectionSerializer):
    """Serializer for product collections.

    Models handled:
        - Collection: Product groupings with image, banner, and M2M products

    M2M product assignments are exported as SKU lists and resolved on import.
    """

    category_key = "collections"
    natural_key_fields = ["slug"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from catalog.models import Collection

        self.model_class = Collection

    def get_count(self):
        from catalog.models import Collection

        return Collection.objects.count()

    def export(self, credential_mode="redact"):
        from catalog.models import Collection

        items = []

        for coll in Collection.objects.prefetch_related("products").all():
            data = {f: getattr(coll, f) for f in COLLECTION_FIELDS}
            data["_model"] = "Collection"
            data["_source_pk"] = coll.pk

            # M2M products as SKU list
            data["_product_skus"] = list(coll.products.values_list("sku", flat=True))

            # File fields
            data["_files"] = {}
            for ff in ("image", "banner_image"):
                file_data = export_file_field(coll, ff)
                if file_data:
                    data["_files"][ff] = file_data

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
            if item.get("_model") != "Collection":
                skipped += 1
                continue
            try:
                with transaction.atomic():
                    self._import_collection(item)
                    synced += 1
            except Exception as e:
                failed += 1
                errors.append(f"Collection {item.get('slug', '?')}: {e}")

        result = {"synced": synced, "skipped": skipped, "failed": failed, "errors": errors}

        if sync_mode == "mirror":
            deleted = self._delete_absent(items)
            result["deleted"] = deleted

        return result

    def _import_collection(self, item):
        from catalog.models import Collection, Product

        existing = Collection.objects.filter(slug=item["slug"]).first()
        coll = existing or Collection()

        for f in COLLECTION_FIELDS:
            if f in item:
                setattr(coll, f, item[f])

        coll.save()

        # Import files
        files = item.get("_files", {})
        for ff in ("image", "banner_image"):
            if ff in files:
                import_file_field(coll, ff, files[ff])
        if files:
            coll.save()

        # M2M products (resolved by SKU, silently skip missing)
        product_skus = item.get("_product_skus", [])
        if product_skus:
            products = Product.objects.filter(sku__in=product_skus)
            coll.products.set(products)
        elif existing:
            # Clear if empty list provided
            coll.products.clear()

    def _delete_absent(self, remote_items):
        from catalog.models import Collection

        remote_slugs = {item["slug"] for item in remote_items if item.get("_model") == "Collection"}

        deleted = 0
        for coll in Collection.objects.all():
            if coll.slug not in remote_slugs:
                try:
                    coll.delete()
                    deleted += 1
                except Exception as e:
                    logger.warning(f"Cannot delete collection {coll.slug}: {e}")
        return deleted

    def generate_diff(self, remote_data):
        from catalog.models import Collection

        items = remote_data.get("items", [])
        changes = []

        for item in items:
            if item.get("_model") != "Collection":
                continue

            slug = item.get("slug")
            existing = Collection.objects.filter(slug=slug).first()

            if existing:
                field_changes = self._compute_field_diff(existing, item, COLLECTION_FIELDS)
                if field_changes:
                    changes.append(
                        {
                            "type": "modify",
                            "model": "Collection",
                            "name": slug,
                            "changes": field_changes,
                        }
                    )
            else:
                changes.append(
                    {
                        "type": "add",
                        "model": "Collection",
                        "name": slug,
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
