"""
Catalog Sync Serializer

Handles export/import of product catalog models (full_migration only):
- ProductAttribute: Attribute type definitions (Size, Color, etc.)
- AttributeValue: Attribute value options (S, M, L, Red, Blue, etc.)
- Category: Product category hierarchy with self-referencing parent
- Brand: Brand definitions with logo/banner images
- Product: Product records with pricing, inventory, and metadata
- ProductVariant: SKU-level variant data with attribute selections
- ProductImage: Product images linked via MediaAsset
- ProductAttributeAssignment: Links attributes to products with allowed values
- BundleItem: Bundle product composition

Only active products (is_deleted=False) are exported.
MoneyFields (price, cost) are serialized as separate amount/currency pairs.
MediaAsset references are exported inline with file data.
"""
import logging
from decimal import Decimal, InvalidOperation

from django.db import transaction

from .base import CollectionSyncSerializer
from ..file_handler import export_file_field, import_file_field

logger = logging.getLogger(__name__)

# -- Field constants --

PRODUCT_ATTRIBUTE_FIELDS = [
    'name', 'slug', 'type', 'is_required',
    'sort_order', 'translations',
]

ATTRIBUTE_VALUE_FIELDS = [
    'value', 'slug', 'color_hex',
    'sort_order', 'translations',
]

CATEGORY_FIELDS = [
    'name', 'slug', 'description', 'external_id', 'icon',
    'products_per_page', 'show_subcategories', 'page_template',
    'cascade_theme_to_children', 'cascade_theme_to_products',
    'out_of_stock_action_override', 'allow_backorders_override',
    'meta_title', 'meta_description', 'seo_auto_generated',
    'translations',
    'is_active', 'is_featured', 'sort_order',
    'custom_fields',
    'template_variant', 'css_classes', 'layout_config',
    'style_overrides', 'responsive_config', 'inherit_parent_theme',
]

BRAND_FIELDS = [
    'name', 'slug', 'description', 'external_id',
    'website', 'show_brand_page', 'brand_story',
    'meta_title', 'meta_description', 'seo_auto_generated',
    'is_active', 'is_featured',
    'template_variant', 'css_classes', 'layout_config',
    'style_overrides', 'responsive_config', 'inherit_parent_theme',
]

BRAND_FILE_FIELDS = ['logo', 'banner_image']

PRODUCT_FIELDS = [
    'name', 'slug', 'sku', 'product_type', 'external_id',
    'short_description', 'full_description', 'translations',
    'meta_title', 'meta_description', 'seo_auto_generated',
    'features', 'specifications',
    'sale_type', 'sale_value', 'sale_start_date', 'sale_end_date',
    'pricing_strategy',
    'bundle_pricing_strategy', 'bundle_discount_percentage',
    'gift_card_denomination_type', 'gift_card_denominations',
    'gift_card_min_amount', 'gift_card_max_amount',
    'gift_card_expires_days', 'gift_card_currency',
    'allow_customization', 'customization_preview_template',
    'configurator_pricing_strategy',
    'is_subscription_enabled', 'allow_one_time_purchase',
    'subscription_default',
    'track_inventory', 'low_stock_threshold', 'allow_backorders',
    'out_of_stock_action_override',
    'is_preorder', 'preorder_release_date', 'preorder_message',
    'weight', 'length', 'width', 'height',
    'gtin', 'ean', 'upc', 'isbn', 'asin', 'mpn',
    'hs_code', 'country_of_origin', 'unit_price_for_customs',
    'export_license_number', 'export_license_expiry',
    'page_template', 'gallery_type',
    'show_related_products', 'show_reviews', 'show_specifications',
    'product_sections',
    'status', 'is_featured', 'is_digital', 'hide_from_storefront',
    'default_license_type', 'default_max_activations',
    'default_validity_days', 'requires_license',
    'license_generation_trigger',
    'sales_channel', 'barcode',
    'custom_fields',
    'template_variant', 'css_classes', 'layout_config',
    'style_overrides', 'responsive_config', 'inherit_parent_theme',
]

PRODUCT_MONEY_FIELDS = ['price', 'cost', 'configurator_base_price']

PRODUCT_ATTRIBUTE_ASSIGNMENT_FIELDS = ['sort_order']

PRODUCT_VARIANT_FIELDS = [
    'name', 'sku', 'external_id', 'pricing_strategy',
    'weight', 'length', 'width', 'height',
    'barcode', 'color_swatch', 'is_active',
    'template_variant', 'css_classes', 'layout_config',
    'style_overrides', 'responsive_config', 'inherit_parent_theme',
]

PRODUCT_IMAGE_FIELDS = [
    'alt_text', 'is_primary', 'position',
    'show_in_gallery', 'show_in_listing',
]

BUNDLE_ITEM_FIELDS = [
    'quantity', 'sort_order', 'is_optional', 'allow_variant_selection',
]


# -- MoneyField helpers --

