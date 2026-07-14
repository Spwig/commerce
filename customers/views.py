import csv
from datetime import datetime, timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.db.models import Avg, Q, Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
    inline_serializer,
)
from rest_framework import serializers as drf_serializers
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import CustomerProfile
from core.api.api_descriptions import (
    AUTH_REQUIRED,
    INTERNAL_SERVER_ERROR,
)
from core.api.authentication import HeadlessAPIMixin

from .models import (
    AbandonedCart,
    CustomerCohort,
    CustomerMetrics,
    CustomerNote,
    CustomerSegment,
    LTVSettings,
    ProductCategoryLTVMultiplier,
)
from .serializers import (
    CustomerDashboardSerializer,
    CustomerFavoritesSerializer,
    CustomerInsightsSerializer,
    CustomerLifetimeValueSerializer,
    CustomerLoyaltyStatusSerializer,
    CustomerRecommendationsSerializer,
    CustomerSavingsSerializer,
    CustomerStatsSerializer,
)
from .services import CustomerService, RecommendationService, SavingsService
from .services.cohort_service import CohortService
from .services.probabilistic_ltv_service import ProbabilisticLTVService

User = get_user_model()


@staff_member_required
def filter_customers(request):
    """
    AJAX endpoint for filtering customer profiles in admin

    Query Parameters:
    - search: Search by name, username, or email
    - user_type: Filter by is_affiliate/is_loyalty/is_staff
    - segment: Filter by vip/active/at_risk
    - newsletter: Filter by subscribed/not_subscribed
    - min_spent: Minimum total spent
    - max_spent: Maximum total spent
    - min_orders: Minimum order count
    - max_orders: Maximum order count
    - date_from: Registration date from
    - date_to: Registration date to
    """
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Start with all customer profiles (excluding guests)
    profiles = (
        CustomerProfile.objects.select_related(
            "user", "preferred_theme", "user__communication_preferences"
        )
        .prefetch_related("user__orders", "user__affiliate_profile", "user__social_shares")
        .exclude(user__username__startswith="guest_")
    )

    # Search filter
    search = request.GET.get("search", "").strip()
    if search:
        profiles = profiles.filter(
            Q(user__username__icontains=search)
            | Q(user__email__icontains=search)
            | Q(user__first_name__icontains=search)
            | Q(user__last_name__icontains=search)
            | Q(phone__icontains=search)
        )

    # User type filter
    user_type = request.GET.get("user_type", "").strip()
    if user_type == "is_affiliate":
        from affiliate.models import Affiliate

        affiliate_users = Affiliate.objects.values_list("user_id", flat=True)
        profiles = profiles.filter(user_id__in=affiliate_users)
    elif user_type == "is_loyalty":
        from loyalty.models import LoyaltyMember

        loyalty_users = LoyaltyMember.objects.filter(is_active=True).values_list(
            "customer_id", flat=True
        )
        profiles = profiles.filter(user_id__in=loyalty_users)
    elif user_type == "is_staff":
        profiles = profiles.filter(user__is_staff=True)

    # Marketing emails filter (via CommunicationPreference)
    newsletter = request.GET.get("newsletter", "").strip()
    if newsletter == "subscribed":
        from accounts.models import CommunicationPreference

        subscribed_ids = CommunicationPreference.objects.filter(email_marketing=True).values_list(
            "user_id", flat=True
        )
        profiles = profiles.filter(user_id__in=subscribed_ids)
    elif newsletter == "not_subscribed":
        from accounts.models import CommunicationPreference

        subscribed_ids = CommunicationPreference.objects.filter(email_marketing=True).values_list(
            "user_id", flat=True
        )
        profiles = profiles.exclude(user_id__in=subscribed_ids)

    # Registration date filters
    date_from = request.GET.get("date_from", "").strip()
    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, "%Y-%m-%d")
            profiles = profiles.filter(created_at__gte=date_from_obj)
        except ValueError:
            pass

    date_to = request.GET.get("date_to", "").strip()
    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, "%Y-%m-%d")
            profiles = profiles.filter(created_at__lte=date_to_obj)
        except ValueError:
            pass

    # Convert to list for custom filtering
    profiles_list = list(profiles)

    # Customer segment filter (requires property evaluation)
    segment = request.GET.get("segment", "").strip()
    if segment == "vip":
        profiles_list = [p for p in profiles_list if p.is_vip_customer]
    elif segment == "at_risk":
        profiles_list = [p for p in profiles_list if p.is_at_risk]
    elif segment == "active":
        # Active = has recent orders and not at risk
        profiles_list = [p for p in profiles_list if p.total_orders > 0 and not p.is_at_risk]

    # Total spent filters (requires property evaluation)
    min_spent = request.GET.get("min_spent", "").strip()
    max_spent = request.GET.get("max_spent", "").strip()

    if min_spent or max_spent:
        filtered = []
        for profile in profiles_list:
            try:
                total = profile.total_spent
                amount = total.amount if hasattr(total, "amount") else float(total or 0)

                if min_spent and amount < float(min_spent):
                    continue
                if max_spent and amount > float(max_spent):
                    continue

                filtered.append(profile)
            except Exception:
                pass
        profiles_list = filtered

    # Order count filters (requires property evaluation)
    min_orders = request.GET.get("min_orders", "").strip()
    max_orders = request.GET.get("max_orders", "").strip()

    if min_orders or max_orders:
        filtered = []
        for profile in profiles_list:
            try:
                orders = profile.total_orders

                if min_orders and orders < int(min_orders):
                    continue
                if max_orders and orders > int(max_orders):
                    continue

                filtered.append(profile)
            except Exception:
                pass
        profiles_list = filtered

    # Render the partial template
    from django.template.loader import render_to_string

    html = render_to_string(
        "admin/accounts/customerprofile/partials/customer_cards.html",
        {"customers": profiles_list},
        request=request,
    )

    return JsonResponse({"html": html, "count": len(profiles_list)})


