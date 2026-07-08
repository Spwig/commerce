"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import RedirectView
from core import views
from core.currency_views import set_currency
from catalog.api.translation_endpoints import get_available_languages
from catalog.api.image_endpoints import get_product_images
from catalog.download_views import download_digital_asset
from core.api import currency_endpoints, translation_api
from core.sandbox.views import tamper_report
from core.error_reporting import views as error_reporting_views
from pos_app import views as pos_views
from pos_app.community_gate import pos_upgrade_required_view
import accounts.urls

# Health check endpoints (must be accessible without auth, before any middleware)
urlpatterns = [
    path('health/', views.health_check, name='health_check'),  # Minimal public health check
    path('health/detailed/', views.health_detailed, name='health_detailed'),  # Detailed (requires staff auth)
    path('health/live/', views.health_live, name='health_live'),
    path('health/ready/', views.health_ready, name='health_ready'),
    # .well-known endpoints (public, no auth)
    path('.well-known/apple-app-site-association', views.apple_app_site_association, name='apple_aasa'),
    path('.well-known/security.txt', views.security_txt, name='security_txt'),
]

# Platform activation (non-i18n, must work before auth/license/setup)
urlpatterns += [
    path('activate/', views.activate, name='activate'),
]

# License acceptance (non-i18n, must work before auth/setup)
urlpatterns += [
    path('license/accept/', views.license_accept, name='license_accept'),
    path('license/view/', views.license_view, name='license_view'),
    path('license/third-party-notices/', views.third_party_notices_view, name='third_party_notices'),
]

