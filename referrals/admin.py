"""
Admin registration for referrals app.

Enhanced admin interface with filters, actions, and inline forms.
"""

from django.contrib import admin, messages
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext

from .models import (
    ReferralAttribution,
    ReferralEvent,
    ReferralIdentity,
    ReferralProgram,
    ReferralReward,
)

# =====================================================================
# CUSTOM FILTERS
# =====================================================================


class RiskScoreFilter(admin.SimpleListFilter):
    """Filter attributions by risk score ranges."""

    title = _("Risk Level")
    parameter_name = "risk_level"

    def lookups(self, request, model_admin):
        return (
            ("low", _("Low Risk (0-30)")),
            ("medium", _("Medium Risk (31-70)")),
            ("high", _("High Risk (71-89)")),
            ("very_high", _("Very High Risk (90+)")),
        )

    def queryset(self, request, queryset):
        if self.value() == "low":
            return queryset.filter(risk_score__lte=30)
        elif self.value() == "medium":
            return queryset.filter(risk_score__gt=30, risk_score__lte=70)
        elif self.value() == "high":
            return queryset.filter(risk_score__gt=70, risk_score__lt=90)
        elif self.value() == "very_high":
            return queryset.filter(risk_score__gte=90)


class RewardExpiringFilter(admin.SimpleListFilter):
    """Filter rewards by expiration status."""

    title = _("Expiration Status")
    parameter_name = "expiring"

    def lookups(self, request, model_admin):
        return (
            ("expiring_soon", _("Expiring Soon (7 days)")),
            ("expired", _("Expired")),
            ("no_expiry", _("No Expiry")),
        )

    def queryset(self, request, queryset):
        from datetime import timedelta

        from django.utils import timezone

        if self.value() == "expiring_soon":
            seven_days = timezone.now() + timedelta(days=7)
            return queryset.filter(
                expires_at__lte=seven_days, expires_at__gt=timezone.now(), status="issued"
            )
        elif self.value() == "expired":
            return queryset.filter(expires_at__lt=timezone.now(), status="issued")
        elif self.value() == "no_expiry":
            return queryset.filter(expires_at__isnull=True)


# =====================================================================
# INLINE ADMINS
# =====================================================================


class ReferralAttributionInline(admin.TabularInline):
    """Inline admin for attributions under ReferralIdentity."""

    model = ReferralAttribution
    fk_name = "referrer_identity"
    extra = 0
    can_delete = False
    readonly_fields = ["referee_customer", "first_order", "status", "risk_score", "created_at"]
    fields = ["referee_customer", "first_order", "status", "risk_score", "created_at"]

    def has_add_permission(self, request, obj=None):
        return False


class ReferralRewardInline(admin.TabularInline):
    """Inline admin for rewards under ReferralAttribution."""

    model = ReferralReward
    fk_name = "attribution"
    extra = 0
    can_delete = False
    readonly_fields = ["customer", "recipient_type", "kind", "amount", "status", "created_at"]
    fields = ["customer", "recipient_type", "kind", "amount", "status", "created_at"]

    def has_add_permission(self, request, obj=None):
        return False


# =====================================================================
# MODEL ADMINS
# =====================================================================


