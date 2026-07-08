"""
URL configuration for Orders API and Admin HTMX endpoints
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    OrderViewSet, AddressViewSet, ReturnRequestViewSet,
    # Admin HTMX views
    order_item_add_view, order_item_update_view, order_item_remove_view,
    order_calculate_totals_view, order_voucher_apply_view, order_voucher_remove_view,
    order_manual_discount_apply_view,
    order_customer_update_view, order_address_update_view, order_status_update_view,
    product_search_api_view, customer_search_api_view
)

app_name = 'orders'

# Create router for viewsets
router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'addresses', AddressViewSet, basename='address')
router.register(r'return-requests', ReturnRequestViewSet, basename='return-request')

# Admin HTMX endpoints for order editing
admin_htmx_patterns = [
    # Order item management
    path('admin/order/<int:order_id>/item/add/', order_item_add_view, name='admin-order-item-add'),
    path('admin/order/<int:order_id>/item/<int:item_id>/update/', order_item_update_view, name='admin-order-item-update'),
    path('admin/order/<int:order_id>/item/<int:item_id>/remove/', order_item_remove_view, name='admin-order-item-remove'),

    # Order totals
    path('admin/order/<int:order_id>/calculate-totals/', order_calculate_totals_view, name='admin-order-calculate-totals'),

    # Voucher management
    path('admin/order/<int:order_id>/voucher/apply/', order_voucher_apply_view, name='admin-order-voucher-apply'),
    path('admin/order/<int:order_id>/voucher/<int:voucher_id>/remove/', order_voucher_remove_view, name='admin-order-voucher-remove'),

    # Manual discount management
    path('admin/order/<int:order_id>/discount/apply/', order_manual_discount_apply_view, name='admin-order-manual-discount-apply'),

    # Customer and address management
    path('admin/order/<int:order_id>/customer/update/', order_customer_update_view, name='admin-order-customer-update'),
    path('admin/order/<int:order_id>/address/update/', order_address_update_view, name='admin-order-address-update'),

    # Status update
    path('admin/order/<int:order_id>/status/update/', order_status_update_view, name='admin-order-status-update'),

    # Product search
    path('admin/product-search/', product_search_api_view, name='admin-product-search'),

    # Customer search
    path('admin/customer-search/', customer_search_api_view, name='admin-customer-search'),
]

urlpatterns = [
    # Admin HTMX endpoints
    *admin_htmx_patterns,

    # Router URLs (orders, addresses, return-requests)
    path('', include(router.urls)),
]
