from django.urls import path

from . import admin_views

app_name = 'configurator_3d'

urlpatterns = [
    # Main scene manager page
    path('product/<int:product_id>/3d-scene/',
         admin_views.scene_setup, name='scene_setup'),

    # AJAX: Parse uploaded GLB file
    path('product/<int:product_id>/parse-glb/',
         admin_views.parse_glb_view, name='parse_glb'),

    # AJAX: Save scene config settings
    path('product/<int:product_id>/save-scene/',
         admin_views.save_scene_config, name='save_scene_config'),

    # AJAX: List all mappings for a scene
    path('product/<int:product_id>/mappings/',
         admin_views.list_mappings, name='list_mappings'),

    # AJAX: Create or update a mapping
    path('product/<int:product_id>/mappings/save/',
         admin_views.save_mapping, name='save_mapping'),

    # AJAX: Delete a mapping (scoped to product)
    path('product/<int:product_id>/mappings/<int:mapping_id>/delete/',
         admin_views.delete_mapping, name='delete_mapping'),

    # AJAX: Save/update geometry asset
    path('product/<int:product_id>/geometry-assets/save/',
         admin_views.save_geometry_asset, name='save_geometry_asset'),

    # AJAX: Delete geometry asset (scoped to product)
    path('product/<int:product_id>/geometry-assets/<int:asset_id>/delete/',
         admin_views.delete_geometry_asset, name='delete_geometry_asset'),

    # AJAX: List texture assets
    path('product/<int:product_id>/textures/',
         admin_views.list_textures, name='list_textures'),

    # AJAX: Save/update texture asset
    path('product/<int:product_id>/textures/save/',
         admin_views.save_texture_asset, name='save_texture_asset'),

    # AJAX: Delete texture asset (scoped to product)
    path('product/<int:product_id>/textures/<int:asset_id>/delete/',
         admin_views.delete_texture_asset, name='delete_texture_asset'),

    # AJAX: Capture thumbnail from 3D viewer
    path('product/<int:product_id>/capture-thumbnail/',
         admin_views.capture_thumbnail, name='capture_thumbnail'),
]
