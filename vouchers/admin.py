import csv

from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from django.utils.html import format_html
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum, Count, Q
from .models import VoucherCode, VoucherUsage, VoucherRestriction, GiftCard, AppliedVoucher
from .services.voucher_importer import export_queryset
from .views.import_export import (
    VoucherImportPreviewView,
    VoucherImportResultView,
    VoucherImportUploadView,
    export_vouchers_xlsx,
)


class VoucherRestrictionInline(admin.TabularInline):
    model = VoucherRestriction
    extra = 0
    fields = ['restriction_type', 'restriction_value', 'is_inclusive']


class VoucherUsageInline(admin.TabularInline):
    model = VoucherUsage
    extra = 0
    readonly_fields = ['user', 'order', 'discount_amount', 'cart_total', 'used_at']
    fields = ['user', 'order', 'discount_amount', 'cart_total', 'used_at']

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(VoucherCode)
class VoucherCodeAdmin(admin.ModelAdmin):
    change_list_template = 'admin/vouchers/vouchercode/change_list.html'
    change_form_template = 'admin/vouchers/vouchercode/change_form.html'

    list_display = [
        'code', 'name', 'discount_display', 'scope_display',
        'usage_display', 'status_display', 'expiry_display', 'created_at'
    ]
    list_filter = [
        'discount_type', 'application_scope', 'is_active',
        'exclude_sale_items', 'first_time_customers_only', 'created_at'
    ]
    search_fields = ['code', 'name', 'description']
    readonly_fields = ['current_uses', 'created_at', 'updated_at']

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('code', 'name', 'description', 'is_active')
        }),
        (_('Discount Configuration'), {
            'fields': (
                'discount_type', 'discount_value', 'max_discount_amount',
                'application_scope'
            )
        }),
        (_('Eligible Items'), {
            'fields': ('eligible_products', 'eligible_categories'),
            'classes': ('collapse',),
            'description': _('Only applies when scope is "Specific Products" or "Specific Categories"')
        }),
        (_('Validity Period'), {
            'fields': ('start_date', 'end_date', 'days_valid'),
            'description': _('Leave end_date blank for no expiry. days_valid overrides end_date.')
        }),
        (_('Usage Limits'), {
            'fields': ('max_uses_total', 'max_uses_per_customer', 'current_uses', 'min_order_value')
        }),
        (_('Restrictions & Rules'), {
            'fields': (
                'exclude_sale_items', 'cannot_combine_with_other_vouchers',
                'cannot_combine_with_sale_items', 'first_time_customers_only'
            ),
            'classes': ('collapse',)
        }),
        (_('Gift Card Settings'), {
            'fields': ('original_gift_card_value', 'gift_card_balance'),
            'classes': ('collapse',),
            'description': _('Only applies to gift card type vouchers')
        }),
        (_('Admin Info'), {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    inlines = [VoucherRestrictionInline, VoucherUsageInline]

    class Media:
        css = {
            'all': ('vouchers/css/admin-voucher-badges.css',)
        }

    def get_form(self, request, obj=None, **kwargs):
        """Override to filter MoneyField currency choices"""
        form = super().get_form(request, obj, **kwargs)
        from core.admin_mixins import _apply_money_field_currency_defaults
        _apply_money_field_currency_defaults(form, obj)
        return form

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('created_by').prefetch_related(
            'eligible_products', 'eligible_categories', 'uses'
        )

    def discount_display(self, obj):
        if obj.discount_type == 'percentage':
            display = f"{obj.discount_value}%"
            if obj.max_discount_amount:
                display += f" (max ${obj.max_discount_amount.amount})"
            css_class = 'voucher-discount voucher-discount--percentage'
        elif obj.discount_type == 'fixed':
            display = f"${obj.discount_value}"
            css_class = 'voucher-discount voucher-discount--fixed'
        elif obj.discount_type == 'gift_card':
            display = f"Gift Card ${obj.original_gift_card_value.amount if obj.original_gift_card_value else 0}"
            css_class = 'voucher-discount voucher-discount--gift-card'
        else:
            display = str(obj.discount_value)
            css_class = 'voucher-discount'

        return format_html('<span class="{}">{}</span>', css_class, display)
    discount_display.short_description = _('Discount')

    def scope_display(self, obj):
        scope_css = {
            'cart': 'voucher-scope voucher-scope--cart',
            'products': 'voucher-scope voucher-scope--products',
            'categories': 'voucher-scope voucher-scope--categories',
        }
        css_class = scope_css.get(obj.application_scope, 'voucher-scope')
        scope_text = dict(VoucherCode.APPLICATION_SCOPES)[obj.application_scope]

        return format_html('<span class="{}">{}</span>', css_class, scope_text)
    scope_display.short_description = _('Scope')

    def usage_display(self, obj):
        if obj.max_uses_total:
            percentage = (obj.current_uses / obj.max_uses_total) * 100
            if percentage >= 80:
                css_class = 'voucher-usage--full'
            elif percentage >= 60:
                css_class = 'voucher-usage--warning'
            else:
                css_class = 'voucher-usage--ok'

            return format_html(
                '<span class="{}">{}/{}</span>',
                css_class, obj.current_uses, obj.max_uses_total
            )
        else:
            return f"{obj.current_uses}/\u221e"
    usage_display.short_description = _('Uses')

    def status_display(self, obj):
        if not obj.is_active:
            return format_html(
                '<span class="voucher-status--inactive">'
                '<i class="fas fa-times-circle"></i> {}</span>',
                _('Inactive')
            )
        elif not obj.is_valid:
            return format_html(
                '<span class="voucher-status--expired">'
                '<i class="fas fa-clock"></i> {}</span>',
                _('Expired')
            )
        else:
            return format_html(
                '<span class="voucher-status--active">'
                '<i class="fas fa-check-circle"></i> {}</span>',
                _('Active')
            )
    status_display.short_description = _('Status')

    def expiry_display(self, obj):
        if not obj.end_date and not obj.days_valid:
            return format_html(
                '<span class="voucher-expiry--none">{}</span>',
                _('No expiry')
            )
        elif obj.end_date:
            now = timezone.now()
            if obj.end_date < now:
                return format_html(
                    '<span class="voucher-expiry--expired">{}</span>',
                    _('Expired')
                )
            else:
                days_left = (obj.end_date - now).days
                if days_left <= 7:
                    css_class = 'voucher-expiry--warning'
                else:
                    css_class = 'voucher-expiry--ok'
                return format_html(
                    '<span class="{}"><i class="fas fa-calendar-alt"></i> {} {}</span>',
                    css_class, days_left, _('days')
                )
        elif obj.days_valid:
            return format_html(
                '<span class="voucher-expiry--none">{} {}</span>',
                obj.days_valid, _('days from first use')
            )
        return '-'
    expiry_display.short_description = _('Expiry')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    actions = [
        'activate_vouchers', 'deactivate_vouchers',
        'export_vouchers', 'export_vouchers_xlsx',
        'clone_vouchers',
    ]

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                'import/',
                self.admin_site.admin_view(VoucherImportUploadView.as_view()),
                name='vouchers_vouchercode_import',
            ),
            path(
                'import/preview/',
                self.admin_site.admin_view(VoucherImportPreviewView.as_view()),
                name='vouchers_vouchercode_import_preview',
            ),
            path(
                'import/result/<uuid:job_id>/',
                self.admin_site.admin_view(VoucherImportResultView.as_view()),
                name='vouchers_vouchercode_import_result',
            ),
        ]
        return custom + urls

    # XLSX export wired as an admin action — symmetric with the CSV export.
    export_vouchers_xlsx = staticmethod(export_vouchers_xlsx)

    def activate_vouchers(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, _("Activated {} vouchers.").format(updated))
    activate_vouchers.short_description = _("Activate selected vouchers")

    def deactivate_vouchers(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, _("Deactivated {} vouchers.").format(updated))
    deactivate_vouchers.short_description = _("Deactivate selected vouchers")

    def export_vouchers(self, request, queryset):
        """Export selected vouchers to CSV (round-trip-compatible with the import wizard)."""
        return export_queryset(queryset, fmt='csv', filename='vouchers_export')
    export_vouchers.short_description = _("Export selected vouchers to CSV")

    def clone_vouchers(self, request, queryset):
        cloned = 0
        for original in queryset:
            # Capture M2M before clearing pk
            product_ids = list(original.eligible_products.values_list('pk', flat=True))
            category_ids = list(original.eligible_categories.values_list('pk', flat=True))

            original.pk = None
            original.code = original.generate_unique_code()
            original.name = f"Copy of {original.name}"
            original.current_uses = 0
            original.save()

            # Restore M2M relationships
            if product_ids:
                original.eligible_products.set(product_ids)
            if category_ids:
                original.eligible_categories.set(category_ids)

            cloned += 1
        self.message_user(request, _("Cloned {} vouchers.").format(cloned))
    clone_vouchers.short_description = _("Clone selected vouchers")

    def changelist_view(self, request, extra_context=None):
        """Add context for the custom change list template"""
        extra_context = extra_context or {}

        # Count active vouchers (is_active=True and not expired)
        now = timezone.now()
        active_qs = VoucherCode.objects.filter(is_active=True).filter(
            Q(end_date__isnull=True) | Q(end_date__gt=now)
        )
        extra_context['active_count'] = active_qs.count()

        # Count inactive vouchers (is_active=False or expired)
        inactive_qs = VoucherCode.objects.filter(
            Q(is_active=False) | Q(end_date__lt=now)
        )
        extra_context['inactive_count'] = inactive_qs.count()

        # Total redemptions (sum of all voucher uses)
        extra_context['total_redemptions'] = VoucherCode.objects.aggregate(
            total=Sum('current_uses')
        )['total'] or 0

        return super().changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Add dashboard context for the custom change form"""
        extra_context = extra_context or {}

        if object_id:
            try:
                voucher = VoucherCode.objects.get(pk=object_id)
                now = timezone.now()

                # Determine status
                if not voucher.is_active:
                    extra_context['voucher_status'] = 'inactive'
                elif voucher.end_date and voucher.end_date < now:
                    extra_context['voucher_status'] = 'expired'
                elif voucher.max_uses_total and voucher.current_uses >= voucher.max_uses_total:
                    extra_context['voucher_status'] = 'exhausted'
                else:
                    extra_context['voucher_status'] = 'active'

                # Usage analytics
                usage_stats = voucher.uses.aggregate(
                    total_discount=Sum('discount_amount'),
                    unique_customers=Count('user', distinct=True)
                )
                extra_context['total_discount_given'] = usage_stats['total_discount'] or 0
                extra_context['unique_customers'] = usage_stats['unique_customers'] or 0
            except VoucherCode.DoesNotExist:
                pass

        return super().change_view(request, object_id, form_url, extra_context=extra_context)


@admin.register(VoucherUsage)
class VoucherUsageAdmin(admin.ModelAdmin):
    list_display = ['voucher', 'user', 'order', 'discount_amount', 'cart_total', 'used_at']
    list_filter = ['used_at', 'voucher__discount_type']
    search_fields = ['voucher__code', 'user__username', 'user__email', 'order__order_number']
    readonly_fields = ['used_at']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'voucher', 'user', 'order'
        )


@admin.register(VoucherRestriction)
class VoucherRestrictionAdmin(admin.ModelAdmin):
    list_display = ['voucher', 'restriction_type', 'restriction_value', 'is_inclusive']
    list_filter = ['restriction_type', 'is_inclusive']
    search_fields = ['voucher__code', 'restriction_value']


@admin.register(GiftCard)
class GiftCardAdmin(admin.ModelAdmin):
    list_display = [
        'voucher_code', 'original_value', 'current_balance', 'recipient_email',
        'status', 'delivery_status', 'created_at'
    ]
    list_filter = ['status', 'is_delivered', 'send_immediately', 'created_at']
    search_fields = [
        'voucher__code', 'recipient_email', 'recipient_name', 'sender_name'
    ]
    readonly_fields = ['created_at', 'updated_at', 'delivered_at']

    fieldsets = (
        (_('Gift Card Information'), {
            'fields': ('voucher', 'status')
        }),
        (_('Recipient Details'), {
            'fields': ('recipient_email', 'recipient_name', 'sender_name', 'message')
        }),
        (_('Delivery Settings'), {
            'fields': ('send_immediately', 'delivery_date', 'is_delivered', 'delivered_at')
        }),
        (_('Purchase Information'), {
            'fields': ('purchased_by', 'purchase_order'),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    class Media:
        css = {
            'all': ('vouchers/css/admin-voucher-badges.css',)
        }

    def voucher_code(self, obj):
        return obj.voucher.code
    voucher_code.short_description = _('Code')

    def original_value(self, obj):
        return f"${obj.original_value.amount}" if obj.original_value else "$0"
    original_value.short_description = _('Original Value')

    def current_balance(self, obj):
        if obj.balance:
            css_class = 'giftcard-balance--positive' if obj.balance.amount > 0 else 'giftcard-balance--zero'
            return format_html(
                '<span class="{}">${}</span>',
                css_class, obj.balance.amount
            )
        return "$0"
    current_balance.short_description = _('Balance')

    def delivery_status(self, obj):
        if obj.is_delivered:
            return format_html(
                '<span class="giftcard-delivery--delivered">'
                '<i class="fas fa-check-circle"></i> {}</span>',
                _('Delivered')
            )
        elif obj.send_immediately:
            return format_html(
                '<span class="giftcard-delivery--pending">'
                '<i class="fas fa-clock"></i> {}</span>',
                _('Pending')
            )
        else:
            return format_html(
                '<span class="giftcard-delivery--scheduled">'
                '<i class="fas fa-calendar-alt"></i> {}</span>',
                _('Scheduled')
            )
    delivery_status.short_description = _('Delivery')


@admin.register(AppliedVoucher)
class AppliedVoucherAdmin(admin.ModelAdmin):
    list_display = ['cart', 'voucher', 'discount_amount', 'applied_at']
    list_filter = ['applied_at', 'voucher__discount_type']
    search_fields = ['voucher__code', 'cart__user__username']
    readonly_fields = ['applied_at']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'cart', 'voucher', 'cart__user'
        )
