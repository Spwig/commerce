"""
Secured Address Autocomplete Service Client
Includes IP restriction and API key authentication
"""
import hashlib
import httpx
import json
from typing import Dict, Any, Optional, List
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class SecuredAutocompleteClient:
    """
    Secured client for address autocomplete service
    Supports both IP restriction and API key authentication
    """

    def __init__(self):
        # Service configuration
        self.base_url = getattr(settings, 'ADDRESS_AUTOCOMPLETE_URL', 'http://geocoder.spwig.com')
        self.api_key = getattr(settings, 'ADDRESS_AUTOCOMPLETE_API_KEY', None)
        self.timeout = getattr(settings, 'ADDRESS_AUTOCOMPLETE_TIMEOUT', 5.0)
        self.cache_ttl = getattr(settings, 'ADDRESS_AUTOCOMPLETE_CACHE_TTL', 300)

        # Security settings
        self.require_https = getattr(settings, 'ADDRESS_AUTOCOMPLETE_REQUIRE_HTTPS', False)
        self.verify_ssl = getattr(settings, 'ADDRESS_AUTOCOMPLETE_VERIFY_SSL', True)

        # Validate configuration
        if self.require_https and not self.base_url.startswith('https://'):
            raise ValueError("HTTPS required but base_url is not HTTPS")

    def _get_headers(self) -> Dict[str, str]:
        """Build request headers with authentication"""
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': f'SpwigShop/{settings.VERSION if hasattr(settings, "VERSION") else "1.0"}'
        }

        # Add API key if configured
        if self.api_key:
            headers['X-API-Key'] = self.api_key

        return headers

    def _get_cache_key(self, operation: str, params: Dict) -> str:
        """Generate cache key for request"""
        # Create deterministic cache key
        param_str = json.dumps(params, sort_keys=True)
        hash_str = hashlib.md5(param_str.encode()).hexdigest()
        return f'geocoder:{operation}:{hash_str}'

    async def _make_request(self, endpoint: str, data: Dict, use_cache: bool = True) -> Dict[str, Any]:
        """Make authenticated request to geocoder service"""
        url = f"{self.base_url}{endpoint}"

        # Check cache first
        if use_cache:
            cache_key = self._get_cache_key(endpoint, data)
            cached_result = cache.get(cache_key)
            if cached_result:
                logger.debug(f"Cache hit for {endpoint}")
                return cached_result

        try:
            async with httpx.AsyncClient(verify=self.verify_ssl) as client:
                response = await client.post(
                    url,
                    json=data,
                    headers=self._get_headers(),
                    timeout=self.timeout
                )

                if response.status_code == 403:
                    logger.error("Access denied - check API key or IP restrictions")
                    raise PermissionError("Access denied to geocoder service")

                response.raise_for_status()
                result = response.json()

                # Cache successful result
                if use_cache:
                    cache.set(cache_key, result, self.cache_ttl)

                return result

        except httpx.TimeoutException:
            logger.error(f"Timeout calling {endpoint}")
            raise TimeoutError(f"Geocoder service timeout")
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error calling {endpoint}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error calling geocoder service: {e}")
            raise

    async def autocomplete(self,
                          query: str,
                          country_bias: Optional[str] = None,
                          lat: Optional[float] = None,
                          lon: Optional[float] = None,
                          limit: int = 5) -> Dict[str, Any]:
        """
        Get address suggestions with authentication
        """
        data = {
            "query": query,
            "limit": limit
        }

        if country_bias:
            data["country_bias"] = country_bias
        if lat and lon:
            data["lat"] = lat
            data["lon"] = lon

        return await self._make_request("/api/v1/autocomplete", data)

    async def validate_address(self, address_data: Dict) -> Dict[str, Any]:
        """
        Validate address with authentication
        """
        return await self._make_request("/api/v1/validate", address_data)

    async def normalize_address(self, address_text: str) -> Dict[str, Any]:
        """
        Normalize address with authentication
        """
        data = {"address": address_text}
        return await self._make_request("/api/v1/normalize", data)

    async def reverse_geocode(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Reverse geocode coordinates with authentication
        """
        data = {"lat": lat, "lon": lon}
        return await self._make_request("/api/v1/reverse", data)

    def test_connection(self) -> bool:
        """
        Test connection and authentication
        Returns True if service is accessible
        """
        try:
            import requests
            response = requests.get(
                f"{self.base_url}/health",
                headers=self._get_headers(),
                timeout=self.timeout,
                verify=self.verify_ssl
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False


class SecuredAddressEnhancer:
    """
    Enhanced address handling with security
    """

    def __init__(self):
        self.client = SecuredAutocompleteClient()

    async def enhance_checkout_address(self, address_data: Dict) -> Dict:
        """
        Enhance address data during checkout with validation
        """
        try:
            # Validate the address
            validation_result = await self.client.validate_address(address_data)

            if validation_result.get('is_valid'):
                # Return normalized address
                return validation_result.get('normalized', address_data)
            else:
                # Log validation issues
                issues = validation_result.get('issues', [])
                logger.warning(f"Address validation issues: {issues}")
                return address_data

        except PermissionError:
            # Authentication failed - log and continue without enhancement
            logger.error("Geocoder authentication failed - check API key")
            return address_data
        except Exception as e:
            # Log error and return original address
            logger.error(f"Failed to enhance address: {e}")
            return address_data

    def verify_service_access(self) -> Dict[str, Any]:
        """
        Verify service access and return status
        """
        status = {
            'accessible': False,
            'authenticated': False,
            'error': None
        }

        try:
            # Test basic connection
            if self.client.test_connection():
                status['accessible'] = True
                status['authenticated'] = True
            else:
                status['error'] = 'Service not accessible'
        except PermissionError:
            status['accessible'] = True
            status['error'] = 'Authentication failed'
        except Exception as e:
            status['error'] = str(e)

        return status