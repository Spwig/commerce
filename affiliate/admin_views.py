"""
Admin AJAX views for affiliate app.
Handles list filtering for admin change_list templates.
"""
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q

from affiliate.models import Commission, Affiliate, Program, AffiliateProgramMembership, Payout

# Whitelisted order_by fields per model to prevent arbitrary field enumeration
COMMISSION_ORDER_FIELDS = {
    'created_at', '-created_at', 'amount', '-amount', 'status', '-status',
}
AFFILIATE_ORDER_FIELDS = {
    'created_at', '-created_at', 'user__email', '-user__email',
    'status', '-status', 'affiliate_code', '-affiliate_code',
}
PROGRAM_ORDER_FIELDS = {
    'created_at', '-created_at', 'name', '-name', 'status', '-status',
}
MEMBERSHIP_ORDER_FIELDS = {
    'joined_at', '-joined_at', 'status', '-status',
}
PAYOUT_ORDER_FIELDS = {
    'created_at', '-created_at', 'amount', '-amount', 'status', '-status',
}


def _safe_int(value):
    """Return integer or None for ID filter parameters."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


@staff_member_required
def filter_commissions(request):
    """
    AJAX endpoint for filtering commissions in admin.

    Supports filtering by:
    - search: Affiliate code, order number
    - status: pending, approved, paid, rejected, reversed
    - affiliate: Affiliate ID
    - program: Program ID
    """
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    # Get filter parameters
    search = request.GET.get('search', '').strip()
    status = request.GET.get('status', '').strip()
    affiliate_id = request.GET.get('affiliate', '').strip()
    program_id = request.GET.get('program', '').strip()

    # Build query
    commissions = Commission.objects.select_related(
        'affiliate', 'affiliate__user', 'program', 'order'
    ).order_by('-created_at')

    # Apply filters
    if search:
        commissions = commissions.filter(
            Q(affiliate__affiliate_code__icontains=search) |
            Q(order__order_number__icontains=search) |
            Q(affiliate__user__username__icontains=search) |
            Q(affiliate__user__email__icontains=search)
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
        'admin/affiliate/partials/commission_cards.html',
        {'commissions': commissions}
    )

    return JsonResponse({'html': html, 'count': commissions.count()})


@staff_member_required
def filter_affiliates(request):
    """AJAX endpoint for filtering affiliates."""
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    # Extract filters
    search = request.GET.get('search', '').strip()
    status = request.GET.get('status', '').strip()
    payment_method = request.GET.get('payment-method', '').strip()
    order = request.GET.get('order', '-created_at').strip()

    # Build queryset
    queryset = Affiliate.objects.select_related('user').all()

    # Apply filters
    if search:
        queryset = queryset.filter(
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(user__email__icontains=search) |
            Q(affiliate_code__icontains=search) |
            Q(company_name__icontains=search)
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
        'admin/affiliate/partials/affiliate_cards.html',
        {'affiliates': queryset}
    )

    return JsonResponse({'html': html, 'count': queryset.count()})


@staff_member_required
def filter_programs(request):
    """AJAX endpoint for filtering affiliate programs."""
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    # Extract filters
    search = request.GET.get('search', '').strip()
    status = request.GET.get('status', '').strip()
    commission_type = request.GET.get('commission-type', '').strip()
    order = request.GET.get('order', '-created_at').strip()

    # Build queryset
    queryset = Program.objects.all()

    # Apply filters
    if search:
        queryset = queryset.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )

    if status:
        queryset = queryset.filter(is_active=(status == 'active'))

    if commission_type:
        queryset = queryset.filter(commission_type=commission_type)

    # Apply sorting (whitelist only)
    if order and order in PROGRAM_ORDER_FIELDS:
        queryset = queryset.order_by(order)

    # Render results
    html = render_to_string(
        'admin/affiliate/partials/program_cards.html',
        {'programs': queryset}
    )

    return JsonResponse({'html': html, 'count': queryset.count()})


@staff_member_required
def filter_memberships(request):
    """AJAX endpoint for filtering affiliate program memberships."""
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    # Extract filters
    search = request.GET.get('search', '').strip()
    status = request.GET.get('status', '').strip()
    program_id = request.GET.get('program', '').strip()
    order = request.GET.get('order', '-joined_at').strip()

    # Build queryset
    queryset = AffiliateProgramMembership.objects.select_related(
        'affiliate', 'affiliate__user', 'program'
    ).all()

    # Apply filters
    if search:
        queryset = queryset.filter(
            Q(affiliate__user__email__icontains=search) |
            Q(affiliate__affiliate_code__icontains=search) |
            Q(program__name__icontains=search)
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
        'admin/affiliate/partials/membership_cards.html',
        {'memberships': queryset}
    )

    return JsonResponse({'html': html, 'count': queryset.count()})


@staff_member_required
def filter_payouts(request):
    """AJAX endpoint for filtering affiliate payouts."""
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    # Extract filters
    search = request.GET.get('search', '').strip()
    status = request.GET.get('status', '').strip()
    payment_method = request.GET.get('payment-method', '').strip()
    order = request.GET.get('order', '-created_at').strip()

    # Build queryset
    queryset = Payout.objects.select_related('affiliate', 'affiliate__user').all()

    # Apply filters
    if search:
        queryset = queryset.filter(
            Q(affiliate__user__email__icontains=search) |
            Q(affiliate__affiliate_code__icontains=search) |
            Q(reference_number__icontains=search)
        )

    if status:
        queryset = queryset.filter(status=status)

    if payment_method:
        queryset = queryset.filter(payment_method=payment_method)

    # Apply sorting (whitelist only)
    if order and order in PAYOUT_ORDER_FIELDS:
        queryset = queryset.order_by(order)

    # Render results
    html = render_to_string(
        'admin/affiliate/partials/payout_cards.html',
        {'payouts': queryset}
    )

    return JsonResponse({'html': html, 'count': queryset.count()})
