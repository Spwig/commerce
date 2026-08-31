"""Builder API — block CRUD, reorder, and save-to-MJML for the visual builder.

All endpoints are staff-only and gated on the marketing category (the same gate
the admin uses). CSRF is enforced; the builder JS sends the X-CSRFToken header.
Blocks are edited as CampaignBlock rows; ``save`` serialises them to the
campaign's MJML so the existing send path delivers them unchanged.
"""

import json
import logging

from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from staff_roles.decorators import requires_category

from .block_registry import get_block, sanitize_content
from .merge_fields import resolve_preview
from .models import Campaign, CampaignBlock
from .services.block_serializer import (
    render_block_canvas,
    save_campaign_html,
    serialize_campaign,
)

logger = logging.getLogger("email_marketing")


def _json(request):
    try:
        return json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return {}


def _block_payload(block) -> dict:
    """Serialise a block for the builder JS (canvas HTML + content + schema)."""
    cfg = get_block(block.block_type)
    return {
        "id": str(block.id),
        "block_type": block.block_type,
        "order": block.order,
        "content": block.content,
        "html": render_block_canvas(block),
        "name": cfg.name if cfg else block.block_type,
        "properties": cfg.properties if cfg else {},
    }


@staff_member_required
@requires_category("marketing", "full", ajax=True)
@require_http_methods(["POST"])
def create_block(request):
    """Add a block to a campaign with its default content."""
    data = _json(request)
    campaign = get_object_or_404(Campaign, id=data.get("campaign_id"))
    block_type = data.get("block_type", "")
    cfg = get_block(block_type)
    if not cfg:
        return JsonResponse({"error": "unknown_block_type"}, status=400)

    next_order = (campaign.blocks.aggregate(m=Max("order"))["m"] or 0) + 1
    block = CampaignBlock.objects.create(
        campaign=campaign,
        block_type=block_type,
        content=cfg.default_content(),
        order=next_order,
    )
    return JsonResponse({"success": True, "block": _block_payload(block)})


@staff_member_required
@requires_category("marketing", "full", ajax=True)
@require_http_methods(["PATCH", "POST"])
def update_block(request, block_id):
    """Merge new content into a block and return its re-rendered canvas HTML."""
    block = get_object_or_404(CampaignBlock, id=block_id)
    data = _json(request)
    content = data.get("content")
    if not isinstance(content, dict):
        return JsonResponse({"error": "content_must_be_object"}, status=400)

    cfg = get_block(block.block_type)
    if not cfg:
        return JsonResponse({"error": "unknown_block_type"}, status=400)
    # Validate values against the schema (select whitelist, safe URLs, colours)
    # and keep only declared properties — no mass-assignment, no XSS payloads.
    merged = dict(block.content or {})
    merged.update(sanitize_content(cfg, content))
    block.content = merged
    block.save(update_fields=["content", "updated_at"])
    return JsonResponse({"success": True, "block": _block_payload(block)})


@staff_member_required
@requires_category("marketing", "full", ajax=True)
@require_http_methods(["DELETE", "POST"])
def delete_block(request, block_id):
    """Remove a block from its campaign."""
    block = get_object_or_404(CampaignBlock, id=block_id)
    block.delete()
    return JsonResponse({"success": True})


@staff_member_required
@requires_category("marketing", "full", ajax=True)
@require_http_methods(["POST"])
def reorder_blocks(request):
    """Persist a new block order from a list of block ids."""
    data = _json(request)
    campaign = get_object_or_404(Campaign, id=data.get("campaign_id"))
    ordered_ids = data.get("order", [])
    if not isinstance(ordered_ids, list):
        return JsonResponse({"error": "order_must_be_list"}, status=400)

    blocks = {str(b.id): b for b in campaign.blocks.all()}
    with transaction.atomic():
        for index, bid in enumerate(ordered_ids):
            block = blocks.get(str(bid))
            if block and block.order != index:
                block.order = index
                block.save(update_fields=["order", "updated_at"])
    return JsonResponse({"success": True})


@staff_member_required
@requires_category("marketing", "full", ajax=True)
@require_http_methods(["POST"])
def save_campaign(request, campaign_id):
    """Serialise the campaign's blocks to MJML on Campaign.html_content."""
    campaign = get_object_or_404(Campaign, id=campaign_id)
    mjml = save_campaign_html(campaign)
    return JsonResponse({"success": True, "mjml_length": len(mjml)})


