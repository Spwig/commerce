"""
RFC 9421 verification engine.

The signing helper here is the mirror image of the verifier: it builds the same
signature base, so a passing round-trip proves base construction agrees end to
end. The negative tests are the point — each asserts that a specific tamper or
staleness turns into a safe refusal, never an accept.
"""

import base64

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec, ed25519
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature

from agentic.identity import rfc9421
from agentic.identity.rfc9421 import SignatureRequest, verify

pytestmark = pytest.mark.unit


def _b64url(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _ed25519_key():
    priv = ed25519.Ed25519PrivateKey.generate()
    x = priv.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    jwk = {"kty": "OKP", "crv": "Ed25519", "x": _b64url(x), "kid": "ed-kid"}
    return priv, jwk


def _ec_key():
    priv = ec.generate_private_key(ec.SECP256R1())
    nums = priv.public_key().public_numbers()
    jwk = {
        "kty": "EC",
        "crv": "P-256",
        "x": _b64url(nums.x.to_bytes(32, "big")),
        "y": _b64url(nums.y.to_bytes(32, "big")),
        "kid": "ec-kid",
    }
    return priv, jwk


def _sign(req, priv, jwk, *, covered=("@method", "@authority", "@path"), params=None):
    """Produce (Signature-Input, Signature) header values for `req`."""
    params = dict(params or {})
    params.setdefault("keyid", jwk["kid"])
    alg = rfc9421.ALG_ED25519 if jwk["kty"] == "OKP" else rfc9421.ALG_ES256
    params.setdefault("alg", alg)

    comp_str = " ".join(f'"{c}"' for c in covered)
    parts = [f"({comp_str})"]
    for k, v in params.items():
        parts.append(f';{k}="{v}"' if isinstance(v, str) else f";{k}={v}")
    raw_value = "".join(parts)

    member = rfc9421._SignatureInputMember("sig1", [(c, {}) for c in covered], {}, raw_value)
    base = rfc9421.build_signature_base(member, req)

    if jwk["kty"] == "OKP":
        sig = priv.sign(base)
    else:
        from cryptography.hazmat.primitives import hashes

        der = priv.sign(base, ec.ECDSA(hashes.SHA256()))
        r, s = decode_dss_signature(der)
        sig = r.to_bytes(32, "big") + s.to_bytes(32, "big")

    sig_b64 = base64.b64encode(sig).decode("ascii")
    return f"sig1={raw_value}", f"sig1=:{sig_b64}:"


def _request(headers=None, **kw):
    base = {
        "method": "POST",
        "scheme": "https",
        "authority": "shop.example.com",
        "path": "/api/agentic/mcp",
        "query": "",
    }
    base.update(kw)
    base["headers"] = headers or {}
    return SignatureRequest(**base)


def _signed_request(priv, jwk, *, covered=("@method", "@authority", "@path"), params=None, **kw):
    req = _request(**kw)
    si, s = _sign(req, priv, jwk, covered=covered, params=params)
    headers = {**req.headers, "signature-input": si, "signature": s}
    return SignatureRequest(
        method=req.method,
        scheme=req.scheme,
        authority=req.authority,
        path=req.path,
        query=req.query,
        headers=headers,
    )


class TestRoundTrip:
    def test_ed25519_ok(self):
        priv, jwk = _ed25519_key()
        req = _signed_request(priv, jwk, params={"created": 1_000_000})
        r = verify(req, public_jwk=jwk, now=1_000_010)
        assert r.ok is True
        assert r.keyid == "ed-kid"
        assert r.alg == rfc9421.ALG_ED25519
        assert r.covered == ("@method", "@authority", "@path")

    def test_ecdsa_p256_ok(self):
        priv, jwk = _ec_key()
        req = _signed_request(priv, jwk, params={"created": 1_000_000})
        r = verify(req, public_jwk=jwk, now=1_000_010)
        assert r.ok is True
        assert r.alg == rfc9421.ALG_ES256

    def test_covers_query_and_header(self):
        priv, jwk = _ed25519_key()
        req = _signed_request(
            priv,
            jwk,
            covered=("@method", "@authority", "@path", "@query", "content-digest"),
            params={"created": 1_000_000},
            query="q=oil&page=2",
            headers={"content-digest": "sha-256=:abc:"},
        )
        r = verify(
            req,
            public_jwk=jwk,
            now=1_000_010,
            required_components=("@method", "@authority", "@path", "content-digest"),
        )
        assert r.ok is True


class TestTamper:
    def test_tampered_path_fails(self):
        priv, jwk = _ed25519_key()
        req = _signed_request(priv, jwk, params={"created": 1_000_000})
        forged = SignatureRequest(
            method=req.method,
            scheme=req.scheme,
            authority=req.authority,
            path="/api/agentic/checkout",  # signed over /mcp
            query=req.query,
            headers=req.headers,
        )
        r = verify(forged, public_jwk=jwk, now=1_000_010)
        assert r.ok is False
        assert r.reason == "bad signature"

    def test_replay_against_different_method_fails(self):
        priv, jwk = _ed25519_key()
        req = _signed_request(priv, jwk, params={"created": 1_000_000})
        forged = SignatureRequest(
            method="DELETE",
            scheme=req.scheme,
            authority=req.authority,
            path=req.path,
            query=req.query,
            headers=req.headers,
        )
        assert verify(forged, public_jwk=jwk, now=1_000_010).ok is False

    def test_wrong_key_fails(self):
        priv, jwk = _ed25519_key()
        _, other_jwk = _ed25519_key()
        req = _signed_request(priv, jwk, params={"created": 1_000_000})
        assert verify(req, public_jwk=other_jwk, now=1_000_010).ok is False

    def test_flipped_signature_byte_fails(self):
        priv, jwk = _ed25519_key()
        req = _signed_request(priv, jwk, params={"created": 1_000_000})
        sig = req.headers["signature"]
        # Corrupt one base64 char in the byte sequence.
        corrupted = sig[:-3] + ("A" if sig[-3] != "A" else "B") + sig[-2:]
        headers = {**req.headers, "signature": corrupted}
        r = verify(
            req.__class__(**{**req.__dict__, "headers": headers}), public_jwk=jwk, now=1_000_010
        )
        assert r.ok is False


class TestFreshness:
    def test_stale_created_rejected(self):
        priv, jwk = _ed25519_key()
        req = _signed_request(priv, jwk, params={"created": 1_000_000})
        r = verify(req, public_jwk=jwk, now=1_000_000 + 10_000, max_age=300)
        assert r.ok is False
        assert r.reason == "signature is stale"

    def test_future_created_rejected(self):
        priv, jwk = _ed25519_key()
        req = _signed_request(priv, jwk, params={"created": 1_000_000})
        r = verify(req, public_jwk=jwk, now=1_000_000 - 500, max_skew=30)
        assert r.ok is False
        assert r.reason == "created is in the future"

    def test_expired_rejected(self):
        priv, jwk = _ed25519_key()
        req = _signed_request(priv, jwk, params={"created": 1_000_000, "expires": 1_000_100})
        r = verify(req, public_jwk=jwk, now=1_000_200)
        assert r.ok is False
        assert r.reason == "signature expired"

    def test_missing_created_rejected_by_default(self):
        # A signature with no `created` has no age, so it would replay forever.
        # The verifier must refuse it unless the caller explicitly opts out.
        priv, jwk = _ed25519_key()
        req = _signed_request(priv, jwk, params={})  # no created
        r = verify(req, public_jwk=jwk, now=1_000_010)
        assert r.ok is False
        assert r.reason == "missing created"

    def test_missing_created_allowed_only_on_explicit_optout(self):
        priv, jwk = _ed25519_key()
        req = _signed_request(priv, jwk, params={})  # no created
        r = verify(req, public_jwk=jwk, now=1_000_010, require_created=False)
        assert r.ok is True


class TestPolicy:
    def test_missing_required_component_rejected(self):
        priv, jwk = _ed25519_key()
        # Signs only @method + @path — omits @authority.
        req = _signed_request(
            priv, jwk, covered=("@method", "@path"), params={"created": 1_000_000}
        )
        r = verify(req, public_jwk=jwk, now=1_000_010)
        assert r.ok is False
        assert "authority" in r.reason

    def test_keyid_mismatch_rejected(self):
        priv, jwk = _ed25519_key()
        req = _signed_request(priv, jwk, params={"created": 1_000_000})
        r = verify(req, public_jwk=jwk, now=1_000_010, expected_keyid="someone-else")
        assert r.ok is False
        assert r.reason == "keyid mismatch"

    def test_alg_disagreeing_with_key_rejected(self):
        priv, jwk = _ed25519_key()
        # Claim ES256 in the params while signing with an Ed25519 key.
        req = _signed_request(priv, jwk, params={"created": 1_000_000, "alg": rfc9421.ALG_ES256})
        r = verify(req, public_jwk=jwk, now=1_000_010)
        assert r.ok is False
        assert r.reason == "alg does not match key"


class TestMalformed:
    def test_missing_headers(self):
        r = verify(_request(), public_jwk={"kty": "OKP"})
        assert r.ok is False
        assert "missing" in r.reason

    def test_garbage_signature_input(self):
        req = _request(headers={"signature-input": "sig1=((", "signature": "sig1=:AA==:"})
        r = verify(req, public_jwk={"kty": "OKP", "crv": "Ed25519", "x": "AA"})
        assert r.ok is False

    def test_unsupported_component_parameter_refused(self):
        priv, jwk = _ed25519_key()
        # Hand-craft a Signature-Input with a parameterised component (;sf),
        # which the engine refuses rather than guesses at.
        req = _request(
            headers={
                "signature-input": 'sig1=("@method" "content-type";sf);created=1000000;keyid="ed-kid";alg="ed25519"',
                "signature": "sig1=:AAAA:",
                "content-type": "application/json",
            }
        )
        r = verify(req, public_jwk=jwk, now=1_000_010)
        assert r.ok is False
