"""
RFC 9421 HTTP Message Signature verification — the pure engine.

This module verifies an INBOUND signature from a calling agent. It has no
Django request coupling beyond a small adapter (`SignatureRequest.from_django`)
and no network access — key resolution is the caller's job (see
`agentic/identity/resolver.py`), so this file can be unit-tested purely by
signing a request with a throwaway key and verifying it back.

Scope, deliberately narrow (fail closed on anything outside it):

- Covered components: the derived components ``@method`` ``@authority``
  ``@path`` ``@query`` ``@scheme`` ``@target-uri``, and plain HTTP header
  fields. Anything else (``@query-param``, ``;sf`` / ``;bs`` / ``;key`` /
  ``;req`` component parameters) is refused rather than guessed at — a
  misreconstructed base would only ever fail to verify, but refusing is
  clearer than a mysterious signature mismatch.
- Algorithms: ``ed25519`` (OKP/Ed25519) and ``ecdsa-p256-sha256`` (EC/P-256),
  matching the two AgentKey policies. ``ecdsa-p256-sha256`` signatures are the
  JWS-style raw ``r || s`` (IEEE P1363), converted to DER for verification.

A verification bug here degrades to "the agent cannot authenticate" (a safe
refusal), never to "a forged request is accepted" — every uncertain path
returns ``VerificationResult(ok=False, ...)``.
"""

from __future__ import annotations

import base64
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, ed25519
from cryptography.hazmat.primitives.asymmetric.utils import (
    encode_dss_signature,
)

# Algorithm identifiers (RFC 9421 §3.3 registry).
ALG_ED25519 = "ed25519"
ALG_ES256 = "ecdsa-p256-sha256"

# Default freshness window for the `created` parameter, in seconds.
DEFAULT_MAX_AGE = 300
# Allowed clock skew for a `created` timestamp that sits slightly in the future.
DEFAULT_MAX_SKEW = 30


class SignatureError(Exception):
    """A malformed signature/header the engine refuses to process further."""


@dataclass(frozen=True)
class VerificationResult:
    ok: bool
    reason: str = ""
    keyid: str = ""
    alg: str = ""
    covered: tuple[str, ...] = ()
    created: int | None = None
    tag: str = ""

    def __bool__(self) -> bool:  # allow `if result:`
        return self.ok


# --------------------------------------------------------------------------- #
# Minimal RFC 8941 structured-field parsing (only what RFC 9421 needs).
# --------------------------------------------------------------------------- #


def _b64url_decode(s: str) -> bytes:
    pad = "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s + pad)


