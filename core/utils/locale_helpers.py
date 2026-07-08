"""
Locale Helper Utilities

Provides utilities to bridge GeoIP data with Site Settings for currency, language,
and timezone configuration. Leverages GeoIP CountryMapping data and django-money
for comprehensive international support.
"""
from typing import List, Tuple, Dict, Optional
from django.conf import settings
from django.utils.translation import gettext_lazy as _


def get_all_currencies() -> List[Tuple[str, str]]:
    """
    Get all available currencies from django-money, excluding obsolete and special purpose currencies.

    Filters out:
    - Historical/obsolete currencies (e.g., old European currencies before Euro)
    - Special purpose codes (e.g., gold, silver, test currencies)
    - Non-circulating currencies (e.g., IMF SDR, funds codes)

    Returns:
        List of tuples: [(code, display_name), ...]
        Example: [('USD', 'US Dollar (USD)'), ('EUR', 'Euro (EUR)'), ...]

    Note:
        Returns ~150-170 active e-commerce currencies out of django-money's 308 total currencies.
    """
    # Obsolete/historical currencies
    OBSOLETE_CURRENCIES = {
        'ADP', 'AFA', 'ALK', 'AOK', 'AON', 'AOR', 'ARA', 'ARL', 'ARM', 'ARP', 'ATS', 'AZM',
        'BAD', 'BAN', 'BEC', 'BEF', 'BEL', 'BGL', 'BGO', 'BOL', 'BRB', 'BRC', 'BRE', 'BRN', 'BRR', 'BRZ', 'BYB', 'BYR',
        'CLE', 'CSD', 'CSK', 'CYP', 'DDM', 'DEM', 'ECS', 'ECV', 'EEK',
        'ESA', 'ESB', 'ESP', 'FIM', 'FRF', 'GHC', 'GRD', 'GWP',
        'HRD', 'IEP', 'ILR', 'ILP', 'ISJ', 'ITL', 'KRH', 'KRO', 'LTL', 'LUC', 'LUF', 'LUL', 'LVL',
        'MGF', 'MKN', 'MLF', 'MRO', 'MTL', 'MVP', 'MXP', 'MZM',
        'NIC', 'NLG', 'PEI', 'PES', 'PLZ', 'PTE', 'ROL',
        'RUR', 'SDD', 'SDP', 'SIT', 'SKK', 'SLL', 'SRG', 'STD', 'SUR', 'TJR', 'TMM',
        'TPE', 'TRL', 'TVD', 'UAK', 'UGS', 'UYP', 'VEB', 'VEF', 'VNN',
        'XEU', 'YDD', 'YUD', 'YUM', 'YUN', 'YUR',
        'ZAL', 'ZMK', 'ZRN', 'ZRZ', 'ZWD', 'ZWN', 'ZWR',
        'BUK', 'GEK', 'GNS', 'GQE', 'GWE', 'LTT', 'LVR', 'MAF', 'MCF', 'MTP', 'MZE', 'RHD',
    }

    # Special/non-circulating currencies
    SPECIAL_CURRENCIES = {
        'XAU', 'XAG', 'XPT', 'XPD',  # Precious metals
        'XDR', 'XSU', 'XUA', 'XXX', 'XTS',  # Special purpose
        'XBA', 'XBB', 'XBC', 'XBD', 'XFO', 'XRE', 'XBR', 'XFU', 'XPF',  # Special settlement
        'CHE', 'CHW', 'CLF', 'MXV', 'USN', 'USS', 'UYI', 'UYW',  # Funds codes
        'NPW', 'BOV', 'COU', 'CUC', 'KPW', 'MDC',  # Not for general use
    }

    try:
        from moneyed import list_all_currencies

        currencies = []
        for currency in list_all_currencies():
            # Filter out obsolete and special purpose currencies
            if currency.code in OBSOLETE_CURRENCIES or currency.code in SPECIAL_CURRENCIES:
                continue

            # Format: "Currency Name (CODE)"
            display_name = f"{currency.name} ({currency.code})"
            currencies.append((currency.code, display_name))

        # Sort alphabetically by code
        return sorted(currencies, key=lambda x: x[0])
    except ImportError:
        # Fallback if moneyed is not installed
        return [
            ('USD', 'US Dollar (USD)'),
            ('EUR', 'Euro (EUR)'),
            ('GBP', 'British Pound (GBP)'),
        ]


