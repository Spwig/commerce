"""
Payout Provider Admin Views

AJAX filter endpoint for payout provider accounts list.
"""

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET

from .models import PayoutProviderAccount


@staff_member_required
@require_GET
def filter_providers(request):
    """AJAX filter endpoint for payout provider accounts."""
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    queryset = PayoutProviderAccount.objects.select_related("component").all()

    # Search filter
    search = request.GET.get("search", "").strip()
    if search:
        queryset = queryset.filter(Q(name__icontains=search) | Q(provider_type__icontains=search))

    # Connection status filter
    status = request.GET.get("status", "").strip()
    if status:
        queryset = queryset.filter(connection_status=status)

    # Active status filter
    active = request.GET.get("active", "").strip()
    if active == "active":
        queryset = queryset.filter(is_active=True)
    elif active == "inactive":
        queryset = queryset.filter(is_active=False)

    # Provider type filter
    provider_type = request.GET.get("provider-type", "").strip()
    if provider_type:
        queryset = queryset.filter(provider_type=provider_type)

    total_count = queryset.count()
    providers = queryset.order_by("-is_default", "-is_active", "name")[:100]

    html = render_to_string(
        "admin/payout_providers/payoutprovideraccount/partials/provider_cards.html",
        {"providers": providers},
        request=request,
    )

    return JsonResponse({"html": html, "count": total_count})
