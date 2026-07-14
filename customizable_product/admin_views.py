import json

from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.http import require_GET, require_POST

from catalog.models import Product

from .models import (
    ClipartCategory,
    CustomFont,
    DesignTemplate,
    ProductDesignConfig,
    ProductSurface,
)


@staff_member_required
def design_setup(request, product_id):
    """Main admin page for setting up a customizable product's design editor."""
    product = get_object_or_404(Product, pk=product_id, product_type="customizable")

    # Get or create the design config
    design_config, created = ProductDesignConfig.objects.get_or_create(
        product=product,
    )

    surfaces = list(design_config.surfaces.filter(is_enabled=True).order_by("sort_order"))
    templates = list(design_config.templates.filter(is_active=True).order_by("sort_order"))

    # Prepare data for the template
    surfaces_data = []
    for surface in surfaces:
        surfaces_data.append(
            {
                "id": surface.id,
                "name": surface.name,
                "slug": surface.slug,
                "sort_order": surface.sort_order,
                "mockup_url": surface.mockup_image.original_file.url
                if surface.mockup_image
                else None,
                "mockup_asset_id": str(surface.mockup_image_id)
                if surface.mockup_image_id
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
                "bleed_mm": str(surface.bleed_mm),
                "max_colors": surface.max_colors,
                "background_color": surface.background_color,
                "allow_text": surface.allow_text,
                "allow_image_upload": surface.allow_image_upload,
                "allow_clipart": surface.allow_clipart,
                "max_elements": surface.max_elements,
            }
        )

    templates_data = []
    for template in templates:
        templates_data.append(
            {
                "id": template.id,
                "name": template.name,
                "slug": template.slug,
                "description": template.description,
                "category": template.category,
                "thumbnail_url": template.thumbnail.original_file.url
                if template.thumbnail
                else None,
                "is_active": template.is_active,
                "sort_order": template.sort_order,
            }
        )

    setup_data = {
        "productId": product.id,
        "productName": product.name,
        "config": {
            "id": design_config.id,
            "is_enabled": design_config.is_enabled,
            "editor_mode": design_config.editor_mode,
            "allow_image_upload": design_config.allow_image_upload,
            "allow_text": design_config.allow_text,
            "allow_clipart": design_config.allow_clipart,
            "max_uploads_per_surface": design_config.max_uploads_per_surface,
            "max_upload_size_mb": str(design_config.max_upload_size_mb),
            "allowed_upload_types": design_config.allowed_upload_types,
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
        },
        "surfaces": surfaces_data,
        "templates": templates_data,
        "urls": {
            "listSurfaces": reverse("customizable_product:list_surfaces", args=[product_id]),
            "saveSurface": reverse("customizable_product:save_surface", args=[product_id]),
            "deleteSurfaceBase": reverse("customizable_product:list_surfaces", args=[product_id]),
            "listTemplates": reverse("customizable_product:list_templates", args=[product_id]),
            "saveTemplate": reverse("customizable_product:save_template", args=[product_id]),
            "deleteTemplateBase": reverse("customizable_product:list_templates", args=[product_id]),
            "saveConfig": reverse("customizable_product:save_config", args=[product_id]),
            "captureThumbnail": reverse(
                "customizable_product:capture_thumbnail", args=[product_id]
            ),
        },
        "csrfToken": request.META.get("CSRF_COOKIE", ""),
        "strings": {
            "saveSurface": _("Save Surface"),
            "deleteSurface": _("Delete Surface"),
            "addSurface": _("Add Surface"),
            "surfaceName": _("Surface Name"),
            "mockupImage": _("Mockup Image"),
            "designZone": _("Design Zone"),
            "saveTemplate": _("Save Template"),
            "deleteTemplate": _("Delete Template"),
            "addTemplate": _("Add Template"),
            "saveSuccess": _("Saved successfully"),
            "deleteConfirm": _("Are you sure you want to delete this?"),
            "error": _("An error occurred"),
        },
    }

    context = {
        "product": product,
        "design_config": design_config,
        "setup_data_json": json.dumps(setup_data),
        "title": _("Design Editor Setup: %(product)s") % {"product": product.name},
    }

    return render(request, "admin/customizable_product/design_setup.html", context)


