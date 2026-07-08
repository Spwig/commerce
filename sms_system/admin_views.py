"""
Admin AJAX views for SMS System management.
"""
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.db.models import Q

from .models import SMSOutbox


@staff_member_required
@require_GET
def filter_sms_outbox(request):
    """
    AJAX filter endpoint for SMS Outbox entries.
    Returns rendered HTML for message cards.
    """
    # Verify AJAX request
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    queryset = SMSOutbox.objects.select_related('account', 'template').all()

    # Search filter (phone, message, provider_message_id)
    search = request.GET.get('search', '').strip()
    if search:
        queryset = queryset.filter(
            Q(phone__icontains=search) |
            Q(message__icontains=search) |
            Q(provider_message_id__icontains=search)
        )

    # Status filter
    status = request.GET.get('status', '').strip()
    if status:
        queryset = queryset.filter(status=status)

    # Message type filter
    message_type = request.GET.get('message_type', '').strip()
    if message_type:
        queryset = queryset.filter(message_type=message_type)

    # Get total count before limiting
    total_count = queryset.count()

    # Order by most recent first, limit to 100 for performance
    items = queryset.order_by('-created_at')[:100]

    html = render_to_string(
        'admin/sms_system/partials/smsoutbox_cards.html',
        {'items': items},
        request=request
    )

    return JsonResponse({
        'html': html,
        'count': total_count,
    })
