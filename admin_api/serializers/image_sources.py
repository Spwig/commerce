"""Sized image sources for the mobile Admin API.

The storefront serves a full ``<picture>`` source set via
``MediaAsset.get_picture_sources()``. The mobile app can't do HTML-style
content negotiation — it picks a single URL per context (a 48pt list cell, a
280pt detail hero, a full-screen zoom) — so we expose named sizes mapped to one
WebP-preferred URL each.

Sizes are keyed by the rendition's intrinsic pixel **width**, not its
``size_preset`` name. The admin image-upload path historically generated presets
under different names than the system presets (app upload:
``small=150/medium=300/large=600``; system: ``thumbnail=150/small=300/
medium=600/large=1200``), so keying on width yields a stable contract across
images from either source without a data migration.
"""

# Semantic size name -> intrinsic width in px, ordered smallest first.
_SIZE_WIDTHS = (
    ("thumbnail", 150),
    ("small", 300),
    ("medium", 600),
    ("large", 1200),
)
# Sizes returned in list contexts (cells never need large/full).
_LIST_SIZES = frozenset({"thumbnail", "small", "medium"})
# Preferred preset names when several renditions share a width (e.g. a square
# `large` 1200x1200 vs a wide `banner` 1200x400 — pick the square one).
_PREFERRED_PRESETS = frozenset({"thumbnail", "small", "medium", "large"})


def build_image_sources(asset, *, detail=False):
    """Return ``{size_name: url}`` of sized renditions for the app, or ``None``.

    List contexts get thumbnail/small/medium; ``detail=True`` adds ``large`` and
    a full-resolution ``full`` URL for pinch-to-zoom. Only sizes with a real
    generated rendition are included, so the app never receives a full-size
    image masquerading as a thumbnail.

    Reads the prefetched ``thumbnails`` relation — callers MUST prefetch
    ``…media_asset__thumbnails`` (or ``image_asset__thumbnails``) to avoid an
    N+1 in list rendering.
    """
    if asset is None:
        return None

    # Pick one rendition per width, preferring the standard square presets when
    # several presets share a width. `.all()` reads the prefetch cache.
    by_width = {}
    for thumb in asset.thumbnails.all():
        current = by_width.get(thumb.width)
        if current is None or (
            thumb.size_preset in _PREFERRED_PRESETS
            and current.size_preset not in _PREFERRED_PRESETS
        ):
            by_width[thumb.width] = thumb

    sources = {}
    for name, width in _SIZE_WIDTHS:
        if not detail and name not in _LIST_SIZES:
            continue
        thumb = by_width.get(width)
        if thumb is None:
            continue
        url = thumb.webp_file.url if thumb.webp_file else (thumb.file.url if thumb.file else None)
        if url:
            sources[name] = url

    if detail:
        full = asset.get_display_url()
        if full:
            sources["full"] = full

    return sources or None
