"""
Address Autocomplete Service Client for Django
"""
import os
import logging
import hashlib
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from django.conf import settings
from django.core.cache import cache
from django.contrib.sites.models import Site
from django.utils import timezone
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from .jwt_auth import GeocoderJWTAuth

logger = logging.getLogger(__name__)

class AutocompleteClient:
    """Client for interacting with the address autocomplete service"""

    def __init__(self, prewarm_token=False):
        self.base_url = getattr(
            settings,
            'ADDRESS_AUTOCOMPLETE_URL',
            os.getenv('ADDRESS_AUTOCOMPLETE_URL', 'http://localhost:8001')
        )
        # Get configuration from settings
        config = getattr(settings, 'ADDRESS_AUTOCOMPLETE_CONFIG', {})
        self.timeout = config.get('request_timeout', 5.0)
        self.cache_ttl = config.get('cache_timeout', 300)
        self.max_suggestions = config.get('max_suggestions', 10)
        self.client = httpx.Client(timeout=self.timeout)

        # JWT authentication setup
        self.jwt_auth = GeocoderJWTAuth()
        self._cached_token = None
        self._token_expiry = None

        # Pre-warm token to avoid first-request delay
        if prewarm_token:
            self._get_jwt_token()

    def _is_service_available(self) -> bool:
        """Check if the Spwig geocoder service should be available based on maintenance status."""
        try:
            from core.license import get_license_manager
            return get_license_manager().are_spwig_services_available()
        except Exception:
            return True  # Fail open - don't break autocomplete on import errors

    def _get_cache_key(self, operation: str, params: dict) -> str:
        """Generate cache key for operation"""
        param_str = '-'.join(f"{k}:{v}" for k, v in sorted(params.items()))
        if len(param_str) > 200:
            param_str = hashlib.md5(param_str.encode()).hexdigest()
        return f"address_autocomplete:{operation}:{param_str}"

    def _get_installation_uuid(self) -> str:
        """
        Get or create installation UUID for geocoder service authentication.
        Uses SiteSettings model for persistent storage.
        """
        from core.models import SiteSettings
        return SiteSettings.get_installation_uuid()

    def _get_merchant_id(self) -> str:
        """
        Get unique merchant identifier based on site domain.
        """
        try:
            site = Site.objects.get_current()
            return f"shop-{site.domain}"
        except Exception as e:
            logger.warning(f"Failed to get site domain for merchant_id: {e}")
            return "shop-localhost"

    def _get_jwt_token(self) -> Optional[str]:
        """
        Get cached JWT token or generate a new one if expired.
        Returns None if token generation fails.
        """
        # Check if we have a cached token that's still valid (with 5 min buffer)
        if self._cached_token and self._token_expiry:
            buffer_time = timezone.now() + timedelta(minutes=5)
            if self._token_expiry > buffer_time:
                logger.debug(f"Using cached JWT token for merchant {self._get_merchant_id()}")
                return self._cached_token

        # Generate new token
        return self._generate_token()

    def _generate_token(self) -> Optional[str]:
        """
        Generate a new JWT token for geocoder service authentication.
        Caches the token for future use.
        """
        try:
            merchant_id = self._get_merchant_id()
            installation_uuid = self._get_installation_uuid()

            # Generate token
            token_info = self.jwt_auth.generate_merchant_token(
                merchant_id=merchant_id,
                installation_uuid=installation_uuid,
                tier='standard'
            )

            # Cache token and expiry
            self._cached_token = token_info['token']
            # Parse expiry time (it's in ISO format)
            expiry_str = token_info['expires_at']
            self._token_expiry = datetime.fromisoformat(expiry_str.replace('Z', '+00:00'))

            logger.info(
                f"Generated geocoder JWT for {merchant_id}, "
                f"tier: {token_info['tier']}, "
                f"expires: {expiry_str}"
            )

            return self._cached_token

        except Exception as e:
            logger.error(f"Failed to generate geocoder token: {e}")
            return None

    def _clear_token_cache(self):
        """Clear cached token to force regeneration on next request"""
        self._cached_token = None
        self._token_expiry = None
        logger.debug("Cleared JWT token cache")

    def _get_headers(self, user_tier: str = "anonymous") -> dict:
        """Get request headers with JWT authentication"""
        headers = {
            "X-User-Tier": user_tier,
            "Accept": "application/json"
        }

        # Add JWT token for authentication
        token = self._get_jwt_token()
        if token:
            headers["Authorization"] = f"Bearer {token}"
        else:
            logger.warning("No JWT token available for geocoder request")

        return headers

    # ------------------------------------------------------------------
    # Community-tier over-limit tracking
    # ------------------------------------------------------------------
    # When the geocoder returns 429 (Community per-minute or per-day cap hit),
    # cache the "over limit" state locally for the Retry-After window. All
    # geocoder methods short-circuit while the cache entry exists — avoids
    # hammering the server and lets the UI degrade gracefully.

    def _over_limit_cache_key(self) -> str:
        # Key off installation_uuid (globally unique per install) rather than
        # the site-domain-derived merchant_id, so multiple un-configured
        # installs don't share a single "shop-localhost" over-limit key.
        return f"geocoder:over_limit:{self._get_installation_uuid()}"

    def _is_over_limit(self) -> bool:
        return bool(cache.get(self._over_limit_cache_key()))

    def _mark_over_limit(self, response) -> None:
        retry_after = int(response.headers.get('Retry-After', 60))
        cache.set(self._over_limit_cache_key(), True, timeout=retry_after)
        logger.debug("Geocoder over tier limit; cached for %ds", retry_after)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5))
    def autocomplete(
        self,
        query: str,
        country_bias: Optional[str] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        limit: int = 5,
        user_tier: str = "anonymous",
        is_postcode: bool = False
    ) -> Dict[str, Any]:
        """
        Get address autocomplete suggestions

        Args:
            query: Search query (minimum 3 characters)
            country_bias: ISO country code for biasing results
            lat: Latitude for geo-biasing
            lon: Longitude for geo-biasing
            limit: Maximum number of suggestions
            user_tier: User tier for rate limiting
            is_postcode: If True, treat query as postcode/postal code lookup

        Returns:
            Dict with suggestions and metadata
        """
        # Check if service is available (maintenance status)
        if not self._is_service_available():
            logger.debug("Geocoder service disabled: maintenance expired")
            return {"suggestions": [], "service_unavailable": True}

        # Community-tier over-limit short-circuit — avoids hammering the
        # server while the tier window resets.
        if self._is_over_limit():
            return {"suggestions": [], "error": "over_tier_limit"}

        if len(query) < 3:
            return {"suggestions": [], "error": "Query too short"}

        # Check cache
        cache_params = {
            "query": query,
            "country": country_bias,
            "lat": lat,
            "lon": lon,
            "limit": limit,
            "is_postcode": is_postcode
        }
        cache_key = self._get_cache_key("autocomplete", cache_params)
        cached_result = cache.get(cache_key)

        if cached_result:
            logger.debug(f"Cache hit for autocomplete: {query}")
            return cached_result

        try:
            # Prepare request body with all parameters
            request_data = {
                "query": query,
                "limit": limit
            }

            # Add optional parameters to request body
            if country_bias:
                request_data["country_bias"] = country_bias
            if lat and lon:
                request_data["lat"] = lat
                request_data["lon"] = lon
            if is_postcode:
                request_data["postalcode"] = query
                request_data["addressdetails"] = 1  # Get full address details for postcodes

            # Make request
            response = self.client.post(
                f"{self.base_url}/api/v1/autocomplete",
                json=request_data,
                headers=self._get_headers(user_tier)
            )

            if response.status_code == 401:
                # Authentication failed - clear token cache and retry once
                logger.warning("Geocoder authentication failed, clearing token cache")
                self._clear_token_cache()
                # Retry with new token
                response = self.client.post(
                    f"{self.base_url}/api/v1/autocomplete",
                    json=request_data,
                    headers=self._get_headers(user_tier)
                )

            if response.status_code == 429:
                self._mark_over_limit(response)
                return {"suggestions": [], "error": "Rate limit exceeded"}

            response.raise_for_status()
            data = response.json()

            # Cache successful result
            cache.set(cache_key, data, self.cache_ttl)
            logger.debug(f"Cached autocomplete result for: {query}")

            return data

        except httpx.TimeoutException:
            logger.error(f"Autocomplete timeout for query: {query}")
            return {"suggestions": [], "error": "Service timeout"}
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                logger.error(f"Geocoder authentication failed for merchant {self._get_merchant_id()}")
                return {"suggestions": [], "error": "Authentication failed"}
            logger.error(f"Autocomplete HTTP error: {e}")
            return {"suggestions": [], "error": "Service error"}
        except Exception as e:
            logger.error(f"Autocomplete error: {str(e)}")
            return {"suggestions": [], "error": "Service error"}

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5))
    def normalize_address(
        self,
        address: str,
        user_tier: str = "anonymous"
    ) -> Dict[str, Any]:
        """
        Normalize and parse an address

        Args:
            address: Raw address string
            user_tier: User tier for rate limiting

        Returns:
            Dict with normalized address and components
        """
        if not self._is_service_available():
            return {"error": "Service unavailable (maintenance expired)"}

        if self._is_over_limit():
            return {"normalized": address, "components": {}, "error": "over_tier_limit"}

        # Check cache
        cache_key = self._get_cache_key("normalize", {"address": address})
        cached_result = cache.get(cache_key)

        if cached_result:
            logger.debug(f"Cache hit for normalize: {address}")
            return cached_result

        try:
            response = self.client.post(
                f"{self.base_url}/api/v1/normalize",
                json={"address": address},
                headers=self._get_headers(user_tier)
            )

            if response.status_code == 401:
                # Authentication failed - clear token cache and retry once
                logger.warning("Geocoder authentication failed during normalize, clearing token cache")
                self._clear_token_cache()
                response = self.client.post(
                    f"{self.base_url}/api/v1/normalize",
                    json={"address": address},
                    headers=self._get_headers(user_tier)
                )

            if response.status_code == 429:
                self._mark_over_limit(response)
                return {
                    "normalized": address,
                    "components": {},
                    "error": "Rate limit exceeded"
                }

            response.raise_for_status()
            data = response.json()

            # Cache successful result
            cache.set(cache_key, data, self.cache_ttl * 2)  # Cache longer for normalization

            return data

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                logger.error(f"Geocoder authentication failed during normalize")
                return {
                    "normalized": address,
                    "components": {},
                    "error": "Authentication failed"
                }
            logger.error(f"Normalize HTTP error: {e}")
            return {
                "normalized": address,
                "components": {},
                "error": str(e)
            }
        except Exception as e:
            logger.error(f"Normalize error: {str(e)}")
            return {
                "normalized": address,
                "components": {},
                "error": str(e)
            }

    def validate_address(
        self,
        address_data: Dict[str, str],
        user_tier: str = "anonymous"
    ) -> Dict[str, Any]:
        """
        Validate an address using the autocomplete service

        Args:
            address_data: Dict with address fields
            user_tier: User tier for rate limiting

        Returns:
            Dict with validation result
        """
        if not self._is_service_available():
            return {"valid": True, "error": "Validation unavailable (maintenance expired)"}

        # Build address string
        address_parts = []
        for field in ["address1", "address2", "city", "state", "postal_code", "country"]:
            if address_data.get(field):
                address_parts.append(address_data[field])

        address = ", ".join(address_parts)

        try:
            response = self.client.get(
                f"{self.base_url}/api/v1/validate",
                params={
                    "address": address,
                    "country": address_data.get("country")
                },
                headers=self._get_headers(user_tier)
            )

            if response.status_code == 401:
                logger.warning("Geocoder authentication failed during validate, clearing token cache")
                self._clear_token_cache()
                response = self.client.get(
                    f"{self.base_url}/api/v1/validate",
                    params={
                        "address": address,
                        "country": address_data.get("country")
                    },
                    headers=self._get_headers(user_tier)
                )

            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                logger.error("Geocoder authentication failed during validate")
                return {
                    "valid": False,
                    "errors": ["Authentication failed"],
                    "normalized": {}
                }
            logger.error(f"Validation HTTP error: {e}")
            return {
                "valid": False,
                "errors": [str(e)],
                "normalized": {}
            }
        except Exception as e:
            logger.error(f"Validation error: {str(e)}")
            return {
                "valid": False,
                "errors": [str(e)],
                "normalized": {}
            }

    def reverse_geocode(
        self,
        lat: float,
        lon: float,
        user_tier: str = "anonymous"
    ) -> Dict[str, Any]:
        """
        Reverse geocode coordinates to address

        Args:
            lat: Latitude
            lon: Longitude
            user_tier: User tier for rate limiting

        Returns:
            Dict with address information
        """
        if not self._is_service_available():
            return {"error": "Service unavailable (maintenance expired)"}

        # Check cache
        cache_key = self._get_cache_key("reverse", {"lat": lat, "lon": lon})
        cached_result = cache.get(cache_key)

        if cached_result:
            return cached_result

        try:
            response = self.client.get(
                f"{self.base_url}/api/v1/reverse",
                params={"lat": lat, "lon": lon},
                headers=self._get_headers(user_tier)
            )

            if response.status_code == 401:
                logger.warning("Geocoder authentication failed during reverse geocode, clearing token cache")
                self._clear_token_cache()
                response = self.client.get(
                    f"{self.base_url}/api/v1/reverse",
                    params={"lat": lat, "lon": lon},
                    headers=self._get_headers(user_tier)
                )

            response.raise_for_status()
            data = response.json()

            # Cache result
            cache.set(cache_key, data, self.cache_ttl * 4)  # Cache longer for reverse geocoding

            return data

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                logger.error("Geocoder authentication failed during reverse geocode")
                return {"error": "Authentication failed"}
            logger.error(f"Reverse geocoding HTTP error: {e}")
            return {"error": str(e)}
        except Exception as e:
            logger.error(f"Reverse geocoding error: {str(e)}")
            return {"error": str(e)}

    def get_service_health(self) -> Dict[str, Any]:
        """Check health of autocomplete service"""
        try:
            response = self.client.get(f"{self.base_url}/health")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

    def close(self):
        """Close HTTP client"""
        self.client.close()


