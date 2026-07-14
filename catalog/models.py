from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import F, Prefetch, Q, Sum
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field
from djmoney.models.fields import MoneyField

from custom_fields.mixins import CustomFieldsMixin
from design.models import DesignMixin

User = get_user_model()


class Category(CustomFieldsMixin, DesignMixin):
    """Product categories with hierarchical structure and design customization"""

    # Basic information
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    parent = models.ForeignKey(
        "self", related_name="children", on_delete=models.CASCADE, blank=True, null=True
    )
    description = models.TextField(blank=True)

    # Import tracking
    external_id = models.CharField(
        max_length=100,
        blank=True,
        db_index=True,
        help_text="Original ID from source platform (WooCommerce, Shopify, etc.)",
    )
    migration_job = models.ForeignKey(
        "migration.MigrationJob",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="imported_categories",
        help_text="Migration job that imported this category",
    )
    imported_meta = models.JSONField(
        default=dict, blank=True, help_text="Metadata from import (SEO fields, identifiers, etc.)"
    )

    # Images and media
    icon = models.CharField(max_length=100, blank=True, help_text="Icon class name or SVG")

    # Media Library integration
    image_asset = models.ForeignKey(
        "media_library.MediaAsset",
        on_delete=models.PROTECT,
        related_name="category_images",
        null=True,
        blank=True,
        help_text="Main category image from media library",
    )
    banner_asset = models.ForeignKey(
        "media_library.MediaAsset",
        on_delete=models.PROTECT,
        related_name="category_banners",
        null=True,
        blank=True,
        help_text="Category page banner from media library",
    )

    # Display and layout options
    # Display and layout options
    products_per_page = models.PositiveIntegerField(default=24)
    show_subcategories = models.BooleanField(default=True)

    CATEGORY_PAGE_TEMPLATE_CHOICES = [
        ("", _("Use Site Default")),
        ("grid", _("Grid")),
        ("list", _("List")),
        ("carousel", _("Carousel")),
        ("masonry", _("Masonry")),
        ("featured", _("Featured")),
        ("accordion", _("Accordion")),
    ]
    page_template = models.CharField(
        max_length=30,
        blank=True,
        choices=CATEGORY_PAGE_TEMPLATE_CHOICES,
        default="",
        verbose_name=_("Page Template"),
        help_text=_(
            "Override the site default category page template. Leave empty to use the site default from Design settings."
        ),
    )

    # Theme inheritance for child categories and products
    cascade_theme_to_children = models.BooleanField(
        default=True, help_text="Apply this category's design to child categories"
    )
    cascade_theme_to_products = models.BooleanField(
        default=True, help_text="Apply this category's design to products"
    )

    # Stock settings override (None = use site-wide StockDisplaySettings)
    out_of_stock_action_override = models.CharField(
        _("out of stock action override"),
        max_length=20,
        choices=[
            ("hide", _("Hide from listings")),
            ("show_unavailable", _("Show as unavailable")),
            ("notify_me", _('Show "Notify Me" button')),
            ("allow_backorder", _("Allow backorders")),
        ],
        null=True,
        blank=True,
        help_text=_("Override site-wide out-of-stock behavior for products in this category"),
    )
    allow_backorders_override = models.BooleanField(
        _("allow backorders override"),
        null=True,
        help_text=_(
            "Override site-wide backorder setting for products in this category (None = inherit from site)"
        ),
    )

    # SEO and meta
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(max_length=255, blank=True)
    seo_auto_generated = models.BooleanField(
        default=False, help_text="Automatically regenerate SEO content when category is saved"
    )

    # Translations - all translatable content stored in JSON by language code
    # Structure: {"es": {"name": "...", "description": "...", "meta_title": "...", "meta_description": "..."}}
    translations = models.JSONField(
        default=dict,
        blank=True,
        help_text="Multilingual content (name, description, SEO) by language code",
    )

    # Status and visibility
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["is_featured"]),
            models.Index(fields=["sort_order"]),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/category/{self.slug}/"

    @property
    def full_path(self):
        """Get full category path for breadcrumbs"""
        if self.parent:
            return f"{self.parent.full_path} > {self.name}"
        return self.name

    def get_effective_theme(self):
        """Get effective theme settings including inheritance"""
        theme = {
            "template_variant": self.template_variant,
            "css_classes": self.css_classes,
            "layout_config": self.layout_config,
            "style_overrides": self.style_overrides,
        }

        # Inherit from parent if enabled
        if self.inherit_parent_theme and self.parent:
            parent_theme = self.parent.get_effective_theme()
            # Merge parent theme with current overrides
            for key in theme:
                if isinstance(theme[key], dict) and isinstance(parent_theme.get(key), dict):
                    merged = parent_theme[key].copy()
                    merged.update(theme[key])
                    theme[key] = merged
                elif not theme[key] and parent_theme.get(key):
                    theme[key] = parent_theme[key]

        return theme

    # Media Library convenience methods
    def get_image_url(self):
        """Get category image URL from MediaAsset"""
        if self.image_asset:
            return self.image_asset.get_display_url()
        return None

    def get_card_image_url(self):
        """Get image for category card with product fallback.

        Returns the category's own image if set, otherwise the primary
        image of the first published product in this category.
        """
        if self.image_asset:
            return self.image_asset.get_display_url()
        product = self.products.filter(status="published", images__isnull=False).only("id").first()
        if product:
            return product.primary_image_url
        return None

    def get_card_image_thumbnail(self, size_preset="card"):
        """Get thumbnail for category card with product fallback."""
        if self.image_asset:
            return self.image_asset.get_thumbnail(size_preset)
        product = self.products.filter(status="published", images__isnull=False).only("id").first()
        if product and product.primary_image:
            return product.primary_image.get_thumbnail(size_preset)
        return None

    def get_banner_url(self):
        """Get category banner URL from MediaAsset"""
        if self.banner_asset:
            return self.banner_asset.get_display_url()
        return None

    def get_descendant_ids(self, include_self=True):
        """
        Get IDs of this category and all descendants (recursive).
        Used for querying products across entire category subtree.
        """
        ids = [self.id] if include_self else []
        for child in self.children.filter(is_active=True):
            ids.extend(child.get_descendant_ids(include_self=True))
        return ids

    def get_image_thumbnail(self, size_preset="medium"):
        """Get thumbnail for category image from MediaAsset"""
        if self.image_asset:
            return self.image_asset.get_thumbnail(size_preset)
        return None

    def get_banner_thumbnail(self, size_preset="medium"):
        """Get thumbnail for category banner from MediaAsset"""
        if self.banner_asset:
            return self.banner_asset.get_thumbnail(size_preset)
        return None

    def get_image_alt_text(self):
        """Get alt text for category image"""
        if self.image_asset and self.image_asset.alt_text:
            return self.image_asset.alt_text
        return self.name

    def get_banner_alt_text(self):
        """Get alt text for category banner"""
        if self.banner_asset and self.banner_asset.alt_text:
            return self.banner_asset.alt_text
        return f"{self.name} banner"


class Brand(DesignMixin):
    """Product brands/manufacturers with design customization"""

    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)

    # Import tracking
    external_id = models.CharField(
        max_length=100, blank=True, db_index=True, help_text="Original ID from source platform"
    )
    imported_meta = models.JSONField(default=dict, blank=True, help_text="Metadata from import")

    # Brand assets
    logo = models.ImageField(upload_to="brands/", blank=True, null=True)
    banner_image = models.ImageField(upload_to="brands/banners/", blank=True, null=True)
    website = models.URLField(blank=True)

    # Brand page display
    show_brand_page = models.BooleanField(default=True)
    brand_story = models.TextField(blank=True, help_text="Brand story for brand page")

    # SEO
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(max_length=255, blank=True)
    seo_auto_generated = models.BooleanField(
        default=False, help_text="Automatically regenerate SEO content when brand is saved"
    )

    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/brand/{self.slug}/"


class ProductQuerySet(models.QuerySet):
    """
    Custom QuerySet for Product model with performance optimizations.

    Provides efficient methods for stock calculations and regional filtering.
    """

    def with_stock_totals(self):
        """
        Annotate products with aggregated stock totals across all warehouses.

        Adds:
        - total_on_hand: Total physical stock
        - total_allocated: Total reserved for orders
        - total_available: Total available for sale (on_hand - allocated)

        Returns:
            QuerySet with annotations
        """
        return self.annotate(
            total_on_hand=Sum("stock_items__on_hand"),
            total_allocated=Sum("stock_items__allocated"),
            total_available=Sum(F("stock_items__on_hand") - F("stock_items__allocated")),
        )

    def with_regional_stock(self, region):
        """
        Annotate products with stock in a specific region.

        Args:
            region: SalesRegion instance

        Adds:
        - regional_stock: Available stock in the specified region

        Returns:
            QuerySet with regional_stock annotation
        """
        return self.annotate(
            regional_stock=Sum(
                F("stock_items__on_hand") - F("stock_items__allocated"),
                filter=Q(
                    stock_items__warehouse__region=region, stock_items__warehouse__is_active=True
                ),
            )
        )

    def in_stock_in_region(self, region):
        """
        Filter products with available stock in a specific region.

        Args:
            region: SalesRegion instance

        Returns:
            QuerySet of products with stock > 0 in the region
        """
        return self.with_regional_stock(region).filter(
            Q(track_inventory=False)  # Non-inventory products always available
            | Q(regional_stock__gt=0)  # Or has stock in region
        )

    def with_optimized_stock_prefetch(self):
        """
        Prefetch related stock items and warehouses for efficient access.

        Use this when you need to display stock information for multiple products.

        Returns:
            QuerySet with optimized prefetch_related
        """
        from catalog.models import StockItem  # Import here to avoid circular imports

        return self.prefetch_related(
            Prefetch(
                "stock_items",
                queryset=StockItem.objects.select_related("warehouse").filter(
                    warehouse__is_active=True
                ),
            )
        )

    def published(self):
        """
        Filter to only published products.

        Returns:
            QuerySet of published products
        """
        return self.filter(status="published")

    def available_in_region(self, region):
        """
        Filter products visible and available in a specific region.

        Combines visibility rules and stock availability.

        Args:
            region: SalesRegion instance

        Returns:
            QuerySet of available products
        """
        # Get products with no visibility rules (visible everywhere)
        from catalog.models import ProductRegionVisibility

        products_without_rules = self.exclude(
            id__in=ProductRegionVisibility.objects.values_list("product_id", flat=True)
        )

        # Get products with explicit visibility=True for this region
        products_with_visibility = self.filter(
            region_visibility__region=region, region_visibility__is_visible=True
        )

        # Combine and filter by stock
        visible_products = (products_without_rules | products_with_visibility).distinct()

        return visible_products.filter(
            Q(track_inventory=False)  # Not tracking inventory
            | Q(  # Has stock in region
                stock_items__warehouse__region=region,
                stock_items__warehouse__is_active=True,
                stock_items__on_hand__gt=0,
            )
        ).distinct()

    # Soft-delete methods
    def deleted(self):
        """Return only soft-deleted products"""
        return self.filter(is_deleted=True)

    def active(self):
        """Return only non-deleted products"""
        return self.filter(is_deleted=False)

    def with_deleted(self):
        """Return all products including deleted"""
        return self.all()

    def delete(self):
        """Soft delete all products in the queryset"""
        from django.utils import timezone

        return self.update(is_deleted=True, deleted_at=timezone.now())

    def hard_delete(self):
        """Permanently delete all products in the queryset"""
        return super().delete()

    def restore(self):
        """Restore all soft-deleted products in the queryset"""
        return self.update(is_deleted=False, deleted_at=None, deleted_by=None)


class ProductManager(models.Manager):
    """Manager that filters out soft-deleted products by default"""

    def get_queryset(self):
        """Return only non-deleted products by default"""
        return ProductQuerySet(self.model, using=self._db).active()

    def deleted(self):
        """Return only deleted products"""
        return ProductQuerySet(self.model, using=self._db).deleted()

    def with_deleted(self):
        """Return all products including deleted"""
        return ProductQuerySet(self.model, using=self._db)


