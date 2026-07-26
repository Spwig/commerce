"""
Agent authentication: turn a signed request into a known AgentIdentity.

This is the seam that ties the pieces together, and it deliberately does NOT
inherit any storefront/DRF auth mixin — 1.7.0's HeadlessAPIMixin re-added
SessionAuthentication and MobileTokenAuthentication squats on the `Bearer`
scheme, so routing agent traffic through it would collide. Agents authenticate
purely via the RFC 9421 `Signature` / `Signature-Input` / `Signature-Agent`
headers, which sidestep that collision entirely.

Flow for a request that carries a signature:

1. Parse the `keyid` out of Signature-Input.
2. Resolve that key from the agent's directory (SSRF-guarded).
3. Verify the signature (pure engine).
4. Trust-on-first-use: get_or_create the AgentIdentity for
   (directory, key_thumbprint) with a `capped` policy, and record the outcome
   in the append-only AgentEvent log.

A request with no signature is anonymous (returns None) — the read surface
stays open unless the merchant has set allow_unverified_read=False. A request
with a signature that fails verification is a hard failure: 401 and no identity
is created, so the registry can't be spammed with unverified agents.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from django.core.cache import cache
from django.utils import timezone

from agentic.identity import rfc9421
from agentic.identity.resolver import ResolutionError, resolve_agent_key
from agentic.models import AgentEvent, AgentIdentity, AgentPolicy

logger = logging.getLogger(__name__)

# Signature auth triggers an attacker-directed outbound HTTPS fetch to resolve
# the signing key. These bounds keep that from being a DoS / SSRF-amplification
# primitive: a per-client ceiling, plus a global ceiling so a distributed set of
# clients can't multiply it. Tuned coarse — a legitimate agent reuses one cached
# key and never approaches them.
AUTH_RATE_WINDOW = 60  # seconds
AUTH_RATE_PER_IP = 60  # signed-request auth attempts per client per window
AUTH_RATE_GLOBAL = 600  # signed-request auth attempts store-wide per window


class AgentAuthError(Exception):
    """A signature was presented and it did not verify. Maps to HTTP 401."""

    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(reason)


class AgentRateLimited(Exception):
    """Too many signature-auth attempts. Maps to HTTP 429."""

    def __init__(self, reason: str = "rate limited"):
        self.reason = reason
        super().__init__(reason)


def _bump(key: str, window: int) -> int:
    """Increment a fixed-window counter in the cache, returning the new count."""
    try:
        return cache.incr(key)
    except ValueError:
        # Key absent/expired — (re)initialise the window. A small init race here
        # can only UNDERCOUNT slightly, never let the limiter be bypassed.
        cache.set(key, 1, window)
        return 1


def _enforce_auth_rate_limit(request) -> None:
    """Bound signature-auth attempts before any outbound key resolution."""
    from geoip.utils.ip_utils import get_client_ip

    ip = get_client_ip(request) or "unknown"
    if _bump(f"agentic:auth:ip:{ip}", AUTH_RATE_WINDOW) > AUTH_RATE_PER_IP:
        raise AgentRateLimited("per-client rate limit exceeded")
    if _bump("agentic:auth:global", AUTH_RATE_WINDOW) > AUTH_RATE_GLOBAL:
        raise AgentRateLimited("global rate limit exceeded")


@dataclass(frozen=True)
class AgentContext:
    identity: AgentIdentity
    policy: AgentPolicy
    result: rfc9421.VerificationResult
    created: bool  # True on the first sighting of this agent


def _keyid_from_signature_input(sig_input_header: str) -> str | None:
    try:
        inputs = rfc9421.parse_signature_input(sig_input_header)
    except rfc9421.SignatureError:
        return None
    if len(inputs) != 1:
        return None
    member = next(iter(inputs.values()))
    keyid = member.params.get("keyid")
    return str(keyid) if keyid else None


def _log_failure(directory: str, keyid: str, reason: str, req: rfc9421.SignatureRequest) -> None:
    AgentEvent.append(
        AgentEvent.EVENT_SIG_FAILED,
        directory=directory,
        key_thumbprint=keyid,
        detail={"reason": reason, "method": req.method, "path": req.path},
    )


def authenticate_agent(request) -> AgentContext | None:
    """
    Authenticate an agent from a Django request.

    Returns an AgentContext on a verified signature, None if the request is
    unsigned (anonymous), and raises AgentAuthError if a signature is present
    but does not verify.
    """
    headers = {k.lower(): v for k, v in request.headers.items()}
    sig_input = headers.get("signature-input")
    signature = headers.get("signature")
    signature_agent = headers.get("signature-agent")

    # No signature at all → anonymous. The posture gate decides if that's ok.
    if not sig_input and not signature and not signature_agent:
        return None

    # A signature is present, so this request will cost a key resolution. Bound
    # the rate BEFORE the outbound fetch. Deliberately NOT logged to AgentEvent:
    # the append-only log is itself floodable, so a throttled attempt must not
    # write to it.
    _enforce_auth_rate_limit(request)

    req = rfc9421.SignatureRequest.from_django(request)

    if not (sig_input and signature and signature_agent):
        _log_failure(signature_agent or "", "", "incomplete_signature_headers", req)
        raise AgentAuthError("incomplete signature headers")

    keyid = _keyid_from_signature_input(sig_input)
    if not keyid:
        _log_failure(signature_agent, "", "no_keyid", req)
        raise AgentAuthError("no keyid in Signature-Input")

    # Resolve the signing key from the agent's directory (SSRF-guarded).
    try:
        public_jwk = resolve_agent_key(signature_agent, keyid)
    except ResolutionError as exc:
        _log_failure(signature_agent, keyid, f"key_resolution: {exc}", req)
        raise AgentAuthError("could not resolve signing key") from exc

    result = rfc9421.verify(req, public_jwk=public_jwk, expected_keyid=keyid)
    if not result.ok:
        _log_failure(signature_agent, keyid, result.reason, req)
        raise AgentAuthError(f"signature verification failed: {result.reason}")

    # Verified. Trust-on-first-use: establish (or update) the identity.
    directory = _directory_host(signature_agent)
    identity, created = AgentIdentity.objects.get_or_create(
        directory=directory,
        key_thumbprint=keyid,
        defaults={
            "algorithm": result.alg,
            "public_jwk": public_jwk,
            "trust_state": AgentIdentity.TRUST_CAPPED,
        },
    )
    policy, _ = AgentPolicy.objects.get_or_create(agent=identity)

    if created:
        AgentEvent.append(AgentEvent.EVENT_AGENT_SEEN, agent=identity, detail={"first_seen": True})
    AgentEvent.append(
        AgentEvent.EVENT_SIG_VERIFIED,
        agent=identity,
        detail={"method": req.method, "path": req.path, "alg": result.alg},
    )

    # Touch last-seen / counter without tripping the append-only model (that's a
    # different model) — this is the mutable identity row.
    AgentIdentity.objects.filter(pk=identity.pk).update(
        last_seen_at=timezone.now(),
        request_count=identity.request_count + 1,
    )

    return AgentContext(identity=identity, policy=policy, result=result, created=created)


def _directory_host(signature_agent: str) -> str:
    from urllib.parse import urlparse

    return (urlparse(signature_agent.strip().strip('"')).hostname or "").lower()


def require_read_access(request) -> AgentContext | None:
    """
    Enforce the merchant's read posture on a discovery/catalog request.

    - A present-but-invalid signature always fails (AgentAuthError → 401),
      whatever the posture — a bad signature is never treated as "anonymous".
    - An unsigned request is allowed only when the merchant permits unverified
      reads (the default); otherwise it is refused. A blocked agent is refused.
    """
    ctx = authenticate_agent(request)  # raises AgentAuthError on a bad signature
    if ctx is not None and ctx.identity.is_blocked:
        raise AgentAuthError("agent is blocked")
    if ctx is None:
        from agentic.models import AgenticSettings

        if not AgenticSettings.get_settings().allow_unverified_read:
            raise AgentAuthError("agent signature required")
    return ctx


def require_verified_agent(request) -> AgentContext | None:
    """
    Enforce checkout access — a stricter posture than reads.

    Checkout moves money, so an unsigned request is refused unless the merchant
    has explicitly opted into unverified checkout (default False). A verified
    but blocked agent is always refused. Returns the AgentContext (or None only
    when unverified checkout is permitted and the request is unsigned).
    """
    ctx = authenticate_agent(request)  # raises on a bad signature / rate limit
    if ctx is not None and ctx.identity.is_blocked:
        raise AgentAuthError("agent is blocked")
    if ctx is None:
        from agentic.models import AgenticSettings

        if not AgenticSettings.get_settings().allow_unverified_checkout:
            raise AgentAuthError("a verified agent signature is required for checkout")
    return ctx
