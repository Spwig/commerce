"""
Subpath Middleware

Handles URL subpath configurations when Spwig runs under a path prefix
like /shop/ on an existing domain.

This middleware:
1. Reads X-Script-Name header from reverse proxy
2. Sets SCRIPT_NAME on the request for Django URL routing
3. Adjusts request.path_info for proper URL matching

Configuration:
    Set SUBPATH in environment (e.g., SUBPATH=/shop)
    Or let the reverse proxy set X-Script-Name header

Example nginx config:
    location /shop/ {
        proxy_set_header X-Script-Name /shop;
        proxy_pass http://spwig:8080/;
    }
"""

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class SubpathMiddleware(MiddlewareMixin):
    """
    Middleware to handle running Django under a URL subpath.

    When Spwig is deployed at example.com/shop/, this middleware ensures:
    - URLs are generated with the /shop prefix
    - Incoming requests are properly routed
    - Static/media URLs include the prefix

    Priority: Should be one of the first middleware in the chain.
    """

    def process_request(self, request):
        """
        Process incoming request to set SCRIPT_NAME from header or settings.
        """
        # Check for X-Script-Name header from reverse proxy
        script_name = request.META.get('HTTP_X_SCRIPT_NAME', '')

        # Fall back to settings if no header
        if not script_name:
            script_name = getattr(settings, 'FORCE_SCRIPT_NAME', '') or ''

        # Normalize: ensure starts with / but doesn't end with /
        if script_name:
            script_name = '/' + script_name.strip('/')

        if script_name:
            # Set SCRIPT_NAME for Django's URL generation
            request.META['SCRIPT_NAME'] = script_name

            # Adjust PATH_INFO if it starts with the script name
            # This handles cases where the proxy didn't strip the prefix
            path_info = request.META.get('PATH_INFO', '/')
            if path_info.startswith(script_name):
                request.META['PATH_INFO'] = path_info[len(script_name):] or '/'

            # Store for templates
            request.script_name = script_name
        else:
            request.script_name = ''

        return None

    def process_response(self, request, response):
        """
        Ensure Location headers in redirects include the script name.
        """
        # Django should handle this automatically via SCRIPT_NAME,
        # but we double-check for edge cases
        if response.status_code in (301, 302, 303, 307, 308):
            location = response.get('Location', '')
            script_name = getattr(request, 'script_name', '')

            # If location is absolute path without script name, add it
            if script_name and location.startswith('/') and not location.startswith(script_name):
                # Don't modify if it's a full URL
                if not location.startswith(('http://', 'https://')):
                    response['Location'] = script_name + location

        return response


def get_subpath():
    """
    Utility function to get the current subpath setting.

    Returns:
        str: The subpath prefix (e.g., '/shop') or empty string if none.
    """
    subpath = getattr(settings, 'FORCE_SCRIPT_NAME', '') or ''
    if subpath:
        return '/' + subpath.strip('/')
    return ''


def build_absolute_uri(request, path):
    """
    Build an absolute URI that includes the subpath.

    Args:
        request: The Django request object
        path: The path to build URI for (e.g., '/products/')

    Returns:
        str: Full URI with subpath (e.g., 'https://example.com/shop/products/')
    """
    script_name = getattr(request, 'script_name', '')

    # Build the full path
    if script_name and not path.startswith(script_name):
        full_path = script_name + path
    else:
        full_path = path

    # Get scheme and host
    scheme = request.scheme
    host = request.get_host()

    return f"{scheme}://{host}{full_path}"