class Product(CustomFieldsMixin, DesignMixin):
    """Main product model with design customization"""

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
        ("discontinued", "Discontinued"),
    ]

    PRODUCT_TYPES = [
        ("simple", _("Simple Product")),
        ("variable", _("Variable Product")),
        ("digital", _("Digital Product")),
        ("bundle", _("Product Bundle")),
        ("gift_card", _("Gift Card")),
        ("customizable", _("Customizable Product")),
        ("configurable", _("Configurable Product")),
        ("booking", _("Booking Product")),
    ]

    # Basic information
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255)
    sku = models.CharField(max_length=100, db_index=True)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES, default="simple")

    # Import tracking
    external_id = models.CharField(
        max_length=100,
        blank=True,
        db_index=True,
        help_text="Original ID from source platform (WooCommerce, Shopify, etc.)",
    )
    migration_job = models.ForeignKey(
        "migration.MigrationJob",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="imported_products",
        help_text="Migration job that imported this product",
    )
    imported_meta = models.JSONField(
        default=dict,
        blank=True,
        help_text="Metadata from import (SEO fields, identifiers, product attributes, etc.)",
    )

    # Categorization
    category = models.ForeignKey(Category, related_name="products", on_delete=models.PROTECT)
    brand = models.ForeignKey(
        Brand, related_name="products", on_delete=models.SET_NULL, null=True, blank=True
    )

    # Translations - all translatable content stored in JSON by language code
    # Structure: {
    #   "en": {
    #     "name": "Product Name",
    #     "description_html": "<p>Rich text description</p>",
    #     "description_text": "Plain text description",
    #     "short_description_html": "<p>Short description</p>",
    #     "short_description_text": "Plain text short description",
    #     "meta_title": "SEO Title",
    #     "meta_description": "SEO Description"
    #   },
    #   "ar": { ... }
    # }
    translations = models.JSONField(
        default=dict,
        blank=True,
        help_text="Multilingual content (name, descriptions, SEO) in both HTML and plain text formats",
    )

    # Primary language content (from site_settings.default_language)
    # These fields store content in the merchant's primary language
    # Additional languages are stored in the translations JSONField above
    short_description = CKEditor5Field(
        blank=True,
        config_name="default",
        help_text="Brief product description shown in listings (primary language)",
    )
    full_description = CKEditor5Field(
        blank=True,
        config_name="default",
        help_text="Detailed product description with rich text formatting (primary language)",
    )

    # SEO fields (primary language)
    meta_title = models.CharField(
        max_length=255, blank=True, help_text="SEO title for search engines (primary language)"
    )
    meta_description = models.TextField(
        blank=True,
        max_length=160,
        help_text="SEO meta description for search engines (primary language, max 160 characters)",
    )
    seo_auto_generated = models.BooleanField(
        default=False, help_text="Automatically regenerate SEO content when product is saved"
    )

    # Description and details (non-translatable)
    features = models.JSONField(default=dict, blank=True)  # Store feature key-value pairs
    specifications = models.JSONField(default=dict, blank=True)  # Technical specs

    # Pricing
    price = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency="USD",
        verbose_name="Regular Price",
        help_text="Standard retail price",
    )

    # Sale Settings
    SALE_TYPE_CHOICES = [
        ("none", "No Sale"),
        ("fixed_price", "Fixed Sale Price"),
        ("amount_off", "Amount Off"),
        ("percentage_off", "Percentage Off"),
    ]

    sale_type = models.CharField(
        max_length=20,
        choices=SALE_TYPE_CHOICES,
        default="none",
        verbose_name="Sale Type",
        help_text="Type of discount to apply",
    )
    sale_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Sale Value",
        help_text="Discount amount ($ or %) or fixed sale price, depending on sale type",
    )
    sale_start_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Sale Start Date",
        help_text="When the sale begins (leave empty for immediate)",
    )
    sale_end_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Sale End Date",
        help_text="When the sale ends (leave empty for no end date)",
    )

    cost = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency="USD",
        null=True,
        blank=True,
        verbose_name="Cost",
        help_text="Cost of goods for profit calculation (not shown to customers)",
    )

    # Multi-Currency Pricing Strategy
    PRICING_STRATEGY_CHOICES = [
        ("dynamic", _("Dynamic Pricing (convert from base currency)")),
        ("fixed", _("Fixed Pricing (set prices per currency)")),
    ]

    pricing_strategy = models.CharField(
        max_length=20,
        choices=PRICING_STRATEGY_CHOICES,
        default="dynamic",
        verbose_name=_("Pricing Strategy"),
        help_text=_(
            "How to calculate prices in different currencies. Dynamic: Auto-convert using exchange rates. Fixed: Set custom prices per currency."
        ),
    )

    # Bundle Pricing (only for product_type='bundle')
    BUNDLE_PRICING_STRATEGY_CHOICES = [
        ("fixed", _("Fixed Price")),
        ("percentage_discount", _("Percentage Discount")),
        ("components_sum", _("Sum of Components")),
    ]

    bundle_pricing_strategy = models.CharField(
        max_length=20,
        choices=BUNDLE_PRICING_STRATEGY_CHOICES,
        default="fixed",
        blank=True,
        verbose_name=_("Bundle Pricing Strategy"),
        help_text=_(
            "How to calculate bundle price. Fixed: Use the price field. Percentage Discount: Apply discount to component sum. Components Sum: Total of all components."
        ),
    )

    bundle_discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00"),
        blank=True,
        validators=[MinValueValidator(Decimal("0.00")), MaxValueValidator(Decimal("100.00"))],
        verbose_name=_("Bundle Discount Percentage"),
        help_text=_(
            "Discount percentage off component total (e.g., 15.00 for 15% off). Only used with 'Percentage Discount' strategy."
        ),
    )

    # Gift Card Configuration (only for product_type='gift_card')
    GIFT_CARD_DENOMINATION_TYPE_CHOICES = [
        ("fixed", _("Fixed Denominations")),
        ("custom", _("Customer Chooses Amount")),
        ("both", _("Both Fixed and Custom")),
    ]

    gift_card_denomination_type = models.CharField(
        max_length=20,
        choices=GIFT_CARD_DENOMINATION_TYPE_CHOICES,
        default="fixed",
        blank=True,
        verbose_name=_("Denomination Type"),
        help_text=_(
            "How customers select gift card value. Fixed: Choose from preset amounts. Custom: Enter any amount. Both: Preset amounts + custom option."
        ),
    )

    gift_card_denominations = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("Fixed Denominations"),
        help_text=_(
            "List of preset amounts (e.g., [25, 50, 100, 200]). Currency symbol not needed."
        ),
    )

    gift_card_min_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.01"))],
        verbose_name=_("Minimum Amount"),
        help_text=_("Minimum value for custom amount gift cards"),
    )

    gift_card_max_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.01"))],
        verbose_name=_("Maximum Amount"),
        help_text=_("Maximum value for custom amount gift cards"),
    )

    gift_card_expires_days = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name=_("Expires After (Days)"),
        help_text=_("Days until gift card expires after purchase (0 = never expires)"),
    )

    gift_card_currency = models.CharField(
        max_length=3,
        blank=True,
        null=True,
        verbose_name=_("Gift Card Currency"),
        help_text=_(
            "Currency for issued gift cards. Leave blank for store's base currency. "
            "When set, gift cards are issued in this currency with value converted "
            "at the exchange rate at time of purchase."
        ),
    )

    # Customization Configuration (for customizable products)
    allow_customization = models.BooleanField(
        default=False,
        verbose_name=_("Allow Customization"),
        help_text=_("Does this product support customer customization (text, images, choices)?"),
    )
    customization_preview_template = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Preview Template"),
        help_text=_("Template name for rendering customization preview (optional)"),
    )

    # Configurator Configuration (only for product_type='configurable')
    CONFIGURATOR_PRICING_STRATEGY_CHOICES = [
        ("components_sum", _("Sum of Components")),
        ("base_plus_adjustments", _("Base Price + Adjustments")),
        ("fixed", _("Fixed Price")),
    ]

    configurator_pricing_strategy = models.CharField(
        max_length=25,
        choices=CONFIGURATOR_PRICING_STRATEGY_CHOICES,
        default="components_sum",
        blank=True,
        verbose_name=_("Configurator Pricing Strategy"),
        help_text=_(
            "How the final price is calculated. Sum of Components: total of all selected options. "
            "Base + Adjustments: base price plus per-option surcharges. Fixed: use the product price field."
        ),
    )

    configurator_base_price = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency="USD",
        null=True,
        blank=True,
        verbose_name=_("Configurator Base Price"),
        help_text=_(
            "Starting price for 'Base Price + Adjustments' strategy. "
            "Each option's price adjustment is added to this amount."
        ),
    )

    # Subscription Configuration
    is_subscription_enabled = models.BooleanField(
        default=False,
        verbose_name=_("Enable Subscription"),
        help_text=_(
            "Allow customers to purchase this product as a subscription with recurring billing"
        ),
    )
    subscription_plans = models.ManyToManyField(
        "subscriptions.SubscriptionPlan",
        blank=True,
        related_name="products",
        verbose_name=_("Subscription Plans"),
        help_text=_(
            "Available subscription plans for this product. Customers can choose from these plans."
        ),
    )
    allow_one_time_purchase = models.BooleanField(
        default=True,
        verbose_name=_("Allow One-Time Purchase"),
        help_text=_(
            "Allow customers to buy this product without a subscription. If disabled, subscription is required."
        ),
    )
    subscription_default = models.BooleanField(
        default=False,
        verbose_name=_("Default to Subscription"),
        help_text=_(
            "Pre-select subscription option in the product interface (one-time purchase must also be allowed)"
        ),
    )

    # Inventory
    track_inventory = models.BooleanField(default=True)
    # NOTE: quantity field removed - inventory now tracked via StockItem model
    low_stock_threshold = models.IntegerField(default=5)
    allow_backorders = models.BooleanField(default=False)

    # Stock settings override (None = use category, then site-wide)
    out_of_stock_action_override = models.CharField(
        _("out of stock action override"),
        max_length=20,
        choices=[
            ("hide", _("Hide from listings")),
            ("show_unavailable", _("Show as unavailable")),
            ("notify_me", _('Show "Notify Me" button')),
            ("allow_backorder", _("Allow backorders")),
        ],
        null=True,
        blank=True,
        help_text=_("Override category/site out-of-stock behavior for this product"),
    )

    # Pre-order support
    is_preorder = models.BooleanField(
        _("is pre-order"),
        default=False,
        help_text=_("Enable pre-order for this product (useful for upcoming releases)"),
    )
    preorder_release_date = models.DateField(
        _("pre-order release date"),
        null=True,
        blank=True,
        help_text=_("Expected release/availability date for pre-orders"),
    )
    preorder_message = models.CharField(
        _("pre-order message"),
        max_length=200,
        blank=True,
        help_text=_('Custom pre-order message (e.g., "Ships March 2025")'),
    )

    # Physical attributes
    weight = models.DecimalField(
        max_digits=10, decimal_places=3, null=True, blank=True, help_text="Weight in kg"
    )
    length = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, help_text="Length in cm"
    )
    width = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, help_text="Width in cm"
    )
    height = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, help_text="Height in cm"
    )

    # Shipping package preference
    preferred_shipping_package = models.ForeignKey(
        "shipping.ShippingPackage",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        verbose_name=_("Preferred Shipping Package"),
        help_text=_(
            "Default package to use for shipping this product. If set, package dimensions will be used instead of product dimensions for shipping calculations."
        ),
    )

    # Product Identifiers (GTINs and other standard codes)
    gtin = models.CharField(
        max_length=14,
        blank=True,
        verbose_name=_("GTIN"),
        help_text=_("Global Trade Item Number (GTIN-8, GTIN-12, GTIN-13, or GTIN-14)"),
    )

    ean = models.CharField(
        max_length=13,
        blank=True,
        verbose_name=_("EAN"),
        help_text=_("European Article Number (EAN-13 or EAN-8)"),
    )

    upc = models.CharField(
        max_length=12,
        blank=True,
        verbose_name=_("UPC"),
        help_text=_("Universal Product Code (UPC-A or UPC-E)"),
    )

    isbn = models.CharField(
        max_length=13,
        blank=True,
        verbose_name=_("ISBN"),
        help_text=_("International Standard Book Number (ISBN-10 or ISBN-13, for books)"),
    )

    asin = models.CharField(
        max_length=10,
        blank=True,
        verbose_name=_("ASIN"),
        help_text=_("Amazon Standard Identification Number"),
    )

    mpn = models.CharField(
        max_length=70, blank=True, verbose_name=_("MPN"), help_text=_("Manufacturer Part Number")
    )

    # International Shipping / Customs Fields
    hs_code = models.CharField(
        max_length=12,
        blank=True,
        db_index=True,
        verbose_name=_("HS Code"),
        help_text=_(
            "Harmonized System code (6-12 digits) for customs classification. "
            "Required for international shipping. Look up at hts.usitc.gov"
        ),
    )

    country_of_origin = models.CharField(
        max_length=2,
        blank=True,
        verbose_name=_("Country of Origin"),
        help_text=_(
            "ISO 3166-1 alpha-2 country code where product was manufactured. "
            "Required for international shipping. Example: US, CN, DE"
        ),
    )

    unit_price_for_customs = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.01"))],
        verbose_name=_("Customs Unit Price"),
        help_text=_(
            "Declared value per unit for customs purposes. May differ from retail price. "
            "Use cost or wholesale price if retail is significantly higher."
        ),
    )

    export_license_number = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("Export License Number"),
        help_text=_(
            "Required for controlled/restricted items (ITAR, EAR). Leave blank for most products."
        ),
    )

    export_license_expiry = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Export License Expiry"),
        help_text=_("Expiration date of export license"),
    )

    # Product page customization
    GALLERY_TYPES = [
        ("standard", "Standard Gallery"),
        ("carousel", "Carousel"),
        ("grid", "Grid Layout"),
        ("zoom", "Zoom Gallery"),
        ("360", "360° View"),
    ]

    PAGE_TEMPLATE_CHOICES = [
        ("", _("Use Site Default")),
        ("classic", _("Classic")),
        ("full_width", _("Full Width")),
        ("gallery_focus", _("Gallery Focus")),
        ("digital", _("Digital")),
    ]

    page_template = models.CharField(
        max_length=30,
        blank=True,
        choices=PAGE_TEMPLATE_CHOICES,
        default="",
        verbose_name=_("Page Template"),
        help_text=_(
            "Override the site default product page template. Leave empty to use the site default from Design settings."
        ),
    )

    gallery_type = models.CharField(
        max_length=20,
        choices=GALLERY_TYPES,
        default="standard",
        help_text="How product images are displayed",
    )

    show_related_products = models.BooleanField(default=True)
    show_reviews = models.BooleanField(default=True)
    show_specifications = models.BooleanField(default=True)

    # Content sections for product page
    product_sections = models.JSONField(
        default=list, blank=True, help_text="Custom content sections for product page"
    )

    # Status and visibility
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    is_featured = models.BooleanField(default=False)
    is_digital = models.BooleanField(
        default=False,
        verbose_name=_("Is Digital Product"),
        help_text=_(
            "Check if this product includes digital downloads (e.g., files, licenses). Can be combined with any product type for scenarios like variable digital products (software with Basic/Pro editions) or customizable digital products (custom designs)."
        ),
    )
    hide_from_storefront = models.BooleanField(
        default=False,
        verbose_name=_("Hide from Storefront"),
        help_text=_(
            "Hide this product from catalog listings and search results. "
            "The product remains available as a configurator option or bundle component."
        ),
    )
    license_template = models.ForeignKey(
        "LicenseKeyTemplate",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        verbose_name=_("License Key Template"),
        help_text=_(
            "Custom license key format for digital products. If not set, uses default format."
        ),
    )
    default_license_type = models.CharField(
        max_length=20,
        choices=[
            ("perpetual", _("Perpetual")),
            ("subscription", _("Subscription")),
            ("trial", _("Trial")),
            ("nfr", _("Not For Resale")),
            ("educational", _("Educational")),
            ("standard", _("Standard")),
        ],
        default="perpetual",
        verbose_name=_("Default License Type"),
        help_text=_("Default license type for this product when licenses are generated."),
    )
    default_max_activations = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Default Max Activations"),
        help_text=_("Default maximum device activations per license. Leave blank for unlimited."),
    )
    default_validity_days = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Default Validity (Days)"),
        help_text=_(
            "Default license validity in days from issue date. Leave blank for never expires."
        ),
    )
    license_provider = models.ForeignKey(
        "LicenseProvider",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="licensed_products",
        verbose_name=_("License Provider"),
        help_text=_("External provider to sync licenses to when orders are placed."),
    )
    external_product_id = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("External Product ID"),
        help_text=_("Product/Policy ID in the external license provider system."),
    )
    requires_license = models.BooleanField(
        default=False,
        verbose_name=_("Generate License Key"),
        help_text=_(
            "Generate a license key when this product is purchased. Enable for software licenses, API keys, or activation codes."
        ),
    )

    LICENSE_GENERATION_TRIGGER_CHOICES = [
        ("on_payment", _("When payment is confirmed")),
        ("on_order", _("When order is created")),
        ("manual", _("Manual only (admin generates)")),
    ]
    license_generation_trigger = models.CharField(
        max_length=20,
        choices=LICENSE_GENERATION_TRIGGER_CHOICES,
        default="on_payment",
        verbose_name=_("Generate License"),
        help_text=_("When to automatically generate the license key for this product."),
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Statistics
    views_count = models.PositiveIntegerField(default=0)
    sales_count = models.PositiveIntegerField(default=0)

    # POS / Sales Channel
    SALES_CHANNEL_CHOICES = [
        ("all", _("All Channels")),
        ("online_only", _("Online Only")),
        ("pos_only", _("In-Store Only")),
    ]
    sales_channel = models.CharField(
        _("sales channel"),
        max_length=20,
        choices=SALES_CHANNEL_CHOICES,
        default="all",
        db_index=True,
        help_text=_("Where this product can be sold"),
    )
    barcode = models.CharField(
        _("barcode"),
        max_length=50,
        blank=True,
        db_index=True,
        help_text=_("EAN/UPC barcode for POS scanning"),
    )

    # Tags (lightweight product tagging distinct from Collections)
    tags = models.ManyToManyField(
        "ProductTag",
        blank=True,
        related_name="products",
        verbose_name=_("Tags"),
        help_text=_("Tags for product organization and filtering"),
    )

    # Soft-delete fields
    is_deleted = models.BooleanField(
        default=False, db_index=True, help_text=_("Whether this product has been soft deleted")
    )
    deleted_at = models.DateTimeField(
        null=True, blank=True, db_index=True, help_text=_("When this product was soft deleted")
    )
    deleted_by = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="catalog_product_deleted",
        help_text=_("User who deleted this product"),
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["sku"]),
            models.Index(fields=["status"]),
            models.Index(fields=["is_featured"]),
            models.Index(fields=["-created_at"]),
            models.Index(fields=["hs_code"], name="catalog_pro_hs_code_idx"),
            models.Index(fields=["country_of_origin"], name="catalog_pro_country_idx"),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["slug"],
                condition=models.Q(is_deleted=False),
                name="unique_active_product_slug",
            ),
            models.UniqueConstraint(
                fields=["sku"],
                condition=models.Q(is_deleted=False),
                name="unique_active_product_sku",
            ),
        ]

    # Custom managers for performance-optimized queries and soft-delete
    objects = ProductManager()  # Filters deleted by default
    all_objects = models.Manager()  # Includes deleted products

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        # Auto-set is_digital based on product_type
        # Digital products and gift cards are always digital
        if self.product_type in ["digital", "gift_card"]:
            self.is_digital = True
        # For bundles, check if ALL components are digital
        elif self.product_type == "bundle":
            # Only check if this is an existing bundle (has ID)
            # New bundles will be saved as not digital, then updated when components are added
            if self.pk:
                self.is_digital = self.is_bundle_digital()
            else:
                self.is_digital = False
        # Simple and variable products are not digital by default
        else:
            self.is_digital = False

        # Booking products use slot-based capacity, not stock inventory
        if self.product_type == "booking":
            self.track_inventory = False

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/product/{self.slug}/"

    # ============================================================================
    # Soft-Delete Methods
    # ============================================================================

    def delete(self, using=None, keep_parents=False, user=None):
        """
        Soft delete the product instead of actually deleting it.
        Releases all active stock reservations for this product.

        Args:
            user: The user performing the deletion (optional)

        Note: Related models (StockItem, ProductImage, etc.) remain active
        but are hidden via Product.is_deleted filter in queries.
        """
        from django.utils import timezone

        # Release all active stock reservations for this product
        from catalog.models import StockReservation

        StockReservation.objects.filter(
            stock_item__product=self, expires_at__gt=timezone.now()
        ).delete()

        # Perform soft delete
        self.is_deleted = True
        self.deleted_at = timezone.now()
        if user:
            self.deleted_by = user
        self.save(update_fields=["is_deleted", "deleted_at", "deleted_by"])

    def hard_delete(self, using=None, keep_parents=False):
        """
        Actually delete the product from the database.
        Use with caution! This will CASCADE delete all related data.

        Raises:
            ProtectedError: If the product has associated orders (PROTECT constraint)
        """
        super().delete(using=using, keep_parents=keep_parents)

    def restore(self):
        """
        Restore a soft-deleted product.

        Raises:
            ValidationError: If SKU is already in use by another product
        """
        from django.core.exceptions import ValidationError

        # Check if SKU is now taken by another product
        if Product.objects.filter(sku=self.sku).exists():
            raise ValidationError(
                f"Cannot restore: SKU {self.sku} is already in use by another product. "
                f"Change the SKU before restoring."
            )

        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by = None
        self.save(update_fields=["is_deleted", "deleted_at", "deleted_by"])

    @property
    def is_active(self):
        """Check if the product is active (not deleted)"""
        return not self.is_deleted

    # ============================================================================
    # Multi-Location Inventory Properties
    # ============================================================================

    @property
    def total_stock(self):
        """Total stock across all warehouses"""
        from django.db.models import Sum

        return self.stock_items.aggregate(total=Sum("on_hand"))["total"] or 0

    @property
    def available_stock(self):
        """Available stock (on_hand - allocated) across all warehouses"""
        from django.db.models import F, Sum

        return self.stock_items.aggregate(total=Sum(F("on_hand") - F("allocated")))["total"] or 0

    @property
    def allocated_stock(self):
        """Total allocated stock across all warehouses"""
        from django.db.models import Sum

        return self.stock_items.aggregate(total=Sum("allocated"))["total"] or 0

    @property
    def variant_stock_summary(self):
        """
        Get stock summary for variable products.
        Returns aggregated stock data for all variants.
        For simple products, returns None.
        """
        if self.product_type != "variable":
            return None

        from django.db.models import F, Sum

        variants_data = []
        for variant in self.variants.all():
            variant_stock = variant.stock_items.aggregate(
                total_on_hand=Sum("on_hand"),
                total_allocated=Sum("allocated"),
                total_available=Sum(F("on_hand") - F("allocated")),
            )

            variants_data.append(
                {
                    "variant": variant,
                    "on_hand": variant_stock["total_on_hand"] or 0,
                    "allocated": variant_stock["total_allocated"] or 0,
                    "available": variant_stock["total_available"] or 0,
                }
            )

        # Calculate totals across all variants
        totals = self.stock_items.filter(variant__isnull=False).aggregate(
            total_on_hand=Sum("on_hand"),
            total_allocated=Sum("allocated"),
            total_available=Sum(F("on_hand") - F("allocated")),
        )

        return {
            "variants": variants_data,
            "total_on_hand": totals["total_on_hand"] or 0,
            "total_allocated": totals["total_allocated"] or 0,
            "total_available": totals["total_available"] or 0,
        }

    def get_variant_stock_status(self, variant):
        """
        Get stock status for a specific variant.
        Returns: 'in_stock', 'low_stock', or 'out_of_stock'
        """
        from django.db.models import F, Sum

        available = (
            variant.stock_items.aggregate(total=Sum(F("on_hand") - F("allocated")))["total"] or 0
        )

        if available <= 0:
            return "out_of_stock"
        elif available <= self.low_stock_threshold:
            return "low_stock"
        else:
            return "in_stock"

    def get_stock_in_region(self, region):
        """Get total available stock in a specific region"""
        from django.db.models import F, Sum

        return (
            self.stock_items.filter(warehouse__region=region, warehouse__is_active=True).aggregate(
                total=Sum(F("on_hand") - F("allocated"))
            )["total"]
            or 0
        )

    def is_visible_in_region(self, region):
        """Check if product should be visible in a region"""
        # If no visibility records exist, product is visible everywhere
        visibility_rules = self.region_visibility.filter(region=region)
        if not visibility_rules.exists():
            return True
        return visibility_rules.filter(is_visible=True).exists()

    @property
    def is_in_stock(self):
        if not self.track_inventory:
            return True
        return self.available_stock > 0 or self.allow_backorders

    @property
    def is_low_stock(self):
        if not self.track_inventory:
            return False
        return self.available_stock <= self.low_stock_threshold

    def get_effective_out_of_stock_action(self):
        """
        Get effective out-of-stock action with cascading override.
        Priority: product > category > site-wide
        """
        # Check product-level override first
        if self.out_of_stock_action_override:
            return self.out_of_stock_action_override
        # Check category-level override
        if self.category and self.category.out_of_stock_action_override:
            return self.category.out_of_stock_action_override
        # Fall back to site-wide settings
        return StockDisplaySettings.get_settings().out_of_stock_action

    def get_effective_allow_backorders(self):
        """
        Get effective backorder setting with cascading override.
        Priority: product > category > site-wide
        """
        # Product-level allow_backorders is already a concrete value (True/False)
        # We need to check if it was explicitly set vs using default
        # For simplicity, if allow_backorders is True, use it; otherwise check category
        if self.allow_backorders:
            return True
        # Check category-level override
        if self.category and self.category.allow_backorders_override is not None:
            return self.category.allow_backorders_override
        # Fall back to site-wide settings
        return StockDisplaySettings.get_settings().allow_backorders

    @property
    def is_on_sale(self):
        """Check if product is currently on sale based on sale dates"""
        if self.sale_type == "none":
            return False

        now = timezone.now()

        # Check start date
        if self.sale_start_date and self.sale_start_date > now:
            return False

        # Check end date
        if self.sale_end_date and self.sale_end_date < now:  # noqa: SIM103 — multi-guard pattern reads clearer than compressed form
            return False

        # Sale is active
        return True

    def calculate_sale_price(self):
        """Calculate the sale price based on sale_type and sale_value"""
        if not self.is_on_sale or not self.sale_value:
            return None

        base_price = self.price.amount

        if self.sale_type == "fixed_price":
            return Decimal(str(self.sale_value))

        elif self.sale_type == "amount_off":
            sale_price = base_price - Decimal(str(self.sale_value))
            return max(sale_price, Decimal("0.01"))  # Never go below $0.01

        elif self.sale_type == "percentage_off":
            discount_amount = base_price * (Decimal(str(self.sale_value)) / Decimal("100"))
            sale_price = base_price - discount_amount
            return max(sale_price, Decimal("0.01"))

        return None

    @property
    def effective_price(self):
        """Get the price that should be shown to customers"""
        sale_price = self.calculate_sale_price()

        if sale_price:
            # Return Money object with same currency as regular price
            from djmoney.money import Money

            return Money(sale_price, self.price.currency)

        return self.price

    @property
    def has_discount(self):
        """Check if product currently has any discount"""
        return self.effective_price < self.price

    @property
    def discount_percentage(self):
        """Calculate discount percentage"""
        if not self.has_discount:
            return 0

        savings = self.price - self.effective_price
        discount = (savings / self.price) * Decimal("100")
        return round(discount)

    @property
    def savings_amount(self):
        """Get the amount saved"""
        if not self.has_discount:
            from djmoney.money import Money

            return Money(0, self.price.currency)

        return self.price - self.effective_price

    def sale_expires_in(self):
        """Get human-readable time until sale ends"""
        if not self.is_on_sale or not self.sale_end_date:
            return None

        now = timezone.now()
        remaining = self.sale_end_date - now

        if remaining.days > 0:
            return f"{remaining.days} day{'s' if remaining.days != 1 else ''}"
        elif remaining.seconds > 3600:
            hours = remaining.seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''}"
        elif remaining.seconds > 60:
            minutes = remaining.seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''}"
        else:
            return "Less than a minute"

    @property
    def requires_shipping(self):
        """Check if product requires shipping (digital/booking products don't)"""
        return self.product_type not in ("digital", "booking")

    @property
    def primary_image(self):
        """Get the primary product image, or first image if no primary set"""
        # First try to get the primary image
        primary = self.images.filter(is_primary=True).first()
        if primary and primary.media_asset:
            return primary.media_asset
        # Fall back to first image
        first_image = self.images.first()
        if first_image and first_image.media_asset:
            return first_image.media_asset
        return None

    @property
    def primary_image_url(self):
        """Get URL for primary product image"""
        img = self.primary_image
        return img.get_display_url() if img else None

    @property
    def primary_image_listing_url(self):
        """Get optimized thumbnail URL for product listing cards (400x400)"""
        img = self.primary_image
        if img:
            return img.get_thumbnail("product_listing")
        return None

    @property
    def primary_image_large_url(self):
        """Get large thumbnail URL for featured/hero displays (1200x1200)"""
        img = self.primary_image
        if img:
            return img.get_thumbnail("large")
        return None

    @property
    def formatted_price(self):
        """Get the effective price formatted for display"""
        return str(self.effective_price)

    @property
    def formatted_compare_price(self):
        """Get the original price formatted for display (when on sale)"""
        return str(self.price)

    # ============================================================================
    # Bundle Product Methods
    # ============================================================================

    def get_bundle_component_total(self):
        """Calculate sum of all bundle components."""
        if self.product_type != "bundle":
            return None

        from djmoney.money import Money

        total_amount = Decimal("0.00")

        for item in self.bundle_items.all():
            total_amount += item.get_total_price()

        return Money(total_amount, self.price.currency)

    def get_effective_bundle_price(self):
        """Calculate bundle price based on strategy."""
        if self.product_type != "bundle":
            return self.effective_price

        component_total = self.get_bundle_component_total()

        if not component_total:
            # Empty bundle, return regular price
            return self.price

        if self.bundle_pricing_strategy == "fixed":
            # Use the price field directly
            return self.effective_price

        elif self.bundle_pricing_strategy == "percentage_discount":
            # Apply percentage discount to component total
            discount_multiplier = (Decimal("100.00") - self.bundle_discount_percentage) / Decimal(
                "100.00"
            )
            discounted_amount = component_total.amount * discount_multiplier

            from djmoney.money import Money

            return Money(discounted_amount, self.price.currency)

        elif self.bundle_pricing_strategy == "components_sum":
            # Return sum of all components
            return component_total

        # Default to regular price
        return self.price

    def validate_bundle_inventory(self, warehouse=None):
        """Check if all bundle components are in stock."""
        if self.product_type != "bundle":
            return True

        return all(item.check_stock_availability(warehouse) for item in self.bundle_items.all())

    def is_bundle_digital(self):
        """Check if all bundle components are digital."""
        if self.product_type != "bundle":
            return self.is_digital

        # Empty bundles are not digital
        if not self.bundle_items.exists():
            return False

        # All components must be digital
        return all(item.component_product.is_digital for item in self.bundle_items.all())

    def get_effective_design(self):
        """Get effective design settings including category inheritance"""
        design = {
            "template_variant": self.template_variant,
            "css_classes": self.css_classes,
            "layout_config": self.layout_config,
            "style_overrides": self.style_overrides,
            "gallery_type": self.gallery_type,
        }

        # Inherit from category if enabled
        if self.inherit_parent_theme and self.category and self.category.cascade_theme_to_products:
            category_theme = self.category.get_effective_theme()
            # Merge category theme with product overrides
            for key in ["css_classes", "layout_config", "style_overrides"]:
                if key in design and key in category_theme:
                    if isinstance(design[key], dict) and isinstance(category_theme[key], dict):
                        merged = category_theme[key].copy()
                        merged.update(design[key])
                        design[key] = merged

        return design

    def get_translation(self, language_code, field_name, fallback=True):
        """
        Get translated value for a specific field.

        Args:
            language_code: Language code (e.g., 'en', 'ar')
            field_name: Field name to retrieve (e.g., 'name', 'description_html', 'description_text')
            fallback: If True, fall back to default language if translation not found

        Returns:
            Translated string or empty string if not found
        """
        if not self.translations:
            return ""

        # Try to get translation for requested language
        lang_data = self.translations.get(language_code, {})
        if field_name in lang_data:
            return lang_data[field_name]

        # Fallback to default language if enabled
        if fallback:
            from django.conf import settings

            default_lang = getattr(settings, "LANGUAGE_CODE", "en")
            if language_code != default_lang:
                default_data = self.translations.get(default_lang, {})
                return default_data.get(field_name, "")

        return ""

    def set_translation(self, language_code, field_name, value):
        """
        Set translated value for a specific field.

        Args:
            language_code: Language code (e.g., 'en', 'ar')
            field_name: Field name to set (e.g., 'name', 'description_html')
            value: Value to set
        """
        if not self.translations:
            self.translations = {}

        if language_code not in self.translations:
            self.translations[language_code] = {}

        self.translations[language_code][field_name] = value

    def get_translated_name(self, language_code=None):
        """
        Get product name in specified language (or current language).

        For the primary language, returns the name field.
        For other languages, returns translation from the translations JSON.
        """
        if language_code is None:
            from django.utils.translation import get_language

            language_code = get_language()

        # Check if this is the primary language
        from core.translation_utils import get_primary_language

        primary_lang = get_primary_language()

        # For primary language, use database field
        if language_code == primary_lang:
            return self.name or ""

        # For other languages, use translations JSON
        return self.get_translation(language_code, "name")

    def get_translated_description(self, language_code=None, plain_text=False):
        """
        Get product description in specified language.

        For the primary language, returns the full_description field.
        For other languages, returns translation from the translations JSON.
        """
        if language_code is None:
            from django.utils.translation import get_language

            language_code = get_language()

        # Check if this is the primary language
        from core.translation_utils import get_primary_language

        primary_lang = get_primary_language()

        # For primary language, use database field
        if language_code == primary_lang:
            if plain_text:
                # Strip HTML tags from full_description for plain text
                from django.utils.html import strip_tags

                return strip_tags(self.full_description) if self.full_description else ""
            return self.full_description or ""

        # For other languages, use translations JSON
        field_name = "description_text" if plain_text else "description_html"
        return self.get_translation(language_code, field_name)

    def get_translated_short_description(self, language_code=None, plain_text=False):
        """
        Get product short description in specified language.

        For the primary language, returns the short_description field.
        For other languages, returns translation from the translations JSON.
        """
        if language_code is None:
            from django.utils.translation import get_language

            language_code = get_language()

        # Check if this is the primary language
        from core.translation_utils import get_primary_language

        primary_lang = get_primary_language()

        # For primary language, use database field
        if language_code == primary_lang:
            if plain_text:
                # Strip HTML tags from short_description for plain text
                from django.utils.html import strip_tags

                return strip_tags(self.short_description) if self.short_description else ""
            return self.short_description or ""

        # For other languages, use translations JSON
        field_name = "short_description_text" if plain_text else "short_description_html"
        return self.get_translation(language_code, field_name)

    # International Shipping Methods
    def is_international_shipping_ready(self):
        """Check if product has all required data for international shipments."""
        return bool(self.hs_code and self.country_of_origin and self.unit_price_for_customs)

    def get_missing_customs_fields(self):
        """Return list of missing fields needed for international shipping."""
        missing = []
        if not self.hs_code:
            missing.append("hs_code")
        if not self.country_of_origin:
            missing.append("country_of_origin")
        if not self.unit_price_for_customs:
            missing.append("unit_price_for_customs")
        return missing

    def get_price_in_currency(self, currency_code: str):
        """
        Get product price in specified currency.

        Uses pricing strategy to determine price:
        - Fixed: Look up ProductPrice for currency
        - Dynamic: Convert base price using exchange rates

        Args:
            currency_code: Target currency code (e.g., 'EUR')

        Returns:
            Money object in target currency
        """
        from djmoney.money import Money

        from core.models import SiteSettings
        from exchange_rates.services.exchange_service import ExchangeRateService

        settings = SiteSettings.get_settings()

        # If multi-currency not enabled or requesting base currency, return base price
        if not settings.enable_multi_currency or currency_code == str(self.price.currency):
            return self.get_effective_price()

        # Fixed pricing: Look for ProductPrice
        if self.pricing_strategy == "fixed":
            try:
                product_price = self.currency_prices.get(currency=currency_code, is_active=True)
                return product_price.get_effective_price()
            except Exception:
                # Fallback to dynamic if no fixed price exists
                pass

        # Dynamic pricing: Convert using exchange rates
        service = ExchangeRateService()
        base_price = self.get_effective_price()

        converted_amount = service.convert(
            base_price.amount, str(base_price.currency), currency_code
        )

        # Apply price charming if rule exists
        converted_amount = self._apply_price_charming(converted_amount, currency_code)

        return Money(converted_amount, currency_code)

    def get_effective_price(self):
        """
        Get the effective price (sale price if active, otherwise regular price).

        Returns:
            Money object with effective price
        """
        from django.utils import timezone

        # Check if sale is active
        if self.sale_type != "none" and self.sale_value:
            now = timezone.now()

            # Check sale date range
            sale_active = True
            if self.sale_start_date and now < self.sale_start_date:
                sale_active = False
            if self.sale_end_date and now > self.sale_end_date:
                sale_active = False

            if sale_active:
                if self.sale_type == "fixed_price":
                    # Return the fixed sale price
                    from djmoney.money import Money

                    return Money(self.sale_value, self.price.currency)
                elif self.sale_type == "percentage_off":
                    # Calculate percentage discount
                    discount_amount = self.price.amount * (self.sale_value / 100)
                    sale_price = self.price.amount - discount_amount
                    from djmoney.money import Money

                    return Money(sale_price, self.price.currency)
                elif self.sale_type == "amount_off":
                    # Calculate amount discount
                    sale_price = self.price.amount - self.sale_value
                    from djmoney.money import Money

                    return Money(max(sale_price, 0), self.price.currency)  # Don't go below 0

        return self.price

    def _apply_price_charming(self, amount: Decimal, currency_code: str) -> Decimal:
        """
        Apply price charming rules if configured for currency.

        Args:
            amount: Price amount
            currency_code: Currency code

        Returns:
            Charmed price amount
        """
        try:
            rule = PriceCharmingRule.objects.get(currency=currency_code, is_active=True)
            return rule.apply_charm(amount)
        except PriceCharmingRule.DoesNotExist:
            return amount

    def clean(self):
        """Validate model fields."""
        import re

        from django.core.exceptions import ValidationError

        super().clean()

        # Validate price amount (MoneyField validation)
        if self.price and self.price.amount <= 0:
            raise ValidationError({"price": _("Price must be greater than zero.")})

        # Validate HS code format if provided
        if self.hs_code and not re.match(r"^\d{6,12}$", self.hs_code):
            raise ValidationError(
                {"hs_code": _("HS code must be 6-12 digits. Example: 620342 or 62034235")}
            )

        # Validate country of origin if provided
        if self.country_of_origin:
            # Check format (2-letter uppercase)
            if not re.match(r"^[A-Z]{2}$", self.country_of_origin.upper()):
                raise ValidationError(
                    {
                        "country_of_origin": _(
                            "Country code must be 2-letter ISO code. Example: US, CA, DE"
                        )
                    }
                )
            # Auto-uppercase
            self.country_of_origin = self.country_of_origin.upper()

        # Validate customs price is set if HS code is set
        if self.hs_code and not self.unit_price_for_customs:
            raise ValidationError(
                {
                    "unit_price_for_customs": _(
                        "Customs unit price is required when HS code is specified"
                    )
                }
            )

        # Validate export license expiry is in future if set
        if self.export_license_expiry and self.export_license_expiry < timezone.now().date():
            raise ValidationError(
                {"export_license_expiry": _("Export license expiry date must be in the future")}
            )

        # Validate gift_card_currency
        if self.gift_card_currency:
            if self.product_type != "gift_card":
                raise ValidationError(
                    {
                        "gift_card_currency": _(
                            "Gift card currency can only be set on gift card products."
                        )
                    }
                )
            # Validate it's a supported currency
            from core.models import SiteSettings

            settings = SiteSettings.get_settings()
            if self.gift_card_currency == settings.default_currency:
                # If same as base currency, clear it (no conversion needed)
                self.gift_card_currency = None
            elif (
                settings.supported_currencies
                and self.gift_card_currency not in settings.supported_currencies
            ):
                raise ValidationError(
                    {
                        "gift_card_currency": _(
                            'Currency "%(currency)s" is not in the store\'s supported currencies.'
                        )
                        % {"currency": self.gift_card_currency}
                    }
                )


