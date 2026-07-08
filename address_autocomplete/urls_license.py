"""
URL patterns for license-based geocoder token provisioning
Add these to your main urls.py
"""

from django.urls import path
from .license_views import (
    ProvisionGeocoderTokenView,
    RefreshGeocoderTokenView,
    GeocoderTokenStatusView
)

app_name = 'geocoder_license'

urlpatterns = [
    # Token provisioning endpoints (for internal use)
    path('api/geocoder/provision-token/', ProvisionGeocoderTokenView.as_view(), name='provision_token'),
    path('api/geocoder/refresh-token/', RefreshGeocoderTokenView.as_view(), name='refresh_token'),
    path('api/geocoder/token-status/', GeocoderTokenStatusView.as_view(), name='token_status'),
]