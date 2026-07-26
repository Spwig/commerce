"""
Agentic UCP checkout-session service (build/price/map, pre-payment).

These exercise the translator: a UCP checkout id maps to an anonymous cart, the
store's own CheckoutService does the pricing/validation, and the result projects
into UCP shape. No money moves here — completion is tested end-to-end in the
Test Gateway integration test.
"""

import pytest

from agentic.models import AgentIdentity
from agentic.services import checkout_service as acs
from tests.factories import ProductFactory

pytestmark = [pytest.mark.django_db, pytest.mark.integration]


def _agent(kid="kid-1"):
    return AgentIdentity.objects.create(
        directory="agent.example.com",
        key_thumbprint=kid,
        algorithm="ed25519",
        public_jwk={"kty": "OKP", "crv": "Ed25519", "x": "x"},
    )


def _product(**kw):
    kw.setdefault("status", "published")
    kw.setdefault("price", "25.00")
    return ProductFactory(**kw)


class TestCreate:
    def test_creates_session_stamped_to_agent(self, site_settings):
        agent = _agent()
        p = _product(name="Gadget")
        cid = acs.create_checkout_session(agent=agent, line_items=[{"product_id": p.id}])

        session = acs.load_session(cid, agent)
        assert session is not None
        assert session.metadata["channel"] == "agent"
        assert session.metadata["ucp_checkout_id"] == cid
        assert session.metadata["agent_identity_id"] == str(agent.id)

    def test_line_items_and_totals_projected(self, site_settings):
        agent = _agent()
        p = _product(name="Gadget", price="25.00")
        cid = acs.create_checkout_session(
            agent=agent, line_items=[{"product_id": p.id, "quantity": 2}]
        )
        session = acs.load_session(cid, agent)
        body = acs.build_ucp_checkout_session(session, cid)

        assert body["id"] == cid
        assert len(body["line_items"]) == 1
        li = body["line_items"][0]
        assert li["product_id"] == str(p.id)
        assert li["quantity"] == 2
        # Minor units: $50.00 subtotal.
        assert body["totals"]["subtotal"]["amount"] == 5000
        assert body["totals"]["subtotal"]["currency"]
        # amount_due present and never negative.
        assert body["totals"]["amount_due"]["amount"] >= 0

    def test_empty_line_items_rejected(self, site_settings):
        with pytest.raises(acs.CheckoutError) as exc:
            acs.create_checkout_session(agent=_agent(), line_items=[])
        assert exc.value.code == "empty_cart"

    def test_unknown_product_rejected(self, site_settings):
        with pytest.raises(acs.CheckoutError) as exc:
            acs.create_checkout_session(agent=_agent(), line_items=[{"product_id": 999999}])
        assert exc.value.code == "unknown_product"
        assert exc.value.http_status == 404

    def test_hidden_product_is_invisible(self, site_settings):
        agent = _agent()
        hidden = _product(name="Hidden", agent_visible=False)
        with pytest.raises(acs.CheckoutError) as exc:
            acs.create_checkout_session(agent=agent, line_items=[{"product_id": hidden.id}])
        # Not "forbidden" — it simply doesn't exist to an agent.
        assert exc.value.code == "unknown_product"

    def test_invalid_quantity_rejected(self, site_settings):
        agent = _agent()
        p = _product()
        with pytest.raises(acs.CheckoutError) as exc:
            acs.create_checkout_session(
                agent=agent, line_items=[{"product_id": p.id, "quantity": 0}]
            )
        assert exc.value.code == "invalid_quantity"

    def test_inactive_variant_rejected(self, site_settings):
        # A visible product can have a disabled variant the catalog never
        # advertises; an agent must not be able to order it (security review).
        from catalog.models import ProductVariant

        agent = _agent()
        p = _product(name="Has Variants")
        hidden_variant = ProductVariant.objects.create(product=p, sku="HIDDEN-1", is_active=False)
        with pytest.raises(acs.CheckoutError) as exc:
            acs.create_checkout_session(
                agent=agent,
                line_items=[{"product_id": p.id, "variant_id": hidden_variant.id}],
            )
        assert exc.value.code == "unknown_variant"

    def test_non_list_line_items_rejected(self, site_settings):
        with pytest.raises(acs.CheckoutError) as exc:
            acs.create_checkout_session(agent=_agent(), line_items={"product_id": 1})
        assert exc.value.code == "empty_cart"


class TestOwnership:
    def test_other_agent_cannot_load(self, site_settings):
        owner = _agent(kid="owner")
        other = _agent(kid="other")
        p = _product()
        cid = acs.create_checkout_session(agent=owner, line_items=[{"product_id": p.id}])

        assert acs.load_session(cid, owner) is not None
        # A different identity sees nothing (not a 403 that would confirm it).
        assert acs.load_session(cid, other) is None

    def test_update_rejects_unknown_session(self, site_settings):
        with pytest.raises(acs.CheckoutError) as exc:
            acs.update_checkout_session("does-not-exist", _agent(), buyer={"email": "a@b.c"})
        assert exc.value.http_status == 404

    def test_owned_session_invisible_to_anonymous_caller(self, site_settings):
        # A session created by a verified agent must NOT be reachable by an
        # anonymous caller (agent=None), even under allow_unverified_checkout —
        # otherwise the checkout id becomes an unscoped bearer token.
        owner = _agent(kid="owner-2")
        p = _product()
        cid = acs.create_checkout_session(agent=owner, line_items=[{"product_id": p.id}])
        assert acs.load_session(cid, None) is None
        assert acs.load_session(cid, owner) is not None


class TestStatusMapping:
    def test_new_session_is_not_ready_without_buyer(self, site_settings):
        agent = _agent()
        p = _product()
        cid = acs.create_checkout_session(agent=agent, line_items=[{"product_id": p.id}])
        session = acs.load_session(cid, agent)
        body = acs.build_ucp_checkout_session(session, cid)
        # No address / provider yet → not ready, with actionable messages.
        assert body["status"] == acs.STATUS_NOT_READY
        assert isinstance(body["messages"], list)
        assert body["payment"]["status"] == "requires_payment"
