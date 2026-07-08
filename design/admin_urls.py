"""
Design Admin URLs
AJAX endpoints for admin filtering
"""
from django.urls import path
from . import admin_views

app_name = 'design_admin'

urlpatterns = [
    path('designtoken/filter/', admin_views.filter_design_tokens, name='filter_design_tokens'),
    path('widget/filter/', admin_views.filter_widgets, name='filter_widgets'),
]
