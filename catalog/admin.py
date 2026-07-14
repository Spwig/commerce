import logging

from django import forms
from django.contrib import admin
from django.contrib.admin.options import IS_POPUP_VAR
from django.contrib.admin.widgets import AutocompleteSelect
from django.db import models
from django.db.models import Count, Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)
import json
from datetime import UTC

from django_ckeditor_5.widgets import CKEditor5Widget
from modeltranslation.admin import TranslationAdmin

from core.admin_mixins import MoneyFieldCurrencyMixin, TranslatableAdminMixin
from core.widgets import IconPickerWidget, KeyValueWidget, TranslatableFieldWidget
from custom_fields.mixins import CustomFieldsAdminMixin
from media_library.widgets import MediaLibrarySelectWidget
from seo_generator.admin_mixin import SEOGeneratorAdminMixin

from .forms import CommaSeparatedDecimalField, ProductVariantForm
from .models import (
    AttributeValue,
    Booking,
    BookingAvailabilityRule,
    BookingConfig,
    BookingPersonType,
    BookingRecurrenceRule,
    BookingResource,
    BookingWaitlist,
    Brand,
    BundleItem,
    Category,
    Collection,
    CompatibilityRule,
    ConfigurationPreset,
    ConfigurationSlot,
    ConfigurationSlotOption,
    CustomizationOption,
    DigitalAsset,
    DigitalDownload,
    ExternalLicenseSync,
    GiftCard,
    GiftCardTransaction,
    LicenseKey,
    LicenseKeyTemplate,
    LicensePool,
    LicenseProvider,
    PriceCharmingRule,
    Product,
    ProductAttribute,
    ProductAttributeAssignment,
    ProductDependency,
    ProductImage,
    ProductPrice,
    ProductRegionVisibility,
    ProductReview,
    ProductTag,
    ProductVariant,
    ProductVariantImage,
    Promotion,
    SalesRegion,
    StockDisplaySettings,
    StockItem,
    StockMovement,
    StockNotification,
    Warehouse,
    WebhookSubscription,
)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    template = "admin/edit_inline/tabular.html"  # Explicitly set Django's default


class DigitalAssetInline(admin.StackedInline):
    """Enhanced inline for managing digital product assets with file upload"""

    model = DigitalAsset
    extra = 0
    # Must match template check: inline_admin_formset.opts.verbose_name == 'digital asset'
    verbose_name = "digital asset"
    verbose_name_plural = "digital assets"
    fields = [
        "file",
        "filename",
        "version",
        "file_metadata",
        "requires_license",
        "license_key_preview",
        "download_limit",
        "expiration_days",
        "is_active",
    ]
    readonly_fields = ["file_metadata", "license_key_preview"]
    template = "admin/edit_inline/stacked.html"  # Explicitly set Django's default

    class Media:
        css = {"all": ("catalog/css/admin_digital_asset.css",)}
        js = ("catalog/js/admin_digital_asset.js",)

    def file_metadata(self, obj):
        """Display file metadata (size, type, upload date)"""
        from django.utils.formats import date_format
        from django.utils.html import format_html

        if obj.pk and obj.file:
            # File size with proper formatting
            size_display = (
                obj.get_file_size_display()
                if hasattr(obj, "get_file_size_display")
                else f"{obj.file_size / (1024 * 1024):.2f} MB"
            )

            # File type
            file_type = obj.file_type or _("Unknown")

            # Upload date
            upload_date = (
                date_format(obj.created_at, "SHORT_DATETIME_FORMAT")
                if hasattr(obj, "created_at")
                else _("N/A")
            )

            return format_html(
                '<div class="digital-asset-metadata">'
                '<div class="metadata-row">'
                '<span class="metadata-label">📦 {}</span>'
                '<span class="metadata-value">{}</span>'
                "</div>"
                '<div class="metadata-row">'
                '<span class="metadata-label">📄 {}</span>'
                '<span class="metadata-value">{}</span>'
                "</div>"
                '<div class="metadata-row">'
                '<span class="metadata-label">📅 {}</span>'
                '<span class="metadata-value">{}</span>'
                "</div>"
                "</div>",
                _("Size"),
                size_display,
                _("Type"),
                file_type,
                _("Uploaded"),
                upload_date,
            )
        return format_html('<em style="color: #999;">{}</em>', _("No file uploaded yet"))

    file_metadata.short_description = _("File Information")

    def license_key_preview(self, obj):
        """Display license key generation status and count"""
        if obj.pk:
            from django.utils.html import format_html

            if obj.requires_license:
                # Count generated license keys
                license_count = LicenseKey.objects.filter(digital_asset=obj).count()

                if license_count > 0:
                    return format_html(
                        '<div class="license-status license-active">'
                        '<span class="status-icon">🔑</span>'
                        '<span class="status-text">{} {}</span>'
                        "</div>",
                        license_count,
                        _("license key(s) generated"),
                    )
                else:
                    return format_html(
                        '<div class="license-status license-pending">'
                        '<span class="status-icon">⏳</span>'
                        '<span class="status-text">{}</span>'
                        "</div>",
                        _("License keys will be generated on order completion"),
                    )
            else:
                return format_html(
                    '<div class="license-status license-disabled">'
                    '<span class="status-icon">🔓</span>'
                    '<span class="status-text">{}</span>'
                    "</div>",
                    _("License key not required for this asset"),
                )
        return "-"

    license_key_preview.short_description = _("License Key Status")


class ProductVariantInline(admin.StackedInline):
    """Enhanced inline for managing product variants with comprehensive editing"""

    model = ProductVariant
    form = ProductVariantForm  # Use custom form with context-aware filtering
    extra = 0
    template = "admin/catalog/edit_inline/variant_stacked.html"
    fields = [
        "name",
        "sku",
        "is_active",
        "selected_attributes",
        "pricing_strategy",
        "price",
        "weight",
        "length",
        "width",
        "height",
        "barcode",
        "preferred_shipping_package",
    ]
    readonly_fields = ["attributes_display", "effective_price", "stock_summary"]
    filter_horizontal = [
        "selected_attributes"
    ]  # Use filter_horizontal to respect queryset filtering
    ordering = ["name"]

    class Media:
        css = {"all": ["catalog/css/hide_selected_attributes_add.css"]}

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """Filter selected_attributes to show only values for attributes assigned to this product."""
        if db_field.name == "selected_attributes":
            # Get the product being edited
            product = None
            if request.resolver_match.kwargs.get("object_id"):
                from .models import Product

                try:
                    product = Product.objects.get(pk=request.resolver_match.kwargs["object_id"])
                except Product.DoesNotExist:
                    pass

            if product:
                # Get attributes assigned to this product
                assigned_attrs = ProductAttributeAssignment.objects.filter(
                    product=product
                ).values_list("attribute_id", flat=True)

                if assigned_attrs:
                    # Filter to only show values for assigned attributes
                    kwargs["queryset"] = (
                        AttributeValue.objects.filter(attribute_id__in=assigned_attrs)
                        .select_related("attribute")
                        .order_by("attribute__name", "sort_order")
                    )
                else:
                    # No attributes assigned yet
                    kwargs["queryset"] = AttributeValue.objects.none()

        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def attributes_display(self, obj):
        """Display variant attributes in readable format"""
        if obj.pk:
            attr_dict = obj.get_attribute_dict()
            if attr_dict:
                items = [f"{k}: {v}" for k, v in attr_dict.items()]
                return " • ".join(items)
            return _("No attributes")
        return "-"

    attributes_display.short_description = _("Attributes")

    def effective_price(self, obj):
        """Display the effective price considering pricing strategy"""
        if obj.pk:
            from django.utils.html import format_html

            price = obj.get_effective_price()
            if obj.pricing_strategy == "inherit":
                return format_html(
                    '<span title="Inherited from product">{} (inherited)</span>', price
                )
            return str(price)
        return "-"

    effective_price.short_description = _("Effective Price")

    def stock_summary(self, obj):
        """Display stock summary across all warehouses"""
        if obj.pk:
            from django.db.models import Sum
            from django.utils.html import format_html

            total = obj.get_stock_quantity()

            # Get per-warehouse breakdown
            stock_items = (
                StockItem.objects.filter(product=obj.product, variant=obj)
                .select_related("warehouse")
                .values("warehouse__name", "warehouse__code")
                .annotate(quantity=Sum("on_hand"))
                .order_by("warehouse__name")
            )

            if not stock_items:
                return format_html('<em style="color: #999;">{}</em>', _("No stock records"))

            # Build summary with warehouse breakdown
            breakdown = []
            for item in stock_items:
                warehouse_code = item["warehouse__code"]
                qty = item["quantity"] or 0
                breakdown.append(f"{warehouse_code}: {qty}")

            summary = f"<strong>Total: {total}</strong>"
            if breakdown:
                summary += f'<br><small style="color: #666;">{" | ".join(breakdown)}</small>'

            return format_html(summary)
        return "-"

    stock_summary.short_description = _("Stock")

    def get_fields(self, request, obj=None):
        """Hide pricing_strategy field when multi-currency is disabled"""
        from core.models import SiteSettings

        fields = list(super().get_fields(request, obj))
        settings = SiteSettings.get_settings()

        # If multi-currency is disabled, remove pricing_strategy from fields
        if not settings.enable_multi_currency and "pricing_strategy" in fields:
            fields.remove("pricing_strategy")

        return fields

    def get_formset(self, request, obj=None, **kwargs):
        """Customize formset to filter currency choices for MoneyField"""
        formset = super().get_formset(request, obj, **kwargs)
        from core.admin_mixins import _apply_money_field_currency_defaults

        _apply_money_field_currency_defaults(formset.form, obj)
        return formset

    class Media:
        css = {"all": ("catalog/css/admin_variant_inline.css",)}
        js = (
            # media_manager.js is loaded by change_form.html template
            "catalog/js/admin_variant_inline.js",
        )


