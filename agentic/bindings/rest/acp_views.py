"""
ACP product-feed binding — `/api/agentic/acp/product_feed` (underscore path).

A thin projection of the agent-visible catalogue in ACP feed shape, gated on
`require_protocol("acp")`, so it 404s unless the merchant has enabled ACP (off
by default). Like the UCP read surface it stands on its own (no auth by
default) and reuses the shared catalogue service — no parallel catalog.
"""

from __future__ import annotations

from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from agentic.bindings.rest.serializers import UCPErrorSerializer
from agentic.gating import require_agentic, require_protocol
from agentic.identity.authentication import AgentAuthError, require_read_access
from agentic.services import acp_service

_TAG = "Agentic Commerce"


@extend_schema(
    tags=[_TAG],
    operation_id="agentic_acp_product_feed",
    summary="ACP product feed",
    description=(
        "A page of the store's agent-visible catalogue in ACP feed shape "
        "(nested variants, availability {available,status}, barcodes "
        "[{type,value}]). 404 when agentic commerce or the ACP surface is "
        "disabled (ACP is off by default)."
    ),
    parameters=[
        OpenApiParameter("page", int, description="1-based page number (default 1)."),
        OpenApiParameter("page_size", int, description="Items per page (default 100, max 250)."),
    ],
    responses={
        200: OpenApiResponse(description="A page of the ACP product feed."),
        401: OpenApiResponse(response=UCPErrorSerializer, description="Signature required."),
        404: OpenApiResponse(response=UCPErrorSerializer, description="ACP is not enabled."),
    },
)
@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def acp_product_feed(request):
    require_agentic()
    require_protocol("acp")
    try:
        require_read_access(request)
    except AgentAuthError as exc:
        return Response({"error": "unauthorized", "message": str(exc.reason)}, status=401)

    try:
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 100))
    except (TypeError, ValueError):
        page, page_size = 1, 100

    return Response(acp_service.product_feed(page=page, page_size=page_size, request=request))
