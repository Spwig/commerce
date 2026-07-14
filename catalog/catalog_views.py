from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone

from .models import (
    Category,
    DigitalAsset,
    ExternalLicenseSync,
    LicenseKey,
    LicensePool,
    Product,
    Promotion,
)


@staff_member_required
def filter_categories(request):
    """
    AJAX endpoint for filtering categories in admin

    Query Parameters:
    - search: Search by name or description
    - parent: Filter by parent category (use 'null' for top-level only)
    - status: Filter by active/inactive
    - featured: Filter by featured (yes/no)
    - display_type: Filter by display type
    - has_products: Filter by has products (yes/no)
    - has_subcategories: Filter by has subcategories (yes/no)
    """
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Start with all categories
    categories = Category.objects.select_related("parent").prefetch_related("children", "products")

    # Search filter
    search = request.GET.get("search", "").strip()
    if search:
        categories = categories.filter(Q(name__icontains=search) | Q(description__icontains=search))

    # Parent filter
    parent_filter = request.GET.get("parent", "")
    if parent_filter == "null":
        # Top-level categories only (no parent)
        categories = categories.filter(parent__isnull=True)
    elif parent_filter:
        # Filter by specific parent
        try:
            parent_id = int(parent_filter)
            categories = categories.filter(parent_id=parent_id)
        except ValueError:
            pass

    # Status filter
    status_filter = request.GET.get("status", "")
    if status_filter == "active":
        categories = categories.filter(is_active=True)
    elif status_filter == "inactive":
        categories = categories.filter(is_active=False)

    # Featured filter
    featured_filter = request.GET.get("featured", "")
    if featured_filter == "yes":
        categories = categories.filter(is_featured=True)
    elif featured_filter == "no":
        categories = categories.filter(is_featured=False)

    # Page template filter
    page_template = request.GET.get("page_template", "")
    if page_template:
        categories = categories.filter(page_template=page_template)

    # Has products filter
    has_products = request.GET.get("has_products", "")
    if has_products == "yes":
        categories = categories.annotate(products_count=Count("products")).filter(
            products_count__gt=0
        )
    elif has_products == "no":
        categories = categories.annotate(products_count=Count("products")).filter(products_count=0)

    # Has subcategories filter
    has_subcategories = request.GET.get("has_subcategories", "")
    if has_subcategories == "yes":
        categories = categories.annotate(children_count=Count("children")).filter(
            children_count__gt=0
        )
    elif has_subcategories == "no":
        categories = categories.annotate(children_count=Count("children")).filter(children_count=0)

    # Order by sort order and name
    categories = categories.order_by("sort_order", "name")

    count = categories.count()

    # Render results as HTML
    html = render_to_string(
        "admin/catalog/partials/category_cards.html",
        {
            "categories": categories[:100],  # Limit to 100 results
        },
        request=request,
    )

    return JsonResponse({"html": html, "count": count})


@staff_member_required
def filter_promotions(request):
    """
    AJAX endpoint for filtering promotions in admin

    Query Parameters:
    - search: Search by name or description
    - status: Filter by status (active/scheduled/expired/inactive)
    - discount_type: Filter by discount type
    - apply_to: Filter by apply_to field
    """
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    now = timezone.now()

    # Start with all promotions
    promotions = Promotion.objects.all()

    # Search filter
    search = request.GET.get("search", "").strip()
    if search:
        promotions = promotions.filter(Q(name__icontains=search) | Q(description__icontains=search))

    # Status filter
    status_filter = request.GET.get("status", "")
    if status_filter == "active":
        # Active: is_active=True, started, not ended
        promotions = promotions.filter(is_active=True, start_date__lte=now).filter(
            Q(end_date__isnull=True) | Q(end_date__gt=now)
        )
    elif status_filter == "scheduled":
        # Scheduled: is_active=True, not started yet
        promotions = promotions.filter(is_active=True, start_date__gt=now)
    elif status_filter == "expired":
        # Expired: end_date in the past
        promotions = promotions.filter(end_date__lt=now)
    elif status_filter == "inactive":
        # Inactive: is_active=False
        promotions = promotions.filter(is_active=False)

    # Discount type filter
    discount_type = request.GET.get("discount_type", "")
    if discount_type:
        promotions = promotions.filter(discount_type=discount_type)

    # Apply to filter
    apply_to = request.GET.get("apply_to", "")
    if apply_to:
        promotions = promotions.filter(apply_to=apply_to)

    # Order by priority, then start date
    promotions = promotions.order_by("-priority", "-start_date")

    count = promotions.count()

    # Render results as HTML
    html = render_to_string(
        "admin/catalog/partials/promotion_cards.html",
        {
            "promotions": promotions[:100],  # Limit to 100 results
            "now": now,
        },
        request=request,
    )

    return JsonResponse({"html": html, "count": count})


