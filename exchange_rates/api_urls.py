"""
API URL configuration for the exchange_rates app.
All API endpoints are consolidated here to be included outside i18n_patterns.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from exchange_rates import api_views

app_name = "exchange_rates_api"

router = DefaultRouter()
router.register(r"manual", api_views.ManualExchangeRateViewSet, basename="manual-exchange-rate")

urlpatterns = [
    path("", include(router.urls)),
]
