from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import (
    SearchClick,
    SearchEngine,
    SearchIndex,
    SearchQuery,
    SearchRedirect,
    SearchSettings,
    Synonym,
)


@admin.register(SearchSettings)
class SearchSettingsAdmin(admin.ModelAdmin):
    """
    Admin for the singleton SearchSettings model.
    Uses a custom change form template with tabbed sections.
    """

    change_form_template = "admin/search/searchsettings/change_form.html"

    fieldsets = (
        (
            _("General"),
            {
                "fields": ("is_enabled", "min_query_length"),
                "classes": ("tab-general",),
            },
        ),
        (
            _("Autocomplete"),
            {
                "fields": (
                    "autocomplete_enabled",
                    "autocomplete_max_results",
                    "autocomplete_debounce_ms",
                    "show_thumbnails",
                ),
                "classes": ("tab-autocomplete",),
            },
        ),
        (
            _("Autocomplete Display"),
            {
                "fields": (
                    "autocomplete_product_thumbnail",
                    "autocomplete_product_description",
                    "autocomplete_product_price",
                    "autocomplete_product_sku",
                    "autocomplete_product_stock_status",
                    "autocomplete_blog_thumbnail",
                    "autocomplete_blog_excerpt",
                    "autocomplete_blog_excerpt_length",
                    "autocomplete_category_thumbnail",
                    "autocomplete_category_product_count",
                    "autocomplete_brand_logo",
                    "autocomplete_brand_product_count",
                ),
                "classes": ("tab-autocomplete-display",),
            },
        ),
        (
            _("Content Types"),
            {
                "fields": (
                    "search_products",
                    "search_categories",
                    "search_brands",
                    "search_blog_posts",
                ),
                "classes": ("tab-content-types",),
            },
        ),
        (
            _("Deep Indexing"),
            {
                "fields": (
                    "index_skus",
                    "index_attributes",
                    "index_custom_fields",
                    "index_reviews",
                    "index_documents",
                ),
                "classes": ("tab-indexing",),
            },
        ),
        (
            _("Fuzzy Matching"),
            {
                "fields": (
                    "fuzzy_enabled",
                    "fuzzy_threshold",
                    "fuzzy_max_edits",
                ),
                "classes": ("tab-fuzzy",),
            },
        ),
        (
            _("Relevance Weights"),
            {
                "fields": (
                    "weight_name",
                    "weight_sku",
                    "weight_description",
                    "weight_attributes",
                    "weight_reviews",
                    "weight_categories",
                    "weight_brands",
                    "weight_blog_posts",
                ),
                "classes": ("tab-weights",),
                "description": _(
                    "Adjust the relevance weights for different content types. Higher values (up to 2.0) increase importance."
                ),
            },
        ),
        (
            _("Caching"),
            {
                "fields": (
                    "cache_autocomplete_ttl",
                    "cache_results_ttl",
                ),
                "classes": ("tab-caching",),
            },
        ),
        (
            _("Analytics"),
            {
                "fields": (
                    "track_search_queries",
                    "track_clicks",
                    "track_zero_results",
                ),
                "classes": ("tab-analytics",),
            },
        ),
        (
            _("Pagination"),
            {
                "fields": ("results_per_page",),
                "classes": ("tab-pagination",),
            },
        ),
    )

    def has_add_permission(self, request):
        # Only allow one instance (singleton)
        return not SearchSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        # Add weight fields list for the weights tab
        extra_context["weight_fields"] = [
            "weight_name",
            "weight_sku",
            "weight_description",
            "weight_attributes",
            "weight_reviews",
            "weight_categories",
            "weight_brands",
            "weight_blog_posts",
        ]
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def changelist_view(self, request, extra_context=None):
        # Redirect to the change form for the singleton instance
        extra_context = extra_context or {}
        # Add weight fields list for the weights tab
        extra_context["weight_fields"] = [
            "weight_name",
            "weight_sku",
            "weight_description",
            "weight_attributes",
            "weight_reviews",
            "weight_categories",
            "weight_brands",
            "weight_blog_posts",
        ]
        obj = SearchSettings.get_settings()
        return self.changeform_view(request, str(obj.pk), extra_context=extra_context)


