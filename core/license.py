"""
License Management System
Handles license validation, feature flags, and trial mode.
"""

import base64
import json
import logging
import time
from datetime import datetime
from pathlib import Path

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone

import core

logger = logging.getLogger(__name__)


class LicenseManager:
    """
    Manages platform license validation and feature flags.

    Features:
    - RSA signature verification
    - License caching (30 days)
    - Trial mode support
    - Platform version compatibility checking
    - Feature flag management
    """

    CACHE_KEY = "platform_license_data"
    CACHE_TIMEOUT = 60 * 60 * 24 * 30  # 30 days
    VERSION_CACHE_KEY = "platform_current_major_version"
    VERSION_CACHE_TIMEOUT = 60 * 60 * 24  # 24 hours

    def __init__(self):
        self.license_path = getattr(
            settings, "LICENSE_PATH", "/opt/shop-platform/license/license.json"
        )
        self.public_key_path = Path(__file__).parent / "keys" / "license-public-key.pem"

        self._license_data = None
        self._is_valid = None
        self._validation_error = None

    def get_license_data(self) -> dict | None:
        """Get license data from cache or file"""
        if self._license_data:
            return self._license_data

        # Try cache first
        cached_data = cache.get(self.CACHE_KEY)
        if cached_data:
            self._license_data = cached_data
            return cached_data

        # Read from file
        license_path = Path(self.license_path)
        if not license_path.exists():
            logger.warning(f"License file not found at {self.license_path}")
            return None

        try:
            with open(license_path) as f:
                data = json.load(f)

            # Cache for 30 days
            cache.set(self.CACHE_KEY, data, self.CACHE_TIMEOUT)
            self._license_data = data
            return data
        except Exception as e:
            logger.error(f"Failed to read license file: {e}")
            return None

    def is_valid(self) -> bool:
        """Check if license is valid (cached result)"""
        if self._is_valid is not None:
            return self._is_valid

        valid, error = self.validate_license()
        self._is_valid = valid
        self._validation_error = error
        return valid

    def validate_license(self) -> tuple[bool, str | None]:
        """
        Validate license file completely.

        Returns:
            Tuple[bool, Optional[str]]: (is_valid, error_message)
        """
        # Check if license file exists
        license_data = self.get_license_data()
        if not license_data:
            return False, "License file not found"

        # Verify signature
        if not self.verify_signature(license_data):
            return False, "License signature verification failed"

        # Check if license is active
        license_info = license_data.get("license", {})
        if not license_info.get("is_active", True):
            return False, "License is not active"

        # Check expiration (for time-limited licenses)
        expires_at = license_info.get("expires_at")
        if expires_at:
            try:
                expiry_date = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
                if timezone.now() > expiry_date:
                    return False, "License has expired"
            except Exception as e:
                logger.error(f"Failed to parse expiration date: {e}")
                return False, "Invalid license expiration date"

        # Check platform version compatibility
        # Try entitlements first (new format), fall back to top-level field
        entitlements = license_info.get("entitlements", [])
        license_major = license_info.get("major_version", 1)
        for ent in entitlements:
            if ent.get("slug") == "major_version" and ent.get("value_type") == "numeric":
                license_major = ent.get("value", license_major)
                break

        platform_major = core.__version_info__[0]

        # Exact match: license must cover the current major version
        if platform_major > license_major:
            return False, (
                f"License is for platform v{license_major}.x, you are running v{platform_major}.x. "
                f"Please purchase a version upgrade."
            )

        # Check for pending revocation past grace period
        try:
            from core.models import LicenseRevocation

            revocation = LicenseRevocation.objects.order_by("-detected_at").first()
            if revocation and not revocation.is_in_grace_period:
                return False, (
                    f"License has been revoked: {revocation.reason}. "
                    f"Please contact support or re-activate your license."
                )
        except Exception:
            pass  # Don't fail validation if revocation table doesn't exist yet

        return True, None

    def verify_signature(self, license_data: dict) -> bool:
        """
        Verify RSA signature of license file.

        Args:
            license_data: Full license JSON data including signature

        Returns:
            bool: True if signature is valid
        """
        try:
            # Extract signature
            signature_b64 = license_data.get("signature", "")
            if not signature_b64:
                logger.error("No signature found in license file")
                return False

            signature = base64.b64decode(signature_b64)

            # Get license data without signature for verification
            license_content = license_data.get("license", {})
            license_json = json.dumps(license_content, sort_keys=True).encode()

            # Load public key
            if not self.public_key_path.exists():
                logger.error(f"Public key not found at {self.public_key_path}")
                return False

            with open(self.public_key_path, "rb") as f:
                public_key = serialization.load_pem_public_key(f.read())

            # Verify signature
            public_key.verify(
                signature,
                license_json,
                padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                hashes.SHA256(),
            )

            return True

        except InvalidSignature:
            logger.error("License signature verification failed: Invalid signature")
            return False
        except Exception as e:
            logger.error(f"License signature verification failed: {e}")
            return False

    def get_license_type(self) -> str:
        """Get license type (unlicensed, standard, enterprise)"""
        if not self.is_valid():
            return "unlicensed"

        license_data = self.get_license_data()
        if not license_data:
            return "unlicensed"

        return license_data.get("license", {}).get("license_type", "standard")

    def get_environment_type(self) -> str:
        """Get the environment type from the license file."""
        license_data = self.get_license_data()
        if not license_data:
            return "development"  # No license = developer environment
        return license_data.get("license", {}).get("environment_type", "production")

    def is_sandbox(self) -> bool:
        """
        Determine if this installation is running in sandbox mode.

        Sandbox mode is active when the signed licence has
        environment_type in ('development', 'staging', 'sandbox').

        A missing licence file is no longer treated as sandbox — the Community
        edition auto-bootstrapped at startup covers that path with a real
        production licence. Only explicit dev/staging licences trigger sandbox.

        Result is cached alongside license data (30-day cache via get_license_data).
        """
        license_data = self.get_license_data()
        if not license_data:
            return False  # No licence = platform is unbootstrapped; not sandbox

        license_info = license_data.get("license", {})
        env_type = license_info.get("environment_type", "production")
        return env_type in ("development", "staging", "sandbox")

    def get_edition(self) -> str:
        """
        Get the platform edition.

        Returns:
            'community' - Community edition (default OSS build)
            'pro'       - Paid Pro licence
            'enterprise'- Paid Enterprise licence
            'unlicensed'- No valid licence found (should not happen after bootstrap)
        """
        if not self.is_valid():
            return "unlicensed"

        license_data = self.get_license_data()
        if not license_data:
            return "unlicensed"

        license_info = license_data.get("license", {})

        # Prefer entitlement (new format)
        for ent in license_info.get("entitlements", []):
            if ent.get("slug") == "edition":
                return ent.get("value", "community")

        # Fall back to top-level 'edition' field
        return license_info.get("edition", "community")

    def is_community(self) -> bool:
        """Check if this is the Community edition (default OSS build)."""
        return self.get_edition() == "community"

    def get_enforcement_state(self) -> str:
        """
        Get the current enforcement state.

        Returns:
            'licensed' - Valid license exists
            'grace_period' - No license but within 14-day grace period
            'warning_phase' - No license, days 15-21
            'locked_out' - No license, day 22+
        """
        if self.is_valid():
            return "licensed"

        from core.license_grace import get_grace_period_status

        grace = get_grace_period_status()
        return grace.enforcement_state

    def has_feature(self, feature_name: str) -> bool:
        """
        Check if a feature is enabled for this license.

        Checks entitlements list first (new format), falls back to features dict (legacy).
        After lockout (day 22+), all features are disabled.

        Args:
            feature_name: Feature to check (e.g., 'payment_processing')

        Returns:
            bool: True if feature is enabled
        """
        if not self.is_valid():
            # Grace/warning period: all features available (sandbox payments via PaymentGuard);
            # after lockout: all features disabled.
            return self.get_enforcement_state() != "locked_out"

        license_data = self.get_license_data()
        if not license_data:
            return feature_name != "payment_processing"

        license_info = license_data.get("license", {})

        # Check entitlements list first (new format)
        entitlements = license_info.get("entitlements", [])
        if entitlements:
            for ent in entitlements:
                if ent.get("slug") == feature_name:
                    if ent.get("value_type") == "boolean":
                        return ent.get("value", False)
                    return True  # numeric entitlements are "present" = enabled

        # Fall back to features dict (legacy format)
        features = license_info.get("features", {})
        return features.get(feature_name, False)

    def get_entitlement_value(self, slug: str, default=None):
        """
        Get the value of an entitlement by slug.

        For boolean entitlements, returns True/False.
        For numeric entitlements, returns the numeric value.

        Args:
            slug: Entitlement slug (e.g., 'staging_slots')
            default: Default value if entitlement not found

        Returns:
            The entitlement value, or default
        """
        license_data = self.get_license_data()
        if not license_data:
            return default

        entitlements = license_data.get("license", {}).get("entitlements", [])
        for ent in entitlements:
            if ent.get("slug") == slug:
                return ent.get("value", default)

        return default

    # ================================================================
    # Maintenance Status
    # ================================================================

    MAINTENANCE_GRACE_DAYS = 30

    def get_maintenance_status(self) -> dict:
        """
        Get maintenance status from signed license data.

        Returns dict with:
            active: bool - Is maintenance currently active (not expired)?
            expires_at: datetime or None - When maintenance expires
            days_remaining: int or None - Days until maintenance expires (None if perpetual)
            in_grace_period: bool - Is within 30-day grace after expiry?
            grace_days_remaining: int - Days left in grace period (0 if not in grace)
        """
        license_data = self.get_license_data()
        if not license_data:
            return {
                "active": False,
                "expires_at": None,
                "days_remaining": 0,
                "in_grace_period": False,
                "grace_days_remaining": 0,
            }

        license_info = license_data.get("license", {})

        # Read top-level convenience fields (set by update server)
        maintenance_active = license_info.get("maintenance_active")
        maintenance_expires_str = license_info.get("maintenance_expires_at")

        # Fallback: check entitlements list for older license.json files
        if maintenance_active is None:
            for ent in license_info.get("entitlements", []):
                if ent.get("slug") == "maintenance_active":
                    maintenance_active = ent.get("value", True)
                    maintenance_expires_str = ent.get("expires_at")
                    break
            # Old licenses without maintenance field = active (backward compat)
            if maintenance_active is None:
                maintenance_active = True

        # Parse expiration and compute grace period
        expires_at = None
        in_grace = False
        grace_days_remaining = 0
        days_remaining = None

        if maintenance_expires_str:
            try:
                expires_at = datetime.fromisoformat(maintenance_expires_str.replace("Z", "+00:00"))
                now = timezone.now()
                if now <= expires_at:
                    days_remaining = (expires_at - now).days
                else:
                    # Maintenance expired
                    maintenance_active = False
                    days_past = (now - expires_at).days
                    if days_past <= self.MAINTENANCE_GRACE_DAYS:
                        in_grace = True
                        grace_days_remaining = self.MAINTENANCE_GRACE_DAYS - days_past
            except (ValueError, TypeError) as e:
                logger.error(f"Failed to parse maintenance_expires_at: {e}")

        return {
            "active": maintenance_active,
            "expires_at": expires_at,
            "days_remaining": days_remaining,
            "in_grace_period": in_grace,
            "grace_days_remaining": grace_days_remaining,
        }

    # Services that Community edition is allowed to call (rate-limited by the
    # hosted service; the server returns 429 with an upgrade CTA once the
    # Community-tier quota is exceeded). Mail gateway stays paid-only.
    _COMMUNITY_AVAILABLE_SERVICES = {"geoip", "geocoder", "push"}

    def is_hosted_service_available(self, service: str) -> bool:
        """
        Per-service availability for the Spwig-hosted stack.

        Community edition can call ``geoip``/``geocoder``/``push`` — those
        services enforce a Community-tier rate limit at ingress and return 429
        with an ``upgrade_url`` once the quota is hit. ``mail_gateway`` remains
        paid-only.

        Paid tiers keep the previous behaviour (maintenance-status gated).

        Args:
            service: one of ``'geoip'``, ``'geocoder'``, ``'push'``,
                     ``'mail_gateway'``.
        """
        if self.is_sandbox():
            return True  # Dev/staging installs always allowed
        if self.is_community():
            return service in self._COMMUNITY_AVAILABLE_SERVICES
        status = self.get_maintenance_status()
        return status["active"] or status["in_grace_period"]

    def are_spwig_services_available(self) -> bool:
        """
        Legacy blanket check — retained for callers that haven't been migrated
        to :py:meth:`is_hosted_service_available`. Prefer the per-service
        method for new code; this one is conservative (returns True only when
        *all* of GeoIP, Geocoder, Push are available).

        Community edition returns True here because it can now call the three
        rate-limited services. Mail gateway callers should migrate to the
        per-service check.
        """
        if self.is_sandbox():
            return True  # Services always available in sandbox/dev
        if self.is_community():
            return True  # Community can call GeoIP/Geocoder/Push (rate-limited)
        status = self.get_maintenance_status()
        return status["active"] or status["in_grace_period"]

    # ================================================================
    # Hosting Type & Subscription Status
    # ================================================================

    def get_hosting_type(self) -> str:
        """
        Get the hosting type for this installation.

        Returns 'self_hosted' or 'spwig_hosted'.
        Defaults to 'self_hosted' for older license files without this field.
        """
        license_data = self.get_license_data()
        if not license_data:
            return "self_hosted"
        return license_data.get("license", {}).get("hosting_type", "self_hosted")

    def is_spwig_hosted(self) -> bool:
        """Check if this is a Spwig-hosted subscription installation."""
        return self.get_hosting_type() == "spwig_hosted"

    def is_shared_fleet(self) -> bool:
        """Check if this is a shared fleet (Starter/Growth) hosted installation."""
        from django.conf import settings

        return self.is_spwig_hosted() and settings.HOSTING_INFRA_TIER == "shared"

    def get_account_status(self) -> str:
        """
        Get the account/subscription status.

        Returns one of: 'active', 'past_due', 'grace_period', 'suspended',
        'read_only', 'expired', 'cancelled'.
        Defaults to 'active' for older license files without this field.
        """
        license_data = self.get_license_data()
        if not license_data:
            return "active"
        return license_data.get("license", {}).get("account_status", "active")

    def get_subscription_plan(self) -> dict | None:
        """
        Get subscription plan info from the license data.

        Returns a dict with 'slug', 'name', 'quotas' or None if no plan
        is assigned (self-hosted or older license files).
        """
        license_data = self.get_license_data()
        if not license_data:
            return None
        return license_data.get("license", {}).get("subscription_plan")

    def get_plan_quota(self, quota_key: str, default=None):
        """
        Get a specific quota value from the subscription plan.

        Args:
            quota_key: Quota identifier (e.g., 'max_products', 'max_storage_gb')
            default: Default value if quota not found or no plan assigned

        Returns:
            The quota value, or default
        """
        plan = self.get_subscription_plan()
        if not plan:
            return default
        return plan.get("quotas", {}).get(quota_key, default)

    def get_license_info(self) -> dict:
        """
        Get complete license information for display.

        Returns:
            Dict with license details and validation status
        """
        is_valid = self.is_valid()
        license_data = self.get_license_data()
        enforcement_state = self.get_enforcement_state()

        # Get grace period info
        from core.license_grace import get_grace_period_status

        grace = get_grace_period_status()

        if not license_data:
            return {
                "is_valid": False,
                "is_sandbox": True,
                "environment_type": "development",
                "license_type": "unlicensed",
                "hosting_type": "self_hosted",
                "account_status": "active",
                "subscription_plan": None,
                "is_hosted": False,
                "error": "No license file found",
                "features": {
                    "payment_processing": False,
                },
                "entitlements": [],
                "entitlements_grouped": {},
                "platform_version": core.__version__,
                "trial_mode": True,
                "enforcement_state": enforcement_state,
                "grace_days_remaining": grace.days_remaining,
                "grace_days_elapsed": grace.days_elapsed,
                "installed_at": grace.installed_at,
            }

        license_info = license_data.get("license", {})

        # Parse entitlements if present, group by category
        entitlements = license_info.get("entitlements", [])
        entitlements_grouped = {}
        for ent in entitlements:
            category = ent.get("category", "platform")
            if category not in entitlements_grouped:
                entitlements_grouped[category] = []
            entitlements_grouped[category].append(ent)

        # Get maintenance status
        maintenance = self.get_maintenance_status()

        return {
            "is_valid": is_valid,
            "is_sandbox": self.is_sandbox(),
            "environment_type": license_info.get("environment_type", "production"),
            "license_type": license_info.get("license_type", "unknown"),
            "hosting_type": self.get_hosting_type(),
            "account_status": self.get_account_status(),
            "subscription_plan": self.get_subscription_plan(),
            "is_hosted": self.is_spwig_hosted(),
            "license_key": license_info.get("license_key", "N/A"),
            "owner_name": license_info.get("owner_name", "N/A"),
            "owner_email": license_info.get("owner_email", "N/A"),
            "company": license_info.get("company", ""),
            "issue_date": license_info.get("issue_date", "N/A"),
            "expires_at": license_info.get("expires_at"),
            "major_version": license_info.get("major_version", 1),
            "max_installations": license_info.get("max_installations", 1),
            "features": license_info.get("features", {}),
            "entitlements": entitlements,
            "entitlements_grouped": entitlements_grouped,
            "platform_version": core.__version__,
            "error": self._validation_error,
            "trial_mode": not is_valid,
            "enforcement_state": enforcement_state,
            "grace_days_remaining": grace.days_remaining,
            "grace_days_elapsed": grace.days_elapsed,
            "installed_at": grace.installed_at,
            # Maintenance status
            "maintenance_active": maintenance["active"],
            "maintenance_expires_at": maintenance["expires_at"],
            "maintenance_days_remaining": maintenance["days_remaining"],
            "maintenance_in_grace_period": maintenance["in_grace_period"],
            "maintenance_grace_days_remaining": maintenance["grace_days_remaining"],
            "spwig_services_available": self.are_spwig_services_available(),
            # Revocation status
            **self._get_revocation_info(),
        }

    def _get_revocation_info(self) -> dict:
        """Get pending revocation info for license display."""
        try:
            from core.models import LicenseRevocation

            revocation = LicenseRevocation.objects.order_by("-detected_at").first()
            if revocation:
                return {
                    "revocation_pending": revocation.is_in_grace_period,
                    "revocation_reason": revocation.reason,
                    "revocation_grace_days_remaining": revocation.grace_days_remaining,
                    "revocation_detected_at": revocation.detected_at.isoformat(),
                    "revocation_acknowledged": revocation.acknowledged,
                }
        except Exception:
            pass
        return {
            "revocation_pending": False,
            "revocation_reason": None,
            "revocation_grace_days_remaining": 0,
            "revocation_detected_at": None,
            "revocation_acknowledged": False,
        }

    def _get_current_major_from_update_server(self) -> int | None:
        """
        Fetch the latest platform major version from the update server.

        Results are cached for 24 hours. Returns None if the update server
        is unreachable or not configured.
        """
        cached = cache.get(self.VERSION_CACHE_KEY)
        if cached is not None:
            return cached

        try:
            from component_updates.models import UpdateServerConfig
            from component_updates.services import PlatformUpdateService

            config = UpdateServerConfig.get_instance()
            if not config.server_url or not config.license_key:
                logger.debug("Update server not configured, skipping version check")
                return None

            service = PlatformUpdateService()
            update_info = service.check_for_update(channel="stable")

            # latest_version is only present when an update is available;
            # otherwise current_version indicates we're already at the latest
            version_str = (
                update_info.get("latest_version") or update_info.get("current_version") or ""
            )
            if version_str:
                major = int(version_str.split(".")[0])
                cache.set(self.VERSION_CACHE_KEY, major, self.VERSION_CACHE_TIMEOUT)
                logger.debug(f"Cached current major version from update server: {major}")
                return major

        except Exception as e:
            logger.debug(f"Failed to get current version from update server: {e}")

        return None

    def check_version_support(self) -> tuple[bool, str]:
        """
        Check if current platform version receives updates.

        Returns:
            Tuple[bool, str]: (updates_available, reason)
                - full_updates: Current version, all updates
                - maintenance_updates: Previous version, security + bugfixes
                - end_of_life: 2+ versions behind, no updates
        """
        platform_major = core.__version_info__[0]

        # Get latest major version from update server (cached 24h)
        current_major = self._get_current_major_from_update_server()
        if current_major is None:
            # Fallback: assume this platform's own version is current
            current_major = platform_major

        if platform_major == current_major:
            return True, "full_updates"
        elif platform_major == current_major - 1:
            return True, "maintenance_updates"
        else:
            return False, "end_of_life"

    def clear_cache(self):
        """Clear cached license data and grace period cache"""
        cache.delete(self.CACHE_KEY)
        cache.delete(self.VERSION_CACHE_KEY)
        self._license_data = None
        self._is_valid = None
        self._validation_error = None
        # Also clear grace period cache so it recalculates
        from core.license_grace import clear_grace_period_cache

        clear_grace_period_cache()


