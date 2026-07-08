"""
Badge counts API endpoint for AJAX sidebar badge refresh.
"""
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.core.cache import cache

from core.context_processors import _compute_badges, BADGE_CACHE_KEY, BADGE_CACHE_TTL

# Map badge keys to the staff_roles permission category required to see them
BADGE_PERMISSION_MAP = {
    'orders_new': 'orders',
    'carts_abandoned': 'orders',
    'shipments_pending': 'orders',
    'returns_pending': 'orders',
    'reviews_pending': 'catalog',
    'low_stock': 'catalog',
    'messages_unread': 'customers',
    'forms_submitted': 'settings',
    'emails_failed': 'settings',
    'payments_failed': 'payments',
    'feed_errors': 'marketing',
    'design_updates': 'settings',
    'component_updates': 'system',
    'platform_update': 'system',
    'hotfix_available': 'system',
    'backup_status': 'system',
    'bookings_pending': 'orders',
    'subscriptions_past_due': 'orders',
    'loyalty_redemptions_pending': 'marketing',
    'affiliate_payouts_pending': 'marketing',
    'sms_failed': 'settings',
    'translations_failed': 'settings',
    'blog_drafts': 'marketing',
}


def _filter_badges_for_user(badges, user):
    """Filter badge dict to only include keys the user has permission to see."""
    if user.is_superuser:
        return badges

    from staff_roles.services import has_category_access
    filtered = {}
    for key, value in badges.items():
        category = BADGE_PERMISSION_MAP.get(key)
        if category is None or has_category_access(user, category):
            filtered[key] = value
    return filtered


@require_GET
@login_required
def get_badge_counts(request):
    """Return current badge counts as JSON for AJAX polling."""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Forbidden'}, status=403)

    cached = cache.get(BADGE_CACHE_KEY)
    if cached is not None:
        return JsonResponse({'badges': _filter_badges_for_user(cached, request.user)})

    badges = _compute_badges()
    cache.set(BADGE_CACHE_KEY, badges, BADGE_CACHE_TTL)
    return JsonResponse({'badges': _filter_badges_for_user(badges, request.user)})
