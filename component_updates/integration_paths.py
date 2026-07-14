"""
Centralized integration component paths and helpers.

Single source of truth for integration directory structure.
All provider loaders and registries import from here instead of
hardcoding paths to avoid scattered path references.
"""

import logging
from pathlib import Path

from django.conf import settings

logger = logging.getLogger(__name__)

COMPONENTS_DATA = Path(settings.BASE_DIR) / "components_data"
INTEGRATIONS_DIR = COMPONENTS_DATA / "integrations"

CACHE_MARKERS_DIR = COMPONENTS_DATA / ".cache_markers"


def touch_provider_cache_marker(component_type: str):
    """Write a cache marker file when a provider type is updated.

    Other workers detect the marker's mtime to know their in-memory
    cache is stale and needs reloading from disk.
    """
    try:
        CACHE_MARKERS_DIR.mkdir(parents=True, exist_ok=True)
        marker = CACHE_MARKERS_DIR / f"{component_type}.marker"
        marker.touch()
    except Exception as e:
        logger.warning(f"Could not write cache marker for {component_type}: {e}")


def provider_cache_is_stale(component_type: str, last_loaded_at: float) -> bool:
    """Check if a provider cache marker is newer than the last load time.

    Args:
        component_type: e.g. 'email_provider'
        last_loaded_at: time.time() value recorded when providers were last loaded

    Returns:
        True if the cache should be invalidated
    """
    marker = CACHE_MARKERS_DIR / f"{component_type}.marker"
    try:
        if marker.exists():
            return marker.stat().st_mtime > last_loaded_at
    except Exception:
        pass
    return False


def get_category_dir(component_type: str) -> Path:
    """Get the integration category directory for a component type.

    Uses the component_type slug directly as the directory name.
    This is dynamic — any new component type added on the update server
    will work without code changes.
    """
    return INTEGRATIONS_DIR / component_type


def import_component_module(component_dir: Path, module_path: str, module_name: str):
    """
    Import a provider module using file-path-based loading.

    This avoids requiring the directory to be a Python package.
    Uses importlib.util.spec_from_file_location for path-based imports.

    Args:
        component_dir: Path to component's current/ directory
        module_path: Entry point (e.g., 'provider' or 'provider.py')
        module_name: Unique module name for sys.modules
                     (e.g., 'email_provider_gmail_api')

    Returns:
        Imported module
    """
    import importlib.util
    import sys

    # Reloading a package leaves cached submodule entries in sys.modules
    # (e.g. `payment_provider_stripe.provider`). When __init__.py does
    # `from .provider import X`, Python resolves that through sys.modules
    # first and returns the STALE cached submodule — the class binding
    # then never picks up the new code, even though we just rebuilt the
    # top-level package spec.
    #
    # Purge the whole subtree so the fresh spec_from_file_location + exec
    # below actually run against disk on both the package and every
    # submodule. Without this, hot-swapping a provider component after
    # install requires a container restart to take effect.
    prefix = f"{module_name}."
    for name in [k for k in list(sys.modules) if k == module_name or k.startswith(prefix)]:
        del sys.modules[name]

    init_file = component_dir / "__init__.py"
    is_package = init_file.exists()

    parent_str = str(component_dir.parent)
    if parent_str not in sys.path:
        sys.path.insert(0, parent_str)

    try:
        if is_package:
            spec = importlib.util.spec_from_file_location(
                module_name, init_file, submodule_search_locations=[str(component_dir)]
            )
        else:
            if not module_path.endswith(".py"):
                module_path = f"{module_path}.py"
            module_file_path = component_dir / module_path
            spec = importlib.util.spec_from_file_location(module_name, module_file_path)

        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load module spec from {component_dir}")

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        if parent_str in sys.path:
            sys.path.remove(parent_str)
