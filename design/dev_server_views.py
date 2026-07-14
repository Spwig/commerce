"""
Theme SDK Development Server API Views.

API endpoints for the Spwig Theme SDK CLI to connect to a running
shop instance for live theme development with hot reload.

All endpoints are under /api/theme-dev/ (non-i18n, no language prefix).
"""

import base64
import json
import logging
from functools import wraps

from django.conf import settings
from django.contrib.auth import authenticate
from django.http import JsonResponse, StreamingHttpResponse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from .dev_server_service import get_dev_server_service

logger = logging.getLogger(__name__)


def dev_server_enabled(view_func):
    """Decorator to check if dev server is enabled."""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not settings.DEBUG:
            return JsonResponse({"error": "Dev server is only available in DEBUG mode"}, status=403)
        return view_func(request, *args, **kwargs)

    return wrapper


def require_dev_token(view_func):
    """Decorator to validate dev session token."""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        token = request.META.get("HTTP_X_DEV_TOKEN", "")
        if not token:
            return JsonResponse({"error": "Missing X-Dev-Token header"}, status=401)

        service = get_dev_server_service()
        session = service.validate_token(token)
        if not session:
            return JsonResponse({"error": "Invalid or expired dev token"}, status=401)

        # Attach session to request
        request.dev_session = session
        return view_func(request, *args, **kwargs)

    return wrapper


# ========== Session Management ==========


@extend_schema(
    summary=_("Connect to dev server"),
    description=_("""
    Authenticate with the Spwig shop and create a development session.

    **Authentication**: Basic auth with admin credentials

    Returns a session token for subsequent API calls.
    """),
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "theme_name": {"type": "string", "description": "Name of theme being developed"},
                "theme_path": {"type": "string", "description": "Local path on developer machine"},
                "client_info": {
                    "type": "object",
                    "description": "CLI version, OS, Node version",
                    "properties": {
                        "cli_version": {"type": "string"},
                        "node_version": {"type": "string"},
                        "os": {"type": "string"},
                    },
                },
            },
            "required": ["theme_name"],
        }
    },
    responses={
        200: OpenApiResponse(description=_("Session created successfully")),
        401: OpenApiResponse(description=_("Authentication failed")),
        403: OpenApiResponse(description=_("Dev server not enabled")),
    },
    tags=["Theme Development"],
)
@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
@dev_server_enabled
def dev_connect(request):
    """Create a new development session."""
    # Basic auth
    auth_header = request.META.get("HTTP_AUTHORIZATION", "")
    if not auth_header.startswith("Basic "):
        return JsonResponse({"error": "Basic authentication required"}, status=401)

    try:
        credentials = base64.b64decode(auth_header[6:]).decode("utf-8")
        username, password = credentials.split(":", 1)
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({"error": "Invalid authorization header"}, status=401)

    # Authenticate user
    user = authenticate(request, username=username, password=password)
    if not user or not user.is_staff:
        return JsonResponse(
            {"error": "Invalid credentials or insufficient permissions"}, status=401
        )

    # Parse request data
    try:
        data = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    theme_name = data.get("theme_name", "")
    if not theme_name:
        return JsonResponse({"error": "theme_name is required"}, status=400)

    # Create session
    service = get_dev_server_service()
    session = service.create_session(
        user=user,
        theme_name=theme_name,
        theme_path=data.get("theme_path", ""),
        client_info=data.get("client_info", {}),
    )

    return JsonResponse(
        {
            "token": session.token,
            "expires_at": session.expires_at.isoformat(),
            "theme_dev_url": f"/api/theme-dev/preview/?token={session.token}",
            "message": f"Connected as {user.username}",
        }
    )


@extend_schema(
    summary=_("Disconnect from dev server"),
    description=_("End the development session and cleanup resources."),
    responses={
        200: OpenApiResponse(description=_("Session ended successfully")),
        401: OpenApiResponse(description=_("Invalid token")),
    },
    tags=["Theme Development"],
)
@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
@dev_server_enabled
@require_dev_token
def dev_disconnect(request):
    """End a development session."""
    service = get_dev_server_service()
    service.end_session(request.dev_session)

    return JsonResponse({"message": "Session ended successfully"})


