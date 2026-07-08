"""
Payment Dashboard View
Provides comprehensive payment analytics and metrics for merchants
"""
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from datetime import datetime
import json

from ..services.analytics_service import PaymentAnalyticsService
from core.models import SiteSettings


@staff_member_required
def payment_dashboard_view(request):
    """
    Main Payment Dashboard view

    Displays:
    - Action cards (failed transactions, pending captures, etc.)
    - Payment performance metrics
    - Revenue over time chart
    - Provider performance comparison
    - Transaction status breakdown
    - Webhook statistics
    - Recent transactions
    """
    # Get filter parameters
    period = request.GET.get('period', 'this_month')  # Default to current month
    compare = request.GET.get('compare', 'true').lower() == 'true'

    # Parse custom dates if provided
    custom_start = None
    custom_end = None
    if period == 'custom':
        custom_start_str = request.GET.get('start_date')
        custom_end_str = request.GET.get('end_date')
        if custom_start_str:
            custom_start = datetime.fromisoformat(custom_start_str)
        if custom_end_str:
            custom_end = datetime.fromisoformat(custom_end_str)

    # Get date range
    try:
        start_date, end_date = PaymentAnalyticsService.get_date_range_for_period(
            period, custom_start, custom_end
        )
    except ValueError as e:
        # Fall back to current month if invalid period
        start_date, end_date = PaymentAnalyticsService.get_date_range_for_period('this_month')
        period = 'this_month'

    # Get grouping parameter (for manual override)
    grouping = request.GET.get('grouping', None)

    # Fetch all metrics
    action_cards = PaymentAnalyticsService.get_action_cards()
    payment_performance = PaymentAnalyticsService.get_payment_performance(
        start_date, end_date, compare
    )
    provider_performance = PaymentAnalyticsService.get_provider_performance(
        start_date, end_date
    )
    revenue_over_time = PaymentAnalyticsService.get_revenue_over_time(
        start_date, end_date, compare, grouping
    )
    transaction_by_status = PaymentAnalyticsService.get_transaction_by_status(
        start_date, end_date
    )
    recent_transactions = PaymentAnalyticsService.get_recent_transactions(limit=10)
    payment_methods_distribution = PaymentAnalyticsService.get_payment_methods_distribution(
        start_date, end_date
    )
    webhook_stats = PaymentAnalyticsService.get_webhook_stats(
        start_date, end_date
    )
    refund_metrics = PaymentAnalyticsService.get_refund_metrics(
        start_date, end_date, compare
    )

    # Convert Decimal values to JSON-serializable format
    def decimal_to_float(obj):
        """Recursively convert Decimal to float in dict/list structures"""
        if isinstance(obj, dict):
            return {k: decimal_to_float(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [decimal_to_float(item) for item in obj]
        elif hasattr(obj, '__float__'):
            return float(obj)
        else:
            return obj

    # Get default currency for formatting
    default_currency = SiteSettings.get_settings().default_currency

    context = {
        'title': _('Payment Dashboard'),
        'has_permission': True,

        # Filter state
        'current_period': period,
        'compare_enabled': compare,
        'start_date': start_date,
        'end_date': end_date,
        'default_currency': default_currency,

        # Metrics data
        'action_cards': action_cards,
        'payment_performance': payment_performance,
        'provider_performance': provider_performance,
        'revenue_over_time': revenue_over_time,
        'revenue_over_time_json': json.dumps(decimal_to_float(revenue_over_time)),
        'transaction_by_status': transaction_by_status,
        'transaction_by_status_json': json.dumps(decimal_to_float(transaction_by_status)),
        'recent_transactions': recent_transactions,
        'payment_methods_distribution': payment_methods_distribution,
        'payment_methods_json': json.dumps(decimal_to_float(payment_methods_distribution)),
        'webhook_stats': webhook_stats,
        'refund_metrics': refund_metrics,
        'current_grouping': revenue_over_time.get('grouping', 'day'),

        # Available period options
        'period_options': [
            ('today', _('Today')),
            ('yesterday', _('Yesterday')),
            ('last_7_days', _('Last 7 Days')),
            ('last_30_days', _('Last 30 Days')),
            ('this_month', _('This Month')),
            ('last_month', _('Last Month')),
            ('this_quarter', _('This Quarter')),
            ('last_quarter', _('Last Quarter')),
            ('this_year', _('This Year / YTD')),
            ('last_year', _('Last Year')),
            ('custom', _('Custom Range')),
        ],
    }

    return render(request, 'admin/payment_providers/payment_dashboard.html', context)


@staff_member_required
def payment_dashboard_api(request):
    """
    API endpoint for refreshing dashboard data via AJAX

    Accepts same parameters as main view:
    - period: time period filter
    - compare: whether to compare with previous period
    - start_date: custom start date (ISO format)
    - end_date: custom end date (ISO format)
    - grouping: manual grouping override (day/week/month)

    Returns JSON with all dashboard metrics
    """
    # Get filter parameters
    period = request.GET.get('period', 'this_month')
    compare = request.GET.get('compare', 'true').lower() == 'true'
    grouping = request.GET.get('grouping', None)

    # Parse custom dates if provided
    custom_start = None
    custom_end = None
    if period == 'custom':
        custom_start_str = request.GET.get('start_date')
        custom_end_str = request.GET.get('end_date')
        if custom_start_str:
            try:
                custom_start = datetime.fromisoformat(custom_start_str)
            except ValueError:
                return JsonResponse({'error': 'Invalid start_date format'}, status=400)
        if custom_end_str:
            try:
                custom_end = datetime.fromisoformat(custom_end_str)
            except ValueError:
                return JsonResponse({'error': 'Invalid end_date format'}, status=400)

    # Get date range
    try:
        start_date, end_date = PaymentAnalyticsService.get_date_range_for_period(
            period, custom_start, custom_end
        )
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

    # Fetch metrics
    action_cards = PaymentAnalyticsService.get_action_cards()
    payment_performance = PaymentAnalyticsService.get_payment_performance(
        start_date, end_date, compare
    )
    provider_performance = PaymentAnalyticsService.get_provider_performance(
        start_date, end_date
    )
    revenue_over_time = PaymentAnalyticsService.get_revenue_over_time(
        start_date, end_date, compare, grouping
    )
    transaction_by_status = PaymentAnalyticsService.get_transaction_by_status(
        start_date, end_date
    )
    recent_transactions = PaymentAnalyticsService.get_recent_transactions(limit=10)
    payment_methods_distribution = PaymentAnalyticsService.get_payment_methods_distribution(
        start_date, end_date
    )
    webhook_stats = PaymentAnalyticsService.get_webhook_stats(
        start_date, end_date
    )
    refund_metrics = PaymentAnalyticsService.get_refund_metrics(
        start_date, end_date, compare
    )

    # Convert Decimal values to float for JSON serialization
    def decimal_to_float(obj):
        """Recursively convert Decimal to float in dict/list structures"""
        if isinstance(obj, dict):
            return {k: decimal_to_float(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [decimal_to_float(item) for item in obj]
        elif hasattr(obj, '__float__'):
            return float(obj)
        else:
            return obj

    response_data = {
        'action_cards': decimal_to_float(action_cards),
        'payment_performance': decimal_to_float(payment_performance),
        'provider_performance': decimal_to_float(provider_performance),
        'revenue_over_time': decimal_to_float(revenue_over_time),
        'transaction_by_status': decimal_to_float(transaction_by_status),
        'recent_transactions': decimal_to_float(recent_transactions),
        'payment_methods_distribution': decimal_to_float(payment_methods_distribution),
        'webhook_stats': decimal_to_float(webhook_stats),
        'refund_metrics': decimal_to_float(refund_metrics),
        'period': period,
        'grouping': revenue_over_time.get('grouping', 'day'),
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
    }

    return JsonResponse(response_data)
