"""
Store Information API URL Configuration

Public API endpoints for store information.
Accessed via /api/store/
"""

from django.urls import path
from . import store

urlpatterns = [
    # Complete store info (single request for all data)
    path('', store.get_store_info, name='store-info'),

    # Individual endpoints for specific data
    path('info/', store.get_store_basic_info, name='store-basic-info'),
    path('contact/', store.get_store_contact, name='store-contact'),
    path('social/', store.get_store_social, name='store-social'),
    path('payment-methods/', store.get_store_payment_methods, name='store-payment-methods'),
    path('shipping-info/', store.get_store_shipping_info, name='store-shipping-info'),
    path('currency/', store.get_store_currency_settings, name='store-currency'),
    path('currencies/', store.list_currencies, name='store-currencies'),
    path('set-currency/', store.set_currency_api, name='store-set-currency'),
]
