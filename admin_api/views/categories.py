"""
Admin API Category Views

Category management endpoints for the merchant admin API.
"""

import logging
import mimetypes
import secrets

from django.conf import settings
from django.db import IntegrityError, transaction
from django.db.models import Count, Q
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiParameter, extend_schema
from PIL import Image
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes, permission_classes, throttle_classes
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from admin_api.permissions import IsStaffWithWritePermission
from admin_api.serializers.auth import ErrorResponseSerializer
from admin_api.serializers.categories import (
    AdminCategoryDetailSerializer,
    AdminCategoryListSerializer,
    BulkCategoryCreateSerializer,
    CategoryCreateSerializer,
    CategoryFilterSerializer,
    CategoryImageUploadSerializer,
    CategoryUpdateSerializer,
)
from admin_api.services.audit_service import AuditService
from admin_api.throttling import AdminAPIThrottle, AdminSensitiveOperationThrottle
from catalog.models import Category, Product
from media_library.models import MediaAsset
from media_library.services import ImageProcessor

logger = logging.getLogger(__name__)


def generate_error_reference():
    """Generate a unique error reference for debugging."""
    return f"ERR-{secrets.token_hex(3).upper()}"


def _generate_unique_slug(name, exclude_id=None):
    """Generate a unique slug from a name, appending -2, -3, etc. if needed."""
    base_slug = slugify(name)
    slug = base_slug
    counter = 2
    while True:
        qs = Category.objects.filter(slug=slug)
        if exclude_id:
            qs = qs.exclude(id=exclude_id)
        if not qs.exists():
            return slug
        slug = f"{base_slug}-{counter}"
        counter += 1


