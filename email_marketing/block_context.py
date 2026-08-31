"""Context providers — enrich a block's render context with live catalog data.

Commerce blocks store only *config* in their content (a product id, a mode, a
count). At render time — both for the builder canvas and for the final send —
the matching provider runs the catalog query and returns display-ready data.
Because it runs at send time, every campaign captures a fresh snapshot of
prices, sale state, and stock-visible products (the native-commerce advantage a
synced integration can't match).

All URLs are absolutised against the store origin (image URLs are MEDIA_URL-
relative on non-S3 installs; product URLs live under i18n_patterns), and prices
use the sale- and currency-aware ``get_price_in_currency`` + request-free
``format_money``.
"""

import logging

from django.conf import settings
from django.urls import reverse
from django.utils import translation

logger = logging.getLogger("email_marketing")


def _origin() -> str:
    """Absolute https origin for the store (for image/product links in email)."""
    from django.contrib.sites.models import Site

    from core.models import SiteSettings

    site_url = (SiteSettings.get_settings().site_url or "").rstrip("/")
    # Only trust an http(s) origin (defense-in-depth: never let a stray scheme
    # become the prefix of every href/src in a campaign).
    if site_url.startswith(("http://", "https://")) and site_url != "https://example.com":
        return site_url
    return f"https://{Site.objects.get_current().domain}"


def _currency() -> str:
    from core.models import SiteSettings

    return SiteSettings.get_settings().default_currency or "USD"


def _visible_products():
    """The canonical publicly-visible product queryset (a ProductQuerySet).

    Also excludes products that aren't visible in the store's default market, so a
    region-restricted product (``region_restriction_mode`` / ``ProductRegionVisibility``)
    can't leak into an email sent from a store whose home region doesn't sell it.
    A single-market install (no ``SalesRegion`` rows) is unaffected. When
    per-subscriber region targeting lands, pass the recipient's region here instead.
    """
    from catalog.models import Product, SalesRegion

    qs = Product.objects.filter(status="published", hide_from_storefront=False).exclude(
        sales_channel="pos_only"
    )
    region = SalesRegion.objects.filter(is_active=True).order_by("-priority").first()
    if region is not None:
        qs = qs.visible_in_region(region)
    return qs


def _format(money) -> str:
    from core.utils.currency_helpers import format_money

    return format_money(money.amount, str(money.currency))


def _abs(origin: str, url: str) -> str:
    """Absolutise a MEDIA_URL-relative asset URL (no-op if already absolute)."""
    if url and url.startswith("/"):
        return origin + url
    return url


def _image_sources(asset, origin: str, size_preset: str) -> dict | None:
    """Return format-optimised, correctly-sized, absolute image sources.

    Uses the platform's ``get_picture_sources`` so the canvas can render a real
    <picture> (AVIF/WebP/raster) at the right size, while email uses the raster
    ``fallback`` (the only format all mail clients render) — still the sized
    variant, not the full original.
    """
    if asset is None:
        return None
    try:
        sources = asset.get_picture_sources(size_preset=size_preset) or {}
    except Exception:  # noqa: BLE001 — fall back to the plain display URL
        display = getattr(asset, "get_display_url", lambda: "")()
        return {"fallback": _abs(origin, display)} if display else None

    out = {
        "avif": _abs(origin, sources.get("avif", "")),
        "webp": _abs(origin, sources.get("webp", "")),
        "fallback": _abs(origin, sources.get("fallback", "")),
        "width": sources.get("width"),
        "height": sources.get("height"),
    }
    return out if (out["fallback"] or out["webp"]) else None


def _product_display(product, currency: str, origin: str, image_preset: str) -> dict:
    """Build a display-ready dict for one product (canvas + email safe)."""
    # Product URL (language-prefixed under i18n_patterns) → absolute.
    with translation.override(settings.LANGUAGE_CODE or "en"):
        try:
            path = reverse("page_builder:product_detail", kwargs={"product_slug": product.slug})
        except Exception:  # noqa: BLE001
            path = product.get_absolute_url()
    product_url = origin + path

    price = product.get_price_in_currency(currency)
    on_sale = bool(product.is_on_sale)
    return {
        "name": product.name,
        "url": product_url,
        "image": _image_sources(product.primary_image, origin, image_preset),
        "price": _format(price),
        "was_price": _format(product.price) if on_sale else "",
        "on_sale": on_sale,
    }


def featured_product_context(content: dict, render_ctx: dict | None = None) -> dict:
    """Resolve a single featured product by id.

    Falls back to the triggering event's ``product_id`` when the block itself has
    none configured — so a Featured Product block dropped into a back-in-stock
    journey automatically shows the product that was just restocked.
    """
    raw_id = content.get("product_id")
    if not raw_id and render_ctx:
        raw_id = (render_ctx.get("event") or {}).get("product_id")
    try:
        pid = int(str(raw_id).strip())
    except (TypeError, ValueError):
        return {"product": None}
    product = _visible_products().filter(id=pid).first()
    if not product:
        return {"product": None}
    return {"product": _product_display(product, _currency(), _origin(), "large")}


def _cart_line_display(item, currency: str, origin: str) -> dict | None:
    """Display dict for one cart line (product card + quantity/variant).

    Returns None on any per-product data hiccup (e.g. a since-broken product) so one
    bad line is skipped rather than dropping the whole email.
    """
    product = getattr(item, "product", None)
    if product is None:
        return None
    try:
        d = _product_display(product, currency, origin, "product_listing")
        d["quantity"] = item.quantity
        d["variant"] = getattr(getattr(item, "variant", None), "name", "") or ""
        return d
    except Exception:  # noqa: BLE001 — skip a broken line, keep the rest of the cart
        logger.warning("Abandoned-cart line render failed for item %s", getattr(item, "pk", "?"))
        return None


