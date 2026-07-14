"""
Forms for shipping models
"""

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import ProviderAccount, ShippingZone
from .providers.loader import load_provider_manifest
from .services import ProviderService
from .utils.encryption import decrypt_credentials, encrypt_credentials


class ProviderAccountAdminForm(forms.ModelForm):
    """
    Custom admin form for ProviderAccount that shows decrypted credential fields
    dynamically based on the provider's credential schema.
    """

    class Meta:
        model = ProviderAccount
        fields = [
            "component",
            "user",
            "display_name",
            "is_active",
            "is_default",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make component and user readonly if editing existing account
        if self.instance.pk:
            # Check if fields exist before modifying them
            if "component" in self.fields:
                self.fields["component"].disabled = True
                self.fields["component"].help_text = _(
                    "Component cannot be changed after creation."
                )
            if "user" in self.fields:
                self.fields["user"].disabled = True
                self.fields["user"].help_text = _("User cannot be changed for audit purposes.")

            # Load provider's credential schema
            try:
                # Check if component relationship is loaded
                if not hasattr(self.instance, "component"):
                    import logging

                    logger = logging.getLogger(__name__)
                    logger.warning("Instance does not have component attribute")
                    return

                # Try to access the component, catching RelatedObjectDoesNotExist
                try:
                    component = self.instance.component
                except Exception as e:
                    import logging

                    logger = logging.getLogger(__name__)
                    logger.warning(f"Could not access component relationship: {e}")
                    return

                if component is None:
                    import logging

                    logger = logging.getLogger(__name__)
                    logger.warning("Component is None")
                    return

                component_path = ProviderService.get_component_path(component.slug)
                manifest = load_provider_manifest(component_path)

                if manifest:
                    credential_schema = manifest.get("credential_schema", {})

                    # Decrypt existing credentials
                    decrypted_credentials = {}
                    if self.instance.credentials_encrypted:
                        try:
                            decrypted_credentials = decrypt_credentials(
                                self.instance.credentials_encrypted
                            )
                        except Exception as e:
                            # If decryption fails, log but don't crash
                            import logging

                            logger = logging.getLogger(__name__)
                            logger.error(f"Failed to decrypt credentials: {e}")

                    # Store original credentials for disabled field preservation
                    self._original_credentials = decrypted_credentials.copy()

                    # Add dynamic credential fields based on schema
                    for field_name, field_config in credential_schema.items():
                        field_type = field_config.get("type", "string")
                        field_label = field_config.get("label", field_name)
                        field_required = field_config.get("required", False)
                        field_secret = field_config.get("secret", False) or field_type == "password"
                        field_help = field_config.get(
                            "description", field_config.get("help_text", "")
                        )

                        # Determine widget based on field type
                        if field_type == "select":
                            # Handle choices - can be simple list or list of dicts with value/label
                            choices_config = field_config.get(
                                "choices", field_config.get("options", [])
                            )
                            if choices_config and isinstance(choices_config[0], dict):
                                # Format: [{"value": "x", "label": "X"}]
                                choices = [
                                    (choice["value"], choice["label"]) for choice in choices_config
                                ]
                            else:
                                # Format: ["x", "y"] or already formatted tuples
                                choices = [
                                    (opt, opt) if not isinstance(opt, tuple) else opt
                                    for opt in choices_config
                                ]

                            # Make select fields disabled when editing (read-only reference)
                            widget = forms.Select(
                                attrs={"class": "form-control", "disabled": "disabled"}
                            )
                            self.fields[f"credential_{field_name}"] = forms.ChoiceField(
                                label=field_label,
                                choices=choices,
                                required=False,  # Not required since it's disabled
                                help_text=field_help,
                                widget=widget,
                                initial=decrypted_credentials.get(
                                    field_name, field_config.get("default")
                                ),
                            )
                        elif field_secret:
                            # Secret field - use password input with toggle
                            widget = forms.TextInput(
                                attrs={
                                    "class": "form-control password-field",
                                    "data-secret": "true",
                                    "autocomplete": "off",
                                }
                            )
                            self.fields[f"credential_{field_name}"] = forms.CharField(
                                label=field_label,
                                required=field_required,
                                help_text=field_help,
                                widget=widget,
                                initial=decrypted_credentials.get(field_name, ""),
                            )
                        else:
                            # Regular text field
                            widget = forms.TextInput(attrs={"class": "form-control"})
                            self.fields[f"credential_{field_name}"] = forms.CharField(
                                label=field_label,
                                required=field_required,
                                help_text=field_help,
                                widget=widget,
                                initial=decrypted_credentials.get(field_name, ""),
                            )

            except Exception as e:
                import logging

                logger = logging.getLogger(__name__)
                logger.error(f"Failed to load credential schema: {e}")

    def clean(self):
        """Validate and prepare credential data"""
        cleaned_data = super().clean()

        # Don't process credentials if component/user are being edited (shouldn't happen due to disabled fields)
        if self.instance.pk:
            # Collect credential fields
            credentials = {}
            fields_to_remove = []

            for field_name in self.fields:
                if field_name.startswith("credential_"):
                    credential_key = field_name.replace("credential_", "")

                    # Check if field value is in cleaned_data (it won't be if disabled)
                    if field_name in cleaned_data:
                        credentials[credential_key] = cleaned_data.get(field_name, "")
                    elif hasattr(self, "_original_credentials"):
                        # Use original value for disabled fields
                        credentials[credential_key] = self._original_credentials.get(
                            credential_key, ""
                        )
                    else:
                        credentials[credential_key] = ""

                    fields_to_remove.append(field_name)

            # Remove credential fields from cleaned_data (they're not model fields)
            for field_name in fields_to_remove:
                cleaned_data.pop(field_name, None)

            # Store credentials for save method
            self._credentials = credentials

        return cleaned_data

    def save(self, commit=True):
        """Encrypt and save credentials"""
        instance = super().save(commit=False)

        # Encrypt credentials if we have any
        if hasattr(self, "_credentials") and self._credentials:
            instance.credentials_encrypted = encrypt_credentials(self._credentials)

        if commit:
            instance.save()

        return instance


class ShippingZoneAdminForm(forms.ModelForm):
    """
    Custom admin form for ShippingZone with enhanced widgets.

    JSON fields (countries, states, postal_code_patterns) are enhanced
    with JavaScript-based dual-listbox UI in the change form template.
    """

    class Meta:
        model = ShippingZone
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "vTextField",
                    "placeholder": _("e.g., North America, European Union, Domestic"),
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "vLargeTextField",
                    "rows": 3,
                    "placeholder": _("Optional description of zone coverage"),
                }
            ),
            "priority": forms.NumberInput(attrs={"class": "vIntegerField", "min": 0, "max": 100}),
        }
