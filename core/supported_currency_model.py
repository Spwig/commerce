"""
Multi-Currency Support Model

This module defines the SupportedCurrency model for managing merchant-configurable
currency support, including activation status, display order, and presentation settings.
"""

import moneyed
from django.core.exceptions import ValidationError
from django.db import models
from moneyed import CURRENCIES


class SupportedCurrency(models.Model):
    """
    Merchant-configurable currency support.

    This model tracks which currencies are available for customers to use
    in the storefront, their display order, and presentation settings.
    """

    # Core Fields
    code = models.CharField(
        max_length=3,
        unique=True,
        db_index=True,
        help_text="3-letter ISO 4217 currency code (e.g., USD, EUR, GBP)",
    )

    is_active = models.BooleanField(
        default=False, db_index=True, help_text="Whether this currency is available for customers"
    )

    order = models.IntegerField(
        default=0, db_index=True, help_text="Display order (lower numbers appear first)"
    )

    # Display Settings
    show_flag = models.BooleanField(
        default=True, help_text="Show country flag in currency selector widget"
    )

    show_symbol = models.BooleanField(
        default=True, help_text="Show currency symbol ($, €, £) in displays"
    )

    custom_symbol = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="Optional custom symbol override (defaults to ISO standard)",
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "core_supported_currency"
        ordering = ["order", "code"]
        verbose_name = "Supported Currency"
        verbose_name_plural = "Supported Currencies"
        indexes = [
            models.Index(fields=["is_active", "order"]),
        ]

    def __str__(self):
        return f"{self.code} ({self.get_currency_name()})"

    def clean(self):
        """Validate currency code exists in moneyed library"""
        if self.code not in CURRENCIES:
            raise ValidationError(
                {"code": f"Invalid currency code: {self.code}. Must be a valid ISO 4217 code."}
            )

    def save(self, *args, **kwargs):
        self.code = self.code.upper()
        self.full_clean()
        super().save(*args, **kwargs)

    # Properties
    @property
    def currency_obj(self):
        """Get moneyed Currency object"""
        try:
            return moneyed.get_currency(self.code)
        except Exception:
            return None

    @property
    def symbol(self):
        """Get currency symbol with custom override support"""
        if self.custom_symbol:
            return self.custom_symbol
        currency = self.currency_obj
        return getattr(currency, "symbol", self.code) if currency else self.code

    def get_currency_name(self):
        """Get full currency name (e.g., 'United States Dollar')"""
        currency = self.currency_obj
        return getattr(currency, "name", self.code) if currency else self.code

    def get_country_flag(self):
        """Get country flag emoji (requires django-countries integration)"""
        # Map common currency codes to country codes
        currency_to_country = {
            "USD": "US",
            "EUR": "EU",
            "GBP": "GB",
            "JPY": "JP",
            "CNY": "CN",
            "AUD": "AU",
            "CAD": "CA",
            "CHF": "CH",
            "INR": "IN",
            "MXN": "MX",
            "BRL": "BR",
            "ZAR": "ZA",
            "AED": "AE",
            "SAR": "SA",
            "SGD": "SG",
            "HKD": "HK",
            "NZD": "NZ",
            "SEK": "SE",
            "NOK": "NO",
            "DKK": "DK",
            "PLN": "PL",
            "THB": "TH",
            "IDR": "ID",
            "MYR": "MY",
            "PHP": "PH",
            "CZK": "CZ",
            "ILS": "IL",
            "CLP": "CL",
            "VND": "VN",
            "KRW": "KR",
            "TRY": "TR",
            "RUB": "RU",
            "HUF": "HU",
            "RON": "RO",
            "ARS": "AR",
            "COP": "CO",
            "PEN": "PE",
            "UAH": "UA",
            "EGP": "EG",
            "PKR": "PK",
            "BDT": "BD",
            "NGN": "NG",
            "MAD": "MA",
            "KES": "KE",
        }

        country_code = currency_to_country.get(self.code, "")
        if country_code:
            try:
                from django_countries import countries

                country = countries.countries.get(country_code)
                if country:
                    return country.flag
            except (ImportError, AttributeError):
                pass

        return ""

    # Class Methods
    @classmethod
    def get_active_currencies(cls):
        """Get all active currencies in display order"""
        return cls.objects.filter(is_active=True).order_by("order", "code")

    @classmethod
    def get_active_codes(cls):
        """Get list of active currency codes"""
        return list(cls.get_active_currencies().values_list("code", flat=True))

    @classmethod
    def activate_currency(cls, code):
        """Activate a currency by code"""
        currency, created = cls.objects.get_or_create(
            code=code.upper(), defaults={"is_active": True}
        )
        if not created and not currency.is_active:
            currency.is_active = True
            currency.save(update_fields=["is_active"])
        return currency

    @classmethod
    def deactivate_currency(cls, code):
        """Deactivate a currency by code"""
        try:
            currency = cls.objects.get(code=code.upper())
            currency.is_active = False
            currency.save(update_fields=["is_active"])
            return currency
        except cls.DoesNotExist:
            return None
