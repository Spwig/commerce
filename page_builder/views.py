import json

from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Avg, Count, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.vary import vary_on_headers
from django.views.generic import TemplateView

from catalog.models import Category, Product
from core.decorators import allow_iframe_sameorigin
from core.translation_utils import translate_storefront_context

from .models import Element, Page


class PageView(TemplateView):
    """Generic page view that renders pages built with the page builder"""

    template_name = "page_builder/page.html"

    def get_page_object(self):
        """Get the page object based on URL parameters"""
        page_type = self.kwargs.get("page_type")
        slug = self.kwargs.get("slug")

        if slug:
            # Get page by slug
            try:
                page = (
                    Page.objects.select_related("theme")
                    .prefetch_related("elements")
                    .get(slug=slug, status="published")
                )
            except Page.DoesNotExist:
                raise Http404(_("Page not found"))
        elif page_type:
            # Get default page for page type
            try:
                page = (
                    Page.objects.select_related("theme")
                    .prefetch_related("elements")
                    .get(page_type=page_type, is_default_for_type=True, status="published")
                )
            except Page.DoesNotExist:
                raise Http404(_(f"No default {page_type} page found"))
        else:
            # Default to home page
            try:
                page = (
                    Page.objects.select_related("theme")
                    .prefetch_related("elements")
                    .get(page_type="home", is_default_for_type=True, status="published")
                )
            except Page.DoesNotExist:
                raise Http404(_("No home page found"))

        return page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.get_page_object()

        # Get brand CSS URL if available
        brand_css_url = None
        try:
            from design.theme_models import ThemeBranding

            branding = ThemeBranding.objects.first()
            if branding:
                brand_css_url = branding.get_css_url()
        except Exception:
            pass

        elements = page.elements.filter(parent_element__isnull=True).order_by("order")

        context.update(
            {
                "page": page,
                "elements": elements,
                "page_title": page.meta_title or page.title,
                "page_description": page.meta_description,
                "page_keywords": page.meta_keywords,
                "og_image": page.og_image,
                "brand_css_url": brand_css_url,
            }
        )

        # Collect unique scripts and CSS from all elements on page
        context["element_scripts"] = self._collect_element_scripts(elements)
        context["element_css_files"] = self._collect_element_css(elements)

        # Add page-specific context
        if page.page_type == "home":
            context.update(self.get_home_context())
        elif page.page_type == "category":
            context.update(self.get_category_context())
        elif page.page_type == "product":
            context.update(self.get_product_context())

        return context

    def _collect_element_scripts(self, elements):
        """Recursively collect unique script URLs from all page elements."""
        from .element_registry import get_registry

        registry = get_registry()
        scripts = set()

        def collect_from_elements(element_queryset):
            for element in element_queryset:
                if not element.is_active:
                    continue

                element_config = registry.get_element(element.element_type)
                if element_config and element_config.scripts:
                    scripts.update(element_config.scripts)

                # Handle nested elements (containers)
                children = element.child_elements.filter(is_active=True)
                if children.exists():
                    collect_from_elements(children)

        collect_from_elements(elements)
        return list(scripts)

    def _collect_element_css(self, elements):
        """Recursively collect unique CSS file URLs from all page elements."""
        from .element_registry import get_registry

        registry = get_registry()
        css_files = set()

        def collect_from_elements(element_queryset):
            for element in element_queryset:
                if not element.is_active:
                    continue

                element_config = registry.get_element(element.element_type)
                if element_config and element_config.css_files:
                    css_files.update(element_config.css_files)

                # Handle nested elements (containers)
                children = element.child_elements.filter(is_active=True)
                if children.exists():
                    collect_from_elements(children)

        collect_from_elements(elements)
        return list(css_files)

    def get_home_context(self):
        """Add context specific to home page"""
        return {
            "featured_products": Product.objects.filter(
                is_featured=True, status="published", hide_from_storefront=False
            ).exclude(sales_channel="pos_only")[:8],
            "categories": Category.objects.filter(is_active=True, parent=None)[:6],
        }

    def get_category_context(self):
        """Add context specific to category pages"""
        category_slug = self.kwargs.get("category_slug")
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug, is_active=True)
            # Include products from all descendant categories (full tree depth)
            descendant_ids = category.get_descendant_ids()
            products = Product.objects.filter(
                category_id__in=descendant_ids, status="published"
            ).exclude(sales_channel="pos_only")
            return {
                "category": category,
                "products": products,
                "subcategories": category.children.filter(is_active=True),
            }
        return {}

    def get_product_context(self):
        """Add context specific to product pages"""
        product_slug = self.kwargs.get("product_slug")
        if product_slug:
            product = get_object_or_404(
                Product,
                slug=product_slug,
                status="published",
                sales_channel__in=["all", "online_only"],
            )
            related_products = (
                Product.objects.filter(category=product.category, status="published")
                .exclude(id=product.id)
                .exclude(sales_channel="pos_only")[:4]
            )
            return {
                "product": product,
                "related_products": related_products,
            }
        return {}

    @method_decorator(vary_on_headers("User-Agent"))
    @method_decorator(allow_iframe_sameorigin)
    def dispatch(self, request, *args, **kwargs):
        # Cache pages for performance
        page = self.get_page_object()
        if page.cache_timeout > 0:
            cache_key = f"page_{page.id}_{request.GET.urlencode()}"
            timeout = page.cache_timeout
            return cache_page(timeout, key_prefix=cache_key)(super().dispatch)(
                request, *args, **kwargs
            )
        return super().dispatch(request, *args, **kwargs)


