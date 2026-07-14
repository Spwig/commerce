"""
Tests for GeoIP Integration
Tests the helper functions that integrate with geoip.CountryMapping
"""

from decimal import Decimal

from django.core.cache import cache
from django.test import TestCase

from geoip.models import CountryMapping
from shipping.integrations import geoip


class GeoIPIntegrationTestCase(TestCase):
    """Test GeoIP integration helper functions"""

    def setUp(self):
        """Create test country mappings"""
        # Clear cache before each test
        cache.clear()

        # Clear any existing country mappings to avoid conflicts
        CountryMapping.objects.all().delete()

        # United States
        self.us_mapping = CountryMapping.objects.create(
            country_code="US",
            country_name="United States",
            default_currency="USD",
            accepted_currencies=["USD", "CAD"],
            default_language="en",
            shipping_zone="domestic",
            tax_rate=Decimal("0.00"),  # US tax varies by state
            is_eu_member=False,
            requires_vat=False,
            uses_metric=False,
            timezone="America/New_York",
            supports_cod=False,
            is_active=True,
        )

        # United Kingdom
        self.gb_mapping = CountryMapping.objects.create(
            country_code="GB",
            country_name="United Kingdom",
            default_currency="GBP",
            accepted_currencies=["GBP", "EUR", "USD"],
            default_language="en",
            shipping_zone="europe",
            tax_rate=Decimal("20.00"),
            is_eu_member=False,  # Post-Brexit
            requires_vat=True,
            uses_metric=True,
            timezone="Europe/London",
            supports_cod=True,
            is_active=True,
        )

        # Singapore
        self.sg_mapping = CountryMapping.objects.create(
            country_code="SG",
            country_name="Singapore",
            default_currency="SGD",
            accepted_currencies=["SGD", "USD"],
            default_language="en",
            shipping_zone="asia-pacific",
            tax_rate=Decimal("7.00"),  # GST
            is_eu_member=False,
            requires_vat=False,
            uses_metric=True,
            timezone="Asia/Singapore",
            supports_cod=False,
            is_active=True,
        )

        # Germany (EU member)
        self.de_mapping = CountryMapping.objects.create(
            country_code="DE",
            country_name="Germany",
            default_currency="EUR",
            accepted_currencies=["EUR"],
            default_language="de",
            shipping_zone="europe",
            tax_rate=Decimal("19.00"),
            is_eu_member=True,
            requires_vat=True,
            uses_metric=True,
            timezone="Europe/Berlin",
            supports_cod=True,
            is_active=True,
        )

    def tearDown(self):
        """Clean up cache after each test"""
        cache.clear()

    def test_get_country_mapping(self):
        """Test retrieving country mapping"""
        # Test existing country
        mapping = geoip.get_country_mapping("US")
        self.assertIsNotNone(mapping)
        self.assertEqual(mapping.country_code, "US")
        self.assertEqual(mapping.country_name, "United States")

        # Test lowercase input
        mapping = geoip.get_country_mapping("gb")
        self.assertIsNotNone(mapping)
        self.assertEqual(mapping.country_code, "GB")

        # Test non-existent country
        mapping = geoip.get_country_mapping("XX")
        self.assertIsNone(mapping)

        # Test empty input
        mapping = geoip.get_country_mapping("")
        self.assertIsNone(mapping)

    def test_get_country_mapping_caching(self):
        """Test that country mappings are cached"""
        # First call should hit database
        mapping1 = geoip.get_country_mapping("US")
        self.assertIsNotNone(mapping1)

        # Second call should use cache
        mapping2 = geoip.get_country_mapping("US")
        self.assertEqual(mapping1.id, mapping2.id)

        # Verify cache was used
        cache_key = "country_mapping:US"
        cached_mapping = cache.get(cache_key)
        self.assertIsNotNone(cached_mapping)
        self.assertEqual(cached_mapping.country_code, "US")

    def test_is_domestic_shipment(self):
        """Test domestic shipment detection"""
        # Same country - domestic
        self.assertTrue(geoip.is_domestic_shipment("US", "US"))
        self.assertTrue(geoip.is_domestic_shipment("GB", "GB"))

        # Different countries - international
        self.assertFalse(geoip.is_domestic_shipment("US", "CA"))
        self.assertFalse(geoip.is_domestic_shipment("US", "GB"))

        # Case insensitive
        self.assertTrue(geoip.is_domestic_shipment("us", "US"))
        self.assertTrue(geoip.is_domestic_shipment("Us", "uS"))

        # Empty inputs
        self.assertFalse(geoip.is_domestic_shipment("", "US"))
        self.assertFalse(geoip.is_domestic_shipment("US", ""))
        self.assertFalse(geoip.is_domestic_shipment("", ""))

    def test_get_shipping_zone(self):
        """Test shipping zone determination"""
        # Domestic shipment
        zone = geoip.get_shipping_zone("US", "US")
        self.assertEqual(zone, "domestic")

        # International with custom zone
        zone = geoip.get_shipping_zone("GB", "US")
        self.assertEqual(zone, "europe")

        zone = geoip.get_shipping_zone("SG", "US")
        self.assertEqual(zone, "asia-pacific")

        # International without custom zone (unknown country)
        zone = geoip.get_shipping_zone("XX", "US")
        self.assertEqual(zone, "international")

        # Empty country code
        zone = geoip.get_shipping_zone("", "US")
        self.assertEqual(zone, "international")

    def test_get_country_currency(self):
        """Test currency code retrieval"""
        # Known countries
        self.assertEqual(geoip.get_country_currency("US"), "USD")
        self.assertEqual(geoip.get_country_currency("GB"), "GBP")
        self.assertEqual(geoip.get_country_currency("SG"), "SGD")
        self.assertEqual(geoip.get_country_currency("DE"), "EUR")

        # Case insensitive
        self.assertEqual(geoip.get_country_currency("gb"), "GBP")

        # Unknown country - fallback to USD
        self.assertEqual(geoip.get_country_currency("XX"), "USD")

    def test_get_country_name(self):
        """Test country name retrieval"""
        # Known countries
        self.assertEqual(geoip.get_country_name("US"), "United States")
        self.assertEqual(geoip.get_country_name("GB"), "United Kingdom")
        self.assertEqual(geoip.get_country_name("SG"), "Singapore")
        self.assertEqual(geoip.get_country_name("DE"), "Germany")

        # Case insensitive
        self.assertEqual(geoip.get_country_name("gb"), "United Kingdom")

        # Unknown country - fallback to code
        self.assertEqual(geoip.get_country_name("XX"), "XX")

        # Empty input
        self.assertEqual(geoip.get_country_name(""), "")

    def test_get_country_info(self):
        """Test comprehensive country info retrieval"""
        # Test US
        info = geoip.get_country_info("US")
        self.assertEqual(info["country_code"], "US")
        self.assertEqual(info["country_name"], "United States")
        self.assertEqual(info["currency"], "USD")
        self.assertEqual(info["shipping_zone"], "domestic")
        self.assertEqual(info["tax_rate"], 0.0)
        self.assertFalse(info["is_eu_member"])
        self.assertFalse(info["requires_vat"])
        self.assertFalse(info["uses_metric"])
        self.assertEqual(info["timezone"], "America/New_York")

        # Test GB
        info = geoip.get_country_info("GB")
        self.assertEqual(info["country_code"], "GB")
        self.assertEqual(info["currency"], "GBP")
        self.assertEqual(info["shipping_zone"], "europe")
        self.assertEqual(info["tax_rate"], 20.0)
        self.assertTrue(info["requires_vat"])
        self.assertTrue(info["uses_metric"])

        # Test unknown country - fallback values
        info = geoip.get_country_info("XX")
        self.assertEqual(info["country_code"], "XX")
        self.assertEqual(info["country_name"], "XX")
        self.assertEqual(info["currency"], "USD")
        self.assertEqual(info["shipping_zone"], "international")
        self.assertEqual(info["tax_rate"], 0.0)

    def test_get_accepted_currencies(self):
        """Test accepted currencies retrieval"""
        # US accepts USD and CAD
        currencies = geoip.get_accepted_currencies("US")
        self.assertIn("USD", currencies)
        self.assertIn("CAD", currencies)
        # Default currency should be first
        self.assertEqual(currencies[0], "USD")

        # GB accepts multiple currencies
        currencies = geoip.get_accepted_currencies("GB")
        self.assertIn("GBP", currencies)
        self.assertIn("EUR", currencies)
        self.assertIn("USD", currencies)
        self.assertEqual(currencies[0], "GBP")

        # Unknown country - fallback to USD
        currencies = geoip.get_accepted_currencies("XX")
        self.assertEqual(currencies, ["USD"])

    def test_is_eu_country(self):
        """Test EU membership detection"""
        # EU member
        self.assertTrue(geoip.is_eu_country("DE"))

        # Non-EU members
        self.assertFalse(geoip.is_eu_country("US"))
        self.assertFalse(geoip.is_eu_country("GB"))  # Post-Brexit
        self.assertFalse(geoip.is_eu_country("SG"))

        # Unknown country
        self.assertFalse(geoip.is_eu_country("XX"))

    def test_requires_vat_number(self):
        """Test VAT requirement detection"""
        # Countries requiring VAT
        self.assertTrue(geoip.requires_vat_number("GB"))
        self.assertTrue(geoip.requires_vat_number("DE"))

        # Countries not requiring VAT
        self.assertFalse(geoip.requires_vat_number("US"))
        self.assertFalse(geoip.requires_vat_number("SG"))

        # Unknown country
        self.assertFalse(geoip.requires_vat_number("XX"))

    def test_get_tax_rate(self):
        """Test tax rate retrieval"""
        # Various tax rates
        self.assertEqual(geoip.get_tax_rate("US"), 0.0)
        self.assertEqual(geoip.get_tax_rate("GB"), 20.0)
        self.assertEqual(geoip.get_tax_rate("SG"), 7.0)
        self.assertEqual(geoip.get_tax_rate("DE"), 19.0)

        # Unknown country
        self.assertEqual(geoip.get_tax_rate("XX"), 0.0)

    def test_clear_country_cache(self):
        """Test cache clearing"""
        # Load US into cache
        mapping = geoip.get_country_mapping("US")
        self.assertIsNotNone(mapping)

        # Verify it's cached
        cache_key = "country_mapping:US"
        self.assertIsNotNone(cache.get(cache_key))

        # Clear specific country
        geoip.clear_country_cache("US")
        self.assertIsNone(cache.get(cache_key))

        # Load multiple countries
        geoip.get_country_mapping("US")
        geoip.get_country_mapping("GB")
        geoip.get_country_mapping("SG")

        # Clear all
        geoip.clear_country_cache()
        self.assertIsNone(cache.get("country_mapping:US"))
        self.assertIsNone(cache.get("country_mapping:GB"))
        self.assertIsNone(cache.get("country_mapping:SG"))

    def test_inactive_country_mapping(self):
        """Test that inactive country mappings are not returned"""
        # Create inactive mapping
        CountryMapping.objects.create(
            country_code="CA",
            country_name="Canada",
            default_currency="CAD",
            is_active=False,
        )

        # Should not be retrieved
        mapping = geoip.get_country_mapping("CA")
        self.assertIsNone(mapping)

    def test_supports_cod(self):
        """Test Cash on Delivery support via country info"""
        # GB supports COD
        info = geoip.get_country_info("GB")
        self.assertTrue(info["supports_cod"])

        # US doesn't support COD
        info = geoip.get_country_info("US")
        self.assertFalse(info["supports_cod"])
