"""
Platform License Sync Serializer

Handles export/import of platform license metadata and EULA acceptance history.
This serializer is special: import initiates a license transfer via the update
server API rather than directly manipulating local database records.

Export produces:
- License key and installation UUID from the source
- Hosting type and license type from the local license file
- LicenseAcceptanceRecord history (EULA acceptance audit trail)

Import:
- Calls update server POST /api/v1/licenses/transfer/ to initiate transfer
- Source installation is deactivated, one-time transfer_token returned
- Merchant uses the transfer_token when activating the target installation
- LicenseAcceptanceRecord entries are imported as append-only audit trail
"""

import logging

import requests as http_requests
from django.db import transaction
from django.utils.dateparse import parse_datetime

from .base import BaseSyncSerializer

logger = logging.getLogger(__name__)

ACCEPTANCE_FIELDS = [
    "license_version",
    "software_version",
    "accepted_by_email",
    "accepted_via",
    "license_checksum",
    "is_current",
    "notes",
]


class PlatformLicenseSerializer(BaseSyncSerializer):
    category_key = "platform_license"
    sync_type = "special"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from core.models import LicenseAcceptanceRecord

        self.model_class = LicenseAcceptanceRecord

    def get_count(self):
        from core.models import LicenseAcceptanceRecord

        return LicenseAcceptanceRecord.objects.count() + 1  # +1 for the license itself

    def export(self, credential_mode="redact"):
        from component_updates.models import UpdateServerConfig
        from core.license import get_license_manager

        update_config = UpdateServerConfig.get_instance()
        license_manager = get_license_manager()
        license_data = license_manager.get_license_data()

        # Extract license metadata from the signed license file
        license_info = {}
        if license_data and "license" in license_data:
            lic = license_data["license"]
            license_info = {
                "license_key": lic.get("license_key", ""),
                "license_type": lic.get("license_type", ""),
                "hosting_type": lic.get("hosting_type", "self_hosted"),
                "owner_name": lic.get("owner_name", ""),
                "owner_email": lic.get("owner_email", ""),
                "company_name": lic.get("company_name", ""),
            }

        items = [
            {
                "_model": "PlatformLicenseData",
                "license_key": update_config.license_key or license_info.get("license_key", ""),
                "source_installation_uuid": str(update_config.installation_uuid),
                "source_domain": license_info.get("domain", ""),
                "hosting_type": license_info.get("hosting_type", "self_hosted"),
                "license_type": license_info.get("license_type", ""),
                "owner_name": license_info.get("owner_name", ""),
                "owner_email": license_info.get("owner_email", ""),
                "company_name": license_info.get("company_name", ""),
                "_acceptance_records": self._export_acceptance_records(),
            }
        ]

        return {
            "category": self.category_key,
            "sync_type": "special",
            "items": items,
            "total": len(items),
        }

    def _export_acceptance_records(self):
        from core.models import LicenseAcceptanceRecord

        records = []
        for rec in LicenseAcceptanceRecord.objects.all().order_by("accepted_at"):
            data = {f: getattr(rec, f) for f in ACCEPTANCE_FIELDS}
            if rec.accepted_at:
                data["_accepted_at"] = rec.accepted_at.isoformat()
            if rec.installation_id:
                data["_installation_id"] = str(rec.installation_id)
            records.append(data)
        return records

    def import_data(self, data, dry_run=False, sync_mode="additive"):
        if dry_run:
            return self.generate_diff(data)

        items = data.get("items", [])
        if not items:
            return {
                "synced": 0,
                "skipped": 0,
                "failed": 0,
                "errors": [],
                "transfer_token": None,
                "deferred": False,
            }

        item = items[0]
        errors = []
        transfer_token = None
        deferred = False

        # Phase 1: Initiate license transfer via update server
        try:
            transfer_result = self._initiate_transfer(item, sync_mode)
            transfer_token = transfer_result.get("transfer_token")
        except Exception as e:
            deferred = True
            errors.append(
                f"Update server unreachable or transfer failed: {e}. "
                f"License transfer deferred — activate manually with your license key."
            )

        # Phase 2: Import acceptance records (append-only audit trail)
        synced = 0
        for a_data in item.get("_acceptance_records", []):
            try:
                with transaction.atomic():
                    self._import_acceptance_record(a_data)
                    synced += 1
            except Exception as e:
                errors.append(f"AcceptanceRecord: {e}")

        return {
            "synced": synced,
            "skipped": 0,
            "failed": len([e for e in errors if "AcceptanceRecord" in e]),
            "errors": errors,
            "transfer_token": transfer_token,
            "deferred": deferred,
        }

    def _initiate_transfer(self, item, sync_mode):
        """
        Call the update server to initiate a license transfer.

        The serializer runs on the SOURCE installation which has the JWT
        to authenticate. The target activation is a separate step.
        """
        from component_updates.models import UpdateServerConfig

        update_config = UpdateServerConfig.get_instance()
        jwt_token = update_config.jwt_token

        if not jwt_token:
            raise ValueError(
                "No JWT token available. The source installation must be "
                "registered with the update server to initiate a transfer."
            )

        transfer_type = "staging_clone" if sync_mode == "staging" else "migration"
        transfer_url = f"{update_config.server_url}/api/v1/licenses/transfer/"

        response = http_requests.post(
            transfer_url,
            json={"transfer_type": transfer_type},
            headers={"Authorization": f"Bearer {jwt_token}"},
            timeout=30,
        )

        if response.status_code != 200:
            error_data = {}
            try:
                error_data = response.json()
            except Exception:
                pass
            error_msg = error_data.get(
                "message", error_data.get("error", f"HTTP {response.status_code}")
            )
            raise ValueError(f"Transfer initiation failed: {error_msg}")

        return response.json()

    def _import_acceptance_record(self, a_data):
        from django.contrib.auth import get_user_model

        from core.models import LicenseAcceptanceRecord

        User = get_user_model()

        license_version = a_data.get("license_version", "")
        license_checksum = a_data.get("license_checksum", "")
        accepted_at_str = a_data.get("_accepted_at")
        accepted_at = parse_datetime(accepted_at_str) if accepted_at_str else None

        # Deduplicate by license_version + checksum (accepted_at is auto_now_add
        # so we can't rely on it for matching — it always gets set to now())
        if (
            license_version
            and license_checksum
            and LicenseAcceptanceRecord.objects.filter(
                license_version=license_version,
                license_checksum=license_checksum,
            ).exists()
        ):
            return

        record = LicenseAcceptanceRecord()
        for f in ACCEPTANCE_FIELDS:
            if f in a_data:
                setattr(record, f, a_data[f])

        # Resolve accepted_by user by email
        email = a_data.get("accepted_by_email", "")
        if email:
            user = User.objects.filter(email=email).first()
            if user:
                record.accepted_by = user

        # Set installation_id from source data
        inst_id = a_data.get("_installation_id")
        if inst_id:
            import uuid as uuid_mod

            try:
                record.installation_id = uuid_mod.UUID(inst_id)
            except ValueError:
                pass

        record.save()

        # Override auto_now_add timestamp with the source's original value
        # (QuerySet.update() bypasses auto_now_add)
        if accepted_at:
            LicenseAcceptanceRecord.objects.filter(pk=record.pk).update(accepted_at=accepted_at)

    def generate_diff(self, remote_data):
        items = remote_data.get("items", [])
        if not items:
            return {"changes": [], "warnings": [], "summary": "No license data"}

        item = items[0]
        license_key = item.get("license_key", "?")
        acceptance_count = len(item.get("_acceptance_records", []))

        changes = [
            {
                "type": "transfer",
                "model": "PlatformLicense",
                "name": license_key,
                "fields": {
                    "license_type": item.get("license_type", ""),
                    "hosting_type": item.get("hosting_type", ""),
                    "source_installation_uuid": item.get("source_installation_uuid", ""),
                },
            }
        ]

        warnings = [
            "This will deactivate the license on the source installation. "
            "The source installation will stop working after transfer.",
        ]

        return {
            "changes": changes,
            "warnings": warnings,
            "summary": (
                f"License transfer for {license_key}, {acceptance_count} acceptance record(s)"
            ),
        }

    def snapshot_current(self):
        return self.export(credential_mode="skip")

    def restore_snapshot(self, snapshot):
        # License transfer cannot be reversed via snapshot restore.
        # The source must be re-activated manually via the update server.
        return {
            "restored": 0,
            "errors": [
                "License transfers cannot be automatically reversed. "
                "Contact support or re-activate the source installation manually."
            ],
        }
