from django.urls import path

from . import admin_views

app_name = "media_library_admin"

urlpatterns = [
    path(
        "imagesizepreset/filter/",
        admin_views.filter_image_size_presets,
        name="imagesizepreset_filter",
    ),
    path("mediaasset/filter/", admin_views.filter_media_assets, name="mediaasset_filter"),
    path("image-processing/", admin_views.image_processing_view, name="image_processing"),
    path("api/thumbnail-sizes/", admin_views.thumbnail_sizes_api, name="thumbnail_sizes_api"),
    path(
        "api/save-thumbnail-sizes/",
        admin_views.save_thumbnail_sizes_api,
        name="save_thumbnail_sizes_api",
    ),
    path(
        "api/delete-thumbnail-size/<int:size_id>/",
        admin_views.delete_thumbnail_size_api,
        name="delete_thumbnail_size_api",
    ),
    path("api/image-stats/", admin_views.image_stats_api, name="image_stats_api"),
    path(
        "api/regenerate-thumbnails/",
        admin_views.regenerate_thumbnails_view,
        name="regenerate_thumbnails",
    ),
    path(
        "api/regenerate-thumbnails-status/",
        admin_views.regenerate_thumbnails_status_view,
        name="regenerate_thumbnails_status",
    ),
]
