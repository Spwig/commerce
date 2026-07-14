"""
GeoIP API Views
"""

import hashlib
import logging

from django.core.cache import cache
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)
from rest_framework import serializers, status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.api.authentication import HeadlessAPIMixin

from ..models import BusinessRule, CountryMapping, VisitorLocation
from ..templatetags.geoip_tags import country_flag as _country_code_to_flag
from ..tracking import track_page_view
from ..utils.ip_utils import get_client_ip

logger = logging.getLogger(__name__)


def _get_location_cache_key(ip):
    """Generate cache key based on IP address"""
    return f"geoip_location:{hashlib.md5(ip.encode()).hexdigest()}"


@extend_schema(
    tags=["GeoIP"],
    summary=_("Resolve user location from IP"),
    description=_(
        "Automatically detect user's geographic location from their IP address. Returns country, region, city, coordinates, currency, language, and timezone. Cached for performance."
    ),
    responses={
        200: inline_serializer(
            name="ResolvedLocationResponse",
            fields={
                "ip": serializers.CharField(help_text="IP address"),
                "country": serializers.CharField(help_text="ISO country code"),
                "country_name": serializers.CharField(help_text="Country name"),
                "region": serializers.CharField(required=False, help_text="Region code"),
                "city": serializers.CharField(required=False, help_text="City name"),
                "currency": serializers.CharField(help_text="Default currency"),
                "language": serializers.CharField(help_text="Default language"),
                "timezone": serializers.CharField(help_text="Timezone identifier"),
            },
        )
    },
)
@api_view(["GET"])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([AllowAny])
def resolve_location(request):
    """
    Resolve the current user's location

    GET /api/geoip/v1/resolve/

    Returns:
    {
        "ip": "192.168.1.1",
        "country": "US",
        "country_name": "United States",
        "region": "CA",
        "region_name": "California",
        "city": "San Francisco",
        "postal_code": "94102",
        "lat": 37.7749,
        "lon": -122.4194,
        "currency": "USD",
        "language": "en",
        "timezone": "America/Los_Angeles",
        "is_eu": false,
        "is_vpn": false,
        "is_proxy": false,
        "is_tor": false,
        "is_mobile": false,
        "source": "edge_header",
        "confidence": 0.95
    }
    """
    # Track page view from headless frontend (must happen before cache check,
    # since geo cache is per-IP but different pages are visited within the window)
    page = request.GET.get("page") or request.META.get("HTTP_X_TRACKED_PAGE")
    if page:
        track_page_view(request, page, source="headless")

    # Get client IP for cache key
    ip = get_client_ip(request)
    cache_key = _get_location_cache_key(ip)

    # Check cache first
    cached_location = cache.get(cache_key)
    if cached_location:
        return Response(cached_location)

    # Get location from middleware
    location = getattr(request, "geo_location", {})

    if not location:
        # Fallback if middleware didn't run
        location = {
            "ip": ip,
            "country": "US",
            "currency": "USD",
            "language": "en",
            "source": "default",
            "confidence": 0.0,
        }

    # Add country mapping data if available
    country_code = location.get("country_code") or location.get("country")
    if country_code:
        # Ensure 'country' field exists for frontend compatibility
        if "country" not in location:
            location["country"] = country_code

        try:
            mapping = CountryMapping.objects.get(country_code=country_code, is_active=True)
            location.update(
                {
                    "currency": mapping.default_currency,
                    "language": mapping.default_language,
                    "timezone": mapping.timezone,
                    "is_eu": mapping.is_eu_member,
                    "date_format": mapping.date_format,
                    "uses_metric": mapping.uses_metric,
                }
            )
        except CountryMapping.DoesNotExist:
            pass

    # Add default values for missing fields to avoid "Unknown" in UI
    location.setdefault("city", None)
    location.setdefault("region", None)
    location.setdefault("currency", "USD")
    location.setdefault("language", "en")

    # Use business rules already processed by middleware if available
    # to avoid double-counting trigger statistics
    if hasattr(request, "geo_rules") and request.geo_rules:
        location["business_rules"] = request.geo_rules
    else:
        applicable_rules = []
        for rule in BusinessRule.objects.filter(is_active=True).order_by("priority"):
            if rule.evaluate(location):
                applicable_rules.append({"name": rule.name, "actions": rule.actions})
                rule.times_triggered += 1
                rule.last_triggered = timezone.now()
                rule.save(update_fields=["times_triggered", "last_triggered"])

        if applicable_rules:
            location["business_rules"] = applicable_rules

    # Cache result for 5 minutes (per IP)
    cache.set(cache_key, location, timeout=300)

    return Response(location)