@allow_iframe_sameorigin
def home_view(request):
    """Home page view - renders page builder home page with simple_home fallback"""
    # Try page builder home page first
    try:
        Page.objects.get(page_type="home", is_default_for_type=True, status="published")
        view = PageView.as_view()
        return view(request)
    except Page.DoesNotExist:
        pass

    # Fallback: render simple home template
    categories = Category.objects.filter(is_active=True, parent__isnull=True).order_by(
        "sort_order", "name"
    )[:8]

    featured_products = (
        Product.objects.filter(status="published", is_featured=True)
        .exclude(sales_channel="pos_only")
        .select_related("category")
        .prefetch_related("images")[:8]
    )

    if not featured_products.exists():
        featured_products = (
            Product.objects.filter(status="published")
            .exclude(sales_channel="pos_only")
            .select_related("category")
            .prefetch_related("images")
            .order_by("-created_at")[:8]
        )

    return render(
        request,
        "page_builder/simple_home.html",
        {
            "categories": categories,
            "featured_products": featured_products,
        },
    )


@allow_iframe_sameorigin
def category_view(request, category_slug=None):
    """Category page view with template config, sorting, and pagination."""
    from design.models import PageTemplateConfig
    from design.template_registry import get_category_options, get_category_template_path

    # Get all top-level categories for navigation
    categories = Category.objects.filter(is_active=True, parent__isnull=True).order_by(
        "sort_order", "name"
    )

    # Get current category if specified
    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug, is_active=True)

    # Template selection and options
    config = PageTemplateConfig.get_config()
    template_key = config.category_template or "grid"
    # Backward compatibility
    if template_key == "default":
        template_key = "grid"
    if category and category.page_template:
        template_key = category.page_template

    # Resolve options: schema defaults < site config < per-category overrides
    site_options = config.category_options or {}
    category_overrides = {}
    if category:
        # Use existing Category model fields as per-category overrides
        if category.products_per_page != 24:
            category_overrides["products_per_page"] = str(category.products_per_page)
        if not category.show_subcategories:
            category_overrides["show_subcategories"] = False
    template_options = get_category_options(template_key, site_options, category_overrides)

    # Accordion: annotate categories with product counts for display
    if template_key == "accordion" and not category:
        from django.db.models import Count

        categories = categories.annotate(product_count=Count("products"))
        categories = list(categories)  # Evaluate queryset once for chunking

    # Build product queryset
    products = Product.objects.filter(status="published", hide_from_storefront=False).exclude(
        sales_channel="pos_only"
    )
    if category:
        descendant_ids = category.get_descendant_ids()
        products = products.filter(category_id__in=descendant_ids)

    # Filter by sales region (matches API behavior)
    from catalog.middleware import get_region_from_request

    region = get_region_from_request(request)
    if region:
        products = products.available_in_region(region)

    # Sorting
    sort_param = request.GET.get("sort", template_options.get("default_sort", "newest"))
    sort_map = {
        "newest": "-created_at",
        "price_low": "price",
        "price_high": "-price",
        "name_az": "name",
        "name_za": "-name",
    }
    order_by = sort_map.get(sort_param, "-created_at")
    products = products.select_related("category").prefetch_related("images").order_by(order_by)

    # Total count before pagination
    total_count = products.count()

    # Carousel: fetch enough products to fill all rows
    per_page = int(template_options.get("products_per_page", 24))
    if template_key == "carousel":
        row_size = int(template_options.get("row_size", 8))
        per_page = max(per_page, row_size * 6)  # Enough for up to 6 rows

    # Pagination
    paginator = Paginator(products, per_page)
    page_num = request.GET.get("page", 1)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    sort_choices = [
        ("newest", _("Newest")),
        ("price_low", _("Price: Low to High")),
        ("price_high", _("Price: High to Low")),
        ("name_az", _("Name: A to Z")),
        ("name_za", _("Name: Z to A")),
    ]

    context = {
        "categories": categories,
        "category": category,
        "products": page_obj,
        "page_obj": page_obj,
        "paginator": paginator,
        "total_count": total_count,
        "current_sort": sort_param,
        "sort_choices": sort_choices,
        "template_options": template_options,
    }

    # Featured: split products into hero and remaining
    if template_key == "featured" and category:
        featured_count = int(template_options.get("featured_products_count", 1))
        all_products = list(page_obj)
        context["featured_products"] = all_products[:featured_count]
        context["remaining_products"] = all_products[featured_count:]

    # Carousel: chunk products into rows (Netflix-style row slices)
    if template_key == "carousel" and category:
        row_size = int(template_options.get("row_size", 8))
        all_products = list(page_obj)
        total = len(all_products)
        carousel_rows = []
        for i in range(0, total, row_size):
            chunk = all_products[i : i + row_size]
            carousel_rows.append(
                {
                    "products": chunk,
                    "start": i + 1,
                    "end": min(i + row_size, total),
                    "total": total,
                }
            )
        context["carousel_rows"] = carousel_rows

    # Accordion: chunk categories into rows (avoids overcrowded single row)
    if template_key == "accordion" and not category:
        panels_per_row = int(template_options.get("panels_per_row", 6))
        cats = (
            context["categories"]
            if isinstance(context["categories"], list)
            else list(context["categories"])
        )
        accordion_rows = [cats[i : i + panels_per_row] for i in range(0, len(cats), panels_per_row)]
        context["accordion_rows"] = accordion_rows

    translate_storefront_context(context, request)
    template_path = get_category_template_path(template_key)
    return render(request, template_path, context)


