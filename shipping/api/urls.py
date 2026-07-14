"""
Shipping API URLs
URL patterns for REST API endpoints
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from shipping.api.views import (
    CarrierPresetViewSet,
    ProviderAccountViewSet,
    ShipmentViewSet,
    TrackingEventViewSet,
)

# Create router and register viewsets
router = DefaultRouter()
router.register(r"carriers", CarrierPresetViewSet, basename="carrier")
router.register(r"shipments", ShipmentViewSet, basename="shipment")
router.register(r"tracking-events", TrackingEventViewSet, basename="tracking-event")
router.register(r"providers", ProviderAccountViewSet, basename="provider")

app_name = "shipping_api"

urlpatterns = [
    path("", include(router.urls)),
]
