"""
AP2 Checkout Mandate: JCS canonicalization, SD-JWT issue/verify, and the
mandate service.

The SD-JWT tests are the security-critical ones — a signed mandate that a
verifier accepts must attest exactly what the merchant signed, no more (a
disclosure the signature didn't commit to is rejected) and no less (Ed25519 is
refused outright, per AP2 v0.2).
"""

import base64

import pytest
from cryptography.hazmat.primitives.asymmetric import ec, ed25519

from agentic.domain import jcs
from agentic.identity import sdjwt
from agentic.identity.sdjwt import MandateSigningError

# ---------------------------------------------------------------- JCS -------- #


class TestJCS:
    def test_sorts_keys_and_strips_whitespace(self):
        assert jcs.canonicalize({"b": 1, "a": 2}) == b'{"a":2,"b":1}'

    def test_nested_and_lists(self):
        out = jcs.canonicalize({"z": [3, {"y": 1, "x": 2}], "a": "hi"})
        assert out == b'{"a":"hi","z":[3,{"x":2,"y":1}]}'

    def test_rejects_floats(self):
        # Money must be integer minor units — a float is a loud error.
        with pytest.raises(TypeError):
            jcs.canonicalize({"amount": 19.99})

    def test_deterministic(self):
        obj = {"currency": "USD", "amount": 1999, "items": [{"q": 2, "p": 100}]}
        assert jcs.canonicalize(obj) == jcs.canonicalize(dict(reversed(list(obj.items()))))


# ------------------------------------------------------------- SD-JWT -------- #


def _ec_key(curve=None):
    priv = ec.generate_private_key(curve or ec.SECP256R1())
    nums = priv.public_key().public_numbers()
    size = (priv.curve.key_size + 7) // 8
    crv = {"secp256r1": "P-256", "secp384r1": "P-384", "secp521r1": "P-521"}[priv.curve.name]

    def b64(v):
        return base64.urlsafe_b64encode(v.to_bytes(size, "big")).rstrip(b"=").decode()

    jwk = {"kty": "EC", "crv": crv, "x": b64(nums.x), "y": b64(nums.y), "kid": "ap2-kid"}
    return priv, jwk


def _issue(priv, **kw):
    defaults = {
        "always_claims": {"amount_due": {"amount": 11487, "currency": "USD"}, "order_ref": "1"},
        "sd_claims": {"buyer_email": "shopper@example.com"},
        "private_key": priv,
        "kid": "ap2-kid",
        "iss": "https://store.example",
        "iat": 1_000_000,
        "exp": 1_000_000 + 540 * 86400,
        "vct": "https://spwig.com/ap2/checkout-mandate/v1",
    }
    defaults.update(kw)
    return sdjwt.issue_sd_jwt(**defaults)


WITHIN = 1_000_100  # a `now` inside the issued token's validity window


