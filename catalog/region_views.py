"""
Storefront ship-to region selector.

The shopper chooses a destination *country* ("Ship to [Australia]"); this view
resolves it to the SalesRegion that ships there and persists the choice. The
read side already exists: ``RegionDetectionMiddleware`` honours
``session["preferred_region"]`` (then the cookie) ahead of GeoIP, and every
listing / product page / catalog API routes region through
``get_region_from_request``. So writing ``preferred_region`` here is enough to
make the whole storefront reflect the chosen destination.

``preferred_country`` is stored alongside it purely so the selector can show the
exact country the shopper picked (a region groups several countries, so it can't
be recovered from the region alone).

Mirrors ``core.currency_views.set_currency``.
"""

import json
import logging

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from catalog.middleware import get_region_for_country
from shipping.models import ShippingCountry

logger = logging.getLogger(__name__)

# One year, matching the currency selector's cookie lifetime.
_COOKIE_MAX_AGE = 365 * 24 * 60 * 60


@require_POST
def set_region(request):
    """
    AJAX view to set the shopper's ship-to destination.

    Expects JSON body::

        {"country": "AU"}

    The country must be one the store ships to (an active ``ShippingCountry``).
    Persists ``preferred_region`` (the resolved SalesRegion code, read by the
    region middleware) and ``preferred_country`` in both the session and a
    cookie.
    """
    try:
        data = json.loads(request.body)
        country_code = data.get("country", "").upper()

        if not country_code:
            return JsonResponse({"success": False, "error": "Country code is required"}, status=400)

        # Only allow countries the store actually ships to.
        is_shippable = ShippingCountry.objects.filter(
            site_id=1, country_code=country_code, is_active=True
        ).exists()
        if not is_shippable:
            return JsonResponse(
                {"success": False, "error": f"We do not ship to: {country_code}"}, status=400
            )

        region = get_region_for_country(country_code)

        request.session["preferred_country"] = country_code
        switched_currency = None
        if region:
            request.session["preferred_region"] = region.code
            # Market model: follow the region's currency (but only for stores
            # that deliberately offer several — see switch_currency_for_region).
            switched_currency = switch_currency_for_region(request, region)
        else:
            # Shippable but not mapped to any SalesRegion (merchant config gap).
            # Keep the chosen country for display; leave region resolution to the
            # GeoIP/default fallback rather than pinning a stale value.
            request.session.pop("preferred_region", None)
            logger.warning(
                "Ship-to country %s has no matching SalesRegion; availability will "
                "fall back to the default region.",
                country_code,
            )

        response = JsonResponse(
            {
                "success": True,
                "country": country_code,
                "region": region.code if region else None,
                "currency": switched_currency,
            }
        )
        response.set_cookie(
            "preferred_country", country_code, max_age=_COOKIE_MAX_AGE, samesite="Lax"
        )
        if region:
            response.set_cookie(
                "preferred_region", region.code, max_age=_COOKIE_MAX_AGE, samesite="Lax"
            )
            if switched_currency:
                # Mirror the currency selector's persistence (session + cookie).
                response.set_cookie(
                    "selected_currency",
                    switched_currency,
                    max_age=_COOKIE_MAX_AGE,
                    samesite="Lax",
                )
        else:
            response.delete_cookie("preferred_region")
        return response

    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON in request body"}, status=400)

    except Exception as e:
        logger.error(f"Error setting ship-to region: {e}")
        return JsonResponse(
            {"success": False, "error": "An error occurred while changing your region"}, status=500
        )


def switch_currency_for_region(request, region):
    """
    Switch the session currency to a region's default — but only when the store
    deliberately offers a choice of currencies.

    A merchant is treated as multi-currency only when they have *explicitly*
    listed more than one code in ``SiteSettings.supported_currencies``. An empty
    list means "all currencies" (the untouched default) and a single entry means
    single-currency; in both cases the currency is left alone, so switching
    region never surprises a single-currency merchant (or shows prices in a
    currency with no configured exchange rate). Returns the code switched to, or
    None.
    """
    from core.models import SiteSettings

    target = (region.default_currency or "").upper()
    if not target:
        return None
    supported = SiteSettings.get_settings().supported_currencies or []
    if len(supported) > 1 and target in supported:
        request.session["currency"] = target
        return target
    return None
