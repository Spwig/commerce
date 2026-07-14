"""
Payment Providers Admin AJAX Views.
Provides AJAX filter endpoints for admin change list pages.
"""

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET

from .models import PaymentTransaction, PaymentWebhook


@staff_member_required
@require_GET
def filter_transactions(request):
    """AJAX filter endpoint for PaymentTransaction entries."""
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    queryset = PaymentTransaction.objects.select_related("provider_account", "order").all()

    # Search filter
    search = request.GET.get("search", "").strip()
    if search:
        queryset = queryset.filter(
            Q(transaction_id__icontains=search) | Q(provider_transaction_id__icontains=search)
        )

    # Status filter
    status = request.GET.get("status", "").strip()
    if status:
        queryset = queryset.filter(status=status)

    # Transaction type filter
    txn_type = request.GET.get("type", "").strip()
    if txn_type:
        queryset = queryset.filter(transaction_type=txn_type)

    # Provider account filter
    provider = request.GET.get("provider", "").strip()
    if provider:
        queryset = queryset.filter(provider_account_id=provider)

    total_count = queryset.count()
    transactions = queryset.order_by("-created_at")[:100]

    html = render_to_string(
        "admin/payment_providers/partials/transaction_cards.html",
        {"transactions": transactions},
        request=request,
    )

    return JsonResponse(
        {
            "html": html,
            "count": total_count,
        }
    )


@staff_member_required
@require_GET
def filter_webhooks(request):
    """AJAX filter endpoint for PaymentWebhook entries."""
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    queryset = PaymentWebhook.objects.select_related("provider_account").all()

    # Search filter
    search = request.GET.get("search", "").strip()
    if search:
        queryset = queryset.filter(Q(event_id__icontains=search) | Q(event_type__icontains=search))

    # Provider slug filter
    provider_slug = request.GET.get("provider_slug", "").strip()
    if provider_slug:
        queryset = queryset.filter(provider_slug=provider_slug)

    # Processed filter
    processed = request.GET.get("processed", "").strip()
    if processed == "true":
        queryset = queryset.filter(processed=True)
    elif processed == "false":
        queryset = queryset.filter(processed=False)

    # Signature verified filter
    verified = request.GET.get("verified", "").strip()
    if verified == "true":
        queryset = queryset.filter(signature_verified=True)
    elif verified == "false":
        queryset = queryset.filter(signature_verified=False)

    total_count = queryset.count()
    webhooks = queryset.order_by("-created_at")[:100]

    html = render_to_string(
        "admin/payment_providers/partials/webhook_cards.html",
        {"webhooks": webhooks},
        request=request,
    )

    return JsonResponse(
        {
            "html": html,
            "count": total_count,
        }
    )
