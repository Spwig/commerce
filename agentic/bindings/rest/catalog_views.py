"""
UCP catalog read binding — search and lookup over `/api/agentic/ucp/`.

Unauthenticated public read, matching how UCP/Shopify expose a storefront
catalog to agents (signature verification is a later, separate concern). Every
view gates on `require_agentic()` + `require_protocol("ucp")` first, so the
whole surface is 404 when the merchant hasn't enabled agentic commerce.

Deliberately does NOT reuse the storefront `ProductViewSet` or
`HeadlessAPIMixin`: those carry `MobileTokenAuthentication` (which hard-fails
unknown Bearer tokens) and, since 1.7.0, `SessionAuthentication`. The agentic
binding stands on its own auth stack — here, none — calling the catalog
service directly.
"""

from __future__ import annotations

from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from agentic.bindings.rest.serializers import (
    UCPErrorSerializer,
    UCPProductSerializer,
    UCPSearchResponseSerializer,
)
from agentic.gating import require_agentic, require_protocol
from agentic.identity.authentication import (
    AgentAuthError,
    AgentRateLimited,
    require_read_access,
)
from agentic.services import catalog_service

_TAG = "Agentic Commerce"


def _require_ucp():
    require_agentic()
    require_protocol("ucp")


def _gate_read(request) -> Response | None:
    """Enforce the read posture; return an error Response, or None to proceed."""
    try:
        require_read_access(request)
        return None
    except AgentRateLimited as exc:
        return Response(
            {"error": "rate_limited", "message": str(exc.reason)},
            status=status.HTTP_429_TOO_MANY_REQUESTS,
        )
    except AgentAuthError as exc:
        return Response(
            {"error": "unauthorized", "message": str(exc.reason)},
            status=status.HTTP_401_UNAUTHORIZED,
        )


@extend_schema(
    tags=[_TAG],
    operation_id="agentic_ucp_catalog_search",
    summary="UCP catalog search",
    description=(
        "Search the store's agent-visible catalog and return products in UCP "
        "catalog shape (id, title, description, price_range, variants). Prices "
        "are integer minor units + ISO 4217. Public and unauthenticated; 404 "
        "when agentic commerce is disabled."
    ),
    parameters=[
        OpenApiParameter("q", str, description="Free-text query over title/description."),
        OpenApiParameter("page", int, description="1-based page number (default 1)."),
        OpenApiParameter("page_size", int, description="Items per page (default 20, max 100)."),
    ],
    responses={
        200: OpenApiResponse(
            response=UCPSearchResponseSerializer, description="Paginated UCP products."
        ),
        401: OpenApiResponse(
            response=UCPErrorSerializer,
            description=(
                "The merchant requires a verified agent signature (RFC 9421) and "
                "the request was unsigned, failed verification, or the agent is "
                "blocked."
            ),
        ),
        429: OpenApiResponse(
            response=UCPErrorSerializer,
            description="Too many signature-auth attempts; retry later.",
        ),
        404: OpenApiResponse(
            response=UCPErrorSerializer,
            description="Agentic commerce (or UCP) is not enabled.",
        ),
    },
)
@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def ucp_product_search(request):
    _require_ucp()
    if (denied := _gate_read(request)) is not None:
        return denied

    query = request.query_params.get("q", "").strip()
    try:
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 20))
    except (TypeError, ValueError):
        page, page_size = 1, 20

    products, total = catalog_service.search(query, page=page, page_size=page_size)
    return Response(
        {
            "products": [catalog_service.to_ucp_product(p, request) for p in products],
            "page": max(1, page),
            "page_size": max(1, min(page_size, 100)),
            "total": total,
        }
    )


@extend_schema(
    tags=[_TAG],
    operation_id="agentic_ucp_catalog_lookup",
    summary="UCP catalog lookup",
    description=(
        "Fetch one agent-visible product by id in UCP catalog shape. Public and "
        "unauthenticated; 404 when agentic commerce is disabled or the product "
        "is not sellable."
    ),
    responses={
        200: OpenApiResponse(response=UCPProductSerializer, description="A UCP product."),
        401: OpenApiResponse(
            response=UCPErrorSerializer,
            description=(
                "The merchant requires a verified agent signature (RFC 9421) and "
                "the request was unsigned, failed verification, or the agent is "
                "blocked."
            ),
        ),
        429: OpenApiResponse(
            response=UCPErrorSerializer,
            description="Too many signature-auth attempts; retry later.",
        ),
        404: OpenApiResponse(
            response=UCPErrorSerializer,
            description="Not enabled, or no such sellable product.",
        ),
    },
)
@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def ucp_product_detail(request, product_id: int):
    _require_ucp()
    if (denied := _gate_read(request)) is not None:
        return denied

    product = catalog_service.get_product(product_id)
    if product is None:
        return Response(
            {"error": "not_found", "message": "No such product."},
            status=status.HTTP_404_NOT_FOUND,
        )
    return Response(catalog_service.to_ucp_product(product, request))
