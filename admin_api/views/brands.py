"""
Admin API Brand Views

Brand management endpoints for the merchant admin API.
"""

import secrets

from django.db import IntegrityError, transaction
from django.db.models import Count, Q
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response

from admin_api.permissions import IsStaffWithWritePermission
from admin_api.serializers.auth import ErrorResponseSerializer
from admin_api.serializers.brands import (
    AdminBrandDetailSerializer,
    AdminBrandListSerializer,
    BrandCreateSerializer,
    BrandFilterSerializer,
    BrandUpdateSerializer,
    BulkBrandCreateSerializer,
)
from admin_api.services.audit_service import AuditService
from admin_api.throttling import AdminAPIThrottle, AdminSensitiveOperationThrottle
from catalog.models import Brand, Product


def generate_error_reference():
    """Generate a unique error reference for debugging."""
    return f"ERR-{secrets.token_hex(3).upper()}"


def _generate_unique_slug(name, exclude_id=None):
    """Generate a unique slug from a name, appending -2, -3, etc. if needed."""
    base_slug = slugify(name)
    slug = base_slug
    counter = 2
    while True:
        qs = Brand.objects.filter(slug=slug)
        if exclude_id:
            qs = qs.exclude(id=exclude_id)
        if not qs.exists():
            return slug
        slug = f"{base_slug}-{counter}"
        counter += 1


