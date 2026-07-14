from django.contrib import admin
from django.db.models import Count, Q
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from product_feeds.models import FeedProviderAccount, FeedSyncLog, ProductFeed


@admin.register(FeedProviderAccount)
class FeedProviderAccountAdmin(admin.ModelAdmin):
    """Admin for product feed provider connections"""

    # Use custom change_list template for modern card view
    change_list_template = "admin/product_feeds/feedprovideraccount/change_list.html"

    # Show all providers on one page for client-side filtering
    list_per_page = 1000

    list_display = [
        "display_name_or_component",
        "sync_status_badge",
        "products_count",
        "is_active_badge",
        "is_primary_badge",
        "sync_interval_badge",
        "last_sync_at",
        "created_at",
    ]
    list_filter = ["is_active", "is_primary", "sync_status", "created_at"]
    search_fields = ["name", "component__name", "component__slug"]
    readonly_fields = [
        "credentials_display",
        "last_sync_at",
        "next_sync_at",
        "sync_status",
        "sync_error_message",
        "last_error_at",
        "products_in_feed",
        "feed_url",
        "created_at",
        "updated_at",
    ]

    class Media:
        css = {"all": ("product_feeds/css/admin_provider_list.css",)}

    fieldsets = (
        (_("Provider Information"), {"fields": ("site", "component", "name")}),
        (_("Configuration"), {"fields": ("is_active", "is_primary", "priority", "config")}),
        (
            _("Credentials"),
            {
                "fields": ("credentials_display",),
                "description": _(
                    "Credentials are encrypted and managed through the provider wizard. To update credentials, reinstall the provider."
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Sync Status"),
            {
                "fields": (
                    "sync_status",
                    "sync_error_message",
                    "last_sync_at",
                    "next_sync_at",
                    "last_error_at",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Feed Statistics"),
            {"fields": ("products_in_feed", "feed_url"), "classes": ("collapse",)},
        ),
        (_("Timestamps"), {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def display_name_or_component(self, obj):
        """Display provider name or component name"""
        if obj.name:
            return obj.name
        return format_html("<em>{}</em>", obj.component.name)

    display_name_or_component.short_description = _("Name")

    def sync_status_badge(self, obj):
        """Display sync status with color coding"""
        return format_html(
            '<span class="status-badge status-{}">{}</span>',
            obj.sync_status,
            obj.get_sync_status_display().upper(),
        )

    sync_status_badge.short_description = _("Sync Status")

    def products_count(self, obj):
        """Display products in feed count"""
        if obj.products_in_feed > 0:
            return format_html(
                '<span class="product-count-value">{:,}</span>', obj.products_in_feed
            )
        return "-"

    products_count.short_description = _("Products")

    def sync_interval_badge(self, obj):
        """Display sync interval"""
        interval = obj.config.get("sync_interval", "daily")
        return format_html(
            '<span class="badge-interval badge-interval-{}">{}</span>', interval, interval.upper()
        )

    sync_interval_badge.short_description = _("Interval")

    def is_active_badge(self, obj):
        """Display active status badge"""
        if obj.is_active:
            return format_html(
                '<span class="status-badge active">'
                '<i class="fas fa-check-circle"></i> ACTIVE'
                "</span>"
            )
        return format_html(
            '<span class="status-badge inactive">'
            '<i class="fas fa-times-circle"></i> INACTIVE'
            "</span>"
        )

    is_active_badge.short_description = _("Status")

    def is_primary_badge(self, obj):
        """Display primary provider badge"""
        if obj.is_primary:
            return format_html(
                '<span class="status-badge primary"><i class="fas fa-star"></i> PRIMARY</span>'
            )
        return "-"

    is_primary_badge.short_description = _("Primary")

    def credentials_display(self, obj):
        """Display encrypted credentials info"""
        if obj.credentials:
            return format_html(
                '<div class="messagelist"><li class="info">'
                '<i class="fas fa-lock"></i> <strong>{}</strong><br>'
                '<span class="quiet help">{} bytes encrypted data</span>'
                "</li></div>",
                _("Credentials are encrypted and stored securely"),
                len(obj.credentials),
            )
        return format_html(
            '<div class="messagelist"><li class="warning">'
            '<i class="fas fa-exclamation-triangle"></i> {}'
            "</li></div>",
            _("No credentials configured"),
        )

    credentials_display.short_description = _("Credentials")

    def changelist_view(self, request, extra_context=None):
        """Add custom context data for the provider account list view"""
        extra_context = extra_context or {}

        # Get all provider accounts
        all_providers = FeedProviderAccount.objects.select_related("component").all()

        # Add logo URLs to each provider
        import json

        from django.templatetags.static import static

        from component_updates.integration_paths import INTEGRATIONS_DIR

        for provider in all_providers:
            # Get version directory
            version = provider.component.current_version or "v1.0.0"
            if not version.startswith("v"):
                version = f"v{version}"

            provider_dir = (
                INTEGRATIONS_DIR / "product_feed_provider" / provider.component.slug / version
            )
            manifest_path = provider_dir / "manifest.json"

            logo_url = ""
            if manifest_path.exists():
                with open(manifest_path) as f:
                    manifest = json.load(f)

                    # Get logo URL - handle both dict and string formats
                    logo_file = manifest.get("logo", {})
                    if isinstance(logo_file, dict):
                        logo_filename = logo_file.get("file", "")
                    else:
                        logo_filename = logo_file if logo_file else ""

                    if logo_filename:
                        logo_path = provider_dir / logo_filename
                        if logo_path.exists():
                            logo_url = static(
                                f"product_feed_provider/{provider.component.slug}/current/{logo_filename}"
                            )

            provider.logo_url = logo_url

        # Status counts
        extra_context["active_count"] = all_providers.filter(is_active=True).count()
        extra_context["inactive_count"] = all_providers.filter(is_active=False).count()

        # Sync status counts
        extra_context["success_count"] = all_providers.filter(sync_status="success").count()
        extra_context["error_count"] = all_providers.filter(sync_status="error").count()
        extra_context["pending_count"] = all_providers.filter(sync_status="pending").count()
        extra_context["syncing_count"] = all_providers.filter(sync_status="syncing").count()

        # Total products in feeds
        from django.db.models import Sum

        extra_context["total_products"] = (
            all_providers.aggregate(total=Sum("products_in_feed"))["total"] or 0
        )

        # Primary provider
        try:
            extra_context["primary_provider"] = all_providers.get(is_primary=True)
        except FeedProviderAccount.DoesNotExist:
            extra_context["primary_provider"] = None

        # Component counts (group by provider type)
        component_counts = (
            all_providers.values("component__slug", "component__name")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        # Build component list with counts
        components_with_counts = []
        for item in component_counts:
            if item["component__slug"]:
                components_with_counts.append(
                    {
                        "slug": item["component__slug"],
                        "name": item["component__name"],
                        "count": item["count"],
                    }
                )

        extra_context["component_counts"] = components_with_counts

        # Call parent to get the changelist
        response = super().changelist_view(request, extra_context=extra_context)

        # Add logo URLs to the result_list (the queryset shown in the template)
        if hasattr(response, "context_data") and "cl" in response.context_data:
            cl = response.context_data["cl"]
            for provider in cl.result_list:
                # Get version directory
                version = provider.component.current_version or "v1.0.0"
                if not version.startswith("v"):
                    version = f"v{version}"

                provider_dir = (
                    INTEGRATIONS_DIR / "product_feed_provider" / provider.component.slug / version
                )
                manifest_path = provider_dir / "manifest.json"

                logo_url = ""
                if manifest_path.exists():
                    with open(manifest_path) as f:
                        manifest = json.load(f)

                        logo_file = manifest.get("logo", {})
                        if isinstance(logo_file, dict):
                            logo_filename = logo_file.get("file", "")
                        else:
                            logo_filename = logo_file if logo_file else ""

                        if logo_filename:
                            logo_path = provider_dir / logo_filename
                            if logo_path.exists():
                                logo_url = static(
                                    f"product_feed_provider/{provider.component.slug}/current/{logo_filename}"
                                )

                provider.logo_url = logo_url

        return response

    def get_queryset(self, request):
        """Filter queryset based on request parameters"""
        qs = super().get_queryset(request).select_related("component", "site")

        # Sync status filter
        sync_status = request.GET.get("sync_status")
        if sync_status:
            qs = qs.filter(sync_status=sync_status)

        # Active status filter
        is_active = request.GET.get("is_active")
        if is_active:
            qs = qs.filter(is_active=(is_active == "1"))

        # Primary filter
        is_primary = request.GET.get("is_primary")
        if is_primary:
            qs = qs.filter(is_primary=(is_primary == "1"))

        # Component filter
        component = request.GET.get("component")
        if component:
            qs = qs.filter(component__slug=component)

        # Search query
        search = request.GET.get("q")
        if search:
            qs = qs.filter(
                Q(name__icontains=search)
                | Q(component__name__icontains=search)
                | Q(component__slug__icontains=search)
            )

        return qs


@admin.register(ProductFeed)
class ProductFeedAdmin(admin.ModelAdmin):
    """Admin for generated product feeds"""

    list_display = [
        "account",
        "feed_format",
        "product_count",
        "file_size_display",
        "generated_at",
        "expires_at",
        "expired_indicator",
        "download_count",
    ]
    list_filter = ["feed_format", "generated_at", "account"]
    search_fields = ["account__name", "account__component__name"]
    readonly_fields = [
        "generated_at",
        "file_size",
        "product_count",
        "download_count",
        "last_downloaded_at",
    ]

    def file_size_display(self, obj):
        """Display file size in human readable format"""
        size = obj.file_size
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    file_size_display.short_description = _("Size")

    def expired_indicator(self, obj):
        """Show if feed is expired"""
        if obj.is_expired:
            return format_html('<span class="text-expired">{}</span>', _("Expired"))
        return format_html('<span class="text-valid">{}</span>', _("Valid"))

    expired_indicator.short_description = _("Status")


@admin.register(FeedSyncLog)
class FeedSyncLogAdmin(admin.ModelAdmin):
    """Admin for feed sync logs"""

    change_list_template = "admin/product_feeds/feedsynclog/change_list.html"

    list_display = [
        "account",
        "status_badge",
        "sync_type",
        "products_synced",
        "products_failed",
        "duration_display",
        "started_at",
    ]
    list_filter = ["status", "sync_type", "started_at", "account"]
    search_fields = ["account__name", "error_message"]
    readonly_fields = [
        "started_at",
        "completed_at",
        "duration_seconds",
        "products_synced",
        "products_failed",
        "products_skipped",
        "error_details",
    ]

    def changelist_view(self, request, extra_context=None):
        """Override to add statistics for the sync log change list."""
        from django.db.models import Avg, Sum

        extra_context = extra_context or {}

        # Calculate statistics
        all_logs = FeedSyncLog.objects.all()

        extra_context["total_count"] = all_logs.count()
        extra_context["success_count"] = all_logs.filter(status="success").count()
        extra_context["partial_count"] = all_logs.filter(status="partial").count()
        extra_context["failed_count"] = all_logs.filter(status="failed").count()
        extra_context["running_count"] = all_logs.filter(status="running").count()
        extra_context["pending_count"] = all_logs.filter(status="pending").count()

        # Calculate success rate
        total = all_logs.count()
        if total > 0:
            success_rate = (all_logs.filter(status="success").count() / total) * 100
            extra_context["success_rate"] = f"{success_rate:.1f}"
        else:
            extra_context["success_rate"] = "0.0"

        # Average duration (exclude nulls and in-progress)
        avg_duration = all_logs.filter(duration_seconds__isnull=False).aggregate(
            avg=Avg("duration_seconds")
        )["avg"]
        extra_context["avg_duration"] = avg_duration or 0

        # Total products synced
        extra_context["total_products_synced"] = (
            all_logs.aggregate(total=Sum("products_synced"))["total"] or 0
        )

        # Accounts for filter
        extra_context["feed_accounts"] = FeedProviderAccount.objects.values("id", "name")

        # Sync types for filter
        extra_context["sync_types"] = all_logs.values_list("sync_type", flat=True).distinct()

        # Logs for display
        extra_context["logs"] = self.get_queryset(request).select_related("account")

        return super().changelist_view(request, extra_context=extra_context)

    def status_badge(self, obj):
        """Display status with color coding using CSS variables"""
        badge_classes = {
            "pending": "list-row-card-badge",
            "running": "list-row-card-badge list-row-card-badge-primary",
            "success": "list-row-card-badge list-row-card-badge-success",
            "partial": "list-row-card-badge list-row-card-badge-warning",
            "failed": "list-row-card-badge list-row-card-badge-error",
        }
        icons = {
            "pending": "fa-clock",
            "running": "fa-spinner fa-spin",
            "success": "fa-check-circle",
            "partial": "fa-exclamation-triangle",
            "failed": "fa-times-circle",
        }
        badge_class = badge_classes.get(obj.status, "list-row-card-badge")
        icon = icons.get(obj.status, "fa-info-circle")
        return format_html(
            '<span class="{}"><i class="fas {}"></i> {}</span>',
            badge_class,
            icon,
            obj.get_status_display().upper(),
        )

    status_badge.short_description = _("Status")

    def duration_display(self, obj):
        """Display duration in human readable format"""
        if obj.duration_seconds is None:
            return "-"
        if obj.duration_seconds < 60:
            return f"{obj.duration_seconds}s"
        minutes = obj.duration_seconds // 60
        seconds = obj.duration_seconds % 60
        return f"{minutes}m {seconds}s"

    duration_display.short_description = _("Duration")