# Singleton instance
_license_manager = None

# Cross-worker invalidation: when any worker reloads the license manager
# (e.g. after activation), it sets a reload epoch in Redis. Other gunicorn
# workers periodically check this epoch and recreate their singleton when
# it changes, ensuring license status consistency across all workers.
RELOAD_EPOCH_KEY = "license_manager_reload_epoch"
RELOAD_EPOCH_TTL = 60 * 60 * 24 * 7  # 7 days
EPOCH_CHECK_INTERVAL = 5  # seconds between Redis epoch checks per worker

_manager_epoch = None
_last_epoch_check = 0.0


def get_license_manager(force_reload: bool = False) -> LicenseManager:
    """
    Get singleton LicenseManager instance.

    Periodically checks a Redis epoch key so that when one gunicorn worker
    reloads the license (e.g. after activation), all other workers detect
    the change and recreate their singletons within EPOCH_CHECK_INTERVAL.

    Args:
        force_reload: If True, creates a new instance (useful after license changes)
    """
    global _license_manager, _manager_epoch, _last_epoch_check

    # Periodically check if another worker triggered a reload
    if not force_reload and _license_manager is not None:
        now = time.monotonic()
        if now - _last_epoch_check > EPOCH_CHECK_INTERVAL:
            _last_epoch_check = now
            try:
                current_epoch = cache.get(RELOAD_EPOCH_KEY)
                if current_epoch is not None and current_epoch != _manager_epoch:
                    logger.info("License reload epoch changed — reloading singleton")
                    force_reload = True
                    # Grace period cache depends on license validity; clear it
                    # so it recomputes with the fresh singleton.
                    from core.license_grace import clear_grace_period_cache

                    clear_grace_period_cache()
            except Exception:
                pass  # Redis unavailable — skip epoch check

    if _license_manager is None or force_reload:
        _license_manager = LicenseManager()
        try:
            _manager_epoch = cache.get(RELOAD_EPOCH_KEY)
        except Exception:
            _manager_epoch = None
        _last_epoch_check = time.monotonic()

    return _license_manager


def reload_license_manager():
    """Force reload the license manager singleton (use after license activation/removal)"""
    global _license_manager, _manager_epoch, _last_epoch_check
    # Clear Redis cache from old instance before destroying it
    if _license_manager is not None:
        _license_manager.clear_cache()
    else:
        # No instance exists - clear Redis cache directly
        cache.delete(LicenseManager.CACHE_KEY)
        from core.license_grace import clear_grace_period_cache

        clear_grace_period_cache()

    # Signal all workers to reload by setting a new epoch in Redis
    new_epoch = str(time.time())
    try:
        cache.set(RELOAD_EPOCH_KEY, new_epoch, RELOAD_EPOCH_TTL)
    except Exception:
        logger.warning("Failed to set license reload epoch in Redis")

    _license_manager = None
    # get_license_manager() will read the epoch back from Redis and set
    # _manager_epoch + _last_epoch_check when it creates the new instance.
    return get_license_manager(force_reload=True)


def is_sandbox_mode() -> bool:
    """
    Quick check: is this installation running in sandbox mode?

    Sandbox mode is active when there is no license file (free developer sandbox)
    or the license was activated with a non-production environment type.

    Usage:
        from core.license import is_sandbox_mode
        if is_sandbox_mode():
            # restrict behavior
    """
    return get_license_manager().is_sandbox()
