"""
Django Client for JWT-authenticated Geocoder Service
Used by merchant installations to access the geocoder
"""

import hashlib
import logging
from typing import Any

import httpx
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone

from .jwt_auth import GeocoderJWTAuth

logger = logging.getLogger(__name__)


class GeocoderJWTClient:
    """
    Client for accessing JWT-protected geocoder service
    This would be used by each merchant's shop installation
    """

    def __init__(self, merchant_id: str | None = None, installation_uuid: str | None = None):
        """
        Initialize the geocoder client.

        Args:
            merchant_id: Override merchant ID (uses settings if not provided)
            installation_uuid: Override installation UUID (uses settings if not provided)
        """
        # Service configuration
        self.base_url = getattr(settings, "GEOCODER_SERVICE_URL", "https://geocoder.spwig.com")
        self.timeout = getattr(settings, "GEOCODER_TIMEOUT", 5.0)

        # Merchant identification
        self.merchant_id = merchant_id or getattr(settings, "MERCHANT_ID", "default")
        self.installation_uuid = installation_uuid or getattr(settings, "INSTALLATION_UUID", None)

        # JWT configuration
        self.jwt_auth = GeocoderJWTAuth()
        self.token = None
        self.token_expires = None

        # Get or generate token
        self._ensure_valid_token()

    def _ensure_valid_token(self):
        """Ensure we have a valid JWT token"""
        # Check if current token is still valid
        if self.token and self.token_expires and timezone.now() < self.token_expires:
            return  # Token still valid

        # Check if we have a stored token in settings
        stored_token = getattr(settings, "GEOCODER_JWT_TOKEN", None)
        if stored_token:
            # Verify the stored token
            is_valid, payload = self.jwt_auth.verify_token(stored_token)
            if is_valid:
                self.token = stored_token
                self.token_expires = timezone.datetime.fromtimestamp(
                    payload["exp"], tz=timezone.get_current_timezone()
                )
                return

        # Generate a new token (in production, this would request from auth server)
        # For now, generate locally for the merchant
        token_info = self.jwt_auth.generate_merchant_token(
            merchant_id=self.merchant_id,
            installation_uuid=self.installation_uuid or str(timezone.now().timestamp()),
            tier=getattr(settings, "GEOCODER_TIER", "standard"),
        )

        self.token = token_info["token"]
        self.token_expires = timezone.now() + timezone.timedelta(hours=self.jwt_auth.expiry_hours)

        # Store token for reuse
        cache.set(
            f"geocoder_token:{self.merchant_id}",
            {"token": self.token, "expires": self.token_expires.isoformat()},
            timeout=self.jwt_auth.expiry_hours * 3600,
        )

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with JWT token"""
        self._ensure_valid_token()
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "X-Merchant-ID": self.merchant_id,
            "User-Agent": f"SpwigShop/{self.merchant_id}",
        }

    async def autocomplete(
        self, query: str, limit: int = 5, country_bias: str | None = None, use_cache: bool = True
    ) -> dict[str, Any]:
        """
        Get address autocomplete suggestions.

        Args:
            query: Search query
            limit: Maximum number of suggestions
            country_bias: Country code to bias results
            use_cache: Whether to use cache

        Returns:
            Dict with suggestions
        """
        # Check local cache first
        if use_cache:
            cache_key = f"geocoder:{self.merchant_id}:{hashlib.md5(query.encode()).hexdigest()}"
            cached = cache.get(cache_key)
            if cached:
                logger.debug(f"Local cache hit for query: {query}")
                return cached

        # Prepare request data
        data = {"query": query, "limit": limit}
        if country_bias:
            data["country_bias"] = country_bias

        try:
            # Make request to geocoder service
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/v1/autocomplete",
                    json=data,
                    headers=self._get_headers(),
                    timeout=self.timeout,
                )

                if response.status_code == 401:
                    # Token expired or invalid, refresh and retry
                    logger.warning("JWT token rejected, refreshing...")
                    self.token = None
                    self._ensure_valid_token()

                    # Retry with new token
                    response = await client.post(
                        f"{self.base_url}/api/v1/autocomplete",
                        json=data,
                        headers=self._get_headers(),
                        timeout=self.timeout,
                    )

                if response.status_code == 429:
                    logger.warning(f"Rate limit exceeded for merchant {self.merchant_id}")
                    raise Exception("Rate limit exceeded. Please try again later.")

                response.raise_for_status()
                result = response.json()

                # Cache successful result
                if use_cache and result.get("suggestions"):
                    cache.set(cache_key, result, timeout=300)  # 5 minutes

                return result

        except httpx.TimeoutException:
            logger.error("Geocoder service timeout")
            raise Exception("Geocoder service is not responding")
        except Exception as e:
            logger.error(f"Geocoder request failed: {e}")
            raise

    async def get_usage(self) -> dict[str, Any]:
        """
        Get usage statistics for this merchant.

        Returns:
            Dict with usage stats
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/api/v1/usage",
                    headers=self._get_headers(),
                    timeout=self.timeout,
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Failed to get usage stats: {e}")
            return {"error": str(e)}

    def get_token_info(self) -> dict[str, Any]:
        """
        Get information about the current JWT token.

        Returns:
            Dict with token metadata
        """
        self._ensure_valid_token()
        is_valid, payload = self.jwt_auth.verify_token(self.token)

        if is_valid:
            return {
                "merchant_id": payload["sub"],
                "installation_uuid": payload["installation_uuid"],
                "tier": payload.get("tier", "standard"),
                "rate_limit": payload.get("rate_limit", 100),
                "expires_at": timezone.datetime.fromtimestamp(
                    payload["exp"], tz=timezone.get_current_timezone()
                ).isoformat(),
                "allowed_operations": payload.get("allowed_operations", []),
            }
        else:
            return {"error": "Invalid token"}


# Singleton instance for Django
_geocoder_client = None


def get_geocoder_client() -> GeocoderJWTClient:
    """
    Get or create the geocoder client instance.
    Uses Django settings for configuration.
    """
    global _geocoder_client
    if _geocoder_client is None:
        _geocoder_client = GeocoderJWTClient()
    return _geocoder_client
