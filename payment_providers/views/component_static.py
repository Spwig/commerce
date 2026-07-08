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
from django.http import FileResponse, Http404
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from pathlib import Path
from component_updates.models import ComponentRegistry
import mimetypes
import logging

logger = logging.getLogger(__name__)


@method_decorator(cache_control(max_age=3600), name='dispatch')  # Cache for 1 hour
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
    - Only serves files, not directories
    - Returns 404 for invalid paths

    Cache: Files are cached for 1 hour via @cache_control decorator
    """

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
        if '..' in filename or filename.startswith('/'):
            logger.warning(f"Directory traversal attempt blocked: {filename}")
            raise Http404("Invalid filename")

        # Additional security: Check for suspicious patterns
        suspicious_patterns = ['../', '..\\', '%2e%2e', '%252e']
        if any(pattern in filename.lower() for pattern in suspicious_patterns):
            logger.warning(f"Suspicious path pattern detected: {filename}")
            raise Http404("Invalid filename")

        # Get provider component from registry
        try:
            component = ComponentRegistry.objects.get(
                slug=provider_slug,
                component_type='payment_provider'
            )
        except ComponentRegistry.DoesNotExist:
            logger.warning(f"Provider not found: {provider_slug}")
            raise Http404("Provider not found")

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

            if not str(file_path_resolved).startswith(str(component_path_resolved)):
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
            content_type = 'application/octet-stream'
            logger.debug(f"Unknown MIME type for {filename}, using default")

        # Log successful file serving (debug level to avoid log spam)
        logger.debug(f"Serving {filename} from {provider_slug} as {content_type}")

        # Serve the file
        try:
            response = FileResponse(
                open(file_path_resolved, 'rb'),
                content_type=content_type
            )

            # Add Content-Encoding if detected
            if encoding:
                response['Content-Encoding'] = encoding

            return response
        except IOError as e:
            logger.error(f"Error reading file {filename}: {e}")
            raise Http404("Error reading file")