def products_view(request):
    """All products page — shows every published product with sorting and pagination."""
    from design.models import PageTemplateConfig

    config = PageTemplateConfig.get_config()

    # Build product queryset (same filters as category_view, no category restriction)
    products = Product.objects.filter(status="published", hide_from_storefront=False).exclude(
        sales_channel="pos_only"
    )

    # Filter by sales region
    from catalog.middleware import get_region_from_request

    region = get_region_from_request(request)
    if region:
        products = products.available_in_region(region)

    # Sorting
    sort_param = request.GET.get("sort", "newest")
    sort_map = {
        "newest": "-created_at",
        "price_low": "price",
        "price_high": "-price",
        "name_az": "name",
        "name_za": "-name",
    }
    order_by = sort_map.get(sort_param, "-created_at")
    products = products.select_related("category").prefetch_related("images").order_by(order_by)

    total_count = products.count()

    per_page = int((config.category_options or {}).get("products_per_page", 24))
    paginator = Paginator(products, per_page)
    page_num = request.GET.get("page", 1)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    sort_choices = [
        ("newest", _("Newest")),
        ("price_low", _("Price: Low to High")),
        ("price_high", _("Price: High to Low")),
        ("name_az", _("Name: A to Z")),
        ("name_za", _("Name: Z to A")),
    ]

    context = {
        "products": page_obj,
        "page_obj": page_obj,
        "paginator": paginator,
        "total_count": total_count,
        "current_sort": sort_param,
        "sort_choices": sort_choices,
    }

    translate_storefront_context(context, request)
    return render(request, "page_builder/products/index.html", context)


@allow_iframe_sameorigin
def cart_view(request):
    """Shopping cart page view"""
    return render(request, "page_builder/cart.html")


@allow_iframe_sameorigin
def checkout_view(request):
    """Checkout page - dynamic template selection based on PageTemplateConfig"""
    from django.contrib.auth import REDIRECT_FIELD_NAME

    from core.utils import get_site_settings

    settings = get_site_settings()

    # Check authentication based on account creation timing
    if not request.user.is_authenticated:
        # Only require login if account must be created before checkout
        if settings.account_creation_timing == "before_checkout":
            from django.conf import settings as django_settings

            login_url = getattr(django_settings, "LOGIN_URL", "/accounts/login/")
            return redirect(f"{login_url}?{REDIRECT_FIELD_NAME}={request.get_full_path()}")

    # Check cart has items
    from cart.models import Cart

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        # Guest user - check session-based cart
        cart = (
            Cart.objects.filter(session_key=request.session.session_key).first()
            if request.session.session_key
            else None
        )

    if not cart or cart.total_items == 0:
        return redirect("page_builder:cart")

    context = {}

    # Saved addresses for logged-in users only
    from orders.models import Address

    if request.user.is_authenticated:
        context["saved_addresses"] = Address.objects.filter(
            user=request.user,
            is_active=True,
        ).order_by("-is_default", "-updated_at")
    else:
        context["saved_addresses"] = []

    # Geo country for address autocomplete bias
    geo_location = getattr(request, "geo_location", None)
    context["geo_country"] = ""
    if geo_location:
        if isinstance(geo_location, dict):
            context["geo_country"] = geo_location.get("country_code", "")
        elif hasattr(geo_location, "country_code"):
            context["geo_country"] = geo_location.country_code or ""

    context["user_email"] = request.user.email if request.user.is_authenticated else ""

    # Account creation context
    from accounts.services.account_creation_service import AccountCreationService

    account_context = AccountCreationService.get_account_creation_context(
        user=request.user if request.user.is_authenticated else None
    )

    context.update(
        {
            "account_creation_timing": settings.account_creation_timing,
            "account_creation_message": account_context["account_creation_message"],
            "show_social_auth": account_context["show_social_auth"],
            "social_providers": account_context["social_providers"],
        }
    )

    # Template selection and options
    from design.models import PageTemplateConfig
    from design.template_registry import (
        get_checkout_options,
        get_checkout_template_path,
    )

    config = PageTemplateConfig.get_config()
    template_key = request.GET.get("template") or config.checkout_template
    template_options = get_checkout_options(template_key, config.checkout_options)
    context["template_options"] = template_options
    context["template_options_json"] = json.dumps(template_options)
    context["checkout_trust_badges"] = config.checkout_trust_badges or []

    template_path = get_checkout_template_path(template_key)
    return render(request, template_path, context)


