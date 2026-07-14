import json

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST

from catalog.models import Product
from core.utils import get_default_currency

from .models import (
    ClipartAsset,
    ClipartCategory,
    CustomFont,
    DesignDraft,
    ProductDesignConfig,
    SavedDesign,
)
from .services.design_service import DesignPricingService


@require_GET
def editor_config(request, product_id):
    """Return full editor configuration for a customizable product."""
    product = get_object_or_404(
        Product,
        pk=product_id,
        product_type="customizable",
        allow_customization=True,
    )

    try:
        design_config = product.design_config
    except ProductDesignConfig.DoesNotExist:
        return JsonResponse({"error": "Product has no design configuration"}, status=404)

    if not design_config.is_enabled:
        return JsonResponse({"error": "Design editor is not enabled for this product"}, status=404)

    # Surfaces
    surfaces = []
    for surface in design_config.surfaces.filter(is_enabled=True).order_by("sort_order"):
        surfaces.append(
            {
                "id": surface.id,
                "name": surface.name,
                "slug": surface.slug,
                "mockup_url": surface.mockup_image.original_file.url
                if surface.mockup_image
                else None,
                "dimension_unit": surface.dimension_unit,
                "width": str(surface.width),
                "height": str(surface.height),
                "area_x_percent": str(surface.area_x_percent),
                "area_y_percent": str(surface.area_y_percent),
                "area_width_percent": str(surface.area_width_percent),
                "area_height_percent": str(surface.area_height_percent),
                "min_dpi": surface.min_dpi,
                "recommended_dpi": surface.recommended_dpi,
                "background_color": surface.background_color,
                "allow_text": surface.get_effective_allow_text(),
                "allow_image_upload": surface.get_effective_allow_image_upload(),
                "allow_clipart": surface.get_effective_allow_clipart(),
                "max_elements": surface.max_elements,
            }
        )

    # Clipart categories (global + product-specific)
    clipart_categories = []
    for cat in ClipartCategory.objects.filter(is_active=True).order_by("sort_order"):
        asset_count = (
            ClipartAsset.objects.filter(
                category=cat,
                is_active=True,
            )
            .filter(Q(scope="global") | Q(scope="product", product=product))
            .count()
        )
        if asset_count > 0:
            clipart_categories.append(
                {
                    "id": cat.id,
                    "name": cat.name,
                    "slug": cat.slug,
                    "icon": cat.icon,
                    "asset_count": asset_count,
                }
            )

    # Fonts
    fonts = []
    for font in CustomFont.objects.filter(is_active=True).order_by("sort_order"):
        font_data = {
            "id": font.id,
            "name": font.name,
            "family": font.family,
            "is_system_font": font.is_system_font,
        }
        if not font.is_system_font and font.regular:
            font_data["regular_url"] = font.regular.original_file.url
        if font.bold:
            font_data["bold_url"] = font.bold.original_file.url
        if font.italic:
            font_data["italic_url"] = font.italic.original_file.url
        if font.bold_italic:
            font_data["bold_italic_url"] = font.bold_italic.original_file.url
        fonts.append(font_data)

    # Templates
    templates = []
    for template in design_config.templates.filter(is_active=True).order_by("sort_order"):
        templates.append(
            {
                "id": template.id,
                "name": template.name,
                "slug": template.slug,
                "description": template.description,
                "category": template.category,
                "thumbnail_url": template.thumbnail.original_file.url
                if template.thumbnail
                else None,
                "design_data": template.design_data,
            }
        )

    # Pricing rules
    pricing = {
        "base_design_fee": str(design_config.base_design_fee.amount)
        if design_config.base_design_fee
        else "0",
        "per_surface_fee": str(design_config.per_surface_fee.amount)
        if design_config.per_surface_fee
        else "0",
        "per_upload_fee": str(design_config.per_upload_fee.amount)
        if design_config.per_upload_fee
        else "0",
        "per_text_fee": str(design_config.per_text_fee.amount)
        if design_config.per_text_fee
        else "0",
        "currency": str(design_config.base_design_fee_currency)
        if design_config.base_design_fee
        else get_default_currency(),
    }

    return JsonResponse(
        {
            "product_id": product.id,
            "product_name": product.name,
            "editor_mode": design_config.editor_mode,
            "allow_image_upload": design_config.allow_image_upload,
            "allow_text": design_config.allow_text,
            "allow_clipart": design_config.allow_clipart,
            "max_uploads_per_surface": design_config.max_uploads_per_surface,
            "max_upload_size_mb": str(design_config.max_upload_size_mb),
            "allowed_upload_types": design_config.allowed_upload_types,
            "surfaces": surfaces,
            "clipart_categories": clipart_categories,
            "fonts": fonts,
            "templates": templates,
            "pricing": pricing,
        }
    )


