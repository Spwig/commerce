"""
Sync Admin Interface

Admin views for Spwig-to-Spwig settings sync and full migration.
Provides wizard-based workflows for both features.
"""

import logging

from django.contrib import admin, messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import path, reverse
from django.utils import timezone
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import SyncConnection, SyncJob
from .sync.category_registry import SYNC_CATEGORIES, get_categories_grouped

logger = logging.getLogger(__name__)

VALID_ROLES = {"production", "staging", "backup", "other"}


@admin.register(SyncConnection)
class SyncConnectionAdmin(admin.ModelAdmin):
    """Admin for managing saved sync connections."""

    list_display = [
        "name",
        "role_badge",
        "remote_url",
        "verified_status",
        "last_sync_display",
        "actions_column",
    ]
    list_filter = ["role", "is_verified"]
    readonly_fields = [
        "id",
        "remote_version",
        "remote_site_name",
        "is_verified",
        "last_verified_at",
        "last_sync_at",
        "created_at",
        "updated_at",
    ]

    def role_badge(self, obj):
        colors = {
            "production": "#f44336",
            "staging": "#2196f3",
            "backup": "#ff9800",
            "other": "#9e9e9e",
        }
        color = colors.get(obj.role, "#9e9e9e")
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 10px; '
            'border-radius: 12px; font-size: 11px; font-weight: 600;">{}</span>',
            color,
            obj.get_role_display(),
        )

    role_badge.short_description = _("Role")

    def verified_status(self, obj):
        if obj.is_verified:
            return format_html('<span style="color: #4caf50;">&#10004; Verified</span>')
        return format_html('<span style="color: #999;">Not verified</span>')

    verified_status.short_description = _("Status")

    def last_sync_display(self, obj):
        if obj.last_sync_at:
            return obj.last_sync_at.strftime("%Y-%m-%d %H:%M")
        return "-"

    last_sync_display.short_description = _("Last Sync")

    def actions_column(self, obj):
        return format_html(
            '<a href="{}" class="button" style="font-size: 11px; padding: 4px 10px;">'
            "Sync Settings</a> ",
            reverse("admin:sync_wizard_step1") + f"?connection={obj.pk}",
        )

    actions_column.short_description = _("Actions")

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(SyncJob)
class SyncJobAdmin(admin.ModelAdmin):
    """Admin for viewing sync/migration job history."""

    list_display = [
        "job_id_display",
        "job_type_badge",
        "direction_display",
        "status_badge",
        "progress_bar",
        "items_summary",
        "created_display",
        "actions_column",
    ]
    list_filter = ["job_type", "status", "direction", "created_at"]
    readonly_fields = [
        "id",
        "connection",
        "created_by",
        "created_at",
        "started_at",
        "completed_at",
        "duration_seconds",
        "diff_preview",
        "rollback_snapshot",
    ]

    change_list_template = "admin/migration/syncjob/change_list.html"

    def has_add_permission(self, request):
        return False

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["title"] = _("Spwig-to-Spwig Sync")
        extra_context["management_tools"] = [
            {
                "title": _("Sync Settings"),
                "url": reverse("admin:sync_wizard_step1"),
                "description": _("Sync settings between staging and production"),
                "icon": "fas fa-sync-alt",
                "class": "addlink",
            },
            {
                "title": _("Full Migration"),
                "url": reverse("admin:fullmig_wizard_step1"),
                "description": _("Migrate entire system to a new installation"),
                "icon": "fas fa-truck-moving",
                "class": "addlink",
            },
            {
                "title": _("Manage Tokens"),
                "url": reverse("admin:sync_token_management"),
                "description": _("Generate and manage sync tokens"),
                "icon": "fas fa-key",
                "class": "viewlink",
            },
        ]

        # Stats
        total = SyncJob.objects.count()
        completed = SyncJob.objects.filter(status="completed").count()
        failed = SyncJob.objects.filter(status="failed").count()
        running = SyncJob.objects.filter(status="running").count()
        extra_context["stats"] = {
            "total": total,
            "completed": completed,
            "failed": failed,
            "running": running,
        }
        extra_context["sync_jobs"] = SyncJob.objects.all().order_by("-created_at")

        return super().changelist_view(request, extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            # Settings Sync Wizard
            path(
                "sync/wizard/step1/",
                self.admin_site.admin_view(self.sync_wizard_step1),
                name="sync_wizard_step1",
            ),
            path(
                "sync/wizard/step2/<uuid:job_id>/",
                self.admin_site.admin_view(self.sync_wizard_step2),
                name="sync_wizard_step2",
            ),
            path(
                "sync/wizard/step3/<uuid:job_id>/",
                self.admin_site.admin_view(self.sync_wizard_step3),
                name="sync_wizard_step3",
            ),
            path(
                "sync/wizard/step4/<uuid:job_id>/",
                self.admin_site.admin_view(self.sync_wizard_step4),
                name="sync_wizard_step4",
            ),
            # Full Migration Wizard
            path(
                "fullmig/wizard/step1/",
                self.admin_site.admin_view(self.fullmig_wizard_step1),
                name="fullmig_wizard_step1",
            ),
            path(
                "fullmig/wizard/step2/<uuid:job_id>/",
                self.admin_site.admin_view(self.fullmig_wizard_step2),
                name="fullmig_wizard_step2",
            ),
            path(
                "fullmig/wizard/step3/<uuid:job_id>/",
                self.admin_site.admin_view(self.fullmig_wizard_step3),
                name="fullmig_wizard_step3",
            ),
            path(
                "fullmig/wizard/step4/<uuid:job_id>/",
                self.admin_site.admin_view(self.fullmig_wizard_step4),
                name="fullmig_wizard_step4",
            ),
            path(
                "fullmig/wizard/step5/<uuid:job_id>/",
                self.admin_site.admin_view(self.fullmig_wizard_step5),
                name="fullmig_wizard_step5",
            ),
            # Shared API endpoints
            path(
                "api/test-connection/",
                self.admin_site.admin_view(self.api_test_connection),
                name="sync_api_test_connection",
            ),
            path(
                "api/sync-progress/<uuid:job_id>/",
                self.admin_site.admin_view(self.api_sync_progress),
                name="sync_api_progress",
            ),
            path(
                "api/start-sync/<uuid:job_id>/",
                self.admin_site.admin_view(self.api_start_sync),
                name="sync_api_start",
            ),
            path(
                "api/rollback/<uuid:job_id>/",
                self.admin_site.admin_view(self.api_rollback),
                name="sync_api_rollback",
            ),
            # Token management
            path(
                "tokens/",
                self.admin_site.admin_view(self.token_management),
                name="sync_token_management",
            ),
        ]
        return custom_urls + urls

    # ========================================================================
    # Display Helpers
    # ========================================================================

    def job_id_display(self, obj):
        short_id = str(obj.id)[:8]
        return format_html(
            '<code style="background: var(--darkened-bg, #f8f9fa); padding: 4px 8px; '
            'border-radius: 4px; font-size: 12px;">{}</code>',
            short_id,
        )

    job_id_display.short_description = _("ID")

    def job_type_badge(self, obj):
        colors = {"settings_sync": "#2196f3", "full_migration": "#9c27b0"}
        icons = {"settings_sync": "fas fa-sync-alt", "full_migration": "fas fa-truck-moving"}
        color = colors.get(obj.job_type, "#666")
        icon = icons.get(obj.job_type, "fas fa-circle")
        return format_html(
            '<div style="display: flex; align-items: center; gap: 6px;">'
            '<i class="{}" style="color: {};"></i>'
            '<span style="font-weight: 500;">{}</span>'
            "</div>",
            icon,
            color,
            obj.get_job_type_display(),
        )

    job_type_badge.short_description = _("Type")

    def direction_display(self, obj):
        icons = {"pull": "&#8592;", "push": "&#8594;"}
        return format_html(
            '<span style="font-size: 14px;">{} {}</span>',
            icons.get(obj.direction, ""),
            obj.get_direction_display(),
        )

    direction_display.short_description = _("Direction")

    def status_badge(self, obj):
        colors = {
            "pending": "#ffa500",
            "previewing": "#9c27b0",
            "awaiting_confirmation": "#ff9800",
            "running": "#2196f3",
            "completed": "#4caf50",
            "failed": "#f44336",
            "rolling_back": "#ff5722",
            "rolled_back": "#607d8b",
            "cancelled": "#999",
        }
        color = colors.get(obj.status, "#999")
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 10px; '
            'border-radius: 12px; font-size: 11px; font-weight: 600;">{}</span>',
            color,
            obj.get_status_display(),
        )

    status_badge.short_description = _("Status")

    def progress_bar(self, obj):
        if obj.status not in ("running", "completed"):
            return "-"
        percent = obj.progress_percent
        color = "#4caf50" if percent == 100 else "#2196f3"
        return format_html(
            '<div style="width: 100px; background: #e0e0e0; height: 18px; '
            'border-radius: 9px; overflow: hidden; position: relative;">'
            '<div style="background: {}; width: {}%; height: 100%;"></div>'
            '<span style="position: absolute; inset: 0; text-align: center; '
            'line-height: 18px; font-size: 11px; font-weight: 600;">'
            "{}%</span></div>",
            color,
            percent,
            percent,
        )

    progress_bar.short_description = _("Progress")

    def items_summary(self, obj):
        if obj.items_total == 0:
            return "-"
        return format_html(
            '<span style="color: #4caf50;">{}</span> / '
            '<span style="color: #f44336;">{}</span> / '
            '<span style="color: #999;">{}</span>',
            obj.items_synced,
            obj.items_failed,
            obj.items_total,
        )

    items_summary.short_description = _("Synced/Failed/Total")

    def created_display(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M")

    created_display.short_description = _("Created")

    def actions_column(self, obj):
        buttons = []
        if obj.status == "running":
            buttons.append(
                format_html(
                    '<a href="{}" class="button" style="font-size: 11px;">View Progress</a>',
                    reverse("admin:sync_wizard_step4", args=[obj.pk])
                    if obj.job_type == "settings_sync"
                    else reverse("admin:fullmig_wizard_step4", args=[obj.pk]),
                )
            )
        if obj.is_rollbackable:
            buttons.append(
                format_html(
                    '<button type="button" class="button js-rollback-btn" '
                    'style="font-size: 11px; background: #ff5722; color: white;" '
                    'data-rollback-url="{}">Rollback</button>',
                    reverse("admin:sync_api_rollback", args=[obj.pk]),
                )
            )
        return format_html(" ".join(str(b) for b in buttons)) if buttons else "-"

    actions_column.short_description = _("Actions")

    # ========================================================================
    # Settings Sync Wizard Views
    # ========================================================================

    def sync_wizard_step1(self, request):
        """Step 1: Connection setup."""
        connections = SyncConnection.objects.all().order_by("-updated_at")
        preselected_id = request.GET.get("connection")

        if request.method == "POST":
            # Create or reuse connection
            connection_id = request.POST.get("connection_id")
            if connection_id:
                connection = get_object_or_404(SyncConnection, pk=connection_id)
                # Update fields if provided, but keep existing token if none given
                connection.name = request.POST.get("name", connection.name)
                connection.remote_url = request.POST.get("remote_url", "") or connection.remote_url
                new_token = request.POST.get("auth_token", "").strip()
                if new_token:
                    connection.auth_token = new_token
                role = request.POST.get("role", connection.role)
                connection.role = role if role in VALID_ROLES else connection.role
            else:
                auth_token = request.POST.get("auth_token", "").strip()
                if not auth_token:
                    messages.error(request, _("Sync token is required for new connections."))
                    return redirect(reverse("admin:sync_wizard_step1"))
                connection = SyncConnection(created_by=request.user)
                connection.name = request.POST.get("name", "New Connection")
                connection.remote_url = request.POST.get("remote_url", "")
                connection.auth_token = auth_token
                role = request.POST.get("role", "other")
                connection.role = role if role in VALID_ROLES else "other"
            connection.save()

            # Create SyncJob
            job = SyncJob.objects.create(
                job_type="settings_sync",
                direction="pull",
                connection=connection,
                created_by=request.user,
            )

            return redirect(reverse("admin:sync_wizard_step2", args=[job.pk]))

        return render(
            request,
            "admin/migration/sync/step1_connection.html",
            {
                **self.admin_site.each_context(request),
                "title": _("Settings Sync - Connection"),
                "opts": self.model._meta,
                "connections": connections,
                "preselected_id": preselected_id,
                "current_step": 1,
                "total_steps": 4,
                "wizard_type": "sync",
            },
        )

    def sync_wizard_step2(self, request, job_id):
        """Step 2: Select categories and direction."""
        job = get_object_or_404(SyncJob, pk=job_id)
        grouped_categories = get_categories_grouped("settings_sync")

        if request.method == "POST":
            selected = request.POST.getlist("categories")
            valid_keys = set(SYNC_CATEGORIES.keys())
            selected = [c for c in selected if c in valid_keys]

            if not selected:
                messages.error(request, _("Please select at least one category to sync."))
                return redirect(reverse("admin:sync_wizard_step2", args=[job.pk]))

            direction = request.POST.get("direction", "pull")
            if direction not in ("pull", "push"):
                direction = "pull"
            sync_mode = request.POST.get("sync_mode", "additive")
            if sync_mode not in ("additive", "mirror"):
                sync_mode = "additive"

            job.direction = direction
            job.sync_mode = sync_mode
            job.selected_categories = selected
            job.save(update_fields=["direction", "sync_mode", "selected_categories"])

            return redirect(reverse("admin:sync_wizard_step3", args=[job.pk]))

        return render(
            request,
            "admin/migration/sync/step2_categories.html",
            {
                **self.admin_site.each_context(request),
                "title": _("Settings Sync - Select Categories"),
                "opts": self.model._meta,
                "job": job,
                "grouped_categories": grouped_categories,
                "current_step": 2,
                "total_steps": 4,
                "wizard_type": "sync",
            },
        )

    def sync_wizard_step3(self, request, job_id):
        """Step 3: Preview diff and confirm."""
        job = get_object_or_404(SyncJob, pk=job_id)

        if request.method == "POST":
            # Production confirmation
            if job.connection.is_production and job.direction == "push":
                if not request.POST.get("production_confirmed"):
                    messages.error(request, _("You must confirm production overwrite."))
                    return redirect(reverse("admin:sync_wizard_step3", args=[job.pk]))
                job.production_confirmed = True
                job.save(update_fields=["production_confirmed"])

            return redirect(reverse("admin:sync_wizard_step4", args=[job.pk]))

        # Generate preview if not already done
        if not job.diff_preview:
            try:
                from .sync.orchestrator import SyncOrchestrator

                orchestrator = SyncOrchestrator(job)
                orchestrator.generate_preview()
                job.refresh_from_db()
            except Exception as e:
                logger.error(f"Preview generation failed: {e}")
                messages.error(
                    request,
                    _("Preview generation failed. Please check the connection and try again."),
                )

        return render(
            request,
            "admin/migration/sync/step3_preview.html",
            {
                **self.admin_site.each_context(request),
                "title": _("Settings Sync - Preview Changes"),
                "opts": self.model._meta,
                "job": job,
                "diff": job.diff_preview,
                "is_production": job.connection.is_production and job.direction == "push",
                "current_step": 3,
                "total_steps": 4,
                "wizard_type": "sync",
            },
        )

    def sync_wizard_step4(self, request, job_id):
        """Step 4: Progress and results."""
        job = get_object_or_404(SyncJob, pk=job_id)

        return render(
            request,
            "admin/migration/sync/step4_progress.html",
            {
                **self.admin_site.each_context(request),
                "title": _("Settings Sync - Progress"),
                "opts": self.model._meta,
                "job": job,
                "steps": job.steps.all().order_by("id"),
                "current_step": 4,
                "total_steps": 4,
                "wizard_type": "sync",
            },
        )

    # ========================================================================
    # Full Migration Wizard Views
    # ========================================================================

    def fullmig_wizard_step1(self, request):
        """Step 1: Connection and compatibility check."""
        connections = SyncConnection.objects.all().order_by("-updated_at")

        if request.method == "POST":
            connection_id = request.POST.get("connection_id")
            if connection_id:
                connection = get_object_or_404(SyncConnection, pk=connection_id)
                connection.name = request.POST.get("name", connection.name)
                connection.remote_url = request.POST.get("remote_url", "") or connection.remote_url
                new_token = request.POST.get("auth_token", "").strip()
                if new_token:
                    connection.auth_token = new_token
                role = request.POST.get("role", connection.role)
                connection.role = role if role in VALID_ROLES else connection.role
            else:
                auth_token = request.POST.get("auth_token", "").strip()
                if not auth_token:
                    messages.error(request, _("Sync token is required for new connections."))
                    return redirect(reverse("admin:fullmig_wizard_step1"))
                connection = SyncConnection(created_by=request.user)
                connection.name = request.POST.get("name", "Migration Source")
                connection.remote_url = request.POST.get("remote_url", "")
                connection.auth_token = auth_token
                role = request.POST.get("role", "other")
                connection.role = role if role in VALID_ROLES else "other"
            connection.save()

            job = SyncJob.objects.create(
                job_type="full_migration",
                direction="pull",
                connection=connection,
                created_by=request.user,
            )

            return redirect(reverse("admin:fullmig_wizard_step2", args=[job.pk]))

        return render(
            request,
            "admin/migration/fullmig/step1_connection.html",
            {
                **self.admin_site.each_context(request),
                "title": _("Full Migration - Connection"),
                "opts": self.model._meta,
                "connections": connections,
                "current_step": 1,
                "total_steps": 5,
                "wizard_type": "fullmig",
            },
        )

    def fullmig_wizard_step2(self, request, job_id):
        """Step 2: Migration scope selection."""
        job = get_object_or_404(SyncJob, pk=job_id)
        grouped_categories = get_categories_grouped("full_migration")

        if request.method == "POST":
            selected = request.POST.getlist("categories")
            valid_keys = set(SYNC_CATEGORIES.keys())
            selected = [c for c in selected if c in valid_keys]

            if not selected:
                messages.error(request, _("Please select at least one category to migrate."))
                return redirect(reverse("admin:fullmig_wizard_step2", args=[job.pk]))

            job.selected_categories = selected
            job.save(update_fields=["selected_categories"])
            return redirect(reverse("admin:fullmig_wizard_step3", args=[job.pk]))

        return render(
            request,
            "admin/migration/fullmig/step2_scope.html",
            {
                **self.admin_site.each_context(request),
                "title": _("Full Migration - Select Scope"),
                "opts": self.model._meta,
                "job": job,
                "grouped_categories": grouped_categories,
                "current_step": 2,
                "total_steps": 5,
                "wizard_type": "fullmig",
            },
        )

    def fullmig_wizard_step3(self, request, job_id):
        """Step 3: Pre-flight checks."""
        job = get_object_or_404(SyncJob, pk=job_id)

        # Run compatibility check
        compatibility = {}
        try:
            from .sync.full_migration_orchestrator import FullMigrationOrchestrator

            orchestrator = FullMigrationOrchestrator(job)
            compatibility = orchestrator.check_compatibility()
        except Exception as e:
            logger.error(f"Compatibility check failed: {e}")
            messages.error(
                request,
                _("Compatibility check failed. Please verify the connection and try again."),
            )

        if request.method == "POST":
            return redirect(reverse("admin:fullmig_wizard_step4", args=[job.pk]))

        return render(
            request,
            "admin/migration/fullmig/step3_preflight.html",
            {
                **self.admin_site.each_context(request),
                "title": _("Full Migration - Pre-flight Check"),
                "opts": self.model._meta,
                "job": job,
                "compatibility": compatibility,
                "current_step": 3,
                "total_steps": 5,
                "wizard_type": "fullmig",
            },
        )

    def fullmig_wizard_step4(self, request, job_id):
        """Step 4: Migration progress."""
        job = get_object_or_404(SyncJob, pk=job_id)

        return render(
            request,
            "admin/migration/fullmig/step4_progress.html",
            {
                **self.admin_site.each_context(request),
                "title": _("Full Migration - Progress"),
                "opts": self.model._meta,
                "job": job,
                "steps": job.steps.all().order_by("id"),
                "current_step": 4,
                "total_steps": 5,
                "wizard_type": "fullmig",
            },
        )

    def fullmig_wizard_step5(self, request, job_id):
        """Step 5: Results and next steps."""
        job = get_object_or_404(SyncJob, pk=job_id)

        return render(
            request,
            "admin/migration/fullmig/step5_results.html",
            {
                **self.admin_site.each_context(request),
                "title": _("Full Migration - Results"),
                "opts": self.model._meta,
                "job": job,
                "steps": job.steps.all().order_by("id"),
                "current_step": 5,
                "total_steps": 5,
                "wizard_type": "fullmig",
            },
        )

    # ========================================================================
    # API Endpoints (AJAX)
    # ========================================================================

    def api_test_connection(self, request):
        """Test connection to a remote Spwig instance."""
        if request.method != "POST":
            return JsonResponse({"error": "POST required"}, status=405)

        url = request.POST.get("remote_url", "")
        token = request.POST.get("auth_token", "")
        connection_id = request.POST.get("connection_id", "")

        # For saved connections, use stored token if none provided
        if connection_id and not token:
            try:
                saved_conn = SyncConnection.objects.get(pk=connection_id)
                token = saved_conn.auth_token
                if not url:
                    url = saved_conn.remote_url
            except SyncConnection.DoesNotExist:
                return JsonResponse({"error": "Saved connection not found"}, status=404)

        if not url or not token:
            return JsonResponse({"error": "URL and token are required"}, status=400)

        from .sync.client import SpwigSyncClient, SyncClientError

        # Create a temporary connection object
        temp_connection = SyncConnection(remote_url=url, auth_token=token)
        client = SpwigSyncClient(temp_connection)

        try:
            info = client.test_connection()
            return JsonResponse(
                {
                    "success": True,
                    "version": info.get("version", "unknown"),
                    "site_name": info.get("site_name", "Unknown"),
                    "categories": len(info.get("categories", [])),
                }
            )
        except SyncClientError as e:
            return JsonResponse({"success": False, "error": str(e)})
        except Exception as e:
            logger.error(f"Connection test failed unexpectedly: {e}")
            return JsonResponse(
                {
                    "success": False,
                    "error": "An unexpected error occurred while testing the connection.",
                }
            )

    def api_sync_progress(self, request, job_id):
        """Get real-time progress for a sync job."""
        job = get_object_or_404(SyncJob, pk=job_id)
        # Cursor-based log retrieval to avoid re-sending entries
        try:
            log_cursor = max(0, int(request.GET.get("log_cursor", 0)))
        except (ValueError, TypeError):
            log_cursor = 0

        steps = []
        for step in job.steps.all().order_by("id"):
            config = SYNC_CATEGORIES.get(step.category, {})
            step_data = {
                "category": step.category,
                "label": str(config.get("label", step.category)),
                "status": step.status,
                "items_synced": step.items_synced,
                "items_skipped": step.items_skipped,
                "items_failed": step.items_failed,
                "items_total": step.items_total,
                "progress": step.progress_percent,
                "error_message": step.error_message,
            }
            if step.extra_data:
                step_data["extra_data"] = step.extra_data
            steps.append(step_data)

        # Compute elapsed time
        elapsed_seconds = None
        started_at_iso = None
        if job.started_at:
            started_at_iso = job.started_at.isoformat()
            if job.completed_at:
                elapsed_seconds = int((job.completed_at - job.started_at).total_seconds())
            else:
                elapsed_seconds = int((timezone.now() - job.started_at).total_seconds())

        # Return activity log entries from cursor onwards
        full_log = job.activity_log or []
        new_log_entries = full_log[log_cursor:]

        return JsonResponse(
            {
                "status": job.status,
                "progress_percent": job.progress_percent,
                "current_step": job.current_step,
                "items_synced": job.items_synced,
                "items_skipped": job.items_skipped,
                "items_failed": job.items_failed,
                "items_total": job.items_total,
                "steps": steps,
                "is_rollbackable": job.is_rollbackable,
                "error_summary": job.error_summary,
                "started_at": started_at_iso,
                "elapsed_seconds": elapsed_seconds,
                "activity_log": new_log_entries,
                "log_cursor": len(full_log),
            }
        )

    def api_start_sync(self, request, job_id):
        """Start a sync/migration job (dispatches Celery task)."""
        if request.method != "POST":
            return JsonResponse({"error": "POST required"}, status=405)

        job = get_object_or_404(SyncJob, pk=job_id)

        if job.status not in ("pending", "awaiting_confirmation"):
            return JsonResponse({"error": f"Cannot start job in status: {job.status}"}, status=400)

        from .sync.tasks import execute_full_migration, execute_settings_sync

        if job.job_type == "settings_sync":
            execute_settings_sync.delay(str(job.pk))
        else:
            execute_full_migration.delay(str(job.pk))

        return JsonResponse({"status": "started", "job_id": str(job.pk)})

    def api_rollback(self, request, job_id):
        """Rollback a completed sync job."""
        if request.method != "POST":
            return JsonResponse({"error": "POST required"}, status=405)

        job = get_object_or_404(SyncJob, pk=job_id)

        if not job.is_rollbackable:
            return JsonResponse({"error": "This job cannot be rolled back"}, status=400)

        from .sync.tasks import rollback_sync

        rollback_sync.delay(str(job.pk))

        return JsonResponse({"status": "rolling_back", "job_id": str(job.pk)})

    # ========================================================================
    # Token Management
    # ========================================================================

    def token_management(self, request):
        """Manage sync tokens."""
        from core.models import APIToken
        from core.utils.api_tokens import create_api_token, get_active_tokens_by_type, revoke_token

        if request.method == "POST":
            action = request.POST.get("action")
            if action == "generate":
                name = request.POST.get("name", "Sync Token")
                token = create_api_token(
                    name=name,
                    token_type=APIToken.TOKEN_TYPE_SYNC,
                    description="Generated for Spwig-to-Spwig sync",
                    created_by=request.user,
                )
                messages.success(
                    request,
                    _("Token generated. Copy it now — it will not be shown again:")
                    + f" {token.token}",
                )
            elif action == "revoke":
                token_id = request.POST.get("token_id")
                if token_id:
                    try:
                        revoke_token(int(token_id))
                        messages.success(request, _("Token revoked."))
                    except (ValueError, TypeError):
                        messages.error(request, _("Invalid token ID."))

        tokens = get_active_tokens_by_type(APIToken.TOKEN_TYPE_SYNC)

        return render(
            request,
            "admin/migration/sync/token_management.html",
            {
                **self.admin_site.each_context(request),
                "title": _("Sync Token Management"),
                "opts": self.model._meta,
                "tokens": tokens,
            },
        )
