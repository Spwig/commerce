"""
Loyalty Program Admin Configuration

Provides Django admin interface for loyalty program management with comprehensive
search, filtering, and management capabilities.
"""

import csv
import uuid

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.urls import reverse, path
from django.db import models
from django.db.models import Sum, Count, Q
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from datetime import timedelta

from loyalty.models import (
    LoyaltyMember,
    LoyaltyBalance,
    LoyaltyTransaction,
    LoyaltyRule,
    LoyaltyTier,
    LoyaltyBadge,
    LoyaltyMemberBadge,
    LoyaltyReward,
    LoyaltyRedemption,
    LoyaltyCampaign,
    LoyaltyCampaignExecution,
    LoyaltySegment,
    LoyaltySegmentMembership,
)
from loyalty.services.ledger_service import LedgerService
from media_library.widgets import MediaLibrarySelectWidget
from core.widgets import IconPickerWidget


# ============================================
# Inline Admin Classes
# ============================================

class LoyaltyBalanceInline(admin.StackedInline):
    """Inline for loyalty balance in member admin - displayed in dashboard cards above"""
    model = LoyaltyBalance
    extra = 0
    classes = ('collapse',)  # Collapsed by default since displayed in dashboard
    fields = (
        ('available_points', 'pending_points'),
        ('lifetime_earned', 'lifetime_redeemed', 'lifetime_expired'),
        ('last_earned_at', 'last_redeemed_at'),
    )
    readonly_fields = (
        'available_points', 'pending_points',
        'lifetime_earned', 'lifetime_redeemed', 'lifetime_expired',
        'last_earned_at', 'last_redeemed_at'
    )
    can_delete = False
    verbose_name = "Detailed Balance Record"
    verbose_name_plural = "Detailed Balance Record"

    def has_add_permission(self, request, obj=None):
        return False


class LoyaltyMemberBadgeInline(admin.TabularInline):
    """Inline for member badges"""
    model = LoyaltyMemberBadge
    extra = 0
    fields = ('badge', 'earned_at')
    readonly_fields = ('earned_at',)
    autocomplete_fields = ['badge']


class LoyaltyTransactionInline(admin.TabularInline):
    """Inline for recent transactions"""
    model = LoyaltyTransaction
    extra = 0
    max_num = 10
    fields = ('transaction_type', 'points', 'description', 'created_at')
    readonly_fields = ('transaction_type', 'points', 'description', 'created_at')
    can_delete = False
    ordering = ('-created_at',)

    def has_add_permission(self, request, obj=None):
        return False


# ============================================
# Loyalty Member Admin
# ============================================

