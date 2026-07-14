"""
Models for Component Update & Distribution System
Manages versioning, updates, and rollback for all platform components
"""

import json
import uuid

from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UpdateChannel(models.Model):
    """
    Update channels for controlling component update distribution
    Similar to Chrome's stable/beta/dev channels
    """

    STABLE = "stable"
    BETA = "beta"
    DEV = "dev"
    SECURITY = "security"

    CHANNEL_CHOICES = [
        (STABLE, _("Stable - Production-ready releases")),
        (BETA, _("Beta - Pre-release testing")),
        (DEV, _("Development - Latest features")),
        (SECURITY, _("Security - Critical security patches")),
    ]

    name = models.CharField(
        max_length=20, choices=CHANNEL_CHOICES, unique=True, help_text=_("Update channel name")
    )
    description = models.TextField(blank=True)
    priority = models.IntegerField(
        default=0, help_text=_("Lower numbers = higher priority. Security=99")
    )
    is_active = models.BooleanField(
        default=True, help_text=_("Whether this channel is currently active")
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["priority", "name"]
        verbose_name = _("Update Channel")
        verbose_name_plural = _("Update Channels")

    def __str__(self):
        return self.get_name_display()


class ComponentRegistry(models.Model):
    """
    Central registry of all installed platform components
    Tracks widgets, themes, utilities, elements, and templates
    """

    COMPONENT_TYPES = [
        ("widget", _("Widget")),
        ("theme", _("Theme")),
        ("utility", _("Page Builder Utility")),
        ("element", _("Page Builder Element")),
        ("header_template", _("Header Template")),
        ("footer_template", _("Footer Template")),
        ("shipping_provider", _("Shipping Provider")),
        ("email_provider", _("Email Provider")),
        ("sms_provider", _("SMS Provider")),
        ("exchange_rate_provider", _("Exchange Rate Provider")),
        ("payment_provider", _("Payment Provider")),
        ("product_feed_provider", _("Product Feed Provider")),
        ("terminal_provider", _("Terminal Provider")),
        ("seo_generator_provider", _("SEO Generator Provider")),
        ("social_connector_provider", _("Social Connector Provider")),
        ("translation_provider", _("Translation Provider")),
        ("language_pack", _("Language Pack")),
    ]

    # Component identification
    component_type = models.CharField(
        max_length=50, choices=COMPONENT_TYPES, db_index=True, help_text=_("Type of component")
    )
    slug = models.SlugField(
        max_length=200, db_index=True, help_text=_("Unique component identifier")
    )
    name = models.CharField(max_length=200, help_text=_("Display name"))

    # Current version info
    current_version = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r"^\d+\.\d+\.\d+(?:[-+][\w\d.]+)?$",
                message="Version must follow SemVer format (e.g., 1.2.3)",
            )
        ],
        help_text=_("Currently installed version (SemVer)"),
    )

    # Installation tracking
    installed_at = models.DateTimeField(
        default=timezone.now, help_text=_("When this component was first installed")
    )
    last_updated = models.DateTimeField(auto_now=True, help_text=_("Last update timestamp"))
    last_checked = models.DateTimeField(
        null=True, blank=True, help_text=_("Last time we checked for updates")
    )

    # Update management
    update_available = models.BooleanField(
        default=False, help_text=_("Whether an update is available")
    )
    latest_version = models.CharField(
        max_length=20, blank=True, help_text=_("Latest available version")
    )
    latest_version_checksum = models.CharField(
        max_length=64, blank=True, help_text=_("SHA256 checksum of latest version package")
    )
    auto_update = models.BooleanField(default=False, help_text=_("Automatically install updates"))
    update_channel = models.ForeignKey(
        "UpdateChannel",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_("Update channel to follow"),
    )

    # Lock/freeze component
    locked = models.BooleanField(
        default=False, help_text=_("Prevent any updates to this component")
    )
    lock_reason = models.TextField(blank=True, help_text=_("Why this component is locked"))

    # Metadata
    author = models.CharField(max_length=200, blank=True)
    author_details = models.JSONField(
        default=dict,
        blank=True,
        help_text=_("Author information from update server (name, homepage, logo, etc.)"),
    )
    description = models.TextField(blank=True)
    homepage_url = models.URLField(blank=True)
    support_url = models.URLField(blank=True)

    # Visual assets (for marketplace-style UI)
    thumbnail_url = models.URLField(
        blank=True, help_text=_("URL to component thumbnail image - 600x800px for themes")
    )
    preview_images = models.JSONField(
        default=list, blank=True, help_text=_("Array of preview image URLs")
    )
    preview_videos = models.JSONField(
        default=list,
        blank=True,
        help_text=_("Array of preview video objects [{url, title, mime_type}]"),
    )

    # Platform compatibility
    requires_platform_version = models.CharField(
        max_length=20, blank=True, help_text=_("Required platform version (e.g., '1.x', '2.x')")
    )
    engine_min_version = models.CharField(max_length=20, blank=True)
    engine_max_version = models.CharField(max_length=20, blank=True)

    # Reference to original package (if applicable)
    theme = models.OneToOneField(
        "design.Theme",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="registry_entry",
    )
    header_template = models.OneToOneField(
        "design.HeaderTemplate",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="registry_entry",
    )
    footer_template = models.OneToOneField(
        "design.FooterTemplate",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="registry_entry",
    )

    class Meta:
        unique_together = [["component_type", "slug"]]
        ordering = ["component_type", "name"]
        verbose_name = _("Component")
        verbose_name_plural = _("Component Registry")
        indexes = [
            models.Index(fields=["component_type", "slug"]),
            models.Index(fields=["update_available"]),
            models.Index(fields=["auto_update"]),
        ]

    def __str__(self):
        return f"{self.get_component_type_display()}: {self.name} v{self.current_version}"

    def has_update(self):
        """Check if update is available and not locked"""
        return self.update_available and not self.locked

    def get_rollback_versions(self):
        """Get available versions for rollback (last 3)"""
        return self.versions.filter(rollback_available=True).order_by("-installed_at")[:3]

    def _resolve_component_dir(self):
        """
        Resolve the filesystem directory for this component's current version.
        Integrations live under components_data/integrations/,
        utilities live under components_data/static/utilities/.
        Returns (component_dir, static_prefix) or (None, None).
        """
        from component_updates.integration_paths import COMPONENTS_DATA, INTEGRATIONS_DIR

        if self.component_type == "utility":
            # Utilities use underscore dirs; slug may use hyphens
            slug_variants = [self.slug, self.slug.replace("-", "_"), self.slug.replace("_", "-")]
            utilities_dir = COMPONENTS_DATA / "static" / "utilities"
            for slug in slug_variants:
                component_dir = utilities_dir / slug / "current"
                if component_dir.exists():
                    # Static prefix: relative to components_data/static/ which is in STATICFILES_DIRS
                    return component_dir, f"utilities/{slug}/current"
            return None, None
        else:
            component_dir = INTEGRATIONS_DIR / self.component_type / self.slug / "current"
            if component_dir.exists():
                # Static prefix: relative to components_data/integrations/ which is in STATICFILES_DIRS
                return component_dir, f"{self.component_type}/{self.slug}/current"
            return None, None

    @property
    def logo(self):
        """
        Get the logo URL for this component from its manifest.
        Returns a dict with 'url' and 'mime_type', or None if no logo exists.
        """
        from django.templatetags.static import static

        component_dir, static_prefix = self._resolve_component_dir()
        if not component_dir:
            return None

        # Check for manifest to get logo file name
        manifest_path = component_dir / "manifest.json"
        if manifest_path.exists():
            try:
                with open(manifest_path) as f:
                    manifest = json.load(f)
                    logo_info = manifest.get("logo", {})
                    if isinstance(logo_info, dict):
                        logo_file = logo_info.get("file")
                        mime_type = logo_info.get("mime_type", "image/svg+xml")
                    elif isinstance(logo_info, str):
                        # Backward compatibility: logo might be just a string
                        logo_file = logo_info
                        mime_type = "image/svg+xml"
                    else:
                        logo_file = None

                    if logo_file:
                        logo_path = component_dir / logo_file
                        if logo_path.exists():
                            static_path = f"{static_prefix}/{logo_file}"
                            return {
                                "url": static(static_path),
                                "mime_type": mime_type,
                                "file": logo_file,
                            }
            except (OSError, json.JSONDecodeError, KeyError):
                pass

        # Fallback: check for common logo file names
        for logo_file in ["logo.svg", "logo.png", "icon.svg", "icon.png"]:
            logo_path = component_dir / logo_file
            if logo_path.exists():
                static_path = f"{static_prefix}/{logo_file}"
                mime_type = "image/svg+xml" if logo_file.endswith(".svg") else "image/png"
                return {"url": static(static_path), "mime_type": mime_type, "file": logo_file}

        return None

    @property
    def icon(self):
        """
        Convenience property that returns just the logo URL.
        Returns the static URL string or None if no logo exists.
        """
        logo_data = self.logo
        if logo_data and isinstance(logo_data, dict):
            return logo_data.get("url")
        return None

    def get_manifest(self):
        """
        Get the manifest.json for this component.
        Returns the manifest dict or None if not found.
        """
        component_dir, _ = self._resolve_component_dir()
        if not component_dir:
            return None

        manifest_path = component_dir / "manifest.json"
        if not manifest_path.exists():
            return None

        try:
            with open(manifest_path) as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            return None

    @property
    def installed_path(self):
        """
        Get the installation path for this component.
        Returns the path or None if not applicable.
        """
        component_dir, _ = self._resolve_component_dir()
        return str(component_dir) if component_dir else None


