from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PageBuilderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'page_builder'
    verbose_name = _('Page Builder')
