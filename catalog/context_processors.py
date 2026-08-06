"""
Storefront context processors for sales regions.
"""

import logging

logger = logging.getLogger(__name__)

_HIDDEN = {"region_suggestion": {"show": False}}


def region_suggestion(request):
    """
    Decide whether to show the first-visit region confirmation banner.

    Spwig auto-detects and silently applies the visitor's sales region. This
    confirmation lets the shopper know which region they've landed in and switch
    if it's wrong ("We've set your region to [X] — change?"). It is shown only
    when there's something worth confirming and the shopper hasn't acted:

      * they haven't chosen a region (no ``preferred_region``),
      * they haven't dismissed the banner (``region_prompt_dismissed`` cookie),
      * the store has more than one active SalesRegion, and
      * auto-detection put them in a NON-default region (i.e. it actually moved
        them off the store's primary market — otherwise there's nothing to
        confirm).

    Exposes ``region_suggestion`` = {show, current_region_name, countries,
    current_country_code} where ``countries`` feeds the "change country" picker.
    """
    # Cheap bail-outs first (these cover the vast majority of requests).
    if not hasattr(request, "session"):
        return _HIDDEN
    if request.session.get("preferred_region") or request.COOKIES.get("preferred_region"):
        return _HIDDEN
    if request.COOKIES.get("region_prompt_dismissed"):
        return _HIDDEN

    try:
        from catalog.middleware import get_region_from_request, get_ship_to_options
        from catalog.models import SalesRegion

        active = SalesRegion.objects.filter(is_active=True)
        # A choice only exists when there's more than one active region.
        if active.count() < 2:
            return _HIDDEN

        current = get_region_from_request(request)
        if not current:
            return _HIDDEN

        # Only confirm when auto-detection moved the visitor off the default
        # (highest-priority) region — a visitor already in the default market has
        # nothing to confirm.
        default = active.order_by("-priority").first()
        if not default or current.pk == default.pk:
            return _HIDDEN

        opts = get_ship_to_options(request)
        return {
            "region_suggestion": {
                "show": True,
                "current_region_name": current.name,
                "countries": opts["countries"],
                "current_country_code": opts["current_code"],
            }
        }
    except Exception as e:
        logger.error(f"region_suggestion context processor failed: {e}")
        return _HIDDEN
