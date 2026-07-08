import json
import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

User = get_user_model()


class TranslationProvider(models.Model):
    """Configuration for local/custom translation providers.

    External providers (DeepL, Google, Azure, AWS) are now managed as
    component-based TranslationProviderAccount instances linked to
    ComponentRegistry entries installed via the update server.
    """

    PROVIDER_TYPES = [
        ('local', _('Local AI (CTranslate2)')),
        ('custom', _('Custom API')),
    ]

    name = models.CharField(
        max_length=100,
        verbose_name=_('Provider Name'),
        help_text=_('Display name for this translation provider')
    )
    provider_type = models.CharField(
        max_length=20,
        choices=PROVIDER_TYPES,
        default='local',
        verbose_name=_('Provider Type')
    )
    api_endpoint = models.URLField(
        blank=True,
        null=True,
        verbose_name=_('API Endpoint'),
        help_text=_('API endpoint URL for external providers')
    )
    api_key = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name=_('API Key'),
        help_text=_('API key or authentication token')
    )
    api_secret = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name=_('API Secret'),
        help_text=_('Additional secret or password if required')
    )

    # Language mappings
    language_code_mapping = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_('Language Code Mapping'),
        help_text=_('Map internal language codes to provider-specific codes')
    )

    # Configuration
    max_chars_per_request = models.PositiveIntegerField(
        default=5000,
        verbose_name=_('Max Characters per Request'),
        help_text=_('Maximum number of characters per translation request')
    )
    rate_limit = models.PositiveIntegerField(
        default=100,
        verbose_name=_('Rate Limit'),
        help_text=_('Maximum requests per minute')
    )
    timeout_seconds = models.PositiveIntegerField(
        default=30,
        verbose_name=_('Timeout (seconds)'),
        help_text=_('Request timeout in seconds')
    )

    # Status
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Active'),
        help_text=_('Enable this translation provider')
    )
    is_default = models.BooleanField(
        default=False,
        verbose_name=_('Default Provider'),
        help_text=_('Use as default provider for translations')
    )
    priority = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Priority'),
        help_text=_('Higher priority providers are tried first')
    )

    # Metrics
    total_translations = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Total Translations')
    )
    total_characters = models.BigIntegerField(
        default=0,
        verbose_name=_('Total Characters Translated')
    )
    total_errors = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Total Errors')
    )
    last_used_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Last Used')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Translation Provider')
        verbose_name_plural = _('Translation Providers')
        ordering = ['-priority', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Ensure only one default provider
        if self.is_default:
            TranslationProvider.objects.filter(is_default=True).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)