@allow_iframe_sameorigin
def checkout_return_view(request):
    """Handle return from hosted payment provider checkout"""
    from payment_providers.models import PaymentIntent

    # Providers append intent/session IDs in different query params
    intent_id = (
        request.GET.get("intent_id")
        or request.GET.get("payment_intent")
        or request.GET.get("paymentIntentId")
    )

    if intent_id:
        try:
            intent = PaymentIntent.objects.select_related("order").get(id=intent_id)

            if intent.status == "succeeded" and intent.order:
                return redirect(
                    "page_builder:order_confirmation", order_number=intent.order.order_number
                )
            elif intent.status in ("failed", "canceled"):
                from django.contrib import messages

                messages.error(request, _("Payment was not completed. Please try again."))
                return redirect("page_builder:checkout")

            # Still processing - show polling page
            return render(
                request,
                "page_builder/checkout_return.html",
                {
                    "intent_id": str(intent.id),
                    "order_number": intent.order.order_number if intent.order else "",
                },
            )
        except (PaymentIntent.DoesNotExist, ValueError):
            pass

    # No intent_id or not found - render JS-based polling page
    return render(
        request,
        "page_builder/checkout_return.html",
        {
            "intent_id": "",
            "order_number": "",
        },
    )


@allow_iframe_sameorigin
def order_confirmation_view(request, order_number):
    """Order confirmation page after successful payment"""
    from accounts.services.account_creation_service import AccountCreationService
    from core.utils import get_site_settings
    from orders.models import Order

    order = get_object_or_404(Order, order_number=order_number)

    # Security: only allow order owner or staff
    if request.user.is_authenticated:
        if order.user and order.user != request.user and not request.user.is_staff:
            raise Http404
    else:
        raise Http404

    # Check if user is guest and should see account creation prompt
    settings = get_site_settings()
    is_guest_user = request.user.is_authenticated and request.user.username.startswith("guest_")

    context = {
        "order": order,
        "order_items": order.items.select_related("product").all(),
        "is_guest_user": is_guest_user,
        "account_creation_timing": settings.account_creation_timing,
    }

    # Add account creation context if guest user and post_purchase mode
    if is_guest_user and settings.account_creation_timing == "post_purchase":
        account_context = AccountCreationService.get_account_creation_context(user=request.user)
        context.update(
            {
                "account_creation_message": account_context["account_creation_message"],
                "show_social_auth": account_context["show_social_auth"],
                "social_providers": account_context["social_providers"],
            }
        )

    return render(request, "page_builder/order_confirmation.html", context)