@extend_schema(
    tags=["GeoIP"],
    summary=_("Set user location preference"),
    description=_(
        "Override automatic location detection with user's preferred currency, language, and country. Stored in session and persists across visits."
    ),
    request=inline_serializer(
        name="LocationPreferenceRequest",
        fields={
            "currency": serializers.CharField(
                required=False, help_text="Preferred currency code (e.g., EUR)"
            ),
            "language": serializers.CharField(
                required=False, help_text="Preferred language code (e.g., fr)"
            ),
            "country": serializers.CharField(
                required=False, help_text="Preferred country code (e.g., FR)"
            ),
        },
    ),
    responses={
        200: OpenApiResponse(description=_("Preferences saved successfully")),
    },
)
@api_view(["POST"])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([AllowAny])
def set_preference(request):
    """
    Set user location preferences

    POST /api/geoip/v1/preference/
    {
        "currency": "EUR",
        "language": "fr",
        "country": "FR"
    }
    """
    preferences = request.data

    # Store in session
    for key in ["currency", "language", "country", "city"]:
        if key in preferences:
            request.session[f"preferred_{key}"] = preferences[key]

    # Update visitor location if exists
    session_key = request.session.session_key
    if session_key:
        try:
            visitor = VisitorLocation.objects.get(session_key=session_key)
            if "currency" in preferences:
                visitor.selected_currency = preferences["currency"]
            if "language" in preferences:
                visitor.selected_language = preferences["language"]
            if "country" in preferences:
                visitor.actual_country = preferences["country"]
            if "city" in preferences:
                visitor.actual_city = preferences["city"]
            visitor.save()
        except VisitorLocation.DoesNotExist:
            pass

    return Response({"status": "success"})


@extend_schema(
    tags=["GeoIP"],
    summary=_("Suggest currency based on location"),
    description=_(
        "Get recommended currency for a specific country or the user's detected location. Returns default currency, accepted alternatives, and currency symbol."
    ),
    parameters=[
        OpenApiParameter(
            name="country",
            type=str,
            location=OpenApiParameter.QUERY,
            description=_(
                "Two-letter country code (e.g., 'US', 'GB'). Uses detected location if not provided."
            ),
            required=False,
        ),
    ],
    responses={
        200: inline_serializer(
            name="CurrencySuggestionResponse",
            fields={
                "default": serializers.CharField(help_text="Default currency code"),
                "accepted": serializers.ListField(
                    child=serializers.CharField(), help_text="List of accepted currency codes"
                ),
                "symbol": serializers.CharField(help_text="Currency symbol"),
            },
        )
    },
)
@api_view(["GET"])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([AllowAny])
def suggest_currency(request):
    """
    Get suggested currencies for a country

    GET /api/geoip/v1/suggest/currency/?country=US

    Returns:
    {
        "default": "USD",
        "accepted": ["USD", "CAD"],
        "symbol": "$"
    }
    """
    country_code = request.GET.get("country", "").upper()

    if not country_code:
        # Use current location
        location = getattr(request, "geo_location", {})
        country_code = location.get("country", "US")

    try:
        mapping = CountryMapping.objects.get(country_code=country_code, is_active=True)

        currency_symbols = {
            "USD": "$",
            "EUR": "€",
            "GBP": "£",
            "JPY": "¥",
            "CNY": "¥",
            "INR": "₹",
            "CAD": "C$",
            "AUD": "A$",
        }

        return Response(
            {
                "default": mapping.default_currency,
                "accepted": mapping.accepted_currencies or [mapping.default_currency],
                "symbol": currency_symbols.get(mapping.default_currency, ""),
            }
        )
    except CountryMapping.DoesNotExist:
        return Response({"default": "USD", "accepted": ["USD"], "symbol": "$"})


