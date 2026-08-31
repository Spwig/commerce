"""Storefront endpoint that resolves deferred (per-visitor) navigation."""

import json

from django.http import HttpResponseNotAllowed, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_ratelimit.decorators import ratelimit

from .services.nav_visibility import MAX_NAV_PLACEMENTS, resolve_personalized_nav


@csrf_exempt
@ratelimit(key="ip", rate="60/m", block=False)
def personalize_nav(request):
    """Resolve deferred (per-visitor) navigation placeholders.

    CSRF-exempt READ-ONLY endpoint (same rationale as
    ``page_builder.views.personalize_page``): it is served from cached storefront
    pages where a per-session CSRF token can't be embedded, it changes no server
    state, it only ever returns the requesting visitor's own entitled nav (rules
    evaluate against their real session), and a cross-origin caller can't read the
    JSON response. Keep it read-only — do NOT add state changes here.

    POST ``{widget_placement_ids: [...]}`` → ``{widgets: {id: html|null}}``.
    """
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    # Unauthenticated + renders real widgets → cap per-IP to blunt abuse.
    if getattr(request, "limited", False):
        return JsonResponse({"error": "rate limited"}, status=429)

    try:
        payload = json.loads(request.body or "{}")
    except (ValueError, TypeError):
        return JsonResponse({"error": "invalid JSON"}, status=400)

    if not isinstance(payload, dict):
        return JsonResponse({"error": "invalid JSON"}, status=400)

    ids = payload.get("widget_placement_ids")
    if not isinstance(ids, list):
        return JsonResponse({"error": "widget_placement_ids required"}, status=400)
    # Only integer ids, capped — the service further restricts to placements that
    # are part of the site's active navigation.
    ids = [i for i in ids if isinstance(i, int)][:MAX_NAV_PLACEMENTS]

    # Pin the URL-authoritative market from the client (the POST URL has no
    # market prefix), re-validated against the real market slugs, so shell
    # region/language rules evaluate against the visitor's actual market rather
    # than defaulting. An unknown slug falls back to the default market.
    market_slug = payload.get("market_slug")
    if market_slug and isinstance(market_slug, str):
        from catalog.middleware import get_market_slugs

        request.market_slug = market_slug if market_slug in set(get_market_slugs()) else None

    result = resolve_personalized_nav(request, ids)

    # Keep the endpoint genuinely read-only: the visibility context collector
    # touches the session (first_visit / visit_count), but this endpoint must not
    # create/persist a session for an anonymous caller — drop those writes.
    if hasattr(request, "session"):
        request.session.modified = False

    response = JsonResponse({"widgets": result})
    response["Cache-Control"] = "private, no-store"
    return response