@ensure_csrf_cookie
@allow_iframe_sameorigin
def product_view(request, product_slug):
    """Product page view with full context for high-conversion layout"""
    from catalog.models import ProductReview

    # Get product with all related data
    product = get_object_or_404(
        Product.objects.select_related("category", "brand")
        .prefetch_related(
            "images__media_asset",
            "variants__image_asset",
            "variants__selected_attributes__attribute",
            "attribute_assignments__attribute",
            "attribute_assignments__allowed_values",
            "bundle_items__component_product__images__media_asset",
            "bundle_items__component_variant",
        )
        .exclude(sales_channel="pos_only"),
        slug=product_slug,
        status="published",
    )

    # Check region availability (show product but disable purchase if unavailable)
    from catalog.middleware import get_region_from_request

    region = get_region_from_request(request)
    region_unavailable = False
    if region:
        region_unavailable = (
            not Product.objects.filter(pk=product.pk, status="published")
            .available_in_region(region)
            .exists()
        )

    # Configurable products get their own template with wizard UI
    if product.product_type == "configurable":
        return _render_configurator(request, product)

    # Get product images ordered by position
    images = product.images.filter(show_in_gallery=True).order_by("position")

    # Get active variants with their attributes and images
    variants = (
        product.variants.filter(is_active=True)
        .select_related("image_asset")
        .prefetch_related(
            "images__media_asset",
            "selected_attributes__attribute",
        )
    )

    # Build variant data for JavaScript
    variants_data = []
    has_attribute_mappings = False
    for variant in variants:
        # Primary image URL
        image_url = None
        if variant.image_asset and variant.image_asset.original_file:
            image_url = variant.image_asset.get_display_url()
        else:
            first_img = variant.images.first()
            if first_img and first_img.media_asset and first_img.media_asset.original_file:
                image_url = first_img.media_asset.get_display_url()

        # Variant gallery images
        variant_images = []
        for vi in variant.images.all():
            if vi.media_asset and vi.media_asset.original_file:
                variant_images.append(
                    {
                        "url": vi.media_asset.get_display_url(),
                        "alt": vi.alt_text or variant.name,
                    }
                )

        variant_info = {
            "id": variant.id,
            "sku": variant.sku,
            "name": variant.name,
            "price": str(variant.get_effective_price()),
            "image_url": image_url,
            "images": variant_images,
            "in_stock": (not product.track_inventory)
            or variant.stock_status != "out_of_stock"
            or product.allow_backorders,
            "color_swatch": None,
            "attributes": {},
        }
        for attr_value in variant.selected_attributes.all():
            has_attribute_mappings = True
            variant_info["attributes"][attr_value.attribute.slug] = {
                "value": attr_value.value,
                "slug": attr_value.slug,
                "color_hex": attr_value.color_hex,
            }
            # Use color_hex from first color attribute as swatch
            if attr_value.color_hex and not variant_info["color_swatch"]:
                variant_info["color_swatch"] = attr_value.color_hex
        variants_data.append(variant_info)

    # Get attribute assignments for variant selection UI
    attribute_assignments = (
        product.attribute_assignments.all()
        .prefetch_related("attribute", "allowed_values")
        .order_by("sort_order")
    )

    # Get related products from same category
    related_products = (
        Product.objects.filter(category=product.category, status="published")
        .exclude(id=product.id)
        .exclude(sales_channel="pos_only")
        .prefetch_related("images__media_asset")[:4]
    )

    # Get reviews if enabled
    reviews = []
    review_stats = None
    if product.show_reviews:
        reviews = (
            ProductReview.objects.filter(product=product, is_approved=True)
            .select_related("user")
            .order_by("-created_at")[:10]
        )

        # Calculate review statistics
        stats = ProductReview.objects.filter(product=product, is_approved=True).aggregate(
            avg_rating=Avg("rating"),
            total_count=Count("id"),
            five_star=Count("id", filter=Q(rating=5)),
            four_star=Count("id", filter=Q(rating=4)),
            three_star=Count("id", filter=Q(rating=3)),
            two_star=Count("id", filter=Q(rating=2)),
            one_star=Count("id", filter=Q(rating=1)),
        )
        if stats["total_count"] > 0:
            review_stats = {
                "average": round(stats["avg_rating"], 1) if stats["avg_rating"] else 0,
                "total": stats["total_count"],
                "breakdown": {
                    5: {
                        "count": stats["five_star"],
                        "percent": round(stats["five_star"] / stats["total_count"] * 100),
                    },
                    4: {
                        "count": stats["four_star"],
                        "percent": round(stats["four_star"] / stats["total_count"] * 100),
                    },
                    3: {
                        "count": stats["three_star"],
                        "percent": round(stats["three_star"] / stats["total_count"] * 100),
                    },
                    2: {
                        "count": stats["two_star"],
                        "percent": round(stats["two_star"] / stats["total_count"] * 100),
                    },
                    1: {
                        "count": stats["one_star"],
                        "percent": round(stats["one_star"] / stats["total_count"] * 100),
                    },
                },
            }

    # Template selection and options
    from design.models import PageTemplateConfig
    from design.template_registry import (
        get_product_options,
        get_product_template_path,
    )

    config = PageTemplateConfig.get_config()
    template_key = product.page_template or config.product_template

    # Booking products always use the booking template
    if product.product_type == "booking":
        template_key = "booking"

    # Customizable products auto-select designer template unless overridden
    if product.product_type == "customizable" and not product.page_template:
        template_key = "designer"

    site_options = config.product_options or {}
    template_options = get_product_options(template_key, site_options)

    # Express checkout methods
    express_checkout_methods = []
    payments_enabled = False
    try:
        from payment_providers.models import PaymentProviderAccount

        active_accounts = PaymentProviderAccount.objects.filter(is_active=True)
        payments_enabled = active_accounts.exists()
    except Exception:
        pass

    # Bundle items context
    bundle_items = []
    bundle_items_json_str = "[]"
    if product.product_type == "bundle":
        bundle_items = list(
            product.bundle_items.select_related("component_product", "component_variant")
            .prefetch_related(
                "component_product__variants__selected_attributes__attribute",
                "component_product__images__media_asset",
            )
            .order_by("sort_order")
        )
        bundle_items_data = []
        for bi in bundle_items:
            avail_variants = []
            if bi.allow_variant_selection:
                for v in bi.component_product.variants.filter(is_active=True):
                    avail_variants.append(
                        {
                            "id": v.id,
                            "name": v.name,
                            "price": str(v.get_effective_price()),
                        }
                    )
            bundle_items_data.append(
                {
                    "id": bi.id,
                    "component_product_id": bi.component_product_id,
                    "component_product_name": str(bi.component_product.name),
                    "quantity": bi.quantity,
                    "is_optional": bi.is_optional,
                    "allow_variant_selection": bi.allow_variant_selection,
                    "component_variant_id": bi.component_variant_id,
                    "available_variants": avail_variants,
                }
            )
        import json as json_mod

        bundle_items_json_str = json_mod.dumps(bundle_items_data)

    # Product trust badges (configurable from Template Config)
    if template_key == "digital":
        product_trust_badges = config.digital_trust_badges or []
    else:
        product_trust_badges = config.product_trust_badges or []

    # Booking product context
    booking_config = None
    booking_resources = []
    booking_person_types = []
    if product.product_type == "booking":
        from catalog.models import BookingConfig, BookingPersonType, BookingResource

        try:
            booking_config = BookingConfig.objects.get(product=product)
        except BookingConfig.DoesNotExist:
            pass
        booking_resources = list(
            BookingResource.objects.filter(
                product=product, is_active=True, assignment_type="customer_selected"
            ).order_by("sort_order", "name")
        )
        booking_person_types = list(
            BookingPersonType.objects.filter(product=product).order_by("sort_order", "name")
        )

    # Currency info for JS
    from core.models import SiteSettings
    from core.utils.currency_helpers import get_currency_symbol

    site_settings = SiteSettings.get_settings()
    currency_code = site_settings.default_currency
    currency_symbol = get_currency_symbol(currency_code)

    # Design editor context (customizable products)
    has_design_editor = False
    if product.product_type == "customizable":
        try:
            from customizable_product.models import ProductDesignConfig

            design_config = ProductDesignConfig.objects.filter(
                product=product, is_enabled=True, editor_mode="canvas"
            ).first()
            if design_config and design_config.surfaces.filter(is_enabled=True).exists():
                has_design_editor = True
        except Exception:
            pass

    # Product dependencies
    from catalog.models import ProductDependency
    from catalog.services.dependency_service import check_hard_dependencies, get_recommendations

    dep_satisfied = True
    blocking_dependencies = []
    product_dependencies = list(
        ProductDependency.objects.filter(product=product)
        .select_related("required_product")
        .order_by("sort_order", "id")
    )
    if product_dependencies:
        hard_satisfied, blocking_dependencies = check_hard_dependencies(
            product=product,
            user=request.user if request.user.is_authenticated else None,
            cart=None,
        )
        dep_satisfied = hard_satisfied
    soft_recommendations = get_recommendations(product)

    import json

    context = {
        "product": product,
        "images": images,
        "variants": variants,
        "variants_json": json.dumps(variants_data),
        "attribute_assignments": attribute_assignments if has_attribute_mappings else [],
        "has_attribute_mappings": has_attribute_mappings,
        "related_products": related_products,
        "reviews": reviews,
        "review_stats": review_stats,
        "template_options": template_options,
        "payments_enabled": payments_enabled,
        "express_checkout_methods": express_checkout_methods,
        "bundle_items": bundle_items,
        "bundle_items_json": bundle_items_json_str,
        "product_trust_badges": product_trust_badges,
        "booking_config": booking_config,
        "booking_resources": booking_resources,
        "booking_person_types": booking_person_types,
        "currency_code": currency_code,
        "currency_symbol": currency_symbol,
        "region_unavailable": region_unavailable,
        "has_design_editor": has_design_editor,
        "dep_satisfied": dep_satisfied,
        "blocking_dependencies": blocking_dependencies,
        "soft_recommendations": soft_recommendations,
    }

    translate_storefront_context(context, request)
    template_path = get_product_template_path(template_key)
    return render(request, template_path, context)


