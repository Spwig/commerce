"""
Operational lifecycle for the merchant's OWN agentic signing keys.

`agentic.identity.keys` *generates* keys; this module *transitions* them through
rotation and retirement. The two behaviours the store advertises via the key
STATUS_ROTATING / STATUS_RETIRED states live here, so those states name real
operations rather than dormant enum values:

- **rotate** — bring a fresh key into service and move the outgoing one to a
  time-bounded RETIRED window. A pre-published ROTATING key (see
  `prepublish_signing_key`) is promoted in place; otherwise a new key is minted.
- **retire** — take a specific key out of signing service, keeping it published
  in the JWKS until its overlap window closes so in-flight signatures still
  verify.

Nothing here deletes a key row: a transport signature or an AP2 mandate made
just before a switch must remain verifiable against the published JWKS while its
window is open. The window is enforced by `keys._is_published`.

The operator surface is the `agentic_rotate_keys` management command (the
`AgentKey` model is deliberately never exposed in the admin — it holds encrypted
private material).
"""

from __future__ import annotations

from django.db import transaction
from django.utils import timezone

from agentic.identity import keys as keymod

# A rotated-out key stays published this long by default, so signatures made in
# the moments before the switch still verify. Operators can widen or (with 0)
# eliminate the overlap per call.
DEFAULT_OVERLAP_DAYS = 7


def _generate_active(purpose: str):
    from agentic.models import AgentKey

    if purpose == AgentKey.PURPOSE_TRANSPORT:
        return keymod.generate_transport_key()
    if purpose == AgentKey.PURPOSE_AP2:
        return keymod.generate_ap2_key()
    raise ValueError(f"unknown key purpose: {purpose!r}")


def _generate_rotating(purpose: str):
    from agentic.models import AgentKey

    if purpose == AgentKey.PURPOSE_TRANSPORT:
        return keymod.generate_transport_key(status=AgentKey.STATUS_ROTATING)
    if purpose == AgentKey.PURPOSE_AP2:
        return keymod.generate_ap2_key(status=AgentKey.STATUS_ROTATING)
    raise ValueError(f"unknown key purpose: {purpose!r}")


def prepublish_signing_key(purpose: str):
    """
    Pre-publish a new signing key in the rotating state, ahead of a rotation.

    A rotating key is advertised in the JWKS but does not sign yet, so verifiers
    learn it before the store starts using it — the standard two-phase key
    rollover. Promote it later with `rotate_signing_key`. Returns the AgentKey.
    """
    return _generate_rotating(purpose)


def rotate_signing_key(purpose: str, *, overlap_days: int = DEFAULT_OVERLAP_DAYS) -> dict:
    """
    Rotate the store's active signing key for a purpose.

    Promotes a pre-published rotating key to active (or mints a fresh active key
    when none is staged), and moves every previously-active key of that purpose
    to a time-bounded RETIRED window so recent signatures keep verifying. The
    store is never left without an active key of the purpose. Returns a summary
    dict.
    """
    from agentic.models import AgentKey

    if overlap_days < 0:
        raise ValueError("overlap_days must be >= 0")

    with transaction.atomic():
        # Lock this purpose's live keys so two concurrent rotations can't both
        # promote/retire and leave the JWKS with two actives or none.
        live = list(
            AgentKey.objects.select_for_update()
            .filter(purpose=purpose)
            .exclude(status=AgentKey.STATUS_RETIRED)
            .order_by("created_at")
        )
        active = [k for k in live if k.status == AgentKey.STATUS_ACTIVE]
        rotating = [k for k in live if k.status == AgentKey.STATUS_ROTATING]

        now = timezone.now()
        if rotating:
            new_key = rotating[0]
            new_key.status = AgentKey.STATUS_ACTIVE
            new_key.activated_at = now
            new_key.save(update_fields=["status", "activated_at", "updated_at"])
            promoted = True
            # Any surplus staged keys are retired immediately so exactly one key
            # is active at the end.
            surplus = rotating[1:]
        else:
            new_key = _generate_active(purpose)
            promoted = False
            surplus = []

        retire_after = now + timezone.timedelta(days=overlap_days)
        retired_kids = []
        for k in [*active, *surplus]:
            k.status = AgentKey.STATUS_RETIRED
            # Surplus staged keys never signed, so they drop from the JWKS now.
            k.retire_after = retire_after if k in active else now
            k.save(update_fields=["status", "retire_after", "updated_at"])
            retired_kids.append(k.kid)

        return {
            "purpose": purpose,
            "new_kid": new_key.kid,
            "promoted": promoted,
            "retired_kids": retired_kids,
            "overlap_days": overlap_days,
        }


def retire_signing_key(kid: str, *, overlap_days: int = 0):
    """
    Retire a specific signing key, keeping it published until its window closes.

    Moves the key to RETIRED with a `retire_after` of now + overlap (0 = drops
    from the JWKS at once). Idempotent on an already-retired key (its window is
    reset to the new value). Raises ValueError for an unknown kid. Returns the
    AgentKey.
    """
    from agentic.models import AgentKey

    if overlap_days < 0:
        raise ValueError("overlap_days must be >= 0")

    with transaction.atomic():
        try:
            key = AgentKey.objects.select_for_update().get(kid=kid)
        except AgentKey.DoesNotExist as exc:
            raise ValueError(f"no signing key with kid {kid!r}") from exc

        key.status = AgentKey.STATUS_RETIRED
        key.retire_after = timezone.now() + timezone.timedelta(days=overlap_days)
        key.save(update_fields=["status", "retire_after", "updated_at"])
        return key
