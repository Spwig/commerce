"""
DRF Serializers for Catalog API
Includes multi-language support via translations JSONField
"""

from django.db.models import Avg
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from core.utils import get_default_currency

from .models import (
    AttributeValue,
    Brand,
    BundleItem,
    Category,
    Collection,
    CompatibilityRule,
    ConfigurationPreset,
    ConfigurationSlot,
    ConfigurationSlotOption,
    CustomizationOption,
    GiftCard,
    GiftCardTransaction,
    Product,
    ProductAttribute,
    ProductImage,
    ProductReview,
    ProductVariant,
    Warehouse,
)
from .serializer_mixins import TranslatedFieldsMixin, TranslationAwareSerializer


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for product images"""

    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = [
            "id",
            "image",
            "alt_text",
            "is_primary",
            "position",
            "show_in_gallery",
            "show_in_listing",
        ]

    def get_image(self, obj) -> str | None:
        """Get image URL from MediaAsset (returns relative URL for cross-origin safety)"""
        if obj.media_asset and obj.media_asset.original_file:
            return obj.media_asset.get_display_url()
        return None


class WarehouseSerializer(serializers.ModelSerializer):
    """Serializer for warehouse locations"""

    supports_pickup = serializers.SerializerMethodField()

    class Meta:
        model = Warehouse
        fields = [
            "id",
            "name",
            "code",
            "address_line1",
            "address_line2",
            "city",
            "state_province",
            "postal_code",
            "country",
            "latitude",
            "longitude",
            "contact_phone",
            "supports_pickup",
        ]

    def get_supports_pickup(self, obj) -> bool:
        """Check if warehouse supports customer pickup"""
        return obj.shipping_location is not None


class StockAvailabilitySerializer(serializers.Serializer):
    """Serializer for product stock availability at a specific warehouse"""

    warehouse = WarehouseSerializer(read_only=True)
    on_hand = serializers.IntegerField()
    allocated = serializers.IntegerField()
    available = serializers.IntegerField()
    low_stock_threshold = serializers.IntegerField()
    is_low_stock = serializers.SerializerMethodField()
    is_in_stock = serializers.SerializerMethodField()

    def get_is_low_stock(self, obj) -> bool:
        """Check if stock is low"""
        threshold = obj.get("low_stock_threshold", 0)
        if threshold > 0:
            return obj.get("available", 0) <= threshold
        return False

    def get_is_in_stock(self, obj) -> bool:
        """Check if item is in stock"""
        return obj.get("available", 0) > 0


class AttributeValueSerializer(serializers.ModelSerializer):
    """Serializer for attribute values (e.g., Small, Medium, Red, Blue)"""

    attribute_name = serializers.CharField(source="attribute.name", read_only=True)
    attribute_slug = serializers.CharField(source="attribute.slug", read_only=True)
    attribute_type = serializers.CharField(source="attribute.type", read_only=True)

    class Meta:
        model = AttributeValue
        fields = [
            "id",
            "value",
            "slug",
            "attribute_name",
            "attribute_slug",
            "attribute_type",
            "color_hex",
            "sort_order",
        ]


class ProductAttributeSerializer(serializers.ModelSerializer):
    """Serializer for product attributes (Size, Color, Material, etc.) with nested values"""

    values = AttributeValueSerializer(many=True, read_only=True)
    value_count = serializers.SerializerMethodField()

    class Meta:
        model = ProductAttribute
        fields = [
            "id",
            "name",
            "slug",
            "type",
            "is_required",
            "sort_order",
            "values",
            "value_count",
        ]

    def get_value_count(self, obj) -> int:
        """Get count of values for this attribute"""
        return obj.values.count()


class CustomizationOptionSerializer(serializers.ModelSerializer):
    """
    Serializer for product customization options.
    Shows available customization options with pricing and validation rules.
    """

    price_amount = serializers.DecimalField(
        source="price_amount.amount", max_digits=10, decimal_places=2, read_only=True
    )
    price_currency = serializers.CharField(source="price_amount.currency.code", read_only=True)
    option_type_display = serializers.CharField(source="get_option_type_display", read_only=True)
    pricing_type_display = serializers.CharField(source="get_pricing_type_display", read_only=True)

    class Meta:
        model = CustomizationOption
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "option_type",
            "option_type_display",
            "is_required",
            "sort_order",
            "max_length",
            "allowed_file_types",
            "max_file_size_mb",
            "min_value",
            "max_value",
            "pricing_type",
            "pricing_type_display",
            "price_amount",
            "price_currency",
            "choices",
        ]


class ProductVariantSerializer(serializers.ModelSerializer):
    """Serializer for product variants with structured attribute support"""

    # Pricing fields
    effective_price = serializers.SerializerMethodField()
    price_amount = serializers.DecimalField(
        source="price.amount", max_digits=10, decimal_places=2, read_only=True, allow_null=True
    )
    price_currency = serializers.CharField(
        source="price.currency.code", read_only=True, allow_null=True
    )

    # Structured attributes
    attributes_structured = AttributeValueSerializer(
        source="selected_attributes", many=True, read_only=True
    )

    # Stock information
    stock_quantity = serializers.SerializerMethodField()

    # Image from MediaAsset
    image_url = serializers.SerializerMethodField()

    # Variant gallery images
    images = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "name",
            "sku",
            "pricing_strategy",
            "price_amount",
            "price_currency",
            "effective_price",
            "attributes_structured",
            "stock_quantity",
            "image_url",
            "images",
            "color_swatch",
            "is_active",
        ]

    def get_effective_price(self, obj) -> dict:
        """Get the effective price considering pricing strategy"""
        price = obj.get_effective_price()
        return {"amount": str(price.amount), "currency": price.currency.code}

    def get_stock_quantity(self, obj) -> int:
        """Get total stock across all warehouses"""
        return obj.get_stock_quantity()

    def get_image_url(self, obj) -> str | None:
        """Get primary image URL for this variant (medium thumbnail)"""
        if obj.image_asset and obj.image_asset.original_file:
            return obj.image_asset.get_thumbnail("medium") or obj.image_asset.get_display_url()
        # Try first variant image
        first_img = obj.images.first()
        if first_img and first_img.media_asset and first_img.media_asset.original_file:
            return (
                first_img.media_asset.get_thumbnail("medium")
                or first_img.media_asset.get_display_url()
            )
        # Fallback to deprecated image field
        if obj.image:
            return obj.image.url
        return None

    def get_images(self, obj) -> list:
        """Get all variant gallery images"""
        variant_images = obj.images.select_related("media_asset").order_by("position")
        result = []
        for vi in variant_images:
            if vi.media_asset and vi.media_asset.original_file:
                result.append(
                    {
                        "id": vi.id,
                        "image": vi.media_asset.get_display_url(),
                        "alt_text": vi.alt_text or "",
                    }
                )
        return result


class BundleItemSerializer(serializers.ModelSerializer):
    """
    Serializer for bundle components.
    Shows product/variant details and pricing for each item in a bundle.
    """

    component_product = serializers.SerializerMethodField()
    component_variant = serializers.SerializerMethodField()
    component_price = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    in_stock = serializers.SerializerMethodField()
    available_variants = serializers.SerializerMethodField()
    requires_selection = serializers.SerializerMethodField()

    class Meta:
        model = BundleItem
        fields = [
            "id",
            "component_product",
            "component_variant",
            "quantity",
            "sort_order",
            "is_optional",
            "allow_variant_selection",
            "component_price",
            "total_price",
            "in_stock",
            "available_variants",
            "requires_selection",
        ]

    def get_component_product(self, obj) -> dict:
        """Get basic product info for bundle component"""
        product = obj.component_product
        return {
            "id": product.id,
            "name": product.name,
            "slug": product.slug,
            "sku": product.sku,
            "product_type": product.product_type,
            "is_digital": product.is_digital,
        }

    def get_component_variant(self, obj) -> dict | None:
        """Get variant info if component is a variant"""
        if not obj.component_variant:
            return None

        variant = obj.component_variant
        return {
            "id": variant.id,
            "name": variant.name,
            "sku": variant.sku,
            "attributes": AttributeValueSerializer(
                variant.selected_attributes.all(), many=True
            ).data,
        }

    def get_component_price(self, obj) -> dict:
        """Get the price of this component"""
        price = obj.get_component_price()
        return {"amount": str(price.amount), "currency": price.currency.code}

    def get_total_price(self, obj) -> dict:
        """Get total price (quantity × component price)"""
        from djmoney.money import Money

        total = Money(obj.get_total_price(), obj.bundle.price.currency)
        return {"amount": str(total.amount), "currency": total.currency.code}

    def get_in_stock(self, obj) -> bool:
        """Check if component is in stock"""
        return obj.check_stock_availability()

    def get_available_variants(self, obj) -> list | None:
        """
        Get available variants for customer selection.
        Only populated when allow_variant_selection is True.
        """
        if not obj.allow_variant_selection:
            return None

        product = obj.component_product
        if product.product_type != "variable":
            return None

        variants = product.variants.filter(is_active=True)
        result = []

        for variant in variants:
            # Check stock availability for the variant
            in_stock = variant.stock_quantity > 0 if hasattr(variant, "stock_quantity") else True

            result.append(
                {
                    "id": variant.id,
                    "name": variant.name,
                    "sku": variant.sku,
                    "price": {
                        "amount": str(variant.price.amount),
                        "currency": variant.price.currency.code,
                    }
                    if variant.price
                    else None,
                    "attributes": AttributeValueSerializer(
                        variant.selected_attributes.all(), many=True
                    ).data,
                    "in_stock": in_stock,
                }
            )

        return result

    def get_requires_selection(self, obj) -> bool:
        """
        Check if customer must select a variant for this component.
        True if allow_variant_selection is enabled and product is variable.
        """
        if not obj.allow_variant_selection:
            return False

        product = obj.component_product
        return product.product_type == "variable"


class CategoryListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for category lists"""

    product_count = serializers.SerializerMethodField()
    full_path = extend_schema_field(serializers.CharField())(serializers.ReadOnlyField())
    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "icon",
            "image",
            "parent",
            "full_path",
            "product_count",
            "is_featured",
            "sort_order",
        ]

    def get_product_count(self, obj) -> int:
        """Count products in category and subcategories"""
        return obj.products.filter(status="published").count()

    def get_image(self, obj) -> str | None:
        """Get image URL from MediaAsset"""
        return obj.get_image_url()


class CategoryDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for category pages with translation support"""

    product_count = serializers.SerializerMethodField()
    subcategories = CategoryListSerializer(source="children", many=True, read_only=True)
    full_path = extend_schema_field(serializers.CharField())(serializers.ReadOnlyField())
    effective_theme = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    banner_image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "icon",
            "image",
            "banner_image",
            "parent",
            "full_path",
            "page_template",
            "products_per_page",
            "show_subcategories",
            "meta_title",
            "meta_description",
            "product_count",
            "subcategories",
            "effective_theme",
            "is_featured",
        ]

    def get_product_count(self, obj) -> int:
        return obj.products.filter(status="published").count()

    def get_effective_theme(self, obj) -> dict | None:
        """Get effective theme including inheritance"""
        return obj.get_effective_theme()

    def get_image(self, obj) -> str | None:
        """Get image URL from MediaAsset"""
        return obj.get_image_url()

    def get_banner_image(self, obj) -> str | None:
        """Get banner image URL from MediaAsset"""
        return obj.get_banner_url()

    def to_representation(self, instance):
        """Apply translations for name, description, and SEO fields."""
        data = super().to_representation(instance)
        request = self.context.get("request")
        if request:
            lang = getattr(request, "LANGUAGE_CODE", None)
            if lang and (instance.translations or {}):
                trans = instance.translations.get(lang, {})
                if trans:
                    for field in ("name", "description", "meta_title", "meta_description"):
                        value = trans.get(field)
                        if value:
                            data[field] = value
        return data


class BrandSerializer(serializers.ModelSerializer):
    """Serializer for brands"""

    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Brand
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "logo",
            "banner_image",
            "website",
            "brand_story",
            "meta_title",
            "meta_description",
            "is_featured",
            "product_count",
        ]

    def get_product_count(self, obj) -> int:
        return obj.products.filter(status="published").count()


class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for product listings"""

    category_name = serializers.CharField(source="category.name", read_only=True)
    brand_name = serializers.CharField(source="brand.name", read_only=True, allow_null=True)
    primary_image = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    price_amount = serializers.DecimalField(
        source="price.amount", max_digits=10, decimal_places=2, read_only=True
    )
    price_currency = serializers.CharField(source="price.currency.code", read_only=True)
    compare_at_price_amount = serializers.DecimalField(
        source="compare_at_price.amount",
        max_digits=10,
        decimal_places=2,
        read_only=True,
        allow_null=True,
    )
    discount_percentage = extend_schema_field(serializers.FloatField())(serializers.ReadOnlyField())
    is_in_stock = extend_schema_field(serializers.BooleanField())(serializers.ReadOnlyField())
    is_low_stock = extend_schema_field(serializers.BooleanField())(serializers.ReadOnlyField())
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "sku",
            "product_type",
            "category_name",
            "brand_name",
            "primary_image",
            "images",
            "price_amount",
            "price_currency",
            "compare_at_price_amount",
            "discount_percentage",
            "is_in_stock",
            "is_low_stock",
            "is_featured",
            "average_rating",
            "review_count",
            "views_count",
            "sales_count",
        ]

    def get_primary_image(self, obj) -> dict | None:
        """Get primary image or first image"""
        primary = obj.images.filter(is_primary=True, show_in_listing=True).first()
        if not primary:
            primary = obj.images.filter(show_in_listing=True).first()

        if primary:
            return {
                "url": primary.media_asset.get_display_url() if primary.media_asset else None,
                "alt_text": primary.alt_text,
            }
        return None

    def get_images(self, obj) -> list:
        """Get product images with thumbnails for cart/mini-cart"""
        images = obj.images.filter(show_in_listing=True).order_by("-is_primary", "position")[:1]
        result = []
        for img in images:
            if img.media_asset:
                result.append(
                    {
                        "id": img.id,
                        "thumbnail_url": img.media_asset.get_thumbnail("small")
                        if hasattr(img.media_asset, "get_thumbnail")
                        else img.media_asset.get_display_url(),
                        "image_url": img.media_asset.get_display_url(),
                        "url": img.media_asset.original_file.url
                        if img.media_asset.original_file
                        else "",
                        "alt_text": img.alt_text or "",
                    }
                )
        return result

    def get_average_rating(self, obj) -> float | None:
        """Calculate average rating from reviews"""
        avg = obj.reviews.filter(is_approved=True).aggregate(Avg("rating"))["rating__avg"]
        return round(avg, 1) if avg else None

    def get_review_count(self, obj) -> int:
        """Count approved reviews"""
        return obj.reviews.filter(is_approved=True).count()


