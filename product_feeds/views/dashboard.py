"""
Product Feeds Dashboard View.

Provides an overview of feed provider accounts, sync status, and actions needed.
"""

from datetime import timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.sites.models import Site
from django.db.models import Q, Sum
from django.shortcuts import render
from django.utils import timezone
from django.utils.translation import gettext as _

from product_feeds.models import FeedProviderAccount, FeedSyncLog


@staff_member_required
def product_feeds_dashboard(request):
    """
    Dashboard view for product feeds management.

    Shows:
    - KPIs (total accounts, active feeds, products synced, errors)
    - Accounts needing attention (errors, never synced)
    - Recent sync activity
    - Quick actions
    """
    site = Site.objects.get(pk=1)
    now = timezone.now()

    # Get all accounts for this site
    accounts = FeedProviderAccount.objects.filter(site=site).select_related("component")

    # KPI Statistics
    total_accounts = accounts.count()
    active_accounts = accounts.filter(is_active=True).count()
    accounts_with_errors = accounts.filter(sync_status="error").count()

    # Total products in all active feeds
    total_products = (
        accounts.filter(is_active=True).aggregate(total=Sum("products_in_feed"))["total"] or 0
    )

    # Accounts syncing right now
    syncing_accounts = accounts.filter(sync_status="syncing").count()

    # Accounts that have never synced
    never_synced = accounts.filter(last_sync_at__isnull=True, is_active=True).count()

    # Accounts due for sync (next_sync_at in the past)
    due_for_sync = accounts.filter(is_active=True, next_sync_at__lt=now).count()

    # Recent sync logs (last 10)
    recent_syncs = FeedSyncLog.objects.select_related("account", "account__component").order_by(
        "-started_at"
    )[:10]

    # Accounts needing attention (errors or never synced)
    attention_needed = (
        accounts.filter(Q(sync_status="error") | Q(last_sync_at__isnull=True, is_active=True))
        .select_related("component")
        .order_by("-last_error_at", "-created_at")[:5]
    )

    # Sync statistics for the last 24 hours
    last_24h = now - timedelta(hours=24)
    syncs_24h = FeedSyncLog.objects.filter(started_at__gte=last_24h)
    successful_syncs_24h = syncs_24h.filter(status="success").count()
    failed_syncs_24h = syncs_24h.filter(status="failed").count()

    # Products synced in last 24 hours
    products_synced_24h = (
        syncs_24h.filter(status="success").aggregate(total=Sum("products_synced"))["total"] or 0
    )

    context = {
        "title": _("Product Feeds Dashboard"),
        # Main KPIs
        "total_accounts": total_accounts,
        "active_accounts": active_accounts,
        "total_products": total_products,
        "accounts_with_errors": accounts_with_errors,
        # Secondary stats
        "syncing_accounts": syncing_accounts,
        "never_synced": never_synced,
        "due_for_sync": due_for_sync,
        # 24h stats
        "successful_syncs_24h": successful_syncs_24h,
        "failed_syncs_24h": failed_syncs_24h,
        "products_synced_24h": products_synced_24h,
        # Lists
        "recent_syncs": recent_syncs,
        "attention_needed": attention_needed,
        # For admin breadcrumbs
        "has_permission": True,
    }

    return render(request, "admin/product_feeds/product_feeds_dashboard.html", context)
