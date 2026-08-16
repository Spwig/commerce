"""Attribution signal wiring.

Two concerns live here:

- The login identity-stitch (binds a visitor's anonymous touch stream to their
  account when they log in), and
- Registration of the unified order-completion orchestrator, which subsumes the
  affiliate, referral and reporting order handlers into one entry point (see
  ``attribution.orchestrator``).

The visitor key survives Django's login session-key rotation because it lives
in its own ``attr_vid`` cookie and is stashed in session data — the same
approach the cart uses for ``guest_cart_id`` (see ``cart/signals.py``).
"""

import logging

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

# Importing the orchestrator registers the unified Order pre_save/post_save
# receivers. Keep this import — without it the collapse would silently no-op.
from attribution import orchestrator  # noqa: F401
from attribution.services.identity import stitch_from_request

logger = logging.getLogger(__name__)


@receiver(user_logged_in)
def bind_touch_stream_on_login(sender, request, user, **kwargs):
    try:
        stitch_from_request(request, user)
    except Exception:  # pragma: no cover - never break login
        logger.exception("attribution: failed to stitch touch stream at login")
