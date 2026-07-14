from django import template

from ..models import SiteSettings

register = template.Library()


@register.simple_tag
def get_site_settings():
    """
    Get the current site settings instance
    Usage: {% get_site_settings as site_settings %}
    """
    return SiteSettings.get_settings()


@register.filter
def get_favicon_url(site_settings):
    """
    Get the favicon URL if it exists
    Usage: {{ site_settings|get_favicon_url }}
    """
    if site_settings:
        return site_settings.get_favicon_url()
    return None


@register.filter
def get_site_logo_url(site_settings, size=None):
    """
    Get the site logo URL at a specific size.
    Usage: {{ site_settings|get_site_logo_url:'header' }}

    Available sizes: 'header', 'footer', 'email', 'square', 'original'
    """
    if site_settings:
        return site_settings.get_site_logo_url(size)
    return None


@register.inclusion_tag("core/site_logo.html")
def site_logo(size="header", css_class="", link_url="/", alt_text=None):
    """
    Render the site logo with optional link.
    Usage: {% site_logo size='header' css_class='custom-logo' link_url='/' %}

    Available sizes: 'header', 'footer', 'email', 'square'
    """
    site_settings = SiteSettings.get_settings()

    logo_url = None
    is_svg = False

    if site_settings and site_settings.site_logo:
        logo_url = site_settings.get_site_logo_url(size)
        is_svg = site_settings.site_logo.mime_type == "image/svg+xml"

    # Default alt text from site name
    if not alt_text and site_settings:
        alt_text = site_settings.site_name

    return {
        "site_settings": site_settings,
        "logo_url": logo_url,
        "is_svg": is_svg,
        "size": size,
        "css_class": css_class,
        "link_url": link_url,
        "alt_text": alt_text or "Site Logo",
    }


@register.inclusion_tag("core/favicon_meta.html")
def favicon_meta():
    """
    Include favicon meta tags in templates
    Usage: {% favicon_meta %}
    """
    site_settings = SiteSettings.get_settings()

    # Pre-fetch favicon URLs for template
    favicon_asset = None
    favicon_16_url = None
    favicon_32_url = None
    favicon_180_url = None
    favicon_display_url = None
    is_svg = False
    is_ico = False

    if site_settings and site_settings.favicon:
        favicon_asset = site_settings.favicon
        mime_type = favicon_asset.mime_type or ""

        # Check file type
        is_svg = mime_type == "image/svg+xml"
        is_ico = mime_type in ("image/x-icon", "image/vnd.microsoft.icon")

        # Get appropriate URLs based on type
        if is_svg or is_ico:
            # Use original for SVG/ICO
            favicon_display_url = favicon_asset.get_display_url()
            favicon_16_url = favicon_display_url
            favicon_32_url = favicon_display_url
            favicon_180_url = favicon_display_url
        else:
            # Use optimized thumbnails for standard images
            favicon_16_url = favicon_asset.get_thumbnail("favicon-16")
            favicon_32_url = favicon_asset.get_thumbnail("favicon-32")
            favicon_180_url = favicon_asset.get_thumbnail("favicon-180")

    return {
        "site_settings": site_settings,
        "favicon_asset": favicon_asset,
        "favicon_16_url": favicon_16_url,
        "favicon_32_url": favicon_32_url,
        "favicon_180_url": favicon_180_url,
        "is_svg": is_svg,
        "is_ico": is_ico,
        "use_default": not favicon_asset,
    }


@register.filter
def format_duration(seconds):
    """
    Format a duration in seconds to a human-readable string.
    Usage: {{ job.duration_seconds|format_duration }}

    Examples:
        0 -> "Less than a second"
        42 -> "42 seconds"
        90 -> "1 minute, 30 seconds"
        3661 -> "1 hour, 1 minute"
    """
    try:
        seconds = int(seconds)
    except (TypeError, ValueError):
        return ""

    if seconds <= 0:
        return "Less than a second"

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    parts = []
    if hours:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if secs and not hours:
        # Skip seconds when showing hours (too much precision)
        parts.append(f"{secs} second{'s' if secs != 1 else ''}")

    return ", ".join(parts) if parts else "Less than a second"


