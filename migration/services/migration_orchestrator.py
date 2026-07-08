"""
Migration Orchestrator
Coordinates the complete migration flow from start to finish
"""
from typing import Dict, List, Optional, Callable
from django.db import transaction
from django.utils import timezone
from migration.models import MigrationJob, MigrationStep, MigrationLog
from migration.fetchers.woocommerce_api import WooCommerceAPIClient
from migration.validators.connection import PreFlightChecker
from migration.importers import WooCommerceImporter
from tqdm import tqdm
import logging

logger = logging.getLogger(__name__)


class MigrationOrchestrator:
    """
    Orchestrates the complete migration process

    Flow:
    1. Pre-flight checks
    2. Fetch data from source
    3. Import data to target
    4. Verify import
    5. Cleanup
    """

    def __init__(self, migration_job: MigrationJob):
        """
        Initialize migration orchestrator

        Args:
            migration_job: MigrationJob instance
        """
        self.job = migration_job
        self.connection_config = migration_job.connection_config

        # Initialize components
        self.api_client = None
        self.importer = None
        self.preflight_checker = None

        # Statistics
        self.stats = {
            'start_time': None,
            'end_time': None,
            'duration': None,
            'categories': {},
            'products': {},
            'customers': {},
            'orders': {},
        }

    def run_migration(self, progress_callback: Optional[Callable] = None):
        """
        Run the complete migration process

        Args:
            progress_callback: Optional callback for progress updates
        """
        try:
            self.stats['start_time'] = timezone.now()
            self._update_job_status('connecting', 'Starting migration...')

            # Step 1: Pre-flight checks
            self._log_info("Starting pre-flight checks...")
            if not self._run_preflight_checks():
                raise Exception("Pre-flight checks failed")
            self._log_info("Pre-flight checks completed")

            # Step 2: Initialize API client
            self._log_info("Initializing API client...")
            self._initialize_api_client()
            self._log_info("API client initialized")

            # Step 3: Fetch data
            self._update_job_status('running', 'Fetching data from WooCommerce...')
            self._log_info("Starting data fetching...")

            categories_data = []
            products_data = []

            if self.job.import_categories:
                logger.info("Fetching categories...")
                categories_data = self._fetch_categories(progress_callback)
                logger.info(f"Fetched {len(categories_data)} categories")

            if self.job.import_products:
                logger.info("Fetching products...")
                products_data = self._fetch_products(progress_callback)
                logger.info(f"Fetched {len(products_data)} products")

            self._log_info("Data fetching completed")

            # Step 4: Import data
            self._update_job_status('running', 'Importing data...')
            self._log_info("Starting data import...")
            self._import_data(categories_data, products_data, progress_callback)
            self._log_info("Data import completed")

            # Step 5: Post-import verification
            self._log_info("Starting verification...")
            self._verify_import()
            self._log_info("Verification completed")

            # Success
            self.stats['end_time'] = timezone.now()
            self.stats['duration'] = (self.stats['end_time'] - self.stats['start_time']).total_seconds()

            self._update_job_status('completed', 'Migration completed successfully')
            self._log_completion()

        except Exception as e:
            logger.error(f"Migration failed: {e}")
            self._update_job_status('failed', f'Migration failed: {str(e)}')
            self._log_error(f"Migration failed: {e}")
            raise

        finally:
            self._cleanup()

    def _run_preflight_checks(self) -> bool:
        """Run pre-flight checks"""
        try:
            self.preflight_checker = PreFlightChecker(self.job)
            results = self.preflight_checker.run_all_checks()

            # Results is a dict with categorized checks
            critical_failures = results.get('critical_failures', [])
            warnings = results.get('warnings', [])
            info = results.get('info', [])

            # Check for critical failures
            if critical_failures:
                for failure in critical_failures:
                    self._log_error(f"Pre-flight check failed: {failure['name']} - {failure['message']}")
                return False

            # Log warnings
            for warning in warnings:
                self._log_warning(f"Pre-flight warning: {warning['name']} - {warning['message']}")

            # Log info
            for item in info:
                self._log_info(f"Pre-flight info: {item['name']} - {item['message']}")

            total_checks = len(critical_failures) + len(warnings) + len(info)
            self._log_info(f"Pre-flight checks passed: {total_checks} checks completed")
            return True

        except Exception as e:
            self._log_error(f"Pre-flight checks failed with error: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False

    def _initialize_api_client(self):
        """Initialize API client"""
        store_url = self.connection_config.get('store_url')
        consumer_key = self.connection_config.get('consumer_key')
        consumer_secret = self.connection_config.get('consumer_secret')

        if not all([store_url, consumer_key, consumer_secret]):
            raise ValueError("Missing connection configuration")

        self.api_client = WooCommerceAPIClient(
            store_url=store_url,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret
        )

        self._log_info(f"API client initialized for {store_url}")

    def _fetch_categories(self, progress_callback: Optional[Callable] = None) -> List[Dict]:
        """Fetch all categories"""
        def progress(current, total):
            if progress_callback:
                progress_callback({
                    'stage': 'fetch_categories',
                    'current': current,
                    'total': total,
                    'message': f'Fetching categories: {current}/{total}'
                })

        categories = self.api_client.fetch_all_categories(progress_callback=progress)
        self.stats['categories']['fetched'] = len(categories)
        return categories

    def _fetch_products(self, progress_callback: Optional[Callable] = None) -> List[Dict]:
        """Fetch all products"""
        def progress(current, total):
            if progress_callback:
                progress_callback({
                    'stage': 'fetch_products',
                    'current': current,
                    'total': total,
                    'message': f'Fetching products: {current}/{total}'
                })

        products = self.api_client.fetch_all_products(progress_callback=progress)
        self.stats['products']['fetched'] = len(products)
        return products

    def _import_data(
        self,
        categories: List[Dict],
        products: List[Dict],
        progress_callback: Optional[Callable] = None
    ):
        """Import all data"""
        # Initialize importer
        self.importer = WooCommerceImporter(self.job, dry_run=False)

        # Import categories
        if categories:
            def cat_progress(current, total, **kwargs):
                if progress_callback:
                    progress_callback({
                        'stage': 'import_categories',
                        'current': current,
                        'total': total,
                        'message': f'Importing categories: {current}/{total}'
                    })

            cat_stats = self.importer.import_categories(categories, cat_progress)
            self.stats['categories']['import'] = cat_stats
            self._log_info(
                f"Categories imported: {cat_stats['created']} created, "
                f"{cat_stats['updated']} updated, {cat_stats['failed']} failed"
            )

        # Import products
        if products:
            def prod_progress(current, total, **kwargs):
                if progress_callback:
                    progress_callback({
                        'stage': 'import_products',
                        'current': current,
                        'total': total,
                        'message': f'Importing products: {current}/{total}'
                    })

            prod_stats = self.importer.import_products(products, prod_progress)
            self.stats['products']['import'] = prod_stats
            self._log_info(
                f"Products imported: {prod_stats['created']} created, "
                f"{prod_stats['updated']} updated, {prod_stats['failed']} failed"
            )

    def _verify_import(self):
        """Verify imported data"""
        from catalog.models import Category, Product

        # Count imported records
        categories_count = Category.objects.count()
        products_count = Product.objects.count()

        self._log_info(f"Verification: {categories_count} categories, {products_count} products in database")

        # Check for expected counts
        expected_categories = self.stats['categories'].get('import', {}).get('created', 0) + \
                            self.stats['categories'].get('import', {}).get('updated', 0)
        expected_products = self.stats['products'].get('import', {}).get('created', 0) + \
                          self.stats['products'].get('import', {}).get('updated', 0)

        if expected_categories > 0 and categories_count < expected_categories:
            self._log_warning(f"Expected {expected_categories} categories but found {categories_count}")

        if expected_products > 0 and products_count < expected_products:
            self._log_warning(f"Expected {expected_products} products but found {products_count}")

    def _cleanup(self):
        """Cleanup resources"""
        if self.importer:
            self.importer.cleanup()

        if self.api_client:
            self.api_client.session.close()

        self._log_info("Cleanup completed")

    def _update_job_status(self, status: str, message: str = ''):
        """Update job status"""
        self.job.status = status
        if message:
            self.job.status_message = message
        self.job.save()

        self._log_info(f"Status: {status} - {message}")

    def _log_info(self, message: str):
        """Log info message"""
        MigrationLog.objects.create(
            job=self.job,
            level='info',
            message=message
        )
        logger.info(message)

    def _log_warning(self, message: str):
        """Log warning message"""
        MigrationLog.objects.create(
            job=self.job,
            level='warning',
            message=message
        )
        logger.warning(message)

    def _log_error(self, message: str):
        """Log error message"""
        MigrationLog.objects.create(
            job=self.job,
            level='error',
            message=message
        )
        logger.error(message)

    def _log_completion(self):
        """Log migration completion"""
        summary = f"""
Migration completed successfully!

Duration: {self.stats['duration']:.2f} seconds

Categories:
  - Fetched: {self.stats['categories'].get('fetched', 0)}
  - Created: {self.stats['categories'].get('import', {}).get('created', 0)}
  - Updated: {self.stats['categories'].get('import', {}).get('updated', 0)}
  - Failed: {self.stats['categories'].get('import', {}).get('failed', 0)}

Products:
  - Fetched: {self.stats['products'].get('fetched', 0)}
  - Created: {self.stats['products'].get('import', {}).get('created', 0)}
  - Updated: {self.stats['products'].get('import', {}).get('updated', 0)}
  - Failed: {self.stats['products'].get('import', {}).get('failed', 0)}
"""

        self._log_info(summary)

    def get_stats(self) -> Dict:
        """Get migration statistics"""
        return self.stats