@staff_member_required
@requires_category("marketing", "full", ajax=True)
@require_http_methods(["POST"])
def preview_segment_count(request):
    """Return how many subscribers a draft dynamic rule set currently matches.

    Powers the rule-builder's live count. The rules run through the same
    ``resolve_segment`` (field/operator allowlist) as a saved segment, so a
    crafted payload can't build an unsafe or pathological query.
    """
    from email_marketing.models import Segment
    from email_marketing.services.segmentation import resolve_segment

    data = _json(request)
    rules = data.get("rules")
    if not isinstance(rules, dict):
        return JsonResponse({"error": "rules_must_be_object"}, status=400)

    from django.contrib.sites.models import Site

    draft = Segment(site=Site.objects.get(pk=1), kind=Segment.KIND_DYNAMIC, rules=rules)
    try:
        count = resolve_segment(draft).count()
    except Exception as exc:  # noqa: BLE001 — a bad draft rule shouldn't 500 the builder
        logger.warning("Segment preview-count failed: %s", exc)
        return JsonResponse({"error": "invalid_rules"}, status=422)
    return JsonResponse({"count": count})


@staff_member_required
@requires_category("marketing", "full", ajax=True)
@require_http_methods(["GET"])
def preview_campaign(request, campaign_id):
    """Return the compiled email HTML for the builder's preview (wire format).

    Serialises the current blocks to MJML, compiles to email-safe HTML, and
    substitutes merge fields with sample values so the preview reads naturally.
    The builder renders this inside a Shadow DOM for style isolation.
    """
    from mjml.mjml2html import mjml_to_html

    campaign = get_object_or_404(Campaign, id=campaign_id)
    try:
        result = mjml_to_html(serialize_campaign(campaign))
        html = result.get("html", "")
    except Exception as exc:  # noqa: BLE001 — surface a friendly error, don't 500
        logger.error("Campaign %s preview failed: %s", campaign_id, exc)
        return JsonResponse({"error": "render_failed"}, status=422)
    return JsonResponse({"html": resolve_preview(html)})


def _voucher_summary(voucher) -> str:
    """A one-line, human discount summary for a voucher picker card."""
    try:
        # float() strips a Decimal's trailing zeros (20.00 -> 20) for display.
        value = f"{float(voucher.discount_value):g}"
        if voucher.discount_type == "percentage":
            return f"{value}% off"
        if voucher.discount_type == "fixed":
            return f"{value} {voucher.currency} off"
        if voucher.discount_type == "gift_card":
            return "Gift card"
    except Exception:  # noqa: BLE001 — a summary must never break the picker
        pass
    return ""


@staff_member_required
@requires_category("marketing", "full", ajax=True)
@require_http_methods(["GET"])
def voucher_search(request):
    """Search active vouchers for the Discount Code block's picker.

    Returns a lightweight list (code + internal name + a human discount summary
    + expiry) so merchants pick an existing voucher instead of hand-typing a
    code. Select-existing only — voucher creation stays in the vouchers admin.
    """
    from django.db.models import Q

    from vouchers.models import VoucherCode

    q = (request.GET.get("search") or "").strip()
    qs = VoucherCode.objects.filter(is_active=True)
    if q:
        qs = qs.filter(Q(code__icontains=q) | Q(name__icontains=q))
    qs = qs.order_by("code")[:30]

    vouchers = [
        {
            "code": v.code,
            "name": v.name,
            "summary": _voucher_summary(v),
            "expiry": v.end_date.date().isoformat() if v.end_date else None,
        }
        for v in qs
    ]
    return JsonResponse({"vouchers": vouchers})


# ---------------------------------------------------------------------------
# Journey builder — node + edge CRUD for the flowchart canvas.
# ---------------------------------------------------------------------------


def _node_payload(node) -> dict:
    return {
        "id": str(node.id),
        "node_type": node.node_type,
        "pos_x": node.pos_x,
        "pos_y": node.pos_y,
        "config": node.config or {},
    }


def _edge_payload(edge) -> dict:
    return {
        "id": str(edge.id),
        "from": str(edge.from_node_id),
        "to": str(edge.to_node_id),
        "branch": edge.branch,
    }


def _clamp_pos(value) -> int:
    """Coerce a canvas coordinate to a bounded integer."""
    try:
        return max(-100_000, min(int(value), 100_000))
    except (TypeError, ValueError):
        return 0