class BundleItem(models.Model):
    """
    Individual items that make up a product bundle.
    A bundle product can have multiple component products.
    """

    bundle = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="bundle_items",
        limit_choices_to={"product_type": "bundle"},
        help_text=_("Bundle product this item belongs to"),
    )
    component_product = models.ForeignKey(
        "Product",
        on_delete=models.PROTECT,  # Prevent deletion if used in bundle
        related_name="included_in_bundles",
        help_text=_("Product included in this bundle"),
    )
    component_variant = models.ForeignKey(
        "ProductVariant",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="included_in_bundles",
        help_text=_("Specific variant (if component is variable product)"),
    )
    quantity = models.PositiveIntegerField(
        default=1, help_text=_("How many of this component are included")
    )
    sort_order = models.IntegerField(default=0, help_text=_("Display order in bundle"))
    is_optional = models.BooleanField(
        default=False, help_text=_("Can customers exclude this item? (for customizable bundles)")
    )
    allow_variant_selection = models.BooleanField(
        default=False,
        help_text=_(
            "If True, customer chooses variant at purchase time. "
            "If False, use the pre-selected component_variant."
        ),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Bundle Item")
        verbose_name_plural = _("Bundle Items")
        ordering = ["sort_order", "id"]
        unique_together = [("bundle", "component_product", "component_variant")]
        indexes = [
            models.Index(fields=["bundle"]),
            models.Index(fields=["component_product"]),
        ]

    def __str__(self):
        variant_str = f" ({self.component_variant})" if self.component_variant else ""
        return f"{self.bundle.name}: {self.quantity}x {self.component_product.name}{variant_str}"

    def clean(self):
        """Validate bundle item configuration."""
        from django.core.exceptions import ValidationError

        # Prevent bundle recursion
        if (
            self.bundle_id
            and self.component_product_id
            and self.bundle_id == self.component_product_id
        ):
            raise ValidationError(_("A bundle cannot contain itself."))

        # Prevent bundle products from being used as components
        # This also eliminates the need for circular dependency checking
        if self.component_product and self.component_product.product_type == "bundle":
            raise ValidationError(
                _(
                    "Bundle products cannot be used as components. Only simple and variable products are allowed."
                )
            )

        # Validate variant belongs to product
        if self.component_variant and self.component_product_id:
            if self.component_variant.product_id != self.component_product_id:
                raise ValidationError(
                    _("Variant %(variant)s does not belong to product %(product)s.")
                    % {"variant": self.component_variant, "product": self.component_product}
                )

        # Validate simple products don't have variant
        if (
            self.component_product
            and self.component_product.product_type == "simple"
            and self.component_variant
        ):
            raise ValidationError(_("Simple products cannot have variants."))

        # Validate allow_variant_selection
        if self.allow_variant_selection:
            # Only variable products can have customer variant selection
            if self.component_product and self.component_product.product_type != "variable":
                raise ValidationError(
                    _("Customer variant selection is only available for variable products.")
                )
            # Clear any pre-selected variant when customer selects
            if self.component_variant:
                self.component_variant = None

    def _has_circular_dependency(self):
        """Check if adding this item would create circular dependency."""
        # If component is also a bundle, check its components
        if not self.component_product or self.component_product.product_type != "bundle":
            return False

        # Recursive check
        visited = set()
        return self._check_circular(self.bundle, visited)

    def _check_circular(self, checking_bundle, visited):
        """Recursive circular dependency checker."""
        if checking_bundle.id in visited:
            return True
        visited.add(checking_bundle.id)

        # Get all bundle components
        for item in checking_bundle.bundle_items.all():
            if item.component_product_id == self.bundle_id:
                return True
            if item.component_product.product_type == "bundle":
                if self._check_circular(item.component_product, visited):
                    return True
        return False

    def get_component_price(self):
        """Get the price of this component (variant or product)."""
        if self.component_variant:
            return self.component_variant.get_effective_price()
        return self.component_product.effective_price

    def get_total_price(self):
        """Get total price for this component (price × quantity)."""
        component_price = self.get_component_price()
        return component_price.amount * self.quantity

    def check_stock_availability(self, warehouse=None):
        """Check if sufficient stock is available for this component."""
        if self.component_product.is_digital:
            return True  # Digital products have unlimited stock

        # Check stock
        stock_query = StockItem.objects.filter(product=self.component_product)

        if self.component_variant:
            stock_query = stock_query.filter(variant=self.component_variant)

        if warehouse:
            stock_query = stock_query.filter(warehouse=warehouse)

        total_stock = stock_query.aggregate(total=Sum(F("on_hand") - F("allocated")))["total"] or 0
        return total_stock >= self.quantity


class ProductDependency(models.Model):
    """
    Defines dependencies between products.
    'requires' = hard block — customer must own the required product (or have it in cart).
    'recommends' = soft suggestion — informational notice, never blocks.
    """

    DEPENDENCY_TYPE_CHOICES = [
        ("requires", _("Requires")),
        ("recommends", _("Recommends")),
    ]

    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="dependencies",
        verbose_name=_("Product"),
    )
    required_product = models.ForeignKey(
        "Product",
        on_delete=models.PROTECT,
        related_name="required_by",
        verbose_name=_("Required product"),
    )
    dependency_type = models.CharField(
        max_length=20,
        choices=DEPENDENCY_TYPE_CHOICES,
        default="requires",
        verbose_name=_("Dependency type"),
    )
    customer_message = models.CharField(
        max_length=300,
        blank=True,
        verbose_name=_("Customer message"),
        help_text=_("Custom message shown to the customer. Leave blank for automatic message."),
    )
    sort_order = models.IntegerField(default=0, verbose_name=_("Sort order"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("product", "required_product")]
        ordering = ["sort_order", "id"]
        verbose_name = _("product dependency")
        verbose_name_plural = _("product dependencies")

    def __str__(self):
        return (
            f"{self.product.name} {self.get_dependency_type_display()} {self.required_product.name}"
        )

    def clean(self):
        from django.core.exceptions import ValidationError

        if (
            self.product_id
            and self.required_product_id
            and self.product_id == self.required_product_id
        ):
            raise ValidationError(_("A product cannot depend on itself."))


class ProductPrice(models.Model):
    """
    Fixed prices for products in specific currencies.
    Allows merchants to set custom prices per currency instead of dynamic conversion.
    """

    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="currency_prices",
        verbose_name=_("Product"),
    )

    currency = models.CharField(
        max_length=3, verbose_name=_("Currency"), help_text=_("Currency code (e.g., 'USD', 'EUR')")
    )

    price = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency=None,  # Multi-currency support
        verbose_name=_("Price"),
        help_text=_("Price in this currency"),
    )

    sale_price = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency=None,
        null=True,
        blank=True,
        verbose_name=_("Sale Price"),
        help_text=_("Sale price in this currency (optional)"),
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
        help_text=_("Whether this price is active and should be used"),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Product Price")
        verbose_name_plural = _("Product Prices")
        unique_together = [["product", "currency"]]
        indexes = [
            models.Index(fields=["product", "currency", "is_active"]),
        ]

    def __str__(self):
        return f"{self.product.name} - {self.currency}: {self.price}"

    def get_effective_price(self):
        """Get effective price (sale price if exists, otherwise regular price)"""
        return self.sale_price if self.sale_price else self.price


class PriceCharmingRule(models.Model):
    """
    Price charming (psychological pricing) rules per currency.
    Examples: $19.99, €19.95, ¥1,980
    """

    currency = models.CharField(
        max_length=3,
        unique=True,
        verbose_name=_("Currency"),
        help_text=_("Currency code to apply this rule to"),
    )

    RULE_TYPE_CHOICES = [
        ("round_down", _("Round Down to nearest whole number (e.g., $19.50 → $19.00)")),
        ("round_up", _("Round Up to nearest whole number (e.g., $19.50 → $20.00)")),
        ("charm_99", _("Charm .99 ending (e.g., $20.50 → $19.99)")),
        ("charm_95", _("Charm .95 ending (e.g., $20.50 → $19.95)")),
        ("charm_90", _("Charm .90 ending (e.g., $20.50 → $19.90)")),
        ("round_nearest_5", _("Round to nearest 5 (e.g., $23 → $25)")),
        ("round_nearest_10", _("Round to nearest 10 (e.g., $23 → $20)")),
        ("round_nearest_100", _("Round to nearest 100 (e.g., $1,234 → $1,200)")),
        ("custom_ending", _("Custom ending (specify below)")),
    ]

    rule_type = models.CharField(
        max_length=30,
        choices=RULE_TYPE_CHOICES,
        verbose_name=_("Rule Type"),
        help_text=_("Type of price charming to apply"),
    )

    custom_ending = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Custom Ending"),
        help_text=_("For 'custom_ending' rule type (e.g., 0.88 for .88 endings)"),
    )

    apply_to_sale_prices = models.BooleanField(
        default=True,
        verbose_name=_("Apply to Sale Prices"),
        help_text=_("Whether to apply charming to sale prices (or only regular prices)"),
    )

    min_price_threshold = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Minimum Price Threshold"),
        help_text=_("Only apply charming to prices above this amount (0 = no minimum)"),
    )

    is_active = models.BooleanField(
        default=True, verbose_name=_("Active"), help_text=_("Whether this rule is active")
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Price Charming Rule")
        verbose_name_plural = _("Price Charming Rules")
        ordering = ["currency"]

    def __str__(self):
        return f"{self.currency}: {self.get_rule_type_display()}"

    def apply_charm(self, price: Decimal) -> Decimal:
        """
        Apply this charming rule to a price.

        Args:
            price: Price amount to apply charming to

        Returns:
            Charmed price amount
        """
        from decimal import ROUND_DOWN, ROUND_HALF_UP, ROUND_UP, Decimal

        # Check minimum threshold
        if price < self.min_price_threshold:
            return price

        if self.rule_type == "round_down":
            return price.quantize(Decimal("1"), rounding=ROUND_DOWN)

        elif self.rule_type == "round_up":
            return price.quantize(Decimal("1"), rounding=ROUND_UP)

        elif self.rule_type == "charm_99":
            # Round down to nearest integer, then subtract 0.01
            base = price.quantize(Decimal("1"), rounding=ROUND_DOWN)
            return base - Decimal("0.01")

        elif self.rule_type == "charm_95":
            # Round down to nearest integer, then subtract 0.05
            base = price.quantize(Decimal("1"), rounding=ROUND_DOWN)
            return base - Decimal("0.05")

        elif self.rule_type == "charm_90":
            # Round down to nearest integer, then subtract 0.10
            base = price.quantize(Decimal("1"), rounding=ROUND_DOWN)
            return base - Decimal("0.10")

        elif self.rule_type == "round_nearest_5":
            # Round to nearest 5
            return (price / 5).quantize(Decimal("1"), rounding=ROUND_HALF_UP) * 5

        elif self.rule_type == "round_nearest_10":
            # Round to nearest 10
            return (price / 10).quantize(Decimal("1"), rounding=ROUND_HALF_UP) * 10

        elif self.rule_type == "round_nearest_100":
            # Round to nearest 100
            return (price / 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP) * 100

        elif self.rule_type == "custom_ending" and self.custom_ending is not None:
            # Round down to nearest integer, then add custom ending
            base = price.quantize(Decimal("1"), rounding=ROUND_DOWN)
            # Handle case where custom ending might be >= 1.00
            if self.custom_ending < 1:
                return base + self.custom_ending
            else:
                # If custom ending is 1.00 or more, subtract from next integer
                return (base + Decimal("1")) - (Decimal("1") - (self.custom_ending % 1))

        # No charming applied
        return price


class ProductImage(models.Model):
    """Product images with display configuration"""

    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    media_asset = models.ForeignKey(
        "media_library.MediaAsset",
        on_delete=models.PROTECT,
        related_name="product_uses",
        null=True,  # Temporarily nullable for migration, will be non-null
        help_text="Media asset for this product image",
    )
    alt_text = models.CharField(
        max_length=255, blank=True, help_text="Override media asset alt text if needed"
    )
    is_primary = models.BooleanField(default=False)
    position = models.PositiveIntegerField(default=0)

    # Image display options
    show_in_gallery = models.BooleanField(default=True)
    show_in_listing = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["position", "id"]

    def __str__(self):
        return f"Image for {self.product.name}"

    @property
    def image_url(self):
        """Get the optimized display URL (WebP if available)"""
        return self.media_asset.get_display_url()

    @property
    def thumbnail_small(self):
        """Get small thumbnail (150x150) for admin/list views"""
        return self.media_asset.get_thumbnail("small")

    @property
    def thumbnail_medium(self):
        """Get medium thumbnail (300x300) for cards"""
        return self.media_asset.get_thumbnail("medium")

    def get_thumbnail(self, size_preset="medium"):
        """Get thumbnail for specific size"""
        return self.media_asset.get_thumbnail(size_preset)

    def save(self, *args, **kwargs):
        # Ensure only one primary image per product
        if self.is_primary:
            ProductImage.objects.filter(product=self.product, is_primary=True).exclude(
                pk=self.pk
            ).update(is_primary=False)
        super().save(*args, **kwargs)


class ProductAttribute(models.Model):
    """
    Reusable product attribute definitions (e.g., Size, Color, Material).
    Merchants can create custom attributes for their catalog.
    """

    name = models.CharField(
        max_length=100, unique=True, help_text="Attribute name (e.g., 'Size', 'Color', 'Material')"
    )
    slug = models.SlugField(max_length=100, unique=True, help_text="URL-safe version of name")
    type = models.CharField(
        max_length=20,
        choices=[
            ("select", "Dropdown Select"),
            ("color", "Color Swatch"),
            ("button", "Button Group"),
            ("radio", "Radio Buttons"),
        ],
        default="select",
        help_text="How this attribute displays on the frontend",
    )
    is_required = models.BooleanField(
        default=True, help_text="Must customers select this attribute?"
    )
    sort_order = models.IntegerField(default=0, help_text="Display order in variation selector")
    translations = models.JSONField(
        default=dict,
        blank=True,
        help_text="Translated attribute names: {'es': 'Tamaño', 'fr': 'Taille'}",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name = "Product Attribute"
        verbose_name_plural = "Product Attributes"

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    """
    Values for product attributes (e.g., 'Small', 'Red', 'Cotton').
    Each value belongs to a specific attribute.
    """

    attribute = models.ForeignKey(
        ProductAttribute,
        on_delete=models.CASCADE,
        related_name="values",
        help_text="Attribute this value belongs to",
    )
    value = models.CharField(
        max_length=100, help_text="Value label (e.g., 'Small', 'Red', 'Cotton')"
    )
    slug = models.SlugField(max_length=100, help_text="URL-safe version of value")
    color_hex = models.CharField(
        max_length=7, blank=True, help_text="Hex color code for color swatches (e.g., '#FF0000')"
    )
    sort_order = models.IntegerField(default=0, help_text="Display order within attribute")
    translations = models.JSONField(
        default=dict,
        blank=True,
        help_text="Translated value labels: {'es': 'Pequeño', 'fr': 'Petit'}",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["attribute", "sort_order", "value"]
        unique_together = [("attribute", "slug")]
        verbose_name = "Attribute Value"
        verbose_name_plural = "Attribute Values"

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"


class ProductAttributeAssignment(models.Model):
    """
    Assigns attributes to products and defines which values are available.
    E.g., T-Shirt product uses Size attribute with values: S, M, L, XL.
    """

    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="attribute_assignments",
        help_text="Product this attribute is assigned to",
    )
    attribute = models.ForeignKey(
        ProductAttribute,
        on_delete=models.CASCADE,
        related_name="product_assignments",
        help_text="Attribute assigned to product",
    )
    allowed_values = models.ManyToManyField(
        AttributeValue,
        related_name="product_assignments",
        help_text="Which values are available for this product",
    )
    sort_order = models.IntegerField(
        default=0, help_text="Display order for this attribute on product page"
    )

    class Meta:
        ordering = ["sort_order", "attribute__name"]
        unique_together = [("product", "attribute")]
        verbose_name = "Product Attribute Assignment"
        verbose_name_plural = "Product Attribute Assignments"

    def __str__(self):
        return f"{self.product.name} - {self.attribute.name}"


class ProductVariant(DesignMixin):
    """Product variants (size, color, etc.) with design options"""

    product = models.ForeignKey(Product, related_name="variants", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=100, unique=True)

    # Import tracking
    external_id = models.CharField(
        max_length=100,
        blank=True,
        db_index=True,
        help_text="Original variation ID from source platform",
    )
    imported_meta = models.JSONField(default=dict, blank=True, help_text="Metadata from import")

    # Variant-specific pricing
    price = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency="USD",
        null=True,
        blank=True,
        help_text="Leave blank to use main product price",
    )

    pricing_strategy = models.CharField(
        max_length=20,
        choices=[
            ("inherit", "Inherit from Product"),
            ("custom", "Custom Variant Price"),
        ],
        default="inherit",
        help_text="How to determine variant price",
    )

    # Physical attributes (optional overrides - fall back to product values)
    weight = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True,
        verbose_name="Weight",
        help_text="Variant weight in kg (leave blank to use product weight)",
    )

    length = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Length",
        help_text="Variant length in cm (leave blank to use product length)",
    )

    width = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Width",
        help_text="Variant width in cm (leave blank to use product width)",
    )

    height = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Height",
        help_text="Variant height in cm (leave blank to use product height)",
    )

    # Variant-specific identifier
    barcode = models.CharField(
        max_length=128,
        blank=True,
        verbose_name="Barcode",
        help_text="Variant-specific barcode (SKU barcode, leave blank to use product GTIN/UPC/EAN)",
    )

    # Shipping package preference
    preferred_shipping_package = models.ForeignKey(
        "shipping.ShippingPackage",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="variants",
        verbose_name="Preferred Shipping Package",
        help_text="Package to use for shipping this variant (leave blank to use product's preferred package)",
    )

    # Variant-specific inventory (DEPRECATED - use StockItem instead)
    # Will be migrated to StockItem in Stage 4
    quantity = models.IntegerField(
        default=0, help_text="DEPRECATED: Use StockItem model for multi-warehouse inventory"
    )

    # Structured attribute selection
    selected_attributes = models.ManyToManyField(
        AttributeValue,
        related_name="variants",
        blank=True,
        help_text="Attribute values for this variant (e.g., Size: Large, Color: Red)",
    )

    # Variant display
    image = models.ImageField(
        upload_to="products/variants/",
        blank=True,
        null=True,
        help_text="DEPRECATED: Use image_asset instead",
    )

    # Media library integration (NEW)
    image_asset = models.ForeignKey(
        "media_library.MediaAsset",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="product_variants",
        help_text="Variant-specific image from media library",
    )

    color_swatch = models.CharField(
        max_length=7, blank=True, help_text="Hex color code for color variants"
    )
    barcode = models.CharField(
        _("barcode"),
        max_length=50,
        blank=True,
        db_index=True,
        help_text=_("Variant-specific barcode for POS scanning"),
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.product.name} - {self.name}"

    def get_price(self):
        """DEPRECATED: Use get_effective_price() instead"""
        return self.price or self.product.price

    def get_effective_price(self):
        """
        Get variant price considering pricing strategy.
        Returns the appropriate price based on the pricing_strategy field.

        When the variant inherits pricing from the parent product, the
        parent's *effective* price (after any active sale) is used, so
        product-level sales apply to inherit-pricing variants too.
        """
        if self.pricing_strategy == "custom" and self.price:
            return self.price
        return self.product.get_effective_price()

    def get_effective_weight(self):
        """
        Get variant weight with fallback to product weight.

        Returns:
            Decimal: Weight in kg, or None if neither variant nor product has weight
        """
        return self.weight if self.weight is not None else self.product.weight

    def get_effective_length(self):
        """Get variant length with fallback to product length"""
        return self.length if self.length is not None else self.product.length

    def get_effective_width(self):
        """Get variant width with fallback to product width"""
        return self.width if self.width is not None else self.product.width

    def get_effective_height(self):
        """Get variant height with fallback to product height"""
        return self.height if self.height is not None else self.product.height

    def get_effective_dimensions(self):
        """
        Get variant dimensions with fallback to product dimensions.

        Returns:
            dict: Dictionary with 'length', 'width', 'height' keys (values in cm or None)
        """
        return {
            "length": self.get_effective_length(),
            "width": self.get_effective_width(),
            "height": self.get_effective_height(),
        }

    def get_effective_barcode(self):
        """
        Get variant barcode with fallback to product GTIN/UPC/EAN.

        Returns:
            str: Barcode identifier, or empty string if none available
        """
        if self.barcode:
            return self.barcode
        # Fall back to product barcodes in order of preference
        return self.product.gtin or self.product.upc or self.product.ean or ""

    def get_effective_shipping_package(self):
        """
        Get variant shipping package with fallback to product package.

        Returns:
            ShippingPackage instance or None
        """
        return self.preferred_shipping_package or self.product.preferred_shipping_package

    def get_shipping_dimensions(self):
        """
        Get dimensions for shipping calculation (package or product dimensions).

        Returns cascade priority:
        1. Variant's preferred package dimensions (if set)
        2. Product's preferred package dimensions (if set)
        3. Variant's physical dimensions (if set)
        4. Product's physical dimensions (fallback)

        Returns:
            dict: {'length': Decimal, 'width': Decimal, 'height': Decimal} in cm
        """
        package = self.get_effective_shipping_package()
        if package:
            return {
                "length": package.length,
                "width": package.width,
                "height": package.height,
            }
        # Fall back to product/variant dimensions
        return self.get_effective_dimensions()

    def get_shipping_weight(self):
        """
        Get weight for shipping calculation including package tare weight.

        Returns:
            Decimal: Total weight in kg (product weight + package tare weight if applicable)
        """
        product_weight = self.get_effective_weight() or Decimal("0.000")
        package = self.get_effective_shipping_package()
        if package:
            return product_weight + package.tare_weight
        return product_weight

    def get_stock_quantity(self, warehouse=None):
        """
        Get total stock across warehouses or for specific warehouse.

        Args:
            warehouse: Optional Warehouse instance to filter by

        Returns:
            Total stock quantity as integer
        """
        from django.db.models import Sum

        queryset = StockItem.objects.filter(product=self.product, variant=self)
        if warehouse:
            queryset = queryset.filter(warehouse=warehouse)
        result = queryset.aggregate(total=Sum("on_hand"))
        return result["total"] or 0

    def get_attribute_dict(self):
        """
        Get attributes as dict for display: {'Size': 'Large', 'Color': 'Red'}.
        Uses structured selected_attributes M2M, falls back to JSON attributes if needed.

        Returns:
            Dictionary mapping attribute names to values
        """
        # Use structured selected_attributes M2M
        if self.selected_attributes.exists():
            return {
                attr_value.attribute.name: attr_value.value
                for attr_value in self.selected_attributes.select_related("attribute").all()
            }

        # No attributes defined
        return {}

    @property
    def total_stock(self):
        """Total stock across all warehouses for this variant"""
        from django.db.models import Sum

        return self.stock_items.aggregate(total=Sum("on_hand"))["total"] or 0

    @property
    def available_stock(self):
        """Available stock (on_hand - allocated) across all warehouses"""
        from django.db.models import F, Sum

        return self.stock_items.aggregate(total=Sum(F("on_hand") - F("allocated")))["total"] or 0

    @property
    def allocated_stock(self):
        """Total allocated stock across all warehouses"""
        from django.db.models import Sum

        return self.stock_items.aggregate(total=Sum("allocated"))["total"] or 0

    @property
    def stock_status(self):
        """
        Get stock status for this variant.
        Returns: 'in_stock', 'low_stock', or 'out_of_stock'
        """
        available = self.available_stock

        if available <= 0:
            return "out_of_stock"
        elif available <= self.product.low_stock_threshold:
            return "low_stock"
        else:
            return "in_stock"

    @property
    def stock_status_display(self):
        """Human-readable stock status"""
        status_map = {
            "in_stock": "In Stock",
            "low_stock": "Low Stock",
            "out_of_stock": "Out of Stock",
        }
        return status_map.get(self.stock_status, "Unknown")

    @property
    def stock_status_badge(self):
        """HTML badge for stock status"""
        badge_map = {
            "in_stock": '<span class="stock-badge stock-badge-in-stock">🟢 In Stock</span>',
            "low_stock": '<span class="stock-badge stock-badge-low-stock">🟡 Low Stock</span>',
            "out_of_stock": '<span class="stock-badge stock-badge-out-of-stock">🔴 Out of Stock</span>',
        }
        return badge_map.get(self.stock_status, "")


