from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EmailMarketingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "email_marketing"
    verbose_name = _("Campaign Studio")

    def ready(self):
        # Wire lifecycle signals that start triggered journeys (signup/order).
        from . import signals

        signals._connect_order_signal()
        # Roll email open/click events up onto CampaignSend (engagement metrics).
        signals._connect_engagement_signal()