def abandoned_cart_context(content: dict, render_ctx: dict | None = None) -> dict:
    """Resolve the recipient's abandoned-cart contents for a recovery email.

    Reads the cart id from the triggering event (``render_ctx["event"]["cart_id"]``),
    falling back to the subscriber's most recent regular cart. Returns live line items
    (name, image, price, qty, variant) so the email shows exactly what was left behind,
    plus a link back to the cart. ``has_items`` is False when the cart is gone / emptied
    / converted — the template then renders nothing, so a recovered cart never mails an
    empty reminder even if enrollment cancellation was missed.
    """
    from cart.models import Cart

    render_ctx = render_ctx or {}
    event = render_ctx.get("event") or {}
    subscriber = render_ctx.get("subscriber")

    cart = None
    cart_id = event.get("cart_id")
    if cart_id:
        cart = Cart.objects.filter(id=cart_id).first()
    elif subscriber is not None and getattr(subscriber, "user_id", None):
        cart = (
            Cart.objects.filter(user_id=subscriber.user_id, session_key__isnull=True)
            .order_by("-updated_at")
            .first()
        )

    origin = _origin()
    if cart is None:
        return {"items": [], "has_items": False, "cart_url": origin + "/cart/"}

    currency = _currency()
    items = [
        d
        for d in (
            _cart_line_display(it, currency, origin)
            for it in cart.items.select_related("product", "variant")
        )
        if d
    ]
    return {"items": items, "has_items": bool(items), "cart_url": origin + "/cart/"}


def product_grid_context(content: dict, render_ctx: dict | None = None) -> dict:
    """Resolve a small grid of products by mode.

    Modes: ``new`` (newest), ``bestsellers``, ``sale``, and ``new_since_send``
    — newest products added since the campaign's last send (the ``since``
    watermark in ``render_ctx``). Like the Blog Posts block's since-mode, this
    keeps a recurring newsletter from re-featuring the same "new arrivals";
    without a watermark it behaves like ``new``.
    """
    mode = content.get("mode", "new")
    try:
        count = max(1, min(int(content.get("count") or 3), 4))
    except (TypeError, ValueError):
        count = 3

    qs = _visible_products()
    if mode == "bestsellers":
        qs = qs.order_by("-sales_count", "-views_count", "-created_at")
    elif mode == "sale":
        qs = qs.on_sale().order_by("-updated_at")
    elif mode == "new_since_send":
        since = (render_ctx or {}).get("since")
        if since:
            qs = qs.filter(created_at__gt=since)
        qs = qs.order_by("-created_at")
    else:  # new
        qs = qs.order_by("-created_at")

    currency, origin = _currency(), _origin()
    products = [_product_display(p, currency, origin, "product_listing") for p in qs[:count]]
    return {"products": products, "count": count}


def _blog_excerpt(post) -> str:
    """A short, plain-text teaser for a post card (uses the post's excerpt)."""
    text = (getattr(post, "excerpt", "") or "").strip()
    if len(text) <= 200:
        return text
    return text[:197].rstrip() + "…"


def blog_posts_context(content: dict, render_ctx: dict | None = None) -> dict:
    """Resolve published blog posts for a newsletter block.

    With ``source == "since_last_send"`` and a ``since`` watermark in
    ``render_ctx`` (the campaign's ``last_content_sent_at``), only posts
    published after that time are included — so a recurring newsletter never
    re-sends the same posts. Without a watermark (a first send, or the builder
    canvas) it behaves like "latest".
    """
    try:
        count = max(1, min(int(content.get("count") or 3), 4))
    except (TypeError, ValueError):
        count = 3

    from blog.models import BlogPost

    qs = BlogPost.published()
    since = (render_ctx or {}).get("since")
    if content.get("source") == "since_last_send" and since:
        qs = qs.filter(published_at__gt=since)

    origin = _origin()
    posts = []
    with translation.override(settings.LANGUAGE_CODE or "en"):
        for post in qs.order_by("-published_at")[:count]:
            try:
                path = post.get_absolute_url()
            except Exception:  # noqa: BLE001 — fall back to a conventional path
                path = f"/blog/{post.slug}/"
            posts.append(
                {
                    "title": post.title,
                    "url": _abs(origin, path),
                    "excerpt": _blog_excerpt(post),
                    "date": post.published_at.strftime("%d %b %Y") if post.published_at else "",
                    "image": _image_sources(
                        getattr(post, "featured_image", None), origin, "product_listing"
                    ),
                }
            )
    return {"posts": posts, "count": count}


_PROVIDERS = {
    "featured_product": featured_product_context,
    "product_grid": product_grid_context,
    "blog_posts": blog_posts_context,
    "abandoned_cart": abandoned_cart_context,
}


def get_block_context(block_type: str, content: dict, render_ctx: dict | None = None) -> dict:
    """Return extra render context for a block (empty for non-dynamic blocks).

    ``render_ctx`` carries campaign-level render state (e.g. the ``since``
    watermark for delta-aware blocks); providers that don't need it ignore it.
    """
    provider = _PROVIDERS.get(block_type)
    if not provider:
        return {}
    try:
        return provider(content or {}, render_ctx)
    except Exception as exc:  # noqa: BLE001 — a data hiccup must not break the builder
        logger.error("Block context provider '%s' failed: %s", block_type, exc)
        return {}