@extend_schema(
    tags=["Admin - Brands"],
    summary=_("List brands"),
    description=_("""
    Get a paginated list of brands with filtering and sorting.

    **Rate Limit:** 300 requests per minute
    """),
    parameters=[
        OpenApiParameter(name="search", type=str, required=False, description=_("Search by name")),
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
    responses={200: AdminBrandListSerializer(many=True), 400: ErrorResponseSerializer},
)
@api_view(["GET"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def brand_list(request):
    """Get a paginated list of brands."""
    filter_serializer = BrandFilterSerializer(data=request.query_params)
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
    queryset = Brand.objects.annotate(
        product_count=Count("products", filter=Q(products__is_deleted=False))
    )

    # Apply filters
    search = filters.get("search", "")
    if search:
        queryset = queryset.filter(Q(name__icontains=search) | Q(slug__icontains=search))

    is_active = filters.get("is_active", "all")
    if is_active == "true":
        queryset = queryset.filter(is_active=True)
    elif is_active == "false":
        queryset = queryset.filter(is_active=False)

    # Sort
    sort = filters.get("sort", "name")
    queryset = queryset.order_by(sort)

    # Paginate
    page = filters.get("page", 1)
    page_size = filters.get("page_size", 50)
    start = (page - 1) * page_size
    end = start + page_size
    total_count = queryset.count()
    brands = queryset[start:end]

    serializer = AdminBrandListSerializer(brands, many=True)
    return Response(
        {
            "success": True,
            "data": {
                "brands": serializer.data,
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
    tags=["Admin - Brands"],
    summary=_("Get brand detail"),
    description=_("Get full details for a specific brand."),
    responses={200: AdminBrandDetailSerializer, 404: ErrorResponseSerializer},
)
@api_view(["GET"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def brand_detail(request, brand_id):
    """Get full details for a brand."""
    try:
        brand = Brand.objects.annotate(
            product_count=Count("products", filter=Q(products__is_deleted=False))
        ).get(id=brand_id)
    except Brand.DoesNotExist:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 404,
                    "message": _("Brand not found."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = AdminBrandDetailSerializer(brand)
    return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)


@extend_schema(
    tags=["Admin - Brands"],
    summary=_("Create brand"),
    description=_("""
    Create a new brand.

    **Rate Limit:** 30 requests per minute (sensitive operation)
    """),
    request=BrandCreateSerializer,
    responses={
        201: AdminBrandDetailSerializer,
        400: ErrorResponseSerializer,
        409: ErrorResponseSerializer,
    },
)
@api_view(["POST"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminSensitiveOperationThrottle])
def create_brand(request):
    """Create a new brand."""
    serializer = BrandCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Invalid brand data."),
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
            brand = Brand.objects.create(
                name=data["name"],
                slug=slug,
                description=data.get("description", ""),
                website=data.get("website", ""),
                show_brand_page=data.get("show_brand_page", True),
                brand_story=data.get("brand_story", ""),
                is_active=data.get("is_active", True),
                is_featured=data.get("is_featured", False),
                meta_title=data.get("meta_title", ""),
                meta_description=data.get("meta_description", ""),
            )
    except IntegrityError:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 409,
                    "message": _("A brand with this name or slug already exists."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_409_CONFLICT,
        )

    AuditService.log_brand_change(
        user=request.user,
        action_suffix="create",
        brand=brand,
        new_value={"name": brand.name, "slug": brand.slug},
        request=request,
    )

    # Re-fetch with annotations
    brand = Brand.objects.annotate(
        product_count=Count("products", filter=Q(products__is_deleted=False))
    ).get(id=brand.id)

    return Response(
        {
            "success": True,
            "message": _("Brand created successfully."),
            "data": AdminBrandDetailSerializer(brand).data,
        },
        status=status.HTTP_201_CREATED,
    )


@extend_schema(
    tags=["Admin - Brands"],
    summary=_("Update brand"),
    description=_("""
    Partially update a brand. Only provided fields will be changed.

    **Rate Limit:** 30 requests per minute (sensitive operation)
    """),
    request=BrandUpdateSerializer,
    responses={
        200: AdminBrandDetailSerializer,
        400: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
    },
)
@api_view(["PATCH"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminSensitiveOperationThrottle])
def update_brand(request, brand_id):
    """Partially update a brand."""
    try:
        brand = Brand.objects.get(id=brand_id)
    except Brand.DoesNotExist:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 404,
                    "message": _("Brand not found."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = BrandUpdateSerializer(data=request.data, context={"brand": brand})
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Invalid brand data."),
                    "reference": generate_error_reference(),
                    "details": serializer.errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    data = serializer.validated_data
    old_values = {}
    new_values = {}

    for field in [
        "name",
        "description",
        "website",
        "show_brand_page",
        "brand_story",
        "is_active",
        "is_featured",
        "meta_title",
        "meta_description",
    ]:
        if field in data:
            old_values[field] = getattr(brand, field)
            setattr(brand, field, data[field])
            new_values[field] = data[field]

    if "slug" in data and data["slug"]:
        old_values["slug"] = brand.slug
        brand.slug = data["slug"]
        new_values["slug"] = data["slug"]
    elif "name" in data:
        old_values["slug"] = brand.slug
        brand.slug = _generate_unique_slug(data["name"], exclude_id=brand.id)
        new_values["slug"] = brand.slug

    if new_values:
        try:
            brand.save()
        except IntegrityError:
            return Response(
                {
                    "success": False,
                    "error": {
                        "code": 409,
                        "message": _("A brand with this name or slug already exists."),
                        "reference": generate_error_reference(),
                    },
                },
                status=status.HTTP_409_CONFLICT,
            )

        AuditService.log_brand_change(
            user=request.user,
            action_suffix="update",
            brand=brand,
            old_value=old_values,
            new_value=new_values,
            request=request,
        )

    # Re-fetch with annotations
    brand = Brand.objects.annotate(
        product_count=Count("products", filter=Q(products__is_deleted=False))
    ).get(id=brand.id)

    return Response(
        {
            "success": True,
            "message": _("Brand updated successfully."),
            "data": AdminBrandDetailSerializer(brand).data,
        },
        status=status.HTTP_200_OK,
    )


@extend_schema(
    tags=["Admin - Brands"],
    summary=_("Delete brand"),
    description=_("""
    Delete a brand. Will fail if products are assigned to this brand.

    **Rate Limit:** 30 requests per minute (sensitive operation)
    """),
    responses={200: None, 404: ErrorResponseSerializer, 409: ErrorResponseSerializer},
)
@api_view(["DELETE"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminSensitiveOperationThrottle])
def delete_brand(request, brand_id):
    """Delete a brand."""
    try:
        brand = Brand.objects.get(id=brand_id)
    except Brand.DoesNotExist:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 404,
                    "message": _("Brand not found."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    # Check for products using this brand
    product_count = Product.objects.filter(brand=brand).count()
    if product_count > 0:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 409,
                    "message": _(
                        "Cannot delete brand with %(count)d associated product(s). Reassign or delete products first."
                    )
                    % {"count": product_count},
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_409_CONFLICT,
        )

    brand_name = brand.name

    AuditService.log_brand_change(
        user=request.user,
        action_suffix="delete",
        brand=brand,
        old_value={"name": brand_name, "slug": brand.slug},
        request=request,
    )

    brand.delete()

    return Response(
        {
            "success": True,
            "message": _('Brand "%(name)s" deleted successfully.') % {"name": brand_name},
        },
        status=status.HTTP_200_OK,
    )


@extend_schema(
    tags=["Admin - Brands"],
    summary=_("Bulk create brands"),
    description=_("""
    Create multiple brands in a single request. Maximum 100 brands per request.
    Individual failures do not rollback the entire batch.

    **Rate Limit:** 30 requests per minute (sensitive operation)
    """),
    request=BulkBrandCreateSerializer,
    responses={201: None, 400: ErrorResponseSerializer},
)
@api_view(["POST"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminSensitiveOperationThrottle])
def bulk_create_brands(request):
    """Bulk create brands."""
    wrapper_serializer = BulkBrandCreateSerializer(data=request.data)
    if not wrapper_serializer.is_valid():
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Invalid bulk brand data."),
                    "reference": generate_error_reference(),
                    "details": wrapper_serializer.errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    items = wrapper_serializer.validated_data["brands"]
    created_count = 0
    errors = []

    for index, item_data in enumerate(items):
        try:
            with transaction.atomic():
                slug = item_data.get("slug") or _generate_unique_slug(item_data["name"])
                Brand.objects.create(
                    name=item_data["name"],
                    slug=slug,
                    description=item_data.get("description", ""),
                    website=item_data.get("website", ""),
                    show_brand_page=item_data.get("show_brand_page", True),
                    brand_story=item_data.get("brand_story", ""),
                    is_active=item_data.get("is_active", True),
                    is_featured=item_data.get("is_featured", False),
                    meta_title=item_data.get("meta_title", ""),
                    meta_description=item_data.get("meta_description", ""),
                )
                created_count += 1
        except Exception as e:
            errors.append({"index": index, "name": item_data.get("name", ""), "error": str(e)})

    AuditService.log_bulk_operation(
        user=request.user,
        action="brand.bulk_create",
        resource_type="brand",
        created_count=created_count,
        error_count=len(errors),
        request=request,
    )

    status_code = status.HTTP_201_CREATED if created_count > 0 else status.HTTP_400_BAD_REQUEST
    return Response(
        {
            "success": created_count > 0,
            "message": _("Created %(created)d brand(s). %(errors)d failed.")
            % {"created": created_count, "errors": len(errors)},
            "data": {"created_count": created_count, "error_count": len(errors), "errors": errors},
        },
        status=status_code,
    )
