"""
Multi-Location Inventory Middleware
Determines visitor's sales region based on GeoIP data
"""

import logging

from django.core.cache import cache
from django.urls import set_script_prefix
from django.utils.functional import SimpleLazyObject

from .models import SalesRegion

logger = logging.getLogger(__name__)

# Shared version stamp for every SalesRegion-derived cache entry
# (``default_sales_region`` and all ``region_by_country:*`` mappings). Bumping
# it strands the previously cached region IDs so that a priority change,
# deactivation, or edit to a region's country list takes effect immediately
# instead of persisting for up to the one-hour entry timeout.
_REGION_CACHE_VERSION_KEY = "sales_region_cache_version"


def _region_cache_version() -> int:
    """Return the current version stamp for cached SalesRegion lookups.

    Seeds the stamp on first use. It never expires so that long-lived region
    entries can't be resurrected by the stamp resetting under them.
    """
    version = cache.get(_REGION_CACHE_VERSION_KEY)
    if version is None:
        version = 1
        cache.add(_REGION_CACHE_VERSION_KEY, version, timeout=None)
    return version


def invalidate_region_cache() -> None:
    """Invalidate every cached SalesRegion lookup by bumping the version stamp.

    Call this whenever a SalesRegion is saved or deleted (including priority and
    active-state changes) so the cached default region and country-to-region
    mappings can never serve an obsolete match.
    """
    _region_cache_version()  # ensure the stamp exists so incr can't miss
    try:
        cache.incr(_REGION_CACHE_VERSION_KEY)
    except ValueError:
        # Expired between seed and incr; reseed ahead of any stale entries.
        cache.set(_REGION_CACHE_VERSION_KEY, 2, timeout=None)


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
        request.sales_region = SimpleLazyObject(lambda: self._detect_region(request))

        response = self.get_response(request)

        # Add Content-Language header for SEO
        self._add_content_language_header(request, response)

        return response

    def _detect_region(self, request) -> SalesRegion | None:
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
        # URL-derived market is authoritative: when the visitor is on a market
        # URL (/nz/en/…), the market — not a cookie or GeoIP — sets the region,
        # so each market URL renders deterministically (SEO/cache safety).
        market_slug = getattr(request, "market_slug", None)
        if market_slug:
            region = get_region_for_market_slug(market_slug)
            if region:
                logger.debug(f"Pinned region to URL market: {region.code}")
                return region

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

    def _get_user_override(self, request) -> SalesRegion | None:
        """
        Get user's region preference override from session/cookie.

        Args:
            request: Django request object

        Returns:
            SalesRegion instance or None
        """
        # Check session first
        if hasattr(request, "session"):
            region_code = request.session.get("preferred_region")
            if region_code:
                try:
                    return SalesRegion.objects.get(code=region_code, is_active=True)
                except SalesRegion.DoesNotExist:
                    # Invalid region code in session, clear it
                    del request.session["preferred_region"]

        # Check cookie
        if hasattr(request, "COOKIES"):
            region_code = request.COOKIES.get("preferred_region")
            if region_code:
                try:
                    return SalesRegion.objects.get(code=region_code, is_active=True)
                except SalesRegion.DoesNotExist:
                    pass

        return None

    def _get_country_code(self, request) -> str | None:
        """
        Extract country code from geo location data.

        Args:
            request: Django request object

        Returns:
            Two-letter country code or None
        """
        if not hasattr(request, "geo_location"):
            return None

        try:
            # geo_location is a SimpleLazyObject, accessing it triggers resolution
            geo_location = request.geo_location
            if isinstance(geo_location, dict):
                country_code = geo_location.get("country_code", "").upper()
                return country_code if country_code else None
        except Exception as e:
            logger.error(f"Error accessing geo_location: {e}")

        return None

    def _find_region_by_country(self, country_code: str) -> SalesRegion | None:
        """Thin wrapper around the shared ``get_region_for_country`` helper."""
        return get_region_for_country(country_code)

    def _get_default_region(self) -> SalesRegion | None:
        """Get the default sales region (delegates to the shared helper)."""
        return get_default_region()

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
            language_code = getattr(request, "LANGUAGE_CODE", "en")

            # Get detected region
            region = None
            if hasattr(request, "sales_region"):
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

            response["Content-Language"] = content_language

        except Exception as e:
            logger.error(f"Error adding Content-Language header: {e}")
            # Don't fail the request if header setting fails


def get_region_from_request(request) -> SalesRegion | None:
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
    if hasattr(request, "sales_region"):
        try:
            # Force evaluation of lazy object
            return request.sales_region if request.sales_region else None
        except Exception as e:
            logger.error(f"Error accessing request.sales_region: {e}")

    return None


