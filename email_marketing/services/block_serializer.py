"""Serialise a campaign's block tree into MJML, and render blocks for the canvas.

The visual builder edits ordered ``CampaignBlock`` rows. ``serialize_campaign``
walks them, renders each block's ``email.mjml`` partial with its content, wraps
the result in an ``<mjml>`` document, and stores it on ``Campaign.html_content``
— so the existing (P0) send path renders and delivers it with no changes.

``render_block_canvas`` renders a single block's ``canvas.html`` for live
editing (styled by the shop's frontend theme tokens inside the isolated canvas).
"""

import json
import logging
import re

from django.template.loader import render_to_string

from email_marketing.block_context import get_block_context
from email_marketing.block_registry import get_block, sanitize_content
from email_marketing.merge_fields import resolve_preview

logger = logging.getLogger("email_marketing")


def _derive_style_context(content: dict) -> dict:
    """Turn the utility editors' CSS-string values into MJML-ready attributes.

    The Style-tab controls store the CSS the shared editors emit (padding
    shorthand, border-* declarations). MJML wants discrete attribute values, so
    parse them here into ``mj_padding`` / ``mj_border`` / ``mj_radius`` that the
    section partial consumes. ``section_bg`` is already a plain colour.
    """
    ctx: dict = {}

    padding = (content.get("padding") or "").strip()
    if padding:
        # "padding: 16px 0px" -> "16px 0px"
        padding = re.sub(r"^padding:\s*", "", padding, flags=re.I).rstrip(";").strip()
    ctx["mj_padding"] = padding or "16px 0"

    border = (content.get("border") or "").strip()
    if border:
        width = re.search(r"border-width:\s*([^;\n]+)", border, re.I)
        style = re.search(r"border-style:\s*([^;\n]+)", border, re.I)
        color = re.search(r"border-color:\s*([^;\n]+)", border, re.I)
        radius = re.search(r"border-radius:\s*([^;\n]+)", border, re.I)
        if width and style and color:
            # Use the first token of each (linked sides) — email borders are uniform.
            ctx["mj_border"] = (
                f"{width.group(1).split()[0]} "
                f"{style.group(1).split()[0]} "
                f"{color.group(1).split()[0]}"
            )
        elif re.match(r"^\d", border):
            # Shorthand fallback like "1px solid #000".
            ctx["mj_border"] = border.split(";")[0].strip()
        if radius:
            ctx["mj_radius"] = radius.group(1).split()[0]

    return ctx


# Map TypographyEditor settings -> template context keys used by text/heading.
_TYPO_MAP = {
    "typo_family": "fontFamily",
    "typo_size": "fontSize",
    "typo_weight": "fontWeight",
    "typo_lh": "lineHeight",
    "typo_ls": "letterSpacing",
    "typo_align": "textAlign",
    "typo_color": "color",
    "typo_style": "fontStyle",
    "typo_transform": "textTransform",
    "typo_decoration": "textDecoration",
}


def _derive_typography_context(content: dict) -> dict:
    """Expose sanitized typography settings as ``typo_*`` template variables."""
    typo = content.get("typography") or {}
    if isinstance(typo, str):
        try:
            typo = json.loads(typo)
        except (ValueError, TypeError):
            typo = {}
    if not isinstance(typo, dict):
        return {}
    ctx = {}
    for out_key, in_key in _TYPO_MAP.items():
        value = typo.get(in_key)
        if value and value not in ("inherit", "currentColor"):
            ctx[out_key] = value
    return ctx


def _neutralize_template_syntax(text: str) -> str:
    """Break Django template delimiters so block content can't be executed.

    Block content is literal text, but the send path re-renders the compiled
    HTML through Django's Template engine to substitute merge tags. Without this,
    a ``{% ... %}`` or ``{{ ... }}`` typed into a block would execute at send
    time (SSTI). Replacing a brace with its HTML entity keeps the visible text
    identical (entities decode to '{'/'}') while defeating the template parser.
    Percent signs are untouched, so "50% off" is unaffected.
    """
    return (
        text.replace("{{", "&#123;&#123;")
        .replace("}}", "&#125;&#125;")
        .replace("{%", "&#123;%")
        .replace("%}", "%&#125;")
    )


# MJML document scaffold. Blocks render as <mj-*> children of a single column.
# Each block renders its OWN <mj-section> so blocks can span multiple columns
# (e.g. a product grid). The body just frames the 600px canvas.
_MJML_HEAD = '<mjml><mj-body background-color="#f4f4f4" width="600px">'
_MJML_TAIL = "</mj-body></mjml>"


def _render_ctx(block, extra_ctx=None) -> dict:
    """Render state for context-aware blocks.

    The ``since`` watermark (the campaign's ``last_content_sent_at``) so a "new since
    last send" Blog Posts block only pulls fresh posts, merged with any per-send
    ``extra_ctx`` (e.g. a triggered journey's event payload + subscriber, so an
    abandoned-cart block can resolve that subscriber's live cart).
    """
    campaign = getattr(block, "campaign", None)
    ctx = {"since": getattr(campaign, "last_content_sent_at", None)}
    if extra_ctx:
        ctx.update(extra_ctx)
    return ctx


def render_block_mjml(block, extra_ctx=None) -> str:
    """Render one block's MJML partial with sanitised content (SSTI-neutralised)."""
    cfg = get_block(block.block_type)
    if not cfg:
        logger.warning("Unknown email block type: %s", block.block_type)
        return ""
    ctx = sanitize_content(cfg, block.content or {})
    ctx.update(_derive_style_context(ctx))
    ctx.update(_derive_typography_context(ctx))
    ctx.update(get_block_context(block.block_type, ctx, _render_ctx(block, extra_ctx)))
    return _neutralize_template_syntax(render_to_string(cfg.mjml_template, ctx))


def render_block_canvas(block) -> str:
    """Render one block's canvas (admin-side live-edit) HTML with sanitised content."""
    cfg = get_block(block.block_type)
    if not cfg:
        return ""
    ctx = sanitize_content(cfg, block.content or {})
    ctx.update(_derive_typography_context(ctx))
    ctx.update(get_block_context(block.block_type, ctx, _render_ctx(block)))
    html = render_to_string(cfg.canvas_template, ctx)
    # Show merge fields as highlighted sample values so the merchant previews
    # the personalised result (the email substitutes real per-recipient values).
    return resolve_preview(html)


def serialize_campaign(campaign, extra_ctx=None) -> str:
    """Return the full MJML document for a campaign's ordered blocks.

    ``extra_ctx`` is per-send render state (e.g. a triggered journey's event payload +
    subscriber). Pass it to re-serialize a campaign for one recipient so per-subscriber
    dynamic blocks (an abandoned-cart block) resolve live; omit it for the shared
    broadcast serialization saved to ``html_content``.
    """
    parts = [render_block_mjml(block, extra_ctx) for block in campaign.blocks.all()]
    body = "\n".join(p for p in parts if p.strip())
    return f"{_MJML_HEAD}\n{body}\n{_MJML_TAIL}"


def save_campaign_html(campaign) -> str:
    """Serialise blocks to MJML and persist to Campaign.html_content. Returns MJML."""
    mjml = serialize_campaign(campaign)
    campaign.html_content = mjml
    campaign.save(update_fields=["html_content", "updated_at"])
    return mjml
