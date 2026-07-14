"""
Component Update Services
Handles component update operations, version management, and rollback functionality.
"""

import hashlib
import json
import logging
import shutil
import tempfile
import zipfile
from datetime import timedelta
from pathlib import Path

import requests
from django.conf import settings
from django.db import transaction
from django.utils import timezone

from .models import (
    ComponentDependency,
    ComponentRegistry,
    ComponentVersion,
    UpdateLog,
    UpdateServerConfig,
)

logger = logging.getLogger(__name__)


class UpdateAuthenticationError(Exception):
    """Raised when authentication with update server fails"""

    pass


class UpdateDownloadError(Exception):
    """Raised when component download fails"""

    pass


class UpdateInstallError(Exception):
    """Raised when component installation fails"""

    pass


class DependencyError(Exception):
    """Raised when dependency resolution fails"""

    pass


class UpdateManager:
    """
    Centralized service for managing component updates.

    Handles:
    - Checking for available updates
    - Downloading component packages
    - Installing/updating components
    - Rolling back to previous versions
    - Health checking after updates
    - Dependency resolution
    """

    def __init__(self):
        self.config = UpdateServerConfig.get_instance()
        self.session = requests.Session()
        self.session.headers.update(
            {"User-Agent": "ShopPlatform/1.0", "Accept": "application/json"}
        )

    def _calculate_checksum(self, file_path: Path) -> str:
        """
        Calculate SHA256 checksum of a file.

        Args:
            file_path: Path to file

        Returns:
            str: SHA256 hex digest
        """
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()

    def _ensure_authenticated(self) -> bool:
        """
        Ensure we have a valid JWT token for the update server.
        Refreshes token if expired or missing.

        Returns:
            bool: True if authenticated successfully

        Raises:
            UpdateAuthenticationError: If authentication fails
        """
        if not self.config.server_url:
            raise UpdateAuthenticationError("Update server URL not configured")

        # Check if we have a valid token
        if self.config.is_jwt_valid():
            self.session.headers.update({"Authorization": f"Bearer {self.config.jwt_token}"})
            # Even with valid token, ensure platform secrets are initialized
            self._ensure_platform_secrets_initialized()
            return True

        # Need to authenticate
        logger.info("JWT token expired or missing, authenticating with update server...")

        try:
            from core.license import get_license_manager, is_sandbox_mode

            license_manager = get_license_manager()

            # Community edition installations self-register with the synthetic
            # licence key. The paid `self.config.license_key` is unset for
            # Community installs so we can't send that.
            if license_manager.is_community() and not self.config.license_key:
                effective_license_key = "COMMUNITY-EDITION"
            else:
                effective_license_key = self.config.license_key

            registration_data = {
                "installation_uuid": str(self.config.installation_uuid),
                "platform_version": getattr(settings, "PLATFORM_VERSION", "1.0.0"),
                "license_key": effective_license_key,
                "is_sandbox": is_sandbox_mode(),
                "environment_type": license_manager.get_environment_type(),
            }

            # Include domain from Sites framework for server-side tracking
            try:
                from django.contrib.sites.models import Site

                registration_data["domain"] = Site.objects.get(pk=1).domain
            except Exception:
                pass

            # Include license acceptance data for phone-home
            try:
                from core.license_acceptance import get_license_acceptance_service

                acceptance_service = get_license_acceptance_service()
                acceptance_info = acceptance_service.get_acceptance_info()
                if acceptance_info and acceptance_info.get("accepted"):
                    registration_data["license_acceptance"] = {
                        "license_version": acceptance_info.get("license_version", ""),
                        "accepted_at": acceptance_info.get("timestamp", ""),
                        "checksum": acceptance_info.get("license_checksum", ""),
                        "accepted_via": acceptance_info.get("accepted_via", ""),
                        "accepted_by_email": acceptance_info.get("accepted_by_email", ""),
                    }
            except Exception:
                pass  # Don't block registration if acceptance read fails

            response = self.session.post(
                f"{self.config.server_url}/api/v1/auth/register/",
                json=registration_data,
                timeout=10,
            )

            # Surface clear error for installation UUID mismatch
            if response.status_code == 404:
                logger.error(
                    f"❌ Installation UUID {self.config.installation_uuid} is not registered "
                    f"on the update server. Re-activate your license via Admin > License Status "
                    f"to register this installation."
                )

            response.raise_for_status()

            data = response.json()

            # Store the JWT token
            self.config.jwt_token = data["token"]
            self.config.jwt_expires_at = timezone.now() + timedelta(
                seconds=data.get("expires_in", 3600)
            )
            self.config.save()

            # Store service secrets if returned (per-installation secrets for platform services)
            service_secrets = data.get("service_secrets")
            if service_secrets:
                self._store_service_secrets(service_secrets, data.get("installation_uuid"))
                logger.info("✅ Service secrets stored from license server")
            else:
                # For existing installations, fetch secrets from dedicated endpoint
                self._fetch_service_secrets()

            # Auto-configure POS license if returned by update server
            pos_license_key = data.get("pos_license_key")
            if pos_license_key and pos_license_key != self.config.pos_license_key:
                self.config.pos_license_key = pos_license_key
                self.config.pos_license_status = "active"
                self.config.pos_license_validated_at = timezone.now()
                self.config.save(
                    update_fields=[
                        "pos_license_key",
                        "pos_license_status",
                        "pos_license_validated_at",
                    ]
                )
                # Clear any cached POS validation result
                try:
                    from pos_app.license import clear_pos_license_cache

                    clear_pos_license_cache()
                except ImportError:
                    pass
                logger.info("✅ POS license auto-configured from update server")

            # Update session headers
            self.session.headers.update({"Authorization": f"Bearer {self.config.jwt_token}"})

            logger.info("✅ Successfully authenticated with update server")
            return True

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Failed to authenticate with update server: {e}")
            raise UpdateAuthenticationError(f"Authentication failed: {e}")

    def _store_service_secrets(self, service_secrets: dict, installation_uuid: str | None = None):
        """
        Store service secrets from license server in PlatformSecrets model.

        Args:
            service_secrets: Dict with keys 'geoip', 'push', 'sso'
            installation_uuid: Optional installation UUID from server
        """
        import uuid

        from core.models import PlatformSecrets

        try:
            secrets = PlatformSecrets.get_secrets()

            # Store JWT secrets for each service
            if "geoip" in service_secrets:
                secrets.geoip_jwt_secret = service_secrets["geoip"]
            if "push" in service_secrets:
                secrets.push_jwt_secret = service_secrets["push"]
            if "sso" in service_secrets:
                secrets.sso_jwt_secret = service_secrets["sso"]

            # Store installation UUID if provided
            if installation_uuid:
                try:
                    secrets.installation_uuid = uuid.UUID(installation_uuid)
                except (ValueError, TypeError):
                    logger.warning(f"Invalid installation UUID format: {installation_uuid}")

            # Store license server tokens for future refresh
            secrets.license_server_token = self.config.jwt_token
            secrets.token_expires_at = self.config.jwt_expires_at
            secrets.secrets_fetched_at = timezone.now()

            secrets.save()
            logger.info(
                f"✅ Platform secrets updated: geoip={bool(secrets.geoip_jwt_secret)}, push={bool(secrets.push_jwt_secret)}, sso={bool(secrets.sso_jwt_secret)}"
            )

        except Exception as e:
            logger.error(f"❌ Failed to store service secrets: {e}")

    def _ensure_platform_secrets_initialized(self):
        """
        Ensure platform secrets are initialized.
        Fetches from license server if not already stored in database.
        """
        from core.models import PlatformSecrets

        try:
            secrets = PlatformSecrets.get_secrets()
            if not secrets.is_initialized:
                logger.info("Platform secrets not initialized, fetching from license server...")
                self._fetch_service_secrets()
        except Exception as e:
            logger.warning(f"Could not check platform secrets initialization: {e}")

    def _fetch_service_secrets(self):
        """
        Fetch service secrets from the dedicated endpoint.
        Used for existing installations that registered before service_secrets were added.
        """
        try:
            response = self.session.get(
                f"{self.config.server_url}/api/v1/auth/service-secrets/",
                headers={"Authorization": f"Bearer {self.config.jwt_token}"},
                timeout=10,
            )

            if response.status_code == 200:
                data = response.json()
                service_secrets = data.get("service_secrets")
                if service_secrets:
                    self._store_service_secrets(service_secrets, data.get("installation_uuid"))
                    logger.info("✅ Service secrets fetched from dedicated endpoint")
                else:
                    logger.warning("⚠️ Service secrets endpoint returned empty secrets")
            elif response.status_code == 404:
                logger.debug("Service secrets endpoint not available on this server version")
            else:
                logger.warning(f"⚠️ Failed to fetch service secrets: HTTP {response.status_code}")

        except requests.exceptions.RequestException as e:
            logger.warning(f"⚠️ Could not fetch service secrets: {e}")

    def refresh_license(self, force_write: bool = False) -> dict:
        """
        Refresh license.json from the update server.

        Calls the license refresh endpoint to get a freshly signed license
        with current entitlements and maintenance status.

        Args:
            force_write: Write license.json even if data hasn't changed

        Returns:
            Dict with keys:
                - refreshed: bool (True if license.json was updated)
                - changes: list of changed field names
                - maintenance_status: dict from server
                - error: str if refresh failed (network issues, etc.)
        """
        from core.activation import write_license_file
        from core.license import get_license_manager, is_sandbox_mode, reload_license_manager

        # Skip in sandbox mode (no license file)
        if is_sandbox_mode():
            return {"refreshed": False, "changes": [], "error": "sandbox_mode"}

        try:
            self._ensure_authenticated()
        except Exception as e:
            logger.warning(f"License refresh: authentication failed: {e}")
            return {"refreshed": False, "changes": [], "error": f"auth_failed: {e}"}

        try:
            # Include usage metrics for abuse detection
            request_body = {}
            try:
                request_body["usage_metrics"] = self._collect_usage_metrics()
            except Exception as e:
                logger.debug(f"Could not collect usage metrics: {e}")

            response = self.session.post(
                f"{self.config.server_url}/api/v1/licenses/refresh/", json=request_body, timeout=30
            )

            # Handle revocation/expiry
            if response.status_code == 403:
                data = response.json()
                error_code = data.get("error", "")

                if error_code in ("license_revoked", "license_expired"):
                    logger.warning(f"License refresh: {error_code} — {data.get('message', '')}")
                    self._handle_license_revocation(error_code, data.get("message", ""))
                    return {
                        "refreshed": False,
                        "changes": [],
                        "error": error_code,
                        "message": data.get("message", ""),
                    }

                return {"refreshed": False, "changes": [], "error": f"forbidden: {data}"}

            if response.status_code != 200:
                logger.warning(f"License refresh: HTTP {response.status_code}")
                return {"refreshed": False, "changes": [], "error": f"http_{response.status_code}"}

            data = response.json()
            if not data.get("success"):
                return {"refreshed": False, "changes": [], "error": data.get("error", "unknown")}

            new_license_data = {
                "license": data["license"],
                "signature": data["signature"],
            }

            # Verify signature locally before writing
            license_manager = get_license_manager()
            if not license_manager.verify_signature(new_license_data):
                logger.error("License refresh: signature verification failed")
                return {"refreshed": False, "changes": [], "error": "signature_verification_failed"}

            # Compare with current license data
            current_data = license_manager.get_license_data()
            changes = []
            if current_data and current_data.get("license"):
                current_license = current_data["license"]
                new_license = data["license"]
                for key in (
                    "maintenance_active",
                    "maintenance_expires_at",
                    "is_active",
                    "license_type",
                    "product_type",
                    "max_installations",
                    "entitlements",
                    "features",
                    "expires_at",
                ):
                    old_val = current_license.get(key)
                    new_val = new_license.get(key)
                    if old_val != new_val:
                        changes.append(key)

            # Write if changed or forced
            if changes or force_write or not current_data:
                write_license_file(new_license_data)
                reload_license_manager()
                logger.info(f"License refreshed — changes: {changes or ['force_write']}")
            else:
                logger.debug("License refresh: no changes detected")

            # Clear any pending revocation since license is valid
            self._clear_license_revocation()

            # Update service secrets if returned
            service_secrets = data.get("service_secrets")
            if service_secrets:
                self._store_service_secrets(service_secrets)

            # Update POS license key if changed
            pos_key = data.get("pos_license_key")
            if pos_key and pos_key != self.config.pos_license_key:
                self.config.pos_license_key = pos_key
                self.config.pos_license_status = "active"
                self.config.pos_license_validated_at = timezone.now()
                self.config.save(
                    update_fields=[
                        "pos_license_key",
                        "pos_license_status",
                        "pos_license_validated_at",
                    ]
                )
                try:
                    from pos_app.license import clear_pos_license_cache

                    clear_pos_license_cache()
                except ImportError:
                    pass

            return {
                "refreshed": bool(changes) or force_write,
                "changes": changes,
                "maintenance_status": data.get("maintenance_status", {}),
            }

        except requests.exceptions.RequestException as e:
            logger.warning(f"License refresh: network error: {e}")
            return {"refreshed": False, "changes": [], "error": f"network: {e}"}
        except Exception as e:
            logger.error(f"License refresh: unexpected error: {e}", exc_info=True)
            return {"refreshed": False, "changes": [], "error": str(e)}

    def _handle_license_revocation(self, error_code: str, message: str):
        """Record a license revocation detected during refresh."""
        from core.models import LicenseRevocation

        # Only create if no existing pending revocation
        if not LicenseRevocation.objects.filter(grace_expires_at__gt=timezone.now()).exists():
            grace_days = getattr(settings, "LICENSE_REVOCATION_GRACE_DAYS", 7)
            LicenseRevocation.objects.create(
                reason=f"{error_code}: {message}",
                grace_expires_at=timezone.now() + timedelta(days=grace_days),
            )
            logger.warning(
                f"License revocation recorded: {error_code}. Grace period: {grace_days} days."
            )

    def _clear_license_revocation(self):
        """Clear any pending revocation since license is confirmed valid."""
        from core.models import LicenseRevocation

        deleted, _ = LicenseRevocation.objects.all().delete()
        if deleted:
            logger.info("License revocation cleared — license confirmed valid by server")

    @staticmethod
    def _collect_usage_metrics() -> dict:
        """
        Collect lightweight usage metrics for telemetry.

        Sent with the license refresh request to help detect
        dev-license abuse (production-like usage on free licenses).
        """
        from django.contrib.auth import get_user_model

        User = get_user_model()

        metrics = {}

        try:
            from catalog.models import Product

            metrics["product_count"] = Product.objects.count()
        except Exception:
            pass

        try:
            from orders.models import Order

            metrics["order_count"] = Order.objects.count()
        except Exception:
            pass

        try:
            metrics["customer_count"] = User.objects.filter(
                is_staff=False, is_superuser=False
            ).count()
        except Exception:
            pass

        return metrics

    def list_available_components(
        self,
        component_type: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
        search: str | None = None,
    ) -> list[dict]:
        """
        List available components from the update server.

        Args:
            component_type: Optional component type filter (e.g., 'shipping_provider', 'widget')
            page: Page number (1-based). If provided, returns paginated dict instead of list.
            page_size: Results per page (default 24).
            search: Search query string for name/slug.

        Returns:
            List of component dicts (unpaginated), or dict with pagination metadata when page is set.
        """
        try:
            self._ensure_authenticated()

            # Build query parameters
            # Note: API uses 'type' not 'component_type' as the parameter name
            params = {}
            if component_type:
                params["type"] = component_type
            if page is not None:
                params["page"] = page
            if page_size is not None:
                params["page_size"] = page_size
            if search:
                params["search"] = search

            response = self.session.get(
                f"{self.config.server_url}/api/v1/components/", params=params, timeout=30
            )
            response.raise_for_status()

            data = response.json()

            # If paginated request, return full response dict with pagination metadata
            if page is not None and isinstance(data, dict) and "results" in data:
                return data

            # Handle response - could be a list directly or a dict with 'components' key
            if isinstance(data, list):
                components_list = data
            elif isinstance(data, dict):
                components_list = data.get("components", data.get("results", []))
            else:
                components_list = []

            return components_list

        except Exception as e:
            logger.error(f"Failed to list available components: {e}")
            raise

    def check_for_updates(self, component: ComponentRegistry | None = None) -> dict:
        """
        Check for available updates from the update server.

        Args:
            component: Specific component to check, or None to check all

        Returns:
            Dict with update information
        """
        self._ensure_authenticated()

        components = [component] if component else ComponentRegistry.objects.filter(locked=False)

        # Build installed components dict for bulk check
        installed_components = {}
        for comp in components:
            # Use slug as-is (don't convert underscores to hyphens)
            # Update server expects simple slug: version mapping
            installed_components[comp.slug] = comp.current_version

        updates_found = []

        try:
            # Bulk check for updates (includes sandbox/environment info for telemetry)
            from core.license import is_sandbox_mode

            response = self.session.post(
                f"{self.config.server_url}/api/v1/updates/check/",
                json={
                    "platform_version": getattr(settings, "PLATFORM_VERSION", "1.0.0"),
                    "installed_components": installed_components,
                    "channels": ["stable"],  # TODO: support multiple channels
                    "is_sandbox": is_sandbox_mode(),
                },
                timeout=30,
            )
            response.raise_for_status()

            data = response.json()

            # Handle response - could be a list directly or a dict with 'updates_available' key
            if isinstance(data, list):
                updates_list = data
            elif isinstance(data, dict):
                updates_list = data.get("updates_available", [])
            else:
                updates_list = []

            # Process updates
            for update_info in updates_list:
                # Find the component by slug
                # API returns 'component_slug', not 'slug'
                # Try both formats (underscored and hyphenated) for compatibility
                comp_slug = update_info.get("component_slug", update_info.get("slug", ""))
                comp = ComponentRegistry.objects.filter(slug=comp_slug).first()

                # If not found with exact slug, try converting hyphens to underscores (backwards compatibility)
                if not comp and "-" in comp_slug:
                    comp_slug_underscored = comp_slug.replace("-", "_")
                    comp = ComponentRegistry.objects.filter(slug=comp_slug_underscored).first()

                if comp:
                    # API returns 'latest_version' for the new version
                    latest_ver = update_info.get("latest_version", update_info.get("version", ""))
                    checksum = update_info.get("package_checksum", "")

                    logger.debug(
                        f"🔍 Update info for {comp.slug}: checksum={checksum[:16]}..."
                        if checksum
                        else f"🔍 Update info for {comp.slug}: NO CHECKSUM"
                    )

                    comp.update_available = True
                    comp.latest_version = latest_ver
                    comp.latest_version_checksum = checksum

                    # Store author and visual asset information from update server
                    if "author_name" in update_info:
                        comp.author = update_info["author_name"]
                    if "author_details" in update_info:
                        comp.author_details = update_info["author_details"]
                    if "thumbnail_url" in update_info:
                        comp.thumbnail_url = update_info["thumbnail_url"]
                    if "preview_images" in update_info:
                        comp.preview_images = update_info["preview_images"]
                    if "preview_videos" in update_info:
                        comp.preview_videos = update_info["preview_videos"]

                    comp.last_checked = timezone.now()
                    comp.save()

                    logger.debug(
                        f"💾 Saved {comp.slug}: checksum={comp.latest_version_checksum[:16]}..."
                        if comp.latest_version_checksum
                        else f"💾 Saved {comp.slug}: checksum is EMPTY"
                    )

                    updates_found.append(
                        {
                            "component": comp,
                            "current_version": comp.current_version,
                            "latest_version": latest_ver,
                            "changelog": update_info.get("changelog", ""),
                            "critical": update_info.get(
                                "security_update", update_info.get("critical", False)
                            ),
                            "checksum": update_info.get("package_checksum", ""),
                            "package_size": update_info.get("package_size_bytes", 0),
                        }
                    )

                    logger.info(
                        f"📦 Update available for {comp.name}: "
                        f"{comp.current_version} → {latest_ver}"
                    )

            # Mark components WITHOUT updates as checked (up-to-date)
            # Note: Components WITH updates were already saved above with update_available=True
            # We must NOT save the original objects here as they would overwrite the updates
            updated_slugs = {u["component"].slug for u in updates_found}
            for comp in components:
                if comp.slug not in updated_slugs:
                    comp.update_available = False
                    comp.last_checked = timezone.now()
                    comp.save()

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to check updates: {e}")
            # Don't raise, just return empty results for graceful degradation
            pass

        # Capture maintenance status from server response if available
        maintenance_active = True  # Default for old servers
        if isinstance(data, dict):
            maintenance_active = data.get("maintenance_active", True)

        # Opportunistic license refresh if maintenance status differs from local
        try:
            from core.license import get_license_manager

            current_maintenance = get_license_manager().get_maintenance_status()
            if maintenance_active != current_maintenance.get("active"):
                logger.info(
                    f"Maintenance status mismatch (server={maintenance_active}, "
                    f"local={current_maintenance.get('active')}) — triggering license refresh"
                )
                self.refresh_license()
        except Exception as e:
            logger.debug(f"Opportunistic license refresh skipped: {e}")

        return {
            "updates_found": len(updates_found),
            "updates": updates_found,
            "checked_at": timezone.now(),
            "maintenance_active": maintenance_active,
        }

    def get_version_history(self, slug: str, channel: str = "stable") -> list:
        """
        Fetch version history for a component from the update server.

        Args:
            slug: Component slug
            channel: Channel filter (default: stable)

        Returns:
            List of version dicts with: version, channel, changelog,
            release_notes, breaking_changes, security_update, published_at
        """
        self._ensure_authenticated()

        try:
            response = self.session.get(
                f"{self.config.server_url}/api/v1/versions/{slug}/",
                params={"channel": channel},
                timeout=15,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.warning(f"Failed to fetch version history for {slug}: {e}")
            return []

    def download_component(self, component: ComponentRegistry, version: str) -> Path:
        """
        Download a component package from the update server.

        Args:
            component: The component to download
            version: Version to download

        Returns:
            Path to downloaded package file

        Raises:
            UpdateDownloadError: If download fails
        """
        self._ensure_authenticated()

        try:
            logger.info(f"📥 Downloading {component.name} v{version}...")

            # Download directly from update server (streaming)
            # Use slug as-is (don't convert underscores to hyphens)
            response = self.session.post(
                f"{self.config.server_url}/api/v1/download/{component.slug}/{version}/",
                stream=True,
                timeout=120,
            )
            response.raise_for_status()

            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(  # noqa: SIM115  # delete=False; path returned to caller
                delete=False, suffix=".zip", prefix=f"{component.slug}_"
            )

            # Download with progress
            int(response.headers.get("content-length", 0))
            downloaded = 0

            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    temp_file.write(chunk)
                    downloaded += len(chunk)

            temp_file.close()

            logger.info(f"✅ Downloaded {component.name} v{version} ({downloaded} bytes)")

            # Verify checksum if available
            expected_checksum = component.latest_version_checksum
            if expected_checksum:
                logger.info("🔍 Verifying package checksum...")
                actual_checksum = self._calculate_checksum(Path(temp_file.name))

                if actual_checksum != expected_checksum:
                    # Delete corrupted file
                    Path(temp_file.name).unlink()
                    raise UpdateDownloadError(
                        f"Checksum mismatch: expected {expected_checksum}, got {actual_checksum}. "
                        f"Package may be corrupted or tampered with."
                    )

                logger.info(f"✅ Checksum verified: {actual_checksum[:16]}...")
            else:
                logger.warning("⚠️ No checksum available for verification")

            return Path(temp_file.name)

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Failed to download {component.name}: {e}")
            raise UpdateDownloadError(f"Download failed: {e}")

    @transaction.atomic
    def install_update(self, component: ComponentRegistry, version: str | None = None) -> bool:
        """
        Install an update for a component.

        Args:
            component: Component to update
            version: Specific version to install, or None for latest

        Returns:
            bool: True if successful

        Raises:
            UpdateInstallError: If installation fails
        """
        if component.locked:
            raise UpdateInstallError(f"Component {component.name} is locked")

        target_version = version or component.latest_version

        # Create update log
        log = UpdateLog.objects.create(
            component=component,
            action="update",
            old_version=component.current_version,
            new_version=target_version,
            status="in_progress",
            is_automatic=False,
        )

        start_time = timezone.now()

        try:
            # Download the package
            package_path = self.download_component(component, target_version)

            # Install the package (component-type specific)
            self._install_package(component, package_path, target_version)

            # Create version record
            new_version = ComponentVersion.objects.create(
                component=component,
                version=target_version,
                install_method="auto",
                package_url=f"{self.config.server_url}/api/components/{component.component_type}/{component.slug}/download/?version={target_version}",
                is_active=False,  # Not active yet
            )

            # Deactivate old version
            ComponentVersion.objects.filter(component=component, is_active=True).update(
                is_active=False
            )

            # Activate new version
            new_version.activate()

            # Update component registry
            component.current_version = target_version
            component.update_available = False
            component.save()

            # Mark log as completed
            duration = (timezone.now() - start_time).total_seconds()
            log.mark_completed(duration=duration)

            # Run health check
            health_passed = self._health_check(component, new_version)

            # If health check failed, rollback
            if not health_passed:
                logger.warning(
                    f"⚠️ Health check failed for {component.name} v{target_version}, attempting rollback..."
                )
                try:
                    # Find previous active version
                    previous_version = (
                        ComponentVersion.objects.filter(component=component, is_active=False)
                        .exclude(id=new_version.id)
                        .order_by("-installed_at")
                        .first()
                    )

                    if previous_version:
                        logger.info(f"🔄 Rolling back to v{previous_version.version}...")
                        # Rollback (deactivate new, reactivate old)
                        new_version.is_active = False
                        new_version.save()

                        previous_version.is_active = True
                        previous_version.save()

                        component.current_version = previous_version.version
                        component.save()

                        # Log rollback
                        UpdateLog.objects.create(
                            component=component,
                            action="rollback",
                            old_version=target_version,
                            new_version=previous_version.version,
                            status="completed",
                            details={"reason": "health_check_failed", "automatic": True},
                        )

                        logger.info(f"✅ Rolled back to v{previous_version.version}")
                        raise UpdateInstallError(
                            f"Health check failed, rolled back to v{previous_version.version}"
                        )
                    else:
                        logger.error("❌ No previous version available for rollback")
                        raise UpdateInstallError(
                            "Health check failed and no previous version to rollback to"
                        )

                except Exception as rollback_error:
                    logger.error(f"❌ Rollback failed: {rollback_error}")
                    raise UpdateInstallError(
                        f"Health check failed and rollback failed: {rollback_error}"
                    )

            # Cleanup
            package_path.unlink()

            # Cleanup old versions (keep last 3)
            self._cleanup_old_versions(component)

            # Invalidate provider cache so updated code is loaded from disk
            self._invalidate_provider_cache(component.component_type)

            logger.info(f"✅ Successfully updated {component.name} to v{target_version}")
            return True

        except Exception as e:
            # Mark log as failed
            log.mark_failed(error_message=str(e))
            logger.error(f"❌ Failed to update {component.name}: {e}")
            raise UpdateInstallError(f"Installation failed: {e}")

    @transaction.atomic
    def install_component(self, component_type: str, slug: str, version: str | None = None) -> dict:
        """
        Install a new component from the update server.

        Args:
            component_type: Type of component (e.g., 'social_connector_provider')
            slug: Component slug (e.g., 'facebook_page')
            version: Specific version to install, or None for latest

        Returns:
            Dict with success status and component info
        """
        try:
            self._ensure_authenticated()

            # Fetch component info from update server
            logger.info(f"📦 Fetching component info for {slug}...")
            response = self.session.get(
                f"{self.config.server_url}/api/v1/component/{slug}/", timeout=30
            )
            response.raise_for_status()
            component_info = response.json()

            # Get version to install
            target_version = version or component_info.get("current_version")
            if not target_version:
                raise UpdateInstallError(f"No version available for {slug}")

            # Check if component already exists
            existing = ComponentRegistry.objects.filter(
                component_type=component_type, slug=slug
            ).first()

            if existing:
                # Component exists, use install_update instead
                logger.info(f"Component {slug} already exists, updating...")
                existing.latest_version = target_version
                existing.save()
                self.install_update(existing, target_version)
                return {"success": True, "component": existing, "action": "updated"}

            # Create new ComponentRegistry entry
            logger.info(f"📝 Creating registry entry for {slug}...")
            component = ComponentRegistry.objects.create(
                component_type=component_type,
                slug=slug,
                name=component_info.get("name", slug),
                description=component_info.get("description", ""),
                current_version=target_version,
                latest_version=target_version,
                thumbnail_url=component_info.get("thumbnail_url", ""),
                homepage_url=component_info.get("homepage_url", ""),
                support_url=component_info.get("documentation_url", ""),
                author=component_info.get("author", {}).get("name", "Unknown")
                if isinstance(component_info.get("author"), dict)
                else component_info.get("author", "Unknown"),
            )

            # Create update log
            log = UpdateLog.objects.create(
                component=component,
                action="install",
                old_version="",
                new_version=target_version,
                status="in_progress",
                is_automatic=False,
            )

            start_time = timezone.now()

            try:
                # Download the package
                logger.info(f"📥 Downloading {slug} v{target_version}...")
                response = self.session.post(
                    f"{self.config.server_url}/api/v1/download/{slug}/{target_version}/",
                    stream=True,
                    timeout=120,
                )
                response.raise_for_status()

                # Save to temp file
                temp_file = tempfile.NamedTemporaryFile(  # noqa: SIM115  # delete=False; path returned to caller
                    delete=False, suffix=".zip", prefix=f"{slug}_"
                )

                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        temp_file.write(chunk)
                temp_file.close()

                package_path = Path(temp_file.name)

                # Install the package
                self._install_package(component, package_path, target_version)

                # Create version record
                ComponentVersion.objects.create(
                    component=component,
                    version=target_version,
                    install_method="manual",
                    is_active=True,
                )

                # Mark log as completed
                duration = (timezone.now() - start_time).total_seconds()
                log.mark_completed(duration=duration)

                # Cleanup temp file
                package_path.unlink()

                # Invalidate provider cache so new provider code is loaded from disk
                self._invalidate_provider_cache(component_type)

                logger.info(f"✅ Successfully installed {slug} v{target_version}")
                return {"success": True, "component": component, "action": "installed"}

            except Exception as e:
                # Mark log as failed
                log.mark_failed(error_message=str(e))
                # Delete the component registry entry on failure
                component.delete()
                raise

        except Exception as e:
            logger.error(f"❌ Failed to install {slug}: {e}")
            raise UpdateInstallError(f"Installation failed: {e}")

    def update_component(self, component_type: str, slug: str, version: str | None = None) -> dict:
        """
        Update an existing component from the update server.

        Args:
            component_type: Type of component (e.g., 'social_connector_provider')
            slug: Component slug (e.g., 'facebook_page')
            version: Specific version to install, or None for latest

        Returns:
            Dict with success status
        """
        try:
            # Find the existing component
            component = ComponentRegistry.objects.filter(
                component_type=component_type, slug=slug
            ).first()

            if not component:
                raise UpdateInstallError(f"Component {slug} not found in registry")

            # Fetch latest version info from server
            self._ensure_authenticated()
            response = self.session.get(
                f"{self.config.server_url}/api/v1/component/{slug}/", timeout=30
            )
            response.raise_for_status()
            component_info = response.json()

            target_version = version or component_info.get("current_version")
            if not target_version:
                raise UpdateInstallError(f"No version available for {slug}")

            # Update latest version info
            component.latest_version = target_version
            component.save()

            # Use existing install_update method
            self.install_update(component, target_version)

            return {"success": True, "component": component}

        except Exception as e:
            logger.error(f"❌ Failed to update {slug}: {e}")
            return {"success": False, "error": str(e)}

    def _install_package(self, component: ComponentRegistry, package_path: Path, version: str):
        """
        Install a component package (type-specific logic).

        Args:
            component: Component being installed
            package_path: Path to downloaded package
            version: Version being installed
        """
        # Extract package
        extract_dir = Path(tempfile.mkdtemp(prefix=f"{component.slug}_extract_"))

        try:
            with zipfile.ZipFile(package_path, "r") as zip_ref:
                zip_ref.extractall(extract_dir)

            # Read manifest
            manifest_path = extract_dir / "manifest.json"
            if not manifest_path.exists():
                raise UpdateInstallError("Package missing manifest.json")

            with open(manifest_path) as f:
                manifest = json.load(f)

            # Verify manifest (normalize slugs for comparison - handle hyphenated vs underscored)
            manifest_slug = manifest.get("slug", "").replace("-", "_")
            component_slug = component.slug.replace("-", "_")
            if manifest_slug != component_slug:
                raise UpdateInstallError(
                    f"Package slug mismatch: expected {component.slug}, got {manifest.get('slug')}"
                )

            if manifest.get("version") != version:
                raise UpdateInstallError("Package version mismatch")

            # Component-type specific installation
            # Note: Widgets are baked into the platform and don't use the update system
            if component.component_type == "theme":
                self._install_theme_package(component, extract_dir, manifest)
            elif component.component_type == "utility":
                self._install_utility_package(component, extract_dir, manifest)
            elif component.component_type == "element":
                self._install_element_package(component, extract_dir, manifest)
            elif component.component_type in ["header_template", "footer_template"]:
                self._install_template_package(component, extract_dir, manifest)
            elif component.component_type == "language_pack":
                self._install_language_pack_package(component, extract_dir, manifest)
            else:
                # Generic installation for provider types and any future component types
                # Handles: shipping_provider, payment_provider, hosting_provider, etc.
                self._install_generic_provider_package(component, extract_dir, manifest)

        finally:
            # Cleanup extraction directory
            shutil.rmtree(extract_dir, ignore_errors=True)

    def _install_theme_package(
        self, component: ComponentRegistry, extract_dir: Path, manifest: dict
    ):
        """
        Install a theme package using symlink-based versioning.

        Themes use a special installation system:
        - Files installed to components_data/static/design/themes/{slug}/{version}/
        - Activated via symlink: current -> {version}
        - Zero-downtime updates by flipping symlinks
        - Only ONE theme can be active at a time (enforced by ThemeVersionManager)
        """
        from design.theme_version_manager import ThemeVersionManager

        theme_slug = manifest["slug"]
        version = manifest["version"]

        logger.info(f"Installing theme: {theme_slug} v{version}")

        try:
            # Use ThemeVersionManager to install the theme
            result = ThemeVersionManager.install_theme_version(
                theme_slug=theme_slug, version=version, package_path=extract_dir
            )

            if not result["success"]:
                raise UpdateInstallError(f"Failed to install theme: {result.get('error')}")

            logger.info(f"✅ Theme {theme_slug} v{version} installed successfully")

            # Collect static files so NGINX can serve the new theme's assets
            self._collect_static_files()

            # Note: Theme is installed but NOT automatically activated
            # Only ONE theme can be active at a time
            # Admin must manually activate via ThemeVersionManager.activate_theme_version()
            # or through the unified theme management UI
            # This allows reviewing the theme before making it live

        except Exception as e:
            logger.error(f"Failed to install theme {theme_slug}: {e}")
            raise UpdateInstallError(f"Theme installation failed: {e}")

    def _install_utility_package(
        self, component: ComponentRegistry, extract_dir: Path, manifest: dict
    ):
        """
        Install a page builder utility package using symlink-based versioning.

        Utilities use a special installation system:
        - Files installed to components_data/static/utilities/{slug}/v{version}/
        - Activated via symlink: current -> v{version}
        - Zero-downtime updates by flipping symlinks
        """
        from .utility_version_manager import UtilityVersionManager

        utility_slug = manifest["slug"].replace("-", "_")
        version = manifest["version"]

        logger.info(f"Installing utility: {utility_slug} v{version}")

        try:
            fs_version = f"v{version}"  # Add 'v' prefix for filesystem

            # Use UtilityVersionManager to install the utility files
            result = UtilityVersionManager.install_utility_version(
                utility_slug=utility_slug, version=fs_version, package_path=extract_dir
            )

            if not result["success"]:
                raise UpdateInstallError(f"Failed to install utility: {result.get('error')}")

            # Activate the version (flip symlink) so it's live immediately
            activate_result = UtilityVersionManager.activate_utility_version(
                utility_slug=utility_slug, version=fs_version
            )

            if not activate_result["success"]:
                raise UpdateInstallError(
                    f"Failed to activate utility: {activate_result.get('error')}"
                )

            logger.info(f"✅ Utility {utility_slug} v{version} installed and activated")

            # Collect static files so NGINX can serve the new utility's assets
            self._collect_static_files()

        except Exception as e:
            logger.error(f"Failed to install utility {utility_slug}: {e}")
            raise UpdateInstallError(f"Utility installation failed: {e}")

    def _install_element_package(
        self, component: ComponentRegistry, extract_dir: Path, manifest: dict
    ):
        """Install a page builder element package"""
        # TODO: Implement when element model is available
        logger.warning("Element package installation not yet implemented")

    def _install_generic_provider_package(
        self, component: ComponentRegistry, extract_dir: Path, manifest: dict
    ):
        """
        Install a generic provider package using symlink-based versioning.

        This method handles any provider type (shipping, payment, hosting, etc.) that follows
        the standard provider pattern:
        - Files installed to components_data/integrations/{type}/{slug}/v{version}/
        - Activated via symlink: current -> v{version}
        - Zero-downtime updates by flipping symlinks
        """
        from component_updates.integration_paths import INTEGRATIONS_DIR

        component_type = component.component_type
        provider_slug = manifest["slug"]
        version = manifest["version"]

        logger.info(f"Installing {component_type}: {provider_slug} v{version}")

        try:
            # Base path uses component_type slug directly as directory name
            base_path = INTEGRATIONS_DIR / component_type / provider_slug
            base_path.mkdir(parents=True, exist_ok=True)

            # Version directory with 'v' prefix
            version_dir = base_path / f"v{version}"

            # Remove existing version directory if it exists
            if version_dir.exists():
                logger.info(f"Removing existing version directory: {version_dir}")
                shutil.rmtree(version_dir)

            # Copy all files from extracted package to version directory
            shutil.copytree(extract_dir, version_dir)
            logger.info(f"✅ Files copied to {version_dir}")

            # Update or create 'current' symlink
            current_link = base_path / "current"
            if current_link.exists() or current_link.is_symlink():
                current_link.unlink()

            current_link.symlink_to(f"v{version}")
            logger.info(f"✅ Symlink 'current' -> v{version}")

            logger.info(f"✅ {component_type} {provider_slug} v{version} installed successfully")

            # Collect static files so NGINX can serve the new component's assets
            self._collect_static_files()

        except Exception as e:
            logger.error(f"Failed to install {component_type} {provider_slug}: {e}")
            raise UpdateInstallError(f"{component_type} installation failed: {e}")

    def _install_template_package(
        self, component: ComponentRegistry, extract_dir: Path, manifest: dict
    ):
        """Install a header/footer template package"""
        # TODO: Implement when template models are available
        logger.warning("Template package installation not yet implemented")

    def _install_language_pack_package(
        self, component: ComponentRegistry, extract_dir: Path, manifest: dict
    ):
        """
        Install a language pack package.

        Language packs deliver Django .po/.mo files, UI string translations,
        help content, and SiteLanguage metadata for a single language.
        """
        from .language_pack_installer import install_language_pack

        language_code = manifest.get("language_code")
        version = manifest.get("version", "1.0.0")

        if not language_code:
            raise UpdateInstallError("Language pack manifest missing 'language_code'")

        logger.info(f"Installing language pack: {component.slug} v{version} (lang={language_code})")

        result = install_language_pack(extract_dir, manifest)

        if not result.get("success"):
            raise UpdateInstallError(f"Language pack installation failed: {result.get('error')}")

        if result.get("restart_required"):
            logger.info(
                "Language pack installed — worker/server restart required "
                "for settings.LANGUAGES to pick up the new language."
            )

    def _collect_static_files(self):
        """Sync component static files into STATIC_ROOT for WhiteNoise to serve."""
        try:
            from django.core.management import call_command

            call_command("collect_component_statics", verbosity=0)
            logger.info("✅ Component static files synced")
        except Exception as e:
            logger.warning(
                f"collect_component_statics failed, falling back to full collectstatic: {e}"
            )
            try:
                call_command("collectstatic", "--noinput", verbosity=0)
                logger.info("✅ Static files collected (full)")
            except Exception as e2:
                logger.warning(f"collectstatic also failed (non-fatal): {e2}")

    def _health_check(self, component: ComponentRegistry, version: ComponentVersion) -> bool:
        """
        Run health check on newly installed component.

        Args:
            component: Component to check
            version: Version to check

        Returns:
            bool: True if health check passed, False otherwise
        """
        try:
            # Component-type specific health checks
            health_status = "healthy"
            health_details = {}

            # Note: Widgets are baked into the platform and don't need health checks
            if component.component_type == "theme":
                # Use ThemeVersionManager for health check with symlink validation
                from design.theme_version_manager import ThemeVersionManager

                theme_slug = component.slug
                installed_version = version.version

                # Run ThemeVersionManager health check
                theme_health = ThemeVersionManager.health_check(theme_slug, installed_version)
                health_details.update(theme_health)

                # Map health check status
                if theme_health["status"] == "healthy":
                    health_status = "healthy"
                elif theme_health["status"] == "degraded":
                    health_status = "degraded"
                else:
                    health_status = "unhealthy"

            elif component.component_type == "utility":
                # Check utility files exist and symlink is valid
                from .utility_version_manager import UTILITIES_STATIC, UtilityVersionManager

                utility_slug = component.slug
                installed_version = f"v{version.version}"

                # Check version directory exists
                version_dir = UTILITIES_STATIC / utility_slug.replace("-", "_") / installed_version
                health_details["version_files_exist"] = version_dir.exists()

                # Check if this version is currently active
                current_version = UtilityVersionManager.get_current_version(utility_slug)
                health_details["is_active"] = current_version == installed_version
                health_details["current_version"] = current_version

                # Check symlink is valid
                from .utility_discovery import discover_installed_utilities

                utilities = discover_installed_utilities(use_cache=False)
                utility_found = any(u["name"] == utility_slug.replace("-", "_") for u in utilities)
                health_details["discoverable"] = utility_found

                if not version_dir.exists():
                    health_status = "unhealthy"
                elif not health_details["is_active"]:
                    health_status = "degraded"  # Installed but not active
                    health_details["status_note"] = "Installed but not activated"

            version.health_status = health_status
            version.health_details = health_details
            version.health_checked_at = timezone.now()
            version.save()

            # Log health check
            UpdateLog.objects.create(
                component=component,
                action="health_check",
                new_version=version.version,
                status="completed" if health_status == "healthy" else "failed",
                details=health_details,
            )

            logger.info(f"🏥 Health check for {component.name} v{version.version}: {health_status}")
            return health_status == "healthy"

        except Exception as e:
            logger.error(f"Health check failed for {component.name}: {e}")
            version.health_status = "unhealthy"
            version.save()

            # Log failed health check
            UpdateLog.objects.create(
                component=component,
                action="health_check",
                new_version=version.version,
                status="failed",
                error_message=str(e),
                details={"error": str(e)},
            )

            return False

    def _cleanup_old_versions(self, component: ComponentRegistry):
        """
        Cleanup old versions, keeping only the last 3.

        Args:
            component: Component to cleanup
        """
        versions = ComponentVersion.objects.filter(component=component).order_by("-installed_at")

        # Keep first 3, delete the rest
        for version in versions[3:]:
            version.rollback_available = False
            version.save()

    def _invalidate_provider_cache(self, component_type: str):
        """
        Invalidate in-memory provider cache after a component is installed or updated.

        Provider loaders cache provider classes in memory (class-level dicts + sys.modules).
        After installing/updating a provider component, the cached classes must be cleared
        so the new code is loaded from disk on the next request.

        This method maps component_type to the appropriate registry's reload_providers()
        method. Non-provider component types (themes, utilities, etc.) are silently skipped.
        """
        # Map component_type to their registry's reload_providers callable
        PROVIDER_RELOAD_MAP = {
            "email_provider": "email_system.providers.registry.ProviderRegistry",
            "exchange_rate_provider": "exchange_rates.providers.registry.ProviderRegistry",
            "payment_provider": "payment_providers.providers.registry.ProviderRegistry",
            "shipping_provider": "shipping.providers.registry.ProviderRegistry",
            "seo_generator_provider": "seo_generator.providers.registry.ProviderRegistry",
            "product_feed_provider": "product_feeds.providers.registry.ProviderRegistry",
            "payout_provider": "payout_providers.loader.PayoutProviderLoader",
            "sms_provider": "sms_system.providers.loader.ProviderLoader",
            "terminal_provider": "pos_app.terminal_providers.registry.ProviderRegistry",
            "license_server_provider": "catalog.providers.registry.ProviderRegistry",
        }

        registry_path = PROVIDER_RELOAD_MAP.get(component_type)
        if not registry_path:
            return  # Not a provider type, nothing to invalidate

        # Write a file-based marker so OTHER workers detect the stale cache
        from component_updates.integration_paths import touch_provider_cache_marker

        touch_provider_cache_marker(component_type)

        try:
            # Reload providers in THIS worker immediately
            module_path, class_name = registry_path.rsplit(".", 1)
            import importlib

            module = importlib.import_module(module_path)
            registry_class = getattr(module, class_name)
            registry_class.reload_providers()
            logger.info(f"🔄 Invalidated provider cache for {component_type}")
        except Exception as e:
            # Cache invalidation failure is non-fatal — providers will reload on next server restart
            logger.warning(f"⚠️ Failed to invalidate provider cache for {component_type}: {e}")

    @transaction.atomic
    def rollback(self, component: ComponentRegistry, target_version: str | None = None) -> bool:
        """
        Rollback a component to a previous version.

        Args:
            component: Component to rollback
            target_version: Specific version to rollback to, or None for previous

        Returns:
            bool: True if successful
        """
        current_version = component.current_version

        # Find target version
        if target_version:
            version = ComponentVersion.objects.filter(
                component=component, version=target_version, rollback_available=True
            ).first()
        else:
            # Get most recent non-active version
            version = (
                ComponentVersion.objects.filter(
                    component=component, is_active=False, rollback_available=True
                )
                .order_by("-installed_at")
                .first()
            )

        if not version:
            raise UpdateInstallError("No rollback version available")

        # Create rollback log
        log = UpdateLog.objects.create(
            component=component,
            action="rollback",
            old_version=current_version,
            new_version=version.version,
            status="in_progress",
            is_automatic=False,
        )

        start_time = timezone.now()

        try:
            # Activate the target version
            version.activate()

            # Mark log as completed
            duration = (timezone.now() - start_time).total_seconds()
            log.mark_completed(duration=duration)

            # Invalidate provider cache so rolled-back code is loaded from disk
            self._invalidate_provider_cache(component.component_type)

            logger.info(
                f"✅ Rolled back {component.name} from v{current_version} to v{version.version}"
            )
            return True

        except Exception as e:
            log.mark_failed(error_message=str(e))
            logger.error(f"❌ Rollback failed for {component.name}: {e}")
            raise UpdateInstallError(f"Rollback failed: {e}")

    def check_dependencies(
        self, component: ComponentRegistry, version: str
    ) -> tuple[bool, list[str]]:
        """
        Check if component dependencies are satisfied.

        Args:
            component: Component to check
            version: Version to check dependencies for

        Returns:
            Tuple of (dependencies_satisfied, list of missing/incompatible dependencies)
        """
        dependencies = ComponentDependency.objects.filter(component=component, version=version)

        issues = []

        for dep in dependencies:
            # Find the required component
            required = ComponentRegistry.objects.filter(
                component_type=dep.required_component_type, slug=dep.required_slug
            ).first()

            if not required:
                issues.append(
                    f"Missing required {dep.required_component_type}: {dep.required_slug}"
                )
                continue

            # Check version constraint
            if dep.version_constraint:
                # Simple version check (could use packaging.version for full SemVer)
                if not self._version_satisfies(required.current_version, dep.version_constraint):
                    issues.append(
                        f"{dep.required_slug} version {required.current_version} "
                        f"does not satisfy constraint {dep.version_constraint}"
                    )

        return (len(issues) == 0, issues)

    def _version_satisfies(self, version: str, constraint: str) -> bool:
        """
        Check if a version satisfies a constraint.
        Simple implementation - could be enhanced with proper SemVer parsing.

        Args:
            version: Actual version
            constraint: Version constraint (e.g., ">=1.0.0", "^2.0.0")

        Returns:
            bool: True if constraint is satisfied
        """
        # TODO: Implement proper SemVer constraint checking
        # For now, just check if versions match
        if constraint.startswith(">="):
            required = constraint[2:].strip()
            return version >= required
        elif constraint.startswith("^"):
            # Caret: compatible with version
            required = constraint[1:].strip()
            return version.split(".")[0] == required.split(".")[0]
        else:
            return version == constraint


# =============================================================================
# Platform Update Service
# =============================================================================


class PlatformUpdateError(Exception):
    """Base exception for platform update errors"""

    pass


class PlatformUpdateService:
    """
    Service for managing platform updates with blue-green deployment.

    Handles:
    - Checking for platform updates
    - Downloading platform packages
    - Verifying package integrity
    - Orchestrating blue-green deployment
    - Reporting update status to update server
    - Rollback operations
    """

    # Update steps with progress percentages
    UPDATE_STEPS = [
        {"name": "Downloading", "progress": 10},
        {"name": "Verifying", "progress": 15},
        {"name": "Extracting", "progress": 25},
        {"name": "Pre-checks", "progress": 35},
        {"name": "Migrations", "progress": 55},
        {"name": "Building", "progress": 70},
        {"name": "Health check", "progress": 85},
        {"name": "Switching", "progress": 95},
    ]

    def __init__(self):
        self.config = UpdateServerConfig.get_instance()
        self.session = requests.Session()
        self.session.headers.update(
            {"User-Agent": "ShopPlatform/1.0", "Accept": "application/json"}
        )

    def _ensure_authenticated(self) -> bool:
        """Ensure we have a valid JWT token for the update server."""
        if not self.config.server_url:
            raise PlatformUpdateError("Update server URL not configured")

        if self.config.is_jwt_valid():
            self.session.headers.update({"Authorization": f"Bearer {self.config.jwt_token}"})
            return True

        # Authenticate with update server
        try:
            from core.license import get_license_manager, is_sandbox_mode

            reg_data = {
                "installation_uuid": str(self.config.installation_uuid),
                "platform_version": self.get_current_version(),
                "license_key": self.config.license_key,
                "is_sandbox": is_sandbox_mode(),
                "environment_type": get_license_manager().get_environment_type(),
            }

            # Include domain from Sites framework for server-side tracking
            try:
                from django.contrib.sites.models import Site

                reg_data["domain"] = Site.objects.get(pk=1).domain
            except Exception:
                pass

            # Include license acceptance data for phone-home
            try:
                from core.license_acceptance import get_license_acceptance_service

                acceptance_service = get_license_acceptance_service()
                acceptance_info = acceptance_service.get_acceptance_info()
                if acceptance_info and acceptance_info.get("accepted"):
                    reg_data["license_acceptance"] = {
                        "license_version": acceptance_info.get("license_version", ""),
                        "accepted_at": acceptance_info.get("timestamp", ""),
                        "checksum": acceptance_info.get("license_checksum", ""),
                        "accepted_via": acceptance_info.get("accepted_via", ""),
                        "accepted_by_email": acceptance_info.get("accepted_by_email", ""),
                    }
            except Exception:
                pass  # Don't block registration if acceptance read fails

            response = self.session.post(
                f"{self.config.server_url}/api/v1/auth/register/", json=reg_data, timeout=10
            )
            response.raise_for_status()

            data = response.json()
            self.config.jwt_token = data["token"]
            self.config.jwt_expires_at = timezone.now() + timedelta(
                seconds=data.get("expires_in", 3600)
            )
            self.config.save()

            self.session.headers.update({"Authorization": f"Bearer {self.config.jwt_token}"})
            return True

        except requests.exceptions.RequestException as e:
            raise PlatformUpdateError(f"Authentication failed: {e}")

    def get_current_version(self) -> str:
        """Get the current platform version."""
        return getattr(settings, "PLATFORM_VERSION", "1.0.0")

    def check_for_update(self, channel: str = "stable") -> dict:
        """
        Check if a platform update is available.

        Args:
            channel: Update channel ('stable', 'beta', 'dev')

        Returns:
            Dict with update information including:
            - update_available: bool
            - current_version: str
            - latest_version: str (if available)
            - changelog: str
            - requires_migration: bool
            - package_size_bytes: int
            - etc.
        """
        self._ensure_authenticated()

        try:
            response = self.session.post(
                f"{self.config.server_url}/api/v1/platform/check/",
                json={"current_version": self.get_current_version(), "channel": channel},
                timeout=30,
            )
            response.raise_for_status()

            data = response.json()
            logger.info(f"Platform update check: {data.get('update_available', False)}")
            return data

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to check for platform updates: {e}")
            raise PlatformUpdateError(f"Update check failed: {e}")

    def download_package(self, version: str, update_record=None) -> Path:
        """
        Download a platform package from the update server.

        Args:
            version: Version to download
            update_record: Optional PlatformUpdate record for progress tracking

        Returns:
            Path to downloaded package file

        Raises:
            PlatformUpdateError: If download fails
        """

        self._ensure_authenticated()

        try:
            logger.info(f"📥 Downloading platform v{version}...")

            if update_record:
                update_record.status = "downloading"
                update_record.current_step = "Downloading package"
                update_record.add_log_line(f"Starting download of platform v{version}...")
                update_record.save()

            response = self.session.post(
                f"{self.config.server_url}/api/v1/platform/download/{version}/",
                stream=True,
                timeout=600,  # 10 minute timeout for large packages
            )
            response.raise_for_status()

            # Get expected checksum from header
            expected_checksum = response.headers.get("X-Package-Checksum", "")

            # Create staging directory
            staging_dir = Path(settings.BASE_DIR) / "updates" / "staging"
            staging_dir.mkdir(parents=True, exist_ok=True)

            # Download to temp file
            package_path = staging_dir / f"spwig-v{version}.zip"
            total_size = int(response.headers.get("content-length", 0))
            downloaded = 0

            with open(package_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)

                        # Update progress
                        if update_record and total_size > 0:
                            update_record.bytes_downloaded = downloaded
                            update_record.save(update_fields=["bytes_downloaded"])

            logger.info(f"✅ Downloaded platform v{version} ({downloaded} bytes)")

            if update_record:
                update_record.add_log_line(f"Downloaded {downloaded} bytes")
                update_record.package_checksum = expected_checksum
                update_record.package_size_bytes = downloaded
                update_record.save()

            return package_path

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Failed to download platform package: {e}")
            raise PlatformUpdateError(f"Download failed: {e}")

    def verify_package(
        self, package_path: Path, expected_checksum: str, update_record=None
    ) -> bool:
        """
        Verify package integrity using SHA256 checksum.

        Args:
            package_path: Path to downloaded package
            expected_checksum: Expected SHA256 checksum
            update_record: Optional PlatformUpdate record for progress tracking

        Returns:
            bool: True if checksum matches

        Raises:
            PlatformUpdateError: If verification fails
        """
        logger.info("🔍 Verifying package checksum...")

        if update_record:
            update_record.status = "verifying"
            update_record.current_step = "Verifying package integrity"
            update_record.add_log_line("Calculating SHA256 checksum...")
            update_record.save()

        sha256 = hashlib.sha256()
        with open(package_path, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)

        actual_checksum = sha256.hexdigest()

        if expected_checksum and actual_checksum != expected_checksum:
            logger.error(
                f"❌ Checksum mismatch: expected {expected_checksum}, got {actual_checksum}"
            )
            raise PlatformUpdateError(
                "Checksum verification failed. Package may be corrupted or tampered with."
            )

        logger.info(f"✅ Checksum verified: {actual_checksum[:16]}...")

        if update_record:
            update_record.add_log_line(f"Checksum verified: {actual_checksum[:16]}...")
            update_record.update_step("Verifying", "completed", "SHA256 matched")

        return True

    def extract_package(self, package_path: Path, version: str, update_record=None) -> Path:
        """
        Extract package to staging directory.

        Args:
            package_path: Path to downloaded package
            version: Version being installed
            update_record: Optional PlatformUpdate record for progress tracking

        Returns:
            Path to extracted package directory

        Raises:
            PlatformUpdateError: If extraction fails
        """
        logger.info("📦 Extracting package...")

        if update_record:
            update_record.status = "extracting"
            update_record.current_step = "Extracting files"
            update_record.add_log_line("Extracting package...")
            update_record.save()

        staging_dir = Path(settings.BASE_DIR) / "updates" / "staging" / f"v{version}"

        # Clean up any existing staging directory
        if staging_dir.exists():
            shutil.rmtree(staging_dir)

        staging_dir.mkdir(parents=True, exist_ok=True)

        try:
            with zipfile.ZipFile(package_path, "r") as zf:
                # Count files for progress
                file_count = len(zf.namelist())
                zf.extractall(staging_dir)

            logger.info(f"✅ Extracted {file_count} files to {staging_dir}")

            if update_record:
                update_record.add_log_line(f"Extracted {file_count} files")
                update_record.update_step("Extracting", "completed", f"{file_count} files")

            return staging_dir

        except zipfile.BadZipFile as e:
            logger.error(f"❌ Failed to extract package: {e}")
            raise PlatformUpdateError(f"Package extraction failed: {e}")

    def run_pre_checks(self, staging_dir: Path, update_record=None) -> bool:
        """
        Run pre-update compatibility checks.

        Args:
            staging_dir: Path to extracted package
            update_record: Optional PlatformUpdate record for progress tracking

        Returns:
            bool: True if all checks pass

        Raises:
            PlatformUpdateError: If any check fails
        """
        import subprocess

        logger.info("🔍 Running pre-update checks...")

        if update_record:
            update_record.status = "pre_checks"
            update_record.current_step = "Running pre-update checks"
            update_record.add_log_line("Running compatibility checks...")
            update_record.save()

        # Check for pre_update.sh script
        pre_update_script = staging_dir / "scripts" / "pre_update.sh"
        if pre_update_script.exists():
            try:
                result = subprocess.run(
                    ["/bin/bash", str(pre_update_script)],
                    cwd=staging_dir,
                    capture_output=True,
                    text=True,
                    timeout=120,
                )

                if result.returncode != 0:
                    logger.error(f"❌ Pre-update checks failed: {result.stderr}")
                    raise PlatformUpdateError(f"Pre-update checks failed: {result.stderr}")

                logger.info("✅ Pre-update checks passed")

                if update_record:
                    update_record.add_log_line("All pre-update checks passed")
                    update_record.update_step("Pre-checks", "completed", "All checks passed")

            except subprocess.TimeoutExpired:
                raise PlatformUpdateError("Pre-update checks timed out")
        else:
            logger.info("No pre_update.sh script found, skipping")
            if update_record:
                update_record.add_log_line("No pre-update script found")
                update_record.update_step("Pre-checks", "completed", "No script")

        return True

    def report_update_status(
        self,
        from_version: str,
        to_version: str,
        status: str,
        duration_seconds: int = None,
        downtime_seconds: int = None,
        error_message: str = "",
        error_stage: str = "",
        was_rolled_back: bool = False,
        rollback_reason: str = "",
    ):
        """
        Report update status to the update server.

        Args:
            from_version: Version updated from
            to_version: Version updated to
            status: Update status ('started', 'migrating', 'deploying', 'completed', 'failed', 'rolled_back')
            duration_seconds: Total update duration
            downtime_seconds: Actual downtime during update
            error_message: Error message if failed
            error_stage: Stage where error occurred
            was_rolled_back: Whether rollback was performed
            rollback_reason: Reason for rollback
        """
        try:
            self._ensure_authenticated()

            response = self.session.post(
                f"{self.config.server_url}/api/v1/platform/report/",
                json={
                    "from_version": from_version,
                    "to_version": to_version,
                    "status": status,
                    "duration_seconds": duration_seconds,
                    "downtime_seconds": downtime_seconds,
                    "error_message": error_message,
                    "error_stage": error_stage,
                    "was_rolled_back": was_rolled_back,
                    "rollback_reason": rollback_reason,
                },
                timeout=10,
            )
            response.raise_for_status()
            logger.info(f"✅ Reported update status: {status}")

        except Exception as e:
            # Don't fail the update if reporting fails
            logger.warning(f"⚠️ Failed to report update status: {e}")

    def create_update_record(self, to_version: str, update_info: dict, user=None):
        """
        Create a PlatformUpdate record for tracking.

        Args:
            to_version: Target version
            update_info: Update information from check_for_update()
            user: User who initiated the update

        Returns:
            PlatformUpdate instance
        """
        from .models import PlatformUpdate

        # Initialize steps
        steps = []
        for step in self.UPDATE_STEPS:
            steps.append({"name": step["name"], "status": "pending", "detail": None})

        update = PlatformUpdate.objects.create(
            from_version=self.get_current_version(),
            to_version=to_version,
            channel=update_info.get("channel", "stable"),
            status="checking",
            progress_percent=0,
            current_step="Initializing",
            steps=steps,
            changelog=update_info.get("changelog", ""),
            release_notes=update_info.get("release_notes", ""),
            requires_migration=update_info.get("requires_migration", False),
            migration_estimate_seconds=update_info.get("migration_estimate_seconds", 30),
            breaking_changes=update_info.get("breaking_changes", False),
            security_update=update_info.get("security_update", False),
            package_size_bytes=update_info.get("package_size_bytes", 0),
            rollback_version=self.get_current_version(),
            started_at=timezone.now(),
            initiated_by=user,
        )

        return update

    def get_update_status(self, update_id: str) -> dict:
        """
        Get the current status of a platform update.

        Args:
            update_id: UUID of the update

        Returns:
            Dict with update status information
        """
        from .models import PlatformUpdate

        try:
            update = PlatformUpdate.objects.get(id=update_id)
            return {
                "update_id": str(update.id),
                "status": update.status,
                "progress_percent": update.progress_percent,
                "current_step": update.current_step,
                "steps": update.steps,
                "log_lines": update.log_lines[-20:],  # Last 20 lines
                "estimated_seconds_remaining": self._estimate_remaining_time(update),
                "can_cancel": update.status in ["checking", "downloading"],
                "error_message": update.error_message,
                "rollback_available": update.rollback_available,
            }
        except PlatformUpdate.DoesNotExist:
            return {"error": "Update not found"}

    def _estimate_remaining_time(self, update) -> int | None:
        """Estimate remaining time based on progress and elapsed time."""
        if not update.started_at or update.progress_percent <= 0:
            return None

        elapsed = (timezone.now() - update.started_at).total_seconds()
        if update.progress_percent >= 100:
            return 0

        # Estimate based on linear progress
        estimated_total = elapsed / (update.progress_percent / 100)
        remaining = estimated_total - elapsed

        return max(0, int(remaining))

    def cleanup_staging(self, version: str = None):
        """
        Clean up staging directory.

        Args:
            version: Specific version to clean up, or None for all
        """
        staging_base = Path(settings.BASE_DIR) / "updates" / "staging"

        if version:
            version_dir = staging_base / f"v{version}"
            if version_dir.exists():
                shutil.rmtree(version_dir)
                logger.info(f"Cleaned up staging for v{version}")
        else:
            if staging_base.exists():
                shutil.rmtree(staging_base)
                staging_base.mkdir(parents=True, exist_ok=True)
                logger.info("Cleaned up all staging directories")

    def get_rollback_info(self) -> dict:
        """
        Get information about available rollback.

        Returns:
            Dict with rollback availability and details
        """
        from .models import PlatformUpdate

        # Find the most recent successful update
        last_successful = (
            PlatformUpdate.objects.filter(status="completed", rollback_available=True)
            .order_by("-completed_at")
            .first()
        )

        if not last_successful:
            return {"available": False, "reason": "No previous version available for rollback"}

        return {
            "available": True,
            "current_version": self.get_current_version(),
            "rollback_version": last_successful.from_version,
            "updated_at": last_successful.completed_at.isoformat()
            if last_successful.completed_at
            else None,
        }

    def get_applied_hotfixes(self) -> list:
        """
        Read the list of applied hotfix numbers from the marker file.

        Supports two formats:
        - New: "1.3.0:1,2,3" → [1, 2, 3]
        - Legacy: "1.3.0-hf2" → [2]
        - No marker → []
        """
        from pathlib import Path

        marker = Path("/app/hotfixes/.applied")
        if not marker.exists():
            return []
        try:
            content = marker.read_text().strip()
            if not content:
                return []
            # New format: "1.3.0:1,2,3"
            if ":" in content:
                nums_str = content.split(":", 1)[1]
                return sorted(int(n) for n in nums_str.split(",") if n.strip())
            # Legacy format: "1.3.0-hf2"
            if "-hf" in content:
                return [int(content.split("-hf")[1])]
        except (ValueError, IndexError, OSError):
            pass
        return []

    def get_current_hotfix_number(self) -> int:
        """Highest applied hotfix number (legacy compat)."""
        applied = self.get_applied_hotfixes()
        return max(applied) if applied else 0

    def check_for_hotfix(self) -> dict:
        """
        Check for available hotfixes from the update server.

        Sends the list of applied hotfixes so the server can return
        all missing ones. Caches the result for 24 hours.
        """
        self._ensure_authenticated()

        current_version = self.get_current_version()
        applied_hotfixes = self.get_applied_hotfixes()
        current_hotfix = max(applied_hotfixes) if applied_hotfixes else 0

        try:
            response = self.session.post(
                f"{self.config.server_url}/api/v1/hotfixes/check/",
                json={
                    "current_version": current_version,
                    "current_hotfix": current_hotfix,
                    "applied_hotfixes": applied_hotfixes,
                },
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()

            # Augment with local state
            data["current_hotfix"] = current_hotfix
            data["current_version"] = current_version
            data["applied_hotfixes"] = applied_hotfixes

            # Cache the result
            from django.core.cache import cache

            cache.set("hotfix_check_result", data, timeout=86400)

            return data

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to check for hotfixes: {e}")
            raise PlatformUpdateError(f"Hotfix check failed: {e}")

    def get_hotfix_status(self) -> dict:
        """
        Get combined hotfix status for display purposes.

        Returns cached check result combined with local state.
        Does not make network calls - safe for use in views/templates.
        """
        from django.core.cache import cache

        applied_hotfixes = self.get_applied_hotfixes()
        status = {
            "current_hotfix": max(applied_hotfixes) if applied_hotfixes else 0,
            "applied_hotfixes": applied_hotfixes,
            "current_version": self.get_current_version(),
            "hotfix_available": False,
            "latest_hotfix": None,
            "missing_hotfixes": [],
        }

        cached = cache.get("hotfix_check_result")
        if cached:
            status["hotfix_available"] = cached.get("hotfix_available", False)
            status["latest_hotfix"] = cached.get("latest_hotfix")
            status["missing_hotfixes"] = cached.get("missing_hotfixes", [])

        return status
