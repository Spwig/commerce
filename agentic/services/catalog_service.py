"""
Projects Spwig catalog data into the UCP catalog shape.

This reads live `Product`/`ProductVariant` data — there is no separate agentic
catalog table, and never should be (that would be the parallel-commerce-engine
failure mode). The queryset is copied from the verified-working
`ProductViewSet.get_queryset` so it avoids the property traps that broke
product_feeds (`is_active`/`primary_image` are @property, not fields).

UCP shapes (2026-04-08):
  Product  required: id, title, description, price_range, variants (>=1)
  Variant  required: id, title, description, price
  Price:   integer minor units + ISO 4217, e.g. {"amount": 1999, "currency": "USD"}

A "simple" Spwig product (no variants) is emitted as a single synthetic
variant carrying the product's own price, so the UCP "variants >= 1" rule
holds without inventing catalog structure.
"""

from __future__ import annotations

from decimal import ROUND_HALF_UP
from typing import Any

from django.db.models import Prefetch, Q


def _description(product) -> str:
    """
    Plain-text product description for UCP.

    `Product` has no `description` field — it stores `full_description`
    (rich HTML) and `short_description`. get_translated_description(plain_text=
    True) resolves the language-appropriate full_description and strips HTML,
    which is what an agent wants. Falls back to the product name so the UCP
    required `description` is never empty.
    """
    text = product.get_translated_description(plain_text=True)
    return (text or "").strip() or product.name


def money_to_ucp(money) -> dict | None:
    """djmoney Money -> {"amount": <int minor units>, "currency": <ISO>}."""
    if money is None:
        return None
    # moneyed knows the sub-unit per currency (USD 100, JPY 1, BHD 1000), so
    # zero-decimal currencies are handled correctly without a hand-maintained list.
    sub_unit = getattr(money.currency, "sub_unit", 100) or 100
    minor = int((money.amount * sub_unit).to_integral_value(rounding=ROUND_HALF_UP))
    return {"amount": minor, "currency": str(money.currency)}


def sellable_products():
    """
    Products an agent may see: the same set the storefront API exposes.

    Copied from ProductViewSet.get_queryset (catalog/api_views.py) — published,
    not hidden, not soft-deleted, not POS-only — plus the per-product
    `agent_visible` opt-out, so a merchant can hide a product from agents while
    it stays on the storefront.
    """
    from catalog.models import Product, ProductImage, ProductVariant

    return (
        Product.objects.filter(
            status="published",
            hide_from_storefront=False,
            is_deleted=False,
            agent_visible=True,
        )
        .exclude(sales_channel="pos_only")
        .select_related("category", "brand")
        .prefetch_related(
            Prefetch("images", queryset=ProductImage.objects.filter(show_in_listing=True)),
            Prefetch("variants", queryset=ProductVariant.objects.filter(is_active=True)),
            "stock_items",
        )
    )


def search(query: str = "", page: int = 1, page_size: int = 20) -> tuple[list, int]:
    """
    Text search over sellable products. Returns (page_of_products, total_count).

    Uses a simple name/description match; the platform SearchService can be
    swapped in later without changing the caller.
    """

    qs = sellable_products()
    if query:
        qs = qs.filter(Q(name__icontains=query) | Q(full_description__icontains=query))
    qs = qs.order_by("id")
    total = qs.count()

    page = max(1, page)
    page_size = max(1, min(page_size, 100))
    start = (page - 1) * page_size
    return list(qs[start : start + page_size]), total


def get_product(product_id: int):
    """A single sellable product by id, or None."""
    return sellable_products().filter(pk=product_id).first()


def _availability(product) -> dict:
    """A boolean + status. UCP does not model stock depth; checkout is truth."""
    if not product.track_inventory:
        return {"available": True, "status": "in_stock"}
    in_stock = (product.total_stock or 0) > 0
    if in_stock:
        return {"available": True, "status": "in_stock"}
    if product.allow_backorders:
        return {"available": True, "status": "backorder"}
    return {"available": False, "status": "out_of_stock"}


def _variant_to_ucp(variant, product, availability, absolute_url) -> dict:
    price = variant.get_effective_price()
    return {
        "id": str(variant.id),
        "title": variant.name or product.name,
        "description": _description(product),
        "price": money_to_ucp(price),
        "availability": availability,
        "sku": variant.sku or "",
    }


def _synthetic_variant(product, availability) -> dict:
    """A simple product with no variants becomes a single default variant."""
    return {
        "id": f"product-{product.id}",
        "title": product.name,
        "description": _description(product),
        "price": money_to_ucp(product.effective_price),
        "availability": availability,
        "sku": product.sku or "",
    }


def to_ucp_product(product, request=None) -> dict[str, Any]:
    """Project one Product into the UCP catalog Product shape."""
    availability = _availability(product)
    url = product.get_absolute_url() if hasattr(product, "get_absolute_url") else None
    if request is not None and url:
        url = request.build_absolute_uri(url)

    variants = list(product.variants.all())
    if variants:
        ucp_variants = [_variant_to_ucp(v, product, availability, url) for v in variants]
        prices = [v.get_effective_price() for v in variants if v.get_effective_price() is not None]
    else:
        ucp_variants = [_synthetic_variant(product, availability)]
        prices = [product.effective_price] if product.effective_price is not None else []

    price_range = None
    if prices:
        price_range = {
            "min": money_to_ucp(min(prices)),
            "max": money_to_ucp(max(prices)),
        }

    doc = {
        "id": str(product.id),
        "title": product.name,
        "description": _description(product),
        "price_range": price_range,
        "variants": ucp_variants,
        "availability": availability,
        "condition": product.condition,
    }
    if url:
        doc["url"] = url
    if product.brand_id and product.brand:
        doc["brand"] = product.brand.name
    return doc
