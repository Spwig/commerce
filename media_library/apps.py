from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MediaLibraryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "media_library"
    verbose_name = _("Media Library")
