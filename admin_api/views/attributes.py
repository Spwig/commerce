"""
Admin API Attribute Views

Product attribute management endpoints for the merchant admin API.
"""

import secrets

from django.db import IntegrityError, transaction
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response

from admin_api.permissions import IsStaffWithWritePermission
from admin_api.serializers.attributes import (
    AdminAttributeListSerializer,
    AttributeCreateSerializer,
    ProductAttributeAssignSerializer,
)
from admin_api.serializers.auth import ErrorResponseSerializer
from admin_api.services.audit_service import AuditService
from admin_api.throttling import AdminAPIThrottle, AdminSensitiveOperationThrottle
from catalog.models import AttributeValue, Product, ProductAttribute, ProductAttributeAssignment


def generate_error_reference():
    """Generate a unique error reference for debugging."""
    return f"ERR-{secrets.token_hex(3).upper()}"


def _generate_unique_attr_slug(name, model_class, exclude_id=None):
    """Generate a unique slug for an attribute or value."""
    base_slug = slugify(name)
    if not base_slug:
        base_slug = "attr"
    slug = base_slug
    counter = 2
    while True:
        qs = model_class.objects.filter(slug=slug)
        if exclude_id:
            qs = qs.exclude(id=exclude_id)
        if not qs.exists():
            return slug
        slug = f"{base_slug}-{counter}"
        counter += 1


@extend_schema(
    tags=["Admin - Attributes"],
    summary=_("List product attributes"),
    description=_("""
    Get all product attributes with their values.

    **Rate Limit:** 300 requests per minute
    """),
    responses={200: AdminAttributeListSerializer(many=True)},
)
@api_view(["GET"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminAPIThrottle])
def attribute_list(request):
    """List all product attributes with their values."""
    attributes = ProductAttribute.objects.prefetch_related("values").order_by("sort_order", "name")
    serializer = AdminAttributeListSerializer(attributes, many=True)
    return Response(
        {"success": True, "data": {"attributes": serializer.data}}, status=status.HTTP_200_OK
    )


@extend_schema(
    tags=["Admin - Attributes"],
    summary=_("Create product attribute"),
    description=_("""
    Create a new product attribute with optional values.

    Example request:
    ```json
    {
        "name": "Color",
        "type": "color",
        "values": [
            {"value": "Red", "color_hex": "#FF0000", "sort_order": 0},
            {"value": "Blue", "color_hex": "#0000FF", "sort_order": 1}
        ]
    }
    ```

    **Rate Limit:** 30 requests per minute (sensitive operation)
    """),
    request=AttributeCreateSerializer,
    responses={
        201: AdminAttributeListSerializer,
        400: ErrorResponseSerializer,
        409: ErrorResponseSerializer,
    },
)
@api_view(["POST"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminSensitiveOperationThrottle])
def create_attribute(request):
    """Create a new product attribute with optional values."""
    serializer = AttributeCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Invalid attribute data."),
                    "reference": generate_error_reference(),
                    "details": serializer.errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    data = serializer.validated_data

    try:
        with transaction.atomic():
            attribute = ProductAttribute.objects.create(
                name=data["name"],
                slug=_generate_unique_attr_slug(data["name"], ProductAttribute),
                type=data.get("type", "select"),
                is_required=data.get("is_required", True),
                sort_order=data.get("sort_order", 0),
            )

            # Create values
            for val_data in data.get("values", []):
                AttributeValue.objects.create(
                    attribute=attribute,
                    value=val_data["value"],
                    slug=_generate_unique_attr_slug(val_data["value"], AttributeValue),
                    color_hex=val_data.get("color_hex", ""),
                    sort_order=val_data.get("sort_order", 0),
                )
    except IntegrityError:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 409,
                    "message": _("An attribute with this name already exists."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_409_CONFLICT,
        )

    AuditService.log(
        user=request.user,
        action="attribute.create",
        resource_type="attribute",
        resource_id=str(attribute.id),
        new_value={
            "name": attribute.name,
            "type": attribute.type,
            "values_count": attribute.values.count(),
        },
        request=request,
    )

    # Re-fetch with values
    attribute = ProductAttribute.objects.prefetch_related("values").get(id=attribute.id)

    return Response(
        {
            "success": True,
            "message": _("Attribute created successfully."),
            "data": AdminAttributeListSerializer(attribute).data,
        },
        status=status.HTTP_201_CREATED,
    )


@extend_schema(
    tags=["Admin - Attributes"],
    summary=_("Assign attributes to product"),
    description=_("""
    Assign attributes and their allowed values to a product. This creates
    ProductAttributeAssignment records that define which attributes and values
    are available for a product's variants.

    Example request:
    ```json
    {
        "assignments": [
            {"attribute_id": 1, "value_ids": [1, 2, 3], "sort_order": 0},
            {"attribute_id": 2, "value_ids": [5, 6], "sort_order": 1}
        ]
    }
    ```

    **Rate Limit:** 30 requests per minute (sensitive operation)
    """),
    request=ProductAttributeAssignSerializer,
    responses={200: None, 400: ErrorResponseSerializer, 404: ErrorResponseSerializer},
)
@api_view(["POST"])
@permission_classes([IsStaffWithWritePermission])
@throttle_classes([AdminSensitiveOperationThrottle])
def assign_product_attributes(request, product_id):
    """Assign attributes and allowed values to a product."""
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 404,
                    "message": _("Product not found."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = ProductAttributeAssignSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Invalid assignment data."),
                    "reference": generate_error_reference(),
                    "details": serializer.errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    assignments_data = serializer.validated_data["assignments"]
    created = 0
    updated = 0
    errors = []

    for item in assignments_data:
        attribute_id = item["attribute_id"]
        value_ids = item.get("value_ids", [])
        sort_order = item.get("sort_order", 0)

        try:
            attribute = ProductAttribute.objects.get(id=attribute_id)
        except ProductAttribute.DoesNotExist:
            errors.append({"attribute_id": attribute_id, "error": "Attribute not found."})
            continue

        # Validate that value_ids belong to this attribute
        valid_value_ids = set(
            AttributeValue.objects.filter(id__in=value_ids, attribute=attribute).values_list(
                "id", flat=True
            )
        )
        invalid_ids = set(value_ids) - valid_value_ids
        if invalid_ids:
            errors.append(
                {
                    "attribute_id": attribute_id,
                    "error": f'Value IDs {list(invalid_ids)} do not belong to attribute "{attribute.name}".',
                }
            )
            continue

        assignment, was_created = ProductAttributeAssignment.objects.get_or_create(
            product=product, attribute=attribute, defaults={"sort_order": sort_order}
        )
        if not was_created:
            assignment.sort_order = sort_order
            assignment.save(update_fields=["sort_order"])
            updated += 1
        else:
            created += 1

        assignment.allowed_values.set(valid_value_ids)

    AuditService.log(
        user=request.user,
        action="product.assign_attributes",
        resource_type="product",
        resource_id=str(product.id),
        new_value={
            "created": created,
            "updated": updated,
            "errors": len(errors),
        },
        request=request,
    )

    return Response(
        {
            "success": True,
            "message": _(
                "Attributes assigned successfully. %(created)d created, %(updated)d updated."
            )
            % {"created": created, "updated": updated},
            "data": {"created": created, "updated": updated, "errors": errors},
        },
        status=status.HTTP_200_OK,
    )