def _render_configurator(request, product):
    """Render the configurator wizard for configurable products."""
    from catalog.models import CompatibilityRule, ConfigurationPreset
    from catalog.serializers import (
        CompatibilityRuleSerializer,
        ConfigurationPresetSerializer,
        ConfigurationSlotSerializer,
    )

    slots = product.configuration_slots.prefetch_related(
        "options__option_product__images__media_asset",
        "options__option_product__stock_items",
        "options__option_variant",
    ).order_by("sort_order")

    rules = CompatibilityRule.objects.filter(configurable_product=product).prefetch_related(
        "compatible_options"
    )

    presets = (
        ConfigurationPreset.objects.filter(product=product)
        .select_related("image_asset")
        .order_by("sort_order")
    )

    images = product.images.filter(show_in_gallery=True).order_by("position")

    base_price = product.configurator_base_price or product.price
    from core.utils import get_default_currency

    currency = base_price.currency if hasattr(base_price, "currency") else get_default_currency()

    configurator_data = {
        "product_id": product.pk,
        "pricing_strategy": product.configurator_pricing_strategy,
        "base_price": str(base_price.amount) if base_price else "0.00",
        "currency": str(currency),
        "slots": ConfigurationSlotSerializer(slots, many=True, context={"request": request}).data,
        "rules": CompatibilityRuleSerializer(rules, many=True).data,
        "presets": ConfigurationPresetSerializer(
            presets, many=True, context={"request": request}
        ).data,
    }

    # Check for 3D scene — use different template if available
    template = "page_builder/configurator_product.html"
    try:
        from configurator_3d.models import SceneConfig
        from configurator_3d.serializers import serialize_scene_3d

        scene = (
            SceneConfig.objects.select_related("base_model", "environment_image")
            .prefetch_related(
                "mappings__slot_option",
                "geometry_assets__media_asset",
                "textures__media_asset",
            )
            .get(product=product)
        )
        if scene and scene.is_enabled and scene.base_model:
            template = "page_builder/configurator_3d_product.html"
            configurator_data["scene_3d"] = serialize_scene_3d(scene)
            _bloom_strength = scene.bloom_strength or 0
    except (SceneConfig.DoesNotExist, Exception):
        pass

    # Related products from same category
    related_products = []
    if product.category:
        related_products = (
            Product.objects.filter(category=product.category, status="published")
            .exclude(id=product.id)
            .exclude(sales_channel="pos_only")
            .prefetch_related("images__media_asset")[:4]
        )

    # Reviews
    from catalog.models import ProductReview

    reviews = []
    review_stats = None
    if product.show_reviews:
        reviews = (
            ProductReview.objects.filter(product=product, is_approved=True)
            .select_related("user")
            .order_by("-created_at")[:10]
        )

        stats = ProductReview.objects.filter(product=product, is_approved=True).aggregate(
            avg_rating=Avg("rating"),
            total_count=Count("id"),
            five_star=Count("id", filter=Q(rating=5)),
            four_star=Count("id", filter=Q(rating=4)),
            three_star=Count("id", filter=Q(rating=3)),
            two_star=Count("id", filter=Q(rating=2)),
            one_star=Count("id", filter=Q(rating=1)),
        )
        if stats["total_count"] > 0:
            review_stats = {
                "average": round(stats["avg_rating"], 1) if stats["avg_rating"] else 0,
                "total": stats["total_count"],
                "breakdown": {
                    5: {
                        "count": stats["five_star"],
                        "percent": round(stats["five_star"] / stats["total_count"] * 100),
                    },
                    4: {
                        "count": stats["four_star"],
                        "percent": round(stats["four_star"] / stats["total_count"] * 100),
                    },
                    3: {
                        "count": stats["three_star"],
                        "percent": round(stats["three_star"] / stats["total_count"] * 100),
                    },
                    2: {
                        "count": stats["two_star"],
                        "percent": round(stats["two_star"] / stats["total_count"] * 100),
                    },
                    1: {
                        "count": stats["one_star"],
                        "percent": round(stats["one_star"] / stats["total_count"] * 100),
                    },
                },
            }

    # Template options for tabs partial
    from design.models import PageTemplateConfig
    from design.template_registry import get_product_options

    config = PageTemplateConfig.get_config()
    site_options = config.product_options or {}
    template_options = get_product_options("classic", site_options)

    context = {
        "product": product,
        "images": images,
        "configurator_json": json.dumps(configurator_data, cls=DjangoJSONEncoder),
        "bloom_strength": locals().get("_bloom_strength", 0),
        "related_products": related_products,
        "reviews": reviews,
        "review_stats": review_stats,
        "template_options": template_options,
    }
    translate_storefront_context(context, request)
    return render(request, template, context)