# Non-i18n URLs (language switcher, static/media files, API)
urlpatterns += [
    path('i18n/', include('translations.i18n_urls')),
    # Currency switcher API (non-i18n as it's an API)
    path('api/set-currency/', set_currency, name='set_currency'),
    # Multi-Currency Management API
    path('api/currencies/', currency_endpoints.list_all_currencies, name='api_currencies_list'),
    path('api/currencies/active/', currency_endpoints.list_active_currencies, name='api_currencies_active'),
    path('api/currencies/activate/', currency_endpoints.activate_currencies, name='api_currencies_activate'),
    path('api/currencies/deactivate/', currency_endpoints.deactivate_currencies, name='api_currencies_deactivate'),
    path('api/currencies/reorder/', currency_endpoints.reorder_currencies, name='api_currencies_reorder'),
    path('api/currencies/<str:code>/', currency_endpoints.update_currency_settings, name='api_currency_update'),
    path('api/currencies/bulk-update/', currency_endpoints.bulk_update_currencies, name='api_currencies_bulk_update'),
    # Translation and Product Image APIs
    path('api/translations/languages/', get_available_languages, name='api_available_languages'),
    path('api/products/<int:product_id>/images/', get_product_images, name='api_product_images'),
    # Generic Translation API (works with any model)
    path('api/translation/health/', translation_api.translation_health, name='api_translation_health'),
    path('api/translation/languages/', translation_api.get_available_languages_api, name='api_translation_languages'),
    path('api/translation/<str:model_type>/<int:object_id>/<str:field_key>/status/',
         translation_api.generic_translation_status, name='api_generic_translation_status'),
    path('api/translation/<str:model_type>/<int:object_id>/<str:field_key>/translate/',
         translation_api.translate_generic_field, name='api_translate_generic_field'),
    path('api/translation/<str:model_type>/<int:object_id>/<str:field_key>/save/',
         translation_api.save_generic_translations, name='api_save_generic_translations'),
    path('api/translation/<str:model_type>/<int:object_id>/<str:field_key>/save_field/',
         translation_api.save_field_value, name='api_save_field_value'),
    # Translations Service API (non-i18n as it's an API)
    path('api/translations/service/', include('translations.api_urls')),
    # GeoIP API (non-i18n as it's an API)
    path('', include('geoip.urls')),
    # Cookie consent (non-i18n, csrf-exempt — must work on first visit)
    path('api/cookie-consent/', views.cookie_consent_view, name='cookie_consent'),
    # Sandbox tamper report beacon (non-i18n, csrf-exempt)
    path('api/sandbox/tamper-report/', tamper_report, name='sandbox_tamper_report'),
    # CSP violation report endpoint (non-i18n, csrf-exempt, POST-only)
    path('api/csp-report/', views.csp_report, name='csp_report'),
    # JS error report endpoint (non-i18n, csrf-exempt, POST-only)
    path('api/error-reports/js/', error_reporting_views.receive_js_errors, name='js_error_report'),
    # Bug report submission from admin wizard (staff-only, requires CSRF)
    path('api/bug-reports/submit/', error_reporting_views.submit_bug_report, name='submit_bug_report'),
    # Core API (Help System) (non-i18n as it's an API)
    path('api/core/', include('core.api_urls')),
    # Accounts API (non-i18n as it's an API)
    path('api/accounts/', include('accounts.api_urls')),
    # Enterprise SSO (OIDC) URLs — must be outside i18n_patterns
    path('oidc/', include('enterprise_sso.urls')),
    # Django-allauth URLs (must be separate from accounts.urls to avoid namespace issues)
    path('accounts/', include(accounts.urls.allauth_urlpatterns)),
    # Blog API (non-i18n as it's an API)
    path('api/blog/', include('blog.api_urls')),
    # Catalog API (non-i18n as it's an API)
    path('api/catalog/', include('catalog.api_urls')),
    # Cart, Wishlist & Checkout API (non-i18n as it's an API)
    path('api/', include('cart.urls')),
    # Orders & Addresses API (non-i18n as it's an API)
    path('api/', include('orders.urls')),
    # Customer Analytics & Insights API (non-i18n as it's an API)
    path('api/customers/', include('customers.urls')),
    # Shipping API (non-i18n as it's an API)
    path('api/shipping/', include('shipping.api.urls')),
    # Social Sharing API (non-i18n as it's an API)
    path('api/social/', include('social_sharing.api.urls')),
    # Referral Program API (non-i18n as it's an API)
    path('api/referrals/', include('referrals.api.urls')),
    # Affiliate API (non-i18n as it's an API)
    path('api/affiliate/', include('affiliate.api_urls')),
    # Media Library API (non-i18n as it's an API)
    path('api/media/', include('media_library.api_urls')),
    # Vouchers API (non-i18n as it's an API)
    path('api/vouchers/', include('vouchers.api.urls')),
    # Page Builder API (non-i18n as it's an API)
    path('api/page-builder/', include('page_builder.api_urls')),
    # Subscriptions API (non-i18n as it's an API)
    path('api/subscriptions/', include('subscriptions.api_urls')),
    # SEO Generator API (non-i18n as it's an API)
    path('api/seo/', include('seo_generator.urls')),
    # Admin API for merchant mobile app (non-i18n as it's an API)
    path('api/admin/', include('admin_api.urls')),
    # Announcements API (non-i18n as it's an API)
    path('api/announcements/', include('announcements.api_urls')),
    # Loyalty Program API (non-i18n as it's an API)
    path('api/loyalty/', include('loyalty.api.urls')),
    # Wallet API (non-i18n as it's an API)
    path('api/wallet/', include('wallet.api.urls')),
    # Store Information API (non-i18n as it's an API)
    path('api/store/', include('core.api.store_urls')),
    # Customer Messages API (non-i18n as it's an API)
    path('api/messages/', include('core.api.messages_urls')),
    # Webhooks API (non-i18n as it's an API)
    path('api/webhooks/', include('webhooks.api_urls')),
    # Form Builder API (non-i18n as it's an API)
    path('api/form-builder/', include('form_builder.api_urls')),
    # Address Autocomplete API (non-i18n as it's an API)
    path('api/address/', include('address_autocomplete.urls')),
    # Search API (non-i18n as it's an API)
    path('api/search/', include('search.api_urls')),
    # Element Builder API (non-i18n as it's an API)
    path('api/element-builder/', include('element_builder.urls')),
    # POS API (non-i18n, license-gated via middleware)
    path('api/pos/', include('pos_api.urls')),
    # Menu Builder API (non-i18n as it's an API)
    path('api/menu/', include('design.menu_api_urls')),
    # Header/Footer Builder API (non-i18n as it's an API)
    path('api/hf-builder/', include('design.hf_api_urls')),
    # Theme SDK Development Server API (non-i18n, DEBUG only)
    path('api/theme-dev/', include('design.dev_server_urls')),
    # Payment Orchestration API (non-i18n as it's an API)
    path('api/payments/', include('payment_providers.api_urls')),
    # Customizable Product API (non-i18n as it's an API)
    path('api/customizable-product/', include('customizable_product.api_urls')),
    # Custom Fields API (non-i18n as it's an API)
    path('api/custom-fields/', include('custom_fields.api_urls')),
    # Exchange Rates API (non-i18n as it's an API)
    path('api/exchange-rates/', include('exchange_rates.api_urls')),
    # Domain & SSL Configuration API (non-i18n as it's an API)
    path('api/domain-ssl/', include('domain_ssl.api_urls')),
    # Spwig Sync API (non-i18n, instance-to-instance communication)
    path('api/sync/', include('migration.sync.urls')),
    # POS Terminal SPA (non-i18n, standalone PWA interface)
    path('pos/', include('pos_app.urls')),
    # POS upgrade CTA (shown to Community edition merchants navigating to POS)
    path('pos-upgrade/', pos_upgrade_required_view, name='pos_upgrade'),
    # Digital Product Downloads (non-i18n, download links should work without language prefix)
    path('download/<str:token>/', download_digital_asset, name='digital_download'),
    # POS Public Receipt (non-i18n, receipt links from email/SMS should work without language prefix)
    path('receipt/<str:token>/', pos_views.PublicReceiptView.as_view(), name='public_receipt'),
    # CKEditor 5 file upload (used in admin rich text editors)
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    # Email tracking (non-i18n: tracking pixels/links in emails must work without language prefix)
    path('email/', include('email_system.tracking_urls')),
]

# Theme CSS serving (non-i18n: CSS is language-independent, URLs must work without prefix)
# get_css_url() in theme_models.py returns /theme/css/... without language prefix
from design.views import ThemeCSSView, BrandCSSView, LayeredCSSView, EditorContentCSSView
urlpatterns += [
    path('theme/css/brand.css', BrandCSSView.as_view(), name='brand_css_direct'),
    path('theme/css/layered.css', LayeredCSSView.as_view(), name='layered_css_direct'),
    path('theme/css/theme/<slug:slug>.css', ThemeCSSView.as_view(), name='theme_css_direct'),
    path('theme/css/editor-content.css', EditorContentCSSView.as_view(), name='editor_content_css'),
]

# Webhook endpoints (non-i18n, external services don't support language prefixes)
# These must be outside i18n_patterns to be accessible without language prefix
# IMPORTANT: Specific paths (health/) must come BEFORE generic patterns (<str:provider_key>/)
from shipping.webhooks import provider_webhook, webhook_health_check
urlpatterns += [
    path('webhooks/shipping/health/', webhook_health_check, name='shipping_webhook_health'),
    path('webhooks/shipping/<str:provider_key>/', provider_webhook, name='shipping_provider_webhook'),
]

# Payout provider webhooks (for affiliate payouts via PayPal/Airwallex)
urlpatterns += [
    path('webhooks/payouts/', include('payout_providers.webhook_urls')),
]

# Payment provider webhooks (for payment intent notifications from Stripe, AirWallex, etc.)
from payment_providers.views.handlers import payment_webhook_handler
urlpatterns += [
    path('webhooks/payments/<str:provider_slug>/', payment_webhook_handler, name='payment_webhook'),
]

# Payment provider component static files (JavaScript handlers, CSS, assets)
from payment_providers.views.component_static import ComponentStaticFileView
urlpatterns += [
    path(
        'components/payments/<slug:provider_slug>/current/<path:filename>',
        ComponentStaticFileView.as_view(),
        name='provider_component_static'
    ),
]

# Marketplace Checkout API (only active on spwig.com when SPWIG_IS_HQ=true)
# Non-i18n: external API calls from spwig.com frontend don't use language prefixes
if getattr(settings, 'SPWIG_IS_HQ', False):
    from core.api.sales_bell import bell_events
    from license_checkout.views import HostingEventWebhookView
    urlpatterns += [
        path('api/marketplace/', include('marketplace_checkout.urls')),
        path('api/license-checkout/', include('license_checkout.urls')),
        path('api/hq/account/', include('accounts.api_urls_hq')),
        path('api/hosting-events/', HostingEventWebhookView.as_view(), name='hosting-events'),
        path('api/internal/bell/events/', bell_events, name='sales_bell_events'),
    ]

