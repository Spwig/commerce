"""
Admin URL configuration to add translation menu items
"""

from django.shortcuts import redirect
from django.urls import path


def redirect_to_translations(request):
    """Redirect to translations dashboard"""
    return redirect("/admin/translations/")


# This can be imported in admin customization if needed
translation_admin_urls = [
    path("translations/", redirect_to_translations, name="admin_translations_redirect"),
]
