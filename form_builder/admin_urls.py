"""
Form Builder Admin URLs.
Routes for AJAX filter endpoints used in admin change lists.
"""
from django.urls import path
from . import admin_views

app_name = 'form_builder_admin'

urlpatterns = [
    path('forms/filter/', admin_views.filter_forms, name='filter_forms'),
    path('forms/recycle-bin/', admin_views.form_recycle_bin, name='form_recycle_bin'),
]
