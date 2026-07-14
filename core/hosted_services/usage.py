"""
Client-side snapshot of per-service hosted usage.

Polls each hosted service's ``/api/v1/usage/`` endpoint on a 5-minute cache
and returns a merged dict for the admin dashboard tile + 80% banner + 90%
email task.

Design notes:
- Each hosted service (GeoIP, Geocoder, Push) is polled with its own JWT.
  For GeoIP and Geocoder the shop client already signs its own JWTs (via
  ``GeoIPClient`` and ``AutocompleteClient``). For Push we reuse
  ``PushClient``. Failures are non-fatal — a service that's unreachable
  simply appears as ``{'error': 'unreachable'}`` in the snapshot.
- Under Community edition, the ``day``/``month`` block in the response is
  what powers the "500 lookups today" progress bar. Paid tiers only report
  a minute/hour block.
"""

import logging
from typing import Any

import requests
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

CACHE_KEY = "hosted_services:usage_snapshot"
CACHE_TIMEOUT = 300  # 5 minutes


def _fetch_geoip_usage() -> dict[str, Any] | None:
    """Poll ``geoip.spwig.com/api/v1/usage/`` using the shop's GeoIPClient."""
    try:
        from geoip.client import GeoIPClient

        client = GeoIPClient()
        # Reuse the token the client already manages
        client._ensure_token()
        base_url = getattr(settings, "GEOIP_SERVICE_URL", "https://geoip.spwig.com")
        response = client.session.get(
            f"{base_url.rstrip('/')}/api/v1/usage",
            timeout=5,
        )
        if response.status_code != 200:
            return {"error": f"http_{response.status_code}"}
        return response.json()
    except Exception as e:
        logger.debug("GeoIP usage fetch failed: %s", e)
        return {"error": "unreachable"}


def _fetch_geocoder_usage() -> dict[str, Any] | None:
    """Poll ``geocoder.spwig.com/api/v1/usage`` using the shop's AutocompleteClient."""
    try:
        from address_autocomplete.services import AutocompleteClient

        client = AutocompleteClient()
        token = client._get_jwt_token()
        if not token:
            return {"error": "no_token"}
        base_url = getattr(settings, "ADDRESS_AUTOCOMPLETE_URL", "https://geocoder.spwig.com")
        response = requests.get(
            f"{base_url.rstrip('/')}/api/v1/usage",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5,
        )
        if response.status_code != 200:
            return {"error": f"http_{response.status_code}"}
        return response.json()
    except Exception as e:
        logger.debug("Geocoder usage fetch failed: %s", e)
        return {"error": "unreachable"}


def _fetch_push_usage() -> dict[str, Any] | None:
    """Poll ``push.spwig.com/api/v1/usage/`` using the shop's PushClient."""
    try:
        from admin_api.services.push_client import PushClient

        client = PushClient()
        base_url = client.base_url
        response = requests.get(
            f"{base_url.rstrip('/')}/api/v1/usage/",
            headers=client._get_headers(),
            timeout=5,
        )
        if response.status_code != 200:
            return {"error": f"http_{response.status_code}"}
        return response.json()
    except Exception as e:
        logger.debug("Push usage fetch failed: %s", e)
        return {"error": "unreachable"}


def _normalise(service: str, raw: dict[str, Any] | None) -> dict[str, Any]:
    """
    Reduce a per-service usage response to a common shape:

        {
          "service": "geoip",
          "tier": "community",
          "primary_window": {  # what the dashboard bar should track
              "label": "this month",  # or "today" / "this minute" / "this hour"
              "current": 3241,
              "limit": 10000,
              "pct": 32.4,
          },
          "over_limit": False,
          "error": None,
        }
    """
    if not raw or raw.get("error"):
        return {
            "service": service,
            "tier": None,
            "primary_window": None,
            "over_limit": False,
            "error": (raw or {}).get("error", "unreachable"),
        }

    tier = raw.get("tier")

    # Prefer the largest-scoped window that's set — month > day > hour > minute.
    window = None
    if raw.get("month"):
        window = ("this month", raw["month"])
    elif raw.get("day"):
        window = ("today", raw["day"])
    elif service == "push" and raw.get("requests_this_hour") is not None:
        # Legacy push /usage/ response
        window = (
            "this hour",
            {
                "current": raw["requests_this_hour"],
                "limit": raw.get("rate_limit"),
            },
        )
    elif raw.get("minute"):
        window = ("this minute", raw["minute"])

    if window is None:
        return {
            "service": service,
            "tier": tier,
            "primary_window": None,
            "over_limit": False,
            "error": None,
        }

    label, block = window
    current = block.get("current") or 0
    limit = block.get("limit")
    pct = round(100.0 * current / limit, 1) if limit and limit > 0 else 0.0

    return {
        "service": service,
        "tier": tier,
        "primary_window": {
            "label": label,
            "current": current,
            "limit": limit,
            "pct": pct,
        },
        "over_limit": (limit is not None and current >= limit),
        "error": None,
    }


def get_usage_snapshot() -> dict[str, Any] | None:
    """
    Return the cached per-service usage snapshot, or ``None`` if cold.

    **Never** fetches inline — outbound HTTPS is done exclusively by the
    ``refresh_hosted_service_usage`` Celery beat task. This keeps request
    threads (admin pages, context processors) synchronous-safe: a
    degraded upstream service can't stall admin rendering.

    Shape when warm:
        {
          'geoip':    {...normalised block...},
          'geocoder': {...},
          'push':     {...},
          'any_over_80':  bool,
          'any_over_100': bool,
          'upgrade_url': str,
        }
    """
    return cache.get(CACHE_KEY)


def refresh_usage_snapshot() -> dict[str, Any]:
    """
    Poll all three hosted services and repopulate the cache.

    Called by the ``refresh_hosted_service_usage`` Celery beat task on a
    5-minute cadence. Also usable from a management command for manual
    refresh. Does the actual outbound HTTPS work — do not call from a
    request handler.
    """
    from core.hosted_services.tiers import get_tier_config

    tier_config = get_tier_config()
    upgrade_url = tier_config.get("upgrade_url", "https://updates.spwig.com/upgrade/")

    geoip = _normalise("geoip", _fetch_geoip_usage())
    geocoder = _normalise("geocoder", _fetch_geocoder_usage())
    push = _normalise("push", _fetch_push_usage())

    services = {"geoip": geoip, "geocoder": geocoder, "push": push}
    percentages = [s["primary_window"]["pct"] for s in services.values() if s["primary_window"]]

    snapshot = {
        **services,
        "any_over_80": any(p >= 80.0 for p in percentages),
        "any_over_100": any(s["over_limit"] for s in services.values()),
        "upgrade_url": upgrade_url,
    }

    cache.set(CACHE_KEY, snapshot, timeout=CACHE_TIMEOUT)
    return snapshot
