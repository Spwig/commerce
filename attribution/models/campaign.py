"""Store-wide Campaign / Source model.

The unifying primitive the platform lacked: a single table every marketing
emitter (email, social auto-share, affiliate links, voucher codes) references
for its ``utm_campaign`` value, and that inbound capture resolves back to. A
campaign is orthogonal to channel — one campaign can span email + social +
paid search — so it rides *on top of* the channel label, it is not a channel.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class Campaign(models.Model):
    """A named marketing campaign that emitters tag links with and inbound
    touches resolve to by slug. Spans any number of channels."""

    name = models.CharField(max_length=255, verbose_name=_("name"))
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name=_("slug"),
        help_text=_("Used as the utm_campaign value on tagged links."),
    )
    channel_hint = models.CharField(
        max_length=32,
        blank=True,
        verbose_name=_("default channel"),
        help_text=_("Default channel emitters use when tagging this campaign."),
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name=_("active"),
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        verbose_name = _("campaign")
        verbose_name_plural = _("campaigns")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["is_active", "created_at"]),
        ]

    def __str__(self):
        return self.name
