"""Personalized (per-visitor) navigation resolution.

Deferred nav — a header/footer widget placement whose visibility depends on a
per-visitor rule, or a menu widget carrying such an item — is emitted as a
content-less placeholder in the cacheable shell (see design.templatetags.
theme_tags). This service renders the actual widget for the requesting visitor,
evaluating the per-visitor rules against their real session, and only ever for a
placement that is genuinely part of the site's live navigation (the IDOR guard).
"""

import logging

from django.db.models import Q
from django.template.loader import render_to_string

from ..header_footer_models import WidgetPlacement

logger = logging.getLogger(__name__)

# The whole nav has a handful of placements; cap what one request can trigger.
MAX_NAV_PLACEMENTS = 40

_RENDER_TEMPLATE = "design/partials/render_deferred_widget.html"


def _active_nav_placement(placement_id):
    """Return the widget placement iff it is part of an ACTIVE header or footer —
    the site's live navigation. Bounds the id space so a client can't probe or
    render arbitrary placements (the ownership/IDOR guard). Single-tenant: the one
    site's active header/footer are the only legitimate nav containers.
    """
    try:
        pid = int(placement_id)
    except (ValueError, TypeError):
        return None
    return (
        WidgetPlacement.objects.filter(is_active=True, widget__is_active=True)
        .filter(Q(header__is_active=True) | Q(footer__is_active=True))
        .select_related("widget", "header", "footer")
        .filter(pk=pid)
        .first()
    )


def resolve_personalized_nav(request, widget_placement_ids):
    """Render the deferred nav widgets this visitor is entitled to see.

    Returns ``{str(placement_id): html_or_None}`` — every requested id maps to
    html or ``None`` (never absent), so a caller can't distinguish "not a live-nav
    placement" from "not entitled" (removes an enumeration oracle). A placement is
    rendered only if it is part of the site's active navigation AND the visitor
    passes its full visibility (per-visitor rules evaluated with the real session).
    Menu/account widgets render only the items this visitor is entitled to.
    """
    # Full-visibility mode: theme_tags.render_widget then evaluates per-visitor
    # rules and renders the real widget (not another placeholder), and menu items
    # at every depth are filtered against the visitor's real context (nested
    # per-visitor items are gated too — see theme_tags._annotate_visible_children).
    request._nav_full_visibility = True

    result = {str(pid): None for pid in widget_placement_ids}
    for pid in widget_placement_ids:
        placement = _active_nav_placement(pid)
        if placement is None:
            continue  # not part of the live nav — reject (stays None)
        try:
            html = render_to_string(_RENDER_TEMPLATE, {"placement": placement}, request=request)
        except Exception:
            logger.exception("personalize-nav: failed rendering placement %s", pid)
            html = None
        result[str(pid)] = html.strip() if html and html.strip() else None
    return result
