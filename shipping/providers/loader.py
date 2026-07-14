"""
Provider component loading utilities.

Handles loading and validating shipping provider component packages.
"""

import json
import logging
from pathlib import Path
from typing import Any

from packaging import version

logger = logging.getLogger(__name__)


def load_provider_manifest(component_dir: Path) -> dict[str, Any]:
    """
    Load and parse provider manifest.json file.

    Args:
        component_dir: Path to component directory

    Returns:
        Parsed manifest dictionary

    Raises:
        FileNotFoundError: If manifest.json not found
        json.JSONDecodeError: If manifest is invalid JSON
    """
    manifest_path = component_dir / "manifest.json"

    if not manifest_path.exists():
        raise FileNotFoundError(f"manifest.json not found in {component_dir}")

    try:
        with open(manifest_path, encoding="utf-8") as f:
            manifest = json.load(f)

        logger.debug(f"Loaded manifest from {manifest_path}")
        return manifest

    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in {manifest_path}: {e.msg}", e.doc, e.pos)


def validate_provider_package(manifest: dict[str, Any], component_dir: Path) -> None:
    """
    Validate provider package structure and manifest.

    Args:
        manifest: Parsed manifest dictionary
        component_dir: Path to component directory

    Raises:
        ValueError: If package is invalid
    """
    # Required manifest fields
    required_fields = [
        "name",
        "version",
        "component_type",
        "provider_key",
        "entry_point",
        "class_name",
    ]

    missing_fields = [field for field in required_fields if field not in manifest]
    if missing_fields:
        raise ValueError(f"Missing required manifest fields: {', '.join(missing_fields)}")

    # Validate component_type
    if manifest["component_type"] != "shipping_provider":
        raise ValueError(
            f"Invalid component type: {manifest['component_type']} (expected 'shipping_provider')"
        )

    # Validate version format
    try:
        version.parse(manifest["version"])
    except version.InvalidVersion:
        raise ValueError(f"Invalid version format: {manifest['version']}")

    # Validate entry point file exists
    entry_point = manifest["entry_point"]
    if not entry_point.endswith(".py"):
        entry_point = f"{entry_point}.py"

    entry_point_path = component_dir / entry_point
    if not entry_point_path.exists():
        raise ValueError(f"Entry point file not found: {entry_point}")

    logger.debug(f"Provider package validation passed for {manifest['name']}")


def check_platform_compatibility(manifest: dict[str, Any], platform_version: str) -> bool:
    """
    Check if provider is compatible with platform version.

    Args:
        manifest: Provider manifest dictionary
        platform_version: Current platform version string

    Returns:
        True if compatible, False otherwise
    """
    if "min_platform_version" not in manifest:
        # No requirement specified, assume compatible
        return True

    try:
        min_version = version.parse(manifest["min_platform_version"])
        current_version = version.parse(platform_version)

        compatible = current_version >= min_version

        if not compatible:
            logger.warning(
                f"Provider {manifest['name']} requires platform version "
                f">= {manifest['min_platform_version']}, current: {platform_version}"
            )

        return compatible

    except version.InvalidVersion as e:
        logger.error(f"Invalid version format: {e}")
        return False


def check_dependencies(manifest: dict[str, Any]) -> list[str]:
    """
    Check if all required dependencies are installed.

    Args:
        manifest: Provider manifest dictionary

    Returns:
        List of missing dependencies (empty if all present)
    """
    if "dependencies" not in manifest:
        return []

    missing = []

    for dep_name, dep_version in manifest["dependencies"].items():
        try:
            # Try to import the package
            importlib.import_module(dep_name)
            # TODO: Could add version checking here
        except ImportError:
            missing.append(f"{dep_name} {dep_version}")

    if missing:
        logger.warning(f"Missing dependencies: {', '.join(missing)}")

    return missing


def get_provider_metadata(component_dir: Path) -> dict[str, Any]:
    """
    Extract provider metadata from manifest.

    Args:
        component_dir: Path to component directory

    Returns:
        Dictionary with provider metadata:
        {
            'name': 'Easyship',
            'version': '1.0.0',
            'provider_key': 'easyship',
            'description': '...',
            'author': '...',
            'website': '...',
            'capabilities': {...}
        }
    """
    manifest = load_provider_manifest(component_dir)

    return {
        "name": manifest.get("name"),
        "version": manifest.get("version"),
        "provider_key": manifest.get("provider_key"),
        "description": manifest.get("description", ""),
        "author": manifest.get("author", ""),
        "website": manifest.get("website", ""),
        "capabilities": manifest.get("capabilities", {}),
        "entry_point": manifest.get("entry_point"),
        "class_name": manifest.get("class_name"),
    }


# Import at bottom to avoid circular imports
import importlib
