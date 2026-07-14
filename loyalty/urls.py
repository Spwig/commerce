"""
Loyalty Program URL Configuration
"""

from django.urls import path

from loyalty import views
from loyalty.views import analytics

app_name = "loyalty"

urlpatterns = [
    # Admin Dashboard
    path("dashboard/", views.loyalty_dashboard, name="dashboard"),
    # Campaign Wizard
    path("campaigns/wizard/", views.campaign_wizard, name="campaign_wizard"),
    # Admin Analytics
    path("analytics/", analytics.analytics_dashboard, name="analytics_dashboard"),
    path(
        "analytics/campaign/<int:campaign_id>/",
        analytics.campaign_analytics,
        name="campaign_analytics",
    ),
    path(
        "analytics/campaign/<int:campaign_id>/export/",
        analytics.export_campaign_report,
        name="export_campaign_report",
    ),
    path("analytics/members/", analytics.member_analytics, name="member_analytics"),
    # Admin AJAX Endpoints
    path("members/filter/", views.filter_members, name="filter_members"),
    path("transactions/filter/", views.filter_transactions, name="filter_transactions"),
    path("rewards/filter/", views.filter_rewards, name="filter_rewards"),
    path("redemptions/filter/", views.filter_redemptions, name="filter_redemptions"),
    path("tiers/filter/", views.filter_tiers, name="filter_tiers"),
    path("badges/filter/", views.filter_badges, name="filter_badges"),
    path("rules/filter/", views.filter_rules, name="filter_rules"),
    path("rules/<int:rule_id>/activate/", views.toggle_rule_status, name="activate_rule"),
    path("rules/<int:rule_id>/deactivate/", views.toggle_rule_status, name="deactivate_rule"),
    path("segments/filter/", views.filter_segments, name="filter_segments"),
    path("segments/<int:segment_id>/refresh/", views.refresh_segment, name="refresh_segment"),
    path("campaigns/filter/", views.filter_campaigns, name="filter_campaigns"),
    path(
        "campaigns/<int:campaign_id>/activate/",
        views.toggle_campaign_status,
        name="activate_campaign",
    ),
    path(
        "campaigns/<int:campaign_id>/deactivate/",
        views.toggle_campaign_status,
        name="deactivate_campaign",
    ),
    # Customer-Facing URLs
    path("account/", views.customer_dashboard, name="customer_dashboard"),
    path("account/history/", views.customer_transaction_history, name="customer_history"),
    path("account/rewards/", views.customer_rewards_catalog, name="customer_rewards"),
    path(
        "account/rewards/<int:reward_id>/redeem/",
        views.customer_redeem_reward,
        name="customer_redeem",
    ),
    path(
        "account/redemptions/<int:redemption_id>/",
        views.customer_redemption_detail,
        name="customer_redemption_detail",
    ),
    path("account/tiers/", views.customer_tier_info, name="customer_tiers"),
    path("account/badges/", views.customer_badges, name="customer_badges"),
]
