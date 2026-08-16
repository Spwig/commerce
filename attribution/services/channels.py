"""Resolve a raw arrival signal into a single channel label.

This is the collision hierarchy from ``constants.CHANNEL_PRIORITY`` made
concrete. It answers only *what to call this touch*; it says nothing about how
revenue is split across a journey (that is the attribution model's job). Kept
as a pure function of extracted signal so it is trivially testable and reused
by both live capture and any backfill.
"""

from attribution.constants import (
    CHANNEL_CAMPAIGN,
    CHANNEL_DIRECT,
    CHANNEL_EMAIL,
    CHANNEL_ORGANIC_SEARCH,
    CHANNEL_ORGANIC_SOCIAL,
    CHANNEL_PAID_SEARCH,
    CHANNEL_PAID_SOCIAL,
    CHANNEL_REFERRAL_EXTERNAL,
)

# Referrer hosts (substring match) that identify a search engine.
_SEARCH_HOSTS = (
    "google.",
    "bing.",
    "yahoo.",
    "duckduckgo.",
    "baidu.",
    "yandex.",
    "ecosia.",
    "brave.",
    "startpage.",
    "qwant.",
)

# Referrer hosts (substring match) that identify a social network.
_SOCIAL_HOSTS = (
    "facebook.",
    "fb.",
    "instagram.",
    "twitter.",
    "x.com",
    "t.co",
    "linkedin.",
    "lnkd.in",
    "pinterest.",
    "tiktok.",
    "youtube.",
    "youtu.be",
    "reddit.",
    "threads.",
    "snapchat.",
    "whatsapp.",
    "telegram.",
)

# utm_medium values that read as paid.
_PAID_MEDIUMS = {"cpc", "ppc", "paid", "paidsearch", "paid_search", "paid-search", "display"}
_PAID_SOCIAL_MEDIUMS = {"paid_social", "paid-social", "paidsocial", "social_paid"}
_SOCIAL_MEDIUMS = {"social", "social_organic", "social-media", "sm"}
_EMAIL_MEDIUMS = {"email", "e-mail", "newsletter", "mail"}


def _host_matches(host, needles):
    host = (host or "").lower()
    return any(n in host for n in needles)


def resolve_channel(
    *,
    utm_source="",
    utm_medium="",
    utm_campaign="",
    gclid="",
    fbclid="",
    msclkid="",
    referrer_host="",
    referrer_is_internal=False,
):
    """Return the highest-priority channel label for this signal.

    Returns ``CHANNEL_DIRECT`` when nothing distinguishes the arrival. Callers
    decide whether a ``direct`` result with no external referrer is worth
    recording (it usually is not — see ``capture.has_signal``).

    Note: ``affiliate`` and ``referral`` channels are assigned by their own
    subsystems at their capture points (they carry first-party markers, not
    UTM), so they are intentionally not derived here.
    """
    medium = (utm_medium or "").lower().strip()

    # Paid click identifiers are the strongest paid signal.
    if gclid:
        return CHANNEL_PAID_SEARCH
    if fbclid or msclkid:
        return CHANNEL_PAID_SOCIAL

    # Explicit paid mediums.
    if medium in _PAID_SOCIAL_MEDIUMS:
        return CHANNEL_PAID_SOCIAL
    if medium in _PAID_MEDIUMS:
        return CHANNEL_PAID_SEARCH

    # Email.
    if medium in _EMAIL_MEDIUMS:
        return CHANNEL_EMAIL

    # Organic social (tagged).
    if medium in _SOCIAL_MEDIUMS:
        return CHANNEL_ORGANIC_SOCIAL

    # A campaign tag with no more-specific medium.
    if utm_campaign or utm_source:
        return CHANNEL_CAMPAIGN

    # Fall back to referrer host classification (untagged inbound).
    if referrer_host and not referrer_is_internal:
        if _host_matches(referrer_host, _SEARCH_HOSTS):
            return CHANNEL_ORGANIC_SEARCH
        if _host_matches(referrer_host, _SOCIAL_HOSTS):
            return CHANNEL_ORGANIC_SOCIAL
        return CHANNEL_REFERRAL_EXTERNAL

    return CHANNEL_DIRECT
