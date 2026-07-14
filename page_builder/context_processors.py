"""
Context Processors for Page Builder

Provides utility assets and other data to page builder templates.
"""

from typing import Any

from django.http import HttpRequest


def utility_assets(request: HttpRequest) -> dict[str, Any]:
    """
    Provide utility CSS and JS assets to templates.

    Uses the auto-discovery system to dynamically load assets from
    all installed utility components. This allows merchants to install
    new utilities without modifying templates.

    Args:
        request: HttpRequest object

    Returns:
        Dictionary with utility_css_files and utility_js_files lists
    """
    from component_updates.utility_registry import get_utility_assets

    assets = get_utility_assets()

    return {
        "utility_css_files": assets.get("css", []),
        "utility_js_files": assets.get("js", []),
    }
