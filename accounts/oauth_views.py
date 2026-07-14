"""
OAuth Provider Dashboard and Wizard Views
"""

from allauth.socialaccount.models import SocialApp
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.sites.models import Site
from django.db import transaction
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

from .models import OAuthProviderSettings

# Provider configuration data
PROVIDER_CONFIGS = {
    "google": {
        "name": "Google",
        "display_name": "Google Sign-In",
        "icon": "fab fa-google",
        "color": "#4285f4",
        "signup_url": "https://console.cloud.google.com",
        "dashboard_url": "https://console.cloud.google.com/apis/credentials",
        "docs_url": "https://developers.google.com/identity/protocols/oauth2",
        "free_tier": "Unlimited OAuth requests",
        "paid_tier": "Free for authentication",
        "requires": ["client_id", "client_secret"],
        "description": "Let customers sign in with their Google account. Google OAuth is free, reliable, and widely trusted by users worldwide.",
        "benefits": [
            "Most popular social login option",
            "Completely free - no usage limits",
            "Trusted by billions of users",
            "Fast and reliable authentication",
            "Automatic email verification",
        ],
        "callback_url_template": "{domain}/accounts/google/login/callback/",
    },
    "apple": {
        "name": "Apple",
        "display_name": "Sign in with Apple",
        "icon": "fab fa-apple",
        "color": "#000000",
        "signup_url": "https://developer.apple.com/account",
        "dashboard_url": "https://developer.apple.com/account/resources/identifiers/list/serviceId",
        "docs_url": "https://developer.apple.com/sign-in-with-apple/",
        "free_tier": "Unlimited OAuth requests",
        "paid_tier": "Requires Apple Developer Account ($99/year)",
        "requires": ["client_id", "team_id", "key_id", "certificate"],
        "description": "Enable Sign in with Apple for iOS users and privacy-conscious customers. Required for iOS apps, optional for web.",
        "benefits": [
            "Required for iOS applications",
            "Privacy-focused (email relay option)",
            "Seamless iOS integration",
            "Trusted by Apple users",
            "High conversion rates on Apple devices",
        ],
        "callback_url_template": "{domain}/accounts/apple/login/callback/",
    },
    "microsoft": {
        "name": "Microsoft",
        "display_name": "Sign in with Microsoft",
        "icon": "fab fa-microsoft",
        "color": "#00a4ef",
        "signup_url": "https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade",
        "dashboard_url": "https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade",
        "docs_url": "https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow",
        "free_tier": "Unlimited OAuth requests",
        "paid_tier": "Free for authentication",
        "requires": ["client_id", "client_secret", "tenant"],
        "description": "Allow customers to sign in with their Microsoft, Outlook, or Office 365 accounts. Popular with business customers.",
        "benefits": [
            "Popular with business customers",
            "Free unlimited authentication",
            "Access to Microsoft ecosystem",
            "Enterprise-grade security",
            "Works with personal and work accounts",
        ],
        "callback_url_template": "{domain}/accounts/microsoft/login/callback/",
    },
}


@staff_member_required
def oauth_dashboard(request):
    """OAuth provider dashboard showing all providers and their status"""

    # Get all provider settings
    providers = OAuthProviderSettings.objects.all().order_by("button_order")

    # Get statistics
    total_providers = providers.count()
    enabled_providers = providers.filter(enabled=True).count()
    configured_providers = providers.filter(is_configured=True).count()
    active_providers = providers.filter(enabled=True, is_configured=True).count()

    # Get social apps for configuration status
    configured_apps = {app.provider: app for app in SocialApp.objects.all()}

    # Build provider cards
    provider_cards = []
    for provider in providers:
        config = PROVIDER_CONFIGS.get(provider.provider, {})
        social_app = configured_apps.get(provider.provider)

        card = {
            "provider": provider,
            "config": config,
            "social_app": social_app,
            "is_configured": provider.is_configured,
            "is_enabled": provider.enabled,
            "is_active": provider.enabled and provider.is_configured,
            "wizard_url": f"/accounts/oauth/wizard/{provider.provider}/",
        }
        provider_cards.append(card)

    # Get current site for callback URLs
    site = Site.objects.get_current()

    context = {
        "title": _("OAuth Provider Dashboard"),
        "total_providers": total_providers,
        "enabled_providers": enabled_providers,
        "configured_providers": configured_providers,
        "active_providers": active_providers,
        "provider_cards": provider_cards,
        "site": site,
    }

    return render(request, "admin/accounts/oauth_dashboard.html", context)


@staff_member_required
def oauth_provider_wizard(request, provider_type):
    """Setup wizard for OAuth providers"""

    if provider_type not in PROVIDER_CONFIGS:
        messages.error(request, _("Invalid provider type"))
        return redirect("accounts:oauth_dashboard")

    provider_config = PROVIDER_CONFIGS[provider_type]

    # Get or create provider settings
    provider_settings, created = OAuthProviderSettings.objects.get_or_create(
        provider=provider_type,
        defaults={"display_name": provider_config["display_name"], "enabled": False},
    )

    # Get existing social app if any
    try:
        social_app = SocialApp.objects.get(provider=provider_type)
    except SocialApp.DoesNotExist:
        social_app = None

    # Get current site
    site = Site.objects.get_current()

    # Handle form submission
    if request.method == "POST":
        step = request.POST.get("step")

        if step == "final":
            try:
                with transaction.atomic():
                    # Create or update SocialApp
                    if social_app is None:
                        social_app = SocialApp(provider=provider_type, name=provider_config["name"])

                    social_app.client_id = request.POST.get("client_id", "")
                    social_app.secret = request.POST.get("client_secret", "")
                    social_app.save()

                    # Add current site to the app
                    if site not in social_app.sites.all():
                        social_app.sites.add(site)

                    # Update provider settings
                    provider_settings.enabled = request.POST.get("is_active") == "on"
                    provider_settings.button_order = int(request.POST.get("button_order", 0))
                    provider_settings.configuration_notes = request.POST.get("notes", "")
                    provider_settings.save()

                    messages.success(
                        request, _(f"{provider_config['name']} has been configured successfully!")
                    )
                    return redirect("accounts:oauth_dashboard")

            except Exception as e:
                messages.error(request, _(f"Error saving configuration: {str(e)}"))

    # Determine current step
    step = int(request.GET.get("step", 1))

    # Generate callback URL
    protocol = "https" if request.is_secure() else "http"
    domain = f"{protocol}://{site.domain}"
    callback_url = provider_config["callback_url_template"].format(domain=domain)

    context = {
        "title": _(f"Setup {provider_config['name']}"),
        "provider_type": provider_type,
        "provider_config": provider_config,
        "provider_settings": provider_settings,
        "social_app": social_app,
        "step": step,
        "site": site,
        "callback_url": callback_url,
        "redirect_uri": callback_url,  # Alias for clarity
    }

    return render(request, "admin/accounts/oauth_wizard.html", context)
