"""
URL configuration for referrals admin views.

These URLs are for admin-only views (dashboard, filters, actions).
They are included with language prefix in core/urls.py.
"""

from django.urls import path

from . import views

app_name = "referrals"

urlpatterns = [
    # Dashboard
    path("dashboard/", views.referral_dashboard, name="dashboard"),
    # AJAX Filter Endpoints
    path("referrers/filter/", views.filter_referrers, name="filter_referrers"),
    path("attributions/filter/", views.filter_attributions, name="filter_attributions"),
    path("rewards/filter/", views.filter_rewards, name="filter_rewards"),
    path("events/filter/", views.filter_events, name="filter_events"),
    # Admin Action Endpoints
    path("attributions/<int:pk>/approve/", views.approve_attribution, name="approve_attribution"),
    path("attributions/<int:pk>/reject/", views.reject_attribution, name="reject_attribution"),
    path("rewards/<int:pk>/issue/", views.issue_reward_view, name="issue_reward"),
    path("rewards/<int:pk>/revoke/", views.revoke_reward_view, name="revoke_reward"),
]