@admin.register(LoyaltyMember)
class LoyaltyMemberAdmin(admin.ModelAdmin):
    """Admin interface for Loyalty Members"""

    change_list_template = 'admin/loyalty/loyaltymember/change_list.html'
    change_form_template = 'admin/loyalty/loyaltymember/change_form.html'

    list_display = (
        'member_id_display',
        'customer_name',
        'customer_email',
        'tier_badge',
        'points_display',
        'status_badge',
        'enrolled_at',
    )
    list_filter = (
        'is_active',
        'current_tier',
        'enrolled_at',
    )
    search_fields = (
        'customer__username',
        'customer__email',
        'customer__first_name',
        'customer__last_name',
        'uuid',
    )
    readonly_fields = (
        'uuid',
        'enrolled_at',
        'updated_at',
        'member_stats',
    )
    autocomplete_fields = ['customer', 'current_tier']

    fieldsets = (
        (_('Member Information'), {
            'fields': ('customer', 'uuid', 'current_tier', 'is_active'),
            'description': _('Basic member information. Points balance displayed in dashboard cards above.')
        }),
        (_('Statistics'), {
            'fields': ('member_stats',),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('enrolled_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    inlines = [LoyaltyBalanceInline, LoyaltyMemberBadgeInline]

    def changelist_view(self, request, extra_context=None):
        """Add tiers to context for filter dropdown"""
        extra_context = extra_context or {}
        extra_context['tiers'] = LoyaltyTier.objects.filter(is_active=True).order_by('rank')
        return super().changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Add recent transactions to context for member detail view"""
        extra_context = extra_context or {}
        if object_id:
            # Get the last 10 transactions for this member
            extra_context['recent_transactions'] = LoyaltyTransaction.objects.filter(
                member_id=object_id
            ).order_by('-created_at')[:10]
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    actions = ['activate_members', 'deactivate_members', 'export_to_csv']

    def get_urls(self):
        """Add custom URL for point adjustment"""
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:member_id>/adjust-points/',
                self.admin_site.admin_view(self.adjust_points_view),
                name='loyalty_loyaltymember_adjust_points',
            ),
        ]
        return custom_urls + urls

    def member_id_display(self, obj):
        """Display member ID with copy button"""
        return format_html(
            '<code style="font-size: 11px;">{}</code>',
            obj.id
        )
    member_id_display.short_description = _('Member ID')

    def customer_name(self, obj):
        """Display customer name with link"""
        name = obj.customer.get_full_name() or obj.customer.username
        url = reverse('admin:auth_user_change', args=[obj.customer.id])
        return format_html(
            '<a href="{}"><i class="fas fa-user"></i> {}</a>',
            url,
            name
        )
    customer_name.short_description = _('Customer')

    def customer_email(self, obj):
        """Display customer email"""
        return obj.customer.email
    customer_email.short_description = _('Email')

    def tier_badge(self, obj):
        """Display tier with colored badge"""
        if not obj.current_tier:
            return format_html(
                '<span style="color: var(--body-quiet-color);">—</span>'
            )

        return format_html(
            '<span class="badge" style="background: {}; color: white; padding: 4px 8px; border-radius: 4px;">'
            '<i class="fas fa-layer-group"></i> {}</span>',
            obj.current_tier.color or '#667eea',
            obj.current_tier.name
        )
    tier_badge.short_description = _('Tier')

    def points_display(self, obj):
        """Display available points"""
        try:
            balance = obj.balance
            return format_html(
                '<strong style="color: var(--primary);">{}</strong> <small>pts</small>',
                balance.available_points
            )
        except LoyaltyBalance.DoesNotExist:
            return '—'
    points_display.short_description = _('Points')

    def status_badge(self, obj):
        """Display status with colored badge"""
        if obj.is_active:
            return format_html(
                '<span class="badge badge-success">'
                '<i class="fas fa-check-circle"></i> {}</span>',
                _('Active')
            )
        else:
            return format_html(
                '<span class="badge badge-secondary">'
                '<i class="fas fa-times-circle"></i> {}</span>',
                _('Inactive')
            )
    status_badge.short_description = _('Status')

    def member_stats(self, obj):
        """Display comprehensive member statistics"""
        try:
            balance = obj.balance
        except LoyaltyBalance.DoesNotExist:
            return _('No balance record')

        # Get transaction counts
        txn_counts = LoyaltyTransaction.objects.filter(member=obj).aggregate(
            earn_count=Count('id', filter=Q(transaction_type=LoyaltyTransaction.TYPE_EARN)),
            redeem_count=Count('id', filter=Q(transaction_type=LoyaltyTransaction.TYPE_REDEEM)),
            total_count=Count('id')
        )

        # Get badge count
        badge_count = obj.badges_earned.count()

        return format_html(
            '<div style="line-height: 2;">'
            '<strong>{}</strong> {} | '
            '<strong>{}</strong> {} | '
            '<strong>{}</strong> {} | '
            '<strong>{}</strong> {} | '
            '<strong>{}</strong> {}'
            '</div>',
            balance.lifetime_earned,
            _('Lifetime Earned'),
            balance.lifetime_redeemed,
            _('Lifetime Redeemed'),
            balance.lifetime_expired or 0,
            _('Expired'),
            badge_count,
            _('Badges'),
            txn_counts['total_count'],
            _('Transactions')
        )
    member_stats.short_description = _('Member Statistics')

    def adjust_points_view(self, request, member_id):
        """Custom view for adjusting member points"""
        member = get_object_or_404(LoyaltyMember, id=member_id)

        if request.method == 'POST':
            points = int(request.POST.get('points', 0))
            reason = request.POST.get('reason', '')

            if points != 0 and reason:
                try:
                    ledger = LedgerService()
                    ledger.manual_adjustment(
                        member=member,
                        points=points,
                        reason=reason,
                        admin_user=request.user
                    )

                    messages.success(
                        request,
                        _('Successfully adjusted points by {} for {}').format(points, member.customer.get_full_name())
                    )
                    return HttpResponseRedirect(reverse('admin:loyalty_loyaltymember_change', args=[member_id]))
                except Exception as e:
                    messages.error(request, _('Error adjusting points: {}').format(str(e)))
            else:
                messages.error(request, _('Points and reason are required'))

        context = {
            'member': member,
            'balance': member.balance,
            'title': _('Adjust Points for {}').format(member.customer.get_full_name()),
            'opts': self.model._meta,
            'has_view_permission': self.has_view_permission(request, member),
        }

        return render(request, 'admin/loyalty/member_adjust_points.html', context)

    # Actions
    def activate_members(self, request, queryset):
        """Activate selected members"""
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            _('{} members activated').format(updated),
            messages.SUCCESS
        )
    activate_members.short_description = _('Activate selected members')

    def deactivate_members(self, request, queryset):
        """Deactivate selected members"""
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            _('{} members deactivated').format(updated),
            messages.SUCCESS
        )
    deactivate_members.short_description = _('Deactivate selected members')

    def export_to_csv(self, request, queryset):
        """Export selected members to CSV"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="loyalty_members_export.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'Member ID', 'UUID', 'Customer Name', 'Email',
            'Current Tier', 'Status', 'Enrolled At',
            'Available Points', 'Pending Points',
            'Lifetime Earned', 'Lifetime Redeemed', 'Lifetime Expired',
            'Last Earned At', 'Last Redeemed At',
        ])

        for member in queryset.select_related('customer', 'current_tier', 'balance').order_by('id'):
            try:
                balance = member.balance
            except LoyaltyBalance.DoesNotExist:
                balance = None

            writer.writerow([
                member.id,
                str(member.uuid),
                member.customer.get_full_name() or member.customer.username,
                member.customer.email,
                member.current_tier.name if member.current_tier else '',
                _('Active') if member.is_active else _('Inactive'),
                member.enrolled_at.strftime('%Y-%m-%d %H:%M:%S') if member.enrolled_at else '',
                balance.available_points if balance else 0,
                balance.pending_points if balance else 0,
                balance.lifetime_earned if balance else 0,
                balance.lifetime_redeemed if balance else 0,
                balance.lifetime_expired if balance else 0,
                balance.last_earned_at.strftime('%Y-%m-%d %H:%M:%S') if balance and balance.last_earned_at else '',
                balance.last_redeemed_at.strftime('%Y-%m-%d %H:%M:%S') if balance and balance.last_redeemed_at else '',
            ])

        self.message_user(request, _('{} members exported to CSV').format(queryset.count()), messages.SUCCESS)
        return response
    export_to_csv.short_description = _('Export to CSV')


# ============================================
# Loyalty Transaction Admin
# ============================================

@admin.register(LoyaltyTransaction)
class LoyaltyTransactionAdmin(admin.ModelAdmin):
    """Admin interface for Loyalty Transactions (Read-only)"""

    change_list_template = 'admin/loyalty/loyaltytransaction/change_list.html'

    list_display = (
        'id',
        'member_link',
        'transaction_type_badge',
        'points_display',
        'description_short',
        'created_at',
    )
    list_filter = (
        'transaction_type',
        'created_at',
    )
    search_fields = (
        'member__customer__username',
        'member__customer__email',
        'description',
        'related_object_id',
    )
    readonly_fields = (
        'member',
        'transaction_type',
        'points',
        'description',
        'related_object_type',
        'related_object_id',
        'expires_at',
        'created_at',
    )
    date_hierarchy = 'created_at'

    fieldsets = (
        (_('Transaction Details'), {
            'fields': ('member', 'transaction_type', 'points', 'description')
        }),
        (_('References'), {
            'fields': ('related_object_type', 'related_object_id'),
            'classes': ('collapse',)
        }),
        (_('Additional Information'), {
            'fields': ('expires_at', 'created_at'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        """Transactions cannot be added manually"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Transactions cannot be deleted (immutable ledger)"""
        return False

    def member_link(self, obj):
        """Link to member detail"""
        url = reverse('admin:loyalty_loyaltymember_change', args=[obj.member.id])
        name = obj.member.customer.get_full_name() or obj.member.customer.username
        return format_html('<a href="{}">{}</a>', url, name)
    member_link.short_description = _('Member')

    def transaction_type_badge(self, obj):
        """Display transaction type with badge"""
        colors = {
            LoyaltyTransaction.TYPE_EARN: 'success',
            LoyaltyTransaction.TYPE_REDEEM: 'danger',
            LoyaltyTransaction.TYPE_BONUS: 'info',
            LoyaltyTransaction.TYPE_ADJUSTMENT: 'warning',
            LoyaltyTransaction.TYPE_REVOKE: 'secondary',
            LoyaltyTransaction.TYPE_EXPIRE: 'secondary',
        }
        icons = {
            LoyaltyTransaction.TYPE_EARN: 'fa-arrow-up',
            LoyaltyTransaction.TYPE_REDEEM: 'fa-arrow-down',
            LoyaltyTransaction.TYPE_BONUS: 'fa-gift',
            LoyaltyTransaction.TYPE_ADJUSTMENT: 'fa-edit',
            LoyaltyTransaction.TYPE_REVOKE: 'fa-ban',
            LoyaltyTransaction.TYPE_EXPIRE: 'fa-clock',
        }
        return format_html(
            '<span class="badge badge-{}">'
            '<i class="fas {}"></i> {}</span>',
            colors.get(obj.transaction_type, 'secondary'),
            icons.get(obj.transaction_type, 'fa-circle'),
            obj.get_transaction_type_display()
        )
    transaction_type_badge.short_description = _('Type')

    def points_display(self, obj):
        """Display points with color"""
        if obj.points > 0:
            return format_html(
                '<strong style="color: var(--success-fg, #10b981);">+{}</strong>',
                obj.points
            )
        else:
            return format_html(
                '<strong style="color: var(--error-fg, #ef4444);">{}</strong>',
                obj.points
            )
    points_display.short_description = _('Points')

    def description_short(self, obj):
        """Truncated description"""
        if len(obj.description) > 60:
            return obj.description[:60] + '...'
        return obj.description
    description_short.short_description = _('Description')


# ============================================
# Loyalty Rule Admin
# ============================================

@admin.register(LoyaltyRule)
class LoyaltyRuleAdmin(admin.ModelAdmin):
    """Admin interface for Loyalty Rules"""

    change_list_template = 'admin/loyalty/loyaltyrule/change_list.html'
    change_form_template = 'admin/loyalty/loyaltyrule/change_form.html'

    list_display = (
        'name',
        'rule_type_badge',
        'points_rate',
        'priority',
        'status_badge',
        'date_range_display',
    )
    list_filter = (
        'is_active',
        'rule_type',
        'scope',
        'start_date',
        'end_date',
    )
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'description', 'is_active', 'priority'),
            'classes': ('tab-basic',),
        }),
        (_('Rule Configuration'), {
            'fields': (
                'rule_type',
                'scope',
                'scope_filters',
                'points_rate',
            ),
            'classes': ('tab-config',),
        }),
        (_('Conditions'), {
            'fields': (
                'min_order_amount',
                'allowed_tiers',
            ),
            'classes': ('tab-conditions',),
        }),
        (_('Limits & Restrictions'), {
            'fields': (
                'is_exclusive',
            ),
            'classes': ('tab-limits',),
        }),
        (_('Date Restrictions'), {
            'fields': ('start_date', 'end_date'),
            'classes': ('tab-dates',),
        }),
        (_('Points Behavior'), {
            'fields': ('points_pending_days', 'points_expire_days'),
            'classes': ('tab-points',),
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('tab-timestamps',),
        }),
    )

    actions = ['activate_rules', 'deactivate_rules', 'duplicate_rules']

    def rule_type_badge(self, obj):
        """Display rule type with icon"""
        icons = {
            'spend': 'fa-shopping-cart',
            'item': 'fa-box',
            'action': 'fa-bolt',
            'event': 'fa-calendar',
        }
        return format_html(
            '<i class="fas {}"></i> {}',
            icons.get(obj.rule_type, 'fa-circle'),
            obj.get_rule_type_display()
        )
    rule_type_badge.short_description = _('Type')

    def status_badge(self, obj):
        """Display status badge"""
        if obj.is_active:
            return format_html(
                '<span class="badge badge-success">'
                '<i class="fas fa-check-circle"></i> {}</span>',
                _('Active')
            )
        else:
            return format_html(
                '<span class="badge badge-secondary">'
                '<i class="fas fa-times-circle"></i> {}</span>',
                _('Inactive')
            )
    status_badge.short_description = _('Status')

    def date_range_display(self, obj):
        """Display date range"""
        if obj.start_date or obj.end_date:
            start = obj.start_date.strftime('%Y-%m-%d') if obj.start_date else '—'
            end = obj.end_date.strftime('%Y-%m-%d') if obj.end_date else '—'
            return format_html('{} → {}', start, end)
        return '—'
    date_range_display.short_description = _('Date Range')

    # Actions
    def activate_rules(self, request, queryset):
        """Activate selected rules"""
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            _('{} rules activated').format(updated),
            messages.SUCCESS
        )
    activate_rules.short_description = _('Activate selected rules')

    def deactivate_rules(self, request, queryset):
        """Deactivate selected rules"""
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            _('{} rules deactivated').format(updated),
            messages.SUCCESS
        )
    deactivate_rules.short_description = _('Deactivate selected rules')

    def duplicate_rules(self, request, queryset):
        """Duplicate selected rules"""
        cloned = 0
        for original in queryset:
            # Capture M2M before clearing pk
            tier_ids = list(original.allowed_tiers.values_list('pk', flat=True))

            original.pk = None
            original.uuid = uuid.uuid4()
            original.name = f"Copy of {original.name}"
            original.is_active = False
            original.created_by = request.user
            original.save()

            # Restore M2M relationships
            if tier_ids:
                original.allowed_tiers.set(tier_ids)

            cloned += 1

        self.message_user(request, _('{} rules duplicated').format(cloned), messages.SUCCESS)
    duplicate_rules.short_description = _('Duplicate selected rules')

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        return super().change_view(request, object_id, form_url, extra_context)