class TranslationJob(models.Model):
    """Queue for translation jobs"""

    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('processing', _('Processing')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
        ('cancelled', _('Cancelled')),
    ]

    JOB_TYPES = [
        ('product', _('Product')),
        ('category', _('Category')),
        ('page', _('Page')),
        ('email', _('Email Template')),
        ('bulk', _('Bulk Translation')),
        ('custom', _('Custom')),
    ]

    # Job details
    job_type = models.CharField(
        max_length=20,
        choices=JOB_TYPES,
        default='custom',
        verbose_name=_('Job Type')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('Status')
    )
    priority = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Priority'),
        help_text=_('Higher priority jobs are processed first')
    )

    # Content
    source_language = models.CharField(
        max_length=10,
        verbose_name=_('Source Language')
    )
    target_languages = models.JSONField(
        default=list,
        verbose_name=_('Target Languages')
    )
    content_type = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_('Content Type'),
        help_text=_('Content type for the object being translated')
    )
    object_id = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_('Object ID')
    )
    fields_to_translate = models.JSONField(
        default=list,
        verbose_name=_('Fields to Translate')
    )

    # Provider (legacy — for local provider jobs)
    provider = models.ForeignKey(
        TranslationProvider,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Translation Provider'),
        related_name='jobs',
    )

    # External provider account (component-based providers)
    provider_account = models.ForeignKey(
        'TranslationProviderAccount',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Provider Account'),
        related_name='jobs',
    )

    # Metrics
    total_characters = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Total Characters')
    )
    translated_characters = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Translated Characters')
    )
    progress = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Progress (%)')
    )

    # Timing
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    # User tracking
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_translation_jobs',
        verbose_name=_('Created By')
    )

    # Error handling
    error_message = models.TextField(
        blank=True,
        verbose_name=_('Error Message')
    )
    retry_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Retry Count')
    )
    max_retries = models.PositiveIntegerField(
        default=3,
        verbose_name=_('Max Retries')
    )

    # Translation results
    translated_data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_('Translated Data'),
        help_text=_('Stores the completed translations for each language')
    )

    class Meta:
        verbose_name = _('Translation Job')
        verbose_name_plural = _('Translation Jobs')
        ordering = ['-priority', '-created_at']
        indexes = [
            models.Index(fields=['status', 'priority']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.get_job_type_display()} - {self.get_status_display()}"

    def mark_processing(self):
        self.status = 'processing'
        self.started_at = timezone.now()
        self.save()

    def mark_completed(self):
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.progress = 100
        self.save()

    def mark_failed(self, error_message):
        self.status = 'failed'
        self.error_message = error_message
        self.save()


class TranslationMeta(models.Model):
    """Metadata for translated content"""

    content_type = models.CharField(
        max_length=100,
        verbose_name=_('Content Type')
    )
    object_id = models.PositiveIntegerField(
        verbose_name=_('Object ID')
    )
    field_name = models.CharField(
        max_length=100,
        verbose_name=_('Field Name')
    )
    language = models.CharField(
        max_length=10,
        verbose_name=_('Language')
    )

    # Locking
    is_locked = models.BooleanField(
        default=False,
        verbose_name=_('Locked'),
        help_text=_('Prevent automatic translation of this field')
    )
    locked_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='locked_translations',
        verbose_name=_('Locked By')
    )
    locked_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Locked At')
    )

    # Translation info
    source_checksum = models.CharField(
        max_length=64,
        blank=True,
        verbose_name=_('Source Checksum'),
        help_text=_('MD5 hash of source content')
    )
    translation_provider = models.ForeignKey(
        TranslationProvider,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Translation Provider')
    )
    translated_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Translated At')
    )
    translated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='performed_translations',
        verbose_name=_('Translated By')
    )

    # Quality
    confidence_score = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        verbose_name=_('Confidence Score')
    )
    is_reviewed = models.BooleanField(
        default=False,
        verbose_name=_('Reviewed'),
        help_text=_('Has been reviewed by a human')
    )
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_translations',
        verbose_name=_('Reviewed By')
    )
    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Reviewed At')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Translation Metadata')
        verbose_name_plural = _('Translation Metadata')
        unique_together = [['content_type', 'object_id', 'field_name', 'language']]
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['language']),
            models.Index(fields=['is_locked']),
        ]

    def __str__(self):
        return f"{self.content_type} #{self.object_id} - {self.field_name} ({self.language})"


class SiteLanguage(models.Model):
    """Language configuration for the site"""

    SUPPORT_LEVELS = [
        ('full', _('Full Support')),
        ('limited', _('Limited Support')),
        ('external', _('External Provider Recommended')),
        ('none', _('Not Supported')),
    ]

    # Basic info
    code = models.CharField(
        max_length=10,
        unique=True,
        verbose_name=_('Language Code'),
        help_text=_('ISO language code (e.g., en, es, zh-CN)')
    )
    name = models.CharField(
        max_length=100,
        verbose_name=_('English Name'),
        help_text=_('Language name in English')
    )
    native_name = models.CharField(
        max_length=100,
        verbose_name=_('Native Name'),
        help_text=_('Language name in its own language')
    )

    # Configuration
    is_active = models.BooleanField(
        default=False,
        verbose_name=_('Active'),
        help_text=_('Enable this language for site translations')
    )
    is_default = models.BooleanField(
        default=False,
        verbose_name=_('Default Language'),
        help_text=_('Primary language for the site')
    )

    # Model support
    m2m100_support = models.CharField(
        max_length=10,
        choices=SUPPORT_LEVELS,
        default='none',
        verbose_name=_('M2M100 Support'),
        help_text=_('Support level in M2M100 models')
    )
    nllb_support = models.CharField(
        max_length=10,
        choices=SUPPORT_LEVELS,
        default='none',
        verbose_name=_('NLLB Support'),
        help_text=_('Support level in NLLB models')
    )
    requires_nllb = models.BooleanField(
        default=False,
        verbose_name=_('Requires NLLB'),
        help_text=_('This language requires NLLB model installation')
    )

    # Ordering
    order = models.IntegerField(
        default=0,
        verbose_name=_('Display Order'),
        help_text=_('Order in language selector')
    )

    # Metadata
    rtl = models.BooleanField(
        default=False,
        verbose_name=_('Right-to-Left'),
        help_text=_('Text direction for this language')
    )
    flag = models.CharField(
        max_length=10,
        blank=True,
        verbose_name=_('Flag Emoji'),
        help_text=_('Country flag emoji for this language')
    )
    date_format = models.CharField(
        max_length=50,
        default='Y-m-d',
        verbose_name=_('Date Format'),
        help_text=_('PHP date format string')
    )
    time_format = models.CharField(
        max_length=50,
        default='H:i:s',
        verbose_name=_('Time Format'),
        help_text=_('PHP time format string')
    )

    # Statistics
    total_translations = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Total Translations')
    )
    last_used = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Last Used')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Site Language')
        verbose_name_plural = _('Site Languages')
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.native_name} ({self.code})"

    def save(self, *args, **kwargs):
        # Ensure only one default language
        if self.is_default:
            SiteLanguage.objects.filter(is_default=True).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)

    def get_flag_emoji(self):
        """Get flag emoji or fallback to language code"""
        return self.flag or f"[{self.code.upper()}]"

    def get_support_indicator(self):
        """Get visual indicator for support level"""
        indicators = {
            'full': '🟢',
            'limited': '🟡',
            'external': '🔵',
            'none': '🔴'
        }
        return indicators.get(self.m2m100_support, '⚪')


