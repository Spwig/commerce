"""
SD-JWT issuance for AP2 mandates.

AP2 v0.2 (FIDO Alliance) attests a checkout with an SD-JWT — a signed JWT whose
payload carries hash digests of individually salted "disclosures", so a holder
can reveal some claims and withhold others while the signature still verifies.
This module issues the merchant's Checkout Mandate: it signs with the merchant's
own ECDSA (AP2) key.

Hard crypto policy, enforced here and by the AgentKey DB constraint:

- **ECDSA only — Ed25519 is REJECTED.** AP2 v0.2 forbids Ed25519 for the
  checkout JWT (its deterministic signatures are the wrong choice there), so an
  Ed25519/OKP key is refused with an error rather than quietly downgraded.
- Algorithms: ``ES256`` / ``ES384`` / ``ES512`` (P-256 / P-384 / P-521). The
  signature is JWS raw ``r || s`` (each coordinate left-padded to the curve
  size), never DER.

Disclosure digests and the ``[salt, name, value]`` disclosure arrays are
serialized with RFC 8785 JCS (`agentic.domain.jcs`), so issuer and verifier
compute identical bytes.
"""

from __future__ import annotations

import base64
import hashlib
import secrets
import time

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import (
    decode_dss_signature,
    encode_dss_signature,
)

from agentic.domain import jcs

# alg -> (hash factory, curve name). ES256/384/512 only; no EdDSA.
_ES_ALGS = {
    "ES256": (hashes.SHA256, "secp256r1"),
    "ES384": (hashes.SHA384, "secp384r1"),
    "ES512": (hashes.SHA512, "secp521r1"),
}


class MandateSigningError(Exception):
    """The mandate could not be signed (wrong key type, bad alg)."""


def b64url_encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def b64url_decode(s: str) -> bytes:
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


def _coord_bytes(value: int, size: int) -> bytes:
    return value.to_bytes(size, "big")


def _alg_for_key(private_key) -> str:
    if not isinstance(private_key, ec.EllipticCurvePrivateKey):
        # Ed25519 (or anything non-EC) is refused: AP2 forbids it for this JWT.
        raise MandateSigningError("AP2 mandates require an ECDSA key; Ed25519 is not allowed")
    curve = private_key.curve.name
    for alg, (_h, curve_name) in _ES_ALGS.items():
        if curve_name == curve:
            return alg
    raise MandateSigningError(f"unsupported EC curve for AP2: {curve}")


def _sign(signing_input: bytes, private_key, alg: str) -> bytes:
    hash_factory, _curve = _ES_ALGS[alg]
    der = private_key.sign(signing_input, ec.ECDSA(hash_factory()))
    r, s = decode_dss_signature(der)
    size = (private_key.curve.key_size + 7) // 8
    return _coord_bytes(r, size) + _coord_bytes(s, size)


def _make_disclosure(name: str, value) -> tuple[str, str]:
    """Return (disclosure, digest) for a selectively-disclosable claim."""
    salt = b64url_encode(secrets.token_bytes(16))
    disclosure = b64url_encode(jcs.canonicalize([salt, name, value]))
    digest = b64url_encode(hashlib.sha256(disclosure.encode("ascii")).digest())
    return disclosure, digest


def issue_sd_jwt(
    *,
    always_claims: dict,
    sd_claims: dict | None,
    private_key,
    kid: str,
    iss: str,
    iat: int,
    exp: int,
    vct: str,
) -> str:
    """
    Build and sign an SD-JWT.

    ``always_claims`` are disclosed in the clear; ``sd_claims`` are turned into
    salted disclosures whose digests go in ``_sd``. Returns the SD-JWT
    presentation string ``<jwt>~<disclosure>~...~``.
    """
    alg = _alg_for_key(private_key)

    disclosures: list[str] = []
    digests: list[str] = []
    for name, value in (sd_claims or {}).items():
        disclosure, digest = _make_disclosure(name, value)
        disclosures.append(disclosure)
        digests.append(digest)
    digests.sort()  # order must not leak the claim order

    payload = {
        **always_claims,
        "iss": iss,
        "iat": iat,
        "exp": exp,
        "vct": vct,
    }
    if digests:
        payload["_sd"] = digests
        payload["_sd_alg"] = "sha-256"

    header = {"typ": "dc+sd-jwt", "alg": alg, "kid": kid}
    signing_input = (
        b64url_encode(jcs.canonicalize(header)).encode("ascii")
        + b"."
        + b64url_encode(jcs.canonicalize(payload)).encode("ascii")
    )
    signature = _sign(signing_input, private_key, alg)
    jwt = signing_input.decode("ascii") + "." + b64url_encode(signature)

    # Trailing '~' marks a presentation with no key binding.
    return "~".join([jwt, *disclosures]) + "~"


