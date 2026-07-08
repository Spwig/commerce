"""
System Status Service

Provides health checks and status collection for:
- Database (PostgreSQL)
- Redis
- Celery workers
- SSL certificates
- Disk usage
- Version info

Results are cached in Redis with 60-second TTL for dashboard display.
"""

import logging
import os
import shutil
import socket
import ssl
import subprocess
from datetime import datetime, timedelta, timezone as dt_timezone
from typing import Any, Dict, Optional

from django.conf import settings
from django.core.cache import cache
from django.db import connection
from django.utils import timezone

logger = logging.getLogger(__name__)

# Cache keys and TTL
SYSTEM_STATUS_CACHE_KEY = 'system_status_snapshot'
SYSTEM_STATUS_CACHE_TTL = 60  # seconds


class SystemStatusService:
    """
    Service for collecting system health and status information.

    Methods are designed to be called individually or as a batch.
    Results are cached to avoid repeated expensive checks.
    """

    @classmethod
    def get_cached_status(cls) -> Optional[Dict[str, Any]]:
        """Get cached status if available"""
        return cache.get(SYSTEM_STATUS_CACHE_KEY)

    @classmethod
    def collect_all_status(cls) -> Dict[str, Any]:
        """
        Collect all status information and cache it.
        Called by the periodic Celery task.
        """
        status = {
            'checked_at': timezone.now().isoformat(),
            'database': cls.check_database(),
            'redis': cls.check_redis(),
            'celery': cls.check_celery(),
            'ssl': cls.check_ssl(),
            'disk': cls.check_disk(),
            'version': cls.get_version_info(),
            'maintenance': cls.check_maintenance_mode(),
        }

        # Cache the result
        cache.set(SYSTEM_STATUS_CACHE_KEY, status, SYSTEM_STATUS_CACHE_TTL)

        return status

    @classmethod
    def check_database(cls) -> Dict[str, Any]:
        """Check PostgreSQL database health"""
        result = {
            'healthy': False,
            'name': '',
            'host': '',
            'size': None,
            'connections': None,
            'error': None,
        }

        try:
            # Get database settings
            db_settings = settings.DATABASES.get('default', {})
            result['name'] = db_settings.get('NAME', 'unknown')
            result['host'] = db_settings.get('HOST', 'localhost')

            # Test connection
            with connection.cursor() as cursor:
                # Simple connectivity test
                cursor.execute("SELECT 1")
                cursor.fetchone()

                # Get database size
                try:
                    cursor.execute("""
                        SELECT pg_database_size(current_database())
                    """)
                    size_bytes = cursor.fetchone()[0]
                    result['size'] = size_bytes
                    result['size_display'] = cls._format_bytes(size_bytes)
                except Exception:
                    pass

                # Get active connections
                try:
                    cursor.execute("""
                        SELECT count(*) FROM pg_stat_activity
                        WHERE datname = current_database()
                    """)
                    result['connections'] = cursor.fetchone()[0]
                except Exception:
                    pass

            result['healthy'] = True

        except Exception as e:
            result['error'] = str(e)
            logger.error(f"Database health check failed: {e}")

        return result

    @classmethod
    def check_redis(cls) -> Dict[str, Any]:
        """Check Redis health"""
        result = {
            'healthy': False,
            'host': '',
            'memory_used': None,
            'memory_used_display': None,
            'connected_clients': None,
            'error': None,
        }

        try:
            import redis as redis_lib

            # Get Redis URL from settings
            redis_url = getattr(settings, 'CELERY_BROKER_URL', None) or \
                        getattr(settings, 'REDIS_URL', 'redis://localhost:6379/0')

            result['host'] = redis_url.split('@')[-1].split('/')[0] if '@' in redis_url else \
                            redis_url.replace('redis://', '').split('/')[0]

            # Connect and ping
            client = redis_lib.from_url(redis_url)
            client.ping()

            # Get memory info
            info = client.info('memory')
            result['memory_used'] = info.get('used_memory', 0)
            result['memory_used_display'] = cls._format_bytes(result['memory_used'])

            # Get client info
            client_info = client.info('clients')
            result['connected_clients'] = client_info.get('connected_clients', 0)

            result['healthy'] = True

        except ImportError:
            result['error'] = 'redis package not installed'
        except Exception as e:
            result['error'] = str(e)
            logger.error(f"Redis health check failed: {e}")

        return result

    @classmethod
    def check_celery(cls) -> Dict[str, Any]:
        """Check Celery workers health"""
        result = {
            'healthy': False,
            'workers': [],
            'active_workers': 0,
            'queued_tasks': 0,
            'error': None,
        }

        try:
            from celery import current_app

            # Get active workers via inspect
            inspect = current_app.control.inspect(timeout=2.0)

            # Get ping response from workers
            ping_response = inspect.ping()
            if ping_response:
                for worker_name, response in ping_response.items():
                    result['workers'].append({
                        'name': worker_name,
                        'status': 'ok' if response.get('ok') == 'pong' else 'error',
                    })
                result['active_workers'] = len(result['workers'])

            # Get queued tasks count
            try:
                import redis as redis_lib
                redis_url = getattr(settings, 'CELERY_BROKER_URL', 'redis://localhost:6379/0')
                client = redis_lib.from_url(redis_url)
                # Default Celery queue
                result['queued_tasks'] = client.llen('celery')
            except Exception:
                pass

            result['healthy'] = result['active_workers'] > 0

        except Exception as e:
            result['error'] = str(e)
            logger.error(f"Celery health check failed: {e}")

        return result

    @classmethod
    def check_ssl(cls) -> Dict[str, Any]:
        """Check SSL certificate status using DomainConfiguration model."""
        result = {
            'valid': False,
            'domain': '',
            'issuer': '',
            'expiry_date': None,
            'days_remaining': None,
            'error': None,
        }

        try:
            from domain_ssl.models import DomainConfiguration
            config = DomainConfiguration.objects.filter(pk=1).first()

            if not config or config.ssl_mode == DomainConfiguration.SSLMode.NONE:
                result['error'] = 'SSL not configured'
                return result

            # For externally managed SSL, verify upstream
            if config.ssl_mode == DomainConfiguration.SSLMode.MANAGED_EXTERNALLY:
                if not config.domain:
                    result['error'] = 'No domain configured'
                    return result

                from domain_ssl.services.ssl_service import verify_external_ssl
                valid, info = verify_external_ssl(config.domain, timeout=5)
                result['valid'] = valid
                result['domain'] = info.get('domain', config.domain)
                result['issuer'] = info.get('issuer', '')
                if info.get('expires_at'):
                    result['expiry_date'] = info['expires_at'].isoformat()
                    result['days_remaining'] = (
                        info['expires_at'] - datetime.now(dt_timezone.utc)
                    ).days
                if not valid:
                    result['error'] = info.get('error', 'External SSL verification failed')
                return result

            # For locally managed SSL, use model cert metadata if available
            if config.cert_expires_at:
                result['domain'] = config.cert_domain or config.domain
                result['issuer'] = config.cert_issuer
                result['expiry_date'] = config.cert_expires_at.isoformat()
                days_remaining = (
                    config.cert_expires_at - datetime.now(dt_timezone.utc)
                ).days
                result['days_remaining'] = days_remaining
                result['valid'] = days_remaining > 0
                return result

            # Fallback: try reading local cert files
            cert_paths = [
                '/opt/spwig/certs/fullchain.pem',
                '/etc/letsencrypt/live/*/fullchain.pem',
                os.path.join(settings.BASE_DIR, 'deploy', 'certs', 'fullchain.pem'),
            ]

            cert_path = None
            for path in cert_paths:
                if '*' in path:
                    import glob
                    matches = glob.glob(path)
                    if matches:
                        cert_path = matches[0]
                        break
                elif os.path.exists(path):
                    cert_path = path
                    break

            if not cert_path:
                result['error'] = 'No SSL certificate found'
                return result

            try:
                output = subprocess.check_output(
                    ['openssl', 'x509', '-in', cert_path, '-noout',
                     '-subject', '-issuer', '-enddate'],
                    stderr=subprocess.STDOUT, text=True
                )
                import re
                _kv_re = re.compile(r'(?:^|,\s*)(\w+)\s*=\s*([^,\n]+)')
                for line in output.strip().split('\n'):
                    if line.startswith('subject='):
                        content = line.split('=', 1)[1]
                        kvs = dict(_kv_re.findall(content))
                        result['domain'] = kvs.get('CN', '').strip()
                    elif line.startswith('issuer='):
                        content = line.split('=', 1)[1]
                        kvs = dict(_kv_re.findall(content))
                        result['issuer'] = (
                            kvs.get('O', '').strip()
                            or kvs.get('CN', '').strip()
                        )
                    elif line.startswith('notAfter='):
                        date_str = line.split('=', 1)[1].strip()
                        clean_date = date_str.replace(' GMT', '').replace(' UTC', '')
                        expiry = datetime.strptime(clean_date, '%b %d %H:%M:%S %Y')
                        result['expiry_date'] = expiry.isoformat()
                        result['days_remaining'] = (expiry - datetime.utcnow()).days
                        result['valid'] = result['days_remaining'] > 0
            except Exception as e:
                result['error'] = f'Failed to parse certificate: {e}'

        except Exception as e:
            result['error'] = str(e)
            logger.error(f"SSL check failed: {e}")

        return result

    @classmethod
    def check_disk(cls) -> Dict[str, Any]:
        """Check disk usage"""
        result = {
            'total': None,
            'used': None,
            'free': None,
            'percent': None,
            'total_display': None,
            'used_display': None,
            'free_display': None,
            'error': None,
        }

        try:
            # Check the main data directory
            check_path = getattr(settings, 'MEDIA_ROOT', '/') or '/'

            usage = shutil.disk_usage(check_path)
            result['total'] = usage.total
            result['used'] = usage.used
            result['free'] = usage.free
            result['percent'] = round((usage.used / usage.total) * 100, 1)

            result['total_display'] = cls._format_bytes(usage.total)
            result['used_display'] = cls._format_bytes(usage.used)
            result['free_display'] = cls._format_bytes(usage.free)

        except Exception as e:
            result['error'] = str(e)
            logger.error(f"Disk check failed: {e}")

        return result

    @classmethod
    def get_version_info(cls) -> Dict[str, Any]:
        """Get current version and check for updates"""
        result = {
            'current': 'unknown',
            'available': None,
            'update_available': False,
            'changelog': None,
            'error': None,
        }

        try:
            # Try to read version from core module first (primary source)
            try:
                import core
                result['current'] = getattr(core, '__version__', None)
            except (ImportError, AttributeError):
                result['current'] = None

            # Fallback to VERSION file
            if not result['current']:
                version_file = os.path.join(settings.BASE_DIR, 'VERSION')
                if os.path.exists(version_file):
                    with open(version_file, 'r') as f:
                        result['current'] = f.read().strip()

            # Final fallback to environment variable
            if not result['current']:
                result['current'] = os.environ.get('SPWIG_VERSION', 'dev')

            # Check for updates using PlatformUpdateService (authenticated)
            try:
                from component_updates.services import PlatformUpdateService
                from component_updates.models import UpdateServerConfig

                config = UpdateServerConfig.get_instance()
                if config.server_url and config.license_key:
                    service = PlatformUpdateService()
                    update_info = service.check_for_update(channel='stable')

                    result['update_available'] = update_info.get('update_available', False)
                    if result['update_available']:
                        result['available'] = update_info.get('latest_version')
                        result['changelog'] = update_info.get('changelog')
                else:
                    logger.debug("Update server not configured, skipping update check")
            except Exception as e:
                logger.debug(f"Failed to check for updates: {e}")

        except Exception as e:
            result['error'] = str(e)
            logger.error(f"Version check failed: {e}")

        return result

    @classmethod
    def check_maintenance_mode(cls) -> Dict[str, Any]:
        """Check if maintenance mode is enabled"""
        result = {
            'enabled': False,
            'reason': '',
        }

        try:
            # Check cache for maintenance mode flag
            maintenance = cache.get('maintenance_mode', {})
            if isinstance(maintenance, dict):
                result['enabled'] = maintenance.get('enabled', False)
                result['reason'] = maintenance.get('reason', '')
            elif maintenance:
                result['enabled'] = True

            # Also check environment variable
            if os.environ.get('MAINTENANCE_MODE', '').lower() in ('true', '1', 'yes'):
                result['enabled'] = True

        except Exception as e:
            logger.error(f"Maintenance mode check failed: {e}")

        return result

    @classmethod
    def toggle_maintenance_mode(cls, enabled: bool, reason: str = '') -> bool:
        """Toggle maintenance mode on/off.

        Writes to SiteSettings.maintenance_mode (the field the maintenance
        middleware actually reads) and invalidates the cache key it uses.
        Also updates the SystemStatus model for the admin dashboard.
        """
        try:
            from core.models import SiteSettings
            SiteSettings.objects.filter(pk=1).update(maintenance_mode=enabled)
            cache.delete('maintenance_mode_status')

            # Also update the SystemStatus model
            from management.models import SystemStatus
            status = SystemStatus.get_instance()
            status.maintenance_mode = enabled
            status.maintenance_reason = reason
            status.save(update_fields=['maintenance_mode', 'maintenance_reason'])

            return True
        except Exception as e:
            logger.error(f"Failed to toggle maintenance mode: {e}")
            return False

    @classmethod
    def update_system_status_model(cls, status_data: Dict[str, Any]) -> None:
        """Update the SystemStatus model with collected data"""
        try:
            from management.models import SystemStatus

            obj = SystemStatus.get_instance()

            # Database
            db_data = status_data.get('database', {})
            obj.db_healthy = db_data.get('healthy', False)
            obj.db_details = db_data

            # Redis
            redis_data = status_data.get('redis', {})
            obj.redis_healthy = redis_data.get('healthy', False)
            obj.redis_details = redis_data

            # Celery
            celery_data = status_data.get('celery', {})
            obj.celery_healthy = celery_data.get('healthy', False)
            obj.celery_details = celery_data

            # SSL
            ssl_data = status_data.get('ssl', {})
            obj.ssl_valid = ssl_data.get('valid', False)
            obj.ssl_domain = ssl_data.get('domain', '')
            if ssl_data.get('expiry_date'):
                try:
                    obj.ssl_expiry_date = datetime.fromisoformat(
                        ssl_data['expiry_date'].replace('Z', '+00:00')
                    )
                except Exception:
                    pass
            obj.ssl_days_remaining = ssl_data.get('days_remaining')

            # Version
            version_data = status_data.get('version', {})
            obj.current_version = version_data.get('current') or ''
            obj.available_version = version_data.get('available') or ''
            obj.update_available = version_data.get('update_available', False)

            # Maintenance
            maintenance_data = status_data.get('maintenance', {})
            obj.maintenance_mode = maintenance_data.get('enabled', False)
            obj.maintenance_reason = maintenance_data.get('reason', '')

            # Disk
            disk_data = status_data.get('disk', {})
            obj.disk_total = disk_data.get('total')
            obj.disk_used = disk_data.get('used')
            obj.disk_free = disk_data.get('free')
            obj.disk_percent = disk_data.get('percent')

            obj.save()

        except Exception as e:
            logger.error(f"Failed to update SystemStatus model: {e}")

    @staticmethod
    def _format_bytes(size: int) -> str:
        """Format bytes to human-readable string"""
        if size is None:
            return "Unknown"
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