@staff_member_required
@require_GET
def list_surfaces(request, product_id):
    """List all surfaces for a product's design config."""
    product = get_object_or_404(Product, pk=product_id, product_type="customizable")
    design_config = get_object_or_404(ProductDesignConfig, product=product)

    surfaces = design_config.surfaces.order_by("sort_order")
    data = []
    for surface in surfaces:
        data.append(
            {
                "id": surface.id,
                "name": surface.name,
                "slug": surface.slug,
                "sort_order": surface.sort_order,
                "mockup_url": surface.mockup_image.original_file.url
                if surface.mockup_image
                else None,
                "mockup_asset_id": str(surface.mockup_image_id)
                if surface.mockup_image_id
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
                "bleed_mm": str(surface.bleed_mm),
                "max_colors": surface.max_colors,
                "background_color": surface.background_color,
                "is_enabled": surface.is_enabled,
                "allow_text": surface.allow_text,
                "allow_image_upload": surface.allow_image_upload,
                "allow_clipart": surface.allow_clipart,
                "max_elements": surface.max_elements,
            }
        )

    return JsonResponse({"surfaces": data})


@staff_member_required
@require_POST
def save_surface(request, product_id):
    """Create or update a product surface."""
    product = get_object_or_404(Product, pk=product_id, product_type="customizable")
    design_config = get_object_or_404(ProductDesignConfig, product=product)

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": _("Invalid JSON")}, status=400)

    surface_id = body.get("id")
    if surface_id:
        surface = get_object_or_404(ProductSurface, pk=surface_id, design_config=design_config)
    else:
        surface = ProductSurface(design_config=design_config)

    # Update fields
    surface.name = body.get("name", surface.name)
    surface.slug = body.get("slug", surface.slug)
    surface.sort_order = body.get("sort_order", surface.sort_order)
    surface.dimension_unit = body.get("dimension_unit", surface.dimension_unit)

    if "width" in body:
        surface.width = body["width"]
    if "height" in body:
        surface.height = body["height"]
    if "area_x_percent" in body:
        surface.area_x_percent = body["area_x_percent"]
    if "area_y_percent" in body:
        surface.area_y_percent = body["area_y_percent"]
    if "area_width_percent" in body:
        surface.area_width_percent = body["area_width_percent"]
    if "area_height_percent" in body:
        surface.area_height_percent = body["area_height_percent"]
    if "min_dpi" in body:
        surface.min_dpi = body["min_dpi"]
    if "recommended_dpi" in body:
        surface.recommended_dpi = body["recommended_dpi"]
    if "bleed_mm" in body:
        surface.bleed_mm = body["bleed_mm"]
    if "max_colors" in body:
        surface.max_colors = body["max_colors"]
    if "background_color" in body:
        surface.background_color = body["background_color"]
    if "is_enabled" in body:
        surface.is_enabled = body["is_enabled"]

    # Per-surface constraint overrides (None = inherit from config)
    if "allow_text" in body:
        surface.allow_text = body["allow_text"]
    if "allow_image_upload" in body:
        surface.allow_image_upload = body["allow_image_upload"]
    if "allow_clipart" in body:
        surface.allow_clipart = body["allow_clipart"]
    if "max_elements" in body:
        surface.max_elements = body["max_elements"]

    # Handle mockup image (MediaAsset ID)
    if "mockup_asset_id" in body:
        from media_library.models import MediaAsset

        if body["mockup_asset_id"]:
            try:
                asset = MediaAsset.objects.get(pk=body["mockup_asset_id"])
                surface.mockup_image = asset
            except MediaAsset.DoesNotExist:
                return JsonResponse({"error": _("Media asset not found")}, status=400)
        else:
            surface.mockup_image = None

    surface.save()

    return JsonResponse(
        {
            "success": True,
            "surface": {
                "id": surface.id,
                "name": surface.name,
                "slug": surface.slug,
            },
        }
    )


@staff_member_required
@require_POST
def delete_surface(request, product_id, surface_id):
    """Delete a product surface."""
    product = get_object_or_404(Product, pk=product_id, product_type="customizable")
    design_config = get_object_or_404(ProductDesignConfig, product=product)
    surface = get_object_or_404(ProductSurface, pk=surface_id, design_config=design_config)

    surface.delete()
    return JsonResponse({"success": True})


