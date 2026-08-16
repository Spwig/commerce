"""
The merchant's own signing keys.

Two keypairs, two policies, and the split is deliberate — never share a key
across purposes:

- **transport** — Ed25519 (OKP / EdDSA). Signs the store's own outbound
  requests (agent callbacks, ACP push later) and interoperates with Web Bot
  Auth, whose profile schema RECOMMENDS OKP.
- **ap2_mandate** — ECDSA P-256 (EC / ES256). Signs AP2 checkout mandates.
  AP2 v0.2 EXPLICITLY DISALLOWS Ed25519 for the checkout JWT (a deterministic
  signature is rainbow-table-vulnerable there), so this must be ECDSA.

The `kid` is the RFC 7638 JWK SHA-256 Thumbprint for both — that is exactly
what lets a `UCP-Agent` lookup and a `Signature-Agent` (Web Bot Auth) lookup
resolve the same key for a dual-audience signature.

Private keys are stored Fernet-encrypted with a key derived from Django's
SECRET_KEY, matching payment_providers/utils/encryption.py. Caveat, same as
payment credentials: rotating SECRET_KEY orphans the private keys — rotate keys
(agentic_rotate_keys, later) rather than the platform secret.
"""

from __future__ import annotations

import base64
import hashlib
import json

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec, ed25519
from django.conf import settings
from django.utils import timezone


def _fernet() -> Fernet:
    key = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(key))


def _b64url(raw: bytes) -> str:
    """Unpadded base64url, as JWK/JWS require."""
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _thumbprint(required_members: dict) -> str:
    """
    RFC 7638 JWK thumbprint: SHA-256 over the canonical JSON of ONLY the
    required members (lexicographically ordered, no whitespace), base64url.
    """
    canonical = json.dumps(required_members, sort_keys=True, separators=(",", ":"))
    return _b64url(hashlib.sha256(canonical.encode("ascii")).digest())


# RFC 7638 §3.2: the required JWK members per key type, in the order the spec
# lists them (the thumbprint hashes them lexicographically regardless, but this
# documents which members are canonical for each type).
_RFC7638_REQUIRED = {
    "EC": ("crv", "kty", "x", "y"),
    "OKP": ("crv", "kty", "x"),
    "RSA": ("e", "kty", "n"),
    "oct": ("k", "kty"),
}


def required_jwk_members(jwk: dict) -> dict:
    """
    The RFC 7638 required-member subset of ``jwk`` for its key type.

    Used to recompute a key's thumbprint from a directory-served JWK so we can
    confirm it matches the claimed ``keyid`` rather than trusting the served
    ``kid``. Raises KeyError/ValueError on a JWK missing a required member.
    """
    kty = jwk.get("kty")
    members = _RFC7638_REQUIRED.get(kty)
    if members is None:
        raise ValueError(f"unsupported kty for thumbprint: {kty!r}")
    return {m: jwk[m] for m in members}


def _encrypt(pem: bytes) -> bytes:
    return _fernet().encrypt(pem)


def _decrypt(token: bytes) -> bytes:
    return _fernet().decrypt(bytes(token))


def _pkcs8_pem(private_key) -> bytes:
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )


def generate_transport_key(*, status=None):
    """
    Create and persist an Ed25519 transport key. Returns the AgentKey.

    Defaults to an ACTIVE key; pass ``status=AgentKey.STATUS_ROTATING`` to
    pre-publish one ahead of a rotation (published in the JWKS, not yet signing).
    A rotating key carries no ``activated_at`` until it is promoted.
    """
    from agentic.models import AgentKey

    status = status or AgentKey.STATUS_ACTIVE
    priv = ed25519.Ed25519PrivateKey.generate()
    x = priv.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    required = {"crv": "Ed25519", "kty": "OKP", "x": _b64url(x)}
    kid = _thumbprint(required)
    public_jwk = {**required, "kid": kid, "alg": "EdDSA", "use": "sig"}

    return AgentKey.objects.create(
        purpose=AgentKey.PURPOSE_TRANSPORT,
        kty="OKP",
        alg="EdDSA",
        crv="Ed25519",
        kid=kid,
        public_jwk=public_jwk,
        private_key_encrypted=_encrypt(_pkcs8_pem(priv)),
        status=status,
        activated_at=timezone.now() if status == AgentKey.STATUS_ACTIVE else None,
    )


