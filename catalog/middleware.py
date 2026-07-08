"""
Multi-Location Inventory Middleware
Determines visitor's sales region based on GeoIP data
"""
from django.core.cache import cache
from django.utils.functional import SimpleLazyObject
from typing import Optional
import logging

from .models import SalesRegion

logger = logging.getLogger(__name__)


class RegionDetectionMiddleware:
    """
    Middleware that determines visitor's sales region based on GeoIP location.
    Adds request.sales_region with the matched SalesRegion instance.

    This middleware depends on GeoIPMiddleware being loaded first to provide
    request.geo_location data.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Add sales_region to request as lazy object
        request.sales_region = SimpleLazyObject(
            lambda: self._detect_region(request)
        )

        response = self.get_response(request)

        # Add Content-Language header for SEO
        self._add_content_language_header(request, response)

        return response

    def _detect_region(self, request) -> Optional[SalesRegion]:
        """
        Detect visitor's sales region based on geo location.

        Priority order:
        1. User preference override (session/cookie)
        2. GeoIP country code match
        3. Default region (highest priority region)

        Args:
            request: Django request object

        Returns:
            SalesRegion instance or None
        """
        # Check for user preference override
        region = self._get_user_override(request)
        if region:
            logger.debug(f"Using user-selected region: {region.code}")
            return region

        # Get country code from geo location
        country_code = self._get_country_code(request)
        if not country_code:
            logger.debug("No country code available, using default region")
            return self._get_default_region()

        # Try to find matching region (with caching)
        region = self._find_region_by_country(country_code)
        if region:
            logger.debug(f"Matched country {country_code} to region {region.code}")
            return region

        # Fall back to default region
        logger.debug(f"No region match for country {country_code}, using default")
        return self._get_default_region()

    def _get_user_override(self, request) -> Optional[SalesRegion]:
        """
        Get user's region preference override from session/cookie.

        Args:
            request: Django request object

        Returns:
            SalesRegion instance or None
        """
        # Check session first
        if hasattr(request, 'session'):
            region_code = request.session.get('preferred_region')
            if region_code:
                try:
                    return SalesRegion.objects.get(code=region_code, is_active=True)
                except SalesRegion.DoesNotExist:
                    # Invalid region code in session, clear it
                    del request.session['preferred_region']

        # Check cookie
        if hasattr(request, 'COOKIES'):
            region_code = request.COOKIES.get('preferred_region')
            if region_code:
                try:
                    return SalesRegion.objects.get(code=region_code, is_active=True)
                except SalesRegion.DoesNotExist:
                    pass

        return None

    def _get_country_code(self, request) -> Optional[str]:
        """
        Extract country code from geo location data.

        Args:
            request: Django request object

        Returns:
            Two-letter country code or None
        """
        if not hasattr(request, 'geo_location'):
            return None

        try:
            # geo_location is a SimpleLazyObject, accessing it triggers resolution
            geo_location = request.geo_location
            if isinstance(geo_location, dict):
                country_code = geo_location.get('country_code', '').upper()
                return country_code if country_code else None
        except Exception as e:
            logger.error(f"Error accessing geo_location: {e}")

        return None

    def _find_region_by_country(self, country_code: str) -> Optional[SalesRegion]:
        """
        Find sales region that includes the given country code.

        Uses caching to avoid repeated database queries.

        Args:
            country_code: Two-letter ISO country code

        Returns:
            SalesRegion instance or None
        """
        # Check cache first
        cache_key = f"region_by_country:{country_code}"
        cached_region_id = cache.get(cache_key)

        if cached_region_id:
            try:
                return SalesRegion.objects.get(pk=cached_region_id, is_active=True)
            except SalesRegion.DoesNotExist:
                # Cached region no longer exists, invalidate cache
                cache.delete(cache_key)

        # Query database for matching region
        # A region matches if the country_code is in its countries JSON array
        try:
            regions = SalesRegion.objects.filter(is_active=True).order_by('-priority')

            for region in regions:
                if isinstance(region.countries, list) and country_code in region.countries:
                    # Cache the match for 1 hour
                    cache.set(cache_key, region.id, timeout=3600)
                    return region
        except Exception as e:
            logger.error(f"Error querying regions for country {country_code}: {e}")

        return None

    def _get_default_region(self) -> Optional[SalesRegion]:
        """
        Get the default sales region (highest priority active region).

        Uses caching to avoid repeated database queries.

        Returns:
            SalesRegion instance or None
        """
        cache_key = "default_sales_region"
        cached_region_id = cache.get(cache_key)

        if cached_region_id:
            try:
                return SalesRegion.objects.get(pk=cached_region_id, is_active=True)
            except SalesRegion.DoesNotExist:
                # Cached region no longer exists, invalidate cache
                cache.delete(cache_key)

        # Query database for highest priority region
        try:
            region = SalesRegion.objects.filter(is_active=True).order_by('-priority').first()
            if region:
                # Cache for 1 hour
                cache.set(cache_key, region.id, timeout=3600)
                return region
        except Exception as e:
            logger.error(f"Error getting default region: {e}")

        return None

    def _add_content_language_header(self, request, response):
        """
        Add Content-Language HTTP header for SEO purposes.

        Format: language-region (e.g., "en-US", "fr-CA")

        Args:
            request: Django request object
            response: Django response object
        """
        try:
            # Get current language from request
            language_code = getattr(request, 'LANGUAGE_CODE', 'en')

            # Get detected region
            region = None
            if hasattr(request, 'sales_region'):
                try:
                    region = request.sales_region if request.sales_region else None
                except Exception:
                    pass

            # Build Content-Language header
            if region and region.code:
                # Format: language-region (e.g., "en-US", "fr-CA")
                content_language = f"{language_code}-{region.code}"
            else:
                # Just language code
                content_language = language_code

            response['Content-Language'] = content_language

        except Exception as e:
            logger.error(f"Error adding Content-Language header: {e}")
            # Don't fail the request if header setting fails


def get_region_from_request(request) -> Optional[SalesRegion]:
    """
    Utility function to safely get the sales region from a request.

    Usage:
        from catalog.middleware import get_region_from_request
        region = get_region_from_request(request)

    Args:
        request: Django request object

    Returns:
        SalesRegion instance or None
    """
    if hasattr(request, 'sales_region'):
        try:
            # Force evaluation of lazy object
            return request.sales_region if request.sales_region else None
        except Exception as e:
            logger.error(f"Error accessing request.sales_region: {e}")

    return None
