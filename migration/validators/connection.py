"""
Pre-flight connection and system checks before migration
"""
import requests
from django.conf import settings
import psutil
import logging

logger = logging.getLogger(__name__)


class PreFlightChecker:
    """Run pre-flight checks before starting migration"""

    def __init__(self, migration_job):
        self.job = migration_job
        self.config = migration_job.connection_config
        self.checks = []

    def run_all_checks(self):
        """
        Run all pre-flight checks

        Returns:
            dict: {
                'critical_failures': list,
                'warnings': list,
                'info': list,
                'all_passed': bool
            }
        """
        results = {
            'critical_failures': [],
            'warnings': [],
            'info': [],
            'all_passed': True
        }

        # Run checks based on platform
        if self.job.platform == 'woocommerce' and self.job.method == 'api':
            checks = [
                self.check_api_connection(),
                self.check_api_permissions(),
                self.check_api_version(),
                self.check_disk_space(),
                self.check_database(),
                self.estimate_duration(),
            ]
        elif self.job.platform == 'woocommerce' and self.job.method == 'csv':
            checks = [
                self.check_disk_space(),
                self.check_database(),
            ]
        elif self.job.platform == 'magento' and self.job.method == 'api':
            from migration.validators.magento_connection import MagentoPreFlightChecker
            checker = MagentoPreFlightChecker(self.job)
            return checker.run_all_checks()
        else:
            checks = []

        # Categorize results
        for check in checks:
            if check['status'] == 'critical':
                results['critical_failures'].append(check)
                results['all_passed'] = False
            elif check['status'] == 'warning':
                results['warnings'].append(check)
            else:
                results['info'].append(check)

        return results

    def check_api_connection(self):
        """Test WooCommerce API connection"""
        try:
            url = f"{self.config['store_url'].rstrip('/')}/wp-json/wc/v3/system_status"
            auth = (self.config['consumer_key'], self.config['consumer_secret'])

            response = requests.get(url, auth=auth, timeout=10)

            if response.status_code == 200:
                data = response.json()
                return {
                    'name': 'API Connection',
                    'status': 'success',
                    'message': 'Successfully connected to WooCommerce API',
                    'details': {
                        'environment': data.get('environment', {}),
                        'database': data.get('database', {})
                    }
                }
            elif response.status_code == 401:
                return {
                    'name': 'API Connection',
                    'status': 'critical',
                    'message': 'Authentication failed. Check your API credentials.',
                    'details': {'status_code': 401}
                }
            elif response.status_code == 404:
                return {
                    'name': 'API Connection',
                    'status': 'critical',
                    'message': 'WooCommerce REST API not found. Ensure WooCommerce is installed.',
                    'details': {'status_code': 404}
                }
            else:
                return {
                    'name': 'API Connection',
                    'status': 'critical',
                    'message': f'API connection failed with status {response.status_code}',
                    'details': {'status_code': response.status_code}
                }

        except requests.exceptions.Timeout:
            return {
                'name': 'API Connection',
                'status': 'warning',
                'message': 'API connection timed out. Migration may be slow.',
                'details': {}
            }
        except requests.exceptions.ConnectionError:
            return {
                'name': 'API Connection',
                'status': 'critical',
                'message': 'Could not connect to store. Check store URL.',
                'details': {}
            }
        except Exception as e:
            return {
                'name': 'API Connection',
                'status': 'critical',
                'message': f'Connection error: {str(e)}',
                'details': {}
            }

    def check_api_permissions(self):
        """Verify API has read permissions for required endpoints"""
        try:
            auth = (self.config['consumer_key'], self.config['consumer_secret'])
            base_url = f"{self.config['store_url'].rstrip('/')}/wp-json/wc/v3"

            # Test endpoints (following WooCommerce REST API v3 docs)
            # See: https://woocommerce.github.io/woocommerce-rest-api-docs/
            endpoints = [
                ('products', 'Products'),
                ('customers', 'Customers'),
                ('orders', 'Orders'),
                ('products/categories', 'Categories'),  # Correct: products/categories not product_categories
            ]

            accessible = []
            not_accessible = []

            for endpoint, name in endpoints:
                try:
                    response = requests.get(
                        f"{base_url}/{endpoint}",
                        auth=auth,
                        params={'per_page': 1},
                        timeout=5
                    )

                    if response.status_code == 200:
                        accessible.append(name)
                    else:
                        not_accessible.append(name)
                except:
                    not_accessible.append(name)

            if len(accessible) == len(endpoints):
                return {
                    'name': 'API Permissions',
                    'status': 'success',
                    'message': 'API has read access to all required endpoints',
                    'details': {'accessible': accessible}
                }
            elif len(accessible) > 0:
                return {
                    'name': 'API Permissions',
                    'status': 'warning',
                    'message': f'API has limited access. Cannot access: {", ".join(not_accessible)}',
                    'details': {
                        'accessible': accessible,
                        'not_accessible': not_accessible
                    }
                }
            else:
                return {
                    'name': 'API Permissions',
                    'status': 'critical',
                    'message': 'API does not have read permissions',
                    'details': {'not_accessible': not_accessible}
                }

        except Exception as e:
            return {
                'name': 'API Permissions',
                'status': 'warning',
                'message': f'Could not verify permissions: {str(e)}',
                'details': {}
            }

    def check_api_version(self):
        """Check WooCommerce API version"""
        try:
            url = f"{self.config['store_url'].rstrip('/')}/wp-json/wc/v3"
            auth = (self.config['consumer_key'], self.config['consumer_secret'])

            response = requests.get(url, auth=auth, timeout=10)

            if response.status_code == 200:
                data = response.json()
                namespace = data.get('namespace', '')

                if 'wc/v3' in namespace:
                    return {
                        'name': 'API Version',
                        'status': 'success',
                        'message': 'WooCommerce REST API v3 detected',
                        'details': {'namespace': namespace}
                    }
                else:
                    return {
                        'name': 'API Version',
                        'status': 'warning',
                        'message': f'Unexpected API version: {namespace}',
                        'details': {'namespace': namespace}
                    }
            else:
                return {
                    'name': 'API Version',
                    'status': 'warning',
                    'message': 'Could not detect API version',
                    'details': {}
                }

        except Exception as e:
            return {
                'name': 'API Version',
                'status': 'info',
                'message': f'Could not check API version: {str(e)}',
                'details': {}
            }

    def check_disk_space(self):
        """Check available disk space for media files"""
        try:
            media_root = settings.MEDIA_ROOT
            stat = psutil.disk_usage(str(media_root))

            # Estimate: 500KB per product image × 3 (original + webp + thumbnails) × 5 images per product
            estimated_products = 1000  # Conservative estimate
            estimated_space_mb = estimated_products * 5 * 0.5 * 3  # ~7.5 GB for 1000 products
            estimated_space_bytes = estimated_space_mb * 1024 * 1024

            available_gb = stat.free / (1024**3)
            required_gb = estimated_space_bytes / (1024**3)

            if stat.free > estimated_space_bytes * 2:  # 2x safety margin
                return {
                    'name': 'Disk Space',
                    'status': 'success',
                    'message': f'Sufficient disk space: {available_gb:.1f} GB available',
                    'details': {
                        'available_gb': available_gb,
                        'estimated_required_gb': required_gb,
                        'percent_used': stat.percent
                    }
                }
            elif stat.free > estimated_space_bytes:
                return {
                    'name': 'Disk Space',
                    'status': 'warning',
                    'message': f'Limited disk space: {available_gb:.1f} GB available (estimated {required_gb:.1f} GB needed)',
                    'details': {
                        'available_gb': available_gb,
                        'estimated_required_gb': required_gb,
                        'percent_used': stat.percent
                    }
                }
            else:
                return {
                    'name': 'Disk Space',
                    'status': 'critical',
                    'message': f'Insufficient disk space: {available_gb:.1f} GB available, estimated {required_gb:.1f} GB needed',
                    'details': {
                        'available_gb': available_gb,
                        'estimated_required_gb': required_gb,
                        'percent_used': stat.percent
                    }
                }
        except Exception as e:
            return {
                'name': 'Disk Space',
                'status': 'warning',
                'message': f'Could not check disk space: {str(e)}',
                'details': {}
            }

    def check_database(self):
        """Check database connection and capacity"""
        from django.db import connection

        try:
            # Test basic connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")

            # Get database size (PostgreSQL specific)
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT pg_database_size(current_database()) as size,
                               pg_size_pretty(pg_database_size(current_database())) as pretty_size
                    """)
                    row = cursor.fetchone()
                    db_size_bytes = row[0]
                    db_size_pretty = row[1]

                return {
                    'name': 'Database',
                    'status': 'success',
                    'message': f'Database connection successful (size: {db_size_pretty})',
                    'details': {
                        'size_bytes': db_size_bytes,
                        'size_pretty': db_size_pretty
                    }
                }
            except:
                # If pg_database_size fails (e.g., permissions), still pass
                return {
                    'name': 'Database',
                    'status': 'success',
                    'message': 'Database connection successful',
                    'details': {}
                }

        except Exception as e:
            return {
                'name': 'Database',
                'status': 'critical',
                'message': f'Database connection failed: {str(e)}',
                'details': {}
            }

    def estimate_duration(self):
        """Estimate migration duration based on data volume"""
        try:
            # Try to get product count from API
            if self.job.platform == 'woocommerce' and self.job.method == 'api':
                url = f"{self.config['store_url'].rstrip('/')}/wp-json/wc/v3/products"
                auth = (self.config['consumer_key'], self.config['consumer_secret'])

                response = requests.head(url, auth=auth, timeout=5)

                # WooCommerce includes X-WP-Total header with total count
                total_products = int(response.headers.get('X-WP-Total', 1000))

                # Rough estimate: 100 products per minute with images
                estimated_minutes = max(1, total_products / 100)

                return {
                    'name': 'Duration Estimate',
                    'status': 'info',
                    'message': f'Estimated duration: {estimated_minutes:.0f} minutes for {total_products} products',
                    'details': {
                        'estimated_products': total_products,
                        'estimated_minutes': estimated_minutes,
                        'rate': '100 products/minute'
                    }
                }
            else:
                return {
                    'name': 'Duration Estimate',
                    'status': 'info',
                    'message': 'Duration depends on data volume',
                    'details': {}
                }

        except Exception as e:
            return {
                'name': 'Duration Estimate',
                'status': 'info',
                'message': 'Could not estimate duration',
                'details': {}
            }
