"""Engine configuration — a single-row settings object.

Single-tenant by design (Site ID=1), like ``core.SiteSettings``. Holds the
active attribution model and its parameters. Because attribution is a
recomputable projection, changing ``active_model`` here does not migrate data —
it just changes which model the next resolution (or a re-run) applies.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from attribution.constants import ATTRIBUTION_MODEL_CHOICES, MODEL_LAST_NON_DIRECT


class AttributionSettings(models.Model):
    """Singleton configuration for the attribution engine."""

    active_model = models.CharField(
        max_length=32,
        choices=ATTRIBUTION_MODEL_CHOICES,
        default=MODEL_LAST_NON_DIRECT,
        verbose_name=_("active model"),
        help_text=_("Attribution model applied at resolution time."),
    )
    lookback_days = models.PositiveIntegerField(
        default=90,
        verbose_name=_("lookback window (days)"),
        help_text=_("How far before an order a touch may still receive credit."),
    )
    time_decay_half_life_days = models.PositiveIntegerField(
        default=7,
        verbose_name=_("time-decay half-life (days)"),
        help_text=_("Half-life for the time-decay model."),
    )

    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        verbose_name = _("attribution settings")
        verbose_name_plural = _("attribution settings")

    def __str__(self):
        return f"Attribution settings ({self.get_active_model_display()})"

    def save(self, *args, **kwargs):
        # Enforce the singleton.
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        obj, _created = cls.objects.get_or_create(pk=1)
        return obj
