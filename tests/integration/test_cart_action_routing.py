"""
P1.0 guard: every ``@action`` on the cart/checkout viewsets must be reachable.

``CartViewSet`` and ``CheckoutViewSet`` are **not** router-registered.
``cart/urls.py`` wires each action by hand with
``path(..., CartViewSet.as_view({"post": "apply_voucher"}))``. That means a
``@action`` decorator on those classes routes **nothing on its own** — it is
inert unless somebody also adds a matching ``path()``.

That is exactly how the gift-card 404 happened: ``@action(url_path=
"apply-gift-card")`` was added at ``cart/views.py:371`` and ``:406``, no
``path()`` was added alongside, and the published headless SDK's
``spwig.cart.applyGiftCard()`` has been 404ing ever since with nothing in the
suite to notice.

This module is the general-purpose guard against that class of defect
recurring. It introspects the decorated actions off the classes themselves —
so a *newly added* unrouted action fails here automatically, without anyone
remembering to write a test for it.

Resolution strategy: these routes are hand-wired and mostly carry names that
do not follow the router's ``{basename}-{url_name}`` convention, so
``reverse()`` by name is not a reliable oracle. We resolve the concrete URL
path instead (``django.urls.resolve``) and then assert the resolved view is
genuinely bound to the expected viewset *and* dispatches the expected handler
for the expected HTTP methods. Resolving to *some* view is not enough.

Plan: docs/.claude_code/plans/wondrous-moseying-wolf.md (P1.0)
The two currently-dead gift card actions are routed in phase **P2.2**.
"""

import re

import pytest
from django.urls import Resolver404, resolve

from cart.views import CartViewSet, CheckoutViewSet

pytestmark = [
    pytest.mark.integration,
    pytest.mark.url_routing,
]


# Where each viewset's hand-wired actions are mounted.
# ``core/urls.py:165`` mounts ``cart.urls`` under ``api/`` (outside
# ``i18n_patterns`` — APIs never carry a language prefix).
VIEWSET_PREFIXES = {
    CartViewSet: "/api/cart/",
    CheckoutViewSet: "/api/checkout/",
}

# Actions known to be unroutable today, as (viewset, action). Empty: the two
# former entries were CartViewSet.apply_gift_card / .remove_gift_card, which
# never had path() entries and 404'd since inception. P2.2f deleted both — gift
# cards are tendered at checkout now. Every @action is expected to be reachable.
KNOWN_UNROUTED: set[tuple[str, str]] = set()

# Matches a DRF named regex group inside an ``url_path``,
# e.g. ``items/(?P<item_id>[^/.]+)``.
_NAMED_GROUP = re.compile(r"\(\?P<\w+>[^)]*\)")


# Literals tried in place of a captured parameter. The URLconf may use a path
# converter that only accepts a particular shape — `<uuid:tender_id>` will not
# match "1" — so an action is considered reachable if ANY of these resolves.
# A genuinely unrouted action resolves for none of them, which is what this
# guard is actually asserting.
_PARAM_LITERALS = ("1", "8cb0434e-0000-4000-8000-000000000000")


def _concrete_paths(viewset, action):
    """
    Build candidate resolvable URL paths for a decorated action.

    ``url_path`` may embed regex capture groups. Each is substituted with every
    literal in ``_PARAM_LITERALS``, yielding one candidate path per literal.
    """
    prefix = VIEWSET_PREFIXES[viewset]
    if not _NAMED_GROUP.search(action.url_path):
        return [f"{prefix}{action.url_path}/"]
    return [f"{prefix}{_NAMED_GROUP.sub(literal, action.url_path)}/" for literal in _PARAM_LITERALS]


def _action_params():
    """Yield one pytest param per decorated action across both viewsets."""
    for viewset in (CartViewSet, CheckoutViewSet):
        for action in viewset.get_extra_actions():
            key = (viewset.__name__, action.__name__)
            marks = []
            if key in KNOWN_UNROUTED:
                marks.append(
                    pytest.mark.xfail(
                        strict=True,
                        reason=(
                            f"{key[0]}.{key[1]} has an @action decorator but no matching "
                            "path() in cart/urls.py, so it 404s. The published headless SDK "
                            "calls it. Routed in plan phase P2.2."
                        ),
                    )
                )
            yield pytest.param(
                viewset, action, id=f"{viewset.__name__}.{action.__name__}", marks=marks
            )


