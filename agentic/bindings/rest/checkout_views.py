"""
UCP checkout-session REST binding — `/api/agentic/ucp/checkout-sessions`.

A thin HTTP shell over `agentic.services.checkout_service`: it parses the UCP
request, calls the service (which reuses the store's checkout/payment
machinery), and serialises the result. It invents no checkout or pricing logic.

Unlike the read surfaces, checkout REQUIRES a verified agent signature (RFC
9421) unless the merchant has opted into unverified checkout — money is moving.
Create and complete honour an `Idempotency-Key` header so a retried request
never places or charges twice.
"""

from __future__ import annotations

import hashlib

from django.core.cache import cache
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
    throttle_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from agentic.bindings.rest.serializers import (
    UCPCheckoutCompleteRequestSerializer,
    UCPCheckoutCreateRequestSerializer,
    UCPCheckoutSessionSerializer,
    UCPCheckoutUpdateRequestSerializer,
    UCPErrorSerializer,
)
from agentic.gating import require_agentic, require_protocol
from agentic.identity.authentication import (
    AgentAuthError,
    AgentRateLimited,
    require_verified_agent,
)
from agentic.services import checkout_service as acs
from core.api.throttling import AgenticCheckoutThrottle, AgenticPaymentThrottle

_TAG = "Agentic Commerce"
IDEMPOTENCY_TTL = 24 * 60 * 60  # seconds


def _require_ucp():
    require_agentic()
    require_protocol("ucp")


def _error(exc: acs.CheckoutError) -> Response:
    body = {"error": exc.code, "message": exc.message}
    if exc.messages:
        body["messages"] = exc.messages
    return Response(body, status=exc.http_status)


def _gate(request):
    """Verified-agent gate; returns (agent_context, error_response|None)."""
    try:
        return require_verified_agent(request), None
    except AgentRateLimited as exc:
        return None, Response(
            {"error": "rate_limited", "message": str(exc.reason)},
            status=status.HTTP_429_TOO_MANY_REQUESTS,
        )
    except AgentAuthError as exc:
        return None, Response(
            {"error": "unauthorized", "message": str(exc.reason)},
            status=status.HTTP_401_UNAUTHORIZED,
        )


def _idem_key(request, agent, scope: str) -> str | None:
    raw = request.headers.get("Idempotency-Key")
    if not raw or agent is None:
        # Server-side idempotency only for a VERIFIED agent. Anonymous callers
        # (allow_unverified_checkout) share no identity, so a common namespace
        # would let one caller's key fetch another's cached response (leaking the
        # checkout id + buyer PII). Better to not cache than to cross-replay.
        return None
    body_hash = hashlib.sha256(request.body or b"").hexdigest()[:16]
    material = f"{scope}:{agent.identity.id}:{raw}:{body_hash}"
    return f"agentic:idem:{hashlib.sha256(material.encode()).hexdigest()}"


def _continue_url(request) -> str:
    """Best-effort storefront URL a human can use to finish this checkout."""
    return request.build_absolute_uri("/checkout/")


def _agent_identity(ctx):
    return ctx.identity if ctx else None


@extend_schema(
    tags=[_TAG],
    operation_id="agentic_ucp_checkout_create",
    summary="Create UCP checkout session",
    description=(
        "Create an agentic checkout session from line items (and optional "
        "buyer). Returns the session in UCP shape with computed totals and "
        "status. Requires a verified agent signature unless the merchant allows "
        "unverified checkout. Honours Idempotency-Key."
    ),
    request=UCPCheckoutCreateRequestSerializer,
    responses={
        201: OpenApiResponse(
            response=UCPCheckoutSessionSerializer, description="The created UCP checkout session."
        ),
        400: OpenApiResponse(response=UCPErrorSerializer, description="Invalid request."),
        401: OpenApiResponse(response=UCPErrorSerializer, description="Signature required."),
        404: OpenApiResponse(
            response=UCPErrorSerializer, description="Not enabled / unknown product."
        ),
        429: OpenApiResponse(response=UCPErrorSerializer, description="Rate limited."),
    },
)
@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([AgenticCheckoutThrottle])
def checkout_create(request):
    _require_ucp()
    ctx, denied = _gate(request)
    if denied is not None:
        return denied

    cache_key = _idem_key(request, ctx, "create")
    if cache_key and (cached := cache.get(cache_key)) is not None:
        return Response(cached, status=status.HTTP_201_CREATED)

    data = request.data if isinstance(request.data, dict) else {}
    line_items = data.get("line_items") or []
    buyer = data.get("buyer")
    agent = _agent_identity(ctx)
    try:
        checkout_id = acs.create_checkout_session(agent=agent, line_items=line_items, buyer=buyer)
    except acs.CheckoutError as exc:
        return _error(exc)

    body = acs.get_checkout_view(checkout_id, agent, continue_url=_continue_url(request))
    if cache_key:
        cache.set(cache_key, body, IDEMPOTENCY_TTL)
    return Response(body, status=status.HTTP_201_CREATED)


