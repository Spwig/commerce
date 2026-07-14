"""
API views for custom field definitions.

Provides read-only access to field definitions so external integrations
can discover what custom fields exist for a model.
"""

from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import generics, permissions

from .models import CustomFieldDefinition
from .serializers import CustomFieldDefinitionSerializer


@extend_schema(
    tags=["Custom Fields"],
    summary=_("List custom field definitions"),
    description=_(
        "List all active custom field definitions, optionally filtered by model. "
        "Use this to discover what custom fields are configured for a given model type "
        "(e.g., product, order, category). Requires authentication."
    ),
    parameters=[
        OpenApiParameter("model", str, description=_('Filter by model name (e.g., "product")')),
        OpenApiParameter("app", str, description=_('Filter by app label (e.g., "catalog")')),
    ],
    responses={200: CustomFieldDefinitionSerializer(many=True)},
)
class FieldDefinitionListView(generics.ListAPIView):
    """
    List custom field definitions, optionally filtered by model.

    Query parameters:
    - model: Filter by model name (e.g., "product", "order", "category", "customerprofile")
    - app: Filter by app label (e.g., "catalog", "orders")

    Example: GET /api/custom-fields/definitions/?model=product&app=catalog
    """

    serializer_class = CustomFieldDefinitionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = (
            CustomFieldDefinition.objects.filter(is_active=True)
            .select_related("group")
            .order_by("group__sort_order", "sort_order")
        )

        model_name = self.request.query_params.get("model")
        app_label = self.request.query_params.get("app")

        if model_name and app_label:
            try:
                ct = ContentType.objects.get(app_label=app_label, model=model_name)
                qs = qs.filter(content_type=ct)
            except ContentType.DoesNotExist:
                qs = qs.none()
        elif model_name:
            qs = qs.filter(content_type__model=model_name)

        return qs


@extend_schema(
    tags=["Custom Fields"],
    summary=_("Get custom field definition"),
    description=_(
        "Get detailed information about a specific custom field definition "
        "including its type, validation config, choices, and group. Requires authentication."
    ),
    responses={
        200: CustomFieldDefinitionSerializer,
        404: OpenApiResponse(description=_("Field definition not found or inactive")),
    },
)
class FieldDefinitionDetailView(generics.RetrieveAPIView):
    """Get details of a single custom field definition."""

    serializer_class = CustomFieldDefinitionSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomFieldDefinition.objects.filter(is_active=True).select_related("group")
