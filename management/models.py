import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class DatabaseBackup(models.Model):
    """Track database backup operations"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file_path = models.CharField(max_length=500, blank=True)
    file_size = models.BigIntegerField(null=True, blank=True, help_text="File size in bytes")
    
    # Backup details
    backup_type = models.CharField(
        max_length=20,
        choices=[
            ('full', 'Full Database'),
            ('schema', 'Schema Only'),
            ('data', 'Data Only'),
        ],
        default='full'
    )
    
    compression = models.CharField(
        max_length=10,
        choices=[
            ('none', 'None'),
            ('gzip', 'Gzip'),
            ('bzip2', 'Bzip2'),
        ],
        default='gzip'
    )
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Status
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True)
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Database Backup"
        verbose_name_plural = "Database Backups"

    def __str__(self):
        return f"Backup: {self.name} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"


class QueryHistory(models.Model):
    """Track SQL queries executed through the admin"""
    query = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    executed_at = models.DateTimeField(auto_now_add=True)
    
    # Execution details
    execution_time = models.FloatField(help_text="Execution time in seconds")
    rows_affected = models.IntegerField(default=0)
    
    # Status
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-executed_at']
        verbose_name = "Query History"
        verbose_name_plural = "Query History"

    def __str__(self):
        return f"Query by {self.user} at {self.executed_at.strftime('%Y-%m-%d %H:%M')}"


class SystemMetrics(models.Model):
    """Store system performance metrics"""
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # CPU metrics
    cpu_percent = models.FloatField()
    cpu_count = models.IntegerField()
    load_average = models.JSONField(default=list)  # 1min, 5min, 15min
    
    # Memory metrics
    memory_total = models.BigIntegerField()  # bytes
    memory_available = models.BigIntegerField()  # bytes
    memory_percent = models.FloatField()
    memory_used = models.BigIntegerField()  # bytes
    
    # Disk metrics
    disk_total = models.BigIntegerField()  # bytes
    disk_used = models.BigIntegerField()  # bytes
    disk_free = models.BigIntegerField()  # bytes
    disk_percent = models.FloatField()
    
    # Network metrics
    network_bytes_sent = models.BigIntegerField(default=0)
    network_bytes_recv = models.BigIntegerField(default=0)
    network_packets_sent = models.BigIntegerField(default=0)
    network_packets_recv = models.BigIntegerField(default=0)
    
    # Django metrics
    active_sessions = models.IntegerField(default=0)
    cache_hits = models.BigIntegerField(default=0)
    cache_misses = models.BigIntegerField(default=0)
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "System Metrics"
        verbose_name_plural = "System Metrics"

    def __str__(self):
        return f"Metrics {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"


class AccessLog(models.Model):
    """Track admin access and actions"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    
    # Request details
    path = models.CharField(max_length=500)
    method = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Response details
    status_code = models.IntegerField()
    response_time = models.FloatField(help_text="Response time in seconds")
    
    # Action context
    action = models.CharField(max_length=100, blank=True)  # e.g., "Database Query", "File Upload"
    details = models.JSONField(default=dict, blank=True)
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Access Log"
        verbose_name_plural = "Access Logs"

    def __str__(self):
        user_info = self.user.username if self.user else "Anonymous"
        return f"{user_info} - {self.method} {self.path} at {self.timestamp.strftime('%H:%M:%S')}"


class FileOperation(models.Model):
    """Track file operations in the file manager"""
    OPERATION_TYPES = [
        ('upload', 'Upload'),
        ('download', 'Download'),
        ('delete', 'Delete'),
        ('rename', 'Rename'),
        ('move', 'Move'),
        ('copy', 'Copy'),
        ('create_folder', 'Create Folder'),
    ]
    
    operation_type = models.CharField(max_length=20, choices=OPERATION_TYPES)
    file_path = models.CharField(max_length=1000)
    file_size = models.BigIntegerField(null=True, blank=True)
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Operation details
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)
    
    # Additional context
    source_path = models.CharField(max_length=1000, blank=True)  # For move/copy operations
    details = models.JSONField(default=dict, blank=True)
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "File Operation"
        verbose_name_plural = "File Operations"

    def __str__(self):
        return f"{self.operation_type}: {self.file_path} by {self.user}"