class ProductVariantImage(models.Model):
    """
    Multiple images for product variants with display configuration.
    Similar to ProductImage but for variants, allowing merchants to show
    multiple images for each variant (e.g., different angles of a color variant).
    """

    variant = models.ForeignKey(
        ProductVariant,
        related_name="images",
        on_delete=models.CASCADE,
        help_text="Product variant this image belongs to",
    )
    media_asset = models.ForeignKey(
        "media_library.MediaAsset",
        on_delete=models.PROTECT,
        related_name="variant_uses",
        help_text="Media asset for this variant image",
    )
    alt_text = models.CharField(
        max_length=255, blank=True, help_text="Override media asset alt text if needed"
    )
    is_primary = models.BooleanField(
        default=False, help_text="Primary image shown first in variant gallery"
    )
    position = models.PositiveIntegerField(
        default=0, help_text="Display order (lower numbers shown first)"
    )

    # Image display options
    show_in_gallery = models.BooleanField(
        default=True, help_text="Show in product detail page gallery"
    )
    show_in_listing = models.BooleanField(default=True, help_text="Show in product listing pages")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["position", "id"]
        verbose_name = "Variant Image"
        verbose_name_plural = "Variant Images"

    def __str__(self):
        return f"Image for {self.variant.name}"

    @property
    def image_url(self):
        """Get the optimized display URL (WebP if available)"""
        return self.media_asset.get_display_url()

    @property
    def thumbnail_small(self):
        """Get small thumbnail (150x150) for admin/list views"""
        return self.media_asset.get_thumbnail("small")

    @property
    def thumbnail_medium(self):
        """Get medium thumbnail (300x300) for cards"""
        return self.media_asset.get_thumbnail("medium")

    def get_thumbnail(self, size_preset="medium"):
        """Get thumbnail for specific size"""
        return self.media_asset.get_thumbnail(size_preset)

    def save(self, *args, **kwargs):
        # Ensure only one primary image per variant
        if self.is_primary:
            ProductVariantImage.objects.filter(variant=self.variant, is_primary=True).exclude(
                pk=self.pk
            ).update(is_primary=False)
        super().save(*args, **kwargs)


class ProductReview(models.Model):
    """Customer product reviews"""

    product = models.ForeignKey(Product, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="product_reviews", on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=255)
    comment = models.TextField()

    # Import tracking
    external_id = models.CharField(
        max_length=100,
        blank=True,
        db_index=True,
        help_text="Original review ID from source platform",
    )
    migration_job = models.ForeignKey(
        "migration.MigrationJob",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="imported_reviews",
        help_text="Migration job that imported this review",
    )

    # Review metadata
    is_verified_purchase = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    helpful_count = models.PositiveIntegerField(default=0)

    # Review images
    images = models.JSONField(default=list, blank=True, help_text="URLs to review images")

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["product", "user"]

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username}"


class ProductTag(models.Model):
    """Lightweight product tag for organization and filtering."""

    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Product Tag")
        verbose_name_plural = _("Product Tags")
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify

            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Collection(DesignMixin):
    """Product collections with custom design"""

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)

    # Collection type
    COLLECTION_TYPES = [
        ("manual", "Manual Selection"),
        ("auto", "Automatic Rules"),
        ("featured", "Featured Products"),
        ("seasonal", "Seasonal"),
    ]

    collection_type = models.CharField(max_length=20, choices=COLLECTION_TYPES, default="manual")

    # Collection criteria for automatic collections
    auto_criteria = models.JSONField(
        default=dict, blank=True, help_text="Criteria for automatic product selection"
    )

    # Manual product selection
    products = models.ManyToManyField(Product, blank=True, related_name="collections")

    # Collection display
    image = models.ImageField(upload_to="collections/", blank=True, null=True)
    banner_image = models.ImageField(upload_to="collections/banners/", blank=True, null=True)

    # SEO
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(max_length=255, blank=True)

    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/collection/{self.slug}/"


class Promotion(models.Model):
    """Bulk sales and promotions for managing discounts across multiple products"""

    DISCOUNT_TYPE_CHOICES = [
        ("percentage_off", "Percentage Off"),
        ("amount_off", "Amount Off"),
        ("fixed_price", "Fixed Sale Price"),
    ]

    APPLY_TO_CHOICES = [
        ("all", "All Products"),
        ("categories", "Specific Categories"),
        ("brands", "Specific Brands"),
        ("collections", "Specific Collections"),
        ("products", "Specific Products"),
    ]

    # Basic information
    name = models.CharField(max_length=200, help_text="Internal name for this promotion")
    description = models.TextField(blank=True, help_text="Internal notes about this promotion")

    # Discount settings
    discount_type = models.CharField(
        max_length=20,
        choices=DISCOUNT_TYPE_CHOICES,
        default="percentage_off",
        verbose_name="Discount Type",
        help_text="Type of discount to apply",
    )
    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        verbose_name="Discount Value",
        help_text="Discount amount ($ or %) or fixed sale price",
    )

    # Scheduling
    start_date = models.DateTimeField(
        verbose_name="Start Date", help_text="When this promotion becomes active"
    )
    end_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="End Date",
        help_text="When this promotion ends (leave empty for no end date)",
    )

    # Product selection
    apply_to = models.CharField(
        max_length=20,
        choices=APPLY_TO_CHOICES,
        default="all",
        verbose_name="Apply To",
        help_text="What products this promotion applies to",
    )

    # Relationships for targeted promotions
    categories = models.ManyToManyField(
        Category,
        blank=True,
        related_name="promotions",
        help_text="Categories to include (when Apply To is 'Specific Categories')",
    )
    brands = models.ManyToManyField(
        Brand,
        blank=True,
        related_name="promotions",
        help_text="Brands to include (when Apply To is 'Specific Brands')",
    )
    collections = models.ManyToManyField(
        Collection,
        blank=True,
        related_name="promotions",
        help_text="Collections to include (when Apply To is 'Specific Collections')",
    )
    products = models.ManyToManyField(
        Product,
        blank=True,
        related_name="promotions",
        help_text="Specific products to include (when Apply To is 'Specific Products')",
    )

    # Priority and stacking
    priority = models.PositiveIntegerField(
        default=0, help_text="Higher priority promotions are applied first (0 is lowest)"
    )
    can_stack_with_product_sales = models.BooleanField(
        default=False,
        verbose_name="Stack with Product Sales",
        help_text="Allow this promotion to stack with product-level sales",
    )

    # Status
    is_active = models.BooleanField(default=True, help_text="Enable or disable this promotion")

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_promotions"
    )

    class Meta:
        ordering = ["-priority", "-start_date"]
        verbose_name = "Promotion"
        verbose_name_plural = "Promotions"
        indexes = [
            models.Index(fields=["is_active", "start_date", "end_date"]),
            models.Index(fields=["-priority"]),
        ]

    def __str__(self):
        return self.name

    @property
    def is_currently_active(self):
        """Check if promotion is active right now based on dates and status"""
        if not self.is_active:
            return False

        now = timezone.now()

        # Check start date
        if self.start_date and self.start_date > now:
            return False

        # Check end date
        return not (self.end_date and self.end_date < now)

    def get_eligible_products(self):
        """Get all products eligible for this promotion"""
        if self.apply_to == "all":
            return Product.objects.filter(status="published")

        elif self.apply_to == "categories":
            return Product.objects.filter(category__in=self.categories.all(), status="published")

        elif self.apply_to == "brands":
            return Product.objects.filter(brand__in=self.brands.all(), status="published")

        elif self.apply_to == "collections":
            # Products in any of the selected collections
            collection_products = Product.objects.none()
            for collection in self.collections.all():
                collection_products |= collection.products.all()
            return collection_products.filter(status="published").distinct()

        elif self.apply_to == "products":
            return self.products.filter(status="published")

        return Product.objects.none()

    def calculate_discount_for_product(self, product):
        """
        Calculate the discounted price for a product based on promotion settings.

        Args:
            product: Product instance

        Returns:
            Decimal: Discounted price amount, or None if not applicable
        """
        if not self.is_currently_active:
            return None

        # Handle stacking with product-level sales
        if product.is_on_sale:
            if not self.can_stack_with_product_sales:
                # Product already has an individual discount — skip it
                return None
            # Stack: apply promotion on top of the product's sale price
            base_price = product.calculate_sale_price()
        else:
            base_price = product.price.amount

        if self.discount_type == "fixed_price":
            return Decimal(str(self.discount_value))

        elif self.discount_type == "amount_off":
            discounted_price = base_price - Decimal(str(self.discount_value))
            return max(discounted_price, Decimal("0.01"))

        elif self.discount_type == "percentage_off":
            discount_amount = base_price * (Decimal(str(self.discount_value)) / Decimal("100"))
            discounted_price = base_price - discount_amount
            return max(discounted_price, Decimal("0.01"))

        return None

    def get_affected_products_count(self):
        """Get count of products affected by this promotion"""
        return self.get_eligible_products().count()

    def expires_in(self):
        """Get human-readable time until promotion ends"""
        if not self.end_date:
            return "No end date"

        now = timezone.now()

        if self.end_date < now:
            return "Expired"

        remaining = self.end_date - now

        if remaining.days > 0:
            return f"{remaining.days} day{'s' if remaining.days != 1 else ''}"
        elif remaining.seconds > 3600:
            hours = remaining.seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''}"
        elif remaining.seconds > 60:
            minutes = remaining.seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''}"
        else:
            return "Less than a minute"


# ============================================================================
# Multi-Location Inventory Models
# ============================================================================


class SalesRegion(models.Model):
    """
    Geographic market/region where products can be sold.
    Examples: Asia-Pacific, New Zealand, Singapore
    """

    name = models.CharField(
        _("region name"),
        max_length=100,
        unique=True,
        help_text=_("Display name for this sales region"),
    )
    code = models.CharField(
        _("region code"),
        max_length=10,
        unique=True,
        db_index=True,
        help_text=_('Unique code (e.g., "APAC", "NZ", "SG")'),
    )
    countries = models.JSONField(
        _("countries"),
        default=list,
        help_text=_('ISO country codes in this region (e.g., ["NZ", "FJ"])'),
    )
    default_currency = models.CharField(
        _("default currency"), max_length=3, help_text=_('ISO currency code (e.g., "NZD", "SGD")')
    )
    is_active = models.BooleanField(
        _("active"), default=True, help_text=_("Whether this region is currently active")
    )
    priority = models.IntegerField(
        _("priority"), default=0, help_text=_("Higher priority regions are checked first for stock")
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Sales Region")
        verbose_name_plural = _("Sales Regions")
        ordering = ["-priority", "name"]

    def __str__(self):
        return self.name


class Warehouse(models.Model):
    """
    Physical location where inventory is stored and from which orders are fulfilled.
    """

    name = models.CharField(
        _("warehouse name"),
        max_length=200,
        help_text=_('Display name (e.g., "Singapore Warehouse 1")'),
    )
    code = models.CharField(
        _("warehouse code"),
        max_length=50,
        unique=True,
        db_index=True,
        help_text=_('Unique code (e.g., "SG-W1", "AKL-W1")'),
    )
    region = models.ForeignKey(
        "SalesRegion",
        on_delete=models.PROTECT,
        related_name="warehouses",
        verbose_name=_("sales region"),
        help_text=_("The region this warehouse serves"),
    )

    # Optional link to shipping.Location for pickup points
    shipping_location = models.OneToOneField(
        "shipping.Location",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="warehouse",
        verbose_name=_("shipping location"),
        help_text=_("Link to pickup location if this warehouse supports customer pickup"),
    )

    # Address & Geocoding
    address_line1 = models.CharField(_("address line 1"), max_length=255)
    address_line2 = models.CharField(_("address line 2"), max_length=255, blank=True)
    city = models.CharField(_("city"), max_length=100)
    state_province = models.CharField(_("state/province"), max_length=100, blank=True)
    postal_code = models.CharField(_("postal code"), max_length=20)
    country = models.CharField(_("country"), max_length=2, help_text=_("ISO country code"))

    latitude = models.DecimalField(
        _("latitude"),
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        help_text=_("Latitude for distance calculations"),
    )
    longitude = models.DecimalField(
        _("longitude"),
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        help_text=_("Longitude for distance calculations"),
    )

    # Settings
    is_active = models.BooleanField(
        _("active"), default=True, help_text=_("Whether this warehouse is currently operational")
    )
    fulfillment_priority = models.IntegerField(
        _("fulfillment priority"),
        default=0,
        help_text=_("Higher priority warehouses are preferred for fulfillment"),
    )
    stock_buffer_percentage = models.IntegerField(
        _("stock buffer percentage"),
        default=10,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text=_("Reserve percentage of stock as safety buffer (0-100)"),
    )

    # Customer-facing display settings
    display_name = models.CharField(
        _("display name"),
        max_length=100,
        blank=True,
        help_text=_(
            'Customer-facing name (e.g., "Ships from Australia"). Leave blank to use warehouse name.'
        ),
    )
    show_on_frontend = models.BooleanField(
        _("show on frontend"),
        default=False,
        help_text=_('Display this warehouse location to customers (e.g., "Ships from X")'),
    )

    # Contact Info
    contact_name = models.CharField(_("contact name"), max_length=200, blank=True)
    contact_email = models.EmailField(_("contact email"), blank=True)
    contact_phone = models.CharField(_("contact phone"), max_length=50, blank=True)

    # POS / Retail Location
    is_retail_location = models.BooleanField(
        _("retail location"),
        default=False,
        help_text=_("This warehouse is a physical retail store with POS terminals"),
    )
    pos_display_name = models.CharField(
        _("POS display name"),
        max_length=200,
        blank=True,
        help_text=_('Short name shown in POS interface, e.g. "Downtown Store"'),
    )
    store_group = models.ForeignKey(
        "pos_app.StoreGroup",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="warehouses",
        verbose_name=_("store group"),
        help_text=_("POS store group for settings inheritance (currency, language, etc.)"),
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Warehouse")
        verbose_name_plural = _("Warehouses")
        ordering = ["-fulfillment_priority", "name"]
        indexes = [
            models.Index(fields=["region", "is_active"]),
            models.Index(fields=["code"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.code})"

    @property
    def full_address(self):
        """Return formatted full address"""
        parts = [
            self.address_line1,
            self.address_line2,
            self.city,
            self.state_province,
            self.postal_code,
        ]
        return ", ".join(filter(None, parts))

    def get_effective_stock_buffer(self, quantity):
        """Calculate actual buffer quantity from percentage"""
        return int(quantity * (self.stock_buffer_percentage / 100))

    def get_display_name(self):
        """
        Get customer-facing display name for frontend.
        Returns None if warehouse shouldn't be shown to customers.
        """
        if not self.show_on_frontend:
            return None
        return self.display_name or self.name


class StockItem(models.Model):
    """
    Inventory record linking a product to a warehouse with quantity tracking.
    Tracks both on-hand stock and allocated (reserved) stock.
    """

    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="stock_items", verbose_name=_("product")
    )
    warehouse = models.ForeignKey(
        "Warehouse",
        on_delete=models.PROTECT,
        related_name="stock_items",
        verbose_name=_("warehouse"),
    )
    variant = models.ForeignKey(
        "ProductVariant",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="stock_items",
        verbose_name=_("variant"),
        help_text=_("Variant this stock is for (null for simple products)"),
    )

    # Stock Quantities
    on_hand = models.IntegerField(
        _("on hand"),
        default=0,
        validators=[MinValueValidator(0)],
        help_text=_("Physical stock in warehouse"),
    )
    allocated = models.IntegerField(
        _("allocated"),
        default=0,
        validators=[MinValueValidator(0)],
        help_text=_("Stock reserved for orders (not yet fulfilled)"),
    )

    # Low Stock Alert
    low_stock_threshold = models.IntegerField(
        _("low stock threshold"),
        default=0,
        validators=[MinValueValidator(0)],
        help_text=_("Alert when available stock drops below this (0 = use product default)"),
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Stock Item")
        verbose_name_plural = _("Stock Items")
        unique_together = [("product", "warehouse", "variant")]
        indexes = [
            models.Index(fields=["product", "warehouse", "variant"]),
            models.Index(fields=["warehouse", "on_hand"]),
        ]

    def __str__(self):
        return f"{self.product} @ {self.warehouse}: {self.available}/{self.on_hand}"

    @property
    def available(self):
        """Stock available for sale (on_hand - allocated)"""
        return max(0, self.on_hand - self.allocated)

    @property
    def effective_low_stock_threshold(self):
        """Get threshold, falling back to product default"""
        return self.low_stock_threshold or self.product.low_stock_threshold

    @property
    def is_low_stock(self):
        """Check if available stock is below threshold"""
        return self.available <= self.effective_low_stock_threshold

    def allocate(self, quantity):
        """
        Reserve stock for an order (does not reduce on_hand).
        Raises ValueError if insufficient available stock.
        """
        from django.db.models import F

        if quantity > self.available:
            raise ValueError(f"Cannot allocate {quantity} units. Only {self.available} available.")
        self.allocated = F("allocated") + quantity
        self.save(update_fields=["allocated"])
        self.refresh_from_db(fields=["allocated"])

    def deallocate(self, quantity):
        """Release reserved stock (e.g., on order cancellation)"""
        from django.db.models import F

        self.allocated = F("allocated") - quantity
        self.save(update_fields=["allocated"])
        self.refresh_from_db(fields=["allocated"])

    def fulfill(self, quantity):
        """
        Fulfill allocated stock (reduces both allocated and on_hand).
        Raises ValueError if insufficient allocated stock.
        """
        from django.db.models import F

        if quantity > self.allocated:
            raise ValueError(f"Cannot fulfill {quantity} units. Only {self.allocated} allocated.")
        self.allocated = F("allocated") - quantity
        self.on_hand = F("on_hand") - quantity
        self.save(update_fields=["allocated", "on_hand"])
        self.refresh_from_db(fields=["allocated", "on_hand"])

    def adjust_stock(self, quantity, reason=""):
        """
        Adjust on_hand stock (for receiving shipments, corrections, etc.).
        Creates StockMovement record for audit trail.
        """
        from django.db.models import F

        old_quantity = self.on_hand
        self.on_hand = F("on_hand") + quantity
        self.save(update_fields=["on_hand"])
        self.refresh_from_db(fields=["on_hand"])

        # Create movement record
        StockMovement.objects.create(
            stock_item=self,
            movement_type="adjustment",
            quantity=quantity,
            previous_quantity=old_quantity,
            new_quantity=self.on_hand,
            reason=reason,
        )


class StockMovement(models.Model):
    """
    Immutable audit trail of all stock changes.
    Tracks adjustments, allocations, fulfillments, and returns.
    """

    MOVEMENT_TYPES = [
        ("adjustment", _("Stock Adjustment")),
        ("allocation", _("Order Allocation")),
        ("fulfillment", _("Order Fulfillment")),
        ("return", _("Customer Return")),
        ("transfer", _("Warehouse Transfer")),
        ("damage", _("Damaged/Lost")),
        ("recount", _("Physical Recount")),
    ]

    stock_item = models.ForeignKey(
        "StockItem",
        on_delete=models.CASCADE,
        related_name="movements",
        verbose_name=_("stock item"),
    )
    movement_type = models.CharField(_("movement type"), max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField(
        _("quantity"), help_text=_("Change in quantity (positive or negative)")
    )
    previous_quantity = models.IntegerField(
        _("previous quantity"), help_text=_("Stock level before this movement")
    )
    new_quantity = models.IntegerField(
        _("new quantity"), help_text=_("Stock level after this movement")
    )
    reason = models.TextField(_("reason"), blank=True, help_text=_("Explanation for this movement"))

    # Optional references
    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="stock_movements",
        verbose_name=_("order"),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="stock_movements",
        verbose_name=_("user"),
    )

    # Idempotency key for offline/retry deduplication
    reference_key = models.CharField(
        _("reference key"),
        max_length=64,
        null=True,
        blank=True,
        db_index=True,
        help_text=_("Idempotency key for deduplication of offline/retry operations"),
    )

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Stock Movement")
        verbose_name_plural = _("Stock Movements")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["stock_item", "-created_at"]),
            models.Index(fields=["movement_type", "-created_at"]),
            models.Index(fields=["order"]),
        ]

    def __str__(self):
        return f"{self.movement_type}: {self.quantity:+d} @ {self.stock_item.warehouse}"


class StockReservation(models.Model):
    """
    Temporary stock hold tied to a cart item.

    When a product is added to a cart (POS or web), stock is reserved by
    incrementing StockItem.allocated and creating a StockReservation record.
    This prevents overselling between add-to-cart and checkout.

    At checkout, the reservation is converted to an order allocation.
    If the reservation expires (customer abandons cart), a Celery task
    releases the hold by decrementing allocated.
    """

    CHANNEL_CHOICES = [
        ("web", _("Web")),
        ("pos", _("POS")),
    ]

    stock_item = models.ForeignKey(
        "StockItem",
        on_delete=models.CASCADE,
        related_name="reservations",
        verbose_name=_("stock item"),
    )
    cart_item = models.ForeignKey(
        "cart.CartItem",
        on_delete=models.CASCADE,
        related_name="stock_reservations",
        verbose_name=_("cart item"),
    )
    quantity = models.PositiveIntegerField(_("quantity"), help_text=_("Number of units reserved"))
    channel = models.CharField(_("channel"), max_length=10, choices=CHANNEL_CHOICES, default="web")
    warehouse = models.ForeignKey(
        "Warehouse",
        on_delete=models.CASCADE,
        related_name="stock_reservations",
        verbose_name=_("warehouse"),
        help_text=_("Warehouse the reservation is held at"),
    )
    expires_at = models.DateTimeField(
        _("expires at"),
        db_index=True,
        help_text=_("When this reservation expires and stock is released"),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Stock Reservation")
        verbose_name_plural = _("Stock Reservations")
        unique_together = [("stock_item", "cart_item")]
        indexes = [
            models.Index(fields=["expires_at"]),
            models.Index(fields=["cart_item"]),
        ]

    def __str__(self):
        return (
            f"Reservation: {self.quantity}x "
            f"{self.stock_item.product} @ {self.warehouse} "
            f"(expires {self.expires_at})"
        )


class ProductRegionVisibility(models.Model):
    """
    Controls which products are visible in which regions.
    If no records exist for a product, it's visible in all regions.
    """

    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="region_visibility",
        verbose_name=_("product"),
    )
    region = models.ForeignKey(
        "SalesRegion",
        on_delete=models.CASCADE,
        related_name="visible_products",
        verbose_name=_("region"),
    )
    is_visible = models.BooleanField(
        _("visible"), default=True, help_text=_("Whether product is visible in this region")
    )

    class Meta:
        verbose_name = _("Product Region Visibility")
        verbose_name_plural = _("Product Region Visibility")
        unique_together = [("product", "region")]
        indexes = [
            models.Index(fields=["region", "is_visible"]),
        ]

    def __str__(self):
        return f"{self.product} in {self.region}: {'Visible' if self.is_visible else 'Hidden'}"


# ============================================================================
# Digital Products Models
# ============================================================================


class DigitalAsset(models.Model):
    """
    Digital files for downloadable products (eBooks, software, courses, etc.).
    Files are stored in MinIO with secure signed URL delivery.
    """

    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="digital_assets",
        verbose_name=_("Product"),
        help_text=_("Product this digital asset belongs to"),
    )

    # File storage (MinIO)
    file = models.FileField(
        upload_to="digital-assets/%Y/%m/",
        storage=None,  # Will be set via storage class
        verbose_name=_("File"),
        help_text=_("Digital file stored in MinIO (S3-compatible storage)"),
    )

    # File metadata
    filename = models.CharField(
        max_length=255,
        verbose_name=_("Original Filename"),
        help_text=_("Original filename when uploaded"),
    )
    file_size = models.BigIntegerField(
        verbose_name=_("File Size (bytes)"), help_text=_("File size in bytes")
    )
    file_type = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("File Type"),
        help_text=_("MIME type (e.g., application/pdf, application/zip)"),
    )
    file_hash = models.CharField(
        max_length=64,
        blank=True,
        verbose_name=_("File Hash (SHA-256)"),
        help_text=_("SHA-256 hash for file integrity verification"),
    )

    # Version management
    version = models.CharField(
        max_length=50,
        default="1.0",
        verbose_name=_("Version"),
        help_text=_("Version number (e.g., 1.0, 2.1.3)"),
    )
    changelog = models.TextField(
        blank=True, verbose_name=_("Changelog"), help_text=_("What changed in this version")
    )

    # Access control
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
        help_text=_("Whether this asset is available for download"),
    )
    download_limit = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name=_("Download Limit"),
        help_text=_("Max downloads per purchase (null = unlimited)"),
    )
    expiration_days = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
        verbose_name=_("Download Link Expiration (days)"),
        help_text=_("Days before download link expires after purchase (null = never)"),
    )

    # License key integration
    requires_license = models.BooleanField(
        default=False,
        verbose_name=_("Requires License Key"),
        help_text=_("Whether this asset requires a license key for activation"),
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_digital_assets",
        verbose_name=_("Created By"),
    )

    class Meta:
        verbose_name = _("Digital Asset")
        verbose_name_plural = _("Digital Assets")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["product", "is_active"]),
            models.Index(fields=["version"]),
        ]

    def __str__(self):
        return f"{self.product.name} - {self.filename} (v{self.version})"

    def save(self, *args, **kwargs):
        """Override save to set custom storage backend"""
        from core.storage import MinIODigitalAssetsStorage

        # Set storage backend for file field
        if (
            not self.file.field.storage
            or self.file.field.storage.__class__.__name__ != "MinIODigitalAssetsStorage"
        ):
            self.file.field.storage = MinIODigitalAssetsStorage()

        # Extract filename if not set
        if not self.filename and self.file:
            import os

            self.filename = os.path.basename(self.file.name)

        # Extract file size if not set
        if not self.file_size and self.file:
            self.file_size = self.file.size

        super().save(*args, **kwargs)

    def get_file_size_display(self):
        """
        Get human-readable file size.

        Returns:
            str: Formatted file size (e.g., '10.5 MB', '1.2 GB')
        """
        size = self.file_size
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"

    def generate_download_url(self, expiration_seconds=3600):
        """
        Generate a time-limited signed URL for secure downloads.

        Args:
            expiration_seconds: URL validity in seconds (default: 1 hour)

        Returns:
            str: Signed download URL
        """
        from core.storage import MinIODigitalAssetsStorage

        # Use MinIO storage for signed URLs
        storage = MinIODigitalAssetsStorage()

        # Generate signed URL with expiration
        url = storage.url(
            self.file.name,
            parameters={"ResponseContentDisposition": f'attachment; filename="{self.filename}"'},
            expire=expiration_seconds,
        )

        return url

    def calculate_file_hash(self):
        """
        Calculate SHA-256 hash of file for integrity verification.

        Returns:
            str: Hexadecimal hash string
        """
        import hashlib

        hash_sha256 = hashlib.sha256()

        # Read file in chunks to handle large files
        self.file.seek(0)
        for chunk in iter(lambda: self.file.read(4096), b""):
            hash_sha256.update(chunk)

        self.file.seek(0)  # Reset file pointer
        return hash_sha256.hexdigest()

    def get_download_count(self):
        """
        Get total number of downloads for this asset.

        Returns:
            int: Total download count
        """
        return self.downloads.count()

    def is_download_limit_exceeded(self, order_item):
        """
        Check if download limit has been exceeded for a specific purchase.

        Args:
            order_item: OrderItem instance representing the purchase

        Returns:
            bool: True if limit exceeded, False otherwise
        """
        if not self.download_limit:
            return False  # Unlimited downloads

        download_count = self.downloads.filter(order_item=order_item).count()
        return download_count >= self.download_limit

    def is_download_expired(self, purchase_date):
        """
        Check if download access has expired for a purchase.

        Args:
            purchase_date: datetime when product was purchased

        Returns:
            bool: True if expired, False otherwise
        """
        if not self.expiration_days:
            return False  # Never expires

        from datetime import timedelta

        expiration_date = purchase_date + timedelta(days=self.expiration_days)
        return timezone.now() > expiration_date


