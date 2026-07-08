from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import CustomerWallet, WalletTransaction


class WalletTransactionInline(admin.TabularInline):
    model = WalletTransaction
    extra = 0
    readonly_fields = (
        'transaction_type', 'amount', 'balance_after', 'status',
        'source', 'description', 'reference_id', 'reversed_by',
        'created_by', 'created_at',
    )
    fields = readonly_fields
    ordering = ('-created_at',)
    show_change_link = True

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(CustomerWallet)
class CustomerWalletAdmin(admin.ModelAdmin):
    list_display = (
        'customer_email', 'available_balance', 'pending_balance',
        'is_active', 'last_credited_at',
    )
    list_filter = ('is_active',)
    search_fields = ('customer__email', 'customer__first_name', 'customer__last_name')
    readonly_fields = (
        'available_balance', 'pending_balance',
        'lifetime_credited', 'lifetime_used',
        'last_credited_at', 'last_used_at',
        'created_at', 'updated_at',
    )
    inlines = [WalletTransactionInline]

    @admin.display(description=_('Customer'))
    def customer_email(self, obj):
        return obj.customer.email


@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'wallet_customer', 'transaction_type', 'amount',
        'balance_after', 'source', 'status', 'created_at',
    )
    list_filter = ('transaction_type', 'source', 'status')
    search_fields = (
        'wallet__customer__email', 'description', 'reference_id',
    )
    readonly_fields = (
        'wallet', 'transaction_type', 'amount', 'balance_after',
        'status', 'source', 'description', 'reference_id',
        'reversed_by', 'created_by', 'created_at',
    )
    date_hierarchy = 'created_at'

    @admin.display(description=_('Customer'))
    def wallet_customer(self, obj):
        return obj.wallet.customer.email

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
