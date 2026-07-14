import logging

from django.contrib import admin, messages
from django.db.models import Count, Q, Sum
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import path, reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from core.utils import get_default_currency, get_shipping_origin_country
from custom_fields.mixins import CustomFieldsAdminMixin

from .models import Address, Order, OrderItem, OrderNote, Refund, ReturnRequest

logger = logging.getLogger(__name__)


class OrderItemInline(admin.TabularInline):
    """Inline admin for order items"""

    model = OrderItem
    extra = 0
    fields = [
        "product_name",
        "product_status",
        "variant_name",
        "sku",
        "quantity",
        "unit_price",
        "total_price",
        "customization_summary",
        "warehouse_info",
        "fulfillment_status",
    ]
    readonly_fields = [
        "product",
        "variant",
        "product_name",
        "product_status",
        "variant_name",
        "sku",
        "quantity",
        "unit_price",
        "total_price",
        "created_at",
        "customization_summary",
        "warehouse_info",
        "fulfillment_status",
    ]
    can_delete = False

    def customization_summary(self, obj):
        """Display customizations in a readable format"""
        from django.utils.html import escape, format_html
        from django.utils.safestring import mark_safe

        if not obj.customizations:
            return format_html('<span class="admin-text-muted">—</span>')

        # Build HTML for customizations display
        html_parts = []
        for option_id, customization_data in obj.customizations.items():
            if not isinstance(customization_data, dict):
                continue

            value = customization_data.get("value", "")
            price = customization_data.get("calculated_price", "0")

            # Try to get the option name
            try:
                from catalog.models import CustomizationOption

                option = CustomizationOption.objects.get(id=int(option_id))
                option_name = escape(option.name)
            except Exception:
                option_name = f"Option #{escape(str(option_id))}"

            # Format the value based on length
            if len(str(value)) > 50:
                display_value = escape(f"{str(value)[:50]}...")
            else:
                display_value = escape(str(value))

            # Add price if non-zero
            price_display = (
                f' <span class="admin-text-success">+${escape(str(price))}</span>'
                if float(price) > 0
                else ""
            )

            html_parts.append(
                f'<div class="admin-customization-line">'
                f"<strong>{option_name}:</strong> {display_value}{price_display}"
                f"</div>"
            )

        if html_parts:
            return mark_safe("".join(html_parts))
        return format_html('<span class="admin-text-muted">—</span>')

    customization_summary.short_description = _("Customizations")

    def product_status(self, obj):
        """Display product deletion status"""
        from django.utils.html import format_html

        from catalog.models import Product

        if not obj.product_id:
            return format_html('<span class="admin-text-muted">—</span>')

        try:
            # Check if product is soft-deleted
            product = Product.all_objects.get(id=obj.product_id)
            if product.is_deleted:
                return format_html(
                    '<span class="admin-text-danger admin-text-bold" title="Product has been deleted">⚠️ Deleted</span>'
                )
            else:
                return format_html(
                    '<span class="admin-text-success" title="Product is active">✓ Active</span>'
                )
        except Product.DoesNotExist:
            return format_html(
                '<span class="admin-text-danger" title="Product not found">⚠️ Not Found</span>'
            )

    product_status.short_description = _("Status")

    def warehouse_info(self, obj):
        """Display warehouse and region information"""
        from django.utils.html import format_html

        if obj.warehouse:
            return format_html(
                '<strong>{}</strong><br/><span class="admin-text-small-muted">{}</span>',
                obj.warehouse.name,
                obj.warehouse.region.name if obj.warehouse.region else _("No region"),
            )
        return format_html('<span class="admin-text-muted">—</span>')

    warehouse_info.short_description = _("Warehouse")

    def fulfillment_status(self, obj):
        """Display fulfillment status with icons"""
        from django.utils.html import format_html

        if obj.stock_fulfilled:
            return format_html(
                '<span class="admin-text-success admin-text-bold" title="Stock Fulfilled">✅ Fulfilled</span>'
            )
        elif obj.stock_allocated:
            return format_html(
                '<span class="admin-text-warning admin-text-bold" title="Stock Allocated">📦 Allocated</span>'
            )
        else:
            return format_html(
                '<span class="admin-text-muted" title="Not Allocated">⏳ Pending</span>'
            )

    fulfillment_status.short_description = _("Fulfillment")

    def has_add_permission(self, request, obj=None):
        """Prevent adding items through admin"""
        return False