class DigitalDownload(models.Model):
    """
    Tracks every download of digital assets for analytics and limit enforcement.
    Provides audit trail of who downloaded what and when.
    """

    digital_asset = models.ForeignKey(
        "DigitalAsset",
        on_delete=models.CASCADE,
        related_name="downloads",
        verbose_name=_("Digital Asset"),
        help_text=_("Asset that was downloaded"),
    )
    order_item = models.ForeignKey(
        "orders.OrderItem",
        on_delete=models.CASCADE,
        related_name="digital_downloads",
        verbose_name=_("Order Item"),
        help_text=_("Purchase that grants download access"),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="digital_downloads",
        verbose_name=_("User"),
        help_text=_("User who downloaded the file"),
    )

    # Download details
    downloaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Downloaded At"),
        help_text=_("When the download occurred"),
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_("IP Address"),
        help_text=_("IP address of the downloader"),
    )
    user_agent = models.TextField(
        blank=True, verbose_name=_("User Agent"), help_text=_("Browser/client user agent string")
    )

    # Download status
    STATUS_CHOICES = [
        ("initiated", _("Download Initiated")),
        ("completed", _("Download Completed")),
        ("failed", _("Download Failed")),
        ("expired", _("Link Expired")),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="initiated",
        verbose_name=_("Status"),
        help_text=_("Status of this download attempt"),
    )
    error_message = models.TextField(
        blank=True, verbose_name=_("Error Message"), help_text=_("Error details if download failed")
    )

    # Analytics
    file_version = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("File Version"),
        help_text=_("Version of file at time of download"),
    )
    download_duration_seconds = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_("Download Duration (seconds)"),
        help_text=_("How long the download took"),
    )

    class Meta:
        verbose_name = _("Digital Download")
        verbose_name_plural = _("Digital Downloads")
        ordering = ["-downloaded_at"]
        indexes = [
            models.Index(fields=["digital_asset", "-downloaded_at"]),
            models.Index(fields=["order_item", "-downloaded_at"]),
            models.Index(fields=["user", "-downloaded_at"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.digital_asset.filename} - {self.user or 'Anonymous'} @ {self.downloaded_at}"

    def save(self, *args, **kwargs):
        """Auto-populate file version on save"""
        if not self.file_version:
            self.file_version = self.digital_asset.version
        super().save(*args, **kwargs)

    def mark_completed(self, duration_seconds=None):
        """Mark download as successfully completed"""
        self.status = "completed"
        if duration_seconds:
            self.download_duration_seconds = duration_seconds
        self.save(update_fields=["status", "download_duration_seconds"])

    def mark_failed(self, error_message):
        """Mark download as failed with error message"""
        self.status = "failed"
        self.error_message = error_message
        self.save(update_fields=["status", "error_message"])

    def mark_expired(self):
        """Mark download link as expired"""
        self.status = "expired"
        self.save(update_fields=["status"])

    @classmethod
    def create_download_record(
        cls, digital_asset, order_item, user=None, ip_address=None, user_agent=""
    ):
        """
        Factory method to create a new download record.

        Args:
            digital_asset: DigitalAsset instance
            order_item: OrderItem instance
            user: User instance (optional)
            ip_address: IP address string (optional)
            user_agent: User agent string (optional)

        Returns:
            DigitalDownload instance
        """
        return cls.objects.create(
            digital_asset=digital_asset,
            order_item=order_item,
            user=user,
            ip_address=ip_address,
            user_agent=user_agent,
            file_version=digital_asset.version,
        )

    def get_download_url(self, expiration_seconds=3600):
        """
        Generate download URL for this specific download record.

        Args:
            expiration_seconds: URL validity in seconds

        Returns:
            str: Signed download URL
        """
        return self.digital_asset.generate_download_url(expiration_seconds)


class LicenseKey(models.Model):
    """
    Software license keys for digital products requiring activation.
    Supports device limits, expiration, and activation tracking.
    """

    # Pool association (for pre-generated bulk licenses)
    license_pool = models.ForeignKey(
        "LicensePool",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pool_keys",
        verbose_name=_("License Pool"),
        help_text=_("License pool this key belongs to (if pre-generated)"),
    )

    digital_asset = models.ForeignKey(
        "DigitalAsset",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="license_keys",
        verbose_name=_("Digital Asset"),
        help_text=_("Digital asset this license is for"),
    )
    order_item = models.ForeignKey(
        "orders.OrderItem",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="license_keys",
        verbose_name=_("Order Item"),
        help_text=_("Purchase that generated this license"),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="license_keys",
        verbose_name=_("User"),
        help_text=_("User who owns this license"),
    )

    # License key
    KEY_TYPE_CHOICES = [
        ("perpetual", _("Perpetual")),
        ("subscription", _("Subscription")),
        ("trial", _("Trial")),
        ("nfr", _("Not For Resale")),
        ("educational", _("Educational")),
        ("standard", _("Standard")),
    ]

    key = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name=_("License Key"),
        help_text=_("Unique activation key (auto-generated)"),
    )
    key_type = models.CharField(
        max_length=50,
        choices=KEY_TYPE_CHOICES,
        default="standard",
        verbose_name=_("Key Type"),
        help_text=_("Type of license (standard, professional, enterprise, etc.)"),
    )

    # Activation limits
    max_activations = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name=_("Max Activations"),
        help_text=_("Maximum number of devices/installations allowed"),
    )
    current_activations = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name=_("Current Activations"),
        help_text=_("Number of active installations"),
    )

    # Status
    STATUS_CHOICES = [
        ("active", _("Active")),
        ("suspended", _("Suspended")),
        ("expired", _("Expired")),
        ("revoked", _("Revoked")),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active",
        db_index=True,
        verbose_name=_("Status"),
        help_text=_("Current status of this license"),
    )

    # Expiration
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Expires At"),
        help_text=_("When this license expires (null = never)"),
    )
    is_lifetime = models.BooleanField(
        default=True,
        verbose_name=_("Lifetime License"),
        help_text=_("Whether this is a lifetime license"),
    )

    # Metadata
    issued_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Issued At"),
        help_text=_("When this license was generated"),
    )
    first_activated_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("First Activated At"),
        help_text=_("When this license was first activated"),
    )
    last_activated_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Last Activated At"),
        help_text=_("Most recent activation timestamp"),
    )

    # Admin notes
    notes = models.TextField(
        blank=True, verbose_name=_("Admin Notes"), help_text=_("Internal notes about this license")
    )

    class Meta:
        verbose_name = _("License Key")
        verbose_name_plural = _("License Keys")
        ordering = ["-issued_at"]
        indexes = [
            models.Index(fields=["key"]),
            models.Index(fields=["digital_asset", "order_item"]),
            models.Index(fields=["user", "-issued_at"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.digital_asset.product.name} - {self.key[:20]}..."

    def save(self, *args, **kwargs):
        """Auto-generate license key if not set"""
        if not self.key:
            self.key = self.generate_license_key()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_license_key(length=25, separator="-", chunk_size=5):
        """
        Generate a random license key.

        Args:
            length: Total character length (default: 25)
            separator: Separator character (default: '-')
            chunk_size: Characters per chunk (default: 5)

        Returns:
            str: Generated license key (e.g., 'ABCDE-12345-FGHIJ-67890-KLMNO')
        """
        import secrets

        # Use alphanumeric characters excluding similar-looking ones (0/O, 1/I, etc.)
        alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"

        # Generate random key
        key_chars = "".join(secrets.choice(alphabet) for _ in range(length))

        # Split into chunks with separator
        chunks = [key_chars[i : i + chunk_size] for i in range(0, len(key_chars), chunk_size)]
        return separator.join(chunks)

    @property
    def is_expired(self):
        """Check if license has expired"""
        if self.is_lifetime:
            return False
        if not self.expires_at:
            return False
        return timezone.now() > self.expires_at

    @property
    def is_valid(self):
        """Check if license is valid and can be activated"""
        if self.status != "active":
            return False
        return not self.is_expired

    @property
    def activations_remaining(self):
        """Get number of activations remaining"""
        return max(0, self.max_activations - self.current_activations)

    def can_activate(self):
        """
        Check if license can be activated on a new device.

        Returns:
            tuple: (bool, str) - (can_activate, reason_if_not)
        """
        if not self.is_valid:
            return False, "License is not valid"

        if self.current_activations >= self.max_activations:
            return False, f"Maximum activations ({self.max_activations}) reached"

        return True, "OK"

    def activate(self, device_identifier, device_name="", ip_address=None):
        """
        Activate license on a new device.

        Args:
            device_identifier: Unique device ID (hardware ID, MAC address, etc.)
            device_name: Human-readable device name (optional)
            ip_address: IP address of activation request (optional)

        Returns:
            LicenseActivation: Created activation record

        Raises:
            ValueError: If license cannot be activated
        """
        can_activate, reason = self.can_activate()
        if not can_activate:
            raise ValueError(f"Cannot activate license: {reason}")

        # Check if device is already activated
        existing = self.activations.filter(
            device_identifier=device_identifier, is_active=True
        ).first()

        if existing:
            # Update last seen timestamp
            existing.last_seen_at = timezone.now()
            existing.save(update_fields=["last_seen_at"])
            return existing

        # Create new activation
        activation = LicenseActivation.objects.create(
            license_key=self,
            device_identifier=device_identifier,
            device_name=device_name,
            ip_address=ip_address,
            is_active=True,
        )

        # Update activation count
        self.current_activations = self.activations.filter(is_active=True).count()
        self.last_activated_at = timezone.now()

        if not self.first_activated_at:
            self.first_activated_at = self.last_activated_at

        self.save(update_fields=["current_activations", "first_activated_at", "last_activated_at"])

        return activation

    def deactivate(self, device_identifier):
        """
        Deactivate license on a specific device.

        Args:
            device_identifier: Device ID to deactivate

        Returns:
            bool: True if deactivated, False if not found
        """
        activation = self.activations.filter(
            device_identifier=device_identifier, is_active=True
        ).first()

        if not activation:
            return False

        activation.is_active = False
        activation.deactivated_at = timezone.now()
        activation.save(update_fields=["is_active", "deactivated_at"])

        # Update activation count
        self.current_activations = self.activations.filter(is_active=True).count()
        self.save(update_fields=["current_activations"])

        return True

    def deactivate_all(self):
        """Deactivate license on all devices"""
        self.activations.filter(is_active=True).update(
            is_active=False, deactivated_at=timezone.now()
        )
        self.current_activations = 0
        self.save(update_fields=["current_activations"])

    def suspend(self, reason=""):
        """Suspend license (can be reactivated)"""
        self.status = "suspended"
        if reason:
            self.notes = f"{self.notes}\n[{timezone.now()}] Suspended: {reason}".strip()
        self.save(update_fields=["status", "notes"])

    def revoke(self, reason=""):
        """Revoke license permanently"""
        self.status = "revoked"
        self.deactivate_all()
        if reason:
            self.notes = f"{self.notes}\n[{timezone.now()}] Revoked: {reason}".strip()
        self.save(update_fields=["status", "notes"])

    def restore(self):
        """Restore suspended/revoked license to active status"""
        if self.is_expired:
            raise ValueError("Cannot restore expired license")
        self.status = "active"
        self.notes = f"{self.notes}\n[{timezone.now()}] Restored to active".strip()
        self.save(update_fields=["status", "notes"])

    def extend_expiration(self, days):
        """
        Extend license expiration by specified days.

        Args:
            days: Number of days to extend
        """
        from datetime import timedelta

        if self.is_lifetime:
            # Convert to time-limited license
            self.is_lifetime = False
            self.expires_at = timezone.now() + timedelta(days=days)
        elif self.expires_at:
            self.expires_at += timedelta(days=days)
        else:
            self.expires_at = timezone.now() + timedelta(days=days)
            self.is_lifetime = False

        self.save(update_fields=["is_lifetime", "expires_at"])

    def verify(self, device_identifier):
        """
        Verify license is valid for a specific device.

        Args:
            device_identifier: Device ID to verify

        Returns:
            tuple: (bool, str, dict) - (is_valid, message, metadata)
        """
        if not self.is_valid:
            return False, f"License is {self.status}", {}

        # Check if device is activated
        activation = self.activations.filter(
            device_identifier=device_identifier, is_active=True
        ).first()

        if not activation:
            return False, "Device not activated", {}

        # Update last seen
        activation.last_seen_at = timezone.now()
        activation.save(update_fields=["last_seen_at"])

        metadata = {
            "key_type": self.key_type,
            "max_activations": self.max_activations,
            "current_activations": self.current_activations,
            "is_lifetime": self.is_lifetime,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "product": {
                "name": self.digital_asset.product.name,
                "version": self.digital_asset.version,
            },
        }

        return True, "License valid", metadata


class LicenseActivation(models.Model):
    """
    Tracks individual device activations for license keys.
    Records which devices have activated a license and when.
    """

    license_key = models.ForeignKey(
        "LicenseKey",
        on_delete=models.CASCADE,
        related_name="activations",
        verbose_name=_("License Key"),
        help_text=_("License that was activated"),
    )

    # Device identification
    device_identifier = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name=_("Device Identifier"),
        help_text=_("Unique device ID (hardware ID, MAC address, UUID, etc.)"),
    )
    device_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Device Name"),
        help_text=_('Human-readable device name (e.g., "John\'s MacBook Pro")'),
    )
    device_info = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Device Information"),
        help_text=_("Additional device details (OS, version, hardware specs, etc.)"),
    )

    # Activation status
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name=_("Active"),
        help_text=_("Whether this activation is currently active"),
    )

    # Timestamps
    activated_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Activated At"),
        help_text=_("When this device was activated"),
    )
    deactivated_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Deactivated At"),
        help_text=_("When this device was deactivated"),
    )
    last_seen_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Last Seen At"),
        help_text=_("Last time this device validated the license"),
    )

    # Network info
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_("IP Address"),
        help_text=_("IP address at time of activation"),
    )
    location = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Location"),
        help_text=_("Geographic location (city, country) if available"),
    )

    class Meta:
        verbose_name = _("License Activation")
        verbose_name_plural = _("License Activations")
        ordering = ["-activated_at"]
        unique_together = [("license_key", "device_identifier")]
        indexes = [
            models.Index(fields=["license_key", "is_active"]),
            models.Index(fields=["device_identifier"]),
            models.Index(fields=["-activated_at"]),
        ]

    def __str__(self):
        status = "Active" if self.is_active else "Deactivated"
        device = self.device_name or self.device_identifier[:20]
        return f"{device} - {status}"

    @property
    def is_recently_active(self, hours=24):
        """
        Check if device has validated license recently.

        Args:
            hours: Number of hours to consider as "recent"

        Returns:
            bool: True if device validated within the time window
        """
        if not self.is_active:
            return False

        from datetime import timedelta

        cutoff = timezone.now() - timedelta(hours=hours)
        return self.last_seen_at >= cutoff

    @property
    def activation_duration(self):
        """
        Get how long this device has been/was activated.

        Returns:
            timedelta: Duration of activation
        """
        end_time = self.deactivated_at if self.deactivated_at else timezone.now()
        return end_time - self.activated_at

    def deactivate(self, reason=""):
        """
        Deactivate this specific activation.

        Args:
            reason: Optional reason for deactivation
        """
        if not self.is_active:
            return

        self.is_active = False
        self.deactivated_at = timezone.now()
        self.save(update_fields=["is_active", "deactivated_at"])

        # Update license key activation count
        self.license_key.current_activations = self.license_key.activations.filter(
            is_active=True
        ).count()
        self.license_key.save(update_fields=["current_activations"])

    def update_device_info(self, **kwargs):
        """
        Update device information.

        Args:
            **kwargs: Device info fields to update (os, version, etc.)
        """
        self.device_info.update(kwargs)
        self.save(update_fields=["device_info"])

    def heartbeat(self):
        """
        Update last_seen_at timestamp (automatic via auto_now).
        Call this method during license validation to track activity.
        """
        self.save(update_fields=["last_seen_at"])


