"""
SyncStep Model
Tracks individual steps within a sync job.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class SyncStep(models.Model):
    """
    Individual step within a sync job (one per category).
    Mirrors MigrationStep pattern.
    """
    job = models.ForeignKey(
        'migration.SyncJob',
        on_delete=models.CASCADE,
        related_name='steps',
        help_text=_("Parent sync job")
    )

    # Category key from the sync category registry
    category = models.CharField(
        max_length=50,
        help_text=_("Sync category key (e.g., 'email_config', 'design_theme')")
    )

    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('running', _('Running')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
        ('skipped', _('Skipped')),
        ('rolled_back', _('Rolled Back')),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    items_total = models.IntegerField(default=0)
    items_synced = models.IntegerField(default=0)
    items_skipped = models.IntegerField(default=0)
    items_failed = models.IntegerField(default=0)

    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)

    # Per-step diff data and ID mappings (for rollback and relational integrity)
    diff_data = models.JSONField(
        default=dict,
        blank=True,
        help_text=_("Diff data, created object IDs, or ID mappings for this step")
    )

    # Category-specific progress info (e.g., media bytes transferred)
    extra_data = models.JSONField(
        default=dict,
        blank=True,
        help_text=_("Extra progress data for the UI (e.g., bytes transferred for media)")
    )

    class Meta:
        ordering = ['id']
        verbose_name = _("Sync Step")
        verbose_name_plural = _("Sync Steps")
        unique_together = [['job', 'category']]

    def __str__(self):
        return f"{self.category} - {self.get_status_display()}"

    @property
    def progress_percent(self):
        if self.items_total == 0:
            return 0
        return round(((self.items_synced + self.items_skipped + self.items_failed) / self.items_total) * 100)

    def start(self):
        self.status = 'running'
        self.started_at = timezone.now()
        self.save(update_fields=['status', 'started_at'])

    def complete(self):
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save(update_fields=[
            'status', 'completed_at',
            'items_total', 'items_synced', 'items_skipped', 'items_failed',
            'diff_data', 'extra_data',
        ])

    def fail(self, error_message=''):
        self.status = 'failed'
        self.completed_at = timezone.now()
        self.error_message = error_message
        self.save(update_fields=['status', 'completed_at', 'error_message'])

    def skip(self, reason=''):
        self.status = 'skipped'
        self.error_message = reason
        self.save(update_fields=['status', 'error_message'])

    def increment_synced(self):
        self.items_synced += 1
        self.save(update_fields=['items_synced'])

    def increment_skipped(self):
        self.items_skipped += 1
        self.save(update_fields=['items_skipped'])

    def increment_failed(self):
        self.items_failed += 1
        self.save(update_fields=['items_failed'])
