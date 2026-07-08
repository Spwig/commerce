"""
Visitor Analytics Service

Provides aggregated visitor statistics and metrics for the analytics dashboard.
Uses DailyPageStats/DailyTrafficStats for historical data and raw PageView for current day.
"""
from django.db.models import Count, Sum, Avg, Q, F, Value, CharField
from django.db.models.functions import TruncDate, TruncHour, ExtractHour
from django.utils import timezone
from datetime import timedelta, date, datetime
import logging

from ..models import PageView, DailyPageStats, DailyTrafficStats, VisitorLocation

logger = logging.getLogger(__name__)


def get_date_range_for_period(period, start_date=None, end_date=None):
    """
    Convert a period string or custom dates into a (start, end) datetime tuple.

    Args:
        period: '7_days', '30_days', '90_days', or 'custom'
        start_date: Date or datetime for custom range start
        end_date: Date or datetime for custom range end

    Returns:
        tuple: (start_datetime, end_datetime)
    """
    now = timezone.now()

    if period == 'custom' and start_date and end_date:
        if isinstance(start_date, date) and not isinstance(start_date, datetime):
            start_date = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
        if isinstance(end_date, date) and not isinstance(end_date, datetime):
            end_date = timezone.make_aware(datetime.combine(end_date, datetime.max.time()))
        return start_date, end_date

    days_map = {
        '7_days': 7,
        '30_days': 30,
        '90_days': 90,
    }
    days = days_map.get(period, 30)
    return now - timedelta(days=days), now


def get_overview(start, end):
    """
    High-level KPIs for the dashboard header cards.

    Returns:
        dict with total_views, unique_visitors, human_visitors, bot_views,
        bounce_rate, avg_pages_per_session
    """
    human_filter = Q(is_bot=False)
    pv_qs = PageView.objects.filter(timestamp__range=(start, end))

    total_views = pv_qs.count()
    human_views = pv_qs.filter(human_filter).count()
    bot_views = total_views - human_views
    unique_visitors = pv_qs.filter(human_filter).values('session_key').distinct().count()

    # Bounce rate: sessions with only 1 page view
    if unique_visitors > 0:
        session_counts = (
            pv_qs.filter(human_filter)
            .values('session_key')
            .annotate(pv_count=Count('id'))
        )
        single_page_sessions = session_counts.filter(pv_count=1).count()
        bounce_rate = round((single_page_sessions / unique_visitors) * 100, 1)

        total_human_views = pv_qs.filter(human_filter).count()
        avg_pages = round(total_human_views / unique_visitors, 1)
    else:
        bounce_rate = 0.0
        avg_pages = 0.0

    return {
        'total_views': total_views,
        'human_views': human_views,
        'unique_visitors': unique_visitors,
        'bot_views': bot_views,
        'bounce_rate': bounce_rate,
        'avg_pages_per_session': avg_pages,
    }


def get_top_pages(start, end, limit=20):
    """
    Most viewed pages ranked by view count (human traffic only).

    Returns:
        list of dicts: url_path, views, unique_visitors, entries
    """
    return list(
        PageView.objects.filter(
            timestamp__range=(start, end),
            is_bot=False,
        )
        .values('url_path')
        .annotate(
            views=Count('id'),
            unique_visitors=Count('session_key', distinct=True),
            entries=Count('id', filter=Q(is_entry_page=True)),
        )
        .order_by('-views')[:limit]
    )


def get_traffic_trends(start, end):
    """
    Daily time-series data for Chart.js line charts.

    Returns:
        dict with labels (dates), views, visitors, bot_views lists
    """
    daily = (
        PageView.objects.filter(timestamp__range=(start, end))
        .annotate(day=TruncDate('timestamp'))
        .values('day')
        .annotate(
            views=Count('id'),
            visitors=Count('session_key', distinct=True, filter=Q(is_bot=False)),
            bot_views=Count('id', filter=Q(is_bot=True)),
        )
        .order_by('day')
    )

    labels = []
    views = []
    visitors = []
    bot_views = []

    for row in daily:
        labels.append(row['day'].strftime('%Y-%m-%d'))
        views.append(row['views'])
        visitors.append(row['visitors'])
        bot_views.append(row['bot_views'])

    return {
        'labels': labels,
        'views': views,
        'visitors': visitors,
        'bot_views': bot_views,
    }


def get_campaign_stats(start, end):
    """
    UTM campaign attribution metrics.

    Returns:
        list of dicts: utm_source, utm_medium, utm_campaign, visitors, page_views
    """
    return list(
        VisitorLocation.objects.filter(
            first_seen__range=(start, end),
            is_bot=False,
        )
        .exclude(utm_source='')
        .values('utm_source', 'utm_medium', 'utm_campaign')
        .annotate(
            visitors=Count('id'),
            page_views=Sum('page_views'),
        )
        .order_by('-visitors')[:20]
    )


