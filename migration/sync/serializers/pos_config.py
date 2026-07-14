"""
POS Configuration Sync Serializer

Handles export/import of POS configuration models:
- StoreGroup
- POSTerminalProvider (with encrypted credentials)
- POSTerminal
- ReceiptTemplate
- PromoSlide
- POSStaffDiscount
"""

import logging
from decimal import Decimal

from django.db import transaction

from ..credential_handler import (
    decrypt_credentials_for_export,
    encrypt_credentials_for_import,
    redact_credentials,
)
from .base import CollectionSyncSerializer

logger = logging.getLogger(__name__)

STORE_GROUP_FIELDS = [
    "name",
    "code",
    "currency",
    "language",
    "timezone",
    "settings",
    "sort_order",
    "is_active",
]

TERMINAL_PROVIDER_FIELDS = [
    "provider_key",
    "display_name",
    "provider_settings",
    "is_active",
]

TERMINAL_FIELDS = [
    "name",
    "hardware_config",
    "currency",
    "order_sync_days",
    "order_sync_limit",
    "is_active",
]

RECEIPT_TEMPLATE_FIELDS = [
    "name",
    "paper_width",
    "header_text",
    "show_store_address",
    "custom_address",
    "show_store_phone",
    "custom_phone",
    "show_store_email",
    "custom_email",
    "tax_id_label",
    "tax_id_number",
    "business_registration",
    "show_sku",
    "show_cashier",
    "show_terminal_name",
    "footer_text",
    "return_policy",
    "qr_enabled",
    "qr_url",
    "qr_label",
    "show_powered_by",
]

PROMO_SLIDE_FIELDS = [
    "title",
    "subtitle",
    "sort_order",
    "is_active",
]

STAFF_DISCOUNT_FIELDS = [
    "max_discount_percentage",
    "max_discount_amount",
    "can_apply_item_discounts",
    "can_apply_cart_discounts",
    "requires_reason",
    "is_manager",
]


