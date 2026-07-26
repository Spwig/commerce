"""
Agent authentication: trust-on-first-use, the read-posture gate, and the two
read surfaces (catalog REST + MCP) enforcing it.

Key resolution is mocked throughout (resolve_agent_key), so no network is
touched; the signatures themselves are real (signed with a throwaway Ed25519
key) and travel through the actual verification engine.
"""

import base64
import time
from unittest import mock

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from django.test import Client, RequestFactory

from agentic.identity import authentication, rfc9421
from agentic.identity import keys as key_utils
from agentic.identity.authentication import (
    AgentAuthError,
    authenticate_agent,
    require_read_access,
)
from agentic.models import AgentEvent, AgenticSettings, AgentIdentity, AgentPolicy

pytestmark = [pytest.mark.django_db, pytest.mark.integration]

SIG_AGENT = "https://agent.example.com"


@pytest.fixture(autouse=True)
def _clear_cache():
    # The rate limiter and resolver caches live in the process cache; isolate
    # each test so counters/keys don't leak across them.
    from django.core.cache import cache

    cache.clear()
    yield
    cache.clear()


def _keypair():
    priv = ed25519.Ed25519PrivateKey.generate()
    x = priv.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    x_b64 = base64.urlsafe_b64encode(x).rstrip(b"=").decode()
    required = {"crv": "Ed25519", "kty": "OKP", "x": x_b64}
    kid = key_utils._thumbprint(required)
    jwk = {**required, "kid": kid, "alg": "EdDSA", "use": "sig"}
    return priv, jwk, kid


def _sign_headers(priv, jwk, kid, *, method, host, path, query=""):
    """Build Signature-Input / Signature / Signature-Agent for a request."""
    covered = ("@method", "@authority", "@path")
    created = int(time.time())
    raw_value = f'("@method" "@authority" "@path");created={created};keyid="{kid}";alg="ed25519"'
    member = rfc9421._SignatureInputMember("sig1", [(c, {}) for c in covered], {}, raw_value)
    req = rfc9421.SignatureRequest(
        method=method, scheme="http", authority=host, path=path, query=query
    )
    base = rfc9421.build_signature_base(member, req)
    sig = priv.sign(base)
    return {
        "Signature-Input": f"sig1={raw_value}",
        "Signature": f"sig1=:{base64.b64encode(sig).decode()}:",
        "Signature-Agent": SIG_AGENT,
    }


def _enable(**overrides):
    s = AgenticSettings.get_settings()
    s.is_enabled = True
    for k, v in overrides.items():
        setattr(s, k, v)
    s.save()


class TestAuthenticateAgent:
    def test_unsigned_request_is_anonymous(self):
        rf = RequestFactory()
        assert authenticate_agent(rf.get("/api/agentic/ucp/products/")) is None

    def test_trust_on_first_use_creates_capped_identity(self):
        priv, jwk, kid = _keypair()
        rf = RequestFactory()
        headers = _sign_headers(
            priv, jwk, kid, method="POST", host="testserver", path="/api/agentic/mcp"
        )
        req = rf.post("/api/agentic/mcp", headers=headers)

        with mock.patch.object(authentication, "resolve_agent_key", return_value=jwk):
            ctx = authenticate_agent(req)

        assert ctx is not None
        assert ctx.created is True
        assert ctx.identity.directory == "agent.example.com"
        assert ctx.identity.key_thumbprint == kid
        assert ctx.identity.trust_state == AgentIdentity.TRUST_CAPPED
        # A capped policy was created alongside it.
        assert AgentPolicy.objects.filter(agent=ctx.identity).exists()
        # First-use + verification both logged, chain intact.
        types = list(AgentEvent.objects.values_list("event_type", flat=True))
        assert AgentEvent.EVENT_AGENT_SEEN in types
        assert AgentEvent.EVENT_SIG_VERIFIED in types
        assert AgentEvent.verify_chain() is True

    def test_second_sighting_reuses_identity(self):
        priv, jwk, kid = _keypair()
        rf = RequestFactory()

        def _authed():
            headers = _sign_headers(
                priv, jwk, kid, method="POST", host="testserver", path="/api/agentic/mcp"
            )
            req = rf.post("/api/agentic/mcp", headers=headers)
            with mock.patch.object(authentication, "resolve_agent_key", return_value=jwk):
                return authenticate_agent(req)

        first = _authed()
        second = _authed()
        assert first.created is True
        assert second.created is False
        assert AgentIdentity.objects.count() == 1
        # Only one agent_seen, but two sig_verified.
        assert AgentEvent.objects.filter(event_type=AgentEvent.EVENT_AGENT_SEEN).count() == 1
        assert AgentEvent.objects.filter(event_type=AgentEvent.EVENT_SIG_VERIFIED).count() == 2
        second.identity.refresh_from_db()
        assert second.identity.request_count == 2

    def test_bad_signature_creates_no_identity_and_logs_failure(self):
        priv, jwk, kid = _keypair()
        rf = RequestFactory()
        headers = _sign_headers(
            priv, jwk, kid, method="POST", host="testserver", path="/api/agentic/mcp"
        )
        # Tamper: deliver to a different path than was signed.
        req = rf.post("/api/agentic/checkout", headers=headers)

        with mock.patch.object(authentication, "resolve_agent_key", return_value=jwk):
            with pytest.raises(AgentAuthError):
                authenticate_agent(req)

        assert AgentIdentity.objects.count() == 0
        assert AgentEvent.objects.filter(event_type=AgentEvent.EVENT_SIG_FAILED).exists()

    def test_incomplete_headers_rejected(self):
        rf = RequestFactory()
        # Signature-Agent present but no Signature/Signature-Input.
        req = rf.post("/api/agentic/mcp", headers={"Signature-Agent": SIG_AGENT})
        with pytest.raises(AgentAuthError):
            authenticate_agent(req)

    def test_unresolvable_key_rejected(self):
        priv, jwk, kid = _keypair()
        rf = RequestFactory()
        headers = _sign_headers(
            priv, jwk, kid, method="POST", host="testserver", path="/api/agentic/mcp"
        )
        req = rf.post("/api/agentic/mcp", headers=headers)
        with mock.patch.object(
            authentication,
            "resolve_agent_key",
            side_effect=authentication.ResolutionError("nope"),
        ):
            with pytest.raises(AgentAuthError):
                authenticate_agent(req)
        assert AgentIdentity.objects.count() == 0


