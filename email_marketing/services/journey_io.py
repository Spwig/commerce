"""Portable import/export for journeys — the format behind sharing + starters.

A journey is exported to a self-describing document that carries the flow's
*shape* (steps, waits, branches, Yes/No paths and canvas layout) plus the
*names* of the emails and segments each step used — never their install-specific
ids. On import the shape is rebuilt and each email/segment is re-linked by name
where a local match exists; anything unmatched is left for the merchant to pick.

The same document is what a template starter is, so ``apply_template`` and a
user-uploaded share file both flow through :func:`import_into_journey`.
"""

import logging

from django.db import transaction

logger = logging.getLogger("email_marketing")

FORMAT_KEY = "spwig_journey"
FORMAT_VERSION = 1

# Import guard-rails — a shared file is untrusted input.
MAX_NODES = 200
MAX_EDGES = 400
MAX_WAIT = 3650


class JourneyImportError(ValueError):
    """Raised when a share document can't be understood or is unsafe."""


def _campaign_name(site, campaign_id):
    from email_marketing.models import Campaign

    if not campaign_id:
        return None
    c = Campaign.objects.filter(pk=campaign_id, site=site).only("name").first()
    return c.name if c else None


def _segment_name(site, segment_id):
    from email_marketing.models import Segment

    if not segment_id:
        return None
    s = Segment.objects.filter(pk=segment_id, site=site).only("name").first()
    return s.name if s else None


def export_journey(journey) -> dict:
    """Serialise a journey's graph to the portable share document."""
    nodes = list(journey.nodes.all())
    key_by_id = {n.id: f"n{i}" for i, n in enumerate(nodes)}

    out_nodes = []
    for n in nodes:
        cfg = n.config or {}
        item = {
            "key": key_by_id[n.id],
            "node_type": n.node_type,
            "pos_x": n.pos_x,
            "pos_y": n.pos_y,
            "config": _portable_config(n.node_type, cfg),
        }
        if n.node_type == "send_email":
            name = _campaign_name(journey.site, cfg.get("campaign_id"))
            if name:
                item["campaign_name"] = name
        elif n.node_type == "branch":
            name = _segment_name(journey.site, cfg.get("segment_id"))
            if name:
                item["segment_name"] = name
        out_nodes.append(item)

    out_edges = [
        {"from": key_by_id[e.from_node_id], "to": key_by_id[e.to_node_id], "branch": e.branch}
        for e in journey.edges.all()
    ]

    return {
        FORMAT_KEY: FORMAT_VERSION,
        "name": journey.name,
        "trigger_event": journey.trigger_event,
        "nodes": out_nodes,
        "edges": out_edges,
    }


def _portable_config(node_type, cfg) -> dict:
    """The config values that travel — install-specific ids are dropped."""
    if node_type == "wait_delay":
        try:
            value = int(cfg.get("value") or 0)
        except (TypeError, ValueError):
            value = 0
        unit = cfg.get("unit") if cfg.get("unit") in ("hours", "days") else "days"
        return {"value": max(0, min(value, MAX_WAIT)), "unit": unit}
    if node_type == "branch" and cfg.get("condition"):
        return {"condition": cfg.get("condition")}
    return {}


def _clamp_pos(value) -> int:
    try:
        return max(-100_000, min(int(value), 100_000))
    except (TypeError, ValueError):
        return 0


def _resolve_config(journey, node_type, raw):
    """Rebuild a node's config from a share item, re-linking names to local ids."""
    from email_marketing.models import Campaign, JourneyNode, Segment

    cfg = raw.get("config") if isinstance(raw.get("config"), dict) else {}

    if node_type == JourneyNode.TYPE_SEND_EMAIL:
        name = raw.get("campaign_name")
        if name:
            c = Campaign.objects.filter(site=journey.site, name=name).only("id").first()
            if c:
                return {"campaign_id": str(c.id)}
        return {}

    if node_type == JourneyNode.TYPE_WAIT_DELAY:
        return _portable_config(node_type, cfg)

    if node_type == JourneyNode.TYPE_BRANCH:
        out = {}
        if cfg.get("condition") == JourneyNode.CONDITION_IN_SEGMENT:
            out["condition"] = JourneyNode.CONDITION_IN_SEGMENT
            name = raw.get("segment_name")
            if name:
                s = Segment.objects.filter(site=journey.site, name=name).only("id").first()
                if s:
                    out["segment_id"] = str(s.id)
        return out

    return {}


