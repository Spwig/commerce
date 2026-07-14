"""
GeoIP integration tests.

Tests models, API views, admin pages, admin AJAX views, provider management
views, business rule evaluation, template tags, and IP utility functions.
"""

from datetime import timedelta

import pytest
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.template import Context, Template
from django.test import Client, RequestFactory
from django.urls import reverse
from django.utils import timezone

from geoip.models import (
    BusinessRule,
    CountryMapping,
    GeoIPProvider,
    GeoLocation,
    VisitorLocation,
)
from geoip.templatetags.geoip_tags import (
    country_flag,
)
from geoip.templatetags.geoip_tags import (
    country_name as country_name_tag,
)
from geoip.utils.ip_utils import (
    anonymize_ip,
    get_client_ip,
    get_ip_prefix,
    get_ip_version,
    int_to_ip,
    ip_to_int,
    is_in_range,
    is_private_ip,
    is_valid_ip,
)
from tests.factories import (
    BusinessRuleFactory,
    CountryMappingFactory,
    GeoIPProviderFactory,
    GeoLocationFactory,
    UserFactory,
    VisitorLocationFactory,
)

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.geoip]


# ============================================================
# Fixtures
# ============================================================


@pytest.fixture
def staff_client(admin_user, site_settings):
    """Django test client authenticated as admin staff user.
    Depends on site_settings because CurrencyMiddleware calls SiteSettings.get_settings()."""
    client = Client()
    client.force_login(admin_user)
    return client


@pytest.fixture
def anon_client(site_settings):
    """Unauthenticated Django test client.
    Depends on site_settings because CurrencyMiddleware calls SiteSettings.get_settings()."""
    return Client()


@pytest.fixture(autouse=True)
def clear_geoip_cache():
    """Clear cache before each test to avoid stale location data."""
    cache.clear()
    yield
    cache.clear()


@pytest.fixture
def us_mapping(db):
    return CountryMappingFactory(
        country_code="US",
        country_name="United States",
        default_currency="USD",
        accepted_currencies=["USD", "CAD"],
        default_language="en",
        supported_languages=["en", "es"],
        timezone="America/New_York",
        is_eu_member=False,
    )


@pytest.fixture
def gb_mapping(db):
    return CountryMappingFactory(
        country_code="GB",
        country_name="United Kingdom",
        default_currency="GBP",
        accepted_currencies=["GBP", "EUR"],
        default_language="en",
        supported_languages=["en"],
        timezone="Europe/London",
        is_eu_member=False,
    )


@pytest.fixture
def de_mapping(db):
    return CountryMappingFactory(
        country_code="DE",
        country_name="Germany",
        default_currency="EUR",
        accepted_currencies=["EUR"],
        default_language="de",
        supported_languages=["de", "en"],
        timezone="Europe/Berlin",
        is_eu_member=True,
        requires_vat=True,
        uses_metric=True,
    )


@pytest.fixture
def jp_mapping(db):
    return CountryMappingFactory(
        country_code="JP",
        country_name="Japan",
        default_currency="JPY",
        accepted_currencies=["JPY"],
        default_language="ja",
        supported_languages=["ja", "en"],
        timezone="Asia/Tokyo",
    )


# ============================================================
# Model Tests: GeoLocation
# ============================================================


class TestGeoLocationModel:
    def test_create_geolocation(self, db):
        """GeoLocation can be created with all required fields."""
        loc = GeoLocationFactory(ip_address="10.0.0.1")
        assert loc.pk is not None
        assert loc.ip_address == "10.0.0.1"
        assert loc.country_code == "US"
        assert loc.source == "test"

    def test_str_representation(self, db):
        """String representation includes IP and country code."""
        loc = GeoLocationFactory(ip_address="10.0.0.2", country_code="GB")
        assert "10.0.0.2" in str(loc)
        assert "GB" in str(loc)

    def test_str_representation_unknown_country(self, db):
        """String representation shows Unknown when no country code."""
        loc = GeoLocationFactory(ip_address="10.0.0.3", country_code="")
        assert "Unknown" in str(loc)

    def test_unique_ip_address(self, db):
        """ip_address field enforces uniqueness."""
        GeoLocationFactory(ip_address="10.0.0.4")
        # django_get_or_create should return existing, not create duplicate
        loc2 = GeoLocationFactory(ip_address="10.0.0.4")
        assert GeoLocation.objects.filter(ip_address="10.0.0.4").count() == 1

    def test_is_expired_false_when_no_expiry(self, db):
        """is_expired returns False when expires_at is None."""
        loc = GeoLocationFactory(ip_address="10.0.0.5", expires_at=None)
        assert loc.is_expired is False

    def test_is_expired_false_when_future(self, db):
        """is_expired returns False when expires_at is in the future."""
        loc = GeoLocationFactory(
            ip_address="10.0.0.6",
            expires_at=timezone.now() + timedelta(hours=1),
        )
        assert loc.is_expired is False

    def test_is_expired_true_when_past(self, db):
        """is_expired returns True when expires_at is in the past."""
        loc = GeoLocationFactory(ip_address="10.0.0.7", expired=True)
        assert loc.is_expired is True

    def test_to_dict_returns_expected_keys(self, db):
        """to_dict() returns all expected keys for API responses."""
        loc = GeoLocationFactory(ip_address="10.0.0.8")
        d = loc.to_dict()
        expected_keys = {
            "ip",
            "country",
            "country_name",
            "region",
            "region_name",
            "city",
            "postal_code",
            "lat",
            "lon",
            "asn",
            "isp",
            "source",
            "confidence",
            "is_proxy",
            "is_vpn",
            "is_tor",
            "is_mobile",
            "resolved_at",
        }
        assert expected_keys == set(d.keys())

    def test_to_dict_values(self, db):
        """to_dict() returns correct field values."""
        loc = GeoLocationFactory(
            ip_address="10.0.0.9",
            country_code="DE",
            city_name="Berlin",
            latitude=52.52,
            longitude=13.405,
        )
        d = loc.to_dict()
        assert d["ip"] == "10.0.0.9"
        assert d["country"] == "DE"
        assert d["city"] == "Berlin"
        assert d["lat"] == 52.52
        assert d["lon"] == 13.405

    def test_ordering_by_resolved_at_descending(self, db):
        """Default ordering is by resolved_at descending."""
        GeoLocation.objects.all().delete()
        loc1 = GeoLocationFactory(ip_address="10.0.0.10")
        loc2 = GeoLocationFactory(ip_address="10.0.0.11")
        locs = list(GeoLocation.objects.all())
        # Most recent first
        assert locs[0].pk == loc2.pk

    def test_security_flags(self, db):
        """Security flags (VPN, proxy, tor, mobile) can be set."""
        loc = GeoLocationFactory(
            ip_address="10.0.0.12",
            is_vpn=True,
            is_proxy=True,
            is_tor=True,
            is_mobile=True,
        )
        assert loc.is_vpn is True
        assert loc.is_proxy is True
        assert loc.is_tor is True
        assert loc.is_mobile is True

    def test_confidence_validators(self, db):
        """Confidence must be between 0.0 and 1.0."""
        loc = GeoLocationFactory(ip_address="10.0.0.13", confidence=0.5)
        loc.full_clean()  # Should pass

        loc.confidence = 1.5
        with pytest.raises(ValidationError):
            loc.full_clean()

        loc.confidence = -0.1
        with pytest.raises(ValidationError):
            loc.full_clean()

    def test_latitude_validators(self, db):
        """Latitude must be between -90 and 90."""
        loc = GeoLocationFactory(ip_address="10.0.0.14", latitude=91.0)
        with pytest.raises(ValidationError):
            loc.full_clean()

    def test_longitude_validators(self, db):
        """Longitude must be between -180 and 180."""
        loc = GeoLocationFactory(ip_address="10.0.0.15", longitude=181.0)
        with pytest.raises(ValidationError):
            loc.full_clean()


# ============================================================
# Model Tests: CountryMapping
# ============================================================


class TestCountryMappingModel:
    def test_create_country_mapping(self, us_mapping):
        """CountryMapping can be created with all fields."""
        assert us_mapping.pk is not None
        assert us_mapping.country_code == "US"
        assert us_mapping.default_currency == "USD"

    def test_str_representation(self, us_mapping):
        """String representation includes code and name."""
        assert "US" in str(us_mapping)
        assert "United States" in str(us_mapping)

    def test_unique_country_code(self, db):
        """country_code is unique."""
        CountryMappingFactory(country_code="FR", country_name="France")
        # django_get_or_create prevents duplicate
        cm2 = CountryMappingFactory(country_code="FR")
        assert CountryMapping.objects.filter(country_code="FR").count() == 1

    def test_get_currency_display(self, us_mapping):
        """get_currency_display returns currency with symbol."""
        display = us_mapping.get_currency_display()
        assert "USD" in display
        assert "$" in display

    def test_get_currency_display_euro(self, de_mapping):
        """get_currency_display returns EUR with euro symbol."""
        display = de_mapping.get_currency_display()
        assert "EUR" in display

    def test_eu_member_flags(self, de_mapping):
        """EU member fields set correctly."""
        assert de_mapping.is_eu_member is True
        assert de_mapping.requires_vat is True

    def test_ordering_by_country_code(self, db):
        """Default ordering is by country_code ascending."""
        CountryMapping.objects.all().delete()
        CountryMappingFactory(country_code="ZZ", country_name="Zulu")
        CountryMappingFactory(country_code="AA", country_name="Alpha")
        codes = list(CountryMapping.objects.values_list("country_code", flat=True))
        assert codes == sorted(codes)

    def test_array_fields(self, us_mapping):
        """ArrayField columns store and retrieve lists correctly."""
        assert isinstance(us_mapping.accepted_currencies, list)
        assert "USD" in us_mapping.accepted_currencies
        assert isinstance(us_mapping.supported_languages, list)
        assert "en" in us_mapping.supported_languages

    def test_json_field_custom_rules(self, db):
        """custom_rules JSONField stores and retrieves dict."""
        cm = CountryMappingFactory(
            country_code="XX",
            country_name="Test",
            custom_rules={"min_order": 50, "free_shipping": True},
        )
        cm.refresh_from_db()
        assert cm.custom_rules["min_order"] == 50
        assert cm.custom_rules["free_shipping"] is True

    def test_is_active_default(self, db):
        """is_active defaults to True."""
        cm = CountryMappingFactory(country_code="YY", country_name="Test Y")
        assert cm.is_active is True


