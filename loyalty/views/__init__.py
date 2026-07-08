"""
Loyalty Program Views

Admin views for managing and viewing loyalty program data.
Customer-facing views for loyalty dashboard, rewards, and history.
"""

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from datetime import timedelta
from decimal import Decimal
import json

from loyalty.models import (
    LoyaltyMember,
    LoyaltyBalance,
    LoyaltyTransaction,
    LoyaltyRule,
    LoyaltyTier,
    LoyaltyBadge,
    LoyaltyMemberBadge,
    LoyaltyReward,
    LoyaltyRedemption,
    LoyaltySegment,
    LoyaltyCampaign,
)
from loyalty.services.redemption_engine import RedemptionEngine


@staff_member_required
def loyalty_dashboard(request):
    """
    Main loyalty program dashboard showing KPIs and analytics.
    """
    # Get date range (default: last 30 days)
    end_date = timezone.now()
    start_date = end_date - timedelta(days=30)

    # Calculate KPIs
    total_members = LoyaltyMember.objects.filter(is_active=True).count()

    # Active members (those who have earned/redeemed points in period)
    active_members = LoyaltyTransaction.objects.filter(
        created_at__gte=start_date,
        created_at__lte=end_date
    ).values('member').distinct().count()

    # Points outstanding (total available + pending across all members)
    points_stats = LoyaltyBalance.objects.aggregate(
        total_available=Sum('available_points'),
        total_pending=Sum('pending_points'),
        total_lifetime_earned=Sum('lifetime_earned'),
        total_lifetime_redeemed=Sum('lifetime_redeemed'),
    )

    points_outstanding = (points_stats['total_available'] or 0) + (points_stats['total_pending'] or 0)

    # Calculate redemption rate
    lifetime_earned = points_stats['total_lifetime_earned'] or 1  # Avoid division by zero
    lifetime_redeemed = points_stats['total_lifetime_redeemed'] or 0
    redemption_rate = round((lifetime_redeemed / lifetime_earned) * 100, 1) if lifetime_earned > 0 else 0

    # Points earned in period
    points_earned_period = LoyaltyTransaction.objects.filter(
        transaction_type__in=[LoyaltyTransaction.TYPE_EARN, LoyaltyTransaction.TYPE_BONUS],
        created_at__gte=start_date,
        created_at__lte=end_date
    ).aggregate(total=Sum('points'))['total'] or 0

    # Points redeemed in period
    points_redeemed_period = abs(LoyaltyTransaction.objects.filter(
        transaction_type=LoyaltyTransaction.TYPE_REDEEM,
        created_at__gte=start_date,
        created_at__lte=end_date
    ).aggregate(total=Sum('points'))['total'] or 0)

    # Average points per member
    avg_points_per_member = round(
        LoyaltyBalance.objects.filter(
            member__is_active=True
        ).aggregate(avg=Avg('available_points'))['avg'] or 0
    )

    # Member enrollment trend (last 30 days, grouped by day)
    enrollment_data = []
    for i in range(30):
        date = start_date + timedelta(days=i)
        next_date = date + timedelta(days=1)
        count = LoyaltyMember.objects.filter(
            enrolled_at__gte=date,
            enrolled_at__lt=next_date
        ).count()
        enrollment_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'count': count
        })

    # Points trend (last 30 days)
    points_trend = []
    for i in range(30):
        date = start_date + timedelta(days=i)
        next_date = date + timedelta(days=1)

        earned = LoyaltyTransaction.objects.filter(
            transaction_type__in=[LoyaltyTransaction.TYPE_EARN, LoyaltyTransaction.TYPE_BONUS],
            created_at__gte=date,
            created_at__lt=next_date
        ).aggregate(total=Sum('points'))['total'] or 0

        redeemed = abs(LoyaltyTransaction.objects.filter(
            transaction_type=LoyaltyTransaction.TYPE_REDEEM,
            created_at__gte=date,
            created_at__lt=next_date
        ).aggregate(total=Sum('points'))['total'] or 0)

        points_trend.append({
            'date': date.strftime('%Y-%m-%d'),
            'earned': earned,
            'redeemed': redeemed
        })

    # Tier distribution
    tier_distribution = []
    tiers = LoyaltyTier.objects.filter(is_active=True).order_by('rank')
    for tier in tiers:
        count = LoyaltyMember.objects.filter(
            current_tier=tier,
            is_active=True
        ).count()
        tier_distribution.append({
            'name': tier.name,
            'count': count,
            'color': tier.color or '#667eea'
        })

    # Members with no tier
    no_tier_count = LoyaltyMember.objects.filter(
        current_tier__isnull=True,
        is_active=True
    ).count()
    if no_tier_count > 0:
        tier_distribution.append({
            'name': 'No Tier',
            'count': no_tier_count,
            'color': '#999999'
        })

    # Top earners (in period)
    top_earners = []
    top_earner_data = LoyaltyTransaction.objects.filter(
        transaction_type__in=[LoyaltyTransaction.TYPE_EARN, LoyaltyTransaction.TYPE_BONUS],
        created_at__gte=start_date,
        created_at__lte=end_date
    ).values('member').annotate(
        total_points=Sum('points')
    ).order_by('-total_points')[:10]

    for data in top_earner_data:
        member = LoyaltyMember.objects.select_related('customer').get(id=data['member'])
        top_earners.append({
            'id': member.id,
            'name': member.customer.get_full_name() or member.customer.username,
            'points': data['total_points'],
            'tier': member.current_tier.name if member.current_tier else 'No Tier',
        })

    # Recent transactions (limited to 10)
    recent_transactions = LoyaltyTransaction.objects.select_related(
        'member__customer',
        'member__current_tier'
    ).order_by('-created_at')[:10]

    # Top 5 most redeemed rewards
    top_redeemed_rewards = LoyaltyRedemption.objects.filter(
        status__in=[LoyaltyRedemption.STATUS_CONFIRMED, LoyaltyRedemption.STATUS_FULFILLED]
    ).values('reward__name', 'reward__id').annotate(
        redemption_count=Count('id')
    ).order_by('-redemption_count')[:5]

    # Top 5 most recent members
    recent_members = LoyaltyMember.objects.select_related(
        'customer',
        'current_tier'
    ).order_by('-enrolled_at')[:5]

    # Active rules count
    active_rules_count = LoyaltyRule.objects.filter(is_active=True).count()

    # Campaign Performance Metrics
    from loyalty.models import LoyaltyCampaign, LoyaltyCampaignExecution

    active_campaigns = LoyaltyCampaign.objects.filter(
        is_active=True,
        status=LoyaltyCampaign.STATUS_ACTIVE
    ).count()

    # Campaign executions in period
    campaign_executions = LoyaltyCampaignExecution.objects.filter(
        triggered_at__gte=start_date,
        triggered_at__lte=end_date
    )

    total_executions = campaign_executions.count()
    completed_executions = campaign_executions.filter(
        status=LoyaltyCampaignExecution.STATUS_COMPLETED
    ).count()
    failed_executions = campaign_executions.filter(
        status=LoyaltyCampaignExecution.STATUS_FAILED
    ).count()

    campaign_completion_rate = 0
    if total_executions > 0:
        campaign_completion_rate = round((completed_executions / total_executions) * 100, 1)

    # Top performing campaigns
    top_campaigns = LoyaltyCampaign.objects.filter(
        is_active=True
    ).annotate(
        executions_in_period=Count(
            'executions',
            filter=Q(executions__triggered_at__gte=start_date, executions__triggered_at__lte=end_date)
        )
    ).order_by('-executions_in_period')[:5]

    context = {
        # KPIs
        'total_members': total_members,
        'active_members': active_members,
        'points_outstanding': points_outstanding,
        'redemption_rate': redemption_rate,
        'points_earned_period': points_earned_period,
        'points_redeemed_period': points_redeemed_period,
        'avg_points_per_member': avg_points_per_member,
        'active_rules_count': active_rules_count,

        # Campaign metrics
        'active_campaigns': active_campaigns,
        'total_campaign_executions': total_executions,
        'completed_campaign_executions': completed_executions,
        'failed_campaign_executions': failed_executions,
        'campaign_completion_rate': campaign_completion_rate,
        'top_campaigns': top_campaigns,

        # Charts data (JSON)
        'enrollment_data_json': json.dumps(enrollment_data),
        'points_trend_json': json.dumps(points_trend),
        'tier_distribution_json': json.dumps(tier_distribution),

        # Lists
        'top_earners': top_earners,
        'recent_transactions': recent_transactions,
        'top_redeemed_rewards': top_redeemed_rewards,
        'recent_members': recent_members,

        # Date range
        'start_date': start_date,
        'end_date': end_date,
    }

    return render(request, 'admin/loyalty/loyalty_dashboard.html', context)


