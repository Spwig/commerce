"""
Social Sharing Template Tags

Template tags for rendering social share buttons based on merchant settings.
"""

from django import template
from django.utils.safestring import mark_safe
from social_sharing.settings_models import SocialSharingSettings

register = template.Library()


# Platform data: key -> {label, icon_svg}
# SVG icons are minimal, CSP-safe inline SVGs (no external dependencies)
PLATFORM_DATA = {
    'facebook': {
        'label': 'Share on Facebook',
        'icon_svg': mark_safe(
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
            '<path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 '
            '4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 '
            '1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 '
            '0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 '
            '23.027 24 18.062 24 12.073z"/></svg>'
        ),
    },
    'twitter': {
        'label': 'Share on Twitter',
        'icon_svg': mark_safe(
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
            '<path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 '
            '21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 '
            '4.126H5.117z"/></svg>'
        ),
    },
    'linkedin': {
        'label': 'Share on LinkedIn',
        'icon_svg': mark_safe(
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
            '<path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 '
            '0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 '
            '1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 '
            '7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 '
            '1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 '
            '13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 '
            '23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 '
            '.774 23.2 0 22.222 0h.003z"/></svg>'
        ),
    },
    'pinterest': {
        'label': 'Share on Pinterest',
        'icon_svg': mark_safe(
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
            '<path d="M12.017 0C5.396 0 .029 5.367.029 11.987c0 5.079 3.158 9.417 '
            '7.618 11.162-.105-.949-.199-2.403.041-3.439.219-.937 1.406-5.957 '
            '1.406-5.957s-.359-.72-.359-1.781c0-1.668.967-2.914 2.171-2.914 '
            '1.023 0 1.518.769 1.518 1.69 0 1.029-.655 2.568-.994 3.995-.283 '
            '1.194.599 2.169 1.777 2.169 2.133 0 3.772-2.249 3.772-5.495 '
            '0-2.873-2.064-4.882-5.012-4.882-3.414 0-5.418 2.561-5.418 '
            '5.207 0 1.031.397 2.138.893 2.738a.36.36 0 01.083.345l-.333 '
            '1.36c-.053.22-.174.267-.402.161-1.499-.698-2.436-2.889-2.436-4.649 '
            '0-3.785 2.75-7.262 7.929-7.262 4.163 0 7.398 2.967 7.398 6.931 '
            '0 4.136-2.607 7.464-6.227 7.464-1.216 0-2.359-.631-2.75-1.378l-.748 '
            '2.853c-.271 1.043-1.002 2.35-1.492 3.146C9.57 23.812 10.763 24 12.017 '
            '24c6.624 0 11.99-5.367 11.99-11.988C24.007 5.367 18.641 0 12.017 0z"/></svg>'
        ),
    },
    'whatsapp': {
        'label': 'Share on WhatsApp',
        'icon_svg': mark_safe(
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
            '<path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 '
            '1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 '
            '0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 '
            '3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 '
            '1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 '
            '7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 '
            '9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 '
            '2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 '
            '9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 '
            '11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 '
            '005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 '
            '00-3.48-8.413z"/></svg>'
        ),
    },
    'telegram': {
        'label': 'Share on Telegram',
        'icon_svg': mark_safe(
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
            '<path d="M11.944 0A12 12 0 000 12a12 12 0 0012 12 12 12 0 0012-12A12 '
            '12 0 0012 0a12 12 0 00-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 '
            '0 01.171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 '
            '8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 '
            '3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 '
            '1.14-5.061 3.345-.479.33-.913.492-1.302.48-.428-.013-1.252-.242-1.865-.44-.751-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 '
            '3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"/></svg>'
        ),
    },
    'email': {
        'label': 'Share via Email',
        'icon_svg': mark_safe(
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
            '<path d="M1.5 8.67v8.58a3 3 0 003 3h15a3 3 0 003-3V8.67l-8.928 '
            '5.493a3 3 0 01-3.144 0L1.5 8.67z"/>'
            '<path d="M22.5 6.908V6.75a3 3 0 00-3-3h-15a3 3 0 00-3 3v.158l9.714 '
            '5.978a1.5 1.5 0 001.572 0L22.5 6.908z"/></svg>'
        ),
    },
}

