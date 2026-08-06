"""
Tier-2: every checkout template renders, and the express fallback rule holds.

The merchant picks one of four checkout templates (accordion, multi_step,
single_page, express) via ``PageTemplateConfig``; ``?template=`` overrides it.
A broken template is invisible to a suite that only ever drives the default —
this parametrised matrix renders each one against a real cart through the real
``checkout_view`` and asserts the right template file was used.

It also pins the express-fallback rule: express is a returning-customer flow,
so a shipping cart with no saved address must fall back (to accordion) rather
than render an unusable express shell (page_builder/views.py:689).
"""

from decimal import Decimal

import pytest
from django.urls import reverse

from tests.factories import (
    AddressFactory,
    CartFactory,
    CartItemFactory,
    ProductFactory,
    UserFactory,
)

pytestmark = [pytest.mark.django_db, pytest.mark.checkout, pytest.mark.tier2]

CHECKOUT_TEMPLATE_PATHS = {
    "accordion": "page_builder/checkout/accordion.html",
    "multi_step": "page_builder/checkout/multi_step.html",
    "single_page": "page_builder/checkout/single_page.html",
    "express": "page_builder/checkout/express.html",
}


def _login_with_cart(client, *, digital, saved_address=False):
    """Log a fresh customer in with a one-item cart. Digital carts don't require
    shipping (so express never falls back); simple products do."""
    customer = UserFactory()
    cart = CartFactory(user=customer)
    product = (
        ProductFactory(digital=True, price=Decimal("9.99"))
        if digital
        else ProductFactory(price=Decimal("20.00"))
    )
    CartItemFactory(cart=cart, product=product, quantity=1)
    if saved_address:
        AddressFactory(user=customer, default_address=True)
    client.force_login(customer)
    return customer


_TOP_LEVEL = set(CHECKOUT_TEMPLATE_PATHS.values())


def _rendered(resp):
    return [t.name for t in resp.templates if t.name]


def _rendered_variant(resp):
    """The single top-level checkout variant that rendered. Intersecting with
    the known variant set means a partial-include of a sibling can't produce a
    false match — exactly one main template must be present."""
    return set(_rendered(resp)) & _TOP_LEVEL


@pytest.mark.parametrize("template_key,expected_path", list(CHECKOUT_TEMPLATE_PATHS.items()))
def test_each_checkout_template_renders(
    template_key, expected_path, client, django_site, site_settings
):
    # Digital cart: no shipping, so express renders as express (no fallback).
    _login_with_cart(client, digital=True)
    resp = client.get(reverse("page_builder:checkout") + f"?template={template_key}")
    assert resp.status_code == 200
    assert _rendered_variant(resp) == {expected_path}, (
        f"template {template_key!r} did not render exactly {expected_path!r}: {_rendered(resp)}"
    )


def test_express_falls_back_for_shipping_cart_without_saved_address(
    client, django_site, site_settings
):
    """A physical cart + no saved address on express → fall back to accordion,
    not the unusable express shell."""
    _login_with_cart(client, digital=False)
    resp = client.get(reverse("page_builder:checkout") + "?template=express")
    assert resp.status_code == 200
    assert _rendered_variant(resp) == {
        CHECKOUT_TEMPLATE_PATHS["accordion"]
    }  # fell back, not express


def test_express_renders_for_shipping_cart_with_saved_address(client, django_site, site_settings):
    """Guard-the-guard for the fallback: the SAME physical cart WITH a saved
    default address renders express (proves the fallback above is the
    no-address branch, not express being broken for shipping carts)."""
    _login_with_cart(client, digital=False, saved_address=True)
    resp = client.get(reverse("page_builder:checkout") + "?template=express")
    assert resp.status_code == 200
    assert _rendered_variant(resp) == {CHECKOUT_TEMPLATE_PATHS["express"]}
