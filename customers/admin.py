import csv

from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from accounts.models import CustomerProfile
from core.admin_mixins import MoneyFieldCurrencyMixin
from core.utils import get_default_currency
from custom_fields.mixins import CustomFieldsAdminMixin

from .models import AbandonedCart, CustomerMetrics, CustomerNote, CustomerSegment, LTVSettings

User = get_user_model()


class AffiliateStatusFilter(admin.SimpleListFilter):
    """Filter customers by affiliate status"""

    title = _("affiliate status")
    parameter_name = "affiliate_status"

    def lookups(self, request, model_admin):
        return [
            ("is_affiliate", _("Is Affiliate")),
            ("not_affiliate", _("Not Affiliate")),
            ("pending", _("Affiliate Pending")),
            ("active", _("Affiliate Active")),
            ("suspended", _("Affiliate Suspended")),
            ("rejected", _("Affiliate Rejected")),
        ]

    def queryset(self, request, queryset):
        from affiliate.models import Affiliate

        if self.value() == "is_affiliate":
            affiliate_users = Affiliate.objects.values_list("user_id", flat=True)
            return queryset.filter(user_id__in=affiliate_users)

        if self.value() == "not_affiliate":
            affiliate_users = Affiliate.objects.values_list("user_id", flat=True)
            return queryset.exclude(user_id__in=affiliate_users)

        if self.value() in ["pending", "active", "suspended", "rejected"]:
            affiliate_users = Affiliate.objects.filter(status=self.value()).values_list(
                "user_id", flat=True
            )
            return queryset.filter(user_id__in=affiliate_users)

        return queryset


class LTVCalculationMethodFilter(admin.SimpleListFilter):
    """Filter customers by LTV calculation method"""

    title = _("LTV calculation method")
    parameter_name = "ltv_method"

    def lookups(self, request, model_admin):
        return [
            ("simple", _("Simple (RFM)")),
            ("cohort", _("Cohort-based")),
            ("probabilistic", _("Probabilistic")),
            ("not_calculated", _("Not calculated")),
        ]

    def queryset(self, request, queryset):
        if self.value() == "not_calculated":
            return queryset.filter(ltv_calculation_method__isnull=True)
        elif self.value():
            return queryset.filter(ltv_calculation_method=self.value())
        return queryset


class LTVConfidenceFilter(admin.SimpleListFilter):
    """Filter customers by LTV confidence score"""

    title = _("LTV confidence")
    parameter_name = "ltv_confidence"

    def lookups(self, request, model_admin):
        return [
            ("high", _("High (80-100)")),
            ("medium", _("Medium (50-79)")),
            ("low", _("Low (0-49)")),
        ]

    def queryset(self, request, queryset):
        if self.value() == "high":
            return queryset.filter(ltv_confidence_score__gte=80)
        elif self.value() == "medium":
            return queryset.filter(ltv_confidence_score__gte=50, ltv_confidence_score__lt=80)
        elif self.value() == "low":
            return queryset.filter(ltv_confidence_score__lt=50)
        return queryset


class AccountTypeFilter(admin.SimpleListFilter):
    """Filter customers by account type (guest vs registered)"""

    title = _("account type")
    parameter_name = "account_type"

    def lookups(self, request, model_admin):
        return [
            ("guest", _("Guest")),
            ("registered", _("Registered")),
        ]

    def queryset(self, request, queryset):
        if self.value() == "guest":
            return queryset.filter(user__username__startswith="guest_")
        elif self.value() == "registered":
            return queryset.exclude(user__username__startswith="guest_")
        return queryset


