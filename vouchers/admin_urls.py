"""
Vouchers Admin URL Configuration
Separate from API URLs - these are for admin interface AJAX endpoints
"""

from django.urls import path

from vouchers import views

app_name = "vouchers_admin"

urlpatterns = [
    # Admin AJAX Endpoints
    path("vouchercode/filter/", views.filter_voucher_codes, name="filter_voucher_codes"),
]
