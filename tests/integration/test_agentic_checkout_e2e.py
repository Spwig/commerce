"""
End-to-end agentic UCP checkout: create -> update -> complete -> paid order.

Drives the agentic checkout SERVICE and the REST BINDING through the store's
real checkout + payment orchestration, with the payment provider stubbed (the
same pattern the payment-orchestration tests use — no live gateway, no network).
Proves the agent path reaches a `paid` Order stamped `channel="agent"`, reusing
the shared machinery rather than a parallel engine.

CI-flake note (fixed 2026-07-26): the payment provider is stubbed for the WHOLE
module via an autouse fixture, not just around the `complete` call. Provider
auto-selection runs inside `update_checkout_session` too, and it walks
`PaymentMethodFilter._supports_currency`, which loads a provider instance inside
a `try/except Exception: return False`. Left unmocked there, a transient
provider-load hiccup on the slow CI runner made `get_available_payment_providers`
return empty, so no provider was selected and the session stayed
`not_ready_for_payment` — cascading into every failure seen in Gitea CI run 312.
Stubbing the instance everywhere (and giving it `get_supported_currencies`) makes
selection deterministic and load-independent.
"""

from unittest import mock

import pytest

from agentic.models import AgenticSettings, AgentIdentity
from agentic.services import checkout_service as acs
from tests.factories import PaymentProviderAccountFactory

pytestmark = [pytest.mark.django_db, pytest.mark.integration]

REGISTRY = "payment_providers.services.payment_orchestration_service.ProviderRegistry.get_provider"
GET_PROVIDER = "payment_providers.models.PaymentProviderAccount.get_provider_instance"

BUYER = {
    "email": "shopper@example.com",
    "name": "Dana Digital",
    "billing_address": {
        "address_type": "billing",
        "name": "Dana Digital",
        "address1": "500 Market St",
        "city": "Beverly Hills",
        "state": "CA",
        "country": "US",
        "postal_code": "90210",
    },
}

CARD = {"card": {"number": "4242424242424242"}}


def _paid_provider():
    provider = mock.MagicMock()
    provider.create_payment_intent_for_checkout.return_value = {
        "success": True,
        "provider_intent_id": "pi_test",
        "status": "requires_payment_method",
    }
    provider.confirm_payment_intent.return_value = {"success": True, "status": "succeeded"}
    # Currency support is consulted during provider auto-selection
    # (PaymentMethodFilter._supports_currency). Give a real list so selection is
    # deterministic and never touches a real provider class.
    provider.get_supported_currencies.return_value = ["USD", "GBP", "EUR"]
    return provider


@pytest.fixture(autouse=True)
def _stub_payment_provider():
    """
    Stub the payment provider for the ENTIRE flow (create/update/complete), so
    provider auto-selection never loads a real provider instance — see the
    module docstring for why scoping this only around `complete` flaked on CI.
    """
    with (
        mock.patch(REGISTRY, return_value=mock.MagicMock()),
        mock.patch(GET_PROVIDER, return_value=_paid_provider()),
    ):
        yield


@pytest.fixture
def agent_identity(db):
    return AgentIdentity.objects.create(
        directory="agent.example.com",
        key_thumbprint="kid-e2e",
        algorithm="ed25519",
        public_jwk={"kty": "OKP", "crv": "Ed25519", "x": "x"},
    )


@pytest.fixture
def enabled(db):
    s = AgenticSettings.get_settings()
    s.is_enabled = True
    s.allow_unverified_checkout = True  # isolate the checkout flow from auth
    s.save()
    return s


@pytest.fixture
def gateway(db, digital_product, site_settings, warehouse):
    # A connected provider available for the US billing country.
    return PaymentProviderAccountFactory()


