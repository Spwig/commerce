"""
Cart Admin URL Configuration
Separate from API URLs - these are for admin interface AJAX endpoints
"""
from django.urls import path
from cart import views

app_name = 'cart_admin'

urlpatterns = [
    # Admin AJAX Endpoints
    path('cart/filter/', views.filter_carts, name='filter_carts'),

    # Tax Rate Admin AJAX Endpoints
    path('taxrate/filter/', views.filter_tax_rates, name='filter_tax_rates'),
    path('taxrate/load-preset/', views.load_tax_preset, name='load_tax_preset'),
]
