from django import forms
from django.core.validators import EmailValidator, URLValidator
from django.utils.translation import gettext_lazy as _
from core.models import SiteSettings


class SiteInfoForm(forms.Form):
    """Form for basic site information"""

    site_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'My Awesome Store'
        }),
        help_text=_("The name of your store that appears in the header and emails")
    )

    site_url = forms.URLField(
        required=True,
        validators=[URLValidator()],
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://yourstore.com'
        }),
        help_text=_("The main URL of your store (used in emails and links)")
    )

    site_description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'A brief description of your store and what you sell...'
        }),
        help_text=_("A brief description of your store")
    )

    favicon = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        help_text=_("Upload a favicon for your site (recommended: 32x32 or 16x16 pixels, ICO, PNG, or SVG format)")
    )


class ContactInfoForm(forms.Form):
    """Form for contact information"""

    admin_email = forms.EmailField(
        required=True,
        validators=[EmailValidator()],
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'admin@yourstore.com'
        }),
        help_text=_("Primary admin email for system notifications and customer service")
    )

    support_email = forms.EmailField(
        required=False,
        validators=[EmailValidator()],
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'support@yourstore.com'
        }),
        help_text=_("Customer support email (if different from admin email)")
    )

    phone_number = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+1 (555) 123-4567'
        }),
        help_text=_("Store contact phone number")
    )


class BusinessAddressForm(forms.Form):
    """Form for business address information"""

    address_line_1 = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '123 Main Street'
        }),
        help_text=_("Street address")
    )

    address_line_2 = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Suite 100'
        }),
        help_text=_("Apartment, suite, etc.")
    )

    city = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'New York'
        }),
        help_text=_("City")
    )

    state_province = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'NY'
        }),
        help_text=_("State or Province")
    )

    postal_code = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '10001'
        }),
        help_text=_("ZIP or Postal Code")
    )

    country = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'United States'
        }),
        help_text=_("Country")
    )


class CurrencyLocaleForm(forms.Form):
    """Form for currency, language, and locale settings"""

    default_currency = forms.ChoiceField(
        choices=[],
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        help_text=_("Default currency for product prices and transactions")
    )

    default_language = forms.ChoiceField(
        choices=[],
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        help_text=_("Default language for the store interface")
    )

    default_timezone = forms.ChoiceField(
        choices=[],
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        help_text=_("Default timezone for displaying dates and times")
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from core.utils.locale_helpers import (
            get_grouped_currencies, get_grouped_languages, get_grouped_timezones,
        )

        # Currencies: same grouped list as SiteSettings admin (160+ currencies)
        currency_groups = get_grouped_currencies()
        self.fields['default_currency'].choices = [
            ('', _('-- Select currency --')),
            (_('Popular Currencies'), currency_groups['popular']),
            (_('Other Currencies'), currency_groups['other']),
        ]

        # Languages: same grouped list as SiteSettings admin (99+ languages)
        language_groups = get_grouped_languages()
        self.fields['default_language'].choices = [
            (_('Admin Languages'), language_groups['admin']),
            (_('Popular Languages'), language_groups['popular']),
            (_('Other Languages'), language_groups['other']),
        ]

        # Timezones: same grouped list as SiteSettings admin (599 timezones)
        timezone_groups = get_grouped_timezones()
        self.fields['default_timezone'].choices = [
            (_('Popular Timezones'), timezone_groups['popular']),
            (_('Americas'), timezone_groups['americas']),
            (_('Europe'), timezone_groups['europe']),
            (_('Asia'), timezone_groups['asia']),
            (_('Africa'), timezone_groups['africa']),
            (_('Pacific'), timezone_groups['pacific']),
            (_('Other'), timezone_groups['other']),
        ]


class PaymentMethodsInfoForm(forms.Form):
    """
    Informational form for the payment methods step.

    This step does not collect data — it informs merchants that payment
    providers are configured through the dedicated Payment Provider admin.
    """
    pass


class EcommerceSettingsForm(forms.Form):
    """Form for core e-commerce settings"""

    allow_guest_checkout = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label=_("Allow Guest Checkout"),
        help_text=_("Allow customers to checkout without creating an account")
    )

    require_phone_for_checkout = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label=_("Require Phone for Checkout"),
        help_text=_("Require phone number during checkout")
    )

    enable_inventory_tracking = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label=_("Enable Inventory Tracking"),
        help_text=_("Track product inventory and prevent overselling")
    )

    auto_approve_reviews = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label=_("Auto-approve Reviews"),
        help_text=_("Automatically approve product reviews without moderation")
    )

    enable_error_reporting = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label=_("Help Improve Spwig"),
        help_text=_("Send anonymized error reports to help us improve the platform. No personal data is ever transmitted. You can change this anytime in Site Settings.")
    )