class TestServiceEndToEnd:
    def test_create_update_complete_reaches_paid_agent_order(
        self, agent_identity, digital_product, gateway, site_settings, warehouse
    ):
        from orders.models import Order

        # 1) Create the checkout session from a line item.
        cid = acs.create_checkout_session(
            agent=agent_identity, line_items=[{"product_id": digital_product.id}]
        )

        # 2) Provide the buyer (billing address for a digital order).
        acs.update_checkout_session(cid, agent_identity, buyer=BUYER)
        session = acs.load_session(cid, agent_identity)
        # A provider was auto-selected and the session is now ready.
        body = acs.build_ucp_checkout_session(session, cid)
        assert body["status"] == acs.STATUS_READY, body["messages"]

        # 3) Complete with a payment credential (provider stubbed to succeed).
        result = acs.complete_checkout_session(
            cid, agent_identity, payment=CARD, attested_total=body["totals"]["total"]
        )

        assert result["status"] == acs.STATUS_COMPLETED
        assert result["order"]["status"] == "paid"

        order = Order.objects.get(id=result["order"]["id"])
        assert order.payment_status == "paid"
        assert order.channel == "agent"  # attribution landed
        assert order.metadata.get("ucp_checkout_id") == cid

    def test_price_attestation_mismatch_refuses(
        self, agent_identity, digital_product, gateway, site_settings, warehouse
    ):
        cid = acs.create_checkout_session(
            agent=agent_identity, line_items=[{"product_id": digital_product.id}]
        )
        acs.update_checkout_session(cid, agent_identity, buyer=BUYER)

        # Attest a total that does not match — must refuse before charging.
        with pytest.raises(acs.CheckoutError) as exc:
            acs.complete_checkout_session(
                cid, agent_identity, payment=CARD, attested_total={"amount": 1, "currency": "USD"}
            )
        assert exc.value.code == "price_changed"
        assert exc.value.http_status == 409

    def test_completion_is_idempotent_on_replay(
        self, agent_identity, digital_product, gateway, site_settings, warehouse
    ):
        from orders.models import Order

        cid = acs.create_checkout_session(
            agent=agent_identity, line_items=[{"product_id": digital_product.id}]
        )
        acs.update_checkout_session(cid, agent_identity, buyer=BUYER)

        first = acs.complete_checkout_session(cid, agent_identity, payment=CARD)
        # The session is gone after payment; a replay resolves via the order.
        second = acs.complete_checkout_session(cid, agent_identity, payment=CARD)

        assert first["order"]["id"] == second["order"]["id"]
        assert Order.objects.filter(channel="agent").count() == 1


class TestMandateIssuance:
    def test_completion_issues_verifiable_mandate(
        self, agent_identity, digital_product, gateway, site_settings, warehouse
    ):
        from agentic.identity import sdjwt
        from agentic.identity.keys import generate_ap2_key, get_jwks
        from agentic.models import Mandate

        key = generate_ap2_key()  # store now advertises + issues AP2 mandates

        cid = acs.create_checkout_session(
            agent=agent_identity, line_items=[{"product_id": digital_product.id}]
        )
        acs.update_checkout_session(cid, agent_identity, buyer=BUYER)
        result = acs.complete_checkout_session(cid, agent_identity, payment=CARD)

        assert result["status"] == acs.STATUS_COMPLETED
        mandate = result["mandate"]
        assert mandate is not None
        assert mandate["format"] == "ap2-checkout-mandate+sd-jwt"

        # Completion issues both AP2 mandates: the Checkout Mandate (surfaced as
        # `mandate`) and the Payment Mandate (surfaced as `payment_mandate`).
        assert Mandate.objects.filter(mandate_type=Mandate.TYPE_CHECKOUT).count() == 1
        assert Mandate.objects.filter(mandate_type=Mandate.TYPE_PAYMENT).count() == 1
        jwk = next(k for k in get_jwks()["keys"] if k["kid"] == key.kid)
        payload, disclosed = sdjwt.verify_sd_jwt(mandate["value"], public_jwk=jwk)
        assert payload["order_ref"] == result["order"]["id"]
        assert disclosed["buyer_email"] == BUYER["email"]

        # The payment mandate is present, verifies, and carries the agent-presence
        # signal without leaking the operator's identity.
        payment_mandate = result["payment_mandate"]
        assert payment_mandate is not None
        assert payment_mandate["format"] == "ap2-payment-mandate+sd-jwt"
        ppayload, _ = sdjwt.verify_sd_jwt(payment_mandate["value"], public_jwk=jwk)
        assert ppayload["mandate_type"] == "payment"
        assert ppayload["human_present"] is False

    def test_mandate_endpoint_scopes_and_serves(
        self, client, enabled, agent_identity, digital_product, gateway, site_settings, warehouse
    ):
        from agentic.identity.keys import generate_ap2_key

        generate_ap2_key()
        create = client.post(
            "/api/agentic/ucp/checkout-sessions/",
            data={"line_items": [{"product_id": digital_product.id}], "buyer": BUYER},
            content_type="application/json",
        )
        cid = create.json()["id"]
        client.post(
            f"/api/agentic/ucp/checkout-sessions/{cid}/complete/",
            data={"payment": CARD},
            content_type="application/json",
        )
        resp = client.get(f"/api/agentic/ucp/checkout-sessions/{cid}/mandate/")
        assert resp.status_code == 200
        assert resp.json()["format"] == "ap2-checkout-mandate+sd-jwt"


