from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StaffRolesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "staff_roles"
    verbose_name = _("Staff Roles")
