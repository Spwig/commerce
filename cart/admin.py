import json
import logging

from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from core.widgets import IconPickerWidget
from media_library.widgets import MediaLibrarySelectWidget
from shipping.models import ShippingRateTable

from .models import (
    Cart,
    CartItem,
    CheckoutSession,
    RecentlyViewed,
    ShippingMethod,
    TaxRate,
    Wishlist,
    WishlistItem,
)

logger = logging.getLogger(__name__)


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ["total_price"]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    change_list_template = "admin/cart/cart/change_list.html"
    list_display = [
        "__str__",
        "user",
        "total_items",
        "total_amount",
        "shipping_cost",
        "grand_total",
        "updated_at",
    ]
    list_filter = ["cart_layout", "checkout_flow", "shipping_method", "created_at"]
    search_fields = ["user__username", "session_key"]
    readonly_fields = [
        "total_items",
        "total_amount",
        "total_savings",
        "grand_total",
        "requires_shipping",
        "total_weight",
    ]
    inlines = [CartItemInline]

    fieldsets = (
        ("Cart Information", {"fields": ("user", "session_key")}),
        (
            "Layout & Display",
            {
                "fields": (
                    "cart_layout",
                    "show_product_images",
                    "show_product_variants",
                    "show_remove_button",
                    "show_quantity_controls",
                )
            },
        ),
        ("Pricing Display", {"fields": ("show_item_totals", "show_cart_summary", "show_savings")}),
        ("Checkout", {"fields": ("checkout_flow",)}),
        (
            "Shipping Information",
            {
                "fields": (
                    "shipping_address",
                    "shipping_method",
                    "shipping_cost",
                    "estimated_delivery_date",
                    "shipping_notes",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Summary",
            {
                "fields": (
                    "total_items",
                    "total_amount",
                    "total_savings",
                    "requires_shipping",
                    "total_weight",
                    "grand_total",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    def has_add_permission(self, request):
        """
        Disable adding carts manually - carts are created automatically
        when users/guests add items to their cart
        """
        return False


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ["__str__", "cart", "quantity", "unit_price", "total_price"]
    list_filter = ["created_at"]
    search_fields = ["product__name", "cart__user__username"]
    readonly_fields = ["total_price", "savings"]


class WishlistItemInline(admin.TabularInline):
    model = WishlistItem
    extra = 0


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ["name", "user", "total_items", "is_public", "created_at"]
    list_filter = ["wishlist_layout", "is_public", "created_at"]
    search_fields = ["name", "user__username"]
    readonly_fields = ["total_items", "total_value"]
    inlines = [WishlistItemInline]

    fieldsets = (
        ("Wishlist Information", {"fields": ("user", "name")}),
        (
            "Display Settings",
            {"fields": ("wishlist_layout", "show_prices", "show_availability", "show_add_to_cart")},
        ),
        ("Privacy & Sharing", {"fields": ("is_public", "share_slug")}),
        ("Summary", {"fields": ("total_items", "total_value"), "classes": ("collapse",)}),
    )


@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ["__str__", "wishlist", "priority", "notify_when_available", "created_at"]
    list_filter = ["priority", "notify_when_available", "notify_when_on_sale", "created_at"]
    search_fields = ["product__name", "wishlist__name", "wishlist__user__username"]


@admin.register(RecentlyViewed)
class RecentlyViewedAdmin(admin.ModelAdmin):
    list_display = ["product", "user_display", "view_count", "viewed_at"]
    list_filter = ["viewed_at"]
    search_fields = ["product__name", "user__username", "session_key"]
    readonly_fields = ["viewed_at"]

    def user_display(self, obj):
        if obj.user:
            return obj.user.username
        return f"Session: {obj.session_key[:8]}..."

    user_display.short_description = "User/Session"


class ShippingRateTableInline(admin.TabularInline):
    """Inline for viewing/managing rate tables linked to a shipping method"""

    model = ShippingRateTable
    extra = 0
    fields = ["name", "basis_type", "is_active"]
    readonly_fields = ["name"]
    show_change_link = True


@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    """Admin for shipping methods with modern card-based interface"""

    # Use custom templates
    change_list_template = "admin/cart/shippingmethod/change_list.html"
    change_form_template = "admin/cart/shippingmethod/change_form.html"

    # Show all methods on one page for client-side filtering
    list_per_page = 1000

    list_display = ["name", "method_type", "flat_rate_cost", "is_active", "sort_order"]
    list_filter = ["method_type", "is_active", "carrier"]
    search_fields = ["name", "description"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["sort_order", "name"]
    inlines = [ShippingRateTableInline]

    class Media:
        css = {"all": ("cart/css/admin_shipping_method.css",)}
        js = ("cart/js/admin_shipping_method.js",)

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": ("name", "description", "method_type", "is_active", "sort_order"),
                "classes": ("tab-basic",),
            },
        ),
        ("Pricing", {"fields": ("flat_rate_cost",), "classes": ("tab-pricing",)}),
        ("Geographic Coverage", {"fields": ("zones",), "classes": ("tab-zones",)}),
        (
            "Delivery Time",
            {"fields": ("min_delivery_days", "max_delivery_days"), "classes": ("tab-delivery",)},
        ),
        (
            "Carrier Integration",
            {"fields": ("carrier", "carrier_service_code"), "classes": ("tab-carrier",)},
        ),
        ("Display", {"fields": ("image", "icon"), "classes": ("tab-display",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at"), "classes": ("tab-timestamps",)}),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Use MediaLibrarySelectWidget for image field"""
        if db_field.name == "image":
            return forms.ModelChoiceField(
                queryset=db_field.remote_field.model.objects.all(),
                widget=MediaLibrarySelectWidget(),
                required=False,
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        """Override form fields to use custom widgets"""
        if db_field.name == "icon":
            return forms.CharField(
                widget=IconPickerWidget(
                    priority_icons=[
                        "fa-truck",
                        "fa-truck-fast",
                        "fa-box",
                        "fa-warehouse",
                        "fa-dolly",
                        "fa-cube",
                        "fa-ship",
                        "fa-plane",
                        "fa-bicycle",
                    ],
                    style_prefix=False,
                ),
                required=False,
                initial="fa-truck",
            )
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        """Override to filter MoneyField currency choices"""
        form = super().get_form(request, obj, **kwargs)
        from core.admin_mixins import _apply_money_field_currency_defaults

        _apply_money_field_currency_defaults(form, obj)
        return form

    def changelist_view(self, request, extra_context=None):
        """Add custom context data for the method list view"""

        extra_context = extra_context or {}

        # Get all methods for counts
        all_methods = ShippingMethod.objects.all()

        # Status counts
        extra_context["active_count"] = all_methods.filter(is_active=True).count()
        extra_context["inactive_count"] = all_methods.filter(is_active=False).count()

        # Method type counts
        extra_context["flat_rate_count"] = all_methods.filter(method_type="flat_rate").count()
        extra_context["real_time_count"] = all_methods.filter(method_type="real_time").count()
        extra_context["local_pickup_count"] = all_methods.filter(method_type="local_pickup").count()
        extra_context["table_rate_count"] = all_methods.filter(method_type="table_rate").count()

        return super().changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        from django.db.models import Count

        from shipping.models import ShippingPromotion

        extra_context = extra_context or {}
        if object_id:
            obj = self.get_object(request, object_id)
            if obj:
                # Promotions explicitly targeting this method
                targeting_this = ShippingPromotion.objects.filter(
                    is_active=True, shipping_methods=obj
                )
                # Promotions with no method restrictions (apply to all)
                targeting_all = (
                    ShippingPromotion.objects.filter(is_active=True)
                    .annotate(method_count=Count("shipping_methods"))
                    .filter(method_count=0)
                )

                extra_context["active_promotions"] = (targeting_this | targeting_all).distinct()
        return super().change_view(request, object_id, form_url, extra_context)

    def get_urls(self):
        from django.urls import path

        urls = super().get_urls()
        custom_urls = [
            path(
                "bulk-action/",
                self.admin_site.admin_view(self.bulk_action_view),
                name="cart_shippingmethod_bulk_action",
            ),
        ]
        return custom_urls + urls

    def bulk_action_view(self, request):
        """Handle bulk actions on shipping methods via AJAX."""
        from django.http import JsonResponse

        if request.method != "POST":
            return JsonResponse({"success": False, "message": "POST required"}, status=405)

        try:
            data = json.loads(request.body)
            action = data.get("action")
            method_ids = data.get("method_ids", [])

            if not action or not method_ids:
                return JsonResponse(
                    {"success": False, "message": _("Action and method IDs required")}, status=400
                )

            methods = ShippingMethod.objects.filter(id__in=method_ids)
            count = methods.count()

            if action == "enable":
                methods.update(is_active=True)
                message = _("{} method(s) enabled").format(count)

            elif action == "disable":
                methods.update(is_active=False)
                message = _("{} method(s) disabled").format(count)

            elif action == "delete":
                methods.delete()
                message = _("{} method(s) deleted").format(count)

            else:
                return JsonResponse({"success": False, "message": _("Unknown action")}, status=400)

            return JsonResponse({"success": True, "message": str(message)})

        except json.JSONDecodeError:
            return JsonResponse(
                {"success": False, "message": _("Invalid request data")}, status=400
            )
        except Exception as e:
            logger.error("Shipping method bulk action error: %s", e, exc_info=True)
            return JsonResponse(
                {"success": False, "message": _("An unexpected error occurred. Please try again.")},
                status=500,
            )


@admin.register(TaxRate)
class TaxRateAdmin(admin.ModelAdmin):
    change_list_template = "admin/cart/taxrate/change_list.html"
    change_form_template = "admin/cart/taxrate/change_form.html"
    list_display = ["name", "country", "state", "city", "rate_percent", "tax_type", "is_active"]
    list_filter = ["tax_type", "is_active", "country", "applies_to_shipping"]
    search_fields = ["name", "country", "state", "city"]
    readonly_fields = ["created_at", "updated_at"]
    autocomplete_fields = ["exempt_categories"]
    list_per_page = 1000

    fieldsets = (
        (
            _("Basic Information"),
            {
                "fields": ("name", "is_active", "tax_type", "rate", "priority"),
                "classes": ("tab-basic",),
            },
        ),
        (
            _("Geographic Scope"),
            {"fields": ("country", "state", "city", "postal_codes"), "classes": ("tab-geography",)},
        ),
        (
            _("Application Rules"),
            {"fields": ("applies_to_shipping", "compound"), "classes": ("tab-rules",)},
        ),
        (
            _("Product Exemptions"),
            {
                "fields": ("exempt_product_types", "exempt_categories"),
                "classes": ("tab-exemptions",),
            },
        ),
        (_("Timestamps"), {"fields": ("created_at", "updated_at"), "classes": ("tab-timestamps",)}),
    )

    def get_form(self, request, obj=None, **kwargs):
        from cart.forms import TaxRateAdminForm

        kwargs["form"] = TaxRateAdminForm
        return super().get_form(request, obj, **kwargs)

    def rate_percent(self, obj):
        return f"{obj.rate * 100}%"

    rate_percent.short_description = _("Rate %")

    def changelist_view(self, request, extra_context=None):
        from django.db.models import Count
        from django.urls import reverse

        from cart.models import TaxPresetGroup

        extra_context = extra_context or {}

        qs = TaxRate.objects.all()
        extra_context["stats"] = {
            "total_rules": qs.count(),
            "active_rules": qs.filter(is_active=True).count(),
            "countries_covered": qs.values("country").distinct().count(),
            "tax_types_used": qs.values("tax_type").distinct().count(),
        }

        # Distinct countries for filter dropdown
        extra_context["countries"] = (
            TaxRate.objects.values("country").annotate(count=Count("id")).order_by("country")
        )

        # Tax rates with exempt count annotation
        tax_rates = qs.prefetch_related("exempt_categories").order_by(
            "-priority", "country", "state", "city"
        )
        # Add rate_percent and exempt_count as properties
        for rate in tax_rates:
            rate.rate_percent = f"{rate.rate * 100}%"
            rate.exempt_count = rate.exempt_categories.count()
        extra_context["tax_rates"] = tax_rates

        # Preset groups for the modal
        extra_context["preset_groups"] = (
            TaxPresetGroup.objects.filter(is_active=True)
            .prefetch_related("rates")
            .order_by("region", "name")
        )

        # URLs for JS
        extra_context["filter_url"] = reverse("cart_admin:filter_tax_rates")
        extra_context["preset_api_url"] = reverse("cart_admin:load_tax_preset")

        return super().changelist_view(request, extra_context=extra_context)


@admin.register(CheckoutSession)
class CheckoutSessionAdmin(admin.ModelAdmin):
    list_display = ["cart", "step_completed", "total_amount", "expires_at", "created_at"]
    list_filter = ["step_completed", "billing_same_as_shipping", "created_at"]
    search_fields = ["cart__user__username", "cart__session_key"]
    readonly_fields = [
        "cart",
        "subtotal",
        "tax_amount",
        "discount_amount",
        "total_amount",
        "tax_breakdown",
        "available_shipping_methods",
        "created_at",
        "updated_at",
    ]

    fieldsets = (
        ("Cart & Session", {"fields": ("cart", "step_completed", "expires_at")}),
        (
            "Addresses",
            {"fields": ("shipping_address", "billing_address", "billing_same_as_shipping")},
        ),
        (
            "Shipping",
            {
                "fields": (
                    "selected_shipping_method",
                    "shipping_cost",
                    "estimated_delivery_date",
                    "available_shipping_methods",
                )
            },
        ),
        ("Payment", {"fields": ("payment_provider",)}),
        ("Tax", {"fields": ("tax_amount", "tax_breakdown"), "classes": ("collapse",)}),
        ("Order Totals", {"fields": ("subtotal", "discount_amount", "total_amount")}),
        ("Timestamps", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )
