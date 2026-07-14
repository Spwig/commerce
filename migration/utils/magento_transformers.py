"""
Magento-specific transformation functions for field mapping.

Handles Magento 2 REST API data structures including:
- Product status/visibility integer codes
- EAV custom_attributes resolution
- Order status mapping
- CMS content directive cleanup
"""

import re


def transform_magento_status(value) -> str:
    """Transform Magento product status (int) to internal status.

    Magento values: 1 = Enabled, 2 = Disabled
    """
    mapping = {
        1: "published",
        "1": "published",
        2: "draft",
        "2": "draft",
    }
    return mapping.get(value, "draft")


def transform_magento_visibility(value) -> str:
    """Transform Magento product visibility to descriptive string.

    1 = Not Visible Individually (configurable child)
    2 = Catalog only
    3 = Search only
    4 = Catalog, Search (fully visible)
    """
    mapping = {
        1: "not_visible",
        "1": "not_visible",
        2: "catalog",
        "2": "catalog",
        3: "search",
        "3": "search",
        4: "visible",
        "4": "visible",
    }
    return mapping.get(value, "visible")


def transform_magento_product_type(type_id: str) -> str:
    """Transform Magento product type_id to internal product type.

    Magento types: simple, configurable, grouped, bundle, virtual, downloadable
    """
    mapping = {
        "simple": "simple",
        "configurable": "variable",
        "grouped": "bundle",
        "bundle": "bundle",
        "virtual": "digital",
        "downloadable": "digital",
    }
    return mapping.get(str(type_id).lower(), "simple")


def transform_magento_order_status(status: str) -> str:
    """Transform Magento order status to internal order status.

    Magento statuses: pending, processing, complete, closed, canceled, holded,
                      payment_review, fraud, pending_payment
    """
    mapping = {
        "pending": "pending",
        "pending_payment": "pending",
        "payment_review": "on_hold",
        "fraud": "on_hold",
        "processing": "processing",
        "complete": "completed",
        "closed": "completed",
        "canceled": "cancelled",
        "holded": "on_hold",
    }
    return mapping.get(str(status).lower(), "pending")


def transform_magento_payment_status(status: str) -> str:
    """Transform Magento order status to a payment status."""
    mapping = {
        "pending": "pending",
        "pending_payment": "pending",
        "payment_review": "pending",
        "fraud": "failed",
        "processing": "paid",
        "complete": "paid",
        "closed": "refunded",
        "canceled": "cancelled",
        "holded": "pending",
    }
    return mapping.get(str(status).lower(), "pending")


def transform_magento_discount_type(simple_action: str) -> str:
    """Transform Magento sales rule simple_action to internal discount type.

    Magento actions: by_percent, by_fixed, cart_fixed, buy_x_get_y
    """
    mapping = {
        "by_percent": "percentage",
        "by_fixed": "fixed",
        "cart_fixed": "fixed",
        "buy_x_get_y": "percentage",
    }
    return mapping.get(str(simple_action).lower(), "fixed")


def resolve_custom_attribute(custom_attributes: list[dict], code: str) -> str | None:
    """Extract a value from Magento's custom_attributes array by attribute_code.

    Magento returns custom attributes as:
        [{"attribute_code": "description", "value": "<p>HTML</p>"}, ...]

    Returns None if the attribute is not found.
    """
    if not custom_attributes:
        return None
    for attr in custom_attributes:
        if attr.get("attribute_code") == code:
            return attr.get("value")
    return None


def resolve_attribute_label(value, attribute_code: str, options_cache: dict) -> str:
    """Resolve a Magento EAV option ID to its human-readable label.

    Args:
        value: The option ID (e.g., "53") or comma-separated IDs for multiselect
        attribute_code: The attribute code (e.g., "color")
        options_cache: Dict of {attribute_code: {option_id: label}}

    Returns:
        The label string, or the original value if not resolvable.
    """
    if value is None:
        return ""
    attr_options = options_cache.get(attribute_code, {})
    if not attr_options:
        return str(value)

    # Handle multiselect (comma-separated IDs)
    value_str = str(value)
    if "," in value_str:
        ids = [v.strip() for v in value_str.split(",")]
        labels = [attr_options.get(v, v) for v in ids]
        return ", ".join(labels)

    return attr_options.get(value_str, value_str)


def transform_magento_rating(ratings: list[dict]) -> int:
    """Convert Magento review ratings to a 1-5 star rating.

    Magento ratings have a percent field (0-100).
    Convert to 1-5 scale: percent / 20, rounded.
    """
    if not ratings:
        return 0
    try:
        percent = int(ratings[0].get("percent", 0))
        stars = round(percent / 20)
        return max(1, min(5, stars))
    except (ValueError, TypeError, IndexError):
        return 0


def clean_cms_directives(content: str, store_url: str = "") -> str:
    """Clean Magento CMS content directives for use outside Magento.

    Transforms:
    - {{media url="path/to/file.jpg"}} -> absolute URL
    - {{store url="page/path"}} -> relative URL
    - {{widget ...}} -> removed (no equivalent)
    - {{block ...}} -> removed (no equivalent)
    """
    if not content:
        return ""

    store_url = store_url.rstrip("/")

    # Convert {{media url="..."}} to absolute image URLs
    def replace_media(match):
        path = match.group(1)
        if store_url:
            return f"{store_url}/media/{path}"
        return f"/media/{path}"

    content = re.sub(r'\{\{media\s+url="([^"]+)"\}\}', replace_media, content)

    # Convert {{store url="..."}} to relative URLs
    def replace_store_url(match):
        path = match.group(1)
        return f"/{path}"

    content = re.sub(r'\{\{store\s+url="([^"]+)"\}\}', replace_store_url, content)

    # Remove {{widget ...}} directives entirely
    content = re.sub(r"\{\{widget\b[^}]*\}\}", "", content)

    # Remove {{block ...}} directives entirely
    content = re.sub(r"\{\{block\b[^}]*\}\}", "", content)

    # Remove {{config ...}} directives
    content = re.sub(r"\{\{config\b[^}]*\}\}", "", content)

    return content.strip()
