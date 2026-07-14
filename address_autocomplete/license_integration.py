"""
License-based JWT Token Management for Geocoder Service
Integrates with Spwig platform licensing system
"""

import hashlib
import logging
from datetime import datetime, timedelta
from typing import Any

import httpx
import jwt
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone

from .jwt_auth import GeocoderJWTAuth

logger = logging.getLogger(__name__)


class LicenseBasedGeocoderAuth:
    """
    Manages geocoder JWT tokens based on valid Spwig licenses
    """

    def __init__(self):
        # Update server configuration
        self.update_server_url = getattr(settings, "UPDATE_SERVER_URL", "https://updates.spwig.com")
        self.update_server_api_key = getattr(settings, "UPDATE_SERVER_API_KEY", None)

        # Geocoder JWT configuration
        self.geocoder_jwt_auth = GeocoderJWTAuth()

        # License tier mapping to geocoder tiers
        self.tier_mapping = {
            "trial": "standard",  # Trial license -> standard geocoder tier
            "standard": "standard",  # Standard license -> standard geocoder tier
            "professional": "premium",  # Professional license -> premium geocoder tier
            "enterprise": "enterprise",  # Enterprise license -> enterprise geocoder tier
        }

    async def validate_license_and_get_token(
        self, license_key: str, installation_uuid: str
    ) -> dict[str, Any]:
        """
        Validate license with update server and get geocoder JWT token.

        Args:
            license_key: Spwig platform license key
            installation_uuid: Unique installation identifier

        Returns:
            Dict with token info and license details
        """
        try:
            # Check cache first
            cache_key = f"geocoder_token:{hashlib.md5(license_key.encode()).hexdigest()}"
            cached_token = cache.get(cache_key)
            if cached_token:
                logger.debug(f"Using cached token for license {license_key[:8]}...")
                return cached_token

            # Validate license with update server
            license_info = await self._validate_license(license_key, installation_uuid)

            if not license_info["is_valid"]:
                return {"success": False, "error": license_info.get("error", "Invalid license")}

            # Generate geocoder JWT token based on license tier
            geocoder_tier = self.tier_mapping.get(license_info["license_type"], "standard")

            # Create merchant ID from license key hash
            merchant_id = f"merchant_{hashlib.md5(license_key.encode()).hexdigest()[:12]}"

            # Generate JWT token
            token_info = self.geocoder_jwt_auth.generate_merchant_token(
                merchant_id=merchant_id,
                installation_uuid=installation_uuid,
                tier=geocoder_tier,
                custom_claims={
                    "license_key_hash": hashlib.sha256(license_key.encode()).hexdigest()[:16],
                    "license_type": license_info["license_type"],
                    "owner_email": license_info.get("owner_email", ""),
                },
            )

            # Prepare response
            result = {
                "success": True,
                "token": token_info["token"],
                "expires_at": token_info["expires_at"],
                "tier": geocoder_tier,
                "rate_limit": token_info["rate_limit"],
                "merchant_id": merchant_id,
                "license_type": license_info["license_type"],
            }

            # Cache for 23 hours (less than token expiry)
            cache.set(cache_key, result, timeout=23 * 3600)

            logger.info(
                f"Generated geocoder token for license {license_key[:8]}... (tier: {geocoder_tier})"
            )
            return result

        except Exception as e:
            logger.error(f"Failed to generate geocoder token: {e}")
            return {"success": False, "error": str(e)}

    async def _validate_license(self, license_key: str, installation_uuid: str) -> dict[str, Any]:
        """
        Validate license with update server.

        Args:
            license_key: Platform license key
            installation_uuid: Installation UUID

        Returns:
            Dict with license validation info
        """
        try:
            # Call update server API
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.update_server_url}/api/v1/validate-license",
                    json={"license_key": license_key, "installation_uuid": installation_uuid},
                    headers={
                        "Authorization": f"Bearer {self.update_server_api_key}"
                        if self.update_server_api_key
                        else "",
                        "Content-Type": "application/json",
                    },
                    timeout=10.0,
                )

                if response.status_code == 200:
                    data = response.json()
                    return {
                        "is_valid": True,
                        "license_type": data.get("license_type", "standard"),
                        "owner_email": data.get("owner_email", ""),
                        "expiry_date": data.get("expiry_date"),
                        "max_domains": data.get("max_domains", 1),
                    }
                else:
                    return {
                        "is_valid": False,
                        "error": f"License validation failed: {response.status_code}",
                    }

        except Exception as e:
            logger.error(f"License validation error: {e}")
            # Fallback to cached license info if available
            cached_license = cache.get(f"license:{license_key}")
            if cached_license:
                return cached_license

            return {"is_valid": False, "error": str(e)}

    def refresh_token_if_needed(self, current_token: str) -> dict[str, Any] | None:
        """
        Check if token needs refresh and refresh if necessary.

        Args:
            current_token: Current JWT token

        Returns:
            New token info if refreshed, None otherwise
        """
        try:
            # Decode token without verification to check expiry
            payload = jwt.decode(
                current_token, options={"verify_signature": False, "verify_exp": False}
            )

            # Check if token expires within next hour
            exp_time = datetime.fromtimestamp(payload["exp"])
            if exp_time - datetime.now() < timedelta(hours=1):
                # Token expiring soon, refresh it
                return self.geocoder_jwt_auth.refresh_token(current_token)

            return None

        except Exception as e:
            logger.error(f"Token refresh check failed: {e}")
            return None


