"""
Version Compatibility Checker

Checks version compatibility between source and target Spwig installations.
"""

import logging
import re

from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class CompatibilityResult:
    """Result of a version compatibility check."""

    def __init__(self, compatible, message="", warnings=None):
        self.compatible = compatible
        self.message = message
        self.warnings = warnings or []

    def __bool__(self):
        return self.compatible


def parse_version(version_string):
    """
    Parse a version string into (major, minor, patch) tuple.

    Handles formats like '1.2.3', 'v1.2.3', '1.2'
    """
    if not version_string:
        return None

    # Strip 'v' prefix
    version_string = version_string.lstrip("v").strip()

    match = re.match(r"^(\d+)\.(\d+)(?:\.(\d+))?", version_string)
    if not match:
        return None

    major = int(match.group(1))
    minor = int(match.group(2))
    patch = int(match.group(3)) if match.group(3) else 0

    return (major, minor, patch)


def get_local_version():
    """Get the current Spwig version from settings or version file."""
    try:
        from django.conf import settings

        return getattr(settings, "SPWIG_VERSION", None) or getattr(settings, "VERSION", None)
    except Exception:
        return None


def check_version_compatibility(local_version_str, remote_version_str):
    """
    Check compatibility between local and remote Spwig versions.

    Rules:
    - Same major.minor: fully compatible
    - Same major, different minor: compatible with warnings
    - Different major: incompatible (blocked)

    Args:
        local_version_str: Local installation version string
        remote_version_str: Remote installation version string

    Returns:
        CompatibilityResult
    """
    local_version = parse_version(local_version_str)
    remote_version = parse_version(remote_version_str)

    if not local_version:
        return CompatibilityResult(
            True,
            message=str(_("Could not determine local version. Proceeding with caution.")),
            warnings=[str(_("Local version could not be determined."))],
        )

    if not remote_version:
        return CompatibilityResult(
            True,
            message=str(_("Could not determine remote version. Proceeding with caution.")),
            warnings=[str(_("Remote version could not be determined."))],
        )

    local_major, local_minor, local_patch = local_version
    remote_major, remote_minor, remote_patch = remote_version

    # Different major version - incompatible
    if local_major != remote_major:
        return CompatibilityResult(
            False,
            message=(
                f"Major version mismatch: local v{local_version_str} vs "
                f"remote v{remote_version_str}. Migration between different "
                f"major versions is not supported."
            ),
        )

    # Same major, different minor - compatible with warnings
    if local_minor != remote_minor:
        return CompatibilityResult(
            True,
            message=(
                f"Minor version difference: local v{local_version_str} vs "
                f"remote v{remote_version_str}."
            ),
            warnings=[
                (
                    f"Minor version mismatch (local: {local_minor}, remote: {remote_minor}). "
                    f"Some settings may not transfer correctly if they were introduced "
                    f"in a newer version."
                )
            ],
        )

    # Same major.minor, different patch - fully compatible
    if local_patch != remote_patch:
        return CompatibilityResult(
            True,
            message=(
                f"Compatible versions: local v{local_version_str} vs remote v{remote_version_str}."
            ),
        )

    # Exact same version
    return CompatibilityResult(True, message=f"Exact version match: v{local_version_str}.")


def check_component_compatibility(local_components, remote_components):
    """
    Compare installed components between source and target.

    Args:
        local_components: list of {slug, version, type} dicts
        remote_components: list of {slug, version, type} dicts

    Returns:
        dict: {
            'compatible': bool,
            'missing_on_target': list of component slugs,
            'missing_on_source': list of component slugs,
            'version_mismatches': list of {slug, local_version, remote_version},
            'warnings': list[str],
        }
    """
    local_map = {c["slug"]: c for c in local_components}
    remote_map = {c["slug"]: c for c in remote_components}

    missing_on_target = [slug for slug in remote_map if slug not in local_map]
    missing_on_source = [slug for slug in local_map if slug not in remote_map]

    version_mismatches = []
    for slug in set(local_map.keys()) & set(remote_map.keys()):
        if local_map[slug].get("version") != remote_map[slug].get("version"):
            version_mismatches.append(
                {
                    "slug": slug,
                    "local_version": local_map[slug].get("version"),
                    "remote_version": remote_map[slug].get("version"),
                }
            )

    warnings = []
    if missing_on_target:
        warnings.append(
            f"{len(missing_on_target)} component(s) on source not installed here: "
            f"{', '.join(missing_on_target[:5])}"
        )
    if version_mismatches:
        warnings.append(f"{len(version_mismatches)} component(s) have version mismatches.")

    return {
        "compatible": len(missing_on_target) == 0,
        "missing_on_target": missing_on_target,
        "missing_on_source": missing_on_source,
        "version_mismatches": version_mismatches,
        "warnings": warnings,
    }
