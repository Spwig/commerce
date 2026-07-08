"""
GeoIP Middleware for automatic IP resolution
"""
from django.core.cache import cache
from django.conf import settings
from django.utils.functional import SimpleLazyObject
from django.utils import timezone
from typing import Optional, Dict, Any
import logging
import time
from .models import GeoLocation, BusinessRule
from .providers import EdgeHeaderProvider, BrowserHintProvider
from .utils.ip_utils import get_client_ip, get_ip_prefix
from .tracking import track_page_view, BOT_UA_PATTERNS

logger = logging.getLogger(__name__)


class GeoIPMiddleware:
    """
    Middleware that resolves visitor IP to location data
    Adds request.geo_location with resolved data
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.providers = []
        self._initialize_providers()

    def _initialize_providers(self):
        """
        Initialize configured providers
        """
        # Initialize providers based on settings
        geoip_config = getattr(settings, 'GEOIP_CONFIG', {})

        # Default providers if not configured
        provider_classes = geoip_config.get('PROVIDERS', [
            'geoip.providers.EdgeHeaderProvider',
            'geoip.providers.BrowserHintProvider',
        ])

        for provider_path in provider_classes:
            try:
                # Import provider class
                module_path, class_name = provider_path.rsplit('.', 1)
                module = __import__(module_path, fromlist=[class_name])
                provider_class = getattr(module, class_name)

                # Initialize provider
                provider = provider_class(geoip_config.get('PROVIDER_CONFIG', {}))
                if provider.initialize():
                    self.providers.append(provider)
                    logger.info(f"Initialized GeoIP provider: {class_name}")
                else:
                    logger.warning(f"Failed to initialize GeoIP provider: {class_name}")
            except Exception as e:
                logger.error(f"Error loading GeoIP provider {provider_path}: {e}")

    # Paths that should not be tracked as page views
    EXCLUDED_PATH_PREFIXES = (
        '/static/',
        '/media/',
        '/favicon.ico',
        '/robots.txt',
        '/sitemap',
        '/api/',
        '/__debug__/',
        '/jsi18n/',
    )

    # Admin/staff path prefixes - tracked but flagged as admin traffic
    ADMIN_PATH_PREFIXES = (
        '/admin/',
        '/en/admin/',
        '/builder/',
        '/en/builder/',
        '/theme/',
        '/en/theme/',
    )

    # Bot patterns are defined in geoip.tracking.BOT_UA_PATTERNS (single source of truth)

    def __call__(self, request):
        # Add geo_location to request as lazy object
        request.geo_location = SimpleLazyObject(
            lambda: self._resolve_location(request)
        )

        # Track visitor location (only for trackable page requests)
        self._track_visitor(request)

        # Process business rules
        self._process_business_rules(request)

        response = self.get_response(request)

        return response

    def _resolve_location(self, request) -> Dict[str, Any]:
        """
        Resolve IP address to location data

        Args:
            request: Django request object

        Returns:
            Dictionary with location data
        """
        # Get client IP
        ip = get_client_ip(request)
        if not ip:
            logger.debug("Could not determine client IP")
            return self._get_default_location()

        # Check for user preference override (cookie/session)
        user_override = self._get_user_override(request)
        if user_override:
            logger.debug(f"Using user override for IP {ip}")
            return user_override

        # Check cache first
        cache_key = f"geoip:{ip}"
        cached = cache.get(cache_key)
        if cached:
            logger.debug(f"Cache hit for IP {ip}")
            return cached

        # Check database cache
        db_cached = self._get_db_cache(ip)
        if db_cached:
            logger.debug(f"Database cache hit for IP {ip}")
            # Update Redis cache
            cache.set(cache_key, db_cached, timeout=3600)  # 1 hour
            return db_cached

        # Try providers in order
        location_data = None
        is_private_ip = False
        for provider in self.providers:
            try:
                # Set request for providers that need it
                if hasattr(provider, 'set_request'):
                    provider.set_request(request)

                if provider.is_available():
                    start_time = time.time()
                    location_data = provider.lookup(ip)
                    lookup_time = (time.time() - start_time) * 1000

                    if location_data:
                        location_data['lookup_time_ms'] = lookup_time

                        # Check if this is a private/internal IP response
                        if location_data.get('source') == 'private_network' or location_data.get('data_source') == 'private_network':
                            is_private_ip = True
                            logger.info(f"Private/internal IP detected: {ip}")

                        logger.debug(f"Provider {provider.name} resolved IP {ip} in {lookup_time:.2f}ms")
                        break
            except Exception as e:
                logger.error(f"Provider {provider.name} error: {e}")

        # Use default if no resolution
        if not location_data:
            location_data = self._get_default_location(is_internal_ip=is_private_ip)
            location_data['ip'] = ip
        elif is_private_ip:
            # Replace private IP response with store's location
            store_location = self._get_default_location(is_internal_ip=True)
            store_location['ip'] = ip
            store_location['lookup_time_ms'] = location_data.get('lookup_time_ms', 0)
            location_data = store_location

        # Save to cache
        cache.set(cache_key, location_data, timeout=3600)  # 1 hour

        # Save to database cache (async if possible)
        self._save_to_db_cache(ip, location_data)

        return location_data

    def _get_user_override(self, request) -> Optional[Dict[str, Any]]:
        """
        Get user's location preference override

        Args:
            request: Django request object

        Returns:
            Location data or None
        """
        # Check session
        if hasattr(request, 'session'):
            override = request.session.get('geo_location_override')
            if override:
                return override

        # Check cookies
        if hasattr(request, 'COOKIES'):
            country = request.COOKIES.get('geo_country')
            if country:
                return {
                    'country_code': country,
                    'source': 'user_preference',
                    'confidence': 1.0
                }

        return None

    def _get_db_cache(self, ip: str) -> Optional[Dict[str, Any]]:
        """
        Get cached location from database

        Args:
            ip: IP address

        Returns:
            Location data or None
        """
        try:
            from django.utils import timezone
            # Filter by expires_at to exclude expired entries
            geo_location = GeoLocation.objects.filter(
                ip_address=ip
            ).exclude(
                expires_at__lt=timezone.now()
            ).first()

            if geo_location:
                return geo_location.to_dict()
        except Exception as e:
            logger.error(f"Database cache lookup error: {e}")

        return None

    def _save_to_db_cache(self, ip: str, location_data: Dict[str, Any]):
        """
        Save location to database cache

        Args:
            ip: IP address
            location_data: Location data
        """
        try:
            from django.utils import timezone
            from datetime import timedelta

            # Calculate expiry based on confidence
            confidence = location_data.get('confidence', 0.5)
            if confidence > 0.8:
                expires_in = timedelta(days=30)  # High confidence: 30 days
            elif confidence > 0.5:
                expires_in = timedelta(days=7)   # Medium confidence: 7 days
            else:
                expires_in = timedelta(hours=24)  # Low confidence: 24 hours

            GeoLocation.objects.update_or_create(
                ip_address=ip,
                defaults={
                    'ip_prefix': get_ip_prefix(ip),
                    'country_code': location_data.get('country_code', ''),
                    'country_name': location_data.get('country_name', ''),
                    'region_code': location_data.get('region_code', ''),
                    'region_name': location_data.get('region_name', ''),
                    'city_name': location_data.get('city_name', ''),
                    'postal_code': location_data.get('postal_code', ''),
                    'latitude': location_data.get('latitude'),
                    'longitude': location_data.get('longitude'),
                    'source': location_data.get('source', 'unknown'),
                    'confidence': confidence,
                    'is_proxy': location_data.get('is_proxy', False),
                    'is_vpn': location_data.get('is_vpn', False),
                    'is_tor': location_data.get('is_tor', False),
                    'is_mobile': location_data.get('is_mobile', False),
                    'expires_at': timezone.now() + expires_in
                }
            )
        except Exception as e:
            logger.error(f"Failed to save to database cache: {e}")

    def _get_default_location(self, is_internal_ip: bool = False) -> Dict[str, Any]:
        """
        Get default location when resolution fails

        Args:
            is_internal_ip: Whether this is for an internal/private IP address

        Returns:
            Default location dictionary
        """
        # For internal IPs, use the store's configured location instead of hardcoded US
        if is_internal_ip:
            try:
                from core.models import SiteSettings
                from .models import CountryMapping

                site_settings = SiteSettings.get_settings()

                # Try to get country code from country name
                country_code = None
                if site_settings.country:
                    # First check if it's already a 2-letter code
                    if len(site_settings.country) == 2:
                        country_code = site_settings.country.upper()
                    else:
                        # Look up country code from name
                        mapping = CountryMapping.objects.filter(
                            country_name__iexact=site_settings.country
                        ).first()
                        if mapping:
                            country_code = mapping.country_code

                # Fallback to merchant default country if no country configured
                if not country_code:
                    from core.utils import get_default_country
                    country_code = get_default_country()

                return {
                    'country_code': country_code,
                    'currency': site_settings.default_currency,
                    'language': site_settings.default_language,
                    'source': 'internal_ip',
                    'confidence': 0.0,
                    'is_internal_ip': True
                }
            except Exception as e:
                logger.warning(f"Failed to get store settings for internal IP, using fallback: {e}")

        # For regular fallback (non-internal IPs), still use configured fallback
        config = getattr(settings, 'GEOIP_CONFIG', {})
        from core.utils import get_default_country
        default_country = config.get('FALLBACK_COUNTRY', get_default_country())

        return {
            'country_code': default_country,
            'source': 'default',
            'confidence': 0.0
        }

    def _is_bot(self, user_agent_string):
        """Check if user agent indicates a bot, crawler, or headless browser."""
        from .tracking import detect_bot
        return detect_bot(user_agent_string)

    def _is_ajax_request(self, request):
        """Check if this is an AJAX/fetch request (not a page navigation)."""
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return True
        # fetch() requests with Accept: application/json
        accept = request.META.get('HTTP_ACCEPT', '')
        if 'application/json' in accept and 'text/html' not in accept:
            return True
        return False

    def _track_visitor(self, request):
        """
        Track visitor location for analytics, including UTM parameters.

        Filtering applied:
        - Static/media/API/debug paths are excluded entirely
        - AJAX/fetch requests are excluded (only count page navigations)
        - Bot/headless traffic is tracked but flagged with is_bot=True
        - Admin/builder paths are tracked but flagged with is_admin_traffic=True
        - Unique visitors keyed by session_key only (not session+IP)

        Note: Headless frontend tracking (Next.js) is handled separately by
        the resolve_location() API view via geoip.tracking.track_page_view().
        """
        if not hasattr(request, 'session'):
            return

        path = request.path_info

        # Skip non-page requests entirely (static, media, API, etc.)
        if path.startswith(self.EXCLUDED_PATH_PREFIXES):
            return

        # Skip AJAX/fetch requests - only count full page navigations
        if self._is_ajax_request(request):
            return

        # Only count GET requests (form submissions etc. are not page views)
        if request.method != 'GET':
            return

        # Delegate to shared tracking utility (creates VisitorLocation + PageView)
        track_page_view(request, path, source='middleware')

    def _process_business_rules(self, request):
        """
        Process business rules based on location

        Args:
            request: Django request object
        """
        try:
            if not hasattr(request, 'geo_location'):
                return

            location = request.geo_location
            if not isinstance(location, dict):
                return

            # Get active business rules (cached for 60 seconds)
            cache_key = 'geoip:active_business_rules'
            rules = cache.get(cache_key)
            if rules is None:
                rules = list(BusinessRule.objects.filter(is_active=True).order_by('priority'))
                cache.set(cache_key, rules, timeout=60)

            request.geo_rules = []
            for rule in rules:
                if rule.evaluate(location):
                    request.geo_rules.append(rule.actions)
                    # Update tracking
                    rule.times_triggered += 1
                    rule.last_triggered = timezone.now()
                    rule.save(update_fields=['times_triggered', 'last_triggered'])

        except Exception as e:
            logger.error(f"Failed to process business rules: {e}")