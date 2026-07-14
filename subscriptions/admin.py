"""
Django Admin for Subscription Management
"""

import json
from decimal import Decimal

from django import forms
from django.contrib import admin, messages
from django.shortcuts import redirect, render
from django.urls import path
from django.utils.html import format_html
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from core.admin_mixins import TranslatableAdminMixin
from core.widgets import TranslatableFieldWidget

from .models import (
    BillingCycleLog,
    CustomerSubscription,
    CustomerSubscriptionAddon,
    PaymentToken,
    PlanAddon,
    PlanPricingTier,
    SubscriptionDiscount,
    SubscriptionPlan,
)


class SubscriptionPlanForm(forms.ModelForm):
    """Form for subscription plans with translatable fields"""

    class Meta:
        model = SubscriptionPlan
        fields = "__all__"
        widgets = {
            "name": TranslatableFieldWidget(
                base_widget=forms.TextInput(attrs={"class": "vTextField", "style": "width: 100%;"})
            ),
            "description": TranslatableFieldWidget(
                base_widget=forms.Textarea(
                    attrs={"rows": 4, "class": "vLargeTextField", "style": "width: 100%;"}
                )
            ),
        }


class PlanPricingTierForm(forms.ModelForm):
    """Form for pricing tiers with translatable fields"""

    class Meta:
        model = PlanPricingTier
        fields = "__all__"
        widgets = {
            "tier_name": TranslatableFieldWidget(
                base_widget=forms.TextInput(attrs={"class": "vTextField", "style": "width: 100%;"})
            ),
        }
        help_texts = {
            "discount_percentage": _(
                "Discount applied to product price when customer subscribes (0 for full price, 10 for 10% off, etc.)"
            ),
        }

    def clean_discount_percentage(self):
        """Validate discount percentage is set"""
        discount = self.cleaned_data.get("discount_percentage")
        if discount is None:
            raise forms.ValidationError(
                _("Discount percentage is required (use 0 for no discount)")
            )
        if discount < 0 or discount > 100:
            raise forms.ValidationError(_("Discount must be between 0% and 100%"))
        return discount


class PlanAddonForm(forms.ModelForm):
    """Form for plan add-ons with translatable fields"""

    class Meta:
        model = PlanAddon
        fields = "__all__"
        widgets = {
            "name": TranslatableFieldWidget(
                base_widget=forms.TextInput(attrs={"class": "vTextField", "style": "width: 100%;"})
            ),
            "description": TranslatableFieldWidget(
                base_widget=forms.Textarea(
                    attrs={"rows": 3, "class": "vLargeTextField", "style": "width: 100%;"}
                )
            ),
        }


class PlanPricingTierInline(admin.TabularInline):
    """Inline for pricing tiers (subscription templates use product prices)"""

    model = PlanPricingTier
    form = PlanPricingTierForm
    extra = 1
    fields = [
        "tier_name",
        "billing_cycle",
        "billing_interval",
        "discount_percentage",
        "is_default",
        "is_active",
    ]


