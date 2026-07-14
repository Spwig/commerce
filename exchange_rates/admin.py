from django.contrib import admin
from django.db.models import Count, Q
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from exchange_rates.models import (
    ExchangeRate,
    ExchangeRateHistory,
    ExchangeRateProviderAccount,
    ManualExchangeRate,
)


@admin.register(ExchangeRateProviderAccount)
class ExchangeRateProviderAccountAdmin(admin.ModelAdmin):
    """Admin for exchange rate provider connections"""

    # Use custom change_list template for modern card view
    change_list_template = "admin/exchange_rates/exchangerateprovideraccount/change_list.html"

    # Show all providers on one page for client-side filtering
    list_per_page = 1000

    list_display = [
        "display_name_or_component",
        "sync_status_badge",
        "is_active_badge",
        "is_primary_badge",
        "last_sync_at",
        "created_at",
    ]
    list_filter = ["is_active", "is_primary", "sync_status", "created_at"]
    search_fields = ["name", "component__name", "component__slug"]
    readonly_fields = [
        "credentials_display",
        "last_sync_at",
        "sync_status",
        "sync_error_message",
        "created_at",
        "updated_at",
    ]

    class Media:
        css = {"all": ("exchange_rates/css/admin_provider_list.css",)}

    fieldsets = (
        (_("Provider Information"), {"fields": ("site", "component", "name")}),
        (_("Configuration"), {"fields": ("is_active", "is_primary", "priority", "settings")}),
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
                "fields": ("sync_status", "sync_error_message", "last_sync_at"),
                "classes": ("collapse",),
            },
        ),
        (_("Timestamps"), {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    @admin.display(description=_("Name"))
    def display_name_or_component(self, obj):
        if obj.name:
            return obj.name
        return format_html("<em>{}</em>", obj.component.name)

    @admin.display(description=_("Sync Status"))
    def sync_status_badge(self, obj):
        css_class = {
            "pending": "sync-pending",
            "success": "sync-success",
            "error": "sync-error",
        }.get(obj.sync_status, "sync-pending")
        return format_html(
            '<span class="exchange-rates-admin-badge {}">{}</span>',
            css_class,
            obj.get_sync_status_display().upper(),
        )

    @admin.display(description=_("Status"))
    def is_active_badge(self, obj):
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

    @admin.display(description=_("Primary"))
    def is_primary_badge(self, obj):
        if obj.is_primary:
            return format_html(
                '<span class="status-badge primary"><i class="fas fa-star"></i> PRIMARY</span>'
            )
        return "-"

    @admin.display(description=_("Credentials"))
    def credentials_display(self, obj):
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

    @staticmethod
    def _attach_logo_urls(providers):
        """Attach logo_url to each provider from its component manifest."""
        import json

        from django.templatetags.static import static

        for provider in providers:
            version = provider.component.current_version or "v1.0.0"
            if not version.startswith("v"):
                version = f"v{version}"

            from component_updates.integration_paths import INTEGRATIONS_DIR

            provider_dir = (
                INTEGRATIONS_DIR / "exchange_rate_provider" / provider.component.slug / version
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
                            f"exchange_rate_provider/{provider.component.slug}/current/{logo_filename}"
                        )

            provider.logo_url = logo_url

    def changelist_view(self, request, extra_context=None):
        """Add custom context data for the provider account list view"""
        extra_context = extra_context or {}

        # Get all provider accounts
        all_providers = ExchangeRateProviderAccount.objects.select_related("component").all()

        # Add logo URLs to each provider
        self._attach_logo_urls(all_providers)

        # Status counts
        extra_context["active_count"] = all_providers.filter(is_active=True).count()
        extra_context["inactive_count"] = all_providers.filter(is_active=False).count()

        # Sync status counts
        extra_context["success_count"] = all_providers.filter(sync_status="success").count()
        extra_context["error_count"] = all_providers.filter(sync_status="error").count()
        extra_context["pending_count"] = all_providers.filter(sync_status="pending").count()

        # Primary provider
        try:
            extra_context["primary_provider"] = all_providers.get(is_primary=True)
        except ExchangeRateProviderAccount.DoesNotExist:
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
            self._attach_logo_urls(response.context_data["cl"].result_list)

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


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ["currency_pair", "rate", "provider_account", "fetched_at", "stale_indicator"]
    list_filter = ["provider_account", "base_currency", "target_currency", "fetched_at"]
    search_fields = ["base_currency", "target_currency"]
    readonly_fields = ["fetched_at"]

    @admin.display(description=_("Currency Pair"))
    def currency_pair(self, obj):
        return f"{obj.base_currency}/{obj.target_currency}"

    @admin.display(description=_("Status"))
    def stale_indicator(self, obj):
        if obj.is_stale:
            return format_html('<span class="exchange-rates-stale">⚠ {}</span>', _("Stale"))
        return format_html('<span class="exchange-rates-fresh">✓ {}</span>', _("Fresh"))


@admin.register(ExchangeRateHistory)
class ExchangeRateHistoryAdmin(admin.ModelAdmin):
    list_display = ["currency_pair", "rate", "provider_name", "order_link", "created_at"]
    list_filter = ["base_currency", "target_currency", "created_at"]
    search_fields = ["base_currency", "target_currency", "order__order_number"]
    readonly_fields = ["created_at"]

    @admin.display(description=_("Currency Pair"))
    def currency_pair(self, obj):
        return f"{obj.base_currency}/{obj.target_currency}"

    @admin.display(description=_("Order"))
    def order_link(self, obj):
        if obj.order:
            from django.urls import reverse

            url = reverse("admin:orders_order_change", args=[obj.order.id])
            return format_html('<a href="{}">{}</a>', url, obj.order.order_number)
        return "-"


@admin.register(ManualExchangeRate)
class ManualExchangeRateAdmin(admin.ModelAdmin):
    """Admin for merchant-defined manual exchange rates"""

    change_list_template = "admin/exchange_rates/manualexchangerate/change_list.html"
    list_per_page = 100

    list_display = [
        "currency_pair",
        "rate",
        "is_active_badge",
        "notes_truncated",
        "updated_at",
    ]
    list_filter = ["is_active", "base_currency", "target_currency"]
    search_fields = ["base_currency", "target_currency", "notes"]
    readonly_fields = ["created_at", "updated_at"]

    class Media:
        css = {"all": ("exchange_rates/css/admin_manual_rates.css",)}
        js = ("exchange_rates/js/admin_manual_rates.js",)

    fieldsets = (
        (_("Currency Pair"), {"fields": ("site", "base_currency", "target_currency")}),
        (_("Rate"), {"fields": ("rate",)}),
        (_("Settings"), {"fields": ("is_active", "exclude_from_auto_sync", "notes")}),
        (_("Timestamps"), {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def get_changeform_initial_data(self, request):
        """Pre-fill site field with current site"""
        from django.contrib.sites.models import Site

        return {"site": Site.objects.get(pk=1).pk}

    @admin.display(description=_("Currency Pair"))
    def currency_pair(self, obj):
        return f"{obj.base_currency}/{obj.target_currency}"

    @admin.display(description=_("Status"))
    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html(
                '<span class="status-badge active"><i class="fas fa-check-circle"></i> {}</span>',
                _("ACTIVE"),
            )
        return format_html(
            '<span class="status-badge inactive"><i class="fas fa-times-circle"></i> {}</span>',
            _("INACTIVE"),
        )

    @admin.display(description=_("Notes"))
    def notes_truncated(self, obj):
        if obj.notes:
            truncated = obj.notes[:60] + "..." if len(obj.notes) > 60 else obj.notes
            return truncated
        return "-"

    def changelist_view(self, request, extra_context=None):
        """Add stats and provider comparison context for the change list template"""
        extra_context = extra_context or {}
        from django.contrib.sites.models import Site

        site = Site.objects.get(pk=1)

        all_rates = ManualExchangeRate.objects.filter(site=site)
        extra_context["total_count"] = all_rates.count()
        extra_context["active_count"] = all_rates.filter(is_active=True).count()
        extra_context["inactive_count"] = all_rates.filter(is_active=False).count()
        extra_context["locked_count"] = all_rates.filter(exclude_from_auto_sync=True).count()

        # Fetch provider rates for comparison
        provider_rates = {}
        try:
            from core.models import SiteSettings
            from exchange_rates.models import ExchangeRate

            SiteSettings.get_settings()

            # Get latest provider rate for each currency pair
            for rate in all_rates:
                db_rate = (
                    ExchangeRate.objects.filter(
                        base_currency=rate.base_currency,
                        target_currency=rate.target_currency,
                        provider_account__is_active=True,
                    )
                    .order_by("-fetched_at")
                    .first()
                )

                if db_rate:
                    provider_rates[f"{rate.base_currency}/{rate.target_currency}"] = {
                        "rate": str(db_rate.rate),
                        "provider": db_rate.provider_account.name
                        or db_rate.provider_account.component.name,
                        "fetched_at": db_rate.fetched_at.isoformat()
                        if db_rate.fetched_at
                        else None,
                    }
        except Exception:
            pass

        extra_context["provider_rates"] = provider_rates

        return super().changelist_view(request, extra_context=extra_context)
