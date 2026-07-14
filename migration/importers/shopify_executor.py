"""
Shopify Import Execution Engine
Orchestrates the entire Shopify import process with progress tracking, field mapping, and quarantine
"""

import logging
from decimal import Decimal
from typing import Any

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
from migration.fetchers.shopify_api import ShopifyAPIClient
from migration.mappers.shopify import (
    ShopifyArticleMapper,
    ShopifyCollectionMapper,
    ShopifyCustomerMapper,
    ShopifyDiscountMapper,
    ShopifyOrderMapper,
    ShopifyProductMapper,
)
from migration.models import MigrationJob, MigrationLog, MigrationStagedItem, MigrationStep
from migration.services.attribute_service import AttributeService
from migration.utils.shopify_transformers import (
    parse_shopify_tags,
    transform_shopify_discount_type,
    transform_shopify_discount_value,
    transform_shopify_inventory_policy,
    transform_shopify_inventory_tracked,
    transform_shopify_order_status,
    transform_shopify_payment_status,
    transform_shopify_status,
)
from migration.utils.transformers import (
    safe_decimal,
    safe_money,
    transform_decimal_nullable,
    transform_integer_nullable,
    transform_money,
)
from orders.models import Order, OrderItem
from vouchers.models import VoucherCode

User = get_user_model()

logger = logging.getLogger(__name__)


