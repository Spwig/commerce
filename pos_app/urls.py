from django.urls import path, re_path
from . import views

app_name = 'pos_app'

urlpatterns = [
    # Built frontend assets (JS, CSS, SW, manifest, images)
    # The path kwarg includes 'assets/' prefix to match the dist/ directory structure
    path('assets/<path:path>', views.POSAssetView.as_view(), name='pos_asset',
         kwargs={'prefix': 'assets'}),
    path('sw.js', views.POSAssetView.as_view(), {'path': 'sw.js'}, name='pos_sw'),
    path('manifest.webmanifest', views.POSAssetView.as_view(), {'path': 'manifest.webmanifest'}, name='pos_manifest'),
    path('registerSW.js', views.POSAssetView.as_view(), {'path': 'registerSW.js'}, name='pos_register_sw'),
    re_path(r'^(?P<path>workbox-[\w.-]+\.js)$', views.POSAssetView.as_view(), name='pos_workbox'),

    # Root-level static files (logo, favicon, icons)
    re_path(r'^(?P<path>[\w.-]+\.(?:svg|png|ico|webp|jpg))$', views.POSAssetView.as_view(), name='pos_root_static'),

    # Customer-facing display (no login required)
    path('display/', views.POSCustomerDisplayView.as_view(), name='pos_display'),
    re_path(r'^display/.*$', views.POSCustomerDisplayView.as_view()),

    # SPA catch-all: any other /pos/* route serves index.html
    # React Router handles client-side routing
    path('', views.POSAppView.as_view(), name='pos_terminal'),
    re_path(r'^(?!assets/|sw\.js|manifest|registerSW).*$', views.POSAppView.as_view()),
]