class PlanAddonInline(admin.TabularInline):
    """Inline for plan add-ons"""

    model = PlanAddon
    form = PlanAddonForm
    extra = 1
    fields = [
        "name",
        "description",
        "price",
        "billing_frequency",
        "allow_quantity",
        "is_required",
        "is_active",
    ]


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(TranslatableAdminMixin, admin.ModelAdmin):
    """Admin interface for subscription plans"""

    form = SubscriptionPlanForm
    translatable_fields = ["name", "description"]
    inlines = [PlanPricingTierInline, PlanAddonInline]
    change_list_template = "admin/subscriptions/subscriptionplan/change_list.html"

    class Media:
        css = {
            "all": (
                "utilities/translation_editor/current/translation_editor.css",
                "subscriptions/css/subscription-admin.css",
            )
        }
        js = ("utilities/translation_editor/current/translation_editor.js",)

    list_display = [
        "name",
        "pricing_model",
        "active_subscriptions_count",
        "is_active",
        "is_public",
        "created_at",
    ]

    list_filter = [
        "is_active",
        "is_public",
        "pricing_model",
        "cancellation_policy",
        "created_at",
    ]

    search_fields = [
        "name",
        "slug",
        "description",
    ]

    readonly_fields = [
        "plan_id",
        "created_at",
        "updated_at",
        "active_subscriptions_count",
        "total_revenue_display",
    ]

    fieldsets = (
        (
            _("Plan Information"),
            {
                "fields": (
                    "plan_id",
                    "name",
                    "slug",
                    "description",
                )
            },
        ),
        (
            _("Pricing Configuration"),
            {
                "fields": (
                    "pricing_model",
                    "allow_quantity",
                    "minimum_quantity",
                    "maximum_quantity",
                )
            },
        ),
        (
            _("Trial Period"),
            {
                "fields": (
                    "trial_period_days",
                    "trial_price",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Cancellation Policy"),
            {
                "fields": (
                    "cancellation_policy",
                    "minimum_commitment_cycles",
                    "grace_period_days",
                    "reactivation_period_days",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Plan Change Behavior"),
            {
                "fields": (
                    "upgrade_behavior",
                    "downgrade_behavior",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Limits & Restrictions"),
            {
                "fields": ("max_billing_cycles",),
                "classes": ("collapse",),
            },
        ),
        (
            _("Status"),
            {
                "fields": (
                    "is_active",
                    "is_public",
                )
            },
        ),
        (
            _("Provider Integration"),
            {
                "fields": ("provider_plan_mappings",),
                "classes": ("collapse",),
                "description": _(
                    'Map this plan to provider-specific plan IDs (e.g., {"stripe": "price_xxx", "paypal": "P-xxx"})'
                ),
            },
        ),
        (
            _("Statistics"),
            {
                "fields": (
                    "active_subscriptions_count",
                    "total_revenue_display",
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    prepopulated_fields = {"slug": ("name",)}

    def get_urls(self):
        """Add wizard URL to admin URLs"""
        urls = super().get_urls()
        custom_urls = [
            path(
                "wizard/",
                self.admin_site.admin_view(self.wizard_view),
                name="subscriptions_subscriptionplan_wizard",
            ),
        ]
        return custom_urls + urls

    def wizard_view(self, request):
        """Handle the subscription plan wizard"""
        if request.method == "POST":
            try:
                # Extract form data
                name = request.POST.get("name", "").strip()
                description = request.POST.get("description", "").strip()
                pricing_model = request.POST.get("pricing_model", "tiered")

                # Generate slug
                slug = slugify(name)

                # Validate required fields
                if not name:
                    messages.error(request, _("Plan name is required"))
                    return render(request, "admin/subscriptions/subscriptionplan/wizard.html")

                # Trial & Setup
                trial_period_days = int(request.POST.get("trial_period_days", 0))
                trial_price_value = request.POST.get("trial_price", "").strip()
                trial_price = Decimal(trial_price_value) if trial_price_value else None
                setup_fee = Decimal(request.POST.get("setup_fee", "0.00"))

                # Quantity settings
                allow_quantity = request.POST.get("allow_quantity") == "on"
                minimum_quantity = int(request.POST.get("minimum_quantity", 1))
                maximum_quantity_str = request.POST.get("maximum_quantity", "").strip()
                maximum_quantity = int(maximum_quantity_str) if maximum_quantity_str else None

                # Billing limits
                max_billing_cycles_str = request.POST.get("max_billing_cycles", "").strip()
                max_billing_cycles = int(max_billing_cycles_str) if max_billing_cycles_str else None

                # Cancellation policy
                cancellation_policy = request.POST.get("cancellation_policy", "end_of_period")
                minimum_commitment_cycles = int(request.POST.get("minimum_commitment_cycles", 0))
                grace_period_days = int(request.POST.get("grace_period_days", 0))
                reactivation_period_days = int(request.POST.get("reactivation_period_days", 0))

                # Visibility & Status
                is_active = request.POST.get("is_active") == "on"
                is_public = request.POST.get("is_public") == "on"
                sort_order = int(request.POST.get("sort_order", 0))

                # Parse tiers data
                tiers_data_json = request.POST.get("tiers_data", "[]")
                tiers_data = json.loads(tiers_data_json)

                if not tiers_data:
                    messages.error(request, _("At least one pricing tier is required"))
                    return render(request, "admin/subscriptions/subscriptionplan/wizard.html")

                # Create subscription plan
                plan = SubscriptionPlan.objects.create(
                    name=name,
                    slug=slug,
                    description=description,
                    pricing_model=pricing_model,
                    allow_quantity=allow_quantity,
                    minimum_quantity=minimum_quantity,
                    maximum_quantity=maximum_quantity,
                    trial_period_days=trial_period_days,
                    trial_price=trial_price,
                    setup_fee=setup_fee,
                    max_billing_cycles=max_billing_cycles,
                    cancellation_policy=cancellation_policy,
                    minimum_commitment_cycles=minimum_commitment_cycles,
                    grace_period_days=grace_period_days,
                    reactivation_period_days=reactivation_period_days,
                    is_active=is_active,
                    is_public=is_public,
                    sort_order=sort_order,
                )

                # Create pricing tiers
                for tier_data in tiers_data:
                    PlanPricingTier.objects.create(
                        plan=plan,
                        tier_name=tier_data["tier_name"],
                        billing_cycle=tier_data["billing_cycle"],
                        billing_interval=int(tier_data["billing_interval"]),
                        discount_percentage=Decimal(tier_data["discount_percentage"]),
                        is_default=tier_data.get("is_default", False),
                        is_active=True,
                    )

                messages.success(
                    request,
                    _(
                        "Subscription plan '{}' created successfully! You can now add translations and configure additional settings."
                    ).format(name),
                )
                return redirect("admin:subscriptions_subscriptionplan_change", plan.pk)

            except Exception as e:
                messages.error(request, _("Error creating subscription plan: {}").format(str(e)))
                return render(request, "admin/subscriptions/subscriptionplan/wizard.html")

        # GET request - show wizard
        return render(request, "admin/subscriptions/subscriptionplan/wizard.html")

    def changelist_view(self, request, extra_context=None):
        """Override to handle AJAX filtering requests"""
        extra_context = extra_context or {}

        # Store original GET parameters for our custom filters
        # Strip custom filter params from request.GET to prevent Django's ChangeList from trying to use them
        original_get = request.GET.copy()
        request._custom_filters = original_get  # Store for get_queryset to use

        # Strip our custom filter parameters from request.GET
        custom_filter_params = [
            "filter_search",
            "filter_pricing_model",
            "filter_status",
            "filter_visibility",
            "filter_cancellation_policy",
            "filter_trial_period",
            "ajax",
        ]

        # Create a mutable copy of GET parameters without custom filters
        get_params = request.GET.copy()
        for param in custom_filter_params:
            get_params.pop(param, None)

        # Replace request.GET with cleaned parameters
        request.GET = get_params

        # Check if this is an AJAX request (check original params since we removed 'ajax')
        is_ajax = (
            original_get.get("ajax") == "1"
            or request.headers.get("X-Requested-With") == "XMLHttpRequest"
        )

        if is_ajax:
            # Get filtered queryset
            cl = self.get_changelist_instance(request)

            # Render only the plan cards partial
            from django.template.loader import render_to_string

            html = render_to_string(
                "admin/subscriptions/partials/plan_cards.html",
                {"plans": cl.result_list},
                request=request,  # Pass request for context processors (i18n, static, etc.)
            )

            from django.http import HttpResponse

            return HttpResponse(html)

        # Add subscription-admin-container class to context
        extra_context["subscription_admin"] = True

        return super().changelist_view(request, extra_context)

    def get_queryset(self, request):
        """Override to add custom filtering from filter panel"""
        qs = super().get_queryset(request)

        # Get custom filter parameters (stored by changelist_view to avoid conflicts with Django's ChangeList)
        custom_filters = getattr(request, "_custom_filters", request.GET)

        # Apply custom filters from filter panel
        search_query = custom_filters.get("filter_search", "").strip()
        if search_query:
            from django.db.models import Q

            qs = qs.filter(
                Q(name__icontains=search_query)
                | Q(slug__icontains=search_query)
                | Q(description__icontains=search_query)
            )

        pricing_model = custom_filters.get("filter_pricing_model", "").strip()
        if pricing_model:
            qs = qs.filter(pricing_model=pricing_model)

        status = custom_filters.get("filter_status", "").strip()
        if status:
            is_active = status == "active"
            qs = qs.filter(is_active=is_active)

        visibility = custom_filters.get("filter_visibility", "").strip()
        if visibility:
            is_public = visibility == "public"
            qs = qs.filter(is_public=is_public)

        cancellation_policy = custom_filters.get("filter_cancellation_policy", "").strip()
        if cancellation_policy:
            qs = qs.filter(cancellation_policy=cancellation_policy)

        trial_period = custom_filters.get("filter_trial_period", "").strip()
        if trial_period == "with_trial":
            qs = qs.filter(trial_period_days__gt=0)
        elif trial_period == "no_trial":
            qs = qs.filter(trial_period_days=0)

        return qs

    def get_form(self, request, obj=None, **kwargs):
        """Override to filter MoneyField currency choices"""
        form = super().get_form(request, obj, **kwargs)
        from core.admin_mixins import _apply_money_field_currency_defaults

        _apply_money_field_currency_defaults(form, obj)
        return form

    def active_subscriptions_count(self, obj):
        """Count of active subscriptions using this plan"""
        count = obj.subscriptions.filter(status__in=["active", "trial"]).count()
        return count

    active_subscriptions_count.short_description = _("Active Subscriptions")

    def total_revenue_display(self, obj):
        """Total revenue generated from this plan"""
        from django.db.models import Sum

        total = obj.subscriptions.filter(billing_logs__status="successful").aggregate(
            total=Sum("billing_logs__total_amount")
        )["total"]

        if total:
            # Assuming USD for display - would need to handle multi-currency properly
            return f"${total:,.2f}"
        return "$0.00"

    total_revenue_display.short_description = _("Total Revenue")


@admin.register(PaymentToken)
class PaymentTokenAdmin(admin.ModelAdmin):
    """Admin interface for payment tokens"""

    list_display = [
        "user",
        "payment_method_display",
        "provider_account",
        "is_default",
        "is_active",
        "is_verified",
        "expiry_status",
        "created_at",
    ]

    list_filter = [
        "payment_method_type",
        "is_default",
        "is_active",
        "is_verified",
        "provider_account",
        "created_at",
    ]

    search_fields = [
        "user__username",
        "user__email",
        "gateway_customer_id",
        "card_last4",
    ]

    readonly_fields = [
        "token_id",
        "gateway_token_id",
        "created_at",
        "updated_at",
        "expiry_status",
    ]

    fieldsets = (
        (
            _("Token Information"),
            {
                "fields": (
                    "token_id",
                    "user",
                    "provider_account",
                )
            },
        ),
        (
            _("Provider Details"),
            {
                "fields": (
                    "gateway_customer_id",
                    "gateway_token_id",
                )
            },
        ),
        (
            _("Payment Method"),
            {
                "fields": (
                    "payment_method_type",
                    "card_brand",
                    "card_last4",
                    "card_exp_month",
                    "card_exp_year",
                    "expiry_status",
                )
            },
        ),
        (
            _("Status"),
            {
                "fields": (
                    "is_default",
                    "is_active",
                    "is_verified",
                )
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    def payment_method_display(self, obj):
        """Display payment method with details"""
        if obj.payment_method_type == "card":
            brand = obj.card_brand.upper() if obj.card_brand else "Card"
            return f"{brand} •••• {obj.card_last4}"
        return obj.get_payment_method_type_display()

    payment_method_display.short_description = _("Payment Method")

    def expiry_status(self, obj):
        """Display expiry status with color coding"""
        if obj.payment_method_type != "card":
            return "-"

        if obj.is_expired():
            return format_html('<span class="sub-status sub-status-error">{}</span>', _("Expired"))
        elif obj.card_exp_month and obj.card_exp_year:
            from datetime import date

            today = date.today()
            expiry_date = date(obj.card_exp_year, obj.card_exp_month, 1)

            # Warning if expires within 60 days
            if expiry_date.year == today.year and expiry_date.month - today.month <= 2:
                return format_html(
                    '<span class="sub-status sub-status-warning">{} ({}/{})</span>',
                    _("Expires Soon"),
                    obj.card_exp_month,
                    obj.card_exp_year,
                )

            return f"{obj.card_exp_month}/{obj.card_exp_year}"

        return "-"

    expiry_status.short_description = _("Expiry")


@admin.register(PlanPricingTier)
class PlanPricingTierAdmin(TranslatableAdminMixin, admin.ModelAdmin):
    """Admin interface for pricing tiers"""

    form = PlanPricingTierForm
    translatable_fields = ["tier_name"]

    class Media:
        css = {"all": ("utilities/translation_editor/current/translation_editor.css",)}
        js = ("utilities/translation_editor/current/translation_editor.js",)

    list_display = [
        "tier_name",
        "plan",
        "billing_cycle_display",
        "discount_percentage",
        "is_default",
        "is_active",
    ]

    list_filter = [
        "plan",
        "billing_cycle",
        "is_default",
        "is_active",
    ]

    search_fields = [
        "tier_name",
        "plan__name",
    ]

    readonly_fields = [
        "tier_id",
        "created_at",
        "updated_at",
    ]

    fieldsets = (
        (
            _("Tier Information"),
            {
                "fields": (
                    "tier_id",
                    "plan",
                    "tier_name",
                )
            },
        ),
        (
            _("Billing Configuration"),
            {
                "fields": (
                    "billing_cycle",
                    "billing_interval",
                    "discount_percentage",
                )
            },
        ),
        (
            _("Status"),
            {
                "fields": (
                    "is_default",
                    "is_active",
                )
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    def billing_cycle_display(self, obj):
        """Display billing cycle with interval"""
        if obj.billing_interval == 1:
            return obj.get_billing_cycle_display()
        return f"Every {obj.billing_interval} {obj.get_billing_cycle_display()}s"

    billing_cycle_display.short_description = _("Billing Cycle")


@admin.register(PlanAddon)
class PlanAddonAdmin(TranslatableAdminMixin, admin.ModelAdmin):
    """Admin interface for plan add-ons"""

    form = PlanAddonForm
    translatable_fields = ["name", "description"]

    class Media:
        css = {"all": ("utilities/translation_editor/current/translation_editor.css",)}
        js = ("utilities/translation_editor/current/translation_editor.js",)

    list_display = [
        "name",
        "plan",
        "price",
        "billing_frequency",
        "allow_quantity",
        "is_required",
        "is_active",
    ]

    list_filter = [
        "plan",
        "billing_frequency",
        "allow_quantity",
        "is_required",
        "is_active",
    ]

    search_fields = [
        "name",
        "description",
        "plan__name",
    ]

    readonly_fields = [
        "addon_id",
        "created_at",
        "updated_at",
    ]

    fieldsets = (
        (
            _("Add-on Information"),
            {
                "fields": (
                    "addon_id",
                    "plan",
                    "name",
                    "description",
                )
            },
        ),
        (
            _("Pricing"),
            {
                "fields": (
                    "price",
                    "billing_frequency",
                    "allow_quantity",
                )
            },
        ),
        (
            _("Status"),
            {
                "fields": (
                    "is_required",
                    "is_active",
                )
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )


class BillingCycleLogInline(admin.TabularInline):
    """Inline for billing cycle logs"""

    model = BillingCycleLog
    extra = 0
    can_delete = False

    fields = [
        "cycle_number",
        "billing_date",
        "total_amount",
        "status",
        "retry_count",
        "error_message",
    ]

    readonly_fields = [
        "cycle_number",
        "billing_date",
        "total_amount",
        "status",
        "retry_count",
        "error_message",
    ]

    def has_add_permission(self, request, obj=None):
        return False


class CustomerSubscriptionAddonInline(admin.TabularInline):
    """Inline for subscription add-ons on CustomerSubscription"""

    model = CustomerSubscriptionAddon
    extra = 0
    fields = [
        "addon",
        "quantity",
        "is_active",
        "activated_at",
        "deactivated_at",
    ]
    readonly_fields = ["activated_at"]


@admin.register(CustomerSubscription)
class CustomerSubscriptionAdmin(admin.ModelAdmin):
    """Admin interface for customer subscriptions"""

    change_list_template = "admin/subscriptions/customersubscription/change_list.html"
    change_form_template = "admin/subscriptions/customersubscription/change_form.html"

    class Media:
        css = {
            "all": (
                "subscriptions/css/subscription-admin.css",
                "subscriptions/css/customersubscription_change_form.css",
            )
        }
        js = ("subscriptions/js/customersubscription_change_form.js",)

    list_display = [
        "subscription_id_short",
        "user",
        "plan",
        "status_display",
        "provider_mode",
        "next_billing_date",
        "billing_cycle_count",
        "created_at",
    ]

    list_filter = [
        "status",
        "provider_mode",
        "payment_provider_account",
        "plan",
        "product",
        "cancellation_type",
        "created_at",
    ]

    search_fields = [
        "subscription_id",
        "user__username",
        "user__email",
        "provider_subscription_id",
    ]

    readonly_fields = [
        "subscription_id",
        "provider_subscription_id",
        "created_at",
        "updated_at",
        "days_until_next_billing_display",
        "total_amount_paid_display",
        "grace_period_end_date",
        "reactivation_deadline",
        "scheduled_plan_change",
        "proration_credit",
    ]

    fieldsets = (
        (
            _("Subscription Information"),
            {
                "fields": (
                    "subscription_id",
                    "user",
                    "plan",
                    "pricing_tier",
                    "product",
                    "variant",
                ),
                "classes": ("tab-subscription",),
            },
        ),
        (
            _("Payment Configuration"),
            {
                "fields": (
                    "payment_provider_account",
                    "payment_token",
                    "provider_mode",
                    "provider_subscription_id",
                ),
                "classes": ("tab-payment",),
            },
        ),
        (
            _("Status"),
            {
                "fields": (
                    "status",
                    "cancellation_type",
                    "quantity",
                    "grace_period_end_date",
                ),
                "classes": ("tab-lifecycle",),
            },
        ),
        (
            _("Billing Schedule"),
            {
                "fields": (
                    "current_period_start",
                    "current_period_end",
                    "next_billing_date",
                    "days_until_next_billing_display",
                    "trial_end_date",
                ),
                "classes": ("tab-billing",),
            },
        ),
        (
            _("Billing History"),
            {
                "fields": (
                    "billing_cycle_count",
                    "last_billing_date",
                    "last_billing_status",
                    "total_amount_paid_display",
                ),
                "classes": ("tab-billing",),
            },
        ),
        (
            _("Cancellation"),
            {
                "fields": (
                    "canceled_at",
                    "cancellation_reason",
                    "reactivation_deadline",
                ),
                "classes": ("tab-lifecycle",),
            },
        ),
        (
            _("Pause/Resume"),
            {
                "fields": (
                    "paused_at",
                    "pause_reason",
                    "auto_resume_date",
                ),
                "classes": ("tab-lifecycle",),
            },
        ),
        (
            _("Plan Changes"),
            {
                "fields": (
                    "scheduled_plan_change",
                    "proration_credit",
                ),
                "classes": ("tab-lifecycle",),
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": ("tab-metadata",),
            },
        ),
    )

    inlines = [BillingCycleLogInline, CustomerSubscriptionAddonInline]

    actions = [
        "cancel_subscriptions",
        "pause_subscriptions",
        "resume_subscriptions",
    ]

    def subscription_id_short(self, obj):
        """Display shortened subscription ID"""
        return str(obj.subscription_id)[:8] + "..."

    subscription_id_short.short_description = _("ID")

    def status_display(self, obj):
        """Display status with color coding"""
        css_classes = {
            "trial": "sub-status-info",
            "active": "sub-status-success",
            "past_due": "sub-status-error",
            "paused": "sub-status-warning",
            "canceled": "sub-status-muted",
            "expired": "sub-status-muted",
        }

        css_class = css_classes.get(obj.status, "")

        html = format_html(
            '<span class="sub-status {}">{}</span>', css_class, obj.get_status_display()
        )

        if obj.cancellation_type == "end_of_period":
            html += format_html(
                '<br><small class="sub-status-note sub-status-error">{}</small>',
                _("Cancels at period end"),
            )
        elif obj.cancellation_type == "immediate":
            html += format_html(
                '<br><small class="sub-status-note sub-status-error">{}</small>',
                _("Canceled immediately"),
            )

        return html

    status_display.short_description = _("Status")

    def days_until_next_billing_display(self, obj):
        """Display days until next billing"""
        days = obj.days_until_next_billing()
        if days is None:
            return "-"

        if days == 0:
            return format_html('<span class="sub-status sub-status-error">{}</span>', _("Today"))
        elif days <= 7:
            return format_html(
                '<span class="sub-status sub-status-warning">{} {}</span>', days, _("days")
            )
        else:
            return format_html("{} {}", days, _("days"))

    days_until_next_billing_display.short_description = _("Days Until Billing")

    def total_amount_paid_display(self, obj):
        """Display total amount paid"""
        total = obj.total_amount_paid()
        if total:
            return f"${total:,.2f}"
        return "$0.00"

    total_amount_paid_display.short_description = _("Total Paid")

    def cancel_subscriptions(self, request, queryset):
        """Bulk cancel subscriptions"""
        from .manager import SubscriptionManager

        canceled_count = 0
        for subscription in queryset:
            try:
                if subscription.status not in ["canceled", "expired"]:
                    manager = SubscriptionManager(subscription.payment_provider_account)
                    manager.cancel_subscription(
                        subscription, immediately=False, reason="Canceled by admin"
                    )
                    canceled_count += 1
            except Exception as e:
                self.message_user(
                    request,
                    f"Error canceling {subscription.subscription_id}: {str(e)}",
                    level="error",
                )

        self.message_user(
            request,
            f"Successfully canceled {canceled_count} subscription(s) at period end",
            level="success",
        )

    cancel_subscriptions.short_description = _("Cancel selected subscriptions at period end")

    def pause_subscriptions(self, request, queryset):
        """Bulk pause subscriptions"""
        from .manager import SubscriptionManager

        paused_count = 0
        for subscription in queryset:
            try:
                if subscription.status in ["active", "trial"]:
                    manager = SubscriptionManager(subscription.payment_provider_account)
                    manager.pause_subscription(subscription, reason="Paused by admin")
                    paused_count += 1
            except Exception as e:
                self.message_user(
                    request,
                    f"Error pausing {subscription.subscription_id}: {str(e)}",
                    level="error",
                )

        self.message_user(
            request, f"Successfully paused {paused_count} subscription(s)", level="success"
        )

    pause_subscriptions.short_description = _("Pause selected subscriptions")

    def resume_subscriptions(self, request, queryset):
        """Bulk resume subscriptions"""
        from .manager import SubscriptionManager

        resumed_count = 0
        for subscription in queryset:
            try:
                if subscription.status == "paused":
                    manager = SubscriptionManager(subscription.payment_provider_account)
                    manager.resume_subscription(subscription)
                    resumed_count += 1
            except Exception as e:
                self.message_user(
                    request,
                    f"Error resuming {subscription.subscription_id}: {str(e)}",
                    level="error",
                )

        self.message_user(
            request, f"Successfully resumed {resumed_count} subscription(s)", level="success"
        )

    resume_subscriptions.short_description = _("Resume selected subscriptions")

    def change_view(self, request, object_id, form_url="", extra_context=None):
        """Override to pass dashboard stats to template"""
        extra_context = extra_context or {}
        obj = self.get_object(request, object_id)
        if obj:
            extra_context["days_until_billing"] = obj.days_until_next_billing()
            extra_context["total_paid"] = obj.total_amount_paid()
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def changelist_view(self, request, extra_context=None):
        """Override to handle AJAX filtering requests and pass filter options"""
        extra_context = extra_context or {}

        # Store original GET parameters for our custom filters
        # We need to strip custom filter params from request.GET to prevent Django's ChangeList from trying to use them
        original_get = request.GET.copy()
        request._custom_filters = original_get  # Store for get_queryset to use

        # Strip our custom filter parameters from request.GET
        custom_filter_params = [
            "filter_search",
            "filter_status",
            "filter_plan",
            "filter_product",
            "filter_provider_mode",
            "filter_payment_provider",
            "ajax",
        ]

        # Create a mutable copy of GET parameters without custom filters
        get_params = request.GET.copy()
        for param in custom_filter_params:
            get_params.pop(param, None)

        # Replace request.GET with cleaned parameters
        request.GET = get_params

        # Check if this is an AJAX request (check original params since we removed 'ajax')
        is_ajax = (
            original_get.get("ajax") == "1"
            or request.headers.get("X-Requested-With") == "XMLHttpRequest"
        )

        if is_ajax:
            # Get filtered queryset
            cl = self.get_changelist_instance(request)

            # Render only the subscription cards partial
            from django.template.loader import render_to_string

            html = render_to_string(
                "admin/subscriptions/partials/subscription_cards.html",
                {"subscriptions": cl.result_list},
                request=request,  # Pass request for context processors (i18n, static, etc.)
            )

            from django.http import HttpResponse

            return HttpResponse(html)

        # Pass filter options to template
        from catalog.models import Product
        from payment_providers.models import PaymentProviderAccount

        extra_context["products"] = Product.objects.filter(status="published").order_by("name")
        extra_context["plans"] = SubscriptionPlan.objects.filter(is_active=True).order_by("name")
        extra_context["payment_providers"] = PaymentProviderAccount.objects.filter(
            is_active=True
        ).order_by("display_name")

        return super().changelist_view(request, extra_context=extra_context)

    def get_queryset(self, request):
        """Override to add custom filtering from filter panel"""
        qs = super().get_queryset(request)

        # Get custom filter parameters (stored by changelist_view to avoid conflicts with Django's ChangeList)
        custom_filters = getattr(request, "_custom_filters", request.GET)

        # Apply custom filters from filter panel
        search_query = custom_filters.get("filter_search", "").strip()
        if search_query:
            from django.db.models import Q

            qs = qs.filter(
                Q(subscription_id__icontains=search_query)
                | Q(user__username__icontains=search_query)
                | Q(user__email__icontains=search_query)
                | Q(user__first_name__icontains=search_query)
                | Q(user__last_name__icontains=search_query)
                | Q(provider_subscription_id__icontains=search_query)
            )

        status = custom_filters.get("filter_status", "").strip()
        if status:
            qs = qs.filter(status=status)

        plan_id = custom_filters.get("filter_plan", "").strip()
        if plan_id:
            qs = qs.filter(plan_id=plan_id)

        product_id = custom_filters.get("filter_product", "").strip()
        if product_id:
            qs = qs.filter(product_id=product_id)

        provider_mode = custom_filters.get("filter_provider_mode", "").strip()
        if provider_mode:
            qs = qs.filter(provider_mode=provider_mode)

        payment_provider_id = custom_filters.get("filter_payment_provider", "").strip()
        if payment_provider_id:
            qs = qs.filter(payment_provider_account_id=payment_provider_id)

        return qs


@admin.register(BillingCycleLog)
class BillingCycleLogAdmin(admin.ModelAdmin):
    """Admin interface for billing cycle logs"""

    list_display = [
        "subscription",
        "cycle_number",
        "billing_date",
        "total_amount",
        "status_display",
        "retry_count",
    ]

    list_filter = [
        "status",
        "billing_date",
    ]

    search_fields = [
        "subscription__subscription_id",
        "subscription__user__username",
        "subscription__user__email",
    ]

    readonly_fields = [
        "subscription",
        "cycle_number",
        "billing_date",
        "base_amount",
        "quantity_amount",
        "addons_amount",
        "discount_amount",
        "tax_amount",
        "proration_amount",
        "total_amount",
        "status",
        "transaction",
        "order",
        "retry_count",
        "next_retry_date",
        "max_retries",
        "error_message",
        "error_code",
        "provider_response",
    ]

    fieldsets = (
        (
            _("Billing Cycle"),
            {
                "fields": (
                    "subscription",
                    "cycle_number",
                    "billing_date",
                )
            },
        ),
        (
            _("Billing Breakdown"),
            {
                "fields": (
                    "base_amount",
                    "quantity_amount",
                    "addons_amount",
                    "discount_amount",
                    "tax_amount",
                    "proration_amount",
                    "total_amount",
                )
            },
        ),
        (
            _("Status"),
            {
                "fields": (
                    "status",
                    "transaction",
                    "order",
                )
            },
        ),
        (
            _("Retry Management"),
            {
                "fields": (
                    "retry_count",
                    "max_retries",
                    "next_retry_date",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Error Details"),
            {
                "fields": (
                    "error_message",
                    "error_code",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Provider Response"),
            {
                "fields": ("provider_response",),
                "classes": ("collapse",),
            },
        ),
    )

    def has_add_permission(self, request):
        """Billing logs are created automatically"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Keep billing logs for audit trail"""
        return False

    def status_display(self, obj):
        """Display status with color coding"""
        css_classes = {
            "pending": "sub-status-info",
            "processing": "sub-status-warning",
            "successful": "sub-status-success",
            "failed": "sub-status-error",
            "retrying": "sub-status-warning",
        }

        css_class = css_classes.get(obj.status, "")

        return format_html(
            '<span class="sub-status {}">{}</span>', css_class, obj.get_status_display()
        )

    status_display.short_description = _("Status")


@admin.register(CustomerSubscriptionAddon)
class CustomerSubscriptionAddonAdmin(admin.ModelAdmin):
    """Admin interface for customer subscription add-ons"""

    list_display = [
        "subscription",
        "addon",
        "quantity",
        "is_active",
        "activated_at",
    ]

    list_filter = [
        "is_active",
        "addon__plan",
        "activated_at",
    ]

    search_fields = [
        "subscription__subscription_id",
        "subscription__user__email",
        "addon__name",
    ]

    readonly_fields = [
        "activated_at",
    ]

    fieldsets = (
        (
            _("Add-on Details"),
            {
                "fields": (
                    "subscription",
                    "addon",
                    "quantity",
                )
            },
        ),
        (
            _("Status"),
            {
                "fields": (
                    "is_active",
                    "activated_at",
                    "deactivated_at",
                )
            },
        ),
    )


@admin.register(SubscriptionDiscount)
class SubscriptionDiscountAdmin(admin.ModelAdmin):
    """Admin interface for subscription discounts"""

    list_display = [
        "subscription",
        "discount_display",
        "discount_type",
        "duration_type",
        "is_active",
        "applied_at",
    ]

    list_filter = [
        "discount_type",
        "duration_type",
        "is_active",
        "applied_at",
    ]

    search_fields = [
        "subscription__subscription_id",
        "subscription__user__email",
        "coupon_code",
    ]

    readonly_fields = [
        "applied_at",
    ]

    fieldsets = (
        (
            _("Discount Details"),
            {
                "fields": (
                    "subscription",
                    "coupon_code",
                    "discount_type",
                    "value",
                )
            },
        ),
        (
            _("Duration"),
            {
                "fields": (
                    "duration_type",
                    "duration_months",
                    "remaining_cycles",
                )
            },
        ),
        (
            _("Status"),
            {
                "fields": (
                    "is_active",
                    "applied_at",
                    "expires_at",
                )
            },
        ),
    )

    def discount_display(self, obj):
        """Display human-readable discount"""
        return obj.get_discount_display()

    discount_display.short_description = _("Discount")
