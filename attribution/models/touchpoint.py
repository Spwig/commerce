"""The canonical touch stream and its identity spine.

``TouchPoint`` is append-only and raw: one row per arrival that carries a real
source signal. Nothing is interpreted destructively at capture time beyond a
cheap channel label, so any attribution model can be recomputed later over the
full history. This is what ``geoip.VisitorLocation`` cannot do — it keeps one
first-touch row per session and overwrites nothing after, which is fatal for
multi-touch. We keep ``VisitorLocation`` for geo/visitor analytics and record
attribution touches here instead.

``VisitorThread`` is the missing spine: a stable, first-party visitor identity
that survives Django's login session-key rotation and binds an anonymous touch
stream to a customer at login/checkout (mirroring the cart's proven
``guest_cart_id`` adoption in ``cart/signals.py``).
"""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from attribution.constants import CHANNEL_CHOICES, CHANNEL_UNKNOWN, CONSENT_CHOICES, CONSENT_UNKNOWN


class VisitorThread(models.Model):
    """A stable anonymous visitor identity, bound to a customer once known.

    Keyed by an opaque first-party ``visitor_key`` cookie that is independent
    of Django's rotating ``session_key``. When the same browser reaches login
    or checkout, ``customer`` is set and the visitor's touch stream is bound.
    Cross-device unification is intentionally out of scope and disclosed to
    merchants as a known limit.
    """

    visitor_key = models.CharField(
        max_length=64,
        unique=True,
        verbose_name=_("visitor key"),
        help_text=_("Opaque first-party visitor identifier (cookie-backed)."),
    )
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True,
        related_name="attribution_threads",
        verbose_name=_("customer"),
    )
    first_seen = models.DateTimeField(auto_now_add=True, verbose_name=_("first seen"))
    last_seen = models.DateTimeField(auto_now=True, verbose_name=_("last seen"))

    class Meta:
        verbose_name = _("visitor thread")
        verbose_name_plural = _("visitor threads")
        ordering = ["-last_seen"]
        indexes = [
            models.Index(fields=["customer", "last_seen"]),
        ]

    def __str__(self):
        who = self.customer_id or "anon"
        return f"VisitorThread {self.visitor_key[:8]}… ({who})"


class TouchPoint(models.Model):
    """A single recorded arrival with a source signal. Append-only; raw."""

    # Identity
    visitor_key = models.CharField(
        max_length=64,
        db_index=True,
        verbose_name=_("visitor key"),
        help_text=_("Stable anonymous id; survives session rotation."),
    )
    session_key = models.CharField(
        max_length=100,
        blank=True,
        db_index=True,
        verbose_name=_("session key"),
    )
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True,
        related_name="attribution_touchpoints",
        verbose_name=_("customer"),
        help_text=_("Backfilled when the visitor thread binds to a customer."),
    )
    occurred_at = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name=_("occurred at")
    )

    # Resolved label (see attribution.constants.CHANNEL_PRIORITY)
    channel = models.CharField(
        max_length=32,
        choices=CHANNEL_CHOICES,
        default=CHANNEL_UNKNOWN,
        db_index=True,
        verbose_name=_("channel"),
    )

    # Raw UTM signal
    source = models.CharField(max_length=255, blank=True, verbose_name=_("utm source"))
    medium = models.CharField(max_length=255, blank=True, verbose_name=_("utm medium"))
    campaign = models.CharField(max_length=255, blank=True, verbose_name=_("utm campaign"))
    term = models.CharField(max_length=255, blank=True, verbose_name=_("utm term"))
    content = models.CharField(max_length=255, blank=True, verbose_name=_("utm content"))

    # Paid-click identifiers (not captured anywhere in the platform today)
    gclid = models.CharField(max_length=255, blank=True, db_index=True, verbose_name=_("gclid"))
    fbclid = models.CharField(max_length=255, blank=True, db_index=True, verbose_name=_("fbclid"))
    msclkid = models.CharField(max_length=255, blank=True, verbose_name=_("msclkid"))

    # Inbound context (host only — full URL is unnecessary and privacy-heavier)
    referrer_host = models.CharField(
        max_length=255, blank=True, db_index=True, verbose_name=_("referrer host")
    )
    landing_path = models.CharField(max_length=512, blank=True, verbose_name=_("landing path"))

    # Resolved links
    campaign_ref = models.ForeignKey(
        "attribution.Campaign",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True,
        related_name="touchpoints",
        verbose_name=_("campaign"),
    )
    affiliate_click = models.ForeignKey(
        "affiliate.Click",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="attribution_touchpoints",
        verbose_name=_("affiliate click"),
    )
    referral_event = models.ForeignKey(
        "referrals.ReferralEvent",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="attribution_touchpoints",
        verbose_name=_("referral event"),
    )

    # Compliance / hygiene
    consent_state = models.CharField(
        max_length=16,
        choices=CONSENT_CHOICES,
        default=CONSENT_UNKNOWN,
        verbose_name=_("consent state"),
        help_text=_("Analytics-consent snapshot at capture time."),
    )
    is_bot = models.BooleanField(default=False, db_index=True, verbose_name=_("is bot"))
    device_type = models.CharField(max_length=16, blank=True, verbose_name=_("device type"))

    class Meta:
        verbose_name = _("touch point")
        verbose_name_plural = _("touch points")
        ordering = ["-occurred_at"]
        indexes = [
            models.Index(fields=["visitor_key", "occurred_at"]),
            models.Index(fields=["customer", "occurred_at"]),
            models.Index(fields=["channel", "occurred_at"]),
            models.Index(fields=["campaign_ref", "occurred_at"]),
        ]

    def __str__(self):
        return f"{self.get_channel_display()} touch @ {self.occurred_at:%Y-%m-%d %H:%M}"
