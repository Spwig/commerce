"""
Magento 2 Import Execution Engine
Orchestrates the entire Magento import process with progress tracking, field mapping, and quarantine.

Handles Magento-specific structures:
- EAV attribute option pre-fetching and resolution
- Configurable product children fetched separately per parent
- Category tree flattening with parent resolution
- Image URLs constructed from relative paths
- CMS page directive cleanup
"""

import logging
from decimal import Decimal

import requests
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.utils import timezone
from tqdm import tqdm

from accounts.models import CustomerProfile
from catalog.models import (
    Category,
    Product,
    ProductImage,
    ProductVariant,
    StockItem,
    Warehouse,
)
from media_library.models import MediaAsset
from migration.fetchers.magento_api import MagentoAPIClient
from migration.mappers.magento import (
    MagentoCategoryMapper,
    MagentoCmsPageMapper,
    MagentoCouponMapper,
    MagentoCustomerMapper,
    MagentoOrderMapper,
    MagentoProductMapper,
    MagentoReviewMapper,
)
from migration.models import MigrationJob, MigrationLog, MigrationStagedItem, MigrationStep
from migration.utils.magento_transformers import resolve_attribute_label
from migration.utils.transformers import safe_money
from orders.models import Order, OrderItem
from vouchers.models import VoucherCode

User = get_user_model()

logger = logging.getLogger(__name__)


