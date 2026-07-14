import json
import os
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib import admin, messages
from django.http import FileResponse, HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render
from django.urls import path, reverse
from django.utils import timezone
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import (
    AccessLog,
    BackupSchedule,
    DatabaseBackup,
    DeploymentBackup,
    FileOperation,
    LogEntry,
    LogViewerSettings,
    QueryHistory,
    RemoteStorageDestination,
    SystemMetrics,
    SystemRestore,
    SystemStatus,
    SystemUpgrade,
)
from .services import SystemStatusService
from .shop_dashboard import ShopDashboardAdmin
from .utils import DatabaseManager, DataExporter, FileManager, SystemMonitor
from .views.oauth import storage_oauth_callback, storage_oauth_initiate
from .views.wizard import (
    StorageWizardStep1View,
    StorageWizardStep2View,
    StorageWizardStep3View,
    delete_destination_view,
    retest_destination_view,
    storage_destinations_view,
    test_connection_view,
)


def _check_not_hosted(request):
    """Return HttpResponseForbidden if running on a Spwig-hosted installation."""
    from core.license import get_license_manager

    if get_license_manager().is_spwig_hosted():
        return HttpResponseForbidden(
            "This feature is not available for Spwig-hosted installations."
        )
    return None


@admin.register(DatabaseBackup)
class DatabaseBackupAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "backup_type",
        "file_size_display",
        "status",
        "created_at",
        "created_by",
    ]
    list_filter = ["status", "backup_type", "compression", "created_at"]
    search_fields = ["name", "description"]
    readonly_fields = ["file_path", "file_size", "created_at", "error_message"]
    change_list_template = "admin/management/change_list.html"

    def has_add_permission(self, request):
        return False  # Use custom backup creation interface

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["title"] = _("Database Backups")
        extra_context["management_tools"] = [
            {
                "title": _("Create New Backup"),
                "url": reverse("admin:management_backup_create"),
                "description": _("Create a new database backup"),
                "class": "addlink",
                "icon": "fas fa-save",
            }
        ]
        return super().changelist_view(request, extra_context)

    def file_size_display(self, obj):
        if obj.file_size:
            size = obj.file_size
            for unit in ["B", "KB", "MB", "GB"]:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
            return f"{size:.1f} TB"
        return "Unknown"

    file_size_display.short_description = _("File Size")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "create-backup/",
                self.admin_site.admin_view(self.create_backup_view),
                name="management_backup_create",
            ),
            path(
                "download/<int:backup_id>/",
                self.admin_site.admin_view(self.download_backup),
                name="management_backup_download",
            ),
        ]
        return custom_urls + urls

    def create_backup_view(self, request):
        if request.method == "POST":
            name = request.POST.get("name")
            description = request.POST.get("description", "")
            backup_type = request.POST.get("backup_type", "full")
            compression = request.POST.get("compression", "gzip")

            # Create backup
            result = DatabaseManager.create_backup(name, backup_type, compression)

            if result["success"]:
                DatabaseBackup.objects.create(
                    name=name,
                    description=description,
                    file_path=result["file_path"],
                    file_size=result["file_size"],
                    backup_type=backup_type,
                    compression=compression,
                    created_by=request.user,
                    status="completed",
                )
                messages.success(request, _("Backup '{}' created successfully!").format(name))
            else:
                DatabaseBackup.objects.create(
                    name=name,
                    description=description,
                    backup_type=backup_type,
                    compression=compression,
                    created_by=request.user,
                    status="failed",
                    error_message=result["error"],
                )
                messages.error(request, _("Backup failed: {}").format(result["error"]))

            return redirect("admin:management_databasebackup_changelist")

        return render(
            request,
            "admin/management/create_backup.html",
            {
                "title": _("Create Database Backup"),
                "opts": self.model._meta,
            },
        )

    def download_backup(self, request, backup_id):
        try:
            backup = DatabaseBackup.objects.get(id=backup_id)
            if backup.file_path and os.path.exists(backup.file_path):
                return FileResponse(
                    open(backup.file_path, "rb"),
                    content_type="application/octet-stream",
                    as_attachment=True,
                    filename=os.path.basename(backup.file_path),
                )
            else:
                messages.error(request, _("Backup file not found."))
        except DatabaseBackup.DoesNotExist:
            messages.error(request, _("Backup not found."))

        return redirect("admin:management_databasebackup_changelist")


