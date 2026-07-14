"""
Preference Export Service

Handles exporting communication preferences for GDPR Article 15 (Right to Access).
Provides complete preference data including change history in JSON/CSV formats.
"""

import csv
import logging
from datetime import timedelta
from io import StringIO

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.utils import timezone

logger = logging.getLogger(__name__)
User = get_user_model()


class PreferenceExportService:
    """
    Service for exporting user preference data.

    Implements GDPR Article 15 (Right to Access) by providing complete
    preference data including change history in structured formats.
    """

    @classmethod
    def export_user_preferences(cls, user) -> dict:
        """
        Export complete preference data for a user.

        Args:
            user: User instance

        Returns:
            Dict with complete preference data including:
            - User info
            - Current preferences
            - Consent metadata
            - Verification status
            - Change history (last 90 days)
            - Export metadata
        """
        from accounts.models import CommunicationPreference
        from accounts.serializers import CommunicationPreferenceSerializer

        try:
            # Get preference
            prefs = CommunicationPreference.objects.get(user=user)

            # Serialize current state
            serializer = CommunicationPreferenceSerializer(prefs)

            # Build export data
            export_data = {
                # User information
                "user": {
                    "email": user.email,
                    "username": user.username,
                    "full_name": user.get_full_name() or "",
                },
                # Current preferences
                "preferences": serializer.data,
                # Consent metadata
                "consent": {
                    "source": prefs.consent_source,
                    "timestamp": prefs.consent_timestamp.isoformat()
                    if prefs.consent_timestamp
                    else None,
                    "ip_address": prefs.consent_ip or "",
                    "user_agent": prefs.consent_user_agent or "",
                },
                # Verification status
                "verification": {
                    "email_verified": prefs.email_verified,
                    "email_verified_at": prefs.email_verified_at.isoformat()
                    if prefs.email_verified_at
                    else None,
                    "sms_verified": prefs.sms_verified,
                    "sms_verified_at": prefs.sms_verified_at.isoformat()
                    if prefs.sms_verified_at
                    else None,
                },
                # Change history
                "change_history": cls._get_change_history(prefs),
                # Export metadata
                "export_metadata": {
                    "timestamp": timezone.now().isoformat(),
                    "format_version": "1.0",
                },
            }

            logger.info(f"Exported preferences for user {user.email}")

            return export_data

        except Exception as e:
            logger.error(f"Error exporting preferences for user {user.email}: {e}", exc_info=True)
            return {
                "error": str(e),
                "export_metadata": {
                    "timestamp": timezone.now().isoformat(),
                    "format_version": "1.0",
                },
            }

    @classmethod
    def export_to_file(cls, user, format="json") -> HttpResponse:
        """
        Export preferences to downloadable file.

        Args:
            user: User instance
            format: 'json' or 'csv'

        Returns:
            HttpResponse with file download
        """
        import json

        if format == "json":
            # Export as JSON
            data = cls.export_user_preferences(user)

            response = HttpResponse(json.dumps(data, indent=2), content_type="application/json")
            filename = f"preferences_{user.username}_{timezone.now().strftime('%Y%m%d')}.json"
            response["Content-Disposition"] = f'attachment; filename="{filename}"'

            return response

        elif format == "csv":
            # Export as CSV (flattened key-value pairs)
            data = cls.export_user_preferences(user)
            flattened = cls._flatten_for_csv(data)

            output = StringIO()
            writer = csv.writer(output)

            # Write header
            writer.writerow(["Field", "Value"])

            # Write data
            for key, value in flattened.items():
                writer.writerow([key, value])

            response = HttpResponse(output.getvalue(), content_type="text/csv")
            filename = f"preferences_{user.username}_{timezone.now().strftime('%Y%m%d')}.csv"
            response["Content-Disposition"] = f'attachment; filename="{filename}"'

            return response

        else:
            raise ValueError(f"Unsupported format: {format}")

    @classmethod
    def _get_change_history(cls, preference) -> list[dict]:
        """
        Get change history for preference (last 90 days, max 100 entries).

        Args:
            preference: CommunicationPreference instance

        Returns:
            List of change log entries
        """
        from accounts.models import PreferenceChangeLog

        # Last 90 days
        cutoff_date = timezone.now() - timedelta(days=90)

        logs = PreferenceChangeLog.objects.filter(
            preference=preference, timestamp__gte=cutoff_date
        ).order_by("-timestamp")[:100]

        history = []
        for log in logs:
            history.append(
                {
                    "timestamp": log.timestamp.isoformat(),
                    "action": log.action,
                    "source": log.source,
                    "old_value": log.old_value,
                    "new_value": log.new_value,
                    "ip_address": log.ip_address or "",
                    "notes": log.notes or "",
                }
            )

        return history

    @classmethod
    def _flatten_for_csv(cls, data: dict, parent_key: str = "", sep: str = ".") -> dict:
        """
        Flatten nested dict for CSV export.

        Args:
            data: Nested dict
            parent_key: Parent key for recursion
            sep: Separator for nested keys

        Returns:
            Flattened dict with dot-separated keys
        """
        items = []

        for key, value in data.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else key

            if isinstance(value, dict):
                # Recursively flatten nested dicts
                items.extend(cls._flatten_for_csv(value, new_key, sep=sep).items())
            elif isinstance(value, list):
                # Convert lists to comma-separated string
                if value and isinstance(value[0], dict):
                    # List of dicts - show count
                    items.append((new_key, f"{len(value)} entries"))
                else:
                    # List of primitives - join as string
                    items.append((new_key, ", ".join(str(v) for v in value)))
            else:
                # Primitive value
                items.append((new_key, str(value) if value is not None else ""))

        return dict(items)