# ============================================================================
# CUSTOMER-FACING VIEWS
# ============================================================================

@login_required
def customer_dashboard(request):
    """
    Customer loyalty dashboard showing points, tier progress, and recent activity.
    """
    # Get or create loyalty member for this customer
    try:
        member = LoyaltyMember.objects.select_related(
            'customer', 'current_tier', 'balance'
        ).prefetch_related('badges_earned').get(
            customer=request.user,
            is_active=True
        )
    except LoyaltyMember.DoesNotExist:
        # Auto-enroll the customer
        member = LoyaltyMember.objects.create(
            customer=request.user,
            is_active=True
        )
        messages.success(request, _("Welcome to our loyalty program! Start earning points today."))

    # Get balance
    balance = member.balance

    # Calculate tier progress
    tier_progress = 0
    next_tier = None
    points_to_next_tier = 0

    if member.current_tier:
        # Find next tier (higher rank number = higher tier requirement)
        next_tier = LoyaltyTier.objects.filter(
            is_active=True,
            rank__gt=member.current_tier.rank
        ).order_by('rank').first()

        if next_tier and next_tier.min_points_earned > 0:
            current_points = balance.lifetime_earned
            tier_progress = min(100, int((current_points / next_tier.min_points_earned) * 100))
            points_to_next_tier = max(0, next_tier.min_points_earned - current_points)
    else:
        # No current tier - show progress to first tier
        next_tier = LoyaltyTier.objects.filter(is_active=True).order_by('rank').first()
        if next_tier and next_tier.min_points_earned > 0:
            current_points = balance.lifetime_earned
            tier_progress = min(100, int((current_points / next_tier.min_points_earned) * 100))
            points_to_next_tier = max(0, next_tier.min_points_earned - current_points)

    # Recent transactions (last 10)
    recent_transactions = LoyaltyTransaction.objects.filter(
        member=member
    ).order_by('-created_at')[:10]

    # Available rewards (featured or popular)
    available_rewards = LoyaltyReward.objects.filter(
        is_active=True,
        featured=True
    ).order_by('display_order', 'points_cost')[:6]

    # Recent badges
    recent_badges = LoyaltyMemberBadge.objects.filter(
        member=member
    ).select_related('badge').order_by('-earned_at')[:4]

    # Pending redemptions
    pending_redemptions = LoyaltyRedemption.objects.filter(
        member=member,
        status__in=[LoyaltyRedemption.STATUS_PENDING, LoyaltyRedemption.STATUS_CONFIRMED]
    ).select_related('reward').order_by('-created_at')[:5]

    # Points expiring soon (within 30 days)
    expiry_cutoff = timezone.now() + timedelta(days=30)
    expiring_points_total = LoyaltyTransaction.objects.filter(
        member=member,
        transaction_type=LoyaltyTransaction.TYPE_EARN,
        status=LoyaltyTransaction.STATUS_AVAILABLE,
        expires_at__isnull=False,
        expires_at__lte=expiry_cutoff,
        expires_at__gt=timezone.now(),
    ).aggregate(total=Sum('points'))['total'] or 0

    context = {
        'member': member,
        'balance': balance,
        'tier_progress': tier_progress,
        'next_tier': next_tier,
        'points_to_next_tier': points_to_next_tier,
        'recent_transactions': recent_transactions,
        'available_rewards': available_rewards,
        'recent_badges': recent_badges,
        'pending_redemptions': pending_redemptions,
        'expiring_points_total': expiring_points_total,
    }

    return render(request, 'loyalty/customer/dashboard.html', context)


