"""
WooCommerce Importer
Import WooCommerce data into the platform with transaction support
"""

import logging

from django.contrib.auth import get_user_model

from catalog.models import Category, Product, ProductImage, StockItem, Warehouse
from migration.mappers import (
    WooCommerceCategoryMapper,
    WooCommerceProductMapper,
)
from migration.services.media_downloader import MediaDownloader

from .base import BaseImporter

logger = logging.getLogger(__name__)

User = get_user_model()


class WooCommerceCategoryImporter(BaseImporter):
    """Import WooCommerce categories"""

    def __init__(self, migration_job, dry_run: bool = False):
        super().__init__(migration_job, dry_run)
        self.mapper = WooCommerceCategoryMapper(migration_job)
        self.category_map = {}  # Map WC IDs to internal IDs

    def import_data(self, mapped_data: dict) -> Category | None:
        """Import a single category"""
        try:
            # Get unique slug
            slug = self._get_unique_slug(mapped_data["slug"], Category)

            # Create or update category
            category, created = self.get_or_create(
                Category,
                lookup_fields={"slug": slug},
                defaults={
                    "name": mapped_data["name"],
                    "description": mapped_data["description"],
                    "sort_order": mapped_data["sort_order"],
                    "is_active": mapped_data["is_active"],
                    "is_featured": mapped_data["is_featured"],
                    "meta_title": mapped_data.get("meta_title", ""),
                    "meta_description": mapped_data.get("meta_description", ""),
                    "page_template": mapped_data.get("page_template", "grid"),
                    "products_per_page": mapped_data.get("products_per_page", 24),
                    "show_subcategories": mapped_data.get("show_subcategories", True),
                },
                update_existing=True,
            )

            # Store mapping for parent resolution later
            self.category_map[mapped_data["source_id"]] = category.id

            # Record mapping
            self.record_mapping(
                source_id=mapped_data["source_id"],
                source_platform="woocommerce",
                target_model="Category",
                target_id=category.id,
            )

            return category

        except Exception as e:
            logger.error(f"Failed to import category {mapped_data.get('name')}: {e}")
            raise

    def resolve_category_parents(self, categories_data: list[dict]):
        """
        Resolve category parent relationships after all categories are imported

        Args:
            categories_data: List of mapped category data with parent_id
        """
        for cat_data in categories_data:
            parent_wc_id = cat_data.get("parent_id", 0)

            if parent_wc_id and str(parent_wc_id) in self.category_map:
                # Get internal category
                category = Category.objects.get(id=self.category_map[cat_data["source_id"]])

                # Set parent
                parent_id = self.category_map[str(parent_wc_id)]
                category.parent_id = parent_id
                category.save()

                logger.debug(f"Set parent for category {category.name}")

    def _get_unique_slug(self, slug: str, model_class) -> str:
        """Generate unique slug"""
        original_slug = slug
        counter = 1

        while model_class.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1

        return slug


