"""
Admin views for subscription management AJAX endpoints
"""
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q, Count
from .models import SubscriptionPlan, CustomerSubscription


@staff_member_required
def filter_subscription_plans(request):
    """AJAX endpoint for filtering subscription plans."""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    # Extract filters
    search = request.GET.get('search', '').strip()
    pricing_model = request.GET.get('pricing-model', '').strip()
    status = request.GET.get('status', '').strip()
    visibility = request.GET.get('visibility', '').strip()
    cancellation = request.GET.get('cancellation', '').strip()
    trial = request.GET.get('trial', '').strip()

    # Build queryset
    queryset = SubscriptionPlan.objects.annotate(
        subscription_count=Count('subscriptions')
    ).all()

    # Apply filters
    if search:
        queryset = queryset.filter(
            Q(name__icontains=search) |
            Q(slug__icontains=search) |
            Q(description__icontains=search)
        )

    if pricing_model:
        queryset = queryset.filter(pricing_model=pricing_model)

    if status:
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'inactive':
            queryset = queryset.filter(is_active=False)

    if visibility:
        if visibility == 'public':
            queryset = queryset.filter(is_public=True)
        elif visibility == 'private':
            queryset = queryset.filter(is_public=False)

    if cancellation:
        queryset = queryset.filter(cancellation_policy=cancellation)

    if trial:
        if trial == 'yes':
            queryset = queryset.filter(trial_period_days__gt=0)
        elif trial == 'no':
            queryset = queryset.filter(trial_period_days=0)

    # Order by created date (newest first)
    queryset = queryset.order_by('-created_at')

    # Render results
    html = render_to_string(
        'admin/subscriptions/partials/plan_cards.html',
        {'plans': queryset}
    )

    return JsonResponse({'html': html, 'count': queryset.count()})


@staff_member_required
def filter_customer_subscriptions(request):
    """AJAX endpoint for filtering customer subscriptions."""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    # Extract filters
    search = request.GET.get('search', '').strip()
    status = request.GET.get('status', '').strip()
    plan = request.GET.get('plan', '').strip()
    product = request.GET.get('product', '').strip()
    provider_mode = request.GET.get('provider-mode', '').strip()
    payment_provider = request.GET.get('payment-provider', '').strip()

    # Build queryset
    queryset = CustomerSubscription.objects.select_related(
        'user', 'plan', 'payment_provider_account', 'product'
    ).all()

    # Apply filters
    if search:
        queryset = queryset.filter(
            Q(user__email__icontains=search) |
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(plan__name__icontains=search)
        )

    if status:
        queryset = queryset.filter(status=status)

    if plan:
        queryset = queryset.filter(plan_id=plan)

    if product:
        queryset = queryset.filter(product_id=product)

    if provider_mode:
        queryset = queryset.filter(provider_mode=provider_mode)

    if payment_provider:
        queryset = queryset.filter(payment_provider_account_id=payment_provider)

    # Order by created date (newest first)
    queryset = queryset.order_by('-created_at')

    # Render results
    html = render_to_string(
        'admin/subscriptions/partials/subscription_cards.html',
        {'subscriptions': queryset}
    )

    return JsonResponse({'html': html, 'count': queryset.count()})
