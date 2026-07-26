"""
Agent identity / policy / event models.

The AgentEvent tests are the load-bearing ones: it is the deliberately
separate, append-only, hash-chained audit log, and those three properties are
exactly what a "consolidate the audit logs" refactor would quietly break.
"""

import pytest
from django.db import IntegrityError

from agentic.models import AgentEvent, AgentIdentity, AgentPolicy

pytestmark = [pytest.mark.django_db, pytest.mark.integration]


def _agent(directory="agent.example.com", kid="thumb-aaa", **kw):
    return AgentIdentity.objects.create(
        directory=directory,
        key_thumbprint=kid,
        algorithm="ed25519",
        public_jwk={"kty": "OKP", "crv": "Ed25519", "x": "x"},
        **kw,
    )


class TestAgentIdentity:
    def test_defaults_to_capped(self):
        a = _agent()
        assert a.trust_state == AgentIdentity.TRUST_CAPPED
        assert a.is_blocked is False

    def test_directory_key_pair_is_unique(self):
        _agent(directory="a.com", kid="k1")
        # Same directory, different key → allowed (rotation / multiple keys).
        _agent(directory="a.com", kid="k2")
        # Same directory AND key → rejected.
        with pytest.raises(IntegrityError):
            _agent(directory="a.com", kid="k1")

    def test_str_prefers_claimed_name_but_shows_directory(self):
        a = _agent(claimed_name="ShopBot")
        assert "ShopBot" in str(a)
        assert "agent.example.com" in str(a)


class TestAgentPolicy:
    def test_capped_defaults(self):
        a = _agent()
        p = AgentPolicy.objects.create(agent=a)
        # Higher-risk capabilities off under the default capped policy.
        assert p.allow_discount_codes is False
        assert p.allow_gift_cards is False
        assert p.allow_digital_goods is False
        assert p.rate_limit_per_minute == 60

    def test_one_policy_per_agent(self):
        a = _agent()
        AgentPolicy.objects.create(agent=a)
        with pytest.raises(IntegrityError):
            AgentPolicy.objects.create(agent=a)


class TestAgentEventChain:
    def test_append_builds_a_chain(self):
        a = _agent()
        e1 = AgentEvent.append(AgentEvent.EVENT_AGENT_SEEN, agent=a)
        e2 = AgentEvent.append(AgentEvent.EVENT_SIG_VERIFIED, agent=a, detail={"path": "/x"})

        assert e1.chain_index == 1
        assert e2.chain_index == 2
        assert e1.prev_hash == AgentEvent._GENESIS_HASH
        assert e2.prev_hash == e1.entry_hash
        assert AgentEvent.verify_chain() is True

    def test_failed_sig_event_needs_no_agent(self):
        # A verification failure has no established identity, but is still logged.
        e = AgentEvent.append(
            AgentEvent.EVENT_SIG_FAILED,
            directory="unknown.example",
            key_thumbprint="k9",
            detail={"reason": "bad_signature"},
        )
        assert e.agent is None
        assert e.directory == "unknown.example"
        assert AgentEvent.verify_chain() is True

    def test_rows_cannot_be_updated(self):
        a = _agent()
        e = AgentEvent.append(AgentEvent.EVENT_AGENT_SEEN, agent=a)
        e.event_type = AgentEvent.EVENT_AGENT_BLOCKED
        with pytest.raises(ValueError, match="append-only"):
            e.save()

    def test_rows_cannot_be_deleted(self):
        a = _agent()
        e = AgentEvent.append(AgentEvent.EVENT_AGENT_SEEN, agent=a)
        with pytest.raises(ValueError, match="append-only"):
            e.delete()

    def test_tamper_is_detectable(self):
        a = _agent()
        AgentEvent.append(AgentEvent.EVENT_AGENT_SEEN, agent=a)
        AgentEvent.append(AgentEvent.EVENT_SIG_VERIFIED, agent=a)
        assert AgentEvent.verify_chain() is True

        # Tamper with a row's payload directly in the DB (bypassing save()).
        AgentEvent.objects.filter(chain_index=1).update(detail={"path": "/tampered"})
        assert AgentEvent.verify_chain() is False

    def test_chain_hash_is_keyed_with_secret(self):
        # The chain is an HMAC keyed on SECRET_KEY, not a bare hash: recomputing
        # a row's hash under a different key must NOT reproduce the stored value,
        # so a DB-level forger without the secret can't rebuild a valid chain.
        from unittest import mock

        a = _agent()
        ev = AgentEvent.append(AgentEvent.EVENT_AGENT_SEEN, agent=a)
        payload = AgentEvent._payload(
            ev.event_type, ev.directory, ev.key_thumbprint, ev.detail, ev.created_at
        )
        with mock.patch.object(AgentEvent, "_chain_key", return_value=b"wrong-key"):
            forged = AgentEvent._compute_hash(ev.chain_index, ev.prev_hash, payload)
        assert forged != ev.entry_hash

    def test_nulling_agent_preserves_denormalized_origin(self):
        a = _agent(directory="keep.example", kid="kk")
        AgentEvent.append(AgentEvent.EVENT_SIG_VERIFIED, agent=a)
        a.delete()  # SET_NULL on the event's FK
        ev = AgentEvent.objects.get(chain_index=1)
        assert ev.agent is None
        # The chain still verifies because the event stored the origin itself.
        assert ev.directory == "keep.example"
        assert ev.key_thumbprint == "kk"
        assert AgentEvent.verify_chain() is True