# Default platform order when no specific platforms are configured
DEFAULT_PLATFORM_ORDER = [
    'facebook', 'twitter', 'linkedin', 'pinterest',
    'whatsapp', 'telegram', 'email',
]


@register.inclusion_tag('social_sharing/widget_include.html', takes_context=True)
def social_share_buttons(context, content_type=None, object_id=None, **kwargs):
    """
    Render social share buttons for content.

    Usage in templates:
        {% load social_share_tags %}
        {% social_share_buttons content_type='product' object_id=product.id %}

    Or with additional context:
        {% social_share_buttons content_type='product' object_id=product.id share_title=product.name share_image=product.image.url %}

    Merchants control visibility and configuration through admin settings.
    """
    # Get merchant settings
    settings = SocialSharingSettings.get_settings()

    # Merge merchant settings with any template overrides
    widget_config = {
        'show_counts': settings.show_counts,
        'track_shares': settings.track_shares,
    }

    # Add merchant's default config
    if settings.default_config:
        widget_config.update(settings.default_config)

    # Template-level overrides
    widget_config.update(kwargs)

    # Build share data
    request = context.get('request')
    share_data = {
        'content_type': content_type,
        'object_id': object_id,
        'share_url': kwargs.get('share_url', request.build_absolute_uri() if request else ''),
        'share_title': kwargs.get('share_title', ''),
        'share_description': kwargs.get('share_description', ''),
        'share_image': kwargs.get('share_image', ''),
    }

    # Build enabled platforms list with icons
    enabled = settings.enabled_platforms or DEFAULT_PLATFORM_ORDER
    enabled_platforms = [
        {'key': p, **PLATFORM_DATA[p]}
        for p in enabled
        if p in PLATFORM_DATA
    ]

    # Build CSS modifier classes from settings
    css_classes = [f'social-share-placement-{settings.placement_position}']
    if settings.mobile_visibility == 'hide':
        css_classes.append('social-share-mobile-hide')
    elif settings.mobile_visibility == 'mobile_only':
        css_classes.append('social-share-mobile-only')

    return {
        'render': True,
        'widget_config': widget_config,
        'share_data': share_data,
        'enabled_platforms': enabled_platforms,
        'placement_class': f'social-share-placement-{settings.placement_position}',
        'button_style': settings.button_style,
        'button_size': settings.button_size,
        'layout_direction': settings.layout_direction,
        'show_title': settings.show_title,
        'mobile_visibility': settings.mobile_visibility,
        'widget_css_classes': ' '.join(css_classes),
    }


@register.simple_tag
def auto_social_share_buttons(page_type, content_type=None, object_id=None):
    """
    Automatically render share buttons based on merchant settings.

    Usage in product template:
        {% load social_share_tags %}
        {% auto_social_share_buttons 'product' content_type='product' object_id=product.id %}

    Returns empty string if disabled for this page type.
    """
    settings = SocialSharingSettings.get_settings()

    # Check if enabled for this page type
    enabled_map = {
        'product': settings.enable_on_products,
        'category': settings.enable_on_categories,
        'blog_post': settings.enable_on_blog_posts,
        'page': settings.enable_on_pages,
    }

    if not enabled_map.get(page_type, False):
        return ''

    # Render the widget
    from django.template.loader import render_to_string
    from django.template import Context

    context = Context({
        'content_type': content_type,
        'object_id': object_id,
    })

    return mark_safe(render_to_string('social_sharing/auto_include.html', context.flatten()))


@register.simple_tag
def social_share_enabled(page_type):
    """
    Check if social sharing is enabled for a page type.

    Usage:
        {% social_share_enabled 'product' as enabled %}
        {% if enabled %}
            ... render share UI ...
        {% endif %}
    """
    settings = SocialSharingSettings.get_settings()

    enabled_map = {
        'product': settings.enable_on_products,
        'category': settings.enable_on_categories,
        'blog_post': settings.enable_on_blog_posts,
        'page': settings.enable_on_pages,
    }

    return enabled_map.get(page_type, False)
