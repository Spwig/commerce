"""
Custom forms for accounts app.
"""

from allauth.account.models import EmailAddress
from allauth.mfa.forms import ActivateTOTPForm as BaseActivateTOTPForm
from django import forms
from django.utils.translation import gettext_lazy as _


class ActivateTOTPForm(BaseActivateTOTPForm):
    """
    Custom TOTP activation form that only checks PRIMARY email verification.

    The default allauth form blocks 2FA activation if ANY email is unverified.
    We only care about the PRIMARY email being verified - secondary unverified
    emails shouldn't block 2FA setup.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Override the email_verified check to only look at primary email
        self.email_verified = self._check_primary_email_verified()

    def _check_primary_email_verified(self):
        """Check if the user's PRIMARY email is verified."""
        try:
            primary_email = EmailAddress.objects.get(user=self.user, primary=True)
            return primary_email.verified
        except EmailAddress.DoesNotExist:
            # No primary email set - treat as unverified
            return False


class CustomerMessageForm(forms.Form):
    """
    Form for customers to submit messages from the account portal.
    Name/email are taken from request.user in the view, not shown in the form.
    """

    MESSAGE_TYPE_CHOICES = [
        ("general", _("General Inquiry")),
        ("support", _("Support Request")),
        ("order", _("Order Related")),
        ("product", _("Product Question")),
        ("other", _("Other")),
    ]

    subject = forms.CharField(
        max_length=300,
        label=_("Subject"),
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "placeholder": _("What is your message about?"),
            }
        ),
    )
    message_type = forms.ChoiceField(
        choices=MESSAGE_TYPE_CHOICES,
        initial="general",
        label=_("Message Type"),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    order = forms.ModelChoiceField(
        queryset=None,
        required=False,
        label=_("Related Order"),
        empty_label=_("No order selected"),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    message = forms.CharField(
        max_length=5000,
        label=_("Message"),
        widget=forms.Textarea(
            attrs={
                "class": "form-textarea",
                "rows": 6,
                "placeholder": _("Please describe your inquiry in detail..."),
                "maxlength": "5000",
                "data-char-counter": "true",
                "data-max-chars": "5000",
            }
        ),
    )


class FollowUpMessageForm(forms.Form):
    """Form for customers to send a follow-up to an existing message."""

    message = forms.CharField(
        max_length=5000,
        label=_("Your follow-up message"),
        widget=forms.Textarea(
            attrs={
                "class": "form-textarea",
                "rows": 4,
                "placeholder": _("Type your follow-up message..."),
                "maxlength": "5000",
                "data-char-counter": "true",
                "data-max-chars": "5000",
            }
        ),
    )