@require_POST
def upload_image(request):
    """Handle customer image upload for the design editor."""
    from media_library.models import MediaAsset

    if not request.FILES.get("image"):
        return JsonResponse({"error": "No image file provided"}, status=400)

    image_file = request.FILES["image"]

    # Validate file type
    allowed_extensions = ["jpg", "jpeg", "png", "webp"]
    ext = image_file.name.rsplit(".", 1)[-1].lower() if "." in image_file.name else ""
    if ext not in allowed_extensions:
        return JsonResponse(
            {
                "error": f"File type .{ext} is not allowed. Accepted: {', '.join(allowed_extensions)}"
            },
            status=400,
        )

    # Validate file size using product config if available
    max_size_mb = 10  # Default 10MB
    product_id = request.POST.get("product_id")
    if product_id:
        try:
            config = ProductDesignConfig.objects.get(product_id=product_id, is_enabled=True)
            max_size_mb = float(config.max_upload_size_mb)
        except (ProductDesignConfig.DoesNotExist, ValueError):
            pass
    max_size = int(max_size_mb * 1024 * 1024)
    if image_file.size > max_size:
        return JsonResponse(
            {"error": f"File size exceeds maximum allowed ({max_size_mb}MB)"}, status=400
        )

    # Detect MIME type and image dimensions
    import mimetypes

    mime_type, _ = mimetypes.guess_type(image_file.name)
    if not mime_type:
        mime_type = image_file.content_type or "application/octet-stream"

    width = None
    height = None
    if mime_type.startswith("image/"):
        try:
            from PIL import Image

            image_file.seek(0)
            img = Image.open(image_file)
            width, height = img.size
            image_file.seek(0)
        except Exception:
            pass

    # Create MediaAsset with required metadata
    asset = MediaAsset(
        title=f"Customer upload: {image_file.name}",
        alt_text="Customer uploaded design image",
        file_size=image_file.size,
        mime_type=mime_type,
        width=width,
        height=height,
    )
    asset.original_file.save(image_file.name, image_file, save=True)

    return JsonResponse(
        {
            "success": True,
            "asset_id": asset.id,
            "url": asset.original_file.url,
            "filename": image_file.name,
        }
    )


@require_GET
def clipart_list(request):
    """List clipart assets, optionally filtered by category and search."""
    category_slug = request.GET.get("category", "")
    search_query = request.GET.get("search", "")
    product_id = request.GET.get("product_id", "")

    queryset = ClipartAsset.objects.filter(is_active=True).select_related("category", "media_asset")

    # Scope filter: global assets + product-specific assets
    if product_id:
        queryset = queryset.filter(Q(scope="global") | Q(scope="product", product_id=product_id))
    else:
        queryset = queryset.filter(scope="global")

    if category_slug:
        queryset = queryset.filter(category__slug=category_slug)

    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) | Q(tags__contains=[search_query])
        )

    assets = []
    for asset in queryset.order_by("sort_order")[:100]:
        assets.append(
            {
                "id": asset.id,
                "name": asset.name,
                "category": asset.category.name,
                "category_slug": asset.category.slug,
                "url": asset.media_asset.original_file.url,
                "tags": asset.tags,
            }
        )

    return JsonResponse({"assets": assets})


@require_GET
def font_list(request):
    """List available fonts for the design editor."""
    fonts = []
    for font in CustomFont.objects.filter(is_active=True).order_by("sort_order"):
        font_data = {
            "id": font.id,
            "name": font.name,
            "family": font.family,
            "is_system_font": font.is_system_font,
        }
        if not font.is_system_font and font.regular:
            font_data["regular_url"] = font.regular.original_file.url
        if font.bold:
            font_data["bold_url"] = font.bold.original_file.url
        if font.italic:
            font_data["italic_url"] = font.italic.original_file.url
        if font.bold_italic:
            font_data["bold_italic_url"] = font.bold_italic.original_file.url
        fonts.append(font_data)

    return JsonResponse({"fonts": fonts})


@require_GET
def template_list(request, product_id):
    """List design templates for a specific product."""
    product = get_object_or_404(Product, pk=product_id, product_type="customizable")

    try:
        design_config = product.design_config
    except ProductDesignConfig.DoesNotExist:
        return JsonResponse({"templates": []})

    templates = []
    for template in design_config.templates.filter(is_active=True).order_by("sort_order"):
        templates.append(
            {
                "id": template.id,
                "name": template.name,
                "slug": template.slug,
                "description": template.description,
                "category": template.category,
                "thumbnail_url": template.thumbnail.original_file.url
                if template.thumbnail
                else None,
                "design_data": template.design_data,
            }
        )

    return JsonResponse({"templates": templates})