class ProductDetailSerializer(
    TranslatedFieldsMixin, TranslationAwareSerializer, serializers.ModelSerializer
):
    """Detailed serializer for product pages with multi-language support"""

    category = CategoryListSerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    customization_options = CustomizationOptionSerializer(many=True, read_only=True)

    price_amount = serializers.DecimalField(
        source="price.amount", max_digits=10, decimal_places=2, read_only=True
    )
    price_currency = serializers.CharField(source="price.currency.code", read_only=True)
    compare_at_price_amount = serializers.DecimalField(
        source="compare_at_price.amount",
        max_digits=10,
        decimal_places=2,
        read_only=True,
        allow_null=True,
    )
    cost_amount = serializers.DecimalField(
        source="cost.amount", max_digits=10, decimal_places=2, read_only=True, allow_null=True
    )

    discount_percentage = extend_schema_field(serializers.FloatField())(serializers.ReadOnlyField())
    is_in_stock = extend_schema_field(serializers.BooleanField())(serializers.ReadOnlyField())
    is_low_stock = extend_schema_field(serializers.BooleanField())(serializers.ReadOnlyField())

    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    rating_distribution = serializers.SerializerMethodField()

    related_products = serializers.SerializerMethodField()
    effective_design = serializers.SerializerMethodField()

    # Variable product fields (NEW)
    available_attributes = serializers.SerializerMethodField()
    variant_count = serializers.SerializerMethodField()

    # Bundle product fields (NEW)
    bundle_items = BundleItemSerializer(many=True, read_only=True)
    bundle_component_total = serializers.SerializerMethodField()
    effective_bundle_price = serializers.SerializerMethodField()
    bundle_savings = serializers.SerializerMethodField()

    # Multi-location inventory fields
    stock_availability = serializers.SerializerMethodField()
    regional_stock = serializers.SerializerMethodField()
    pickup_locations = serializers.SerializerMethodField()

    # Translated fields from translations JSON
    description = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    meta_title = serializers.SerializerMethodField()
    meta_description = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "sku",
            "product_type",
            "category",
            "brand",
            "description",
            "short_description",
            "features",
            "specifications",
            "price_amount",
            "price_currency",
            "compare_at_price_amount",
            "cost_amount",
            "discount_percentage",
            "track_inventory",
            "low_stock_threshold",
            "allow_backorders",
            "is_in_stock",
            "is_low_stock",
            "weight",
            "length",
            "width",
            "height",
            "gallery_type",
            "show_related_products",
            "show_reviews",
            "show_specifications",
            "product_sections",
            "is_featured",
            "is_digital",
            "meta_title",
            "meta_description",
            "views_count",
            "sales_count",
            "average_rating",
            "review_count",
            "rating_distribution",
            "images",
            "variants",
            "available_attributes",
            "variant_count",
            "allow_customization",
            "customization_options",
            "bundle_items",
            "bundle_pricing_strategy",
            "bundle_discount_percentage",
            "bundle_component_total",
            "effective_bundle_price",
            "bundle_savings",
            "gift_card_denomination_type",
            "gift_card_denominations",
            "gift_card_min_amount",
            "gift_card_max_amount",
            "gift_card_expires_days",
            "gift_card_currency",
            "related_products",
            "effective_design",
            "stock_availability",
            "regional_stock",
            "pickup_locations",
            "created_at",
            "updated_at",
        ]

    def get_average_rating(self, obj) -> float | None:
        """Calculate average rating"""
        avg = obj.reviews.filter(is_approved=True).aggregate(Avg("rating"))["rating__avg"]
        return round(avg, 1) if avg else None

    def get_review_count(self, obj) -> int:
        """Count approved reviews"""
        return obj.reviews.filter(is_approved=True).count()

    def get_rating_distribution(self, obj) -> dict:
        """Get rating distribution (1-5 stars)"""
        distribution = {}
        for rating in range(1, 6):
            count = obj.reviews.filter(is_approved=True, rating=rating).count()
            distribution[str(rating)] = count
        return distribution

    def get_related_products(self, obj) -> list:
        """Get related products (same category, different product)"""
        if not obj.show_related_products:
            return []

        related = (
            Product.objects.filter(category=obj.category, status="published")
            .exclude(id=obj.id)
            .exclude(sales_channel="pos_only")[:6]
        )

        return ProductListSerializer(related, many=True, context=self.context).data

    def get_effective_design(self, obj) -> dict | None:
        """Get effective design settings"""
        return obj.get_effective_design()

    def get_available_attributes(self, obj) -> list:
        """
        Get product attributes with allowed values for variation selector.
        Only returns attributes assigned to this product.
        """
        from .models import ProductAttributeAssignment

        assignments = (
            ProductAttributeAssignment.objects.filter(product=obj)
            .select_related("attribute")
            .prefetch_related("allowed_values__attribute")
            .order_by("sort_order")
        )

        attributes = []
        for assignment in assignments:
            attribute_data = {
                "id": assignment.attribute.id,
                "name": assignment.attribute.name,
                "slug": assignment.attribute.slug,
                "type": assignment.attribute.type,
                "is_required": assignment.attribute.is_required,
                "values": [],
            }

            for value in assignment.allowed_values.all().order_by("sort_order"):
                attribute_data["values"].append(
                    {
                        "id": value.id,
                        "value": value.value,
                        "slug": value.slug,
                        "color_hex": value.color_hex or None,
                    }
                )

            attributes.append(attribute_data)

        return attributes

    def get_variant_count(self, obj) -> int:
        """Get count of active variants"""
        return obj.variants.filter(is_active=True).count()

    def get_bundle_component_total(self, obj) -> dict | None:
        """Get sum of all bundle component prices"""
        if obj.product_type != "bundle":
            return None

        total = obj.get_bundle_component_total()
        if not total:
            return None

        return {"amount": str(total.amount), "currency": total.currency.code}

    def get_effective_bundle_price(self, obj) -> dict | None:
        """Get effective bundle price based on pricing strategy"""
        if obj.product_type != "bundle":
            return None

        price = obj.get_effective_bundle_price()
        return {"amount": str(price.amount), "currency": price.currency.code}

    def get_bundle_savings(self, obj) -> dict | None:
        """Calculate savings on bundle vs buying components separately"""
        if obj.product_type != "bundle":
            return None

        component_total = obj.get_bundle_component_total()
        bundle_price = obj.get_effective_bundle_price()

        if not component_total or component_total.amount == 0:
            return None

        savings = component_total - bundle_price
        if savings.amount <= 0:
            return None

        percentage = (savings.amount / component_total.amount) * 100

        return {
            "amount": str(savings.amount),
            "currency": savings.currency.code,
            "percentage": round(float(percentage), 1),
        }

    def get_description(self, obj) -> str | None:
        """Get translated description from translations JSON"""
        return self.get_translated_description(obj)

    def get_short_description(self, obj) -> str | None:
        """Get translated short description from translations JSON"""
        return self.get_translated_short_description(obj)

    def get_meta_title(self, obj) -> str | None:
        """Get translated meta title from translations JSON"""
        return self.get_translated_meta_title(obj)

    def get_meta_description(self, obj) -> str | None:
        """Get translated meta description from translations JSON"""
        return self.get_translated_meta_description(obj)

    def get_stock_availability(self, obj) -> list:
        """
        Get detailed stock availability for all warehouses.
        Returns list of warehouse stock information.
        """
        if not obj.track_inventory:
            return []

        stock_items = (
            obj.stock_items.select_related("warehouse")
            .filter(warehouse__is_active=True)
            .order_by("-warehouse__fulfillment_priority")
        )

        availability = []
        for stock_item in stock_items:
            availability.append(
                {
                    "warehouse": WarehouseSerializer(stock_item.warehouse).data,
                    "on_hand": stock_item.on_hand,
                    "allocated": stock_item.allocated,
                    "available": stock_item.available,
                    "low_stock_threshold": stock_item.low_stock_threshold
                    or obj.low_stock_threshold,
                }
            )

        return availability

    def get_regional_stock(self, obj) -> dict | None:
        """
        Get total available stock in the customer's region.
        Returns None if no region detected or product doesn't track inventory.
        """
        if not obj.track_inventory:
            return {"available": True, "quantity": None, "message": "In Stock"}

        # Get region from request
        request = self.context.get("request")
        region = getattr(request, "sales_region", None) if request else None

        if not region:
            # No region detected - show global stock
            total_available = sum(
                item.available for item in obj.stock_items.filter(warehouse__is_active=True)
            )
            return {
                "available": total_available > 0,
                "quantity": total_available,
                "message": f"{total_available} available"
                if total_available > 0
                else "Out of Stock",
            }

        # Calculate regional stock
        regional_stock = obj.stock_items.filter(warehouse__region=region, warehouse__is_active=True)

        total_available = sum(item.available for item in regional_stock)

        return {
            "region_name": region.name,
            "region_code": region.code,
            "available": total_available > 0,
            "quantity": total_available,
            "message": f"{total_available} available in {region.name}"
            if total_available > 0
            else f"Currently unavailable in {region.name}",
        }

    def get_pickup_locations(self, obj) -> list:
        """
        Get warehouses that support customer pickup and have stock.
        Only includes warehouses linked to shipping locations.
        """
        if not obj.track_inventory:
            # For non-inventory products, show all pickup locations
            pickup_warehouses = Warehouse.objects.filter(
                is_active=True, shipping_location__isnull=False
            ).select_related("shipping_location")

            return [
                {
                    "warehouse": WarehouseSerializer(wh).data,
                    "in_stock": True,
                    "available_quantity": None,
                }
                for wh in pickup_warehouses
            ]

        # For inventory-tracked products, only show locations with stock
        stock_items = (
            obj.stock_items.select_related("warehouse", "warehouse__shipping_location")
            .filter(
                warehouse__is_active=True,
                warehouse__shipping_location__isnull=False,  # Only warehouses that support pickup
                on_hand__gt=0,  # Has physical stock
            )
            .order_by("-warehouse__fulfillment_priority")
        )

        pickup_locations = []
        for stock_item in stock_items:
            pickup_locations.append(
                {
                    "warehouse": WarehouseSerializer(stock_item.warehouse).data,
                    "in_stock": stock_item.available > 0,
                    "available_quantity": stock_item.available,
                }
            )

        return pickup_locations