def _unreachable_reason(viewset, action):
    """
    Return ``None`` if the action is genuinely reachable, else a human-readable
    explanation of why it is not.
    """
    candidates = _concrete_paths(viewset, action)

    match = None
    path = candidates[0]
    for candidate in candidates:
        try:
            match = resolve(candidate)
            path = candidate
            break
        except Resolver404:
            continue

    if match is None:
        tried = ", ".join(candidates)
        return (
            f"{viewset.__name__}.{action.__name__} is decorated with "
            f"@action(url_path={action.url_path!r}) but none of [{tried}] resolves to "
            f"any URL pattern. {viewset.__name__} is not router-registered, so the "
            f"decorator alone routes nothing — add a path() for it in cart/urls.py."
        )

    resolved_cls = getattr(match.func, "cls", None)
    if resolved_cls is not viewset:
        return (
            f"{path} resolves to {resolved_cls!r}, not {viewset.__name__} — "
            f"{viewset.__name__}.{action.__name__} is shadowed by another route."
        )

    # ``ViewSetMixin.as_view`` stores the {http_method: handler_name} mapping.
    routed_actions = getattr(match.func, "actions", None) or {}

    missing = {
        http_method
        for http_method in action.mapping
        if routed_actions.get(http_method) != action.__name__
    }
    if missing:
        return (
            f"{path} resolves to {viewset.__name__}, but the HTTP method(s) "
            f"{sorted(missing)} are not wired to {action.__name__}: the route's mapping "
            f"is {routed_actions!r} while the @action declares {dict(action.mapping)!r}."
        )

    return None


@pytest.mark.parametrize(("viewset", "action"), list(_action_params()))
def test_decorated_action_is_reachable(viewset, action):
    """
    Every ``@action`` on the cart/checkout viewsets must resolve to a real URL
    that dispatches to that action for its declared HTTP methods.
    """
    reason = _unreachable_reason(viewset, action)
    assert reason is None, reason


def test_no_new_unrouted_actions_have_appeared():
    """
    Aggregate recurrence guard.

    The set of unreachable actions must be *exactly* the known-broken set.
    This passes today and fails the moment somebody adds an ``@action`` to
    either viewset without a matching ``path()`` — the failure names the
    offending action rather than surfacing as a mystery 404 in a client.

    It also fails if a known-broken action is fixed without ``KNOWN_UNROUTED``
    being updated, keeping this module honest in both directions.
    """
    unreachable = {
        f"{viewset.__name__}.{action.__name__}"
        for viewset in (CartViewSet, CheckoutViewSet)
        for action in viewset.get_extra_actions()
        if _unreachable_reason(viewset, action) is not None
    }
    expected = {f"{cls}.{name}" for cls, name in KNOWN_UNROUTED}

    newly_broken = unreachable - expected
    newly_fixed = expected - unreachable

    assert not newly_broken, (
        "New unrouted @action(s) on CartViewSet/CheckoutViewSet: "
        f"{sorted(newly_broken)}. These viewsets are hand-wired in cart/urls.py — "
        "add a matching path() entry, or the endpoint 404s silently."
    )
    assert not newly_fixed, (
        f"{sorted(newly_fixed)} now route correctly. Remove them from "
        "KNOWN_UNROUTED (and drop the corresponding xfail) so the guard keeps "
        "protecting them."
    )


def test_voucher_actions_are_reachable_as_a_control():
    """
    Control for the guard itself.

    The voucher actions sit right next to the gift card ones in
    ``cart/views.py`` and differ only in having ``path()`` entries. If this
    ever fails, the guard's resolution logic is broken rather than the
    application — without this control, a bug in ``_unreachable_reason``
    would make every action look reachable and the whole module would pass
    vacuously.
    """
    for name in ("apply_voucher", "remove_voucher"):
        action = getattr(CartViewSet, name)
        assert _unreachable_reason(CartViewSet, action) is None, (
            f"CartViewSet.{name} should be routed via cart/urls.py"
        )
