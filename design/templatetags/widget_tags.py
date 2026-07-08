"""
Template tags and filters for header/footer widgets.
"""
from django import template
from urllib.parse import urlparse
import json
import re

register = template.Library()


@register.filter
def get_site_variable(site_settings, variable_name):
    """
    Get a site settings value by variable name.
    Usage: {{ site_settings|get_site_variable:variable }}
    """
    if not site_settings:
        return ''

    # Handle special method-based values
    if variable_name == 'full_address':
        return site_settings.get_full_address() or ''
    elif variable_name == 'support_email':
        return site_settings.get_support_email() or ''
    else:
        return getattr(site_settings, variable_name, '') or ''


@register.filter
def parse_typography(value):
    """
    Parse typography JSON or CSS string and return CSS string.
    Handles both JSON format (new) and CSS string format (legacy).
    Usage: {{ config.typography|parse_typography }}
    """
    if not value:
        return ''

    # If it's already a dict, use it directly
    if isinstance(value, dict):
        typo = value
    elif isinstance(value, str):
        # Try to parse as JSON first
        try:
            typo = json.loads(value)
        except (json.JSONDecodeError, TypeError):
            # If JSON parse fails, check if it's already a CSS string
            # CSS strings contain property: value; patterns
            if ':' in value and ';' in value:
                # It's already a CSS string, return as-is
                return value
            return ''
    else:
        return ''

    # Build CSS from JSON object
    css_parts = []

    if typo.get('fontFamily'):
        css_parts.append(f"font-family: {typo['fontFamily']};")
    if typo.get('fontSize'):
        css_parts.append(f"font-size: {typo['fontSize']};")
    if typo.get('fontWeight'):
        css_parts.append(f"font-weight: {typo['fontWeight']};")
    if typo.get('lineHeight'):
        css_parts.append(f"line-height: {typo['lineHeight']};")
    if typo.get('letterSpacing'):
        css_parts.append(f"letter-spacing: {typo['letterSpacing']};")

    return ' '.join(css_parts)


@register.filter
def is_link_type(variable_name):
    """Check if variable should be rendered as a link"""
    url_types = ['site_url', 'facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url']
    email_types = ['admin_email', 'support_email']
    phone_types = ['phone_number']
    return variable_name in url_types + email_types + phone_types


@register.filter
def get_link_href(value, variable_name):
    """Get the href for a linkable variable"""
    if variable_name in ['admin_email', 'support_email']:
        return f'mailto:{value}'
    elif variable_name == 'phone_number':
        return f'tel:{value}'
    else:
        return value


@register.filter
def is_external_link(variable_name):
    """Check if link should open in new tab"""
    return variable_name in ['site_url', 'facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url']


@register.filter
def phone_href(value):
    """
    Convert a phone number to a tel: href value.
    Strips everything except digits and leading +.
    Usage: {{ config.phone|phone_href }}
    Example: "+1 (555) 123-4567" -> "+15551234567"
    """
    if not value:
        return ''
    # Keep only + (if leading) and digits
    cleaned = re.sub(r'[^\d+]', '', str(value))
    # Ensure + only appears at the start
    if '+' in cleaned:
        cleaned = '+' + cleaned.replace('+', '')
    return cleaned


@register.filter
def validate_css_color(value):
    """
    Validate a CSS color value, returning it only if safe.
    Allows hex colors, rgb/rgba, hsl/hsla, and named colors.
    Returns empty string if the value contains suspicious content.
    Usage: {{ item.badge_color|validate_css_color }}
    """
    if not value:
        return ''
    value = str(value).strip()
    # Allow hex colors
    if re.match(r'^#[0-9a-fA-F]{3,8}$', value):
        return value
    # Allow rgb/rgba/hsl/hsla functions
    if re.match(r'^(rgb|rgba|hsl|hsla)\([^)]+\)$', value):
        return value
    # Allow CSS named colors (basic check: alpha only, max 20 chars)
    if re.match(r'^[a-zA-Z]{1,20}$', value):
        return value
    # Reject anything else (potential CSS injection)
    return ''


