"""
Client-side polling of the update server's ``/api/v1/tiers/`` endpoint.

Returns the per-service, per-tier rate-limit config so the admin dashboard
can render "used / limit" progress bars with correct denominators. Cached
for 5 min in the Django cache — matches the poll interval hosted services
use to hot-reload their own limits.
"""

import logging

import requests
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

CACHE_KEY = 'hosted_services:tier_config'
CACHE_TIMEOUT = 300  # 5 minutes


def get_tier_config() -> dict:
    """
    Return the currently-published tier config.

    Response shape mirrors ``GET /api/v1/tiers/`` on the update server:
        {
          "services": {
             "geoip":    {"community": {...}, "pro": {...}, ...},
             "geocoder": {...},
             "push":     {...},
          },
          "upgrade_url": "https://updates.spwig.com/upgrade/"
        }

    Falls back to an empty ``services`` dict when the update server is
    unreachable — the dashboard tile renders "usage unknown" rather than
    crashing.
    """
    cached = cache.get(CACHE_KEY)
    if cached is not None:
        return cached

    server_url = getattr(settings, 'UPDATE_SERVER_URL', None) or 'https://updates.spwig.com'
    try:
        response = requests.get(
            f"{server_url.rstrip('/')}/api/v1/tiers/",
            timeout=5,
        )
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        logger.debug("Tier config fetch failed: %s", e)
        data = {'services': {}, 'upgrade_url': 'https://updates.spwig.com/upgrade/'}

    cache.set(CACHE_KEY, data, timeout=CACHE_TIMEOUT)
    return data