@allow_iframe_sameorigin
def page_view(request, slug):
    """Custom page view"""
    view = PageView.as_view()
    return view(request, slug=slug)


@staff_member_required
def visual_builder(request, page_id):
    """Visual drag-and-drop page builder interface"""
    import json

    from django.core.serializers.json import DjangoJSONEncoder

    page = get_object_or_404(
        Page.objects.select_related("theme").prefetch_related("elements"), id=page_id
    )

    # Serialize page data properly for JavaScript
    page_data = {"id": page.id, "title": page.title, "slug": page.slug, "elements": []}

    # Get top-level elements only
    for element in page.elements.filter(parent_element__isnull=True).order_by("order"):
        element_data = {
            "id": element.id,
            "type": element.element_type,
            "name": element.name,
            "content": element.content,  # This will be properly serialized by DjangoJSONEncoder
            "order": element.order,
        }
        page_data["elements"].append(element_data)

    # Convert to JSON string with proper boolean handling
    page_data_json = json.dumps(page_data, cls=DjangoJSONEncoder)

    # Get theme and brand CSS URLs for the canvas preview
    # Use effective_theme to ensure pages always have a theme (fallback to default)
    page_theme_css_url = None
    if page.effective_theme:
        page_theme_css_url = page.effective_theme.css_url

    brand_css_url = None
    try:
        from design.theme_models import ThemeBranding

        branding = ThemeBranding.objects.first()
        if branding:
            brand_css_url = branding.get_css_url()
    except Exception:
        pass

    # Build element metadata for data-driven JS (icons, defaults, names)
    from .element_registry import get_registry

    registry = get_registry()
    element_metadata_json = json.dumps(registry.get_element_metadata(), cls=DjangoJSONEncoder)

    # Flat map of ALL elements (top-level + nested) for client-side style initialization.
    # Eliminates per-element API calls during page builder init (prefetch_related cache = 0 extra queries).
    all_elements_data = {}
    for element in page.elements.all():
        all_elements_data[str(element.id)] = {
            "content": element.content,
            "element_type": element.element_type,
        }
    all_elements_data_json = json.dumps(all_elements_data, cls=DjangoJSONEncoder)

    # Icon registry JSON for icon picker utility
    from core.icon_registry import get_registry_as_json

    icon_registry_json = json.dumps(get_registry_as_json(), ensure_ascii=False)

    # Compute admin page builder URL prefix for JavaScript
    from django.urls import reverse

    admin_pb_prefix = reverse(
        "page_builder_admin:render_element_ajax", kwargs={"element_id": 0}
    ).rsplit("ajax/element/0/", 1)[0]

    return render(
        request,
        "page_builder/visual_builder.html",
        {
            "page": page,
            "page_data_json": page_data_json,
            "all_elements_data_json": all_elements_data_json,
            "page_theme_css_url": page_theme_css_url,
            "brand_css_url": brand_css_url,
            "element_metadata_json": element_metadata_json,
            "icon_registry_json": icon_registry_json,
            "admin_pb_prefix": admin_pb_prefix,
        },
    )