class _Parser:
    """A small cursor over an ASCII structured-field string (RFC 8941 §4.2)."""

    def __init__(self, text: str):
        self.s = text
        self.i = 0

    def _skip_sp(self):
        while self.i < len(self.s) and self.s[self.i] == " ":
            self.i += 1

    def _skip_ows(self):
        while self.i < len(self.s) and self.s[self.i] in " \t":
            self.i += 1

    def eof(self) -> bool:
        return self.i >= len(self.s)

    def peek(self) -> str:
        return self.s[self.i] if self.i < len(self.s) else ""

    # --- bare items ------------------------------------------------------- #
    def parse_string(self) -> str:
        if self.peek() != '"':
            raise SignatureError("expected string")
        self.i += 1
        out = []
        while self.i < len(self.s):
            ch = self.s[self.i]
            self.i += 1
            if ch == "\\":
                if self.i >= len(self.s):
                    raise SignatureError("bad string escape")
                nxt = self.s[self.i]
                self.i += 1
                if nxt not in ('"', "\\"):
                    raise SignatureError("invalid escape")
                out.append(nxt)
            elif ch == '"':
                return "".join(out)
            elif ord(ch) < 0x20 or ord(ch) >= 0x7F:
                raise SignatureError("invalid string char")
            else:
                out.append(ch)
        raise SignatureError("unterminated string")

    def parse_token(self) -> _Token:
        start = self.i
        c = self.peek()
        if not (c.isalpha() or c == "*"):
            raise SignatureError("expected token")
        self.i += 1
        allowed = "!#$%&'*+-.^_`|~:/"
        while self.i < len(self.s):
            c = self.s[self.i]
            if c.isalnum() or c in allowed:
                self.i += 1
            else:
                break
        return _Token(self.s[start : self.i])

    def parse_byte_sequence(self) -> bytes:
        if self.peek() != ":":
            raise SignatureError("expected byte sequence")
        self.i += 1
        end = self.s.find(":", self.i)
        if end == -1:
            raise SignatureError("unterminated byte sequence")
        raw = self.s[self.i : end]
        self.i = end + 1
        try:
            pad = "=" * (-len(raw) % 4)
            return base64.b64decode(raw + pad, validate=True)
        except Exception as exc:
            raise SignatureError("bad base64 in byte sequence") from exc

    def parse_boolean(self) -> bool:
        if self.peek() != "?":
            raise SignatureError("expected boolean")
        self.i += 1
        c = self.peek()
        if c not in ("0", "1"):
            raise SignatureError("bad boolean")
        self.i += 1
        return c == "1"

    def parse_number(self):
        start = self.i
        if self.peek() == "-":
            self.i += 1
        is_decimal = False
        while self.i < len(self.s):
            c = self.s[self.i]
            if c.isdigit():
                self.i += 1
            elif c == "." and not is_decimal:
                is_decimal = True
                self.i += 1
            else:
                break
        raw = self.s[start : self.i]
        if raw in ("", "-"):
            raise SignatureError("expected number")
        return float(raw) if is_decimal else int(raw)

    def parse_bare_item(self):
        c = self.peek()
        if c == '"':
            return self.parse_string()
        if c == ":":
            return self.parse_byte_sequence()
        if c == "?":
            return self.parse_boolean()
        if c == "-" or c.isdigit():
            return self.parse_number()
        if c.isalpha() or c == "*":
            return self.parse_token()
        raise SignatureError(f"unexpected char {c!r}")

    def parse_key(self) -> str:
        start = self.i
        c = self.peek()
        if not (c.islower() or c == "*"):
            raise SignatureError("expected parameter key")
        self.i += 1
        while self.i < len(self.s):
            c = self.s[self.i]
            if c.islower() or c.isdigit() or c in "_-.*":
                self.i += 1
            else:
                break
        return self.s[start : self.i]

    def parse_parameters(self) -> dict:
        params: dict = {}
        while self.peek() == ";":
            self.i += 1
            self._skip_sp()
            key = self.parse_key()
            if self.peek() == "=":
                self.i += 1
                value = self.parse_bare_item()
            else:
                value = True
            params[key] = value
        return params

    def parse_inner_list(self) -> tuple[list, dict]:
        if self.peek() != "(":
            raise SignatureError("expected inner list")
        self.i += 1
        items = []
        while True:
            self._skip_sp()
            if self.peek() == ")":
                self.i += 1
                break
            if self.eof():
                raise SignatureError("unterminated inner list")
            item = self.parse_bare_item()
            item_params = self.parse_parameters()
            items.append((item, item_params))
            if self.peek() not in (" ", ")"):
                raise SignatureError("bad inner-list separator")
        list_params = self.parse_parameters()
        return items, list_params


@dataclass(frozen=True)
class _Token:
    value: str


@dataclass
class _SignatureInputMember:
    label: str
    components: list  # list[(name:str, params:dict)]
    params: dict
    raw_value: str  # verbatim, for the @signature-params base line


def _split_dictionary_members(text: str) -> list[tuple[str, str]]:
    """
    Split a structured Dictionary into (label, raw_value) pairs WITHOUT
    interpreting the values, so we can keep each value verbatim for the
    @signature-params line. Commas inside strings/byte-sequences/inner-lists
    are respected.
    """
    members: list[tuple[str, str]] = []
    i, n = 0, len(text)
    while i < n:
        while i < n and text[i] in " \t":
            i += 1
        # key
        start = i
        while i < n and (text[i].islower() or text[i].isdigit() or text[i] in "_-.*"):
            i += 1
        if i == start:
            raise SignatureError("expected dictionary key")
        label = text[start:i]
        if i < n and text[i] == "=":
            i += 1
            v_start = i
            depth = 0
            in_str = False
            in_bytes = False
            while i < n:
                c = text[i]
                if in_str:
                    if c == "\\":
                        i += 2
                        continue
                    if c == '"':
                        in_str = False
                elif in_bytes:
                    if c == ":":
                        in_bytes = False
                elif c == '"':
                    in_str = True
                elif c == ":":
                    in_bytes = True
                elif c == "(":
                    depth += 1
                elif c == ")":
                    depth -= 1
                elif c == "," and depth == 0:
                    break
                i += 1
            raw_value = text[v_start:i].strip()
        else:
            raw_value = ""  # bare-key member (boolean true); unused here
        members.append((label, raw_value))
        while i < n and text[i] in " \t":
            i += 1
        if i < n and text[i] == ",":
            i += 1
    return members


