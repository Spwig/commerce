"""
SEO Providers Sync Serializer

Handles export/import of SEO generator provider accounts.
"""

import logging

from django.contrib.sites.models import Site
from django.db import transaction

from ..credential_handler import (
    decrypt_credentials_for_export,
    encrypt_credentials_for_import,
    redact_credentials,
)
from .base import CollectionSyncSerializer

logger = logging.getLogger(__name__)

SEO_PROVIDER_FIELDS = [
    "provider_key",
    "name",
    "is_active",
    "is_primary",
    "priority",
    "settings",
]


class SEOProvidersSerializer(CollectionSyncSerializer):
    """Serializer for SEO generator provider accounts.

    Models handled:
        - SEOProviderAccount: SEO generator provider configurations
    """

    category_key = "seo_providers"
    natural_key_fields = ["provider_key"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from seo_generator.models import SEOProviderAccount

        self.model_class = SEOProviderAccount

    def get_count(self):
        from seo_generator.models import SEOProviderAccount

        return SEOProviderAccount.objects.count()

    def export(self, credential_mode="redact"):
        from seo_generator.models import SEOProviderAccount

        items = []
        for account in SEOProviderAccount.objects.all():
            data = {f: getattr(account, f) for f in SEO_PROVIDER_FIELDS}
            data["_source_pk"] = account.pk
            data["_model"] = "SEOProviderAccount"

            if account.component:
                data["_component_slug"] = account.component.slug

            if credential_mode == "decrypt":
                creds = decrypt_credentials_for_export(
                    "seo_providers", "SEOProviderAccount", account
                )
                if creds:
                    data["_credentials"] = creds
            elif credential_mode == "redact":
                creds = decrypt_credentials_for_export(
                    "seo_providers", "SEOProviderAccount", account
                )
                if creds:
                    data["_credentials_redacted"] = redact_credentials(creds)

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

        site = Site.objects.get(pk=1)

        for item in items:
            try:
                with transaction.atomic():
                    self._import_account(item, site)
                    synced += 1
            except Exception as e:
                failed += 1
                errors.append(f"SEOProviderAccount '{item.get('provider_key', '?')}': {e}")

        result = {"synced": synced, "skipped": skipped, "failed": failed, "errors": errors}

        if sync_mode == "mirror":
            deleted = self._delete_absent(items)
            result["deleted"] = deleted

        return result

    def _import_account(self, item, site):
        from seo_generator.models import SEOProviderAccount

        existing = SEOProviderAccount.objects.filter(
            provider_key=item["provider_key"],
        ).first()
        obj = existing or SEOProviderAccount(site=site)

        for f in SEO_PROVIDER_FIELDS:
            if f in item:
                setattr(obj, f, item[f])

        if "_credentials" in item and item["_credentials"]:
            encrypted = encrypt_credentials_for_import(
                "seo_providers",
                "SEOProviderAccount",
                item["_credentials"],
            )
            if encrypted:
                obj.credentials = encrypted

        if "_component_slug" in item and item["_component_slug"]:
            try:
                from component_updates.models import ComponentRegistry

                obj.component = ComponentRegistry.objects.get(slug=item["_component_slug"])
            except Exception:
                pass

        obj.save()

    def _delete_absent(self, remote_items):
        from seo_generator.models import SEOProviderAccount

        remote_keys = {item["provider_key"] for item in remote_items}
        deleted = 0
        for obj in SEOProviderAccount.objects.all():
            if obj.provider_key not in remote_keys:
                try:
                    obj.delete()
                    deleted += 1
                except Exception as e:
                    logger.warning(f"Cannot delete SEOProviderAccount '{obj.provider_key}': {e}")
        return deleted

    def generate_diff(self, remote_data):
        from seo_generator.models import SEOProviderAccount

        items = remote_data.get("items", [])
        changes = []

        for item in items:
            existing = SEOProviderAccount.objects.filter(
                provider_key=item.get("provider_key"),
            ).first()
            if existing:
                field_changes = self._compute_field_diff(existing, item, SEO_PROVIDER_FIELDS)
                if field_changes:
                    changes.append(
                        {
                            "type": "modify",
                            "model": "SEOProviderAccount",
                            "name": item.get("name", item.get("provider_key", "?")),
                            "changes": field_changes,
                        }
                    )
            else:
                changes.append(
                    {
                        "type": "add",
                        "model": "SEOProviderAccount",
                        "name": item.get("name", item.get("provider_key", "?")),
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