# =============================================================================
# Deployment Dashboard Models
# =============================================================================

class DeploymentBackup(models.Model):
    """
    Enhanced backup model for full system backups (db + media + config).
    Different from DatabaseBackup which only handles database dumps.
    This model tracks backups created via the deployment scripts.
    """
    BACKUP_TYPES = [
        ('full', 'Full System'),
        ('db', 'Database Only'),
        ('media', 'Media Only'),
        ('config', 'Configuration Only'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('compressing', 'Compressing'),
        ('encrypting', 'Encrypting'),
        ('uploading', 'Uploading'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    name = models.CharField(max_length=200)
    backup_type = models.CharField(max_length=20, choices=BACKUP_TYPES, default='full')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Storage locations
    local_path = models.CharField(max_length=500, blank=True)

    # Options
    is_compressed = models.BooleanField(default=True)
    is_encrypted = models.BooleanField(default=False)

    # Size
    file_size = models.BigIntegerField(null=True, blank=True, help_text="File size in bytes")

    # Progress tracking for real-time UI
    progress_percent = models.IntegerField(default=0)
    current_step = models.CharField(max_length=100, blank=True)
    task_id = models.CharField(max_length=100, blank=True, help_text="Celery task ID")

    # Timing
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    error_message = models.TextField(blank=True)
    manifest = models.JSONField(default=dict, blank=True, help_text="Backup contents manifest")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Deployment Backup"
        verbose_name_plural = "Deployment Backups"

    def __str__(self):
        return f"{self.name} ({self.get_backup_type_display()}) - {self.get_status_display()}"

    @property
    def file_size_display(self):
        """Return human-readable file size"""
        if not self.file_size:
            return "Unknown"
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"


class BackupSchedule(models.Model):
    """
    Scheduled backup configuration.
    Singleton-like model - only one schedule configuration per installation.
    """
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    BACKUP_TYPE_CHOICES = [
        ('full', 'Full System'),
        ('db', 'Database Only'),
    ]

    is_enabled = models.BooleanField(default=False)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='daily')
    time_of_day = models.TimeField(default='03:00', help_text="Time to run backup (server timezone)")
    day_of_week = models.IntegerField(
        default=0,
        help_text="0=Monday, 6=Sunday. Only used for weekly backups."
    )
    day_of_month = models.IntegerField(
        default=1,
        help_text="Day of month (1-28). Only used for monthly backups."
    )

    backup_type = models.CharField(max_length=20, choices=BACKUP_TYPE_CHOICES, default='full')

    # Remote storage destinations
    remote_destinations = models.ManyToManyField(
        'RemoteStorageDestination',
        blank=True,
        related_name='backup_schedules',
        verbose_name=_("remote destinations"),
        help_text=_("Upload scheduled backups to these destinations"),
    )

    # Encryption
    encrypt = models.BooleanField(default=False)

    # Retention
    retention_days = models.IntegerField(default=30, help_text="Delete backups older than this many days")

    # Tracking
    last_run = models.DateTimeField(null=True, blank=True)
    next_run = models.DateTimeField(null=True, blank=True)
    last_backup = models.ForeignKey(
        DeploymentBackup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='schedule_runs'
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Backup Schedule"
        verbose_name_plural = "Backup Schedules"

    def __str__(self):
        status = "Enabled" if self.is_enabled else "Disabled"
        return f"Backup Schedule ({self.get_frequency_display()}) - {status}"

    def calculate_next_run(self):
        """Calculate the next run time based on frequency and schedule"""
        from datetime import datetime, timedelta
        import calendar

        now = timezone.now()
        base_time = now.replace(
            hour=self.time_of_day.hour,
            minute=self.time_of_day.minute,
            second=0,
            microsecond=0
        )

        if self.frequency == 'daily':
            next_run = base_time
            if next_run <= now:
                next_run += timedelta(days=1)

        elif self.frequency == 'weekly':
            days_ahead = self.day_of_week - now.weekday()
            if days_ahead < 0 or (days_ahead == 0 and base_time <= now):
                days_ahead += 7
            next_run = base_time + timedelta(days=days_ahead)

        elif self.frequency == 'monthly':
            next_run = base_time.replace(day=min(self.day_of_month, 28))
            if next_run <= now:
                # Move to next month
                if now.month == 12:
                    next_run = next_run.replace(year=now.year + 1, month=1)
                else:
                    next_run = next_run.replace(month=now.month + 1)

        self.next_run = next_run
        return next_run


class SystemUpgrade(models.Model):
    """Track upgrade operations"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('preflight', 'Running Preflight Checks'),
        ('backup', 'Creating Backup'),
        ('draining', 'Draining Celery Tasks'),
        ('maintenance', 'Enabling Maintenance Mode'),
        ('pulling', 'Pulling New Images'),
        ('upgrading', 'Upgrading Containers'),
        ('migrating', 'Running Migrations'),
        ('finalizing', 'Finalizing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('rolling_back', 'Rolling Back'),
        ('rolled_back', 'Rolled Back'),
    ]

    from_version = models.CharField(max_length=50)
    to_version = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Progress tracking
    progress_percent = models.IntegerField(default=0)
    current_step = models.CharField(max_length=100, blank=True)
    task_id = models.CharField(max_length=100, blank=True, help_text="Celery task ID")

    # Related backup
    pre_upgrade_backup = models.ForeignKey(
        DeploymentBackup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='upgrade_operations'
    )

    # Preflight and migration info
    preflight_results = models.JSONField(default=dict, blank=True)
    migration_plan = models.JSONField(default=list, blank=True)

    # Timing
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    error_message = models.TextField(blank=True)
    changelog = models.TextField(blank=True, help_text="What's new in this version")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "System Upgrade"
        verbose_name_plural = "System Upgrades"

    def __str__(self):
        return f"Upgrade {self.from_version} → {self.to_version} ({self.get_status_display()})"


class SystemRestore(models.Model):
    """Track restore operations"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirming', 'Awaiting Confirmation'),
        ('backup', 'Creating Safety Backup'),
        ('downloading', 'Downloading from Remote Storage'),
        ('decrypting', 'Decrypting'),
        ('extracting', 'Extracting'),
        ('restoring_db', 'Restoring Database'),
        ('restoring_media', 'Restoring Media'),
        ('restoring_config', 'Restoring Configuration'),
        ('post_restore', 'Running Post-Restore Tasks'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    source_backup = models.ForeignKey(
        DeploymentBackup,
        on_delete=models.CASCADE,
        related_name='restores'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Progress tracking
    progress_percent = models.IntegerField(default=0)
    current_step = models.CharField(max_length=100, blank=True)
    task_id = models.CharField(max_length=100, blank=True, help_text="Celery task ID")

    # Component selection
    skip_database = models.BooleanField(default=False)
    skip_media = models.BooleanField(default=False)
    skip_config = models.BooleanField(default=False)

    # Safety backup before restore
    pre_restore_backup = models.ForeignKey(
        DeploymentBackup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='restore_safety_backups'
    )

    # Timing
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    error_message = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "System Restore"
        verbose_name_plural = "System Restores"

    def __str__(self):
        return f"Restore from {self.source_backup.name} ({self.get_status_display()})"


class SystemStatus(models.Model):
    """
    Cached system status snapshot.
    Updated periodically by Celery task.
    Only one record should exist - acts as a singleton.
    """
    checked_at = models.DateTimeField(auto_now=True)

    # Service health (DB, Redis, Celery - not NGINX since it's external)
    db_healthy = models.BooleanField(default=False)
    db_details = models.JSONField(default=dict, blank=True, help_text="Database status details")

    redis_healthy = models.BooleanField(default=False)
    redis_details = models.JSONField(default=dict, blank=True, help_text="Redis status details")

    celery_healthy = models.BooleanField(default=False)
    celery_details = models.JSONField(default=dict, blank=True, help_text="Celery worker details")

    # SSL status
    ssl_domain = models.CharField(max_length=200, blank=True)
    ssl_expiry_date = models.DateTimeField(null=True, blank=True)
    ssl_days_remaining = models.IntegerField(null=True, blank=True)
    ssl_valid = models.BooleanField(default=False)

    # Version info
    current_version = models.CharField(max_length=50, blank=True)
    available_version = models.CharField(max_length=50, blank=True)
    update_available = models.BooleanField(default=False)

    # Maintenance mode
    maintenance_mode = models.BooleanField(default=False)
    maintenance_reason = models.CharField(max_length=200, blank=True)

    # Disk usage
    disk_total = models.BigIntegerField(null=True, blank=True)
    disk_used = models.BigIntegerField(null=True, blank=True)
    disk_free = models.BigIntegerField(null=True, blank=True)
    disk_percent = models.FloatField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "System Status"
        verbose_name_plural = "System Status"

    def __str__(self):
        return f"System Status (checked {self.checked_at})"

    @classmethod
    def get_instance(cls):
        """Get or create the singleton instance"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def all_services_healthy(self):
        """Check if all monitored services are healthy"""
        return self.db_healthy and self.redis_healthy and self.celery_healthy

    @property
    def healthy_service_count(self):
        """Count of healthy services"""
        count = 0
        if self.db_healthy:
            count += 1
        if self.redis_healthy:
            count += 1
        if self.celery_healthy:
            count += 1
        return count

    @property
    def total_service_count(self):
        """Total number of monitored services"""
        return 3  # DB, Redis, Celery


# =============================================================================
# Log Viewer Models
# =============================================================================

class LogEntry(models.Model):
    """Archived log entries from Docker containers"""

    LEVEL_CHOICES = [
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
        ('CRITICAL', 'Critical'),
    ]

    CONTAINER_CHOICES = [
        ('db', 'PostgreSQL'),
        ('redis', 'Redis'),
        ('minio', 'MinIO'),
        ('shop', 'Spwig Web'),
        ('celery', 'Celery Worker'),
        ('celery_beat', 'Celery Beat'),
        ('translator', 'Translator'),
        ('nginx', 'Nginx'),
        ('upgrader', 'Upgrader'),
    ]

    SOURCE_CHOICES = [
        ('stdout', 'Standard Output'),
        ('stderr', 'Standard Error'),
    ]

    # Core fields
    container_name = models.CharField(max_length=50, choices=CONTAINER_CHOICES, db_index=True)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, db_index=True)
    message = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

    # Metadata
    raw_line = models.TextField(blank=True, help_text="Original log line before parsing")
    source = models.CharField(max_length=20, default='stdout', choices=SOURCE_CHOICES)

    # For efficient cleanup
    archived_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Log Entry"
        verbose_name_plural = "Log Entries"
        indexes = [
            models.Index(fields=['container_name', 'timestamp'], name='mgmt_log_container_ts'),
            models.Index(fields=['level', 'timestamp'], name='mgmt_log_level_ts'),
            models.Index(fields=['container_name', 'level', 'timestamp'], name='mgmt_log_container_level_ts'),
            models.Index(fields=['archived_at'], name='mgmt_log_archived'),
        ]

    def __str__(self):
        return f"[{self.container_name}] {self.level}: {self.message[:100]}"


class LogViewerSettings(models.Model):
    """
    Log viewer configuration - singleton pattern.
    Controls retention periods, streaming settings, and display options.
    """

    # Retention settings
    redis_retention_minutes = models.IntegerField(
        default=60,
        help_text="How long to keep logs in Redis (minutes)"
    )
    db_retention_days = models.IntegerField(
        default=30,
        help_text="How long to keep archived logs in database (days)"
    )

    # Archive settings
    archive_batch_size = models.IntegerField(
        default=100,
        help_text="Number of logs to archive in each batch"
    )
    archive_interval_seconds = models.IntegerField(
        default=300,
        help_text="How often to archive logs from Redis to DB (seconds)"
    )

    # Streaming settings
    stream_enabled = models.BooleanField(
        default=True,
        help_text="Enable real-time log collection from Docker containers"
    )
    max_logs_per_container = models.IntegerField(
        default=1000,
        help_text="Maximum logs to keep in Redis per container"
    )

    # Sanitization patterns (JSON list of regex patterns)
    sensitive_patterns = models.JSONField(
        default=list,
        blank=True,
        help_text="Regex patterns to redact from logs (e.g., passwords, tokens)"
    )

    # Display settings
    default_page_size = models.IntegerField(
        default=50,
        help_text="Default number of logs to show per page"
    )
    auto_refresh_interval = models.IntegerField(
        default=5,
        help_text="Auto-refresh interval in seconds for UI"
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Log Viewer Settings"
        verbose_name_plural = "Log Viewer Settings"

    def save(self, *args, **kwargs):
        # Singleton pattern - only one instance allowed
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_instance(cls):
        """Get or create the singleton instance"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Log Viewer Settings"


# =============================================================================
# Remote Storage Models
# =============================================================================

class RemoteStorageDestination(models.Model):
    """
    A configured remote storage destination for backup uploads.
    Merchants can configure multiple destinations (e.g. S3 + SFTP).
    Credentials are encrypted using the same Fernet pattern as
    PaymentProviderAccount.
    """
    PROVIDER_TYPES = [
        ('s3', _('Amazon S3 / S3-Compatible')),
        ('sftp', _('SFTP')),
        ('google_drive', _('Google Drive')),
        ('dropbox', _('Dropbox')),
    ]

    CONNECTION_STATUS_CHOICES = [
        ('unknown', _('Unknown')),
        ('connected', _('Connected')),
        ('error', _('Error')),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(
        max_length=200,
        verbose_name=_("destination name"),
        help_text=_("Friendly name for this destination"),
    )
    provider_type = models.CharField(
        max_length=20,
        choices=PROVIDER_TYPES,
        verbose_name=_("storage type"),
    )

    # Encrypted credentials (Fernet per-field encryption in JSONField)
    credentials_encrypted = models.JSONField(
        default=dict,
        verbose_name=_("encrypted credentials"),
    )

    # Non-secret provider settings (bucket, prefix, region, etc.)
    settings = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("provider settings"),
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_("active"),
    )
    is_default = models.BooleanField(
        default=False,
        verbose_name=_("default destination"),
        help_text=_("Automatically upload all backups to this destination"),
    )

    # Connection health
    connection_status = models.CharField(
        max_length=20,
        choices=CONNECTION_STATUS_CHOICES,
        default='unknown',
    )
    connection_error = models.TextField(blank=True)
    last_tested_at = models.DateTimeField(null=True, blank=True)

    # Upload stats
    last_upload_at = models.DateTimeField(null=True, blank=True)
    last_upload_size = models.BigIntegerField(null=True, blank=True)
    total_uploads = models.IntegerField(default=0)
    total_bytes_uploaded = models.BigIntegerField(default=0)

    # Per-destination retention (0 = no auto-deletion)
    retention_days = models.IntegerField(
        default=0,
        help_text=_("Delete remote backups older than this many days. 0 = keep forever."),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = _("Remote Storage Destination")
        verbose_name_plural = _("Remote Storage Destinations")

    def __str__(self):
        return f"{self.name} ({self.get_provider_type_display()})"

    @property
    def total_bytes_display(self):
        """Human-readable total bytes uploaded."""
        size = self.total_bytes_uploaded
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"


class BackupRemoteUpload(models.Model):
    """
    Tracks individual backup uploads to remote destinations.
    One backup can be uploaded to multiple destinations.
    """
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('uploading', _('Uploading')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
    ]

    backup = models.ForeignKey(
        DeploymentBackup,
        on_delete=models.CASCADE,
        related_name='remote_uploads',
    )
    destination = models.ForeignKey(
        RemoteStorageDestination,
        on_delete=models.CASCADE,
        related_name='uploads',
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    remote_path = models.CharField(max_length=500, blank=True)
    file_size = models.BigIntegerField(null=True, blank=True)

    progress_percent = models.IntegerField(default=0)
    task_id = models.CharField(max_length=100, blank=True)

    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = [['backup', 'destination']]
        verbose_name = _("Backup Remote Upload")
        verbose_name_plural = _("Backup Remote Uploads")

    def __str__(self):
        return f"{self.backup.name} → {self.destination.name} ({self.get_status_display()})"