"""
URL configuration for referrals API views.

These URLs are for public API endpoints (no language prefix).
They are included directly in core/urls.py outside i18n_patterns.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views, views_drf

# Create router for DRF viewsets
router = DefaultRouter()
router.register(r"program", views_drf.ReferralProgramViewSet, basename="program")
router.register(r"identities", views_drf.ReferralIdentityViewSet, basename="identity")
router.register(r"events", views_drf.ReferralEventViewSet, basename="event")
router.register(r"attributions", views_drf.ReferralAttributionViewSet, basename="attribution")
router.register(r"rewards", views_drf.ReferralRewardViewSet, basename="reward")

app_name = "referrals_api"

urlpatterns = [
    # Legacy public API endpoints (backward compatibility)
    path("click/", views.track_click_api, name="track_click"),
    path("me/", views.referrer_dashboard_data, name="referrer_data"),
    # DRF router URLs
    path("", include(router.urls)),
]
