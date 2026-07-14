import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.models import SoftDeleteModel

User = get_user_model()


class EmailAccount(models.Model):
    """
    Merchant's connection to an email provider component.
    Stores encrypted credentials and configuration for email sending.
    Pattern follows exchange_rates/models.py ExchangeRateProviderAccount.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    site = models.ForeignKey(
        "sites.Site",
        on_delete=models.CASCADE,
        verbose_name=_("site"),
        help_text=_("Site this email account belongs to"),
    )

    component = models.ForeignKey(
        "component_updates.ComponentRegistry",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        limit_choices_to={"component_type": "email_provider"},
        related_name="email_accounts",
        verbose_name=_("provider component"),
        help_text=_("Email provider component from update system (null for built-in providers)"),
    )

    provider_key = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("provider key"),
        help_text=_(
            "Provider identifier (e.g., 'builtin_smtp', 'gmail_api'). Required for built-in providers."
        ),
    )

    name = models.CharField(
        max_length=255,
        verbose_name=_("account name"),
        help_text=_("Friendly name for this email account (e.g., 'Main Email Account')"),
    )

    # Sender configuration
    from_email = models.EmailField(
        verbose_name=_("from email"), help_text=_("Default sender email address")
    )

    from_name = models.CharField(
        max_length=255, blank=True, verbose_name=_("from name"), help_text=_("Default sender name")
    )

    reply_to = models.EmailField(
        blank=True, verbose_name=_("reply-to email"), help_text=_("Default reply-to email address")
    )

    # Encrypted credentials
    credentials = models.BinaryField(
        verbose_name=_("encrypted credentials"),
        help_text=_("Encrypted API credentials for this provider"),
    )

    # Status flags
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("active"),
        help_text=_("Whether this email account is active and should be used for sending"),
    )

    is_default = models.BooleanField(
        default=False,
        verbose_name=_("default account"),
        help_text=_("Use this account as default for sending emails"),
    )

    # Provider-specific settings
    settings = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("provider settings"),
        help_text=_("Provider-specific settings and configuration"),
    )

    # Connection health tracking
    connection_status = models.CharField(
        max_length=32,
        choices=[
            ("unknown", _("Unknown")),
            ("connected", _("Connected")),
            ("error", _("Error")),
        ],
        default="unknown",
        verbose_name=_("connection status"),
        help_text=_("Current connection status with provider"),
    )

    connection_error = models.TextField(
        blank=True,
        verbose_name=_("connection error"),
        help_text=_("Error message from last connection test"),
    )

    last_tested_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("last tested at"),
        help_text=_("When connection was last tested"),
    )

    # DNS validation tracking
    dns_validated = models.BooleanField(
        default=False,
        verbose_name=_("DNS validated"),
        help_text=_("Whether DNS records (SPF/DKIM/DMARC) have been validated"),
    )

    dns_validated_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("DNS validated at"),
        help_text=_("When DNS validation last passed"),
    )

    dns_domain = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("DNS domain"),
        help_text=_("Domain used for DNS validation (if different from email domain)"),
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_email_accounts",
        verbose_name=_("created by"),
    )

    class Meta:
        verbose_name = _("email account")
        verbose_name_plural = _("email accounts")
        ordering = ["-is_default", "-is_active", "name"]
        indexes = [
            models.Index(fields=["site", "is_active"]),
            models.Index(fields=["is_default"]),
            models.Index(fields=["connection_status"]),
        ]
        constraints = [
            # Only one default account per site
            models.UniqueConstraint(
                fields=["site", "is_default"],
                condition=models.Q(is_default=True),
                name="unique_default_email_account_per_site",
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.from_email})"

    def save(self, *args, **kwargs):
        """
        Override save to ensure only one default account per site.
        If this account is being set as default, unset all other defaults for this site.
        """
        if self.is_default:
            # Unset all other defaults for this site
            EmailAccount.objects.filter(site=self.site, is_default=True).exclude(pk=self.pk).update(
                is_default=False
            )

        super().save(*args, **kwargs)

    def validate_constraints(self, exclude=None):
        """
        Override to suppress the unique_default_email_account_per_site constraint
        during form validation. The save() method handles clearing other defaults
        before saving, so this constraint check would falsely reject valid changes.
        """
        from django.core.exceptions import ValidationError

        try:
            super().validate_constraints(exclude=exclude)
        except ValidationError as e:
            if hasattr(e, "error_dict"):
                errors = {}
                for key, error_list in e.error_dict.items():
                    filtered = [
                        err
                        for err in error_list
                        if "unique_default_email_account_per_site"
                        not in getattr(err, "message", str(err))
                    ]
                    if filtered:
                        errors[key] = filtered
                if errors:
                    raise ValidationError(errors)
            else:
                raise

    def get_credentials(self):
        """
        Decrypt and return credentials as a dictionary.

        Returns:
            dict: Decrypted credentials
        """
        from email_system.utils.encryption import decrypt_credentials

        if not self.credentials:
            return {}

        return decrypt_credentials(self.credentials)

    def set_credentials(self, credentials_dict):
        """
        Encrypt and store credentials.

        Args:
            credentials_dict (dict): Credentials to encrypt and store
        """
        from email_system.utils.encryption import encrypt_credentials

        self.credentials = encrypt_credentials(credentials_dict)

    def get_provider(self):
        """
        Get the provider class for this account.

        Returns:
            class: EmailProviderBase subclass
        """
        from email_system.providers.registry import ProviderRegistry

        provider_class = ProviderRegistry.get_provider(self.component.slug)
        if not provider_class:
            raise ValueError(f"Provider {self.component.slug} not found in registry")

        return provider_class

    def get_provider_instance(self):
        """Get initialized provider instance"""
        from email_system.providers.registry import ProviderRegistry
        from email_system.utils.encryption import decrypt_credentials

        # Determine provider slug: use component slug for installed providers, provider_key for built-in
        if self.component:
            provider_slug = self.component.slug
        elif self.provider_key:
            provider_slug = self.provider_key
        else:
            raise ValueError("EmailAccount must have either a component or provider_key")

        provider_class = ProviderRegistry.get_provider(provider_slug)
        if not provider_class:
            raise ValueError(f"Provider {provider_slug} not found in registry")

        # Decrypt credentials and pass to provider
        credentials = decrypt_credentials(self.credentials)
        return provider_class(credentials=credentials, config=self.settings)


class EmailTemplate(SoftDeleteModel):
    """
    Transactional email templates with multi-language support.
    Supports MJML for responsive email rendering.

    Inherits soft delete functionality from SoftDeleteModel:
    - is_deleted: Boolean flag
    - deleted_at: Timestamp of deletion
    - deleted_by: User who deleted the template
    - delete(): Soft delete (moves to recycle bin)
    - hard_delete(): Permanent deletion
    - restore(): Recover from recycle bin
    """

    # Prefixes for template types that only exist on SPWIG HQ installations.
    # Templates with these prefixes are skipped during seeding and hidden
    # from admin on non-HQ (merchant) installations.
    HQ_ONLY_PREFIXES = ("hosted_", "license_", "dev_")

    @classmethod
    def is_hq_only_type(cls, template_type: str) -> bool:
        """Check if a template_type is HQ-only."""
        return template_type.startswith(cls.HQ_ONLY_PREFIXES)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    site = models.ForeignKey(
        "sites.Site",
        on_delete=models.CASCADE,
        verbose_name=_("site"),
        help_text=_("Site this template belongs to"),
    )

    # Template identification
    template_type = models.CharField(
        max_length=64,
        choices=[
            # Core E-commerce
            ("account_invitation", _("Account Invitation")),
            ("account_welcome", _("Account Welcome")),
            ("delivery_confirmation", _("Delivery Confirmation")),
            ("email_verification", _("Email Verification")),
            ("message_reply", _("Message Reply")),
            ("order_cancelled", _("Order Cancelled")),
            ("order_confirmation", _("Order Confirmation")),
            ("order_delay", _("Order Delay Notification")),
            ("order_note_notification", _("Order Note Notification")),
            ("order_shipped", _("Order Shipped")),
            ("password_reset", _("Password Reset")),
            ("staff_invitation", _("Staff Invitation")),
            ("payment_confirmation", _("Payment Confirmation")),
            ("refund_notification", _("Refund Notification")),
            ("review_request", _("Review Request")),
            ("shipping_confirmation", _("Shipping Confirmation")),
            ("shipping_delayed", _("Shipping: Delayed")),
            ("shipping_exception", _("Shipping: Exception")),
            ("shipping_tracking_milestone", _("Shipping: Tracking Milestone")),
            ("order_status_update", _("Order Status Update")),
            # Returns
            ("return_request_confirmation", _("Returns: Request Received")),
            ("return_request_approved", _("Returns: Approved")),
            ("return_request_rejected", _("Returns: Rejected")),
            ("return_received", _("Returns: Package Received")),
            ("return_refund_processed", _("Returns: Refund Processed")),
            # Admin Notifications
            ("admin_new_order", _("Admin: New Order")),
            ("admin_payment_failed", _("Admin: Payment Failed")),
            ("admin_payment_sdk_failure", _("Admin: Payment SDK Failure")),
            ("admin_return_inspection_reminder", _("Admin: Return Inspection Reminder")),
            ("admin_report_abandoned_carts_summary", _("Admin: Abandoned Carts Summary")),
            ("admin_report_customer_insights", _("Admin: Customer Insights")),
            ("admin_report_daily_sales", _("Admin: Daily Sales Report")),
            ("admin_report_low_stock_alert", _("Admin: Low Stock Alert")),
            ("admin_report_monthly_review", _("Admin: Monthly Review")),
            ("admin_report_revenue_forecast", _("Admin: Revenue Forecast")),
            ("admin_report_top_products", _("Admin: Top Products")),
            ("admin_report_weekly_digest", _("Admin: Weekly Digest")),
            # Affiliate Program
            ("affiliate_account_activated", _("Affiliate: Account Activated")),
            ("affiliate_account_approved", _("Affiliate: Account Approved")),
            ("affiliate_account_rejected", _("Affiliate: Account Rejected")),
            ("affiliate_account_suspended", _("Affiliate: Account Suspended")),
            ("affiliate_commission_approved", _("Affiliate: Commission Approved")),
            ("affiliate_commission_earned", _("Affiliate: Commission Earned")),
            ("affiliate_commission_rejected", _("Affiliate: Commission Rejected")),
            ("affiliate_commission_reversed", _("Affiliate: Commission Reversed")),
            ("affiliate_high_commission_alert", _("Affiliate: High Commission Alert")),
            ("affiliate_monthly_report", _("Affiliate: Monthly Report")),
            ("affiliate_payout_cancelled", _("Affiliate: Payout Cancelled")),
            ("affiliate_payout_completed", _("Affiliate: Payout Completed")),
            ("affiliate_payout_failed", _("Affiliate: Payout Failed")),
            ("affiliate_payout_processing", _("Affiliate: Payout Processing")),
            ("affiliate_payout_threshold_reached", _("Affiliate: Payout Threshold Reached")),
            ("affiliate_program_approved", _("Affiliate: Program Approved")),
            ("affiliate_program_rejected", _("Affiliate: Program Rejected")),
            # Backups
            ("backup_completed", _("Backup: Completed")),
            ("backup_failed", _("Backup: Failed")),
            ("backup_restore_completed", _("Backup: Restore Completed")),
            ("backup_restore_failed", _("Backup: Restore Failed")),
            ("backup_scheduled_missed", _("Backup: Scheduled Missed")),
            ("backup_size_warning", _("Backup: Size Warning")),
            ("backup_storage_quota_alert", _("Backup: Storage Quota Alert")),
            ("backup_weekly_report", _("Backup: Weekly Report")),
            # Bookings
            ("admin_booking_cancelled", _("Admin: Booking Cancelled")),
            ("admin_new_booking", _("Admin: New Booking")),
            ("booking_cancelled", _("Booking: Cancelled")),
            ("booking_completed", _("Booking: Completed")),
            ("booking_confirmation", _("Booking: Confirmation")),
            ("booking_deposit_receipt", _("Booking: Deposit Receipt")),
            ("booking_no_show", _("Booking: No Show")),
            ("booking_pending_confirmation", _("Booking: Pending Confirmation")),
            ("booking_recurring_created", _("Booking: Recurring Series Created")),
            ("booking_reminder", _("Booking: Reminder")),
            ("booking_rescheduled", _("Booking: Rescheduled")),
            ("booking_waitlist_notification", _("Booking: Waitlist Notification")),
            # Blog
            ("blog_comment_approved", _("Blog: Comment Approved")),
            ("blog_comment_reply", _("Blog: Comment Reply")),
            ("blog_digest_weekly", _("Blog: Weekly Digest")),
            ("blog_post_published", _("Blog: Post Published")),
            ("blog_subscriber_welcome", _("Blog: Subscriber Welcome")),
            ("blog_subscription_confirmed", _("Blog: Subscription Confirmed")),
            # Cart Recovery
            ("cart_abandoned_1h", _("Cart: Abandoned (1 Hour)")),
            ("cart_abandoned_24h", _("Cart: Abandoned (24 Hours)")),
            ("cart_abandoned_48h", _("Cart: Abandoned (48 Hours)")),
            ("cart_abandoned_discount", _("Cart: Abandoned (Discount Offer)")),
            ("cart_recovered_thank_you", _("Cart: Recovery Thank You")),
            # Component Updates
            ("component_deprecated_warning", _("Component: Deprecated Warning")),
            ("component_incompatible_warning", _("Component: Incompatible Warning")),
            ("component_rollback_success", _("Component: Rollback Success")),
            ("component_security_update", _("Component: Security Update")),
            ("component_update_available", _("Component: Update Available")),
            ("component_update_failed", _("Component: Update Failed")),
            ("component_update_installed", _("Component: Update Installed")),
            # Developer Portal
            ("dev_account_approved", _("Developer: Account Approved")),
            ("dev_account_rejected", _("Developer: Account Rejected")),
            ("dev_account_suspended", _("Developer: Account Suspended")),
            ("dev_component_published", _("Developer: Component Published")),
            ("dev_license_approved", _("Developer: License Approved")),
            ("dev_license_rejected", _("Developer: License Rejected")),
            ("dev_new_review", _("Developer: New Review")),
            ("dev_registration_ack", _("Developer: Registration Received")),
            ("dev_review_digest", _("Developer: Review Digest")),
            ("dev_revision_requested", _("Developer: Revision Requested")),
            ("dev_submission_approved", _("Developer: Submission Approved")),
            ("dev_submission_received", _("Developer: Submission Received")),
            ("dev_submission_rejected", _("Developer: Submission Rejected")),
            # Digital Products
            ("digital_product_delivery", _("Digital Product: Download Ready")),
            ("digital_product_download_expired", _("Digital Product: Download Link Expired")),
            ("digital_product_license_expired", _("Digital Product: License Expired")),
            ("digital_product_license_key", _("Digital Product: License Key")),
            # License Checkout (HQ)
            ("license_trial_welcome", _("License: Trial Welcome")),
            ("license_purchase_confirmation", _("License: Purchase Confirmation")),
            ("license_maintenance_renewal", _("License: Maintenance Renewal")),
            # Hosted Solution (HQ)
            ("hosted_provision_failed", _("Hosted: Provisioning Failed")),
            ("hosted_provision_complete", _("Hosted: Provisioning Complete")),
            ("hosted_onboarding_tips", _("Hosted: Onboarding Tips")),
            # Hosted Subscription Lifecycle (HQ)
            ("hosted_subscription_confirmation", _("Hosted: Subscription Confirmation")),
            ("hosted_payment_receipt", _("Hosted: Payment Receipt")),
            ("hosted_payment_failed", _("Hosted: Payment Failed")),
            ("hosted_payment_recovered", _("Hosted: Payment Recovered")),
            ("hosted_suspension_warning", _("Hosted: Suspension Warning")),
            ("hosted_suspended", _("Hosted: Account Suspended")),
            ("hosted_cancellation_confirmation", _("Hosted: Cancellation Confirmed")),
            ("hosted_termination_warning", _("Hosted: Termination Warning")),
            ("hosted_terminated", _("Hosted: Account Terminated")),
            # Hosted Onboarding Sequence (HQ)
            ("hosted_onboarding_day3", _("Hosted: Onboarding Day 3")),
            ("hosted_onboarding_day7", _("Hosted: Onboarding Day 7")),
            ("hosted_onboarding_day14", _("Hosted: Onboarding Day 14")),
            # Form Builder
            ("form_submission_admin_notification", _("Form: Admin Notification")),
            ("form_submission_approved", _("Form: Submission Approved")),
            ("form_submission_auto_response", _("Form: Auto Response")),
            ("form_submission_confirmation", _("Form: Submission Confirmation")),
            ("form_submission_rejected", _("Form: Submission Rejected")),
            # Gift Cards
            ("gift_card_delivery", _("Gift Card: Delivery Email")),
            # Loyalty Program
            ("loyalty_anniversary_bonus", _("Loyalty: Anniversary Bonus")),
            ("loyalty_birthday_bonus", _("Loyalty: Birthday Bonus")),
            ("loyalty_double_points_event", _("Loyalty: Double Points Event")),
            ("loyalty_points_earned", _("Loyalty: Points Earned")),
            ("loyalty_points_expiring", _("Loyalty: Points Expiring")),
            ("loyalty_referral_bonus", _("Loyalty: Referral Bonus")),
            ("loyalty_reward_available", _("Loyalty: Reward Available")),
            ("loyalty_tier_demotion_warning", _("Loyalty: Tier Demotion Warning")),
            ("loyalty_tier_upgrade", _("Loyalty: Tier Upgrade")),
            ("loyalty_welcome", _("Loyalty: Welcome")),
            # Marketing
            ("newsletter", _("Newsletter")),
            # POS
            ("pos_cash_discrepancy_alert", _("POS: Cash Discrepancy Alert")),
            ("pos_daily_z_report", _("POS: Daily Z-Report")),
            ("pos_high_value_transaction", _("POS: High Value Transaction")),
            ("pos_low_inventory_alert", _("POS: Low Inventory Alert")),
            ("pos_receipt", _("POS: Receipt")),
            ("pos_shift_closed_report", _("POS: Shift Closed Report")),
            ("pos_terminal_offline", _("POS: Terminal Offline")),
            ("pos_license_expiration_warning", _("POS: License Expiration Warning")),
            # Product Feeds
            ("feed_generation_completed", _("Feed: Generation Completed")),
            ("feed_generation_failed", _("Feed: Generation Failed")),
            ("feed_sync_failed", _("Feed: Sync Failed")),
            ("feed_sync_success", _("Feed: Sync Success")),
            ("feed_validation_errors", _("Feed: Validation Errors")),
            ("feed_weekly_report", _("Feed: Weekly Report")),
            # Referral Program
            ("referral_invitation", _("Referral: Invitation Email")),
            ("referral_reward_expired", _("Referral: Reward Expired")),
            ("referral_reward_expiring", _("Referral: Reward Expiring Soon")),
            ("referral_reward_issued_referee", _("Referral: Reward Issued (Referee)")),
            ("referral_reward_issued_referrer", _("Referral: Reward Issued (Referrer)")),
            ("referral_reward_revoked", _("Referral: Reward Revoked")),
            ("referral_successful", _("Referral: Successful Referral")),
            # Stock Notifications
            ("back_in_stock", _("Back In Stock: Notification")),
            ("back_in_stock_low_stock_warning", _("Back In Stock: Low Stock Warning")),
            ("back_in_stock_waitlist_confirmation", _("Back In Stock: Waitlist Confirmation")),
            # Subscriptions
            ("subscription_addon_added", _("Subscription: Add-on Added")),
            ("subscription_addon_removed", _("Subscription: Add-on Removed")),
            ("subscription_canceled", _("Subscription: Canceled")),
            ("subscription_created", _("Subscription: Created")),
            ("subscription_dunning_final_notice", _("Subscription: Dunning Final Notice")),
            ("subscription_expired", _("Subscription: Expired")),
            ("subscription_paused", _("Subscription: Paused")),
            ("subscription_payment_failed", _("Subscription: Payment Failed")),
            ("subscription_payment_method_expiring", _("Subscription: Payment Method Expiring")),
            ("subscription_payment_success", _("Subscription: Payment Successful")),
            ("subscription_plan_downgraded", _("Subscription: Plan Downgraded")),
            ("subscription_plan_upgraded", _("Subscription: Plan Upgraded")),
            ("subscription_reactivated", _("Subscription: Reactivated")),
            ("subscription_renewal_reminder", _("Subscription: Renewal Reminder")),
            ("subscription_resumed", _("Subscription: Resumed")),
            ("subscription_trial_ending", _("Subscription: Trial Ending Soon")),
            # System Health
            ("system_health_critical", _("System: Critical Alert")),
            ("system_health_daily_report", _("System: Daily Health Report")),
            ("system_health_recovered", _("System: Issue Resolved")),
            ("system_health_warning", _("System: Warning")),
            ("system_performance_degraded", _("System: Performance Degraded")),
            # Translation Jobs
            ("translation_job_completed", _("Translation: Job Completed")),
            ("translation_job_failed", _("Translation: Job Failed")),
            ("translation_job_started", _("Translation: Job Started")),
            ("translation_quality_review_needed", _("Translation: Quality Review Needed")),
            # Wishlist
            ("wishlist_back_in_stock", _("Wishlist: Back In Stock")),
            ("wishlist_item_added_confirmation", _("Wishlist: Item Added")),
            ("wishlist_low_stock_warning", _("Wishlist: Low Stock Warning")),
            ("wishlist_price_drop", _("Wishlist: Price Drop")),
            ("wishlist_reminder_weekly", _("Wishlist: Weekly Reminder")),
            ("wishlist_shared_confirmation", _("Wishlist: Shared Confirmation")),
        ],
        verbose_name=_("template type"),
        help_text=_("Type of email (transactional or marketing)"),
    )

    language_code = models.CharField(
        max_length=7,
        default="en",
        verbose_name=_("language code"),
        help_text=_("Language code for this template (e.g., 'en', 'es', 'fr')"),
    )

    # Template content
    subject = models.CharField(
        max_length=255,
        verbose_name=_("subject"),
        help_text=_("Email subject line (supports {{ variables }})"),
    )

    html_content = models.TextField(
        verbose_name=_("HTML content"), help_text=_("HTML email content (MJML or plain HTML)")
    )

    text_content = models.TextField(
        blank=True,
        verbose_name=_("text content"),
        help_text=_("Plain text version (auto-generated if empty)"),
    )

    # Flags
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("active"),
        help_text=_("Whether this template is active and should be used"),
    )

    is_system = models.BooleanField(
        default=False,
        verbose_name=_("system template"),
        help_text=_("Pre-installed system template (can be customized)"),
    )

    # Version control
    version = models.IntegerField(
        default=1, verbose_name=_("version"), help_text=_("Template version number")
    )

    parent_template = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="versions",
        verbose_name=_("parent template"),
        help_text=_("Original template this was cloned from"),
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_email_templates",
        verbose_name=_("created by"),
    )

    class Meta:
        verbose_name = _("email template")
        verbose_name_plural = _("email templates")
        ordering = ["template_type", "language_code"]
        indexes = [
            models.Index(fields=["site", "template_type", "language_code"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["is_system", "is_active"]),
        ]
        # Note: No unique constraint - allows multiple templates per type/language
        # (system template + custom clones)

    def __str__(self):
        return f"{self.get_template_type_display()} ({self.language_code})"

    def clone(self, user=None, set_active=True, clone_language=None):
        """
        Clone this template for customization

        Creates a copy with is_system=False. If clone_language is specified,
        the clone will be created using that language's translation (if available),
        and only that specific translation will be included in the clone.

        Args:
            user: User performing the clone (optional)
            set_active: Set cloned template as active (default: True)
            clone_language: Language code to clone (if None, clones base + all translations)

        Returns:
            Cloned EmailTemplate instance
        """
        import logging

        from email_system.models import EmailTemplateTranslation

        logger = logging.getLogger(__name__)

        # Determine source content for clone
        subject = self.subject
        html_content = self.html_content
        text_content = self.text_content
        language_code = self.language_code

        if clone_language and clone_language != self.language_code:
            # Try to get translation in specified language
            translation = EmailTemplateTranslation.objects.filter(
                template=self, language_code=clone_language
            ).first()

            if translation:
                # Use translation content for the clone's base template
                subject = translation.subject
                html_content = translation.html_content
                text_content = translation.text_content
                language_code = clone_language

                logger.info(
                    f"Cloning template '{self.template_type}' using "
                    f"translation language={clone_language}"
                )
            else:
                logger.warning(
                    f"No translation found for language={clone_language}, "
                    f"cloning base template in {self.language_code}"
                )

        # Create clone
        clone = EmailTemplate.objects.create(
            site=self.site,
            template_type=self.template_type,
            subject=subject,
            html_content=html_content,
            text_content=text_content,
            is_system=False,
            is_active=set_active,
            language_code=language_code,
            created_by=user,
        )

        # If setting as active, deactivate others of same type+language
        if set_active:
            EmailTemplate.objects.filter(
                site=self.site,
                template_type=self.template_type,
                language_code=language_code,
                is_active=True,
            ).exclude(id=clone.id).update(is_active=False)

        # Handle translation cloning
        if clone_language:
            # Language-specific clone: don't copy any translations
            # The cloned base template IS the translation
            logger.info(
                f"Language-specific clone: no additional translations copied "
                f"(base is already in {language_code})"
            )
        else:
            # Legacy behavior: clone all translations
            for translation in self.translations.all():
                EmailTemplateTranslation.objects.create(
                    template=clone,
                    language_code=translation.language_code,
                    subject=translation.subject,
                    html_content=translation.html_content,
                    text_content=translation.text_content,
                    translated_by=translation.translated_by,
                    is_verified=translation.is_verified,
                    quality_score=translation.quality_score,
                )

        logger.info(
            f"Cloned template '{self.template_type}' (id={self.id}) to "
            f"custom template (id={clone.id}, language={language_code})"
        )

        return clone

    def activate(self):
        """
        Set this template as the active template for its type
        """
        import logging

        logger = logging.getLogger(__name__)

        # Deactivate all other templates of this type
        EmailTemplate.objects.filter(
            site=self.site, template_type=self.template_type, is_active=True
        ).exclude(id=self.id).update(is_active=False)

        # Activate this template
        self.is_active = True
        self.save(update_fields=["is_active"])

        logger.info(f"Activated template {self.id} ({self.template_type})")

    def deactivate(self):
        """
        Deactivate this template (falls back to system template)
        """
        import logging

        logger = logging.getLogger(__name__)

        self.is_active = False
        self.save(update_fields=["is_active"])

        logger.info(f"Deactivated template {self.id} ({self.template_type})")

        # Ensure system template is active as fallback
        system_template = EmailTemplate.objects.filter(
            site=self.site, template_type=self.template_type, is_system=True
        ).first()

        if (
            system_template
            and not EmailTemplate.objects.filter(
                site=self.site, template_type=self.template_type, is_active=True
            ).exists()
        ):
            system_template.is_active = True
            system_template.save(update_fields=["is_active"])
            logger.info("Activated system template as fallback")

    @classmethod
    def get_active_template(cls, template_type, site=None, language_code="en"):
        """
        Get the active template for a given type

        Fallback chain (deduplicated):
        For each language in [requested, site_default, 'en']:
          1. Active custom template
          2. Active system template
        Then for each language:
          3. Any system template (even inactive)

        Note: Deleted templates (is_deleted=True) are automatically excluded
        by the SoftDeleteManager.

        Args:
            template_type: Template type
            site: Site instance (optional, uses current site if None)
            language_code: Language code (default: 'en')

        Returns:
            Active EmailTemplate

        Raises:
            EmailTemplate.DoesNotExist: If no template found
        """
        if not site:
            from django.contrib.sites.models import Site

            site = Site.objects.get_current()

        # Build deduplicated fallback language list
        languages = [language_code]
        try:
            from core.models import SiteSettings

            site_default = SiteSettings.get_settings().default_language
            if site_default and site_default not in languages:
                languages.append(site_default)
        except Exception:
            pass
        if "en" not in languages:
            languages.append("en")

        # Try active template (custom first, then system) in each fallback language
        for lang in languages:
            active = (
                cls.objects.filter(
                    site=site, template_type=template_type, language_code=lang, is_active=True
                )
                .order_by("is_system")
                .first()
            )  # Custom templates (is_system=False) first

            if active:
                return active

        # Fall back to any system template in fallback order
        for lang in languages:
            system = cls.objects.filter(
                site=site, template_type=template_type, language_code=lang, is_system=True
            ).first()

            if system:
                return system

        raise cls.DoesNotExist(f"No template found for type '{template_type}'")

    def create_version(self, user=None):
        """
        Create a new version of this template

        Saves current state as a new record with incremented version number.
        Original template is updated with new content.

        Args:
            user: User creating the version

        Returns:
            New version EmailTemplate
        """
        import logging

        logger = logging.getLogger(__name__)

        # Create snapshot of current version
        version_snapshot = EmailTemplate.objects.create(
            site=self.site,
            template_type=self.template_type,
            subject=self.subject,
            html_content=self.html_content,
            text_content=self.text_content,
            is_system=False,
            is_active=False,
            language_code=self.language_code,
            version=self.version,
            parent_template=self.parent_template or self,
            created_by=user,
        )

        # Increment version on current template
        self.version += 1
        self.save(update_fields=["version"])

        logger.info(f"Created version {version_snapshot.version} of template {self.id}")

        return version_snapshot

    def revert_to_version(self, version_number):
        """
        Revert to a previous version

        Copies content from version snapshot back to this template

        Args:
            version_number: Version number to revert to
        """
        import logging

        logger = logging.getLogger(__name__)

        # Find version snapshot
        parent = self.parent_template or self
        version_snapshot = EmailTemplate.objects.get(parent_template=parent, version=version_number)

        # Copy content from snapshot
        self.subject = version_snapshot.subject
        self.html_content = version_snapshot.html_content
        self.text_content = version_snapshot.text_content
        self.save()

        logger.info(f"Reverted template {self.id} to version {version_number}")

    def get_version_history(self):
        """
        Get all versions of this template

        Returns:
            List of EmailTemplate versions ordered by version number (newest first)
        """
        parent = self.parent_template or self
        return EmailTemplate.objects.filter(
            models.Q(id=parent.id) | models.Q(parent_template=parent)
        ).order_by("-version")


class EmailOutbox(models.Model):
    """
    Email queue and history.
    Stores emails to be sent and tracks delivery status.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    site = models.ForeignKey(
        "sites.Site",
        on_delete=models.CASCADE,
        verbose_name=_("site"),
        help_text=_("Site this email belongs to"),
    )

    account = models.ForeignKey(
        EmailAccount,
        on_delete=models.SET_NULL,
        null=True,
        related_name="sent_emails",
        verbose_name=_("email account"),
        help_text=_("Email account used to send this message"),
    )

    # Email details
    to_email = models.EmailField(verbose_name=_("to email"), help_text=_("Recipient email address"))

    from_email = models.EmailField(
        verbose_name=_("from email"), help_text=_("Sender email address")
    )

    from_name = models.CharField(max_length=255, blank=True, verbose_name=_("from name"))

    subject = models.CharField(max_length=255, verbose_name=_("subject"))

    html_body = models.TextField(verbose_name=_("HTML body"))

    text_body = models.TextField(blank=True, verbose_name=_("text body"))

    reply_to = models.EmailField(blank=True, verbose_name=_("reply-to"))

    # Additional recipients
    cc = models.JSONField(
        default=list, blank=True, verbose_name=_("CC"), help_text=_("CC email addresses")
    )

    bcc = models.JSONField(
        default=list, blank=True, verbose_name=_("BCC"), help_text=_("BCC email addresses")
    )

    # Email metadata
    headers = models.JSONField(
        default=dict, blank=True, verbose_name=_("headers"), help_text=_("Custom email headers")
    )

    tags = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("tags"),
        help_text=_("Provider tags for categorization"),
    )

    # Attachments stored as references
    attachments = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("attachments"),
        help_text=_("Attachment file references"),
    )

    # Template reference
    template_type = models.CharField(
        max_length=64,
        blank=True,
        verbose_name=_("template type"),
        help_text=_("Template used to generate this email"),
    )

    # Status tracking
    status = models.CharField(
        max_length=32,
        choices=[
            ("queued", _("Queued")),
            ("held", _("Held")),
            ("logged", _("Logged")),
            ("sandbox_logged", _("Sandbox Logged")),
            ("sending", _("Sending")),
            ("sent", _("Sent")),
            ("failed", _("Failed")),
            ("bounced", _("Bounced")),
            ("skipped", _("Skipped")),
        ],
        default="queued",
        verbose_name=_("status"),
    )

    skip_reason = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("skip reason"),
        help_text=_(
            "Reason why email was skipped (e.g., 'user_preference_disabled', 'unsubscribed')"
        ),
    )

    provider_message_id = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("provider message ID"),
        help_text=_("Message ID from email provider"),
    )

    error_message = models.TextField(
        blank=True, verbose_name=_("error message"), help_text=_("Error details if sending failed")
    )

    # Priority (lower number = higher priority)
    priority = models.PositiveSmallIntegerField(
        default=5,
        verbose_name=_("priority"),
        help_text=_("Email priority (1=highest, 10=lowest). Lower priority emails are sent first."),
    )

    # Retry logic
    retry_count = models.PositiveIntegerField(
        default=0, verbose_name=_("retry count"), help_text=_("Number of send attempts")
    )

    max_retries = models.PositiveIntegerField(
        default=3, verbose_name=_("max retries"), help_text=_("Maximum number of retry attempts")
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))
    queued_at = models.DateTimeField(default=timezone.now, verbose_name=_("queued at"))
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name=_("sent at"))
    failed_at = models.DateTimeField(null=True, blank=True, verbose_name=_("failed at"))

    class Meta:
        verbose_name = _("email outbox")
        verbose_name_plural = _("email outbox")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["site", "status"]),
            models.Index(fields=["status", "queued_at"]),
            models.Index(fields=["to_email"]),
            models.Index(fields=["provider_message_id"]),
            models.Index(fields=["template_type"]),
        ]

    def __str__(self):
        return f"{self.subject} → {self.to_email} ({self.get_status_display()})"


