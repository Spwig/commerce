"""
Element Builder Admin URLs

These URLs are included inside i18n_patterns for admin functionality.
"""
from django.urls import path
from . import admin_views

app_name = 'element_builder_admin'

urlpatterns = [
    path(
        'customelement/filter/',
        admin_views.filter_elements,
        name='customelement_filter'
    ),
]
