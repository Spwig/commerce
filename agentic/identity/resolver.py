"""
Resolve a calling agent's public key from its Web Bot Auth key directory.

An agent authenticates with an RFC 9421 signature and a ``Signature-Agent``
header naming the HTTPS URL of its key directory. To verify the signature we
must fetch that directory, find the key whose RFC 7638 thumbprint equals the
signature's ``keyid``, and confirm the served key really does hash to that
thumbprint (so a directory cannot serve an arbitrary key under someone else's
id).

Fetching an attacker-named URL is an SSRF sink, so ``_fetch_directory`` is
hardened:

- **HTTPS only.** No ``http://``, no ``file://``, no other scheme.
- **No redirects.** A 302 could bounce onto a private address after the IP
  check; redirects are refused outright.
- **Public IPs only.** The host is resolved and every returned address must be
  global — loopback, private, link-local, and other reserved ranges are
  rejected (blocks ``localhost``, ``169.254.169.254`` cloud metadata, RFC 1918).
- **Bounded.** Short timeout and a response-size cap; the body is streamed and
  truncated rather than read whole.

Residual: the IP is validated and then a normal request is issued, so a
determined DNS-rebinding attacker controlling the directory's DNS could flip the
record between the check and the fetch. Closing that fully needs a connection
pinned to the validated IP with SNI kept on the hostname; it is called out for
the mandated security-auditor pass. The blast radius meanwhile is a read-only
GET, only reachable once an agent presents a signature.
"""

from __future__ import annotations

import ipaddress
import logging
import socket
from urllib.parse import urlparse

import requests
from django.core.cache import cache

from agentic.identity import keys as key_utils

logger = logging.getLogger(__name__)

DIRECTORY_WELL_KNOWN = "/.well-known/http-message-signatures-directory"
FETCH_TIMEOUT = 5  # seconds
MAX_DIRECTORY_BYTES = 256 * 1024
CACHE_TTL = 300  # seconds; a resolved (directory, keyid) -> jwk mapping
NEGATIVE_CACHE_TTL = 60  # seconds; remember "not found" briefly to blunt abuse
DOC_CACHE_TTL = 120  # seconds; the fetched directory DOCUMENT, keyed by URL

# IPv6 ranges that EMBED an IPv4 address and can therefore be used to smuggle an
# internal v4 target past a naive `is_global` check. `ipaddress` classifies the
# NAT64 well-known prefix as global on CPython 3.12, so it must be blocked
# explicitly; 6to4 wraps an arbitrary v4 in the same way.
_EMBEDDED_V4_NETS = [
    ipaddress.ip_network("64:ff9b::/96"),  # NAT64 well-known (RFC 6052)
    ipaddress.ip_network("64:ff9b:1::/48"),  # NAT64 local-use (RFC 8215)
    ipaddress.ip_network("2002::/16"),  # 6to4 (RFC 3056)
]


class ResolutionError(Exception):
    """The agent's key could not be resolved (bad URL, SSRF block, not found)."""


def _addr_is_public(addr: ipaddress._BaseAddress) -> bool:
    """A single address is usable only if it is global and not an SSRF smuggle."""
    if not addr.is_global or addr.is_multicast:
        return False
    # Unwrap an IPv4-mapped IPv6 address (::ffff:a.b.c.d) and re-check the v4.
    mapped = getattr(addr, "ipv4_mapped", None)
    if mapped is not None and (not mapped.is_global or mapped.is_multicast):
        return False
    return all(addr not in net for net in _EMBEDDED_V4_NETS)


def _resolve_public_ips(host: str) -> list[str]:
    """Resolve ``host`` to IPs, rejecting the lookup if ANY address is not global."""
    try:
        infos = socket.getaddrinfo(host, None)
    except socket.gaierror as exc:
        raise ResolutionError(f"cannot resolve host {host!r}") from exc

    ips = {info[4][0] for info in infos}
    if not ips:
        raise ResolutionError(f"no addresses for host {host!r}")
    for ip in ips:
        addr = ipaddress.ip_address(ip)
        # Refuse the WHOLE host if any resolved address is unusable — a host that
        # resolves to both a public and a private (or IPv4-embedding) address is
        # a classic SSRF dodge.
        if not _addr_is_public(addr):
            raise ResolutionError(f"host {host!r} resolves to a non-public address")
    return sorted(ips)


