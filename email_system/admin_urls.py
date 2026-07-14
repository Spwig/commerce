"""
Admin URL routing for Email System AJAX endpoints.
"""

from django.urls import path

from . import admin_views

app_name = "email_system_admin"

urlpatterns = [
    # EmailOutbox AJAX filter
    path("outbox/filter/", admin_views.filter_email_outbox, name="outbox_filter"),
    # EmailAccount AJAX actions
    path(
        "accounts/<uuid:account_id>/toggle-active/",
        admin_views.toggle_account_active,
        name="account_toggle_active",
    ),
    path(
        "accounts/<uuid:account_id>/set-default/",
        admin_views.set_account_default,
        name="account_set_default",
    ),
    path(
        "accounts/<uuid:account_id>/test-connection/",
        admin_views.test_account_connection,
        name="account_test_connection",
    ),
    path("accounts/<uuid:account_id>/delete/", admin_views.delete_account, name="account_delete"),
    path("accounts/bulk-action/", admin_views.bulk_account_action, name="account_bulk_action"),
]
