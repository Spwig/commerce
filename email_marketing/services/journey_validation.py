"""Graph validation for journeys — what must be true before one can go live.

``validate_journey`` returns a flat list of issues, each tagged ``error`` or
``warning`` and (where relevant) anchored to a node so the canvas can highlight
it. Errors block activation; warnings are advisory. Keeping this in one named
service means the Activate gate, the canvas "check" affordance, and tests all
judge a journey the same way.
"""


def _resolve_existing(nodes):
    """Return the sets of campaign/segment ids (as str) referenced by ``nodes``
    that still exist, via the default managers — one query each, no N+1."""
    from email_marketing.models import Campaign, JourneyNode, Segment

    campaign_ids = set()
    for n in nodes:
        if n.node_type != JourneyNode.TYPE_SEND_EMAIL:
            continue
        cfg = n.config or {}
        if cfg.get("campaign_id"):
            campaign_ids.add(cfg["campaign_id"])
        campaign_ids.update(c for c in (cfg.get("variant_campaign_ids") or []) if c)
    segment_ids = {
        (n.config or {}).get("segment_id")
        for n in nodes
        if n.node_type == JourneyNode.TYPE_BRANCH and (n.config or {}).get("segment_id")
    }
    existing_campaigns = (
        {
            str(pk)
            for pk in Campaign.objects.filter(pk__in=campaign_ids).values_list("pk", flat=True)
        }
        if campaign_ids
        else set()
    )
    existing_segments = (
        {str(pk) for pk in Segment.objects.filter(pk__in=segment_ids).values_list("pk", flat=True)}
        if segment_ids
        else set()
    )
    return existing_campaigns, existing_segments


def _has_cycle(entry_id, out_by_node) -> bool:
    """Iterative DFS three-colouring — True if a cycle is reachable from entry."""
    WHITE, GREY, BLACK = 0, 1, 2
    color = {}
    color[entry_id] = GREY
    stack = [(entry_id, iter(out_by_node.get(entry_id, [])))]
    while stack:
        nid, it = stack[-1]
        advanced = False
        for edge in it:
            target = edge.to_node_id
            c = color.get(target, WHITE)
            if c == GREY:
                return True
            if c == WHITE:
                color[target] = GREY
                stack.append((target, iter(out_by_node.get(target, []))))
                advanced = True
                break
        if not advanced:
            color[nid] = BLACK
            stack.pop()
    return False


def _send_email_issues(node, cfg, existing_campaigns) -> list[dict]:
    """Issues for a send step — single email, content A/B, or subject A/B."""
    nid = str(node.id)

    def err(message):
        return {"level": "error", "message": message, "node_id": nid}

    test_type = cfg.get("ab_test_type")
    if test_type == "content":
        ids = [c for c in (cfg.get("variant_campaign_ids") or []) if c]
        if len(ids) < 2:
            return [err("An A/B “Send email” step needs at least two email variants.")]
        if any(cid not in existing_campaigns for cid in ids):
            return [err("An A/B “Send email” step points to an email that no longer exists.")]
        return []
    if test_type == "subject":
        out = []
        cid = cfg.get("campaign_id")
        if not cid:
            out.append(err("An A/B “Send email” step has no email chosen."))
        elif cid not in existing_campaigns:
            out.append(err("An A/B “Send email” step points to an email that no longer exists."))
        if len([s for s in (cfg.get("variant_subjects") or []) if str(s).strip()]) < 2:
            out.append(err("An A/B subject-line step needs at least two subject lines."))
        return out
    cid = cfg.get("campaign_id")
    if not cid:
        return [err("A “Send email” step has no email chosen.")]
    if cid not in existing_campaigns:
        return [err("A “Send email” step points to an email that no longer exists.")]
    return []


def validate_journey(journey) -> list[dict]:
    """Return graph issues for ``journey``. Empty ⇒ safe to activate.

    Each issue is ``{"level": "error"|"warning", "message": str, "node_id": str|None}``.
    """
    from email_marketing.models import JourneyEdge, JourneyNode

    nodes = list(journey.nodes.all())
    edges = list(journey.edges.all())
    issues: list[dict] = []

    entry = next((n for n in nodes if n.node_type == JourneyNode.TYPE_ENTRY), None)
    if entry is None:
        issues.append({"level": "error", "message": "The journey has no start.", "node_id": None})
        return issues

    out_by_node: dict = {}
    for e in edges:
        out_by_node.setdefault(e.from_node_id, []).append(e)

    if not out_by_node.get(entry.id):
        issues.append(
            {
                "level": "error",
                "message": "Nothing happens after the start — connect a step.",
                "node_id": str(entry.id),
            }
        )

    # Which referenced emails/segments still exist — batched (avoids N+1) and via
    # the default manager, so a since-deleted target reads as missing here just as
    # it does at send time. A stale UUID left in config must block activation.
    existing_campaigns, existing_segments = _resolve_existing(nodes)

    for n in nodes:
        cfg = n.config or {}
        if n.node_type == JourneyNode.TYPE_SEND_EMAIL:
            issues.extend(_send_email_issues(n, cfg, existing_campaigns))
        if n.node_type == JourneyNode.TYPE_BRANCH:
            sid = cfg.get("segment_id")
            if not sid:
                issues.append(
                    {
                        "level": "error",
                        "message": "A “Branch” step has no segment chosen.",
                        "node_id": str(n.id),
                    }
                )
            elif sid not in existing_segments:
                issues.append(
                    {
                        "level": "error",
                        "message": "A “Branch” step points to a segment that no longer exists.",
                        "node_id": str(n.id),
                    }
                )
            branch_labels = {e.branch for e in out_by_node.get(n.id, [])}
            has_yes = JourneyEdge.BRANCH_YES in branch_labels
            has_no = JourneyEdge.BRANCH_NO in branch_labels
            if not has_yes and not has_no:
                issues.append(
                    {
                        "level": "error",
                        "message": "A “Branch” step has no Yes or No path.",
                        "node_id": str(n.id),
                    }
                )
            elif not has_yes or not has_no:
                issues.append(
                    {
                        "level": "warning",
                        "message": "A “Branch” step is missing one of its Yes / No paths.",
                        "node_id": str(n.id),
                    }
                )
        if n.node_type == JourneyNode.TYPE_WAIT_DELAY and not cfg.get("value"):
            issues.append(
                {
                    "level": "warning",
                    "message": "A “Wait” step has no delay set — it won't pause.",
                    "node_id": str(n.id),
                }
            )

    # Reachability from the entry node.
    reachable = set()
    stack = [entry.id]
    while stack:
        nid = stack.pop()
        if nid in reachable:
            continue
        reachable.add(nid)
        for e in out_by_node.get(nid, []):
            stack.append(e.to_node_id)

    for n in nodes:
        if n.id not in reachable:
            issues.append(
                {
                    "level": "warning",
                    "message": f"This “{n.get_node_type_display()}” step can't be reached from the start.",
                    "node_id": str(n.id),
                }
            )

    # A cycle would loop a subscriber indefinitely — block activation. (The
    # runtime also cancels an enrollment that hits the hop cap, for graphs built
    # outside the editor, e.g. via import.)
    if _has_cycle(entry.id, out_by_node):
        issues.append(
            {
                "level": "error",
                "message": "The journey loops back on itself — remove the loop.",
                "node_id": None,
            }
        )

    return issues


def can_activate(issues) -> bool:
    """A journey may go live when it has no error-level issues (warnings are ok)."""
    return not any(i["level"] == "error" for i in issues)
