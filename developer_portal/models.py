"""
Developer Portal Models
Manages developer accounts, component submissions, and review workflow.
Only active when SPWIG_IS_HQ=true (spwig.com backend).
"""

import uuid
import hashlib

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.utils.crypto import get_random_string
from django_countries.fields import CountryField


def generate_api_key():
    """Generate a random API key for developers."""
    return f"dev_{get_random_string(48)}"


class DeveloperProfile(models.Model):
    """
    Developer account linked to a spwig.com user.
    Follows the same pattern as affiliate/models.py Affiliate model.
    """

    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending Review')
        APPROVED = 'approved', _('Approved')
        SUSPENDED = 'suspended', _('Suspended')
        REJECTED = 'rejected', _('Rejected')

    class PayoutMethod(models.TextChoices):
        AIRWALLEX = 'airwallex', _('Bank Transfer (Airwallex)')
        PAYPAL = 'paypal', _('PayPal')

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='developer_profile',
    )

    # Developer identification
    developer_slug = models.SlugField(
        max_length=100,
        unique=True,
        help_text=_('Unique identifier for your developer profile (used in URLs)'),
    )
    display_name = models.CharField(
        max_length=200,
        help_text=_('Public display name for your developer profile'),
    )
    bio = models.TextField(
        blank=True,
        help_text=_('Short description about you or your company'),
    )
    website = models.URLField(
        blank=True,
        help_text=_('Your website or portfolio URL'),
    )
    company_name = models.CharField(
        max_length=200,
        blank=True,
        help_text=_('Company or organization name'),
    )
    country = CountryField(
        blank=True,
        help_text=_('Country of residence or business'),
    )
    logo = models.ForeignKey(
        'media_library.MediaAsset',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_('Developer logo or avatar'),
    )

    # Status
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )
    rejection_reason = models.TextField(
        blank=True,
        help_text=_('Reason for rejection (visible to developer)'),
    )

    # Upgrade server link
    upgrade_server_author_slug = models.CharField(
        max_length=200,
        blank=True,
        help_text=_('Slug of the Author record on the upgrade server'),
    )
    logo_url = models.CharField(
        max_length=500,
        blank=True,
        default='',
        help_text=_('Logo URL from upgrade server (used when no local logo uploaded)'),
    )

    # API access
    api_key = models.CharField(
        max_length=64,
        default=generate_api_key,
        unique=True,
        help_text=_('API key for programmatic submissions'),
    )

    # Agreement
    terms_accepted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    # Payout settings (Phase 3)
    payout_method = models.CharField(
        max_length=20,
        choices=PayoutMethod.choices,
        blank=True,
        help_text=_('Preferred payout method'),
    )
    payout_details = models.JSONField(
        default=dict,
        blank=True,
        help_text=_('Bank details (Airwallex) or PayPal email'),
    )

    # Notification preferences
    review_notification_preference = models.CharField(
        max_length=20,
        choices=[
            ('immediate', _('Immediately')),
            ('daily', _('Daily digest')),
            ('weekly', _('Weekly digest')),
            ('none', _('No notifications')),
        ],
        default='immediate',
        help_text=_('How often to receive review notifications'),
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _('Developer Profile')
        verbose_name_plural = _('Developer Profiles')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.display_name} ({self.developer_slug})"

    @property
    def is_approved(self):
        return self.status == self.Status.APPROVED

    def approve(self):
        """Approve this developer."""
        self.status = self.Status.APPROVED
        self.approved_at = timezone.now()
        self.save(update_fields=['status', 'approved_at', 'updated_at'])

    def reject(self, reason=''):
        """Reject this developer application."""
        self.status = self.Status.REJECTED
        self.rejection_reason = reason
        self.save(update_fields=['status', 'rejection_reason', 'updated_at'])

    def suspend(self, reason=''):
        """Suspend this developer."""
        self.status = self.Status.SUSPENDED
        self.rejection_reason = reason
        self.save(update_fields=['status', 'rejection_reason', 'updated_at'])

    def regenerate_api_key(self):
        """Generate a new API key."""
        self.api_key = generate_api_key()
        self.save(update_fields=['api_key', 'updated_at'])
        return self.api_key

    @property
    def has_free_license(self):
        """Whether this developer has already claimed their free license."""
        return self.license_requests.filter(
            is_free=True,
            status__in=[
                DeveloperLicenseRequest.Status.PENDING,
                DeveloperLicenseRequest.Status.APPROVED,
            ],
        ).exists()

    @property
    def approved_licenses_count(self):
        """Count of approved licenses."""
        return self.license_requests.filter(
            status=DeveloperLicenseRequest.Status.APPROVED,
        ).count()


class ComponentSubmission(models.Model):
    """
    Component submission for review and publication.
    Tracks the full lifecycle from upload to publication on the upgrade server.
    Supports any component type (theme, widget, provider, etc.).
    """

    class ValidationStatus(models.TextChoices):
        PENDING = 'pending', _('Pending Validation')
        VALIDATING = 'validating', _('Validating')
        PASSED = 'passed', _('Validation Passed')
        FAILED = 'failed', _('Validation Failed')

    class ReviewStatus(models.TextChoices):
        PENDING = 'pending', _('Pending Review')
        IN_REVIEW = 'in_review', _('In Review')
        APPROVED = 'approved', _('Approved')
        REJECTED = 'rejected', _('Rejected')
        REVISION_REQUESTED = 'revision_requested', _('Revision Requested')

    class PricingModel(models.TextChoices):
        FREE = 'free', _('Free')
        PAID = 'paid', _('Paid')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    developer = models.ForeignKey(
        DeveloperProfile,
        on_delete=models.CASCADE,
        related_name='submissions',
    )

    # Component identification
    component_type = models.CharField(
        max_length=50,
        default='theme',
        db_index=True,
        help_text=_('Component type slug (e.g. theme, widget, payment_provider)'),
    )
    component_slug = models.SlugField(
        max_length=200,
        help_text=_('Component identifier slug (from manifest)'),
    )
    component_name = models.CharField(
        max_length=200,
        help_text=_('Display name of the component'),
    )
    version = models.CharField(
        max_length=20,
        help_text=_('Semantic version (e.g., 1.0.0)'),
    )
    description = models.TextField(
        blank=True,
        help_text=_('Description for marketplace listing'),
    )
    changelog = models.TextField(
        blank=True,
        help_text=_('What changed in this version'),
    )

    # Package
    package_file = models.FileField(
        upload_to='developer/submissions/%Y/%m/',
        help_text=_('Component ZIP package'),
    )
    package_checksum = models.CharField(
        max_length=64,
        blank=True,
        help_text=_('SHA-256 checksum of the package file'),
    )
    package_size_bytes = models.BigIntegerField(default=0)
    manifest_data = models.JSONField(
        default=dict,
        blank=True,
        help_text=_('Extracted manifest.json content'),
    )

    # Visual assets
    thumbnail = models.ForeignKey(
        'media_library.MediaAsset',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_('Thumbnail image for marketplace listing'),
    )
    preview_images = models.ManyToManyField(
        'media_library.MediaAsset',
        blank=True,
        related_name='+',
        help_text=_('Screenshots and preview images'),
    )

    # Validation
    validation_status = models.CharField(
        max_length=20,
        choices=ValidationStatus.choices,
        default=ValidationStatus.PENDING,
        db_index=True,
    )
    validation_results = models.JSONField(
        default=dict,
        blank=True,
        help_text=_('Detailed validation output'),
    )
    validated_at = models.DateTimeField(null=True, blank=True)

    # Review
    review_status = models.CharField(
        max_length=20,
        choices=ReviewStatus.choices,
        default=ReviewStatus.PENDING,
        db_index=True,
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    review_notes = models.TextField(
        blank=True,
        help_text=_('Notes from the reviewer (visible to developer)'),
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)

    # Publication
    is_published = models.BooleanField(default=False, db_index=True)
    published_at = models.DateTimeField(null=True, blank=True)
    upgrade_server_component_slug = models.CharField(
        max_length=200,
        blank=True,
        help_text=_('Component slug on the upgrade server'),
    )
    upgrade_server_version_id = models.IntegerField(
        null=True,
        blank=True,
        help_text=_('ComponentVersion ID on the upgrade server'),
    )

    # Pricing
    pricing_model = models.CharField(
        max_length=10,
        choices=PricingModel.choices,
        default=PricingModel.FREE,
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text=_('Base price in EUR (0 for free components). Marketplace prices in other currencies are derived from exchange rates.'),
    )
    currency = models.CharField(max_length=3, default='EUR')

    # Timestamps
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Component Submission')
        verbose_name_plural = _('Component Submissions')
        ordering = ['-submitted_at']
        unique_together = [('component_slug', 'version', 'component_type')]

    def __str__(self):
        return f"{self.component_name} v{self.version} ({self.get_component_type_display()})"

    def get_component_type_display(self):
        """Dynamic display name from upgrade server types."""
        from .services.component_types import get_type_display
        return get_type_display(self.component_type)

    @property
    def type_display(self):
        return self.get_component_type_display()

    @property
    def type_icon(self):
        """Dynamic icon from upgrade server component types."""
        from .services.component_types import get_type_icon
        return get_type_icon(self.component_type)

    def calculate_checksum(self):
        """Calculate SHA-256 checksum of the package file."""
        if not self.package_file:
            return ''
        sha256 = hashlib.sha256()
        self.package_file.seek(0)
        for chunk in self.package_file.chunks():
            sha256.update(chunk)
        self.package_file.seek(0)
        return sha256.hexdigest()

    @property
    def is_free(self):
        return self.pricing_model == self.PricingModel.FREE

    @property
    def can_resubmit(self):
        """Whether the developer can submit a new version."""
        return self.review_status in (
            self.ReviewStatus.REJECTED,
            self.ReviewStatus.REVISION_REQUESTED,
        )

    @property
    def is_pending_review(self):
        return (
            self.validation_status == self.ValidationStatus.PASSED
            and self.review_status == self.ReviewStatus.PENDING
        )


class SubmissionReview(models.Model):
    """
    Individual review action on a submission.
    Provides an audit trail of the review process.
    """

    class Action(models.TextChoices):
        COMMENT = 'comment', _('Comment')
        APPROVE = 'approve', _('Approved')
        REJECT = 'reject', _('Rejected')
        REQUEST_REVISION = 'request_revision', _('Revision Requested')
        VALIDATION_PASSED = 'validation_passed', _('Automated Validation Passed')
        VALIDATION_FAILED = 'validation_failed', _('Automated Validation Failed')

    submission = models.ForeignKey(
        ComponentSubmission,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    action = models.CharField(
        max_length=20,
        choices=Action.choices,
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Submission Review')
        verbose_name_plural = _('Submission Reviews')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_action_display()} by {self.reviewer} on {self.submission}"


# ============================================
# Analytics & Review Mirror Models
# ============================================

class ComponentAnalytics(models.Model):
    """
    Local cache of per-component download analytics from the upgrade server.
    Synced periodically by Celery Beat task.
    """
    developer = models.ForeignKey(
        DeveloperProfile,
        on_delete=models.CASCADE,
        related_name='component_analytics',
    )
    component_slug = models.CharField(max_length=200, db_index=True)
    component_name = models.CharField(max_length=200)
    current_version = models.CharField(max_length=20, blank=True)
    is_published = models.BooleanField(default=True)

    # Component metadata (synced from upgrade server marketplace)
    component_type = models.CharField(max_length=50, blank=True, default='')
    description = models.TextField(blank=True, default='')
    thumbnail_url = models.URLField(max_length=500, blank=True, default='')
    pricing_model = models.CharField(max_length=10, blank=True, default='free')
    price_eur = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Download stats
    downloads_total = models.PositiveIntegerField(default=0)
    downloads_period = models.PositiveIntegerField(
        default=0,
        help_text=_('Downloads in the last N days (see period_days)'),
    )
    period_days = models.PositiveIntegerField(default=30)
    versions_count = models.PositiveIntegerField(default=0)

    # Rating stats (denormalized from upgrade server)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    rating_count = models.PositiveIntegerField(default=0)

    # Sync metadata
    last_synced_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Component Analytics')
        verbose_name_plural = _('Component Analytics')
        unique_together = [('developer', 'component_slug')]
        ordering = ['-downloads_total']

    def __str__(self):
        return f"{self.component_name} ({self.downloads_total} downloads)"


class DailyDownloadStat(models.Model):
    """
    Daily download trend data for chart rendering.
    Stores date-based download counts per developer (aggregate across components).
    """
    developer = models.ForeignKey(
        DeveloperProfile,
        on_delete=models.CASCADE,
        related_name='daily_download_stats',
    )
    date = models.DateField(db_index=True)
    downloads = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _('Daily Download Stat')
        verbose_name_plural = _('Daily Download Stats')
        unique_together = [('developer', 'date')]
        ordering = ['date']

    def __str__(self):
        return f"{self.developer.developer_slug} - {self.date}: {self.downloads}"


class ComponentReviewMirror(models.Model):
    """
    Local mirror of merchant reviews from the upgrade server.
    Includes developer response fields managed locally and synced to upgrade server.
    """
    developer = models.ForeignKey(
        DeveloperProfile,
        on_delete=models.CASCADE,
        related_name='component_reviews',
    )
    component_slug = models.CharField(max_length=200, db_index=True)
    component_name = models.CharField(max_length=200, blank=True)

    # Review data (from upgrade server)
    upgrade_server_review_id = models.PositiveIntegerField(
        db_index=True,
        help_text=_('ID of the ComponentReview on the upgrade server'),
    )
    rating = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=200, blank=True)
    comment = models.TextField(blank=True)
    author_name = models.CharField(max_length=100)
    is_verified_purchase = models.BooleanField(default=False)
    review_created_at = models.DateTimeField()

    # Developer response (written locally, synced to upgrade server)
    developer_response = models.TextField(blank=True)
    developer_response_at = models.DateTimeField(null=True, blank=True)
    response_synced = models.BooleanField(
        default=True,
        help_text=_('Whether the response has been synced to the upgrade server'),
    )

    # Read tracking
    is_read = models.BooleanField(
        default=False,
        help_text=_('Whether the developer has seen this review'),
    )

    # Email notification tracking
    notification_sent_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_('When the notification email was sent for this review'),
    )

    # Sync metadata
    last_synced_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Component Review')
        verbose_name_plural = _('Component Reviews')
        unique_together = [('developer', 'upgrade_server_review_id')]
        ordering = ['-review_created_at']

    def __str__(self):
        return f"{self.author_name}: {self.rating}/5 on {self.component_name}"