@staff_member_required
def filter_license_keys(request):
    """
    AJAX endpoint for filtering license keys in admin

    Query Parameters:
    - search: Search by key, user email, order number
    - status: Filter by status (active, suspended, revoked, expired)
    - key_type: Filter by key type (permanent, trial, subscription)
    - product: Filter by product ID
    """
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Start with all license keys with related data
    licenses = LicenseKey.objects.select_related(
        "digital_asset", "digital_asset__product", "user", "order_item", "order_item__order"
    ).prefetch_related("activations")

    # Search filter
    search = request.GET.get("search", "").strip()
    if search:
        licenses = licenses.filter(
            Q(key__icontains=search)
            | Q(user__email__icontains=search)
            | Q(user__username__icontains=search)
            | Q(order_item__order__order_number__icontains=search)
            | Q(digital_asset__filename__icontains=search)
            | Q(digital_asset__product__name__icontains=search)
        )

    # Status filter
    status = request.GET.get("status", "")
    if status:
        licenses = licenses.filter(status=status)

    # Key type filter
    key_type = request.GET.get("key_type", "")
    if key_type:
        licenses = licenses.filter(key_type=key_type)

    # Product filter
    product = request.GET.get("product", "")
    if product:
        try:
            product_id = int(product)
            licenses = licenses.filter(digital_asset__product_id=product_id)
        except ValueError:
            pass

    # Order by newest first
    licenses = licenses.order_by("-issued_at")

    count = licenses.count()
    now = timezone.now()

    # Render results as HTML
    html = render_to_string(
        "admin/catalog/licensekey/partials/license_cards.html",
        {
            "licenses": licenses[:100],  # Limit to 100 results
            "now": now,
        },
        request=request,
    )

    return JsonResponse({"html": html, "count": count})


@staff_member_required
def filter_license_pools(request):
    """
    AJAX endpoint for filtering license pools in admin

    Query Parameters:
    - search: Search by pool name, product name
    - status: Filter by status (generating, ready, depleted, expired)
    - product: Filter by product ID
    """
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Start with all license pools with related data
    pools = LicensePool.objects.select_related(
        "product", "license_template", "sync_to_provider", "created_by"
    )

    # Search filter
    search = request.GET.get("search", "").strip()
    if search:
        pools = pools.filter(
            Q(name__icontains=search)
            | Q(description__icontains=search)
            | Q(product__name__icontains=search)
        )

    # Status filter
    status = request.GET.get("status", "")
    if status:
        pools = pools.filter(status=status)

    # Product filter
    product = request.GET.get("product", "")
    if product:
        try:
            product_id = int(product)
            pools = pools.filter(product_id=product_id)
        except ValueError:
            pass

    # Order by newest first
    pools = pools.order_by("-created_at")

    count = pools.count()

    # Render results as HTML
    html = render_to_string(
        "admin/catalog/licensepool/partials/pool_cards.html",
        {
            "pools": pools[:100],  # Limit to 100 results
        },
        request=request,
    )

    return JsonResponse({"html": html, "count": count})