@extend_schema(
    tags=["Admin - Categories"],
    summary=_("List categories"),
    description=_("""
    Get a paginated list of categories with filtering and sorting.

    **Rate Limit:** 300 requests per minute
    """),
    parameters=[
        OpenApiParameter(name="search", type=str, required=False, description=_("Search by name")),
        OpenApiParameter(
            name="parent_id",
            type=int,
            required=False,
            description=_("Filter by parent category ID"),
        ),
        OpenApiParameter(
            name="is_active",
            type=str,
            required=False,
            description=_("Filter by active status (all/true/false)"),
        ),
        OpenApiParameter(name="sort", type=str, required=False, description=_("Sort order")),
        OpenApiParameter(name="page", type=int, required=False, description=_("Page number")),
        OpenApiParameter(
            name="page_size", type=int, required=False, description=_("Items per page (max 100)")
        ),
    ],
    responses={200: AdminCategoryListSerializer(many=True), 400: ErrorResponseSerializer},
)
@api_view(["GET"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def category_list(request):
    """Get a paginated list of categories."""
    filter_serializer = CategoryFilterSerializer(data=request.query_params)
    if not filter_serializer.is_valid():
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Invalid filter parameters."),
                    "reference": generate_error_reference(),
                    "details": filter_serializer.errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    filters = filter_serializer.validated_data
    queryset = Category.objects.select_related("parent").annotate(
        product_count=Count("products", filter=Q(products__is_deleted=False))
    )

    # Apply filters
    search = filters.get("search", "")
    if search:
        queryset = queryset.filter(Q(name__icontains=search) | Q(slug__icontains=search))

    parent_id = filters.get("parent_id")
    if parent_id is not None:
        queryset = queryset.filter(parent_id=parent_id)

    is_active = filters.get("is_active", "all")
    if is_active == "true":
        queryset = queryset.filter(is_active=True)
    elif is_active == "false":
        queryset = queryset.filter(is_active=False)

    # Sort
    sort = filters.get("sort", "sort_order")
    if sort == "sort_order":
        queryset = queryset.order_by("sort_order", "name")
    else:
        queryset = queryset.order_by(sort)

    # Paginate
    page = filters.get("page", 1)
    page_size = filters.get("page_size", 50)
    start = (page - 1) * page_size
    end = start + page_size
    total_count = queryset.count()
    categories = queryset[start:end]

    serializer = AdminCategoryListSerializer(categories, many=True)
    return Response(
        {
            "success": True,
            "data": {
                "categories": serializer.data,
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "total_count": total_count,
                    "total_pages": (total_count + page_size - 1) // page_size,
                },
            },
        },
        status=status.HTTP_200_OK,
    )


@extend_schema(
    tags=["Admin - Categories"],
    summary=_("Get category detail"),
    description=_("Get full details for a specific category."),
    responses={200: AdminCategoryDetailSerializer, 404: ErrorResponseSerializer},
)
@api_view(["GET"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def category_detail(request, category_id):
    """Get full details for a category."""
    try:
        category = (
            Category.objects.select_related("parent")
            .annotate(product_count=Count("products", filter=Q(products__is_deleted=False)))
            .get(id=category_id)
        )
    except Category.DoesNotExist:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 404,
                    "message": _("Category not found."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = AdminCategoryDetailSerializer(category)
    return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)


@extend_schema(
    tags=["Admin - Categories"],
    summary=_("Create category"),
    description=_("""
    Create a new product category.

    **Rate Limit:** 30 requests per minute (sensitive operation)
    """),
    request=CategoryCreateSerializer,
    responses={
        201: AdminCategoryDetailSerializer,
        400: ErrorResponseSerializer,
        409: ErrorResponseSerializer,
    },
)
@api_view(["POST"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminSensitiveOperationThrottle])
def create_category(request):
    """Create a new category."""
    serializer = CategoryCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Invalid category data."),
                    "reference": generate_error_reference(),
                    "details": serializer.errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    data = serializer.validated_data
    slug = data.get("slug") or _generate_unique_slug(data["name"])

    try:
        with transaction.atomic():
            category = Category.objects.create(
                name=data["name"],
                slug=slug,
                parent_id=data.get("parent_id"),
                description=data.get("description", ""),
                icon=data.get("icon", ""),
                is_active=data.get("is_active", True),
                is_featured=data.get("is_featured", False),
                sort_order=data.get("sort_order", 0),
                products_per_page=data.get("products_per_page", 24),
                page_template=data.get("page_template", ""),
                meta_title=data.get("meta_title", ""),
                meta_description=data.get("meta_description", ""),
                external_id=data.get("external_id", ""),
            )
    except IntegrityError:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 409,
                    "message": _("A category with this slug already exists."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_409_CONFLICT,
        )

    AuditService.log_category_change(
        user=request.user,
        action_suffix="create",
        category=category,
        new_value={"name": category.name, "slug": category.slug},
        request=request,
    )

    # Re-fetch with annotations for response
    category = (
        Category.objects.select_related("parent")
        .annotate(product_count=Count("products", filter=Q(products__is_deleted=False)))
        .get(id=category.id)
    )

    return Response(
        {
            "success": True,
            "message": _("Category created successfully."),
            "data": AdminCategoryDetailSerializer(category).data,
        },
        status=status.HTTP_201_CREATED,
    )


@extend_schema(
    tags=["Admin - Categories"],
    summary=_("Update category"),
    description=_("""
    Partially update a category. Only provided fields will be changed.

    **Rate Limit:** 30 requests per minute (sensitive operation)
    """),
    request=CategoryUpdateSerializer,
    responses={
        200: AdminCategoryDetailSerializer,
        400: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
    },
)
@api_view(["PATCH"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminSensitiveOperationThrottle])
def update_category(request, category_id):
    """Partially update a category."""
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 404,
                    "message": _("Category not found."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = CategoryUpdateSerializer(data=request.data, context={"category": category})
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Invalid category data."),
                    "reference": generate_error_reference(),
                    "details": serializer.errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    data = serializer.validated_data
    old_values = {}
    new_values = {}
    update_fields = []

    for field in [
        "name",
        "description",
        "icon",
        "is_active",
        "is_featured",
        "sort_order",
        "products_per_page",
        "page_template",
        "meta_title",
        "meta_description",
    ]:
        if field in data:
            old_values[field] = getattr(category, field)
            setattr(category, field, data[field])
            new_values[field] = data[field]
            update_fields.append(field)

    if "parent_id" in data:
        old_values["parent_id"] = category.parent_id
        category.parent_id = data["parent_id"]
        new_values["parent_id"] = data["parent_id"]
        update_fields.append("parent_id")

    if "slug" in data and data["slug"]:
        old_values["slug"] = category.slug
        category.slug = data["slug"]
        new_values["slug"] = data["slug"]
        update_fields.append("slug")
    elif "name" in data:
        # Regenerate slug if name changed and no explicit slug provided
        old_values["slug"] = category.slug
        category.slug = _generate_unique_slug(data["name"], exclude_id=category.id)
        new_values["slug"] = category.slug
        update_fields.append("slug")

    if update_fields:
        try:
            category.save(update_fields=update_fields + ["updated_at"])
        except IntegrityError:
            return Response(
                {
                    "success": False,
                    "error": {
                        "code": 409,
                        "message": _("A category with this slug already exists."),
                        "reference": generate_error_reference(),
                    },
                },
                status=status.HTTP_409_CONFLICT,
            )

        AuditService.log_category_change(
            user=request.user,
            action_suffix="update",
            category=category,
            old_value=old_values,
            new_value=new_values,
            request=request,
        )

    # Re-fetch with annotations
    category = (
        Category.objects.select_related("parent")
        .annotate(product_count=Count("products", filter=Q(products__is_deleted=False)))
        .get(id=category.id)
    )

    return Response(
        {
            "success": True,
            "message": _("Category updated successfully."),
            "data": AdminCategoryDetailSerializer(category).data,
        },
        status=status.HTTP_200_OK,
    )


@extend_schema(
    tags=["Admin - Categories"],
    summary=_("Delete category"),
    description=_("""
    Delete a category. Will fail if products are assigned to this category.

    **Rate Limit:** 30 requests per minute (sensitive operation)
    """),
    responses={200: None, 404: ErrorResponseSerializer, 409: ErrorResponseSerializer},
)
@api_view(["DELETE"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminSensitiveOperationThrottle])
def delete_category(request, category_id):
    """Delete a category."""
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 404,
                    "message": _("Category not found."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    # Check for products using this category
    product_count = Product.objects.filter(category=category).count()
    if product_count > 0:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 409,
                    "message": _(
                        "Cannot delete category with %(count)d associated product(s). Reassign or delete products first."
                    )
                    % {"count": product_count},
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_409_CONFLICT,
        )

    # Check for child categories
    child_count = category.children.count()
    if child_count > 0:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 409,
                    "message": _(
                        "Cannot delete category with %(count)d child category(ies). Delete or reassign children first."
                    )
                    % {"count": child_count},
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_409_CONFLICT,
        )

    category_name = category.name
    str(category.id)

    AuditService.log_category_change(
        user=request.user,
        action_suffix="delete",
        category=category,
        old_value={"name": category_name, "slug": category.slug},
        request=request,
    )

    category.delete()

    return Response(
        {
            "success": True,
            "message": _('Category "%(name)s" deleted successfully.') % {"name": category_name},
        },
        status=status.HTTP_200_OK,
    )


@extend_schema(
    tags=["Admin - Categories"],
    summary=_("Bulk create categories"),
    description=_("""
    Create multiple categories in a single request. Maximum 100 categories per request.
    Individual failures do not rollback the entire batch.

    **Rate Limit:** 30 requests per minute (sensitive operation)
    """),
    request=BulkCategoryCreateSerializer,
    responses={201: None, 400: ErrorResponseSerializer},
)
@api_view(["POST"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminSensitiveOperationThrottle])
def bulk_create_categories(request):
    """Bulk create categories."""
    wrapper_serializer = BulkCategoryCreateSerializer(data=request.data)
    if not wrapper_serializer.is_valid():
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Invalid bulk category data."),
                    "reference": generate_error_reference(),
                    "details": wrapper_serializer.errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    items = wrapper_serializer.validated_data["categories"]
    created_count = 0
    errors = []

    for index, item_data in enumerate(items):
        try:
            with transaction.atomic():
                slug = item_data.get("slug") or _generate_unique_slug(item_data["name"])
                Category.objects.create(
                    name=item_data["name"],
                    slug=slug,
                    parent_id=item_data.get("parent_id"),
                    description=item_data.get("description", ""),
                    icon=item_data.get("icon", ""),
                    is_active=item_data.get("is_active", True),
                    is_featured=item_data.get("is_featured", False),
                    sort_order=item_data.get("sort_order", 0),
                    products_per_page=item_data.get("products_per_page", 24),
                    page_template=item_data.get("page_template", ""),
                    meta_title=item_data.get("meta_title", ""),
                    meta_description=item_data.get("meta_description", ""),
                    external_id=item_data.get("external_id", ""),
                )
                created_count += 1
        except Exception as e:
            errors.append({"index": index, "name": item_data.get("name", ""), "error": str(e)})

    AuditService.log_bulk_operation(
        user=request.user,
        action="category.bulk_create",
        resource_type="category",
        created_count=created_count,
        error_count=len(errors),
        request=request,
    )

    status_code = status.HTTP_201_CREATED if created_count > 0 else status.HTTP_400_BAD_REQUEST
    return Response(
        {
            "success": created_count > 0,
            "message": _("Created %(created)d category(ies). %(errors)d failed.")
            % {"created": created_count, "errors": len(errors)},
            "data": {"created_count": created_count, "error_count": len(errors), "errors": errors},
        },
        status=status_code,
    )


# ── Category image/banner upload endpoints ─────────────────────────


def _upload_category_asset(request, category_id, field_name):
    """
    Shared logic for uploading a category image or banner.

    field_name: 'image_asset' or 'banner_asset'
    """
    from media_library.models import MediaThumbnail

    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 404,
                    "message": _("Category not found."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = CategoryImageUploadSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Invalid image upload."),
                    "reference": generate_error_reference(),
                    "details": serializer.errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    image_file = serializer.validated_data["image"]
    alt_text = serializer.validated_data.get("alt_text", "")

    try:
        image_file.seek(0)
        img = Image.open(image_file)
        width, height = img.size

        mime_type, _encoding = mimetypes.guess_type(image_file.name)
        if not mime_type:
            format_to_mime = {
                "JPEG": "image/jpeg",
                "PNG": "image/png",
                "GIF": "image/gif",
                "WEBP": "image/webp",
            }
            mime_type = format_to_mime.get(img.format, "image/jpeg")

        image_file.seek(0)

        label = "Image" if field_name == "image_asset" else "Banner"
        media_asset = MediaAsset.objects.create(
            title=f"{category.name} - {label}",
            alt_text=alt_text,
            original_file=image_file,
            mime_type=mime_type,
            file_size=image_file.size,
            width=width,
            height=height,
            uploaded_by=request.user,
        )

        # Generate WebP version
        processor = ImageProcessor()
        if mime_type != "image/webp":
            image_file.seek(0)
            webp_content = processor.convert_to_webp(image_file)
            if webp_content:
                media_asset.webp_file.save(f"{media_asset.id}.webp", webp_content, save=True)

        # Generate thumbnails
        thumbnail_sizes = getattr(settings, "MEDIA_LIBRARY_SETTINGS", {}).get(
            "THUMBNAIL_SIZES",
            {
                "small": (150, 150),
                "medium": (300, 300),
                "large": (600, 600),
            },
        )

        for size_name, (thumb_width, thumb_height) in thumbnail_sizes.items():
            try:
                image_file.seek(0)
                original_content, webp_content = processor.generate_thumbnail(
                    image_file, thumb_width, thumb_height
                )
                if original_content:
                    thumbnail = MediaThumbnail.objects.create(
                        media_asset=media_asset,
                        size_preset=size_name,
                        width=thumb_width,
                        height=thumb_height,
                    )
                    thumbnail.file.save(
                        f"{media_asset.id}_{size_name}.jpg", original_content, save=False
                    )
                    if webp_content:
                        thumbnail.webp_file.save(
                            f"{media_asset.id}_{size_name}.webp", webp_content, save=False
                        )
                    thumbnail.save()
            except Exception as e:
                logger.error(f"Error generating thumbnail {size_name}: {e}")
                continue

        # Replace existing asset if present
        getattr(category, field_name)
        setattr(category, field_name, media_asset)
        category.save(update_fields=[field_name, "updated_at"])

        AuditService.log_category_change(
            user=request.user,
            action_suffix=f"{field_name}.upload",
            category=category,
            new_value={"media_asset_id": str(media_asset.id), "field": field_name},
            request=request,
        )

        display_url = media_asset.get_display_url()
        thumbnail_url = media_asset.get_thumbnail("medium") or display_url

        return Response(
            {
                "success": True,
                "message": _("%(label)s uploaded successfully.") % {"label": label},
                "data": {
                    "media_asset_id": str(media_asset.id),
                    "image_url": display_url,
                    "thumbnail_url": thumbnail_url,
                    "width": width,
                    "height": height,
                },
            },
            status=status.HTTP_201_CREATED,
        )

    except Exception as e:
        logger.error(f"Error uploading category {field_name}: {e}")
        return Response(
            {
                "success": False,
                "error": {
                    "code": 500,
                    "message": _("Failed to upload image."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def _delete_category_asset(request, category_id, field_name):
    """Shared logic for deleting a category image or banner."""
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 404,
                    "message": _("Category not found."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    current_asset = getattr(category, field_name)
    if not current_asset:
        label = "image" if field_name == "image_asset" else "banner"
        return Response(
            {
                "success": False,
                "error": {
                    "code": 404,
                    "message": _("Category has no %(label)s to delete.") % {"label": label},
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    old_asset_id = str(current_asset.id)
    setattr(category, field_name, None)
    category.save(update_fields=[field_name, "updated_at"])

    AuditService.log_category_change(
        user=request.user,
        action_suffix=f"{field_name}.delete",
        category=category,
        old_value={"media_asset_id": old_asset_id, "field": field_name},
        request=request,
    )

    label = "Image" if field_name == "image_asset" else "Banner"
    return Response(
        {
            "success": True,
            "message": _("%(label)s removed successfully.") % {"label": label},
        },
        status=status.HTTP_200_OK,
    )


@extend_schema(
    tags=["Admin - Categories"],
    summary=_("Upload category image"),
    description=_("""
    Upload or replace the main image for a category.

    **Rate Limit:** 300 requests per minute
    """),
    request={"multipart/form-data": CategoryImageUploadSerializer},
    responses={201: None, 400: ErrorResponseSerializer, 404: ErrorResponseSerializer},
)
@api_view(["POST"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
@parser_classes([MultiPartParser, FormParser])
def upload_category_image(request, category_id):
    """Upload or replace the main image for a category."""
    return _upload_category_asset(request, category_id, "image_asset")


@extend_schema(
    tags=["Admin - Categories"],
    summary=_("Upload category banner"),
    description=_("""
    Upload or replace the banner image for a category.

    **Rate Limit:** 300 requests per minute
    """),
    request={"multipart/form-data": CategoryImageUploadSerializer},
    responses={201: None, 400: ErrorResponseSerializer, 404: ErrorResponseSerializer},
)
@api_view(["POST"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
@parser_classes([MultiPartParser, FormParser])
def upload_category_banner(request, category_id):
    """Upload or replace the banner image for a category."""
    return _upload_category_asset(request, category_id, "banner_asset")


@extend_schema(
    tags=["Admin - Categories"],
    summary=_("Delete category image"),
    description=_("""
    Remove the main image from a category.

    **Rate Limit:** 300 requests per minute
    """),
    responses={200: None, 404: ErrorResponseSerializer},
)
@api_view(["DELETE"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def delete_category_image(request, category_id):
    """Remove the main image from a category."""
    return _delete_category_asset(request, category_id, "image_asset")


@extend_schema(
    tags=["Admin - Categories"],
    summary=_("Delete category banner"),
    description=_("""
    Remove the banner image from a category.

    **Rate Limit:** 300 requests per minute
    """),
    responses={200: None, 404: ErrorResponseSerializer},
)
@api_view(["DELETE"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def delete_category_banner(request, category_id):
    """Remove the banner image from a category."""
    return _delete_category_asset(request, category_id, "banner_asset")
