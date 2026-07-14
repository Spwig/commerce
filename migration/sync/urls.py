"""
Sync API URL Configuration

Server-side endpoints exposed by every Spwig instance for Spwig-to-Spwig sync.
Authenticated via SyncToken (Authorization: SyncToken <token>).
"""

from django.urls import path

from . import api_views

app_name = "sync_api"

urlpatterns = [
    # Instance info
    path("info/", api_views.sync_info, name="info"),
    path("categories/", api_views.sync_categories, name="categories"),
    # Export (read data from this instance)
    # Media export MUST come before the <str:category> catch-all
    path("export/media/<int:asset_id>/", api_views.sync_media_export, name="media_export"),
    path("export/<str:category>/count/", api_views.sync_export_count, name="export_count"),
    path("export/<str:category>/", api_views.sync_export, name="export"),
    # Import (write data to this instance)
    # Media import MUST come before the <str:category> catch-all
    path("import/media/", api_views.sync_media_import, name="media_import"),
    path("import/<str:category>/preview/", api_views.sync_import_preview, name="import_preview"),
    path("import/<str:category>/", api_views.sync_import, name="import"),
    # Pre-flight check (for full migration)
    path("preflight/", api_views.sync_preflight, name="preflight"),
    # Token management (admin session auth, not SyncToken)
    path("tokens/", api_views.sync_token_list, name="token_list"),
    path("tokens/generate/", api_views.sync_token_generate, name="token_generate"),
    path("tokens/<int:token_id>/revoke/", api_views.sync_token_revoke, name="token_revoke"),
]