class LicenseKeyTemplate(models.Model):
    """Template for generating license keys with custom formats"""

    # Basic Info
    name = models.CharField(
        max_length=255, help_text=_("Template name (e.g., 'Standard App License')")
    )
    description = models.TextField(
        blank=True, help_text=_("Description of this template and when to use it")
    )
    is_active = models.BooleanField(
        default=True, help_text=_("Inactive templates cannot be used for new products")
    )

    # Pattern Configuration
    pattern = models.CharField(
        max_length=255,
        default="{RANDOM:5}-{RANDOM:5}-{RANDOM:5}-{RANDOM:5}-{RANDOM:5}",
        help_text=_(
            "Pattern template using placeholders:\n"
            "- {RANDOM:N} = N random characters\n"
            "- {CHECKSUM:N} = N-digit checksum\n"
            "- {PREFIX} = Template prefix\n"
            "- {SUFFIX} = Template suffix\n"
            "- {ORDER_ID} = Order number\n"
            "- {PRODUCT_SKU} = Product SKU\n"
            "- {DATE:FORMAT} = Formatted date (e.g., {DATE:YYMMDD})\n"
            "Example: MYAPP-{RANDOM:5}-{RANDOM:5}-{CHECKSUM:2}"
        ),
    )

    prefix = models.CharField(
        max_length=20, blank=True, help_text=_("Static prefix for all keys (e.g., 'MYAPP')")
    )

    suffix = models.CharField(max_length=20, blank=True, help_text=_("Static suffix for all keys"))

    separator = models.CharField(
        max_length=5, default="-", help_text=_("Character(s) used to separate key segments")
    )

    character_set = models.CharField(
        max_length=100,
        default="ABCDEFGHJKLMNPQRSTUVWXYZ23456789",
        help_text=_(
            "Characters to use for {RANDOM} segments. "
            "Default excludes ambiguous chars (0/O, 1/I, etc.)"
        ),
    )

    # Validation Rules
    min_length = models.IntegerField(
        default=20, help_text=_("Minimum total key length (including separators)")
    )

    max_length = models.IntegerField(
        default=50, help_text=_("Maximum total key length (including separators)")
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="license_templates_created",
    )

    class Meta:
        verbose_name = _("License Key Template")
        verbose_name_plural = _("License Key Templates")
        ordering = ["name"]

    def __str__(self):
        return self.name

    def generate_sample_key(self, context=None):
        """Generate a sample license key for preview"""
        from catalog.services.license_generator import LicenseKeyGenerator

        generator = LicenseKeyGenerator()
        return generator.generate(self, context or {})

    def validate_pattern(self):
        """Validate the pattern syntax"""
        import re

        from django.core.exceptions import ValidationError

        # Check for valid placeholders
        valid_placeholders = [
            "RANDOM",
            "CHECKSUM",
            "PREFIX",
            "SUFFIX",
            "ORDER_ID",
            "PRODUCT_SKU",
            "DATE",
        ]
        pattern_placeholders = re.findall(r"\{([A-Z_]+)(?::\w+)?\}", self.pattern)

        for placeholder in pattern_placeholders:
            if placeholder not in valid_placeholders:
                raise ValidationError(
                    f"Invalid placeholder: {{{placeholder}}}. "
                    f"Valid placeholders: {', '.join(valid_placeholders)}"
                )


class LicenseProvider(models.Model):
    """External license management system integration"""

    PROVIDER_TYPE_CHOICES = [
        ("spwig_server", _("Spwig Built-in License Server")),
        ("keygen", _("Keygen.sh")),
        ("licensespring", _("License Spring")),
        ("cryptlex", _("Cryptlex")),
        ("custom", _("Custom API")),
    ]

    CONNECTION_STATUS_CHOICES = [
        ("not_tested", _("Not Tested")),
        ("connected", _("Connected")),
        ("error", _("Error")),
    ]

    # Basic Info
    name = models.CharField(
        max_length=255, help_text=_("Provider name (e.g., 'Keygen Production')")
    )
    provider_type = models.CharField(
        max_length=20,
        choices=PROVIDER_TYPE_CHOICES,
        help_text=_("Type of external license provider"),
    )
    is_active = models.BooleanField(
        default=True, help_text=_("Inactive providers will not sync licenses")
    )

    # API Configuration
    api_endpoint = models.URLField(
        max_length=500, help_text=_("API base URL (e.g., 'https://api.keygen.sh/v1')")
    )
    api_key = models.CharField(
        max_length=500,
        help_text=_(
            "API key or token for authentication. NOTE: Store securely - consider encryption in production."
        ),
    )
    api_secret = models.CharField(
        max_length=500, blank=True, help_text=_("API secret (if required by provider)")
    )

    # Sync Configuration
    sync_on_order = models.BooleanField(
        default=True, help_text=_("Automatically sync license to provider when order is completed")
    )
    sync_on_activation = models.BooleanField(
        default=True, help_text=_("Sync device activations to provider")
    )
    sync_on_deactivation = models.BooleanField(
        default=True, help_text=_("Sync device deactivations to provider")
    )
    sync_bidirectional = models.BooleanField(
        default=False, help_text=_("Allow provider to update Spwig licenses via webhooks")
    )

    # Webhook Configuration
    webhook_secret = models.CharField(
        max_length=255, blank=True, help_text=_("Shared secret for webhook signature verification")
    )
    webhook_events = models.JSONField(
        default=list, blank=True, help_text=_("List of webhook events to receive from provider")
    )

    # Provider-Specific Config
    provider_config = models.JSONField(
        default=dict,
        blank=True,
        help_text=_("Provider-specific configuration (account ID, policy mappings, etc.)"),
    )

    # Product Mapping
    product_mapping = models.JSONField(
        default=dict,
        blank=True,
        help_text=_(
            "Map Spwig product IDs to external license policies/products. Format: {product_id: external_policy_id}"
        ),
    )

    # Connection Status
    connection_status = models.CharField(
        max_length=20,
        choices=CONNECTION_STATUS_CHOICES,
        default="not_tested",
        help_text=_("Current connection status to provider API"),
    )
    connection_error = models.TextField(
        blank=True, help_text=_("Error message if connection test failed")
    )
    last_tested_at = models.DateTimeField(
        null=True, blank=True, help_text=_("Last time connection was tested")
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("License Provider")
        verbose_name_plural = _("License Providers")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.get_provider_type_display()})"


class ExternalLicenseSync(models.Model):
    """Track synchronization operations with external license providers"""

    SYNC_DIRECTION_CHOICES = [
        ("outbound", _("Spwig → Provider")),
        ("inbound", _("Provider → Spwig")),
    ]

    SYNC_STATUS_CHOICES = [
        ("pending", _("Pending")),
        ("success", _("Success")),
        ("failed", _("Failed")),
    ]

    # Relationships
    license_key = models.ForeignKey(
        "LicenseKey",
        on_delete=models.CASCADE,
        related_name="external_syncs",
        help_text=_("Local license key being synced"),
    )
    provider = models.ForeignKey(
        "LicenseProvider",
        on_delete=models.CASCADE,
        related_name="sync_operations",
        help_text=_("External provider this sync is for"),
    )

    # External Reference
    external_id = models.CharField(
        max_length=255, db_index=True, help_text=_("License ID in external provider system")
    )
    external_data = models.JSONField(
        default=dict, blank=True, help_text=_("Full response data from external provider")
    )

    # Sync Info
    sync_direction = models.CharField(
        max_length=20, choices=SYNC_DIRECTION_CHOICES, help_text=_("Direction of synchronization")
    )
    sync_status = models.CharField(
        max_length=20,
        choices=SYNC_STATUS_CHOICES,
        default="pending",
        help_text=_("Status of sync operation"),
    )
    error_message = models.TextField(blank=True, help_text=_("Error details if sync failed"))

    # Timestamps
    synced_at = models.DateTimeField(auto_now_add=True)
    retry_count = models.IntegerField(default=0, help_text=_("Number of retry attempts"))
    next_retry_at = models.DateTimeField(
        null=True, blank=True, help_text=_("When to retry failed sync")
    )

    class Meta:
        verbose_name = _("External License Sync")
        verbose_name_plural = _("External License Syncs")
        ordering = ["-synced_at"]
        indexes = [
            models.Index(fields=["external_id"]),
            models.Index(fields=["sync_status"]),
        ]

    def __str__(self):
        return f"{self.license_key.key[:16]}... → {self.provider.name} ({self.sync_status})"


class WebhookSubscription(models.Model):
    """Webhook endpoint subscriptions for license events"""

    # Basic Info
    name = models.CharField(
        max_length=255,
        help_text=_("Descriptive name for this webhook (e.g., 'Production License Server')"),
    )
    url = models.URLField(max_length=500, help_text=_("Webhook endpoint URL"))
    secret = models.CharField(
        max_length=255, help_text=_("Shared secret for HMAC signature verification")
    )
    is_active = models.BooleanField(
        default=True, help_text=_("Inactive webhooks will not receive events")
    )

    # Event Configuration
    events = models.JSONField(
        default=list,
        help_text=_(
            "List of event types to receive (e.g., ['license.generated', 'license.activated'])"
        ),
    )

    # Filtering
    product_filter = models.ManyToManyField(
        "Product",
        blank=True,
        related_name="webhook_subscriptions",
        help_text=_("Only send events for these products (empty = all products)"),
    )
    license_type_filter = models.JSONField(
        default=list,
        blank=True,
        help_text=_("Only send events for these license types (e.g., ['software', 'content'])"),
    )

    # Delivery Settings
    max_retries = models.IntegerField(
        default=3, help_text=_("Maximum number of retry attempts for failed deliveries")
    )
    retry_delay_seconds = models.IntegerField(
        default=300, help_text=_("Delay in seconds between retry attempts")
    )

    # Statistics
    total_deliveries = models.IntegerField(
        default=0, help_text=_("Total webhook deliveries attempted")
    )
    successful_deliveries = models.IntegerField(
        default=0, help_text=_("Successful webhook deliveries")
    )
    failed_deliveries = models.IntegerField(default=0, help_text=_("Failed webhook deliveries"))
    last_delivery_at = models.DateTimeField(
        null=True, blank=True, help_text=_("Timestamp of last delivery attempt")
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Webhook Subscription")
        verbose_name_plural = _("Webhook Subscriptions")
        ordering = ["name"]

    def __str__(self):
        return self.name


class LicensePool(models.Model):
    """
    Bulk pre-generated license keys for products.

    License pools allow merchants to pre-generate batches of license keys
    for distribution via external channels (physical packaging, resellers, etc.)
    """

    STATUS_CHOICES = [
        ("generating", _("Generating")),
        ("ready", _("Ready")),
        ("depleted", _("Depleted")),
        ("expired", _("Expired")),
    ]

    # Basic Information
    name = models.CharField(max_length=255, help_text=_("Descriptive name for this license pool"))
    description = models.TextField(blank=True, help_text=_("Internal notes about this pool"))

    # Product Configuration
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="license_pools",
        verbose_name=_("Product"),
        help_text=_("Product these licenses are for"),
    )

    license_template = models.ForeignKey(
        "LicenseKeyTemplate",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="license_pools",
        verbose_name=_("License Template"),
        help_text=_("Template for generating keys. Uses product's template if not set."),
    )

    # Pool Configuration
    total_keys = models.IntegerField(default=100, help_text=_("Total number of keys to generate"))

    keys_generated = models.IntegerField(
        default=0, help_text=_("Number of keys successfully generated")
    )

    keys_distributed = models.IntegerField(
        default=0, help_text=_("Number of keys that have been distributed/used")
    )

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="generating", db_index=True
    )

    # License Configuration
    key_type = models.CharField(
        max_length=20,
        choices=LicenseKey.KEY_TYPE_CHOICES,
        default="perpetual",
        help_text=_("Type of license keys in this pool"),
    )

    max_activations = models.IntegerField(
        default=1, help_text=_("Maximum device activations per key")
    )

    expires_after_days = models.IntegerField(
        null=True,
        blank=True,
        help_text=_("Days until license expires after first activation (null = never)"),
    )

    # Expiration
    pool_expires_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("Date after which unused keys from this pool become invalid"),
    )

    # External Provider Sync
    sync_to_provider = models.ForeignKey(
        "LicenseProvider",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="synced_pools",
        verbose_name=_("Sync to Provider"),
        help_text=_("Automatically sync generated keys to this external provider"),
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_license_pools",
        verbose_name=_("Created By"),
    )

    # Generation metadata
    generation_started_at = models.DateTimeField(null=True, blank=True)
    generation_completed_at = models.DateTimeField(null=True, blank=True)
    generation_error = models.TextField(blank=True)

    class Meta:
        verbose_name = _("License Pool")
        verbose_name_plural = _("License Pools")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["product", "status"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.keys_distributed}/{self.keys_generated} used)"

    @property
    def available_keys_count(self):
        """Number of keys available for distribution"""
        return self.keys_generated - self.keys_distributed

    @property
    def progress_percentage(self):
        """Generation progress as percentage"""
        if self.total_keys == 0:
            return 100
        return int((self.keys_generated / self.total_keys) * 100)

    def get_available_keys(self, limit=None):
        """Get unassigned keys from this pool"""

        queryset = LicenseKey.objects.filter(
            license_pool=self,
            order_item__isnull=True,  # Not assigned to any order
            status="active",
        )

        if limit:
            queryset = queryset[:limit]

        return queryset

    def assign_key_to_order(self, order_item):
        """
        Assign a key from this pool to an order item.
        Returns the assigned LicenseKey or None if pool is depleted.
        """
        available_key = self.get_available_keys(limit=1).first()

        if not available_key:
            return None

        # Assign to order
        available_key.order_item = order_item
        available_key.user = order_item.order.user
        available_key.save()

        # Update pool statistics
        self.keys_distributed += 1
        if self.keys_distributed >= self.keys_generated:
            self.status = "depleted"
        self.save()

        return available_key


# ============================================================================
# CUSTOMIZABLE PRODUCTS
# ============================================================================


class CustomizationOption(models.Model):
    """
    Defines a customization option for a product.
    E.g., "Engraving Text", "Upload Design", "Wood Type"

    Each option has a type (text, file, select, etc.) and validation rules.
    Options can have pricing modifiers (fixed fee, percentage, per-unit).
    """

    OPTION_TYPE_CHOICES = [
        ("text", _("Text Input")),
        ("textarea", _("Multi-line Text")),
        ("file", _("File Upload")),
        ("select", _("Dropdown Select")),
        ("color", _("Color Picker")),
        ("number", _("Numeric Input")),
    ]

    PRICING_TYPE_CHOICES = [
        ("free", _("No Extra Charge")),
        ("fixed", _("Fixed Fee")),
        ("percentage", _("Percentage of Base Price")),
        ("per_unit", _("Per Character/Inch/etc")),
    ]

    # Product this option belongs to
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="customization_options",
        verbose_name=_("Product"),
        help_text=_("Product this customization option applies to"),
    )

    # Basic information
    name = models.CharField(
        max_length=200,
        verbose_name=_("Option Name"),
        help_text=_("Name of the customization option (e.g., 'Engraving Text', 'Wood Type')"),
    )
    slug = models.SlugField(
        max_length=200, verbose_name=_("Slug"), help_text=_("URL-friendly identifier")
    )
    description = models.TextField(
        blank=True, verbose_name=_("Description"), help_text=_("Help text shown to customers")
    )

    # Option configuration
    option_type = models.CharField(
        max_length=20,
        choices=OPTION_TYPE_CHOICES,
        verbose_name=_("Option Type"),
        help_text=_("Type of input field"),
    )
    is_required = models.BooleanField(
        default=True,
        verbose_name=_("Required"),
        help_text=_("Must customer provide this customization?"),
    )
    sort_order = models.IntegerField(
        default=0, verbose_name=_("Sort Order"), help_text=_("Display order (lower numbers first)")
    )

    # Validation rules (type-specific)
    max_length = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
        verbose_name=_("Max Length"),
        help_text=_("Maximum characters (for text/textarea)"),
    )
    allowed_file_types = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("Allowed File Types"),
        help_text=_("List of allowed file extensions (e.g., ['jpg', 'png', 'pdf'])"),
    )
    max_file_size_mb = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.01"))],
        verbose_name=_("Max File Size (MB)"),
        help_text=_("Maximum file size in megabytes"),
    )
    min_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Minimum Value"),
        help_text=_("Minimum numeric value (for number type)"),
    )
    max_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Maximum Value"),
        help_text=_("Maximum numeric value (for number type)"),
    )

    # Pricing
    pricing_type = models.CharField(
        max_length=20,
        choices=PRICING_TYPE_CHOICES,
        default="free",
        verbose_name=_("Pricing Type"),
        help_text=_("How to calculate additional cost"),
    )
    price_amount = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency="USD",
        default=Decimal("0.00"),
        verbose_name=_("Price Amount"),
        help_text=_("Fixed fee or per-unit rate depending on pricing type"),
    )

    # For select/color options - list of choices
    # Structure: [
    #   {'value': 'oak', 'label': 'Oak Wood', 'price_modifier': 10.00, 'color': '#...'},
    #   {'value': 'walnut', 'label': 'Walnut Wood', 'price_modifier': 25.00},
    # ]
    choices = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("Choices"),
        help_text=_("Available choices for select/color options with optional price modifiers"),
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Customization Option")
        verbose_name_plural = _("Customization Options")
        ordering = ["product", "sort_order", "name"]
        unique_together = [["product", "slug"]]
        indexes = [
            models.Index(fields=["product", "sort_order"]),
        ]

    def __str__(self):
        return f"{self.product.name} - {self.name}"

    def save(self, *args, **kwargs):
        """Auto-generate slug if not provided"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def validate_value(self, value):
        """
        Validate a customer's input value against this option's rules.

        Args:
            value: The value to validate (str, file, number, etc.)

        Returns:
            tuple: (is_valid: bool, error_message: str or None)
        """

        # Required check
        if self.is_required and not value:
            return False, _("This customization is required")

        if not value:
            return True, None

        # Type-specific validation
        if self.option_type in ("text", "textarea"):
            if self.max_length and len(str(value)) > self.max_length:
                return False, _("Text exceeds maximum length of {max} characters").format(
                    max=self.max_length
                )

        elif self.option_type == "number":
            try:
                num_value = Decimal(str(value))
                if self.min_value is not None and num_value < self.min_value:
                    return False, _("Value must be at least {min}").format(min=self.min_value)
                if self.max_value is not None and num_value > self.max_value:
                    return False, _("Value must be at most {max}").format(max=self.max_value)
            except (ValueError, TypeError):
                return False, _("Invalid numeric value")

        elif self.option_type == "select":
            # Validate choice exists
            valid_values = [choice.get("value") for choice in self.choices]
            if value not in valid_values:
                return False, _("Invalid selection")

        elif self.option_type == "color":
            # Basic hex color validation
            import re

            if not re.match(r"^#[0-9A-Fa-f]{6}$", str(value)):
                return False, _("Invalid color format (use #RRGGBB)")

        return True, None

    def calculate_price(self, value, base_price):
        """
        Calculate the additional price for this customization.

        Args:
            value: Customer's input value
            base_price: Product base price (Money object)

        Returns:
            Money: Additional price for this customization
        """
        from djmoney.money import Money

        # For select/color options, check choice-specific price modifiers first
        # This takes precedence over the general pricing_type setting
        if self.option_type in ("select", "color") and self.choices:
            for choice in self.choices:
                if choice.get("value") == value:
                    modifier = choice.get("price_modifier")
                    if modifier is not None:
                        return Money(Decimal(str(modifier)), base_price.currency)

        # Apply general pricing rules
        if self.pricing_type == "free":
            return Money(0, base_price.currency)

        elif self.pricing_type == "fixed":
            return Money(self.price_amount.amount, base_price.currency)

        elif self.pricing_type == "percentage":
            percentage = self.price_amount.amount / Decimal("100")
            return Money(base_price.amount * percentage, base_price.currency)

        elif self.pricing_type == "per_unit":
            # Calculate units based on option type
            if self.option_type in ("text", "textarea"):
                units = len(str(value)) if value else 0
            elif self.option_type == "number":
                try:
                    units = Decimal(str(value))
                except (ValueError, TypeError):
                    units = Decimal("0")
            else:
                units = 1

            return Money(self.price_amount.amount * Decimal(str(units)), base_price.currency)

        return Money(0, base_price.currency)


class CustomizationValue(models.Model):
    """
    Stores a customer's customization choice for an order item.

    Each CustomizationValue represents one filled-out option
    (e.g., "Engraving Text = 'Happy Birthday'").
    """

    # Order item this customization belongs to
    order_item = models.ForeignKey(
        "orders.OrderItem",
        on_delete=models.CASCADE,
        related_name="customization_values",
        verbose_name=_("Order Item"),
        help_text=_("Order item this customization applies to"),
    )

    # The option being customized
    customization_option = models.ForeignKey(
        "CustomizationOption",
        on_delete=models.PROTECT,
        related_name="values",
        verbose_name=_("Customization Option"),
        help_text=_("Which customization option this value is for"),
    )

    # Value storage (type depends on option_type)
    text_value = models.TextField(
        blank=True, verbose_name=_("Text Value"), help_text=_("Text/textarea input value")
    )
    file_value = models.ForeignKey(
        "media_library.MediaAsset",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="customization_values",
        verbose_name=_("File Value"),
        help_text=_("Uploaded file asset"),
    )
    choice_value = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("Choice Value"),
        help_text=_("Selected choice (select/color)"),
    )
    number_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Numeric Value"),
        help_text=_("Numeric input value"),
    )

    # Calculated price for this specific customization
    calculated_price = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency="USD",
        default=Decimal("0.00"),
        verbose_name=_("Calculated Price"),
        help_text=_("Additional cost for this customization"),
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    class Meta:
        verbose_name = _("Customization Value")
        verbose_name_plural = _("Customization Values")
        ordering = ["order_item", "customization_option__sort_order"]
        indexes = [
            models.Index(fields=["order_item"]),
        ]

    def __str__(self):
        option_name = self.customization_option.name
        value = self.get_display_value()
        return f"{option_name}: {value}"

    def get_display_value(self):
        """Get the customer's value in a human-readable format"""
        option_type = self.customization_option.option_type

        if option_type in ("text", "textarea"):
            return self.text_value or _("(empty)")
        elif option_type == "file":
            return self.file_value.filename if self.file_value else _("(no file)")
        elif option_type in ("select", "color"):
            # Try to find label from choices
            if self.choice_value:
                for choice in self.customization_option.choices:
                    if choice.get("value") == self.choice_value:
                        return choice.get("label", self.choice_value)
            return self.choice_value or _("(not selected)")
        elif option_type == "number":
            return str(self.number_value) if self.number_value is not None else _("(not set)")

        return _("(unknown)")

    def get_value_for_export(self):
        """
        Get the raw value suitable for export/production systems.

        Returns:
            dict with value and any metadata
        """
        option_type = self.customization_option.option_type

        if option_type in ("text", "textarea"):
            return {
                "type": option_type,
                "value": self.text_value,
            }
        elif option_type == "file":
            if self.file_value:
                return {
                    "type": "file",
                    "filename": self.file_value.filename,
                    "url": self.file_value.file.url if self.file_value.file else None,
                    "file_type": self.file_value.file_type,
                }
            return {"type": "file", "value": None}
        elif option_type in ("select", "color"):
            return {
                "type": option_type,
                "value": self.choice_value,
                "label": self.get_display_value(),
            }
        elif option_type == "number":
            return {
                "type": "number",
                "value": float(self.number_value) if self.number_value else None,
            }

        return {"type": "unknown", "value": None}


