from django.db.models import Count, Exists, OuterRef, Prefetch, Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from admin_api.authentication import MobileTokenAuthentication
from core.api.api_descriptions import (
    AUTH_REQUIRED,
    POS_LICENSE_REQUIRED,
    PRODUCT_NOT_FOUND,
)
from pos_api.permissions import IsStaffUser
from pos_api.serializers.product import (
    POSCategorySerializer,
    POSProductListSerializer,
    POSProductSerializer,
)


def _get_terminal_context(request):
    """Extract warehouse ID and currency from terminal UUID header or query params."""
    terminal_uuid = request.headers.get("X-Terminal-UUID")
    warehouse_id = request.query_params.get("warehouse_id")
    currency = None

    if warehouse_id:
        warehouse_id = int(warehouse_id)

    if terminal_uuid:
        from pos_app.models import POSTerminal

        try:
            terminal = POSTerminal.objects.select_related("warehouse").get(
                uuid=terminal_uuid, is_active=True
            )
            if not warehouse_id:
                warehouse_id = terminal.warehouse_id
            currency = terminal.effective_currency
        except POSTerminal.DoesNotExist:
            pass

    # Fallback currency from site settings
    if not currency:
        from core.models import SiteSettings

        settings = SiteSettings.objects.first()
        currency = str(settings.default_currency) if settings else "EUR"

    return warehouse_id, currency