def import_into_journey(journey, doc, *, replace=True) -> dict:
    """Validate a share document and (re)build ``journey``'s graph from it.

    Returns ``{"nodes": n, "edges": m, "unmatched": k}`` where ``unmatched`` is
    how many send/branch steps couldn't be re-linked to a local email/segment.
    Raises :class:`JourneyImportError` on an unrecognised or unsafe document.
    """
    from email_marketing.models import JourneyEdge, JourneyNode

    if not isinstance(doc, dict) or doc.get(FORMAT_KEY) != FORMAT_VERSION:
        raise JourneyImportError("unrecognised_format")
    raw_nodes = doc.get("nodes")
    raw_edges = doc.get("edges") or []
    if not isinstance(raw_nodes, list) or not isinstance(raw_edges, list):
        raise JourneyImportError("bad_shape")
    if len(raw_nodes) > MAX_NODES or len(raw_edges) > MAX_EDGES:
        raise JourneyImportError("too_large")

    valid_types = {t for t, _ in JourneyNode.TYPE_CHOICES}
    valid_branches = {b for b, _ in JourneyEdge.BRANCH_CHOICES}

    unmatched = 0
    with transaction.atomic():
        if replace:
            journey.nodes.all().delete()  # cascades edges

        node_by_key = {}
        has_entry = False
        for raw in raw_nodes:
            if not isinstance(raw, dict):
                continue
            nt = raw.get("node_type")
            if nt not in valid_types:
                continue
            if nt == JourneyNode.TYPE_ENTRY:
                if has_entry:
                    continue  # exactly one entry
                has_entry = True
            config = _resolve_config(journey, nt, raw)
            if nt == JourneyNode.TYPE_SEND_EMAIL and not config.get("campaign_id"):
                unmatched += 1
            if nt == JourneyNode.TYPE_BRANCH and not config.get("segment_id"):
                unmatched += 1
            node = JourneyNode.objects.create(
                journey=journey,
                node_type=nt,
                pos_x=_clamp_pos(raw.get("pos_x")),
                pos_y=_clamp_pos(raw.get("pos_y")),
                config=config,
            )
            key = raw.get("key")
            if isinstance(key, str):
                node_by_key[key] = node

        # Every journey needs its single entry node.
        if not has_entry:
            JourneyNode.objects.create(
                journey=journey, node_type=JourneyNode.TYPE_ENTRY, pos_x=340, pos_y=40
            )

        edge_count = 0
        used_slots = set()  # (from_node_id, branch) — one edge per output slot
        for raw in raw_edges:
            if not isinstance(raw, dict):
                continue
            a = node_by_key.get(raw.get("from"))
            b = node_by_key.get(raw.get("to"))
            if not a or not b or a.id == b.id:
                continue
            branch = raw.get("branch", JourneyEdge.BRANCH_DEFAULT)
            if branch not in valid_branches:
                continue
            # Respect the same graph-sanity rules the live editor enforces.
            if a.node_type == JourneyNode.TYPE_EXIT:
                continue
            if a.node_type == JourneyNode.TYPE_BRANCH:
                if branch not in (JourneyEdge.BRANCH_YES, JourneyEdge.BRANCH_NO):
                    continue
            elif branch != JourneyEdge.BRANCH_DEFAULT:
                continue
            slot = (a.id, branch)
            if slot in used_slots:
                continue
            used_slots.add(slot)
            JourneyEdge.objects.create(journey=journey, from_node=a, to_node=b, branch=branch)
            edge_count += 1

    logger.info(
        "Imported graph into journey %s: %d nodes, %d edges, %d unmatched",
        journey.pk,
        len(node_by_key),
        edge_count,
        unmatched,
    )
    return {"nodes": len(node_by_key), "edges": edge_count, "unmatched": unmatched}
