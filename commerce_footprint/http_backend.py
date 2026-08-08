"""HTTP backend for the footprint oracle — Django-free, standard library only.

The standalone ``spwig-e2e`` certification suite cannot import Django models
against a remote host, so it reads the *same* :class:`Footprint` shape over HTTP
from the read-only ``/api/e2e/inspect/`` endpoint and rebuilds the **identical**
dataclass via :meth:`Footprint.from_dict`. The lifecycle assertions in
``footprint.py`` then run unchanged against either backend — this is what makes
"same tests, two targets" real.

Only ``urllib`` is used so this module (with ``footprint.py``) can be vendored
into the standalone repo without pulling in ``requests`` or Django.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from urllib.parse import quote

from commerce_footprint.footprint import Footprint

_INSPECT_PATH = "/api/e2e/inspect/order/{order_number}/"


class InspectionError(RuntimeError):
    """A footprint could not be fetched from the inspection endpoint.

    Distinct from an assertion failure: this means the *transport* failed (host
    down, wrong secret → 404, order not found → 404), not that a commercial
    invariant was violated. The caller decides whether that's fatal.
    """


class HttpBackend:
    """Reads footprints from a deployed host's inspection endpoint.

    ``footprint_for_order`` mirrors the ORM backend's callable of the same name,
    so a test can swap backends without changing how it asks for a footprint.
    """

    def __init__(self, base_url: str, token: str, *, timeout: float = 10.0):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.timeout = timeout

    def footprint_for_order(self, order_number: str) -> Footprint:
        url = self.base_url + _INSPECT_PATH.format(order_number=quote(str(order_number), safe=""))
        request = urllib.request.Request(
            url,
            method="GET",
            headers={"X-E2E-Inspection-Token": self.token, "Accept": "application/json"},
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                body = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            # 404 covers all fail-closed cases (disabled / bad secret / no such
            # order) — indistinguishable by design, so don't over-interpret it.
            raise InspectionError(f"inspection GET {url} returned HTTP {exc.code}") from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            # A connect-timeout arrives wrapped in URLError, but a timeout during
            # response.read() (inside the `with`) raises a bare TimeoutError that
            # would otherwise crash the caller instead of surfacing as a clean
            # transport error. Catch both.
            reason = getattr(exc, "reason", exc)
            raise InspectionError(f"inspection GET {url} failed: {reason}") from exc

        try:
            payload = json.loads(body)
        except json.JSONDecodeError as exc:
            raise InspectionError(f"inspection GET {url} returned non-JSON body") from exc

        try:
            return Footprint.from_dict(payload)
        except (KeyError, TypeError, ValueError) as exc:
            # A truncated/partial payload (a missing top-level collection, a
            # malformed record) is a contract breach — surface it as a transport
            # error, never a silently-empty footprint that passes assertions.
            raise InspectionError(
                f"inspection GET {url} returned a payload that isn't a valid footprint"
            ) from exc
