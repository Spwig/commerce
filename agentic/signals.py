"""Agentic signal receivers."""

from __future__ import annotations

import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from agentic.models import AgenticSettings

logger = logging.getLogger(__name__)


@receiver(post_save, sender=AgenticSettings)
def generate_keys_on_enable(sender, instance, **kwargs):
    """
    When agentic commerce is turned on, make sure signing keys exist.

    Keys underpin the discovery JWKS and the AP2 mandate capability, so a
    merchant flipping the switch should never be left with an empty key set.
    Generation is idempotent and cheap; a failure here must not break saving
    the settings row, so it is logged rather than raised.
    """
    if not instance.is_enabled:
        return
    try:
        from agentic.identity.keys import ensure_keys

        ensure_keys()
    except Exception:
        logger.exception("Failed to ensure agentic signing keys on enable")
