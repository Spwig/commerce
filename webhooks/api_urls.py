"""
API URL configuration for webhooks app.

All API endpoints are consolidated here to be included outside i18n_patterns.
"""
from django.urls import path
from . import api_views

app_name = 'webhooks_api'

urlpatterns = [
    # Documentation (public access for developers)
    path('docs/', api_views.get_webhook_documentation, name='documentation'),

    # Endpoint Management
    path('endpoints/', api_views.WebhookEndpointList.as_view(), name='endpoint-list'),
    path('endpoints/<uuid:pk>/', api_views.WebhookEndpointDetail.as_view(), name='endpoint-detail'),
    path('endpoints/<uuid:pk>/test/', api_views.test_webhook_endpoint, name='endpoint-test'),
    path('endpoints/<uuid:pk>/rotate-secret/', api_views.rotate_webhook_secret, name='endpoint-rotate-secret'),
    path('endpoints/<uuid:pk>/reset-failures/', api_views.reset_endpoint_failures, name='endpoint-reset-failures'),
    path('endpoints/<uuid:pk>/stats/', api_views.get_webhook_stats, name='endpoint-stats'),

    # Delivery Logs
    path('deliveries/', api_views.WebhookDeliveryList.as_view(), name='delivery-list'),
    path('deliveries/<uuid:pk>/', api_views.WebhookDeliveryDetail.as_view(), name='delivery-detail'),
    path('deliveries/<uuid:pk>/retry/', api_views.retry_webhook_delivery, name='delivery-retry'),

    # Event Types
    path('events/', api_views.list_webhook_events, name='event-list'),
]