def _is_uuid(value) -> bool:
    """True if ``value`` is a well-formed UUID string.

    Guards ``.filter(pk=...)`` on UUID primary keys — a non-UUID would otherwise
    raise ValidationError (an uncaught 500) rather than simply not matching.
    """
    import uuid

    try:
        uuid.UUID(str(value))
        return True
    except (ValueError, TypeError, AttributeError):
        return False


def _ab_metric(raw) -> str:
    return "clicks" if raw.get("ab_metric") == "clicks" else "opens"


def _same_ab_test(old, new) -> bool:
    """Whether two send configs describe the same A/B arms + metric, so a locked
    winner still applies. Any change to the test type, variants, or metric is a
    fresh test."""
    keys = ("ab_test_type", "ab_metric", "variant_campaign_ids", "campaign_id", "variant_subjects")
    return all((old or {}).get(k) == new.get(k) for k in keys)


def _carry_winner(old_config, new_config) -> dict:
    """Copy an engine-set winner from the old config to the new one, but ONLY when
    the A/B test is otherwise unchanged. Editing the variants or metric starts a
    fresh test, so a stale positional winner must not be applied to new arms."""
    if new_config.get("ab_test_type") and _same_ab_test(old_config, new_config):
        for key in ("ab_winner_label", "ab_winner_locked_at"):
            if (old_config or {}).get(key):
                new_config[key] = old_config[key]
    return new_config


def _reset_ab_sends_if_changed(node, old_config, new_config) -> None:
    """Delete a node's per-variant sends when its A/B test is redefined, so the
    fresh test — and the auto-optimiser — don't inherit the previous test's
    engagement under the same positional labels."""
    if (old_config or {}).get("ab_test_type") and not _same_ab_test(old_config, new_config):
        from .models import JourneyStepSend

        JourneyStepSend.objects.filter(node=node).delete()


def _sanitize_send_email_config(raw, site) -> dict:
    """Sanitize a send_email node's config: a single campaign, or an A/B test —
    content (2–4 real campaigns) or subject (a base campaign + 2–4 subject lines).

    Winner keys (``ab_winner_label`` / ``ab_winner_locked_at``) are engine-only and
    are never accepted from the client here; ``update_journey_node`` carries an
    existing winner across edits. An under-configured A/B falls back to a plain
    single-campaign node.
    """
    from .models import Campaign
    from .services.ab_testing import MAX_VARIANTS

    def _valid_campaign(cid):
        return bool(cid and _is_uuid(cid) and Campaign.objects.filter(pk=cid, site=site).exists())

    test_type = raw.get("ab_test_type")
    if test_type == "content":
        # Cap BEFORE the per-id existence query so a crafted list can't fan out
        # thousands of point lookups (the UI only ever sends the arms).
        raw_ids = (raw.get("variant_campaign_ids") or [])[:MAX_VARIANTS]
        ids = [str(c) for c in raw_ids if _valid_campaign(c)]
        if len(ids) >= 2:
            return {
                "ab_test_type": "content",
                "variant_campaign_ids": ids,
                "ab_metric": _ab_metric(raw),
            }
    elif test_type == "subject":
        base = raw.get("campaign_id")
        raw_subjects = (raw.get("variant_subjects") or [])[:MAX_VARIANTS]
        subjects = [s.strip()[:255] for s in raw_subjects if isinstance(s, str) and s.strip()]
        if _valid_campaign(base) and len(subjects) >= 2:
            return {
                "ab_test_type": "subject",
                "campaign_id": str(base),
                "variant_subjects": subjects,
                "ab_metric": _ab_metric(raw),
            }

    cid = raw.get("campaign_id")
    if _valid_campaign(cid):
        return {"campaign_id": str(cid)}
    return {}


