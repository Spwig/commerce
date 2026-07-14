from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.decorators.http import require_GET


@staff_member_required
@require_GET
def filter_store_groups(request):
    """AJAX endpoint for filtering store groups."""
    from django.db.models import Count, Q
    from django.template.loader import render_to_string

    from .models import StoreGroup

    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Extract filters
    search = request.GET.get("search", "").strip()
    currency = request.GET.get("currency", "").strip()
    is_active = request.GET.get("is_active", "").strip()

    # Build queryset
    queryset = StoreGroup.objects.annotate(store_count=Count("warehouses")).all()

    # Apply filters
    if search:
        queryset = queryset.filter(Q(name__icontains=search) | Q(code__icontains=search))

    if currency:
        queryset = queryset.filter(currency=currency)

    if is_active == "true":
        queryset = queryset.filter(is_active=True)
    elif is_active == "false":
        queryset = queryset.filter(is_active=False)

    # Order by sort order
    queryset = queryset.order_by("sort_order", "name")

    # Render results
    html = render_to_string(
        "admin/pos_app/storegroup/partials/storegroup_cards.html",
        {"store_groups": queryset},
        request=request,
    )

    return JsonResponse({"html": html, "count": queryset.count()})
