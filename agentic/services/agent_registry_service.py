"""
Merchant actions on the calling-agent registry: promote to verified, and change
a calling agent's policy.

Trust-on-first-use establishes an identity in the `capped` state with concrete
spend/tender limits (see `agentic.identity.authentication`). Lifting those
limits, or adjusting them, is always a deliberate merchant action — never
automatic — so both operations live behind named service functions that record
the change in the append-only `AgentEvent` audit log.

These functions are the single write-seam for agent trust/policy; the admin
(and any future API) route through them so the audit trail is never bypassed.
"""

from __future__ import annotations

from django.db import transaction
from djmoney.money import Money

# The policy fields a merchant may change. Anything outside this set is refused —
# `agent`, timestamps, and pk are not policy.
_MONEY_CAP_FIELDS = frozenset({"max_order_amount", "daily_spend_cap"})
_BOOL_FIELDS = frozenset({"allow_discount_codes", "allow_gift_cards", "allow_digital_goods"})
_INT_FIELDS = frozenset({"rate_limit_per_minute"})
POLICY_FIELDS = _MONEY_CAP_FIELDS | _BOOL_FIELDS | _INT_FIELDS


def _jsonable(value):
    """Render a policy value for the audit detail (Money → string, else as-is)."""
    if isinstance(value, Money):
        return str(value)
    return value


def _validate_policy_value(field: str, value):
    """
    Guard values as well as field names, so a future untrusted caller (a mobile
    or public API) can't route a bad type/negative amount straight into a policy.

    The admin inline already form-validates, so this is belt-and-braces for it and
    a hard gate for any other caller.
    """
    if field in _MONEY_CAP_FIELDS:
        if value is None:  # NULL == no cap
            return
        if not isinstance(value, Money):
            raise ValueError(f"{field} must be a Money or None")
        if value.amount < 0:
            raise ValueError(f"{field} cannot be negative")
    elif field in _BOOL_FIELDS:
        if not isinstance(value, bool):
            raise ValueError(f"{field} must be a bool")
    elif field in _INT_FIELDS:
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError(f"{field} must be a non-negative integer")


def verify_agent_identity(agent, *, actor: str = ""):
    """
    Promote a calling agent to the verified trust state, removing its caps.

    Verification is the deliberate removal of the `capped` limits: the agent's
    order-value and daily-spend caps are nulled (no cap) and the trust state
    becomes `verified`. A blocked agent cannot be verified — it must be unblocked
    first (unblock returns it to `capped`, never straight to `verified`). Records
    an `agent_verified` audit event. Idempotent on an already-verified agent.
    Returns the AgentIdentity.
    """
    from agentic.models import AgentEvent, AgentIdentity, AgentPolicy

    if agent.trust_state == AgentIdentity.TRUST_BLOCKED:
        raise ValueError("A blocked agent must be unblocked before it can be verified.")

    if agent.trust_state == AgentIdentity.TRUST_VERIFIED:
        return agent  # already verified — no-op, no duplicate event

    # Atomic: the state flip, cap removal, and audit append commit together, so a
    # verified agent can never end up without its `agent_verified` audit row (this
    # is the single audited write-seam for the promotion).
    with transaction.atomic():
        agent.trust_state = AgentIdentity.TRUST_VERIFIED
        agent.save(update_fields=["trust_state", "updated_at"])

        # Verified means "limits removed": null the caps so nothing downstream
        # keeps enforcing them. NULL == no cap (see AgentPolicy). A full save()
        # (rather than update_fields) is deliberate: a MoneyField carries a
        # companion `_currency` column, and a field-scoped save can skip it.
        policy, _ = AgentPolicy.objects.get_or_create(agent=agent)
        if policy.max_order_amount is not None or policy.daily_spend_cap is not None:
            policy.max_order_amount = None
            policy.daily_spend_cap = None
            policy.save()

        AgentEvent.append(
            AgentEvent.EVENT_AGENT_VERIFIED,
            agent=agent,
            detail={"by": actor, "caps_removed": True},
        )
    return agent


def change_agent_policy(agent, *, changes: dict, actor: str = ""):
    """
    Apply changes to a calling agent's spend/tender/rate-limit policy.

    `changes` maps policy field names to new values; only fields in
    `POLICY_FIELDS` are accepted (anything else raises ValueError). Money caps
    accept a `Money` or None (no cap). Only fields that actually differ are
    written, and when at least one changes an `policy_changed` audit event is
    appended carrying the before/after of each. A no-op change writes nothing and
    records no event. Returns the AgentPolicy.
    """
    from agentic.models import AgentEvent, AgentPolicy

    unknown = set(changes) - POLICY_FIELDS
    if unknown:
        raise ValueError(f"not policy fields: {sorted(unknown)}")
    for field, value in changes.items():
        _validate_policy_value(field, value)

    with transaction.atomic():
        policy, _ = AgentPolicy.objects.get_or_create(agent=agent)

        diff: dict[str, dict] = {}
        for field, new in changes.items():
            old = getattr(policy, field)
            if old != new:
                diff[field] = {"from": _jsonable(old), "to": _jsonable(new)}
                setattr(policy, field, new)

        if not diff:
            return policy

        # Full save() (not update_fields): a MoneyField carries a companion
        # `_currency` column that a field-scoped save can skip.
        policy.save()
        AgentEvent.append(
            AgentEvent.EVENT_POLICY_CHANGED,
            agent=agent,
            detail={"by": actor, "changes": diff},
        )
    return policy
