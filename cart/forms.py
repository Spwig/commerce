"""
Forms for Cart app
"""

from decimal import Decimal

from django import forms
from django.utils.translation import gettext_lazy as _

from core.widgets import IconPickerWidget
from media_library.models import MediaAsset
from media_library.widgets import MediaLibrarySelectWidget


class PercentageInput(forms.NumberInput):
    """Widget that displays a decimal value as a percentage."""

    def format_value(self, value):
        if value is not None and value != "":
            try:
                return str((Decimal(str(value)) * 100).normalize())
            except Exception:
                return value
        return value


class TaxRateAdminForm(forms.ModelForm):
    """Admin form that lets merchants enter rate as percentage (e.g., 8.25 for 8.25%)."""

    rate = forms.DecimalField(
        max_digits=7,
        decimal_places=4,
        widget=PercentageInput(attrs={"step": "0.01", "min": "0", "max": "100"}),
        help_text=_("Enter as percentage (e.g., 8.25 for 8.25%)"),
        label=_("Rate (%)"),
    )

    class Meta:
        from cart.models import TaxRate

        model = TaxRate
        fields = "__all__"

    def clean_rate(self):
        """Convert percentage input to decimal for storage."""
        rate = self.cleaned_data["rate"]
        return rate / Decimal("100")


class ShippingMethodWizardStep1Form(forms.Form):
    """Form for Step 1 of shipping method wizard"""

    METHOD_TYPE_CHOICES = [
        ("", "Select method type..."),
        ("flat_rate", "Flat Rate - Fixed shipping cost"),
        ("real_time", "Real-Time Carrier Rates - Live rates from carriers"),
        ("local_pickup", "Local Pickup - Customer picks up at location"),
        ("table_rate", "Table Rate - Complex rules based on weight/price/destination"),
    ]

    # CARRIER_CHOICES dynamically generated in __init__ from configured providers

    # Basic fields
    name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "e.g., Standard Shipping, Express Delivery",
            }
        ),
    )

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Optional description of this shipping method",
            }
        ),
    )

    # Image/Icon fields
    image = forms.ModelChoiceField(
        queryset=MediaAsset.objects.all(), required=False, widget=MediaLibrarySelectWidget()
    )

    icon = forms.CharField(
        required=False,
        widget=IconPickerWidget(
            priority_icons=[
                "fa-truck",
                "fa-truck-fast",
                "fa-box",
                "fa-warehouse",
                "fa-dolly",
                "fa-cube",
                "fa-ship",
                "fa-plane",
                "fa-bicycle",
            ],
            style_prefix=False,
        ),
    )

    is_active = forms.BooleanField(
        required=False, initial=True, widget=forms.CheckboxInput(attrs={"class": "form-checkbox"})
    )

    # Method type and pricing
    method_type = forms.ChoiceField(
        choices=METHOD_TYPE_CHOICES,
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    flat_rate_cost = forms.DecimalField(
        required=False,
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "0.00", "step": "0.01"}
        ),
    )

    # Carrier fields (for real_time)
    carrier = forms.ChoiceField(
        choices=[],  # Will be populated in __init__
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    carrier_service_code = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "e.g., PRIORITY, GROUND"}
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Dynamically populate carrier choices from configured providers
        carrier_choices = self._get_configured_carrier_choices()
        self.fields["carrier"].choices = carrier_choices

        # Store whether we have carriers available for template access
        self.has_configured_carriers = len(carrier_choices) > 1  # > 1 because first is empty choice

    def _get_configured_carrier_choices(self):
        """
        Get carrier choices from active ProviderAccounts that support real-time rates.
        Returns list of (slug, display_name) tuples.
        """
        from shipping.models import ProviderAccount
        from shipping.providers.loader import load_provider_manifest
        from shipping.services import ProviderService

        choices = [("", "Select carrier...")]

        try:
            # Get all active provider accounts
            active_accounts = (
                ProviderAccount.objects.filter(is_active=True)
                .select_related("component")
                .order_by("component__name")
            )

            for account in active_accounts:
                try:
                    # Get component path and load manifest
                    component_path = ProviderService.get_component_path(account.component.slug)

                    if not component_path or not component_path.exists():
                        continue

                    manifest = load_provider_manifest(component_path)

                    if not manifest:
                        continue

                    # Check if provider supports real-time rates
                    capabilities = manifest.get("capabilities", {})
                    if capabilities.get("rates", False):
                        # Add this provider to choices
                        # Use component slug as value and account display name (or component name) as label
                        display_name = account.display_name or account.component.name
                        choices.append(
                            (account.component.slug, f"{display_name} ({account.component.name})")
                        )

                except Exception as e:
                    # Log but don't fail if one provider has issues
                    import logging

                    logger = logging.getLogger(__name__)
                    logger.warning(f"Error loading provider {account.component.slug}: {e}")
                    continue

        except Exception as e:
            # Log but return empty choices if there's a database error
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"Error fetching provider accounts: {e}")

        return choices