def _sanitize_node_config(node_type, raw) -> dict:
    """Validate a node's config by type — drop unknown keys, bound values.

    A send node stores only a real Campaign id; a wait stores a bounded value +
    an allowed unit; a branch stores an allowed condition + a real Segment id.
    Anything else is dropped so a crafted payload can't smuggle data into config.
    """
    from django.contrib.sites.models import Site

    from .models import JourneyNode, Segment

    raw = raw if isinstance(raw, dict) else {}
    site = Site.objects.get(pk=1)

    if node_type == JourneyNode.TYPE_SEND_EMAIL:
        return _sanitize_send_email_config(raw, site)

    if node_type == JourneyNode.TYPE_WAIT_DELAY:
        try:
            value = int(raw.get("value", 0))
        except (TypeError, ValueError):
            value = 0
        value = max(0, min(value, 3650))
        unit = raw.get("unit")
        if unit not in (JourneyNode.UNIT_HOURS, JourneyNode.UNIT_DAYS):
            unit = JourneyNode.UNIT_DAYS
        return {"value": value, "unit": unit}

    if node_type == JourneyNode.TYPE_BRANCH:
        if raw.get("condition") == JourneyNode.CONDITION_IN_SEGMENT:
            sid = raw.get("segment_id")
            if sid and _is_uuid(sid) and Segment.objects.filter(pk=sid, site=site).exists():
                return {"condition": JourneyNode.CONDITION_IN_SEGMENT, "segment_id": str(sid)}
            return {"condition": JourneyNode.CONDITION_IN_SEGMENT}
        return {}

    return {}


@staff_member_required
@requires_category("marketing", "full", ajax=True)
@require_http_methods(["POST"])
def create_journey_node(request, journey_id):
    """Add a node to a journey's graph at a canvas position."""
    from .models import Journey, JourneyNode

    journey = get_object_or_404(Journey, id=journey_id)
    data = _json(request)
    node_type = data.get("node_type", "")
    valid_types = {t for t, _ in JourneyNode.TYPE_CHOICES}
    if node_type not in valid_types:
        return JsonResponse({"error": "unknown_node_type"}, status=400)
    # Bound graph size (parity with the import guard-rail in journey_io).
    from .services.journey_io import MAX_NODES

    if journey.nodes.count() >= MAX_NODES:
        return JsonResponse({"error": "too_many_nodes"}, status=409)
    # Exactly one entry node per journey — it is the graph's root.
    if (
        node_type == JourneyNode.TYPE_ENTRY
        and journey.nodes.filter(node_type=JourneyNode.TYPE_ENTRY).exists()
    ):
        return JsonResponse({"error": "entry_exists"}, status=409)

    node = JourneyNode.objects.create(
        journey=journey,
        node_type=node_type,
        pos_x=_clamp_pos(data.get("pos_x")),
        pos_y=_clamp_pos(data.get("pos_y")),
        config=_sanitize_node_config(node_type, data.get("config")),
    )
    return JsonResponse({"success": True, "node": _node_payload(node)})


@staff_member_required
@requires_category("marketing", "full", ajax=True)
@require_http_methods(["PATCH", "POST"])
def update_journey_node(request, node_id):
    """Move a node and/or update its type-validated config."""
    from .models import JourneyNode

    node = get_object_or_404(JourneyNode, id=node_id)
    data = _json(request)
    fields = []
    if "pos_x" in data:
        node.pos_x = _clamp_pos(data.get("pos_x"))
        fields.append("pos_x")
    if "pos_y" in data:
        node.pos_y = _clamp_pos(data.get("pos_y"))
        fields.append("pos_y")
    if "config" in data:
        old_config = node.config
        new_config = _sanitize_node_config(node.node_type, data.get("config"))
        # The auto-optimiser's winner is engine-only; carry it across edits only
        # while the A/B test itself is unchanged (a variant/metric change resets it).
        node.config = _carry_winner(old_config, new_config)
        _reset_ab_sends_if_changed(node, old_config, new_config)
        fields.append("config")
    if fields:
        node.save(update_fields=[*fields, "updated_at"])
    return JsonResponse({"success": True, "node": _node_payload(node)})


@staff_member_required
@requires_category("marketing", "full", ajax=True)
@require_http_methods(["DELETE", "POST"])
def delete_journey_node(request, node_id):
    """Remove a node (its edges cascade). The entry node can't be deleted."""
    from .models import JourneyNode

    node = get_object_or_404(JourneyNode, id=node_id)
    if node.node_type == JourneyNode.TYPE_ENTRY:
        return JsonResponse({"error": "cannot_delete_entry"}, status=400)
    node.delete()
    return JsonResponse({"success": True})