@extend_schema(
    summary=_("Get session status"),
    description=_("Get current status of the development session."),
    responses={
        200: OpenApiResponse(description=_("Session status")),
        401: OpenApiResponse(description=_("Invalid token")),
    },
    tags=["Theme Development"],
)
@api_view(["GET"])
@permission_classes([AllowAny])
@dev_server_enabled
@require_dev_token
def dev_status(request):
    """Get session status."""
    service = get_dev_server_service()
    status = service.get_session_status(request.dev_session)

    return JsonResponse(status)


# ========== File Synchronization ==========


@extend_schema(
    summary=_("Sync theme files"),
    description=_("""
    Sync individual files from SDK to dev server.

    Send an array of files with path, content (base64 for binary), and checksum.
    Files are written to the dev theme directory and trigger appropriate reload.
    """),
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "files": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "Relative file path"},
                            "content": {
                                "type": "string",
                                "description": "File content (base64 for binary)",
                            },
                            "checksum": {"type": "string", "description": "SHA256 checksum"},
                            "encoding": {"type": "string", "enum": ["utf-8", "base64"]},
                        },
                        "required": ["path", "content"],
                    },
                }
            },
            "required": ["files"],
        }
    },
    responses={
        200: OpenApiResponse(description=_("Files synced successfully")),
        400: OpenApiResponse(description=_("Invalid request")),
        401: OpenApiResponse(description=_("Invalid token")),
    },
    tags=["Theme Development"],
)
@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
@dev_server_enabled
@require_dev_token
def dev_sync_files(request):
    """Sync individual files from SDK."""
    try:
        data = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    files = data.get("files", [])
    if not files:
        return JsonResponse({"error": "No files provided"}, status=400)

    # Decode base64 content where needed
    processed_files = []
    for file_data in files:
        processed = {"path": file_data.get("path", ""), "checksum": file_data.get("checksum", "")}

        content = file_data.get("content", "")
        encoding = file_data.get("encoding", "utf-8")

        if encoding == "base64":
            try:
                processed["content"] = base64.b64decode(content)
            except Exception:
                return JsonResponse(
                    {"error": f"Failed to decode base64 for {processed['path']}"}, status=400
                )
        else:
            processed["content"] = content

        processed_files.append(processed)

    service = get_dev_server_service()
    success, result = service.sync_files(request.dev_session, processed_files)

    return JsonResponse({"success": success, **result})


@extend_schema(
    summary=_("Sync full theme archive"),
    description=_("""
    Sync a complete theme as a ZIP archive.

    The archive replaces the entire dev theme directory.
    Send the ZIP file as raw binary in the request body.
    """),
    responses={
        200: OpenApiResponse(description=_("Theme synced successfully")),
        400: OpenApiResponse(description=_("Invalid archive")),
        401: OpenApiResponse(description=_("Invalid token")),
    },
    tags=["Theme Development"],
)
@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
@dev_server_enabled
@require_dev_token
def dev_sync_full(request):
    """Sync complete theme archive."""
    if not request.body:
        return JsonResponse({"error": "No archive provided"}, status=400)

    service = get_dev_server_service()
    success, result = service.sync_full_theme(request.dev_session, request.body)

    if success:
        return JsonResponse({"success": True, **result})
    else:
        return JsonResponse(
            {"success": False, "error": result.get("error", "Sync failed")}, status=400
        )


# ========== Hot Reload (SSE) ==========


@extend_schema(
    summary=_("Watch for reload events"),
    description=_("""
    Server-Sent Events stream for hot reload notifications.

    Events:
    - `css`: CSS-only reload (no page refresh)
    - `full`: Full page reload
    - `keepalive`: Connection keepalive

    Inject a small JS snippet in dev mode to listen to this stream.
    """),
    responses={
        200: OpenApiResponse(description=_("SSE stream")),
        401: OpenApiResponse(description=_("Invalid token")),
    },
    tags=["Theme Development"],
)
@dev_server_enabled
def dev_watch(request):
    """SSE stream for hot reload events."""
    token = request.GET.get("token", "")
    if not token:
        return JsonResponse({"error": "Missing token parameter"}, status=401)

    service = get_dev_server_service()
    session = service.validate_token(token)
    if not session:
        return JsonResponse({"error": "Invalid or expired token"}, status=401)

    def event_stream():
        """Generate SSE events."""
        for event in service.get_reload_events(token):
            event_type = event.get("type", "message")
            data = json.dumps(event)
            yield f"event: {event_type}\ndata: {data}\n\n"

    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response["Cache-Control"] = "no-cache"
    response["X-Accel-Buffering"] = "no"
    return response


