"""
Loyalty Program API URL Configuration

Customer-facing API endpoints for the loyalty program.
Accessed via /api/loyalty/
"""

from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

# No app_name to avoid namespace conflicts

# ViewSet-based routes
router = DefaultRouter()
router.register(r"tiers", views.LoyaltyTierViewSet, basename="loyalty-tier")
router.register(r"rewards", views.LoyaltyRewardViewSet, basename="loyalty-reward")
router.register(r"redemptions", views.LoyaltyRedemptionViewSet, basename="loyalty-redemption")

urlpatterns = [
    # Status & Progress
    path("status/", views.LoyaltyStatusViewSet.as_view({"get": "list"}), name="loyalty-status"),
    path(
        "progress/",
        views.LoyaltyStatusViewSet.as_view({"get": "progress"}),
        name="loyalty-progress",
    ),
    # Transaction History
    path("history/", views.LoyaltyHistoryViewSet.as_view({"get": "list"}), name="loyalty-history"),
    # Badges
    path("badges/", views.LoyaltyBadgeViewSet.as_view({"get": "list"}), name="loyalty-badges"),
    path(
        "badges/available/",
        views.LoyaltyBadgeViewSet.as_view({"get": "available"}),
        name="loyalty-badges-available",
    ),
    # Earning Rules
    path(
        "earning-rules/",
        views.LoyaltyEarningRulesViewSet.as_view({"get": "list"}),
        name="loyalty-earning-rules",
    ),
]

# Add router URLs
urlpatterns += router.urls
