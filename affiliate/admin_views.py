"""
Admin AJAX views for affiliate app.
Handles list filtering for admin change_list templates.
"""

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, F, Q, Sum
from django.http import JsonResponse
from django.template.loader import render_to_string

from affiliate.models import Affiliate, AffiliateProgramMembership, Commission, Payout, Program

# Whitelisted order_by fields per model to prevent arbitrary field enumeration
COMMISSION_ORDER_FIELDS = {
    "created_at",
    "-created_at",
    "amount",
    "-amount",
    "status",
    "-status",
}
AFFILIATE_ORDER_FIELDS = {
    "created_at",
    "-created_at",
    "user__email",
    "-user__email",
    "status",
    "-status",
    "affiliate_code",
    "-affiliate_code",
}
PROGRAM_ORDER_FIELDS = {
    "created_at",
    "-created_at",
    "name",
    "-name",
    "status",
    "-status",
}
MEMBERSHIP_ORDER_FIELDS = {
    "applied_at",
    "-applied_at",
    "status",
    "-status",
}
PAYOUT_ORDER_FIELDS = {
    "created_at",
    "-created_at",
    "amount",
    "-amount",
    "status",
    "-status",
}


from staff_roles.decorators import requires_permission


def _safe_int(value):
    """Return integer or None for ID filter parameters."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


@staff_member_required
@requires_permission("affiliate.view_commission", ajax=True)
def filter_commissions(request):
    """
    AJAX endpoint for filtering commissions in admin.

    Supports filtering by:
    - search: Affiliate code, order number
    - status: pending, approved, paid, rejected, reversed
    - affiliate: Affiliate ID
    - program: Program ID
    """
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Get filter parameters
    search = request.GET.get("search", "").strip()
    status = request.GET.get("status", "").strip()
    affiliate_id = request.GET.get("affiliate", "").strip()
    program_id = request.GET.get("program", "").strip()

    # Build query
    commissions = Commission.objects.select_related(
        "affiliate", "affiliate__user", "program", "order"
    ).order_by("-created_at")

    # Apply filters
    if search:
        commissions = commissions.filter(
            Q(affiliate__affiliate_code__icontains=search)
            | Q(order__order_number__icontains=search)
            | Q(affiliate__user__username__icontains=search)
            | Q(affiliate__user__email__icontains=search)
        )

    if status:
        commissions = commissions.filter(status=status)

    if affiliate_id:
        aid = _safe_int(affiliate_id)
        if aid:
            commissions = commissions.filter(affiliate__id=aid)

    if program_id:
        pid = _safe_int(program_id)
        if pid:
            commissions = commissions.filter(program__id=pid)

    # Render results
    html = render_to_string(
        "admin/affiliate/partials/commission_cards.html", {"commissions": commissions}
    )

    return JsonResponse({"html": html, "count": commissions.count()})


@staff_member_required
@requires_permission("affiliate.view_affiliate", ajax=True)
def filter_affiliates(request):
    """AJAX endpoint for filtering affiliates."""
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Extract filters
    search = request.GET.get("search", "").strip()
    status = request.GET.get("status", "").strip()
    payment_method = request.GET.get("payment-method", "").strip()
    order = request.GET.get("order", "-created_at").strip()

    # Build queryset with the same annotations AffiliateAdmin uses for card display.
    # total_earned/outstanding_balance/total_paid are getter-only model properties,
    # so the earnings totals are annotated under sort_-prefixed names to avoid a
    # name clash (matching AffiliateAdmin.changelist_view).
    queryset = (
        Affiliate.objects.select_related("user")
        .annotate(
            programs_count=Count(
                "programs", filter=Q(affiliateprogrammembership__status="approved")
            ),
            links_count=Count("links"),
            sort_total_earned=Sum(
                "commissions__amount", filter=Q(commissions__status__in=["approved", "paid"])
            ),
            sort_outstanding_balance=Sum(
                "commissions__amount", filter=Q(commissions__status="approved")
            ),
        )
        .all()
    )

    # Apply filters
    if search:
        queryset = queryset.filter(
            Q(user__first_name__icontains=search)
            | Q(user__last_name__icontains=search)
            | Q(user__email__icontains=search)
            | Q(affiliate_code__icontains=search)
            | Q(company_name__icontains=search)
        )

    if status:
        queryset = queryset.filter(status=status)

    if payment_method:
        queryset = queryset.filter(payment_method=payment_method)

    # Apply sorting (whitelist only)
    if order and order in AFFILIATE_ORDER_FIELDS:
        queryset = queryset.order_by(order)

    # Render results
    html = render_to_string(
        "admin/affiliate/partials/affiliate_cards.html", {"affiliates": queryset}
    )

    return JsonResponse({"html": html, "count": queryset.count()})


@staff_member_required
def filter_programs(request):
    """AJAX endpoint for filtering affiliate programs."""
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Extract filters
    search = request.GET.get("search", "").strip()
    status = request.GET.get("status", "").strip()
    commission_type = request.GET.get("commission-type", "").strip()
    order = request.GET.get("order", "-created_at").strip()

    # Build queryset with the same annotations/eager loading the program changelist uses.
    queryset = Program.objects.select_related("merchant").annotate(
        affiliates_count=Count(
            "affiliates", filter=Q(affiliateprogrammembership__status="approved")
        ),
        active_affiliates=Count(
            "affiliates", filter=Q(affiliateprogrammembership__status="approved")
        ),
        total_earned=Sum("commissions__amount"),
    )

    # Apply filters
    if search:
        queryset = queryset.filter(Q(name__icontains=search) | Q(description__icontains=search))

    if status:
        queryset = queryset.filter(status=status)

    if commission_type:
        queryset = queryset.filter(commission_type=commission_type)

    # Apply sorting (whitelist only)
    if order and order in PROGRAM_ORDER_FIELDS:
        queryset = queryset.order_by(order)

    # Render results
    html = render_to_string("admin/affiliate/partials/program_cards.html", {"programs": queryset})

    return JsonResponse({"html": html, "count": queryset.count()})


@staff_member_required
def filter_memberships(request):
    """AJAX endpoint for filtering affiliate program memberships."""
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Extract filters
    search = request.GET.get("search", "").strip()
    status = request.GET.get("status", "").strip()
    program_id = request.GET.get("program", "").strip()
    order = request.GET.get("order", "-applied_at").strip()

    # Build queryset with the per-membership annotations the card template expects,
    # scoped to each membership's own program (matching filter_memberships in views.py).
    queryset = AffiliateProgramMembership.objects.select_related(
        "affiliate", "affiliate__user", "program"
    ).annotate(
        commissions_count=Count(
            "affiliate__commissions", filter=Q(affiliate__commissions__program=F("program"))
        ),
        total_earned=Sum(
            "affiliate__commissions__amount",
            filter=Q(
                affiliate__commissions__program=F("program"),
                affiliate__commissions__status__in=["approved", "paid"],
            ),
        ),
        links_count=Count("affiliate__links", filter=Q(affiliate__links__program=F("program"))),
    )

    # Apply filters
    if search:
        queryset = queryset.filter(
            Q(affiliate__user__email__icontains=search)
            | Q(affiliate__affiliate_code__icontains=search)
            | Q(program__name__icontains=search)
        )

    if status:
        queryset = queryset.filter(status=status)

    if program_id:
        pid = _safe_int(program_id)
        if pid:
            queryset = queryset.filter(program__id=pid)

    # Apply sorting (whitelist only)
    if order and order in MEMBERSHIP_ORDER_FIELDS:
        queryset = queryset.order_by(order)

    # Render results
    html = render_to_string(
        "admin/affiliate/partials/membership_cards.html", {"memberships": queryset}
    )

    return JsonResponse({"html": html, "count": queryset.count()})


@staff_member_required
@requires_permission("affiliate.view_payout", ajax=True)
def filter_payouts(request):
    """AJAX endpoint for filtering affiliate payouts."""
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Extract filters
    search = request.GET.get("search", "").strip()
    status = request.GET.get("status", "").strip()
    payment_method = request.GET.get("payment-method", "").strip()
    order = request.GET.get("order", "-created_at").strip()

    # Build queryset
    queryset = Payout.objects.select_related("affiliate", "affiliate__user").all()

    # Apply filters
    if search:
        queryset = queryset.filter(
            Q(affiliate__user__email__icontains=search)
            | Q(affiliate__affiliate_code__icontains=search)
            | Q(reference__icontains=search)
        )

    if status:
        queryset = queryset.filter(status=status)

    if payment_method:
        queryset = queryset.filter(method=payment_method)

    # Apply sorting (whitelist only)
    if order and order in PAYOUT_ORDER_FIELDS:
        queryset = queryset.order_by(order)

    # Render results
    html = render_to_string(
        "admin/affiliate/payout/partials/payout_cards.html", {"payouts": queryset}
    )

    return JsonResponse({"html": html, "count": queryset.count()})
