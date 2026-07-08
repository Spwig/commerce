"""
Currency helper utilities for multi-currency support.

This module provides utilities for working with currencies using django-money's
full currency list (308 currencies) instead of hardcoded values.
"""

from django.utils.translation import gettext_lazy as _
from decimal import Decimal, ROUND_HALF_UP
import logging

logger = logging.getLogger(__name__)


def get_all_currencies():
    """
    Get all available currencies from django-money (308 total).

    Returns:
        list: List of tuples [(code, display_name), ...]
              e.g., [('USD', 'USD - US Dollar'), ('EUR', 'EUR - Euro'), ...]
    """
    from moneyed import CURRENCIES

    return [
        (code, f"{code} - {curr.name}")
        for code, curr in CURRENCIES.items()
    ]


def get_common_currencies():
    """
    Get commonly used currencies for quick selection.

    Returns:
        list: List of tuples [(code, display_name), ...]
    """
    from moneyed import CURRENCIES

    # Common currencies used in e-commerce
    common = [
        'USD',  # US Dollar
        'EUR',  # Euro
        'GBP',  # British Pound
        'JPY',  # Japanese Yen
        'CNY',  # Chinese Yuan
        'CAD',  # Canadian Dollar
        'AUD',  # Australian Dollar
        'CHF',  # Swiss Franc
        'HKD',  # Hong Kong Dollar
        'SGD',  # Singapore Dollar
        'SEK',  # Swedish Krona
        'NOK',  # Norwegian Krone
        'NZD',  # New Zealand Dollar
        'INR',  # Indian Rupee
        'KRW',  # South Korean Won
        'MXN',  # Mexican Peso
        'BRL',  # Brazilian Real
        'ZAR',  # South African Rand
        'DKK',  # Danish Krone
        'PLN',  # Polish Złoty
    ]

    return [
        (code, f"{code} - {CURRENCIES[code].name}")
        for code in common
        if code in CURRENCIES
    ]


def get_currency_decimal_places(currency_code):
    """
    Get decimal places for currency based on ISO 4217 standard.

    Zero decimal place currencies (no cents):
    - JPY (Japanese Yen), KRW (Korean Won), VND (Vietnamese Dong), etc.

    Three decimal place currencies:
    - BHD (Bahraini Dinar), IQD (Iraqi Dinar), JOD (Jordanian Dinar), etc.

    Four decimal place currencies (rare):
    - CLF (Chilean Unit of Account), UYW (Uruguayan Nominal Wage Index Unit)

    Args:
        currency_code: ISO 4217 currency code (e.g., 'USD', 'JPY')

    Returns:
        int: Number of decimal places (0, 2, 3, or 4)
    """
    # Zero decimal currencies
    no_decimal_currencies = [
        'BIF',  # Burundian Franc
        'CLP',  # Chilean Peso
        'DJF',  # Djiboutian Franc
        'GNF',  # Guinean Franc
        'ISK',  # Icelandic Króna
        'JPY',  # Japanese Yen
        'KMF',  # Comorian Franc
        'KRW',  # South Korean Won
        'PYG',  # Paraguayan Guaraní
        'RWF',  # Rwandan Franc
        'UGX',  # Ugandan Shilling
        'VND',  # Vietnamese Dong
        'VUV',  # Vanuatu Vatu
        'XAF',  # Central African CFA Franc
        'XOF',  # West African CFA Franc
        'XPF',  # CFP Franc
    ]

    # Three decimal currencies
    three_decimal_currencies = [
        'BHD',  # Bahraini Dinar
        'IQD',  # Iraqi Dinar
        'JOD',  # Jordanian Dinar
        'KWD',  # Kuwaiti Dinar
        'LYD',  # Libyan Dinar
        'OMR',  # Omani Rial
        'TND',  # Tunisian Dinar
    ]

    # Four decimal currencies (rare)
    four_decimal_currencies = [
        'CLF',  # Chilean Unit of Account (UF)
        'UYW',  # Uruguayan Nominal Wage Index Unit
    ]

    if currency_code in no_decimal_currencies:
        return 0
    elif currency_code in three_decimal_currencies:
        return 3
    elif currency_code in four_decimal_currencies:
        return 4
    else:
        return 2  # Default for most currencies


def round_money(amount, currency_code):
    """
    Round money amount according to currency decimal places.

    Args:
        amount: Decimal amount
        currency_code: Currency code

    Returns:
        Decimal: Rounded Decimal amount
    """
    if not isinstance(amount, Decimal):
        amount = Decimal(str(amount))

    decimal_places = get_currency_decimal_places(currency_code)

    if decimal_places == 0:
        return amount.quantize(Decimal('1'), rounding=ROUND_HALF_UP)
    else:
        quantizer = Decimal('0.1') ** decimal_places
        return amount.quantize(quantizer, rounding=ROUND_HALF_UP)


