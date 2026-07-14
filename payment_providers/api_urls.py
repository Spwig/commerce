"""
Payment Orchestration API URLs

Public API endpoints for payment orchestration.
These endpoints are used by headless frontends to initiate and manage payments.

All endpoints are under /api/payments/ (non-i18n, no language prefix).
"""

from django.urls import path

from payment_providers import api_views

app_name = "payments_api"

urlpatterns = [
    # Payment Intents (public - customer facing)
    path("intents/", api_views.PaymentIntentCreateView.as_view(), name="intent-create"),
    path(
        "intents/<uuid:intent_id>/",
        api_views.PaymentIntentDetailView.as_view(),
        name="intent-detail",
    ),
    path(
        "intents/<uuid:intent_id>/confirm/",
        api_views.PaymentIntentConfirmView.as_view(),
        name="intent-confirm",
    ),
    path(
        "intents/<uuid:intent_id>/cancel/",
        api_views.PaymentIntentCancelView.as_view(),
        name="intent-cancel",
    ),
    # Saved Payment Methods (authenticated users only)
    path("methods/", api_views.SavedMethodListCreateView.as_view(), name="methods-list"),
    path(
        "methods/<uuid:method_id>/", api_views.SavedMethodDetailView.as_view(), name="method-detail"
    ),
    path(
        "methods/<uuid:method_id>/set-default/",
        api_views.SetDefaultMethodView.as_view(),
        name="method-set-default",
    ),
    # SDK failure reporting (frontend -> merchant notification)
    path(
        "report-sdk-failure/",
        api_views.PaymentSDKFailureReportView.as_view(),
        name="report-sdk-failure",
    ),
]
