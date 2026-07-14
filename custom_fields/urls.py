"""
URL configuration for custom fields management (admin-facing, i18n).

These URLs live under /en/admin/custom-fields/ (inside i18n_patterns).
"""

from django.urls import path

from . import views

app_name = "custom_fields"

urlpatterns = [
    # Management page
    path("", views.management_view, name="management"),
    # Recycle bin
    path("recycle-bin/", views.recycle_bin_view, name="recycle_bin"),
    # Group CRUD (AJAX)
    path("groups/create/", views.create_group, name="create_group"),
    path("groups/<int:group_id>/update/", views.update_group, name="update_group"),
    path("groups/<int:group_id>/delete/", views.delete_group, name="delete_group"),
    path("groups/<int:group_id>/restore/", views.restore_group, name="restore_group"),
    path(
        "groups/<int:group_id>/permanent-delete/",
        views.permanent_delete_group,
        name="permanent_delete_group",
    ),
    # Field CRUD (AJAX)
    path("fields/create/", views.create_field, name="create_field"),
    path("fields/<int:field_id>/", views.get_field_detail, name="field_detail"),
    path("fields/<int:field_id>/update/", views.update_field, name="update_field"),
    path("fields/<int:field_id>/delete/", views.delete_field, name="delete_field"),
    path("fields/<int:field_id>/restore/", views.restore_field, name="restore_field"),
    path(
        "fields/<int:field_id>/permanent-delete/",
        views.permanent_delete_field,
        name="permanent_delete_field",
    ),
    # Reorder (AJAX)
    path("fields/reorder/", views.reorder_fields, name="reorder_fields"),
]