class ComponentVersion(models.Model):
    """
    Version history for components, enabling rollback capability
    Keeps last 3 versions installed for quick rollback
    """

    HEALTH_CHOICES = [
        ("healthy", _("Healthy - Working as expected")),
        ("degraded", _("Degraded - Some issues detected")),
        ("unhealthy", _("Unhealthy - Critical issues")),
        ("unknown", _("Unknown - Not yet verified")),
    ]

    component = models.ForeignKey(
        ComponentRegistry, on_delete=models.CASCADE, related_name="versions"
    )

    # Version info
    version = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r"^\d+\.\d+\.\d+(?:[-+][\w\d.]+)?$",
                message="Version must follow SemVer format",
            )
        ],
    )

    # Installation tracking
    installed_at = models.DateTimeField(default=timezone.now)
    uninstalled_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(
        default=True, help_text=_("Whether this version is currently active")
    )

    # Installation method
    install_method = models.CharField(
        max_length=50,
        choices=[
            ("bundled", _("Bundled")),
            ("manual", _("Manual Upload")),
            ("update_server", _("Update Server")),
            ("git", _("Git Repository")),
            ("marketplace", _("Marketplace")),
        ],
        default="update_server",
    )

    # Rollback capability
    rollback_available = models.BooleanField(
        default=True, help_text=_("Whether this version can be rolled back to")
    )

    # Health monitoring
    health_status = models.CharField(max_length=20, choices=HEALTH_CHOICES, default="unknown")
    health_checked_at = models.DateTimeField(null=True, blank=True)
    health_details = models.JSONField(
        default=dict, blank=True, help_text=_("Detailed health check results")
    )

    # Package info
    package_checksum = models.CharField(
        max_length=64, blank=True, help_text=_("SHA256 checksum of package")
    )
    package_size_bytes = models.IntegerField(default=0)
    package_url = models.URLField(blank=True)

    # Metadata
    release_notes = models.TextField(blank=True)
    breaking_changes = models.BooleanField(default=False)
    security_update = models.BooleanField(default=False)

    # Installation details
    installation_log = models.TextField(blank=True, help_text=_("Installation output and logs"))
    installed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="component_installations",
    )

    class Meta:
        ordering = ["-installed_at"]
        unique_together = [["component", "version"]]
        verbose_name = _("Component Version")
        verbose_name_plural = _("Component Versions")

    def __str__(self):
        status = "Active" if self.is_active else "Inactive"
        return f"{self.component.name} v{self.version} ({status})"

    def activate(self):
        """Make this version the active one"""
        # Deactivate all other versions
        ComponentVersion.objects.filter(component=self.component).update(is_active=False)

        # Activate this version
        self.is_active = True
        self.save()

        # Update component registry
        self.component.current_version = self.version
        self.component.save()


