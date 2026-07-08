"""
Context processor for multi-currency support.
Provides currency data to templates and widgets.
"""

from django.conf import settings
from core.models import SiteSettings
from moneyed import CURRENCIES
import logging

logger = logging.getLogger(__name__)


# Currency to country code mapping for flags
CURRENCY_TO_COUNTRY = {
    'USD': 'US', 'EUR': 'EU', 'GBP': 'GB', 'JPY': 'JP', 'AUD': 'AU',
    'CAD': 'CA', 'CHF': 'CH', 'CNY': 'CN', 'SEK': 'SE', 'NZD': 'NZ',
    'MXN': 'MX', 'SGD': 'SG', 'HKD': 'HK', 'NOK': 'NO', 'KRW': 'KR',
    'TRY': 'TR', 'RUB': 'RU', 'INR': 'IN', 'BRL': 'BR', 'ZAR': 'ZA',
    'DKK': 'DK', 'PLN': 'PL', 'TWD': 'TW', 'THB': 'TH', 'MYR': 'MY',
    'IDR': 'ID', 'HUF': 'HU', 'CZK': 'CZ', 'ILS': 'IL', 'CLP': 'CL',
    'PHP': 'PH', 'AED': 'AE', 'COP': 'CO', 'SAR': 'SA', 'RON': 'RO',
    'BGN': 'BG', 'ARS': 'AR', 'VND': 'VN', 'UAH': 'UA', 'BDT': 'BD',
}


def get_country_flag_emoji(country_code):
    """
    Convert country code to flag emoji.

    Args:
        country_code: 2-letter country code (e.g., 'US')

    Returns:
        Flag emoji string (e.g., '🇺🇸')
    """
    if not country_code or len(country_code) != 2:
        return '🏳️'

    # Convert to regional indicator symbols
    # A=127462 (🇦), B=127463 (🇧), etc.
    return ''.join(chr(127462 + ord(c) - ord('A')) for c in country_code.upper())


def get_currency_flag(currency_code):
    """
    Get flag emoji for currency code.

    Args:
        currency_code: 3-letter currency code (e.g., 'USD')

    Returns:
        Flag emoji or generic flag for unmapped currencies
    """
    country_code = CURRENCY_TO_COUNTRY.get(currency_code)
    if country_code:
        return get_country_flag_emoji(country_code)
    return '💱'  # Currency exchange symbol for unmapped currencies


def get_current_currency(request):
    """
    Get current currency from session or cookie.

    Priority:
    1. Session currency
    2. Cookie currency
    3. GeoIP detection
    4. Site default currency

    Args:
        request: Django request object

    Returns:
        Currency code string (e.g., 'USD')
    """
    # Check session
    if 'currency' in request.session:
        return request.session['currency']

    # Check cookie
    if 'selected_currency' in request.COOKIES:
        currency = request.COOKIES['selected_currency']
        # Validate it's a supported currency
        settings_obj = SiteSettings.get_settings()
        if settings_obj.supported_currencies and currency in settings_obj.supported_currencies:
            request.session['currency'] = currency
            return currency

    # GeoIP detection (if available)
    if hasattr(request, 'geo_location') and request.geo_location:
        # Map country to currency (you may want to add a more comprehensive mapping)
        country_to_currency = {
            'US': 'USD', 'CA': 'CAD', 'GB': 'GBP', 'AU': 'AUD', 'NZ': 'NZD',
            'JP': 'JP', 'CN': 'CNY', 'IN': 'INR', 'BR': 'BRL', 'MX': 'MXN',
            'SG': 'SGD', 'HK': 'HKD', 'KR': 'KRW', 'TH': 'THB', 'MY': 'MYR',
            'ID': 'IDR', 'PH': 'PHP', 'VN': 'VND', 'TR': 'TRY', 'SA': 'SAR',
            'AE': 'AED', 'ZA': 'ZAR', 'IL': 'IL', 'RU': 'RUB', 'UA': 'UAH',
            'PL': 'PLN', 'CZ': 'CZK', 'HU': 'HUF', 'RO': 'RON', 'BG': 'BGN',
            'NO': 'NOK', 'SE': 'SEK', 'DK': 'DKK', 'CH': 'CHF', 'CL': 'CLP',
            'CO': 'COP', 'AR': 'ARS',
        }

        # Eurozone countries
        eurozone = [
            'AT', 'BE', 'CY', 'EE', 'FI', 'FR', 'DE', 'GR', 'IE', 'IT',
            'LV', 'LT', 'LU', 'MT', 'NL', 'PT', 'SK', 'SI', 'ES'
        ]

        country_code = request.geo_location.get('country_code', '').upper()

        if country_code in eurozone:
            currency = 'EUR'
        else:
            currency = country_to_currency.get(country_code)

        if currency:
            settings_obj = SiteSettings.get_settings()
            if not settings_obj.supported_currencies or currency in settings_obj.supported_currencies:
                request.session['currency'] = currency
                return currency

    # Default to site currency
    settings_obj = SiteSettings.get_settings()
    return settings_obj.default_currency


def currency_context(request):
    """
    Context processor to provide currency data to all templates.

    Adds:
    - current_currency: Current selected currency data
    - available_currencies: List of available currencies for switcher
    - multi_currency_enabled: Boolean flag

    Returns:
        Dict with currency context data
    """
    settings_obj = SiteSettings.get_settings()

    # Check if multi-currency is enabled
    if not settings_obj.enable_multi_currency:
        default_curr = CURRENCIES.get(settings_obj.default_currency, CURRENCIES['USD'])
        return {
            'multi_currency_enabled': False,
            'current_currency': {
                'code': settings_obj.default_currency,
                'symbol': getattr(default_curr, 'symbol', settings_obj.default_currency),
                'name': getattr(default_curr, 'name', 'US Dollar'),
                'flag': get_currency_flag(settings_obj.default_currency),
            },
            'available_currencies': [],
        }

    # Get current currency
    current_currency_code = get_current_currency(request)

    # Get available currencies
    if settings_obj.supported_currencies:
        available_currency_codes = settings_obj.supported_currencies
    else:
        # If no specific currencies configured, use common currencies
        from core.utils.currency_helpers import get_common_currencies
        available_currency_codes = [code for code, _ in get_common_currencies()]

    # Build currency data
    available_currencies = []
    for code in available_currency_codes:
        if code not in CURRENCIES:
            continue

        currency_obj = CURRENCIES[code]
        available_currencies.append({
            'code': code,
            'symbol': getattr(currency_obj, 'symbol', code),
            'name': getattr(currency_obj, 'name', code),
            'flag': get_currency_flag(code),
        })

    # Current currency data
    current_currency = None
    if current_currency_code in CURRENCIES:
        currency_obj = CURRENCIES[current_currency_code]
        current_currency = {
            'code': current_currency_code,
            'symbol': getattr(currency_obj, 'symbol', current_currency_code),
            'name': getattr(currency_obj, 'name', current_currency_code),
            'flag': get_currency_flag(current_currency_code),
        }
    else:
        # Fallback to first available
        dc = settings_obj.default_currency
        current_currency = available_currencies[0] if available_currencies else {
            'code': dc,
            'symbol': CURRENCIES[dc].symbol if dc in CURRENCIES else dc,
            'name': CURRENCIES[dc].name if dc in CURRENCIES else dc,
            'flag': get_currency_flag(dc),
        }

    return {
        'multi_currency_enabled': True,
        'current_currency': current_currency,
        'available_currencies': available_currencies,
    }
