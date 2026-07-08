"""
Import Execution Engine
Orchestrates the entire import process with progress tracking, field mapping, and quarantine
"""
import logging
from typing import Dict, List, Optional, Any, Callable
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from django.core.files.base import ContentFile
from django.utils.html import strip_tags
import requests
from io import BytesIO

from migration.models import MigrationJob, MigrationStep, MigrationStagedItem, MigrationLog
from migration.fetchers.woocommerce_api import WooCommerceAPIClient
from migration.fetchers.wordpress_api import WordPressAPIClient
from migration.importers.wordpress_blog import WordPressBlogImporter
from migration.importers.affiliate_importer import AffiliateImporter
from migration.fetchers.spwig_bridge_api import SpwigBridgeAPIClient
from migration.utils.transformers import (
    transform_woocommerce_status,
    transform_woocommerce_type,
    transform_money,
    transform_integer_nullable,
    transform_decimal_nullable,
    transform_woocommerce_backorders,
    extract_seo_meta,
    filter_meta_data,
    detect_subscription_product,
    detect_digital_product,
    detect_external_product,
    detect_addon_product,
    detect_bundle_product,
    detect_gift_card_product,
    detect_composite_product,
    detect_booking_product,
    parse_woocommerce_datetime,
)
from migration.services.attribute_service import AttributeService
from migration.services.extension_import_service import WooCommerceExtensionImportService
from migration.mapping_config import IGNORE_META_PREFIXES
from catalog.models import Category, Brand, Product, ProductVariant, ProductImage, ProductReview, StockItem, Warehouse
from media_library.models import MediaAsset
from orders.models import Order, OrderItem, Address
from vouchers.models import VoucherCode
from accounts.models import CustomerProfile
from django.contrib.auth import get_user_model
from tqdm import tqdm

User = get_user_model()

logger = logging.getLogger(__name__)