def get_referrer_stats(start, end, limit=20):
    """
    Top referrer domains (human traffic only, excluding self-referrals).

    Returns:
        list of dicts: referrer, count
    """
    from django.db.models.functions import Substr, StrIndex

    results = (
        PageView.objects.filter(
            timestamp__range=(start, end),
            is_bot=False,
        )
        .exclude(referrer='')
        .values('referrer')
        .annotate(count=Count('id'))
        .order_by('-count')[:limit * 2]  # Fetch extra for domain dedup
    )

    # Aggregate by domain
    domain_counts = {}
    for row in results:
        try:
            from urllib.parse import urlparse
            domain = urlparse(row['referrer']).netloc or row['referrer']
        except Exception:
            domain = row['referrer']
        domain_counts[domain] = domain_counts.get(domain, 0) + row['count']

    sorted_domains = sorted(domain_counts.items(), key=lambda x: -x[1])[:limit]
    return [{'referrer': domain, 'count': count} for domain, count in sorted_domains]


def get_geographic_distribution(start, end):
    """
    Visitor distribution by country (human traffic only).

    Returns:
        list of dicts: country, visitors, page_views
    """
    return list(
        VisitorLocation.objects.filter(
            first_seen__range=(start, end),
            is_bot=False,
        )
        .exclude(resolved_country='')
        .values('resolved_country')
        .annotate(
            visitors=Count('id'),
            page_views=Sum('page_views'),
        )
        .order_by('-visitors')[:20]
    )


def get_device_distribution(start, end):
    """
    Device type breakdown (human traffic only).

    Returns:
        dict: desktop, mobile, tablet, unknown counts
    """
    counts = (
        VisitorLocation.objects.filter(
            first_seen__range=(start, end),
            is_bot=False,
        )
        .values('device_type')
        .annotate(count=Count('id'))
    )

    result = {'desktop': 0, 'mobile': 0, 'tablet': 0, 'unknown': 0}
    for row in counts:
        if row['device_type'] in result:
            result[row['device_type']] = row['count']
    return result


def get_landing_pages(start, end, limit=20):
    """
    Most common entry (landing) pages for human traffic.

    Returns:
        list of dicts: url_path, entries, unique_visitors
    """
    return list(
        PageView.objects.filter(
            timestamp__range=(start, end),
            is_bot=False,
            is_entry_page=True,
        )
        .values('url_path')
        .annotate(
            entries=Count('id'),
            unique_visitors=Count('session_key', distinct=True),
        )
        .order_by('-entries')[:limit]
    )


def get_bot_summary(start, end):
    """
    Bot traffic summary with top user-agents.

    Returns:
        dict: bot_count, human_count, bot_pct, top_bot_agents
    """
    pv_qs = PageView.objects.filter(timestamp__range=(start, end))
    total = pv_qs.count()
    bot_count = pv_qs.filter(is_bot=True).count()
    human_count = total - bot_count

    top_agents = list(
        VisitorLocation.objects.filter(
            first_seen__range=(start, end),
            is_bot=True,
        )
        .values('user_agent')
        .annotate(count=Count('id'))
        .order_by('-count')[:10]
    )

    return {
        'bot_count': bot_count,
        'human_count': human_count,
        'bot_pct': round((bot_count / total) * 100, 1) if total else 0.0,
        'top_bot_agents': top_agents,
    }


def get_session_journey(session_key):
    """
    Ordered page views for a specific session (visitor journey).

    Returns:
        list of dicts: url_path, url, timestamp, referrer, is_entry_page
    """
    return list(
        PageView.objects.filter(session_key=session_key)
        .order_by('timestamp')
        .values('url_path', 'url', 'timestamp', 'referrer', 'is_entry_page')
    )


def get_hourly_distribution(start, end):
    """
    Page views by hour of day (human traffic).

    Returns:
        list of 24 integers (views per hour 0-23)
    """
    hourly = (
        PageView.objects.filter(
            timestamp__range=(start, end),
            is_bot=False,
        )
        .annotate(hour=ExtractHour('timestamp'))
        .values('hour')
        .annotate(count=Count('id'))
        .order_by('hour')
    )

    result = [0] * 24
    for row in hourly:
        result[row['hour']] = row['count']
    return result


def get_new_vs_returning(start, end):
    """
    New vs returning visitor counts.

    Returns:
        dict: new_visitors, returning_visitors
    """
    visitors = VisitorLocation.objects.filter(
        last_seen__range=(start, end),
        is_bot=False,
    )
    new = visitors.filter(first_seen__range=(start, end)).count()
    returning = visitors.exclude(first_seen__range=(start, end)).count()

    return {
        'new_visitors': new,
        'returning_visitors': returning,
    }


def get_campaign_engagement(start, end):
    """
    Campaign quality metrics: avg pages/session per campaign.

    Returns:
        list of dicts: utm_source, utm_campaign, visitors, avg_pages, bounce_rate
    """
    campaigns = (
        VisitorLocation.objects.filter(
            first_seen__range=(start, end),
            is_bot=False,
        )
        .exclude(utm_source='')
        .values('utm_source', 'utm_campaign')
        .annotate(
            visitors=Count('id'),
            avg_pages=Avg('page_views'),
        )
        .order_by('-visitors')[:20]
    )

    return list(campaigns)