# Maps payment method slugs to their SVG icon paths under providers_common/images/brands/payment_methods/
PAYMENT_METHOD_ICONS = {
    # Cards
    'visa': {'path': 'cards/visa.svg', 'label': 'Visa'},
    'mastercard': {'path': 'cards/mastercard.svg', 'label': 'Mastercard'},
    'amex': {'path': 'cards/american-express.svg', 'label': 'American Express'},
    'discover': {'path': 'cards/discover.svg', 'label': 'Discover'},
    'diners': {'path': 'cards/diners.svg', 'label': 'Diners Club'},
    'jcb': {'path': 'cards/jcb.svg', 'label': 'JCB'},
    'unionpay': {'path': 'cards/unionpay.svg', 'label': 'UnionPay'},
    'maestro': {'path': 'cards/maestro.svg', 'label': 'Maestro'},
    # Wallets
    'apple_pay': {'path': 'wallets/apple-pay.svg', 'label': 'Apple Pay'},
    'google_pay': {'path': 'wallets/google-pay.svg', 'label': 'Google Pay'},
    'samsung_pay': {'path': 'wallets/samsung-pay.svg', 'label': 'Samsung Pay'},
    # Alternative
    'paypal': {'path': 'alternative/paypal.svg', 'label': 'PayPal'},
    'klarna': {'path': 'alternative/klarna.svg', 'label': 'Klarna'},
    'ideal': {'path': 'alternative/ideal.svg', 'label': 'iDEAL'},
    'sepa': {'path': 'alternative/sepa.svg', 'label': 'SEPA'},
    'twint': {'path': 'alternative/twint.svg', 'label': 'TWINT'},
    'eps': {'path': 'alternative/eps.svg', 'label': 'EPS'},
    'giropay': {'path': 'alternative/giropay.svg', 'label': 'Giropay'},
    'bancontact': {'path': 'alternative/bancontact.svg', 'label': 'Bancontact'},
    'alipay': {'path': 'alternative/alipay.svg', 'label': 'Alipay'},
    'wechat_pay': {'path': 'alternative/wechat-pay.svg', 'label': 'WeChat Pay'},
}


@register.simple_tag
def get_payment_method_icons(config):
    """
    Get payment method icons for the payment widget.
    Supports manual config list, auto-detection from active providers,
    and backward-compatible show_X boolean flags.
    Returns list of dicts with 'static_path' and 'label'.
    """
    from django.templatetags.static import static

    methods = []

    if config.get('auto_detect'):
        try:
            from payment_providers.models import PaymentProviderAccount
            active_providers = PaymentProviderAccount.objects.filter(
                is_active=True, connection_status='connected'
            )
            seen = set()
            for provider in active_providers:
                for country_methods in provider.enabled_payment_methods.values():
                    for method_slug in country_methods:
                        if method_slug not in seen and method_slug in PAYMENT_METHOD_ICONS:
                            icon_info = PAYMENT_METHOD_ICONS[method_slug]
                            methods.append({
                                'static_path': static(f'providers_common/images/brands/payment_methods/{icon_info["path"]}'),
                                'label': icon_info['label'],
                            })
                            seen.add(method_slug)
        except Exception:
            pass

    # Also add manually configured methods (config.methods is a list of slugs)
    if config.get('methods'):
        seen = {m['label'] for m in methods}
        for slug in config['methods']:
            if slug in PAYMENT_METHOD_ICONS:
                icon_info = PAYMENT_METHOD_ICONS[slug]
                if icon_info['label'] not in seen:
                    methods.append({
                        'static_path': static(f'providers_common/images/brands/payment_methods/{icon_info["path"]}'),
                        'label': icon_info['label'],
                    })
                    seen.add(icon_info['label'])

    # Backward compatibility: support legacy show_X boolean flags
    if not methods:
        legacy_map = {
            'show_visa': 'visa',
            'show_mastercard': 'mastercard',
            'show_amex': 'amex',
            'show_paypal': 'paypal',
        }
        for flag, slug in legacy_map.items():
            if config.get(flag):
                icon_info = PAYMENT_METHOD_ICONS[slug]
                methods.append({
                    'static_path': static(f'providers_common/images/brands/payment_methods/{icon_info["path"]}'),
                    'label': icon_info['label'],
                })

    return methods


# Known social platforms with their FontAwesome icons
SOCIAL_PLATFORMS = {
    'facebook': {'icon': 'fab fa-facebook-f', 'label': 'Facebook'},
    'twitter': {'icon': 'fab fa-twitter', 'label': 'Twitter'},
    'instagram': {'icon': 'fab fa-instagram', 'label': 'Instagram'},
    'youtube': {'icon': 'fab fa-youtube', 'label': 'YouTube'},
    'linkedin': {'icon': 'fab fa-linkedin-in', 'label': 'LinkedIn'},
    'pinterest': {'icon': 'fab fa-pinterest-p', 'label': 'Pinterest'},
    'tiktok': {'icon': 'fab fa-tiktok', 'label': 'TikTok'},
    'whatsapp': {'icon': 'fab fa-whatsapp', 'label': 'WhatsApp'},
    'threads': {'icon': 'fab fa-threads', 'label': 'Threads'},
    'discord': {'icon': 'fab fa-discord', 'label': 'Discord'},
    'telegram': {'icon': 'fab fa-telegram-plane', 'label': 'Telegram'},
    'snapchat': {'icon': 'fab fa-snapchat-ghost', 'label': 'Snapchat'},
    'reddit': {'icon': 'fab fa-reddit-alien', 'label': 'Reddit'},
    'tumblr': {'icon': 'fab fa-tumblr', 'label': 'Tumblr'},
    'vimeo': {'icon': 'fab fa-vimeo-v', 'label': 'Vimeo'},
    'twitch': {'icon': 'fab fa-twitch', 'label': 'Twitch'},
}


