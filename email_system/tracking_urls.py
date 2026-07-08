"""
Email tracking URL configuration.

These URLs must be outside i18n_patterns since they are embedded in email
tracking pixels and click redirect links. Adding a language prefix would
break tracking when email clients follow these URLs.
"""
from django.urls import path
from email_system.views import tracking

app_name = 'email_tracking'

urlpatterns = [
    path('track/open/<str:tracking_id>/', tracking.track_open, name='track_open'),
    path('track/click/<str:tracking_id>/', tracking.track_click, name='track_click'),
]
