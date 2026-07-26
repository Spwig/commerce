"""
Storefront MCP endpoint at /api/agentic/mcp — JSON-RPC 2.0 over HTTP.

MCP 2025-11-25 (the current stable spec; NOT the 2026-07-28 release
candidate). Single JSON-RPC requests only — batching was removed from MCP in
2025-06-18. A plain Django view rather than DRF: MCP is JSON-RPC, not REST, so
it deliberately stays out of the OpenAPI contract.

Unauthenticated, matching how Shopify exposes its storefront MCP server. Gated
on require_agentic() + require_protocol("mcp"), so it 404s when off.
"""

from __future__ import annotations

import json
import logging

from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from agentic.bindings.mcp import storefront_tools
from agentic.gating import require_agentic, require_protocol
from agentic.identity.authentication import (
    AgentAuthError,
    AgentRateLimited,
    require_read_access,
)

logger = logging.getLogger(__name__)

PROTOCOL_VERSION = "2025-11-25"

# JSON-RPC 2.0 error codes.
PARSE_ERROR = -32700
INVALID_REQUEST = -32600
METHOD_NOT_FOUND = -32601
INVALID_PARAMS = -32602
INTERNAL_ERROR = -32603


def _server_info() -> dict:
    try:
        import core

        version = getattr(core, "__version__", "")
    except Exception:
        version = ""
    return {"name": "Spwig Storefront", "version": version or "1.0"}


def _result(request_id, result):
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def _error(request_id, code, message):
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def _handle(message: dict, request):
    """Dispatch one JSON-RPC message. Returns a response dict, or None for a notification."""
    if message.get("jsonrpc") != "2.0" or "method" not in message:
        return _error(message.get("id"), INVALID_REQUEST, "Not a valid JSON-RPC 2.0 request.")

    method = message["method"]
    request_id = message.get("id")
    is_notification = "id" not in message
    params = message.get("params") or {}

    # Notifications (no id) never get a response.
    if is_notification:
        return None

    if method == "initialize":
        return _result(
            request_id,
            {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {}},
                "serverInfo": _server_info(),
            },
        )

    if method == "ping":
        return _result(request_id, {})

    if method == "tools/list":
        return _result(request_id, {"tools": storefront_tools.TOOLS})

    if method == "tools/call":
        name = params.get("name")
        arguments = params.get("arguments") or {}
        if name not in storefront_tools.TOOL_NAMES:
            return _error(request_id, METHOD_NOT_FOUND, f"Unknown tool: {name!r}")
        try:
            data = storefront_tools.call_tool(name, arguments, request)
        except storefront_tools.ToolError as exc:
            # A tool-level failure is reported IN the result (isError), not as a
            # protocol error — that's how MCP surfaces tool errors to the model.
            return _result(
                request_id,
                {"content": [{"type": "text", "text": str(exc)}], "isError": True},
            )
        return _result(
            request_id,
            {
                "content": [{"type": "text", "text": json.dumps(data)}],
                "structuredContent": data,
            },
        )

    return _error(request_id, METHOD_NOT_FOUND, f"Unknown method: {method!r}")


@csrf_exempt
def mcp_endpoint(request):
    require_agentic()
    require_protocol("mcp")

    if request.method != "POST":
        # A bare GET (some clients probe for an SSE stream) is not supported here.
        return HttpResponse(status=405)

    # Enforce the merchant's read posture: unsigned is allowed only when
    # unverified reads are permitted; a present-but-invalid signature is 401,
    # and too many signed attempts is 429 (this plain view has no DRF throttle).
    try:
        require_read_access(request)
    except AgentRateLimited as exc:
        return JsonResponse({"error": "rate_limited", "message": str(exc.reason)}, status=429)
    except AgentAuthError as exc:
        return JsonResponse({"error": "unauthorized", "message": str(exc.reason)}, status=401)

    try:
        message = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(_error(None, PARSE_ERROR, "Invalid JSON."), status=400)

    if isinstance(message, list):
        # Batching was removed from MCP; reject it explicitly rather than guess.
        return JsonResponse(
            _error(None, INVALID_REQUEST, "JSON-RPC batching is not supported."),
            status=400,
        )
    if not isinstance(message, dict):
        return JsonResponse(_error(None, INVALID_REQUEST, "Expected a JSON object."), status=400)

    try:
        response = _handle(message, request)
    except Http404:
        raise
    except Exception:
        logger.exception("MCP handler error")
        return JsonResponse(
            _error(message.get("id"), INTERNAL_ERROR, "Internal error."), status=500
        )

    if response is None:
        # Notification — nothing to return.
        return HttpResponse(status=202)
    return JsonResponse(response)