class EmailEvent(models.Model):
    """
    Email delivery and engagement events (bounces, opens, clicks).
    Populated via webhooks from email providers.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.ForeignKey(
        EmailOutbox,
        on_delete=models.CASCADE,
        related_name="events",
        verbose_name=_("email"),
        help_text=_("Email this event relates to"),
    )

    # Event details
    event_type = models.CharField(
        max_length=32,
        choices=[
            ("delivered", _("Delivered")),
            ("bounced", _("Bounced")),
            ("opened", _("Opened")),
            ("clicked", _("Clicked")),
            ("complained", _("Complained")),
            ("unsubscribed", _("Unsubscribed")),
        ],
        verbose_name=_("event type"),
    )

    event_data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("event data"),
        help_text=_("Provider-specific event details"),
    )

    # Bounce details
    bounce_type = models.CharField(
        max_length=32,
        blank=True,
        choices=[
            ("hard", _("Hard Bounce")),
            ("soft", _("Soft Bounce")),
            ("transient", _("Transient")),
        ],
        verbose_name=_("bounce type"),
    )

    bounce_reason = models.TextField(blank=True, verbose_name=_("bounce reason"))

    # Tracking
    user_agent = models.TextField(
        blank=True,
        verbose_name=_("user agent"),
        help_text=_("Browser/client information for opens/clicks"),
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_("IP address"),
        help_text=_("IP address for opens/clicks"),
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))
    occurred_at = models.DateTimeField(
        default=timezone.now,
        verbose_name=_("occurred at"),
        help_text=_("When the event occurred (from provider)"),
    )

    class Meta:
        verbose_name = _("email event")
        verbose_name_plural = _("email events")
        ordering = ["-occurred_at"]
        indexes = [
            models.Index(fields=["email", "event_type"]),
            models.Index(fields=["event_type", "occurred_at"]),
        ]

    def __str__(self):
        return f"{self.get_event_type_display()} - {self.email.subject}"


class EmailDNSCheck(models.Model):
    """
    DNS validation check history for email accounts.
    Tracks SPF, DKIM, and DMARC validation results over time.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    account = models.ForeignKey(
        EmailAccount,
        on_delete=models.CASCADE,
        related_name="dns_checks",
        verbose_name=_("email account"),
        help_text=_("Email account being validated"),
    )

    domain = models.CharField(
        max_length=255, verbose_name=_("domain"), help_text=_("Domain being validated")
    )

    # SPF validation results
    spf_status = models.CharField(
        max_length=16,
        choices=[
            ("pass", _("Pass")),
            ("fail", _("Fail")),
            ("warn", _("Warning")),
            ("error", _("Error")),
        ],
        default="error",
        verbose_name=_("SPF status"),
    )

    spf_record = models.TextField(
        blank=True, verbose_name=_("SPF record"), help_text=_("SPF TXT record value found")
    )

    spf_errors = models.TextField(
        blank=True, verbose_name=_("SPF errors"), help_text=_("SPF validation error messages")
    )

    # DKIM validation results
    dkim_status = models.CharField(
        max_length=16,
        choices=[
            ("pass", _("Pass")),
            ("fail", _("Fail")),
            ("warn", _("Warning")),
            ("error", _("Error")),
        ],
        default="error",
        verbose_name=_("DKIM status"),
    )

    dkim_record = models.TextField(
        blank=True, verbose_name=_("DKIM record"), help_text=_("DKIM TXT record value found")
    )

    dkim_selector = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("DKIM selector"),
        help_text=_("DKIM selector used for validation"),
    )

    dkim_errors = models.TextField(
        blank=True, verbose_name=_("DKIM errors"), help_text=_("DKIM validation error messages")
    )

    # DMARC validation results
    dmarc_status = models.CharField(
        max_length=16,
        choices=[
            ("pass", _("Pass")),
            ("fail", _("Fail")),
            ("warn", _("Warning")),
            ("error", _("Error")),
        ],
        default="error",
        verbose_name=_("DMARC status"),
    )

    dmarc_record = models.TextField(
        blank=True, verbose_name=_("DMARC record"), help_text=_("DMARC TXT record value found")
    )

    dmarc_errors = models.TextField(
        blank=True, verbose_name=_("DMARC errors"), help_text=_("DMARC validation error messages")
    )

    # Propagation tracking
    resolvers_checked = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("resolvers checked"),
        help_text=_("DNS resolver results (e.g., {'8.8.8.8': 'success', '1.1.1.1': 'success'})"),
    )

    propagation_status = models.CharField(
        max_length=16,
        choices=[
            ("full", _("Fully Propagated")),
            ("partial", _("Partially Propagated")),
            ("none", _("Not Propagated")),
            ("error", _("Error")),
        ],
        default="error",
        verbose_name=_("propagation status"),
        help_text=_("DNS propagation status across multiple resolvers"),
    )

    # Overall validation result
    overall_status = models.CharField(
        max_length=16,
        choices=[
            ("pass", _("Pass")),
            ("warn", _("Warning")),
            ("fail", _("Fail")),
        ],
        default="fail",
        verbose_name=_("overall status"),
        help_text=_("Overall DNS validation status"),
    )

    # Metadata
    checked_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("checked at"),
        help_text=_("When this DNS check was performed"),
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    checked_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("checked by"),
        help_text=_("User who initiated this check"),
    )

    class Meta:
        verbose_name = _("DNS check")
        verbose_name_plural = _("DNS checks")
        ordering = ["-checked_at"]
        indexes = [
            models.Index(fields=["account", "-checked_at"]),
            models.Index(fields=["domain", "-checked_at"]),
            models.Index(fields=["overall_status"]),
        ]

    def __str__(self):
        return f"DNS Check for {self.domain} - {self.get_overall_status_display()} ({self.checked_at.strftime('%Y-%m-%d %H:%M')})"

    @property
    def is_valid(self) -> bool:
        """Check if DNS validation passed"""
        return self.overall_status == "pass"

    @property
    def has_warnings(self) -> bool:
        """Check if DNS validation has warnings"""
        return self.overall_status == "warn"