@login_required
def customer_transaction_history(request):
    """
    Paginated transaction history for the customer.
    """
    try:
        member = LoyaltyMember.objects.get(customer=request.user, is_active=True)
    except LoyaltyMember.DoesNotExist:
        messages.warning(request, _("Please join our loyalty program first."))
        return redirect('loyalty:customer_dashboard')

    # Filter by transaction type if specified
    transaction_type = request.GET.get('type', '')
    transactions = LoyaltyTransaction.objects.filter(member=member)

    if transaction_type:
        transactions = transactions.filter(transaction_type=transaction_type)

    transactions = transactions.order_by('-created_at')

    # Pagination
    paginator = Paginator(transactions, 25)  # 25 transactions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get transaction type choices for filter
    transaction_types = [
        {'value': '', 'label': _('All Transactions')},
        {'value': LoyaltyTransaction.TYPE_EARN, 'label': _('Points Earned')},
        {'value': LoyaltyTransaction.TYPE_REDEEM, 'label': _('Points Redeemed')},
        {'value': LoyaltyTransaction.TYPE_BONUS, 'label': _('Bonus Points')},
        {'value': LoyaltyTransaction.TYPE_ADJUSTMENT, 'label': _('Adjustments')},
        {'value': LoyaltyTransaction.TYPE_EXPIRE, 'label': _('Expired Points')},
    ]

    context = {
        'member': member,
        'page_obj': page_obj,
        'transaction_types': transaction_types,
        'selected_type': transaction_type,
    }

    return render(request, 'loyalty/customer/transaction_history.html', context)


@login_required
def customer_rewards_catalog(request):
    """
    Browse available rewards that can be redeemed.
    """
    try:
        member = LoyaltyMember.objects.select_related('balance', 'current_tier').get(
            customer=request.user,
            is_active=True
        )
    except LoyaltyMember.DoesNotExist:
        messages.warning(request, _("Please join our loyalty program first."))
        return redirect('loyalty:customer_dashboard')

    # Filter rewards
    reward_type = request.GET.get('type', '')
    sort_by = request.GET.get('sort', 'points')  # points, name, featured

    rewards = LoyaltyReward.objects.filter(is_active=True)

    # Type filter
    if reward_type:
        rewards = rewards.filter(reward_type=reward_type)

    # Sorting
    if sort_by == 'points':
        rewards = rewards.order_by('points_cost')
    elif sort_by == 'name':
        rewards = rewards.order_by('name')
    elif sort_by == 'featured':
        rewards = rewards.order_by('-featured', 'display_order', 'points_cost')

    # Pagination
    paginator = Paginator(rewards, 12)  # 12 rewards per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Add eligibility info to each reward
    for reward in page_obj:
        can_redeem, reason = reward.can_member_redeem(member)
        reward.can_redeem = can_redeem
        reward.cannot_redeem_reason = reason

    # Reward type choices for filter
    reward_types = [
        {'value': '', 'label': _('All Rewards')},
        {'value': LoyaltyReward.TYPE_DISCOUNT, 'label': _('Discounts')},
        {'value': LoyaltyReward.TYPE_PRODUCT, 'label': _('Free Products')},
        {'value': LoyaltyReward.TYPE_SHIPPING, 'label': _('Free Shipping')},
        {'value': LoyaltyReward.TYPE_EXPERIENCE, 'label': _('Special Experiences')},
    ]

    context = {
        'member': member,
        'page_obj': page_obj,
        'reward_types': reward_types,
        'selected_type': reward_type,
        'sort_by': sort_by,
    }

    return render(request, 'loyalty/customer/rewards_catalog.html', context)


@login_required
def customer_redeem_reward(request, reward_id):
    """
    Redeem a specific reward.
    """
    try:
        member = LoyaltyMember.objects.select_related('balance', 'current_tier').get(
            customer=request.user,
            is_active=True
        )
    except LoyaltyMember.DoesNotExist:
        messages.error(request, _("You must be a loyalty member to redeem rewards."))
        return redirect('loyalty:customer_dashboard')

    reward = get_object_or_404(LoyaltyReward, id=reward_id, is_active=True)

    # Check eligibility
    can_redeem, reason = reward.can_member_redeem(member)

    if request.method == 'POST':
        if not can_redeem:
            messages.error(request, reason)
            return redirect('loyalty:customer_rewards_catalog')

        # Process redemption
        try:
            engine = RedemptionEngine()
            redemption, success, message = engine.redeem_reward(member, reward)

            if success:
                messages.success(request, message)
                return redirect('loyalty:customer_redemption_detail', redemption_id=redemption.id)
            else:
                messages.error(request, message)
                return redirect('loyalty:customer_rewards_catalog')
        except Exception as e:
            messages.error(request, _("Failed to process redemption: {}").format(str(e)))
            return redirect('loyalty:customer_rewards_catalog')

    # GET request - show confirmation page
    context = {
        'member': member,
        'reward': reward,
        'can_redeem': can_redeem,
        'cannot_redeem_reason': reason,
    }

    return render(request, 'loyalty/customer/redeem_reward.html', context)