@admin.register(QueryHistory)
class QueryHistoryAdmin(admin.ModelAdmin):
    list_display = [
        "query_preview",
        "user",
        "executed_at",
        "execution_time",
        "rows_affected",
        "success",
    ]
    list_filter = ["success", "executed_at", "user"]
    search_fields = ["query", "user__username"]
    readonly_fields = [
        "query",
        "executed_at",
        "execution_time",
        "rows_affected",
        "success",
        "error_message",
    ]
    change_list_template = "admin/management/change_list.html"

    def has_add_permission(self, request):
        return False  # Queries are added automatically through the query runner

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["title"] = _("Query History")
        extra_context["management_tools"] = [
            {
                "title": _("Database Browser"),
                "url": reverse("admin:management_database_browser"),
                "description": _("Browse database tables and data"),
                "class": "addlink",
                "icon": "fas fa-database",
            },
            {
                "title": _("SQL Query Runner"),
                "url": reverse("admin:management_query_runner"),
                "description": _("Execute SQL queries interactively"),
                "class": "viewlink",
                "icon": "fas fa-terminal",
            },
        ]
        return super().changelist_view(request, extra_context)

    def query_preview(self, obj):
        preview = obj.query[:100] + "..." if len(obj.query) > 100 else obj.query
        return format_html('<code class="mgmt-code-preview">{}</code>', preview)

    query_preview.short_description = _("Query")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "query-runner/",
                self.admin_site.admin_view(self.query_runner_view),
                name="management_query_runner",
            ),
            path(
                "database-browser/",
                self.admin_site.admin_view(self.database_browser_view),
                name="management_database_browser",
            ),
            path(
                "browse-table/<str:table_name>/",
                self.admin_site.admin_view(self.browse_table_view),
                name="management_browse_table",
            ),
            path(
                "execute-query/",
                self.admin_site.admin_view(self.execute_query),
                name="management_execute_query",
            ),
        ]
        return custom_urls + urls

    def query_runner_view(self, request):
        hosted = _check_not_hosted(request)
        if hosted:
            return hosted
        recent_queries = QueryHistory.objects.filter(user=request.user).order_by("-executed_at")[
            :10
        ]
        return render(
            request,
            "admin/management/query_runner.html",
            {
                "title": _("SQL Query Runner"),
                "opts": self.model._meta,
                "recent_queries": recent_queries,
            },
        )

    def execute_query(self, request):
        hosted = _check_not_hosted(request)
        if hosted:
            return hosted
        if request.method != "POST":
            return JsonResponse({"success": False, "error": "POST method required"}, status=405)

        query = request.POST.get("query", "").strip()
        if not query:
            return JsonResponse({"success": False, "error": _("No query provided")})

        # Execute query (read-only to prevent DML/DDL from admin UI)
        result = DatabaseManager.execute_query(query, read_only=True)

        # Save to history
        QueryHistory.objects.create(
            query=query,
            user=request.user,
            execution_time=result["execution_time"],
            rows_affected=result.get("row_count", result.get("rows_affected", 0)),
            success=result["success"],
            error_message=result.get("error", ""),
        )

        return JsonResponse(result)

    def database_browser_view(self, request):
        """Database browser with table listing"""
        hosted = _check_not_hosted(request)
        if hosted:
            return hosted
        tables = DatabaseManager.get_table_list()
        db_info = DatabaseManager.get_database_info()

        context = {
            "title": _("Database Browser"),
            "opts": self.model._meta,
            "tables": tables,
            "db_info": db_info,
            "has_permission": True,
            "user": request.user,
            "site_url": getattr(settings, "SITE_URL", "/"),
            "site_title": self.admin_site.site_title,
            "site_header": self.admin_site.site_header,
        }

        return render(request, "admin/management/database_browser.html", context)

    @staticmethod
    def _validate_table_name(table_name):
        """Validate table_name exists in public schema to prevent SQL injection."""
        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM information_schema.tables "
                "WHERE table_schema = 'public' AND table_name = %s",
                [table_name],
            )
            return cursor.fetchone() is not None

    def browse_table_view(self, request, table_name):
        """Browse specific table data"""
        hosted = _check_not_hosted(request)
        if hosted:
            return hosted
        if not self._validate_table_name(table_name):
            messages.error(request, _("Invalid table name."))
            return redirect("admin:management_database_browser")

        from django.db import connection

        safe_name = connection.ops.quote_name(table_name)

        page = int(request.GET.get("page", 1))
        limit = 50
        offset = (page - 1) * limit

        # Get table data with pagination
        query = f"SELECT * FROM {safe_name} LIMIT {limit} OFFSET {offset}"
        result = DatabaseManager.execute_query(query)

        # If no rows but query was successful, get column info with a LIMIT 0 query
        if result["success"] and not result.get("rows"):
            column_query = f"SELECT * FROM {safe_name} LIMIT 0"
            column_result = DatabaseManager.execute_query(column_query)
            if column_result["success"] and column_result.get("columns"):
                result["columns"] = column_result["columns"]

        # Get total count
        count_query = f"SELECT COUNT(*) as total FROM {safe_name}"
        count_result = DatabaseManager.execute_query(count_query)
        total_rows = count_result["rows"][0][0] if count_result["success"] else 0

        # Calculate pagination info
        total_pages = (total_rows + limit - 1) // limit
        has_previous = page > 1
        has_next = page < total_pages

        # Calculate pagination display values
        start_row = (page - 1) * limit + 1
        end_row = min(page * limit, total_rows)

        context = {
            "title": _("Browse Table: {}").format(table_name),
            "opts": self.model._meta,
            "table_name": table_name,
            "result": result,
            "total_rows": total_rows,
            "page": page,
            "total_pages": total_pages,
            "has_previous": has_previous,
            "has_next": has_next,
            "previous_page": page - 1 if has_previous else None,
            "next_page": page + 1 if has_next else None,
            "start_row": start_row,
            "end_row": end_row,
            "has_permission": True,
            "user": request.user,
            "site_url": getattr(settings, "SITE_URL", "/"),
            "site_title": self.admin_site.site_title,
            "site_header": self.admin_site.site_header,
        }

        return render(request, "admin/management/browse_table.html", context)


