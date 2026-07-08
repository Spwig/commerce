"""
Loyalty Analytics Views

Provides comprehensive analytics and reporting for the loyalty program including:
- Campaign performance metrics
- Member engagement statistics
- Points economy health
- Tier distribution and progression
- Segment performance
"""

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Sum, Count, Avg, Q, F
from django.db.models.functions import TruncDate, TruncMonth
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from datetime import timedelta
from decimal import Decimal
import csv

from loyalty.models import (
    LoyaltyMember,
    LoyaltyBalance,
    LoyaltyTransaction,
    LoyaltyCampaign,
    LoyaltyCampaignExecution,
    LoyaltyTier,
    LoyaltySegment,
    LoyaltyRedemption,
)


@staff_member_required
def analytics_dashboard(request):
    """
    Main analytics dashboard showing overview of loyalty program health
    """
    # Date range filter
    days = int(request.GET.get('days', 30))
    start_date = timezone.now() - timedelta(days=days)

    # Program Overview
    overview = get_program_overview()

    # Campaign Performance
    campaign_stats = get_campaign_performance(start_date)

    # Member Engagement
    engagement_stats = get_member_engagement(start_date)

    # Points Economy
    points_stats = get_points_economy(start_date)

    # Tier Distribution
    tier_stats = get_tier_distribution()

    context = {
        'overview': overview,
        'campaign_stats': campaign_stats,
        'engagement_stats': engagement_stats,
        'points_stats': points_stats,
        'tier_stats': tier_stats,
        'date_range_days': days,
        'start_date': start_date,
    }

    return render(request, 'admin/loyalty/analytics_dashboard.html', context)


@staff_member_required
def campaign_analytics(request, campaign_id):
    """
    Detailed analytics for a specific campaign
    """
    from django.shortcuts import get_object_or_404

    campaign = get_object_or_404(LoyaltyCampaign, pk=campaign_id)

    # Execution statistics
    executions = LoyaltyCampaignExecution.objects.filter(campaign=campaign)

    stats = {
        'total_executions': executions.count(),
        'completed': executions.filter(status=LoyaltyCampaignExecution.STATUS_COMPLETED).count(),
        'failed': executions.filter(status=LoyaltyCampaignExecution.STATUS_FAILED).count(),
        'in_progress': executions.filter(status=LoyaltyCampaignExecution.STATUS_PROCESSING).count(),
        'total_points_awarded': executions.aggregate(total=Sum('points_awarded'))['total'] or 0,
        'total_emails_sent': sum(len(e.emails_sent) for e in executions),
        'total_rewards_issued': sum(len(e.rewards_issued) for e in executions),
    }

    # Completion rate
    if stats['total_executions'] > 0:
        stats['completion_rate'] = (stats['completed'] / stats['total_executions']) * 100
    else:
        stats['completion_rate'] = 0

    # Journey analytics (if journey campaign)
    journey_stats = None
    if campaign.is_journey:
        journey_stats = analyze_journey_performance(campaign)

    # Daily execution trend
    daily_trend = executions.annotate(
        date=TruncDate('triggered_at')
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')

    context = {
        'campaign': campaign,
        'stats': stats,
        'journey_stats': journey_stats,
        'daily_trend': list(daily_trend),
    }

    return render(request, 'admin/loyalty/campaign_analytics.html', context)


@staff_member_required
def export_campaign_report(request, campaign_id):
    """
    Export campaign performance report as CSV
    """
    from django.shortcuts import get_object_or_404

    campaign = get_object_or_404(LoyaltyCampaign, pk=campaign_id)
    executions = LoyaltyCampaignExecution.objects.filter(campaign=campaign).select_related('member__customer')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="campaign_{campaign.slug}_report.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Execution ID',
        'Member ID',
        'Customer Email',
        'Status',
        'Triggered At',
        'Completed At',
        'Points Awarded',
        'Emails Sent',
        'Current Step',
        'Steps Completed'
    ])

    for execution in executions:
        writer.writerow([
            execution.id,
            execution.member.id,
            execution.member.customer.email,
            execution.status,
            execution.triggered_at,
            execution.completed_at,
            execution.points_awarded,
            len(execution.emails_sent),
            execution.current_step,
            len(execution.steps_completed)
        ])

    return response