@require_GET
def saved_design_list(request):
    """List saved designs for the current user."""
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)

    product_id = request.GET.get("product_id", "")

    queryset = SavedDesign.objects.filter(user=request.user).select_related("product")
    if product_id:
        queryset = queryset.filter(product_id=product_id)

    designs = []
    for design in queryset.order_by("-updated_at")[:50]:
        designs.append(
            {
                "id": design.id,
                "name": design.name,
                "product_id": design.product_id,
                "product_name": design.product.name,
                "thumbnails": design.thumbnails,
                "created_at": design.created_at.isoformat(),
                "updated_at": design.updated_at.isoformat(),
            }
        )

    return JsonResponse({"designs": designs})


@require_POST
def save_design(request):
    """Save or update a customer's design."""
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    product_id = body.get("product_id")
    design_id = body.get("design_id")
    name = body.get("name", "")
    design_data = body.get("design_data", {})
    thumbnails = body.get("thumbnails", {})

    if not product_id or not name:
        return JsonResponse({"error": "product_id and name are required"}, status=400)

    product = get_object_or_404(Product, pk=product_id, product_type="customizable")

    if design_id:
        design = get_object_or_404(SavedDesign, pk=design_id, user=request.user)
        design.name = name
        design.design_data = design_data
        design.thumbnails = thumbnails
    else:
        design = SavedDesign(
            user=request.user,
            product=product,
            name=name,
            design_data=design_data,
            thumbnails=thumbnails,
        )

    design.save()

    return JsonResponse(
        {
            "success": True,
            "design_id": design.id,
            "name": design.name,
        }
    )


@require_GET
def saved_design_detail(request, design_id):
    """Load a specific saved design."""
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)

    design = get_object_or_404(SavedDesign, pk=design_id, user=request.user)

    return JsonResponse(
        {
            "id": design.id,
            "name": design.name,
            "product_id": design.product_id,
            "design_data": design.design_data,
            "thumbnails": design.thumbnails,
            "created_at": design.created_at.isoformat(),
            "updated_at": design.updated_at.isoformat(),
        }
    )


@require_POST
def delete_saved_design(request, design_id):
    """Delete a specific saved design."""
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)

    design = get_object_or_404(SavedDesign, pk=design_id, user=request.user)
    design.delete()

    return JsonResponse({"success": True})


@require_POST
def calculate_price(request):
    """Calculate pricing for a design based on its elements."""
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    product_id = body.get("product_id")
    design_data = body.get("design_data", {})

    if not product_id:
        return JsonResponse({"error": "product_id is required"}, status=400)

    product = get_object_or_404(Product, pk=product_id, product_type="customizable")

    try:
        design_config = product.design_config
    except ProductDesignConfig.DoesNotExist:
        return JsonResponse({"error": "Product has no design configuration"}, status=404)

    breakdown = DesignPricingService.calculate(design_config, design_data)

    return JsonResponse({"pricing": breakdown})


@require_POST
def prepare_for_cart(request):
    """Validate design, create a DesignDraft, and return a token for the cart."""
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    product_id = body.get("product_id")
    design_data = body.get("design_data", {})
    thumbnails = body.get("thumbnails", {})

    if not product_id:
        return JsonResponse({"error": "product_id is required"}, status=400)

    product = get_object_or_404(Product, pk=product_id, product_type="customizable")

    try:
        design_config = product.design_config
    except ProductDesignConfig.DoesNotExist:
        return JsonResponse({"error": "Product has no design configuration"}, status=404)

    # Validate design has at least one element
    surfaces = design_data.get("surfaces", {})
    has_elements = False
    for surface_data in surfaces.values():
        canvas_json = surface_data.get("canvas_json", {})
        if canvas_json.get("objects"):
            has_elements = True
            break

    if not has_elements:
        return JsonResponse({"error": "Design must have at least one element"}, status=400)

    # Calculate pricing
    pricing_breakdown = DesignPricingService.calculate(design_config, design_data)

    # Create the draft
    draft = DesignDraft(
        product=product,
        design_data=design_data,
        thumbnails=thumbnails,
        pricing_breakdown=pricing_breakdown,
        session_key=request.session.session_key or "",
        user=request.user if request.user.is_authenticated else None,
        expires_at=timezone.now() + timezone.timedelta(days=7),
    )
    draft.save()

    return JsonResponse(
        {
            "success": True,
            "design_token": str(draft.token),
            "pricing": pricing_breakdown,
        }
    )