class WooCommerceProductImporter(BaseImporter):
    """Import WooCommerce products"""

    def __init__(self, migration_job, media_downloader: MediaDownloader, dry_run: bool = False):
        super().__init__(migration_job, dry_run)
        self.mapper = WooCommerceProductMapper(migration_job)
        self.media_downloader = media_downloader
        self.category_map = {}  # Will be populated from mappings

    def import_data(self, mapped_data: dict) -> Product | None:
        """Import a single product"""
        try:
            # Skip if no price
            if not mapped_data.get("price"):
                logger.warning(f"Skipping product {mapped_data['name']} - no price")
                self.stats["skipped"] += 1
                return None

            # Get category (use first category or create default)
            category = self._get_or_create_category(mapped_data)

            if not category:
                logger.error(f"No category for product {mapped_data['name']}")
                return None

            # Generate unique slug and SKU
            slug = self._get_unique_slug(mapped_data["slug"], Product)
            sku = self._get_unique_sku(mapped_data.get("sku", ""))

            # Create or update product
            product, created = self.get_or_create(
                Product,
                lookup_fields={"sku": sku},
                defaults={
                    "name": mapped_data["name"],
                    "slug": slug,
                    "product_type": mapped_data.get("product_type", "simple"),
                    "category": category,
                    "full_description": mapped_data.get("full_description", ""),
                    "short_description": mapped_data.get("short_description", ""),
                    "price": mapped_data["price"],
                    "sale_type": "fixed_price"
                    if (
                        mapped_data.get("sale_price")
                        and mapped_data.get("price")
                        and mapped_data["sale_price"] < mapped_data["price"]
                    )
                    else "none",
                    "sale_value": mapped_data["sale_price"]
                    if (
                        mapped_data.get("sale_price")
                        and mapped_data.get("price")
                        and mapped_data["sale_price"] < mapped_data["price"]
                    )
                    else None,
                    "track_inventory": mapped_data.get("track_inventory", True),
                    "allow_backorders": mapped_data.get("allow_backorders", False),
                    "low_stock_threshold": mapped_data.get("low_stock_threshold", 5),
                    "weight": mapped_data.get("weight"),
                    "length": mapped_data.get("length"),
                    "width": mapped_data.get("width"),
                    "height": mapped_data.get("height"),
                    "status": mapped_data.get("status", "published"),
                    "is_featured": mapped_data.get("is_featured", False),
                    "is_digital": mapped_data.get("is_digital", False),
                    "meta_title": mapped_data.get("meta_title", ""),
                    "meta_description": mapped_data.get("meta_description", ""),
                },
                update_existing=True,
            )

            # Create stock item for inventory tracking
            if created and mapped_data.get("track_inventory", False):
                warehouse = Warehouse.objects.filter(is_active=True).first()
                if warehouse:
                    StockItem.objects.get_or_create(
                        product=product,
                        warehouse=warehouse,
                        variant=None,
                        defaults={
                            "on_hand": int(mapped_data.get("stock_quantity", 0) or 0),
                            "allocated": 0,
                        },
                    )

            # Import product images
            if mapped_data.get("images"):
                self._import_product_images(product, mapped_data["images"])

            # Record mapping
            self.record_mapping(
                source_id=mapped_data["source_id"],
                source_platform="woocommerce",
                target_model="Product",
                target_id=product.id,
            )

            return product

        except Exception as e:
            logger.error(f"Failed to import product {mapped_data.get('name')}: {e}")
            raise

    def _get_or_create_category(self, product_data: dict) -> Category | None:
        """Get or create product category"""
        # Try to get mapped category
        primary_category_id = product_data.get("primary_category_id")

        if primary_category_id:
            # Look up in migration mappings
            mapped_id = self.get_mapped_id(str(primary_category_id), "woocommerce", "Category")

            if mapped_id:
                try:
                    return Category.objects.get(id=mapped_id)
                except Category.DoesNotExist:
                    pass

        # Fallback: get or create "Uncategorized"
        category, created = Category.objects.get_or_create(
            slug="uncategorized",
            defaults={
                "name": "Uncategorized",
                "description": "Products without a category",
                "is_active": True,
            },
        )

        return category

    def _import_product_images(self, product: Product, images_data: list[dict]):
        """Import product images from WooCommerce"""
        # Clear existing images if updating
        if not product._state.adding:
            ProductImage.objects.filter(product=product).delete()

        for img_data in images_data:
            try:
                # Download image using media downloader
                # For now, create placeholder ProductImage
                # In full implementation, integrate with MediaDownloader

                img_url = img_data.get("src")
                if not img_url:
                    continue

                # Create product image record
                ProductImage.objects.create(
                    product=product,
                    image=img_url,  # This will need proper file handling
                    alt_text=img_data.get("alt_text", ""),
                    is_primary=img_data.get("is_primary", False),
                    position=img_data.get("position", 0),
                    show_in_gallery=True,
                    show_in_listing=True,
                )

            except Exception as e:
                logger.warning(f"Failed to import image for product {product.name}: {e}")
                continue

    def _get_unique_slug(self, slug: str, model_class) -> str:
        """Generate unique slug"""
        original_slug = slug or "product"
        slug = original_slug
        counter = 1

        while model_class.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1

        return slug

    def _get_unique_sku(self, sku: str) -> str:
        """Generate unique SKU"""
        if not sku:
            # Generate SKU from timestamp
            import time

            sku = f"SKU-{int(time.time())}"

        original_sku = sku
        counter = 1

        while Product.objects.filter(sku=sku).exists():
            sku = f"{original_sku}-{counter}"
            counter += 1

        return sku


