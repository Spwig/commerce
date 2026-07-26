"""
Signing keys: generation, the two-key policy, storage round-trip, JWKS, and the
AP2 capability + enable-signal wiring.

The security-critical invariants under test:
  - transport keys are Ed25519/OKP, AP2 keys are ECDSA/EC — enforced by a DB
    constraint, not convention (AP2 forbids Ed25519 for the checkout JWT);
  - the kid is the RFC 7638 thumbprint of the public JWK;
  - a stored private key decrypts and actually signs (so it is usable, and the
    Fernet round-trip works);
  - only public material is ever exposed in the JWKS.
"""

import base64
import hashlib
import json

import pytest
from cryptography.hazmat.primitives.asymmetric import ec, ed25519
from django.db import IntegrityError, transaction
from django.utils import timezone

from agentic.identity import keys as keymod
from agentic.models import AgenticSettings, AgentKey

pytestmark = [pytest.mark.django_db, pytest.mark.integration]


def _thumbprint(required: dict) -> str:
    canonical = json.dumps(required, sort_keys=True, separators=(",", ":"))
    return (
        base64.urlsafe_b64encode(hashlib.sha256(canonical.encode()).digest()).rstrip(b"=").decode()
    )


class TestTransportKey:
    def test_is_ed25519_okp(self):
        k = keymod.generate_transport_key()
        assert k.purpose == AgentKey.PURPOSE_TRANSPORT
        assert (k.kty, k.alg, k.crv) == ("OKP", "EdDSA", "Ed25519")
        assert k.status == AgentKey.STATUS_ACTIVE
        assert k.public_jwk["kty"] == "OKP"
        assert "d" not in k.public_jwk  # never leak the private scalar

    def test_kid_is_rfc7638_thumbprint(self):
        k = keymod.generate_transport_key()
        expected = _thumbprint({"crv": "Ed25519", "kty": "OKP", "x": k.public_jwk["x"]})
        assert k.kid == expected
        assert k.public_jwk["kid"] == k.kid

    def test_private_key_round_trips_and_signs(self):
        k = keymod.generate_transport_key()
        priv = keymod.load_private_key(k)
        assert isinstance(priv, ed25519.Ed25519PrivateKey)
        sig = priv.sign(b"hello agent")
        # The public JWK must verify what the stored private key signed.
        x = base64.urlsafe_b64decode(k.public_jwk["x"] + "==")
        pub = ed25519.Ed25519PublicKey.from_public_bytes(x)
        pub.verify(sig, b"hello agent")  # raises on mismatch


class TestAp2Key:
    def test_is_ecdsa_p256(self):
        k = keymod.generate_ap2_key()
        assert k.purpose == AgentKey.PURPOSE_AP2
        assert (k.kty, k.alg, k.crv) == ("EC", "ES256", "P-256")
        assert set(k.public_jwk) >= {"crv", "kty", "x", "y", "kid"}
        assert "d" not in k.public_jwk

    def test_private_key_round_trips(self):
        k = keymod.generate_ap2_key()
        priv = keymod.load_private_key(k)
        assert isinstance(priv, ec.EllipticCurvePrivateKey)


class TestTwoKeyPolicyConstraint:
    def test_ap2_purpose_cannot_be_okp(self):
        with pytest.raises(IntegrityError):
            with transaction.atomic():
                AgentKey.objects.create(
                    purpose=AgentKey.PURPOSE_AP2,
                    kty="OKP",  # forbidden: AP2 must be EC
                    alg="EdDSA",
                    crv="Ed25519",
                    kid="x" * 20,
                    public_jwk={},
                    private_key_encrypted=b"x",
                )

    def test_transport_purpose_cannot_be_ec(self):
        with pytest.raises(IntegrityError):
            with transaction.atomic():
                AgentKey.objects.create(
                    purpose=AgentKey.PURPOSE_TRANSPORT,
                    kty="EC",  # forbidden: transport must be OKP
                    alg="ES256",
                    crv="P-256",
                    kid="y" * 20,
                    public_jwk={},
                    private_key_encrypted=b"y",
                )

    def test_full_tuple_is_pinned_not_just_kty(self):
        # Correct kty for AP2 (EC), but a mismatched alg/crv must still be
        # rejected — the constraint pins the whole crypto tuple.
        with pytest.raises(IntegrityError):
            with transaction.atomic():
                AgentKey.objects.create(
                    purpose=AgentKey.PURPOSE_AP2,
                    kty="EC",
                    alg="EdDSA",  # wrong: AP2 EC key must be ES256
                    crv="Ed25519",  # wrong: must be P-256
                    kid="z" * 20,
                    public_jwk={},
                    private_key_encrypted=b"z",
                )


