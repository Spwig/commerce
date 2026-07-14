"""
License Acceptance Service

Manages the Software License Agreement acceptance flow.
This is separate from core/license.py (product license keys) —
this handles the legal agreement that merchants must accept before using Spwig.

Storage: {BASE_DIR}/license_acceptance.json (JSON, not executable Python)
Audit: LicenseAcceptanceRecord model in database
"""

import hashlib
import json
import logging
import os
import re
import time
import uuid
from datetime import UTC, datetime
from pathlib import Path

from django.conf import settings

logger = logging.getLogger(__name__)


class LicenseAcceptanceService:
    """
    Service class for managing Software License Agreement acceptance.

    Follows the singleton pattern used by LicenseManager in core/license.py.
    Uses a JSON file as primary storage (works before DB is configured)
    and a database model for audit trail.
    """

    # Class-level cache to minimize filesystem I/O
    _acceptance_cache = None
    _cache_time = 0
    CACHE_TTL = 60  # seconds

    def __init__(self):
        self.base_dir = Path(settings.BASE_DIR)
        self.license_path = self.base_dir / "LICENSE.txt"

        # Store acceptance alongside the license file on a persistent volume
        # so it survives container rebuilds / upgrades. Fall back to BASE_DIR
        # for dev environments where the license volume doesn't exist.
        license_dir = Path(
            getattr(settings, "LICENSE_PATH", "/opt/shop-platform/license/license.json")
        ).parent
        if license_dir.is_dir():
            self.acceptance_path = license_dir / "license_acceptance.json"
        else:
            self.acceptance_path = self.base_dir / "license_acceptance.json"

    def is_accepted(self) -> bool:
        """Check if the license agreement has been accepted."""
        # Check environment variable override (for Docker/CI)
        if os.environ.get("SPWIG_ACCEPT_LICENSE", "").lower() == "true":
            return True

        info = self._get_cached_acceptance()
        if info is None:
            return False
        return info.get("accepted", False)

    def needs_reacceptance(self) -> tuple[bool, str | None]:
        """
        Check if the license version has changed materially since acceptance.

        Returns:
            (needs_reaccept, change_type) where change_type is 'major' or None
        """
        if not self.is_accepted():
            return True, None

        info = self.get_acceptance_info()
        if not info:
            return True, None

        accepted_version = info.get("license_version", "0.0.0")
        current_version = self.get_current_license_version()

        if not current_version:
            return False, None

        try:
            accepted_parts = [int(x) for x in accepted_version.split(".")]
            current_parts = [int(x) for x in current_version.split(".")]

            # Major version bump requires re-acceptance
            if current_parts[0] > accepted_parts[0]:
                return True, "major"

        except (ValueError, IndexError):
            logger.warning(
                f"Could not parse license versions: accepted={accepted_version}, "
                f"current={current_version}"
            )

        return False, None

    def get_acceptance_info(self) -> dict | None:
        """Get the current acceptance record."""
        return self._get_cached_acceptance()

    def get_license_text(self) -> str:
        """Read the LICENSE.txt file."""
        if not self.license_path.exists():
            logger.error(f"LICENSE.txt not found at {self.license_path}")
            return ""

        try:
            with open(self.license_path, encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to read LICENSE.txt: {e}")
            return ""

    def get_current_license_version(self) -> str | None:
        """Extract version from LICENSE.txt header."""
        license_text = self.get_license_text()
        if not license_text:
            return None
        return self.extract_license_version(license_text)

    @staticmethod
    def extract_license_version(license_text: str) -> str | None:
        """Extract version string from license header."""
        match = re.search(r"Version:\s*(\d+\.\d+\.\d+)", license_text)
        return match.group(1) if match else None

    @staticmethod
    def compute_checksum(text: str) -> str:
        """Compute SHA-256 checksum of license text."""
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def record_acceptance(
        self,
        accepted_via: str = "web",
        ip_address: str | None = None,
        email: str = "",
        user=None,
    ) -> dict:
        """
        Record license acceptance to JSON file and database.

        Args:
            accepted_via: 'web', 'cli', or 'env'
            ip_address: Client IP address (for web acceptance)
            email: Admin email address
            user: Django User instance (if authenticated)

        Returns:
            The acceptance record dict
        """
        from core.version import __version__ as software_version

        license_text = self.get_license_text()
        license_version = self.extract_license_version(license_text) or "1.0.0"
        checksum = self.compute_checksum(license_text)
        installation_id = str(uuid.uuid4())

        acceptance_data = {
            "accepted": True,
            "license_version": license_version,
            "software_version": software_version,
            "timestamp": datetime.now(UTC).isoformat(),
            "accepted_via": accepted_via,
            "installation_id": installation_id,
            "license_checksum": f"sha256:{checksum}",
            "accepted_by_email": email,
            "ip_address": ip_address or "",
        }

        # Write JSON file
        self._write_acceptance_file(acceptance_data)

        # Write database record (best-effort, DB may not be available)
        self._write_db_record(acceptance_data, user)

        # Invalidate cache
        self._invalidate_cache()

        # Fire-and-forget phone-home (for re-acceptance of registered installations)
        try:
            self.phone_home(acceptance_data)
        except Exception:
            pass  # Silent failure — local acceptance is authoritative

        logger.info(
            f"License v{license_version} accepted via {accepted_via} by {email or 'unknown'}"
        )

        return acceptance_data

    def verify_integrity(self) -> bool:
        """Verify the accepted license hasn't been tampered with."""
        info = self.get_acceptance_info()
        if not info:
            return False

        license_text = self.get_license_text()
        if not license_text:
            return False

        current_checksum = self.compute_checksum(license_text)
        accepted_checksum = info.get("license_checksum", "").replace("sha256:", "")

        return current_checksum == accepted_checksum

    def phone_home(self, acceptance_data: dict | None = None):
        """
        Report license acceptance to the upgrade server.

        For fresh installs this is a no-op (no JWT yet) — the acceptance data
        is included in the next registration call instead.
        For re-acceptance of registered installations, reports immediately.
        """
        info = acceptance_data or self.get_acceptance_info()
        if not info or not info.get("accepted"):
            return

        try:
            from component_updates.models import UpdateServerConfig

            config = UpdateServerConfig.get_instance()
            if not config.jwt_token or not config.is_jwt_valid():
                return  # Will be sent during next registration

            import requests as http_requests

            response = http_requests.post(
                f"{config.server_url}/api/v1/license-acceptance/report/",
                json={
                    "license_version": info.get("license_version", ""),
                    "accepted_at": info.get("timestamp", ""),
                    "checksum": info.get("license_checksum", ""),
                    "accepted_via": info.get("accepted_via", ""),
                    "accepted_by_email": info.get("accepted_by_email", ""),
                },
                headers={"Authorization": f"Bearer {config.jwt_token}"},
                timeout=10,
            )
            response.raise_for_status()
            logger.info("License acceptance reported to upgrade server")
        except Exception as e:
            logger.warning(f"License acceptance phone-home failed: {e}")

    # --- Private methods ---

    def _get_cached_acceptance(self) -> dict | None:
        """Get acceptance info with class-level caching."""
        now = time.time()
        if (
            LicenseAcceptanceService._acceptance_cache is not None
            and (now - LicenseAcceptanceService._cache_time) < self.CACHE_TTL
        ):
            return LicenseAcceptanceService._acceptance_cache

        data = self._read_acceptance_file()
        LicenseAcceptanceService._acceptance_cache = data
        LicenseAcceptanceService._cache_time = now
        return data

    def _invalidate_cache(self):
        """Clear the class-level cache."""
        LicenseAcceptanceService._acceptance_cache = None
        LicenseAcceptanceService._cache_time = 0

    def _read_acceptance_file(self) -> dict | None:
        """Read the acceptance JSON file."""
        if not self.acceptance_path.exists():
            return None

        try:
            with open(self.acceptance_path, encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            logger.error(f"Failed to read license_acceptance.json: {e}")
            return None

    def _write_acceptance_file(self, data: dict):
        """Write the acceptance JSON file."""
        try:
            self.acceptance_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.acceptance_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except OSError as e:
            logger.error(f"Failed to write license_acceptance.json: {e}")
            raise

    def _write_db_record(self, data: dict, user=None):
        """Write acceptance record to database (best-effort)."""
        try:
            from core.models import LicenseAcceptanceRecord

            # Mark all previous records as not current
            LicenseAcceptanceRecord.objects.filter(is_current=True).update(is_current=False)

            # Create new record
            LicenseAcceptanceRecord.objects.create(
                license_version=data["license_version"],
                software_version=data["software_version"],
                accepted_by=user,
                accepted_by_email=data.get("accepted_by_email", ""),
                accepted_via=data["accepted_via"],
                installation_id=data["installation_id"],
                license_checksum=data["license_checksum"],
                ip_address=data.get("ip_address") or None,
                is_current=True,
            )
        except Exception as e:
            # Database may not be available (pre-migration, connection issues)
            logger.warning(f"Could not write license acceptance to database: {e}")


# Module-level singleton accessor
_license_acceptance_service = None


def get_license_acceptance_service() -> LicenseAcceptanceService:
    """Get the singleton LicenseAcceptanceService instance."""
    global _license_acceptance_service
    if _license_acceptance_service is None:
        _license_acceptance_service = LicenseAcceptanceService()
    return _license_acceptance_service