@login_required
def customer_redemption_detail(request, redemption_id):
    """
    View details of a redemption.
    """
    try:
        member = LoyaltyMember.objects.get(customer=request.user, is_active=True)
    except LoyaltyMember.DoesNotExist:
        messages.error(request, _("Loyalty member not found."))
        return redirect('loyalty:customer_dashboard')

    redemption = get_object_or_404(
        LoyaltyRedemption.objects.select_related('reward', 'member'),
        id=redemption_id,
        member=member
    )

    context = {
        'member': member,
        'redemption': redemption,
    }

    return render(request, 'loyalty/customer/redemption_detail.html', context)


@login_required
def customer_tier_info(request):
    """
    Display tier information and benefits.
    """
    try:
        member = LoyaltyMember.objects.select_related('current_tier', 'balance').get(
            customer=request.user,
            is_active=True
        )
    except LoyaltyMember.DoesNotExist:
        messages.warning(request, _("Please join our loyalty program first."))
        return redirect('loyalty:customer_dashboard')

    # Get all tiers
    all_tiers = LoyaltyTier.objects.filter(is_active=True).order_by('rank')

    # Calculate progress for each tier
    for tier in all_tiers:
        if tier.min_points_earned > 0:
            progress = min(100, int((member.balance.lifetime_earned / tier.min_points_earned) * 100))
            tier.progress = progress
            tier.is_achieved = member.balance.lifetime_earned >= tier.min_points_earned
        elif tier.min_spend > 0:
            progress = min(100, int((member.balance.lifetime_earned / tier.min_spend) * 100))
            tier.progress = progress
            tier.is_achieved = False
        else:
            tier.progress = 0
            tier.is_achieved = False

    context = {
        'member': member,
        'all_tiers': all_tiers,
    }

    return render(request, 'loyalty/customer/tier_info.html', context)


@login_required
def customer_badges(request):
    """
    Display all badges - earned and available to earn.
    """
    try:
        member = LoyaltyMember.objects.select_related('current_tier', 'balance').get(
            customer=request.user,
            is_active=True
        )
    except LoyaltyMember.DoesNotExist:
        messages.warning(request, _("Please join our loyalty program first."))
        return redirect('loyalty:customer_dashboard')

    # Get all earned badges for this member
    earned_badges = LoyaltyMemberBadge.objects.filter(
        member=member
    ).select_related('badge').order_by('-earned_at')

    earned_badge_ids = set(earned_badges.values_list('badge_id', flat=True))

    # Get all visible badges (for "available to earn" section)
    all_badges = LoyaltyBadge.objects.filter(
        is_active=True, is_visible=True
    ).order_by('display_order', 'name')

    available_badges = [b for b in all_badges if b.id not in earned_badge_ids]

    context = {
        'member': member,
        'earned_badges': earned_badges,
        'available_badges': available_badges,
        'earned_count': len(earned_badge_ids),
        'total_count': all_badges.count(),
    }

    return render(request, 'loyalty/customer/badges.html', context)


@staff_member_required
def filter_members(request):
    """
    AJAX endpoint for filtering loyalty members.
    Returns filtered member list as HTML with count.
    """
    from django.template.loader import render_to_string

    # Ensure this is an AJAX request
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    # Get filter parameters
    search = request.GET.get('search', '').strip()
    tier_id = request.GET.get('tier', '').strip()
    status = request.GET.get('status', '').strip()

    # Build query with proper prefetching for performance
    members = LoyaltyMember.objects.select_related(
        'customer',
        'current_tier',
        'balance'
    ).all()

    # Apply search filter
    if search:
        members = members.filter(
            Q(customer__first_name__icontains=search) |
            Q(customer__last_name__icontains=search) |
            Q(customer__email__icontains=search) |
            Q(customer__username__icontains=search)
        )

    # Apply tier filter
    if tier_id:
        try:
            members = members.filter(current_tier_id=int(tier_id))
        except (ValueError, TypeError):
            pass

    # Apply status filter
    if status == 'active':
        members = members.filter(is_active=True)
    elif status == 'inactive':
        members = members.filter(is_active=False)

    # Order by most recent first
    members = members.order_by('-enrolled_at')

    # Render results as HTML
    html = render_to_string('admin/loyalty/partials/member_cards.html', {
        'members': members,
    })

    return JsonResponse({
        'html': html,
        'count': members.count()
    })


@staff_member_required
def filter_transactions(request):
    """
    AJAX endpoint for filtering loyalty transactions.
    Returns filtered transaction list as HTML with count.
    """
    from django.template.loader import render_to_string

    # Ensure this is an AJAX request
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    # Get filter parameters
    search = request.GET.get('search', '').strip()
    transaction_type = request.GET.get('type', '').strip()
    status = request.GET.get('status', '').strip()
    member_id = request.GET.get('member', '').strip()

    # Build query with proper prefetching for performance
    transactions = LoyaltyTransaction.objects.select_related(
        'member__customer',
        'member__current_tier'
    ).all()

    # Apply search filter
    if search:
        transactions = transactions.filter(
            Q(member__customer__first_name__icontains=search) |
            Q(member__customer__last_name__icontains=search) |
            Q(member__customer__email__icontains=search) |
            Q(member__customer__username__icontains=search) |
            Q(description__icontains=search) |
            Q(reason__icontains=search)
        )

    # Apply type filter
    if transaction_type:
        transactions = transactions.filter(transaction_type=transaction_type)

    # Apply status filter
    if status:
        transactions = transactions.filter(status=status)

    # Apply member filter
    if member_id:
        try:
            transactions = transactions.filter(member_id=int(member_id))
        except (ValueError, TypeError):
            pass

    # Order by most recent first
    transactions = transactions.order_by('-created_at')

    # Render results as HTML
    html = render_to_string('admin/loyalty/partials/transaction_cards.html', {
        'transactions': transactions,
    })

    return JsonResponse({
        'html': html,
        'count': transactions.count()
    })


