"""
Seed default GeoIP providers and enrich priority country mappings with business data.
"""

from core.management.commands._seed_base import SeedCommand
from geoip.models import CountryMapping, GeoIPProvider


class Command(SeedCommand):
    help = "Seed GeoIP providers and enrich priority country mappings with business data"
    seed_name = "geoip_provider"
    seed_version = 1
    dependencies = ["country_mappings"]

    def seed(self) -> int:
        count = 0

        # --- Seed built-in GeoIP providers ---
        _, created = GeoIPProvider.objects.get_or_create(
            provider_type="spwig",
            defaults={
                "name": "Spwig GeoIP",
                "is_active": True,
                "priority": 0,
                "config": {},
            },
        )
        if created:
            count += 1

        _, created = GeoIPProvider.objects.get_or_create(
            provider_type="edge_header",
            defaults={
                "name": "Edge Headers",
                "is_active": True,
                "priority": 100,
                "config": {},
            },
        )
        if created:
            count += 1

        # --- Enrich priority country mappings with business data ---
        # These add tax rates, shipping zones, VAT, payment methods, etc.
        # to the baseline data created by seed_country_mappings.
        countries = [
            # North America
            {
                "country_code": "US",
                "country_name": "United States",
                "default_currency": "USD",
                "accepted_currencies": ["USD"],
                "default_language": "en",
                "supported_languages": ["en", "es"],
                "timezone": "America/New_York",
                "date_format": "MM/DD/YYYY",
                "uses_metric": False,
                "tax_rate": 8.00,
                "is_eu_member": False,
                "requires_vat": False,
                "shipping_zone": "NORTH_AMERICA",
                "supports_cod": False,
            },
            {
                "country_code": "CA",
                "country_name": "Canada",
                "default_currency": "CAD",
                "accepted_currencies": ["CAD", "USD"],
                "default_language": "en",
                "supported_languages": ["en", "fr"],
                "timezone": "America/Toronto",
                "date_format": "DD/MM/YYYY",
                "uses_metric": True,
                "tax_rate": 13.00,
                "is_eu_member": False,
                "requires_vat": False,
                "shipping_zone": "NORTH_AMERICA",
                "supports_cod": False,
            },
            {
                "country_code": "MX",
                "country_name": "Mexico",
                "default_currency": "MXN",
                "accepted_currencies": ["MXN", "USD"],
                "default_language": "es",
                "supported_languages": ["es", "en"],
                "timezone": "America/Mexico_City",
                "date_format": "DD/MM/YYYY",
                "uses_metric": True,
                "tax_rate": 16.00,
                "is_eu_member": False,
                "requires_vat": False,
                "shipping_zone": "NORTH_AMERICA",
                "supports_cod": True,
            },
            # Europe
            {
                "country_code": "GB",
                "country_name": "United Kingdom",
                "default_currency": "GBP",
                "accepted_currencies": ["GBP", "EUR"],
                "default_language": "en",
                "supported_languages": ["en"],
                "timezone": "Europe/London",
                "date_format": "DD/MM/YYYY",
                "uses_metric": True,
                "tax_rate": 20.00,
                "is_eu_member": False,  # Post-Brexit
                "requires_vat": True,
                "shipping_zone": "EUROPE",
                "supports_cod": False,
            },
            {
                "country_code": "DE",
                "country_name": "Germany",
                "default_currency": "EUR",
                "accepted_currencies": ["EUR"],
                "default_language": "de",
                "supported_languages": ["de", "en"],
                "timezone": "Europe/Berlin",
                "date_format": "DD.MM.YYYY",
                "uses_metric": True,
                "tax_rate": 19.00,
                "is_eu_member": True,
                "requires_vat": True,
                "shipping_zone": "EUROPE",
                "supports_cod": False,
            },
            {
                "country_code": "FR",
                "country_name": "France",
                "default_currency": "EUR",
                "accepted_currencies": ["EUR"],
                "default_language": "fr",
                "supported_languages": ["fr", "en"],
                "timezone": "Europe/Paris",
                "date_format": "DD/MM/YYYY",
                "uses_metric": True,
                "tax_rate": 20.00,
                "is_eu_member": True,
                "requires_vat": True,
                "shipping_zone": "EUROPE",
                "supports_cod": False,
            },
            {
                "country_code": "ES",
                "country_name": "Spain",
                "default_currency": "EUR",
                "accepted_currencies": ["EUR"],
                "default_language": "es",
                "supported_languages": ["es", "en"],
                "timezone": "Europe/Madrid",
                "date_format": "DD/MM/YYYY",
                "uses_metric": True,
                "tax_rate": 21.00,
                "is_eu_member": True,
                "requires_vat": True,
                "shipping_zone": "EUROPE",
                "supports_cod": False,
            },
            {
                "country_code": "IT",
                "country_name": "Italy",
                "default_currency": "EUR",
                "accepted_currencies": ["EUR"],
                "default_language": "it",
                "supported_languages": ["it", "en"],
                "timezone": "Europe/Rome",
                "date_format": "DD/MM/YYYY",
                "uses_metric": True,
                "tax_rate": 22.00,
                "is_eu_member": True,
                "requires_vat": True,
                "shipping_zone": "EUROPE",
                "supports_cod": False,
            },
            # Asia-Pacific
            {
                "country_code": "JP",
                "country_name": "Japan",
                "default_currency": "JPY",
                "accepted_currencies": ["JPY"],
                "default_language": "ja",
                "supported_languages": ["ja", "en"],
                "timezone": "Asia/Tokyo",
                "date_format": "YYYY/MM/DD",
                "uses_metric": True,
                "tax_rate": 10.00,
                "is_eu_member": False,
                "requires_vat": False,
                "shipping_zone": "ASIA",
                "supports_cod": True,
            },
            {
                "country_code": "CN",
                "country_name": "China",
                "default_currency": "CNY",
                "accepted_currencies": ["CNY"],
                "default_language": "zh-hans",
                "supported_languages": ["zh-hans", "en"],
                "timezone": "Asia/Shanghai",
                "date_format": "YYYY-MM-DD",
                "uses_metric": True,
                "tax_rate": 13.00,
                "is_eu_member": False,
                "requires_vat": False,
                "shipping_zone": "ASIA",
                "supports_cod": True,
            },
            {
                "country_code": "IN",
                "country_name": "India",
                "default_currency": "INR",
                "accepted_currencies": ["INR", "USD"],
                "default_language": "en",
                "supported_languages": ["en", "hi"],
                "timezone": "Asia/Kolkata",
                "date_format": "DD/MM/YYYY",
                "uses_metric": True,
                "tax_rate": 18.00,
                "is_eu_member": False,
                "requires_vat": False,
                "shipping_zone": "ASIA",
                "supports_cod": True,
            },
            {
                "country_code": "AU",
                "country_name": "Australia",
                "default_currency": "AUD",
                "accepted_currencies": ["AUD"],
                "default_language": "en",
                "supported_languages": ["en"],
                "timezone": "Australia/Sydney",
                "date_format": "DD/MM/YYYY",
                "uses_metric": True,
                "tax_rate": 10.00,
                "is_eu_member": False,
                "requires_vat": False,
                "shipping_zone": "OCEANIA",
                "supports_cod": False,
            },
            # South America
            {
                "country_code": "BR",
                "country_name": "Brazil",
                "default_currency": "BRL",
                "accepted_currencies": ["BRL", "USD"],
                "default_language": "pt",
                "supported_languages": ["pt", "en"],
                "timezone": "America/Sao_Paulo",
                "date_format": "DD/MM/YYYY",
                "uses_metric": True,
                "tax_rate": 17.00,
                "is_eu_member": False,
                "requires_vat": False,
                "shipping_zone": "SOUTH_AMERICA",
                "supports_cod": True,
            },
        ]

        for country_data in countries:
            country_code = country_data["country_code"]
            _, created = CountryMapping.objects.update_or_create(
                country_code=country_code, defaults=country_data
            )
            count += 1

        return count
