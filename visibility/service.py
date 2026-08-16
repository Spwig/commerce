"""Shared visibility resolution for any object gated by RuleGroups.

Both page content (``page_builder.Element``) and navigation (``design.MenuItem``,
``design.WidgetPlacement``) decide show / hide / defer through the SAME function
here, so the shell-vs-deferred contract can never drift between them:

* **shell** rules (geo_region / market, language, currency) and **temporal** rules
  (date/time/day/business-hours) are evaluated server-side into the cacheable
  shell — deterministic per market URL, SEO-safe.
* **deferred** (per-visitor: auth, cart, device, precise geo, behaviour) rules are
  never evaluated into the shared shell; the object defers to the personalization
  pass instead.

Any object passed here must expose ``get_visibility_rule_groups()`` returning its
``visibility.RuleGroup`` M2M manager, and may expose an ``is_active`` flag.
"""

import logging

logger = logging.getLogger(__name__)

SHOW = "show"
HIDE = "hide"
DEFER = "defer"


def collect_visibility_context(request, context=None):
    """Collect (and memoize on the request) the rule-evaluation context.

    ``ContextCollector.collect_context`` does cart/geo/user queries, so it is
    gathered once per request and reused across every element and nav item rather
    than re-collected per object.
    """
    if context is not None or request is None:
        return context
    context = getattr(request, "_visibility_context", None)
    if context is None:
        from .evaluator import ContextCollector

        context = ContextCollector().collect_context(request)
        try:
            request._visibility_context = context
        except Exception:
            pass
    return context


def resolve_visibility(obj, request=None, context=None):
    """Decide how ``obj`` renders in the cacheable shell: ``"show"`` / ``"hide"`` /
    ``"defer"``.

    - ``"show"``  — render it (no rules, or a shell/temporal rule matched).
    - ``"hide"``  — omit it (a shell rule excluded it, or it is inactive).
    - ``"defer"`` — its visibility depends on a per-visitor rule that must not be
      evaluated into the shared shell; the caller emits a placeholder for the
      personalization pass (page elements) or, until deferred nav lands, fails
      closed (nav).
    """
    if not getattr(obj, "is_active", True):
        return HIDE

    active_groups = list(obj.get_visibility_rule_groups().filter(is_active=True))
    if not active_groups:
        # No ACTIVE gate → visible. Inactive (disabled) rule groups impose no
        # restriction, so disabling every group on an item restores normal
        # visibility rather than hiding it (an inactive group is not a "hide all"
        # switch). Also avoids a redundant existence query.
        return SHOW

    context = collect_visibility_context(request, context)

    # A group is shell-safe only if it contains no per-visitor (deferred) rule.
    shell_groups = [g for g in active_groups if not g.contains_deferred_rule()]
    # OR across groups: visible if any shell-safe group matches.
    if any(group.evaluate(context) for group in shell_groups):
        return SHOW
    # A deferred group might still make it visible — defer that decision.
    if any(group.contains_deferred_rule() for group in active_groups):
        return DEFER
    return HIDE


def is_fully_visible(obj, request=None, context=None):
    """Full server-side visibility for ``obj`` — evaluate EVERY active rule group
    (shell AND deferred) against the real visitor context.

    Used by the personalization pass, which runs with the visitor's actual
    session (auth, cart, device, precise geo) and so may evaluate the per-visitor
    rules that ``resolve_visibility`` deliberately defers. Returns True when the
    object has no active gate, or when any active group matches.
    """
    if not getattr(obj, "is_active", True):
        return False
    active_groups = list(obj.get_visibility_rule_groups().filter(is_active=True))
    if not active_groups:
        return True
    context = collect_visibility_context(request, context)
    return any(group.evaluate(context) for group in active_groups)


def requires_personalization(obj):
    """True if any rule group on ``obj`` holds a per-visitor (deferred) rule —
    such an object can't be baked into the cacheable shell.

    ``contains_deferred_rule`` already ignores inactive rules/child-groups
    internally, so this walks every attached group (matching the page engine's
    original semantics)."""
    return any(group.contains_deferred_rule() for group in obj.get_visibility_rule_groups().all())


def set_visibility_rule_groups(obj, rule_group_ids):
    """Attach a set of visibility RuleGroups to a target (page element, menu item,
    or widget placement), replacing whatever was there.

    Keeps only ids that are real RuleGroups so a stale/bogus id can never create a
    dangling through-row. Returns the applied ids. Raises ``ValueError`` if the
    ids aren't integers.
    """
    from .models import RuleGroup

    try:
        wanted = {int(i) for i in rule_group_ids}
    except (ValueError, TypeError) as exc:
        raise ValueError("rule_group_ids must be integers") from exc
    valid_ids = list(RuleGroup.objects.filter(id__in=wanted).values_list("id", flat=True))
    obj.get_visibility_rule_groups().set(valid_ids)
    return valid_ids


def create_quick_rule_group(rule_type, operator="equals", value=None, name=""):
    """Create a single-rule RuleGroup in one step (one VisibilityRule wrapped in a
    group), for the editor's quick-create shortcut.

    Materialises a real VisibilityRule + RuleGroup so the engine evaluates it like
    any admin-authored group. Validates against the model choices and refuses the
    ``regex`` operator (a merchant-authored catastrophic pattern would run against
    visitor input on the storefront — advanced regex rules go through the full
    rule builder). Raises ``ValueError`` on invalid input. Returns the RuleGroup.
    """
    from django.db import transaction

    from .models import RuleGroup, RuleGroupMember, VisibilityRule

    valid_types = {rt[0] for rt in VisibilityRule.RULE_TYPES}
    valid_ops = {op[0] for op in VisibilityRule.OPERATORS}
    if rule_type not in valid_types:
        raise ValueError("Invalid rule_type")
    if operator not in valid_ops:
        raise ValueError("Invalid operator")
    if operator == "regex":
        raise ValueError("Use the rule builder for regex rules")

    name = (name or "").strip() or dict(VisibilityRule.RULE_TYPES).get(rule_type, rule_type)
    with transaction.atomic():
        rule = VisibilityRule.objects.create(
            name=name, rule_type=rule_type, operator=operator, value=value or {}
        )
        group = RuleGroup.objects.create(name=name)
        RuleGroupMember.objects.create(rule_group=group, rule=rule, order=0)
    return group
