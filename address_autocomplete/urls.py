"""
URL configuration for address autocomplete
"""

from django.urls import path

from .views import (
    AutocompleteView,
    EnhanceAddressView,
    NormalizeView,
    ReverseGeocodeView,
    ServiceHealthView,
    ValidateView,
)

app_name = "address_autocomplete"

urlpatterns = [
    # Main autocomplete endpoint
    path("autocomplete/", AutocompleteView.as_view(), name="autocomplete"),
    # Address normalization
    path("normalize/", NormalizeView.as_view(), name="normalize"),
    # Address validation
    path("validate/", ValidateView.as_view(), name="validate"),
    # Address enhancement (requires login)
    path("enhance/", EnhanceAddressView.as_view(), name="enhance"),
    # Reverse geocoding
    path("reverse/", ReverseGeocodeView.as_view(), name="reverse"),
    # Service health check
    path("health/", ServiceHealthView.as_view(), name="health"),
]
