"""
Signing-key lifecycle: rotation, two-phase pre-publish/promote, and retirement.

These make the STATUS_ROTATING / STATUS_RETIRED states name real operations. The
invariants under test:
  - the store is never left without an active key of a purpose (no signing gap);
  - a rotated-out key stays published in the JWKS for its overlap window, so a
    signature made just before the switch still verifies, then drops out;
  - a key row is transitioned, never deleted.
"""

import pytest
from django.core.management import call_command
from django.utils import timezone

from agentic.identity import keys as keymod
from agentic.models import AgentKey
from agentic.services import key_service

pytestmark = [pytest.mark.django_db, pytest.mark.integration]

TRANSPORT = AgentKey.PURPOSE_TRANSPORT
AP2 = AgentKey.PURPOSE_AP2


def _jwks_kids() -> set[str]:
    return {k["kid"] for k in keymod.get_jwks()["keys"]}


class TestRotate:
    def test_rotate_mints_new_active_and_retires_old(self):
        old = keymod.generate_transport_key()
        result = key_service.rotate_signing_key(TRANSPORT, overlap_days=7)

        old.refresh_from_db()
        assert old.status == AgentKey.STATUS_RETIRED
        assert old.retire_after is not None and old.retire_after > timezone.now()
        assert result["promoted"] is False
        assert old.kid in result["retired_kids"]
        assert result["new_kid"] != old.kid
        # Exactly one active transport key remains, and it is the new one.
        actives = AgentKey.objects.filter(purpose=TRANSPORT, status=AgentKey.STATUS_ACTIVE)
        assert actives.count() == 1
        assert actives.first().kid == result["new_kid"]

    def test_retired_key_stays_published_within_window(self):
        old = keymod.generate_transport_key()
        key_service.rotate_signing_key(TRANSPORT, overlap_days=1)
        assert old.kid in _jwks_kids()  # still verifiable during overlap

    def test_zero_overlap_drops_old_from_jwks_at_once(self):
        old = keymod.generate_ap2_key()
        key_service.rotate_signing_key(AP2, overlap_days=0)
        assert old.kid not in _jwks_kids()

    def test_rotate_with_no_existing_active_just_mints(self):
        result = key_service.rotate_signing_key(AP2)
        assert result["retired_kids"] == []
        assert AgentKey.objects.filter(purpose=AP2, status=AgentKey.STATUS_ACTIVE).count() == 1

    def test_ap2_capability_never_gaps_across_rotation(self):
        from agentic.services.capability_service import _has_ap2_signing_key

        keymod.generate_ap2_key()
        assert _has_ap2_signing_key() is True
        key_service.rotate_signing_key(AP2, overlap_days=0)
        assert _has_ap2_signing_key() is True  # new active exists before old retires

    def test_rejects_negative_overlap(self):
        with pytest.raises(ValueError):
            key_service.rotate_signing_key(TRANSPORT, overlap_days=-1)

    def test_rejects_unknown_purpose(self):
        with pytest.raises(ValueError):
            key_service.rotate_signing_key("nonsense")


class TestPrepublishThenPromote:
    def test_prepublish_creates_rotating_not_active(self):
        active = keymod.generate_transport_key()
        staged = key_service.prepublish_signing_key(TRANSPORT)

        assert staged.status == AgentKey.STATUS_ROTATING
        assert staged.activated_at is None
        # Both published, but only one is active (staged does not sign yet).
        assert {active.kid, staged.kid} <= _jwks_kids()
        assert (
            AgentKey.objects.filter(purpose=TRANSPORT, status=AgentKey.STATUS_ACTIVE).count() == 1
        )

    def test_rotate_promotes_staged_key_in_place(self):
        active = keymod.generate_transport_key()
        staged = key_service.prepublish_signing_key(TRANSPORT)

        result = key_service.rotate_signing_key(TRANSPORT, overlap_days=3)

        staged.refresh_from_db()
        active.refresh_from_db()
        assert result["promoted"] is True
        assert result["new_kid"] == staged.kid
        assert staged.status == AgentKey.STATUS_ACTIVE
        assert staged.activated_at is not None
        assert active.status == AgentKey.STATUS_RETIRED


class TestRetire:
    def test_retire_specific_key_with_window(self):
        k = keymod.generate_transport_key()
        key_service.retire_signing_key(k.kid, overlap_days=2)
        k.refresh_from_db()
        assert k.status == AgentKey.STATUS_RETIRED
        assert k.retire_after > timezone.now()
        assert k.kid in _jwks_kids()  # published during the window

    def test_retire_zero_overlap_unpublishes(self):
        k = keymod.generate_ap2_key()
        key_service.retire_signing_key(k.kid)  # overlap defaults to 0
        assert k.kid not in _jwks_kids()

    def test_retire_unknown_kid_raises(self):
        with pytest.raises(ValueError):
            key_service.retire_signing_key("does-not-exist")

    def test_retire_is_idempotent(self):
        k = keymod.generate_transport_key()
        key_service.retire_signing_key(k.kid, overlap_days=1)
        key_service.retire_signing_key(k.kid, overlap_days=5)  # no error
        k.refresh_from_db()
        assert k.status == AgentKey.STATUS_RETIRED


class TestRotateKeysCommand:
    def test_command_rotates_all_purposes(self):
        keymod.ensure_keys()
        call_command("agentic_rotate_keys", "--overlap-days", "0")
        for purpose in (TRANSPORT, AP2):
            assert (
                AgentKey.objects.filter(purpose=purpose, status=AgentKey.STATUS_ACTIVE).count() == 1
            )

    def test_command_prepublish_stages_a_rotating_key(self):
        keymod.ensure_keys()
        call_command("agentic_rotate_keys", "--purpose", "transport", "--prepublish")
        assert (
            AgentKey.objects.filter(purpose=TRANSPORT, status=AgentKey.STATUS_ROTATING).count() == 1
        )

    def test_command_retire_specific_key_with_force(self):
        # Retiring the only active key of a purpose is guarded — force it.
        k = keymod.generate_ap2_key()
        call_command("agentic_rotate_keys", "--retire", k.kid, "--overlap-days", "0", "--force")
        k.refresh_from_db()
        assert k.status == AgentKey.STATUS_RETIRED

    def test_command_retire_last_active_refused_without_force(self):
        from django.core.management.base import CommandError

        k = keymod.generate_ap2_key()
        with pytest.raises(CommandError):
            call_command("agentic_rotate_keys", "--retire", k.kid)
        k.refresh_from_db()
        assert k.status == AgentKey.STATUS_ACTIVE  # untouched

    def test_command_retire_non_last_key_allowed(self):
        # A second active key exists, so retiring one is fine without --force.
        keymod.generate_ap2_key()
        victim = keymod.generate_ap2_key()
        call_command("agentic_rotate_keys", "--retire", victim.kid, "--overlap-days", "0")
        victim.refresh_from_db()
        assert victim.status == AgentKey.STATUS_RETIRED
