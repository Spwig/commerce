from django.urls import path
from . import views

app_name = 'page_builder'

urlpatterns = [
    # Page rendering URLs (storefront)
    path('', views.home_view, name='home'),
    path('category/', views.category_view, name='category_list'),
    path('category/<slug:category_slug>/', views.category_view, name='category_detail'),
    path('products/', views.products_view, name='products'),
    path('product/<slug:product_slug>/', views.product_view, name='product_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('checkout/return/', views.checkout_return_view, name='checkout_return'),
    path('checkout/confirmation/<str:order_number>/', views.order_confirmation_view, name='order_confirmation'),
    path('page/<slug:slug>/', views.page_view, name='page_detail'),

    # NOTE: Visual builder, preview, AJAX element, and utility template URLs
    # have been moved to admin_urls.py (mounted at /admin/page_builder/)
    # to ensure role-based admin access control via AdminAccessMiddleware.

    # NOTE: API endpoints are in api_urls.py (mounted at /api/page-builder/)
    # outside i18n_patterns to prevent language prefixes.
]
