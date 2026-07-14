"""
Affiliate App URL Configuration
Defines URL patterns for affiliate portal, merchant dashboard, and tracking
Note: API URLs are in api_urls.py and should be included without language prefix
"""

from django.urls import include, path

from . import views

app_name = "affiliate"

# Merchant URLs (merchant dashboard)
merchant_patterns = [
    path("", views.MerchantDashboardView.as_view(), name="merchant_dashboard"),
    path("programs/", views.ProgramListView.as_view(), name="program_list"),
    path("programs/<int:pk>/", views.ProgramDetailView.as_view(), name="program_detail"),
    path(
        "programs/<int:program_id>/affiliates/",
        views.ProgramAffiliatesView.as_view(),
        name="program_affiliates",
    ),
    path("applications/", views.ProgramApplicationsView.as_view(), name="program_applications"),
]

# Affiliate Portal URLs
portal_patterns = [
    path("", views.AffiliatePortalView.as_view(), name="portal"),
    path("dashboard/", views.AffiliateDashboardView.as_view(), name="dashboard"),
    path("links/", views.AffiliateLinksView.as_view(), name="links"),
    path("commissions/", views.AffiliateCommissionsView.as_view(), name="commissions"),
    path("payouts/", views.AffiliatePayoutsView.as_view(), name="payouts"),
    path("programs/", views.AffiliateProgramsView.as_view(), name="programs"),
]

# Tracking URLs (public, no auth required)
tracking_patterns = [
    path("<str:link_code>/", views.TrackingRedirectView.as_view(), name="track"),
    path("postback/", views.ConversionPostbackView.as_view(), name="postback"),
]

# Main URL patterns
urlpatterns = [
    # Admin Wizard
    path("programs/wizard/", views.program_wizard, name="program_wizard"),
    # Admin AJAX Endpoints - Programs
    path("programs/filter/", views.filter_programs, name="filter_programs"),
    path(
        "programs/<int:program_id>/activate/", views.toggle_program_status, name="activate_program"
    ),
    path("programs/<int:program_id>/pause/", views.toggle_program_status, name="pause_program"),
    path(
        "programs/<int:program_id>/archived/",
        views.update_program_status,
        {"new_status": "archived"},
        name="archive_program",
    ),
    path(
        "programs/<int:program_id>/active/",
        views.update_program_status,
        {"new_status": "active"},
        name="activate_program_status",
    ),
    path(
        "programs/<int:program_id>/paused/",
        views.update_program_status,
        {"new_status": "paused"},
        name="pause_program_status",
    ),
    path(
        "programs/<int:program_id>/members/filter/",
        views.filter_program_members,
        name="filter_program_members",
    ),
    # Admin AJAX Endpoints - Affiliates
    path("affiliates/filter/", views.filter_affiliates, name="filter_affiliates"),
    path(
        "affiliates/<int:affiliate_id>/approve/",
        views.toggle_affiliate_status,
        name="approve_affiliate",
    ),
    path(
        "affiliates/<int:affiliate_id>/suspend/",
        views.toggle_affiliate_status,
        name="suspend_affiliate",
    ),
    path(
        "affiliates/<int:affiliate_id>/activate/",
        views.toggle_affiliate_status,
        name="activate_affiliate",
    ),
    # Admin AJAX Endpoints - Payouts
    path("admin/payouts/filter/", views.filter_payouts, name="filter_payouts"),
    # Admin AJAX Endpoints - Memberships
    path("memberships/filter/", views.filter_memberships, name="filter_memberships"),
    path(
        "memberships/<int:membership_id>/approve/",
        views.toggle_membership_status,
        name="approve_membership",
    ),
    path(
        "memberships/<int:membership_id>/reject/",
        views.toggle_membership_status,
        name="reject_membership",
    ),
    # Template views
    path("", views.AffiliatePortalView.as_view(), name="index"),
    path("merchant/", include(merchant_patterns)),
    path("portal/", include(portal_patterns)),
    path("t/", include(tracking_patterns)),  # Short URL for tracking links
    # Note: API endpoints moved to api_urls.py and included in core/urls.py without language prefix
]