# ============================================
# Loyalty Tier Admin
# ============================================

@admin.register(LoyaltyTier)
class LoyaltyTierAdmin(admin.ModelAdmin):
    """Admin interface for Loyalty Tiers"""

    change_list_template = 'admin/loyalty/loyaltytier/change_list.html'
    change_form_template = 'admin/loyalty/loyaltytier/change_form.html'

    list_display = (
        'name',
        'rank',
        'tier_color_display',
        'thresholds_display',
        'points_multiplier',
        'members_count',
        'status_badge',
    )
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'description', 'rank', 'color', 'icon', 'is_active')
        }),
        (_('Qualification Thresholds'), {
            'fields': ('min_points_earned', 'min_spend', 'min_orders'),
            'description': _('Member qualifies if ANY threshold is met')
        }),
        (_('Benefits'), {
            'fields': ('points_multiplier',),
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        """Override form fields to use custom widgets"""
        if db_field.name == 'icon':
            from django import forms
            return forms.CharField(
                widget=IconPickerWidget(
                    priority_icons=[
                        'fa-layer-group', 'fa-medal', 'fa-crown', 'fa-trophy',
                        'fa-gem', 'fa-star', 'fa-shield', 'fa-certificate',
                    ],
                    style_prefix=False,
                ),
                required=False,
                initial='fa-layer-group',
            )
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def tier_color_display(self, obj):
        """Display tier color swatch"""
        color = obj.color or '#667eea'
        return format_html(
            '<div style="display: inline-block; width: 20px; height: 20px; '
            'background: {}; border: 1px solid var(--border-color); '
            'border-radius: 4px; vertical-align: middle;"></div>',
            color
        )
    tier_color_display.short_description = _('Color')

    def thresholds_display(self, obj):
        """Display qualification thresholds"""
        parts = []
        if obj.min_points_earned:
            parts.append(f'{obj.min_points_earned} pts')
        if obj.min_spend:
            parts.append(f'${obj.min_spend}')
        if obj.min_orders:
            parts.append(f'{obj.min_orders} orders')

        return ' | '.join(parts) if parts else '—'
    thresholds_display.short_description = _('Thresholds')

    def members_count(self, obj):
        """Count of members in this tier"""
        count = LoyaltyMember.objects.filter(current_tier=obj, is_active=True).count()
        return format_html(
            '<a href="{}?current_tier__id__exact={}">'
            '<i class="fas fa-users"></i> {}</a>',
            reverse('admin:loyalty_loyaltymember_changelist'),
            obj.id,
            count
        )
    members_count.short_description = _('Members')

    def status_badge(self, obj):
        """Display status badge"""
        if obj.is_active:
            return format_html(
                '<span class="badge badge-success">'
                '<i class="fas fa-check-circle"></i> {}</span>',
                _('Active')
            )
        else:
            return format_html(
                '<span class="badge badge-secondary">'
                '<i class="fas fa-times-circle"></i> {}</span>',
                _('Inactive')
            )
    status_badge.short_description = _('Status')


# ============================================
# Loyalty Badge Admin
# ============================================

@admin.register(LoyaltyBadge)
class LoyaltyBadgeAdmin(admin.ModelAdmin):
    """Admin interface for Loyalty Badges"""

    change_list_template = 'admin/loyalty/loyaltybadge/change_list.html'
    change_form_template = 'admin/loyalty/loyaltybadge/change_form.html'

    list_display = (
        'name',
        'badge_icon_display',
        'criteria_type',
        'points_reward',
        'earned_count',
        'status_badge',
    )
    list_filter = ('is_active', 'criteria_type')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'description', 'is_active')
        }),
        (_('Appearance'), {
            'fields': ('image', 'icon'),
            'description': _('Select an image from the media library or choose a Font Awesome icon. Image takes priority if both are provided.')
        }),
        (_('Badge Configuration'), {
            'fields': ('criteria_type', 'criteria_value', 'points_reward', 'auto_award'),
            'description': _(
                'Configure how this badge is earned. Select a criteria type from the dropdown, '
                'then set the target value. For example: "Order Count" with value "10" means '
                'the badge is earned after 10 orders. If auto_award is enabled, badges are '
                'automatically awarded when criteria is met. If disabled, badges can only be '
                'awarded through campaigns.'
            )
        }),
        (_('Display Settings'), {
            'fields': ('is_visible', 'display_order'),
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Use MediaLibrarySelectWidget for image field"""
        if db_field.name == 'image':
            from media_library.widgets import MediaLibrarySelectWidget
            from django import forms
            return forms.ModelChoiceField(
                queryset=db_field.remote_field.model.objects.all(),
                widget=MediaLibrarySelectWidget(),
                required=False
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        """Override form fields to use custom widgets"""
        if db_field.name == 'icon':
            from django import forms
            return forms.CharField(
                widget=IconPickerWidget(
                    priority_icons=[
                        'fa-medal', 'fa-trophy', 'fa-award', 'fa-star',
                        'fa-gem', 'fa-certificate', 'fa-crown', 'fa-heart',
                        'fa-fire', 'fa-bolt',
                    ],
                    style_prefix=False,
                ),
                required=False,
                initial='fa-medal',
            )
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def badge_icon_display(self, obj):
        """Display badge icon or image"""
        if obj.image and obj.image.file:
            return format_html(
                '<img src="{}" style="width: 40px; height: 40px; object-fit: contain; border-radius: 4px;" />',
                obj.image.file.url
            )
        elif obj.icon:
            return format_html('<i class="fas {} fa-2x" style="color: var(--primary);"></i>', obj.icon)
        return '—'
    badge_icon_display.short_description = _('Badge')

    def earned_count(self, obj):
        """Count of members who earned this badge"""
        count = obj.earned_by.count()
        return format_html('<i class="fas fa-medal"></i> {}', count)
    earned_count.short_description = _('Times Earned')

    def status_badge(self, obj):
        """Display status badge"""
        if obj.is_active:
            return format_html(
                '<span class="badge badge-success">'
                '<i class="fas fa-check-circle"></i> {}</span>',
                _('Active')
            )
        else:
            return format_html(
                '<span class="badge badge-secondary">'
                '<i class="fas fa-times-circle"></i> {}</span>',
                _('Inactive')
            )
    status_badge.short_description = _('Status')


# ============================================
# Loyalty Balance Admin (Read-only)
# ============================================

@admin.register(LoyaltyBalance)
class LoyaltyBalanceAdmin(admin.ModelAdmin):
    """Admin interface for Loyalty Balances (Read-only)"""

    list_display = (
        'member_link',
        'available_display',
        'pending_display',
        'lifetime_earned_display',
        'lifetime_redeemed_display',
    )
    search_fields = (
        'member__customer__username',
        'member__customer__email',
    )
    readonly_fields = (
        'member',
        'available_points',
        'pending_points',
        'lifetime_earned',
        'lifetime_redeemed',
        'lifetime_expired',
        'last_earned_at',
        'last_redeemed_at',
        'updated_at',
    )

    def has_add_permission(self, request):
        """Balances cannot be added manually"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Balances cannot be deleted"""
        return False

    def member_link(self, obj):
        """Link to member detail"""
        url = reverse('admin:loyalty_loyaltymember_change', args=[obj.member.id])
        name = obj.member.customer.get_full_name() or obj.member.customer.username
        return format_html('<a href="{}">{}</a>', url, name)
    member_link.short_description = _('Member')

    def available_display(self, obj):
        """Display available points"""
        return format_html(
            '<strong style="color: var(--primary);">{}</strong>',
            obj.available_points
        )
    available_display.short_description = _('Available')

    def pending_display(self, obj):
        """Display pending points"""
        return format_html(
            '<span style="color: var(--warning-fg, #f59e0b);">{}</span>',
            obj.pending_points
        )
    pending_display.short_description = _('Pending')

    def lifetime_earned_display(self, obj):
        """Display lifetime earned"""
        return format_html(
            '<span style="color: var(--success-fg, #10b981);">{}</span>',
            obj.lifetime_earned
        )
    lifetime_earned_display.short_description = _('Lifetime Earned')

    def lifetime_redeemed_display(self, obj):
        """Display lifetime redeemed"""
        return format_html(
            '<span style="color: var(--error-fg, #ef4444);">{}</span>',
            obj.lifetime_redeemed
        )
    lifetime_redeemed_display.short_description = _('Lifetime Redeemed')


# ============================================
# Member Badge Junction Admin
# ============================================

@admin.register(LoyaltyMemberBadge)
class LoyaltyMemberBadgeAdmin(admin.ModelAdmin):
    """Admin interface for Member Badge Awards"""

    list_display = ('member_link', 'badge', 'earned_at')
    list_filter = ('earned_at', 'badge')
    search_fields = (
        'member__customer__username',
        'member__customer__email',
        'badge__name',
    )
    readonly_fields = ('earned_at',)
    date_hierarchy = 'earned_at'

    def member_link(self, obj):
        """Link to member detail"""
        url = reverse('admin:loyalty_loyaltymember_change', args=[obj.member.id])
        name = obj.member.customer.get_full_name() or obj.member.customer.username
        return format_html('<a href="{}">{}</a>', url, name)
    member_link.short_description = _('Member')


# ============================================
# Loyalty Reward Admin
# ============================================

@admin.register(LoyaltyReward)
class LoyaltyRewardAdmin(admin.ModelAdmin):
    """Admin interface for Loyalty Rewards"""

    change_list_template = 'admin/loyalty/loyaltyreward/change_list.html'
    change_form_template = 'admin/loyalty/loyaltyreward/change_form.html'

    formfield_overrides = {
        models.ImageField: {'widget': MediaLibrarySelectWidget(attrs={'folder': 'loyalty/rewards'})},
    }

    list_display = (
        'name',
        'reward_type_display',
        'points_cost',
        'availability_status',
        'quantity_display',
        'featured_badge',
        'status_badge',
    )
    list_filter = (
        'is_active',
        'reward_type',
        'featured',
        'start_date',
        'end_date',
    )
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('uuid', 'created_at', 'updated_at', 'reward_preview')
    autocomplete_fields = ['product', 'required_tier']

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'slug', 'description', 'reward_type', 'points_cost')
        }),
        (_('Discount Configuration'), {
            'fields': ('discount_type', 'discount_value', 'min_purchase_amount'),
            'classes': ('collapse',),
            'description': _('Required for discount rewards')
        }),
        (_('Product Configuration'), {
            'fields': ('product',),
            'classes': ('collapse',),
            'description': _('Required for product rewards')
        }),
        (_('Media'), {
            'fields': ('image', 'icon'),
        }),
        (_('Availability'), {
            'fields': (
                'is_active',
                ('start_date', 'end_date'),
                ('quantity_total', 'quantity_remaining'),
                'max_redemptions_per_member',
                'required_tier',
            )
        }),
        (_('Display Settings'), {
            'fields': ('featured', 'display_order'),
        }),
        (_('Expiration'), {
            'fields': ('redemption_expires_days',),
            'classes': ('collapse',)
        }),
        (_('Terms & Conditions'), {
            'fields': ('terms',),
            'classes': ('collapse',)
        }),
        (_('Preview'), {
            'fields': ('reward_preview',),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('uuid', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['activate_rewards', 'deactivate_rewards', 'feature_rewards', 'unfeature_rewards']

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        """Override form fields to use custom widgets"""
        if db_field.name == 'icon':
            from django import forms
            return forms.CharField(
                widget=IconPickerWidget(
                    priority_icons=[
                        'fa-gift', 'fa-percent', 'fa-tag', 'fa-ticket',
                        'fa-coins', 'fa-money-bill-wave', 'fa-certificate',
                        'fa-star',
                    ],
                    style_prefix=False,
                ),
                required=False,
                initial='fa-gift',
            )
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def reward_type_display(self, obj):
        """Display reward type with icon"""
        icons = {
            'discount': 'fa-percent',
            'product': 'fa-box',
            'shipping': 'fa-truck',
            'experience': 'fa-star',
        }
        return format_html(
            '<i class="fas {}"></i> {}',
            icons.get(obj.reward_type, 'fa-gift'),
            obj.get_reward_type_display()
        )
    reward_type_display.short_description = _('Type')

    def availability_status(self, obj):
        """Display availability status"""
        if not obj.is_active:
            return format_html(
                '<span style="color: var(--body-quiet-color);">{}</span>',
                _('Inactive')
            )

        if obj.is_available():
            return format_html(
                '<span style="color: var(--success-fg, #10b981);">✓ {}</span>',
                _('Available')
            )
        else:
            return format_html(
                '<span style="color: var(--error-fg, #ef4444);">✗ {}</span>',
                _('Unavailable')
            )
    availability_status.short_description = _('Status')

    def quantity_display(self, obj):
        """Display quantity status"""
        if obj.quantity_total is None:
            return _('Unlimited')

        if obj.quantity_remaining == 0:
            return format_html(
                '<strong style="color: var(--error-fg, #ef4444);">0 / {}</strong>',
                obj.quantity_total
            )
        elif obj.quantity_remaining and obj.quantity_remaining < (obj.quantity_total * 0.2):
            return format_html(
                '<strong style="color: var(--warning-fg, #f59e0b);">{} / {}</strong>',
                obj.quantity_remaining,
                obj.quantity_total
            )
        else:
            return format_html(
                '{} / {}',
                obj.quantity_remaining,
                obj.quantity_total
            )
    quantity_display.short_description = _('Quantity')

    def featured_badge(self, obj):
        """Display featured badge"""
        if obj.featured:
            return format_html(
                '<span class="badge badge-info">'
                '<i class="fas fa-star"></i> {}</span>',
                _('Featured')
            )
        return ''
    featured_badge.short_description = _('Featured')

    def status_badge(self, obj):
        """Display status badge"""
        if obj.is_active:
            return format_html(
                '<span class="badge badge-success">'
                '<i class="fas fa-check-circle"></i> {}</span>',
                _('Active')
            )
        else:
            return format_html(
                '<span class="badge badge-secondary">'
                '<i class="fas fa-times-circle"></i> {}</span>',
                _('Inactive')
            )
    status_badge.short_description = _('Status')

    def reward_preview(self, obj):
        """Display reward preview card"""
        if obj.image:
            image_html = format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px; border-radius: 8px;" />',
                obj.image.url
            )
        else:
            image_html = format_html(
                '<i class="fas {} fa-5x" style="color: var(--primary);"></i>',
                obj.icon
            )

        return format_html(
            '<div style="background: var(--darkened-bg); padding: 1.5rem; border-radius: 8px; border: 1px solid var(--border-color);">'
            '<div style="text-align: center; margin-bottom: 1rem;">{}</div>'
            '<h3 style="margin: 0 0 0.5rem 0;">{}</h3>'
            '<p style="color: var(--body-quiet-color); margin-bottom: 1rem;">{}</p>'
            '<div style="display: flex; justify-content: space-between; align-items: center;">'
            '<strong style="color: var(--primary); font-size: 1.5rem;">{} pts</strong>'
            '<span class="badge badge-{}">{}</span>'
            '</div>'
            '</div>',
            image_html,
            obj.name,
            obj.description[:100] + '...' if len(obj.description) > 100 else obj.description,
            obj.points_cost,
            'success' if obj.is_available() else 'secondary',
            _('Available') if obj.is_available() else _('Unavailable')
        )
    reward_preview.short_description = _('Preview')

    # Actions
    def activate_rewards(self, request, queryset):
        """Activate selected rewards"""
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            _('{} rewards activated').format(updated),
            messages.SUCCESS
        )
    activate_rewards.short_description = _('Activate selected rewards')

    def deactivate_rewards(self, request, queryset):
        """Deactivate selected rewards"""
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            _('{} rewards deactivated').format(updated),
            messages.SUCCESS
        )
    deactivate_rewards.short_description = _('Deactivate selected rewards')

    def feature_rewards(self, request, queryset):
        """Mark rewards as featured"""
        updated = queryset.update(featured=True)
        self.message_user(
            request,
            _('{} rewards marked as featured').format(updated),
            messages.SUCCESS
        )
    feature_rewards.short_description = _('Mark as featured')

    def unfeature_rewards(self, request, queryset):
        """Remove featured status"""
        updated = queryset.update(featured=False)
        self.message_user(
            request,
            _('{} rewards unmarked as featured').format(updated),
            messages.SUCCESS
        )
    unfeature_rewards.short_description = _('Remove featured status')