# i18n URLs (admin and frontend with language prefixes)
urlpatterns += i18n_patterns(
    # Redirect old Django admin URL for TranslationJob to new interface
    path('admin/translations/translationjob/',
         RedirectView.as_view(url='/admin/translations/jobs/', permanent=True)),
    path('admin/translations/translationjob/<path:rest>/',
         RedirectView.as_view(url='/admin/translations/jobs/', permanent=True)),

    # Maintenance preview (staff only)
    path('maintenance/preview/', views.maintenance_preview, name='maintenance_preview'),

    # Admin and admin-related apps
    path('admin/switch-theme/', views.switch_admin_theme, name='admin_switch_theme'),
    path('admin/style-guide/', views.admin_style_guide, name='admin_style_guide'),
    path('admin/users/filter/', views.filter_users, name='filter_users'),
    path('admin/community/', views.community_redirect, name='community_redirect'),
    path('admin/sso/redirect/', views.sso_redirect, name='sso_redirect'),
    path('admin/setup/', include('setup_wizard.urls')),
    path('admin/customers/', include('customers.urls_admin')),
    path('admin/accounts/', include('accounts.admin_urls')),
    path('admin/translations/', include('translations.urls')),
    path('admin/shipping/', include('shipping.urls')),
    path('admin/shipping/', include('shipping.admin_urls')),
    path('admin/payment-providers/', include('payment_providers.urls')),
    path('admin/exchange-rates/', include('exchange_rates.urls')),
    path('admin/exchange-rates/', include('exchange_rates.admin_urls')),
    path('admin/product-feeds/', include('product_feeds.urls')),
    path('admin/blog/', include('blog.admin_urls')),
    path('admin/vouchers/', include('vouchers.admin_urls')),
    path('admin/affiliate/', include('affiliate.admin_urls')),
    path('admin/email-system/', include('email_system.urls')),
    path('admin/email-system/', include('email_system.admin_urls')),
    path('admin/sms-system/', include('sms_system.urls')),
    path('admin/subscriptions/', include('subscriptions.admin_urls')),
    path('admin/loyalty/', include('loyalty.urls')),
    path('admin/social_sharing/', include('social_sharing.urls')),
    path('admin/referrals/', include('referrals.urls')),
    path('admin/orders/', include('orders.admin_urls')),
    path('admin/cart/', include('cart.admin_urls')),
    path('admin/catalog/', include('catalog.admin_urls')),
    path('admin/page_builder/', include('page_builder.admin_urls')),
    path('admin/media-library/', include('media_library.admin_urls')),
    path('admin/design/', include('design.admin_urls')),
    path('admin/seo-generator/', include('seo_generator.admin_urls')),
    path('admin/webhooks/', include('webhooks.urls')),
    path('admin/form_builder/', include('form_builder.urls')),
    path('admin/form_builder/', include('form_builder.admin_urls')),
    path('admin/search/', include('search.admin_urls')),
    path('admin/element-builder/', include('element_builder.admin_urls')),
    path('admin/geoip/', include('geoip.admin_urls')),
    path('admin/admin_api/', include('admin_api.admin_urls')),
    path('admin/pos/', include('pos_app.admin_urls')),
    path('admin/configurator-3d/', include('configurator_3d.admin_urls')),
    path('admin/customizable-product/', include('customizable_product.admin_urls')),
    path('admin/marketplace/', include('marketplace.urls')),
    path('admin/custom-fields/', include('custom_fields.urls')),
    path('admin/payout-providers/', include('payout_providers.urls')),
    path('admin/payout-providers/', include('payout_providers.admin_urls')),
    # Developer Portal Admin (only active on spwig.com when SPWIG_IS_HQ=true)
    *(
        [path('admin/developer_portal/', include('developer_portal.admin_urls'))]
        if getattr(settings, 'SPWIG_IS_HQ', False)
        else []
    ),
    path('admin/', admin.site.urls),  # Using custom rate-limited admin site (5 attempts/min)

    # Other apps that should support i18n
    path('media-library/', include('media_library.urls')),

    # Affiliate Marketing
    path('affiliate/', include('affiliate.urls')),

    # Customer Account Management (dashboard, addresses, subscriptions, payment methods)
    path('account/', include('accounts.urls')),

    # Developer Portal (only active on spwig.com when SPWIG_IS_HQ=true)
    *(
        [path('developers/', include('developer_portal.urls'))]
        if getattr(settings, 'SPWIG_IS_HQ', False)
        else []
    ),

    # Theme system URLs
    path('theme/', include('design.urls')),

    # Blog URLs
    path('blog/', include('blog.urls')),

    # Search URLs
    path('search/', include('search.urls')),

    # Frontend URLs
    path('', include('page_builder.urls')),

    prefix_default_language=True
)

# Serve media and static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# API Documentation URLs for Merchants and Developers
# These provide interactive API documentation for headless frontend development
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns += [
    # OpenAPI 3.0 schema generation (downloadable)
    path('admin/api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Interactive Swagger UI documentation (for testing APIs)
    path('admin/api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # ReDoc documentation (clean reference documentation)
    path('admin/api/docs/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