class ShopifyImportExecutor:
    """
    Shopify import executor that orchestrates the entire migration process.

    Follows the same pattern as ImportExecutor (WooCommerce) but handles
    Shopify-specific data structures:
    - Cursor-based pagination
    - Embedded variants (no separate API calls per product)
    - Flat collections (no parent hierarchy)
    - Compound order status (financial + fulfillment)
    - Price rules + discount codes
    """

    # How often to flush step progress counters to DB
    STEP_SAVE_INTERVAL = 25

    def __init__(self, migration_job: MigrationJob):
        self.job = migration_job
        self.client = None
        self.field_mappings = {}
        self.category_map = {}  # Maps external_id -> Category instance
        self.current_step = None
        self.default_warehouse = None

        # Performance caches
        self._product_type_category_cache = {}  # product_type -> Category
        self._existing_slugs = {}  # model_class -> set of slugs
        self._existing_skus = set()
        self._existing_variant_skus = set()
        self._collects_by_product = {}  # product_id -> [collection_ids]
        self._step_dirty_count = 0  # Counter for batching step.save()
        self._image_session = None  # Persistent session for image downloads

        # Initialize Shopify client
        if self.job.platform == "shopify" and self.job.connection_config:
            self.client = ShopifyAPIClient(
                store_domain=self.job.connection_config["store_domain"],
                client_id=self.job.connection_config["client_id"],
                client_secret=self.job.connection_config["client_secret"],
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
        """Log to both Python logger and MigrationLog model"""
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
        """Load field mappings from MigrationMapping model"""
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
        """Get or create a persistent session for image downloads (connection pooling)."""
        if self._image_session is None:
            self._image_session = requests.Session()
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

    def _prefetch_collects(self):
        """
        Pre-fetch ALL product-collection assignments in one paginated call.
        Builds a lookup dict: {product_id_str: [collection_id_str, ...]}
        This replaces per-product API calls (eliminates N+1 problem).
        """
        logger.info("Pre-fetching all product-collection assignments...")
        all_collects = self.client.fetch_collects()
        for collect in all_collects:
            pid = str(collect.get("product_id", ""))
            cid = str(collect.get("collection_id", ""))
            if pid and cid:
                self._collects_by_product.setdefault(pid, []).append(cid)
        logger.info(
            f"Pre-fetched {len(all_collects)} collects for "
            f"{len(self._collects_by_product)} products"
        )

    def _preload_slugs(self, model_class):
        """Pre-load all existing slugs for a model into a set for O(1) lookups."""
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

    def execute(self):
        """Execute the complete Shopify import process"""
        try:
            self.job.status = "running"
            self.job.started_at = timezone.now()
            self.job.save()

            logger.info(f"Starting Shopify import for job {self.job.id}")

            config = self.job.connection_config or {}

            # Execute imports in order
            if config.get("import_categories", False):
                self._import_collections()

            if config.get("import_products", False):
                self._import_products()

            if config.get("import_customers", False):
                self._import_customers()

            if config.get("import_orders", False):
                self._import_orders()

            if config.get("import_coupons", False):
                self._import_discounts()

            if config.get("import_blog", False):
                self._import_blog()

            # Post-import: scan content for internal links
            self._scan_content_links()

            # Mark job as complete
            self.job.status = "completed"
            self.job.completed_at = timezone.now()
            self.job.duration_seconds = int(
                (self.job.completed_at - self.job.started_at).total_seconds()
            )
            self.job.progress_percent = 100
            self.job.save()

            logger.info(f"Shopify import completed for job {self.job.id}")
            self._update_overall_progress()

        except Exception as e:
            logger.error(f"Shopify import failed: {e}", exc_info=True)
            self.job.status = "failed"
            self.job.error_summary = str(e)
            self.job.completed_at = timezone.now()
            if self.job.started_at:
                self.job.duration_seconds = (
                    self.job.completed_at - self.job.started_at
                ).total_seconds()
            self.job.save()
            raise

    # ──────────────────────────────────────────────
    # Collections (Categories)
    # ──────────────────────────────────────────────

    def _import_collections(self):
        """Import Shopify collections (custom + smart) as categories"""
        step = MigrationStep.objects.create(
            job=self.job,
            step_type="categories",
            status="running",
            started_at=timezone.now(),
        )
        self.current_step = step

        self._log("info", "Starting Shopify collection import...")

        try:
            # Fetch all custom collections
            def progress_cb(count):
                pass  # Progress tracked by tqdm below

            custom_collections = self.client.fetch_all_custom_collections(progress_cb)
            smart_collections = self.client.fetch_all_smart_collections(progress_cb)
            all_collections = custom_collections + smart_collections

            step.items_total = self.job.connection_config.get(
                "total_categories", len(all_collections)
            )
            step.save()

            self._log(
                "info",
                f"Fetched {len(custom_collections)} custom + "
                f"{len(smart_collections)} smart collections",
            )

            mapper = ShopifyCollectionMapper(self.job)
            self._preload_slugs(Category)

            with tqdm(total=len(all_collections), desc="📂 Collections", unit="col") as pbar:
                for col_data in all_collections:
                    try:
                        self._import_single_collection(col_data, step, mapper)
                    except Exception as e:
                        self._log(
                            "error",
                            f"Failed to import collection {col_data.get('id')}: {e}",
                            source_type="category",
                            source_id=str(col_data.get("id")),
                        )
                        self._quarantine_item(col_data, "category", str(e))
                        self._step_increment(step, "items_failed")
                    finally:
                        pbar.update(1)

            self._step_flush(step)
            # No parent resolution needed — Shopify collections are flat

            step.status = "completed"
            step.completed_at = timezone.now()
            step.duration_seconds = (step.completed_at - step.started_at).total_seconds()
            step.save()

            self.job.categories_imported = step.items_imported
            self.job.categories_failed = step.items_failed
            self.job.categories_skipped = step.items_skipped
            self.job.save()

            self._update_overall_progress()

            self._log(
                "info",
                f"Collection import complete: {step.items_imported} imported, "
                f"{step.items_failed} failed",
            )

        except Exception as e:
            step.status = "failed"
            step.error_message = str(e)
            step.completed_at = timezone.now()
            step.save()
            raise

    def _import_single_collection(
        self, col_data: dict, step: MigrationStep, mapper: ShopifyCollectionMapper
    ) -> Category | None:
        """Import a single Shopify collection as a Category"""
        external_id = str(col_data.get("id"))

        # Check if already imported
        existing = Category.objects.filter(external_id=external_id).first()
        if existing:
            self._step_increment(step, "items_skipped")
            self.category_map[external_id] = existing
            return existing

        mapped = mapper.map(col_data)

        category = Category.objects.create(
            external_id=external_id,
            migration_job=self.job,
            name=mapped.get("name", col_data.get("title")),
            slug=self._get_unique_slug(mapped.get("slug", col_data.get("handle")), Category),
            description=mapped.get("description", ""),
            is_active=mapped.get("is_active", True),
            imported_meta={
                "shopify_id": external_id,
                "collection_type": mapped.get("collection_type", "custom"),
            },
        )

        self.category_map[external_id] = category

        # Download collection image if present
        image_url = mapped.get("image_url")
        if image_url:
            self._download_category_image(category, image_url, mapped.get("image_alt", ""))

        self._step_increment(step, "items_imported")

        logger.debug(f"Imported collection: {category.name}")
        return category

    def _download_category_image(self, category: Category, image_url: str, alt_text: str):
        """Download and attach image to category"""
        try:
            response = self._get_image_session().get(image_url, timeout=30)
            response.raise_for_status()

            filename = image_url.split("/")[-1].split("?")[0]
            if not filename:
                filename = f"category_{category.id}_image.jpg"

            media_asset = MediaAsset.objects.create(
                migration_job=self.job,
                title=f"{category.name} Image",
                alt_text=alt_text or category.name,
                mime_type="image/jpeg",
                file_size=len(response.content),
            )
            media_asset.original_file.save(filename, ContentFile(response.content), save=True)

            category.image_asset = media_asset
            category.save(update_fields=["image_asset"])
        except Exception as e:
            logger.warning(f"Failed to download category image: {e}")

    # ──────────────────────────────────────────────
    # Products
    # ──────────────────────────────────────────────

    def _import_products(self):
        """Import Shopify products with embedded variants"""
        step = MigrationStep.objects.create(
            job=self.job,
            step_type="products",
            status="running",
            started_at=timezone.now(),
        )
        self.current_step = step

        self._log("info", "Starting Shopify product import...")

        try:
            total_products = self.job.connection_config.get("total_products", 0)
            step.items_total = total_products
            step.save()

            # Resolve default warehouse for stock items
            self.default_warehouse = Warehouse.objects.filter(is_active=True).first()
            if not self.default_warehouse:
                self._log(
                    "warning", "No active warehouse found. Stock quantities will not be imported."
                )

            # Pre-fetch ALL collects in bulk (eliminates N+1 API calls)
            if self.category_map:
                self._prefetch_collects()

            # Pre-load slugs and SKUs for O(1) uniqueness checks
            self._preload_slugs(Product)
            self._preload_skus()

            mapper = ShopifyProductMapper(self.job)
            products_processed = 0

            progress_bar = tqdm(
                total=total_products,
                desc="📦 Products",
                unit="prod",
            )

            def on_product_fetched(count):
                pass  # Progress tracked by tqdm

            all_products = self.client.fetch_all_products(on_product_fetched)

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
                    products_processed += 1

            progress_bar.close()
            self._step_flush(step)

            step.status = "completed"
            step.completed_at = timezone.now()
            step.duration_seconds = (step.completed_at - step.started_at).total_seconds()
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

    def _import_single_product(
        self, product_data: dict, step: MigrationStep, mapper: ShopifyProductMapper
    ) -> Product | None:
        """Import a single Shopify product"""
        external_id = str(product_data.get("id"))

        # Check if already imported
        existing = Product.objects.filter(external_id=external_id).first()
        if existing:
            self._step_increment(step, "items_skipped")
            return existing

        mapped = mapper.map(product_data)

        # Get or create category from collection assignments
        category = self._get_product_category(product_data)
        if not category:
            raise ValueError("No category found for product")

        # Get price — try mapped price first, then scan all variants for a price
        currency = self._get_currency()
        price = transform_money(mapped.get("price") or mapped.get("regular_price"), currency)

        if not price or price == 0:
            # Fallback: scan all variants for the lowest non-zero price
            variants = product_data.get("variants", [])
            for v in variants:
                v_price = transform_money(v.get("price"), currency)
                if v_price and v_price > 0 and (not price or v_price < price):
                    price = v_price

        if not price or price == 0:
            # Still no price — use Decimal('0.00') and log a warning
            price = Decimal("0.00")
            logger.warning(
                f"Product {external_id} ({product_data.get('title')}) has no price, "
                f"defaulting to 0.00"
            )

        # Apply price adjustment
        price_adjustment_type = self.job.connection_config.get("price_adjustment_type", "none")
        if price_adjustment_type != "none":
            adjustment_value = Decimal(
                self.job.connection_config.get("price_adjustment_value", "0")
            )
            if price_adjustment_type == "percentage":
                price = price * (1 + adjustment_value / 100)
            elif price_adjustment_type == "fixed":
                price = price + adjustment_value

        # Compute sale fields
        sale_type = "none"
        sale_value_decimal = None
        regular_price = mapped.get("regular_price")
        sale_price = mapped.get("sale_price")
        if sale_price and regular_price and sale_price < regular_price:
            sale_type = "fixed_price"
            sale_value_decimal = sale_price

        # Short description
        short_desc = mapped.get("short_description", "")
        if len(short_desc) > 500:
            short_desc = short_desc[:497] + "..."

        # Build imported_meta
        imported_meta = {
            "shopify_id": external_id,
            "product_type": product_data.get("product_type", ""),
            "vendor": product_data.get("vendor", ""),
            "tags": product_data.get("tags", ""),
        }

        product_type = mapped.get("product_type", "simple")

        product = Product.objects.create(
            external_id=external_id,
            migration_job=self.job,
            name=mapped.get("name", product_data.get("title")),
            slug=self._get_unique_slug(mapped.get("slug", product_data.get("handle")), Product),
            sku=self._get_unique_sku(mapped.get("sku", "")),
            product_type=product_type,
            category=category,
            full_description=mapped.get("full_description", ""),
            short_description=short_desc,
            price=price,
            sale_type=sale_type,
            sale_value=sale_value_decimal,
            status=transform_shopify_status(product_data.get("status", "active")),
            is_featured=False,
            track_inventory=mapped.get("track_inventory", False),
            allow_backorders=mapped.get("allow_backorders", False),
            weight=transform_decimal_nullable(mapped.get("weight")),
            imported_meta=imported_meta,
        )

        # Create stock item
        if self.default_warehouse and mapped.get("track_inventory"):
            stock_qty = mapped.get("stock_quantity", 0) or 0
            StockItem.objects.create(
                product=product,
                warehouse=self.default_warehouse,
                on_hand=stock_qty,
                allocated=0,
            )

        # Import product images
        if product_data.get("images"):
            self._import_product_images(product, product_data["images"])

        # Import variants (embedded in product data)
        variants = product_data.get("variants", [])
        options = product_data.get("options", [])
        if len(variants) > 1:
            self._import_shopify_variants(product, variants, options, currency)

        # Link product to collections (uses pre-fetched cache, no API call)
        self._link_product_collections(product, external_id)

        self._step_increment(step, "items_imported")

        logger.debug(f"Imported product: {product.name}")
        return product

    def _import_product_images(self, product: Product, images_data: list[dict]):
        """Download and import Shopify product images (original only, deduplicated)"""
        import re

        from media_library.models import ImageSizePreset, MediaThumbnail
        from media_library.services import ImageProcessor

        processor = ImageProcessor()
        # Only generate product-relevant presets during migration
        # (other presets like favicon, logo, banner are never used for product images)
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
                img_url = img_data.get("src")
                if not img_url:
                    continue

                image_external_id = str(img_data.get("id", ""))

                # Skip if this image was already imported (deduplication)
                if image_external_id:
                    existing_asset = MediaAsset.objects.filter(
                        external_id=image_external_id,
                        migration_job=self.job,
                    ).first()
                    if existing_asset:
                        # Reuse the existing asset, just link to this product
                        ProductImage.objects.create(
                            product=product,
                            media_asset=existing_asset,
                            alt_text=img_data.get("alt") or product.name,
                            is_primary=(idx == 0),
                            position=idx,
                            show_in_gallery=True,
                            show_in_listing=True,
                        )
                        continue

                # Strip Shopify CDN size suffixes to get the original image
                # e.g. image_small.jpg → image.jpg, image_100x.jpg → image.jpg
                clean_url = re.sub(
                    r"_(?:small|medium|large|grande|compact|\d+x\d*|\d*x\d+)", "", img_url
                )

                response = session.get(clean_url, timeout=30)
                response.raise_for_status()

                filename = clean_url.split("/")[-1].split("?")[0]
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
                    alt_text=img_data.get("alt") or product.name,
                    mime_type=mime_type,
                    file_size=len(response.content),
                )

                media_asset.original_file.save(filename, ContentFile(response.content), save=True)

                # Spwig generates its own optimised thumbnails — no need to
                # download Shopify CDN variants. Just create WebP + thumbnails.
                if media_asset.is_image() and mime_type != "image/svg+xml":
                    try:
                        webp_content = processor.convert_to_webp(media_asset.original_file)
                        if webp_content:
                            webp_filename = f"{media_asset.id}.webp"
                            media_asset.webp_file.save(webp_filename, webp_content, save=True)
                    except Exception as e:
                        logger.warning(f"Failed to generate WebP: {e}")

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
                    alt_text=img_data.get("alt") or product.name,
                    is_primary=(idx == 0),
                    position=idx,
                    show_in_gallery=True,
                    show_in_listing=True,
                )

            except Exception as e:
                logger.warning(f"Failed to import image for product {product.name}: {e}")
                continue

    def _import_shopify_variants(
        self, product: Product, variants: list[dict], options: list[dict], currency: str
    ):
        """
        Import Shopify product variants from embedded variant data.

        Unlike WooCommerce which requires separate API calls per product,
        Shopify embeds variants directly in the product response.
        Options array maps option1/option2/option3 to named attributes.
        """
        attribute_service = AttributeService()
        product_attribute_values: dict[int, list] = {}

        # Build option name mapping: position → name
        # options: [{"name": "Color", "position": 1}, {"name": "Size", "position": 2}]
        option_names = {}
        for opt in options:
            pos = opt.get("position", 0)
            name = opt.get("name", "")
            if name and name != "Title":
                option_names[pos] = name

        imported_count = 0
        failed_count = 0

        for variant_data in tqdm(variants, desc=f"  Variants for {product.name[:30]}", leave=False):
            try:
                variant = self._import_single_shopify_variant(
                    product=product,
                    variant_data=variant_data,
                    option_names=option_names,
                    attribute_service=attribute_service,
                    product_attribute_values=product_attribute_values,
                    currency=currency,
                )
                if variant:
                    imported_count += 1
            except Exception as e:
                self._log(
                    "error",
                    f"Failed to import variant {variant_data.get('id')}: {e}",
                    source_type="variation",
                    source_id=str(variant_data.get("id")),
                )
                self._quarantine_item(variant_data, "variation", str(e))
                failed_count += 1

        # Create ProductAttributeAssignments
        from catalog.models import ProductAttribute

        for attribute_id, values in product_attribute_values.items():
            try:
                attribute = ProductAttribute.objects.get(id=attribute_id)
                attribute_service.ensure_product_attribute_assignment(
                    product=product, attribute=attribute, values=values
                )
            except ProductAttribute.DoesNotExist:
                pass

        self._log(
            "info", f"Imported {imported_count} variants for {product.name} ({failed_count} failed)"
        )

    def _import_single_shopify_variant(
        self,
        product: Product,
        variant_data: dict,
        option_names: dict,
        attribute_service: AttributeService,
        product_attribute_values: dict,
        currency: str,
    ) -> ProductVariant | None:
        """Import a single Shopify variant"""
        external_id = str(variant_data.get("id"))

        # Check if already imported
        existing = ProductVariant.objects.filter(external_id=external_id).first()
        if existing:
            return existing

        # Parse Shopify option1/option2/option3 into attribute pairs
        attribute_pairs = []
        for pos, name in option_names.items():
            value_str = variant_data.get(f"option{pos}")
            if value_str and value_str != "Default Title":
                attr, val = attribute_service.get_or_create_attribute_value(name, value_str)
                attribute_pairs.append((attr, val))

        # Build variant name
        variant_name = attribute_service.build_variant_name(attribute_pairs) or variant_data.get(
            "title", f"Variant {external_id}"
        )

        # Accumulate values for parent
        for attribute, value in attribute_pairs:
            if attribute.id not in product_attribute_values:
                product_attribute_values[attribute.id] = []
            if value not in product_attribute_values[attribute.id]:
                product_attribute_values[attribute.id].append(value)

        # SKU
        sku = variant_data.get("sku", "")
        if not sku:
            sku = f"{product.sku}-{external_id}"
        sku = self._get_unique_variant_sku(sku)

        # Pricing
        regular_price = transform_money(
            variant_data.get("compare_at_price") or variant_data.get("price"), currency
        )

        pricing_strategy = "inherit"
        variant_price = None
        if regular_price and product.price and regular_price != product.price:
            pricing_strategy = "custom"
            variant_price = regular_price

        variant = ProductVariant.objects.create(
            product=product,
            external_id=external_id,
            name=variant_name,
            sku=sku,
            pricing_strategy=pricing_strategy,
            price=variant_price,
            weight=transform_decimal_nullable(variant_data.get("weight")),
            is_active=True,
            imported_meta={
                "shopify_id": external_id,
                "inventory_quantity": variant_data.get("inventory_quantity"),
                "inventory_management": variant_data.get("inventory_management"),
                "inventory_policy": variant_data.get("inventory_policy"),
                "option1": variant_data.get("option1"),
                "option2": variant_data.get("option2"),
                "option3": variant_data.get("option3"),
            },
        )

        # Create stock item
        if self.default_warehouse and variant_data.get("inventory_management") == "shopify":
            variant_stock = transform_integer_nullable(variant_data.get("inventory_quantity")) or 0
            StockItem.objects.create(
                product=product,
                warehouse=self.default_warehouse,
                variant=variant,
                on_hand=variant_stock,
                allocated=0,
            )

        # Link attributes
        for _, value in attribute_pairs:
            variant.selected_attributes.add(value)

        # Variant image
        image_id = variant_data.get("image_id")
        if image_id:
            existing_asset = MediaAsset.objects.filter(external_id=str(image_id)).first()
            if existing_asset:
                variant.image_asset = existing_asset
                variant.save(update_fields=["image_asset"])

        return variant

    def _link_product_collections(self, product: Product, shopify_product_id: str):
        """Link product to collections using pre-fetched collects cache (no API call)."""
        collection_ids = self._collects_by_product.get(shopify_product_id, [])
        if not collection_ids:
            return

        additional = []
        for collection_id in collection_ids:
            if collection_id in self.category_map:
                additional.append(collection_id)

        if additional:
            meta = product.imported_meta or {}
            meta["additional_categories"] = additional
            product.imported_meta = meta
            product.save(update_fields=["imported_meta"])

    def _get_product_category(self, product_data: dict) -> Category | None:
        """Get or create category for Shopify product (with in-memory cache)."""
        external_id = str(product_data.get("id", ""))
        product_type = product_data.get("product_type", "")

        # First, try to find a collection assignment from pre-fetched collects
        collection_ids = self._collects_by_product.get(external_id, [])
        for cid in collection_ids:
            if cid in self.category_map:
                return self.category_map[cid]

        # Try product_type matching (cached)
        if product_type:
            if product_type in self._product_type_category_cache:
                return self._product_type_category_cache[product_type]

            category = Category.objects.filter(name__iexact=product_type).first()
            if category:
                self._product_type_category_cache[product_type] = category
                return category

        # Fallback to any imported collection
        if self.category_map:
            first_cat = next(iter(self.category_map.values()))
            return first_cat

        # Final fallback: get or create "Uncategorized" (cached)
        if "_uncategorized" not in self._product_type_category_cache:
            category, _ = Category.objects.get_or_create(
                slug="uncategorized",
                defaults={
                    "name": "Uncategorized",
                    "description": "Products without a category",
                    "is_active": True,
                },
            )
            self._product_type_category_cache["_uncategorized"] = category
        return self._product_type_category_cache["_uncategorized"]

    # ──────────────────────────────────────────────
    # Customers
    # ──────────────────────────────────────────────

    def _import_customers(self):
        """Import Shopify customers"""
        step = MigrationStep.objects.create(
            job=self.job,
            step_type="customers",
            status="running",
            started_at=timezone.now(),
        )
        self.current_step = step

        self._log("info", "Starting Shopify customer import...")

        try:
            all_customers = self.client.fetch_all_customers()

            step.items_total = self.job.connection_config.get("total_customers", len(all_customers))
            step.save()

            self._log("info", f"Fetched {len(all_customers)} customers from Shopify")

            mapper = ShopifyCustomerMapper(self.job)

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
            step.duration_seconds = (step.completed_at - step.started_at).total_seconds()
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
        self, customer_data: dict, step: MigrationStep, mapper: ShopifyCustomerMapper
    ) -> User | None:
        """Import a single Shopify customer"""
        external_id = str(customer_data.get("id"))
        email = customer_data.get("email")

        if not email:
            raise ValueError("Customer has no email address")

        # Check if already imported
        existing_profile = CustomerProfile.objects.filter(external_id=external_id).first()
        if existing_profile:
            self._step_increment(step, "items_skipped")
            return existing_profile.user

        # Check if user with this email exists
        existing_user = User.objects.filter(email=email).first()
        if existing_user:
            profile, created = CustomerProfile.objects.get_or_create(
                user=existing_user,
                defaults={
                    "external_id": external_id,
                    "migration_job": self.job,
                    "phone": customer_data.get("phone", "") or "",
                },
            )
            if not created and not profile.external_id:
                profile.external_id = external_id
                profile.migration_job = self.job
                profile.save()

            self._step_increment(step, "items_imported")
            return existing_user

        mapped = mapper.map(customer_data)

        # Generate unique username
        username = mapped.get("username") or email.split("@")[0]
        original_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{original_username}{counter}"
            counter += 1

        # Parse date
        date_joined = timezone.now()
        if customer_data.get("created_at"):
            try:
                date_joined = timezone.datetime.fromisoformat(
                    customer_data["created_at"].replace("Z", "+00:00")
                )
            except (ValueError, AttributeError):
                pass

        user = User.objects.create(
            username=username,
            email=email,
            first_name=mapped.get("first_name", ""),
            last_name=mapped.get("last_name", ""),
            date_joined=date_joined,
            is_active=True,
        )
        user.set_unusable_password()
        user.save()

        CustomerProfile.objects.create(
            user=user,
            external_id=external_id,
            migration_job=self.job,
            phone=customer_data.get("phone", "") or "",
        )

        # Create address from default address
        billing = mapped.get("billing_address", {})
        if billing.get("address_1"):
            from orders.models import Address

            Address.objects.create(
                user=user,
                address_type="billing",
                name=f"{billing.get('first_name', '')} {billing.get('last_name', '')}".strip(),
                company=billing.get("company", ""),
                address1=billing.get("address_1", ""),
                address2=billing.get("address_2", ""),
                city=billing.get("city", ""),
                state=billing.get("state", ""),
                postal_code=billing.get("postcode", ""),
                country=billing.get("country", ""),
                phone=billing.get("phone", ""),
                is_default=True,
            )

        self._step_increment(step, "items_imported")

        logger.debug(f"Imported customer: {user.email}")
        return user

    # ──────────────────────────────────────────────
    # Orders
    # ──────────────────────────────────────────────

    def _import_orders(self):
        """Import Shopify orders"""
        step = MigrationStep.objects.create(
            job=self.job,
            step_type="orders",
            status="running",
            started_at=timezone.now(),
        )
        self.current_step = step

        self._log("info", "Starting Shopify order import...")

        try:
            all_orders = self.client.fetch_all_orders()

            step.items_total = self.job.connection_config.get("total_orders", len(all_orders))
            step.save()

            self._log("info", f"Fetched {len(all_orders)} orders from Shopify")

            mapper = ShopifyOrderMapper(self.job)

            with tqdm(total=len(all_orders), desc="🛒 Orders", unit="ord") as pbar:
                for order_data in all_orders:
                    try:
                        self._import_single_order(order_data, step, mapper)
                    except Exception as e:
                        self._log(
                            "error",
                            f"Failed to import order {order_data.get('id')}: {e}",
                            source_type="order",
                            source_id=str(order_data.get("id")),
                        )
                        self._quarantine_item(order_data, "order", str(e))
                        self._step_increment(step, "items_failed")
                    finally:
                        pbar.update(1)

            self._step_flush(step)

            step.status = "completed"
            step.completed_at = timezone.now()
            step.duration_seconds = (step.completed_at - step.started_at).total_seconds()
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
        self, order_data: dict, step: MigrationStep, mapper: ShopifyOrderMapper
    ) -> Order | None:
        """Import a single Shopify order"""
        external_id = str(order_data.get("id"))
        order_number = str(order_data.get("order_number", external_id))

        # Check if already imported
        existing_order = Order.objects.filter(order_number=order_number).first()
        if existing_order:
            self._step_increment(step, "items_skipped")
            return existing_order

        mapper.map(order_data)

        # Find customer
        user = None
        customer = order_data.get("customer") or {}
        customer_id = customer.get("id")
        if customer_id:
            profile = CustomerProfile.objects.filter(external_id=str(customer_id)).first()
            if profile:
                user = profile.user

        if not user:
            email = order_data.get("email") or order_data.get("contact_email", "")
            if email:
                user = User.objects.filter(email=email).first()

        # Create guest user if needed
        if not user:
            email = (
                order_data.get("email")
                or order_data.get("contact_email")
                or f"guest_{external_id}@example.com"
            )
            username = f"guest_{external_id}"
            existing_guest = User.objects.filter(username=username).first()
            if existing_guest:
                user = existing_guest
            else:
                billing = order_data.get("billing_address") or {}
                user = User.objects.create(
                    username=username,
                    email=email,
                    first_name=billing.get("first_name") or "Guest",
                    last_name=billing.get("last_name") or "",
                    is_active=False,
                )
                user.set_unusable_password()
                user.save()

        # Map status
        status = transform_shopify_order_status(
            order_data.get("financial_status", "pending"),
            order_data.get("fulfillment_status"),
            order_data.get("cancelled_at"),
        )
        # Map to platform statuses
        status_map = {
            "completed": "delivered",
            "cancelled": "cancelled",
            "refunded": "refunded",
            "processing": "processing",
            "on_hold": "pending",
            "pending": "pending",
        }
        status = status_map.get(status, "pending")

        # Map payment status from Shopify financial_status
        payment_status = transform_shopify_payment_status(
            order_data.get("financial_status", "pending")
        )

        currency = order_data.get("currency") or self._get_currency()
        billing_addr = order_data.get("billing_address") or {}
        shipping_addr = order_data.get("shipping_address") or billing_addr

        # Parse created_at
        created_at = timezone.now()
        if order_data.get("created_at"):
            try:
                created_at = timezone.datetime.fromisoformat(
                    order_data["created_at"].replace("Z", "+00:00")
                )
            except (ValueError, AttributeError):
                pass

        order = Order.objects.create(
            order_number=order_number,
            user=user,
            external_id=external_id,
            migration_job=self.job,
            status=status,
            payment_status=payment_status,
            email=order_data.get("email") or order_data.get("contact_email") or user.email,
            phone=billing_addr.get("phone") or "",
            # Shipping address
            shipping_name=f"{shipping_addr.get('first_name') or ''} {shipping_addr.get('last_name') or ''}".strip(),
            shipping_address1=shipping_addr.get("address1") or "",
            shipping_address2=shipping_addr.get("address2") or "",
            shipping_city=shipping_addr.get("city") or "",
            shipping_state=shipping_addr.get("province")
            or shipping_addr.get("province_code")
            or "",
            shipping_postal_code=shipping_addr.get("zip") or "",
            shipping_country=shipping_addr.get("country_code")
            or shipping_addr.get("country")
            or "",
            # Billing address
            billing_same_as_shipping=False,
            billing_name=f"{billing_addr.get('first_name') or ''} {billing_addr.get('last_name') or ''}".strip(),
            billing_address1=billing_addr.get("address1") or "",
            billing_address2=billing_addr.get("address2") or "",
            billing_city=billing_addr.get("city") or "",
            billing_state=billing_addr.get("province") or billing_addr.get("province_code") or "",
            billing_postal_code=billing_addr.get("zip") or "",
            billing_country=billing_addr.get("country_code") or billing_addr.get("country") or "",
            # Totals (use safe_money to guarantee non-null for required MoneyFields)
            subtotal=safe_money(order_data.get("subtotal_price"), currency),
            tax_amount=safe_money(order_data.get("total_tax"), currency),
            shipping_cost=safe_money(
                sum(
                    safe_decimal(line.get("price")) for line in order_data.get("shipping_lines", [])
                ),
                currency,
            ),
            discount_amount=safe_money(order_data.get("total_discounts"), currency),
            gift_card_discount=safe_money(0, currency),
            total_amount=safe_money(order_data.get("total_price"), currency),
            amount_paid=safe_money(0, currency),
            amount_refunded=safe_money(0, currency),
            special_instructions=order_data.get("note") or "",
            language=self._get_site_default_language(),
            created_at=created_at,
        )

        # Import line items
        for item_data in order_data.get("line_items", []):
            try:
                self._import_order_item(order, item_data, currency)
            except Exception as e:
                logger.warning(f"Failed to import order item for order {order.order_number}: {e}")

        self._step_increment(step, "items_imported")

        logger.debug(f"Imported order: {order.order_number}")
        return order

    def _import_order_item(self, order: Order, item_data: dict, currency: str):
        """Import a single Shopify order line item"""
        product_id = item_data.get("product_id")
        variant_id = item_data.get("variant_id")

        product = None
        variant = None

        if product_id:
            product = Product.objects.filter(external_id=str(product_id)).first()

        if variant_id:
            variant = ProductVariant.objects.filter(external_id=str(variant_id)).first()

        if not product:
            logger.warning(f"Product {product_id} not found for order {order.order_number}")
            return

        quantity = item_data.get("quantity") or 1
        item_price = safe_decimal(item_data.get("price"))

        OrderItem.objects.create(
            order=order,
            product=product,
            variant=variant,
            product_name=item_data.get("title") or item_data.get("name") or product.name,
            sku=item_data.get("sku") or product.sku or "",
            quantity=quantity,
            unit_price=safe_money(item_data.get("price"), currency),
            total_price=safe_money(item_price * quantity, currency),
        )

    def _get_site_default_language(self):
        """Get site default language"""
        try:
            from core.models import SiteSettings

            return SiteSettings.get_settings().default_language or "en"
        except Exception:
            return "en"

    # ──────────────────────────────────────────────
    # Discounts (Price Rules + Discount Codes)
    # ──────────────────────────────────────────────

    def _import_discounts(self):
        """Import Shopify discounts (price rules + discount codes)"""
        step = MigrationStep.objects.create(
            job=self.job,
            step_type="coupons",
            status="running",
            started_at=timezone.now(),
        )
        self.current_step = step

        self._log("info", "Starting Shopify discount import...")

        try:
            all_price_rules = self.client.fetch_all_price_rules()

            step.items_total = self.job.connection_config.get("total_coupons", len(all_price_rules))
            step.save()

            self._log("info", f"Fetched {len(all_price_rules)} price rules from Shopify")

            mapper = ShopifyDiscountMapper(self.job)

            with tqdm(total=len(all_price_rules), desc="🏷️ Discounts", unit="disc") as pbar:
                for price_rule in all_price_rules:
                    try:
                        # Fetch discount codes for this price rule
                        codes = self.client.fetch_discount_codes(price_rule["id"])
                        if codes:
                            for code in codes:
                                combined = {
                                    "price_rule": price_rule,
                                    "discount_code": code,
                                }
                                self._import_single_discount(combined, step, mapper)
                        else:
                            # Price rule without explicit codes — use title as code
                            combined = {
                                "price_rule": price_rule,
                                "discount_code": {
                                    "code": price_rule.get("title", ""),
                                    "usage_count": 0,
                                },
                            }
                            self._import_single_discount(combined, step, mapper)
                    except Exception as e:
                        self._log(
                            "error",
                            f"Failed to import discount {price_rule.get('id')}: {e}",
                            source_type="coupon",
                            source_id=str(price_rule.get("id")),
                        )
                        self._quarantine_item(price_rule, "coupon", str(e))
                        self._step_increment(step, "items_failed")
                    finally:
                        pbar.update(1)

            self._step_flush(step)

            step.status = "completed"
            step.completed_at = timezone.now()
            step.duration_seconds = (step.completed_at - step.started_at).total_seconds()
            step.save()

            self.job.coupons_imported = step.items_imported
            self.job.coupons_failed = step.items_failed
            self.job.coupons_skipped = step.items_skipped
            self.job.save()

            self._update_overall_progress()

            self._log(
                "info",
                f"Discount import complete: {step.items_imported} imported, "
                f"{step.items_failed} failed",
            )

        except Exception as e:
            step.status = "failed"
            step.error_message = str(e)
            step.completed_at = timezone.now()
            step.save()
            raise

    def _import_single_discount(
        self, combined_data: dict, step: MigrationStep, mapper: ShopifyDiscountMapper
    ) -> VoucherCode | None:
        """Import a single Shopify discount"""
        mapped = mapper.map(combined_data)

        code = mapped.get("code", "")
        if not code:
            raise ValueError("Discount has no code")

        # Check if exists
        existing = VoucherCode.objects.filter(code=code.upper()).first()
        if existing:
            self._step_increment(step, "items_skipped")
            return existing

        external_id = mapped.get("source_id", "")
        currency = self._get_currency()

        # Parse dates
        end_date = None
        if mapped.get("end_date"):
            try:
                end_date = timezone.datetime.fromisoformat(
                    mapped["end_date"].replace("Z", "+00:00")
                )
            except (ValueError, AttributeError):
                pass

        voucher = VoucherCode.objects.create(
            code=code.upper(),
            name=mapped.get("description", code) or code,
            description=mapped.get("description", ""),
            external_id=external_id,
            migration_job=self.job,
            discount_type=mapped.get("discount_type", "percentage"),
            discount_value=mapped.get("discount_value", Decimal("0")),
            application_scope="cart",
            end_date=end_date,
            max_uses_total=mapped.get("max_uses_total"),
            max_uses_per_customer=mapped.get("max_uses_per_customer"),
            current_uses=mapped.get("current_uses", 0),
            min_order_value=(
                transform_money(mapped.get("min_order_value"), currency)
                if mapped.get("min_order_value")
                else None
            ),
            is_active=True,
        )

        self._step_increment(step, "items_imported")

        logger.debug(f"Imported discount: {voucher.code}")
        return voucher

    # ──────────────────────────────────────────────
    # Blog (Articles)
    # ──────────────────────────────────────────────

    def _import_blog(self):
        """Import Shopify blog articles"""
        step = MigrationStep.objects.create(
            job=self.job,
            step_type="blog",
            status="running",
            started_at=timezone.now(),
        )
        self.current_step = step

        self._log("info", "Starting Shopify blog import...")

        try:
            from blog.models import BlogCategory, BlogPost, BlogTag

            # Fetch all blogs (containers)
            blogs = self.client.fetch_blogs()
            self._log("info", f"Found {len(blogs)} blogs on Shopify")

            mapper = ShopifyArticleMapper(self.job)
            blog_category_map = {}  # shopify blog_id -> BlogCategory
            total_articles = 0
            articles_imported = 0
            articles_failed = 0

            # Create BlogCategory for each Shopify blog
            for blog_data in blogs:
                blog_id = blog_data.get("id")
                blog_title = blog_data.get("title", "Blog")
                blog_handle = blog_data.get("handle", "blog")

                cat, _ = BlogCategory.objects.get_or_create(
                    slug=self._get_unique_slug(blog_handle, BlogCategory),
                    defaults={
                        "name": blog_title,
                        "description": "",
                    },
                )
                blog_category_map[blog_id] = cat

            # Fetch and import articles for each blog
            for blog_data in blogs:
                blog_id = blog_data.get("id")
                articles = self.client.fetch_all_articles(blog_id)
                total_articles += len(articles)

                self._log(
                    "info", f"Fetched {len(articles)} articles from blog '{blog_data.get('title')}'"
                )

                blog_category = blog_category_map.get(blog_id)

                with tqdm(
                    total=len(articles),
                    desc=f"📝 Blog: {blog_data.get('title', '')[:20]}",
                    unit="art",
                ) as pbar:
                    for article_data in articles:
                        try:
                            self._import_single_article(
                                article_data, step, mapper, blog_category, BlogPost, BlogTag
                            )
                            articles_imported += 1
                        except Exception as e:
                            self._log(
                                "error",
                                f"Failed to import article {article_data.get('id')}: {e}",
                                source_type="blog_post",
                                source_id=str(article_data.get("id")),
                            )
                            self._quarantine_item(article_data, "blog_post", str(e))
                            articles_failed += 1
                        finally:
                            pbar.update(1)

            step.items_total = total_articles
            step.items_imported = articles_imported
            step.items_failed = articles_failed
            step.status = "completed"
            step.completed_at = timezone.now()
            step.duration_seconds = (step.completed_at - step.started_at).total_seconds()
            step.save()

            self.job.blog_posts_total = total_articles
            self.job.blog_posts_imported = articles_imported
            self.job.blog_posts_failed = articles_failed
            self.job.blog_categories_total = len(blogs)
            self.job.blog_categories_imported = len(blogs)
            self.job.save()

            self._update_overall_progress()

            self._log(
                "info",
                f"Blog import complete: {articles_imported} articles, {len(blogs)} categories",
            )

        except Exception as e:
            step.status = "failed"
            step.error_message = str(e)
            step.completed_at = timezone.now()
            step.save()
            self._log("error", f"Blog import failed: {e}")
            raise

    def _import_single_article(
        self,
        article_data: dict,
        step: MigrationStep,
        mapper: ShopifyArticleMapper,
        blog_category,
        BlogPost,
        BlogTag,
    ):
        """Import a single Shopify blog article"""
        mapped = mapper.map(article_data)
        mapped.get("source_id", str(article_data.get("id")))

        # Check if already imported
        existing = BlogPost.objects.filter(slug=mapped.get("slug", "")).first()
        if existing:
            self._step_increment(step, "items_skipped")
            return existing

        # Parse dates
        published_at = timezone.now()
        if mapped.get("published_at"):
            try:
                published_at = timezone.datetime.fromisoformat(
                    mapped["published_at"].replace("Z", "+00:00")
                )
            except (ValueError, AttributeError):
                pass

        post = BlogPost.objects.create(
            title=mapped.get("title", ""),
            slug=self._get_unique_slug(mapped.get("slug", ""), BlogPost),
            simple_content=mapped.get("content", ""),
            excerpt=mapped.get("excerpt", ""),
            status="published" if mapped.get("status") == "published" else "draft",
            published_at=published_at,
        )

        # Assign blog category
        if blog_category:
            post.categories.add(blog_category)

        # Create and assign tags
        for tag_name in mapped.get("tags", []):
            if tag_name:
                tag, _ = BlogTag.objects.get_or_create(
                    slug=self._get_unique_slug(tag_name.lower().replace(" ", "-"), BlogTag),
                    defaults={"name": tag_name},
                )
                post.tags.add(tag)

        # Download featured image
        if mapped.get("featured_image_url"):
            self._download_blog_featured_image(
                post, mapped["featured_image_url"], mapped.get("featured_image_alt", "")
            )

        return post

    def _download_blog_featured_image(self, post, image_url: str, alt_text: str):
        """Download and attach featured image to blog post"""
        try:
            response = self._get_image_session().get(image_url, timeout=30)
            response.raise_for_status()

            filename = image_url.split("/")[-1].split("?")[0]
            if not filename:
                filename = f"blog_{post.id}_featured.jpg"

            media_asset = MediaAsset.objects.create(
                migration_job=self.job,
                title=f"{post.title} Featured Image",
                alt_text=alt_text or post.title,
                mime_type="image/jpeg",
                file_size=len(response.content),
            )
            media_asset.original_file.save(filename, ContentFile(response.content), save=True)

            post.featured_image = media_asset
            post.save(update_fields=["featured_image"])

        except Exception as e:
            logger.warning(f"Failed to download blog featured image: {e}")

    # ──────────────────────────────────────────────
    # Content Link Scanning
    # ──────────────────────────────────────────────

    def _scan_content_links(self):
        """
        Post-import: scan imported content for internal links
        pointing to the old Shopify store.
        """
        from migration.services.content_link_processor import ContentLinkProcessor

        store_domain = self.job.connection_config.get("store_domain", "")
        if not store_domain:
            self._log("warning", "No store_domain in config, skipping link scan")
            return

        # Shopify domains: yourstore.myshopify.com
        source_domain = store_domain

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
            step.duration_seconds = (step.completed_at - step.started_at).total_seconds()
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

    # ──────────────────────────────────────────────
    # Utility methods
    # ──────────────────────────────────────────────

    def _apply_mappings(self, source_data: dict, source_type: str) -> dict:
        """Apply field mappings to source data"""
        mapped_data = {}
        for source_field, value in source_data.items():
            key = f"{source_type}.{source_field}"
            if key in self.field_mappings:
                mapping = self.field_mappings[key]
                dest_field = mapping["dest_field"]
                transform_type = mapping["transform_type"]
                transformed_value = self._apply_transform(value, transform_type)
                mapped_data[dest_field] = transformed_value
        return mapped_data

    def _apply_transform(self, value: Any, transform_type: str) -> Any:
        """Apply transformation to a value"""
        if not value or transform_type == "none":
            return value

        try:
            if transform_type == "string":
                return str(value)
            elif transform_type == "integer":
                return int(value)
            elif transform_type == "integer_nullable":
                return transform_integer_nullable(value)
            elif transform_type == "decimal":
                return Decimal(str(value))
            elif transform_type == "decimal_nullable":
                return transform_decimal_nullable(value)
            elif transform_type == "boolean":
                return bool(value)
            elif transform_type == "money":
                return transform_money(value)
            elif transform_type == "shopify_status":
                return transform_shopify_status(value)
            elif transform_type == "shopify_order_status":
                return transform_shopify_order_status(value)
            elif transform_type == "shopify_discount_type":
                return transform_shopify_discount_type(value)
            elif transform_type == "shopify_discount_value":
                return transform_shopify_discount_value(value)
            elif transform_type == "shopify_inventory_tracked":
                return transform_shopify_inventory_tracked(value)
            elif transform_type == "shopify_inventory_policy":
                return transform_shopify_inventory_policy(value)
            elif transform_type == "comma_separated":
                return parse_shopify_tags(value)
            else:
                return value
        except Exception as e:
            logger.warning(f"Transform failed ({transform_type}): {e}")
            return value

    def _quarantine_item(self, source_data: dict, item_type: str, error_message: str):
        """Quarantine a failed item"""
        external_id = str(source_data.get("id", "unknown"))
        MigrationStagedItem.objects.create(
            job=self.job,
            item_type=item_type,
            external_id=external_id,
            source_data=source_data,
            failure_reason="validation_failed",
            error_message=error_message,
            status="pending_review",
        )

    def _get_unique_slug(self, slug: str, model_class) -> str:
        """Generate unique slug using in-memory cache (O(1) lookups)."""
        if not slug:
            slug = "item"

        # Ensure slug cache is loaded for this model
        self._preload_slugs(model_class)
        slug_set = self._existing_slugs[model_class]

        original_slug = slug
        counter = 1
        while slug in slug_set:
            slug = f"{original_slug}-{counter}"
            counter += 1

        # Add to cache so subsequent calls see it
        slug_set.add(slug)
        return slug

    def _get_unique_sku(self, sku: str) -> str:
        """Generate unique product SKU using in-memory cache."""
        if not sku:
            import time

            sku = f"SKU-{int(time.time())}"

        original_sku = sku
        counter = 1
        while sku in self._existing_skus:
            sku = f"{original_sku}-{counter}"
            counter += 1

        self._existing_skus.add(sku)
        return sku

    def _get_unique_variant_sku(self, sku: str) -> str:
        """Generate unique variant SKU using in-memory cache."""
        if not sku:
            import time

            sku = f"VAR-{int(time.time())}"

        original_sku = sku
        counter = 1
        while sku in self._existing_variant_skus:
            sku = f"{original_sku}-{counter}"
            counter += 1

        self._existing_variant_skus.add(sku)
        return sku

    def _update_overall_progress(self):
        """Calculate and update overall progress percentage"""
        steps = self.job.steps.all()
        if not steps.exists():
            self.job.progress_percent = 0
            self.job.save()
            return

        total_items = sum(step.items_total for step in steps if step.items_total > 0)
        total_processed = sum(
            step.items_imported + step.items_skipped + step.items_failed for step in steps
        )

        if total_items > 0:
            self.job.progress_percent = int((total_processed / total_items) * 100)
        else:
            self.job.progress_percent = 0

        self.job.save()
