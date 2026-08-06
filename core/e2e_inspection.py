"""Read-only transaction-footprint inspection endpoint for the E2E cert tier.

`/api/e2e/inspect/order/<order_number>/` returns the same
:class:`commerce_footprint.footprint.Footprint` an in-process test reads from
the ORM, serialised to JSON, so the standalone ``spwig-e2e`` certification suite
can assert the *identical* financial footprint against a deployed host over
HTTP (its ``HttpBackend`` consumes this).

Safety posture — this must never become an information-leak surface on a real
merchant install:

- **Off by default.** ``settings.SPWIG_E2E_INSPECTION`` is ``False`` unless a
  deployment explicitly opts in; ``tests`` assert the default config 404s.
- **Fail closed.** When disabled — or the shared-secret header is missing or
  wrong — the view raises 404 (not 403): a disabled endpoint is indistinguish-
  able from a non-existent one, so its presence isn't confirmable.
- **Shared secret even when on.** ``settings.SPWIG_E2E_INSPECTION_TOKEN`` must
  match the ``X-E2E-Inspection-Token`` header (constant-time compare). Settings
  refuses to boot with inspection on but no token set.
- **Read-only.** GET only; it returns commercial facts the server already holds
  for one order and mutates nothing.

The payload is deliberately **secret-bearing**: the footprint includes full
gift-card and voucher codes (bearer instruments redeemable at checkout),
customer emails, line-item history, and payment-provider transaction ids — the
assertions need identity/equality, so the raw values are carried, not masked.
That makes an *isolated certification sandbox* the only acceptable place to
enable it: never a real merchant install. The flag default, the mandatory
shared secret, and the boot guard together enforce that.
"""

from __future__ import annotations

import hmac

from django.conf import settings
from django.http import Http404, HttpResponseNotAllowed, JsonResponse
from django.views.decorators.csrf import csrf_exempt


def _inspection_enabled() -> bool:
    return bool(getattr(settings, "SPWIG_E2E_INSPECTION", False))


def _authorised(request) -> bool:
    """True only when inspection is on AND the request carries the shared secret.

    A missing/empty configured token can never authorise (fail closed), so the
    endpoint cannot be reached tokenless even if the settings guard is bypassed.
    """
    if not _inspection_enabled():
        return False
    token = getattr(settings, "SPWIG_E2E_INSPECTION_TOKEN", "") or ""
    provided = request.headers.get("X-E2E-Inspection-Token", "") or ""
    if not token:
        return False
    # Compare as bytes: header values are latin-1 decoded, so a non-ASCII byte
    # would make ``hmac.compare_digest`` raise TypeError on *str* operands → an
    # unhandled 500 that (on an enabled host) distinguishes this route from an
    # absent one. Encoding both sides sidesteps that; the guard is belt-and-
    # braces so any odd input still fails closed rather than 500ing.
    try:
        return hmac.compare_digest(provided.encode("utf-8"), token.encode("utf-8"))
    except (AttributeError, TypeError):
        return False


@csrf_exempt  # read-only GET view; exempt so unsafe verbs reach the uniform-404
def inspect_order(request, order_number: str):
    """Return the transaction Footprint for ``order_number`` as JSON.

    404s when inspection is disabled, the secret is missing/wrong, or no such
    order exists — all indistinguishable from the outside. Authorisation is
    checked *before* the HTTP method so a disabled endpoint 404s for every verb
    (including POST/OPTIONS) rather than leaking its existence via a 405. The
    ``@csrf_exempt`` matters here too: without it ``CsrfViewMiddleware`` would
    answer an unsafe verb with 403 *before* the view runs, and that 403 (vs a
    plain 404) would itself confirm the route exists.
    """
    if not _authorised(request):
        raise Http404
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    # Imported lazily so a disabled endpoint pulls in no ORM/gathering code, and
    # so this module stays importable during URL setup regardless of app-load
    # ordering.
    from commerce_footprint.orm_backend import footprint_for_order
    from orders.models import Order

    try:
        footprint = footprint_for_order(order_number)
    except Order.DoesNotExist as exc:
        raise Http404 from exc

    return JsonResponse(footprint.to_dict())
