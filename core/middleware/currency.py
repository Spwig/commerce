"""
Currency Middleware for Multi-Currency Support

Handles automatic currency detection and selection based on multiple sources:
1. URL parameter (?currency=EUR)
2. Cookie (selected_currency)
3. Session currency
4. GeoIP detection (if enabled)
5. Browser Accept-Language header
6. Site default currency

Priority order follows the list above.
"""

from django.utils.deprecation import MiddlewareMixin
from django.conf import settings as django_settings
from core.models import SiteSettings
from moneyed import CURRENCIES
import logging

logger = logging.getLogger(__name__)


# Country to currency mapping for GeoIP and locale detection
COUNTRY_CURRENCY_MAP = {
    # Eurozone countries
    'AT': 'EUR', 'BE': 'EUR', 'CY': 'EUR', 'EE': 'EUR', 'FI': 'EUR',
    'FR': 'EUR', 'DE': 'EUR', 'GR': 'EUR', 'IE': 'EUR', 'IT': 'EUR',
    'LV': 'EUR', 'LT': 'EUR', 'LU': 'EUR', 'MT': 'EUR', 'NL': 'EUR',
    'PT': 'EUR', 'SK': 'EUR', 'SI': 'EUR', 'ES': 'EUR', 'HR': 'EUR',

    # United Kingdom
    'GB': 'GBP',

    # Americas
    'US': 'USD', 'CA': 'CAD', 'MX': 'MXN', 'BR': 'BRL', 'AR': 'ARS',
    'CL': 'CLP', 'CO': 'COP', 'PE': 'PEN', 'UY': 'UYU', 'VE': 'VES',
    'BO': 'BOB', 'PY': 'PYG', 'EC': 'USD',  # Ecuador uses USD

    # Asia Pacific
    'AU': 'AUD', 'NZ': 'NZD', 'JP': 'JPY', 'CN': 'CNY', 'HK': 'HKD',
    'SG': 'SGD', 'IN': 'INR', 'KR': 'KRW', 'TH': 'THB', 'MY': 'MYR',
    'ID': 'IDR', 'PH': 'PHP', 'VN': 'VND', 'TW': 'TWD', 'BD': 'BDT',
    'PK': 'PKR', 'LK': 'LKR', 'NP': 'NPR', 'MM': 'MMK', 'KH': 'KHR',
    'LA': 'LAK', 'MN': 'MNT',

    # Middle East
    'AE': 'AED', 'SA': 'SAR', 'IL': 'ILS', 'TR': 'TRY', 'QA': 'QAR',
    'KW': 'KWD', 'BH': 'BHD', 'OM': 'OMR', 'JO': 'JOD', 'LB': 'LBP',
    'IQ': 'IQD', 'YE': 'YER', 'SY': 'SYP',

    # Nordic countries
    'SE': 'SEK', 'NO': 'NOK', 'DK': 'DKK', 'IS': 'ISK',

    # Switzerland
    'CH': 'CHF',

    # Eastern Europe
    'PL': 'PLN', 'CZ': 'CZK', 'HU': 'HUF', 'RO': 'RON', 'BG': 'BGN',
    'UA': 'UAH', 'RU': 'RUB', 'BY': 'BYN', 'MD': 'MDL', 'RS': 'RSD',
    'BA': 'BAM', 'MK': 'MKD', 'AL': 'ALL', 'ME': 'EUR',

    # Africa
    'ZA': 'ZAR', 'NG': 'NGN', 'KE': 'KES', 'EG': 'EGP', 'MA': 'MAD',
    'TN': 'TND', 'DZ': 'DZD', 'GH': 'GHS', 'ET': 'ETB', 'TZ': 'TZS',
    'UG': 'UGX', 'ZW': 'ZWL', 'MU': 'MUR', 'BW': 'BWP', 'NA': 'NAD',
    'ZM': 'ZMW', 'MW': 'MWK', 'MZ': 'MZN', 'AO': 'AOA', 'SN': 'XOF',
    'CI': 'XOF', 'CM': 'XAF', 'CD': 'CDF', 'RW': 'RWF', 'BI': 'BIF',
}