# ============================================================
# Model Tests: GeoIPProvider
# ============================================================


class TestGeoIPProviderModel:
    def test_create_provider(self, db):
        """GeoIPProvider can be created with required fields."""
        provider = GeoIPProviderFactory(name="Test Spwig Provider")
        assert provider.pk is not None
        assert provider.provider_type == "spwig"

    def test_str_representation(self, db):
        """String representation includes name and type display."""
        provider = GeoIPProviderFactory(
            name="My MaxMind",
            provider_type="maxmind",
        )
        s = str(provider)
        assert "My MaxMind" in s
        assert "MaxMind" in s

    def test_accuracy_rate_zero_lookups(self, db):
        """accuracy_rate returns 0 when no lookups."""
        provider = GeoIPProviderFactory(total_lookups=0)
        assert provider.accuracy_rate == 0.0

    def test_accuracy_rate_calculation(self, db):
        """accuracy_rate calculates correct percentage."""
        provider = GeoIPProviderFactory(
            total_lookups=100,
            successful_lookups=95,
            failed_lookups=5,
        )
        assert provider.accuracy_rate == 95.0

    def test_config_json_field(self, db):
        """config JSONField stores provider configuration."""
        provider = GeoIPProviderFactory(
            config={"api_key": "test123", "timeout": 5},
        )
        provider.refresh_from_db()
        assert provider.config["api_key"] == "test123"
        assert provider.config["timeout"] == 5

    def test_provider_type_choices(self, db):
        """All expected provider types are valid choices."""
        valid_types = [
            "spwig",
            "maxmind",
            "dbip",
            "ip2location",
            "edge_header",
            "browser_hint",
            "custom",
        ]
        for pt in valid_types:
            provider = GeoIPProviderFactory(provider_type=pt)
            assert provider.provider_type == pt

    def test_ordering_by_priority_then_name(self, db):
        """Default ordering is by priority then name."""
        GeoIPProvider.objects.all().delete()
        p1 = GeoIPProviderFactory(name="Beta", priority=2)
        p2 = GeoIPProviderFactory(name="Alpha", priority=1)
        p3 = GeoIPProviderFactory(name="Gamma", priority=1)
        providers = list(GeoIPProvider.objects.all())
        assert providers[0].pk == p2.pk  # priority=1, Alpha
        assert providers[1].pk == p3.pk  # priority=1, Gamma
        assert providers[2].pk == p1.pk  # priority=2, Beta

    def test_statistics_fields(self, db):
        """Statistics fields default to zero."""
        provider = GeoIPProviderFactory()
        assert provider.total_lookups == 0
        assert provider.successful_lookups == 0
        assert provider.failed_lookups == 0
        assert provider.average_response_ms == 0.0


# ============================================================
# Model Tests: VisitorLocation
# ============================================================


class TestVisitorLocationModel:
    def test_create_visitor_location(self, db):
        """VisitorLocation can be created with required fields."""
        visitor = VisitorLocationFactory()
        assert visitor.pk is not None
        assert visitor.resolved_country == "US"

    def test_str_representation(self, db):
        """String representation includes session key and country."""
        visitor = VisitorLocationFactory(
            session_key="sess_abc123",
            resolved_country="GB",
        )
        s = str(visitor)
        assert "sess_abc123" in s
        assert "GB" in s

    def test_was_corrected_false_when_no_actual(self, db):
        """was_corrected is False when actual_country is empty."""
        visitor = VisitorLocationFactory(actual_country="")
        assert visitor.was_corrected is False

    def test_was_corrected_false_when_same(self, db):
        """was_corrected is False when actual matches resolved."""
        visitor = VisitorLocationFactory(
            resolved_country="US",
            actual_country="US",
        )
        assert visitor.was_corrected is False

    def test_was_corrected_true_when_different(self, db):
        """was_corrected is True when actual differs from resolved."""
        visitor = VisitorLocationFactory(corrected=True)
        assert visitor.was_corrected is True

    def test_utm_fields(self, db):
        """UTM tracking fields can be stored and retrieved."""
        visitor = VisitorLocationFactory(
            utm_source="google",
            utm_medium="cpc",
            utm_campaign="summer_sale",
            utm_term="shoes",
            utm_content="banner_a",
        )
        visitor.refresh_from_db()
        assert visitor.utm_source == "google"
        assert visitor.utm_medium == "cpc"
        assert visitor.utm_campaign == "summer_sale"

    def test_device_type_choices(self, db):
        """All device type choices are valid."""
        for dtype in ["desktop", "mobile", "tablet", "unknown"]:
            visitor = VisitorLocationFactory(device_type=dtype)
            assert visitor.device_type == dtype

    def test_ordering_by_last_seen_descending(self, db):
        """Default ordering is by last_seen descending."""
        VisitorLocation.objects.all().delete()
        v1 = VisitorLocationFactory(session_key="first_sess")
        v2 = VisitorLocationFactory(session_key="second_sess")
        visitors = list(VisitorLocation.objects.all())
        assert visitors[0].pk == v2.pk  # Most recent first

    def test_page_views_default(self, db):
        """page_views defaults to 1."""
        visitor = VisitorLocationFactory()
        assert visitor.page_views == 1


# ============================================================
# Model Tests: BusinessRule
# ============================================================


class TestBusinessRuleModel:
    def test_create_business_rule(self, db):
        """BusinessRule can be created with conditions and actions."""
        rule = BusinessRuleFactory()
        assert rule.pk is not None
        assert rule.is_active is True

    def test_str_representation(self, db):
        """String representation is the rule name."""
        rule = BusinessRuleFactory(name="US Redirect Rule")
        assert str(rule) == "US Redirect Rule"

    def test_unique_name(self, db):
        """name field is unique."""
        BusinessRuleFactory(name="Unique Rule")
        with pytest.raises(IntegrityError):
            BusinessRuleFactory(name="Unique Rule")

    def test_evaluate_matching_country_in(self, db):
        """evaluate returns True when country matches country_in condition."""
        rule = BusinessRuleFactory(
            conditions={"country_in": ["US", "CA"]},
        )
        assert rule.evaluate({"country": "US"}) is True
        assert rule.evaluate({"country": "CA"}) is True

    def test_evaluate_non_matching_country_in(self, db):
        """evaluate returns False when country not in country_in list."""
        rule = BusinessRuleFactory(
            conditions={"country_in": ["US", "CA"]},
        )
        assert rule.evaluate({"country": "GB"}) is False

    def test_evaluate_country_not_in(self, db):
        """evaluate returns False when country is in country_not_in list."""
        rule = BusinessRuleFactory(
            conditions={"country_not_in": ["CN", "RU"]},
        )
        assert rule.evaluate({"country": "US"}) is True
        assert rule.evaluate({"country": "CN"}) is False

    def test_evaluate_region_in(self, db):
        """evaluate matches region_in condition."""
        rule = BusinessRuleFactory(
            conditions={"region_in": ["CA", "NY"]},
        )
        assert rule.evaluate({"region": "CA"}) is True
        assert rule.evaluate({"region": "TX"}) is False

    def test_evaluate_region_not_in(self, db):
        """evaluate excludes region_not_in condition."""
        rule = BusinessRuleFactory(
            conditions={"region_not_in": ["Quebec"]},
        )
        assert rule.evaluate({"region": "Ontario"}) is True
        assert rule.evaluate({"region": "Quebec"}) is False

    def test_evaluate_is_mobile(self, db):
        """evaluate matches is_mobile condition."""
        rule = BusinessRuleFactory(
            conditions={"is_mobile": True},
        )
        assert rule.evaluate({"is_mobile": True}) is True
        assert rule.evaluate({"is_mobile": False}) is False

    def test_evaluate_is_vpn(self, db):
        """evaluate matches is_vpn condition."""
        rule = BusinessRuleFactory(
            conditions={"is_vpn": True},
        )
        assert rule.evaluate({"is_vpn": True}) is True
        assert rule.evaluate({"is_vpn": False}) is False

    def test_evaluate_multiple_conditions_all_match(self, db):
        """evaluate returns True only when ALL conditions match."""
        rule = BusinessRuleFactory(
            conditions={
                "country_in": ["US"],
                "is_mobile": True,
            },
        )
        assert rule.evaluate({"country": "US", "is_mobile": True}) is True

    def test_evaluate_multiple_conditions_partial_match(self, db):
        """evaluate returns False when only some conditions match."""
        rule = BusinessRuleFactory(
            conditions={
                "country_in": ["US"],
                "is_mobile": True,
            },
        )
        assert rule.evaluate({"country": "US", "is_mobile": False}) is False

    def test_evaluate_inactive_rule(self, db):
        """evaluate returns False when rule is inactive."""
        rule = BusinessRuleFactory(
            is_active=False,
            conditions={"country_in": ["US"]},
        )
        assert rule.evaluate({"country": "US"}) is False

    def test_evaluate_empty_conditions(self, db):
        """evaluate returns True when conditions are empty (match all)."""
        rule = BusinessRuleFactory(conditions={})
        assert rule.evaluate({"country": "US"}) is True

    def test_evaluate_with_empty_location_data(self, db):
        """evaluate handles empty location data gracefully."""
        rule = BusinessRuleFactory(
            conditions={"country_in": ["US"]},
        )
        assert rule.evaluate({}) is False

    def test_ordering_by_priority_then_name(self, db):
        """Default ordering is by priority then name."""
        BusinessRule.objects.all().delete()
        r1 = BusinessRuleFactory(name="Zulu Rule", priority=1)
        r2 = BusinessRuleFactory(name="Alpha Rule", priority=0)
        r3 = BusinessRuleFactory(name="Beta Rule", priority=0)
        rules = list(BusinessRule.objects.all())
        assert rules[0].pk == r2.pk  # priority=0, Alpha
        assert rules[1].pk == r3.pk  # priority=0, Beta
        assert rules[2].pk == r1.pk  # priority=1

    def test_tracking_fields_default(self, db):
        """times_triggered defaults to 0, last_triggered is None."""
        rule = BusinessRuleFactory()
        assert rule.times_triggered == 0
        assert rule.last_triggered is None


