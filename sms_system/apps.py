from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SmsSystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sms_system'
    verbose_name = _('SMS System')