class CurrencyMiddleware(MiddlewareMixin):
    """
    Middleware to detect and set customer's currency preference.

    Adds 'currency' attribute to request object with the selected currency code.

    Detection priority:
    1. URL parameter (?currency=EUR)
    2. Cookie (selected_currency)
    3. Session currency
    4. GeoIP detection (if enabled)
    5. Browser Accept-Language header
    6. Site default currency
    """

    def process_request(self, request):
        """Process incoming request and set currency"""
        settings = SiteSettings.get_settings()

        # Skip if multi-currency is disabled
        if not settings.enable_multi_currency:
            request.currency = settings.default_currency
            return

        detected_currency = None

        # 1. Check URL parameter (highest priority - explicit user action)
        url_currency = request.GET.get('currency', '').upper()
        if url_currency and self._is_valid_currency(url_currency, settings):
            detected_currency = url_currency
            request.session['currency'] = url_currency
            logger.debug(f"Currency set from URL parameter: {url_currency}")

        # 2. Check cookie (user's persistent preference)
        elif 'selected_currency' in request.COOKIES:
            cookie_currency = request.COOKIES.get('selected_currency', '').upper()
            if self._is_valid_currency(cookie_currency, settings):
                detected_currency = cookie_currency
                request.session['currency'] = cookie_currency
                logger.debug(f"Currency set from cookie: {cookie_currency}")

        # 3. Check session (current session preference)
        elif 'currency' in request.session:
            session_currency = request.session.get('currency', '').upper()
            if self._is_valid_currency(session_currency, settings):
                detected_currency = session_currency
                logger.debug(f"Currency set from session: {session_currency}")

        # 4. GeoIP detection (automatic based on location)
        elif settings.currency_selection_mode in ['auto_geoip', 'both']:
            geoip_currency = self._detect_currency_from_geoip(request, settings)
            if geoip_currency:
                detected_currency = geoip_currency
                request.session['currency'] = geoip_currency
                logger.info(f"Currency auto-detected from GeoIP: {geoip_currency}")

        # 5. Browser locale detection (Accept-Language header)
        if not detected_currency:
            browser_currency = self._detect_currency_from_locale(request, settings)
            if browser_currency:
                detected_currency = browser_currency
                request.session['currency'] = browser_currency
                logger.info(f"Currency detected from browser locale: {browser_currency}")

        # 6. Fallback to default
        if not detected_currency:
            detected_currency = settings.default_currency
            request.session['currency'] = detected_currency
            logger.debug(f"Currency set to default: {detected_currency}")

        # Set currency on request
        request.currency = detected_currency

    def _is_valid_currency(self, currency_code, settings):
        """Check if currency code is valid and supported"""
        if not currency_code:
            return False

        # Check if currency exists in django-money
        if currency_code not in CURRENCIES:
            logger.warning(f"Invalid currency code: {currency_code}")
            return False

        # Check if currency is in supported currencies list
        if currency_code not in settings.supported_currencies:
            logger.warning(f"Currency not supported: {currency_code}")
            return False

        return True

    def _detect_currency_from_geoip(self, request, settings):
        """Detect currency from customer's country via GeoIP"""
        try:
            # Get client IP
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0].strip()
            else:
                ip = request.META.get('REMOTE_ADDR', '')

            # Skip local/private IPs
            if not ip or ip in ['127.0.0.1', 'localhost'] or ip.startswith('192.168.') or ip.startswith('10.'):
                return None

            # Try to use django-geoip2 if available
            try:
                from django.contrib.gis.geoip2 import GeoIP2
                g = GeoIP2()
                country_info = g.country(ip)
                country_code = country_info.get('country_code')
            except Exception as geoip_error:
                logger.debug(f"GeoIP2 lookup failed, trying fallback: {geoip_error}")
                # Fallback: try requests to external GeoIP service if configured
                country_code = self._external_geoip_lookup(ip)

            if not country_code:
                return None

            # Map country to currency
            currency = COUNTRY_CURRENCY_MAP.get(country_code)

            # Validate currency is supported
            if currency and self._is_valid_currency(currency, settings):
                logger.info(f"GeoIP detected currency {currency} for country {country_code} (IP: {ip})")
                return currency

        except Exception as e:
            logger.warning(f"GeoIP currency detection failed: {e}")

        return None

    def _external_geoip_lookup(self, ip):
        """Fallback: lookup IP using external GeoIP service"""
        try:
            import requests
            # Using ip-api.com (free, no API key required)
            response = requests.get(f'http://ip-api.com/json/{ip}', timeout=2)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    return data.get('countryCode')
        except Exception as e:
            logger.debug(f"External GeoIP lookup failed: {e}")

        return None

    def _detect_currency_from_locale(self, request, settings):
        """Detect currency from browser Accept-Language header"""
        try:
            accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
            if not accept_language:
                return None

            # Parse first language (e.g., "en-US,en;q=0.9,es;q=0.8")
            first_lang = accept_language.split(',')[0].strip()

            # Extract locale (e.g., "en-US" -> "US")
            if '-' in first_lang:
                _, country_code = first_lang.split('-', 1)
                currency = COUNTRY_CURRENCY_MAP.get(country_code.upper())

                if currency and self._is_valid_currency(currency, settings):
                    logger.info(f"Browser locale detected currency {currency} from {first_lang}")
                    return currency

        except Exception as e:
            logger.warning(f"Browser locale currency detection failed: {e}")

        return None