# --------------------------------------------------------------------------- #
# Verification (for self-check, tests, and the independent oracle).
# --------------------------------------------------------------------------- #


def _load_ec_public_key(jwk: dict):
    if jwk.get("kty") != "EC":
        raise MandateSigningError("AP2 verification requires an EC JWK")
    curves = {"P-256": ec.SECP256R1(), "P-384": ec.SECP384R1(), "P-521": ec.SECP521R1()}
    crv = curves.get(jwk.get("crv"))
    if crv is None:
        raise MandateSigningError(f"unsupported EC curve: {jwk.get('crv')}")
    x = int.from_bytes(b64url_decode(jwk["x"]), "big")
    y = int.from_bytes(b64url_decode(jwk["y"]), "big")
    return ec.EllipticCurvePublicNumbers(x, y, crv).public_key()


# AP2/JWA binds each ES alg to exactly one curve; a verifier must reject any
# other pairing (an ES384 header over a P-256 key, etc.).
_ALG_TO_CRV = {"ES256": "P-256", "ES384": "P-384", "ES512": "P-521"}


def verify_sd_jwt(
    sd_jwt: str, *, public_jwk: dict, now: int | None = None, leeway: int = 0
) -> tuple[dict, dict]:
    """
    Verify an SD-JWT signature, expiry, and rebuild its full claim set.

    Returns (payload, disclosed_claims). Raises MandateSigningError on any
    signature, expiry, algorithm, digest, or structural failure. In particular:

    - ``alg`` must be an ES family member AND match the key's curve (ES256↔P-256,
      ES384↔P-384, ES512↔P-521) — no mixed pairings.
    - ``exp`` is enforced (a payment network treats verification success as
      validity, so an expired mandate must not verify here).
    - each disclosure's digest MUST appear in ``_sd``, and ``_sd_alg`` (when
      disclosures are present) MUST be ``sha-256`` — the only digest algorithm
      this verifier computes.
    """
    parts = sd_jwt.split("~")
    jwt = parts[0]
    disclosures = [p for p in parts[1:] if p]  # drop the trailing empty segment

    try:
        header_b64, payload_b64, sig_b64 = jwt.split(".")
    except ValueError as exc:
        raise MandateSigningError("malformed JWT") from exc

    header = jcs_loads(b64url_decode(header_b64))
    alg = header.get("alg")
    if alg not in _ES_ALGS:
        raise MandateSigningError(f"unsupported or forbidden alg: {alg}")
    if _ALG_TO_CRV[alg] != public_jwk.get("crv"):
        raise MandateSigningError("alg does not match the key's curve")

    public_key = _load_ec_public_key(public_jwk)
    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
    signature = b64url_decode(sig_b64)
    size = (public_key.curve.key_size + 7) // 8
    if len(signature) != 2 * size:
        raise MandateSigningError("bad signature length")
    r = int.from_bytes(signature[:size], "big")
    s = int.from_bytes(signature[size:], "big")
    hash_factory, _curve = _ES_ALGS[alg]
    try:
        public_key.verify(encode_dss_signature(r, s), signing_input, ec.ECDSA(hash_factory()))
    except Exception as exc:
        raise MandateSigningError("signature verification failed") from exc

    payload = jcs_loads(b64url_decode(payload_b64))

    # Expiry — signature-valid is not the same as still-valid.
    now = int(time.time()) if now is None else now
    exp = payload.get("exp")
    if exp is None or now > int(exp) + leeway:
        raise MandateSigningError("mandate expired" if exp is not None else "mandate has no exp")

    committed = set(payload.get("_sd", []))
    if disclosures and payload.get("_sd_alg") != "sha-256":
        # We only compute SHA-256 digests; any other (or missing) _sd_alg means
        # our digest check does not match what the signature committed to.
        raise MandateSigningError("unsupported _sd_alg")
    disclosed: dict = {}
    for disclosure in disclosures:
        digest = b64url_encode(hashlib.sha256(disclosure.encode("ascii")).digest())
        if digest not in committed:
            raise MandateSigningError("disclosure not committed by the signature")
        salt, name, value = jcs_loads(b64url_decode(disclosure))
        disclosed[name] = value
    return payload, disclosed


def jcs_loads(raw: bytes):
    import json

    return json.loads(raw.decode("utf-8"))