class ProductReviewSerializer(serializers.ModelSerializer):
    """Serializer for product reviews"""

    user_name = serializers.CharField(source="user.username", read_only=True)
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = ProductReview
        fields = [
            "id",
            "product",
            "product_name",
            "user",
            "user_name",
            "rating",
            "title",
            "comment",
            "is_verified_purchase",
            "is_approved",
            "helpful_count",
            "images",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["user", "is_verified_purchase", "is_approved", "helpful_count"]

    def validate_rating(self, value):
        """Validate rating is between 1 and 5"""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value

    def validate(self, data):
        """Validate that user hasn't already reviewed this product"""
        request = self.context.get("request")
        if request and request.method == "POST":
            product = data.get("product")
            if ProductReview.objects.filter(product=product, user=request.user).exists():
                raise serializers.ValidationError(
                    {"detail": "You have already reviewed this product"}
                )
        return data

    def create(self, validated_data):
        """Create review with current user"""
        request = self.context.get("request")
        validated_data["user"] = request.user

        # Check if user has purchased this product (verified purchase)
        # This will be implemented when Orders app is ready
        # For now, set to False
        validated_data["is_verified_purchase"] = False

        return super().create(validated_data)


class CollectionSerializer(serializers.ModelSerializer):
    """Serializer for collections"""

    product_count = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()

    class Meta:
        model = Collection
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "collection_type",
            "image",
            "banner_image",
            "meta_title",
            "meta_description",
            "is_featured",
            "sort_order",
            "product_count",
            "products",
        ]

    def get_product_count(self, obj) -> int:
        """Count products in collection"""
        if obj.collection_type == "manual":
            return obj.products.filter(status="published").count()
        else:
            # For automatic collections, apply criteria
            # This is a placeholder - full implementation would parse auto_criteria
            return obj.products.filter(status="published").count()

    def get_products(self, obj) -> list | None:
        """Get collection products"""
        # Only include products in detail view
        if self.context.get("include_products", False):
            products = obj.products.filter(status="published")[:24]
            return ProductListSerializer(products, many=True, context=self.context).data
        return None


class GiftCardTransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for gift card transactions.
    Provides transaction history for gift cards.
    """

    transaction_type_display = serializers.CharField(
        source="get_transaction_type_display", read_only=True
    )
    amount = serializers.SerializerMethodField()
    balance_after = serializers.SerializerMethodField()
    order_number = serializers.SerializerMethodField()

    class Meta:
        model = GiftCardTransaction
        fields = [
            "id",
            "transaction_type",
            "transaction_type_display",
            "amount",
            "balance_after",
            "order_number",
            "notes",
            "created_at",
        ]
        read_only_fields = fields

    @extend_schema_field(
        {
            "type": "object",
            "properties": {"amount": {"type": "string"}, "currency": {"type": "string"}},
        }
    )
    def get_amount(self, obj) -> dict:
        """Get transaction amount with currency"""
        return {"amount": str(obj.amount.amount), "currency": obj.amount.currency.code}

    @extend_schema_field(
        {
            "type": "object",
            "properties": {"amount": {"type": "string"}, "currency": {"type": "string"}},
        }
    )
    def get_balance_after(self, obj) -> dict:
        """Get balance after transaction"""
        return {
            "amount": str(obj.balance_after.amount),
            "currency": obj.balance_after.currency.code,
        }

    @extend_schema_field({"type": "string", "nullable": True})
    def get_order_number(self, obj) -> str | None:
        """Get order number if associated with order"""
        if obj.order:
            return obj.order.order_number
        return None


class GiftCardSerializer(serializers.ModelSerializer):
    """
    Serializer for gift cards.
    Provides full gift card details including balance and transaction history.
    """

    initial_value = serializers.SerializerMethodField()
    current_balance = serializers.SerializerMethodField()
    product_name = serializers.CharField(source="product.name", read_only=True)
    status = serializers.SerializerMethodField()
    transactions = GiftCardTransactionSerializer(many=True, read_only=True)

    class Meta:
        model = GiftCard
        fields = [
            "id",
            "code",
            "product_name",
            "initial_value",
            "current_balance",
            "recipient_email",
            "recipient_name",
            "sender_name",
            "message",
            "is_active",
            "expires_at",
            "status",
            "created_at",
            "issued_at",
            "first_used_at",
            "transactions",
        ]
        read_only_fields = [
            "id",
            "code",
            "initial_value",
            "current_balance",
            "created_at",
            "issued_at",
            "first_used_at",
            "transactions",
        ]

    @extend_schema_field(
        {
            "type": "object",
            "properties": {"amount": {"type": "string"}, "currency": {"type": "string"}},
        }
    )
    def get_initial_value(self, obj) -> dict:
        """Get initial gift card value"""
        return {
            "amount": str(obj.initial_value.amount),
            "currency": obj.initial_value.currency.code,
        }

    @extend_schema_field(
        {
            "type": "object",
            "properties": {"amount": {"type": "string"}, "currency": {"type": "string"}},
        }
    )
    def get_current_balance(self, obj) -> dict:
        """Get current gift card balance"""
        return {
            "amount": str(obj.current_balance.amount),
            "currency": obj.current_balance.currency.code,
        }

    @extend_schema_field({"type": "object"})
    def get_status(self, obj) -> dict:
        """Get gift card status information"""
        return {
            "is_valid": obj.is_valid,
            "is_expired": obj.is_expired,
            "is_fully_redeemed": obj.is_fully_redeemed,
            "redemption_percentage": round(obj.redemption_percentage, 2),
        }


class GiftCardBalanceCheckSerializer(serializers.Serializer):
    """
    Serializer for checking gift card balance without authentication.
    Used for public balance check endpoint.
    """

    code = serializers.CharField(
        max_length=50, required=True, help_text=_("Gift card code to check")
    )
    current_balance = serializers.SerializerMethodField(read_only=True)
    initial_value = serializers.SerializerMethodField(read_only=True)
    is_valid = serializers.BooleanField(read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    expires_at = serializers.DateTimeField(read_only=True)
    redemption_percentage = serializers.FloatField(read_only=True)

    def validate_code(self, value):
        """Validate that gift card exists"""
        try:
            gift_card = GiftCard.objects.get(code=value)
            self.context["gift_card"] = gift_card
            return value
        except GiftCard.DoesNotExist:
            raise serializers.ValidationError("Invalid gift card code")

    @extend_schema_field(
        {
            "type": "object",
            "properties": {"amount": {"type": "string"}, "currency": {"type": "string"}},
        }
    )
    def get_current_balance(self, obj) -> dict:
        """Get current balance"""
        gift_card = self.context.get("gift_card")
        if gift_card:
            return {
                "amount": str(gift_card.current_balance.amount),
                "currency": gift_card.current_balance.currency.code,
            }
        return {"amount": "0", "currency": get_default_currency()}

    @extend_schema_field(
        {
            "type": "object",
            "properties": {"amount": {"type": "string"}, "currency": {"type": "string"}},
        }
    )
    def get_initial_value(self, obj) -> dict:
        """Get initial value"""
        gift_card = self.context.get("gift_card")
        if gift_card:
            return {
                "amount": str(gift_card.initial_value.amount),
                "currency": gift_card.initial_value.currency.code,
            }
        return {"amount": "0", "currency": get_default_currency()}


class GiftCardPurchaseSerializer(serializers.Serializer):
    """
    Serializer for purchasing a gift card.
    Validates denomination and recipient information.
    """

    product_id = serializers.IntegerField(required=True, help_text=_("Gift card product ID"))
    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        help_text=_("Custom amount (if allowed by product)"),
    )
    denomination = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, help_text=_("Fixed denomination choice")
    )
    recipient_email = serializers.EmailField(
        required=True, help_text=_("Email to send gift card to")
    )
    recipient_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    sender_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    message = serializers.CharField(
        required=False, allow_blank=True, help_text=_("Personal message")
    )
    quantity = serializers.IntegerField(default=1, min_value=1, max_value=10)

    def validate(self, data):
        """Validate gift card purchase data"""
        from decimal import Decimal

        # Get product
        try:
            product = Product.objects.get(id=data["product_id"], product_type="gift_card")
        except Product.DoesNotExist:
            raise serializers.ValidationError({"product_id": "Invalid gift card product"})

        # Validate denomination vs custom amount
        if product.gift_card_denomination_type == "fixed":
            # Must select from fixed denominations
            if "denomination" not in data:
                raise serializers.ValidationError({"denomination": "Please select a denomination"})

            # Validate denomination is in allowed list
            allowed = [Decimal(str(d)) for d in product.gift_card_denominations]
            if data["denomination"] not in allowed:
                raise serializers.ValidationError(
                    {
                        "denomination": f"Invalid denomination. Allowed values: {product.gift_card_denominations}"
                    }
                )

            data["final_amount"] = data["denomination"]

        elif product.gift_card_denomination_type == "custom":
            # Must provide custom amount
            if "amount" not in data:
                raise serializers.ValidationError({"amount": "Please enter an amount"})

            # Validate min/max
            if product.gift_card_min_amount and data["amount"] < product.gift_card_min_amount:
                raise serializers.ValidationError(
                    {"amount": f"Minimum amount is {product.gift_card_min_amount}"}
                )

            if product.gift_card_max_amount and data["amount"] > product.gift_card_max_amount:
                raise serializers.ValidationError(
                    {"amount": f"Maximum amount is {product.gift_card_max_amount}"}
                )

            data["final_amount"] = data["amount"]

        elif product.gift_card_denomination_type == "both":
            # Can use either denomination or custom amount
            if "denomination" in data:
                allowed = [Decimal(str(d)) for d in product.gift_card_denominations]
                if data["denomination"] not in allowed:
                    raise serializers.ValidationError(
                        {
                            "denomination": f"Invalid denomination. Allowed values: {product.gift_card_denominations}"
                        }
                    )
                data["final_amount"] = data["denomination"]
            elif "amount" in data:
                if product.gift_card_min_amount and data["amount"] < product.gift_card_min_amount:
                    raise serializers.ValidationError(
                        {"amount": f"Minimum amount is {product.gift_card_min_amount}"}
                    )
                if product.gift_card_max_amount and data["amount"] > product.gift_card_max_amount:
                    raise serializers.ValidationError(
                        {"amount": f"Maximum amount is {product.gift_card_max_amount}"}
                    )
                data["final_amount"] = data["amount"]
            else:
                raise serializers.ValidationError(
                    "Please provide either a denomination or custom amount"
                )

        data["product"] = product
        return data


# ── Configurator Serializers ──────────────────────────────────────────────────


class ConfigurationSlotOptionSerializer(TranslationAwareSerializer, serializers.ModelSerializer):
    """Serializer for options available within a configuration slot."""

    product_name = serializers.CharField(source="option_product.name", read_only=True)
    product_slug = serializers.CharField(source="option_product.slug", read_only=True)
    product_sku = serializers.CharField(source="option_product.sku", read_only=True)
    product_image = serializers.SerializerMethodField()
    effective_price = serializers.SerializerMethodField()
    variant_name = serializers.CharField(source="option_variant.name", read_only=True, default=None)
    variant_id = serializers.IntegerField(source="option_variant_id", read_only=True)
    in_stock = serializers.SerializerMethodField()

    class Meta:
        model = ConfigurationSlotOption
        fields = [
            "id",
            "product_name",
            "product_slug",
            "product_sku",
            "product_image",
            "variant_name",
            "variant_id",
            "allow_variant_selection",
            "effective_price",
            "price_adjustment",
            "is_default",
            "is_popular",
            "sort_order",
            "compatibility_tags",
            "quantity",
            "in_stock",
        ]

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_product_image(self, obj) -> str | None:
        first_image = obj.option_product.images.first()
        if first_image and first_image.media_asset:
            return first_image.media_asset.get_display_url()
        return None

    @extend_schema_field(serializers.DecimalField(max_digits=10, decimal_places=2))
    def get_effective_price(self, obj):
        """Return the effective price for this option based on the configurable product's pricing strategy."""
        product = obj.slot.product
        strategy = product.configurator_pricing_strategy

        if strategy == "base_plus_adjustments":
            adj = obj.price_adjustment
            return str(adj.amount) if adj else "0.00"
        else:
            # components_sum or fixed — show the component's own price
            if obj.option_variant:
                price = obj.option_variant.get_price()
            else:
                price = obj.option_product.price
            return str(price.amount) if price else "0.00"

    @extend_schema_field(serializers.BooleanField())
    def get_in_stock(self, obj) -> bool:
        product = obj.option_product
        if obj.option_variant:
            stock = product.stock_items.filter(variant=obj.option_variant).first()
            if stock:
                return stock.available > 0
        total = sum(s.available for s in product.stock_items.all())
        return total > 0


