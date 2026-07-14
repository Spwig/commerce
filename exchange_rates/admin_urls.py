"""
Exchange Rates Admin URL Configuration
Separate from main URLs - these are for admin interface AJAX endpoints
"""

from django.urls import path

from exchange_rates.views import filter_exchange_rate_providers

app_name = "exchange_rates_admin"

urlpatterns = [
    # Admin List Filtering Endpoint
    path(
        "exchangerateprovideraccount/filter/",
        filter_exchange_rate_providers,
        name="filter_exchange_rate_providers",
    ),
]