# ============================================================================
# GIFT CARDS
# ============================================================================


class GiftCard(models.Model):
    """
    Store credit that can be purchased and redeemed.
    Always digital products delivered via email with unique redemption codes.
    """

    # Unique redemption code (e.g., GC-XXXX-XXXX-XXXX)
    code = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        verbose_name=_("Gift Card Code"),
        help_text=_("Unique redemption code"),
    )

    # Product this gift card was purchased from
    product = models.ForeignKey(
        "Product",
        on_delete=models.PROTECT,
        limit_choices_to={"product_type": "gift_card"},
        related_name="gift_cards",
        verbose_name=_("Product"),
        help_text=_("Gift card product"),
    )

    # Order that created this gift card
    order_item = models.ForeignKey(
        "orders.OrderItem",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="gift_cards",
        verbose_name=_("Order Item"),
        help_text=_("Purchase that created this card"),
    )

    # Balance tracking
    initial_value = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency=None,
        verbose_name=_("Initial Value"),
        help_text=_("Original amount"),
    )

    current_balance = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency=None,
        verbose_name=_("Current Balance"),
        help_text=_("Remaining balance"),
    )

    # Recipient information
    recipient_email = models.EmailField(
        verbose_name=_("Recipient Email"), help_text=_("Email address to send gift card to")
    )

    recipient_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Recipient Name"),
        help_text=_("Name of gift card recipient"),
    )

    sender_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Sender Name"),
        help_text=_("Name of person sending the gift card"),
    )

    # Personal message from sender (supports translations for display)
    message = models.TextField(
        blank=True,
        verbose_name=_("Personal Message"),
        help_text=_("Message from sender to recipient"),
    )

    # Translations for template content (not user message)
    translations = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Translations"),
        help_text=_("Multi-language content for email template"),
    )

    # Status and expiration
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
        help_text=_("Whether this gift card can be redeemed"),
    )

    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Expires At"),
        help_text=_("Expiration date and time (null = never expires)"),
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    issued_at = models.DateTimeField(
        null=True, blank=True, verbose_name=_("Issued At"), help_text=_("When sent to recipient")
    )

    first_used_at = models.DateTimeField(
        null=True, blank=True, verbose_name=_("First Used At"), help_text=_("When first redeemed")
    )

    # Scheduled delivery
    scheduled_send_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Scheduled Send At"),
        help_text=_("When to send the gift card email. If null, sends immediately."),
    )

    # Creator (for manually created cards)
    created_by = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_gift_cards",
        verbose_name=_("Created By"),
        help_text=_("Admin who manually created this card"),
    )

    class Meta:
        verbose_name = _("Gift Card")
        verbose_name_plural = _("Gift Cards")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["recipient_email"]),
            models.Index(fields=["is_active", "expires_at"]),
            models.Index(fields=["scheduled_send_at", "issued_at"]),
        ]

    def __str__(self):
        return f"{self.code} - {self.current_balance} / {self.initial_value}"

    def save(self, *args, **kwargs):
        """Generate unique code if not set"""
        if not self.code:
            self.code = self.generate_code()

        # Ensure current_balance is set on creation
        if not self.pk and not self.current_balance:
            self.current_balance = self.initial_value

        super().save(*args, **kwargs)

    @staticmethod
    def generate_code(prefix="GC"):
        """
        Generate a unique gift card code.
        Format: GC-XXXX-XXXX-XXXX (16 random alphanumeric characters)

        Returns:
            str: Unique gift card code
        """
        import secrets
        import string

        # Use cryptographically secure random generation
        alphabet = string.ascii_uppercase + string.digits
        # Remove easily confused characters (0, O, I, 1)
        alphabet = alphabet.replace("0", "").replace("O", "").replace("I", "").replace("1", "")

        max_attempts = 10
        for _attempt in range(max_attempts):
            # Generate 12 random characters in groups of 4
            part1 = "".join(secrets.choice(alphabet) for _c in range(4))
            part2 = "".join(secrets.choice(alphabet) for _c in range(4))
            part3 = "".join(secrets.choice(alphabet) for _c in range(4))

            code = f"{prefix}-{part1}-{part2}-{part3}"

            # Check uniqueness
            if not GiftCard.objects.filter(code=code).exists():
                return code

        # Fallback to UUID if random generation fails (very unlikely)
        import uuid

        return f"{prefix}-{uuid.uuid4().hex[:12].upper()}"

    def clean(self):
        """Validate gift card configuration"""
        from django.core.exceptions import ValidationError

        # Validate balance
        if self.current_balance and self.current_balance.amount < 0:
            raise ValidationError({"current_balance": _("Balance cannot be negative")})

        if self.initial_value and self.current_balance:
            if self.current_balance.amount > self.initial_value.amount:
                raise ValidationError(
                    {"current_balance": _("Current balance cannot exceed initial value")}
                )

        # Validate expiration
        if self.expires_at and self.expires_at < timezone.now() and not self.pk:  # New card
            raise ValidationError({"expires_at": _("Expiration date must be in the future")})

    @property
    def is_expired(self):
        """Check if gift card has expired"""
        if not self.expires_at:
            return False
        return timezone.now() > self.expires_at

    @property
    def is_fully_redeemed(self):
        """Check if gift card has been fully used"""
        return self.current_balance.amount == 0

    @property
    def is_valid(self):
        """Check if gift card can be used"""
        return (
            self.is_active
            and not self.is_expired
            and not self.is_fully_redeemed
            and self.current_balance.amount > 0
        )

    @property
    def redemption_percentage(self):
        """Get percentage of card that has been redeemed"""
        if self.initial_value.amount == 0:
            return 0
        redeemed = self.initial_value.amount - self.current_balance.amount
        return (redeemed / self.initial_value.amount) * 100

    def can_redeem(self, amount):
        """
        Check if gift card can redeem a specific amount.

        Args:
            amount: Money object or Decimal amount to redeem

        Returns:
            tuple: (bool, str) - (can_redeem, error_message)
        """
        from decimal import Decimal

        from djmoney.money import Money

        # Convert to Money if needed
        if isinstance(amount, (Decimal, int, float)):
            amount = Money(amount, self.current_balance.currency)

        if not self.is_active:
            return False, _("Gift card is not active")

        if self.is_expired:
            return False, _("Gift card has expired")

        if self.current_balance.amount == 0:
            return False, _("Gift card has no remaining balance")

        if amount.amount <= 0:
            return False, _("Redemption amount must be positive")

        if amount.amount > self.current_balance.amount:
            return False, _("Insufficient balance. Available: {balance}").format(
                balance=self.current_balance
            )

        # Check currency match
        if amount.currency.code != self.current_balance.currency.code:
            return False, _(
                "Currency mismatch. Gift card is in {card_currency}, order is in {order_currency}"
            ).format(
                card_currency=self.current_balance.currency.code,
                order_currency=amount.currency.code,
            )

        return True, ""

    def redeem(self, amount, order=None, notes=""):
        """
        Redeem an amount from this gift card.
        Creates a transaction record and updates balance.

        Args:
            amount: Money object to redeem
            order: Optional Order this is being redeemed for
            notes: Optional notes about the redemption

        Returns:
            GiftCardTransaction: The transaction record

        Raises:
            ValidationError: If redemption is not allowed
        """
        from django.core.exceptions import ValidationError

        can_redeem, error_msg = self.can_redeem(amount)
        if not can_redeem:
            raise ValidationError(error_msg)

        # Update balance
        self.current_balance -= amount

        # Set first_used_at if this is the first redemption
        if not self.first_used_at:
            self.first_used_at = timezone.now()

        self.save(update_fields=["current_balance", "first_used_at"])

        # Create transaction record
        transaction = GiftCardTransaction.objects.create(
            gift_card=self,
            transaction_type="redemption",
            amount=-amount,  # Negative for redemptions
            balance_after=self.current_balance,
            order=order,
            notes=notes,
        )

        return transaction

    def issue(self, send_email=True):
        """
        Mark gift card as issued and optionally send email.

        Args:
            send_email: Whether to send email to recipient
        """
        if not self.issued_at:
            self.issued_at = timezone.now()
            self.save(update_fields=["issued_at"])

            # Create issue transaction
            GiftCardTransaction.objects.create(
                gift_card=self,
                transaction_type="issue",
                amount=self.initial_value,
                balance_after=self.current_balance,
                notes=_("Gift card issued to {email}").format(email=self.recipient_email),
            )

        if send_email and self.recipient_email:
            try:
                from core.models import SiteSettings
                from email_system.services.email_sender import EmailSendingService

                settings = SiteSettings.get_settings()
                site_url = (settings.site_url or "").rstrip("/")

                formatted_expiry = ""
                if self.expires_at:
                    formatted_expiry = self.expires_at.strftime("%B %d, %Y")

                context = {
                    "gift_card": {
                        "code": self.code,
                        "current_balance": str(self.current_balance),
                        "initial_value": str(self.initial_value),
                        "expires_at": formatted_expiry,
                        "message": self.message or "",
                        "sender_name": self.sender_name or "",
                        "recipient_name": self.recipient_name or "",
                        "recipient_email": self.recipient_email,
                    },
                    "recipient_name": self.recipient_name or "",
                    "recipient_email": self.recipient_email,
                    "sender_name": self.sender_name or "",
                    "gift_card_code": self.code,
                    "gift_card_amount": str(self.initial_value),
                    "gift_card_message": self.message or "",
                    "gift_card_expiry": formatted_expiry,
                    "check_balance_url": f"{site_url}/gift-cards/check-balance/",
                    "redeem_url": f"{site_url}/gift-cards/redeem/",
                }

                EmailSendingService.send_template_email(
                    to_email=self.recipient_email,
                    template_type="gift_card_delivery",
                    context=context,
                    language=settings.default_language,
                )
            except Exception:
                import logging

                logging.getLogger(__name__).exception(
                    "Failed to send gift card delivery email for ***%s", self.code[-4:]
                )

    def adjust_balance(self, amount, reason="", created_by=None):
        """
        Manually adjust gift card balance (admin function).

        Args:
            amount: Money object (positive or negative)
            reason: Reason for adjustment
            created_by: User making the adjustment

        Returns:
            GiftCardTransaction: The transaction record
        """

        # Update balance
        self.current_balance += amount
        self.save(update_fields=["current_balance"])

        # Create transaction
        transaction = GiftCardTransaction.objects.create(
            gift_card=self,
            transaction_type="adjustment",
            amount=amount,
            balance_after=self.current_balance,
            notes=reason,
            created_by=created_by,
        )

        return transaction


class GiftCardTransaction(models.Model):
    """
    Tracks all balance changes for a gift card.
    Provides complete audit trail of all gift card activity.
    """

    TRANSACTION_TYPE_CHOICES = [
        ("issue", _("Issued")),
        ("redemption", _("Redeemed")),
        ("adjustment", _("Manual Adjustment")),
        ("refund", _("Refunded")),
        ("expiration", _("Expired")),
    ]

    gift_card = models.ForeignKey(
        GiftCard, on_delete=models.CASCADE, related_name="transactions", verbose_name=_("Gift Card")
    )

    transaction_type = models.CharField(
        max_length=20, choices=TRANSACTION_TYPE_CHOICES, verbose_name=_("Transaction Type")
    )

    amount = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency=None,
        verbose_name=_("Amount"),
        help_text=_("Positive for additions, negative for deductions"),
    )

    balance_after = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency=None,
        verbose_name=_("Balance After"),
        help_text=_("Gift card balance after this transaction"),
    )

    # Order this transaction is associated with (for redemptions/refunds)
    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="gift_card_transactions",
        verbose_name=_("Order"),
    )

    notes = models.TextField(
        blank=True,
        verbose_name=_("Notes"),
        help_text=_("Additional information about this transaction"),
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    created_by = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="gift_card_transactions",
        verbose_name=_("Created By"),
        help_text=_("User who performed this transaction"),
    )

    class Meta:
        verbose_name = _("Gift Card Transaction")
        verbose_name_plural = _("Gift Card Transactions")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["gift_card", "-created_at"]),
            models.Index(fields=["transaction_type"]),
        ]

    def __str__(self):
        return f"{self.gift_card.code} - {self.get_transaction_type_display()} - {self.amount}"

    def clean(self):
        """Validate transaction"""
        from django.core.exceptions import ValidationError

        # Ensure currencies match
        if self.amount.currency != self.balance_after.currency:
            raise ValidationError(_("Amount and balance currencies must match"))

        if self.gift_card_id and self.amount.currency != self.gift_card.current_balance.currency:
            raise ValidationError(_("Transaction currency must match gift card currency"))


# ============================================================================
# STOCK DISPLAY SETTINGS (Singleton)
# ============================================================================


class StockDisplaySettings(models.Model):
    """
    Site-wide stock display configuration for the storefront.
    This is a singleton model - only one instance should exist.
    """

    # Out-of-stock action choices (used by Category and Product overrides too)
    OUT_OF_STOCK_ACTIONS = [
        ("hide", _("Hide from listings")),
        ("show_unavailable", _("Show as unavailable")),
        ("notify_me", _('Show "Notify Me" button')),
        ("allow_backorder", _("Allow backorders")),
    ]

    # Stock status display
    show_stock_status = models.BooleanField(
        _("show stock status"),
        default=True,
        help_text=_("Display stock status (In Stock, Out of Stock) on product pages"),
    )
    show_low_stock_warning = models.BooleanField(
        _("show low stock warning"),
        default=True,
        help_text=_('Display "Only X left" warning when stock is low'),
    )
    low_stock_threshold = models.PositiveIntegerField(
        _("low stock threshold"),
        default=5,
        help_text=_("Show low stock warning when available quantity is at or below this number"),
    )
    show_exact_quantity = models.BooleanField(
        _("show exact quantity"),
        default=False,
        help_text=_('Display exact quantity available (e.g., "Only 3 left!")'),
    )

    # Out-of-stock behavior (site-wide default)
    out_of_stock_action = models.CharField(
        _("out of stock action"),
        max_length=20,
        choices=OUT_OF_STOCK_ACTIONS,
        default="notify_me",
        help_text=_("Default behavior when a product is out of stock"),
    )
    out_of_stock_message = models.CharField(
        _("out of stock message"),
        max_length=100,
        default="Out of Stock",
        help_text=_("Message shown when product is out of stock"),
    )
    backorder_message = models.CharField(
        _("backorder message"),
        max_length=100,
        default="Available on backorder",
        help_text=_("Message shown when backorders are allowed"),
    )

    # Warehouse display
    show_ships_from = models.BooleanField(
        _('show "ships from" location'),
        default=False,
        help_text=_("Display the warehouse location a product ships from"),
    )
    show_estimated_delivery = models.BooleanField(
        _("show estimated delivery"),
        default=True,
        help_text=_("Display estimated delivery dates on product pages"),
    )

    # Allow backorders (site-wide default)
    allow_backorders = models.BooleanField(
        _("allow backorders"),
        default=False,
        help_text=_("Allow customers to order products that are out of stock"),
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Stock Display Settings")
        verbose_name_plural = _("Stock Display Settings")

    def __str__(self):
        return _("Stock Display Settings")

    @classmethod
    def get_settings(cls):
        """
        Get the current stock display settings instance, creating one if it doesn't exist.
        """
        settings, created = cls.objects.get_or_create(pk=1)
        return settings


# ============================================================================
# STOCK NOTIFICATION
# ============================================================================


class StockNotification(models.Model):
    """
    Customer requests for back-in-stock notifications.
    When a product comes back in stock, customers who signed up will be notified.
    """

    email = models.EmailField(_("email address"))
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="stock_notifications",
        verbose_name=_("product"),
    )
    variant = models.ForeignKey(
        "ProductVariant",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="stock_notifications",
        verbose_name=_("variant"),
        help_text=_("Specific variant to notify about (null for base product)"),
    )

    # Optional: track which warehouse they wanted
    preferred_warehouse = models.ForeignKey(
        "Warehouse",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="stock_notifications",
        verbose_name=_("preferred warehouse"),
        help_text=_("Preferred warehouse for regional notifications"),
    )

    # Track notification status
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notified_at = models.DateTimeField(
        _("notified at"),
        null=True,
        blank=True,
        help_text=_("When the back-in-stock notification was sent"),
    )

    class Meta:
        verbose_name = _("Stock Notification")
        verbose_name_plural = _("Stock Notifications")
        unique_together = ["email", "product", "variant"]
        indexes = [
            models.Index(fields=["product", "notified_at"]),
            models.Index(fields=["email"]),
        ]

    def __str__(self):
        variant_str = f" ({self.variant})" if self.variant else ""
        return f"{self.email} - {self.product.name}{variant_str}"


# ============================================================================
# PRODUCT CONFIGURATOR
# ============================================================================


class ConfigurationSlot(models.Model):
    """
    A configurable slot within a configurable product.
    Each slot represents a component category (e.g., CPU, RAM, Storage, Add-ons).
    """

    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="configuration_slots",
        limit_choices_to={"product_type": "configurable"},
        verbose_name=_("Product"),
    )
    name = models.CharField(
        max_length=200,
        verbose_name=_("Slot Name"),
        help_text=_("Name shown to customers, e.g. 'Processor', 'Memory', 'Add-ons'"),
    )
    slug = models.SlugField(max_length=200, verbose_name=_("Slug"))
    description = models.TextField(
        blank=True,
        verbose_name=_("Description"),
        help_text=_("Optional description shown to customers when selecting options for this slot"),
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("Icon"),
        help_text=_("Font Awesome icon class, e.g. 'fas fa-microchip'"),
    )

    # Selection rules
    is_required = models.BooleanField(
        default=True,
        verbose_name=_("Required"),
        help_text=_("Must the customer select an option in this slot?"),
    )
    min_selections = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Minimum Selections"),
        help_text=_("Minimum number of options the customer must pick (1 for single-select)"),
    )
    max_selections = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Maximum Selections"),
        help_text=_(
            "Maximum options allowed. Set >1 for multi-select (e.g., add-ons, extra storage)."
        ),
    )

    sort_order = models.IntegerField(default=0, verbose_name=_("Sort Order"))

    # Translations for merchant content
    translations = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Translations"),
        help_text=_("Translated name and description by language code"),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Configuration Slot")
        verbose_name_plural = _("Configuration Slots")
        ordering = ["sort_order", "name"]
        unique_together = [("product", "slug")]
        indexes = [
            models.Index(fields=["product", "sort_order"]),
        ]

    def __str__(self):
        return f"{self.product.name} - {self.name}"

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.min_selections > self.max_selections:
            raise ValidationError(
                {"min_selections": _("Minimum selections cannot exceed maximum selections.")}
            )
        if not self.is_required and self.min_selections > 0:
            # Optional slots can have min_selections = 0
            pass


class ConfigurationSlotOption(models.Model):
    """
    A product available as an option within a configuration slot.
    Links a real product (with inventory) to a slot.
    """

    slot = models.ForeignKey(
        ConfigurationSlot,
        on_delete=models.CASCADE,
        related_name="options",
        verbose_name=_("Slot"),
    )
    option_product = models.ForeignKey(
        "Product",
        on_delete=models.PROTECT,
        related_name="configurator_slot_options",
        verbose_name=_("Option Product"),
        help_text=_("The product offered as an option in this slot."),
    )
    option_variant = models.ForeignKey(
        "ProductVariant",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="configurator_slot_options",
        verbose_name=_("Option Variant"),
        help_text=_("Specific variant, if applicable."),
    )

    # Allow customer to choose variant at configuration time
    allow_variant_selection = models.BooleanField(
        default=False,
        verbose_name=_("Allow Variant Selection"),
        help_text=_("Let customer choose a variant of this product at configuration time."),
    )

    # Price adjustment (for base_plus_adjustments strategy)
    price_adjustment = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency="USD",
        default=Decimal("0.00"),
        verbose_name=_("Price Adjustment"),
        help_text=_(
            "For 'Base + Adjustments' pricing: amount added to base price when selected. "
            "Positive = surcharge, negative = discount."
        ),
    )

    # Display
    is_default = models.BooleanField(
        default=False,
        verbose_name=_("Default Option"),
        help_text=_("Pre-selected when the slot first loads."),
    )
    is_popular = models.BooleanField(
        default=False,
        verbose_name=_("Popular / Recommended"),
        help_text=_("Highlight as a popular or recommended choice."),
    )
    sort_order = models.IntegerField(default=0, verbose_name=_("Sort Order"))

    # Compatibility tags (for batch rule generation)
    compatibility_tags = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("Compatibility Tags"),
        help_text=_('Tags like ["socket-AM5", "DDR5"] for batch compatibility rule generation.'),
    )

    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Quantity"),
        help_text=_("How many units of this product are included when selected."),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Configuration Slot Option")
        verbose_name_plural = _("Configuration Slot Options")
        ordering = ["sort_order", "pk"]
        unique_together = [("slot", "option_product", "option_variant")]
        indexes = [
            models.Index(fields=["slot", "sort_order"]),
            models.Index(fields=["option_product"]),
        ]

    def __str__(self):
        variant_str = f" ({self.option_variant})" if self.option_variant else ""
        return f"{self.slot.name}: {self.option_product.name}{variant_str}"

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.option_variant and self.option_variant.product != self.option_product:
            raise ValidationError(
                {"option_variant": _("Variant must belong to the selected product.")}
            )

    def get_effective_price(self):
        """Get the effective price of this option (product/variant price)."""
        if self.option_variant:
            return self.option_variant.get_effective_price()
        return self.option_product.effective_price


class CompatibilityRule(models.Model):
    """
    Pairwise compatibility rule: when source option is selected,
    only compatible target options are available in the target slot.

    If no rules exist for a source_option→target_slot pair, all options are available (open).
    If 'requires' rules exist, only listed options are shown (whitelist).
    If 'excludes' rules exist, listed options are hidden (blacklist).
    """

    RULE_TYPE_CHOICES = [
        ("requires", _("Requires (compatible with)")),
        ("excludes", _("Excludes (incompatible with)")),
    ]

    configurable_product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="compatibility_rules",
        limit_choices_to={"product_type": "configurable"},
        verbose_name=_("Configurable Product"),
    )

    rule_type = models.CharField(
        max_length=10,
        choices=RULE_TYPE_CHOICES,
        default="requires",
        verbose_name=_("Rule Type"),
    )

    # Source: when this option is selected...
    source_option = models.ForeignKey(
        ConfigurationSlotOption,
        on_delete=models.CASCADE,
        related_name="outgoing_rules",
        verbose_name=_("Source Option"),
        help_text=_("When this option is selected..."),
    )

    # Target: ...filter options in this slot
    target_slot = models.ForeignKey(
        ConfigurationSlot,
        on_delete=models.CASCADE,
        related_name="incoming_rules",
        verbose_name=_("Target Slot"),
        help_text=_("...filter options in this slot."),
    )

    compatible_options = models.ManyToManyField(
        ConfigurationSlotOption,
        related_name="compatible_via_rules",
        blank=True,
        verbose_name=_("Compatible Options"),
        help_text=_(
            "Options in target slot affected by this rule. "
            "For 'requires': only these are shown. For 'excludes': these are hidden."
        ),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Compatibility Rule")
        verbose_name_plural = _("Compatibility Rules")
        indexes = [
            models.Index(fields=["configurable_product"]),
            models.Index(fields=["source_option", "target_slot"]),
        ]

    def __str__(self):
        return f"{self.source_option} → {self.target_slot.name} ({self.get_rule_type_display()})"

    def clean(self):
        from django.core.exceptions import ValidationError

        # Source option must belong to the same configurable product
        if self.source_option_id and self.source_option.slot.product != self.configurable_product:
            raise ValidationError(
                {"source_option": _("Source option must belong to this configurable product.")}
            )
        # Target slot must belong to the same configurable product
        if self.target_slot_id and self.target_slot.product != self.configurable_product:
            raise ValidationError(
                {"target_slot": _("Target slot must belong to this configurable product.")}
            )
        # Source and target must be different slots
        if self.source_option_id and self.target_slot_id:
            if self.source_option.slot == self.target_slot:
                raise ValidationError(
                    {
                        "target_slot": _(
                            "Target slot must be different from the source option's slot."
                        )
                    }
                )


class ConfigurationPreset(models.Model):
    """
    A pre-built configuration that customers can use as a starting point.
    E.g., 'Budget Build', 'Pro Workstation', 'Gaming Rig'.
    """

    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="configuration_presets",
        limit_choices_to={"product_type": "configurable"},
        verbose_name=_("Product"),
    )
    name = models.CharField(max_length=200, verbose_name=_("Preset Name"))
    slug = models.SlugField(max_length=200, verbose_name=_("Slug"))
    description = models.TextField(blank=True, verbose_name=_("Description"))

    # Image for the preset card
    image_asset = models.ForeignKey(
        "media_library.MediaAsset",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Preset Image"),
    )

    # The actual selections: {slot_id: [option_id, ...], ...}
    selections = models.JSONField(
        default=dict,
        verbose_name=_("Preset Selections"),
        help_text=_("Map of slot ID to list of selected option IDs."),
    )

    is_featured = models.BooleanField(default=False, verbose_name=_("Featured Preset"))
    sort_order = models.IntegerField(default=0, verbose_name=_("Sort Order"))

    # Translations for merchant content
    translations = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Translations"),
        help_text=_("Translated name and description by language code"),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Configuration Preset")
        verbose_name_plural = _("Configuration Presets")
        ordering = ["sort_order", "name"]
        unique_together = [("product", "slug")]

    def __str__(self):
        return f"{self.product.name} - {self.name}"

    def get_total_price(self):
        """Calculate total price for this preset based on selected options."""
        from djmoney.money import Money

        total = Decimal("0.00")
        currency = self.product.price.currency if self.product.price else "USD"

        for _slot_id_str, option_ids in self.selections.items():
            for option_id in option_ids:
                try:
                    option = ConfigurationSlotOption.objects.select_related(
                        "option_product", "option_variant"
                    ).get(id=option_id)
                    price = option.get_effective_price()
                    if price:
                        total += price.amount * option.quantity
                except ConfigurationSlotOption.DoesNotExist:
                    continue
        return Money(total, currency)