class ImportExecutor:
    """
    Main import executor that orchestrates the entire migration process

    Features:
    - Progress tracking with MigrationStep records
    - Field mapping from MigrationMapping model
    - Custom transformers for data conversion
    - Quarantine system for failed imports
    - Real-time progress updates
    """

    def __init__(self, migration_job: MigrationJob):
        self.job = migration_job
        self.client = None
        self.field_mappings = {}
        self.category_map = {}  # Maps external_id -> Category instance
        self.brand_map = {}
        self.current_step = None  # Track current step for logging
        self.default_warehouse = None  # Resolved in _import_products()

        # Initialize data client based on platform
        if self.job.platform == 'woocommerce' and self.job.connection_config:
            self.client = WooCommerceAPIClient(
                store_url=self.job.connection_config['store_url'],
                consumer_key=self.job.connection_config['consumer_key'],
                consumer_secret=self.job.connection_config['consumer_secret']
            )
        elif self.job.platform == 'csv' and self.job.connection_config:
            from migration.fetchers.csv_reader import CSVDataReader
            self.client = CSVDataReader(
                csv_files_config=self.job.connection_config.get('csv_files', {}),
                column_mappings=self.job.connection_config.get('csv_column_mappings', {}),
            )

        # Initialize extension import service
        self.extension_service = WooCommerceExtensionImportService(
            migration_job=self.job,
            currency=self._get_currency()
        )

        # Load field mappings
        self._load_field_mappings()

    def _get_currency(self):
        """Get currency from job config, falling back to merchant's default."""
        if self.job.connection_config:
            currency = self.job.connection_config.get('currency')
            if currency:
                return currency
        from core.utils import get_default_currency
        return get_default_currency()

    def _log(self, level: str, message: str, source_type: str = 'system', source_id: str = ''):
        """Log to both Python logger and MigrationLog model"""
        # Log to Python logger
        getattr(logger, level.lower())(message)

        # Log to database
        MigrationLog.objects.create(
            job=self.job,
            step=self.current_step,
            level=level,
            message=message,
            source_type=source_type,
            source_id=source_id
        )

    def _load_field_mappings(self):
        """Load field mappings from MigrationMapping model"""
        mappings = self.job.mappings.all()

        for mapping in mappings:
            key = f"{mapping.source_type}.{mapping.source_field}"
            self.field_mappings[key] = {
                'dest_model': mapping.dest_model,
                'dest_field': mapping.dest_field,
                'transform_type': mapping.transform_type,
                'transform_function': mapping.transform_function,
            }

        logger.info(f"Loaded {len(self.field_mappings)} field mappings")

    def execute(self):
        """Execute the complete import process"""
        try:
            # Update job status
            self.job.status = 'running'
            self.job.started_at = timezone.now()
            self.job.save()

            logger.info(f"Starting import for job {self.job.id}")

            # Get import settings from step 3
            config = self.job.connection_config or {}

            # Execute imports in order
            if config.get('import_categories', False):
                self._import_categories()

            if config.get('import_products', False):
                self._import_products()
                # Resolve deferred bundle/composite references
                resolved = self.extension_service.resolve_deferred_extensions()
                if resolved:
                    self._log('info', f"Resolved {resolved} deferred extension references (bundles/composites)")

            if config.get('import_customers', False):
                self._import_customers()

            if config.get('import_orders', False):
                self._import_orders()

            if config.get('import_reviews', False):
                self._import_reviews()

            if config.get('import_coupons', False):
                self._import_coupons()

            if config.get('import_blog', False):
                self._import_blog()

            if config.get('import_affiliates', False):
                self._import_affiliates()

            # Post-import: scan content for internal links that need rewriting
            self._scan_content_links()

            # Mark job as complete
            self.job.status = 'completed'
            self.job.completed_at = timezone.now()
            self.job.duration_seconds = int((self.job.completed_at - self.job.started_at).total_seconds())
            self.job.progress_percent = 100
            self.job.save()

            logger.info(f"Import completed successfully for job {self.job.id}")
            self._update_overall_progress()

        except Exception as e:
            logger.error(f"Import failed: {e}", exc_info=True)

            # Mark job as failed
            self.job.status = 'failed'
            self.job.error_summary = str(e)
            self.job.completed_at = timezone.now()
            if self.job.started_at:
                self.job.duration_seconds = (self.job.completed_at - self.job.started_at).total_seconds()
            self.job.save()

            raise

    def _import_categories(self):
        """Import categories with parent resolution"""
        # Create migration step
        step = MigrationStep.objects.create(
            job=self.job,
            step_type='categories',
            status='running',
            started_at=timezone.now(),
        )
        self.current_step = step

        self._log('info', "Starting category import...")

        try:
            # Fetch all categories from WooCommerce
            categories = []
            page = 1
            per_page = 100

            while True:
                batch = self.client.fetch_categories(page=page, per_page=per_page)
                if not batch:
                    break
                categories.extend(batch)
                page += 1

                if len(batch) < per_page:
                    break

            # Use saved count from wizard preview, fallback to fetched count
            step.items_total = self.job.connection_config.get('total_categories', len(categories))
            step.save()

            self._log('info', f"Fetched {len(categories)} categories from WooCommerce")

            # First pass: Create all categories (without parents)
            for idx, cat_data in enumerate(categories):
                try:
                    self._import_single_category(cat_data, step)
                except Exception as e:
                    logger.error(f"Failed to import category {cat_data.get('id')}: {e}")
                    self._quarantine_item(cat_data, 'category', str(e))
                    step.items_failed += 1
                    step.save()

            # Second pass: Resolve parent relationships
            for cat_data in categories:
                parent_id = cat_data.get('parent')
                if parent_id and parent_id > 0:
                    try:
                        # Find child category by external_id
                        child_external_id = str(cat_data.get('id'))
                        child = Category.objects.filter(external_id=child_external_id).first()

                        # Find parent category by external_id
                        parent_external_id = str(parent_id)
                        parent = Category.objects.filter(external_id=parent_external_id).first()

                        if child and parent:
                            child.parent = parent
                            child.save()
                            logger.debug(f"Set parent for category {child.name}")
                    except Exception as e:
                        logger.warning(f"Failed to set parent for category {cat_data.get('id')}: {e}")

            # Post-import: validate hierarchy integrity
            self._validate_category_hierarchy(step)

            # Mark step as complete
            step.status = 'completed'
            step.completed_at = timezone.now()
            step.duration_seconds = (step.completed_at - step.started_at).total_seconds()
            step.save()

            # Update job statistics
            self.job.categories_imported = step.items_imported
            self.job.categories_failed = step.items_failed
            self.job.categories_skipped = step.items_skipped
            self.job.save()

            # Update overall progress
            self._update_overall_progress()

            logger.info(f"Category import complete: {step.items_imported} imported, {step.items_failed} failed")

        except Exception as e:
            step.status = 'failed'
            step.error_message = str(e)
            step.completed_at = timezone.now()
            step.save()
            raise

    def _import_single_category(self, cat_data: Dict, step: MigrationStep) -> Optional[Category]:
        """Import a single category"""
        external_id = str(cat_data.get('id'))

        # Check if already imported
        existing = Category.objects.filter(external_id=external_id).first()
        if existing:
            # Ensure previously-imported categories are active (re-import fix)
            if not existing.is_active:
                existing.is_active = True
                existing.save(update_fields=['is_active'])
                logger.info(f"Reactivated previously-imported category: {existing.name}")
            logger.debug(f"Category {external_id} already imported, skipping")
            step.items_skipped += 1
            step.save()
            return existing

        # Apply field mappings
        mapped_data = self._apply_mappings(cat_data, 'category')

        # Create category
        category = Category.objects.create(
            external_id=external_id,
            migration_job=self.job,
            name=mapped_data.get('name', cat_data.get('name')),
            slug=self._get_unique_slug(mapped_data.get('slug', cat_data.get('slug')), Category),
            description=mapped_data.get('description', cat_data.get('description', '')),
            is_active=True,
            imported_meta=filter_meta_data(cat_data.get('meta_data', []), IGNORE_META_PREFIXES),
        )

        # Store in category map
        self.category_map[external_id] = category

        step.items_imported += 1
        step.save()

        logger.debug(f"Imported category: {category.name}")
        return category

    def _validate_category_hierarchy(self, step: MigrationStep):
        """
        Post-import hierarchy validation.
        Ensures all parent categories referenced by active children are themselves active,
        and that the imported hierarchy matches the source structure.
        """
        # Get all categories from this migration job
        imported_categories = Category.objects.filter(migration_job=self.job)

        # Find inactive parents that have active children
        inactive_parents = Category.objects.filter(
            children__in=imported_categories.filter(is_active=True),
            is_active=False,
        ).distinct()

        reactivated = 0
        for parent in inactive_parents:
            parent.is_active = True
            parent.save(update_fields=['is_active'])
            reactivated += 1
            self._log('info',
                f"Reactivated parent category '{parent.name}' (ID: {parent.id}) — "
                f"required by active child categories",
                source_type='category', source_id=str(parent.external_id or parent.id))

        # Also check the full ancestor chain (grandparents, etc.)
        activated_any = reactivated > 0
        while activated_any:
            activated_any = False
            inactive_ancestors = Category.objects.filter(
                children__is_active=True,
                is_active=False,
            ).distinct()
            for ancestor in inactive_ancestors:
                ancestor.is_active = True
                ancestor.save(update_fields=['is_active'])
                reactivated += 1
                activated_any = True
                self._log('info',
                    f"Reactivated ancestor category '{ancestor.name}' (ID: {ancestor.id}) — "
                    f"required for hierarchy integrity",
                    source_type='category', source_id=str(ancestor.external_id or ancestor.id))

        if reactivated:
            self._log('info', f"Hierarchy validation: reactivated {reactivated} parent categories")

        logger.info(f"Category hierarchy validation complete: {reactivated} parents reactivated")

    def _import_products(self):
        """Import products in batches"""
        # Create migration step
        step = MigrationStep.objects.create(
            job=self.job,
            step_type='products',
            status='running',
            started_at=timezone.now(),
        )
        self.current_step = step

        self._log('info', "Starting product import...")

        try:
            # Get batch size from settings
            batch_size = self.job.connection_config.get('batch_size', 20)

            # Fetch total count from WooCommerce API
            counts = self.client.get_total_counts()
            total_products = counts.get('products', 0)

            # Use saved count from wizard preview, fallback to fetched count
            step.items_total = self.job.connection_config.get('total_products', total_products)
            step.save()

            self._log('info', f"Found {total_products} products to import")

            # Resolve default warehouse once for StockItem creation
            self.default_warehouse = Warehouse.objects.filter(is_active=True).first()
            if not self.default_warehouse:
                self._log('warning', "No active warehouse found. Stock quantities will not be imported.")

            page = 1
            processed_count = 0

            # Create progress bar for products
            progress_bar = tqdm(
                total=total_products,
                desc="📦 Products",
                unit="prod",
            )

            while processed_count < total_products:
                products = self.client.fetch_products(page=page, per_page=batch_size)
                if not products:
                    break

                self._log('info', f"Processing batch {page} ({len(products)} products)")

                for product_data in products:
                    try:
                        self._import_single_product(product_data, step)
                    except Exception as e:
                        self._log('error', f"Failed to import product {product_data.get('id')}: {e}",
                                 source_type='product', source_id=str(product_data.get('id')))
                        self._quarantine_item(product_data, 'product', str(e))
                        step.items_failed += 1
                        step.save()
                    finally:
                        progress_bar.update(1)

                processed_count += len(products)
                page += 1

                if len(products) < batch_size:
                    break

            progress_bar.close()

            # Mark step as complete
            step.status = 'completed'
            step.completed_at = timezone.now()
            step.duration_seconds = (step.completed_at - step.started_at).total_seconds()
            step.save()

            # Update job statistics
            self.job.products_imported = step.items_imported
            self.job.products_failed = step.items_failed
            self.job.products_skipped = step.items_skipped
            self.job.save()

            # Update overall progress
            self._update_overall_progress()

            self._log('info', f"Product import complete: {step.items_imported} imported, {step.items_failed} failed")

        except Exception as e:
            step.status = 'failed'
            step.error_message = str(e)
            step.completed_at = timezone.now()
            step.save()
            raise

    def _import_single_product(self, product_data: Dict, step: MigrationStep) -> Optional[Product]:
        """Import a single product"""
        external_id = str(product_data.get('id'))

        # Check if already imported
        existing = Product.objects.filter(external_id=external_id).first()
        if existing:
            logger.debug(f"Product {external_id} already imported, skipping")
            step.items_skipped += 1
            step.save()
            return existing

        # Apply field mappings
        mapped_data = self._apply_mappings(product_data, 'product')

        # Get or create category
        category = self._get_product_category(product_data)
        if not category:
            raise ValueError("No category found for product")

        # Transform price
        price = transform_money(
            product_data.get('regular_price', product_data.get('price')),
            self._get_currency()
        )

        # Handle products without price (free products, gift cards, etc.)
        if not price or price == 0:
            # Check if this is intentionally free or missing data
            if product_data.get('type') in ['variable', 'grouped']:
                # Variable/grouped products might not have base price
                price = Decimal('0.00')
            else:
                # Missing price data - skip this product
                raise ValueError("Product has no price")

        # Apply price adjustment if configured
        price_adjustment_type = self.job.connection_config.get('price_adjustment_type', 'none')
        if price_adjustment_type != 'none':
            adjustment_value = Decimal(self.job.connection_config.get('price_adjustment_value', '0'))
            if price_adjustment_type == 'percentage':
                price = price * (1 + adjustment_value / 100)
            elif price_adjustment_type == 'fixed':
                price = price + adjustment_value

        # Transform sale price
        compare_at_price = None
        if product_data.get('sale_price'):
            compare_at_price = transform_money(
                product_data.get('sale_price'),
                self._get_currency()
            )

        # Prepare short description (truncate to 500 chars)
        short_desc = mapped_data.get('short_description', product_data.get('short_description', ''))
        if len(short_desc) > 500:
            short_desc = short_desc[:497] + '...'

        # Detect special product types
        is_subscription, subscription_data = detect_subscription_product(product_data)
        is_digital, digital_data = detect_digital_product(product_data)
        is_external, external_data = detect_external_product(product_data)

        # Detect WooCommerce extension types
        has_addons, addon_data = detect_addon_product(product_data)
        is_wc_bundle, bundle_data = detect_bundle_product(product_data)
        is_gift_card, gift_card_data = detect_gift_card_product(product_data)
        is_composite, composite_data = detect_composite_product(product_data)
        is_booking, booking_data = detect_booking_product(product_data)

        # Determine product type with extension handling (priority order)
        product_type = transform_woocommerce_type(product_data.get('type', 'simple'))

        if is_gift_card:
            product_type = 'gift_card'
        elif is_composite:
            product_type = 'configurable'
        elif is_wc_bundle:
            product_type = 'bundle'
        elif is_digital and digital_data.get('is_downloadable'):
            product_type = 'digital'
        elif has_addons and product_type == 'simple':
            product_type = 'customizable'

        # Subscriptions keep their base type (simple/variable)
        # The subscription flag is set separately via SubscriptionPlan

        # Bookings import as simple until booking module is built
        if is_booking:
            product_type = 'simple'

        # Build imported_meta with special type data
        imported_meta = {
            'woocommerce_id': external_id,
            'seo': extract_seo_meta(product_data.get('meta_data', [])),
            'original_type': product_data.get('type'),
            'meta_data': filter_meta_data(product_data.get('meta_data', []), IGNORE_META_PREFIXES),
        }

        # Add special type data to imported_meta
        if is_subscription:
            imported_meta['subscription_data'] = subscription_data

        if is_digital:
            imported_meta['digital_data'] = digital_data
            if digital_data.get('files_count', 0) > 0:
                self._log('info',
                    f"Digital product '{product_data.get('name')}' has {digital_data['files_count']} download files - merchant should re-upload",
                    source_type='product', source_id=external_id)

        if is_external:
            imported_meta['external_data'] = external_data
            imported_meta['is_external'] = True
            imported_meta['requires_review'] = True
            imported_meta['review_reason'] = 'external_affiliate_product'
            self._log('info',
                f"External/affiliate product '{product_data.get('name')}' - links to {external_data.get('external_url', 'N/A')}",
                source_type='product', source_id=external_id)

        # Compute sale fields from WooCommerce sale_price
        sale_type = 'none'
        sale_value_decimal = None
        if compare_at_price and price and compare_at_price < price:
            sale_type = 'fixed_price'
            sale_value_decimal = compare_at_price.amount  # Money → Decimal

        # Create product
        product = Product.objects.create(
            external_id=external_id,
            migration_job=self.job,
            name=mapped_data.get('name', product_data.get('name')),
            slug=self._get_unique_slug(mapped_data.get('slug', product_data.get('slug')), Product),
            sku=self._get_unique_sku(mapped_data.get('sku', product_data.get('sku', ''))),
            product_type=product_type,
            category=category,
            full_description=mapped_data.get('full_description', product_data.get('description', '')),
            short_description=short_desc,
            price=price,
            sale_type=sale_type,
            sale_value=sale_value_decimal,
            status=transform_woocommerce_status(product_data.get('status', 'publish')),
            is_featured=product_data.get('featured', False),
            track_inventory=product_data.get('manage_stock', True),
            allow_backorders=transform_woocommerce_backorders(product_data.get('backorders', 'no')),
            weight=transform_decimal_nullable(product_data.get('weight')),
            length=transform_decimal_nullable(product_data.get('dimensions', {}).get('length')),
            width=transform_decimal_nullable(product_data.get('dimensions', {}).get('width')),
            height=transform_decimal_nullable(product_data.get('dimensions', {}).get('height')),
            imported_meta=imported_meta,
        )

        # Create stock item for inventory tracking
        if self.default_warehouse and product_data.get('manage_stock', False):
            stock_qty = transform_integer_nullable(product_data.get('stock_quantity')) or 0
            StockItem.objects.create(
                product=product,
                warehouse=self.default_warehouse,
                on_hand=stock_qty,
                allocated=0,
            )

        # Import product images
        if product_data.get('images'):
            self._import_product_images(product, product_data['images'])

        # Import variants for variable products
        if product_data.get('type') in ('variable', 'variable-subscription') and product_data.get('variations'):
            self._import_product_variants(product, product_data['variations'])

        # ── Extension imports (post-product-creation) ──

        # 1. Subscriptions: Create SubscriptionPlan and link to product
        if is_subscription:
            try:
                self.extension_service.import_subscription_data(
                    product, product_data, subscription_data
                )
                self._log('info',
                    f"Created subscription plan for '{product.name}'",
                    source_type='product', source_id=external_id)
            except Exception as e:
                self._log('warning',
                    f"Failed to create subscription for '{product.name}': {e}. "
                    f"Subscription data preserved in imported_meta.",
                    source_type='product', source_id=external_id)

        # 2. Product Add-Ons: Create CustomizationOption records
        if has_addons:
            try:
                options = self.extension_service.import_product_addons(
                    product, product_data
                )
                if options:
                    self._log('info',
                        f"Created {len(options)} customization options for '{product.name}'",
                        source_type='product', source_id=external_id)
            except Exception as e:
                self._log('warning',
                    f"Failed to import add-ons for '{product.name}': {e}",
                    source_type='product', source_id=external_id)

        # 3. WC Bundles: Create BundleItem records
        if is_wc_bundle:
            try:
                items = self.extension_service.import_bundle_data(
                    product, product_data, bundle_data
                )
                if items:
                    self._log('info',
                        f"Created {len(items)} bundle items for '{product.name}'",
                        source_type='product', source_id=external_id)
            except Exception as e:
                self._log('warning',
                    f"Failed to import bundle components for '{product.name}': {e}",
                    source_type='product', source_id=external_id)

        # 4. Gift Cards: Configure denominations
        if is_gift_card:
            try:
                self.extension_service.import_gift_card_data(
                    product, product_data, gift_card_data
                )
                self._log('info',
                    f"Configured gift card settings for '{product.name}'",
                    source_type='product', source_id=external_id)
            except Exception as e:
                self._log('warning',
                    f"Failed to configure gift card for '{product.name}': {e}",
                    source_type='product', source_id=external_id)

        # 5. Composite Products: Create ConfigurationSlots
        if is_composite:
            try:
                slots = self.extension_service.import_composite_data(
                    product, product_data, composite_data
                )
                if slots:
                    self._log('info',
                        f"Created {len(slots)} configuration slots for '{product.name}'",
                        source_type='product', source_id=external_id)
            except Exception as e:
                self._log('warning',
                    f"Failed to import composite data for '{product.name}': {e}",
                    source_type='product', source_id=external_id)

        # 6. Bookings: Import booking config, resources, person types, availability rules
        if is_booking:
            try:
                self.extension_service.import_booking_data(
                    product, product_data, booking_data
                )
                self._log('info',
                    f"Imported booking data for '{product.name}'",
                    source_type='product', source_id=external_id)
            except Exception as e:
                self._log('warning',
                    f"Failed to import booking data for '{product.name}': {e}",
                    source_type='product', source_id=external_id)

        step.items_imported += 1
        step.save()

        logger.debug(f"Imported product: {product.name}")
        return product

    def _import_product_images(self, product: Product, images_data: List[Dict]):
        """Download and import product images with WebP conversion and thumbnail generation"""
        from media_library.services import ImageProcessor
        from media_library.models import MediaThumbnail, ImageSizePreset
        from django.conf import settings

        processor = ImageProcessor()
        # Get image size presets from database (configurable in Media Library → Image Size Presets)
        image_presets = list(ImageSizePreset.objects.filter(is_active=True))

        for idx, img_data in enumerate(images_data[:5]):  # Limit to 5 images
            try:
                img_url = img_data.get('src')
                if not img_url:
                    continue

                # Download image
                response = requests.get(img_url, timeout=30)
                response.raise_for_status()

                # Get filename from URL
                filename = img_url.split('/')[-1].split('?')[0]
                if not filename:
                    filename = f"product_{product.id}_image_{idx}.jpg"

                # Detect MIME type from filename extension
                ext = filename.lower().split('.')[-1] if '.' in filename else 'jpg'
                mime_type_map = {
                    'jpg': 'image/jpeg',
                    'jpeg': 'image/jpeg',
                    'png': 'image/png',
                    'gif': 'image/gif',
                    'webp': 'image/webp',
                    'svg': 'image/svg+xml',
                }
                mime_type = mime_type_map.get(ext, 'image/jpeg')

                # Create MediaAsset
                media_asset = MediaAsset.objects.create(
                    external_id=str(img_data.get('id', '')),
                    migration_job=self.job,
                    title=img_data.get('name') or f"{product.name} - Image {idx + 1}",
                    alt_text=img_data.get('alt') or product.name,
                    mime_type=mime_type,
                    file_size=len(response.content),
                )

                # Save original file to MediaAsset
                media_asset.original_file.save(
                    filename,
                    ContentFile(response.content),
                    save=True
                )

                # HIGH PERFORMANCE: Generate WebP version for faster loading
                if media_asset.is_image() and not mime_type == 'image/svg+xml':
                    try:
                        webp_content = processor.convert_to_webp(media_asset.original_file)
                        if webp_content:
                            webp_filename = f"{media_asset.id}.webp"
                            media_asset.webp_file.save(webp_filename, webp_content, save=True)
                            logger.debug(f"Generated WebP for product image {idx + 1}")
                    except Exception as e:
                        logger.warning(f"Failed to generate WebP for image: {e}")

                # HIGH PERFORMANCE: Generate thumbnails for faster page loads
                for preset in image_presets:
                    try:
                        original_content, webp_content = processor.generate_thumbnail(
                            media_asset.original_file,
                            preset.width,
                            preset.height,
                            crop_mode=preset.crop_mode
                        )

                        if original_content:
                            thumbnail = MediaThumbnail.objects.create(
                                media_asset=media_asset,
                                size_preset=preset.slug,
                                width=preset.width,
                                height=preset.height
                            )
                            thumbnail.file.save(f"{media_asset.id}_{preset.slug}.jpg", original_content, save=False)
                            if webp_content:
                                thumbnail.webp_file.save(f"{media_asset.id}_{preset.slug}.webp", webp_content, save=False)
                            thumbnail.save()
                            logger.debug(f"Generated {preset.slug} thumbnail for product image {idx + 1}")
                    except Exception as e:
                        logger.warning(f"Failed to generate {preset.slug} thumbnail: {e}")

                # Create ProductImage linking to MediaAsset
                ProductImage.objects.create(
                    product=product,
                    media_asset=media_asset,
                    alt_text=img_data.get('alt') or product.name,
                    is_primary=(idx == 0),
                    position=idx,
                    show_in_gallery=True,
                    show_in_listing=True,
                )

                logger.debug(f"Imported image {idx + 1} for product {product.name} with WebP and thumbnails")

            except Exception as e:
                logger.warning(f"Failed to import image for product {product.name}: {e}")
                continue

    def _import_product_variants(self, product: Product, variant_ids: List[int]):
        """
        Import product variants from WooCommerce.

        This method:
        1. Fetches full variation data from WooCommerce API
        2. Creates/matches ProductAttribute and AttributeValue records
        3. Creates ProductVariant records with proper attribute assignments
        4. Downloads variant images to media library
        5. Maps pricing, stock, weight, dimensions

        Args:
            product: Parent Product instance
            variant_ids: List of WooCommerce variation IDs (from parent product)
        """
        if not variant_ids:
            return

        attribute_service = AttributeService()
        external_product_id = product.external_id
        currency = self._get_currency()

        self._log('info', f"Fetching {len(variant_ids)} variations for product {product.name}")

        # Fetch all variations from WooCommerce API
        try:
            variations = self.client.fetch_all_product_variations(int(external_product_id))
        except Exception as e:
            self._log('error', f"Failed to fetch variations for product {external_product_id}: {e}",
                     source_type='product', source_id=external_product_id)
            return

        if not variations:
            self._log('warning', f"No variations returned for product {product.name}")
            return

        # Track attribute assignments for the parent product
        product_attribute_values: Dict[int, List] = {}  # attribute_id -> [values]

        # Import each variation with progress tracking
        imported_count = 0
        failed_count = 0

        for variation_data in tqdm(variations, desc=f"Variants for {product.name[:30]}", leave=False):
            try:
                variant = self._import_single_variant(
                    product=product,
                    variation_data=variation_data,
                    attribute_service=attribute_service,
                    product_attribute_values=product_attribute_values,
                    currency=currency
                )
                if variant:
                    imported_count += 1
            except Exception as e:
                self._log('error',
                         f"Failed to import variation {variation_data.get('id')}: {e}",
                         source_type='variation',
                         source_id=str(variation_data.get('id')))
                self._quarantine_item(variation_data, 'variation', str(e))
                failed_count += 1

        # Create ProductAttributeAssignments for the parent product
        from catalog.models import ProductAttribute
        for attribute_id, values in product_attribute_values.items():
            try:
                attribute = ProductAttribute.objects.get(id=attribute_id)
                attribute_service.ensure_product_attribute_assignment(
                    product=product,
                    attribute=attribute,
                    values=values
                )
            except ProductAttribute.DoesNotExist:
                pass

        self._log('info',
                 f"Imported {imported_count} variants for {product.name} ({failed_count} failed)")

    def _import_single_variant(
        self,
        product: Product,
        variation_data: Dict,
        attribute_service: AttributeService,
        product_attribute_values: Dict,
        currency: str
    ) -> Optional[ProductVariant]:
        """
        Import a single product variant.

        Args:
            product: Parent Product instance
            variation_data: WooCommerce variation data
            attribute_service: AttributeService instance
            product_attribute_values: Dict to accumulate attribute values for parent
            currency: Currency code

        Returns:
            ProductVariant instance or None
        """
        external_id = str(variation_data.get('id'))

        # Check if variant already imported
        existing = ProductVariant.objects.filter(external_id=external_id).first()
        if existing:
            logger.debug(f"Variant {external_id} already imported, skipping")
            return existing

        # Parse attributes
        wc_attributes = variation_data.get('attributes', [])
        attribute_pairs = attribute_service.parse_woocommerce_attributes(wc_attributes)

        # Build variant name from attributes (e.g., "Large / Red")
        variant_name = attribute_service.build_variant_name(attribute_pairs) or f"Variant {external_id}"

        # Accumulate values for parent product assignments
        for attribute, value in attribute_pairs:
            if attribute.id not in product_attribute_values:
                product_attribute_values[attribute.id] = []
            if value not in product_attribute_values[attribute.id]:
                product_attribute_values[attribute.id].append(value)

        # Get unique SKU
        sku = variation_data.get('sku', '')
        if not sku:
            sku = f"{product.sku}-{external_id}"
        sku = self._get_unique_variant_sku(sku)

        # Transform pricing
        regular_price = transform_money(
            variation_data.get('regular_price') or variation_data.get('price'),
            currency
        )

        # Determine pricing strategy
        pricing_strategy = 'inherit'
        variant_price = None

        if regular_price and product.price and regular_price != product.price:
            pricing_strategy = 'custom'
            variant_price = regular_price

        # Transform dimensions
        dimensions = variation_data.get('dimensions', {})

        # Create variant
        variant = ProductVariant.objects.create(
            product=product,
            external_id=external_id,
            name=variant_name,
            sku=sku,
            pricing_strategy=pricing_strategy,
            price=variant_price,
            weight=transform_decimal_nullable(variation_data.get('weight')),
            length=transform_decimal_nullable(dimensions.get('length')),
            width=transform_decimal_nullable(dimensions.get('width')),
            height=transform_decimal_nullable(dimensions.get('height')),
            is_active=variation_data.get('status', 'publish') == 'publish',
            imported_meta={
                'woocommerce_id': external_id,
                'stock_status': variation_data.get('stock_status'),
                'stock_quantity': variation_data.get('stock_quantity'),
                'manage_stock': variation_data.get('manage_stock'),
                'original_attributes': wc_attributes,
            }
        )

        # Create stock item for variant inventory
        if self.default_warehouse and variation_data.get('manage_stock', False):
            variant_stock = transform_integer_nullable(variation_data.get('stock_quantity')) or 0
            StockItem.objects.create(
                product=product,
                warehouse=self.default_warehouse,
                variant=variant,
                on_hand=variant_stock,
                allocated=0,
            )

        # Link selected_attributes M2M
        for _, value in attribute_pairs:
            variant.selected_attributes.add(value)

        # Import variant image if present
        image_data = variation_data.get('image')
        if image_data and image_data.get('src'):
            self._import_variant_image(variant, image_data)

        logger.debug(f"Imported variant: {variant.name} (SKU: {variant.sku})")
        return variant

    def _import_variant_image(self, variant: ProductVariant, image_data: Dict):
        """
        Download and import variant-specific image.

        Args:
            variant: ProductVariant instance
            image_data: WooCommerce image data dict
        """
        from media_library.models import MediaThumbnail, ImageSizePreset

        try:
            img_url = image_data.get('src')
            if not img_url:
                return

            # Check for existing by external_id
            wc_image_id = str(image_data.get('id', ''))
            if wc_image_id:
                existing = MediaAsset.objects.filter(external_id=wc_image_id).first()
                if existing:
                    variant.image_asset = existing
                    variant.save(update_fields=['image_asset'])
                    return

            # Download image
            response = requests.get(img_url, timeout=30)
            response.raise_for_status()

            # Get filename
            filename = img_url.split('/')[-1].split('?')[0]
            if not filename:
                filename = f"variant_{variant.id}_image.jpg"

            # Detect MIME type
            ext = filename.lower().split('.')[-1] if '.' in filename else 'jpg'
            mime_type_map = {
                'jpg': 'image/jpeg',
                'jpeg': 'image/jpeg',
                'png': 'image/png',
                'gif': 'image/gif',
                'webp': 'image/webp',
            }
            mime_type = mime_type_map.get(ext, 'image/jpeg')

            # Create MediaAsset
            media_asset = MediaAsset.objects.create(
                external_id=wc_image_id,
                migration_job=self.job,
                title=image_data.get('name') or f"{variant.name} Image",
                alt_text=image_data.get('alt') or variant.name,
                mime_type=mime_type,
                file_size=len(response.content),
            )

            # Save original file
            media_asset.original_file.save(
                filename,
                ContentFile(response.content),
                save=True
            )

            # Generate WebP version
            try:
                from media_library.services import ImageProcessor
                processor = ImageProcessor()
                if mime_type != 'image/svg+xml':
                    webp_content = processor.convert_to_webp(media_asset.original_file)
                    if webp_content:
                        webp_filename = f"{media_asset.id}.webp"
                        media_asset.webp_file.save(webp_filename, webp_content, save=True)
            except Exception as e:
                logger.debug(f"Failed to generate WebP for variant image: {e}")

            # Generate thumbnails
            try:
                from media_library.services import ImageProcessor
                processor = ImageProcessor()
                for preset in ImageSizePreset.objects.filter(is_active=True):
                    original_content, webp_content = processor.generate_thumbnail(
                        media_asset.original_file,
                        preset.width,
                        preset.height,
                        crop_mode=preset.crop_mode
                    )
                    if original_content:
                        thumbnail = MediaThumbnail.objects.create(
                            media_asset=media_asset,
                            size_preset=preset.slug,
                            width=preset.width,
                            height=preset.height
                        )
                        thumbnail.file.save(
                            f"{media_asset.id}_{preset.slug}.jpg",
                            original_content,
                            save=False
                        )
                        if webp_content:
                            thumbnail.webp_file.save(
                                f"{media_asset.id}_{preset.slug}.webp",
                                webp_content,
                                save=False
                            )
                        thumbnail.save()
            except Exception as e:
                logger.debug(f"Failed to generate thumbnails for variant image: {e}")

            # Link to variant
            variant.image_asset = media_asset
            variant.save(update_fields=['image_asset'])

            logger.debug(f"Imported image for variant {variant.name}")

        except Exception as e:
            logger.warning(f"Failed to import image for variant {variant.name}: {e}")

    def _get_unique_variant_sku(self, sku: str) -> str:
        """Generate unique SKU for variant."""
        if not sku:
            import time
            sku = f"VAR-{int(time.time())}"

        original_sku = sku
        counter = 1

        while ProductVariant.objects.filter(sku=sku).exists():
            sku = f"{original_sku}-{counter}"
            counter += 1

        return sku

    def _import_customers(self):
        """Import customers with User model and Address records"""
        # Create migration step
        step = MigrationStep.objects.create(
            job=self.job,
            step_type='customers',
            status='running',
            started_at=timezone.now(),
        )
        self.current_step = step

        self._log('info', "Starting customer import...")

        try:
            # Fetch all customers from WooCommerce
            customers = []
            page = 1
            per_page = 100

            while True:
                batch = self.client.fetch_customers(page=page, per_page=per_page)
                if not batch:
                    break
                customers.extend(batch)
                page += 1

                if len(batch) < per_page:
                    break

            # Use saved count from wizard preview, fallback to fetched count
            step.items_total = self.job.connection_config.get('total_customers', len(customers))
            step.save()

            self._log('info', f"Fetched {len(customers)} customers from WooCommerce")

            # Import each customer with progress bar
            with tqdm(total=len(customers), desc="Importing customers") as pbar:
                for customer_data in customers:
                    try:
                        self._import_single_customer(customer_data, step)
                        pbar.update(1)
                    except Exception as e:
                        self._log('error', f"Failed to import customer {customer_data.get('id')}: {e}",
                                 source_type='customer', source_id=str(customer_data.get('id')))
                        self._quarantine_item(customer_data, 'customer', str(e))
                        step.items_failed += 1
                        step.save()
                        pbar.update(1)

            # Mark step as complete
            step.status = 'completed'
            step.completed_at = timezone.now()
            step.duration_seconds = (step.completed_at - step.started_at).total_seconds()
            step.save()

            # Update job statistics
            self.job.customers_imported = step.items_imported
            self.job.customers_failed = step.items_failed
            self.job.customers_skipped = step.items_skipped
            self.job.save()

            # Update overall progress
            self._update_overall_progress()

            self._log('info', f"Customer import complete: {step.items_imported} imported, {step.items_failed} failed")

        except Exception as e:
            step.status = 'failed'
            step.error_message = str(e)
            step.completed_at = timezone.now()
            step.save()
            raise

    def _import_single_customer(self, customer_data: Dict, step: MigrationStep) -> Optional[User]:
        """Import a single customer with User and CustomerProfile"""
        external_id = str(customer_data.get('id'))
        email = customer_data.get('email')

        if not email:
            raise ValueError("Customer has no email address")

        # Check if customer already imported by external_id
        existing_profile = CustomerProfile.objects.filter(external_id=external_id).first()
        if existing_profile:
            logger.debug(f"Customer {external_id} already imported, skipping")
            step.items_skipped += 1
            step.save()
            return existing_profile.user

        # Check if user with this email already exists
        existing_user = User.objects.filter(email=email).first()
        if existing_user:
            # User exists but wasn't imported as a customer yet - link it
            profile, created = CustomerProfile.objects.get_or_create(
                user=existing_user,
                defaults={
                    'external_id': external_id,
                    'migration_job': self.job,
                    'phone': customer_data.get('billing', {}).get('phone', ''),
                }
            )
            if not created:
                # Profile already exists, just update external_id if not set
                if not profile.external_id:
                    profile.external_id = external_id
                    profile.migration_job = self.job
                    profile.save()

            # Count as imported (not skipped) since we successfully linked the customer data
            step.items_imported += 1
            step.save()
            logger.debug(f"Linked existing user {email} to WooCommerce customer {external_id}")
            return existing_user

        # Generate username from email or use WooCommerce username
        username = customer_data.get('username') or email.split('@')[0]

        # Ensure username is unique
        original_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{original_username}{counter}"
            counter += 1

        # Create User
        user = User.objects.create(
            username=username,
            email=email,
            first_name=customer_data.get('first_name', ''),
            last_name=customer_data.get('last_name', ''),
            date_joined=timezone.datetime.fromisoformat(customer_data.get('date_created', '').replace('Z', '+00:00'))
                if customer_data.get('date_created') else timezone.now(),
            is_active=True,
        )

        # Set unusable password (users will need to reset)
        user.set_unusable_password()
        user.save()

        # Create CustomerProfile with external_id
        CustomerProfile.objects.create(
            user=user,
            external_id=external_id,
            migration_job=self.job,
            phone=customer_data.get('billing', {}).get('phone', ''),
        )

        # Create billing address if provided
        billing = customer_data.get('billing', {})
        if billing.get('address_1'):
            Address.objects.create(
                user=user,
                address_type='billing',
                name=f"{billing.get('first_name', '')} {billing.get('last_name', '')}".strip(),
                company=billing.get('company', ''),
                address1=billing.get('address_1', ''),
                address2=billing.get('address_2', ''),
                city=billing.get('city', ''),
                state=billing.get('state', ''),
                postal_code=billing.get('postcode', ''),
                country=billing.get('country', ''),
                phone=billing.get('phone', ''),
                is_default=True,
            )

        # Create shipping address if provided and different from billing
        shipping = customer_data.get('shipping', {})
        if shipping.get('address_1'):
            # Check if shipping is different from billing
            is_different = (
                shipping.get('address_1') != billing.get('address_1') or
                shipping.get('city') != billing.get('city') or
                shipping.get('postcode') != billing.get('postcode')
            )

            if is_different:
                Address.objects.create(
                    user=user,
                    address_type='shipping',
                    name=f"{shipping.get('first_name', '')} {shipping.get('last_name', '')}".strip(),
                    company=shipping.get('company', ''),
                    address1=shipping.get('address_1', ''),
                    address2=shipping.get('address_2', ''),
                    city=shipping.get('city', ''),
                    state=shipping.get('state', ''),
                    postal_code=shipping.get('postcode', ''),
                    country=shipping.get('country', ''),
                    phone=billing.get('phone', ''),  # Use billing phone as shipping often doesn't have one
                    is_default=True,
                )

        step.items_imported += 1
        step.save()

        logger.debug(f"Imported customer: {user.email}")
        return user

    def _import_orders(self):
        """Import orders with OrderItem line items"""
        # Create migration step
        step = MigrationStep.objects.create(
            job=self.job,
            step_type='orders',
            status='running',
            started_at=timezone.now(),
        )
        self.current_step = step

        self._log('info', "Starting order import...")

        try:
            # Fetch all orders from WooCommerce
            orders = []
            page = 1
            per_page = 100

            while True:
                batch = self.client.fetch_orders(page=page, per_page=per_page)
                if not batch:
                    break
                orders.extend(batch)
                page += 1

                if len(batch) < per_page:
                    break

            # Use saved count from wizard preview, fallback to fetched count
            step.items_total = self.job.connection_config.get('total_orders', len(orders))
            step.save()

            self._log('info', f"Fetched {len(orders)} orders from WooCommerce")

            # Import each order with progress bar
            with tqdm(total=len(orders), desc="Importing orders") as pbar:
                for order_data in orders:
                    try:
                        self._import_single_order(order_data, step)
                        pbar.update(1)
                    except Exception as e:
                        self._log('error', f"Failed to import order {order_data.get('id')}: {e}",
                                 source_type='order', source_id=str(order_data.get('id')))
                        self._quarantine_item(order_data, 'order', str(e))
                        step.items_failed += 1
                        step.save()
                        pbar.update(1)

            # Mark step as complete
            step.status = 'completed'
            step.completed_at = timezone.now()
            step.duration_seconds = (step.completed_at - step.started_at).total_seconds()
            step.save()

            # Update job statistics
            self.job.orders_imported = step.items_imported
            self.job.orders_failed = step.items_failed
            self.job.orders_skipped = step.items_skipped
            self.job.save()

            # Update overall progress
            self._update_overall_progress()

            self._log('info', f"Order import complete: {step.items_imported} imported, {step.items_failed} failed")

        except Exception as e:
            step.status = 'failed'
            step.error_message = str(e)
            step.completed_at = timezone.now()
            step.save()
            raise

    def _import_single_order(self, order_data: Dict, step: MigrationStep) -> Optional[Order]:
        """Import a single order with OrderItem line items"""
        external_id = str(order_data.get('id'))

        # Check if order already imported by order_number or external check
        existing_order = Order.objects.filter(order_number=order_data.get('number')).first()
        if existing_order:
            logger.debug(f"Order {external_id} already imported, skipping")
            step.items_skipped += 1
            step.save()
            return existing_order

        # Find customer by WooCommerce customer_id
        user = None
        customer_id = order_data.get('customer_id')
        if customer_id and customer_id > 0:
            profile = CustomerProfile.objects.filter(external_id=str(customer_id)).first()
            if profile:
                user = profile.user
            else:
                # Customer not found - try to find by email
                email = order_data.get('billing', {}).get('email')
                if email:
                    user = User.objects.filter(email=email).first()

        # If no user found, create a guest user
        if not user:
            email = order_data.get('billing', {}).get('email', f'guest_{external_id}@example.com')
            username = f'guest_{external_id}'

            # Check if guest user already exists (from previous import attempts)
            existing_guest = User.objects.filter(username=username).first()
            if existing_guest:
                user = existing_guest
            else:
                user = User.objects.create(
                    username=username,
                    email=email,
                    first_name=order_data.get('billing', {}).get('first_name', 'Guest'),
                    last_name=order_data.get('billing', {}).get('last_name', ''),
                    is_active=False,  # Guest users are inactive per django-SHOP best practices
                )
                user.set_unusable_password()
                user.save()

        # Map WooCommerce status to platform status
        status_mapping = {
            'pending': 'pending',
            'processing': 'processing',
            'on-hold': 'pending',
            'completed': 'delivered',
            'cancelled': 'cancelled',
            'refunded': 'refunded',
            'failed': 'cancelled',
        }
        status = status_mapping.get(order_data.get('status', 'pending'), 'pending')

        # Get currency
        currency = order_data.get('currency') or self._get_currency()

        # Create Order
        billing = order_data.get('billing', {})
        shipping = order_data.get('shipping', {})

        order = Order.objects.create(
            order_number=order_data.get('number', external_id),
            user=user,
            external_id=external_id,
            migration_job=self.job,
            status=status,
            email=billing.get('email', ''),
            phone=billing.get('phone', ''),
            # Shipping address
            shipping_name=f"{shipping.get('first_name', '')} {shipping.get('last_name', '')}".strip() or billing.get('first_name', ''),
            shipping_address1=shipping.get('address_1', '') or billing.get('address_1', ''),
            shipping_address2=shipping.get('address_2', ''),
            shipping_city=shipping.get('city', '') or billing.get('city', ''),
            shipping_state=shipping.get('state', '') or billing.get('state', ''),
            shipping_postal_code=shipping.get('postcode', '') or billing.get('postcode', ''),
            shipping_country=shipping.get('country', '') or billing.get('country', ''),
            # Billing address
            billing_same_as_shipping=False,
            billing_name=f"{billing.get('first_name', '')} {billing.get('last_name', '')}".strip(),
            billing_address1=billing.get('address_1', ''),
            billing_address2=billing.get('address_2', ''),
            billing_city=billing.get('city', ''),
            billing_state=billing.get('state', ''),
            billing_postal_code=billing.get('postcode', ''),
            billing_country=billing.get('country', ''),
            # Totals
            subtotal=transform_money(order_data.get('total', 0), currency),
            tax_amount=transform_money(order_data.get('total_tax', 0), currency),
            shipping_cost=transform_money(order_data.get('shipping_total', 0), currency),
            discount_amount=transform_money(order_data.get('discount_total', 0), currency),
            total_amount=transform_money(order_data.get('total', 0), currency),
            # Notes
            special_instructions=order_data.get('customer_note', ''),
            # Language — use source data if available, otherwise site default
            language=order_data.get('language', '') or self._get_site_default_language(),
            created_at=timezone.datetime.fromisoformat(order_data.get('date_created', '').replace('Z', '+00:00'))
                if order_data.get('date_created') else timezone.now(),
        )

        # Import order line items
        line_items = order_data.get('line_items', [])
        for item_data in line_items:
            try:
                self._import_order_item(order, item_data, currency)
            except Exception as e:
                logger.warning(f"Failed to import order item for order {order.order_number}: {e}")
                # Continue with other items

        step.items_imported += 1
        step.save()

        logger.debug(f"Imported order: {order.order_number}")
        return order

    def _get_site_default_language(self):
        """Get site default language for imported records."""
        try:
            from core.models import SiteSettings
            return SiteSettings.get_settings().default_language or 'en'
        except Exception:
            return 'en'

    def _import_order_item(self, order: Order, item_data: Dict, currency: str):
        """Import a single order line item"""
        product_id = item_data.get('product_id')
        variant_id = item_data.get('variation_id')

        # Find product by external_id
        product = None
        variant = None

        if product_id:
            product = Product.objects.filter(external_id=str(product_id)).first()

        if variant_id and variant_id > 0:
            variant = ProductVariant.objects.filter(external_id=str(variant_id)).first()

        if not product:
            # Product not found - skip this line item
            logger.warning(f"Product {product_id} not found for order {order.order_number}, skipping line item")
            return

        # Create OrderItem
        OrderItem.objects.create(
            order=order,
            product=product,
            variant=variant,
            product_name=item_data.get('name', product.name),
            sku=item_data.get('sku', product.sku),
            quantity=item_data.get('quantity', 1),
            unit_price=transform_money(item_data.get('price', 0), currency),
            total_price=transform_money(item_data.get('total', 0), currency),
        )

    def _import_reviews(self):
        """Import product reviews with external_id product matching"""
        # Create migration step
        step = MigrationStep.objects.create(
            job=self.job,
            step_type='reviews',
            status='running',
            started_at=timezone.now(),
        )
        self.current_step = step

        self._log('info', "Starting review import...")

        try:
            # Fetch all reviews from WooCommerce
            reviews = []
            page = 1
            per_page = 100

            while True:
                batch = self.client.fetch_reviews(page=page, per_page=per_page)
                if not batch:
                    break
                reviews.extend(batch)
                page += 1

                if len(batch) < per_page:
                    break

            # Use saved count from wizard preview, fallback to fetched count
            step.items_total = self.job.connection_config.get('total_reviews', len(reviews))
            step.save()

            self._log('info', f"Fetched {len(reviews)} reviews from WooCommerce")

            # Import each review with progress bar
            with tqdm(total=len(reviews), desc="Importing reviews") as pbar:
                for review_data in reviews:
                    try:
                        self._import_single_review(review_data, step)
                        pbar.update(1)
                    except Exception as e:
                        self._log('error', f"Failed to import review {review_data.get('id')}: {e}",
                                 source_type='review', source_id=str(review_data.get('id')))
                        self._quarantine_item(review_data, 'review', str(e))
                        step.items_failed += 1
                        step.save()
                        pbar.update(1)

            # Mark step as complete
            step.status = 'completed'
            step.completed_at = timezone.now()
            step.duration_seconds = (step.completed_at - step.started_at).total_seconds()
            step.save()

            # Update job statistics
            self.job.reviews_imported = step.items_imported
            self.job.reviews_failed = step.items_failed
            self.job.reviews_skipped = step.items_skipped
            self.job.save()

            # Update overall progress
            self._update_overall_progress()

            self._log('info', f"Review import complete: {step.items_imported} imported, {step.items_failed} failed")

        except Exception as e:
            step.status = 'failed'
            step.error_message = str(e)
            step.completed_at = timezone.now()
            step.save()
            raise

    def _import_single_review(self, review_data: Dict, step: MigrationStep) -> Optional[ProductReview]:
        """Import a single product review"""
        external_id = str(review_data.get('id'))
        product_id = str(review_data.get('product_id'))

        # Find product by external_id
        product = Product.objects.filter(external_id=product_id).first()
        if not product:
            raise ValueError(f"Product {product_id} not found for review")

        # Find user by email or create anonymous guest user
        reviewer_email = review_data.get('reviewer_email')
        reviewer_name = review_data.get('reviewer', 'Anonymous')
        user = None

        if reviewer_email:
            user = User.objects.filter(email=reviewer_email).first()

        if not user:
            # Create anonymous guest user for reviewers without accounts
            # This handles WooCommerce's feature allowing unregistered users to review
            username = f'guest_reviewer_{external_id}'
            email = reviewer_email or f'guest_reviewer_{external_id}@anonymous.local'

            user = User.objects.create(
                username=username,
                email=email,
                first_name=reviewer_name.split()[0] if reviewer_name else 'Anonymous',
                last_name=' '.join(reviewer_name.split()[1:]) if len(reviewer_name.split()) > 1 else '',
                is_active=False,  # Mark guest reviewers as inactive
            )
            user.set_unusable_password()
            user.save()

            logger.debug(f"Created anonymous guest user for reviewer: {reviewer_name}")

        # Check if review already exists (unique constraint on product + user)
        existing_review = ProductReview.objects.filter(product=product, user=user).first()
        if existing_review:
            logger.debug(f"Review already exists for product {product.name} by {user.email}, skipping")
            step.items_skipped += 1
            step.save()
            return existing_review

        # Generate title from comment (WooCommerce doesn't have title field)
        comment = review_data.get('review', '')
        clean_text = strip_tags(comment).strip()
        title = clean_text[:50] if len(clean_text) > 50 else clean_text
        if not title:
            title = f"Review by {user.username}"

        # Map status to is_approved
        is_approved = review_data.get('status') == 'approved'

        # Create ProductReview
        review = ProductReview.objects.create(
            product=product,
            user=user,
            external_id=external_id,
            migration_job=self.job,
            rating=min(5, max(1, int(review_data.get('rating', 5)))),  # Ensure 1-5 range
            title=title,
            comment=comment,
            is_verified_purchase=review_data.get('verified', False),
            is_approved=is_approved,
            created_at=timezone.datetime.fromisoformat(review_data.get('date_created', '').replace('Z', '+00:00'))
                if review_data.get('date_created') else timezone.now(),
        )

        step.items_imported += 1
        step.save()

        logger.debug(f"Imported review for product {product.name} by {user.email}")
        return review

    def _import_coupons(self):
        """Import coupons/vouchers with discount type mapping"""
        # Create migration step
        step = MigrationStep.objects.create(
            job=self.job,
            step_type='coupons',
            status='running',
            started_at=timezone.now(),
        )
        self.current_step = step

        self._log('info', "Starting coupon import...")

        try:
            # Fetch all coupons from WooCommerce
            coupons = []
            page = 1
            per_page = 100

            while True:
                batch = self.client.fetch_coupons(page=page, per_page=per_page)
                if not batch:
                    break
                coupons.extend(batch)
                page += 1

                if len(batch) < per_page:
                    break

            # Use saved count from wizard preview, fallback to fetched count
            step.items_total = self.job.connection_config.get('total_coupons', len(coupons))
            step.save()

            self._log('info', f"Fetched {len(coupons)} coupons from WooCommerce")

            # Import each coupon with progress bar
            with tqdm(total=len(coupons), desc="Importing coupons") as pbar:
                for coupon_data in coupons:
                    try:
                        self._import_single_coupon(coupon_data, step)
                        pbar.update(1)
                    except Exception as e:
                        self._log('error', f"Failed to import coupon {coupon_data.get('id')}: {e}",
                                 source_type='coupon', source_id=str(coupon_data.get('id')))
                        self._quarantine_item(coupon_data, 'coupon', str(e))
                        step.items_failed += 1
                        step.save()
                        pbar.update(1)

            # Mark step as complete
            step.status = 'completed'
            step.completed_at = timezone.now()
            step.duration_seconds = (step.completed_at - step.started_at).total_seconds()
            step.save()

            # Update job statistics
            self.job.coupons_imported = step.items_imported
            self.job.coupons_failed = step.items_failed
            self.job.coupons_skipped = step.items_skipped
            self.job.save()

            # Update overall progress
            self._update_overall_progress()

            self._log('info', f"Coupon import complete: {step.items_imported} imported, {step.items_failed} failed")

        except Exception as e:
            step.status = 'failed'
            step.error_message = str(e)
            step.completed_at = timezone.now()
            step.save()
            raise

    def _import_single_coupon(self, coupon_data: Dict, step: MigrationStep) -> Optional[VoucherCode]:
        """Import a single coupon/voucher"""
        external_id = str(coupon_data.get('id'))
        code = coupon_data.get('code')

        if not code:
            raise ValueError("Coupon has no code")

        # Check if voucher already exists by code
        existing_voucher = VoucherCode.objects.filter(code=code).first()
        if existing_voucher:
            logger.debug(f"Voucher {code} already exists, skipping")
            step.items_skipped += 1
            step.save()
            return existing_voucher

        # Map WooCommerce discount type to platform discount type
        discount_type_mapping = {
            'percent': 'percentage',
            'fixed_cart': 'fixed',
            'fixed_product': 'fixed',
        }
        wc_discount_type = coupon_data.get('discount_type', 'percent')
        discount_type = discount_type_mapping.get(wc_discount_type, 'percentage')

        # Get currency
        currency = self._get_currency()

        # Parse expiry date
        end_date = None
        if coupon_data.get('date_expires'):
            end_date = timezone.datetime.fromisoformat(coupon_data.get('date_expires').replace('Z', '+00:00'))

        # Create VoucherCode
        voucher = VoucherCode.objects.create(
            code=code.upper(),  # Store codes in uppercase
            name=coupon_data.get('description', code) or code,
            description=coupon_data.get('description', ''),
            external_id=external_id,
            migration_job=self.job,
            discount_type=discount_type,
            discount_value=Decimal(coupon_data.get('amount', 0)),
            max_discount_amount=transform_money(coupon_data.get('maximum_amount', 0), currency) if coupon_data.get('maximum_amount') else None,
            application_scope='cart',  # WooCommerce coupons apply to cart
            end_date=end_date,
            max_uses_total=coupon_data.get('usage_limit') if coupon_data.get('usage_limit') else None,
            max_uses_per_customer=coupon_data.get('usage_limit_per_user') if coupon_data.get('usage_limit_per_user') else None,
            current_uses=coupon_data.get('usage_count', 0),
            min_order_value=transform_money(coupon_data.get('minimum_amount', 0), currency) if coupon_data.get('minimum_amount') else None,
            exclude_sale_items=coupon_data.get('exclude_sale_items', False),
            cannot_combine_with_other_vouchers=coupon_data.get('individual_use', False),
            is_active=True,
        )

        # Link eligible products if specified
        product_ids = coupon_data.get('product_ids', [])
        if product_ids:
            products = Product.objects.filter(external_id__in=[str(pid) for pid in product_ids])
            voucher.eligible_products.set(products)

        # Link eligible categories if specified
        category_ids = coupon_data.get('product_categories', [])
        if category_ids:
            categories = Category.objects.filter(external_id__in=[str(cid) for cid in category_ids])
            voucher.eligible_categories.set(categories)

        step.items_imported += 1
        step.save()

        logger.debug(f"Imported coupon: {voucher.code}")
        return voucher

    def _get_product_category(self, product_data: Dict) -> Optional[Category]:
        """Get or create category for product"""
        categories = product_data.get('categories', [])

        if not categories:
            # Get or create "Uncategorized" category
            category, _ = Category.objects.get_or_create(
                slug='uncategorized',
                defaults={
                    'name': 'Uncategorized',
                    'description': 'Products without a category',
                    'is_active': True,
                }
            )
            return category

        # Use first category (or primary category from Yoast SEO if available)
        primary_cat_id = None
        for meta_item in product_data.get('meta_data', []):
            if meta_item.get('key') == '_yoast_wpseo_primary_product_cat':
                primary_cat_id = str(meta_item.get('value'))
                break

        # Find category by external_id
        if primary_cat_id:
            category = Category.objects.filter(external_id=primary_cat_id).first()
            if category:
                return category

        # Fallback to first category
        first_cat_id = str(categories[0].get('id'))
        category = Category.objects.filter(external_id=first_cat_id).first()

        if not category:
            # Create category if it doesn't exist
            cat_data = categories[0]
            category = Category.objects.create(
                external_id=first_cat_id,
                migration_job=self.job,
                name=cat_data.get('name', 'Unknown'),
                slug=self._get_unique_slug(cat_data.get('slug', 'unknown'), Category),
                is_active=True,
            )

        return category

    def _apply_mappings(self, source_data: Dict, source_type: str) -> Dict:
        """Apply field mappings to source data"""
        mapped_data = {}

        for source_field, value in source_data.items():
            key = f"{source_type}.{source_field}"

            if key in self.field_mappings:
                mapping = self.field_mappings[key]
                dest_field = mapping['dest_field']
                transform_type = mapping['transform_type']

                # Apply transformation
                transformed_value = self._apply_transform(value, transform_type)
                mapped_data[dest_field] = transformed_value

        return mapped_data

    def _apply_transform(self, value: Any, transform_type: str) -> Any:
        """Apply transformation to a value"""
        if not value or transform_type == 'none':
            return value

        try:
            if transform_type == 'string':
                return str(value)
            elif transform_type == 'integer':
                return int(value)
            elif transform_type == 'integer_nullable':
                return transform_integer_nullable(value)
            elif transform_type == 'decimal':
                return Decimal(str(value))
            elif transform_type == 'decimal_nullable':
                return transform_decimal_nullable(value)
            elif transform_type == 'boolean':
                return bool(value)
            elif transform_type == 'money':
                return transform_money(value)
            elif transform_type == 'woocommerce_status':
                return transform_woocommerce_status(value)
            elif transform_type == 'woocommerce_type':
                return transform_woocommerce_type(value)
            elif transform_type == 'woocommerce_backorders':
                return transform_woocommerce_backorders(value)
            else:
                return value
        except Exception as e:
            logger.warning(f"Transform failed ({transform_type}): {e}")
            return value

    def _quarantine_item(self, source_data: Dict, item_type: str, error_message: str):
        """Quarantine an item that failed to import"""
        external_id = str(source_data.get('id', 'unknown'))

        MigrationStagedItem.objects.create(
            job=self.job,
            item_type=item_type,
            external_id=external_id,
            source_data=source_data,
            failure_reason='validation_failed',
            error_message=error_message,
            status='pending_review',
        )

        logger.info(f"Quarantined {item_type} {external_id} for review")

    def _get_unique_slug(self, slug: str, model_class) -> str:
        """Generate unique slug"""
        if not slug:
            slug = 'item'

        original_slug = slug
        counter = 1

        while model_class.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1

        return slug

    def _get_unique_sku(self, sku: str) -> str:
        """Generate unique SKU"""
        if not sku:
            import time
            sku = f"SKU-{int(time.time())}"

        original_sku = sku
        counter = 1

        while Product.objects.filter(sku=sku).exists():
            sku = f"{original_sku}-{counter}"
            counter += 1

        return sku

    def _update_overall_progress(self):
        """Calculate and update overall progress percentage based on total items across all steps"""
        steps = self.job.steps.all()
        if not steps.exists():
            self.job.progress_percent = 0
            self.job.save()
            return

        # Calculate based on total items across ALL imports, not average of steps
        total_items = sum(step.items_total for step in steps if step.items_total > 0)
        total_processed = sum(
            step.items_imported + step.items_skipped + step.items_failed
            for step in steps
        )

        if total_items > 0:
            self.job.progress_percent = int((total_processed / total_items) * 100)
        else:
            self.job.progress_percent = 0

        self.job.save()

    def _import_blog(self):
        """Import WordPress blog posts, categories, and tags"""
        # Create migration step
        step = MigrationStep.objects.create(
            job=self.job,
            step_type='blog',
            status='running',
            started_at=timezone.now(),
        )
        self.current_step = step

        self._log('info', "Starting WordPress blog import...")

        try:
            # Get WordPress site URL (same as WooCommerce store URL)
            store_url = self.job.connection_config.get('store_url', '')

            if not store_url:
                raise ValueError("Store URL is required for blog import")

            # Create blog importer
            config = self.job.connection_config or {}
            skip_existing = config.get('skip_existing', True)
            blog_importer = WordPressBlogImporter(
                source_url=store_url,
                migration_job=self.job,
                skip_existing=skip_existing,
            )

            # Run the import with real-time step progress tracking
            stats = blog_importer.import_all(progress_bar=True, step=step)

            # Update step statistics
            cat_stats = stats.get('categories', {})
            tag_stats = stats.get('tags', {})
            post_stats = stats.get('posts', {})
            media_stats = stats.get('media', {})

            step.items_total = (
                cat_stats.get('created', 0) + cat_stats.get('updated', 0) + cat_stats.get('skipped', 0) + cat_stats.get('errors', 0) +
                tag_stats.get('created', 0) + tag_stats.get('updated', 0) + tag_stats.get('skipped', 0) + tag_stats.get('errors', 0) +
                post_stats.get('created', 0) + post_stats.get('updated', 0) + post_stats.get('skipped', 0) + post_stats.get('errors', 0)
            )
            step.items_imported = (
                cat_stats.get('created', 0) + cat_stats.get('updated', 0) +
                tag_stats.get('created', 0) + tag_stats.get('updated', 0) +
                post_stats.get('created', 0) + post_stats.get('updated', 0)
            )
            step.items_skipped = (
                cat_stats.get('skipped', 0) +
                tag_stats.get('skipped', 0) +
                post_stats.get('skipped', 0)
            )
            step.items_failed = (
                cat_stats.get('errors', 0) +
                tag_stats.get('errors', 0) +
                post_stats.get('errors', 0)
            )

            # Mark step as complete
            step.status = 'completed'
            step.completed_at = timezone.now()
            step.duration_seconds = (step.completed_at - step.started_at).total_seconds()
            step.save()

            # Update job blog statistics
            self.job.blog_categories_total = cat_stats.get('created', 0) + cat_stats.get('updated', 0) + cat_stats.get('skipped', 0) + cat_stats.get('errors', 0)
            self.job.blog_categories_imported = cat_stats.get('created', 0) + cat_stats.get('updated', 0)
            self.job.blog_categories_skipped = cat_stats.get('skipped', 0)
            self.job.blog_categories_failed = cat_stats.get('errors', 0)

            self.job.blog_tags_total = tag_stats.get('created', 0) + tag_stats.get('updated', 0) + tag_stats.get('skipped', 0) + tag_stats.get('errors', 0)
            self.job.blog_tags_imported = tag_stats.get('created', 0) + tag_stats.get('updated', 0)
            self.job.blog_tags_skipped = tag_stats.get('skipped', 0)
            self.job.blog_tags_failed = tag_stats.get('errors', 0)

            self.job.blog_posts_total = post_stats.get('created', 0) + post_stats.get('updated', 0) + post_stats.get('skipped', 0) + post_stats.get('errors', 0)
            self.job.blog_posts_imported = post_stats.get('created', 0) + post_stats.get('updated', 0)
            self.job.blog_posts_skipped = post_stats.get('skipped', 0)
            self.job.blog_posts_failed = post_stats.get('errors', 0)

            self.job.media_imported = (self.job.media_imported or 0) + media_stats.get('imported', 0)
            self.job.save()

            # Update overall progress
            self._update_overall_progress()

            self._log('info',
                f"Blog import complete: "
                f"{self.job.blog_posts_imported} posts, "
                f"{self.job.blog_categories_imported} categories, "
                f"{self.job.blog_tags_imported} tags, "
                f"{media_stats.get('imported', 0)} media assets"
            )

        except Exception as e:
            step.status = 'failed'
            step.error_message = str(e)
            step.completed_at = timezone.now()
            step.save()
            self._log('error', f"Blog import failed: {e}")
            raise

    def _import_affiliates(self):
        """Import affiliate data from WordPress via Spwig Migration Bridge plugin."""
        # Create migration steps for each sub-type
        affiliates_step = MigrationStep.objects.create(
            job=self.job,
            step_type='affiliates',
            status='running',
            started_at=timezone.now(),
        )
        commissions_step = MigrationStep.objects.create(
            job=self.job,
            step_type='commissions',
            status='pending',
        )
        payouts_step = MigrationStep.objects.create(
            job=self.job,
            step_type='payouts',
            status='pending',
        )
        self.current_step = affiliates_step

        self._log('info', "Starting affiliate data import via Spwig Bridge...")

        try:
            config = self.job.connection_config or {}
            store_url = config.get('store_url', '')
            consumer_key = config.get('consumer_key', '')
            consumer_secret = config.get('consumer_secret', '')

            if not store_url:
                raise ValueError("Store URL is required for affiliate import")

            # Create bridge API client (same WC credentials)
            bridge_client = SpwigBridgeAPIClient(
                store_url=store_url,
                consumer_key=consumer_key,
                consumer_secret=consumer_secret,
            )

            # Create importer and run
            importer = AffiliateImporter(
                bridge_client=bridge_client,
                migration_job=self.job,
            )
            stats = importer.import_all(progress_bar=True)

            # Update affiliates step
            aff_stats = stats.get('affiliates', {})
            prog_stats = stats.get('programs', {})
            affiliates_step.items_total = (
                aff_stats.get('created', 0) + aff_stats.get('skipped', 0) +
                aff_stats.get('errors', 0)
            )
            affiliates_step.items_imported = aff_stats.get('created', 0)
            affiliates_step.items_skipped = aff_stats.get('skipped', 0)
            affiliates_step.items_failed = aff_stats.get('errors', 0)
            affiliates_step.status = 'completed'
            affiliates_step.completed_at = timezone.now()
            affiliates_step.duration_seconds = (
                affiliates_step.completed_at - affiliates_step.started_at
            ).total_seconds()
            affiliates_step.save()

            # Update commissions step
            comm_stats = stats.get('commissions', {})
            commissions_step.started_at = affiliates_step.completed_at
            commissions_step.status = 'completed'
            commissions_step.items_total = (
                comm_stats.get('created', 0) + comm_stats.get('skipped', 0) +
                comm_stats.get('errors', 0)
            )
            commissions_step.items_imported = comm_stats.get('created', 0)
            commissions_step.items_skipped = comm_stats.get('skipped', 0)
            commissions_step.items_failed = comm_stats.get('errors', 0)
            commissions_step.completed_at = timezone.now()
            commissions_step.duration_seconds = (
                commissions_step.completed_at - commissions_step.started_at
            ).total_seconds()
            commissions_step.save()

            # Update payouts step
            pay_stats = stats.get('payouts', {})
            payouts_step.started_at = commissions_step.completed_at
            payouts_step.status = 'completed'
            payouts_step.items_total = (
                pay_stats.get('created', 0) + pay_stats.get('skipped', 0) +
                pay_stats.get('errors', 0)
            )
            payouts_step.items_imported = pay_stats.get('created', 0)
            payouts_step.items_skipped = pay_stats.get('skipped', 0)
            payouts_step.items_failed = pay_stats.get('errors', 0)
            payouts_step.completed_at = timezone.now()
            payouts_step.duration_seconds = (
                payouts_step.completed_at - payouts_step.started_at
            ).total_seconds()
            payouts_step.save()

            # Update job statistics
            self.job.affiliates_total = aff_stats.get('created', 0) + aff_stats.get('skipped', 0) + aff_stats.get('errors', 0)
            self.job.affiliates_imported = aff_stats.get('created', 0)
            self.job.affiliates_skipped = aff_stats.get('skipped', 0)
            self.job.affiliates_failed = aff_stats.get('errors', 0)

            self.job.commissions_total = comm_stats.get('created', 0) + comm_stats.get('skipped', 0) + comm_stats.get('errors', 0)
            self.job.commissions_imported = comm_stats.get('created', 0)
            self.job.commissions_skipped = comm_stats.get('skipped', 0)
            self.job.commissions_failed = comm_stats.get('errors', 0)

            self.job.payouts_total = pay_stats.get('created', 0) + pay_stats.get('skipped', 0) + pay_stats.get('errors', 0)
            self.job.payouts_imported = pay_stats.get('created', 0)
            self.job.payouts_skipped = pay_stats.get('skipped', 0)
            self.job.payouts_failed = pay_stats.get('errors', 0)

            self.job.save()
            self._update_overall_progress()

            self._log('info',
                f"Affiliate import complete: "
                f"{prog_stats.get('created', 0)} programs, "
                f"{self.job.affiliates_imported} affiliates, "
                f"{self.job.commissions_imported} commissions "
                f"({comm_stats.get('orders_unlinked', 0)} skipped - orders not migrated), "
                f"{self.job.payouts_imported} payouts"
            )

        except Exception as e:
            for step in [affiliates_step, commissions_step, payouts_step]:
                if step.status not in ('completed', 'failed'):
                    step.status = 'failed'
                    step.error_message = str(e)
                    step.completed_at = timezone.now()
                    step.save()
            self._log('error', f"Affiliate import failed: {e}")
            raise

    def _scan_content_links(self):
        """
        Post-import: scan all imported content for internal links
        pointing to the old WordPress/WooCommerce site.

        Creates ContentLink records with auto-suggested replacement URLs.
        This runs after all content imports are complete.
        """
        from urllib.parse import urlparse
        from migration.services.content_link_processor import ContentLinkProcessor

        store_url = self.job.connection_config.get('store_url', '')
        if not store_url:
            self._log('warning', "No store_url in config, skipping link scan")
            return

        source_domain = urlparse(store_url).netloc
        if not source_domain:
            self._log('warning', f"Could not parse domain from store_url: {store_url}")
            return

        # Create migration step
        step = MigrationStep.objects.create(
            job=self.job,
            step_type='link_rewriting',
            status='running',
            started_at=timezone.now(),
        )
        self.current_step = step

        self._log('info', f"Scanning imported content for links from {source_domain}...")

        try:
            processor = ContentLinkProcessor(
                source_domain=source_domain,
                migration_job=self.job,
            )

            # Phase 1: Scan all imported content for same-origin links
            processor.scan_all_content()

            # Phase 2: Auto-match discovered links to Spwig objects
            processor.auto_match_links()

            stats = processor.get_stats()

            # Update step statistics
            step.items_total = stats['links_same_origin']
            step.items_imported = stats['links_matched']
            step.items_skipped = stats['links_external_skipped']
            step.items_failed = stats['links_unmatched']

            step.status = 'completed'
            step.completed_at = timezone.now()
            step.duration_seconds = int((step.completed_at - step.started_at).total_seconds())
            step.save()

            self._log('info',
                f"Link scan complete: {stats['links_same_origin']} internal links found, "
                f"{stats['links_matched']} auto-matched, "
                f"{stats['links_unmatched']} need manual review"
            )

        except Exception as e:
            step.status = 'failed'
            step.error_message = str(e)
            step.completed_at = timezone.now()
            step.save()
            self._log('warning', f"Link scanning failed (non-fatal): {e}")
            # Don't raise - link scanning failure should not fail the entire import