class WooCommerceImporter:
    """
    Main importer that orchestrates the full WooCommerce migration

    This class coordinates:
    - Category import with parent resolution
    - Product import with images
    - Customer import
    - Order import
    """

    def __init__(self, migration_job, dry_run: bool = False):
        """
        Initialize WooCommerce importer

        Args:
            migration_job: MigrationJob instance
            dry_run: If True, don't commit to database
        """
        self.migration_job = migration_job
        self.dry_run = dry_run

        # Initialize sub-importers
        self.media_downloader = MediaDownloader(migration_job)
        self.category_importer = WooCommerceCategoryImporter(migration_job, dry_run)
        self.product_importer = WooCommerceProductImporter(
            migration_job, self.media_downloader, dry_run
        )

        # Statistics
        self.stats = {
            "categories": {},
            "products": {},
            "customers": {},
            "orders": {},
        }

    def import_categories(self, categories_data: list[dict], progress_callback=None) -> dict:
        """
        Import categories with parent resolution

        Args:
            categories_data: List of WooCommerce category data
            progress_callback: Optional progress callback

        Returns:
            Import statistics
        """
        logger.info(f"Importing {len(categories_data)} categories...")

        # Map categories
        mapped_categories = []
        for cat_data in categories_data:
            try:
                mapped = self.category_importer.mapper.map(cat_data)
                mapped_categories.append(mapped)
            except Exception as e:
                logger.error(f"Failed to map category {cat_data.get('id')}: {e}")
                continue

        # Import categories
        stats = self.category_importer.import_batch(mapped_categories, progress_callback)

        # Resolve parent relationships
        self.category_importer.resolve_category_parents(mapped_categories)

        # Post-import: validate hierarchy integrity
        self._validate_category_hierarchy()

        self.stats["categories"] = stats
        return stats

    def import_products(self, products_data: list[dict], progress_callback=None) -> dict:
        """
        Import products

        Args:
            products_data: List of WooCommerce product data
            progress_callback: Optional progress callback

        Returns:
            Import statistics
        """
        logger.info(f"Importing {len(products_data)} products...")

        # Map products
        mapped_products = []
        for product_data in products_data:
            try:
                mapped = self.product_importer.mapper.map(product_data)
                mapped_products.append(mapped)
            except Exception as e:
                logger.error(f"Failed to map product {product_data.get('id')}: {e}")
                continue

        # Import products
        stats = self.product_importer.import_batch(mapped_products, progress_callback)

        self.stats["products"] = stats
        return stats

    def import_all(
        self, categories: list[dict], products: list[dict], progress_callback=None
    ) -> dict:
        """
        Import all data in correct order

        Args:
            categories: WooCommerce categories
            products: WooCommerce products
            progress_callback: Optional progress callback

        Returns:
            Overall statistics
        """
        logger.info("Starting full WooCommerce import...")

        try:
            # 1. Import categories first (products depend on them)
            self.import_categories(categories, progress_callback)

            # 2. Import products
            self.import_products(products, progress_callback)

            logger.info("WooCommerce import completed successfully")
            return self.get_stats()

        except Exception as e:
            logger.error(f"WooCommerce import failed: {e}")
            raise

    def _validate_category_hierarchy(self):
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
                logger.info(
                    f"Reactivated parent category '{parent.name}' (ID: {parent.id}) for hierarchy integrity"
                )

        if reactivated:
            logger.info(f"Hierarchy validation: reactivated {reactivated} parent categories")

    def get_stats(self) -> dict:
        """Get overall import statistics"""
        return self.stats

    def cleanup(self):
        """Cleanup resources"""
        self.media_downloader.cleanup()