class TestRateLimit:
    def test_signed_attempts_are_rate_limited(self):
        # The per-IP ceiling bounds the attacker-directed key-resolution fetch.
        priv, jwk, kid = _keypair()
        rf = RequestFactory()

        def _attempt():
            headers = _sign_headers(
                priv, jwk, kid, method="POST", host="testserver", path="/api/agentic/mcp"
            )
            req = rf.post("/api/agentic/mcp", headers=headers)
            with mock.patch.object(authentication, "resolve_agent_key", return_value=jwk):
                return authenticate_agent(req)

        # Drive just past the per-IP window and confirm it trips.
        with mock.patch.object(authentication, "AUTH_RATE_PER_IP", 3):
            for _ in range(3):
                _attempt()
            with pytest.raises(authentication.AgentRateLimited):
                _attempt()

    def test_rate_limited_attempt_is_not_logged(self):
        # A throttled attempt must NOT write to the floodable append-only log.
        priv, jwk, kid = _keypair()
        rf = RequestFactory()
        headers = _sign_headers(
            priv, jwk, kid, method="POST", host="testserver", path="/api/agentic/mcp"
        )
        req = rf.post("/api/agentic/mcp", headers=headers)
        with mock.patch.object(authentication, "AUTH_RATE_PER_IP", 0):
            with pytest.raises(authentication.AgentRateLimited):
                authenticate_agent(req)
        assert AgentEvent.objects.count() == 0


class TestReadPosture:
    def test_unsigned_allowed_when_unverified_reads_permitted(self):
        _enable(allow_unverified_read=True)
        rf = RequestFactory()
        assert require_read_access(rf.get("/api/agentic/ucp/products/")) is None

    def test_unsigned_refused_when_unverified_reads_disallowed(self):
        _enable(allow_unverified_read=False)
        rf = RequestFactory()
        with pytest.raises(AgentAuthError, match="required"):
            require_read_access(rf.get("/api/agentic/ucp/products/"))

    def test_blocked_agent_refused(self):
        priv, jwk, kid = _keypair()
        AgentIdentity.objects.create(
            directory="agent.example.com",
            key_thumbprint=kid,
            algorithm="ed25519",
            public_jwk=jwk,
            trust_state=AgentIdentity.TRUST_BLOCKED,
        )
        rf = RequestFactory()
        headers = _sign_headers(
            priv, jwk, kid, method="GET", host="testserver", path="/api/agentic/ucp/products/"
        )
        req = rf.get("/api/agentic/ucp/products/", headers=headers)
        with mock.patch.object(authentication, "resolve_agent_key", return_value=jwk):
            with pytest.raises(AgentAuthError, match="blocked"):
                require_read_access(req)


class TestReadSurfacesEnforcePosture:
    """The catalog REST + MCP endpoints must honour the posture end-to-end."""

    def test_catalog_401_when_unverified_disallowed_and_unsigned(self):
        _enable(allow_unverified_read=False)
        resp = Client().get("/api/agentic/ucp/products/")
        assert resp.status_code == 401

    def test_catalog_ok_with_valid_signature(self):
        _enable(allow_unverified_read=False)
        priv, jwk, kid = _keypair()
        headers = _sign_headers(
            priv, jwk, kid, method="GET", host="testserver", path="/api/agentic/ucp/products/"
        )
        with mock.patch.object(authentication, "resolve_agent_key", return_value=jwk):
            resp = Client().get("/api/agentic/ucp/products/", headers=headers)
        assert resp.status_code == 200
        assert AgentIdentity.objects.count() == 1

    def test_mcp_401_when_unverified_disallowed_and_unsigned(self):
        _enable(allow_unverified_read=False)
        resp = Client().post(
            "/api/agentic/mcp",
            data='{"jsonrpc":"2.0","method":"ping","id":1}',
            content_type="application/json",
        )
        assert resp.status_code == 401

    def test_mcp_ok_with_valid_signature(self):
        _enable(allow_unverified_read=False)
        priv, jwk, kid = _keypair()
        headers = _sign_headers(
            priv, jwk, kid, method="POST", host="testserver", path="/api/agentic/mcp"
        )
        with mock.patch.object(authentication, "resolve_agent_key", return_value=jwk):
            resp = Client().post(
                "/api/agentic/mcp",
                data='{"jsonrpc":"2.0","method":"ping","id":1}',
                content_type="application/json",
                headers=headers,
            )
        assert resp.status_code == 200
        assert resp.json()["result"] == {}
