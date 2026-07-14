"""
GeoIP URL Configuration

API endpoints only (non-i18n). Admin views are in admin_urls.py (i18n block).
"""

from django.urls import include, path

app_name = "geoip"

urlpatterns = [
    # API endpoints (non-i18n)
    path("api/geoip/", include("geoip.api.urls")),
]
