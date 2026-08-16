"""The recomputable, versioned attribution record.

Each row credits a share (``weight``) of an order's net revenue to one touch,
under one named attribution model (``model_version``). Rows are **immutable and
forward-only**: switching the active model or handling a refund writes a *new*
``model_version`` batch and leaves prior batches intact, mirroring the affiliate
``Commission`` invariant. The active attribution for an order is the newest
``model_version`` batch.

Money is a frozen snapshot (Decimal amount + currency string + base-currency
equivalent + the exchange rate used), not a live ``MoneyField`` — attribution
figures must be reproducible after the fact, exactly as commissions are. This
is the same deliberate exception the affiliate subsystem makes to the
platform's MoneyField rule.
"""

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from attribution.constants import CHANNEL_CHOICES, ROLE_CHOICES, ROLE_PRIMARY


class Attribution(models.Model):
    """One touch's credited share of one order's net revenue, under one model."""

    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="attributions",
        db_index=True,
        verbose_name=_("order"),
    )
    touchpoint = models.ForeignKey(
        "attribution.TouchPoint",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="attributions",
        verbose_name=_("touch point"),
    )

    # Denormalised for fast grouping without joining through the touch.
    channel = models.CharField(
        max_length=32, choices=CHANNEL_CHOICES, db_index=True, verbose_name=_("channel")
    )
    campaign_ref = models.ForeignKey(
        "attribution.Campaign",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True,
        related_name="attributions",
        verbose_name=_("campaign"),
    )

    model_version = models.CharField(
        max_length=32,
        db_index=True,
        verbose_name=_("model version"),
        help_text=_("Attribution model that produced this row."),
    )
    role = models.CharField(
        max_length=16,
        choices=ROLE_CHOICES,
        default=ROLE_PRIMARY,
        db_index=True,
        verbose_name=_("role"),
        help_text=_("Primary weights sum to 1.0 per order; assist is a separate lens."),
    )
    weight = models.DecimalField(
        max_digits=9,
        decimal_places=8,
        validators=[MinValueValidator(0)],
        verbose_name=_("weight"),
        help_text=_("Share of the order (0..1) credited to this touch."),
    )

    # Frozen money snapshot (see module docstring).
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_("amount"),
    )
    currency = models.CharField(max_length=3, blank=True, verbose_name=_("currency"))
    amount_base = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("base currency amount"),
    )
    base_currency = models.CharField(max_length=3, blank=True, verbose_name=_("base currency"))
    exchange_rate_used = models.DecimalField(
        max_digits=18,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name=_("exchange rate used"),
    )

    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name=_("created at")
    )
    # True only for rows in the newest batch for their order. Re-resolution
    # (model switch, refund) flips prior batches to False, so reporting reads
    # exactly one batch per order without racing on created_at timestamps.
    is_current = models.BooleanField(default=True, db_index=True, verbose_name=_("current"))

    class Meta:
        verbose_name = _("attribution")
        verbose_name_plural = _("attributions")
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["order", "touchpoint", "model_version", "role"],
                name="uniq_attribution_order_touch_model_role",
            ),
        ]
        indexes = [
            models.Index(fields=["order", "model_version"]),
            models.Index(fields=["channel", "created_at"]),
            models.Index(fields=["model_version", "role"]),
            models.Index(fields=["is_current", "channel"]),
        ]

    def __str__(self):
        return f"{self.get_channel_display()} {self.weight} of order {self.order_id}"

    @property
    def is_primary(self):
        return self.role == ROLE_PRIMARY