@staff_member_required
def customer_dashboard(request):
    """Main customer analytics dashboard"""
    # Get key metrics
    total_customers = CustomerProfile.objects.exclude(user__username__startswith="guest_").count()

    # Active customers (purchased in last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    active_customers = (
        CustomerProfile.objects.filter(
            user__orders__created_at__gte=thirty_days_ago, user__orders__status="delivered"
        )
        .distinct()
        .count()
    )

    # VIP customers
    vip_count = 0
    for profile in CustomerProfile.objects.exclude(user__username__startswith="guest_"):
        if profile.is_vip_customer:
            vip_count += 1

    # At-risk customers
    at_risk_count = 0
    for profile in CustomerProfile.objects.exclude(user__username__startswith="guest_"):
        if profile.is_at_risk:
            at_risk_count += 1

    # Revenue metrics
    total_revenue = CustomerMetrics.objects.aggregate(total=Sum("total_spent"))["total"] or 0

    avg_order_value = CustomerMetrics.objects.aggregate(avg=Avg("average_order_value"))["avg"] or 0

    # Customer segments
    segments = CustomerSegment.objects.filter(is_active=True).order_by("-priority")
    segment_data = []
    for segment in segments:
        count = 0
        for user in User.objects.filter(is_active=True).exclude(username__startswith="guest_"):
            if segment.determine_segment_for_user(user) == segment:
                count += 1
        segment_data.append({"name": segment.display_name, "count": count, "color": segment.color})

    # Recent abandoned carts
    recent_abandoned = (
        AbandonedCart.objects.select_related("user__profile")
        .filter(
            recovered=False,
            user__profile__isnull=False,
        )
        .order_by("-abandoned_at")[:10]
    )

    # Top customers by value
    top_customers = (
        CustomerMetrics.objects.select_related("user__profile")
        .filter(
            user__profile__isnull=False,
        )
        .exclude(user__username__startswith="guest_")
        .order_by("-total_spent")[:10]
    )

    # Cohort analytics data (for Cohort Analytics tab)
    cohorts = CustomerCohort.objects.order_by("-cohort_date")[:12]
    total_cohorts = CustomerCohort.objects.count()
    customers_in_cohorts = CustomerMetrics.objects.filter(cohort_month__isnull=False).count()

    # Get best performing cohort (by LTV)
    # Note: Can't order by property, so we get all and sort in Python
    all_cohorts = list(CustomerCohort.objects.all())
    if all_cohorts:
        best_cohort = max(
            all_cohorts, key=lambda c: float(c.average_ltv.amount) if c.average_ltv else 0
        )
    else:
        best_cohort = None

    # Get most recent cohort
    newest_cohort = CustomerCohort.objects.order_by("-cohort_date").first()

    context = {
        "total_customers": total_customers,
        "active_customers": active_customers,
        "vip_count": vip_count,
        "at_risk_count": at_risk_count,
        "total_revenue": total_revenue,
        "avg_order_value": avg_order_value,
        "segment_data": segment_data,
        "recent_abandoned": recent_abandoned,
        "top_customers": top_customers,
        # Cohort analytics context
        "cohorts": cohorts,
        "total_cohorts": total_cohorts,
        "customers_in_cohorts": customers_in_cohorts,
        "best_cohort": best_cohort,
        "newest_cohort": newest_cohort,
    }

    return render(request, "customers/dashboard.html", context)


@staff_member_required
def customer_analytics_api(request):
    """API endpoint for dashboard analytics data"""
    from customers.services.customer_service import CustomerService

    # Customer growth over time (last 12 months)
    months = []
    customer_growth = []

    for i in range(12, 0, -1):
        month_start = timezone.now().replace(day=1) - timedelta(days=30 * i)
        month_end = month_start + timedelta(days=30)

        count = (
            CustomerProfile.objects.filter(created_at__gte=month_start, created_at__lt=month_end)
            .exclude(user__username__startswith="guest_")
            .count()
        )

        months.append(month_start.strftime("%b %Y"))
        customer_growth.append(count)

    # Revenue by segment (legacy format for existing chart)
    segment_revenue = []
    for segment in CustomerSegment.objects.filter(is_active=True):
        revenue = 0
        for user in User.objects.filter(is_active=True).exclude(username__startswith="guest_"):
            if segment.determine_segment_for_user(user) == segment:
                try:
                    revenue += float(user.customer_metrics.total_spent.amount)
                except Exception:
                    pass
        segment_revenue.append(
            {"name": segment.display_name, "revenue": revenue, "color": segment.color}
        )

    # Purchase frequency distribution
    frequency_data = {
        "high": 0,  # >2 orders/month
        "medium": 0,  # 0.5-2 orders/month
        "low": 0,  # <0.5 orders/month
        "none": 0,  # No orders
    }

    for profile in CustomerProfile.objects.exclude(user__username__startswith="guest_"):
        freq = profile.purchase_frequency
        if freq > 2:
            frequency_data["high"] += 1
        elif freq > 0.5:
            frequency_data["medium"] += 1
        elif freq > 0:
            frequency_data["low"] += 1
        else:
            frequency_data["none"] += 1

    # New: Get detailed segment revenue data with insights
    segment_revenue_data = CustomerService.get_revenue_by_segment()
    segment_insights = CustomerService.get_segment_insights()

    # New: Churn risk distribution and insights
    churn_risk_data = CustomerService.get_churn_risk_distribution()
    churn_risk_insights = CustomerService.get_churn_risk_insights()

    # New: Purchase frequency histogram and insights
    frequency_histogram_data = CustomerService.get_purchase_frequency_distribution()
    frequency_histogram_insights = CustomerService.get_frequency_insights()

    # New: Predicted vs actual purchases and insights
    prediction_data = CustomerService.get_predicted_vs_actual()
    prediction_insights = CustomerService.get_prediction_insights()

    data = {
        "customer_growth": {"months": months, "data": customer_growth},
        "segment_revenue": segment_revenue,
        "frequency_distribution": frequency_data,
        # New data for Revenue by Segment chart
        "segment_revenue_data": segment_revenue_data,
        "segment_insights": segment_insights,
        # New data for Churn Risk Distribution chart
        "churn_risk_data": churn_risk_data,
        "churn_risk_insights": churn_risk_insights,
        # New data for Purchase Frequency Histogram
        "frequency_histogram_data": frequency_histogram_data,
        "frequency_histogram_insights": frequency_histogram_insights,
        # New data for Predicted vs Actual Purchases
        "prediction_data": prediction_data,
        "prediction_insights": prediction_insights,
    }

    return JsonResponse(data)


@staff_member_required
def export_customers(request):
    """Export customer data as CSV"""
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="customers_export.csv"'

    writer = csv.writer(response)
    writer.writerow(
        [
            _("Username"),
            _("Email"),
            _("Full Name"),
            _("Phone"),
            _("Total Spent"),
            _("Lifetime Value"),
            _("Total Orders"),
            _("Completed Orders"),
            _("Last Purchase Date"),
            _("Customer Segment"),
            _("VIP Status"),
            _("At Risk"),
            _("Created Date"),
        ]
    )

    for profile in CustomerProfile.objects.exclude(
        user__username__startswith="guest_"
    ).select_related("user"):
        segment = profile.customer_segment
        writer.writerow(
            [
                profile.user.username,
                profile.user.email,
                profile.user.get_full_name(),
                profile.phone,
                profile.total_spent,
                profile.lifetime_value,
                profile.total_orders,
                profile.completed_orders_count,
                profile.days_since_last_order,
                segment.display_name if segment else "",
                _("Yes") if profile.is_vip_customer else _("No"),
                _("Yes") if profile.is_at_risk else _("No"),
                profile.created_at.strftime("%Y-%m-%d"),
            ]
        )

    return response


