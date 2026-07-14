"""
Helper module for OAuth providers summary in Site Settings admin.
This generates the OAuth providers tab content using CSS classes instead of inline styles.
"""

from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _


def generate_oauth_providers_summary():
    """
    Generate OAuth providers summary HTML using CSS classes.
    Returns formatted HTML for the Authentication tab.
    """
    try:
        from accounts.models import OAuthProviderSettings

        # Get OAuth provider statistics
        total_providers = OAuthProviderSettings.objects.count()
        enabled_providers = OAuthProviderSettings.objects.filter(enabled=True).count()
        OAuthProviderSettings.objects.filter(is_configured=True).count()
        active_providers = OAuthProviderSettings.objects.filter(enabled=True, is_configured=True)

        # Build status summary
        summary_parts = []

        # Overall status
        if total_providers == 0:
            # Providers not yet initialized — auto-initialize them now
            # This handles legacy installs that predate the install.sh init step
            _auto_initialize_oauth_providers()
            total_providers = OAuthProviderSettings.objects.count()

            if total_providers == 0:
                summary_parts.append(f"""
                    <div class="oauth-provider-card">
                        <span class="oauth-provider-status warning">
                            <i class="fas fa-exclamation-triangle"></i> {_("Could not initialize OAuth providers. Please contact support.")}
                        </span>
                    </div>
                """)
        if total_providers > 0 and enabled_providers == 0:
            summary_parts.append(f"""
                <div class="oauth-provider-card">
                    <span class="oauth-provider-status disabled">
                        <i class="fas fa-circle"></i> {_("No social login providers enabled")}
                    </span>
                    <p style="margin-top: 8px;">
                        {_("Email/password authentication is always available. Enable social providers below to offer customers more login options.")}
                    </p>
                </div>
            """)
        elif enabled_providers > 0:
            summary_parts.append(f"""
                <div class="oauth-provider-card">
                    <span class="oauth-provider-status active">
                        <i class="fas fa-check-circle"></i> {_(f"{enabled_providers} social login provider(s) active")}
                    </span>
                </div>
            """)

        # Active providers list
        if active_providers.exists():
            provider_icons = {
                "google": '<i class="fab fa-google"></i>',
                "apple": '<i class="fab fa-apple"></i>',
                "microsoft": '<i class="fab fa-microsoft"></i>',
            }

            provider_badges = []
            for provider in active_providers.order_by("button_order"):
                icon = provider_icons.get(provider.provider, '<i class="fas fa-key"></i>')
                provider_badges.append(f"""
                    <span class="oauth-provider-badge">
                        {icon} {provider.display_name}
                    </span>
                """)

            summary_parts.append(f"""
                <div class="oauth-provider-card">
                    <div style="font-weight: 600; margin-bottom: 10px;">
                        {_("Active Social Login Providers")}:
                    </div>
                    <div>
                        {"".join(provider_badges)}
                    </div>
                </div>
            """)

        # Configuration warnings
        enabled_not_configured = OAuthProviderSettings.objects.filter(
            enabled=True, is_configured=False
        )

        if enabled_not_configured.exists():
            warning_providers = []
            for provider in enabled_not_configured:
                warning_providers.append(f"<li>{provider.get_provider_display()}</li>")

            summary_parts.append(f"""
                <div class="oauth-warning-box">
                    <div class="oauth-warning-title">
                        <i class="fas fa-exclamation-triangle"></i> {_("Configuration Required")}
                    </div>
                    <div class="oauth-warning-content">
                        {_("The following providers are enabled but missing OAuth credentials")}:
                        <ul class="oauth-warning-list">
                            {"".join(warning_providers)}
                        </ul>
                    </div>
                </div>
            """)

        # Check if site URL is configured in SiteSettings
        from core.models import SiteSettings

        site_settings = SiteSettings.get_settings()
        if not site_settings.site_url or site_settings.site_url in (
            "http://example.com",
            "https://example.com",
            "",
        ):
            summary_parts.append(f"""
                <div class="oauth-warning-box">
                    <div class="oauth-warning-title">
                        <i class="fas fa-exclamation-triangle"></i> {_("Site URL Not Configured")}
                    </div>
                    <div class="oauth-warning-content">
                        {_("Update your site URL in the")} <a href="#" onclick="document.querySelector('[data-tab=general]').click(); return false;">{_("General tab")}</a> {_("for OAuth to work correctly")}.
                    </div>
                </div>
            """)

        # OAuth Dashboard link
        oauth_dashboard_url = reverse("accounts:oauth_dashboard")
        view_accounts_url = reverse("admin:socialaccount_socialaccount_changelist")

        # Translate strings outside of f-string
        title_text = _("Social Authentication Management")
        description_text = _(
            "Configure which social login providers (Google, Apple, Microsoft) are available to customers"
        )
        dashboard_btn_text = _("Open OAuth Dashboard")
        accounts_btn_text = _("View Connected Accounts")
        setup_guide_title = _("Setup Guide")
        wizard_intro = _(
            "Visit the OAuth Dashboard to configure social login providers using our step-by-step wizard. Each provider has detailed instructions for:"
        )
        step1_text = _("Creating developer accounts")
        step2_text = _("Generating OAuth credentials")
        step3_text = _("Configuring callback URLs")
        step4_text = _("Testing the integration")
        tip_label = _("Tip:")
        tip_text = _(
            "Start with Google OAuth - it's free, unlimited, and trusted by billions of users."
        )

        summary_parts.append(f'''
            <div class="oauth-management-box">
                <div class="oauth-management-title">
                    <i class="fas fa-shield-alt"></i> {title_text}
                </div>
                <div class="oauth-management-description">
                    {description_text}
                </div>
                <div class="oauth-management-buttons">
                    <a href="{oauth_dashboard_url}" class="button default">
                        <i class="fas fa-shield-alt"></i> {dashboard_btn_text}
                    </a>
                    <a href="{view_accounts_url}" class="button secondary">
                        <i class="fas fa-users"></i> {accounts_btn_text}
                    </a>
                </div>

                <div class="oauth-setup-guide">
                    <div class="oauth-setup-guide-title">
                        <i class="fas fa-magic"></i> {setup_guide_title}:
                    </div>
                    <p style="color: var(--body-fg); margin: 10px 0;">
                        {wizard_intro}
                    </p>
                    <ul style="color: var(--body-fg);">
                        <li>{step1_text}</li>
                        <li>{step2_text}</li>
                        <li>{step3_text}</li>
                        <li>{step4_text}</li>
                    </ul>
                    <p style="color: var(--body-fg); margin: 10px 0;">
                        <strong>{tip_label}</strong> {tip_text}
                    </p>
                </div>
            </div>
        ''')

        return format_html("".join(summary_parts))

    except ImportError:
        return format_html("""
            <div class="oauth-warning-box">
                <div class="oauth-warning-title">
                    <i class="fas fa-times-circle"></i> {_('Social authentication module not available')}
                </div>
            </div>
        """)
    except Exception as e:
        return format_html(f"""
            <div class="oauth-warning-box">
                <div class="oauth-warning-title">
                    <i class="fas fa-times-circle"></i> {_("Error loading OAuth providers")}
                </div>
                <div class="oauth-warning-content">{str(e)}</div>
            </div>
        """)


def _auto_initialize_oauth_providers():
    """
    Auto-initialize default OAuth provider settings if none exist.
    Fallback for legacy installs that predate the install.sh init step.
    """
    try:
        from django.contrib.sites.models import Site

        from accounts.models import OAuthProviderSettings

        providers = [
            {"provider": "google", "display_name": "Google", "button_order": 1, "enabled": False},
            {"provider": "apple", "display_name": "Apple", "button_order": 2, "enabled": False},
            {
                "provider": "microsoft",
                "display_name": "Microsoft",
                "button_order": 3,
                "enabled": False,
            },
        ]
        for provider_data in providers:
            OAuthProviderSettings.objects.get_or_create(
                provider=provider_data["provider"],
                defaults=provider_data,
            )

        # Ensure default site exists (required by django-allauth)
        Site.objects.get_or_create(
            pk=1,
            defaults={"domain": "example.com", "name": "My Shop"},
        )
    except Exception:
        pass