class TestDoubleChargeGuard:
    def test_second_intent_on_paid_order_does_not_resettle(
        self, agent_identity, digital_product, gateway, site_settings, warehouse
    ):
        """The security backstop: a second intent confirmed against an already-
        paid order must not create a second charge/transaction (Codex + auditor
        double-charge finding)."""
        from payment_providers.models import PaymentIntent, PaymentTransaction
        from payment_providers.services.payment_orchestration_service import (
            PaymentOrchestrationService,
        )

        cid = acs.create_checkout_session(
            agent=agent_identity, line_items=[{"product_id": digital_product.id}]
        )
        acs.update_checkout_session(cid, agent_identity, buyer=BUYER)
        session = acs.load_session(cid, agent_identity)
        assert session.payment_provider is not None  # auto-selected deterministically

        # First intent settles the order.
        _, intent1, _ = PaymentOrchestrationService.create_payment_intent(
            session, session.payment_provider, "http://r", "http://c"
        )
        PaymentOrchestrationService.confirm_payment_intent(intent1, confirmation_data=CARD)
        order = intent1.order
        order.refresh_from_db()
        assert order.payment_status == "paid"
        txns_after_first = PaymentTransaction.objects.filter(order=order).count()

        # Fabricate a second intent on the SAME (now paid) order and confirm.
        intent2 = PaymentIntent.objects.create(
            order=order,
            provider_account=session.payment_provider,
            amount=intent1.amount,
            provider_intent_id="pi_second",
            status="created",
            expires_at=intent1.expires_at,
        )
        ok, msg = PaymentOrchestrationService.confirm_payment_intent(
            intent2, confirmation_data=CARD
        )

        # The confirm must be refused (order already paid), and NO second
        # settlement transaction created.
        assert ok is False
        assert PaymentTransaction.objects.filter(order=order).count() == txns_after_first


class TestBindingEndToEnd:
    def test_http_create_then_complete(
        self, client, enabled, agent_identity, digital_product, gateway, site_settings, warehouse
    ):
        # allow_unverified_checkout is on (fixture), so no signature needed.
        create = client.post(
            "/api/agentic/ucp/checkout-sessions/",
            data={"line_items": [{"product_id": digital_product.id}], "buyer": BUYER},
            content_type="application/json",
        )
        assert create.status_code == 201, create.content
        cid = create.json()["id"]

        complete = client.post(
            f"/api/agentic/ucp/checkout-sessions/{cid}/complete/",
            data={"payment": CARD},
            content_type="application/json",
        )
        assert complete.status_code == 200, complete.content
        assert complete.json()["status"] == acs.STATUS_COMPLETED

    def test_http_checkout_requires_signature_when_not_allowed(
        self, client, digital_product, site_settings
    ):
        s = AgenticSettings.get_settings()
        s.is_enabled = True
        s.allow_unverified_checkout = False
        s.save()

        resp = client.post(
            "/api/agentic/ucp/checkout-sessions/",
            data={"line_items": [{"product_id": digital_product.id}]},
            content_type="application/json",
        )
        assert resp.status_code == 401