@admin.register(SearchEngine)
class SearchEngineAdmin(admin.ModelAdmin):
    """Admin for search engines with custom list template, wizard, and tabbed change form."""

    change_list_template = "admin/search/searchengine/change_list.html"
    change_form_template = "admin/search/searchengine/change_form.html"
    list_display = ["name", "slug", "is_active", "content_types_display", "updated_at"]
    list_filter = ["is_active"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ["excluded_categories", "excluded_brands"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        (
            _("Basic Information"),
            {
                "fields": ("name", "slug", "is_active"),
                "classes": ("tab-basic",),
            },
        ),
        (
            _("Content Configuration"),
            {
                "fields": ("content_types", "weight_overrides"),
                "classes": ("tab-content",),
            },
        ),
        (
            _("Exclusions"),
            {
                "fields": ("excluded_categories", "excluded_brands"),
                "classes": ("tab-exclusions",),
            },
        ),
        (
            _("Metadata"),
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("tab-metadata",),
            },
        ),
    )

    class Media:
        css = {"all": ("search/admin/css/searchengine_form.css",)}
        js = ("search/admin/js/searchengine_form.js",)

    def content_types_display(self, obj):
        if obj.content_types:
            return ", ".join(obj.content_types)
        return _("All")

    content_types_display.short_description = _("Content Types")

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["search_engines"] = SearchEngine.objects.filter(is_active=True)
        return super().changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        return super().change_view(request, object_id, form_url, extra_context=extra_context)