def get_popular_currencies() -> List[Tuple[str, str]]:
    """
    Get the most commonly used currencies worldwide.

    Returns:
        List of tuples with top 20 currencies by global usage

    Based on:
        - IMF Special Drawing Rights basket
        - Global payment currencies (SWIFT data)
        - Major trading currencies
    """
    popular = [
        ('USD', 'US Dollar ($)'),
        ('EUR', 'Euro (€)'),
        ('GBP', 'British Pound (£)'),
        ('JPY', 'Japanese Yen (¥)'),
        ('CNY', 'Chinese Yuan (¥)'),
        ('CAD', 'Canadian Dollar (C$)'),
        ('AUD', 'Australian Dollar (A$)'),
        ('CHF', 'Swiss Franc (CHF)'),
        ('SEK', 'Swedish Krona (kr)'),
        ('NZD', 'New Zealand Dollar (NZ$)'),
        ('MXN', 'Mexican Peso (MX$)'),
        ('SGD', 'Singapore Dollar (S$)'),
        ('HKD', 'Hong Kong Dollar (HK$)'),
        ('NOK', 'Norwegian Krone (kr)'),
        ('KRW', 'South Korean Won (₩)'),
        ('TRY', 'Turkish Lira (₺)'),
        ('INR', 'Indian Rupee (₹)'),
        ('BRL', 'Brazilian Real (R$)'),
        ('ZAR', 'South African Rand (R)'),
        ('DKK', 'Danish Krone (kr)'),
    ]
    return popular


def get_grouped_currencies() -> Dict[str, List[Tuple[str, str]]]:
    """
    Get currencies organized into groups for better UI/UX.

    Returns:
        Dictionary with groups: 'popular', 'crypto', 'all'

    Usage in forms:
        Used to create optgroups in select widgets for better organization
    """
    all_currencies = get_all_currencies()
    popular_codes = [code for code, _ in get_popular_currencies()]

    # Separate popular from the rest
    popular = [(code, name) for code, name in all_currencies if code in popular_codes]
    other = [(code, name) for code, name in all_currencies if code not in popular_codes]

    return {
        'popular': sorted(popular, key=lambda x: popular_codes.index(x[0])),
        'other': other,
        'all': all_currencies,
    }


def get_all_timezones() -> List[Tuple[str, str]]:
    """
    Get all available timezones from Python's zoneinfo.

    Returns:
        List of tuples: [(timezone, display_name), ...]
        Example: [('America/New_York', 'America/New_York (UTC-5)'), ...]

    Note:
        Returns 599 timezones from the IANA Time Zone Database
    """
    import zoneinfo
    from datetime import datetime, timezone as dt_timezone

    timezones = []
    now = datetime.now(dt_timezone.utc)

    for tz_name in sorted(zoneinfo.available_timezones()):
        try:
            # Get UTC offset for display
            tz = zoneinfo.ZoneInfo(tz_name)
            aware_now = now.astimezone(tz)
            offset = aware_now.utcoffset()

            if offset:
                total_seconds = int(offset.total_seconds())
                hours = total_seconds // 3600
                minutes = abs(total_seconds % 3600) // 60
                if minutes:
                    offset_str = f"UTC{hours:+d}:{minutes:02d}"
                else:
                    offset_str = f"UTC{hours:+d}"
            else:
                offset_str = "UTC±0"

            display_name = f"{tz_name} ({offset_str})"
            timezones.append((tz_name, display_name))
        except Exception:
            # If offset calculation fails, just use timezone name
            timezones.append((tz_name, tz_name))

    return timezones