@extend_schema(
    tags=[_TAG],
    operation_id="agentic_ucp_checkout_get",
    summary="Get UCP checkout session",
    responses={
        200: OpenApiResponse(
            response=UCPCheckoutSessionSerializer, description="The UCP checkout session."
        ),
        401: OpenApiResponse(response=UCPErrorSerializer, description="Signature required."),
        404: OpenApiResponse(response=UCPErrorSerializer, description="No such session."),
    },
)
@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([AgenticCheckoutThrottle])
def checkout_detail(request, checkout_id: str):
    _require_ucp()
    ctx, denied = _gate(request)
    if denied is not None:
        return denied
    body = acs.get_checkout_view(
        checkout_id, _agent_identity(ctx), continue_url=_continue_url(request)
    )
    if body is None:
        return Response(
            {"error": "not_found", "message": "No such checkout session."},
            status=status.HTTP_404_NOT_FOUND,
        )
    return Response(body)


@extend_schema(
    tags=[_TAG],
    operation_id="agentic_ucp_checkout_mandate",
    summary="Get the AP2 checkout mandate",
    description=(
        "Return the merchant-signed AP2 Checkout Mandate (SD-JWT) for a "
        "completed checkout — the signed attestation of what was charged, "
        "verifiable against the store's JWKS at /.well-known/ucp. 404 if the "
        "checkout isn't the agent's, isn't completed, or the store issues no "
        "mandate (no AP2 key)."
    ),
    responses={
        200: OpenApiResponse(description="The AP2 checkout mandate."),
        401: OpenApiResponse(response=UCPErrorSerializer, description="Signature required."),
        404: OpenApiResponse(response=UCPErrorSerializer, description="No mandate."),
    },
)
@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([AgenticCheckoutThrottle])
def checkout_mandate(request, checkout_id: str):
    _require_ucp()
    ctx, denied = _gate(request)
    if denied is not None:
        return denied
    mandate = acs.get_mandate(checkout_id, _agent_identity(ctx))
    if mandate is None:
        return Response(
            {"error": "not_found", "message": "No mandate for this checkout."},
            status=status.HTTP_404_NOT_FOUND,
        )
    return Response(mandate)


@extend_schema(
    tags=[_TAG],
    operation_id="agentic_ucp_checkout_update",
    summary="Update UCP checkout session",
    description="Apply buyer and/or fulfillment selection to a checkout session, then re-price.",
    request=UCPCheckoutUpdateRequestSerializer,
    responses={
        200: OpenApiResponse(
            response=UCPCheckoutSessionSerializer, description="The updated UCP checkout session."
        ),
        400: OpenApiResponse(response=UCPErrorSerializer, description="Invalid update."),
        401: OpenApiResponse(response=UCPErrorSerializer, description="Signature required."),
        404: OpenApiResponse(response=UCPErrorSerializer, description="No such session."),
    },
)
@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([AgenticCheckoutThrottle])
def checkout_update(request, checkout_id: str):
    _require_ucp()
    ctx, denied = _gate(request)
    if denied is not None:
        return denied

    data = request.data if isinstance(request.data, dict) else {}
    agent = _agent_identity(ctx)
    try:
        acs.update_checkout_session(
            checkout_id,
            agent,
            buyer=data.get("buyer"),
            fulfillment_option_id=data.get("fulfillment_option_id"),
        )
    except acs.CheckoutError as exc:
        return _error(exc)
    body = acs.get_checkout_view(checkout_id, agent, continue_url=_continue_url(request))
    return Response(body)


@extend_schema(
    tags=[_TAG],
    operation_id="agentic_ucp_checkout_complete",
    summary="Complete (pay) UCP checkout session",
    description=(
        "Charge the agent's payment credential and place the order. Agent orders "
        "are gateway-only. `attested_total` (UCP money) is a checkout-time price "
        "lock: a mismatch against the freshly-priced total returns 409 "
        "price_changed. Honours Idempotency-Key; a replay after success returns "
        "the same completed session. A 3DS/redirect flow returns "
        "payment.status=requires_action with a continue_url for a human to finish."
    ),
    request=UCPCheckoutCompleteRequestSerializer,
    responses={
        200: OpenApiResponse(
            response=UCPCheckoutSessionSerializer,
            description="Completed (or requires_action) UCP checkout session.",
        ),
        401: OpenApiResponse(response=UCPErrorSerializer, description="Signature required."),
        402: OpenApiResponse(response=UCPErrorSerializer, description="Payment declined."),
        409: OpenApiResponse(response=UCPErrorSerializer, description="Not ready / price changed."),
        429: OpenApiResponse(response=UCPErrorSerializer, description="Rate limited."),
    },
)
@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([AgenticPaymentThrottle])
def checkout_complete(request, checkout_id: str):
    _require_ucp()
    ctx, denied = _gate(request)
    if denied is not None:
        return denied

    cache_key = _idem_key(request, ctx, f"complete:{checkout_id}")
    if cache_key and (cached := cache.get(cache_key)) is not None:
        return Response(cached)

    data = request.data if isinstance(request.data, dict) else {}
    agent = _agent_identity(ctx)
    try:
        body = acs.complete_checkout_session(
            checkout_id,
            agent,
            payment=data.get("payment") or {},
            attested_total=data.get("attested_total"),
            return_url=data.get("return_url", ""),
            cancel_url=data.get("cancel_url", ""),
            continue_url=_continue_url(request),
        )
    except acs.CheckoutError as exc:
        return _error(exc)

    if cache_key and body.get("status") == acs.STATUS_COMPLETED:
        cache.set(cache_key, body, IDEMPOTENCY_TTL)
    return Response(body)