@admin.register(CustomerProfile)
class EnhancedCustomerProfileAdmin(CustomFieldsAdminMixin, admin.ModelAdmin):
    change_list_template = "admin/accounts/customerprofile/change_list.html"
    change_form_template = "admin/accounts/customerprofile/change_form.html"

    list_display = [
        "user",
        "account_type_display",
        "affiliate_status_display",
        "customer_value",
        "customer_segment_display",
        "total_orders_display",
        "days_since_last_order",
        "is_vip_customer",
    ]
    list_filter = [AccountTypeFilter, AffiliateStatusFilter, "dashboard_layout", "created_at"]
    search_fields = [
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
        "phone",
    ]
    readonly_fields = [
        "created_at",
        "updated_at",
        "customer_analytics_summary",
        "purchase_behavior_summary",
        "engagement_summary",
    ]

    fieldsets = (
        (_("Customer Information"), {"fields": ("user", "phone", "date_of_birth")}),
        (
            _("Dashboard Preferences"),
            {
                "fields": (
                    "dashboard_layout",
                    "show_order_history",
                    "show_wishlist",
                    "show_recent_products",
                    "show_recommendations",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Customer Analytics"),
            {
                "fields": (
                    "customer_analytics_summary",
                    "purchase_behavior_summary",
                    "engagement_summary",
                ),
                "classes": ("wide",),
            },
        ),
        (_("Timestamps"), {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("user", "preferred_theme", "user__communication_preferences")
            .prefetch_related("user__orders", "user__customer_notes")
        )

    class Media:
        css = {"all": ("customers/css/customer_admin_list.css",)}

    def account_type_display(self, obj):
        """Display guest or registered account type badge"""
        if obj.user.username.startswith("guest_"):
            return format_html(
                '<span class="customer-list-badge customer-badge-guest">'
                '<i class="fas fa-user-clock"></i> {}</span>',
                _("Guest"),
            )
        return format_html(
            '<span class="customer-list-badge customer-badge-registered">'
            '<i class="fas fa-user-check"></i> {}</span>',
            _("Registered"),
        )

    account_type_display.short_description = _("Account Type")

    def send_activation_invitations(self, request, queryset):
        """Send activation invitation emails to selected guest customers"""
        from django.conf import settings as django_settings
        from django.contrib.auth.tokens import default_token_generator
        from django.contrib.sites.models import Site
        from django.utils.encoding import force_bytes
        from django.utils.http import urlsafe_base64_encode

        try:
            site = Site.objects.get_current()
            site_url = (
                f"http://{site.domain}" if django_settings.DEBUG else f"https://{site.domain}"
            )
        except Exception:
            site_url = getattr(django_settings, "SITE_URL", "http://localhost:8000")

        sent_count = 0
        skipped_count = 0

        for profile in queryset:
            user = profile.user
            if not user.username.startswith("guest_"):
                skipped_count += 1
                continue

            if not user.email:
                skipped_count += 1
                continue

            try:
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                lang = request.LANGUAGE_CODE or "en"
                activation_url = f"{site_url}/{lang}/accounts/activate-guest/{uid}/{token}/"

                from email_system.services.email_sender import EmailSendingService

                EmailSendingService.send_template_email(
                    to_email=user.email,
                    template_type="account_welcome",
                    context={
                        "customer_name": user.first_name or _("Customer"),
                        "activation_url": activation_url,
                        "is_guest_invitation": True,
                    },
                    language=lang,
                )
                sent_count += 1
            except Exception as e:
                import logging

                logging.getLogger(__name__).warning(
                    f"Failed to send activation invite to {user.email}: {e}"
                )
                skipped_count += 1

        messages.success(
            request,
            _(
                "Sent %(sent)d activation invitation(s). Skipped %(skipped)d (not guest or no email)."
            )
            % {"sent": sent_count, "skipped": skipped_count},
        )

    send_activation_invitations.short_description = _("Send activation invitation email")

    def affiliate_status_display(self, obj):
        """Display if customer is also an affiliate"""
        if hasattr(obj.user, "affiliate_profile"):
            affiliate = obj.user.affiliate_profile
            status_classes = {
                "pending": "customer-badge-affiliate-pending",
                "active": "customer-badge-affiliate-active",
                "suspended": "customer-badge-affiliate-suspended",
                "rejected": "customer-badge-affiliate-rejected",
            }
            status_icons = {
                "pending": "fa-clock",
                "active": "fa-check-circle",
                "suspended": "fa-ban",
                "rejected": "fa-times-circle",
            }
            affiliate_url = reverse("admin:affiliate_affiliate_change", args=[affiliate.pk])
            css_class = status_classes.get(affiliate.status, "customer-badge-affiliate-default")
            return format_html(
                '<a href="{}" class="affiliate-link">'
                '<span class="customer-list-badge {}">'
                '<i class="fas {}"></i> {} ({})'
                "</span></a>",
                affiliate_url,
                css_class,
                status_icons.get(affiliate.status, "fa-circle"),
                _("Affiliate"),
                affiliate.get_status_display(),
            )
        return format_html('<span class="muted-dash">—</span>')

    affiliate_status_display.short_description = _("Affiliate Status")

    def customer_value(self, obj):
        value = obj.total_spent
        # Extract numeric amount for comparison (Money field)
        amount = value.amount if hasattr(value, "amount") else float(value or 0)

        if amount > 1000:
            css_class = "customer-value-high"
        elif amount > 500:
            css_class = "customer-value-medium"
        else:
            css_class = "customer-value-low"
        return format_html('<span class="{}">{}</span>', css_class, value)

    customer_value.short_description = _("Customer Value")
    customer_value.admin_order_field = "user__customer_metrics__total_spent"

    def customer_segment_display(self, obj):
        segment = obj.customer_segment
        if segment:
            return format_html(
                '<span class="customer-segment-list-badge" style="--segment-bg: {}">{}</span>',
                segment.color,
                segment.display_name,
            )
        return "-"

    customer_segment_display.short_description = _("Segment")

    def total_orders_display(self, obj):
        total = obj.total_orders
        completed = obj.completed_orders_count
        return f"{completed}/{total}"

    total_orders_display.short_description = _("Orders (Completed/Total)")

    def customer_analytics_summary(self, obj):
        # Get customer metrics for LTV information
        try:
            metrics = CustomerMetrics.objects.get(user=obj.user)
            ltv_method = metrics.ltv_calculation_method or _("not calculated")
            ltv_confidence = metrics.ltv_confidence_score

            if ltv_confidence is not None:
                confidence_display = f"{ltv_confidence:.0f}%"
                if ltv_confidence >= 80:
                    confidence_class = "ltv-confidence-high"
                elif ltv_confidence >= 50:
                    confidence_class = "ltv-confidence-medium"
                else:
                    confidence_class = "ltv-confidence-low"
            else:
                # Base on order history
                if metrics.total_orders >= 10:
                    confidence_display = _("85% (estimated)")
                    confidence_class = "ltv-confidence-high"
                elif metrics.total_orders >= 5:
                    confidence_display = _("65% (estimated)")
                    confidence_class = "ltv-confidence-medium"
                else:
                    confidence_display = _("35% (estimated)")
                    confidence_class = "ltv-confidence-low"

            cohort_display = (
                metrics.cohort_month.strftime("%b %Y") if metrics.cohort_month else _("None")
            )
        except CustomerMetrics.DoesNotExist:
            ltv_method = _("not calculated")
            confidence_display = _("N/A")
            confidence_class = "muted-dash"
            cohort_display = _("None")

        return format_html(
            '<div class="analytics-summary">'
            "<h4>{}</h4>"
            '<div class="summary-grid">'
            "<div><strong>{}:</strong> {}</div>"
            "<div><strong>{}:</strong> {}</div>"
            "<div><strong>{}:</strong> {}</div>"
            "<div><strong>{}:</strong> {}</div>"
            "<div><strong>{}:</strong> {}</div>"
            "<div><strong>{}:</strong> {}/{}</div>"
            "<div><strong>{}:</strong> {}</div>"
            "<div><strong>{}:</strong> {}</div>"
            "</div>"
            '<div class="summary-ltv-section">'
            "<h5>{}</h5>"
            '<div class="summary-grid">'
            '<div><strong>{}:</strong> <span class="summary-ltv-method">{}</span></div>'
            '<div><strong>{}:</strong> <span class="{}">{}</span></div>'
            "<div><strong>{}:</strong> {}</div>"
            '<div><a href="{}" class="summary-ltv-link">{} →</a></div>'
            "</div>"
            "</div>"
            "</div>",
            _("Customer Analytics"),
            _("Total Spent"),
            obj.total_spent,
            _("Lifetime Value"),
            obj.lifetime_value,
            _("Total Orders"),
            obj.total_orders,
            _("Completed Orders"),
            obj.completed_orders_count,
            _("Average Order Value"),
            obj.average_order_value,
            _("Purchase Frequency"),
            f"{obj.purchase_frequency:.1f}",
            _("month"),
            _("VIP Status"),
            _("Yes") if obj.is_vip_customer else _("No"),
            _("At Risk"),
            _("Yes") if obj.is_at_risk else _("No"),
            _("Lifetime Value Analysis"),
            _("LTV Method"),
            ltv_method,
            _("Confidence"),
            confidence_class,
            confidence_display,
            _("Cohort"),
            cohort_display,
            reverse("customers:ltv_settings"),
            _("View LTV Settings"),
        )

    customer_analytics_summary.short_description = _("Analytics Summary")

    def purchase_behavior_summary(self, obj):
        categories = obj.favorite_categories[:3]
        categories_str = ", ".join(categories) if categories else _("None")

        return format_html(
            '<div class="behavior-summary">'
            "<h4>{}</h4>"
            "<div><strong>{}:</strong> {}</div>"
            "<div><strong>{}:</strong> {}</div>"
            "<div><strong>{}:</strong> {}</div>"
            "<div><strong>{}:</strong> {}</div>"
            "</div>",
            _("Purchase Behavior"),
            _("Days Since Last Order"),
            obj.days_since_last_order or _("No orders yet"),
            _("Favorite Categories"),
            categories_str,
            _("Abandoned Carts"),
            obj.abandoned_carts_count,
            _("Customer Segment"),
            obj.customer_segment.display_name if obj.customer_segment else _("Not classified"),
        )

    purchase_behavior_summary.short_description = _("Purchase Behavior")

    def engagement_summary(self, obj):
        try:
            prefs = obj.user.communication_preferences
            marketing = prefs.email_marketing
            transactional = prefs.email_transactional
        except Exception:
            marketing = False
            transactional = True

        return format_html(
            '<div class="engagement-summary">'
            "<h4>{}</h4>"
            "<div><strong>{}:</strong> {}</div>"
            "<div><strong>{}:</strong> {}</div>"
            "<div><strong>{}:</strong> {}</div>"
            "</div>",
            _("Customer Engagement"),
            _("Wishlist Items"),
            obj.wishlist_items_count,
            _("Marketing Emails"),
            _("Yes") if marketing else _("No"),
            _("Order Notifications"),
            _("Yes") if transactional else _("No"),
        )

    engagement_summary.short_description = _("Engagement Summary")

    def change_view(self, request, object_id, form_url="", extra_context=None):
        """Add additional context data for the change form"""
        from core.models import SiteSettings

        extra_context = extra_context or {}

        # Get site settings for currency
        try:
            site_settings = SiteSettings.objects.first()
            extra_context["site_settings"] = site_settings
        except Exception:
            pass

        if object_id:
            from orders.models import Order
            from orders.services.address_service import AddressService

            customer_profile = self.get_object(request, object_id)

            if customer_profile:
                # Get customer addresses with usage counts (active only)
                extra_context["addresses"] = AddressService.get_address_with_usage(
                    customer_profile.user
                )

                # Get recent orders (last 10)
                extra_context["recent_orders"] = Order.objects.filter(
                    user=customer_profile.user
                ).order_by("-created_at")[:10]

                # Get customer notes
                extra_context["customer_notes"] = (
                    CustomerNote.objects.filter(customer=customer_profile.user)
                    .select_related("created_by")
                    .order_by("-created_at")[:20]
                )

                # Get customer segment
                extra_context["customer_segment"] = customer_profile.customer_segment

                # Get or create communication preferences
                from accounts.models import CommunicationPreference

                comm_prefs, _ = CommunicationPreference.get_or_create_for_user(
                    customer_profile.user
                )
                extra_context["comm_prefs"] = comm_prefs

        return super().change_view(request, object_id, form_url, extra_context)

    actions = [
        "refresh_customer_metrics",
        "export_customer_data",
        "convert_to_affiliate",
        "send_activation_invitations",
    ]

    def refresh_customer_metrics(self, request, queryset):
        updated = 0
        for profile in queryset:
            profile.refresh_metrics()
            updated += 1
        self.message_user(request, f"Refreshed metrics for {updated} customers.")

    refresh_customer_metrics.short_description = _("Refresh customer metrics")

    def export_customer_data(self, request, queryset):
        """Export selected customers as CSV"""
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="customers_export.csv"'

        writer = csv.writer(response)
        writer.writerow(
            [
                str(_("Username")),
                str(_("Email")),
                str(_("Full Name")),
                str(_("Phone")),
                str(_("Total Spent")),
                str(_("Lifetime Value")),
                str(_("Total Orders")),
                str(_("Completed Orders")),
                str(_("Last Purchase Date")),
                str(_("Customer Segment")),
                str(_("VIP Status")),
                str(_("At Risk")),
                str(_("Created Date")),
            ]
        )

        for profile in queryset.select_related("user"):
            segment = profile.customer_segment
            writer.writerow(
                [
                    profile.user.username,
                    profile.user.email,
                    profile.user.get_full_name(),
                    profile.phone,
                    profile.total_spent,
                    profile.lifetime_value,
                    profile.total_orders,
                    profile.completed_orders_count,
                    profile.days_since_last_order,
                    segment.display_name if segment else "",
                    str(_("Yes")) if profile.is_vip_customer else str(_("No")),
                    str(_("Yes")) if profile.is_at_risk else str(_("No")),
                    profile.created_at.strftime("%Y-%m-%d"),
                ]
            )

        self.message_user(
            request,
            _("Exported data for %(count)s customers.") % {"count": queryset.count()},
            messages.SUCCESS,
        )
        return response

    export_customer_data.short_description = _("Export customer data")

    def convert_to_affiliate(self, request, queryset):
        """Convert selected customers to affiliates"""
        from affiliate.models import Affiliate

        created = 0
        skipped = 0
        errors = 0

        for profile in queryset:
            user = profile.user

            # Check if already an affiliate
            if hasattr(user, "affiliate_profile"):
                skipped += 1
                continue

            try:
                # Create affiliate profile with customer's existing data
                Affiliate.objects.create(
                    user=user,
                    payment_email=user.email,
                    payment_method="paypal",
                    status="pending",  # Default to pending for review
                    company_name="",
                    website="",
                )
                created += 1

            except Exception as e:
                errors += 1
                self.message_user(
                    request,
                    _("Error converting {}: {}").format(user.username, str(e)),
                    level=messages.ERROR,
                )

        # Success message
        if created > 0:
            self.message_user(
                request,
                _("Successfully converted {} customer(s) to affiliate status.").format(created),
                level=messages.SUCCESS,
            )

        # Info messages
        if skipped > 0:
            self.message_user(
                request,
                _("Skipped {} customer(s) who are already affiliates.").format(skipped),
                level=messages.WARNING,
            )

        if errors > 0:
            self.message_user(
                request,
                _("Failed to convert {} customer(s). Check error messages above.").format(errors),
                level=messages.ERROR,
            )

    convert_to_affiliate.short_description = _("Convert to Affiliate")


@admin.register(CustomerMetrics)
class CustomerMetricsAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "total_spent",
        "lifetime_value_display",
        "total_orders",
        "completed_orders",
        "ltv_method_display",
        "ltv_confidence_display",
        "cohort_month_display",
        "last_calculated",
    ]
    list_filter = [
        LTVCalculationMethodFilter,
        LTVConfidenceFilter,
        "last_calculated",
        "first_purchase_date",
        "last_purchase_date",
        "cohort_month",
    ]
    search_fields = ["user__username", "user__email", "user__first_name", "user__last_name"]
    readonly_fields = ["created_at", "last_calculated", "ltv_last_calculated"]

    fieldsets = (
        (_("Customer"), {"fields": ("user",)}),
        (
            _("Financial Metrics"),
            {"fields": ("total_spent", "lifetime_value", "average_order_value")},
        ),
        (
            _("LTV Calculation"),
            {
                "fields": (
                    "ltv_calculation_method",
                    "ltv_confidence_score",
                    "ltv_last_calculated",
                    "cohort_month",
                ),
                "description": _("Lifetime Value calculation details and cohort assignment"),
            },
        ),
        (
            _("Probabilistic LTV Fields"),
            {
                "fields": (
                    "probability_alive",
                    "predicted_purchases_12m",
                    "predicted_purchases_24m",
                ),
                "classes": ("collapse",),
                "description": _("Statistical predictions from probabilistic LTV models"),
            },
        ),
        (
            _("Order Statistics"),
            {"fields": ("total_orders", "completed_orders", "cancelled_orders")},
        ),
        (
            _("Purchase Behavior"),
            {
                "fields": (
                    "first_purchase_date",
                    "last_purchase_date",
                    "days_since_last_purchase",
                    "purchase_frequency",
                )
            },
        ),
        (
            _("Cart & Product Insights"),
            {
                "fields": (
                    "abandoned_carts_count",
                    "cart_abandonment_rate",
                    "favorite_category",
                    "most_purchased_product",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Engagement & Risk"),
            {
                "fields": (
                    "total_sessions",
                    "wishlist_items_count",
                    "reviews_count",
                    "refund_rate",
                    "support_tickets_count",
                ),
                "classes": ("collapse",),
            },
        ),
        (_("Timestamps"), {"fields": ("created_at", "last_calculated"), "classes": ("collapse",)}),
    )

    class Media:
        css = {"all": ("customers/css/customer_admin_list.css",)}

    actions = ["recalculate_metrics", "recalculate_ltv_all_methods"]

    def lifetime_value_display(self, obj):
        """Display lifetime value with visual styling"""
        amount = float(obj.lifetime_value.amount) if obj.lifetime_value else 0

        if amount > 5000:
            css_class = "ltv-value-very-high"
            icon = "fa-crown"
        elif amount > 2000:
            css_class = "ltv-value-high"
            icon = "fa-star"
        elif amount > 500:
            css_class = "ltv-value-medium"
            icon = "fa-circle"
        else:
            css_class = "ltv-value-low"
            icon = "fa-circle"

        currency = obj.lifetime_value.currency if obj.lifetime_value else get_default_currency()
        formatted_amount = f"{amount:,.2f}"
        return format_html(
            '<span class="{}"><i class="fas {}"></i> {} {}</span>',
            css_class,
            icon,
            currency,
            formatted_amount,
        )

    lifetime_value_display.short_description = _("Lifetime Value")
    lifetime_value_display.admin_order_field = "lifetime_value"

    def ltv_method_display(self, obj):
        """Display LTV calculation method with badge"""
        if not obj.ltv_calculation_method:
            return format_html(
                '<span class="customer-list-badge-sm ltv-badge-not-calculated">{}</span>',
                _("Not Calculated"),
            )

        method_classes = {
            "simple": "ltv-badge-rfm",
            "cohort": "ltv-badge-cohort",
            "probabilistic": "ltv-badge-probabilistic",
        }

        method_labels = {
            "simple": _("RFM"),
            "cohort": _("Cohort"),
            "probabilistic": _("Probabilistic"),
        }

        css_class = method_classes.get(obj.ltv_calculation_method, "ltv-badge-default")
        label = method_labels.get(obj.ltv_calculation_method, obj.ltv_calculation_method)

        return format_html('<span class="customer-list-badge-sm {}">{}</span>', css_class, label)

    ltv_method_display.short_description = _("Method")
    ltv_method_display.admin_order_field = "ltv_calculation_method"

    def ltv_confidence_display(self, obj):
        """Display LTV confidence score with visual indicator"""
        if obj.ltv_confidence_score is None:
            # Base confidence on order history for simple/cohort methods
            if obj.total_orders >= 10:
                score = 85
                level = "high"
            elif obj.total_orders >= 5:
                score = 65
                level = "medium"
            else:
                score = 35
                level = "low"
        else:
            score = float(obj.ltv_confidence_score) * 100
            if score >= 80:
                level = "high"
            elif score >= 50:
                level = "medium"
            else:
                level = "low"

        css_classes = {
            "high": "ltv-confidence-high",
            "medium": "ltv-confidence-medium",
            "low": "ltv-confidence-low",
        }

        icons = {
            "high": "fa-check-circle",
            "medium": "fa-exclamation-circle",
            "low": "fa-times-circle",
        }

        formatted_score = f"{score:.0f}"
        return format_html(
            '<span class="{}" title="{}"><i class="fas {}"></i> {}%</span>',
            css_classes[level],
            _("%s confidence") % level.capitalize(),
            icons[level],
            formatted_score,
        )

    ltv_confidence_display.short_description = _("Confidence")
    ltv_confidence_display.admin_order_field = "ltv_confidence_score"

    def cohort_month_display(self, obj):
        """Display cohort month with link to cohort dashboard"""
        if not obj.cohort_month:
            return format_html('<span class="muted-dash">—</span>')

        return format_html(
            '<a href="{}?cohort_month={}" class="cohort-month-link">'
            '<span class="customer-list-badge-sm cohort-month-badge">{}</span></a>',
            reverse("customers:cohort_dashboard"),
            obj.cohort_month.strftime("%Y-%m"),
            obj.cohort_month.strftime("%b %Y"),
        )

    cohort_month_display.short_description = _("Cohort")
    cohort_month_display.admin_order_field = "cohort_month"

    def recalculate_metrics(self, request, queryset):
        """Recalculate all metrics for selected customers"""
        updated = 0
        for metrics in queryset:
            CustomerMetrics.calculate_for_user(metrics.user)
            updated += 1
        self.message_user(
            request, _(f"Recalculated metrics for {updated} customer(s)."), level=messages.SUCCESS
        )

    recalculate_metrics.short_description = _("Recalculate customer metrics")

    def recalculate_ltv_all_methods(self, request, queryset):
        """Recalculate LTV using configured method"""
        from .tasks import calculate_customer_ltv_task

        settings = LTVSettings.get_settings()
        method = settings.calculation_method

        # Queue tasks for each customer
        task_ids = []
        for metrics in queryset:
            task = calculate_customer_ltv_task.delay(metrics.user.id)
            task_ids.append(task.id)

        self.message_user(
            request,
            _(
                f"Queued LTV recalculation for {len(task_ids)} customer(s) using {method} method. "
                f"This may take a few minutes."
            ),
            level=messages.SUCCESS,
        )

    recalculate_ltv_all_methods.short_description = _("Recalculate LTV (async)")


@admin.register(CustomerSegment)
class CustomerSegmentAdmin(MoneyFieldCurrencyMixin, admin.ModelAdmin):
    change_form_template = "admin/customers/customersegment/change_form.html"

    list_display = [
        "display_name",
        "name",
        "color_preview",
        "priority",
        "customer_count",
        "is_active",
    ]
    list_filter = ["is_active", "priority"]
    search_fields = ["name", "display_name", "description"]
    ordering = ["-priority", "name"]

    fieldsets = (
        (
            _("Segment Information"),
            {
                "fields": ("name", "display_name", "description"),
                "classes": ("tab-basic",),
            },
        ),
        (
            _("Criteria - Spending"),
            {
                "fields": ("min_total_spent", "max_total_spent"),
                "classes": ("tab-spending",),
            },
        ),
        (
            _("Criteria - Orders"),
            {
                "fields": ("min_orders", "max_orders"),
                "classes": ("tab-orders",),
            },
        ),
        (
            _("Criteria - Recency"),
            {
                "fields": ("min_days_since_last_purchase", "max_days_since_last_purchase"),
                "classes": ("tab-recency",),
            },
        ),
        (
            _("Display Settings"),
            {
                "fields": ("color", "priority", "is_active"),
                "classes": ("tab-display",),
            },
        ),
    )

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        return super().change_view(request, object_id, form_url, extra_context)

    class Media:
        css = {"all": ("customers/css/customer_admin_list.css",)}

    def color_preview(self, obj):
        return format_html('<div class="color-swatch" style="--swatch-color: {}"></div>', obj.color)

    color_preview.short_description = _("Color")

    def customer_count(self, obj):
        """Count customers matching this segment using a DB query."""
        if obj.name == "guest":
            return User.objects.filter(is_active=True, username__startswith="guest_").count()

        # Build queryset filter from segment criteria
        filters = Q(user__is_active=True) & ~Q(user__username__startswith="guest_")
        if obj.min_total_spent:
            filters &= Q(total_spent__gte=obj.min_total_spent)
        if obj.max_total_spent:
            filters &= Q(total_spent__lte=obj.max_total_spent)
        if obj.min_orders:
            filters &= Q(completed_orders__gte=obj.min_orders)
        if obj.max_orders:
            filters &= Q(completed_orders__lte=obj.max_orders)
        if obj.min_days_since_last_purchase:
            filters &= Q(days_since_last_purchase__gte=obj.min_days_since_last_purchase)
        if obj.max_days_since_last_purchase:
            filters &= Q(days_since_last_purchase__lte=obj.max_days_since_last_purchase)

        return CustomerMetrics.objects.filter(filters).count()

    customer_count.short_description = _("Customers")


@admin.register(AbandonedCart)
class AbandonedCartAdmin(admin.ModelAdmin):
    change_form_template = "admin/customers/abandonedcart/change_form.html"
    list_display = [
        "user",
        "abandoned_at",
        "total_value",
        "total_items",
        "estimated_reason",
        "recovery_status",
        "days_since_abandonment",
    ]
    list_filter = ["estimated_reason", "recovered", "abandoned_at"]
    search_fields = ["user__username", "user__email", "user__first_name", "user__last_name"]
    readonly_fields = ["abandoned_at", "days_since_abandonment", "cart"]

    fieldsets = (
        (
            _("Abandonment Details"),
            {
                "fields": ("user", "cart", "abandoned_at", "estimated_reason"),
                "classes": ("card-details",),
            },
        ),
        (
            _("Cart Summary"),
            {
                "fields": ("total_items", "total_value"),
                "classes": ("card-summary",),
            },
        ),
        (
            _("Recovery Tracking"),
            {
                "fields": ("recovery_emails_sent", "recovered", "recovered_at", "recovery_order"),
                "classes": ("card-recovery",),
            },
        ),
    )

    class Media:
        css = {
            "all": (
                "customers/css/abandonedcart_change_form.css",
                "customers/css/customer_admin_list.css",
            )
        }
        js = ("customers/js/abandonedcart_change_form.js",)

    def recovery_status(self, obj):
        if obj.recovered:
            return format_html(
                '<span class="recovery-recovered"><i class="fas fa-check-circle"></i> {}</span>',
                _("Recovered"),
            )
        elif obj.recovery_emails_sent > 0:
            return format_html(
                '<span class="recovery-contacted"><i class="fas fa-envelope"></i> {} {}</span>',
                obj.recovery_emails_sent,
                _("emails sent"),
            )
        else:
            return format_html(
                '<span class="recovery-not-contacted"><i class="fas fa-times-circle"></i> {}</span>',
                _("Not contacted"),
            )

    recovery_status.short_description = _("Recovery Status")

    actions = ["mark_as_recovered", "send_recovery_email"]

    def mark_as_recovered(self, request, queryset):
        from django.utils import timezone

        updated = queryset.update(recovered=True, recovered_at=timezone.now())
        self.message_user(request, f"Marked {updated} carts as recovered.")

    mark_as_recovered.short_description = _("Mark as recovered")

    def send_recovery_email(self, request, queryset):
        """Send cart recovery emails for selected abandoned carts."""
        from core.models import SiteSettings
        from email_system.services.email_sender import EmailSendingService

        site_settings = SiteSettings.objects.first()
        site_name = site_settings.site_name if site_settings else "Our Store"

        # Only send for non-recovered carts with a valid user email
        eligible = queryset.filter(recovered=False, user__email__isnull=False).exclude(
            user__email=""
        )
        sent = 0
        errors = 0

        for cart in eligible.select_related("user"):
            try:
                name = cart.user.get_full_name() or cart.user.username
                subject = str(_("%(name)s, you left items in your cart!") % {"name": name})
                html_body = (
                    f"<p>{str(_('Hi %(name)s,') % {'name': name})}</p>"
                    f"<p>{str(_('You left %(count)s item(s) worth %(value)s in your cart.') % {'count': cart.total_items, 'value': cart.total_value})}</p>"
                    f"<p>{str(_('Complete your purchase today!'))}</p>"
                    f"<p>{str(_('Best regards,'))}<br>{site_name}</p>"
                )
                EmailSendingService.queue_email(
                    to_email=cart.user.email,
                    subject=subject,
                    html_body=html_body,
                    template_type="abandoned_cart_recovery",
                    tags=["abandoned_cart", "recovery"],
                )
                cart.recovery_emails_sent += 1
                cart.save(update_fields=["recovery_emails_sent"])
                sent += 1
            except Exception:
                errors += 1

        if sent:
            self.message_user(
                request,
                _("Queued recovery emails for %(count)s abandoned carts.") % {"count": sent},
                messages.SUCCESS,
            )
        if errors:
            self.message_user(
                request,
                _("Failed to queue emails for %(count)s carts.") % {"count": errors},
                messages.WARNING,
            )
        skipped = queryset.count() - sent - errors
        if skipped:
            self.message_user(
                request,
                _("Skipped %(count)s carts (already recovered or no email).") % {"count": skipped},
                messages.INFO,
            )

    send_recovery_email.short_description = _("Send recovery emails")


@admin.register(CustomerNote)
class CustomerNoteAdmin(admin.ModelAdmin):
    list_display = [
        "customer",
        "note_type",
        "title",
        "requires_follow_up",
        "follow_up_date",
        "completed",
        "created_by",
        "created_at",
    ]
    list_filter = ["note_type", "requires_follow_up", "completed", "is_internal", "created_at"]
    search_fields = ["customer__username", "customer__email", "title", "content"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        (
            _("Note Information"),
            {"fields": ("customer", "created_by", "note_type", "title", "content")},
        ),
        (_("Follow-up"), {"fields": ("requires_follow_up", "follow_up_date", "completed")}),
        (_("Visibility"), {"fields": ("is_internal",)}),
        (_("Timestamps"), {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    actions = ["mark_completed", "set_follow_up_required"]

    def mark_completed(self, request, queryset):
        updated = queryset.update(completed=True)
        self.message_user(request, f"Marked {updated} notes as completed.")

    mark_completed.short_description = _("Mark as completed")

    def set_follow_up_required(self, request, queryset):
        updated = queryset.update(requires_follow_up=True)
        self.message_user(request, f"Set follow-up required for {updated} notes.")

    set_follow_up_required.short_description = _("Set follow-up required")
