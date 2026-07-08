"""
API URL configuration for catalog app.
All API endpoints are consolidated here to be included outside i18n_patterns.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views, license_api_views
from .api import translation_endpoints, image_endpoints, booking_endpoints

app_name = 'catalog_api'

# Create router for viewsets
router = DefaultRouter()
router.register(r'categories', api_views.CategoryViewSet, basename='category')
router.register(r'brands', api_views.BrandViewSet, basename='brand')
router.register(r'attributes', api_views.ProductAttributeViewSet, basename='attribute')
router.register(r'products', api_views.ProductViewSet, basename='product')
router.register(r'collections', api_views.CollectionViewSet, basename='collection')
router.register(r'reviews', api_views.ProductReviewViewSet, basename='review')

# API URL patterns
urlpatterns = [
    # Product recommendations (for mini-cart empty state)
    path('recommendations/', api_views.product_recommendations, name='recommendations'),

    # Catalog statistics
    path('stats/', api_views.catalog_stats, name='stats'),

    # Available filter options
    path('filters/', api_views.available_filters, name='filters'),

    # Multi-location inventory endpoints
    path('products/<slug:product_slug>/check-stock/', api_views.check_warehouse_stock, name='check-warehouse-stock'),
    path('pickup-locations/', api_views.pickup_locations, name='pickup-locations'),

    # Stock availability & notification endpoints
    path('products/<slug:product_slug>/availability/', api_views.product_availability, name='product-availability'),
    path('products/<slug:product_slug>/notify-me/', api_views.stock_notification_subscribe, name='stock-notification-subscribe'),

    # Gift card endpoints
    path('gift-cards/check-balance/', api_views.check_gift_card_balance, name='gift-card-check-balance'),

    # License API endpoints (public - for software clients)
    path('licenses/validate/', license_api_views.validate_license, name='license-validate'),
    path('licenses/activate/', license_api_views.activate_license, name='license-activate'),
    path('licenses/deactivate/', license_api_views.deactivate_license, name='license-deactivate'),
    path('licenses/<str:key>/info/', license_api_views.get_license_info, name='license-info'),

    # License Pool endpoints (admin only)
    path('license-pools/', license_api_views.list_license_pools, name='license-pools-list'),
    path('license-pools/<int:pool_id>/', license_api_views.get_license_pool, name='license-pool-detail'),
    path('licenses/bulk-generate/', license_api_views.bulk_generate_licenses, name='license-bulk-generate'),

    # Product translation endpoints
    path('products/<int:product_id>/translations/',
         translation_endpoints.get_product_translations,
         name='product-translations'),
    path('products/<int:product_id>/translations/save/',
         translation_endpoints.save_product_translation,
         name='product-translation-save'),
    path('products/<int:product_id>/translations/save-all/',
         translation_endpoints.save_all_product_translations,
         name='product-translations-save-all'),
    path('translations/languages/',
         translation_endpoints.get_available_languages,
         name='available-languages'),

    # Product image endpoints
    path('products/<int:product_id>/images/',
         image_endpoints.get_product_images,
         name='product-images'),
    path('products/<int:product_id>/images/order/',
         image_endpoints.update_image_order,
         name='product-images-order'),
    path('products/<int:product_id>/images/<int:image_id>/primary/',
         image_endpoints.set_primary_image,
         name='product-image-primary'),
    path('products/<int:product_id>/images/<int:image_id>/',
         image_endpoints.delete_product_image,
         name='product-image-delete'),

    # Product Attribute Assignment Management (admin only)
    path('products/<int:product_id>/attribute-assignments/',
         api_views.list_product_attributes, name='product-attributes-list'),
    path('products/<int:product_id>/attribute-assignments/add/',
         api_views.add_product_attribute, name='product-attribute-add'),
    path('products/<int:product_id>/attribute-assignments/<int:assignment_id>/remove/',
         api_views.remove_product_attribute, name='product-attribute-remove'),
    path('products/<int:product_id>/attribute-assignments/<int:assignment_id>/values/',
         api_views.update_attribute_values, name='product-attribute-values-update'),
    path('products/<int:product_id>/attribute-assignments/search/',
         api_views.search_available_attributes, name='product-attributes-search'),

    # Booking endpoints
    path('products/<slug:product_slug>/booking/availability/',
         booking_endpoints.booking_availability,
         name='booking-availability'),
    path('products/<slug:product_slug>/booking/slots/',
         booking_endpoints.booking_slots,
         name='booking-slots'),
    path('products/<slug:product_slug>/booking/check/',
         booking_endpoints.booking_check,
         name='booking-check'),
    path('products/<slug:product_slug>/booking/resource-availability/',
         booking_endpoints.booking_resource_availability,
         name='booking-resource-availability'),
    path('products/<slug:product_slug>/booking/resources/<int:resource_id>/',
         booking_endpoints.booking_resource_detail,
         name='booking-resource-detail'),
    path('products/<slug:product_slug>/booking/ical/<str:ical_uid>/',
         booking_endpoints.booking_ical,
         name='booking-ical'),
    path('products/<slug:product_slug>/booking/waitlist/',
         booking_endpoints.booking_waitlist,
         name='booking-waitlist'),

    # Customer booking self-service (authenticated)
    path('bookings/my/',
         booking_endpoints.my_bookings,
         name='my-bookings'),
    path('bookings/<int:booking_id>/',
         booking_endpoints.booking_detail_api,
         name='booking-detail-api'),
    path('bookings/<int:booking_id>/cancel/',
         booking_endpoints.booking_cancel,
         name='booking-cancel'),
    path('bookings/<int:booking_id>/reschedule/',
         booking_endpoints.booking_reschedule_api,
         name='booking-reschedule-api'),

    # Router URLs (includes all viewsets)
    path('', include(router.urls)),
]
