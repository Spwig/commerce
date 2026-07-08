"""
Store Information API

Public API endpoints for store information accessible by headless frontends.
Provides store details, contact info, social links, and accepted payment methods.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache
from django.utils import timezone

from core.models import SiteSettings
from core.api.authentication import HeadlessAPIMixin


# Cache timeout for store info (5 minutes)
STORE_INFO_CACHE_TIMEOUT = 300


def get_site_settings():
    """Get or create the singleton SiteSettings instance."""
    try:
        return SiteSettings.objects.first()
    except SiteSettings.DoesNotExist:
        return None


@extend_schema(
    tags=['Store'],
    summary=_("Get complete store information"),
    description=_("Get all public store information including basic info, contact details, address, and social links. Cached for 5 minutes."),
    responses={
        200: OpenApiResponse(description=_("Store information retrieved successfully")),
        404: OpenApiResponse(description=_("Store settings not configured")),
    }
)
@api_view(['GET'])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([AllowAny])
def get_store_info(request):
    """
    Get complete store information.

    Returns all public store information in a single request.
    Suitable for initial page load or store configuration.
    """
    cache_key = 'store_info_complete'
    cached_data = cache.get(cache_key)

    if cached_data:
        return Response({
            'success': True,
            'data': cached_data,
            'cached': True
        })

    settings = get_site_settings()
    if not settings:
        return Response({
            'success': False,
            'message': _('Store settings not configured')
        }, status=status.HTTP_404_NOT_FOUND)

    data = {
        'basic': {
            'name': settings.site_name,
            'tagline': settings.site_tagline,
            'description': settings.site_description,
            'url': settings.site_url,
            'favicon': request.build_absolute_uri(settings.get_favicon_url()) if settings.get_favicon_url() else None,
        },
        'contact': {
            'email': settings.support_email or settings.admin_email,
            'phone': settings.phone_number,
        },
        'address': {
            'line_1': settings.address_line_1,
            'line_2': settings.address_line_2,
            'city': settings.city,
            'state_province': settings.state_province,
            'postal_code': settings.postal_code,
            'country': settings.country,
            'formatted': _format_address(settings),
        },
        'social': {
            'facebook': settings.facebook_url or None,
            'twitter': settings.twitter_url or None,
            'instagram': settings.instagram_url or None,
            'linkedin': settings.linkedin_url or None,
        },
        'locale': {
            'default_currency': settings.default_currency,
            'default_language': settings.default_language,
            'default_timezone': settings.default_timezone,
        },
        'seo': {
            'meta_title': settings.meta_title,
            'meta_description': settings.meta_description,
            'meta_keywords': settings.meta_keywords,
        },
    }

    cache.set(cache_key, data, STORE_INFO_CACHE_TIMEOUT)

    return Response({
        'success': True,
        'data': data,
        'cached': False
    })


@extend_schema(
    tags=['Store'],
    summary=_("Get basic store information"),
    description=_("Get basic store details: name, tagline, description, and logo."),
    responses={200: OpenApiResponse(description=_("Basic store info"))}
)
@api_view(['GET'])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([AllowAny])
def get_store_basic_info(request):
    """Get basic store information."""
    settings = get_site_settings()
    if not settings:
        return Response({
            'success': False,
            'message': _('Store settings not configured')
        }, status=status.HTTP_404_NOT_FOUND)

    data = {
        'name': settings.site_name,
        'tagline': settings.site_tagline,
        'description': settings.site_description,
        'url': settings.site_url,
        'favicon': request.build_absolute_uri(settings.get_favicon_url()) if settings.get_favicon_url() else None,
    }

    return Response({
        'success': True,
        'data': data
    })


@extend_schema(
    tags=['Store'],
    summary=_("Get store contact information"),
    description=_("Get store contact details: email and phone number."),
    responses={200: OpenApiResponse(description=_("Contact information"))}
)
@api_view(['GET'])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([AllowAny])
def get_store_contact(request):
    """Get store contact information."""
    settings = get_site_settings()
    if not settings:
        return Response({
            'success': False,
            'message': _('Store settings not configured')
        }, status=status.HTTP_404_NOT_FOUND)

    data = {
        'email': settings.support_email or settings.admin_email,
        'phone': settings.phone_number,
        'address': {
            'line_1': settings.address_line_1,
            'line_2': settings.address_line_2,
            'city': settings.city,
            'state_province': settings.state_province,
            'postal_code': settings.postal_code,
            'country': settings.country,
        }
    }

    return Response({
        'success': True,
        'data': data
    })


@extend_schema(
    tags=['Store'],
    summary=_("Get store social media links"),
    description=_("Get store social media profile URLs."),
    responses={200: OpenApiResponse(description=_("Social media links"))}
)
@api_view(['GET'])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([AllowAny])
def get_store_social(request):
    """Get store social media links."""
    settings = get_site_settings()
    if not settings:
        return Response({
            'success': False,
            'message': _('Store settings not configured')
        }, status=status.HTTP_404_NOT_FOUND)

    # Only include non-empty URLs
    social_links = []

    if settings.facebook_url:
        social_links.append({
            'platform': 'facebook',
            'url': settings.facebook_url,
            'icon': 'fab fa-facebook-f'
        })

    if settings.twitter_url:
        social_links.append({
            'platform': 'twitter',
            'url': settings.twitter_url,
            'icon': 'fab fa-twitter'
        })

    if settings.instagram_url:
        social_links.append({
            'platform': 'instagram',
            'url': settings.instagram_url,
            'icon': 'fab fa-instagram'
        })

    if settings.linkedin_url:
        social_links.append({
            'platform': 'linkedin',
            'url': settings.linkedin_url,
            'icon': 'fab fa-linkedin-in'
        })

    return Response({
        'success': True,
        'data': {
            'links': social_links,
            'has_social': len(social_links) > 0
        }
    })


@extend_schema(
    tags=['Store'],
    summary=_("Get accepted payment methods"),
    description=_("Get list of payment methods accepted by the store."),
    responses={200: OpenApiResponse(description=_("Payment methods"))}
)
@api_view(['GET'])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([AllowAny])
def get_store_payment_methods(request):
    """
    Get accepted payment methods.

    Returns a list of active payment providers configured for the store.
    This is display information only - actual payment processing uses
    the checkout API.
    """
    try:
        from payment_providers.models import ProviderAccount

        active_providers = ProviderAccount.objects.filter(
            is_active=True,
            is_live=True  # Only show production-enabled providers
        ).values('provider_type', 'display_name')

        # Build display-friendly list
        payment_methods = []

        for provider in active_providers:
            # Map provider types to display info
            provider_info = _get_payment_provider_display_info(provider['provider_type'])
            payment_methods.append({
                'type': provider['provider_type'],
                'name': provider['display_name'] or provider_info['name'],
                'icon': provider_info['icon'],
                'logo': provider_info.get('logo'),
            })

        return Response({
            'success': True,
            'data': {
                'methods': payment_methods,
                'has_payments': len(payment_methods) > 0
            }
        })

    except Exception:
        # If payment_providers app not configured, return empty
        return Response({
            'success': True,
            'data': {
                'methods': [],
                'has_payments': False
            }
        })


@extend_schema(
    tags=['Store'],
    summary=_("Get shipping information"),
    description=_("Get general shipping information for the store."),
    responses={200: OpenApiResponse(description=_("Shipping information"))}
)
@api_view(['GET'])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([AllowAny])
def get_store_shipping_info(request):
    """
    Get general shipping information.

    Returns the store's shipping origin and available shipping methods.
    For actual shipping rates, use the checkout API.
    """
    settings = get_site_settings()
    if not settings:
        return Response({
            'success': False,
            'message': _('Store settings not configured')
        }, status=status.HTTP_404_NOT_FOUND)

    data = {
        'origin_country': settings.shipping_origin_country,
        'labels_enabled': settings.enable_shipping_labels,
    }

    # Get active shipping providers if available
    try:
        from shipping.models import ProviderAccount

        active_carriers = ProviderAccount.objects.filter(
            is_active=True
        ).values_list('display_name', flat=True)

        data['carriers'] = list(active_carriers)
    except Exception:
        data['carriers'] = []

    return Response({
        'success': True,
        'data': data
    })


@extend_schema(
    tags=['Store'],
    summary=_("Get store currency settings"),
    description=_("Get store's currency configuration including multi-currency support."),
    responses={200: OpenApiResponse(description=_("Currency settings"))}
)
@api_view(['GET'])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([AllowAny])
def get_store_currency_settings(request):
    """Get store currency configuration."""
    settings = get_site_settings()
    if not settings:
        return Response({
            'success': False,
            'message': _('Store settings not configured')
        }, status=status.HTTP_404_NOT_FOUND)

    data = {
        'default_currency': settings.default_currency,
        'multi_currency_enabled': settings.enable_multi_currency,
        'supported_currencies': settings.supported_currencies or [],
        'show_currency_switcher': settings.show_currency_switcher,
        'currency_selection_mode': settings.currency_selection_mode,
        'show_exchange_rate_info': settings.show_exchange_rate_info,
        'locale_formatting_enabled': settings.enable_locale_formatting,
    }

    return Response({
        'success': True,
        'data': data
    })


@extend_schema(
    tags=['Store'],
    summary=_("List available currencies"),
    description=_("Get all active currencies that the store accepts. Use this to populate a currency switcher on the storefront."),
    responses={200: OpenApiResponse(description=_("List of active currencies"))}
)
@api_view(['GET'])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([AllowAny])
def list_currencies(request):
    """
    List all active currencies for the storefront currency switcher.

    Returns active currencies with display info (code, name, symbol, flag).
    """
    from core.supported_currency_model import SupportedCurrency

    currencies = []
    for curr in SupportedCurrency.get_active_currencies():
        currencies.append({
            'code': curr.code,
            'name': curr.get_currency_name(),
            'symbol': curr.symbol,
            'is_active': True,
            'flag': curr.get_country_flag(),
            'show_flag': curr.show_flag,
            'show_symbol': curr.show_symbol,
            'custom_symbol': curr.custom_symbol,
        })

    return Response({
        'success': True,
        'currencies': currencies,
        'count': len(currencies)
    })


@extend_schema(
    tags=['Store'],
    summary=_("Set active currency"),
    description=_("Switch the session's active currency. The currency code must be a valid, supported ISO 4217 code."),
    request={'application/json': {'type': 'object', 'properties': {'currency': {'type': 'string', 'example': 'EUR'}}, 'required': ['currency']}},
    responses={
        200: OpenApiResponse(description=_("Currency changed successfully")),
        400: OpenApiResponse(description=_("Invalid or unsupported currency code")),
    }
)
@api_view(['POST'])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([AllowAny])
def set_currency_api(request):
    """
    Set the user's active currency for the session.

    Expects JSON body: {"currency": "EUR"}
    """
    from moneyed import CURRENCIES as MONEYED_CURRENCIES

    currency_code = (request.data.get('currency') or '').upper()

    if not currency_code:
        return Response({
            'success': False,
            'error': 'Currency code is required'
        }, status=status.HTTP_400_BAD_REQUEST)

    if currency_code not in MONEYED_CURRENCIES:
        return Response({
            'success': False,
            'error': f'Invalid currency code: {currency_code}'
        }, status=status.HTTP_400_BAD_REQUEST)

    settings = get_site_settings()
    if settings and settings.supported_currencies and currency_code not in settings.supported_currencies:
        return Response({
            'success': False,
            'error': f'Currency not supported: {currency_code}'
        }, status=status.HTTP_400_BAD_REQUEST)

    request.session['currency'] = currency_code

    return Response({
        'success': True,
        'currency': currency_code,
        'message': f'Currency changed to {currency_code}'
    })


def _format_address(settings):
    """Format address into a single string."""
    parts = []

    if settings.address_line_1:
        parts.append(settings.address_line_1)
    if settings.address_line_2:
        parts.append(settings.address_line_2)

    city_state_zip = []
    if settings.city:
        city_state_zip.append(settings.city)
    if settings.state_province:
        city_state_zip.append(settings.state_province)
    if settings.postal_code:
        city_state_zip.append(settings.postal_code)

    if city_state_zip:
        parts.append(', '.join(city_state_zip))

    if settings.country:
        parts.append(settings.country)

    return '\n'.join(parts)


def _get_payment_provider_display_info(provider_type):
    """Get display information for a payment provider type."""
    provider_info = {
        'stripe': {
            'name': 'Credit Card',
            'icon': 'fas fa-credit-card',
            'logo': '/static/images/payments/stripe.svg'
        },
        'paypal': {
            'name': 'PayPal',
            'icon': 'fab fa-paypal',
            'logo': '/static/images/payments/paypal.svg'
        },
        'square': {
            'name': 'Square',
            'icon': 'fas fa-credit-card',
            'logo': '/static/images/payments/square.svg'
        },
        'klarna': {
            'name': 'Klarna',
            'icon': 'fas fa-money-check',
            'logo': '/static/images/payments/klarna.svg'
        },
        'afterpay': {
            'name': 'Afterpay',
            'icon': 'fas fa-money-check',
            'logo': '/static/images/payments/afterpay.svg'
        },
        'apple_pay': {
            'name': 'Apple Pay',
            'icon': 'fab fa-apple-pay',
            'logo': '/static/images/payments/apple-pay.svg'
        },
        'google_pay': {
            'name': 'Google Pay',
            'icon': 'fab fa-google-pay',
            'logo': '/static/images/payments/google-pay.svg'
        },
    }

    return provider_info.get(provider_type, {
        'name': provider_type.replace('_', ' ').title(),
        'icon': 'fas fa-credit-card',
    })