@register.filter
def get_field_label(form, field_name):
    """
    Get the human-readable label for a form field.
    Usage: {{ form|get_field_label:'field_name' }}
    """
    if hasattr(form, "fields") and field_name in form.fields:
        return form.fields[field_name].label or field_name.replace("_", " ").title()
    return field_name.replace("_", " ").title()


@register.simple_tag(takes_context=True)
def get_2fa_grace_period_status(context):
    """
    Get the 2FA grace period status for the current user.
    Returns a dict with:
    - show_banner: bool - whether to show the grace period banner
    - days_remaining: int - days remaining in grace period
    - enforcement_level: str - 'required' or 'recommended'
    - mfa_enabled: bool - whether user has MFA enabled
    - profile_url: str - URL to staff profile

    Usage: {% get_2fa_grace_period_status as mfa_status %}
    """
    from django.utils import timezone

    request = context.get("request")
    if not request or not hasattr(request, "user"):
        return {"show_banner": False}

    user = request.user
    if not user.is_authenticated or not user.is_staff:
        return {"show_banner": False}

    try:
        settings = SiteSettings.get_settings()
    except Exception:
        return {"show_banner": False}

    # Check enforcement level
    if settings.staff_2fa_enforcement not in ("required", "recommended"):
        return {"show_banner": False}

    # Check if user has MFA enabled
    try:
        from allauth.mfa.utils import is_mfa_enabled

        mfa_enabled = is_mfa_enabled(user)
    except ImportError:
        mfa_enabled = False

    if mfa_enabled:
        return {"show_banner": False, "mfa_enabled": True}

    # Calculate grace period remaining (only for required enforcement)
    days_remaining = None
    if settings.staff_2fa_enforcement == "required" and settings.staff_2fa_enforcement_date:
        # For users created after enforcement date, use their date_joined
        if user.date_joined > settings.staff_2fa_enforcement_date:
            grace_end = user.date_joined + timezone.timedelta(
                days=settings.staff_2fa_grace_period_days
            )
        else:
            grace_end = settings.staff_2fa_enforcement_date + timezone.timedelta(
                days=settings.staff_2fa_grace_period_days
            )

        days_remaining = (grace_end - timezone.now()).days
        if days_remaining < 0:
            days_remaining = 0

    return {
        "show_banner": True,
        "days_remaining": days_remaining,
        "enforcement_level": settings.staff_2fa_enforcement,
        "mfa_enabled": mfa_enabled,
        "profile_url": "/admin/accounts/user/staff-profile/",
    }


@register.simple_tag
def get_admin_sso_context():
    """
    Get the SSO configuration context for the admin login page.

    Returns a dict with:
    - admin_sso_enabled: bool
    - admin_password_login_enabled: bool
    - sso_configured: bool - whether SSO provider is fully configured
    - sso_provider_name: str - display name for the SSO button
    - sso_login_url: str - URL to initiate OIDC login

    Usage: {% get_admin_sso_context as sso %}
    """
    try:
        site_settings = SiteSettings.get_settings()
    except Exception:
        return {
            "admin_sso_enabled": False,
            "admin_password_login_enabled": True,
        }

    context = {
        "admin_sso_enabled": site_settings.admin_sso_enabled,
        "admin_password_login_enabled": site_settings.admin_password_login_enabled,
        "sso_configured": False,
        "sso_provider_name": "SSO",
        "sso_login_url": "/oidc/authenticate/",
    }

    if site_settings.admin_sso_enabled:
        try:
            from enterprise_sso.models import SSOProviderConfig

            config = SSOProviderConfig.get_config()
            context["sso_configured"] = config.is_configured
            context["sso_provider_name"] = config.provider_name
        except Exception:
            pass

    return context
