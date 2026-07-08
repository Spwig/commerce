"""
GeoIP Service Client for Django
Provides integration with the JWT-authenticated GeoIP service
"""

import json
import hashlib
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from urllib.parse import urljoin

import requests
from django.conf import settings
from django.core.cache import cache
import jwt

logger = logging.getLogger(__name__)


class GeoIPClient:
    """Client for GeoIP service with JWT authentication"""

    def __init__(
        self,
        base_url: Optional[str] = None,
        jwt_secret: Optional[str] = None,
        jwt_algorithm: str = 'HS256',
        jwt_issuer: str = 'spwig-platform',
        timeout: int = 10,
        cache_prefix: str = 'geoip:'
    ):
        """
        Initialize GeoIP client.

        Args:
            base_url: GeoIP service URL (defaults to settings.GEOIP_SERVICE_URL)
            jwt_secret: JWT secret key (uses platform secrets from database, then env fallback)
            jwt_algorithm: JWT algorithm (default: HS256)
            jwt_issuer: JWT issuer (default: spwig-platform)
            timeout: Request timeout in seconds
            cache_prefix: Cache key prefix
        """
        self.base_url = base_url or getattr(settings, 'GEOIP_SERVICE_URL', 'http://localhost:8003')
        # Use platform secrets helper to get JWT secret (checks DB first, then env)
        if jwt_secret:
            self.jwt_secret = jwt_secret
        else:
            from core.platform_secrets import get_geoip_secret
            self.jwt_secret = get_geoip_secret()
        self.jwt_algorithm = jwt_algorithm
        self.jwt_issuer = jwt_issuer
        self.timeout = timeout
        self.cache_prefix = cache_prefix

        # Get merchant configuration from settings
        self.merchant_id = getattr(settings, 'MERCHANT_ID', self._generate_merchant_id())
        self.installation_uuid = getattr(settings, 'INSTALLATION_UUID', 'default')
        self.tier = getattr(settings, 'GEOIP_TIER', 'standard')

        # Session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Spwig-GeoIP-Client/1.0'
        })

        # Get or generate JWT token
        self._ensure_token()

    def _generate_merchant_id(self) -> str:
        """Generate merchant ID from license or domain"""
        # Try to get from license
        try:
            license_path = '/opt/shop-platform/license/license.json'
            with open(license_path, 'r') as f:
                license_data = json.load(f)
                return hashlib.sha256(
                    license_data.get('license_key', '').encode()
                ).hexdigest()[:16]
        except:
            pass

        # Fallback to domain-based ID
        domain = getattr(settings, 'ALLOWED_HOSTS', ['localhost'])[0]
        return hashlib.sha256(domain.encode()).hexdigest()[:16]

    def _ensure_token(self):
        """Ensure we have a valid JWT token"""
        # Check cache for existing token
        cache_key = f"{self.cache_prefix}jwt_token:{self.merchant_id}"
        token = cache.get(cache_key)

        if not token and self.jwt_secret:
            # Generate new token
            token = self._generate_token()
            # Cache for 23 hours (leave 1 hour buffer before expiry)
            cache.set(cache_key, token, timeout=23 * 3600)

        if token:
            self.session.headers['Authorization'] = f'Bearer {token}'

    def _generate_token(self) -> str:
        """Generate JWT token for authentication"""
        now = datetime.utcnow()
        payload = {
            'iss': self.jwt_issuer,
            'sub': self.merchant_id,
            'aud': 'geoip.spwig.com',
            'exp': (now + timedelta(hours=24)).timestamp(),
            'iat': now.timestamp(),
            'installation_uuid': self.installation_uuid,
            'tier': self.tier,
            'rate_limit': self._get_rate_limit(),
            'allowed_operations': self._get_allowed_operations()
        }
        return jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)

    def _get_rate_limit(self) -> int:
        """Get rate limit based on tier"""
        limits = {
            'standard': 1000,
            'premium': 5000,
            'enterprise': 20000
        }
        return limits.get(self.tier, 1000)

    def _get_allowed_operations(self) -> List[str]:
        """Get allowed operations based on tier"""
        operations = {
            'standard': ['lookup', 'asn'],
            'premium': ['lookup', 'asn', 'bulk'],
            'enterprise': ['lookup', 'asn', 'bulk', 'analytics']
        }
        return operations.get(self.tier, ['lookup'])

    def lookup_ip(self, ip: str, use_cache: bool = True) -> Optional[Dict[str, Any]]:
        """
        Lookup geolocation for a single IP address.

        Args:
            ip: IP address to lookup
            use_cache: Whether to use local cache

        Returns:
            Dictionary with geolocation data or None on error
        """
        # Check cache
        if use_cache:
            cache_key = f"{self.cache_prefix}ip:{ip}"
            cached = cache.get(cache_key)
            if cached:
                return cached

        # Short-circuit if we've recently seen a 429 for this merchant — avoids
        # hammering the server while the Community-tier window resets. TTL was
        # set from the Retry-After header on the previous 429.
        over_limit_key = f"{self.cache_prefix}over_limit:{self.merchant_id}"
        if cache.get(over_limit_key):
            logger.debug("GeoIP over Community-tier limit; skipping call for %s", ip)
            return None

        try:
            # Make API request
            url = urljoin(self.base_url, '/api/v1/lookup')
            response = self.session.post(
                url,
                json={'ip': ip},
                timeout=self.timeout
            )

            if response.status_code == 200:
                data = response.json()

                # Cache result
                if use_cache:
                    cache_ttl = {
                        'standard': 3600,
                        'premium': 7200,
                        'enterprise': 14400
                    }.get(self.tier, 3600)
                    cache.set(cache_key, data, timeout=cache_ttl)

                return data

            elif response.status_code == 401:
                logger.error("GeoIP authentication failed - regenerating token")
                # Clear cached token and regenerate
                token_cache_key = f"{self.cache_prefix}jwt_token:{self.merchant_id}"
                cache.delete(token_cache_key)
                self._ensure_token()
                # Retry once with new token
                response = self.session.post(
                    url,
                    json={'ip': ip},
                    timeout=self.timeout
                )
                if response.status_code == 200:
                    data = response.json()
                    if use_cache:
                        ip_cache_key = f"{self.cache_prefix}ip:{ip}"
                        cache_ttl = {
                            'standard': 3600,
                            'premium': 7200,
                            'enterprise': 14400
                        }.get(self.tier, 3600)
                        cache.set(ip_cache_key, data, timeout=cache_ttl)
                    return data
                return None

            elif response.status_code == 429:
                # Community/paid tier hit its quota — cache the over-limit
                # state so we short-circuit subsequent calls until reset.
                retry_after = int(response.headers.get('Retry-After', 60))
                cache.set(over_limit_key, True, timeout=retry_after)
                # Log at DEBUG (not ERROR) — this is expected behaviour for
                # Community merchants approaching the tier cap.
                logger.debug(
                    "GeoIP over tier limit; retry after %ds. Response: %s",
                    retry_after, response.text[:200],
                )
                return None

            else:
                logger.error(f"GeoIP lookup failed: {response.status_code}")
                return None

        except requests.RequestException as e:
            logger.error(f"GeoIP request error: {e}")
            return None

    def bulk_lookup(self, ips: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Bulk lookup for multiple IP addresses.

        Args:
            ips: List of IP addresses (max 100)

        Returns:
            Dictionary mapping IP to geolocation data
        """
        if len(ips) > 100:
            logger.warning(f"Bulk lookup limited to 100 IPs, got {len(ips)}")
            ips = ips[:100]

        # Short-circuit if we've recently seen a 429 for this merchant
        over_limit_key = f"{self.cache_prefix}over_limit:{self.merchant_id}"
        if cache.get(over_limit_key):
            logger.debug("GeoIP over tier limit; skipping bulk lookup")
            return {}

        try:
            url = urljoin(self.base_url, '/api/v1/bulk')
            response = self.session.post(
                url,
                json={'ips': ips},
                timeout=self.timeout * 2  # Longer timeout for bulk
            )

            if response.status_code == 200:
                data = response.json()
                # Convert list to dict keyed by IP
                result = {}
                for item in data.get('results', []):
                    result[item['ip']] = item
                return result

            elif response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 60))
                cache.set(over_limit_key, True, timeout=retry_after)
                logger.debug("GeoIP over tier limit on bulk; retry after %ds", retry_after)
                return {}

            else:
                logger.error(f"Bulk lookup failed: {response.status_code}")
                return {}

        except requests.RequestException as e:
            logger.error(f"Bulk lookup error: {e}")
            return {}

    def get_asn_info(self, asn: int) -> Optional[Dict[str, Any]]:
        """
        Get information about an Autonomous System Number.

        Args:
            asn: AS number to lookup

        Returns:
            Dictionary with ASN information or None on error
        """
        # Check cache
        cache_key = f"{self.cache_prefix}asn:{asn}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        try:
            url = urljoin(self.base_url, f'/api/v1/asn/{asn}')
            response = self.session.get(url, timeout=self.timeout)

            if response.status_code == 200:
                data = response.json()
                # Cache for 24 hours (ASN info changes rarely)
                cache.set(cache_key, data, timeout=86400)
                return data

            else:
                logger.error(f"ASN lookup failed: {response.status_code}")
                return None

        except requests.RequestException as e:
            logger.error(f"ASN lookup error: {e}")
            return None

    def get_stats(self) -> Optional[Dict[str, Any]]:
        """
        Get GeoIP database statistics.

        Returns:
            Dictionary with statistics or None on error
        """
        try:
            url = urljoin(self.base_url, '/api/v1/stats')
            response = self.session.get(url, timeout=self.timeout)

            if response.status_code == 200:
                return response.json()
            else:
                return None

        except requests.RequestException:
            return None

    def get_usage(self) -> Optional[Dict[str, Any]]:
        """
        Get usage statistics for the merchant.

        Returns:
            Dictionary with usage stats or None on error
        """
        try:
            url = urljoin(self.base_url, '/api/v1/usage')
            response = self.session.get(url, timeout=self.timeout)

            if response.status_code == 200:
                return response.json()
            else:
                return None

        except requests.RequestException:
            return None

    def close(self):
        """Close the session"""
        self.session.close()


# Convenience function for one-off lookups
def lookup_ip(ip: str) -> Optional[Dict[str, Any]]:
    """
    Quick IP lookup using default client.

    Args:
        ip: IP address to lookup

    Returns:
        Geolocation data dictionary or None
    """
    client = GeoIPClient()
    try:
        return client.lookup_ip(ip)
    finally:
        client.close()


# Context manager support
class GeoIPContext:
    """Context manager for GeoIP client"""

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.client = None

    def __enter__(self) -> GeoIPClient:
        self.client = GeoIPClient(**self.kwargs)
        return self.client

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            self.client.close()