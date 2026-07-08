from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FormBuilderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'form_builder'
    verbose_name = _('Form Builder')