@staff_member_required
def member_analytics(request):
    """
    Member engagement and behavior analytics
    """
    days = int(request.GET.get('days', 30))
    start_date = timezone.now() - timedelta(days=days)

    # Member growth
    member_growth = LoyaltyMember.objects.filter(
        joined_at__gte=start_date
    ).annotate(
        date=TruncDate('joined_at')
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')

    # Active members
    active_members = LoyaltyMember.objects.filter(
        balance__last_earned_at__gte=start_date
    ).count()

    # Top members by points
    top_members = LoyaltyMember.objects.select_related('customer', 'current_tier').annotate(
        total_points=F('balance__lifetime_earned')
    ).order_by('-total_points')[:20]

    # Member distribution by tier
    tier_distribution = LoyaltyMember.objects.values(
        'current_tier__name'
    ).annotate(
        count=Count('id')
    ).order_by('-count')

    context = {
        'member_growth': list(member_growth),
        'active_members': active_members,
        'top_members': top_members,
        'tier_distribution': list(tier_distribution),
        'date_range_days': days,
    }

    return render(request, 'admin/loyalty/member_analytics.html', context)


# ============================================
# Helper Functions
# ============================================

def get_program_overview():
    """Get overall program health metrics"""
    total_members = LoyaltyMember.objects.count()

    balances = LoyaltyBalance.objects.aggregate(
        total_available=Sum('available_points'),
        total_pending=Sum('pending_points'),
        total_earned=Sum('lifetime_earned'),
        total_redeemed=Sum('lifetime_redeemed'),
        total_expired=Sum('lifetime_expired')
    )

    # Active campaigns
    active_campaigns = LoyaltyCampaign.objects.filter(
        is_active=True,
        status=LoyaltyCampaign.STATUS_ACTIVE
    ).count()

    # Recent activity (last 7 days)
    week_ago = timezone.now() - timedelta(days=7)
    recent_transactions = LoyaltyTransaction.objects.filter(
        created_at__gte=week_ago
    ).count()

    return {
        'total_members': total_members,
        'active_campaigns': active_campaigns,
        'recent_transactions': recent_transactions,
        'total_points_available': balances['total_available'] or 0,
        'total_points_pending': balances['total_pending'] or 0,
        'total_points_earned': balances['total_earned'] or 0,
        'total_points_redeemed': balances['total_redeemed'] or 0,
        'total_points_expired': balances['total_expired'] or 0,
    }


def get_campaign_performance(start_date):
    """Get campaign performance metrics"""
    campaigns = LoyaltyCampaign.objects.filter(
        is_active=True
    ).annotate(
        executions_count=Count('executions', filter=Q(executions__triggered_at__gte=start_date)),
        completed_count=Count('executions', filter=Q(
            executions__triggered_at__gte=start_date,
            executions__status=LoyaltyCampaignExecution.STATUS_COMPLETED
        )),
        failed_count=Count('executions', filter=Q(
            executions__triggered_at__gte=start_date,
            executions__status=LoyaltyCampaignExecution.STATUS_FAILED
        ))
    ).order_by('-executions_count')[:10]

    campaign_list = []
    for campaign in campaigns:
        completion_rate = 0
        if campaign.executions_count > 0:
            completion_rate = (campaign.completed_count / campaign.executions_count) * 100

        campaign_list.append({
            'id': campaign.id,
            'name': campaign.name,
            'type': campaign.get_campaign_type_display(),
            'executions': campaign.executions_count,
            'completed': campaign.completed_count,
            'failed': campaign.failed_count,
            'completion_rate': round(completion_rate, 1)
        })

    return campaign_list


def get_member_engagement(start_date):
    """Get member engagement metrics"""
    # Members who earned points
    active_earners = LoyaltyMember.objects.filter(
        balance__last_earned_at__gte=start_date
    ).count()

    # Members who redeemed
    active_redeemers = LoyaltyRedemption.objects.filter(
        created_at__gte=start_date
    ).values('member').distinct().count()

    # Average points per member
    avg_balance = LoyaltyBalance.objects.aggregate(
        avg=Avg('available_points')
    )['avg'] or 0

    # Engagement rate
    total_members = LoyaltyMember.objects.count()
    engagement_rate = 0
    if total_members > 0:
        engagement_rate = (active_earners / total_members) * 100

    return {
        'active_earners': active_earners,
        'active_redeemers': active_redeemers,
        'avg_balance': round(avg_balance),
        'engagement_rate': round(engagement_rate, 1)
    }


def get_points_economy(start_date):
    """Get points economy health metrics"""
    transactions = LoyaltyTransaction.objects.filter(
        created_at__gte=start_date
    )

    earned = transactions.filter(
        transaction_type=LoyaltyTransaction.TYPE_EARN
    ).aggregate(total=Sum('points'))['total'] or 0

    redeemed = transactions.filter(
        transaction_type=LoyaltyTransaction.TYPE_REDEEM
    ).aggregate(total=Sum('points'))['total'] or 0

    expired = transactions.filter(
        transaction_type=LoyaltyTransaction.TYPE_EXPIRE
    ).aggregate(total=Sum('points'))['total'] or 0

    bonus = transactions.filter(
        transaction_type=LoyaltyTransaction.TYPE_BONUS
    ).aggregate(total=Sum('points'))['total'] or 0

    # Daily trend
    daily_trend = transactions.annotate(
        date=TruncDate('created_at')
    ).values('date', 'transaction_type').annotate(
        total=Sum('points')
    ).order_by('date')

    return {
        'earned': earned,
        'redeemed': redeemed,
        'expired': expired,
        'bonus': bonus,
        'net': earned + bonus - redeemed - expired,
        'daily_trend': list(daily_trend)
    }


def get_tier_distribution():
    """Get tier distribution and progression metrics"""
    tiers = LoyaltyTier.objects.annotate(
        member_count=Count('members')
    ).order_by('rank')

    tier_list = []
    for tier in tiers:
        tier_list.append({
            'name': tier.name,
            'rank': tier.rank,
            'member_count': tier.member_count,
            'min_points': tier.min_points_earned
        })

    return tier_list


def analyze_journey_performance(campaign):
    """Analyze multi-step journey performance"""
    executions = LoyaltyCampaignExecution.objects.filter(campaign=campaign)

    # Step completion rates
    step_stats = {}
    if campaign.journey_steps:
        for step in campaign.journey_steps:
            step_num = step.get('step')
            completed_count = sum(1 for e in executions if step_num in e.steps_completed)

            step_stats[step_num] = {
                'completed': completed_count,
                'completion_rate': (completed_count / executions.count() * 100) if executions.count() > 0 else 0
            }

    # Average journey duration
    completed_executions = executions.filter(
        status=LoyaltyCampaignExecution.STATUS_COMPLETED,
        completed_at__isnull=False
    )

    avg_duration = None
    if completed_executions.exists():
        durations = []
        for execution in completed_executions:
            if execution.triggered_at and execution.completed_at:
                duration = (execution.completed_at - execution.triggered_at).total_seconds() / 86400  # days
                durations.append(duration)

        if durations:
            avg_duration = sum(durations) / len(durations)

    return {
        'total_steps': len(campaign.journey_steps) if campaign.journey_steps else 0,
        'step_stats': step_stats,
        'avg_duration_days': round(avg_duration, 1) if avg_duration else None
    }