class POSConfigSerializer(CollectionSyncSerializer):
    """Serializer for POS configuration.

    Models handled:
        - StoreGroup: POS store group definitions
        - POSTerminalProvider: Terminal hardware provider accounts
        - POSTerminal: Individual terminal configurations
        - ReceiptTemplate: Receipt printing templates
        - PromoSlide: Promotional slides displayed on POS
        - POSStaffDiscount: Staff discount permissions
    """

    category_key = "pos_config"
    natural_key_fields = ["code"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from pos_app.models import StoreGroup

        self.model_class = StoreGroup

    def get_count(self):
        from pos_app.models import (
            POSStaffDiscount,
            POSTerminal,
            POSTerminalProvider,
            PromoSlide,
            ReceiptTemplate,
            StoreGroup,
        )

        return (
            StoreGroup.objects.count()
            + POSTerminalProvider.objects.count()
            + POSTerminal.objects.count()
            + ReceiptTemplate.objects.count()
            + PromoSlide.objects.count()
            + POSStaffDiscount.objects.count()
        )

    def export(self, credential_mode="redact"):
        from pos_app.models import (
            POSStaffDiscount,
            POSTerminal,
            POSTerminalProvider,
            PromoSlide,
            ReceiptTemplate,
            StoreGroup,
        )

        from ..file_handler import export_file_field

        items = []

        # StoreGroups
        for sg in StoreGroup.objects.all().order_by("sort_order"):
            data = {f: getattr(sg, f) for f in STORE_GROUP_FIELDS}
            data["_source_pk"] = sg.pk
            data["_model"] = "StoreGroup"
            items.append(data)

        # Terminal Providers
        for tp in POSTerminalProvider.objects.all():
            data = {f: getattr(tp, f) for f in TERMINAL_PROVIDER_FIELDS}
            data["_source_pk"] = str(tp.pk)
            data["_model"] = "POSTerminalProvider"

            if tp.component:
                data["_component_slug"] = tp.component.slug

            if credential_mode == "decrypt":
                creds = decrypt_credentials_for_export(
                    "pos_config",
                    "POSTerminalProvider",
                    tp,
                )
                if creds:
                    data["_credentials"] = creds
            elif credential_mode == "redact":
                creds = decrypt_credentials_for_export(
                    "pos_config",
                    "POSTerminalProvider",
                    tp,
                )
                if creds:
                    data["_credentials_redacted"] = redact_credentials(creds)

            items.append(data)

        # Terminals
        for term in POSTerminal.objects.select_related("warehouse").all():
            data = {f: getattr(term, f) for f in TERMINAL_FIELDS}
            data["_source_pk"] = term.pk
            data["_model"] = "POSTerminal"
            data["_warehouse_code"] = term.warehouse.code if term.warehouse else None
            # Assigned users exported by email
            data["_assigned_user_emails"] = list(
                term.assigned_users.values_list("email", flat=True)
            )
            items.append(data)

        # Receipt Templates
        for rt in ReceiptTemplate.objects.all():
            data = {f: getattr(rt, f) for f in RECEIPT_TEMPLATE_FIELDS}
            data["_source_pk"] = rt.pk
            data["_model"] = "ReceiptTemplate"
            data["_store_group_code"] = rt.store_group.code if rt.store_group else None
            data["_warehouse_code"] = rt.warehouse.code if rt.warehouse else None
            # Logo via MediaAsset FK
            if rt.logo:
                data["_logo_file"] = export_file_field(rt.logo, "file")
            items.append(data)

        # Promo Slides
        for ps in PromoSlide.objects.all().order_by("sort_order"):
            data = {f: getattr(ps, f) for f in PROMO_SLIDE_FIELDS}
            data["_source_pk"] = ps.pk
            data["_model"] = "PromoSlide"
            data["_store_group_code"] = ps.store_group.code if ps.store_group else None
            data["_warehouse_code"] = ps.warehouse.code if ps.warehouse else None
            if ps.image:
                data["_image_file"] = export_file_field(ps.image, "file")
            items.append(data)

        # Staff Discounts
        for sd in POSStaffDiscount.objects.select_related("user").all():
            data = {f: getattr(sd, f) for f in STAFF_DISCOUNT_FIELDS}
            data["_source_pk"] = sd.pk
            data["_model"] = "POSStaffDiscount"
            data["_user_email"] = sd.user.email
            for df in ["max_discount_percentage", "max_discount_amount"]:
                if data.get(df) is not None:
                    data[df] = str(data[df])
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
            "StoreGroup": 0,
            "POSTerminalProvider": 1,
            "POSTerminal": 2,
            "ReceiptTemplate": 3,
            "PromoSlide": 4,
            "POSStaffDiscount": 5,
        }
        sorted_items = sorted(items, key=lambda x: order_map.get(x.get("_model"), 99))

        for item in sorted_items:
            model_type = item.get("_model")
            try:
                with transaction.atomic():
                    if model_type == "StoreGroup":
                        self._import_store_group(item)
                    elif model_type == "POSTerminalProvider":
                        self._import_terminal_provider(item)
                    elif model_type == "POSTerminal":
                        self._import_terminal(item)
                    elif model_type == "ReceiptTemplate":
                        self._import_receipt_template(item)
                    elif model_type == "PromoSlide":
                        self._import_promo_slide(item)
                    elif model_type == "POSStaffDiscount":
                        self._import_staff_discount(item)
                    else:
                        skipped += 1
                        continue
                    synced += 1
            except Exception as e:
                failed += 1
                name = item.get("name", item.get("code", item.get("title", "?")))
                errors.append(f"{model_type} '{name}': {e}")

        result = {"synced": synced, "skipped": skipped, "failed": failed, "errors": errors}

        if sync_mode == "mirror":
            deleted = self._delete_absent(items)
            result["deleted"] = deleted

        return result

    def _import_store_group(self, item):
        from pos_app.models import StoreGroup

        existing = StoreGroup.objects.filter(code=item["code"]).first()
        obj = existing or StoreGroup()
        for f in STORE_GROUP_FIELDS:
            if f in item:
                setattr(obj, f, item[f])
        obj.save()

    def _import_terminal_provider(self, item):
        from pos_app.models import POSTerminalProvider

        existing = POSTerminalProvider.objects.filter(
            provider_key=item["provider_key"],
        ).first()
        obj = existing or POSTerminalProvider()
        for f in TERMINAL_PROVIDER_FIELDS:
            if f in item:
                setattr(obj, f, item[f])

        if "_credentials" in item and item["_credentials"]:
            encrypted = encrypt_credentials_for_import(
                "pos_config",
                "POSTerminalProvider",
                item["_credentials"],
            )
            if encrypted:
                obj.credentials_encrypted = encrypted

        if "_component_slug" in item and item["_component_slug"]:
            try:
                from component_updates.models import ComponentRegistry

                obj.component = ComponentRegistry.objects.get(slug=item["_component_slug"])
            except Exception:
                pass

        obj.save()

    def _import_terminal(self, item):
        from django.contrib.auth import get_user_model

        from catalog.models import Warehouse
        from pos_app.models import POSTerminal

        User = get_user_model()

        existing = POSTerminal.objects.filter(name=item["name"]).first()
        obj = existing or POSTerminal()

        for f in TERMINAL_FIELDS:
            if f in item:
                setattr(obj, f, item[f])

        wh_code = item.get("_warehouse_code")
        if wh_code:
            obj.warehouse = Warehouse.objects.filter(code=wh_code).first()

        obj.save()

        # M2M assigned users
        user_emails = item.get("_assigned_user_emails", [])
        if user_emails:
            users = User.objects.filter(email__in=user_emails)
            obj.assigned_users.set(users)

    def _import_receipt_template(self, item):
        from catalog.models import Warehouse
        from pos_app.models import ReceiptTemplate, StoreGroup

        from ..file_handler import import_file_field

        # Match by store_group or warehouse
        sg_code = item.get("_store_group_code")
        wh_code = item.get("_warehouse_code")

        existing = None
        if sg_code:
            sg = StoreGroup.objects.filter(code=sg_code).first()
            if sg:
                existing = ReceiptTemplate.objects.filter(store_group=sg).first()
        elif wh_code:
            wh = Warehouse.objects.filter(code=wh_code).first()
            if wh:
                existing = ReceiptTemplate.objects.filter(warehouse=wh).first()
        if not existing:
            existing = ReceiptTemplate.objects.filter(name=item.get("name")).first()

        obj = existing or ReceiptTemplate()

        for f in RECEIPT_TEMPLATE_FIELDS:
            if f in item:
                setattr(obj, f, item[f])

        if sg_code:
            obj.store_group = StoreGroup.objects.filter(code=sg_code).first()
        if wh_code:
            obj.warehouse = Warehouse.objects.filter(code=wh_code).first()

        # Logo
        logo_data = item.get("_logo_file")
        if logo_data:
            from media_library.models import MediaAsset

            asset = MediaAsset()
            import_file_field(asset, "file", logo_data)
            asset.save()
            obj.logo = asset

        obj.save()

    def _import_promo_slide(self, item):
        from catalog.models import Warehouse
        from pos_app.models import PromoSlide, StoreGroup

        from ..file_handler import import_file_field

        # Match by title + sort_order
        existing = PromoSlide.objects.filter(
            title=item.get("title", ""),
            sort_order=item.get("sort_order", 0),
        ).first()

        obj = existing or PromoSlide()

        for f in PROMO_SLIDE_FIELDS:
            if f in item:
                setattr(obj, f, item[f])

        sg_code = item.get("_store_group_code")
        if sg_code:
            obj.store_group = StoreGroup.objects.filter(code=sg_code).first()

        wh_code = item.get("_warehouse_code")
        if wh_code:
            obj.warehouse = Warehouse.objects.filter(code=wh_code).first()

        # Image (required FK)
        image_data = item.get("_image_file")
        if image_data:
            from media_library.models import MediaAsset

            asset = MediaAsset()
            import_file_field(asset, "file", image_data)
            asset.save()
            obj.image = asset

        obj.save()

    def _import_staff_discount(self, item):
        from django.contrib.auth import get_user_model

        from pos_app.models import POSStaffDiscount

        User = get_user_model()

        user_email = item.get("_user_email")
        if not user_email:
            return

        user = User.objects.filter(email=user_email).first()
        if not user:
            logger.warning(f"User not found for staff discount: {user_email}")
            return

        existing = POSStaffDiscount.objects.filter(user=user).first()
        obj = existing or POSStaffDiscount(user=user)

        for f in STAFF_DISCOUNT_FIELDS:
            if f in item:
                val = item[f]
                if f in ("max_discount_percentage", "max_discount_amount") and val is not None:
                    val = Decimal(str(val))
                setattr(obj, f, val)

        obj.save()

    def _delete_absent(self, remote_items):
        from pos_app.models import (
            POSStaffDiscount,
            POSTerminal,
            POSTerminalProvider,
            StoreGroup,
        )

        deleted = 0

        # Delete in reverse dependency order
        remote_sd_emails = {
            item["_user_email"] for item in remote_items if item.get("_model") == "POSStaffDiscount"
        }
        for sd in POSStaffDiscount.objects.select_related("user").all():
            if sd.user.email not in remote_sd_emails:
                try:
                    sd.delete()
                    deleted += 1
                except Exception as e:
                    logger.warning(f"Cannot delete POSStaffDiscount: {e}")

        remote_codes = {item["code"] for item in remote_items if item.get("_model") == "StoreGroup"}
        remote_provider_keys = {
            item["provider_key"]
            for item in remote_items
            if item.get("_model") == "POSTerminalProvider"
        }

        for term in POSTerminal.objects.all():
            # Simplified: delete terminals whose name isn't in remote
            remote_names = {
                item["name"] for item in remote_items if item.get("_model") == "POSTerminal"
            }
            if term.name not in remote_names:
                try:
                    term.delete()
                    deleted += 1
                except Exception as e:
                    logger.warning(f"Cannot delete POSTerminal '{term.name}': {e}")

        for tp in POSTerminalProvider.objects.all():
            if tp.provider_key not in remote_provider_keys:
                try:
                    tp.delete()
                    deleted += 1
                except Exception as e:
                    logger.warning(f"Cannot delete POSTerminalProvider '{tp.provider_key}': {e}")

        for sg in StoreGroup.objects.all():
            if sg.code not in remote_codes:
                try:
                    sg.delete()
                    deleted += 1
                except Exception as e:
                    logger.warning(f"Cannot delete StoreGroup '{sg.code}': {e}")

        return deleted

    def generate_diff(self, remote_data):
        from pos_app.models import POSTerminal, POSTerminalProvider, StoreGroup

        items = remote_data.get("items", [])
        changes = []

        for item in items:
            model_type = item.get("_model")
            if model_type == "StoreGroup":
                existing = StoreGroup.objects.filter(code=item.get("code")).first()
                fields = STORE_GROUP_FIELDS
                name = item.get("name", item.get("code", "?"))
            elif model_type == "POSTerminalProvider":
                existing = POSTerminalProvider.objects.filter(
                    provider_key=item.get("provider_key"),
                ).first()
                fields = TERMINAL_PROVIDER_FIELDS
                name = item.get("display_name", item.get("provider_key", "?"))
            elif model_type == "POSTerminal":
                existing = POSTerminal.objects.filter(name=item.get("name")).first()
                fields = TERMINAL_FIELDS
                name = item.get("name", "?")
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
