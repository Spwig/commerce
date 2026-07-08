"""
Edge Header Provider - Reads location from CDN headers
"""
from typing import Dict, Optional, Any
from .base import GeoIPProviderBase
import logging

logger = logging.getLogger(__name__)


class EdgeHeaderProvider(GeoIPProviderBase):
    """
    Provider that reads location data from CDN edge headers
    Supports Cloudflare, Fastly, AWS CloudFront, etc.
    """

    # Known CDN headers that contain country information
    COUNTRY_HEADERS = [
        'CF-IPCountry',          # Cloudflare
        'CloudFront-Viewer-Country',  # AWS CloudFront
        'X-Country-Code',        # Generic
        'X-GeoIP-Country',       # Nginx GeoIP module
        'X-Real-Country',        # Custom
        'Fastly-Client-Country', # Fastly
        'X-Akamai-Country-Code', # Akamai
    ]

    REGION_HEADERS = [
        'CloudFront-Viewer-Country-Region',  # AWS CloudFront
        'X-GeoIP-Region',        # Nginx GeoIP module
        'CF-Region',             # Cloudflare (if configured)
    ]

    CITY_HEADERS = [
        'CloudFront-Viewer-City',  # AWS CloudFront
        'X-GeoIP-City',            # Nginx GeoIP module
        'CF-City',                 # Cloudflare (if configured)
    ]

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.request = None  # Will be set by middleware
        self.trusted_headers = config.get('trusted_headers', self.COUNTRY_HEADERS) if config else self.COUNTRY_HEADERS

    def initialize(self) -> bool:
        """
        No initialization needed for header provider
        """
        self._initialized = True
        return True

    def is_available(self) -> bool:
        """
        Available if we have a request object to read headers from
        """
        return self.request is not None

    def set_request(self, request):
        """
        Set the current request object

        Args:
            request: Django request object
        """
        self.request = request

    def lookup(self, ip: str) -> Optional[Dict[str, Any]]:
        """
        Read location from request headers

        Args:
            ip: IP address (not used, but kept for interface compatibility)

        Returns:
            Location data from headers
        """
        if not self.request:
            logger.debug("No request object available for header lookup")
            return None

        result = {}

        # Try to get country from headers
        country = self._get_header_value(self.COUNTRY_HEADERS)
        if country:
            result['country_code'] = country

        # Try to get region
        region = self._get_header_value(self.REGION_HEADERS)
        if region:
            result['region_code'] = region

        # Try to get city
        city = self._get_header_value(self.CITY_HEADERS)
        if city:
            result['city_name'] = city

        # Check for IP type headers
        if self._get_header_value(['CF-IPCountry']) == 'T1':
            result['is_tor'] = True

        # Check for mobile headers
        mobile_header = self._get_header_value([
            'CloudFront-Is-Mobile-Viewer',
            'CF-Device-Type'
        ])
        if mobile_header in ['true', 'mobile']:
            result['is_mobile'] = True

        if not result:
            logger.debug(f"No geo headers found in request")
            return None

        # Add metadata
        result['source'] = 'edge_header'

        logger.debug(f"Edge header lookup result: {result}")
        return self.format_response(result)

    def _get_header_value(self, headers: list) -> Optional[str]:
        """
        Get first available header value

        Args:
            headers: List of header names to check

        Returns:
            Header value or None
        """
        if not self.request:
            return None

        for header in headers:
            # Try both META format and direct header format
            meta_key = f"HTTP_{header.upper().replace('-', '_')}"
            value = self.request.META.get(meta_key)

            if value and value != 'XX':  # XX often means unknown
                return value

            # Also try direct header access (for some frameworks)
            if hasattr(self.request, 'headers'):
                value = self.request.headers.get(header)
                if value and value != 'XX':
                    return value

        return None

    def get_all_headers(self) -> Dict[str, str]:
        """
        Get all geo-related headers for debugging

        Returns:
            Dictionary of header name to value
        """
        if not self.request:
            return {}

        headers = {}
        all_headers = self.COUNTRY_HEADERS + self.REGION_HEADERS + self.CITY_HEADERS

        for header in all_headers:
            value = self._get_header_value([header])
            if value:
                headers[header] = value

        return headers