@staff_member_required
def filter_external_sync(request):
    """
    AJAX endpoint for filtering external license syncs in admin

    Query Parameters:
    - search: Search by license key, external ID
    - status: Filter by sync status (pending, success, failed)
    - direction: Filter by sync direction (outbound, inbound)
    - provider: Filter by provider ID
    """
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Start with all external syncs with related data
    syncs = ExternalLicenseSync.objects.select_related(
        "license_key", "license_key__user", "provider"
    )

    # Search filter
    search = request.GET.get("search", "").strip()
    if search:
        syncs = syncs.filter(
            Q(license_key__key__icontains=search)
            | Q(external_id__icontains=search)
            | Q(provider__name__icontains=search)
        )

    # Status filter
    status = request.GET.get("status", "")
    if status:
        syncs = syncs.filter(sync_status=status)

    # Direction filter
    direction = request.GET.get("direction", "")
    if direction:
        syncs = syncs.filter(sync_direction=direction)

    # Provider filter
    provider = request.GET.get("provider", "")
    if provider:
        try:
            provider_id = int(provider)
            syncs = syncs.filter(provider_id=provider_id)
        except ValueError:
            pass

    # Order by newest first
    syncs = syncs.order_by("-synced_at")

    count = syncs.count()

    # Render results as HTML
    html = render_to_string(
        "admin/catalog/externallicensesync/partials/sync_cards.html",
        {
            "syncs": syncs[:100],  # Limit to 100 results
        },
        request=request,
    )

    return JsonResponse({"html": html, "count": count})


@staff_member_required
def filter_digital_assets(request):
    """
    AJAX endpoint for filtering digital assets in admin

    Query Parameters:
    - search: Search by filename, product name, version
    - status: Filter by is_active (active, inactive)
    - license: Filter by requires_license (yes, no)
    - product: Filter by product ID
    """
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Start with all digital assets with related data
    assets = DigitalAsset.objects.select_related("product", "created_by")

    # Search filter
    search = request.GET.get("search", "").strip()
    if search:
        assets = assets.filter(
            Q(filename__icontains=search)
            | Q(product__name__icontains=search)
            | Q(version__icontains=search)
            | Q(file_type__icontains=search)
        )

    # Status filter
    status = request.GET.get("status", "")
    if status == "active":
        assets = assets.filter(is_active=True)
    elif status == "inactive":
        assets = assets.filter(is_active=False)

    # License filter
    license_filter = request.GET.get("license", "")
    if license_filter == "yes":
        assets = assets.filter(requires_license=True)
    elif license_filter == "no":
        assets = assets.filter(requires_license=False)

    # Product filter
    product = request.GET.get("product", "")
    if product:
        try:
            product_id = int(product)
            assets = assets.filter(product_id=product_id)
        except ValueError:
            pass

    # Order by newest first
    assets = assets.order_by("-created_at")

    count = assets.count()

    # Render results as HTML
    html = render_to_string(
        "admin/catalog/digitalasset/partials/asset_cards.html",
        {
            "assets": assets[:100],  # Limit to 100 results
        },
        request=request,
    )

    return JsonResponse({"html": html, "count": count})


