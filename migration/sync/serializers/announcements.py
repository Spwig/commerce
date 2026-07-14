"""
Announcements Sync Serializer

Handles export/import of site announcements.
"""

import logging
from decimal import Decimal

from django.db import transaction

from ..file_handler import export_file_field, import_file_field
from .base import CollectionSyncSerializer

logger = logging.getLogger(__name__)

ANNOUNCEMENT_FIELDS = [
    "title",
    "body",
    "image_display_mode",
    "image_overlay_opacity",
    "link_type",
    "custom_url",
    "link_text",
    "show_modal",
    "is_enabled",
    "priority",
    "translations",
]


class AnnouncementsSerializer(CollectionSyncSerializer):
    """Serializer for site announcements.

    Models handled:
        - Announcement: Site announcements with optional link targets and images
    """

    category_key = "announcements"
    natural_key_fields = ["title"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from announcements.models import Announcement

        self.model_class = Announcement

    def get_count(self):
        from announcements.models import Announcement

        return Announcement.objects.count()

    def export(self, credential_mode="redact"):
        from announcements.models import Announcement

        items = []
        for ann in Announcement.objects.all().order_by("priority"):
            data = {f: getattr(ann, f) for f in ANNOUNCEMENT_FIELDS}
            data["_source_pk"] = ann.pk
            data["_model"] = "Announcement"

            # Decimal field
            if data.get("image_overlay_opacity") is not None:
                data["image_overlay_opacity"] = str(data["image_overlay_opacity"])

            # Datetime
            if ann.expires_at:
                data["_expires_at"] = ann.expires_at.isoformat()

            # Image via MediaAsset FK
            if ann.image:
                data["_image_file"] = export_file_field(ann.image, "file")
                data["_image_alt"] = ann.image.alt_text if hasattr(ann.image, "alt_text") else ""

            # Link target references (portable by slug/identifier)
            if ann.product_reference:
                data["_product_sku"] = ann.product_reference.sku
            if ann.category_reference:
                data["_category_slug"] = ann.category_reference.slug
            if ann.blog_post_reference:
                data["_blog_post_slug"] = ann.blog_post_reference.slug
            if ann.page_reference:
                data["_page_slug"] = ann.page_reference.slug

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
                    self._import_announcement(item)
                    synced += 1
            except Exception as e:
                failed += 1
                errors.append(f"Announcement '{item.get('title', '?')[:50]}': {e}")

        result = {"synced": synced, "skipped": skipped, "failed": failed, "errors": errors}

        if sync_mode == "mirror":
            deleted = self._delete_absent(items)
            result["deleted"] = deleted

        return result

    def _import_announcement(self, item):
        from django.utils.dateparse import parse_datetime

        from announcements.models import Announcement

        existing = Announcement.objects.filter(title=item["title"]).first()
        obj = existing or Announcement()

        for f in ANNOUNCEMENT_FIELDS:
            if f in item:
                val = item[f]
                if f == "image_overlay_opacity" and val is not None:
                    val = Decimal(str(val))
                setattr(obj, f, val)

        # Expires at
        expires = item.get("_expires_at")
        if expires:
            parsed = parse_datetime(expires)
            if parsed:
                obj.expires_at = parsed

        # Image (create MediaAsset inline)
        image_data = item.get("_image_file")
        if image_data:
            from media_library.models import MediaAsset

            asset = MediaAsset()
            import_file_field(asset, "file", image_data)
            asset.alt_text = item.get("_image_alt", "")
            asset.save()
            obj.image = asset

        # Resolve link targets silently
        product_sku = item.get("_product_sku")
        if product_sku:
            from catalog.models import Product

            obj.product_reference = Product.objects.filter(sku=product_sku).first()

        category_slug = item.get("_category_slug")
        if category_slug:
            from catalog.models import Category

            obj.category_reference = Category.objects.filter(slug=category_slug).first()

        blog_slug = item.get("_blog_post_slug")
        if blog_slug:
            from blog.models import BlogPost

            obj.blog_post_reference = BlogPost.objects.filter(slug=blog_slug).first()

        page_slug = item.get("_page_slug")
        if page_slug:
            from page_builder.models import Page

            obj.page_reference = Page.objects.filter(slug=page_slug).first()

        obj.save()

    def _delete_absent(self, remote_items):
        from announcements.models import Announcement

        remote_titles = {item["title"] for item in remote_items}
        deleted = 0
        for obj in Announcement.objects.all():
            if obj.title not in remote_titles:
                try:
                    obj.delete()
                    deleted += 1
                except Exception as e:
                    logger.warning(f"Cannot delete Announcement: {e}")
        return deleted

    def generate_diff(self, remote_data):
        from announcements.models import Announcement

        items = remote_data.get("items", [])
        changes = []

        for item in items:
            existing = Announcement.objects.filter(title=item.get("title")).first()
            if existing:
                field_changes = self._compute_field_diff(existing, item, ANNOUNCEMENT_FIELDS)
                if field_changes:
                    changes.append(
                        {
                            "type": "modify",
                            "model": "Announcement",
                            "name": item.get("title", "?")[:50],
                            "changes": field_changes,
                        }
                    )
            else:
                changes.append(
                    {
                        "type": "add",
                        "model": "Announcement",
                        "name": item.get("title", "?")[:50],
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