@staff_member_required
def refresh_customer_metrics(request):
    """Refresh metrics for all customers"""
    if request.method == "POST":
        updated_count = 0
        for user in User.objects.filter(is_active=True).exclude(username__startswith="guest_"):
            CustomerMetrics.calculate_for_user(user)
            updated_count += 1

        return JsonResponse(
            {
                "success": True,
                "message": _("Refreshed metrics for %(count)s customers")
                % {"count": updated_count},
            }
        )

    return JsonResponse({"success": False, "message": _("Invalid request method")})


# ============================================================================
# Customer-Facing API ViewSets (Phase 5: Customer Analytics & Insights)
# ============================================================================


@extend_schema_view(
    list=extend_schema(
        tags=["Customers"],
        summary=_("Get customer dashboard"),
        description=_(
            "Get comprehensive customer dashboard data including order history, loyalty status, spending insights, recommendations, and recent activity."
        ),
        responses=CustomerDashboardSerializer,
    ),
)
class CustomerDashboardViewSet(HeadlessAPIMixin, viewsets.ViewSet):
    """
    Customer Dashboard ViewSet

    Provides customer-facing dashboard and analytics endpoints

    Endpoints:
    - GET /api/customers/dashboard/ - Get dashboard summary
    - GET /api/customers/stats/ - Get detailed statistics
    - GET /api/customers/insights/ - Get spending insights
    """

    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        Get customer dashboard summary

        Returns comprehensive dashboard data including:
        - Customer info and membership details
        - Quick stats (orders, spend, savings, points)
        - Loyalty status
        - Recent activity
        - Product recommendations
        - Alerts and notifications
        """
        try:
            dashboard_data = CustomerService.get_dashboard_summary(request.user)
            serializer = CustomerDashboardSerializer(dashboard_data)

            return Response({"success": True, "data": serializer.data})

        except Exception as e:
            return Response(
                {"success": False, "message": _("Failed to load dashboard data"), "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @extend_schema(tags=["Customers"])
    @extend_schema(tags=["Customers"])
    @action(detail=False, methods=["get"])
    def stats(self, request):
        """
        Get detailed customer statistics

        Returns:
        - Order statistics (total, completed, cancelled, average value)
        - Purchase behavior (items purchased, frequency)
        - Return behavior
        - Engagement metrics (wishlist, reviews, views)
        """
        try:
            stats_data = CustomerService.get_order_statistics(request.user)
            serializer = CustomerStatsSerializer(stats_data)

            return Response({"success": True, "data": serializer.data})

        except Exception as e:
            return Response(
                {"success": False, "message": _("Failed to load statistics"), "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @extend_schema(tags=["Customers"])
    @action(detail=False, methods=["get"])
    def insights(self, request):
        """
        Get spending insights and trends

        Returns:
        - Spending overview and trends
        - Monthly spending data (last 12 months)
        - Category and brand preferences
        - Shopping patterns
        - Discount usage
        """
        try:
            insights_data = CustomerService.get_spending_insights(request.user)
            serializer = CustomerInsightsSerializer(insights_data)

            return Response({"success": True, "data": serializer.data})

        except Exception as e:
            return Response(
                {"success": False, "message": _("Failed to load insights"), "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@extend_schema_view(
    lifetime_value=extend_schema(
        tags=["Customers"],
        summary=_("Get lifetime value metrics"),
        description=_(
            "Get detailed customer lifetime value metrics including current value, predicted LTV, value tier, engagement score, and churn risk analysis."
        ),
        responses=CustomerLifetimeValueSerializer,
    ),
    loyalty_status=extend_schema(
        tags=["Customers"],
        summary=_("Get loyalty status and benefits"),
        description=_(
            "Get customer loyalty program status including tier, points balance, rewards available, and tier benefits."
        ),
        responses=CustomerLoyaltyStatusSerializer,
    ),
    savings=extend_schema(
        tags=["Customers"],
        summary=_("Get savings history"),
        description=_(
            "Get customer savings history from vouchers, discounts, and promotional offers over time."
        ),
        responses=CustomerSavingsSerializer,
    ),
)
class CustomerAnalyticsViewSet(HeadlessAPIMixin, viewsets.ViewSet):
    """
    Customer Analytics ViewSet

    Provides customer-facing analytics endpoints

    Endpoints:
    - GET /api/customers/lifetime-value/ - Get lifetime value metrics
    - GET /api/customers/loyalty-status/ - Get loyalty status and benefits
    - GET /api/customers/savings/ - Get savings history
    """

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"], url_path="lifetime-value")
    def lifetime_value(self, request):
        """
        Get customer lifetime value metrics

        Returns:
        - Current value (revenue, orders, average order value)
        - Predicted LTV and confidence level
        - Value tier and percentile
        - Engagement score and churn risk
        - Customer timeline
        """
        try:
            ltv_data = CustomerService.get_lifetime_value(request.user)
            serializer = CustomerLifetimeValueSerializer(ltv_data)

            return Response({"success": True, "data": serializer.data})

        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": _("Failed to load lifetime value data"),
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"], url_path="loyalty-status")
    def loyalty_status(self, request):
        """
        Get customer loyalty status and benefits

        Returns:
        - Current segment and tier
        - Loyalty points
        - Current and next tier benefits
        - Progress to next tier
        - Membership statistics
        """
        try:
            loyalty_data = CustomerService.get_loyalty_status(request.user)
            serializer = CustomerLoyaltyStatusSerializer(loyalty_data)

            return Response({"success": True, "data": serializer.data})

        except Exception as e:
            return Response(
                {"success": False, "message": _("Failed to load loyalty status"), "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @extend_schema(tags=["Customers"])
    @action(detail=False, methods=["get"])
    def savings(self, request):
        """
        Get customer savings history

        Returns:
        - Total savings and breakdown
        - Recent savings (last 5 orders)
        - Monthly savings trends
        - Best savings month
        """
        try:
            savings_data = SavingsService.get_savings_summary(request.user)
            serializer = CustomerSavingsSerializer(savings_data)

            return Response({"success": True, "data": serializer.data})

        except Exception as e:
            return Response(
                {"success": False, "message": _("Failed to load savings data"), "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@extend_schema_view(
    favorites=extend_schema(
        tags=["Customers"],
        summary=_("Get favorite products"),
        description=_(
            "Get customer's favorite products including most purchased, favorite categories and brands, recently purchased, and wishlist summary."
        ),
        responses=CustomerFavoritesSerializer,
    ),
    recommendations=extend_schema(
        tags=["Customers"],
        summary=_("Get personalized recommendations"),
        description=_(
            "Get personalized product recommendations based on purchase history, trending in favorite categories, back in stock items, and sales."
        ),
        responses=CustomerRecommendationsSerializer,
    ),
)
class CustomerPreferencesViewSet(HeadlessAPIMixin, viewsets.ViewSet):
    """
    Customer Preferences ViewSet

    Provides customer-facing preferences and recommendations

    Endpoints:
    - GET /api/customers/favorites/ - Get favorite products
    - GET /api/customers/recommendations/ - Get personalized recommendations
    """

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def favorites(self, request):
        """
        Get customer's favorite products

        Returns:
        - Most purchased products
        - Favorite categories
        - Favorite brands
        - Recently purchased products
        - Wishlist summary
        """
        try:
            # Get favorite products
            most_purchased = RecommendationService.get_favorite_products(request.user, limit=10)

            # Get favorite categories
            favorite_categories = RecommendationService.get_favorite_categories(
                request.user, limit=5
            )

            # Get favorite brands
            favorite_brands = RecommendationService.get_favorite_brands(request.user, limit=5)

            # Get recently purchased
            recently_purchased = RecommendationService.get_recently_purchased(
                request.user, limit=10
            )

            # Get wishlist summary
            from cart.models import Wishlist

            wishlist = Wishlist.objects.filter(user=request.user).first()
            wishlist_count = wishlist.items.count() if wishlist else 0

            # Calculate wishlist value
            if wishlist:
                from django.db.models import F, Sum

                wishlist_value = (
                    wishlist.items.aggregate(total=Sum(F("product__price")))["total"] or 0
                )
            else:
                wishlist_value = 0

            favorites_data = {
                "most_purchased": most_purchased,
                "favorite_categories": favorite_categories,
                "favorite_brands": favorite_brands,
                "recently_purchased": recently_purchased,
                "wishlist_count": wishlist_count,
                "wishlist_value": wishlist_value,
            }

            serializer = CustomerFavoritesSerializer(favorites_data)

            return Response({"success": True, "data": serializer.data})

        except Exception as e:
            return Response(
                {"success": False, "message": _("Failed to load favorites"), "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"])
    def recommendations(self, request):
        """
        Get personalized product recommendations

        Returns:
        - Based on purchase history
        - Trending in favorite categories
        - Back in stock (from wishlist)
        - On sale (from favorite categories)
        """
        try:
            recommendations = RecommendationService.get_purchase_recommendations(request.user)

            serializer = CustomerRecommendationsSerializer(recommendations)

            return Response({"success": True, "data": serializer.data})

        except Exception as e:
            return Response(
                {"success": False, "message": _("Failed to load recommendations"), "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# ============================================================================
# Digital Products ViewSet (Customer-Facing)
# ============================================================================


@extend_schema_view(
    list=extend_schema(
        tags=["Customers"],
        summary=_("List purchased digital products"),
        description=_("""Get all digital products purchased by the authenticated customer.

        Returns complete information about each purchase including:
        - Product details and order information
        - Available digital assets for download
        - Software license keys
        - Download history and usage stats

        **Authentication**: Required - Customer must be logged in

        **Use Case**: Display customer's digital library with available downloads

        **Security**: Only shows products from completed/processing orders owned by the authenticated user
        """),
        responses={
            200: inline_serializer(
                name="DigitalProductsListResponse",
                fields={
                    "success": drf_serializers.BooleanField(default=True),
                    "count": drf_serializers.IntegerField(help_text="Number of digital products"),
                    "data": drf_serializers.ListField(
                        child=drf_serializers.JSONField(),
                        help_text="Array of digital products with order, product, digital_assets, license_keys, downloads",
                    ),
                },
            ),
            401: OpenApiResponse(description=AUTH_REQUIRED),
            500: OpenApiResponse(description=INTERNAL_SERVER_ERROR),
        },
    ),
    get_download_link=extend_schema(
        tags=["Customers"],
        summary=_("Generate download link"),
        description=_("""Generate a time-limited signed download URL for a purchased digital asset.

        Creates a secure, expiring download link that:
        - Expires after 1 hour for security
        - Validates customer ownership of the product
        - Enforces download limits if configured
        - Checks expiration date from purchase
        - Tracks download attempts for analytics

        **Authentication**: Required - Customer must own the digital product

        **Security**:
        - Signed URLs prevent unauthorized access
        - Download limits prevent abuse
        - Expiration dates enforce license terms
        - All downloads are logged for audit trail

        **Use Case**: Customer clicks "Download" button in their digital library

        **Example Response**:
        ```json
        {
          "success": true,
          "data": {
            "download_url": "https://example.com/download/abc123token",
            "expires_in_seconds": 3600,
            "filename": "software-pro-v1.0.zip",
            "file_size": "245.3 MB",
            "downloads_remaining": 5
          }
        }
        ```
        """),
        parameters=[
            OpenApiParameter(
                name="pk",
                type=int,
                location=OpenApiParameter.PATH,
                description=_("Digital Asset ID to download"),
                required=True,
            ),
        ],
        responses={
            200: inline_serializer(
                name="DownloadLinkResponse",
                fields={
                    "success": drf_serializers.BooleanField(default=True),
                    "data": inline_serializer(
                        name="DownloadLinkData",
                        fields={
                            "download_url": drf_serializers.URLField(
                                help_text="Signed download URL"
                            ),
                            "expires_in_seconds": drf_serializers.IntegerField(
                                help_text="Link expiration time"
                            ),
                            "filename": drf_serializers.CharField(help_text="Original filename"),
                            "file_size": drf_serializers.CharField(
                                help_text="Human-readable file size"
                            ),
                            "downloads_remaining": drf_serializers.IntegerField(
                                help_text="Remaining download count", allow_null=True
                            ),
                        },
                    ),
                },
            ),
            401: OpenApiResponse(description=AUTH_REQUIRED),
            403: OpenApiResponse(
                description=_(
                    "Access denied - customer doesn't own this product, download limit exceeded, or download expired"
                )
            ),
            404: OpenApiResponse(description=_("Digital asset not found")),
            500: OpenApiResponse(description=INTERNAL_SERVER_ERROR),
        },
    ),
    licenses=extend_schema(
        tags=["Customers"],
        summary=_("List customer license keys"),
        description=_("""Get all software license keys owned by the authenticated customer.

        Returns license keys with:
        - License key string (formatted with dashes)
        - Status (active, expired, revoked, suspended)
        - Activation limits and current usage
        - Associated product and asset
        - Device activation history
        - Expiration date if applicable

        **Authentication**: Required - Customer must be logged in

        **Use Case**: Display customer's license keys for software activation

        **Security**: Only shows licenses from completed orders owned by the authenticated user
        """),
        responses={
            200: inline_serializer(
                name="LicenseKeysListResponse",
                fields={
                    "success": drf_serializers.BooleanField(default=True),
                    "data": drf_serializers.ListField(
                        child=inline_serializer(
                            name="LicenseKeyItem",
                            fields={
                                "key": drf_serializers.CharField(
                                    help_text="Formatted license key (XXXX-XXXX-XXXX-XXXX)"
                                ),
                                "status": drf_serializers.CharField(
                                    help_text="License status: active, expired, revoked, suspended"
                                ),
                                "max_activations": drf_serializers.IntegerField(
                                    help_text="Maximum allowed activations"
                                ),
                                "current_activations": drf_serializers.IntegerField(
                                    help_text="Current activation count"
                                ),
                                "product": drf_serializers.CharField(help_text="Product name"),
                                "expires_at": drf_serializers.DateTimeField(
                                    help_text="Expiration date", allow_null=True
                                ),
                            },
                        )
                    ),
                },
            ),
            401: OpenApiResponse(description=AUTH_REQUIRED),
            500: OpenApiResponse(description=INTERNAL_SERVER_ERROR),
        },
    ),
    activate_license=extend_schema(
        tags=["Customers"],
        summary=_("Activate license on device"),
        description=_("""Activate a software license key on a specific device.

        Records device activation with:
        - Device fingerprint (unique identifier)
        - Device name and hardware info
        - Activation timestamp
        - IP address and user agent

        **Authentication**: Required - Customer must own the license key

        **Validation**:
        - Checks if license is active (not expired/revoked/suspended)
        - Enforces maximum activation limit
        - Prevents duplicate activations on same device
        - Validates device fingerprint format

        **Use Case**: Customer activates software on their computer/device

        **Security**:
        - Tracks all device activations
        - Enforces activation limits
        - Prevents license sharing abuse
        - Allows deactivation for device changes
        """),
        parameters=[
            OpenApiParameter(
                name="license_id",
                type=int,
                location=OpenApiParameter.PATH,
                description=_("License Key ID to activate"),
                required=True,
            ),
        ],
        request=inline_serializer(
            name="LicenseActivationRequest",
            fields={
                "device_fingerprint": drf_serializers.CharField(
                    required=True, help_text="Unique device identifier (hardware ID)"
                ),
                "device_name": drf_serializers.CharField(
                    required=True, help_text="User-friendly device name"
                ),
                "hardware_info": drf_serializers.JSONField(
                    required=False, help_text="Optional hardware specifications"
                ),
            },
        ),
        responses={
            200: inline_serializer(
                name="LicenseActivationResponse",
                fields={
                    "success": drf_serializers.BooleanField(default=True),
                    "message": drf_serializers.CharField(help_text="Status message"),
                    "activation_id": drf_serializers.IntegerField(
                        help_text="ID of the new activation record"
                    ),
                },
            ),
            400: OpenApiResponse(
                description=_("Invalid request - missing fields or activation limit reached")
            ),
            401: OpenApiResponse(description=AUTH_REQUIRED),
            403: OpenApiResponse(
                description=_("License is expired, revoked, or customer doesn't own it")
            ),
            404: OpenApiResponse(description=_("License key not found")),
            500: OpenApiResponse(description=INTERNAL_SERVER_ERROR),
        },
    ),
    deactivate_license=extend_schema(
        tags=["Customers"],
        summary=_("Deactivate license from device"),
        description=_("""Deactivate a software license key from a specific device.

        Removes device activation allowing:
        - Re-activation on different device
        - Freeing up activation slot
        - Device upgrade/replacement scenarios

        **Authentication**: Required - Customer must own the license key

        **Validation**:
        - Checks if license belongs to customer
        - Verifies device is currently activated
        - Matches device fingerprint for security

        **Use Case**: Customer upgrades computer or wants to move license to new device

        **Security**:
        - Requires device fingerprint to prevent unauthorized deactivation
        - Logs all deactivation events
        - Maintains audit trail
        """),
        parameters=[
            OpenApiParameter(
                name="license_id",
                type=int,
                location=OpenApiParameter.PATH,
                description=_("License Key ID to deactivate"),
                required=True,
            ),
        ],
        request=inline_serializer(
            name="LicenseDeactivationRequest",
            fields={
                "device_fingerprint": drf_serializers.CharField(
                    required=True, help_text="Device fingerprint to deactivate"
                ),
            },
        ),
        responses={
            200: inline_serializer(
                name="LicenseDeactivationResponse",
                fields={
                    "success": drf_serializers.BooleanField(default=True),
                    "message": drf_serializers.CharField(help_text="Status message"),
                },
            ),
            400: OpenApiResponse(description=_("Invalid request - missing device fingerprint")),
            401: OpenApiResponse(description=AUTH_REQUIRED),
            403: OpenApiResponse(description=_("Customer doesn't own this license")),
            404: OpenApiResponse(description=_("License key or activation not found")),
            500: OpenApiResponse(description=INTERNAL_SERVER_ERROR),
        },
    ),
)
class CustomerDigitalProductsViewSet(HeadlessAPIMixin, viewsets.ViewSet):
    """
    Customer Digital Products ViewSet

    Provides customer-facing endpoints for managing digital products,
    downloads, and software licenses.

    Endpoints:
    - GET /api/customers/digital-products/ - List all purchased digital products
    - GET /api/customers/digital-products/{id}/download/ - Get download link
    - GET /api/customers/digital-products/licenses/ - List all license keys
    - POST /api/customers/digital-products/licenses/{id}/activate/ - Activate license
    - POST /api/customers/digital-products/licenses/{id}/deactivate/ - Deactivate license
    """

    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        List all digital products purchased by the customer

        Returns:
        - Order items with digital products
        - Associated digital assets
        - License keys
        - Download history
        """
        try:
            from catalog.models import DigitalAsset, DigitalDownload, LicenseKey
            from orders.models import OrderItem

            from .serializers import CustomerDigitalProductSerializer

            # Get all order items for completed orders with digital products
            digital_order_items = (
                OrderItem.objects.filter(
                    order__user=request.user,
                    order__status__in=["processing", "completed", "delivered"],
                    product__is_digital=True,
                )
                .select_related("order", "product")
                .prefetch_related(
                    "digital_downloads__digital_asset",
                    "license_keys__digital_asset",
                    "license_keys__activations",
                )
                .order_by("-order__created_at")
            )

            # Build response data
            digital_products = []
            for item in digital_order_items:
                # Get digital assets for this product
                assets = DigitalAsset.objects.filter(product=item.product, is_active=True)

                # Get license keys for this purchase
                licenses = LicenseKey.objects.filter(order_item=item).prefetch_related(
                    "activations"
                )

                # Get download history
                downloads = (
                    DigitalDownload.objects.filter(order_item=item)
                    .select_related("digital_asset")
                    .order_by("-downloaded_at")
                )

                product_data = {
                    "order": item.order,
                    "product": item.product,
                    "digital_assets": assets,
                    "license_keys": licenses,
                    "digital_downloads": downloads,
                }

                digital_products.append(product_data)

            serializer = CustomerDigitalProductSerializer(digital_products, many=True)

            return Response(
                {"success": True, "count": len(digital_products), "data": serializer.data}
            )

        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": _("Failed to load digital products"),
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["get"], url_path="download")
    def get_download_link(self, request, pk=None):
        """
        Generate a time-limited download link for a digital asset

        Args:
            pk: DigitalAsset ID

        Returns:
            Signed download URL with expiration
        """
        try:
            from catalog.download_views import generate_download_token
            from catalog.models import DigitalAsset
            from orders.models import OrderItem

            from .serializers import DownloadLinkSerializer

            # Get the digital asset
            asset = get_object_or_404(DigitalAsset, pk=pk, is_active=True)

            # Verify customer owns this asset (purchased it)
            order_item = OrderItem.objects.filter(
                order__user=request.user,
                order__status__in=["processing", "completed", "delivered"],
                product=asset.product,
            ).first()

            if not order_item:
                return Response(
                    {
                        "success": False,
                        "message": _("You do not have access to this digital product"),
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Check download limit
            if asset.is_download_limit_exceeded(order_item):
                return Response(
                    {"success": False, "message": _("Download limit exceeded for this product")},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Check expiration
            if asset.is_download_expired(order_item.order.created_at):
                return Response(
                    {"success": False, "message": _("Download link has expired")},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Generate signed download token (1 hour expiration)
            token = generate_download_token(asset.id, order_item.id)

            # Build download URL
            download_url = request.build_absolute_uri(
                reverse("digital_download", kwargs={"token": token})
            )

            # Calculate downloads remaining
            download_count = asset.downloads.filter(order_item=order_item).count()
            downloads_remaining = None
            if asset.download_limit:
                downloads_remaining = asset.download_limit - download_count

            response_data = {
                "download_url": download_url,
                "expires_in_seconds": 3600,
                "filename": asset.filename,
                "file_size": asset.get_file_size_display(),
                "downloads_remaining": downloads_remaining,
            }

            serializer = DownloadLinkSerializer(response_data)

            return Response({"success": True, "data": serializer.data})

        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": _("Failed to generate download link"),
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"])
    def licenses(self, request):
        """
        List all license keys owned by the customer

        Returns:
        - All license keys with activation status
        - Active devices
        - License validity information
        """
        try:
            from catalog.models import LicenseKey

            from .serializers import LicenseActivationSerializer, LicenseKeySerializer

            # Get all license keys for this customer
            licenses = (
                LicenseKey.objects.filter(user=request.user)
                .prefetch_related("activations")
                .order_by("-issued_at")
            )

            license_data = []
            for license in licenses:
                # Get active activations
                active_activations = license.activations.filter(is_active=True)

                license_info = {
                    "license": license,
                    "active_devices": active_activations,
                }

                license_data.append(license_info)

            serializer = LicenseKeySerializer(licenses, many=True)

            # Include activation details in response
            response_data = serializer.data
            for i, license in enumerate(licenses):
                active_devices = license.activations.filter(is_active=True)
                response_data[i]["active_devices"] = LicenseActivationSerializer(
                    active_devices, many=True
                ).data

            return Response({"success": True, "count": len(licenses), "data": response_data})

        except Exception as e:
            return Response(
                {"success": False, "message": _("Failed to load license keys"), "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["post"], url_path="licenses/(?P<license_id>[^/.]+)/activate")
    def activate_license(self, request, pk=None, license_id=None):
        """
        Activate a license key on a device

        Request Body:
        {
            "device_identifier": "unique-device-id",
            "device_name": "John's MacBook Pro",
            "device_info": {"os": "macOS", "version": "14.0"}
        }
        """
        try:
            from catalog.models import LicenseKey

            from .serializers import LicenseActivationRequestSerializer, LicenseActivationSerializer

            # Validate request data
            serializer = LicenseActivationRequestSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {
                        "success": False,
                        "message": _("Invalid request data"),
                        "errors": serializer.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Get license key
            license_key = get_object_or_404(LicenseKey, pk=license_id, user=request.user)

            # Activate license
            activation = license_key.activate(
                device_identifier=serializer.validated_data["device_identifier"],
                device_name=serializer.validated_data.get("device_name", ""),
                ip_address=self._get_client_ip(request),
            )

            # Update device info if provided
            if "device_info" in serializer.validated_data:
                activation.update_device_info(**serializer.validated_data["device_info"])

            activation_serializer = LicenseActivationSerializer(activation)

            return Response(
                {
                    "success": True,
                    "message": _("License activated successfully"),
                    "data": activation_serializer.data,
                }
            )

        except ValueError as e:
            return Response(
                {"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"success": False, "message": _("Failed to activate license"), "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["post"], url_path="licenses/(?P<license_id>[^/.]+)/deactivate")
    def deactivate_license(self, request, pk=None, license_id=None):
        """
        Deactivate a license key from a device

        Request Body:
        {
            "device_identifier": "unique-device-id"
        }
        """
        try:
            from catalog.models import LicenseKey

            # Get device identifier from request
            device_identifier = request.data.get("device_identifier")
            if not device_identifier:
                return Response(
                    {"success": False, "message": _("device_identifier is required")},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Get license key
            license_key = get_object_or_404(LicenseKey, pk=license_id, user=request.user)

            # Deactivate license
            success = license_key.deactivate(device_identifier)

            if not success:
                return Response(
                    {"success": False, "message": _("Device not found or already deactivated")},
                    status=status.HTTP_404_NOT_FOUND,
                )

            return Response(
                {
                    "success": True,
                    "message": _("License deactivated successfully"),
                    "activations_remaining": license_key.activations_remaining,
                }
            )

        except Exception as e:
            return Response(
                {"success": False, "message": _("Failed to deactivate license"), "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def _get_client_ip(self, request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        ip = x_forwarded_for.split(",")[0] if x_forwarded_for else request.META.get("REMOTE_ADDR")
        return ip


@staff_member_required
def add_customer_note(request):
    """
    AJAX endpoint for adding customer notes from the admin change form
    """
    if request.method != "POST":
        return JsonResponse({"success": False, "message": _("Invalid request method")}, status=405)

    try:
        customer_id = request.POST.get("customer_id")
        note_type = request.POST.get("note_type")
        title = request.POST.get("title")
        content = request.POST.get("content")
        requires_follow_up = request.POST.get("requires_follow_up") == "on"

        # Get customer profile
        customer_profile = get_object_or_404(CustomerProfile, pk=customer_id)

        # Create note
        note = CustomerNote.objects.create(
            customer=customer_profile.user,
            created_by=request.user,
            note_type=note_type,
            title=title,
            content=content,
            requires_follow_up=requires_follow_up,
        )

        return JsonResponse(
            {"success": True, "message": _("Note added successfully"), "note_id": note.pk}
        )

    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@staff_member_required
def customer_profile_actions(request, object_id):
    """
    Handle custom actions for customer profiles
    - refresh_metrics: Refresh customer metrics
    - export: Export customer data
    - convert_to_affiliate: Convert customer to affiliate
    """
    customer_profile = get_object_or_404(CustomerProfile, pk=object_id)
    action = request.GET.get("action") or request.POST.get("action")

    if action == "refresh_metrics":
        try:
            # Refresh metrics
            metrics, created = CustomerMetrics.objects.get_or_create(user=customer_profile.user)
            CustomerMetrics.calculate_for_user(customer_profile.user)

            return JsonResponse({"success": True, "message": _("Metrics refreshed successfully")})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    elif action == "export":
        # Export customer data to CSV
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            f'attachment; filename="customer_{customer_profile.user.username}.csv"'
        )

        writer = csv.writer(response)
        writer.writerow(["Field", "Value"])
        writer.writerow(["Username", customer_profile.user.username])
        writer.writerow(["Email", customer_profile.user.email])
        writer.writerow(["Name", customer_profile.user.get_full_name()])
        writer.writerow(["Phone", customer_profile.phone or ""])
        writer.writerow(["Total Orders", customer_profile.total_orders])
        writer.writerow(["Total Spent", customer_profile.total_spent])
        writer.writerow(["Average Order Value", customer_profile.average_order_value])
        writer.writerow(["VIP Status", "Yes" if customer_profile.is_vip_customer else "No"])
        writer.writerow(
            [
                "Customer Segment",
                customer_profile.customer_segment.display_name
                if customer_profile.customer_segment
                else "None",
            ]
        )
        writer.writerow(["Registration Date", customer_profile.created_at.strftime("%Y-%m-%d")])

        return response

    elif action == "convert_to_affiliate":
        try:
            from affiliate.models import Affiliate

            # Check if already an affiliate
            if hasattr(customer_profile.user, "affiliate_profile"):
                return JsonResponse(
                    {"success": False, "message": _("Customer is already an affiliate")}, status=400
                )

            # Create affiliate profile
            affiliate = Affiliate.objects.create(
                user=customer_profile.user,
                payment_email=customer_profile.user.email,
                payment_method="paypal",
                status="active",  # Set to active since merchant is manually converting them
            )

            return JsonResponse(
                {
                    "success": True,
                    "message": _("Customer converted to affiliate successfully"),
                    "redirect": f"/admin/affiliate/affiliate/{affiliate.pk}/change/",
                }
            )
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    elif action == "send_account_invitation":
        try:
            # Check if user is a guest
            if not customer_profile.is_guest_user:
                return JsonResponse(
                    {"success": False, "message": _("Customer already has a registered account")},
                    status=400,
                )

            # Check if user has an email
            if not customer_profile.user.email:
                return JsonResponse(
                    {
                        "success": False,
                        "message": _("Guest customer does not have an email address"),
                    },
                    status=400,
                )

            # Send the invitation email
            from django.contrib.auth.tokens import default_token_generator
            from django.utils.encoding import force_bytes
            from django.utils.http import urlsafe_base64_encode

            from email_system.services.email_sender import EmailSendingService

            # Generate password reset token
            token = default_token_generator.make_token(customer_profile.user)
            uid = urlsafe_base64_encode(force_bytes(customer_profile.user.pk))

            # Calculate total spent for context
            total_spent = customer_profile.total_spent

            context = {
                "customer_name": customer_profile.user.get_full_name()
                or customer_profile.user.email,
                "customer_email": customer_profile.user.email,
                "total_orders": customer_profile.total_orders,
                "total_spent": total_spent,
                "activation_url": request.build_absolute_uri(
                    f"/accounts/activate-guest/{uid}/{token}/"
                ),
                "site_name": request.get_host(),
            }

            # Queue email using email system
            from email_system.utils.language import get_user_email_language

            outbox = EmailSendingService.send_template_email(
                template_type="account_invitation",
                to_email=customer_profile.user.email,
                context=context,
                language=get_user_email_language(customer_profile.user),
            )

            # Send the queued email immediately
            if outbox and outbox.status == "queued":
                success = EmailSendingService.send_email(str(outbox.id))

                if success:
                    return JsonResponse(
                        {
                            "success": True,
                            "message": _("Account invitation sent to {}").format(
                                customer_profile.user.email
                            ),
                        }
                    )
                else:
                    return JsonResponse(
                        {"success": False, "message": _("Failed to send invitation email")},
                        status=500,
                    )
            else:
                return JsonResponse(
                    {
                        "success": False,
                        "message": _(
                            "Email could not be sent — template may be missing or email preferences blocked delivery"
                        ),
                    },
                    status=500,
                )

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    return JsonResponse({"success": False, "message": _("Invalid action")}, status=400)


@require_http_methods(["POST"])
@staff_member_required
def set_address_default(request, address_id):
    """
    AJAX endpoint to set an address as default.
    Admin-only endpoint for setting customer addresses as default.
    """
    from orders.models import Address
    from orders.services.address_service import AddressService

    try:
        address = Address.objects.get(pk=address_id)

        # Set as default
        success, message = AddressService.set_default_address(address=address, user=address.user)

        if success:
            return JsonResponse({"success": True, "message": _("Address set as default")})
        else:
            return JsonResponse({"success": False, "message": message}, status=400)

    except Address.DoesNotExist:
        return JsonResponse({"success": False, "message": _("Address not found")}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


# ============================================================================
# LTV (Lifetime Value) Admin Views
# ============================================================================


@staff_member_required
def ltv_settings(request):
    """
    LTV Settings Admin View

    Allows merchants to:
    - Select LTV calculation method (simple/cohort/probabilistic)
    - Configure discount rate and thresholds
    - View data quality recommendations
    - Trigger immediate recalculation
    - View last calculation timestamp
    """
    settings = LTVSettings.get_settings()

    # Handle form submission
    if request.method == "POST":
        try:
            # Update settings
            settings.calculation_method = request.POST.get("calculation_method", "simple")
            settings.default_discount_rate = request.POST.get("default_discount_rate", "0.10")
            settings.min_data_quality_threshold = int(
                request.POST.get("min_data_quality_threshold", 100)
            )
            settings.save()

            # Check if immediate recalculation was requested
            if request.POST.get("trigger_recalculation") == "true":
                from .tasks import calculate_all_customer_ltv_task

                task = calculate_all_customer_ltv_task.delay()

                return JsonResponse(
                    {
                        "success": True,
                        "message": _("Settings saved and LTV calculation started"),
                        "task_id": task.id,
                    }
                )

            return JsonResponse({"success": True, "message": _("Settings saved successfully")})

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    # Check data quality for probabilistic method
    data_quality = ProbabilisticLTVService.check_data_quality()

    # Get customer counts
    total_customers = CustomerMetrics.objects.filter(completed_orders__gte=1).count()
    repeat_customers = CustomerMetrics.objects.filter(completed_orders__gte=2).count()

    # Get cohort stats
    cohort_count = CustomerCohort.objects.count()

    # Category multipliers
    category_multipliers = ProductCategoryLTVMultiplier.objects.all()

    context = {
        "title": _("LTV Settings"),
        "settings": settings,
        "data_quality": data_quality,
        "total_customers": total_customers,
        "repeat_customers": repeat_customers,
        "cohort_count": cohort_count,
        "category_multipliers": category_multipliers,
        "calculation_methods": LTVSettings.CALCULATION_METHODS,
    }

    return render(request, "customers/ltv_settings.html", context)


@staff_member_required
def cohort_dashboard(request):
    """
    Deprecated: Redirects to the main dashboard's cohort tab.
    Cohort analytics are now integrated into the unified dashboard.
    """
    return redirect(reverse("customers:dashboard") + "?tab=cohorts")


@staff_member_required
def recalculate_ltv(request):
    """
    AJAX endpoint to trigger LTV recalculation

    Query Parameters:
    - scope: 'all' or specific user_id
    - method: Force specific method (optional)
    - async: 'true' to run via Celery (default), 'false' for synchronous
    """
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        scope = request.POST.get("scope", "all")
        use_async = request.POST.get("async", "true") == "true"

        if scope == "all":
            # Recalculate for all customers
            if use_async:
                from .tasks import calculate_all_customer_ltv_task

                task = calculate_all_customer_ltv_task.delay()

                return JsonResponse(
                    {
                        "success": True,
                        "message": _("LTV calculation task queued"),
                        "task_id": task.id,
                        "async": True,
                    }
                )
            else:
                # Synchronous calculation (not recommended for production)
                from .services.probabilistic_ltv_service import ProbabilisticLTVService

                settings = LTVSettings.get_settings()

                if settings.calculation_method == "simple":
                    updated = 0
                    for user in User.objects.filter(is_active=True).exclude(
                        username__startswith="guest_"
                    ):
                        CustomerMetrics.calculate_for_user(user)
                        updated += 1

                    return JsonResponse(
                        {
                            "success": True,
                            "message": _("Updated %(count)s customers") % {"count": updated},
                            "customers_updated": updated,
                        }
                    )

                elif settings.calculation_method == "cohort":
                    CohortService.build_all_cohorts()
                    CohortService.calculate_cohort_metrics()
                    result = CohortService.update_customer_cohort_ltv()

                    return JsonResponse(
                        {
                            "success": True,
                            "message": _("Cohort calculation completed"),
                            "customers_updated": result.get("customers_updated", 0),
                        }
                    )

                elif settings.calculation_method == "probabilistic":
                    service = ProbabilisticLTVService()
                    result = service.update_all_customer_ltv()

                    if result["success"]:
                        return JsonResponse(
                            {
                                "success": True,
                                "message": _("Probabilistic calculation completed"),
                                "customers_updated": result["customers_updated"],
                                "customers_failed": result["customers_failed"],
                            }
                        )
                    else:
                        return JsonResponse(
                            {
                                "success": False,
                                "message": result.get("error", "Calculation failed"),
                            },
                            status=500,
                        )

        else:
            # Recalculate for specific user
            user_id = int(scope)
            user = get_object_or_404(User, id=user_id)

            if use_async:
                from .tasks import calculate_customer_ltv_task

                task = calculate_customer_ltv_task.delay(user_id)

                return JsonResponse(
                    {
                        "success": True,
                        "message": _("LTV calculation task queued for user"),
                        "task_id": task.id,
                        "async": True,
                    }
                )
            else:
                CustomerMetrics.calculate_for_user(user)
                metrics = CustomerMetrics.objects.get(user=user)

                return JsonResponse(
                    {
                        "success": True,
                        "message": _("LTV updated successfully"),
                        "lifetime_value": str(metrics.lifetime_value),
                        "confidence": metrics.ltv_confidence_score,
                    }
                )

    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@staff_member_required
def cohort_data_api(request):
    """
    API endpoint for cohort dashboard charts

    Returns JSON data for:
    - Cohort retention curves
    - LTV by cohort
    - Customer counts by cohort
    """
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    try:
        cohort_id = request.GET.get("cohort_id")

        if cohort_id:
            # Get specific cohort data
            cohort = get_object_or_404(CustomerCohort, id=cohort_id)
            retention_curve = CohortService.get_cohort_retention_curve(cohort_id)

            return JsonResponse(
                {
                    "success": True,
                    "cohort": {
                        "id": cohort.id,
                        "name": str(cohort),
                        "cohort_month": cohort.cohort_date.strftime("%Y-%m"),
                        "customer_count": cohort.customer_count,
                        "total_revenue": float(cohort.total_revenue.amount)
                        if cohort.total_revenue
                        else 0,
                        "average_ltv": float(cohort.average_ltv.amount)
                        if cohort.average_ltv
                        else 0,
                    },
                    "retention_curve": retention_curve,
                }
            )
        else:
            # Get comparison data for all recent cohorts
            comparison_data = CohortService.get_cohort_comparison(limit=12)

            # Format for chart display
            labels = [c["cohort_date"] for c in comparison_data]
            customer_counts = [c["customer_count"] for c in comparison_data]
            ltv_values = [c["average_ltv"] for c in comparison_data]
            retention_rates = [c["retention_rate"] for c in comparison_data]

            # Get retention heatmap data and insights
            heatmap_data = CohortService.get_retention_heatmap_data(limit=12)
            retention_insights = CohortService.get_retention_insights()

            # Get LTV by channel data and insights
            channel_data = CohortService.get_ltv_by_channel()
            channel_insights = CohortService.get_channel_insights()

            # Get LTV by first category data and insights
            category_data = CohortService.get_ltv_by_category()
            category_insights = CohortService.get_category_insights()

            # Get cumulative revenue curve data and insights
            revenue_curve_data = CohortService.get_cumulative_revenue_curve(limit=6)
            revenue_curve_insights = CohortService.get_revenue_curve_insights()

            return JsonResponse(
                {
                    "success": True,
                    "labels": labels,
                    "datasets": {
                        "customer_counts": customer_counts,
                        "ltv_values": ltv_values,
                        "retention_rates": retention_rates,
                    },
                    "comparison_data": comparison_data,
                    # New: Retention heatmap data
                    "heatmap_data": {
                        "cohorts": heatmap_data["cohorts"],
                        "months": heatmap_data["months"],
                        "data": heatmap_data["data"],
                    },
                    "retention_insights": retention_insights,
                    # New: LTV by channel
                    "channel_data": channel_data,
                    "channel_insights": channel_insights,
                    # New: LTV by first category
                    "category_data": category_data,
                    "category_insights": category_insights,
                    # New: Cumulative revenue curves
                    "revenue_curve_data": revenue_curve_data,
                    "revenue_curve_insights": revenue_curve_insights,
                }
            )

    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)