@staff_member_required
@require_GET
def list_templates(request, product_id):
    """List all design templates for a product."""
    product = get_object_or_404(Product, pk=product_id, product_type="customizable")
    design_config = get_object_or_404(ProductDesignConfig, product=product)

    templates = design_config.templates.order_by("sort_order")
    data = []
    for template in templates:
        data.append(
            {
                "id": template.id,
                "name": template.name,
                "slug": template.slug,
                "description": template.description,
                "category": template.category,
                "thumbnail_url": template.thumbnail.original_file.url
                if template.thumbnail
                else None,
                "is_active": template.is_active,
                "sort_order": template.sort_order,
            }
        )

    return JsonResponse({"templates": data})


@staff_member_required
@require_POST
def save_template(request, product_id):
    """Create or update a design template."""
    product = get_object_or_404(Product, pk=product_id, product_type="customizable")
    design_config = get_object_or_404(ProductDesignConfig, product=product)

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": _("Invalid JSON")}, status=400)

    template_id = body.get("id")
    if template_id:
        template = get_object_or_404(DesignTemplate, pk=template_id, design_config=design_config)
    else:
        template = DesignTemplate(design_config=design_config)

    template.name = body.get("name", template.name)
    template.slug = body.get("slug", template.slug)
    template.description = body.get("description", template.description or "")
    template.category = body.get("category", template.category or "")
    template.sort_order = body.get("sort_order", template.sort_order)

    if "design_data" in body:
        template.design_data = body["design_data"]
    if "is_active" in body:
        template.is_active = body["is_active"]

    # Handle thumbnail (MediaAsset ID)
    if "thumbnail_asset_id" in body:
        from media_library.models import MediaAsset

        if body["thumbnail_asset_id"]:
            try:
                asset = MediaAsset.objects.get(pk=body["thumbnail_asset_id"])
                template.thumbnail = asset
            except MediaAsset.DoesNotExist:
                return JsonResponse({"error": _("Media asset not found")}, status=400)
        else:
            template.thumbnail = None

    template.save()

    return JsonResponse(
        {
            "success": True,
            "template": {
                "id": template.id,
                "name": template.name,
                "slug": template.slug,
            },
        }
    )


@staff_member_required
@require_POST
def delete_template(request, product_id, template_id):
    """Delete a design template."""
    product = get_object_or_404(Product, pk=product_id, product_type="customizable")
    design_config = get_object_or_404(ProductDesignConfig, product=product)
    template = get_object_or_404(DesignTemplate, pk=template_id, design_config=design_config)

    template.delete()
    return JsonResponse({"success": True})


@staff_member_required
@require_POST
def capture_thumbnail(request, product_id):
    """Save a canvas screenshot as a MediaAsset thumbnail."""
    import base64

    from django.core.files.base import ContentFile

    from media_library.models import MediaAsset

    product = get_object_or_404(Product, pk=product_id, product_type="customizable")

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": _("Invalid JSON")}, status=400)

    image_data = body.get("image_data", "")
    target_type = body.get("target_type", "")  # 'surface' or 'template'
    target_id = body.get("target_id")

    if not image_data:
        return JsonResponse({"error": _("No image data provided")}, status=400)

    # Parse base64 data URL
    if "," in image_data:
        image_data = image_data.split(",", 1)[1]

    try:
        image_bytes = base64.b64decode(image_data)
    except Exception:
        return JsonResponse({"error": _("Invalid image data")}, status=400)

    # Create MediaAsset
    filename = f"design_thumbnail_{product.slug}_{target_type}_{target_id}.png"
    asset = MediaAsset(
        title=f"Design Thumbnail - {product.name}",
        alt_text=f"Design thumbnail for {product.name}",
    )
    asset.original_file.save(filename, ContentFile(image_bytes), save=True)

    return JsonResponse(
        {
            "success": True,
            "asset_id": asset.id,
            "url": asset.original_file.url,
        }
    )


