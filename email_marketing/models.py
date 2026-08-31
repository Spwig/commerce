"""Data models for the Campaign Studio — Spwig's native email-marketing feature.

Four models make up the foundation:

* ``Subscriber`` — a marketing recipient, either a registered customer or an
  anonymous lead, unified into one audience.
* ``Segment`` — a saved, materialisable audience (dynamic rules or a static
  member list).
* ``Campaign`` — an authored email tied to a segment, plus its send state.
* ``CampaignSend`` — the per-recipient join that links a campaign to the
  ``email_system`` outbox and carries engagement state.

Consent is never re-implemented here: for registered subscribers it defers to
``accounts.CommunicationPreference``; anonymous subscribers carry their own
opt-in and double-opt-in verification state.
"""

import secrets
import uuid
from datetime import time

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField

from core.models import SoftDeleteModel

# Marketing message types recognised by the consent system
# (accounts.constants.MARKETING_EMAIL_TYPES). A campaign's message_type must be
# one of these so consent gating and unsubscribe links resolve correctly.
MESSAGE_TYPE_CHOICES = [
    ("newsletter", _("Newsletter")),
    ("promotional_offers", _("Promotional offers")),
    ("product_recommendations", _("Product recommendations")),
    ("back_in_stock", _("Back in stock")),
]


def generate_token() -> str:
    """Return a URL-safe unsubscribe/verification token."""
    return secrets.token_urlsafe(32)


class SubscriberTag(models.Model):
    """A merchant-defined label for organising subscribers and building segments.

    Tags are applied to subscribers (a many-to-many) and can be used as a
    ``has_tag`` condition in the segment rule-builder, so a merchant can slice
    their audience by their own labels (e.g. ``vip``, ``wholesale``, ``event``).
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    site = models.ForeignKey(
        "sites.Site",
        on_delete=models.CASCADE,
        related_name="subscriber_tags",
        verbose_name=_("site"),
    )
    name = models.CharField(max_length=50, verbose_name=_("name"))
    slug = models.SlugField(max_length=60, verbose_name=_("slug"))
    color = models.CharField(
        max_length=7,
        blank=True,
        default="",
        verbose_name=_("colour"),
        help_text=_("Optional hex colour for the tag chip, e.g. #2563eb."),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        verbose_name = _("subscriber tag")
        verbose_name_plural = _("subscriber tags")
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["site", "slug"], name="uniq_subscribertag_site_slug"),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify

            self.slug = slugify(self.name)[:60]
        super().save(*args, **kwargs)


class Subscriber(SoftDeleteModel):
    """A marketing-email recipient: a registered customer or an anonymous lead.

    Unifies account holders and anonymous emails (storefront signups, imports)
    into a single audience. Consent decisions defer to the linked customer's
    CommunicationPreference; anonymous subscribers carry their own opt-in and
    double-opt-in verification state and their own unsubscribe token.
    """

    STATUS_ACTIVE = "active"
    STATUS_UNSUBSCRIBED = "unsubscribed"
    STATUS_BOUNCED = "bounced"
    STATUS_COMPLAINED = "complained"
    STATUS_PENDING = "pending"
    STATUS_CHOICES = [
        (STATUS_ACTIVE, _("Active")),
        (STATUS_UNSUBSCRIBED, _("Unsubscribed")),
        (STATUS_BOUNCED, _("Bounced")),
        (STATUS_COMPLAINED, _("Complained")),
        (STATUS_PENDING, _("Pending confirmation")),
    ]

    SOURCE_CHOICES = [
        ("signup", _("Storefront signup")),
        ("import", _("Import")),
        ("order", _("Order")),
        ("manual", _("Added manually")),
        ("api", _("API")),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    site = models.ForeignKey(
        "sites.Site",
        on_delete=models.CASCADE,
        related_name="email_subscribers",
        verbose_name=_("site"),
    )

    email = models.EmailField(db_index=True, verbose_name=_("email"))

    # Names for anonymous subscribers (registered users' names come from the
    # linked account). Lets personalisation like [[first_name]] work for
    # imported / storefront-signup contacts too.
    first_name = models.CharField(max_length=100, blank=True, verbose_name=_("first name"))
    last_name = models.CharField(max_length=100, blank=True, verbose_name=_("last name"))

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="email_subscriber",
        verbose_name=_("linked user"),
        help_text=_("The customer account, when this subscriber is a registered user."),
    )

    status = models.CharField(
        max_length=16,
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE,
        db_index=True,
        verbose_name=_("status"),
    )

    source = models.CharField(
        max_length=16,
        choices=SOURCE_CHOICES,
        default="manual",
        verbose_name=_("source"),
    )

    tags = models.ManyToManyField(
        "SubscriberTag",
        related_name="subscribers",
        blank=True,
        verbose_name=_("tags"),
        help_text=_("Merchant-defined labels for organising and segmenting subscribers."),
    )

    language_code = models.CharField(
        max_length=10,
        blank=True,
        verbose_name=_("language"),
        help_text=_("Preferred language for campaigns, e.g. 'en', 'es'."),
    )

    # --- Consent (anonymous subscribers only; registered defer to CommunicationPreference) ---
    marketing_opt_in = models.BooleanField(
        default=False,
        verbose_name=_("marketing opt-in"),
        help_text=_("Whether an anonymous subscriber has opted into marketing email."),
    )
    marketing_verified = models.BooleanField(
        default=False,
        verbose_name=_("opt-in verified"),
        help_text=_("Double opt-in confirmed (anonymous subscribers)."),
    )
    verification_token = models.CharField(
        max_length=64, blank=True, verbose_name=_("verification token")
    )
    consent_source = models.CharField(max_length=32, blank=True, verbose_name=_("consent source"))
    consent_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name=_("consent IP"))
    consent_user_agent = models.TextField(blank=True, verbose_name=_("consent user agent"))
    consent_timestamp = models.DateTimeField(
        null=True, blank=True, verbose_name=_("consent timestamp")
    )

    unsubscribe_token = models.CharField(
        max_length=64,
        unique=True,
        default=generate_token,
        editable=False,
        verbose_name=_("unsubscribe token"),
    )

    # --- Engagement (denormalised) ---
    last_sent_at = models.DateTimeField(null=True, blank=True, verbose_name=_("last sent at"))
    last_opened_at = models.DateTimeField(null=True, blank=True, verbose_name=_("last opened at"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        verbose_name = _("subscriber")
        verbose_name_plural = _("subscribers")
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["site", "email"], name="uniq_subscriber_site_email"),
        ]
        indexes = [
            models.Index(fields=["site", "status"]),
            models.Index(fields=["unsubscribe_token"]),
        ]

    def __str__(self):
        return f"{self.email} ({self.get_status_display()})"

    @staticmethod
    def _double_opt_in_required() -> bool:
        """Whether anonymous opt-ins need email confirmation (merchant policy)."""
        try:
            from core.models import SiteSettings

            return bool(SiteSettings.get_settings().enable_double_opt_in)
        except Exception:
            return True  # fail safe: require confirmation

    def is_emailable(self, message_type: str = "newsletter") -> bool:
        """Return whether this subscriber may receive a marketing message now.

        Registered subscribers defer to their CommunicationPreference; anonymous
        subscribers must have opted in (and confirmed, when double opt-in is on).
        """
        if self.status != self.STATUS_ACTIVE:
            return False

        if self.user_id:
            from accounts.models import CommunicationPreference

            prefs, _ = CommunicationPreference.get_or_create_for_user(self.user)
            return prefs.should_send_email(message_type)

        # Anonymous subscriber
        if not self.marketing_opt_in:
            return False
        return not (self._double_opt_in_required() and not self.marketing_verified)


class Segment(SoftDeleteModel):
    """A saved, targetable audience — dynamic rules or a static member list.

    Dynamic segments resolve to an annotated Subscriber queryset at query time
    (never a per-user Python loop); static segments hold an explicit membership.
    """

    KIND_DYNAMIC = "dynamic"
    KIND_STATIC = "static"
    KIND_CHOICES = [
        (KIND_DYNAMIC, _("Dynamic (rules)")),
        (KIND_STATIC, _("Static (fixed list)")),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    site = models.ForeignKey(
        "sites.Site",
        on_delete=models.CASCADE,
        related_name="email_segments",
        verbose_name=_("site"),
    )

    name = models.CharField(max_length=200, verbose_name=_("name"))
    slug = models.SlugField(max_length=200, verbose_name=_("slug"))
    description = models.TextField(blank=True, verbose_name=_("description"))

    kind = models.CharField(
        max_length=16,
        choices=KIND_CHOICES,
        default=KIND_DYNAMIC,
        verbose_name=_("kind"),
    )

    rules = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("rules"),
        help_text=_("Rule tree evaluated for dynamic segments."),
    )

    members = models.ManyToManyField(
        Subscriber,
        blank=True,
        related_name="segments",
        verbose_name=_("members"),
        help_text=_("Explicit membership for static segments."),
    )

    is_active = models.BooleanField(default=True, db_index=True, verbose_name=_("active"))

    cached_count = models.PositiveIntegerField(default=0, verbose_name=_("cached member count"))
    last_built_at = models.DateTimeField(null=True, blank=True, verbose_name=_("last built at"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        verbose_name = _("segment")
        verbose_name_plural = _("segments")
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["site", "slug"], name="uniq_segment_site_slug"),
        ]

    def __str__(self):
        return f"{self.name} ({self.cached_count})"

    def resolve_queryset(self):
        """Return the Subscriber queryset this segment currently targets."""
        from email_marketing.services.segmentation import resolve_segment

        return resolve_segment(self)

    def rebuild(self):
        """Recompute and cache this segment's member count."""
        from email_marketing.services.segmentation import build_segment

        return build_segment(self)


