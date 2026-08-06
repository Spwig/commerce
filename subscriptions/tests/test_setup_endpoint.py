"""
Tests for the provider-agnostic reusable-method setup endpoint
(`POST /api/subscriptions/tokens/begin-setup/`).

The point of these tests is that NO gateway is named in core: a provider that
ships a setup handler (declares `reusable_setup`) returns a client bundle, and
one that doesn't degrades gracefully to `supported: False` so the storefront can
fall back to saved tokens.
"""

import pytest
from rest_framework.test import APIClient

from tests.factories import PaymentProviderAccountFactory, UserFactory

pytestmark = [pytest.mark.django_db, pytest.mark.integration]

SETUP_URL = "/api/subscriptions/tokens/begin-setup/"


def _client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


def test_begin_setup_returns_client_bundle_for_a_setup_capable_provider():
    user = UserFactory()
    account = PaymentProviderAccountFactory(setup_capable=True, user=user)

    resp = _client(user).post(SETUP_URL, {"provider_account_id": str(account.id)}, format="json")

    assert resp.status_code == 200
    body = resp.json()
    assert body["supported"] is True
    assert body["provider_key"] == account.component.slug
    # client_params come from the provider's begin_setup(), not from core.
    assert body["client_params"]["client_secret"] == "seti_fake_secret"
    # manifest-driven bundle keys are always present (may be null for the fake).
    assert "handler_url" in body
    assert "sdk_dependencies" in body


def test_begin_setup_is_gracefully_gated_for_a_provider_without_setup_support():
    user = UserFactory()
    # subscribable fake supports subscriptions but NOT reusable setup.
    account = PaymentProviderAccountFactory(subscribable=True, user=user)

    resp = _client(user).post(SETUP_URL, {"provider_account_id": str(account.id)}, format="json")

    assert resp.status_code == 200
    assert resp.json()["supported"] is False


def test_begin_setup_requires_authentication():
    account = PaymentProviderAccountFactory(setup_capable=True)
    resp = APIClient().post(SETUP_URL, {"provider_account_id": str(account.id)}, format="json")
    assert resp.status_code in (401, 403)


def test_begin_setup_requires_a_provider_account_id():
    user = UserFactory()
    resp = _client(user).post(SETUP_URL, {}, format="json")
    assert resp.status_code == 400


def test_client_bundle_resolves_templated_sdk_urls(monkeypatch):
    """The bundle must substitute {{CLIENT_ID}}-style SDK templates from
    credentials (PayPal loads its SDK with client-id=...), or the SDK 404s."""
    import payment_providers.utils.encryption as enc

    monkeypatch.setattr(enc, "decrypt_credentials", lambda raw: {"client_id": "ABC123"})
    from payment_providers.services.frontend_bundle import build_client_bundle

    class _Comp:
        slug = "paypal_checkout"

        def get_manifest(self):
            return {
                "frontend": {
                    "checkout_handler": "checkout-handler.js",
                    "sdk_dependencies": ["https://www.paypal.com/sdk/js?client-id={{CLIENT_ID}}"],
                }
            }

    class _Acct:
        component = _Comp()
        credentials_encrypted = {"anything": True}

    bundle = build_client_bundle(_Acct())
    assert bundle["provider_key"] == "paypal_checkout"
    assert bundle["handler_url"] == (
        "/components/payments/paypal_checkout/current/checkout-handler.js"
    )
    assert bundle["sdk_dependencies"] == ["https://www.paypal.com/sdk/js?client-id=ABC123"]
