"""
Shipping Admin AJAX Views.
Provides AJAX filter endpoints for admin change list pages.
"""

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET

from .models import ShippingPackage, TrackingEvent, WebhookLog


@staff_member_required
@require_GET
def filter_shipping_packages(request):
    """AJAX filter endpoint for ShippingPackage entries."""
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    queryset = ShippingPackage.objects.all()

    # Search filter
    search = request.GET.get("search", "").strip()
    if search:
        queryset = queryset.filter(Q(name__icontains=search) | Q(description__icontains=search))

    # Status filter
    status = request.GET.get("status", "").strip()
    if status == "active":
        queryset = queryset.filter(is_active=True)
    elif status == "inactive":
        queryset = queryset.filter(is_active=False)

    # Sort
    sort = request.GET.get("sort", "").strip()
    if sort == "name":
        queryset = queryset.order_by("name")
    elif sort == "volume":
        queryset = queryset.order_by("length")
    elif sort == "max_weight":
        queryset = queryset.order_by("max_weight")
    else:
        queryset = queryset.order_by("-priority", "name")

    total_count = queryset.count()

    html = render_to_string(
        "admin/shipping/shippingpackage/package_cards.html", {"packages": queryset}, request=request
    )

    return JsonResponse(
        {
            "html": html,
            "count": total_count,
        }
    )


@staff_member_required
@require_GET
def filter_tracking_events(request):
    """AJAX filter endpoint for TrackingEvent entries."""
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    queryset = TrackingEvent.objects.select_related("shipment").all()

    # Search filter
    search = request.GET.get("search", "").strip()
    if search:
        queryset = queryset.filter(Q(location__icontains=search) | Q(description__icontains=search))

    # Status filter
    status = request.GET.get("status", "").strip()
    if status:
        queryset = queryset.filter(status=status)

    total_count = queryset.count()
    events = queryset.order_by("-occurred_at")[:100]

    html = render_to_string(
        "admin/shipping/trackingevent/event_cards.html", {"events": events}, request=request
    )

    return JsonResponse(
        {
            "html": html,
            "count": total_count,
        }
    )


@staff_member_required
@require_GET
def filter_webhook_logs(request):
    """AJAX filter endpoint for WebhookLog entries."""
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    queryset = WebhookLog.objects.all()

    # Search filter
    search = request.GET.get("search", "").strip()
    if search:
        queryset = queryset.filter(
            Q(provider_key__icontains=search)
            | Q(endpoint__icontains=search)
            | Q(error_message__icontains=search)
        )

    # Provider filter
    provider = request.GET.get("provider", "").strip()
    if provider:
        queryset = queryset.filter(provider_key=provider)

    # Status filter
    status = request.GET.get("status", "").strip()
    if status:
        queryset = queryset.filter(processing_status=status)

    # HTTP status filter
    http_status = request.GET.get("http_status", "").strip()
    if http_status == "2xx":
        queryset = queryset.filter(status_code__gte=200, status_code__lt=300)
    elif http_status == "4xx":
        queryset = queryset.filter(status_code__gte=400, status_code__lt=500)
    elif http_status == "5xx":
        queryset = queryset.filter(status_code__gte=500)

    total_count = queryset.count()
    logs = queryset.order_by("-received_at")[:100]

    html = render_to_string(
        "admin/shipping/webhooklog/log_cards.html", {"logs": logs}, request=request
    )

    return JsonResponse(
        {
            "html": html,
            "count": total_count,
        }
    )