@staff_member_required
def filter_rewards(request):
    """
    AJAX endpoint for filtering loyalty rewards.
    Returns filtered reward list as HTML with count.
    """
    from django.template.loader import render_to_string
    from loyalty.models import LoyaltyReward
    from datetime import date

    # Ensure this is an AJAX request
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    # Get filter parameters
    search = request.GET.get('search', '').strip()
    reward_type = request.GET.get('type', '').strip()
    status = request.GET.get('status', '').strip()
    availability = request.GET.get('availability', '').strip()
    featured = request.GET.get('featured', '').strip()

    # Build query with proper prefetching for performance
    rewards = LoyaltyReward.objects.select_related(
        'product',
        'required_tier'
    ).all()

    # Apply search filter
    if search:
        rewards = rewards.filter(
            Q(name__icontains=search) |
            Q(slug__icontains=search) |
            Q(description__icontains=search)
        )

    # Apply type filter
    if reward_type:
        rewards = rewards.filter(reward_type=reward_type)

    # Apply status filter
    if status == 'active':
        rewards = rewards.filter(is_active=True)
    elif status == 'inactive':
        rewards = rewards.filter(is_active=False)

    # Apply availability filter
    today = date.today()
    if availability == 'available':
        # Active, within date range, and has quantity remaining
        rewards = rewards.filter(is_active=True)
        rewards = rewards.filter(
            Q(start_date__isnull=True) | Q(start_date__lte=today)
        )
        rewards = rewards.filter(
            Q(end_date__isnull=True) | Q(end_date__gte=today)
        )
        # Either unlimited or has quantity remaining
        rewards = rewards.filter(
            Q(quantity_total__isnull=True) | Q(quantity_remaining__gt=0)
        )
    elif availability == 'unavailable':
        # Not active OR outside date range OR no quantity
        rewards = rewards.filter(
            Q(is_active=False) |
            Q(start_date__gt=today) |
            Q(end_date__lt=today) |
            (Q(quantity_total__isnull=False) & Q(quantity_remaining=0))
        )
    elif availability == 'out_of_stock':
        # Has quantity limit and is out of stock
        rewards = rewards.filter(quantity_total__isnull=False, quantity_remaining=0)

    # Apply featured filter
    if featured == 'yes':
        rewards = rewards.filter(featured=True)
    elif featured == 'no':
        rewards = rewards.filter(featured=False)

    # Order by display order, then name
    rewards = rewards.order_by('display_order', 'name')

    # Render results as HTML
    html = render_to_string('admin/loyalty/partials/reward_cards.html', {
        'rewards': rewards,
    })

    return JsonResponse({
        'html': html,
        'count': rewards.count()
    })


def filter_redemptions(request):
    """
    AJAX endpoint for filtering loyalty redemptions.
    Returns filtered redemption list as HTML with count.
    """
    from django.template.loader import render_to_string
    from loyalty.models import LoyaltyRedemption
    from datetime import date, timedelta

    # Ensure this is an AJAX request
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    # Get filter parameters
    search = request.GET.get('search', '').strip()
    status = request.GET.get('status', '').strip()
    expiry = request.GET.get('expiry', '').strip()
    date_from = request.GET.get('date_from', '').strip()
    date_to = request.GET.get('date_to', '').strip()

    # Build query with proper prefetching for performance
    redemptions = LoyaltyRedemption.objects.select_related(
        'member',
        'member__customer',
        'reward'
    ).all()

    # Apply search filter
    if search:
        redemptions = redemptions.filter(
            Q(redemption_code__icontains=search) |
            Q(member__customer__first_name__icontains=search) |
            Q(member__customer__last_name__icontains=search) |
            Q(member__customer__username__icontains=search) |
            Q(member__email__icontains=search) |
            Q(reward__name__icontains=search)
        )

    # Apply status filter
    if status:
        redemptions = redemptions.filter(status=status)

    # Apply expiry filter
    today = date.today()
    if expiry == 'active':
        # Not expired (expires_at is null or in future)
        redemptions = redemptions.filter(
            Q(expires_at__isnull=True) | Q(expires_at__gte=today)
        ).exclude(status='expired')
    elif expiry == 'expired':
        # Expired (expires_at is in past or status is expired)
        redemptions = redemptions.filter(
            Q(expires_at__lt=today) | Q(status='expired')
        )
    elif expiry == 'expiring-soon':
        # Expiring within 7 days
        seven_days = today + timedelta(days=7)
        redemptions = redemptions.filter(
            expires_at__gte=today,
            expires_at__lte=seven_days,
            status='pending'
        )

    # Apply date range filters
    if date_from:
        try:
            from datetime import datetime
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
            redemptions = redemptions.filter(created_at__gte=date_from_obj)
        except ValueError:
            pass  # Invalid date format, skip filter

    if date_to:
        try:
            from datetime import datetime
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
            # Include the entire day by adding 1 day
            date_to_obj = date_to_obj + timedelta(days=1)
            redemptions = redemptions.filter(created_at__lt=date_to_obj)
        except ValueError:
            pass  # Invalid date format, skip filter

    # Order by most recent first
    redemptions = redemptions.order_by('-created_at')

    # Render results as HTML
    html = render_to_string('admin/loyalty/partials/redemption_cards.html', {
        'redemptions': redemptions,
    })

    return JsonResponse({
        'html': html,
        'count': redemptions.count()
    })


