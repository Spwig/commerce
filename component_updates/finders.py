"""
Custom staticfiles finders for component directories.

components_data/ contains two subdirectories that need special handling:

1. integrations/ — Full provider packages (Python source, tests, markdown)
   alongside a few static assets (logos). IntegrationStaticFinder filters
   by file extension to only collect actual static assets.

2. static/ — Utility and theme static files (CSS, JS) organized in versioned
   directories (v1.0.0, v1.0.1, ...) with a 'current' symlink pointing to
   the active version. ComponentStaticFinder skips old version directories
   so only files reachable via 'current/' are collected.
"""

import os
import re
from pathlib import Path

from django.conf import settings
from django.contrib.staticfiles import utils as staticfiles_utils
from django.contrib.staticfiles.finders import BaseFinder
from django.core.files.storage import FileSystemStorage

# File extensions that are actual static assets served to browsers
STATIC_EXTENSIONS = frozenset(
    {
        ".svg",
        ".png",
        ".gif",
        ".jpg",
        ".jpeg",
        ".webp",
        ".ico",
        ".css",
        ".js",
        ".woff",
        ".woff2",
        ".ttf",
        ".eot",
        ".json",
    }
)


_VERSION_RE = re.compile(r"^v?\d+\.\d+\.\d+$")


def _is_version_dir(name):
    """Check if a directory name is a version directory like v1.0.0, v2.1.3."""
    return bool(_VERSION_RE.match(name))


class IntegrationStaticFinder(BaseFinder):
    """
    Finds static files in components_data/integrations/, filtering to
    only include actual static assets (images, CSS, JS, fonts, JSON).

    Skips Python source code, markdown, tests, and other non-static files
    that exist in provider component packages.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.integrations_root = Path(settings.BASE_DIR) / "components_data" / "integrations"
        self.storage = FileSystemStorage(location=str(self.integrations_root))
        self.storage.prefix = ""

    def _is_static_asset(self, path):
        """Check if a file path has a static asset extension."""
        return Path(path).suffix.lower() in STATIC_EXTENSIONS

    def find(self, path, all=False):
        """Find a requested static file in the integrations directory."""
        full_path = self.integrations_root / path
        if full_path.exists() and full_path.is_file() and self._is_static_asset(path):
            if all:
                return [str(full_path)]
            return str(full_path)
        return [] if all else ""

    def list(self, ignore_patterns):
        """
        List all static asset files in the integrations directory.
        """
        if not self.integrations_root.exists():
            return

        for root, dirs, files in os.walk(str(self.integrations_root), followlinks=True):
            # Skip __pycache__ and versioned directories (v1.0.0, v2.1.3, etc.)
            # Only the 'current' symlink is used for static URL resolution.
            dirs[:] = [d for d in dirs if d != "__pycache__" and not _is_version_dir(d)]

            for filename in files:
                if not self._is_static_asset(filename):
                    continue

                full_path = os.path.join(root, filename)
                # Relative path from integrations root, used as the static URL path
                rel_path = os.path.relpath(full_path, str(self.integrations_root))

                # Skip if matches ignore patterns
                if staticfiles_utils.matches_patterns(rel_path, ignore_patterns):
                    continue

                # Yield (relative_path, storage) tuple
                yield rel_path, self.storage


class ComponentStaticFinder(BaseFinder):
    """
    Finds static files in components_data/static/, skipping old versioned
    directories so only files reachable via 'current/' symlinks are collected.

    Without this, Django's FileSystemFinder collects every version directory
    (v1.0.0, v1.0.1, v1.0.2, ...) as separate static files, roughly doubling
    the file count.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.static_root = Path(settings.BASE_DIR) / "components_data" / "static"
        self.storage = FileSystemStorage(location=str(self.static_root))
        self.storage.prefix = ""

    def find(self, path, all=False):
        """Find a requested static file in the components static directory."""
        full_path = self.static_root / path
        if full_path.exists() and full_path.is_file():
            if all:
                return [str(full_path)]
            return str(full_path)
        return [] if all else ""

    def list(self, ignore_patterns):
        """
        List static files, skipping old versioned directories.
        """
        if not self.static_root.exists():
            return

        for root, dirs, files in os.walk(str(self.static_root), followlinks=True):
            # Skip __pycache__ and versioned directories.
            # Only the 'current' symlink is used for static URL resolution.
            dirs[:] = [d for d in dirs if d != "__pycache__" and not _is_version_dir(d)]

            for filename in files:
                full_path = os.path.join(root, filename)
                rel_path = os.path.relpath(full_path, str(self.static_root))

                if staticfiles_utils.matches_patterns(rel_path, ignore_patterns):
                    continue

                yield rel_path, self.storage