def generate_ap2_key(*, status=None):
    """
    Create and persist an ECDSA P-256 mandate key. Returns the AgentKey.

    Defaults to an ACTIVE key; pass ``status=AgentKey.STATUS_ROTATING`` to
    pre-publish one ahead of a rotation. A rotating key carries no
    ``activated_at`` until it is promoted.
    """
    from agentic.models import AgentKey

    status = status or AgentKey.STATUS_ACTIVE
    priv = ec.generate_private_key(ec.SECP256R1())
    nums = priv.public_key().public_numbers()
    required = {
        "crv": "P-256",
        "kty": "EC",
        "x": _b64url(nums.x.to_bytes(32, "big")),
        "y": _b64url(nums.y.to_bytes(32, "big")),
    }
    kid = _thumbprint(required)
    public_jwk = {**required, "kid": kid, "alg": "ES256", "use": "sig"}

    return AgentKey.objects.create(
        purpose=AgentKey.PURPOSE_AP2,
        kty="EC",
        alg="ES256",
        crv="P-256",
        kid=kid,
        public_jwk=public_jwk,
        private_key_encrypted=_encrypt(_pkcs8_pem(priv)),
        status=status,
        activated_at=timezone.now() if status == AgentKey.STATUS_ACTIVE else None,
    )


def load_private_key(agent_key):
    """Decrypt and load the stored private key object for signing."""
    pem = _decrypt(agent_key.private_key_encrypted)
    return serialization.load_pem_private_key(pem, password=None)


def ensure_keys() -> dict:
    """
    Idempotently ensure one active transport key and one active AP2 key exist.

    Safe to call repeatedly (the management command and the enable signal both
    do). Returns a small summary of what was created.
    """
    from agentic.models import AgentKey

    created = {"transport": False, "ap2_mandate": False}
    if not AgentKey.objects.filter(
        purpose=AgentKey.PURPOSE_TRANSPORT, status=AgentKey.STATUS_ACTIVE
    ).exists():
        generate_transport_key()
        created["transport"] = True
    if not AgentKey.objects.filter(
        purpose=AgentKey.PURPOSE_AP2, status=AgentKey.STATUS_ACTIVE
    ).exists():
        generate_ap2_key()
        created["ap2_mandate"] = True
    return created


# Only these members ever leave the server. Building each published JWK from
# this allowlist means the unauthenticated /.well-known/ucp endpoint CANNOT
# leak a private component (d, and the RSA/symmetric private members) no matter
# what a future rotation or import path happened to store in public_jwk. This
# is the exposure point, so the invariant is enforced here, not merely trusted.
PUBLIC_JWK_MEMBERS = ("kty", "crv", "x", "y", "kid", "alg", "use")


def public_jwk_view(jwk: dict) -> dict:
    """Strip a stored JWK down to publishable public members only."""
    return {k: jwk[k] for k in PUBLIC_JWK_MEMBERS if k in jwk}


def _is_published(key, now) -> bool:
    """Whether a key still belongs in the public JWKS."""
    from agentic.models import AgentKey

    if key.status in (AgentKey.STATUS_ACTIVE, AgentKey.STATUS_ROTATING):
        return True
    if key.status == AgentKey.STATUS_RETIRED:
        # Retired keys stay published until their window closes, so signatures
        # made just before rotation still verify.
        return key.retire_after is None or key.retire_after > now
    return False


def get_jwks() -> dict:
    """
    The public JWK Set for the discovery profile: every key that is active,
    rotating, or retired-but-not-yet-expired. A rotating key is published
    before it is signed with, so verifiers learn it ahead of time.

    Each entry is reconstructed from the public-members allowlist, so no
    private material can escape even if a key row's public_jwk were poisoned.
    """
    from agentic.models import AgentKey

    now = timezone.now()
    keys = [
        public_jwk_view(k.public_jwk)
        for k in AgentKey.objects.all().order_by("purpose", "created_at")
        if _is_published(k, now)
    ]
    return {"keys": keys}
