"""Visibility resolution — the capability seam for market-aware and personalized
page content.

Two behaviours, kept out of views/templatetags so the capability is discoverable
by name:

- ``resolve_element_visibility`` — decide how a page element renders in the
  cacheable storefront shell (show / hide / defer), so market/geo/language/
  currency content is deterministic per URL and per-visitor content is never
  baked into the shared cache.
- ``resolve_personalized_elements`` — render the deferred (per-visitor) elements a
  visitor is actually entitled to see, evaluating auth/cart/device/geo rules with
  their real context and enforcing the ancestor-container chain.
"""

import logging

from page_builder.models import Element

logger = logging.getLogger(__name__)


def resolve_element_visibility(element, request, context=None):
    """Decide whether a page element shows, hides, or defers in the shell.

    Returns ``"show"``, ``"hide"`` or ``"defer"``. Only shell-stage rules
    (geo_region / language / currency) are evaluated here; per-visitor rules are
    deferred to the personalization pass so they never enter the cached shell.
    """
    return element.shell_visibility(request, context=context)


def _owning_page_id(element):
    """The id of the page a (possibly nested) element belongs to.

    Nested children have ``page=NULL`` and are linked to the page only through
    ``parent_element``, so walk up to the top-level ancestor and read its page.
    Bounded against a cyclic parent chain.
    """
    node = element
    seen = set()
    while node.parent_element_id is not None and node.id not in seen:
        seen.add(node.id)
        node = node.parent_element
    return node.page_id


def _build_route_context(page, request, category_slug=None, product_slug=None):
    """Rebuild the page-type context PageView supplies (home / category / product),
    so deferred elements that read product/category/products render correctly.

    The client sends the route slug because a page_builder category/product page
    is a template shared across many categories/products — the specific one is in
    the storefront URL, not derivable from page_id alone.
    """
    from page_builder.views import PageView

    view = PageView()
    view.request = request
    view.kwargs = {}
    if category_slug:
        view.kwargs["category_slug"] = category_slug
    if product_slug:
        view.kwargs["product_slug"] = product_slug
    try:
        if page.page_type == "home":
            return view.get_home_context()
        if page.page_type == "category" and category_slug:
            return view.get_category_context()
        if page.page_type == "product" and product_slug:
            return view.get_product_context()
    except Exception:
        logger.exception("personalize: failed building route context for page %s", page.id)
    return {}


def resolve_personalized_elements(
    page, element_ids, request, category_slug=None, product_slug=None
):
    """Render the per-visitor page elements a visitor is entitled to see.

    Returns ``{str(element_id): html_or_None}``. An element is rendered only if it
    belongs to ``page`` (by top-level ancestor, so nested children count) AND it
    and its whole ancestor-container chain pass full visibility for this visitor —
    the ancestor/page checks are the IDOR guard against fetching arbitrary ids.
    ``category_slug`` / ``product_slug`` let the endpoint rebuild the page-type
    context so deferred elements on category/product pages render fully.
    """
    from page_builder.templatetags.element_tags import render_personalized_element

    route_context = _build_route_context(page, request, category_slug, product_slug)

    result = {}
    for element in Element.objects.filter(id__in=element_ids):
        if _owning_page_id(element) != page.id:
            continue  # not this page's element (nested or not) — reject
        try:
            result[str(element.id)] = render_personalized_element(request, element, route_context)
        except Exception:
            logger.exception("personalize: failed rendering element %s", element.id)
            result[str(element.id)] = None
    return result
