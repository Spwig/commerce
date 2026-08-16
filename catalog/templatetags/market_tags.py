"""Template helpers for multi-market storefront URLs.

Same-market links need nothing special: ``MarketMiddleware`` folds the current
market into the script prefix, so a plain ``{% url %}`` / ``reverse()`` already
keeps the visitor inside their market. These tags are for CROSS-market links —
a market switcher, hreflang alternates, "view this in the NZ store" — where the
target market differs from the one the request is currently on.
"""

from django import template
from django.urls import reverse

register = template.Library()


def _neutral_base(request, full):
    """Reduce a reversed URL to its market- and subpath-neutral path.

    ``reverse()`` returns ``<subpath><current_market>/<lang>/<path>`` — the
    script prefix carries both the deployment subpath (``/shop``, set by
    ``SubpathMiddleware`` as ``request.script_name``) and the current market
    (``/nz``, ``request.market_prefix``). Stripping both yields ``/<lang>/<path>``,
    onto which any other market prefix can be prepended under the same subpath.
    """
    subpath = getattr(request, "script_name", "") if request else ""
    market_prefix = getattr(request, "market_prefix", "") if request else ""
    prefix = subpath + market_prefix  # e.g. "/shop/nz"
    if prefix and (full == prefix or full.startswith(prefix + "/")):
        return full[len(prefix) :] or "/"
    return full


@register.simple_tag(takes_context=True)
def market_url(context, market_slug, view_name, *args, **kwargs):
    """Build a path for ``view_name`` under a specific market.

    ``market_slug`` empty or ``"default"`` → the unprefixed default market.
    The result keeps any deployment subpath, e.g. ``/shop/sg/en/products/…``.
    Usage: ``{% market_url 'sg' 'product:detail' slug=product.slug %}``.
    """
    request = context.get("request")
    subpath = getattr(request, "script_name", "") if request else ""
    base = _neutral_base(request, reverse(view_name, args=args, kwargs=kwargs))
    target = (
        f"/{market_slug.strip('/')}" if market_slug and market_slug not in ("", "default") else ""
    )
    return f"{subpath}{target}{base}"


@register.simple_tag(takes_context=True)
def current_market(context):
    """The current request's market slug (``""`` for the default market)."""
    request = context.get("request")
    return getattr(request, "market_slug", None) or ""
