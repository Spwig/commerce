"""Shared vocabulary for the revenue attribution engine.

Channels are the resolved, human-meaningful label for *where a touch came
from*. They are deliberately separate from the raw ``utm_medium`` string a
touch may carry: many mediums collapse into one channel, and some channels
(affiliate, referral) are identified by first-party markers, not UTM at all.

The ordering of ``CHANNEL_PRIORITY`` is the collision hierarchy: when a single
arrival carries more than one signal, the highest-priority channel wins as the
touch's label. This is orthogonal to how revenue is *split* across a journey —
that is the attribution model's job (see ``services/resolution``).
"""

from django.utils.translation import gettext_lazy as _

# Channel identifiers
CHANNEL_AFFILIATE = "affiliate"
CHANNEL_REFERRAL = "referral"  # customer refer-a-friend
CHANNEL_PAID_SEARCH = "paid_search"
CHANNEL_PAID_SOCIAL = "paid_social"
CHANNEL_EMAIL = "email"
CHANNEL_CAMPAIGN = "campaign"  # generic UTM campaign / coupon-driven
CHANNEL_ORGANIC_SOCIAL = "organic_social"
CHANNEL_ORGANIC_SEARCH = "organic_search"
CHANNEL_REFERRAL_EXTERNAL = "referral_external"  # inbound link from another site
CHANNEL_LOYALTY = "loyalty"
CHANNEL_DIRECT = "direct"
CHANNEL_UNKNOWN = "unknown"

CHANNEL_CHOICES = [
    (CHANNEL_AFFILIATE, _("Affiliate")),
    (CHANNEL_REFERRAL, _("Refer a Friend")),
    (CHANNEL_PAID_SEARCH, _("Paid Search")),
    (CHANNEL_PAID_SOCIAL, _("Paid Social")),
    (CHANNEL_EMAIL, _("Email")),
    (CHANNEL_CAMPAIGN, _("Campaign")),
    (CHANNEL_ORGANIC_SOCIAL, _("Organic Social")),
    (CHANNEL_ORGANIC_SEARCH, _("Organic Search")),
    (CHANNEL_REFERRAL_EXTERNAL, _("External Link")),
    (CHANNEL_LOYALTY, _("Loyalty")),
    (CHANNEL_DIRECT, _("Direct")),
    (CHANNEL_UNKNOWN, _("Unknown")),
]

# Collision hierarchy — highest priority first. Used at capture time to pick a
# single channel label when an arrival carries multiple signals.
CHANNEL_PRIORITY = [
    CHANNEL_AFFILIATE,
    CHANNEL_REFERRAL,
    CHANNEL_PAID_SEARCH,
    CHANNEL_PAID_SOCIAL,
    CHANNEL_CAMPAIGN,
    CHANNEL_EMAIL,
    CHANNEL_ORGANIC_SOCIAL,
    CHANNEL_ORGANIC_SEARCH,
    CHANNEL_REFERRAL_EXTERNAL,
    CHANNEL_LOYALTY,
    CHANNEL_DIRECT,
    CHANNEL_UNKNOWN,
]

# Consent snapshot recorded on every touch (GDPR proof-of-basis).
CONSENT_GRANTED = "granted"
CONSENT_DENIED = "denied"
CONSENT_UNKNOWN = "unknown"
CONSENT_CHOICES = [
    (CONSENT_GRANTED, _("Granted")),
    (CONSENT_DENIED, _("Denied")),
    (CONSENT_UNKNOWN, _("Unknown")),
]

# Attribution models — pure functions over the retained touch stream. Adding a
# model here + a resolver implementation is all it takes; no data migration,
# because touches are never discarded.
MODEL_LAST_NON_DIRECT = "last_non_direct"
MODEL_FIRST_TOUCH = "first_touch"
MODEL_LINEAR = "linear"
MODEL_TIME_DECAY = "time_decay"
MODEL_POSITION_BASED = "position_based"

ATTRIBUTION_MODEL_CHOICES = [
    (MODEL_LAST_NON_DIRECT, _("Last Non-Direct Click")),
    (MODEL_FIRST_TOUCH, _("First Touch")),
    (MODEL_LINEAR, _("Linear")),
    (MODEL_TIME_DECAY, _("Time Decay")),
    (MODEL_POSITION_BASED, _("Position Based (40/20/40)")),
]

# Role of an attribution row within an order's journey.
ROLE_PRIMARY = "primary"  # weights across primary rows sum to 1.0 per order
ROLE_ASSIST = "assist"  # top-of-funnel lens; may exceed 100% by design
ROLE_CHOICES = [
    (ROLE_PRIMARY, _("Primary")),
    (ROLE_ASSIST, _("Assist")),
]
