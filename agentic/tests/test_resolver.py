"""
Directory key resolver — SSRF guards, thumbprint binding, caching.

The network fetch itself is never exercised against a real host: the SSRF
decision surface (URL scheme, IP classification) and the key-selection logic
(recomputed thumbprint must match the claimed keyid) are what matter, and both
are unit-testable with the socket/HTTP layer patched.
"""

from unittest import mock

import pytest

from agentic.identity import keys as key_utils
from agentic.identity import resolver
from agentic.identity.resolver import ResolutionError, resolve_agent_key

pytestmark = pytest.mark.django_db


def _make_jwk():
    """A real Ed25519 public JWK plus its RFC 7638 thumbprint (the keyid)."""
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import ed25519

    priv = ed25519.Ed25519PrivateKey.generate()
    x = priv.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    import base64

    x_b64 = base64.urlsafe_b64encode(x).rstrip(b"=").decode()
    required = {"crv": "Ed25519", "kty": "OKP", "x": x_b64}
    kid = key_utils._thumbprint(required)
    return {**required, "kid": kid, "alg": "EdDSA", "use": "sig"}, kid


class TestSSRFGuards:
    def test_http_scheme_rejected(self):
        with pytest.raises(ResolutionError, match="https"):
            resolver._directory_url("http://agent.example.com")

    def test_empty_signature_agent_rejected(self):
        with pytest.raises(ResolutionError):
            resolver._directory_url("")

    def test_bare_origin_gets_well_known_path(self):
        url = resolver._directory_url("https://agent.example.com")
        assert url.endswith(resolver.DIRECTORY_WELL_KNOWN)

    def test_explicit_path_preserved(self):
        url = resolver._directory_url("https://agent.example.com/keys.json")
        assert url == "https://agent.example.com/keys.json"

    def test_private_ip_rejected(self):
        with mock.patch.object(
            resolver.socket,
            "getaddrinfo",
            return_value=[(None, None, None, "", ("10.0.0.5", 0))],
        ):
            with pytest.raises(ResolutionError, match="non-public"):
                resolver._resolve_public_ips("internal.example")

    def test_loopback_rejected(self):
        with mock.patch.object(
            resolver.socket,
            "getaddrinfo",
            return_value=[(None, None, None, "", ("127.0.0.1", 0))],
        ):
            with pytest.raises(ResolutionError):
                resolver._resolve_public_ips("localhost")

    def test_cloud_metadata_ip_rejected(self):
        # 169.254.169.254 — the classic SSRF target.
        with mock.patch.object(
            resolver.socket,
            "getaddrinfo",
            return_value=[(None, None, None, "", ("169.254.169.254", 0))],
        ):
            with pytest.raises(ResolutionError):
                resolver._resolve_public_ips("metadata")

    def test_mixed_public_and_private_rejected(self):
        # A host resolving to both a public and a private address is refused
        # wholesale — the classic DNS-rebinding dodge.
        with mock.patch.object(
            resolver.socket,
            "getaddrinfo",
            return_value=[
                (None, None, None, "", ("93.184.216.34", 0)),
                (None, None, None, "", ("10.0.0.1", 0)),
            ],
        ):
            with pytest.raises(ResolutionError):
                resolver._resolve_public_ips("evil.example")

    def test_public_ip_allowed(self):
        with mock.patch.object(
            resolver.socket,
            "getaddrinfo",
            return_value=[(None, None, None, "", ("93.184.216.34", 0))],
        ):
            assert resolver._resolve_public_ips("example.com") == ["93.184.216.34"]

    def test_nat64_embedded_private_v4_rejected(self):
        # 64:ff9b::/96 (NAT64) classifies as global on CPython but can map to an
        # internal v4 target — it must be blocked explicitly.
        with mock.patch.object(
            resolver.socket,
            "getaddrinfo",
            return_value=[(None, None, None, "", ("64:ff9b::a00:1", 0))],  # -> 10.0.0.1
        ):
            with pytest.raises(ResolutionError):
                resolver._resolve_public_ips("nat64.example")

    def test_ipv4_mapped_private_rejected(self):
        with mock.patch.object(
            resolver.socket,
            "getaddrinfo",
            return_value=[(None, None, None, "", ("::ffff:10.0.0.1", 0))],
        ):
            with pytest.raises(ResolutionError):
                resolver._resolve_public_ips("mapped.example")


class TestKeySelection:
    def test_matching_key_selected(self):
        jwk, kid = _make_jwk()
        got = resolver._select_key({"keys": [jwk]}, kid)
        assert got["kid"] == kid
        assert "d" not in got  # public members only

    def test_keyid_bound_to_recomputed_thumbprint(self):
        # A directory that serves a key under a LYING kid must not resolve: we
        # recompute the thumbprint and match on that, never on the served kid.
        jwk, kid = _make_jwk()
        lying = {**jwk, "kid": "attacker-chosen-id"}
        with pytest.raises(ResolutionError, match="no key"):
            resolver._select_key({"keys": [lying]}, "attacker-chosen-id")
        # ...but it DOES resolve under its true thumbprint.
        assert resolver._select_key({"keys": [lying]}, kid)["kid"] == kid

    def test_no_keys_array(self):
        with pytest.raises(ResolutionError):
            resolver._select_key({}, "whatever")


class TestResolveAndCache:
    def test_resolve_end_to_end_with_mocked_fetch(self):
        jwk, kid = _make_jwk()
        with mock.patch.object(resolver, "_fetch_directory", return_value={"keys": [jwk]}) as f:
            got = resolve_agent_key("https://agent.example.com", kid, use_cache=False)
            assert got["kid"] == kid
            f.assert_called_once()

    def test_missing_keyid(self):
        with pytest.raises(ResolutionError, match="keyid"):
            resolve_agent_key("https://agent.example.com", "", use_cache=False)

    def test_positive_result_is_cached(self):
        jwk, kid = _make_jwk()
        with mock.patch.object(resolver, "_fetch_directory", return_value={"keys": [jwk]}) as f:
            resolve_agent_key("https://a.example.com", kid)
            resolve_agent_key("https://a.example.com", kid)
            # Second call served from cache — fetch happened once.
            f.assert_called_once()

    def test_negative_result_is_cached(self):
        with mock.patch.object(resolver, "_fetch_directory", return_value={"keys": []}) as f:
            with pytest.raises(ResolutionError):
                resolve_agent_key("https://b.example.com", "nope")
            with pytest.raises(ResolutionError, match="cached"):
                resolve_agent_key("https://b.example.com", "nope")
            f.assert_called_once()

    def test_document_cached_by_url_across_keyids(self):
        # Probing many keyids against ONE host must not re-trigger the outbound
        # fetch: the document is cached by URL, so requests.get is hit once.
        jwk, kid = _make_jwk()
        url = "https://c.example.com" + resolver.DIRECTORY_WELL_KNOWN

        import json as _json

        raw = mock.Mock()
        raw.read.return_value = _json.dumps({"keys": [jwk]}).encode()
        resp = mock.MagicMock(status_code=200, raw=raw)
        resp.__enter__.return_value = resp
        resp.__exit__.return_value = False

        with mock.patch.object(resolver, "_resolve_public_ips", return_value=["93.184.216.34"]):
            with mock.patch.object(resolver.requests, "get", return_value=resp) as g:
                # Real keyid resolves; a bogus keyid against the same host reuses
                # the cached document (fetch still happened only once).
                assert resolve_agent_key("https://c.example.com", kid)["kid"] == kid
                with pytest.raises(ResolutionError):
                    resolve_agent_key("https://c.example.com", "missing-kid")
                g.assert_called_once()
