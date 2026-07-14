"""
Search Configuration Sync Serializer

Handles export/import of search models:
- SearchRedirect
"""

import logging

from django.db import transaction

from .base import CollectionSyncSerializer

logger = logging.getLogger(__name__)

SEARCH_REDIRECT_FIELDS = [
    "term",
    "match_type",
    "redirect_url",
    "redirect_type",
    "is_active",
]


class SearchConfigSerializer(CollectionSyncSerializer):
    """Serializer for search configuration.

    Models handled:
        - SearchRedirect: Search term redirects
    """

    category_key = "search_config"
    natural_key_fields = ["term"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from search.models import SearchRedirect

        self.model_class = SearchRedirect

    def get_count(self):
        from search.models import SearchRedirect

        return SearchRedirect.objects.count()

    def export(self, credential_mode="redact"):
        from search.models import SearchRedirect

        items = []
        for redirect in SearchRedirect.objects.all():
            data = {f: getattr(redirect, f) for f in SEARCH_REDIRECT_FIELDS}
            data["_source_pk"] = redirect.pk
            data["_model"] = "SearchRedirect"
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
                    self._import_redirect(item)
                    synced += 1
            except Exception as e:
                failed += 1
                errors.append(f"SearchRedirect '{item.get('term', '?')}': {e}")

        result = {"synced": synced, "skipped": skipped, "failed": failed, "errors": errors}

        if sync_mode == "mirror":
            deleted = self._delete_absent(items)
            result["deleted"] = deleted

        return result

    def _import_redirect(self, item):
        from search.models import SearchRedirect

        existing = SearchRedirect.objects.filter(term=item["term"]).first()
        obj = existing or SearchRedirect()

        for f in SEARCH_REDIRECT_FIELDS:
            if f in item:
                setattr(obj, f, item[f])
        obj.save()

    def _delete_absent(self, remote_items):
        from search.models import SearchRedirect

        remote_terms = {item["term"] for item in remote_items}
        deleted = 0
        for obj in SearchRedirect.objects.all():
            if obj.term not in remote_terms:
                try:
                    obj.delete()
                    deleted += 1
                except Exception as e:
                    logger.warning(f"Cannot delete SearchRedirect '{obj.term}': {e}")
        return deleted

    def generate_diff(self, remote_data):
        from search.models import SearchRedirect

        items = remote_data.get("items", [])
        changes = []

        for item in items:
            existing = SearchRedirect.objects.filter(term=item.get("term")).first()
            if existing:
                field_changes = self._compute_field_diff(existing, item, SEARCH_REDIRECT_FIELDS)
                if field_changes:
                    changes.append(
                        {
                            "type": "modify",
                            "model": "SearchRedirect",
                            "name": item.get("term", "?"),
                            "changes": field_changes,
                        }
                    )
            else:
                changes.append(
                    {
                        "type": "add",
                        "model": "SearchRedirect",
                        "name": item.get("term", "?"),
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