class ConfigurationSlotSerializer(TranslationAwareSerializer, serializers.ModelSerializer):
    """Serializer for a configuration slot with its nested options."""

    options = ConfigurationSlotOptionSerializer(many=True, read_only=True)

    class Meta:
        model = ConfigurationSlot
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "icon",
            "is_required",
            "min_selections",
            "max_selections",
            "sort_order",
            "options",
        ]
        translated_fields = ["name", "description"]


class CompatibilityRuleSerializer(serializers.ModelSerializer):
    """Serializer for compatibility rules between slot options."""

    compatible_option_ids = serializers.SerializerMethodField()

    class Meta:
        model = CompatibilityRule
        fields = [
            "id",
            "rule_type",
            "source_option",
            "target_slot",
            "compatible_option_ids",
        ]

    @extend_schema_field(serializers.ListField(child=serializers.IntegerField()))
    def get_compatible_option_ids(self, obj) -> list:
        return list(obj.compatible_options.values_list("id", flat=True))


class ConfigurationPresetSerializer(TranslationAwareSerializer, serializers.ModelSerializer):
    """Serializer for pre-built configuration presets."""

    image_url = serializers.SerializerMethodField()
    calculated_price = serializers.SerializerMethodField()

    class Meta:
        model = ConfigurationPreset
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "image_url",
            "selections",
            "is_featured",
            "sort_order",
            "calculated_price",
        ]
        translated_fields = ["name", "description"]

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_image_url(self, obj) -> str | None:
        if obj.image_asset and obj.image_asset.original_file:
            return obj.image_asset.get_display_url()
        return None

    @extend_schema_field(serializers.DecimalField(max_digits=10, decimal_places=2))
    def get_calculated_price(self, obj):
        """Calculate the total price for this preset's selections."""
        from cart.services.cart_service import CartService

        product = obj.product
        resolved_options = []

        for _slot_id_str, option_ids in (obj.selections or {}).items():
            for option_id in option_ids:
                try:
                    option = ConfigurationSlotOption.objects.select_related(
                        "option_product", "option_variant"
                    ).get(pk=option_id)
                    resolved_options.append((option, option.option_variant))
                except ConfigurationSlotOption.DoesNotExist:
                    continue

        if resolved_options:
            price = CartService._calculate_configurable_price(product, resolved_options)
            return str(price.amount)
        return "0.00"