@admin.register(SystemMetrics)
class SystemMetricsAdmin(admin.ModelAdmin):
    list_display = ["timestamp", "cpu_percent", "memory_percent", "disk_percent", "active_sessions"]
    list_filter = ["timestamp"]
    readonly_fields = [field.name for field in SystemMetrics._meta.fields]
    change_list_template = "admin/management/change_list.html"

    def has_add_permission(self, request):
        return False  # Metrics are collected automatically

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["title"] = _("System Metrics")
        extra_context["management_tools"] = [
            {
                "title": _("Shop Dashboard"),
                "url": reverse("admin:management_shop_dashboard"),
                "description": _("Business metrics and analytics for your shop"),
                "class": "addlink",
                "icon": "fas fa-chart-pie",
            },
            {
                "title": _("System Dashboard"),
                "url": reverse("admin:management_system_dashboard"),
                "description": _("Real-time system monitoring with charts"),
                "class": "viewlink",
                "icon": "fas fa-server",
            },
            {
                "title": _("Collect Metrics"),
                "url": reverse("admin:management_collect_metrics"),
                "description": _("Manually collect current system metrics"),
                "class": "viewlink",
                "icon": "fas fa-chart-bar",
            },
        ]
        return super().changelist_view(request, extra_context)

    def get_urls(self):
        urls = super().get_urls()

        # Create instance of ShopDashboardAdmin for delegation
        shop_dashboard = ShopDashboardAdmin(SystemMetrics, self.admin_site)

        custom_urls = [
            path(
                "shop-dashboard/",
                self.admin_site.admin_view(shop_dashboard.shop_dashboard_view),
                name="management_shop_dashboard",
            ),
            path(
                "shop-dashboard-api/",
                self.admin_site.admin_view(shop_dashboard.shop_dashboard_api),
                name="management_shop_dashboard_api",
            ),
            path(
                "shop-dashboard/geography-cities/<str:country_code>/",
                self.admin_site.admin_view(shop_dashboard.get_geography_cities),
                name="management_geography_cities",
            ),
            path(
                "dashboard/",
                self.admin_site.admin_view(self.dashboard_view),
                name="management_system_dashboard",
            ),
            path(
                "metrics-api/",
                self.admin_site.admin_view(self.metrics_api),
                name="management_metrics_api",
            ),
            path(
                "collect-metrics/",
                self.admin_site.admin_view(self.collect_metrics),
                name="management_collect_metrics",
            ),
            # Deployment Dashboard URLs
            path(
                "deployment-status/",
                self.admin_site.admin_view(self.deployment_status_api),
                name="management_deployment_status",
            ),
            path(
                "run-diagnostics/",
                self.admin_site.admin_view(self.run_diagnostics_view),
                name="management_run_diagnostics",
            ),
            path(
                "toggle-maintenance/",
                self.admin_site.admin_view(self.toggle_maintenance_view),
                name="management_toggle_maintenance",
            ),
            # Full Backup URLs
            path(
                "create-full-backup/",
                self.admin_site.admin_view(self.create_full_backup_view),
                name="management_create_full_backup",
            ),
            path(
                "backup-progress/<int:backup_id>/",
                self.admin_site.admin_view(self.backup_progress_api),
                name="management_backup_progress",
            ),
            path(
                "backup-schedule/",
                self.admin_site.admin_view(self.backup_schedule_view),
                name="management_backup_schedule",
            ),
            # Restore URLs
            path(
                "restore/",
                self.admin_site.admin_view(self.restore_list_view),
                name="management_restore",
            ),
            path(
                "restore/<int:backup_id>/",
                self.admin_site.admin_view(self.restore_confirm_view),
                name="management_restore_confirm",
            ),
            path(
                "restore/<int:backup_id>/execute/",
                self.admin_site.admin_view(self.restore_execute_view),
                name="management_restore_execute",
            ),
            path(
                "restore-progress/<int:restore_id>/",
                self.admin_site.admin_view(self.restore_progress_api),
                name="management_restore_progress",
            ),
            # Upgrade URLs
            path(
                "check-updates/",
                self.admin_site.admin_view(self.check_updates_view),
                name="management_check_updates",
            ),
            path(
                "upgrade/", self.admin_site.admin_view(self.upgrade_view), name="management_upgrade"
            ),
            path(
                "upgrade/start/",
                self.admin_site.admin_view(self.upgrade_start_view),
                name="management_upgrade_start",
            ),
            path(
                "upgrade/<int:upgrade_id>/execute/",
                self.admin_site.admin_view(self.upgrade_execute_view),
                name="management_upgrade_execute",
            ),
            path(
                "upgrade-progress/<int:upgrade_id>/",
                self.admin_site.admin_view(self.upgrade_progress_api),
                name="management_upgrade_progress",
            ),
            # Remote Storage URLs
            path(
                "remote-storage/",
                self.admin_site.admin_view(storage_destinations_view),
                name="management_storage_destinations",
            ),
            path(
                "remote-storage/add/step1/",
                self.admin_site.admin_view(StorageWizardStep1View.as_view()),
                name="management_storage_wizard_step1",
            ),
            path(
                "remote-storage/add/step2/",
                self.admin_site.admin_view(StorageWizardStep2View.as_view()),
                name="management_storage_wizard_step2",
            ),
            path(
                "remote-storage/add/step3/",
                self.admin_site.admin_view(StorageWizardStep3View.as_view()),
                name="management_storage_wizard_step3",
            ),
            path(
                "remote-storage/test-connection/",
                self.admin_site.admin_view(test_connection_view),
                name="management_storage_test_connection",
            ),
            path(
                "remote-storage/delete/<uuid:destination_id>/",
                self.admin_site.admin_view(delete_destination_view),
                name="management_storage_delete",
            ),
            path(
                "remote-storage/retest/<uuid:destination_id>/",
                self.admin_site.admin_view(retest_destination_view),
                name="management_storage_retest",
            ),
            path(
                "remote-storage/oauth/initiate/",
                self.admin_site.admin_view(storage_oauth_initiate),
                name="management_storage_oauth_initiate",
            ),
            path(
                "remote-storage/oauth/callback/",
                storage_oauth_callback,
                name="management_storage_oauth_callback",
            ),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        hosted = _check_not_hosted(request)
        if hosted:
            return hosted
        # Get recent metrics
        recent_metrics = SystemMetrics.objects.order_by("-timestamp")[:100]
        current_metrics = SystemMonitor.get_system_metrics()

        # Get deployment status - refresh if data is stale or never collected
        system_status = SystemStatus.get_instance()

        # Check if status data needs refresh (stale if > 2 minutes old or never collected)
        needs_refresh = False
        if system_status.checked_at:
            age_seconds = (timezone.now() - system_status.checked_at).total_seconds()
            needs_refresh = age_seconds > 120  # Refresh if older than 2 minutes
        else:
            needs_refresh = True  # Never collected

        # Also refresh if all services show unhealthy (likely never properly collected)
        if (
            not needs_refresh
            and not system_status.db_healthy
            and not system_status.redis_healthy
            and not system_status.celery_healthy
        ):
            needs_refresh = True

        if needs_refresh:
            try:
                from .services import SystemStatusService

                status_data = SystemStatusService.collect_all_status()
                SystemStatusService.update_system_status_model(status_data)
                # Refresh the instance to get updated data
                system_status.refresh_from_db()
            except Exception as e:
                # Log but don't fail the dashboard
                import logging

                logger = logging.getLogger(__name__)
                logger.warning(f"Failed to refresh system status: {e}")

        # Get recent backups
        recent_backups = DeploymentBackup.objects.order_by("-created_at")[:5]
        last_backup = recent_backups.first() if recent_backups else None

        # Get backup schedule
        backup_schedule = BackupSchedule.objects.first()

        # Get running operations
        running_backup = DeploymentBackup.objects.filter(
            status__in=["pending", "running", "compressing", "encrypting", "uploading"]
        ).first()
        running_restore = SystemRestore.objects.filter(
            status__in=[
                "pending",
                "backup",
                "downloading",
                "restoring_db",
                "restoring_media",
                "restoring_config",
            ]
        ).first()
        running_upgrade = SystemUpgrade.objects.filter(
            status__in=[
                "pending",
                "preflight",
                "backup",
                "draining",
                "maintenance",
                "pulling",
                "upgrading",
                "migrating",
            ]
        ).first()

        # Remote storage destinations
        remote_destinations = RemoteStorageDestination.objects.filter(is_active=True)

        # Hotfix status
        hotfix_status = {}
        try:
            from component_updates.services import PlatformUpdateService

            hotfix_status = PlatformUpdateService().get_hotfix_status()
        except Exception:
            pass

        return render(
            request,
            "admin/management/system_dashboard.html",
            {
                "title": _("System Dashboard"),
                "opts": self.model._meta,
                "current_metrics": current_metrics,
                "recent_metrics": recent_metrics[:10],
                # Deployment context
                "system_status": system_status,
                "recent_backups": recent_backups,
                "last_backup": last_backup,
                "backup_schedule": backup_schedule,
                "running_backup": running_backup,
                "running_restore": running_restore,
                "running_upgrade": running_upgrade,
                "remote_destinations": remote_destinations,
                "hotfix_status": hotfix_status,
            },
        )

    def metrics_api(self, request):
        hosted = _check_not_hosted(request)
        if hosted:
            return hosted
        try:
            hours = int(request.GET.get("hours", 24))
        except (ValueError, TypeError):
            hours = 24
        hours = max(1, min(hours, 168))
        since = timezone.now() - timedelta(hours=hours)

        # Get current system metrics in real time
        from .utils import SystemMonitor

        current_metrics_raw = SystemMonitor.get_system_metrics()

        # Format current metrics for the dashboard
        def format_bytes(bytes_val):
            """Format bytes into human readable format"""
            for unit in ["B", "KB", "MB", "GB", "TB"]:
                if bytes_val < 1024.0:
                    return f"{bytes_val:.1f} {unit}"
                bytes_val /= 1024.0
            return f"{bytes_val:.1f} PB"

        current_metrics = {
            "cpu_percent": round(current_metrics_raw["cpu_percent"], 1),
            "cpu_count": current_metrics_raw["cpu_count"],
            "memory_percent": round(current_metrics_raw["memory_percent"], 1),
            "memory_used": format_bytes(current_metrics_raw["memory_used"]),
            "memory_available": format_bytes(current_metrics_raw["memory_available"]),
            "memory_total": format_bytes(current_metrics_raw["memory_total"]),
            "disk_percent": round(current_metrics_raw["disk_percent"], 1),
            "disk_used": format_bytes(current_metrics_raw["disk_used"]),
            "disk_free": format_bytes(current_metrics_raw["disk_free"]),
            "disk_total": format_bytes(current_metrics_raw["disk_total"]),
            "network_bytes_sent": format_bytes(current_metrics_raw["network_bytes_sent"]),
            "network_bytes_recv": format_bytes(current_metrics_raw["network_bytes_recv"]),
            "network_packets_sent": current_metrics_raw["network_packets_sent"],
            "network_packets_recv": current_metrics_raw["network_packets_recv"],
            "active_sessions": current_metrics_raw["active_sessions"],
        }

        # Get historical metrics
        metrics = (
            SystemMetrics.objects.filter(timestamp__gte=since)
            .order_by("timestamp")
            .values(
                "timestamp",
                "cpu_percent",
                "memory_percent",
                "disk_percent",
                "active_sessions",
                "network_bytes_sent",
                "network_bytes_recv",
            )
        )

        history = list(metrics)

        # If no recent data, fall back to most recent N records regardless of timeframe
        if not history:
            fallback_metrics = SystemMetrics.objects.order_by("-timestamp")[:100].values(
                "timestamp",
                "cpu_percent",
                "memory_percent",
                "disk_percent",
                "active_sessions",
                "network_bytes_sent",
                "network_bytes_recv",
            )
            # Reverse to get chronological order
            history = list(reversed(list(fallback_metrics)))

        return JsonResponse({"current": current_metrics, "history": history})

    def collect_metrics(self, request):
        """Manually collect current system metrics"""
        hosted = _check_not_hosted(request)
        if hosted:
            return hosted
        metrics = SystemMonitor.get_system_metrics()
        SystemMetrics.objects.create(**metrics)
        return JsonResponse({"success": True, "message": _("Metrics collected")})

    # =========================================================================
    # Deployment Dashboard Views
    # =========================================================================

    def deployment_status_api(self, request):
        """API endpoint for deployment status (service health, SSL, version)"""
        try:
            # Try to get cached status first
            cached = SystemStatusService.get_cached_status()
            if cached:
                return JsonResponse({"success": True, "status": cached, "source": "cache"})

            # Collect fresh status
            status = SystemStatusService.collect_all_status()
            return JsonResponse({"success": True, "status": status, "source": "fresh"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    def run_diagnostics_view(self, request):
        """Run system diagnostics and display results"""
        hosted = _check_not_hosted(request)
        if hosted:
            return hosted
        from .tasks import run_diagnostics

        if request.method == "POST":
            # Run diagnostics synchronously for immediate results
            result = run_diagnostics()
            return JsonResponse(result)

        # GET - show diagnostics page
        return render(
            request,
            "admin/management/diagnostics.html",
            {
                "title": _("System Diagnostics"),
                "opts": self.model._meta,
            },
        )

    def toggle_maintenance_view(self, request):
        """Toggle maintenance mode on/off"""
        hosted = _check_not_hosted(request)
        if hosted:
            return hosted
        if request.method != "POST":
            return JsonResponse({"success": False, "error": "POST method required"}, status=405)

        try:
            data = json.loads(request.body) if request.body else {}
            enabled = data.get("enabled", False)
            reason = data.get("reason", "")

            success = SystemStatusService.toggle_maintenance_mode(enabled, reason)

            if success:
                if enabled:
                    messages.success(request, _("Maintenance mode enabled"))
                else:
                    messages.success(request, _("Maintenance mode disabled"))
                return JsonResponse({"success": True, "enabled": enabled})
            else:
                return JsonResponse(
                    {"success": False, "error": _("Failed to toggle maintenance mode")}
                )
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    def create_full_backup_view(self, request):
        """Create a full system backup (db + media + config)"""
        hosted = _check_not_hosted(request)
        if hosted:
            return hosted
        from django.utils import timezone

        from .tasks import run_full_backup

        if request.method == "POST":
            backup_type = request.POST.get("backup_type", "full")
            encrypt = request.POST.get("encrypt") == "on"

            # Collect selected remote destination IDs
            destination_ids = request.POST.getlist("destinations")

            # Create backup record
            backup = DeploymentBackup.objects.create(
                name=request.POST.get("name", "").strip()
                or f"Manual backup {timezone.now().strftime('%Y%m%d_%H%M%S')}",
                backup_type=backup_type,
                status="pending",
                is_encrypted=encrypt,
                created_by=request.user,
            )

            # Queue the backup task
            task = run_full_backup.delay(
                backup.id,
                backup_type,
                encrypt,
                destination_ids or None,
            )

            # Update with task ID
            backup.task_id = task.id
            backup.save(update_fields=["task_id"])

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"success": True, "backup_id": backup.id})
            messages.info(request, _("Backup started. You can monitor progress below."))
            return redirect(reverse("admin:management_system_dashboard"))

        # GET - show backup form
        recent_backups = DeploymentBackup.objects.order_by("-created_at")[:5]
        destinations = RemoteStorageDestination.objects.filter(is_active=True)
        return render(
            request,
            "admin/management/create_full_backup.html",
            {
                "title": _("Create Full Backup"),
                "opts": self.model._meta,
                "recent_backups": recent_backups,
                "destinations": destinations,
            },
        )

    def backup_progress_api(self, request, backup_id):
        """API endpoint for backup progress polling"""
        hosted = _check_not_hosted(request)
        if hosted:
            return hosted
        try:
            backup = DeploymentBackup.objects.get(pk=backup_id)
            return JsonResponse(
                {
                    "success": True,
                    "status": backup.status,
                    "progress_percent": backup.progress_percent,
                    "current_step": backup.current_step,
                    "completed": backup.status == "completed",
                    "failed": backup.status == "failed",
                    "error_message": backup.error_message if backup.status == "failed" else None,
                    "file_size": backup.file_size_display if backup.file_size else None,
                }
            )
        except DeploymentBackup.DoesNotExist:
            return JsonResponse({"success": False, "error": _("Backup not found")})

    def backup_schedule_view(self, request):
        """Configure scheduled backups"""
        hosted = _check_not_hosted(request)
        if hosted:
            return hosted
        # Get or create the schedule (singleton)
        schedule, created = BackupSchedule.objects.get_or_create(pk=1)

        if request.method == "POST":
            schedule.is_enabled = request.POST.get("is_enabled") == "on"
            schedule.frequency = request.POST.get("frequency", "daily")
            schedule.backup_type = request.POST.get("backup_type", "full")
            schedule.retention_days = int(request.POST.get("retention_days", 30))

            # Time
            time_str = request.POST.get("time_of_day", "03:00")
            try:
                from datetime import time

                hour, minute = map(int, time_str.split(":"))
                schedule.time_of_day = time(hour, minute)
            except (ValueError, AttributeError):
                pass

            # Weekly/Monthly settings
            if schedule.frequency == "weekly":
                schedule.day_of_week = int(request.POST.get("day_of_week", 0))
            elif schedule.frequency == "monthly":
                schedule.day_of_month = int(request.POST.get("day_of_month", 1))

            # Encryption
            schedule.encrypt = request.POST.get("encrypt") == "on"

            # Calculate next run
            schedule.calculate_next_run()
            schedule.save()

            # Update remote destinations M2M
            dest_ids = request.POST.getlist("remote_destinations")
            schedule.remote_destinations.set(
                RemoteStorageDestination.objects.filter(pk__in=dest_ids, is_active=True)
            )

            messages.success(request, _("Backup schedule updated"))
            return redirect(reverse("admin:management_system_dashboard"))

        destinations = RemoteStorageDestination.objects.filter(is_active=True)
        selected_dest_ids = set(schedule.remote_destinations.values_list("pk", flat=True))
        # Annotate each destination with a selected flag for the template
        for dest in destinations:
            dest.is_selected = dest.pk in selected_dest_ids
        return render(
            request,
            "admin/management/backup_schedule.html",
            {
                "title": _("Backup Schedule"),
                "opts": self.model._meta,
                "schedule": schedule,
                "destinations": destinations,
            },
        )

    def restore_list_view(self, request):
        """List available backups for restore"""
        hosted = _check_not_hosted(request)
        if hosted:
            return hosted
        backups = DeploymentBackup.objects.filter(status="completed").order_by("-created_at")
        return render(
            request,
            "admin/management/restore_list.html",
            {
                "title": _("Restore from Backup"),
                "opts": self.model._meta,
                "backups": backups,
            },
        )

    def restore_confirm_view(self, request, backup_id):
        """Confirm restore with warnings"""
        hosted = _check_not_hosted(request)
        if hosted:
            return hosted
        try:
            backup = DeploymentBackup.objects.get(pk=backup_id, status="completed")
        except DeploymentBackup.DoesNotExist:
            messages.error(request, _("Backup not found"))
            return redirect(reverse("admin:management_restore"))

        return render(
            request,
            "admin/management/restore_confirm.html",
            {
                "title": _("Confirm Restore"),
                "opts": self.model._meta,
                "backup": backup,
            },
        )

    def restore_execute_view(self, request, backup_id):
        """Execute the restore operation"""
        hosted = _check_not_hosted(request)
        if hosted:
            return hosted
        if request.method != "POST":
            return JsonResponse({"success": False, "error": "POST method required"}, status=405)

        from .tasks import run_restore

        try:
            backup = DeploymentBackup.objects.get(pk=backup_id, status="completed")
        except DeploymentBackup.DoesNotExist:
            messages.error(request, _("Backup not found"))
            return redirect(reverse("admin:management_restore"))

        # Check confirmation
        if request.POST.get("confirm") != "RESTORE":
            messages.error(request, _("Please type RESTORE to confirm"))
            return redirect(reverse("admin:management_restore_confirm", args=[backup_id]))

        # Create restore record
        restore = SystemRestore.objects.create(
            source_backup=backup,
            status="pending",
            skip_database=request.POST.get("skip_database") == "on",
            skip_media=request.POST.get("skip_media") == "on",
            skip_config=request.POST.get("skip_config") == "on",
            created_by=request.user,
        )

        # Queue the restore task
        task = run_restore.delay(restore.id)
        restore.task_id = task.id
        restore.save(update_fields=["task_id"])

        messages.info(request, _("Restore started. This may take several minutes."))
        return redirect(reverse("admin:management_system_dashboard"))

    def restore_progress_api(self, request, restore_id):
        """API endpoint for restore progress polling"""
        hosted = _check_not_hosted(request)
        if hosted:
            return hosted
        try:
            restore = SystemRestore.objects.get(pk=restore_id)
            return JsonResponse(
                {
                    "success": True,
                    "status": restore.status,
                    "progress_percent": restore.progress_percent,
                    "current_step": restore.current_step,
                    "completed": restore.status == "completed",
                    "failed": restore.status == "failed",
                    "error_message": restore.error_message if restore.status == "failed" else None,
                }
            )
        except SystemRestore.DoesNotExist:
            return JsonResponse({"success": False, "error": _("Restore not found")})

    def check_updates_view(self, request):
        """Check for available updates"""
        from core.license import get_license_manager

        if get_license_manager().is_spwig_hosted():
            return JsonResponse({"error": "Use hosted upgrade page"}, status=403)
        SystemStatus.get_instance()

        # Refresh version info
        version_info = SystemStatusService.get_version_info()

        return JsonResponse(
            {
                "success": True,
                "current_version": version_info.get("current", "unknown"),
                "available_version": version_info.get("available"),
                "update_available": version_info.get("update_available", False),
                "changelog": version_info.get("changelog"),
            }
        )

    def upgrade_view(self, request):
        """View upgrade options and status"""
        from core.license import get_license_manager

        if get_license_manager().is_spwig_hosted():
            from django.shortcuts import redirect

            return redirect(reverse("admin:component_updates_hosted_upgrade"))
        status = SystemStatus.get_instance()

        # Get version info
        version_info = SystemStatusService.get_version_info()

        # Get recent upgrades
        recent_upgrades = SystemUpgrade.objects.order_by("-created_at")[:5]

        return render(
            request,
            "admin/management/upgrade.html",
            {
                "title": _("System Upgrade"),
                "opts": self.model._meta,
                "current_version": version_info.get("current", "unknown"),
                "available_version": version_info.get("available"),
                "update_available": version_info.get("update_available", False),
                "changelog": version_info.get("changelog"),
                "recent_upgrades": recent_upgrades,
                "status": status,
            },
        )

    def upgrade_start_view(self, request):
        """Start a new upgrade - returns JSON with upgrade_id for progress polling"""
        from core.license import get_license_manager

        if get_license_manager().is_spwig_hosted():
            return JsonResponse({"error": "Use hosted upgrade page"}, status=403)
        if request.method != "POST":
            return JsonResponse({"error": "POST method required"}, status=405)

        import json

        from .tasks import run_upgrade

        try:
            data = json.loads(request.body) if request.body else {}
            target_version = data.get("target_version", "latest")
        except json.JSONDecodeError:
            target_version = request.POST.get("version", "latest")

        status = SystemStatus.get_instance()

        # Create upgrade record
        upgrade = SystemUpgrade.objects.create(
            from_version=status.current_version or "unknown",
            to_version=target_version,
            status="pending",
            created_by=request.user,
        )

        # Queue the upgrade task
        task = run_upgrade.delay(upgrade.id, target_version)
        upgrade.task_id = task.id
        upgrade.save(update_fields=["task_id"])

        return JsonResponse(
            {
                "success": True,
                "upgrade_id": upgrade.id,
                "message": _("Upgrade started"),
            }
        )

    def upgrade_execute_view(self, request, upgrade_id=None):
        """Execute the upgrade operation (legacy - redirects to dashboard)"""
        from core.license import get_license_manager

        if get_license_manager().is_spwig_hosted():
            return JsonResponse({"error": "Use hosted upgrade page"}, status=403)
        if request.method != "POST":
            return JsonResponse({"error": "POST method required"}, status=405)

        from .tasks import run_upgrade

        target_version = request.POST.get("version", "latest")
        status = SystemStatus.get_instance()

        # Create upgrade record
        upgrade = SystemUpgrade.objects.create(
            from_version=status.current_version or "unknown",
            to_version=target_version,
            status="pending",
            created_by=request.user,
        )

        # Queue the upgrade task
        task = run_upgrade.delay(upgrade.id, target_version)
        upgrade.task_id = task.id
        upgrade.save(update_fields=["task_id"])

        messages.info(
            request,
            _("Upgrade started. The system will be in maintenance mode during the upgrade."),
        )
        return redirect(reverse("admin:management_system_dashboard"))

    def upgrade_progress_api(self, request, upgrade_id):
        """API endpoint for upgrade progress polling"""
        from core.license import get_license_manager

        if get_license_manager().is_spwig_hosted():
            return JsonResponse({"error": "Use hosted upgrade page"}, status=403)
        try:
            upgrade = SystemUpgrade.objects.get(pk=upgrade_id)
            return JsonResponse(
                {
                    "success": True,
                    "status": upgrade.status,
                    "progress_percent": upgrade.progress_percent,
                    "current_step": upgrade.current_step,
                    "completed": upgrade.status == "completed",
                    "failed": upgrade.status == "failed",
                    "rolled_back": upgrade.status == "rolled_back",
                    "error_message": upgrade.error_message
                    if upgrade.status in ("failed", "rolled_back")
                    else None,
                }
            )
        except SystemUpgrade.DoesNotExist:
            return JsonResponse({"success": False, "error": _("Upgrade not found")})


@admin.register(AccessLog)
class AccessLogAdmin(admin.ModelAdmin):
    list_display = ["user_display", "ip_address", "method", "path", "status_code", "timestamp"]
    list_filter = ["method", "status_code", "timestamp", "action"]
    search_fields = ["user__username", "ip_address", "path", "action"]
    readonly_fields = [field.name for field in AccessLog._meta.fields]
    change_list_template = "admin/management/change_list.html"

    def has_add_permission(self, request):
        return False  # Access logs are created automatically

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["title"] = _("Access Logs")
        extra_context["management_tools"] = [
            {
                "title": _("Database Browser"),
                "url": reverse("admin:management_database_browser"),
                "description": _("Browse and query database tables"),
                "class": "addlink",
                "icon": "fas fa-database",
            },
            {
                "title": _("System Dashboard"),
                "url": reverse("admin:management_system_dashboard"),
                "description": _("Monitor system performance and metrics"),
                "class": "viewlink",
                "icon": "fas fa-server",
            },
            {
                "title": _("File Manager"),
                "url": reverse("admin:management_file_manager"),
                "description": _("Manage static and media files"),
                "class": "addlink",
                "icon": "fas fa-folder",
            },
        ]
        return super().changelist_view(request, extra_context)

    def user_display(self, obj):
        return obj.user.username if obj.user else _("Anonymous")

    user_display.short_description = _("User")


@admin.register(FileOperation)
class FileOperationAdmin(admin.ModelAdmin):
    list_display = [
        "operation_type",
        "file_name",
        "user",
        "timestamp",
        "success",
        "file_size_display",
    ]
    list_filter = ["operation_type", "success", "timestamp"]
    search_fields = ["file_path", "user__username"]
    readonly_fields = [field.name for field in FileOperation._meta.fields]
    change_list_template = "admin/management/change_list.html"

    def has_add_permission(self, request):
        return False  # File operations are logged automatically

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["title"] = _("File Operations")
        extra_context["management_tools"] = [
            {
                "title": _("File Manager"),
                "url": reverse("admin:management_file_manager"),
                "description": _("Browse, upload and manage files"),
                "class": "addlink",
                "icon": "fas fa-folder",
            }
        ]
        return super().changelist_view(request, extra_context)

    def file_name(self, obj):
        return os.path.basename(obj.file_path)

    file_name.short_description = _("File Name")

    def file_size_display(self, obj):
        if obj.file_size:
            size = obj.file_size
            for unit in ["B", "KB", "MB", "GB"]:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
            return f"{size:.1f} TB"
        return ""

    file_size_display.short_description = _("Size")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "file-manager/",
                self.admin_site.admin_view(self.file_manager_view),
                name="management_file_manager",
            ),
            path(
                "upload-file/",
                self.admin_site.admin_view(self.upload_file),
                name="management_upload_file",
            ),
            path(
                "delete-file/",
                self.admin_site.admin_view(self.delete_file),
                name="management_delete_file",
            ),
        ]
        return custom_urls + urls

    def file_manager_view(self, request):
        hosted = _check_not_hosted(request)
        if hosted:
            return hosted
        current_path = request.GET.get("path", settings.MEDIA_ROOT)

        # Security check
        safe_path = FileManager.safe_path(settings.MEDIA_ROOT, current_path)
        if not safe_path:
            messages.error(request, _("Access denied to that path."))
            current_path = settings.MEDIA_ROOT
            safe_path = current_path

        try:
            files = FileManager.get_directory_listing(safe_path)
            if isinstance(files, dict) and "error" in files:
                messages.error(request, _("Error reading directory: {}").format(files["error"]))
                files = []
        except Exception as e:
            messages.error(request, _("Error accessing directory: {}").format(str(e)))
            files = []

        context = {
            "title": _("File Manager"),
            "opts": self.model._meta,
            "current_path": current_path,
            "files": files,
            "parent_path": os.path.dirname(current_path)
            if current_path != settings.MEDIA_ROOT
            else None,
            "has_permission": True,
            "user": request.user,
            "site_url": getattr(settings, "SITE_URL", "/"),
            "site_title": self.admin_site.site_title,
            "site_header": self.admin_site.site_header,
        }

        return render(request, "admin/management/file_manager.html", context)

    def upload_file(self, request):
        hosted = _check_not_hosted(request)
        if hosted:
            return hosted
        if request.method != "POST":
            return JsonResponse({"success": False, "error": "POST method required"}, status=405)

        if not request.FILES.get("file"):
            return JsonResponse({"success": False, "error": _("No file uploaded")})

        upload_path = request.POST.get("path", settings.MEDIA_ROOT)
        safe_path = FileManager.safe_path(settings.MEDIA_ROOT, upload_path)

        if not safe_path:
            return JsonResponse({"success": False, "error": _("Invalid upload path")})

        try:
            uploaded_file = request.FILES["file"]
            file_path = os.path.join(safe_path, uploaded_file.name)

            with open(file_path, "wb") as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)

            # Log operation
            FileOperation.objects.create(
                operation_type="upload",
                file_path=file_path,
                file_size=uploaded_file.size,
                user=request.user,
                success=True,
            )

            return JsonResponse({"success": True, "message": _("File uploaded successfully")})

        except Exception as e:
            FileOperation.objects.create(
                operation_type="upload",
                file_path=file_path if "file_path" in locals() else "unknown",
                user=request.user,
                success=False,
                error_message=str(e),
            )
            return JsonResponse({"success": False, "error": str(e)})

    def delete_file(self, request):
        hosted = _check_not_hosted(request)
        if hosted:
            return hosted
        if request.method != "POST":
            return JsonResponse({"success": False, "error": "POST method required"}, status=405)

        file_path = request.POST.get("file_path")
        if not file_path:
            return JsonResponse({"success": False, "error": _("No file path provided")})

        safe_path = FileManager.safe_path(settings.MEDIA_ROOT, file_path)
        if not safe_path:
            return JsonResponse({"success": False, "error": _("Invalid file path")})

        try:
            if os.path.exists(safe_path):
                file_size = os.path.getsize(safe_path)
                os.remove(safe_path)

                # Log operation
                FileOperation.objects.create(
                    operation_type="delete",
                    file_path=safe_path,
                    file_size=file_size,
                    user=request.user,
                    success=True,
                )

                return JsonResponse({"success": True, "message": _("File deleted successfully")})
            else:
                return JsonResponse({"success": False, "error": _("File not found")})

        except Exception as e:
            FileOperation.objects.create(
                operation_type="delete",
                file_path=safe_path,
                user=request.user,
                success=False,
                error_message=str(e),
            )
            return JsonResponse({"success": False, "error": str(e)})


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    """Admin for viewing archived Docker container logs"""

    list_display = ["timestamp", "container_name", "level_badge", "message_preview", "source"]
    list_filter = ["container_name", "level", "source", "timestamp"]
    search_fields = ["message", "raw_line"]
    readonly_fields = [
        "container_name",
        "level",
        "message",
        "timestamp",
        "raw_line",
        "source",
        "archived_at",
    ]
    date_hierarchy = "timestamp"
    ordering = ["-timestamp"]
    list_per_page = 50
    change_list_template = "admin/management/change_list.html"

    def has_add_permission(self, request):
        return False  # Logs are created automatically

    def has_change_permission(self, request, obj=None):
        return False  # Read-only

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["title"] = _("Archived Logs")
        extra_context["management_tools"] = [
            {
                "title": _("Log Viewer Dashboard"),
                "url": reverse("admin:management_logentry_log_viewer"),
                "description": _("Real-time log viewer with filtering and stats"),
                "class": "addlink",
                "icon": "fas fa-clipboard-list",
            }
        ]
        return super().changelist_view(request, extra_context)

    def level_badge(self, obj):
        return format_html(
            '<span class="mgmt-level-badge mgmt-level-badge-{}">{}</span>', obj.level, obj.level
        )

    level_badge.short_description = _("Level")
    level_badge.admin_order_field = "level"

    def message_preview(self, obj):
        preview = obj.message[:100] + "..." if len(obj.message) > 100 else obj.message
        return format_html('<code class="mgmt-code-message">{}</code>', preview)

    message_preview.short_description = _("Message")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "log-viewer/",
                self.admin_site.admin_view(self.log_viewer_view),
                name="management_logentry_log_viewer",
            ),
            path(
                "log-viewer/api/logs/",
                self.admin_site.admin_view(self.logs_api),
                name="management_logentry_logs_api",
            ),
            path(
                "log-viewer/api/stats/",
                self.admin_site.admin_view(self.stats_api),
                name="management_logentry_stats_api",
            ),
            path(
                "log-viewer/api/containers/",
                self.admin_site.admin_view(self.containers_api),
                name="management_logentry_containers_api",
            ),
            path(
                "log-viewer/api/export/",
                self.admin_site.admin_view(self.export_api),
                name="management_logentry_export_api",
            ),
        ]
        return custom_urls + urls

    def log_viewer_view(self, request):
        """Main log viewer dashboard"""
        hosted = _check_not_hosted(request)
        if hosted:
            return hosted
        from .services.docker_log_service import DockerLogService

        service = DockerLogService()
        settings_obj = LogViewerSettings.get_instance()

        # Get initial data
        stats = service.get_log_stats()
        containers = service.get_container_status()

        context = {
            "title": _("Log Viewer"),
            "opts": self.model._meta,
            "stats": stats,
            "containers": containers,
            "settings": settings_obj,
            "refresh_interval_ms": settings_obj.auto_refresh_interval * 1000,
            "container_choices": LogEntry.CONTAINER_CHOICES,
            "level_choices": LogEntry.LEVEL_CHOICES,
            "has_permission": True,
            "user": request.user,
            "site_url": getattr(settings, "SITE_URL", "/"),
            "site_title": self.admin_site.site_title,
            "site_header": self.admin_site.site_header,
        }

        return render(request, "admin/management/log_viewer.html", context)

    def logs_api(self, request):
        """API endpoint for fetching logs"""
        hosted = _check_not_hosted(request)
        if hosted:
            return hosted
        if request.headers.get("X-Requested-With") != "XMLHttpRequest":
            return JsonResponse({"error": "AJAX request required"}, status=400)

        from .services.docker_log_service import DockerLogService

        container = request.GET.get("container", "")
        level = request.GET.get("level", "")
        search = request.GET.get("search", "")
        source = request.GET.get("source", "redis")  # 'redis' or 'db'
        limit = min(int(request.GET.get("limit", 50)), 200)
        offset = int(request.GET.get("offset", 0))

        if source == "redis":
            # Fetch from Redis (recent logs)
            service = DockerLogService()
            logs = service.get_recent_logs(
                container=container or None, level=level or None, search=search or None, limit=limit
            )
            # Apply offset manually for Redis
            logs = logs[offset : offset + limit]
            has_more = len(logs) == limit
            total = None  # Unknown for Redis
        else:
            # Fetch from database (archived logs)
            queryset = LogEntry.objects.all()

            if container:
                queryset = queryset.filter(container_name=container)
            if level:
                queryset = queryset.filter(level=level)
            if search:
                queryset = queryset.filter(message__icontains=search)

            total = queryset.count()
            logs_qs = queryset.order_by("-timestamp")[offset : offset + limit]

            logs = []
            for log in logs_qs:
                logs.append(
                    {
                        "container": log.container_name,
                        "level": log.level,
                        "message": log.message,
                        "timestamp": log.timestamp.isoformat(),
                        "source": log.source,
                    }
                )
            has_more = offset + limit < total

        return JsonResponse(
            {
                "success": True,
                "logs": logs,
                "count": len(logs),
                "has_more": has_more,
                "total": total,
                "source": source,
            }
        )

    def stats_api(self, request):
        """API endpoint for log statistics"""
        hosted = _check_not_hosted(request)
        if hosted:
            return hosted
        if request.headers.get("X-Requested-With") != "XMLHttpRequest":
            return JsonResponse({"error": "AJAX request required"}, status=400)

        from .services.docker_log_service import DockerLogService

        service = DockerLogService()
        stats = service.get_log_stats()

        return JsonResponse(
            {
                "success": True,
                "stats": stats,
            }
        )

    def containers_api(self, request):
        """API endpoint for container status"""
        hosted = _check_not_hosted(request)
        if hosted:
            return hosted
        if request.headers.get("X-Requested-With") != "XMLHttpRequest":
            return JsonResponse({"error": "AJAX request required"}, status=400)

        from .services.docker_log_service import DockerLogService

        service = DockerLogService()
        containers = service.get_container_status()

        return JsonResponse(
            {
                "success": True,
                "containers": containers,
            }
        )

    def export_api(self, request):
        """Export logs as CSV or JSON file download"""
        hosted = _check_not_hosted(request)
        if hosted:
            return hosted
        import csv

        export_format = request.GET.get("format", "csv")
        if export_format not in ("csv", "json"):
            return JsonResponse({"error": "Invalid format. Use csv or json."}, status=400)

        container = request.GET.get("container", "")
        level = request.GET.get("level", "")
        search = request.GET.get("search", "")
        source = request.GET.get("source", "redis")
        MAX_EXPORT = 10000

        if source == "redis":
            from .services.docker_log_service import DockerLogService

            service = DockerLogService()
            logs = service.get_recent_logs(
                container=container or None,
                level=level or None,
                search=search or None,
                limit=MAX_EXPORT,
            )
        else:
            queryset = LogEntry.objects.all()
            if container:
                queryset = queryset.filter(container_name=container)
            if level:
                queryset = queryset.filter(level=level)
            if search:
                queryset = queryset.filter(message__icontains=search)

            logs = []
            for log in queryset.order_by("-timestamp")[:MAX_EXPORT]:
                logs.append(
                    {
                        "container": log.container_name,
                        "level": log.level,
                        "message": log.message,
                        "timestamp": log.timestamp.isoformat(),
                        "source": log.source,
                    }
                )

        timestamp_str = datetime.now().strftime("%Y-%m-%d_%H%M%S")

        if export_format == "csv":
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = (
                f'attachment; filename="logs_export_{timestamp_str}.csv"'
            )
            writer = csv.writer(response)
            writer.writerow(["timestamp", "container", "level", "message", "source"])
            for log in logs:
                writer.writerow(
                    [
                        log.get("timestamp", ""),
                        log.get("container", ""),
                        log.get("level", ""),
                        log.get("message", ""),
                        log.get("source", ""),
                    ]
                )
            return response
        else:
            response = HttpResponse(
                json.dumps(logs, indent=2, ensure_ascii=False), content_type="application/json"
            )
            response["Content-Disposition"] = (
                f'attachment; filename="logs_export_{timestamp_str}.json"'
            )
            return response