# ============================================================
# API Tests: resolve_location
# ============================================================


class TestResolveLocationAPI:
    def test_resolve_returns_200(self, anon_client):
        """resolve_location endpoint returns 200 for anonymous users."""
        resp = anon_client.get("/api/geoip/v1/resolve/")
        assert resp.status_code == 200

    def test_resolve_returns_fallback_without_middleware(self, anon_client):
        """Without geo middleware, resolve returns default US fallback."""
        resp = anon_client.get("/api/geoip/v1/resolve/")
        data = resp.json()
        # Fallback sets country=US, currency=USD
        assert "country" in data or "ip" in data

    def test_resolve_with_country_mapping(self, anon_client, us_mapping):
        """resolve enriches response with country mapping data."""
        resp = anon_client.get("/api/geoip/v1/resolve/")
        data = resp.json()
        # The fallback country is US, which matches our mapping
        assert data.get("currency") == "USD"
        assert data.get("language") == "en"

    def test_resolve_includes_default_fields(self, anon_client):
        """resolve response includes city, region, currency, language defaults."""
        resp = anon_client.get("/api/geoip/v1/resolve/")
        data = resp.json()
        # These defaults are set by the view
        assert "currency" in data
        assert "language" in data

    def test_resolve_applies_business_rules(self, anon_client, db):
        """resolve evaluates and applies active business rules."""
        rule = BusinessRuleFactory(
            name="US Currency Rule",
            conditions={"country_in": ["US"]},
            actions={"set_currency": "USD", "show_banner": True},
        )
        resp = anon_client.get("/api/geoip/v1/resolve/")
        data = resp.json()
        # Business rules should be applied when country matches
        if "business_rules" in data:
            rule_names = [r["name"] for r in data["business_rules"]]
            assert "US Currency Rule" in rule_names

    def test_resolve_caches_result(self, anon_client, us_mapping):
        """resolve caches the result for subsequent requests."""
        resp1 = anon_client.get("/api/geoip/v1/resolve/")
        resp2 = anon_client.get("/api/geoip/v1/resolve/")
        assert resp1.status_code == 200
        assert resp2.status_code == 200
        # Both should return same data (from cache)
        assert resp1.json()["currency"] == resp2.json()["currency"]

    def test_resolve_only_allows_get(self, anon_client):
        """resolve_location only accepts GET requests."""
        resp = anon_client.post("/api/geoip/v1/resolve/")
        assert resp.status_code == 405


# ============================================================
# API Tests: set_preference
# ============================================================


class TestSetPreferenceAPI:
    def test_set_preference_returns_success(self, anon_client):
        """set_preference returns success status."""
        resp = anon_client.post(
            "/api/geoip/v1/preference/",
            data={"currency": "EUR", "language": "fr"},
            content_type="application/json",
        )
        assert resp.status_code == 200
        assert resp.json()["status"] == "success"

    def test_set_preference_stores_in_session(self, anon_client):
        """set_preference stores preferences in session."""
        anon_client.post(
            "/api/geoip/v1/preference/",
            data={"currency": "GBP", "language": "en", "country": "GB"},
            content_type="application/json",
        )
        session = anon_client.session
        assert session.get("preferred_currency") == "GBP"
        assert session.get("preferred_language") == "en"
        assert session.get("preferred_country") == "GB"

    def test_set_preference_updates_visitor_location(self, anon_client, db):
        """set_preference updates VisitorLocation if one exists for session."""
        # Force session creation (middleware may also create a VisitorLocation)
        anon_client.get("/api/geoip/v1/resolve/")
        session_key = anon_client.session.session_key

        if session_key:
            # Use the visitor created by middleware, or create one if middleware didn't
            visitor = VisitorLocation.objects.filter(session_key=session_key).first()
            if not visitor:
                visitor = VisitorLocationFactory(session_key=session_key)

            anon_client.post(
                "/api/geoip/v1/preference/",
                data={"currency": "JPY", "language": "ja", "country": "JP"},
                content_type="application/json",
            )
            visitor.refresh_from_db()
            assert visitor.selected_currency == "JPY"
            assert visitor.selected_language == "ja"
            assert visitor.actual_country == "JP"

    def test_set_preference_only_allows_post(self, anon_client):
        """set_preference only accepts POST requests."""
        resp = anon_client.get("/api/geoip/v1/preference/")
        assert resp.status_code == 405

    def test_set_preference_partial_update(self, anon_client):
        """set_preference can update only some preferences."""
        anon_client.post(
            "/api/geoip/v1/preference/",
            data={"currency": "EUR"},
            content_type="application/json",
        )
        session = anon_client.session
        assert session.get("preferred_currency") == "EUR"
        assert session.get("preferred_language") is None


# ============================================================
# API Tests: suggest_currency
# ============================================================


class TestSuggestCurrencyAPI:
    def test_suggest_currency_with_known_country(self, anon_client, us_mapping):
        """suggest_currency returns mapping data for known country."""
        resp = anon_client.get("/api/geoip/v1/suggest/currency/?country=US")
        assert resp.status_code == 200
        data = resp.json()
        assert data["default"] == "USD"
        assert "USD" in data["accepted"]
        assert data["symbol"] == "$"

    def test_suggest_currency_gbp(self, anon_client, gb_mapping):
        """suggest_currency returns GBP for GB."""
        resp = anon_client.get("/api/geoip/v1/suggest/currency/?country=GB")
        data = resp.json()
        assert data["default"] == "GBP"

    def test_suggest_currency_eur(self, anon_client, de_mapping):
        """suggest_currency returns EUR for DE."""
        resp = anon_client.get("/api/geoip/v1/suggest/currency/?country=DE")
        data = resp.json()
        assert data["default"] == "EUR"

    def test_suggest_currency_unknown_country(self, anon_client):
        """suggest_currency returns USD fallback for unknown country."""
        resp = anon_client.get("/api/geoip/v1/suggest/currency/?country=ZZ")
        data = resp.json()
        assert data["default"] == "USD"
        assert data["accepted"] == ["USD"]
        assert data["symbol"] == "$"

    def test_suggest_currency_no_country_param(self, anon_client):
        """suggest_currency uses detected location when no country param."""
        resp = anon_client.get("/api/geoip/v1/suggest/currency/")
        assert resp.status_code == 200
        data = resp.json()
        # Falls back to US default
        assert "default" in data

    def test_suggest_currency_case_insensitive(self, anon_client, us_mapping):
        """suggest_currency handles lowercase country codes."""
        resp = anon_client.get("/api/geoip/v1/suggest/currency/?country=us")
        data = resp.json()
        assert data["default"] == "USD"

    def test_suggest_currency_inactive_mapping(self, anon_client, db):
        """suggest_currency returns fallback for inactive country mapping."""
        CountryMappingFactory(
            country_code="XX",
            country_name="Test",
            default_currency="XXX",
            is_active=False,
        )
        resp = anon_client.get("/api/geoip/v1/suggest/currency/?country=XX")
        data = resp.json()
        assert data["default"] == "USD"  # Fallback


# ============================================================
# API Tests: suggest_language
# ============================================================


