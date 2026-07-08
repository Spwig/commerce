"""
Context Processors for Design App

Provides utility assets and other data to design templates (branding builder, header builder, etc.).
"""

from typing import Dict, Any
from django.http import HttpRequest


def design_settings(request: HttpRequest) -> Dict[str, Any]:
    """
    Provide global design settings to all templates.

    Includes logo, brand colors, typography settings from GlobalDesignSettings.

    Args:
        request: HttpRequest object

    Returns:
        Dictionary with design_settings object
    """
    from .models import GlobalDesignSettings

    try:
        settings = GlobalDesignSettings.get_settings()
        return {'design_settings': settings}
    except Exception:
        return {'design_settings': None}


def utility_assets(request: HttpRequest) -> Dict[str, Any]:
    """
    Provide utility CSS and JS assets to design templates.

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
        'utility_css_files': assets.get('css', []),
        'utility_js_files': assets.get('js', []),
    }