@staff_member_required
def filter_products(request):
    """
    AJAX endpoint for filtering products in admin

    Query Parameters:
    - search: Search by name, SKU, HS code
    - product_type: Filter by product type (simple, variable, bundle, etc.)
    - category: Filter by category ID
    - brand: Filter by brand ID
    - status: Filter by product status (published, draft, archived)
    - is_digital: Filter by digital status (digital, physical)
    - has_digital_assets: Filter by digital assets (with, without)
    - requires_license: Filter by license requirement (licensed, unlicensed)
    - pricing_strategy: Filter by pricing strategy
    - on_sale: Filter by sale status (yes, no)
    - is_subscription: Filter by subscription (yes, no)
    - is_preorder: Filter by preorder status (yes, no)
    - track_inventory: Filter by inventory tracking (yes, no)
    - import_source: Filter by import source (manual, imported)
    - is_featured: Filter by featured status (yes, no)
    """
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Start with all products with related data
    products = Product.objects.select_related("category", "brand").prefetch_related(
        "digital_assets"
    )

    # Search filter
    search = request.GET.get("search", "").strip()
    if search:
        products = products.filter(
            Q(name__icontains=search) | Q(sku__icontains=search) | Q(hs_code__icontains=search)
        )

    # Status filter
    status = request.GET.get("status", "")
    if status:
        products = products.filter(status=status)

    # Product type filter
    product_type = request.GET.get("product_type", "")
    if product_type:
        products = products.filter(product_type=product_type)

    # Category filter
    category_id = request.GET.get("category", "")
    if category_id:
        try:
            products = products.filter(category_id=int(category_id))
        except ValueError:
            pass

    # Brand filter
    brand_id = request.GET.get("brand", "")
    if brand_id:
        try:
            products = products.filter(brand_id=int(brand_id))
        except ValueError:
            pass

    # Digital filter
    is_digital = request.GET.get("is_digital", "")
    if is_digital == "digital":
        products = products.filter(is_digital=True)
    elif is_digital == "physical":
        products = products.filter(is_digital=False)

    # Has digital assets filter (uses Count annotation)
    has_digital_assets = request.GET.get("has_digital_assets", "")
    if has_digital_assets == "with":
        products = products.annotate(digital_asset_count=Count("digital_assets")).filter(
            digital_asset_count__gt=0
        )
    elif has_digital_assets == "without":
        products = products.annotate(digital_asset_count=Count("digital_assets")).filter(
            digital_asset_count=0
        )

    # Requires license filter
    requires_license = request.GET.get("requires_license", "")
    if requires_license == "licensed":
        products = products.filter(requires_license=True)
    elif requires_license == "unlicensed":
        products = products.filter(requires_license=False)

    # Pricing strategy filter
    pricing_strategy = request.GET.get("pricing_strategy", "")
    if pricing_strategy:
        products = products.filter(pricing_strategy=pricing_strategy)

    # On sale filter
    on_sale = request.GET.get("on_sale", "")
    if on_sale == "yes":
        products = products.filter(sale_price__isnull=False)
    elif on_sale == "no":
        products = products.filter(sale_price__isnull=True)

    # Subscription filter
    is_subscription = request.GET.get("is_subscription", "")
    if is_subscription == "yes":
        products = products.filter(is_subscription_enabled=True)
    elif is_subscription == "no":
        products = products.filter(is_subscription_enabled=False)

    # Preorder filter
    is_preorder = request.GET.get("is_preorder", "")
    if is_preorder == "yes":
        products = products.filter(is_preorder=True)
    elif is_preorder == "no":
        products = products.filter(is_preorder=False)

    # Inventory tracking filter
    track_inventory = request.GET.get("track_inventory", "")
    if track_inventory == "yes":
        products = products.filter(track_inventory=True)
    elif track_inventory == "no":
        products = products.filter(track_inventory=False)

    # Import source filter
    import_source = request.GET.get("import_source", "")
    if import_source == "manual":
        products = products.filter(import_source__isnull=True)
    elif import_source == "imported":
        products = products.exclude(import_source__isnull=True)

    # Featured filter
    is_featured = request.GET.get("is_featured", "")
    if is_featured == "yes":
        products = products.filter(is_featured=True)
    elif is_featured == "no":
        products = products.filter(is_featured=False)

    # Order by most recently updated
    products = products.order_by("-updated_at")

    count = products.count()

    # Render results as HTML
    html = render_to_string(
        "admin/catalog/product/partials/product_cards.html",
        {
            "products": products[:100],  # Limit to 100 results
        },
        request=request,
    )

    return JsonResponse({"html": html, "count": count})
