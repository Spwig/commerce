"""Admin API for attaching visibility RuleGroups to targets.

The shared visibility editor (the ``visibility_rules_editor`` utility) uses these
endpoints to gate ANY object — a page element, a menu item, or a header/footer
widget placement — by the same reusable ``RuleGroup``s, persisting the object's
``rule_groups`` / ``visibility_rules`` M2M.

Kept deliberately small and target-agnostic so all three builders share one
persistence path instead of threading M2M writes through each builder's own save.
"""

import logging

from django.apps import apps
from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import RuleGroup
from .service import create_quick_rule_group, set_visibility_rule_groups

logger = logging.getLogger(__name__)

# These are admin-UI-only endpoints (the builder pages, session-authenticated).
# Pin to SessionAuthentication so a non-session Bearer/API token — which is scope-
# gated elsewhere for the mobile Admin API but not here — can't reach them.
_ADMIN_UI_AUTH = [SessionAuthentication]

# Bound the full-replace list so a single request can't attach an absurd number of
# groups (cheap DoS guard; real installs have a handful).
_MAX_RULE_GROUPS = 100


# target_type -> (app_label, model_name, change_permission). The object must
# expose get_visibility_rule_groups() (Element, MenuItem, WidgetPlacement do).
_TARGETS = {
    "element": ("page_builder", "Element", "page_builder.change_element"),
    "menuitem": ("design", "MenuItem", "design.change_menuitem"),
    "widgetplacement": ("design", "WidgetPlacement", "design.change_widgetplacement"),
}


def _resolve_target(target_type, target_id, user):
    """Return (obj, error_response). Enforces the per-target change permission —
    being staff is not enough to edit a given object's visibility (CLAUDE.md)."""
    spec = _TARGETS.get(target_type)
    if spec is None:
        return None, Response(
            {"success": False, "error": "Unknown target_type"}, status=status.HTTP_400_BAD_REQUEST
        )
    app_label, model_name, perm = spec
    if not user.has_perm(perm):
        return None, Response(
            {"success": False, "error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
        )
    model = apps.get_model(app_label, model_name)
    try:
        obj = model.objects.get(pk=target_id)
    except (model.DoesNotExist, ValueError, TypeError):
        return None, Response(
            {"success": False, "error": "Target not found"}, status=status.HTTP_404_NOT_FOUND
        )
    return obj, None


def _group_summary(group):
    """Compact option payload for the editor's rule-group picker."""
    try:
        labels = group.rule_labels()
    except Exception:
        labels = []
    return {
        "id": group.id,
        "name": group.name,
        "logic_operator": group.logic_operator,
        "rules_count": group.rules.count(),
        "summary": ", ".join(str(x) for x in labels[:4]),
    }


class RuleGroupOptionsView(APIView):
    """GET: list active, top-level RuleGroups for the editor's picker."""

    authentication_classes = _ADMIN_UI_AUTH
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        groups = (
            RuleGroup.objects.filter(is_active=True, parent_group__isnull=True)
            .prefetch_related("rules")
            .order_by("name")
        )
        return Response({"success": True, "rule_groups": [_group_summary(g) for g in groups]})


class VisibilityAttachView(APIView):
    """Read or set the RuleGroups attached to a target object.

    GET  ?target_type=&target_id=            -> {rule_group_ids: [...]}
    POST {target_type, target_id, rule_group_ids} -> sets the M2M (full replace).
    """

    authentication_classes = _ADMIN_UI_AUTH
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        obj, err = _resolve_target(
            request.query_params.get("target_type"),
            request.query_params.get("target_id"),
            request.user,
        )
        if err:
            return err
        ids = list(obj.get_visibility_rule_groups().values_list("id", flat=True))
        return Response({"success": True, "rule_group_ids": ids})

    def post(self, request):
        data = request.data or {}
        obj, err = _resolve_target(data.get("target_type"), data.get("target_id"), request.user)
        if err:
            return err

        raw_ids = data.get("rule_group_ids", [])
        if not isinstance(raw_ids, list):
            return Response(
                {"success": False, "error": "rule_group_ids must be a list"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(raw_ids) > _MAX_RULE_GROUPS:
            return Response(
                {"success": False, "error": f"At most {_MAX_RULE_GROUPS} rule groups"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            valid_ids = set_visibility_rule_groups(obj, raw_ids)
        except ValueError as exc:
            return Response(
                {"success": False, "error": str(exc)}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response({"success": True, "rule_group_ids": valid_ids})


class QuickRuleGroupView(APIView):
    """POST: create a single-rule RuleGroup in one call, for the editor's
    'quick create' shortcut. Materialises a real VisibilityRule + RuleGroup so the
    engine evaluates it like any admin-authored group (never a throwaway JSON)."""

    authentication_classes = _ADMIN_UI_AUTH
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        if not (
            request.user.has_perm("visibility.add_rulegroup")
            and request.user.has_perm("visibility.add_visibilityrule")
        ):
            return Response(
                {"success": False, "error": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN,
            )
        data = request.data or {}
        try:
            group = create_quick_rule_group(
                rule_type=data.get("rule_type"),
                operator=data.get("operator", "equals"),
                value=data.get("value", {}),
                name=data.get("name", ""),
            )
        except ValueError as exc:
            return Response(
                {"success": False, "error": str(exc)}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {"success": True, "rule_group": _group_summary(group)},
            status=status.HTTP_201_CREATED,
        )
