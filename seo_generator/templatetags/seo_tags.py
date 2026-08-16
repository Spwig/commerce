"""Reusable SEO status tag.

Any object that carries ``meta_title`` + ``meta_description`` fields can render a
system-wide "SEO complete / incomplete" badge with ``{% seo_badge obj %}``.
"Complete" matches the definition used everywhere else in the SEO generator
(coverage service, dashboard): both the meta title AND meta description are
populated in the primary language.
"""

from django import template

register = template.Library()


def _is_seo_complete(obj):
    """True when both meta_title and meta_description are non-empty.

    Uses the same ``!= "" and not NULL`` predicate as
    seo_generator.services.coverage_service and the brand/collection/blogpost
    filter endpoints — no ``.strip()`` — so the badge never disagrees with the
    SEO dashboard's coverage numbers or the "SEO state" filters, even for
    whitespace-only values.
    """
    title = getattr(obj, "meta_title", "") or ""
    description = getattr(obj, "meta_description", "") or ""
    return bool(title and description)


@register.inclusion_tag("seo_generator/components/seo_badge.html")
def seo_badge(obj, show_label=True):
    """Render an SEO-status badge for ``obj``.

    Renders nothing for objects that don't expose the SEO fields, so it is safe
    to drop into any card/list/detail template without a guard.
    """
    applicable = hasattr(obj, "meta_title") and hasattr(obj, "meta_description")
    return {
        "applicable": applicable,
        "complete": applicable and _is_seo_complete(obj),
        "show_label": show_label,
    }
