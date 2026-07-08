"""
Shop Dashboard Admin Integration
Provides the Shop Dashboard view for business metrics
"""
from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from datetime import datetime
import json
from .services import ShopAnalyticsService
from .models import SystemMetrics
from referrals.services import get_referral_dashboard_stats
from core.models import SiteSettings
from setup_wizard.models import SetupProgress
from setup_wizard.views import get_wizard_groups


class ShopDashboardAdmin(admin.ModelAdmin):
    """
    Admin integration for Shop Dashboard
    Note: This is NOT directly registered - it's integrated into SystemMetricsAdmin
    """

    change_list_template = 'admin/management/shop_dashboard.html'

    def get_urls(self):
        """Add custom URLs for dashboard"""
        urls = super().get_urls()
        custom_urls = [
            path(
                'shop-dashboard/',
                self.admin_site.admin_view(self.shop_dashboard_view),
                name='management_shop_dashboard'
            ),
            path(
                'shop-dashboard-api/',
                self.admin_site.admin_view(self.shop_dashboard_api),
                name='management_shop_dashboard_api'
            ),
            path(
                'geography-cities/<str:country_code>/',
                self.admin_site.admin_view(self.get_geography_cities),
                name='management_geography_cities'
            ),
        ]
        return custom_urls + urls

    def shop_dashboard_view(self, request):
        """
        Main Shop Dashboard view

        Displays:
        - Action cards (incomplete orders, abandoned carts, etc.)
        - Sales performance metrics
        - Top products
        - Visitor analytics
        - Traffic statistics
        """
        # Get filter parameters
        period = request.GET.get('period', 'this_year')  # Default to YTD
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
            start_date, end_date = ShopAnalyticsService.get_date_range_for_period(
                period, custom_start, custom_end
            )
        except ValueError as e:
            # Fall back to YTD if invalid period
            start_date, end_date = ShopAnalyticsService.get_date_range_for_period('this_year')
            period = 'this_year'

        # Get grouping parameter (for manual override)
        grouping = request.GET.get('grouping', None)

        # Fetch all metrics
        action_cards = ShopAnalyticsService.get_action_cards()
        sales_performance = ShopAnalyticsService.get_sales_performance(
            start_date, end_date, compare
        )
        profit_metrics = ShopAnalyticsService.get_profit_metrics(
            start_date, end_date, compare
        )
        abandoned_cart_metrics = ShopAnalyticsService.get_abandoned_cart_metrics(
            start_date, end_date, compare
        )
        voucher_performance = ShopAnalyticsService.get_voucher_performance(
            start_date, end_date, compare
        )
        customer_segmentation = ShopAnalyticsService.get_customer_segmentation()
        affiliate_summary = ShopAnalyticsService.get_affiliate_summary()
        loyalty_summary = ShopAnalyticsService.get_loyalty_summary(start_date, end_date)
        customer_messages = ShopAnalyticsService.get_customer_messages(limit=10)
        # Calculate unread count
        unread_messages_count = sum(1 for msg in customer_messages if not msg.get('is_read', True))
        shipment_summary = ShopAnalyticsService.get_shipment_summary(start_date, end_date)
        email_campaign_roi = ShopAnalyticsService.get_email_campaign_roi(start_date, end_date)
        sales_channel_performance = ShopAnalyticsService.get_sales_channel_performance(
            start_date, end_date, compare
        )
        conversion_funnel = ShopAnalyticsService.get_conversion_funnel(start_date, end_date)
        traffic_source_analytics = ShopAnalyticsService.get_traffic_source_analytics(start_date, end_date)
        # PRIMARY CHART: Sales over time with automatic grouping
        sales_over_time = ShopAnalyticsService.get_sales_over_time(
            start_date, end_date, compare, grouping
        )
        top_products = ShopAnalyticsService.get_top_products(
            start_date, end_date, limit=10
        )
        visitor_analytics = ShopAnalyticsService.get_visitor_analytics(
            start_date, end_date, compare
        )
        # Use grouped views for better visualization
        views_over_time = ShopAnalyticsService.get_views_over_time_grouped(
            start_date, end_date, compare, grouping
        )
        most_viewed_products = ShopAnalyticsService.get_most_viewed_products(
            start_date, end_date, limit=10
        )
        # Geography with optional drill-down
        country_drill_down = request.GET.get('country', None)
        visitor_geography = ShopAnalyticsService.get_visitor_geography(
            start_date, end_date, limit=10, country_code=country_drill_down
        )
        referrer_stats = ShopAnalyticsService.get_referrer_stats(
            start_date, end_date, limit=10
        )

        # Page-level analytics from PageView model
        from geoip.services import analytics_service as page_analytics_svc
        top_pages = page_analytics_svc.get_top_pages(start_date, end_date, limit=10)
        landing_pages = page_analytics_svc.get_landing_pages(start_date, end_date, limit=10)

        # Get referral program stats
        referral_stats = get_referral_dashboard_stats(start_date, end_date)

        # Get preference metrics
        try:
            from accounts.services.preference_dashboard_service import PreferenceDashboardService
            preference_action_cards = PreferenceDashboardService.get_action_cards()
            preference_metrics = PreferenceDashboardService.get_metrics()

            # Merge preference counts into action_cards dict
            for card in preference_action_cards:
                key = card.get('title', '').lower().replace(' ', '_')
                if key:
                    action_cards[key] = card.get('count', 0)
        except Exception as e:
            # Gracefully handle errors - don't break dashboard
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error loading preference dashboard metrics: {e}", exc_info=True)
            preference_metrics = []

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

        # Translation setup check (local provider, external component accounts, or downloaded models)
        try:
            from translations.models import TranslationProvider, TranslationProviderAccount, InstalledModel
            translation_needs_setup = (
                not TranslationProvider.objects.filter(is_active=True).exists()
                and not TranslationProviderAccount.objects.filter(is_active=True).exists()
                and not InstalledModel.objects.filter(is_downloaded=True).exists()
            )
        except Exception:
            translation_needs_setup = False

        # Setup wizard progress
        setup_progress = SetupProgress.get_progress()
        setup_essential_complete = setup_progress.is_essential_setup_complete()
        setup_completion_pct = setup_progress.get_essential_completion_percentage()
        setup_groups = get_wizard_groups(setup_progress)
        setup_essential_completed = setup_progress.get_essential_groups_completed()
        setup_essential_total = setup_progress.get_essential_groups_total()
        # Auto-open modal on first visit if setup incomplete and not skipped
        setup_auto_open = (
            not setup_essential_complete
            and not setup_progress.wizard_skipped
            and not setup_progress.setup_started_at
        ) or request.GET.get('setup') == 'open'

        context = {
            'title': _('Shop Dashboard'),
            'opts': self.model._meta,
            'has_permission': True,

            # Filter state
            'current_period': period,
            'compare_enabled': compare,
            'start_date': start_date,
            'end_date': end_date,
            'default_currency': default_currency,

            # Metrics data
            'action_cards': action_cards,
            'sales_performance': sales_performance,
            'profit_metrics': profit_metrics,
            'abandoned_cart_metrics': abandoned_cart_metrics,
            'voucher_performance': voucher_performance,
            'customer_segmentation': customer_segmentation,
            'affiliate_summary': affiliate_summary,
            'loyalty_summary': loyalty_summary,
            'customer_messages': customer_messages,
            'unread_messages_count': unread_messages_count,
            'shipment_summary': shipment_summary,
            'email_campaign_roi': email_campaign_roi,
            'sales_channel_performance': sales_channel_performance,
            'sales_channel_performance_json': json.dumps(decimal_to_float(sales_channel_performance)),
            'conversion_funnel': conversion_funnel,
            'conversion_funnel_json': json.dumps(decimal_to_float(conversion_funnel)),
            'traffic_source_analytics': traffic_source_analytics,
            'traffic_source_analytics_json': json.dumps(decimal_to_float(traffic_source_analytics)),
            'sales_over_time': sales_over_time,
            'sales_over_time_json': json.dumps(decimal_to_float(sales_over_time)),
            'top_products': top_products,
            'visitor_analytics': visitor_analytics,
            'views_over_time': views_over_time,
            'views_over_time_json': json.dumps(decimal_to_float(views_over_time)),
            'most_viewed_products': most_viewed_products,
            'visitor_geography': visitor_geography,
            'referrer_stats': referrer_stats,
            'top_pages': top_pages,
            'landing_pages': landing_pages,
            'current_grouping': sales_over_time.get('grouping', 'day'),
            'drill_down_country': country_drill_down,

            # Referral program stats
            'referral_stats': referral_stats,

            # Preference metrics
            'preference_metrics': preference_metrics,

            # Translation setup
            'translation_needs_setup': translation_needs_setup,

            # Setup wizard
            'setup_progress': setup_progress,
            'setup_essential_complete': setup_essential_complete,
            'setup_completion_pct': setup_completion_pct,
            'setup_essential_remaining': 100 - setup_completion_pct,
            'setup_groups': setup_groups,
            'setup_essential_completed': setup_essential_completed,
            'setup_essential_total': setup_essential_total,
            'setup_auto_open': setup_auto_open,

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

        return render(request, 'admin/management/shop_dashboard.html', context)

    def shop_dashboard_api(self, request):
        """
        API endpoint for refreshing dashboard data via AJAX

        Accepts same parameters as main view:
        - period: time period filter
        - compare: whether to compare with previous period
        - start_date: custom start date (ISO format)
        - end_date: custom end date (ISO format)

        Returns JSON with all dashboard metrics
        """
        # Get filter parameters
        period = request.GET.get('period', 'this_year')
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
            start_date, end_date = ShopAnalyticsService.get_date_range_for_period(
                period, custom_start, custom_end
            )
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)

        # Fetch metrics
        action_cards = ShopAnalyticsService.get_action_cards()
        sales_performance = ShopAnalyticsService.get_sales_performance(
            start_date, end_date, compare
        )
        profit_metrics = ShopAnalyticsService.get_profit_metrics(
            start_date, end_date, compare
        )
        abandoned_cart_metrics = ShopAnalyticsService.get_abandoned_cart_metrics(
            start_date, end_date, compare
        )
        voucher_performance = ShopAnalyticsService.get_voucher_performance(
            start_date, end_date, compare
        )
        customer_segmentation = ShopAnalyticsService.get_customer_segmentation()
        affiliate_summary_api = ShopAnalyticsService.get_affiliate_summary()
        loyalty_summary_api = ShopAnalyticsService.get_loyalty_summary(start_date, end_date)
        customer_messages_api = ShopAnalyticsService.get_customer_messages(limit=10)
        shipment_summary_api = ShopAnalyticsService.get_shipment_summary(start_date, end_date)
        email_campaign_roi_api = ShopAnalyticsService.get_email_campaign_roi(start_date, end_date)
        sales_channel_performance_api = ShopAnalyticsService.get_sales_channel_performance(
            start_date, end_date, compare
        )
        conversion_funnel_api = ShopAnalyticsService.get_conversion_funnel(start_date, end_date)
        traffic_source_analytics_api = ShopAnalyticsService.get_traffic_source_analytics(start_date, end_date)
        sales_over_time = ShopAnalyticsService.get_sales_over_time(
            start_date, end_date, compare, grouping
        )
        top_products = ShopAnalyticsService.get_top_products(
            start_date, end_date, limit=10
        )
        visitor_analytics = ShopAnalyticsService.get_visitor_analytics(
            start_date, end_date, compare
        )
        views_over_time = ShopAnalyticsService.get_views_over_time_grouped(
            start_date, end_date, compare, grouping
        )
        most_viewed_products = ShopAnalyticsService.get_most_viewed_products(
            start_date, end_date, limit=10
        )
        # Geography with optional drill-down
        country_drill_down = request.GET.get('country', None)
        visitor_geography = ShopAnalyticsService.get_visitor_geography(
            start_date, end_date, limit=10, country_code=country_drill_down
        )
        referrer_stats = ShopAnalyticsService.get_referrer_stats(
            start_date, end_date, limit=10
        )

        # Page-level analytics from PageView model
        from geoip.services import analytics_service as page_analytics_svc
        top_pages_api = page_analytics_svc.get_top_pages(start_date, end_date, limit=10)
        landing_pages_api = page_analytics_svc.get_landing_pages(start_date, end_date, limit=10)

        # Get referral program stats
        referral_stats_api = get_referral_dashboard_stats(start_date, end_date)

        # Get preference metrics
        try:
            from accounts.services.preference_dashboard_service import PreferenceDashboardService
            preference_action_cards_api = PreferenceDashboardService.get_action_cards()
            preference_metrics_api = PreferenceDashboardService.get_metrics()

            # Merge preference counts into action_cards dict
            for card in preference_action_cards_api:
                key = card.get('title', '').lower().replace(' ', '_')
                if key:
                    action_cards[key] = card.get('count', 0)
        except Exception as e:
            # Gracefully handle errors - don't break dashboard
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error loading preference dashboard metrics for API: {e}", exc_info=True)
            preference_metrics_api = []

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
            'sales_performance': decimal_to_float(sales_performance),
            'profit_metrics': decimal_to_float(profit_metrics),
            'abandoned_cart_metrics': decimal_to_float(abandoned_cart_metrics),
            'voucher_performance': decimal_to_float(voucher_performance),
            'customer_segmentation': decimal_to_float(customer_segmentation),
            'affiliate_summary': decimal_to_float(affiliate_summary_api),
            'loyalty_summary': decimal_to_float(loyalty_summary_api),
            'customer_messages': decimal_to_float(customer_messages_api),
            'shipment_summary': decimal_to_float(shipment_summary_api),
            'email_campaign_roi': decimal_to_float(email_campaign_roi_api),
            'sales_channel_performance': decimal_to_float(sales_channel_performance_api),
            'conversion_funnel': decimal_to_float(conversion_funnel_api),
            'traffic_source_analytics': decimal_to_float(traffic_source_analytics_api),
            'sales_over_time': decimal_to_float(sales_over_time),
            'top_products': decimal_to_float(top_products),
            'visitor_analytics': decimal_to_float(visitor_analytics),
            'views_over_time': decimal_to_float(views_over_time),
            'most_viewed_products': decimal_to_float(most_viewed_products),
            'visitor_geography': decimal_to_float(visitor_geography),
            'referrer_stats': decimal_to_float(referrer_stats),
            'top_pages': top_pages_api,
            'landing_pages': landing_pages_api,
            'referral_stats': decimal_to_float(referral_stats_api),
            'preference_metrics': decimal_to_float(preference_metrics_api),
            'period': period,
            'grouping': sales_over_time.get('grouping', 'day'),
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
        }

        return JsonResponse(response_data)

    def get_geography_cities(self, request, country_code):
        """
        API endpoint for getting cities within a country (accordion drill-down)

        Returns list of cities with visitor counts for the specified country
        """
        # Get date range parameters
        period = request.GET.get('period', 'this_year')
        custom_start = None
        custom_end = None

        if period == 'custom':
            custom_start_str = request.GET.get('start_date')
            custom_end_str = request.GET.get('end_date')
            if custom_start_str:
                try:
                    custom_start = datetime.fromisoformat(custom_start_str)
                except ValueError:
                    pass
            if custom_end_str:
                try:
                    custom_end = datetime.fromisoformat(custom_end_str)
                except ValueError:
                    pass

        try:
            start_date, end_date = ShopAnalyticsService.get_date_range_for_period(
                period, custom_start, custom_end
            )
        except ValueError:
            start_date, end_date = ShopAnalyticsService.get_date_range_for_period('this_year')

        # Get cities for this country
        cities = ShopAnalyticsService.get_visitor_geography(
            start_date, end_date, limit=20, country_code=country_code
        )

        return JsonResponse({'cities': cities})

    # Hide default admin actions since this is a dashboard
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        # Allow access to view the dashboard
        return request.user.is_staff