class InstalledModel(models.Model):
    """Registry of installed translation models"""

    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name=_('Model Name')
    )
    version = models.CharField(
        max_length=50,
        verbose_name=_('Version')
    )
    model_type = models.CharField(
        max_length=50,
        default='m2m100',
        verbose_name=_('Model Type')
    )

    # Language support
    languages = models.PositiveIntegerField(
        default=100,
        verbose_name=_('Number of Languages'),
        help_text=_('Number of languages supported by this model')
    )
    source_languages = models.JSONField(
        default=list,
        verbose_name=_('Source Languages')
    )
    target_languages = models.JSONField(
        default=list,
        verbose_name=_('Target Languages')
    )

    # Storage
    file_path = models.CharField(
        max_length=500,
        verbose_name=_('File Path')
    )
    size_mb = models.FloatField(
        verbose_name=_('Size (MB)')
    )

    # Performance
    compute_type = models.CharField(
        max_length=20,
        default='int8',
        verbose_name=_('Compute Type'),
        help_text=_('int8, int16, float16, float32')
    )
    device = models.CharField(
        max_length=20,
        default='cpu',
        verbose_name=_('Device'),
        help_text=_('cpu or cuda')
    )

    # Status
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Active')
    )
    is_downloaded = models.BooleanField(
        default=False,
        verbose_name=_('Downloaded')
    )
    is_default = models.BooleanField(
        default=False,
        verbose_name=_('Default Model'),
        help_text=_('This model is used for translations')
    )
    download_progress = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Download Progress (%)')
    )

    # Metrics
    total_translations = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Total Translations')
    )
    avg_latency_ms = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Average Latency (ms)')
    )

    installed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _('Installed Model')
        verbose_name_plural = _('Installed Models')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} v{self.version}"


class UITranslationOverride(models.Model):
    """
    Merchant overrides for frontend UI strings.

    One row per language. The overrides JSONField stores a flat dictionary
    of string_key -> translated_value. Keys come from the UI string registry.

    Structure of overrides field:
    {
        "cart.shopping_cart": "장바구니",
        "checkout.place_order": "주문하기",
        ...
    }

    Structure of meta_info field:
    {
        "cart.shopping_cart": {"auto": true, "verified": false, "translated_at": "..."},
        ...
    }
    """
    language = models.OneToOneField(
        SiteLanguage,
        on_delete=models.CASCADE,
        related_name='ui_overrides',
        verbose_name=_('Language'),
    )
    overrides = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_('UI String Overrides'),
        help_text=_('Merchant translations for frontend UI strings'),
    )
    meta_info = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_('Translation Metadata'),
        help_text=_('Per-string metadata: auto-translated, verified, timestamp'),
    )
    total_strings = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Total Strings'),
    )
    translated_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Translated Count'),
    )
    verified_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Verified Count'),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_auto_translated_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Last Auto-Translated'),
    )

    class Meta:
        verbose_name = _('UI Translation Override')
        verbose_name_plural = _('UI Translation Overrides')

    def __str__(self):
        return f"UI Translations ({self.language.code}) - {self.translated_count}/{self.total_strings}"

    @property
    def completion_percentage(self):
        if self.total_strings == 0:
            return 0
        return round((self.translated_count / self.total_strings) * 100, 1)