@register.simple_tag
def get_social_links(config):
    """
    Get social links for the social widget.
    Supports new 'links' list format and legacy per-platform URL fields.
    Returns list of dicts with 'url', 'icon', 'label'.
    """
    links = []

    # New format: config.links is a list of {platform, url, icon?, label?}
    if config.get('links'):
        for link in config['links']:
            platform = link.get('platform', '')
            platform_info = SOCIAL_PLATFORMS.get(platform, {})
            links.append({
                'url': link.get('url', '#'),
                'icon': link.get('icon') or platform_info.get('icon', 'fas fa-link'),
                'label': link.get('label') or platform_info.get('label', platform.title()),
            })
        return links

    # Legacy format: per-platform URL fields (facebook, twitter, etc.)
    for platform, info in SOCIAL_PLATFORMS.items():
        url = config.get(platform)
        if url:
            links.append({
                'url': url,
                'icon': info['icon'],
                'label': info['label'],
            })

    return links


# Preset trust badge types (matching page_builder element pattern)
TRUST_BADGE_PRESETS = {
    'secure_checkout': {'icon': 'fas fa-lock', 'label': 'Secure Checkout'},
    'money_back': {'icon': 'fas fa-undo-alt', 'label': 'Money-Back Guarantee'},
    'free_shipping': {'icon': 'fas fa-truck', 'label': 'Free Shipping'},
    'fast_delivery': {'icon': 'fas fa-shipping-fast', 'label': 'Fast Delivery'},
    'support_24_7': {'icon': 'fas fa-headset', 'label': '24/7 Support'},
    'quality': {'icon': 'fas fa-medal', 'label': 'Quality Guaranteed'},
    'ssl': {'icon': 'fas fa-shield-alt', 'label': 'SSL Secure'},
    'satisfaction': {'icon': 'fas fa-thumbs-up', 'label': '100% Satisfaction'},
    'verified': {'icon': 'fas fa-check-circle', 'label': 'Verified Seller'},
}


@register.simple_tag
def get_trust_badges(config):
    """
    Get trust badges for the trust badges widget.
    Supports new 'badges' array format and legacy show_X boolean flags.
    Returns list of dicts with 'icon', 'title', 'description'.
    """
    badges = []

    # New format: config.badges is a list of {type, icon?, title?, description?}
    if config.get('badges'):
        for badge in config['badges']:
            badge_type = badge.get('type', 'custom')
            preset = TRUST_BADGE_PRESETS.get(badge_type, {})
            badges.append({
                'icon': badge.get('icon') or preset.get('icon', 'fas fa-star'),
                'title': badge.get('title') or preset.get('label', ''),
                'description': badge.get('description', ''),
                'image': badge.get('image', ''),
            })
        return badges

    # Legacy format: boolean flags
    if config.get('show_secure') or config.get('show_ssl'):
        badges.append(TRUST_BADGE_PRESETS['secure_checkout'])
    if config.get('show_guarantee') or config.get('show_money_back'):
        badges.append(TRUST_BADGE_PRESETS['money_back'])
    if config.get('show_shipping'):
        badges.append(TRUST_BADGE_PRESETS['free_shipping'])
    if config.get('show_support'):
        badges.append(TRUST_BADGE_PRESETS['support_24_7'])

    return badges


@register.filter
def safe_url(url):
    """
    Validate a URL, allowing only safe protocols.
    Returns '#' for dangerous URLs (javascript:, data:, vbscript:).
    Usage: {{ link.url|safe_url }}
    """
    if not url:
        return '#'
    url = str(url).strip()
    # Allow relative URLs and anchors
    if url.startswith('/') or url.startswith('#') or url.startswith('?'):
        return url
    # Parse and check protocol
    try:
        parsed = urlparse(url)
        if parsed.scheme and parsed.scheme.lower() not in ('http', 'https', 'mailto', 'tel'):
            return '#'
    except Exception:
        return '#'
    return url