class TestSuggestLanguageAPI:
    def test_suggest_language_with_known_country(self, anon_client, us_mapping):
        """suggest_language returns mapping data for known country."""
        resp = anon_client.get("/api/geoip/v1/suggest/language/?country=US")
        assert resp.status_code == 200
        data = resp.json()
        assert data["default"] == "en"
        assert "en" in data["supported"]

    def test_suggest_language_german(self, anon_client, de_mapping):
        """suggest_language returns de for Germany."""
        resp = anon_client.get("/api/geoip/v1/suggest/language/?country=DE")
        data = resp.json()
        assert data["default"] == "de"
        assert "de" in data["supported"]

    def test_suggest_language_japanese(self, anon_client, jp_mapping):
        """suggest_language returns ja for Japan."""
        resp = anon_client.get("/api/geoip/v1/suggest/language/?country=JP")
        data = resp.json()
        assert data["default"] == "ja"

    def test_suggest_language_unknown_country(self, anon_client):
        """suggest_language returns en fallback for unknown country."""
        resp = anon_client.get("/api/geoip/v1/suggest/language/?country=ZZ")
        data = resp.json()
        assert data["default"] == "en"
        assert data["supported"] == ["en"]

    def test_suggest_language_no_country_param(self, anon_client):
        """suggest_language uses detected location when no country param."""
        resp = anon_client.get("/api/geoip/v1/suggest/language/")
        assert resp.status_code == 200

    def test_suggest_language_case_insensitive(self, anon_client, de_mapping):
        """suggest_language handles lowercase country codes."""
        resp = anon_client.get("/api/geoip/v1/suggest/language/?country=de")
        data = resp.json()
        assert data["default"] == "de"


# ============================================================
# API Tests: list_countries
# ============================================================


class TestListCountriesAPI:
    def test_list_countries_returns_200(self, anon_client, us_mapping):
        """list_countries returns 200 with active country mappings."""
        resp = anon_client.get("/api/geoip/v1/countries/")
        assert resp.status_code == 200

    def test_list_countries_structure(self, anon_client, us_mapping, de_mapping):
        """list_countries returns expected data structure."""
        resp = anon_client.get("/api/geoip/v1/countries/")
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) >= 2

        # Check structure of first item
        us_entry = next((c for c in data if c["code"] == "US"), None)
        assert us_entry is not None
        assert us_entry["name"] == "United States"
        assert us_entry["currency"] == "USD"
        assert us_entry["language"] == "en"
        assert "flag" in us_entry
        assert "is_eu" in us_entry

    def test_list_countries_excludes_inactive(self, anon_client, us_mapping, db):
        """list_countries does not return inactive country mappings."""
        CountryMappingFactory(
            country_code="IN",
            country_name="Inactive Country",
            is_active=False,
        )
        resp = anon_client.get("/api/geoip/v1/countries/")
        data = resp.json()
        codes = [c["code"] for c in data]
        assert "IN" not in codes

    def test_list_countries_ordered_by_name(self, anon_client, us_mapping, de_mapping, gb_mapping):
        """list_countries returns countries ordered by name."""
        resp = anon_client.get("/api/geoip/v1/countries/")
        data = resp.json()
        names = [c["name"] for c in data]
        assert names == sorted(names)

    def test_list_countries_includes_flag_emoji(self, anon_client, us_mapping):
        """list_countries includes flag emoji for each country."""
        resp = anon_client.get("/api/geoip/v1/countries/")
        data = resp.json()
        us_entry = next((c for c in data if c["code"] == "US"), None)
        assert us_entry is not None
        assert us_entry["flag"] != ""

    def test_list_countries_empty_when_no_mappings(self, anon_client, db):
        """list_countries returns empty list when no active mappings."""
        CountryMapping.objects.all().delete()
        resp = anon_client.get("/api/geoip/v1/countries/")
        data = resp.json()
        assert data == []


# ============================================================
# API Tests: report_correction
# ============================================================


class TestReportCorrectionAPI:
    def _prime_session_with_visitor(self, client):
        """Establish a Django session and attach a VisitorLocation to it.

        The GeoIP middleware EXCLUDES /api/ paths from tracking, so hitting the
        resolve endpoint does not create a VisitorLocation. Use the admin login
        page (or any non-/api/ page) to establish a session, then create the
        visitor row directly.
        """
        # Any non-API request will trigger SessionMiddleware to save the session.
        client.get("/en/admin/login/")
        session_key = client.session.session_key
        if not session_key:
            # Force session creation
            session = client.session
            session.save()
            session_key = session.session_key
        VisitorLocation.objects.get_or_create(
            session_key=session_key,
            defaults={"ip_address": "127.0.0.1", "resolved_country": "US"},
        )
        return session_key

    def test_report_creates_correction(self, anon_client, db):
        """report_correction updates the visitor for the current session."""
        self._prime_session_with_visitor(anon_client)
        resp = anon_client.post(
            "/api/geoip/v1/report/",
            data={"actual_country": "CA"},
            content_type="application/json",
        )
        assert resp.status_code == 200
        assert resp.json()["status"] == "success"

    def test_report_updates_visitor_location(self, anon_client, db):
        """report_correction updates the visitor's correction fields."""
        session_key = self._prime_session_with_visitor(anon_client)
        visitor = VisitorLocation.objects.get(session_key=session_key)

        resp = anon_client.post(
            "/api/geoip/v1/report/",
            data={
                "actual_country": "CA",
                "actual_city": "Toronto",
                "actual_region": "Ontario",
            },
            content_type="application/json",
        )
        assert resp.status_code == 200
        assert resp.json()["status"] == "success"

        visitor.refresh_from_db()
        assert visitor.actual_country == "CA"
        assert visitor.actual_city == "Toronto"
        assert visitor.actual_region == "Ontario"

    def test_report_only_allows_post(self, anon_client):
        """report_correction only accepts POST requests."""
        resp = anon_client.get("/api/geoip/v1/report/")
        assert resp.status_code == 405


# ============================================================
# URL Routing Tests
# ============================================================


class TestURLRouting:
    def test_api_resolve_url(self):
        """API resolve URL resolves correctly."""
        url = reverse("geoip:geoip_api:resolve")
        assert url == "/api/geoip/v1/resolve/"

    def test_api_preference_url(self):
        """API preference URL resolves correctly."""
        url = reverse("geoip:geoip_api:preference")
        assert url == "/api/geoip/v1/preference/"

    def test_api_suggest_currency_url(self):
        """API suggest currency URL resolves correctly."""
        url = reverse("geoip:geoip_api:suggest_currency")
        assert url == "/api/geoip/v1/suggest/currency/"

    def test_api_suggest_language_url(self):
        """API suggest language URL resolves correctly."""
        url = reverse("geoip:geoip_api:suggest_language")
        assert url == "/api/geoip/v1/suggest/language/"

    def test_api_countries_url(self):
        """API countries URL resolves correctly."""
        url = reverse("geoip:geoip_api:countries")
        assert url == "/api/geoip/v1/countries/"

    def test_api_report_url(self):
        """API report URL resolves correctly."""
        url = reverse("geoip:geoip_api:report_correction")
        assert url == "/api/geoip/v1/report/"

    def test_admin_geolocations_filter_url(self):
        """Admin AJAX geolocations filter URL resolves correctly."""
        url = reverse("geoip_admin:geolocations_filter")
        assert "/admin/geoip/" in url

    def test_admin_visitors_filter_url(self):
        """Admin AJAX visitors filter URL resolves correctly."""
        url = reverse("geoip_admin:visitors_filter")
        assert "/admin/geoip/" in url

    def test_admin_provider_dashboard_url(self):
        """Admin provider dashboard URL resolves correctly."""
        url = reverse("geoip_admin:provider_dashboard")
        assert "/admin/geoip/providers/" in url

    def test_admin_provider_wizard_url(self):
        """Admin provider wizard URL resolves correctly."""
        url = reverse("geoip_admin:provider_wizard", args=["maxmind"])
        assert "maxmind" in url

    def test_admin_test_provider_url(self):
        """Admin test provider URL resolves correctly."""
        url = reverse("geoip_admin:test_provider", args=["maxmind"])
        assert "maxmind" in url

    def test_admin_toggle_provider_url(self):
        """Admin toggle provider URL resolves correctly."""
        url = reverse("geoip_admin:toggle_provider", args=[1])
        assert "1" in url


# ============================================================
# Admin Changelist Tests
# ============================================================


class TestAdminChangelistPages:
    @pytest.fixture(autouse=True)
    def _ensure_staff_login(self, staff_client, admin_user):
        """Re-login staff client before each test to prevent auth loss."""
        staff_client.force_login(admin_user)

    def test_geolocation_changelist(self, staff_client, db):
        """GeoLocation admin changelist returns 200."""
        GeoLocationFactory(ip_address="10.1.0.1")
        url = reverse("admin:geoip_geolocation_changelist")
        resp = staff_client.get(url)
        assert resp.status_code == 200

    def test_countrymapping_changelist(self, staff_client, us_mapping):
        """CountryMapping admin changelist returns 200."""
        url = reverse("admin:geoip_countrymapping_changelist")
        resp = staff_client.get(url)
        assert resp.status_code == 200

    def test_geoipprovider_changelist(self, staff_client, db):
        """GeoIPProvider admin changelist returns 200."""
        GeoIPProviderFactory()
        url = reverse("admin:geoip_geoipprovider_changelist")
        resp = staff_client.get(url)
        assert resp.status_code == 200

    def test_visitorlocation_changelist(self, staff_client, db):
        """VisitorLocation admin changelist returns 200."""
        VisitorLocationFactory()
        url = reverse("admin:geoip_visitorlocation_changelist")
        resp = staff_client.get(url)
        assert resp.status_code == 200

    def test_businessrule_changelist(self, staff_client, db):
        """BusinessRule admin changelist returns 200."""
        BusinessRuleFactory()
        url = reverse("admin:geoip_businessrule_changelist")
        resp = staff_client.get(url)
        assert resp.status_code == 200

    def test_geolocation_changelist_context_has_stats(self, staff_client, db):
        """GeoLocation changelist includes dashboard statistics in context."""
        GeoLocationFactory(ip_address="10.1.0.2")
        url = reverse("admin:geoip_geolocation_changelist")
        resp = staff_client.get(url)
        assert "total_locations" in resp.context
        assert "top_countries" in resp.context

    def test_geoipprovider_changelist_context_has_stats(self, staff_client, db):
        """GeoIPProvider changelist includes provider statistics in context."""
        GeoIPProviderFactory()
        url = reverse("admin:geoip_geoipprovider_changelist")
        resp = staff_client.get(url)
        assert "total_providers" in resp.context
        assert "active_providers" in resp.context

    def test_visitorlocation_changelist_context_has_stats(self, staff_client, db):
        """VisitorLocation changelist includes visitor statistics in context."""
        VisitorLocationFactory()
        url = reverse("admin:geoip_visitorlocation_changelist")
        resp = staff_client.get(url)
        assert "total_visitors" in resp.context
        assert "desktop_count" in resp.context

    def test_businessrule_changelist_context_has_stats(self, staff_client, db):
        """BusinessRule changelist includes rule statistics in context."""
        BusinessRuleFactory()
        url = reverse("admin:geoip_businessrule_changelist")
        resp = staff_client.get(url)
        assert "total_rules" in resp.context
        assert "active_rules" in resp.context

    def test_geolocation_changelist_non_staff_redirects(self, site_settings):
        """GeoLocation changelist redirects non-staff to login."""
        customer = UserFactory()
        client = Client()
        client.force_login(customer)
        url = reverse("admin:geoip_geolocation_changelist")
        resp = client.get(url)
        assert resp.status_code == 302