class EmailTemplateTranslation(models.Model):
    """
    Translations for email templates

    Stores translated versions of email templates in different languages.
    Integrates with translations app for AI-powered translation.
    """

    template = models.ForeignKey(
        "EmailTemplate",
        on_delete=models.CASCADE,
        related_name="translations",
        help_text=_("Template this translation belongs to"),
    )

    language_code = models.CharField(
        max_length=10,
        choices=[
            ("en", _("English")),
            ("es", _("Spanish")),
            ("fr", _("French")),
            ("de", _("German")),
            ("ja", _("Japanese")),
            ("pt", _("Portuguese")),
            ("zh-hans", _("Chinese (Simplified)")),
            ("ar", _("Arabic")),
            ("ru", _("Russian")),
        ],
        help_text=_("Language code (ISO 639-1)"),
    )

    subject = models.CharField(
        max_length=255,
        verbose_name=_("subject"),
        help_text=_("Translated email subject (template syntax)"),
    )

    html_content = models.TextField(
        verbose_name=_("HTML content"), help_text=_("Translated MJML/HTML template")
    )

    text_content = models.TextField(
        verbose_name=_("text content"), help_text=_("Translated plain text version")
    )

    translated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="translated_email_templates",
        help_text=_("User who created/verified this translation"),
    )

    translation_job = models.ForeignKey(
        "translations.TranslationJob",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="email_template_translations",
        help_text=_("AI translation job that created this translation"),
    )

    is_verified = models.BooleanField(
        default=False,
        verbose_name=_("verified"),
        help_text=_("Has this translation been manually verified?"),
    )

    quality_score = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_("quality score"),
        help_text=_("Translation quality score (0-1) from AI service"),
    )

    base_template_version = models.IntegerField(
        default=1,
        verbose_name=_("base template version"),
        help_text=_("Version of base template this translation was created from"),
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        db_table = "email_template_translations"
        verbose_name = _("email template translation")
        verbose_name_plural = _("email template translations")
        unique_together = [["template", "language_code"]]
        ordering = ["template", "language_code"]
        indexes = [
            models.Index(fields=["template", "language_code"]),
            models.Index(fields=["language_code"]),
        ]

    def __str__(self):
        return f"{self.template.template_type} - {self.get_language_code_display()}"

    def is_outdated(self):
        """Check if translation is outdated compared to base template"""
        return self.base_template_version < self.template.version

    def save(self, *args, **kwargs):
        """Validate MJML syntax before saving"""
        if self.html_content:
            from django.core.exceptions import ValidationError

            try:
                from mjml.mjml2html import mjml_to_html

                result = mjml_to_html(self.html_content)
                if result.get("errors"):
                    error_msgs = [
                        f"Line {e.get('line', '?')}: {e.get('message', 'Unknown error')}"
                        for e in result["errors"]
                    ]
                    raise ValidationError(
                        {"html_content": f"MJML validation errors: {'; '.join(error_msgs)}"}
                    )
            except ValidationError:
                raise
            except Exception as e:
                raise ValidationError({"html_content": f"Invalid MJML content: {e}"})
        super().save(*args, **kwargs)


class ScheduledEmail(models.Model):
    """Database-backed scheduled email for delayed sending.

    Reusable for any delayed email: onboarding tips, subscription reminders, etc.
    Processed by a Celery Beat task every 5 minutes.
    """

    STATUS_CHOICES = [
        ("pending", _("Pending")),
        ("sent", _("Sent")),
        ("cancelled", _("Cancelled")),
        ("failed", _("Failed")),
    ]

    template_type = models.CharField(
        max_length=100,
        verbose_name=_("template type"),
        help_text=_("EmailTemplate template_type to send"),
    )
    recipient_email = models.EmailField(
        verbose_name=_("recipient email"),
    )
    context_json = models.JSONField(
        default=dict,
        verbose_name=_("template context"),
        help_text=_("JSON context dict passed to EmailSendingService.send_template_email()"),
    )
    scheduled_for = models.DateTimeField(
        db_index=True,
        verbose_name=_("scheduled for"),
        help_text=_("When this email should be sent"),
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name=_("status"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name=_("sent at"))
    error_message = models.TextField(blank=True, verbose_name=_("error message"))

    class Meta:
        db_table = "email_scheduled"
        verbose_name = _("scheduled email")
        verbose_name_plural = _("scheduled emails")
        indexes = [
            models.Index(fields=["status", "scheduled_for"]),
        ]
        ordering = ["scheduled_for"]

    def __str__(self):
        return f"{self.template_type} → {self.recipient_email} ({self.get_status_display()})"
