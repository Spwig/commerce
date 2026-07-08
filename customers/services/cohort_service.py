"""
Cohort-based LTV calculation service
Builds customer cohorts and calculates retention-based lifetime value
"""

from django.db.models import Sum, Count, Q, F
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from djmoney.money import Money

from customers.models import CustomerMetrics, CustomerCohort, CohortMetrics
from orders.models import Order
from core.utils import get_default_currency


class CohortService:
    """Service for building and analyzing customer cohorts"""

    @classmethod
    def build_all_cohorts(cls):
        """
        Build or update all customer cohorts from order data
        Returns: dict with cohort statistics
        """
        # Get all customers with at least one completed order
        customers_with_orders = CustomerMetrics.objects.filter(
            completed_orders__gte=1
        ).select_related('user')

        cohorts_created = 0
        customers_assigned = 0

        for metrics in customers_with_orders:
            if metrics.first_purchase_date and metrics.cohort_month:
                # Get the first order to determine acquisition channel and category
                first_order = metrics.user.orders.filter(
                    status='delivered'
                ).order_by('created_at').first()

                if first_order:
                    acquisition_channel = first_order.source or 'unknown'

                    # Get first product category from the first order
                    first_category = ''
                    first_item = first_order.items.select_related('product__category').first()
                    if first_item and first_item.product and first_item.product.category:
                        first_category = first_item.product.category.name

                    # Create or get cohort
                    cohort, created = CustomerCohort.objects.get_or_create(
                        cohort_date=metrics.cohort_month,
                        acquisition_channel=acquisition_channel,
                        first_product_category=first_category
                    )

                    if created:
                        cohorts_created += 1

                    customers_assigned += 1

        # Update customer counts for each cohort
        cls._update_cohort_counts()

        return {
            'cohorts_created': cohorts_created,
            'cohorts_updated': CustomerCohort.objects.count(),
            'customers_assigned': customers_assigned,
        }

    @classmethod
    def _update_cohort_counts(cls):
        """Update customer_count for all cohorts"""
        for cohort in CustomerCohort.objects.all():
            count = CustomerMetrics.objects.filter(
                cohort_month=cohort.cohort_date,
                first_purchase_date__isnull=False
            ).count()
            cohort.customer_count = count
            cohort.save(update_fields=['customer_count', 'updated_at'])

    @classmethod
    def calculate_cohort_metrics(cls, cohort_id=None):
        """
        Calculate retention and LTV metrics for cohorts
        Args:
            cohort_id: Optional - calculate for specific cohort, or all if None
        Returns: dict with calculation statistics
        """
        default_currency = get_default_currency()

        if cohort_id:
            cohorts = CustomerCohort.objects.filter(id=cohort_id)
        else:
            cohorts = CustomerCohort.objects.all()

        metrics_created = 0
        metrics_updated = 0

        for cohort in cohorts:
            # Calculate metrics for each month since cohort creation
            cohort_age = cohort.cohort_age_months

            for month_offset in range(cohort_age + 1):
                result = cls._calculate_cohort_month_metrics(
                    cohort,
                    month_offset,
                    default_currency
                )
                if result == 'created':
                    metrics_created += 1
                elif result == 'updated':
                    metrics_updated += 1

        return {
            'cohorts_processed': cohorts.count(),
            'metrics_created': metrics_created,
            'metrics_updated': metrics_updated,
        }

    @classmethod
    def _calculate_cohort_month_metrics(cls, cohort, months_since_acquisition, default_currency):
        """
        Calculate metrics for a specific cohort at a specific time offset
        """
        # Define the time window for this cohort month
        cohort_date = cohort.cohort_date
        cutoff_date = cohort_date + timedelta(days=30 * (months_since_acquisition + 1))

        # Get customers in this cohort
        cohort_customers = CustomerMetrics.objects.filter(
            cohort_month=cohort_date,
            first_purchase_date__isnull=False
        ).values_list('user_id', flat=True)

        if not cohort_customers:
            return None

        # Get all orders from cohort customers up to the cutoff date
        orders_in_period = Order.objects.filter(
            user_id__in=cohort_customers,
            status='delivered',
            created_at__lte=cutoff_date
        )

        # Calculate cumulative revenue
        total_revenue = orders_in_period.aggregate(
            total=Sum('total_amount')
        )['total']

        if total_revenue is None:
            total_revenue = Money(0, default_currency)

        # Calculate cumulative orders
        total_orders = orders_in_period.count()

        # Calculate active customers (made purchase in last 6 months from cutoff)
        activity_start = cutoff_date - timedelta(days=180)
        active_customers = Order.objects.filter(
            user_id__in=cohort_customers,
            status='delivered',
            created_at__gte=activity_start,
            created_at__lte=cutoff_date
        ).values('user_id').distinct().count()

        # Calculate average LTV
        customer_count = len(cohort_customers)
        if customer_count > 0:
            average_ltv = total_revenue / customer_count
            retention_rate = active_customers / customer_count
        else:
            average_ltv = Money(0, default_currency)
            retention_rate = 0.0

        # Create or update cohort metrics
        cohort_metric, created = CohortMetrics.objects.update_or_create(
            cohort=cohort,
            months_since_acquisition=months_since_acquisition,
            defaults={
                'active_customers': active_customers,
                'cumulative_revenue': total_revenue,
                'cumulative_orders': total_orders,
                'average_ltv': average_ltv,
                'retention_rate': retention_rate,
            }
        )

        return 'created' if created else 'updated'

    @classmethod
    def update_customer_cohort_ltv(cls):
        """
        Update LTV for all customers using cohort-based calculation
        Only updates customers with completed orders
        Returns: dict with update statistics
        """
        customers_updated = 0
        customers_with_cohort = CustomerMetrics.objects.filter(
            cohort_month__isnull=False,
            completed_orders__gte=1
        )

        for metrics in customers_with_cohort:
            # Find the customer's cohort
            first_order = metrics.user.orders.filter(
                status='delivered'
            ).order_by('created_at').first()

            if not first_order:
                continue

            acquisition_channel = first_order.source or 'unknown'
            first_category = ''
            first_item = first_order.items.select_related('product__category').first()
            if first_item and first_item.product and first_item.product.category:
                first_category = first_item.product.category.name

            # Try to find exact cohort match
            try:
                cohort = CustomerCohort.objects.get(
                    cohort_date=metrics.cohort_month,
                    acquisition_channel=acquisition_channel,
                    first_product_category=first_category
                )
            except CustomerCohort.DoesNotExist:
                # Try without category
                try:
                    cohort = CustomerCohort.objects.get(
                        cohort_date=metrics.cohort_month,
                        acquisition_channel=acquisition_channel,
                        first_product_category=''
                    )
                except CustomerCohort.DoesNotExist:
                    continue

            # Get the latest cohort metric
            latest_metric = cohort.metrics.order_by('-months_since_acquisition').first()

            if latest_metric and latest_metric.average_ltv:
                # Use cohort's average LTV
                metrics.lifetime_value = latest_metric.average_ltv
                metrics.ltv_calculation_method = 'cohort'
                metrics.ltv_last_calculated = timezone.now()

                # Calculate confidence based on cohort size and age
                if cohort.customer_count >= 50 and cohort.cohort_age_months >= 6:
                    metrics.ltv_confidence_score = 0.9
                elif cohort.customer_count >= 20 and cohort.cohort_age_months >= 3:
                    metrics.ltv_confidence_score = 0.7
                else:
                    metrics.ltv_confidence_score = 0.5

                metrics.save(update_fields=[
                    'lifetime_value',
                    'ltv_calculation_method',
                    'ltv_last_calculated',
                    'ltv_confidence_score'
                ])
                customers_updated += 1

        return {
            'customers_updated': customers_updated,
            'customers_processed': customers_with_cohort.count(),
        }

    @classmethod
    def get_cohort_retention_curve(cls, cohort_id):
        """
        Get retention curve data for a specific cohort
        Returns: list of dicts with month and retention_rate
        """
        try:
            cohort = CustomerCohort.objects.get(id=cohort_id)
        except CustomerCohort.DoesNotExist:
            return []

        metrics = cohort.metrics.order_by('months_since_acquisition')

        return [
            {
                'month': metric.months_since_acquisition,
                'retention_rate': round(metric.retention_rate * 100, 2),
                'active_customers': metric.active_customers,
                'average_ltv': float(metric.average_ltv.amount),
                'cumulative_revenue': float(metric.cumulative_revenue.amount),
            }
            for metric in metrics
        ]

    @classmethod
    def get_cohort_comparison(cls, limit=12):
        """
        Get comparison data for recent cohorts, aggregated by month.
        Combines all channels/categories for each cohort month.
        Args:
            limit: Number of most recent cohort months to compare
        Returns: list of cohort comparison data aggregated by month
        """
        # Get distinct cohort dates
        distinct_dates = CustomerCohort.objects.values_list(
            'cohort_date', flat=True
        ).distinct().order_by('-cohort_date')[:limit]

        comparison_data = []
        for cohort_date in distinct_dates:
            # Get all cohorts for this month
            month_cohorts = CustomerCohort.objects.filter(cohort_date=cohort_date)

            # Get actual customer count from CustomerMetrics (not duplicated)
            actual_customer_count = CustomerMetrics.objects.filter(
                cohort_month=cohort_date,
                first_purchase_date__isnull=False
            ).count()

            # Calculate weighted average LTV and retention
            total_ltv = Decimal('0')
            total_retention = 0.0
            cohorts_with_metrics = 0

            for cohort in month_cohorts:
                latest_metric = cohort.metrics.order_by('-months_since_acquisition').first()
                if latest_metric:
                    total_ltv += latest_metric.average_ltv.amount
                    total_retention += latest_metric.retention_rate
                    cohorts_with_metrics += 1

            if cohorts_with_metrics > 0:
                avg_ltv = float(total_ltv / cohorts_with_metrics)
                avg_retention = round((total_retention / cohorts_with_metrics) * 100, 2)
            else:
                avg_ltv = 0.0
                avg_retention = 0.0

            # Calculate cohort age
            today = timezone.now().date()
            cohort_age_months = (today.year - cohort_date.year) * 12 + (today.month - cohort_date.month)

            comparison_data.append({
                'cohort_date': cohort_date.strftime('%Y-%m'),
                'customer_count': actual_customer_count,
                'average_ltv': avg_ltv,
                'retention_rate': avg_retention,
                'cohort_age_months': cohort_age_months,
            })

        return comparison_data

    @classmethod
    def get_channel_performance(cls):
        """
        Get LTV performance by acquisition channel
        Returns: dict with channel stats
        """
        channels = CustomerCohort.objects.values('acquisition_channel').distinct()

        channel_stats = []
        for channel in channels:
            channel_name = channel['acquisition_channel']
            cohorts = CustomerCohort.objects.filter(acquisition_channel=channel_name)

            # Get all latest metrics for these cohorts
            total_customers = cohorts.aggregate(total=Sum('customer_count'))['total'] or 0

            if total_customers > 0:
                # Calculate weighted average LTV
                weighted_ltv_sum = Decimal('0')
                for cohort in cohorts:
                    latest_metric = cohort.metrics.order_by('-months_since_acquisition').first()
                    if latest_metric and cohort.customer_count > 0:
                        weight = Decimal(str(cohort.customer_count)) / Decimal(str(total_customers))
                        weighted_ltv_sum += Decimal(str(latest_metric.average_ltv.amount)) * weight

                channel_stats.append({
                    'channel': channel_name,
                    'total_customers': total_customers,
                    'average_ltv': float(weighted_ltv_sum),
                    'cohort_count': cohorts.count(),
                })

        # Sort by average LTV descending
        channel_stats.sort(key=lambda x: x['average_ltv'], reverse=True)

        return channel_stats

    @classmethod
    def get_category_performance(cls):
        """
        Get LTV performance by first product category
        Returns: list of category stats
        """
        categories = CustomerCohort.objects.exclude(
            first_product_category=''
        ).values('first_product_category').distinct()

        category_stats = []
        for category in categories:
            category_name = category['first_product_category']
            cohorts = CustomerCohort.objects.filter(first_product_category=category_name)

            total_customers = cohorts.aggregate(total=Sum('customer_count'))['total'] or 0

            if total_customers > 0:
                # Calculate weighted average LTV
                weighted_ltv_sum = Decimal('0')
                for cohort in cohorts:
                    latest_metric = cohort.metrics.order_by('-months_since_acquisition').first()
                    if latest_metric and cohort.customer_count > 0:
                        weight = Decimal(str(cohort.customer_count)) / Decimal(str(total_customers))
                        weighted_ltv_sum += Decimal(str(latest_metric.average_ltv.amount)) * weight

                category_stats.append({
                    'category': category_name,
                    'total_customers': total_customers,
                    'average_ltv': float(weighted_ltv_sum),
                    'cohort_count': cohorts.count(),
                })

        # Sort by average LTV descending
        category_stats.sort(key=lambda x: x['average_ltv'], reverse=True)

        return category_stats

    @classmethod
    def get_cohort_dashboard_data(cls):
        """
        Get comprehensive cohort data for dashboard display
        Returns: dict with all dashboard metrics
        """
        total_cohorts = CustomerCohort.objects.count()
        total_customers_in_cohorts = CustomerMetrics.objects.filter(
            cohort_month__isnull=False
        ).count()

        # Get recent cohort comparison
        cohort_comparison = cls.get_cohort_comparison(limit=12)

        # Get channel performance
        channel_performance = cls.get_channel_performance()

        # Get category performance
        category_performance = cls.get_category_performance()

        # Get overall retention trend (average across all active cohorts)
        recent_cohorts = CustomerCohort.objects.order_by('-cohort_date')[:6]
        avg_retention_by_month = {}

        for month in range(13):  # 0-12 months
            retention_values = []
            for cohort in recent_cohorts:
                metric = cohort.metrics.filter(months_since_acquisition=month).first()
                if metric:
                    retention_values.append(metric.retention_rate)

            if retention_values:
                avg_retention_by_month[month] = round(
                    sum(retention_values) / len(retention_values) * 100, 2
                )

        return {
            'total_cohorts': total_cohorts,
            'total_customers_in_cohorts': total_customers_in_cohorts,
            'cohort_comparison': cohort_comparison,
            'channel_performance': channel_performance,
            'category_performance': category_performance,
            'average_retention_curve': [
                {'month': month, 'retention': retention}
                for month, retention in avg_retention_by_month.items()
            ],
        }

    @classmethod
    def get_retention_heatmap_data(cls, limit=12):
        """
        Get retention data in heatmap format.
        Returns: dict with cohort labels, month labels, and retention matrix
        """
        # Get distinct cohort dates
        distinct_dates = list(CustomerCohort.objects.values_list(
            'cohort_date', flat=True
        ).distinct().order_by('-cohort_date')[:limit])

        if not distinct_dates:
            return {'cohorts': [], 'months': [], 'data': [], 'raw_data': []}

        # Build retention matrix
        cohort_labels = []
        retention_matrix = []
        raw_data = []  # For insights calculation

        for cohort_date in distinct_dates:
            cohort_labels.append(cohort_date.strftime('%b %Y'))

            # Get all cohorts for this month and aggregate retention
            month_cohorts = CustomerCohort.objects.filter(cohort_date=cohort_date)

            row = []
            row_raw = {'cohort_date': cohort_date, 'retention_by_month': {}}

            for month_offset in range(13):  # Months 0-12
                retention_values = []
                for cohort in month_cohorts:
                    metric = cohort.metrics.filter(months_since_acquisition=month_offset).first()
                    if metric:
                        retention_values.append(metric.retention_rate * 100)

                if retention_values:
                    avg_retention = round(sum(retention_values) / len(retention_values), 1)
                    row.append(avg_retention)
                    row_raw['retention_by_month'][month_offset] = avg_retention
                else:
                    row.append(None)  # No data yet for this period

            retention_matrix.append(row)
            raw_data.append(row_raw)

        return {
            'cohorts': cohort_labels,
            'months': list(range(13)),
            'data': retention_matrix,
            'raw_data': raw_data
        }

    @classmethod
    def get_retention_insights(cls):
        """
        Analyze retention data and generate actionable insights.
        Returns: list of insight dicts with type, title, description, and priority
        """
        insights = []
        heatmap_data = cls.get_retention_heatmap_data(limit=12)

        if not heatmap_data['data']:
            return [{
                'type': 'info',
                'icon': 'fa-info-circle',
                'title': 'No Cohort Data Yet',
                'description': 'Cohort data will appear once customers make purchases. Check back soon!',
                'priority': 1
            }]

        # Analyze drop-off points
        all_dropoffs = []
        for row_idx, row in enumerate(heatmap_data['data']):
            for month in range(1, len(row)):
                if row[month] is not None and row[month - 1] is not None:
                    dropoff = row[month - 1] - row[month]
                    if dropoff > 0:
                        all_dropoffs.append({
                            'from_month': month - 1,
                            'to_month': month,
                            'dropoff': dropoff,
                            'cohort': heatmap_data['cohorts'][row_idx]
                        })

        # Find biggest drop-off point across all cohorts
        if all_dropoffs:
            # Group by month transition and average
            month_transitions = {}
            for d in all_dropoffs:
                key = (d['from_month'], d['to_month'])
                if key not in month_transitions:
                    month_transitions[key] = []
                month_transitions[key].append(d['dropoff'])

            # Find worst transition
            worst_transition = None
            worst_avg_dropoff = 0
            for (from_m, to_m), dropoffs in month_transitions.items():
                avg_dropoff = sum(dropoffs) / len(dropoffs)
                if avg_dropoff > worst_avg_dropoff:
                    worst_avg_dropoff = avg_dropoff
                    worst_transition = (from_m, to_m)

            if worst_transition and worst_avg_dropoff > 10:
                from_m, to_m = worst_transition
                insights.append({
                    'type': 'warning',
                    'icon': 'fa-exclamation-triangle',
                    'title': f'Biggest Drop-off at Month {to_m}',
                    'description': f'Retention drops by {worst_avg_dropoff:.0f}% between month {from_m} and {to_m}. '
                                   f'Consider adding a re-engagement email around day {to_m * 30 - 15}.',
                    'priority': 1
                })

        # Compare cohort performance
        cohort_performance = []
        for row_idx, row in enumerate(heatmap_data['data']):
            # Calculate average retention for months 1-3 (if available)
            early_retention = [r for r in row[1:4] if r is not None]
            if early_retention:
                avg_early = sum(early_retention) / len(early_retention)
                cohort_performance.append({
                    'cohort': heatmap_data['cohorts'][row_idx],
                    'avg_retention': avg_early
                })

        if len(cohort_performance) >= 2:
            cohort_performance.sort(key=lambda x: x['avg_retention'], reverse=True)
            best = cohort_performance[0]
            worst = cohort_performance[-1]

            if best['avg_retention'] - worst['avg_retention'] > 10:
                insights.append({
                    'type': 'success',
                    'icon': 'fa-star',
                    'title': f'{best["cohort"]} Cohort Outperforms',
                    'description': f'{best["cohort"]} has {best["avg_retention"]:.0f}% early retention vs '
                                   f'{worst["avg_retention"]:.0f}% for {worst["cohort"]}. '
                                   f'Analyze what made {best["cohort"]} successful.',
                    'priority': 2
                })

        # Calculate overall retention health
        latest_cohorts = heatmap_data['data'][:3]  # Last 3 cohorts
        month_3_retention = []
        for row in latest_cohorts:
            if len(row) > 3 and row[3] is not None:
                month_3_retention.append(row[3])

        if month_3_retention:
            avg_3m_retention = sum(month_3_retention) / len(month_3_retention)
            if avg_3m_retention >= 40:
                insights.append({
                    'type': 'success',
                    'icon': 'fa-thumbs-up',
                    'title': 'Strong 3-Month Retention',
                    'description': f'Your 3-month retention is {avg_3m_retention:.0f}%, which is excellent. '
                                   f'Keep up the great customer experience!',
                    'priority': 3
                })
            elif avg_3m_retention >= 25:
                insights.append({
                    'type': 'info',
                    'icon': 'fa-chart-line',
                    'title': 'Average 3-Month Retention',
                    'description': f'Your 3-month retention is {avg_3m_retention:.0f}%. '
                                   f'Consider loyalty programs or post-purchase follow-ups to improve.',
                    'priority': 3
                })
            else:
                insights.append({
                    'type': 'warning',
                    'icon': 'fa-exclamation-circle',
                    'title': 'Low 3-Month Retention',
                    'description': f'Your 3-month retention is {avg_3m_retention:.0f}%. '
                                   f'Focus on early customer engagement and product quality feedback.',
                    'priority': 1
                })

        # Sort by priority
        insights.sort(key=lambda x: x['priority'])

        return insights

    @classmethod
    def get_ltv_by_channel(cls):
        """
        Get LTV breakdown by acquisition channel.
        Calculates directly from customer orders for accuracy.
        Returns: dict with channel data for chart and analysis
        """
        from django.db.models import Sum
        from django.contrib.auth import get_user_model
        User = get_user_model()

        # Get all customers with completed orders
        customers_with_orders = CustomerMetrics.objects.filter(
            completed_orders__gte=1,
            first_purchase_date__isnull=False
        ).select_related('user')

        # Build channel data from actual customer orders
        channel_aggregation = {}  # channel -> {customers: set, total_revenue: Decimal}

        for metrics in customers_with_orders:
            # Get the customer's first order to determine acquisition channel
            first_order = Order.objects.filter(
                user=metrics.user,
                status='delivered'
            ).order_by('created_at').first()

            if not first_order:
                continue

            channel = first_order.source or 'direct'

            if channel not in channel_aggregation:
                channel_aggregation[channel] = {
                    'customer_ids': set(),
                    'total_revenue': Decimal('0'),
                }

            # Add customer and their total revenue
            channel_aggregation[channel]['customer_ids'].add(metrics.user_id)
            channel_aggregation[channel]['total_revenue'] += metrics.total_spent.amount

        # Build channel data list
        channel_data = []
        for channel, data in channel_aggregation.items():
            customer_count = len(data['customer_ids'])
            total_revenue = float(data['total_revenue'])
            avg_ltv = total_revenue / customer_count if customer_count > 0 else 0

            channel_data.append({
                'channel': channel,
                'display_name': cls._format_channel_name(channel),
                'average_ltv': avg_ltv,
                'total_revenue': total_revenue,
                'customer_count': customer_count,
                'color': cls._get_channel_color(channel),
            })

        # Sort by average LTV descending
        channel_data.sort(key=lambda x: x['average_ltv'], reverse=True)

        return {
            'channels': channel_data,
            'total_channels': len(channel_data),
        }

    @classmethod
    def get_channel_insights(cls):
        """
        Analyze channel data and generate actionable insights.
        Always returns at least one useful insight.
        """
        insights = []
        channel_data = cls.get_ltv_by_channel()

        if not channel_data['channels']:
            return [{
                'type': 'info',
                'icon': 'fas fa-info-circle',
                'title': 'No Channel Data Yet',
                'description': 'Channel performance data will appear once customers make purchases.',
                'priority': 1
            }]

        channels = channel_data['channels']
        total_customers = sum(c['customer_count'] for c in channels)
        total_revenue = sum(c['total_revenue'] for c in channels)

        # Find best and worst performing channels
        if len(channels) >= 2:
            best = channels[0]
            worst = channels[-1]

            if best['average_ltv'] > 0 and worst['average_ltv'] > 0:
                ltv_diff = ((best['average_ltv'] - worst['average_ltv']) / worst['average_ltv']) * 100

                if ltv_diff > 50:
                    insights.append({
                        'type': 'success',
                        'icon': 'fas fa-trophy',
                        'title': f'{best["display_name"]} Delivers Best LTV',
                        'description': f'Customers from {best["display_name"]} have ${best["average_ltv"]:.0f} avg LTV, '
                                       f'{ltv_diff:.0f}% higher than {worst["display_name"]}. '
                                       f'Consider increasing investment in this channel.',
                        'priority': 1
                    })
                else:
                    # Still show which channel is best even if difference is small
                    insights.append({
                        'type': 'info',
                        'icon': 'fas fa-chart-bar',
                        'title': f'{best["display_name"]} Leads in LTV',
                        'description': f'{best["display_name"]} has the highest avg LTV at ${best["average_ltv"]:.0f}. '
                                       f'Channel performance is relatively balanced across your acquisition sources.',
                        'priority': 2
                    })

        # Check for underperforming high-traffic channels
        for channel in channels:
            if channel['customer_count'] > 10 and channel['average_ltv'] < 50:
                insights.append({
                    'type': 'warning',
                    'icon': 'fas fa-exclamation-triangle',
                    'title': f'{channel["display_name"]} Has Low LTV',
                    'description': f'{channel["display_name"]} brings {channel["customer_count"]} customers '
                                   f'but avg LTV is only ${channel["average_ltv"]:.0f}. '
                                   f'Review targeting or onboarding for this channel.',
                    'priority': 2
                })
                break  # Only show one warning

        # If only one channel or no specific insights, show summary
        if len(channels) == 1:
            channel = channels[0]
            insights.append({
                'type': 'info',
                'icon': 'fas fa-bullhorn',
                'title': f'All Traffic from {channel["display_name"]}',
                'description': f'Your {channel["customer_count"]} customers all came through {channel["display_name"]} '
                               f'with avg LTV of ${channel["average_ltv"]:.0f}. Consider diversifying acquisition channels.',
                'priority': 1
            })

        # Always add a summary insight if we have data
        if not insights and channels:
            avg_ltv = sum(c['average_ltv'] for c in channels) / len(channels)
            insights.append({
                'type': 'info',
                'icon': 'fas fa-info-circle',
                'title': f'{len(channels)} Acquisition Channels',
                'description': f'Tracking {total_customers} customers across {len(channels)} channels '
                               f'with ${total_revenue:,.0f} total revenue and ${avg_ltv:.0f} average LTV.',
                'priority': 3
            })

        insights.sort(key=lambda x: x['priority'])
        return insights

    @classmethod
    def get_ltv_by_category(cls):
        """
        Get LTV breakdown by first product's ROOT category.
        Groups leaf categories under their top-level parent for cleaner analysis.
        Calculates directly from customer orders for accuracy.
        Returns: dict with category data for chart and analysis
        """
        from catalog.models import Category

        # Build a mapping from category ID to root category name
        category_id_to_root = {}
        category_name_to_root = {}
        for cat in Category.objects.select_related('parent').all():
            root = cat
            while root.parent:
                root = root.parent
            category_id_to_root[cat.id] = root.name
            category_name_to_root[cat.name] = root.name

        # Get all customers with completed orders
        customers_with_orders = CustomerMetrics.objects.filter(
            completed_orders__gte=1,
            first_purchase_date__isnull=False
        ).select_related('user')

        # Aggregate by root category
        root_category_data = {}

        for metrics in customers_with_orders:
            # Get the customer's first order
            first_order = Order.objects.filter(
                user=metrics.user,
                status='delivered'
            ).order_by('created_at').first()

            if not first_order:
                continue

            # Get the first item's category
            first_item = first_order.items.select_related('product__category').first()
            if not first_item or not first_item.product or not first_item.product.category:
                continue

            category = first_item.product.category
            root_category = category_id_to_root.get(category.id, category.name)

            if root_category not in root_category_data:
                root_category_data[root_category] = {
                    'customer_ids': set(),
                    'total_revenue': Decimal('0'),
                }

            # Add customer and their total revenue
            root_category_data[root_category]['customer_ids'].add(metrics.user_id)
            root_category_data[root_category]['total_revenue'] += metrics.total_spent.amount

        # Build category data list
        category_data = []
        for category, data in root_category_data.items():
            customer_count = len(data['customer_ids'])
            total_revenue = float(data['total_revenue'])
            avg_ltv = total_revenue / customer_count if customer_count > 0 else 0

            category_data.append({
                'category': category,
                'display_name': category,
                'average_ltv': avg_ltv,
                'total_revenue': total_revenue,
                'customer_count': customer_count,
                'color': cls._get_category_color(len(category_data)),
            })

        category_data.sort(key=lambda x: x['average_ltv'], reverse=True)

        return {
            'categories': category_data,
            'total_categories': len(category_data),
        }

    @classmethod
    def get_category_insights(cls):
        """
        Analyze first product category data and generate insights.
        Always returns at least one useful insight.
        """
        insights = []
        category_data = cls.get_ltv_by_category()

        if not category_data['categories']:
            return [{
                'type': 'info',
                'icon': 'fas fa-info-circle',
                'title': 'No Category Data Yet',
                'description': 'Category performance will appear once customers make purchases.',
                'priority': 1
            }]

        categories = category_data['categories']
        total_customers = sum(c['customer_count'] for c in categories)
        total_revenue = sum(c['total_revenue'] for c in categories)
        best = categories[0]  # Already sorted by LTV desc

        if len(categories) >= 2:
            worst = categories[-1]

            # Strong performer insight
            if best['average_ltv'] > worst['average_ltv'] * 1.5:
                insights.append({
                    'type': 'success',
                    'icon': 'fas fa-star',
                    'title': f'"{best["display_name"]}" Leads to Highest LTV',
                    'description': f'Customers who first buy from "{best["display_name"]}" have '
                                   f'${best["average_ltv"]:.0f} avg LTV. Consider featuring this category '
                                   f'in acquisition campaigns.',
                    'priority': 1
                })
            else:
                # Still highlight the top performer even if difference is smaller
                insights.append({
                    'type': 'info',
                    'icon': 'fas fa-trophy',
                    'title': f'Top Category: {best["display_name"]}',
                    'description': f'Leads with ${best["average_ltv"]:.0f} avg LTV from '
                                   f'{best["customer_count"]} customers. All categories show '
                                   f'similar LTV performance.',
                    'priority': 2
                })

            # Gateway product insight
            if best['customer_count'] < categories[1]['customer_count'] if len(categories) > 1 else 0:
                insights.append({
                    'type': 'info',
                    'icon': 'fas fa-lightbulb',
                    'title': 'Gateway Product Opportunity',
                    'description': f'"{best["display_name"]}" has best LTV but fewer customers. '
                                   f'Promote it as an entry point to increase high-value acquisitions.',
                    'priority': 2
                })

            # Volume vs value insight
            volume_leader = max(categories, key=lambda x: x['customer_count'])
            if volume_leader != best:
                insights.append({
                    'type': 'info',
                    'icon': 'fas fa-users',
                    'title': f'Most Popular: {volume_leader["display_name"]}',
                    'description': f'Attracts {volume_leader["customer_count"]} customers '
                                   f'(${volume_leader["average_ltv"]:.0f} avg LTV). '
                                   f'Good entry point for customer acquisition.',
                    'priority': 3
                })

        elif len(categories) == 1:
            # Single category insight
            insights.append({
                'type': 'info',
                'icon': 'fas fa-tag',
                'title': f'Single Category: {best["display_name"]}',
                'description': f'All {best["customer_count"]} customers started with '
                               f'"{best["display_name"]}" (${best["average_ltv"]:.0f} avg LTV). '
                               f'Expand your product range to attract diverse customer segments.',
                'priority': 1
            })

        # Fallback summary if still no insights
        if not insights:
            insights.append({
                'type': 'info',
                'icon': 'fas fa-chart-pie',
                'title': f'{len(categories)} Product Categories',
                'description': f'Tracking {total_customers} customers across categories. '
                               f'Top performer: "{best["display_name"]}" with '
                               f'${best["average_ltv"]:.0f} avg LTV.',
                'priority': 3
            })

        insights.sort(key=lambda x: x['priority'])
        return insights

    @classmethod
    def get_cumulative_revenue_curve(cls, limit=6):
        """
        Get cumulative revenue curves for recent cohorts.
        Returns: dict with cohort curves for chart
        """
        distinct_dates = list(CustomerCohort.objects.values_list(
            'cohort_date', flat=True
        ).distinct().order_by('-cohort_date')[:limit])

        curves = []
        max_months = 0

        for cohort_date in distinct_dates:
            cohorts = CustomerCohort.objects.filter(cohort_date=cohort_date)

            # Aggregate cumulative revenue by month
            monthly_data = {}
            for cohort in cohorts:
                for metric in cohort.metrics.all():
                    month = metric.months_since_acquisition
                    if month not in monthly_data:
                        monthly_data[month] = []
                    monthly_data[month].append(float(metric.cumulative_revenue.amount))

            # Average across all cohorts for this date
            curve_data = []
            for month in sorted(monthly_data.keys()):
                avg_revenue = sum(monthly_data[month]) / len(monthly_data[month])
                curve_data.append({'month': month, 'revenue': avg_revenue})
                max_months = max(max_months, month)

            curves.append({
                'cohort': cohort_date.strftime('%b %Y'),
                'data': curve_data,
                'color': cls._get_curve_color(len(curves)),
            })

        return {
            'curves': curves,
            'max_months': max_months,
            'months': list(range(max_months + 1)),
        }

    @classmethod
    def get_revenue_curve_insights(cls):
        """
        Analyze revenue curves and generate insights.
        Always returns at least one useful insight.
        """
        insights = []
        curve_data = cls.get_cumulative_revenue_curve(limit=6)

        if not curve_data['curves']:
            return [{
                'type': 'info',
                'icon': 'fas fa-info-circle',
                'title': 'No Revenue Curve Data Yet',
                'description': 'Revenue curves will appear as cohorts mature.',
                'priority': 1
            }]

        curves = curve_data['curves']
        max_months = curve_data['max_months']

        # Compare early revenue velocity
        curves_with_data = [c for c in curves if len(c['data']) >= 3]
        if len(curves_with_data) >= 2:
            # Get month 3 revenue for each curve
            month_3_revenues = []
            for curve in curves_with_data:
                month_3 = next((d['revenue'] for d in curve['data'] if d['month'] == 3), None)
                if month_3:
                    month_3_revenues.append({'cohort': curve['cohort'], 'revenue': month_3})

            if len(month_3_revenues) >= 2:
                month_3_revenues.sort(key=lambda x: x['revenue'], reverse=True)
                best = month_3_revenues[0]
                recent = month_3_revenues[-1]  # Most recent cohort

                if best['revenue'] > recent['revenue'] * 1.2:
                    insights.append({
                        'type': 'warning',
                        'icon': 'fas fa-chart-line',
                        'title': 'Revenue Velocity Declining',
                        'description': f'{best["cohort"]} reached ${best["revenue"]:.0f} by month 3, '
                                       f'vs ${recent["revenue"]:.0f} for {recent["cohort"]}. '
                                       f'Review recent acquisition quality.',
                        'priority': 1
                    })
                elif recent['revenue'] > best['revenue'] * 1.1:
                    insights.append({
                        'type': 'success',
                        'icon': 'fas fa-rocket',
                        'title': 'Revenue Velocity Improving',
                        'description': f'Recent cohorts are generating revenue faster. '
                                       f'{recent["cohort"]} reached ${recent["revenue"]:.0f} by month 3.',
                        'priority': 2
                    })
                else:
                    # Consistent velocity
                    avg_month3 = sum(r['revenue'] for r in month_3_revenues) / len(month_3_revenues)
                    insights.append({
                        'type': 'info',
                        'icon': 'fas fa-balance-scale',
                        'title': 'Consistent Revenue Velocity',
                        'description': f'Cohorts are generating revenue at a steady pace. '
                                       f'Average ${avg_month3:.0f} by month 3. '
                                       f'Consider strategies to accelerate early purchases.',
                        'priority': 2
                    })

        # Find the most mature cohort and share its performance
        most_mature = max(curves, key=lambda c: len(c['data'])) if curves else None
        if most_mature and most_mature['data']:
            latest_revenue = most_mature['data'][-1]['revenue'] if most_mature['data'] else 0
            months_tracked = len(most_mature['data'])
            insights.append({
                'type': 'info',
                'icon': 'fas fa-history',
                'title': f'Longest Tracked: {most_mature["cohort"]}',
                'description': f'Your oldest cohort has generated ${latest_revenue:.0f} avg cumulative '
                               f'revenue over {months_tracked} months. Use this as a benchmark.',
                'priority': 3
            })

        # Newest cohort insight
        if len(curves) >= 2:
            newest = curves[0]  # First in list is most recent
            if newest['data']:
                month_0_revenue = next((d['revenue'] for d in newest['data'] if d['month'] == 0), None)
                if month_0_revenue:
                    insights.append({
                        'type': 'info',
                        'icon': 'fas fa-seedling',
                        'title': f'New Cohort: {newest["cohort"]}',
                        'description': f'Started with ${month_0_revenue:.0f} avg first-month revenue. '
                                       f'Monitor this cohort to track acquisition quality trends.',
                        'priority': 4
                    })

        # Fallback summary if still no insights
        if not insights:
            insights.append({
                'type': 'info',
                'icon': 'fas fa-chart-area',
                'title': f'{len(curves)} Cohorts Tracked',
                'description': f'Monitoring revenue growth across {len(curves)} cohorts '
                               f'over {max_months} months. More data will reveal trends.',
                'priority': 3
            })

        insights.sort(key=lambda x: x['priority'])
        return insights

    @staticmethod
    def _format_channel_name(channel):
        """Format channel name for display."""
        if not channel:
            return 'Direct'
        return channel.replace('_', ' ').title()

    @staticmethod
    def _get_channel_color(channel):
        """Get color for channel."""
        colors = {
            'organic': '#10b981',
            'paid': '#3b82f6',
            'social': '#8b5cf6',
            'email': '#f59e0b',
            'referral': '#ec4899',
            'direct': '#6b7280',
        }
        return colors.get(channel, '#6b7280')

    @staticmethod
    def _get_category_color(index):
        """Get color for category by index."""
        colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#06b6d4', '#84cc16']
        return colors[index % len(colors)]

    @staticmethod
    def _get_curve_color(index):
        """Get color for revenue curve by index."""
        colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899']
        return colors[index % len(colors)]