class GeocoderTokenProvisioningService:
    """
    Service to automatically provision geocoder tokens for shop installations
    """

    def __init__(self):
        self.auth_manager = LicenseBasedGeocoderAuth()

    async def provision_on_startup(self) -> dict[str, Any]:
        """
        Automatically provision geocoder token on shop startup.
        Called during Django startup or license validation.

        Returns:
            Token provisioning result
        """
        # Get license from Django settings
        license_key = getattr(settings, "PLATFORM_LICENSE_KEY", None)
        installation_uuid = getattr(settings, "INSTALLATION_UUID", None)

        if not license_key:
            logger.warning("No platform license key found in settings")
            return {"success": False, "error": "No license key configured"}

        # Validate license and get token
        result = await self.auth_manager.validate_license_and_get_token(
            license_key, installation_uuid or self._generate_installation_uuid()
        )

        if result["success"]:
            # Store token in settings for use by geocoder client
            self._store_token_in_settings(result["token"])

            # Log provisioning
            logger.info(f"Geocoder token provisioned for merchant {result['merchant_id']}")

        return result

    def _generate_installation_uuid(self) -> str:
        """Generate unique installation UUID if not provided."""
        import platform
        import uuid

        # Create UUID based on hostname and timestamp
        hostname = platform.node()
        unique_str = f"{hostname}-{timezone.now().isoformat()}"
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, unique_str))

    def _store_token_in_settings(self, token: str):
        """Store token in Django settings for client use."""
        # This would typically be stored in a database or cache
        # For now, store in cache with long TTL
        cache.set("geocoder_jwt_token", token, timeout=24 * 3600)

        # Also set in settings if possible (for current session)
        if hasattr(settings, "GEOCODER_JWT_TOKEN"):
            settings.GEOCODER_JWT_TOKEN = token


class GeocoderLicenseMiddleware:
    """
    Django middleware to ensure geocoder token is available for valid licenses
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.provisioning_service = GeocoderTokenProvisioningService()
        self._token_provisioned = False

    def __call__(self, request):
        # Check if token needs provisioning (once per session)
        if not self._token_provisioned:
            # Check if we have a valid token
            token = cache.get("geocoder_jwt_token")
            if not token:
                # Provision token asynchronously
                import asyncio

                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)

                result = loop.run_until_complete(self.provisioning_service.provision_on_startup())

                if result["success"]:
                    self._token_provisioned = True
                    request.geocoder_token = result["token"]
                    request.geocoder_tier = result["tier"]

        response = self.get_response(request)
        return response