def get_region_for_country(country_code: str) -> SalesRegion | None:
    """
    Resolve a two-letter ISO country code to the SalesRegion that ships it.

    A region matches when the country code is in its ``countries`` JSON list;
    the highest-priority active region wins. Results are cached for one hour.

    This is the single shared implementation of the country → region mapping.
    ``RegionDetectionMiddleware`` uses it for GeoIP resolution, and the ship-to
    selector / checkout / fulfilment paths use it to turn a chosen or shipping
    country into a region.

    Args:
        country_code: Two-letter ISO country code (case-insensitive).

    Returns:
        SalesRegion instance or None.
    """
    if not country_code:
        return None

    country_code = country_code.upper()
    cache_key = f"region_by_country:{country_code}"
    version = _region_cache_version()
    cached_region_id = cache.get(cache_key, version=version)

    if cached_region_id:
        try:
            return SalesRegion.objects.get(pk=cached_region_id, is_active=True)
        except SalesRegion.DoesNotExist:
            # Cached region no longer exists, invalidate cache
            cache.delete(cache_key, version=version)

    # A region matches if the country_code is in its countries JSON array.
    try:
        regions = SalesRegion.objects.filter(is_active=True).order_by("-priority")
        for region in regions:
            if isinstance(region.countries, list) and country_code in region.countries:
                cache.set(cache_key, region.id, timeout=3600, version=version)
                return region
    except Exception as e:
        logger.error(f"Error querying regions for country {country_code}: {e}")

    return None


def get_default_region() -> SalesRegion | None:
    """Return the default market: the highest-priority active SalesRegion.

    Cached for one hour under the shared region cache version, so a priority
    change or deactivation (which bumps the version via ``invalidate_region_cache``)
    takes effect immediately.
    """
    cache_key = "default_sales_region"
    version = _region_cache_version()
    cached_region_id = cache.get(cache_key, version=version)

    if cached_region_id:
        try:
            return SalesRegion.objects.get(pk=cached_region_id, is_active=True)
        except SalesRegion.DoesNotExist:
            cache.delete(cache_key, version=version)

    try:
        region = SalesRegion.objects.filter(is_active=True).order_by("-priority").first()
        if region:
            cache.set(cache_key, region.id, timeout=3600, version=version)
            return region
    except Exception as e:
        logger.error(f"Error getting default region: {e}")

    return None


def get_market_slugs() -> set[str]:
    """Return the set of active market slugs (lower-cased).

    A "market" is an active SalesRegion with a non-empty ``slug`` — the segment
    that gives it its own storefront URL (``/nz/en/…``). Cached for one hour
    under the shared region cache version.
    """
    cache_key = "market_slugs"
    version = _region_cache_version()
    cached = cache.get(cache_key, version=version)
    if cached is not None:
        return cached

    try:
        slugs = {
            slug.lower()
            for slug in SalesRegion.objects.filter(is_active=True)
            .exclude(slug="")
            .values_list("slug", flat=True)
        }
        # The default market (highest-priority region) is always served WITHOUT a
        # prefix. Drop its slug so it can't also be reached at /<slug>/… — that
        # would serve the default market at two URLs (duplicate content).
        default = get_default_region()
        if default and default.slug:
            slugs.discard(default.slug.lower())
    except Exception as e:
        logger.error(f"Error loading market slugs: {e}")
        slugs = set()

    cache.set(cache_key, slugs, timeout=3600, version=version)
    return slugs


def get_region_for_market_slug(slug: str) -> SalesRegion | None:
    """Resolve a market slug to its SalesRegion (active only), cached one hour."""
    if not slug:
        return None

    slug = slug.lower()
    cache_key = f"region_by_market_slug:{slug}"
    version = _region_cache_version()
    cached_region_id = cache.get(cache_key, version=version)

    if cached_region_id:
        try:
            return SalesRegion.objects.get(pk=cached_region_id, is_active=True)
        except SalesRegion.DoesNotExist:
            cache.delete(cache_key, version=version)

    try:
        region = SalesRegion.objects.filter(slug__iexact=slug, is_active=True).first()
        if region:
            cache.set(cache_key, region.id, timeout=3600, version=version)
            return region
    except Exception as e:
        logger.error(f"Error resolving market slug {slug}: {e}")

    return None


