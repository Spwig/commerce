"""
SyncJob Model
Tracks Spwig-to-Spwig sync and migration operations.
"""

import uuid
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class SyncJob(models.Model):
    """
    Tracks a sync or migration operation between Spwig instances.
    Analogous to MigrationJob for external platform imports.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    JOB_TYPE_CHOICES = [
        ("settings_sync", _("Settings Sync")),
        ("full_migration", _("Full System Migration")),
    ]
    job_type = models.CharField(
        max_length=20, choices=JOB_TYPE_CHOICES, help_text=_("Type of sync operation")
    )

    DIRECTION_CHOICES = [
        ("pull", _("Pull from Remote")),
        ("push", _("Push to Remote")),
    ]
    direction = models.CharField(
        max_length=10, choices=DIRECTION_CHOICES, help_text=_("Direction of data flow")
    )

    connection = models.ForeignKey(
        "migration.SyncConnection",
        on_delete=models.SET_NULL,
        null=True,
        related_name="sync_jobs",
        help_text=_("Connection to the remote instance"),
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="sync_jobs",
        help_text=_("User who initiated this sync"),
    )

    # Selected categories (list of category keys from the registry)
    selected_categories = models.JSONField(
        default=list, blank=True, help_text=_("List of sync category keys selected for this job")
    )

    SYNC_MODE_CHOICES = [
        ("additive", _("Add & Update Only")),
        ("mirror", _("Full Mirror")),
    ]
    sync_mode = models.CharField(
        max_length=20,
        choices=SYNC_MODE_CHOICES,
        default="additive",
        help_text=_("Sync behaviour: additive (no deletions) or mirror (exact copy)"),
    )

    STATUS_CHOICES = [
        ("pending", _("Pending")),
        ("previewing", _("Generating Preview")),
        ("awaiting_confirmation", _("Awaiting Confirmation")),
        ("running", _("Running")),
        ("completed", _("Completed")),
        ("failed", _("Failed")),
        ("rolling_back", _("Rolling Back")),
        ("rolled_back", _("Rolled Back")),
        ("cancelled", _("Cancelled")),
    ]
    status = models.CharField(
        max_length=25,
        choices=STATUS_CHOICES,
        default="pending",
        help_text=_("Current status of the sync operation"),
    )

    progress_percent = models.IntegerField(
        default=0, help_text=_("Overall progress percentage (0-100)")
    )
    current_step = models.CharField(
        max_length=100, blank=True, help_text=_("Name of the currently executing step")
    )

    # Preview/diff data
    diff_preview = models.JSONField(
        default=dict, blank=True, help_text=_("Structured diff from preview step")
    )

    # Production safety
    production_confirmed = models.BooleanField(
        default=False, help_text=_("Whether the merchant confirmed production overwrite")
    )

    # Rollback support
    rollback_snapshot = models.JSONField(
        default=dict, blank=True, help_text=_("Pre-sync state snapshot for rollback")
    )
    can_rollback = models.BooleanField(
        default=True, help_text=_("Whether this job can be rolled back")
    )
    rollback_deadline = models.DateTimeField(
        null=True, blank=True, help_text=_("Deadline for rollback (24 hours after completion)")
    )

    # Statistics
    items_total = models.IntegerField(default=0)
    items_synced = models.IntegerField(default=0)
    items_skipped = models.IntegerField(default=0)
    items_failed = models.IntegerField(default=0)

    # Timing
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.IntegerField(null=True, blank=True)

    error_summary = models.TextField(blank=True)

    # Activity log for real-time progress display
    activity_log = models.JSONField(
        default=list,
        blank=True,
        help_text=_("Recent activity log entries [{ts, msg}, ...] (last 50)"),
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Sync Job")
        verbose_name_plural = _("Sync Jobs")

    def __str__(self):
        return f"{self.get_job_type_display()} - {self.get_status_display()} ({str(self.id)[:8]})"

    @property
    def total_items(self):
        return self.items_total

    @property
    def total_synced(self):
        return self.items_synced

    @property
    def success_rate(self):
        if self.items_total == 0:
            return 0
        return round((self.items_synced / self.items_total) * 100, 1)

    @property
    def is_rollbackable(self):
        if not self.can_rollback:
            return False
        if self.status != "completed":
            return False
        return not (self.rollback_deadline and timezone.now() > self.rollback_deadline)

    def add_log_entry(self, message):
        """
        Append a timestamped log entry, keeping last 50 entries.

        Note: This uses read-modify-write which is NOT safe for concurrent
        writers. All current callers execute within a single Celery task
        (execute_settings_sync or execute_full_migration), so no race
        condition exists. If concurrent writes are needed in future, use
        a DB-level atomic JSON append instead.
        """
        entry = {
            "ts": timezone.now().strftime("%H:%M:%S"),
            "msg": str(message),
        }
        self.refresh_from_db(fields=["activity_log"])
        log = list(self.activity_log or [])
        log.append(entry)
        if len(log) > 50:
            log = log[-50:]
        self.activity_log = log
        self.save(update_fields=["activity_log"])

    def update_progress(self, step, percent):
        self.current_step = step
        self.progress_percent = min(100, max(0, percent))
        self.save(update_fields=["current_step", "progress_percent"])

    def start(self):
        self.status = "running"
        self.started_at = timezone.now()
        self.save(update_fields=["status", "started_at"])

    def mark_completed(self):
        self.status = "completed"
        self.completed_at = timezone.now()
        self.progress_percent = 100
        if self.started_at:
            self.duration_seconds = int((self.completed_at - self.started_at).total_seconds())
        self.rollback_deadline = timezone.now() + timedelta(hours=24)
        self.save(
            update_fields=[
                "status",
                "completed_at",
                "progress_percent",
                "duration_seconds",
                "rollback_deadline",
                "items_total",
                "items_synced",
                "items_skipped",
                "items_failed",
            ]
        )

    def mark_failed(self, error_message=""):
        self.status = "failed"
        self.completed_at = timezone.now()
        self.error_summary = error_message
        if self.started_at:
            self.duration_seconds = int((self.completed_at - self.started_at).total_seconds())
        self.save(
            update_fields=[
                "status",
                "completed_at",
                "error_summary",
                "duration_seconds",
                "items_total",
                "items_synced",
                "items_skipped",
                "items_failed",
            ]
        )

    def mark_cancelled(self):
        self.status = "cancelled"
        self.completed_at = timezone.now()
        self.save(update_fields=["status", "completed_at"])