class ComponentDependency(models.Model):
    """
    Track dependencies between components
    Ensures components are updated in correct order
    """

    component = models.ForeignKey(
        ComponentRegistry, on_delete=models.CASCADE, related_name="dependencies"
    )

    depends_on = models.ForeignKey(
        ComponentRegistry, on_delete=models.CASCADE, related_name="dependents"
    )

    # SemVer version constraint (e.g., "^1.2.0", ">=2.0.0")
    version_constraint = models.CharField(max_length=50, help_text=_("Semantic version constraint"))

    # Dependency type
    is_required = models.BooleanField(
        default=True, help_text=_("Whether this dependency is required")
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [["component", "depends_on"]]
        verbose_name = _("Component Dependency")
        verbose_name_plural = _("Component Dependencies")

    def __str__(self):
        return f"{self.component.name} depends on {self.depends_on.name} {self.version_constraint}"


class UpdateLog(models.Model):
    """
    Audit trail of all component updates, installations, and rollbacks
    """

    ACTION_CHOICES = [
        ("install", _("Install - New component installed")),
        ("update", _("Update - Component updated to new version")),
        ("rollback", _("Rollback - Reverted to previous version")),
        ("uninstall", _("Uninstall - Component removed")),
        ("health_check", _("Health Check - Component verified")),
    ]

    STATUS_CHOICES = [
        ("pending", _("Pending")),
        ("in_progress", _("In Progress")),
        ("completed", _("Completed Successfully")),
        ("failed", _("Failed")),
        ("rolled_back", _("Rolled Back")),
    ]

    component = models.ForeignKey(
        ComponentRegistry, on_delete=models.CASCADE, related_name="update_logs"
    )

    # Action details
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    # Version tracking
    old_version = models.CharField(max_length=20, blank=True)
    new_version = models.CharField(max_length=20, blank=True)

    # Timing
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.IntegerField(
        null=True, blank=True, help_text=_("How long the operation took")
    )

    # Error tracking
    error_message = models.TextField(blank=True)
    error_traceback = models.TextField(blank=True)

    # Additional details
    details = models.JSONField(
        default=dict, blank=True, help_text=_("Additional operation details")
    )

    # User tracking
    performed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="component_update_logs"
    )

    # Automatic vs manual
    is_automatic = models.BooleanField(
        default=False, help_text=_("Whether this was an automatic update")
    )

    class Meta:
        ordering = ["-started_at"]
        verbose_name = _("Update Log")
        verbose_name_plural = _("Update Logs")
        indexes = [
            models.Index(fields=["component", "-started_at"]),
            models.Index(fields=["status"]),
            models.Index(fields=["action"]),
        ]

    def __str__(self):
        return f"{self.component.name}: {self.get_action_display()} ({self.get_status_display()})"

    def mark_completed(self, duration=None):
        """Mark the operation as completed"""
        self.status = "completed"
        self.completed_at = timezone.now()
        if duration is not None:
            self.duration_seconds = int(duration)
        elif self.started_at:
            delta = self.completed_at - self.started_at
            self.duration_seconds = int(delta.total_seconds())
        self.save()

    def mark_failed(self, error_message, traceback=""):
        """Mark the operation as failed"""
        self.status = "failed"
        self.completed_at = timezone.now()
        self.error_message = error_message
        self.error_traceback = traceback
        if self.started_at:
            delta = self.completed_at - self.started_at
            self.duration_seconds = int(delta.total_seconds())
        self.save()