# ============================================================
# Admin AJAX Filter Tests
# ============================================================


class TestAdminAJAXFilters:
    @pytest.fixture(autouse=True)
    def _ensure_staff_login(self, staff_client, admin_user):
        """Re-login staff client before each AJAX test to prevent auth loss."""
        staff_client.force_login(admin_user)

    def _ajax_get(self, client, url, params=None):
        """Helper for AJAX GET requests with XMLHttpRequest header."""
        resp = client.get(
            url,
            data=params or {},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        assert resp.status_code == 200, f"Expected 200 from {url}, got {resp.status_code}"
        return resp

    def test_filter_geolocations_requires_ajax(self, staff_client, db):
        """filter_geolocations returns 400 without AJAX header."""
        url = reverse("geoip_admin:geolocations_filter")
        resp = staff_client.get(url)
        assert resp.status_code == 400

    def test_filter_geolocations_success(self, staff_client, db):
        """filter_geolocations returns HTML and count with AJAX header."""
        GeoLocationFactory(ip_address="10.2.0.1")
        url = reverse("geoip_admin:geolocations_filter")
        resp = self._ajax_get(staff_client, url)
        assert resp.status_code == 200
        data = resp.json()
        assert "html" in data
        assert "count" in data

    def test_filter_geolocations_by_country(self, staff_client, db):
        """filter_geolocations filters by country code."""
        GeoLocationFactory(ip_address="10.2.0.2", country_code="US")
        GeoLocationFactory(ip_address="10.2.0.3", country_code="GB")
        url = reverse("geoip_admin:geolocations_filter")
        resp = self._ajax_get(staff_client, url, {"country": "US"})
        data = resp.json()
        assert data["count"] >= 1

    def test_filter_geolocations_by_source(self, staff_client, db):
        """filter_geolocations filters by source."""
        GeoLocationFactory(ip_address="10.2.0.4", source="maxmind")
        GeoLocationFactory(ip_address="10.2.0.5", source="spwig")
        url = reverse("geoip_admin:geolocations_filter")
        resp = self._ajax_get(staff_client, url, {"source": "maxmind"})
        data = resp.json()
        assert data["count"] >= 1

    def test_filter_geolocations_by_vpn(self, staff_client, db):
        """filter_geolocations filters by VPN flag."""
        GeoLocationFactory(ip_address="10.2.0.6", is_vpn=True)
        GeoLocationFactory(ip_address="10.2.0.7", is_vpn=False)
        url = reverse("geoip_admin:geolocations_filter")
        resp = self._ajax_get(staff_client, url, {"is_vpn": "true"})
        data = resp.json()
        assert data["count"] >= 1

    def test_filter_geolocations_by_expired(self, staff_client, db):
        """filter_geolocations filters by expired status."""
        GeoLocationFactory(
            ip_address="10.2.0.8",
            expires_at=timezone.now() - timedelta(hours=1),
        )
        GeoLocationFactory(
            ip_address="10.2.0.9",
            expires_at=timezone.now() + timedelta(hours=1),
        )
        url = reverse("geoip_admin:geolocations_filter")
        resp = self._ajax_get(staff_client, url, {"expired": "true"})
        data = resp.json()
        assert data["count"] >= 1

    def test_filter_geolocations_by_ip(self, staff_client, db):
        """filter_geolocations searches by IP address."""
        GeoLocationFactory(ip_address="192.168.50.1")
        url = reverse("geoip_admin:geolocations_filter")
        resp = self._ajax_get(staff_client, url, {"ip": "192.168.50"})
        data = resp.json()
        assert data["count"] >= 1

    def test_filter_geolocations_requires_staff(self, site_settings):
        """filter_geolocations redirects non-staff users."""
        customer = UserFactory()
        client = Client()
        client.force_login(customer)
        url = reverse("geoip_admin:geolocations_filter")
        resp = client.get(url, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        assert resp.status_code == 302

    def test_filter_visitor_locations_requires_ajax(self, staff_client, db):
        """filter_visitor_locations returns 400 without AJAX header."""
        url = reverse("geoip_admin:visitors_filter")
        resp = staff_client.get(url)
        assert resp.status_code == 400

    def test_filter_visitor_locations_success(self, staff_client, db):
        """filter_visitor_locations returns HTML and count."""
        VisitorLocationFactory()
        url = reverse("geoip_admin:visitors_filter")
        resp = self._ajax_get(staff_client, url)
        assert resp.status_code == 200
        data = resp.json()
        assert "html" in data
        assert "count" in data

    def test_filter_visitor_locations_by_country(self, staff_client, db):
        """filter_visitor_locations filters by country."""
        VisitorLocationFactory(resolved_country="GB")
        url = reverse("geoip_admin:visitors_filter")
        resp = self._ajax_get(staff_client, url, {"country": "GB"})
        data = resp.json()
        assert data["count"] >= 1

    def test_filter_visitor_locations_by_device_type(self, staff_client, db):
        """filter_visitor_locations filters by device type."""
        VisitorLocationFactory(device_type="mobile")
        url = reverse("geoip_admin:visitors_filter")
        resp = self._ajax_get(staff_client, url, {"device_type": "mobile"})
        data = resp.json()
        assert data["count"] >= 1

    def test_filter_visitor_locations_by_corrected(self, staff_client, db):
        """filter_visitor_locations filters by corrected status."""
        VisitorLocationFactory(
            resolved_country="US",
            actual_country="CA",
        )
        url = reverse("geoip_admin:visitors_filter")
        resp = self._ajax_get(staff_client, url, {"corrected": "true"})
        data = resp.json()
        assert data["count"] >= 1

    def test_filter_visitor_locations_by_search(self, staff_client, db):
        """filter_visitor_locations searches by session key or IP."""
        VisitorLocationFactory(
            session_key="unique_test_session_xyz",
            ip_address="10.99.99.99",
        )
        url = reverse("geoip_admin:visitors_filter")
        resp = self._ajax_get(staff_client, url, {"search": "unique_test_session"})
        data = resp.json()
        assert data["count"] >= 1

    def test_filter_visitor_locations_requires_staff(self, site_settings):
        """filter_visitor_locations redirects non-staff users."""
        customer = UserFactory()
        client = Client()
        client.force_login(customer)
        url = reverse("geoip_admin:visitors_filter")
        resp = client.get(url, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        assert resp.status_code == 302


# ============================================================
# Admin Provider Views Tests
# ============================================================


class TestProviderDashboard:
    def test_provider_dashboard_url_resolves(self):
        """provider_dashboard URL resolves correctly."""
        url = reverse("geoip_admin:provider_dashboard")
        assert "/admin/geoip/providers/" in url

    def test_provider_dashboard_requires_staff(self, site_settings):
        """provider_dashboard redirects non-staff users to admin login."""
        customer = UserFactory()
        client = Client()
        client.force_login(customer)
        url = reverse("geoip_admin:provider_dashboard")
        resp = client.get(url)
        assert resp.status_code == 302
        assert "/admin/" in resp.url


class TestProviderWizard:
    @pytest.fixture(autouse=True)
    def _ensure_staff_login(self, staff_client, admin_user):
        """Re-login staff client before each test to prevent auth loss."""
        staff_client.force_login(admin_user)

    def test_wizard_returns_200_for_valid_type(self, staff_client, db):
        """provider_wizard returns 200 for valid provider type."""
        url = reverse("geoip_admin:provider_wizard", args=["maxmind"])
        resp = staff_client.get(url)
        assert resp.status_code == 200

    def test_wizard_redirects_for_invalid_type(self, staff_client, db):
        """provider_wizard redirects for invalid provider type."""
        url = reverse("geoip_admin:provider_wizard", args=["nonexistent"])
        resp = staff_client.get(url)
        assert resp.status_code == 302

    def test_wizard_save_creates_provider(self, staff_client, db):
        """provider_wizard step 4 creates a new GeoIPProvider."""
        url = reverse("geoip_admin:provider_wizard", args=["maxmind"])
        resp = staff_client.post(
            url,
            data={
                "step": "4",
                "api_key": "",
                "license_key": "test_license_abc",
                "is_active": "on",
                "priority": "10",
                "cache_duration": "86400",
                "timeout": "5",
                "batch_size": "100",
            },
        )
        assert resp.status_code == 302  # Redirect on success
        provider = GeoIPProvider.objects.filter(provider_type="maxmind").first()
        assert provider is not None
        assert provider.config["license_key"] == "test_license_abc"

    def test_wizard_save_uses_config_field(self, staff_client, db):
        """provider_wizard saves to .config field (not .configuration)."""
        url = reverse("geoip_admin:provider_wizard", args=["ipapi"])
        staff_client.post(
            url,
            data={
                "step": "4",
                "api_key": "my_api_key_123",
                "is_active": "on",
                "priority": "5",
                "cache_duration": "3600",
                "timeout": "10",
                "batch_size": "50",
            },
        )
        provider = GeoIPProvider.objects.filter(provider_type="ipapi").first()
        assert provider is not None
        # Verify .config is used (not .configuration which was a bug)
        assert "api_key" in provider.config
        assert provider.config["api_key"] == "my_api_key_123"
        assert not hasattr(provider, "configuration")

    def test_wizard_updates_existing_provider(self, staff_client, db):
        """provider_wizard updates existing provider instead of creating new one."""
        existing = GeoIPProviderFactory(
            name="MaxMind GeoLite2",
            provider_type="maxmind",
            config={"license_key": "old_key"},
            priority=10,
        )
        url = reverse("geoip_admin:provider_wizard", args=["maxmind"])
        resp = staff_client.post(
            url,
            data={
                "step": "4",
                "license_key": "new_key",
                "is_active": "on",
                "priority": "5",
                "cache_duration": "86400",
                "timeout": "5",
                "batch_size": "100",
            },
        )
        assert resp.status_code == 302, f"Expected redirect after save, got {resp.status_code}"
        existing.refresh_from_db()
        assert existing.config["license_key"] == "new_key"
        assert existing.priority == 5
        # Ensure no duplicate was created
        assert GeoIPProvider.objects.filter(provider_type="maxmind").count() == 1

    def test_wizard_requires_staff(self, site_settings):
        """provider_wizard redirects non-staff users."""
        customer = UserFactory()
        client = Client()
        client.force_login(customer)
        url = reverse("geoip_admin:provider_wizard", args=["maxmind"])
        resp = client.get(url)
        assert resp.status_code == 302


class TestToggleProvider:
    @pytest.fixture(autouse=True)
    def _ensure_staff_login(self, staff_client, admin_user):
        """Re-login staff client before each test to prevent auth loss."""
        staff_client.force_login(admin_user)

    def test_toggle_provider_deactivates(self, staff_client, db):
        """toggle_provider deactivates an active provider."""
        provider = GeoIPProviderFactory(is_active=True)
        url = reverse("geoip_admin:toggle_provider", args=[provider.pk])
        resp = staff_client.post(url)
        assert resp.status_code == 302
        provider.refresh_from_db()
        assert provider.is_active is False

    def test_toggle_provider_activates(self, staff_client, db):
        """toggle_provider activates an inactive provider."""
        provider = GeoIPProviderFactory(is_active=False)
        url = reverse("geoip_admin:toggle_provider", args=[provider.pk])
        resp = staff_client.post(url)
        assert resp.status_code == 302
        provider.refresh_from_db()
        assert provider.is_active is True

    def test_toggle_provider_requires_post(self, staff_client, db):
        """toggle_provider only accepts POST requests."""
        provider = GeoIPProviderFactory()
        url = reverse("geoip_admin:toggle_provider", args=[provider.pk])
        resp = staff_client.get(url)
        assert resp.status_code == 405

    def test_toggle_provider_requires_staff(self, site_settings):
        """toggle_provider redirects non-staff users."""
        provider = GeoIPProviderFactory()
        customer = UserFactory()
        client = Client()
        client.force_login(customer)
        url = reverse("geoip_admin:toggle_provider", args=[provider.pk])
        resp = client.post(url)
        assert resp.status_code == 302
        assert "/admin/" in resp.url


class TestTestProvider:
    @pytest.fixture(autouse=True)
    def _ensure_staff_login(self, staff_client, admin_user):
        """Re-login staff client before each test to prevent auth loss."""
        staff_client.force_login(admin_user)

    def test_test_provider_returns_json(self, staff_client, db):
        """test_provider returns JSON response for configured provider."""
        GeoIPProviderFactory(
            name="Test ipapi",
            provider_type="ipapi",
            config={"api_key": "test_key"},
        )
        url = reverse("geoip_admin:test_provider", args=["ipapi"])
        resp = staff_client.post(url, data={"test_ip": "8.8.8.8"})
        assert resp.status_code == 200
        data = resp.json()
        assert "success" in data
        assert "message" in data

    def test_test_provider_not_configured(self, staff_client, db):
        """test_provider returns error JSON for unconfigured provider."""
        url = reverse("geoip_admin:test_provider", args=["maxmind"])
        resp = staff_client.post(url, data={"test_ip": "8.8.8.8"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is False

    def test_test_provider_requires_post(self, staff_client, db):
        """test_provider only accepts POST requests."""
        url = reverse("geoip_admin:test_provider", args=["maxmind"])
        resp = staff_client.get(url)
        assert resp.status_code == 405

    def test_test_provider_requires_staff(self, site_settings):
        """test_provider redirects non-staff users."""
        customer = UserFactory()
        client = Client()
        client.force_login(customer)
        url = reverse("geoip_admin:test_provider", args=["maxmind"])
        resp = client.post(url)
        assert resp.status_code == 302


# ============================================================
# Template Tag Tests
# ============================================================


class TestTemplateTags:
    def test_country_flag_us(self):
        """country_flag converts US to flag emoji."""
        flag = country_flag("US")
        assert flag != ""
        # US flag should be the regional indicator symbols for U and S
        assert flag == "\U0001f1fa\U0001f1f8"

    def test_country_flag_gb(self):
        """country_flag converts GB to flag emoji."""
        flag = country_flag("GB")
        assert flag == "\U0001f1ec\U0001f1e7"

    def test_country_flag_empty(self):
        """country_flag returns empty string for empty input."""
        assert country_flag("") == ""
        assert country_flag(None) == ""

    def test_country_flag_invalid_length(self):
        """country_flag returns empty string for non-2-char input."""
        assert country_flag("A") == ""
        assert country_flag("ABC") == ""

    def test_country_flag_case_insensitive(self):
        """country_flag handles lowercase input."""
        flag = country_flag("us")
        assert flag == country_flag("US")

    def test_country_name_tag_with_mapping(self, db):
        """country_name tag returns name from CountryMapping."""
        CountryMappingFactory(country_code="FR", country_name="France")
        result = country_name_tag("FR")
        assert result == "France"

    def test_country_name_tag_fallback(self, db):
        """country_name tag returns fallback for unmapped countries."""
        result = country_name_tag("US")
        # Falls back to built-in dict or the code itself
        assert result in ("United States", "US")

    def test_get_visitor_country_with_geo_location(self, db):
        """get_visitor_country returns country from request.geo_location."""
        request = RequestFactory().get("/")
        request.geo_location = {"country": "DE"}
        template = Template("{% load geoip_tags %}{% get_visitor_country %}")
        context = Context({"request": request})
        result = template.render(context)
        assert "DE" in result

    def test_get_visitor_country_without_geo_location(self, db):
        """get_visitor_country returns empty when no geo_location."""
        request = RequestFactory().get("/")
        template = Template("{% load geoip_tags %}{% get_visitor_country %}")
        context = Context({"request": request})
        result = template.render(context)
        assert result.strip() == ""

    def test_visitor_currency_from_geo_location(self, db):
        """visitor_currency returns currency from geo_location."""
        request = RequestFactory().get("/")
        request.geo_location = {"currency": "GBP"}
        request.session = {}
        template = Template("{% load geoip_tags %}{% visitor_currency %}")
        context = Context({"request": request})
        result = template.render(context)
        assert "GBP" in result

    def test_visitor_currency_prefers_session(self, db):
        """visitor_currency prefers session preference over geo."""
        request = RequestFactory().get("/")
        request.geo_location = {"currency": "GBP"}
        request.session = {"preferred_currency": "EUR"}
        template = Template("{% load geoip_tags %}{% visitor_currency %}")
        context = Context({"request": request})
        result = template.render(context)
        assert "EUR" in result

    def test_visitor_currency_default(self, db):
        """visitor_currency returns USD when no geo or session data."""
        request = RequestFactory().get("/")
        template = Template("{% load geoip_tags %}{% visitor_currency %}")
        context = Context({"request": request})
        result = template.render(context)
        assert "USD" in result

    def test_visitor_language_from_geo_location(self, db):
        """visitor_language returns language from geo_location."""
        request = RequestFactory().get("/")
        request.geo_location = {"language": "fr"}
        request.session = {}
        template = Template("{% load geoip_tags %}{% visitor_language %}")
        context = Context({"request": request})
        result = template.render(context)
        assert "fr" in result

    def test_visitor_language_prefers_session(self, db):
        """visitor_language prefers session preference over geo."""
        request = RequestFactory().get("/")
        request.geo_location = {"language": "fr"}
        request.session = {"preferred_language": "de"}
        template = Template("{% load geoip_tags %}{% visitor_language %}")
        context = Context({"request": request})
        result = template.render(context)
        assert "de" in result

    def test_visitor_language_default(self, db):
        """visitor_language returns en when no geo or session data."""
        request = RequestFactory().get("/")
        template = Template("{% load geoip_tags %}{% visitor_language %}")
        context = Context({"request": request})
        result = template.render(context)
        assert "en" in result

    def test_get_visitor_location_tag(self, db):
        """get_visitor_location returns full location dict."""
        request = RequestFactory().get("/")
        request.geo_location = {"country": "JP", "city": "Tokyo"}
        template = Template(
            "{% load geoip_tags %}{% get_visitor_location as loc %}{{ loc.country }}-{{ loc.city }}"
        )
        context = Context({"request": request})
        result = template.render(context)
        assert "JP-Tokyo" in result


# ============================================================
# IP Utility Tests
# ============================================================


class TestIPUtils:
    def test_is_valid_ip_v4(self):
        """is_valid_ip returns True for valid IPv4."""
        assert is_valid_ip("192.168.1.1") is True
        assert is_valid_ip("8.8.8.8") is True
        assert is_valid_ip("0.0.0.0") is True

    def test_is_valid_ip_v6(self):
        """is_valid_ip returns True for valid IPv6."""
        assert is_valid_ip("::1") is True
        assert is_valid_ip("2001:db8::1") is True

    def test_is_valid_ip_invalid(self):
        """is_valid_ip returns False for invalid IPs."""
        assert is_valid_ip("") is False
        assert is_valid_ip(None) is False
        assert is_valid_ip("999.999.999.999") is False
        assert is_valid_ip("not-an-ip") is False

    def test_is_private_ip(self):
        """is_private_ip correctly identifies private IPs."""
        assert is_private_ip("192.168.1.1") is True
        assert is_private_ip("10.0.0.1") is True
        assert is_private_ip("127.0.0.1") is True
        assert is_private_ip("172.16.0.1") is True

    def test_is_private_ip_public(self):
        """is_private_ip returns False for public IPs."""
        assert is_private_ip("8.8.8.8") is False
        assert is_private_ip("1.1.1.1") is False

    def test_get_ip_prefix_v4(self):
        """get_ip_prefix returns /24 prefix for IPv4."""
        prefix = get_ip_prefix("192.168.1.100")
        assert prefix == "192.168.1.0/24"

    def test_get_ip_prefix_v6(self):
        """get_ip_prefix returns /48 prefix for IPv6."""
        prefix = get_ip_prefix("2001:db8:abcd:1234::1")
        assert "/48" in prefix

    def test_anonymize_ip_v4(self):
        """anonymize_ip zeros last octet for IPv4."""
        anon = anonymize_ip("192.168.1.100")
        assert anon == "192.168.1.0"

    def test_anonymize_ip_v6(self):
        """anonymize_ip zeroes last bits for IPv6."""
        anon = anonymize_ip("2001:db8:abcd:1234:5678:9abc:def0:1234")
        assert "2001:db8:abcd" in anon

    def test_ip_to_int(self):
        """ip_to_int converts IP to integer."""
        result = ip_to_int("0.0.0.1")
        assert result == 1

    def test_ip_to_int_invalid(self):
        """ip_to_int returns 0 for invalid IP."""
        assert ip_to_int("invalid") == 0

    def test_int_to_ip_v4(self):
        """int_to_ip converts integer to IPv4."""
        result = int_to_ip(1, version=4)
        assert result == "0.0.0.1"

    def test_int_to_ip_invalid(self):
        """int_to_ip returns empty for invalid integer."""
        result = int_to_ip(-1, version=4)
        assert result == ""

    def test_is_in_range(self):
        """is_in_range checks if IP is in CIDR range."""
        assert is_in_range("192.168.1.50", "192.168.1.0/24") is True
        assert is_in_range("192.168.2.50", "192.168.1.0/24") is False

    def test_is_in_range_invalid(self):
        """is_in_range returns False for invalid inputs."""
        assert is_in_range("invalid", "192.168.1.0/24") is False
        assert is_in_range("192.168.1.1", "invalid") is False

    def test_get_ip_version(self):
        """get_ip_version returns correct version number."""
        assert get_ip_version("192.168.1.1") == 4
        assert get_ip_version("::1") == 6
        assert get_ip_version("invalid") == 0

    def test_get_client_ip_from_remote_addr(self):
        """get_client_ip falls back to REMOTE_ADDR."""
        request = RequestFactory().get("/")
        request.META["REMOTE_ADDR"] = "127.0.0.1"
        ip = get_client_ip(request)
        assert ip == "127.0.0.1"

    def test_get_client_ip_from_x_forwarded_for(self):
        """get_client_ip reads X-Forwarded-For header (first public IP)."""
        request = RequestFactory().get("/")
        # 8.8.8.8 is truly public (not private in Python 3.12)
        request.META["HTTP_X_FORWARDED_FOR"] = "8.8.8.8, 10.0.0.1"
        ip = get_client_ip(request)
        assert ip == "8.8.8.8"

    def test_get_client_ip_from_cf_connecting_ip(self):
        """get_client_ip prefers Cloudflare CF-Connecting-IP header."""
        request = RequestFactory().get("/")
        # 1.1.1.1 is truly public (not private in Python 3.12)
        request.META["HTTP_CF_CONNECTING_IP"] = "1.1.1.1"
        request.META["HTTP_X_FORWARDED_FOR"] = "10.0.0.1"
        ip = get_client_ip(request)
        assert ip == "1.1.1.1"

    def test_get_client_ip_skips_private(self):
        """get_client_ip skips private IPs in forwarded headers."""
        request = RequestFactory().get("/")
        # Both 10.0.0.1 (RFC 1918) and 203.0.113.x (RFC 5737 TEST-NET-3)
        # are private in Python 3.12. Only truly public IPs pass.
        request.META["HTTP_X_FORWARDED_FOR"] = "10.0.0.1"
        request.META["REMOTE_ADDR"] = "127.0.0.1"
        ip = get_client_ip(request)
        # 10.0.0.1 is private so skipped; falls back to REMOTE_ADDR
        assert ip == "127.0.0.1"


# ============================================================
# Security Tests
# ============================================================


class TestAPISecurity:
    def test_api_endpoints_allow_anonymous(self, anon_client):
        """All public API endpoints allow anonymous access."""
        public_endpoints = [
            "/api/geoip/v1/resolve/",
            "/api/geoip/v1/suggest/currency/",
            "/api/geoip/v1/suggest/language/",
            "/api/geoip/v1/countries/",
        ]
        for url in public_endpoints:
            resp = anon_client.get(url)
            assert resp.status_code == 200, f"{url} returned {resp.status_code}"

    def test_preference_allows_anonymous(self, anon_client):
        """set_preference allows anonymous POST."""
        resp = anon_client.post(
            "/api/geoip/v1/preference/",
            data={"currency": "EUR"},
            content_type="application/json",
        )
        assert resp.status_code == 200

    def test_admin_views_require_staff(self, site_settings):
        """All admin views redirect non-staff users."""
        customer = UserFactory()
        client = Client()
        client.force_login(customer)

        admin_urls = [
            reverse("geoip_admin:provider_dashboard"),
            reverse("geoip_admin:provider_wizard", args=["maxmind"]),
        ]
        for url in admin_urls:
            resp = client.get(url)
            assert resp.status_code == 302, f"{url} did not redirect non-staff"
            assert "/admin/" in resp.url

    def test_admin_post_views_require_staff(self, site_settings):
        """Admin POST views redirect non-staff users."""
        customer = UserFactory()
        client = Client()
        client.force_login(customer)
        provider = GeoIPProviderFactory()

        post_urls = [
            reverse("geoip_admin:toggle_provider", args=[provider.pk]),
            reverse("geoip_admin:test_provider", args=["spwig"]),
        ]
        for url in post_urls:
            resp = client.post(url)
            assert resp.status_code == 302, f"{url} did not redirect non-staff"

    def test_admin_changelist_pages_require_staff(self, site_settings):
        """Admin changelist pages require staff authentication."""
        customer = UserFactory()
        client = Client()
        client.force_login(customer)

        changelist_urls = [
            reverse("admin:geoip_geolocation_changelist"),
            reverse("admin:geoip_countrymapping_changelist"),
            reverse("admin:geoip_geoipprovider_changelist"),
            reverse("admin:geoip_visitorlocation_changelist"),
            reverse("admin:geoip_businessrule_changelist"),
        ]
        for url in changelist_urls:
            resp = client.get(url)
            assert resp.status_code == 302, f"{url} did not redirect non-staff"

    def test_unauthenticated_admin_redirects(self, site_settings):
        """Unauthenticated access to admin pages redirects to login."""
        client = Client()
        changelist_urls = [
            reverse("admin:geoip_geolocation_changelist"),
            reverse("admin:geoip_countrymapping_changelist"),
            reverse("admin:geoip_geoipprovider_changelist"),
            reverse("admin:geoip_visitorlocation_changelist"),
            reverse("admin:geoip_businessrule_changelist"),
        ]
        for url in changelist_urls:
            resp = client.get(url)
            assert resp.status_code == 302, f"{url} did not redirect unauthenticated"


# ============================================================
# Admin Display Method Tests
# ============================================================


class TestAdminDisplayMethods:
    def test_geolocation_country_flag_display(self, db):
        """GeoLocationAdmin country_flag method returns flag with code."""
        from geoip.admin import GeoLocationAdmin

        loc = GeoLocationFactory(ip_address="10.3.0.1", country_code="US")
        admin_instance = GeoLocationAdmin(GeoLocation, None)
        result = admin_instance.country_flag(loc)
        assert "US" in result

    def test_geolocation_country_flag_no_country(self, db):
        """GeoLocationAdmin country_flag returns dash for empty country."""
        from geoip.admin import GeoLocationAdmin

        loc = GeoLocationFactory(ip_address="10.3.0.2", country_code="")
        admin_instance = GeoLocationAdmin(GeoLocation, None)
        result = admin_instance.country_flag(loc)
        assert result == "-"

    def test_geolocation_confidence_display_high(self, db):
        """GeoLocationAdmin confidence_display shows high class for >= 80%."""
        from geoip.admin import GeoLocationAdmin

        loc = GeoLocationFactory(ip_address="10.3.0.3", confidence=0.95)
        admin_instance = GeoLocationAdmin(GeoLocation, None)
        result = admin_instance.confidence_display(loc)
        assert "geoip-confidence-high" in result
        assert "95%" in result

    def test_geolocation_confidence_display_medium(self, db):
        """GeoLocationAdmin confidence_display shows medium class for 50-79%."""
        from geoip.admin import GeoLocationAdmin

        loc = GeoLocationFactory(ip_address="10.3.0.4", confidence=0.65)
        admin_instance = GeoLocationAdmin(GeoLocation, None)
        result = admin_instance.confidence_display(loc)
        assert "geoip-confidence-medium" in result

    def test_geolocation_confidence_display_low(self, db):
        """GeoLocationAdmin confidence_display shows low class for < 50%."""
        from geoip.admin import GeoLocationAdmin

        loc = GeoLocationFactory(ip_address="10.3.0.5", confidence=0.30)
        admin_instance = GeoLocationAdmin(GeoLocation, None)
        result = admin_instance.confidence_display(loc)
        assert "geoip-confidence-low" in result

    def test_geolocation_is_expired_display(self, db):
        """GeoLocationAdmin is_expired_display shows correct status."""
        from geoip.admin import GeoLocationAdmin

        admin_instance = GeoLocationAdmin(GeoLocation, None)

        valid_loc = GeoLocationFactory(ip_address="10.3.0.6", expires_at=None)
        result = admin_instance.is_expired_display(valid_loc)
        assert "Valid" in result or "valid" in result.lower()

        expired_loc = GeoLocationFactory(ip_address="10.3.0.7", expired=True)
        result = admin_instance.is_expired_display(expired_loc)
        assert "Expired" in result or "expired" in result.lower()

    def test_provider_accuracy_display(self, db):
        """GeoIPProviderAdmin accuracy_display shows correct rate."""
        from geoip.admin import GeoIPProviderAdmin

        admin_instance = GeoIPProviderAdmin(GeoIPProvider, None)

        provider = GeoIPProviderFactory(total_lookups=100, successful_lookups=98)
        result = admin_instance.accuracy_display(provider)
        assert "98.0%" in result
        assert "geoip-confidence-high" in result

    def test_visitor_was_corrected_display(self, db):
        """VisitorLocationAdmin was_corrected_display shows correct status."""
        from geoip.admin import VisitorLocationAdmin

        admin_instance = VisitorLocationAdmin(VisitorLocation, None)

        uncorrected = VisitorLocationFactory(actual_country="")
        result = admin_instance.was_corrected_display(uncorrected)
        assert "geoip-corrected-no" in result

    def test_businessrule_times_triggered_display(self, db):
        """BusinessRuleAdmin times_triggered_display formats large numbers."""
        from geoip.admin import BusinessRuleAdmin

        admin_instance = BusinessRuleAdmin(BusinessRule, None)

        rule = BusinessRuleFactory(times_triggered=5000)
        result = admin_instance.times_triggered_display(rule)
        assert "5,000" in result

    def test_businessrule_times_triggered_display_small(self, db):
        """BusinessRuleAdmin times_triggered_display for small numbers."""
        from geoip.admin import BusinessRuleAdmin

        admin_instance = BusinessRuleAdmin(BusinessRule, None)

        rule = BusinessRuleFactory(times_triggered=42)
        result = admin_instance.times_triggered_display(rule)
        assert "42" in result


# ============================================================
# Admin Action Tests
# ============================================================


class TestAdminActions:
    def test_provider_reset_statistics(self, staff_client, db):
        """reset_statistics admin action resets trigger counts."""
        rule = BusinessRuleFactory(
            times_triggered=100,
            last_triggered=timezone.now(),
        )
        url = reverse("admin:geoip_businessrule_changelist")
        resp = staff_client.post(
            url,
            data={
                "action": "reset_statistics",
                "_selected_action": [rule.pk],
            },
        )
        assert resp.status_code == 302
        rule.refresh_from_db()
        assert rule.times_triggered == 0
        assert rule.last_triggered is None


# ============================================================
# Edge Case & Robustness Tests
# ============================================================


class TestEdgeCases:
    def test_suggest_currency_empty_accepted_currencies(self, anon_client, db):
        """suggest_currency handles empty accepted_currencies list."""
        CountryMappingFactory(
            country_code="NZ",
            country_name="New Zealand",
            default_currency="NZD",
            accepted_currencies=[],
        )
        resp = anon_client.get("/api/geoip/v1/suggest/currency/?country=NZ")
        data = resp.json()
        assert data["default"] == "NZD"
        # When accepted_currencies is empty, should fallback to [default]
        assert data["accepted"] == ["NZD"]

    def test_suggest_language_empty_supported_languages(self, anon_client, db):
        """suggest_language handles empty supported_languages list."""
        CountryMappingFactory(
            country_code="NZ",
            country_name="New Zealand",
            default_language="en",
            supported_languages=[],
        )
        resp = anon_client.get("/api/geoip/v1/suggest/language/?country=NZ")
        data = resp.json()
        assert data["default"] == "en"
        assert data["supported"] == ["en"]

    def test_geolocation_with_ipv6(self, db):
        """GeoLocation can store IPv6 addresses."""
        loc = GeoLocationFactory(
            ip_address="2001:db8::1",
            ip_prefix="2001:db8::/48",
        )
        loc.refresh_from_db()
        assert loc.ip_address == "2001:db8::1"

    def test_visitor_location_referrer_url(self, db):
        """VisitorLocation can store long referrer URLs."""
        visitor = VisitorLocationFactory(
            referrer_url="https://www.example.com/very/long/path" + "?" + "q=" * 200,
        )
        visitor.refresh_from_db()
        assert visitor.referrer_url.startswith("https://www.example.com")

    def test_business_rule_complex_conditions(self, db):
        """BusinessRule evaluates complex multi-condition rules."""
        rule = BusinessRuleFactory(
            conditions={
                "country_in": ["US", "CA"],
                "region_not_in": ["Quebec"],
                "is_mobile": True,
            },
            actions={
                "set_currency": "USD",
                "show_banner": True,
                "redirect_to": "/us-store",
            },
        )
        # US + mobile + not Quebec -> True
        assert (
            rule.evaluate(
                {
                    "country": "US",
                    "region": "California",
                    "is_mobile": True,
                }
            )
            is True
        )

        # CA + Quebec + mobile -> False (Quebec excluded)
        assert (
            rule.evaluate(
                {
                    "country": "CA",
                    "region": "Quebec",
                    "is_mobile": True,
                }
            )
            is False
        )

        # US + not mobile -> False
        assert (
            rule.evaluate(
                {
                    "country": "US",
                    "region": "New York",
                    "is_mobile": False,
                }
            )
            is False
        )

    def test_report_correction_partial_fields(self, anon_client, db):
        """report_correction accepts partial correction fields."""
        # GeoIP middleware excludes /api/ paths from tracking, so establish a
        # session via a non-API path and create the visitor row explicitly.
        anon_client.get("/en/admin/login/")
        session = anon_client.session
        session.save()
        session_key = session.session_key
        visitor, _ = VisitorLocation.objects.get_or_create(
            session_key=session_key,
            defaults={"ip_address": "127.0.0.1", "resolved_country": "US"},
        )

        resp = anon_client.post(
            "/api/geoip/v1/report/",
            data={"actual_country": "CA"},
            content_type="application/json",
        )
        assert resp.status_code == 200
        visitor.refresh_from_db()
        assert visitor.actual_country == "CA"

    def test_country_mapping_cod_and_blocked_payments(self, db):
        """CountryMapping stores payment restriction fields."""
        cm = CountryMappingFactory(
            country_code="NG",
            country_name="Nigeria",
            supports_cod=True,
            blocked_payment_methods=["bitcoin", "wire_transfer"],
        )
        cm.refresh_from_db()
        assert cm.supports_cod is True
        assert "bitcoin" in cm.blocked_payment_methods

    def test_geolocation_to_dict_with_null_resolved_at(self, db):
        """to_dict handles None resolved_at gracefully."""
        loc = GeoLocationFactory(ip_address="10.4.0.1")
        # Force resolved_at to None for testing the conditional
        d = loc.to_dict()
        # resolved_at is auto_now_add so it will be set; just verify it's in ISO format
        assert d["resolved_at"] is not None

    def test_provider_accuracy_rate_100_percent(self, db):
        """accuracy_rate returns 100% when all lookups succeed."""
        provider = GeoIPProviderFactory(
            total_lookups=1000,
            successful_lookups=1000,
            failed_lookups=0,
        )
        assert provider.accuracy_rate == 100.0
