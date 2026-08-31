"""Email-block registry — filesystem-discovered block definitions.

Adapts page_builder's config.json-per-block pattern (a block is a folder under
``email_marketing/blocks/<type>/`` holding ``config.json``, ``email.mjml``, and
``canvas.html``) but is deliberately lean: a flat property schema, no base-merge,
and email-appropriate blocks only.

``config.json`` shape::

    {
        "block_type": "heading",
        "name": "Heading",
        "icon": "fas fa-heading",
        "category": "content",
        "properties": {
            "text": {"type": "string", "label": "Text", "default": "…", "translatable": true},
            "level": {"type": "select", "label": "Level", "default": "h2",
                       "options": [{"value": "h1", "label": "H1"}, …]}
        },
        "defaults": {"text": "…", "level": "h2"}
    }
"""

import json
import logging
import re
from functools import lru_cache
from pathlib import Path

from django.conf import settings

logger = logging.getLogger("email_marketing")

# URL schemes allowed in link/image fields — blocks javascript:, data:, etc.
_SAFE_URL_SCHEMES = ("http://", "https://", "mailto:", "tel:")
_COLOR_RE = re.compile(r"^(#[0-9a-fA-F]{3,8}|rgba?\([0-9.,%\s]+\)|[a-zA-Z]{3,20})$")
# CSS-string values from the utility editors. Deliberately allow ONLY the
# characters those declarations need — no `<`, `>`, or quotes — so the values
# can't break out of the MJML attribute they land in (autoescape is a second
# line of defence). Length-capped to bound pathological input.
_SPACING_RE = re.compile(r"^(padding:\s*)?[\d.\sa-z%-]{1,60}$", re.I)
_BORDER_RE = re.compile(r"^[\d.\sa-z%#(),:;-]{1,200}$", re.I)
# Typography sub-value validators.
_SIZE_RE = re.compile(r"^[\d.]+(px|em|rem|%)?$|^normal$", re.I)  # size / line-height / spacing
_FONT_FAMILY_RE = re.compile(r"^[a-zA-Z0-9 ,'\"-]{1,120}$")
_FONT_WEIGHTS = {*(str(w) for w in range(100, 1000, 100)), "normal", "bold", "bolder", "lighter"}
_TEXT_ALIGNS = {"left", "center", "right", "justify"}
_FONT_STYLES = {"normal", "italic", "oblique"}
_TEXT_TRANSFORMS = {"none", "uppercase", "lowercase", "capitalize"}
_TEXT_DECORATIONS = {"none", "underline", "line-through", "overline"}


def _safe_url(value) -> str:
    """Return the URL if it uses a safe scheme (or is relative/anchor), else ''."""
    v = (value or "").strip() if isinstance(value, str) else ""
    if not v:
        return ""
    low = v.lower()
    if low.startswith(("/", "#")):
        return v
    if any(low.startswith(scheme) for scheme in _SAFE_URL_SCHEMES):
        return v
    return ""


def _safe_product_id(value) -> str:
    """Return a positive integer product id (as a string), else ''.

    The product picker stores the chosen product's id; block_context coerces it
    back with int(), so we only need to guarantee it's a positive integer and
    never free text that could reach a template unescaped.
    """
    try:
        n = int(str(value).strip())
    except (TypeError, ValueError):
        return ""
    return str(n) if n > 0 else ""


def _safe_color(value) -> str:
    """Return the colour if it matches a hex/rgb(a)/named form, else ''."""
    v = (value or "").strip() if isinstance(value, str) else ""
    return v if _COLOR_RE.match(v) else ""


def _safe_spacing(value) -> str:
    """Validate a SpacingEditor value (a padding shorthand / declaration)."""
    v = (value or "").strip() if isinstance(value, str) else ""
    return v if v and _SPACING_RE.match(v) else ""


def _safe_border(value) -> str:
    """Validate a BorderEditor value (border-* declarations / shorthand)."""
    v = (value or "").strip() if isinstance(value, str) else ""
    return v if v and _BORDER_RE.match(v) else ""