@admin.register(Synonym)
class SynonymAdmin(admin.ModelAdmin):
    """Admin for synonyms with custom list template."""

    change_list_template = "admin/search/synonym/change_list.html"
    list_display = [
        "term",
        "synonyms_display",
        "language_display",
        "is_bidirectional",
        "engine",
        "is_active",
    ]
    list_filter = ["is_active", "is_bidirectional", "language", "engine"]
    search_fields = ["term"]
    raw_id_fields = ["engine"]

    fieldsets = (
        (
            None,
            {
                "fields": ("term", "synonyms", "is_bidirectional", "is_active"),
            },
        ),
        (
            _("Scope"),
            {
                "fields": ("language", "engine"),
                "description": _(
                    "Optionally limit this synonym to a specific language or search engine."
                ),
            },
        ),
    )

    def synonyms_display(self, obj):
        if obj.synonyms:
            display = ", ".join(obj.synonyms[:3])
            if len(obj.synonyms) > 3:
                display += f" (+{len(obj.synonyms) - 3})"
            return display
        return "-"

    synonyms_display.short_description = _("Synonyms")

    def language_display(self, obj):
        return obj.language or _("All")

    language_display.short_description = _("Language")

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["search_engines"] = SearchEngine.objects.filter(is_active=True)
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(SearchRedirect)
class SearchRedirectAdmin(admin.ModelAdmin):
    """Admin for search redirects."""

    change_list_template = "admin/search/searchredirect/change_list.html"
    list_display = [
        "term",
        "match_type",
        "redirect_url_display",
        "redirect_type",
        "hit_count",
        "is_active",
    ]
    list_filter = ["is_active", "match_type", "redirect_type", "engine"]
    search_fields = ["term", "redirect_url"]
    raw_id_fields = ["engine"]

    fieldsets = (
        (
            None,
            {
                "fields": ("term", "match_type", "is_active"),
            },
        ),
        (
            _("Redirect"),
            {
                "fields": ("redirect_url", "redirect_type"),
            },
        ),
        (
            _("Scope"),
            {
                "fields": ("engine",),
                "classes": ("collapse",),
            },
        ),
        (
            _("Statistics"),
            {
                "fields": ("hit_count",),
                "classes": ("collapse",),
            },
        ),
    )

    readonly_fields = ["hit_count"]

    def redirect_url_display(self, obj):
        if len(obj.redirect_url) > 50:
            return obj.redirect_url[:50] + "..."
        return obj.redirect_url

    redirect_url_display.short_description = _("Redirect URL")

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["search_engines"] = SearchEngine.objects.filter(is_active=True)
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    """Admin for search query analytics with custom dashboard."""

    change_list_template = "admin/search/searchquery/change_list.html"
    list_display = [
        "query",
        "result_count",
        "language",
        "is_zero_result",
        "response_time_ms",
        "created_at",
    ]
    list_filter = ["is_zero_result", "language", "engine", "created_at"]
    search_fields = ["query", "query_normalized"]
    readonly_fields = [
        "query",
        "query_normalized",
        "result_count",
        "user",
        "session_key",
        "language",
        "engine",
        "is_zero_result",
        "response_time_ms",
        "created_at",
    ]
    date_hierarchy = "created_at"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        # Allow bulk deletion for cleanup
        return request.user.is_superuser

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["search_engines"] = SearchEngine.objects.filter(is_active=True)
        # Add dashboard statistics
        from datetime import timedelta

        from django.db.models import Avg, Count
        from django.utils import timezone

        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = today_start - timedelta(days=7)
        today_start - timedelta(days=30)

        # Today's stats
        today_queries = SearchQuery.objects.filter(created_at__gte=today_start)
        extra_context["today_total"] = today_queries.count()
        extra_context["today_unique"] = today_queries.values("query_normalized").distinct().count()
        extra_context["today_zero_result"] = today_queries.filter(is_zero_result=True).count()

        # Week stats
        week_queries = SearchQuery.objects.filter(created_at__gte=week_start)
        extra_context["week_total"] = week_queries.count()

        # Average response time
        avg_response = SearchQuery.objects.filter(created_at__gte=week_start).aggregate(
            avg=Avg("response_time_ms")
        )
        extra_context["avg_response_time"] = int(avg_response["avg"] or 0)

        # Top queries this week
        extra_context["top_queries"] = (
            SearchQuery.objects.filter(created_at__gte=week_start)
            .values("query_normalized")
            .annotate(count=Count("id"))
            .order_by("-count")[:10]
        )

        # Zero result queries
        extra_context["zero_result_queries"] = (
            SearchQuery.objects.filter(created_at__gte=week_start, is_zero_result=True)
            .values("query_normalized")
            .annotate(count=Count("id"))
            .order_by("-count")[:10]
        )

        return super().changelist_view(request, extra_context=extra_context)


@admin.register(SearchClick)
class SearchClickAdmin(admin.ModelAdmin):
    """Admin for search click analytics."""

    list_display = ["search_query", "content_type", "object_id", "position", "created_at"]
    list_filter = ["content_type", "created_at"]
    search_fields = ["search_query__query"]
    readonly_fields = [
        "search_query",
        "content_type",
        "object_id",
        "position",
        "user",
        "session_key",
        "created_at",
    ]
    date_hierarchy = "created_at"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(SearchIndex)
class SearchIndexAdmin(admin.ModelAdmin):
    """Admin for document search indexes."""

    list_display = ["content_type", "object_id", "file_type", "text_preview", "indexed_at"]
    list_filter = ["file_type", "content_type", "indexed_at"]
    search_fields = ["extracted_text"]
    readonly_fields = [
        "content_type",
        "object_id",
        "extracted_text",
        "file_type",
        "checksum",
        "indexed_at",
        "created_at",
    ]

    def text_preview(self, obj):
        if obj.extracted_text:
            preview = obj.extracted_text[:100]
            if len(obj.extracted_text) > 100:
                preview += "..."
            return preview
        return "-"

    text_preview.short_description = _("Text Preview")

    def has_add_permission(self, request):
        return False
