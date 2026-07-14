import json

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.core.cache import cache
from django.forms import ModelForm, widgets
from django.shortcuts import render
from django.urls import path
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from media_library.widgets import MediaLibrarySelectWidget

from .admin_mixins import TranslatableAdminMixin
from .license import get_license_manager
from .models import APIToken, BugReport, CookieConsentLog, ErrorReport, LicenseStatus, SiteSettings
from .utils.locale_helpers import (
    get_currency_icon,
    get_grouped_currencies,
    get_grouped_languages,
    get_grouped_timezones,
    get_language_icon,
    get_timezone_icon,
)
from .widgets import SearchableSelectWidget, TranslatableFieldWidget


class SiteSettingsForm(ModelForm):
    """
    Custom form for Site Settings with improved widgets and validation.
    Dynamically populates currency, language, and timezone choices with Font Awesome icons.
    """

    class Meta:
        model = SiteSettings
        fields = "__all__"
        widgets = {
            # Note: favicon is handled by formfield_for_foreignkey in the admin class
            # Translatable fields with translation buttons
            "site_name": TranslatableFieldWidget(
                base_widget=widgets.TextInput(
                    attrs={"style": "width: 100%; max-width: 100%; box-sizing: border-box;"}
                )
            ),
            "site_tagline": TranslatableFieldWidget(
                base_widget=widgets.TextInput(
                    attrs={
                        "style": "width: 100%; max-width: 100%; box-sizing: border-box;",
                        "placeholder": "e.g., Quality Products, Unbeatable Prices",
                    }
                )
            ),
            "site_description": TranslatableFieldWidget(
                base_widget=widgets.Textarea(
                    attrs={
                        "rows": 3,
                        "style": "width: 100%; max-width: 100%; box-sizing: border-box;",
                    }
                )
            ),
            # Non-translatable fields
            "address_line_1": widgets.TextInput(
                attrs={"style": "width: 100%; max-width: 100%; box-sizing: border-box;"}
            ),
            "address_line_2": widgets.TextInput(
                attrs={"style": "width: 100%; max-width: 100%; box-sizing: border-box;"}
            ),
            "meta_title": widgets.TextInput(
                attrs={
                    "maxlength": 60,
                    "style": "width: 100%; max-width: 100%; box-sizing: border-box;",
                }
            ),
            "meta_description": widgets.Textarea(
                attrs={
                    "rows": 3,
                    "maxlength": 160,
                    "style": "width: 100%; max-width: 100%; box-sizing: border-box;",
                }
            ),
            "meta_keywords": widgets.TextInput(
                attrs={"style": "width: 100%; max-width: 100%; box-sizing: border-box;"}
            ),
            "maintenance_message": widgets.Textarea(
                attrs={"rows": 4, "style": "width: 100%; max-width: 100%; box-sizing: border-box;"}
            ),
            # Account creation settings
            "account_creation_message": TranslatableFieldWidget(
                base_widget=widgets.Textarea(
                    attrs={
                        "rows": 3,
                        "style": "width: 100%; max-width: 100%; box-sizing: border-box;",
                        "placeholder": "Create an account to track your order...",
                    }
                )
            ),
            # Cookie consent translatable fields
            "cookie_banner_title": TranslatableFieldWidget(
                base_widget=widgets.TextInput(
                    attrs={
                        "style": "width: 100%; max-width: 100%; box-sizing: border-box;",
                        "placeholder": "e.g., We use cookies",
                    }
                )
            ),
            "cookie_banner_text": TranslatableFieldWidget(
                base_widget=widgets.Textarea(
                    attrs={
                        "rows": 3,
                        "style": "width: 100%; max-width: 100%; box-sizing: border-box;",
                    }
                )
            ),
            "cookie_analytics_description": TranslatableFieldWidget(
                base_widget=widgets.Textarea(
                    attrs={
                        "rows": 2,
                        "style": "width: 100%; max-width: 100%; box-sizing: border-box;",
                    }
                )
            ),
            "cookie_marketing_description": TranslatableFieldWidget(
                base_widget=widgets.Textarea(
                    attrs={
                        "rows": 2,
                        "style": "width: 100%; max-width: 100%; box-sizing: border-box;",
                    }
                )
            ),
            "cookie_functional_description": TranslatableFieldWidget(
                base_widget=widgets.Textarea(
                    attrs={
                        "rows": 2,
                        "style": "width: 100%; max-width: 100%; box-sizing: border-box;",
                    }
                )
            ),
            # Leave dropdowns and other elements with natural sizing
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Currency field with Font Awesome currency icons
        currency_groups = get_grouped_currencies()
        self.fields["default_currency"].widget = SearchableSelectWidget(
            icon_callback=get_currency_icon, attrs={"data-placeholder": "Search currencies..."}
        )
        self.fields["default_currency"].widget.choices = [
            (_("Popular Currencies"), currency_groups["popular"]),
            (_("Other Currencies"), currency_groups["other"]),
        ]

        # Language field with Font Awesome language icon
        language_groups = get_grouped_languages()
        self.fields["default_language"].widget = SearchableSelectWidget(
            icon_callback=get_language_icon, attrs={"data-placeholder": "Search languages..."}
        )
        self.fields["default_language"].widget.choices = [
            (_("Admin Languages"), language_groups["admin"]),
            (_("Popular Languages"), language_groups["popular"]),
            (_("Other Languages"), language_groups["other"]),
        ]

        # Timezone field with Font Awesome regional globe icons
        timezone_groups = get_grouped_timezones()
        self.fields["default_timezone"].widget = SearchableSelectWidget(
            icon_callback=get_timezone_icon, attrs={"data-placeholder": "Search timezones..."}
        )
        self.fields["default_timezone"].widget.choices = [
            (_("Popular Timezones"), timezone_groups["popular"]),
            (_("Americas"), timezone_groups["americas"]),
            (_("Europe"), timezone_groups["europe"]),
            (_("Asia"), timezone_groups["asia"]),
            (_("Africa"), timezone_groups["africa"]),
            (_("Pacific"), timezone_groups["pacific"]),
            (_("Other"), timezone_groups["other"]),
        ]

        # Multi-currency fields are hidden when multi-currency is disabled,
        # so they must not be required (model defaults apply).
        self.fields["exchange_rate_sync_interval"].required = False
        self.fields["multi_currency_checkout_mode"].required = False

    def clean_sandbox_email_whitelist(self):
        """Validate sandbox email whitelist entries."""
        value = self.cleaned_data.get("sandbox_email_whitelist")
        if not value:
            return []
        from core.sandbox.email_guard import validate_whitelist

        is_valid, errors = validate_whitelist(value)
        if not is_valid:
            raise forms.ValidationError(errors)
        return value

    def clean_sandbox_sms_whitelist(self):
        """Validate sandbox SMS whitelist entries."""
        value = self.cleaned_data.get("sandbox_sms_whitelist")
        if not value:
            return []
        from core.sandbox.sms_guard import validate_sms_whitelist

        is_valid, errors = validate_sms_whitelist(value)
        if not is_valid:
            raise forms.ValidationError(errors)
        return value

    def clean(self):
        """Validate SiteSettings form data"""
        cleaned_data = super().clean()
        timing = cleaned_data.get("account_creation_timing")
        guest_checkout = cleaned_data.get("allow_guest_checkout")

        if timing == "post_purchase" and not guest_checkout:
            raise forms.ValidationError(
                {
                    "account_creation_timing": _(
                        "Post-purchase account creation requires guest checkout to be enabled."
                    )
                }
            )

        return cleaned_data


@admin.register(SiteSettings)
class SiteSettingsAdmin(TranslatableAdminMixin, admin.ModelAdmin):
    """
    Admin interface for Site Settings with organized fieldsets and translation support
    """

    form = SiteSettingsForm
    change_form_template = "admin/core/sitesettings/change_form.html"

    # Fields that can be translated
    translatable_fields = [
        "site_name",
        "site_tagline",
        "site_description",
        "cookie_banner_title",
        "cookie_banner_text",
        "cookie_analytics_description",
        "cookie_marketing_description",
        "cookie_functional_description",
        "account_creation_message",
    ]

    class Media:
        js = TranslatableAdminMixin.Media.js
        css = TranslatableAdminMixin.Media.css

    # Only allow editing the existing instance, not creating new ones
    def has_add_permission(self, request):
        # Only allow adding if no instance exists
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Never allow deletion of site settings
        return False

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Use MediaLibrarySelectWidget for the favicon and site_logo ForeignKey fields with auto-save"""
        if db_field.name in ("favicon", "site_logo"):
            # Get the instance pk for auto-save - try from URL first, then from existing settings
            object_id = request.resolver_match.kwargs.get("object_id")
            if not object_id:
                # Fallback: get the single SiteSettings instance
                settings = SiteSettings.objects.first()
                object_id = settings.pk if settings else ""

            return forms.ModelChoiceField(
                queryset=db_field.remote_field.model.objects.all(),
                widget=MediaLibrarySelectWidget(
                    attrs={
                        "folder": f"site/{db_field.name}",
                        # Auto-save configuration - saves immediately on selection
                        "auto_save_url": "/api/media/auto-save/",
                        "auto_save_app": "core",
                        "auto_save_model": "sitesettings",
                        "auto_save_pk": object_id,
                        "auto_save_field": db_field.name,
                    }
                ),
                required=False,
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Note: fieldsets are not used - the custom template renders tabs manually
    # Readonly fields are used by the template for dynamic content
    readonly_fields = (
        "created_at",
        "updated_at",
        "payment_methods_summary",
        "oauth_providers_summary",
        "email_accounts_summary",
    )

    list_display = ("site_name", "admin_email", "default_currency", "updated_at")

    # Custom method to ensure we redirect to the correct instance
    def changelist_view(self, request, extra_context=None):
        """
        Override changelist to redirect to the single settings instance
        """
        if SiteSettings.objects.exists():
            settings = SiteSettings.objects.first()
            from django.shortcuts import redirect
            from django.urls import reverse

            return redirect(reverse("admin:core_sitesettings_change", args=[settings.pk]))
        else:
            # If no settings exist, redirect to add form
            from django.shortcuts import redirect
            from django.urls import reverse

            return redirect(reverse("admin:core_sitesettings_add"))

    def response_change(self, request, obj):
        """
        Override to provide custom success message
        """
        response = super().response_change(request, obj)
        self.message_user(
            request, _(f"Site settings for '{obj.site_name}' have been updated successfully.")
        )
        return response

    def response_add(self, request, obj, post_url_continue=None):
        """
        Override to provide custom success message for new settings
        """
        response = super().response_add(request, obj, post_url_continue)
        self.message_user(
            request, _(f"Site settings for '{obj.site_name}' have been created successfully.")
        )
        return response

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        extra_context = extra_context or {}
        from email_system.models import EmailOutbox

        extra_context["held_email_count"] = EmailOutbox.objects.filter(status="held").count()
        return super().changeform_view(request, object_id, form_url, extra_context)

    def payment_methods_summary(self, obj):
        """Display payment providers status and management links"""
        from django.urls import reverse
        from django.utils.html import format_html

        try:
            from payment_providers.models import PaymentProviderAccount

            # Get payment provider statistics
            total_providers = PaymentProviderAccount.objects.count()
            active_providers = PaymentProviderAccount.objects.filter(is_active=True).count()

            # Build status summary
            summary_parts = []

            # Overall status
            if total_providers == 0:
                status_class = "status-error"
                status_text = str(_("No payment providers configured"))
            elif active_providers == 0:
                status_class = "status-warning"
                status_text = str(_("{} provider(s) configured but none active")).format(
                    total_providers
                )
            else:
                status_class = "status-success"
                status_text = str(_("{} of {} provider(s) active")).format(
                    active_providers, total_providers
                )

            summary_parts.append(f"""
                <div class="dashboard-stat-summary">
                    <span class="status-badge {status_class}">
                        📊 {status_text}
                    </span>
                </div>
            """)

            # Active providers list
            if active_providers > 0:
                active_provider_list = PaymentProviderAccount.objects.filter(
                    is_active=True
                ).select_related("component")
                provider_badges = []
                for provider in active_provider_list:
                    provider_name = provider.display_name or provider.component.name
                    env_mode = "test" if provider.test_mode else "live"
                    env_class = "status-warning" if provider.test_mode else "status-success"

                    provider_badges.append(f"""
                        <span class="provider-badge {env_class}">
                            {provider_name} <small>({env_mode})</small>
                        </span>
                    """)

                summary_parts.append(f"""
                    <div class="provider-list-section">
                        <div class="section-label">
                            {str(_("Active Payment Providers"))}:
                        </div>
                        <div class="badge-container">
                            {"".join(provider_badges)}
                        </div>
                    </div>
                """)

            # Management links
            dashboard_url = reverse("payment_providers:payment_dashboard")
            browse_url = reverse("payment_providers:provider_browse")
            manage_url = reverse("admin:payment_providers_paymentprovideraccount_changelist")
            transactions_url = reverse("admin:payment_providers_paymenttransaction_changelist")

            summary_parts.append(f'''
                <div class="dashboard-action-card">
                    <div class="card-title">
                        💳 {str(_("Payment Provider Management"))}
                    </div>
                    <div class="action-buttons">
                        <a href="{dashboard_url}" class="btn btn-primary btn-sm">
                            <i class="fas fa-chart-line"></i> {str(_("Dashboard"))}
                        </a>
                        <a href="{browse_url}" class="btn btn-success btn-sm">
                            <i class="fas fa-plus-circle"></i> {str(_("Install Provider"))}
                        </a>
                        <a href="{manage_url}" class="btn btn-secondary btn-sm">
                            <i class="fas fa-cog"></i> {str(_("Configure"))}
                        </a>
                        <a href="{transactions_url}" class="btn btn-secondary btn-sm">
                            <i class="fas fa-receipt"></i> {str(_("Transactions"))}
                        </a>
                    </div>
                </div>
            ''')

            return format_html("".join(summary_parts))

        except ImportError:
            return format_html(
                '<div class="error-message">❌ {}</div>',
                _("Payment providers module not available"),
            )
        except Exception as e:
            return format_html(
                '<div class="error-message">❌ {}: {}</div>',
                _("Error loading payment providers"),
                str(e),
            )

    payment_methods_summary.short_description = _("Payment Providers")

    def oauth_providers_summary(self, obj):
        """Display OAuth provider status and management links (using CSS classes per rules.md)"""
        from .admin_oauth_summary import generate_oauth_providers_summary

        return generate_oauth_providers_summary()

    def _oauth_providers_summary_old(self, obj):
        """OLD VERSION - DEPRECATED - keeping for reference"""
        from django.urls import reverse
        from django.utils.html import format_html

        try:
            from accounts.models import OAuthProviderSettings

            # Get OAuth provider statistics
            total_providers = OAuthProviderSettings.objects.count()
            enabled_providers = OAuthProviderSettings.objects.filter(enabled=True).count()
            OAuthProviderSettings.objects.filter(is_configured=True).count()
            active_providers = OAuthProviderSettings.objects.filter(
                enabled=True, is_configured=True
            )

            # Build status summary
            summary_parts = []

            # Overall status
            if total_providers == 0:
                status_color = "#ffc107"  # Yellow
                status_text = _("OAuth providers not initialized")
                summary_parts.append(f"""
                    <div style="margin-bottom: 15px;">
                        <span style="color: {status_color}; font-weight: bold; font-size: 14px;">
                            ⚠️ {status_text}
                        </span>
                        <p style="margin-top: 8px; color: #666; font-size: 12px;">
                            Run: <code style="background: #f5f5f5; padding: 2px 6px; border-radius: 3px;">python manage.py init_oauth_providers</code>
                        </p>
                    </div>
                """)
            elif enabled_providers == 0:
                status_color = "#6c757d"  # Gray
                status_text = _("No social login providers enabled")
                summary_parts.append(f"""
                    <div style="margin-bottom: 15px;">
                        <span style="color: {status_color}; font-weight: bold; font-size: 14px;">
                            ○ {status_text}
                        </span>
                        <p style="margin-top: 8px; color: #666; font-size: 12px;">
                            {_("Email/password authentication is always available. Enable social providers below to offer customers more login options.")}
                        </p>
                    </div>
                """)
            else:
                status_color = "#28a745"  # Green
                status_text = _(f"{enabled_providers} social login provider(s) active")
                summary_parts.append(f"""
                    <div style="margin-bottom: 15px;">
                        <span style="color: {status_color}; font-weight: bold; font-size: 14px;">
                            ✓ {status_text}
                        </span>
                    </div>
                """)

            # Active providers list
            if active_providers.exists():
                provider_icons = {
                    "google": "🔍",
                    "apple": "🍎",
                    "microsoft": "🪟",
                }

                provider_badges = []
                for provider in active_providers.order_by("button_order"):
                    icon = provider_icons.get(provider.provider, "🔐")
                    provider_badges.append(f"""
                        <span style="
                            display: inline-block;
                            background: #e9ecef;
                            padding: 6px 12px;
                            margin: 2px;
                            border-radius: 4px;
                            font-size: 13px;
                            border-left: 3px solid {status_color};
                        ">
                            {icon} {provider.display_name}
                        </span>
                    """)

                summary_parts.append(f"""
                    <div style="margin-bottom: 15px;">
                        <div style="font-weight: bold; margin-bottom: 5px; font-size: 12px; color: #666;">
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
                    <div style="
                        background: #fff3cd;
                        border: 1px solid #ffc107;
                        border-radius: 6px;
                        padding: 12px;
                        margin-bottom: 15px;
                    ">
                        <div style="font-weight: bold; color: #856404; margin-bottom: 5px;">
                            ⚠️ {_("Configuration Required")}
                        </div>
                        <div style="color: #856404; font-size: 12px;">
                            {_("The following providers are enabled but missing OAuth credentials")}:
                            <ul style="margin: 5px 0 0 20px; padding: 0;">
                                {"".join(warning_providers)}
                            </ul>
                        </div>
                    </div>
                """)

            # Check if site URL is configured in SiteSettings
            site_settings = SiteSettings.get_settings()
            if not site_settings.site_url or site_settings.site_url in (
                "http://example.com",
                "https://example.com",
                "",
            ):
                summary_parts.append(f"""
                    <div style="
                        background: #fff3cd;
                        border: 1px solid #ffc107;
                        border-radius: 6px;
                        padding: 12px;
                        margin-bottom: 15px;
                    ">
                        <div style="font-weight: bold; color: #856404; margin-bottom: 5px;">
                            ⚠️ {_("Site URL Not Configured")}
                        </div>
                        <div style="color: #856404; font-size: 12px;">
                            {_("Update your site URL in the")} <a href="#" onclick="document.querySelector(\\'[data-tab=general]\\').click(); return false;" style="color: #856404; text-decoration: underline;">{_("General tab")}</a> {_("for OAuth to work correctly")}.
                        </div>
                    </div>
                """)

            # Management links
            manage_providers_url = reverse("admin:accounts_oauthprovidersettings_changelist")
            manage_apps_url = reverse("admin:socialaccount_socialapp_changelist")
            add_app_url = reverse("admin:socialaccount_socialapp_add")
            view_accounts_url = reverse("admin:socialaccount_socialaccount_changelist")

            summary_parts.append(f'''
                <div style="
                    background: #f8f9fa;
                    padding: 15px;
                    border-radius: 6px;
                    border: 1px solid #dee2e6;
                ">
                    <div style="font-weight: bold; margin-bottom: 10px; color: #495057;">
                        🔐 {_("Social Authentication Management")}
                    </div>
                    <div style="margin-bottom: 10px; font-size: 12px; color: #666;">
                        {_("Configure which social login providers (Google, Apple, Microsoft) are available to customers")}
                    </div>
                    <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                        <a href="{manage_providers_url}"
                           style="
                               background: #28a745;
                               color: white;
                               padding: 8px 12px;
                               text-decoration: none;
                               border-radius: 4px;
                               font-size: 12px;
                               font-weight: 500;
                           ">
                            ⚙️ {_("Enable/Disable Providers")}
                        </a>
                        <a href="{add_app_url}"
                           style="
                               background: #007cba;
                               color: white;
                               padding: 8px 12px;
                               text-decoration: none;
                               border-radius: 4px;
                               font-size: 12px;
                               font-weight: 500;
                           ">
                            🔑 {_("Add OAuth Credentials")}
                        </a>
                        <a href="{manage_apps_url}"
                           style="
                               background: #6c757d;
                               color: white;
                               padding: 8px 12px;
                               text-decoration: none;
                               border-radius: 4px;
                               font-size: 12px;
                               font-weight: 500;
                           ">
                            📋 {_("Manage Credentials")}
                        </a>
                        <a href="{view_accounts_url}"
                           style="
                               background: #6c757d;
                               color: white;
                               padding: 8px 12px;
                               text-decoration: none;
                               border-radius: 4px;
                               font-size: 12px;
                               font-weight: 500;
                           ">
                            👥 {_("View Connected Accounts")}
                        </a>
                    </div>

                    <div style="
                        margin-top: 15px;
                        padding-top: 15px;
                        border-top: 1px solid #dee2e6;
                        font-size: 12px;
                        color: #666;
                    ">
                        <div style="font-weight: bold; margin-bottom: 5px; color: #495057;">
                            📚 {_("Quick Setup Guide")}:
                        </div>
                        <ol style="margin: 5px 0 0 20px; padding: 0; line-height: 1.6;">
                            <li>{_("Choose which providers to enable in")} <a href="{manage_providers_url}" style="color: #007cba;">OAuth Provider Settings</a></li>
                            <li>{_("Get OAuth credentials from provider")} (<a href="https://console.cloud.google.com" target="_blank" style="color: #007cba;">Google</a>, <a href="https://developer.apple.com" target="_blank" style="color: #007cba;">Apple</a>, <a href="https://portal.azure.com" target="_blank" style="color: #007cba;">Microsoft</a>)</li>
                            <li>{_("Add credentials in")} <a href="{manage_apps_url}" style="color: #007cba;">Social Applications</a></li>
                            <li>{_("Enable provider - customers will see it on login page")}</li>
                        </ol>
                    </div>
                </div>
            ''')

            return format_html("".join(summary_parts))

        except ImportError:
            return format_html("""
                <div style="color: #dc3545; font-weight: bold;">
                    ❌ {_('Social authentication module not available')}
                </div>
            """)
        except Exception as e:
            return format_html(f"""
                <div style="color: #dc3545;">
                    ❌ {_("Error loading OAuth providers")}: {str(e)}
                </div>
            """)

    oauth_providers_summary.short_description = _("Customer Authentication")

    def email_accounts_summary(self, obj):
        """Display email provider status and management links"""
        from django.urls import reverse
        from django.utils.html import format_html

        try:
            from email_system.models import EmailAccount

            # Get email account statistics
            total_accounts = EmailAccount.objects.count()
            active_accounts = EmailAccount.objects.filter(is_active=True).count()
            connected_accounts = EmailAccount.objects.filter(
                is_active=True, connection_status="connected"
            ).count()

            # Build status summary
            summary_parts = []

            # Overall status
            if total_accounts == 0:
                status_color = "#ffc107"  # Yellow
                status_text = _("No email providers connected")
                status_icon = "⚠️"
            elif connected_accounts == 0:
                status_color = "#dc3545"  # Red
                status_text = _(f"{total_accounts} provider(s) configured but none connected")
                status_icon = "❌"
            else:
                status_color = "#28a745"  # Green
                status_text = _(f"{connected_accounts} of {active_accounts} provider(s) connected")
                status_icon = "✅"

            summary_parts.append(f"""
                <div style="margin-bottom: 15px;">
                    <span style="color: {status_color}; font-weight: bold; font-size: 14px;">
                        {status_icon} {status_text}
                    </span>
                </div>
            """)

            # Active accounts list
            if connected_accounts > 0:
                active_list = EmailAccount.objects.filter(
                    is_active=True, connection_status="connected"
                ).order_by("-is_default", "from_email")

                account_badges = []
                for account in active_list:
                    badge_color = "#007bff" if account.is_default else "#6c757d"
                    default_marker = " ⭐ DEFAULT" if account.is_default else ""
                    account_badges.append(f"""
                        <span style="background-color: {badge_color}; color: white; padding: 4px 12px;
                                     border-radius: 4px; display: inline-block; margin: 4px 4px 4px 0;
                                     font-size: 12px; font-weight: 500;">
                            {account.component.name}: {account.from_email}{default_marker}
                        </span>
                    """)

                summary_parts.append(f"""
                    <div style="margin-bottom: 15px;">
                        <div style="margin-top: 8px;">
                            {"".join(account_badges)}
                        </div>
                    </div>
                """)

            # Quick actions
            manage_url = reverse("admin:email_system_emailaccount_changelist")
            queue_url = reverse("admin:email_system_emailoutbox_changelist")

            summary_parts.append(f'''
                <div style="margin-top: 15px;">
                    <a href="{manage_url}" class="button" style="margin-right: 8px;">
                        <i class="fas fa-cog"></i> {_("Manage Accounts")}
                    </a>
                    <a href="{queue_url}" class="button">
                        <i class="fas fa-inbox"></i> {_("View Queue")}
                    </a>
                </div>
            ''')

            return format_html("".join(summary_parts))

        except ImportError:
            return format_html('<p style="color: #dc3545;">{}</p>', _("Email system not installed"))
        except Exception as e:
            return format_html(
                '<p style="color: #dc3545;">{}: {}</p>', _("Error loading email accounts"), str(e)
            )

    email_accounts_summary.short_description = _("Email Provider Status")

    def change_view(self, request, object_id, form_url="", extra_context=None):
        """Override change_view to add payment methods, oauth providers, and shipping summary to context"""
        extra_context = extra_context or {}
        obj = self.get_object(request, object_id)
        if obj:
            extra_context["payment_methods_html"] = self.payment_methods_summary(obj)
            extra_context["oauth_providers_html"] = self.oauth_providers_summary(obj)

            # Add 2FA compliance data
            extra_context.update(self._get_2fa_compliance_data())

        # Add field-to-tab mapping for error navigation
        extra_context["field_tab_mapping_json"] = json.dumps(self.get_field_tab_mapping())

        # Add Domain & SSL configuration context
        try:
            from domain_ssl.models import DomainConfiguration

            extra_context["domain_ssl_config"] = DomainConfiguration.get_instance()
        except Exception:
            extra_context["domain_ssl_config"] = None

        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def _get_2fa_compliance_data(self):
        """Calculate 2FA compliance statistics for staff users"""
        from django.contrib.auth import get_user_model

        User = get_user_model()

        # Get all staff users
        staff_users = User.objects.filter(is_staff=True, is_active=True)
        total_staff = staff_users.count()

        # Count staff with 2FA enabled
        staff_with_2fa = 0
        try:
            from allauth.mfa.utils import is_mfa_enabled

            for user in staff_users:
                if is_mfa_enabled(user):
                    staff_with_2fa += 1
        except ImportError:
            pass

        # Calculate percentage
        compliance_percent = round(staff_with_2fa / total_staff * 100) if total_staff > 0 else 0

        return {
            "total_staff": total_staff,
            "staff_with_2fa": staff_with_2fa,
            "staff_2fa_compliance_percent": compliance_percent,
        }

    def save_model(self, request, obj, form, change):
        """Override save_model to set enforcement_date when enforcement is enabled"""
        from django.utils import timezone

        if change:
            # Check if enforcement level changed to 'required'
            old_obj = SiteSettings.objects.get(pk=obj.pk)
            if (
                old_obj.staff_2fa_enforcement != "required"
                and obj.staff_2fa_enforcement == "required"
                and not obj.staff_2fa_enforcement_date
            ):
                # Set the enforcement date to now
                obj.staff_2fa_enforcement_date = timezone.now()
            elif obj.staff_2fa_enforcement != "required":
                # Clear the enforcement date if not required
                obj.staff_2fa_enforcement_date = None

        # Validate SSO settings — prevent disabling password login without configured SSO
        if not obj.admin_password_login_enabled:
            try:
                from enterprise_sso.models import SSOProviderConfig

                sso_config = SSOProviderConfig.get_config()
                if not obj.admin_sso_enabled or not sso_config.is_configured:
                    obj.admin_password_login_enabled = True
                    from django.contrib import messages

                    messages.warning(
                        request,
                        _(
                            "Password login was re-enabled because SSO is not configured. "
                            "Configure an SSO provider before disabling password login."
                        ),
                    )
            except Exception:
                obj.admin_password_login_enabled = True

        super().save_model(request, obj, form, change)

    def get_field_tab_mapping(self):
        """Return a mapping of field names to tab IDs for error navigation in the admin form"""
        return {
            # General tab
            "site_name": "general",
            "site_tagline": "general",
            "site_url": "general",
            "site_description": "general",
            "favicon": "general",
            "site_logo": "general",
            "facebook_url": "general",
            "twitter_url": "general",
            "instagram_url": "general",
            "linkedin_url": "general",
            # Contact tab
            "admin_email": "contact",
            "support_email": "contact",
            "phone_number": "contact",
            "address_line_1": "contact",
            "address_line_2": "contact",
            "city": "contact",
            "state_province": "contact",
            "postal_code": "contact",
            "country": "contact",
            # Locale tab
            "default_currency": "locale",
            "default_timezone": "locale",
            "default_language": "locale",
            "default_weight_unit": "locale",
            "default_length_unit": "locale",
            "default_volume_unit": "locale",
            "default_area_unit": "locale",
            "default_temperature_unit": "locale",
            "enable_unit_conversion": "locale",
            # Multi-currency tab
            "enable_multi_currency": "multicurrency",
            "currency_selection_mode": "multicurrency",
            "currency_switcher_position": "multicurrency",
            "show_currency_switcher": "multicurrency",
            "show_exchange_rate_info": "multicurrency",
            "enable_locale_formatting": "multicurrency",
            "exchange_rate_markup_enabled": "multicurrency",
            "exchange_rate_markup_percentage": "multicurrency",
            "exchange_rate_selection_strategy": "multicurrency",
            "exchange_rate_sync_interval": "multicurrency",
            "multi_currency_checkout_mode": "multicurrency",
            # E-commerce tab
            "allow_guest_checkout": "ecommerce",
            "account_creation_timing": "ecommerce",
            "account_creation_message": "ecommerce",
            "show_social_auth_on_account_creation": "ecommerce",
            "require_phone_for_checkout": "ecommerce",
            "auto_approve_reviews": "ecommerce",
            # Shipping tab
            "enable_shipping_labels": "shipping",
            "default_shipping_provider": "shipping",
            "default_manual_carrier": "shipping",
            "shipping_origin_country": "shipping",
            # Authentication tab
            "staff_2fa_enforcement": "authentication",
            "staff_2fa_grace_period_days": "authentication",
            "allow_trusted_devices": "authentication",
            "trusted_device_duration_days": "authentication",
            "admin_sso_enabled": "authentication",
            "admin_password_login_enabled": "authentication",
            # E-commerce tab (Inventory & Stock)
            "enable_inventory_tracking": "ecommerce",
            "enable_multi_warehouse": "ecommerce",
            "enable_low_stock_alerts": "ecommerce",
            "low_stock_threshold": "ecommerce",
            "allow_backorders_by_default": "ecommerce",
            "default_reorder_lead_days": "ecommerce",
            "safety_stock_multiplier": "ecommerce",
            "velocity_calculation_window_days": "ecommerce",
            "low_stock_alert_frequency": "ecommerce",
            # E-commerce tab (Documents)
            "invoice_footer_text": "ecommerce",
            "packing_slip_footer_text": "ecommerce",
            "tax_id": "ecommerce",
            "document_logo_width": "ecommerce",
            # Pages tab (SEO)
            "meta_title": "pages",
            "meta_description": "pages",
            "meta_keywords": "pages",
            # Advanced tab
            "maintenance_mode": "advanced",
            "maintenance_message": "advanced",
            "maintenance_page": "advanced",
            "default_image_resize_mode": "advanced",
            "default_padding_color": "advanced",
            "logo_resize_mode": "advanced",
            "logo_padding_color": "advanced",
            # Pages tab
            "home_page": "pages",
            "privacy_page": "pages",
            "terms_page": "pages",
            "cookie_page": "pages",
            "shipping_page": "pages",
            "returns_page": "pages",
            "error_404_page": "pages",
            "error_500_page": "pages",
            # Cookies tab
            "cookie_consent_enabled": "cookies",
            "cookie_banner_position": "cookies",
            "cookie_consent_mode": "cookies",
            "cookie_banner_title": "cookies",
            "cookie_banner_text": "cookies",
            "cookie_analytics_description": "cookies",
            "cookie_marketing_description": "cookies",
            "cookie_functional_description": "cookies",
        }

    class Media:
        css = {"all": ("core/admin/css/site_settings.css", "media_library/css/media-library.css")}
        js = ("core/admin/js/site_settings.js", "media_library/js/media-library.js")


@admin.register(LicenseStatus)
class LicenseStatusAdmin(admin.ModelAdmin):
    """
    Admin interface for viewing and managing platform license status.
    This is a virtual model - no database table exists.
    """

    change_list_template = "admin/core/license_status/changelist.html"

    def has_add_permission(self, request):
        """No adding - this is a singleton display"""
        return False

    def has_delete_permission(self, request, obj=None):
        """No deleting - this is a singleton display"""
        return False

    def has_module_permission(self, request):
        """Show in admin"""
        return True

    def changelist_view(self, request, extra_context=None):
        """Custom changelist view showing license status dashboard"""
        # Don't call super() - it tries to query the database
        # Render template directly instead

        extra_context = extra_context or {}

        # Get license manager
        license_manager = get_license_manager()
        license_info = license_manager.get_license_info()

        # Add license data to context
        extra_context["license_info"] = license_info
        extra_context["is_licensed"] = license_info["is_valid"]
        extra_context["trial_mode"] = license_info["trial_mode"]
        extra_context["title"] = _("Platform License Status")
        extra_context["opts"] = self.model._meta
        extra_context["has_view_permission"] = self.has_view_permission(request)
        extra_context["site_url"] = "/"
        extra_context["has_add_permission"] = self.has_add_permission(request)
        extra_context["app_label"] = self.model._meta.app_label

        # Check version support
        updates_available, support_status = license_manager.check_version_support()
        extra_context["updates_available"] = updates_available
        extra_context["support_status"] = support_status

        # Maintenance status
        extra_context["maintenance_status"] = license_manager.get_maintenance_status()
        extra_context["spwig_services_available"] = license_manager.are_spwig_services_available()

        # POS license status
        try:
            from pos_app.license import get_pos_license_status

            extra_context["pos_license"] = get_pos_license_status()
        except Exception:
            extra_context["pos_license"] = None

        # Available add-on products from update server (cached 1 hour)
        available_addons = cache.get("entitlement_products_cache")
        if available_addons is None:
            try:
                from component_updates.models import UpdateServerConfig

                config = UpdateServerConfig.get_instance()
                import requests

                resp = requests.get(
                    f"{config.server_url.rstrip('/')}/api/v1/internal/entitlements/products/",
                    headers={
                        "X-API-KEY": config.api_key,
                        "Content-Type": "application/json",
                    },
                    timeout=5,
                )
                if resp.status_code == 200:
                    available_addons = resp.json().get("products", [])
                else:
                    available_addons = []
            except Exception:
                available_addons = []
            cache.set("entitlement_products_cache", available_addons, 3600)
        extra_context["available_addons"] = available_addons

        # Render template directly
        return render(
            request,
            self.change_list_template
            or [
                f"admin/{self.model._meta.app_label}/{self.model._meta.model_name}/change_list.html",
                f"admin/{self.model._meta.app_label}/change_list.html",
                "admin/change_list.html",
            ],
            {
                **self.admin_site.each_context(request),
                **extra_context,
            },
        )

    def get_urls(self):
        """Add custom URLs for license actions"""
        urls = super().get_urls()
        custom_urls = [
            path(
                "api/status/",
                self.admin_site.admin_view(self.license_status_api),
                name="core_licensestatus_api",
            ),
            path(
                "upload/",
                self.admin_site.admin_view(self.upload_license_view),
                name="core_licensestatus_upload",
            ),
            path(
                "activate/",
                self.admin_site.admin_view(self.activate_license_view),
                name="core_licensestatus_activate",
            ),
            path(
                "clear-cache/",
                self.admin_site.admin_view(self.clear_cache_view),
                name="core_licensestatus_clear_cache",
            ),
            path(
                "refresh/",
                self.admin_site.admin_view(self.refresh_license_view),
                name="core_licensestatus_refresh",
            ),
        ]
        return custom_urls + urls

    def license_status_api(self, request):
        """API endpoint for license status (for dashboard widget)"""
        from django.http import JsonResponse

        license_manager = get_license_manager()
        license_info = license_manager.get_license_info()

        return JsonResponse(license_info)

    def upload_license_view(self, request):
        """Handle license file upload"""
        import json
        from pathlib import Path

        from django.http import JsonResponse

        if request.method == "POST" and request.FILES.get("license_file"):
            try:
                license_file = request.FILES["license_file"]

                # Read and validate JSON
                license_content = license_file.read().decode("utf-8")
                license_data = json.loads(license_content)

                # Validate structure
                if "license" not in license_data or "signature" not in license_data:
                    return JsonResponse(
                        {
                            "success": False,
                            "error": _("Invalid license file format. Missing required fields."),
                        },
                        status=400,
                    )

                # Verify signature
                license_manager = get_license_manager()
                if not license_manager.verify_signature(license_data):
                    return JsonResponse(
                        {
                            "success": False,
                            "error": _(
                                "License signature verification failed. This license may be tampered or invalid."
                            ),
                        },
                        status=400,
                    )

                # Save to license directory
                license_path = Path(license_manager.license_path)
                license_path.parent.mkdir(parents=True, exist_ok=True)

                # Write license file
                with open(license_path, "w") as f:
                    json.dump(license_data, f, indent=2)

                # Sync license key to UpdateServerConfig so update server auth works
                from component_updates.models import UpdateServerConfig

                file_key = license_data["license"].get("license_key", "")
                if file_key:
                    update_config = UpdateServerConfig.get_instance()
                    update_config.license_key = file_key
                    update_config.save()

                # Force reload license manager singleton
                from core.license import reload_license_manager

                reload_license_manager()

                return JsonResponse(
                    {
                        "success": True,
                        "message": _("License activated successfully!"),
                        "license_key": license_data["license"]["license_key"],
                        "license_type": license_data["license"]["license_type"],
                    }
                )

            except json.JSONDecodeError:
                return JsonResponse(
                    {"success": False, "error": _("Invalid JSON format in license file.")},
                    status=400,
                )
            except Exception as e:
                return JsonResponse({"success": False, "error": str(e)}, status=500)

        return JsonResponse({"success": False, "error": _("No license file provided")}, status=400)

    def activate_license_view(self, request):
        """
        Activate license by fetching from update server with license key.
        This provides a streamlined activation flow without manual file downloads.
        """
        import hashlib
        import hmac
        import json
        import secrets
        from pathlib import Path

        import requests
        from django.http import JsonResponse

        from component_updates.models import UpdateServerConfig

        if request.method != "POST":
            return JsonResponse({"success": False, "error": _("POST method required")}, status=405)

        license_key = request.POST.get("license_key", "").strip()
        environment_type = request.POST.get("environment_type", "production")

        if not license_key:
            return JsonResponse(
                {"success": False, "error": _("License key is required")}, status=400
            )

        try:
            # Get or create update server config (contains installation_uuid)
            update_config = UpdateServerConfig.get_instance()
            installation_uuid = str(update_config.installation_uuid)

            # Generate random challenge for verification
            challenge = secrets.token_urlsafe(32)

            # Get platform version
            import core

            platform_version = core.__version__

            # Get current domain
            domain = request.get_host()

            # Call update server activation API
            update_server_url = update_config.server_url
            activation_url = f"{update_server_url}/api/v1/licenses/activate/"

            payload = {
                "license_key": license_key,
                "installation_uuid": installation_uuid,
                "domain": domain,
                "platform_version": platform_version,
                "environment_type": environment_type,
                "challenge": challenge,
            }

            response = requests.post(activation_url, json=payload, timeout=30)

            if response.status_code != 200:
                error_data = (
                    response.json()
                    if response.headers.get("content-type", "").startswith("application/json")
                    else {}
                )
                error_msg = error_data.get("message", error_data.get("error", "Activation failed"))

                return JsonResponse(
                    {
                        "success": False,
                        "error": _(f"Activation failed: {error_msg}"),
                        "error_code": error_data.get("error"),
                    },
                    status=response.status_code,
                )

            activation_data = response.json()

            # Verify challenge response (prevents MITM attacks)
            expected_response = hmac.new(
                license_key.encode(), (challenge + installation_uuid).encode(), hashlib.sha256
            ).hexdigest()

            received_response = activation_data.get("challenge_response", "")

            if received_response != expected_response:
                return JsonResponse(
                    {
                        "success": False,
                        "error": _("Challenge verification failed. Possible security issue."),
                    },
                    status=400,
                )

            # Extract license data
            license_data_obj = {
                "license": activation_data["license"],
                "signature": activation_data["signature"],
            }

            # Verify signature locally
            license_manager = get_license_manager()
            if not license_manager.verify_signature(license_data_obj):
                return JsonResponse(
                    {"success": False, "error": _("License signature verification failed.")},
                    status=400,
                )

            # Save license file
            license_path = Path(license_manager.license_path)
            license_path.parent.mkdir(parents=True, exist_ok=True)

            with open(license_path, "w") as f:
                json.dump(license_data_obj, f, indent=2)

            # Store license key in update config
            update_config.license_key = license_key
            update_config.save()

            # Force reload the license manager singleton (NO RESTART NEEDED!)
            from core.license import reload_license_manager

            reload_license_manager()

            # Return success
            return JsonResponse(
                {
                    "success": True,
                    "message": _("License activated successfully! No restart required."),
                    "license_key": activation_data["license"]["license_key"],
                    "license_type": activation_data["license"]["license_type"],
                    "owner_name": activation_data["license"]["owner_name"],
                    "environment_type": activation_data.get("environment_type"),
                    "active_installations": activation_data.get("active_installations"),
                    "max_installations": activation_data.get("max_installations"),
                }
            )

        except requests.exceptions.Timeout:
            return JsonResponse(
                {
                    "success": False,
                    "error": _("Connection to update server timed out. Please try again."),
                },
                status=504,
            )
        except requests.exceptions.ConnectionError:
            return JsonResponse(
                {
                    "success": False,
                    "error": _(
                        "Could not connect to update server. Please check your internet connection."
                    ),
                },
                status=503,
            )
        except Exception as e:
            return JsonResponse(
                {"success": False, "error": _(f"Activation error: {str(e)}")}, status=500
            )

    def refresh_license_view(self, request):
        """Refresh license from update server to get latest entitlements."""
        from django.http import JsonResponse

        if request.method != "POST":
            return JsonResponse({"success": False, "error": _("POST method required")}, status=405)

        try:
            from component_updates.services import UpdateManager

            manager = UpdateManager()
            result = manager.refresh_license(force_write=True)

            if result.get("error"):
                return JsonResponse(
                    {"success": False, "error": _("License refresh failed: %s") % result["error"]},
                    status=502,
                )

            return JsonResponse(
                {
                    "success": True,
                    "refreshed": result.get("refreshed", False),
                    "changes": result.get("changes", []),
                    "message": _("License updated successfully!")
                    if result.get("refreshed")
                    else _("License is already up to date."),
                }
            )

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    def clear_cache_view(self, request):
        """Clear license cache and reload singleton"""
        from django.http import JsonResponse

        try:
            # Force reload the singleton to pick up any license file changes
            from core.license import reload_license_manager

            reload_license_manager()

            return JsonResponse(
                {"success": True, "message": _("License cache cleared and reloaded successfully!")}
            )
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)


# Customize admin site header
admin.site.site_header = _("Spwig Admin")
admin.site.site_title = _("Spwig Admin")
admin.site.index_title = _("Welcome to Spwig Administration")

# Lock down Sites framework to single-tenant
# Prevent merchants from creating additional sites or modifying the default site
# Note: Sites framework is required for django-allauth OAuth but should be locked to SITE_ID=1
from django.contrib.sites.models import Site

admin.site.unregister(Site)


# Custom User Admin with email verification features
@admin.action(description=_("Send email verification to selected users"))
def send_verification_email(modeladmin, request, queryset):
    """Send verification emails to users who haven't verified their email."""
    from allauth.account.models import EmailAddress
    from allauth.account.utils import send_email_confirmation

    sent_count = 0
    already_verified = 0
    no_email = 0

    for user in queryset:
        if not user.email:
            no_email += 1
            continue

        # Get or create EmailAddress record
        email_address, created = EmailAddress.objects.get_or_create(
            user=user, email=user.email, defaults={"primary": True, "verified": False}
        )

        if email_address.verified:
            already_verified += 1
            continue

        # Send verification email
        send_email_confirmation(request, user)
        sent_count += 1

    # Build result message
    msg_parts = []
    if sent_count:
        msg_parts.append(_("Sent verification emails to %d user(s).") % sent_count)
    if already_verified:
        msg_parts.append(_("%d user(s) already verified.") % already_verified)
    if no_email:
        msg_parts.append(_("%d user(s) have no email address.") % no_email)

    modeladmin.message_user(request, " ".join(str(m) for m in msg_parts))


# Unregister default User admin and register custom one
admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    """
    Custom User admin with email verification status display, role badges, and actions.
    """

    list_display = [
        "username",
        "email",
        "email_verified",
        "display_roles",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    ]
    list_filter = ["is_staff", "is_superuser", "is_active", "groups"]

    # Add the verification email action
    actions = [send_verification_email]

    def display_roles(self, obj):
        """Show colored role badges for the user."""
        from staff_roles.services import get_user_roles

        roles = get_user_roles(obj)
        if obj.is_superuser and not roles:
            return format_html(
                '<span style="background: var(--primary); color: #fff; padding: 2px 8px; border-radius: 10px; font-size: 11px;">Owner</span>'
            )
        if not roles:
            return format_html('<span style="color: var(--body-quiet-color);">—</span>')
        color_map = {
            "primary": "#7c3aed",
            "success": "#22c55e",
            "warning": "#f59e0b",
            "error": "#ef4444",
            "info": "#06b6d4",
            "default": "#6b7280",
        }
        badges = []
        for role in roles:
            bg = color_map.get(role.color, "#6b7280")
            badges.append(
                f'<span style="background: {bg}; color: #fff; padding: 2px 8px; border-radius: 10px; font-size: 11px; margin-right: 4px;">{role.display_name}</span>'
            )
        return format_html("".join(badges))

    display_roles.short_description = _("Roles")

    def email_verified(self, obj):
        """Display email verification status with icon."""
        from allauth.account.models import EmailAddress

        if not obj.email:
            return format_html(
                '<span style="color: var(--body-quiet-color);" title="{}">—</span>', _("No email")
            )

        try:
            email_address = EmailAddress.objects.get(user=obj, email=obj.email)
            if email_address.verified:
                return format_html(
                    '<span style="color: var(--success-fg, #28a745);" title="{}">'
                    '<i class="fas fa-check-circle"></i>'
                    "</span>",
                    _("Email verified"),
                )
            else:
                return format_html(
                    '<span style="color: var(--warning-fg, #ffc107);" title="{}">'
                    '<i class="fas fa-exclamation-circle"></i>'
                    "</span>",
                    _("Not verified"),
                )
        except EmailAddress.DoesNotExist:
            return format_html(
                '<span style="color: var(--error-fg, #dc3545);" title="{}">'
                '<i class="fas fa-times-circle"></i>'
                "</span>",
                _("No verification record"),
            )

    email_verified.short_description = _("Verified")
    email_verified.admin_order_field = "email"


@admin.register(APIToken)
class APITokenAdmin(admin.ModelAdmin):
    """
    Admin interface for managing API tokens

    Merchants can generate and manage API tokens for various integrations
    including Help System, external services, webhooks, and custom applications.
    """

    change_list_template = "admin/core/apitoken/change_list.html"

    list_display = [
        "name",
        "token_type_display",
        "masked_token_display",
        "is_active",
        "usage_count",
        "last_used_display",
        "expires_at",
        "created_at",
    ]

    list_filter = [
        "token_type",
        "is_active",
        "created_at",
    ]

    search_fields = ["name", "description", "token"]

    readonly_fields = [
        "token",
        "full_token_display",
        "created_by",
        "created_at",
        "last_used_at",
        "usage_count",
        "is_expired_display",
        "is_valid_display",
    ]

    fieldsets = [
        (
            _("Token Information"),
            {
                "fields": [
                    "name",
                    "token_type",
                    "description",
                ]
            },
        ),
        (
            _("Token Value"),
            {
                "fields": [
                    "full_token_display",
                ],
                "description": _(
                    "Copy this token now - it will be masked in the list view for security."
                ),
            },
        ),
        (
            _("Status & Permissions"),
            {
                "fields": [
                    "is_active",
                    "expires_at",
                    "allowed_ips",
                ]
            },
        ),
        (
            _("Usage Statistics"),
            {
                "fields": [
                    "usage_count",
                    "last_used_at",
                    "is_expired_display",
                    "is_valid_display",
                ],
                "classes": ["collapse"],
            },
        ),
        (
            _("Metadata"),
            {
                "fields": [
                    "created_by",
                    "created_at",
                ],
                "classes": ["collapse"],
            },
        ),
    ]

    def save_model(self, request, obj, form, change):
        """Set created_by and generate token if new"""
        if not change:  # New object
            # Set the user who created this token
            obj.created_by = request.user

            # Token is auto-generated in the form's save method
            # (we'll handle this in the form)

        super().save_model(request, obj, form, change)

    def token_type_display(self, obj):
        """Display token type with icon"""
        icons = {
            "help_system": '<i class="fas fa-question-circle"></i>',
            "integration": '<i class="fas fa-plug"></i>',
            "webhook": '<i class="fas fa-webhook"></i>',
            "custom": '<i class="fas fa-code"></i>',
        }
        icon = icons.get(obj.token_type, '<i class="fas fa-key"></i>')
        return format_html("{} {}", mark_safe(icon), obj.get_token_type_display())

    token_type_display.short_description = _("Type")

    def masked_token_display(self, obj):
        """Display masked token in list view"""
        return obj.mask_token()

    masked_token_display.short_description = _("Token")

    def full_token_display(self, obj):
        """Display full token with copy button in change form"""
        if obj.pk:
            token_id = f"token-{obj.pk}"
            button_id = f"copy-btn-{obj.pk}"
            return format_html(
                '<div style="font-family: monospace; background: var(--darkened-bg); padding: 12px; '
                'border-radius: 4px; border: 1px solid var(--border-color); margin-bottom: 10px;">'
                '<div style="display: flex; justify-content: space-between; align-items: center;">'
                '<code id="{}" style="flex: 1; word-break: break-all;">{}</code>'
                '<button type="button" id="{}" style="margin-left: 10px; '
                "padding: 6px 12px; cursor: pointer; background: var(--primary); color: var(--primary-fg); "
                'border: none; border-radius: 4px;">'
                '<i class="fas fa-copy"></i> {}'
                "</button>"
                "</div>"
                "</div>"
                "<script>"
                "(function() {{"
                '  const btn = document.getElementById("{}");'
                '  const tokenEl = document.getElementById("{}");'
                "  if (btn && tokenEl) {{"
                '    btn.addEventListener("click", function() {{'
                "      const token = tokenEl.textContent;"
                "      navigator.clipboard.writeText(token).then(function() {{"
                "        const original = btn.innerHTML;"
                "        btn.innerHTML = '<i class=\"fas fa-check\"></i> {}!';"
                '        btn.style.background = "var(--success-color, #28a745)";'
                "        setTimeout(function() {{"
                "          btn.innerHTML = original;"
                '          btn.style.background = "var(--primary)";'
                "        }}, 2000);"
                "      }}).catch(function(err) {{"
                '        console.error("Failed to copy:", err);'
                '        alert("Failed to copy token. Please copy it manually.");'
                "      }});"
                "    }});"
                "  }}"
                "}})();"
                "</script>",
                token_id,
                obj.token,
                button_id,
                _("Copy"),
                button_id,
                token_id,
                _("Copied"),
            )
        return _("Token will be generated when you save")

    full_token_display.short_description = _("API Token")

    def last_used_display(self, obj):
        """Display last used with time since"""
        if obj.last_used_at:
            from django.utils.timesince import timesince

            return format_html(
                '{}<br><small style="color: var(--body-quiet-color);">{} ago</small>',
                obj.last_used_at.strftime("%Y-%m-%d %H:%M"),
                timesince(obj.last_used_at),
            )
        return format_html('<em style="color: var(--body-quiet-color);">{}</em>', _("Never used"))

    last_used_display.short_description = _("Last Used")

    def is_expired_display(self, obj):
        """Display expiration status"""
        if obj.is_expired:
            return format_html(
                '<span style="color: var(--error-fg); background: var(--error-bg); '
                'padding: 3px 8px; border-radius: 3px;">'
                '<i class="fas fa-exclamation-triangle"></i> {}'
                "</span>",
                _("Expired"),
            )
        elif obj.expires_at:
            from django.utils.timesince import timeuntil

            return format_html(
                '<span style="color: var(--success-fg); background: var(--success-bg); '
                'padding: 3px 8px; border-radius: 3px;">'
                '<i class="fas fa-check-circle"></i> {} (expires in {})'
                "</span>",
                _("Valid"),
                timeuntil(obj.expires_at),
            )
        return format_html(
            '<span style="color: var(--body-quiet-color);">'
            '<i class="fas fa-infinity"></i> {}'
            "</span>",
            _("Never expires"),
        )

    is_expired_display.short_description = _("Expiration Status")

    def is_valid_display(self, obj):
        """Display overall validity status"""
        if obj.is_valid:
            return format_html(
                '<span style="color: var(--success-fg);">'
                '<i class="fas fa-check-circle"></i> {}'
                "</span>",
                _("Valid"),
            )
        return format_html(
            '<span style="color: var(--error-fg);"><i class="fas fa-times-circle"></i> {}</span>',
            _("Invalid"),
        )

    is_valid_display.short_description = _("Status")

    def get_form(self, request, obj=None, **kwargs):
        """Customize the form"""
        form = super().get_form(request, obj, **kwargs)

        # Auto-generate token for new objects
        if not obj and "token" in form.base_fields:
            from core.utils.api_tokens import generate_secure_token

            form.base_fields["token"].initial = generate_secure_token()

        return form

    class Media:
        css = {"all": ["admin/css/forms.css"]}

    def changelist_view(self, request, extra_context=None):
        """Add extra context to changelist"""
        extra_context = extra_context or {}

        # Add summary statistics
        from django.db.models import Count, Q

        stats = APIToken.objects.aggregate(
            total=Count("id"),
            active=Count("id", filter=Q(is_active=True)),
            help_system=Count("id", filter=Q(token_type="help_system", is_active=True)),
            integration=Count("id", filter=Q(token_type="integration", is_active=True)),
        )

        extra_context["token_stats"] = stats
        extra_context["help_text"] = _(
            "API tokens allow external services and integrations to authenticate with your shop. "
            "Keep these tokens secure and never share them publicly. You can revoke tokens at any time "
            "by marking them as inactive."
        )

        return super().changelist_view(request, extra_context=extra_context)


@admin.register(ErrorReport)
class ErrorReportAdmin(admin.ModelAdmin):
    list_display = (
        "error_type_badge",
        "exception_summary",
        "occurrence_count",
        "status_badge",
        "last_seen",
    )
    list_filter = ("error_type", "status")
    search_fields = ("error_data",)
    readonly_fields = (
        "error_type",
        "fingerprint",
        "occurrence_count",
        "error_data",
        "first_seen",
        "last_seen",
        "sent_at",
    )
    actions = ["submit_selected", "dismiss_selected"]
    change_list_template = "admin/core/errorreport/change_list.html"

    def has_add_permission(self, request):
        return False

    @admin.display(description=_("Type"))
    def error_type_badge(self, obj):
        colors = {"python": "#3776ab", "javascript": "#f7df1e"}
        labels = {"python": "Python", "javascript": "JS"}
        color = colors.get(obj.error_type, "#666")
        text_color = "#000" if obj.error_type == "javascript" else "#fff"
        label = labels.get(obj.error_type, obj.error_type)
        return format_html(
            '<span style="display:inline-block;padding:2px 8px;border-radius:4px;'
            'font-size:11px;font-weight:600;background:{};color:{}">{}</span>',
            color,
            text_color,
            label,
        )

    @admin.display(description=_("Error"))
    def exception_summary(self, obj):
        if not obj.error_data:
            return "-"
        exc_type = obj.error_data.get("exception_type", obj.error_data.get("message", "Unknown"))
        msg = obj.error_data.get("exception_message", obj.error_data.get("message", ""))
        summary = exc_type
        if msg and msg != exc_type:
            summary = f"{exc_type}: {msg}"
        if len(summary) > 100:
            summary = summary[:97] + "..."
        return summary

    @admin.display(description=_("Status"))
    def status_badge(self, obj):
        colors = {
            "pending": "#ff9800",
            "sent": "#4caf50",
            "failed": "#f44336",
            "held": "#2196f3",
        }
        color = colors.get(obj.status, "#666")
        return format_html(
            '<span style="display:inline-block;padding:2px 8px;border-radius:4px;'
            'font-size:11px;font-weight:600;background:{};color:#fff">{}</span>',
            color,
            obj.get_status_display(),
        )

    @admin.action(description=_("Submit selected reports to Spwig"))
    def submit_selected(self, request, queryset):
        count = queryset.filter(status="held").update(status="pending")
        self.message_user(request, _("{} report(s) queued for submission.").format(count))

    @admin.action(description=_("Dismiss selected reports"))
    def dismiss_selected(self, request, queryset):
        count = queryset.filter(status="held").delete()[0]
        self.message_user(request, _("{} report(s) dismissed.").format(count))


@admin.register(BugReport)
class BugReportAdmin(admin.ModelAdmin):
    list_display = (
        "category",
        "severity_badge",
        "description_short",
        "status_badge",
        "submitted_by",
        "created_at",
    )
    list_filter = ("category", "severity", "status")
    readonly_fields = (
        "category",
        "description",
        "severity",
        "browser_data",
        "consent_flags",
        "contact_name",
        "contact_email",
        "contact_consent",
        "page_url",
        "admin_section",
        "submitted_by",
        "created_at",
        "sent_at",
    )
    search_fields = ("description",)

    def has_add_permission(self, request):
        return False

    @admin.display(description=_("Description"))
    def description_short(self, obj):
        return obj.description[:80] + "..." if len(obj.description) > 80 else obj.description

    @admin.display(description=_("Severity"))
    def severity_badge(self, obj):
        colors = {"minor": "#2196f3", "significant": "#ff9800", "blocking": "#f44336"}
        color = colors.get(obj.severity, "#666")
        return format_html(
            '<span style="display:inline-block;padding:2px 8px;border-radius:4px;'
            'font-size:11px;font-weight:600;background:{};color:#fff">{}</span>',
            color,
            obj.get_severity_display(),
        )

    @admin.display(description=_("Status"))
    def status_badge(self, obj):
        colors = {"pending": "#ff9800", "sent": "#4caf50", "failed": "#f44336"}
        color = colors.get(obj.status, "#666")
        return format_html(
            '<span style="display:inline-block;padding:2px 8px;border-radius:4px;'
            'font-size:11px;font-weight:600;background:{};color:#fff">{}</span>',
            color,
            obj.get_status_display(),
        )


@admin.register(CookieConsentLog)
class CookieConsentLogAdmin(admin.ModelAdmin):
    """Read-only audit trail for GDPR Article 7(1) cookie consent compliance."""

    list_display = ["timestamp", "action", "ip_address", "user_email", "consent_summary"]
    list_filter = ["action", "timestamp"]
    search_fields = ["ip_address", "user__email", "session_key"]
    readonly_fields = [
        "timestamp",
        "action",
        "consent_data",
        "ip_address",
        "user_agent",
        "user",
        "session_key",
    ]
    list_per_page = 50
    ordering = ["-timestamp"]

    actions = ["export_consent_csv"]

    fieldsets = [
        (
            None,
            {
                "fields": ("timestamp", "action", "consent_data"),
            },
        ),
        (
            _("Visitor"),
            {
                "fields": ("user", "session_key", "ip_address", "user_agent"),
            },
        ),
    ]

    @admin.display(description=_("User"))
    def user_email(self, obj):
        return obj.user.email if obj.user_id else "—"

    @admin.display(description=_("Consent"))
    def consent_summary(self, obj):
        d = obj.consent_data or {}
        parts = []
        for key in ("analytics", "marketing", "functional"):
            if d.get(key):
                parts.append(key[:3].upper())
        return ", ".join(parts) if parts else _("None")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    @admin.action(description=_("Export selected as CSV"))
    def export_consent_csv(self, request, queryset):
        import csv

        from django.http import HttpResponse

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="cookie_consent_log.csv"'
        writer = csv.writer(response)
        writer.writerow(
            [
                "Timestamp",
                "Action",
                "IP Address",
                "User Agent",
                "User Email",
                "Session Key",
                "Analytics",
                "Marketing",
                "Functional",
            ]
        )
        for log in queryset.select_related("user").order_by("-timestamp"):
            d = log.consent_data or {}
            writer.writerow(
                [
                    log.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    log.get_action_display(),
                    log.ip_address or "",
                    log.user_agent,
                    log.user.email if log.user_id else "",
                    log.session_key,
                    d.get("analytics", False),
                    d.get("marketing", False),
                    d.get("functional", False),
                ]
            )
        self.message_user(request, _("{} record(s) exported.").format(queryset.count()))