def filter_tiers(request):
    """
    AJAX endpoint for filtering loyalty tiers.
    Returns filtered tier list as HTML with count.
    """
    from django.template.loader import render_to_string
    from loyalty.models import LoyaltyTier

    # Ensure this is an AJAX request
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    # Get filter parameters
    search = request.GET.get('search', '').strip()
    status = request.GET.get('status', '').strip()
    order = request.GET.get('order', 'rank').strip()

    # Build query
    tiers = LoyaltyTier.objects.all()

    # Apply search filter
    if search:
        tiers = tiers.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )

    # Apply status filter
    if status == 'active':
        tiers = tiers.filter(is_active=True)
    elif status == 'inactive':
        tiers = tiers.filter(is_active=False)

    # Apply ordering
    if order:
        tiers = tiers.order_by(order)
    else:
        tiers = tiers.order_by('rank')

    # Render results as HTML
    html = render_to_string('admin/loyalty/partials/tier_cards.html', {
        'tiers': tiers,
    })

    return JsonResponse({
        'html': html,
        'count': tiers.count()
    })


def filter_badges(request):
    """
    AJAX endpoint for filtering loyalty badges.
    Returns filtered badge list as HTML with count.
    """
    from django.template.loader import render_to_string
    from loyalty.models import LoyaltyBadge

    # Ensure this is an AJAX request
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    # Get filter parameters
    search = request.GET.get('search', '').strip()
    status = request.GET.get('status', '').strip()
    visibility = request.GET.get('visibility', '').strip()
    badge_type = request.GET.get('type', '').strip()
    order = request.GET.get('order', 'display_order').strip()

    # Build query
    badges = LoyaltyBadge.objects.all()

    # Apply search filter
    if search:
        badges = badges.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search) |
            Q(criteria_type__icontains=search)
        )

    # Apply status filter
    if status == 'active':
        badges = badges.filter(is_active=True)
    elif status == 'inactive':
        badges = badges.filter(is_active=False)

    # Apply visibility filter
    if visibility == 'visible':
        badges = badges.filter(is_visible=True)
    elif visibility == 'hidden':
        badges = badges.filter(is_visible=False)

    # Apply type filter
    if badge_type:
        badges = badges.filter(criteria_type=badge_type)

    # Apply ordering
    if order:
        badges = badges.order_by(order)
    else:
        badges = badges.order_by('display_order', 'name')

    # Render results as HTML
    html = render_to_string('admin/loyalty/partials/badge_cards.html', {
        'badges': badges,
    })

    return JsonResponse({
        'html': html,
        'count': badges.count()
    })


@staff_member_required
def filter_rules(request):
    """
    AJAX endpoint for filtering loyalty rules.
    Returns filtered rule list as HTML with count.
    """
    from django.template.loader import render_to_string

    # Ensure this is an AJAX request
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    # Get filter parameters
    search = request.GET.get('search', '').strip()
    rule_type = request.GET.get('rule_type', '').strip()
    status = request.GET.get('status', '').strip()
    exclusive = request.GET.get('exclusive', '').strip()
    sort = request.GET.get('sort', '-created_at').strip()

    # Build query
    rules = LoyaltyRule.objects.all()

    # Apply search filter
    if search:
        rules = rules.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )

    # Apply rule type filter
    if rule_type:
        rules = rules.filter(rule_type=rule_type)

    # Apply status filter
    if status == 'active':
        rules = rules.filter(is_active=True)
    elif status == 'inactive':
        rules = rules.filter(is_active=False)

    # Apply exclusive filter
    if exclusive == 'yes':
        rules = rules.filter(is_exclusive=True)
    elif exclusive == 'no':
        rules = rules.filter(is_exclusive=False)

    # Apply sorting
    if sort:
        rules = rules.order_by(sort)
    else:
        rules = rules.order_by('-created_at')

    # Render results as HTML
    html = render_to_string('admin/loyalty/partials/rule_cards.html', {
        'rules': rules,
    })

    return JsonResponse({
        'html': html,
        'count': rules.count()
    })


@staff_member_required
def toggle_rule_status(request, rule_id):
    """
    AJAX endpoint for activating or deactivating a rule.
    Determines action from the URL path.
    """
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        rule = LoyaltyRule.objects.get(id=rule_id)

        # Determine action from URL path
        path = request.path
        if 'activate' in path:
            rule.is_active = True
            action_msg = _('Rule activated successfully.')
        elif 'deactivate' in path:
            rule.is_active = False
            action_msg = _('Rule deactivated successfully.')
        else:
            # Fallback to toggle
            rule.is_active = not rule.is_active
            action_msg = _('Rule status updated successfully.')

        rule.save()

        return JsonResponse({
            'success': True,
            'is_active': rule.is_active,
            'message': action_msg
        })
    except LoyaltyRule.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': _('Rule not found.')
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@staff_member_required
def filter_segments(request):
    """
    AJAX endpoint for filtering loyalty segments.
    Returns filtered segment list as HTML with count.
    """
    from django.template.loader import render_to_string

    # Ensure this is an AJAX request
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    # Get filter parameters
    search = request.GET.get('search', '').strip()
    status = request.GET.get('status', '').strip()
    criteria_type = request.GET.get('type', '').strip()
    order = request.GET.get('order', '-created_at').strip()

    # Build query
    segments = LoyaltySegment.objects.all()

    # Apply search filter
    if search:
        segments = segments.filter(
            Q(name__icontains=search) |
            Q(slug__icontains=search) |
            Q(description__icontains=search)
        )

    # Apply status filter
    if status == 'active':
        segments = segments.filter(is_active=True)
    elif status == 'inactive':
        segments = segments.filter(is_active=False)

    # Apply criteria type filter
    if criteria_type:
        segments = segments.filter(criteria_type=criteria_type)

    # Apply ordering
    if order:
        segments = segments.order_by(order)
    else:
        segments = segments.order_by('-created_at')

    # Render results as HTML
    html = render_to_string('admin/loyalty/partials/segment_cards.html', {
        'segments': segments,
    })

    return JsonResponse({
        'html': html,
        'count': segments.count()
    })


