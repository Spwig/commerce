"""
Vouchers views package.

`filter_voucher_codes` (this module) backs the existing admin list AJAX
filter. The voucher import wizard views live in `import_export`.
"""

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string

from ..models import VoucherCode


@staff_member_required
def filter_voucher_codes(request):
    """
    AJAX endpoint for filtering voucher codes in admin.

    Supports filtering by:
    - search: Code, name, description
    - type: Discount type (percentage/fixed/gift_card)
    - status: Active/inactive
    - scope: Application scope (cart/products/categories)
    """
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    search = request.GET.get("search", "").strip() or request.GET.get("q", "").strip()
    discount_type = (
        request.GET.get("type", "").strip() or request.GET.get("discount_type__exact", "").strip()
    )
    status = (
        request.GET.get("status", "").strip() or request.GET.get("is_active__exact", "").strip()
    )
    scope = (
        request.GET.get("scope", "").strip()
        or request.GET.get("application_scope__exact", "").strip()
    )

    vouchers = VoucherCode.objects.all().order_by("-created_at")

    if search:
        vouchers = vouchers.filter(
            Q(code__icontains=search) | Q(name__icontains=search) | Q(description__icontains=search)
        )

    if discount_type:
        vouchers = vouchers.filter(discount_type=discount_type)

    if status:
        is_active = status == "1" or status.lower() == "active"
        vouchers = vouchers.filter(is_active=is_active)

    if scope:
        vouchers = vouchers.filter(application_scope=scope)

    html = render_to_string(
        "admin/vouchers/vouchercode/voucher_cards.html",
        {"vouchers": vouchers},
    )

    return JsonResponse({"html": html, "count": vouchers.count()})
