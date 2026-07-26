"""
JSON Canonicalization Scheme (RFC 8785), for the subset AP2 mandates use.

A mandate is signed over a byte-exact serialization of its claims, so issuer and
verifier MUST agree on those bytes to the last character. RFC 8785 fixes that:
object keys sorted by their UTF-16 code units, no insignificant whitespace, and
a canonical form for every primitive.

Deliberately restricted: this canonicalizer accepts only ``dict``, ``list``,
``str``, ``bool``, ``int`` and ``None`` — and **rejects floats**. Money in this
codebase is always integer minor units, and RFC 8785's number canonicalization
(ECMAScript ``Number.prototype.toString``) is the one genuinely fiddly corner of
the spec. Refusing floats outright means we never depend on it, and a stray
float becomes a loud error instead of a silent cross-implementation mismatch.

For this subset, Python's ``json.dumps(sort_keys=True, separators=(",", ":"),
ensure_ascii=False)`` already emits RFC 8785 output: our keys are ASCII (so
code-point sort == UTF-16 sort), integers serialize identically, and string
escaping matches. The float guard is what keeps that equivalence honest.
"""

from __future__ import annotations

import json


def _reject_floats(obj):
    """Walk the structure and raise on any float (or unsupported type)."""
    if obj is None or isinstance(obj, (str, bool)):
        return
    if isinstance(obj, float):
        raise TypeError("JCS canonicalization refuses floats; use integer minor units")
    if isinstance(obj, int):
        return
    if isinstance(obj, dict):
        for k, v in obj.items():
            if not isinstance(k, str):
                raise TypeError("JCS object keys must be strings")
            _reject_floats(v)
        return
    if isinstance(obj, (list, tuple)):
        for v in obj:
            _reject_floats(v)
        return
    raise TypeError(f"JCS: unsupported type {type(obj).__name__}")


def _scalar(obj) -> str:
    # str / bool / int / None. json.dumps(ensure_ascii=False) already matches
    # RFC 8785 escaping for these (floats are rejected before we get here).
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def _canon(obj) -> str:
    if isinstance(obj, dict):
        # RFC 8785: object members are sorted by the UTF-16 code units of the
        # key, NOT by Unicode code point (the two differ for supplementary
        # characters). json.dumps(sort_keys=True) uses code-point order, so we
        # sort explicitly to stay byte-identical to a conforming implementation.
        items = sorted(obj.items(), key=lambda kv: kv[0].encode("utf-16-be"))
        return "{" + ",".join(f"{_scalar(k)}:{_canon(v)}" for k, v in items) + "}"
    if isinstance(obj, (list, tuple)):
        return "[" + ",".join(_canon(v) for v in obj) + "]"
    return _scalar(obj)


def canonicalize(obj) -> bytes:
    """Return the RFC 8785 canonical UTF-8 bytes of ``obj`` (float-free subset)."""
    _reject_floats(obj)
    return _canon(obj).encode("utf-8")