def _serialize_money_field(data, instance, field_name):
    """Serialize a MoneyField as separate amount string + currency code."""
    money_obj = getattr(instance, field_name, None)
    if money_obj is not None and hasattr(money_obj, 'amount'):
        data[f'_{field_name}_amount'] = str(money_obj.amount)
        data[f'_{field_name}_currency'] = str(
            getattr(instance, f'{field_name}_currency', '')
        )
    else:
        data[f'_{field_name}_amount'] = None
        data[f'_{field_name}_currency'] = None


def _deserialize_money_field(instance, item, field_name):
    """Restore a MoneyField from serialized amount + currency."""
    amount_str = item.get(f'_{field_name}_amount')
    currency = item.get(f'_{field_name}_currency')
    if amount_str is not None and currency:
        try:
            setattr(instance, field_name, Decimal(amount_str))
            setattr(instance, f'{field_name}_currency', currency)
        except (InvalidOperation, ValueError) as e:
            logger.warning("Invalid money value for %s: %s", field_name, e)
    else:
        # Nullable MoneyField — clear it
        try:
            setattr(instance, field_name, None)
            setattr(instance, f'{field_name}_currency', '')
        except (ValueError, TypeError):
            pass


# -- MediaAsset helpers --

def _export_media_asset_meta(asset):
    """Extract portable metadata from a MediaAsset for inline export."""
    return {
        'title': asset.title,
        'alt_text': asset.alt_text,
        'description': asset.description,
        'mime_type': asset.mime_type,
        'width': asset.width,
        'height': asset.height,
        'focal_point_x': asset.focal_point_x,
        'focal_point_y': asset.focal_point_y,
    }


def _import_media_asset_inline(meta, files, file_key):
    """Create a new MediaAsset from inline file data + metadata."""
    from media_library.models import MediaAsset

    file_data = files.get(file_key)
    if not file_data:
        return None

    asset = MediaAsset(
        title=meta.get('title', 'Imported'),
        alt_text=meta.get('alt_text', ''),
        description=meta.get('description', ''),
        mime_type=meta.get('mime_type', 'image/jpeg'),
        width=meta.get('width'),
        height=meta.get('height'),
        focal_point_x=meta.get('focal_point_x', 0.5),
        focal_point_y=meta.get('focal_point_y', 0.5),
        file_size=file_data.get('size', 0),
        is_public=True,
    )
    if import_file_field(asset, 'original_file', file_data):
        asset.save()
        return asset
    return None


