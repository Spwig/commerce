"""
Base provider class for GeoIP resolution
"""

import ipaddress
import logging
import time
from abc import ABC, abstractmethod
from typing import Any

logger = logging.getLogger(__name__)


class GeoIPProviderBase(ABC):
    """
    Abstract base class for GeoIP providers
    """

    def __init__(self, config: dict[str, Any] = None):
        """
        Initialize provider with optional configuration

        Args:
            config: Provider-specific configuration dictionary
        """
        self.config = config or {}
        self.name = self.__class__.__name__
        self._initialized = False
        self._last_error = None

    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialize the provider (load databases, connect to services, etc.)

        Returns:
            True if initialization successful, False otherwise
        """
        pass

    @abstractmethod
    def lookup(self, ip: str) -> dict[str, Any] | None:
        """
        Perform IP lookup

        Args:
            ip: IP address to lookup

        Returns:
            Dictionary with location data or None if not found
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if provider is available and ready

        Returns:
            True if provider can perform lookups, False otherwise
        """
        pass

    def close(self):  # noqa: B027 — optional hook; default no-op for providers with no resources
        """
        Cleanup resources (databases, connections, etc.)
        Override if needed
        """
        pass

    def get_ip_prefix(self, ip: str) -> str:
        """
        Get IP prefix for caching

        Args:
            ip: IP address

        Returns:
            IP prefix string
        """
        try:
            addr = ipaddress.ip_address(ip)
            if addr.version == 4:
                # Use /24 prefix for IPv4
                network = ipaddress.ip_network(f"{ip}/24", strict=False)
            else:
                # Use /48 prefix for IPv6
                network = ipaddress.ip_network(f"{ip}/48", strict=False)
            return str(network)
        except Exception as e:
            logger.warning(f"Failed to get IP prefix for {ip}: {e}")
            return ip

    def validate_ip(self, ip: str) -> bool:
        """
        Validate IP address

        Args:
            ip: IP address to validate

        Returns:
            True if valid, False otherwise
        """
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

    def standardize_country_code(self, code: str) -> str:
        """
        Standardize country code to ISO 3166-1 alpha-2

        Args:
            code: Country code

        Returns:
            Standardized 2-letter country code
        """
        if not code:
            return ""
        return code.upper()[:2]

    def measure_lookup_time(self, func):
        """
        Decorator to measure lookup time
        """

        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            elapsed = (time.time() - start) * 1000  # Convert to ms
            if result:
                result["lookup_time_ms"] = elapsed
            return result

        return wrapper

    def get_confidence_score(self, data: dict[str, Any]) -> float:
        """
        Calculate confidence score based on available data

        Args:
            data: Location data

        Returns:
            Confidence score between 0 and 1
        """
        if not data:
            return 0.0

        score = 0.0
        weights = {
            "country": 0.3,
            "region": 0.2,
            "city": 0.2,
            "postal_code": 0.1,
            "lat": 0.1,
            "lon": 0.1,
        }

        for field, weight in weights.items():
            if data.get(field):
                score += weight

        return min(score, 1.0)

    def format_response(self, data: dict[str, Any]) -> dict[str, Any]:
        """
        Format response to standard structure

        Args:
            data: Raw location data

        Returns:
            Standardized location dictionary
        """
        if not data:
            return None

        # Map common field names to standard ones
        field_mapping = {
            "country": "country_code",
            "country_iso": "country_code",
            "country_code": "country_code",
            "country_name": "country_name",
            "region": "region_code",
            "region_code": "region_code",
            "region_name": "region_name",
            "state": "region_name",
            "city": "city_name",
            "city_name": "city_name",
            "postal": "postal_code",
            "postal_code": "postal_code",
            "zip": "postal_code",
            "latitude": "latitude",
            "lat": "latitude",
            "longitude": "longitude",
            "lon": "longitude",
            "lng": "longitude",
        }

        result = {"source": self.name, "confidence": self.get_confidence_score(data)}

        # Map fields
        for src, dst in field_mapping.items():
            if src in data and data[src]:
                result[dst] = data[src]

        # Standardize country code
        if "country_code" in result:
            result["country_code"] = self.standardize_country_code(result["country_code"])

        # Convert lat/lon to float
        for coord in ["latitude", "longitude"]:
            if coord in result:
                try:
                    result[coord] = float(result[coord])
                except (ValueError, TypeError):
                    del result[coord]

        return result