@admin.register(ReferralProgram)
class ReferralProgramAdmin(admin.ModelAdmin):
    """
    Admin for ReferralProgram (singleton).
    """

    change_list_template = "admin/referrals/referralprogram/change_list.html"
    list_display = ["name", "get_status_badge", "created_at", "updated_at"]
    list_filter = ["status"]
    search_fields = ["name"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        (_("Basic Information"), {"fields": ("name", "status", "terms_and_conditions")}),
        (
            _("Reward Configuration"),
            {
                "fields": ("reward_config",),
                "classes": ("collapse",),
                "description": _(
                    "Configure referrer and referee rewards (amounts, types, double-sided)"
                ),
            },
        ),
        (
            _("Eligibility Rules"),
            {
                "fields": ("eligibility_rules",),
                "classes": ("collapse",),
                "description": _(
                    "Define minimum order values, product restrictions, customer segments"
                ),
            },
        ),
        (
            _("Timing Configuration"),
            {
                "fields": ("timing_config",),
                "classes": ("collapse",),
                "description": _("Attribution window, cookie expiry, reward issuance timing"),
            },
        ),
        (
            _("Caps & Limits"),
            {
                "fields": ("caps_config",),
                "classes": ("collapse",),
                "description": _("Per-referrer limits, per-referee limits, daily/monthly caps"),
            },
        ),
        (
            _("Tracking Configuration"),
            {
                "fields": ("tracking_config",),
                "classes": ("collapse",),
                "description": _("Cookie settings, tracking pixels, conversion events"),
            },
        ),
        (
            _("Fraud Policy"),
            {
                "fields": ("fraud_policy",),
                "classes": ("collapse",),
                "description": _("Fraud detection rules, risk scoring, auto-rejection thresholds"),
            },
        ),
        (_("Timestamps"), {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def changelist_view(self, request, extra_context=None):
        """Redirect changelist to the singleton instance."""
        from django.shortcuts import redirect
        from django.urls import reverse

        obj, created = ReferralProgram.objects.get_or_create(pk=1)
        return redirect(reverse("admin:referrals_referralprogram_change", args=[obj.pk]))

    def change_view(self, request, object_id, form_url="", extra_context=None):
        """Override to add statistics for the change form."""
        from django.db.models import Sum

        from core.utils import get_default_currency
        from core.utils.currency_helpers import get_currency_symbol
        from referrals.models import ReferralAttribution, ReferralIdentity, ReferralReward

        extra_context = extra_context or {}
        extra_context["currency_symbol"] = get_currency_symbol(get_default_currency())

        # Get the singleton program instance
        program = ReferralProgram.get_program()

        # Calculate statistics
        stats = {
            "total_referrers": ReferralIdentity.objects.count(),
            "total_clicks": ReferralIdentity.objects.aggregate(total=Sum("total_clicks"))["total"]
            or 0,
            "total_signups": ReferralIdentity.objects.aggregate(total=Sum("total_signups"))["total"]
            or 0,
            "total_conversions": ReferralIdentity.objects.aggregate(total=Sum("total_conversions"))[
                "total"
            ]
            or 0,
            "total_rewards_issued": ReferralReward.objects.filter(
                program=program, status="issued"
            ).count(),
            "total_rewards_redeemed": ReferralReward.objects.filter(
                program=program, status="redeemed"
            ).count(),
            "pending_attributions": ReferralAttribution.objects.filter(
                program=program, status="pending"
            ).count(),
            "approved_attributions": ReferralAttribution.objects.filter(
                program=program, status="approved"
            ).count(),
            "rejected_attributions": ReferralAttribution.objects.filter(
                program=program, status="rejected"
            ).count(),
        }

        extra_context["stats"] = stats

        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def get_status_badge(self, obj):
        """Display status with badge."""
        badge_classes = {
            "active": "referral-badge-success",
            "paused": "referral-badge-warning",
            "inactive": "referral-badge-danger",
        }
        cls = badge_classes.get(obj.status, "referral-badge-secondary")
        return format_html(
            '<span class="referral-badge {}">{}</span>', cls, obj.get_status_display()
        )

    get_status_badge.short_description = _("Status")

    def has_add_permission(self, request):
        """Prevent adding more than one program (singleton)."""
        return ReferralProgram.objects.count() == 0

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of the singleton instance."""
        return False


@admin.register(ReferralIdentity)
class ReferralIdentityAdmin(admin.ModelAdmin):
    """
    Admin for ReferralIdentity with inline attributions.
    """

    change_list_template = "admin/referrals/referralidentity/change_list.html"
    list_display = [
        "get_customer_name",
        "get_token_short",
        "total_clicks",
        "total_signups",
        "total_conversions",
        "get_rewards_earned",
        "created_at",
    ]
    list_filter = ["created_at"]
    search_fields = ["customer__email", "customer__first_name", "customer__last_name", "token"]
    readonly_fields = [
        "token",
        "total_clicks",
        "total_signups",
        "total_conversions",
        "total_rewards_earned",
        "created_at",
        "updated_at",
        "get_referral_link",
        "get_qr_code",
    ]
    inlines = [ReferralAttributionInline]

    class Media:
        css = {"all": ("referrals/admin/css/referral_change_list.css",)}

    fieldsets = (
        (_("Customer"), {"fields": ("customer",)}),
        (
            _("Referral Details"),
            {"fields": ("token", "get_referral_link", "get_qr_code", "qr_code")},
        ),
        (
            _("Statistics"),
            {
                "fields": (
                    "total_clicks",
                    "total_signups",
                    "total_conversions",
                    "total_rewards_earned",
                ),
                "description": _("Statistics are automatically updated by background tasks"),
            },
        ),
        (_("Timestamps"), {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def get_customer_name(self, obj):
        """Display customer name with link."""
        if obj.customer:
            url = reverse("admin:auth_user_change", args=[obj.customer.id])
            name = obj.customer.get_full_name() or obj.customer.email
            return format_html('<a href="{}">{}</a>', url, name)
        return "-"

    get_customer_name.short_description = _("Customer")

    def get_token_short(self, obj):
        """Display shortened token."""
        return format_html("<code>{}</code>", obj.token[:8])

    get_token_short.short_description = _("Token")

    def get_rewards_earned(self, obj):
        """Display rewards earned with currency."""
        from core.utils import get_default_currency
        from core.utils.currency_helpers import get_currency_symbol

        symbol = get_currency_symbol(get_default_currency())
        return format_html("<strong>{}{}</strong>", symbol, obj.total_rewards_earned)

    get_rewards_earned.short_description = _("Rewards Earned")

    def get_referral_link(self, obj):
        """Display referral link."""
        link = obj.get_referral_link()
        return format_html(
            '<input type="text" value="{}" readonly class="referral-link-input">', link
        )

    get_referral_link.short_description = _("Referral Link")

    def get_qr_code(self, obj):
        """Display QR code image if available."""
        if obj.qr_code:
            return format_html('<img src="{}" class="referral-qr-code">', obj.qr_code.url)
        return _("No QR code generated")

    get_qr_code.short_description = _("QR Code")


@admin.register(ReferralEvent)
class ReferralEventAdmin(admin.ModelAdmin):
    """
    Admin for ReferralEvent (read-only tracking).
    """

    change_list_template = "admin/referrals/referralevent/change_list.html"
    list_display = [
        "event_type",
        "get_referrer_name",
        "get_customer_name",
        "get_ip_address",
        "created_at",
    ]
    list_filter = ["event_type", "created_at"]
    search_fields = ["referrer_identity__customer__email", "customer__email", "ip_address"]
    readonly_fields = [
        "program",
        "referrer_identity",
        "customer",
        "order",
        "event_type",
        "ip_address",
        "user_agent",
        "device_fingerprint",
        "referrer_url",
        "landing_url",
        "metadata",
        "created_at",
    ]
    date_hierarchy = "created_at"

    fieldsets = (
        (_("Event Details"), {"fields": ("event_type", "program", "created_at")}),
        (_("Related Objects"), {"fields": ("referrer_identity", "customer", "order")}),
        (
            _("Tracking Data"),
            {
                "fields": (
                    "ip_address",
                    "user_agent",
                    "device_fingerprint",
                    "referrer_url",
                    "landing_url",
                    "metadata",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    def has_add_permission(self, request):
        """Events are created automatically."""
        return False

    def has_change_permission(self, request, obj=None):
        """Events are read-only."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Allow deletion for cleanup."""
        return request.user.is_superuser

    def get_referrer_name(self, obj):
        """Display referrer name."""
        if obj.referrer_identity and obj.referrer_identity.customer:
            return (
                obj.referrer_identity.customer.get_full_name()
                or obj.referrer_identity.customer.email
            )
        return "-"

    get_referrer_name.short_description = _("Referrer")

    def get_customer_name(self, obj):
        """Display customer name."""
        if obj.customer:
            return obj.customer.get_full_name() or obj.customer.email
        return "-"

    get_customer_name.short_description = _("Customer")

    def get_ip_address(self, obj):
        """Display shortened IP address."""
        if obj.ip_address:
            return obj.ip_address[:12] + "..." if len(obj.ip_address) > 12 else obj.ip_address
        return "-"

    get_ip_address.short_description = _("IP Address")


@admin.register(ReferralAttribution)
class ReferralAttributionAdmin(admin.ModelAdmin):
    """
    Admin for ReferralAttribution with approval actions.
    """

    change_list_template = "admin/referrals/referralattribution/change_list.html"
    list_display = [
        "get_referrer_name",
        "get_referee_name",
        "get_status_badge",
        "get_order_value",
        "get_risk_badge",
        "created_at",
    ]
    list_filter = ["status", "rejection_reason", RiskScoreFilter, "created_at"]
    search_fields = [
        "referrer_identity__customer__email",
        "referee_customer__email",
        "first_order__order_number",
    ]
    readonly_fields = [
        "program",
        "created_at",
        "approved_at",
        "reviewed_at",
        "validation_data",
        "get_order_link",
    ]
    date_hierarchy = "created_at"
    inlines = [ReferralRewardInline]
    actions = ["approve_attributions", "reject_attributions"]

    fieldsets = (
        (
            _("Attribution"),
            {
                "fields": (
                    "program",
                    "referrer_identity",
                    "referee_customer",
                    "first_order",
                    "get_order_link",
                )
            },
        ),
        (_("Status"), {"fields": ("status", "risk_score", "rejection_reason", "rejection_notes")}),
        (
            _("Review"),
            {"fields": ("reviewed_by", "reviewed_at", "approved_at"), "classes": ("collapse",)},
        ),
        (
            _("Validation"),
            {
                "fields": ("validation_data",),
                "classes": ("collapse",),
                "description": _("Fraud detection and validation check results"),
            },
        ),
        (_("Timestamps"), {"fields": ("created_at",), "classes": ("collapse",)}),
    )

    def get_referrer_name(self, obj):
        """Display referrer name with link."""
        if obj.referrer_identity and obj.referrer_identity.customer:
            url = reverse("admin:auth_user_change", args=[obj.referrer_identity.customer.id])
            name = (
                obj.referrer_identity.customer.get_full_name()
                or obj.referrer_identity.customer.email
            )
            return format_html('<a href="{}">{}</a>', url, name)
        return "-"

    get_referrer_name.short_description = _("Referrer")

    def get_referee_name(self, obj):
        """Display referee name with link."""
        if obj.referee_customer:
            url = reverse("admin:auth_user_change", args=[obj.referee_customer.id])
            name = obj.referee_customer.get_full_name() or obj.referee_customer.email
            return format_html('<a href="{}">{}</a>', url, name)
        return "-"

    get_referee_name.short_description = _("Referee")

    def get_status_badge(self, obj):
        """Display status with colored badge."""
        badge_classes = {
            "pending": "referral-badge-warning",
            "approved": "referral-badge-success",
            "rejected": "referral-badge-danger",
            "expired": "referral-badge-secondary",
        }
        cls = badge_classes.get(obj.status, "referral-badge-secondary")
        return format_html(
            '<span class="referral-badge {}">{}</span>', cls, obj.get_status_display()
        )

    get_status_badge.short_description = _("Status")

    def get_risk_badge(self, obj):
        """Display risk score with colored badge."""
        if obj.risk_score < 30:
            cls = "referral-badge-success"
            level = _("LOW")
        elif obj.risk_score < 70:
            cls = "referral-badge-warning"
            level = _("MEDIUM")
        elif obj.risk_score < 90:
            cls = "referral-badge-orange"
            level = _("HIGH")
        else:
            cls = "referral-badge-danger"
            level = _("CRITICAL")

        return format_html(
            '<span class="referral-badge {}">{} ({})</span>', cls, level, obj.risk_score
        )

    get_risk_badge.short_description = _("Risk")

    def get_order_value(self, obj):
        """Display order value."""
        if obj.first_order:
            return format_html("<strong>{}</strong>", obj.first_order.total_amount)
        return "-"

    get_order_value.short_description = _("Order Value")

    def get_order_link(self, obj):
        """Display order link."""
        if obj.first_order:
            url = reverse("admin:orders_order_change", args=[obj.first_order.id])
            return format_html(
                '<a href="{}" target="_blank">Order #{}</a>', url, obj.first_order.order_number
            )
        return "-"

    get_order_link.short_description = _("Order")

    @admin.action(description=_("Approve selected attributions"))
    def approve_attributions(self, request, queryset):
        """Approve selected pending attributions and create rewards."""
        from .services.rewards import create_rewards, issue_reward

        pending = queryset.filter(status="pending")
        approved_count = 0

        for attribution in pending:
            attribution.approve(reviewed_by=request.user)

            # Create and issue rewards
            try:
                referrer_reward, referee_reward = create_rewards(attribution)

                if referrer_reward:
                    issue_reward(referrer_reward)
                if referee_reward:
                    issue_reward(referee_reward)

                approved_count += 1
            except Exception as e:
                messages.error(
                    request,
                    _("Error creating rewards for attribution %(id)s: %(error)s")
                    % {"id": attribution.id, "error": e},
                )

        messages.success(
            request,
            ngettext(
                "Approved %(count)d attribution and issued rewards.",
                "Approved %(count)d attributions and issued rewards.",
                approved_count,
            )
            % {"count": approved_count},
        )

    @admin.action(description=_("Reject selected attributions"))
    def reject_attributions(self, request, queryset):
        """Reject selected pending attributions."""
        pending = queryset.filter(status="pending")

        for attribution in pending:
            attribution.reject(
                reason="manual_rejection", notes="Rejected by admin", reviewed_by=request.user
            )

        count = pending.count()
        messages.success(
            request,
            ngettext("Rejected %(count)d attribution.", "Rejected %(count)d attributions.", count)
            % {"count": count},
        )


@admin.register(ReferralReward)
class ReferralRewardAdmin(admin.ModelAdmin):
    """
    Admin for ReferralReward with issuance actions.
    """

    change_list_template = "admin/referrals/referralreward/change_list.html"
    list_display = [
        "get_customer_name",
        "get_recipient_badge",
        "get_kind_badge",
        "amount",
        "get_status_badge",
        "created_at",
        "get_expires_at",
    ]
    list_filter = ["status", "kind", "recipient_type", RewardExpiringFilter, "created_at"]
    search_fields = [
        "customer__email",
        "customer__first_name",
        "customer__last_name",
        "description",
    ]
    readonly_fields = [
        "program",
        "attribution",
        "created_at",
        "issued_at",
        "redeemed_at",
        "revoked_at",
    ]
    date_hierarchy = "created_at"
    actions = ["issue_rewards", "revoke_rewards"]

    fieldsets = (
        (
            _("Reward Details"),
            {
                "fields": (
                    "program",
                    "attribution",
                    "referrer_identity",
                    "customer",
                    "recipient_type",
                )
            },
        ),
        (_("Reward Configuration"), {"fields": ("kind", "amount", "percentage", "description")}),
        (_("Status"), {"fields": ("status", "revocation_reason")}),
        (
            _("Integration"),
            {
                "fields": ("wallet_transaction", "voucher_code_id"),
                "classes": ("collapse",),
                "description": _(
                    "Links to wallet transactions or voucher codes (populated when issued)"
                ),
            },
        ),
        (
            _("Lifecycle"),
            {
                "fields": ("created_at", "issued_at", "redeemed_at", "expires_at", "revoked_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def get_customer_name(self, obj):
        """Display customer name with link."""
        if obj.customer:
            url = reverse("admin:auth_user_change", args=[obj.customer.id])
            name = obj.customer.get_full_name() or obj.customer.email
            return format_html('<a href="{}">{}</a>', url, name)
        return "-"

    get_customer_name.short_description = _("Customer")

    def get_recipient_badge(self, obj):
        """Display recipient type badge."""
        badge_classes = {"referrer": "referral-badge-primary", "referee": "referral-badge-info"}
        cls = badge_classes.get(obj.recipient_type, "referral-badge-secondary")
        return format_html(
            '<span class="referral-badge referral-badge-sm {}">{}</span>',
            cls,
            obj.get_recipient_type_display(),
        )

    get_recipient_badge.short_description = _("Recipient")

    def get_kind_badge(self, obj):
        """Display reward kind badge."""
        badge_classes = {
            "credit": "referral-badge-success",
            "coupon": "referral-badge-warning",
            "percent": "referral-badge-orange",
            "perk": "referral-badge-purple",
        }
        cls = badge_classes.get(obj.kind, "referral-badge-secondary")
        return format_html(
            '<span class="referral-badge referral-badge-sm {}">{}</span>',
            cls,
            obj.get_kind_display(),
        )

    get_kind_badge.short_description = _("Type")

    def get_status_badge(self, obj):
        """Display status badge."""
        badge_classes = {
            "pending": "referral-badge-warning",
            "issued": "referral-badge-success",
            "redeemed": "referral-badge-primary",
            "expired": "referral-badge-secondary",
            "revoked": "referral-badge-danger",
        }
        cls = badge_classes.get(obj.status, "referral-badge-secondary")
        return format_html(
            '<span class="referral-badge {}">{}</span>', cls, obj.get_status_display()
        )

    get_status_badge.short_description = _("Status")

    def get_expires_at(self, obj):
        """Display expiration date with warning."""
        if not obj.expires_at:
            return format_html('<span class="referral-text-muted">{}</span>', _("No expiry"))

        from datetime import timedelta

        from django.utils import timezone

        if obj.expires_at < timezone.now():
            return format_html('<span class="referral-text-danger">{}</span>', _("Expired"))
        elif obj.expires_at < timezone.now() + timedelta(days=7):
            return format_html(
                '<span class="referral-text-warning">{}</span>', obj.expires_at.strftime("%Y-%m-%d")
            )
        else:
            return obj.expires_at.strftime("%Y-%m-%d")

    get_expires_at.short_description = _("Expires")

    @admin.action(description=_("Issue selected pending rewards"))
    def issue_rewards(self, request, queryset):
        """Issue selected pending rewards."""
        from .services.rewards import issue_reward

        pending = queryset.filter(status="pending")
        issued_count = 0

        for reward in pending:
            try:
                success = issue_reward(reward)
                if success:
                    issued_count += 1
                else:
                    messages.warning(
                        request, _("Failed to issue reward %(id)s") % {"id": reward.id}
                    )
            except Exception as e:
                messages.error(
                    request,
                    _("Error issuing reward %(id)s: %(error)s") % {"id": reward.id, "error": e},
                )

        messages.success(
            request,
            ngettext("Issued %(count)d reward.", "Issued %(count)d rewards.", issued_count)
            % {"count": issued_count},
        )

    @admin.action(description=_("Revoke selected issued rewards"))
    def revoke_rewards(self, request, queryset):
        """Revoke selected issued rewards."""
        from .services.rewards import revoke_reward

        issued = queryset.filter(status="issued")
        revoked_count = 0

        for reward in issued:
            try:
                success = revoke_reward(reward, reason="Admin revocation")
                if success:
                    revoked_count += 1
            except Exception as e:
                messages.error(
                    request,
                    _("Error revoking reward %(id)s: %(error)s") % {"id": reward.id, "error": e},
                )

        messages.success(
            request,
            ngettext("Revoked %(count)d reward.", "Revoked %(count)d rewards.", revoked_count)
            % {"count": revoked_count},
        )
