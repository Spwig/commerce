from django.db import models
from django.utils.translation import gettext_lazy as _


class SEOProviderAccount(models.Model):
    """
    Merchant's connection to an SEO generation provider.
    Pattern follows exchange_rates/models.py ExchangeRateProviderAccount.
    """

    site = models.ForeignKey(
        "sites.Site",
        on_delete=models.CASCADE,
        default=1,
        verbose_name=_("Site"),
        help_text=_("Site this provider account belongs to"),
    )

    component = models.ForeignKey(
        "component_updates.ComponentRegistry",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        limit_choices_to={"component_type": "seo_generator_provider"},
        related_name="seo_provider_accounts",
        verbose_name=_("Provider Component"),
        help_text=_("SEO provider component from update system (null for built-in)"),
    )

    provider_key = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Provider Key"),
        help_text=_("Built-in provider key (e.g., 'deterministic'). Used when component is null."),
    )

    name = models.CharField(
        max_length=255,
        verbose_name=_("Account Name"),
        help_text=_("Friendly name for this provider account"),
    )

    credentials = models.BinaryField(
        null=True,
        blank=True,
        verbose_name=_("Encrypted Credentials"),
        help_text=_("Encrypted API credentials for this provider"),
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
        help_text=_("Whether this provider account is active"),
    )

    is_primary = models.BooleanField(
        default=False,
        verbose_name=_("Primary Provider"),
        help_text=_("Use this provider as primary source for SEO generation"),
    )

    priority = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Priority"),
        help_text=_("Priority for fallback chain (lower = higher priority)"),
    )

    settings = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Provider Settings"),
        help_text=_("Provider-specific settings and configuration"),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("SEO Provider Account")
        verbose_name_plural = _("SEO Provider Accounts")
        ordering = ["-is_primary", "priority", "name"]
        indexes = [
            models.Index(fields=["site", "is_active"]),
            models.Index(fields=["is_primary"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["site", "is_primary"],
                condition=models.Q(is_primary=True),
                name="unique_primary_seo_provider",
            )
        ]

    def __str__(self):
        if self.component:
            return f"{self.name} ({self.component.name})"
        return f"{self.name} ({self.provider_key})"

    def get_provider_instance(self):
        """Get initialized provider instance."""
        if self.component:
            from seo_generator.providers.registry import ProviderRegistry
            from seo_generator.utils.encryption import decrypt_credentials

            provider_class = ProviderRegistry.get_provider(self.component.slug)
            if not provider_class:
                raise ValueError(f"Provider {self.component.slug} not found in registry")

            credentials = decrypt_credentials(self.credentials) if self.credentials else {}
            return provider_class(credentials=credentials, config=self.settings)
        else:
            # Built-in provider
            from seo_generator.providers.registry import ProviderRegistry

            provider_class = ProviderRegistry.get_provider(self.provider_key)
            if not provider_class:
                raise ValueError(f"Provider {self.provider_key} not found in registry")
            return provider_class(config=self.settings)

    def save(self, *args, **kwargs):
        # Auto-set is_primary if this is the first account
        if not self.pk and not SEOProviderAccount.objects.exists():
            self.is_primary = True
        super().save(*args, **kwargs)