def get_popular_timezones() -> List[Tuple[str, str]]:
    """
    Get commonly used timezones grouped by major regions.

    Returns:
        List of tuples with ~30 most commonly used timezones
    """
    popular = [
        # UTC
        ('UTC', 'UTC (Coordinated Universal Time)'),

        # Americas
        ('America/New_York', 'Eastern Time - New York (UTC-5/-4)'),
        ('America/Chicago', 'Central Time - Chicago (UTC-6/-5)'),
        ('America/Denver', 'Mountain Time - Denver (UTC-7/-6)'),
        ('America/Los_Angeles', 'Pacific Time - Los Angeles (UTC-8/-7)'),
        ('America/Phoenix', 'Arizona - Phoenix (UTC-7)'),
        ('America/Toronto', 'Eastern Canada - Toronto (UTC-5/-4)'),
        ('America/Vancouver', 'Pacific Canada - Vancouver (UTC-8/-7)'),
        ('America/Mexico_City', 'Mexico City (UTC-6/-5)'),
        ('America/Sao_Paulo', 'Brazil - São Paulo (UTC-3)'),
        ('America/Argentina/Buenos_Aires', 'Argentina - Buenos Aires (UTC-3)'),

        # Europe
        ('Europe/London', 'United Kingdom - London (UTC±0/+1)'),
        ('Europe/Paris', 'France - Paris (UTC+1/+2)'),
        ('Europe/Berlin', 'Germany - Berlin (UTC+1/+2)'),
        ('Europe/Rome', 'Italy - Rome (UTC+1/+2)'),
        ('Europe/Madrid', 'Spain - Madrid (UTC+1/+2)'),
        ('Europe/Amsterdam', 'Netherlands - Amsterdam (UTC+1/+2)'),
        ('Europe/Brussels', 'Belgium - Brussels (UTC+1/+2)'),
        ('Europe/Zurich', 'Switzerland - Zurich (UTC+1/+2)'),
        ('Europe/Stockholm', 'Sweden - Stockholm (UTC+1/+2)'),
        ('Europe/Moscow', 'Russia - Moscow (UTC+3)'),

        # Asia
        ('Asia/Dubai', 'UAE - Dubai (UTC+4)'),
        ('Asia/Kolkata', 'India - Kolkata (UTC+5:30)'),
        ('Asia/Singapore', 'Singapore (UTC+8)'),
        ('Asia/Hong_Kong', 'Hong Kong (UTC+8)'),
        ('Asia/Shanghai', 'China - Shanghai (UTC+8)'),
        ('Asia/Tokyo', 'Japan - Tokyo (UTC+9)'),
        ('Asia/Seoul', 'South Korea - Seoul (UTC+9)'),

        # Pacific
        ('Australia/Sydney', 'Australia - Sydney (UTC+10/+11)'),
        ('Australia/Melbourne', 'Australia - Melbourne (UTC+10/+11)'),
        ('Pacific/Auckland', 'New Zealand - Auckland (UTC+12/+13)'),
    ]
    return popular


def get_grouped_timezones() -> Dict[str, List[Tuple[str, str]]]:
    """
    Get timezones organized by geographic region.

    Returns:
        Dictionary with regions: 'popular', 'americas', 'europe', 'asia', 'africa', 'pacific', 'other'
    """
    all_timezones = get_all_timezones()

    groups = {
        'popular': get_popular_timezones(),
        'americas': [],
        'europe': [],
        'asia': [],
        'africa': [],
        'pacific': [],
        'other': [],
    }

    for tz_code, tz_display in all_timezones:
        if tz_code.startswith('America/'):
            groups['americas'].append((tz_code, tz_display))
        elif tz_code.startswith('Europe/'):
            groups['europe'].append((tz_code, tz_display))
        elif tz_code.startswith('Asia/'):
            groups['asia'].append((tz_code, tz_display))
        elif tz_code.startswith('Africa/'):
            groups['africa'].append((tz_code, tz_display))
        elif tz_code.startswith('Pacific/') or tz_code.startswith('Australia/'):
            groups['pacific'].append((tz_code, tz_display))
        elif tz_code not in [code for code, _ in groups['popular']]:
            groups['other'].append((tz_code, tz_display))

    return groups


def get_all_languages() -> List[Tuple[str, str]]:
    """
    Get all available languages from Django's global settings.

    Returns:
        List of tuples: [(code, display_name), ...]
        Example: [('en', 'English'), ('es', 'Spanish'), ...]

    Note:
        Uses Django's global_settings.LANGUAGES which includes 99 languages.
        This provides a comprehensive list beyond the project's LANGUAGES setting.
    """
    # Import Django's global languages list (99 languages)
    from django.conf import global_settings

    # Use Django's complete language list
    languages = list(global_settings.LANGUAGES)

    return sorted(languages, key=lambda x: x[1])


