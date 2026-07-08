"""
Component Types Service
Fetches and caches component types from the upgrade server.
Provides display name and icon lookups for component type slugs.
"""

import logging

import requests
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

CACHE_KEY = 'developer_portal:component_types'
CACHE_TTL = 600  # 10 minutes

# Fallback when upgrade server is unreachable
FALLBACK_TYPES = [
    {'slug': 'theme', 'name': 'Theme', 'icon': 'palette', 'description': ''},
]

# Map upgrade server icon identifiers to Font Awesome classes
ICON_MAP = {
    'palette': 'fa-palette',
    'widget': 'fa-puzzle-piece',
    'build': 'fa-tools',
    'extension': 'fa-cube',
    'vertical_align_top': 'fa-arrow-up',
    'vertical_align_bottom': 'fa-arrow-down',
    'local_shipping': 'fa-truck',
    'pos': 'fa-cash-register',
    'email': 'fa-envelope',
    'sms': 'fa-sms',
    'payment': 'fa-credit-card',
    'exchange': 'fa-exchange-alt',
    'terminal': 'fa-cash-register',
}
DEFAULT_ICON = 'fa-box'


def _fetch_types_from_server():
    """Fetch submittable component types from the upgrade server."""
    base_url = getattr(settings, 'UPGRADE_SERVER_URL', 'https://updates.spwig.com')
    api_key = getattr(settings, 'UPGRADE_SERVER_INTERNAL_API_KEY', '')

    if not api_key:
        logger.warning('UPGRADE_SERVER_INTERNAL_API_KEY not configured, using fallback types')
        return None

    try:
        response = requests.get(
            f'{base_url}/api/v1/internal/component-types/',
            params={'submittable': 'true'},
            headers={'X-API-KEY': api_key},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        return data.get('types', [])
    except requests.RequestException as e:
        logger.error('Failed to fetch component types from upgrade server: %s', str(e))
        return None


def get_submittable_types():
    """
    Get list of developer-submittable component types.
    Cached for 10 minutes. Falls back to theme-only on failure.

    Returns list of dicts: [{'slug': 'theme', 'name': 'Theme', 'icon': 'palette', ...}, ...]
    """
    cached = cache.get(CACHE_KEY)
    if cached is not None:
        return cached

    types = _fetch_types_from_server()
    if types is None:
        types = FALLBACK_TYPES

    cache.set(CACHE_KEY, types, CACHE_TTL)
    return types


def get_type_display(component_type_slug):
    """Get the display name for a component type slug."""
    for t in get_submittable_types():
        if t['slug'] == component_type_slug:
            return t['name']
    # Fallback: humanize the slug
    return component_type_slug.replace('_', ' ').title()


def get_type_icon(component_type_slug):
    """Get the Font Awesome icon class for a component type slug."""
    for t in get_submittable_types():
        if t['slug'] == component_type_slug:
            icon_id = t.get('icon', '')
            return ICON_MAP.get(icon_id, DEFAULT_ICON)
    return DEFAULT_ICON


def get_type_choices():
    """
    Get component types formatted as Django-style choices tuples.
    Useful for form dropdowns: [(slug, name), ...]
    """
    return [(t['slug'], t['name']) for t in get_submittable_types()]


def invalidate_cache():
    """Force refresh of cached types on next request."""
    cache.delete(CACHE_KEY)