@staff_member_required
@requires_category("marketing", "full", ajax=True)
@require_http_methods(["POST"])
def create_journey_edge(request, journey_id):
    """Connect two of a journey's nodes along a branch path.

    Enforces graph sanity: both nodes belong to the journey, no self-loops, a
    valid branch label, and one edge per output (a linear node has a single
    ``default`` out-edge; a branch node has one ``yes`` and one ``no``).
    """
    from .models import Journey, JourneyEdge, JourneyNode

    journey = get_object_or_404(Journey, id=journey_id)
    data = _json(request)
    from_id, to_id = data.get("from"), data.get("to")
    if not from_id or not to_id or from_id == to_id:
        return JsonResponse({"error": "invalid_endpoints"}, status=400)

    nodes = {str(n.id): n for n in journey.nodes.all()}
    from_node, to_node = nodes.get(str(from_id)), nodes.get(str(to_id))
    if not from_node or not to_node:
        return JsonResponse({"error": "node_not_in_journey"}, status=400)

    branch = data.get("branch", JourneyEdge.BRANCH_DEFAULT)
    valid_branches = {b for b, _ in JourneyEdge.BRANCH_CHOICES}
    if branch not in valid_branches:
        return JsonResponse({"error": "invalid_branch"}, status=400)
    # Branch nodes route via yes/no; every other node uses a single default path.
    if from_node.node_type == JourneyNode.TYPE_BRANCH:
        if branch not in (JourneyEdge.BRANCH_YES, JourneyEdge.BRANCH_NO):
            return JsonResponse({"error": "branch_needs_yes_no"}, status=400)
    elif branch != JourneyEdge.BRANCH_DEFAULT:
        return JsonResponse({"error": "only_branch_nodes_split"}, status=400)
    # An exit node is terminal — it has no outputs.
    if from_node.node_type == JourneyNode.TYPE_EXIT:
        return JsonResponse({"error": "exit_has_no_output"}, status=400)

    # One edge per output slot: replace any existing edge on this branch label.
    JourneyEdge.objects.filter(from_node=from_node, branch=branch).delete()
    edge = JourneyEdge.objects.create(
        journey=journey, from_node=from_node, to_node=to_node, branch=branch
    )
    return JsonResponse({"success": True, "edge": _edge_payload(edge)})


@staff_member_required
@requires_category("marketing", "full", ajax=True)
@require_http_methods(["DELETE", "POST"])
def delete_journey_edge(request, edge_id):
    """Remove a connection between two nodes."""
    from .models import JourneyEdge

    edge = get_object_or_404(JourneyEdge, id=edge_id)
    edge.delete()
    return JsonResponse({"success": True})


def _graph_payload(journey) -> dict:
    """The whole graph in the builder's shape, for a post-import canvas refresh."""
    return {
        "nodes": [_node_payload(n) for n in journey.nodes.all()],
        "edges": [_edge_payload(e) for e in journey.edges.all()],
    }


# ---------------------------------------------------------------------------
# Journey starters + import/export (sharing).
# ---------------------------------------------------------------------------


@staff_member_required
@requires_category("marketing", "full", ajax=True)
@require_http_methods(["GET"])
def list_journey_templates(request):
    """The starter catalogue for the "start from a template" picker."""
    from .journey_templates import get_starters

    return JsonResponse({"templates": get_starters()})


@staff_member_required
@requires_category("marketing", "full", ajax=True)
@require_http_methods(["POST"])
def apply_journey_template(request, journey_id):
    """Replace a journey's graph with a starter, re-linking emails/segments by name."""
    from .journey_templates import get_starter_doc
    from .models import Journey
    from .services.journey_io import JourneyImportError, import_into_journey

    journey = get_object_or_404(Journey, id=journey_id)
    doc = get_starter_doc(_json(request).get("template_key"))
    if doc is None:
        return JsonResponse({"error": "unknown_template"}, status=400)
    try:
        stats = import_into_journey(journey, doc, replace=True)
    except JourneyImportError as exc:
        return JsonResponse({"error": str(exc)}, status=422)
    return JsonResponse({"success": True, "graph": _graph_payload(journey), "stats": stats})


@staff_member_required
@requires_category("marketing", "full", ajax=True)
@require_http_methods(["GET"])
def export_journey(request, journey_id):
    """Download a journey as a portable share document (flow shape + names)."""
    from django.utils.text import slugify

    from .models import Journey
    from .services.journey_io import export_journey as export_doc

    journey = get_object_or_404(Journey, id=journey_id)
    doc = export_doc(journey)
    response = JsonResponse(doc, json_dumps_params={"indent": 2})
    filename = (slugify(journey.name) or "journey") + ".journey.json"
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


