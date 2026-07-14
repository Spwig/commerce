"""
Design Admin Views
Admin-specific views for AJAX endpoints
"""

from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import DesignToken


def filter_design_tokens(request):
    """
    AJAX endpoint for filtering design tokens in admin

    Query Parameters:
    - search: Search by name or value
    - token_type: Filter by token type
    - source: Filter by source
    - priority: Filter by priority level
    - status: Filter by active/inactive status
    """
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Start with all tokens
    tokens = DesignToken.objects.select_related("theme", "component")

    # Search filter
    search = request.GET.get("search", "").strip()
    if search:
        tokens = tokens.filter(
            Q(name__icontains=search)
            | Q(value__icontains=search)
            | Q(description__icontains=search)
        )

    # Token type filter
    token_type = request.GET.get("token_type", "")
    if token_type:
        tokens = tokens.filter(token_type=token_type)

    # Source filter
    source = request.GET.get("source", "")
    if source:
        tokens = tokens.filter(source=source)

    # Priority filter
    priority = request.GET.get("priority", "")
    if priority:
        try:
            priority_level = int(priority)
            tokens = tokens.filter(priority_level=priority_level)
        except ValueError:
            pass

    # Status filter
    status = request.GET.get("status", "")
    if status == "active":
        tokens = tokens.filter(is_active=True)
    elif status == "inactive":
        tokens = tokens.filter(is_active=False)

    # Order by priority level, then by name
    tokens = tokens.order_by("priority_level", "token_type", "name")

    # Render partial template
    html = render_to_string(
        "admin/design/partials/designtoken_cards.html", {"tokens": tokens, "request": request}
    )

    return JsonResponse({"html": html, "count": tokens.count()})


from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_GET


@staff_member_required
@require_GET
def filter_widgets(request):
    """AJAX endpoint for filtering widgets."""
    from django.db.models import Count, Q
    from django.template.loader import render_to_string

    from .header_footer_models import Widget

    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Extract filters
    search = request.GET.get("search", "").strip()
    widget_type = request.GET.get("widget_type", "").strip()
    is_active = request.GET.get("is_active", "").strip()

    # Build queryset with usage count
    queryset = Widget.objects.annotate(placement_count=Count("placements")).select_related(
        "created_by"
    )

    # Apply filters
    if search:
        queryset = queryset.filter(Q(name__icontains=search) | Q(content__icontains=search))

    if widget_type:
        queryset = queryset.filter(widget_type=widget_type)

    if is_active == "true":
        queryset = queryset.filter(is_active=True)
    elif is_active == "false":
        queryset = queryset.filter(is_active=False)

    # Order by type and name
    queryset = queryset.order_by("widget_type", "name")

    # Render results
    html = render_to_string(
        "admin/design/widget/partials/widget_cards.html", {"widgets": queryset}, request=request
    )

    return JsonResponse({"html": html, "count": queryset.count()})