def _safe_typography(value) -> dict:
    """Validate a TypographyEditor settings object; keep only safe known keys.

    Accepts the settings dict or its JSON string. Every value is validated
    against a tight pattern/allow-set before it can reach an MJML/CSS attribute.
    """
    if isinstance(value, str):
        try:
            value = json.loads(value or "{}")
        except (ValueError, TypeError):
            return {}
    if not isinstance(value, dict):
        return {}

    out: dict = {}

    def keep(key, predicate):
        v = value.get(key)
        if isinstance(v, str) and predicate(v):
            out[key] = v

    keep("fontFamily", lambda v: bool(_FONT_FAMILY_RE.match(v)))
    keep("fontSize", lambda v: bool(_SIZE_RE.match(v)))
    keep("lineHeight", lambda v: bool(_SIZE_RE.match(v)))
    keep("letterSpacing", lambda v: bool(_SIZE_RE.match(v)))
    keep("fontWeight", lambda v: v in _FONT_WEIGHTS)
    keep("textAlign", lambda v: v in _TEXT_ALIGNS)
    keep("fontStyle", lambda v: v in _FONT_STYLES)
    keep("textTransform", lambda v: v in _TEXT_TRANSFORMS)
    keep("textDecoration", lambda v: v in _TEXT_DECORATIONS)
    color = _safe_color(value.get("color"))
    if color:
        out["color"] = color
    return out


def sanitize_content(cfg: "BlockConfig", raw: dict) -> dict:
    """Coerce/validate incoming block content against its declared schema.

    Enforced per property type: ``select`` values must be a declared option
    (else the default), ``url``/``image`` values must use a safe scheme, ``color``
    must be a valid colour, and free text is coerced to a plain string. Only
    declared properties are kept (no mass-assignment). This is applied on write
    AND at render, so content is safe regardless of how it entered the DB.
    """
    clean = {}
    for key, prop in cfg.properties.items():
        if key not in raw:
            continue
        value = raw[key]
        ptype = prop.get("type")
        if ptype == "select":
            allowed = {opt["value"] for opt in prop.get("options", [])}
            clean[key] = value if value in allowed else prop.get("default", "")
        elif ptype in ("url", "image", "media", "link"):
            # media = a chosen media-library asset URL; link = a picked internal
            # URL (product/page/category) or a raw URL — both scheme-checked.
            clean[key] = _safe_url(value)
        elif ptype == "product":
            clean[key] = _safe_product_id(value)
        elif ptype == "voucher":
            # A voucher code — picked from the store's vouchers or typed manually.
            # Bounded plain text (codes are <= 50 chars); rendering auto-escapes.
            clean[key] = ("" if value is None else str(value)).strip()[:64]
        elif ptype == "color":
            clean[key] = _safe_color(value)
        elif ptype == "spacing":
            clean[key] = _safe_spacing(value)
        elif ptype == "border_advanced":
            clean[key] = _safe_border(value)
        elif ptype == "typography":
            clean[key] = _safe_typography(value)
        else:  # string, textarea, and anything else → plain text
            clean[key] = "" if value is None else str(value)
    return clean


# Blocks live under templates/ so Django's app template loader resolves the
# email.mjml / canvas.html by name; config.json is read directly from disk.
BLOCKS_DIR = Path(__file__).resolve().parent / "templates" / "email_marketing" / "blocks"

# Universal "Style" properties every block inherits (mirrors page_builder's
# _base/base_properties.json). Kept email-appropriate: the background and
# vertical padding of the block's own <mj-section>. A block can opt out with
# "inherit_base": false or drop individual keys via "disable_base_properties".
_PADDING_OPTIONS = [
    {"value": "0", "label": "None"},
    {"value": "8px", "label": "Small"},
    {"value": "16px", "label": "Medium"},
    {"value": "24px", "label": "Large"},
    {"value": "40px", "label": "Extra large"},
]
# Universal Style props, rendered with the shared utility editors:
#   section_bg → ColorPickerUtility, padding → SpacingEditor, border →
#   BorderEditorUtility. Their stored values are the CSS strings the editors
#   emit (same round-trip page_builder uses); the serializer maps them to MJML.
BASE_PROPERTIES = {
    "section_bg": {"type": "color", "label": "Background", "default": "", "tab": "style"},
    "padding": {
        "type": "spacing",
        "label": "Padding",
        "default": "padding: 16px 0px 16px 0px",
        "tab": "style",
    },
    "border": {"type": "border_advanced", "label": "Border", "default": "", "tab": "style"},
}

