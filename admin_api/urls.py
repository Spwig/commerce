"""
Admin API URL Configuration

All admin API endpoints for the Spwig Merchant mobile app and headless management.
These URLs are included at /api/admin/ in core/urls.py (outside i18n_patterns).
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from admin_api.views import (
    auth, analytics, orders, products, messages, settings,
    categories, brands, variants, attributes, sso, inventory,
    staff, roles, bulk_orders, bulk_products, documents, branding,
)

app_name = 'admin_api'

# Router for ViewSet-based endpoints (will be added later)
router = DefaultRouter()

urlpatterns = [
    # Authentication endpoints
    path('auth/login/', auth.staff_login, name='staff_login'),
    path('auth/verify-2fa/', auth.verify_2fa, name='verify_2fa'),
    path('auth/refresh/', auth.refresh_token, name='refresh_token'),
    path('auth/logout/', auth.staff_logout, name='staff_logout'),
    path('auth/profile/', auth.staff_profile, name='staff_profile'),
    path('auth/password-reset/', auth.staff_password_reset_request, name='staff_password_reset_request'),
    path('auth/password-reset/confirm/', auth.staff_password_reset_confirm, name='staff_password_reset_confirm'),

    # Staff management endpoints
    path('staff/', staff.staff_list, name='staff_list'),
    path('staff/invite/', staff.staff_invite, name='staff_invite'),
    path('staff/<int:staff_id>/', staff.staff_update, name='staff_update'),
    path('staff/<int:staff_id>/delete/', staff.staff_delete, name='staff_delete'),
    path('auth/accept-invitation/<str:token>/', staff.accept_invitation, name='accept_invitation'),

    # Role management endpoints
    path('roles/', roles.role_list, name='role_list'),
    path('roles/create/', roles.role_create, name='role_create'),
    path('roles/<int:role_id>/', roles.role_update, name='role_update'),
    path('roles/<int:role_id>/delete/', roles.role_delete, name='role_delete'),
    path('permissions/', roles.permissions_list, name='permissions_list'),

    # Analytics endpoints (dashboard / mobile)
    path('analytics/dashboard/', analytics.dashboard_analytics, name='dashboard_analytics'),
    path('analytics/quick-stats/', analytics.quick_stats, name='quick_stats'),
    path('analytics/sales-kpi/', analytics.sales_kpi, name='sales_kpi'),
    path('analytics/top-products/', analytics.top_products, name='top_products'),
    path('analytics/sales-comparison/', analytics.sales_comparison, name='sales_comparison'),
    path('analytics/daily-stats/', analytics.daily_stats, name='daily_stats'),
    path('analytics/sales-hourly/', analytics.hourly_sales, name='sales_hourly'),

    # Advanced analytics endpoints
    path('analytics/products/', analytics.product_analytics, name='product_analytics'),
    path('analytics/customers/', analytics.customer_analytics, name='customer_analytics'),
    path('analytics/categories/', analytics.category_analytics, name='category_analytics'),
    path('analytics/brands/', analytics.brand_analytics, name='brand_analytics'),
    path('analytics/comparison/', analytics.analytics_comparison, name='analytics_comparison'),
    path('analytics/export/', analytics.analytics_export, name='analytics_export'),

    # Inventory intelligence endpoints
    path('inventory/dashboard/', inventory.inventory_dashboard, name='inventory_dashboard'),
    path('inventory/low-stock/', inventory.inventory_low_stock, name='inventory_low_stock'),
    path('inventory/velocity/', inventory.inventory_velocity, name='inventory_velocity'),
    path('inventory/movements/', inventory.inventory_movements, name='inventory_movements'),
    path('inventory/reorder-suggestions/', inventory.inventory_reorder_suggestions, name='inventory_reorder_suggestions'),
    path('inventory/settings/', inventory.inventory_settings_get, name='inventory_settings_get'),
    path('inventory/settings/update/', inventory.inventory_settings_update, name='inventory_settings_update'),

    # Order management endpoints
    # NOTE: Literal paths must come before <str:order_number> wildcard patterns
    path('orders/', orders.order_list, name='order_list'),
    path('orders/counts/', orders.order_counts, name='order_counts'),
    path('orders/batch-documents/', documents.batch_documents, name='batch_documents'),
    path('orders/bulk/status/', bulk_orders.bulk_order_status, name='bulk_order_status'),
    path('orders/bulk/fulfill/', bulk_orders.bulk_order_fulfill, name='bulk_order_fulfill'),
    path('orders/<str:order_number>/', orders.order_detail, name='order_detail'),
    path('orders/<str:order_number>/status/', orders.update_order_status, name='update_order_status'),
    path('orders/<str:order_number>/tracking/', orders.update_tracking, name='update_tracking'),
    path('orders/<str:order_number>/cancel/', orders.cancel_order, name='cancel_order'),
    path('orders/<str:order_number>/refund/', orders.initiate_refund, name='initiate_refund'),
    path('orders/<str:order_number>/notes/', orders.order_notes, name='order_notes'),
    path('orders/<str:order_number>/notes/add/', orders.add_order_note, name='add_order_note'),

    # Order document generation endpoints
    path('orders/<str:order_number>/invoice/pdf/', documents.order_invoice_pdf, name='order_invoice_pdf'),
    path('orders/<str:order_number>/packing-slip/pdf/', documents.order_packing_slip_pdf, name='order_packing_slip_pdf'),
    path('orders/<str:order_number>/pick-list/pdf/', documents.order_pick_list_pdf, name='order_pick_list_pdf'),

    # Product/Stock management endpoints (existing read + stock/status/image)
    path('products/', products.product_list, name='product_list'),
    path('products/counts/', products.product_counts, name='product_counts'),
    path('products/by-sku/', products.product_by_sku, name='product_by_sku'),
    path('products/low-stock/', products.low_stock_products, name='low_stock_products'),
    path('products/warehouses/', products.warehouse_list, name='warehouse_list'),
    path('products/create/', products.create_product, name='create_product'),
    path('products/bulk/', products.bulk_create_products, name='bulk_create_products'),
    path('products/bulk/update/', products.bulk_update_products, name='bulk_update_products'),
    path('products/<int:product_id>/', products.product_detail, name='product_detail'),
    path('products/<int:product_id>/update/', products.update_product, name='update_product'),
    path('products/<int:product_id>/delete/', products.delete_product, name='delete_product'),
    path('products/<int:product_id>/stock/', products.adjust_stock, name='adjust_stock'),
    path('products/<int:product_id>/status/', products.update_product_status, name='update_product_status'),

    # Product image management endpoints
    path('products/<int:product_id>/images/', products.upload_product_image, name='upload_product_image'),
    path('products/<int:product_id>/images/reorder/', products.reorder_product_images, name='reorder_product_images'),
    path('products/<int:product_id>/images/<int:image_id>/', products.delete_product_image, name='delete_product_image'),
    path('products/<int:product_id>/images/<int:image_id>/primary/', products.set_primary_image, name='set_primary_image'),
    path('products/<int:product_id>/images/<int:image_id>/update/', products.update_product_image, name='update_product_image'),

    # Product variant management endpoints
    path('products/<int:product_id>/variants/', variants.variant_list, name='variant_list'),
    path('products/<int:product_id>/variants/create/', variants.create_variant, name='create_variant'),
    path('products/<int:product_id>/variants/<int:variant_id>/update/', variants.update_variant, name='update_variant'),
    path('products/<int:product_id>/variants/<int:variant_id>/delete/', variants.delete_variant, name='delete_variant'),

    # Product attribute assignment endpoints
    path('products/<int:product_id>/attributes/assign/', attributes.assign_product_attributes, name='assign_product_attributes'),

    # Bulk product operations endpoints
    path('inventory/bulk/adjust/', bulk_products.bulk_stock_adjust, name='bulk_stock_adjust'),
    path('products/bulk/price/', bulk_products.bulk_price_update, name='bulk_price_update'),
    path('products/bulk/assign-category/', bulk_products.bulk_assign_category, name='bulk_assign_category'),
    path('products/bulk/assign-tags/', bulk_products.bulk_assign_tags, name='bulk_assign_tags'),
    path('products/bulk/sale/', bulk_products.bulk_sale_update, name='bulk_sale_update'),

    # Category management endpoints
    path('categories/', categories.category_list, name='category_list'),
    path('categories/create/', categories.create_category, name='create_category'),
    path('categories/bulk/', categories.bulk_create_categories, name='bulk_create_categories'),
    path('categories/<int:category_id>/', categories.category_detail, name='category_detail'),
    path('categories/<int:category_id>/update/', categories.update_category, name='update_category'),
    path('categories/<int:category_id>/delete/', categories.delete_category, name='delete_category'),

    # Category image/banner management endpoints
    path('categories/<int:category_id>/image/', categories.upload_category_image, name='upload_category_image'),
    path('categories/<int:category_id>/image/delete/', categories.delete_category_image, name='delete_category_image'),
    path('categories/<int:category_id>/banner/', categories.upload_category_banner, name='upload_category_banner'),
    path('categories/<int:category_id>/banner/delete/', categories.delete_category_banner, name='delete_category_banner'),

    # Brand management endpoints
    path('brands/', brands.brand_list, name='brand_list'),
    path('brands/create/', brands.create_brand, name='create_brand'),
    path('brands/bulk/', brands.bulk_create_brands, name='bulk_create_brands'),
    path('brands/<int:brand_id>/', brands.brand_detail, name='brand_detail'),
    path('brands/<int:brand_id>/update/', brands.update_brand, name='update_brand'),
    path('brands/<int:brand_id>/delete/', brands.delete_brand, name='delete_brand'),

    # Attribute management endpoints
    path('attributes/', attributes.attribute_list, name='attribute_list'),
    path('attributes/create/', attributes.create_attribute, name='create_attribute'),

    # Customer messages endpoints (unified: contact_form + order_note sources)
    path('messages/', messages.message_list, name='message_list'),
    path('messages/counts/', messages.message_counts, name='message_counts'),
    path('messages/unread-count/', messages.unread_count, name='unread_count'),
    path('messages/<str:source>/<int:message_id>/', messages.message_detail, name='message_detail'),
    path('messages/<str:source>/<int:message_id>/status/', messages.update_message_status, name='update_message_status'),
    path('messages/contact_form/<int:message_id>/reply/', messages.reply_to_message, name='reply_to_message'),

    # SSO mobile auth endpoints
    path('auth/sso/config/', sso.sso_config, name='sso_config'),
    path('auth/sso/mobile/authorize/', sso.sso_mobile_authorize, name='sso_mobile_authorize'),
    path('auth/sso/mobile/callback/', sso.sso_mobile_callback, name='sso_mobile_callback'),
    path('auth/sso/mobile/token/', sso.sso_mobile_token, name='sso_mobile_token'),

    # Settings and device management endpoints
    path('settings/', settings.get_settings, name='get_settings'),
    path('settings/languages/', settings.available_languages, name='available_languages'),
    path('settings/devices/', settings.list_devices, name='list_devices'),
    path('settings/devices/register/', settings.register_device, name='register_device'),
    path('settings/devices/<str:device_id>/', settings.unregister_device, name='unregister_device'),
    path('settings/push-token/', settings.update_push_token, name='update_push_token'),
    path('settings/notifications/', settings.update_notifications, name='update_notifications'),
    path('settings/sessions/', settings.active_sessions, name='active_sessions'),
    path('settings/sessions/<str:device_id>/revoke/', settings.revoke_session, name='revoke_session'),

    # Branding settings endpoints
    path('settings/branding/', branding.branding_settings_get, name='branding_settings_get'),
    path('settings/branding/update/', branding.branding_settings_update, name='branding_settings_update'),
    path('settings/branding/logo/', branding.branding_logo_upload, name='branding_logo_upload'),

    # Router URLs
    path('', include(router.urls)),
]