@extend_schema(
    tags=["GeoIP"],
    summary=_("Suggest language based on location"),
    description=_(
        "Get recommended language for a specific country or the user's detected location. Returns default language and list of supported languages for that region."
    ),
    parameters=[
        OpenApiParameter(
            name="country",
            type=str,
            location=OpenApiParameter.QUERY,
            description=_(
                "Two-letter country code (e.g., 'US', 'CA'). Uses detected location if not provided."
            ),
            required=False,
        ),
    ],
    responses={
        200: inline_serializer(
            name="LanguageSuggestionResponse",
            fields={
                "default": serializers.CharField(help_text="Default language code"),
                "supported": serializers.ListField(
                    child=serializers.CharField(), help_text="List of supported language codes"
                ),
            },
        )
    },
)
@api_view(["GET"])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([AllowAny])
def suggest_language(request):
    """
    Get suggested languages for a country

    GET /api/geoip/v1/suggest/language/?country=US

    Returns:
    {
        "default": "en",
        "supported": ["en", "es"]
    }
    """
    country_code = request.GET.get("country", "").upper()

    if not country_code:
        # Use current location
        from core.utils import get_default_country

        location = getattr(request, "geo_location", {})
        country_code = location.get("country", get_default_country())

    try:
        mapping = CountryMapping.objects.get(country_code=country_code, is_active=True)

        return Response(
            {
                "default": mapping.default_language,
                "supported": mapping.supported_languages or [mapping.default_language],
            }
        )
    except CountryMapping.DoesNotExist:
        return Response({"default": "en", "supported": ["en"]})


@extend_schema(
    tags=["GeoIP"],
    summary=_("List all countries"),
    description=_(
        "Get list of all supported countries with their default currency, language, flag emoji, and EU membership status. Used for country selector components."
    ),
    responses={
        200: inline_serializer(
            name="CountryListItem",
            many=True,
            fields={
                "code": serializers.CharField(help_text="ISO country code"),
                "name": serializers.CharField(help_text="Country name"),
                "flag": serializers.CharField(help_text="Flag emoji"),
                "currency": serializers.CharField(help_text="Default currency code"),
                "language": serializers.CharField(help_text="Default language code"),
                "is_eu": serializers.BooleanField(help_text="EU membership status"),
            },
        )
    },
)
@api_view(["GET"])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([AllowAny])
def list_countries(request):
    """
    List all available countries

    GET /api/geoip/v1/countries/

    Returns:
    [
        {
            "code": "US",
            "name": "United States",
            "flag": "🇺🇸",
            "currency": "USD",
            "language": "en"
        },
        ...
    ]
    """
    countries = CountryMapping.objects.filter(is_active=True).order_by("country_name")

    data = []
    for country in countries:
        data.append(
            {
                "code": country.country_code,
                "name": country.country_name,
                "flag": _country_code_to_flag(country.country_code),
                "currency": country.default_currency,
                "language": country.default_language,
                "is_eu": country.is_eu_member,
                "timezone": country.timezone,
            }
        )

    return Response(data)


@extend_schema(
    tags=["GeoIP"],
    summary=_("Report location correction"),
    description=_(
        "Report incorrect location detection to help improve accuracy. Users can submit their actual location when automatic detection is wrong. Logged for analysis and model improvement."
    ),
    request=inline_serializer(
        name="LocationCorrectionRequest",
        fields={
            "actual_country": serializers.CharField(
                required=False, help_text="2-letter country code"
            ),
            "actual_city": serializers.CharField(required=False, help_text="City name"),
            "actual_region": serializers.CharField(required=False, help_text="Region/state code"),
            "feedback": serializers.CharField(required=False, help_text="Additional feedback"),
        },
    ),
    responses={
        200: OpenApiResponse(description=_("Correction reported successfully")),
        400: OpenApiResponse(description=_("Session required")),
    },
)
@api_view(["POST"])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([AllowAny])
def report_correction(request):
    """
    Report a location correction

    POST /api/geoip/v1/report/
    {
        "actual_country": "CA",
        "actual_city": "Toronto",
        "feedback": "I'm in Canada, not US"
    }
    """
    session_key = request.session.session_key
    if not session_key:
        return Response({"error": "Session required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        visitor = VisitorLocation.objects.get(session_key=session_key)

        # Update with corrections
        if "actual_country" in request.data:
            visitor.actual_country = request.data["actual_country"]
        if "actual_city" in request.data:
            visitor.actual_city = request.data["actual_city"]
        if "actual_region" in request.data:
            visitor.actual_region = request.data["actual_region"]

        visitor.save()

        logger.info(
            f"Location correction reported: {visitor.resolved_country} -> {visitor.actual_country}"
        )

        return Response({"status": "success", "message": "Thank you for the correction"})

    except VisitorLocation.DoesNotExist:
        return Response({"error": "Visitor not found"}, status=status.HTTP_404_NOT_FOUND)
