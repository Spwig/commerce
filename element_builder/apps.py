from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ElementBuilderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'element_builder'
    verbose_name = _('Element Builder')
