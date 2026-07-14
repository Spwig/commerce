"""
API URL configuration for accounts app.
All API endpoints are consolidated here to be included outside i18n_patterns.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import api_views

app_name = "accounts_api"

# Create router for viewsets
router = DefaultRouter()
router.register(r"addresses", api_views.AddressViewSet, basename="address")

# API URL patterns
urlpatterns = [
    # Authentication endpoints
    path("register/", api_views.register, name="register"),
    path("login/", api_views.user_login, name="login"),
    path("logout/", api_views.user_logout, name="logout"),
    # Password reset endpoints
    path("password-reset/", api_views.password_reset_request, name="password_reset"),
    path(
        "password-reset-confirm/<str:uidb64>/<str:token>/",
        api_views.password_reset_confirm,
        name="password_reset_confirm",
    ),
    # Profile endpoints
    path("profile/", api_views.get_profile, name="profile_get"),
    path("profile/update/", api_views.update_profile, name="profile_update"),
    path("preferences/", api_views.update_preferences, name="preferences"),
    path("refresh-metrics/", api_views.refresh_metrics, name="refresh_metrics"),
    # Communication preferences
    path(
        "communication-preferences/",
        api_views.get_communication_preferences,
        name="communication_preferences_get",
    ),
    path(
        "communication-preferences/update/",
        api_views.update_communication_preference,
        name="communication_preference_update",
    ),
    path(
        "communication-preferences/bulk-update/",
        api_views.bulk_update_communication_preferences,
        name="communication_preferences_bulk_update",
    ),
    path(
        "communication-preferences/unsubscribe-all/",
        api_views.unsubscribe_all_communications,
        name="unsubscribe_all",
    ),
    # SMS Verification (TCPA double opt-in)
    path("sms/send-verification/", api_views.send_sms_verification, name="sms_send_verification"),
    path("sms/verify/", api_views.verify_sms_code, name="sms_verify"),
    path("sms/resend/", api_views.resend_sms_verification, name="sms_resend"),
    # Export Preferences (GDPR Article 15)
    path("preferences/export/", api_views.export_preferences, name="export_preferences"),
    # Address management (router-based)
    path("", include(router.urls)),
    # Social authentication endpoints
    path("social/providers/", api_views.available_social_providers, name="social_providers"),
    # Guest account conversion endpoints
    path("convert-guest/", api_views.convert_guest_to_account, name="convert_guest"),
    path("creation-context/", api_views.account_creation_context, name="creation_context"),
]