def _serialize_product(product, warehouse_id=None, currency=None):
    """Convert a Product model to POS serializer-compatible dict."""
    # Get primary image using prefetch cache if available
    image = None
    prefetched = getattr(product, "_prefetched_objects_cache", {}).get("images", None)
    if prefetched is not None:
        primary = next((i for i in prefetched if i.is_primary), None) or (
            prefetched[0] if prefetched else None
        )
    elif hasattr(product, "images"):
        primary = (
            product.images.select_related("media_asset").filter(is_primary=True).first()
            or product.images.select_related("media_asset").first()
        )
    else:
        primary = None
    if primary and primary.media_asset:
        image = primary.media_asset.get_thumbnail("medium")

    # Convert price to terminal currency if needed
    price_amount = str(product.price.amount) if product.price else "0.00"
    price_currency = currency or (str(product.price.currency) if product.price else "EUR")

    if currency and product.price and str(product.price.currency) != currency:
        try:
            converted = product.get_price_in_currency(currency)
            price_amount = str(converted.amount)
            price_currency = currency
        except Exception:
            pass  # Fall back to stored price on conversion error

    # Get stock for warehouse
    stock_available = None
    is_low_stock = False
    if warehouse_id and product.track_inventory:
        from django.db.models import F, Sum, Value
        from django.db.models.functions import Greatest

        from catalog.models import StockItem

        if product.product_type == "variable":
            # Aggregate stock across all variants (available is a property, not a column)
            agg = StockItem.objects.filter(
                product=product, variant__isnull=False, warehouse_id=warehouse_id
            ).aggregate(total_available=Sum(Greatest(F("on_hand") - F("allocated"), Value(0))))
            stock_available = agg["total_available"] or 0
            is_low_stock = stock_available > 0 and stock_available <= (
                product.low_stock_threshold or 5
            )
        elif product.product_type == "bundle":
            # Bundle stock = minimum available across all required component products
            from catalog.models import BundleItem

            bundle_items = BundleItem.objects.filter(
                bundle=product, is_optional=False
            ).select_related("component_product")
            min_available = None
            for bi in bundle_items:
                comp = bi.component_product
                if not comp.track_inventory:
                    continue
                if comp.product_type == "variable":
                    agg = StockItem.objects.filter(
                        product=comp, variant__isnull=False, warehouse_id=warehouse_id
                    ).aggregate(
                        total_available=Sum(Greatest(F("on_hand") - F("allocated"), Value(0)))
                    )
                    comp_avail = agg["total_available"] or 0
                else:
                    try:
                        si = StockItem.objects.get(
                            product=comp, variant__isnull=True, warehouse_id=warehouse_id
                        )
                        comp_avail = si.available
                    except StockItem.DoesNotExist:
                        comp_avail = 0
                # How many bundles can we make from this component?
                comp_bundles = comp_avail // bi.quantity if bi.quantity > 0 else comp_avail
                if min_available is None or comp_bundles < min_available:
                    min_available = comp_bundles
            stock_available = min_available if min_available is not None else 0
            is_low_stock = stock_available > 0 and stock_available <= (
                product.low_stock_threshold or 5
            )
        elif product.product_type == "configurable":
            # Configurable stock: in stock if every required slot has at least one available option
            from catalog.models import ConfigurationSlot

            slots = ConfigurationSlot.objects.filter(
                product=product, is_required=True
            ).prefetch_related("options__option_product", "options__option_variant")
            all_slots_have_stock = True
            for slot in slots:
                slot_has_option = False
                for opt in slot.options.all():
                    if not opt.option_product.track_inventory:
                        slot_has_option = True
                        break
                    if opt.option_variant:
                        try:
                            si = StockItem.objects.get(
                                variant=opt.option_variant, warehouse_id=warehouse_id
                            )
                            if si.available > 0:
                                slot_has_option = True
                                break
                        except StockItem.DoesNotExist:
                            pass
                    else:
                        try:
                            si = StockItem.objects.get(
                                product=opt.option_product,
                                variant__isnull=True,
                                warehouse_id=warehouse_id,
                            )
                            if si.available > 0:
                                slot_has_option = True
                                break
                        except StockItem.DoesNotExist:
                            pass
                if not slot_has_option:
                    all_slots_have_stock = False
                    break
            stock_available = 1 if all_slots_have_stock else 0
            is_low_stock = False
        else:
            try:
                stock = StockItem.objects.get(
                    product=product, variant__isnull=True, warehouse_id=warehouse_id
                )
                stock_available = stock.available
                is_low_stock = stock.is_low_stock
            except StockItem.DoesNotExist:
                stock_available = 0

    # Get category
    category = product.category

    data = {
        "id": product.id,
        "name": str(product.name),
        "slug": product.slug,
        "sku": product.sku or "",
        "barcode": getattr(product, "barcode", "") or "",
        "price": price_amount,
        "currency": price_currency,
        "product_type": product.product_type,
        "sales_channel": getattr(product, "sales_channel", "all"),
        "category_id": category.id if category else None,
        "category_name": str(category.name) if category else None,
        "image": image,
        "track_inventory": product.track_inventory,
        "stock_available": stock_available,
        "is_low_stock": is_low_stock,
        "has_variants": product.product_type == "variable",
        "is_configurable": product.product_type == "configurable",
        "is_bundle": product.product_type == "bundle",
        "is_featured": getattr(product, "is_featured", False),
        "created_at": product.created_at.isoformat(),
        "updated_at": product.updated_at.isoformat(),
    }

    # Include variant data for variable products (offline POS support)
    if product.product_type == "variable":
        from catalog.models import StockItem

        variant_list = []
        # Use prefetched variants if available, otherwise query
        prefetched_variants = getattr(product, "_prefetched_objects_cache", {}).get(
            "variants", None
        )
        if prefetched_variants is not None:
            variants_qs = [v for v in prefetched_variants if v.is_active]
        else:
            variants_qs = product.variants.filter(is_active=True).prefetch_related(
                "selected_attributes__attribute"
            )
        for v in variants_qs:
            # Variant price
            effective_price = v.get_effective_price()
            v_price = str(effective_price.amount) if effective_price else price_amount

            # Variant image
            v_image = None
            if v.image_asset:
                v_image = v.image_asset.get_thumbnail("medium")

            # Variant attributes
            attrs = {}
            for av in v.selected_attributes.select_related("attribute").all():
                attrs[av.attribute.name] = {
                    "value": av.value,
                    "color_hex": av.color_hex or None,
                }

            # Variant stock at this warehouse
            v_stock = None
            if warehouse_id and product.track_inventory:
                try:
                    si = StockItem.objects.get(variant=v, warehouse_id=warehouse_id)
                    v_stock = si.available
                except StockItem.DoesNotExist:
                    v_stock = 0

            variant_list.append(
                {
                    "id": v.id,
                    "name": v.name,
                    "sku": v.sku or "",
                    "barcode": v.barcode or "",
                    "price": v_price,
                    "attributes": attrs,
                    "stock_available": v_stock,
                    "image": v_image,
                    "color_swatch": v.color_swatch or None,
                }
            )
        data["variants"] = variant_list

    # Include bundle data for bundle products
    if product.product_type == "bundle":
        from catalog.models import BundleItem
        from catalog.models import StockItem as BundleStockItem

        bundle_items_qs = (
            BundleItem.objects.filter(bundle=product)
            .select_related("component_product", "component_variant")
            .prefetch_related(
                "component_product__images__media_asset",
                "component_product__variants",
            )
            .order_by("sort_order")
        )

        items_data = []
        for bi in bundle_items_qs:
            # Component image
            bi_image = None
            if bi.component_product.images.exists():
                bi_primary = (
                    bi.component_product.images.filter(is_primary=True).first()
                    or bi.component_product.images.first()
                )
                if bi_primary and bi_primary.media_asset:
                    bi_image = bi_primary.media_asset.get_thumbnail("medium")

            # Component stock
            bi_stock = None
            if warehouse_id and bi.component_product.track_inventory:
                try:
                    si = BundleStockItem.objects.get(
                        product=bi.component_product,
                        variant=bi.component_variant,
                        warehouse_id=warehouse_id,
                    )
                    bi_stock = si.available
                except BundleStockItem.DoesNotExist:
                    bi_stock = 0

            # Available variants for variant selection
            avail_variants = []
            if bi.allow_variant_selection:
                for v in bi.component_product.variants.filter(is_active=True):
                    v_stock = None
                    if warehouse_id and bi.component_product.track_inventory:
                        try:
                            vsi = BundleStockItem.objects.get(variant=v, warehouse_id=warehouse_id)
                            v_stock = vsi.available
                        except BundleStockItem.DoesNotExist:
                            v_stock = 0
                    avail_variants.append(
                        {
                            "id": v.id,
                            "name": v.name,
                            "sku": v.sku or "",
                            "price": str(v.get_effective_price().amount)
                            if v.get_effective_price()
                            else "0.00",
                            "stock_available": v_stock,
                            "image": v.image_asset.get_thumbnail("medium")
                            if v.image_asset
                            else None,
                        }
                    )

            items_data.append(
                {
                    "id": bi.id,
                    "component_product_id": bi.component_product_id,
                    "component_product_name": str(bi.component_product.name),
                    "component_product_sku": bi.component_product.sku or "",
                    "component_variant_id": bi.component_variant_id,
                    "component_variant_name": bi.component_variant.name
                    if bi.component_variant
                    else None,
                    "quantity": bi.quantity,
                    "is_optional": bi.is_optional,
                    "allow_variant_selection": bi.allow_variant_selection,
                    "sort_order": bi.sort_order,
                    "image": bi_image,
                    "stock_available": bi_stock,
                    "available_variants": avail_variants,
                }
            )

        data["bundle"] = {
            "pricing_strategy": product.bundle_pricing_strategy,
            "discount_percentage": str(product.bundle_discount_percentage)
            if product.bundle_discount_percentage
            else "0",
            "items": items_data,
        }
        data["is_bundle"] = True

    # Include configurator data for configurable products
    if product.product_type == "configurable":
        from catalog.models import (
            CompatibilityRule,
            ConfigurationPreset,
            ConfigurationSlot,
            StockItem,
        )

        slots_data = []
        slots = (
            ConfigurationSlot.objects.filter(product=product)
            .order_by("sort_order")
            .prefetch_related(
                "options__option_product__images__media_asset",
                "options__option_variant",
            )
        )
        for slot in slots:
            options_data = []
            for opt in slot.options.order_by("sort_order"):
                opt_image = None
                if opt.option_product.images.exists():
                    primary = (
                        opt.option_product.images.filter(is_primary=True).first()
                        or opt.option_product.images.first()
                    )
                    if primary and primary.media_asset:
                        opt_image = primary.media_asset.get_thumbnail("medium")

                # Option stock at this warehouse
                opt_stock = None
                if warehouse_id and opt.option_product.track_inventory:
                    try:
                        si = StockItem.objects.get(
                            product=opt.option_product,
                            variant=opt.option_variant,
                            warehouse_id=warehouse_id,
                        )
                        opt_stock = si.available
                    except StockItem.DoesNotExist:
                        opt_stock = 0

                opt_price = (
                    str(opt.option_product.price.amount) if opt.option_product.price else "0.00"
                )
                if (
                    currency
                    and opt.option_product.price
                    and str(opt.option_product.price.currency) != currency
                ):
                    try:
                        converted = opt.option_product.get_price_in_currency(currency)
                        opt_price = str(converted.amount)
                    except Exception:
                        pass

                options_data.append(
                    {
                        "id": opt.id,
                        "product_id": opt.option_product_id,
                        "product_name": str(opt.option_product.name),
                        "variant_id": opt.option_variant_id,
                        "variant_name": opt.option_variant.name if opt.option_variant else None,
                        "price": opt_price,
                        "price_adjustment": str(opt.price_adjustment.amount)
                        if opt.price_adjustment
                        else "0.00",
                        "image": opt_image,
                        "is_default": opt.is_default,
                        "is_popular": opt.is_popular,
                        "stock_available": opt_stock,
                        "quantity": opt.quantity,
                        "sort_order": opt.sort_order,
                    }
                )

            slots_data.append(
                {
                    "id": slot.id,
                    "name": str(slot.name),
                    "slug": slot.slug,
                    "description": str(slot.description) if slot.description else "",
                    "icon": slot.icon or "",
                    "is_required": slot.is_required,
                    "min_selections": slot.min_selections,
                    "max_selections": slot.max_selections,
                    "sort_order": slot.sort_order,
                    "options": options_data,
                }
            )

        # Compatibility rules
        rules = CompatibilityRule.objects.filter(configurable_product=product).prefetch_related(
            "compatible_options"
        )
        rules_data = []
        for rule in rules:
            rules_data.append(
                {
                    "id": rule.id,
                    "rule_type": rule.rule_type,
                    "source_option_id": rule.source_option_id,
                    "target_slot_id": rule.target_slot_id,
                    "compatible_option_ids": list(
                        rule.compatible_options.values_list("id", flat=True)
                    ),
                }
            )

        # Presets
        presets = ConfigurationPreset.objects.filter(product=product).order_by("sort_order")
        presets_data = []
        for preset in presets:
            preset_image = None
            if preset.image_asset:
                preset_image = preset.image_asset.get_thumbnail("medium")
            presets_data.append(
                {
                    "id": preset.id,
                    "name": str(preset.name),
                    "description": str(preset.description) if preset.description else "",
                    "image": preset_image,
                    "selections": preset.selections,
                    "is_featured": preset.is_featured,
                }
            )

        data["configurator"] = {
            "pricing_strategy": product.configurator_pricing_strategy,
            "base_price": str(product.configurator_base_price.amount)
            if product.configurator_base_price
            else None,
            "slots": slots_data,
            "rules": rules_data,
            "presets": presets_data,
        }

        # Include 3D scene data if available
        try:
            from configurator_3d.models import SceneConfig
            from configurator_3d.serializers import serialize_scene_3d

            scene = (
                SceneConfig.objects.select_related("base_model", "environment_image")
                .prefetch_related("mappings", "geometry_assets__media_asset")
                .get(product=product, is_enabled=True)
            )
            if scene.base_model:
                data["configurator"]["scene_3d"] = serialize_scene_3d(scene)
        except (SceneConfig.DoesNotExist, Exception):
            pass

    return data