@staff_member_required
@require_POST
def save_config(request, product_id):
    """Save design config settings (pricing, feature toggles, upload restrictions)."""
    product = get_object_or_404(Product, pk=product_id, product_type="customizable")
    design_config = get_object_or_404(ProductDesignConfig, product=product)

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": _("Invalid JSON")}, status=400)

    # Update feature toggles
    if "is_enabled" in body:
        design_config.is_enabled = body["is_enabled"]
    if "editor_mode" in body:
        design_config.editor_mode = body["editor_mode"]
    if "allow_image_upload" in body:
        design_config.allow_image_upload = body["allow_image_upload"]
    if "allow_text" in body:
        design_config.allow_text = body["allow_text"]
    if "allow_clipart" in body:
        design_config.allow_clipart = body["allow_clipart"]

    # Upload restrictions
    if "max_uploads_per_surface" in body:
        design_config.max_uploads_per_surface = body["max_uploads_per_surface"]
    if "max_upload_size_mb" in body:
        design_config.max_upload_size_mb = body["max_upload_size_mb"]
    if "allowed_upload_types" in body:
        design_config.allowed_upload_types = body["allowed_upload_types"]

    # Pricing
    if "base_design_fee" in body:
        design_config.base_design_fee = body["base_design_fee"]
    if "per_surface_fee" in body:
        design_config.per_surface_fee = body["per_surface_fee"]
    if "per_upload_fee" in body:
        design_config.per_upload_fee = body["per_upload_fee"]
    if "per_text_fee" in body:
        design_config.per_text_fee = body["per_text_fee"]

    design_config.save()

    return JsonResponse({"success": True})


@staff_member_required
def template_editor(request, product_id):
    """Full-page visual template editor using Fabric.js canvas."""
    product = get_object_or_404(Product, pk=product_id, product_type="customizable")
    design_config = get_object_or_404(ProductDesignConfig, product=product)

    template_id = request.GET.get("template_id")
    template = None
    if template_id:
        template = get_object_or_404(DesignTemplate, pk=template_id, design_config=design_config)

    # Surfaces with mockup data
    surfaces_data = []
    for surface in design_config.surfaces.filter(is_enabled=True).order_by("sort_order"):
        surfaces_data.append(
            {
                "id": surface.id,
                "name": surface.name,
                "slug": surface.slug,
                "mockup_url": surface.mockup_image.original_file.url
                if surface.mockup_image
                else None,
                "area_x_percent": str(surface.area_x_percent),
                "area_y_percent": str(surface.area_y_percent),
                "area_width_percent": str(surface.area_width_percent),
                "area_height_percent": str(surface.area_height_percent),
                "background_color": surface.background_color,
                "width": str(surface.width),
                "height": str(surface.height),
                "dimension_unit": surface.dimension_unit,
            }
        )

    # Fonts
    fonts_data = []
    for font in CustomFont.objects.filter(is_active=True).order_by("sort_order"):
        font_entry = {
            "id": font.id,
            "name": font.name,
            "family": font.family,
            "is_system_font": font.is_system_font,
        }
        if not font.is_system_font and font.regular:
            font_entry["regular_url"] = font.regular.original_file.url
        if font.bold:
            font_entry["bold_url"] = font.bold.original_file.url
        if font.italic:
            font_entry["italic_url"] = font.italic.original_file.url
        fonts_data.append(font_entry)

    # Clipart categories
    from django.db.models import Q

    clipart_categories = []
    for cat in ClipartCategory.objects.filter(is_active=True).order_by("sort_order"):
        from .models import ClipartAsset

        count = (
            ClipartAsset.objects.filter(
                category=cat,
                is_active=True,
            )
            .filter(Q(scope="global") | Q(scope="product", product=product))
            .count()
        )
        if count > 0:
            clipart_categories.append(
                {
                    "id": cat.id,
                    "name": cat.name,
                    "slug": cat.slug,
                    "icon": cat.icon,
                }
            )

    editor_data = {
        "productId": product.id,
        "productName": product.name,
        "surfaces": surfaces_data,
        "fonts": fonts_data,
        "clipartCategories": clipart_categories,
        "template": {
            "id": template.id,
            "name": template.name,
            "slug": template.slug,
            "description": template.description or "",
            "category": template.category or "",
            "design_data": template.design_data or {},
            "sort_order": template.sort_order,
        }
        if template
        else None,
        "urls": {
            "saveTemplate": reverse("customizable_product:save_template", args=[product_id]),
            "captureThumbnail": reverse(
                "customizable_product:capture_thumbnail", args=[product_id]
            ),
            "clipartApi": "/api/customizable-product/clipart/",
            "uploadImage": "/api/customizable-product/upload-image/",
            "designSetup": reverse("customizable_product:design_setup", args=[product_id]),
        },
        "csrfToken": request.META.get("CSRF_COOKIE", ""),
    }

    context = {
        "product": product,
        "design_config": design_config,
        "template": template,
        "editor_data_json": json.dumps(editor_data),
        "title": _("Template Editor: %(product)s") % {"product": product.name},
    }

    return render(request, "admin/customizable_product/template_editor.html", context)