# ============================================================================
# BOOKING PRODUCT TYPE
# ============================================================================


class BookingConfig(models.Model):
    """
    Configuration for a booking product. One-to-one with Product.

    Supports appointments, rentals, classes, events, and accommodation bookings.
    Beyond WooCommerce: adds recurring bookings, waitlist, deposits, timezone
    awareness, and multiple calendar display modes.
    """

    BOOKING_TYPES = [
        ("appointment", _("Appointment")),
        ("rental", _("Rental")),
        ("class", _("Class / Workshop")),
        ("accommodation", _("Accommodation")),
        ("event", _("Event")),
    ]

    DURATION_TYPES = [
        ("fixed", _("Fixed Duration")),
        ("customer_selected", _("Customer Selects Duration")),
    ]

    DURATION_UNITS = [
        ("minute", _("Minute(s)")),
        ("hour", _("Hour(s)")),
        ("day", _("Day(s)")),
        ("night", _("Night(s)")),
    ]

    CALENDAR_DISPLAY = [
        ("calendar", _("Calendar View")),
        ("date_picker", _("Date Picker")),
        ("dropdown", _("Available Dates Dropdown")),
        ("date_range", _("Date Range Picker")),
    ]

    DEPOSIT_TYPES = [
        ("fixed", _("Fixed Amount")),
        ("percentage", _("Percentage of Total")),
    ]

    ADVANCE_UNITS = [
        ("hour", _("Hours")),
        ("day", _("Days")),
        ("week", _("Weeks")),
        ("month", _("Months")),
    ]

    CANCELLATION_UNITS = [
        ("hour", _("Hours")),
        ("day", _("Days")),
        ("week", _("Weeks")),
    ]

    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="booking_config",
    )

    # Booking type
    booking_type = models.CharField(
        max_length=20,
        choices=BOOKING_TYPES,
        default="appointment",
    )

    # Duration
    duration_type = models.CharField(
        max_length=20,
        choices=DURATION_TYPES,
        default="fixed",
    )
    duration = models.PositiveIntegerField(
        default=60,
        help_text=_("Default duration value"),
    )
    duration_unit = models.CharField(
        max_length=10,
        choices=DURATION_UNITS,
        default="minute",
    )
    min_duration = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text=_("Minimum duration for customer-selected (in duration_unit)"),
    )
    max_duration = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text=_("Maximum duration for customer-selected (in duration_unit)"),
    )

    # Buffer time
    buffer_before = models.PositiveIntegerField(
        default=0,
        help_text=_("Buffer time before booking (minutes)"),
    )
    buffer_after = models.PositiveIntegerField(
        default=0,
        help_text=_("Buffer time after booking (minutes)"),
    )

    # Advance booking window
    min_advance = models.PositiveIntegerField(
        default=0,
        help_text=_("Minimum advance notice required"),
    )
    min_advance_unit = models.CharField(
        max_length=10,
        choices=ADVANCE_UNITS,
        default="hour",
    )
    max_advance = models.PositiveIntegerField(
        default=365,
        help_text=_("Maximum advance booking window"),
    )
    max_advance_unit = models.CharField(
        max_length=10,
        choices=ADVANCE_UNITS,
        default="day",
    )

    # Capacity
    max_bookings_per_slot = models.PositiveIntegerField(
        default=1,
        help_text=_("Maximum simultaneous bookings per time slot"),
    )

    # Confirmation
    confirmation_required = models.BooleanField(
        default=False,
        help_text=_("Require manual confirmation (vs auto-confirm)"),
    )

    # Cancellation
    cancellation_allowed = models.BooleanField(default=True)
    cancellation_deadline = models.PositiveIntegerField(
        default=24,
        help_text=_("Cancellation deadline before booking start"),
    )
    cancellation_deadline_unit = models.CharField(
        max_length=10,
        choices=CANCELLATION_UNITS,
        default="hour",
    )

    # Display
    calendar_display = models.CharField(
        max_length=20,
        choices=CALENDAR_DISPLAY,
        default="calendar",
        help_text=_("How customers select booking dates"),
    )

    # Timezone
    customer_timezone_enabled = models.BooleanField(
        default=False,
        help_text=_("Show times in customer timezone"),
    )

    # Deposits (beyond WooCommerce)
    deposit_enabled = models.BooleanField(default=False)
    deposit_type = models.CharField(
        max_length=15,
        choices=DEPOSIT_TYPES,
        default="percentage",
        blank=True,
    )
    deposit_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text=_("Fixed amount or percentage for deposit"),
    )

    # Accommodation-specific
    check_in_time = models.TimeField(
        null=True,
        blank=True,
        help_text=_("Check-in time (accommodation only)"),
    )
    check_out_time = models.TimeField(
        null=True,
        blank=True,
        help_text=_("Check-out time (accommodation only)"),
    )
    standard_occupancy = models.PositiveIntegerField(
        default=2,
        help_text=_("Number of guests included in the base nightly rate"),
    )
    max_occupancy = models.PositiveIntegerField(
        default=0,
        help_text=_("Maximum total guests across all person types. 0 = no limit."),
    )
    min_stay = models.PositiveIntegerField(
        default=1,
        help_text=_("Minimum number of nights"),
    )
    max_stay = models.PositiveIntegerField(
        default=365,
        help_text=_("Maximum number of nights"),
    )

    # Recurring bookings (beyond WooCommerce)
    recurrence_enabled = models.BooleanField(
        default=False,
        help_text=_("Allow recurring booking schedules"),
    )

    # Reminder settings
    reminder_enabled = models.BooleanField(default=True)
    reminder_hours_before = models.JSONField(
        default=list,
        blank=True,
        help_text=_("List of hours before booking to send reminders, e.g. [1, 24, 168]"),
    )

    class Meta:
        verbose_name = _("Booking Configuration")
        verbose_name_plural = _("Booking Configurations")

    def __str__(self):
        return f"Booking Config: {self.product.name}"


class BookingResource(models.Model):
    """
    A bookable resource: staff member, room, equipment, vehicle, etc.

    Resources can have their own availability rules and are optionally
    selected by the customer or auto-assigned.
    """

    RESOURCE_TYPES = [
        ("staff", _("Staff Member")),
        ("room", _("Room")),
        ("equipment", _("Equipment")),
        ("vehicle", _("Vehicle")),
        ("generic", _("Generic Resource")),
    ]

    ASSIGNMENT_TYPES = [
        ("customer_selected", _("Customer Selects")),
        ("automatic", _("Auto-Assigned")),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="booking_resources",
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    resource_type = models.CharField(
        max_length=20,
        choices=RESOURCE_TYPES,
        default="generic",
    )
    quantity = models.PositiveIntegerField(
        default=1,
        help_text=_("Available units of this resource"),
    )
    base_cost_adjustment = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text=_("Price adjustment when this resource is selected"),
    )
    assignment_type = models.CharField(
        max_length=20,
        choices=ASSIGNMENT_TYPES,
        default="customer_selected",
    )
    email = models.EmailField(
        blank=True,
        default="",
        help_text=_("Email for staff (calendar sync + notifications)"),
    )
    tags = models.JSONField(
        default=list,
        blank=True,
        help_text=_('Skills/tags for automatic matching, e.g. ["Spanish", "Advanced"]'),
    )
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_per_night = models.BooleanField(
        default=True,
        help_text=_("If true, cost adjustment is applied per night (accommodation)"),
    )

    class Meta:
        verbose_name = _("Booking Resource")
        verbose_name_plural = _("Booking Resources")
        ordering = ["sort_order", "name"]

    def __str__(self):
        return f"{self.name} ({self.get_resource_type_display()})"

    @property
    def primary_image(self):
        return (
            self.images.filter(is_primary=True).select_related("media_asset").first()
            or self.images.select_related("media_asset").first()
        )


class BookingResourceImage(models.Model):
    """Image/video for a booking resource (room photo, equipment image, etc.)"""

    resource = models.ForeignKey(
        BookingResource,
        on_delete=models.CASCADE,
        related_name="images",
    )
    media_asset = models.ForeignKey(
        "media_library.MediaAsset",
        on_delete=models.PROTECT,
        related_name="booking_resource_uses",
    )
    alt_text = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["position", "id"]
        verbose_name = _("Booking Resource Image")
        verbose_name_plural = _("Booking Resource Images")

    def __str__(self):
        return f"Image for {self.resource.name}"

    @property
    def image_url(self):
        return self.media_asset.get_display_url()

    @property
    def thumbnail_small(self):
        return self.media_asset.get_thumbnail("small")

    @property
    def thumbnail_medium(self):
        return self.media_asset.get_thumbnail("medium")

    def save(self, *args, **kwargs):
        if self.is_primary:
            BookingResourceImage.objects.filter(resource=self.resource, is_primary=True).exclude(
                pk=self.pk
            ).update(is_primary=False)
        super().save(*args, **kwargs)


class BookingPersonType(models.Model):
    """
    Person type for group bookings with per-person pricing.

    Example: Adult ($50), Child ($25), Senior ($40)
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="booking_person_types",
    )
    name = models.CharField(
        max_length=100,
        help_text=_("e.g., Adult, Child, Senior"),
    )
    cost_adjustment = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text=_("Per-person price modifier"),
    )
    min_persons = models.PositiveIntegerField(default=0)
    max_persons = models.PositiveIntegerField(default=10)
    is_counted_for_capacity = models.BooleanField(
        default=True,
        help_text=_("Count this person type against slot capacity"),
    )
    is_per_night = models.BooleanField(
        default=True,
        help_text=_("If true, cost_adjustment is charged per night (accommodation)"),
    )
    sort_order = models.IntegerField(default=0)

    class Meta:
        verbose_name = _("Booking Person Type")
        verbose_name_plural = _("Booking Person Types")
        ordering = ["sort_order", "name"]

    def __str__(self):
        return f"{self.name} ({'+' if self.cost_adjustment >= 0 else ''}{self.cost_adjustment})"


class BookingAvailabilityRule(models.Model):
    """
    Availability and pricing rules for booking products.

    Rules define when a product is bookable, blocked, or has custom pricing.
    Rules can apply to the product overall or to a specific resource.
    Higher priority rules override lower priority ones.
    """

    RULE_TYPES = [
        ("available", _("Available")),
        ("unavailable", _("Unavailable")),
        ("custom_cost", _("Custom Cost")),
    ]

    SCOPE_TYPES = [
        ("all_dates", _("All Dates")),
        ("date_range", _("Date Range")),
        ("days_of_week", _("Days of Week")),
        ("time_range", _("Time Range")),
        ("specific_dates", _("Specific Dates")),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="booking_availability_rules",
    )
    resource = models.ForeignKey(
        BookingResource,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="availability_rules",
        help_text=_("If set, rule applies to this resource only"),
    )

    rule_type = models.CharField(max_length=15, choices=RULE_TYPES, default="available")
    scope = models.CharField(max_length=20, choices=SCOPE_TYPES, default="all_dates")

    # Date range scope
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    # Time range scope
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    # Days of week scope (0=Monday, 6=Sunday)
    days_of_week = models.JSONField(
        default=list,
        blank=True,
        help_text=_("List of day numbers (0=Mon, 6=Sun)"),
    )

    # Specific dates scope
    specific_dates = models.JSONField(
        default=list,
        blank=True,
        help_text=_("List of specific date strings (YYYY-MM-DD)"),
    )

    # Cost overrides (for custom_cost rule type)
    cost_override = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Replace base cost entirely"),
    )
    cost_adjustment = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Add/subtract from base cost"),
    )
    cost_adjustment_type = models.CharField(
        max_length=10,
        choices=[("flat", _("Flat Amount")), ("percentage", _("Percentage"))],
        default="flat",
        help_text=_("How cost_adjustment is applied"),
    )

    # Min stay override for this rule's date scope
    min_stay_override = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text=_("Override minimum stay for dates matching this rule"),
    )

    # Length-of-stay discount
    length_of_stay_min = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text=_("Minimum nights for length-of-stay discount to apply"),
    )
    length_of_stay_discount_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Percentage discount for stays >= min nights"),
    )

    # Lead-time pricing (early-bird / last-minute)
    lead_time_min_days = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text=_("Minimum days before check-in for this rule to apply"),
    )
    lead_time_max_days = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text=_("Maximum days before check-in for this rule to apply"),
    )

    priority = models.IntegerField(
        default=10,
        help_text=_("Higher priority rules override lower (default 10)"),
    )

    class Meta:
        verbose_name = _("Booking Availability Rule")
        verbose_name_plural = _("Booking Availability Rules")
        ordering = ["-priority", "start_date"]

    def __str__(self):
        return f"{self.get_rule_type_display()} - {self.get_scope_display()} (priority {self.priority})"


class BookingRecurrenceRule(models.Model):
    """
    Recurring booking schedule rule (beyond WooCommerce).

    Defines repeating availability patterns like "every Monday 9am-5pm"
    or "first Saturday of month 10am-2pm".
    """

    FREQUENCY_CHOICES = [
        ("daily", _("Daily")),
        ("weekly", _("Weekly")),
        ("biweekly", _("Every Two Weeks")),
        ("monthly", _("Monthly")),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="booking_recurrence_rules",
    )

    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default="weekly")
    day_of_week = models.IntegerField(
        null=True,
        blank=True,
        help_text=_("Day of week (0=Mon, 6=Sun) for weekly/biweekly"),
    )
    day_of_month = models.IntegerField(
        null=True,
        blank=True,
        help_text=_("Day of month (1-31) for monthly"),
    )
    start_time = models.TimeField()
    end_time = models.TimeField()

    # Recurrence window
    start_date = models.DateField(
        help_text=_("Recurrence starts from this date"),
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        help_text=_("Recurrence ends on this date (null = ongoing)"),
    )

    auto_create_days_ahead = models.PositiveIntegerField(
        default=90,
        help_text=_("How many days ahead to generate bookable slots"),
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Booking Recurrence Rule")
        verbose_name_plural = _("Booking Recurrence Rules")

    def __str__(self):
        return f"{self.get_frequency_display()} {self.start_time}-{self.end_time}"


class Booking(models.Model):
    """
    An actual booking reservation record.

    Created when a customer completes checkout for a booking product.
    """

    BOOKING_STATUSES = [
        ("pending_confirmation", _("Pending Confirmation")),
        ("confirmed", _("Confirmed")),
        ("cancelled", _("Cancelled")),
        ("completed", _("Completed")),
        ("no_show", _("No Show")),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    resource = models.ForeignKey(
        BookingResource,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookings",
    )
    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookings",
    )
    order_item = models.ForeignKey(
        "orders.OrderItem",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookings",
    )
    customer = models.ForeignKey(
        "accounts.CustomerProfile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookings",
    )

    # Booking details
    start_datetime = models.DateTimeField(db_index=True)
    end_datetime = models.DateTimeField(db_index=True)
    status = models.CharField(
        max_length=25,
        choices=BOOKING_STATUSES,
        default="pending_confirmation",
        db_index=True,
    )

    # Person counts
    persons = models.JSONField(
        default=dict,
        blank=True,
        help_text=_('Person counts by type, e.g. {"Adult": 2, "Child": 1}'),
    )

    # Pricing
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_breakdown = models.JSONField(
        default=dict,
        blank=True,
        help_text=_("Itemized price breakdown at time of booking"),
    )

    # Customer info
    customer_name = models.CharField(max_length=255, blank=True, default="")
    customer_email = models.EmailField(blank=True, default="")
    customer_phone = models.CharField(max_length=50, blank=True, default="")
    customer_notes = models.TextField(blank=True, default="")
    customer_timezone = models.CharField(max_length=50, blank=True, default="")

    # Cancellation
    cancellation_reason = models.TextField(blank=True, default="")

    # Calendar sync
    ical_uid = models.CharField(
        max_length=255,
        blank=True,
        default="",
        db_index=True,
        help_text=_("iCal UID for calendar sync"),
    )

    # Reminders
    reminder_sent_at = models.DateTimeField(null=True, blank=True)

    # Recurring bookings (beyond WooCommerce)
    is_recurring = models.BooleanField(default=False)
    recurrence_group_id = models.UUIDField(
        null=True,
        blank=True,
        db_index=True,
        help_text=_("Links recurring bookings together"),
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Booking")
        verbose_name_plural = _("Bookings")
        ordering = ["-start_datetime"]
        indexes = [
            models.Index(fields=["product", "start_datetime", "status"]),
            models.Index(fields=["status", "start_datetime"]),
        ]

    def __str__(self):
        return f"Booking #{self.pk} - {self.product.name} ({self.start_datetime.strftime('%Y-%m-%d %H:%M')})"

    @property
    def duration_minutes(self):
        """Duration of booking in minutes."""
        delta = self.end_datetime - self.start_datetime
        return int(delta.total_seconds() / 60)

    @property
    def is_upcoming(self):
        """Whether booking is in the future."""
        from django.utils import timezone as tz

        return self.start_datetime > tz.now()

    @property
    def is_cancellable(self):
        """Check if booking can still be cancelled based on deadline."""
        from datetime import timedelta

        from django.utils import timezone as tz

        if self.status in ("cancelled", "completed", "no_show"):
            return False

        try:
            config = self.product.booking_config
        except BookingConfig.DoesNotExist:
            return False

        if not config.cancellation_allowed:
            return False

        deadline_hours = config.cancellation_deadline
        if config.cancellation_deadline_unit == "day":
            deadline_hours *= 24
        elif config.cancellation_deadline_unit == "week":
            deadline_hours *= 168

        return tz.now() + timedelta(hours=deadline_hours) < self.start_datetime


class BookingWaitlist(models.Model):
    """
    Waitlist for fully-booked slots (beyond WooCommerce).

    When a slot opens up (cancellation), waitlisted customers are notified
    automatically in order.
    """

    WAITLIST_STATUSES = [
        ("waiting", _("Waiting")),
        ("notified", _("Notified")),
        ("booked", _("Converted to Booking")),
        ("expired", _("Expired")),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="booking_waitlist",
    )
    customer = models.ForeignKey(
        "accounts.CustomerProfile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="booking_waitlist_entries",
    )

    customer_email = models.EmailField()
    customer_name = models.CharField(max_length=255, blank=True, default="")

    desired_date = models.DateField()
    desired_time_start = models.TimeField(null=True, blank=True)
    desired_time_end = models.TimeField(null=True, blank=True)
    desired_persons = models.JSONField(
        default=dict,
        blank=True,
        help_text=_("Desired person counts by type"),
    )

    status = models.CharField(
        max_length=10,
        choices=WAITLIST_STATUSES,
        default="waiting",
    )
    notified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Booking Waitlist Entry")
        verbose_name_plural = _("Booking Waitlist Entries")
        ordering = ["created_at"]

    def __str__(self):
        return f"Waitlist: {self.customer_email} for {self.product.name} on {self.desired_date}"


class BookingNote(models.Model):
    """
    Audit trail and notes for bookings.

    Tracks manual notes, status changes, reschedules, system events,
    and email notifications. Used to display an activity timeline on
    the booking change form.
    """

    NOTE_TYPES = [
        ("manual", _("Manual Note")),
        ("status_change", _("Status Change")),
        ("reschedule", _("Reschedule")),
        ("system", _("System")),
        ("email", _("Email Sent")),
    ]

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="booking_notes",
    )
    author = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="booking_notes",
    )

    note = models.TextField(help_text=_("Note content"))
    note_type = models.CharField(
        max_length=20,
        choices=NOTE_TYPES,
        default="manual",
    )
    is_customer_visible = models.BooleanField(
        default=False,
        help_text=_("Whether this note is visible to the customer"),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Booking Note")
        verbose_name_plural = _("Booking Notes")
        indexes = [
            models.Index(fields=["booking", "-created_at"]),
        ]

    def __str__(self):
        author_name = self.author.get_full_name() if self.author else "System"
        return f"{self.get_note_type_display()} by {author_name} on Booking #{self.booking_id}"


class BookingSlotReservation(models.Model):
    """
    Temporary hold on a booking slot while the customer is in checkout.

    Similar to StockReservation - uses TTL pattern with Celery cleanup.
    Default TTL: 30 minutes for web, 15 minutes for POS.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="booking_slot_reservations",
    )
    resource = models.ForeignKey(
        BookingResource,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="slot_reservations",
    )
    cart_item = models.ForeignKey(
        "cart.CartItem",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="booking_slot_reservations",
    )

    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    persons = models.JSONField(default=dict, blank=True)

    expires_at = models.DateTimeField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Booking Slot Reservation")
        verbose_name_plural = _("Booking Slot Reservations")
        indexes = [
            models.Index(fields=["product", "start_datetime", "end_datetime"]),
        ]

    def __str__(self):
        return f"Slot hold: {self.product.name} {self.start_datetime.strftime('%Y-%m-%d %H:%M')}"

    @property
    def is_expired(self):
        from django.utils import timezone as tz

        return tz.now() > self.expires_at


# ============================================================================
# SIGNALS
# ============================================================================

from django.db.models.signals import m2m_changed
from django.dispatch import receiver


@receiver(m2m_changed, sender=ProductVariant.selected_attributes.through)
def auto_assign_attributes(sender, instance, action, pk_set, **kwargs):
    """
    Automatically create ProductAttributeAssignment when attributes are added to variants.

    When a merchant adds attribute values to a variant, this signal:
    1. Creates ProductAttributeAssignment if it doesn't exist
    2. Adds the attribute value to allowed_values

    This eliminates the manual step of managing ProductAttributeAssignment.
    """
    if action == "post_add" and pk_set:
        # Get the variant and its product
        variant = instance
        product = variant.product

        # Get all AttributeValue objects that were added
        attr_values = AttributeValue.objects.filter(pk__in=pk_set).select_related("attribute")

        for attr_value in attr_values:
            # Get or create ProductAttributeAssignment for this attribute
            assignment, created = ProductAttributeAssignment.objects.get_or_create(
                product=product, attribute=attr_value.attribute, defaults={"sort_order": 0}
            )

            # Add this value to allowed_values if not already there
            if not assignment.allowed_values.filter(pk=attr_value.pk).exists():
                assignment.allowed_values.add(attr_value)