# ============================================
# Loyalty Redemption Admin
# ============================================

@admin.register(LoyaltyRedemption)
class LoyaltyRedemptionAdmin(admin.ModelAdmin):
    """Admin interface for Loyalty Redemptions"""

    change_list_template = 'admin/loyalty/loyaltyredemption/change_list.html'

    list_display = (
        'redemption_code',
        'member_link',
        'reward_link',
        'points_spent',
        'status_badge',
        'expires_display',
        'created_at',
    )
    list_filter = (
        'status',
        'created_at',
        'expires_at',
    )
    search_fields = (
        'redemption_code',
        'member__customer__username',
        'member__customer__email',
        'reward__name',
    )
    readonly_fields = (
        'uuid',
        'redemption_code',
        'member',
        'reward',
        'points_spent',
        'transaction',
        'order',
        'voucher_code',
        'expires_at',
        'confirmed_at',
        'fulfilled_at',
        'cancelled_at',
        'created_at',
        'updated_at',
    )
    date_hierarchy = 'created_at'

    fieldsets = (
        (_('Redemption Details'), {
            'fields': ('redemption_code', 'member', 'reward', 'points_spent', 'status')
        }),
        (_('Linked Records'), {
            'fields': ('transaction', 'order', 'voucher_code'),
            'classes': ('collapse',)
        }),
        (_('Expiration'), {
            'fields': ('expires_at',),
        }),
        (_('State Tracking'), {
            'fields': ('confirmed_at', 'fulfilled_at', 'cancelled_at', 'cancellation_reason'),
            'classes': ('collapse',)
        }),
        (_('Notes'), {
            'fields': ('admin_note',),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('uuid', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_fulfilled', 'cancel_redemptions']

    def has_add_permission(self, request):
        """Redemptions should be created through the redemption service"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Redemptions cannot be deleted (audit trail)"""
        return False

    def member_link(self, obj):
        """Link to member detail"""
        url = reverse('admin:loyalty_loyaltymember_change', args=[obj.member.id])
        name = obj.member.customer.get_full_name() or obj.member.customer.username
        return format_html('<a href="{}">{}</a>', url, name)
    member_link.short_description = _('Member')

    def reward_link(self, obj):
        """Link to reward detail"""
        url = reverse('admin:loyalty_loyaltyreward_change', args=[obj.reward.id])
        return format_html('<a href="{}">{}</a>', url, obj.reward.name)
    reward_link.short_description = _('Reward')

    def status_badge(self, obj):
        """Display status with colored badge"""
        colors = {
            'pending': 'warning',
            'confirmed': 'info',
            'fulfilled': 'success',
            'cancelled': 'secondary',
            'expired': 'danger',
        }
        icons = {
            'pending': 'fa-clock',
            'confirmed': 'fa-check',
            'fulfilled': 'fa-check-double',
            'cancelled': 'fa-times',
            'expired': 'fa-hourglass-end',
        }
        return format_html(
            '<span class="badge badge-{}">'
            '<i class="fas {}"></i> {}</span>',
            colors.get(obj.status, 'secondary'),
            icons.get(obj.status, 'fa-circle'),
            obj.get_status_display()
        )
    status_badge.short_description = _('Status')

    def expires_display(self, obj):
        """Display expiration status"""
        if not obj.expires_at:
            return '—'

        if obj.is_expired():
            return format_html(
                '<span style="color: var(--error-fg, #ef4444);">✗ {}</span>',
                _('Expired')
            )
        else:
            return format_html(
                '<span style="color: var(--body-fg);">{}</span>',
                obj.expires_at.strftime('%Y-%m-%d %H:%M')
            )
    expires_display.short_description = _('Expires')

    # Actions
    def mark_fulfilled(self, request, queryset):
        """Mark redemptions as fulfilled"""
        updated = 0
        for redemption in queryset.filter(status__in=['pending', 'confirmed']):
            redemption.status = 'fulfilled'
            redemption.fulfilled_at = timezone.now()
            redemption.save()
            updated += 1

        self.message_user(
            request,
            _('{} redemptions marked as fulfilled').format(updated),
            messages.SUCCESS
        )
    mark_fulfilled.short_description = _('Mark as fulfilled')

    def cancel_redemptions(self, request, queryset):
        """Cancel selected redemptions"""
        updated = 0
        for redemption in queryset.filter(status__in=['pending', 'confirmed']):
            if redemption.can_cancel():
                redemption.status = 'cancelled'
                redemption.cancelled_at = timezone.now()
                redemption.cancellation_reason = 'Cancelled by admin'
                redemption.save()
                updated += 1

        self.message_user(
            request,
            _('{} redemptions cancelled').format(updated),
            messages.SUCCESS
        )
    cancel_redemptions.short_description = _('Cancel selected redemptions')

# ============================================================================
# CAMPAIGN & AUTOMATION ADMIN
# ============================================================================


@admin.register(LoyaltyCampaign)
class LoyaltyCampaignAdmin(admin.ModelAdmin):
    """Admin interface for loyalty campaigns"""

    change_form_template = 'admin/loyalty/loyaltycampaign/change_form.html'
    change_list_template = 'admin/loyalty/loyaltycampaign/change_list.html'

    class Media:
        css = {
            'all': ('loyalty/css/campaign-builder.css',)
        }
        js = ('loyalty/js/campaign-builder.js',)

    list_display = [
        'name',
        'campaign_type',
        'trigger_event_display',
        'status',
        'is_active',
        'total_triggered_display',
        'completion_rate_display',
        'last_triggered_at',
        'created_at'
    ]

    list_filter = [
        'status',
        'is_active',
        'campaign_type',
        'trigger_event',
        'is_journey',
        'is_ab_test',
        'created_at'
    ]

    search_fields = [
        'name',
        'slug',
        'description'
    ]

    readonly_fields = [
        'uuid',
        'total_triggered',
        'total_completed',
        'total_failed',
        'last_triggered_at',
        'created_at',
        'updated_at'
    ]

    fieldsets = [
        (_('Basic Information'), {
            'fields': [
                'uuid',
                'name',
                'slug',
                'description',
                'status',
                'is_active'
            ]
        }),
        (_('Campaign Configuration'), {
            'fields': [
                'campaign_type',
                'trigger_event',
                'trigger_conditions',
                'actions'
            ]
        }),
        (_('Journey Configuration'), {
            'fields': [
                'is_journey',
                'journey_steps'
            ],
            'classes': ['collapse']
        }),
        (_('Scheduling'), {
            'fields': [
                'schedule_type',
                'schedule_config',
                'start_date',
                'end_date'
            ],
            'classes': ['collapse']
        }),
        (_('Targeting'), {
            'fields': [
                'target_all_members',
                'target_segment',
                'target_tiers'
            ]
        }),
        (_('Limits & Controls'), {
            'fields': [
                'max_triggers_per_member',
                'cooldown_days'
            ]
        }),
        (_('A/B Testing'), {
            'fields': [
                'is_ab_test',
                'ab_variant',
                'ab_split_percentage'
            ],
            'classes': ['collapse']
        }),
        (_('Statistics'), {
            'fields': [
                'total_triggered',
                'total_completed',
                'total_failed',
                'last_triggered_at'
            ]
        }),
        (_('Metadata'), {
            'fields': [
                'created_by',
                'created_at',
                'updated_at'
            ]
        })
    ]

    filter_horizontal = ['target_tiers']

    def save_model(self, request, obj, form, change):
        """Set created_by on new campaigns"""
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def trigger_event_display(self, obj):
        """Display trigger event with badge styling"""
        if not obj.trigger_event:
            return '-'
        return format_html(
            '<span style="background: var(--primary); color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            obj.get_trigger_event_display()
        )
    trigger_event_display.short_description = _('Trigger Event')

    def total_triggered_display(self, obj):
        """Display total triggered count"""
        return format_html('<strong>{}</strong>', obj.total_triggered)
    total_triggered_display.short_description = _('Triggered')

    def completion_rate_display(self, obj):
        """Display completion rate"""
        if obj.total_triggered == 0:
            return '-'
        rate = (obj.total_completed / obj.total_triggered) * 100
        color = 'var(--success-fg)' if rate >= 80 else 'var(--warning-fg)' if rate >= 50 else 'var(--error-fg)'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{:.1f}%</span>',
            color,
            rate
        )
    completion_rate_display.short_description = _('Completion Rate')

    # Actions
    def activate_campaigns(self, request, queryset):
        """Activate selected campaigns"""
        queryset.update(is_active=True, status='active')
        self.message_user(
            request,
            _('{} campaigns activated').format(queryset.count()),
            messages.SUCCESS
        )
    activate_campaigns.short_description = _('Activate campaigns')

    def pause_campaigns(self, request, queryset):
        """Pause selected campaigns"""
        queryset.update(status='paused')
        self.message_user(
            request,
            _('{} campaigns paused').format(queryset.count()),
            messages.SUCCESS
        )
    pause_campaigns.short_description = _('Pause campaigns')

    actions = ['activate_campaigns', 'pause_campaigns']

    def changelist_view(self, request, extra_context=None):
        """Override to pass campaigns to the template"""
        extra_context = extra_context or {}
        extra_context['campaigns'] = LoyaltyCampaign.objects.all().order_by('-created_at')
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(LoyaltyCampaignExecution)
class LoyaltyCampaignExecutionAdmin(admin.ModelAdmin):
    """Admin interface for campaign executions (read-only)"""

    list_display = [
        'id',
        'campaign',
        'member_display',
        'status_display',
        'points_awarded_display',
        'current_step',
        'triggered_at',
        'completed_at'
    ]

    list_filter = [
        'status',
        'campaign',
        'triggered_at',
        'completed_at'
    ]

    search_fields = [
        'campaign__name',
        'member__customer__username',
        'member__customer__email',
        'member__customer__first_name',
        'member__customer__last_name'
    ]

    readonly_fields = [
        'uuid',
        'campaign',
        'member',
        'triggered_at',
        'completed_at',
        'status',
        'current_step',
        'next_step_at',
        'steps_completed',
        'actions_executed',
        'points_awarded',
        'rewards_issued',
        'emails_sent',
        'error_message',
        'retry_count',
        'ab_variant_assigned',
        'trigger_context'
    ]

    fieldsets = [
        (_('Execution Details'), {
            'fields': [
                'uuid',
                'campaign',
                'member',
                'status',
                'triggered_at',
                'completed_at'
            ]
        }),
        (_('Journey Progress'), {
            'fields': [
                'current_step',
                'next_step_at',
                'steps_completed'
            ]
        }),
        (_('Results'), {
            'fields': [
                'actions_executed',
                'points_awarded',
                'rewards_issued',
                'emails_sent'
            ]
        }),
        (_('Error Information'), {
            'fields': [
                'error_message',
                'retry_count'
            ],
            'classes': ['collapse']
        }),
        (_('A/B Testing'), {
            'fields': [
                'ab_variant_assigned'
            ],
            'classes': ['collapse']
        }),
        (_('Context'), {
            'fields': [
                'trigger_context'
            ],
            'classes': ['collapse']
        })
    ]

    def has_add_permission(self, request):
        """Campaign executions cannot be added manually"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Campaign executions cannot be deleted (audit trail)"""
        return False

    def member_display(self, obj):
        """Display member name with link"""
        return format_html(
            '<a href="{}">{}</a>',
            f'/admin/loyalty/loyaltymember/{obj.member.id}/change/',
            obj.member.customer.get_full_name() or obj.member.customer.username
        )
    member_display.short_description = _('Member')

    def status_display(self, obj):
        """Display status with colored badge"""
        colors = {
            'pending': 'var(--body-quiet-color)',
            'processing': 'var(--primary)',
            'completed': 'var(--success-fg)',
            'failed': 'var(--error-fg)',
            'cancelled': 'var(--body-quiet-color)'
        }
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            colors.get(obj.status, 'var(--body-fg)'),
            obj.get_status_display()
        )
    status_display.short_description = _('Status')

    def points_awarded_display(self, obj):
        """Display points awarded"""
        if obj.points_awarded == 0:
            return '-'
        return format_html(
            '<strong style="color: var(--success-fg);">+{}</strong>',
            obj.points_awarded
        )
    points_awarded_display.short_description = _('Points')


@admin.register(LoyaltySegment)
class LoyaltySegmentAdmin(admin.ModelAdmin):
    """Admin interface for customer segments"""

    change_list_template = 'admin/loyalty/loyaltysegment/change_list.html'
    change_form_template = 'admin/loyalty/loyaltysegment/change_form.html'

    list_display = [
        'name',
        'criteria_type',
        'member_count_display',
        'last_calculated_display',
        'is_active',
        'created_at'
    ]

    list_filter = [
        'criteria_type',
        'is_active',
        'created_at',
        'last_calculated_at'
    ]

    search_fields = [
        'name',
        'slug',
        'description'
    ]

    readonly_fields = [
        'uuid',
        'member_count',
        'last_calculated_at',
        'segment_preview',
        'created_at',
        'updated_at'
    ]

    fieldsets = [
        (_('Basic Information'), {
            'fields': [
                'uuid',
                'name',
                'slug',
                'description',
                'is_active'
            ],
            'classes': ('tab-basic',),
        }),
        (_('Segment Configuration'), {
            'fields': [
                'criteria_type',
                'criteria_config'
            ],
            'classes': ('tab-config',),
        }),
        (_('Statistics'), {
            'fields': [
                'member_count',
                'last_calculated_at',
                'segment_preview'
            ],
            'classes': ('tab-stats',),
        }),
        (_('Metadata'), {
            'fields': [
                'created_at',
                'updated_at'
            ],
            'classes': ('tab-metadata',),
        })
    ]

    def member_count_display(self, obj):
        """Display member count with link"""
        return format_html(
            '<strong>{}</strong> members',
            obj.member_count
        )
    member_count_display.short_description = _('Members')

    def last_calculated_display(self, obj):
        """Display last calculated timestamp"""
        if not obj.last_calculated_at:
            return format_html('<em style="color: var(--body-quiet-color);">Never</em>')
        return obj.last_calculated_at.strftime('%Y-%m-%d %H:%M')
    last_calculated_display.short_description = _('Last Calculated')

    def segment_preview(self, obj):
        """Show preview of segment members"""
        if obj.criteria_type == 'manual':
            return format_html('<em>Manual segment - members added manually</em>')

        if not obj.criteria_config:
            return format_html('<em style="color: var(--body-fg-error);">No rules configured</em>')

        try:
            from loyalty.services.segment_evaluator import SegmentEvaluator

            evaluator = SegmentEvaluator()
            qualifying_members = evaluator.get_segment_members(obj)[:10]  # Preview first 10

            if not qualifying_members:
                return format_html('<em>No members currently qualify</em>')

            html = '<div style="margin-top: 10px;">'
            html += '<strong>Sample Members ({} total):</strong><ul>'.format(obj.member_count)

            for member in qualifying_members:
                name = member.customer.get_full_name() or member.customer.email
                tier = member.current_tier.name if member.current_tier else 'No Tier'
                html += f'<li>{name} ({tier})</li>'

            if obj.member_count > 10:
                html += f'<li><em>...and {obj.member_count - 10} more</em></li>'

            html += '</ul></div>'

            return format_html(html)

        except Exception as e:
            return format_html(
                '<em style="color: var(--body-fg-error);">Error: {}</em>',
                str(e)
            )
    segment_preview.short_description = _('Preview')

    # Actions
    def refresh_memberships(self, request, queryset):
        """Refresh memberships for selected segments using SegmentEvaluator"""
        from loyalty.services.segment_evaluator import SegmentEvaluator
        from loyalty.tasks import refresh_single_segment

        evaluator = SegmentEvaluator()
        total_added = 0
        total_removed = 0

        for segment in queryset:
            if segment.criteria_type == 'manual':
                self.message_user(
                    request,
                    _('{} is a manual segment - skipped').format(segment.name),
                    messages.WARNING
                )
                continue

            try:
                # Queue async refresh
                refresh_single_segment.delay(segment.id)
                self.message_user(
                    request,
                    _('Queued refresh for segment: {}').format(segment.name),
                    messages.SUCCESS
                )
            except Exception as e:
                self.message_user(
                    request,
                    _('Error refreshing {}: {}').format(segment.name, str(e)),
                    messages.ERROR
                )

    refresh_memberships.short_description = _('Refresh segment memberships')

    actions = ['refresh_memberships']

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        return super().change_view(request, object_id, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):
        """Override to pass segments to the template"""
        extra_context = extra_context or {}
        extra_context['segments'] = LoyaltySegment.objects.all().order_by('-created_at')
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(LoyaltySegmentMembership)
class LoyaltySegmentMembershipAdmin(admin.ModelAdmin):
    """Admin interface for segment memberships"""

    list_display = [
        'segment',
        'member_display',
        'assigned_at',
        'assigned_by'
    ]

    list_filter = [
        'segment',
        'assigned_at'
    ]

    search_fields = [
        'segment__name',
        'member__customer__username',
        'member__customer__email',
        'member__customer__first_name',
        'member__customer__last_name'
    ]

    readonly_fields = [
        'assigned_at'
    ]

    fieldsets = [
        (_('Membership Details'), {
            'fields': [
                'segment',
                'member',
                'assigned_at',
                'assigned_by'
            ]
        })
    ]

    def member_display(self, obj):
        """Display member name with link"""
        return format_html(
            '<a href="{}">{}</a>',
            f'/admin/loyalty/loyaltymember/{obj.member.id}/change/',
            obj.member.customer.get_full_name() or obj.member.customer.username
        )
    member_display.short_description = _('Member')
