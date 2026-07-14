"""
Sync Diff Engine

Generates structured, human-readable diffs between source and target states.
Used for the preview step in settings sync and full migration.
"""

import logging

from django.utils.translation import gettext_lazy as _

from .category_registry import SYNC_CATEGORIES

logger = logging.getLogger(__name__)


class SyncDiffEngine:
    """
    Generates structured diffs for preview display.
    Aggregates per-category diffs into an overall job diff.
    """

    def generate_job_diff(self, sync_job, remote_data_by_category):
        """
        Generate a complete diff for a sync job across all selected categories.

        Args:
            sync_job: SyncJob instance
            remote_data_by_category: dict of category_key -> export data from remote

        Returns:
            dict: {
                'categories': {
                    'category_key': {
                        'label': str,
                        'changes': [...],
                        'warnings': [...],
                        'summary': str,
                    }
                },
                'overall_summary': str,
                'total_additions': int,
                'total_modifications': int,
                'total_removals': int,
                'warnings': list[str],
            }
        """
        from .serializers import get_serializer_for_category

        result = {
            "categories": {},
            "overall_summary": "",
            "total_additions": 0,
            "total_modifications": 0,
            "total_removals": 0,
            "warnings": [],
        }

        for category_key in sync_job.selected_categories:
            config = SYNC_CATEGORIES.get(category_key)
            if not config:
                continue

            remote_data = remote_data_by_category.get(category_key, {})
            if not remote_data:
                result["categories"][category_key] = {
                    "label": str(config["label"]),
                    "changes": [],
                    "warnings": [],
                    "summary": "No data available from remote",
                }
                continue

            try:
                serializer = get_serializer_for_category(category_key, sync_job=sync_job)
                diff = serializer.generate_diff(remote_data)

                # Add production warnings if applicable
                warnings = list(diff.get("warnings", []))
                if (
                    sync_job.connection.is_production
                    and sync_job.direction == "push"
                    and config.get("production_warning")
                ):
                    warnings.append(str(config["production_warning"]))

                if config.get("has_credentials") and sync_job.connection.is_production:
                    warnings.append(
                        str(_("Credentials will be re-encrypted on the target instance."))
                    )

                result["categories"][category_key] = {
                    "label": str(config["label"]),
                    "changes": diff.get("changes", []),
                    "warnings": warnings,
                    "summary": diff.get("summary", ""),
                }

                # Count totals
                for change in diff.get("changes", []):
                    change_type = change.get("type")
                    if change_type == "add":
                        result["total_additions"] += 1
                    elif change_type == "modify":
                        result["total_modifications"] += 1
                    elif change_type == "remove":
                        result["total_removals"] += 1

            except Exception as e:
                logger.error(f"Error generating diff for {category_key}: {e}")
                result["categories"][category_key] = {
                    "label": str(config["label"]),
                    "changes": [],
                    "warnings": [f"Error generating diff: {str(e)}"],
                    "summary": "Error",
                }

        # Build overall summary
        parts = []
        if result["total_additions"]:
            parts.append(f"{result['total_additions']} addition(s)")
        if result["total_modifications"]:
            parts.append(f"{result['total_modifications']} modification(s)")
        if result["total_removals"]:
            parts.append(f"{result['total_removals']} removal(s)")
        result["overall_summary"] = ", ".join(parts) if parts else "No changes detected"

        return result

    def generate_mirror_diff(self, sync_job, remote_data_by_category):
        """
        Generate diff that includes items to be deleted (mirror mode).
        Extends generate_job_diff with deletion detection.
        """
        diff = self.generate_job_diff(sync_job, remote_data_by_category)

        if sync_job.sync_mode != "mirror":
            return diff

        from .serializers import get_serializer_for_category

        for category_key, cat_diff in diff["categories"].items():
            config = SYNC_CATEGORIES.get(category_key, {})
            if config.get("sync_type") == "singleton":
                continue  # Singletons are always updated, never deleted

            try:
                serializer = get_serializer_for_category(category_key, sync_job=sync_job)
                remote_data = remote_data_by_category.get(category_key, {})
                remote_items = remote_data.get("items", [])

                # Get local items for comparison
                local_export = serializer.export(credential_mode="skip")
                local_items = local_export.get("items", [])

                if not isinstance(local_items, list):
                    continue

                # Find local items not in remote (candidates for deletion)
                remote_keys = set()
                key_fields = getattr(serializer, "natural_key_fields", None) or ["name"]
                for item in remote_items:
                    key = tuple(item.get(f) for f in key_fields)
                    remote_keys.add(key)

                for item in local_items:
                    key = tuple(item.get(f) for f in key_fields)
                    if key not in remote_keys:
                        cat_diff["changes"].append(
                            {
                                "type": "remove",
                                "model": config.get("models", ["Unknown"])[0].split(".")[-1],
                                "name": serializer._get_display_name(item),
                            }
                        )
                        diff["total_removals"] += 1

            except Exception as e:
                logger.error(f"Error computing mirror diff for {category_key}: {e}")
                cat_diff["warnings"].append(f"Could not compute deletions: {str(e)}")

        # Rebuild summary
        parts = []
        if diff["total_additions"]:
            parts.append(f"{diff['total_additions']} addition(s)")
        if diff["total_modifications"]:
            parts.append(f"{diff['total_modifications']} modification(s)")
        if diff["total_removals"]:
            parts.append(f"{diff['total_removals']} removal(s)")
        diff["overall_summary"] = ", ".join(parts) if parts else "No changes detected"

        return diff
