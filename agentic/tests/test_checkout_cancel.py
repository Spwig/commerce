"""
Agentic checkout cancellation — the STATUS_CANCELED transition.

Cancellation is recorded on the shared CheckoutSession's metadata (it has no
status column), so a canceled session reads back as `canceled` and refuses
further update/complete rather than silently reverting to not-ready.
"""

import pytest

from agentic.models import AgentIdentity
from agentic.services import checkout_service as acs
from tests.factories import ProductFactory

pytestmark = [pytest.mark.django_db, pytest.mark.integration]


def _agent(kid="cx-1"):
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


def _session(agent):
    p = _product()
    return acs.create_checkout_session(agent=agent, line_items=[{"product_id": p.id}])


class TestCancel:
    def test_cancel_marks_session_canceled(self, site_settings):
        agent = _agent()
        cid = _session(agent)
        body = acs.cancel_checkout_session(cid, agent)
        assert body["status"] == acs.STATUS_CANCELED
        assert body["payment"]["status"] == "canceled"
        assert body["payment"]["continue_url"] is None
        # A subsequent GET reflects the canceled state too.
        assert acs.get_checkout_view(cid, agent)["status"] == acs.STATUS_CANCELED

    def test_cancel_is_idempotent(self, site_settings):
        agent = _agent()
        cid = _session(agent)
        acs.cancel_checkout_session(cid, agent)
        body = acs.cancel_checkout_session(cid, agent)  # no error
        assert body["status"] == acs.STATUS_CANCELED

    def test_update_refused_after_cancel(self, site_settings):
        agent = _agent()
        cid = _session(agent)
        acs.cancel_checkout_session(cid, agent)
        with pytest.raises(acs.CheckoutError) as exc:
            acs.update_checkout_session(cid, agent, buyer={"email": "a@b.c"})
        assert exc.value.code == "checkout_canceled"
        assert exc.value.http_status == 409

    def test_complete_refused_after_cancel(self, site_settings):
        agent = _agent()
        cid = _session(agent)
        acs.cancel_checkout_session(cid, agent)
        with pytest.raises(acs.CheckoutError) as exc:
            acs.complete_checkout_session(cid, agent, payment={})
        assert exc.value.code == "checkout_canceled"
        assert exc.value.http_status == 409

    def test_cancel_refused_while_completion_is_locked(self, site_settings):
        # Cancel shares the completion lock: if a charge is in flight it must not
        # return a `canceled` view for a checkout that is about to be paid.
        from django.core.cache import cache

        from agentic.services.checkout_service import COMPLETE_LOCK_TTL, _complete_lock_key

        agent = _agent()
        cid = _session(agent)
        cache.add(_complete_lock_key(cid), "1", COMPLETE_LOCK_TTL)  # simulate in-flight completion
        try:
            with pytest.raises(acs.CheckoutError) as exc:
                acs.cancel_checkout_session(cid, agent)
            assert exc.value.code == "completion_in_progress"
            assert exc.value.http_status == 409
        finally:
            cache.delete(_complete_lock_key(cid))
        # Once the lock clears, cancel proceeds normally.
        assert acs.cancel_checkout_session(cid, agent)["status"] == acs.STATUS_CANCELED

    def _make_intent(self, session, status):
        from django.utils import timezone
        from djmoney.money import Money

        from payment_providers.models import PaymentIntent
        from tests.factories import OrderFactory, PaymentProviderAccountFactory

        return PaymentIntent.objects.create(
            checkout_session=session,
            provider_account=PaymentProviderAccountFactory(),
            order=OrderFactory(),
            provider_intent_id=f"pi_test_{status}",
            amount=Money(25, "USD"),
            status=status,
            expires_at=timezone.now() + timezone.timedelta(hours=1),
        )

    def test_cancel_refused_when_settleable_intent_exists(self, site_settings):
        # A 3DS/redirect (requires_action) or processing intent can still settle
        # via the provider/webhook, so cancel must refuse rather than report a
        # canceled session that could still be paid.
        agent = _agent()
        cid = _session(agent)
        self._make_intent(acs.load_session(cid, agent), "requires_action")
        with pytest.raises(acs.CheckoutError) as exc:
            acs.cancel_checkout_session(cid, agent)
        assert exc.value.code == "payment_in_progress"
        assert exc.value.http_status == 409
        assert acs.get_checkout_view(cid, agent)["status"] != acs.STATUS_CANCELED

    def test_cancel_refused_when_pending_order_exists(self, site_settings):
        # A failed/retryable completion attempt already created an unpaid order
        # holding a stock allocation. Cancel is for pre-order sessions only, so it
        # must refuse (order_pending) rather than stamp `canceled` over that
        # allocation — the order has its own lifecycle.
        from tests.factories import OrderFactory

        agent = _agent()
        cid = _session(agent)
        OrderFactory(
            channel="agent",
            payment_status="unpaid",
            metadata={"ucp_checkout_id": cid, "agent_identity_id": str(agent.id)},
        )
        with pytest.raises(acs.CheckoutError) as exc:
            acs.cancel_checkout_session(cid, agent)
        assert exc.value.code == "order_pending"
        assert exc.value.http_status == 409
        assert acs.get_checkout_view(cid, agent)["status"] != acs.STATUS_CANCELED

    def test_cancel_unknown_session_is_404(self, site_settings):
        with pytest.raises(acs.CheckoutError) as exc:
            acs.cancel_checkout_session("does-not-exist", _agent())
        assert exc.value.http_status == 404

    def test_other_agent_cannot_cancel(self, site_settings):
        owner = _agent("owner")
        other = _agent("other")
        cid = _session(owner)
        # A non-owner sees not-found, never a 403 that would confirm existence.
        with pytest.raises(acs.CheckoutError) as exc:
            acs.cancel_checkout_session(cid, other)
        assert exc.value.http_status == 404
        # And the owner's session is untouched — still cancelable by the owner.
        assert acs.cancel_checkout_session(cid, owner)["status"] == acs.STATUS_CANCELED
