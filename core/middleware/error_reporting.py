"""
Error Reporting Middleware

Captures unhandled Python exceptions (500 errors) and buffers them
as ErrorReport records for batch transmission to Spwig.

Must be placed near the end of MIDDLEWARE to catch all exceptions
not handled by other middleware.
"""

import logging
import platform
import traceback

import django
from django.conf import settings
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin

from core.error_reporting.sanitizer import DataSanitizer

logger = logging.getLogger(__name__)

SETTINGS_CACHE_KEY = 'error_reporting:site_settings'
SETTINGS_CACHE_TTL = 30  # seconds


class ErrorReportingMiddleware(MiddlewareMixin):
    """Captures unhandled exceptions and buffers sanitized error reports."""

    def process_exception(self, request, exception):
        """Called by Django when a view raises an unhandled exception."""
        try:
            self._capture_error(request, exception)
        except Exception:
            # Never let error reporting itself cause a secondary failure
            pass
        return None

    def _capture_error(self, request, exception):
        from core.error_reporting.buffer import buffer_python_error

        settings_obj = self._get_settings()
        if not settings_obj:
            return

        tb_string = ''.join(
            traceback.format_exception(type(exception), exception, exception.__traceback__)
        )
        sanitized_tb = DataSanitizer.sanitize_traceback(tb_string)

        error_data = {
            'exception_type': f"{type(exception).__module__}.{type(exception).__qualname__}",
            'exception_message': DataSanitizer.sanitize_traceback(str(exception)),
            'traceback': sanitized_tb,
            'request_url': DataSanitizer.sanitize_url(request.build_absolute_uri()),
            'request_method': request.method,
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'safe_headers': DataSanitizer.sanitize_headers(
                {k: v for k, v in request.META.items() if k.startswith('HTTP_')}
            ),
            'django_version': django.get_version(),
            'platform_version': getattr(settings, 'PLATFORM_VERSION', 'unknown'),
            'python_version': platform.python_version(),
            'timestamp': django.utils.timezone.now().isoformat(),
        }

        status = 'pending' if settings_obj.error_reporting_enabled else 'held'
        buffer_python_error(error_data, status=status)

    def _get_settings(self):
        """Get SiteSettings with short cache to avoid DB hit on every exception."""
        settings_obj = cache.get(SETTINGS_CACHE_KEY)
        if settings_obj is None:
            from core.models import SiteSettings
            try:
                settings_obj = SiteSettings.get_settings()
            except Exception:
                return None
            if settings_obj:
                cache.set(SETTINGS_CACHE_KEY, settings_obj, SETTINGS_CACHE_TTL)
        return settings_obj