@admin.register(Order)
class OrderAdmin(CustomFieldsAdminMixin, admin.ModelAdmin):
    change_list_template = "admin/orders/order/change_list.html"
    change_form_template = "admin/orders/order/change_form.html"

    list_display = [
        "order_number",
        "user",
        "test_order_badge",
        "status_badge",
        "payment_status_badge",
        "source_badge",
        "total_amount",
        "created_at",
    ]
    list_filter = [
        "status",
        "payment_status",
        "is_test_order",
        "source",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "order_number",
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
        "phone",
        "email",
        "items__product__name",
    ]
    readonly_fields = [
        "order_number",
        "created_at",
        "updated_at",
        "item_count",
        "packing_slip_preview",
        "commercial_invoice_preview",
        "customs_form_preview",
        "customer_currency",
        "base_currency",
        "exchange_rate_used",
        "exchange_rate_provider",
        "fx_policy",
    ]
    inlines = [OrderItemInline]
    actions = [
        "mark_as_processing",
        "mark_as_shipped",
        "mark_as_delivered",
        "mark_as_cancelled",
        "mark_as_paid",
        "mark_as_unpaid",
        "mark_payment_pending",
        "generate_licenses_now",
        "generate_packing_slips",
        "generate_commercial_invoices",
        "generate_customs_forms",
    ]

    fieldsets = (
        (
            _("Order Information"),
            {
                "fields": (
                    "order_number",
                    "user",
                    "status",
                    "source",
                    "tracking_number",
                    "item_count",
                )
            },
        ),
        (_("Customer Information"), {"fields": ("email", "phone")}),
        (
            _("Shipping Address"),
            {
                "fields": (
                    "shipping_name",
                    "shipping_address1",
                    "shipping_address2",
                    "shipping_city",
                    "shipping_state",
                    "shipping_postal_code",
                    "shipping_country",
                )
            },
        ),
        (
            _("Billing Address"),
            {
                "fields": (
                    "billing_same_as_shipping",
                    "billing_name",
                    "billing_address1",
                    "billing_address2",
                    "billing_city",
                    "billing_state",
                    "billing_postal_code",
                    "billing_country",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Order Totals"),
            {
                "fields": (
                    "subtotal",
                    "tax_amount",
                    "shipping_cost",
                    "discount_amount",
                    "total_amount",
                )
            },
        ),
        (
            _("Payment Information"),
            {
                "fields": (
                    "payment_status",
                    "payment_provider",
                    "payment_method_type",
                    "payment_method_last4",
                    "paid_at",
                    "amount_paid",
                    "amount_refunded",
                ),
                "description": _("Payment status and details for this order."),
            },
        ),
        (
            _("Currency & Exchange Rate"),
            {
                "fields": (
                    "customer_currency",
                    "base_currency",
                    "exchange_rate_used",
                    "exchange_rate_provider",
                    "fx_policy",
                ),
                "classes": ("collapse",),
                "description": _(
                    "Multi-currency details. Shows the customer's payment currency and the exchange rate used to compute base-currency equivalents for reporting."
                ),
            },
        ),
        (
            _("Documents (Phase 6)"),
            {
                "fields": (
                    "packing_slip_preview",
                    "commercial_invoice_preview",
                    "customs_form_preview",
                ),
                "classes": ("collapse",),
                "description": _(
                    "Shipping documents are generated from the order's shipment. If no shipment exists, documents cannot be generated."
                ),
            },
        ),
        (
            _("Display Preferences"),
            {
                "fields": (
                    "order_page_layout",
                    "show_order_progress",
                    "show_shipping_updates",
                    "show_item_images",
                ),
                "classes": ("collapse",),
            },
        ),
        (_("Notes"), {"fields": ("notes", "special_instructions"), "classes": ("collapse",)}),
        (_("Timestamps"), {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def status_badge(self, obj):
        """Display status with color badge"""
        return format_html(
            '<span class="admin-badge admin-badge-status-{}">{}</span>',
            obj.status,
            obj.get_status_display(),
        )

    status_badge.short_description = _("Status")

    def payment_status_badge(self, obj):
        """Display payment status with color badge"""
        return format_html(
            '<span class="admin-badge admin-badge-payment-{}">{}</span>',
            obj.payment_status,
            obj.get_payment_status_display(),
        )

    payment_status_badge.short_description = _("Payment")

    def source_badge(self, obj):
        """Display source with icon and badge"""
        icons = {
            "direct": "fa-globe",
            "referral": "fa-users",
            "email": "fa-envelope",
            "social": "fa-share-alt",
            "loyalty": "fa-award",
            "organic": "fa-search",
            "utm_tracked": "fa-link",
            "unknown": "fa-question",
        }
        icon = icons.get(obj.source, "fa-question")
        return format_html(
            '<span class="admin-badge admin-badge-source-{}"><i class="fas {}"></i> {}</span>',
            obj.source,
            icon,
            obj.get_source_display(),
        )

    source_badge.short_description = _("Source")

    def test_order_badge(self, obj):
        """Display TEST badge for sandbox/test orders"""
        if obj.is_test_order:
            return format_html('<span class="admin-badge-test">TEST</span>')
        return ""

    test_order_badge.short_description = _("Test")

    def item_count(self, obj):
        """Display number of items in order"""
        return obj.items.count()

    item_count.short_description = _("Items")

    # Phase 6: Document Generation Preview Methods
    def packing_slip_preview(self, obj):
        """Display packing slip preview from order's shipment"""
        shipment = obj.shipments.first()

        if not shipment:
            return format_html(
                '<em class="admin-text-muted">{}</em>',
                _("No shipment available. Create a shipment to generate documents."),
            )

        if not shipment.packing_slip_url:
            return format_html(
                '<em class="admin-text-muted">{}</em>', _("No packing slip available")
            )

        if shipment.packing_slip_url.startswith("data:"):
            return format_html(
                '<div class="admin-doc-preview">'
                '<iframe src="{}"></iframe>'
                '<div class="admin-doc-actions">'
                '<a href="{}" download="packing_slip_{}.pdf" class="button admin-doc-download-btn">'
                '<i class="fas fa-download"></i> {} Packing Slip'
                "</a>"
                "</div>"
                "</div>",
                shipment.packing_slip_url,
                shipment.packing_slip_url,
                obj.order_number,
                _("Download"),
            )
        else:
            return format_html(
                '<a href="{}" target="_blank" rel="noopener" class="button admin-doc-download-btn">'
                '<i class="fas fa-external-link-alt"></i> {} Packing Slip'
                "</a>",
                shipment.packing_slip_url,
                _("View"),
            )

    packing_slip_preview.short_description = _("Packing Slip")

    def commercial_invoice_preview(self, obj):
        """Display commercial invoice preview from order's shipment"""
        shipment = obj.shipments.first()

        if not shipment:
            return format_html(
                '<em class="admin-text-muted">{}</em>',
                _("No shipment available. Create a shipment to generate documents."),
            )

        if not shipment.commercial_invoice_url:
            return format_html(
                '<em class="admin-text-muted">{}</em>', _("No commercial invoice available")
            )

        if shipment.commercial_invoice_url.startswith("data:"):
            return format_html(
                '<div class="admin-doc-preview">'
                '<iframe src="{}"></iframe>'
                '<div class="admin-doc-actions">'
                '<a href="{}" download="commercial_invoice_{}.pdf" class="button admin-doc-download-btn-warning">'
                '<i class="fas fa-download"></i> {} Commercial Invoice'
                "</a>"
                "</div>"
                "</div>",
                shipment.commercial_invoice_url,
                shipment.commercial_invoice_url,
                obj.order_number,
                _("Download"),
            )
        else:
            return format_html(
                '<a href="{}" target="_blank" rel="noopener" class="button admin-doc-download-btn-warning">'
                '<i class="fas fa-external-link-alt"></i> {} Commercial Invoice'
                "</a>",
                shipment.commercial_invoice_url,
                _("View"),
            )

    commercial_invoice_preview.short_description = _("Commercial Invoice")

    def customs_form_preview(self, obj):
        """Display customs form preview from order's shipment"""
        shipment = obj.shipments.first()

        if not shipment:
            return format_html(
                '<em class="admin-text-muted">{}</em>',
                _("No shipment available. Create a shipment to generate documents."),
            )

        if not shipment.customs_form_url:
            return format_html(
                '<em class="admin-text-muted">{}</em>', _("No customs form available")
            )

        if shipment.customs_form_url.startswith("data:"):
            return format_html(
                '<div class="admin-doc-preview">'
                '<iframe src="{}"></iframe>'
                '<div class="admin-doc-actions">'
                '<a href="{}" download="customs_form_{}.pdf" class="button admin-doc-download-btn-muted">'
                '<i class="fas fa-download"></i> {} Customs Form'
                "</a>"
                "</div>"
                "</div>",
                shipment.customs_form_url,
                shipment.customs_form_url,
                obj.order_number,
                _("Download"),
            )
        else:
            return format_html(
                '<a href="{}" target="_blank" rel="noopener" class="button admin-doc-download-btn-muted">'
                '<i class="fas fa-external-link-alt"></i> {} Customs Form'
                "</a>",
                shipment.customs_form_url,
                _("View"),
            )

    customs_form_preview.short_description = _("Customs Form")

    # Bulk actions
    @admin.action(description=_("Mark selected orders as Processing"))
    def mark_as_processing(self, request, queryset):
        updated = queryset.update(status="processing")
        self.message_user(request, _(f"{updated} orders marked as processing"))

    @admin.action(description=_("Mark selected orders as Shipped"))
    def mark_as_shipped(self, request, queryset):
        updated = queryset.update(status="shipped")
        self.message_user(request, _(f"{updated} orders marked as shipped"))

    @admin.action(description=_("Mark selected orders as Delivered"))
    def mark_as_delivered(self, request, queryset):
        updated = queryset.update(status="delivered")
        self.message_user(request, _(f"{updated} orders marked as delivered"))

    @admin.action(description=_("Mark selected orders as Cancelled"))
    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status="cancelled")
        self.message_user(request, _(f"{updated} orders marked as cancelled"))

    # Payment Status Actions
    @admin.action(description=_("Mark selected orders as Paid"))
    def mark_as_paid(self, request, queryset):
        from django.utils import timezone

        updated = queryset.update(payment_status="paid", paid_at=timezone.now())
        # Also update amount_paid to match total for each order
        for order in queryset:
            if order.amount_paid != order.total_amount:
                order.amount_paid = order.total_amount
                order.save(update_fields=["amount_paid"])
        self.message_user(request, _(f"{updated} orders marked as paid"))

    @admin.action(description=_("Mark selected orders as Unpaid"))
    def mark_as_unpaid(self, request, queryset):
        updated = queryset.update(payment_status="unpaid", paid_at=None)
        self.message_user(request, _(f"{updated} orders marked as unpaid"))

    @admin.action(description=_("Mark selected orders as Payment Pending"))
    def mark_payment_pending(self, request, queryset):
        updated = queryset.update(payment_status="pending")
        self.message_user(request, _(f"{updated} orders marked as payment pending"))

    @admin.action(description=_("Generate licenses now (manual trigger)"))
    def generate_licenses_now(self, request, queryset):
        """
        Manually generate license keys for products with license_generation_trigger='manual'.
        Also works for any products with requires_license=True that don't have licenses yet.
        """
        from django.db import transaction

        from catalog.models import LicenseKey
        from catalog.signals import process_digital_product_order_item

        generated_count = 0
        skipped_count = 0
        error_count = 0

        for order in queryset:
            # Find items needing manual license generation
            items_needing_license = order.items.filter(product__requires_license=True).distinct()

            if not items_needing_license.exists():
                skipped_count += 1
                continue

            for order_item in items_needing_license:
                # Check if license already exists
                existing_license = LicenseKey.objects.filter(
                    order_item=order_item,
                    digital_asset__isnull=True,  # Product-level license
                ).exists()

                if existing_license:
                    continue

                try:
                    with transaction.atomic():
                        licenses = process_digital_product_order_item(order_item, order)
                        generated_count += len(licenses)

                    # Create order note
                    if licenses:
                        OrderNote.objects.create(
                            order=order,
                            author=request.user,
                            note=f"🔑 Manually generated {len(licenses)} license key(s) for {order_item.product_name}",
                            is_customer_note=False,
                        )
                except Exception as e:
                    error_count += 1
                    self.message_user(
                        request,
                        _(f"Failed to generate license for order {order.order_number}: {str(e)}"),
                        level="error",
                    )

        if generated_count > 0:
            self.message_user(
                request,
                _(f"Successfully generated {generated_count} license key(s)."),
                level="success",
            )

        if skipped_count > 0:
            self.message_user(
                request,
                _(f"Skipped {skipped_count} order(s) without products requiring licenses."),
                level="warning",
            )

    # Phase 6: Document Generation Admin Actions
    @admin.action(description=_("Generate packing slips for selected orders"))
    def generate_packing_slips(self, request, queryset):
        """Admin action to generate packing slips for selected orders"""
        from shipping.services.document_service import DocumentService

        generated_count = 0
        skipped_count = 0
        error_count = 0

        for order in queryset:
            # Get first shipment for this order
            shipment = order.shipments.first()

            if not shipment:
                skipped_count += 1
                continue

            try:
                # Generate packing slip
                data_uri = DocumentService.generate_packing_slip(shipment)
                shipment.packing_slip_url = data_uri
                shipment.save(update_fields=["packing_slip_url"])
                generated_count += 1
            except Exception as e:
                error_count += 1
                self.message_user(
                    request,
                    _("Failed to generate packing slip for order %(order_number)s: %(error)s")
                    % {"order_number": order.order_number, "error": str(e)},
                    level="error",
                )

        if generated_count > 0:
            self.message_user(
                request,
                _("Successfully generated %(count)d packing slip(s).") % {"count": generated_count},
                level="success",
            )

        if skipped_count > 0:
            self.message_user(
                request,
                _("Skipped %(count)d order(s) without shipments.") % {"count": skipped_count},
                level="warning",
            )

    @admin.action(description=_("Generate commercial invoices for selected orders"))
    def generate_commercial_invoices(self, request, queryset):
        """Admin action to generate commercial invoices for selected orders"""
        from shipping.services.document_service import DocumentService

        generated_count = 0
        skipped_count = 0
        error_count = 0

        for order in queryset:
            # Get first shipment for this order
            shipment = order.shipments.first()

            if not shipment:
                skipped_count += 1
                continue

            try:
                # Generate commercial invoice
                data_uri = DocumentService.generate_commercial_invoice(shipment)
                shipment.commercial_invoice_url = data_uri
                shipment.save(update_fields=["commercial_invoice_url"])
                generated_count += 1
            except Exception as e:
                error_count += 1
                self.message_user(
                    request,
                    _("Failed to generate commercial invoice for order %(order_number)s: %(error)s")
                    % {"order_number": order.order_number, "error": str(e)},
                    level="error",
                )

        if generated_count > 0:
            self.message_user(
                request,
                _("Successfully generated %(count)d commercial invoice(s).")
                % {"count": generated_count},
                level="success",
            )

        if skipped_count > 0:
            self.message_user(
                request,
                _("Skipped %(count)d order(s) without shipments.") % {"count": skipped_count},
                level="warning",
            )

    @admin.action(description=_("Generate customs forms for selected orders"))
    def generate_customs_forms(self, request, queryset):
        """Admin action to generate customs forms for selected orders"""
        from shipping.services.document_service import DocumentService

        generated_count = 0
        skipped_count = 0
        error_count = 0

        for order in queryset:
            # Get first shipment for this order
            shipment = order.shipments.first()

            if not shipment:
                skipped_count += 1
                continue

            try:
                # Determine form type based on shipment characteristics
                # CN22: up to 2kg and value <= 425 EUR
                # CN23: over 2kg or value > 425 EUR
                # For simplicity, we'll use CN23 as default (more comprehensive)
                form_type = "CN23"

                # Generate customs form
                data_uri = DocumentService.generate_customs_form(shipment, form_type=form_type)
                shipment.customs_form_url = data_uri
                shipment.save(update_fields=["customs_form_url"])
                generated_count += 1
            except Exception as e:
                error_count += 1
                self.message_user(
                    request,
                    _("Failed to generate customs form for order %(order_number)s: %(error)s")
                    % {"order_number": order.order_number, "error": str(e)},
                    level="error",
                )

        if generated_count > 0:
            self.message_user(
                request,
                _("Successfully generated %(count)d customs form(s).") % {"count": generated_count},
                level="success",
            )

        if skipped_count > 0:
            self.message_user(
                request,
                _("Skipped %(count)d order(s) without shipments.") % {"count": skipped_count},
                level="warning",
            )

    def get_urls(self):
        """Add custom URLs for order admin"""
        urls = super().get_urls()
        custom_urls = [
            path(
                "<path:object_id>/add-tracking/",
                self.admin_site.admin_view(self.add_tracking_view),
                name="orders_order_add_tracking",
            ),
        ]
        return custom_urls + urls

    def add_tracking_view(self, request, object_id):
        """Handle quick tracking number addition"""
        if request.method != "POST":
            return HttpResponseRedirect(reverse("admin:orders_order_change", args=[object_id]))

        try:
            order = Order.objects.get(pk=object_id)
            from shipping.models import CarrierPreset, Shipment

            carrier_id = request.POST.get("carrier")
            tracking_number = request.POST.get("tracking_number", "").strip()

            if not carrier_id or not tracking_number:
                messages.error(request, _("Please provide both carrier and tracking number"))
                return HttpResponseRedirect(reverse("admin:orders_order_change", args=[object_id]))

            try:
                carrier = CarrierPreset.objects.get(pk=carrier_id, is_active=True)
            except CarrierPreset.DoesNotExist:
                messages.error(request, _("Invalid carrier selected"))
                return HttpResponseRedirect(reverse("admin:orders_order_change", args=[object_id]))

            # Create shipment
            Shipment.objects.create(
                order=order,
                user=request.user,
                carrier_preset=carrier,
                origin_country=get_shipping_origin_country(),
                dest_country=order.shipping_country or get_shipping_origin_country(),
                tracking_id=tracking_number,
                status="in_transit",
            )

            messages.success(
                request, _(f"Tracking number {tracking_number} added via {carrier.name}")
            )

        except Order.DoesNotExist:
            messages.error(request, _("Order not found"))
        except Exception as e:
            messages.error(request, _(f"Error adding tracking: {str(e)}"))

        return HttpResponseRedirect(reverse("admin:orders_order_change", args=[object_id]))

    def change_view(self, request, object_id, form_url="", extra_context=None):
        """Handle quick action buttons in order detail view"""
        extra_context = extra_context or {}

        # Add shipping context
        try:
            order = Order.objects.get(pk=object_id)
            from orders.models import OrderNote
            from shipping.models import CarrierPreset, Shipment

            # Get shipments for this order
            shipments = (
                Shipment.objects.filter(order=order)
                .select_related("carrier_preset", "provider_account", "provider_account__component")
                .order_by("-created_at")
            )

            # Get available carriers for dropdown
            available_carriers = CarrierPreset.objects.filter(is_active=True).order_by("name")

            extra_context["shipments"] = shipments
            extra_context["available_carriers"] = available_carriers

            # Get applied vouchers for discounts section
            try:
                from vouchers.models import AppliedVoucher

                applied_vouchers = AppliedVoucher.objects.filter(order=order).select_related(
                    "voucher"
                )
                extra_context["applied_vouchers"] = applied_vouchers
            except Exception:
                extra_context["applied_vouchers"] = []

            # Get active customers for customer change dropdown
            from django.contrib.auth import get_user_model

            User = get_user_model()
            customers = User.objects.filter(is_active=True).order_by("email")[
                :100
            ]  # Limit to 100 for performance
            extra_context["customers"] = customers

            # Get order notes for timeline (including system notes for payment changes, etc.)
            order_notes = (
                OrderNote.objects.filter(order=order)
                .select_related("author")
                .order_by("-created_at")
            )
            extra_context["order_notes"] = order_notes

        except Order.DoesNotExist:
            pass

        # Handle quick actions from POST
        if request.method == "POST" and "action" in request.POST:
            try:
                order = Order.objects.get(pk=object_id)
                action = request.POST.get("action")

                if action == "mark_as_processing":
                    old_status = order.get_status_display()
                    order.status = "processing"
                    order.save()
                    OrderNote.objects.create(
                        order=order,
                        author=request.user,
                        note=f'Order status changed from "{old_status}" to "Processing"',
                        is_customer_note=False,
                    )
                    messages.success(request, _("Order marked as processing"))
                elif action == "mark_as_shipped":
                    old_status = order.get_status_display()
                    order.status = "shipped"
                    order.save()
                    OrderNote.objects.create(
                        order=order,
                        author=request.user,
                        note=f'Order status changed from "{old_status}" to "Shipped"',
                        is_customer_note=False,
                    )
                    messages.success(request, _("Order marked as shipped"))
                elif action == "mark_as_delivered":
                    old_status = order.get_status_display()
                    order.status = "delivered"
                    order.save()
                    OrderNote.objects.create(
                        order=order,
                        author=request.user,
                        note=f'Order status changed from "{old_status}" to "Delivered"',
                        is_customer_note=False,
                    )
                    messages.success(request, _("Order marked as delivered"))
                elif action == "mark_as_cancelled":
                    old_status = order.get_status_display()
                    order.status = "cancelled"
                    order.save()
                    OrderNote.objects.create(
                        order=order,
                        author=request.user,
                        note=f'Order status changed from "{old_status}" to "Cancelled"',
                        is_customer_note=False,
                    )
                    messages.warning(request, _("Order has been cancelled"))
                elif action == "change_status":
                    # Direct status change from dropdown
                    new_status = request.POST.get("new_status", "").strip()
                    valid_statuses = [
                        "pending",
                        "processing",
                        "shipped",
                        "delivered",
                        "cancelled",
                        "refunded",
                    ]

                    if new_status and new_status in valid_statuses and new_status != order.status:
                        old_status_display = order.get_status_display()
                        order.status = new_status
                        order.save()

                        # Process gift card refunds when order is refunded
                        if new_status == "refunded":
                            try:
                                from catalog.services.gift_card_service import GiftCardService

                                gc_count = GiftCardService.process_gift_card_refund(order)
                                if gc_count > 0:
                                    messages.info(
                                        request,
                                        _("%(count)d gift card(s) processed for refund")
                                        % {"count": gc_count},
                                    )
                            except Exception as e:
                                logger.error(
                                    f"Gift card refund processing failed for order {order.order_number}: {e}"
                                )

                        # Create system note for audit trail
                        OrderNote.objects.create(
                            order=order,
                            author=request.user,
                            note=f'Order status changed from "{old_status_display}" to "{order.get_status_display()}"',
                            is_customer_note=False,
                        )

                        messages.success(
                            request, _(f"Order status changed to {order.get_status_display()}")
                        )
                    elif new_status == order.status:
                        messages.info(request, _("Order is already in this status"))
                    else:
                        messages.error(request, _("Please select a valid status"))
                elif action == "mark_as_paid":
                    from django.utils import timezone

                    from orders.models import OrderNote

                    old_status = order.get_payment_status_display()
                    order.payment_status = "paid"
                    order.paid_at = timezone.now()
                    order.amount_paid = order.total_amount

                    # Record payment method if provided
                    payment_method = request.POST.get("payment_method", "").strip()
                    payment_reference = request.POST.get("payment_reference", "").strip()
                    if payment_method:
                        order.payment_method_type = payment_method
                    if payment_reference:
                        order.payment_method_last4 = (
                            payment_reference[-4:]
                            if len(payment_reference) > 4
                            else payment_reference
                        )

                    order.save()

                    # Create system note for audit trail
                    note_parts = [f'Payment status changed from "{old_status}" to "Paid"']
                    if payment_method:
                        note_parts.append(f"Payment method: {payment_method}")
                    if payment_reference:
                        note_parts.append(f"Reference: {payment_reference}")
                    note_parts.append(f"Amount: {order.amount_paid}")

                    OrderNote.objects.create(
                        order=order,
                        author=request.user,
                        note="\n".join(note_parts),
                        is_customer_note=False,
                    )

                    messages.success(request, _("Order marked as paid"))
                elif action == "mark_as_unpaid":
                    from orders.models import OrderNote

                    old_status = order.get_payment_status_display()
                    order.payment_status = "unpaid"
                    order.paid_at = None
                    order.save()

                    # Create system note for audit trail
                    OrderNote.objects.create(
                        order=order,
                        author=request.user,
                        note=f'Payment status changed from "{old_status}" to "Unpaid"',
                        is_customer_note=False,
                    )

                    messages.warning(request, _("Order marked as unpaid"))
                elif action == "mark_payment_pending":
                    from orders.models import OrderNote

                    old_status = order.get_payment_status_display()
                    order.payment_status = "pending"
                    order.save()

                    # Create system note for audit trail
                    OrderNote.objects.create(
                        order=order,
                        author=request.user,
                        note=f'Payment status changed from "{old_status}" to "Pending"',
                        is_customer_note=False,
                    )

                    messages.info(request, _("Order payment marked as pending"))
                elif action == "assign_affiliate":
                    # Assign affiliate to order
                    from decimal import Decimal

                    from affiliate.models import Affiliate, Commission, Program

                    affiliate_id = request.POST.get("affiliate_id")
                    if affiliate_id:
                        try:
                            affiliate = Affiliate.objects.get(pk=affiliate_id, status="active")

                            # Get default program
                            program = Program.objects.filter(status="active").first()
                            if not program:
                                messages.error(request, _("No active affiliate program found"))
                            else:
                                # Calculate commission amount
                                if program.commission_type == "percentage":
                                    commission_amount = (
                                        order.total_amount.amount
                                        * Decimal(program.commission_value)
                                    ) / Decimal(100)
                                else:
                                    commission_amount = Decimal(program.commission_value)

                                # Create commission
                                Commission.objects.create(
                                    affiliate=affiliate,
                                    program=program,
                                    order=order,
                                    amount=commission_amount,
                                    status="pending",
                                )

                                messages.success(
                                    request,
                                    _(f"Order attributed to {affiliate.user.get_full_name()}"),
                                )
                        except Affiliate.DoesNotExist:
                            messages.error(request, _("Invalid affiliate selected"))
                    else:
                        messages.error(request, _("No affiliate selected"))
                elif action == "remove_affiliate":
                    # Remove affiliate attribution
                    from affiliate.models import Commission

                    deleted_count = order.affiliate_commissions.all().delete()[0]
                    if deleted_count > 0:
                        messages.success(request, _("Affiliate attribution removed"))
                    else:
                        messages.warning(request, _("No affiliate attribution found"))
                elif action == "add_note":
                    # Add note to order
                    from orders.models import OrderNote

                    note_content = request.POST.get("note_content", "").strip()
                    is_customer_note = request.POST.get("is_customer_note") == "1"

                    if note_content:
                        OrderNote.objects.create(
                            order=order,
                            author=request.user,
                            note=note_content,
                            is_customer_note=is_customer_note,
                        )

                        note_type = _("customer-visible") if is_customer_note else _("private")
                        messages.success(request, _(f"Added {note_type} note to order"))
                    else:
                        messages.error(request, _("Note content cannot be empty"))

                # Redirect to same page to show updated status
                return redirect(request.path)
            except Order.DoesNotExist:
                messages.error(request, _("Order not found"))

        return super().change_view(request, object_id, form_url, extra_context)

    def add_view(self, request, form_url="", extra_context=None):
        """Create a draft order and redirect to the modern editing interface"""
        from django.contrib.auth import get_user_model
        from djmoney.money import Money

        User = get_user_model()

        # Create a draft order with minimal required fields
        # Get a default user (admin or first user)
        default_user = request.user if request.user.is_authenticated else User.objects.first()

        if not default_user:
            messages.error(request, _("No users available. Please create a user first."))
            return redirect("admin:orders_order_changelist")

        # Create draft order
        from django.utils.translation import get_language

        order = Order.objects.create(
            user=default_user,
            email=default_user.email,
            status="draft",
            source="admin",
            subtotal=Money("0.00", get_default_currency()),
            total_amount=Money("0.00", get_default_currency()),
            language=get_language() or "en",
        )

        messages.success(
            request,
            _("Draft order %(order_number)s created. Add items and customer details below.")
            % {"order_number": order.order_number},
        )

        # Redirect to the change view which uses the modern interface
        return redirect("admin:orders_order_change", order.pk)

    def changelist_view(self, request, extra_context=None):
        """Add order statistics and filtered orders to context"""
        extra_context = extra_context or {}

        # Get overall statistics (unfiltered)
        stats = Order.objects.aggregate(
            total_count=Count("id"),
            pending_count=Count("id", filter=Q(status="pending")),
            processing_count=Count("id", filter=Q(status="processing")),
            shipped_count=Count("id", filter=Q(status="shipped")),
            delivered_count=Count("id", filter=Q(status="delivered")),
            cancelled_count=Count("id", filter=Q(status="cancelled")),
            refunded_count=Count("id", filter=Q(status="refunded")),
            total_revenue=Sum(
                "total_amount", filter=Q(status__in=["processing", "shipped", "delivered"])
            ),
        )

        extra_context.update(
            {
                "total_orders": stats["total_count"] or 0,
                "pending_count": stats["pending_count"] or 0,
                "processing_count": stats["processing_count"] or 0,
                "shipped_count": stats["shipped_count"] or 0,
                "delivered_count": stats["delivered_count"] or 0,
                "cancelled_count": stats["cancelled_count"] or 0,
                "refunded_count": stats["refunded_count"] or 0,
                "total_revenue": stats["total_revenue"] or 0,
            }
        )

        # Get URL parameters for filtering
        status_filter = request.GET.get("status", "")
        search_query = request.GET.get("q", "")
        page = int(request.GET.get("page", 1))
        per_page = 100

        # Start with base queryset
        orders_qs = Order.objects.select_related("user").prefetch_related(
            "items__product__images",
            "items__component_items__product__images",
        )

        # Apply status filter
        if status_filter and status_filter != "all":
            orders_qs = orders_qs.filter(status=status_filter)

        # Apply search filter
        if search_query:
            orders_qs = orders_qs.filter(
                Q(order_number__icontains=search_query)
                | Q(user__first_name__icontains=search_query)
                | Q(user__last_name__icontains=search_query)
                | Q(user__username__icontains=search_query)
                | Q(email__icontains=search_query)
                | Q(phone__icontains=search_query)
                | Q(items__product__name__icontains=search_query)
            ).distinct()

        # Order by most recent
        orders_qs = orders_qs.order_by("-created_at")

        # Get total count of filtered results
        total = orders_qs.count()

        # Paginate
        start = (page - 1) * per_page
        end = start + per_page

        # Pass filtered orders and context to template
        extra_context.update(
            {
                "recent_orders": orders_qs[start:end],
                "has_more_orders": total > end,
                "current_page": page,
                "total_order_count": total,
                "current_status": status_filter if status_filter else "all",
                "current_search": search_query,
                "filtered_count": total,  # Count of results after filters
            }
        )

        return super().changelist_view(request, extra_context=extra_context)


class CustomizationValueInline(admin.TabularInline):
    """Inline admin for customization values"""

    from catalog.models import CustomizationValue

    model = CustomizationValue
    extra = 0
    fields = ["customization_option", "display_value", "calculated_price"]
    readonly_fields = ["customization_option", "display_value", "calculated_price"]
    can_delete = False

    def display_value(self, obj):
        """Display the customization value in human-readable format"""
        return obj.get_display_value()

    display_value.short_description = _("Value")

    def has_add_permission(self, request, obj=None):
        """Prevent adding customizations through admin"""
        return False


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "product_name", "quantity", "unit_price", "total_price"]
    list_filter = ["order__status", "created_at"]
    search_fields = ["order__order_number", "product_name", "sku"]
    inlines = [CustomizationValueInline]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "name",
        "city",
        "state",
        "address_type_badge",
        "is_default",
        "version_info",
        "usage_count",
        "is_active",
    ]
    list_filter = ["address_type", "is_default", "is_active", "country", "version"]
    search_fields = ["user__username", "user__email", "name", "city", "address1"]
    readonly_fields = [
        "created_at",
        "updated_at",
        "edited_at",
        "version",
        "original_address",
        "order_usage",
    ]

    fieldsets = (
        (
            _("Address Information"),
            {
                "fields": (
                    "user",
                    "address_type",
                    "is_default",
                    "is_active",
                    "name",
                    "company",
                    "address1",
                    "address2",
                    "city",
                    "state",
                    "postal_code",
                    "country",
                    "phone",
                )
            },
        ),
        (
            _("Versioning & Audit"),
            {
                "fields": ("version", "original_address", "edited_at", "order_usage"),
                "classes": ("collapse",),
            },
        ),
        (_("Timestamps"), {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def address_type_badge(self, obj):
        """Display address type with color badge"""
        return format_html(
            '<span class="admin-badge admin-badge-sm admin-badge-address-{}">{}</span>',
            obj.address_type,
            obj.get_address_type_display(),
        )

    address_type_badge.short_description = _("Type")

    def version_info(self, obj):
        """Display version information"""
        if obj.version > 1:
            return format_html(
                '<span class="admin-text-warning admin-text-bold">v{}</span>', obj.version
            )
        return format_html('<span class="admin-text-muted">v1</span>')

    version_info.short_description = _("Version")

    def usage_count(self, obj):
        """Display order usage count"""
        count = obj.get_order_count()
        if count > 0:
            return format_html(
                '<a href="{}?shipping_address_ref={}" class="admin-text-bold">{} {}</a>',
                reverse("admin:orders_order_changelist"),
                obj.pk,
                count,
                _("order" if count == 1 else "orders"),
            )
        return format_html('<span class="admin-text-muted">—</span>')

    usage_count.short_description = _("Used in")

    def order_usage(self, obj):
        """Detailed order usage information"""
        count = obj.get_order_count()
        if count > 0:
            return format_html(
                '<div class="admin-usage-info">'
                "<p><strong>{}</strong></p>"
                '<a href="{}?shipping_address_ref={}" class="button">{}</a>'
                '<a href="{}?billing_address_ref={}" class="button">{}</a>'
                "</div>",
                _("This address has been used in {} order(s)").format(count),
                reverse("admin:orders_order_changelist"),
                obj.pk,
                _("View as Shipping"),
                reverse("admin:orders_order_changelist"),
                obj.pk,
                _("View as Billing"),
            )
        return format_html('<em class="admin-text-muted">{}</em>', _("Not used in any orders"))

    order_usage.short_description = _("Order Usage")

    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        return super().get_queryset(request).select_related("user", "original_address")


@admin.register(OrderNote)
class OrderNoteAdmin(admin.ModelAdmin):
    list_display = ["order", "author", "is_customer_note", "created_at"]
    list_filter = ["is_customer_note", "created_at"]
    search_fields = ["order__order_number", "author__username", "note"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        (None, {"fields": ("order", "author", "note", "is_customer_note")}),
        (_("Timestamps"), {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    """Admin interface for refund management"""

    list_display = [
        "order",
        "refund_type",
        "status_badge",
        "reason",
        "total_amount",
        "processed_by",
        "created_at",
    ]
    list_filter = ["status", "refund_type", "reason", "created_at", "approved_at", "completed_at"]
    search_fields = [
        "order__order_number",
        "order__user__username",
        "order__user__email",
        "customer_notes",
        "staff_notes",
    ]
    readonly_fields = [
        "created_at",
        "approved_at",
        "processed_at",
        "completed_at",
        "calculated_items_total",
    ]

    actions = ["approve_refunds", "mark_as_processing", "mark_as_completed"]

    fieldsets = (
        (
            _("Refund Information"),
            {"fields": ("order", "refund_type", "status", "reason", "processed_by")},
        ),
        (
            _("Refund Amounts"),
            {
                "fields": (
                    "total_amount",
                    "shipping_refund_amount",
                    "tax_refund_amount",
                    "calculated_items_total",
                )
            },
        ),
        (
            _("Item Details"),
            {"fields": ("items_json",), "description": "Item-level refund details in JSON format"},
        ),
        (_("Notes"), {"fields": ("customer_notes", "staff_notes")}),
        (
            _("Timestamps"),
            {
                "fields": ("created_at", "approved_at", "processed_at", "completed_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def get_form(self, request, obj=None, **kwargs):
        """Override to filter MoneyField currency choices"""
        form = super().get_form(request, obj, **kwargs)
        from core.admin_mixins import _apply_money_field_currency_defaults

        _apply_money_field_currency_defaults(form, obj)
        return form

    def status_badge(self, obj):
        """Display status with color badge"""
        return format_html(
            '<span class="admin-badge admin-badge-refund-{}">{}</span>',
            obj.status,
            obj.get_status_display(),
        )

    status_badge.short_description = _("Status")

    def calculated_items_total(self, obj):
        """Display calculated total from items JSON"""
        if obj.pk:
            return format_html("{}", obj.calculate_items_total())
        return "-"

    calculated_items_total.short_description = _("Items Total")

    # Bulk actions
    @admin.action(description=_("Approve selected refunds"))
    def approve_refunds(self, request, queryset):
        """Bulk approve refunds"""
        updated = 0
        for refund in queryset.filter(status="requested"):
            refund.approve(user=request.user)
            updated += 1
        self.message_user(request, _(f"{updated} refunds approved"))

    @admin.action(description=_("Mark selected refunds as Processing"))
    def mark_as_processing(self, request, queryset):
        """Bulk mark as processing"""
        updated = 0
        for refund in queryset.filter(status="approved"):
            refund.start_processing()
            updated += 1
        self.message_user(request, _(f"{updated} refunds marked as processing"))

    @admin.action(description=_("Mark selected refunds as Completed"))
    def mark_as_completed(self, request, queryset):
        """Bulk mark as completed"""
        updated = 0
        for refund in queryset.filter(status="processing"):
            refund.complete()
            updated += 1
        self.message_user(request, _(f"{updated} refunds marked as completed"))

    def save_model(self, request, obj, form, change):
        """Auto-set processed_by if approving"""
        if not change:  # New refund
            if obj.status == "approved" and not obj.processed_by:
                obj.processed_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ReturnRequest)
class ReturnRequestAdmin(admin.ModelAdmin):
    """
    Admin interface for return request management (Phase 7: Returns & RMA).
    Supports full return workflow from request to completion.
    """

    change_list_template = "admin/orders/returnrequest/change_list.html"
    change_form_template = "admin/orders/returnrequest/change_form.html"

    list_display = [
        "order",
        "user",
        "status_badge",
        "reason",
        "items_summary",
        "return_tracking_link",
        "requested_at",
        "has_refund",
    ]
    list_filter = [
        "status",
        "reason",
        "items_condition",
        "requested_at",
        "approved_at",
        "received_at",
        "inspected_at",
        "completed_at",
    ]
    search_fields = [
        "order__order_number",
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
        "return_tracking_number",
        "customer_notes",
        "merchant_notes",
    ]
    readonly_fields = [
        "requested_at",
        "approved_at",
        "rejected_at",
        "label_sent_at",
        "received_at",
        "inspected_at",
        "completed_at",
        "updated_at",
        "suggested_refund_amount",
        "items_summary",
    ]

    actions = [
        "approve_returns",
        "reject_returns",
        "mark_label_sent",
        "mark_received",
        "cancel_returns",
    ]

    fieldsets = (
        (
            _("Return Request Information"),
            {
                "fields": (
                    "order",
                    "user",
                    "status",
                    "reason",
                    "items_summary",
                    "suggested_refund_amount",
                ),
                "classes": ("tab-details",),
            },
        ),
        (
            _("Items Being Returned"),
            {
                "fields": ("items_json",),
                "classes": ("tab-items",),
            },
        ),
        (
            _("Return Shipping"),
            {
                "fields": (
                    "return_shipment",
                    "return_label_generated",
                    "return_tracking_number",
                    "return_label_url",
                ),
                "classes": ("tab-shipping",),
            },
        ),
        (
            _("Inspection Results"),
            {
                "fields": ("items_condition", "inspection_notes", "restocking_fee", "inspected_by"),
                "classes": ("tab-inspection",),
            },
        ),
        (
            _("Notes & Communication"),
            {
                "fields": ("customer_notes", "merchant_notes", "rejection_reason"),
                "classes": ("tab-notes",),
            },
        ),
        (
            _("Refund Processing"),
            {
                "fields": ("refund",),
                "classes": ("tab-refund",),
            },
        ),
        (
            _("Workflow Tracking"),
            {
                "fields": ("approved_by",),
                "classes": ("tab-workflow",),
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": (
                    "requested_at",
                    "approved_at",
                    "rejected_at",
                    "label_sent_at",
                    "received_at",
                    "inspected_at",
                    "completed_at",
                    "updated_at",
                ),
                "classes": ("tab-timestamps",),
            },
        ),
    )

    def change_view(self, request, object_id, form_url="", extra_context=None):
        """Add dashboard context for edit mode."""
        extra_context = extra_context or {}

        if object_id:
            try:
                obj = self.get_object(request, object_id)
                if obj:
                    # Items count
                    items_count = len(obj.items_json) if obj.items_json else 0

                    # Suggested refund
                    try:
                        suggested = obj.calculate_refund_amount()
                        currency = (
                            obj.order.total_amount.currency.code
                            if hasattr(obj.order.total_amount, "currency")
                            else get_default_currency()
                        )
                        suggested_refund = f"{currency} {suggested}"
                    except Exception:
                        suggested_refund = "-"

                    # Workflow step (1-7 based on status)
                    step_map = {
                        "pending": 1,
                        "approved": 2,
                        "label_sent": 3,
                        "in_transit": 4,
                        "received": 5,
                        "inspected": 6,
                        "completed": 7,
                        "rejected": 2,
                        "cancelled": 0,
                    }
                    workflow_step = step_map.get(obj.status, 0)

                    # Days open
                    from django.utils import timezone

                    if obj.completed_at:
                        days_open = (obj.completed_at - obj.requested_at).days
                    else:
                        days_open = (timezone.now() - obj.requested_at).days

                    extra_context.update(
                        {
                            "items_count": items_count,
                            "suggested_refund": suggested_refund,
                            "workflow_step": workflow_step,
                            "days_open": days_open,
                        }
                    )
            except Exception:
                pass

        return super().change_view(request, object_id, form_url, extra_context)

    def get_form(self, request, obj=None, **kwargs):
        """Override to filter MoneyField currency choices"""
        form = super().get_form(request, obj, **kwargs)
        from core.admin_mixins import _apply_money_field_currency_defaults

        _apply_money_field_currency_defaults(form, obj)
        return form

    def status_badge(self, obj):
        """Display status with color badge"""
        return format_html(
            '<span class="admin-badge admin-badge-return-{}">{}</span>',
            obj.status,
            obj.get_status_display(),
        )

    status_badge.short_description = _("Status")

    def items_summary(self, obj):
        """Display summary of items being returned"""
        return format_html('<span class="admin-text-muted">{}</span>', obj.get_items_summary())

    items_summary.short_description = _("Items")

    def return_tracking_link(self, obj):
        """Display return tracking number with link if available"""
        if not obj.return_tracking_number:
            return format_html('<em class="admin-text-muted">{}</em>', _("No tracking"))

        # If return shipment has tracking URL, use it
        if obj.return_shipment and hasattr(obj.return_shipment, "get_tracking_url"):
            tracking_url = obj.return_shipment.get_tracking_url()
            if tracking_url:
                return format_html(
                    '<a href="{}" target="_blank" rel="noopener">'
                    '<i class="fas fa-external-link-alt"></i> {}'
                    "</a>",
                    tracking_url,
                    obj.return_tracking_number,
                )

        # Otherwise just display tracking number
        return format_html("<code>{}</code>", obj.return_tracking_number)

    return_tracking_link.short_description = _("Return Tracking")

    def has_refund(self, obj):
        """Show if refund has been processed"""
        if obj.refund:
            return format_html(
                '<a href="{}" class="admin-text-success">'
                '<i class="fas fa-check-circle"></i> {}'
                "</a>",
                reverse("admin:orders_refund_change", args=[obj.refund.pk]),
                _("View Refund"),
            )
        return format_html('<em class="admin-text-muted">{}</em>', _("No refund"))

    has_refund.short_description = _("Refund")

    def suggested_refund_amount(self, obj):
        """Display suggested refund amount based on returned items"""
        if obj.pk:
            amount = obj.calculate_refund_amount()
            return format_html(
                "<strong>{} {}</strong>", obj.order.total_amount.currency.code, amount
            )
        return "-"

    suggested_refund_amount.short_description = _("Suggested Refund Amount")

    # Bulk actions
    @admin.action(description=_("Approve selected return requests"))
    def approve_returns(self, request, queryset):
        """Bulk approve return requests"""
        updated = 0
        for return_request in queryset.filter(status="pending"):
            return_request.approve(user=request.user)
            updated += 1
        self.message_user(
            request,
            _(
                "%(count)d return request(s) approved. Return labels should be generated and sent to customers."
            )
            % {"count": updated},
            level="success",
        )

    @admin.action(description=_("Reject selected return requests"))
    def reject_returns(self, request, queryset):
        """Bulk reject return requests (requires reason in individual view)"""
        pending_count = queryset.filter(status="pending").count()
        if pending_count > 0:
            self.message_user(
                request,
                _(
                    "Cannot bulk reject returns. Please reject individually to provide rejection reasons."
                ),
                level="warning",
            )
        else:
            self.message_user(request, _("No pending returns to reject."), level="info")

    @admin.action(description=_("Mark return labels as sent"))
    def mark_label_sent(self, request, queryset):
        """Bulk mark return labels as sent"""
        updated = 0
        for return_request in queryset.filter(status="approved"):
            return_request.mark_label_sent()
            updated += 1
        self.message_user(
            request,
            _("%(count)d return label(s) marked as sent.") % {"count": updated},
            level="success",
        )

    @admin.action(description=_("Mark returns as received"))
    def mark_received(self, request, queryset):
        """Bulk mark returns as received at warehouse"""
        updated = 0
        for return_request in queryset.filter(status__in=["label_sent", "in_transit"]):
            return_request.mark_received(user=request.user)
            updated += 1
        self.message_user(
            request,
            _("%(count)d return(s) marked as received. Please inspect items and process refunds.")
            % {"count": updated},
            level="success",
        )

    @admin.action(description=_("Cancel selected return requests"))
    def cancel_returns(self, request, queryset):
        """Bulk cancel return requests"""
        updated = 0
        for return_request in queryset.exclude(status__in=["completed", "cancelled"]):
            return_request.cancel()
            updated += 1
        self.message_user(
            request,
            _("%(count)d return request(s) cancelled.") % {"count": updated},
            level="warning",
        )

    def save_model(self, request, obj, form, change):
        """Auto-set approved_by/inspected_by when status changes"""
        if change:  # Existing return request
            # Get original object to compare
            original = ReturnRequest.objects.get(pk=obj.pk)

            # Auto-set approved_by if status changed to approved/rejected
            if obj.status in ["approved", "rejected"] and original.status == "pending":
                if not obj.approved_by:
                    obj.approved_by = request.user

            # Auto-set inspected_by if status changed to inspected
            if obj.status == "inspected" and original.status != "inspected":
                if not obj.inspected_by:
                    obj.inspected_by = request.user

        super().save_model(request, obj, form, change)

    def changelist_view(self, request, extra_context=None):
        """Add context for the custom change list template"""
        extra_context = extra_context or {}
        extra_context["pending_count"] = ReturnRequest.objects.filter(status="pending").count()
        extra_context["approved_count"] = ReturnRequest.objects.filter(status="approved").count()
        extra_context["in_transit_count"] = ReturnRequest.objects.filter(
            status="in_transit"
        ).count()
        extra_context["completed_count"] = ReturnRequest.objects.filter(status="completed").count()
        return super().changelist_view(request, extra_context=extra_context)
