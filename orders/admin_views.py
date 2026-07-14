"""
Orders Admin Views.
AJAX filter endpoints for admin change lists.
"""

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET

from .models import ReturnRequest


@staff_member_required
@require_GET
def filter_return_requests(request):
    """
    AJAX endpoint for filtering return requests in admin.

    Query Parameters:
    - search: Search by order number, customer name, or tracking number
    - status: Filter by return status
    - reason: Filter by return reason
    """
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    queryset = ReturnRequest.objects.select_related("order", "user", "return_shipment").order_by(
        "-created_at"
    )

    # Search filter
    search = request.GET.get("search", "").strip()
    if search:
        queryset = queryset.filter(
            Q(order__order_number__icontains=search)
            | Q(user__first_name__icontains=search)
            | Q(user__last_name__icontains=search)
            | Q(user__email__icontains=search)
            | Q(tracking_number__icontains=search)
        )

    # Status filter
    status = request.GET.get("status", "").strip()
    if status:
        queryset = queryset.filter(status=status)

    # Reason filter
    reason = request.GET.get("reason", "").strip()
    if reason:
        queryset = queryset.filter(reason=reason)

    total_count = queryset.count()

    html = render_to_string(
        "admin/orders/returnrequest/request_cards.html",
        {"requests": queryset[:100]},
        request=request,
    )

    return JsonResponse(
        {
            "html": html,
            "count": total_count,
        }
    )
