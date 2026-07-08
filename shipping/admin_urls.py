"""
Shipping Admin URLs.
Routes for AJAX filter endpoints used in admin change lists.
"""
from django.urls import path
from . import admin_views

app_name = 'shipping_admin'

urlpatterns = [
    path('packages/filter/', admin_views.filter_shipping_packages, name='filter_shipping_packages'),
    path('tracking-events/filter/', admin_views.filter_tracking_events, name='filter_tracking_events'),
    path('webhook-logs/filter/', admin_views.filter_webhook_logs, name='filter_webhook_logs'),
]
