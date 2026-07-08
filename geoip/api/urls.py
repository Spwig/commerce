"""
GeoIP API URL Configuration
"""
from django.urls import path
from . import views

app_name = 'geoip_api'

urlpatterns = [
    # Main endpoints
    path('v1/resolve/', views.resolve_location, name='resolve'),
    path('v1/preference/', views.set_preference, name='preference'),

    # Suggestion endpoints
    path('v1/suggest/currency/', views.suggest_currency, name='suggest_currency'),
    path('v1/suggest/language/', views.suggest_language, name='suggest_language'),

    # Data endpoints
    path('v1/countries/', views.list_countries, name='countries'),

    # Feedback endpoint
    path('v1/report/', views.report_correction, name='report_correction'),
]