from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SeoGeneratorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'seo_generator'
    verbose_name = _('SEO Generator')

    def ready(self):
        from . import signals  # noqa: F401