@admin.register(LogViewerSettings)
class LogViewerSettingsAdmin(admin.ModelAdmin):
    """Admin for configuring log viewer settings (singleton)"""

    list_display = [
        "__str__",
        "stream_enabled",
        "redis_retention_minutes",
        "db_retention_days",
        "auto_refresh_interval",
    ]

    fieldsets = (
        (
            _("Retention Settings"),
            {
                "fields": ("redis_retention_minutes", "db_retention_days"),
                "description": _("Configure how long logs are kept in Redis and the database."),
            },
        ),
        (
            _("Archive Settings"),
            {
                "fields": ("archive_batch_size", "archive_interval_seconds"),
                "description": _("Configure how logs are archived from Redis to the database."),
            },
        ),
        (
            _("Streaming"),
            {
                "fields": ("stream_enabled", "max_logs_per_container"),
                "description": _("Configure real-time log collection from Docker containers."),
            },
        ),
        (
            _("Security"),
            {
                "fields": ("sensitive_patterns",),
                "description": _(
                    'Regex patterns to redact from logs (e.g., passwords, tokens). Enter as a JSON array: ["pattern1", "pattern2"]'
                ),
            },
        ),
        (
            _("Display"),
            {
                "fields": ("default_page_size", "auto_refresh_interval"),
                "description": _("Configure the log viewer UI settings."),
            },
        ),
    )

    def has_add_permission(self, request):
        # Only allow adding if no instance exists
        return not LogViewerSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False  # Singleton - never delete

    def changelist_view(self, request, extra_context=None):
        # Redirect to the single instance if it exists, otherwise show add form
        try:
            obj = LogViewerSettings.objects.first()
            if obj:
                return redirect(reverse("admin:management_logviewersettings_change", args=[obj.pk]))
        except LogViewerSettings.DoesNotExist:
            pass
        return super().changelist_view(request, extra_context)