class CatalogSerializer(CollectionSyncSerializer):
    """Serializer for the full product catalog (full_migration only).

    Models handled (9 total):
        - ProductAttribute: Attribute type definitions
        - AttributeValue: Attribute value options
        - Category: Product category hierarchy
        - Brand: Brand definitions with files
        - Product: Full product records
        - ProductAttributeAssignment: Attribute-product links
        - ProductVariant: SKU-level variant data
        - ProductImage: Product images via MediaAsset
        - BundleItem: Bundle product composition

    Import order follows dependency chain:
    Attributes → Values → Categories → Brands → Products →
    Assignments → Variants → Images → BundleItems
    """

    category_key = 'catalog'
    natural_key_fields = ['sku']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from catalog.models import Product
        self.model_class = Product

    def get_count(self):
        from catalog.models import (
            Category, Brand, Product, ProductVariant, ProductImage,
            ProductAttribute, AttributeValue, ProductAttributeAssignment,
            BundleItem,
        )
        return (
            ProductAttribute.objects.count()
            + AttributeValue.objects.count()
            + Category.objects.count()
            + Brand.objects.count()
            + Product.objects.count()
            + ProductAttributeAssignment.objects.count()
            + ProductVariant.objects.count()
            + ProductImage.objects.count()
            + BundleItem.objects.count()
        )

    # -- Export --

    def export(self, credential_mode='redact'):
        from catalog.models import (
            Category, Brand, Product, ProductVariant, ProductImage,
            ProductAttribute, AttributeValue, ProductAttributeAssignment,
            BundleItem,
        )

        items = []
        files = {}

        # 1. ProductAttribute
        for attr in ProductAttribute.objects.all():
            data = {f: getattr(attr, f) for f in PRODUCT_ATTRIBUTE_FIELDS}
            data['_source_pk'] = attr.pk
            data['_model'] = 'ProductAttribute'
            items.append(data)

        # 2. AttributeValue
        for val in AttributeValue.objects.select_related('attribute').all():
            data = {f: getattr(val, f) for f in ATTRIBUTE_VALUE_FIELDS}
            data['_source_pk'] = val.pk
            data['_model'] = 'AttributeValue'
            data['_attribute_slug'] = val.attribute.slug
            items.append(data)

        # 3. Category
        for cat in Category.objects.select_related(
            'parent', 'image_asset', 'banner_asset'
        ).all():
            data = {f: getattr(cat, f) for f in CATEGORY_FIELDS}
            data['_source_pk'] = cat.pk
            data['_model'] = 'Category'
            data['_parent_slug'] = cat.parent.slug if cat.parent else None
            # Inline MediaAsset for image_asset
            if cat.image_asset:
                data['_image_asset_meta'] = _export_media_asset_meta(
                    cat.image_asset
                )
                fd = export_file_field(cat.image_asset, 'original_file')
                if fd:
                    files[f'Category:{cat.slug}:image_asset'] = fd
            # Inline MediaAsset for banner_asset
            if cat.banner_asset:
                data['_banner_asset_meta'] = _export_media_asset_meta(
                    cat.banner_asset
                )
                fd = export_file_field(cat.banner_asset, 'original_file')
                if fd:
                    files[f'Category:{cat.slug}:banner_asset'] = fd
            items.append(data)

        # 4. Brand
        for brand in Brand.objects.all():
            data = {f: getattr(brand, f) for f in BRAND_FIELDS}
            data['_source_pk'] = brand.pk
            data['_model'] = 'Brand'
            items.append(data)
            for ff in BRAND_FILE_FIELDS:
                fd = export_file_field(brand, ff)
                if fd:
                    files[f'Brand:{brand.slug}:{ff}'] = fd

        # 5. Product (active only via default manager)
        for product in Product.objects.select_related(
            'category', 'brand'
        ).all():
            data = {f: getattr(product, f) for f in PRODUCT_FIELDS}
            data['_source_pk'] = product.pk
            data['_model'] = 'Product'
            data['_category_slug'] = product.category.slug
            data['_brand_slug'] = (
                product.brand.slug if product.brand else None
            )
            for mf in PRODUCT_MONEY_FIELDS:
                _serialize_money_field(data, product, mf)
            data['_subscription_plan_slugs'] = list(
                product.subscription_plans.values_list('slug', flat=True)
            )
            items.append(data)

        # 6. ProductAttributeAssignment
        for assign in ProductAttributeAssignment.objects.select_related(
            'product', 'attribute'
        ).prefetch_related('allowed_values').all():
            data = {
                f: getattr(assign, f)
                for f in PRODUCT_ATTRIBUTE_ASSIGNMENT_FIELDS
            }
            data['_source_pk'] = assign.pk
            data['_model'] = 'ProductAttributeAssignment'
            data['_product_sku'] = assign.product.sku
            data['_attribute_slug'] = assign.attribute.slug
            data['_allowed_value_slugs'] = list(
                assign.allowed_values.values_list('slug', flat=True)
            )
            items.append(data)

        # 7. ProductVariant
        for variant in ProductVariant.objects.select_related(
            'product', 'image_asset'
        ).prefetch_related(
            'selected_attributes__attribute'
        ).all():
            data = {f: getattr(variant, f) for f in PRODUCT_VARIANT_FIELDS}
            data['_source_pk'] = variant.pk
            data['_model'] = 'ProductVariant'
            data['_product_sku'] = variant.product.sku
            _serialize_money_field(data, variant, 'price')
            data['_selected_attributes'] = [
                {
                    'attribute_slug': av.attribute.slug,
                    'value_slug': av.slug,
                }
                for av in variant.selected_attributes.select_related(
                    'attribute'
                ).all()
            ]
            if variant.image_asset:
                data['_image_asset_meta'] = _export_media_asset_meta(
                    variant.image_asset
                )
                fd = export_file_field(
                    variant.image_asset, 'original_file'
                )
                if fd:
                    files[f'ProductVariant:{variant.sku}:image_asset'] = fd
            items.append(data)

        # 8. ProductImage
        for img in ProductImage.objects.select_related(
            'product', 'media_asset'
        ).all():
            data = {f: getattr(img, f) for f in PRODUCT_IMAGE_FIELDS}
            data['_source_pk'] = img.pk
            data['_model'] = 'ProductImage'
            data['_product_sku'] = img.product.sku
            if img.media_asset:
                data['_media_asset_meta'] = _export_media_asset_meta(
                    img.media_asset
                )
                fd = export_file_field(img.media_asset, 'original_file')
                if fd:
                    files[
                        f'ProductImage:{img.product.sku}:'
                        f'{img.position}:media_asset'
                    ] = fd
            items.append(data)

        # 9. BundleItem
        for bi in BundleItem.objects.select_related(
            'bundle', 'component_product', 'component_variant'
        ).all():
            data = {f: getattr(bi, f) for f in BUNDLE_ITEM_FIELDS}
            data['_source_pk'] = bi.pk
            data['_model'] = 'BundleItem'
            data['_bundle_sku'] = bi.bundle.sku
            data['_component_product_sku'] = bi.component_product.sku
            data['_component_variant_sku'] = (
                bi.component_variant.sku if bi.component_variant else None
            )
            items.append(data)

        return {
            'category': self.category_key,
            'sync_type': 'collection',
            'items': items,
            'total': len(items),
            'files': files,
        }

    # -- Import --

    def import_data(self, data, dry_run=False, sync_mode='additive'):
        if dry_run:
            return self.generate_diff(data)

        items = data.get('items', [])
        files = data.get('files', {})
        synced = 0
        skipped = 0
        failed = 0
        deleted = 0
        errors = []

        try:
            with transaction.atomic():
                # Separate items by model type
                attributes = [
                    i for i in items
                    if i.get('_model') == 'ProductAttribute'
                ]
                attr_values = [
                    i for i in items
                    if i.get('_model') == 'AttributeValue'
                ]
                categories = [
                    i for i in items if i.get('_model') == 'Category'
                ]
                brands = [
                    i for i in items if i.get('_model') == 'Brand'
                ]
                products = [
                    i for i in items if i.get('_model') == 'Product'
                ]
                assignments = [
                    i for i in items
                    if i.get('_model') == 'ProductAttributeAssignment'
                ]
                variants = [
                    i for i in items
                    if i.get('_model') == 'ProductVariant'
                ]
                images = [
                    i for i in items
                    if i.get('_model') == 'ProductImage'
                ]
                bundle_items_list = [
                    i for i in items if i.get('_model') == 'BundleItem'
                ]

                # Pass 1: ProductAttribute
                for item in attributes:
                    try:
                        with transaction.atomic():
                            self._import_product_attribute(item)
                        synced += 1
                    except Exception as e:
                        failed += 1
                        errors.append(
                            f"ProductAttribute '{item.get('slug', '?')}': {e}"
                        )

                # Pass 2: AttributeValue
                for item in attr_values:
                    try:
                        with transaction.atomic():
                            self._import_attribute_value(item)
                        synced += 1
                    except Exception as e:
                        failed += 1
                        errors.append(
                            f"AttributeValue '{item.get('slug', '?')}': {e}"
                        )

                # Pass 3a: Category (create/update without parent)
                for item in categories:
                    try:
                        with transaction.atomic():
                            self._import_category(item, files)
                        synced += 1
                    except Exception as e:
                        failed += 1
                        errors.append(
                            f"Category '{item.get('slug', '?')}': {e}"
                        )

                # Pass 3b: Set category parents
                for item in categories:
                    if item.get('_parent_slug'):
                        try:
                            with transaction.atomic():
                                self._set_category_parent(item)
                        except Exception as e:
                            errors.append(
                                f"Category parent "
                                f"'{item.get('slug', '?')}': {e}"
                            )

                # Pass 4: Brand
                for item in brands:
                    try:
                        with transaction.atomic():
                            self._import_brand(item, files)
                        synced += 1
                    except Exception as e:
                        failed += 1
                        errors.append(
                            f"Brand '{item.get('slug', '?')}': {e}"
                        )

                # Pass 5: Product
                for item in products:
                    try:
                        with transaction.atomic():
                            self._import_product(item)
                        synced += 1
                    except Exception as e:
                        failed += 1
                        errors.append(
                            f"Product '{item.get('sku', '?')}': {e}"
                        )

                # Pass 6: ProductAttributeAssignment
                for item in assignments:
                    try:
                        with transaction.atomic():
                            self._import_attribute_assignment(item)
                        synced += 1
                    except Exception as e:
                        failed += 1
                        errors.append(
                            f"AttrAssignment "
                            f"'{item.get('_product_sku', '?')}/"
                            f"{item.get('_attribute_slug', '?')}': {e}"
                        )

                # Pass 7: ProductVariant
                for item in variants:
                    try:
                        with transaction.atomic():
                            self._import_product_variant(item, files)
                        synced += 1
                    except Exception as e:
                        failed += 1
                        errors.append(
                            f"ProductVariant '{item.get('sku', '?')}': {e}"
                        )

                # Pass 8: ProductImage
                for item in images:
                    try:
                        with transaction.atomic():
                            self._import_product_image(item, files)
                        synced += 1
                    except Exception as e:
                        failed += 1
                        errors.append(
                            f"ProductImage "
                            f"'{item.get('_product_sku', '?')}' "
                            f"pos {item.get('position', '?')}: {e}"
                        )

                # Pass 9: BundleItem
                for item in bundle_items_list:
                    try:
                        with transaction.atomic():
                            self._import_bundle_item(item)
                        synced += 1
                    except Exception as e:
                        failed += 1
                        errors.append(
                            f"BundleItem '{item.get('_bundle_sku', '?')}' "
                            f"-> '{item.get('_component_product_sku', '?')}"
                            f"': {e}"
                        )

                # Mirror mode
                if sync_mode == 'mirror':
                    deleted = self._delete_absent(items)

        except Exception as e:
            logger.error("Catalog import failed: %s", e)
            return {
                'synced': 0, 'skipped': 0, 'failed': 1,
                'errors': [str(e)],
            }

        result = {
            'synced': synced, 'skipped': skipped,
            'failed': failed, 'errors': errors,
        }
        if sync_mode == 'mirror':
            result['deleted'] = deleted
        return result

    # -- Per-model import helpers --

    def _import_product_attribute(self, item):
        from catalog.models import ProductAttribute

        existing = ProductAttribute.objects.filter(
            slug=item['slug']
        ).first()
        if existing:
            for f in PRODUCT_ATTRIBUTE_FIELDS:
                if f in item:
                    setattr(existing, f, item[f])
            existing.save()
        else:
            attr = ProductAttribute()
            for f in PRODUCT_ATTRIBUTE_FIELDS:
                if f in item:
                    setattr(attr, f, item[f])
            attr.save()

    def _import_attribute_value(self, item):
        from catalog.models import ProductAttribute, AttributeValue

        attr = ProductAttribute.objects.filter(
            slug=item['_attribute_slug']
        ).first()
        if not attr:
            raise ValueError(
                f"ProductAttribute '{item['_attribute_slug']}' not found"
            )

        existing = AttributeValue.objects.filter(
            attribute=attr, slug=item['slug']
        ).first()
        if existing:
            for f in ATTRIBUTE_VALUE_FIELDS:
                if f in item:
                    setattr(existing, f, item[f])
            existing.save()
        else:
            val = AttributeValue(attribute=attr)
            for f in ATTRIBUTE_VALUE_FIELDS:
                if f in item:
                    setattr(val, f, item[f])
            val.save()

    def _import_category(self, item, files):
        from catalog.models import Category

        slug = item['slug']
        existing = Category.objects.filter(slug=slug).first()

        if existing:
            for f in CATEGORY_FIELDS:
                if f in item:
                    setattr(existing, f, item[f])
            existing.parent = None  # Set in pass 3b
            self._import_category_assets(existing, item, files, slug)
            existing.save()
        else:
            cat = Category(parent=None)
            for f in CATEGORY_FIELDS:
                if f in item:
                    setattr(cat, f, item[f])
            cat.save()
            self._import_category_assets(cat, item, files, slug)
            if cat.image_asset or cat.banner_asset:
                cat.save()

    def _import_category_assets(self, cat, item, files, slug):
        """Handle inline MediaAsset import for category image_asset/banner_asset."""
        meta = item.get('_image_asset_meta')
        if meta:
            asset = _import_media_asset_inline(
                meta, files, f'Category:{slug}:image_asset'
            )
            if asset:
                cat.image_asset = asset
        meta = item.get('_banner_asset_meta')
        if meta:
            asset = _import_media_asset_inline(
                meta, files, f'Category:{slug}:banner_asset'
            )
            if asset:
                cat.banner_asset = asset

    def _set_category_parent(self, item):
        from catalog.models import Category

        slug = item['slug']
        parent_slug = item.get('_parent_slug')
        if not parent_slug:
            return

        cat = Category.objects.filter(slug=slug).first()
        parent = Category.objects.filter(slug=parent_slug).first()

        if cat and parent:
            cat.parent = parent
            cat.save(update_fields=['parent'])
        elif cat:
            logger.warning(
                "Parent category '%s' not found for '%s'",
                parent_slug, slug
            )

    def _import_brand(self, item, files):
        from catalog.models import Brand

        slug = item['slug']
        existing = Brand.objects.filter(slug=slug).first()

        if existing:
            for f in BRAND_FIELDS:
                if f in item:
                    setattr(existing, f, item[f])
            for ff in BRAND_FILE_FIELDS:
                file_key = f'Brand:{slug}:{ff}'
                fd = files.get(file_key)
                if fd:
                    import_file_field(existing, ff, fd)
            existing.save()
        else:
            brand = Brand()
            for f in BRAND_FIELDS:
                if f in item:
                    setattr(brand, f, item[f])
            brand.save()
            for ff in BRAND_FILE_FIELDS:
                file_key = f'Brand:{slug}:{ff}'
                fd = files.get(file_key)
                if fd:
                    import_file_field(brand, ff, fd)
            brand.save()

    def _import_product(self, item):
        from catalog.models import Product, Category, Brand

        sku = item['sku']
        existing = Product.objects.filter(sku=sku).first()

        # Resolve required category FK
        cat_slug = item.get('_category_slug')
        category = Category.objects.filter(slug=cat_slug).first()
        if not category:
            raise ValueError(
                f"Category '{cat_slug}' not found for product '{sku}'"
            )

        # Resolve optional brand FK
        brand_slug = item.get('_brand_slug')
        brand = None
        if brand_slug:
            brand = Brand.objects.filter(slug=brand_slug).first()
            if not brand:
                logger.warning(
                    "Brand '%s' not found for product '%s', setting to None",
                    brand_slug, sku
                )

        if existing:
            for f in PRODUCT_FIELDS:
                if f in item:
                    setattr(existing, f, item[f])
            existing.category = category
            existing.brand = brand
            for mf in PRODUCT_MONEY_FIELDS:
                _deserialize_money_field(existing, item, mf)
            existing.save()
            self._set_product_subscription_plans(existing, item)
        else:
            product = Product(category=category, brand=brand)
            for f in PRODUCT_FIELDS:
                if f in item:
                    setattr(product, f, item[f])
            for mf in PRODUCT_MONEY_FIELDS:
                _deserialize_money_field(product, item, mf)
            product.save()
            self._set_product_subscription_plans(product, item)

    def _set_product_subscription_plans(self, product, item):
        """Resolve subscription_plans M2M from slugs (cross-category)."""
        plan_slugs = item.get('_subscription_plan_slugs', [])
        if not plan_slugs:
            product.subscription_plans.clear()
            return
        try:
            from subscriptions.models import SubscriptionPlan
            plans = SubscriptionPlan.objects.filter(slug__in=plan_slugs)
            product.subscription_plans.set(plans)
            found = set(plans.values_list('slug', flat=True))
            missing = set(plan_slugs) - found
            for slug in missing:
                logger.warning(
                    "SubscriptionPlan '%s' not found for product '%s'",
                    slug, product.sku
                )
        except ImportError:
            pass

    def _import_attribute_assignment(self, item):
        from catalog.models import (
            Product, ProductAttribute, AttributeValue,
            ProductAttributeAssignment,
        )

        product = Product.objects.filter(
            sku=item['_product_sku']
        ).first()
        if not product:
            raise ValueError(
                f"Product '{item['_product_sku']}' not found for assignment"
            )

        attr = ProductAttribute.objects.filter(
            slug=item['_attribute_slug']
        ).first()
        if not attr:
            raise ValueError(
                f"ProductAttribute '{item['_attribute_slug']}' not found"
            )

        assign, _created = ProductAttributeAssignment.objects.get_or_create(
            product=product, attribute=attr,
            defaults={'sort_order': item.get('sort_order', 0)},
        )
        if not _created:
            assign.sort_order = item.get('sort_order', 0)
            assign.save()

        # Set allowed_values M2M
        value_slugs = item.get('_allowed_value_slugs', [])
        vals = AttributeValue.objects.filter(
            attribute=attr, slug__in=value_slugs
        )
        assign.allowed_values.set(vals)

    def _import_product_variant(self, item, files):
        from catalog.models import (
            Product, ProductVariant, ProductAttribute, AttributeValue,
        )

        sku = item['sku']
        product = Product.objects.filter(
            sku=item['_product_sku']
        ).first()
        if not product:
            raise ValueError(
                f"Product '{item['_product_sku']}' not found for variant"
            )

        existing = ProductVariant.objects.filter(sku=sku).first()

        if existing:
            for f in PRODUCT_VARIANT_FIELDS:
                if f in item:
                    setattr(existing, f, item[f])
            existing.product = product
            _deserialize_money_field(existing, item, 'price')
            # Inline MediaAsset for image_asset
            meta = item.get('_image_asset_meta')
            if meta:
                asset = _import_media_asset_inline(
                    meta, files,
                    f'ProductVariant:{sku}:image_asset',
                )
                if asset:
                    existing.image_asset = asset
            existing.save()
        else:
            variant = ProductVariant(product=product)
            for f in PRODUCT_VARIANT_FIELDS:
                if f in item:
                    setattr(variant, f, item[f])
            _deserialize_money_field(variant, item, 'price')
            variant.save()
            meta = item.get('_image_asset_meta')
            if meta:
                asset = _import_media_asset_inline(
                    meta, files,
                    f'ProductVariant:{sku}:image_asset',
                )
                if asset:
                    variant.image_asset = asset
                    variant.save()

        # Set selected_attributes M2M
        target = existing or ProductVariant.objects.filter(sku=sku).first()
        attr_refs = item.get('_selected_attributes', [])
        attr_values = []
        for ref in attr_refs:
            val = AttributeValue.objects.filter(
                attribute__slug=ref['attribute_slug'],
                slug=ref['value_slug'],
            ).first()
            if val:
                attr_values.append(val)
            else:
                logger.warning(
                    "AttributeValue '%s/%s' not found for variant '%s'",
                    ref.get('attribute_slug'), ref.get('value_slug'), sku
                )
        target.selected_attributes.set(attr_values)

    def _import_product_image(self, item, files):
        from catalog.models import Product, ProductImage

        product = Product.objects.filter(
            sku=item['_product_sku']
        ).first()
        if not product:
            raise ValueError(
                f"Product '{item['_product_sku']}' not found for image"
            )

        position = item.get('position', 0)
        existing = ProductImage.objects.filter(
            product=product, position=position
        ).first()

        # Import inline MediaAsset
        media_asset = None
        meta = item.get('_media_asset_meta')
        if meta:
            file_key = (
                f'ProductImage:{item["_product_sku"]}:'
                f'{position}:media_asset'
            )
            media_asset = _import_media_asset_inline(meta, files, file_key)

        if existing:
            for f in PRODUCT_IMAGE_FIELDS:
                if f in item:
                    setattr(existing, f, item[f])
            if media_asset:
                existing.media_asset = media_asset
            existing.save()
        else:
            img = ProductImage(product=product)
            for f in PRODUCT_IMAGE_FIELDS:
                if f in item:
                    setattr(img, f, item[f])
            if media_asset:
                img.media_asset = media_asset
            img.save()

    def _import_bundle_item(self, item):
        from catalog.models import Product, ProductVariant, BundleItem

        bundle = Product.objects.filter(
            sku=item['_bundle_sku']
        ).first()
        if not bundle:
            raise ValueError(
                f"Bundle product '{item['_bundle_sku']}' not found"
            )

        component = Product.objects.filter(
            sku=item['_component_product_sku']
        ).first()
        if not component:
            raise ValueError(
                f"Component product "
                f"'{item['_component_product_sku']}' not found"
            )

        comp_variant = None
        variant_sku = item.get('_component_variant_sku')
        if variant_sku:
            comp_variant = ProductVariant.objects.filter(
                sku=variant_sku
            ).first()
            if not comp_variant:
                logger.warning(
                    "Component variant '%s' not found for bundle item",
                    variant_sku
                )

        existing = BundleItem.objects.filter(
            bundle=bundle,
            component_product=component,
            component_variant=comp_variant,
        ).first()

        if existing:
            for f in BUNDLE_ITEM_FIELDS:
                if f in item:
                    setattr(existing, f, item[f])
            existing.save()
        else:
            bi = BundleItem(
                bundle=bundle,
                component_product=component,
                component_variant=comp_variant,
            )
            for f in BUNDLE_ITEM_FIELDS:
                if f in item:
                    setattr(bi, f, item[f])
            bi.save()

    # -- Mirror mode deletion --

    def _delete_absent(self, items):
        from catalog.models import (
            Category, Brand, Product, ProductVariant, ProductImage,
            ProductAttribute, AttributeValue, ProductAttributeAssignment,
            BundleItem,
        )

        deleted_count = 0

        # Build lookup sets from remote data
        remote_attr_slugs = {
            i['slug'] for i in items
            if i.get('_model') == 'ProductAttribute'
        }
        remote_val_keys = {
            (i['_attribute_slug'], i['slug']) for i in items
            if i.get('_model') == 'AttributeValue'
        }
        remote_cat_slugs = {
            i['slug'] for i in items if i.get('_model') == 'Category'
        }
        remote_brand_slugs = {
            i['slug'] for i in items if i.get('_model') == 'Brand'
        }
        remote_product_skus = {
            i['sku'] for i in items if i.get('_model') == 'Product'
        }
        remote_assign_keys = {
            (i['_product_sku'], i['_attribute_slug']) for i in items
            if i.get('_model') == 'ProductAttributeAssignment'
        }
        remote_variant_skus = {
            i['sku'] for i in items
            if i.get('_model') == 'ProductVariant'
        }
        remote_image_keys = {
            (i['_product_sku'], i['position']) for i in items
            if i.get('_model') == 'ProductImage'
        }
        remote_bundle_keys = {
            (
                i['_bundle_sku'],
                i['_component_product_sku'],
                i.get('_component_variant_sku'),
            )
            for i in items if i.get('_model') == 'BundleItem'
        }

        # Delete in reverse dependency order

        # 1. BundleItem (PROTECT FK to Product)
        for bi in BundleItem.objects.select_related(
            'bundle', 'component_product', 'component_variant'
        ).all():
            key = (
                bi.bundle.sku,
                bi.component_product.sku,
                bi.component_variant.sku if bi.component_variant else None,
            )
            if key not in remote_bundle_keys:
                bi.delete()
                deleted_count += 1

        # 2. ProductImage
        for img in ProductImage.objects.select_related('product').all():
            key = (img.product.sku, img.position)
            if key not in remote_image_keys:
                img.delete()
                deleted_count += 1

        # 3. ProductVariant
        for variant in ProductVariant.objects.all():
            if variant.sku not in remote_variant_skus:
                variant.delete()
                deleted_count += 1

        # 4. ProductAttributeAssignment
        for assign in ProductAttributeAssignment.objects.select_related(
            'product', 'attribute'
        ).all():
            key = (assign.product.sku, assign.attribute.slug)
            if key not in remote_assign_keys:
                assign.delete()
                deleted_count += 1

        # 5. Product (soft-delete aware — use hard_delete)
        for product in Product.all_objects.all():
            if product.sku not in remote_product_skus:
                try:
                    with transaction.atomic():
                        product.hard_delete()
                    deleted_count += 1
                except Exception as e:
                    logger.warning(
                        "Cannot delete product '%s': %s "
                        "(likely has orders or other protected references)",
                        product.sku, e
                    )

        # 6. Brand (Product.brand is SET_NULL, safe after products)
        for brand in Brand.objects.all():
            if brand.slug not in remote_brand_slugs:
                brand.delete()
                deleted_count += 1

        # 7. Category (Product.category is PROTECT, safe after products)
        #    Delete children before parents by sorting deepest first
        for cat in Category.objects.all().order_by('-sort_order'):
            if cat.slug not in remote_cat_slugs:
                try:
                    with transaction.atomic():
                        cat.delete()
                    deleted_count += 1
                except Exception as e:
                    logger.warning(
                        "Cannot delete category '%s': %s",
                        cat.slug, e
                    )

        # 8. AttributeValue
        for val in AttributeValue.objects.select_related('attribute').all():
            key = (val.attribute.slug, val.slug)
            if key not in remote_val_keys:
                val.delete()
                deleted_count += 1

        # 9. ProductAttribute
        for attr in ProductAttribute.objects.all():
            if attr.slug not in remote_attr_slugs:
                attr.delete()
                deleted_count += 1

        return deleted_count

    # -- Diff --

    def generate_diff(self, remote_data):
        from catalog.models import (
            Category, Brand, Product, ProductVariant, ProductImage,
            ProductAttribute, AttributeValue, ProductAttributeAssignment,
            BundleItem,
        )

        items = remote_data.get('items', [])
        if not items:
            return {
                'changes': [], 'warnings': [],
                'summary': 'No data to sync',
            }

        changes = []
        warnings = []

        for item in items:
            model_type = item.get('_model')
            existing = None
            compare_fields = []
            display_name = ''

            if model_type == 'ProductAttribute':
                existing = ProductAttribute.objects.filter(
                    slug=item.get('slug')
                ).first()
                compare_fields = PRODUCT_ATTRIBUTE_FIELDS
                display_name = f"Attribute: {item.get('name', '?')}"

            elif model_type == 'AttributeValue':
                attr = ProductAttribute.objects.filter(
                    slug=item.get('_attribute_slug')
                ).first()
                existing = (
                    AttributeValue.objects.filter(
                        attribute=attr, slug=item.get('slug')
                    ).first() if attr else None
                )
                compare_fields = ATTRIBUTE_VALUE_FIELDS
                display_name = (
                    f"Value: {item.get('_attribute_slug', '?')}/"
                    f"{item.get('value', '?')}"
                )

            elif model_type == 'Category':
                existing = Category.objects.filter(
                    slug=item.get('slug')
                ).first()
                compare_fields = CATEGORY_FIELDS
                display_name = f"Category: {item.get('name', '?')}"

            elif model_type == 'Brand':
                existing = Brand.objects.filter(
                    slug=item.get('slug')
                ).first()
                compare_fields = BRAND_FIELDS
                display_name = f"Brand: {item.get('name', '?')}"

            elif model_type == 'Product':
                existing = Product.objects.filter(
                    sku=item.get('sku')
                ).first()
                compare_fields = PRODUCT_FIELDS
                display_name = (
                    f"Product: {item.get('name', '?')} "
                    f"({item.get('sku', '?')})"
                )

            elif model_type == 'ProductAttributeAssignment':
                product = Product.objects.filter(
                    sku=item.get('_product_sku')
                ).first()
                attr = ProductAttribute.objects.filter(
                    slug=item.get('_attribute_slug')
                ).first()
                existing = (
                    ProductAttributeAssignment.objects.filter(
                        product=product, attribute=attr
                    ).first() if product and attr else None
                )
                compare_fields = PRODUCT_ATTRIBUTE_ASSIGNMENT_FIELDS
                display_name = (
                    f"Assignment: {item.get('_product_sku', '?')}/"
                    f"{item.get('_attribute_slug', '?')}"
                )

            elif model_type == 'ProductVariant':
                existing = ProductVariant.objects.filter(
                    sku=item.get('sku')
                ).first()
                compare_fields = PRODUCT_VARIANT_FIELDS
                display_name = (
                    f"Variant: {item.get('name', '?')} "
                    f"({item.get('sku', '?')})"
                )

            elif model_type == 'ProductImage':
                product = Product.objects.filter(
                    sku=item.get('_product_sku')
                ).first()
                existing = (
                    ProductImage.objects.filter(
                        product=product, position=item.get('position')
                    ).first() if product else None
                )
                compare_fields = PRODUCT_IMAGE_FIELDS
                display_name = (
                    f"Image: {item.get('_product_sku', '?')} "
                    f"pos {item.get('position', '?')}"
                )

            elif model_type == 'BundleItem':
                bundle = Product.objects.filter(
                    sku=item.get('_bundle_sku')
                ).first()
                comp = Product.objects.filter(
                    sku=item.get('_component_product_sku')
                ).first()
                v_sku = item.get('_component_variant_sku')
                comp_v = (
                    ProductVariant.objects.filter(sku=v_sku).first()
                    if v_sku else None
                )
                existing = (
                    BundleItem.objects.filter(
                        bundle=bundle,
                        component_product=comp,
                        component_variant=comp_v,
                    ).first() if bundle and comp else None
                )
                compare_fields = BUNDLE_ITEM_FIELDS
                display_name = (
                    f"Bundle: {item.get('_bundle_sku', '?')} -> "
                    f"{item.get('_component_product_sku', '?')}"
                )

            else:
                warnings.append(f"Unknown model type: {model_type}")
                continue

            if existing:
                field_changes = self._compute_field_diff(
                    existing, item, compare_fields
                )
                if field_changes:
                    changes.append({
                        'type': 'modify',
                        'model': model_type,
                        'name': display_name,
                        'changes': field_changes,
                    })
            else:
                changes.append({
                    'type': 'add',
                    'model': model_type,
                    'name': display_name,
                    'fields': {
                        k: v for k, v in item.items()
                        if not k.startswith('_')
                    },
                })

        adds = sum(1 for c in changes if c['type'] == 'add')
        mods = sum(1 for c in changes if c['type'] == 'modify')
        parts = []
        if adds:
            parts.append(f'{adds} addition(s)')
        if mods:
            parts.append(f'{mods} modification(s)')

        return {
            'changes': changes,
            'warnings': warnings,
            'summary': ', '.join(parts) if parts else 'No changes',
        }

    # -- Snapshot & Restore --

    def snapshot_current(self):
        return self.export(credential_mode='skip')

    def restore_snapshot(self, snapshot):
        try:
            result = self.import_data(snapshot, dry_run=False)
            return {
                'restored': result.get('synced', 0),
                'errors': result.get('errors', []),
            }
        except Exception as e:
            return {'restored': 0, 'errors': [str(e)]}
