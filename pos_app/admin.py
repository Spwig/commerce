from datetime import timedelta

from django.contrib import admin
from django.db.models import BooleanField, Case, Count, Value, When
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from catalog.models import Warehouse
from media_library.widgets import MediaLibrarySelectWidget

from .models import (
    CashMovement,
    POSPayment,
    POSShift,
    POSStaffDiscount,
    POSTerminal,
    POSTerminalProvider,
    POSTerminalReader,
    PromoSlide,
    ReceiptTemplate,
    StoreGroup,
    TerminalLockEvent,
)


@admin.register(POSTerminal)
class POSTerminalAdmin(admin.ModelAdmin):
    change_list_template = "admin/pos_app/posterminal/change_list.html"
    change_form_template = "admin/pos_app/posterminal/change_form.html"
    list_display = [
        "name",
        "warehouse",
        "is_active",
        "last_heartbeat_display",
        "assigned_users_count",
        "pairing_code",
    ]
    list_filter = ["is_active", "warehouse"]
    search_fields = ["name", "uuid", "pairing_code"]
    readonly_fields = ["uuid", "created_at", "updated_at", "last_heartbeat", "remote_unlock_at"]
    autocomplete_fields = ["assigned_users"]

    fieldsets = (
        (
            _("Basic Information"),
            {
                "fields": ("name", "warehouse", "is_active", "currency"),
                "classes": ("tab-basic",),
            },
        ),
        (
            _("Device Pairing"),
            {
                "fields": ("uuid", "pairing_code"),
                "classes": ("tab-device",),
            },
        ),
        (
            _("Hardware Configuration"),
            {
                "fields": ("hardware_config",),
                "classes": ("tab-device-hw",),
            },
        ),
        (
            _("Sync & Cache"),
            {
                "fields": ("order_sync_days", "order_sync_limit"),
                "classes": ("tab-sync",),
            },
        ),
        (
            _("Staff Assignment"),
            {
                "fields": ("assigned_users",),
                "classes": ("tab-staff",),
            },
        ),
        (
            _("Status"),
            {
                "fields": ("last_heartbeat", "remote_unlock_at", "created_at", "updated_at"),
                "classes": ("tab-status",),
            },
        ),
    )

    class Media:
        css = {"all": ("pos_app/admin/css/posterminal_form.css",)}
        js = ("pos_app/admin/js/posterminal_form.js",)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "assigned_users":
            kwargs["queryset"] = db_field.related_model.objects.filter(is_staff=True)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        online_cutoff = timezone.now() - timedelta(seconds=300)
        qs = (
            qs.select_related("warehouse")
            .prefetch_related("assigned_users")
            .annotate(
                shift_count=Count("shifts", distinct=True),
                staff_count=Count("assigned_users", distinct=True),
                is_online=Case(
                    When(last_heartbeat__gte=online_cutoff, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField(),
                ),
            )
        )
        return qs

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        if object_id:
            obj = self.get_object(request, object_id)
            if obj:
                online_cutoff = timezone.now() - timedelta(seconds=300)
                extra_context["is_online"] = (
                    obj.last_heartbeat is not None and obj.last_heartbeat >= online_cutoff
                )
        return super().change_view(request, object_id, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        retail_warehouses = Warehouse.objects.filter(is_retail_location=True).order_by("name")
        extra_context["warehouses"] = retail_warehouses
        extra_context["has_store_locations"] = retail_warehouses.exists()

        if not extra_context["has_store_locations"]:
            active_warehouses = Warehouse.objects.filter(is_active=True).order_by("name")
            extra_context["warehouse_count"] = active_warehouses.count()
            if active_warehouses.count() == 1:
                extra_context["main_warehouse"] = active_warehouses.first()

        return super().changelist_view(request, extra_context=extra_context)

    def last_heartbeat_display(self, obj):
        if not obj.last_heartbeat:
            return _("Never")
        delta = timezone.now() - obj.last_heartbeat
        if delta.total_seconds() < 300:  # 5 minutes
            return _("Online")
        return _("Offline (%s ago)") % timezone.timesince(obj.last_heartbeat)

    last_heartbeat_display.short_description = _("Status")

    def assigned_users_count(self, obj):
        return obj.assigned_users.count()

    assigned_users_count.short_description = _("Staff")

    actions = ["regenerate_pairing_codes", "remote_unlock_terminals"]

    @admin.action(description=_("Regenerate pairing codes"))
    def regenerate_pairing_codes(self, request, queryset):
        for terminal in queryset:
            terminal.regenerate_pairing_code()
        self.message_user(
            request, _("Pairing codes regenerated for %d terminals.") % queryset.count()
        )

    @admin.action(description=_("Unlock terminal (remote)"))
    def remote_unlock_terminals(self, request, queryset):
        count = queryset.update(remote_unlock_at=timezone.now())
        self.message_user(
            request,
            _("Remote unlock signal sent to %d terminal(s). They will unlock within a few seconds.")
            % count,
        )


@admin.register(StoreGroup)
class StoreGroupAdmin(admin.ModelAdmin):
    """Admin for POS store groups (regional settings inheritance)."""

    change_list_template = "admin/pos_app/storegroup/change_list.html"
    change_form_template = "admin/pos_app/storegroup/change_form.html"
    list_display = ["name", "code", "store_count", "currency_display", "is_active", "sort_order"]
    list_filter = ["is_active"]
    search_fields = ["name", "code"]
    list_editable = ["sort_order", "is_active"]
    ordering = ["sort_order", "name"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        (
            None,
            {
                "fields": ("name", "code", "is_active", "sort_order"),
                "classes": ("tab-basic",),
            },
        ),
        (
            _("Regional Settings"),
            {
                "fields": ("currency", "language", "timezone"),
                "classes": ("tab-regional",),
                "description": _(
                    "Settings applied to all stores in this group. Blank = inherit from site default."
                ),
            },
        ),
        (
            _("Advanced"),
            {
                "fields": ("settings",),
                "classes": ("tab-advanced",),
                "description": _("Additional group-level settings as JSON."),
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
        css = {"all": ("pos_app/admin/css/storegroup_form.css",)}
        js = ("pos_app/admin/js/storegroup_form.js",)

    def store_count(self, obj):
        return obj.store_count

    store_count.short_description = _("Stores")

    def changelist_view(self, request, extra_context=None):
        """Add currencies to context for filter dropdown"""
        extra_context = extra_context or {}
        extra_context["currencies"] = (
            StoreGroup.objects.exclude(currency="")
            .values_list("currency", flat=True)
            .distinct()
            .order_by("currency")
        )
        return super().changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        return super().change_view(request, object_id, form_url, extra_context)

    def currency_display(self, obj):
        return obj.currency or _("(Site Default)")

    currency_display.short_description = _("Currency")


class POSTerminalReaderInline(admin.TabularInline):
    model = POSTerminalReader
    extra = 0
    readonly_fields = [
        "provider_reader_id",
        "reader_type",
        "serial_number",
        "status",
        "last_seen_at",
    ]
    fields = [
        "reader_label",
        "provider_reader_id",
        "reader_type",
        "terminal",
        "status",
        "last_seen_at",
    ]


@admin.register(POSTerminalProvider)
class POSTerminalProviderAdmin(admin.ModelAdmin):
    change_list_template = "admin/pos_app/posterminalprovider/change_list.html"
    list_display = [
        "display_name",
        "provider_key",
        "is_active",
        "connection_status",
        "last_tested_at",
    ]
    list_filter = ["is_active", "connection_status"]
    readonly_fields = [
        "id",
        "connection_status",
        "connection_error",
        "last_tested_at",
        "created_at",
        "updated_at",
    ]
    inlines = [POSTerminalReaderInline]

    fieldsets = (
        (
            None,
            {
                "fields": ("provider_key", "display_name", "is_active"),
            },
        ),
        (
            _("Component"),
            {
                "fields": ("component",),
                "description": _(
                    "Component package from upgrade server. Null for built-in manual provider."
                ),
            },
        ),
        (
            _("Credentials"),
            {
                "fields": ("credentials_encrypted",),
                "description": _(
                    "Encrypted API credentials. Use set_credentials() to update safely."
                ),
            },
        ),
        (
            _("Provider Settings"),
            {
                "fields": ("provider_settings",),
                "description": _("Non-secret provider config, e.g. Stripe location ID."),
            },
        ),
        (
            _("Connection Health"),
            {
                "fields": ("connection_status", "connection_error", "last_tested_at"),
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": ("id", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    actions = ["test_provider_connection"]

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        # Annotate queryset with reader_count for template
        qs = POSTerminalProvider.objects.annotate(reader_count=Count("readers", distinct=True))
        extra_context["annotated_providers"] = qs
        return super().changelist_view(request, extra_context=extra_context)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(reader_count=Count("readers", distinct=True))

    @admin.action(description=_("Test connection"))
    def test_provider_connection(self, request, queryset):
        for provider in queryset:
            success = provider.test_connection()
            status_text = _("connected") if success else _("error")
            self.message_user(
                request,
                _("%(name)s: %(status)s") % {"name": provider.display_name, "status": status_text},
            )


@admin.register(POSTerminalReader)
class POSTerminalReaderAdmin(admin.ModelAdmin):
    change_list_template = "admin/pos_app/posterminalreader/change_list.html"
    list_display = [
        "reader_label",
        "provider",
        "terminal",
        "reader_type",
        "status",
        "last_seen_at",
        "splash_status",
    ]
    list_filter = ["status", "provider"]
    search_fields = ["reader_label", "provider_reader_id", "serial_number"]
    readonly_fields = [
        "id",
        "created_at",
        "updated_at",
        "last_seen_at",
        "stripe_splash_file_id",
        "stripe_splash_config_id",
        "splash_generated_at",
    ]
    actions = ["regenerate_splash_screen"]

    fieldsets = (
        (
            None,
            {
                "fields": ("provider", "terminal", "reader_label"),
            },
        ),
        (
            _("Provider Details"),
            {
                "fields": ("provider_reader_id", "reader_type", "serial_number", "ip_address"),
            },
        ),
        (
            _("Status"),
            {
                "fields": ("status", "last_seen_at"),
            },
        ),
        (
            _("Splash Screen"),
            {
                "fields": (
                    "splash_override_image",
                    "splash_generated_at",
                    "stripe_splash_file_id",
                    "stripe_splash_config_id",
                ),
                "description": _(
                    "Custom splash screen for this reader. Leave blank to auto-generate from your site logo. "
                    "Splash screens are uploaded to Stripe when the reader is registered."
                ),
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": ("id", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if "splash_override_image" in form.base_fields:
            form.base_fields["splash_override_image"].widget = MediaLibrarySelectWidget()
        return form

    @admin.display(description=_("Splash"))
    def splash_status(self, obj):
        """Display splash screen status in list view."""
        from django.utils.html import format_html

        if obj.splash_generated_at:
            if obj.splash_override_image:
                return format_html(
                    '<span style="color: #28a745;" title="Custom splash uploaded">&#10003; Custom</span>'
                )
            return format_html(
                '<span style="color: #28a745;" title="Auto-generated splash uploaded">&#10003; Auto</span>'
            )
        return format_html(
            '<span style="color: #6c757d;" title="No splash screen configured">&mdash;</span>'
        )

    @admin.action(description=_("Regenerate splash screen"))
    def regenerate_splash_screen(self, request, queryset):
        """Admin action to regenerate splash screens for selected readers."""
        from django.contrib import messages

        from pos_app.tasks import update_reader_splash_screen

        count = 0
        for reader in queryset:
            if reader.provider and reader.provider.provider_key == "stripe_terminal":
                update_reader_splash_screen.delay(str(reader.pk))
                count += 1

        if count > 0:
            messages.success(
                request,
                _("Queued splash screen regeneration for %(count)d reader(s).") % {"count": count},
            )
        else:
            messages.warning(request, _("No Stripe Terminal readers selected."))

    def save_model(self, request, obj, form, change):
        """Trigger splash screen update when override image changes."""
        super().save_model(request, obj, form, change)

        # If splash_override_image was changed, trigger update
        if "splash_override_image" in form.changed_data:
            from pos_app.tasks import update_splash_screen_for_reader_override

            update_splash_screen_for_reader_override.delay(str(obj.pk))

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["has_providers"] = POSTerminalProvider.objects.filter(is_active=True).exists()
        extra_context["providers"] = POSTerminalProvider.objects.filter(is_active=True).order_by(
            "display_name"
        )
        extra_context["terminals"] = POSTerminal.objects.filter(is_active=True).order_by("name")
        return super().changelist_view(request, extra_context=extra_context)


class CashMovementInline(admin.TabularInline):
    model = CashMovement
    extra = 0
    readonly_fields = ["created_at"]
    fields = ["movement_type", "amount", "reason", "performed_by", "created_at"]


class POSPaymentInline(admin.TabularInline):
    model = POSPayment
    extra = 0
    readonly_fields = ["created_at"]
    fields = [
        "method",
        "amount",
        "amount_tendered",
        "change_given",
        "card_last_four",
        "card_reference",
        "card_brand",
        "provider_payment_id",
        "gift_card_code",
        "created_at",
    ]


@admin.register(POSShift)
class POSShiftAdmin(admin.ModelAdmin):
    change_list_template = "admin/pos_app/posshift/change_list.html"
    list_display = [
        "cashier",
        "terminal",
        "started_at",
        "ended_at",
        "total_sales",
        "total_transactions",
        "shift_status",
    ]
    list_filter = ["terminal", "started_at", "ended_at"]
    search_fields = ["cashier__username", "cashier__first_name", "cashier__last_name"]
    readonly_fields = [
        "started_at",
        "ended_at",
        "expected_cash",
        "cash_difference",
        "total_sales",
        "total_refunds",
        "total_transactions",
    ]
    inlines = [CashMovementInline, POSPaymentInline]

    fieldsets = (
        (None, {"fields": ("terminal", "cashier", "started_at", "ended_at")}),
        (
            _("Cash Reconciliation"),
            {
                "fields": ("opening_cash", "closing_cash", "expected_cash", "cash_difference"),
            },
        ),
        (
            _("Shift Totals"),
            {
                "fields": ("total_sales", "total_refunds", "total_transactions"),
            },
        ),
        (
            _("Notes"),
            {
                "fields": ("notes",),
                "classes": ("collapse",),
            },
        ),
    )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("terminal", "terminal__warehouse", "cashier")
        )

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["terminals"] = POSTerminal.objects.filter(is_active=True).order_by("name")
        extra_context["total_count"] = POSShift.objects.count()
        extra_context["open_count"] = POSShift.objects.filter(ended_at__isnull=True).count()
        extra_context["closed_count"] = POSShift.objects.filter(ended_at__isnull=False).count()
        return super().changelist_view(request, extra_context=extra_context)

    def shift_status(self, obj):
        if obj.is_open:
            return _("Open")
        if obj.cash_difference is not None and obj.cash_difference != 0:
            return _("Closed (%.2f difference)") % obj.cash_difference
        return _("Closed")

    shift_status.short_description = _("Status")


class ReceiptTemplateForm(admin.ModelAdmin):
    """Custom form to use MediaLibrarySelectWidget for logo field."""

    pass


@admin.register(ReceiptTemplate)
class ReceiptTemplateAdmin(admin.ModelAdmin):
    change_list_template = "admin/pos_app/receipttemplate/change_list.html"
    change_form_template = "admin/pos_app/receipttemplate/change_form.html"
    list_display = ["name", "scope_display", "paper_width", "qr_enabled", "updated_at"]
    list_filter = ["paper_width", "qr_enabled", "store_group"]
    search_fields = ["name"]

    fieldsets = (
        (
            None,
            {
                "fields": ("name", "paper_width"),
            },
        ),
        (
            _("Assignment"),
            {
                "fields": ("store_group", "warehouse"),
                "description": _(
                    "Leave both blank for the default template. "
                    "Select a group for all stores in that group. "
                    "Select a specific store to override group/default."
                ),
            },
        ),
        (
            _("Header & Logo"),
            {
                "fields": ("logo", "header_text"),
            },
        ),
        (
            _("Store Information"),
            {
                "fields": (
                    "show_store_address",
                    "custom_address",
                    "show_store_phone",
                    "custom_phone",
                    "show_store_email",
                    "custom_email",
                ),
            },
        ),
        (
            _("Business Details"),
            {
                "fields": ("tax_id_label", "tax_id_number", "business_registration"),
            },
        ),
        (
            _("Receipt Options"),
            {
                "fields": ("show_sku", "show_cashier", "show_terminal_name"),
            },
        ),
        (
            _("Footer"),
            {
                "fields": ("footer_text", "return_policy"),
            },
        ),
        (
            _("QR Code Promotion"),
            {
                "fields": ("qr_enabled", "qr_url", "qr_label"),
                "description": _(
                    "Add a QR code to the bottom of receipts for promotions like "
                    '"Scan for 10% off", "Leave a review", or "Visit our website".'
                ),
            },
        ),
        (
            _("Branding"),
            {
                "fields": ("show_powered_by",),
            },
        ),
    )

    class Media:
        css = {"all": ("pos_app/admin/css/receipt_preview.css",)}
        js = ("pos_app/admin/js/receipt_preview.js",)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["store_groups"] = StoreGroup.objects.filter(is_active=True).order_by(
            "sort_order", "name"
        )
        extra_context["warehouses"] = Warehouse.objects.filter(is_retail_location=True).order_by(
            "name"
        )
        extra_context["paper_widths"] = ReceiptTemplate.PAPER_WIDTHS
        return super().changelist_view(request, extra_context=extra_context)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "logo":
            kwargs["widget"] = MediaLibrarySelectWidget()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def scope_display(self, obj):
        return obj.get_scope_display()

    scope_display.short_description = _("Scope")


@admin.register(PromoSlide)
class PromoSlideAdmin(admin.ModelAdmin):
    """Admin for promotional slides shown on customer-facing POS displays."""

    change_list_template = "admin/pos_app/promoslide/change_list.html"
    list_display = ["title_display", "scope_display", "sort_order", "is_active", "updated_at"]
    list_filter = ["is_active", "store_group", "warehouse"]
    list_editable = ["sort_order", "is_active"]
    search_fields = ["title", "subtitle"]
    ordering = ["sort_order"]

    fieldsets = (
        (
            None,
            {
                "fields": ("is_active",),
            },
        ),
        (
            _("Assignment"),
            {
                "fields": ("store_group", "warehouse"),
                "description": _(
                    "Leave both blank for All Stores. "
                    "Select a group to show in all stores of that group. "
                    "Select a specific store to show only there."
                ),
            },
        ),
        (
            _("Content"),
            {
                "fields": ("image", "title", "subtitle"),
                "description": _(
                    "Create promotional slides for your customer-facing display. "
                    "Recommended image size: 1920x1080 or 16:9 aspect ratio."
                ),
            },
        ),
        (
            _("Display Order"),
            {
                "fields": ("sort_order",),
                "description": _("Lower numbers appear first in the slideshow."),
            },
        ),
    )

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["store_groups"] = StoreGroup.objects.filter(is_active=True).order_by(
            "sort_order", "name"
        )
        extra_context["warehouses"] = Warehouse.objects.filter(is_retail_location=True).order_by(
            "name"
        )
        return super().changelist_view(request, extra_context=extra_context)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "image":
            kwargs["widget"] = MediaLibrarySelectWidget()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def title_display(self, obj):
        return obj.title or _("Untitled Slide")

    title_display.short_description = _("Title")

    def scope_display(self, obj):
        return obj.get_scope_display()

    scope_display.short_description = _("Scope")


@admin.register(POSStaffDiscount)
class POSStaffDiscountAdmin(admin.ModelAdmin):
    """Admin for POS staff discount permissions and limits."""

    list_display = [
        "user",
        "max_discount_percentage",
        "max_discount_amount_display",
        "can_apply_item_discounts",
        "can_apply_cart_discounts",
        "requires_reason",
        "is_manager",
    ]
    list_filter = [
        "is_manager",
        "requires_reason",
        "can_apply_item_discounts",
        "can_apply_cart_discounts",
    ]
    search_fields = ["user__username", "user__first_name", "user__last_name", "user__email"]
    autocomplete_fields = ["user"]
    ordering = ["-is_manager", "user__username"]

    fieldsets = (
        (
            None,
            {
                "fields": ("user",),
            },
        ),
        (
            _("Discount Limits"),
            {
                "fields": ("max_discount_percentage", "max_discount_amount"),
                "description": _(
                    "Set the maximum discount this staff member can apply. "
                    "Percentage limit applies to both % and fixed discounts relative to line/cart total."
                ),
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "can_apply_item_discounts",
                    "can_apply_cart_discounts",
                    "requires_reason",
                ),
            },
        ),
        (
            _("Manager Approval"),
            {
                "fields": ("is_manager", "manager_pin"),
                "description": _(
                    "Managers can approve discounts that exceed other staff members' limits. "
                    "The PIN is used for quick approval at the terminal."
                ),
            },
        ),
        (
            _("Terminal Lock"),
            {
                "fields": ("cashier_pin",),
                "description": _(
                    "Personal PIN for unlocking the terminal after locking. 4-6 digits recommended."
                ),
            },
        ),
    )

    def max_discount_amount_display(self, obj):
        if obj.max_discount_amount:
            return f"{obj.max_discount_amount}"
        return _("No limit")

    max_discount_amount_display.short_description = _("Max Amount")

    def get_form(self, request, obj=None, **kwargs):
        from django.forms import PasswordInput

        form = super().get_form(request, obj, **kwargs)
        for field_name in ("manager_pin", "cashier_pin"):
            if field_name in form.base_fields:
                form.base_fields[field_name].widget = PasswordInput(
                    attrs={"autocomplete": "off", "placeholder": "****"}
                )
        return form

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = db_field.related_model.objects.filter(is_staff=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(TerminalLockEvent)
class TerminalLockEventAdmin(admin.ModelAdmin):
    """Admin for terminal lock/unlock audit events (read-only)."""

    list_display = [
        "created_at",
        "terminal",
        "event_type",
        "performed_by",
        "locked_by",
        "manager_override",
        "cart_summary",
    ]
    list_filter = ["event_type", "manager_override", "terminal", "created_at"]
    search_fields = [
        "terminal__name",
        "performed_by__username",
        "performed_by__email",
        "locked_by__username",
        "locked_by__email",
    ]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    readonly_fields = [
        "terminal",
        "shift",
        "event_type",
        "performed_by",
        "locked_by",
        "manager_override",
        "failed_attempt_count",
        "cart_item_count",
        "cart_total",
        "ip_address",
        "created_at",
    ]

    fieldsets = (
        (
            None,
            {
                "fields": ("terminal", "shift", "event_type", "created_at"),
            },
        ),
        (
            _("Users"),
            {
                "fields": ("locked_by", "performed_by", "manager_override"),
            },
        ),
        (
            _("Security"),
            {
                "fields": ("failed_attempt_count", "ip_address"),
            },
        ),
        (
            _("Cart State"),
            {
                "fields": ("cart_item_count", "cart_total"),
            },
        ),
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def cart_summary(self, obj):
        if obj.cart_item_count:
            if obj.cart_total:
                return f"{obj.cart_item_count} items ({obj.cart_total})"
            return f"{obj.cart_item_count} items"
        return "-"

    cart_summary.short_description = _("Cart")
