from django import template
from django.core.cache import cache
from django.db.models import Q
from django.utils import timezone

from core.translation_utils import get_primary_language, translate_instance

register = template.Library()

_ANNOUNCEMENT_FIELDS = {'title': 'title', 'body': 'body', 'link_text': 'link_text'}


@register.simple_tag(takes_context=True)
def get_active_announcements(context):
    """
    Get active announcements ordered by priority.
    Returns announcements that are enabled and not expired.
    Results are cached per-language for 5 minutes and invalidated on save/delete.
    Translated fields (title, body, link_text) are applied in-place for
    non-primary languages.
    """
    request = context.get('request')
    lang = getattr(request, 'LANGUAGE_CODE', None) if request else None

    cache_key = f'active_announcements_{lang}' if lang else 'active_announcements'
    announcements = cache.get(cache_key)

    if announcements is None:
        from announcements.models import Announcement

        now = timezone.now()
        qs = Announcement.objects.filter(
            is_enabled=True,
        ).filter(
            Q(expires_at__isnull=True) | Q(expires_at__gt=now)
        ).select_related(
            'image',
            'product_reference',
            'category_reference',
            'blog_post_reference',
            'page_reference',
        ).order_by('priority', '-created_at')

        announcements = list(qs)
        # Pre-resolve URLs for template usage
        for ann in announcements:
            ann.resolved_url = ann.get_resolved_url()

        # Apply translations for non-primary languages
        if lang:
            primary = get_primary_language()
            if lang != primary:
                for ann in announcements:
                    translate_instance(ann, lang, _ANNOUNCEMENT_FIELDS)

        cache.set(cache_key, announcements, 300)

    return announcements