@extend_schema(
    summary=_("List POS products"),
    description=_(
        "Returns products available for in-store sale, filtered by sales channel. "
        "Includes warehouse-specific stock levels when a terminal is identified. "
        "Products with images appear first, ordered by per-warehouse popularity."
    ),
    parameters=[
        OpenApiParameter("q", OpenApiTypes.STR, description=_("Search by name, SKU, or barcode")),
        OpenApiParameter("category", OpenApiTypes.INT, description=_("Filter by category ID")),
        OpenApiParameter(
            "warehouse_id", OpenApiTypes.INT, description=_("Warehouse for stock levels")
        ),
        OpenApiParameter("page", OpenApiTypes.INT, description=_("Page number (default: 1)")),
        OpenApiParameter(
            "page_size", OpenApiTypes.INT, description=_("Items per page (default: 50, max: 200)")
        ),
    ],
    responses={
        200: POSProductListSerializer(many=True),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
    },
    tags=["POS - Catalog"],
)
@api_view(["GET"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def product_list(request):
    """List products available for POS sale."""
    from catalog.models import Category, Product, ProductImage, ProductVariant

    warehouse_id, currency = _get_terminal_context(request)

    # Base queryset: published products available in POS channel
    products = (
        Product.objects.filter(
            status="published",
            sales_channel__in=["all", "pos_only"],
        )
        .exclude(
            hide_from_storefront=True,
        )
        .select_related("category", "brand")
        .prefetch_related(
            Prefetch(
                "images",
                queryset=ProductImage.objects.select_related("media_asset").order_by(
                    "-is_primary", "position"
                ),
            ),
            Prefetch(
                "variants",
                queryset=ProductVariant.objects.filter(is_active=True).prefetch_related(
                    "selected_attributes__attribute"
                ),
            ),
        )
    )

    # Popularity ordering: per-warehouse sales in last 90 days
    ninety_days_ago = timezone.now() - timezone.timedelta(days=90)
    popularity_filter = Q(
        orderitem__order__status__in=["processing", "shipped", "delivered"],
        orderitem__order__created_at__gte=ninety_days_ago,
    )
    if warehouse_id:
        popularity_filter &= Q(orderitem__order__pos_terminal__warehouse_id=warehouse_id)

    products = products.annotate(
        popularity=Count("orderitem", filter=popularity_filter),
        has_image=Exists(ProductImage.objects.filter(product=OuterRef("pk"))),
    ).order_by("-is_featured", "-has_image", "-popularity", "-created_at", "name")

    # Search filter
    q = request.query_params.get("q", "").strip()
    if q:
        products = products.filter(
            Q(name__icontains=q) | Q(sku__icontains=q) | Q(barcode__icontains=q)
        )

    # Category filter - include all descendant categories
    category_id = request.query_params.get("category")
    if category_id:
        try:
            category = Category.objects.get(id=category_id, is_active=True)
            descendant_ids = category.get_descendant_ids()
            products = products.filter(category_id__in=descendant_ids)
        except Category.DoesNotExist:
            products = products.filter(category__id=category_id)

    # Pagination
    page = int(request.query_params.get("page", 1))
    page_size = min(int(request.query_params.get("page_size", 50)), 200)
    start = (page - 1) * page_size
    end = start + page_size

    total = products.count()
    products_page = products[start:end]

    results = [_serialize_product(p, warehouse_id, currency) for p in products_page]

    return Response(
        {
            "success": True,
            "results": results,
            "count": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
        }
    )


@extend_schema(
    summary=_("Get product detail"),
    description=_("Returns full product details including variants and warehouse stock."),
    responses={
        200: POSProductSerializer,
        404: OpenApiResponse(description=PRODUCT_NOT_FOUND),
    },
    tags=["POS - Catalog"],
)
@api_view(["GET"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def product_detail(request, product_id):
    """Get full product details for POS."""
    from catalog.models import Product, ProductImage, ProductVariant

    warehouse_id, currency = _get_terminal_context(request)

    try:
        product = (
            Product.objects.select_related("category", "brand")
            .prefetch_related(
                Prefetch(
                    "images",
                    queryset=ProductImage.objects.select_related("media_asset").order_by(
                        "-is_primary", "position"
                    ),
                ),
                Prefetch(
                    "variants",
                    queryset=ProductVariant.objects.filter(is_active=True).prefetch_related(
                        "selected_attributes__attribute"
                    ),
                ),
            )
            .get(
                id=product_id,
                status="published",
                sales_channel__in=["all", "pos_only"],
            )
        )
    except Product.DoesNotExist:
        return Response(
            {"success": False, "error": {"code": "NOT_FOUND", "message": "Product not found."}},
            status=status.HTTP_404_NOT_FOUND,
        )

    data = _serialize_product(product, warehouse_id, currency)

    # Variants are now included by _serialize_product for variable products

    return Response({"success": True, "product": data})


@extend_schema(
    summary=_("Barcode lookup"),
    description=_("Look up a product or variant by barcode. Fast, indexed lookup for scanning."),
    responses={
        200: POSProductSerializer,
        404: OpenApiResponse(description=_("No product found with this barcode")),
    },
    tags=["POS - Catalog"],
)
@api_view(["GET"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def barcode_lookup(request, barcode):
    """Look up a product by barcode."""
    from catalog.models import Product, ProductVariant

    warehouse_id, currency = _get_terminal_context(request)

    # Try product barcode first
    try:
        product = Product.objects.get(
            barcode=barcode,
            status="published",
            sales_channel__in=["all", "pos_only"],
        )
        data = _serialize_product(product, warehouse_id, currency)
        return Response({"success": True, "product": data, "variant_id": None})
    except Product.DoesNotExist:
        pass

    # Try variant barcode
    try:
        variant = ProductVariant.objects.select_related("product").get(
            barcode=barcode,
            is_active=True,
            product__status="published",
            product__sales_channel__in=["all", "pos_only"],
        )
        data = _serialize_product(variant.product, warehouse_id, currency)
        data["selected_variant_id"] = variant.id
        return Response({"success": True, "product": data, "variant_id": variant.id})
    except ProductVariant.DoesNotExist:
        pass

    # Try SKU as fallback
    try:
        product = Product.objects.get(
            sku=barcode,
            status="published",
            sales_channel__in=["all", "pos_only"],
        )
        data = _serialize_product(product, warehouse_id, currency)
        return Response({"success": True, "product": data, "variant_id": None})
    except Product.DoesNotExist:
        pass

    return Response(
        {
            "success": False,
            "error": {
                "code": "NOT_FOUND",
                "message": f'No product found with barcode "{barcode}".',
            },
        },
        status=status.HTTP_404_NOT_FOUND,
    )


@extend_schema(
    summary=_("List categories"),
    description=_("Returns the category tree for POS product navigation."),
    responses={
        200: POSCategorySerializer(many=True),
    },
    tags=["POS - Catalog"],
)
@api_view(["GET"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def category_list(request):
    """List categories for POS navigation."""
    from catalog.models import Category

    categories = (
        Category.objects.filter(is_active=True)
        .select_related("image_asset")
        .order_by("sort_order", "name")
    )

    results = []
    for cat in categories:
        image = None
        if cat.image_asset:
            image = cat.image_asset.get_thumbnail("thumbnail")
        results.append(
            {
                "id": cat.id,
                "name": cat.name,
                "slug": cat.slug,
                "parent_id": cat.parent_id,
                "image": image,
            }
        )

    return Response(
        {
            "success": True,
            "categories": results,
        }
    )
