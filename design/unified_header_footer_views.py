"""
Unified Header/Footer Management Views
Modern card-based interface for managing header and footer templates
"""

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Q
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from .header_footer_models import FooterTemplate, HeaderTemplate


@staff_member_required
def unified_header_management_view(request):
    """
    Unified view for header template management with modern interface
    """
    filter_type = request.GET.get("filter", "all")  # all, active, inactive
    search_query = request.GET.get("q", "")

    context = {
        "title": _("Header Management"),
        "filter_type": filter_type,
        "search_query": search_query,
        "headers": [],
    }

    # Get default header (the one marked as is_default=True)
    default_header = HeaderTemplate.objects.filter(is_default=True).first()

    # Get all headers with widget placement counts and page counts
    headers = HeaderTemplate.objects.annotate(
        widget_count=Count("widget_placements"), page_count=Count("pages")
    ).order_by("-is_default", "-is_active", "name")

    # Apply search filter
    if search_query:
        headers = headers.filter(
            Q(name__icontains=search_query)
            | Q(slug__icontains=search_query)
            | Q(description__icontains=search_query)
        )

    # Build header data list
    headers_data = []
    for header in headers:
        # Count usage (how many pages/views use this header)
        # For now, we'll use widget count as a proxy for complexity
        usage_count = header.widget_count

        header_data = {
            "id": header.id,
            "name": header.name,
            "slug": header.slug,
            "description": header.description or "",
            "layout_type": header.layout_type,
            "layout_type_display": header.get_layout_type_display(),
            "is_sticky": header.is_sticky,
            "has_top_bar": header.has_top_bar,
            "is_active": header.is_active,
            "is_default": header.is_default,
            "widget_count": usage_count,
            "page_count": header.page_count,
            "mobile_layout": header.mobile_layout,
            "created_by": header.created_by.username if header.created_by else _("System"),
            "created_at": header.created_at,
        }
        headers_data.append(header_data)

    # Calculate counts before filtering
    all_count = len(headers_data)
    active_count = sum(1 for h in headers_data if h["is_active"])
    inactive_count = sum(1 for h in headers_data if not h["is_active"])

    # Apply status filter
    if filter_type == "active":
        headers_data = [h for h in headers_data if h["is_active"]]
    elif filter_type == "inactive":
        headers_data = [h for h in headers_data if not h["is_active"]]

    context["headers"] = headers_data
    context["default_header"] = default_header
    context["all_count"] = all_count
    context["active_count"] = active_count
    context["inactive_count"] = inactive_count

    return render(request, "admin/design/headertemplate/unified_management.html", context)


@staff_member_required
def unified_footer_management_view(request):
    """
    Unified view for footer template management with modern interface
    """
    filter_type = request.GET.get("filter", "all")  # all, active, inactive
    search_query = request.GET.get("q", "")

    context = {
        "title": _("Footer Management"),
        "filter_type": filter_type,
        "search_query": search_query,
        "footers": [],
    }

    # Get default footer (the one marked as is_default=True)
    default_footer = FooterTemplate.objects.filter(is_default=True).first()

    # Get all footers with widget placement counts
    footers = FooterTemplate.objects.annotate(widget_count=Count("widget_placements")).order_by(
        "-is_default", "-is_active", "name"
    )

    # Apply search filter
    if search_query:
        footers = footers.filter(
            Q(name__icontains=search_query)
            | Q(slug__icontains=search_query)
            | Q(description__icontains=search_query)
        )

    # Build footer data list
    footers_data = []
    for footer in footers:
        # Count usage (how many pages/views use this footer)
        usage_count = footer.widget_count

        footer_data = {
            "id": footer.id,
            "name": footer.name,
            "slug": footer.slug,
            "description": footer.description or "",
            "layout_type": footer.layout_type,
            "layout_type_display": footer.get_layout_type_display(),
            "column_count": footer.column_count,
            "has_bottom_bar": footer.has_bottom_bar,
            "is_active": footer.is_active,
            "is_default": footer.is_default,
            "widget_count": usage_count,
            "background_color": footer.background_color,
            "text_color": footer.text_color,
            "created_by": footer.created_by.username if footer.created_by else _("System"),
            "created_at": footer.created_at,
        }
        footers_data.append(footer_data)

    # Calculate counts before filtering
    all_count = len(footers_data)
    active_count = sum(1 for f in footers_data if f["is_active"])
    inactive_count = sum(1 for f in footers_data if not f["is_active"])

    # Apply status filter
    if filter_type == "active":
        footers_data = [f for f in footers_data if f["is_active"]]
    elif filter_type == "inactive":
        footers_data = [f for f in footers_data if not f["is_active"]]

    context["footers"] = footers_data
    context["default_footer"] = default_footer
    context["all_count"] = all_count
    context["active_count"] = active_count
    context["inactive_count"] = inactive_count

    return render(request, "admin/design/footertemplate/unified_management.html", context)
