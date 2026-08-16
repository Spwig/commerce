"""
Agent-registry merchant actions: verify (promote + remove caps) and change-policy,
plus the admin surfaces that route through them so every change is audited.
"""

import pytest
from djmoney.money import Money

from agentic.models import AgentEvent, AgentIdentity, AgentPolicy
from agentic.services import agent_registry_service as ars

pytestmark = [pytest.mark.django_db, pytest.mark.integration]


def _agent(kid="reg-1", trust=AgentIdentity.TRUST_CAPPED, **kw):
    return AgentIdentity.objects.create(
        directory="agent.example.com",
        key_thumbprint=kid,
        algorithm="ed25519",
        public_jwk={"kty": "OKP", "crv": "Ed25519", "x": "x"},
        trust_state=trust,
        **kw,
    )


class TestVerifyAgentIdentity:
    def test_promotes_capped_to_verified_and_removes_caps(self):
        agent = _agent()
        AgentPolicy.objects.create(
            agent=agent, max_order_amount=Money(100, "USD"), daily_spend_cap=Money(500, "USD")
        )

        ars.verify_agent_identity(agent, actor="dayyan")

        agent.refresh_from_db()
        assert agent.trust_state == AgentIdentity.TRUST_VERIFIED
        policy = agent.policy
        policy.refresh_from_db()
        assert policy.max_order_amount is None  # caps lifted
        assert policy.daily_spend_cap is None
        ev = AgentEvent.objects.filter(event_type=AgentEvent.EVENT_AGENT_VERIFIED).first()
        assert ev is not None and ev.detail["caps_removed"] is True
        assert AgentEvent.verify_chain() is True

    def test_blocked_agent_cannot_be_verified(self):
        agent = _agent(trust=AgentIdentity.TRUST_BLOCKED)
        with pytest.raises(ValueError):
            ars.verify_agent_identity(agent)
        agent.refresh_from_db()
        assert agent.trust_state == AgentIdentity.TRUST_BLOCKED  # unchanged
        assert not AgentEvent.objects.filter(event_type=AgentEvent.EVENT_AGENT_VERIFIED).exists()

    def test_verify_is_idempotent(self):
        agent = _agent(trust=AgentIdentity.TRUST_VERIFIED)
        ars.verify_agent_identity(agent)  # already verified → no-op
        assert AgentEvent.objects.filter(event_type=AgentEvent.EVENT_AGENT_VERIFIED).count() == 0

    def test_verify_creates_policy_when_missing(self):
        agent = _agent()  # no policy row yet
        ars.verify_agent_identity(agent)
        assert AgentPolicy.objects.filter(agent=agent).exists()


class TestChangeAgentPolicy:
    def test_applies_changes_and_records_diff_event(self):
        agent = _agent()
        AgentPolicy.objects.create(agent=agent)

        ars.change_agent_policy(
            agent,
            changes={
                "allow_discount_codes": True,
                "max_order_amount": Money(250, "USD"),
                "rate_limit_per_minute": 120,
            },
            actor="dayyan",
        )

        policy = agent.policy
        policy.refresh_from_db()
        assert policy.allow_discount_codes is True
        assert policy.max_order_amount == Money(250, "USD")
        assert policy.rate_limit_per_minute == 120
        ev = AgentEvent.objects.filter(event_type=AgentEvent.EVENT_POLICY_CHANGED).first()
        assert ev is not None
        assert ev.detail["changes"]["rate_limit_per_minute"] == {"from": 60, "to": 120}
        assert "allow_discount_codes" in ev.detail["changes"]

    def test_noop_change_writes_no_event(self):
        agent = _agent()
        AgentPolicy.objects.create(agent=agent, rate_limit_per_minute=60)
        ars.change_agent_policy(agent, changes={"rate_limit_per_minute": 60})
        assert not AgentEvent.objects.filter(event_type=AgentEvent.EVENT_POLICY_CHANGED).exists()

    def test_unknown_field_is_rejected(self):
        agent = _agent()
        AgentPolicy.objects.create(agent=agent)
        with pytest.raises(ValueError):
            ars.change_agent_policy(agent, changes={"trust_state": "verified"})

    def test_creates_policy_when_missing(self):
        agent = _agent()
        ars.change_agent_policy(agent, changes={"allow_gift_cards": True})
        assert agent.policy.allow_gift_cards is True


class TestAdminVerifyAction:
    def _call(self, action, queryset):
        from django.contrib.admin.sites import AdminSite
        from django.test import RequestFactory

        from agentic.admin import AgentIdentityAdmin

        admin = AgentIdentityAdmin(AgentIdentity, AdminSite())
        req = RequestFactory().post("/")
        req.user = type("U", (), {"get_username": lambda self: "tester"})()
        admin.message_user = lambda *a, **k: None
        getattr(admin, action)(req, queryset)

    def test_verify_action_promotes_capped(self):
        agent = _agent()
        self._call("verify_agents", AgentIdentity.objects.filter(pk=agent.pk))
        agent.refresh_from_db()
        assert agent.trust_state == AgentIdentity.TRUST_VERIFIED

    def test_verify_action_skips_blocked(self):
        agent = _agent(trust=AgentIdentity.TRUST_BLOCKED)
        self._call("verify_agents", AgentIdentity.objects.filter(pk=agent.pk))
        agent.refresh_from_db()
        assert agent.trust_state == AgentIdentity.TRUST_BLOCKED  # left alone


class TestAdminPolicyInline:
    @pytest.fixture
    def superuser(self):
        from django.contrib.auth import get_user_model

        return get_user_model().objects.create_superuser(
            username="reg_admin", email="reg_admin@test.spwig.com", password="pw-12345!"
        )

    def test_editing_policy_inline_records_event(self, superuser):
        from django.test import Client

        agent = _agent()
        policy, _ = AgentPolicy.objects.get_or_create(agent=agent)

        c = Client()
        c.force_login(superuser)
        url = f"/en/admin/agentic/agentidentity/{agent.pk}/change/"
        assert c.get(url).status_code == 200

        data = {
            "policy-TOTAL_FORMS": "1",
            "policy-INITIAL_FORMS": "1",
            "policy-MIN_NUM_FORMS": "0",
            "policy-MAX_NUM_FORMS": "1",
            "policy-0-id": str(policy.pk),
            "policy-0-agent": str(agent.pk),
            "policy-0-max_order_amount_0": "",
            "policy-0-max_order_amount_1": "USD",
            "policy-0-daily_spend_cap_0": "",
            "policy-0-daily_spend_cap_1": "USD",
            "policy-0-allow_discount_codes": "on",
            "policy-0-rate_limit_per_minute": "90",
            "_save": "Save",
        }
        resp = c.post(url, data=data, follow=True)
        assert resp.status_code == 200
        assert b"errornote" not in resp.content

        policy.refresh_from_db()
        assert policy.allow_discount_codes is True
        assert policy.rate_limit_per_minute == 90
        assert AgentEvent.objects.filter(event_type=AgentEvent.EVENT_POLICY_CHANGED).exists()
