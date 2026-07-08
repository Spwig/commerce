from django import template

register = template.Library()


@register.simple_tag
def get_sso_config_status():
    """
    Get the SSO provider configuration status for the admin settings page.

    Returns a dict with:
    - is_configured: bool
    - provider_name: str

    Usage: {% get_sso_config_status as sso_status %}
    """
    try:
        from enterprise_sso.models import SSOProviderConfig
        config = SSOProviderConfig.get_config()
        return {
            'is_configured': config.is_configured,
            'provider_name': config.provider_name,
        }
    except Exception:
        return {
            'is_configured': False,
            'provider_name': '',
        }
