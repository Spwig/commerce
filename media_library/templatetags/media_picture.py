"""Template helpers for rendering responsive <picture> elements.

AVIF is offered first, WebP second, and the original-format <img> is the
universal fallback. A <source> is emitted only when the corresponding file is
known to exist, so browsers never land on a 404 candidate (which would render a
broken image with no fallback).

Two entry points share the same resolution logic:

- ``{% picture source size="product_listing" alt=... css=... %}`` — a complete
  <picture> for simple call sites (product cards, category cards, thumbnails).
- ``{{ url_or_asset|picture_sources:"product_listing" }}`` — returns just the
  ``{avif, webp, fallback, width, height}`` dict for bespoke markup (e.g. the
  page-builder image element) that keeps its own <img> and only needs sources.

``source`` may be a MediaAsset, a stored media URL string, or an already-built
sources dict. URL inputs are resolved to their asset and cached, so page-builder
pages with many images don't regress on query count.
"""

from django import template
from django.core.cache import cache

from media_library.models import MediaAsset

register = template.Library()

# Cache resolved source sets for URL inputs. AVIF is generated asynchronously,
# so a briefly stale "no avif yet" entry only delays serving AVIF — it never
# serves a broken source.
_SOURCES_CACHE_TTL = 300


def _empty_sources(fallback=None):
    return {"avif": None, "webp": None, "fallback": fallback, "width": None, "height": None}


def _sources_from_thumbnail(thumb):
    return {
        "avif": thumb.avif_file.url if thumb.avif_file else None,
        "webp": thumb.webp_file.url if thumb.webp_file else None,
        "fallback": thumb.file.url if thumb.file else None,
        "width": thumb.width,
        "height": thumb.height,
    }


def _resolve_url_sources(url):
    """Resolve a stored media URL (thumbnail rendition OR full-size) to sources.

    A URL may point at a per-preset MediaThumbnail file (``{id}_{preset}.webp``)
    or at the asset's own full-size file (``{id}.webp``). Match the thumbnail
    first so its exact-size AVIF/WebP siblings are served; fall back to the
    asset. Unrecognised/external URLs return a plain fallback so the caller
    just renders a normal <img>.
    """
    import os
    from urllib.parse import urlparse

    from django.db.models import Q

    from media_library.models import MediaThumbnail

    filename = os.path.basename(urlparse(url).path)
    if not filename:
        return _empty_sources(url)

    thumb = MediaThumbnail.objects.filter(
        Q(file__icontains=filename)
        | Q(webp_file__icontains=filename)
        | Q(avif_file__icontains=filename)
    ).first()
    if thumb:
        sources = _sources_from_thumbnail(thumb)
        if not sources["fallback"]:
            sources["fallback"] = url
        return sources

    asset = MediaAsset.resolve_from_url(url)
    if asset:
        return asset.get_picture_sources()
    return _empty_sources(url)


def resolve_sources(source, size_preset=None):
    """Resolve ``source`` (MediaAsset | URL str | dict) to a sources dict."""
    if source is None:
        return None
    if isinstance(source, dict):
        return source
    if isinstance(source, MediaAsset):
        return source.get_picture_sources(size_preset)
    if isinstance(source, str):
        # An asset object + preset resolves precisely; a bare URL is resolved
        # (and cached) against thumbnail then full-size renditions.
        cache_key = f"picture_sources:url:{source}"
        cached = cache.get(cache_key)
        if cached is not None:
            return cached
        result = _resolve_url_sources(source)
        cache.set(cache_key, result, _SOURCES_CACHE_TTL)
        return result
    # Unknown type (e.g. a model exposing get_picture_sources) — duck-type it.
    getter = getattr(source, "get_picture_sources", None)
    if callable(getter):
        return getter(size_preset)
    return None


@register.filter(name="picture_sources")
def picture_sources(source, size_preset=None):
    """Filter form: return the sources dict for use in custom <picture> markup."""
    return resolve_sources(source, size_preset or None)


@register.inclusion_tag("media_library/components/picture.html")
def picture(
    source,
    size=None,
    alt="",
    css="",
    loading="lazy",
    sizes=None,
    width=None,
    height=None,
    fetchpriority=None,
):
    """Render a complete <picture> element for ``source``.

    Args:
        source: MediaAsset, stored media URL, or a sources dict.
        size: named ImageSizePreset slug (omit for the full-size rendition).
        alt: <img> alt text (always pass something meaningful).
        css: class(es) applied to the inner <img>.
        loading: <img> loading attr ("lazy" default; "eager" for LCP images).
        sizes: optional ``sizes`` attribute for the <source>/<img>.
        width/height: explicit intrinsic dimensions (fall back to the rendition).
        fetchpriority: optional ``fetchpriority`` (e.g. "high" for the hero).
    """
    sources = resolve_sources(source, size) or _empty_sources()
    return {
        "sources": sources,
        "alt": alt,
        "css": css,
        "loading": loading,
        "sizes": sizes,
        "width": width if width is not None else sources.get("width"),
        "height": height if height is not None else sources.get("height"),
        "fetchpriority": fetchpriority,
    }
