"""
Utility Auto-Discovery System

Scans the components_data directory for utility components and extracts their metadata.
Enables dynamic loading of utilities without hardcoding paths.
Includes caching for performance and zero-downtime installations.
"""

import logging
from typing import Any

from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

# Cache configuration
UTILITY_CACHE_KEY = "installed_utilities_list"
UTILITY_CACHE_TIMEOUT = 300  # 5 minutes
UTILITY_ASSETS_CACHE_KEY = "utility_assets_dict"


def discover_installed_utilities(use_cache: bool = True) -> list[dict[str, Any]]:
    """
    Discover all installed utility components by scanning the filesystem.

    This enables TRUE zero-downtime installation - new utilities appear
    immediately after extraction without requiring server restart or
    INSTALLED_APPS modifications.

    Args:
        use_cache: If True, use cached results for performance. Set False to force refresh.

    Returns:
        List of utility metadata dictionaries containing:
        - name: Utility name (e.g., 'color_picker')
        - css: List of CSS file paths
        - js: List of JS file paths
        - template: Template path (or None)
        - version: Utility version
        - description: Utility description
    """
    # Check cache first
    if use_cache:
        cached_utilities = cache.get(UTILITY_CACHE_KEY)
        if cached_utilities is not None:
            logger.debug(f"Using cached utilities list ({len(cached_utilities)} utilities)")
            return cached_utilities

    utilities = []

    # Scan filesystem for utility directories with 'current' symlinks
    from pathlib import Path

    utilities_static_path = Path(settings.BASE_DIR) / "components_data" / "static" / "utilities"

    if not utilities_static_path.exists():
        logger.warning(f"Utilities static path does not exist: {utilities_static_path}")
        return utilities

    for utility_dir in utilities_static_path.iterdir():
        if not utility_dir.is_dir():
            continue

        # Check for 'current' symlink
        current_link = utility_dir / "current"
        if not current_link.exists() or not current_link.is_symlink():
            logger.debug(f"Skipping {utility_dir.name} - no 'current' symlink")
            continue

        utility_name = utility_dir.name

        try:
            # Resolve symlink to get version
            version_dir = current_link.resolve()
            version = version_dir.name  # e.g., "v1.0.0"

            # Build asset paths (convention-based)
            css_files = []
            js_files = []

            # Find all CSS files in current version
            for css_file in version_dir.glob("*.css"):
                css_files.append(f"utilities/{utility_name}/current/{css_file.name}")

            # Find all JS files in current version
            for js_file in version_dir.glob("*.js"):
                js_files.append(f"utilities/{utility_name}/current/{js_file.name}")

            if css_files or js_files:
                utility_data = {
                    "name": utility_name,
                    "css": css_files,
                    "js": js_files,
                    "template": f"utilities/{utility_name}/current/template.html",
                    "version": version,
                    "description": f"{utility_name.replace('_', ' ').title()} utility",
                    "component_name": utility_name,
                }

                utilities.append(utility_data)
                logger.debug(f"Discovered utility: {utility_name} {version} (symlink-based)")

        except Exception as e:
            logger.error(f"Error discovering utility {utility_name}: {e}")

    logger.info(f"Discovered {len(utilities)} installed utilities")

    # Cache the results
    if use_cache:
        cache.set(UTILITY_CACHE_KEY, utilities, UTILITY_CACHE_TIMEOUT)
        logger.debug(f"Cached utilities list for {UTILITY_CACHE_TIMEOUT} seconds")

    return utilities


def get_utility_assets() -> dict[str, list[str]]:
    """
    Get all CSS and JS assets from installed utilities.

    Returns:
        Dictionary with 'css' and 'js' keys containing lists of asset paths.
    """
    utilities = discover_installed_utilities()

    assets = {
        "css": [],
        "js": [],
    }

    for utility in utilities:
        assets["css"].extend(utility["css"])
        assets["js"].extend(utility["js"])

    # Deduplicate by filename to handle both hyphen/underscore directory variants
    seen_js = set()
    assets["js"] = [
        p
        for p in assets["js"]
        if (fn := p.rsplit("/", 1)[-1]) not in seen_js and not seen_js.add(fn)
    ]
    seen_css = set()
    assets["css"] = [
        p
        for p in assets["css"]
        if (fn := p.rsplit("/", 1)[-1]) not in seen_css and not seen_css.add(fn)
    ]

    return assets


def get_utility_info(utility_name: str) -> dict[str, Any] | None:
    """
    Get metadata for a specific utility by name.

    Args:
        utility_name: Name of the utility (e.g., 'color_picker')

    Returns:
        Utility metadata dictionary or None if not found
    """
    utilities = discover_installed_utilities()
    for utility in utilities:
        if utility["name"] == utility_name:
            return utility
    logger.warning(f"Utility not found: {utility_name}")
    return None


def invalidate_utility_cache():
    """
    Invalidate the utility discovery cache.

    Call this after installing or uninstalling utilities to force
    re-discovery on next request. Enables zero-downtime installations.

    Example:
        # After installing new utility
        invalidate_utility_cache()
        # Next page request will discover the new utility
    """
    cache.delete(UTILITY_CACHE_KEY)
    cache.delete(UTILITY_ASSETS_CACHE_KEY)
    logger.info("Utility discovery cache invalidated")


def refresh_utility_cache():
    """
    Refresh the utility cache by forcing re-discovery.

    Returns:
        Number of utilities discovered
    """
    utilities = discover_installed_utilities(use_cache=False)
    logger.info(f"Utility cache refreshed with {len(utilities)} utilities")
    return len(utilities)