class TestSDJWT:
    def test_es256_roundtrip(self):
        priv, jwk = _ec_key()
        token = _issue(priv)
        assert token.endswith("~")
        payload, disclosed = sdjwt.verify_sd_jwt(token, public_jwk=jwk, now=WITHIN)
        assert payload["amount_due"] == {"amount": 11487, "currency": "USD"}
        assert payload["vct"].endswith("checkout-mandate/v1")
        # Selectively-disclosed claim recovered; only its digest was in the JWT.
        assert disclosed["buyer_email"] == "shopper@example.com"
        assert "buyer_email" not in payload

    def test_es384_and_es512(self):
        for curve in (ec.SECP384R1(), ec.SECP521R1()):
            priv, jwk = _ec_key(curve)
            token = _issue(priv)
            payload, _ = sdjwt.verify_sd_jwt(token, public_jwk=jwk, now=WITHIN)
            assert payload["order_ref"] == "1"

    def test_ed25519_is_rejected(self):
        # AP2 v0.2 forbids Ed25519 for the checkout JWT.
        priv = ed25519.Ed25519PrivateKey.generate()
        with pytest.raises(MandateSigningError, match="ECDSA"):
            _issue(priv)

    def test_tampered_payload_fails(self):
        priv, jwk = _ec_key()
        token = _issue(priv)
        jwt, _, rest = token.partition("~")
        h, p, s = jwt.split(".")
        # Flip a byte in the payload segment.
        forged_p = p[:-2] + ("AA" if p[-2:] != "AA" else "BB")
        forged = f"{h}.{forged_p}.{s}~{rest}"
        with pytest.raises(MandateSigningError):
            sdjwt.verify_sd_jwt(forged, public_jwk=jwk, now=WITHIN)

    def test_wrong_key_fails(self):
        priv, _ = _ec_key()
        _, other_jwk = _ec_key()
        token = _issue(priv)
        with pytest.raises(MandateSigningError):
            sdjwt.verify_sd_jwt(token, public_jwk=other_jwk, now=WITHIN)

    def test_forged_disclosure_rejected(self):
        # Appending a disclosure the signature never committed to must be refused.
        priv, jwk = _ec_key()
        token = _issue(priv)
        rogue = sdjwt.b64url_encode(jcs.canonicalize(["saltsaltsalt", "is_admin", True]))
        forged = token + rogue + "~"
        with pytest.raises(MandateSigningError, match="not committed"):
            sdjwt.verify_sd_jwt(forged, public_jwk=jwk, now=WITHIN)

    def test_expired_mandate_rejected(self):
        # Signature-valid but past exp → refused (a payment network treats
        # verification success as validity).
        priv, jwk = _ec_key()
        token = _issue(priv)
        after_expiry = 1_000_000 + 541 * 86400
        with pytest.raises(MandateSigningError, match="expired"):
            sdjwt.verify_sd_jwt(token, public_jwk=jwk, now=after_expiry)

    def test_alg_curve_mismatch_rejected(self):
        # A P-256 key presented with an ES384 header must not verify.
        priv, jwk = _ec_key()
        token = _issue(priv)
        lying = {**jwk, "crv": "P-384"}
        with pytest.raises(MandateSigningError, match="curve"):
            sdjwt.verify_sd_jwt(token, public_jwk=lying, now=WITHIN)


# ------------------------------------------------------- mandate service ----- #


@pytest.mark.django_db
class TestMandateService:
    def _order(self):
        from tests.factories import OrderFactory, OrderItemFactory

        order = OrderFactory()
        OrderItemFactory(order=order, quantity=2)
        return order

    def test_no_ap2_key_means_no_mandate(self, site_settings):
        from agentic.services import mandate_service

        assert mandate_service.issue_checkout_mandate(self._order()) is None

    def test_issues_and_is_verifiable_against_published_jwk(self, site_settings):
        from agentic.identity.keys import generate_ap2_key, get_jwks
        from agentic.services import mandate_service

        key = generate_ap2_key()
        order = self._order()
        mandate = mandate_service.issue_checkout_mandate(order, ucp_checkout_id="chk1")

        assert mandate is not None
        assert mandate.alg == "ES256"
        assert mandate.attested_amount == order.total_amount
        assert mandate.ucp_checkout_id == "chk1"
        # 540-day retention window.
        assert (mandate.expires_at - mandate.issued_at).days == 540

        # The published JWKS contains the signing key; the SD-JWT verifies.
        jwk = next(k for k in get_jwks()["keys"] if k["kid"] == key.kid)
        payload, disclosed = sdjwt.verify_sd_jwt(mandate.sd_jwt, public_jwk=jwk)
        assert payload["order_ref"] == str(order.id)
        assert payload["amount_due"]["currency"] == str(order.total_amount.currency)
        assert disclosed["buyer_email"] == order.email

    def test_mandate_cannot_be_deleted(self, site_settings):
        from agentic.identity.keys import generate_ap2_key
        from agentic.services import mandate_service

        generate_ap2_key()
        mandate = mandate_service.issue_checkout_mandate(self._order())
        with pytest.raises(ValueError, match="cannot be deleted"):
            mandate.delete()
