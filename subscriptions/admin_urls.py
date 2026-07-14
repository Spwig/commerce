"""
Admin URLs for subscription AJAX endpoints
"""

from django.urls import path

from . import admin_views

app_name = "subscriptions"

urlpatterns = [
    path("plans/filter/", admin_views.filter_subscription_plans, name="filter_subscription_plans"),
    path(
        "subscriptions/filter/",
        admin_views.filter_customer_subscriptions,
        name="filter_customer_subscriptions",
    ),
]