class ConfiguratorDataSerializer(serializers.Serializer):
    """Full configurator data payload for the frontend wizard."""

    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    product_slug = serializers.CharField()
    pricing_strategy = serializers.CharField()
    base_price = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True)
    currency = serializers.CharField()
    slots = ConfigurationSlotSerializer(many=True)
    rules = CompatibilityRuleSerializer(many=True)
    presets = ConfigurationPresetSerializer(many=True)


class ConfigurationSelectionSerializer(serializers.Serializer):
    """Input serializer for configuration validation and price calculation."""

    configuration = serializers.DictField(
        child=serializers.ListField(child=serializers.IntegerField()),
        help_text=_("Mapping of slot_id to list of selected option_ids"),
    )
    preset_id = serializers.IntegerField(required=False, allow_null=True)


class ConfiguratorValidationResponseSerializer(serializers.Serializer):
    """Response serializer for configuration validation."""

    valid = serializers.BooleanField()
    errors = serializers.ListField(child=serializers.CharField(), required=False)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    currency = serializers.CharField(required=False)
    price_breakdown = serializers.DictField(required=False)


class ConfiguratorPriceResponseSerializer(serializers.Serializer):
    """Response serializer for price calculation."""

    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField()
    pricing_strategy = serializers.CharField()
    slot_subtotals = serializers.DictField(
        child=serializers.DecimalField(max_digits=10, decimal_places=2),
        help_text=_("Price subtotal per slot"),
    )