@staff_member_required
def refresh_segment(request, segment_id):
    """
    AJAX endpoint for refreshing a segment's membership.
    Queues an async task to recalculate segment members.
    """
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        segment = LoyaltySegment.objects.get(id=segment_id)

        if segment.criteria_type == 'manual':
            return JsonResponse({
                'success': False,
                'error': _('Manual segments cannot be automatically refreshed.')
            }, status=400)

        # Queue async refresh task
        from loyalty.tasks import refresh_single_segment
        refresh_single_segment.delay(segment.id)

        return JsonResponse({
            'success': True,
            'message': _('Segment refresh has been queued.')
        })
    except LoyaltySegment.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': _('Segment not found.')
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@staff_member_required
def filter_campaigns(request):
    """
    AJAX endpoint for filtering loyalty campaigns.
    Returns filtered campaign list as HTML with count.
    """
    from django.template.loader import render_to_string

    # Ensure this is an AJAX request
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    # Get filter parameters
    search = request.GET.get('search', '').strip()
    status = request.GET.get('status', '').strip()
    campaign_type = request.GET.get('type', '').strip()
    trigger_event = request.GET.get('trigger', '').strip()
    is_journey = request.GET.get('journey', '').strip()
    order = request.GET.get('order', '-created_at').strip()

    # Build query with prefetching for performance
    campaigns = LoyaltyCampaign.objects.select_related('target_segment').all()

    # Apply search filter
    if search:
        campaigns = campaigns.filter(
            Q(name__icontains=search) |
            Q(slug__icontains=search) |
            Q(description__icontains=search)
        )

    # Apply status filter
    if status:
        campaigns = campaigns.filter(status=status)

    # Apply campaign type filter
    if campaign_type:
        campaigns = campaigns.filter(campaign_type=campaign_type)

    # Apply trigger event filter
    if trigger_event:
        campaigns = campaigns.filter(trigger_event=trigger_event)

    # Apply journey filter
    if is_journey == 'yes':
        campaigns = campaigns.filter(is_journey=True)
    elif is_journey == 'no':
        campaigns = campaigns.filter(is_journey=False)

    # Apply ordering
    if order:
        campaigns = campaigns.order_by(order)
    else:
        campaigns = campaigns.order_by('-created_at')

    # Render results as HTML
    html = render_to_string('admin/loyalty/partials/campaign_cards.html', {
        'campaigns': campaigns,
    })

    return JsonResponse({
        'html': html,
        'count': campaigns.count()
    })


@staff_member_required
def toggle_campaign_status(request, campaign_id):
    """
    AJAX endpoint for activating or pausing a campaign.
    Determines action from the URL path.
    """
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        campaign = LoyaltyCampaign.objects.get(id=campaign_id)

        # Determine action from URL path
        path = request.path
        if 'activate' in path:
            if campaign.status in ['draft', 'paused']:
                campaign.status = 'active'
                campaign.is_active = True
                campaign.save()
                action_msg = _('Campaign activated successfully.')
            else:
                return JsonResponse({
                    'success': False,
                    'error': _('Campaign cannot be activated from its current status.')
                }, status=400)
        elif 'pause' in path:
            if campaign.status == 'active':
                campaign.status = 'paused'
                campaign.save()
                action_msg = _('Campaign paused successfully.')
            else:
                return JsonResponse({
                    'success': False,
                    'error': _('Only active campaigns can be paused.')
                }, status=400)
        else:
            return JsonResponse({
                'success': False,
                'error': _('Invalid action.')
            }, status=400)

        return JsonResponse({
            'success': True,
            'status': campaign.status,
            'is_active': campaign.is_active,
            'message': action_msg
        })
    except LoyaltyCampaign.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': _('Campaign not found.')
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


# ============================================================================
# CAMPAIGN WIZARD
# ============================================================================