# Custom admin site integration
class ManagementAdminSite:
    """Custom admin integration for management tools"""

    @staticmethod
    def get_database_info():
        """Get database statistics for admin dashboard"""
        return DatabaseManager.get_database_info()

    @staticmethod
    def get_table_list():
        """Get list of database tables"""
        return DatabaseManager.get_table_list()

    @staticmethod
    def export_table_data(table_name, format="csv"):
        """Export table data"""
        return DataExporter.export_table_data(table_name, format)


# Add management links to admin index
def add_management_links(request):
    """Add management tool links to admin index"""
    if request.user.is_staff:
        return {
            "management_links": [
                {
                    "title": _("Shop Dashboard"),
                    "url": reverse("admin:management_shop_dashboard"),
                    "description": _("Business metrics and sales analytics"),
                    "icon": "fas fa-chart-pie",
                },
                {
                    "title": _("Database Browser"),
                    "url": reverse("admin:management_database_browser"),
                    "description": _("Browse database tables and data"),
                    "icon": "fas fa-database",
                },
                {
                    "title": _("SQL Query Runner"),
                    "url": reverse("admin:management_query_runner"),
                    "description": _("Execute SQL queries interactively"),
                    "icon": "fas fa-terminal",
                },
                {
                    "title": _("System Dashboard"),
                    "url": reverse("admin:management_system_dashboard"),
                    "description": _("Monitor system performance and metrics"),
                    "icon": "fas fa-server",
                },
                {
                    "title": _("File Manager"),
                    "url": reverse("admin:management_file_manager"),
                    "description": _("Manage static and media files"),
                    "icon": "fas fa-folder",
                },
                {
                    "title": _("Create Backup"),
                    "url": reverse("admin:management_backup_create"),
                    "description": _("Create database backups"),
                    "icon": "fas fa-save",
                },
            ]
        }
    return {}