class ProductPriceForm(forms.ModelForm):
    """Custom form for ProductPrice to handle price fields without currency dropdowns"""

    # Override price and sale_price as DecimalFields (amounts only, no currency)
    price_amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0,
        label=_("Price"),
        widget=forms.NumberInput(attrs={"step": "0.01", "min": "0", "class": "vDecimalField"}),
    )

    sale_price_amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0,
        required=False,
        label=_("Sale Price"),
        widget=forms.NumberInput(attrs={"step": "0.01", "min": "0", "class": "vDecimalField"}),
    )

    class Meta:
        model = ProductPrice
        fields = ["currency", "is_active"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Populate price_amount and sale_price_amount from MoneyFields
        if self.instance and self.instance.pk:
            if self.instance.price:
                self.fields["price_amount"].initial = self.instance.price.amount
            if self.instance.sale_price:
                self.fields["sale_price_amount"].initial = self.instance.sale_price.amount

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Convert decimal amounts to Money objects with the selected currency
        from djmoney.money import Money

        price_amount = self.cleaned_data.get("price_amount")
        sale_price_amount = self.cleaned_data.get("sale_price_amount")
        currency = self.cleaned_data.get("currency")

        if price_amount is not None:
            instance.price = Money(price_amount, currency)

        if sale_price_amount:
            instance.sale_price = Money(sale_price_amount, currency)
        else:
            instance.sale_price = None

        if commit:
            instance.save()

        return instance


class ProductPriceInline(admin.TabularInline):
    """Inline for managing multi-currency fixed prices"""

    model = ProductPrice
    form = ProductPriceForm
    extra = 0
    fields = ["currency", "price_amount", "sale_price_amount", "is_active"]
    template = "admin/edit_inline/tabular.html"  # Explicitly set Django's default
    verbose_name = _("Currency-Specific Price")
    verbose_name_plural = _("Multi-Currency Pricing (Fixed Strategy)")

    def get_formset(self, request, obj=None, **kwargs):
        """Customize formset for multi-currency pricing"""
        from core.utils.currency_helpers import get_enabled_currencies

        formset = super().get_formset(request, obj, **kwargs)

        # Get enabled currencies (respects multi-currency settings and active currencies)
        choices = get_enabled_currencies()

        # Update currency field widget with choices
        if hasattr(formset.form, "base_fields") and "currency" in formset.form.base_fields:
            formset.form.base_fields["currency"].widget = forms.Select(choices=choices)

        return formset


class StockItemInline(admin.TabularInline):
    """Inline for managing stock at different warehouses"""

    model = StockItem
    extra = 0
    # Must match template check: inline_admin_formset.opts.verbose_name == 'stock item'
    verbose_name = "stock item"
    verbose_name_plural = "stock items"
    fields = ["warehouse", "on_hand", "allocated", "available", "low_stock_threshold"]
    readonly_fields = ["available"]
    template = "admin/edit_inline/tabular.html"  # Explicitly set Django's default

    def available(self, obj):
        """Show calculated available stock"""
        if obj.pk:
            return obj.available
        return 0

    available.short_description = _("Available")


class ProductRegionVisibilityInline(admin.TabularInline):
    """Inline for managing product visibility per region"""

    model = ProductRegionVisibility
    extra = 0
    fields = ["region", "is_visible"]
    template = "admin/catalog/edit_inline/simple_tabular.html"

    class Media:
        css = {"all": ("catalog/css/admin_region_visibility.css",)}
        js = ("catalog/js/admin_region_visibility.js",)


class BundleComponentAutocomplete(AutocompleteSelect):
    """Custom autocomplete widget pointing to our filtered endpoint."""

    def get_url(self):
        return reverse("catalog_admin:autocomplete_component_products")


class BundleItemForm(forms.ModelForm):
    """Custom form that dynamically sets the component_variant queryset."""

    class Meta:
        model = BundleItem
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        product_id = None
        # Existing item: use instance's product
        if self.instance.pk and self.instance.component_product_id:
            product_id = self.instance.component_product_id
        # Form submission: read product from POST data
        elif self.data and self.prefix:
            product_id = self.data.get(f"{self.prefix}-component_product")

        if product_id:
            self.fields["component_variant"].queryset = ProductVariant.objects.filter(
                product_id=product_id
            )
        else:
            self.fields["component_variant"].queryset = ProductVariant.objects.none()


class BundleItemInline(admin.StackedInline):
    """Inline for managing bundle components - card-based layout"""

    model = BundleItem
    form = BundleItemForm
    fk_name = "bundle"  # Required: BundleItem has two FKs to Product (bundle, component_product)
    extra = 1
    verbose_name = _("bundle item")
    verbose_name_plural = _("bundle items")
    fields = [
        "component_product",
        "allow_variant_selection",
        "component_variant",
        "quantity",
        "sort_order",
        "is_optional",
    ]
    ordering = ["sort_order", "id"]
    template = "admin/catalog/edit_inline/bundle_stacked.html"

    class Media:
        css = {"all": ("catalog/css/admin_bundle.css",)}
        js = ("catalog/js/admin_bundle_inline.js",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Filter component_product to exclude unbundleable product types."""
        if db_field.name == "component_product":
            kwargs["queryset"] = Product.objects.exclude(
                product_type__in=["bundle", "configurable", "gift_card"]
            )
            kwargs["widget"] = BundleComponentAutocomplete(
                db_field.remote_field,
                self.admin_site,
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ProductDependencyInline(admin.TabularInline):
    """Inline for managing product dependencies (requires/recommends)"""

    model = ProductDependency
    fk_name = "product"  # Required: two FKs to Product
    extra = 1
    verbose_name = "product dependency"
    verbose_name_plural = "product dependencies"
    fields = ["required_product", "dependency_type", "customer_message", "sort_order"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "required_product":
            obj_id = request.resolver_match.kwargs.get("object_id")
            qs = Product.objects.filter(status="published").exclude(is_deleted=True)
            if obj_id:
                qs = qs.exclude(pk=obj_id)
            kwargs["queryset"] = qs
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class CustomizationOptionInline(admin.TabularInline):
    """Inline for managing product customization options"""

    model = CustomizationOption
    extra = 0
    # Must match template check: inline_admin_formset.opts.verbose_name == 'customization option'
    verbose_name = "customization option"
    verbose_name_plural = "customization options"
    fields = [
        "name",
        "option_type",
        "is_required",
        "sort_order",
        "pricing_type",
        "price_amount",
        "max_length",
        "min_value",
        "max_value",
        "choices_display",
    ]
    readonly_fields = ["choices_display"]
    ordering = ["sort_order", "name"]
    template = "admin/edit_inline/tabular.html"  # Explicitly set Django's default

    class Media:
        css = {"all": ("catalog/css/admin_customization.css",)}
        js = ("catalog/js/admin_customization.js",)

    def choices_display(self, obj):
        """Display choices in a readable format for select/color options"""
        if obj.pk and obj.option_type in ("select", "color") and obj.choices:
            from django.utils.safestring import mark_safe

            choice_html = '<div class="customization-choices">'
            for choice in obj.choices:
                value = choice.get("value", "")
                label = choice.get("label", value)
                modifier = choice.get("price_modifier")

                modifier_text = f" (+${modifier})" if modifier else ""
                choice_html += f'<div class="choice-item"><strong>{label}</strong> [{value}]{modifier_text}</div>'

            choice_html += "</div>"
            return mark_safe(choice_html)
        return "-"

    choices_display.short_description = _("Choices")


class ConfigurationSlotInline(admin.StackedInline):
    """Inline for managing configuration slots on configurable products"""

    model = ConfigurationSlot
    extra = 0
    verbose_name = _("configuration slot")
    verbose_name_plural = _("configuration slots")
    fields = [
        "name",
        "slug",
        "description",
        "icon",
        "is_required",
        "min_selections",
        "max_selections",
        "sort_order",
    ]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["sort_order", "name"]

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == "icon":
            from django import forms

            return forms.CharField(
                widget=IconPickerWidget(
                    priority_icons=[
                        "fa-microchip",
                        "fa-gear",
                        "fa-sliders",
                        "fa-puzzle-piece",
                        "fa-wrench",
                        "fa-cube",
                        "fa-palette",
                        "fa-memory",
                    ],
                    style_prefix=True,
                ),
                required=False,
            )
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("options")


class ConfigurationPresetInline(admin.TabularInline):
    """Inline for managing configuration presets (e.g., Budget Build, Pro Build)"""

    model = ConfigurationPreset
    extra = 0
    verbose_name = _("configuration preset")
    verbose_name_plural = _("configuration presets")
    fields = [
        "name",
        "slug",
        "description",
        "is_featured",
        "sort_order",
    ]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["sort_order", "name"]

    class Media:
        css = {"all": ("catalog/css/admin_customization.css",)}
        js = ("catalog/js/admin_customization.js",)


class BookingConfigInline(admin.StackedInline):
    """Inline for booking product configuration (OneToOne with Product)"""

    model = BookingConfig
    extra = 0
    max_num = 1
    verbose_name = _("booking configuration")
    verbose_name_plural = _("booking configuration")
    fieldsets = (
        (
            _("Booking Type & Duration"),
            {
                "fields": (
                    "booking_type",
                    "duration_type",
                    "duration",
                    "duration_unit",
                    "min_duration",
                    "max_duration",
                ),
            },
        ),
        (
            _("Scheduling"),
            {
                "fields": (
                    "buffer_before",
                    "buffer_after",
                    "min_advance",
                    "min_advance_unit",
                    "max_advance",
                    "max_advance_unit",
                    "max_bookings_per_slot",
                ),
            },
        ),
        (
            _("Confirmation & Cancellation"),
            {
                "fields": (
                    "confirmation_required",
                    "cancellation_allowed",
                    "cancellation_deadline",
                    "cancellation_deadline_unit",
                ),
            },
        ),
        (
            _("Display & UX"),
            {
                "fields": (
                    "calendar_display",
                    "customer_timezone_enabled",
                ),
            },
        ),
        (
            _("Deposits"),
            {
                "fields": (
                    "deposit_enabled",
                    "deposit_type",
                    "deposit_amount",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Accommodation"),
            {
                "fields": (
                    "check_in_time",
                    "check_out_time",
                ),
                "classes": ("collapse",),
                "description": _('Only applies when booking type is "Accommodation"'),
            },
        ),
        (
            _("Recurring Bookings"),
            {
                "fields": ("recurrence_enabled",),
                "classes": ("collapse",),
            },
        ),
        (
            _("Reminders"),
            {
                "fields": (
                    "reminder_enabled",
                    "reminder_hours_before",
                ),
                "classes": ("collapse",),
            },
        ),
    )


class BookingResourceInline(admin.TabularInline):
    """Inline for managing booking resources (staff, rooms, equipment)"""

    model = BookingResource
    extra = 0
    verbose_name = _("booking resource")
    verbose_name_plural = _("booking resources")
    fields = [
        "name",
        "resource_type",
        "quantity",
        "assignment_type",
        "base_cost_adjustment",
        "email",
        "is_active",
        "sort_order",
    ]
    ordering = ["sort_order", "name"]


class BookingPersonTypeInline(admin.TabularInline):
    """Inline for person types (Adult, Child, Senior, etc.)"""

    model = BookingPersonType
    extra = 0
    verbose_name = _("person type")
    verbose_name_plural = _("person types")
    fields = [
        "name",
        "cost_adjustment",
        "min_persons",
        "max_persons",
        "is_counted_for_capacity",
        "sort_order",
    ]
    ordering = ["sort_order", "name"]


class BookingAvailabilityRuleInline(admin.TabularInline):
    """Inline for availability and pricing rules"""

    model = BookingAvailabilityRule
    extra = 0
    verbose_name = _("availability rule")
    verbose_name_plural = _("availability rules")
    fields = [
        "rule_type",
        "scope",
        "start_date",
        "end_date",
        "start_time",
        "end_time",
        "days_of_week",
        "cost_override",
        "cost_adjustment",
        "priority",
    ]
    ordering = ["-priority", "start_date"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Limit resource choices to those belonging to the parent product."""
        if db_field.name == "resource":
            parent_id = request.resolver_match.kwargs.get("object_id")
            if parent_id:
                kwargs["queryset"] = BookingResource.objects.filter(product_id=parent_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class BookingRecurrenceRuleInline(admin.TabularInline):
    """Inline for recurring schedule rules"""

    model = BookingRecurrenceRule
    extra = 0
    verbose_name = _("recurrence rule")
    verbose_name_plural = _("recurrence rules")
    fields = [
        "frequency",
        "day_of_week",
        "day_of_month",
        "start_time",
        "end_time",
        "start_date",
        "end_date",
        "auto_create_days_ahead",
        "is_active",
    ]


class AttributeValueInline(admin.TabularInline):
    """Inline for managing attribute values"""

    model = AttributeValue
    extra = 1
    fields = ["value", "slug", "color_hex", "sort_order"]
    prepopulated_fields = {"slug": ("value",)}
    ordering = ["sort_order", "value"]

    class Media:
        css = {"all": ("catalog/css/admin_attribute.css",)}


class ProductAttributeAssignmentInline(admin.TabularInline):
    """Inline for assigning attributes to products"""

    model = ProductAttributeAssignment
    extra = 0
    fields = ["attribute", "allowed_values", "sort_order"]
    autocomplete_fields = ["attribute"]
    filter_horizontal = ["allowed_values"]
    ordering = ["sort_order"]
    verbose_name = _("Product Attribute")
    verbose_name_plural = _("Product Attributes & Variations")
    template = "admin/catalog/edit_inline/tabular_with_quick_add.html"

    # Note: Media (CSS/JS) is loaded in ProductAdmin.Media to ensure it loads
    # even when the Variations tab is hidden (e.g., when product_type != 'variable')


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    """Admin for managing attribute values (for use with autocomplete in variants)"""

    list_display = ["value", "attribute", "color_hex", "sort_order"]
    list_filter = ["attribute"]
    search_fields = ["value", "attribute__name"]  # Enables autocomplete
    prepopulated_fields = {"slug": ("value",)}
    autocomplete_fields = ["attribute"]
    ordering = ["attribute__name", "sort_order", "value"]

    fieldsets = (
        (_("Basic Information"), {"fields": ("attribute", "value", "slug")}),
        (_("Display Options"), {"fields": ("color_hex", "sort_order")}),
    )

    def get_form(self, request, obj=None, **kwargs):
        """Customize form to prevent cascading popups"""
        form = super().get_form(request, obj, **kwargs)

        if obj:
            # Editing existing - make attribute field read-only to prevent changes
            form.base_fields["attribute"].disabled = True
            form.base_fields["attribute"].help_text = _(
                "Attribute cannot be changed after creation. To change it, create a new value."
            )
        else:
            # Creating new - disable add/change/delete buttons to prevent cascading popups
            form.base_fields["attribute"].widget.can_add_related = False
            form.base_fields["attribute"].widget.can_change_related = False
            form.base_fields["attribute"].widget.can_delete_related = False
            form.base_fields["attribute"].help_text = _(
                "Select an attribute. To create new attributes, go to Product Attributes admin."
            )

        return form

    class Media:
        css = {
            "all": (
                "utilities/base/current/utility_base.css",
                "utilities/color_picker/current/color_picker.css",
            )
        }
        js = (
            "utilities/color_picker/current/color_picker.js",
            "catalog/js/admin_attribute_value.js",
        )


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    """Admin for managing product attributes (Size, Color, Material, etc.)"""

    change_form_template = "admin/catalog/productattribute/change_form.html"
    list_display = ["name", "type", "is_required", "value_count", "sort_order"]
    list_filter = ["type", "is_required"]
    search_fields = ["name", "slug"]  # Enables autocomplete
    prepopulated_fields = {"slug": ("name",)}
    inlines = [AttributeValueInline]
    ordering = ["sort_order", "name"]

    fieldsets = (
        (_("Basic Information"), {"fields": ("name", "slug", "type", "is_required", "sort_order")}),
        (
            _("Translations"),
            {
                "fields": ("translations",),
            },
        ),
    )

    def value_count(self, obj):
        """Display count of values for this attribute"""
        return obj.values.count()

    value_count.short_description = _("Values")

    class Media:
        css = {
            "all": (
                "catalog/css/admin_attribute.css",
                "catalog/css/productattribute_change_form.css",
            )
        }
        js = ("catalog/js/productattribute_change_form.js",)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        if object_id:
            try:
                obj = self.get_object(request, object_id)
                if obj:
                    extra_context["value_count"] = obj.values.count()
            except Exception:
                extra_context["value_count"] = 0
        return super().change_view(request, object_id, form_url, extra_context)


class CategoryForm(forms.ModelForm):
    """
    Custom form for Category admin with translatable field widgets and media library integration.
    Uses JSON-based translation system per rules_llm.md guidelines.
    """

    class Meta:
        model = Category
        fields = "__all__"
        widgets = {
            # Translatable fields with globe icon for multi-language editing
            "name": TranslatableFieldWidget(
                base_widget=forms.TextInput(attrs={"class": "vTextField", "style": "width: 100%;"})
            ),
            "description": TranslatableFieldWidget(
                base_widget=forms.Textarea(attrs={"rows": 4, "style": "width: 100%;"})
            ),
            "meta_title": TranslatableFieldWidget(
                base_widget=forms.TextInput(attrs={"class": "vTextField", "style": "width: 100%;"})
            ),
            "meta_description": TranslatableFieldWidget(
                base_widget=forms.Textarea(attrs={"rows": 3, "style": "width: 100%;"})
            ),
            # Media library widgets for image selection
            "image_asset": MediaLibrarySelectWidget(selection_mode="single"),
            "banner_asset": MediaLibrarySelectWidget(selection_mode="single"),
            # Font Awesome icon selector
            "icon": IconPickerWidget(
                priority_icons=[
                    "fa-bag-shopping",
                    "fa-store",
                    "fa-tag",
                    "fa-folder",
                    "fa-shirt",
                    "fa-laptop",
                    "fa-house",
                    "fa-utensils",
                    "fa-heart",
                    "fa-star",
                ],
                style_prefix=True,
            ),
        }


@admin.register(Category)
class CategoryAdmin(
    CustomFieldsAdminMixin, SEOGeneratorAdminMixin, TranslatableAdminMixin, admin.ModelAdmin
):
    """
    Category admin with JSON-based translation system and enhanced media selection.
    """

    form = CategoryForm
    change_list_template = "admin/catalog/category/change_list.html"
    change_form_template = "admin/catalog/category/change_form.html"

    # Fields that support translation via the translation editor
    translatable_fields = ["name", "description", "meta_title", "meta_description"]

    list_display = ["name", "parent", "page_template", "is_active", "is_featured"]
    list_filter = ["is_active", "is_featured", "page_template"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}

    # Parent category autocomplete (image fields now use MediaLibrarySelectWidget)
    autocomplete_fields = ["parent"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Configure auto-save for media asset fields so selections persist immediately."""
        if db_field.name in ("image_asset", "banner_asset"):
            object_id = request.resolver_match.kwargs.get("object_id", "")
            return forms.ModelChoiceField(
                queryset=db_field.remote_field.model.objects.all(),
                widget=MediaLibrarySelectWidget(
                    attrs={
                        "auto_save_url": "/api/media/auto-save/",
                        "auto_save_app": "catalog",
                        "auto_save_model": "category",
                        "auto_save_pk": object_id,
                        "auto_save_field": db_field.name,
                    }
                ),
                required=False,
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    fieldsets = (
        (
            _("Basic Information"),
            {
                "fields": ("name", "slug", "parent", "description"),
                "description": _(
                    "Click the globe icon to translate name and description into other languages."
                ),
            },
        ),
        (
            _("Media"),
            {
                "fields": ("image_asset", "banner_asset", "icon"),
                "description": _(
                    "Select images from your media library or choose an icon for this category."
                ),
            },
        ),
        (
            _("Display Options"),
            {"fields": ("page_template", "products_per_page", "show_subcategories")},
        ),
        (
            _("Design & Theme"),
            {
                "fields": (
                    "template_variant",
                    "css_classes",
                    "layout_config",
                    "style_overrides",
                    "cascade_theme_to_children",
                    "cascade_theme_to_products",
                    "inherit_parent_theme",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("SEO"),
            {
                "fields": ("meta_title", "meta_description", "seo_auto_generated"),
                "description": _(
                    'Click the globe icon to translate SEO fields. Use "Regenerate SEO" to auto-generate.'
                ),
            },
        ),
        (_("Status"), {"fields": ("is_active", "is_featured", "sort_order")}),
    )

    class Media:
        js = TranslatableAdminMixin.Media.js + SEOGeneratorAdminMixin.Media.js
        css = {
            "all": list(TranslatableAdminMixin.Media.css.get("all", []))
            + list(SEOGeneratorAdminMixin.Media.css.get("all", []))
        }

    def get_form(self, request, obj=None, **kwargs):
        """In popup mode, limit to basic fields so hidden fields don't cause validation errors."""
        if IS_POPUP_VAR in request.GET:
            kwargs["fields"] = ["name", "slug", "parent", "description"]
        return super().get_form(request, obj, **kwargs)

    def changelist_view(self, request, extra_context=None):
        """Add custom context data for the category list view"""
        extra_context = extra_context or {}

        # Get all parent categories (categories that have no parent or have children)
        # for the parent filter dropdown
        extra_context["parent_categories"] = Category.objects.filter(parent__isnull=True).order_by(
            "name"
        )

        return super().changelist_view(request, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        """Handle translations data from custom form"""
        # Check if translations_data was submitted (from translation editor)
        translations_data = request.POST.get("translations_data")
        if translations_data:
            try:
                translations = json.loads(translations_data)
                obj.translations = translations
            except json.JSONDecodeError:
                pass  # Keep existing translations if JSON is invalid
        super().save_model(request, obj, form, change)


@admin.register(Brand)
class BrandAdmin(SEOGeneratorAdminMixin, TranslationAdmin):
    change_form_template = "admin/catalog/brand/change_form.html"
    list_display = ["name", "is_active", "is_featured"]
    list_filter = ["is_active", "is_featured"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (
        (_("Basic Information"), {"fields": ("name", "slug", "description", "website")}),
        (_("Brand Assets"), {"fields": ("logo", "banner_image", "brand_story")}),
        (_("SEO"), {"fields": ("meta_title", "meta_description", "seo_auto_generated")}),
        (_("Status"), {"fields": ("is_active", "is_featured", "show_brand_page")}),
    )

    class Media:
        css = {"all": ("catalog/css/brand_change_form.css",)}

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        obj = self.get_object(request, object_id)
        if obj:
            from catalog.models import Product

            extra_context["product_count"] = Product.objects.filter(brand=obj).count()
        return super().change_view(request, object_id, form_url, extra_context=extra_context)


class ProductForm(forms.ModelForm):
    """
    Custom form for Product admin with translatable field widgets.
    Wraps translatable fields with TranslatableFieldWidget to enable inline translation.
    """

    # Custom field for gift card denominations - accepts comma-separated values
    gift_card_denominations = CommaSeparatedDecimalField(
        label=_("Fixed Denominations"),
        help_text=_(
            "Enter amounts separated by commas (e.g., 25, 50, 100). Currency symbol not needed."
        ),
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "vTextField",
                "style": "width: 100%;",
                "placeholder": "25, 50, 100, 200",
            }
        ),
    )

    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            # Translatable text fields
            "name": TranslatableFieldWidget(
                base_widget=forms.TextInput(attrs={"class": "vTextField", "style": "width: 100%;"})
            ),
            # Translatable rich text fields
            "short_description": TranslatableFieldWidget(
                base_widget=CKEditor5Widget(config_name="product_short")
            ),
            "full_description": TranslatableFieldWidget(
                base_widget=CKEditor5Widget(config_name="content_rich")
            ),
            # Translatable SEO fields
            "meta_title": TranslatableFieldWidget(
                base_widget=forms.TextInput(attrs={"class": "vTextField", "style": "width: 100%;"})
            ),
            "meta_description": TranslatableFieldWidget(
                base_widget=forms.Textarea(
                    attrs={"rows": 3, "class": "vLargeTextField", "style": "width: 100%;"}
                )
            ),
            # Key-value editors for JSON dict fields
            "features": KeyValueWidget(key_label="Feature", value_label="Detail"),
            "specifications": KeyValueWidget(key_label="Specification", value_label="Value"),
        }


@admin.register(Product)
class ProductAdmin(
    CustomFieldsAdminMixin,
    SEOGeneratorAdminMixin,
    TranslatableAdminMixin,
    MoneyFieldCurrencyMixin,
    admin.ModelAdmin,
):
    # Use custom change_form template for the new design
    change_form_template = "admin/catalog/product/change_form.html"

    # Specify which fields are translatable
    translatable_fields = [
        "name",
        "short_description",
        "full_description",
        "meta_title",
        "meta_description",
    ]

    # Use the custom form with translation widgets
    form = ProductForm

    # Include translation editor assets
    class Media:
        js = TranslatableAdminMixin.Media.js + SEOGeneratorAdminMixin.Media.js
        css = {**TranslatableAdminMixin.Media.css, **SEOGeneratorAdminMixin.Media.css}

    # Use custom change_list template
    change_list_template = "admin/catalog/product/change_list.html"
    list_per_page = 50

    list_display = [
        "name",
        "sku",
        "category",
        "brand",
        "price",
        "pricing_strategy",
        "status",
        "is_featured",
        "international_ready",
    ]
    list_filter = [
        "status",
        "is_featured",
        "pricing_strategy",
        "category",
        "brand",
        "product_type",
        "country_of_origin",
    ]
    search_fields = ["name", "sku", "hs_code"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [
        ProductImageInline,
        ProductAttributeAssignmentInline,
        ProductVariantInline,
        ProductPriceInline,
        DigitalAssetInline,
        StockItemInline,
        ProductRegionVisibilityInline,
    ]
    actions = [
        "mark_international_ready",
        "export_customs_data",
        "delete_selected_products",
        "restore_selected_products",
    ]
    readonly_fields = ["variant_stock_display"]
    filter_horizontal = ["tags"]

    # Fieldsets with translation support
    fieldsets = (
        (
            _("Basic Information"),
            {"fields": ("name", "slug", "sku", "product_type", "category", "brand", "tags")},
        ),
        (
            _("Product Descriptions"),
            {
                "fields": ("short_description", "full_description"),
                "description": _(
                    "Short description appears in product listings. Full description shows on the product page."
                ),
            },
        ),
        (
            _("SEO"),
            {
                "fields": ("meta_title", "meta_description", "seo_auto_generated"),
                "description": _(
                    "Search engine optimization fields for better visibility in search results."
                ),
            },
        ),
        (_("Product Details"), {"fields": ("features", "specifications")}),
        (
            _("Pricing"),
            {
                "fields": (
                    "pricing_strategy",
                    "price",
                    "cost",
                    "sale_type",
                    "sale_value",
                    "sale_start_date",
                    "sale_end_date",
                ),
                "description": _(
                    'Use "Dynamic" pricing to auto-convert prices using exchange rates, or "Fixed" to set custom prices per currency below.'
                ),
            },
        ),
        (
            _("Bundle Pricing"),
            {
                "fields": ("bundle_pricing_strategy", "bundle_discount_percentage"),
                "description": _(
                    'Configure how the bundle price is calculated. Choose "Fixed Price" to use the price field above, "Percentage Discount" to discount component sum, or "Sum of Components" to show total of all components.'
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Gift Card Configuration"),
            {
                "fields": (
                    "gift_card_denomination_type",
                    "gift_card_denominations",
                    "gift_card_min_amount",
                    "gift_card_max_amount",
                    "gift_card_expires_days",
                    "gift_card_currency",
                ),
                "description": _(
                    "Configure gift card options. Choose fixed denominations, custom amounts, or both. Set expiration period (0 = never expires). Optionally set a specific currency for multi-currency stores."
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Customization Configuration"),
            {
                "fields": ("allow_customization", "customization_preview_template"),
                "description": _(
                    "Enable product customization to allow customers to personalize this product with text, images, or selections. Customization options are managed in the section below."
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Subscription Configuration"),
            {
                "fields": (
                    "is_subscription_enabled",
                    "subscription_plans",
                    "allow_one_time_purchase",
                    "subscription_default",
                ),
                "description": _(
                    "Enable subscription billing for this product. Customers can purchase with recurring payments. Configure available subscription plans and whether one-time purchase is also allowed."
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Configurator Configuration"),
            {
                "fields": ("configurator_pricing_strategy", "configurator_base_price"),
                "description": _(
                    "Configure pricing for build-to-order products. "
                    "Slots and options are managed in the sections below."
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Inventory"),
            {
                "fields": (
                    "track_inventory",
                    "low_stock_threshold",
                    "allow_backorders",
                    "out_of_stock_action_override",
                ),
                "description": _(
                    "Inventory is tracked per warehouse. Manage stock levels in the Stock Items section below. Out of stock action overrides site-wide and category settings."
                ),
            },
        ),
        (
            _("Pre-Order"),
            {
                "fields": ("is_preorder", "preorder_release_date", "preorder_message"),
                "description": _(
                    "Enable pre-orders for products not yet available. Pre-order products are purchasable even when out of stock."
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Physical Attributes"),
            {"fields": ("weight", "length", "width", "height", "preferred_shipping_package")},
        ),
        (_("Product Identifiers"), {"fields": ("gtin", "ean", "upc", "isbn", "asin", "mpn")}),
        (
            _("International Shipping / Customs"),
            {
                "fields": (
                    "hs_code",
                    "country_of_origin",
                    "unit_price_for_customs",
                    "export_license_number",
                    "export_license_expiry",
                ),
                "description": _(
                    "Required for international shipments. "
                    '<a href="https://hts.usitc.gov/" target="_blank">Look up HS codes here</a>. '
                    "Products without this data cannot be shipped internationally."
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Product Page Design"),
            {
                "fields": (
                    "page_template",
                    "gallery_type",
                    "show_related_products",
                    "show_reviews",
                    "show_specifications",
                ),
                "description": _(
                    'Leave "Page Template" empty to use the site default. Configure site-wide defaults under Design > Page Templates.'
                ),
            },
        ),
        (_("Status"), {"fields": ("status", "is_featured", "is_digital", "hide_from_storefront")}),
        (
            _("Licensing"),
            {
                "fields": (
                    "requires_license",
                    "license_generation_trigger",
                    "license_template",
                    "default_license_type",
                    "default_max_activations",
                    "default_validity_days",
                    "license_provider",
                    "external_product_id",
                ),
                "description": _("Configure license generation settings for this digital product."),
                "classes": ("collapse",),
            },
        ),
    )

    def get_fieldsets(self, request, obj=None):
        """
        Dynamically modify fieldsets based on site settings and product type.

        When multi-currency is disabled, hide the pricing_strategy field since only
        one currency is in use and the strategy choice doesn't apply.

        For variable products, add variant_stock_display to Inventory fieldset to show
        aggregated stock totals from all variants (stock management happens at variant level).
        """
        from core.models import SiteSettings

        settings = SiteSettings.get_settings()

        # Get the base fieldsets
        fieldsets = super().get_fieldsets(request, obj)
        # Make a mutable copy
        fieldsets = list(fieldsets)

        # If multi-currency is disabled, remove pricing_strategy from Pricing fieldset
        if not settings.enable_multi_currency:
            # Find and modify the Pricing fieldset
            for i, (name, options) in enumerate(fieldsets):
                if name == _("Pricing"):
                    # Create a mutable copy of the options dict
                    options = dict(options)
                    fields = list(options["fields"])

                    # Remove pricing_strategy from fields
                    if "pricing_strategy" in fields:
                        fields.remove("pricing_strategy")

                    # Update the options with modified fields
                    options["fields"] = tuple(fields)
                    # Update description to remove multi-currency reference
                    options["description"] = _("Set product pricing and sales information.")

                    # Replace the fieldset
                    fieldsets[i] = (name, options)
                    break

        # For variable products, replace Inventory fieldset with variant stock summary
        if obj and obj.product_type == "variable":
            for i, (name, options) in enumerate(fieldsets):
                if name == _("Inventory"):
                    # Replace entire Inventory fieldset for variable products
                    # Stock is managed at variant level in the Variations tab
                    options = {
                        "fields": ("variant_stock_display",),
                        "description": _(
                            "<strong>Stock is managed at the variant level.</strong> "
                            "Go to the Variations tab below to manage stock for each variant. "
                            "The table below shows aggregated stock totals from all variants."
                        ),
                    }
                    fieldsets[i] = (name, options)
                    break

        # For configurable products, remove Configurator Configuration fieldset
        # (fields are rendered directly in the Configuration tab panel)
        if obj and obj.product_type == "configurable":
            fieldsets = [(n, o) for n, o in fieldsets if n != _("Configurator Configuration")]

        return tuple(fieldsets)

    def get_inlines(self, request, obj=None):
        """
        Exclude ProductImageInline since we use a custom media manager in the change form.
        The inline formset would interfere with our custom JSON-based image handling.

        StockItemInline is conditionally included based on enable_multi_warehouse setting.
        When multi-warehouse is disabled, simplified stock management is shown instead.

        ProductPriceInline is conditionally included only when multi-currency is enabled.
        When multi-currency is disabled, only the default currency is used.

        DigitalAssetInline is conditionally included for digital products only.
        CustomizationOptionInline is shown when product allows customization.
        """
        from core.models import SiteSettings

        settings = SiteSettings.get_settings()

        # Base inlines (always shown)
        inlines = [ProductVariantInline, ProductRegionVisibilityInline, ProductDependencyInline]

        # Only show ProductPriceInline when multi-currency is enabled
        if settings.enable_multi_currency:
            inlines.append(ProductPriceInline)

        # Only show BundleItemInline for bundle products
        if obj and obj.product_type == "bundle":
            inlines.insert(0, BundleItemInline)  # Add at the beginning for prominence

        # Only show DigitalAssetInline for digital products
        if obj and obj.is_digital:
            inlines.insert(0, DigitalAssetInline)  # Add at the beginning for prominence

        # Only show CustomizationOptionInline when product allows customization
        if obj and obj.allow_customization:
            inlines.insert(0, CustomizationOptionInline)  # Add at the beginning for prominence

        # Only show configurator inlines for configurable products
        if obj and obj.product_type == "configurable":
            inlines.insert(0, ConfigurationSlotInline)  # Add at the beginning for prominence
            inlines.append(ConfigurationPresetInline)

        # Only show booking inlines for booking products
        if obj and obj.product_type == "booking":
            inlines.insert(0, BookingConfigInline)
            inlines.insert(1, BookingResourceInline)
            inlines.insert(2, BookingPersonTypeInline)
            inlines.insert(3, BookingAvailabilityRuleInline)
            inlines.insert(4, BookingRecurrenceRuleInline)

        # StockItemInline: Only show for physical products when multi-warehouse is enabled
        # - Variable products: Stock managed at variant level (in ProductVariantInline)
        # - Digital/gift_card products: No physical inventory to track
        if settings.enable_multi_warehouse:
            # For new products (obj is None), show the inline
            # For existing products, check if it's a physical product type
            if not obj or (
                obj.product_type not in ("variable", "digital", "gift_card", "booking")
                and not obj.is_digital
            ):
                inlines.append(StockItemInline)

        return inlines

    def get_form(self, request, obj=None, **kwargs):
        """Override for gift card currency choices (MoneyField handling via mixin)"""
        form = super().get_form(request, obj, **kwargs)

        # Populate gift_card_currency choices from enabled currencies
        if "gift_card_currency" in form.base_fields:
            from core.utils.currency_helpers import get_enabled_currencies

            currency_choices = get_enabled_currencies()
            gc_currency_choices = [("", _("Store base currency (default)"))]
            gc_currency_choices.extend((code, label) for code, label in currency_choices)
            form.base_fields["gift_card_currency"].widget = forms.Select(
                choices=gc_currency_choices
            )

        return form

    def changelist_view(self, request, extra_context=None):
        """Add custom context data for the product list view"""
        extra_context = extra_context or {}

        # Get all products for counting
        queryset = self.get_queryset(request)

        # Calculate counts for filter tabs
        extra_context["all_count"] = queryset.count()
        extra_context["published_count"] = queryset.filter(status="published").count()
        extra_context["draft_count"] = queryset.filter(status="draft").count()
        extra_context["featured_count"] = queryset.filter(is_featured=True).count()
        # NOTE: Stock counts removed - inventory is now managed per-warehouse via StockItem admin

        # Add filter dropdown data for Advanced Filters panel
        extra_context["categories"] = Category.objects.filter(is_active=True).order_by("name")
        extra_context["brands"] = Brand.objects.filter(is_active=True).order_by("name")

        return super().changelist_view(request, extra_context=extra_context)

    def get_queryset(self, request):
        """
        Filter queryset based on request parameters.

        Optimizes queries with select_related() and prefetch_related() to reduce
        database queries on the product change form.
        """
        qs = super().get_queryset(request)

        # Optimize ForeignKey lookups with select_related
        qs = qs.select_related("category", "brand")

        # Optimize reverse relations with prefetch_related for change form
        qs = qs.prefetch_related(
            "images",  # ProductImage inline
            "variants",  # ProductVariant inline
            "variants__images",  # ProductVariantImage (nested in variants)
            "currency_prices",  # ProductPrice inline
            "digital_assets",  # DigitalAsset inline
            "stock_items",  # StockItem inline
            "stock_items__warehouse",  # Warehouse FK in StockItem
            "region_visibility",  # ProductRegionVisibility inline
            "attribute_assignments",  # ProductAttributeAssignment inline
            "attribute_assignments__attribute",  # Attribute FK
            "attribute_assignments__allowed_values",  # AttributeValue M2M
            "bundle_items",  # BundleItem inline
            "bundle_items__component_product",  # Product FK in BundleItem
            "customization_options",  # CustomizationOption inline
        )

        # Apply custom filters from URL parameters

        # Search filter
        search = request.GET.get("search", "").strip()
        if search:
            qs = qs.filter(
                Q(name__icontains=search) | Q(sku__icontains=search) | Q(hs_code__icontains=search)
            )

        # Status filter
        status_filter = request.GET.get("status")
        if status_filter:
            qs = qs.filter(status=status_filter)

        # Product type filter
        product_type = request.GET.get("product_type")
        if product_type:
            qs = qs.filter(product_type=product_type)

        # Category filter
        category_id = request.GET.get("category")
        if category_id:
            try:
                qs = qs.filter(category_id=int(category_id))
            except ValueError:
                pass

        # Brand filter
        brand_id = request.GET.get("brand")
        if brand_id:
            try:
                qs = qs.filter(brand_id=int(brand_id))
            except ValueError:
                pass

        # Digital filter
        is_digital = request.GET.get("is_digital")
        if is_digital == "digital":
            qs = qs.filter(is_digital=True)
        elif is_digital == "physical":
            qs = qs.filter(is_digital=False)

        # Has digital assets filter (uses Count annotation)
        has_digital_assets = request.GET.get("has_digital_assets")
        if has_digital_assets == "with":
            qs = qs.annotate(digital_asset_count=Count("digital_assets")).filter(
                digital_asset_count__gt=0
            )
        elif has_digital_assets == "without":
            qs = qs.annotate(digital_asset_count=Count("digital_assets")).filter(
                digital_asset_count=0
            )

        # Requires license filter
        requires_license = request.GET.get("requires_license")
        if requires_license == "licensed":
            qs = qs.filter(requires_license=True)
        elif requires_license == "unlicensed":
            qs = qs.filter(requires_license=False)

        # Pricing strategy filter
        pricing_strategy = request.GET.get("pricing_strategy")
        if pricing_strategy:
            qs = qs.filter(pricing_strategy=pricing_strategy)

        # On sale filter
        on_sale = request.GET.get("on_sale")
        if on_sale == "yes":
            qs = qs.filter(sale_price__isnull=False)
        elif on_sale == "no":
            qs = qs.filter(sale_price__isnull=True)

        # Subscription filter
        is_subscription = request.GET.get("is_subscription")
        if is_subscription == "yes":
            qs = qs.filter(is_subscription_enabled=True)
        elif is_subscription == "no":
            qs = qs.filter(is_subscription_enabled=False)

        # Preorder filter
        is_preorder = request.GET.get("is_preorder")
        if is_preorder == "yes":
            qs = qs.filter(is_preorder=True)
        elif is_preorder == "no":
            qs = qs.filter(is_preorder=False)

        # Inventory tracking filter
        track_inventory = request.GET.get("track_inventory")
        if track_inventory == "yes":
            qs = qs.filter(track_inventory=True)
        elif track_inventory == "no":
            qs = qs.filter(track_inventory=False)

        # Import source filter
        import_source = request.GET.get("import_source")
        if import_source == "manual":
            qs = qs.filter(import_source__isnull=True)
        elif import_source == "imported":
            qs = qs.exclude(import_source__isnull=True)

        # Featured filter
        is_featured = request.GET.get("is_featured")
        if is_featured == "yes":
            qs = qs.filter(is_featured=True)
        elif is_featured == "no":
            qs = qs.filter(is_featured=False)

        return qs

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        """Override to debug form and formset validation"""
        if request.method == "POST":
            print("\n" + "=" * 80)
            print("[ProductAdmin.changeform_view] POST REQUEST RECEIVED")
            print(f"[ProductAdmin.changeform_view] Object ID: {object_id}")
            print(
                f"[ProductAdmin.changeform_view] POST keys (first 30): {list(request.POST.keys())[:30]}"
            )
            print(
                f"[ProductAdmin.changeform_view] product_images_data present: {'product_images_data' in request.POST}"
            )

            # Get the form class and create form instance
            Form = self.get_form(request, obj=self.get_object(request, object_id))
            form = Form(request.POST, request.FILES, instance=self.get_object(request, object_id))

            print(f"[ProductAdmin.changeform_view] Form is_valid: {form.is_valid()}")
            if not form.is_valid():
                print(f"[ProductAdmin.changeform_view] Form errors: {form.errors}")

            # Check inline formsets
            formsets, inline_instances = self._create_formsets(
                request, self.get_object(request, object_id), change=bool(object_id)
            )
            print(f"[ProductAdmin.changeform_view] Number of inline formsets: {len(formsets)}")
            for i, formset in enumerate(formsets):
                inline_name = inline_instances[i].__class__.__name__
                is_valid = formset.is_valid()
                print(
                    f"[ProductAdmin.changeform_view] Formset {i} ({inline_name}) is_valid: {is_valid}"
                )
                if not is_valid:
                    print(f"[ProductAdmin.changeform_view] Formset {i} errors: {formset.errors}")
                    print(
                        f"[ProductAdmin.changeform_view] Formset {i} non_form_errors: {formset.non_form_errors()}"
                    )
            print("=" * 80 + "\n")

        return super().changeform_view(request, object_id, form_url, extra_context)

    def save_model(self, request, obj, form, change):
        """Handle translations data and simple stock quantity from custom form"""
        import json

        print(f"[ProductAdmin.save_model] Called for product {obj.id if obj.id else 'NEW'}")
        print(
            f"[ProductAdmin.save_model] POST keys: {list(request.POST.keys())[:20]}"
        )  # Show first 20 keys
        print(
            f"[ProductAdmin.save_model] product_images_data in POST: {'product_images_data' in request.POST}"
        )

        # Check if translations_data was submitted (from our custom form)
        translations_data = request.POST.get("translations_data")
        if translations_data:
            try:
                translations = json.loads(translations_data)
                obj.translations = translations
            except json.JSONDecodeError:
                pass  # Keep existing translations if JSON is invalid

        super().save_model(request, obj, form, change)

        # Handle simple stock quantity (only when multi-warehouse is disabled AND product is not variable)
        from core.models import SiteSettings

        settings = SiteSettings.get_settings()

        if (
            not settings.enable_multi_warehouse
            and obj.product_type != "variable"
            and "simple_stock_quantity" in request.POST
        ):
            try:
                from decimal import Decimal

                from catalog.models import SalesRegion, StockItem, Warehouse

                simple_stock_qty = request.POST.get("simple_stock_quantity", "0")
                quantity = Decimal(simple_stock_qty) if simple_stock_qty else Decimal("0")

                # Get or create default sales region (required for warehouse)
                default_region, region_created = SalesRegion.objects.get_or_create(
                    code="DEFAULT",
                    defaults={
                        "name": "Default Region",
                        "countries": ["SG"],
                        "default_currency": "SGD",
                        "is_active": True,
                        "priority": 0,
                    },
                )
                if region_created:
                    print("[ProductAdmin.save_model] Created default sales region (DEFAULT)")

                # Get or create default warehouse (code 'MAIN-WH' to match migration 0031 and SiteSettings validation)
                default_warehouse, wh_created = Warehouse.objects.get_or_create(
                    code="MAIN-WH",
                    defaults={
                        "name": "Main Warehouse",
                        "is_active": True,
                        "region": default_region,
                        "address_line1": "123 Main Street",
                        "city": "City",
                        "country": "US",  # Default to US to match setup command
                        "postal_code": "00000",
                        "fulfillment_priority": 100,
                    },
                )
                if wh_created:
                    print("[ProductAdmin.save_model] Created default warehouse (MAIN-WH)")

                if default_warehouse:
                    # Get or create stock item for this product in the default warehouse
                    # Important: variant=None ensures we only get the parent product's stock item
                    stock_item, created = StockItem.objects.get_or_create(
                        product=obj,
                        warehouse=default_warehouse,
                        variant=None,  # Explicitly filter for parent product stock only
                        defaults={"on_hand": quantity},
                    )

                    if not created and stock_item.on_hand != quantity:
                        # Update quantity if it changed
                        old_quantity = stock_item.on_hand
                        stock_item.on_hand = quantity
                        stock_item.save()

                        print(
                            f"[ProductAdmin.save_model] Updated simple stock: {old_quantity} -> {quantity}"
                        )

                        # Optionally create a stock movement record for audit trail
                        try:
                            from catalog.models import StockMovement

                            movement_qty = quantity - old_quantity
                            StockMovement.objects.create(
                                stock_item=stock_item,
                                movement_type="adjustment",
                                quantity=movement_qty,
                                previous_quantity=old_quantity,
                                new_quantity=quantity,
                                reason=f"Stock adjusted via product admin by {request.user.username}",
                            )
                        except Exception as e:
                            print(f"[ProductAdmin.save_model] Error creating stock movement: {e}")
                    elif created:
                        print(
                            f"[ProductAdmin.save_model] Created simple stock item with on_hand: {quantity}"
                        )
            except Exception as e:
                print(f"[ProductAdmin.save_model] Error updating simple stock quantity: {e}")

        print("[ProductAdmin.save_model] Completed")

    def save_formset(self, request, form, formset, change):
        """Handle variant stock updates from custom inline form"""
        import logging

        logger = logging.getLogger(__name__)

        print(f"[ProductAdmin.save_formset] Called for formset model: {formset.model.__name__}")

        # Save the formset first (creates/updates variants)
        instances = formset.save()
        print(f"[ProductAdmin.save_formset] Saved {len(instances)} instances")

        # Process stock updates for each variant
        if formset.model == ProductVariant:
            from catalog.models import StockItem, Warehouse

            print("[ProductAdmin.save_formset] Processing variant stock updates...")

            # Debug: Print all POST keys related to stock
            stock_keys = [k for k in request.POST if "stock_item_" in k]
            print(
                f"[ProductAdmin.save_formset] Found {len(stock_keys)} stock-related POST keys: {stock_keys[:5]}..."
            )

            # Process ALL variants in the formset, not just newly saved ones
            # This is important because stock updates might be the only change
            all_variants = []
            for form in formset.forms:
                if hasattr(form, "instance") and form.instance and form.instance.pk:
                    all_variants.append(form.instance)

            print(
                f"[ProductAdmin.save_formset] Processing stock for {len(all_variants)} total variants"
            )

            for instance in all_variants:
                print(
                    f"[ProductAdmin.save_formset] Processing variant: {instance.name} (ID: {instance.pk})"
                )

                # Ensure variant has stock items for all warehouses
                warehouses = Warehouse.objects.all()
                for warehouse in warehouses:
                    stock_item, created = StockItem.objects.get_or_create(
                        product=instance.product,
                        variant=instance,
                        warehouse=warehouse,
                        defaults={"on_hand": 0, "allocated": 0, "low_stock_threshold": 0},
                    )
                    if created:
                        print(
                            f"[ProductAdmin.save_formset] Created stock item for variant {instance.name} in warehouse {warehouse.code}"
                        )

                # Look for stock item updates in request.POST
                stock_items = instance.stock_items.all()
                print(
                    f"[ProductAdmin.save_formset] Found {stock_items.count()} stock items for this variant"
                )

                for stock_item in stock_items:
                    on_hand_key = f"stock_item_{stock_item.id}_on_hand"
                    threshold_key = f"stock_item_{stock_item.id}_low_stock_threshold"

                    print(
                        f"[ProductAdmin.save_formset] Looking for keys: {on_hand_key}, {threshold_key}"
                    )
                    print(
                        f"[ProductAdmin.save_formset] Keys in POST: {on_hand_key in request.POST}, {threshold_key in request.POST}"
                    )

                    if on_hand_key in request.POST:
                        print(
                            f"[ProductAdmin.save_formset] Found {on_hand_key} = {request.POST[on_hand_key]}"
                        )

                    updated = False

                    # Update on_hand if provided
                    if on_hand_key in request.POST:
                        try:
                            new_on_hand = int(request.POST[on_hand_key])
                            if stock_item.on_hand != new_on_hand:
                                old_on_hand = stock_item.on_hand
                                stock_item.on_hand = new_on_hand
                                updated = True

                                logger.info(
                                    f"Updated stock for variant {instance.name} in {stock_item.warehouse.code}: {old_on_hand} -> {new_on_hand}"
                                )
                                print(
                                    f"[ProductAdmin.save_formset] Updated stock: {old_on_hand} -> {new_on_hand}"
                                )

                                # Create stock movement record
                                try:
                                    from catalog.models import StockMovement

                                    movement_qty = new_on_hand - old_on_hand
                                    StockMovement.objects.create(
                                        stock_item=stock_item,
                                        movement_type="adjustment",
                                        quantity=movement_qty,
                                        previous_quantity=old_on_hand,
                                        new_quantity=new_on_hand,
                                        reason=f"Stock adjusted for variant via product admin by {request.user.username}",
                                    )
                                    print(
                                        "[ProductAdmin.save_formset] Created stock movement record"
                                    )
                                except Exception as e:
                                    logger.error(f"Error creating stock movement: {e}")
                                    print(
                                        f"[ProductAdmin.save_formset] Error creating stock movement: {e}"
                                    )
                        except (ValueError, TypeError) as e:
                            logger.warning(f"Invalid on_hand value for {on_hand_key}: {e}")
                            print(f"[ProductAdmin.save_formset] Invalid on_hand value: {e}")

                    # Update low_stock_threshold if provided
                    if threshold_key in request.POST:
                        try:
                            new_threshold = int(request.POST[threshold_key])
                            if stock_item.low_stock_threshold != new_threshold:
                                stock_item.low_stock_threshold = new_threshold
                                updated = True
                                logger.info(
                                    f"Updated low stock threshold for variant {instance.name} in {stock_item.warehouse.code}: {new_threshold}"
                                )
                                print(
                                    f"[ProductAdmin.save_formset] Updated threshold: {new_threshold}"
                                )
                        except (ValueError, TypeError) as e:
                            logger.warning(f"Invalid threshold value for {threshold_key}: {e}")
                            print(f"[ProductAdmin.save_formset] Invalid threshold value: {e}")

                    # Save stock item if any changes were made
                    if updated:
                        stock_item.save()
                        print(f"[ProductAdmin.save_formset] Saved stock item ID: {stock_item.id}")
                    else:
                        print(
                            f"[ProductAdmin.save_formset] No changes for stock item ID: {stock_item.id}"
                        )

    def save_related(self, request, form, formsets, change):
        """Handle product images data from custom form"""
        import json
        import logging

        logger = logging.getLogger(__name__)

        # First save the default related objects (formsets)
        super().save_related(request, form, formsets, change)

        # Handle product images from JSON data
        product_images_data = request.POST.get("product_images_data")
        print(
            f"[ProductAdmin.save_related] product_images_data present: {bool(product_images_data)}"
        )
        if product_images_data:
            print(
                f"[ProductAdmin.save_related] product_images_data length: {len(product_images_data)}"
            )
            try:
                images_data = json.loads(product_images_data)
                print(
                    f"[ProductAdmin.save_related] Successfully parsed {len(images_data)} images from JSON"
                )
                logger.info(f"Processing product images data: {len(images_data)} images")

                # Get existing image IDs to track deletions
                existing_image_ids = set(form.instance.images.values_list("id", flat=True))
                updated_image_ids = set()

                # Process each image in the data
                for image_data in images_data:
                    image_id = image_data.get("id")
                    media_asset_id = image_data.get("media_asset_id")

                    if not media_asset_id:
                        logger.warning(f"Skipping image with no media_asset_id: {image_data}")
                        continue

                    # Update existing or create new ProductImage
                    if image_id and not str(image_id).startswith("new_"):
                        # Update existing image
                        try:
                            product_image = ProductImage.objects.get(
                                id=image_id, product=form.instance
                            )
                            product_image.media_asset_id = media_asset_id
                            product_image.alt_text = image_data.get("alt_text", "")
                            product_image.show_in_gallery = image_data.get("show_in_gallery", True)
                            product_image.show_in_listing = image_data.get("show_in_listing", True)
                            product_image.is_primary = image_data.get("is_primary", False)
                            product_image.position = image_data.get("position", 0)
                            product_image.save()
                            updated_image_ids.add(product_image.id)
                            logger.info(f"Updated ProductImage {product_image.id}")
                        except ProductImage.DoesNotExist:
                            logger.warning(f"ProductImage {image_id} not found, creating new one")
                            # Fall through to create new one
                            image_id = None

                    if not image_id or str(image_id).startswith("new_"):
                        # Create new image
                        print(
                            f"[ProductAdmin.save_related] Creating new image for media_asset_id: {media_asset_id}"
                        )
                        from media_library.models import MediaAsset

                        try:
                            media_asset = MediaAsset.objects.get(id=media_asset_id)
                            print(f"[ProductAdmin.save_related] Found MediaAsset: {media_asset.id}")
                            product_image = ProductImage.objects.create(
                                product=form.instance,
                                media_asset=media_asset,
                                alt_text=image_data.get("alt_text", ""),
                                show_in_gallery=image_data.get("show_in_gallery", True),
                                show_in_listing=image_data.get("show_in_listing", True),
                                is_primary=image_data.get("is_primary", False),
                                position=image_data.get("position", 0),
                            )
                            updated_image_ids.add(product_image.id)
                            print(
                                f"[ProductAdmin.save_related] Created new ProductImage with id: {product_image.id}"
                            )
                            logger.info(f"Created new ProductImage {product_image.id}")
                        except MediaAsset.DoesNotExist:
                            print(
                                f"[ProductAdmin.save_related] ERROR: MediaAsset {media_asset_id} not found"
                            )
                            logger.error(f"MediaAsset {media_asset_id} not found")
                            continue

                # Delete images that were removed from the form
                images_to_delete = existing_image_ids - updated_image_ids
                if images_to_delete:
                    ProductImage.objects.filter(id__in=images_to_delete).delete()
                    print(
                        f"[ProductAdmin.save_related] Deleted {len(images_to_delete)} ProductImages"
                    )
                    logger.info(f"Deleted {len(images_to_delete)} ProductImages")

                print(
                    f"[ProductAdmin.save_related] Finished processing images. Updated: {len(updated_image_ids)}, Deleted: {len(images_to_delete)}"
                )

            except json.JSONDecodeError as e:
                print(f"[ProductAdmin.save_related] ERROR: Failed to parse JSON: {e}")
                logger.error(f"Failed to parse product_images_data: {e}")
            except Exception as e:
                print(f"[ProductAdmin.save_related] ERROR: Exception: {e}")
                logger.error(f"Error processing product images: {e}", exc_info=True)
        else:
            print(
                "[ProductAdmin.save_related] No product_images_data in POST, skipping image processing"
            )

        # Handle variant images from JSON data
        print("[ProductAdmin.save_related] Processing variant images...")
        for formset in formsets:
            # Check if this is the ProductVariant formset
            if formset.model == ProductVariant:
                for form_obj in formset.forms:
                    if form_obj.instance.pk:  # Only process saved variants
                        variant = form_obj.instance
                        variant_images_data_key = f"{form_obj.prefix}-images_data"
                        variant_images_data = request.POST.get(variant_images_data_key)

                        print(
                            f"[ProductAdmin.save_related] Variant {variant.id} ({variant.name}): images_data present: {bool(variant_images_data)}"
                        )

                        if variant_images_data:
                            try:
                                images_data = json.loads(variant_images_data)
                                print(
                                    f"[ProductAdmin.save_related] Processing {len(images_data)} images for variant {variant.id}"
                                )
                                logger.info(
                                    f"Processing variant {variant.id} images: {len(images_data)} images"
                                )

                                # Get existing image IDs to track deletions
                                existing_image_ids = set(
                                    variant.images.values_list("id", flat=True)
                                )
                                updated_image_ids = set()

                                # Process each image in the data
                                for image_data in images_data:
                                    image_id = image_data.get("id")
                                    media_asset_id = image_data.get("media_asset_id")

                                    if not media_asset_id:
                                        logger.warning(
                                            f"Skipping variant image with no media_asset_id: {image_data}"
                                        )
                                        continue

                                    # Update existing or create new ProductVariantImage
                                    if image_id and not str(image_id).startswith("new_"):
                                        # Update existing image
                                        try:
                                            variant_image = ProductVariantImage.objects.get(
                                                id=image_id, variant=variant
                                            )
                                            variant_image.media_asset_id = media_asset_id
                                            variant_image.alt_text = image_data.get("alt_text", "")
                                            variant_image.show_in_gallery = image_data.get(
                                                "show_in_gallery", True
                                            )
                                            variant_image.show_in_listing = image_data.get(
                                                "show_in_listing", True
                                            )
                                            variant_image.is_primary = image_data.get(
                                                "is_primary", False
                                            )
                                            variant_image.position = image_data.get("position", 0)
                                            variant_image.save()
                                            updated_image_ids.add(variant_image.id)
                                            logger.info(
                                                f"Updated ProductVariantImage {variant_image.id}"
                                            )
                                        except ProductVariantImage.DoesNotExist:
                                            logger.warning(
                                                f"ProductVariantImage {image_id} not found, creating new one"
                                            )
                                            # Fall through to create new one
                                            image_id = None

                                    if not image_id or str(image_id).startswith("new_"):
                                        # Create new image
                                        print(
                                            f"[ProductAdmin.save_related] Creating new variant image for media_asset_id: {media_asset_id}"
                                        )
                                        from media_library.models import MediaAsset

                                        try:
                                            media_asset = MediaAsset.objects.get(id=media_asset_id)
                                            print(
                                                f"[ProductAdmin.save_related] Found MediaAsset: {media_asset.id}"
                                            )
                                            variant_image = ProductVariantImage.objects.create(
                                                variant=variant,
                                                media_asset=media_asset,
                                                alt_text=image_data.get("alt_text", ""),
                                                show_in_gallery=image_data.get(
                                                    "show_in_gallery", True
                                                ),
                                                show_in_listing=image_data.get(
                                                    "show_in_listing", True
                                                ),
                                                is_primary=image_data.get("is_primary", False),
                                                position=image_data.get("position", 0),
                                            )
                                            updated_image_ids.add(variant_image.id)
                                            print(
                                                f"[ProductAdmin.save_related] Created new ProductVariantImage with id: {variant_image.id}"
                                            )
                                            logger.info(
                                                f"Created new ProductVariantImage {variant_image.id}"
                                            )
                                        except MediaAsset.DoesNotExist:
                                            print(
                                                f"[ProductAdmin.save_related] ERROR: MediaAsset {media_asset_id} not found"
                                            )
                                            logger.error(f"MediaAsset {media_asset_id} not found")
                                            continue

                                # Delete images that were removed from the form
                                images_to_delete = existing_image_ids - updated_image_ids
                                if images_to_delete:
                                    ProductVariantImage.objects.filter(
                                        id__in=images_to_delete
                                    ).delete()
                                    print(
                                        f"[ProductAdmin.save_related] Deleted {len(images_to_delete)} ProductVariantImages for variant {variant.id}"
                                    )
                                    logger.info(
                                        f"Deleted {len(images_to_delete)} ProductVariantImages for variant {variant.id}"
                                    )

                                print(
                                    f"[ProductAdmin.save_related] Finished processing variant {variant.id} images. Updated: {len(updated_image_ids)}, Deleted: {len(images_to_delete)}"
                                )

                            except json.JSONDecodeError as e:
                                print(
                                    f"[ProductAdmin.save_related] ERROR: Failed to parse variant images JSON: {e}"
                                )
                                logger.error(
                                    f"Failed to parse variant images data for variant {variant.id}: {e}"
                                )
                            except Exception as e:
                                print(
                                    f"[ProductAdmin.save_related] ERROR: Exception processing variant images: {e}"
                                )
                                logger.error(
                                    f"Error processing variant {variant.id} images: {e}",
                                    exc_info=True,
                                )

        print("[ProductAdmin.save_related] Finished processing all variant images")

    def change_view(self, request, object_id, form_url="", extra_context=None):
        """Add extra context for change view"""
        extra_context = extra_context or {}

        # Get available languages from translations app
        try:
            from translations.models import Language

            languages = Language.objects.filter(is_active=True).values("code", "name")
            extra_context["available_languages"] = list(languages)
        except Exception:
            # Fallback to settings languages
            from django.conf import settings

            extra_context["available_languages"] = [
                {"code": code, "name": name} for code, name in settings.LANGUAGES
            ]

        # Add inventory management settings
        from core.models import SiteSettings

        settings = SiteSettings.get_settings()
        extra_context["enable_multi_warehouse"] = settings.enable_multi_warehouse

        # For simple stock mode, get current stock quantity from default warehouse
        if not settings.enable_multi_warehouse and object_id:
            try:
                from catalog.models import Product, StockItem, Warehouse

                product = Product.objects.get(pk=object_id)
                default_warehouse = Warehouse.objects.filter(code="MAIN-WH").first()

                if default_warehouse:
                    stock_item = StockItem.objects.filter(
                        product=product, warehouse=default_warehouse
                    ).first()

                    extra_context["simple_stock_quantity"] = stock_item.on_hand if stock_item else 0
                else:
                    extra_context["simple_stock_quantity"] = 0
            except Exception as e:
                print(f"[ProductAdmin.change_view] Error getting simple stock quantity: {e}")
                extra_context["simple_stock_quantity"] = 0

        # Check if product has a 3D scene (for configurable products)
        if object_id:
            try:
                from configurator_3d.models import SceneConfig

                product = Product.objects.get(pk=object_id)
                if product.product_type == "configurable":
                    extra_context["has_3d_scene"] = SceneConfig.objects.filter(
                        product_id=object_id, base_model__isnull=False
                    ).exists()
            except Exception:
                pass

        # Check if product has a design editor config (for customizable products)
        if object_id:
            try:
                from customizable_product.models import ProductDesignConfig

                product_obj = extra_context.get("_product") or Product.objects.get(pk=object_id)
                if product_obj.product_type == "customizable":
                    extra_context["has_design_config"] = (
                        ProductDesignConfig.objects.filter(
                            product_id=object_id, surfaces__isnull=False
                        )
                        .distinct()
                        .exists()
                    )
            except Exception:
                pass

        # Configuration tab context for configurable products
        if object_id:
            try:
                product = extra_context.get("_product") or Product.objects.get(pk=object_id)
                if product.product_type == "configurable":
                    from django.db.models import Count

                    from catalog.models import CompatibilityRule, ConfigurationSlot

                    slots = (
                        ConfigurationSlot.objects.filter(product=product)
                        .annotate(option_count=Count("options"))
                        .order_by("sort_order")
                    )

                    slots_data = []
                    for slot in slots:
                        slots_data.append(
                            {
                                "id": slot.id,
                                "name": str(slot.name),
                                "icon": slot.icon or "fas fa-puzzle-piece",
                                "is_required": slot.is_required,
                                "min_selections": slot.min_selections,
                                "max_selections": slot.max_selections,
                                "option_count": slot.option_count,
                            }
                        )

                    extra_context["configuration_slots_data"] = slots_data
                    extra_context["compatibility_rule_count"] = CompatibilityRule.objects.filter(
                        configurable_product=product
                    ).count()
            except Exception:
                pass

        # Component usage: show which configurable products use this product as an option
        if object_id:
            try:
                from catalog.models import ConfigurationSlotOption

                product = Product.objects.get(pk=object_id)
                slot_options = (
                    ConfigurationSlotOption.objects.filter(option_product=product)
                    .select_related("slot__product")
                    .distinct()
                )
                if slot_options.exists():
                    parent_products = {}
                    for opt in slot_options:
                        parent = opt.slot.product
                        if parent.pk not in parent_products:
                            parent_products[parent.pk] = {
                                "id": parent.pk,
                                "name": str(parent.name),
                                "slot_names": [],
                            }
                        slot_name = str(opt.slot.name)
                        if slot_name not in parent_products[parent.pk]["slot_names"]:
                            parent_products[parent.pk]["slot_names"].append(slot_name)
                    extra_context["configurator_parent_products"] = list(parent_products.values())
            except Exception:
                pass

        return super().change_view(request, object_id, form_url, extra_context)

    def international_ready(self, obj):
        """Display icon indicating if product is ready for international shipping"""
        if obj.is_international_shipping_ready():
            return "✅"
        return "❌"

    international_ready.short_description = _("Intl Ready")

    def variant_stock_display(self, obj):
        """Display aggregated stock totals from all variants for variable products"""
        from django.utils.html import format_html

        if obj.product_type != "variable":
            return "-"

        summary = obj.variant_stock_summary

        if not summary or not summary["variants"]:
            return format_html(
                '<div style="padding: 12px; background: #f8f9fa; border-radius: 6px; color: #6c757d;">'
                '<i class="fas fa-info-circle"></i> No variants with stock yet'
                "</div>"
            )

        # Build HTML table
        html = ['<div style="margin: 8px 0;">']
        html.append(
            '<table style="width: 100%; border-collapse: collapse; background: white; '
            'border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">'
        )
        html.append(
            '<thead style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">'
            "<tr>"
            '<th style="padding: 12px; text-align: left; font-weight: 600;">Variant</th>'
            '<th style="padding: 12px; text-align: center; font-weight: 600;">On Hand</th>'
            '<th style="padding: 12px; text-align: center; font-weight: 600;">Allocated</th>'
            '<th style="padding: 12px; text-align: center; font-weight: 600;">Available</th>'
            "</tr>"
            "</thead>"
        )
        html.append("<tbody>")

        for variant_data in summary["variants"]:
            variant = variant_data["variant"]
            available = variant_data["available"]

            # Color code availability
            if available <= 0:
                avail_color = "#ef4444"  # Red
            elif available < 10:
                avail_color = "#f59e0b"  # Orange
            else:
                avail_color = "#10b981"  # Green

            html.append(
                f'<tr style="border-bottom: 1px solid #e5e7eb;">'
                f'<td style="padding: 10px;"><strong>{variant.name}</strong></td>'
                f'<td style="padding: 10px; text-align: center;">{variant_data["on_hand"]}</td>'
                f'<td style="padding: 10px; text-align: center;">{variant_data["allocated"]}</td>'
                f'<td style="padding: 10px; text-align: center; color: {avail_color}; font-weight: 600;">'
                f"{available}</td>"
                f"</tr>"
            )

        # Add totals row
        total_available = summary["total_available"]
        if total_available <= 0:
            total_color = "#ef4444"
        elif total_available < 10:
            total_color = "#f59e0b"
        else:
            total_color = "#10b981"

        html.append(
            '<tr style="background: #f9fafb; font-weight: 600; border-top: 2px solid #d1d5db;">'
            '<td style="padding: 12px;"><strong>TOTALS</strong></td>'
            f'<td style="padding: 12px; text-align: center;">{summary["total_on_hand"]}</td>'
            f'<td style="padding: 12px; text-align: center;">{summary["total_allocated"]}</td>'
            f'<td style="padding: 12px; text-align: center; color: {total_color}; font-weight: 700;">'
            f"{total_available}</td>"
            "</tr>"
        )

        html.append("</tbody></table></div>")

        return format_html("".join(html))

    variant_stock_display.short_description = _("Variant Stock Summary")

    def mark_international_ready(self, request, queryset):
        """Admin action to check which products need customs data"""
        from django.contrib import messages

        ready_count = 0
        missing_count = 0
        missing_products = []

        for product in queryset:
            if product.is_international_shipping_ready():
                ready_count += 1
            else:
                missing_count += 1
                missing_fields = product.get_missing_customs_fields()
                missing_products.append(f"{product.name} (missing: {', '.join(missing_fields)})")

        if ready_count > 0:
            messages.success(
                request, f"{ready_count} product(s) are ready for international shipping."
            )

        if missing_count > 0:
            messages.warning(
                request,
                f"{missing_count} product(s) are NOT ready for international shipping:\n"
                + "\n".join(missing_products[:10])  # Show max 10
                + (f"\n...and {missing_count - 10} more" if missing_count > 10 else ""),
            )

    mark_international_ready.short_description = _("Check international shipping readiness")

    def export_customs_data(self, request, queryset):
        """Admin action to export customs data as CSV"""
        import csv

        from django.http import HttpResponse

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="product_customs_data.csv"'

        writer = csv.writer(response)
        writer.writerow(
            [
                "SKU",
                "Name",
                "HS Code",
                "Country of Origin",
                "Customs Unit Price",
                "Export License",
                "License Expiry",
                "International Ready",
            ]
        )

        for product in queryset:
            writer.writerow(
                [
                    product.sku,
                    product.name,
                    product.hs_code or "",
                    product.country_of_origin or "",
                    product.unit_price_for_customs or "",
                    product.export_license_number or "",
                    product.export_license_expiry or "",
                    "Yes" if product.is_international_shipping_ready() else "No",
                ]
            )

        return response

    export_customs_data.short_description = _("Export customs data to CSV")

    # ============================================================================
    # Soft-Delete Methods
    # ============================================================================

    def delete_model(self, request, obj):
        """Override delete_model to use soft delete"""
        obj.delete(user=request.user)

    def delete_queryset(self, request, queryset):
        """Override delete_queryset to use soft delete"""
        for obj in queryset:
            obj.delete(user=request.user)

    def delete_selected_products(self, request, queryset):
        """Soft delete selected products"""
        from django.contrib import messages

        count = 0
        for product in queryset:
            product.delete(user=request.user)
            count += 1

        self.message_user(request, f"{count} product(s) moved to recycle bin.", messages.SUCCESS)

    delete_selected_products.short_description = _("Delete selected products")

    def restore_selected_products(self, request, queryset):
        """Restore soft-deleted products"""
        from django.contrib import messages
        from django.core.exceptions import ValidationError

        count = 0
        errors = []

        for product in queryset.filter(is_deleted=True):
            try:
                product.restore()
                count += 1
            except ValidationError as e:
                errors.append(f"{product.name}: {str(e)}")

        if count:
            self.message_user(
                request, f"{count} product(s) restored from recycle bin.", messages.SUCCESS
            )

        if errors:
            self.message_user(
                request, "Some products could not be restored: " + "; ".join(errors), messages.ERROR
            )

    restore_selected_products.short_description = _("Restore selected products")

    def get_urls(self):
        from django.urls import path

        urls = super().get_urls()
        custom_urls = [
            path(
                "bulk-action/",
                self.admin_site.admin_view(self.bulk_action_view),
                name="catalog_product_bulk_action",
            ),
        ]
        return custom_urls + urls

    def bulk_action_view(self, request):
        """Handle bulk actions on products via AJAX."""
        import csv

        from django.http import HttpResponse, JsonResponse

        if request.method != "POST":
            return JsonResponse({"success": False, "message": "POST required"}, status=405)

        try:
            data = json.loads(request.body)
            action = data.get("action")
            product_ids = data.get("product_ids", [])

            if not action or not product_ids:
                return JsonResponse(
                    {"success": False, "message": _("Action and product IDs required")}, status=400
                )

            products = Product.objects.filter(id__in=product_ids)
            count = products.count()

            if action == "publish":
                products.update(status="published")
                message = _("%d product(s) marked as published.") % count

            elif action == "draft":
                products.update(status="draft")
                message = _("%d product(s) marked as draft.") % count

            elif action == "feature":
                products.update(is_featured=True)
                message = _("%d product(s) marked as featured.") % count

            elif action == "unfeature":
                products.update(is_featured=False)
                message = _("%d product(s) removed from featured.") % count

            elif action == "export":
                response = HttpResponse(content_type="text/csv")
                response["Content-Disposition"] = 'attachment; filename="products_export.csv"'
                writer = csv.writer(response)
                writer.writerow(["ID", "Name", "SKU", "Status", "Featured", "Price"])
                for p in products.select_related():
                    writer.writerow(
                        [
                            p.id,
                            p.name,
                            p.sku or "",
                            p.status,
                            p.is_featured,
                            str(p.price) if p.price else "",
                        ]
                    )
                return response

            elif action == "delete":
                deleted_count = 0
                for product in products:
                    product.delete(user=request.user)
                    deleted_count += 1
                message = _("%d product(s) moved to recycle bin.") % deleted_count

            else:
                return JsonResponse(
                    {"success": False, "message": _("Unknown action: %s") % action}, status=400
                )

            return JsonResponse({"success": True, "message": str(message)})

        except json.JSONDecodeError:
            return JsonResponse(
                {"success": False, "message": _("Invalid request data")}, status=400
            )
        except Exception as e:
            logger.error("Product bulk action error: %s", e, exc_info=True)
            return JsonResponse(
                {"success": False, "message": _("An unexpected error occurred. Please try again.")},
                status=500,
            )

    class Media:
        css = {
            "all": (
                "utilities/color_picker/current/color_picker.css",
                "catalog/css/admin_attribute.css",
            )
        }
        js = ("utilities/color_picker/current/color_picker.js",)


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    change_list_template = "admin/catalog/productreview/change_list.html"
    list_display = [
        "product",
        "user",
        "rating",
        "is_approved",
        "is_verified_purchase",
        "created_at",
    ]
    list_filter = ["rating", "is_approved", "is_verified_purchase"]
    search_fields = ["product__name", "user__username", "title"]
    actions = ["approve_reviews", "reject_reviews"]

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["rating_choices"] = range(1, 6)
        return super().changelist_view(request, extra_context=extra_context)

    def approve_reviews(self, request, queryset):
        count = queryset.update(is_approved=True)
        self.message_user(request, _("%d review(s) approved.") % count)

    approve_reviews.short_description = _("Approve selected reviews")

    def reject_reviews(self, request, queryset):
        count = queryset.update(is_approved=False)
        self.message_user(request, _("%d review(s) rejected.") % count)

    reject_reviews.short_description = _("Reject selected reviews")


@admin.register(Collection)
class CollectionAdmin(TranslationAdmin):
    change_form_template = "admin/catalog/collection/change_form.html"
    list_display = ["name", "collection_type", "is_active", "is_featured"]
    list_filter = ["collection_type", "is_active", "is_featured"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ["products"]

    fieldsets = (
        (
            _("Basic Information"),
            {
                "fields": ("name", "slug", "collection_type", "description"),
                "classes": ("tab-basic",),
            },
        ),
        (
            _("Products"),
            {
                "fields": ("products", "auto_criteria"),
                "classes": ("tab-products",),
            },
        ),
        (
            _("Media"),
            {
                "fields": ("image", "banner_image"),
                "classes": ("tab-media",),
            },
        ),
        (
            _("SEO"),
            {
                "fields": ("meta_title", "meta_description"),
                "classes": ("tab-seo",),
            },
        ),
        (
            _("Design"),
            {
                "fields": (
                    "template_variant",
                    "inherit_parent_theme",
                    "css_classes",
                    "layout_config",
                    "style_overrides",
                    "responsive_config",
                ),
                "classes": ("tab-design",),
            },
        ),
        (
            _("Status"),
            {
                "fields": ("is_active", "is_featured", "sort_order"),
                "classes": ("tab-status",),
            },
        ),
    )

    class Media:
        css = {"all": ("catalog/css/collection_change_form.css",)}
        js = ("catalog/js/collection_change_form.js",)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        if object_id:
            try:
                obj = self.get_object(request, object_id)
                if obj:
                    extra_context["product_count"] = obj.products.count()
            except Exception:
                extra_context["product_count"] = 0
        return super().change_view(request, object_id, form_url, extra_context)


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    # Use custom templates
    change_list_template = "admin/catalog/promotion/change_list.html"
    change_form_template = "admin/catalog/promotion/change_form.html"

    list_display = [
        "name",
        "discount_type",
        "discount_value",
        "apply_to",
        "is_active",
        "start_date",
        "end_date",
        "priority",
    ]
    list_filter = ["is_active", "discount_type", "apply_to", "start_date"]
    search_fields = ["name", "description"]
    date_hierarchy = "start_date"

    # M2M fields are handled manually via save_related (wizard sends comma-separated IDs)
    # so we exclude them from the form to prevent validation errors
    exclude = ["categories", "brands", "collections", "products"]

    fieldsets = (
        (_("Basic Information"), {"fields": ("name", "description", "is_active")}),
        (_("Discount Settings"), {"fields": ("discount_type", "discount_value")}),
        (_("Scheduling"), {"fields": ("start_date", "end_date")}),
        (
            _("Product Selection"),
            {
                "fields": ("apply_to",),
                "description": 'Select what products this promotion applies to. Only the relevant fields for your "Apply To" choice will be used.',
            },
        ),
        (
            _("Advanced Settings"),
            {"fields": ("priority", "can_stack_with_product_sales"), "classes": ("collapse",)},
        ),
    )

    def get_form(self, request, obj=None, **kwargs):
        """Use plain DateTimeField to accept HTML5 datetime-local format (Y-m-dTH:M)"""
        from django import forms as dj_forms

        form = super().get_form(request, obj, **kwargs)
        datetime_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"]
        for field_name in ("start_date", "end_date"):
            if field_name in form.base_fields:
                old_field = form.base_fields[field_name]
                form.base_fields[field_name] = dj_forms.DateTimeField(
                    required=old_field.required,
                    input_formats=datetime_formats,
                    help_text=old_field.help_text,
                    label=old_field.label,
                )
        return form

    def changelist_view(self, request, extra_context=None):
        """Add custom context data for the promotions dashboard"""
        from django.utils import timezone

        extra_context = extra_context or {}

        # Get all promotions for counting
        queryset = self.get_queryset(request)
        now = timezone.now()

        # Calculate counts for stats cards
        extra_context["total_count"] = queryset.count()

        # Active promotions (is_active=True, started, not ended)
        active_promotions = queryset.filter(is_active=True, start_date__lte=now)
        active_promotions = active_promotions.filter(
            models.Q(end_date__isnull=True) | models.Q(end_date__gt=now)
        )
        extra_context["active_count"] = active_promotions.count()

        # Scheduled promotions (is_active=True, not started yet)
        extra_context["scheduled_count"] = queryset.filter(
            is_active=True, start_date__gt=now
        ).count()

        # Expired promotions (end_date in the past)
        extra_context["expired_count"] = queryset.filter(end_date__lt=now).count()

        # Add current time for template comparisons
        extra_context["now"] = now

        return super().changelist_view(request, extra_context=extra_context)

    def get_queryset(self, request):
        """Filter queryset based on request parameters"""
        qs = super().get_queryset(request)

        # Apply custom filters from URL parameters
        status_filter = request.GET.get("status")
        if status_filter == "active":
            from django.utils import timezone

            now = timezone.now()
            qs = qs.filter(is_active=True, start_date__lte=now).filter(
                models.Q(end_date__isnull=True) | models.Q(end_date__gt=now)
            )
        elif status_filter == "scheduled":
            from django.utils import timezone

            qs = qs.filter(is_active=True, start_date__gt=timezone.now())
        elif status_filter == "expired":
            from django.utils import timezone

            qs = qs.filter(end_date__lt=timezone.now())

        return qs

    def get_urls(self):
        """Add custom URLs for promotion actions"""
        from django.urls import path

        urls = super().get_urls()
        custom_urls = [
            path(
                "<path:object_id>/activate/",
                self.admin_site.admin_view(self.activate_promotion),
                name="catalog_promotion_activate",
            ),
            path(
                "<path:object_id>/deactivate/",
                self.admin_site.admin_view(self.deactivate_promotion),
                name="catalog_promotion_deactivate",
            ),
            path(
                "selector-data/<str:selector_type>/",
                self.admin_site.admin_view(self.selector_data_view),
                name="catalog_promotion_selector_data",
            ),
        ]
        return custom_urls + urls

    def activate_promotion(self, request, object_id):
        """Activate a promotion"""
        from django.contrib import messages
        from django.shortcuts import redirect

        promotion = self.get_object(request, object_id)
        if promotion:
            promotion.is_active = True
            promotion.save()
            messages.success(request, f'Promotion "{promotion.name}" has been activated.')

        return redirect("admin:catalog_promotion_changelist")

    def deactivate_promotion(self, request, object_id):
        """Deactivate a promotion"""
        from django.contrib import messages
        from django.shortcuts import redirect

        promotion = self.get_object(request, object_id)
        if promotion:
            promotion.is_active = False
            promotion.save()
            messages.success(request, f'Promotion "{promotion.name}" has been deactivated.')

        return redirect("admin:catalog_promotion_changelist")

    def selector_data_view(self, request, selector_type):
        """Return JSON data for product selectors"""
        from django.http import JsonResponse

        items = []

        if selector_type == "categories":
            from .models import Category

            categories = Category.objects.filter(is_active=True).order_by("name")
            for cat in categories:
                items.append(
                    {
                        "id": cat.id,
                        "name": cat.name,
                        "thumbnail": cat.image.url if cat.image else None,
                        "meta": f"{cat.products.count()} products"
                        if hasattr(cat, "products")
                        else None,
                    }
                )

        elif selector_type == "brands":
            from .models import Brand

            brands = Brand.objects.filter(is_active=True).order_by("name")
            for brand in brands:
                items.append(
                    {
                        "id": brand.id,
                        "name": brand.name,
                        "thumbnail": brand.logo.url if brand.logo else None,
                        "meta": f"{brand.products.count()} products"
                        if hasattr(brand, "products")
                        else None,
                    }
                )

        elif selector_type == "collections":
            from .models import Collection

            collections = Collection.objects.filter(is_active=True).order_by("name")
            for collection in collections:
                items.append(
                    {
                        "id": collection.id,
                        "name": collection.name,
                        "thumbnail": collection.image.url if collection.image else None,
                        "meta": f"{collection.products.count()} products",
                    }
                )

        elif selector_type == "products":
            from .models import Product

            products = (
                Product.objects.filter(status="published")
                .select_related("category", "brand")
                .prefetch_related("images")
                .order_by("name")
            )
            for product in products:
                # Get first image thumbnail
                thumbnail = None
                if product.images.exists():
                    first_image = product.images.first()
                    if hasattr(first_image, "thumbnail_small"):
                        thumbnail = first_image.thumbnail_small

                items.append(
                    {
                        "id": product.id,
                        "name": product.name,
                        "thumbnail": thumbnail,
                        "meta": f"${product.price} • {product.sku}",
                    }
                )

        return JsonResponse({"items": items})

    def save_model(self, request, obj, form, change):
        """Set created_by to current user if creating new promotion"""
        if not change:  # Only on creation
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        """Handle the custom product selector ManyToMany fields from wizard form"""
        super().save_related(request, form, formsets, change)

        obj = form.instance

        # Process comma-separated IDs from wizard form hidden inputs
        categories_ids = request.POST.get("categories", "").strip()
        brands_ids = request.POST.get("brands", "").strip()
        collections_ids = request.POST.get("collections", "").strip()
        products_ids = request.POST.get("products", "").strip()

        # Clear existing and set new ManyToMany relationships based on apply_to
        apply_to = request.POST.get("apply_to", "all")

        # Clear all selections first
        obj.categories.clear()
        obj.brands.clear()
        obj.collections.clear()
        obj.products.clear()

        # Set new selections based on apply_to value
        if apply_to == "categories" and categories_ids:
            category_pks = [pk for pk in categories_ids.split(",") if pk.strip()]
            if category_pks:
                obj.categories.set(category_pks)

        elif apply_to == "brands" and brands_ids:
            brand_pks = [pk for pk in brands_ids.split(",") if pk.strip()]
            if brand_pks:
                obj.brands.set(brand_pks)

        elif apply_to == "collections" and collections_ids:
            collection_pks = [pk for pk in collections_ids.split(",") if pk.strip()]
            if collection_pks:
                obj.collections.set(collection_pks)

        elif apply_to == "products" and products_ids:
            product_pks = [pk for pk in products_ids.split(",") if pk.strip()]
            if product_pks:
                obj.products.set(product_pks)


@admin.register(ProductPrice)
class ProductPriceAdmin(admin.ModelAdmin):
    """Admin for multi-currency product prices"""

    list_display = ["product", "currency", "price", "sale_price", "is_active", "updated_at"]
    list_filter = ["is_active", "currency", "updated_at"]
    search_fields = ["product__name", "product__sku", "currency"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        (_("Product & Currency"), {"fields": ("product", "currency")}),
        (_("Pricing"), {"fields": ("price", "sale_price")}),
        (_("Settings"), {"fields": ("is_active",)}),
        (_("Timestamps"), {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def get_form(self, request, obj=None, **kwargs):
        """Override to filter MoneyField currency choices"""
        form = super().get_form(request, obj, **kwargs)
        from core.admin_mixins import _apply_money_field_currency_defaults

        _apply_money_field_currency_defaults(form, obj)
        return form


@admin.register(PriceCharmingRule)
class PriceCharmingRuleAdmin(admin.ModelAdmin):
    """Admin for price charming (psychological pricing) rules"""

    list_display = ["currency", "rule_type", "custom_ending", "min_price_threshold", "is_active"]
    list_filter = ["is_active", "rule_type"]
    search_fields = ["currency"]

    fieldsets = (
        (_("Currency"), {"fields": ("currency",)}),
        (
            _("Charming Rule"),
            {
                "fields": ("rule_type", "custom_ending"),
                "description": _(
                    "Select the type of price charming to apply. For custom endings, specify the decimal value (e.g., 0.99 for .99 endings)."
                ),
            },
        ),
        (_("Settings"), {"fields": ("min_price_threshold", "apply_to_sale_prices", "is_active")}),
    )

    def get_form(self, request, obj=None, **kwargs):
        """Customize form to show/hide custom_ending field based on rule_type"""
        form = super().get_form(request, obj, **kwargs)

        # Add help text with examples
        if "rule_type" in form.base_fields:
            form.base_fields["rule_type"].help_text = _(
                "Examples: "
                "charm_99 converts $20.50 → $19.99, "
                "charm_95 converts €20.50 → €19.95, "
                "round_nearest_10 converts ¥1,234 → ¥1,230"
            )

        return form


@admin.register(BundleItem)
class BundleItemAdmin(admin.ModelAdmin):
    """Admin for managing bundle items (can also be managed via ProductAdmin inline)"""

    list_display = [
        "bundle",
        "component_product",
        "component_variant",
        "quantity",
        "sort_order",
        "is_optional",
    ]
    list_filter = ["is_optional", "bundle__product_type"]
    search_fields = ["bundle__name", "component_product__name"]
    autocomplete_fields = ["bundle", "component_product"]
    ordering = ["bundle", "sort_order", "id"]

    fieldsets = (
        (
            _("Bundle Configuration"),
            {"fields": ("bundle", "component_product", "component_variant")},
        ),
        (_("Item Details"), {"fields": ("quantity", "sort_order", "is_optional")}),
    )


# ============================================================================
# Multi-Location Inventory Admin
# ============================================================================


@admin.register(SalesRegion)
class SalesRegionAdmin(admin.ModelAdmin):
    """Admin for sales regions"""

    change_list_template = "admin/catalog/salesregion/change_list.html"
    change_form_template = "admin/catalog/salesregion/change_form.html"
    list_display = ["name", "code", "default_currency", "warehouse_count", "is_active", "priority"]
    list_filter = ["is_active", "default_currency"]
    search_fields = ["name", "code"]
    ordering = ["-priority", "name"]

    fieldsets = (
        (_("Basic Information"), {"fields": ("name", "code", "is_active", "priority")}),
        (
            _("Geographic Settings"),
            {
                "fields": ("countries", "default_currency"),
                "description": _(
                    'Enter ISO country codes as a JSON array (e.g., ["NZ", "FJ", "AU"])'
                ),
            },
        ),
    )

    class Media:
        css = {"all": ("catalog/css/salesregion_change_form.css",)}

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        if object_id:
            try:
                obj = self.get_object(request, object_id)
                if obj:
                    extra_context["warehouse_count"] = obj.warehouses.count()
                    countries = obj.countries or []
                    extra_context["country_count"] = (
                        len(countries) if isinstance(countries, list) else 0
                    )
            except Exception:
                pass
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def warehouse_count(self, obj):
        """Display count of warehouses in this region"""
        return obj.warehouses.count()

    warehouse_count.short_description = _("Warehouses")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        from django.db.models import Count

        return qs.annotate(warehouse_total=Count("warehouses"))

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        qs = SalesRegion.objects.all()
        extra_context["all_count"] = qs.count()
        extra_context["active_count"] = qs.filter(is_active=True).count()
        extra_context["inactive_count"] = qs.filter(is_active=False).count()

        # Add filter options
        extra_context["currencies"] = (
            SalesRegion.objects.values_list("default_currency", flat=True)
            .distinct()
            .order_by("default_currency")
        )

        # Handle custom filter tabs
        is_active = request.GET.get("is_active")
        if is_active == "1":
            request.GET = request.GET.copy()
            request.GET["is_active__exact"] = "1"
        elif is_active == "0":
            request.GET = request.GET.copy()
            request.GET["is_active__exact"] = "0"

        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    """Admin for warehouses"""

    change_list_template = "admin/catalog/warehouse/change_list.html"
    change_form_template = "admin/catalog/warehouse/change_form.html"
    list_display = [
        "name",
        "code",
        "region",
        "city",
        "country",
        "is_active",
        "fulfillment_priority",
        "stock_item_count",
    ]
    list_filter = ["is_active", "region", "country"]
    search_fields = ["name", "code", "city", "address_line1"]
    ordering = ["-fulfillment_priority", "name"]

    fieldsets = (
        (
            _("Basic Information"),
            {
                "fields": ("name", "code", "region", "is_active"),
                "classes": ("tab-basic",),
            },
        ),
        (
            _("Address"),
            {
                "fields": (
                    "address_line1",
                    "address_line2",
                    "city",
                    "state_province",
                    "postal_code",
                    "country",
                ),
                "classes": ("tab-address",),
            },
        ),
        (
            _("Geocoding"),
            {
                "fields": ("latitude", "longitude"),
                "classes": ("tab-geocoding",),
            },
        ),
        (
            _("Fulfillment Settings"),
            {
                "fields": ("fulfillment_priority", "stock_buffer_percentage", "shipping_location"),
                "classes": ("tab-fulfillment",),
            },
        ),
        (
            _("Customer Display"),
            {
                "fields": ("display_name", "show_on_frontend"),
                "classes": ("tab-display",),
            },
        ),
        (
            _("POS / Retail Store"),
            {
                "fields": ("is_retail_location", "pos_display_name", "store_group"),
                "classes": ("tab-pos",),
            },
        ),
        (
            _("Contact Information"),
            {
                "fields": ("contact_name", "contact_email", "contact_phone"),
                "classes": ("tab-contact",),
            },
        ),
    )

    def stock_item_count(self, obj):
        """Display count of products stocked at this warehouse"""
        return obj.stock_items.count()

    stock_item_count.short_description = _("Products Stocked")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        from django.db.models import Count

        return qs.select_related("region").annotate(stock_count=Count("stock_items"))

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        qs = Warehouse.objects.all()
        extra_context["all_count"] = qs.count()
        extra_context["active_count"] = qs.filter(is_active=True).count()
        extra_context["inactive_count"] = qs.filter(is_active=False).count()
        extra_context["retail_count"] = qs.filter(is_retail_location=True).count()

        # Add filter options
        from .models import SalesRegion

        extra_context["regions"] = SalesRegion.objects.all().order_by("name")
        extra_context["countries"] = (
            Warehouse.objects.values_list("country", flat=True).distinct().order_by("country")
        )

        # Handle custom filter tabs
        is_active = request.GET.get("is_active")
        is_retail = request.GET.get("is_retail")
        if is_active is not None or is_retail is not None:
            request.GET = request.GET.copy()
            if is_active == "1":
                request.GET["is_active__exact"] = "1"
            elif is_active == "0":
                request.GET["is_active__exact"] = "0"
            if is_retail == "1":
                request.GET["is_retail_location__exact"] = "1"

        return super().changelist_view(request, extra_context=extra_context)


class StockMovementInline(admin.TabularInline):
    """Inline for viewing stock movement history"""

    model = StockMovement
    extra = 0
    can_delete = False
    fields = [
        "created_at",
        "movement_type",
        "quantity",
        "previous_quantity",
        "new_quantity",
        "reason",
        "user",
    ]
    readonly_fields = [
        "created_at",
        "movement_type",
        "quantity",
        "previous_quantity",
        "new_quantity",
        "reason",
        "user",
    ]
    ordering = ["-created_at"]

    def has_add_permission(self, request, obj=None):
        """Prevent manual creation - movements are auto-created"""
        return False


class LowStockFilter(admin.SimpleListFilter):
    """Filter for low stock items"""

    title = _("stock status")
    parameter_name = "stock_status"

    def lookups(self, request, model_admin):
        return [
            ("low", _("Low Stock (At or below threshold)")),
            ("adequate", _("Adequate Stock (Above threshold)")),
            ("out", _("Out of Stock (0 available)")),
            ("allocated", _("Has Allocated Stock")),
        ]

    def queryset(self, request, queryset):
        from django.db.models import F

        if self.value() == "low":
            return queryset.filter(on_hand__lte=F("low_stock_threshold"))
        elif self.value() == "adequate":
            return queryset.filter(on_hand__gt=F("low_stock_threshold"))
        elif self.value() == "out":
            return queryset.filter(on_hand__lte=F("allocated"))
        elif self.value() == "allocated":
            return queryset.filter(allocated__gt=0)
        return queryset


@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    """Admin for stock items (product-warehouse inventory)"""

    change_list_template = "admin/catalog/stockitem/change_list.html"
    change_form_template = "admin/catalog/stockitem/change_form.html"
    list_display = [
        "product_link",
        "sku",
        "warehouse",
        "on_hand",
        "allocated",
        "available",
        "low_stock_threshold",
        "stock_status_icon",
        "updated_at",
    ]
    list_filter = [LowStockFilter, "warehouse", "warehouse__region", "updated_at"]
    search_fields = ["product__name", "product__sku", "warehouse__name", "warehouse__code"]
    readonly_fields = ["available", "created_at", "updated_at"]
    inlines = [StockMovementInline]
    list_per_page = 50
    date_hierarchy = "updated_at"

    fieldsets = (
        (
            _("Product & Location"),
            {
                "fields": ("product", "warehouse"),
                "classes": ("tab-product",),
            },
        ),
        (
            _("Stock Levels"),
            {
                "fields": ("on_hand", "allocated", "available", "low_stock_threshold"),
                "classes": ("tab-levels",),
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("tab-timestamps",),
            },
        ),
    )

    actions = ["adjust_stock_action", "export_stock_report", "mark_for_reorder"]

    def change_view(self, request, object_id, form_url="", extra_context=None):
        """Add movement count for edit mode."""
        extra_context = extra_context or {}

        if object_id:
            try:
                obj = self.get_object(request, object_id)
                if obj:
                    extra_context["movement_count"] = obj.movements.count()
            except Exception:
                pass

        return super().change_view(request, object_id, form_url, extra_context)

    def product_link(self, obj):
        """Link to product admin"""
        from django.urls import reverse
        from django.utils.html import format_html

        url = reverse("admin:catalog_product_change", args=[obj.product.id])
        return format_html('<a href="{}">{}</a>', url, obj.product.name)

    product_link.short_description = _("Product")
    product_link.admin_order_field = "product__name"

    def sku(self, obj):
        """Display product SKU"""
        return obj.product.sku

    sku.short_description = _("SKU")
    sku.admin_order_field = "product__sku"

    def available(self, obj):
        """Show calculated available stock"""
        return obj.available

    available.short_description = _("Available")

    def stock_status_icon(self, obj):
        """Display icon indicating stock status"""
        from django.utils.html import format_html

        available = obj.available

        if available <= 0:
            # Out of stock
            return format_html(
                '<span style="color: #dc3545; font-weight: bold;" title="Out of Stock">🔴 Out</span>'
            )
        elif available <= obj.low_stock_threshold:
            # Low stock
            return format_html(
                '<span style="color: #ffc107; font-weight: bold;" title="Low Stock">⚠️ Low</span>'
            )
        else:
            # Adequate stock
            return format_html('<span style="color: #28a745;" title="In Stock">✅ OK</span>')

    stock_status_icon.short_description = _("Status")
    stock_status_icon.admin_order_field = "on_hand"

    def adjust_stock_action(self, request, queryset):
        """Bulk action to adjust stock levels"""
        from django import forms
        from django.contrib import messages
        from django.shortcuts import redirect, render

        # Define inline form for stock adjustment
        class StockAdjustmentForm(forms.Form):
            adjustment_type = forms.ChoiceField(
                choices=[
                    ("add", _("Add stock (increase on_hand)")),
                    ("remove", _("Remove stock (decrease on_hand)")),
                    ("set", _("Set stock to specific value")),
                ],
                widget=forms.RadioSelect,
                initial="add",
                label=_("Adjustment Type"),
            )
            quantity = forms.IntegerField(
                min_value=0,
                initial=0,
                label=_("Quantity"),
                help_text=_(
                    'For "Add" and "Remove": amount to change. For "Set": new on_hand value.'
                ),
            )
            reason = forms.CharField(
                widget=forms.Textarea(attrs={"rows": 3}),
                required=False,
                label=_("Reason"),
                help_text=_("Optional: Explain why this adjustment is being made"),
            )

        # If form submitted (POST request)
        if "apply" in request.POST:
            form = StockAdjustmentForm(request.POST)
            if form.is_valid():
                adjustment_type = form.cleaned_data["adjustment_type"]
                quantity = form.cleaned_data["quantity"]
                reason = form.cleaned_data["reason"] or "Bulk stock adjustment via admin"

                updated_count = 0
                for stock_item in queryset:
                    try:
                        if adjustment_type == "add":
                            stock_item.adjust_stock(quantity, reason=reason)
                        elif adjustment_type == "remove":
                            stock_item.adjust_stock(-quantity, reason=reason)
                        elif adjustment_type == "set":
                            # Calculate adjustment needed
                            adjustment = quantity - stock_item.on_hand
                            stock_item.adjust_stock(adjustment, reason=reason)
                        updated_count += 1
                    except Exception as e:
                        messages.error(request, f"Error adjusting {stock_item}: {e}")

                messages.success(
                    request, f"Successfully adjusted stock for {updated_count} item(s)"
                )
                return redirect(request.get_full_path())
        else:
            form = StockAdjustmentForm()

        # Render intermediate page with form
        return render(
            request,
            "admin/catalog/stock_adjustment.html",
            {
                "form": form,
                "stock_items": queryset,
                "title": _("Adjust Stock Levels"),
                "opts": self.model._meta,
                "action_checkbox_name": admin.helpers.ACTION_CHECKBOX_NAME,
            },
        )

    adjust_stock_action.short_description = _("Adjust stock levels")

    def export_stock_report(self, request, queryset):
        """Export stock report to CSV"""
        import csv

        from django.http import HttpResponse
        from django.utils import timezone

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            f'attachment; filename="stock_report_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        )

        writer = csv.writer(response)
        writer.writerow(
            [
                "Product",
                "SKU",
                "Warehouse",
                "Region",
                "On Hand",
                "Allocated",
                "Available",
                "Low Stock Threshold",
                "Status",
                "Last Updated",
            ]
        )

        for stock_item in queryset.select_related("product", "warehouse", "warehouse__region"):
            available = stock_item.available
            if available <= 0:
                status = "Out of Stock"
            elif available <= stock_item.low_stock_threshold:
                status = "Low Stock"
            else:
                status = "In Stock"

            writer.writerow(
                [
                    stock_item.product.name,
                    stock_item.product.sku,
                    stock_item.warehouse.name,
                    stock_item.warehouse.region.name if stock_item.warehouse.region else "",
                    stock_item.on_hand,
                    stock_item.allocated,
                    available,
                    stock_item.low_stock_threshold,
                    status,
                    stock_item.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                ]
            )

        return response

    export_stock_report.short_description = _("Export stock report (CSV)")

    def mark_for_reorder(self, request, queryset):
        """Mark low stock items for reorder"""
        from django.contrib import messages

        low_stock_items = []
        for stock_item in queryset:
            if stock_item.available <= stock_item.low_stock_threshold:
                low_stock_items.append(stock_item)

        if low_stock_items:
            # In a real system, this could trigger purchase orders or notifications
            # For now, just show a message with the list
            items_list = ", ".join(
                [f"{item.product.name} ({item.warehouse.code})" for item in low_stock_items]
            )
            messages.warning(
                request,
                _(f"{len(low_stock_items)} low stock item(s) marked for reorder: {items_list}"),
            )
        else:
            messages.info(request, _("No low stock items in selection"))

    mark_for_reorder.short_description = _("Mark low stock items for reorder")

    def changelist_view(self, request, extra_context=None):
        """Add summary statistics to the change list"""
        extra_context = extra_context or {}

        # Get filtered queryset
        from django.contrib.admin.views.main import ChangeList

        cl = ChangeList(
            request,
            self.model,
            self.list_display,
            self.list_display_links,
            self.list_filter,
            self.date_hierarchy,
            self.search_fields,
            self.list_select_related,
            self.list_per_page,
            self.list_max_show_all,
            self.list_editable,
            self,
            self.sortable_by,
            self.search_help_text,
        )
        queryset = cl.get_queryset(request)

        # Calculate statistics
        from django.db.models import F, Sum

        total_items = queryset.count()
        total_on_hand = queryset.aggregate(Sum("on_hand"))["on_hand__sum"] or 0
        total_allocated = queryset.aggregate(Sum("allocated"))["allocated__sum"] or 0
        total_available = total_on_hand - total_allocated

        low_stock_count = queryset.filter(on_hand__lte=F("low_stock_threshold")).count()
        out_of_stock_count = queryset.filter(on_hand__lte=F("allocated")).count()

        extra_context["stock_summary"] = {
            "total_items": total_items,
            "total_on_hand": total_on_hand,
            "total_allocated": total_allocated,
            "total_available": total_available,
            "low_stock_count": low_stock_count,
            "out_of_stock_count": out_of_stock_count,
        }

        # Add warehouses for filter dropdown
        extra_context["warehouses"] = Warehouse.objects.filter(is_active=True).order_by("name")

        return super().changelist_view(request, extra_context=extra_context)


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    """Admin for stock movements (audit trail)"""

    change_list_template = "admin/catalog/stockmovement/change_list.html"
    list_display = [
        "created_at",
        "stock_item",
        "movement_type",
        "quantity",
        "previous_quantity",
        "new_quantity",
        "user",
        "order",
    ]
    list_filter = ["movement_type", "created_at", "stock_item__warehouse"]
    search_fields = [
        "stock_item__product__name",
        "stock_item__product__sku",
        "reason",
        "order__order_number",
    ]
    readonly_fields = [
        "created_at",
        "stock_item",
        "movement_type",
        "quantity",
        "previous_quantity",
        "new_quantity",
        "reason",
        "order",
        "user",
    ]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]
    list_select_related = ["stock_item__product", "stock_item__warehouse", "user", "order"]

    fieldsets = (
        (
            _("Movement Details"),
            {"fields": ("created_at", "stock_item", "movement_type", "quantity")},
        ),
        (_("Stock Levels"), {"fields": ("previous_quantity", "new_quantity")}),
        (_("Context"), {"fields": ("reason", "order", "user")}),
    )

    def has_add_permission(self, request):
        """Prevent manual creation - movements are auto-created"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion - immutable audit trail"""
        return False

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        qs = StockMovement.objects.all()
        extra_context["all_count"] = qs.count()
        extra_context["adjustment_count"] = qs.filter(movement_type="adjustment").count()
        extra_context["allocation_count"] = qs.filter(movement_type="allocation").count()
        extra_context["fulfillment_count"] = qs.filter(movement_type="fulfillment").count()
        extra_context["return_count"] = qs.filter(movement_type="return").count()

        # Handle custom filter tabs
        movement_type = request.GET.get("movement_type")
        if movement_type:
            request.GET = request.GET.copy()
            request.GET["movement_type__exact"] = movement_type

        return super().changelist_view(request, extra_context=extra_context)


@admin.register(ProductRegionVisibility)
class ProductRegionVisibilityAdmin(admin.ModelAdmin):
    """Admin for product region visibility"""

    list_display = ["product", "region", "is_visible"]
    list_filter = ["region", "is_visible"]
    search_fields = ["product__name", "product__sku", "region__name"]

    fieldsets = (
        (_("Product & Region"), {"fields": ("product", "region")}),
        (
            _("Visibility"),
            {
                "fields": ("is_visible",),
                "description": _(
                    "Controls whether this product appears in this region. If no rules exist for a product, it is visible in all regions by default."
                ),
            },
        ),
    )


# ============================================================================
# Digital Products Admin
# ============================================================================


@admin.register(LicenseKey)
class LicenseKeyAdmin(admin.ModelAdmin):
    """Admin for license keys with bulk generation and management actions"""

    change_list_template = "admin/catalog/licensekey/change_list.html"

    list_display = [
        "key_display",
        "digital_asset_link",
        "user_link",
        "order_link",
        "key_type",
        "status_badge",
        "activation_status",
        "issued_at",
    ]
    list_filter = ["status", "key_type", "issued_at", "expires_at"]
    search_fields = [
        "key",
        "user__email",
        "user__username",
        "order_item__order__order_number",
        "digital_asset__filename",
        "digital_asset__product__name",
    ]
    readonly_fields = [
        "key",
        "order_item",
        "digital_asset",
        "user",
        "current_activations",
        "issued_at",
        "activation_list_display",
    ]
    date_hierarchy = "issued_at"
    ordering = ["-issued_at"]
    actions = [
        "activate_licenses",
        "deactivate_licenses",
        "revoke_licenses",
        "export_license_keys",
        "regenerate_license_keys",
        "resend_license_email",
    ]

    fieldsets = (
        (_("License Key"), {"fields": ("key", "key_type", "status")}),
        (_("Associated Records"), {"fields": ("digital_asset", "order_item", "user")}),
        (
            _("Activation Limits"),
            {
                "fields": ("max_activations", "current_activations", "activation_list_display"),
                "description": _("Maximum number of devices this license can be activated on."),
            },
        ),
        (_("Expiration"), {"fields": ("expires_at",), "classes": ("collapse",)}),
        (_("Timestamps"), {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def key_display(self, obj):
        """Display license key with copy button"""
        from django.utils.html import format_html

        return format_html(
            '<div style="display: flex; align-items: center; gap: 8px;">'
            '<code style="font-family: monospace; background: var(--darkened-bg, #f8f9fa); '
            'padding: 4px 8px; border-radius: 4px; font-size: 13px;">{}</code>'
            '<button type="button" class="copy-license-key" data-key="{}" '
            'style="padding: 4px 8px; font-size: 11px; cursor: pointer;" '
            'title="Copy to clipboard">📋</button>'
            "</div>",
            obj.key,
            obj.key,
        )

    key_display.short_description = _("License Key")

    def digital_asset_link(self, obj):
        """Link to digital asset"""
        from django.urls import reverse
        from django.utils.html import format_html

        if obj.digital_asset:
            url = reverse("admin:catalog_digitalasset_change", args=[obj.digital_asset.id])
            return format_html(
                '<a href="{}">{}</a><br><small style="color: #666;">{}</small>',
                url,
                obj.digital_asset.filename,
                obj.digital_asset.product.name,
            )
        return "-"

    digital_asset_link.short_description = _("Digital Asset")

    def user_link(self, obj):
        """Link to user"""
        from django.urls import reverse
        from django.utils.html import format_html

        if obj.user:
            try:
                url = reverse("admin:accounts_customuser_change", args=[obj.user.id])
                return format_html('<a href="{}">{}</a>', url, obj.user.email)
            except Exception:
                return obj.user.email
        return "-"

    user_link.short_description = _("User")

    def order_link(self, obj):
        """Link to order"""
        from django.urls import reverse
        from django.utils.html import format_html

        if obj.order_item and obj.order_item.order:
            try:
                url = reverse("admin:orders_order_change", args=[obj.order_item.order.id])
                return format_html('<a href="{}">{}</a>', url, obj.order_item.order.order_number)
            except Exception:
                return obj.order_item.order.order_number
        return "-"

    order_link.short_description = _("Order")

    def status_badge(self, obj):
        """Display status with color badge"""
        from django.utils.html import format_html

        status_colors = {
            "active": "#28a745",
            "expired": "#dc3545",
            "revoked": "#6c757d",
            "suspended": "#ffc107",
        }

        color = status_colors.get(obj.status, "#6c757d")

        return format_html(
            '<span style="display: inline-block; padding: 4px 12px; '
            "background: {}; color: white; border-radius: 12px; "
            'font-size: 12px; font-weight: 500;">{}</span>',
            color,
            obj.get_status_display(),
        )

    status_badge.short_description = _("Status")

    def activation_status(self, obj):
        """Display activation count with visual indicator"""
        from django.utils.html import format_html

        if obj.max_activations is None:
            return format_html('<span style="color: #28a745;">♾️ Unlimited</span>')

        percentage = (
            (obj.current_activations / obj.max_activations * 100) if obj.max_activations > 0 else 0
        )

        if percentage >= 100:
            color = "#dc3545"
            icon = "🔴"
        elif percentage >= 80:
            color = "#ffc107"
            icon = "⚠️"
        else:
            color = "#28a745"
            icon = "✅"

        return format_html(
            '<span style="color: {};">{} {}/{}</span>',
            color,
            icon,
            obj.current_activations,
            obj.max_activations,
        )

    activation_status.short_description = _("Activations")

    def activation_list_display(self, obj):
        """Display list of device activations"""
        from django.utils.html import format_html

        if obj.pk:
            activations = obj.activations.filter(status="active").order_by("-activated_at")

            if not activations.exists():
                return format_html(
                    '<em style="color: #999;">{}</em>', _("No active device activations")
                )

            rows = []
            for activation in activations:
                rows.append(
                    f"<tr>"
                    f'<td style="padding: 6px 8px;">{activation.device_name or "Unknown Device"}</td>'
                    f'<td style="padding: 6px 8px; font-size: 11px; color: #666;">'
                    f"{activation.device_fingerprint[:16]}...</td>"
                    f'<td style="padding: 6px 8px; font-size: 11px;">{activation.activated_at.strftime("%Y-%m-%d %H:%M")}</td>'
                    f"</tr>"
                )

            return format_html(
                '<table style="width: 100%; border-collapse: collapse; font-size: 12px;">'
                '<thead><tr style="background: var(--darkened-bg, #f8f9fa);">'
                '<th style="padding: 6px 8px; text-align: left;">Device</th>'
                '<th style="padding: 6px 8px; text-align: left;">Fingerprint</th>'
                '<th style="padding: 6px 8px; text-align: left;">Activated</th>'
                "</tr></thead>"
                "<tbody>{}</tbody>"
                "</table>",
                "".join(rows),
            )
        return "-"

    activation_list_display.short_description = _("Active Devices")

    # Bulk Actions

    def activate_licenses(self, request, queryset):
        """Bulk activate selected license keys"""
        updated = queryset.update(status="active")
        self.message_user(request, _(f"{updated} license key(s) activated successfully."))

    activate_licenses.short_description = _("✅ Activate selected license keys")

    def deactivate_licenses(self, request, queryset):
        """Bulk deactivate selected license keys"""
        updated = queryset.update(status="suspended")
        self.message_user(request, _(f"{updated} license key(s) suspended successfully."))

    deactivate_licenses.short_description = _("⏸️ Suspend selected license keys")

    def revoke_licenses(self, request, queryset):
        """Bulk revoke selected license keys"""
        updated = queryset.update(status="revoked")
        # Also deactivate all device activations
        for license_key in queryset:
            license_key.activations.filter(status="active").update(status="deactivated")
        self.message_user(
            request, _(f"{updated} license key(s) revoked and all device activations removed.")
        )

    revoke_licenses.short_description = _("🚫 Revoke selected license keys")

    def export_license_keys(self, request, queryset):
        """Export selected license keys to CSV"""
        import csv

        from django.http import HttpResponse
        from django.utils import timezone

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            f'attachment; filename="license_keys_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        )

        writer = csv.writer(response)
        writer.writerow(
            [
                "License Key",
                "Product",
                "Asset",
                "Customer Email",
                "Order Number",
                "Status",
                "Type",
                "Max Activations",
                "Current Activations",
                "Created",
                "Expires",
            ]
        )

        for license_key in queryset.select_related(
            "digital_asset", "digital_asset__product", "user", "order_item__order"
        ):
            writer.writerow(
                [
                    license_key.key,
                    license_key.digital_asset.product.name if license_key.digital_asset else "",
                    license_key.digital_asset.filename if license_key.digital_asset else "",
                    license_key.user.email if license_key.user else "",
                    license_key.order_item.order.order_number
                    if license_key.order_item and license_key.order_item.order
                    else "",
                    license_key.get_status_display(),
                    license_key.get_key_type_display(),
                    license_key.max_activations if license_key.max_activations else "Unlimited",
                    license_key.current_activations,
                    license_key.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    license_key.expires_at.strftime("%Y-%m-%d")
                    if license_key.expires_at
                    else "Never",
                ]
            )

        return response

    export_license_keys.short_description = _("📥 Export selected license keys to CSV")

    def regenerate_license_keys(self, request, queryset):
        """Regenerate selected license keys (creates new keys, marks old as revoked)"""
        import hashlib
        import os

        from django.contrib import messages

        regenerated = 0
        for old_license in queryset:
            # Mark old license as revoked
            old_license.status = "revoked"
            old_license.save()

            # Generate new license key
            unique_string = f"{old_license.order_item.id}-{old_license.digital_asset.id}-{os.urandom(16).hex()}-regenerated"
            hash_digest = hashlib.sha256(unique_string.encode()).hexdigest()[:16].upper()
            new_key = "-".join([hash_digest[i : i + 4] for i in range(0, 16, 4)])

            # Create new license
            LicenseKey.objects.create(
                order_item=old_license.order_item,
                digital_asset=old_license.digital_asset,
                user=old_license.user,
                key=new_key,
                key_type=old_license.key_type,
                max_activations=old_license.max_activations,
                status="active",
            )
            regenerated += 1

        messages.success(
            request, _(f"{regenerated} license key(s) regenerated. Old keys have been revoked.")
        )

    regenerate_license_keys.short_description = _("🔄 Regenerate selected license keys")

    def resend_license_email(self, request, queryset):
        """Resend license key delivery email to customers"""
        from django.contrib import messages

        from email_system.services.email_sender import EmailSendingService

        sent_count = 0
        failed_count = 0

        for license_key in queryset.select_related(
            "user", "digital_asset__product", "order_item__order"
        ):
            # Must have a user/email to send to
            if not license_key.user or not license_key.user.email:
                failed_count += 1
                continue

            # Build context for email template
            context = {
                "customer_name": license_key.user.get_full_name() or license_key.user.username,
                "license_key": license_key.key,
                "product_name": license_key.digital_asset.product.name
                if license_key.digital_asset
                else "Digital Product",
                "order_number": license_key.order_item.order.order_number
                if license_key.order_item and license_key.order_item.order
                else "",
                "license_type": license_key.get_key_type_display(),
                "max_activations": license_key.max_activations or "Unlimited",
                "is_lifetime": license_key.expires_at is None,
                "expiration_date": license_key.expires_at.strftime("%B %d, %Y")
                if license_key.expires_at
                else None,
            }

            try:
                from email_system.utils.language import get_user_email_language

                outbox = EmailSendingService.send_template_email(
                    to_email=license_key.user.email,
                    template_type="digital_product_license_key",
                    context=context,
                    language=get_user_email_language(license_key.user),
                )

                # Try to send immediately
                if outbox and outbox.status == "queued":
                    EmailSendingService.send_email(str(outbox.id))
                    sent_count += 1
                elif outbox and outbox.status == "skipped":
                    logger.info(
                        f"License email skipped for {license_key.key}: {outbox.skip_reason}"
                    )
                    failed_count += 1

            except Exception as e:
                logger.error(f"Failed to resend license email for {license_key.key}: {e}")
                failed_count += 1

        if sent_count > 0:
            messages.success(
                request, _(f"Successfully sent license key email to {sent_count} customer(s).")
            )
        if failed_count > 0:
            messages.warning(
                request,
                _(
                    f"Failed to send email for {failed_count} license key(s). Check that customers have valid email addresses."
                ),
            )

    resend_license_email.short_description = _("📧 Resend license key email")

    def changelist_view(self, request, extra_context=None):
        """Add custom context data for the license key list view"""
        extra_context = extra_context or {}

        # Get all products with digital assets that require licenses
        digital_products = (
            Product.objects.filter(digital_assets__requires_license=True)
            .distinct()
            .order_by("name")
        )

        extra_context["digital_products"] = digital_products

        return super().changelist_view(request, extra_context=extra_context)

    class Media:
        css = {"all": ("catalog/css/admin_license_key.css",)}
        js = ("catalog/js/admin_license_key.js",)


@admin.register(LicenseKeyTemplate)
class LicenseKeyTemplateAdmin(admin.ModelAdmin):
    """Admin for license key templates with live preview"""

    change_list_template = "admin/catalog/licensekeytemplate/change_list.html"

    list_display = [
        "name",
        "pattern_preview",
        "sample_key_preview",
        "products_count",
        "is_active",
        "created_at",
    ]
    list_filter = ["is_active", "created_at"]
    search_fields = ["name", "description", "pattern"]
    readonly_fields = ["created_at", "updated_at", "created_by", "sample_key_display"]

    fieldsets = (
        (_("Basic Information"), {"fields": ("name", "description", "is_active")}),
        (
            _("Pattern Configuration"),
            {
                "fields": ("pattern", "prefix", "suffix", "separator", "character_set"),
                "description": _(
                    "Define the license key format using placeholders:<br>"
                    "• <code>{RANDOM:N}</code> - N random characters<br>"
                    "• <code>{CHECKSUM:N}</code> - N-digit checksum<br>"
                    "• <code>{PREFIX}</code> - Template prefix<br>"
                    "• <code>{SUFFIX}</code> - Template suffix<br>"
                    "• <code>{ORDER_ID}</code> - Order number<br>"
                    "• <code>{PRODUCT_SKU}</code> - Product SKU<br>"
                    "• <code>{DATE:FORMAT}</code> - Date (YYMMDD, YYYYMMDD, etc.)"
                ),
            },
        ),
        (_("Validation Rules"), {"fields": ("min_length", "max_length")}),
        (
            _("Preview"),
            {
                "fields": ("sample_key_display",),
                "description": _("Sample license keys generated with this template"),
            },
        ),
        (
            _("Metadata"),
            {"fields": ("created_at", "updated_at", "created_by"), "classes": ("collapse",)},
        ),
    )

    def pattern_preview(self, obj):
        """Show pattern with syntax highlighting"""
        import re

        from django.utils.html import format_html
        from django.utils.safestring import mark_safe

        pattern = obj.pattern
        # Highlight placeholders
        pattern = re.sub(
            r"\{([A-Z_:]+)\}",
            r'<span style="color: #0066cc; font-weight: bold;">{\1}</span>',
            pattern,
        )
        return format_html("<code>{}</code>", mark_safe(pattern))

    pattern_preview.short_description = _("Pattern")

    def sample_key_preview(self, obj):
        """Generate and display sample key"""
        from django.utils.html import format_html

        try:
            sample = obj.generate_sample_key({"order_id": 12345, "product_sku": "SW001"})
            return format_html(
                '<code style="background: #f0f0f0; padding: 4px 8px; border-radius: 3px;">{}</code>',
                sample,
            )
        except Exception as e:
            return format_html('<span style="color: red;">Error: {}</span>', str(e))

    sample_key_preview.short_description = _("Sample Key")

    def sample_key_display(self, obj):
        """Detailed sample key display in form"""
        from django.utils.html import format_html
        from django.utils.safestring import mark_safe

        if not obj.pk:
            return _("Save template to see sample")

        try:
            samples = []
            for i in range(3):
                key = obj.generate_sample_key(
                    {"order_id": 12340 + i, "product_sku": f"SW00{i + 1}"}
                )
                samples.append(f"<li><code>{key}</code></li>")

            return format_html(
                '<ul style="list-style: none; padding: 0;">{}</ul>', mark_safe("".join(samples))
            )
        except Exception as e:
            return format_html('<span style="color: red;">Error: {}</span>', str(e))

    sample_key_display.short_description = _("Sample Keys")

    def products_count(self, obj):
        """Count products using this template"""
        from django.urls import reverse
        from django.utils.html import format_html

        count = obj.products.count()
        if count > 0:
            url = (
                reverse("admin:catalog_product_changelist")
                + f"?license_template__id__exact={obj.pk}"
            )
            return format_html('<a href="{}">{} products</a>', url, count)
        return "0 products"

    products_count.short_description = _("Usage")

    def save_model(self, request, obj, form, change):
        """Set created_by on creation"""
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    class Media:
        css = {"all": ("catalog/css/admin_license_template.css",)}
        js = ("catalog/js/admin_license_template.js",)


@admin.register(LicenseProvider)
class LicenseProviderAdmin(admin.ModelAdmin):
    """Admin for external license providers"""

    # Use custom change_list template for card view
    change_list_template = "admin/catalog/licenseprovider/change_list.html"
    # Use custom change_form template for product mapping UI
    change_form_template = "admin/catalog/licenseprovider/change_form.html"

    # Show all providers on one page for client-side filtering
    list_per_page = 1000

    list_display = [
        "name",
        "provider_type_display",
        "connection_status_badge",
        "is_active_badge",
        "sync_status_display",
        "last_tested_at",
        "created_at",
    ]
    list_filter = ["provider_type", "is_active", "connection_status", "created_at"]
    search_fields = ["name", "api_endpoint"]
    readonly_fields = [
        "connection_status_badge",
        "connection_error_display",
        "last_tested_at",
        "created_at",
        "updated_at",
    ]
    actions = ["test_provider_connections", "enable_providers", "disable_providers"]

    class Media:
        css = {"all": ("catalog/css/admin_license_provider.css",)}

    fieldsets = (
        (_("Basic Information"), {"fields": ("name", "provider_type", "is_active")}),
        (
            _("API Configuration"),
            {
                "fields": ("api_endpoint", "api_key", "api_secret"),
                "description": _(
                    "API credentials for connecting to external license provider. Keep these secure!"
                ),
            },
        ),
        (
            _("Synchronization Settings"),
            {
                "fields": (
                    "sync_on_order",
                    "sync_on_activation",
                    "sync_on_deactivation",
                    "sync_bidirectional",
                )
            },
        ),
        (
            _("Webhook Configuration"),
            {"fields": ("webhook_secret", "webhook_events"), "classes": ("collapse",)},
        ),
        (
            _("Provider Configuration"),
            {
                "fields": ("provider_config", "product_mapping"),
                "description": _("Provider-specific settings and product mapping"),
                "classes": ("collapse",),
            },
        ),
        (
            _("Connection Status"),
            {
                "fields": ("connection_status_badge", "connection_error_display", "last_tested_at"),
                "classes": ("collapse",),
            },
        ),
        (_("Metadata"), {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def provider_type_display(self, obj):
        """Display provider type with icon"""
        from django.utils.html import format_html

        return format_html("<span>{}</span>", obj.get_provider_type_display())

    provider_type_display.short_description = _("Provider Type")

    def connection_status_badge(self, obj):
        """Display connection status with color coding"""
        from django.utils.html import format_html

        colors = {"not_tested": "#6C757D", "connected": "#28A745", "error": "#DC3545"}
        color = colors.get(obj.connection_status, "#6C757D")

        status_text = obj.get_connection_status_display().upper()

        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-weight: bold; font-size: 11px;">{}</span>',
            color,
            status_text,
        )

    connection_status_badge.short_description = _("Connection")

    def connection_error_display(self, obj):
        """Display connection error message"""
        from django.utils.html import format_html

        if obj.connection_error:
            return format_html(
                '<div class="messagelist"><li class="error">'
                '<i class="fas fa-exclamation-circle"></i> {}'
                "</li></div>",
                obj.connection_error,
            )
        elif obj.connection_status == "connected":
            return format_html(
                '<div class="messagelist"><li class="success">'
                '<i class="fas fa-check-circle"></i> {}'
                "</li></div>",
                _("Connection successful"),
            )
        return format_html(
            '<div class="messagelist"><li class="info">'
            '<i class="fas fa-info-circle"></i> {}'
            "</li></div>",
            _("Connection not tested yet"),
        )

    connection_error_display.short_description = _("Connection Details")

    def is_active_badge(self, obj):
        """Display active status badge"""
        from django.utils.html import format_html

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

    def sync_status_display(self, obj):
        """Display sync configuration status"""
        from django.utils.html import format_html

        syncs = []
        if obj.sync_on_order:
            syncs.append("Order")
        if obj.sync_on_activation:
            syncs.append("Activation")
        if obj.sync_on_deactivation:
            syncs.append("Deactivation")

        if syncs:
            return format_html('<span style="color: #28a745;">✓ {}</span>', ", ".join(syncs))
        return format_html('<span style="color: #999;">No sync enabled</span>')

    sync_status_display.short_description = _("Sync Events")

    @admin.action(description=_("Test connection to selected providers"))
    def test_provider_connections(self, request, queryset):
        """Test connection for selected providers"""
        from django.contrib import messages

        from catalog.services import LicenseProviderService

        results = []
        for provider in queryset:
            service = LicenseProviderService(provider)

            if service.adapter and hasattr(service.adapter, "test_connection"):
                result = service.adapter.test_connection()

                if result["success"]:
                    provider.connection_status = "connected"
                    provider.connection_error = ""
                    results.append(f"✓ {provider.name}: Connected")
                else:
                    provider.connection_status = "error"
                    provider.connection_error = result["error"]
                    results.append(f"✗ {provider.name}: {result['error']}")

                provider.last_tested_at = timezone.now()
                provider.save()
            else:
                results.append(f"⚠ {provider.name}: No test available")

        messages.info(request, "\n".join(results))

    @admin.action(description=_("Enable selected providers"))
    def enable_providers(self, request, queryset):
        """Enable selected providers"""
        from django.contrib import messages

        count = queryset.update(is_active=True)
        messages.success(request, _(f"Enabled {count} provider(s)"))

    @admin.action(description=_("Disable selected providers"))
    def disable_providers(self, request, queryset):
        """Disable selected providers"""
        from django.contrib import messages

        count = queryset.update(is_active=False)
        messages.success(request, _(f"Disabled {count} provider(s)"))

    def changelist_view(self, request, extra_context=None):
        """Add custom context data for the provider list view"""
        from catalog.providers.registry import LicenseProviderRegistry

        extra_context = extra_context or {}

        # Get all provider accounts
        all_providers = self.get_queryset(request)

        # Discover available providers from registry
        LicenseProviderRegistry.discover_providers()
        available_providers = LicenseProviderRegistry.list_providers()

        # Add provider metadata
        for provider in all_providers:
            provider_class = LicenseProviderRegistry.get_provider(provider.provider_type)
            if provider_class:
                provider.provider_class = provider_class
                provider.provider_display_name = provider_class.provider_name

                # Add logo from registry
                provider_meta = next(
                    (p for p in available_providers if p["key"] == provider.provider_type), None
                )
                if provider_meta and provider_meta.get("logo"):
                    provider.logo_path = provider_meta["logo"]
                else:
                    provider.logo_path = None

        # Status counts
        extra_context["active_count"] = all_providers.filter(is_active=True).count()
        extra_context["inactive_count"] = all_providers.filter(is_active=False).count()

        # Connection status counts
        extra_context["connected_count"] = all_providers.filter(
            connection_status="connected"
        ).count()
        extra_context["error_count"] = all_providers.filter(connection_status="error").count()
        extra_context["not_tested_count"] = all_providers.filter(
            connection_status="not_tested"
        ).count()

        # Available provider types
        extra_context["available_providers"] = available_providers

        return super().changelist_view(request, extra_context=extra_context)


@admin.register(ExternalLicenseSync)
class ExternalLicenseSyncAdmin(admin.ModelAdmin):
    """Admin for external license sync operations"""

    change_list_template = "admin/catalog/externallicensesync/change_list.html"

    list_display = [
        "license_key_display",
        "provider",
        "external_id",
        "sync_direction",
        "status_badge",
        "synced_at",
        "retry_count",
    ]
    list_filter = ["sync_status", "sync_direction", "provider", "synced_at"]
    search_fields = ["license_key__key", "external_id", "error_message"]
    readonly_fields = ["license_key", "provider", "synced_at", "external_data_display"]
    date_hierarchy = "synced_at"

    fieldsets = (
        (
            _("Sync Information"),
            {"fields": ("license_key", "provider", "sync_direction", "sync_status")},
        ),
        (_("External Reference"), {"fields": ("external_id", "external_data_display")}),
        (_("Error Details"), {"fields": ("error_message",), "classes": ("collapse",)}),
        (
            _("Retry Information"),
            {"fields": ("retry_count", "next_retry_at"), "classes": ("collapse",)},
        ),
        (_("Timestamps"), {"fields": ("synced_at",), "classes": ("collapse",)}),
    )

    def license_key_display(self, obj):
        """Display license key with link"""
        from django.urls import reverse
        from django.utils.html import format_html

        url = reverse("admin:catalog_licensekey_change", args=[obj.license_key.id])
        return format_html('<a href="{}">{}</a>', url, obj.license_key.key[:20] + "...")

    license_key_display.short_description = _("License Key")

    def status_badge(self, obj):
        """Display status with color badge"""
        from django.utils.html import format_html

        colors = {
            "success": "#28a745",
            "failed": "#dc3545",
            "pending": "#ffc107",
        }
        color = colors.get(obj.sync_status, "#6c757d")

        return format_html(
            '<span style="background: {}; color: white; padding: 4px 12px; '
            'border-radius: 12px; font-size: 12px;">{}</span>',
            color,
            obj.get_sync_status_display(),
        )

    status_badge.short_description = _("Status")

    def external_data_display(self, obj):
        """Display external data as formatted JSON"""
        import json

        from django.utils.html import format_html

        if obj.external_data:
            formatted = json.dumps(obj.external_data, indent=2)
            return format_html(
                '<pre style="max-height: 300px; overflow: auto;">{}</pre>', formatted
            )
        return "-"

    external_data_display.short_description = _("External Response Data")

    def changelist_view(self, request, extra_context=None):
        """Add providers to context for filters"""
        extra_context = extra_context or {}

        # Get all providers
        from .models import LicenseProvider

        providers = LicenseProvider.objects.all().order_by("name")

        extra_context["providers"] = providers
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(WebhookSubscription)
class WebhookSubscriptionAdmin(admin.ModelAdmin):
    """Admin for webhook subscriptions"""

    list_display = [
        "name",
        "url",
        "events_display",
        "delivery_stats",
        "is_active",
        "last_delivery_at",
    ]
    list_filter = ["is_active", "created_at"]
    search_fields = ["name", "url"]
    filter_horizontal = ["product_filter"]
    readonly_fields = [
        "total_deliveries",
        "successful_deliveries",
        "failed_deliveries",
        "last_delivery_at",
        "created_at",
        "updated_at",
    ]

    fieldsets = (
        (_("Basic Information"), {"fields": ("name", "url", "secret", "is_active")}),
        (
            _("Event Configuration"),
            {"fields": ("events",), "description": _("Select which license events to receive")},
        ),
        (
            _("Filtering"),
            {
                "fields": ("product_filter", "license_type_filter"),
                "description": _("Filter events by product or license type (empty = all)"),
                "classes": ("collapse",),
            },
        ),
        (
            _("Delivery Settings"),
            {"fields": ("max_retries", "retry_delay_seconds"), "classes": ("collapse",)},
        ),
        (
            _("Statistics"),
            {
                "fields": (
                    "total_deliveries",
                    "successful_deliveries",
                    "failed_deliveries",
                    "last_delivery_at",
                ),
                "classes": ("collapse",),
            },
        ),
        (_("Metadata"), {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def events_display(self, obj):
        """Display subscribed events"""
        if obj.events:
            return ", ".join(obj.events[:3]) + ("..." if len(obj.events) > 3 else "")
        return "None"

    events_display.short_description = _("Events")

    def delivery_stats(self, obj):
        """Display delivery statistics"""
        from django.utils.html import format_html

        if obj.total_deliveries > 0:
            success_rate = (obj.successful_deliveries / obj.total_deliveries) * 100
            color = (
                "#28a745"
                if success_rate >= 95
                else ("#ffc107" if success_rate >= 80 else "#dc3545")
            )
            return format_html(
                '<span style="color: {};">{}/{} ({:.1f}%)</span>',
                color,
                obj.successful_deliveries,
                obj.total_deliveries,
                success_rate,
            )
        return format_html('<span style="color: #999;">No deliveries yet</span>')

    delivery_stats.short_description = _("Success Rate")


@admin.register(LicensePool)
class LicensePoolAdmin(admin.ModelAdmin):
    """Admin for license pools with bulk generation"""

    change_list_template = "admin/catalog/licensepool/change_list.html"

    list_display = [
        "name",
        "product",
        "status_badge",
        "progress_display",
        "keys_stats",
        "created_at",
    ]
    list_filter = ["status", "key_type", "created_at"]
    search_fields = ["name", "product__name", "product__sku"]
    readonly_fields = [
        "keys_generated",
        "keys_distributed",
        "status",
        "progress_display",
        "available_keys_display",
        "generation_started_at",
        "generation_completed_at",
        "generation_error",
        "created_at",
        "updated_at",
    ]
    autocomplete_fields = ["product", "license_template", "sync_to_provider", "created_by"]
    date_hierarchy = "created_at"
    actions = ["generate_pool_keys", "export_pool_keys", "reset_pool_status"]

    fieldsets = (
        (_("Basic Information"), {"fields": ("name", "description", "product")}),
        (
            _("License Configuration"),
            {
                "fields": (
                    "license_template",
                    "key_type",
                    "max_activations",
                    "expires_after_days",
                    "pool_expires_at",
                )
            },
        ),
        (
            _("Pool Configuration"),
            {"fields": ("total_keys", "keys_generated", "keys_distributed", "status")},
        ),
        (
            _("Progress"),
            {"fields": ("progress_display", "available_keys_display"), "classes": ("collapse",)},
        ),
        (_("External Sync"), {"fields": ("sync_to_provider",), "classes": ("collapse",)}),
        (
            _("Generation Status"),
            {
                "fields": ("generation_started_at", "generation_completed_at", "generation_error"),
                "classes": ("collapse",),
            },
        ),
        (
            _("Metadata"),
            {"fields": ("created_at", "updated_at", "created_by"), "classes": ("collapse",)},
        ),
    )

    def status_badge(self, obj):
        """Display status with color badge"""
        from django.utils.html import format_html

        colors = {
            "generating": "#ffc107",
            "ready": "#28a745",
            "depleted": "#dc3545",
            "expired": "#6c757d",
        }
        color = colors.get(obj.status, "#999")

        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display(),
        )

    status_badge.short_description = _("Status")

    def progress_display(self, obj):
        """Display generation progress"""
        from django.utils.html import format_html

        progress = obj.progress_percentage
        color = "#28a745" if progress == 100 else ("#ffc107" if progress > 0 else "#999")

        return format_html(
            '<div style="width: 200px; background: #f0f0f0; border-radius: 10px; overflow: hidden;">'
            '<div style="width: {}%; background: {}; padding: 4px 0; text-align: center; color: white; font-size: 11px; font-weight: bold;">'
            "{}%"
            "</div></div>",
            progress,
            color,
            progress,
        )

    progress_display.short_description = _("Progress")

    def keys_stats(self, obj):
        """Display key statistics"""
        from django.utils.html import format_html

        return format_html(
            '<strong>{}</strong> generated | <strong>{}</strong> distributed | <strong style="color: #28a745;">{}</strong> available',
            obj.keys_generated,
            obj.keys_distributed,
            obj.available_keys_count,
        )

    keys_stats.short_description = _("Keys")

    def available_keys_display(self, obj):
        """Display available keys count"""
        from django.utils.html import format_html

        available = obj.available_keys_count
        color = "#28a745" if available > 10 else ("#ffc107" if available > 0 else "#dc3545")

        return format_html(
            '<span style="color: {}; font-weight: bold; font-size: 14px;">{}</span> keys available',
            color,
            available,
        )

    available_keys_display.short_description = _("Available Keys")

    def save_model(self, request, obj, form, change):
        """Set created_by on new pools"""
        if not obj.pk and not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    # Bulk Admin Actions

    @admin.action(description=_("Generate license keys for selected pools"))
    def generate_pool_keys(self, request, queryset):
        """Bulk action to generate keys for selected pools"""
        from django.contrib import messages
        from django.db import transaction

        from .services.license_generator import LicenseKeyGenerator

        generated_total = 0
        errors = []

        for pool in queryset:
            if pool.status == "depleted":
                errors.append(f"{pool.name}: Pool is depleted")
                continue

            remaining = pool.total_keys - pool.keys_generated
            if remaining <= 0:
                errors.append(f"{pool.name}: All keys already generated")
                continue

            # Update status
            pool.status = "generating"
            pool.generation_started_at = timezone.now()
            pool.save(update_fields=["status", "generation_started_at"])

            # Get template
            template = pool.license_template or pool.product.license_template

            # Generate keys
            generator = LicenseKeyGenerator()
            generated_count = 0

            try:
                with transaction.atomic():
                    for i in range(remaining):
                        context = {
                            "product_sku": pool.product.sku,
                            "pool_id": pool.id,
                            "sequence": pool.keys_generated + i + 1,
                        }

                        key = generator.generate(template, context)

                        LicenseKey.objects.create(
                            license_pool=pool,
                            digital_asset=pool.product.digital_assets.first()
                            if pool.product.digital_assets.exists()
                            else None,
                            key=key,
                            key_type=pool.key_type,
                            max_activations=pool.max_activations,
                            status="active",
                            is_lifetime=(pool.expires_after_days is None),
                        )

                        generated_count += 1
                        pool.keys_generated += 1

                pool.status = "ready"
                pool.generation_completed_at = timezone.now()
                pool.save(update_fields=["keys_generated", "status", "generation_completed_at"])

                generated_total += generated_count

            except Exception as e:
                pool.status = "ready"
                pool.generation_error = str(e)
                pool.save(update_fields=["status", "generation_error"])
                errors.append(f"{pool.name}: {str(e)}")

        if generated_total > 0:
            self.message_user(
                request, f"Successfully generated {generated_total} license keys", messages.SUCCESS
            )

        if errors:
            self.message_user(request, "Errors: " + "; ".join(errors), messages.ERROR)

    @admin.action(description=_("Export pool keys to CSV"))
    def export_pool_keys(self, request, queryset):
        """Export license keys from selected pools to CSV"""
        import csv

        from django.http import HttpResponse

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="license_pool_keys.csv"'

        writer = csv.writer(response)
        writer.writerow(
            ["Pool Name", "License Key", "Key Type", "Max Activations", "Status", "Is Distributed"]
        )

        for pool in queryset:
            keys = LicenseKey.objects.filter(license_pool=pool)
            for key in keys:
                writer.writerow(
                    [
                        pool.name,
                        key.key,
                        key.key_type,
                        key.max_activations,
                        key.status,
                        "Yes" if key.order_item_id else "No",
                    ]
                )

        return response

    @admin.action(description=_("Reset pool status to ready"))
    def reset_pool_status(self, request, queryset):
        """Reset pool status to ready"""
        from django.contrib import messages

        updated = queryset.update(status="ready", generation_error="")
        self.message_user(request, f"Reset {updated} pool(s) to ready status", messages.SUCCESS)

    def changelist_view(self, request, extra_context=None):
        """Add digital products to context for filters"""
        extra_context = extra_context or {}

        # Get all products that have digital assets requiring licenses
        digital_products = (
            Product.objects.filter(digital_assets__requires_license=True)
            .distinct()
            .order_by("name")
        )

        extra_context["digital_products"] = digital_products
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(DigitalAsset)
class DigitalAssetAdmin(admin.ModelAdmin):
    """Standalone admin for digital assets with file management and analytics"""

    change_list_template = "admin/catalog/digitalasset/change_list.html"

    list_display = [
        "filename_display",
        "product_link",
        "version",
        "file_info",
        "download_stats",
        "license_stats",
        "is_active_badge",
        "created_at",
    ]
    list_filter = ["is_active", "requires_license", "created_at", "product__product_type"]
    search_fields = ["filename", "product__name", "product__sku", "file_type"]
    readonly_fields = [
        "file_size",
        "file_type",
        "created_at",
        "updated_at",
        "download_analytics",
        "license_key_analytics",
    ]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]
    autocomplete_fields = ["product"]
    actions = ["activate_assets", "deactivate_assets", "export_asset_report"]

    fieldsets = (
        (_("Product Association"), {"fields": ("product",)}),
        (
            _("File Information"),
            {"fields": ("file", "filename", "version", "file_size", "file_type")},
        ),
        (
            _("License Settings"),
            {
                "fields": ("requires_license", "license_key_analytics"),
                "description": _(
                    "If enabled, license keys will be generated automatically on order completion."
                ),
            },
        ),
        (
            _("Download Settings"),
            {
                "fields": ("download_limit", "expiration_days", "download_analytics"),
                "description": _(
                    "Leave blank for unlimited downloads. Expiration is counted from order date."
                ),
            },
        ),
        (_("Status"), {"fields": ("is_active",)}),
        (_("Timestamps"), {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def filename_display(self, obj):
        """Display filename with icon based on file type"""
        from django.utils.html import format_html

        # Map file types to emojis
        type_icons = {
            "application/zip": "📦",
            "application/pdf": "📄",
            "image": "🖼️",
            "video": "🎥",
            "audio": "🎵",
            "text": "📝",
            "application/x-msdownload": "💾",
        }

        icon = "📁"  # Default
        if obj.file_type:
            for key, emoji in type_icons.items():
                if key in obj.file_type:
                    icon = emoji
                    break

        return format_html(
            '<div style="display: flex; align-items: center; gap: 8px;">'
            '<span style="font-size: 18px;">{}</span>'
            '<span style="font-family: monospace; font-size: 13px;">{}</span>'
            "</div>",
            icon,
            obj.filename,
        )

    filename_display.short_description = _("Filename")

    def product_link(self, obj):
        """Link to product"""
        from django.urls import reverse
        from django.utils.html import format_html

        if obj.product:
            url = reverse("admin:catalog_product_change", args=[obj.product.id])
            return format_html(
                '<a href="{}">{}</a><br><small style="color: #666;">SKU: {}</small>',
                url,
                obj.product.name,
                obj.product.sku,
            )
        return "-"

    product_link.short_description = _("Product")

    def file_info(self, obj):
        """Display file size and type"""
        from django.utils.html import format_html

        size = (
            obj.get_file_size_display()
            if hasattr(obj, "get_file_size_display")
            else f"{obj.file_size / (1024 * 1024):.2f} MB"
        )
        file_type = obj.file_type or _("Unknown")

        return format_html(
            '<div style="font-size: 12px;">'
            '<div style="font-weight: 600;">{}</div>'
            '<div style="color: #666; margin-top: 2px;">{}</div>'
            "</div>",
            size,
            file_type,
        )

    file_info.short_description = _("File Info")

    def download_stats(self, obj):
        """Display download statistics"""
        from django.utils.html import format_html

        if obj.pk:
            total_downloads = DigitalDownload.objects.filter(digital_asset=obj).count()
            completed_downloads = DigitalDownload.objects.filter(
                digital_asset=obj, status="completed"
            ).count()

            if total_downloads == 0:
                return format_html('<em style="color: #999;">{}</em>', _("No downloads"))

            success_rate = (
                (completed_downloads / total_downloads * 100) if total_downloads > 0 else 0
            )

            color = (
                "#28a745" if success_rate >= 90 else "#ffc107" if success_rate >= 70 else "#dc3545"
            )

            return format_html(
                '<div style="font-size: 12px;">'
                '<div style="font-weight: 600;">{} downloads</div>'
                '<div style="color: {}; margin-top: 2px;">{} completed ({:.0f}%)</div>'
                "</div>",
                total_downloads,
                color,
                completed_downloads,
                success_rate,
            )
        return "-"

    download_stats.short_description = _("Downloads")

    def license_stats(self, obj):
        """Display license key statistics"""
        from django.utils.html import format_html

        if obj.pk:
            if not obj.requires_license:
                return format_html('<em style="color: #999;">{}</em>', _("Not required"))

            license_count = LicenseKey.objects.filter(digital_asset=obj).count()
            active_licenses = LicenseKey.objects.filter(digital_asset=obj, status="active").count()

            if license_count == 0:
                return format_html('<em style="color: #999;">{}</em>', _("No keys generated"))

            return format_html(
                '<div style="font-size: 12px;">'
                '<div style="font-weight: 600;">{} keys</div>'
                '<div style="color: #28a745; margin-top: 2px;">{} active</div>'
                "</div>",
                license_count,
                active_licenses,
            )
        return "-"

    license_stats.short_description = _("License Keys")

    def is_active_badge(self, obj):
        """Display active status badge"""
        from django.utils.html import format_html

        if obj.is_active:
            return format_html('<span style="color: #28a745; font-weight: 600;">✓ Active</span>')
        return format_html('<span style="color: #dc3545; font-weight: 600;">✗ Inactive</span>')

    is_active_badge.short_description = _("Status")

    def download_analytics(self, obj):
        """Detailed download analytics in change form"""
        from django.utils.html import format_html

        if obj.pk:
            downloads = DigitalDownload.objects.filter(digital_asset=obj)

            if not downloads.exists():
                return format_html(
                    '<em style="color: #999;">{}</em>', _("No download activity yet")
                )

            total = downloads.count()
            completed = downloads.filter(status="completed").count()
            failed = downloads.filter(status="failed").count()
            in_progress = downloads.filter(status="in_progress").count()

            # Get unique users
            unique_users = downloads.values("user").distinct().count()

            # Recent downloads (last 30 days)
            from datetime import timedelta

            from django.utils import timezone

            thirty_days_ago = timezone.now() - timedelta(days=30)
            recent_downloads = downloads.filter(download_date__gte=thirty_days_ago).count()

            return format_html(
                '<div style="background: var(--darkened-bg, #f8f9fa); padding: 16px; '
                'border-radius: 6px; border: 1px solid var(--hairline-color, #e8e8e8);">'
                '<h4 style="margin: 0 0 12px 0; font-size: 14px;">Download Analytics</h4>'
                '<table style="width: 100%; font-size: 13px; border-collapse: collapse;">'
                '<tr><td style="padding: 6px 0; font-weight: 600;">Total Downloads:</td><td style="padding: 6px 0;">{}</td></tr>'
                '<tr><td style="padding: 6px 0; font-weight: 600; color: #28a745;">Completed:</td><td style="padding: 6px 0;">{}</td></tr>'
                '<tr><td style="padding: 6px 0; font-weight: 600; color: #dc3545;">Failed:</td><td style="padding: 6px 0;">{}</td></tr>'
                '<tr><td style="padding: 6px 0; font-weight: 600; color: #17a2b8;">In Progress:</td><td style="padding: 6px 0;">{}</td></tr>'
                '<tr><td style="padding: 6px 0; font-weight: 600;">Unique Users:</td><td style="padding: 6px 0;">{}</td></tr>'
                '<tr><td style="padding: 6px 0; font-weight: 600;">Last 30 Days:</td><td style="padding: 6px 0;">{}</td></tr>'
                "</table>"
                "</div>",
                total,
                completed,
                failed,
                in_progress,
                unique_users,
                recent_downloads,
            )
        return "-"

    download_analytics.short_description = _("Download Analytics")

    def license_key_analytics(self, obj):
        """Detailed license key analytics in change form"""
        from django.utils.html import format_html

        if obj.pk:
            if not obj.requires_license:
                return format_html(
                    '<div style="padding: 12px; background: var(--darkened-bg, #f8f9fa); '
                    'border-radius: 6px; color: #666; font-size: 13px;">'
                    "🔓 License keys are not required for this asset"
                    "</div>"
                )

            licenses = LicenseKey.objects.filter(digital_asset=obj)

            if not licenses.exists():
                return format_html(
                    '<div style="padding: 12px; background: var(--warning-light, #fff3cd); '
                    'border-radius: 6px; color: #856404; font-size: 13px;">'
                    "⚠️ No license keys generated yet. Keys will be created automatically on order completion."
                    "</div>"
                )

            total = licenses.count()
            active = licenses.filter(status="active").count()
            expired = licenses.filter(status="expired").count()
            revoked = licenses.filter(status="revoked").count()
            suspended = licenses.filter(status="suspended").count()

            # Total activations
            total_activations = sum(lic.current_activations for lic in licenses)

            return format_html(
                '<div style="background: var(--darkened-bg, #f8f9fa); padding: 16px; '
                'border-radius: 6px; border: 1px solid var(--hairline-color, #e8e8e8);">'
                '<h4 style="margin: 0 0 12px 0; font-size: 14px;">License Key Analytics</h4>'
                '<table style="width: 100%; font-size: 13px; border-collapse: collapse;">'
                '<tr><td style="padding: 6px 0; font-weight: 600;">Total Keys Generated:</td><td style="padding: 6px 0;">{}</td></tr>'
                '<tr><td style="padding: 6px 0; font-weight: 600; color: #28a745;">Active:</td><td style="padding: 6px 0;">{}</td></tr>'
                '<tr><td style="padding: 6px 0; font-weight: 600; color: #dc3545;">Expired:</td><td style="padding: 6px 0;">{}</td></tr>'
                '<tr><td style="padding: 6px 0; font-weight: 600; color: #6c757d;">Revoked:</td><td style="padding: 6px 0;">{}</td></tr>'
                '<tr><td style="padding: 6px 0; font-weight: 600; color: #ffc107;">Suspended:</td><td style="padding: 6px 0;">{}</td></tr>'
                '<tr><td style="padding: 6px 0; font-weight: 600;">Total Device Activations:</td><td style="padding: 6px 0;">{}</td></tr>'
                "</table>"
                "</div>",
                total,
                active,
                expired,
                revoked,
                suspended,
                total_activations,
            )
        return "-"

    license_key_analytics.short_description = _("License Key Analytics")

    # Bulk Actions

    def activate_assets(self, request, queryset):
        """Bulk activate selected digital assets"""
        updated = queryset.update(is_active=True)
        self.message_user(request, _(f"{updated} digital asset(s) activated successfully."))

    activate_assets.short_description = _("✅ Activate selected assets")

    def deactivate_assets(self, request, queryset):
        """Bulk deactivate selected digital assets"""
        updated = queryset.update(is_active=False)
        self.message_user(request, _(f"{updated} digital asset(s) deactivated successfully."))

    deactivate_assets.short_description = _("🚫 Deactivate selected assets")

    def export_asset_report(self, request, queryset):
        """Export asset report to CSV"""
        import csv

        from django.http import HttpResponse
        from django.utils import timezone

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            f'attachment; filename="digital_assets_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        )

        writer = csv.writer(response)
        writer.writerow(
            [
                "Filename",
                "Product",
                "SKU",
                "Version",
                "File Size (MB)",
                "File Type",
                "Requires License",
                "Download Limit",
                "Expiration Days",
                "Is Active",
                "Total Downloads",
                "License Keys Generated",
                "Created",
            ]
        )

        for asset in queryset.select_related("product"):
            # Get statistics
            total_downloads = DigitalDownload.objects.filter(digital_asset=asset).count()
            license_count = (
                LicenseKey.objects.filter(digital_asset=asset).count()
                if asset.requires_license
                else 0
            )

            writer.writerow(
                [
                    asset.filename,
                    asset.product.name if asset.product else "",
                    asset.product.sku if asset.product else "",
                    asset.version,
                    f"{asset.file_size / (1024 * 1024):.2f}",
                    asset.file_type or "",
                    "Yes" if asset.requires_license else "No",
                    asset.download_limit if asset.download_limit else "Unlimited",
                    asset.expiration_days if asset.expiration_days else "Never",
                    "Yes" if asset.is_active else "No",
                    total_downloads,
                    license_count,
                    asset.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                ]
            )

        return response

    export_asset_report.short_description = _("📥 Export asset report to CSV")

    def changelist_view(self, request, extra_context=None):
        """Add digital products to context for filters"""
        extra_context = extra_context or {}

        # Get all products that have digital assets
        digital_products = (
            Product.objects.filter(digital_assets__isnull=False).distinct().order_by("name")
        )

        extra_context["digital_products"] = digital_products
        return super().changelist_view(request, extra_context=extra_context)

    class Media:
        css = {"all": ("catalog/css/admin_digital_asset.css",)}


@admin.register(DigitalDownload)
class DigitalDownloadAdmin(admin.ModelAdmin):
    """Admin for digital download tracking"""

    list_display = [
        "id",
        "digital_asset_link",
        "user_link",
        "status_badge",
        "ip_address",
        "downloaded_at",
        "file_size_display",
    ]
    list_filter = ["status", "downloaded_at"]
    search_fields = [
        "user__email",
        "user__username",
        "digital_asset__filename",
        "digital_asset__product__name",
        "order_item__order__order_number",
        "ip_address",
    ]
    readonly_fields = [
        "digital_asset",
        "order_item",
        "user",
        "ip_address",
        "user_agent",
        "downloaded_at",
        "status",
        "error_message",
        "file_version",
    ]
    date_hierarchy = "downloaded_at"
    ordering = ["-downloaded_at"]

    fieldsets = (
        (_("Download Information"), {"fields": ("digital_asset", "order_item", "user", "status")}),
        (_("Client Information"), {"fields": ("ip_address", "user_agent")}),
        (_("Timing"), {"fields": ("downloaded_at", "file_version")}),
        (_("Error Details"), {"fields": ("error_message",), "classes": ("collapse",)}),
    )

    def has_add_permission(self, request):
        """Prevent manual creation - downloads are tracked automatically"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion - maintain audit trail"""
        return False

    def digital_asset_link(self, obj):
        """Link to digital asset"""
        from django.urls import reverse
        from django.utils.html import format_html

        if obj.digital_asset:
            url = reverse("admin:catalog_digitalasset_change", args=[obj.digital_asset.id])
            return format_html('<a href="{}">{}</a>', url, obj.digital_asset.filename)
        return "-"

    digital_asset_link.short_description = _("Asset")

    def user_link(self, obj):
        """Link to user"""
        from django.urls import reverse
        from django.utils.html import format_html

        if obj.user:
            try:
                url = reverse("admin:accounts_customuser_change", args=[obj.user.id])
                return format_html('<a href="{}">{}</a>', url, obj.user.email)
            except Exception:
                return obj.user.email
        return "-"

    user_link.short_description = _("User")

    def status_badge(self, obj):
        """Display status with color badge"""
        from django.utils.html import format_html

        status_colors = {
            "initiated": "#17a2b8",
            "completed": "#28a745",
            "failed": "#dc3545",
            "expired": "#6c757d",
        }

        icons = {"initiated": "⬇️", "completed": "✅", "failed": "❌", "expired": "⏰"}

        color = status_colors.get(obj.status, "#6c757d")
        icon = icons.get(obj.status, "●")

        return format_html(
            '<span style="display: inline-flex; align-items: center; gap: 4px; '
            'color: {}; font-weight: 500;">{} {}</span>',
            color,
            icon,
            obj.get_status_display(),
        )

    status_badge.short_description = _("Status")

    def file_size_display(self, obj):
        """Display file size in human-readable format"""
        if obj.digital_asset:
            return obj.digital_asset.get_file_size_display()
        return "-"

    file_size_display.short_description = _("File Size")


# ========================================
# Gift Cards
# ========================================


class GiftCardTransactionInline(admin.TabularInline):
    """Inline for viewing gift card transaction history"""

    model = GiftCardTransaction
    extra = 0
    fields = [
        "transaction_type",
        "amount",
        "balance_after",
        "order_link",
        "notes",
        "created_at",
        "created_by",
    ]
    readonly_fields = [
        "transaction_type",
        "amount",
        "balance_after",
        "order_link",
        "notes",
        "created_at",
        "created_by",
    ]
    ordering = ["-created_at"]
    can_delete = False

    def has_add_permission(self, request, obj=None):
        """Prevent manual creation - transactions are created automatically"""
        return False

    def order_link(self, obj):
        """Link to order"""
        from django.urls import reverse
        from django.utils.html import format_html

        if obj.order:
            url = reverse("admin:orders_order_change", args=[obj.order.id])
            return format_html('<a href="{}">Order #{}</a>', url, obj.order.order_number)
        return "-"

    order_link.short_description = _("Order")

    class Media:
        css = {"all": ("catalog/css/admin_gift_card.css",)}


@admin.register(GiftCard)
class GiftCardAdmin(admin.ModelAdmin):
    """Admin interface for managing gift cards"""

    change_list_template = "admin/catalog/giftcard/change_list.html"
    change_form_template = "admin/catalog/giftcard/change_form.html"
    list_display = [
        "code",
        "status_badge",
        "balance_display",
        "recipient_email",
        "recipient_name",
        "issued_at",
        "expires_at",
        "created_at",
    ]
    list_filter = [
        "is_active",
        "expires_at",
        "issued_at",
        "created_at",
        ("product", admin.RelatedOnlyFieldListFilter),
    ]
    search_fields = ["code", "recipient_email", "recipient_name", "sender_name"]
    readonly_fields = [
        "code",
        "product_link",
        "order_item_link",
        "initial_value",
        "current_balance",
        "balance_display",
        "redemption_progress",
        "is_expired",
        "is_valid",
        "created_at",
        "issued_at",
        "first_used_at",
    ]
    fieldsets = [
        (
            _("Gift Card Information"),
            {
                "fields": ["code", "product_link", "order_item_link"],
                "classes": ["tab-details"],
            },
        ),
        (
            _("Balance"),
            {
                "fields": [
                    "initial_value",
                    "current_balance",
                    "balance_display",
                    "redemption_progress",
                ],
                "classes": ["tab-balance"],
            },
        ),
        (
            _("Recipient"),
            {
                "fields": ["recipient_email", "recipient_name", "sender_name", "message"],
                "classes": ["tab-recipient"],
            },
        ),
        (
            _("Status"),
            {
                "fields": ["is_active", "expires_at", "is_expired", "is_valid"],
                "classes": ["tab-status"],
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": ["created_at", "issued_at", "first_used_at"],
                "classes": ["tab-timestamps"],
            },
        ),
    ]
    inlines = [GiftCardTransactionInline]
    actions = ["mark_as_inactive", "send_gift_card_email"]
    date_hierarchy = "created_at"

    class Media:
        css = {"all": ("catalog/css/admin_gift_card.css", "catalog/css/giftcard_change_form.css")}
        js = ("catalog/js/giftcard_change_form.js",)

    def get_queryset(self, request):
        """Optimize queryset with related data"""
        qs = super().get_queryset(request)
        return qs.select_related("product", "order_item", "created_by")

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        if object_id:
            try:
                obj = self.get_object(request, object_id)
                if obj:
                    # Determine status string for template
                    if not obj.is_active:
                        extra_context["gc_status"] = "inactive"
                    elif obj.is_expired:
                        extra_context["gc_status"] = "expired"
                    elif obj.is_fully_redeemed:
                        extra_context["gc_status"] = "redeemed"
                    elif obj.first_used_at:
                        extra_context["gc_status"] = "partial"
                    elif obj.issued_at:
                        extra_context["gc_status"] = "issued"
                    else:
                        extra_context["gc_status"] = "active"

                    extra_context["redemption_pct"] = int(obj.redemption_percentage)
                    extra_context["transaction_count"] = obj.transactions.count()
            except Exception:
                extra_context["gc_status"] = "inactive"
                extra_context["redemption_pct"] = 0
                extra_context["transaction_count"] = 0
        return super().change_view(request, object_id, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):
        """Add statistics to the changelist view context"""
        from django.db.models import Sum
        from django.utils import timezone

        extra_context = extra_context or {}

        # Calculate gift card statistics
        all_gift_cards = GiftCard.objects.all()
        now = timezone.now()

        # Total count
        total_count = all_gift_cards.count()

        # Active count (not expired, not fully redeemed, is_active=True)
        active_count = all_gift_cards.filter(is_active=True).exclude(expires_at__lt=now).count()

        # Total balance across all active gift cards
        total_balance = (
            all_gift_cards.filter(is_active=True).aggregate(total=Sum("current_balance"))["total"]
            or 0
        )

        # Partially used count
        partially_used_count = all_gift_cards.filter(
            first_used_at__isnull=False, current_balance__gt=0, is_active=True
        ).count()

        extra_context["stats"] = {
            "total": total_count,
            "active": active_count,
            "total_balance": total_balance,
            "partially_used": partially_used_count,
        }

        return super().changelist_view(request, extra_context=extra_context)

    def status_badge(self, obj):
        """Display status with color badge"""
        from django.utils.html import format_html

        if not obj.is_active:
            status = _("Inactive")
            color = "#6c757d"
            icon_class = "fa-ban"
        elif obj.is_expired:
            status = _("Expired")
            color = "#dc3545"
            icon_class = "fa-clock"
        elif obj.is_fully_redeemed:
            status = _("Fully Redeemed")
            color = "#28a745"
            icon_class = "fa-check-circle"
        elif obj.first_used_at:
            status = _("Partially Used")
            color = "#ffc107"
            icon_class = "fa-chart-pie"
        elif obj.issued_at:
            status = _("Issued")
            color = "#17a2b8"
            icon_class = "fa-envelope"
        else:
            status = _("Created")
            color = "#6c757d"
            icon_class = "fa-file-alt"

        return format_html(
            '<span style="display: inline-flex; align-items: center; gap: 4px; '
            'color: {}; font-weight: 500;"><i class="fas {}"></i> {}</span>',
            color,
            icon_class,
            status,
        )

    status_badge.short_description = _("Status")

    def balance_display(self, obj):
        """Display current balance vs initial value"""
        from django.utils.html import format_html

        percentage = obj.redemption_percentage

        if percentage == 0:
            color = "#28a745"  # Green - full balance
        elif percentage < 50:
            color = "#17a2b8"  # Blue - mostly full
        elif percentage < 100:
            color = "#ffc107"  # Yellow - partially used
        else:
            color = "#6c757d"  # Gray - fully redeemed

        return format_html(
            '<span style="color: {}; font-weight: 500;">{} / {}</span>',
            color,
            obj.current_balance,
            obj.initial_value,
        )

    balance_display.short_description = _("Balance")

    def redemption_progress(self, obj):
        """Display redemption progress bar"""
        from django.utils.html import format_html

        percentage = obj.redemption_percentage

        if percentage == 0:
            bar_color = "#28a745"
        elif percentage < 50:
            bar_color = "#17a2b8"
        elif percentage < 100:
            bar_color = "#ffc107"
        else:
            bar_color = "#6c757d"

        return format_html(
            '<div style="display: flex; align-items: center; gap: 8px;">'
            '<div style="flex: 1; height: 20px; background: #e9ecef; border-radius: 4px; overflow: hidden;">'
            '<div style="height: 100%; background: {}; width: {}%;"></div>'
            "</div>"
            '<span style="font-weight: 500; min-width: 50px; text-align: right;">{:.0f}%</span>'
            "</div>",
            bar_color,
            percentage,
            percentage,
        )

    redemption_progress.short_description = _("Redeemed")

    def product_link(self, obj):
        """Link to product"""
        from django.urls import reverse
        from django.utils.html import format_html

        if obj.product:
            url = reverse("admin:catalog_product_change", args=[obj.product.id])
            return format_html('<a href="{}">{}</a>', url, obj.product.name)
        return "-"

    product_link.short_description = _("Product")

    def order_item_link(self, obj):
        """Link to order item"""
        from django.urls import reverse
        from django.utils.html import format_html

        if obj.order_item:
            order = obj.order_item.order
            url = reverse("admin:orders_order_change", args=[order.id])
            return format_html('<a href="{}">Order #{}</a>', url, order.order_number)
        return "-"

    order_item_link.short_description = _("Purchase Order")

    def mark_as_inactive(self, request, queryset):
        """Deactivate selected gift cards"""
        count = queryset.update(is_active=False)
        self.message_user(request, _("{count} gift card(s) marked as inactive").format(count=count))

    mark_as_inactive.short_description = _("Mark selected gift cards as inactive")

    def send_gift_card_email(self, request, queryset):
        """Send gift card emails to recipients"""
        for gift_card in queryset:
            gift_card.issue(send_email=True)
        self.message_user(
            request, _("{count} gift card email(s) sent").format(count=queryset.count())
        )

    send_gift_card_email.short_description = _("Send gift card emails")


@admin.register(GiftCardTransaction)
class GiftCardTransactionAdmin(admin.ModelAdmin):
    """Admin interface for viewing gift card transaction history"""

    change_list_template = "admin/catalog/giftcardtransaction/change_list.html"
    list_display = [
        "id",
        "gift_card_code",
        "transaction_type_badge",
        "amount_display",
        "balance_after",
        "order_link",
        "created_at",
        "created_by",
    ]
    list_filter = [
        "transaction_type",
        "created_at",
        ("gift_card", admin.RelatedOnlyFieldListFilter),
    ]
    search_fields = ["gift_card__code", "notes"]
    readonly_fields = [
        "gift_card",
        "transaction_type",
        "amount",
        "balance_after",
        "order",
        "notes",
        "created_at",
        "created_by",
    ]
    fieldsets = [
        (
            _("Transaction Information"),
            {"fields": ["gift_card", "transaction_type_badge", "amount", "balance_after"]},
        ),
        (_("Details"), {"fields": ["order", "notes", "created_at", "created_by"]}),
    ]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    class Media:
        css = {"all": ("catalog/css/admin_gift_card.css",)}

    def get_queryset(self, request):
        """Optimize queryset with related data"""
        qs = super().get_queryset(request)
        return qs.select_related("gift_card", "order", "created_by")

    def changelist_view(self, request, extra_context=None):
        """Add statistics to the changelist view context"""
        extra_context = extra_context or {}

        # Calculate transaction statistics
        all_transactions = GiftCardTransaction.objects.all()

        extra_context["stats"] = {
            "total": all_transactions.count(),
            "issued": all_transactions.filter(transaction_type="issue").count(),
            "redeemed": all_transactions.filter(transaction_type="redemption").count(),
            "refunded": all_transactions.filter(transaction_type="refund").count(),
        }

        return super().changelist_view(request, extra_context=extra_context)

    def has_add_permission(self, request):
        """Prevent manual creation - transactions are created automatically"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion - maintain audit trail"""
        return False

    def gift_card_code(self, obj):
        """Display gift card code with link"""
        from django.urls import reverse
        from django.utils.html import format_html

        url = reverse("admin:catalog_giftcard_change", args=[obj.gift_card.id])
        return format_html('<a href="{}">{}</a>', url, obj.gift_card.code)

    gift_card_code.short_description = _("Gift Card")

    def transaction_type_badge(self, obj):
        """Display transaction type with color badge"""
        from django.utils.html import format_html

        type_colors = {
            "issue": "#17a2b8",
            "redemption": "#28a745",
            "adjustment": "#ffc107",
            "refund": "#dc3545",
            "expiration": "#6c757d",
        }

        icon_classes = {
            "issue": "fa-envelope",
            "redemption": "fa-shopping-cart",
            "adjustment": "fa-sliders-h",
            "refund": "fa-undo",
            "expiration": "fa-clock",
        }

        color = type_colors.get(obj.transaction_type, "#6c757d")
        icon_class = icon_classes.get(obj.transaction_type, "fa-circle")

        return format_html(
            '<span style="display: inline-flex; align-items: center; gap: 4px; '
            'color: {}; font-weight: 500;"><i class="fas {}"></i> {}</span>',
            color,
            icon_class,
            obj.get_transaction_type_display(),
        )

    transaction_type_badge.short_description = _("Type")

    def amount_display(self, obj):
        """Display amount with color based on positive/negative"""
        from django.utils.html import format_html

        if obj.amount.amount >= 0:
            color = "#28a745"  # Green for positive
            sign = "+"
        else:
            color = "#dc3545"  # Red for negative
            sign = ""

        return format_html(
            '<span style="color: {}; font-weight: 500;">{}{}</span>', color, sign, obj.amount
        )

    amount_display.short_description = _("Amount")

    def order_link(self, obj):
        """Link to order"""
        from django.urls import reverse
        from django.utils.html import format_html

        if obj.order:
            url = reverse("admin:orders_order_change", args=[obj.order.id])
            return format_html('<a href="{}">Order #{}</a>', url, obj.order.order_number)
        return "-"

    order_link.short_description = _("Order")


# ============================================================================
# CUSTOMIZATION OPTIONS ADMIN
# ============================================================================


@admin.register(CustomizationOption)
class CustomizationOptionAdmin(admin.ModelAdmin):
    """Standalone admin for managing customization options"""

    list_display = [
        "name",
        "product",
        "option_type",
        "is_required",
        "pricing_type",
        "price_amount",
        "sort_order",
    ]
    list_filter = ["option_type", "pricing_type", "is_required", "product"]
    search_fields = ["name", "product__name", "product__sku"]
    autocomplete_fields = ["product"]
    ordering = ["product", "sort_order", "name"]

    fieldsets = (
        (_("Basic Information"), {"fields": ("product", "name", "description", "sort_order")}),
        (_("Option Configuration"), {"fields": ("option_type", "is_required")}),
        (
            _("Validation Rules"),
            {
                "fields": (
                    "max_length",
                    "allowed_file_types",
                    "max_file_size_mb",
                    "min_value",
                    "max_value",
                    "choices",
                ),
                "description": _(
                    "Configure validation rules based on option type. Text/textarea uses max_length, file uses allowed_file_types and max_file_size_mb, number uses min/max_value, select/color uses choices."
                ),
            },
        ),
        (
            _("Pricing"),
            {
                "fields": ("pricing_type", "price_amount"),
                "description": _(
                    "Configure additional pricing for this customization. For select options, you can also set per-choice price modifiers in the choices field."
                ),
            },
        ),
    )

    def get_form(self, request, obj=None, **kwargs):
        """Override to filter MoneyField currency choices"""
        form = super().get_form(request, obj, **kwargs)
        from core.admin_mixins import _apply_money_field_currency_defaults

        _apply_money_field_currency_defaults(form, obj)
        return form

    class Media:
        css = {"all": ("catalog/css/admin_customization.css",)}
        js = ("catalog/js/admin_customization.js",)


# ============================================================================
# Stock Display Settings Admin (Singleton)
# ============================================================================


@admin.register(StockDisplaySettings)
class StockDisplaySettingsAdmin(admin.ModelAdmin):
    """
    Admin for site-wide stock display settings.
    This is a singleton - only one instance should exist.
    """

    list_display = [
        "__str__",
        "out_of_stock_action",
        "allow_backorders",
        "show_stock_status",
        "updated_at",
    ]

    fieldsets = (
        (
            _("Stock Status Display"),
            {
                "fields": (
                    "show_stock_status",
                    "show_low_stock_warning",
                    "low_stock_threshold",
                    "show_exact_quantity",
                ),
                "description": _("Configure how stock status is displayed on product pages."),
            },
        ),
        (
            _("Out of Stock Behavior"),
            {
                "fields": (
                    "out_of_stock_action",
                    "out_of_stock_message",
                    "allow_backorders",
                    "backorder_message",
                ),
                "description": _(
                    "Configure default behavior when products are out of stock. These can be overridden at category and product level."
                ),
            },
        ),
        (
            _("Warehouse Display"),
            {
                "fields": ("show_ships_from", "show_estimated_delivery"),
                "description": _(
                    "Configure warehouse and delivery information shown to customers."
                ),
            },
        ),
    )

    def has_add_permission(self, request):
        """Only allow adding if no instance exists"""
        return not StockDisplaySettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Never allow deletion of stock settings"""
        return False

    def changelist_view(self, request, extra_context=None):
        """Redirect to the singleton instance"""
        settings = StockDisplaySettings.get_settings()
        from django.shortcuts import redirect
        from django.urls import reverse

        return redirect(reverse("admin:catalog_stockdisplaysettings_change", args=[settings.pk]))


# ============================================================================
# Stock Notification Admin
# ============================================================================


@admin.register(StockNotification)
class StockNotificationAdmin(admin.ModelAdmin):
    """
    Admin for managing back-in-stock notification subscriptions.
    """

    list_display = [
        "email",
        "product_name",
        "variant_name",
        "created_at",
        "notified_status",
        "notified_at",
    ]
    list_filter = ["notified_at", "created_at", "product__category"]
    search_fields = ["email", "product__name", "product__sku"]
    readonly_fields = ["created_at", "updated_at", "notified_at"]
    date_hierarchy = "created_at"
    list_per_page = 50

    fieldsets = (
        (_("Subscriber Information"), {"fields": ("email",)}),
        (_("Product"), {"fields": ("product", "variant", "preferred_warehouse")}),
        (
            _("Notification Status"),
            {
                "fields": ("notified_at", "created_at", "updated_at"),
            },
        ),
    )

    actions = ["send_notifications", "clear_sent_notifications"]

    def product_name(self, obj):
        """Display product name"""
        return obj.product.name

    product_name.short_description = _("Product")
    product_name.admin_order_field = "product__name"

    def variant_name(self, obj):
        """Display variant name if applicable"""
        if obj.variant:
            return obj.variant.name
        return "-"

    variant_name.short_description = _("Variant")

    def notified_status(self, obj):
        """Display notification status with icon"""
        from django.utils.html import format_html

        if obj.notified_at:
            return format_html('<span style="color: green;">✓</span> {}', _("Sent"))
        return format_html('<span style="color: orange;">⏳</span> {}', _("Pending"))

    notified_status.short_description = _("Status")

    @admin.action(description=_("Send notifications for selected items"))
    def send_notifications(self, request, queryset):
        """Send back-in-stock notifications for selected items"""
        from django.contrib import messages
        from django.utils import timezone

        from core.models import SiteSettings
        from email_system.services.email_sender import EmailSendingService

        settings = SiteSettings.get_settings()
        site_url = (settings.site_url or "").rstrip("/")

        # Filter to only pending notifications with in-stock products
        pending = queryset.filter(notified_at__isnull=True).select_related("product", "variant")
        sent_count = 0
        skipped_count = 0
        for notification in pending:
            # Check if product is now in stock
            if notification.product.is_in_stock:
                product_image_url = ""
                if notification.product.main_image:
                    product_image_url = f"{site_url}{notification.product.main_image.url}"

                context = {
                    "back_in_stock": {
                        "product_name": notification.product.name,
                        "variant_name": str(notification.variant) if notification.variant else "",
                        "product_url": f"{site_url}/products/{notification.product.slug}",
                        "product_image_url": product_image_url,
                        "subscriber_email": notification.email,
                    }
                }

                try:
                    outbox = EmailSendingService.send_template_email(
                        to_email=notification.email,
                        template_type="back_in_stock",
                        context=context,
                        language=settings.default_language,
                    )
                    if outbox and outbox.status != "failed":
                        notification.notified_at = timezone.now()
                        notification.save(update_fields=["notified_at"])
                        if outbox.status == "skipped":
                            skipped_count += 1
                        else:
                            sent_count += 1
                except Exception:
                    import logging

                    logging.getLogger(__name__).exception(
                        "Failed to send back-in-stock email to %s", notification.email
                    )

        if sent_count > 0:
            msg = _("Sent {} notification(s).").format(sent_count)
            if skipped_count:
                msg += " " + _("Skipped {} (user preferences).").format(skipped_count)
            messages.success(request, msg)
        elif skipped_count > 0:
            messages.info(
                request,
                _("All {} notification(s) skipped due to user preferences.").format(skipped_count),
            )
        else:
            messages.warning(
                request,
                _("No notifications to send (products still out of stock or already notified)."),
            )

    @admin.action(description=_("Clear already-sent notifications"))
    def clear_sent_notifications(self, request, queryset):
        """Delete notifications that have already been sent"""
        from django.contrib import messages

        deleted_count = queryset.filter(notified_at__isnull=False).delete()[0]
        messages.success(request, _("Deleted {} sent notification(s).").format(deleted_count))


# ============================================================================
# PRODUCT CONFIGURATOR ADMIN
# ============================================================================


@admin.register(ConfigurationSlot)
class ConfigurationSlotAdmin(admin.ModelAdmin):
    """Standalone admin for ConfigurationSlot (primarily managed via product inline)"""

    list_display = [
        "name",
        "product",
        "is_required",
        "min_selections",
        "max_selections",
        "sort_order",
    ]
    list_filter = ["is_required", "product"]
    search_fields = ["name", "product__name"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["product", "sort_order"]

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == "icon":
            from django import forms

            return forms.CharField(
                widget=IconPickerWidget(
                    priority_icons=[
                        "fa-microchip",
                        "fa-gear",
                        "fa-sliders",
                        "fa-puzzle-piece",
                        "fa-wrench",
                        "fa-cube",
                        "fa-palette",
                        "fa-memory",
                    ],
                    style_prefix=True,
                ),
                required=False,
            )
        return super().formfield_for_dbfield(db_field, request, **kwargs)


@admin.register(ConfigurationSlotOption)
class ConfigurationSlotOptionAdmin(admin.ModelAdmin):
    """Standalone admin for ConfigurationSlotOption (primarily managed via slot options view)"""

    list_display = ["option_product", "slot", "is_default", "is_popular", "sort_order"]
    list_filter = ["slot__product", "slot", "is_default", "is_popular"]
    search_fields = ["option_product__name", "slot__name"]
    autocomplete_fields = ["option_product"]
    raw_id_fields = ["option_variant"]
    ordering = ["slot", "sort_order"]


@admin.register(CompatibilityRule)
class CompatibilityRuleAdmin(admin.ModelAdmin):
    """Standalone admin for CompatibilityRule (primarily managed via compatibility matrix view)"""

    list_display = ["source_option", "rule_type", "target_slot", "configurable_product"]
    list_filter = ["rule_type", "configurable_product"]
    search_fields = ["source_option__option_product__name", "target_slot__name"]
    filter_horizontal = ["compatible_options"]
    ordering = ["configurable_product", "source_option"]


@admin.register(ConfigurationPreset)
class ConfigurationPresetAdmin(admin.ModelAdmin):
    """Standalone admin for ConfigurationPreset (primarily managed via product inline)"""

    list_display = ["name", "product", "is_featured", "sort_order"]
    list_filter = ["product", "is_featured"]
    search_fields = ["name", "product__name"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["product", "sort_order"]


# ============================================================================
# BOOKING ADMIN
# ============================================================================


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Booking management with list view and calendar view.

    Merchants can view bookings in a traditional list or as a visual calendar.
    Supports filtering by product, resource, status, and date range.
    """

    change_list_template = "admin/catalog/booking/change_list.html"
    change_form_template = "admin/catalog/booking/change_form.html"
    list_display = [
        "booking_id",
        "product_link",
        "resource",
        "customer_display",
        "start_datetime",
        "end_datetime",
        "status_badge",
        "total_cost",
    ]
    list_filter = ["status", "product", "resource", "is_recurring"]
    search_fields = [
        "customer_name",
        "customer_email",
        "customer_phone",
        "product__name",
        "resource__name",
    ]
    date_hierarchy = "start_datetime"
    ordering = ["-start_datetime"]
    readonly_fields = [
        "ical_uid",
        "recurrence_group_id",
        "created_at",
        "updated_at",
        "reminder_sent_at",
        "duration_display",
    ]
    list_per_page = 50
    actions = ["mark_confirmed", "mark_completed", "mark_no_show", "mark_cancelled"]

    fieldsets = (
        (
            _("Booking Details"),
            {
                "fields": (
                    "product",
                    "resource",
                    "status",
                    "start_datetime",
                    "end_datetime",
                    "duration_display",
                ),
            },
        ),
        (
            _("Customer"),
            {
                "fields": (
                    "customer",
                    "customer_name",
                    "customer_email",
                    "customer_phone",
                    "customer_notes",
                    "customer_timezone",
                ),
            },
        ),
        (
            _("Person Counts"),
            {
                "fields": ("persons",),
            },
        ),
        (
            _("Pricing"),
            {
                "fields": ("total_cost", "deposit_amount"),
            },
        ),
        (
            _("Order Link"),
            {
                "fields": ("order", "order_item"),
                "classes": ("collapse",),
            },
        ),
        (
            _("Cancellation"),
            {
                "fields": ("cancellation_reason",),
                "classes": ("collapse",),
            },
        ),
        (
            _("Recurring"),
            {
                "fields": ("is_recurring", "recurrence_group_id"),
                "classes": ("collapse",),
            },
        ),
        (
            _("Calendar Sync"),
            {
                "fields": ("ical_uid", "reminder_sent_at"),
                "classes": ("collapse",),
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def booking_id(self, obj):
        return f"#{obj.pk}"

    booking_id.short_description = _("ID")
    booking_id.admin_order_field = "pk"

    def product_link(self, obj):
        from django.utils.html import format_html

        url = reverse("admin:catalog_product_change", args=[obj.product_id])
        return format_html('<a href="{}">{}</a>', url, obj.product.name)

    product_link.short_description = _("Product")
    product_link.admin_order_field = "product__name"

    def customer_display(self, obj):
        if obj.customer_name:
            return f"{obj.customer_name} ({obj.customer_email})"
        return obj.customer_email or "-"

    customer_display.short_description = _("Customer")

    def status_badge(self, obj):
        from django.utils.html import format_html

        badge_classes = {
            "pending_confirmation": "list-row-card-badge list-row-card-badge-warning",
            "confirmed": "list-row-card-badge list-row-card-badge-success",
            "cancelled": "list-row-card-badge list-row-card-badge-error",
            "completed": "list-row-card-badge list-row-card-badge-primary",
            "no_show": "list-row-card-badge",
        }
        css_class = badge_classes.get(obj.status, "list-row-card-badge")
        return format_html('<span class="{}">{}</span>', css_class, obj.get_status_display())

    status_badge.short_description = _("Status")
    status_badge.admin_order_field = "status"

    def duration_display(self, obj):
        mins = obj.duration_minutes
        if mins >= 1440:
            days = mins // 1440
            return f"{days} day{'s' if days > 1 else ''}"
        elif mins >= 60:
            hours = mins // 60
            remaining = mins % 60
            if remaining:
                return f"{hours}h {remaining}m"
            return f"{hours} hour{'s' if hours > 1 else ''}"
        return f"{mins} minutes"

    duration_display.short_description = _("Duration")

    @admin.action(description=_("Mark selected as Confirmed"))
    def mark_confirmed(self, request, queryset):
        updated = queryset.filter(status__in=["pending_confirmation"]).update(status="confirmed")
        self.message_user(request, _("%d booking(s) confirmed.") % updated)

    @admin.action(description=_("Mark selected as Completed"))
    def mark_completed(self, request, queryset):
        updated = queryset.filter(status__in=["confirmed"]).update(status="completed")
        self.message_user(request, _("%d booking(s) marked as completed.") % updated)

    @admin.action(description=_("Mark selected as No Show"))
    def mark_no_show(self, request, queryset):
        updated = queryset.filter(status__in=["confirmed"]).update(status="no_show")
        self.message_user(request, _("%d booking(s) marked as no show.") % updated)

    @admin.action(description=_("Mark selected as Cancelled"))
    def mark_cancelled(self, request, queryset):
        updated = queryset.exclude(status__in=["completed", "cancelled"]).update(status="cancelled")
        self.message_user(request, _("%d booking(s) cancelled.") % updated)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        """Custom change form with dashboard layout for existing bookings."""
        extra_context = extra_context or {}

        if object_id:
            # Handle POST actions before rendering
            if request.method == "POST" and "action" in request.POST:
                return self._handle_booking_action(request, object_id)

            try:
                booking = Booking.objects.select_related(
                    "product",
                    "resource",
                    "order",
                    "customer",
                ).get(pk=object_id)

                extra_context.update(
                    {
                        "booking_notes": booking.booking_notes.select_related("author").all()[:50],
                        "order_link": (
                            reverse("admin:orders_order_change", args=[booking.order_id])
                            if booking.order_id
                            else None
                        ),
                        "product_link": reverse(
                            "admin:catalog_product_change", args=[booking.product_id]
                        ),
                        "ical_url": (
                            reverse(
                                "catalog_api:booking-ical",
                                kwargs={
                                    "product_slug": booking.product.slug,
                                    "ical_uid": booking.ical_uid,
                                },
                            )
                            if booking.ical_uid and booking.product
                            else None
                        ),
                        "can_confirm": booking.status == "pending_confirmation",
                        "can_complete": booking.status == "confirmed",
                        "can_cancel": booking.status not in ("cancelled", "completed", "no_show"),
                        "can_no_show": booking.status == "confirmed",
                        "can_reschedule": booking.status in ("pending_confirmation", "confirmed"),
                    }
                )
            except Booking.DoesNotExist:
                pass

        return super().change_view(request, object_id, form_url, extra_context)

    def _handle_booking_action(self, request, object_id):
        """Process POST actions from the booking change form."""
        from datetime import datetime as dt

        from django.contrib import messages

        from catalog.services.booking_service import BookingLifecycleService

        try:
            booking = Booking.objects.select_related("product", "resource").get(pk=object_id)
        except Booking.DoesNotExist:
            messages.error(request, _("Booking not found."))
            return HttpResponseRedirect(reverse("admin:catalog_booking_changelist"))

        action = request.POST.get("action")
        author = request.user
        redirect_url = reverse("admin:catalog_booking_change", args=[object_id])

        if action == "confirm":
            ok, msg = BookingLifecycleService.confirm_from_admin(booking, author=author)
        elif action == "complete":
            ok, msg = BookingLifecycleService.mark_completed(booking, author=author)
        elif action == "no_show":
            ok, msg = BookingLifecycleService.mark_no_show(booking, author=author)
        elif action == "cancel":
            reason = request.POST.get("cancel_reason", "")
            ok, msg = BookingLifecycleService.cancel_booking(
                booking,
                author=author,
                reason=reason,
                initiated_by="admin",
            )
        elif action == "change_status":
            new_status = request.POST.get("new_status", "")
            if not new_status:
                messages.warning(request, _("Please select a status."))
                return HttpResponseRedirect(redirect_url)
            ok, msg = BookingLifecycleService.change_status(
                booking,
                new_status,
                author=author,
            )
        elif action == "reschedule":
            new_date = request.POST.get("new_date", "")
            new_start_time = request.POST.get("new_time_start", "")
            new_end_time = request.POST.get("new_time_end", "")
            if not (new_date and new_start_time and new_end_time):
                messages.warning(request, _("Please provide date and times."))
                return HttpResponseRedirect(redirect_url)
            try:
                new_start = dt.fromisoformat(f"{new_date}T{new_start_time}").replace(
                    tzinfo=UTC,
                )
                new_end = dt.fromisoformat(f"{new_date}T{new_end_time}").replace(
                    tzinfo=UTC,
                )
            except (ValueError, TypeError):
                messages.error(request, _("Invalid date/time format."))
                return HttpResponseRedirect(redirect_url)
            ok, msg = BookingLifecycleService.reschedule_booking(
                booking,
                new_start,
                new_end,
                author=author,
            )
        elif action == "add_note":
            note_text = request.POST.get("note_text", "").strip()
            if not note_text:
                messages.warning(request, _("Note cannot be empty."))
                return HttpResponseRedirect(redirect_url)
            is_visible = bool(request.POST.get("is_customer_visible"))
            BookingLifecycleService.add_note(
                booking,
                note_text,
                author=author,
                is_customer_visible=is_visible,
            )
            messages.success(request, _("Note added."))
            return HttpResponseRedirect(redirect_url)
        else:
            messages.error(request, _("Unknown action."))
            return HttpResponseRedirect(redirect_url)

        if ok:
            messages.success(request, msg)
        else:
            messages.error(request, msg)

        return HttpResponseRedirect(redirect_url)

    def changelist_view(self, request, extra_context=None):
        """Add booking calendar data to change list context."""
        import calendar as cal_module
        from collections import defaultdict
        from datetime import date, datetime, timedelta

        extra_context = extra_context or {}

        view_mode = request.GET.get("view", "list")
        extra_context["view_mode"] = view_mode

        # Common context for all views
        extra_context["booking_products"] = Product.objects.filter(
            product_type="booking"
        ).values_list("id", "name")
        extra_context["status_choices"] = Booking.BOOKING_STATUSES
        extra_context["total_bookings"] = Booking.objects.count()

        now = timezone.now()
        year = int(request.GET.get("year", now.year))
        month = int(request.GET.get("month", now.month))
        day_num = int(request.GET.get("day", now.day))

        # Store for JS config
        extra_context["calendar_year"] = year
        extra_context["calendar_month"] = month
        extra_context["calendar_day"] = day_num

        def _apply_calendar_filters(qs):
            """Apply status/product filters to a calendar queryset."""
            status_filter = request.GET.get("status__exact")
            if status_filter:
                qs = qs.filter(status=status_filter)
            product_filter = request.GET.get("product__id__exact")
            if product_filter:
                qs = qs.filter(product_id=product_filter)
            return qs

        if view_mode == "calendar":
            # Month view
            first_day = datetime(year, month, 1, tzinfo=UTC)
            _, last_day_num = cal_module.monthrange(year, month)
            last_day = datetime(year, month, last_day_num, 23, 59, 59, tzinfo=UTC)

            bookings = (
                Booking.objects.filter(
                    start_datetime__gte=first_day,
                    start_datetime__lte=last_day,
                )
                .select_related("product", "resource", "customer")
                .order_by("start_datetime")
            )
            bookings = _apply_calendar_filters(bookings)

            bookings_by_date = defaultdict(list)
            for b in bookings:
                bookings_by_date[b.start_datetime.strftime("%Y-%m-%d")].append(b)

            cal = cal_module.Calendar(firstweekday=0)
            weeks = cal.monthdatescalendar(year, month)

            extra_context.update(
                {
                    "calendar_weeks": weeks,
                    "bookings_by_date": dict(bookings_by_date),
                    "calendar_month_name": cal_module.month_name[month],
                    "prev_month": month - 1 if month > 1 else 12,
                    "prev_year": year if month > 1 else year - 1,
                    "next_month": month + 1 if month <= 11 else 1,
                    "next_year": year if month <= 11 else year + 1,
                }
            )

        elif view_mode == "week":
            # Week view
            target_date = date(year, month, day_num)
            weekday = target_date.weekday()  # 0=Monday
            week_start = target_date - timedelta(days=weekday)
            week_end = week_start + timedelta(days=6)

            start_dt = datetime.combine(week_start, datetime.min.time()).replace(tzinfo=UTC)
            end_dt = datetime.combine(week_end, datetime.max.time()).replace(tzinfo=UTC)

            bookings = (
                Booking.objects.filter(
                    start_datetime__gte=start_dt,
                    start_datetime__lte=end_dt,
                )
                .select_related("product", "resource", "customer")
                .order_by("start_datetime")
            )
            bookings = _apply_calendar_filters(bookings)

            week_days = [week_start + timedelta(days=i) for i in range(7)]
            hours = list(range(24))

            bookings_by_day = defaultdict(list)
            for b in bookings:
                bookings_by_day[b.start_datetime.strftime("%Y-%m-%d")].append(b)

            prev_week = week_start - timedelta(days=7)
            next_week = week_start + timedelta(days=7)

            extra_context.update(
                {
                    "week_days": week_days,
                    "week_start": week_start,
                    "week_end": week_end,
                    "hours": hours,
                    "bookings_by_day": dict(bookings_by_day),
                    "prev_week": prev_week,
                    "next_week": next_week,
                }
            )

        elif view_mode == "day":
            # Day view
            target_date = date(year, month, day_num)

            start_dt = datetime.combine(target_date, datetime.min.time()).replace(tzinfo=UTC)
            end_dt = datetime.combine(target_date, datetime.max.time()).replace(tzinfo=UTC)

            bookings = (
                Booking.objects.filter(
                    start_datetime__gte=start_dt,
                    start_datetime__lte=end_dt,
                )
                .select_related("product", "resource", "customer")
                .order_by("start_datetime")
            )
            bookings = _apply_calendar_filters(bookings)

            hours = list(range(24))
            bookings_by_hour = defaultdict(list)
            for b in bookings:
                bookings_by_hour[str(b.start_datetime.hour)].append(b)

            prev_day = target_date - timedelta(days=1)
            next_day = target_date + timedelta(days=1)

            extra_context.update(
                {
                    "target_date": target_date,
                    "hours": hours,
                    "day_bookings": list(bookings),
                    "bookings_by_hour": dict(bookings_by_hour),
                    "prev_day": prev_day,
                    "next_day": next_day,
                }
            )

        # Strip custom params so Django's ChangeList doesn't reject them
        custom_params = {"view", "year", "month", "day"}
        if custom_params & set(request.GET.keys()):
            request.GET = request.GET.copy()
            for param in custom_params:
                request.GET.pop(param, None)

        return super().changelist_view(request, extra_context=extra_context)


@admin.register(BookingWaitlist)
class BookingWaitlistAdmin(admin.ModelAdmin):
    """Booking waitlist management"""

    change_list_template = "admin/catalog/bookingwaitlist/change_list.html"
    list_display = [
        "customer_email",
        "customer_name",
        "product",
        "desired_date",
        "time_range",
        "status_badge",
        "created_at",
    ]
    list_filter = ["status", "product"]
    search_fields = ["customer_email", "customer_name", "product__name"]
    date_hierarchy = "desired_date"
    ordering = ["created_at"]
    readonly_fields = ["notified_at", "created_at"]
    actions = ["notify_customers", "mark_expired"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "product",
                    "customer",
                    "customer_email",
                    "customer_name",
                    "desired_date",
                    "desired_time_start",
                    "desired_time_end",
                    "desired_persons",
                    "status",
                    "notified_at",
                    "created_at",
                ),
            },
        ),
    )

    def time_range(self, obj):
        if obj.desired_time_start and obj.desired_time_end:
            return f"{obj.desired_time_start.strftime('%H:%M')} - {obj.desired_time_end.strftime('%H:%M')}"
        elif obj.desired_time_start:
            return f"From {obj.desired_time_start.strftime('%H:%M')}"
        return _("Any time")

    time_range.short_description = _("Desired Time")

    def status_badge(self, obj):
        from django.utils.html import format_html

        badge_classes = {
            "waiting": "list-row-card-badge list-row-card-badge-warning",
            "notified": "list-row-card-badge list-row-card-badge-info",
            "booked": "list-row-card-badge list-row-card-badge-success",
            "expired": "list-row-card-badge",
        }
        css_class = badge_classes.get(obj.status, "list-row-card-badge")
        return format_html('<span class="{}">{}</span>', css_class, obj.get_status_display())

    status_badge.short_description = _("Status")

    @admin.action(description=_("Notify selected customers"))
    def notify_customers(self, request, queryset):
        updated = queryset.filter(status="waiting").update(
            status="notified",
            notified_at=timezone.now(),
        )
        self.message_user(request, _("%d customer(s) notified.") % updated)

    @admin.action(description=_("Mark selected as expired"))
    def mark_expired(self, request, queryset):
        updated = queryset.filter(status__in=["waiting", "notified"]).update(status="expired")
        self.message_user(request, _("%d waitlist entries expired.") % updated)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        from django.db.models import Count, Q

        counts = BookingWaitlist.objects.aggregate(
            waiting=Count("id", filter=Q(status="waiting")),
            notified=Count("id", filter=Q(status="notified")),
            booked=Count("id", filter=Q(status="booked")),
        )
        extra_context["stats"] = counts
        return super().changelist_view(request, extra_context=extra_context)


# ============================================================================
# Product Tags Admin
# ============================================================================


@admin.register(ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "product_count", "created_at"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["created_at"]

    def product_count(self, obj):
        return obj.products.count()

    product_count.short_description = "Products"
