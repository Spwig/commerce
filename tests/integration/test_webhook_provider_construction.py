"""Regression tests for WebhookService provider construction.

WebhookService used to build its provider with ``provider_class(provider_account)``
— handing the account MODEL to a constructor whose contract is
``__init__(self, credentials: dict, ...)``. That raised ``TypeError`` inside
``_select_credentials`` ("argument of type 'PaymentProviderAccount' is not
iterable"); swallowed by the surrounding ``try/except``, signature verification
failed **closed** and every inbound webhook was rejected with a 400. There was
no test for it, so it went unnoticed.

These pin the fix: the service constructs via the account's own
credential-aware factory (``get_provider_instance()``) and delegates to the
provider's real methods, so a genuinely valid signature verifies and webhook
processing runs.
"""

from unittest import mock

import pytest

from payment_providers.models import PaymentProviderAccount
from payment_providers.services.webhook_service import WebhookService
from tests.factories import PaymentProviderAccountFactory

pytestmark = pytest.mark.django_db

# The registry existence-guard runs before construction; in the test env the
# component isn't discoverable on disk, so stub it truthy to reach the fix.
WS_REGISTRY = "payment_providers.services.webhook_service.ProviderRegistry.get_provider"
GET_PROVIDER = "payment_providers.models.PaymentProviderAccount.get_provider_instance"


def test_verify_webhook_signature_uses_credential_factory_and_delegates():
    """A valid signature verifies: the service builds the provider via
    get_provider_instance() (not provider_class(account)) and returns the
    provider's verdict rather than a swallowed-TypeError False."""
    account = PaymentProviderAccountFactory()
    provider = mock.MagicMock()
    provider.verify_webhook_signature.return_value = True

    with (
        mock.patch(WS_REGISTRY, return_value=mock.MagicMock()),
        mock.patch.object(
            PaymentProviderAccount, "get_provider_instance", return_value=provider
        ) as factory,
    ):
        ok = WebhookService.verify_webhook_signature(
            provider_account=account,
            payload=b"{}",
            signature="sig",
            headers={"x-test": "1"},
        )

    assert ok is True
    # Built via the credential-aware factory, not by passing the account model.
    factory.assert_called_once()
    provider.verify_webhook_signature.assert_called_once()


def test_verify_webhook_signature_returns_false_on_bad_signature():
    """A bad signature is rejected — but because the provider said so, not
    because construction crashed. (The old bug returned False for *every*
    signature, good or bad.)"""
    account = PaymentProviderAccountFactory()
    provider = mock.MagicMock()
    provider.verify_webhook_signature.return_value = False

    with (
        mock.patch(WS_REGISTRY, return_value=mock.MagicMock()),
        mock.patch.object(PaymentProviderAccount, "get_provider_instance", return_value=provider),
    ):
        ok = WebhookService.verify_webhook_signature(
            provider_account=account,
            payload=b"{}",
            signature="bad",
            headers={},
        )

    assert ok is False
    provider.verify_webhook_signature.assert_called_once()