@staff_member_required
def campaign_wizard(request):
    """
    Multi-step wizard for creating loyalty campaigns.
    Handles both GET (display form) and POST (save campaign).
    """
    from django.utils.text import slugify
    from loyalty.models import LoyaltyTier

    # Get available tiers and segments for the form
    tiers = LoyaltyTier.objects.filter(is_active=True).order_by('rank')
    segments = LoyaltySegment.objects.filter(is_active=True).order_by('name')

    # Campaign type choices
    campaign_types = [
        {
            'value': 'trigger_based',
            'name': _('Trigger-Based'),
            'description': _('Automatically activates when specific customer actions occur'),
            'icon': 'bolt'
        },
        {
            'value': 'scheduled',
            'name': _('Scheduled'),
            'description': _('Runs at specific times or on a recurring schedule'),
            'icon': 'calendar'
        },
        {
            'value': 'manual',
            'name': _('Manual'),
            'description': _('Manually triggered by administrators'),
            'icon': 'hand-pointer'
        },
        {
            'value': 'behavioral',
            'name': _('Behavioral'),
            'description': _('Targets customers based on browsing and purchase patterns'),
            'icon': 'chart-line'
        },
    ]

    # Trigger events grouped by category
    trigger_events = {
        'purchase': [
            {'value': 'order_placed', 'name': _('Order Placed'), 'icon': 'shopping-cart', 'description': _('When a customer completes a purchase')},
            {'value': 'first_purchase', 'name': _('First Purchase'), 'icon': 'star', 'description': _('Customer makes their first purchase')},
            {'value': 'nth_purchase', 'name': _('Nth Purchase'), 'icon': 'layer-group', 'description': _('Customer reaches a purchase milestone')},
        ],
        'account': [
            {'value': 'customer_signup', 'name': _('Customer Signup'), 'icon': 'user-plus', 'description': _('New customer creates an account')},
            {'value': 'birthday', 'name': _('Birthday'), 'icon': 'birthday-cake', 'description': _('Customer\'s birthday')},
            {'value': 'anniversary', 'name': _('Anniversary'), 'icon': 'gift', 'description': _('Account creation anniversary')},
        ],
        'tier': [
            {'value': 'tier_promoted', 'name': _('Tier Promoted'), 'icon': 'arrow-up', 'description': _('Customer moves up a tier')},
            {'value': 'tier_demoted', 'name': _('Tier Demoted'), 'icon': 'arrow-down', 'description': _('Customer moves down a tier')},
        ],
        'engagement': [
            {'value': 'cart_abandoned', 'name': _('Cart Abandoned'), 'icon': 'shopping-basket', 'description': _('Customer abandons their cart')},
            {'value': 'no_purchase_90d', 'name': _('Inactive 90 Days'), 'icon': 'clock', 'description': _('No purchase in 90 days')},
            {'value': 'points_expiring', 'name': _('Points Expiring'), 'icon': 'hourglass-end', 'description': _('Points about to expire')},
            {'value': 'review_submitted', 'name': _('Review Submitted'), 'icon': 'comment', 'description': _('Customer submits a review')},
            {'value': 'referral_converted', 'name': _('Referral Converted'), 'icon': 'users', 'description': _('A referred customer makes a purchase')},
        ],
    }

    # Action types
    action_types = [
        {'value': 'award_points', 'name': _('Award Points'), 'icon': 'coins', 'description': _('Give a fixed number of points')},
        {'value': 'bonus_points', 'name': _('Bonus Points'), 'icon': 'percentage', 'description': _('Multiply points earned')},
        {'value': 'send_email', 'name': _('Send Email'), 'icon': 'envelope', 'description': _('Send a notification email')},
        {'value': 'upgrade_tier', 'name': _('Upgrade Tier'), 'icon': 'arrow-up', 'description': _('Move customer to higher tier')},
        {'value': 'grant_badge', 'name': _('Grant Badge'), 'icon': 'medal', 'description': _('Award an achievement badge')},
    ]

    if request.method == 'POST':
        try:
            # Parse form data
            data = request.POST

            # Basic validation
            name = data.get('name', '').strip()
            if not name:
                return JsonResponse({'success': False, 'error': _('Campaign name is required.')}, status=400)

            campaign_type = data.get('campaign_type', '').strip()
            if not campaign_type:
                return JsonResponse({'success': False, 'error': _('Campaign type is required.')}, status=400)

            # Generate slug
            slug = slugify(name)
            base_slug = slug
            counter = 1
            while LoyaltyCampaign.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            # Build actions JSON
            actions = []
            action_types_list = request.POST.getlist('action_type[]')
            action_values = request.POST.getlist('action_value[]')

            for i, action_type in enumerate(action_types_list):
                if action_type:
                    action = {'type': action_type}
                    if i < len(action_values) and action_values[i]:
                        action['value'] = action_values[i]
                    actions.append(action)

            # Build trigger conditions JSON if applicable
            trigger_conditions = {}
            if campaign_type == 'trigger_based':
                trigger_event = data.get('trigger_event', '')
                if trigger_event == 'nth_purchase':
                    trigger_conditions['purchase_count'] = int(data.get('trigger_nth_value', 5))
                elif trigger_event == 'points_expiring':
                    trigger_conditions['days_before'] = int(data.get('trigger_expiry_days', 7))

            # Build schedule config if applicable
            schedule_config = {}
            if campaign_type == 'scheduled':
                schedule_type = data.get('schedule_type', 'one_time')
                schedule_config['type'] = schedule_type
                if schedule_type == 'recurring':
                    schedule_config['frequency'] = data.get('schedule_frequency', 'weekly')
                    schedule_config['day'] = data.get('schedule_day', 'monday')
                    schedule_config['time'] = data.get('schedule_time', '09:00')

            # Get target tiers
            target_tiers = []
            if not data.get('target_all_members'):
                target_tiers = request.POST.getlist('target_tiers[]')

            # Create the campaign
            campaign = LoyaltyCampaign(
                name=name,
                slug=slug,
                description=data.get('description', ''),
                campaign_type=campaign_type,
                trigger_event=data.get('trigger_event', '') if campaign_type == 'trigger_based' else '',
                trigger_conditions=trigger_conditions if trigger_conditions else None,
                actions=actions if actions else None,
                schedule_type=data.get('schedule_type', 'one_time') if campaign_type == 'scheduled' else 'one_time',
                schedule_config=schedule_config if schedule_config else None,
                target_all_members=bool(data.get('target_all_members')),
                max_triggers_per_member=int(data.get('max_triggers', 0)) or None,
                cooldown_days=int(data.get('cooldown_days', 0)) or None,
                status='draft',
                is_active=False,
            )

            # Set optional relations
            if data.get('target_segment'):
                try:
                    campaign.target_segment_id = int(data.get('target_segment'))
                except (ValueError, TypeError):
                    pass

            # Parse and set dates
            if data.get('start_date'):
                from datetime import datetime
                try:
                    campaign.start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d').date()
                except ValueError:
                    pass

            if data.get('end_date'):
                from datetime import datetime
                try:
                    campaign.end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d').date()
                except ValueError:
                    pass

            campaign.save()

            # Set target tiers (M2M relationship)
            if target_tiers:
                campaign.target_tiers.set(target_tiers)

            messages.success(request, _('Campaign "%(name)s" created successfully.') % {'name': name})

            return JsonResponse({
                'success': True,
                'message': _('Campaign created successfully.'),
                'redirect_url': f'/admin/loyalty/loyaltycampaign/{campaign.id}/change/'
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

    # GET request - render the wizard
    context = {
        'title': _('Create Campaign'),
        'campaign_types': campaign_types,
        'trigger_events': trigger_events,
        'action_types': action_types,
        'tiers': tiers,
        'segments': segments,
    }

    return render(request, 'admin/loyalty/loyaltycampaign/wizard.html', context)
