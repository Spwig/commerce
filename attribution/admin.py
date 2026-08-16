"""Minimal admin registration for the attribution engine (P0).

Read-mostly listings so the engine's data is inspectable during development.
A merchant-facing dashboard is a later, separate workstream — this is not it.
"""

from django.contrib import admin

from .models import Attribution, AttributionSettings, Campaign, TouchPoint, VisitorThread


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "channel_hint", "is_active", "created_at")
    list_filter = ("is_active", "channel_hint")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(TouchPoint)
class TouchPointAdmin(admin.ModelAdmin):
    list_display = ("occurred_at", "channel", "source", "medium", "campaign", "customer", "is_bot")
    list_filter = ("channel", "is_bot", "consent_state")
    search_fields = ("visitor_key", "session_key", "source", "campaign", "referrer_host")
    date_hierarchy = "occurred_at"
    raw_id_fields = ("customer", "campaign_ref", "affiliate_click", "referral_event")
    readonly_fields = ("occurred_at",)


@admin.register(VisitorThread)
class VisitorThreadAdmin(admin.ModelAdmin):
    list_display = ("visitor_key", "customer", "first_seen", "last_seen")
    search_fields = ("visitor_key",)
    raw_id_fields = ("customer",)
    readonly_fields = ("first_seen", "last_seen")


@admin.register(Attribution)
class AttributionAdmin(admin.ModelAdmin):
    list_display = ("order", "channel", "role", "weight", "amount", "currency", "model_version")
    list_filter = ("channel", "role", "model_version")
    search_fields = ("order__id",)
    raw_id_fields = ("order", "touchpoint", "campaign_ref")
    readonly_fields = ("created_at",)


@admin.register(AttributionSettings)
class AttributionSettingsAdmin(admin.ModelAdmin):
    list_display = ("active_model", "lookback_days", "time_decay_half_life_days", "updated_at")

    def has_add_permission(self, request):
        # Singleton — never more than one row.
        return not AttributionSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