@staff_member_required
@allow_iframe_sameorigin
def page_preview(request, slug):
    """Preview page (including draft pages) - staff only"""
    from .element_registry import get_registry

    page = get_object_or_404(
        Page.objects.select_related("theme").prefetch_related("elements"), slug=slug
    )

    elements = page.elements.filter(parent_element__isnull=True).order_by("order")

    # Get theme CSS URL for the page (use effective_theme like visual_builder)
    page_theme_css_url = None
    if page.effective_theme:
        page_theme_css_url = page.effective_theme.css_url

    # Get brand CSS URL if available
    brand_css_url = None
    try:
        from design.theme_models import ThemeBranding

        branding = ThemeBranding.objects.first()
        if branding:
            brand_css_url = branding.get_css_url()
    except Exception:
        pass

    # Collect element scripts and CSS
    registry = get_registry()
    element_scripts = set()
    element_css_files = set()

    def collect_assets(element_queryset):
        for element in element_queryset:
            if not element.is_active:
                continue
            element_config = registry.get_element(element.element_type)
            if element_config:
                if element_config.scripts:
                    element_scripts.update(element_config.scripts)
                if element_config.css_files:
                    element_css_files.update(element_config.css_files)
            children = element.child_elements.filter(is_active=True)
            if children.exists():
                collect_assets(children)

    collect_assets(elements)

    context = {
        "page": page,
        "elements": elements,
        "page_title": _(f"Preview: {page.title or page.slug}"),
        "is_preview": True,
        "capture_mode": request.GET.get("capture") == "1",
        "page_theme_css_url": page_theme_css_url,
        "brand_css_url": brand_css_url,
        "element_scripts": list(element_scripts),
        "element_css_files": list(element_css_files),
    }

    return render(request, "page_builder/page.html", context)


def get_active_languages():
    """Get active languages from the translations app"""
    try:
        from page_builder.translation_utils import get_primary_language
        from translations.models import SiteLanguage

        primary_lang = get_primary_language()
        languages = []

        # Get all active languages
        for lang in SiteLanguage.objects.filter(is_active=True).order_by("order", "name"):
            languages.append(
                {
                    "code": lang.code,
                    "name": lang.name,
                    "is_primary": lang.code == primary_lang,
                }
            )
        return languages
    except ImportError:
        # Fallback if translations app not available
        from django.conf import settings

        languages = []
        for code, name in getattr(settings, "LANGUAGES", [("en", "English")]):
            languages.append(
                {
                    "code": code,
                    "name": name,
                    "is_primary": code == settings.LANGUAGE_CODE,
                }
            )
        return languages


@staff_member_required
def builder_preview(request, slug):
    """Preview wrapper with device controls for page builder"""
    from django.urls import reverse

    page = get_object_or_404(Page, slug=slug)

    # Get active languages for the switcher
    languages = get_active_languages()

    preview_url = reverse("page_builder_admin:page_preview", kwargs={"slug": slug})

    context = {
        "page": page,
        "preview_url": preview_url,
        "page_title": _(f"Preview: {page.title or page.slug}"),
        "languages": languages,
    }

    return render(request, "page_builder/builder_preview.html", context)


# Section rendering removed - sections no longer exist
# def render_section_ajax(request, section_id):
#     """AJAX view to render individual sections - REMOVED"""
#     pass


@staff_member_required
def render_element_ajax(request, element_id):
    """AJAX view to render individual elements - staff only"""
    from .element_registry import get_registry

    element = get_object_or_404(
        Element.objects.select_related("page"), id=element_id, is_active=True
    )

    registry = get_registry()
    element_config = registry.get_element(element.element_type)

    # Check if visual builder mode is requested
    is_visual_builder = request.GET.get("visual_builder", "").lower() in ("true", "1", "yes")

    context = {
        "element": element,
        "element_config": element_config,
        "is_visual_builder": is_visual_builder,
    }

    # Use modular template if available, fallback to old template
    if element_config:
        template_path = f"page_builder/elements/{element.element_type}/template.html"
    else:
        template_path = f"page_builder/elements/{element.element_type}.html"

    return render(request, template_path, context)
