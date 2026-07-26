"""
Readiness service + the agent-registry admin actions.
"""

import pytest

from agentic.models import AgentEvent, AgenticSettings, AgentIdentity
from agentic.services import readiness_service

pytestmark = [pytest.mark.django_db, pytest.mark.integration]


def _enable(**overrides):
    s = AgenticSettings.get_settings()
    s.is_enabled = True
    for k, v in overrides.items():
        setattr(s, k, v)
    s.save()


def _agent(kid="k1", **kw):
    return AgentIdentity.objects.create(
        directory="agent.example.com",
        key_thumbprint=kid,
        algorithm="ed25519",
        public_jwk={"kty": "OKP", "crv": "Ed25519", "x": "x"},
        **kw,
    )


class TestReadinessVerdict:
    def test_off_when_disabled(self, site_settings):
        r = readiness_service.store_readiness()
        assert r["verdict"] == readiness_service.VERDICT_OFF
        assert r["enabled"] is False

    def test_stopped_when_kill_switch(self, site_settings):
        _enable(kill_switch_engaged=True)
        r = readiness_service.store_readiness()
        assert r["verdict"] == readiness_service.VERDICT_STOPPED

    def test_browse_only_without_payment_provider(self, site_settings):
        _enable()
        r = readiness_service.store_readiness()
        # No connected payment provider in this DB → discoverable, not buyable.
        assert r["verdict"] == readiness_service.VERDICT_BROWSE_ONLY
        assert r["capabilities"]["checkout"] is False

    def test_ready_with_payment_provider(self, site_settings):
        from tests.factories import PaymentProviderAccountFactory

        PaymentProviderAccountFactory()  # active + connected
        _enable()
        r = readiness_service.store_readiness()
        assert r["verdict"] == readiness_service.VERDICT_READY
        assert r["capabilities"]["checkout"] is True

    def test_never_raises_and_has_checks(self, site_settings):
        r = readiness_service.store_readiness()
        assert isinstance(r["checks"], list) and len(r["checks"]) >= 3
        assert "products" in r and "agents" in r


class TestAgentRegistryActions:
    def _admin_call(self, action, queryset):
        from django.contrib.admin.sites import AdminSite
        from django.test import RequestFactory

        from agentic.admin import AgentIdentityAdmin

        admin = AgentIdentityAdmin(AgentIdentity, AdminSite())
        req = RequestFactory().post("/")
        req.user = type("U", (), {"get_username": lambda self: "tester"})()
        # message_user needs the messages framework; stub it.
        admin.message_user = lambda *a, **k: None
        getattr(admin, action)(req, queryset)

    def test_block_sets_state_and_logs(self, site_settings):
        agent = _agent()
        self._admin_call("block_agents", AgentIdentity.objects.filter(pk=agent.pk))
        agent.refresh_from_db()
        assert agent.trust_state == AgentIdentity.TRUST_BLOCKED
        assert agent.blocked_at is not None
        assert AgentEvent.objects.filter(event_type=AgentEvent.EVENT_AGENT_BLOCKED).exists()
        assert AgentEvent.verify_chain() is True

    def test_unblock_returns_to_capped_not_verified(self, site_settings):
        agent = _agent(trust_state=AgentIdentity.TRUST_BLOCKED)
        self._admin_call("unblock_agents", AgentIdentity.objects.filter(pk=agent.pk))
        agent.refresh_from_db()
        # Unblock never jumps straight to verified — lifting limits is separate.
        assert agent.trust_state == AgentIdentity.TRUST_CAPPED
        assert agent.blocked_at is None
        assert AgentEvent.objects.filter(event_type=AgentEvent.EVENT_AGENT_UNBLOCKED).exists()
