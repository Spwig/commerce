"""
Payout Provider Webhook URLs

Webhook endpoints for PayPal, Airwallex etc.
These must be outside i18n_patterns (external services don't use language prefixes).
"""

from django.urls import path

from . import views

app_name = "payout_webhooks"

urlpatterns = [
    path("paypal/", views.paypal_webhook, name="webhook_paypal"),
    path("airwallex/", views.airwallex_webhook, name="webhook_airwallex"),
]
