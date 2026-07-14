from django.urls import path

from . import admin_views

app_name = "customizable_product"

urlpatterns = [
    # Design setup page
    path(
        "product/<int:product_id>/design-setup/",
        admin_views.design_setup,
        name="design_setup",
    ),
    # Surface CRUD
    path(
        "product/<int:product_id>/surfaces/",
        admin_views.list_surfaces,
        name="list_surfaces",
    ),
    path(
        "product/<int:product_id>/surfaces/save/",
        admin_views.save_surface,
        name="save_surface",
    ),
    path(
        "product/<int:product_id>/surfaces/<int:surface_id>/delete/",
        admin_views.delete_surface,
        name="delete_surface",
    ),
    # Template CRUD
    path(
        "product/<int:product_id>/templates/",
        admin_views.list_templates,
        name="list_templates",
    ),
    path(
        "product/<int:product_id>/templates/save/",
        admin_views.save_template,
        name="save_template",
    ),
    path(
        "product/<int:product_id>/templates/<int:template_id>/delete/",
        admin_views.delete_template,
        name="delete_template",
    ),
    # Thumbnail capture
    path(
        "product/<int:product_id>/capture-thumbnail/",
        admin_views.capture_thumbnail,
        name="capture_thumbnail",
    ),
    # Template visual editor
    path(
        "product/<int:product_id>/template-editor/",
        admin_views.template_editor,
        name="template_editor",
    ),
    # Design config save (pricing, settings)
    path(
        "product/<int:product_id>/save-config/",
        admin_views.save_config,
        name="save_config",
    ),
]