def _directory_url(signature_agent: str) -> str:
    """
    Normalise a ``Signature-Agent`` value to the directory URL to fetch.

    Accepts either the directory URL directly or a bare origin (to which the
    well-known path is appended). Rejects anything that is not HTTPS.
    """
    value = (signature_agent or "").strip().strip('"')
    if not value:
        raise ResolutionError("empty Signature-Agent")
    parsed = urlparse(value)
    if parsed.scheme != "https":
        raise ResolutionError("Signature-Agent must be an https URL")
    if not parsed.hostname:
        raise ResolutionError("Signature-Agent has no host")
    path = parsed.path or ""
    if path in ("", "/"):
        # A bare origin → append the Web Bot Auth well-known directory path.
        return f"https://{parsed.netloc}{DIRECTORY_WELL_KNOWN}"
    return f"https://{parsed.netloc}{path}"


def _fetch_directory(url: str) -> dict:
    """SSRF-guarded GET of a JWKS directory document. Returns the parsed JSON."""
    # Cache the whole document by URL so that probing many keyids against one
    # host cannot re-trigger the outbound fetch — only the first hit costs a
    # network round-trip (and the SSRF check) within the window.
    doc_cache_key = f"agentic:dir-doc:{url}"
    cached_doc = cache.get(doc_cache_key)
    if cached_doc is not None:
        return cached_doc

    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname:
        raise ResolutionError("directory URL must be https with a host")
    _resolve_public_ips(parsed.hostname)  # raises on any non-public address

    try:
        resp = requests.get(
            url,
            timeout=FETCH_TIMEOUT,
            allow_redirects=False,  # a redirect could escape the IP check
            stream=True,
            headers={"Accept": "application/json"},
        )
    except requests.RequestException as exc:
        raise ResolutionError(f"directory fetch failed: {exc}") from exc

    with resp:
        if resp.status_code != 200:
            raise ResolutionError(f"directory returned HTTP {resp.status_code}")
        body = resp.raw.read(MAX_DIRECTORY_BYTES + 1, decode_content=True)
    if len(body) > MAX_DIRECTORY_BYTES:
        raise ResolutionError("directory document too large")
    try:
        import json

        document = json.loads(body.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as exc:
        raise ResolutionError("directory is not valid JSON") from exc
    cache.set(doc_cache_key, document, DOC_CACHE_TTL)
    return document


def _select_key(document: dict, keyid: str) -> dict:
    """
    Find the key in a JWKS whose RFC 7638 thumbprint equals ``keyid``, and
    confirm the served key material actually hashes to that id.
    """
    jwks = document.get("keys")
    if not isinstance(jwks, list):
        raise ResolutionError("directory has no 'keys' array")
    for jwk in jwks:
        if not isinstance(jwk, dict):
            continue
        try:
            required = key_utils.required_jwk_members(jwk)
            computed = key_utils._thumbprint(required)
        except Exception:
            continue
        if computed == keyid:
            # Trust the recomputed thumbprint, never the served "kid" field.
            return key_utils.public_jwk_view({**jwk, "kid": computed})
    raise ResolutionError(f"no key in directory matches keyid {keyid!r}")


def resolve_agent_key(signature_agent: str, keyid: str, *, use_cache: bool = True) -> dict:
    """
    Resolve and return the public JWK for ``keyid`` from the agent's directory.

    The returned JWK is stripped to public members and its ``kid`` is the
    RFC 7638 thumbprint we recomputed — never the value the directory claimed.
    Raises ResolutionError on any failure (unresolvable, SSRF-blocked, missing).
    """
    if not keyid:
        raise ResolutionError("missing keyid")
    url = _directory_url(signature_agent)
    cache_key = f"agentic:agentkey:{url}:{keyid}"

    if use_cache:
        cached = cache.get(cache_key)
        if cached is not None:
            if cached == "__miss__":
                raise ResolutionError("key not found (cached)")
            return cached

    try:
        document = _fetch_directory(url)
        jwk = _select_key(document, keyid)
    except ResolutionError:
        if use_cache:
            cache.set(cache_key, "__miss__", NEGATIVE_CACHE_TTL)
        raise

    if use_cache:
        cache.set(cache_key, jwk, CACHE_TTL)
    return jwk
