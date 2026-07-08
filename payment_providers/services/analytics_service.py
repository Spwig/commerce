"""
Payment Analytics Service
Provides comprehensive analytics and metrics for payment provider performance
"""
from django.db.models import Sum, Count, Avg, Q, F, DecimalField
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth, Coalesce
from django.utils import timezone
from django.utils.translation import gettext as _
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, List, Any, Optional, Tuple

from ..models import PaymentProviderAccount, PaymentTransaction, PaymentWebhook
from orders.models import Order


class PaymentAnalyticsService:
    """Service for retrieving payment analytics and metrics"""

    @staticmethod
    def get_date_range_for_period(
        period: str,
        custom_start: Optional[datetime] = None,
        custom_end: Optional[datetime] = None
    ) -> Tuple[datetime, datetime]:
        """
        Calculate date range for a given period.
        Returns (start_date, end_date)
        """
        now = timezone.now()
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)

        if period == 'today':
            return today, now
        elif period == 'yesterday':
            yesterday = today - timedelta(days=1)
            return yesterday, today
        elif period == 'last_7_days':
            return today - timedelta(days=7), now
        elif period == 'last_30_days':
            return today - timedelta(days=30), now
        elif period == 'this_month':
            start = today.replace(day=1)
            return start, now
        elif period == 'last_month':
            first_of_month = today.replace(day=1)
            last_month_end = first_of_month - timedelta(days=1)
            last_month_start = last_month_end.replace(day=1)
            return last_month_start, last_month_end + timedelta(days=1)
        elif period == 'this_quarter':
            quarter = (now.month - 1) // 3
            start = today.replace(month=quarter * 3 + 1, day=1)
            return start, now
        elif period == 'last_quarter':
            quarter = (now.month - 1) // 3
            if quarter == 0:
                last_quarter_start = today.replace(year=now.year - 1, month=10, day=1)
                last_quarter_end = today.replace(year=now.year, month=1, day=1)
            else:
                last_quarter_start = today.replace(month=(quarter - 1) * 3 + 1, day=1)
                last_quarter_end = today.replace(month=quarter * 3 + 1, day=1)
            return last_quarter_start, last_quarter_end
        elif period == 'this_year':
            start = today.replace(month=1, day=1)
            return start, now
        elif period == 'last_year':
            last_year_start = today.replace(year=now.year - 1, month=1, day=1)
            last_year_end = today.replace(month=1, day=1)
            return last_year_start, last_year_end
        elif period == 'custom':
            if custom_start and custom_end:
                return custom_start, custom_end
            raise ValueError("Custom period requires start_date and end_date")
        else:
            raise ValueError(f"Invalid period: {period}")

    @staticmethod
    def get_action_cards() -> Dict[str, int]:
        """Get action cards requiring merchant attention"""
        return {
            'failed_transactions': PaymentTransaction.objects.filter(
                status='failed',
                created_at__gte=timezone.now() - timedelta(days=7)
            ).count(),
            'pending_captures': PaymentTransaction.objects.filter(
                status='authorized',
                transaction_type='authorize'
            ).count(),
            'pending_refunds': Order.objects.filter(
                refunds__status='pending'
            ).distinct().count(),
            'connection_errors': PaymentProviderAccount.objects.filter(
                connection_status='error'
            ).count(),
            'unprocessed_webhooks': PaymentWebhook.objects.filter(
                processed=False
            ).count(),
        }

    @staticmethod
    def get_payment_performance(
        start_date: datetime,
        end_date: datetime,
        compare: bool = False
    ) -> Dict[str, Any]:
        """
        Get payment performance metrics
        """
        # Current period
        current_transactions = PaymentTransaction.objects.filter(
            created_at__gte=start_date,
            created_at__lte=end_date
        )

        current_stats = current_transactions.aggregate(
            total_revenue=Coalesce(Sum('amount', filter=Q(status='succeeded')), Decimal('0'), output_field=DecimalField()),
            total_transactions=Count('id'),
            successful_transactions=Count('id', filter=Q(status='succeeded')),
            failed_transactions=Count('id', filter=Q(status='failed')),
            authorized_amount=Coalesce(Sum('amount', filter=Q(status='authorized')), Decimal('0'), output_field=DecimalField()),
            refunded_amount=Coalesce(Sum('amount', filter=Q(status='refunded')), Decimal('0'), output_field=DecimalField()),
            average_transaction=Avg('amount', filter=Q(status='succeeded')),
        )

        # Calculate success rate
        total = current_stats['total_transactions']
        success_rate = (current_stats['successful_transactions'] / total * 100) if total > 0 else 0

        result = {
            'current': {
                'revenue': current_stats['total_revenue'],
                'transactions': current_stats['total_transactions'],
                'successful': current_stats['successful_transactions'],
                'failed': current_stats['failed_transactions'],
                'success_rate': round(success_rate, 2),
                'authorized_amount': current_stats['authorized_amount'],
                'refunded_amount': current_stats['refunded_amount'],
                'average_transaction': current_stats['average_transaction'] or Decimal('0'),
            },
            'changes': {}
        }

        if compare:
            # Previous period (same duration)
            duration = end_date - start_date
            prev_start = start_date - duration
            prev_end = start_date

            prev_transactions = PaymentTransaction.objects.filter(
                created_at__gte=prev_start,
                created_at__lt=prev_end
            )

            prev_stats = prev_transactions.aggregate(
                total_revenue=Coalesce(Sum('amount', filter=Q(status='succeeded')), Decimal('0'), output_field=DecimalField()),
                total_transactions=Count('id'),
                successful_transactions=Count('id', filter=Q(status='succeeded')),
            )

            # Calculate changes
            result['changes'] = {
                'revenue': PaymentAnalyticsService._calculate_change(
                    float(prev_stats['total_revenue']),
                    float(current_stats['total_revenue'])
                ),
                'transactions': PaymentAnalyticsService._calculate_change(
                    prev_stats['total_transactions'],
                    current_stats['total_transactions']
                ),
                'success_rate': PaymentAnalyticsService._calculate_change(
                    (prev_stats['successful_transactions'] / prev_stats['total_transactions'] * 100) if prev_stats['total_transactions'] > 0 else 0,
                    success_rate
                ),
            }

        return result

    @staticmethod
    def get_provider_performance(
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict[str, Any]]:
        """Get performance metrics by payment provider"""
        providers = PaymentProviderAccount.objects.all()
        results = []

        for provider in providers:
            transactions = PaymentTransaction.objects.filter(
                provider_account=provider,
                created_at__gte=start_date,
                created_at__lte=end_date
            )

            stats = transactions.aggregate(
                total_revenue=Coalesce(Sum('amount', filter=Q(status='succeeded')), Decimal('0'), output_field=DecimalField()),
                total_transactions=Count('id'),
                successful=Count('id', filter=Q(status='succeeded')),
                failed=Count('id', filter=Q(status='failed')),
                average_amount=Avg('amount', filter=Q(status='succeeded')),
            )

            success_rate = (stats['successful'] / stats['total_transactions'] * 100) if stats['total_transactions'] > 0 else 0

            results.append({
                'provider_name': provider.display_name or provider.component.name,
                'provider_logo': provider.component.logo.get('url') if provider.component.logo else None,
                'total_revenue': stats['total_revenue'],
                'total_transactions': stats['total_transactions'],
                'successful': stats['successful'],
                'failed': stats['failed'],
                'success_rate': round(success_rate, 2),
                'average_amount': stats['average_amount'] or Decimal('0'),
                'is_active': provider.is_active,
                'is_default': provider.is_default,
            })

        # Sort by revenue
        results.sort(key=lambda x: x['total_revenue'], reverse=True)
        return results

    @staticmethod
    def get_revenue_over_time(
        start_date: datetime,
        end_date: datetime,
        compare: bool = False,
        grouping: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get revenue over time with automatic grouping"""
        # Auto-detect grouping if not specified
        if not grouping:
            duration = (end_date - start_date).days
            if duration <= 7:
                grouping = 'day'
            elif duration <= 90:
                grouping = 'week'
            else:
                grouping = 'month'

        # Select truncation function
        if grouping == 'day':
            trunc_func = TruncDate('created_at')
        elif grouping == 'week':
            trunc_func = TruncWeek('created_at')
        else:
            trunc_func = TruncMonth('created_at')

        # Current period
        current_data = PaymentTransaction.objects.filter(
            created_at__gte=start_date,
            created_at__lte=end_date,
            status='succeeded'
        ).annotate(
            period=trunc_func
        ).values('period').annotate(
            revenue=Sum('amount'),
            transactions=Count('id')
        ).order_by('period')

        labels = []
        revenue_values = []
        transaction_counts = []

        for item in current_data:
            labels.append(item['period'].strftime('%Y-%m-%d'))
            revenue_values.append(float(item['revenue']))
            transaction_counts.append(item['transactions'])

        result = {
            'labels': labels,
            'current': {
                'revenue': revenue_values,
                'transactions': transaction_counts,
            },
            'grouping': grouping,
        }

        if compare:
            duration = end_date - start_date
            prev_start = start_date - duration
            prev_end = start_date

            prev_data = PaymentTransaction.objects.filter(
                created_at__gte=prev_start,
                created_at__lt=prev_end,
                status='succeeded'
            ).annotate(
                period=trunc_func
            ).values('period').annotate(
                revenue=Sum('amount'),
                transactions=Count('id')
            ).order_by('period')

            prev_revenue = []
            prev_transactions = []

            for item in prev_data:
                prev_revenue.append(float(item['revenue']))
                prev_transactions.append(item['transactions'])

            result['previous'] = {
                'revenue': prev_revenue,
                'transactions': prev_transactions,
            }

        return result

    @staticmethod
    def get_transaction_by_status(
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict[str, Any]]:
        """Get transaction counts by status for pie chart"""
        statuses = PaymentTransaction.objects.filter(
            created_at__gte=start_date,
            created_at__lte=end_date
        ).values('status').annotate(
            count=Count('id'),
            amount=Sum('amount')
        ).order_by('-count')

        return list(statuses)

    @staticmethod
    def get_recent_transactions(limit: int = 10) -> List[Dict[str, Any]]:
        """Get most recent transactions"""
        transactions = PaymentTransaction.objects.select_related(
            'provider_account', 'provider_account__component', 'order'
        ).order_by('-created_at')[:limit]

        results = []
        for txn in transactions:
            results.append({
                'id': str(txn.id),
                'transaction_id': txn.transaction_id,
                'amount': txn.amount,
                'status': txn.status,
                'provider_name': txn.provider_account.display_name or txn.provider_account.component.name,
                'order_number': txn.order.order_number if txn.order else None,
                'created_at': txn.created_at,
                'payment_method_type': txn.payment_method_type,
            })

        return results

    @staticmethod
    def get_payment_methods_distribution(
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict[str, Any]]:
        """Get distribution of payment methods used"""
        methods = PaymentTransaction.objects.filter(
            created_at__gte=start_date,
            created_at__lte=end_date,
            status='succeeded'
        ).values('payment_method_type').annotate(
            count=Count('id'),
            revenue=Sum('amount')
        ).order_by('-count')

        return list(methods)

    @staticmethod
    def get_webhook_stats(
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """Get webhook statistics"""
        webhooks = PaymentWebhook.objects.filter(
            created_at__gte=start_date,
            created_at__lte=end_date
        )

        stats = webhooks.aggregate(
            total=Count('id'),
            processed_count=Count('id', filter=Q(processed=True)),
            unprocessed_count=Count('id', filter=Q(processed=False)),
            verified_count=Count('id', filter=Q(signature_verified=True)),
        )

        # By provider
        by_provider = webhooks.values('provider_slug').annotate(
            count=Count('id'),
            processed_count=Count('id', filter=Q(processed=True))
        ).order_by('-count')

        return {
            'total': stats['total'],
            'processed': stats['processed_count'],
            'unprocessed': stats['unprocessed_count'],
            'verified': stats['verified_count'],
            'by_provider': list(by_provider),
        }

    @staticmethod
    def get_refund_metrics(
        start_date: datetime,
        end_date: datetime,
        compare: bool = False
    ) -> Dict[str, Any]:
        """Get refund metrics"""
        refund_transactions = PaymentTransaction.objects.filter(
            created_at__gte=start_date,
            created_at__lte=end_date,
            transaction_type='refund'
        )

        current_stats = refund_transactions.aggregate(
            total_refunded=Coalesce(Sum('amount'), Decimal('0'), output_field=DecimalField()),
            refund_count=Count('id'),
            full_refunds=Count('id', filter=Q(transaction_type='refund', status='succeeded')),
        )

        # Calculate refund rate
        total_revenue = PaymentTransaction.objects.filter(
            created_at__gte=start_date,
            created_at__lte=end_date,
            status='succeeded',
            transaction_type='charge'
        ).aggregate(revenue=Coalesce(Sum('amount'), Decimal('0'), output_field=DecimalField()))['revenue']

        refund_rate = (float(current_stats['total_refunded']) / float(total_revenue) * 100) if total_revenue > 0 else 0

        result = {
            'current': {
                'total_refunded': current_stats['total_refunded'],
                'refund_count': current_stats['refund_count'],
                'refund_rate': round(refund_rate, 2),
            },
            'changes': {}
        }

        if compare:
            duration = end_date - start_date
            prev_start = start_date - duration
            prev_end = start_date

            prev_refunds = PaymentTransaction.objects.filter(
                created_at__gte=prev_start,
                created_at__lt=prev_end,
                transaction_type='refund'
            ).aggregate(
                total_refunded=Coalesce(Sum('amount'), Decimal('0'), output_field=DecimalField()),
                refund_count=Count('id'),
            )

            result['changes'] = {
                'total_refunded': PaymentAnalyticsService._calculate_change(
                    float(prev_refunds['total_refunded']),
                    float(current_stats['total_refunded'])
                ),
                'refund_count': PaymentAnalyticsService._calculate_change(
                    prev_refunds['refund_count'],
                    current_stats['refund_count']
                ),
            }

        return result

    @staticmethod
    def _calculate_change(old_value: float, new_value: float) -> float:
        """Calculate percentage change between two values"""
        if old_value == 0:
            return 100.0 if new_value > 0 else 0.0
        return round(((new_value - old_value) / old_value) * 100, 2)