def parse_signature_input(header: str) -> dict[str, _SignatureInputMember]:
    out: dict[str, _SignatureInputMember] = {}
    for label, raw in _split_dictionary_members(header):
        if not raw:
            continue
        p = _Parser(raw)
        items, params = p.parse_inner_list()
        p._skip_ows()
        if not p.eof():
            raise SignatureError("trailing data in signature-input member")
        components = []
        for item, item_params in items:
            if not isinstance(item, str):
                raise SignatureError("covered component must be a string")
            components.append((item, item_params))
        # Coerce token-valued params (alg, tag come as tokens or strings).
        clean_params = {k: (v.value if isinstance(v, _Token) else v) for k, v in params.items()}
        out[label] = _SignatureInputMember(label, components, clean_params, raw)
    return out


def parse_signature(header: str) -> dict[str, bytes]:
    out: dict[str, bytes] = {}
    for label, raw in _split_dictionary_members(header):
        if not raw:
            continue
        p = _Parser(raw)
        value = p.parse_bare_item()
        p.parse_parameters()  # discard any member params
        p._skip_ows()
        if not p.eof():
            raise SignatureError("trailing data in signature member")
        if not isinstance(value, (bytes, bytearray)):
            raise SignatureError("signature value must be a byte sequence")
        out[label] = bytes(value)
    return out


# --------------------------------------------------------------------------- #
# Request adapter + signature base construction (RFC 9421 §2).
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class SignatureRequest:
    method: str
    scheme: str
    authority: str  # host[:port], lowercased
    path: str
    query: str  # without a leading '?'
    headers: Mapping[str, str] = field(default_factory=dict)  # lowercased name -> value

    @classmethod
    def from_django(cls, request) -> SignatureRequest:
        host = request.get_host().lower()
        headers = {k.lower(): v for k, v in request.headers.items()}
        return cls(
            method=request.method.upper(),
            scheme=request.scheme.lower(),
            authority=host,
            path=request.path,
            query=request.META.get("QUERY_STRING", ""),
            headers=headers,
        )

    def target_uri(self) -> str:
        uri = f"{self.scheme}://{self.authority}{self.path}"
        if self.query:
            uri += f"?{self.query}"
        return uri


def _serialize_component_id(name: str, params: dict) -> str:
    """Serialize a covered-component identifier as it appears in the base line."""
    out = f'"{name}"'
    for k, v in params.items():
        if v is True:
            out += f";{k}"
        elif isinstance(v, str):
            out += f';{k}="{v}"'
        else:
            out += f";{k}={v}"
    return out


def _derived_value(name: str, req: SignatureRequest) -> str:
    if name == "@method":
        return req.method
    if name == "@authority":
        return req.authority
    if name == "@path":
        return req.path
    if name == "@scheme":
        return req.scheme
    if name == "@query":
        # RFC 9421 §2.2.7: leading '?', and just '?' when there is no query.
        return f"?{req.query}" if req.query else "?"
    if name == "@target-uri":
        return req.target_uri()
    raise SignatureError(f"unsupported derived component: {name}")


def build_signature_base(member: _SignatureInputMember, req: SignatureRequest) -> bytes:
    lines: list[str] = []
    for name, params in member.components:
        if params:
            # We support only bare component identifiers; any parameter
            # (@query-param name=, header ;sf/;bs/;key/;req) is refused.
            raise SignatureError(f"unsupported component parameters on {name!r}")
        lname = name.lower()
        if name.startswith("@"):
            value = _derived_value(lname, req)
        else:
            if lname not in req.headers:
                raise SignatureError(f"covered header not present: {lname}")
            value = req.headers[lname].strip()
        lines.append(f"{_serialize_component_id(lname, {})}: {value}")
    lines.append(f'"@signature-params": {member.raw_value}')
    return "\n".join(lines).encode("ascii")


# --------------------------------------------------------------------------- #
# Key loading + signature verification.
# --------------------------------------------------------------------------- #


def _load_public_key(jwk: Mapping):
    kty = jwk.get("kty")
    if kty == "OKP" and jwk.get("crv") == "Ed25519":
        return ed25519.Ed25519PublicKey.from_public_bytes(_b64url_decode(jwk["x"]))
    if kty == "EC" and jwk.get("crv") == "P-256":
        x = int.from_bytes(_b64url_decode(jwk["x"]), "big")
        y = int.from_bytes(_b64url_decode(jwk["y"]), "big")
        return ec.EllipticCurvePublicNumbers(x, y, ec.SECP256R1()).public_key()
    raise SignatureError(f"unsupported JWK: kty={kty!r} crv={jwk.get('crv')!r}")