class MagentoImportExecutor:
    """
    Magento 2 import executor that orchestrates the entire migration process.

    Follows the same pattern as ShopifyImportExecutor but handles
    Magento-specific data structures:
    - searchCriteria-based pagination
    - EAV custom_attributes with option ID resolution
    - Configurable products as separate parent + child product records
    - Category tree (recursive, flattened for import)
    - Image URLs constructed from relative paths
    - CMS pages with {{directive}} cleanup
    """

    STEP_SAVE_INTERVAL = 25

    def __init__(self, migration_job: MigrationJob):
        self.job = migration_job
        self.client = None
        self.field_mappings = {}
        self.category_map = {}  # Maps external_id -> Category instance
        self.product_map = {}  # Maps external_id -> Product instance
        self.current_step = None
        self.default_warehouse = None

        # Performance caches
        self._existing_slugs = {}
        self._existing_skus = set()
        self._existing_variant_skus = set()
        self._step_dirty_count = 0
        self._image_session = None
        self._attribute_options_cache = {}

        # Initialize Magento client
        if self.job.platform == "magento" and self.job.connection_config:
            self.client = MagentoAPIClient(
                store_url=self.job.connection_config.get("store_url", ""),
                access_token=self.job.connection_config.get("access_token", ""),
                verify_ssl=self.job.connection_config.get("verify_ssl", True),
            )

        # Load field mappings
        self._load_field_mappings()

    def _get_currency(self):
        """Get currency from job config, falling back to merchant's default."""
        if self.job.connection_config:
            currency = self.job.connection_config.get("currency")
            if currency:
                return currency
        from core.utils import get_default_currency

        return get_default_currency()

    def _log(self, level: str, message: str, source_type: str = "system", source_id: str = ""):
        """Log to both Python logger and MigrationLog model."""
        getattr(logger, level.lower())(message)
        MigrationLog.objects.create(
            job=self.job,
            step=self.current_step,
            level=level,
            message=message,
            source_type=source_type,
            source_id=source_id,
        )

    def _load_field_mappings(self):
        """Load field mappings from MigrationMapping model."""
        mappings = self.job.mappings.all()
        for mapping in mappings:
            key = f"{mapping.source_type}.{mapping.source_field}"
            self.field_mappings[key] = {
                "dest_model": mapping.dest_model,
                "dest_field": mapping.dest_field,
                "transform_type": mapping.transform_type,
                "transform_function": mapping.transform_function,
            }
        logger.info(f"Loaded {len(self.field_mappings)} field mappings")

    def _get_image_session(self) -> requests.Session:
        """Get or create a persistent session for image downloads."""
        if self._image_session is None:
            self._image_session = requests.Session()
            self._image_session.verify = self.job.connection_config.get("verify_ssl", True)
            adapter = requests.adapters.HTTPAdapter(pool_connections=5, pool_maxsize=10)
            self._image_session.mount("https://", adapter)
            self._image_session.mount("http://", adapter)
        return self._image_session

    def _step_increment(self, step: MigrationStep, field: str, amount: int = 1):
        """Increment a step counter and batch-save to reduce DB writes."""
        current = getattr(step, field, 0)
        setattr(step, field, current + amount)
        self._step_dirty_count += 1
        if self._step_dirty_count >= self.STEP_SAVE_INTERVAL:
            step.save()
            self._step_dirty_count = 0

    def _step_flush(self, step: MigrationStep):
        """Flush any pending step counter changes to DB."""
        if self._step_dirty_count > 0:
            step.save()
            self._step_dirty_count = 0

    def _preload_slugs(self, model_class):
        """Pre-load all existing slugs for O(1) lookups."""
        if model_class not in self._existing_slugs:
            self._existing_slugs[model_class] = set(
                model_class.objects.values_list("slug", flat=True)
            )

    def _preload_skus(self):
        """Pre-load all existing SKUs for products and variants."""
        if not self._existing_skus:
            self._existing_skus = set(Product.objects.values_list("sku", flat=True))
        if not self._existing_variant_skus:
            self._existing_variant_skus = set(ProductVariant.objects.values_list("sku", flat=True))

    def _get_unique_slug(self, slug: str, model_class) -> str:
        """Generate a unique slug by appending a counter if needed."""
        if not slug:
            slug = "imported-item"
        self._preload_slugs(model_class)
        slugs = self._existing_slugs[model_class]
        if slug not in slugs:
            slugs.add(slug)
            return slug
        counter = 2
        while f"{slug}-{counter}" in slugs:
            counter += 1
        unique_slug = f"{slug}-{counter}"
        slugs.add(unique_slug)
        return unique_slug

    def _get_unique_sku(self, sku: str, is_variant: bool = False) -> str:
        """Generate a unique SKU by appending a counter if needed."""
        if not sku:
            return ""
        target_set = self._existing_variant_skus if is_variant else self._existing_skus
        if sku not in target_set:
            target_set.add(sku)
            return sku
        counter = 2
        while f"{sku}-{counter}" in target_set:
            counter += 1
        unique_sku = f"{sku}-{counter}"
        target_set.add(unique_sku)
        return unique_sku

    def _quarantine_item(self, source_data: dict, item_type: str, error_msg: str):
        """Store a failed item for later review."""
        try:
            MigrationStagedItem.objects.create(
                job=self.job,
                item_type=item_type,
                external_id=str(source_data.get("id") or source_data.get("entity_id", "")),
                source_data=source_data,
                status="pending_review",
                failure_reason="validation_failed",
                error_message=error_msg[:500],
            )
        except Exception as e:
            logger.warning(f"Failed to quarantine item: {e}")

    def _update_overall_progress(self):
        """Recalculate overall job progress from step completion."""
        steps = MigrationStep.objects.filter(job=self.job)
        total_steps = steps.count()
        if total_steps == 0:
            return
        completed_steps = steps.filter(status="completed").count()
        self.job.progress_percent = int((completed_steps / total_steps) * 100)
        self.job.save(update_fields=["progress_percent"])

    # ──────────────────────────────────────────────
    # Main execution
    # ──────────────────────────────────────────────

    def execute(self):
        """Execute the complete Magento import process."""
        try:
            self.job.status = "running"
            self.job.started_at = timezone.now()
            self.job.save()

            logger.info(f"Starting Magento import for job {self.job.id}")

            # Pre-fetch EAV attribute options for product mapping
            if self.job.import_products:
                self._log("info", "Pre-fetching Magento attribute options...")
                self.client.load_attribute_options()
                self._attribute_options_cache = self.client.get_attribute_options_cache()
                self._log(
                    "info", f"Cached {len(self._attribute_options_cache)} attribute option sets"
                )

            # Execute imports in order
            if self.job.import_categories:
                self._import_categories()

            if self.job.import_products:
                self._import_products()

            if self.job.import_customers:
                self._import_customers()

            if self.job.import_orders:
                self._import_orders()

            if self.job.import_reviews:
                self._import_reviews()

            if self.job.import_coupons:
                self._import_coupons()

            if self.job.import_blog:
                self._import_cms_pages()

            # Post-import: scan content for internal links
            self._scan_content_links()

            # Mark job as complete
            self.job.status = "completed"
            self.job.completed_at = timezone.now()
            self.job.duration_seconds = int(
                (self.job.completed_at - self.job.started_at).total_seconds()
            )
            self.job.progress_percent = 100
            self.job.can_rollback = True
            self.job.rollback_deadline = timezone.now() + timezone.timedelta(hours=24)
            self.job.save()

            logger.info(f"Magento import completed for job {self.job.id}")
            self._update_overall_progress()

        except Exception as e:
            logger.error(f"Magento import failed: {e}", exc_info=True)
            self.job.status = "failed"
            self.job.error_summary = str(e)
            self.job.completed_at = timezone.now()
            if self.job.started_at:
                self.job.duration_seconds = int(
                    (self.job.completed_at - self.job.started_at).total_seconds()
                )
            self.job.save()
            raise

    # ──────────────────────────────────────────────
    # Categories
    # ──────────────────────────────────────────────

    def _import_categories(self):
        """Import Magento categories from tree API."""
        step = MigrationStep.objects.create(
            job=self.job,
            step_type="categories",
            status="running",
            started_at=timezone.now(),
        )
        self.current_step = step

        self._log("info", "Starting Magento category import...")

        try:
            # Fetch full category tree
            tree = self.client.fetch_all_categories()
            if not tree:
                self._log("warning", "Empty category tree returned")
                step.status = "completed"
                step.completed_at = timezone.now()
                step.save()
                return

            # Flatten tree into list
            flat_categories = MagentoCategoryMapper.flatten_category_tree(tree)
            step.items_total = len(flat_categories)
            step.save()

            self._log("info", f"Fetched {len(flat_categories)} categories from tree")

            mapper = MagentoCategoryMapper(self.job)
            self._preload_slugs(Category)

            # First pass: create all categories (without parents)
            with tqdm(total=len(flat_categories), desc="📂 Categories", unit="cat") as pbar:
                for cat_data in flat_categories:
                    try:
                        self._import_single_category(cat_data, step, mapper)
                    except Exception as e:
                        self._log(
                            "error",
                            f"Failed to import category {cat_data.get('id')}: {e}",
                            source_type="category",
                            source_id=str(cat_data.get("id")),
                        )
                        self._quarantine_item(cat_data, "category", str(e))
                        self._step_increment(step, "items_failed")
                    finally:
                        pbar.update(1)

            self._step_flush(step)

            # Second pass: resolve parent relationships
            self._resolve_category_parents(flat_categories)

            # Post-import: validate hierarchy integrity
            self._validate_category_hierarchy(step)

            step.status = "completed"
            step.completed_at = timezone.now()
            step.duration_seconds = int((step.completed_at - step.started_at).total_seconds())
            step.save()

            self.job.categories_imported = step.items_imported
            self.job.categories_failed = step.items_failed
            self.job.categories_skipped = step.items_skipped
            self.job.save()
            self._update_overall_progress()

            self._log(
                "info",
                f"Category import complete: {step.items_imported} imported, "
                f"{step.items_failed} failed",
            )

        except Exception as e:
            step.status = "failed"
            step.error_message = str(e)
            step.completed_at = timezone.now()
            step.save()
            raise

    def _import_single_category(
        self, cat_data: dict, step: MigrationStep, mapper: MagentoCategoryMapper
    ) -> Category | None:
        """Import a single Magento category."""
        external_id = str(cat_data.get("id"))

        existing = Category.objects.filter(external_id=external_id).first()
        if existing:
            # Ensure previously-imported categories are active (re-import fix)
            if not existing.is_active:
                existing.is_active = True
                existing.save(update_fields=["is_active"])
                logger.info(f"Reactivated previously-imported category: {existing.name}")
            self._step_increment(step, "items_skipped")
            self.category_map[external_id] = existing
            return existing

        mapped = mapper.map(cat_data)

        category = Category.objects.create(
            external_id=external_id,
            migration_job=self.job,
            name=mapped.get("name", ""),
            slug=self._get_unique_slug(mapped.get("slug", ""), Category),
            description=mapped.get("description", ""),
            is_active=mapped.get("is_active", True),
            imported_meta={
                "magento_id": external_id,
                "magento_level": cat_data.get("level"),
            },
        )

        self.category_map[external_id] = category
        self._step_increment(step, "items_imported")
        return category

    def _resolve_category_parents(self, flat_categories: list[dict]):
        """Second pass: set parent relationships using category_map."""
        for cat_data in flat_categories:
            external_id = str(cat_data.get("id"))
            parent_id = str(cat_data.get("parent_id", 0))

            category = self.category_map.get(external_id)
            parent = self.category_map.get(parent_id)

            if category and parent and category != parent:
                category.parent = parent
                category.save(update_fields=["parent"])

    def _validate_category_hierarchy(self, step):
        """Ensure all parent categories with active children are themselves active."""
        reactivated = 0
        activated_any = True
        while activated_any:
            activated_any = False
            inactive_parents = Category.objects.filter(
                children__is_active=True,
                is_active=False,
            ).distinct()
            for parent in inactive_parents:
                parent.is_active = True
                parent.save(update_fields=["is_active"])
                reactivated += 1
                activated_any = True
                self._log(
                    "info",
                    f"Reactivated parent category '{parent.name}' (ID: {parent.id}) "
                    f"for hierarchy integrity",
                    source_type="category",
                    source_id=str(parent.external_id or parent.id),
                )

        if reactivated:
            self._log("info", f"Hierarchy validation: reactivated {reactivated} parent categories")
            logger.info(f"Category hierarchy validation: reactivated {reactivated} parents")

    # ──────────────────────────────────────────────
    # Products
    # ──────────────────────────────────────────────

    def _import_products(self):
        """Import Magento products with configurable variant handling."""
        step = MigrationStep.objects.create(
            job=self.job,
            step_type="products",
            status="running",
            started_at=timezone.now(),
        )
        self.current_step = step

        self._log("info", "Starting Magento product import...")

        try:
            total_products = self.job.connection_config.get("total_products", 0)
            step.items_total = total_products
            step.save()

            self.default_warehouse = Warehouse.objects.filter(is_active=True).first()
            if not self.default_warehouse:
                self._log(
                    "warning", "No active warehouse found. Stock quantities will not be imported."
                )

            self._preload_slugs(Product)
            self._preload_skus()

            store_url = self.job.connection_config.get("store_url", "")
            mapper = MagentoProductMapper(
                self.job,
                attribute_options_cache=self._attribute_options_cache,
                store_url=store_url,
            )

            # Fetch all products (visibility != 1 to exclude configurable children)
            all_products = self.client.fetch_all_products()

            progress_bar = tqdm(
                total=len(all_products),
                desc="📦 Products",
                unit="prod",
            )

            for product_data in all_products:
                try:
                    self._import_single_product(product_data, step, mapper)
                except Exception as e:
                    self._log(
                        "error",
                        f"Failed to import product {product_data.get('id')}: {e}",
                        source_type="product",
                        source_id=str(product_data.get("id")),
                    )
                    self._quarantine_item(product_data, "product", str(e))
                    self._step_increment(step, "items_failed")
                finally:
                    progress_bar.update(1)

            progress_bar.close()
            self._step_flush(step)

            step.status = "completed"
            step.completed_at = timezone.now()
            step.duration_seconds = int((step.completed_at - step.started_at).total_seconds())
            step.save()

            self.job.products_imported = step.items_imported
            self.job.products_failed = step.items_failed
            self.job.products_skipped = step.items_skipped
            self.job.save()
            self._update_overall_progress()

            self._log(
                "info",
                f"Product import complete: {step.items_imported} imported, "
                f"{step.items_failed} failed",
            )

        except Exception as e:
            step.status = "failed"
            step.error_message = str(e)
            step.completed_at = timezone.now()
            step.save()
            raise

    def _get_product_category(self, product_data: dict, mapped: dict) -> Category:
        """Resolve the primary category for a product, with fallbacks."""
        # Try mapped category IDs first
        for cat_ext_id in mapped.get("category_ids", []):
            cat = self.category_map.get(str(cat_ext_id))
            if cat:
                return cat

        # Fallback to any imported category
        if self.category_map:
            return next(iter(self.category_map.values()))

        # Final fallback: get or create "Uncategorized"
        if not hasattr(self, "_uncategorized_category"):
            self._uncategorized_category, _ = Category.objects.get_or_create(
                slug="uncategorized",
                defaults={
                    "name": "Uncategorized",
                    "description": "Products without a category",
                    "is_active": True,
                },
            )
        return self._uncategorized_category

    def _import_single_product(
        self, product_data: dict, step: MigrationStep, mapper: MagentoProductMapper
    ) -> Product | None:
        """Import a single Magento product."""
        external_id = str(product_data.get("id"))

        existing = Product.objects.filter(external_id=external_id).first()
        if existing:
            self._step_increment(step, "items_skipped")
            self.product_map[external_id] = existing
            return existing

        mapped = mapper.map(product_data)
        sku = self._get_unique_sku(mapped.get("sku", ""))

        # Compute sale fields (sale_type + sale_value from sale_price)
        sale_type = "none"
        sale_value_decimal = None
        regular_price = mapped.get("regular_price") or mapped.get("price")
        sale_price = mapped.get("sale_price")
        if sale_price and regular_price and Decimal(str(sale_price)) < Decimal(str(regular_price)):
            sale_type = "fixed_price"
            sale_value_decimal = Decimal(str(sale_price))

        # Short description (truncate to avoid field limits)
        short_desc = mapped.get("short_description", "")
        if len(short_desc) > 500:
            short_desc = short_desc[:497] + "..."

        # Resolve primary category (required FK)
        category = self._get_product_category(product_data, mapped)

        product = Product.objects.create(
            external_id=external_id,
            migration_job=self.job,
            name=mapped.get("name", ""),
            slug=self._get_unique_slug(mapped.get("slug", ""), Product),
            sku=sku,
            product_type=mapped.get("product_type", "simple"),
            category=category,
            short_description=short_desc,
            full_description=mapped.get("full_description", ""),
            price=Decimal(str(regular_price)) if regular_price else Decimal("0"),
            sale_type=sale_type,
            sale_value=sale_value_decimal,
            status=mapped.get("status", "draft"),
            is_digital=mapped.get("is_digital", False),
            track_inventory=mapped.get("track_inventory", False),
            allow_backorders=mapped.get("allow_backorders", False),
            weight=mapped.get("weight"),
            meta_title=mapped.get("meta_title", ""),
            meta_description=mapped.get("meta_description", ""),
            imported_meta={
                "magento_id": external_id,
                "magento_type": product_data.get("type_id"),
                "magento_visibility": product_data.get("visibility"),
                "attributes": mapped.get("attributes", {}),
            },
        )

        self.product_map[external_id] = product

        # Store additional category mappings in imported_meta
        additional_cat_ids = []
        for cat_ext_id in mapped.get("category_ids", []):
            cat = self.category_map.get(str(cat_ext_id))
            if cat and cat.id != category.id:
                additional_cat_ids.append(str(cat_ext_id))
        if additional_cat_ids:
            meta = product.imported_meta or {}
            meta["additional_categories"] = additional_cat_ids
            product.imported_meta = meta
            product.save(update_fields=["imported_meta"])

        # Import images
        self._import_product_images(product, mapped.get("images", []))

        # Import stock
        if self.default_warehouse and mapped.get("track_inventory"):
            StockItem.objects.update_or_create(
                product=product,
                warehouse=self.default_warehouse,
                defaults={
                    "on_hand": mapped.get("stock_quantity", 0),
                    "low_stock_threshold": mapped.get("low_stock_threshold", 5),
                },
            )

        # Handle configurable products: fetch and create variants
        if product_data.get("type_id") == "configurable":
            self._import_configurable_variants(product, product_data, step)

        self._step_increment(step, "items_imported")
        return product

    def _import_configurable_variants(
        self, parent_product: Product, parent_data: dict, step: MigrationStep
    ):
        """Fetch and import configurable product children as variants."""
        parent_sku = parent_data.get("sku", "")
        if not parent_sku:
            return

        children = self.client.fetch_configurable_children(parent_sku)
        if not children:
            return

        # Fetch configurable options to know which attributes define variants
        options = self.client.fetch_configurable_options(parent_sku)
        {opt.get("attribute_id"): opt.get("label", "") for opt in options}

        for _idx, child in enumerate(children):
            try:
                child_sku = self._get_unique_sku(child.get("sku", ""), is_variant=True)
                child_custom_attrs = child.get("custom_attributes", [])

                # Build variant option values from configurable attributes
                option_values = {}
                for attr in child_custom_attrs:
                    code = attr.get("attribute_code", "")
                    value = attr.get("value")
                    if code in self._attribute_options_cache:
                        label = resolve_attribute_label(value, code, self._attribute_options_cache)
                        option_values[code] = label

                child_price = Decimal(str(child.get("price", 0) or 0))
                parent_price = parent_product.price or Decimal("0")
                pricing_strategy = "inherit" if child_price == parent_price else "custom"

                child_ext = child.get("extension_attributes", {})
                child_stock = child_ext.get("stock_item", {})

                variant = ProductVariant.objects.create(
                    product=parent_product,
                    sku=child_sku,
                    name=" / ".join(option_values.values())
                    if option_values
                    else child.get("name", ""),
                    price=child_price if pricing_strategy == "custom" else None,
                    pricing_strategy=pricing_strategy,
                    is_active=child.get("status") == 1,
                    external_id=str(child.get("id", "")),
                    imported_meta={
                        "magento_id": str(child.get("id", "")),
                        "option_values": option_values,
                    },
                )

                # Import variant stock
                if self.default_warehouse and child_stock.get("manage_stock"):
                    StockItem.objects.update_or_create(
                        product=parent_product,
                        variant=variant,
                        warehouse=self.default_warehouse,
                        defaults={
                            "on_hand": int(child_stock.get("qty", 0) or 0),
                        },
                    )

                self.job.variants_imported = (self.job.variants_imported or 0) + 1

            except Exception as e:
                self._log(
                    "warning",
                    f"Failed to import variant {child.get('sku')}: {e}",
                    source_type="variant",
                    source_id=str(child.get("id", "")),
                )

        self.job.save(update_fields=["variants_imported"])

    def _import_product_images(self, product: Product, images_data: list[dict]):
        """Download and import Magento product images (deduplicated, with WebP + thumbnails)."""
        from media_library.models import ImageSizePreset, MediaThumbnail
        from media_library.services import ImageProcessor

        processor = ImageProcessor()
        PRODUCT_PRESET_SLUGS = {
            "thumbnail",
            "small",
            "medium",
            "large",
            "product_listing",
            "product_detail",
            "product_thumbnail",
        }
        image_presets = list(
            ImageSizePreset.objects.filter(is_active=True, slug__in=PRODUCT_PRESET_SLUGS)
        )
        session = self._get_image_session()

        for idx, img_data in enumerate(images_data[:5]):
            try:
                img_url = img_data.get("src", "")
                if not img_url:
                    continue

                image_external_id = str(img_data.get("external_id", ""))

                # Skip if this image was already imported (deduplication)
                if image_external_id:
                    existing_asset = MediaAsset.objects.filter(
                        external_id=image_external_id,
                        migration_job=self.job,
                    ).first()
                    if existing_asset:
                        ProductImage.objects.create(
                            product=product,
                            media_asset=existing_asset,
                            alt_text=img_data.get("alt_text") or product.name,
                            is_primary=(idx == 0),
                            position=idx,
                            show_in_gallery=True,
                            show_in_listing=True,
                        )
                        continue

                response = session.get(img_url, timeout=30)
                response.raise_for_status()

                filename = img_url.split("/")[-1].split("?")[0]
                if not filename:
                    filename = f"product_{product.id}_image_{idx}.jpg"

                ext = filename.lower().split(".")[-1] if "." in filename else "jpg"
                mime_type_map = {
                    "jpg": "image/jpeg",
                    "jpeg": "image/jpeg",
                    "png": "image/png",
                    "gif": "image/gif",
                    "webp": "image/webp",
                    "svg": "image/svg+xml",
                }
                mime_type = mime_type_map.get(ext, "image/jpeg")

                media_asset = MediaAsset.objects.create(
                    external_id=image_external_id,
                    migration_job=self.job,
                    title=f"{product.name} - Image {idx + 1}",
                    alt_text=img_data.get("alt_text") or product.name,
                    mime_type=mime_type,
                    file_size=len(response.content),
                )
                media_asset.original_file.save(filename, ContentFile(response.content), save=True)

                # Generate WebP version
                if media_asset.is_image() and mime_type != "image/svg+xml":
                    try:
                        webp_content = processor.convert_to_webp(media_asset.original_file)
                        if webp_content:
                            webp_filename = f"{media_asset.id}.webp"
                            media_asset.webp_file.save(webp_filename, webp_content, save=True)
                    except Exception as e:
                        logger.warning(f"Failed to generate WebP: {e}")

                # Generate thumbnails for product presets
                for preset in image_presets:
                    try:
                        original_content, webp_content = processor.generate_thumbnail(
                            media_asset.original_file,
                            preset.width,
                            preset.height,
                            crop_mode=preset.crop_mode,
                        )
                        if original_content:
                            thumbnail = MediaThumbnail.objects.create(
                                media_asset=media_asset,
                                size_preset=preset.slug,
                                width=preset.width,
                                height=preset.height,
                            )
                            thumbnail.file.save(
                                f"{media_asset.id}_{preset.slug}.jpg", original_content, save=False
                            )
                            if webp_content:
                                thumbnail.webp_file.save(
                                    f"{media_asset.id}_{preset.slug}.webp", webp_content, save=False
                                )
                            thumbnail.save()
                    except Exception as e:
                        logger.warning(f"Failed to generate {preset.slug} thumbnail: {e}")

                ProductImage.objects.create(
                    product=product,
                    media_asset=media_asset,
                    alt_text=img_data.get("alt_text") or product.name,
                    is_primary=(idx == 0),
                    position=idx,
                    show_in_gallery=True,
                    show_in_listing=True,
                )

            except Exception as e:
                logger.warning(f"Failed to import image for product {product.name}: {e}")
                continue

    # ──────────────────────────────────────────────
    # Customers
    # ──────────────────────────────────────────────

    def _import_customers(self):
        """Import Magento customers with addresses."""
        step = MigrationStep.objects.create(
            job=self.job,
            step_type="customers",
            status="running",
            started_at=timezone.now(),
        )
        self.current_step = step

        self._log("info", "Starting Magento customer import...")

        try:
            all_customers = self.client.fetch_all_customers()
            step.items_total = len(all_customers)
            step.save()

            mapper = MagentoCustomerMapper(self.job)

            with tqdm(total=len(all_customers), desc="👥 Customers", unit="cust") as pbar:
                for customer_data in all_customers:
                    try:
                        self._import_single_customer(customer_data, step, mapper)
                    except Exception as e:
                        self._log(
                            "error",
                            f"Failed to import customer {customer_data.get('id')}: {e}",
                            source_type="customer",
                            source_id=str(customer_data.get("id")),
                        )
                        self._quarantine_item(customer_data, "customer", str(e))
                        self._step_increment(step, "items_failed")
                    finally:
                        pbar.update(1)

            self._step_flush(step)

            step.status = "completed"
            step.completed_at = timezone.now()
            step.duration_seconds = int((step.completed_at - step.started_at).total_seconds())
            step.save()

            self.job.customers_imported = step.items_imported
            self.job.customers_failed = step.items_failed
            self.job.customers_skipped = step.items_skipped
            self.job.save()
            self._update_overall_progress()

            self._log(
                "info",
                f"Customer import complete: {step.items_imported} imported, "
                f"{step.items_failed} failed",
            )

        except Exception as e:
            step.status = "failed"
            step.error_message = str(e)
            step.completed_at = timezone.now()
            step.save()
            raise

    def _import_single_customer(
        self, customer_data: dict, step: MigrationStep, mapper: MagentoCustomerMapper
    ):
        """Import a single Magento customer."""
        mapped = mapper.map(customer_data)
        email = mapped.get("email", "")
        if not email:
            self._step_increment(step, "items_skipped")
            return

        existing = User.objects.filter(email=email).first()
        if existing:
            self._step_increment(step, "items_skipped")
            return

        user = User.objects.create_user(
            email=email,
            username=mapped.get("username", email.split("@")[0]),
            first_name=mapped.get("first_name", ""),
            last_name=mapped.get("last_name", ""),
        )
        user.set_unusable_password()
        user.save()

        CustomerProfile.objects.update_or_create(
            user=user,
            defaults={
                "migration_job": self.job,
                "external_id": mapped.get("source_id", ""),
            },
        )

        self._step_increment(step, "items_imported")

    # ──────────────────────────────────────────────
    # Orders
    # ──────────────────────────────────────────────

    def _import_orders(self):
        """Import Magento orders with line items and addresses."""
        step = MigrationStep.objects.create(
            job=self.job,
            step_type="orders",
            status="running",
            started_at=timezone.now(),
        )
        self.current_step = step

        self._log("info", "Starting Magento order import...")

        try:
            all_orders = self.client.fetch_all_orders()
            step.items_total = len(all_orders)
            step.save()

            mapper = MagentoOrderMapper(self.job)

            with tqdm(total=len(all_orders), desc="📋 Orders", unit="ord") as pbar:
                for order_data in all_orders:
                    try:
                        self._import_single_order(order_data, step, mapper)
                    except Exception as e:
                        self._log(
                            "error",
                            f"Failed to import order {order_data.get('increment_id')}: {e}",
                            source_type="order",
                            source_id=str(order_data.get("entity_id")),
                        )
                        self._quarantine_item(order_data, "order", str(e))
                        self._step_increment(step, "items_failed")
                    finally:
                        pbar.update(1)

            self._step_flush(step)

            step.status = "completed"
            step.completed_at = timezone.now()
            step.duration_seconds = int((step.completed_at - step.started_at).total_seconds())
            step.save()

            self.job.orders_imported = step.items_imported
            self.job.orders_failed = step.items_failed
            self.job.orders_skipped = step.items_skipped
            self.job.save()
            self._update_overall_progress()

            self._log(
                "info",
                f"Order import complete: {step.items_imported} imported, "
                f"{step.items_failed} failed",
            )

        except Exception as e:
            step.status = "failed"
            step.error_message = str(e)
            step.completed_at = timezone.now()
            step.save()
            raise

    def _import_single_order(
        self, order_data: dict, step: MigrationStep, mapper: MagentoOrderMapper
    ):
        """Import a single Magento order."""
        external_id = str(order_data.get("entity_id"))

        existing = Order.objects.filter(external_id=external_id).first()
        if existing:
            self._step_increment(step, "items_skipped")
            return

        mapped = mapper.map(order_data)

        # Find customer by email
        customer_email = mapped.get("customer_email", "")
        customer = User.objects.filter(email=customer_email).first() if customer_email else None

        currency = mapped.get("currency") or self._get_currency()
        billing = mapped.get("billing_address", {})
        shipping = mapped.get("shipping_address", {})

        order = Order.objects.create(
            external_id=external_id,
            migration_job=self.job,
            order_number=mapped.get("order_number", ""),
            user=customer,
            email=customer_email or billing.get("email", ""),
            phone=billing.get("phone", ""),
            status=mapped.get("status", "pending"),
            payment_status=mapped.get("payment_status", "pending"),
            payment_method_type=mapped.get("payment_method", ""),
            # Shipping address
            shipping_name=f"{shipping.get('first_name', '')} {shipping.get('last_name', '')}".strip(),
            shipping_address1=shipping.get("address_1", ""),
            shipping_address2=shipping.get("address_2", ""),
            shipping_city=shipping.get("city", ""),
            shipping_state=shipping.get("state", ""),
            shipping_postal_code=shipping.get("postcode", ""),
            shipping_country=shipping.get("country", ""),
            shipping_phone=shipping.get("phone", ""),
            # Billing address
            billing_same_as_shipping=False,
            billing_name=f"{billing.get('first_name', '')} {billing.get('last_name', '')}".strip(),
            billing_address1=billing.get("address_1", ""),
            billing_address2=billing.get("address_2", ""),
            billing_city=billing.get("city", ""),
            billing_state=billing.get("state", ""),
            billing_postal_code=billing.get("postcode", ""),
            billing_country=billing.get("country", ""),
            billing_phone=billing.get("phone", ""),
            # Totals (use safe_money to guarantee non-null for required MoneyFields)
            subtotal=safe_money(mapped.get("subtotal"), currency),
            discount_amount=safe_money(mapped.get("discount_total"), currency),
            shipping_cost=safe_money(mapped.get("shipping_total"), currency),
            tax_amount=safe_money(mapped.get("tax_total"), currency),
            total_amount=safe_money(mapped.get("total"), currency),
            # Currency info
            customer_currency=currency,
            base_currency=currency,
            # Notes
            notes=mapped.get("customer_note", ""),
        )

        # Import line items
        for item in mapped.get("line_items", []):
            product_ext_id = str(item.get("product_id", ""))
            product = self.product_map.get(product_ext_id)

            # Try SKU lookup if product_map miss
            if not product:
                sku = item.get("sku", "")
                if sku:
                    product = Product.objects.filter(sku=sku, migration_job=self.job).first()

            if not product:
                self._log(
                    "warning",
                    f"Order {external_id}: skipping line item '{item.get('name')}' - product not found (ext_id={product_ext_id})",
                )
                continue

            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=item.get("name", ""),
                sku=item.get("sku", ""),
                quantity=item.get("quantity", 1),
                unit_price=safe_money(item.get("price"), currency),
                total_price=safe_money(item.get("total"), currency),
            )

        self._step_increment(step, "items_imported")

    # ──────────────────────────────────────────────
    # Reviews
    # ──────────────────────────────────────────────

    def _import_reviews(self):
        """Import Magento product reviews."""
        step = MigrationStep.objects.create(
            job=self.job,
            step_type="reviews",
            status="running",
            started_at=timezone.now(),
        )
        self.current_step = step

        self._log("info", "Starting Magento review import...")

        try:
            all_reviews = self.client.fetch_all_reviews()
            step.items_total = len(all_reviews)
            step.save()

            mapper = MagentoReviewMapper(self.job)

            from catalog.models import ProductReview

            with tqdm(total=len(all_reviews), desc="⭐ Reviews", unit="rev") as pbar:
                for review_data in all_reviews:
                    try:
                        mapped = mapper.map(review_data)
                        product_ext_id = mapped.get("product_external_id", "")
                        product = self.product_map.get(product_ext_id)

                        if not product:
                            self._step_increment(step, "items_skipped")
                            pbar.update(1)
                            continue

                        # ProductReview requires a user FK — find by nickname or use a placeholder
                        reviewer_name = mapped.get("reviewer_name", "Anonymous")
                        review_user = User.objects.filter(username=reviewer_name).first()
                        if not review_user:
                            review_user = User.objects.create_user(
                                username=f"reviewer_{mapped.get('source_id', review_data.get('id', ''))}",
                                first_name=reviewer_name,
                            )
                            review_user.set_unusable_password()
                            review_user.save()

                        ProductReview.objects.create(
                            product=product,
                            user=review_user,
                            migration_job=self.job,
                            title=mapped.get("title", ""),
                            comment=mapped.get("content", ""),
                            rating=max(1, min(5, mapped.get("rating", 1))),
                            is_approved=mapped.get("is_approved", False),
                            external_id=mapped.get("source_id", ""),
                        )
                        self._step_increment(step, "items_imported")

                    except Exception as e:
                        self._log(
                            "error",
                            f"Failed to import review {review_data.get('id')}: {e}",
                            source_type="review",
                            source_id=str(review_data.get("id")),
                        )
                        self._step_increment(step, "items_failed")
                    finally:
                        pbar.update(1)

            self._step_flush(step)

            step.status = "completed"
            step.completed_at = timezone.now()
            step.duration_seconds = int((step.completed_at - step.started_at).total_seconds())
            step.save()

            self.job.reviews_imported = step.items_imported
            self.job.reviews_failed = step.items_failed
            self.job.reviews_skipped = step.items_skipped
            self.job.save()
            self._update_overall_progress()

        except Exception as e:
            step.status = "failed"
            step.error_message = str(e)
            step.completed_at = timezone.now()
            step.save()
            raise

    # ──────────────────────────────────────────────
    # Coupons
    # ──────────────────────────────────────────────

    def _import_coupons(self):
        """Import Magento sales rules + coupon codes."""
        step = MigrationStep.objects.create(
            job=self.job,
            step_type="coupons",
            status="running",
            started_at=timezone.now(),
        )
        self.current_step = step

        self._log("info", "Starting Magento coupon import...")

        try:
            all_rules = self.client.fetch_all_sales_rules()
            step.items_total = len(all_rules)
            step.save()

            mapper = MagentoCouponMapper(self.job)

            with tqdm(total=len(all_rules), desc="🎟️ Coupons", unit="coup") as pbar:
                for rule_data in all_rules:
                    try:
                        rule_id = rule_data.get("rule_id")
                        coupons = []
                        if rule_data.get("coupon_type", 1) != 1:
                            coupons = self.client.fetch_coupons_for_rule(rule_id)

                        if coupons:
                            for coupon in coupons:
                                combined = {
                                    "sales_rule": rule_data,
                                    "coupon": coupon,
                                }
                                mapped = mapper.map(combined)
                                self._create_voucher(mapped, step)
                        else:
                            mapped = mapper.map({"sales_rule": rule_data})
                            self._create_voucher(mapped, step)

                    except Exception as e:
                        self._log(
                            "error",
                            f"Failed to import coupon rule {rule_data.get('rule_id')}: {e}",
                            source_type="coupon",
                            source_id=str(rule_data.get("rule_id")),
                        )
                        self._step_increment(step, "items_failed")
                    finally:
                        pbar.update(1)

            self._step_flush(step)

            step.status = "completed"
            step.completed_at = timezone.now()
            step.duration_seconds = int((step.completed_at - step.started_at).total_seconds())
            step.save()

            self.job.coupons_imported = step.items_imported
            self.job.coupons_failed = step.items_failed
            self.job.coupons_skipped = step.items_skipped
            self.job.save()
            self._update_overall_progress()

        except Exception as e:
            step.status = "failed"
            step.error_message = str(e)
            step.completed_at = timezone.now()
            step.save()
            raise

    def _create_voucher(self, mapped: dict, step: MigrationStep):
        """Create a VoucherCode from mapped data."""
        code = mapped.get("code", "")
        if not code:
            self._step_increment(step, "items_skipped")
            return

        existing = VoucherCode.objects.filter(code=code).first()
        if existing:
            self._step_increment(step, "items_skipped")
            return

        VoucherCode.objects.create(
            code=code.upper(),
            name=mapped.get("name", code) or code,
            description=mapped.get("description", ""),
            migration_job=self.job,
            external_id=mapped.get("source_id", ""),
            discount_type=mapped.get("discount_type", "fixed"),
            discount_value=mapped.get("discount_value") or Decimal("0"),
            is_active=mapped.get("is_active", False),
            application_scope="cart",
            end_date=mapped.get("end_date"),
            max_uses_per_customer=mapped.get("max_uses_per_customer"),
            current_uses=mapped.get("current_uses", 0),
        )
        self._step_increment(step, "items_imported")

    # ──────────────────────────────────────────────
    # CMS Pages (Blog)
    # ──────────────────────────────────────────────

    def _import_cms_pages(self):
        """Import Magento CMS pages as blog posts."""
        step = MigrationStep.objects.create(
            job=self.job,
            step_type="blog",
            status="running",
            started_at=timezone.now(),
        )
        self.current_step = step

        self._log("info", "Starting Magento CMS page import...")

        try:
            all_pages = self.client.fetch_all_cms_pages()
            step.items_total = len(all_pages)
            step.save()

            store_url = self.job.connection_config.get("store_url", "")
            mapper = MagentoCmsPageMapper(self.job, store_url=store_url)

            from blog.models import BlogPost

            with tqdm(total=len(all_pages), desc="📝 CMS Pages", unit="page") as pbar:
                for page_data in all_pages:
                    try:
                        mapped = mapper.map(page_data)

                        # Skip system pages (home, no-route, etc.)
                        identifier = page_data.get("identifier", "")
                        if identifier in (
                            "home",
                            "no-route",
                            "enable-cookies",
                            "privacy-policy-cookie-restriction-mode",
                        ):
                            self._step_increment(step, "items_skipped")
                            pbar.update(1)
                            continue

                        existing = BlogPost.objects.filter(slug=mapped.get("slug", "")).first()
                        if existing:
                            self._step_increment(step, "items_skipped")
                            pbar.update(1)
                            continue

                        BlogPost.objects.create(
                            title=mapped.get("title", ""),
                            slug=self._get_unique_slug(mapped.get("slug", ""), BlogPost),
                            simple_content=mapped.get("content", ""),
                            excerpt=mapped.get("excerpt", ""),
                            status=mapped.get("status", "draft"),
                            meta_title=mapped.get("meta_title", ""),
                            meta_description=mapped.get("meta_description", ""),
                            migration_job=self.job,
                            external_id=mapped.get("source_id", ""),
                        )
                        self._step_increment(step, "items_imported")

                    except Exception as e:
                        self._log(
                            "error",
                            f"Failed to import CMS page {page_data.get('id')}: {e}",
                            source_type="blog_post",
                            source_id=str(page_data.get("id")),
                        )
                        self._step_increment(step, "items_failed")
                    finally:
                        pbar.update(1)

            self._step_flush(step)

            step.status = "completed"
            step.completed_at = timezone.now()
            step.duration_seconds = int((step.completed_at - step.started_at).total_seconds())
            step.save()

            self.job.blog_posts_imported = step.items_imported
            self.job.blog_posts_failed = step.items_failed
            self.job.blog_posts_skipped = step.items_skipped
            self.job.save()
            self._update_overall_progress()

        except Exception as e:
            step.status = "failed"
            step.error_message = str(e)
            step.completed_at = timezone.now()
            step.save()
            raise

    # ──────────────────────────────────────────────
    # Post-processing
    # ──────────────────────────────────────────────

    def _scan_content_links(self):
        """
        Post-import: scan imported content for internal links
        pointing to the old Magento store.
        """
        from urllib.parse import urlparse

        from migration.services.content_link_processor import ContentLinkProcessor

        store_url = self.job.connection_config.get("store_url", "")
        if not store_url:
            return

        source_domain = urlparse(store_url).netloc

        step = MigrationStep.objects.create(
            job=self.job,
            step_type="link_rewriting",
            status="running",
            started_at=timezone.now(),
        )
        self.current_step = step

        self._log("info", f"Scanning imported content for links from {source_domain}...")

        try:
            processor = ContentLinkProcessor(
                migration_job=self.job,
                source_domain=source_domain,
            )

            processor.scan_all_content()
            stats = getattr(processor, "stats", {})

            step.items_total = stats.get("links_found", 0)
            step.items_imported = stats.get("links_same_origin", 0)
            step.status = "completed"
            step.completed_at = timezone.now()
            step.duration_seconds = int((step.completed_at - step.started_at).total_seconds())
            step.save()

            self._log(
                "info",
                f"Link scan complete: {stats.get('links_found', 0)} found, "
                f"{stats.get('links_same_origin', 0)} same-origin, "
                f"{stats.get('links_external_skipped', 0)} external skipped",
            )

        except Exception as e:
            step.status = "failed"
            step.error_message = str(e)
            step.completed_at = timezone.now()
            step.save()
            self._log("warning", f"Link scan failed (non-critical): {e}")