def get_admin_languages() -> List[Tuple[str, str]]:
    """
    Get languages supported for the admin interface.

    Based on rules.md Target Languages for admin interface:
    - Primary: English (en)
    - Secondary: Spanish (es), French (fr), German (de), Japanese (ja), Portuguese (pt), Chinese (zh-hans)

    Returns:
        List of admin-supported languages
    """
    return [
        ('en', 'English'),
        ('es', 'Spanish (Español)'),
        ('fr', 'French (Français)'),
        ('de', 'German (Deutsch)'),
        ('ja', 'Japanese (日本語)'),
        ('pt', 'Portuguese (Português)'),
        ('zh-hans', 'Chinese Simplified (简体中文)'),
    ]


def get_grouped_languages() -> Dict[str, List[Tuple[str, str]]]:
    """
    Get languages organized into groups.

    Returns:
        Dictionary with groups: 'admin', 'popular', 'all'
    """
    admin_langs = get_admin_languages()
    all_langs = get_all_languages()

    admin_codes = {code for code, _ in admin_langs}

    # Popular languages (by number of speakers)
    popular_codes = {
        'en', 'zh', 'zh-hans', 'zh-hant', 'es', 'hi', 'ar', 'pt', 'bn', 'ru',
        'ja', 'pa', 'de', 'jv', 'ko', 'fr', 'te', 'mr', 'tr', 'ta', 'vi', 'ur'
    }

    popular = [(code, name) for code, name in all_langs
               if code in popular_codes and code not in admin_codes]

    other = [(code, name) for code, name in all_langs
             if code not in admin_codes and code not in popular_codes]

    return {
        'admin': admin_langs,
        'popular': popular,
        'other': other,
        'all': all_langs,
    }


def get_country_defaults(country_code: str) -> Optional[Dict[str, str]]:
    """
    Get default currency, language, and timezone for a country from GeoIP data.

    Args:
        country_code: ISO 2-letter country code (e.g., 'US', 'GB', 'FR')

    Returns:
        Dictionary with 'currency', 'language', 'timezone', 'uses_metric'
        or None if country not found

    Example:
        >>> get_country_defaults('US')
        {
            'currency': 'USD',
            'language': 'en',
            'timezone': 'America/New_York',
            'uses_metric': False
        }
    """
    try:
        from geoip.models import CountryMapping

        mapping = CountryMapping.objects.filter(
            country_code=country_code.upper(),
            is_active=True
        ).first()

        if mapping:
            return {
                'currency': mapping.default_currency,
                'language': mapping.default_language,
                'timezone': mapping.timezone or 'UTC',
                'uses_metric': mapping.uses_metric,
            }
    except:
        pass

    return None


def get_currency_symbol(currency_code: str) -> str:
    """
    Get the symbol for a currency code.

    Args:
        currency_code: 3-letter currency code (e.g., 'USD', 'EUR')

    Returns:
        Currency symbol or empty string if not found

    Example:
        >>> get_currency_symbol('USD')
        '$'
    """
    symbols = {
        'USD': '$', 'EUR': '€', 'GBP': '£', 'JPY': '¥', 'CNY': '¥',
        'INR': '₹', 'CAD': 'C$', 'AUD': 'A$', 'CHF': 'CHF', 'SEK': 'kr',
        'NZD': 'NZ$', 'MXN': 'MX$', 'SGD': 'S$', 'HKD': 'HK$', 'NOK': 'kr',
        'KRW': '₩', 'TRY': '₺', 'BRL': 'R$', 'ZAR': 'R', 'DKK': 'kr',
        'PLN': 'zł', 'THB': '฿', 'IDR': 'Rp', 'HUF': 'Ft', 'CZK': 'Kč',
        'ILS': '₪', 'CLP': '$', 'PHP': '₱', 'AED': 'د.إ', 'COP': '$',
        'SAR': '﷼', 'MYR': 'RM', 'RON': 'lei',
    }
    return symbols.get(currency_code, '')