def _raw_verify(public_key, alg: str, signature: bytes, base: bytes) -> bool:
    try:
        if alg == ALG_ED25519:
            public_key.verify(signature, base)
            return True
        if alg == ALG_ES256:
            if len(signature) != 64:
                return False  # JWS raw r||s is exactly 64 bytes for P-256
            r = int.from_bytes(signature[:32], "big")
            s = int.from_bytes(signature[32:], "big")
            der = encode_dss_signature(r, s)
            public_key.verify(der, base, ec.ECDSA(hashes.SHA256()))
            return True
    except InvalidSignature:
        return False
    raise SignatureError(f"unsupported algorithm: {alg}")


def _key_algorithm(jwk: Mapping) -> str:
    if jwk.get("kty") == "OKP":
        return ALG_ED25519
    if jwk.get("kty") == "EC":
        return ALG_ES256
    raise SignatureError("cannot derive algorithm from key")


def verify(
    req: SignatureRequest,
    *,
    public_jwk: Mapping,
    label: str | None = None,
    required_components: tuple[str, ...] = ("@method", "@authority", "@path"),
    max_age: int = DEFAULT_MAX_AGE,
    max_skew: int = DEFAULT_MAX_SKEW,
    now: int | None = None,
    expected_keyid: str | None = None,
    require_created: bool = True,
) -> VerificationResult:
    """
    Verify the RFC 9421 signature on ``req`` against ``public_jwk``.

    Returns a VerificationResult; never raises for an untrusted input (a
    malformed header is ``ok=False``, not an exception). ``required_components``
    are the covered components that MUST be present — the defaults bind the
    signature to this exact request line, so a captured signature can't be
    replayed against a different method/host/path.

    ``require_created`` (default True) rejects any signature that omits the
    ``created`` parameter: without it there is no age to check, so an otherwise
    valid captured signature would be replayable indefinitely regardless of
    ``max_age``. Freshness is a necessary — not sufficient — replay defence; a
    nonce/seen-signature cache belongs in the auth layer on top of this.
    """
    try:
        sig_input_hdr = req.headers.get("signature-input")
        sig_hdr = req.headers.get("signature")
        if not sig_input_hdr or not sig_hdr:
            return VerificationResult(False, "missing Signature/Signature-Input")

        inputs = parse_signature_input(sig_input_hdr)
        sigs = parse_signature(sig_hdr)
        if not inputs:
            return VerificationResult(False, "empty Signature-Input")

        if label is None:
            if len(inputs) != 1:
                return VerificationResult(False, "ambiguous signature label")
            label = next(iter(inputs))
        if label not in inputs or label not in sigs:
            return VerificationResult(False, f"no signature for label {label!r}")

        member = inputs[label]
        params = member.params
        covered = tuple(name.lower() for name, _ in member.components)

        missing = [c for c in required_components if c not in covered]
        if missing:
            return VerificationResult(False, f"missing required covered components: {missing}")

        keyid = str(params.get("keyid", ""))
        if expected_keyid is not None and keyid != expected_keyid:
            return VerificationResult(False, "keyid mismatch")

        # Algorithm: honour an explicit alg param if present, else derive from
        # the key. A stated alg that disagrees with the key is a hard refusal.
        key_alg = _key_algorithm(public_jwk)
        stated_alg = params.get("alg")
        if stated_alg is not None and str(stated_alg) != key_alg:
            return VerificationResult(False, "alg does not match key")
        alg = key_alg

        now = int(datetime.now(UTC).timestamp()) if now is None else now
        created = params.get("created")
        if created is None:
            if require_created:
                # No timestamp ⇒ no freshness ⇒ replayable forever. Refuse.
                return VerificationResult(False, "missing created")
        else:
            created = int(created)
            if created - now > max_skew:
                return VerificationResult(False, "created is in the future")
            if max_age is not None and now - created > max_age:
                return VerificationResult(False, "signature is stale")
        expires = params.get("expires")
        if expires is not None and now > int(expires):
            return VerificationResult(False, "signature expired")

        base = build_signature_base(member, req)
        public_key = _load_public_key(public_jwk)
        if not _raw_verify(public_key, alg, sigs[label], base):
            return VerificationResult(False, "bad signature")

        return VerificationResult(
            True,
            "",
            keyid=keyid,
            alg=alg,
            covered=covered,
            created=created,
            tag=str(params.get("tag", "")),
        )
    except SignatureError as exc:
        return VerificationResult(False, f"malformed signature: {exc}")
    except Exception as exc:  # never leak an unexpected error as an accept
        return VerificationResult(False, f"verification error: {exc}")
