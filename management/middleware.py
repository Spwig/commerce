"""
Management middleware for security and access logging
"""
import time
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.conf import settings
from .models import AccessLog


class ManagementAccessMiddleware(MiddlewareMixin):
    """Middleware to log access to management tools and enforce security"""
    
    def process_request(self, request):
        # Store start time for response time calculation
        request._management_start_time = time.time()
        return None
    
    def process_response(self, request, response):
        # Only log management tool access
        if request.path.startswith('/admin/management/'):
            self.log_access(request, response)
        return response
    
    def log_access(self, request, response):
        """Log access attempt to management tools"""
        try:
            # Calculate response time
            response_time = time.time() - getattr(request, '_management_start_time', time.time())
            
            # Get client IP
            ip_address = self.get_client_ip(request)
            
            # Create access log entry
            AccessLog.objects.create(
                user=request.user if request.user.is_authenticated else None,
                ip_address=ip_address,
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
                path=request.path,
                method=request.method,
                status_code=response.status_code,
                response_time=response_time,
                action=self.get_action_from_path(request.path),
                details={
                    'query_params': dict(request.GET),
                    'is_ajax': request.headers.get('X-Requested-With') == 'XMLHttpRequest',
                    'referer': request.META.get('HTTP_REFERER', ''),
                }
            )
        except Exception as e:
            # Don't let logging errors break the response
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to log management access: {e}")
    
    def get_client_ip(self, request):
        """Get the real client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
        return ip
    
    def get_action_from_path(self, path):
        """Extract action type from request path"""
        if 'query-runner' in path:
            return 'Database Query'
        elif 'dashboard' in path:
            return 'System Monitor'
        elif 'file-manager' in path:
            return 'File Manager'
        elif 'backup' in path:
            return 'Database Backup'
        elif 'upload' in path:
            return 'File Upload'
        elif 'delete' in path:
            return 'File Delete'
        else:
            return 'Management Access'


def management_staff_required(view_func):
    """Decorator to ensure only staff users can access management tools"""
    def check_staff(user):
        return user.is_staff and user.is_active
    
    return user_passes_test(check_staff)(view_func)


def management_superuser_required(view_func):
    """Decorator for sensitive operations requiring superuser access"""
    def check_superuser(user):
        return user.is_superuser and user.is_active
    
    return user_passes_test(check_superuser)(view_func)


class ManagementSecurityMixin:
    """Mixin to add security checks to management admin views"""
    
    def dispatch(self, request, *args, **kwargs):
        # Check if user has permission to access management tools
        if not self.has_management_permission(request.user):
            return HttpResponseForbidden("Access denied to management tools")
        
        # Additional security checks for sensitive operations
        if self.requires_superuser() and not request.user.is_superuser:
            return HttpResponseForbidden("Superuser access required")
        
        return super().dispatch(request, *args, **kwargs)
    
    def has_management_permission(self, user):
        """Check if user has permission to access management tools"""
        return user.is_staff and user.is_active
    
    def requires_superuser(self):
        """Override in subclasses to require superuser for specific views"""
        return False


class DatabaseSecurityMixin(ManagementSecurityMixin):
    """Security mixin for database-related operations"""
    
    def requires_superuser(self):
        """Database operations require superuser access"""
        return True
    
    def dispatch(self, request, *args, **kwargs):
        # Additional database-specific security checks
        if hasattr(settings, 'MANAGEMENT_DISABLE_DB_ACCESS') and settings.MANAGEMENT_DISABLE_DB_ACCESS:
            return HttpResponseForbidden("Database access is disabled")
        
        return super().dispatch(request, *args, **kwargs)


class FileSecurityMixin(ManagementSecurityMixin):
    """Security mixin for file operations"""
    
    def dispatch(self, request, *args, **kwargs):
        # Check if file operations are enabled
        if hasattr(settings, 'MANAGEMENT_DISABLE_FILE_OPS') and settings.MANAGEMENT_DISABLE_FILE_OPS:
            return HttpResponseForbidden("File operations are disabled")
        
        return super().dispatch(request, *args, **kwargs)
    
    def is_safe_path(self, path):
        """Check if the path is safe for file operations"""
        import os
        
        # Ensure path is within allowed directories
        allowed_dirs = [
            settings.MEDIA_ROOT,
            settings.STATIC_ROOT,
        ]
        
        abs_path = os.path.abspath(path)
        for allowed_dir in allowed_dirs:
            if allowed_dir and abs_path.startswith(os.path.abspath(allowed_dir)):
                return True
        
        return False


class RateLimitMixin:
    """Mixin to add rate limiting to management operations"""
    
    def check_rate_limit(self, request, operation_type):
        """Check if user has exceeded rate limits for operation type"""
        from django.core.cache import cache
        
        # Create cache key based on user and operation
        cache_key = f"mgmt_rate_limit_{request.user.id}_{operation_type}"
        
        # Get current count
        current_count = cache.get(cache_key, 0)
        
        # Define rate limits per operation type
        rate_limits = {
            'query': 10,  # 10 queries per minute
            'backup': 3,  # 3 backups per hour
            'file_upload': 20,  # 20 uploads per minute
            'file_delete': 10,  # 10 deletions per minute
        }
        
        limit = rate_limits.get(operation_type, 5)
        
        if current_count >= limit:
            return False
        
        # Increment counter
        timeout = 3600 if operation_type == 'backup' else 60  # 1 hour for backup, 1 minute for others
        cache.set(cache_key, current_count + 1, timeout)
        
        return True