def get_currency_icon(currency_code: str) -> str:
    """
    Get Font Awesome icon class for a currency code.

    Maps currencies to appropriate Font Awesome icons based on currency family.
    Uses specific icons for major currencies and generic fallback for others.

    Args:
        currency_code: 3-letter currency code (e.g., 'USD', 'EUR')

    Returns:
        Font Awesome icon class (e.g., 'fa-dollar-sign', 'fa-euro-sign')

    Example:
        >>> get_currency_icon('USD')
        'fa-dollar-sign'
        >>> get_currency_icon('EUR')
        'fa-euro-sign'
    """
    # Map currencies to Font Awesome icon classes
    icon_map = {
        # Dollar-based currencies
        'USD': 'fa-dollar-sign',
        'CAD': 'fa-dollar-sign',
        'AUD': 'fa-dollar-sign',
        'NZD': 'fa-dollar-sign',
        'HKD': 'fa-dollar-sign',
        'SGD': 'fa-dollar-sign',
        'TWD': 'fa-dollar-sign',
        'MXN': 'fa-dollar-sign',
        'ARS': 'fa-dollar-sign',
        'CLP': 'fa-dollar-sign',
        'COP': 'fa-dollar-sign',

        # Euro
        'EUR': 'fa-euro-sign',

        # Pound
        'GBP': 'fa-pound-sign',
        'EGP': 'fa-pound-sign',
        'SYP': 'fa-pound-sign',
        'LBP': 'fa-pound-sign',

        # Yen/Yuan
        'JPY': 'fa-yen-sign',
        'CNY': 'fa-yen-sign',

        # Rupee
        'INR': 'fa-rupee-sign',
        'PKR': 'fa-rupee-sign',
        'LKR': 'fa-rupee-sign',
        'NPR': 'fa-rupee-sign',
        'IDR': 'fa-rupee-sign',

        # Ruble
        'RUB': 'fa-ruble-sign',

        # Lira
        'TRY': 'fa-lira-sign',

        # Won
        'KRW': 'fa-won-sign',

        # Shekel
        'ILS': 'fa-shekel-sign',

        # Bitcoin and crypto
        'BTC': 'fa-bitcoin',
    }

    return icon_map.get(currency_code, 'fa-money-bill-wave')


def get_timezone_icon(timezone: str) -> str:
    """
    Get Font Awesome icon class for a timezone based on geographic region.

    Maps timezones to regional globe icons. Uses the timezone prefix to determine
    the appropriate regional icon.

    Args:
        timezone: Timezone identifier (e.g., 'America/New_York', 'Europe/London')

    Returns:
        Font Awesome icon class (e.g., 'fa-globe-americas', 'fa-globe-europe')

    Example:
        >>> get_timezone_icon('America/New_York')
        'fa-globe-americas'
        >>> get_timezone_icon('Europe/London')
        'fa-globe-europe'
        >>> get_timezone_icon('UTC')
        'fa-globe'
    """
    if not timezone or timezone == 'UTC':
        return 'fa-globe'

    # Extract region from timezone (e.g., 'America' from 'America/New_York')
    region = timezone.split('/')[0] if '/' in timezone else timezone

    # Map regions to Font Awesome globe icons
    region_icons = {
        'America': 'fa-globe-americas',
        'Europe': 'fa-globe-europe',
        'Asia': 'fa-globe-asia',
        'Africa': 'fa-globe-africa',
        'Pacific': 'fa-globe',
        'Australia': 'fa-globe',
        'Antarctica': 'fa-globe',
        'Atlantic': 'fa-globe',
        'Indian': 'fa-globe',
        'Arctic': 'fa-globe',
    }

    # Return regional icon or clock as fallback
    return region_icons.get(region, 'fa-clock')


def get_language_icon(language_code: str) -> str:
    """
    Get Font Awesome icon class for a language.

    Currently uses a generic language icon for all languages. Could be extended
    in the future to use region-specific icons if needed.

    Args:
        language_code: Language code (e.g., 'en', 'es', 'fr')

    Returns:
        Font Awesome icon class ('fa-language')

    Example:
        >>> get_language_icon('en')
        'fa-language'
        >>> get_language_icon('es')
        'fa-language'
    """
    # Use generic language icon for all languages
    # Future enhancement: Could map specific languages to regional icons
    return 'fa-language'
