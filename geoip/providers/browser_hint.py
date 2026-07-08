"""
Browser Hint Provider - Uses browser hints (language, timezone) as fallback
"""
from typing import Dict, Optional, Any
from .base import GeoIPProviderBase
import re
import logging

logger = logging.getLogger(__name__)


class BrowserHintProvider(GeoIPProviderBase):
    """
    Provider that uses browser hints (Accept-Language, timezone) to guess location
    This is a fallback provider with lower confidence
    """

    # Language to country mapping (most common)
    LANGUAGE_COUNTRY_MAP = {
        'en-US': 'US',
        'en-GB': 'GB',
        'en-AU': 'AU',
        'en-CA': 'CA',
        'en-NZ': 'NZ',
        'en-IN': 'IN',
        'en-ZA': 'ZA',
        'es-ES': 'ES',
        'es-MX': 'MX',
        'es-AR': 'AR',
        'es-CO': 'CO',
        'es-CL': 'CL',
        'fr-FR': 'FR',
        'fr-CA': 'CA',
        'fr-BE': 'BE',
        'fr-CH': 'CH',
        'de-DE': 'DE',
        'de-AT': 'AT',
        'de-CH': 'CH',
        'it-IT': 'IT',
        'it-CH': 'CH',
        'pt-PT': 'PT',
        'pt-BR': 'BR',
        'nl-NL': 'NL',
        'nl-BE': 'BE',
        'ru-RU': 'RU',
        'zh-CN': 'CN',
        'zh-TW': 'TW',
        'zh-HK': 'HK',
        'ja-JP': 'JP',
        'ko-KR': 'KR',
        'ar-SA': 'SA',
        'ar-AE': 'AE',
        'ar-EG': 'EG',
        'hi-IN': 'IN',
        'th-TH': 'TH',
        'vi-VN': 'VN',
        'id-ID': 'ID',
        'ms-MY': 'MY',
        'tr-TR': 'TR',
        'pl-PL': 'PL',
        'uk-UA': 'UA',
        'cs-CZ': 'CZ',
        'sv-SE': 'SE',
        'da-DK': 'DK',
        'no-NO': 'NO',
        'fi-FI': 'FI',
        'el-GR': 'GR',
        'he-IL': 'IL',
    }

    # Timezone to country mapping (approximate)
    TIMEZONE_COUNTRY_MAP = {
        -11: ['AS', 'NU'],  # UTC-11
        -10: ['US'],  # Hawaii
        -9: ['US'],   # Alaska
        -8: ['US', 'CA', 'MX'],  # Pacific Time
        -7: ['US', 'CA', 'MX'],  # Mountain Time
        -6: ['US', 'CA', 'MX'],  # Central Time
        -5: ['US', 'CA', 'CO', 'PE', 'EC'],  # Eastern Time
        -4: ['CA', 'BR', 'CL', 'AR'],  # Atlantic Time
        -3: ['BR', 'AR', 'UY'],  #
        -2: ['BR'],   #
        -1: ['PT'],   # Azores
        0: ['GB', 'IE', 'PT', 'IS'],  # UTC
        1: ['DE', 'FR', 'IT', 'ES', 'NO', 'SE', 'PL'],  # CET
        2: ['FI', 'EE', 'LV', 'LT', 'UA', 'RO', 'BG', 'GR', 'EG', 'ZA'],  # EET
        3: ['RU', 'SA', 'KE', 'ET'],  # Moscow, Arabia
        4: ['AE', 'AM', 'AZ'],  # Gulf
        5: ['PK', 'UZ'],  # Pakistan
        5.5: ['IN', 'LK'],  # India
        6: ['KZ', 'BD'],  #
        7: ['TH', 'VN', 'ID'],  # Indochina
        8: ['CN', 'MY', 'SG', 'PH', 'AU'],  # China, SE Asia
        9: ['JP', 'KR'],  # Japan, Korea
        10: ['AU'],  # Eastern Australia
        11: ['AU', 'NC'],  #
        12: ['NZ', 'FJ'],  # New Zealand
    }

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.request = None

    def initialize(self) -> bool:
        """
        No initialization needed
        """
        self._initialized = True
        return True

    def is_available(self) -> bool:
        """
        Available if we have a request object
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
        Guess location from browser hints

        Args:
            ip: IP address (not used, but kept for interface compatibility)

        Returns:
            Guessed location data
        """
        if not self.request:
            return None

        result = {}
        confidence = 0.0

        # Try Accept-Language header
        accept_language = self.request.META.get('HTTP_ACCEPT_LANGUAGE', '')
        if accept_language:
            country = self._parse_accept_language(accept_language)
            if country:
                result['country_code'] = country
                confidence += 0.3

        # Try timezone if available (requires JavaScript to send)
        timezone_offset = self._get_timezone_offset()
        if timezone_offset is not None:
            countries = self._guess_countries_from_timezone(timezone_offset)
            if countries:
                # If we already have a country from language, check if it matches
                if 'country_code' in result:
                    if result['country_code'] in countries:
                        confidence += 0.2  # Matching increases confidence
                else:
                    # Use first country from timezone
                    result['country_code'] = countries[0]
                    confidence += 0.2

        # Check User-Agent for mobile
        user_agent = self.request.META.get('HTTP_USER_AGENT', '').lower()
        if any(device in user_agent for device in ['mobile', 'android', 'iphone', 'ipad']):
            result['is_mobile'] = True

        if not result:
            return None

        # This is a low-confidence provider
        result['source'] = 'browser_hint'
        result['confidence'] = min(confidence, 0.5)  # Cap at 0.5

        return self.format_response(result)

    def _parse_accept_language(self, header: str) -> Optional[str]:
        """
        Parse Accept-Language header to get country

        Args:
            header: Accept-Language header value

        Returns:
            Country code or None
        """
        # Parse header like: "en-US,en;q=0.9,es;q=0.8"
        languages = []
        for part in header.split(','):
            lang_quality = part.strip().split(';')
            lang = lang_quality[0].strip()
            quality = 1.0

            if len(lang_quality) > 1:
                try:
                    quality = float(lang_quality[1].split('=')[1])
                except (IndexError, ValueError):
                    quality = 0.0

            languages.append((lang, quality))

        # Sort by quality
        languages.sort(key=lambda x: x[1], reverse=True)

        # Try to find country from language codes
        for lang, _ in languages:
            # Try full language-country code first
            if lang in self.LANGUAGE_COUNTRY_MAP:
                return self.LANGUAGE_COUNTRY_MAP[lang]

            # Try to extract country from language code (e.g., en-US -> US)
            match = re.match(r'^[a-z]{2,3}-([A-Z]{2})$', lang)
            if match:
                return match.group(1)

        return None

    def _get_timezone_offset(self) -> Optional[float]:
        """
        Get timezone offset from request

        Returns:
            Timezone offset in hours or None
        """
        # This would typically be sent via JavaScript
        # Check if it's in session or cookie
        if hasattr(self.request, 'session'):
            offset_minutes = self.request.session.get('timezone_offset')
            if offset_minutes is not None:
                return -offset_minutes / 60  # Convert to hours, invert sign

        # Check cookies
        if hasattr(self.request, 'COOKIES'):
            offset = self.request.COOKIES.get('timezone_offset')
            if offset:
                try:
                    return -float(offset) / 60
                except ValueError:
                    pass

        return None

    def _guess_countries_from_timezone(self, offset: float) -> list:
        """
        Guess possible countries from timezone offset

        Args:
            offset: Timezone offset in hours

        Returns:
            List of possible country codes
        """
        # Handle half-hour timezones
        for tz_offset, countries in self.TIMEZONE_COUNTRY_MAP.items():
            if abs(tz_offset - offset) < 0.5:
                return countries

        return []