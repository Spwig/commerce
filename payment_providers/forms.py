"""
Payment Provider Admin Forms
==============================
ModelForm for PaymentProviderAccount admin editing.
"""

from django import forms

from payment_providers.models import PaymentProviderAccount


class PaymentProviderConfigForm(forms.ModelForm):
    """
    Form for editing PaymentProviderAccount in admin.

    Payment method configuration is handled via the per-country
    configure-payment-methods page (not inline on this form).
    """

    class Meta:
        model = PaymentProviderAccount
        fields = ["display_name", "checkout_mode", "is_active", "is_default", "sort_order"]