class ComponentVersionMirror(models.Model):
    """
    Local mirror of component version history from the upgrade server.
    Provides historical version information for the developer console.
    """
    developer = models.ForeignKey(
        DeveloperProfile,
        on_delete=models.CASCADE,
        related_name='component_versions',
    )
    component_slug = models.CharField(max_length=200, db_index=True)
    version = models.CharField(max_length=20)
    channel = models.CharField(max_length=20, default='stable')
    changelog = models.TextField(blank=True, default='')
    published_at = models.DateTimeField(null=True, blank=True)
    package_size_bytes = models.BigIntegerField(default=0)
    breaking_changes = models.BooleanField(default=False)
    security_update = models.BooleanField(default=False)

    # Sync metadata
    last_synced_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Component Version')
        verbose_name_plural = _('Component Versions')
        unique_together = [('developer', 'component_slug', 'version')]
        ordering = ['-published_at']

    def __str__(self):
        return f"{self.component_slug} v{self.version} ({self.channel})"


class DeveloperLicenseRequest(models.Model):
    """
    Developer license record. Free first license is auto-provisioned via the
    update server; additional licenses cost EUR 100 via Airwallex checkout.
    """

    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        APPROVED = 'approved', _('Approved')
        REJECTED = 'rejected', _('Rejected')

    class LicenseType(models.TextChoices):
        SHOP = 'shop', _('Spwig Shop')
        POS = 'pos', _('Spwig POS')
        BOTH = 'both', _('Shop + POS')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    developer = models.ForeignKey(
        DeveloperProfile,
        on_delete=models.CASCADE,
        related_name='license_requests',
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )
    license_type = models.CharField(
        max_length=20,
        choices=LicenseType.choices,
        default=LicenseType.BOTH,
        help_text=_('Which products this license covers'),
    )
    reason = models.TextField(
        blank=True,
        default='',
        help_text=_('Why do you need a development license?'),
    )
    admin_notes = models.TextField(
        blank=True,
        help_text=_('Internal notes (shown to developer on rejection)'),
    )
    is_free = models.BooleanField(
        default=False,
        help_text=_('Whether this is the free developer license'),
    )

    # Populated on approval
    order = models.ForeignKey(
        'orders.Order',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_('Auto-generated order for the dev license product'),
    )
    license_key = models.CharField(
        max_length=64,
        blank=True,
        help_text=_('License key from the update server'),
    )
    license_expires_at = models.DateTimeField(null=True, blank=True)

    # Setup token for installation activation
    setup_token = models.TextField(
        blank=True,
        help_text=_('JWT setup token for installation activation (from update server)'),
    )
    setup_token_expires_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_('When the setup token expires'),
    )
    setup_token_id = models.UUIDField(
        null=True,
        blank=True,
        help_text=_('Setup token UUID on the update server (needed for regeneration)'),
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _('Developer License')
        verbose_name_plural = _('Developer Licenses')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.developer.display_name} - {self.get_license_type_display()} ({self.get_status_display()})"

    @property
    def is_token_expired(self):
        """Whether the setup token has expired."""
        if not self.setup_token_expires_at:
            return not bool(self.setup_token)
        return timezone.now() > self.setup_token_expires_at