# ========== Theme Operations ==========


@extend_schema(
    summary=_("Validate theme"),
    description=_("Run validation on the synced dev theme."),
    responses={
        200: OpenApiResponse(description=_("Validation result")),
        401: OpenApiResponse(description=_("Invalid token")),
    },
    tags=["Theme Development"],
)
@api_view(["GET"])
@permission_classes([AllowAny])
@dev_server_enabled
@require_dev_token
def dev_validate(request):
    """Validate the dev theme."""
    service = get_dev_server_service()
    result = service.validate_theme(request.dev_session)

    return JsonResponse(result)


@extend_schema(
    summary=_("Compile theme CSS"),
    description=_("Compile CSS from design tokens and return the URL."),
    responses={
        200: OpenApiResponse(description=_("CSS compiled successfully")),
        400: OpenApiResponse(description=_("Compilation failed")),
        401: OpenApiResponse(description=_("Invalid token")),
    },
    tags=["Theme Development"],
)
@api_view(["POST"])
@permission_classes([AllowAny])
@dev_server_enabled
@require_dev_token
def dev_compile_css(request):
    """Compile CSS from design tokens."""
    service = get_dev_server_service()
    success, result = service.compile_css(request.dev_session)

    if success:
        return JsonResponse({"success": True, "css_url": result})
    else:
        return JsonResponse({"success": False, "error": result}, status=400)


# ========== Component Operations ==========


@extend_schema(
    summary=_("List theme components"),
    description=_("List all bundled components in the dev theme."),
    responses={
        200: OpenApiResponse(description=_("Component list")),
        401: OpenApiResponse(description=_("Invalid token")),
    },
    tags=["Theme Development"],
)
@api_view(["GET"])
@permission_classes([AllowAny])
@dev_server_enabled
@require_dev_token
def dev_list_components(request):
    """List components in the dev theme."""
    service = get_dev_server_service()
    components = service.list_components(request.dev_session)

    return JsonResponse({"components": components, "count": len(components)})


@extend_schema(
    summary=_("Get component details"),
    description=_("Get details for a specific component by name."),
    parameters=[
        OpenApiParameter(
            name="component_name",
            location=OpenApiParameter.PATH,
            description=_("Component name"),
            required=True,
            type=str,
        )
    ],
    responses={
        200: OpenApiResponse(description=_("Component details")),
        404: OpenApiResponse(description=_("Component not found")),
        401: OpenApiResponse(description=_("Invalid token")),
    },
    tags=["Theme Development"],
)
@api_view(["GET"])
@permission_classes([AllowAny])
@dev_server_enabled
@require_dev_token
def dev_component_detail(request, component_name):
    """Get details for a specific component."""
    service = get_dev_server_service()
    component = service.get_component(request.dev_session, component_name)

    if component:
        return JsonResponse(component)
    else:
        return JsonResponse({"error": f"Component '{component_name}' not found"}, status=404)


# ========== Preview ==========


@extend_schema(
    summary=_("Get preview URL"),
    description=_("Get the URL to preview the dev theme in the shop."),
    responses={
        200: OpenApiResponse(description=_("Preview URL")),
        401: OpenApiResponse(description=_("Invalid token")),
    },
    tags=["Theme Development"],
)
@api_view(["GET"])
@permission_classes([AllowAny])
@dev_server_enabled
@require_dev_token
def dev_preview_url(request):
    """Get the preview URL for the dev theme."""
    session = request.dev_session

    # The preview URL would load the shop with the dev theme applied
    preview_url = f"/?dev_theme={session.token}"

    return JsonResponse(
        {
            "preview_url": preview_url,
            "theme_name": session.theme_name,
            "watch_url": f"/api/theme-dev/watch/?token={session.token}",
        }
    )
