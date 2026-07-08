from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

User = get_user_model()


class SetupProgress(models.Model):
    """
    Tracks the setup progress for the store. This should be a singleton model.
    """

    # Basic setup completion flags
    admin_user_configured = models.BooleanField(
        default=False,
        help_text=_("Admin user account has been properly configured")
    )

    site_info_completed = models.BooleanField(
        default=False,
        help_text=_("Basic site information (name, URL, description) completed")
    )

    contact_info_completed = models.BooleanField(
        default=False,
        help_text=_("Contact information (emails, phone) completed")
    )

    business_address_completed = models.BooleanField(
        default=False,
        help_text=_("Business address information completed")
    )

    currency_locale_completed = models.BooleanField(
        default=False,
        help_text=_("Currency and locale settings configured")
    )

    payment_methods_configured = models.BooleanField(
        default=False,
        help_text=_("Payment provider setup has been acknowledged")
    )

    ecommerce_settings_completed = models.BooleanField(
        default=False,
        help_text=_("Core e-commerce settings have been configured")
    )

    # Optional setup completion flags
    favicon_uploaded = models.BooleanField(
        default=False,
        help_text=_("Site favicon has been uploaded")
    )

    seo_settings_completed = models.BooleanField(
        default=False,
        help_text=_("SEO meta tags have been configured")
    )

    social_media_completed = models.BooleanField(
        default=False,
        help_text=_("Social media links have been added")
    )

    email_settings_completed = models.BooleanField(
        default=False,
        help_text=_("Email notification settings configured")
    )

    # Setup metadata
    setup_started_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("When the setup wizard was first started")
    )

    setup_completed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("When the essential setup was completed")
    )

    setup_started_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='setup_started',
        help_text=_("User who started the setup process")
    )

    setup_completed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='setup_completed',
        help_text=_("User who completed the setup process")
    )

    last_step_completed = models.CharField(
        max_length=50,
        blank=True,
        help_text=_("Last setup step that was completed")
    )

    wizard_skipped = models.BooleanField(
        default=False,
        help_text=_("User chose to skip the setup wizard")
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Setup Progress")
        verbose_name_plural = _("Setup Progress")

    def __str__(self):
        return f"Setup Progress - {self.get_completion_percentage()}% complete"

    def save(self, *args, **kwargs):
        """
        Ensure only one instance of SetupProgress exists (singleton pattern)
        """
        if not self.pk and SetupProgress.objects.exists():
            # If trying to create a new instance but one already exists, update the existing one
            existing = SetupProgress.objects.first()
            self.pk = existing.pk
        elif not self.pk:
            # If this is the first instance, force ID to 1
            self.pk = 1

        # Auto-mark setup as started if any progress is made
        if not self.setup_started_at and self._has_any_progress():
            self.setup_started_at = timezone.now()

        # Auto-mark setup as completed if all essential items are done
        if not self.setup_completed_at and self.is_essential_setup_complete():
            self.setup_completed_at = timezone.now()

        super().save(*args, **kwargs)

    @classmethod
    def get_progress(cls):
        """
        Get the current setup progress instance, creating one if it doesn't exist
        """
        progress, created = cls.objects.get_or_create(pk=1)
        return progress

    def _has_any_progress(self):
        """Check if any setup progress has been made"""
        return any([
            self.site_info_completed,
            self.contact_info_completed,
            self.currency_locale_completed,
            self.payment_methods_configured,
            self.ecommerce_settings_completed,
        ])

    def get_essential_items(self):
        """Get list of essential setup items with their completion status"""
        return [
            {
                'key': 'site_info_completed',
                'step_key': 'site_info',
                'label': _('Site Information'),
                'description': _('Set your store name, URL, and description'),
                'completed': self.site_info_completed,
                'required': True,
                'icon': 'fas fa-store',
                'order': 1
            },
            {
                'key': 'contact_info_completed',
                'step_key': 'contact_info',
                'label': _('Contact Information'),
                'description': _('Configure admin and support email addresses'),
                'completed': self.contact_info_completed,
                'required': True,
                'icon': 'fas fa-envelope',
                'order': 2
            },
            {
                'key': 'currency_locale_completed',
                'step_key': 'currency_locale',
                'label': _('Currency & Locale'),
                'description': _('Set your default currency, language, and timezone'),
                'completed': self.currency_locale_completed,
                'required': True,
                'icon': 'fas fa-coins',
                'order': 3
            },
            {
                'key': 'payment_methods_configured',
                'step_key': 'payment_methods',
                'label': _('Payment Providers'),
                'description': _('Review payment provider configuration'),
                'completed': self.payment_methods_configured,
                'required': True,
                'icon': 'fas fa-credit-card',
                'order': 4
            },
        ]

    def get_optional_items(self):
        """Get list of optional setup items with their completion status"""
        return [
            {
                'key': 'business_address_completed',
                'step_key': 'business_address',
                'label': _('Business Address'),
                'description': _('Add your business address information'),
                'completed': self.business_address_completed,
                'required': False,
                'icon': 'fas fa-map-marker-alt',
                'order': 5
            },
            {
                'key': 'ecommerce_settings_completed',
                'step_key': 'ecommerce_settings',
                'label': _('E-commerce Settings'),
                'description': _('Configure checkout and inventory settings'),
                'completed': self.ecommerce_settings_completed,
                'required': False,
                'icon': 'fas fa-cog',
                'order': 6
            },
            {
                'key': 'email_settings_completed',
                'step_key': 'email_settings',
                'label': _('Email Notifications'),
                'description': _('Configure email notification preferences'),
                'completed': self.email_settings_completed,
                'required': False,
                'icon': 'fas fa-bell',
                'order': 7
            },
            {
                'key': 'seo_settings_completed',
                'step_key': 'seo_settings',
                'label': _('SEO Settings'),
                'description': _('Set up meta tags and SEO defaults'),
                'completed': self.seo_settings_completed,
                'required': False,
                'icon': 'fas fa-search',
                'order': 8
            },
            {
                'key': 'social_media_completed',
                'step_key': 'social_media',
                'label': _('Social Media'),
                'description': _('Add links to your social media profiles'),
                'completed': self.social_media_completed,
                'required': False,
                'icon': 'fas fa-share-alt',
                'order': 9
            },
        ]

    def get_all_items(self):
        """Get all setup items (essential + optional) sorted by order"""
        all_items = self.get_essential_items() + self.get_optional_items()
        return sorted(all_items, key=lambda x: x['order'])

    def get_completion_percentage(self):
        """Calculate overall completion percentage"""
        all_items = self.get_all_items()
        if not all_items:
            return 0

        completed_count = sum(1 for item in all_items if item['completed'])
        return round((completed_count / len(all_items)) * 100)

    def get_essential_completion_percentage(self):
        """Calculate completion percentage for essential items only"""
        essential_items = self.get_essential_items()
        if not essential_items:
            return 0

        completed_count = sum(1 for item in essential_items if item['completed'])
        return round((completed_count / len(essential_items)) * 100)

    def is_essential_setup_complete(self):
        """Check if all essential setup items are completed"""
        return self.get_essential_completion_percentage() == 100

    def is_setup_complete(self):
        """Check if all setup items (essential + optional) are completed"""
        return self.get_completion_percentage() == 100

    def get_next_step(self):
        """Get the next incomplete setup step"""
        # Check essential items first (in order)
        essential_fields = [
            ('site_info_completed', 'site_info'),
            ('contact_info_completed', 'contact_info'),
            ('currency_locale_completed', 'currency_locale'),
            ('payment_methods_configured', 'payment_methods'),
        ]

        for field_name, step_key in essential_fields:
            if not getattr(self, field_name):
                return {
                    'key': step_key,
                    'label': step_key.replace('_', ' ').title(),
                    'required': True,
                    'completed': False
                }

        # Then check optional items
        optional_fields = [
            ('business_address_completed', 'business_address'),
            ('ecommerce_settings_completed', 'ecommerce_settings'),
            ('email_settings_completed', 'email_settings'),
            ('seo_settings_completed', 'seo_settings'),
            ('social_media_completed', 'social_media'),
        ]

        for field_name, step_key in optional_fields:
            if not getattr(self, field_name):
                return {
                    'key': step_key,
                    'label': step_key.replace('_', ' ').title(),
                    'required': False,
                    'completed': False
                }

        return None

    def get_incomplete_essential_items(self):
        """Get list of incomplete essential setup items"""
        return [item for item in self.get_essential_items() if not item['completed']]

    def get_incomplete_optional_items(self):
        """Get list of incomplete optional setup items"""
        return [item for item in self.get_optional_items() if not item['completed']]

    def mark_step_completed(self, step_key, user=None):
        """Mark a specific setup step as completed"""
        if hasattr(self, step_key):
            setattr(self, step_key, True)
            self.last_step_completed = step_key

            # If this completes essential setup, mark completion and go live
            if self.is_essential_setup_complete() and not self.setup_completed_at:
                self.setup_completed_at = timezone.now()
                if user:
                    self.setup_completed_by = user

                # Auto-disable maintenance mode so the store goes live
                try:
                    from core.models import SiteSettings
                    site_settings = SiteSettings.get_settings()
                    if site_settings and site_settings.maintenance_mode:
                        site_settings.maintenance_mode = False
                        site_settings.save(update_fields=['maintenance_mode'])
                        from django.core.cache import cache
                        cache.delete('maintenance_mode_status')
                except Exception:
                    pass  # Don't block setup completion if this fails

            self.save()
            return True
        return False

    def start_setup(self, user=None):
        """Mark setup as started"""
        if not self.setup_started_at:
            self.setup_started_at = timezone.now()
            if user:
                self.setup_started_by = user
            self.save()

    def skip_wizard(self, user=None):
        """Mark wizard as skipped by user"""
        self.wizard_skipped = True
        if not self.setup_started_at:
            self.setup_started_at = timezone.now()
            if user:
                self.setup_started_by = user
        self.save()

    def get_group_status(self):
        """
        Map individual step flags to the 5-group wizard structure.
        Returns a list of dicts with group key and completion status.
        """
        return [
            {
                'key': 'store',
                'completed': self.site_info_completed,
            },
            {
                'key': 'contact',
                'completed': self.contact_info_completed,
            },
            {
                'key': 'locale',
                'completed': self.currency_locale_completed,
            },
            {
                'key': 'payments',
                'completed': self.payment_methods_configured,
            },
            {
                'key': 'finetune',
                'completed': all([
                    self.ecommerce_settings_completed,
                    self.email_settings_completed,
                    self.seo_settings_completed,
                    self.social_media_completed,
                ]),
            },
        ]

    def get_essential_groups_completed(self):
        """Count of completed essential groups (first 4)."""
        groups = self.get_group_status()
        return sum(1 for g in groups[:4] if g['completed'])

    def get_essential_groups_total(self):
        """Total number of essential groups."""
        return 4