class EmailSettingsForm(forms.Form):
    """Form for email notification settings"""

    enable_order_confirmation_emails = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label=_("Order Confirmation Emails"),
        help_text=_("Send order confirmation emails to customers")
    )

    enable_shipping_notification_emails = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label=_("Shipping Notification Emails"),
        help_text=_("Send shipping notification emails to customers")
    )

    enable_low_stock_alerts = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label=_("Low Stock Alerts"),
        help_text=_("Send low stock alerts to admin email")
    )

    low_stock_threshold = forms.IntegerField(
        required=False,
        initial=10,
        min_value=1,
        max_value=1000,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1',
            'max': '1000'
        }),
        help_text=_("Stock level at which to send low stock alerts")
    )


class SEOSettingsForm(forms.Form):
    """Form for SEO settings"""

    meta_title = forms.CharField(
        max_length=60,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'maxlength': '60',
            'placeholder': 'Your Store - Quality Products Online'
        }),
        help_text=_("Default meta title for pages (60 characters max)")
    )

    meta_description = forms.CharField(
        max_length=160,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'maxlength': '160',
            'placeholder': 'Discover quality products at great prices. Fast shipping and excellent customer service.'
        }),
        help_text=_("Default meta description for pages (160 characters max)")
    )

    meta_keywords = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'online store, e-commerce, quality products'
        }),
        help_text=_("Default meta keywords for pages (comma-separated)")
    )


class SocialMediaForm(forms.Form):
    """Form for social media links"""

    facebook_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://facebook.com/yourstore'
        }),
        help_text=_("Facebook page URL")
    )

    twitter_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://twitter.com/yourstore'
        }),
        help_text=_("Twitter profile URL")
    )

    instagram_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://instagram.com/yourstore'
        }),
        help_text=_("Instagram profile URL")
    )

    linkedin_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://linkedin.com/company/yourstore'
        }),
        help_text=_("LinkedIn page URL")
    )


class ContactLocationForm(forms.Form):
    """Combined contact information and business address form."""

    admin_email = forms.EmailField(
        required=True,
        validators=[EmailValidator()],
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'admin@yourstore.com'
        }),
        help_text=_("Primary admin email for system notifications and customer service")
    )

    support_email = forms.EmailField(
        required=False,
        validators=[EmailValidator()],
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'support@yourstore.com'
        }),
        help_text=_("Customer support email (if different from admin email)")
    )

    phone_number = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+1 (555) 123-4567'
        }),
        help_text=_("Store contact phone number")
    )

    address_line_1 = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '123 Main Street'
        }),
        help_text=_("Street address")
    )

    address_line_2 = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Suite 100'
        }),
        help_text=_("Apartment, suite, etc.")
    )

    city = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'New York'
        }),
        help_text=_("City")
    )

    state_province = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'NY'
        }),
        help_text=_("State or Province")
    )

    postal_code = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '10001'
        }),
        help_text=_("ZIP or Postal Code")
    )

    country = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'United States'
        }),
        help_text=_("Country")
    )
