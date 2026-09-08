"""
Component Static File Serving View

Serves static files (JavaScript, CSS, images, etc.) from payment provider
component directories. Enables providers to ship their own frontend assets
for checkout integration without requiring core code changes.

This view implements secure file serving with:
- Directory traversal prevention
- Path validation and sanitization
- Component verification through ComponentRegistry
- Proper MIME type detection
- File existence checks

URL Pattern: /components/payments/{provider_slug}/current/{filename}
Example: /components/payments/airwallex/current/checkout-handler.js
"""

import logging
import mimetypes
from pathlib import Path, PurePosixPath

from django.http import FileResponse, Http404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_control

from component_updates.models import ComponentRegistry

logger = logging.getLogger(__name__)


@method_decorator(
    # The "current" segment is a mutable pointer: a provider update can replace
    # it while keeping the same handler filename. Force revalidation so a client
    # never runs a stale handler against a freshly installed backend.
    cache_control(no_cache=True, must_revalidate=True),
    name="dispatch",
)
class ComponentStaticFileView(View):
    """
    Serve static files from payment provider component directories.

    This view enables payment providers to ship their own JavaScript
    handlers, stylesheets, and other assets as part of their component
    package. Files are served dynamically based on the provider's current
    version symlink.

    Security measures:
    - Validates provider exists in ComponentRegistry
    - Prevents directory traversal attacks
    - Ensures file is within component directory
    - Only serves the exact frontend files the manifest declares, never
      the package's Python entry point or any other undeclared source
    - Only serves files, not directories
    - Returns 404 for invalid paths

    Cache: The "current" route is mutable, so responses are marked
    no-cache/must-revalidate to avoid serving a stale handler after an update.
    """

    @staticmethod
    def _declared_frontend_files(manifest):
        """Return the set of filenames the manifest publishes as frontend assets.

        Providers must name the files they intend to expose (checkout handler,
        stylesheets, logo). Backend sources such as the required Python entry
        point are never listed here and therefore stay private.
        """
        files = set()
        frontend = manifest.get("frontend") or {}

        handler = frontend.get("checkout_handler")
        if isinstance(handler, str):
            files.add(handler)

        for key in ("assets", "styles", "stylesheets", "scripts"):
            value = frontend.get(key)
            if isinstance(value, str):
                files.add(value)
            elif isinstance(value, list):
                files.update(item for item in value if isinstance(item, str))
            elif isinstance(value, dict):
                for group in value.values():
                    if isinstance(group, list):
                        files.update(item for item in group if isinstance(item, str))

        logo = manifest.get("logo")
        if isinstance(logo, dict) and isinstance(logo.get("file"), str):
            files.add(logo["file"])
        elif isinstance(logo, str):
            files.add(logo)

        return {str(PurePosixPath(f.lstrip("/"))) for f in files if f}

    @staticmethod
    def _entry_point_paths(manifest):
        """Normalized paths of the package's Python entry point.

        The loader accepts the entry point with or without a ``.py`` suffix
        (see ``payment_providers.providers.loader``), so exclude both spellings
        even if a manifest were to (mis)declare it as a frontend asset.
        """
        entry_point = manifest.get("entry_point") or "provider"
        if not isinstance(entry_point, str):
            return set()
        entry_point = entry_point.lstrip("/")
        variants = {entry_point}
        if entry_point.endswith(".py"):
            variants.add(entry_point[:-3])
        else:
            variants.add(f"{entry_point}.py")
        return {str(PurePosixPath(v)) for v in variants if v}

    @classmethod
    def _is_allowed_asset(cls, filename, manifest):
        """Allow only the exact files the manifest declares as frontend assets.

        Directory-level allowances are deliberately avoided: a provider could
        place a nested Python entry point (e.g. ``static/provider.py``) or other
        backend sources inside an otherwise front-endy directory, so nothing is
        servable unless the manifest names it explicitly. The entry point is
        excluded even if a manifest declares it.
        """
        normalized = str(PurePosixPath(filename))
        declared = cls._declared_frontend_files(manifest) - cls._entry_point_paths(manifest)
        return normalized in declared

    def get(self, request, provider_slug, filename):
        """
        Serve a static file from a provider component directory.

        Args:
            request: Django HttpRequest
            provider_slug: Provider identifier (e.g., 'airwallex', 'stripe')
            filename: Relative path to file within component directory
                     (e.g., 'checkout-handler.js', 'assets/logo.png')

        Returns:
            FileResponse with appropriate content-type header

        Raises:
            Http404: If provider not found, file not found, or invalid path
        """
        # Security: Prevent directory traversal
        if ".." in filename or filename.startswith("/"):
            logger.warning(f"Directory traversal attempt blocked: {filename}")
            raise Http404("Invalid filename")

        # Additional security: Check for suspicious patterns
        suspicious_patterns = ["../", "..\\", "%2e%2e", "%252e"]
        if any(pattern in filename.lower() for pattern in suspicious_patterns):
            logger.warning(f"Suspicious path pattern detected: {filename}")
            raise Http404("Invalid filename")

        # Get provider component from registry
        try:
            component = ComponentRegistry.objects.get(
                slug=provider_slug, component_type="payment_provider"
            )
        except ComponentRegistry.DoesNotExist:
            logger.warning(f"Provider not found: {provider_slug}")
            raise Http404("Provider not found")

        # Security: only serve files the manifest explicitly declares as
        # frontend assets. This keeps the backend Python entry point and every
        # other undeclared package source unreachable.
        manifest = component.get_manifest()
        if not manifest or not self._is_allowed_asset(filename, manifest):
            logger.warning(f"Blocked non-asset request '{filename}' for provider {provider_slug}")
            raise Http404("File not found")

        # Build file path using component's installed path
        component_path = component.installed_path
        if not component_path:
            logger.error(f"No installed path for provider: {provider_slug}")
            raise Http404("Provider not configured")

        file_path = Path(component_path) / filename

        # Security: Resolve paths and ensure file is within component directory
        try:
            file_path_resolved = file_path.resolve()
            component_path_resolved = Path(component_path).resolve()

            if not file_path_resolved.is_relative_to(component_path_resolved):
                logger.warning(
                    f"Path escape attempt: {filename} "
                    f"resolved outside component directory for {provider_slug}"
                )
                raise Http404("Access denied")
        except (OSError, ValueError) as e:
            logger.error(f"Path resolution error for {filename}: {e}")
            raise Http404("Invalid path")

        # Check file exists and is actually a file (not a directory)
        if not file_path_resolved.is_file():
            logger.info(f"File not found: {filename} in {provider_slug} component")
            raise Http404("File not found")

        # Determine content type based on file extension
        content_type, encoding = mimetypes.guess_type(str(file_path_resolved))

        # Default to application/octet-stream if type unknown
        if not content_type:
            content_type = "application/octet-stream"
            logger.debug(f"Unknown MIME type for {filename}, using default")

        # Log successful file serving (debug level to avoid log spam)
        logger.debug(f"Serving {filename} from {provider_slug} as {content_type}")

        # Serve the file
        try:
            response = FileResponse(open(file_path_resolved, "rb"), content_type=content_type)  # noqa: SIM115  # FileResponse takes ownership + closes on stream end

            # Add Content-Encoding if detected
            if encoding:
                response["Content-Encoding"] = encoding

            return response
        except OSError as e:
            logger.error(f"Error reading file {filename}: {e}")
            raise Http404("Error reading file")
