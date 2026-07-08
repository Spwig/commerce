"""
Magento 2 pre-flight connection and system checks before migration.

Validates:
- API connection via Bearer token
- Endpoint accessibility (products, customers, orders, categories)
- Disk space requirements
- Database connectivity
- Duration estimation
"""
import logging
import psutil

logger = logging.getLogger(__name__)


class MagentoPreFlightChecker:
    """Run pre-flight checks specific to Magento 2 migrations."""

    def __init__(self, migration_job):
        self.job = migration_job
        self.config = migration_job.connection_config or {}

    def run_all_checks(self):
        """
        Run all Magento pre-flight checks.

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
            'all_passed': True,
        }

        checks = [
            self.check_connection(),
            self.check_permissions(),
            self.check_disk_space(),
            self.check_database(),
            self.estimate_duration(),
        ]

        for check in checks:
            if check['status'] == 'critical':
                results['critical_failures'].append(check)
                results['all_passed'] = False
            elif check['status'] == 'warning':
                results['warnings'].append(check)
            else:
                results['info'].append(check)

        return results

    def check_connection(self):
        """Verify Magento REST API connection via store config endpoint."""
        try:
            from migration.fetchers.magento_api import MagentoAPIClient

            client = MagentoAPIClient(
                store_url=self.config.get('store_url', ''),
                access_token=self.config.get('access_token', ''),
                verify_ssl=self.config.get('verify_ssl', True),
            )

            result = client.test_connection()
            if result.get('success'):
                store_info = result.get('store_info', {})
                currency = store_info.get('currency', 'USD')
                return {
                    'name': 'API Connection',
                    'status': 'ok',
                    'message': f"Connected to Magento store (currency: {currency})",
                }
            else:
                return {
                    'name': 'API Connection',
                    'status': 'critical',
                    'message': f"Connection failed: {result.get('error', 'Unknown error')}",
                }

        except Exception as e:
            logger.error(f"Magento connection check failed: {e}")
            return {
                'name': 'API Connection',
                'status': 'critical',
                'message': f"Connection check failed: {str(e)}",
            }

    def check_permissions(self):
        """Test access to key Magento API endpoints."""
        try:
            from migration.fetchers.magento_api import MagentoAPIClient

            client = MagentoAPIClient(
                store_url=self.config.get('store_url', ''),
                access_token=self.config.get('access_token', ''),
                verify_ssl=self.config.get('verify_ssl', True),
            )

            endpoints = {
                'Products': '/products',
                'Customers': '/customers/search',
                'Orders': '/orders',
                'Categories': '/categories',
                'Reviews': '/reviews',
                'Sales Rules': '/salesRules/search',
                'CMS Pages': '/cmsPage/search',
            }

            accessible = []
            inaccessible = []

            for name, endpoint in endpoints.items():
                if endpoint == '/categories':
                    # Categories endpoint doesn't use searchCriteria
                    try:
                        response = client._request('GET', endpoint)
                        if response.status_code == 200:
                            accessible.append(name)
                        else:
                            inaccessible.append(name)
                    except Exception:
                        inaccessible.append(name)
                else:
                    if client.check_endpoint_access(endpoint):
                        accessible.append(name)
                    else:
                        inaccessible.append(name)

            if not inaccessible:
                return {
                    'name': 'API Permissions',
                    'status': 'ok',
                    'message': f"All {len(accessible)} endpoints accessible",
                }

            # Check if critical endpoints (products, categories) are accessible
            critical_missing = [e for e in inaccessible if e in ('Products', 'Categories')]
            if critical_missing:
                return {
                    'name': 'API Permissions',
                    'status': 'critical',
                    'message': (
                        f"Cannot access: {', '.join(critical_missing)}. "
                        f"Check your Integration has API access to these resources."
                    ),
                }

            return {
                'name': 'API Permissions',
                'status': 'warning',
                'message': (
                    f"Limited access: {', '.join(accessible)} OK. "
                    f"Cannot access: {', '.join(inaccessible)}. "
                    f"Some data types may not import."
                ),
            }

        except Exception as e:
            logger.error(f"Magento permission check failed: {e}")
            return {
                'name': 'API Permissions',
                'status': 'warning',
                'message': f"Permission check failed: {str(e)}",
            }

    def check_disk_space(self):
        """Check available disk space for media downloads."""
        try:
            disk = psutil.disk_usage('/')
            free_gb = disk.free / (1024 ** 3)

            if free_gb < 1:
                return {
                    'name': 'Disk Space',
                    'status': 'critical',
                    'message': f"Only {free_gb:.1f} GB free. At least 1 GB required.",
                }
            elif free_gb < 5:
                return {
                    'name': 'Disk Space',
                    'status': 'warning',
                    'message': (
                        f"{free_gb:.1f} GB free. "
                        f"Recommended: 5+ GB for stores with many product images."
                    ),
                }
            else:
                return {
                    'name': 'Disk Space',
                    'status': 'ok',
                    'message': f"{free_gb:.1f} GB free",
                }

        except Exception as e:
            return {
                'name': 'Disk Space',
                'status': 'warning',
                'message': f"Could not check disk space: {str(e)}",
            }

    def check_database(self):
        """Verify database connectivity."""
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")

            return {
                'name': 'Database',
                'status': 'ok',
                'message': 'Database connection verified',
            }

        except Exception as e:
            return {
                'name': 'Database',
                'status': 'critical',
                'message': f"Database connection failed: {str(e)}",
            }

    def estimate_duration(self):
        """Estimate migration duration based on item counts."""
        try:
            from migration.fetchers.magento_api import MagentoAPIClient

            client = MagentoAPIClient(
                store_url=self.config.get('store_url', ''),
                access_token=self.config.get('access_token', ''),
                verify_ssl=self.config.get('verify_ssl', True),
            )

            counts = client.get_total_counts()
            total_items = sum(counts.values())

            # Magento products take ~3 seconds each (extra API calls for configurable children)
            # Other items ~2 seconds each
            product_seconds = counts.get('products', 0) * 3
            other_seconds = (total_items - counts.get('products', 0)) * 2
            estimated_seconds = product_seconds + other_seconds

            if estimated_seconds < 60:
                duration_str = f"{estimated_seconds} seconds"
            elif estimated_seconds < 3600:
                duration_str = f"{estimated_seconds // 60} minutes"
            else:
                hours = estimated_seconds // 3600
                minutes = (estimated_seconds % 3600) // 60
                duration_str = f"{hours}h {minutes}m"

            # Store counts in connection_config for later use
            self.job.connection_config['total_products'] = counts.get('products', 0)
            self.job.connection_config['total_categories'] = counts.get('categories', 0)
            self.job.connection_config['total_customers'] = counts.get('customers', 0)
            self.job.connection_config['total_orders'] = counts.get('orders', 0)
            self.job.connection_config['total_reviews'] = counts.get('reviews', 0)
            self.job.connection_config['total_coupons'] = counts.get('coupons', 0)
            self.job.connection_config['total_cms_pages'] = counts.get('cms_pages', 0)
            self.job.save()

            # Build summary
            details = []
            for key, count in counts.items():
                if count > 0:
                    details.append(f"{count} {key}")

            return {
                'name': 'Duration Estimate',
                'status': 'ok',
                'message': (
                    f"~{duration_str} estimated. "
                    f"Found: {', '.join(details) if details else 'no items'}."
                ),
            }

        except Exception as e:
            logger.warning(f"Failed to estimate duration: {e}")
            return {
                'name': 'Duration Estimate',
                'status': 'warning',
                'message': f"Could not estimate duration: {str(e)}",
            }