@staff_member_required
@requires_category("marketing", "full", ajax=True)
@require_http_methods(["POST"])
def import_journey(request, journey_id):
    """Rebuild a journey's graph from an uploaded share document."""
    from .models import Journey
    from .services.journey_io import JourneyImportError, import_into_journey

    journey = get_object_or_404(Journey, id=journey_id)
    doc = _json(request).get("doc")
    try:
        stats = import_into_journey(journey, doc, replace=True)
    except JourneyImportError as exc:
        return JsonResponse({"error": str(exc)}, status=422)
    return JsonResponse({"success": True, "graph": _graph_payload(journey), "stats": stats})


# ---------------------------------------------------------------------------
# Journey live stats + validation + activation gate.
# ---------------------------------------------------------------------------


@staff_member_required
@requires_category("marketing", "full", ajax=True)
@require_http_methods(["GET"])
def journey_node_stats(request, journey_id):
    """Live per-node occupancy counts, plus per-variant A/B engagement for any
    A/B send steps (open/click rate per arm + confidence + the locked winner)."""
    from django.db.models import Count

    from .models import Journey, JourneyEnrollment, JourneyNode

    journey = get_object_or_404(Journey, id=journey_id)
    rows = (
        JourneyEnrollment.objects.filter(
            journey=journey,
            status=JourneyEnrollment.STATUS_ACTIVE,
            current_node__isnull=False,
        )
        .values("current_node")
        .annotate(c=Count("id"))
    )
    counts = {str(r["current_node"]): r["c"] for r in rows}

    ab = {}
    for node in journey.nodes.filter(node_type=JourneyNode.TYPE_SEND_EMAIL):
        if node.is_ab_send:
            ab[str(node.id)] = _journey_ab_summary(node)
    return JsonResponse({"counts": counts, "ab": ab})


def _journey_ab_summary(node) -> dict:
    """Per-variant rates + confidence + winner for one A/B send node."""
    from .services.ab_stats import assess
    from .services.journeys import variant_arms

    arms = variant_arms(node)
    leader = max(arms, key=lambda a: a.rate(node.ab_metric))
    result = assess(leader, arms, node.ab_metric)

    def _rate(wins, n):
        return round(100 * wins / n, 1) if n else 0.0

    return {
        "metric": node.ab_metric,
        "winner": node.ab_winner_label,
        "confidence": round(result["confidence"] * 100, 1) if result["reliable"] else None,
        "variants": [
            {
                "label": a.label,
                "recipients": a.recipients,
                "open_rate": _rate(a.opened, a.recipients),
                "click_rate": _rate(a.clicked, a.recipients),
            }
            for a in arms
        ],
    }


@staff_member_required
@requires_category("marketing", "full", ajax=True)
@require_http_methods(["GET"])
def validate_journey_view(request, journey_id):
    """Report graph issues (errors block activation; warnings are advisory)."""
    from .models import Journey
    from .services.journey_validation import can_activate, validate_journey

    journey = get_object_or_404(Journey, id=journey_id)
    issues = validate_journey(journey)
    return JsonResponse({"issues": issues, "can_activate": can_activate(issues)})


@staff_member_required
@requires_category("marketing", "full", ajax=True)
@require_http_methods(["POST"])
def set_journey_status(request, journey_id):
    """Change a journey's status. Activation is gated on passing validation.

    Going Active runs :func:`validate_journey` first; if there are error-level
    issues the status is left unchanged and the issues are returned so the canvas
    can highlight them. Draft/Paused transitions always apply.
    """
    from .models import Journey
    from .services.journey_validation import can_activate, validate_journey

    journey = get_object_or_404(Journey, id=journey_id)
    status = _json(request).get("status")
    valid = {Journey.STATUS_DRAFT, Journey.STATUS_ACTIVE, Journey.STATUS_PAUSED}
    if status not in valid:
        return JsonResponse({"error": "invalid_status"}, status=400)

    issues = []
    if status == Journey.STATUS_ACTIVE:
        issues = validate_journey(journey)
        if not can_activate(issues):
            # Blocked, not an error: return 200 so the canvas can show the issues.
            return JsonResponse(
                {
                    "success": False,
                    "blocked": True,
                    "status": journey.status,
                    "status_display": journey.get_status_display(),
                    "issues": issues,
                }
            )

    journey.status = status
    journey.save(update_fields=["status", "updated_at"])
    return JsonResponse(
        {
            "success": True,
            "status": journey.status,
            "status_display": journey.get_status_display(),
            "issues": issues,
        }
    )
