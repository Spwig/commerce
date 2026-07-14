from django.urls import path

from . import admin_views

app_name = "admin_api_admin"

urlpatterns = [
    path("customermessage/filter/", admin_views.filter_messages, name="filter_messages"),
    path(
        "customermessage/<int:message_id>/reply/",
        admin_views.reply_to_message,
        name="reply_to_message",
    ),
]
