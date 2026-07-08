"""
MigrationLog Model
Detailed logs for each imported item and migration events.
Used for debugging, audit trail, and progress display.
"""
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _


class MigrationLog(models.Model):
    """
    Detailed logs for each imported item.
    Used for debugging, audit trail, and real-time progress display.
    """
    job = models.ForeignKey(
        'migration.MigrationJob',
        on_delete=models.CASCADE,
        related_name='logs',
        db_index=True,
        help_text=_("Parent migration job")
    )

    step = models.ForeignKey(
        'migration.MigrationStep',
        on_delete=models.CASCADE,
        related_name='logs',
        null=True,
        blank=True,
        help_text=_("Migration step this log belongs to")
    )

    timestamp = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text=_("When this log entry was created")
    )

    LEVEL_CHOICES = [
        ('debug', _('Debug')),
        ('info', _('Info')),
        ('warning', _('Warning')),
        ('error', _('Error')),
        ('critical', _('Critical')),
    ]
    level = models.CharField(
        max_length=10,
        choices=LEVEL_CHOICES,
        db_index=True,
        help_text=_("Log severity level")
    )

    message = models.TextField(
        help_text=_("Log message")
    )

    # Reference to source item (WooCommerce, Shopify, etc.)
    source_type = models.CharField(
        max_length=50,
        blank=True,
        help_text=_("Source data type (e.g., 'woocommerce_product')")
    )
    source_id = models.CharField(
        max_length=100,
        blank=True,
        db_index=True,
        help_text=_("ID from source system")
    )
    source_name = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("Name/title of source item")
    )

    # Reference to created/modified item in our platform
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text=_("Type of created object")
    )
    object_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text=_("ID of created object")
    )
    content_object = GenericForeignKey('content_type', 'object_id')

    # Additional context (JSON for structured data)
    context = models.JSONField(
        default=dict,
        blank=True,
        help_text=_("Additional context data")
    )

    # Action taken
    ACTION_CHOICES = [
        ('fetch', _('Fetched')),
        ('validate', _('Validated')),
        ('map', _('Mapped')),
        ('create', _('Created')),
        ('update', _('Updated')),
        ('skip', _('Skipped')),
        ('error', _('Error')),
    ]
    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES,
        blank=True,
        help_text=_("Action performed")
    )

    class Meta:
        ordering = ['timestamp']
        verbose_name = _('Migration Log')
        verbose_name_plural = _('Migration Logs')
        indexes = [
            models.Index(fields=['job', 'timestamp']),
            models.Index(fields=['job', 'level']),
            models.Index(fields=['step', 'timestamp']),
            models.Index(fields=['level', 'timestamp']),
            models.Index(fields=['source_type', 'source_id']),
        ]

    def __str__(self):
        return f"{self.timestamp.strftime('%H:%M:%S')} [{self.level.upper()}] {self.message[:50]}"

    @classmethod
    def log_info(cls, job, message, step=None, source_type=None, source_id=None, **context):
        """Helper to log info message"""
        return cls.objects.create(
            job=job,
            step=step,
            level='info',
            message=message,
            source_type=source_type or '',
            source_id=source_id or '',
            context=context,
            action='info'
        )

    @classmethod
    def log_warning(cls, job, message, step=None, source_type=None, source_id=None, **context):
        """Helper to log warning message"""
        if step:
            step.warning_count += 1
            step.save(update_fields=['warning_count'])

        return cls.objects.create(
            job=job,
            step=step,
            level='warning',
            message=message,
            source_type=source_type or '',
            source_id=source_id or '',
            context=context,
            action='warning'
        )

    @classmethod
    def log_error(cls, job, message, step=None, source_type=None, source_id=None, error=None, **context):
        """Helper to log error message"""
        if step:
            step.error_count += 1
            step.save(update_fields=['error_count'])

        if error:
            context['error_type'] = type(error).__name__
            context['error_details'] = str(error)

        return cls.objects.create(
            job=job,
            step=step,
            level='error',
            message=message,
            source_type=source_type or '',
            source_id=source_id or '',
            context=context,
            action='error'
        )

    @classmethod
    def log_create(cls, job, message, step=None, source_type=None, source_id=None,
                   source_name=None, created_object=None, **context):
        """Helper to log successful creation"""
        log = cls.objects.create(
            job=job,
            step=step,
            level='info',
            message=message,
            source_type=source_type or '',
            source_id=source_id or '',
            source_name=source_name or '',
            context=context,
            action='create'
        )

        if created_object:
            log.content_object = created_object
            log.save()

        return log

    @classmethod
    def log_skip(cls, job, message, step=None, source_type=None, source_id=None,
                 source_name=None, reason=None, **context):
        """Helper to log skipped item"""
        if reason:
            context['skip_reason'] = reason

        return cls.objects.create(
            job=job,
            step=step,
            level='warning',
            message=message,
            source_type=source_type or '',
            source_id=source_id or '',
            source_name=source_name or '',
            context=context,
            action='skip'
        )

    @classmethod
    def get_recent_logs(cls, job, limit=50):
        """Get recent logs for a job (for live display)"""
        return cls.objects.filter(job=job).order_by('-timestamp')[:limit]

    @classmethod
    def get_error_logs(cls, job):
        """Get all error logs for a job"""
        return cls.objects.filter(job=job, level='error').order_by('-timestamp')

    @classmethod
    def get_logs_by_step(cls, step):
        """Get all logs for a specific step"""
        return cls.objects.filter(step=step).order_by('timestamp')