# Property-panel tabs, in display order.
TAB_ORDER = ["content", "style"]
TAB_LABELS = {"content": "Content", "style": "Style"}


def _merge_base_properties(props: dict, data: dict) -> dict:
    """Merge the universal base properties into a block's own properties.

    Block-specific properties come first (tab defaults to 'content'); base
    properties follow on the 'style' tab. Honours ``inherit_base`` (default
    True) and ``disable_base_properties`` — the same knobs page_builder uses.
    """
    merged: dict = {}
    for key, prop in props.items():
        prop = dict(prop)
        prop.setdefault("tab", "content")
        merged[key] = prop
    if data.get("inherit_base", True):
        disabled = set(data.get("disable_base_properties", []))
        for key, prop in BASE_PROPERTIES.items():
            if key not in disabled:
                merged[key] = dict(prop)
    return merged


# Palette grouping + order (mirrors page_builder's CATEGORY_DISPLAY_ORDER idea).
CATEGORY_ORDER = ["structure", "content", "media", "commerce"]
CATEGORY_LABELS = {
    "structure": "Structure",
    "content": "Content",
    "media": "Media",
    "commerce": "Commerce",
}


class BlockConfig:
    """A single block definition loaded from its config.json."""

    def __init__(self, data: dict):
        self.data = data
        self.block_type = data["block_type"]
        self.name = data.get("name", self.block_type.title())
        self.icon = data.get("icon", "fas fa-cube")
        self.category = data.get("category", "content")
        self.description = data.get("description", "")
        # Block-specific properties merged with the inherited base (Style) props.
        self.properties = _merge_base_properties(data.get("properties", {}), data)
        self.defaults = data.get("defaults", {})

    @property
    def mjml_template(self) -> str:
        return f"email_marketing/blocks/{self.block_type}/email.mjml"

    @property
    def canvas_template(self) -> str:
        return f"email_marketing/blocks/{self.block_type}/canvas.html"

    def default_content(self) -> dict:
        """Initial content for a freshly dropped block."""
        content = {key: prop.get("default") for key, prop in self.properties.items()}
        content.update(self.defaults)
        return content

    def to_palette_dict(self) -> dict:
        return {
            "block_type": self.block_type,
            "name": self.name,
            "icon": self.icon,
            "description": self.description,
        }


def _load_all() -> dict:
    """Read every blocks/<type>/config.json into BlockConfig objects."""
    registry: dict[str, BlockConfig] = {}
    if not BLOCKS_DIR.is_dir():
        return registry
    for child in sorted(BLOCKS_DIR.iterdir()):
        if not child.is_dir() or child.name.startswith("_"):
            continue
        config_path = child / "config.json"
        if not config_path.is_file():
            continue
        try:
            data = json.loads(config_path.read_text(encoding="utf-8"))
            registry[data["block_type"]] = BlockConfig(data)
        except (json.JSONDecodeError, KeyError) as exc:
            logger.error("Invalid email block config at %s: %s", config_path, exc)
    return registry


@lru_cache(maxsize=1)
def _cached_registry() -> dict:
    return _load_all()


def get_registry() -> dict:
    """Return {block_type: BlockConfig}. Bypasses the cache in DEBUG for live edits."""
    if settings.DEBUG:
        return _load_all()
    return _cached_registry()


def get_block(block_type: str) -> BlockConfig | None:
    return get_registry().get(block_type)


def get_palette() -> list[dict]:
    """Return blocks grouped by category for the builder palette."""
    reg = get_registry()
    grouped: dict[str, list] = {}
    for cfg in reg.values():
        grouped.setdefault(cfg.category, []).append(cfg)

    palette = []
    seen = set()
    for category in CATEGORY_ORDER + list(grouped.keys()):
        if category in seen or category not in grouped:
            continue
        seen.add(category)
        blocks = sorted(grouped[category], key=lambda c: c.name)
        palette.append(
            {
                "category": category,
                "label": CATEGORY_LABELS.get(category, category.title()),
                "blocks": [b.to_palette_dict() for b in blocks],
            }
        )
    return palette