class AddressEnhancer:
    """Enhance existing address service with autocomplete capabilities"""

    def __init__(self, client=None):
        self.client = client if client is not None else AutocompleteClient(prewarm_token=True)

    def enhance_address_data(
        self,
        address_data: Dict[str, Any],
        user_tier: str = "anonymous"
    ) -> Dict[str, Any]:
        """
        Enhance address data with normalized components and geocoding

        Args:
            address_data: Original address data
            user_tier: User tier

        Returns:
            Enhanced address data
        """
        # Build address string
        address_parts = []
        for field in ["address1", "address2", "city", "state", "postal_code", "country"]:
            if address_data.get(field):
                address_parts.append(str(address_data[field]))

        address_string = ", ".join(address_parts)

        # Normalize address
        normalized = self.client.normalize_address(address_string, user_tier)

        # Enhance data
        enhanced = address_data.copy()
        enhanced["normalized_address"] = normalized.get("normalized", address_string)
        enhanced["address_components"] = normalized.get("components", {})
        enhanced["validation_confidence"] = normalized.get("confidence", 0.0)

        # Try to get coordinates if not present
        if not enhanced.get("latitude") or not enhanced.get("longitude"):
            # Use autocomplete to get coordinates
            suggestions = self.client.autocomplete(
                query=address_string,
                country_bias=address_data.get("country"),
                limit=1,
                user_tier=user_tier
            )

            if suggestions.get("suggestions"):
                first_suggestion = suggestions["suggestions"][0]
                if first_suggestion.get("centroid"):
                    enhanced["latitude"] = first_suggestion["centroid"]["lat"]
                    enhanced["longitude"] = first_suggestion["centroid"]["lon"]

        return enhanced

    def validate_and_enhance(
        self,
        address_data: Dict[str, Any],
        user_tier: str = "anonymous"
    ) -> tuple[bool, Dict[str, Any], List[str]]:
        """
        Validate and enhance address data

        Args:
            address_data: Address data to validate
            user_tier: User tier

        Returns:
            Tuple of (is_valid, enhanced_data, errors)
        """
        errors = []

        # Basic validation
        required_fields = ["address1", "city", "postal_code", "country"]
        for field in required_fields:
            if not address_data.get(field):
                errors.append(f"Missing required field: {field}")

        if errors:
            return False, address_data, errors

        # Enhance data
        enhanced = self.enhance_address_data(address_data, user_tier)

        # Validate with service
        validation_result = self.client.validate_address(enhanced, user_tier)

        if not validation_result.get("valid"):
            errors.extend(validation_result.get("errors", ["Invalid address"]))

        return len(errors) == 0, enhanced, errors