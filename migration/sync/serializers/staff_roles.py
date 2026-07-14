"""
Staff Roles Sync Serializer

Handles export/import of staff role models:
- StaffRole (with linked auth.Group)
"""

import logging

from django.db import transaction

from .base import CollectionSyncSerializer

logger = logging.getLogger(__name__)

STAFF_ROLE_FIELDS = [
    "display_name",
    "description",
    "icon",
    "color",
    "is_predefined",
    "permission_categories",
    "pos_permissions",
    "can_access_admin",
    "can_access_pos",
    "sort_order",
]


class StaffRolesSerializer(CollectionSyncSerializer):
    """Serializer for staff roles and permissions.

    Models handled:
        - StaffRole: Role definitions with permission sets (linked to auth.Group)
    """

    category_key = "staff_roles"
    natural_key_fields = ["display_name"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from staff_roles.models import StaffRole

        self.model_class = StaffRole

    def get_count(self):
        from staff_roles.models import StaffRole

        return StaffRole.objects.count()

    def export(self, credential_mode="redact"):
        from staff_roles.models import StaffRole

        items = []
        for role in StaffRole.objects.select_related("group").all():
            data = {field: getattr(role, field) for field in STAFF_ROLE_FIELDS}
            data["_source_pk"] = role.pk
            data["_model"] = "StaffRole"
            data["_group_name"] = role.group.name if role.group else ""
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
                    self._import_role(item)
                    synced += 1
            except Exception as e:
                failed += 1
                errors.append(f"{item.get('display_name', 'Unknown')}: {e}")

        result = {"synced": synced, "skipped": skipped, "failed": failed, "errors": errors}

        if sync_mode == "mirror":
            deleted = self._delete_absent(items)
            result["deleted"] = deleted

        return result

    def _import_role(self, item):
        from django.contrib.auth.models import Group

        from staff_roles.models import StaffRole

        display_name = item["display_name"]
        group_name = item.get("_group_name", display_name)

        existing = StaffRole.objects.filter(display_name=display_name).first()

        if existing:
            for field in STAFF_ROLE_FIELDS:
                if field in item:
                    setattr(existing, field, item[field])
            existing.save()
        else:
            group, _ = Group.objects.get_or_create(name=group_name)
            role = StaffRole(group=group)
            for field in STAFF_ROLE_FIELDS:
                if field in item:
                    setattr(role, field, item[field])
            role.save()

    def _delete_absent(self, remote_items):
        from staff_roles.models import StaffRole

        remote_names = {
            item["display_name"]
            for item in remote_items
            if item.get("_model") == "StaffRole" or "_model" not in item
        }
        deleted = 0
        for role in StaffRole.objects.exclude(is_predefined=True):
            if role.display_name not in remote_names:
                try:
                    with transaction.atomic():
                        group = role.group
                        role.delete()
                        if group:
                            group.delete()
                        deleted += 1
                except Exception as e:
                    logger.warning(f"Cannot delete role {role.display_name}: {e}")
        return deleted

    def generate_diff(self, remote_data):
        from staff_roles.models import StaffRole

        items = remote_data.get("items", [])
        changes = []

        for item in items:
            existing = StaffRole.objects.filter(display_name=item.get("display_name")).first()

            if existing:
                field_changes = self._compute_field_diff(existing, item, STAFF_ROLE_FIELDS)
                if field_changes:
                    changes.append(
                        {
                            "type": "modify",
                            "model": "StaffRole",
                            "name": item.get("display_name", "Unknown"),
                            "changes": field_changes,
                        }
                    )
            else:
                changes.append(
                    {
                        "type": "add",
                        "model": "StaffRole",
                        "name": item.get("display_name", "Unknown"),
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