def format_money(amount, currency_code, locale=None):
    """
    Format money according to locale conventions.

    Uses Babel for locale-aware formatting when available.

    Args:
        amount: Decimal amount
        currency_code: ISO 4217 currency code
        locale: Locale code (e.g., 'en_US', 'de_DE'). If None, uses currency's default.

    Returns:
        str: Formatted money string

    Examples:
        >>> format_money(Decimal('1234.56'), 'USD', 'en_US')
        '$1,234.56'
        >>> format_money(Decimal('1234.56'), 'EUR', 'de_DE')
        '1.234,56 €'
        >>> format_money(Decimal('1234'), 'JPY', 'ja_JP')
        '¥1,234'
    """
    try:
        from babel.numbers import format_currency

        # Default locales for common currencies
        currency_locales = {
            'USD': 'en_US',
            'EUR': 'de_DE',  # German format: 1.234,56 €
            'GBP': 'en_GB',
            'JPY': 'ja_JP',
            'CNY': 'zh_CN',
            'AUD': 'en_AU',
            'CAD': 'en_CA',
            'CHF': 'de_CH',
            'HKD': 'en_HK',
            'SGD': 'en_SG',
            'SEK': 'sv_SE',
            'NOK': 'nb_NO',
            'DKK': 'da_DK',
            'INR': 'en_IN',
            'KRW': 'ko_KR',
            'MXN': 'es_MX',
            'BRL': 'pt_BR',
            'ZAR': 'en_ZA',
        }

        if not locale:
            locale = currency_locales.get(currency_code, 'en_US')

        return format_currency(amount, currency_code, locale=locale)

    except ImportError:
        logger.warning("Babel not installed, using fallback formatting")
        # Fallback to simple format
        return _format_money_simple(amount, currency_code)
    except Exception as e:
        logger.warning(f"Babel currency formatting failed: {e}")
        return _format_money_simple(amount, currency_code)


def _format_money_simple(amount, currency_code):
    """
    Simple money formatting fallback when Babel is unavailable.

    Args:
        amount: Decimal amount
        currency_code: Currency code

    Returns:
        str: Formatted money string
    """
    from moneyed import CURRENCIES

    if currency_code not in CURRENCIES:
        return f"{amount} {currency_code}"

    currency_obj = CURRENCIES[currency_code]
    symbol = getattr(currency_obj, 'symbol', currency_code)

    # Format with proper decimal places
    decimal_places = get_currency_decimal_places(currency_code)

    if decimal_places == 0:
        formatted_amount = f"{amount:,.0f}"
    else:
        formatted_amount = f"{amount:,.{decimal_places}f}"

    return f"{symbol}{formatted_amount}"


def get_currency_symbol(currency_code):
    """
    Get currency symbol for currency code.

    Args:
        currency_code: ISO 4217 currency code

    Returns:
        str: Currency symbol (e.g., "$", "€", "£")
    """
    from moneyed import CURRENCIES

    if currency_code not in CURRENCIES:
        return currency_code

    currency_obj = CURRENCIES[currency_code]
    return getattr(currency_obj, 'symbol', currency_code)


def get_currency_name(currency_code):
    """
    Get currency name for currency code.

    Args:
        currency_code: ISO 4217 currency code

    Returns:
        str: Currency name (e.g., "US Dollar", "Euro")
    """
    from moneyed import CURRENCIES

    if currency_code not in CURRENCIES:
        return currency_code

    currency_obj = CURRENCIES[currency_code]
    return currency_obj.name


def validate_currency_code(currency_code):
    """
    Validate if currency code is valid and supported by django-money.

    Args:
        currency_code: Currency code to validate

    Returns:
        bool: True if valid, False otherwise
    """
    from moneyed import CURRENCIES
    return currency_code in CURRENCIES


def get_enabled_currencies():
    """
    Get currencies enabled in site settings for form choices.

    Returns list of enabled currencies from SiteSettings.supported_currencies
    If no currencies are enabled, returns only the default currency.

    Returns:
        list: List of tuples [(code, display_name), ...]
              e.g., [('USD', 'USD - US Dollar'), ('EUR', 'EUR - Euro'), ...]
    """
    from moneyed import CURRENCIES
    from core.models import SiteSettings
    from core.supported_currency_model import SupportedCurrency

    try:
        settings = SiteSettings.get_settings()

        # Check if multi-currency is enabled
        if not settings.enable_multi_currency:
            # Only return default currency
            default_currency = settings.default_currency
            if default_currency in CURRENCIES:
                return [(default_currency, f"{default_currency} - {CURRENCIES[default_currency].name}")]
            return [(default_currency, default_currency)]

        # Get active currencies from SupportedCurrency model
        active_codes = SupportedCurrency.get_active_codes()

        if not active_codes:
            # If no currencies are active, return default currency only
            default_currency = settings.default_currency
            if default_currency in CURRENCIES:
                return [(default_currency, f"{default_currency} - {CURRENCIES[default_currency].name}")]
            return [(default_currency, default_currency)]

        # Build choices from active currencies
        choices = []
        for code in active_codes:
            if code in CURRENCIES:
                choices.append((code, f"{code} - {CURRENCIES[code].name}"))

        if not choices:
            default_currency = settings.default_currency
            return [(default_currency, f"{default_currency} - {CURRENCIES[default_currency].name}" if default_currency in CURRENCIES else default_currency)]

        return choices

    except Exception as e:
        from core.utils import get_default_currency
        dc = get_default_currency()
        logger.warning(f"Failed to get enabled currencies: {e}, falling back to {dc}")
        return [(dc, dc)]