class UpdateServerConfig(models.Model):
    """
    Configuration for the update server connection
    Singleton model - only one instance should exist
    """

    # Server configuration
    server_url = models.URLField(
        default="https://updates.spwig.com", help_text=_("Update server base URL")
    )
    api_version = models.CharField(max_length=10, default="v1", help_text=_("API version to use"))

    # Authentication
    installation_uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        help_text=_("Unique installation identifier"),
    )
    license_key = models.CharField(max_length=200, blank=True, help_text=_("Platform license key"))
    jwt_token = models.TextField(blank=True, help_text=_("Current JWT authentication token"))
    jwt_expires_at = models.DateTimeField(
        null=True, blank=True, help_text=_("When the JWT token expires")
    )

    # Update checking
    check_interval_hours = models.IntegerField(
        default=24, help_text=_("How often to check for updates (hours)")
    )
    last_check = models.DateTimeField(
        null=True, blank=True, help_text=_("Last successful update check")
    )

    # Update behavior
    auto_download = models.BooleanField(
        default=True, help_text=_("Automatically download available updates")
    )
    auto_install_security = models.BooleanField(
        default=True, help_text=_("Automatically install security updates")
    )

    # Telemetry
    send_telemetry = models.BooleanField(
        default=True, help_text=_("Send anonymous usage statistics")
    )

    # POS license management
    pos_license_key = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("POS license key"),
        help_text=_("POS subscription license key (POS-XXXX-XXXX-XXXX-XXXX)"),
    )
    pos_license_validated_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("Last successful POS license validation against update server"),
    )
    pos_license_expires_at = models.DateTimeField(
        null=True, blank=True, help_text=_("When the POS license subscription expires")
    )
    pos_license_status = models.CharField(
        max_length=20,
        choices=[
            ("not_configured", _("Not Configured")),
            ("active", _("Active")),
            ("grace", _("Grace Period")),
            ("expired", _("Expired")),
        ],
        default="not_configured",
        help_text=_("Current POS license status"),
    )

    # Server status
    is_connected = models.BooleanField(
        default=False, help_text=_("Whether we can connect to update server")
    )
    last_connection_attempt = models.DateTimeField(null=True, blank=True)
    last_connection_error = models.TextField(blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Update Server Configuration")
        verbose_name_plural = _("Update Server Configuration")

    def __str__(self):
        return f"Update Server: {self.server_url}"

    def save(self, *args, **kwargs):
        # Ensure only one instance exists (singleton pattern)
        if not self.pk and UpdateServerConfig.objects.exists():
            raise ValueError("Only one UpdateServerConfig instance is allowed")
        return super().save(*args, **kwargs)

    @classmethod
    def get_instance(cls):
        """Get or create the singleton instance"""
        instance, created = cls.objects.get_or_create(pk=1)
        return instance

    def is_jwt_valid(self):
        """Check if current JWT is still valid"""
        if not self.jwt_token or not self.jwt_expires_at:
            return False
        return timezone.now() < self.jwt_expires_at


class PlatformUpdate(models.Model):
    """
    Track platform updates for blue-green deployment.
    Each record represents an attempted or completed platform update.
    """

    STATUS_CHOICES = [
        ("checking", _("Checking for Updates")),
        ("downloading", _("Downloading Package")),
        ("verifying", _("Verifying Package")),
        ("extracting", _("Extracting Files")),
        ("pre_checks", _("Running Pre-Update Checks")),
        ("migrating", _("Running Migrations")),
        ("building", _("Building Container")),
        ("deploying", _("Deploying New Version")),
        ("health_check", _("Running Health Checks")),
        ("switching", _("Switching Traffic")),
        ("completed", _("Update Completed")),
        ("failed", _("Update Failed")),
        ("rolled_back", _("Rolled Back")),
    ]

    # Unique update identifier
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Version tracking
    from_version = models.CharField(max_length=20, help_text=_("Platform version before update"))
    to_version = models.CharField(max_length=20, help_text=_("Target platform version"))
    channel = models.CharField(max_length=20, default="stable", help_text=_("Update channel"))

    # Status tracking
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="checking", db_index=True
    )
    progress_percent = models.IntegerField(
        default=0, help_text=_("Overall update progress (0-100)")
    )
    current_step = models.CharField(
        max_length=100, blank=True, help_text=_("Current step description")
    )

    # Step details for progress UI
    steps = models.JSONField(
        default=list, blank=True, help_text=_("List of update steps with status")
    )
    log_lines = models.JSONField(default=list, blank=True, help_text=_("Recent log output lines"))

    # Package details
    package_checksum = models.CharField(
        max_length=64, blank=True, help_text=_("SHA256 checksum of the downloaded package")
    )
    package_size_bytes = models.BigIntegerField(default=0, help_text=_("Package file size"))
    bytes_downloaded = models.BigIntegerField(default=0, help_text=_("Bytes downloaded so far"))

    # Release info (from update server)
    changelog = models.TextField(blank=True, help_text=_("Changelog for this update"))
    release_notes = models.TextField(blank=True, help_text=_("User-facing release notes"))
    requires_migration = models.BooleanField(
        default=False, help_text=_("Whether database migrations are required")
    )
    migration_estimate_seconds = models.IntegerField(
        default=30, help_text=_("Estimated migration time")
    )
    breaking_changes = models.BooleanField(
        default=False, help_text=_("Whether this update has breaking changes")
    )
    security_update = models.BooleanField(
        default=False, help_text=_("Whether this is a security update")
    )

    # Rollback capability
    rollback_available = models.BooleanField(
        default=False, help_text=_("Whether rollback to previous version is available")
    )
    rollback_version = models.CharField(
        max_length=20, blank=True, help_text=_("Version to rollback to if needed")
    )

    # Error tracking
    error_message = models.TextField(blank=True, help_text=_("Error message if update failed"))
    error_stage = models.CharField(
        max_length=50, blank=True, help_text=_("Stage where error occurred")
    )
    error_traceback = models.TextField(blank=True, help_text=_("Full error traceback"))

    # Timing
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(
        null=True, blank=True, help_text=_("When the update process started")
    )
    completed_at = models.DateTimeField(
        null=True, blank=True, help_text=_("When the update process completed")
    )
    duration_seconds = models.IntegerField(
        null=True, blank=True, help_text=_("Total update duration")
    )
    downtime_seconds = models.IntegerField(
        null=True, blank=True, help_text=_("Actual downtime during update")
    )

    # User tracking
    initiated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="platform_updates",
        help_text=_("Admin who initiated the update"),
    )

    # Celery task tracking
    celery_task_id = models.CharField(
        max_length=255, blank=True, help_text=_("Celery task ID for this update")
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Platform Update")
        verbose_name_plural = _("Platform Updates")
        indexes = [
            models.Index(fields=["status", "-created_at"]),
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return f"v{self.from_version} → v{self.to_version} ({self.get_status_display()})"

    def add_log_line(self, message):
        """Add a log line to the update log"""
        from django.utils import timezone

        timestamp = timezone.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"

        # Keep only last 50 lines
        logs = self.log_lines or []
        logs.append(log_entry)
        self.log_lines = logs[-50:]
        self.save(update_fields=["log_lines"])

    def update_step(self, step_name, status, detail=None):
        """Update a step's status"""
        steps = self.steps or []
        for step in steps:
            if step.get("name") == step_name:
                step["status"] = status
                if detail:
                    step["detail"] = detail
                break
        self.steps = steps
        self.save(update_fields=["steps"])

    def mark_failed(self, error_message, error_stage="", traceback=""):
        """Mark the update as failed"""
        self.status = "failed"
        self.error_message = error_message
        self.error_stage = error_stage
        self.error_traceback = traceback
        self.completed_at = timezone.now()
        if self.started_at:
            delta = self.completed_at - self.started_at
            self.duration_seconds = int(delta.total_seconds())
        self.save()

    def mark_completed(self):
        """Mark the update as completed"""
        self.status = "completed"
        self.progress_percent = 100
        self.completed_at = timezone.now()
        if self.started_at:
            delta = self.completed_at - self.started_at
            self.duration_seconds = int(delta.total_seconds())
        self.save()

    def mark_rolled_back(self, reason=""):
        """Mark the update as rolled back"""
        self.status = "rolled_back"
        self.error_message = reason or self.error_message
        self.completed_at = timezone.now()
        if self.started_at:
            delta = self.completed_at - self.started_at
            self.duration_seconds = int(delta.total_seconds())
        self.save()

    @classmethod
    def get_current_update(cls):
        """Get the currently running update, if any"""
        return cls.objects.filter(
            status__in=[
                "checking",
                "downloading",
                "verifying",
                "extracting",
                "pre_checks",
                "migrating",
                "building",
                "deploying",
                "health_check",
                "switching",
            ]
        ).first()

    @classmethod
    def can_start_update(cls):
        """Check if a new update can be started"""
        return not cls.objects.filter(
            status__in=[
                "checking",
                "downloading",
                "verifying",
                "extracting",
                "pre_checks",
                "migrating",
                "building",
                "deploying",
                "health_check",
                "switching",
            ]
        ).exists()
