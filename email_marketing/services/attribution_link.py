"""Bridge Campaign Studio campaigns to the multi-touch attribution engine.

A Studio campaign gets a stable ``attribution_slug`` (its ``utm_campaign`` value),
and a matching ``attribution.Campaign`` row must exist *before* a recipient clicks —
inbound capture resolves ``utm_campaign`` to a Campaign by slug and never auto-creates
one (attribution/services/capture.py). So at send time we pre-create the row here.

Dependency direction: email_marketing → attribution (a peer app). ``email_system``
never imports this; it only reads the slug stamped on the outbox column.
"""

import logging

logger = logging.getLogger("email_marketing")


def ensure_attribution_campaign(campaign):
    """Ensure an ``attribution.Campaign`` exists for this Studio campaign's slug.

    Mints the campaign's stable ``attribution_slug`` if needed, then idempotently
    creates (or fetches) the attribution.Campaign keyed on that slug. Returns the
    slug (the value to stamp on the outbox as ``utm_campaign``), or ``None`` on any
    failure so a hiccup in the attribution layer can never break a send.
    """
    try:
        slug = campaign.ensure_attribution_slug()
        from attribution.constants import CHANNEL_EMAIL
        from attribution.models import Campaign as AttributionCampaign

        AttributionCampaign.objects.get_or_create(
            slug=slug,
            defaults={
                "name": campaign.name[:255],
                "channel_hint": CHANNEL_EMAIL,
                "is_active": True,
            },
        )
        return slug
    except Exception:  # noqa: BLE001 — attribution must never break sending
        logger.warning("Could not link campaign %s to attribution", getattr(campaign, "id", "?"))
        return None