class TestEnsureKeys:
    def test_creates_both_and_is_idempotent(self):
        first = keymod.ensure_keys()
        assert first == {"transport": True, "ap2_mandate": True}
        assert AgentKey.objects.count() == 2

        second = keymod.ensure_keys()
        assert second == {"transport": False, "ap2_mandate": False}
        assert AgentKey.objects.count() == 2  # no duplicates


class TestNoPrivateLeakage:
    def test_get_jwks_strips_private_members_even_if_stored(self):
        # Poison the stored JWK behind the save() guard (QuerySet.update skips
        # clean), then confirm the published JWKS still cannot expose `d`.
        k = keymod.generate_ap2_key()
        poisoned = dict(k.public_jwk)
        poisoned["d"] = "PRIVATE-SCALAR-MUST-NOT-ESCAPE"
        AgentKey.objects.filter(pk=k.pk).update(public_jwk=poisoned)

        jwks = keymod.get_jwks()
        assert all("d" not in entry for entry in jwks["keys"])
        # The public members are still there.
        published = jwks["keys"][0]
        assert published["kty"] == "EC"
        assert "PRIVATE-SCALAR-MUST-NOT-ESCAPE" not in json.dumps(jwks)

    def test_save_rejects_a_private_member_in_public_jwk(self):
        from django.core.exceptions import ValidationError

        k = keymod.generate_transport_key()
        k.public_jwk = {**k.public_jwk, "d": "leak"}
        with pytest.raises(ValidationError):
            k.save()

    def test_save_rejects_public_jwk_kty_mismatch(self):
        from django.core.exceptions import ValidationError

        k = keymod.generate_ap2_key()  # kty column = EC
        k.public_jwk = {**k.public_jwk, "kty": "OKP"}  # disagrees with the row
        with pytest.raises(ValidationError):
            k.save()


class TestJwks:
    def test_includes_active_excludes_expired_retired(self):
        keymod.ensure_keys()  # two active keys
        # A retired key still within its window stays published...
        rotating = keymod.generate_transport_key()
        rotating.status = AgentKey.STATUS_ROTATING
        rotating.save()
        retired_live = keymod.generate_transport_key()
        retired_live.status = AgentKey.STATUS_RETIRED
        retired_live.retire_after = timezone.now() + timezone.timedelta(days=1)
        retired_live.save()
        retired_expired = keymod.generate_transport_key()
        retired_expired.status = AgentKey.STATUS_RETIRED
        retired_expired.retire_after = timezone.now() - timezone.timedelta(days=1)
        retired_expired.save()

        jwks = keymod.get_jwks()
        kids = {k["kid"] for k in jwks["keys"]}

        assert rotating.kid in kids  # rotating is published ahead of signing
        assert retired_live.kid in kids  # within its window
        assert retired_expired.kid not in kids  # past retire_after
        # Only public material.
        assert all("d" not in k for k in jwks["keys"])


class TestCapabilityAndSignalWiring:
    def test_ap2_capability_flips_on_with_a_key(self):
        from agentic.services.capability_service import compute_capabilities

        assert "dev.ucp.shopping.ap2_mandate" not in compute_capabilities()
        keymod.generate_ap2_key()
        assert "dev.ucp.shopping.ap2_mandate" in compute_capabilities()

    def test_enabling_agentic_generates_keys(self):
        assert AgentKey.objects.count() == 0
        s = AgenticSettings.get_settings()
        s.is_enabled = True
        s.save()  # post_save signal → ensure_keys()
        assert AgentKey.objects.filter(status=AgentKey.STATUS_ACTIVE).count() == 2