class MarketMiddleware:
    """Resolve the storefront *market* from a leading URL segment and strip it.

    A market URL looks like ``/nz/en/products/…``: the first segment (``nz``) is
    an active :class:`SalesRegion` slug. This middleware strips that segment from
    ``path_info`` so the rest of the stack — ``LocaleMiddleware``,
    ``i18n_patterns``, URL resolution — sees the ordinary ``/en/products/…`` path
    unchanged, and folds the segment into the script prefix so that a plain
    ``{% url %}`` / ``reverse()`` keeps the visitor inside their market.

    Sets on the request:
        ``market_slug``   — the matched slug, or ``None`` for the default
                            (unprefixed) market.
        ``market_prefix`` — ``"/nz"`` for URL building, or ``""`` for the default.
        ``market``        — lazy resolved SalesRegion (matched slug, else default).

    When a market slug is present it is authoritative:
    ``RegionDetectionMiddleware`` pins ``request.sales_region`` to it (see
    ``_detect_region``), so the URL — not a cookie or GeoIP — determines the
    market, keeping each market URL's rendered content deterministic.

    MUST be ordered before ``LocaleMiddleware``. Only ever strips a segment that
    is a known active market slug, so page/product slugs can never be mistaken
    for a market.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.market_slug = None
        request.market_prefix = ""

        path_info = request.path_info or "/"
        first = path_info.lstrip("/").split("/", 1)[0].lower()

        if first and first in get_market_slugs():
            prefix_seg = "/" + first
            remainder = path_info[len(prefix_seg) :] or "/"
            if not remainder.startswith("/"):
                remainder = "/" + remainder

            # Strip the market segment from the path used for resolution + i18n.
            request.path_info = remainder
            request.META["PATH_INFO"] = remainder

            # Fold the market into the script prefix so reverse()/{% url %} keep
            # it, while request.path (script_name + path_info) stays the full
            # /nz/en/… for correct absolute URIs / canonical links. Derive the
            # base from SCRIPT_NAME (set by SubpathMiddleware for /shop subpath
            # deployments) so a subpath composes correctly as /shop/nz.
            new_script = request.META.get("SCRIPT_NAME", "") + prefix_seg
            request.META["SCRIPT_NAME"] = new_script
            set_script_prefix(new_script + "/")

            request.market_slug = first
            request.market_prefix = prefix_seg

        request.market = SimpleLazyObject(lambda: self._resolve_market(request))

        return self.get_response(request)

    @staticmethod
    def _resolve_market(request) -> SalesRegion | None:
        slug = getattr(request, "market_slug", None)
        if slug:
            region = get_region_for_market_slug(slug)
            if region:
                return region
        return get_default_region()


def get_ship_to_options(request):
    """
    Build the ship-to picker options: the store's active shippable countries and
    the shopper's current selection.

    Options are the active ``ShippingCountry`` rows (code + display name, sorted
    by name). The current selection is the explicitly chosen ``preferred_country``
    (session, then cookie), else the GeoIP-detected country when the store ships
    there, else None. Shared by the ship-to header widget and the region
    confirmation modal.
    """
    from django_countries import countries as dj_countries

    from shipping.models import ShippingCountry

    codes = ShippingCountry.objects.filter(site_id=1, is_active=True).values_list(
        "country_code", flat=True
    )
    options = sorted(
        ({"code": c, "name": dj_countries.name(c) or c} for c in codes),
        key=lambda x: x["name"],
    )
    shippable = {o["code"] for o in options}

    current_code = None
    if request is not None:
        if hasattr(request, "session"):
            current_code = request.session.get("preferred_country")
        if not current_code and hasattr(request, "COOKIES"):
            current_code = request.COOKIES.get("preferred_country")
        if not current_code:
            try:
                geo = getattr(request, "geo_location", None)
                geo_cc = geo.get("country_code", "").upper() if isinstance(geo, dict) else ""
            except Exception:
                geo_cc = ""
            if geo_cc in shippable:
                current_code = geo_cc

    current_code = current_code.upper() if current_code else None
    if current_code and current_code not in shippable:
        current_code = None

    return {
        "countries": options,
        "current_code": current_code,
        "current_name": (dj_countries.name(current_code) or current_code) if current_code else None,
    }


def get_ship_to_display(request):
    """
    Resolve the shopper's ship-to destination for display purposes.

    Returns ``(country_code_or_None, display_name)``. Prefers the explicitly
    chosen ``preferred_country`` (session then cookie), then the GeoIP-detected
    country, and finally falls back to the resolved region's name. Used to word
    the "does not ship to X" marks/notices consistently across listings and the
    product page.
    """
    from django_countries import countries as dj_countries

    code = None
    if hasattr(request, "session"):
        code = request.session.get("preferred_country")
    if not code and hasattr(request, "COOKIES"):
        code = request.COOKIES.get("preferred_country")
    if not code:
        try:
            geo = getattr(request, "geo_location", None)
            code = geo.get("country_code", "").upper() if isinstance(geo, dict) else None
        except Exception:
            code = None

    if code:
        code = code.upper()
        return code, (dj_countries.name(code) or code)

    region = get_region_from_request(request)
    return None, (region.name if region else "")