class Campaign(SoftDeleteModel):
    """An authored marketing email, its target segment, and its send state.

    Content is authored as MJML in ``html_content`` today; ``content_tree`` is
    reserved for the visual block builder. Sending is delegated to the
    ``email_system`` render + provider stack via the campaign service.
    """

    STATUS_DRAFT = "draft"
    STATUS_SCHEDULED = "scheduled"
    STATUS_SENDING = "sending"
    STATUS_SENT = "sent"
    STATUS_PAUSED = "paused"
    STATUS_FAILED = "failed"
    STATUS_CHOICES = [
        (STATUS_DRAFT, _("Draft")),
        (STATUS_SCHEDULED, _("Scheduled")),
        (STATUS_SENDING, _("Sending")),
        (STATUS_SENT, _("Sent")),
        (STATUS_PAUSED, _("Paused")),
        (STATUS_FAILED, _("Failed")),
    ]

    # Campaign type — a broadcast is sent once; a recurring campaign is a
    # template that spawns a broadcast "occurrence" on each scheduled run.
    TYPE_BROADCAST = "broadcast"
    TYPE_RECURRING = "recurring"
    TYPE_CHOICES = [
        (TYPE_BROADCAST, _("Broadcast")),
        (TYPE_RECURRING, _("Recurring")),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    site = models.ForeignKey(
        "sites.Site",
        on_delete=models.CASCADE,
        related_name="email_campaigns",
        verbose_name=_("site"),
    )

    name = models.CharField(max_length=200, verbose_name=_("name"))
    subject = models.CharField(max_length=255, verbose_name=_("subject"))
    preview_text = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("preview text"),
        help_text=_("Preheader shown after the subject in most inboxes."),
    )

    message_type = models.CharField(
        max_length=32,
        choices=MESSAGE_TYPE_CHOICES,
        default="newsletter",
        verbose_name=_("message type"),
        help_text=_("Consent category this campaign is sent under."),
    )

    campaign_type = models.CharField(
        max_length=16,
        choices=TYPE_CHOICES,
        default=TYPE_BROADCAST,
        db_index=True,
        verbose_name=_("campaign type"),
        help_text=_("Broadcast sends once; recurring sends on a schedule."),
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="occurrences",
        verbose_name=_("recurring template"),
        help_text=_("For a recurring occurrence, the template it was spawned from."),
    )

    segment = models.ForeignKey(
        Segment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="campaigns",
        verbose_name=_("segment"),
    )

    from_account = models.ForeignKey(
        "email_system.EmailAccount",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="campaigns",
        verbose_name=_("from account"),
        help_text=_("Sending account; the default account is used when unset."),
    )

    content_tree = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("content tree"),
        help_text=_("Block tree authored by the visual builder (reserved)."),
    )
    html_content = models.TextField(
        blank=True,
        verbose_name=_("MJML content"),
        help_text=_("MJML source rendered to email-safe HTML at send time."),
    )

    status = models.CharField(
        max_length=16,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
        db_index=True,
        verbose_name=_("status"),
    )

    scheduled_for = models.DateTimeField(null=True, blank=True, verbose_name=_("scheduled for"))

    last_content_sent_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("last content sent at"),
        help_text=_(
            "Watermark for 'since last send' dynamic blocks — e.g. a Blog Posts "
            "block set to only include posts published after this time. Updated "
            "each time the campaign (or a recurring occurrence) finishes sending."
        ),
    )

    total_recipients = models.PositiveIntegerField(default=0, verbose_name=_("total recipients"))
    sent_count = models.PositiveIntegerField(default=0, verbose_name=_("sent"))
    failed_count = models.PositiveIntegerField(default=0, verbose_name=_("failed"))
    skipped_count = models.PositiveIntegerField(default=0, verbose_name=_("skipped"))

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_email_campaigns",
        verbose_name=_("created by"),
    )

    # Marketing-attribution link. ``attribution_slug`` is the stable per-campaign
    # ``utm_campaign`` value stamped on tracked links + the slug of the matching
    # ``attribution.Campaign`` row, so clicks that convert credit revenue back to
    # THIS campaign (not the coarse template_type). Set once (see
    # ``ensure_attribution_slug``) so a later rename never forks historical revenue.
    attribution_slug = models.SlugField(
        max_length=255,
        blank=True,
        db_index=True,
        verbose_name=_("attribution slug"),
        help_text=_("Stable utm_campaign value linking this campaign to revenue attribution."),
    )
    # Optional spend for ROAS (attributed revenue ÷ spend). Email is an owned
    # channel, so this is blank unless the merchant attributes send/creative cost.
    spend = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency="USD",
        null=True,
        blank=True,
        verbose_name=_("campaign spend"),
        help_text=_("Optional cost of this campaign; enables ROAS on the report."),
    )

    sent_at = models.DateTimeField(null=True, blank=True, verbose_name=_("sent at"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        verbose_name = _("campaign")
        verbose_name_plural = _("campaigns")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["site", "status"]),
            models.Index(fields=["status", "scheduled_for"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"

    def ensure_attribution_slug(self):
        """Return this campaign's stable attribution slug, minting it once.

        Format ``email-<slugified-name>-<id.hex>``: the name gives readability in
        attribution reports/URLs, the full uuid hex guarantees the globally-unique
        ``attribution.Campaign.slug`` (no collision-merge of two campaigns' revenue).
        Persisted on first call and never changed afterwards, so renaming the campaign
        can't split its revenue history. The value is fully deterministic from
        ``name``+``id`` — several call sites rely on that so any partial-persist failure
        reconciles on the next read; do not seed randomness into it.
        """
        if self.attribution_slug:
            return self.attribution_slug
        from django.utils.text import slugify

        name_part = slugify(self.name)[:40].strip("-") or "campaign"
        self.attribution_slug = f"email-{name_part}-{self.id.hex}"
        # Persist just this field; the campaign row already exists at send time.
        type(self).objects.filter(pk=self.pk).update(attribution_slug=self.attribution_slug)
        return self.attribution_slug


class CampaignSend(models.Model):
    """One recipient's copy of a campaign: the link to the outbox and engagement.

    This row is the batch worker's unit of work — it is created queued and the
    drainer sends the linked EmailOutbox — and the basis for per-campaign
    reporting once open/click events roll up.
    """

    STATUS_PENDING = "pending"
    STATUS_QUEUED = "queued"
    STATUS_SENDING = "sending"
    STATUS_SENT = "sent"
    STATUS_FAILED = "failed"
    STATUS_SKIPPED = "skipped"
    STATUS_CHOICES = [
        (STATUS_PENDING, _("Pending")),
        (STATUS_QUEUED, _("Queued")),
        (STATUS_SENDING, _("Sending")),
        (STATUS_SENT, _("Sent")),
        (STATUS_FAILED, _("Failed")),
        (STATUS_SKIPPED, _("Skipped")),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name="sends",
        verbose_name=_("campaign"),
    )

    subscriber = models.ForeignKey(
        Subscriber,
        on_delete=models.CASCADE,
        related_name="campaign_sends",
        verbose_name=_("subscriber"),
    )

    outbox = models.ForeignKey(
        "email_system.EmailOutbox",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="campaign_send",
        verbose_name=_("outbox entry"),
    )

    variant = models.CharField(max_length=32, blank=True, verbose_name=_("A/B variant"))

    status = models.CharField(
        max_length=16,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        db_index=True,
        verbose_name=_("status"),
    )
    skip_reason = models.CharField(max_length=100, blank=True, verbose_name=_("skip reason"))

    opened = models.BooleanField(default=False, verbose_name=_("opened"))
    clicked = models.BooleanField(default=False, verbose_name=_("clicked"))
    opened_at = models.DateTimeField(null=True, blank=True, verbose_name=_("opened at"))
    clicked_at = models.DateTimeField(null=True, blank=True, verbose_name=_("clicked at"))

    # Delivery failures, rolled up from EmailEvent onto this send for per-campaign
    # reporting (separate from the address-level suppression list).
    bounced = models.BooleanField(default=False, verbose_name=_("bounced"))
    complained = models.BooleanField(default=False, verbose_name=_("complained"))
    bounce_type = models.CharField(
        max_length=16, blank=True, verbose_name=_("bounce type")
    )  # hard / soft / transient (from EmailEvent)
    bounced_at = models.DateTimeField(null=True, blank=True, verbose_name=_("bounced at"))
    complained_at = models.DateTimeField(null=True, blank=True, verbose_name=_("complained at"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        verbose_name = _("campaign send")
        verbose_name_plural = _("campaign sends")
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["campaign", "subscriber"], name="uniq_campaignsend_campaign_subscriber"
            ),
        ]
        indexes = [
            models.Index(fields=["campaign", "status"]),
        ]

    def __str__(self):
        return f"{self.campaign_id} → {self.subscriber_id} ({self.status})"


class CampaignBlock(models.Model):
    """One block in a campaign's visual composition (the edit source of truth).

    Blocks are ordered rows authored in the visual builder. On save they are
    serialised into the campaign's MJML (``Campaign.html_content``), so the
    existing send path renders and delivers them unchanged. ``block_type`` names
    a registered block (see ``email_marketing/blocks/<type>/``); ``content``
    holds that block's editable property values.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name="blocks",
        verbose_name=_("campaign"),
    )

    block_type = models.CharField(max_length=64, verbose_name=_("block type"))
    content = models.JSONField(default=dict, blank=True, verbose_name=_("content"))
    order = models.PositiveIntegerField(default=0, db_index=True, verbose_name=_("order"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        verbose_name = _("campaign block")
        verbose_name_plural = _("campaign blocks")
        ordering = ["order", "created_at"]
        indexes = [
            models.Index(fields=["campaign", "order"]),
        ]

    def __str__(self):
        return f"{self.block_type} #{self.order} ({self.campaign_id})"


class CampaignSchedule(models.Model):
    """Recurrence for a recurring campaign template.

    A recurring Campaign is a *template*: it never sends itself. This schedule
    drives a beat task that, at each ``next_run_at``, spawns a broadcast
    *occurrence* (a snapshot of the template's rendered content) and sends it —
    or skips/holds it when the merchant's freshness policy says there's nothing
    new to send (so a blog/product digest never re-sends the same content).
    """

    CADENCE_DAILY = "daily"
    CADENCE_WEEKLY = "weekly"
    CADENCE_MONTHLY = "monthly"
    CADENCE_CHOICES = [
        (CADENCE_DAILY, _("Daily")),
        (CADENCE_WEEKLY, _("Weekly")),
        (CADENCE_MONTHLY, _("Monthly")),
    ]

    # What to do when a run finds no fresh content for its delta-aware blocks.
    POLICY_SKIP = "skip"
    POLICY_SEND_PARTIAL = "send_partial"
    POLICY_HOLD = "hold"
    FRESHNESS_CHOICES = [
        (POLICY_SKIP, _("Skip this send")),
        (POLICY_SEND_PARTIAL, _("Send anyway (omit empty blocks)")),
        (POLICY_HOLD, _("Hold and send late when there's new content")),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    campaign = models.OneToOneField(
        Campaign,
        on_delete=models.CASCADE,
        related_name="schedule",
        verbose_name=_("campaign"),
    )

    cadence = models.CharField(
        max_length=16, choices=CADENCE_CHOICES, default=CADENCE_WEEKLY, verbose_name=_("cadence")
    )
    interval = models.PositiveSmallIntegerField(
        default=1,
        verbose_name=_("interval"),
        help_text=_("Every N cadence units (e.g. every 2 weeks)."),
    )
    weekday = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name=_("weekday"),
        help_text=_("0=Monday … 6=Sunday (weekly)."),
    )
    day_of_month = models.PositiveSmallIntegerField(
        null=True, blank=True, verbose_name=_("day of month"), help_text=_("1–28 (monthly).")
    )
    send_time = models.TimeField(default=time(9, 0), verbose_name=_("send time"))
    timezone = models.CharField(
        max_length=64,
        default="UTC",
        verbose_name=_("timezone"),
        help_text=_("IANA name, e.g. Europe/London."),
    )

    freshness_policy = models.CharField(
        max_length=16,
        choices=FRESHNESS_CHOICES,
        default=POLICY_SKIP,
        verbose_name=_("no-new-content policy"),
    )
    hold_days = models.PositiveSmallIntegerField(
        default=3,
        verbose_name=_("hold window (days)"),
        help_text=_("For the hold policy: how long to wait for new content before giving up."),
    )
    hold_until = models.DateTimeField(null=True, blank=True, verbose_name=_("holding until"))

    is_active = models.BooleanField(default=True, db_index=True, verbose_name=_("active"))
    next_run_at = models.DateTimeField(
        null=True, blank=True, db_index=True, verbose_name=_("next run at")
    )
    last_run_at = models.DateTimeField(null=True, blank=True, verbose_name=_("last run at"))
    occurrences_sent = models.PositiveIntegerField(default=0, verbose_name=_("occurrences sent"))

    # Optional per-occurrence A/B test (subject-line only). With 2+ subjects set,
    # each occurrence splits its audience, tests the subjects, and auto-sends the
    # winner — reusing the broadcast A/B engine one occurrence at a time.
    ab_test_subjects = models.JSONField(
        default=list, blank=True, verbose_name=_("A/B subject lines")
    )
    ab_sample_percent = models.PositiveSmallIntegerField(
        default=20,
        validators=[MinValueValidator(2), MaxValueValidator(100)],
        verbose_name=_("A/B test sample %"),
    )
    ab_test_window_hours = models.PositiveSmallIntegerField(
        default=4,
        validators=[MinValueValidator(1), MaxValueValidator(168)],
        verbose_name=_("A/B test window (hours)"),
    )
    ab_winner_metric = models.CharField(
        max_length=16,
        choices=[("opens", _("Open rate")), ("clicks", _("Click rate"))],
        default="opens",
        verbose_name=_("A/B winner metric"),
    )
    ab_auto_send_winner = models.BooleanField(default=True, verbose_name=_("A/B auto-send winner"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        verbose_name = _("campaign schedule")
        verbose_name_plural = _("campaign schedules")
        indexes = [
            models.Index(fields=["is_active", "next_run_at"]),
        ]

    def __str__(self):
        return f"{self.get_cadence_display()} schedule for {self.campaign_id}"

    @property
    def ab_subjects(self) -> list:
        """The cleaned, de-blanked subject lines configured for the A/B test."""
        return [s.strip() for s in (self.ab_test_subjects or []) if str(s).strip()]

    @property
    def ab_enabled(self) -> bool:
        """A per-occurrence subject A/B runs only when at least two subjects are set."""
        return len(self.ab_subjects) >= 2

    def save(self, *args, **kwargs):
        # Self-arm: an active schedule with no next run computes its first fire
        # time, so creating one in the admin is enough to start the recurrence.
        if self.is_active and self.next_run_at is None:
            from email_marketing.services.recurrence import compute_next_run

            self.next_run_at = compute_next_run(self)
        super().save(*args, **kwargs)


class ABTest(models.Model):
    """An A/B test attached to a *container* campaign (its 1:1 sidecar).

    The container is the campaign the merchant builds; it is never sent directly.
    Each ``ABVariant`` is a child campaign sent to an even slice of a
    ``sample_percent`` sample of the audience; after ``test_window_hours`` the
    winner is chosen by ``winner_metric`` and, if ``auto_send_winner``, sent to
    the held-out remainder. ``sample_percent = 100`` means a pure split test with
    no holdout. Because a variant carries its own subject *and* content, the
    engine is the same whether the merchant varied the subject, the design, or both.
    """

    TYPE_SUBJECT = "subject"
    TYPE_CONTENT = "content"
    TYPE_CHOICES = [
        (TYPE_SUBJECT, _("Subject line")),
        (TYPE_CONTENT, _("Content")),
    ]

    METRIC_OPENS = "opens"
    METRIC_CLICKS = "clicks"
    METRIC_CHOICES = [
        (METRIC_OPENS, _("Open rate")),
        (METRIC_CLICKS, _("Click rate")),
    ]

    # A winner is "significant" once we're this confident it beat the runner-up.
    SIGNIFICANCE_THRESHOLD = 0.95

    STATUS_DRAFT = "draft"
    STATUS_TESTING = "testing"
    STATUS_COMPLETE = "complete"
    STATUS_CANCELLED = "cancelled"
    STATUS_CHOICES = [
        (STATUS_DRAFT, _("Draft")),
        (STATUS_TESTING, _("Testing")),
        (STATUS_COMPLETE, _("Complete")),
        (STATUS_CANCELLED, _("Cancelled")),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    campaign = models.OneToOneField(
        Campaign,
        on_delete=models.CASCADE,
        related_name="ab_test",
        verbose_name=_("campaign"),
    )
    test_type = models.CharField(
        max_length=16, choices=TYPE_CHOICES, default=TYPE_SUBJECT, verbose_name=_("what to test")
    )
    winner_metric = models.CharField(
        max_length=16, choices=METRIC_CHOICES, default=METRIC_OPENS, verbose_name=_("winner by")
    )
    sample_percent = models.PositiveSmallIntegerField(
        default=20,
        validators=[MinValueValidator(2), MaxValueValidator(100)],
        verbose_name=_("test sample %"),
        help_text=_(
            "Share of the audience used for the test (split evenly across variants). The rest receives the winner. 100 = pure split test, no holdout."
        ),
    )
    test_window_hours = models.PositiveSmallIntegerField(
        default=4,
        validators=[MinValueValidator(1), MaxValueValidator(168)],
        verbose_name=_("test window (hours)"),
    )
    auto_send_winner = models.BooleanField(default=True, verbose_name=_("auto-send winner"))

    status = models.CharField(
        max_length=16,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
        db_index=True,
        verbose_name=_("status"),
    )
    decide_at = models.DateTimeField(
        null=True, blank=True, db_index=True, verbose_name=_("decide at")
    )
    winner = models.ForeignKey(
        "ABVariant",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name=_("winner"),
    )
    winner_confidence = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_("winner confidence"),
        help_text=_("Statistical confidence (0–1) that the winner beat the runner-up."),
    )
    started_at = models.DateTimeField(null=True, blank=True, verbose_name=_("started at"))
    decided_at = models.DateTimeField(null=True, blank=True, verbose_name=_("decided at"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        verbose_name = _("A/B test")
        verbose_name_plural = _("A/B tests")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "decide_at"]),
        ]

    def __str__(self):
        return f"A/B test ({self.get_test_type_display()}) for {self.campaign_id}"


class ABVariant(models.Model):
    """One arm of an A/B test: a child campaign sent to a slice of the audience.

    The variant campaign carries this arm's subject and content. Result columns
    are snapshotted at decision time so a completed test reads without re-querying
    the sends.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ab_test = models.ForeignKey(
        ABTest, on_delete=models.CASCADE, related_name="variants", verbose_name=_("A/B test")
    )
    label = models.CharField(max_length=4, verbose_name=_("label"))
    campaign = models.OneToOneField(
        Campaign,
        on_delete=models.CASCADE,
        related_name="ab_variant",
        verbose_name=_("variant campaign"),
    )
    # Result snapshot (filled by decide_ab_test).
    recipients = models.PositiveIntegerField(default=0, verbose_name=_("recipients"))
    opened = models.PositiveIntegerField(default=0, verbose_name=_("opened"))
    clicked = models.PositiveIntegerField(default=0, verbose_name=_("clicked"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        verbose_name = _("A/B variant")
        verbose_name_plural = _("A/B variants")
        ordering = ["label"]
        constraints = [
            models.UniqueConstraint(fields=["ab_test", "label"], name="uniq_abvariant_test_label"),
        ]

    def __str__(self):
        return f"Variant {self.label}"

    def rate(self, metric) -> float:
        """Open- or click-rate over recipients, in [0, 1]. Zero recipients → 0."""
        if not self.recipients:
            return 0.0
        wins = self.clicked if metric == ABTest.METRIC_CLICKS else self.opened
        return wins / self.recipients


class Journey(SoftDeleteModel):
    """A triggered email automation, modelled as a graph (a flowchart).

    A journey is started for a subscriber by a lifecycle event (signup, order).
    Its ``JourneyNode`` graph — sends, waits, branches and exits joined by
    ``JourneyEdge`` — is walked per subscriber by the orchestrator, which can
    fork down Yes/No paths at a branch. Progress is tracked per subscriber by a
    ``JourneyEnrollment`` pointing at the subscriber's *current node*, so the
    same node can fire across separate enrollments (e.g. an order-triggered
    series firing once per order).
    """

    TRIGGER_SIGNUP = "customer_signup"
    TRIGGER_ORDER_PLACED = "order_placed"
    TRIGGER_FIRST_ORDER = "first_order"
    TRIGGER_CART_ABANDONED = "cart_abandoned"
    TRIGGER_WIN_BACK = "win_back"
    TRIGGER_ORDER_DELIVERED = "order_delivered"
    TRIGGER_BACK_IN_STOCK = "back_in_stock"
    TRIGGER_CHOICES = [
        (TRIGGER_SIGNUP, _("Customer signs up")),
        (TRIGGER_ORDER_PLACED, _("Order is placed")),
        (TRIGGER_FIRST_ORDER, _("First order is placed")),
        (TRIGGER_CART_ABANDONED, _("Cart abandoned")),
        (TRIGGER_WIN_BACK, _("Customer lapsed (win-back)")),
        (TRIGGER_ORDER_DELIVERED, _("Order delivered")),
        (TRIGGER_BACK_IN_STOCK, _("Product back in stock")),
    ]

    STATUS_DRAFT = "draft"
    STATUS_ACTIVE = "active"
    STATUS_PAUSED = "paused"
    STATUS_CHOICES = [
        (STATUS_DRAFT, _("Draft")),
        (STATUS_ACTIVE, _("Active")),
        (STATUS_PAUSED, _("Paused")),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    site = models.ForeignKey(
        "sites.Site",
        on_delete=models.CASCADE,
        related_name="email_journeys",
        verbose_name=_("site"),
    )

    name = models.CharField(max_length=200, verbose_name=_("name"))
    trigger_event = models.CharField(
        max_length=32,
        choices=TRIGGER_CHOICES,
        db_index=True,
        verbose_name=_("trigger"),
        help_text=_("The lifecycle event that starts this journey for a subscriber."),
    )
    target_segment = models.ForeignKey(
        Segment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="journeys",
        verbose_name=_("only for segment"),
        help_text=_("If set, only subscribers in this segment are enrolled."),
    )
    once_per_subscriber = models.BooleanField(
        default=True,
        verbose_name=_("once per subscriber"),
        help_text=_("Enroll each subscriber at most once, ever (e.g. a welcome series)."),
    )
    cooldown_days = models.PositiveSmallIntegerField(
        default=0,
        verbose_name=_("re-enrollment cooldown (days)"),
        help_text=_("When re-enrollment is allowed, the minimum days between enrollments."),
    )

    status = models.CharField(
        max_length=16,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
        db_index=True,
        verbose_name=_("status"),
    )

    enrolled_count = models.PositiveIntegerField(default=0, verbose_name=_("enrolled"))
    completed_count = models.PositiveIntegerField(default=0, verbose_name=_("completed"))

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="email_journeys",
        verbose_name=_("created by"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        verbose_name = _("journey")
        verbose_name_plural = _("journeys")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["site", "status", "trigger_event"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_trigger_event_display()})"

    @property
    def is_live(self) -> bool:
        return self.status == self.STATUS_ACTIVE


class JourneyNode(models.Model):
    """One node in a journey's flowchart: an action, a wait, a branch, or an end.

    Behaviour is keyed on ``node_type``; per-type settings live in ``config``:

    * ``entry``      — the graph's root; display mirrors the journey's trigger and
      audience. No config.
    * ``send_email`` — ``{"campaign_id": "<uuid>"}``: send that Campaign, then continue.
    * ``wait_delay`` — ``{"value": 2, "unit": "days"}``: pause the enrollment.
    * ``branch``     — ``{"condition": "in_segment", "segment_id": "<uuid>"}``: route
      the enrollment down the ``yes`` or ``no`` edge.
    * ``exit``       — end the enrollment (also implied by a node with no out-edge).
    """

    TYPE_ENTRY = "entry"
    TYPE_SEND_EMAIL = "send_email"
    TYPE_WAIT_DELAY = "wait_delay"
    TYPE_BRANCH = "branch"
    TYPE_EXIT = "exit"
    TYPE_CHOICES = [
        (TYPE_ENTRY, _("Entry")),
        (TYPE_SEND_EMAIL, _("Send email")),
        (TYPE_WAIT_DELAY, _("Wait")),
        (TYPE_BRANCH, _("Branch")),
        (TYPE_EXIT, _("Exit")),
    ]

    UNIT_HOURS = "hours"
    UNIT_DAYS = "days"
    UNIT_CHOICES = [
        (UNIT_HOURS, _("hours")),
        (UNIT_DAYS, _("days")),
    ]

    # Branch conditions the orchestrator can evaluate. Extensible; ``in_segment``
    # reuses the Segment engine (see services/journeys.py::_evaluate_branch).
    CONDITION_IN_SEGMENT = "in_segment"
    CONDITION_CHOICES = [
        (CONDITION_IN_SEGMENT, _("Subscriber is in segment")),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    journey = models.ForeignKey(
        Journey, on_delete=models.CASCADE, related_name="nodes", verbose_name=_("journey")
    )
    node_type = models.CharField(
        max_length=16, choices=TYPE_CHOICES, db_index=True, verbose_name=_("type")
    )
    pos_x = models.IntegerField(default=0, verbose_name=_("canvas x"))
    pos_y = models.IntegerField(default=0, verbose_name=_("canvas y"))
    config = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("configuration"),
        help_text=_("Node-type-specific settings (campaign, wait, branch condition)."),
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        verbose_name = _("journey node")
        verbose_name_plural = _("journey nodes")
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["journey", "node_type"]),
        ]

    def __str__(self):
        return f"{self.get_node_type_display()} node of {self.journey_id}"

    def delay(self):
        """A ``wait_delay`` node's pause as a timedelta (zero for other types)."""
        from datetime import timedelta

        if self.node_type != self.TYPE_WAIT_DELAY:
            return timedelta(0)
        value = int(self.config.get("value") or 0)
        if self.config.get("unit") == self.UNIT_HOURS:
            return timedelta(hours=value)
        return timedelta(days=value)

    # --- A/B testing (a send_email node can split-test content or subjects) ------

    AB_LABELS = ("A", "B", "C", "D")

    def ab_variant_values(self) -> list:
        """Ordered A/B arm values: campaign ids (content test) or subject lines
        (subject test). Empty unless this is a send node configured for A/B."""
        if self.node_type != self.TYPE_SEND_EMAIL:
            return []
        test_type = self.config.get("ab_test_type")
        if test_type == "content":
            return [v for v in (self.config.get("variant_campaign_ids") or []) if v]
        if test_type == "subject":
            return [v for v in (self.config.get("variant_subjects") or []) if str(v).strip()]
        return []

    @property
    def is_ab_send(self) -> bool:
        """True when this send node runs an A/B test (two or more variants)."""
        return len(self.ab_variant_values()) >= 2

    def ab_labels(self) -> list:
        """Variant labels (A, B, …) for the configured arms."""
        return list(self.AB_LABELS[: len(self.ab_variant_values())])

    @property
    def ab_winner_label(self) -> str:
        """The locked-in winning label, once the auto-optimiser has decided."""
        return self.config.get("ab_winner_label") or ""

    @property
    def ab_metric(self) -> str:
        """Winner metric — 'opens' (default) or 'clicks'."""
        return "clicks" if self.config.get("ab_metric") == "clicks" else "opens"


class JourneyEdge(models.Model):
    """A directed connection between two journey nodes.

    ``branch`` labels which output a connection leaves by: ``default`` for a
    linear step, or ``yes`` / ``no`` for the two outputs of a ``branch`` node.
    """

    BRANCH_DEFAULT = "default"
    BRANCH_YES = "yes"
    BRANCH_NO = "no"
    BRANCH_CHOICES = [
        (BRANCH_DEFAULT, _("Default")),
        (BRANCH_YES, _("Yes")),
        (BRANCH_NO, _("No")),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    journey = models.ForeignKey(
        Journey, on_delete=models.CASCADE, related_name="edges", verbose_name=_("journey")
    )
    from_node = models.ForeignKey(
        JourneyNode, on_delete=models.CASCADE, related_name="out_edges", verbose_name=_("from")
    )
    to_node = models.ForeignKey(
        JourneyNode, on_delete=models.CASCADE, related_name="in_edges", verbose_name=_("to")
    )
    branch = models.CharField(
        max_length=8,
        choices=BRANCH_CHOICES,
        default=BRANCH_DEFAULT,
        verbose_name=_("path"),
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))

    class Meta:
        verbose_name = _("journey edge")
        verbose_name_plural = _("journey edges")
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["journey"]),
            models.Index(fields=["from_node", "branch"]),
        ]

    def __str__(self):
        return f"{self.from_node_id} → {self.to_node_id} ({self.branch})"


class JourneyEnrollment(models.Model):
    """One subscriber's progress through a journey."""

    STATUS_ACTIVE = "active"
    STATUS_COMPLETED = "completed"
    STATUS_CANCELLED = "cancelled"
    STATUS_CHOICES = [
        (STATUS_ACTIVE, _("Active")),
        (STATUS_COMPLETED, _("Completed")),
        (STATUS_CANCELLED, _("Cancelled")),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    journey = models.ForeignKey(
        Journey, on_delete=models.CASCADE, related_name="enrollments", verbose_name=_("journey")
    )
    subscriber = models.ForeignKey(
        Subscriber,
        on_delete=models.CASCADE,
        related_name="journey_enrollments",
        verbose_name=_("subscriber"),
    )
    current_node = models.ForeignKey(
        JourneyNode,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="enrollments",
        verbose_name=_("current node"),
        help_text=_("The node the subscriber is currently sitting at."),
    )
    next_step_at = models.DateTimeField(
        db_index=True,
        verbose_name=_("next step at"),
        help_text=_("When the current node is due to run."),
    )
    status = models.CharField(
        max_length=16,
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE,
        db_index=True,
        verbose_name=_("status"),
    )
    # Event payload for the enrollment (e.g. {"cart_id": 123} / {"order_id": 45}),
    # read at send time so a trigger email can render the actual cart items / product.
    context = models.JSONField(default=dict, blank=True, verbose_name=_("trigger context"))
    # Stable per-instance key of what triggered this enrollment (e.g. "cart:123",
    # "order:45"). Enables "once per cart/order" dedup and targeted cancellation
    # (e.g. cancel the cart-abandonment journey when that cart converts).
    trigger_ref = models.CharField(
        max_length=100, blank=True, db_index=True, verbose_name=_("trigger reference")
    )

    started_at = models.DateTimeField(auto_now_add=True, verbose_name=_("started at"))
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name=_("completed at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        verbose_name = _("journey enrollment")
        verbose_name_plural = _("journey enrollments")
        ordering = ["-started_at"]
        indexes = [
            models.Index(fields=["status", "next_step_at"]),
            models.Index(fields=["journey", "subscriber"]),
            models.Index(fields=["trigger_ref", "status"]),
        ]

    def __str__(self):
        return f"{self.subscriber_id} in {self.journey_id} (at {self.current_node_id})"


class JourneyStepSend(models.Model):
    """One email sent to one enrollee at a send node — the per-send record that lets a
    journey step's opens/clicks be attributed. ``variant`` is the A/B arm ("A"/"B"/…)
    or ``""`` for a plain (non-A/B) step.

    Journey sends create no CampaignSend (a subscriber may get the same step email
    across re-enrollments, which the CampaignSend (campaign, subscriber) uniqueness
    forbids), so this row — keyed by the sent email's ``outbox_id`` — is what the
    engagement rollup stamps, the per-step report aggregates, and the A/B
    auto-optimiser reads (per labelled arm) to pick a winner.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    node = models.ForeignKey(
        JourneyNode,
        on_delete=models.CASCADE,
        related_name="variant_sends",
        verbose_name=_("send node"),
    )
    enrollment = models.ForeignKey(
        JourneyEnrollment,
        on_delete=models.CASCADE,
        related_name="variant_sends",
        verbose_name=_("enrollment"),
    )
    variant = models.CharField(max_length=4, verbose_name=_("variant"))
    outbox_id = models.UUIDField(db_index=True, verbose_name=_("outbox id"))

    opened = models.BooleanField(default=False, verbose_name=_("opened"))
    clicked = models.BooleanField(default=False, verbose_name=_("clicked"))
    opened_at = models.DateTimeField(null=True, blank=True, verbose_name=_("opened at"))
    clicked_at = models.DateTimeField(null=True, blank=True, verbose_name=_("clicked at"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        verbose_name = _("journey step send")
        verbose_name_plural = _("journey step sends")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["node", "variant"]),
        ]

    def __str__(self):
        return f"{self.node_id} variant {self.variant} → {self.enrollment_id}"


class SuppressionEntry(SoftDeleteModel):
    """An email address that must never receive marketing mail (list hygiene).

    A hard bounce, a spam complaint, or a manual block suppresses an *address*,
    not a Subscriber row — so it holds even for a future or re-created subscriber
    with the same email, and regardless of that subscriber's consent state. The
    send path checks this before queuing; releasing an entry (soft-delete) lets
    the address receive mail again.
    """

    REASON_HARD_BOUNCE = "hard_bounce"
    REASON_COMPLAINT = "complaint"
    REASON_SOFT_BOUNCE = "soft_bounce"
    REASON_MANUAL = "manual"
    REASON_CHOICES = [
        (REASON_HARD_BOUNCE, _("Hard bounce")),
        (REASON_COMPLAINT, _("Spam complaint")),
        (REASON_SOFT_BOUNCE, _("Repeated soft bounces")),
        (REASON_MANUAL, _("Manually blocked")),
    ]

    SOURCE_SMTP_REJECT = "smtp_reject"
    SOURCE_GATEWAY_POLL = "gateway_poll"
    SOURCE_WEBHOOK = "webhook"
    SOURCE_MANUAL = "manual"
    SOURCE_CHOICES = [
        (SOURCE_SMTP_REJECT, _("Rejected at send")),
        (SOURCE_GATEWAY_POLL, _("Mail gateway")),
        (SOURCE_WEBHOOK, _("Provider webhook")),
        (SOURCE_MANUAL, _("Added manually")),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    site = models.ForeignKey(
        "sites.Site",
        on_delete=models.CASCADE,
        related_name="email_suppressions",
        verbose_name=_("site"),
    )

    email = models.EmailField(db_index=True, verbose_name=_("email"))

    reason = models.CharField(max_length=16, choices=REASON_CHOICES, verbose_name=_("reason"))
    source = models.CharField(
        max_length=16, choices=SOURCE_CHOICES, default=SOURCE_MANUAL, verbose_name=_("source")
    )
    detail = models.TextField(
        blank=True,
        verbose_name=_("detail"),
        help_text=_("Bounce reason or note explaining the suppression."),
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        verbose_name = _("suppressed address")
        verbose_name_plural = _("suppressed addresses")
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["site", "email"], name="uniq_suppression_site_email"),
        ]

    def __str__(self):
        return f"{self.email} ({self.get_reason_display()})"