class TranslationProviderAccount(models.Model):
    """
    External translation provider account (DeepL, Google, Azure, AWS).

    Linked to a ComponentRegistry entry for the installed provider component.
    Stores encrypted credentials and configuration — follows the same pattern
    as PaymentProviderAccount and shipping ProviderAccount.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Link to ComponentRegistry (translation_provider type)
    component = models.ForeignKey(
        'component_updates.ComponentRegistry',
        on_delete=models.CASCADE,
        limit_choices_to={'component_type': 'translation_provider'},
        related_name='translation_provider_accounts',
        verbose_name=_('component'),
        help_text=_('Installed translation provider component')
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='translation_providers',
        verbose_name=_('user'),
        help_text=_('User who configured this provider account')
    )

    display_name = models.CharField(
        max_length=128,
        blank=True,
        verbose_name=_('display name'),
        help_text=_('Friendly name for this connection (e.g., "My DeepL Account")')
    )

    # Encrypted credentials (API keys, secrets, tokens)
    credentials_encrypted = models.JSONField(
        default=dict,
        verbose_name=_('credentials'),
        help_text=_('Encrypted API credentials (never stored in plain text)')
    )

    # Provider-specific settings
    settings = models.JSONField(
        default=dict,
        verbose_name=_('settings'),
        help_text=_('Provider-specific configuration (rate limits, timeouts, language mappings)')
    )

    # Signup affiliate link (optional)
    signup_url = models.URLField(
        blank=True,
        verbose_name=_('signup URL'),
        help_text=_('Link for merchants to create a provider account')
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_('is active'),
        help_text=_('Whether this provider is active for translations')
    )

    is_default = models.BooleanField(
        default=False,
        verbose_name=_('is default'),
        help_text=_('Use this provider as default for external translations')
    )

    priority = models.PositiveIntegerField(
        default=0,
        verbose_name=_('priority'),
        help_text=_('Higher priority providers are tried first (0 = lowest)')
    )

    # Connection health
    last_tested_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('last tested at'),
        help_text=_('Last successful connection test')
    )

    connection_status = models.CharField(
        max_length=20,
        choices=[
            ('unknown', _('Unknown')),
            ('connected', _('Connected')),
            ('error', _('Connection Error')),
        ],
        default='unknown',
        verbose_name=_('connection status')
    )

    connection_error = models.TextField(
        blank=True,
        verbose_name=_('connection error'),
        help_text=_('Last connection error message')
    )

    # Metrics
    total_translations = models.PositiveIntegerField(
        default=0,
        verbose_name=_('total translations')
    )
    total_characters = models.BigIntegerField(
        default=0,
        verbose_name=_('total characters translated')
    )
    total_errors = models.PositiveIntegerField(
        default=0,
        verbose_name=_('total errors')
    )
    last_used_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('last used')
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

    class Meta:
        ordering = ['-priority', 'display_name']
        verbose_name = _('Translation Provider Account')
        verbose_name_plural = _('Translation Provider Accounts')
        indexes = [
            models.Index(fields=['is_active', 'priority']),
        ]

    def __str__(self):
        return self.display_name or f"{self.component.name} Account"

    def save(self, *args, **kwargs):
        # Ensure only one default provider account
        if self.is_default:
            TranslationProviderAccount.objects.filter(
                is_default=True
            ).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)

    def get_provider_instance(self):
        """
        Get an instantiated provider class with decrypted credentials.

        Returns:
            TranslationProviderBase instance ready for translation
        """
        from translations.providers.registry import ProviderRegistry
        from translations.utils.encryption import decrypt_credentials

        provider_class = ProviderRegistry.get_provider(self.component.slug)
        if not provider_class:
            raise ValueError(f"Provider '{self.component.slug}' not found in registry")

        credentials = decrypt_credentials(self.credentials_encrypted)
        return provider_class(credentials=credentials, config=self.settings)
