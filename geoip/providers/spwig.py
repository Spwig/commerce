"""
Spwig GeoIP Provider
High-accuracy GeoIP service with BGP routing data
"""

import logging
from typing import Any

from django.conf import settings

from ..client import GeoIPClient
from .base import GeoIPProviderBase

logger = logging.getLogger(__name__)


class SpwigProvider(GeoIPProviderBase):
    """
    Spwig GeoIP Provider - Production GeoIP service with BGP data

    Features:
    - 98% accuracy with BGP routing data
    - 458K+ IP ranges from RIR registries
    - 135K+ BGP prefixes from 13K+ ASNs
    - JWT authentication with shared platform secret
    - No setup required - works out of the box
    """

    def __init__(self, config: dict[str, Any] = None):
        """Initialize Spwig provider"""
        super().__init__(config)
        self.name = "Spwig GeoIP"
        self.client = None

        # Get configuration from settings or use defaults
        self.base_url = getattr(settings, "GEOIP_SERVICE_URL", "https://geoip.spwig.com")
        self.jwt_secret = getattr(settings, "GEOIP_JWT_SECRET_KEY", None)

        # Get JWT secret from geocoder if not explicitly set
        if not self.jwt_secret:
            self.jwt_secret = getattr(settings, "GEOCODER_JWT_SECRET", None)

    def initialize(self) -> bool:
        """
        Initialize the Spwig GeoIP client

        Returns:
            True if initialization successful
        """
        try:
            # Initialize the GeoIP client
            self.client = GeoIPClient(
                base_url=self.base_url,
                jwt_secret=self.jwt_secret,
                jwt_issuer="spwig-platform",
                timeout=10,
                cache_prefix="spwig_geoip:",
            )

            # Test connection with a health check
            try:
                import requests

                response = requests.get(f"{self.base_url}/health", timeout=5)
                if response.status_code == 200:
                    health = response.json()
                    if health.get("status") == "healthy":
                        logger.info(
                            f"Spwig GeoIP initialized successfully - Database: {health.get('services', {}).get('database', {}).get('ip_ranges', 0):,} IP ranges"
                        )
                        self._initialized = True
                        return True
            except Exception as e:
                logger.debug(f"Health check failed (non-critical): {e}")
                # Still mark as initialized even if health check fails
                # The service might be behind a firewall
                self._initialized = True
                return True

        except Exception as e:
            logger.error(f"Failed to initialize Spwig GeoIP provider: {e}")
            self._last_error = str(e)
            return False

    def lookup(self, ip: str) -> dict[str, Any] | None:
        """
        Perform IP lookup using Spwig GeoIP service

        Args:
            ip: IP address to lookup

        Returns:
            Dictionary with location data or None if not found
        """
        if not self._initialized or not self.client:
            logger.warning("Spwig provider not initialized")
            return None

        if not self.validate_ip(ip):
            logger.warning(f"Invalid IP address: {ip}")
            return None

        try:
            # Use the client to perform lookup
            result = self.client.lookup_ip(ip, use_cache=True)

            if result:
                # Check if this is a private/internal IP response
                is_private_network = result.get("data_source") == "private_network"

                # For private IPs, return minimal response to signal internal IP
                if is_private_network:
                    return {
                        "country_code": None,
                        "source": "private_network",
                        "data_source": "private_network",
                        "confidence": 0.0,
                        "is_internal_ip": True,
                    }

                # Format response to standard structure for regular IPs
                formatted = self.format_response(
                    {
                        "country_code": result.get("country_code"),
                        "country_name": result.get("country_name"),
                        "region_code": result.get("region_code"),
                        "region_name": result.get("region_name"),
                        "city_name": result.get("city"),
                        "postal_code": result.get("postal_code"),
                        "latitude": result.get("latitude"),
                        "longitude": result.get("longitude"),
                        "asn": result.get("asn"),
                        "isp": result.get("asn_name") or result.get("organization"),
                        "is_vpn": result.get("is_vpn", False),
                        "is_proxy": result.get("is_proxy", False),
                        "is_tor": result.get("is_tor", False),
                        "is_mobile": result.get("is_mobile", False),
                    }
                )

                # Add provider metadata
                if formatted:
                    formatted["source"] = "spwig"
                    formatted["data_source"] = result.get("data_source", "RIR+BGP")
                    # Use confidence from API if available, otherwise default based on data source
                    formatted["confidence"] = result.get("confidence") or (
                        0.98 if result.get("data_source") == "BGP" else 0.95
                    )
                    # Add data_sources array if available (multi-source cascade info)
                    if result.get("data_sources"):
                        formatted["data_sources"] = result.get("data_sources")
                    # Add anycast metadata
                    if result.get("is_anycast"):
                        formatted["is_anycast"] = True
                        if result.get("asn_country"):
                            formatted["asn_country"] = result.get("asn_country")

                return formatted

        except Exception as e:
            logger.error(f"Spwig GeoIP lookup failed for {ip}: {e}")
            self._last_error = str(e)

        return None

    def is_available(self) -> bool:
        """
        Check if Spwig provider is available

        Returns:
            True if provider can perform lookups
        """
        # Check maintenance status - disable if maintenance expired past grace period
        try:
            from core.license import get_license_manager

            if not get_license_manager().are_spwig_services_available():
                logger.debug("Spwig GeoIP provider disabled: maintenance expired")
                return False
        except Exception:
            pass  # Fail open - don't break GeoIP on import errors

        return self._initialized and self.client is not None

    def close(self):
        """Cleanup resources"""
        if self.client:
            self.client.close()
            self.client = None
        self._initialized = False

    def get_stats(self) -> dict[str, Any]:
        """
        Get provider statistics

        Returns:
            Dictionary with provider stats
        """
        stats = {
            "name": self.name,
            "available": self.is_available(),
            "accuracy": "98%",
            "coverage": "Global",
            "data_sources": ["RIR", "BGP"],
        }

        # Try to get live stats from service
        if self.client:
            try:
                service_stats = self.client.get_stats()
                if service_stats:
                    stats.update(
                        {
                            "ip_ranges": service_stats.get("ip_ranges", 0),
                            "bgp_prefixes": service_stats.get("bgp_prefixes", 0),
                            "countries": service_stats.get("countries", 0),
                            "asns": service_stats.get("asns", 0),
                        }
                    )
            except Exception:
                pass

        return stats

    def __str__(self):
        """String representation"""
        return f"SpwigProvider (BGP-enhanced, {'Active' if self.is_available() else 'Inactive'})"
