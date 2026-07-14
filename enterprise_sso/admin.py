from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import SSOProviderConfig


class SSOProviderConfigForm(forms.ModelForm):
    """Custom form that handles the encrypted client secret field."""

    # Plain text field for input — not stored directly in the model
    oidc_client_secret = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": _("Enter client secret (leave blank to keep current)"),
                "autocomplete": "off",
            }
        ),
        label=_("Client Secret"),
        help_text=_("Application/Client secret from your identity provider. Stored encrypted."),
    )

    class Meta:
        model = SSOProviderConfig
        fields = [
            "provider_name",
            "oidc_discovery_url",
            "oidc_authorization_endpoint",
            "oidc_token_endpoint",
            "oidc_userinfo_endpoint",
            "oidc_jwks_endpoint",
            "oidc_end_session_endpoint",
            "oidc_client_id",
            "claim_email",
            "claim_first_name",
            "claim_last_name",
            "claim_groups",
            "staff_groups",
            "superuser_groups",
            "oidc_scopes",
            "auto_create_users",
            "restrict_to_staff",
        ]
        widgets = {
            "staff_groups": forms.Textarea(attrs={"rows": 2}),
            "superuser_groups": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Show whether a secret is currently set
        if self.instance and self.instance.pk and self.instance.oidc_client_secret_encrypted:
            self.fields["oidc_client_secret"].help_text = _(
                "A client secret is currently configured. Leave blank to keep it, or enter a new value to replace it."
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        plain_secret = self.cleaned_data.get("oidc_client_secret", "")
        if plain_secret:
            instance.set_client_secret(plain_secret)
        if commit:
            instance.save()
        return instance


@admin.register(SSOProviderConfig)
class SSOProviderConfigAdmin(admin.ModelAdmin):
    form = SSOProviderConfigForm
    change_form_template = "admin/enterprise_sso/ssoproviderconfig/change_form.html"

    fieldsets = (
        (
            _("Provider"),
            {
                "fields": ("provider_name",),
            },
        ),
        (
            _("OIDC Discovery"),
            {
                "fields": ("oidc_discovery_url",),
            },
        ),
        (
            _("OIDC Endpoints"),
            {
                "fields": (
                    "oidc_authorization_endpoint",
                    "oidc_token_endpoint",
                    "oidc_userinfo_endpoint",
                    "oidc_jwks_endpoint",
                    "oidc_end_session_endpoint",
                ),
            },
        ),
        (
            _("Client Credentials"),
            {
                "fields": ("oidc_client_id", "oidc_client_secret"),
            },
        ),
        (
            _("Claims Mapping"),
            {
                "fields": ("claim_email", "claim_first_name", "claim_last_name", "claim_groups"),
            },
        ),
        (
            _("Role Mapping"),
            {
                "fields": ("staff_groups", "superuser_groups"),
            },
        ),
        (
            _("Scopes & Behavior"),
            {
                "fields": ("oidc_scopes", "auto_create_users", "restrict_to_staff"),
            },
        ),
    )

    def has_add_permission(self, request):
        # Singleton — only allow adding if no config exists
        return not SSOProviderConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        if object_id:
            try:
                obj = self.get_object(request, object_id)
                if obj:
                    extra_context["is_configured"] = obj.is_configured
                    extra_context["callback_url"] = request.build_absolute_uri("/oidc/callback/")
                    extra_context["discover_url"] = "/oidc/discover/"
            except Exception:
                pass
        return super().change_view(request, object_id, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):
        """Redirect changelist to the singleton change page."""
        config = SSOProviderConfig.get_config()
        from django.shortcuts import redirect

        return redirect("admin:enterprise_sso_ssoproviderconfig_change", config.pk)
